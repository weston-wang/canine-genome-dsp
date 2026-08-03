import json

import numpy as np
import pandas as pd
import pytest

from canine_dsp.mapk_cli import (
    BRAIN_PENETRATION_FRACTION,
    CDK46_MAX_KILL_SWEEP,
    COMBINED_EXPOSURE_DERATING,
    canine_cns_hs_scenarios,
    combination_control_demo,
    combination_scenarios,
    combination_toxicity_demo,
    localized_control_demo,
    localized_pihs_scenarios,
    mapk_cns_demo,
)
from canine_dsp.mapk_resistance import run_monte_carlo


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
