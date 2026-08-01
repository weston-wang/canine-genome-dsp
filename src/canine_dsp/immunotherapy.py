"""Mechanistically bounded Volterra model for combination immunotherapy scheduling."""

from dataclasses import dataclass, replace

import numpy as np
from scipy.optimize import differential_evolution

from .evolution import ImmuneKernels, volterra_response


@dataclass(frozen=True)
class ImmunotherapySystem:
    """Two tumor phenotypes driven by cytotoxic, exhaustion, and inflammatory outputs."""

    growth: np.ndarray
    carrying_capacity: float = 1.5
    cytotoxic_kill: np.ndarray = None
    inflammation_kill: float = 0.04
    transition: float = 0.001

    def __post_init__(self):
        if self.cytotoxic_kill is None:
            object.__setattr__(self, "cytotoxic_kill", np.array([0.24, 0.055]))
        if np.asarray(self.growth).shape != (2,) or np.asarray(self.cytotoxic_kill).shape != (2,):
            raise ValueError("growth and cytotoxic_kill must describe sensitive and escape states")


def simulate_immunotherapy(system: ImmunotherapySystem, immune: np.ndarray,
                           initial: np.ndarray) -> np.ndarray:
    """Simulate bounded sensitive/escape tumor states; immune columns are CTL/exhaustion/inflammation."""
    state = np.zeros((len(immune) + 1, 2)); state[0] = initial
    for t, (cytotoxic, exhaustion, inflammation) in enumerate(immune):
        current = state[t]
        effective = cytotoxic / (1.0 + max(0.0, exhaustion))
        net = system.growth * (1 - current.sum() / system.carrying_capacity)
        net -= system.cytotoxic_kill * effective + system.inflammation_kill * inflammation
        grown = current * np.exp(np.clip(net, -20, 20))
        moved = system.transition * grown[0]
        state[t + 1] = [max(0, grown[0] - moved), max(0, grown[1] + moved)]
    return state


def reference_immunotherapy_system() -> tuple[ImmunotherapySystem, ImmuneKernels]:
    """Synthetic but biologically shaped vaccine/checkpoint/radiation response operator."""
    memory = 10
    decay = np.exp(-np.arange(memory) / 3.2)
    delayed = np.r_[0, decay[:-1]]
    h1 = np.zeros((3, 3, memory))
    # Outputs: cytotoxic activity, exhaustion, systemic inflammation.
    h1[0, 0] = .55 * delayed; h1[0, 1] = .30 * decay; h1[0, 2] = .22 * delayed
    h1[1, 0] = .11 * delayed; h1[1, 1] = -.06 * decay; h1[1, 2] = .08 * delayed
    h1[2, 0] = .10 * decay; h1[2, 1] = .08 * decay; h1[2, 2] = .35 * decay
    h2 = np.zeros((3, 3, 3, memory, memory))
    synergy = np.outer(delayed, decay)
    h2[0, 0, 1] = .12 * synergy       # vaccine followed/covered by checkpoint blockade
    h2[0, 1, 0] = .12 * synergy.T
    h2[0, 2, 0] = .07 * synergy       # radiation antigen release with vaccination
    h2[0, 0, 2] = .07 * synergy.T
    for channel in range(3):
        h2[1, channel, channel] = .025 * np.outer(decay, decay)
        h2[2, channel, channel] = .035 * np.outer(decay, decay)
    return ImmunotherapySystem(np.array([.105, .085])), ImmuneKernels(h1, h2)


def perturb_system(system: ImmunotherapySystem, rng: np.random.Generator) -> ImmunotherapySystem:
    return replace(system,
                   growth=system.growth * rng.lognormal(0, .10, 2),
                   cytotoxic_kill=system.cytotoxic_kill * rng.lognormal(0, .15, 2),
                   transition=system.transition * float(rng.lognormal(0, .25)))


def optimize_immunotherapy(systems: list[ImmunotherapySystem], kernels: ImmuneKernels,
                           initial: np.ndarray, horizon: int, administration_times: list[int],
                           max_dose: np.ndarray, toxicity_limit: float = 1.0,
                           maxiter: int = 60, seed: int = 42) -> dict:
    """Robust inverse schedule with a soft inflammatory-toxicity constraint."""
    channels = kernels.h1.shape[1]
    bounds = [(0.0, float(bound)) for _ in administration_times for bound in max_dose]

    def unpack(vector):
        schedule = np.zeros((horizon, channels))
        schedule[administration_times] = np.asarray(vector).reshape(len(administration_times), channels)
        return schedule

    def score(vector):
        schedule = unpack(vector); immune = volterra_response(schedule, kernels)
        burden = []
        for system in systems:
            states = simulate_immunotherapy(system, immune, initial)
            escape = states[-1, 1] / max(states[-1].sum(), np.finfo(float).eps)
            burden.append(states[-1].sum() + .3 * states.sum(axis=1).max() + .8 * escape)
        toxicity = np.maximum(immune[:, 2] - toxicity_limit, 0)
        return max(burden) + 4 * np.square(toxicity).sum() + .006 * np.square(schedule).sum()

    fit = differential_evolution(score, bounds, seed=seed, maxiter=maxiter, popsize=8,
                                 tol=.02, polish=True)
    schedule = unpack(fit.x); immune = volterra_response(schedule, kernels)
    states = np.stack([simulate_immunotherapy(system, immune, initial) for system in systems])
    return {"schedule": schedule, "immune": immune, "states": states,
            "objective": float(fit.fun), "success": bool(fit.success), "message": str(fit.message),
            "toxicity_limit": toxicity_limit}


def synergy_surface(kernels: ImmuneKernels) -> np.ndarray:
    """Vaccine/checkpoint contribution to cytotoxic output by their relative lags."""
    return kernels.h2[0, 0, 1] + kernels.h2[0, 1, 0].T
