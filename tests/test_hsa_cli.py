import json

import pytest

from canine_dsp.hsa_cli import hsa_resistance_demo, hsa_vaccine_followon_demo
from canine_dsp.hsa_scenarios import (
    HSA_CLONE_NAMES,
    HSA_VACCINE_CLONE_NAMES,
    dog_hsa_preset,
    hsa_vaccine_followon_scenarios,
)


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


def test_hsa_vaccine_followon_scenarios_rejects_nonzero_second_drug():
    with pytest.raises(NotImplementedError):
        hsa_vaccine_followon_scenarios(cdk46_max_kill=0.05)


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


def test_hsa_vaccine_followon_demo_higher_potency_does_not_reduce_durable_response(tmp_path):
    hsa_vaccine_followon_demo(tmp_path, horizon_days=365, trials=150, seed=2)
    sensitivity = json.loads((tmp_path / "summary.json").read_text())["sensitivity"]
    durable = [row["probability_durable_response"] for row in sensitivity]
    assert durable == sorted(durable)
