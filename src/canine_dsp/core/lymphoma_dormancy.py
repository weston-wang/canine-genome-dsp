"""The persister as a two-state pool, adapted from the HS branch's `core/dormancy.py`.

WHY THIS EXISTS

The lymphoma catalogue (`core/lymphoma_catalogue.py`) scored the drug-tolerant persister as an
ABSOLUTE WALL: `requires_division=False`, so every division-gated agent -- all of CHOP, rabacfosadine,
lomustine, radiation -- had a margin of exactly zero against it "by construction", and the persister
had to beat the full growth bar of 0.0903/day. That is the model the HS analysis later CORRECTED in
`core/dormancy.py` (a dormant cell is not growing either; persistence is a reversible state, so a
persister is a threat at RE-ENTRY and a continuously present agent is there when it happens). The
lymphoma work never picked that correction up. It matters: the persister is what makes the CNS
T-cell cell "not close" (short by 1.16x) and it is the basis of the "three filters" statement that no
conventional cytotoxic survives.

WHAT IS ADAPTED, AND WHAT IS NOT COPIED

The HS `DormancyModel.margin` is

    margin = sum(kill_from(a)) - growth * cycling_fraction,   kill_from(a) = effective_kill * duty

for a division-gated agent. Two problems, neither of which is copied here:

  1. `effective_kill` is already potency x access x duty, so multiplying by duty again counts duty
     twice.
  2. It credits a division-gated agent at full strength against the WHOLE pool, but such an agent can
     only kill the fraction of the pool that is awake. Treating the pool as two states (awake with
     probability f, dormant otherwise) and solving for its growth rate gives, when switching is fast
     relative to tumour growth,

         pool growth  =  f * g  -  k_nondivision_gated  -  f * (1 - r) * k_division_gated

     so a division-gated agent counts f times its kill, not 1 times. Checked against the exact
     eigenvalue of the 2x2 system in `tests/test_lymphoma_grounded.py`. With f = 0.2 and a
     division-gated kill of 0.05/day the HS-style margin is +0.032 ("closes") while the pool actually
     still grows at +0.008/day.

  3. (Found while testing this module.) With SLOW switching and no non-division-gated agent, the
     dormant reservoir is only drained as fast as cells wake, which is slower than either the
     fast-switching formula or an awake cell's net growth. So "closes" is not enough for a persister
     pool: the RATE of decline matters, and a division-gated-only regimen can "close" so slowly that
     the treatment clock (`core/lymphoma_horizon.py`) rules it out. The decision therefore uses the
     EXACT two-state growth rate, worst-cased over a swept switching rate.

THE TWO PARAMETERS, BOTH UNMEASURED FOR CANINE LYMPHOMA, SO SWEPT NOT ASSUMED

  f  the share of the persister pool awake (cycling) at any moment.
  r  the share of wake-ups that RETAIN tolerance (the cell wakes but is still not killed by
     division-gated agents). r = 0 is the HS assumption (a woken persister is an ordinary sensitive
     cell); r = 1 is the pessimistic one.

The OLD lymphoma "wall" model is exactly the corner f = 1, r = 1, so this module contains the old
answer as a special case rather than replacing it. A conclusion must hold across the sweep or it is
not a conclusion.

WHAT THIS DOES NOT CLAIM

It does not say persisters are harmless. Nothing about canine-lymphoma persisters is measured, so this
gives the SHAPE of the dependence (which regimens close under which (f, r)), not a prediction. And it
moves the burden onto DUTY and TIME: a division-gated agent only helps if it is present at re-entry,
i.e. dosed continuously for as long as persisters exist, which then has to survive the toxicity
ledger (`core/lymphoma_toxicity.py`) and the treatment clock (`core/lymphoma_horizon.py`).
"""

from __future__ import annotations

from dataclasses import dataclass

CYCLING_FRACTION_SWEEP = (0.05, 0.10, 0.20, 0.40, 1.00)
RETAINED_TOLERANCE_SWEEP = (0.0, 0.5, 1.0)
CYCLING_FRACTION_DEFAULT = 0.20
RETAINED_TOLERANCE_DEFAULT = 0.0


def _kills(agents, persister):
    """(k_non_division_gated, k_division_gated): effective kill of every agent that ACTS on the
    persister lineage, split by whether it can reach a dormant cell. `covers` is the derived
    coverage rule, so an agent only counts if the object model says it acts on this lesion."""
    k_nd = k_dg = 0.0
    for a in agents:
        if not a.covers(persister):
            continue
        if a.division_gated:
            k_dg += a.effective_kill
        else:
            k_nd += a.effective_kill
    return k_nd, k_dg


#: Switching rate between awake and dormant (per day), swept: 0.01 = a cell dwells ~100 days in a
#: state, 1.0 = ~1 day. Unmeasured for canine lymphoma.
SWITCH_RATE_SWEEP = (0.01, 0.1, 1.0)


def pool_growth_exact(agents, persister, growth: float, f: float, r: float, switch_rate: float) -> float:
    """Exact dominant growth rate of the two-state persister pool (negative = shrinks).

    Awake cells grow at `growth`, are killed by every non-division-gated agent and by the
    division-gated ones except for the tolerance-retaining share r; dormant cells are killed only by
    non-division-gated agents. Awake -> dormant at `switch_rate`, dormant -> awake at the rate that
    keeps the awake share at f. The 2x2 matrix has positive off-diagonals, so its eigenvalues are
    real and the dominant one is returned in closed form (no numpy needed)."""
    if not 0.0 < f <= 1.0:
        raise ValueError("f must be in (0, 1]")
    if not 0.0 <= r <= 1.0:
        raise ValueError("r must be in [0, 1]")
    k_nd, k_dg = _kills(agents, persister)
    k_awake = k_nd + (1.0 - r) * k_dg
    if f >= 1.0:
        return growth - k_awake
    b = switch_rate
    a = b * f / (1.0 - f)
    m11, m12, m21, m22 = growth - k_awake - b, a, b, -k_nd - a
    tr, det = m11 + m22, m11 * m22 - m12 * m21
    return tr / 2.0 + (tr * tr / 4.0 - det) ** 0.5


def pool_growth_fast(agents, persister, growth: float, f: float, r: float) -> float:
    """Closed form for FAST switching (relative to growth): f*g - k_nd - f*(1-r)*k_dg. Kept because it
    is the readable statement of why a division-gated agent counts f times its kill."""
    k_nd, k_dg = _kills(agents, persister)
    return f * growth - k_nd - f * (1.0 - r) * k_dg


def pool_growth_worst(agents, persister, growth: float, f: float, r: float) -> float:
    """Worst (largest) exact growth over the swept switching rates. A regimen that closes under this
    closes for every switching rate in the sweep."""
    return max(pool_growth_exact(agents, persister, growth, f, r, b) for b in SWITCH_RATE_SWEEP)


def persister_margin(agents, persister, growth: float, f: float = CYCLING_FRACTION_DEFAULT,
                     r: float = RETAINED_TOLERANCE_DEFAULT) -> float:
    """Margin against the persister pool, positive = closes. Replaces
    `Regimen.margin_against(persister, growth)` (the wall model) in the grounded search. The value is
    the pool's rate of DECLINE per day, so `ln(n0) / margin` is the days needed to clear n0 cells."""
    return -pool_growth_worst(agents, persister, growth, f, r)


def hs_style_margin(agents, persister, growth: float, f: float) -> float:
    """The HS `DormancyModel.margin` formula as written (division-gated kill at full strength, times
    duty a second time). Kept ONLY so the discrepancy can be shown; never used to decide closure."""
    total = 0.0
    for a in agents:
        if not a.covers(persister):
            continue
        total += a.effective_kill * a.duty if a.division_gated else a.effective_kill
    return total - growth * f


@dataclass(frozen=True)
class DormancySweep:
    """Margins over the (f, r) grid for one agent set, so 'holds across the sweep' is a computed
    statement."""

    agents: tuple
    persister: object
    growth: float

    def grid(self) -> dict:
        return {(f, r): persister_margin(self.agents, self.persister, self.growth, f, r)
                for f in CYCLING_FRACTION_SWEEP for r in RETAINED_TOLERANCE_SWEEP}

    def closes_everywhere(self) -> bool:
        return all(m > 0.0 for m in self.grid().values())

    def closes_at_hs_assumption(self) -> bool:
        """r = 0 (a woken persister is an ordinary sensitive cell), any f short of the degenerate
        f = 1 endpoint."""
        return all(persister_margin(self.agents, self.persister, self.growth, f, 0.0) > 0.0
                   for f in CYCLING_FRACTION_SWEEP if f < 1.0)

    def closes_under_old_wall_model(self) -> bool:
        return persister_margin(self.agents, self.persister, self.growth, 1.0, 1.0) > 0.0

    def threshold_cycling_fraction(self, r: float = 0.0) -> float:
        """Largest f at which the pool still shrinks (fast-switching closed form), for retained
        tolerance r. 1.0 means it closes even if the whole pool is awake; 0.0 means it never closes."""
        k_nd, k_dg = _kills(self.agents, self.persister)
        # f*g - k_nd - f*(1-r)*k_dg < 0  <=>  f * (g - (1-r)*k_dg) < k_nd
        denom = self.growth - (1.0 - r) * k_dg
        if denom <= 0.0:
            return 1.0
        return max(0.0, min(1.0, k_nd / denom))
