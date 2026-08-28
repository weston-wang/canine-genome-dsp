import numpy as np
import pytest

from canine_dsp.antigen_convergence import (
    ANTIGEN_RETENTION,
    CONVERGENCE_ARGUMENT,
    handoff_timing,
    mechanism_constraint_matrix,
    verify_antigen_convergence,
)
from canine_dsp.mapk_resistance import ramping_kill_schedule
from canine_dsp.mapk_scenarios import VACCINE_CLONE_NAMES


def _engine_schedule(vaccine_max_kill=0.05, horizon=730, start=90, ramp=21.0):
    """Build the vaccine kill schedule exactly the way run_monte_carlo_with_vaccine does."""
    applicable = np.ones(len(VACCINE_CLONE_NAMES))
    applicable[-1] = 0.0
    return ramping_kill_schedule(horizon, start, ramp, vaccine_max_kill, applicable)


def test_every_drug_resistance_route_retains_the_vaccine_target_antigen():
    """The convergence argument in data form: resistance to a MEK inhibitor is acquired by adding a
    lesion or bypassing a node, never by shedding the driver hotspot. Only a separate antigen-loss
    event evades an anti-hotspot response."""
    assert ANTIGEN_RETENTION["pathway_reactivation"]["retains_driver_antigen"] is True
    assert ANTIGEN_RETENTION["rtk_bypass"]["retains_driver_antigen"] is True
    assert ANTIGEN_RETENTION["target_site_mutation"]["retains_driver_antigen"] is True
    assert ANTIGEN_RETENTION["immune_escape"]["retains_driver_antigen"] is False
    evaders = [n for n, v in ANTIGEN_RETENTION.items() if not v["retains_driver_antigen"]]
    assert evaders == ["immune_escape"]


def test_engine_kill_mask_actually_matches_the_convergence_claim():
    """The claim is structural, so it is checked against the engine's real mask rather than inferred
    from an outcome. If a future change excluded a drug-resistance clone from vaccine coverage, the
    whole argument would silently stop holding -- this is what catches that."""
    report = verify_antigen_convergence(VACCINE_CLONE_NAMES, _engine_schedule())
    assert report["consistent"] is True
    assert report["mismatches"] == []
    assert report["all_drug_resistance_routes_covered"] is True
    assert report["n_routes_evading_vaccine"] == 1


def test_verification_fails_loudly_if_a_resistance_route_loses_vaccine_coverage():
    """A regression guard on the guard: a mask that drops a drug-resistance clone must be reported as
    inconsistent, not quietly accepted."""
    broken = np.ones(len(VACCINE_CLONE_NAMES))
    broken[-1] = 0.0
    broken[VACCINE_CLONE_NAMES.index("rtk_bypass")] = 0.0    # wrongly exclude a covered route
    report = verify_antigen_convergence(
        VACCINE_CLONE_NAMES, ramping_kill_schedule(730, 90, 21.0, 0.05, broken))
    assert report["consistent"] is False
    assert "rtk_bypass" in report["mismatches"]
    assert "MASK DOES NOT MATCH" in report["interpretation"]


def test_verification_rejects_a_misshaped_schedule():
    with pytest.raises(ValueError):
        verify_antigen_convergence(VACCINE_CLONE_NAMES, np.zeros((730, 2)))
    with pytest.raises(ValueError):
        verify_antigen_convergence(VACCINE_CLONE_NAMES, np.zeros(730))


def test_vaccine_ramp_begins_before_the_cytotoxic_duration_cap_forces_a_stop():
    """The finding that undoes 'the duration cap is the binding constraint': the vaccine starts
    ramping inside lomustine's real 105-day window, so there is no unopposed interval."""
    from canine_dsp.mapk_scenarios import CCNU_EXPOSURE_DAYS, VACCINE_RAMP_DAYS, VACCINE_START_DAY

    handoff = handoff_timing(CCNU_EXPOSURE_DAYS, VACCINE_START_DAY, VACCINE_RAMP_DAYS)
    assert handoff["continuous_pressure"] is True
    assert handoff["overlap_days"] == pytest.approx(15.0)
    # Coverage is continuous but NOT instantaneously full: the vaccine is about half-strength when
    # lomustine stops, and its ramp keeps climbing for ~6 more days. Asserting the precise shape here
    # rather than "no gap" -- an earlier version of this test asserted zero and was simply wrong.
    assert handoff["vaccine_fraction_of_max_at_cytotoxic_stop"] == pytest.approx(0.51, abs=0.02)
    assert handoff["uncovered_gap_days"] == pytest.approx(6.0)
    assert "only binding in the absence" in handoff["interpretation"]


def test_handoff_reports_an_uncovered_gap_when_the_vaccine_starts_too_late():
    late = handoff_timing(cytotoxic_exposure_days=105, vaccine_start_day=200,
                          vaccine_ramp_days=21.0)
    assert late["continuous_pressure"] is False
    assert late["uncovered_gap_days"] > 0
    assert "neither mechanism at strength" in late["interpretation"]
    for bad in ((0, 90, 21.0), (105, -1, 21.0), (105, 90, 0.0)):
        with pytest.raises(ValueError):
            handoff_timing(*bad)


def test_only_the_vaccine_escapes_both_hard_constraints():
    """The compact reason the endurance case rests on the vaccine: the two constraints that defeated
    each small-molecule second agent do not apply to an immune mechanism, and it still covers every
    drug-resistance route."""
    matrix = mechanism_constraint_matrix()
    assert matrix["cdk46_inhibitor"]["cytostatic_ceiling_applies"] is True
    assert matrix["lomustine"]["cumulative_dose_duration_cap"] is True
    vaccine = matrix["hotspot_vaccine"]
    assert vaccine["cytostatic_ceiling_applies"] is False
    assert vaccine["cumulative_dose_duration_cap"] is False
    assert vaccine["covers_all_drug_resistance_routes"] is True
    unconstrained = [name for name, m in matrix.items()
                     if not m["cytostatic_ceiling_applies"]
                     and not m["cumulative_dose_duration_cap"]]
    assert unconstrained == ["hotspot_vaccine"]


def test_convergence_argument_is_distinguished_from_the_pharmacological_one():
    """Two different convergence claims were made in this project and conflating them loses the
    point: a shared downstream dependency needs a potency threshold, a shared antigen does not."""
    assert "distinct_from" in CONVERGENCE_ARGUMENT
    assert "CDK4/6" in CONVERGENCE_ARGUMENT["distinct_from"]
    assert "PTPN11" in CONVERGENCE_ARGUMENT["load_bearing_unverified_premise"]


def test_vaccine_rescues_the_preexisting_subclone_arm_the_drug_only_regimen_cannot():
    """The substantive correction, end to end in the real engine: three prior analyses reported the
    with-pre-existing-subclone arm as flat 0% durable while running the vaccine at zero. Because a
    pre-existing drug-resistant subclone still carries the driver antigen, that arm is precisely what
    antigen convergence predicts a vaccine covers."""
    from dataclasses import replace

    from canine_dsp.mapk_resistance import run_monte_carlo_with_vaccine
    from canine_dsp.mapk_scenarios import (
        CCNU_EXPOSURE_DAYS,
        CCNU_MATCHED_CSS_NM,
        CCNU_MATCHED_IC50_NM,
        IMMUNE_ESCAPE_SEEDING_RATE,
        VACCINE_RAMP_DAYS,
        VACCINE_START_DAY,
        vaccine_followon_scenarios,
    )
    from canine_dsp.single_patient import partition_by_preexisting_subclone

    model, css, rates, burden, _ = vaccine_followon_scenarios(
        cdk46_max_kill=0.08, vaccine_max_kill_values=[0.0])[0.0]
    model = replace(model, ic50_nM_2=CCNU_MATCHED_IC50_NM, max_kill_2=0.08)

    def subclone_arm(vaccine_max_kill):
        outcome = run_monte_carlo_with_vaccine(
            model, css, 730, rates, VACCINE_START_DAY, VACCINE_RAMP_DAYS, vaccine_max_kill,
            IMMUNE_ESCAPE_SEEDING_RATE, VACCINE_CLONE_NAMES, trials=200, preexisting_prob=0.30,
            initial_burden=burden, css_reference_2=CCNU_MATCHED_CSS_NM,
            css_reference_2_duration_days=CCNU_EXPOSURE_DAYS, seed=7)
        return partition_by_preexisting_subclone(
            outcome)["with_preexisting_subclone"]["durable_response_fraction"]

    assert subclone_arm(0.0) == pytest.approx(0.0, abs=0.02)   # what the prior analyses reported
    assert subclone_arm(0.05) > 0.9                            # what the vaccine actually does


def test_long_horizon_erosion_is_a_growth_rate_threshold_not_antigen_loss():
    """Checked because an earlier draft asserted the opposite. The 10-year leak at vaccine potency
    0.05 is target_site_mutation (growth 0.058) outrunning the vaccine, not the immune-escape clone --
    so it disappears once potency clears that growth rate, which antigen loss would not do."""
    from dataclasses import replace

    import pandas as pd

    from canine_dsp.mapk_resistance import run_monte_carlo_with_vaccine
    from canine_dsp.mapk_scenarios import (
        CCNU_EXPOSURE_DAYS,
        CCNU_MATCHED_CSS_NM,
        CCNU_MATCHED_IC50_NM,
        IMMUNE_ESCAPE_SEEDING_RATE,
        VACCINE_RAMP_DAYS,
        VACCINE_START_DAY,
        vaccine_followon_scenarios,
    )

    model, css, rates, burden, _ = vaccine_followon_scenarios(
        cdk46_max_kill=0.08, vaccine_max_kill_values=[0.0])[0.0]
    model = replace(model, ic50_nM_2=CCNU_MATCHED_IC50_NM, max_kill_2=0.08)
    fastest_resistant_growth = float(np.max(np.asarray(model.growth)[1:4]))

    def ten_year(vaccine_max_kill):
        outcome = run_monte_carlo_with_vaccine(
            model, css, 3650, rates, VACCINE_START_DAY, VACCINE_RAMP_DAYS, vaccine_max_kill,
            IMMUNE_ESCAPE_SEEDING_RATE, VACCINE_CLONE_NAMES, trials=200, preexisting_prob=0.30,
            initial_burden=burden, css_reference_2=CCNU_MATCHED_CSS_NM,
            css_reference_2_duration_days=CCNU_EXPOSURE_DAYS, seed=7)
        counts = pd.Series(outcome.dominant_mechanism).value_counts()
        return float(1 - outcome.progressed.mean()), counts

    below, counts_below = ten_year(0.05)          # below the fastest resistant clone's growth rate
    above, _ = ten_year(fastest_resistant_growth + 0.005)
    assert 0.05 < fastest_resistant_growth        # the premise of the explanation
    assert below < 1.0                            # a real leak exists below threshold
    assert counts_below.get("immune_escape", 0) == 0   # and it is NOT antigen loss
    assert counts_below.get("target_site_mutation", 0) > 0
    assert above > below                          # crossing the growth rate closes it


def test_vaccine_potency_threshold_is_the_fastest_covered_clones_growth_rate():
    """The threshold is set by the fastest clone the vaccine can see -- not by the sensitive clone
    (which the drugs already handle) and not by the immune-escape clone (which the vaccine cannot see
    at all, so no potency covers it)."""
    from canine_dsp.antigen_convergence import vaccine_potency_threshold

    growth = np.array([0.06, 0.05, 0.055, 0.058, 0.0425])
    report = vaccine_potency_threshold(growth, VACCINE_CLONE_NAMES)
    assert report["fastest_covered_clone"] == "target_site_mutation"
    assert report["fastest_covered_growth_rate"] == pytest.approx(0.058)
    assert report["threshold_vaccine_max_kill"] > 0.058
    # the sensitive clone's 0.06 is higher but must not set the threshold, and immune_escape is out
    assert "sensitive" not in report["covered_drug_resistance_clones"]
    assert "immune_escape" not in report["covered_drug_resistance_clones"]
    with pytest.raises(ValueError):
        vaccine_potency_threshold(growth, VACCINE_CLONE_NAMES[:3])
    with pytest.raises(ValueError):
        vaccine_potency_threshold(growth, VACCINE_CLONE_NAMES, margin=-0.01)


def test_crossing_the_threshold_makes_the_outcome_insensitive_to_preexisting_prob():
    """The substantive endurance result, and the reason it matters more than any recalibration: below
    threshold the 10-year outcome swings hugely with preexisting_prob (the parameter no assay can
    measure); at/above threshold that dependence disappears rather than shrinking."""
    from dataclasses import replace

    from canine_dsp.antigen_convergence import vaccine_potency_threshold
    from canine_dsp.mapk_resistance import run_monte_carlo_with_vaccine
    from canine_dsp.mapk_scenarios import (
        CCNU_EXPOSURE_DAYS,
        CCNU_MATCHED_CSS_NM,
        CCNU_MATCHED_IC50_NM,
        IMMUNE_ESCAPE_SEEDING_RATE,
        VACCINE_RAMP_DAYS,
        VACCINE_START_DAY,
        vaccine_followon_scenarios,
    )

    model, css, rates, burden, _ = vaccine_followon_scenarios(
        cdk46_max_kill=0.08, vaccine_max_kill_values=[0.0])[0.0]
    model = replace(model, ic50_nM_2=CCNU_MATCHED_IC50_NM, max_kill_2=0.08)
    threshold = vaccine_potency_threshold(
        np.asarray(model.growth), VACCINE_CLONE_NAMES)["threshold_vaccine_max_kill"]

    def durable(vaccine_max_kill, preexisting_prob):
        outcome = run_monte_carlo_with_vaccine(
            model, css, 1825, rates, VACCINE_START_DAY, VACCINE_RAMP_DAYS, vaccine_max_kill,
            IMMUNE_ESCAPE_SEEDING_RATE, VACCINE_CLONE_NAMES, trials=150,
            preexisting_prob=preexisting_prob, initial_burden=burden,
            css_reference_2=CCNU_MATCHED_CSS_NM,
            css_reference_2_duration_days=CCNU_EXPOSURE_DAYS, seed=7)
        return float(1 - outcome.progressed.mean())

    below_spread = abs(durable(0.03, 0.30) - durable(0.03, 0.62))
    above_spread = abs(durable(threshold, 0.30) - durable(threshold, 0.62))
    assert below_spread > 0.15      # sub-threshold: dominated by the unmeasurable parameter
    assert above_spread < 0.05      # above threshold: dependence essentially gone
    assert above_spread < below_spread
