import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from canine_dsp.osteosarcoma_benchmark import (
    DEFAULT_DESIGN_WEIGHTS,
    PRIOR_EQUIVALENCE_TOLERANCE,
    _ablation_models,
    _anchor_dog_clock,
    _cargo_design,
    _fixed_prior_soc_comparison,
    _illustrative_escape_target,
    _joint_inverse_search,
    _policy_metrics,
    illustrative_canine_antigens,
    load_clinical_anchors,
    run_osteosarcoma_benchmark,
)
from canine_dsp.osteosarcoma_design import SpeciesScenario
from canine_dsp.osteosarcoma_hsmm import Species, reference_osteosarcoma_hsmm
from canine_dsp.osteosarcoma_spec import DesignSpecification, illustrative_canine_design_spec


ANCHORS = Path(__file__).parents[1] / "data/clinical/osteosarcoma_clinical_anchors.csv"


def test_osteosarcoma_evidence_preserves_randomized_and_registry_boundaries():
    table = load_clinical_anchors(ANCHORS).set_index("record_id")
    assert float(table.loc["cotc022_soc_median_dfi", "estimate"]) == 180
    assert float(table.loc["cotc022_soc_median_os", "estimate"]) == 282
    assert float(table.loc["euramos_m0_csr_5y_efs", "estimate"]) == 64
    assert table.loc["rna_prime_trial_status", "evidence_tier"] == "D_registry_no_outcomes"
    assert table.loc["rna_prime_trial_status", "study_status"] == (
        "active_not_recruiting_no_posted_results"
    )
    assert table.loc["uf_canine_rna_pd1_trial_status", "study_status"] == (
        "recruiting_no_posted_results"
    )
    assert table.loc["rt_listeria_2026_median_os", "intervention_class"] == (
        "non_RNA_Listeria_vaccine_plus_radiation"
    )
    assert table.loc["canine_rna_lpa_pilot_acute_activity", "n"] == 5
    assert table.comparability_caveat.str.len().min() > 20
    registry = table.evidence_tier.eq("D_registry_no_outcomes")
    assert pd.to_numeric(table.loc[registry, "estimate"], errors="coerce").isna().all()
    assert table.loc[registry, "unit"].eq("status").all()


def test_default_antigens_are_unambiguously_illustrative_and_species_valid():
    candidates = illustrative_canine_antigens()
    assert len(candidates) == 12
    assert all(candidate.candidate_id.startswith("ILLUSTRATIVE_DOG_")
               for candidate in candidates)
    assert all(allele.startswith("DLA-") for candidate in candidates
               for allele in candidate.class_i_alleles | candidate.class_ii_alleles)


def test_nominal_scenario_must_be_an_unperturbed_identity():
    candidates = illustrative_canine_antigens()
    base = illustrative_canine_design_spec(candidates[0].candidate_id)
    specification = DesignSpecification(
        constraints=base.constraints,
        scenarios=(
            SpeciesScenario("nominal", "canine", expression_scale=.9),
        ),
    )

    with pytest.raises(ValueError, match="unperturbed identity"):
        _cargo_design(candidates, specification)


def test_joint_scenarios_perturb_hsmm_and_nominal_outputs_are_consistent():
    candidates = illustrative_canine_antigens()
    escape_target = _illustrative_escape_target(candidates)
    specification = illustrative_canine_design_spec(escape_target)
    design = _cargo_design(candidates, specification)
    model = _anchor_dog_clock(reference_osteosarcoma_hsmm(memory=8, rank=2))

    joint, scenarios, selected, selected_inputs = _joint_inverse_search(
        model, design, candidates, specification,
    )

    assert escape_target in selected["candidate_ids"]
    selected_scenarios = scenarios.loc[
        scenarios.cargo_rank.eq(selected["cargo_rank"])
        & scenarios.schedule.eq(selected["schedule"])
    ].set_index("scenario")
    nominal = selected_scenarios.loc["nominal"]
    perturbed = selected_scenarios.drop(index="nominal")
    assert np.all(
        np.abs(
            perturbed.prior_objective.to_numpy()
            - nominal.prior_objective
        ) > 1e-12
    )
    assert (
        selected_scenarios.loc[
            "single_antigen_loss", "effective_antigen_coverage_proxy"
        ]
        < nominal.effective_antigen_coverage_proxy
    )

    winner = joint.iloc[0]
    recomputed = _policy_metrics(model, selected_inputs)[0]
    assert winner.cargo_rank == selected["cargo_rank"]
    assert winner.schedule == selected["schedule"]
    assert winner.nominal_prior_objective == pytest.approx(
        recomputed["prior_objective"]
    )
    assert (
        winner.nominal_exact_prior_ever_visible_relapse_probability
        == pytest.approx(
            recomputed["exact_prior_ever_visible_relapse_probability"]
        )
    )
    scenario_weights = selected_scenarios.scenario_weight.to_numpy(float)
    objectives = selected_scenarios.prior_objective.to_numpy(float)
    mean_weight = DEFAULT_DESIGN_WEIGHTS.robust_mean_weight
    expected_robust = (
        (1 - mean_weight) * objectives.min()
        + mean_weight * np.average(objectives, weights=scenario_weights)
    )
    assert selected["worst_case_prior_objective"] == pytest.approx(
        objectives.min()
    )
    assert selected["robust_prior_objective"] == pytest.approx(expected_robust)


def test_fixed_prior_soc_gate_uses_worst_case_and_equivalence_tolerance():
    tolerance = PRIOR_EQUIVALENCE_TOLERANCE
    comparator = {
        "prior_objective": -1.0,
        "exact_prior_ever_visible_relapse_probability": .5,
    }
    selected = {
        "robust_prior_objective": 100.0,
        "worst_case_prior_objective": -1.0 + tolerance / 2,
        "worst_case_exact_prior_ever_visible_relapse_probability": (
            .5 - 2 * tolerance
        ),
    }

    near_equivalent = _fixed_prior_soc_comparison(selected, comparator)
    assert not near_equivalent["favors_candidate"]

    selected["worst_case_prior_objective"] = -1.0 + 2 * tolerance
    favored = _fixed_prior_soc_comparison(selected, comparator)
    assert favored["favors_candidate"]
    assert favored["worst_case_objective_advantage_vs_soc"] == pytest.approx(
        2 * tolerance
    )
    assert favored["worst_case_relapse_probability_reduction_vs_soc"] == pytest.approx(
        2 * tolerance
    )


def test_program_exports_inverse_design_visuals_and_fails_closed(tmp_path):
    # A recognized prior output may be replaced, and none of its stale files
    # may survive publication of the new complete tree.
    (tmp_path / "run_manifest.json").write_text(json.dumps({
        "schema_version": 1,
        "program": "comparative_osteosarcoma_rna_vaccine_inverse_design",
        "status": "COMPLETE",
    }))
    (tmp_path / "stale_previous_artifact.txt").write_text("old run")
    summary = run_osteosarcoma_benchmark(
        tmp_path, anchors=ANCHORS, draws=16, seed=8)
    assert not (tmp_path / "stale_previous_artifact.txt").exists()
    saved = json.loads((tmp_path / "summary.json").read_text())
    assert saved == summary
    assert summary["candidate_origin"] == "illustrative_synthetic_feature_panel"
    assert not summary["clinical_superiority_supported"]
    assert not summary["patient_treatment_recommendation"]
    assert summary["clinical_evidence_status"].startswith("NOT_CLINICALLY_EVALUABLE")
    assert summary["real_data_evaluation"]["status"] == "not_run"
    clock = summary["dog_clock_prior_anchor"]
    assert clock["source"] == "COTC022 aggregate standard-care median DFI"
    assert clock["target_days"] == 180
    assert clock["duration_scale_multiplier"] == 1.29
    assert clock["achieved_soc_proxy_median_first_visible_relapse_days"] is not None
    assert clock["absolute_calibration_error_days"] <= 7
    assert clock["visible_relapse_probability_at_day_zero"] == 0
    assert not clock["patient_level_fit"]
    assert summary["policy_probability_computation"] == "exact_not_monte_carlo"
    assert len(summary["selected_research_hypothesis"]["candidate_ids"]) >= 4
    joint = pd.read_csv(tmp_path / "joint_cargo_schedule_search.csv")
    assert joint.role.eq("prior_driven_research_hypothesis_not_recommendation").all()
    assert joint.schedule_extrapolation.all()
    assert not joint.rna_policy_observed.any()
    assert joint.joint_rank.is_unique
    scenarios = pd.read_csv(tmp_path / "joint_cargo_schedule_scenarios.csv")
    assert scenarios.scenario.nunique() == len(
        summary["design_specification"]["scenarios"]
    )
    audit = pd.read_csv(tmp_path / "identifiability_audit.csv").set_index("component")
    assert audit.loc["second-order interaction", "status"] == "NOT_IDENTIFIABLE"
    ablation = pd.read_csv(tmp_path / "synthetic_model_ablation.csv")
    assert set(ablation.model) == {
        "full_second_order_volterra_hsmm",
        "first_order_volterra_hsmm",
        "hsmm_no_volterra",
        "mean_matched_truncated_geometric_hmm_second_order",
    }
    for name in [
        "cargo_selection.png", "clinical_anchors.png", "filtered_state_probabilities.png",
        "volterra_transition_memory.png", "clinical_interpretation.md",
        "prospective_validation_protocol.csv", "cargo_scenario_contributions.csv",
    ]:
        assert (tmp_path / name).stat().st_size > 0
    manifest = json.loads((tmp_path / "run_manifest.json").read_text())
    assert manifest["status"] == "COMPLETE"
    delayed = manifest["schedule_hypotheses"]["delayed_prime_boost"]
    assert delayed["analog_source_url"].startswith("https://pubmed.ncbi.nlm.nih.gov/")
    assert delayed["analog_secondary_source_url"].startswith(
        "https://clinicaltrials.gov/"
    )
    assert "osteosarcoma_viz.py" in manifest["runtime"]["code_file_sha256"]
    dog_dfi = summary["current_care_reference_anchors"][
        "canine_localized_standard_care"
    ]["median_dfi"]
    assert dog_dfi["study_status"] == "completed"
    assert dog_dfi["intervention_class"] == "current_standard_care"
    inventory = manifest["artifact_inventory"]
    actual_files = {
        path.relative_to(tmp_path).as_posix()
        for path in tmp_path.rglob("*")
        if path.is_file() and path.name != "run_manifest.json"
    }
    assert set(inventory) == actual_files
    assert "run_manifest.json" not in inventory
    for relative, record in inventory.items():
        payload = (tmp_path / relative).read_bytes()
        assert record["sha256"] == hashlib.sha256(payload).hexdigest()
        assert record["bytes"] == len(payload)
    ranking = pd.read_csv(tmp_path / "candidate_antigen_ranking.csv")
    assert ranking.joint_selected.sum() == len(
        summary["selected_research_hypothesis"]["candidate_ids"])


def test_real_candidate_file_requires_patient_specific_design_spec(tmp_path):
    out = tmp_path / "out"
    with pytest.raises(ValueError, match="requires --design-spec"):
        run_osteosarcoma_benchmark(
            out,
            anchors=ANCHORS,
            candidate_file=tmp_path / "candidate.csv",
            draws=16,
        )
    assert not out.exists()
    assert not list(tmp_path.glob(".out.staging-*"))


def test_failed_rerun_preserves_prior_successful_output(tmp_path):
    out = tmp_path / "owned"
    out.mkdir()
    prior_summary = json.dumps({
        "program": "comparative_osteosarcoma_rna_vaccine_inverse_design",
        "sentinel": "prior successful output",
    })
    prior_manifest = json.dumps({
        "schema_version": 1,
        "program": "comparative_osteosarcoma_rna_vaccine_inverse_design",
        "status": "COMPLETE",
    })
    (out / "summary.json").write_text(prior_summary)
    (out / "run_manifest.json").write_text(prior_manifest)
    (out / "prior_artifact.csv").write_text("value\n7\n")
    before = {path.name: path.read_bytes() for path in out.iterdir()}

    with pytest.raises(ValueError, match="requires --design-spec"):
        run_osteosarcoma_benchmark(
            out,
            anchors=ANCHORS,
            candidate_file=tmp_path / "missing_candidates.csv",
            draws=16,
        )
    after = {path.name: path.read_bytes() for path in out.iterdir()}
    assert after == before
    assert not list(tmp_path.glob(".owned.staging-*"))


def test_inputs_inside_output_are_rejected_before_any_work(tmp_path):
    out = tmp_path / "result"
    out.mkdir()
    nested_candidates = out / "candidates.csv"
    nested_candidates.write_text("candidate_id\nunsafe-location\n")
    with pytest.raises(ValueError, match="inside the output directory"):
        run_osteosarcoma_benchmark(
            out,
            anchors=ANCHORS,
            candidate_file=nested_candidates,
            draws=16,
        )
    assert list(out.iterdir()) == [nested_candidates]
    assert not list(tmp_path.glob(".result.staging-*"))


def test_git_repository_root_is_never_an_atomic_publish_target(tmp_path):
    repository = tmp_path / "repository"
    (repository / ".git").mkdir(parents=True)
    with pytest.raises(ValueError, match="Git repository root"):
        run_osteosarcoma_benchmark(repository, anchors=ANCHORS, draws=16)
    assert not (repository / "run_manifest.json").exists()
    assert not list(tmp_path.glob(".repository.staging-*"))


def test_geometric_ablation_matches_each_state_mean_dwell_time():
    model = _anchor_dog_clock(reference_osteosarcoma_hsmm(memory=8, rank=2))
    geometric = _ablation_models(model)[
        "mean_matched_truncated_geometric_hmm_second_order"]
    for species in Species:
        original = model.species_parameters[species].duration_hazards
        challenger = geometric.species_parameters[species].duration_hazards
        original_mean = np.concatenate([
            np.ones((len(original), 1)),
            np.cumprod(1 - original[:, :-1], axis=1),
        ], axis=1).sum(axis=1)
        challenger_mean = np.concatenate([
            np.ones((len(challenger), 1)),
            np.cumprod(1 - challenger[:, :-1], axis=1),
        ], axis=1).sum(axis=1)
        np.testing.assert_allclose(challenger_mean, original_mean, atol=1e-9)


def test_custom_canine_panel_and_design_spec_run_without_demo_labels(tmp_path):
    candidate_path = tmp_path / "candidates.csv"
    pd.DataFrame([
        {
            "candidate_id": f"REAL_FEATURE_{index}",
            "species": "canine",
            "source_class": "fusion" if index == 0 else "snv",
            "expression": .8,
            "clonality": .8,
            "truncality": .9 if index < 3 else .7,
            "mhc_i_presentation": .8,
            "mhc_ii_presentation": .75,
            "normal_proteome_safety": .95,
            "presentation_retention": .85,
            "escape_risk": .1,
            "manufacturability": .9,
            "subclones": "founder;pulmonary_clone" if index % 2 == 0 else "founder",
            "class_i_alleles": "DLA-88*034:01",
            "class_ii_alleles": "DLA-DRB1*001:01",
        }
        for index in range(5)
    ]).to_csv(candidate_path, index=False)
    spec_path = tmp_path / "design.json"
    spec_path.write_text(json.dumps({
        "schema_version": 1,
        "constraints": {
            "species": "canine",
            "min_antigens": 2,
            "max_antigens": 3,
            "min_class_i_antigens": 1,
            "min_class_ii_antigens": 1,
            "min_truncal_antigens": 1,
            "required_subclones": ["founder", "pulmonary_clone"],
            "required_class_i_alleles": ["DLA-88*034:01"],
            "required_class_ii_alleles": ["DLA-DRB1*001:01"],
            "required_source_classes": ["fusion"],
        },
        "scenarios": [
            {"name": "nominal", "species": "canine"},
            {
                "name": "custom_dla_loss",
                "species": "canine",
                "lost_class_i_alleles": ["DLA-88*034:01"],
            },
        ],
    }))
    summary = run_osteosarcoma_benchmark(
        tmp_path / "custom_run",
        anchors=ANCHORS,
        candidate_file=candidate_path,
        design_spec_file=spec_path,
        draws=16,
    )
    assert summary["candidate_origin"] == "user_supplied_deidentified_feature_table"
    assert summary["design_specification"]["constraints"]["required_subclones"] == [
        "founder", "pulmonary_clone"]
    assert all(candidate_id.startswith("REAL_FEATURE_") for candidate_id in
               summary["selected_research_hypothesis"]["candidate_ids"])
