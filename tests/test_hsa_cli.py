import json
import sys

import pandas as pd
import pytest

from canine_dsp import cli
from canine_dsp.hsa_cli import (
    hsa_combination_control_demo,
    hsa_combination_search_demo,
    hsa_combination_toxicity_demo,
    hsa_durability_horizon_demo,
    hsa_resistance_demo,
    hsa_vaccine_followon_demo,
)
from canine_dsp.hsa_scenarios import (
    HSA_CLONE_NAMES,
    HSA_COMBINED_EXPOSURE_DERATING,
    HSA_DURABILITY_HORIZON_SWEEP,
    HSA_VACCINE_CLONE_NAMES,
    _PREEXISTING_PROB_CENTRAL,
    dog_hsa_preset,
    hsa_combination_scenarios,
    hsa_vaccine_followon_scenarios,
)


def test_preexisting_prob_central_recentered_to_pessimistic_end():
    # Recentered from 0.30 to 0.70 after comparing this scenario's output against the one real
    # HSA efficacy benchmark available (eBAT) -- see hsa_scenarios.py's comment for the reasoning
    # and its limits. This pins the value so a future edit can't silently drift it back.
    assert _PREEXISTING_PROB_CENTRAL == 0.70


def test_cli_hsa_demo_defaults_do_not_drift_from_the_recentered_constant(tmp_path, monkeypatch):
    # Regression test for a real bug: cli.py's argparse --preexisting-prob defaults were once
    # hardcoded literals (0.30) duplicating hsa_scenarios._PREEXISTING_PROB_CENTRAL, so when that
    # constant was recentered to 0.70, every hsa_* CLI command silently kept using the stale 0.30
    # default unless --preexisting-prob was passed explicitly. cli.py now imports the constant
    # directly instead of duplicating its value; this checks the CLI path end-to-end, not just
    # that the Python-level function default is correct.
    monkeypatch.setattr(sys, "argv", [
        "canine-dsp", "hsa-vaccine-followon-demo", "--trials", "10", "--horizon-days", "60",
        "--out", str(tmp_path),
    ])
    cli.main()
    summary = json.loads((tmp_path / "summary.json").read_text())
    assert summary["preexisting_prob_used"] == _PREEXISTING_PROB_CENTRAL


def test_cli_hsa_toxicity_and_durability_demos_do_not_drift_from_the_scenario_constant(
        tmp_path, monkeypatch):
    # Same CLI-default-drift bug class, exercised for the two demos added alongside this test.
    tox_out = tmp_path / "tox"
    monkeypatch.setattr(sys, "argv", [
        "canine-dsp", "hsa-combination-toxicity-demo", "--trials", "10", "--horizon-days", "60",
        "--out", str(tox_out),
    ])
    cli.main()
    tox_summary = json.loads((tox_out / "summary.json").read_text())
    assert tox_summary["preexisting_prob_used"] == _PREEXISTING_PROB_CENTRAL

    durability_out = tmp_path / "durability"
    monkeypatch.setattr(sys, "argv", [
        "canine-dsp", "hsa-durability-horizon-demo", "--trials", "10",
        "--out", str(durability_out),
    ])
    cli.main()
    durability_summary = json.loads((durability_out / "summary.json").read_text())
    assert durability_summary["preexisting_prob_used"] == _PREEXISTING_PROB_CENTRAL


def test_dog_hsa_preset_ic50_anchored_to_real_cell_line_mean():
    model, css_reference, seeding_rates, provenance = dog_hsa_preset()
    cell_line_ic50 = provenance["calibrated_from_data"]["sensitive_clone_ic50_nM"]
    assert model.ic50_nM[0] == sum(cell_line_ic50.values()) / len(cell_line_ic50)
    assert len(model.growth) == len(HSA_CLONE_NAMES) == 4
    assert seeding_rates.shape == (3,)


def test_dog_hsa_preset_css_reference_is_illustrative_margin_not_rapamycin_trough():
    # css_reference must sit comfortably above the sensitive clone's real IC50 (an illustrative
    # margin), not at rapamycin's real ~10.9 nM trough concentration -- pairing that real number
    # with a different drug's real IC50 would predict the drug barely works at all, contradicting
    # the real FidoCure survival benefit documented in the module docstring.
    model, css_reference, _, _ = dog_hsa_preset()
    assert css_reference > model.ic50_nM[0]
    assert css_reference != 10.0 * 1000 / 914.17


def test_hsa_resistance_demo_writes_expected_outputs(tmp_path):
    hsa_resistance_demo(tmp_path, trials=20, horizon_days=90, seed=1)
    summary = json.loads((tmp_path / "summary.json").read_text())
    assert len(summary["preexisting_prob_sensitivity"]) == 5
    assert (tmp_path / "preexisting_prob_sensitivity.csv").exists()
    assert (tmp_path / "trajectory_quantiles.csv").exists()
    assert (tmp_path / "escape_mechanism_breakdown.csv").exists()
    assert (tmp_path / "hsa_resistance_monte_carlo.png").exists()
    assert "unverified_extrapolations" in summary
    assert "hsa_rapamycin_real_world_benchmark" in summary
    assert "hsa_standard_of_care_benchmark" in summary


def test_hsa_resistance_demo_durable_response_decreases_with_preexisting_prob(tmp_path):
    hsa_resistance_demo(tmp_path, trials=150, horizon_days=730, seed=3)
    sweep = json.loads((tmp_path / "summary.json").read_text())["preexisting_prob_sensitivity"]
    durable = [row["probability_durable_response"] for row in sweep]
    assert durable == sorted(durable, reverse=True)


def test_hsa_vaccine_followon_scenarios_adds_fifth_clone_inheriting_pi3k_akt_feedback():
    scenarios = hsa_vaccine_followon_scenarios(vaccine_max_kill_values=[0.0])
    model, _, seeding_rates, _ = scenarios[0.0]
    base_model, _, base_seeding_rates, _ = dog_hsa_preset()
    assert len(model.growth) == 5 == len(HSA_VACCINE_CLONE_NAMES)
    assert model.growth[4] < base_model.growth[1]  # inherits clone 1 with a fitness penalty
    assert seeding_rates.shape == base_seeding_rates.shape


def test_hsa_combination_scenarios_zero_kill_matches_inhibitor_only():
    scenarios = hsa_combination_scenarios(ebat_max_kill_values=[0.0])
    combo_model, css, seeding_rates, _ = scenarios[0.0]
    base_model, base_css, base_seeding_rates, _ = dog_hsa_preset()
    assert combo_model.ic50_nM_2 is None and combo_model.max_kill_2 is None
    assert css == base_css
    assert (seeding_rates == base_seeding_rates).all()


def test_hsa_combination_scenarios_inactive_inhibitor_zeros_css():
    scenarios = hsa_combination_scenarios(inhibitor_active=False, ebat_max_kill_values=[0.05])
    _, css, _, provenance = scenarios[0.05]
    assert css == 0.0
    assert provenance["inhibitor_active"] is False


def test_hsa_vaccine_followon_scenarios_with_ebat_carries_second_drug_onto_fifth_clone():
    scenarios = hsa_vaccine_followon_scenarios(ebat_max_kill=0.05, vaccine_max_kill_values=[0.0])
    model, _, _, _ = scenarios[0.0]
    assert model.max_kill_2 == 0.05
    assert len(model.growth) == 5


def test_hsa_combination_control_demo_writes_both_regimens(tmp_path):
    hsa_combination_control_demo(tmp_path, trials=20, horizon_days=90, seed=1)
    summary = json.loads((tmp_path / "summary.json").read_text())
    regimens = {row["regimen"] for row in summary["sensitivity"]}
    assert regimens == {"combination", "ebat_monotherapy"}
    assert (tmp_path / "hsa_combination_sensitivity.csv").exists()
    assert "real_ebat_trial" in summary


def test_hsa_combination_search_demo_writes_grid_and_ebat_monotherapy_point(tmp_path):
    hsa_combination_search_demo(tmp_path, trials=20, horizon_days=90, seed=1)
    summary = json.loads((tmp_path / "summary.json").read_text())
    assert (tmp_path / "hsa_combination_search_grid.csv").exists()
    assert (tmp_path / "hsa_combination_search_grid.png").exists()
    assert "ebat_monotherapy_no_inhibitor" in summary
    assert "minimal_combinations_reaching_threshold" in summary
    assert len(summary["grid"]) == 25  # 5 ebat values x 5 vaccine values


def test_hsa_combination_toxicity_demo_derating_scales_both_drug_exposures(tmp_path):
    hsa_combination_toxicity_demo(tmp_path, ebat_max_kill=0.05, trials=20, horizon_days=90, seed=1)
    table = pd.read_csv(tmp_path / "hsa_toxicity_derating_sensitivity.csv")
    assert len(table) == len(HSA_COMBINED_EXPOSURE_DERATING)
    full_dose = table[table["combined_exposure_derating"] == 1.0].iloc[0]
    low_dose = table[table["combined_exposure_derating"] == 0.4].iloc[0]
    assert low_dose["inhibitor_css_nM"] == pytest.approx(full_dose["inhibitor_css_nM"] * 0.4)
    assert low_dose["ebat_css_nM"] == pytest.approx(full_dose["ebat_css_nM"] * 0.4)
    summary = json.loads((tmp_path / "summary.json").read_text())
    assert "toxicity_extrapolation_rationale" in summary
    assert (tmp_path / "hsa_toxicity_derating.png").exists()


def test_hsa_durability_horizon_demo_writes_full_sweep(tmp_path):
    hsa_durability_horizon_demo(tmp_path, ebat_max_kill=0.05, vaccine_max_kill=0.0,
                                trials=20, seed=1)
    table = pd.read_csv(tmp_path / "hsa_durability_horizon_sensitivity.csv")
    assert len(table) == len(HSA_DURABILITY_HORIZON_SWEEP)
    assert list(table["horizon_days"]) == HSA_DURABILITY_HORIZON_SWEEP
    summary = json.loads((tmp_path / "summary.json").read_text())
    assert "unverified_extrapolations" in summary
    assert (tmp_path / "hsa_durability_horizon.png").exists()


def test_adding_inhibitor_to_ebat_can_erode_long_horizon_durability_more_than_ebat_alone(tmp_path):
    """Real, seed-robust finding surfaced by extending HSA's durability check to 10 years: at
    ebat_max_kill=0.05, relapse under inhibitor+eBAT is driven by resistance mechanisms specific
    to the *inhibitor* (pi3k_akt_feedback_reactivation, target_site_mutation), which only gain a
    foothold because the inhibitor's own selection pressure exists -- eBAT alone, with no
    inhibitor to select against, never lets either route establish. This pins that the combined
    regimen is NOT simply better than or equal to eBAT alone in this model, so a future change
    that silently reverses this (making combination >= monotherapy everywhere) doesn't slip by
    unnoticed."""
    with_inhibitor = tmp_path / "with_inhibitor"
    hsa_durability_horizon_demo(with_inhibitor, ebat_max_kill=0.05, vaccine_max_kill=0.0,
                                inhibitor_active=True, trials=300, seed=1)
    without_inhibitor = tmp_path / "without_inhibitor"
    hsa_durability_horizon_demo(without_inhibitor, ebat_max_kill=0.05, vaccine_max_kill=0.0,
                                inhibitor_active=False, trials=300, seed=1)

    with_summary = json.loads((with_inhibitor / "summary.json").read_text())
    without_summary = json.loads((without_inhibitor / "summary.json").read_text())
    ten_year_with = [r for r in with_summary["sensitivity"] if r["horizon_days"] == 3650][0]
    ten_year_without = [r for r in without_summary["sensitivity"] if r["horizon_days"] == 3650][0]
    assert ten_year_with["probability_durable_response"] < ten_year_without["probability_durable_response"]
    assert ten_year_without["probability_durable_response"] > 0.99


def test_inhibitor_alone_plateaus_rather_than_continuing_to_erode(tmp_path):
    """The inhibitor-alone baseline reaches a stable ~30% durable-response floor by year 2 and
    stays there through year 10, rather than continuing to decay the way the borderline
    inhibitor+eBAT combination does -- the one row in the full endurance picture anchored to
    anything real (see hsa_scenarios' eBAT-trial-based preexisting_prob recentering)."""
    hsa_durability_horizon_demo(tmp_path, ebat_max_kill=0.0, vaccine_max_kill=0.0,
                               inhibitor_active=True, trials=300, seed=1)
    table = pd.read_csv(tmp_path / "hsa_durability_horizon_sensitivity.csv")
    five_year = table.loc[table["horizon_days"] == 1825, "probability_durable_response"].iloc[0]
    ten_year = table.loc[table["horizon_days"] == 3650, "probability_durable_response"].iloc[0]
    assert abs(five_year - ten_year) < 0.05


def test_hsa_durability_horizon_demo_runs_vaccine_only_and_ebat_only_paths(tmp_path):
    # vaccine_max_kill=0.0 must still route through the 5-clone vaccine model without crashing
    # (a harmless immune-escape clone), so both eBAT-only and vaccine-only regimens go through
    # the same code path as the full three-way combination.
    ebat_only = tmp_path / "ebat_only"
    hsa_durability_horizon_demo(ebat_only, ebat_max_kill=0.05, vaccine_max_kill=0.0,
                                trials=15, seed=2)
    vaccine_only = tmp_path / "vaccine_only"
    hsa_durability_horizon_demo(vaccine_only, ebat_max_kill=0.0, vaccine_max_kill=0.05,
                                trials=15, seed=2)
    assert (ebat_only / "hsa_durability_horizon_sensitivity.csv").exists()
    assert (vaccine_only / "hsa_durability_horizon_sensitivity.csv").exists()


def test_hsa_vaccine_followon_demo_writes_expected_outputs(tmp_path):
    hsa_vaccine_followon_demo(tmp_path, horizon_days=90, trials=20, seed=1)
    summary = json.loads((tmp_path / "summary.json").read_text())
    assert len(summary["sensitivity"]) == 5
    assert (tmp_path / "hsa_vaccine_followon_sensitivity.csv").exists()
    assert (tmp_path / "hsa_vaccine_followon.png").exists()
    assert "real_hsa_vaccine_trials" in summary
    assert set(summary["real_hsa_vaccine_trials"]) == {
        "erstreps", "evim", "autologous_whole_cell",
        "vegfr2_dna_negative_control", "calviri_frameshift_peptide",
    }


def test_hsa_vaccine_followon_scenarios_inhibitor_inactive_zeros_css():
    scenarios = hsa_vaccine_followon_scenarios(inhibitor_active=False,
                                               vaccine_max_kill_values=[0.0])
    _, css, _, _ = scenarios[0.0]
    assert css == 0.0


def test_hsa_vaccine_alone_needs_high_potency_to_reach_durable_response(tmp_path):
    # Vaccine with no inhibitor and no eBAT: low potency should fail almost immediately (no drug
    # is suppressing the bulk tumor at all), but sufficiently high vaccine potency should still
    # close the gap on its own, matching the potency threshold found for the drug-combined case.
    hsa_vaccine_followon_demo(tmp_path, inhibitor_active=False, horizon_days=730, trials=200, seed=4)
    sensitivity = json.loads((tmp_path / "summary.json").read_text())["sensitivity"]
    by_potency = {row["vaccine_max_kill"]: row["probability_durable_response"] for row in sensitivity}
    assert by_potency[0.0] < 0.1
    assert by_potency[0.08] > 0.9


def test_hsa_vaccine_followon_demo_higher_potency_does_not_reduce_durable_response(tmp_path):
    hsa_vaccine_followon_demo(tmp_path, horizon_days=365, trials=150, seed=2)
    sensitivity = json.loads((tmp_path / "summary.json").read_text())["sensitivity"]
    durable = [row["probability_durable_response"] for row in sensitivity]
    assert durable == sorted(durable)
