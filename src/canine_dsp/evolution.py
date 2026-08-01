"""Hybrid tumor-clone evolution and nonlinear vaccine response models."""

from dataclasses import dataclass, replace

import numpy as np


@dataclass(frozen=True)
class EvolutionModel:
    growth: np.ndarray
    antigen_expression: np.ndarray
    presentation: np.ndarray
    mutation: np.ndarray
    carrying_capacity: float = 1.0
    immune_kill: float = 1.0
    dt: float = 1.0

    def __post_init__(self):
        clones, antigens = np.asarray(self.antigen_expression).shape
        if np.asarray(self.growth).shape != (clones,):
            raise ValueError("growth must contain one value per clone")
        if np.asarray(self.presentation).shape != (clones, antigens):
            raise ValueError("presentation must match antigen_expression")
        mutation = np.asarray(self.mutation)
        if mutation.shape != (clones, clones) or np.any(mutation < 0):
            raise ValueError("mutation must be a nonnegative clone-by-clone matrix")
        if not np.allclose(mutation.sum(axis=1), 1):
            raise ValueError("mutation rows must sum to one")


@dataclass(frozen=True)
class ImmuneKernels:
    h1: np.ndarray  # response antigen x input channel x lag
    h2: np.ndarray | None = None  # response antigen x input x input x lag x lag


def volterra_response(inputs: np.ndarray, kernels: ImmuneKernels) -> np.ndarray:
    """Evaluate causal first/second-order kernels for a treatment schedule."""
    inputs = np.asarray(inputs, float)
    antigens, channels, memory = kernels.h1.shape
    if inputs.ndim != 2 or inputs.shape[1] != channels:
        raise ValueError("input schedule has the wrong number of channels")
    response = np.zeros((len(inputs), antigens))
    for t in range(len(inputs)):
        for lag in range(min(memory, t + 1)):
            response[t] += kernels.h1[:, :, lag] @ inputs[t - lag]
        if kernels.h2 is not None:
            for lag1 in range(min(memory, t + 1)):
                for lag2 in range(min(memory, t + 1)):
                    response[t] += np.einsum(
                        "aij,i,j->a", kernels.h2[:, :, :, lag1, lag2],
                        inputs[t - lag1], inputs[t - lag2]
                    )
    return np.maximum(response, 0)


def simulate_evolution(
    model: EvolutionModel,
    initial: np.ndarray,
    immune_response: np.ndarray,
) -> np.ndarray:
    """Simulate density-dependent clone growth, immune killing, and mutation."""
    initial = np.asarray(initial, float)
    state = np.zeros((len(immune_response) + 1, len(initial)))
    state[0] = initial
    visibility = np.asarray(model.antigen_expression) * np.asarray(model.presentation)
    for t, immunity in enumerate(np.asarray(immune_response, float)):
        current = state[t]
        density = current.sum() / model.carrying_capacity
        killing = model.immune_kill * (visibility @ immunity)
        net = np.asarray(model.growth) * (1 - density) - killing
        grown = current * np.exp(np.clip(model.dt * net, -30, 30))
        state[t + 1] = grown @ np.asarray(model.mutation)
    return state


def perturb_model(model: EvolutionModel, growth_scale: float = 0.1,
                  kill_scale: float = 0.1, rng: np.random.Generator | None = None) -> EvolutionModel:
    """Draw a nearby model for robust-control uncertainty scenarios."""
    rng = rng or np.random.default_rng()
    growth = np.maximum(0, model.growth * rng.lognormal(0, growth_scale, len(model.growth)))
    immune_kill = model.immune_kill * float(rng.lognormal(0, kill_scale))
    return replace(model, growth=growth, immune_kill=immune_kill)

