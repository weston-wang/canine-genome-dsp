"""Reports and visual diagnostics for the combination-immunotherapy inverse demo."""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .evolution import volterra_response
from .immunotherapy import (optimize_immunotherapy, perturb_system,
                            reference_immunotherapy_system, simulate_immunotherapy,
                            synergy_surface)


def immunotherapy_demo(out: Path, scenarios: int = 12, maxiter: int = 60) -> None:
    system, kernels = reference_immunotherapy_system()
    rng = np.random.default_rng(91)
    systems = [system] + [perturb_system(system, rng) for _ in range(scenarios - 1)]
    initial = np.array([.28, .018]); horizon = 42; times = [0, 7, 14, 21]
    result = optimize_immunotherapy(systems, kernels, initial, horizon, times,
                                    np.array([1., .8, .7]), maxiter=maxiter)
    untreated_immune = volterra_response(np.zeros_like(result["schedule"]), kernels)
    untreated = np.stack([simulate_immunotherapy(s, untreated_immune, initial) for s in systems])
    out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(result["schedule"], columns=["vaccine", "checkpoint", "radiation"]).assign(
        day=np.arange(horizon)).to_csv(out / "optimized_schedule.csv", index=False)
    pd.DataFrame(result["immune"], columns=["cytotoxic", "exhaustion", "inflammation"]).assign(
        day=np.arange(horizon)).to_csv(out / "immune_outputs.csv", index=False)
    rows = []
    for scenario, path in enumerate(result["states"]):
        for day, state in enumerate(path):
            rows.append({"scenario": scenario, "day": day, "sensitive": state[0],
                         "escape": state[1], "total": state.sum(),
                         "escape_fraction": state[1] / max(state.sum(), np.finfo(float).eps)})
    pd.DataFrame(rows).to_csv(out / "scenario_trajectories.csv", index=False)
    surface = synergy_surface(kernels)
    pd.DataFrame(surface, index=pd.Index(range(len(surface)), name="vaccine_lag"),
                 columns=pd.Index(range(len(surface)), name="checkpoint_lag")).to_csv(
                     out / "vaccine_checkpoint_synergy.csv")
    treated_terminal = result["states"][:, -1].sum(axis=1)
    untreated_terminal = untreated[:, -1].sum(axis=1)
    peak_inflammation = float(result["immune"][:, 2].max())
    escape_fraction = result["states"][:, -1, 1] / treated_terminal
    summary = {
        "status": "synthetic proof of method; not fitted to patients and not a dosing recommendation",
        "therapy_channels": ["vaccine", "checkpoint inhibitor", "radiation"],
        "scenarios": scenarios,
        "median_terminal_tumor_reduction_vs_untreated": float(
            1 - np.median(treated_terminal) / np.median(untreated_terminal)),
        "worst_case_terminal_tumor": float(treated_terminal.max()),
        "worst_case_escape_fraction": float(escape_fraction.max()),
        "peak_inflammation_proxy": peak_inflammation,
        "inflammation_constraint": result["toxicity_limit"],
        "constraint_exceeded": bool(peak_inflammation > result["toxicity_limit"] + 1e-6),
        "optimizer_success": result["success"], "optimizer_message": result["message"],
        "clinical_meaning": {
            "tumor_reduction": "Model-estimated change in total tumor state, not RECIST response or survival.",
            "escape_fraction": "Share of modeled residual tumor in a weakly immune-visible state; it is not a measured mutation frequency.",
            "cytotoxic": "Latent antitumor immune activity; requires calibration to CD8/TCR or functional assays.",
            "exhaustion": "Latent attenuation of killing; requires checkpoint/exhaustion-marker validation.",
            "inflammation": "A toxicity-risk proxy, not a probability or grade of an adverse event.",
            "synergy_surface": "Timing-dependent quadratic interaction; positive regions suggest schedules worth testing, not clinical synergy proof."
        }
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    clinical = f"""# Clinical interpretation\n\nThis is a synthetic methods demonstration, not a treatment recommendation. The optimized schedule reduced median terminal modeled tumor burden by **{summary['median_terminal_tumor_reduction_vs_untreated']:.1%}** versus the simulated untreated course across {scenarios} parameter scenarios. The worst modeled residual tumor had an escape-state fraction of **{summary['worst_case_escape_fraction']:.1%}**. This means the schedule may select for weakly immune-visible disease even when total burden falls; clinically, longitudinal ctDNA, imaging, antigen expression, and T-cell measurements would be needed to determine whether that occurred.\n\nPeak inflammation proxy was **{peak_inflammation:.3f}** against a model constraint of **{result['toxicity_limit']:.3f}**. This is not an adverse-event probability or CTCAE grade. It only shows whether the fitted biomarker proxy stayed inside its prespecified modeling bound. The vaccine–checkpoint synergy surface shows which relative timings contribute positively to predicted cytotoxic activity. It generates hypotheses for prospective testing; it cannot establish causal synergy from this synthetic calibration.\n\nBefore clinical use, kernels must be estimated from longitudinal combination-therapy data, validated on held-out patients and external cohorts, calibrated to clinical endpoints, and reviewed under a protocol with explicit dose and safety constraints.\n"""
    (out / "clinical_interpretation.md").write_text(clinical)

    fig, axes = plt.subplots(2, 2, figsize=(11, 8))
    for path in untreated.sum(axis=2): axes[0, 0].plot(path, color="gray", alpha=.25)
    for path in result["states"].sum(axis=2): axes[0, 0].plot(path, color="tab:blue", alpha=.3)
    axes[0, 0].set(title="Tumor scenarios", xlabel="day", ylabel="modeled burden")
    for i, name in enumerate(["cytotoxic", "exhaustion", "inflammation"]):
        axes[0, 1].plot(result["immune"][:, i], label=name)
    axes[0, 1].axhline(result["toxicity_limit"], color="tab:red", ls="--", label="inflammation bound")
    axes[0, 1].set(title="Latent immune outputs", xlabel="day"); axes[0, 1].legend()
    image = axes[1, 0].imshow(surface, origin="lower", aspect="auto", cmap="viridis")
    axes[1, 0].set(title="Vaccine × checkpoint synergy", xlabel="checkpoint lag", ylabel="vaccine lag")
    fig.colorbar(image, ax=axes[1, 0], label="quadratic cytotoxic contribution")
    for i, name in enumerate(["vaccine", "checkpoint", "radiation"]):
        axes[1, 1].step(range(horizon), result["schedule"][:, i], where="post", label=name)
    axes[1, 1].set(title="Model-selected bounded schedule", xlabel="day", ylabel="normalized input")
    axes[1, 1].legend(); fig.tight_layout(); fig.savefig(out / "clinical_dashboard.png", dpi=180); plt.close(fig)
