"""Research-only DSP model for neoadjuvant immunotherapy in stage III melanoma.

The model combines a block-oriented antibody exposure model, a low-dimensional
bilinear immune-state model, a rank-one second-order Volterra residual, and a
stochastic visible/escape tumor model.  Parameters are synthetic research priors;
outputs are not drug-dose recommendations or estimates of clinical response.
"""

from dataclasses import dataclass, field
from itertools import combinations

import numpy as np


IPILIMUMAB = 0
NIVOLUMAB = 1
CHANNEL_NAMES = ("ipilimumab", "nivolumab")
NADINA_DOSE_MG = np.array([80.0, 240.0])
NADINA_TOTAL_MG = 2 * NADINA_DOSE_MG
SURGERY_DAY = 42
LATEST_TREATMENT_DAY = 28


@dataclass(frozen=True)
class AntibodyExposureModel:
    """Hammerstein-Wiener approximation to antibody exposure and occupancy.

    A saturating dose map precedes first-order disposition, and a second static
    nonlinearity maps the normalized exposure to target-occupancy proxies.  The
    values are deliberately normalized rather than a population-PK calibration.
    """

    half_life_days: np.ndarray = field(
        default_factory=lambda: np.array([15.0, 25.0]))
    dose_scale_mg: np.ndarray = field(
        default_factory=lambda: NADINA_DOSE_MG.copy())
    dose_half_saturation: np.ndarray = field(
        default_factory=lambda: np.array([0.65, 0.55]))
    occupancy_half_saturation: np.ndarray = field(
        default_factory=lambda: np.array([0.32, 0.24]))
    hill: np.ndarray = field(default_factory=lambda: np.array([1.2, 1.15]))

    def __post_init__(self):
        arrays = [self.half_life_days, self.dose_scale_mg,
                  self.dose_half_saturation, self.occupancy_half_saturation, self.hill]
        if any(np.asarray(value).shape != (2,) for value in arrays):
            raise ValueError("antibody exposure parameters require two channels")
        if any(np.any(np.asarray(value) <= 0) for value in arrays):
            raise ValueError("antibody exposure parameters must be positive")


@dataclass(frozen=True)
class AntibodyExposure:
    transformed_dose: np.ndarray
    plasma: np.ndarray
    occupancy: np.ndarray


@dataclass(frozen=True)
class VolterraCrossKernel:
    """Rank-one ipilimumab-by-nivolumab residual interaction kernel."""

    ipilimumab_lag: np.ndarray
    nivolumab_lag: np.ndarray
    gain: float = 0.16
    bound: float = 0.30

    def __post_init__(self):
        left = np.asarray(self.ipilimumab_lag)
        right = np.asarray(self.nivolumab_lag)
        if left.ndim != 1 or right.shape != left.shape or left.size < 1:
            raise ValueError("Volterra lag factors must be equal-length vectors")
        if np.any(left < 0) or np.any(right < 0) or self.gain < 0 or self.bound <= 0:
            raise ValueError("Volterra kernel parameters must be nonnegative")

    @property
    def surface(self) -> np.ndarray:
        return self.gain * np.outer(self.ipilimumab_lag, self.nivolumab_lag)


@dataclass(frozen=True)
class MelanomaDynamics:
    """Nominal low-dimensional immune and tumor dynamics in normalized units."""

    progenitor_decay: float = 0.035
    effector_decay: float = 0.115
    exhaustion_decay: float = 0.055
    ipilimumab_priming: float = 0.105
    basal_differentiation: float = 0.070
    nivolumab_bilinear_gain: float = 0.90
    ipilimumab_bilinear_gain: float = 0.28
    effector_suppression: float = 0.11
    stimulation_exhaustion: float = 0.026
    occupancy_inflammation: float = 0.010
    residual_effector_gain: float = 0.22
    # The treatment cross-kernel is supported as an efficacy residual.  Serious
    # toxicity keeps its own bilinear/dose observation head unless data identify
    # a separate toxicity interaction kernel.
    residual_exhaustion_gain: float = 0.0
    tumor_growth: np.ndarray = field(default_factory=lambda: np.array([0.018, 0.014]))
    effector_kill: np.ndarray = field(default_factory=lambda: np.array([0.080, 0.018]))
    carrying_capacity: float = 1.5
    escape_transition: float = 0.00055

    def __post_init__(self):
        if np.asarray(self.tumor_growth).shape != (2,):
            raise ValueError("tumor_growth must describe visible and escape populations")
        if np.asarray(self.effector_kill).shape != (2,):
            raise ValueError("effector_kill must describe visible and escape populations")
        scalar_values = [
            self.progenitor_decay, self.effector_decay, self.exhaustion_decay,
            self.ipilimumab_priming, self.basal_differentiation,
            self.nivolumab_bilinear_gain, self.ipilimumab_bilinear_gain,
            self.effector_suppression, self.stimulation_exhaustion,
            self.occupancy_inflammation, self.residual_effector_gain,
            self.residual_exhaustion_gain, self.carrying_capacity,
            self.escape_transition,
        ]
        if any(value < 0 for value in scalar_values):
            raise ValueError("dynamical parameters must be nonnegative")


@dataclass(frozen=True)
class MelanomaDSPModel:
    exposure: AntibodyExposureModel
    cross_kernel: VolterraCrossKernel
    dynamics: MelanomaDynamics


@dataclass(frozen=True)
class MelanomaSimulationConfig:
    draws: int = 128
    effective_population: int = 8_000
    patient_log_sd: float = 0.14
    immune_process_sd: float = 0.018
    toxicity_threshold: float = 0.72
    mpr_residual_fraction: float = 0.10
    pcr_residual_fraction: float = 0.01
    escape_dominance_threshold: float = 0.50
    initial_immune: np.ndarray = field(
        default_factory=lambda: np.array([0.12, 0.055, 0.075]))
    initial_tumor: np.ndarray = field(
        default_factory=lambda: np.array([0.30, 0.015]))

    def __post_init__(self):
        if self.draws < 2 or self.effective_population < 100:
            raise ValueError("draws must be >=2 and effective_population must be >=100")
        if np.asarray(self.initial_immune).shape != (3,):
            raise ValueError("initial_immune must contain progenitor, effector, and exhaustion")
        if np.asarray(self.initial_tumor).shape != (2,):
            raise ValueError("initial_tumor must contain visible and escape populations")
        if np.any(np.asarray(self.initial_immune) < 0) or np.any(
                np.asarray(self.initial_tumor) < 0):
            raise ValueError("initial states must be nonnegative")


@dataclass(frozen=True)
class MelanomaRun:
    schedule: np.ndarray
    exposure: AntibodyExposure
    immune: np.ndarray       # draw x day+1 x [progenitor TEX, effector, exhaustion]
    tumor: np.ndarray        # draw x day+1 x [immune-visible, escape]
    toxicity: np.ndarray     # draw x day+1, latent burden rather than a CTCAE grade
    seed: int


def reference_melanoma_model(memory: int = 12) -> MelanomaDSPModel:
    """Return a synthetic, biologically shaped model for methods development."""
    if memory < 2:
        raise ValueError("memory must be at least two days")
    lag = np.arange(memory, dtype=float)
    ipilimumab_lag = np.exp(-lag / 4.5)
    nivolumab_lag = np.exp(-lag / 6.5)
    kernel = VolterraCrossKernel(ipilimumab_lag, nivolumab_lag)
    return MelanomaDSPModel(AntibodyExposureModel(), kernel, MelanomaDynamics())


def nadina_schedule(horizon: int = SURGERY_DAY) -> np.ndarray:
    """Two presurgical 80-mg ipilimumab/240-mg nivolumab doses, 3 weeks apart.

    This helper encodes the trial regimen solely as a computational comparator.
    It is not a prescribing function.
    """
    if horizon <= 21:
        raise ValueError("horizon must include treatment days 0 and 21")
    schedule = np.zeros((horizon, 2), dtype=float)
    schedule[[0, 21]] = NADINA_DOSE_MG
    return schedule


def schedule_violations(schedule: np.ndarray) -> dict[str, np.ndarray | float]:
    """Quantify violations of the deliberately narrow NADINA-derived search space."""
    schedule = np.asarray(schedule, dtype=float)
    if schedule.ndim != 2 or schedule.shape[1] != 2:
        raise ValueError("schedule must be day by [ipilimumab, nivolumab]")
    if not np.all(np.isfinite(schedule)):
        raise ValueError("schedule must contain finite values")
    negative = np.maximum(-schedule, 0).sum(axis=0)
    per_dose = np.maximum(schedule.max(axis=0) - NADINA_DOSE_MG, 0)
    cumulative = np.maximum(schedule.sum(axis=0) - NADINA_TOTAL_MG, 0)
    late = float(np.maximum(schedule[LATEST_TREATMENT_DAY + 1:], 0).sum())
    return {"negative": negative, "per_dose": per_dose,
            "cumulative": cumulative, "late": late}


def schedule_is_feasible(schedule: np.ndarray, tolerance: float = 1e-9) -> bool:
    violations = schedule_violations(schedule)
    return all(np.all(np.asarray(value) <= tolerance) for value in violations.values())


def simulate_antibody_exposure(
    schedule: np.ndarray,
    model: AntibodyExposureModel | None = None,
) -> AntibodyExposure:
    """Apply saturating dose, disposition, and target-occupancy blocks."""
    model = model or AntibodyExposureModel()
    schedule = np.asarray(schedule, dtype=float)
    if schedule.ndim != 2 or schedule.shape[1] != 2 or np.any(schedule < 0):
        raise ValueError("schedule must be a nonnegative day-by-two matrix")
    normalized = schedule / np.asarray(model.dose_scale_mg)
    transformed = normalized / (np.asarray(model.dose_half_saturation) + normalized)
    plasma = np.zeros_like(transformed)
    retention = np.exp(-np.log(2) / np.asarray(model.half_life_days))
    for day in range(len(schedule)):
        previous = plasma[day - 1] if day else np.zeros(2)
        plasma[day] = retention * previous + transformed[day]
    powered = np.power(plasma, np.asarray(model.hill))
    denominator = powered + np.power(
        np.asarray(model.occupancy_half_saturation), np.asarray(model.hill))
    occupancy = np.divide(powered, denominator, out=np.zeros_like(powered), where=denominator > 0)
    return AntibodyExposure(transformed, plasma, occupancy)


def volterra_cross_residual(
    effective_input: np.ndarray,
    kernel: VolterraCrossKernel,
) -> np.ndarray:
    """Evaluate a bounded rank-one second-order ipilimumab-by-nivolumab kernel."""
    inputs = np.asarray(effective_input, dtype=float)
    if inputs.ndim != 2 or inputs.shape[1] != 2:
        raise ValueError("effective_input must contain two treatment channels")
    memory = len(kernel.ipilimumab_lag)
    ipilimumab_history = np.zeros(len(inputs))
    nivolumab_history = np.zeros(len(inputs))
    for day in range(len(inputs)):
        available = min(memory, day + 1)
        history = inputs[day - available + 1:day + 1][::-1]
        ipilimumab_history[day] = np.dot(
            kernel.ipilimumab_lag[:available], history[:, IPILIMUMAB])
        nivolumab_history[day] = np.dot(
            kernel.nivolumab_lag[:available], history[:, NIVOLUMAB])
    raw = kernel.gain * ipilimumab_history * nivolumab_history
    return kernel.bound * np.tanh(raw / kernel.bound)


def _immune_step(
    state: np.ndarray,
    occupancy: np.ndarray,
    residual: float,
    dynamics: MelanomaDynamics,
    immune_gain: np.ndarray,
    rng: np.random.Generator,
    process_sd: float,
) -> np.ndarray:
    progenitor, effector, exhaustion = state.T
    ipilimumab = occupancy[IPILIMUMAB]
    nivolumab = occupancy[NIVOLUMAB]
    differentiation = dynamics.basal_differentiation * progenitor * (
        1 + dynamics.nivolumab_bilinear_gain * nivolumab
        + dynamics.ipilimumab_bilinear_gain * ipilimumab)
    next_progenitor = (
        progenitor + immune_gain[:, 0] * dynamics.ipilimumab_priming * ipilimumab
        - dynamics.progenitor_decay * progenitor - 0.42 * differentiation)
    next_effector = (
        effector + immune_gain[:, 1] * differentiation
        + immune_gain[:, 1] * dynamics.residual_effector_gain * residual
        - dynamics.effector_decay * effector
        - dynamics.effector_suppression * exhaustion * effector)
    stimulation = ipilimumab + nivolumab
    next_exhaustion = (
        exhaustion + immune_gain[:, 2] * dynamics.stimulation_exhaustion
        * effector * stimulation
        + immune_gain[:, 2] * dynamics.occupancy_inflammation * stimulation
        + dynamics.residual_exhaustion_gain * residual
        - dynamics.exhaustion_decay * exhaustion)
    updated = np.column_stack([next_progenitor, next_effector, next_exhaustion])
    updated += rng.normal(0, process_sd, updated.shape)
    return np.clip(updated, 0, 3.0)


def _tumor_step(
    counts: np.ndarray,
    immune: np.ndarray,
    dynamics: MelanomaDynamics,
    growth_gain: np.ndarray,
    kill_gain: np.ndarray,
    escape_gain: np.ndarray,
    effective_population: int,
    rng: np.random.Generator,
) -> np.ndarray:
    total = counts.sum(axis=1) / effective_population
    logistic = np.asarray(dynamics.tumor_growth)[None, :] * growth_gain[:, None] * (
        1 - total[:, None] / dynamics.carrying_capacity)
    effective_effector = immune[:, 1] / (1 + immune[:, 2])
    kill_rate = (np.asarray(dynamics.effector_kill)[None, :] * kill_gain[:, None]
                 * effective_effector[:, None])
    births = rng.poisson(counts * np.maximum(logistic, 0))
    background_death = np.maximum(-logistic, 0)
    death_probability = np.clip(1 - np.exp(-(background_death + kill_rate)), 0, 1)
    deaths = rng.binomial(counts.astype(np.int64), death_probability)
    survivors = np.maximum(0, counts + births - deaths).astype(np.int64)
    selection = 1 + 0.8 * effective_effector
    transition_probability = np.clip(
        dynamics.escape_transition * escape_gain * selection, 0, 0.05)
    switched = rng.binomial(survivors[:, 0], transition_probability)
    survivors[:, 0] -= switched
    survivors[:, 1] += switched
    return survivors


def simulate_melanoma(
    schedule: np.ndarray,
    model: MelanomaDSPModel | None = None,
    config: MelanomaSimulationConfig = MelanomaSimulationConfig(),
    seed: int = 42,
    enforce_constraints: bool = True,
) -> MelanomaRun:
    """Simulate stochastic immune, tumor, escape, and toxicity proxy trajectories."""
    model = model or reference_melanoma_model()
    schedule = np.asarray(schedule, dtype=float)
    if schedule.ndim != 2 or schedule.shape[1] != 2 or not np.all(
            np.isfinite(schedule)) or np.any(schedule < 0):
        raise ValueError("schedule must be a finite nonnegative day-by-two matrix")
    if enforce_constraints and not schedule_is_feasible(schedule):
        raise ValueError("schedule lies outside the NADINA-derived research constraints")
    rng = np.random.default_rng(seed)
    exposure = simulate_antibody_exposure(schedule, model.exposure)
    residual = volterra_cross_residual(exposure.occupancy, model.cross_kernel)
    immune = np.zeros((config.draws, len(schedule) + 1, 3))
    immune[:, 0] = np.asarray(config.initial_immune)
    tumor = np.zeros((config.draws, len(schedule) + 1, 2))
    counts = rng.poisson(
        np.asarray(config.initial_tumor)[None, :] * config.effective_population,
        size=(config.draws, 2),
    ).astype(np.int64)
    tumor[:, 0] = counts / config.effective_population
    toxicity = np.zeros((config.draws, len(schedule) + 1))
    immune_gain = rng.lognormal(0, config.patient_log_sd, (config.draws, 3))
    growth_gain = rng.lognormal(0, config.patient_log_sd, config.draws)
    kill_gain = rng.lognormal(0, 1.2 * config.patient_log_sd, config.draws)
    escape_gain = rng.lognormal(0, 1.4 * config.patient_log_sd, config.draws)
    toxicity_gain = rng.lognormal(0, config.patient_log_sd, config.draws)
    for day in range(len(schedule)):
        immune[:, day + 1] = _immune_step(
            immune[:, day], exposure.occupancy[day], residual[day], model.dynamics,
            immune_gain, rng, config.immune_process_sd)
        counts = _tumor_step(
            counts, immune[:, day + 1], model.dynamics, growth_gain, kill_gain,
            escape_gain, config.effective_population, rng)
        tumor[:, day + 1] = counts / config.effective_population
        stimulation = exposure.occupancy[day].sum()
        toxicity[:, day + 1] = toxicity_gain * (
            immune[:, day + 1, 2] + 0.10 * stimulation)
    return MelanomaRun(schedule.copy(), exposure, immune, tumor, toxicity, seed)


def _wilson_interval(events: np.ndarray, z: float = 1.96) -> list[float]:
    values = np.asarray(events, dtype=bool)
    count = len(values)
    estimate = float(values.mean())
    denominator = 1 + z ** 2 / count
    center = (estimate + z ** 2 / (2 * count)) / denominator
    radius = z * np.sqrt(
        estimate * (1 - estimate) / count + z ** 2 / (4 * count ** 2)
    ) / denominator
    return [float(max(0, center - radius)), float(min(1, center + radius))]


def clinical_metrics(
    run: MelanomaRun,
    config: MelanomaSimulationConfig = MelanomaSimulationConfig(),
) -> dict[str, object]:
    """Summarize clinically recognizable but explicitly model-conditional endpoints."""
    initial = run.tumor[:, 0].sum(axis=1)
    terminal = run.tumor[:, -1].sum(axis=1)
    residual_fraction = terminal / np.maximum(initial, np.finfo(float).eps)
    escape_fraction = np.divide(
        run.tumor[:, -1, 1], terminal, out=np.zeros_like(terminal), where=terminal > 0)
    peak_toxicity = run.toxicity.max(axis=1)
    mpr = residual_fraction <= config.mpr_residual_fraction
    pcr = residual_fraction <= config.pcr_residual_fraction
    escape = escape_fraction >= config.escape_dominance_threshold
    toxicity = peak_toxicity > config.toxicity_threshold
    return {
        "modeled_major_pathologic_response_probability": float(mpr.mean()),
        "modeled_major_pathologic_response_mc95": _wilson_interval(mpr),
        "modeled_complete_pathologic_response_probability": float(pcr.mean()),
        "modeled_complete_pathologic_response_mc95": _wilson_interval(pcr),
        "median_residual_viable_tumor_fraction": float(np.median(residual_fraction)),
        "residual_viable_tumor_fraction_p05": float(np.quantile(residual_fraction, 0.05)),
        "residual_viable_tumor_fraction_p95": float(np.quantile(residual_fraction, 0.95)),
        "modeled_escape_dominance_probability": float(escape.mean()),
        "modeled_escape_dominance_mc95": _wilson_interval(escape),
        "median_escape_fraction_at_surgery": float(np.median(escape_fraction)),
        "modeled_toxicity_proxy_exceedance_probability": float(toxicity.mean()),
        "modeled_toxicity_proxy_exceedance_mc95": _wilson_interval(toxicity),
        "peak_toxicity_proxy_p95": float(np.quantile(peak_toxicity, 0.95)),
        "total_ipilimumab_mg": float(run.schedule[:, IPILIMUMAB].sum()),
        "total_nivolumab_mg": float(run.schedule[:, NIVOLUMAB].sum()),
        "surgery_day": len(run.schedule),
        "clinical_superiority_established": False,
        "claim_scope": (
            "Synthetic model-conditional endpoints; not clinical response or toxicity estimates."
        ),
    }


def _policy_loss(run: MelanomaRun, config: MelanomaSimulationConfig) -> float:
    metrics = clinical_metrics(run, config)
    dose_fraction = np.sum(run.schedule, axis=0) / NADINA_TOTAL_MG
    return float(
        metrics["median_residual_viable_tumor_fraction"]
        + 0.55 * metrics["modeled_escape_dominance_probability"]
        + 0.75 * metrics["modeled_toxicity_proxy_exceedance_probability"]
        + 0.08 * metrics["peak_toxicity_proxy_p95"]
        + 0.008 * np.square(dose_fraction).sum()
    )


def _candidate_schedules(count: int, rng: np.random.Generator) -> list[np.ndarray]:
    schedules = [nadina_schedule()]
    for days in [(0, 14), (7, 21), (0, 28), (14, 28)]:
        schedule = np.zeros((SURGERY_DAY, 2))
        schedule[list(days)] = NADINA_DOSE_MG
        schedules.append(schedule)
    day_grid = np.arange(0, LATEST_TREATMENT_DAY + 1, 7)
    while len(schedules) < max(1, count):
        schedule = np.zeros((SURGERY_DAY, 2))
        for channel in range(2):
            event_count = int(rng.integers(1, 3))
            days = np.sort(rng.choice(day_grid, event_count, replace=False))
            fractions = rng.uniform(0.35, 1.0, event_count)
            if fractions.sum() > 2:
                fractions *= 2 / fractions.sum()
            schedule[days, channel] = NADINA_DOSE_MG[channel] * fractions
        schedules.append(schedule)
    return schedules[:max(1, count)]


def search_constrained_schedule(
    model: MelanomaDSPModel | None = None,
    config: MelanomaSimulationConfig = MelanomaSimulationConfig(draws=64),
    candidates: int = 64,
    seed: int = 42,
) -> dict[str, object]:
    """Search only within the NADINA total-dose and presurgical timing envelope.

    The result is an in-silico hypothesis.  The function always reports that
    clinical superiority has not been established.
    """
    if candidates < 1:
        raise ValueError("candidates must be positive")
    model = model or reference_melanoma_model()
    rng = np.random.default_rng(seed)
    schedules = _candidate_schedules(candidates, rng)
    evaluation_seed = seed + 10_000
    best_schedule = schedules[0]
    best_run = simulate_melanoma(best_schedule, model, config, evaluation_seed)
    best_loss = _policy_loss(best_run, config)
    nadina_run = best_run
    nadina_loss = best_loss
    for schedule in schedules[1:]:
        run = simulate_melanoma(schedule, model, config, evaluation_seed)
        loss = _policy_loss(run, config)
        if loss < best_loss:
            best_schedule, best_run, best_loss = schedule, run, loss
    return {
        "schedule": best_schedule,
        "run": best_run,
        "metrics": clinical_metrics(best_run, config),
        "objective": float(best_loss),
        "nadina_objective": float(nadina_loss),
        "in_silico_objective_improvement_vs_nadina": float(nadina_loss - best_loss),
        "schedule_feasible": schedule_is_feasible(best_schedule),
        "candidate_count": len(schedules),
        "clinical_superiority_established": False,
        "claim_scope": (
            "The search compares synthetic trajectories inside a constrained model, not patients."
        ),
    }


def allowed_two_dose_day_pairs() -> tuple[tuple[int, int], ...]:
    """Expose the weekly-grid timing hypotheses used by the deterministic search."""
    return tuple(combinations(range(0, LATEST_TREATMENT_DAY + 1, 7), 2))
