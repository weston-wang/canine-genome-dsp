"""The treatment clock for lymphoma, adapted from the HS branch's `core/response_duration.py` and
`core/treatment_horizon.py`.

THE QUESTION THIS ANSWERS

A regimen whose kill beats growth against every escape looks curative. But "beats growth" is a RATE,
and "10+ years durable" is a DURATION. The HS branch found that a fixed positive margin has exactly
two outcomes in a rate model -- cure or death -- so ">10 years" is "true by default", which is "a
restatement of the sign of a subtraction". What was missing was the treatment clock: can each agent
that carries the margin be GIVEN for as long as clearing takes?

    days to clear n0 cells at net rate m   ~   (ln n0 + 0.577) / m       (deterministic mean-field)

If an agent that carries an escape's margin has to stop before that escape is cleared (a cumulative
toxicity, a schedule cap, a CAR-T that is gone in three weeks), the margin drops when it stops. If it
drops to zero or below the escape regrows: RESPONSE THEN RELAPSE, which is the outcome real dogs have
and the rate model could not produce.

WHAT IT REPORTS, PER ESCAPE

  cleared at day D                   the lineage is gone inside the window
  relapses after an agent stops      margin goes <= 0 at day D before the lineage is cleared
  controlled, needs agents X to D    only the agents with no identified cap remain; clearing needs them
                                     for D days -- CONTROL, not cure, until D has passed

INPUTS AND THEIR STRENGTH

`sustain` maps agent name -> days (None = uncapped) and is built from `core/lymphoma_toxicity.py`;
`margin_fn(active_agents, escape)` lets the grounded search inject its own margin rule (efflux
reversal, dormancy) so the clock and the search cannot disagree, and `kill_of(agent)` the per-agent
kill used for the drug-sensitive bulk.

COURSE AGENTS. The catalogue's `duty` for a one-time course (radiation 21/365, TBI 14/365) is that
course averaged over a YEAR. Inside its course the agent acts at full strength and then stops, so a
time-resolved clock must use potency x access inside the window, not the annual average. Averaging is
what makes a one-time consolidation look as if it adds no durability; the clock does not average. `sustainable_days` per agent comes from `core/lymphoma_toxicity.py` (a canine measurement where
`measured_in_dogs`, else flagged). The starting count of each escape lineage is rate x burden, the
expected number of cells carrying the lesion, from the catalogue's seeding rates -- an ASSUMED rate
(only the existence of each lesion is measured). The mean-field treatment does not represent
stochastic extinction of a handful of cells; it is a schedule check, not a survival estimate.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from .lymphoma_dormancy import (CYCLING_FRACTION_DEFAULT, RETAINED_TOLERANCE_DEFAULT,
                                persister_margin)

EULER_GAMMA = 0.5772156649
#: Growth of the drug-sensitive bulk clone (lymphoma_scenarios._SHARED_GROWTH[0]).
BULK_GROWTH_PER_DAY = 0.100
DAYS_PER_YEAR = 365.0


def days_to_clear(n0: float, margin: float) -> float:
    """Days for `n0` cells to reach extinction at net decline `margin`/day; inf if margin <= 0."""
    if margin <= 0.0:
        return math.inf
    if n0 <= 0.0:
        return 0.0
    return (math.log(max(n0, 1.0)) + EULER_GAMMA) / margin


@dataclass
class EscapeOutcome:
    name: str
    n0: float
    outcome: str                   # "cleared" | "relapses" | "never_cleared"
    day: float                     # day cleared / day the margin was lost
    margin_at_start: float
    carried_by: tuple = ()         # agents whose withdrawal ended the margin (for "relapses")
    note: str = ""


@dataclass
class HorizonResult:
    burden: float
    outcomes: list = field(default_factory=list)

    @property
    def cure_inside_window(self) -> bool:
        return all(o.outcome == "cleared" for o in self.outcomes)

    @property
    def relapsing(self) -> list:
        return [o for o in self.outcomes if o.outcome == "relapses"]

    @property
    def clear_day(self) -> float:
        """Day the LAST lineage is cleared (inf if any is not)."""
        return max((o.day for o in self.outcomes if o.outcome == "cleared"), default=0.0) \
            if self.cure_inside_window else math.inf

    def verdict(self) -> str:
        if self.cure_inside_window:
            return f"cleared inside the window (last lineage gone by day {self.clear_day:.0f})"
        bad = self.relapsing
        if bad:
            worst = min(bad, key=lambda o: o.day)
            return (f"RESPONSE THEN RELAPSE: {worst.name} regrows after day {worst.day:.0f} "
                    f"({', '.join(worst.carried_by) or 'agents stop'})")
        return "not cleared: margin never positive for some lineage"


def _active(agents, sustain, t):
    """Agents still deliverable at day t. `sustain` maps agent name -> days (None = uncapped)."""
    out = []
    for a in agents:
        cap = sustain.get(a.name)
        if cap is None or t < cap:
            out.append(a)
    return out


def _margin(active, escape, growth, f, r):
    if not escape.requires_division:
        return persister_margin(active, escape, growth, f, r)
    return sum(a.effective_kill for a in active if a.reaches(escape)) - growth


def horizon(agents, escapes, sustain: dict, burden: float, growth: float, *,
            f: float = CYCLING_FRACTION_DEFAULT, r: float = RETAINED_TOLERANCE_DEFAULT,
            presence_threshold: float = 0.5, margin_fn=None, always_present=(),
            kill_of=None, fraction: float = 1.0) -> HorizonResult:
    """Walk the schedule: at each day some agents drop out, the margin of every lineage is
    recomputed, and each lineage is either cleared, relapses, or is never cleared.

    Lineages are the escapes likely PRESENT at this burden (P(present) >= threshold, as in the
    catalogue's early-detection premise) plus the drug-sensitive bulk."""
    from .regimen import escape_presence_probability
    # `fraction` scales COUNTS for a compartment that holds only part of the tumour (the CNS). Which
    # lineages are present is still decided at the whole-tumour burden, because a sanctuary seeded from
    # the tumour can carry any lineage the tumour has; each present lineage keeps at least one cell.
    lineages = [("drug-sensitive bulk", burden * fraction, None)]
    for e in escapes:
        if e.name in always_present or escape_presence_probability(e, burden) >= presence_threshold:
            lineages.append((e.name, max(e.seeding_rate * burden * fraction, 1.0), e))

    cutoffs = sorted({c for a in agents for c in [sustain.get(a.name)] if c is not None})
    boundaries = [0.0] + cutoffs + [math.inf]
    result = HorizonResult(burden)

    for name, n0, esc in lineages:
        ln_left = math.log(max(n0, 1.0)) + EULER_GAMMA     # log-cells still to remove
        first_margin = None
        outcome = None
        for i in range(len(boundaries) - 1):
            t0, t1 = boundaries[i], boundaries[i + 1]
            act = _active(agents, sustain, t0)
            if esc is None:
                kill = kill_of if kill_of is not None else (lambda a: a.effective_kill)
                m = sum(kill(a) for a in act) - BULK_GROWTH_PER_DAY
            elif margin_fn is not None:
                m = margin_fn(act, esc)
            else:
                m = _margin(act, esc, growth, f, r)
            if first_margin is None:
                first_margin = m
            if m <= 0.0:
                dropped = tuple(a.name for a in agents if a not in act)
                outcome = EscapeOutcome(name, n0, "relapses" if t0 > 0 else "never_cleared", t0,
                                        first_margin, dropped)
                break
            need = ln_left / m
            if t0 + need <= t1:
                outcome = EscapeOutcome(name, n0, "cleared", t0 + need, first_margin)
                break
            ln_left -= m * (t1 - t0)
        if outcome is None:                                # loop ended without a verdict
            outcome = EscapeOutcome(name, n0, "never_cleared", math.inf, first_margin)
        result.outcomes.append(outcome)
    return result
