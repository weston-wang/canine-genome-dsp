import json

import numpy as np
import pandas as pd
import pytest

from canine_dsp.mapk_cli import (
    BRAIN_PENETRATION_FRACTION,
    CDK46_MAX_KILL_SWEEP,
    COMBINED_EXPOSURE_DERATING,
    DURABILITY_HORIZON_SWEEP,
    IMMUNE_ESCAPE_GROWTH_PENALTY,
    VACCINE_CLONE_NAMES,
    VACCINE_MAX_KILL_SWEEP,
    VACCINE_START_DAY,
    canine_cns_hs_scenarios,
    combination_control_demo,
    combination_scenarios,
    combination_toxicity_demo,
    durability_horizon_demo,
    localized_control_demo,
    localized_pihs_scenarios,
    mapk_cns_demo,
    single_patient_feasibility_demo,
    vaccine_followon_demo,
    vaccine_followon_scenarios,
)
from canine_dsp.mapk_resistance import clone_growth_margins, run_monte_carlo, run_monte_carlo_with_vaccine


def test_cns_scenarios_scale_css_by_brain_penetration_fraction():
    scenarios = canine_cns_hs_scenarios(breed="bmd")
    _, systemic_css, _, _ = scenarios["systemic_reference"]
    for drug, fraction in BRAIN_PENETRATION_FRACTION.items():
        _, css, _, provenance = scenarios[drug]
        assert css == systemic_css * fraction
        assert provenance["brain_penetration_reference_drug"] == drug


def test_cns_scenarios_location_multiplier_scales_all_drugs():
    baseline = canine_cns_hs_scenarios(breed="bmd", location_penetration_multiplier=1.0)
    halved = canine_cns_hs_scenarios(breed="bmd", location_penetration_multiplier=0.5)
    for drug in BRAIN_PENETRATION_FRACTION:
        _, css_base, _, _ = baseline[drug]
        _, css_half, _, _ = halved[drug]
        assert css_half == css_base * 0.5


def test_flat_coated_retriever_shifts_weight_toward_rtk_bypass():
    _, _, rates_bmd, _ = canine_cns_hs_scenarios(breed="bmd")["systemic_reference"]
    _, _, rates_fcr, provenance = canine_cns_hs_scenarios(breed="flat_coated_retriever")["systemic_reference"]
    assert np.argmax(rates_bmd) == 0  # pathway_reactivation dominates for bmd
    assert np.argmax(rates_fcr) == 1  # rtk_bypass dominates for flat_coated_retriever
    assert provenance["breed_germline_locus"] is not None


def test_mapk_cns_demo_writes_expected_outputs(tmp_path):
    mapk_cns_demo(tmp_path, breed="bmd", trials=20, horizon_days=90, seed=1)
    summary = json.loads((tmp_path / "summary.json").read_text())
    assert len(summary["scenarios"]) == len(BRAIN_PENETRATION_FRACTION)
    assert (tmp_path / "cns_penetration_sensitivity.csv").exists()
    assert (tmp_path / "cns_penetration.png").exists()
    assert "unverified_extrapolations" in summary


def test_localized_pihs_scenarios_debulking_shrinks_initial_burden_only():
    arms = localized_pihs_scenarios(breed="bmd", debulking_fraction=0.9)
    _, css_intact, _, burden_intact, _ = arms["intact_trametinib"]
    _, css_debulked, _, burden_debulked, _ = arms["debulked_trametinib"]
    assert burden_debulked == pytest.approx(burden_intact * 0.1)
    assert css_intact == css_debulked  # debulking must not change drug exposure
    _, css_untreated, _, _, _ = arms["intact_untreated"]
    assert css_untreated == 0.0


def test_localized_control_demo_writes_four_arms_with_mechanism_columns(tmp_path):
    localized_control_demo(tmp_path, breed="bmd", trials=20, horizon_days=90, seed=1)
    table = pd.read_csv(tmp_path / "localized_control_arms.csv")
    assert set(table["arm"]) == {"intact_untreated", "intact_trametinib",
                                 "debulked_untreated", "debulked_trametinib"}
    assert "mechanism_pathway_reactivation" in table.columns
    summary = json.loads((tmp_path / "summary.json").read_text())
    assert "reasoning_chain" in summary and "unverified_extrapolations" in summary
    assert (tmp_path / "localized_control.png").exists()


def test_debulking_delays_but_does_not_eliminate_relapse_risk():
    """The model's key qualitative claim: debulking shrinks a pre-existing resistant subclone
    proportionally (delaying when it's detected) but does not change *whether* one exists, so
    it should meaningfully extend median time-to-progression without much changing the
    probability of eventually progressing."""
    arms = localized_pihs_scenarios(breed="bmd")
    outcomes = {}
    for name in ("intact_trametinib", "debulked_trametinib"):
        model, css, seeding_rates, initial_burden, _ = arms[name]
        outcomes[name] = run_monte_carlo(model, css, 730, seeding_rates, trials=150,
                                         preexisting_prob=.3, initial_burden=initial_burden, seed=3)
    intact_ttp = outcomes["intact_trametinib"].time_to_progression
    debulked_ttp = outcomes["debulked_trametinib"].time_to_progression
    intact_median = np.nanmedian(intact_ttp)
    debulked_median = np.nanmedian(debulked_ttp)
    assert debulked_median > intact_median
    intact_durable = 1 - outcomes["intact_trametinib"].progressed.mean()
    debulked_durable = 1 - outcomes["debulked_trametinib"].progressed.mean()
    assert abs(debulked_durable - intact_durable) < 0.15


def test_combination_scenarios_zero_kill_matches_trametinib_only():
    scenarios = combination_scenarios(breed="bmd", max_kill_2_values=[0.0, 0.05])
    zero_model, css, seeding_rates, initial_burden, _ = scenarios[0.0]
    outcome_zero = run_monte_carlo(zero_model, css, 200, seeding_rates, trials=40,
                                   initial_burden=initial_burden, css_reference_2=None, seed=5)
    trametinib_only = localized_pihs_scenarios(breed="bmd")["debulked_trametinib"]
    model2, css2, seeding_rates2, initial_burden2, _ = trametinib_only
    outcome_only = run_monte_carlo(model2, css2, 200, seeding_rates2, trials=40,
                                   initial_burden=initial_burden2, seed=5)
    np.testing.assert_allclose(outcome_zero.trajectories, outcome_only.trajectories)


def test_higher_cdk46_potency_does_not_reduce_durable_response():
    """More kill from a mechanism-agnostic second drug should never make outcomes worse."""
    scenarios = combination_scenarios(breed="bmd", max_kill_2_values=[0.0, 0.12])
    durability = {}
    for max_kill_2, (model, css, seeding_rates, initial_burden, _) in scenarios.items():
        css_2 = 500.0 if max_kill_2 > 0 else None
        outcome = run_monte_carlo(model, css, 400, seeding_rates, trials=80,
                                  initial_burden=initial_burden, css_reference_2=css_2, seed=9)
        durability[max_kill_2] = 1 - outcome.progressed.mean()
    assert durability[0.12] >= durability[0.0]


def test_combination_control_demo_writes_full_sweep(tmp_path):
    combination_control_demo(tmp_path, breed="bmd", trials=20, horizon_days=90, seed=1)
    table = pd.read_csv(tmp_path / "combination_sensitivity.csv")
    assert set(table["regimen"]) == {"combination", "cdk46_monotherapy"}
    assert len(table) == 2 * len(CDK46_MAX_KILL_SWEEP)
    assert "mechanism_pathway_reactivation" in table.columns
    summary = json.loads((tmp_path / "summary.json").read_text())
    assert "mechanism_agnostic_rationale" in summary
    assert "division_of_labor" in summary
    assert (tmp_path / "combination_sensitivity.png").exists()


def test_monotherapy_needs_higher_potency_than_combination():
    """The core claim from this turn's analysis: at a potency where combination already
    achieves near-complete suppression, CDK4/6i monotherapy (no trametinib) should still be
    failing, because it has no help suppressing the bulk (sensitive-clone) tumor."""
    combo = combination_scenarios(breed="bmd", max_kill_2_values=[0.05], trametinib_active=True)
    mono = combination_scenarios(breed="bmd", max_kill_2_values=[0.05], trametinib_active=False)
    model_c, css_c, rates_c, burden_c, _ = combo[0.05]
    model_m, css_m, rates_m, burden_m, _ = mono[0.05]
    assert css_m == 0.0 and css_c > 0.0
    outcome_c = run_monte_carlo(model_c, css_c, 730, rates_c, trials=150, initial_burden=burden_c,
                                css_reference_2=500., seed=4)
    outcome_m = run_monte_carlo(model_m, css_m, 730, rates_m, trials=150, initial_burden=burden_m,
                                css_reference_2=500., seed=4)
    durable_c = 1 - outcome_c.progressed.mean()
    durable_m = 1 - outcome_m.progressed.mean()
    assert durable_c > 0.9
    assert durable_m < durable_c


def test_combination_toxicity_demo_derating_scales_both_drug_exposures(tmp_path):
    combination_toxicity_demo(tmp_path, breed="bmd", max_kill_2=0.05, trials=20,
                              horizon_days=90, seed=1)
    table = pd.read_csv(tmp_path / "toxicity_derating_sensitivity.csv")
    assert len(table) == len(COMBINED_EXPOSURE_DERATING)
    full_dose = table[table["combined_exposure_derating"] == 1.0].iloc[0]
    half_ish = table[table["combined_exposure_derating"] == 0.4].iloc[0]
    assert half_ish["trametinib_css_nM"] == pytest.approx(full_dose["trametinib_css_nM"] * 0.4)
    assert half_ish["cdk46_css_nM"] == pytest.approx(full_dose["cdk46_css_nM"] * 0.4)
    summary = json.loads((tmp_path / "summary.json").read_text())
    assert "toxicity_extrapolation_rationale" in summary
    assert (tmp_path / "toxicity_derating.png").exists()


def test_toxicity_derating_can_erode_the_combination_benefit():
    """The whole point of the de-rating sweep: durable response at full illustrative dose
    should not be worse than at a meaningfully reduced dose (monotonic in the derating, or at
    least not inverted), so the sweep can actually show whether dose reduction costs efficacy."""
    scenarios = combination_scenarios(breed="bmd", max_kill_2_values=[0.05])
    model, css, seeding_rates, initial_burden, _ = scenarios[0.05]
    durability = {}
    for derating in (1.0, 0.4):
        outcome = run_monte_carlo(model, css * derating, 730, seeding_rates, trials=150,
                                  initial_burden=initial_burden,
                                  css_reference_2=500. * derating, seed=6)
        durability[derating] = 1 - outcome.progressed.mean()
    assert durability[1.0] >= durability[0.4]


def test_durability_horizon_demo_writes_full_sweep(tmp_path):
    durability_horizon_demo(tmp_path, breed="bmd", max_kill_2=0.05, trials=20, seed=1)
    table = pd.read_csv(tmp_path / "durability_horizon_sensitivity.csv")
    assert len(table) == len(DURABILITY_HORIZON_SWEEP)
    assert list(table["horizon_days"]) == DURABILITY_HORIZON_SWEEP
    summary = json.loads((tmp_path / "summary.json").read_text())
    assert "note" in summary
    assert (tmp_path / "durability_horizon.png").exists()


def test_durable_response_probability_is_not_flat_across_horizons():
    """The core claim behind adding this demo: at a potency that looks like a cure at 2 years,
    "durable" is not permanent -- durability should decline (not stay flat or rise) as the
    simulated follow-up window is extended toward a decade, because the combination slows the
    pathway_reactivation escape route rather than eliminating it."""
    scenarios = combination_scenarios(breed="bmd", max_kill_2_values=[0.05])
    model, css, seeding_rates, initial_burden, _ = scenarios[0.05]
    durability = {}
    for horizon_days in (730, 3650):
        outcome = run_monte_carlo(model, css, horizon_days, seeding_rates, trials=300,
                                  initial_burden=initial_burden, css_reference_2=500., seed=7)
        durability[horizon_days] = 1 - outcome.progressed.mean()
    assert durability[730] > durability[3650]


def test_higher_cdk46_potency_reverses_every_resistant_clones_growth_margin():
    """The purely pharmacological path forward that doesn't depend on antigen presentation at
    all: at the illustrative central parameters, max_kill_2=0.05 (used throughout most of this
    module) leaves pathway_reactivation and target_site_mutation with a small POSITIVE margin
    (they are slowed, not reversed); max_kill_2=0.08 should reverse every resistant clone's
    margin to negative -- a genuine mechanistic elimination, not just a low detection
    probability within a given follow-up window."""
    scenarios_partial = combination_scenarios(breed="bmd", max_kill_2_values=[0.05])
    scenarios_full = combination_scenarios(breed="bmd", max_kill_2_values=[0.08])
    model_partial, css, _, _, _ = scenarios_partial[0.05]
    model_full, _, _, _, _ = scenarios_full[0.08]
    margins_partial = clone_growth_margins(model_partial, css, 500.0)
    margins_full = clone_growth_margins(model_full, css, 500.0)
    assert (margins_partial[1:] > 0).any()  # at least one resistant clone still net-positive
    assert (margins_full[1:] < 0).all()     # every resistant clone reversed


def test_higher_cdk46_potency_survives_combined_dose_derating():
    """The reversal at max_kill_2=0.08 should not be a knife's-edge result: it should hold
    across this module's own combined-dose de-rating range, not just at full illustrative dose,
    since that's the realistic concern raised by TOXICITY_EXTRAPOLATION_NOTE."""
    from canine_dsp.mapk_cli import COMBINED_EXPOSURE_DERATING as DERATING

    scenarios = combination_scenarios(breed="bmd", max_kill_2_values=[0.08])
    model, css, _, _, _ = scenarios[0.08]
    for derating in DERATING:
        margins = clone_growth_margins(model, css * derating, 500.0 * derating)
        assert (margins[1:] < 0).all(), f"derating={derating} should still reverse every clone"


def test_higher_cdk46_potency_eliminates_long_horizon_erosion():
    """The direct Monte Carlo confirmation of the margin finding above: durability should not
    erode from 2 to 10 years at max_kill_2=0.08 the way it does at 0.05 (see
    test_durable_response_probability_is_not_flat_across_horizons), because none of the
    resistant clones has a positive margin left to slowly regrow into detectability."""
    scenarios = combination_scenarios(breed="bmd", max_kill_2_values=[0.08])
    model, css, seeding_rates, initial_burden, _ = scenarios[0.08]
    durability = {}
    for horizon_days in (730, 3650):
        outcome = run_monte_carlo(model, css, horizon_days, seeding_rates, trials=300,
                                  initial_burden=initial_burden, css_reference_2=500., seed=7)
        durability[horizon_days] = 1 - outcome.progressed.mean()
    assert durability[3650] >= durability[730] - 0.02  # no meaningful erosion, unlike at 0.05
    assert durability[3650] > 0.95


def test_vaccine_followon_scenarios_adds_fifth_clone_inheriting_pathway_reactivation():
    scenarios = vaccine_followon_scenarios(breed="bmd", vaccine_max_kill_values=[0.0, 0.05])
    model, css, seeding_rates, initial_burden, provenance = scenarios[0.05]
    assert len(model.growth) == 5
    assert model.ic50_nM[4] == model.ic50_nM[1]
    assert model.max_kill[4] == model.max_kill[1]
    assert model.growth[4] == pytest.approx(model.growth[1] * IMMUNE_ESCAPE_GROWTH_PENALTY)
    assert provenance["vaccine_max_kill"] == 0.05
    assert css > 0.0  # trametinib still active underneath


def test_vaccine_followon_scenarios_zero_max_kill_behaves_like_combination_only():
    """vaccine_max_kill=0 should carry the 5th clone but never apply vaccine kill or seed it
    before VACCINE_START_DAY -- behaviorally identical to the drug-only combination model."""
    scenarios = vaccine_followon_scenarios(breed="bmd", vaccine_max_kill_values=[0.0])
    model, css, seeding_rates, initial_burden, _ = scenarios[0.0]
    clone_names = VACCINE_CLONE_NAMES
    outcome = run_monte_carlo_with_vaccine(
        model, css, 200, seeding_rates, vaccine_start_day=VACCINE_START_DAY, vaccine_ramp_days=21,
        vaccine_max_kill=0.0, immune_escape_seeding_rate=0.0, clone_names=clone_names,
        trials=30, css_reference_2=500., seed=5)
    assert np.all(outcome.trajectories[:, :, 4] == 0)  # never seeded when the rate itself is 0


def test_vaccine_followon_demo_writes_expected_outputs(tmp_path):
    vaccine_followon_demo(tmp_path, breed="bmd", trials=15, horizon_days=200, seed=1)
    table = pd.read_csv(tmp_path / "vaccine_followon_sensitivity.csv")
    assert len(table) == len(VACCINE_MAX_KILL_SWEEP)
    assert "mechanism_immune_escape" in table.columns
    assert "mechanism_pathway_reactivation" in table.columns
    summary = json.loads((tmp_path / "summary.json").read_text())
    assert "vaccine_precedent" in summary
    assert "antigen_persistence_rationale" in summary
    assert "dendritic_cell_vaccine_caveat" in summary
    assert "unverified_extrapolations" in summary
    assert (tmp_path / "vaccine_followon.png").exists()


def test_vaccine_suppresses_pathway_reactivation_without_worsening_durability():
    """Core claim: since pathway_reactivation still expresses the original driver antigen, adding
    a potent-enough vaccine on top of the combination should not make long-horizon durability
    worse than the drug-only baseline, even though it introduces a new immune_escape route."""
    scenarios = vaccine_followon_scenarios(breed="bmd", vaccine_max_kill_values=[0.0, 0.05])
    durability = {}
    for vaccine_max_kill, (model, css, seeding_rates, initial_burden, _) in scenarios.items():
        outcome = run_monte_carlo_with_vaccine(
            model, css, 1825, seeding_rates, vaccine_start_day=VACCINE_START_DAY,
            vaccine_ramp_days=21, vaccine_max_kill=vaccine_max_kill,
            immune_escape_seeding_rate=6e-5, clone_names=VACCINE_CLONE_NAMES, trials=150,
            initial_burden=initial_burden, css_reference_2=500., seed=9)
        durability[vaccine_max_kill] = 1 - outcome.progressed.mean()
    assert durability[0.05] >= durability[0.0]


def test_single_patient_feasibility_demo_writes_expected_outputs(tmp_path):
    single_patient_feasibility_demo(tmp_path, breed="bmd", horizon_days=200, n_dogs=8,
                                    repeats_per_dog=10, seed=1)
    summary = json.loads((tmp_path / "summary.json").read_text())
    assert "uncertainty_decomposition" in summary
    assert "subclone_value_of_information" in summary
    assert "worst_best_case_bracket" in summary
    assert "interpretation" in summary
    assert "unverified_extrapolations" in summary
    decomposition = summary["uncertainty_decomposition"]
    assert 0 <= decomposition["intraclass_correlation"] <= 1
    table = pd.read_csv(tmp_path / "per_dog_probability.csv")
    assert len(table) == 8
    assert (tmp_path / "single_patient_feasibility.png").exists()


def test_worst_case_is_never_better_than_best_case_for_one_dog():
    """Sanity check on the bracket's own construction: the worst-case combination (least drug
    exposure, least drug-sensitive tumor, highest mutation rate, pre-existing subclone already
    present) must not outperform the best-case combination (the opposite on every axis)."""
    from canine_dsp.mapk_cli import (
        _DETECTABLE_SUBCLONE_FRACTION,
        _PERCENTILE_Z,
        combination_scenarios,
    )
    from canine_dsp.mapk_resistance import run_monte_carlo_fixed_patient
    from dataclasses import replace as dc_replace

    scenarios = combination_scenarios(breed="bmd", max_kill_2_values=[0.05])
    model, css, seeding_rates, initial_burden, _ = scenarios[0.05]
    css_2 = 500.0
    k = len(model.growth)

    no_subclone = np.zeros(k); no_subclone[0] = initial_burden
    dominant_index = 1 + int(np.argmax(seeding_rates))
    has_subclone = no_subclone.copy()
    has_subclone[0] *= (1 - _DETECTABLE_SUBCLONE_FRACTION)
    has_subclone[dominant_index] = initial_burden * _DETECTABLE_SUBCLONE_FRACTION

    low_exposure, high_exposure = np.exp(-_PERCENTILE_Z * .3), np.exp(_PERCENTILE_Z * .3)
    low_ic50, high_ic50 = np.exp(-_PERCENTILE_Z * .2), np.exp(_PERCENTILE_Z * .2)
    low_rate, high_rate = np.exp(-_PERCENTILE_Z * .5), np.exp(_PERCENTILE_Z * .5)

    outcomes = {}
    for label, css_mult, ic50_mult, rate_mult, initial in (
        ("worst_case", low_exposure, high_ic50, high_rate, has_subclone),
        ("best_case", high_exposure, low_ic50, low_rate, no_subclone),
    ):
        bracket_model = dc_replace(model, ic50_nM=model.ic50_nM * ic50_mult)
        outcome = run_monte_carlo_fixed_patient(bracket_model, css * css_mult, 1825,
                                                seeding_rates * rate_mult, initial, repeats=120,
                                                css_2=css_2 * css_mult, seed=5)
        outcomes[label] = 1 - outcome.progressed.mean()
    assert outcomes["best_case"] >= outcomes["worst_case"]
