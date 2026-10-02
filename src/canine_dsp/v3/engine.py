"""Engine v3 -- the first engine in this project that can represent durability.

WHY V3 EXISTS

`v2.the_horizon_does_nothing` established that v2's ten-year figures are day-0 dose-adequacy
calculations: a 100-year horizon returns the same answer as a 1-year horizon, because a single
population with an additive kill term has nothing that accumulates. v1 HAD clone structure and lost
it when v2 was built to gain an extinction state. v3 restores it and adds the four things the audits
showed were missing.

WHAT V3 HAS THAT NEITHER PREDECESSOR DID

1. CLONES WITH SEEDING (from v1). A clone vector, per-clone susceptibility to each agent, and
   Poisson seeding of resistant clones over cumulative cell-days of drug exposure. This is what makes
   the horizon matter: more time on drug means more chances to seed an escape.

2. AN EXPLICIT ANTIGEN/MHC STATE (new). Each clone carries `antigen_present` and `mhc_intact`
   independently, because `v2.the_mhc_contradiction` showed the project had conflated them. A T-cell
   arm needs BOTH. Missing-self NK needs mhc_intact == False. A lineage-directed agent needs NEITHER.
   That is the distinction the whole immune argument turns on and no previous engine could express.

3. COMPARTMENT-AWARE PENETRATION ON EVERY AGENT (new). `v2.the_parallel_agent_defect` found that
   only the first drug was ever barrier-scaled. Here penetration is a property of the (agent,
   compartment) pair and is applied inside the engine, so no call site can forget it.

4. DOSING SCHEDULES WITH WASHOUT (new). Cobimetinib's MTD schedule is 21 days on, 7 off. v2 modelled
   3,650 consecutive days of exposure. An agent that is off has zero concentration, and clones grow.

WHAT V3 STILL CANNOT DO, STATED UP FRONT
It has no PK compartment -- concentrations are steady-state within an on-period, not curves. It has
no explicit persister compartment; quiescence is approximated by a per-clone kill ceiling rather than
a separate non-dividing pool. It models tumour progression, not death, so no canine survival figure
is commensurable with its output. And every rate in it is either measured elsewhere, swept, or
assumed -- building a better engine does not create data.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

CELLS_AT_CARRYING_CAPACITY = 1e9
STOCHASTIC_REGIME_CELLS = 1e4


@dataclass(frozen=True)
class Clone:
    """One tumour subpopulation. The state that decides which mechanisms can touch it."""

    name: str
    growth: float
    mapk_driver: bool          # does a MEK inhibitor have a target here
    antigen_present: bool      # can a vaccine/T-cell arm see it
    mhc_intact: bool           # True blocks missing-self NK; False enables it
    resistance_factor: float = 1.0   # multiplies IC50 of the agent(s) it escapes
    seeded_from: str | None = None


@dataclass(frozen=True)
class Agent:
    """A therapy. Penetration is per-compartment and applied inside the engine."""

    name: str
    concentration_nM: float
    ic50_nM: float
    max_kill: float
    penetration: dict          # compartment -> fraction of systemic concentration reaching it
    hill: float = 1.5
    requires_mapk_driver: bool = False
    requires_antigen: bool = False
    requires_mhc_loss: bool = False
    lineage_directed: bool = False     # acts regardless of driver, antigen or MHC state
    access_scales_kill: bool = False   # for cell- and antibody-based agents, and for any agent
                                       # specified by an effect size rather than a concentration:
                                       # compartment access multiplies the KILL RATE directly.
                                       # Without this, specifying an agent as a large concentration
                                       # against a tiny IC50 saturates Emax and makes penetration
                                       # silently inert -- which it did, until this was found.
    days_on: int = 0                   # 0 = continuous
    days_off: int = 0
    stop_day: int | None = None

    def active_on(self, day: int) -> bool:
        if self.stop_day is not None and day >= self.stop_day:
            return False
        if self.days_on <= 0:
            return True
        return (day % (self.days_on + self.days_off)) < self.days_on

    def kill_against(self, clone: Clone, compartment: str) -> float:
        """Per-day kill rate this agent achieves against this clone in this compartment."""
        if self.requires_mapk_driver and not clone.mapk_driver:
            return 0.0
        if self.requires_antigen and not (clone.antigen_present and clone.mhc_intact):
            return 0.0
        if self.requires_mhc_loss and clone.mhc_intact:
            return 0.0
        access = self.penetration.get(compartment, 0.0)
        if access <= 0.0:
            return 0.0
        if self.access_scales_kill:
            return self.max_kill * access
        c = self.concentration_nM * access
        ic50 = self.ic50_nM * (clone.resistance_factor if not self.lineage_directed else 1.0)
        return self.max_kill * c ** self.hill / (ic50 ** self.hill + c ** self.hill)


@dataclass
class Regimen:
    name: str
    agents: list = field(default_factory=list)


def simulate_one(rng, clones, regimen, compartment, horizon_days, initial_burden,
                 seeding_rate_per_cell_day, detection_floor=0.01):
    """One dog. Returns (progressed, day). Escape is seeded over cumulative cell-days on drug."""
    k = len(clones)
    pop = np.zeros(k)
    pop[0] = initial_burden
    nadir = initial_burden
    growth = np.array([c.growth for c in clones])
    seedable = [i for i, c in enumerate(clones) if c.seeded_from is not None]
    parent_of = {i: next(j for j, c2 in enumerate(clones) if c2.name == clones[i].seeded_from)
                 for i in seedable}

    for day in range(horizon_days):
        active = [a for a in regimen.agents if a.active_on(day)]
        kill = np.zeros(k)
        for i, clone in enumerate(clones):
            kill[i] = sum(a.kill_against(clone, compartment) for a in active)

        total = pop.sum()
        pop = pop * np.exp(growth * (1.0 - total) - kill)

        # Seeding: a resistant clone appears from its parent in proportion to parent cell-days
        # under drug. No drug pressure, no selection pressure, no seeding.
        if any(a.concentration_nM > 0 for a in active):
            for i in seedable:
                p = parent_of[i]
                expected = pop[p] * CELLS_AT_CARRYING_CAPACITY * seeding_rate_per_cell_day
                if expected > 0 and pop[i] == 0.0 and rng.random() < min(expected, 1.0):
                    pop[i] = 1.0 / CELLS_AT_CARRYING_CAPACITY

        cells = pop * CELLS_AT_CARRYING_CAPACITY
        small = cells < STOCHASTIC_REGIME_CELLS
        if small.any():
            cells[small] = rng.poisson(np.maximum(cells[small], 0.0))
            pop = cells / CELLS_AT_CARRYING_CAPACITY
        if pop.sum() == 0.0:
            return False, horizon_days

        burden = pop.sum()
        nadir = min(nadir, burden)
        if burden > max(nadir * 1.2, detection_floor):
            return True, day
    return False, horizon_days


def run(clones, regimen, compartment, trials=400, horizon_days=3650, seed=7,
        residual_median=0.009, residual_spread=2.0, complete_resection_fraction=0.25,
        seeding_rate_per_cell_day=1e-9, growth_spread=0.35):
    """A heterogeneous population of simulated dogs. Returns relapse-free fraction and timing."""
    rng = np.random.default_rng(seed)
    residual = rng.lognormal(np.log(residual_median), residual_spread, trials)
    residual = np.where(rng.random(trials) < complete_resection_fraction, 0.0, residual)
    residual = np.clip(residual, 0.0, 0.5)
    progressed = np.zeros(trials, dtype=bool)
    days = np.full(trials, float(horizon_days))

    for t in range(trials):
        if residual[t] <= 0.0:
            continue
        jitter = rng.lognormal(0.0, growth_spread)
        dogs_clones = [Clone(c.name, c.growth * jitter, c.mapk_driver, c.antigen_present,
                             c.mhc_intact, c.resistance_factor, c.seeded_from) for c in clones]
        p, d = simulate_one(rng, dogs_clones, regimen, compartment, horizon_days,
                            residual[t], seeding_rate_per_cell_day)
        progressed[t] = p
        days[t] = d

    return {
        "relapse_free": float(1 - progressed.mean()),
        "median_days_to_progression": (float(np.median(days[progressed]))
                                       if progressed.any() else float("nan")),
    }
