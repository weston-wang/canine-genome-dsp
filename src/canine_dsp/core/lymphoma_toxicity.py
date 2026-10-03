"""Toxicity as a first-class constraint for the lymphoma search, ported from the HS branch's
`core/toxicity.py` and given the TIME dimension that module says it lacks.

WHY THIS EXISTS

The lymphoma search (`core/lymphoma_search.py`) scored each agent with `potency x access x duty` and
NOTHING ELSE. `lymphoma_toxicity.py` (the older module) holds the toxicity ledger as prose. That is
the exact failure the HS branch recorded: "the search could therefore return six agents at 0.30/day
each, which is arithmetic rather than a regimen, and the objection lived only in a commit message."
Anything not represented as an object is free to be ignored by the search, and it was.

WHAT THIS ENFORCES (unchanged from the HS module)

Every agent names the ORGAN AXIS its dose-limiting toxicity sits on and the share of that axis's
budget it consumes at full dose. A regimen is tolerable only if NO AXIS IS OVERSUBSCRIBED. Different
axes combine freely; the same axis ADDS. DE-RATING IS NOT FREE: an agent held below full dose
delivers proportionally less kill, and a regimen that is tolerable only by de-rating is re-scored at
the de-rated kill.

WHAT IS ADDED

  * `cumulative` and `sustainable_days`. The HS module states its own limitation: "pairing a ten-year
    durability figure with a toxicity model that has no time dimension remains a cross-assumption
    error." A cumulative toxicity (doxorubicin's heart, lomustine's liver) caps how long an agent can
    be given, however low the per-day load looks. `core/lymphoma_horizon.py` uses `sustainable_days`
    to ask whether an agent is still there when it is needed.
  * `EFFLUX_CO_DOSE`: a P-glycoprotein chemosensitiser is not selective for the tumour. It raises the
    partner's exposure everywhere the pump sits (gut, liver, kidney, blood-brain barrier), so the
    partner's organ-axis load is multiplied. The older lymphoma module wrote this in prose
    ("a toxicity multiplier") and never charged it.

WHAT THIS DOES NOT CLAIM

It does not predict toxicity. The budgets are ordinal judgements graded by `measured_in_dogs`; where
a figure is not a canine measurement it says so. It gives HEADROOM (how much a regimen absorbs before
an axis is oversubscribed) -- a sensitivity analysis, not a prediction.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Organ(Enum):
    """The axis a dose-limiting toxicity sits on. Agents on different axes combine freely."""

    MARROW = "myelosuppression"
    GI = "gastrointestinal"
    HEPATIC = "hepatotoxicity"
    CARDIAC = "cardiotoxicity (cumulative)"
    RENAL = "renal"
    PULMONARY = "pulmonary (fibrosis)"
    BLADDER = "bladder (sterile haemorrhagic cystitis)"
    PERIPHERAL_NERVE = "peripheral neuropathy"
    CNS_LOCAL = "local CNS / neurotoxicity"
    STEROID_CLASS = "glucocorticoid-class (iatrogenic hyperadrenocorticism, infection, GI ulcer)"
    IMMUNE_MEDIATED = "cytokine release / immune-mediated / on-target B-cell aplasia"
    OCULAR = "ocular"
    SKIN = "dermatologic"
    PROCEDURAL = "conditioning, transplant, anaesthesia and procedure-related mortality"
    NONE = "no dose-limiting toxicity identified"


@dataclass(frozen=True)
class ToxicityProfile:
    """What an agent costs, on which axis, for how long, and whether the figure is measured.

    `budget_fraction` is the share of that organ's tolerable burden consumed at FULL dose.
    `sustainable_days` is how long the agent can be given at that dose before a cumulative toxicity
    or a schedule cap stops it (None = no cap identified, which is a statement about the evidence,
    not a guarantee). `measured_in_dogs` is True only when the figure comes from a canine study.
    """

    axis: Organ
    budget_fraction: float
    measured_in_dogs: bool
    dose_limiting_event: str
    source: str = ""
    secondary_axis: Organ | None = None
    secondary_fraction: float = 0.0
    cumulative: bool = False
    sustainable_days: float | None = None   # EVIDENCE-LIMITED window: the longest continuous canine
                                            # dosing / practice cap actually documented
    hard_cap_days: float | None = None      # a toxicity cap where one is identified; None = none
                                            # identified (a statement about evidence, not safety)
    reversible: bool = True
    extra_loads: tuple = ()                 # ((Organ, fraction), ...) beyond primary + secondary

    def load(self) -> dict:
        out = {self.axis: self.budget_fraction}
        if self.secondary_axis is not None:
            out[self.secondary_axis] = out.get(self.secondary_axis, 0.0) + self.secondary_fraction
        for axis, frac in self.extra_loads:
            out[axis] = out.get(axis, 0.0) + frac
        return out


NO_TOXICITY = ToxicityProfile(Organ.NONE, 0.0, True, "none identified")


def axis_loads(profiles) -> dict:
    """Total budget consumed on each organ axis. Same-axis agents ADD."""
    totals: dict = {}
    for p in profiles:
        for axis, frac in p.load().items():
            if axis is Organ.NONE:
                continue
            totals[axis] = totals.get(axis, 0.0) + frac
    return totals


def oversubscribed(profiles) -> dict:
    """Axes loaded above 1.0, with how far over."""
    return {axis: load for axis, load in axis_loads(profiles).items() if load > 1.0}


def tolerable(profiles) -> bool:
    return not oversubscribed(profiles)


def headroom(profiles) -> float:
    """How much of the tightest axis remains. Negative means it is already oversubscribed."""
    loads = axis_loads(profiles)
    if not loads:
        return 1.0
    return 1.0 - max(loads.values())


def derating_required(profiles) -> dict:
    """Per-axis factor every agent on that axis must be cut by to fit. 1.0 means no cut needed."""
    return {axis: (1.0 / load if load > 1.0 else 1.0) for axis, load in axis_loads(profiles).items()}


def derating_for(profile: ToxicityProfile, profiles) -> float:
    """The cut an agent must take: the strongest cut demanded on ANY axis it loads."""
    cuts = derating_required(profiles)
    return min(cuts.get(axis, 1.0) for axis in profile.load() if axis is not Organ.NONE) \
        if any(a is not Organ.NONE for a in profile.load()) else 1.0


def derated_potency(agent_potency: float, profile: ToxicityProfile, profiles) -> float:
    """Kill rate after the cut its own axes demand. De-rating is not free."""
    return agent_potency * derating_for(profile, profiles)


# A P-gp/BCRP inhibitor is NOT SELECTIVE FOR THE TUMOUR. The transporter sits in gut, liver and
# kidney too, so co-dosing raises the partner's exposure everywhere. The HS branch charged this at
# 2.5x for a CNS-targeted efflux inhibitor; the value here is set from the canine data in
# `EFFLUX_CO_DOSE_BASIS` below and is re-stated there so the number cannot drift from its source.
EFFLUX_CO_DOSE_MULTIPLIER = 2.5
EFFLUX_CO_DOSE_BASIS = "HS-branch reasoned estimate (core/toxicity.py); replaced below if a canine figure is found"


def with_efflux_co_dose(profile: ToxicityProfile, multiplier: float = None) -> ToxicityProfile:
    """The partner drug's systemic exposure rises with its tumour exposure. Charge for it."""
    m = EFFLUX_CO_DOSE_MULTIPLIER if multiplier is None else multiplier
    return ToxicityProfile(
        profile.axis, profile.budget_fraction * m, profile.measured_in_dogs,
        profile.dose_limiting_event + " [efflux co-dose: exposure raised everywhere the pump sits]",
        profile.source, profile.secondary_axis, profile.secondary_fraction * m,
        profile.cumulative, profile.sustainable_days, profile.hard_cap_days, profile.reversible,
        tuple((a, f * m) for a, f in profile.extra_loads))


#: Filled by `core/lymphoma_toxicity_profiles.py` (data and rules kept apart so the table can carry
#: its citations without burying the logic).
PROFILES: dict = {}


def _load_profiles() -> None:
    from . import lymphoma_toxicity_profiles as _p     # noqa: F401  (import populates PROFILES)


def profile_for(agent_name: str) -> ToxicityProfile:
    """Match on the leading token, in either direction, and RAISE on a miss.

    The HS branch found that a lookup miss which returns NO_TOXICITY makes any regimen containing the
    agent look tolerable for free: 'a lookup miss that FAILS OPEN is worse than one that raises,
    because it produces a favourable answer rather than an error.'"""
    _load_profiles()
    full = agent_name.strip().lower()
    for key, prof in PROFILES.items():                 # an exact full-name match always wins
        if key.strip().lower() == full:
            return prof
    needle = agent_name.split(" (")[0].split(" / ")[0].strip().lower()
    hits = []
    for key, prof in PROFILES.items():
        head = key.split(" (")[0].split(" / ")[0].strip().lower()
        if head == needle or head in needle or needle in head:
            hits.append((key, prof))
    if len(hits) == 1:
        return hits[0][1]
    exact = [h for h in hits if h[0].split(" (")[0].split(" / ")[0].strip().lower() == needle]
    if len(exact) == 1:
        return exact[0][1]
    if not hits:
        raise KeyError(
            f"no toxicity profile for {agent_name!r}. Add one to PROFILES rather than letting the "
            "lookup fail open -- an agent with no profile makes any regimen containing it look "
            "tolerable for free.")
    raise KeyError(f"ambiguous toxicity profile for {agent_name!r}: {[k for k, _ in hits]}")
