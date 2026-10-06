import numpy as np
import pytest

from canine_dsp.mutational_supply import (
    CANINE_HS_EXOME,
    CANINE_TMB_BY_TUMOR_TYPE,
    MUTATIONAL_SUPPLY_HYPOTHESIS,
    TMB_RATIO_SWEEP,
    mutational_supply_report,
    refuse_bmd_benchmark_transfer,
    scale_preexisting_prob,
    scale_seeding_rate,
)


def test_preexisting_prob_scales_by_poisson_survival_not_linearly():
    """The correct form is p' = 1 - (1-p)**r, because preexisting_prob is a saturating probability
    ("at least one clone exists"), not a rate. Scaling it linearly would understate the benefit of
    low burden at small p and overstate it near p=1, where the reference tumor is already saturated
    and reducing mutational supply cannot help much."""
    result = scale_preexisting_prob(0.30, 0.25)
    assert result["preexisting_prob_scaled"] == pytest.approx(1 - 0.7 ** 0.25)
    assert result["preexisting_prob_scaled"] == pytest.approx(0.0853, abs=1e-4)
    # strictly better than the naive linear scaling would suggest at this p
    assert result["preexisting_prob_scaled"] > 0.30 * 0.25
    # ratio 1.0 must be an exact identity, so the status-quo sweep row is a true baseline
    assert scale_preexisting_prob(0.30, 1.0)["preexisting_prob_scaled"] == pytest.approx(0.30)


def test_preexisting_prob_scaling_saturates_for_an_already_certain_tumor():
    """A tumor that essentially always harbours resistance cannot be rescued much by lower supply --
    the honest shape of the argument, and the reason linear scaling would have been misleading."""
    near_certain = scale_preexisting_prob(0.99, 0.25)["preexisting_prob_scaled"]
    assert near_certain > 0.6          # still high; a 4x supply cut does not make it safe
    low = scale_preexisting_prob(0.05, 0.25)["preexisting_prob_scaled"]
    assert low < 0.05 * 0.5            # but at low p the same cut is nearly proportional
    for bad in ((1.5, 0.5), (0.3, 0.0), (0.3, -1.0)):
        with pytest.raises(ValueError):
            scale_preexisting_prob(*bad)


def test_seeding_rate_scales_linearly_and_preserves_mechanism_weighting():
    """A seeding rate IS a rate, so it scales linearly -- and the relative weights between escape
    mechanisms must be preserved, because this argument is about total mutational supply, not about
    which route is favoured."""
    rates = np.array([0.0102, 0.0012, 0.0006])
    scaled = scale_seeding_rate(rates, 0.25)
    np.testing.assert_allclose(scaled, rates * 0.25)
    np.testing.assert_allclose(scaled / scaled.sum(), rates / rates.sum())
    assert scale_seeding_rate(0.012, 0.5) == pytest.approx(0.006)
    with pytest.raises(ValueError):
        scale_seeding_rate(rates, 0.0)
    with pytest.raises(ValueError):
        scale_seeding_rate(np.array([-1.0]), 0.5)


def test_hypothesis_explicitly_disclaims_the_mechanism_count_argument():
    """The distinction this module exists to hold: it is a rate argument, not a count argument.
    Conflating them was a real error made in this project's own discussion, so the disclaimer is
    load-bearing rather than decorative."""
    assert "does_not_claim" in MUTATIONAL_SUPPLY_HYPOTHESIS
    assert "FEWER" in MUTATIONAL_SUPPLY_HYPOTHESIS["does_not_claim"]
    assert MUTATIONAL_SUPPLY_HYPOTHESIS["acts_on_exactly"] == [
        "seeding_rates (poisson_mutation_injections)",
        "preexisting_prob (sample_initial_state)"]
    assert "unverified" in MUTATIONAL_SUPPLY_HYPOTHESIS["status"]


def test_canine_tmb_data_records_that_histiocytic_sarcoma_was_not_measured():
    """The whole argument turns on HS's burden, and the real pan-canine cohort does not contain it.
    That absence must be a structured field, not a sentence someone can skim past, because every
    optimistic row of the sweep depends on it."""
    assert CANINE_TMB_BY_TUMOR_TYPE["histiocytic_sarcoma_included"] is False
    assert "hemangiosarcoma" in CANINE_TMB_BY_TUMOR_TYPE["high_burden_types"]
    assert "oral_melanoma" in CANINE_TMB_BY_TUMOR_TYPE["high_burden_types"]
    assert CANINE_HS_EXOME["tumor_mutational_burden_reported"] is None
    assert CANINE_HS_EXOME["n_dogs_whole_exome_sequenced"] == 5


def test_measured_burden_supports_the_melanoma_rejection_this_repo_already_made():
    """mapk_scenarios rejects the human melanoma trial as a recentering basis partly on burden
    grounds, previously reasoning from human UV biology. Canine oral melanoma being measured
    high-burden means that rejection now has dog-specific support."""
    assert CANINE_TMB_BY_TUMOR_TYPE["high_burden_types"]["oral_melanoma"].startswith("median >=")
    assert "empirically backs" in CANINE_TMB_BY_TUMOR_TYPE["why_this_matters_here"]


def test_sweep_spans_the_status_quo_so_the_baseline_is_visible():
    """TMB_RATIO_SWEEP must include 1.0 -- what both scenario modules currently encode by sharing
    _SEEDING_RATE_TOTAL between HS and a measured-high-burden disease. Without it the sweep would
    only show the optimistic side of an unmeasured parameter."""
    assert 1.0 in TMB_RATIO_SWEEP
    assert min(TMB_RATIO_SWEEP) < 0.5
    report = mutational_supply_report(0.30, 0.012)
    status_quo = [r for r in report["sweep"] if r["is_status_quo"]]
    assert len(status_quo) == 1
    assert status_quo[0]["preexisting_prob"] == pytest.approx(0.30)
    assert status_quo[0]["seeding_rate_total"] == pytest.approx(0.012)
    # durable response must improve monotonically as burden falls
    durable = [r["approximate_durable_response"] for r in report["sweep"]]
    ratios = [r["tmb_ratio"] for r in report["sweep"]]
    assert [d for _, d in sorted(zip(ratios, durable))] == sorted(durable, reverse=True)


def test_benchmark_transfer_guard_names_both_directions_of_the_same_error():
    """The Skorupski inversion (p ~= 0.62) is BMD-context. Carrying it onto an
    unsequenced-breed or low-burden arm would be the same breed/stratification mismatch driver_conditioned_arms refuses -- running
    pessimistically, which is exactly why it was easy to miss."""
    guard = refuse_bmd_benchmark_transfer()
    assert guard["implied_bmd_preexisting_prob"] == pytest.approx(0.62)
    assert any("localized pulmonary" in item for item in guard["must_not_transfer_to"])
    assert any("low-mutational-supply" in item for item in guard["must_not_transfer_to"])
    assert "pessimistic" in guard["symmetry_note"]


def test_the_benefit_flows_through_preexisting_resistance_not_the_acquired_rate():
    """The substantive finding, checked end to end in the real engine rather than argued: at a
    fourfold lower burden, scaling the acquired seeding rate alone barely moves durable response,
    while scaling preexisting_prob alone captures nearly all of it. If this ever inverts, the demo's
    headline conclusion is wrong."""
    from canine_dsp.mapk_resistance import run_monte_carlo
    from canine_dsp.mapk_scenarios import (CCNU_EXPOSURE_DAYS, CCNU_MATCHED_CSS_NM,
                                           ccnu_combination_scenarios)

    potency = 0.08
    model, css, rates, burden, _ = ccnu_combination_scenarios(
        max_kill_2_values=[potency])[potency]

    def durable(prob, seeding):
        outcome = run_monte_carlo(model, css, 730, seeding, trials=200, preexisting_prob=prob,
                                  initial_burden=burden, css_reference_2=CCNU_MATCHED_CSS_NM,
                                  css_reference_2_duration_days=CCNU_EXPOSURE_DAYS, seed=7)
        return float(1 - outcome.progressed.mean())

    ratio = 0.25
    scaled_prob = scale_preexisting_prob(0.30, ratio)["preexisting_prob_scaled"]
    scaled_rates = scale_seeding_rate(rates, ratio)
    baseline = durable(0.30, rates)
    seeding_only = durable(0.30, scaled_rates) - baseline
    prob_only = durable(scaled_prob, rates) - baseline
    assert abs(seeding_only) < 0.05        # acquired-rate half contributes almost nothing
    assert prob_only > 0.15                # pre-existing half carries the argument
    assert prob_only > 4 * abs(seeding_only)


def test_analytic_shortcut_tracks_the_monte_carlo_in_this_saturated_regime():
    """`scale_preexisting_prob` advertises durable response ~= 1 - p. That is only legitimate because
    the two N=1 arms are saturated; it is asserted here against the engine so the shortcut cannot
    quietly be relied on if the regime changes."""
    from canine_dsp.mapk_resistance import run_monte_carlo
    from canine_dsp.mapk_scenarios import (CCNU_EXPOSURE_DAYS, CCNU_MATCHED_CSS_NM,
                                           ccnu_combination_scenarios)

    model, css, rates, burden, _ = ccnu_combination_scenarios(max_kill_2_values=[0.08])[0.08]
    for ratio in (1.0, 0.25):
        scaled = scale_preexisting_prob(0.30, ratio)
        outcome = run_monte_carlo(
            model, css, 730, scale_seeding_rate(rates, ratio), trials=300,
            preexisting_prob=scaled["preexisting_prob_scaled"], initial_burden=burden,
            css_reference_2=CCNU_MATCHED_CSS_NM,
            css_reference_2_duration_days=CCNU_EXPOSURE_DAYS, seed=7)
        simulated = float(1 - outcome.progressed.mean())
        assert abs(simulated - scaled[
            "approximate_durable_response_if_arms_are_saturated"]) < 0.03
