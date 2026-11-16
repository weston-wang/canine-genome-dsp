import numpy as np
import pytest

from canine_dsp import hsa_scenarios as hs
from canine_dsp.hsa_gap_closure import (
    ANTIGENIC_COMPETITION, BOOSTER_INTERVAL_BY_HEADROOM, DUAL_VACCINE, DUAL_VACCINE_TOLERANCE,
    DURABILITY_BAR_PER_DAY, GAP_STATUS, LOWER_THE_BAR, METRONOMIC_IMMUNE_MECHANISM,
    REAL_TRIAL_IMPLIED_MAX_KILL, ROUTE_A_ANCHORING_FAILS, tolerable_booster_interval,
)
from canine_dsp.hsa_vaccine_maintenance import immunity_schedule, run_with_schedule
from canine_dsp.mapk_resistance import drug_kill_rate, replace, run_monte_carlo

H = 3650
S, R = hs.HSA_VACCINE_START_DAY, hs.HSA_VACCINE_RAMP_DAYS
APPLICABLE = np.array([1.0, 1.0, 1.0, 1.0, 0.0])


def _durable(vmk, trials=250):
    m5, css, seeding, _ = hs.hsa_vaccine_followon_scenarios(vaccine_max_kill_values=[vmk])[vmk]
    schedule = immunity_schedule(H, S, R, vmk, APPLICABLE)
    progressed = run_with_schedule(m5, css, H, seeding, schedule, S,
                                   hs.HSA_IMMUNE_ESCAPE_SEEDING_RATE, trials=trials,
                                   preexisting_prob=hs._PREEXISTING_PROB_CENTRAL, seed=7)
    return 1 - progressed.mean()


def _agnostic_only_median_ttp(agnostic, trials=300):
    """No inhibitor, agnostic agent alone -- the arm Route A's anchor has to match."""
    model, _, seeding, _ = hs.dog_hsa_preset()
    kwargs = {}
    if agnostic > 0:
        model = replace(model, ic50_nM_2=hs.HSA_EBAT_ILLUSTRATIVE_IC50_NM, max_kill_2=agnostic)
        kwargs["css_reference_2"] = hs.HSA_EBAT_ILLUSTRATIVE_CSS_NM
    out = run_monte_carlo(model, 0.0, 1095, seeding, trials=trials,
                          preexisting_prob=hs._PREEXISTING_PROB_CENTRAL, seed=7, **kwargs)
    ttp = out.time_to_progression[out.progressed]
    return float(np.median(ttp)) if ttp.size else None


# ---------- route A: the arithmetic works, the anchoring does not ----------

def test_the_bar_does_move_by_the_agnostic_agents_kill_rate():
    """Route A's arithmetic is sound -- which is why the anchoring test below matters."""
    for agnostic, recorded in LOWER_THE_BAR.items():
        kill = float(drug_kill_rate(hs.HSA_EBAT_ILLUSTRATIVE_CSS_NM,
                                    hs.HSA_EBAT_ILLUSTRATIVE_IC50_NM, 1.5, agnostic))
        assert DURABILITY_BAR_PER_DAY - kill == pytest.approx(recorded["bar_after"], abs=0.002)


@pytest.mark.parametrize("agnostic", [0.03, 0.045])
def test_no_agnostic_rate_reproduces_the_real_metronomic_disease_free_interval(agnostic):
    """178 days is unreachable: the arm jumps from tens of days to never progressing."""
    median = _agnostic_only_median_ttp(agnostic)
    recorded = ROUTE_A_ANCHORING_FAILS["agnostic_alone_median_ttp_days"][agnostic]
    assert median == pytest.approx(recorded, abs=25)
    assert median is None or median < 120, "well short of the 178-day anchor"


def test_route_a_is_recorded_as_unsupported_with_its_own_counter_evidence():
    assert ROUTE_A_ANCHORING_FAILS["max_reachable_median_ttp_days"] < 178
    assert ROUTE_A_ANCHORING_FAILS["modelled_inhibitor_alone_median_ttp_days"] == pytest.approx(
        178, abs=15), "the real metronomic result matches the arm that does NOT clear the bar"
    assert "NOT SUPPORTED" in GAP_STATUS["route_A"]


def test_the_metronomic_mechanism_with_canine_evidence_is_immune_not_cytotoxic():
    assert "21736624" in METRONOMIC_IMMUNE_MECHANISM["treg_depletion"]
    assert "18976288" in METRONOMIC_IMMUNE_MECHANISM["clinical_signal"]
    why = METRONOMIC_IMMUNE_MECHANISM["why_it_is_not_route_A"]
    assert "rather than supplying an independent kill term" in why
    assert "no per-day kill rate follows" in why
    assert METRONOMIC_IMMUNE_MECHANISM["toxicity"]


# ---------- route B: fails under documented competition ----------

def test_the_pair_tolerates_far_less_loss_than_competition_actually_imposes():
    single = REAL_TRIAL_IMPLIED_MAX_KILL
    combined_at_tolerance = single + single * (1 - DUAL_VACCINE_TOLERANCE)
    assert combined_at_tolerance == pytest.approx(DURABILITY_BAR_PER_DAY, abs=0.001)

    weakest_documented_loss = 1 - 1 / ANTIGENIC_COMPETITION["suppression_at_2x_excess"]
    assert weakest_documented_loss == pytest.approx(0.90, abs=0.01)
    assert weakest_documented_loss > DUAL_VACCINE_TOLERANCE, "documented loss exceeds tolerance"


@pytest.mark.parametrize("combined", [0.033, 0.06])
def test_dual_vaccine_outcomes_are_recomputed(combined):
    assert _durable(combined) == pytest.approx(DUAL_VACCINE[combined]["ten_year_durable"], abs=0.07)


def test_only_perfect_additivity_clears_the_bar():
    clearing = [k for k in DUAL_VACCINE if k > DURABILITY_BAR_PER_DAY]
    assert clearing == [0.06]
    assert DUAL_VACCINE[0.06]["label"] == "perfect additivity"
    for k in DUAL_VACCINE:
        if k <= DURABILITY_BAR_PER_DAY:
            assert DUAL_VACCINE[k]["ten_year_durable"] < 0.6


def test_competition_is_interference_not_toxicity_and_cannot_be_boosted_around():
    assert ANTIGENIC_COMPETITION["resistant_to_boosting_and_adjuvants"] is True
    assert "30304673" in ANTIGENIC_COMPETITION["citation"]
    assert "not safety" in ANTIGENIC_COMPETITION["not_a_toxicity_problem"]
    assert "NOT SUPPORTED" in GAP_STATUS["route_B"]


# ---------- route C: not a route ----------

def test_booster_tolerance_is_zero_for_every_potency_that_does_not_clear_the_bar():
    """Route C presupposes the gap is already closed; it cannot close it."""
    for potency in (REAL_TRIAL_IMPLIED_MAX_KILL, 0.045, DURABILITY_BAR_PER_DAY):
        assert tolerable_booster_interval(potency, DURABILITY_BAR_PER_DAY, 180) == 0.0
    assert "NOT A ROUTE" in GAP_STATUS["route_C"]


def test_headroom_sets_the_interval_only_once_the_bar_is_cleared():
    for max_kill, row in BOOSTER_INTERVAL_BY_HEADROOM.items():
        assert max_kill > DURABILITY_BAR_PER_DAY
        assert DURABILITY_BAR_PER_DAY / max_kill == pytest.approx(row["may_decay_to"], abs=0.005)
        for half_life in (90, 180, 365):
            assert tolerable_booster_interval(max_kill, DURABILITY_BAR_PER_DAY,
                                              half_life) == pytest.approx(row[half_life], abs=1.0)
    with pytest.raises(ValueError):
        tolerable_booster_interval(0.06, DURABILITY_BAR_PER_DAY, 0)


# ---------- the honest bottom line ----------

def test_the_gap_is_recorded_as_still_open():
    assert GAP_STATUS["open"] is True
    assert all("NOT" in GAP_STATUS[k] for k in ("route_A", "route_B", "route_C"))
    assert "should be reported as a closure" in GAP_STATUS["best_remaining_lead"]
    assert "neither should" in GAP_STATUS["best_remaining_lead"]
