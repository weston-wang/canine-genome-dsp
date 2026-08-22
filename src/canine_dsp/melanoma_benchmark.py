"""Disease-specific, fail-closed benchmark for neoadjuvant melanoma DSP policies."""

from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .clinical_validation import (
    clinical_utility_rank,
    fit_binomial_link,
    leave_one_arm_out_binomial,
)
from .melanoma_dsp import (
    CHANNEL_NAMES,
    MelanomaDSPModel,
    MelanomaRun,
    MelanomaSimulationConfig,
    VolterraCrossKernel,
    nadina_schedule,
    reference_melanoma_model,
    search_constrained_schedule,
    simulate_antibody_exposure,
    simulate_melanoma,
)


DEFAULT_ANCHORS = Path("data/clinical/melanoma_clinical_anchors.csv")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def _load_opacin_arms(path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    anchors = pd.read_csv(path)
    mpr_rows = anchors.loc[(anchors.study == "OpACIN-neo")
                           & (anchors.endpoint == "major_pathological_response")]
    response_endpoint = ("major_pathological_response" if len(mpr_rows) == 3
                         else "pathological_response")
    response = anchors.loc[
        (anchors.study == "OpACIN-neo") & (anchors.endpoint == response_endpoint),
        ["arm", "n", "numerator", "denominator", "schedule_or_sampling"],
    ].copy()
    toxicity = anchors.loc[
        (anchors.study == "OpACIN-neo")
        & (anchors.endpoint == "grade_3_4_immune_related_adverse_event"),
        ["arm", "numerator", "denominator"],
    ].copy()
    response = response.rename(columns={"numerator": "response_events",
                                        "denominator": "response_total"})
    toxicity = toxicity.rename(columns={"numerator": "toxicity_events",
                                        "denominator": "toxicity_total"})
    arms = response.merge(toxicity, on="arm", validate="one_to_one")
    numeric = ["n", "response_events", "response_total", "toxicity_events", "toxicity_total"]
    arms[numeric] = arms[numeric].apply(pd.to_numeric)
    if len(arms) != 3 or not np.all(arms.response_total == arms.toxicity_total):
        raise ValueError("expected three complete OpACIN-neo treatment arms")
    arms["n"] = arms.response_total.astype(int)
    arms["response_events"] = arms.response_events.astype(int)
    arms["toxicity_events"] = arms.toxicity_events.astype(int)
    arms["response_endpoint"] = response_endpoint
    return arms[["arm", "n", "response_events", "toxicity_events",
                 "response_endpoint", "schedule_or_sampling"]], anchors


def opacin_equivalent_schedules(horizon: int = 42) -> dict[str, np.ndarray]:
    """Encode published relative dose/timing arms on the NADINA flat-dose scale.

    OpACIN-neo used mg/kg, while NADINA used flat doses.  These are normalized
    ratio-equivalent model inputs, not reconstructed administered milligrams.
    """
    if horizon < 42:
        raise ValueError("the OpACIN-neo benchmark ends at week-six surgery")
    schedules = {}
    arm_a = np.zeros((horizon, 2)); arm_a[[0, 21]] = [240.0, 80.0]
    arm_b = nadina_schedule(horizon)
    # Arm C used ipilimumab at weeks 0/3, then nivolumab just after the week-3
    # ipilimumab and again at week 5.
    arm_c = np.zeros((horizon, 2)); arm_c[[0, 21], 0] = 240.0
    arm_c[[21, 35], 1] = 240.0
    schedules.update({"arm A": arm_a, "arm B": arm_b, "arm C": arm_c})
    return schedules


def _run_score(run: MelanomaRun) -> tuple[float, float]:
    initial = run.tumor[:, 0].sum(axis=1)
    terminal = run.tumor[:, -1].sum(axis=1)
    residual = terminal / np.maximum(initial, np.finfo(float).eps)
    efficacy = float(-np.log(max(np.median(residual), 1e-8)))
    # Severe toxicity is not only the latent exhaustion state: administered
    # checkpoint-antibody burden remains a direct safety signal, especially
    # for the high-ipilimumab OpACIN arms.
    normalized_total = run.schedule.sum(axis=0) / np.array([160.0, 480.0])
    toxicity = float(np.quantile(run.toxicity.max(axis=1), .95)
                     + .25 * normalized_total[0] + .10 * normalized_total[1])
    return efficacy, toxicity


def _dose_score(schedule: np.ndarray) -> tuple[float, float]:
    total = schedule.sum(axis=0) / np.array([160.0, 480.0])
    return float(.25 * total[0] + .75 * total[1]), float(.85 * total[0] + .15 * total[1])


def _exposure_score(schedule: np.ndarray) -> tuple[float, float]:
    exposure = simulate_antibody_exposure(schedule)
    auc = exposure.occupancy.sum(axis=0) / len(schedule)
    return float(.25 * auc[0] + .75 * auc[1]), float(.85 * auc[0] + .15 * auc[1])


def _without_volterra(model: MelanomaDSPModel) -> MelanomaDSPModel:
    kernel = replace(model.cross_kernel, gain=0.0)
    return replace(model, cross_kernel=kernel)


def _shared_output_volterra(model: MelanomaDSPModel) -> MelanomaDSPModel:
    """Ablation that forces one cross-kernel into efficacy and toxicity states."""
    return replace(model, dynamics=replace(model.dynamics, residual_exhaustion_gain=.025))


def _arm_features(schedules: dict[str, np.ndarray], model: MelanomaDSPModel,
                  config: MelanomaSimulationConfig, seed: int) -> dict[str, pd.DataFrame]:
    rows = {name: [] for name in ["dose_only", "hammerstein_pk", "bilinear_stochastic",
                                   "shared_output_volterra", "full_dsp_stack"]}
    for arm, schedule in schedules.items():
        dose_efficacy, dose_toxicity = _dose_score(schedule)
        pk_efficacy, pk_toxicity = _exposure_score(schedule)
        bilinear = simulate_melanoma(schedule, _without_volterra(model), config, seed,
                                     enforce_constraints=False)
        shared = simulate_melanoma(schedule, _shared_output_volterra(model), config, seed,
                                   enforce_constraints=False)
        full = simulate_melanoma(schedule, model, config, seed, enforce_constraints=False)
        bilinear_efficacy, bilinear_toxicity = _run_score(bilinear)
        shared_efficacy, shared_toxicity = _run_score(shared)
        full_efficacy, full_toxicity = _run_score(full)
        values = {
            "dose_only": (dose_efficacy, dose_toxicity),
            "hammerstein_pk": (pk_efficacy, pk_toxicity),
            "bilinear_stochastic": (bilinear_efficacy, bilinear_toxicity),
            "shared_output_volterra": (shared_efficacy, shared_toxicity),
            "full_dsp_stack": (full_efficacy, full_toxicity),
        }
        for name, (efficacy, toxicity) in values.items():
            rows[name].append({"arm": arm, "efficacy_score_raw": efficacy,
                               "toxicity_score_raw": toxicity})
    result = {}
    for name, values in rows.items():
        table = pd.DataFrame(values)
        for raw, standardized in [("efficacy_score_raw", "efficacy_score"),
                                  ("toxicity_score_raw", "toxicity_score")]:
            scale = table[raw].std(ddof=0)
            table[standardized] = ((table[raw] - table[raw].mean()) / scale
                                   if scale > 1e-12 else 0.0)
        result[name] = table
    return result


def validate_randomized_arms(arms: pd.DataFrame, features: dict[str, pd.DataFrame]
                             ) -> tuple[pd.DataFrame, pd.DataFrame]:
    predictions, rows = [], []
    for name, model_features in features.items():
        table = arms.merge(model_features, on="arm", validate="one_to_one")
        response, response_metrics = leave_one_arm_out_binomial(
            table, ["efficacy_score"], "response_events", "n")
        toxicity, toxicity_metrics = leave_one_arm_out_binomial(
            table, ["toxicity_score"], "toxicity_events", "n")
        response = response.rename(columns={"observed_probability": "observed_response",
                                            "predicted_probability": "predicted_response"})
        toxicity = toxicity.rename(columns={"observed_probability": "observed_toxicity",
                                            "predicted_probability": "predicted_toxicity"})
        merged = response[["arm", "observed_response", "predicted_response"]].merge(
            toxicity[["arm", "observed_toxicity", "predicted_toxicity"]], on="arm")
        merged.insert(0, "model", name); predictions.append(merged)
        rank = clinical_utility_rank(
            table, merged.predicted_response.to_numpy(), merged.predicted_toxicity.to_numpy(),
            "response_events", "toxicity_events", "n")
        rows.append({"model": name,
                     "response_arm_brier": response_metrics["arm_level_weighted_brier"],
                     "response_arm_log_loss": response_metrics["arm_level_weighted_log_loss"],
                     "toxicity_arm_brier": toxicity_metrics["arm_level_weighted_brier"],
                     "toxicity_arm_log_loss": toxicity_metrics["arm_level_weighted_log_loss"],
                     **rank})
    return pd.concat(predictions, ignore_index=True), pd.DataFrame(rows)


def _paired_bootstrap(candidate: np.ndarray, comparator: np.ndarray, seed: int,
                      relative: bool = False, repetitions: int = 2_000) -> tuple[float, list[float]]:
    candidate = np.asarray(candidate, float); comparator = np.asarray(comparator, float)
    if candidate.shape != comparator.shape:
        raise ValueError("paired virtual populations must have equal dimensions")
    rng = np.random.default_rng(seed); values = np.zeros(repetitions)
    for index in range(repetitions):
        selected = rng.integers(0, len(candidate), len(candidate))
        if relative:
            values[index] = np.mean(1 - candidate[selected] / np.maximum(
                comparator[selected], np.finfo(float).eps))
        else:
            values[index] = np.mean(candidate[selected] - comparator[selected])
    estimate = (np.mean(1 - candidate / np.maximum(comparator, np.finfo(float).eps))
                if relative else np.mean(candidate - comparator))
    return float(estimate), [float(value) for value in np.quantile(values, [.025, .975])]


def compare_virtual_policies(candidate: MelanomaRun, comparator: MelanomaRun,
                             seed: int = 941) -> tuple[dict, pd.DataFrame]:
    candidate_total = candidate.tumor[:, -1].sum(axis=1)
    comparator_total = comparator.tumor[:, -1].sum(axis=1)
    candidate_escape = np.divide(candidate.tumor[:, -1, 1], candidate_total,
                                 out=np.zeros_like(candidate_total), where=candidate_total > 0)
    comparator_escape = np.divide(comparator.tumor[:, -1, 1], comparator_total,
                                  out=np.zeros_like(comparator_total), where=comparator_total > 0)
    candidate_toxicity = candidate.toxicity.max(axis=1)
    comparator_toxicity = comparator.toxicity.max(axis=1)
    tumor, tumor_ci = _paired_bootstrap(candidate_total, comparator_total, seed, True)
    toxicity, toxicity_ci = _paired_bootstrap(candidate_toxicity, comparator_toxicity,
                                               seed + 1, True)
    escape, escape_ci = _paired_bootstrap(candidate_escape, comparator_escape, seed + 2)
    efficacy_path = tumor_ci[0] > .05 and toxicity_ci[0] >= -.05
    deintensification_path = tumor_ci[0] >= -.05 and toxicity_ci[0] > .10
    escape_safe = escape_ci[1] <= .05
    summary = {
        "terminal_tumor_relative_improvement": tumor,
        "terminal_tumor_relative_improvement_bootstrap95": tumor_ci,
        "toxicity_proxy_relative_improvement": toxicity,
        "toxicity_proxy_relative_improvement_bootstrap95": toxicity_ci,
        "escape_fraction_difference": escape,
        "escape_fraction_difference_bootstrap95": escape_ci,
        "efficacy_superiority_path_met": bool(efficacy_path),
        "deintensification_path_met": bool(deintensification_path),
        "escape_safety_gate_met": bool(escape_safe),
        "simulation_candidate_supported": bool((efficacy_path or deintensification_path)
                                                and escape_safe),
        "clinical_superiority_established": False,
    }
    rows = []
    for draw in range(len(candidate_total)):
        for policy, total, escaped, toxic in [
            ("dsp_candidate", candidate_total[draw], candidate_escape[draw],
             candidate_toxicity[draw]),
            ("nadina_regimen", comparator_total[draw], comparator_escape[draw],
             comparator_toxicity[draw]),
        ]:
            rows.append({"draw": draw, "policy": policy, "terminal_tumor": total,
                         "escape_fraction": escaped, "peak_toxicity_proxy": toxic})
    return summary, pd.DataFrame(rows)


def _dynamic_anchor_check(model: MelanomaDSPModel, config: MelanomaSimulationConfig,
                          seed: int) -> tuple[pd.DataFrame, dict]:
    horizon = 70; treatment_days = [0, 21, 42, 63]
    schedules = {}
    for name, dose in [("anti_CTLA4", np.array([80.0, 0.])),
                       ("anti_PD1", np.array([0., 240.0])),
                       ("combination", np.array([80.0, 240.0]))]:
        schedule = np.zeros((horizon, 2)); schedule[treatment_days] = dose
        schedules[name] = schedule
    rows = []
    for name, schedule in schedules.items():
        run = simulate_melanoma(schedule, model, config, seed, enforce_constraints=False)
        for week in [0, 3, 6, 9]:
            day = 0 if week == 0 else week * 7
            rows.append({"therapy": name, "week": week,
                         "median_effector_state": float(np.median(run.immune[:, day, 1])),
                         "median_progenitor_tex_state": float(np.median(run.immune[:, day, 0]))})
    table = pd.DataFrame(rows)
    pivot = table.pivot(index="week", columns="therapy", values="median_effector_state")
    checks = {
        "gse_reported_combo_greater_week6_reproduced": bool(
            pivot.loc[6, "combination"] > max(pivot.loc[6, "anti_CTLA4"],
                                               pivot.loc[6, "anti_PD1"])),
        "gse_reported_combo_greater_week9_reproduced": bool(
            pivot.loc[9, "combination"] > max(pivot.loc[9, "anti_CTLA4"],
                                               pivot.loc[9, "anti_PD1"])),
        "quantitative_patient_level_fit": False,
        "anchor_scope": "directional published GSE272993-associated time anchors only",
    }
    checks["directional_dynamic_anchors_reproduced"] = bool(
        checks["gse_reported_combo_greater_week6_reproduced"]
        and checks["gse_reported_combo_greater_week9_reproduced"])
    return table, checks


def _candidate_link_probabilities(arms: pd.DataFrame, full_features: pd.DataFrame,
                                  candidate_score: tuple[float, float],
                                  nadina_score: tuple[float, float]) -> dict:
    table = arms.merge(full_features, on="arm", validate="one_to_one")
    response_link = fit_binomial_link(table, ["efficacy_score"], "response_events", "n")
    toxicity_link = fit_binomial_link(table, ["toxicity_score"], "toxicity_events", "n")
    efficacy_mean = full_features.efficacy_score_raw.mean()
    efficacy_sd = full_features.efficacy_score_raw.std(ddof=0)
    toxicity_mean = full_features.toxicity_score_raw.mean()
    toxicity_sd = full_features.toxicity_score_raw.std(ddof=0)
    def transform(score):
        efficacy = ((score[0] - efficacy_mean) / efficacy_sd if efficacy_sd > 1e-12 else 0.)
        toxicity = ((score[1] - toxicity_mean) / toxicity_sd if toxicity_sd > 1e-12 else 0.)
        return float(response_link.predict_proba([[efficacy]])[0, 1]), float(
            toxicity_link.predict_proba([[toxicity]])[0, 1])
    candidate = transform(candidate_score); nadina = transform(nadina_score)
    response_supported = (full_features.efficacy_score_raw.min() <= candidate_score[0]
                          <= full_features.efficacy_score_raw.max())
    toxicity_supported = (full_features.toxicity_score_raw.min() <= candidate_score[1]
                          <= full_features.toxicity_score_raw.max())
    endpoint = str(arms.response_endpoint.iloc[0])
    warning = ("OpACIN and NADINA MPR both use <=10% viable tumor, but populations, flat versus "
               "weight-based dosing, and downstream treatment differ." if
               endpoint == "major_pathological_response" else
               "OpACIN pathologic response (<50% viable) is not NADINA MPR (<=10%).")
    return {
        "opacin_response_endpoint": endpoint,
        "aggregate_calibrated_candidate_opacin_response_probability": (
            candidate[0] if response_supported else None),
        "aggregate_calibrated_nadina_opacin_response_probability": nadina[0],
        "aggregate_calibrated_candidate_grade3_4_irae_probability": (
            candidate[1] if toxicity_supported else None),
        "aggregate_calibrated_nadina_grade3_4_irae_probability": nadina[1],
        "unsupported_extrapolated_candidate_response_probability": candidate[0],
        "unsupported_extrapolated_candidate_grade3_4_irae_probability": candidate[1],
        "candidate_efficacy_score_inside_opacin_range": bool(response_supported),
        "candidate_toxicity_score_inside_opacin_range": bool(toxicity_supported),
        "endpoint_warning": warning,
    }


def _plot_dashboard(out: Path, predictions: pd.DataFrame, ablations: pd.DataFrame,
                    candidate: MelanomaRun, comparator: MelanomaRun) -> None:
    full = predictions.loc[predictions.model == "full_dsp_stack"]
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    x = np.arange(len(full)); width = .18
    axes[0, 0].bar(x - 1.5 * width, full.observed_response, width,
                   label="observed path response")
    axes[0, 0].bar(x - .5 * width, full.predicted_response, width,
                   label="LOAO path response")
    axes[0, 0].bar(x + .5 * width, full.observed_toxicity, width, label="observed irAE")
    axes[0, 0].bar(x + 1.5 * width, full.predicted_toxicity, width, label="LOAO irAE")
    axes[0, 0].set(xticks=x, xticklabels=full.arm, ylim=(0, 1), ylabel="probability",
                   title="OpACIN-neo held-out-arm recovery")
    axes[0, 0].legend(fontsize=8)

    order = ["dose_only", "hammerstein_pk", "bilinear_stochastic",
             "shared_output_volterra", "full_dsp_stack"]
    metric = ablations.set_index("model").reindex(order)
    x = np.arange(len(order))
    axes[0, 1].bar(x - .18, metric.response_arm_brier, .36, label="path response")
    axes[0, 1].bar(x + .18, metric.toxicity_arm_brier, .36, label="grade 3-4 irAE")
    axes[0, 1].set(xticks=x, xticklabels=["dose", "PK", "bilinear", "shared V", "full DSP"],
                   ylabel="weighted Brier (lower is better)", title="Real-arm ablation")
    axes[0, 1].legend(fontsize=8)

    for channel, name in enumerate(CHANNEL_NAMES):
        axes[1, 0].step(range(len(candidate.schedule)), candidate.schedule[:, channel],
                        where="post", label=f"candidate {name}")
        axes[1, 0].step(range(len(comparator.schedule)), comparator.schedule[:, channel],
                        where="post", linestyle="--", label=f"NADINA {name}")
    axes[1, 0].set(xlabel="day", ylabel="modeled flat-dose input (mg)",
                   title="Locked comparator and candidate hypothesis")
    axes[1, 0].legend(fontsize=7, ncol=2)

    for run, name, color in [(comparator, "NADINA", "tab:gray"),
                             (candidate, "candidate", "tab:blue")]:
        total = run.tumor.sum(axis=2)
        median = np.median(total, axis=0); low = np.quantile(total, .05, axis=0)
        high = np.quantile(total, .95, axis=0); days = np.arange(total.shape[1])
        axes[1, 1].plot(days, median, label=name, color=color)
        axes[1, 1].fill_between(days, low, high, color=color, alpha=.15)
    axes[1, 1].set(xlabel="day", ylabel="normalized tumor burden",
                   title="Virtual population (5th-95th percentile)")
    axes[1, 1].legend()
    fig.tight_layout(); fig.savefig(out / "melanoma_dsp_dashboard.png", dpi=180)
    plt.close(fig)


def _clinical_report(summary: dict, anchors: pd.DataFrame) -> str:
    comparison = summary["virtual_policy_comparison"]
    full = summary["randomized_arm_validation"]["full_dsp_stack"]
    nadina = anchors.loc[(anchors.study == "NADINA") & anchors.endpoint.isin(
        ["major_pathological_response", "event_free_survival",
         "grade_3_or_higher_systemic_treatment_related_adverse_event"]),
        ["record_id", "endpoint", "landmark_week", "estimate", "unit"]]
    benchmark_lines = "\n".join(
        f"- {row.record_id}: {row.estimate} {row.unit} ({row.endpoint}"
        f"{f', landmark week {row.landmark_week:g}' if pd.notna(row.landmark_week) else ''})"
        for row in nadina.itertuples())
    status = summary["simulation_evidence_status"].replace("_", " ").lower()
    tumor_change = comparison["terminal_tumor_relative_improvement"]
    tumor_phrase = (f"improved terminal tumor burden by {tumor_change:.1%}" if tumor_change >= 0
                    else f"worsened terminal tumor burden by {-tumor_change:.1%}")
    toxicity_change = comparison["toxicity_proxy_relative_improvement"]
    toxicity_phrase = (f"improved the toxicity proxy by {toxicity_change:.1%}"
                       if toxicity_change >= 0 else
                       f"worsened the toxicity proxy by {-toxicity_change:.1%}")
    endpoint_note = ("This run uses the like-for-like <=10% viable-tumor MPR definition for "
                     "OpACIN-neo and NADINA. Their populations, dose units, toxicity windows, "
                     "and downstream therapies still differ." if
                     summary["opacin_response_endpoint"] == "major_pathological_response" else
                     "OpACIN-neo pathological response means less than 50% viable tumor; NADINA "
                     "major pathological response means no more than 10%.")
    return f"""# Clinical interpretation

## Bottom line

This benchmark is **{status}**. In the synthetic virtual population, the candidate **{tumor_phrase}**
(relative-improvement paired bootstrap 95%
interval {comparison['terminal_tumor_relative_improvement_bootstrap95'][0]:.1%} to
{comparison['terminal_tumor_relative_improvement_bootstrap95'][1]:.1%}) and **{toxicity_phrase}**.
These are model
outputs, not clinical response or adverse-event rates.

On the three randomized OpACIN-neo arms, the full model's leave-one-arm-out response Brier score was
**{full['response_arm_brier']:.3f}**, its toxicity Brier score was
**{full['toxicity_arm_brier']:.3f}**, and it
{'did' if full['clinical_tradeoff_arm_recovered'] else 'did not'} recover arm B using the locked
rule “within ten percentage points of the best pathologic response, then lowest serious toxicity.”
With only three arm-level points, this is a weak falsification test—not patient-level validation.

## Current clinical benchmark

{benchmark_lines}

{endpoint_note} Toxicity collection windows also differ. The code never converts a short-term
immune score into an EFS claim.

## What the candidate means clinically

It is a constrained experimental schedule hypothesis inside the total dose and presurgical window
of the NADINA regimen. It is **not** a treatment recommendation. Aggregate public data provide no
randomized support for its exact timing, and the optimizer cannot account for an individual
patient's comorbidities, pathology, BRAF status, organ toxicity, or surgical constraints.

The next credible test is a preregistered, site-held-out silent evaluation using patient-level drug
timestamps, serial PBMC/TCR, ctDNA, imaging, pathology, and adverse events. Only after calibration,
overlap checks, and a safety review should the schedule be compared prospectively with NADINA in a
randomized trial. Clinical superiority is **not established**.
"""


def run_melanoma_benchmark(out: Path, anchors_path: Path = DEFAULT_ANCHORS,
                           draws: int = 192, candidates: int = 96,
                           seed: int = 142) -> None:
    if draws < 16 or candidates < 5:
        raise ValueError("benchmark requires draws>=16 and candidates>=5")
    arms, anchors = _load_opacin_arms(anchors_path)
    model = reference_melanoma_model()
    config = MelanomaSimulationConfig(draws=draws)
    schedules = opacin_equivalent_schedules()
    features = _arm_features(schedules, model, config, seed + 100)
    predictions, ablations = validate_randomized_arms(arms, features)

    search = search_constrained_schedule(model, config, candidates, seed)
    candidate_run = search["run"]
    comparator_run = simulate_melanoma(nadina_schedule(), model, config, seed + 10_000)
    virtual_comparison, virtual_draws = compare_virtual_policies(
        candidate_run, comparator_run, seed + 700)
    dynamics, dynamic_checks = _dynamic_anchor_check(model, config, seed + 800)
    calibrated_links = _candidate_link_probabilities(
        arms, features["full_dsp_stack"], _run_score(candidate_run),
        _run_score(comparator_run))

    full_validation = ablations.loc[ablations.model == "full_dsp_stack"].iloc[0].to_dict()
    treatment_support = any(np.array_equal(candidate_run.schedule, schedule)
                            for schedule in schedules.values())
    summary = {
        "disease": "macroscopic resectable stage III cutaneous melanoma",
        "clinical_context": "neoadjuvant ipilimumab plus nivolumab before week-six surgery",
        "data_sources": ["GSE272993", "OpACIN-neo NCT02977052", "NADINA NCT04949113"],
        "opacin_response_endpoint": str(arms.response_endpoint.iloc[0]),
        "anchors_sha256": _sha256(anchors_path),
        "model_stack": ["Hammerstein antibody exposure and occupancy",
                        "bilinear progenitor-TEX to effector state dynamics",
                        "bounded low-rank second-order Volterra efficacy residual",
                        "separate bilinear and dose-driven toxicity head",
                        "stochastic tumor birth-death, escape, and toxicity processes",
                        "risk-constrained schedule search"],
        "randomized_arm_validation": {
            row.model: {key: (None if pd.isna(value) else value)
                        for key, value in row._asdict().items() if key != "model"}
            for row in ablations.itertuples(index=False)},
        "gse272993_directional_dynamic_check": dynamic_checks,
        "aggregate_calibrated_links": calibrated_links,
        "virtual_policy_comparison": virtual_comparison,
        "candidate_schedule_matches_randomized_arm": treatment_support,
        "causal_treatment_support": bool(treatment_support),
        "simulation_evidence_status": ("IN_SILICO_CANDIDATE" if
                                       virtual_comparison["simulation_candidate_supported"] else
                                       "NO_IN_SILICO_ADVANTAGE"),
        "clinical_evidence_status": "NOT_CLINICALLY_EVALUABLE_AGGREGATE_ONLY",
        "clinical_superiority_supported": False,
        "primary_limitations": [
            "GSE272993 dynamics are stage IV and observational, not the stage III randomized arms",
            "OpACIN-neo contributes only three aggregate randomized arm points",
            "candidate timing lacks randomized treatment support unless it exactly matches an arm",
            "NADINA MPR, EFS, and toxicity are benchmark anchors, not model-fitted outcomes",
        ],
    }
    # Normalize numpy scalar values before JSON serialization.
    summary = json.loads(json.dumps(summary, default=lambda value: value.item()
                                    if isinstance(value, np.generic) else str(value)))
    out.mkdir(parents=True, exist_ok=True)
    predictions.to_csv(out / "opacin_leave_one_arm_out_predictions.csv", index=False)
    ablations.to_csv(out / "model_ablation_metrics.csv", index=False)
    dynamics.to_csv(out / "gse272993_directional_anchor_check.csv", index=False)
    virtual_draws.to_csv(out / "candidate_vs_nadina_virtual_draws.csv", index=False)
    pd.DataFrame(candidate_run.schedule, columns=CHANNEL_NAMES).assign(
        day=np.arange(len(candidate_run.schedule)),
        role="research_hypothesis_not_recommendation").to_csv(
            out / "candidate_schedule.csv", index=False)
    pd.DataFrame(comparator_run.schedule, columns=CHANNEL_NAMES).assign(
        day=np.arange(len(comparator_run.schedule)), role="published_NADINA_comparator").to_csv(
            out / "nadina_comparator_schedule.csv", index=False)
    anchors.to_csv(out / "clinical_anchors_used.csv", index=False)
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (out / "clinical_interpretation.md").write_text(_clinical_report(summary, anchors))
    _plot_dashboard(out, predictions, ablations, candidate_run, comparator_run)
