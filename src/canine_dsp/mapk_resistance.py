"""Monte Carlo clonal-escape model for MAPK-pathway inhibitor treatment of histiocytic sarcoma.
Canine histiocytic sarcoma (HS) carries recurrent MAPK-pathway driver mutations, dominated by two
PTPN11/SHP2 hotspots (E76K, G503V) that are mutually exclusive with each other and with KRAS Q61H;
together these alter the MAPK pathway in roughly 43-64% of cases across published cohorts (Takada
et al., "Activating Mutations in PTPN11 and KRAS in Canine Histiocytic Sarcomas," Genes
2019;10(7):505, PMID 31277422; "Canine Histiocytic and Hemophagocytic Histiocytic Sarcomas Display
KRAS and Extensive PTPN11/SHP2 Mutations and Respond In Vitro to MEK Inhibition by Cobimetinib,"
Genes 2024;15(8):1050, PMID 39202410). See docs/HS_MAPK_RESISTANCE.md.
"""

from dataclasses import dataclass, replace

import numpy as np

CLONE_NAMES = ["sensitive", "pathway_reactivation", "rtk_bypass", "target_site_mutation"]
PROGRESSION_THRESHOLD = 1.2  # RECIST-style: >=20% increase from nadir counts as progression


@dataclass(frozen=True)
class ResistanceModel:
    growth: np.ndarray        # (k,) per-day intrinsic growth rate, clone 0 = drug-sensitive
    ic50_nM: np.ndarray       # (k,) drug concentration for half-maximal kill rate
    max_kill: np.ndarray      # (k,) per-day kill-rate constant at saturating drug concentration
    mutation: np.ndarray      # (k,k) row-stochastic per-day clone transition matrix
    hill: float = 1.5
    carrying_capacity: float = 1.0
    # Optional second drug. A scalar ic50/max_kill is applied identically to every clone, which is
    # the right model for a *mechanism-agnostic* node -- e.g. a CDK4/6 inhibitor acting on the
    # shared cyclin D/CDK4/6 cell-cycle machinery, which does not care how a clone reactivated
    # proliferative signaling upstream of it.
    #
    # A (k,) array instead specifies per-clone values, which is required for a second drug that is
    # NOT mechanism-agnostic -- specifically, one acting at a node *upstream, on the same serial
    # pathway* as the resistance lesions themselves. A CSF1R inhibitor is the motivating case: every
    # resistance mechanism this module models, and every candidate driver in `histiocytic_origin`
    # (PTPN11/SHP2, KRAS, NRAS, BRAF, MAP2K1), is constitutively active *downstream* of CSF1R, so
    # blocking the receptor cannot suppress them -- that is what "downstream activating mutation"
    # means. Modeling such a drug with a scalar would silently credit it with resistance coverage it
    # cannot have. See `mapk_scenarios.csf1r_combination_scenarios`.
    #
    # None (default) leaves single-drug behavior unchanged.
    ic50_nM_2: float | np.ndarray | None = None
    max_kill_2: float | np.ndarray | None = None
    hill_2: float = 1.5

    def __post_init__(self):
        k = len(np.asarray(self.growth))
        for name in ("ic50_nM", "max_kill"):
            if np.asarray(getattr(self, name)).shape != (k,):
                raise ValueError(f"{name} must contain one value per clone")
        for name in ("ic50_nM_2", "max_kill_2"):
            value = getattr(self, name)
            if value is not None and np.ndim(value) != 0 and np.asarray(value).shape != (k,):
                raise ValueError(f"{name} must be a scalar (mechanism-agnostic) or contain one "
                                 f"value per clone (pathway-specific); got shape "
                                 f"{np.asarray(value).shape} for k={k} clones")
        mutation = np.asarray(self.mutation)
        if mutation.shape != (k, k) or np.any(mutation < 0):
            raise ValueError("mutation must be a nonnegative clone-by-clone matrix")
        if not np.allclose(mutation.sum(axis=1), 1):
            raise ValueError("mutation rows must sum to one")


def drug_kill_rate(concentration, ic50_nM, hill: float, max_kill) -> np.ndarray:
    """Emax pharmacodynamic model: per-day kill rate rising toward `max_kill` with concentration."""
    c = np.maximum(np.asarray(concentration, dtype=float), 0.0)
    ic50 = np.maximum(np.asarray(ic50_nM, dtype=float), 1e-9)
    return max_kill * c ** hill / (ic50 ** hill + c ** hill)


def simulate_resistance(model: ResistanceModel, concentration: np.ndarray, initial: np.ndarray,
                        injections: dict[int, np.ndarray] | None = None,
                        concentration_2: np.ndarray | None = None,
                        additional_kill: np.ndarray | None = None) -> np.ndarray:
    """Simulate density-dependent multiclone tumor burden under a daily drug-concentration series.
    Net growth is logistic growth minus an Emax drug kill-rate term, so a clone whose kill rate
    exceeds its growth rate actually regresses (not just plateaus) -- required for "response, then
    progression from nadir" dynamics, rather than the drug only ever capping growth at zero.
    """
    initial = np.asarray(initial, float)
    state = np.zeros((len(concentration) + 1, len(initial)))
    state[0] = initial
    has_second_drug = concentration_2 is not None and model.ic50_nM_2 is not None
    for t, c in enumerate(np.asarray(concentration, float)):
        current = state[t]
        density = current.sum() / model.carrying_capacity
        kill = drug_kill_rate(c, model.ic50_nM, model.hill, model.max_kill)
        if has_second_drug:
            kill = kill + drug_kill_rate(concentration_2[t], model.ic50_nM_2, model.hill_2, model.max_kill_2)
        if additional_kill is not None:
            kill = kill + additional_kill[t]
        net = model.growth * (1 - density) - kill
        grown = current * np.exp(np.clip(net, -30, 30))
        state[t + 1] = grown @ model.mutation
        if injections and (t + 1) in injections:
            state[t + 1] = state[t + 1] + injections[t + 1]
    return state


def ramping_kill_schedule(horizon_days: int, start_day: int, ramp_days: float, max_kill: float,
                          applicable_clones: np.ndarray) -> np.ndarray:
    """Time-gated, saturating kill-rate schedule for a vaccine-type mechanism. Zero before
    `start_day`; rises as `1 - exp(-elapsed / ramp_days)` toward `max_kill` after, representing
    T-cell priming/expansion kinetics (a real ~1-3 week immunology timescale, not vaccine- or
    antigen-specific measured data) -- deliberately time-dependent rather than the
    concentration-dependent Emax shape used for the small-molecule drugs, since immune effector
    buildup is not governed by a plasma concentration.
    """
    days = np.arange(horizon_days)
    ramp = np.where(days >= start_day, 1 - np.exp(-(days - start_day) / ramp_days), 0.0)
    mask = np.asarray(applicable_clones, dtype=float)
    return np.outer(ramp * max_kill, mask)


def merge_injections(a: dict[int, np.ndarray], b: dict[int, np.ndarray]) -> dict[int, np.ndarray]:
    """Combine two day-keyed Poisson-injection dictionaries (see `poisson_mutation_injections`),
    summing population vectors on days present in both."""
    merged = {day: vector.copy() for day, vector in a.items()}
    for day, vector in b.items():
        merged[day] = merged[day] + vector if day in merged else vector.copy()
    return merged


def build_mutation_matrix(seeding_rates: np.ndarray) -> np.ndarray:
    """Row-stochastic matrix: the sensitive clone seeds each resistant clone at `seeding_rates`
    per day; resistant clones neither revert nor interconvert."""
    k = len(seeding_rates) + 1
    mutation = np.eye(k)
    mutation[0, 0] = 1 - np.sum(seeding_rates)
    mutation[0, 1:] = seeding_rates
    return mutation


def perturb_resistance_model(model: ResistanceModel, rng: np.random.Generator,
                             ic50_scale: float = .2, mutation_scale: float = .4) -> ResistanceModel:
    """Draw a nearby model for a Monte Carlo uncertainty ensemble."""
    ic50 = model.ic50_nM * rng.lognormal(0, ic50_scale, len(model.ic50_nM))
    k = len(model.growth)
    mutation = model.mutation.copy()
    for i in range(k):
        off_diagonal = [j for j in range(k) if j != i and mutation[i, j] > 0]
        for j in off_diagonal:
            mutation[i, j] *= rng.lognormal(0, mutation_scale)
        mutation[i, i] = 1 - sum(mutation[i, j] for j in off_diagonal)
    updates = {"ic50_nM": ic50, "mutation": mutation}
    if model.ic50_nM_2 is not None:
        updates["ic50_nM_2"] = model.ic50_nM_2 * rng.lognormal(0, ic50_scale)
    return replace(model, **updates)


def poisson_mutation_injections(rng: np.random.Generator, sensitive_trajectory: np.ndarray,
                                seeding_rates: np.ndarray, seed_fraction: float = 1e-8,
                                clone_indices: range | list[int] | None = None,
                                k: int | None = None) -> dict[int, np.ndarray]:
    """Schedule acquired-resistance establishment as a Poisson process over a source population's
    cumulative cell-days (usually the sensitive clone's trajectory). Expected establishment count
    for `seeding_rates[i]` is `seeding_rates[i] * sum(trajectory)`. Unlike a constant per-day
    transfer fraction, a Poisson draw can come back exactly zero, so a resistant lineage can
    genuinely never arise in a given trial -- a rate small enough to make that likely is required
    to reproduce multi-year durable responses; a fixed nonzero daily seeding rate cannot, since it
    guarantees eventual outgrowth given enough follow-up time.
    """
    total_cell_days = float(sensitive_trajectory.sum())
    injections: dict[int, np.ndarray] = {}
    if total_cell_days <= 0:
        return injections
    weights = sensitive_trajectory / total_cell_days
    if clone_indices is None:
        clone_indices = range(1, len(seeding_rates) + 1)
    if k is None:
        k = len(seeding_rates) + 1
    for clone_index, rate in zip(clone_indices, seeding_rates):
        for _ in range(rng.poisson(rate * total_cell_days)):
            day = int(rng.choice(len(sensitive_trajectory), p=weights))
            vector = injections.setdefault(day, np.zeros(k))
            vector[clone_index] += seed_fraction
    return injections


def sample_initial_state(rng: np.random.Generator, k: int, preexisting_prob: float,
                         mechanism_weights: np.ndarray | None = None,
                         initial_burden: float = .3) -> np.ndarray:
    """Most trials start drug-sensitive only; some seed one pre-existing resistant subclone,
    reflecting that a resistant population may or may not already exist before treatment.
    `mechanism_weights` (typically the same relative seeding rates used for acquired resistance)
    picks which mechanism is more likely to already be present; without it, all mechanisms are
    equally likely, which would ignore that some escape routes are mutationally more accessible
    than others.
    """
    state = np.zeros(k)
    resistant_fraction = 0.0
    if rng.random() < preexisting_prob:
        if mechanism_weights is None:
            mechanism = int(rng.integers(1, k))
        else:
            weights = np.asarray(mechanism_weights, dtype=float)
            mechanism = 1 + int(rng.choice(len(weights), p=weights / weights.sum()))
        resistant_fraction = float(10 ** rng.uniform(-6, -3))
        state[mechanism] = resistant_fraction
    state[0] = 1 - resistant_fraction
    return state * initial_burden


@dataclass
class MonteCarloOutcome:
    trajectories: np.ndarray          # (trials, days+1, k)
    progressed: np.ndarray            # (trials,) bool
    time_to_progression: np.ndarray   # (trials,) float days; nan if not progressed by horizon
    dominant_mechanism: list[str]     # per trial, "durable_response" if not progressed


def _dominant_mechanism(state_final: np.ndarray, progressed: bool,
                        clone_names: list[str] = CLONE_NAMES) -> str:
    if not progressed:
        return "durable_response"
    resistant = state_final[1:]
    if resistant.sum() <= 0:
        return "durable_response"
    return clone_names[1 + int(np.argmax(resistant))]


def run_monte_carlo(reference: ResistanceModel, css_reference: float, horizon_days: int,
                   seeding_rates: np.ndarray, trials: int = 500, preexisting_prob: float = .3,
                   exposure_scale: float = .3, seeding_rate_scale: float = .5,
                   seed_fraction: float = 1e-8, detection_floor_fraction: float = .01,
                   initial_burden: float = .3, css_reference_2: float | None = None,
                   exposure_scale_2: float = .3, css_reference_2_duration_days: int | None = None,
                   seed: int = 7) -> MonteCarloOutcome:
    """Run a Monte Carlo ensemble over parameter, exposure, and acquired-mutation-timing uncertainty.
    Acquired resistance is scheduled with `poisson_mutation_injections` rather than a constant
    daily transfer out of `reference.mutation` (`reference` is simulated with mutation forced to
    identity), so a real fraction of trials can see no acquired resistance ever establish.
    """
    rng = np.random.default_rng(seed)
    k = len(reference.growth)
    identity_model = replace(reference, mutation=np.eye(k))
    detection_floor = detection_floor_fraction * reference.carrying_capacity
    trajectories = np.zeros((trials, horizon_days + 1, k))
    progressed = np.zeros(trials, dtype=bool)
    time_to_progression = np.full(trials, np.nan)
    dominant_mechanism = []
    for trial in range(trials):
        model = perturb_resistance_model(identity_model, rng)
        css = css_reference * rng.lognormal(0, exposure_scale)
        concentration = np.full(horizon_days, css)
        concentration_2 = None
        if css_reference_2 is not None:
            css_2 = css_reference_2 * rng.lognormal(0, exposure_scale_2)
            concentration_2 = np.full(horizon_days, css_2)
            if css_reference_2_duration_days is not None:
                concentration_2[css_reference_2_duration_days:] = 0.0
        initial = sample_initial_state(rng, k, preexisting_prob, mechanism_weights=seeding_rates,
                                       initial_burden=initial_burden)
        sensitive_only = np.zeros(k)
        sensitive_only[0] = initial[0]
        sensitive_trajectory = simulate_resistance(model, concentration, sensitive_only,
                                                    concentration_2=concentration_2)[:, 0]
        jittered_rates = seeding_rates * rng.lognormal(0, seeding_rate_scale, len(seeding_rates))
        injections = poisson_mutation_injections(rng, sensitive_trajectory, jittered_rates, seed_fraction)
        state = simulate_resistance(model, concentration, initial, injections, concentration_2)
        trajectories[trial] = state
        total = state.sum(axis=1)
        nadir_day = int(np.argmin(total))
        threshold = max(PROGRESSION_THRESHOLD * total[nadir_day], detection_floor)
        progression_days = np.flatnonzero(total[nadir_day:] >= threshold)
        trial_progressed = progression_days.size > 0 and progression_days[0] > 0
        progressed[trial] = trial_progressed
        if trial_progressed:
            time_to_progression[trial] = nadir_day + progression_days[0]
        dominant_mechanism.append(_dominant_mechanism(state[-1], trial_progressed))
    return MonteCarloOutcome(trajectories, progressed, time_to_progression, dominant_mechanism)


def clone_growth_margins(model: ResistanceModel, concentration: float,
                         concentration_2: float | None = None) -> np.ndarray:
    """Deterministic per-clone net growth margin (growth minus drug kill) at a fixed, sustained drug
    concentration, ignoring density-dependence (valid at low tumor burden, where the logistic term
    is negligible) and mutation transfer. A positive margin means that clone's fitness advantage
    is not reversed at this exposure: it will eventually regrow given enough follow-up time from
    *any* nonzero foothold, however small -- unlike a Monte Carlo trial's empirical progression
    outcome, which also depends on whether/when that foothold is seeded at all and how much
    follow-up time remains to detect it.
    """
    kill = drug_kill_rate(concentration, model.ic50_nM, model.hill, model.max_kill)
    if concentration_2 is not None and model.ic50_nM_2 is not None:
        kill = kill + drug_kill_rate(concentration_2, model.ic50_nM_2, model.hill_2, model.max_kill_2)
    return model.growth - kill


def run_monte_carlo_fixed_patient(model: ResistanceModel, css: float, horizon_days: int,
                                  seeding_rates: np.ndarray, initial: np.ndarray, repeats: int = 200,
                                  seed_fraction: float = 1e-8, detection_floor_fraction: float = .01,
                                  css_2: float | None = None, additional_kill: np.ndarray | None = None,
                                  clone_names: list[str] = CLONE_NAMES, seed: int = 7
                                  ) -> MonteCarloOutcome:
    """Repeats only the stochastic mutation-establishment process for one *given* dog's fixed model,
    drug exposure, and starting tumor state, instead of redrawing a new hypothetical dog every
    trial the way `run_monte_carlo` does. `run_monte_carlo` reports population variability: which
    dog you are.
    """
    k = len(model.growth)
    rng = np.random.default_rng(seed)
    concentration = np.full(horizon_days, css)
    concentration_2 = np.full(horizon_days, css_2) if css_2 is not None else None
    detection_floor = detection_floor_fraction * model.carrying_capacity
    sensitive_only = np.zeros(k)
    sensitive_only[0] = initial[0]
    # Deterministic given a fixed model/concentration/initial state -- computed once, not per
    # repeat, since only the Poisson mutation-timing draw below is meant to vary across repeats.
    sensitive_trajectory = simulate_resistance(model, concentration, sensitive_only,
                                                concentration_2=concentration_2)[:, 0]

    trajectories = np.zeros((repeats, horizon_days + 1, k))
    progressed = np.zeros(repeats, dtype=bool)
    time_to_progression = np.full(repeats, np.nan)
    dominant_mechanism = []
    for trial in range(repeats):
        injections = poisson_mutation_injections(rng, sensitive_trajectory, seeding_rates, seed_fraction)
        state = simulate_resistance(model, concentration, initial, injections, concentration_2,
                                    additional_kill=additional_kill)
        trajectories[trial] = state
        total = state.sum(axis=1)
        nadir_day = int(np.argmin(total))
        threshold = max(PROGRESSION_THRESHOLD * total[nadir_day], detection_floor)
        progression_days = np.flatnonzero(total[nadir_day:] >= threshold)
        trial_progressed = progression_days.size > 0 and progression_days[0] > 0
        progressed[trial] = trial_progressed
        if trial_progressed:
            time_to_progression[trial] = nadir_day + progression_days[0]
        dominant_mechanism.append(_dominant_mechanism(state[-1], trial_progressed, clone_names))
    return MonteCarloOutcome(trajectories, progressed, time_to_progression, dominant_mechanism)


@dataclass
class UncertaintyDecomposition:
    per_dog_durable_probability: np.ndarray  # (n_dogs,) each dog's own true durable-response rate
    between_dog_variance: float    # uncertainty a real diagnostic on THIS dog could resolve
    within_dog_variance: float     # irreducible: exists even with perfect knowledge of the dog
    intraclass_correlation: float  # between / (between + within); near 1 => "which dog" dominates


def decompose_patient_uncertainty(reference: ResistanceModel, css_reference: float, horizon_days: int,
                                  seeding_rates: np.ndarray, n_dogs: int = 40, repeats_per_dog: int = 60,
                                  preexisting_prob: float = .3, exposure_scale: float = .3,
                                  seeding_rate_scale: float = .5, ic50_scale: float = .2,
                                  seed_fraction: float = 1e-8, detection_floor_fraction: float = .01,
                                  initial_burden: float = .3, css_reference_2: float | None = None,
                                  exposure_scale_2: float = .3, seed: int = 7) -> UncertaintyDecomposition:
    """Decomposes `run_monte_carlo`'s population variability into between-dog and within-dog parts.
    Draws `n_dogs` distinct hypothetical dogs from the same distributions `run_monte_carlo` uses
    (perturbed model, drug exposure, starting tumor state, mutation-rate jitter), then for each
    one runs `repeats_per_dog` fixed-patient trials (`run_monte_carlo_fixed_patient`) to estimate
    that dog's own true durable-response probability.
    """
    rng = np.random.default_rng(seed)
    k = len(reference.growth)
    identity_model = replace(reference, mutation=np.eye(k))
    per_dog_probability = np.zeros(n_dogs)
    for dog in range(n_dogs):
        model = perturb_resistance_model(identity_model, rng, ic50_scale=ic50_scale)
        css = css_reference * rng.lognormal(0, exposure_scale)
        css_2 = (css_reference_2 * rng.lognormal(0, exposure_scale_2)
                if css_reference_2 is not None else None)
        initial = sample_initial_state(rng, k, preexisting_prob, mechanism_weights=seeding_rates,
                                       initial_burden=initial_burden)
        jittered_rates = seeding_rates * rng.lognormal(0, seeding_rate_scale, len(seeding_rates))
        outcome = run_monte_carlo_fixed_patient(
            model, css, horizon_days, jittered_rates, initial, repeats=repeats_per_dog,
            seed_fraction=seed_fraction, detection_floor_fraction=detection_floor_fraction,
            css_2=css_2, seed=int(rng.integers(0, 2**32 - 1)))
        per_dog_probability[dog] = 1 - outcome.progressed.mean()
    within = float(np.mean(per_dog_probability * (1 - per_dog_probability)))
    naive_between = float(np.var(per_dog_probability, ddof=1)) if n_dogs > 1 else 0.0
    between = max(0.0, naive_between - within / repeats_per_dog)
    icc = between / (between + within) if (between + within) > 0 else 0.0
    return UncertaintyDecomposition(per_dog_probability, between, within, icc)


def run_monte_carlo_with_vaccine(reference: ResistanceModel, css_reference: float, horizon_days: int,
                                seeding_rates: np.ndarray, vaccine_start_day: int, vaccine_ramp_days: float,
                                vaccine_max_kill: float, immune_escape_seeding_rate: float,
                                clone_names: list[str], trials: int = 500, preexisting_prob: float = .3,
                                exposure_scale: float = .3, seeding_rate_scale: float = .5,
                                seed_fraction: float = 1e-8, detection_floor_fraction: float = .01,
                                initial_burden: float = .3, css_reference_2: float | None = None,
                                exposure_scale_2: float = .3, immune_escape_seed_fraction: float = 1e-8,
                                css_reference_2_duration_days: int | None = None,
                                seed: int = 7) -> MonteCarloOutcome:
    """Adds a time-gated vaccine kill term and a 5th, antigen-loss/immune-escape clone on top of
    `run_monte_carlo`'s drug-resistance model. `reference` must have one more clone than its
    drug-resistance-only counterpart -- the last index is treated as the immune-escape clone and
    is excluded from the vaccine's kill term (see `ramping_kill_schedule`), since the entire
    premise of that clone is that it is not recognized.
    """
    rng = np.random.default_rng(seed)
    k = len(reference.growth)
    immune_escape_index = k - 1
    applicable_clones = np.ones(k)
    applicable_clones[immune_escape_index] = 0.0
    identity_model = replace(reference, mutation=np.eye(k))
    detection_floor = detection_floor_fraction * reference.carrying_capacity
    vaccine_kill = ramping_kill_schedule(horizon_days, vaccine_start_day, vaccine_ramp_days,
                                        vaccine_max_kill, applicable_clones)
    # immune escape is not modeled as pre-existing at treatment start (weight 0): there is no
    # immune pressure yet to select for it, unlike the three drug-resistance mechanisms.
    mechanism_weights = np.concatenate([np.asarray(seeding_rates, dtype=float), [0.0]])
    days_index = np.arange(horizon_days + 1)

    trajectories = np.zeros((trials, horizon_days + 1, k))
    progressed = np.zeros(trials, dtype=bool)
    time_to_progression = np.full(trials, np.nan)
    dominant_mechanism = []
    for trial in range(trials):
        model = perturb_resistance_model(identity_model, rng)
        css = css_reference * rng.lognormal(0, exposure_scale)
        concentration = np.full(horizon_days, css)
        concentration_2 = None
        if css_reference_2 is not None:
            css_2 = css_reference_2 * rng.lognormal(0, exposure_scale_2)
            concentration_2 = np.full(horizon_days, css_2)
            if css_reference_2_duration_days is not None:
                concentration_2[css_reference_2_duration_days:] = 0.0
        initial = sample_initial_state(rng, k, preexisting_prob, mechanism_weights=mechanism_weights,
                                       initial_burden=initial_burden)
        sensitive_only = np.zeros(k)
        sensitive_only[0] = initial[0]
        sensitive_trajectory = simulate_resistance(model, concentration, sensitive_only,
                                                    concentration_2=concentration_2)[:, 0]
        jittered_rates = seeding_rates * rng.lognormal(0, seeding_rate_scale, len(seeding_rates))
        drug_injections = poisson_mutation_injections(rng, sensitive_trajectory, jittered_rates,
                                                       seed_fraction,
                                                       clone_indices=range(1, immune_escape_index), k=k)

        # provisional run (drug + vaccine pressure, drug-resistance escapes seeded, no immune
        # escape yet) purely to obtain the antigen-positive population's cell-days for seeding
        # the immune-escape clone -- not itself a reported trajectory.
        provisional = simulate_resistance(model, concentration, initial, drug_injections,
                                          concentration_2, additional_kill=vaccine_kill)
        antigen_positive_trajectory = provisional[:, :immune_escape_index].sum(axis=1)
        antigen_positive_trajectory = np.where(days_index >= vaccine_start_day,
                                               antigen_positive_trajectory, 0.0)
        jittered_escape_rate = immune_escape_seeding_rate * rng.lognormal(0, seeding_rate_scale)
        escape_injections = poisson_mutation_injections(rng, antigen_positive_trajectory,
                                                        np.array([jittered_escape_rate]),
                                                        immune_escape_seed_fraction,
                                                        clone_indices=[immune_escape_index], k=k)
        injections = merge_injections(drug_injections, escape_injections)
        state = simulate_resistance(model, concentration, initial, injections, concentration_2,
                                    additional_kill=vaccine_kill)
        trajectories[trial] = state
        total = state.sum(axis=1)
        nadir_day = int(np.argmin(total))
        threshold = max(PROGRESSION_THRESHOLD * total[nadir_day], detection_floor)
        progression_days = np.flatnonzero(total[nadir_day:] >= threshold)
        trial_progressed = progression_days.size > 0 and progression_days[0] > 0
        progressed[trial] = trial_progressed
        if trial_progressed:
            time_to_progression[trial] = nadir_day + progression_days[0]
        dominant_mechanism.append(_dominant_mechanism(state[-1], trial_progressed, clone_names))
    return MonteCarloOutcome(trajectories, progressed, time_to_progression, dominant_mechanism)


@dataclass
class TwoCompartmentOutcome:
    primary_trajectories: np.ndarray    # (trials, days+1, k)
    nodal_trajectories: np.ndarray      # (trials, days+1, k) -- all-zero for trials with no nodal disease
    has_nodal_involvement: np.ndarray   # (trials,) bool
    progressed: np.ndarray              # (trials,) bool, based on primary+nodal combined burden
    time_to_progression: np.ndarray
    dominant_mechanism: list[str]
    dominant_compartment: list[str]     # "primary", "nodal", or "none" (durable response)


def run_monte_carlo_two_compartment(reference: ResistanceModel, css_reference: float, horizon_days: int,
                                    seeding_rates: np.ndarray, nodal_involvement_prob: float,
                                    nodal_seed_fraction: float, debulking_fraction: float = 0.0,
                                    trials: int = 500, preexisting_prob: float = .3,
                                    exposure_scale: float = .3, seeding_rate_scale: float = .5,
                                    seed_fraction: float = 1e-8, detection_floor_fraction: float = .01,
                                    initial_burden: float = .3, css_reference_2: float | None = None,
                                    exposure_scale_2: float = .3,
                                    css_reference_2_duration_days: int | None = None,
                                    vaccine_start_day: int | None = None,
                                    vaccine_ramp_days: float = 21.0, vaccine_max_kill: float = 0.0,
                                    immune_escape_seeding_rate: float = 0.0,
                                    immune_escape_seed_fraction: float = 1e-8,
                                    clone_names: list[str] = CLONE_NAMES,
                                    seed: int = 7) -> TwoCompartmentOutcome:
    """A two-compartment extension of `run_monte_carlo` for a resectable primary tumor that may
    already have seeded regional (e.g. lymph node) disease before surgery -- unlike
    `run_monte_carlo`'s single-compartment model, which implicitly assumes debulking reaches every
    tumor cell wherever it is. Per trial: a single perturbed model, drug exposure, and
    primary-tumor initial state are drawn exactly as in `run_monte_carlo`.
    """
    rng = np.random.default_rng(seed)
    k = len(reference.growth)
    identity_model = replace(reference, mutation=np.eye(k))
    detection_floor = detection_floor_fraction * reference.carrying_capacity
    vaccine_active = vaccine_start_day is not None
    if vaccine_active:
        immune_escape_index = k - 1
        applicable_clones = np.ones(k)
        applicable_clones[immune_escape_index] = 0.0
        vaccine_kill = ramping_kill_schedule(horizon_days, vaccine_start_day, vaccine_ramp_days,
                                            vaccine_max_kill, applicable_clones)
        # immune escape is never pre-existing: no immune pressure exists yet to select for it.
        mechanism_weights = np.concatenate([np.asarray(seeding_rates, dtype=float), [0.0]])
        drug_clone_indices = range(1, immune_escape_index)
        days_index = np.arange(horizon_days + 1)
    else:
        vaccine_kill = None
        mechanism_weights = seeding_rates
        drug_clone_indices = None
        days_index = None

    primary_trajectories = np.zeros((trials, horizon_days + 1, k))
    nodal_trajectories = np.zeros((trials, horizon_days + 1, k))
    has_nodal_involvement = np.zeros(trials, dtype=bool)
    progressed = np.zeros(trials, dtype=bool)
    time_to_progression = np.full(trials, np.nan)
    dominant_mechanism = []
    dominant_compartment = []
    for trial in range(trials):
        model = perturb_resistance_model(identity_model, rng)
        css = css_reference * rng.lognormal(0, exposure_scale)
        concentration = np.full(horizon_days, css)
        concentration_2 = None
        if css_reference_2 is not None:
            css_2 = css_reference_2 * rng.lognormal(0, exposure_scale_2)
            concentration_2 = np.full(horizon_days, css_2)
            if css_reference_2_duration_days is not None:
                concentration_2[css_reference_2_duration_days:] = 0.0

        pre_debulking_primary = sample_initial_state(rng, k, preexisting_prob,
                                                      mechanism_weights=mechanism_weights,
                                                      initial_burden=initial_burden)
        primary_initial = pre_debulking_primary * (1 - debulking_fraction)
        has_nodal = bool(rng.random() < nodal_involvement_prob)
        has_nodal_involvement[trial] = has_nodal
        nodal_initial = pre_debulking_primary * nodal_seed_fraction if has_nodal else np.zeros(k)

        compartment_states = []
        for initial in (primary_initial, nodal_initial):
            sensitive_only = np.zeros(k)
            sensitive_only[0] = initial[0]
            sensitive_trajectory = simulate_resistance(model, concentration, sensitive_only,
                                                        concentration_2=concentration_2)[:, 0]
            jittered_rates = seeding_rates * rng.lognormal(0, seeding_rate_scale, len(seeding_rates))
            injections = poisson_mutation_injections(rng, sensitive_trajectory, jittered_rates,
                                                     seed_fraction,
                                                     clone_indices=drug_clone_indices, k=k)
            if vaccine_active:
                # Provisional run to get this compartment's own antigen-positive cell-days, exactly
                # as run_monte_carlo_with_vaccine does -- seeded per compartment because the two are
                # separate populations after metastatic spread.
                provisional = simulate_resistance(model, concentration, initial, injections,
                                                  concentration_2, additional_kill=vaccine_kill)
                antigen_positive = provisional[:, :immune_escape_index].sum(axis=1)
                antigen_positive = np.where(days_index >= vaccine_start_day, antigen_positive, 0.0)
                jittered_escape_rate = immune_escape_seeding_rate * rng.lognormal(
                    0, seeding_rate_scale)
                escape_injections = poisson_mutation_injections(
                    rng, antigen_positive, np.array([jittered_escape_rate]),
                    immune_escape_seed_fraction, clone_indices=[immune_escape_index], k=k)
                injections = merge_injections(injections, escape_injections)
            state = simulate_resistance(model, concentration, initial, injections, concentration_2,
                                        additional_kill=vaccine_kill)
            compartment_states.append(state)
        primary_state, nodal_state = compartment_states
        primary_trajectories[trial] = primary_state
        nodal_trajectories[trial] = nodal_state

        total = primary_state.sum(axis=1) + nodal_state.sum(axis=1)
        nadir_day = int(np.argmin(total))
        threshold = max(PROGRESSION_THRESHOLD * total[nadir_day], detection_floor)
        progression_days = np.flatnonzero(total[nadir_day:] >= threshold)
        trial_progressed = progression_days.size > 0 and progression_days[0] > 0
        progressed[trial] = trial_progressed
        if trial_progressed:
            time_to_progression[trial] = nadir_day + progression_days[0]
        combined_final = primary_state[-1] + nodal_state[-1]
        dominant_mechanism.append(_dominant_mechanism(combined_final, trial_progressed, clone_names))
        if not trial_progressed:
            dominant_compartment.append("none")
        else:
            primary_resistant = primary_state[-1, 1:].sum()
            nodal_resistant = nodal_state[-1, 1:].sum()
            dominant_compartment.append("nodal" if nodal_resistant > primary_resistant else "primary")
    return TwoCompartmentOutcome(primary_trajectories, nodal_trajectories, has_nodal_involvement,
                                 progressed, time_to_progression, dominant_mechanism, dominant_compartment)
