"""Ten-year durability, derived per genotype and per site — not asserted, and not uniform.

THE QUESTION THIS ANSWERS
-------------------------
Closing escape 12 (the maintenance arm) says a single new lesion-carrying cell is killed at
emergence. Ten-year durability is the stronger claim that a *second primary* never establishes over a
decade. This module derives that claim from grounded inputs instead of a hand-set potency, and — the
whole point — returns different answers for different genotypes and sites, including "cannot be
computed" where the inputs do not exist.

THE MODEL (branching-process suppression)
-----------------------------------------
A new primary begins as one founding cell. Under continuous maintenance it divides (net growth
``g``) and is killed by the drug at rate ``k_eff = pkpd kill_rate_at(site access) x duty``. The
lineage is a birth-death branching process with net rate ``g - k_eff``:

  * margin ``m = k_eff - g > 0``  -> subcritical -> the founding cell's lineage goes extinct with
    probability 1. Every founding cell that emerges is suppressed, so the horizon length and the
    (unmeasured) emergence rate drop out: no second primary establishes.
  * margin ``m <= 0``            -> supercritical -> escape is possible; durability FAILS.

So ``m > 0`` is necessary. It is not sufficient, because two more conditions decide whether it HOLDS
for ten years:

  1. GENOTYPE LOCK. A synthetic-lethal target on a homozygous deletion (MTAP) cannot be rerouted —
     escaping would mean re-acquiring a thrown-away locus — so the margin cannot be eroded: DURABLE.
     A pathway target (MEK for the MAPK majority) is reroutable in an *established* lesion, so the
     kill is reliable only against a still-single founding cell: SURVEILLANCE-DEPENDENT, not locked.
  2. REACH. The founding cell must be where the drug is. Lung and a local-delivery brain cavity are
     reachable; systemic brain penetration is unmeasured; the CSF compartment's drug saturation is
     unknown -> NOT_REACHED, no durability number (matching the report's refusal to compute one).

Continuous dosing must also be tolerable for years; each maintenance monotherapy is checked against
``core.toxicity`` (all pass as single agents, but the check is structural, not assumed).

RECONCILIATION WITH THE OLDER MODEL
-----------------------------------
``core.breed_wide_durability`` used a hand-set potency of 0.15/day, giving an access threshold near
0.37 (so it read "fails at 0.30"). This module derives ``k_eff`` from the measured IC50 + Cmax via
``pkpd``, so the raw margin clears at far lower access — but the decisive line is not the raw margin,
it is the LOCK. That is why the honest verdict is "a decade for the locked MTAP tier; surveillance
for the reroutable majority," independent of which potency number one plugs in.

This is an analysis, not veterinary advice.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from . import pkpd
from .core import genotype_tiered_durability as gtd
from .core import toxicity as tox

GROWTH_PER_DAY = pkpd.GROWTH_PER_DAY
DUTY_CONTINUOUS = 1.0  # a maintenance pill taken every day


class Lock(Enum):
    """Can the tumour reroute around the maintenance target?"""

    LOCKED = "genotype-locked (synthetic-lethal on a homozygous deletion; non-reroutable)"
    REROUTABLE = "pathway target; reroutable in an established lesion"
    DEPENDENCY = "strong dependency, but with known resistance routes"
    FLOOR = "no targetable dependency; monitored surveillance only"


class Verdict(Enum):
    DURABLE_10Y = "durable to 10 years (locked, margin > 0, site reachable)"
    SURVEILLANCE_DEPENDENT = "holds only with early detection (reroutable target)"
    DEPENDENCY_HOLD = "strong but not locked (known resistance routes)"
    FLOOR = "monitored floor: immune surveillance + cycled chemo (no single-agent anchor)"
    NOT_REACHED = "site not reachable / access unmeasured -- no durability number"
    FAILS = "margin <= 0: the drug cannot beat growth at this access"


@dataclass(frozen=True)
class GenotypeTier:
    genotype: str
    rough_share: str
    maintenance: str
    lock: Lock
    pkpd_key: str | None       # key into pkpd.PARAMS, or None if potency is not grounded
    tox_key: str | None        # key into core.toxicity.PROFILES for the continuous-dosing check


@dataclass(frozen=True)
class Site:
    name: str
    access: float | None       # unbound CNS access (Kp,uu); None = unknown / not computable


# Continuous-maintenance tiers. Only MTAP and the MAPK majority have a grounded kill rate in pkpd;
# the dependency tiers carry no derived margin until an IC50 + Cmax is measured.
TIERS: tuple[GenotypeTier, ...] = (
    GenotypeTier("MTAP deleted", "recurrent minority", "PRMT5 inhibitor (TNG908/462)",
                 Lock.LOCKED, "tng908", "PRMT5 inhibitor"),
    GenotypeTier("MAPK driver (SHP2/KRAS)", "~59%", "MEK inhibitor (mirdametinib)",
                 Lock.REROUTABLE, "cobimetinib", "mirdametinib"),
    GenotypeTier("PTEN deleted", "minority", "PI3K inhibitor (paxalisib)",
                 Lock.DEPENDENCY, None, "paxalisib"),
    GenotypeTier("CDKN2A deleted, RB1 intact", "minority", "CDK4/6 inhibitor (abemaciclib)",
                 Lock.DEPENDENCY, None, "abemaciclib"),
    GenotypeTier("None targetable", "residual", "immune surveillance + cycled lomustine",
                 Lock.FLOOR, None, "lomustine"),
)

SITES: tuple[Site, ...] = (
    Site("Lung / disseminated", 1.0),
    Site("Brain -- local delivery (cavity implant / CED)", 1.0),
    Site("Brain -- systemic penetration", 0.30),   # conservative; canine value unmeasured
    Site("Leptomeninges / CSF", None),             # drug saturation unknown -> not computable
)


@dataclass(frozen=True)
class Durability:
    tier: GenotypeTier
    site: Site
    kill_per_day: float | None
    margin: float | None
    verdict: Verdict
    reason: str


def _dosable_continuously(tox_key: str | None) -> bool:
    """A maintenance agent must be tolerable as continuous monotherapy to hold for years."""
    if tox_key is None:
        return True
    return tox.tolerable([tox.profile_for(tox_key)])


def durability(tier: GenotypeTier, site: Site) -> Durability:
    """Derive the durability verdict for one genotype at one site."""
    if site.access is None:
        return Durability(tier, site, None, None, Verdict.NOT_REACHED,
                          "drug saturation of this compartment is unmeasured; no margin computable")
    if tier.pkpd_key is None:
        # No measured IC50+Cmax to derive a margin -- defer to the repo's genotype tree, which
        # already resolves every tier (the answer the repo carries). Still resolved, just not
        # pkpd-quantified.
        if tier.lock is Lock.FLOOR:
            return Durability(tier, site, None, None, Verdict.FLOOR,
                              "immune surveillance + cycled chemo; a strategy, not a single-agent "
                              "anchor -- no case is left with nothing, but this is the weakest tier")
        return Durability(tier, site, None, None, Verdict.DEPENDENCY_HOLD,
                          "matched dependency anchor from the genotype tree; strong but reroutable "
                          "via known resistance, and its per-day kill is not yet pkpd-derived "
                          "(needs a measured IC50 + Cmax)")

    drug = pkpd.PARAMS[tier.pkpd_key]
    k_eff = drug.kill_rate_at(site.access) * DUTY_CONTINUOUS
    margin = k_eff - GROWTH_PER_DAY

    if margin <= 0:
        return Durability(tier, site, k_eff, margin, Verdict.FAILS,
                          f"derived kill {k_eff:.3f}/day does not beat growth {GROWTH_PER_DAY}/day")
    if not _dosable_continuously(tier.tox_key):
        return Durability(tier, site, k_eff, margin, Verdict.FAILS,
                          "cannot be dosed continuously (single-agent toxicity oversubscribed)")

    if tier.lock is Lock.LOCKED:
        return Durability(tier, site, k_eff, margin, Verdict.DURABLE_10Y,
                          "subcritical branching + non-reroutable target: founding cells go extinct "
                          "with probability 1, so no second primary establishes")
    if tier.lock is Lock.REROUTABLE:
        return Durability(tier, site, k_eff, margin, Verdict.SURVEILLANCE_DEPENDENT,
                          "kill wins against a single founding cell, but an established lesion can "
                          "reroute the target; holds only if recurrences are caught early")
    return Durability(tier, site, k_eff, margin, Verdict.DEPENDENCY_HOLD,
                      "strong dependency, but known resistance routes prevent a genotype lock")


def _tier_for_gtd_genotype(name: str) -> GenotypeTier:
    """Map a genotype_tiered_durability tier name onto the matching tier here."""
    n = name.upper()
    if "MTAP" in n:
        return TIERS[0]
    if "PTEN" in n:
        return TIERS[2]
    if "CDKN2A" in n:
        return TIERS[3]
    if any(k in n for k in ("SHP2", "KRAS", "PTPN11", "MAPK")):
        return TIERS[1]
    return TIERS[4]


def resolve(markers: set, site: Site) -> Durability:
    """Resolve ANY marker combination to a durability verdict at a site.

    Uses the repo's priority tree (`genotype_tiered_durability.best_tier_for`): the strongest anchor
    a tumour qualifies for wins, so a tumour carrying several markers (e.g. an MTAP deletion AND a
    SHP2 driver) is routed to its best anchor (MTAP), not left ambiguous. Every combination -- empty
    set included -- resolves to exactly one tier, which is what "resolution on all combinations"
    means: no case is left without a matched anchor.
    """
    chosen = gtd.best_tier_for(set(markers))
    return durability(_tier_for_gtd_genotype(chosen.genotype), site)


#: Representative marker combinations, including a co-occurring pair, to demonstrate the priority
#: tree resolves every case (not an exhaustive genotype space -- the tree handles any set).
MARKER_COMBOS: tuple[tuple[frozenset, str], ...] = (
    (frozenset({"MTAP_del"}), "MTAP deletion"),
    (frozenset({"MTAP_del", "SHP2"}), "MTAP deletion + SHP2 driver (co-occurring -> MTAP wins)"),
    (frozenset({"SHP2"}), "SHP2 / PTPN11 driver"),
    (frozenset({"KRAS"}), "KRAS driver"),
    (frozenset({"PTEN_del"}), "PTEN deletion"),
    (frozenset({"CDKN2A_del", "RB1_intact"}), "CDKN2A deletion, RB1 intact"),
    (frozenset({"CDKN2A_del"}), "CDKN2A deletion, RB1 lost/unknown (-> floor)"),
    (frozenset(), "no targetable marker"),
)


def full_resolution(site: Site | None = None) -> list[tuple[str, Durability]]:
    """Resolve every representative marker combination at one site (default lung)."""
    site = site or SITES[0]
    return [(label, resolve(set(markers), site)) for markers, label in MARKER_COMBOS]


def grid() -> list[Durability]:
    """Every genotype x site durability verdict."""
    return [durability(t, s) for t in TIERS for s in SITES]


def durable_scenarios() -> list[Durability]:
    """The (genotype, site) pairs that reach a locked ten-year hold."""
    return [d for d in grid() if d.verdict is Verdict.DURABLE_10Y]


def reconciliation() -> dict:
    """Show that the raw margin clears at far lower access than the old hand-set model implied,
    and that the LOCK -- not the potency number -- is what separates a decade from surveillance."""
    tng = pkpd.PARAMS["tng908"]
    cob = pkpd.PARAMS["cobimetinib"]
    return {
        "old_hand_set_potency_per_day": 0.15,
        "old_access_threshold_approx": round(GROWTH_PER_DAY / 0.15, 3),   # ~0.367
        "derived_min_access_MTAP_tng908": round(tng.min_access_to_close(), 4),
        "derived_min_access_MAPK_cobimetinib": round(cob.min_access_to_close(), 4),
        "decisive_condition": "genotype lock, not the raw margin: MTAP is non-reroutable (durable) "
                              "while the MAPK majority is reroutable (surveillance-dependent). "
                              "Absolute margins are not comparable here -- TNG908's Cmax is a "
                              "placeholder -- so the lock, not the number, separates a decade from "
                              "surveillance.",
    }


def headline() -> str:
    """One paragraph: what ten-year durability actually resolves to, by genotype and site."""
    durable = durable_scenarios()
    locked_tiers = sorted({d.tier.genotype for d in durable})
    return (
        "Every genotype combination resolves to a matched maintenance anchor via the priority tree "
        "(resolve()/best_tier_for) -- no case is left without one, and a tumour carrying several "
        "markers routes to its strongest anchor. But durability is not uniform, and it is derived, "
        "not asserted. It resolves to a "
        f"locked decade only where the target is non-reroutable AND the site is reachable: "
        f"{', '.join(locked_tiers)} at lung and reachable-brain sites. The MAPK majority (~59%) is "
        "surveillance-dependent -- not because its kill is too weak (its derived margin is "
        "comfortably positive) but because a pathway target reroutes in an established lesion, "
        "unlike the MTAP synthetic-lethal lock. The CSF compartment returns no durability number "
        "(drug saturation unmeasured), and the dependency tiers need a measured IC50 + Cmax before a "
        "margin can be derived at all. Caveats on the numbers: TNG908's Cmax is a placeholder, so "
        "the MTAP margin MAGNITUDES are illustrative -- the verdict rests only on margin > 0, which "
        "holds across any plausible access (min access to close ~0.2%). Every 'durable' verdict is "
        "conditional on the MTAP-deleted status (the falsifier) and on continuous dosing being "
        "achievable -- it is a grounded model result, not a demonstrated outcome in any dog."
    )


if __name__ == "__main__":
    print(headline())
    print()
    print("EVERY MARKER COMBINATION, resolved at the lung site (priority tree):")
    for label, d in full_resolution():
        print(f"  {label:52} -> {d.tier.maintenance:34} | {d.verdict.name}")
    print()
    print("FULL genotype x site grid:")
    for d in grid():
        m = f"{d.margin:+.3f}" if d.margin is not None else "  n/a"
        print(f"  {d.tier.genotype:28} | {d.site.name:44} | margin {m} | {d.verdict.name}")
    print()
    print("reconciliation:", reconciliation())
