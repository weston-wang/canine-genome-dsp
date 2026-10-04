"""Closing the dormant-progenitor escape (E5) with agents that exist today, by SUSTAINING them.

Background (docs/LYMPHOMA_UNIVERSE.md section H). The model's `sustainable_days` for each agent is the longest exposure documented
in dogs or humans (oral cytarabine ocfosfate 84 d, verdinexor 56 d, ...). E5 is a dormant, pump-armoured progenitor that wakes slowly and
is killed only once awake, so it is cleared by a pump-independent agent that is simply PRESENT for long enough, not by a stronger one.
The earlier statement (section F) that "longer dosing does not close the brain" was tested only to 730 days; the clock needs about
1,470 days for B-cell brain at the worst swept switching rate (383 days if cells switch state at 0.1/day or faster). This module
re-runs the clock with chosen agents' windows extended, so the dependence on duration is explicit and tested instead of buried in a default.

Nothing here changes a default: `with_windows` overrides toxicity-profile windows inside a context manager and restores them.
Whether those durations are tolerable is a separate, evidenced question (docs/universe/SWEEP_sustain.md); a program using this module
must be reported with the durations it needs.
"""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import replace

from . import lymphoma_joint as J
from .core import lymphoma_grounded as G
from .core.lymphoma_catalogue import CNS, SYSTEMIC
from .core.lymphoma_toxicity import PROFILES

OCFOSFATE = "cytarabine ocfosfate, oral continuous"
VERDINEXOR = "verdinexor"
THIOTEPA = "high-dose thiotepa-based consolidation with autologous stem-cell rescue [human regimen]"


@contextmanager
def with_windows(days_by_profile: dict):
    """Temporarily set `sustainable_days` (and the hard cap, where one exists) for the named toxicity profiles."""
    saved = {n: PROFILES[n] for n in days_by_profile}
    try:
        for n, d in days_by_profile.items():
            p = PROFILES[n]
            PROFILES[n] = replace(p, sustainable_days=float(d), hard_cap_days=(float(d) if p.hard_cap_days else None))
        yield
    finally:
        PROFILES.update(saved)


def clock(ip: str, prefixes, comp: str, *, kill: float = J.CENTRAL["kill"], duty: float = J.CENTRAL["duty"]):
    """Strict clock verdict (cleared?, text) for a program in one compartment."""
    pools = J._pools(ip, kill, duty)
    esc = J._escapes(ip)
    reg = [pools[comp][J._resolve(p, pools)] for p in prefixes]
    ev = G.evaluate_best_schedule(reg, esc, compartment=comp)
    return ev.horizon_strict.cure_inside_window, ev.horizon_strict.verdict()


def minimal_window(ip: str, prefixes, comp: str, profile: str, *, lo: int = 100, hi: int = 9000, step: int = 30) -> int | None:
    """Smallest window (days, to `step`) for one agent's profile at which the program clears every escape in `comp`; None if even `hi` fails."""
    def ok(d):
        with with_windows({profile: d}):
            return clock(ip, prefixes, comp)[0]
    if not ok(hi):
        return None
    while hi - lo > step:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid
    return hi


#: Existing-agent programs (docs/LYMPHOMA_UNIVERSE.md section F); the sustained variants only extend the named agent's window.
EXISTING = J.EXISTING_PROGRAMS
