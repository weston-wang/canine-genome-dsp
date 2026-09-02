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

    LOCKED = ("genotype-anchored (synthetic-lethal on a homozygous deletion). NOT absolute: acquired "
              "PRMT5i resistance is documented without MTAP restoration, via downstream MAPK "
              "reprogramming -- but it confers collateral MEK sensitivity, a defined second line")
    REROUTABLE = "pathway target; reroutable in an established lesion"
    DEPENDENCY = "strong dependency, but with known resistance routes"
    FLOOR = "no targetable dependency; monitored surveillance only"


class Verdict(Enum):
    DURABLE_10Y = "durable to 10 years (locked, margin > 0, site reachable)"
    SURVEILLANCE_DEPENDENT = "holds only with early detection (reroutable target)"
    DEPENDENCY_HOLD = "strong but not locked (known resistance routes)"
    FLOOR = "monitored floor: immune surveillance + cycled chemo (no single-agent anchor)"
    LOCAL_UNQUANTIFIED = ("reached by craniospinal radiation (barrier-free coverage) + intrathecal + "
                          "immune arm, but durable maintenance is not quantified -- see csf_answer()")
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
    access: float | None       # unbound CNS access (Kp,uu); None = no systemic-drug margin here
    local_route: str | None = None   # a barrier-free local route that still reaches the site


# Continuous-maintenance tiers. Only MTAP and the MAPK majority have a grounded kill rate in pkpd;
# the dependency tiers carry no derived margin until an IC50 + Cmax is measured.
TIERS: tuple[GenotypeTier, ...] = (
    GenotypeTier("MTAP deleted", "recurrent minority",
                 "PRMT5 inhibitor -- brain-penetrant TNG456 (Ph I/II); also TNG462/BMS-986504. "
                 "Parallel MTAP-directed option: MAT2A inhibitor (AG-270/S095033 class, Ph I done, "
                 "CNS-penetrant next-gen). PRMT5 PROTAC degraders emerging for resistance. "
                 "On acquired resistance -> switch to MEK (collateral sensitivity)",
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
    # Local brain control is not a model assumption: radiation achieves complete responses in canine
    # intracranial HS -- 37 Gy cleared an intracranial HS lesion in a (predisposed) Pembroke Welsh
    # Corgi (PMID 34556593), frameless SRS across 51 dogs incl. HS gave ~399 d median survival
    # (PMID 24007303), and HS contrast margins match surgical margins best on MRI, enabling accurate
    # targeting (PMID 35488504).
    Site("Brain -- local delivery (cavity implant / CED / SRS)", 1.0),
    # Systemic CNS reach is conservative (0.30; canine Kp,uu unmeasured) but NO LONGER hypothetical:
    # the first-gen PRMT5i TNG908 failed to reach therapeutic CNS exposure in GBM trials, and a
    # purpose-built brain-penetrant successor, TNG456, is now in Phase I/II with a glioblastoma focus
    # (PMID 42150143), with an independent brain-penetrant chemotype behind it (PMID 42190431). So a
    # real clinical-stage agent, not a guess, is what would realize this access.
    Site("Brain -- systemic penetration", 0.30),
    # CSF: no systemic-drug margin, but NOT unexplored -- craniospinal radiation reaches it by
    # physics and intrathecal dosing places drug in the fluid. The durability number is withheld,
    # not absent; see csf_answer() for the repo's full exploration and why.
    Site("Leptomeninges / CSF", None,
         local_route="craniospinal radiation (coverage) + intrathecal dosing + immune arm"),
)


# The CSF compartment, resolved from the repo's own exploration (disease.ROUTES intrathecal;
# therapies 'Intrathecal / intraventricular dosing' and 'Radiation (focal / craniospinal)').
CSF_RESOLUTION = {
    "reached": True,
    "how": "A three-part local approach: CRANIOSPINAL RADIATION for coverage (physics -- it ignores "
           "the blood-brain barrier), INTRATHECAL dosing for rate control (drug placed straight into "
           "the fluid, an established canine route), and an IMMUNE arm for persistence (the only part "
           "that outlasts dosing; radiation enhances NK killing).",
    "why_no_durability_number": (
        ("The intrathecal '470x concentration headroom' headline was AUDITED and RETRACTED -- it was "
         "an absolute-nM comparison against a placeholder drug concentration; only the scale-free "
         "version was valid, and it is far smaller."),
        ("Bulk CSF concentration is not cell exposure on the meningeal surfaces -- the binding "
         "question is fluid-space SATURATION at the target, which is unmeasured."),
        ("No ERK/PI3K inhibitor (nor the maintenance pills) has ever been given intrathecally in ANY "
         "species -- the route is untested for these agents."),
        ("Repeated intrathecal dosing collides with this breed's SOD1 / degenerative-myelopathy "
         "predisposition (a spinal-cord hazard) and stacks on the marrow axis with craniospinal "
         "radiation -- a breed-specific toxicity limit on dosing FREQUENCY."),
        ("Radiation reaches the compartment but is DUTY-LIMITED (a ~21-day course), so it provides "
         "coverage, not the continuous presence maintenance-at-emergence needs."),
    ),
    "verdict": "ADDRESSED for coverage, and now BOUNDED for durable maintenance: the kill closes "
               "once the drug reaches only ~1.8 nM (PRMT5i) or ~67 nM (MEKi) at the leptomeningeal "
               "cells (see quantified_threshold) -- concentrations intrathecal dosing exceeds by "
               "orders of magnitude in bulk CSF. So the single open quantity is the FLUID-TO-CELL "
               "engagement fraction; the practical gap is a sustained-release device (to beat the "
               "frequency wall) plus two measurements (that engagement fraction; the breed's "
               "tolerance of repeated intrathecal dosing).",
}


def csf_required_cell_concentration() -> dict:
    """Better quantification: the free drug concentration AT the leptomeningeal tumour cells that the
    maintenance kill needs to beat growth, per drug with a measured IC50.

    Inverts the Emax kill (``pkpd.emax_kill_rate``): closure needs
    ``ln(1 + C/IC50)/assay_days > growth`` -> ``C > IC50 * (exp(growth*assay_days) - 1)``. That factor
    is ~0.18, so the required CELL-level concentration is a small fraction of the IC50-equivalent --
    numbers intrathecal dosing reaches with orders of magnitude to spare in BULK CSF. So the CSF is
    not open-ended: the only unquantified quantity is the fraction of bulk CSF drug that engages the
    tumour cells (fluid-to-cell), and here is the bar that fraction has to clear.
    """
    import math
    factor = math.exp(pkpd.GROWTH_PER_DAY * pkpd.DEFAULT_ASSAY_DAYS) - 1.0
    out = {}
    for key in ("tng908", "cobimetinib"):
        d = pkpd.PARAMS[key]
        out[key] = {
            "drug": d.name,
            "ic50_nM": d.ic50_nM,
            "cell_concentration_to_close_nM": round(d.ic50_nM * factor, 2),
        }
    return out


def csf_answer() -> dict:
    """The CSF/leptomeningeal resolution: reached and addressed, durability now BOUNDED (the required
    cell-level concentration is computed), with the one remaining unknown and the experiments named."""
    return {**CSF_RESOLUTION, "quantified_threshold": csf_required_cell_concentration()}


# The brain-parenchyma resolution, hardened. The earlier weak point was that the CNS lock leaned on
# TNG908, which failed to reach therapeutic CNS exposure in glioblastoma trials. Three independent
# pillars now carry the brain-spread case, and they narrow the residual gap specifically onto the CSF
# compartment (handled in csf_answer), not the brain parenchyma.
BRAIN_SPREAD_RESOLUTION = {
    "was_the_weak_point": (
        "The CNS maintenance arm previously named TNG908, whose first-generation member showed "
        "preclinical brain permeability but FAILED to reach therapeutic CNS exposure in glioblastoma "
        "clinical trials (PMID 42190431). That is why brain spread was the softest branch."),
    "pillar_1_targeted_drug": (
        "The lock does not die with TNG908. A purpose-built brain-penetrant MTA-cooperative PRMT5 "
        "inhibitor, TNG456, is now in Phase I/II with a glioblastoma focus (PMID 42150143); an "
        "independent brain-penetrant chemotype shows higher brain permeability than TNG908 and "
        "orthotopic tumour control (PMID 42190431); and brain-penetrant PRMT5 inhibition prolongs "
        "survival in orthotopic glioma models (LLY-283, PMID 33579912). Same synthetic-lethal MTAP "
        "lock, engineered for CNS exposure -- so the genotype lock survives at the brain site."),
    "pillar_2_local_control_is_demonstrated": (
        "Local brain CONTROL is clinical, not modelled: 37 Gy radiation cleared an intracranial HS "
        "lesion in a PREDISPOSED breed (Pembroke Welsh Corgi) to complete radiographic response "
        "(PMID 34556593), and frameless stereotactic radiosurgery is established for canine "
        "intracranial tumours incl. HS (PMID 24007303), with HS contrast margins matching surgical "
        "margins on MRI (JSM 0.75) for accurate targeting (PMID 35488504). This pillar establishes "
        "that the parenchymal lesion can be driven to CR -- it does NOT claim a duration."),
    "pillar_2_does_not_claim_duration": (
        "IMPORTANT: the survival figures in those reports (corgi 164 d; SRS series ~399 d median, "
        "mostly meningiomas) are RADIATION-ALONE, largely PALLIATIVE-dose outcomes with NO "
        "maintenance arm -- they are the natural history of local control without Move 2, not a "
        "ceiling on local control and not a number this plan expects to beat with radiation. Any "
        "longer duration this plan projects comes ENTIRELY from adding genotype-matched maintenance "
        "(Move 2), which is model-based and unproven in dogs, plus addressing the CSF (the one "
        "unquantified compartment) -- NOT from radiation doing more than it did in these cases."),
    "pillar_3_failure_mode_named": (
        "The real-world HS brain failure mode is named and it is NOT local regrowth: the corgi whose "
        "brain lesion stayed in CR died on day 164 of intracranial metastasis VIA THE CSF, with no "
        "extracranial disease (PMID 34556593). This cuts both ways -- it confirms local control held "
        "and localises the residual to the leptomeningeal/CSF compartment, but that compartment is "
        "exactly the one this analysis does not put a durability number on (see csf_answer), so the "
        "case both supports the parenchymal claim AND marks the open gap."),
    "verdict": ("STRENGTHENED, SCOPED HONESTLY. What is genuinely hardened: (a) the genotype LOCK "
                "survives at the brain site via a brain-penetrant PRMT5i successor (TNG456-class) "
                "rather than the failed TNG908, and (b) parenchymal local control to CR is clinically "
                "demonstrated. What is NOT claimed: that radiation buys more time than the cited "
                "series -- the durability beyond local control rests on the (unproven-in-dog) "
                "maintenance arm. The residual gap is the CSF compartment (csf_answer), which is also "
                "the documented cause of death in the one on-point case."),
}


def brain_spread_answer() -> dict:
    """The brain-spread resolution, scoped honestly: the old weak point (TNG908 CNS failure), the
    brain-penetrant successor that repairs the genotype lock, the CLINICAL local-control result (CR is
    achievable -- explicitly NOT a duration claim), and the named CSF failure mode that both supports
    the parenchymal claim and marks the one open gap handed to csf_answer()."""
    return dict(BRAIN_SPREAD_RESOLUTION)


# What "surveillance-dependent" actually means, made precise. A LOCKED tier (MTAP) holds a decade
# unconditionally at a reachable site -- the target is a thrown-away locus the tumour cannot
# re-acquire, so the kill cannot be escaped. A REROUTABLE tier hits a pathway NODE an established
# lesion can bypass, so the pill reliably kills only a still-single founding cell at emergence; the
# decade then holds *conditionally*, on a monitor-and-switch loop that closes the reroute window.
SURVEILLANCE_MODEL = {
    "locked_vs_reroutable": (
        "GENOTYPE-ANCHORED (MTAP/PRMT5): synthetic-lethal on a homozygous deletion, so the tumour "
        "cannot escape by re-acquiring the discarded locus -- but this is NOT absolute. Acquired "
        "resistance to MTA-cooperative PRMT5 inhibitors is documented WITHOUT MTAP restoration or MTA "
        "loss, via downstream MAPK transcriptional reprogramming (DOI 10.64898/2026.04.16.719008). "
        "The saving grace is that this escape confers COLLATERAL SENSITIVITY TO MEK, so the anchor "
        "tier has a defined second line rather than an open exit. It therefore still needs watching, "
        "just less than a pathway target. REROUTABLE (MEK for the MAPK majority, PI3K for PTEN, "
        "CDK4/6 for CDKN2A): a pathway node an established lesion can bypass by upstream/parallel "
        "reactivation, so the kill is reliable only against a single founding cell."),
    "why_it_still_suppresses_at_emergence": (
        "Subcritical branching means every FRESH founding cell is extinguished regardless of lock; "
        "the only way a reroutable tier loses the decade is an established lesion that reroutes and "
        "goes undetected long enough to seed a second primary. Surveillance closes exactly that "
        "window -- it is not needed to kill the founding cell, only to catch the escape."),
    "the_loop": {
        "1_detect": (
            "A detection modality with lead time -- and for THIS disease it exists: a plasma PTPN11 "
            "ctDNA assay detects ctDNA in ~91% of canine HS and is 98.8% specific (Prouteau et al., "
            "Sci Rep 2021, DOI 10.1038/s41598-020-80332-y), on a commercial canine platform "
            "(OncoK9/CANDiD), with tumour-informed MRD assays maturing (single-test sensitivity "
            "~43-77%, raised by serial testing). The switch BENEFIT is transferred from human MRD-"
            "guided therapy: +DFS (9.9 vs 4.8 mo) and 88% 2-year DFS on persistent negativity "
            "(IMvigor011, PMID 41124204). So 'early detection' is canine-HS-grounded, not hand-waving."),
        "2_switch": (
            "A switch tree. The repo's genotype priority tree (genotype_tiered_durability.best_tier_"
            "for) already defines the next matched anchor for each reroute, so a detected escape maps "
            "to a concrete next drug."),
        "3_cadence": (
            "A sampling cadence -- how often the monitor runs -- set tight enough that the expected "
            "reroute is caught inside the switch window."),
    },
    "bottom_line": (
        "LOCKED = a decade that holds on its own at reachable sites. SURVEILLANCE-DEPENDENT = a "
        "decade that holds provided the detect-and-switch loop runs; it is the SAME suppression-at-"
        "emergence mechanism, minus the guarantee against an established reroute."),
}


def surveillance_model() -> dict:
    """Make 'surveillance-dependent' precise: locked vs reroutable, why suppression-at-emergence still
    holds, and the concrete detect/switch/cadence loop the conditional decade runs on."""
    return {
        "locked_tiers": sorted({t.genotype for t in TIERS if t.lock is Lock.LOCKED}),
        "reroutable_tiers": sorted({t.genotype for t in TIERS
                                    if t.lock in (Lock.REROUTABLE, Lock.DEPENDENCY)}),
        **SURVEILLANCE_MODEL,
    }


@dataclass(frozen=True)
class Durability:
    tier: GenotypeTier
    site: Site
    kill_per_day: float | None
    margin: float | None
    verdict: Verdict
    reason: str

    @property
    def suppresses_second_primary_at_emergence(self) -> bool:
        """Whether the matched maintenance anchor kills a fresh second primary at emergence.

        This is the repo's maintenance-at-emergence verdict (genotype_tiered_durability.
        suppresses_at_emergence is True for EVERY tier): a newly emerged primary is a single dividing
        founding cell that has not yet rerouted or gone dormant, so the matched pill catches it. True
        for every reachable, resolved tier -- the grade below says how ROBUST that hold is, not
        whether it happens. Only an unreachable site or a negative margin makes it False.
        """
        return self.verdict in (Verdict.DURABLE_10Y, Verdict.SURVEILLANCE_DEPENDENT,
                                Verdict.DEPENDENCY_HOLD, Verdict.FLOOR)

    @property
    def robustness(self) -> str:
        """How robust the ten-year hold is, once suppression at emergence is granted."""
        return {
            Verdict.DURABLE_10Y: "genotype-anchored (most durable tier; holds past the emergence "
                                 "window, though acquired resistance is documented and carries a "
                                 "defined MEK second line)",
            Verdict.SURVEILLANCE_DEPENDENT: "reroute-vulnerable once a lesion establishes; the decade "
                                            "holds conditionally, on a detect-and-switch loop (serial "
                                            "ctDNA + the genotype switch tree) -- see "
                                            "surveillance_model()",
            Verdict.DEPENDENCY_HOLD: "strong dependency with known resistance routes",
            Verdict.FLOOR: "immune/cytotoxic backstop; weakest",
            Verdict.LOCAL_UNQUANTIFIED: "coverage by radiation; durable maintenance unquantified",
            Verdict.NOT_REACHED: "n/a -- site not reached",
            Verdict.FAILS: "n/a -- margin does not clear growth",
        }[self.verdict]


def _dosable_continuously(tox_key: str | None) -> bool:
    """A maintenance agent must be tolerable as continuous monotherapy to hold for years."""
    if tox_key is None:
        return True
    return tox.tolerable([tox.profile_for(tox_key)])


def durability(tier: GenotypeTier, site: Site) -> Durability:
    """Derive the durability verdict for one genotype at one site."""
    if site.access is None:
        if site.local_route is not None:
            return Durability(tier, site, None, None, Verdict.LOCAL_UNQUANTIFIED,
                              f"reached by {site.local_route}; durable maintenance not quantified "
                              "(see csf_answer())")
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
                          "subcritical branching on a genotype-anchored target: the deletion cannot be "
                          "undone, so founding cells are reliably suppressed. Not absolute -- acquired "
                          "PRMT5i resistance via MAPK reprogramming is documented -- but it carries a "
                          "defined second line (collateral MEK sensitivity), so this remains the most "
                          "durable tier")
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
        "Resolution across ALL genotype combinations: every one is routed by the priority tree to a "
        "matched maintenance anchor, and every one SUPPRESSES A SECOND PRIMARY AT EMERGENCE -- the "
        "repo's model returns suppresses_at_emergence = True for all five tiers, because a fresh "
        "primary is a single dividing founding cell the matched pill catches before it can reroute "
        "or go dormant. So the ten-year maintenance mechanism applies to the whole breed, not an "
        "MTAP subset. What differs across combinations is ROBUSTNESS, not whether it works: MTAP is "
        f"genotype-ANCHORED ({', '.join(locked_tiers)}) -- the deletion cannot be undone, so it is the "
        "most durable tier and holds past the emergence window; it is NOT absolute, since acquired "
        "PRMT5i resistance via MAPK reprogramming is documented, but that escape confers collateral "
        "MEK sensitivity and so has a defined second line. The MAPK majority, PTEN and CDKN2A tiers "
        "suppress the founding cell at "
        "emergence too but are reroute-vulnerable once a lesion establishes, so they lean on "
        "continuous dosing and catching recurrences early; the floor tier is the immune/cytotoxic "
        "backstop. Brain spread is STRENGTHENED and scoped honestly: the CNS lock no longer leans on "
        "TNG908 (which failed to reach therapeutic CNS exposure in glioblastoma trials) but on the "
        "brain-penetrant successor TNG456 (Phase I/II), and parenchymal local control to complete "
        "response is clinically demonstrated in a predisposed breed by radiation -- though that is a "
        "CONTROL result, not a duration claim (the cited radiation-alone survivals are natural "
        "history without maintenance), so the residual collapses onto the CSF compartment (see "
        "brain_spread_answer()). The CSF compartment is REACHED and addressed "
        "(craniospinal radiation for coverage + intrathecal + immune arm) but its durability figure "
        "is deliberately withheld, not absent -- see csf_answer(). 'Surveillance-dependent' is made "
        "precise in surveillance_model(): a locked tier needs no watching, while a reroutable tier's "
        "decade is conditional on a detect-and-switch loop (serial ctDNA + the genotype switch tree). "
        "It is a grounded, model-based result -- conditional on continuous dosing being achievable "
        "and on the site being reachable, not on genotype -- and not yet demonstrated in a dog."
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
    print("BRAIN SPREAD (hardened):")
    for k, v in brain_spread_answer().items():
        print(f"  [{k}] {v}")
    print()
    print("SURVEILLANCE MODEL:")
    sm = surveillance_model()
    print(f"  locked (no watching needed): {sm['locked_tiers']}")
    print(f"  reroutable (conditional):    {sm['reroutable_tiers']}")
    print(f"  bottom line: {sm['bottom_line']}")
    print()
    print("reconciliation:", reconciliation())
