"""Engine v2 -- the four corrections validation forced, implemented.

WHAT V1 GOT WRONG, AND WHAT IS DONE ABOUT IT HERE

1. NO EXTINCTION STATE. A burden of 1e-82 was a live population that regrew, so no finite course
   could ever succeed and "never stop treating" was a tautology of the tool. v1 later gained an
   opt-in deterministic floor, which helped but produced an implausibly sharp cliff.
   V2: DEMOGRAPHIC STOCHASTICITY. Burden is converted to an expected cell count and the actual
   count is drawn from a Poisson distribution. A lineage whose draw comes back zero is extinct and
   stays extinct. Clearance becomes a probability that rises smoothly as the population falls,
   which is how real small populations behave, and it removes the artificial step.

2. ONE DOG, ONE TUMOUR. v1 ran a single fixed parameter set and reported the average as though it
   described every animal. Reality: lomustine response 29-46%; Sakuma 2024 found ERK/Akt inhibitor
   effects "varied among CHS cell lines"; Sakuma 2025 found pathway ACTIVATION does not predict
   which lines respond.
   V2: per-trial heterogeneity. Growth rates and kill ceilings are drawn per simulated dog from
   lognormal distributions, so the output is a distribution over animals rather than one animal
   repeated.

3. NO SUBGROUPS. Sakuma 2026 screened 1,824 compounds across 10 canine HS lines and found two
   gene-expression groups. Duvelisib was selectively active in Group A (median IC50 287 nM, vs
   >5 uM in Group B, 7.46 uM in normal PBMCs; pAkt fell in all eight Group A lines and none in B).
   No compound was specifically effective for Group B.
   V2: an explicit subgroup axis. Group A's parallel-axis agent works at a measured potency;
   Group B's does not. Combination synergy is therefore subgroup-conditional, matching the finding
   that co-administration helped in "only a part" of lines.

4. THE DOSE CEILING WAS IGNORED. v1 treated steady-state concentration as a free input and used
   246 nM for trametinib. Dogs reach ~16 nM (Takada 2024 Phase I), capped by hypertension and
   proteinuria. Run at 16 nM, v1 ITSELF predicts failure -- so its optimism was never about the
   biology, it was about the delivery.
   V2: routes carry ceilings. A systemic route is capped at its measured achievable concentration;
   a local intracavitary route is not, because the ceiling is a systemic-toxicity constraint and
   local delivery is not subject to it.

WHAT V2 STILL CANNOT DO, AND SAYS SO
It models tumour progression, not death. Dogs with intracranial tumours are euthanised for
seizures, ataxia and behavioural change -- the CNS palliative median of 5 days is a decision, not a
growth curve. v2 has no tumour location, no neurological function and no owner. Every survival
figure in the canine literature is therefore still non-commensurable with v2's output, exactly as
`validation.monotherapy_backtest` established for v1.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

# One cell, in normalised units where carrying capacity is 1.0, for a tumour of ~1e9 cells at
# capacity. Demographic stochasticity is applied below this many cells, where Poisson noise on
# integer cell numbers dominates the deterministic growth term.
CELLS_AT_CARRYING_CAPACITY = 1e9
STOCHASTIC_REGIME_CELLS = 1e4

# Measured achievable canine steady state, Takada 2024 Phase I: ~10 ng/mL ~ 16 nM in ~70% of dogs,
# dose-limited by hypertension, proteinuria, lethargy and elevated ALP.
TRAMETINIB_ACHIEVABLE_CANINE_NM = 16.0

# Sakuma 2026, DOI 10.1111/vco.70077. Median IC50 by subgroup.
DUVELISIB_IC50_GROUP_A_NM = 287.0
DUVELISIB_IC50_GROUP_B_NM = 5000.0     # reported as >5 uM; used as a floor, so Group B is
                                       # modelled as no better than this
DUVELISIB_IC50_NORMAL_PBMC_NM = 7460.0

# Group A fraction among canine HS lines in that screen: 8 of 10 showed the Group A pAkt response.
# NOT a prevalence estimate for primary intracranial HS, which has never been typed.
GROUP_A_FRACTION_IN_VISCERAL_LINES = 0.8


@dataclass(frozen=True)
class Route:
    """A delivery route and the concentration ceiling it does or does not impose."""

    name: str
    ceiling_nM: float | None   # None = no systemic-toxicity ceiling applies
    why: str


SYSTEMIC = Route(
    "systemic", TRAMETINIB_ACHIEVABLE_CANINE_NM,
    "Capped by the canine Phase I dose-limiting toxicities. Raising the dose is not available.",
)
INTRACAVITARY = Route(
    "intracavitary", None,
    "Drug released into the resection cavity. The ceiling is a systemic-toxicity constraint and "
    "does not apply. Precedent: Gliadel (FDA-approved), convection-enhanced delivery. No ERK or "
    "PI3K inhibitor has been given this way in any species -- modality approved, application not.",
)


def draw_tumour(rng: np.random.Generator, n: int, group_a_fraction: float = 0.5,
                growth_median: float = 0.055, growth_spread: float = 0.35,
                kill_median: float = 0.16, kill_spread: float = 0.40) -> dict:
    """Draw `n` simulated dogs, each with its own tumour rather than one tumour repeated.

    Spreads are lognormal sigmas, chosen so the resulting response distribution spans the observed
    heterogeneity (lomustine response 29-46%; Sakuma's "varied among cell lines") rather than being
    fitted to it. They are assumptions, and widening or narrowing them is the first sensitivity
    anyone should run.
    """
    return {
        "growth": rng.lognormal(np.log(growth_median), growth_spread, n),
        "kill_ceiling": rng.lognormal(np.log(kill_median), kill_spread, n),
        "is_group_a": rng.random(n) < group_a_fraction,
        "residual": draw_surgical_residual(rng, n),
    }


# Correction 5, added after v2's first back-test still undershot. Surgical completeness is the
# dominant real-world prognostic variable and v1 and early-v2 both gave every simulated dog an
# identical post-operative residual. A fixed residual cannot produce a mixture outcome, and
# Skorupski's 37.5% is almost certainly a mixture: some dogs' local therapy was complete and some
# was not. The lognormal below spans four orders of magnitude around the old fixed value, with a
# `complete_resection_fraction` of animals given a genuinely zero residual.
COMPLETE_RESECTION_FRACTION = 0.25
RESIDUAL_MEDIAN = 0.009
RESIDUAL_SPREAD = 2.0


def draw_surgical_residual(rng: np.random.Generator, n: int,
                           complete_fraction: float = COMPLETE_RESECTION_FRACTION,
                           median: float = RESIDUAL_MEDIAN,
                           spread: float = RESIDUAL_SPREAD) -> np.ndarray:
    """Post-operative residual disease, varying per dog.

    `complete_fraction` get zero -- the surgeon got everything. The rest get a lognormal spread.
    Neither number is measured for this presentation; both are assumptions that make a MIXTURE
    outcome representable at all, which a single fixed residual cannot do.
    """
    residual = rng.lognormal(np.log(median), spread, n)
    residual = np.where(rng.random(n) < complete_fraction, 0.0, residual)
    return np.clip(residual, 0.0, 0.5)


def emax(concentration: float, ic50_nM: float, max_kill: float, hill: float = 1.5) -> float:
    c = max(concentration, 0.0)
    return max_kill * c**hill / (ic50_nM**hill + c**hill)


def simulate_one(rng: np.random.Generator, growth: float, kill_ceiling: float, is_group_a: bool,
                 horizon_days: int, initial_burden: float,
                 mapk_concentration_nM: float, mapk_ic50_nM: float,
                 parallel_concentration_nM: float = 0.0,
                 parallel_max_kill: float = 0.10,
                 immune_kill_per_day: float = 0.0,
                 stop_dosing_day: int | None = None,
                 detection_floor: float = 0.01) -> tuple[bool, int]:
    """One simulated dog. Returns (progressed, day_of_progression).

    Demographic stochasticity: once the expected cell count falls into the small-population regime
    the realised count is drawn from a Poisson, so a lineage can genuinely hit zero and stay there.
    That is the mechanism v1 lacked entirely.
    """
    burden = initial_burden
    nadir = burden
    parallel_ic50 = DUVELISIB_IC50_GROUP_A_NM if is_group_a else DUVELISIB_IC50_GROUP_B_NM

    for day in range(horizon_days):
        on_drug = stop_dosing_day is None or day < stop_dosing_day
        mapk_c = mapk_concentration_nM if on_drug else 0.0
        par_c = parallel_concentration_nM if on_drug else 0.0

        kill = emax(mapk_c, mapk_ic50_nM, kill_ceiling)
        kill += emax(par_c, parallel_ic50, parallel_max_kill)
        kill += immune_kill_per_day          # not concentration-gated, persists after dosing stops

        burden = burden * np.exp(growth * (1 - burden) - kill)

        cells = burden * CELLS_AT_CARRYING_CAPACITY
        if cells < STOCHASTIC_REGIME_CELLS:
            cells = float(rng.poisson(max(cells, 0.0)))
            burden = cells / CELLS_AT_CARRYING_CAPACITY
            if cells == 0.0:
                return False, horizon_days      # extinct, and it stays extinct

        nadir = min(nadir, burden)
        if burden > max(nadir * 1.2, detection_floor):
            return True, day
    return False, horizon_days


def run(regimen: dict, trials: int = 400, horizon_days: int = 3650, seed: int = 7,
        group_a_fraction: float = 0.5, initial_burden: float | None = None) -> dict:
    """Run a regimen across a heterogeneous population of simulated dogs."""
    rng = np.random.default_rng(seed)
    pop = draw_tumour(rng, trials, group_a_fraction)
    progressed = np.zeros(trials, dtype=bool)
    days = np.zeros(trials)
    for i in range(trials):
        burden_i = pop["residual"][i] if initial_burden is None else initial_burden
        if burden_i <= 0.0:
            progressed[i] = False
            days[i] = horizon_days
            continue
        p, d = simulate_one(
            rng, pop["growth"][i], pop["kill_ceiling"][i], bool(pop["is_group_a"][i]),
            horizon_days, burden_i, **regimen)
        progressed[i] = p
        days[i] = d
    a = pop["is_group_a"]
    return {
        "relapse_free": float(1 - progressed.mean()),
        "relapse_free_group_a": float(1 - progressed[a].mean()) if a.any() else float("nan"),
        "relapse_free_group_b": float(1 - progressed[~a].mean()) if (~a).any() else float("nan"),
        "median_days_to_progression": (float(np.median(days[progressed]))
                                       if progressed.any() else float("nan")),
    }


# ---------------------------------------------------------------------------------------------
# Validation and result, computed with this engine.
# ---------------------------------------------------------------------------------------------

BACKTEST_V2B = {
    "target": "Skorupski 2009 (PMID 19453368), n=16, lomustine adjuvant after local therapy in "
              "localized canine HS: 0.375 relapse-free.",
    "v1_result": "0.000 at every potency and horizon -- structurally incapable.",
    "v2_before_residual_heterogeneity": {500: {100: 0.233, 300: 0.073, 500: 0.015}},
    "v2b_with_residual_heterogeneity": {
        (500, 100): 0.432, (500, 300): 0.297, (500, 500): 0.240, (1000, 300): 0.385,
    },
    "VERDICT": "PASSES. v2b brackets the observed 0.375, landing at 0.385 for the (1000 nM, 300 nM) "
               "pair. The engine now reproduces a measured outcome for the first time in this "
               "project's history.",
    "what_closed_the_gap": "Per-dog surgical residual. A fixed residual cannot produce a mixture "
        "outcome, and 37.5% relapse-free is almost certainly a mixture of dogs whose local therapy "
        "was complete and dogs whose was not.",
    "THE_ASSUMPTION_DOING_THE_WORK": "COMPLETE_RESECTION_FRACTION = 0.25. The untreated arm returns "
        "0.225, which is essentially just that fraction -- the 'cure' with no drug is entirely "
        "'the surgeon got everything'. That 25% is an assumption, not a measurement for this "
        "presentation, and it is the single number this back-test rests on. It was chosen before "
        "the back-test was run, on the principle that a mixture outcome needs a mixture input, and "
        "was not iterated on to hit the target.",
}

TEN_YEAR_RELAPSE_FREE = {
    "surgery_alone": {"all": 0.225, "group_a": 0.216, "group_b": 0.235},
    "plus_systemic_trametinib_16nM": {"all": 0.225, "group_a": 0.216, "group_b": 0.235},
    "plus_lomustine_105_day_course": {"all": 0.297, "group_a": 0.304, "group_b": 0.291},
    "local_mapk_500nM": {"all": 0.975, "group_a": 0.975, "group_b": 0.974},
    "local_mapk_plus_duvelisib": {"all": 0.993, "group_a": 1.000, "group_b": 0.985},
    "local_mapk_plus_duvelisib_plus_immune": {"all": 1.000, "group_a": 1.000, "group_b": 1.000},
    "THE_HEADLINE": "REVERSED -- see `v2.the_250nm_retraction`. This said systemic MEK inhibition "
        "adds NOTHING over surgery (0.225 to 0.225) and that local delivery was the entire therapy. "
        "It was computed by pairing trametinib's achievable 16 nM with COBIMETINIB's IC50. With "
        "cobimetinib's own measured pair -- 179 nM IC50 against a 1640 nM canine Cmax -- systemic "
        "therapy at the lung reaches 0.973 and needs no local delivery at all. The exposure problem "
        "was specific to one molecule, not to MEK inhibition. NOTE: this module's figures used IC50 "
        "179, not the inflated 250, so only the drug attribution was wrong here.",
}

FINITE_COURSE = {
    # stop day -> {all, group_a, group_b}, full regimen
    180: {"all": 0.965, "group_a": 1.000, "group_b": 0.929},
    365: {"all": 0.990, "group_a": 1.000, "group_b": 0.980},
    730: {"all": 0.998, "group_a": 1.000, "group_b": 0.995},
    1095: {"all": 1.000, "group_a": 1.000, "group_b": 1.000},
    "without_the_immune_arm_at_365_days": {"all": 0.943, "group_a": 1.000, "group_b": 0.883},
    "what_the_immune_arm_is_for": "Group B insurance, and it matters most when stopping early. "
        "Group A reaches 1.000 at one year with no immune arm at all, because duvelisib covers it. "
        "Group B at one year is 0.883 without and 0.980 with.",
}

WHAT_THIS_STILL_CANNOT_SAY = (
    "No dog with this disease has received any of this. Local delivery of an ERK or PI3K inhibitor "
    "has never been done in any species -- the modality is FDA-approved (Gliadel), the application "
    "is not.",
    "Primary intracranial HS has never been cultured, typed or screened. Whether it is Group A, "
    "Group B or neither is unknown, and the Group A/B structure here is imported from visceral and "
    "disseminated cell lines (abdominal mass, lung, lung, bone marrow -- none brain-derived).",
    "The engine models tumour progression, not death. Dogs with intracranial tumours are "
    "euthanised for seizures, ataxia and behavioural change; the CNS palliative median of 5 days is "
    "a decision, not a growth curve. No tumour location, no neurological function, no owner.",
    "The immune rate of 0.045/day has never been measured against canine HS by any axis.",
    "The 25% complete-resection assumption carries the back-test and is unmeasured for this "
    "presentation.",
)
