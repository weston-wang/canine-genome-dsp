import numpy as np
import pytest
from dataclasses import replace

from canine_dsp import hsa_scenarios as hs
from canine_dsp.hsa_gap_stack import (
    BETA_BLOCKADE_EVIDENCE, CROSS_RESISTANCE_INCONSISTENCY, DURABILITY_BAR_PER_DAY,
    GROWTH_REDUCTION_REQUIRED, REAL_TRIAL_IMPLIED_MAX_KILL, STACK,
    STACK_IS_PREEXISTING_INSENSITIVE, STACK_STILL_NEEDS_THE_VACCINE,
    STACK_STOPPING_BOOSTERS, STACK_UNDER_WANING_IMMUNITY, VERDICT,
    corrected_ic50, required_growth_reduction,
)
from canine_dsp.hsa_open_route_closure import joint_durability, screened_rupture_hazard
from canine_dsp.hsa_vaccine_maintenance import (
    EVIM_MAINTENANCE_INTERVAL_DAYS, immunity_schedule, run_with_schedule,
)
from canine_dsp.mapk_resistance import clone_growth_margins

H = 3650
S, R = hs.HSA_VACCINE_START_DAY, hs.HSA_VACCINE_RAMP_DAYS
APPLICABLE = np.array([1.0, 1.0, 1.0, 1.0, 0.0])


def _scenario():
    return hs.hsa_vaccine_followon_scenarios(
        vaccine_max_kill_values=[REAL_TRIAL_IMPLIED_MAX_KILL])[REAL_TRIAL_IMPLIED_MAX_KILL]


def _build(corrected=False, growth_cut=0.0):
    m5, css, seeding, _ = _scenario()
    if corrected:
        m5 = replace(m5, ic50_nM=corrected_ic50(m5.ic50_nM[0]))
    if growth_cut:
        m5 = replace(m5, growth=m5.growth * (1 - growth_cut))
    return m5, css, seeding


def _bar(corrected=False, growth_cut=0.0):
    m5, css, _ = _build(corrected, growth_cut)
    return float(clone_growth_margins(m5, css)[:4].max())


def _durable(corrected=False, growth_cut=0.0, vmk=REAL_TRIAL_IMPLIED_MAX_KILL,
             preexisting=0.70, trials=250, half_life=None, booster=None, n_boosters=None):
    m5, css, seeding = _build(corrected, growth_cut)
    schedule = immunity_schedule(H, S, R, vmk, APPLICABLE, half_life_days=half_life,
                                 booster_interval_days=booster, n_boosters=n_boosters)
    progressed = run_with_schedule(m5, css, H, seeding, schedule, S,
                                   hs.HSA_IMMUNE_ESCAPE_SEEDING_RATE, trials=trials,
                                   preexisting_prob=preexisting, seed=7)
    return 1 - progressed.mean()


# ---------- component 1: the inconsistency ----------

def test_the_two_high_resistance_clones_are_rapalog_mechanisms():
    """The module's own text calls them rapalog routes; the potency anchor is ATP-competitive."""
    as_written = CROSS_RESISTANCE_INCONSISTENCY["as_written"]
    assert as_written["pi3k_akt_feedback_reactivation"] == 35.0
    assert as_written["target_site_mutation"] == 50.0
    m5, _, _, _ = _scenario()
    ratios = m5.ic50_nM / m5.ic50_nM[0]
    assert ratios[1] == pytest.approx(35.0, abs=0.1)
    assert ratios[3] == pytest.approx(50.0, abs=0.1)
    assert "30011343" in CROSS_RESISTANCE_INCONSISTENCY["potency_source"]
    assert "18704194" in CROSS_RESISTANCE_INCONSISTENCY["feedback_evidence"]
    assert "22520976" in CROSS_RESISTANCE_INCONSISTENCY["class_rationale"]


def test_correcting_the_ratios_lowers_the_bar_but_does_not_close_the_gap():
    assert _bar() == pytest.approx(CROSS_RESISTANCE_INCONSISTENCY["bar_as_written"], abs=0.002)
    corrected = _bar(corrected=True)
    assert corrected == pytest.approx(CROSS_RESISTANCE_INCONSISTENCY["bar_corrected"], abs=0.002)
    assert corrected < DURABILITY_BAR_PER_DAY
    assert corrected > REAL_TRIAL_IMPLIED_MAX_KILL, "still short on its own"


def test_the_residual_bar_is_potency_limited_above_a_hard_efficacy_floor():
    """Under the MEASURED ratios the kinase-domain clone binds at 9.5x, so potency still has room --
    but only down to the max_kill floor, which no IC50 change can pass."""
    measured = _bar(corrected=True)
    m5, css, _ = _build(corrected=True)
    no_resistance = replace(m5, ic50_nM=corrected_ic50(m5.ic50_nM[0], [1.0, 1.0, 1.0, 1.0]))
    floor = float(clone_growth_margins(no_resistance, css)[:4].max())
    assert floor < measured - 0.004, "potency is still doing work at the measured ratios"
    assert floor == pytest.approx(CROSS_RESISTANCE_INCONSISTENCY["bar_at_the_efficacy_floor"],
                                  abs=0.004)
    assert floor > REAL_TRIAL_IMPLIED_MAX_KILL, "even a perfect drug leaves the vaccine short"
    assert "efficacy floor" in CROSS_RESISTANCE_INCONSISTENCY["residual_is_set_by"]


def test_corrected_ic50_shape_and_validation():
    vector = corrected_ic50(500.0)
    assert vector.shape == (5,)
    assert vector[4] == vector[1], "escape clone inherits clone 1"
    with pytest.raises(ValueError):
        corrected_ic50(500.0, [1.0, 1.0])


# ---------- component 2: growth reduction ----------

def test_the_correction_cuts_the_growth_reduction_ask_but_by_less_than_first_claimed():
    with_it = GROWTH_REDUCTION_REQUIRED["with_correction"]
    without = GROWTH_REDUCTION_REQUIRED["without_correction"]
    assert _bar(corrected=True, growth_cut=with_it + 0.01) < REAL_TRIAL_IMPLIED_MAX_KILL
    assert _bar(corrected=True, growth_cut=with_it - 0.02) > REAL_TRIAL_IMPLIED_MAX_KILL
    assert _bar(growth_cut=without + 0.01) < REAL_TRIAL_IMPLIED_MAX_KILL
    assert without / with_it == pytest.approx(1.43, abs=0.1), "measured ratios, not the flat guess"
    assert with_it > 0.25, "the ask is still large -- see hsa_growth_pharmacodynamics" 


def test_required_growth_reduction_helper_matches_its_own_definition():
    assert required_growth_reduction(0.0385, 0.03) == pytest.approx(0.221, abs=0.005)
    assert required_growth_reduction(0.0515, 0.03) == pytest.approx(0.417, abs=0.005)
    with pytest.raises(ValueError):
        required_growth_reduction(0.03, 0.05)


def test_beta_blockade_records_the_large_canine_negative_alongside_the_positives():
    assert "40386412" in BETA_BLOCKADE_EVIDENCE["canine_negative"]
    assert "did not appear to influence" in BETA_BLOCKADE_EVIDENCE["canine_negative"]
    assert "27211551" in BETA_BLOCKADE_EVIDENCE["human_angiosarcoma"]
    assert "VINBLASTINE" in BETA_BLOCKADE_EVIDENCE["partner_matters"]
    assert "DOXORUBICIN" in BETA_BLOCKADE_EVIDENCE["partner_matters"]
    assert "not what any study reports" in BETA_BLOCKADE_EVIDENCE["what_is_not_established"]


# ---------- the stack ----------

@pytest.mark.parametrize("key,corrected,cut", [
    ("vaccine_only", False, 0.0),
    ("correction_only", True, 0.0),
    ("growth_cut_20pct_only", False, 0.20),
    ("correction_plus_20pct", True, 0.20),
])
def test_stack_rows_are_recomputed(key, corrected, cut):
    row = STACK[key]
    assert _bar(corrected, cut) == pytest.approx(row["bar"], abs=0.003)
    assert _durable(corrected, cut) == pytest.approx(row["ten_year_durable"], abs=0.08)


def test_no_component_closes_the_gap_alone_but_together_they_do():
    alone = [STACK["vaccine_only"], STACK["correction_only"], STACK["growth_cut_20pct_only"]]
    for row in alone:
        assert row["bar"] > REAL_TRIAL_IMPLIED_MAX_KILL
        assert row["ten_year_durable"] < 0.7
    combined = STACK["correction_plus_20pct"]
    assert combined["bar"] < REAL_TRIAL_IMPLIED_MAX_KILL
    assert combined["ten_year_durable"] == pytest.approx(1.0, abs=0.02)


def test_the_stack_does_not_depend_on_the_unmeasurable_parameter():
    for preexisting, recorded in STACK_IS_PREEXISTING_INSENSITIVE.items():
        assert _durable(True, 0.20, preexisting=preexisting) == pytest.approx(recorded, abs=0.05)


@pytest.mark.parametrize("vmk", [0.0, 0.03])
def test_the_vaccine_remains_load_bearing_inside_the_stack(vmk):
    """The stack is not a way of doing without the vaccine."""
    assert _durable(True, 0.20, vmk=vmk) == pytest.approx(
        STACK_STILL_NEEDS_THE_VACCINE[vmk], abs=0.08)
    assert STACK_STILL_NEEDS_THE_VACCINE[0.0] < 0.35


def test_the_verdict_names_what_is_still_unmeasured_and_the_next_experiment():
    assert VERDICT["closes"] is True
    assert "unmeasured" in VERDICT["what_is_still_unmeasured"] or \
           "no study reports" in VERDICT["what_is_still_unmeasured"]
    assert "vinblastine" in VERDICT["next_experiment"]
    assert "1.43x" in VERDICT["why_the_correction_matters_most"]


# ---------- what the headline 1.000 leaves out ----------

def test_the_stack_collapses_without_boosters_at_every_half_life():
    """The headline 1.000 used the engine's no-waning default. Waning is not the problem;
    unboosted waning is."""
    for half_life, row in STACK_UNDER_WANING_IMMUNITY.items():
        if half_life is None:
            assert row["no_boosters"] == pytest.approx(1.0, abs=0.02)
            continue
        assert row["no_boosters"] < 0.35, "falls to roughly the no-vaccine level"
        assert row["q60d"] == pytest.approx(1.0, abs=0.02), "eVim's real schedule holds it"
    assert STACK_UNDER_WANING_IMMUNITY[90]["q180d"] < 0.6, \
        "q180d is not enough if immunity really lasts only 90 days"


@pytest.mark.parametrize("half_life", [180, 90])
def test_the_q60d_stack_reproduces_under_waning(half_life):
    recorded = STACK_UNDER_WANING_IMMUNITY[half_life]["q60d"]
    assert _durable(True, 0.20, half_life=half_life,
                    booster=EVIM_MAINTENANCE_INTERVAL_DAYS) == pytest.approx(recorded, abs=0.06)


def test_boosting_is_maintenance_not_a_tapering_course():
    assert STACK_STOPPING_BOOSTERS[1] < STACK_STOPPING_BOOSTERS[2] < STACK_STOPPING_BOOSTERS[5]
    assert STACK_STOPPING_BOOSTERS[5] < 0.75, "even five years of boosters does not buy ten"
    assert STACK_STOPPING_BOOSTERS[10] == pytest.approx(1.0, abs=0.02)
    n = int(2 * 365 / EVIM_MAINTENANCE_INTERVAL_DAYS)
    assert _durable(True, 0.20, half_life=180, booster=EVIM_MAINTENANCE_INTERVAL_DAYS,
                    n_boosters=n) == pytest.approx(STACK_STOPPING_BOOSTERS[2], abs=0.10)


def test_tumour_control_is_not_survival_once_rupture_is_carried_as_a_competing_hazard():
    """`joint_durability` is multiplicative: a controlled tumour does not stop a bleed."""
    unscreened = joint_durability(1.0, 0.05, years=10)["joint_durability"]
    assert unscreened == pytest.approx(0.599, abs=0.005), "1.000 control is not 1.000 survival"
    low, high = 0.784, 0.909  # CANDiD sensitivity band for the aggressive-cancer group
    for sensitivity, floor in ((low, 0.85), (high, 0.94)):
        residual = screened_rupture_hazard(0.05, sensitivity)["residual_hazard"]
        assert joint_durability(1.0, residual, years=10)["joint_durability"] > floor
    caveat = VERDICT["the_stack_figure_is_freedom_from_regrowth_not_survival"]
    assert "freedom from regrowth" in caveat
    assert "Screening is a third load-bearing component" in caveat


def test_the_verdict_says_boosters_are_required():
    assert "q60d for the full ten years" in VERDICT["stack"]
    assert "0.244/0.388/0.668" in VERDICT["boosters_are_required_not_optional"]
