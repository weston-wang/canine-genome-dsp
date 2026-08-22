"""Fail-closed off-policy evaluation for logged longitudinal treatment decisions."""

from dataclasses import dataclass

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = ["patient", "step", "reward", "behavior_probability",
                    "target_probability", "q_logged", "v_next", "v_initial"]


@dataclass(frozen=True)
class OPEThresholds:
    min_behavior_probability: float = .02
    min_effective_sample_size: float = 30
    max_importance_weight: float = 50
    max_relative_estimator_disagreement: float = .25


def _trajectory_values(table: pd.DataFrame, gamma: float) -> pd.DataFrame:
    rows = []
    for patient, trajectory in table.groupby("patient"):
        trajectory = trajectory.sort_values("step")
        ratio = trajectory.target_probability.to_numpy(float) / trajectory.behavior_probability.to_numpy(float)
        cumulative = np.cumprod(ratio)
        discount = gamma ** np.arange(len(trajectory))
        reward = trajectory.reward.to_numpy(float)
        q_value = trajectory.q_logged.to_numpy(float)
        next_value = trajectory.v_next.to_numpy(float)
        behavior_return = float(np.sum(discount * reward))
        pdis = float(np.sum(discount * cumulative * reward))
        correction = reward + gamma * next_value - q_value
        sdr = float(trajectory.v_initial.iloc[0] + np.sum(discount * cumulative * correction))
        rows.append({"patient": patient, "behavior_return": behavior_return,
                     "pdis": pdis, "sdr": sdr, "final_weight": cumulative[-1],
                     "max_weight": cumulative.max()})
    return pd.DataFrame(rows)


def _snips(table: pd.DataFrame, gamma: float) -> float:
    weighted = 0.0
    table = table.sort_values(["patient", "step"]).copy()
    table["ratio"] = table.target_probability / table.behavior_probability
    table["cumulative_weight"] = table.groupby("patient").ratio.cumprod()
    for step, rows in table.groupby("step"):
        denominator = rows.cumulative_weight.sum()
        if denominator > 0:
            weighted += gamma ** int(step) * float(
                np.sum(rows.cumulative_weight * rows.reward) / denominator)
    return weighted


def _bootstrap_improvement(values: pd.DataFrame, seed: int,
                           repetitions: int = 2_000) -> list[float]:
    rng = np.random.default_rng(seed); n = len(values); samples = np.zeros(repetitions)
    sdr = values.sdr.to_numpy(); behavior = values.behavior_return.to_numpy()
    for iteration in range(repetitions):
        selected = rng.integers(0, n, n)
        samples[iteration] = np.mean(sdr[selected] - behavior[selected])
    return [float(value) for value in np.quantile(samples, [.025, .975])]


def evaluate_logged_policy(table: pd.DataFrame, thresholds: OPEThresholds = OPEThresholds(),
                           gamma: float = 1.0, cross_fitted_nuisance: bool = False,
                           seed: int = 909) -> dict:
    """Triangulate PDIS, SNIPS, and sequential DR; abstain on weak causal diagnostics."""
    missing = [column for column in REQUIRED_COLUMNS if column not in table]
    if missing:
        raise ValueError(f"logged policy table is missing columns: {missing}")
    if not 0 < gamma <= 1:
        raise ValueError("gamma must lie in (0, 1]")
    values = table[REQUIRED_COLUMNS].copy()
    numeric = [column for column in REQUIRED_COLUMNS if column != "patient"]
    if not np.isfinite(values[numeric].to_numpy(float)).all():
        raise ValueError("logged policy inputs must be finite")
    if (np.any(values.behavior_probability <= 0) or np.any(values.behavior_probability > 1)
            or np.any(values.target_probability < 0) or np.any(values.target_probability > 1)):
        raise ValueError("logged-action probabilities must lie in (0,1] for behavior and [0,1] for target")
    if values.duplicated(["patient", "step"]).any() or np.any(values.step < 0):
        raise ValueError("patient-step rows must be unique and steps nonnegative")
    trajectories = _trajectory_values(values, gamma)
    pdis = float(trajectories.pdis.mean()); snips = float(_snips(values, gamma))
    sdr = float(trajectories.sdr.mean()); behavior = float(trajectories.behavior_return.mean())
    weights = trajectories.final_weight.to_numpy()
    ess = float(np.square(weights.sum()) / np.square(weights).sum()) if np.any(weights) else 0.0
    unsupported = ((values.target_probability > 0)
                   & (values.behavior_probability < thresholds.min_behavior_probability))
    overlap_fraction = float(1 - unsupported.mean())
    scale = max(abs(sdr), abs(behavior), 1e-8)
    disagreement = float((max(pdis, snips, sdr) - min(pdis, snips, sdr)) / scale)
    improvement = sdr - behavior
    improvement_ci = _bootstrap_improvement(trajectories, seed)
    if not cross_fitted_nuisance:
        status = "NOT_EVALUABLE_NUISANCE_NOT_CROSS_FITTED"
    elif unsupported.any():
        status = "NOT_EVALUABLE_NO_OVERLAP"
    elif ess < thresholds.min_effective_sample_size:
        status = "NOT_EVALUABLE_LOW_EFFECTIVE_SAMPLE_SIZE"
    elif trajectories.max_weight.max() > thresholds.max_importance_weight:
        status = "NOT_EVALUABLE_EXTREME_WEIGHTS"
    elif disagreement > thresholds.max_relative_estimator_disagreement:
        status = "NOT_EVALUABLE_ESTIMATOR_DISAGREEMENT"
    elif improvement_ci[0] > 0:
        status = "RETROSPECTIVE_CAUSAL_ESTIMATE"
    else:
        status = "NO_RETROSPECTIVE_ADVANTAGE"
    return {
        "evidence_status": status,
        "patients": int(values.patient.nunique()),
        "decisions": int(len(values)), "gamma": gamma,
        "behavior_policy_value": behavior, "pdis_target_value": pdis,
        "snips_target_value": snips, "sequential_dr_target_value": sdr,
        "sequential_dr_improvement": float(improvement),
        "sequential_dr_improvement_patient_bootstrap95": improvement_ci,
        "effective_sample_size": ess,
        "minimum_required_effective_sample_size": thresholds.min_effective_sample_size,
        "action_overlap_fraction": overlap_fraction,
        "maximum_importance_weight": float(trajectories.max_weight.max()),
        "relative_estimator_disagreement": disagreement,
        "cross_fitted_nuisance": bool(cross_fitted_nuisance),
        "causal_assumptions": ["consistency", "sequential exchangeability",
                               "positivity", "correctly cross-fitted nuisance estimates"],
        "clinical_superiority_supported": False,
        "interpretation": "At most a retrospective causal estimate; prospective randomization is required for clinical superiority."
    }
