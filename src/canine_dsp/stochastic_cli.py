"""End-to-end stochastic Volterra immunotherapy benchmark and clinical report."""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .immunotherapy import reference_immunotherapy_system, synergy_surface
from .stochastic_immunotherapy import (
    StochasticConfig,
    comparative_metrics,
    optimize_stochastic_immunotherapy,
    particle_filter,
    predictive_quantiles,
    risk_metrics,
    sample_observations,
    simulate_stochastic,
)


def _distribution_table(run, config: StochasticConfig) -> pd.DataFrame:
    total = run.states[:, -1].sum(axis=1)
    escape = np.divide(run.states[:, -1, 1], total, out=np.zeros_like(total), where=total > 0)
    return pd.DataFrame({
        "draw": np.arange(len(total)),
        "terminal_tumor": total,
        "escape_fraction": escape,
        "peak_inflammation": run.immune[:, :, 2].max(axis=1),
        "response": total <= run.states[:, 0].sum(axis=1) * config.response_threshold,
        "escape_dominant": escape >= config.escape_threshold,
        "inflammation_exceeded": run.immune[:, :, 2].max(axis=1) > config.inflammation_limit,
    })


def _clinical_report(summary: dict) -> str:
    treated = summary["optimized_risk"]
    untreated = summary["untreated_risk"]
    comparative = summary["counterfactual_comparison"]
    response_mc = treated["response_probability_mc95"]
    untreated_response_mc = untreated["response_probability_mc95"]
    major_mc = comparative["probability_at_least_50pct_lower_than_untreated_mc95"]
    escape_mc = treated["escape_probability_mc95"]
    inflammation_mc = treated["inflammation_exceedance_probability_mc95"]
    return f"""# Clinical interpretation of the stochastic benchmark

This is a synthetic proof of method, not a patient-calibrated model or treatment recommendation.

Across independent ensemble simulations, the model-selected schedule produced a **{treated['response_probability']:.1%} probability of reaching the modeled regression threshold** (finite-simulation 95% interval **{response_mc[0]:.1%}–{response_mc[1]:.1%}**), compared with **{untreated['response_probability']:.1%}** (**{untreated_response_mc[0]:.1%}–{untreated_response_mc[1]:.1%}**) without treatment. Here, regression means terminal modeled burden at or below {summary['response_definition']}; it is not RECIST response, progression-free survival, or overall survival.

Relative to matched simulated untreated trajectories, median terminal burden was **{comparative['median_terminal_reduction_vs_untreated']:.1%} lower**, and **{comparative['probability_at_least_50pct_lower_than_untreated']:.1%}** of simulations achieved at least a 50% counterfactual reduction (finite-simulation 95% interval **{major_mc[0]:.1%}–{major_mc[1]:.1%}**). This represents modeled treatment effect versus a synthetic counterfactual, not observed clinical benefit. A schedule can substantially slow growth without shrinking disease below its starting burden; those outcomes must not be conflated.

The probability that an immune-escape phenotype constituted at least half of residual disease was **{treated['escape_probability']:.1%}** (finite-simulation 95% interval **{escape_mc[0]:.1%}–{escape_mc[1]:.1%}**). This is a model-based evolutionary-risk signal, not a detected mutation or validated resistant clone. Clinically, it would justify closer longitudinal assessment with imaging, ctDNA, antigen-expression measurements, and immune profiling—not an automatic treatment change.

The probability of crossing the inflammation-proxy bound was **{treated['inflammation_exceedance_probability']:.1%}** (finite-simulation 95% interval **{inflammation_mc[0]:.1%}–{inflammation_mc[1]:.1%}**). The nonzero upper bound matters: observing no crossings in {summary['predictive_draws']} simulations does not establish zero risk. The proxy is neither a CTCAE grade nor an adverse-event probability until calibrated against observed toxicity outcomes. The 90% conditional tail mean of terminal tumor burden was **{treated['terminal_tumor_cvar90']:.3f} normalized units**; this summarizes poor-outcome simulations and is the main quantity constrained by the risk-aware optimizer.

The state estimates combine sparse synthetic imaging, ctDNA, and RNA-module observations through a bootstrap particle filter. Their 90% intervals represent model and process uncertainty conditional on those observations. They do not include every source of clinical uncertainty or establish that this model is correctly specified.

Before prospective use, treatment kernels, random-effect distributions, assay likelihoods, escape transitions, clinical thresholds, and safety constraints must be fitted on training patients, locked, and evaluated on untouched patients and an external cohort. A clinical protocol and independent safety oversight remain required.
"""


def _plot_dashboard(out: Path, schedule: np.ndarray, predictive: pd.DataFrame,
                    filtered: pd.DataFrame, observations: pd.DataFrame,
                    distributions: pd.DataFrame, immune: np.ndarray,
                    config: StochasticConfig, kernels) -> None:
    fig, axes = plt.subplots(3, 2, figsize=(12, 11))
    ax = axes[0, 0]
    ax.fill_between(predictive.day, predictive.tumor_p05, predictive.tumor_p95,
                    color="tab:blue", alpha=.18, label="90% predictive interval")
    ax.plot(predictive.day, predictive.tumor_median, color="tab:blue", label="predictive median")
    ax.errorbar(filtered.loc[filtered.observed, "day"], observations.imaging_burden,
                fmt="o", color="black", label="synthetic imaging")
    ax.plot(filtered.day, filtered.tumor_median, color="tab:orange", label="filtered median")
    ax.set(title="Tumor burden: prediction and filtering", xlabel="day", ylabel="normalized burden")
    ax.legend(fontsize=8)

    ax = axes[0, 1]
    ax.fill_between(predictive.day, predictive.escape_p05, predictive.escape_p95,
                    color="tab:red", alpha=.18, label="90% predictive interval")
    ax.plot(predictive.day, predictive.escape_median, color="tab:red", label="escape median")
    ax.plot(filtered.day, filtered.escape_median, color="tab:purple", label="filtered median")
    ax.axhline(config.escape_threshold, color="gray", ls="--", label="escape threshold")
    ax.set(title="Residual escape composition", xlabel="day", ylabel="escape fraction", ylim=(0, 1))
    ax.legend(fontsize=8)

    ax = axes[1, 0]
    for channel, name in enumerate(["cytotoxic", "exhaustion", "inflammation"]):
        median = np.median(immune[:, :, channel], axis=0)
        low, high = np.quantile(immune[:, :, channel], [.05, .95], axis=0)
        ax.plot(median, label=name); ax.fill_between(range(len(median)), low, high, alpha=.10)
    ax.axhline(config.inflammation_limit, color="tab:red", ls="--", label="inflammation bound")
    ax.set(title="Uncertain latent immune response", xlabel="day", ylabel="normalized activity")
    ax.legend(fontsize=8)

    ax = axes[1, 1]
    ax.scatter(distributions.terminal_tumor, distributions.escape_fraction,
               c=distributions.inflammation_exceeded.astype(int), cmap="coolwarm", alpha=.55, s=18)
    ax.axhline(config.escape_threshold, color="gray", ls="--")
    ax.set(title="Joint outcome risk (red: inflammation bound crossed)",
           xlabel="terminal tumor", ylabel="escape fraction", ylim=(0, 1))

    surface = synergy_surface(kernels)
    ax = axes[2, 0]
    image = ax.imshow(surface, origin="lower", aspect="auto", cmap="viridis")
    ax.set(title="Vaccine × checkpoint Volterra kernel", xlabel="checkpoint lag",
           ylabel="vaccine lag")
    fig.colorbar(image, ax=ax, label="quadratic cytotoxic contribution")

    ax = axes[2, 1]
    for channel, name in enumerate(["vaccine", "checkpoint", "radiation"]):
        ax.step(range(len(schedule)), schedule[:, channel], where="post", label=name)
    ax.set(title="Risk-aware bounded schedule", xlabel="day", ylabel="normalized input")
    ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(out / "stochastic_clinical_dashboard.png", dpi=180); plt.close(fig)


def stochastic_immunotherapy_demo(out: Path, draws: int = 256, particles: int = 384,
                                  maxiter: int = 24, seed: int = 42) -> None:
    system, kernels = reference_immunotherapy_system()
    initial = np.array([.28, .018]); horizon = 42; administration_times = [0, 7, 14, 21]
    optimization_config = StochasticConfig(draws=min(64, draws))
    fit = optimize_stochastic_immunotherapy(
        system, kernels, initial, horizon, administration_times, np.array([1., .8, .7]),
        optimization_config, seed=seed, maxiter=maxiter)
    evaluation_config = StochasticConfig(draws=draws)
    treated = simulate_stochastic(system, kernels, fit["schedule"], initial,
                                  evaluation_config, seed=seed + 20_000)
    untreated_schedule = np.zeros_like(fit["schedule"])
    # Shared seed supplies common random numbers for a lower-variance counterfactual comparison.
    untreated = simulate_stochastic(system, kernels, untreated_schedule, initial,
                                    evaluation_config, seed=seed + 20_000)
    observation_days = [0, 3, 7, 10, 14, 21, 28, 35, 42]
    observations = sample_observations(treated, observation_days, evaluation_config,
                                       draw=0, seed=seed + 40_000)
    filtered = particle_filter(system, kernels, fit["schedule"], initial, observations,
                               evaluation_config, particles=particles, seed=seed + 50_000)
    predictive = predictive_quantiles(treated)
    distributions = _distribution_table(treated, evaluation_config)
    treated_risk = risk_metrics(treated, evaluation_config)
    untreated_risk = risk_metrics(untreated, evaluation_config)
    comparison = comparative_metrics(treated, untreated)
    summary = {
        "status": "synthetic proof of method; not patient-calibrated and not a dosing recommendation",
        "architecture": ["second-order MIMO Volterra treatment operator",
                         "patient random effects and kernel gain uncertainty",
                         "correlated latent immune-process noise",
                         "stochastic birth/death and immune-escape transitions",
                         "log-normal imaging, binomial ctDNA, negative-binomial RNA observations",
                         "multimodal bootstrap particle filtering",
                         "common-random-number CVaR-aware inverse optimization"],
        "treatment_channels": ["vaccine", "checkpoint inhibitor", "radiation"],
        "predictive_draws": draws, "filter_particles": particles,
        "optimizer_success": fit["success"], "optimizer_message": fit["message"],
        "response_definition": "50% of the initial normalized tumor state at day 42",
        "escape_definition": "escape phenotype is at least 50% of residual modeled tumor",
        "optimized_risk": treated_risk, "untreated_risk": untreated_risk,
        "counterfactual_comparison": comparison,
        "clinical_guardrail": "All probabilities are conditional on synthetic assumptions and are not clinical estimates."
    }
    out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(fit["schedule"], columns=["vaccine", "checkpoint", "radiation"]).assign(
        day=np.arange(horizon)).to_csv(out / "risk_aware_schedule.csv", index=False)
    predictive.to_csv(out / "predictive_quantiles.csv", index=False)
    observations.to_csv(out / "synthetic_observations.csv", index=False)
    filtered.to_csv(out / "filtered_state_estimates.csv", index=False)
    distributions.to_csv(out / "outcome_draws.csv", index=False)
    (out / "risk_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (out / "clinical_interpretation.md").write_text(_clinical_report(summary))
    _plot_dashboard(out, fit["schedule"], predictive, filtered, observations,
                    distributions, treated.immune, evaluation_config, kernels)
