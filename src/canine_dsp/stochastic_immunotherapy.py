"""Stochastic state-space layer for Volterra-driven combination immunotherapy."""

from dataclasses import dataclass, replace

import numpy as np
import pandas as pd
from scipy.optimize import differential_evolution
from scipy.stats import binom, nbinom, norm

from .evolution import ImmuneKernels, volterra_response
from .immunotherapy import ImmunotherapySystem


@dataclass(frozen=True)
class StochasticConfig:
    """Uncertainty assumptions in normalized model units."""

    draws: int = 128
    effective_population: int = 10_000
    patient_log_sd: float = 0.10
    kernel_log_sd: float = 0.08
    immune_process_sd: float = 0.07
    immune_noise_rho: float = 0.65
    imaging_log_sd: float = 0.12
    ctdna_depth: int = 2_000
    rna_dispersion: float = 20.0
    response_threshold: float = 0.50
    escape_threshold: float = 0.50
    inflammation_limit: float = 1.0

    def __post_init__(self):
        if self.draws < 2 or self.effective_population < 100:
            raise ValueError("draws must be >=2 and effective_population >=100")
        if not 0 <= self.immune_noise_rho < 1:
            raise ValueError("immune_noise_rho must lie in [0, 1)")


@dataclass(frozen=True)
class StochasticRun:
    states: np.ndarray       # draw x time+1 x [sensitive, escape]
    immune: np.ndarray       # draw x time x [cytotoxic, exhaustion, inflammation]
    schedule: np.ndarray
    seed: int


def _wilson_interval(events: np.ndarray, z: float = 1.96) -> list[float]:
    """Binomial interval for finite-Monte-Carlo probability estimates."""
    values = np.asarray(events, bool)
    n = len(values); estimate = values.mean()
    denominator = 1 + z ** 2 / n
    center = (estimate + z ** 2 / (2 * n)) / denominator
    radius = z * np.sqrt(estimate * (1 - estimate) / n + z ** 2 / (4 * n ** 2)) / denominator
    return [float(max(0, center - radius)), float(min(1, center + radius))]


def _patient_parameters(system: ImmunotherapySystem, draws: int, sd: float,
                        rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    growth = np.asarray(system.growth)[None, :] * rng.lognormal(0, sd, (draws, 2))
    killing = np.asarray(system.cytotoxic_kill)[None, :] * rng.lognormal(0, sd, (draws, 2))
    transition = system.transition * rng.lognormal(0, 1.5 * sd, draws)
    return growth, killing, transition


def _uncertain_immune(schedule: np.ndarray, kernels: ImmuneKernels, config: StochasticConfig,
                      rng: np.random.Generator) -> np.ndarray:
    drive = volterra_response(schedule, kernels)
    gains = rng.lognormal(0, config.kernel_log_sd, (config.draws, 1, drive.shape[1]))
    noise = np.zeros((config.draws, drive.shape[1]))
    immune = np.zeros((config.draws, len(schedule), drive.shape[1]))
    innovation_sd = config.immune_process_sd * np.sqrt(1 - config.immune_noise_rho ** 2)
    for day in range(len(schedule)):
        noise = config.immune_noise_rho * noise + rng.normal(
            0, innovation_sd, size=noise.shape)
        immune[:, day] = np.maximum(0, drive[day][None, :] * gains[:, 0] * np.exp(noise))
    return immune


def _advance_counts(counts: np.ndarray, immune: np.ndarray, growth: np.ndarray,
                    killing: np.ndarray, transition: np.ndarray,
                    system: ImmunotherapySystem, config: StochasticConfig,
                    rng: np.random.Generator) -> np.ndarray:
    density = counts.sum(axis=1) / (config.effective_population * system.carrying_capacity)
    logistic = growth * (1 - density[:, None])
    effective_ctl = immune[:, 0] / (1 + immune[:, 1])
    treatment_death = killing * effective_ctl[:, None]
    treatment_death += system.inflammation_kill * immune[:, 2, None]
    births = rng.poisson(counts * np.maximum(logistic, 0))
    death_rate = np.maximum(-logistic, 0) + np.maximum(treatment_death, 0)
    deaths = rng.binomial(counts.astype(np.int64), np.clip(1 - np.exp(-death_rate), 0, 1))
    survivors = np.maximum(0, counts + births - deaths).astype(np.int64)
    switched = rng.binomial(survivors[:, 0], np.clip(1 - np.exp(-transition), 0, 1))
    survivors[:, 0] -= switched
    survivors[:, 1] += switched
    return survivors


def simulate_stochastic(system: ImmunotherapySystem, kernels: ImmuneKernels,
                        schedule: np.ndarray, initial: np.ndarray,
                        config: StochasticConfig = StochasticConfig(),
                        seed: int = 42) -> StochasticRun:
    """Tau-leap birth/death/escape simulation with patient, kernel, and process uncertainty."""
    rng = np.random.default_rng(seed)
    immune = _uncertain_immune(np.asarray(schedule, float), kernels, config, rng)
    growth, killing, transition = _patient_parameters(
        system, config.draws, config.patient_log_sd, rng)
    counts = rng.poisson(np.asarray(initial)[None, :] * config.effective_population,
                         size=(config.draws, 2)).astype(np.int64)
    states = np.zeros((config.draws, len(schedule) + 1, 2), dtype=float)
    states[:, 0] = counts / config.effective_population
    for day in range(len(schedule)):
        counts = _advance_counts(counts, immune[:, day], growth, killing, transition,
                                 system, config, rng)
        states[:, day + 1] = counts / config.effective_population
    return StochasticRun(states, immune, np.asarray(schedule, float), seed)


def risk_metrics(run: StochasticRun, config: StochasticConfig) -> dict[str, float]:
    total = run.states.sum(axis=2)
    terminal = total[:, -1]
    escape = np.divide(run.states[:, -1, 1], terminal, out=np.zeros_like(terminal),
                       where=terminal > 0)
    peak_inflammation = run.immune[:, :, 2].max(axis=1)
    cutoff = run.states[:, 0].sum(axis=1) * config.response_threshold
    tail_start = np.quantile(terminal, .9)
    response_event = terminal <= cutoff
    escape_event = escape >= config.escape_threshold
    inflammation_event = peak_inflammation > config.inflammation_limit
    return {
        "response_probability": float(np.mean(response_event)),
        "response_probability_mc95": _wilson_interval(response_event),
        "escape_probability": float(np.mean(escape_event)),
        "escape_probability_mc95": _wilson_interval(escape_event),
        "inflammation_exceedance_probability": float(np.mean(inflammation_event)),
        "inflammation_exceedance_probability_mc95": _wilson_interval(inflammation_event),
        "median_terminal_tumor": float(np.median(terminal)),
        "terminal_tumor_p05": float(np.quantile(terminal, .05)),
        "terminal_tumor_p95": float(np.quantile(terminal, .95)),
        "median_escape_fraction": float(np.median(escape)),
        "escape_fraction_p95": float(np.quantile(escape, .95)),
        "terminal_tumor_cvar90": float(terminal[terminal >= tail_start].mean()),
    }


def comparative_metrics(treated: StochasticRun, untreated: StochasticRun) -> dict[str, float]:
    """Compare equal-sized counterfactual ensembles, preferably generated with a shared seed."""
    treated_terminal = treated.states[:, -1].sum(axis=1)
    untreated_terminal = untreated.states[:, -1].sum(axis=1)
    if treated_terminal.shape != untreated_terminal.shape:
        raise ValueError("treated and untreated ensembles must have equal numbers of draws")
    relative = 1 - treated_terminal / np.maximum(untreated_terminal, np.finfo(float).eps)
    lower_event = relative > 0
    major_event = relative >= .5
    return {
        "median_terminal_reduction_vs_untreated": float(np.median(relative)),
        "probability_lower_burden_than_untreated": float(np.mean(lower_event)),
        "probability_lower_burden_than_untreated_mc95": _wilson_interval(lower_event),
        "probability_at_least_50pct_lower_than_untreated": float(np.mean(major_event)),
        "probability_at_least_50pct_lower_than_untreated_mc95": _wilson_interval(major_event),
        "relative_reduction_p05": float(np.quantile(relative, .05)),
        "relative_reduction_p95": float(np.quantile(relative, .95)),
    }


def _risk_objective(run: StochasticRun, config: StochasticConfig) -> float:
    metrics = risk_metrics(run, config)
    terminal = run.states[:, -1].sum(axis=1)
    escape = np.divide(run.states[:, -1, 1], terminal, out=np.zeros_like(terminal),
                       where=terminal > 0)
    inflammation = run.immune[:, :, 2].max(axis=1)
    toxicity_excess = np.maximum(inflammation - config.inflammation_limit, 0)
    return (metrics["terminal_tumor_cvar90"] + .35 * metrics["median_terminal_tumor"]
            + .75 * np.mean(escape) + 5 * np.mean(np.square(toxicity_excess))
            + .006 * np.square(run.schedule).sum())


def optimize_stochastic_immunotherapy(system: ImmunotherapySystem, kernels: ImmuneKernels,
                                      initial: np.ndarray, horizon: int,
                                      administration_times: list[int], max_dose: np.ndarray,
                                      config: StochasticConfig = StochasticConfig(draws=48),
                                      seed: int = 42, maxiter: int = 24) -> dict:
    """Minimize a common-random-number Monte Carlo objective emphasizing the adverse tail."""
    max_dose = np.asarray(max_dose, float)
    channels = kernels.h1.shape[1]
    if max_dose.shape != (channels,):
        raise ValueError("max_dose must contain one bound per treatment channel")
    if any(day < 0 or day >= horizon for day in administration_times):
        raise ValueError("administration times must lie inside the horizon")
    bounds = [(0., float(limit)) for _ in administration_times for limit in max_dose]

    def unpack(vector):
        schedule = np.zeros((horizon, channels))
        schedule[administration_times] = np.asarray(vector).reshape(len(administration_times), channels)
        return schedule

    def objective(vector):
        schedule = unpack(vector)
        run = simulate_stochastic(system, kernels, schedule, initial, config, seed)
        return _risk_objective(run, config)

    fit = differential_evolution(objective, bounds, seed=seed, maxiter=maxiter, popsize=6,
                                 tol=.025, polish=True)
    schedule = unpack(fit.x)
    run = simulate_stochastic(system, kernels, schedule, initial, config, seed + 10_000)
    return {"schedule": schedule, "run": run, "objective": float(fit.fun),
            "success": bool(fit.success), "message": str(fit.message),
            "metrics": risk_metrics(run, config)}


def sample_observations(run: StochasticRun, days: list[int], config: StochasticConfig,
                        draw: int = 0, seed: int = 314) -> pd.DataFrame:
    """Generate modality-specific observations from one hidden patient trajectory."""
    rng = np.random.default_rng(seed)
    rows = []
    for day in days:
        if day < 0 or day >= run.states.shape[1]:
            raise ValueError("observation day lies outside the simulated trajectory")
        state = run.states[draw, day]
        total = state.sum()
        escape_fraction = state[1] / max(total, np.finfo(float).eps)
        imaging = float(np.exp(rng.normal(np.log(max(total, 1e-8)), config.imaging_log_sd)))
        alt = int(rng.binomial(config.ctdna_depth, np.clip(escape_fraction, 0, 1)))
        immune_day = min(day, run.immune.shape[1] - 1)
        latent = run.immune[draw, immune_day]
        means = 80 * np.exp(np.clip(.55 * latent, -5, 5))
        probability = config.rna_dispersion / (config.rna_dispersion + means)
        rna = rng.negative_binomial(config.rna_dispersion, probability)
        rows.append({"day": day, "imaging_burden": imaging, "ctdna_alt": alt,
                     "ctdna_depth": config.ctdna_depth, "rna_cytotoxic": int(rna[0]),
                     "rna_exhaustion": int(rna[1]), "rna_inflammation": int(rna[2])})
    return pd.DataFrame(rows)


def particle_filter(system: ImmunotherapySystem, kernels: ImmuneKernels, schedule: np.ndarray,
                    initial: np.ndarray, observations: pd.DataFrame,
                    config: StochasticConfig, particles: int = 256,
                    seed: int = 515) -> pd.DataFrame:
    """Bootstrap filter using imaging, ctDNA, and immune-module RNA observations."""
    rng = np.random.default_rng(seed)
    particle_config = replace(config, draws=particles)
    immune = _uncertain_immune(schedule, kernels, particle_config, rng)
    growth, killing, transition = _patient_parameters(system, particles,
                                                      config.patient_log_sd, rng)
    counts = rng.poisson(np.asarray(initial)[None, :] * config.effective_population,
                         size=(particles, 2)).astype(np.int64)
    observation_by_day = observations.set_index("day")
    rows = []
    for day in range(len(schedule) + 1):
        if day in observation_by_day.index:
            observed = observation_by_day.loc[day]
            total = counts.sum(axis=1) / config.effective_population
            escape = np.divide(counts[:, 1], counts.sum(axis=1), out=np.zeros(particles),
                               where=counts.sum(axis=1) > 0)
            log_weight = norm.logpdf(np.log(max(observed.imaging_burden, 1e-8)),
                                     np.log(np.maximum(total, 1e-8)), config.imaging_log_sd)
            log_weight += binom.logpmf(int(observed.ctdna_alt), int(observed.ctdna_depth),
                                      np.clip(escape, 1e-7, 1 - 1e-7))
            immune_day = min(day, immune.shape[1] - 1)
            rna_means = 80 * np.exp(np.clip(.55 * immune[:, immune_day], -5, 5))
            rna_probability = config.rna_dispersion / (config.rna_dispersion + rna_means)
            rna_observed = observed[["rna_cytotoxic", "rna_exhaustion",
                                     "rna_inflammation"]].to_numpy(dtype=int)
            log_weight += nbinom.logpmf(rna_observed[None, :], config.rna_dispersion,
                                       rna_probability).sum(axis=1)
            weight = np.exp(log_weight - np.max(log_weight)); weight /= weight.sum()
            selected = rng.choice(particles, size=particles, replace=True, p=weight)
            counts = counts[selected]; growth = growth[selected]; killing = killing[selected]
            transition = transition[selected]; immune = immune[selected]
        total = counts.sum(axis=1) / config.effective_population
        escape = np.divide(counts[:, 1], counts.sum(axis=1), out=np.zeros(particles),
                           where=counts.sum(axis=1) > 0)
        immune_day = min(day, immune.shape[1] - 1)
        immune_summary = {}
        for channel, name in enumerate(["cytotoxic", "exhaustion", "inflammation"]):
            immune_summary.update({
                f"{name}_p05": float(np.quantile(immune[:, immune_day, channel], .05)),
                f"{name}_median": float(np.median(immune[:, immune_day, channel])),
                f"{name}_p95": float(np.quantile(immune[:, immune_day, channel], .95)),
            })
        rows.append({"day": day,
                     "tumor_p05": float(np.quantile(total, .05)),
                     "tumor_median": float(np.median(total)),
                     "tumor_p95": float(np.quantile(total, .95)),
                     "escape_p05": float(np.quantile(escape, .05)),
                     "escape_median": float(np.median(escape)),
                     "escape_p95": float(np.quantile(escape, .95)),
                     **immune_summary,
                     "observed": bool(day in observation_by_day.index)})
        if day < len(schedule):
            counts = _advance_counts(counts, immune[:, day], growth, killing, transition,
                                     system, config, rng)
    return pd.DataFrame(rows)


def predictive_quantiles(run: StochasticRun) -> pd.DataFrame:
    total = run.states.sum(axis=2)
    escape = np.divide(run.states[:, :, 1], total, out=np.zeros_like(total), where=total > 0)
    rows = []
    for day in range(total.shape[1]):
        rows.append({"day": day,
                     **{f"tumor_{name}": float(np.quantile(total[:, day], q))
                        for name, q in [("p05", .05), ("median", .5), ("p95", .95)]},
                     **{f"escape_{name}": float(np.quantile(escape[:, day], q))
                        for name, q in [("p05", .05), ("median", .5), ("p95", .95)]}})
    return pd.DataFrame(rows)
