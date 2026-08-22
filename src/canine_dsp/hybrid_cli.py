"""End-to-end real-expression preparation and inverse-control demonstrations."""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .control import ControlWeights, optimize_vaccine, trajectory_cost
from .evolution import (
    EvolutionModel,
    ImmuneKernels,
    perturb_model,
    simulate_evolution,
    volterra_response,
)
from .expression import (
    collapse_technical_replicates,
    pca_modules,
    read_dog10k_aging,
    read_geo_series_matrix,
)


def prepare_gse9794(matrix: Path, out: Path, modules: int = 8) -> None:
    expression, samples = read_geo_series_matrix(matrix)
    collapsed, annotations = collapse_technical_replicates(expression, samples)
    scores, loadings = pca_modules(collapsed, modules)
    out.mkdir(parents=True, exist_ok=True)
    annotations.join(scores).sort_values("time_days").to_csv(out / "sample_modules.csv")
    loadings.to_csv(out / "probe_loadings.csv")
    summary = {"source": "GSE9794", "species": "Canis lupus familiaris",
               "assay": "Affymetrix Canine Genome 1.0 Array",
               "technical_samples": expression.shape[1],
               "biological_samples": collapsed.shape[1], "features": expression.shape[0],
               "modules": scores.shape[1], "warning": "Five destructive-sampling time points; "
               "appropriate for low-resolution method development, not treatment optimization."}
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


def prepare_dog10k_aging(expression_path: Path, information_path: Path, out: Path,
                         modules: int = 8) -> None:
    expression, information = read_dog10k_aging(expression_path, information_path)
    sample_column = information.columns[0]
    information = information.rename(columns={sample_column: "sample_id"}).set_index("sample_id")
    common = [sample for sample in expression.columns if sample in information.index]
    if len(common) < 3:
        raise ValueError("Dog10K expression and information sample identifiers do not align")
    expression = expression[common]
    scores, loadings = pca_modules(expression, modules)
    out.mkdir(parents=True, exist_ok=True)
    information.loc[common].join(scores).to_csv(out / "sample_modules.csv")
    loadings.to_csv(out / "gene_loadings.csv")
    summary = {"source": "Dog10K PRJCA016985", "species": "Canis lupus familiaris",
               "design": "cross-sectional whole-blood aging", "samples": len(common),
               "one_to_one_ortholog_genes": expression.shape[0], "modules": scores.shape[1],
               "warning": "Age is cross-sectional; these observations do not identify temporal "
               "or vaccine-response kernels."}
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


def reference_hybrid_system() -> tuple[EvolutionModel, ImmuneKernels, np.ndarray, np.ndarray]:
    """A transparent three-clone benchmark, not a fitted clinical model."""
    model = EvolutionModel(
        growth=np.array([.10, .085, .075]),
        antigen_expression=np.array([[1., .8, .2], [.05, 1., .2], [0., .1, 1.]]),
        presentation=np.array([[1., 1., 1.], [.8, 1., .9], [.2, .4, 1.]]),
        mutation=np.array([[.9985, .001, .0005], [0., .999, .001], [0., 0., 1.]]),
        carrying_capacity=2.0, immune_kill=.22,
    )
    h1 = np.zeros((3, 3, 6))
    decay = np.array([.9, .72, .50, .32, .18, .08])
    for antigen in range(3):
        h1[antigen, antigen] = decay
    h2 = np.zeros((3, 3, 3, 6, 6))
    # Mild same-antigen saturation and cross-antigen priming synergy.
    for antigen in range(3):
        h2[antigen, antigen, antigen] = -.045 * np.outer(decay, decay)
    h2[:, 0, 1] += .018 * np.outer(decay, decay)
    h2[:, 1, 0] += .018 * np.outer(decay, decay)
    return model, ImmuneKernels(h1, h2), np.array([.32, .025, .005]), np.array([1, 2])


def inverse_demo(out: Path, scenarios: int = 8, maxiter: int = 60) -> None:
    model, kernels, initial, escape = reference_hybrid_system()
    rng = np.random.default_rng(22)
    models = [model] + [perturb_model(model, rng=rng) for _ in range(scenarios - 1)]
    horizon, times = 30, [0, 7, 14]
    weights = ControlWeights(terminal_tumor=1, escape_fraction=1.5, dose=.008, peak_tumor=.2)
    result = optimize_vaccine(models, kernels, initial, horizon, times, np.ones(3), escape,
                              weights, maxiter=maxiter)
    zero_schedule = np.zeros_like(result["schedule"])
    zero_response = volterra_response(zero_schedule, kernels)
    untreated = np.stack([simulate_evolution(item, initial, zero_response) for item in models])
    baseline_cost = max(trajectory_cost(path, zero_schedule, escape, weights) for path in untreated)
    out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(result["schedule"], columns=["antigen_1", "antigen_2", "antigen_3"]).assign(
        time=np.arange(horizon)).to_csv(out / "optimized_schedule.csv", index=False)
    pd.DataFrame(result["immune_response"], columns=["response_1", "response_2", "response_3"]).assign(
        time=np.arange(horizon)).to_csv(out / "immune_response.csv", index=False)
    rows = []
    for scenario, path in enumerate(result["trajectories"]):
        for time, state in enumerate(path):
            rows.append({"scenario": scenario, "time": time, **{f"clone_{i + 1}": value
                        for i, value in enumerate(state)}, "total": state.sum()})
    pd.DataFrame(rows).to_csv(out / "trajectories.csv", index=False)
    summary = {"model_status": "synthetic benchmark; not clinically calibrated",
               "scenarios": scenarios, "horizon": horizon, "administration_times": times,
               "baseline_worst_cost": baseline_cost, "optimized_worst_cost": result["worst_cost"],
               "relative_cost_reduction": 1 - result["worst_cost"] / baseline_cost,
               "optimizer_success": result["success"], "optimizer_message": str(result["message"])}
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    fig, axes = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
    treated_total = result["trajectories"].sum(axis=2)
    untreated_total = untreated.sum(axis=2)
    for values in untreated_total: axes[0].plot(values, color="gray", alpha=.25)
    for values in treated_total: axes[0].plot(values, color="tab:blue", alpha=.35)
    axes[0].set(ylabel="total tumor state", title="Uncertainty scenarios: untreated (gray), optimized (blue)")
    for antigen in range(3): axes[1].step(np.arange(horizon), result["schedule"][:, antigen], where="post",
                                         label=f"antigen {antigen + 1}")
    axes[1].set(xlabel="model time", ylabel="dose", title="Robust inverse solution")
    axes[1].legend(); fig.tight_layout(); fig.savefig(out / "inverse_control.png", dpi=170); plt.close(fig)
