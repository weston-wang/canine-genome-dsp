"""Blinded simulation benchmark for QSP and QSP–Volterra treatment policies."""

from dataclasses import dataclass, replace

import numpy as np
import pandas as pd

from .evolution import ImmuneKernels
from .immunotherapy import ImmunotherapySystem, reference_immunotherapy_system
from .qsp import (ExposureModel, perturb_exposure, protocol_is_feasible,
                  reference_exposure_model, reference_protocol_constraints)
from .stochastic_immunotherapy import (
    StochasticConfig,
    optimize_stochastic_immunotherapy,
    simulate_stochastic,
)


@dataclass(frozen=True)
class BenchmarkScenario:
    name: str
    system: ImmunotherapySystem
    kernels: ImmuneKernels
    exposure: ExposureModel


def _scaled_kernels(kernels: ImmuneKernels, first_order: np.ndarray,
                    second_order: float) -> ImmuneKernels:
    h1 = np.asarray(kernels.h1) * np.asarray(first_order)[:, None, None]
    h2 = None if kernels.h2 is None else np.asarray(kernels.h2) * second_order
    return ImmuneKernels(h1, h2)


def heldout_scenarios(count: int = 12, seed: int = 2026) -> list[BenchmarkScenario]:
    """Generate locked distribution shifts not exposed to either optimizer."""
    base_system, base_kernels = reference_immunotherapy_system()
    base_exposure = reference_exposure_model()
    rng = np.random.default_rng(seed)
    scenarios = []
    for index in range(count):
        growth = base_system.growth * rng.lognormal(0, .13, 2)
        killing = base_system.cytotoxic_kill * rng.lognormal(0, .18, 2)
        transition = base_system.transition * float(rng.lognormal(0, .35))
        system = replace(base_system, growth=growth, cytotoxic_kill=killing,
                         transition=transition)
        exposure = perturb_exposure(base_exposure, rng, .20)
        output_gain = rng.lognormal(0, .12, 3)
        interaction_scale = float(rng.lognormal(-.08, .35))
        # Two prespecified structural stress tests remove learned combination synergy.
        if index in {count - 2, count - 1}:
            interaction_scale = 0.0
        kernels = _scaled_kernels(base_kernels, output_gain, interaction_scale)
        scenarios.append(BenchmarkScenario(f"shift_{index + 1:02d}", system, kernels, exposure))
    return scenarios


def fixed_protocol(horizon: int, administration_times: list[int]) -> np.ndarray:
    """Protocol-level fixed-schedule proxy; not a named clinical standard of care."""
    schedule = np.zeros((horizon, 3))
    schedule[administration_times] = np.array([.75, .60, .45])
    return schedule


def _first_order_only(kernels: ImmuneKernels) -> ImmuneKernels:
    return ImmuneKernels(np.asarray(kernels.h1).copy(), None)


def build_policies(horizon: int, administration_times: list[int], initial: np.ndarray,
                   config: StochasticConfig, maxiter: int, seed: int) -> tuple[dict, dict]:
    """Fit all policies only on the nominal development model."""
    system, kernels = reference_immunotherapy_system()
    exposure = reference_exposure_model()
    constraints = reference_protocol_constraints()
    bounds = np.array([1., .8, .7])
    qsp = optimize_stochastic_immunotherapy(
        system, _first_order_only(kernels), initial, horizon, administration_times,
        bounds, config, seed=seed, maxiter=maxiter, exposure_model=exposure,
        protocol_constraints=constraints)
    hybrid = optimize_stochastic_immunotherapy(
        system, kernels, initial, horizon, administration_times, bounds, config,
        seed=seed, maxiter=maxiter, exposure_model=exposure,
        protocol_constraints=constraints)
    volterra_only = optimize_stochastic_immunotherapy(
        system, kernels, initial, horizon, administration_times, bounds, config,
        seed=seed, maxiter=maxiter)
    policies = {"fixed_protocol_proxy": fixed_protocol(horizon, administration_times),
                "qsp_risk_optimized": qsp["schedule"],
                "volterra_no_pk_ablation": volterra_only["schedule"],
                "qsp_volterra_risk_optimized": hybrid["schedule"]}
    fit = {"qsp_risk_optimized": {"success": qsp["success"], "message": qsp["message"]},
           "qsp_volterra_risk_optimized": {"success": hybrid["success"],
                                           "message": hybrid["message"]},
           "volterra_no_pk_ablation": {"success": volterra_only["success"],
                                        "message": volterra_only["message"]}}
    for name, schedule in policies.items():
        fit.setdefault(name, {})["protocol_feasible"] = protocol_is_feasible(
            schedule, exposure, constraints, tolerance=1e-3)
    return policies, fit


def _outcome_rows(scenario: BenchmarkScenario, policy: str, schedule: np.ndarray,
                  initial: np.ndarray, config: StochasticConfig, seed: int) -> list[dict]:
    run = simulate_stochastic(scenario.system, scenario.kernels, schedule, initial, config,
                              seed, scenario.exposure)
    terminal = run.states[:, -1].sum(axis=1)
    escape = np.divide(run.states[:, -1, 1], terminal, out=np.zeros_like(terminal),
                       where=terminal > 0)
    inflammation = run.immune[:, :, 2].max(axis=1)
    excess = np.maximum(inflammation - config.inflammation_limit, 0)
    dose_cost = .006 * np.square(schedule).sum()
    utility_loss = terminal + .75 * escape + 5 * np.square(excess) + dose_cost
    return [{"scenario": scenario.name, "policy": policy, "draw": draw,
             "terminal_tumor": float(terminal[draw]), "escape_fraction": float(escape[draw]),
             "peak_inflammation": float(inflammation[draw]),
             "inflammation_exceeded": bool(inflammation[draw] > config.inflammation_limit),
             "utility_loss": float(utility_loss[draw])} for draw in range(config.draws)]


def evaluate_policies(policies: dict[str, np.ndarray], scenarios: list[BenchmarkScenario],
                      initial: np.ndarray, config: StochasticConfig,
                      seed: int = 80_000) -> pd.DataFrame:
    """Evaluate locked schedules with common random numbers on untouched model shifts."""
    rows = []
    for scenario_index, scenario in enumerate(scenarios):
        scenario_seed = seed + 1_000 * scenario_index
        for name, schedule in policies.items():
            rows.extend(_outcome_rows(scenario, name, schedule, initial, config, scenario_seed))
    return pd.DataFrame(rows)


def _paired_matrix(outcomes: pd.DataFrame, candidate: str, comparator: str,
                   column: str) -> tuple[np.ndarray, np.ndarray]:
    table = outcomes.pivot(index=["scenario", "draw"], columns="policy", values=column)
    scenarios = table.index.get_level_values("scenario").unique()
    candidate_values = np.stack([table.xs(name, level="scenario")[candidate].to_numpy()
                                 for name in scenarios])
    comparator_values = np.stack([table.xs(name, level="scenario")[comparator].to_numpy()
                                  for name in scenarios])
    return candidate_values, comparator_values


def _cluster_bootstrap_improvement(candidate: np.ndarray, comparator: np.ndarray,
                                   seed: int, repetitions: int = 2_000) -> tuple[float, list[float]]:
    """Relative paired improvement, resampling scenarios and virtual patients."""
    rng = np.random.default_rng(seed)
    scenario_count, draws = candidate.shape
    samples = np.zeros(repetitions)
    for iteration in range(repetitions):
        scenario_index = rng.integers(0, scenario_count, scenario_count)
        candidate_sample, comparator_sample = [], []
        for scenario in scenario_index:
            draw_index = rng.integers(0, draws, draws)
            candidate_sample.append(candidate[scenario, draw_index])
            comparator_sample.append(comparator[scenario, draw_index])
        candidate_mean = np.concatenate(candidate_sample).mean()
        comparator_mean = np.concatenate(comparator_sample).mean()
        samples[iteration] = (comparator_mean - candidate_mean) / comparator_mean
    estimate = float((comparator.mean() - candidate.mean()) / comparator.mean())
    return estimate, [float(value) for value in np.quantile(samples, [.025, .975])]


def _cluster_bootstrap_difference(candidate: np.ndarray, comparator: np.ndarray,
                                  seed: int, repetitions: int = 2_000) -> tuple[float, list[float]]:
    rng = np.random.default_rng(seed)
    scenario_count, draws = candidate.shape
    samples = np.zeros(repetitions)
    for iteration in range(repetitions):
        scenario_index = rng.integers(0, scenario_count, scenario_count)
        values = []
        for scenario in scenario_index:
            draw_index = rng.integers(0, draws, draws)
            values.append(candidate[scenario, draw_index] - comparator[scenario, draw_index])
        samples[iteration] = np.concatenate(values).mean()
    estimate = float((candidate - comparator).mean())
    return estimate, [float(value) for value in np.quantile(samples, [.025, .975])]


def superiority_analysis(outcomes: pd.DataFrame, candidate: str,
                         comparator: str = "qsp_risk_optimized",
                         safety_margin: float = .05, escape_margin: float = .05,
                         tumor_noninferiority_margin: float = .10,
                         minimum_utility_improvement: float = .05,
                         seed: int = 606) -> dict:
    """Prespecified simulation-superiority and safety-noninferiority decision rule."""
    candidate_loss, comparator_loss = _paired_matrix(
        outcomes, candidate, comparator, "utility_loss")
    improvement, improvement_ci = _cluster_bootstrap_improvement(
        candidate_loss, comparator_loss, seed)
    candidate_tumor, comparator_tumor = _paired_matrix(
        outcomes, candidate, comparator, "terminal_tumor")
    tumor_improvement, tumor_improvement_ci = _cluster_bootstrap_improvement(
        candidate_tumor, comparator_tumor, seed + 1)
    candidate_safety, comparator_safety = _paired_matrix(
        outcomes, candidate, comparator, "inflammation_exceeded")
    safety_difference_estimate, safety_difference_ci = _cluster_bootstrap_difference(
        candidate_safety.astype(float), comparator_safety.astype(float), seed + 2)
    candidate_escape, comparator_escape = _paired_matrix(
        outcomes.assign(escape_dominant=outcomes.escape_fraction >= .5),
        candidate, comparator, "escape_dominant")
    escape_difference, escape_difference_ci = _cluster_bootstrap_difference(
        candidate_escape.astype(float), comparator_escape.astype(float), seed + 3)
    scenario_loss = outcomes.groupby(["scenario", "policy"]).utility_loss.mean().unstack()
    scenario_win_rate = float(np.mean(scenario_loss[candidate] < scenario_loss[comparator]))
    efficacy_superior = improvement_ci[0] > 0
    meaningful_improvement = improvement_ci[0] > minimum_utility_improvement
    tumor_noninferior = tumor_improvement_ci[0] >= -tumor_noninferiority_margin
    safety_noninferior = safety_difference_ci[1] <= safety_margin
    escape_noninferior = escape_difference_ci[1] <= escape_margin
    robust_across_shifts = scenario_win_rate >= .75
    return {
        "candidate": candidate, "comparator": comparator,
        "relative_utility_improvement": improvement,
        "relative_utility_improvement_cluster_bootstrap95": improvement_ci,
        "minimum_meaningful_relative_utility_improvement": minimum_utility_improvement,
        "terminal_tumor_relative_improvement": tumor_improvement,
        "terminal_tumor_relative_improvement_cluster_bootstrap95": tumor_improvement_ci,
        "terminal_tumor_noninferiority_margin": tumor_noninferiority_margin,
        "inflammation_exceedance_rate_difference": safety_difference_estimate,
        "inflammation_difference_cluster_bootstrap95": safety_difference_ci,
        "prespecified_safety_margin": safety_margin,
        "escape_dominance_rate_difference": escape_difference,
        "escape_difference_cluster_bootstrap95": escape_difference_ci,
        "prespecified_escape_margin": escape_margin,
        "heldout_scenario_win_rate": scenario_win_rate,
        "efficacy_superiority_criterion_met": bool(efficacy_superior),
        "minimum_meaningful_improvement_criterion_met": bool(meaningful_improvement),
        "tumor_noninferiority_criterion_met": bool(tumor_noninferior),
        "safety_noninferiority_criterion_met": bool(safety_noninferior),
        "escape_noninferiority_criterion_met": bool(escape_noninferior),
        "distribution_shift_robustness_criterion_met": bool(robust_across_shifts),
        "simulation_superiority_supported": bool(
            efficacy_superior and meaningful_improvement and tumor_noninferior
            and safety_noninferior and escape_noninferior and robust_across_shifts),
        "clinical_superiority_established": False,
        "claim_scope": "A positive result applies only to this locked synthetic benchmark.",
    }


def scenario_summary(outcomes: pd.DataFrame) -> pd.DataFrame:
    return outcomes.groupby(["scenario", "policy"], as_index=False).agg(
        mean_utility_loss=("utility_loss", "mean"),
        median_terminal_tumor=("terminal_tumor", "median"),
        escape_probability=("escape_fraction", lambda value: float(np.mean(value >= .5))),
        inflammation_exceedance_probability=("inflammation_exceeded", "mean"),
    )
