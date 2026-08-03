"""Monte Carlo clonal-escape model for MAPK-pathway inhibitor treatment of histiocytic sarcoma.

Canine histiocytic sarcoma (HS) carries recurrent MAPK-pathway driver mutations, dominated by
two PTPN11/SHP2 hotspots (E76K, G503V) that are mutually exclusive with each other and with
KRAS Q61H; together these alter the MAPK pathway in roughly 43-64% of cases across published
cohorts (Takada et al., "Activating Mutations in PTPN11 and KRAS in Canine Histiocytic
Sarcomas," Genes 2019;10(7):505, PMID 31277422; "Canine Histiocytic and Hemophagocytic
Histiocytic Sarcomas Display KRAS and Extensive PTPN11/SHP2 Mutations and Respond In Vitro to
MEK Inhibition by Cobimetinib," Genes 2024;15(8):1050, PMID 39202410). Three canine HS cell
lines (BD, OD, DH82) with these mutations were shown to respond in vitro to the MEK1/2 inhibitor
cobimetinib at IC50 74-372 nM, well below the achievable canine plasma concentration
(Cmax ~1640 nM at 5 mg/kg; PMID 39202410). No canine-specific resistance data has been
published; this module is a hypothesis-generating exploration of plausible escape routes, not a
fitted or validated predictive model.

Human histiocytic sarcoma carries MAPK-pathway mutations spread across more genes (BRAF,
MAP2K1, KRAS, NRAS, PTPN11, NF1, CBL) in about 57% of cases (Shanmugam et al., "Identification
of diverse activating mutations of the RAS-MAPK pathway in histiocytic sarcoma," Mod Pathol.
2019;32(6):830-843), and a MAP2K1-mutant case achieved a complete clinical response to the MEK
inhibitor trametinib (Gounder et al., "Trametinib in Histiocytic Sarcoma with an Activating
MAP2K1 (MEK1) Mutation," N Engl J Med. 2018;378(20):1945-1947, PMID 29768143) -- a complete
response maintained for more than two years with no relapse reported, and independent case
reports of KRAS- and BRAF-mutant HS on MEK/BRAF inhibitors describe similarly long remissions (31
months; 3 years). No published human HS in vitro potency or PK numbers were found, so the human
preset reuses the same illustrative pharmacodynamic shape as the dog preset with a broader, less
concentrated resistance-mutation spectrum reflecting that documented genetic heterogeneity; its
potency/exposure values are not calibrated to a specific dataset.

Three synthetic escape mechanisms are modeled, chosen for general applicability to any MAPK
inhibitor rather than HS-specific evidence: (1) pathway reactivation via a secondary upstream
RAS/RAF alteration restoring ERK signaling around the drug; (2) RTK-mediated bypass, in which
loss of ERK-dependent negative feedback reactivates receptor tyrosine kinases and parallel
(e.g. PI3K/AKT) signaling; (3) on-target site mutation reducing inhibitor binding affinity, the
resistance category seen generally across kinase inhibitors. See MEK1/2 inhibitor resistance
reviews, e.g. PMID 26615130.

Acquired resistance is scheduled as a Poisson process over the sensitive clone's cumulative
cell-days of drug exposure (`poisson_mutation_injections`), not a constant daily transfer
fraction: with a fixed nonzero daily rate and any resistant clone growing net-positive under
drug, eventual outgrowth is mathematically guaranteed given enough follow-up time (a 100x rate
reduction only delayed median escape by degrees in testing), which cannot reproduce a genuinely
durable, multi-year response. A Poisson draw can come back exactly zero, so a resistant lineage
can truly never arise in a given trial. The overall rate is loosely tuned so the dog preset's
durable-response probability is in the same ballpark as the case reports above -- not a fit:
those are a handful of case reports published specifically because the outcome was durable
(survivorship/publication bias), so the true rate is almost certainly lower than "durable in all
of them."
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

    def __post_init__(self):
        k = len(np.asarray(self.growth))
        for name in ("ic50_nM", "max_kill"):
            if np.asarray(getattr(self, name)).shape != (k,):
                raise ValueError(f"{name} must contain one value per clone")
        mutation = np.asarray(self.mutation)
        if mutation.shape != (k, k) or np.any(mutation < 0):
            raise ValueError("mutation must be a nonnegative clone-by-clone matrix")
        if not np.allclose(mutation.sum(axis=1), 1):
            raise ValueError("mutation rows must sum to one")


def drug_kill_rate(concentration, ic50_nM: np.ndarray, hill: float, max_kill: np.ndarray) -> np.ndarray:
    """Emax pharmacodynamic model: per-day kill rate rising toward `max_kill` with concentration."""
    c = np.maximum(np.asarray(concentration, dtype=float), 0.0)
    ic50 = np.maximum(np.asarray(ic50_nM, dtype=float), 1e-9)
    return max_kill * c ** hill / (ic50 ** hill + c ** hill)


def simulate_resistance(model: ResistanceModel, concentration: np.ndarray, initial: np.ndarray,
                        injections: dict[int, np.ndarray] | None = None) -> np.ndarray:
    """Simulate density-dependent multiclone tumor burden under a daily drug-concentration series.

    Net growth is logistic growth minus an Emax drug kill-rate term, so a clone whose kill rate
    exceeds its growth rate actually regresses (not just plateaus) -- required for "response,
    then progression from nadir" dynamics, rather than the drug only ever capping growth at zero.
    `injections` optionally adds a population vector at specific days (see
    `poisson_mutation_injections`), on top of whatever `model.mutation` transfers that day.
    """
    initial = np.asarray(initial, float)
    state = np.zeros((len(concentration) + 1, len(initial)))
    state[0] = initial
    for t, c in enumerate(np.asarray(concentration, float)):
        current = state[t]
        density = current.sum() / model.carrying_capacity
        kill = drug_kill_rate(c, model.ic50_nM, model.hill, model.max_kill)
        net = model.growth * (1 - density) - kill
        grown = current * np.exp(np.clip(net, -30, 30))
        state[t + 1] = grown @ model.mutation
        if injections and (t + 1) in injections:
            state[t + 1] = state[t + 1] + injections[t + 1]
    return state


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
    return replace(model, ic50_nM=ic50, mutation=mutation)


def poisson_mutation_injections(rng: np.random.Generator, sensitive_trajectory: np.ndarray,
                                seeding_rates: np.ndarray, seed_fraction: float = 1e-8
                                ) -> dict[int, np.ndarray]:
    """Schedule acquired-resistance establishment as a Poisson process over sensitive cell-days.

    Expected establishment count for clone i is `seeding_rates[i] * sum(sensitive_trajectory)`.
    Unlike a constant per-day transfer fraction, a Poisson draw can come back exactly zero, so a
    resistant lineage can genuinely never arise in a given trial -- a rate small enough to make
    that likely is required to reproduce multi-year durable responses; a fixed nonzero daily
    seeding rate cannot, since it guarantees eventual outgrowth given enough follow-up time.
    """
    total_cell_days = float(sensitive_trajectory.sum())
    injections: dict[int, np.ndarray] = {}
    if total_cell_days <= 0:
        return injections
    weights = sensitive_trajectory / total_cell_days
    k = len(seeding_rates) + 1
    for clone_index, rate in enumerate(seeding_rates, start=1):
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


def _dominant_mechanism(state_final: np.ndarray, progressed: bool) -> str:
    if not progressed:
        return "durable_response"
    resistant = state_final[1:]
    if resistant.sum() <= 0:
        return "durable_response"
    return CLONE_NAMES[1 + int(np.argmax(resistant))]


def run_monte_carlo(reference: ResistanceModel, css_reference: float, horizon_days: int,
                   seeding_rates: np.ndarray, trials: int = 500, preexisting_prob: float = .3,
                   exposure_scale: float = .3, seeding_rate_scale: float = .5,
                   seed_fraction: float = 1e-8, detection_floor_fraction: float = .01,
                   seed: int = 7) -> MonteCarloOutcome:
    """Run a Monte Carlo ensemble over parameter, exposure, and acquired-mutation-timing uncertainty.

    Acquired resistance is scheduled with `poisson_mutation_injections` rather than a constant
    daily transfer out of `reference.mutation` (`reference` is simulated with mutation forced to
    identity), so a real fraction of trials can see no acquired resistance ever establish.

    Progression requires burden to both regrow >=20% from nadir (RECIST-style) and clear an
    absolute `detection_floor_fraction * carrying_capacity`: without a floor, a regrowth ratio
    computed against a numerically negligible nadir (e.g. 1e-9) can trip the 20% rule while the
    tumor is still clinically undetectable, which is not a real progression event.
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
        initial = sample_initial_state(rng, k, preexisting_prob, mechanism_weights=seeding_rates)
        sensitive_only = np.zeros(k)
        sensitive_only[0] = initial[0]
        sensitive_trajectory = simulate_resistance(model, concentration, sensitive_only)[:, 0]
        jittered_rates = seeding_rates * rng.lognormal(0, seeding_rate_scale, len(seeding_rates))
        injections = poisson_mutation_injections(rng, sensitive_trajectory, jittered_rates, seed_fraction)
        state = simulate_resistance(model, concentration, initial, injections)
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
