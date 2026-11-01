import numpy as np
import pytest
from dataclasses import replace

from canine_dsp import hsa_scenarios as hs
from canine_dsp.hsa_gap_closure import (
    BOOSTER_INTERVAL_BY_HEADROOM, COMBINED_IS_HALF_LIFE_INSENSITIVE, DUAL_VACCINE,
    DUAL_VACCINE_RATIONALE, DURABILITY_BAR_PER_DAY, LOWER_THE_BAR,
    PERSISTENT_AGNOSTIC_CANDIDATE, REAL_TRIAL_IMPLIED_MAX_KILL, tolerable_booster_interval,
)
from canine_dsp.hsa_vaccine_maintenance import immunity_schedule, run_with_schedule
from canine_dsp.mapk_resistance import drug_kill_rate

H = 3650
S, R = hs.HSA_VACCINE_START_DAY, hs.HSA_VACCINE_RAMP_DAYS
APPLICABLE = np.array([1.0, 1.0, 1.0, 1.0, 0.0])


def _durable(vmk, agnostic=0.0, half_life=None, interval=None, trials=250):
    m5, css, seeding, _ = hs.hsa_vaccine_followon_scenarios(vaccine_max_kill_values=[vmk])[vmk]
    schedule = immunity_schedule(H, S, R, vmk, APPLICABLE, half_life_days=half_life,
                                 booster_interval_days=interval)
    if agnostic > 0:
        kill = drug_kill_rate(hs.HSA_EBAT_ILLUSTRATIVE_CSS_NM, hs.HSA_EBAT_ILLUSTRATIVE_IC50_NM,
                              1.5, agnostic)
        schedule = schedule + np.full((H, 5), float(kill))
    progressed = run_with_schedule(m5, css, H, seeding, schedule, S,
                                   hs.HSA_IMMUNE_ESCAPE_SEEDING_RATE, trials=trials,
                                   preexisting_prob=hs._PREEXISTING_PROB_CENTRAL, seed=7)
    return 1 - progressed.mean()


def _agnostic_kill(agnostic):
    return float(drug_kill_rate(hs.HSA_EBAT_ILLUSTRATIVE_CSS_NM,
                                hs.HSA_EBAT_ILLUSTRATIVE_IC50_NM, 1.5, agnostic))


# ---------- route A: lower the bar instead of raising the vaccine ----------

def test_a_persistent_agnostic_agent_lowers_the_bar_by_its_own_kill_rate():
    """The bar is a difference, so it can be cleared from either side."""
    for agnostic, recorded in LOWER_THE_BAR.items():
        expected = DURABILITY_BAR_PER_DAY - _agnostic_kill(agnostic)
        assert expected == pytest.approx(recorded["bar_after"], abs=0.002)


@pytest.mark.parametrize("agnostic", [0.0, 0.03])
def test_real_vaccine_potency_reaches_durability_once_the_bar_is_lowered(agnostic):
    """Vaccine held at the real achievable 0.03/day throughout -- only the bar moves."""
    recorded = LOWER_THE_BAR[agnostic]["ten_year_durable"]
    assert _durable(REAL_TRIAL_IMPLIED_MAX_KILL, agnostic=agnostic) == pytest.approx(recorded,
                                                                                     abs=0.07)


def test_lowering_the_bar_is_monotone_and_crosses_at_the_point_the_margin_predicts():
    values = [LOWER_THE_BAR[a]["ten_year_durable"] for a in sorted(LOWER_THE_BAR)]
    assert values == sorted(values)
    crossing = [a for a in sorted(LOWER_THE_BAR)
                if LOWER_THE_BAR[a]["bar_after"] < REAL_TRIAL_IMPLIED_MAX_KILL]
    assert crossing and min(crossing) == 0.03
    assert LOWER_THE_BAR[min(crossing)]["ten_year_durable"] == pytest.approx(1.0, abs=0.02)


def test_the_persistent_agent_named_is_persistent_and_the_rejected_one_is_not():
    assert "metronomic" in PERSISTENT_AGNOSTIC_CANDIDATE["therapy"]
    assert "17708397" in PERSISTENT_AGNOSTIC_CANDIDATE["citation"]
    assert "32187827" in PERSISTENT_AGNOSTIC_CANDIDATE["rejected_alternative"]
    assert PERSISTENT_AGNOSTIC_CANDIDATE["limits"]


# ---------- route B: two independent vaccines ----------

def test_two_additive_vaccines_clear_the_bar_and_a_lossy_pair_does_not():
    assert DUAL_VACCINE[0.06]["ten_year_durable"] == pytest.approx(1.0, abs=0.02)
    assert DUAL_VACCINE[0.045]["ten_year_durable"] < 0.6
    assert 0.06 > DURABILITY_BAR_PER_DAY > 0.045


@pytest.mark.parametrize("combined", [0.045, 0.06])
def test_dual_vaccine_figures_are_recomputed(combined):
    assert _durable(combined) == pytest.approx(DUAL_VACCINE[combined]["ten_year_durable"], abs=0.07)


def test_the_two_vaccines_named_are_mechanistically_independent():
    assert "37686485" in DUAL_VACCINE_RATIONALE["vaccine_a"]
    assert "41009669" in DUAL_VACCINE_RATIONALE["vaccine_b"]
    assert "assumed, not measured" in DUAL_VACCINE_RATIONALE["caveat"]


# ---------- the link: headroom buys booster-interval tolerance ----------

def test_headroom_above_the_bar_sets_the_tolerable_interval():
    for max_kill, row in BOOSTER_INTERVAL_BY_HEADROOM.items():
        assert DURABILITY_BAR_PER_DAY / max_kill == pytest.approx(row["may_decay_to"], abs=0.005)
        for half_life in (90, 180, 365):
            computed = tolerable_booster_interval(max_kill, DURABILITY_BAR_PER_DAY, half_life)
            assert computed == pytest.approx(row[half_life], abs=1.0)


def test_more_headroom_means_a_longer_tolerable_interval():
    intervals = [BOOSTER_INTERVAL_BY_HEADROOM[k][180] for k in sorted(BOOSTER_INTERVAL_BY_HEADROOM)]
    assert intervals == sorted(intervals)
    assert intervals[-1] > 4 * intervals[0]


def test_a_vaccine_that_does_not_clear_the_bar_has_no_tolerable_interval():
    assert tolerable_booster_interval(REAL_TRIAL_IMPLIED_MAX_KILL, DURABILITY_BAR_PER_DAY, 180) == 0.0
    assert tolerable_booster_interval(DURABILITY_BAR_PER_DAY, DURABILITY_BAR_PER_DAY, 180) == 0.0
    with pytest.raises(ValueError):
        tolerable_booster_interval(0.06, DURABILITY_BAR_PER_DAY, 0)


def test_the_analytic_interval_is_conservative_against_simulation():
    """The analytic rule demands immunity stay above the bar for the whole horizon; simulation
    tolerates longer because the tumour is near-extinct before immunity first dips. Recorded so the
    analytic figure is read as the safe schedule, not the only one that works."""
    analytic = tolerable_booster_interval(0.06, DURABILITY_BAR_PER_DAY, 90)
    assert analytic == pytest.approx(20.0, abs=1.0)
    assert _durable(0.06, half_life=90, interval=90) == pytest.approx(1.0, abs=0.03)


# ---------- the combination is insensitive to the unmeasured half-life ----------

@pytest.mark.parametrize("half_life,interval", [(90, 90), (180, 60)])
def test_combination_holds_across_the_unmeasured_half_life(half_life, interval):
    recorded = COMBINED_IS_HALF_LIFE_INSENSITIVE[(half_life, interval)]
    got = _durable(REAL_TRIAL_IMPLIED_MAX_KILL, agnostic=0.03,
                   half_life=half_life, interval=interval)
    assert got == pytest.approx(recorded, abs=0.05)


def test_the_combination_beats_either_component_alone():
    combined = COMBINED_IS_HALF_LIFE_INSENSITIVE[(90, 90)]
    vaccine_alone = LOWER_THE_BAR[0.0]["ten_year_durable"]
    assert combined > vaccine_alone + 0.4
