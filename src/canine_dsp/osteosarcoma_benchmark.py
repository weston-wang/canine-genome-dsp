"""Fail-closed comparative osteosarcoma RNA-vaccine design benchmark.

The benchmark joins four deliberately separated evidence layers:

* real aggregate dog/human clinical anchors;
* a real 33-dog pretreatment expression/DFI prognostic sensitivity analysis;
* robust multivalent cargo selection from supplied candidate measurements; and
* a species-aware Volterra-HSMM prior for software and prospective-design work.

No public dataset currently identifies a counterfactual RNA-vaccine policy in
osteosarcoma.  Consequently every optimized output is labeled a research
hypothesis and the clinical-superiority gate is hard-coded false.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import shutil
import tempfile
import uuid
from importlib import metadata
from dataclasses import replace
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

from .osteosarcoma_data import prepare_gse76127
from .osteosarcoma_design import (
    AntigenCandidate,
    AntigenSource,
    CargoDesignResult,
    CargoRanking,
    DesignWeights,
    Species as DesignSpecies,
    SpeciesScenario,
    _eligibility_reasons,
    design_vaccine_cargo,
)
from .osteosarcoma_hsmm import (
    N_STATES,
    OsteosarcomaState,
    OsteosarcomaVolterraHSMM,
    Species as HSMMSpecies,
    discrete_weibull_hazards,
    reference_osteosarcoma_hsmm,
)
from .osteosarcoma_spec import (
    DesignSpecification,
    illustrative_canine_design_spec,
    load_design_spec,
)
from .osteosarcoma_viz import (
    plot_cargo_selection,
    plot_clinical_anchors,
    plot_real_data_predictions,
    plot_state_posteriors,
    plot_volterra_memory,
)


DEFAULT_ANCHORS = Path("data/clinical/osteosarcoma_clinical_anchors.csv")
MODEL_STEP_DAYS = 7
MODEL_HORIZON_STEPS = 80
CARGO_TOP_K = 10
JOINT_CARGO_LIMIT = 5
CARGO_BEAM_WIDTH = 512
CARGO_EXACT_ENUMERATION_LIMIT = 200_000
DEFAULT_DESIGN_WEIGHTS = DesignWeights()
PROGRAM_ID = "comparative_osteosarcoma_rna_vaccine_inverse_design"
RESPONSE_PROXY_WEIGHTS = {
    "clone_coverage": .25,
    "allele_coverage": .15,
    "tumor_visibility": .25,
    "retained_presentation": .25,
    "interaction_modifier": .10,
}
POLICY_OBJECTIVE_WEIGHTS = {
    "pre_relapse_adaptive_control_occupancy": 1.0,
    "terminal_ned_without_prior_relapse": .35,
    "ever_visible_relapse": -1.1,
    "terminal_exhausted_without_prior_relapse": -.45,
    "normalized_rna_input": -.003,
}
PRIOR_EQUIVALENCE_TOLERANCE = 1e-3


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def load_clinical_anchors(path: str | Path) -> pd.DataFrame:
    """Load curated evidence while enforcing the fail-closed schema."""
    table = pd.read_csv(path)
    required = {
        "record_id", "study", "species", "setting", "design", "arm", "endpoint",
        "n", "estimate", "unit", "source_url", "access_date", "evidence_tier",
        "data_granularity", "study_status", "intervention_class",
        "comparability_caveat",
    }
    missing = required - set(table.columns)
    if missing:
        raise ValueError(f"clinical anchor table is missing columns: {sorted(missing)}")
    expected = {
        "cotc022_soc_median_dfi", "cotc022_soc_median_os",
        "cotc026_her2_vaccine_median_dfi", "cotc030_il15_median_dfi",
        "canine_rna_lpa_pilot_acute_activity", "rna_prime_trial_status",
        "uf_canine_rna_pd1_trial_status", "rt_listeria_2026_median_os",
        "euramos_m0_csr_5y_efs", "euramos_m0_csr_5y_os",
    }
    absent = expected - set(table.record_id)
    if absent:
        raise ValueError(f"clinical anchor table is missing required records: {sorted(absent)}")
    if table.record_id.duplicated().any() or table[
        ["comparability_caveat", "study_status", "intervention_class"]
    ].isna().any().any():
        raise ValueError(
            "clinical anchors require unique IDs, statuses, intervention classes, and caveats"
        )
    registry = table.evidence_tier.eq("D_registry_no_outcomes")
    registry_numeric = pd.to_numeric(table.loc[registry, "estimate"], errors="coerce")
    if registry_numeric.notna().any() or not table.loc[registry, "unit"].eq("status").all():
        raise ValueError("registry-only anchors cannot contain numeric clinical outcomes")
    return table


def _split(value: object) -> tuple[str, ...]:
    if pd.isna(value) or str(value).strip() == "":
        return ()
    return tuple(item.strip() for item in str(value).split(";") if item.strip())


def _float_tuple(value: object) -> tuple[float, ...]:
    return tuple(float(item) for item in _split(value))


def load_antigen_candidates(path: str | Path) -> list[AntigenCandidate]:
    """Load deidentified upstream candidate scores from a documented CSV schema."""
    table = pd.read_csv(path)
    required = {
        "candidate_id", "species", "source_class", "expression", "clonality",
        "truncality", "mhc_i_presentation", "mhc_ii_presentation",
        "normal_proteome_safety", "presentation_retention", "escape_risk",
        "manufacturability", "subclones", "class_i_alleles", "class_ii_alleles",
    }
    missing = required - set(table.columns)
    if missing:
        raise ValueError(f"candidate table is missing columns: {sorted(missing)}")
    identifier_columns = ("candidate_id", "species", "source_class", "subclones")
    for column in identifier_columns:
        missing_rows = table.index[table[column].isna()].tolist()
        if missing_rows:
            raise ValueError(
                f"candidate table column {column!r} is missing at CSV rows "
                f"{[row + 2 for row in missing_rows]}"
            )
    candidates = []
    for index, row in enumerate(table.to_dict("records"), start=2):
        if str(row["candidate_id"]).strip().lower() in {"nan", "none", "null"}:
            raise ValueError(f"candidate row {index}: candidate_id is not a valid identifier")
        try:
            candidates.append(AntigenCandidate(
                candidate_id=row["candidate_id"],
                species=row["species"],
                source_class=row["source_class"],
                expression=row["expression"],
                clonality=row["clonality"],
                truncality=row["truncality"],
                mhc_i_presentation=row["mhc_i_presentation"],
                mhc_ii_presentation=row["mhc_ii_presentation"],
                normal_proteome_safety=row["normal_proteome_safety"],
                presentation_retention=row["presentation_retention"],
                escape_risk=row["escape_risk"],
                manufacturability=row["manufacturability"],
                subclones=_split(row["subclones"]),
                class_i_alleles=_split(row["class_i_alleles"]),
                class_ii_alleles=_split(row["class_ii_alleles"]),
                gene=None if pd.isna(row.get("gene")) else str(row.get("gene")),
                synergy_loadings=_float_tuple(row.get("synergy_loadings", "")),
                competition_loadings=_float_tuple(row.get("competition_loadings", "")),
            ))
        except (TypeError, ValueError) as error:
            raise ValueError(f"candidate row {index}: {error}") from error
    return candidates


def illustrative_canine_antigens() -> list[AntigenCandidate]:
    """Return a transparent fake panel for exercising the inverse-design software.

    IDs are intentionally non-biological.  These rows must never be interpreted
    as discovered dog or human antigens.
    """
    sources = [
        AntigenSource.STRUCTURAL_VARIANT, AntigenSource.FUSION, AntigenSource.INDEL,
        AntigenSource.SNV, AntigenSource.STRUCTURAL_VARIANT, AntigenSource.FUSION,
        AntigenSource.SNV, AntigenSource.INDEL, AntigenSource.CANCER_TESTIS,
        AntigenSource.OVEREXPRESSED, AntigenSource.STRUCTURAL_VARIANT, AntigenSource.SNV,
    ]
    clones = [
        ("trunk", "lung_A"), ("trunk", "lung_B"), ("trunk",), ("lung_C",),
        ("trunk", "lung_C"), ("lung_A", "lung_B"), ("lung_B",), ("lung_C",),
        ("trunk",), ("lung_A",), ("lung_B", "lung_C"), ("trunk", "lung_A"),
    ]
    candidates = []
    for index, (source, subclones) in enumerate(zip(sources, clones, strict=True)):
        class_i = ("DLA-88*001:01",) if index % 2 == 0 else ("DLA-88*508:01",)
        class_ii = (("DLA-DRB1*015:01",) if index % 3 else ("DLA-DQA1*001:01",))
        candidates.append(AntigenCandidate(
            candidate_id=f"ILLUSTRATIVE_DOG_{index + 1:02d}",
            species="canine",
            source_class=source,
            expression=.58 + .035 * (index % 7),
            clonality=.62 + .04 * ((index + 2) % 6),
            truncality=.90 if "trunk" in subclones else .50 + .04 * (index % 4),
            mhc_i_presentation=.61 + .035 * (index % 6),
            mhc_ii_presentation=.56 + .04 * ((index + 3) % 6),
            normal_proteome_safety=.55 if index == 9 else .82 + .015 * (index % 7),
            presentation_retention=.70 + .025 * ((index + 1) % 7),
            escape_risk=.12 + .035 * (index % 5),
            manufacturability=.72 + .025 * ((index + 4) % 7),
            subclones=subclones,
            class_i_alleles=class_i,
            class_ii_alleles=class_ii,
            synergy_loadings=(.15 + .05 * (index % 3), .08 + .04 * (index % 4)),
            competition_loadings=(.04 + .02 * (index % 4), .03 + .015 * (index % 3)),
        ))
    return candidates


def _cargo_design(
    candidates: list[AntigenCandidate], specification: DesignSpecification,
) -> CargoDesignResult:
    if specification.constraints.species != DesignSpecies.CANINE:
        raise ValueError(
            "the integrated osteosarcoma clinical benchmark is canine-first; use the "
            "species-general cargo design API for human/HLA panels"
        )
    nominal = [scenario for scenario in specification.scenarios
               if scenario.name.lower() == "nominal"]
    if len(nominal) != 1:
        raise ValueError(
            "the integrated benchmark requires exactly one scenario named 'nominal'"
        )
    nominal_scenario = nominal[0]
    nominal_scales = (
        nominal_scenario.expression_scale,
        nominal_scenario.presentation_scale,
        nominal_scenario.retention_scale,
        nominal_scenario.escape_scale,
        nominal_scenario.manufacturability_scale,
        nominal_scenario.interaction_scale,
    )
    if (
        not np.allclose(nominal_scales, 1.0, atol=0, rtol=0)
        or nominal_scenario.lost_class_i_alleles
        or nominal_scenario.lost_class_ii_alleles
        or nominal_scenario.escaped_antigens
        or nominal_scenario.candidate_effect_scale
    ):
        raise ValueError(
            "the scenario named 'nominal' must be an unperturbed identity scenario"
        )
    class_i_universe = set().union(*(candidate.class_i_alleles for candidate in candidates))
    class_ii_universe = set().union(*(candidate.class_ii_alleles for candidate in candidates))
    for scenario in specification.scenarios:
        unknown_i = scenario.lost_class_i_alleles - class_i_universe
        unknown_ii = scenario.lost_class_ii_alleles - class_ii_universe
        if unknown_i or unknown_ii:
            raise ValueError(
                f"scenario {scenario.name!r} references unobserved loss alleles: "
                f"class-I={sorted(unknown_i)}, class-II={sorted(unknown_ii)}"
            )
    result = design_vaccine_cargo(
        candidates,
        specification.constraints,
        scenarios=specification.scenarios,
        weights=DEFAULT_DESIGN_WEIGHTS,
        top_k=CARGO_TOP_K,
        beam_width=CARGO_BEAM_WIDTH,
        exact_enumeration_limit=CARGO_EXACT_ENUMERATION_LIMIT,
    )
    return result


def _illustrative_escape_target(candidates: list[AntigenCandidate]) -> str:
    """Choose a high-risk candidate that passes the bundled hard eligibility gates."""
    if not candidates:
        raise ValueError("illustrative escape-target selection requires candidates")
    provisional = illustrative_canine_design_spec(candidates[0].candidate_id)
    eligible = [
        candidate for candidate in candidates
        if not _eligibility_reasons(candidate, provisional.constraints)
    ]
    if not eligible:
        raise ValueError("illustrative panel has no eligible antigen-loss target")
    return max(
        eligible,
        key=lambda candidate: (candidate.escape_risk, candidate.candidate_id),
    ).candidate_id


def _cargo_tables(result: CargoDesignResult,
                  candidates: Iterable[AntigenCandidate]) -> tuple[pd.DataFrame, pd.DataFrame]:
    by_id = {candidate.candidate_id: candidate for candidate in candidates}
    cargo_only_selected = set(result.selected.candidate_ids)
    candidate_rows = []
    for ranking in result.candidate_rankings:
        candidate = by_id[ranking.candidate_id]
        candidate_rows.append({
            "candidate_id": ranking.candidate_id,
            "robust_score": ranking.robust_singleton_score,
            "cargo_only_selected": ranking.candidate_id in cargo_only_selected,
            "source_class": candidate.source_class.value,
            "subclones": ";".join(sorted(candidate.subclones)),
            "class_i_alleles": ";".join(sorted(candidate.class_i_alleles)),
            "class_ii_alleles": ";".join(sorted(candidate.class_ii_alleles)),
            "expression": candidate.expression,
            "clonality": candidate.clonality,
            "truncality": candidate.truncality,
            "mhc_i_presentation": candidate.mhc_i_presentation,
            "mhc_ii_presentation": candidate.mhc_ii_presentation,
            "normal_proteome_safety": candidate.normal_proteome_safety,
            "presentation_retention": candidate.presentation_retention,
            "escape_risk": candidate.escape_risk,
            "manufacturability": candidate.manufacturability,
            "scenario_scores_json": json.dumps(ranking.scenario_scores, sort_keys=True),
            "worst_scenario": ranking.worst_scenario,
            "role": "research_hypothesis_not_vaccine_sequence",
        })
    for exclusion in result.exclusions:
        candidate = by_id[exclusion.candidate_id]
        candidate_rows.append({
            "candidate_id": exclusion.candidate_id,
            "robust_score": np.nan,
            "cargo_only_selected": False,
            "source_class": candidate.source_class.value,
            "subclones": ";".join(sorted(candidate.subclones)),
            "class_i_alleles": ";".join(sorted(candidate.class_i_alleles)),
            "class_ii_alleles": ";".join(sorted(candidate.class_ii_alleles)),
            "expression": candidate.expression,
            "clonality": candidate.clonality,
            "truncality": candidate.truncality,
            "mhc_i_presentation": candidate.mhc_i_presentation,
            "mhc_ii_presentation": candidate.mhc_ii_presentation,
            "normal_proteome_safety": candidate.normal_proteome_safety,
            "presentation_retention": candidate.presentation_retention,
            "escape_risk": candidate.escape_risk,
            "manufacturability": candidate.manufacturability,
            "scenario_scores_json": "{}",
            "worst_scenario": "excluded:" + ";".join(exclusion.reasons),
            "role": "research_hypothesis_not_vaccine_sequence",
        })
    designs = []
    for ranking in result.rankings:
        designs.append({
            "rank": ranking.rank,
            "candidate_ids": ";".join(ranking.candidate_ids),
            "antigen_count": len(ranking.candidate_ids),
            "robust_score": ranking.robust_score,
            "worst_case_score": ranking.worst_case_score,
            "weighted_mean_score": ranking.weighted_mean_score,
            "worst_scenario": ranking.worst_scenario,
            "covered_subclones": ";".join(sorted(ranking.covered_subclones)),
            "covered_class_i_alleles": ";".join(sorted(ranking.covered_class_i_alleles)),
            "covered_class_ii_alleles": ";".join(sorted(ranking.covered_class_ii_alleles)),
            "scenario_scores_json": json.dumps(ranking.scenario_scores, sort_keys=True),
            "first_order_scores_json": json.dumps(
                ranking.first_order_score_by_scenario, sort_keys=True),
            "interaction_scores_json": json.dumps(
                ranking.interaction_score_by_scenario, sort_keys=True),
            "claim_scope": result.claim_scope,
        })
    return pd.DataFrame(candidate_rows), pd.DataFrame(designs)


def _schedule_options() -> dict[str, tuple[tuple[int, ...], tuple[float, ...]]]:
    return {
        "post_chemo_q3w_x3": ((91, 112, 133), (1.0, 1.0, 1.0)),
        "interleaved_q3w_x5": ((28, 49, 70, 91, 112), (.65, .65, .65, .85, .85)),
        "delayed_prime_boost": ((105, 119, 133, 161, 189), (1.0, .9, .9, .75, .75)),
    }


SCHEDULE_EVIDENCE = {
    "post_chemo_q3w_x3": {
        "analog_source": "COTC026 post-carboplatin q3-week vaccine timing",
        "analog_source_record": "PMID39955616",
        "analog_source_url": "https://pubmed.ncbi.nlm.nih.gov/39955616/",
        "analog_secondary_source_url": "none",
        "evidence_support": "non_RNA_historical_control_timing_analog_only",
    },
    "interleaved_q3w_x5": {
        "analog_source": "no osteosarcoma RNA policy dataset",
        "analog_source_record": "none",
        "analog_source_url": "none",
        "analog_secondary_source_url": "none",
        "evidence_support": "mechanistic_extrapolation_only",
    },
    "delayed_prime_boost": {
        "analog_source": "COTC026 timing plus RNA-PRIME protocol structure only",
        "analog_source_record": "PMID39955616+NCT05660408",
        "analog_source_url": "https://pubmed.ncbi.nlm.nih.gov/39955616/",
        "analog_secondary_source_url": "https://clinicaltrials.gov/study/NCT05660408",
        "evidence_support": "cross_platform_timing_analog_only",
    },
}


def _anchor_dog_clock(model: OsteosarcomaVolterraHSMM) -> OsteosarcomaVolterraHSMM:
    """Set an aggregate COTC022-informed dog dwell-time prior.

    Stretching the reference dog Weibull scales by 1.29 gives an approximately
    180-day median time to first modeled visible relapse under the bundled SOC
    proxy. This is a coarse aggregate anchor, not a patient-level likelihood
    fit or a validation of the transition structure.
    """
    dog = model.species_parameters[HSMMSpecies.DOG]
    base_scales = np.array([6.0, 3.0, 7.0, 5.0, 2.2, 5.0])
    shapes = np.array([1.4, 2.0, 1.5, 1.9, 1.3, 1.7])
    hazards = np.stack([
        discrete_weibull_hazards(scale * 1.29, shape, 24)
        for scale, shape in zip(base_scales, shapes, strict=True)
    ])
    initial = np.array(dog.initial_probabilities, copy=True)
    visible = list(model.states).index(OsteosarcomaState.VISIBLE_RELAPSE)
    occult = list(model.states).index(OsteosarcomaState.OCCULT_ESCAPE)
    initial[occult] += initial[visible]
    initial[visible] = 0.0
    anchored_dog = replace(
        dog,
        duration_hazards=hazards,
        initial_probabilities=initial,
    )
    return OsteosarcomaVolterraHSMM(
        model.kernels, [anchored_dog, model.species_parameters[HSMMSpecies.HUMAN]])


def _cargo_response_proxy(
    ranking: CargoRanking,
    by_id: dict[str, AntigenCandidate],
    specification: DesignSpecification,
    scenario: SpeciesScenario,
) -> dict[str, float | str]:
    """Compress a robust cargo into an auditable HSMM input proxy.

    This remains a two-stage research surrogate. Safety, source diversity, and
    manufacturability are hard cargo gates; they are not treated as immune
    potency. The dynamic proxy combines clone/allele breadth, tumor visibility,
    retained presentation, and the cargo model's low-rank interaction term.
    """
    cargo = [by_id[candidate_id] for candidate_id in ranking.candidate_ids]
    constraints = specification.constraints
    active = [
        candidate for candidate in cargo
        if candidate.candidate_id not in scenario.escaped_antigens
        and scenario.candidate_effect_scale.get(candidate.candidate_id, 1.0) > 0
    ]
    clones = set().union(*(candidate.subclones for candidate in active))
    nominal_clones = set().union(*(candidate.subclones for candidate in cargo))
    class_i = set().union(*(
        candidate.class_i_alleles - scenario.lost_class_i_alleles
        for candidate in active
    ))
    class_ii = set().union(*(
        candidate.class_ii_alleles - scenario.lost_class_ii_alleles
        for candidate in active
    ))
    nominal_i = set().union(*(candidate.class_i_alleles for candidate in cargo))
    nominal_ii = set().union(*(candidate.class_ii_alleles for candidate in cargo))

    required_clones = constraints.required_subclones or nominal_clones
    required_i = constraints.required_class_i_alleles or nominal_i
    required_ii = constraints.required_class_ii_alleles or nominal_ii
    clone_fraction = len(clones & set(required_clones)) / max(1, len(required_clones))
    class_i_fraction = len(class_i & set(required_i)) / max(1, len(required_i))
    class_ii_fraction = len(class_ii & set(required_ii)) / max(1, len(required_ii))
    allele_fraction = .5 * (class_i_fraction + class_ii_fraction)
    tumor_visibility = float(np.mean([
        min(1.0, candidate.expression * scenario.expression_scale)
        * candidate.clonality
        * candidate.truncality
        * (0.0 if candidate.candidate_id in scenario.escaped_antigens else
           scenario.candidate_effect_scale.get(candidate.candidate_id, 1.0))
        for candidate in cargo
    ]))
    retained_presentation = float(np.mean([
        max(
            min(
                1.0,
                candidate.mhc_i_presentation * scenario.presentation_scale
                * (len(candidate.class_i_alleles - scenario.lost_class_i_alleles)
                   / max(1, len(candidate.class_i_alleles))),
            ),
            min(
                1.0,
                candidate.mhc_ii_presentation * scenario.presentation_scale
                * (len(candidate.class_ii_alleles - scenario.lost_class_ii_alleles)
                   / max(1, len(candidate.class_ii_alleles))),
            ),
        )
        * min(1.0, candidate.presentation_retention * scenario.retention_scale)
        * (1 - min(1.0, candidate.escape_risk * scenario.escape_scale))
        * (0.0 if candidate.candidate_id in scenario.escaped_antigens else
           scenario.candidate_effect_scale.get(candidate.candidate_id, 1.0))
        for candidate in cargo
    ]))
    interaction_per_antigen = (
        ranking.interaction_score_by_scenario[scenario.name] / len(cargo)
    )
    interaction_modifier = float(np.clip(.5 + interaction_per_antigen, 0, 1))
    effective = float(np.clip(
        RESPONSE_PROXY_WEIGHTS["clone_coverage"] * clone_fraction
        + RESPONSE_PROXY_WEIGHTS["allele_coverage"] * allele_fraction
        + RESPONSE_PROXY_WEIGHTS["tumor_visibility"] * tumor_visibility
        + RESPONSE_PROXY_WEIGHTS["retained_presentation"] * retained_presentation
        + RESPONSE_PROXY_WEIGHTS["interaction_modifier"] * interaction_modifier,
        .05,
        1.0,
    ))
    return {
        "scenario": scenario.name,
        "effective_antigen_coverage_proxy": effective,
        "required_clone_coverage_fraction": float(clone_fraction),
        "required_allele_coverage_fraction": float(allele_fraction),
        "mean_tumor_visibility": tumor_visibility,
        "mean_retained_presentation": retained_presentation,
        "low_rank_interaction_modifier": interaction_modifier,
    }


def _model_inputs(model: OsteosarcomaVolterraHSMM, schedule_days: tuple[int, ...],
                  relative_doses: tuple[float, ...], antigen_coverage: float,
                  horizon: int = MODEL_HORIZON_STEPS) -> np.ndarray:
    inputs = np.zeros((horizon, len(model.input_names)))
    index = {name: position for position, name in enumerate(model.input_names)}
    # Four normalized carboplatin pulses after amputation are a canine SOC
    # timing proxy, not reconstructed veterinary doses.
    for day in (7, 28, 49, 70):
        step = day // MODEL_STEP_DAYS
        inputs[step, index["chemotherapy"]] = .8
        inputs[step:min(step + 2, horizon), index["immune_suppression"]] = .28
    for day, dose in zip(schedule_days, relative_doses, strict=True):
        step = int(round(day / MODEL_STEP_DAYS))
        if step >= horizon:
            raise ValueError("candidate vaccine day lies beyond the model horizon")
        inputs[step, index["antigen_coverage"]] = antigen_coverage
        inputs[step, index["rna_dose"]] = dose
    return inputs


def _policy_metrics(
    model: OsteosarcomaVolterraHSMM, inputs: np.ndarray,
) -> tuple[dict[str, float | str], pd.DataFrame, np.ndarray]:
    """Propagate the finite HSMM exactly while tracking first visible relapse.

    The extra binary axis records whether visible relapse has ever occurred, so
    favorable post-relapse states cannot improve the disease-free objective.
    """
    parameters = model.species_parameters[HSMMSpecies.DOG]
    time_points = len(inputs)
    visible = list(model.states).index(OsteosarcomaState.VISIBLE_RELAPSE)
    adaptive = list(model.states).index(OsteosarcomaState.ADAPTIVE_CONTROL)
    exhausted = list(model.states).index(OsteosarcomaState.EXHAUSTED)
    ned = list(model.states).index(OsteosarcomaState.NED_MRD)

    distribution = np.zeros((2, N_STATES, parameters.max_duration), dtype=float)
    for state, probability in enumerate(parameters.initial_probabilities):
        distribution[int(state == visible), state, 0] = probability
    state_probability = np.zeros((time_points, N_STATES), dtype=float)
    pre_relapse_probability = np.zeros_like(state_probability)
    relapse_cdf = np.zeros(time_points, dtype=float)

    for time_index in range(time_points):
        state_probability[time_index] = distribution.sum(axis=(0, 2))
        pre_relapse_probability[time_index] = distribution[0].sum(axis=1)
        relapse_cdf[time_index] = distribution[1].sum()
        if time_index == time_points - 1:
            break
        destinations = model.transition_probabilities(
            inputs, time_index, HSMMSpecies.DOG)
        updated = np.zeros_like(distribution)
        for relapsed in range(2):
            for source in range(N_STATES):
                for age in range(parameters.max_duration):
                    mass = distribution[relapsed, source, age]
                    if mass == 0:
                        continue
                    hazard = parameters.duration_hazards[source, age]
                    if age + 1 < parameters.max_duration:
                        updated[relapsed, source, age + 1] += mass * (1 - hazard)
                    if hazard > 0:
                        for destination, probability in enumerate(destinations[source]):
                            if probability > 0:
                                ever_relapsed = int(bool(relapsed or destination == visible))
                                updated[ever_relapsed, destination, 0] += (
                                    mass * hazard * probability
                                )
        total = updated.sum()
        if not np.isclose(total, 1.0, atol=1e-10, rtol=0):
            raise FloatingPointError(f"latent probability mass drifted to {total}")
        distribution = updated / total

    metrics = {
        "exact_prior_ever_visible_relapse_probability": float(relapse_cdf[-1]),
        "exact_prior_terminal_adaptive_control_without_prior_relapse_probability": float(
            pre_relapse_probability[-1, adaptive]),
        "exact_prior_terminal_ned_mrd_without_prior_relapse_probability": float(
            pre_relapse_probability[-1, ned]),
        "exact_prior_terminal_exhausted_without_prior_relapse_probability": float(
            pre_relapse_probability[-1, exhausted]),
        "exact_prior_pre_relapse_adaptive_control_occupancy": float(
            pre_relapse_probability[:, adaptive].mean()),
        "policy_probability_computation": "exact_augmented_state_propagation",
    }
    metrics["prior_objective"] = float(
        POLICY_OBJECTIVE_WEIGHTS["pre_relapse_adaptive_control_occupancy"]
        * metrics["exact_prior_pre_relapse_adaptive_control_occupancy"]
        + POLICY_OBJECTIVE_WEIGHTS["terminal_ned_without_prior_relapse"]
        * metrics["exact_prior_terminal_ned_mrd_without_prior_relapse_probability"]
        + POLICY_OBJECTIVE_WEIGHTS["ever_visible_relapse"]
        * metrics["exact_prior_ever_visible_relapse_probability"]
        + POLICY_OBJECTIVE_WEIGHTS["terminal_exhausted_without_prior_relapse"]
        * metrics[
            "exact_prior_terminal_exhausted_without_prior_relapse_probability"]
        + POLICY_OBJECTIVE_WEIGHTS["normalized_rna_input"]
        * inputs[:, model.input_names.index("rna_dose")].sum()
    )
    rows = []
    for step, probabilities in enumerate(state_probability):
        for state, probability in zip(model.states, probabilities, strict=True):
            rows.append({"day": step * MODEL_STEP_DAYS, "state": state.value,
                         "probability": float(probability)})
    return metrics, pd.DataFrame(rows), relapse_cdf


def _joint_inverse_search(
    model: OsteosarcomaVolterraHSMM,
    design: CargoDesignResult,
    candidates: list[AntigenCandidate],
    specification: DesignSpecification,
) -> tuple[pd.DataFrame, pd.DataFrame, dict, np.ndarray]:
    by_id = {candidate.candidate_id: candidate for candidate in candidates}
    rows = []
    scenario_rows = []
    schedules = _schedule_options()
    candidate_inputs: dict[tuple[int, str], np.ndarray] = {}
    nominal_scenario = next(
        scenario for scenario in specification.scenarios
        if scenario.name.lower() == "nominal"
    )
    for cargo in design.rankings[:JOINT_CARGO_LIMIT]:
        for schedule_name, (days, doses) in schedules.items():
            evaluated = []
            for scenario in specification.scenarios:
                response_proxy = _cargo_response_proxy(
                    cargo, by_id, specification, scenario)
                inputs = _model_inputs(
                    model, days, doses,
                    float(response_proxy["effective_antigen_coverage_proxy"]),
                )
                metrics, _, _ = _policy_metrics(model, inputs)
                evaluated.append((scenario, response_proxy, inputs, metrics))
                scenario_rows.append({
                    "cargo_rank": cargo.rank,
                    "schedule": schedule_name,
                    "candidate_ids": ";".join(cargo.candidate_ids),
                    **response_proxy,
                    "scenario_weight": scenario.weight,
                    "vaccine_days": ";".join(map(str, days)),
                    "relative_doses": ";".join(map(str, doses)),
                    "dose_units": "normalized_model_input",
                    "dose_evidence": "none_not_a_clinical_dose",
                    **metrics,
                })
            nominal = next(item for item in evaluated if item[0] is nominal_scenario)
            candidate_inputs[(cargo.rank, schedule_name)] = nominal[2]
            objectives = np.asarray([item[3]["prior_objective"] for item in evaluated])
            scenario_weights = np.asarray([item[0].weight for item in evaluated])
            worst_index = int(np.argmin(objectives))
            worst = float(objectives[worst_index])
            weighted_mean = float(np.average(objectives, weights=scenario_weights))
            robust = float(
                (1 - DEFAULT_DESIGN_WEIGHTS.robust_mean_weight) * worst
                + DEFAULT_DESIGN_WEIGHTS.robust_mean_weight * weighted_mean
            )
            relapse_values = np.asarray([
                item[3]["exact_prior_ever_visible_relapse_probability"]
                for item in evaluated
            ])
            nominal_proxy = {
                f"nominal_{name}": value
                for name, value in nominal[1].items()
                if name != "scenario"
            }
            nominal_metrics = {
                f"nominal_{name}": value for name, value in nominal[3].items()
            }
            rows.append({
                "cargo_rank": cargo.rank,
                "schedule": schedule_name,
                "candidate_ids": ";".join(cargo.candidate_ids),
                **nominal_proxy,
                "vaccine_days": ";".join(map(str, days)),
                "relative_doses": ";".join(map(str, doses)),
                "dose_units": "normalized_model_input",
                "dose_evidence": "none_not_a_clinical_dose",
                **SCHEDULE_EVIDENCE[schedule_name],
                "rna_policy_observed": False,
                "schedule_extrapolation": True,
                "worst_scenario": evaluated[worst_index][0].name,
                "worst_case_prior_objective": worst,
                "weighted_mean_prior_objective": weighted_mean,
                "prior_objective": robust,
                "worst_case_exact_prior_ever_visible_relapse_probability": float(
                    relapse_values.max()),
                "weighted_mean_exact_prior_ever_visible_relapse_probability": float(
                    np.average(relapse_values, weights=scenario_weights)),
                **nominal_metrics,
                "role": "prior_driven_research_hypothesis_not_recommendation",
            })
    table = pd.DataFrame(rows).sort_values(
        ["prior_objective", "cargo_rank", "schedule"], ascending=[False, True, True])
    table.insert(0, "joint_rank", np.arange(1, len(table) + 1))
    best_objective = float(table.iloc[0].prior_objective)
    table["objective_gap_from_best"] = best_objective - table.prior_objective
    table["within_prior_equivalence_tolerance"] = (
        table.objective_gap_from_best <= PRIOR_EQUIVALENCE_TOLERANCE)
    winner = table.iloc[0]
    key = (int(winner.cargo_rank), str(winner.schedule))
    selected_inputs = candidate_inputs[key]
    runner_up_gap = (
        None if len(table) < 2
        else float(winner.prior_objective - table.iloc[1].prior_objective)
    )
    equivalent = table.loc[table.within_prior_equivalence_tolerance]
    selected = {
        "cargo_rank": int(winner.cargo_rank),
        "candidate_ids": str(winner.candidate_ids).split(";"),
        "schedule": str(winner.schedule),
        "vaccine_days": [int(value) for value in str(winner.vaccine_days).split(";")],
        "relative_doses": [float(value) for value in str(winner.relative_doses).split(";")],
        "nominal_effective_antigen_coverage_proxy": float(
            winner.nominal_effective_antigen_coverage_proxy),
        "schedule_evidence_support": str(winner.evidence_support),
        "schedule_analog_source": str(winner.analog_source),
        "schedule_analog_source_record": str(winner.analog_source_record),
        "schedule_analog_source_url": str(winner.analog_source_url),
        "schedule_analog_secondary_source_url": str(
            winner.analog_secondary_source_url
        ),
        "dose_units": "normalized_model_input",
        "dose_evidence": "none_not_a_clinical_dose",
        "schedule_extrapolation": True,
        "robust_prior_objective": float(winner.prior_objective),
        "worst_scenario": str(winner.worst_scenario),
        "worst_case_prior_objective": float(winner.worst_case_prior_objective),
        "worst_case_exact_prior_ever_visible_relapse_probability": float(
            winner.worst_case_exact_prior_ever_visible_relapse_probability),
        "prior_equivalence_tolerance": PRIOR_EQUIVALENCE_TOLERANCE,
        "objective_gap_to_runner_up": runner_up_gap,
        "near_equivalent_joint_ranks": [int(value) for value in equivalent.joint_rank],
        "selection_resolution": (
            "NEAR_EQUIVALENT_FIXED_PRIOR_SET"
            if len(equivalent) > 1 else "UNIQUE_WITHIN_FIXED_PRIOR_TOLERANCE"
        ),
        "clinical_use": False,
    }
    return table, pd.DataFrame(scenario_rows), selected, selected_inputs


def _fixed_prior_soc_comparison(selected: dict, comparator_metrics: dict) -> dict[str, object]:
    """Compare worst specified candidate behavior with SOC under the fixed prior."""
    objective_advantage = float(
        selected["worst_case_prior_objective"] - comparator_metrics["prior_objective"]
    )
    relapse_reduction = float(
        comparator_metrics["exact_prior_ever_visible_relapse_probability"]
        - selected["worst_case_exact_prior_ever_visible_relapse_probability"]
    )
    favors_candidate = (
        objective_advantage > PRIOR_EQUIVALENCE_TOLERANCE
        and relapse_reduction > PRIOR_EQUIVALENCE_TOLERANCE
    )
    return {
        "worst_case_objective_advantage_vs_soc": objective_advantage,
        "worst_case_relapse_probability_reduction_vs_soc": relapse_reduction,
        "equivalence_tolerance": PRIOR_EQUIVALENCE_TOLERANCE,
        "favors_candidate": bool(favors_candidate),
    }


def _ablation_models(model: OsteosarcomaVolterraHSMM) -> dict[str, OsteosarcomaVolterraHSMM]:
    kernels = model.kernels
    first_only = replace(kernels, second_left=np.zeros_like(kernels.second_left),
                         second_right=np.zeros_like(kernels.second_right))
    none = replace(first_only, first_order=np.zeros_like(kernels.first_order))
    geometric_parameters = []
    for parameters in model.species_parameters.values():
        hazards = np.empty_like(parameters.duration_hazards)
        for state in range(N_STATES):
            original = parameters.duration_hazards[state]
            survival = np.concatenate(([1.0], np.cumprod(1 - original[:-1])))
            target_mean = float(survival.sum())
            low, high = 1e-9, 1 - 1e-9
            for _ in range(80):
                constant = (low + high) / 2
                geometric_mean = float(
                    np.sum((1 - constant) ** np.arange(len(original))))
                if geometric_mean > target_mean:
                    low = constant
                else:
                    high = constant
            constant = (low + high) / 2
            hazards[state, :-1] = constant
            hazards[state, -1] = 1.0
        geometric_parameters.append(replace(parameters, duration_hazards=hazards))
    return {
        "full_second_order_volterra_hsmm": model,
        "first_order_volterra_hsmm": OsteosarcomaVolterraHSMM(
            first_only, model.species_parameters),
        "hsmm_no_volterra": OsteosarcomaVolterraHSMM(none, model.species_parameters),
        "mean_matched_truncated_geometric_hmm_second_order": OsteosarcomaVolterraHSMM(
            kernels, geometric_parameters),
    }


def _synthetic_self_consistency(model: OsteosarcomaVolterraHSMM, inputs: np.ndarray,
                                sequences: int, seed: int) -> pd.DataFrame:
    """Compare ablations only on model-generated data; never call this clinical validation."""
    simulated = [model.simulate(inputs, HSMMSpecies.DOG, seed + index)
                 for index in range(sequences)]
    rows = []
    for name, challenger in _ablation_models(model).items():
        log_likelihoods = []; accuracies = []
        for sequence in simulated:
            filtered = challenger.filter(sequence.observations, inputs, HSMMSpecies.DOG)
            decoded = challenger.most_likely_path(
                sequence.observations, inputs, HSMMSpecies.DOG)
            log_likelihoods.append(filtered.log_likelihood / len(inputs))
            accuracies.append(np.mean(decoded.state_indices == sequence.state_indices))
        rows.append({
            "model": name,
            "mean_log_likelihood_per_step": float(np.mean(log_likelihoods)),
            "mean_latent_path_accuracy": float(np.mean(accuracies)),
            "evaluation_data": "synthetic_from_reference_model",
            "clinical_validation": False,
        })
    return pd.DataFrame(rows).sort_values("mean_log_likelihood_per_step", ascending=False)


def _identifiability_audit(real_data_available: bool) -> pd.DataFrame:
    rows = [
        ("static prognostic sensitivity", "GSE76127 pretreatment tumor + DFI",
         "TESTABLE" if real_data_available else "MISSING_LOCAL_FILE",
         "Not an HSMM-emission validation; one sample per dog and no immune dynamics."),
        ("canine disease-state clock", "COTC021/022 serial surveillance",
         "PARTIAL_EXTERNAL_DATA", "Aggregate anchors bundled; individual event histories external."),
        ("cargo feature model", "paired tumor/normal WES + RNA + DLA typing",
         "PATIENT_DATA_REQUIRED", "Illustrative panel is software data, not discovered antigens."),
        ("first-order vaccine memory", "five-dog RNA-LPA abstract",
         "NOT_IDENTIFIABLE", "No public individual serial measurements."),
        ("second-order interaction", "RNA vaccine x chemotherapy/checkpoint variation",
         "NOT_IDENTIFIABLE", "No randomized schedule or factorial intervention support."),
        ("clinical policy effect", "SOC versus SOC + RNA vaccine",
         "NOT_IDENTIFIABLE", "No completed randomized canine or human RNA-vaccine comparison."),
    ]
    return pd.DataFrame(rows, columns=["component", "best_available_source", "status", "reason"])


def _clinical_interpretation(summary: dict) -> str:
    real = summary["real_data_evaluation"]
    if real.get("status") == "evaluated":
        improved = (
            real["expression_log_dfi_mae"] < real["training_median_log_dfi_mae"]
            and (real.get("expression_dfi_spearman") or 0.0) > 0
        )
        result_sentence = (
            "It passes the current directional checks, but the small cohort still cannot "
            "establish a generalizable survival model."
            if improved else
            "It failed the current explicit checks of lower MAE and positive rank correlation, "
            "so this specific PCA/ridge prognostic pipeline did not generalize in this cohort."
        )
        static_message = (
            f"The fold-local GSE76127 expression sensitivity analysis had log-DFI MAE "
            f"{real['expression_log_dfi_mae']:.3f}, versus "
            f"{real['training_median_log_dfi_mae']:.3f} for a training-median baseline, and "
            f"Spearman correlation {real['expression_dfi_spearman']:.3f}. "
            + result_sentence
            + " Censoring status is unavailable, chemotherapy is heterogeneous, and the public "
            "GEO matrix was cohort-wide preprocessed upstream; this is not a survival or HSMM-"
            "emission validation."
        )
    else:
        static_message = "The optional GSE76127 real-data prognostic sensitivity test was not run."
    selected = summary["selected_research_hypothesis"]
    cargo_description = (
        "an illustrative"
        if summary["candidate_origin"] == "illustrative_synthetic_feature_panel"
        else "a feature-ranked research"
    )
    identifier_warning = (
        "The candidate identifiers are synthetic placeholders."
        if summary["candidate_origin"] == "illustrative_synthetic_feature_panel"
        else "The candidate identifiers come from the supplied deidentified feature table."
    )
    equivalent_count = len(selected["near_equivalent_joint_ranks"])
    resolution_message = (
        f"It is one of {equivalent_count} cargo/timing designs within the prespecified "
        f"fixed-prior tolerance of {selected['prior_equivalence_tolerance']:.3g}; the "
        "reported rank is a deterministic tie-break, not evidence that this cargo is better."
        if equivalent_count > 1 else
        "It is the only evaluated design inside the prespecified fixed-prior equivalence "
        "tolerance."
    )
    interaction = summary["cargo_interaction_model"]
    interaction_message = (
        f"The cargo scorer included low-rank pair effects "
        f"(synergy rank {interaction['synergy_rank']}, competition rank "
        f"{interaction['competition_rank']})."
        if interaction["interaction_enabled"] else
        "Cargo-level pair effects were disabled because the supplied candidate table had "
        "rank-zero interaction loadings."
    )
    candidate_prior = summary["robust_fixed_prior_candidate_metrics"]
    soc_prior = summary["fixed_prior_soc_proxy_metrics"]
    candidate_relapse = 100 * candidate_prior[
        "worst_case_exact_prior_ever_visible_relapse_probability"]
    soc_relapse = 100 * soc_prior["exact_prior_ever_visible_relapse_probability"]
    comparators = summary["current_care_reference_anchors"]
    dog = comparators["canine_localized_standard_care"]
    human = comparators["human_localized_current_care"]
    return f"""# Clinical interpretation

## What the output says

The software produced {cargo_description} {len(selected['candidate_ids'])}-antigen canine cargo and
selected the `{selected['schedule']}` timing pattern under the bundled research priors.
{identifier_warning} They are not validated peptides, manufacturing-ready nucleotide
sequences, veterinary doses, or a treatment recommendation.
{resolution_message} {interaction_message}

{static_message}

Under the fixed illustrative prior, the model's worst specified cargo scenario assigns visible
relapse by the end of the modeled horizon to {candidate_relapse:.1f}% for the research hypothesis,
versus {soc_relapse:.1f}% for the standard-care proxy. These are model probabilities, not expected
clinical response rates. The real
canine comparator is {dog['median_dfi']['estimate']:.0f}-day median DFI and
{dog['median_os']['estimate']:.0f}-day median OS after amputation plus carboplatin. The separate
human EURAMOS landmark target is {human['five_year_efs']['estimate']:.0f}% five-year EFS and
{human['five_year_os']['estimate']:.0f}% five-year OS among M0 patients reaching complete surgical
remission; dog and human endpoints are not numerically interchangeable.

The Volterra-HSMM policy probabilities are propagated exactly under one fixed illustrative prior;
they are not estimated with noisy policy Monte Carlo. The disease-free objective stops rewarding
immune-control states after the first modeled visible relapse. This improves mathematical
consistency, but a favorable fixed-prior difference is still not evidence that a vaccine works.
The software's conservative fixed-prior comparison gate is
**{'favorable' if summary['fixed_prior_favors_candidate'] else 'not favorable'}** for the research
hypothesis; that gate tests the bundled assumptions, not outcomes in treated patients.

The cargo and timing layers are joined by an explicit two-stage response proxy, not a fitted
end-to-end biological model. Each exact schedule is an analog or mechanistic extrapolation; no
osteosarcoma RNA dataset has observed these policy choices.

## What it does not say

It does not show that an RNA vaccine is better than amputation plus carboplatin in dogs or surgery
plus MAP chemotherapy in humans. Public osteosarcoma RNA-vaccine data do not identify first- or
second-order treatment kernels, and there is no completed randomized RNA-vaccine comparison.
Clinical superiority is therefore reported as **false / not evaluable** regardless of the
fixed-prior result.

## The next decisive experiment

Provide paired tumor/normal sequencing, tumor RNA, DLA typing, and validated presentation data for
each dog; lock the upstream candidate pipeline; then randomize standard care versus standard care
plus the model-ranked multivalent RNA vaccine. Collect serial cytokines, CBC, TCR sequencing,
ctDNA, thoracic imaging, toxicity, DFI, and survival on a prespecified schedule. Only that design can
test whether the inferred hidden states and Volterra timing interaction improve outcomes.
"""


def _volterra_plot_arrays(model: OsteosarcomaVolterraHSMM) -> tuple[np.ndarray, np.ndarray]:
    innate = list(model.states).index(OsteosarcomaState.INNATE_PRIMED)
    adaptive = list(model.states).index(OsteosarcomaState.ADAPTIVE_CONTROL)
    first = model.kernels.first_order[innate, adaptive].T
    antigen = model.input_names.index("antigen_coverage")
    dose = model.input_names.index("rna_dose")
    left = model.kernels.second_left[innate, adaptive, :, :, antigen]
    right = model.kernels.second_right[innate, adaptive, :, :, dose]
    surface = np.einsum("rl,rm->lm", left, right)
    return first, surface


def _first_passage_median_days(cumulative_probability: np.ndarray) -> int | None:
    reached = np.flatnonzero(np.asarray(cumulative_probability) >= .5)
    return None if not len(reached) else int(reached[0] * MODEL_STEP_DAYS)


def _clinical_comparators(clinical: pd.DataFrame) -> dict[str, object]:
    indexed = clinical.set_index("record_id")

    def endpoint(record_id: str) -> dict[str, object]:
        row = indexed.loc[record_id]
        numeric_n = pd.to_numeric(pd.Series([row.n]), errors="coerce").iloc[0]
        return {
            "endpoint": str(row.endpoint),
            "estimate": float(row.estimate),
            "unit": str(row.unit),
            "ci_low": None if pd.isna(row.ci_low) else float(row.ci_low),
            "ci_high": None if pd.isna(row.ci_high) else float(row.ci_high),
            "n": None if pd.isna(numeric_n) else int(numeric_n),
            "arm": str(row.arm),
            "design": str(row.design),
            "evidence_tier": str(row.evidence_tier),
            "data_granularity": str(row.data_granularity),
            "study_status": str(row.study_status),
            "intervention_class": str(row.intervention_class),
            "comparability_caveat": str(row.comparability_caveat),
            "source_url": str(row.source_url),
        }

    return {
        "canine_localized_standard_care": {
            "setting": "post-amputation nonmetastatic appendicular osteosarcoma",
            "time_origin": "amputation",
            "regimen": "amputation plus four carboplatin cycles (COTC022)",
            "median_dfi": endpoint("cotc022_soc_median_dfi"),
            "median_os": endpoint("cotc022_soc_median_os"),
        },
        "human_localized_current_care": {
            "setting": "M0 complete surgical remission landmark cohort",
            "time_origin": "complete surgery after induction therapy",
            "regimen": "MAP induction, surgery, and protocol-defined postoperative therapy",
            "five_year_efs": endpoint("euramos_m0_csr_5y_efs"),
            "five_year_os": endpoint("euramos_m0_csr_5y_os"),
        },
        "cross_species_numeric_comparison_valid": False,
    }


def _model_sha256(model: OsteosarcomaVolterraHSMM) -> str:
    digest = hashlib.sha256()
    digest.update(json.dumps({
        "input_names": model.input_names,
        "observation_names": model.observation_names,
        "states": [state.value for state in model.states],
        "logit_bound": model.kernels.logit_bound,
    }, sort_keys=True).encode())
    for array in (
        model.kernels.first_order,
        model.kernels.second_left,
        model.kernels.second_right,
        model.kernels.input_scale,
    ):
        digest.update(np.ascontiguousarray(array).tobytes())
    for species in HSMMSpecies:
        parameters = model.species_parameters[species]
        for array in (
            parameters.initial_probabilities,
            parameters.base_transition_logits,
            parameters.duration_hazards,
            parameters.emission_means,
            parameters.emission_sds,
        ):
            digest.update(np.ascontiguousarray(array).tobytes())
    return digest.hexdigest()


def _runtime_manifest() -> dict[str, object]:
    packages = {}
    for package in ("canine-genome-dsp", "numpy", "pandas", "scipy",
                    "scikit-learn", "matplotlib"):
        try:
            packages[package] = metadata.version(package)
        except metadata.PackageNotFoundError:
            packages[package] = "source_tree_or_unavailable"
    code_files = [
        Path(__file__),
        Path(__file__).with_name("osteosarcoma_design.py"),
        Path(__file__).with_name("osteosarcoma_hsmm.py"),
        Path(__file__).with_name("osteosarcoma_data.py"),
        Path(__file__).with_name("osteosarcoma_spec.py"),
        Path(__file__).with_name("osteosarcoma_viz.py"),
    ]
    return {
        "python": platform.python_version(),
        "packages": packages,
        "code_file_sha256": {path.name: _sha256(path) for path in code_files},
    }


def _artifact_inventory(root: Path, manifest_path: Path) -> dict[str, dict[str, object]]:
    """Hash every published file except the self-referential manifest."""
    inventory = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path == manifest_path:
            continue
        inventory[path.relative_to(root).as_posix()] = {
            "sha256": _sha256(path),
            "bytes": path.stat().st_size,
        }
    return inventory


def _is_owned_result_directory(path: Path) -> bool:
    """Recognize only outputs created by this benchmark."""
    try:
        manifest = json.loads((path / "run_manifest.json").read_text())
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        manifest = {}
    if manifest.get("program") == PROGRAM_ID:
        return True
    # Backward compatibility for successful outputs written before the manifest
    # acquired an explicit program marker.
    try:
        summary = json.loads((path / "summary.json").read_text())
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return False
    return summary.get("program") == PROGRAM_ID


def _validate_publish_target(path: Path) -> None:
    if path.is_symlink():
        raise ValueError("output directory cannot be a symbolic link")
    if not path.exists():
        return
    if not path.is_dir():
        raise FileExistsError(f"output path exists and is not a directory: {path}")
    if any(path.iterdir()) and not _is_owned_result_directory(path):
        raise FileExistsError(
            "refusing to replace a nonempty directory not owned by the osteosarcoma benchmark: "
            f"{path}"
        )


def _path_is_within(path: Path, directory: Path) -> bool:
    try:
        path.relative_to(directory)
    except ValueError:
        return False
    return True


def _validate_safe_output_scope(path: Path) -> None:
    """Reject broad targets that must never participate in a directory swap."""
    resolved = path.resolve(strict=False)
    current_working_directory = Path.cwd().resolve()
    home = Path.home().resolve()
    if resolved == resolved.parent:
        raise ValueError("output directory cannot be a filesystem root")
    if resolved == home:
        raise ValueError("output directory cannot be the user home directory")
    if _path_is_within(current_working_directory, resolved):
        raise ValueError(
            "output directory cannot be the current workspace or one of its ancestors"
        )
    if resolved.exists() and (resolved / ".git").exists():
        raise ValueError("output directory cannot be an existing Git repository root")


def _validate_inputs_outside_output(out: Path, **inputs: str | Path | None) -> None:
    output = out.resolve(strict=False)
    conflicts = []
    for name, value in inputs.items():
        if value is None:
            continue
        candidate = Path(value).expanduser().resolve(strict=False)
        if _path_is_within(candidate, output):
            conflicts.append(name)
    if conflicts:
        raise ValueError(
            "input paths cannot be located inside the output directory: "
            f"{sorted(conflicts)}"
        )


def _publish_staging_directory(staging: Path, destination: Path) -> None:
    """Swap a complete staging tree into place, restoring an old tree on failure."""
    _validate_publish_target(destination)
    if not destination.exists():
        os.replace(staging, destination)
        return
    backup = destination.parent / f".{destination.name}.backup-{uuid.uuid4().hex}"
    os.replace(destination, backup)
    try:
        os.replace(staging, destination)
    except BaseException:
        if not destination.exists() and backup.exists():
            os.replace(backup, destination)
        raise
    shutil.rmtree(backup, ignore_errors=True)


def _run_osteosarcoma_benchmark_staged(
    out: str | Path,
    anchors: str | Path = DEFAULT_ANCHORS,
    candidate_file: str | Path | None = None,
    design_spec_file: str | Path | None = None,
    gse76127_matrix: str | Path | None = None,
    gse76127_supplements: str | Path | None = None,
    draws: int = 192,
    seed: int = 2608,
) -> dict:
    """Build a complete result tree inside a private staging directory."""
    if draws < 16:
        raise ValueError("draws must be at least 16")
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    manifest_path = out / "run_manifest.json"
    manifest_path.write_text(json.dumps({
        "schema_version": 1,
        "program": PROGRAM_ID,
        "status": "INCOMPLETE_FAIL_CLOSED",
        "reason": "run has not reached the completion gate",
    }, indent=2) + "\n")
    anchors = Path(anchors)
    clinical = load_clinical_anchors(anchors)

    if candidate_file:
        if design_spec_file is None:
            raise ValueError(
                "--candidates requires --design-spec so real DLA/HLA and clone constraints "
                "are never replaced by illustrative defaults"
            )
        candidates = load_antigen_candidates(candidate_file)
        candidate_origin = "user_supplied_deidentified_feature_table"
        candidate_hash = _sha256(Path(candidate_file))
    else:
        candidates = illustrative_canine_antigens()
        candidate_origin = "illustrative_synthetic_feature_panel"
        candidate_hash = None
    if design_spec_file:
        specification = load_design_spec(design_spec_file)
        specification_origin = "user_supplied_versioned_design_specification"
        specification_hash = _sha256(Path(design_spec_file))
    else:
        escape_target = _illustrative_escape_target(candidates)
        specification = illustrative_canine_design_spec(escape_target)
        specification_origin = "illustrative_bundled_design_specification"
        specification_hash = None
    design = _cargo_design(candidates, specification)
    candidate_table, cargo_table = _cargo_tables(design, candidates)

    model = _anchor_dog_clock(reference_osteosarcoma_hsmm(memory=8, rank=2))
    joint, joint_scenarios, selected, selected_inputs = _joint_inverse_search(
        model, design, candidates, specification)
    selected_ids = set(selected["candidate_ids"])
    candidate_table["joint_selected"] = candidate_table.candidate_id.isin(selected_ids)
    cargo_table["joint_selected"] = cargo_table["rank"].eq(selected["cargo_rank"])

    clinical.to_csv(out / "clinical_anchors_used.csv", index=False)
    candidate_table.to_csv(out / "candidate_antigen_ranking.csv", index=False)
    cargo_table.to_csv(out / "cargo_design_ranking.csv", index=False)
    joint.to_csv(out / "joint_cargo_schedule_search.csv", index=False)
    joint_scenarios.to_csv(out / "joint_cargo_schedule_scenarios.csv", index=False)
    pd.DataFrame([
        {
            "cargo_rank": ranking.rank,
            "scenario": scenario.name,
            "total_score": ranking.scenario_scores[scenario.name],
            "first_order_score": ranking.first_order_score_by_scenario[scenario.name],
            "low_rank_interaction_score": (
                ranking.interaction_score_by_scenario[scenario.name]),
        }
        for ranking in design.rankings
        for scenario in specification.scenarios
    ]).to_csv(out / "cargo_scenario_contributions.csv", index=False)
    pd.DataFrame([
        {
            "schedule": name,
            "vaccine_days": ";".join(map(str, days)),
            "relative_doses": ";".join(map(str, doses)),
            "dose_units": "normalized_model_input",
            "dose_evidence": "none_not_a_clinical_dose",
            **SCHEDULE_EVIDENCE[name],
            "rna_policy_observed": False,
            "schedule_extrapolation": True,
        }
        for name, (days, doses) in _schedule_options().items()
    ]).to_csv(out / "schedule_hypotheses.csv", index=False)

    real_summary: dict[str, object]
    matrix_path = Path(gse76127_matrix) if gse76127_matrix else None
    supplements_path = Path(gse76127_supplements) if gse76127_supplements else None
    if matrix_path and supplements_path:
        metrics = prepare_gse76127(matrix_path, supplements_path, out / "real_data")
        real_summary = {"status": "evaluated", **metrics,
                        "matrix_sha256": _sha256(matrix_path),
                        "supplements_sha256": _sha256(supplements_path)}
        predictions = pd.read_csv(out / "real_data/gse76127_leave_one_dog_out.csv")
        plot_real_data_predictions(predictions, out / "gse76127_real_data_predictions.png")
    elif matrix_path or supplements_path:
        raise ValueError("both GSE76127 matrix and supplementary archive are required")
    else:
        real_summary = {"status": "not_run", "reason": "optional local files not supplied"}

    pd.DataFrame(selected_inputs, columns=model.input_names).assign(
        day=np.arange(len(selected_inputs)) * MODEL_STEP_DAYS,
        role="normalized_research_input_not_dose",
        dose_units="normalized_model_input",
        dose_evidence="none_not_a_clinical_dose",
        schedule_evidence_support=selected["schedule_evidence_support"],
        schedule_extrapolation=True,
    ).to_csv(out / "selected_normalized_schedule.csv", index=False)

    comparator_inputs = _model_inputs(model, (), (), 0.0)
    candidate_metrics, candidate_states, _ = _policy_metrics(
        model, selected_inputs)
    comparator_metrics, comparator_states, comparator_relapse_cdf = _policy_metrics(
        model, comparator_inputs)
    candidate_states.assign(policy="research_candidate_nominal_scenario").to_csv(
        out / "candidate_state_probabilities.csv", index=False)
    comparator_states.assign(policy="canine_soc_proxy").to_csv(
        out / "soc_state_probabilities.csv", index=False)

    representative = model.simulate(selected_inputs, HSMMSpecies.DOG, seed + 77_000)
    filtered = model.filter(representative.observations, selected_inputs, HSMMSpecies.DOG)
    posterior = pd.DataFrame(filtered.state_posterior,
                             columns=[state.value for state in model.states])
    posterior.insert(0, "day", np.arange(len(posterior)) * MODEL_STEP_DAYS)
    posterior.to_csv(out / "representative_filtered_state_posterior.csv", index=False)

    ablations = _synthetic_self_consistency(
        model, selected_inputs, sequences=max(12, draws // 8), seed=seed + 90_000)
    ablations.to_csv(out / "synthetic_model_ablation.csv", index=False)
    audit = _identifiability_audit(real_summary["status"] == "evaluated")
    audit.to_csv(out / "identifiability_audit.csv", index=False)
    pd.DataFrame([
        ("population", "Client-owned dogs with nonmetastatic appendicular osteosarcoma after "
         "standard local control; eligibility and prognostic strata locked prospectively"),
        ("control_arm", "Stage-appropriate standard care"),
        ("research_arm", "Same standard care plus locked model-ranked multivalent RNA vaccine"),
        ("allocation", "Concurrent randomized comparison; analysis grouped by dog"),
        ("primary_endpoint", "Disease-free interval with event/censor definition prespecified"),
        ("secondary_endpoints", "Overall survival; toxicity; quality of life; immune response"),
        ("serial_measurements", "CBC, cytokines, TCR sequencing, ctDNA, thoracic imaging, toxicity"),
        ("model_gate", "Cargo pipeline, state model, kernels, schedules, and analysis locked before "
         "outcomes are inspected"),
        ("human_translation", "Separate HLA model after canine safety, immunogenicity, calibration, "
         "and randomized efficacy evaluation"),
    ], columns=["design_element", "locked_requirement"]).to_csv(
        out / "prospective_validation_protocol.csv", index=False)

    first, surface = _volterra_plot_arrays(model)
    plot_state_posteriors(
        posterior.day.to_numpy(), posterior.iloc[:, 1:].to_numpy(),
        [state.value for state in model.states], out / "filtered_state_probabilities.png",
        selected["vaccine_days"],
    )
    plot_volterra_memory(first, surface, list(model.input_names),
                         out / "volterra_transition_memory.png")
    plot_cargo_selection(
        candidate_table.dropna(subset=["robust_score"]),
        out / "cargo_selection.png",
        selected_column="joint_selected",
    )
    plot_clinical_anchors(clinical, out / "clinical_anchors.png")

    fixed_prior_comparison = _fixed_prior_soc_comparison(selected, comparator_metrics)
    achieved_median = _first_passage_median_days(comparator_relapse_cdf)
    summary = {
        "program": PROGRAM_ID,
        "target_setting": "canine_appendicular_osteosarcoma_minimal_residual_disease",
        "candidate_origin": candidate_origin,
        "candidate_file_sha256": candidate_hash,
        "design_specification_origin": specification_origin,
        "design_specification_file_sha256": specification_hash,
        "design_specification": specification.to_dict(),
        "selected_research_hypothesis": selected,
        "cargo_hsmm_integration": (
            "two_stage_robust_cargo_ranking_then_auditable_effective_coverage_proxy"
        ),
        "cargo_objective_weights": {
            name: float(value) for name, value in DEFAULT_DESIGN_WEIGHTS.__dict__.items()
        },
        "cargo_interaction_model": {
            "synergy_rank": len(candidates[0].synergy_loadings),
            "competition_rank": len(candidates[0].competition_loadings),
            "interaction_enabled": bool(
                candidates[0].synergy_loadings or candidates[0].competition_loadings),
        },
        "cargo_search_mode": design.search_mode,
        "feasible_cargo_designs_evaluated": design.feasible_designs_evaluated,
        "real_data_evaluation": real_summary,
        "nominal_fixed_prior_candidate_metrics": candidate_metrics,
        "robust_fixed_prior_candidate_metrics": {
            "robust_prior_objective": selected["robust_prior_objective"],
            "worst_scenario": selected["worst_scenario"],
            "worst_case_prior_objective": selected["worst_case_prior_objective"],
            "worst_case_exact_prior_ever_visible_relapse_probability": selected[
                "worst_case_exact_prior_ever_visible_relapse_probability"],
            "scenario_count": len(specification.scenarios),
        },
        "fixed_prior_soc_proxy_metrics": comparator_metrics,
        "fixed_prior_soc_comparison": fixed_prior_comparison,
        "fixed_prior_favors_candidate": fixed_prior_comparison["favors_candidate"],
        "policy_probability_computation": "exact_not_monte_carlo",
        "fixed_prior_equivalence_tolerance": PRIOR_EQUIVALENCE_TOLERANCE,
        "current_care_reference_anchors": _clinical_comparators(clinical),
        "clinical_evidence_status": "NOT_CLINICALLY_EVALUABLE_NO_RANDOMIZED_RNA_POLICY_DATA",
        "clinical_superiority_supported": False,
        "patient_treatment_recommendation": False,
        "volterra_order": 2,
        "hidden_state_model": "explicit_duration_hidden_semi_markov",
        "time_step_days": MODEL_STEP_DAYS,
        "dog_clock_prior_anchor": {
            "source": "COTC022 aggregate standard-care median DFI",
            "target_days": 180,
            "duration_scale_multiplier": 1.29,
            "achieved_soc_proxy_median_first_visible_relapse_days": achieved_median,
            "absolute_calibration_error_days": (
                None if achieved_median is None else abs(achieved_median - 180)),
            "visible_relapse_probability_at_day_zero": float(comparator_relapse_cdf[0]),
            "patient_level_fit": False,
        },
        "clinical_anchor_sha256": _sha256(anchors),
        "claim_scope": (
            "Research software and prospective experiment design. The selected cargo and schedule "
            "are not clinically calibrated, prescribed doses, or evidence of efficacy."
        ),
    }
    summary_path = out / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n")
    (out / "clinical_interpretation.md").write_text(_clinical_interpretation(summary))
    manifest = {
        "schema_version": 1,
        "program": PROGRAM_ID,
        "status": "COMPLETE",
        "arguments": {
            "seed": seed,
            "synthetic_ablation_draw_budget": draws,
            "synthetic_ablation_sequences": max(12, draws // 8),
            "model_step_days": MODEL_STEP_DAYS,
            "model_horizon_steps": MODEL_HORIZON_STEPS,
        },
        "input_sha256": {
            "clinical_anchors": _sha256(anchors),
            "candidate_file": candidate_hash,
            "design_specification_file": specification_hash,
            "gse76127_matrix": real_summary.get("matrix_sha256"),
            "gse76127_supplements": real_summary.get("supplements_sha256"),
        },
        "design_specification": specification.to_dict(),
        "cargo_search": {
            "top_k": CARGO_TOP_K,
            "beam_width": CARGO_BEAM_WIDTH,
            "exact_enumeration_limit": CARGO_EXACT_ENUMERATION_LIMIT,
            "joint_cargo_ranks_considered": JOINT_CARGO_LIMIT,
            "objective_weights": {
                name: float(value)
                for name, value in DEFAULT_DESIGN_WEIGHTS.__dict__.items()
            },
            "interaction_model": {
                "synergy_rank": len(candidates[0].synergy_loadings),
                "competition_rank": len(candidates[0].competition_loadings),
                "interaction_enabled": bool(
                    candidates[0].synergy_loadings
                    or candidates[0].competition_loadings),
            },
        },
        "response_proxy": {
            "weights": RESPONSE_PROXY_WEIGHTS,
            "interaction_offset": .5,
            "effective_proxy_clip": [.05, 1.0],
            "evaluated_per_design_scenario": True,
        },
        "policy_objective": {
            "weights": POLICY_OBJECTIVE_WEIGHTS,
            "favorable_state_terms_stop_after_first_visible_relapse": True,
            "equivalence_tolerance": PRIOR_EQUIVALENCE_TOLERANCE,
        },
        "schedule_hypotheses": {
            name: {
                "days": list(days),
                "relative_doses": list(doses),
                "dose_units": "normalized_model_input",
                "dose_evidence": "none_not_a_clinical_dose",
                **SCHEDULE_EVIDENCE[name],
            }
            for name, (days, doses) in _schedule_options().items()
        },
        "model": {
            "sha256": _model_sha256(model),
            "volterra_order": 2,
            "volterra_memory_steps": model.kernels.memory,
            "volterra_rank": model.kernels.rank,
            "hidden_state_model": "explicit_duration_hidden_semi_markov",
        },
        "runtime": _runtime_manifest(),
        "summary_sha256": _sha256(summary_path),
        "artifact_inventory": _artifact_inventory(out, manifest_path),
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    return summary


def run_osteosarcoma_benchmark(
    out: str | Path,
    anchors: str | Path = DEFAULT_ANCHORS,
    candidate_file: str | Path | None = None,
    design_spec_file: str | Path | None = None,
    gse76127_matrix: str | Path | None = None,
    gse76127_supplements: str | Path | None = None,
    draws: int = 192,
    seed: int = 2608,
) -> dict:
    """Build in a fresh sibling directory and publish only a complete result tree."""
    if draws < 16:
        raise ValueError("draws must be at least 16")
    raw_out = Path(out).expanduser()
    if raw_out.is_symlink():
        raise ValueError("output directory cannot be a symbolic link")
    destination = raw_out.resolve(strict=False)
    _validate_safe_output_scope(destination)
    _validate_inputs_outside_output(
        destination,
        anchors=anchors,
        candidate_file=candidate_file,
        design_spec_file=design_spec_file,
        gse76127_matrix=gse76127_matrix,
        gse76127_supplements=gse76127_supplements,
    )
    _validate_publish_target(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(
        prefix=f".{destination.name}.staging-",
        dir=destination.parent,
    ))
    try:
        summary = _run_osteosarcoma_benchmark_staged(
            out=staging,
            anchors=anchors,
            candidate_file=candidate_file,
            design_spec_file=design_spec_file,
            gse76127_matrix=gse76127_matrix,
            gse76127_supplements=gse76127_supplements,
            draws=draws,
            seed=seed,
        )
        _publish_staging_directory(staging, destination)
        return summary
    except BaseException:
        if staging.exists():
            shutil.rmtree(staging, ignore_errors=True)
        raise


__all__ = [
    "DEFAULT_ANCHORS",
    "illustrative_canine_antigens",
    "load_antigen_candidates",
    "load_clinical_anchors",
    "run_osteosarcoma_benchmark",
]
