"""Vaccine height vs persistence: waning immunity, booster schedules, and 10-year durability.

See docs/HSA_DURABLE_RESPONSE.md for the analysis these functions support.
"""

import numpy as np

from .mapk_resistance import PROGRESSION_THRESHOLD, merge_injections, perturb_resistance_model
from .mapk_resistance import poisson_mutation_injections, sample_initial_state, simulate_resistance
from dataclasses import replace

# Bar a persistent mechanism must out-kill, from clone_growth_margins at dog_hsa_preset.
DURABILITY_BAR_PER_DAY = 0.0515

# Implied by ERstrePs and eVim (each ~+30pp of 1-year survival). Upper bound: the trials report
# survival, the engine reports progression-free.
REAL_TRIAL_IMPLIED_MAX_KILL = 0.03

# 10-year durable response. Boosting does not move a sub-threshold vaccine; height and persistence
# are independent requirements.
BOOSTERS_DO_NOT_SUBSTITUTE_FOR_POTENCY = {
    0.03: {"never_wanes": 0.492, "wanes_180d_boosted_q60d": 0.492},
    0.04: {"never_wanes": 0.536, "wanes_180d_boosted_q60d": 0.536},
    0.05: {"never_wanes": 0.924, "wanes_180d_boosted_q60d": 0.916},
    0.06: {"never_wanes": 1.000, "wanes_180d_boosted_q60d": 1.000},
}

# At threshold potency (0.06), by immunity half-life. The engine's no-waning default carries the
# headline 1.000; with waning and no boosters it falls to roughly the no-vaccine level.
BOOSTER_REQUIREMENT_AT_THRESHOLD = {
    90:   {"no_boosters": 0.268, "q180d": 0.528, "q60d": 1.000},
    180:  {"no_boosters": 0.300, "q180d": 1.000, "q60d": 1.000},
    365:  {"no_boosters": 0.296, "q180d": 1.000, "q60d": 1.000},
    None: {"no_boosters": 1.000, "q180d": 1.000, "q60d": 1.000},
}

# q60d maintenance (eVim's real schedule) stopped after N years; half-life 180 d, potency 0.06.
STOPPING_BOOSTERS_AT_THRESHOLD = {1: 0.276, 2: 0.436, 5: 0.536, None: 1.000}

EVIM_MAINTENANCE_INTERVAL_DAYS = 60  # Engbersen et al. 2025, PMID 41009669


def immunity_schedule(horizon_days: int, start_day: int, ramp_days: float, max_kill: float,
                      applicable_clones: np.ndarray, half_life_days: float | None = None,
                      booster_interval_days: int | None = None,
                      n_boosters: int | None = None) -> np.ndarray:
    """Per-dose kernels superposed and capped at `max_kill`. Each dose at day d contributes `max_kill
    * (1 - exp(-D/ramp)) * exp(-ln2*D/half_life)` for D >= 0. `half_life_days=None` disables
    decay, so a single dose reproduces `mapk_resistance.ramping_kill_schedule` exactly.
    """
    if ramp_days <= 0:
        raise ValueError("ramp_days must be positive")
    if half_life_days is not None and half_life_days <= 0:
        raise ValueError("half_life_days must be positive or None")
    days = np.arange(horizon_days)
    doses = [start_day]
    if booster_interval_days:
        day = start_day + booster_interval_days
        while day < horizon_days and (n_boosters is None or len(doses) <= n_boosters):
            doses.append(day)
            day += booster_interval_days
    decay = 0.0 if half_life_days is None else np.log(2) / half_life_days
    level = np.zeros(horizon_days)
    for dose_day in doses:
        elapsed = np.maximum(days - dose_day, 0)
        rise = np.where(days >= dose_day, 1 - np.exp(-elapsed / ramp_days), 0.0)
        level += max_kill * rise * np.exp(-decay * elapsed)
    return np.outer(np.minimum(level, max_kill), np.asarray(applicable_clones, dtype=float))


def run_with_schedule(reference, css_reference: float, horizon_days: int, seeding_rates: np.ndarray,
                      vaccine_kill: np.ndarray, vaccine_start_day: int,
                      immune_escape_seeding_rate: float, trials: int = 250,
                      preexisting_prob: float = .7, exposure_scale: float = .3,
                      seeding_rate_scale: float = .5, seed_fraction: float = 1e-8,
                      detection_floor_fraction: float = .01, initial_burden: float = .3,
                      seed: int = 7) -> np.ndarray:
    """`run_monte_carlo_with_vaccine` with a caller-supplied kill schedule instead of a ramp.

    Returns the per-trial progressed flags. Same two independent Poisson processes: drug resistance
    seeded from the sensitive clone's cell-days, immune escape from the antigen-positive
    population's cell-days on or after `vaccine_start_day`.
    """
    rng = np.random.default_rng(seed)
    k = len(reference.growth)
    escape_index = k - 1
    identity = replace(reference, mutation=np.eye(k))
    floor = detection_floor_fraction * reference.carrying_capacity
    weights = np.concatenate([np.asarray(seeding_rates, dtype=float), [0.0]])
    days_index = np.arange(horizon_days + 1)
    progressed = np.zeros(trials, dtype=bool)
    for trial in range(trials):
        model = perturb_resistance_model(identity, rng)
        concentration = np.full(horizon_days, css_reference * rng.lognormal(0, exposure_scale))
        initial = sample_initial_state(rng, k, preexisting_prob, mechanism_weights=weights,
                                       initial_burden=initial_burden)
        sensitive_only = np.zeros(k)
        sensitive_only[0] = initial[0]
        trajectory = simulate_resistance(model, concentration, sensitive_only)[:, 0]
        jittered = np.asarray(seeding_rates, float) * rng.lognormal(0, seeding_rate_scale,
                                                                    len(seeding_rates))
        drug = poisson_mutation_injections(rng, trajectory, jittered, seed_fraction,
                                           clone_indices=range(1, escape_index), k=k)
        provisional = simulate_resistance(model, concentration, initial, drug,
                                          additional_kill=vaccine_kill)
        antigen_positive = np.where(days_index >= vaccine_start_day,
                                    provisional[:, :escape_index].sum(axis=1), 0.0)
        escape = poisson_mutation_injections(
            rng, antigen_positive,
            np.array([immune_escape_seeding_rate * rng.lognormal(0, seeding_rate_scale)]),
            seed_fraction, clone_indices=[escape_index], k=k)
        state = simulate_resistance(model, concentration, initial, merge_injections(drug, escape),
                                    additional_kill=vaccine_kill)
        total = state.sum(axis=1)
        nadir = int(np.argmin(total))
        hits = np.flatnonzero(total[nadir:] >= max(PROGRESSION_THRESHOLD * total[nadir], floor))
        progressed[trial] = hits.size > 0 and hits[0] > 0
    return progressed


def required_booster_interval(half_life_days: float, retained_fraction: float = 0.8) -> float:
    """Longest booster interval holding immunity at >= `retained_fraction` of peak.

    Height must already exceed the bar; this only says how often to re-dose to keep it there.
    """
    if not 0 < retained_fraction < 1:
        raise ValueError("retained_fraction must lie in (0, 1)")
    if half_life_days <= 0:
        raise ValueError("half_life_days must be positive")
    return float(-half_life_days * np.log(retained_fraction) / np.log(2))
