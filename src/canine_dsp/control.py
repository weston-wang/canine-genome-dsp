"""Robust inverse vaccine design for the hybrid evolutionary model."""

from dataclasses import dataclass

import numpy as np
from scipy.optimize import differential_evolution

from .evolution import EvolutionModel, ImmuneKernels, simulate_evolution, volterra_response


@dataclass(frozen=True)
class ControlWeights:
    terminal_tumor: float = 1.0
    escape_fraction: float = 2.0
    dose: float = 0.01
    peak_tumor: float = 0.25


def trajectory_cost(states: np.ndarray, schedule: np.ndarray, escape_clones: np.ndarray,
                    weights: ControlWeights) -> float:
    total = states.sum(axis=1)
    terminal_escape = states[-1, escape_clones].sum() / max(total[-1], np.finfo(float).eps)
    return float(weights.terminal_tumor * total[-1] + weights.peak_tumor * total.max()
                 + weights.escape_fraction * terminal_escape + weights.dose * np.square(schedule).sum())


def optimize_vaccine(
    models: list[EvolutionModel],
    kernels: ImmuneKernels,
    initial: np.ndarray,
    horizon: int,
    administration_times: list[int],
    max_dose: np.ndarray,
    escape_clones: np.ndarray,
    weights: ControlWeights = ControlWeights(),
    seed: int = 42,
    maxiter: int = 80,
) -> dict:
    """Minimize worst-scenario cost over bounded antigen doses at fixed administration times."""
    channels = kernels.h1.shape[1]
    max_dose = np.asarray(max_dose, float)
    if max_dose.shape != (channels,):
        raise ValueError("max_dose must contain one bound per input channel")
    bounds = [(0.0, float(bound)) for _ in administration_times for bound in max_dose]

    def unpack(vector: np.ndarray) -> np.ndarray:
        schedule = np.zeros((horizon, channels))
        schedule[administration_times] = vector.reshape(len(administration_times), channels)
        return schedule

    def objective(vector: np.ndarray) -> float:
        schedule = unpack(vector)
        response = volterra_response(schedule, kernels)
        costs = [trajectory_cost(simulate_evolution(model, initial, response), schedule,
                                 escape_clones, weights) for model in models]
        return max(costs)

    result = differential_evolution(objective, bounds, seed=seed, maxiter=maxiter,
                                    polish=True, updating="immediate")
    schedule = unpack(result.x)
    response = volterra_response(schedule, kernels)
    trajectories = np.stack([simulate_evolution(model, initial, response) for model in models])
    return {"schedule": schedule, "immune_response": response, "trajectories": trajectories,
            "worst_cost": float(result.fun), "success": bool(result.success),
            "message": result.message}

