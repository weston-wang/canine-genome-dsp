"""Research-only species-aware Volterra hidden semi-Markov model.

The implementation uses an explicit elapsed-duration state, which makes the
probability of leaving a biological state depend on how long it has been
occupied.  Intervention histories enter the conditional destination logits
through bounded first-order and low-rank second-order Volterra terms.

The reference parameters are illustrative normalized-scale priors for method
development.  They are not fitted clinical parameters and the outputs are not
treatment recommendations.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Mapping, Sequence

import numpy as np
from scipy.special import logsumexp


class OsteosarcomaState(str, Enum):
    """Named latent states used by the comparative research model."""

    NED_MRD = "NED_MRD"
    INNATE_PRIMED = "INNATE_PRIMED"
    ADAPTIVE_CONTROL = "ADAPTIVE_CONTROL"
    OCCULT_ESCAPE = "OCCULT_ESCAPE"
    VISIBLE_RELAPSE = "VISIBLE_RELAPSE"
    EXHAUSTED = "EXHAUSTED"


class Species(str, Enum):
    """Species supported by the comparative model."""

    DOG = "dog"
    HUMAN = "human"


STATE_ORDER = tuple(OsteosarcomaState)
N_STATES = len(STATE_ORDER)


def _readonly_float_array(value: np.ndarray | Sequence[float], name: str) -> np.ndarray:
    array = np.array(value, dtype=float, copy=True)
    if np.isnan(array).any() or np.isposinf(array).any():
        raise ValueError(f"{name} must not contain NaN or positive infinity")
    array.setflags(write=False)
    return array


def _as_species(value: Species | str) -> Species:
    if isinstance(value, Species):
        return value
    try:
        return Species(str(value).lower())
    except ValueError as error:
        choices = ", ".join(species.value for species in Species)
        raise ValueError(f"species must be one of: {choices}") from error


@dataclass(frozen=True)
class VolterraTransitionKernels:
    """Bounded low-rank Volterra kernels for conditional transition logits.

    ``first_order`` has shape ``(state, destination, lag, input)``.  The two
    second-order factors have shape
    ``(state, destination, rank, lag, input)``.  Their projected history
    products form a rank-limited quadratic kernel.
    """

    input_names: tuple[str, ...]
    first_order: np.ndarray
    second_left: np.ndarray
    second_right: np.ndarray
    input_scale: np.ndarray
    logit_bound: float = 2.5

    def __post_init__(self) -> None:
        names = tuple(str(name) for name in self.input_names)
        first = _readonly_float_array(self.first_order, "first_order")
        left = _readonly_float_array(self.second_left, "second_left")
        right = _readonly_float_array(self.second_right, "second_right")
        scale = _readonly_float_array(self.input_scale, "input_scale")

        if not names or any(not name for name in names) or len(set(names)) != len(names):
            raise ValueError("input_names must be non-empty and unique")
        if first.ndim != 4 or first.shape[:2] != (N_STATES, N_STATES):
            raise ValueError(
                f"first_order must have shape ({N_STATES}, {N_STATES}, memory, inputs)"
            )
        if first.shape[2] < 1 or first.shape[3] != len(names):
            raise ValueError("first_order memory must be positive and inputs must match names")
        expected_prefix = (N_STATES, N_STATES)
        if left.ndim != 5 or left.shape[:2] != expected_prefix or left.shape[2] < 1:
            raise ValueError(
                "second_left must have shape (state, destination, rank, memory, inputs)"
            )
        if right.shape != left.shape:
            raise ValueError("second_right must have the same shape as second_left")
        if left.shape[3:] != first.shape[2:]:
            raise ValueError("second-order memory and input dimensions must match first_order")
        if scale.shape != (len(names),) or not np.all(np.isfinite(scale)) or np.any(scale <= 0):
            raise ValueError("input_scale must contain one finite positive value per input")
        if not np.isfinite(self.logit_bound) or self.logit_bound <= 0:
            raise ValueError("logit_bound must be finite and positive")
        if not np.all(np.isfinite(first)) or not np.all(np.isfinite(left)):
            raise ValueError("Volterra kernel coefficients must be finite")
        if not np.all(np.isfinite(right)):
            raise ValueError("Volterra kernel coefficients must be finite")

        object.__setattr__(self, "input_names", names)
        object.__setattr__(self, "first_order", first)
        object.__setattr__(self, "second_left", left)
        object.__setattr__(self, "second_right", right)
        object.__setattr__(self, "input_scale", scale)

    @property
    def memory(self) -> int:
        return int(self.first_order.shape[2])

    @property
    def input_dim(self) -> int:
        return int(self.first_order.shape[3])

    @property
    def rank(self) -> int:
        return int(self.second_left.shape[2])


@dataclass(frozen=True)
class SpeciesParameters:
    """Species-specific clocks, emissions, and baseline destinations."""

    species: Species
    observation_names: tuple[str, ...]
    initial_probabilities: np.ndarray
    base_transition_logits: np.ndarray
    duration_hazards: np.ndarray
    emission_means: np.ndarray
    emission_sds: np.ndarray

    def __post_init__(self) -> None:
        species = _as_species(self.species)
        names = tuple(str(name) for name in self.observation_names)
        initial = _readonly_float_array(self.initial_probabilities, "initial_probabilities")
        logits = _readonly_float_array(self.base_transition_logits, "base_transition_logits")
        hazards = _readonly_float_array(self.duration_hazards, "duration_hazards")
        means = _readonly_float_array(self.emission_means, "emission_means")
        sds = _readonly_float_array(self.emission_sds, "emission_sds")

        if not names or any(not name for name in names) or len(set(names)) != len(names):
            raise ValueError("observation_names must be non-empty and unique")
        if initial.shape != (N_STATES,) or np.any(initial < 0):
            raise ValueError(f"initial_probabilities must have shape ({N_STATES},) and be >= 0")
        if not np.all(np.isfinite(initial)) or not np.isclose(initial.sum(), 1.0):
            raise ValueError("initial_probabilities must be finite and sum to one")
        if logits.shape != (N_STATES, N_STATES):
            raise ValueError(f"base_transition_logits must have shape ({N_STATES}, {N_STATES})")
        if hazards.ndim != 2 or hazards.shape[0] != N_STATES or hazards.shape[1] < 2:
            raise ValueError("duration_hazards must have shape (state, max_duration >= 2)")
        if not np.all(np.isfinite(hazards)) or np.any(hazards < 0) or np.any(hazards > 1):
            raise ValueError("duration_hazards must be finite probabilities in [0, 1]")
        if not np.allclose(hazards[:, -1], 1.0):
            raise ValueError("the final duration hazard must be one for every state")
        if means.shape != (N_STATES, len(names)) or not np.all(np.isfinite(means)):
            raise ValueError("emission_means must have shape (state, observation) and be finite")
        if sds.shape != means.shape or not np.all(np.isfinite(sds)) or np.any(sds <= 0):
            raise ValueError("emission_sds must match emission_means and be finite and positive")
        for source in range(N_STATES):
            allowed = np.isfinite(np.delete(logits[source], source))
            if not allowed.any():
                raise ValueError("each state must have at least one finite exit destination logit")

        object.__setattr__(self, "species", species)
        object.__setattr__(self, "observation_names", names)
        object.__setattr__(self, "initial_probabilities", initial)
        object.__setattr__(self, "base_transition_logits", logits)
        object.__setattr__(self, "duration_hazards", hazards)
        object.__setattr__(self, "emission_means", means)
        object.__setattr__(self, "emission_sds", sds)

    @property
    def max_duration(self) -> int:
        return int(self.duration_hazards.shape[1])

    @property
    def observation_dim(self) -> int:
        return int(self.emission_means.shape[1])


@dataclass(frozen=True)
class FilterResult:
    """Normalized filtering distributions and sequence log likelihood."""

    species: Species
    states: tuple[OsteosarcomaState, ...]
    state_posterior: np.ndarray
    duration_posterior: np.ndarray
    log_likelihood: float


@dataclass(frozen=True)
class PathResult:
    """Most-likely augmented-state path."""

    species: Species
    state_indices: np.ndarray
    state_path: tuple[OsteosarcomaState, ...]
    elapsed_durations: np.ndarray
    log_probability: float


@dataclass(frozen=True)
class SimulationResult:
    """A reproducible latent path and Gaussian normalized-scale observations."""

    species: Species
    observations: np.ndarray
    state_indices: np.ndarray
    state_path: tuple[OsteosarcomaState, ...]
    elapsed_durations: np.ndarray
    inputs: np.ndarray
    seed: int


def discrete_weibull_hazards(scale: float, shape: float, max_duration: int) -> np.ndarray:
    """Return truncated discrete-Weibull exit hazards for elapsed times 1..D."""

    if not np.isfinite(scale) or scale <= 0 or not np.isfinite(shape) or shape <= 0:
        raise ValueError("scale and shape must be finite and positive")
    if not isinstance(max_duration, (int, np.integer)) or max_duration < 2:
        raise ValueError("max_duration must be an integer >= 2")
    elapsed = np.arange(1, max_duration + 1, dtype=float)
    previous = elapsed - 1.0
    increment = (elapsed / scale) ** shape - (previous / scale) ** shape
    hazards = -np.expm1(-increment)
    hazards[-1] = 1.0
    return hazards


class OsteosarcomaVolterraHSMM:
    """Explicit-duration HMM with species-aware Volterra transition logits."""

    def __init__(
        self,
        kernels: VolterraTransitionKernels,
        species_parameters: Sequence[SpeciesParameters] | Mapping[Species, SpeciesParameters],
    ) -> None:
        self.kernels = kernels
        values = (
            tuple(species_parameters.values())
            if isinstance(species_parameters, Mapping)
            else tuple(species_parameters)
        )
        parameters: dict[Species, SpeciesParameters] = {}
        for item in values:
            if not isinstance(item, SpeciesParameters):
                raise TypeError("species_parameters must contain SpeciesParameters objects")
            if item.species in parameters:
                raise ValueError(f"duplicate parameters for species {item.species.value}")
            parameters[item.species] = item
        missing = set(Species) - set(parameters)
        if missing:
            names = ", ".join(sorted(item.value for item in missing))
            raise ValueError(f"species parameters are required for: {names}")
        observation_names = {item.observation_names for item in parameters.values()}
        if len(observation_names) != 1:
            raise ValueError("dog and human parameters must use the same observation names")
        self.species_parameters = MappingProxyType(parameters)
        self.observation_names = next(iter(observation_names))
        self.input_names = kernels.input_names
        self.states = STATE_ORDER

    def _parameters(self, species: Species | str) -> SpeciesParameters:
        return self.species_parameters[_as_species(species)]

    def _validate_inputs(self, inputs: np.ndarray) -> np.ndarray:
        values = np.asarray(inputs, dtype=float)
        if values.ndim != 2 or values.shape[1] != self.kernels.input_dim:
            raise ValueError(
                f"inputs must have shape (time, {self.kernels.input_dim}) in input_names order"
            )
        if values.shape[0] < 1 or not np.all(np.isfinite(values)):
            raise ValueError("inputs must contain at least one finite time point")
        return values

    def _validate_observations(self, observations: np.ndarray, time_points: int) -> np.ndarray:
        values = np.asarray(observations, dtype=float)
        expected = (time_points, len(self.observation_names))
        if values.shape != expected:
            raise ValueError(f"observations must have shape {expected}")
        if np.isinf(values).any():
            raise ValueError("observations may contain NaN for missing values, but not infinity")
        return values

    def _bounded_history(self, inputs: np.ndarray, time_index: int) -> np.ndarray:
        if time_index < 0 or time_index >= len(inputs):
            raise ValueError("time_index must identify a row of inputs")
        history = np.zeros((self.kernels.memory, self.kernels.input_dim), dtype=float)
        for lag in range(self.kernels.memory):
            source = time_index - lag
            if source >= 0:
                history[lag] = np.tanh(inputs[source] / self.kernels.input_scale)
        return history

    def volterra_logit_adjustment(self, inputs: np.ndarray, time_index: int) -> np.ndarray:
        """Return bounded first- plus low-rank second-order logit adjustments."""

        values = self._validate_inputs(inputs)
        history = self._bounded_history(values, time_index)
        first = np.einsum("ijlc,lc->ij", self.kernels.first_order, history)
        left = np.einsum("ijrlc,lc->ijr", self.kernels.second_left, history)
        right = np.einsum("ijrlc,lc->ijr", self.kernels.second_right, history)
        second = np.sum(left * right, axis=2)
        return np.clip(first + second, -self.kernels.logit_bound, self.kernels.logit_bound)

    def transition_probabilities(
        self, inputs: np.ndarray, time_index: int, species: Species | str
    ) -> np.ndarray:
        """Conditional destination probabilities given exit from each state."""

        params = self._parameters(species)
        adjustment = self.volterra_logit_adjustment(inputs, time_index)
        logits = np.asarray(params.base_transition_logits) + adjustment
        result = np.zeros((N_STATES, N_STATES), dtype=float)
        for source in range(N_STATES):
            row = np.array(logits[source], copy=True)
            row[source] = -np.inf
            finite = np.isfinite(row)
            normalizer = logsumexp(row[finite])
            result[source, finite] = np.exp(row[finite] - normalizer)
        return result

    def _transition_log_probabilities(
        self, inputs: np.ndarray, time_index: int, species: Species | str
    ) -> np.ndarray:
        probabilities = self.transition_probabilities(inputs, time_index, species)
        result = np.full_like(probabilities, -np.inf)
        positive = probabilities > 0
        result[positive] = np.log(probabilities[positive])
        return result

    @staticmethod
    def _emission_log_likelihood(observation: np.ndarray, params: SpeciesParameters) -> np.ndarray:
        observed = ~np.isnan(observation)
        if not observed.any():
            return np.zeros(N_STATES, dtype=float)
        residual = (
            observation[observed][None, :] - params.emission_means[:, observed]
        ) / params.emission_sds[:, observed]
        normalizer = np.log(params.emission_sds[:, observed]) + 0.5 * np.log(2 * np.pi)
        return (-0.5 * residual**2 - normalizer).sum(axis=1)

    @staticmethod
    def _log_hazard(probability: float) -> float:
        return float(np.log(probability)) if probability > 0 else float("-inf")

    @staticmethod
    def _log_survival(probability: float) -> float:
        return float(np.log1p(-probability)) if probability < 1 else float("-inf")

    def _forward_prediction(
        self,
        log_alpha: np.ndarray,
        destination_log_probabilities: np.ndarray,
        params: SpeciesParameters,
    ) -> np.ndarray:
        prediction = np.full_like(log_alpha, -np.inf)
        for source in range(N_STATES):
            leave_terms = []
            for age in range(params.max_duration):
                hazard = params.duration_hazards[source, age]
                leave_terms.append(log_alpha[source, age] + self._log_hazard(hazard))
                if age + 1 < params.max_duration:
                    stay = log_alpha[source, age] + self._log_survival(hazard)
                    prediction[source, age + 1] = stay
            leave_mass = logsumexp(leave_terms)
            for destination in range(N_STATES):
                log_destination = destination_log_probabilities[source, destination]
                candidate = leave_mass + log_destination
                prediction[destination, 0] = np.logaddexp(
                    prediction[destination, 0], candidate
                )
        return prediction

    def filter(
        self, observations: np.ndarray, inputs: np.ndarray, species: Species | str
    ) -> FilterResult:
        """Run normalized log-domain forward filtering over state and elapsed duration."""

        values = self._validate_inputs(inputs)
        measured = self._validate_observations(observations, len(values))
        selected_species = _as_species(species)
        params = self._parameters(selected_species)
        time_points = len(values)
        duration_posterior = np.zeros((time_points, N_STATES, params.max_duration))
        log_alpha = np.full((N_STATES, params.max_duration), -np.inf)
        positive = params.initial_probabilities > 0
        log_alpha[positive, 0] = np.log(params.initial_probabilities[positive])
        log_alpha += self._emission_log_likelihood(measured[0], params)[:, None]
        scale = float(logsumexp(log_alpha))
        log_likelihood = scale
        log_alpha -= scale
        duration_posterior[0] = np.exp(log_alpha)

        for time_index in range(1, time_points):
            destinations = self._transition_log_probabilities(
                values, time_index - 1, selected_species
            )
            log_alpha = self._forward_prediction(log_alpha, destinations, params)
            emission = self._emission_log_likelihood(measured[time_index], params)
            log_alpha += emission[:, None]
            scale = float(logsumexp(log_alpha))
            if not np.isfinite(scale):
                raise FloatingPointError("all augmented states became numerically impossible")
            log_likelihood += scale
            log_alpha -= scale
            duration_posterior[time_index] = np.exp(log_alpha)

        state_posterior = duration_posterior.sum(axis=2)
        return FilterResult(
            species=selected_species,
            states=STATE_ORDER,
            state_posterior=state_posterior,
            duration_posterior=duration_posterior,
            log_likelihood=float(log_likelihood),
        )

    def most_likely_path(
        self, observations: np.ndarray, inputs: np.ndarray, species: Species | str
    ) -> PathResult:
        """Decode the most-likely state and elapsed-duration path with Viterbi."""

        values = self._validate_inputs(inputs)
        measured = self._validate_observations(observations, len(values))
        selected_species = _as_species(species)
        params = self._parameters(selected_species)
        time_points = len(values)
        delta = np.full((N_STATES, params.max_duration), -np.inf)
        positive = params.initial_probabilities > 0
        delta[positive, 0] = np.log(params.initial_probabilities[positive])
        delta += self._emission_log_likelihood(measured[0], params)[:, None]
        backpointer = np.full(
            (time_points, N_STATES, params.max_duration), -1, dtype=np.int64
        )

        for time_index in range(1, time_points):
            destinations = self._transition_log_probabilities(
                values, time_index - 1, selected_species
            )
            updated = np.full_like(delta, -np.inf)
            for source in range(N_STATES):
                for age in range(params.max_duration):
                    source_flat = source * params.max_duration + age
                    hazard = params.duration_hazards[source, age]
                    if age + 1 < params.max_duration:
                        stay = delta[source, age] + self._log_survival(hazard)
                        updated[source, age + 1] = stay
                        backpointer[time_index, source, age + 1] = source_flat
                    leave = delta[source, age] + self._log_hazard(hazard)
                    for destination in range(N_STATES):
                        candidate = leave + destinations[source, destination]
                        if candidate > updated[destination, 0]:
                            updated[destination, 0] = candidate
                            backpointer[time_index, destination, 0] = source_flat
            updated += self._emission_log_likelihood(measured[time_index], params)[:, None]
            delta = updated

        final_flat = int(np.argmax(delta))
        final_probability = float(delta.flat[final_flat])
        if not np.isfinite(final_probability):
            raise FloatingPointError("no finite Viterbi path exists")
        augmented_path = np.empty(time_points, dtype=np.int64)
        augmented_path[-1] = final_flat
        for time_index in range(time_points - 1, 0, -1):
            state, age = divmod(int(augmented_path[time_index]), params.max_duration)
            augmented_path[time_index - 1] = backpointer[time_index, state, age]
        state_indices = augmented_path // params.max_duration
        elapsed = augmented_path % params.max_duration + 1
        return PathResult(
            species=selected_species,
            state_indices=state_indices,
            state_path=tuple(STATE_ORDER[index] for index in state_indices),
            elapsed_durations=elapsed,
            log_probability=final_probability,
        )

    def simulate(
        self, inputs: np.ndarray, species: Species | str, seed: int = 42
    ) -> SimulationResult:
        """Sample a latent trajectory and normalized observations reproducibly."""

        values = self._validate_inputs(inputs)
        selected_species = _as_species(species)
        params = self._parameters(selected_species)
        rng = np.random.default_rng(seed)
        time_points = len(values)
        state_indices = np.empty(time_points, dtype=np.int64)
        elapsed = np.empty(time_points, dtype=np.int64)
        observations = np.empty((time_points, params.observation_dim), dtype=float)
        state = int(rng.choice(N_STATES, p=params.initial_probabilities))
        age = 0

        for time_index in range(time_points):
            if time_index > 0:
                hazard = params.duration_hazards[state, age]
                if rng.random() < hazard:
                    destinations = self.transition_probabilities(
                        values, time_index - 1, selected_species
                    )
                    state = int(rng.choice(N_STATES, p=destinations[state]))
                    age = 0
                else:
                    age += 1
            state_indices[time_index] = state
            elapsed[time_index] = age + 1
            observations[time_index] = rng.normal(
                params.emission_means[state], params.emission_sds[state]
            )

        return SimulationResult(
            species=selected_species,
            observations=observations,
            state_indices=state_indices,
            state_path=tuple(STATE_ORDER[index] for index in state_indices),
            elapsed_durations=elapsed,
            inputs=np.array(values, copy=True),
            seed=int(seed),
        )


def _logits_from_probabilities(probabilities: np.ndarray) -> np.ndarray:
    probabilities = np.asarray(probabilities, dtype=float)
    logits = np.full_like(probabilities, -np.inf)
    positive = probabilities > 0
    logits[positive] = np.log(probabilities[positive])
    return logits


def _reference_species_parameters(species: Species) -> SpeciesParameters:
    observation_names = (
        "immune_activation",
        "mrd_signal",
        "escape_signal",
        "exhaustion_signal",
    )
    dog_destinations = np.array(
        [
            [0, .55, 0, .35, .05, .05],
            [.15, 0, .65, .10, 0, .10],
            [.45, .05, 0, .20, 0, .30],
            [0, .10, .10, 0, .65, .15],
            [0, .15, .10, .20, 0, .55],
            [.10, .15, .10, .35, .30, 0],
        ]
    )
    human_destinations = np.array(
        [
            [0, .50, 0, .39, .05, .06],
            [.14, 0, .66, .10, 0, .10],
            [.48, .04, 0, .19, 0, .29],
            [0, .09, .11, 0, .66, .14],
            [0, .12, .11, .22, 0, .55],
            [.10, .14, .11, .35, .30, 0],
        ]
    )
    base_means = np.array(
        [
            [.10, .15, .08, .10],
            [1.15, .17, .10, .25],
            [.95, .12, .10, .22],
            [.18, .70, 1.00, .42],
            [.20, 1.40, 1.10, .48],
            [.35, .78, .62, 1.30],
        ]
    )
    if species is Species.DOG:
        max_duration = 12
        scales = (6.0, 3.0, 7.0, 5.0, 2.2, 5.0)
        shapes = (1.4, 2.0, 1.5, 1.9, 1.3, 1.7)
        destinations = dog_destinations
        means = base_means + np.array([.03, .02, 0, .02])[None, :]
        sds = np.full_like(means, .28)
        initial = np.array([.82, .04, .04, .08, .01, .01])
    else:
        max_duration = 16
        scales = (8.0, 4.0, 9.0, 7.0, 3.0, 6.0)
        shapes = (1.5, 2.1, 1.6, 2.0, 1.4, 1.8)
        destinations = human_destinations
        means = base_means
        sds = np.full_like(means, .24)
        initial = np.array([.84, .03, .04, .07, .01, .01])
    hazards = np.stack(
        [
            discrete_weibull_hazards(scale, shape, max_duration)
            for scale, shape in zip(scales, shapes, strict=True)
        ]
    )
    return SpeciesParameters(
        species=species,
        observation_names=observation_names,
        initial_probabilities=initial,
        base_transition_logits=_logits_from_probabilities(destinations),
        duration_hazards=hazards,
        emission_means=means,
        emission_sds=sds,
    )


def reference_osteosarcoma_hsmm(memory: int = 4, rank: int = 2) -> OsteosarcomaVolterraHSMM:
    """Construct an illustrative comparative model for software experiments."""

    if not isinstance(memory, (int, np.integer)) or memory < 1:
        raise ValueError("memory must be an integer >= 1")
    if not isinstance(rank, (int, np.integer)) or rank < 1:
        raise ValueError("rank must be an integer >= 1")
    input_names = (
        "antigen_coverage",
        "rna_dose",
        "chemotherapy",
        "checkpoint_blockade",
        "immune_suppression",
    )
    channels = len(input_names)
    first = np.zeros((N_STATES, N_STATES, memory, channels))
    left = np.zeros((N_STATES, N_STATES, rank, memory, channels))
    right = np.zeros_like(left)
    decay = np.exp(-np.arange(memory) / max(memory / 2, 1))
    n, innate, adaptive, occult, visible, exhausted = range(N_STATES)

    first[n, innate, :, 0] = .34 * decay
    first[n, innate, :, 1] = .28 * decay
    first[innate, adaptive, :, 0] = .30 * decay
    first[innate, adaptive, :, 1] = .22 * decay
    first[occult, adaptive, :, 0] = .20 * decay
    first[exhausted, adaptive, :, 3] = .32 * decay
    first[adaptive, exhausted, :, 4] = .30 * decay
    first[adaptive, occult, :, 4] = .20 * decay
    first[occult, visible, :, 4] = .18 * decay
    first[visible, exhausted, :, 2] = .16 * decay

    # Rank-zero factor: antigen coverage x RNA exposure interaction.
    for source, destination, strength in (
        (n, innate, .24),
        (innate, adaptive, .20),
        (occult, adaptive, .13),
    ):
        left[source, destination, 0, :, 0] = np.sqrt(strength) * decay
        right[source, destination, 0, :, 1] = np.sqrt(strength) * decay
    if rank > 1:
        # Rank-one factor: a signed timing interaction used as a research hypothesis.
        left[innate, adaptive, 1, :, 1] = np.sqrt(.12) * decay
        right[innate, adaptive, 1, :, 2] = -np.sqrt(.12) * decay
        left[exhausted, adaptive, 1, :, 3] = np.sqrt(.15) * decay
        right[exhausted, adaptive, 1, :, 4] = -np.sqrt(.15) * decay

    kernels = VolterraTransitionKernels(
        input_names=input_names,
        first_order=first,
        second_left=left,
        second_right=right,
        input_scale=np.ones(channels),
        logit_bound=2.5,
    )
    parameters = tuple(_reference_species_parameters(species) for species in Species)
    return OsteosarcomaVolterraHSMM(kernels, parameters)


__all__ = [
    "FilterResult",
    "OsteosarcomaState",
    "OsteosarcomaVolterraHSMM",
    "PathResult",
    "SimulationResult",
    "Species",
    "SpeciesParameters",
    "VolterraTransitionKernels",
    "discrete_weibull_hazards",
    "reference_osteosarcoma_hsmm",
]
