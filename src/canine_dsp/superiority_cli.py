"""Locked synthetic benchmark of reduced PK/PD-QSP and QSP–Volterra policies."""

import hashlib
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .policy_benchmark import (build_policies, evaluate_policies, heldout_scenarios,
                               scenario_summary, superiority_analysis)
from .qsp import (protocol_is_feasible, reference_exposure_model,
                  reference_protocol_constraints, simulate_exposure)
from .stochastic_immunotherapy import StochasticConfig


def _hash_json(value: dict) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def _schedule_hash(schedule: np.ndarray) -> str:
    return hashlib.sha256(np.asarray(schedule, dtype="<f8").tobytes()).hexdigest()


def _read_reference_schedule(path: Path, horizon: int) -> np.ndarray:
    table = pd.read_csv(path)
    required = ["day", "vaccine", "checkpoint", "radiation"]
    if any(column not in table for column in required):
        raise ValueError(f"reference schedule must contain {required}")
    if table.day.duplicated().any() or not table.day.between(0, horizon - 1).all():
        raise ValueError("reference schedule days must be unique and inside the horizon")
    schedule = np.zeros((horizon, 3))
    schedule[table.day.astype(int)] = table[["vaccine", "checkpoint", "radiation"]].to_numpy(float)
    if not np.all(np.isfinite(schedule)) or np.any(schedule < 0):
        raise ValueError("reference schedule inputs must be finite and nonnegative")
    return schedule


def _clinical_report(summary: dict) -> str:
    test = summary["primary_comparison"]
    fixed = summary["active_reference_comparison"]
    supported = test["simulation_superiority_supported"]
    conclusion = (
        "met all prespecified synthetic superiority gates" if supported else
        "did not meet every prespecified synthetic superiority gate")
    tumor_change = test["terminal_tumor_relative_improvement"]
    tumor_direction = "lower" if tumor_change >= 0 else "higher"
    escape_change = test["escape_dominance_rate_difference"]
    escape_direction = "higher" if escape_change >= 0 else "lower"
    reference_label = ("fixed-protocol proxy" if
                       summary["active_reference_policy"] == "fixed_protocol_proxy" else
                       "user-supplied active reference")
    reference_result = ("met every synthetic gate" if fixed["simulation_superiority_supported"]
                        else "did not meet every synthetic gate")
    return f"""# Treatment-policy comparison in plain language

The upgraded QSP–Volterra policy **{conclusion}** against the reduced PK/PD virtual-population optimizer. Its estimated relative utility improvement was **{test['relative_utility_improvement']:.1%}** with a scenario-clustered 95% interval of **{test['relative_utility_improvement_cluster_bootstrap95'][0]:.1%} to {test['relative_utility_improvement_cluster_bootstrap95'][1]:.1%}**. It produced lower average modeled loss in **{test['heldout_scenario_win_rate']:.1%}** of untouched distribution-shift scenarios.

The central tradeoff is important: relative to the PK/PD comparator, terminal tumor burden was **{abs(tumor_change):.1%} {tumor_direction}**, while escape-dominance probability was **{abs(escape_change):.1%} {escape_direction}**. The current objective changed immediate tumor control and immune-evasive residual disease in different directions, without demonstrating that the trade was better overall.

Against the {reference_label}, estimated relative utility improvement was **{fixed['relative_utility_improvement']:.1%}**, and the comparison **{reference_result}**. “Utility” combines terminal tumor burden, escape composition, inflammation-bound violations, and normalized exposure. Its weights are synthetic and are not a clinically validated quality-of-life or survival endpoint.

The candidate treatment plan is written to `candidate_treatment_plan.csv`. Values are normalized research inputs, not drug doses. The exposure layer is a reduced PK/target-engagement model, not a full drug-specific QSP platform. The Volterra kernels are synthetic reference kernels, not kernels learned from a combination-immunotherapy trial.

**This result cannot answer whether the plan is superior to today’s clinical care.** The active comparator is a research proxy, not a disease-, biomarker-, and treatment-line-specific standard of care. Clinical status is therefore `{summary['clinical_evidence_status']}` regardless of the synthetic result. Establishing superiority requires a locked external retrospective evaluation followed by a prospective randomized policy-versus-standard-care trial.
"""


def _plot_comparison(out: Path, schedules: dict[str, np.ndarray], outcomes: pd.DataFrame,
                     scenarios: pd.DataFrame, reference_policy: str) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    order = [reference_policy, "qsp_risk_optimized", "qsp_volterra_risk_optimized"]
    labels = [("fixed proxy" if reference_policy == "fixed_protocol_proxy" else "active reference"),
              "PK/PD-QSP", "PK/PD-QSP + Volterra"]
    grouped = outcomes.groupby("policy").utility_loss
    axes[0, 0].boxplot([grouped.get_group(name) for name in order], tick_labels=labels,
                       showfliers=False)
    axes[0, 0].set(title="Locked held-out utility distribution", ylabel="lower is better")
    axes[0, 0].tick_params(axis="x", rotation=18)

    pivot = scenarios.pivot(index="scenario", columns="policy", values="mean_utility_loss")
    relative = 1 - pivot["qsp_volterra_risk_optimized"] / pivot["qsp_risk_optimized"]
    axes[0, 1].bar(relative.index, relative, color=np.where(relative >= 0, "tab:blue", "tab:red"))
    axes[0, 1].axhline(0, color="gray", linewidth=.8)
    axes[0, 1].set(title="Hybrid improvement by untouched shift", ylabel="relative improvement")
    axes[0, 1].tick_params(axis="x", rotation=60)

    safety = outcomes.groupby("policy").inflammation_exceeded.mean().reindex(order)
    escape = outcomes.assign(dominant=lambda frame: frame.escape_fraction >= .5).groupby(
        "policy").dominant.mean().reindex(order)
    x = np.arange(len(order)); width = .36
    axes[1, 0].bar(x - width / 2, safety, width, label="inflammation bound")
    axes[1, 0].bar(x + width / 2, escape, width, label="escape dominance")
    axes[1, 0].set(xticks=x, xticklabels=labels, ylabel="event probability",
                   title="Safety and evolutionary-risk gates")
    axes[1, 0].tick_params(axis="x", rotation=18); axes[1, 0].legend(fontsize=8)

    candidate = schedules["qsp_volterra_risk_optimized"]
    for channel, name in enumerate(["vaccine", "checkpoint", "radiation"]):
        axes[1, 1].step(range(len(candidate)), candidate[:, channel], where="post", label=name)
    axes[1, 1].set(title="Candidate normalized regimen", xlabel="day", ylabel="input")
    axes[1, 1].legend(fontsize=8)
    fig.tight_layout(); fig.savefig(out / "policy_superiority_dashboard.png", dpi=180); plt.close(fig)


def policy_superiority_benchmark(out: Path, draws: int = 96, scenarios: int = 12,
                                 maxiter: int = 18, seed: int = 73,
                                 reference_schedule: Path | None = None) -> None:
    if draws < 8 or scenarios < 4 or maxiter < 1:
        raise ValueError("benchmark requires draws>=8, scenarios>=4, and maxiter>=1")
    horizon = 42; decision_days = [0, 7, 14, 21]; initial = np.array([.28, .018])
    loaded_reference = (_read_reference_schedule(reference_schedule, horizon)
                        if reference_schedule is not None else None)
    plan = {
        "evidence_tier": "synthetic_challenge_benchmark",
        "context_of_use": "method-development comparison for a normalized three-channel regimen",
        "population": "synthetic two-phenotype virtual tumors with PK and biological shifts",
        "decision_days": decision_days, "horizon_days": horizon,
        "primary_estimand": "relative reduction in mean composite loss over held-out scenarios",
        "primary_comparator": "reduced PK/PD first-order virtual-population risk optimizer",
        "candidate": "reduced PK/PD plus second-order Volterra virtual-population risk optimizer",
        "safety_estimand": "difference in inflammation-bound exceedance probability",
        "superiority_rule": "utility lower 95% bound >5%; tumor no worse than 10%; escape and inflammation upper differences <=5%; wins >=75% of shifts",
        "kernel_source": "synthetic_reference",
        "scenario_seed": 2026, "optimization_seed": seed, "evaluation_seed": 80_000,
        "scenario_count": scenarios, "draws_per_scenario": draws,
        "active_reference_source": ("user_supplied_schedule" if reference_schedule else
                                    "built_in_fixed_protocol_proxy"),
    }
    if loaded_reference is not None:
        plan["active_reference_schedule_sha256"] = _schedule_hash(loaded_reference)
    plan["locked_analysis_sha256"] = _hash_json(plan)
    optimization_config = StochasticConfig(draws=min(48, draws))
    schedules, fit = build_policies(horizon, decision_days, initial, optimization_config,
                                    maxiter, seed)
    reference_policy = "fixed_protocol_proxy"
    if reference_schedule is not None:
        reference_policy = "user_active_reference"
        schedules[reference_policy] = loaded_reference
        fit[reference_policy] = {"protocol_feasible": False}
        fit[reference_policy]["protocol_feasible"] = protocol_is_feasible(
            schedules[reference_policy], reference_exposure_model(),
            reference_protocol_constraints(), tolerance=1e-3)
    locked_scenarios = heldout_scenarios(scenarios, plan["scenario_seed"])
    evaluation_config = StochasticConfig(draws=draws)
    outcomes = evaluate_policies(schedules, locked_scenarios, initial, evaluation_config,
                                 plan["evaluation_seed"])
    scenario_table = scenario_summary(outcomes)
    primary = superiority_analysis(outcomes, "qsp_volterra_risk_optimized")
    fixed = superiority_analysis(outcomes, "qsp_volterra_risk_optimized",
                                 reference_policy, seed=607)
    ablation = superiority_analysis(outcomes, "qsp_volterra_risk_optimized",
                                    "volterra_no_pk_ablation", seed=608)
    primary_policies = ["qsp_risk_optimized", "qsp_volterra_risk_optimized"]
    optimizers_valid = all(fit[name].get("success", False) for name in primary_policies)
    protocols_feasible = all(fit[name].get("protocol_feasible", False)
                             for name in primary_policies)
    primary["optimizer_convergence_gate_met"] = optimizers_valid
    primary["protocol_feasibility_gate_met"] = protocols_feasible
    primary["simulation_superiority_supported"] = bool(
        primary["simulation_superiority_supported"] and optimizers_valid and protocols_feasible)
    for comparison, comparator in [(fixed, reference_policy),
                                   (ablation, "volterra_no_pk_ablation")]:
        comparison_converged = (fit["qsp_volterra_risk_optimized"].get("success", False)
                                and fit[comparator].get("success", True))
        comparison_feasible = (fit["qsp_volterra_risk_optimized"]["protocol_feasible"]
                               and fit[comparator]["protocol_feasible"])
        comparison["optimizer_convergence_gate_met"] = bool(comparison_converged)
        comparison["protocol_feasibility_gate_met"] = bool(comparison_feasible)
        comparison["simulation_superiority_supported"] = bool(
            comparison["simulation_superiority_supported"] and comparison_feasible
            and comparison_converged)
    summary = {
        "analysis_plan_sha256": plan["locked_analysis_sha256"],
        "policy_sha256": {name: _schedule_hash(schedule) for name, schedule in schedules.items()},
        "optimizer_fit": fit, "primary_comparison": primary,
        "active_reference_comparison": fixed,
        "no_pk_ablation_comparison": ablation,
        "simulation_evidence_status": ("IN_SILICO_ADVANTAGE" if
                                       primary["simulation_superiority_supported"] else
                                       "NO_IN_SILICO_ADVANTAGE"),
        "clinical_evidence_status": "NOT_EVALUABLE_NO_DISEASE_SPECIFIC_SOC_OR_PROSPECTIVE_TRIAL",
        "clinical_superiority_supported": False,
        "active_reference_policy": reference_policy,
        "required_next_evidence": ["drug- and disease-specific PK/QSP calibration",
                                   "kernels estimated from longitudinal combination data",
                                   "locked external patient/trial validation",
                                   "causal off-policy evaluation with overlap diagnostics",
                                   "silent prospective evaluation",
                                   "randomized policy-versus-standard-care trial"],
    }
    out.mkdir(parents=True, exist_ok=True)
    (out / "locked_analysis_plan.json").write_text(json.dumps(plan, indent=2) + "\n")
    (out / "superiority_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    outcomes.to_csv(out / "heldout_policy_outcomes.csv", index=False)
    scenario_table.to_csv(out / "heldout_scenario_summary.csv", index=False)
    schedule_rows = []
    for policy, schedule in schedules.items():
        for day, doses in enumerate(schedule):
            schedule_rows.append({"policy": policy, "day": day, "vaccine": doses[0],
                                  "checkpoint": doses[1], "radiation": doses[2]})
    pd.DataFrame(schedule_rows).to_csv(out / "all_policy_schedules.csv", index=False)
    candidate = schedules["qsp_volterra_risk_optimized"]
    exposure = simulate_exposure(candidate, reference_exposure_model())
    pd.DataFrame(candidate, columns=["vaccine", "checkpoint", "radiation"]).assign(
        day=np.arange(horizon)).to_csv(out / "candidate_treatment_plan.csv", index=False)
    exposure_rows = []
    for day in range(horizon):
        for channel, name in enumerate(["vaccine", "checkpoint", "radiation"]):
            exposure_rows.append({"day": day, "channel": name,
                                  "plasma": exposure.plasma[day, channel],
                                  "tumor": exposure.tumor[day, channel],
                                  "effective_input": exposure.effective_input[day, channel]})
    pd.DataFrame(exposure_rows).to_csv(out / "candidate_exposure.csv", index=False)
    (out / "clinical_interpretation.md").write_text(_clinical_report(summary))
    _plot_comparison(out, schedules, outcomes, scenario_table, reference_policy)
