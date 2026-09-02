"""Durable maintenance for EVERY genotype, not only the MTAP-deleted one.

THE CORRECTION THIS MODULE MAKES

`breed_wide_durability` bought ten-year durability with a maintenance arm that is synthetic-lethal
against the MTAP deletion. That is real, but MTAP deletion is a RECURRENT MINORITY, not the whole
disease. The measured somatic driver landscape of canine histiocytic sarcoma is:

    PTPN11 / SHP2 activating mutation      ~56%   (PMID 39258288; MAPK pathway)
    KRAS activating mutation               ~3%    (same; MAPK pathway)
    MTAP / CDKN2A homozygous deletion      recurrent minority (CFA11q16)
    RB1 deletion                           minority
    PTEN deletion                          minority

So the SINGLE most common thing is a MAPK driver (~59%), and the MTAP-anchored answer does NOTHING
for it. A durable response "for all cases" cannot rest on one lesion. It has to be a DECISION TREE
keyed on the tumour's own genotype -- read once from the same tissue by a small NGS panel.

THE INDUCTION IS GENOTYPE-AGNOSTIC ALREADY

Clearing the first tumour does not change per genotype: `microtubule_route` / `breed_wide_durability`
induction closes all eleven escapes at both sites regardless of driver, because a mitotic poison plus
the escape-closing backbone does not care which lesion started the tumour. Genotype only decides the
MAINTENANCE arm -- the part that has to hold for ten years by killing a SECOND primary at emergence.

THE MAINTENANCE TREE (best available anchor wins; all anchors are brain-penetrant and oral/continuous)

    tumour genotype                 anchor                              kind            grade
    MTAP-deleted                    PRMT5i (TNG908/462)                 synthetic-lethal STRONG
    PTEN-deleted                    PI3K inhibitor (paxalisib)          dependency       STRONG
    CDKN2A-deleted, RB1 INTACT      CDK4/6i (abemaciclib)               dependency       MEDIUM-STRONG
    PTPN11/SHP2 or KRAS driver      MEKi (mirdametinib, CNS-penetrant)  pathway-driver   MEDIUM
    none targetable / unknown       immune surveillance + cycled        genotype-        FLOOR
                                    microtubule                          agnostic

WHY THE GRADES DIFFER, AND WHY IT IS HONEST

  * SYNTHETIC-LETHAL (PRMT5 on MTAP-loss): the cell cannot reroute around a homozygous deletion.
    Kills established AND emergent disease. The clean ten-year anchor.
  * DEPENDENCY (PI3K on PTEN-loss; CDK4/6 on CDKN2A-loss): the lost suppressor makes the cell lean on
    one node. Strong, but resistance exists -- and CDK4/6 needs RB1 INTACT, so an RB1-deleted tumour
    (a recurrent minority) drops through to the floor.
  * PATHWAY-DRIVER (MEK on SHP2/KRAS): a MEK block is REROUTABLE in an established tumour -- that is
    literally three of the eleven escapes (MAPK reactivation, MEK-site mutation, activating ERK). But
    a SECOND PRIMARY starts as ONE cell with only its founding driver and none of those reroute
    lesions yet, and a maintenance MEK inhibitor kills that founding cell before it can seed them.
    So MEK maintenance is durable against a NEW primary IF surveillance catches it early -- it is not
    durable against established rerouted disease, which is what re-induction is for. Honest MEDIUM.
  * FLOOR (immune + cycled microtubule): genotype-independent, so it is the backstop for a tumour
    with no targetable lesion or an unknown genotype. Weakest -- "monitored years", not a clean lock.
    But it is never nothing, so no case is left with "clear it and hope".

THE KEY MOVE THAT GENERALISES THE MTAP INSIGHT

The MTAP arm's magic was "kill the second primary at emergence." That does NOT actually require
synthetic lethality -- it requires an agent matched to the founding driver, given continuously, that
reaches where the primary would arise. Synthetic lethality is the STRONGEST version because it also
survives reroute, but every tier here kills the founding clone at emergence. The difference between
tiers is how well they hold if the second primary is caught LATE.

WHAT DECIDES THE TIER, AND IT IS STILL ONE TEST

Not one stain now -- a small NGS panel (MTAP/CDKN2A/PTEN copy number, PTPN11/KRAS/RB1 sequence) on the
same tumour tissue. Every branch is determined by it, and it is run once.

WHAT IS STILL ASSUMED

  * The frequencies are from canine cohorts weighted to Bernese/Golden/Flat-coated; the breed-specific
    split is not established (this breed cases DO carry TP53 variants at 4/7, which this tree treats only as
    an induction/prognosis modifier, not a maintenance anchor -- there is no clean TP53 maintenance).
  * Every anchor's canine CNS access and potency are unmeasured, as everywhere in this project.
  * The MEK-maintenance-catches-emergence argument depends on SURVEILLANCE frequent enough to catch a
    second primary while it is still founding-driver-only. That cadence is not modelled.
  * Drivers CO-OCCUR (a tumour can be SHP2-mutant AND MTAP-deleted); the tree takes the strongest
    available anchor, which is correct, but real tumours may qualify for two arms at once.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from . import toxicity as tox
from .catalogue import ESCAPES, GROWTH_PER_DAY
from .dormancy import DormancyModel
from .regimen import Agent, Axis, Escape, Layer, Regimen


class AnchorKind(Enum):
    SYNTHETIC_LETHAL = "synthetic-lethal on a homozygous deletion (not reroutable)"
    DEPENDENCY = "dependency created by a lost suppressor (slow resistance)"
    PATHWAY_DRIVER = "block on the founding driver (reroutable once established)"
    AGNOSTIC = "genotype-independent surveillance floor"


class Grade(Enum):
    STRONG = "kills established and emergent disease"
    MEDIUM_STRONG = "dependency; resistance exists; gated on a co-factor"
    MEDIUM = "kills the second primary at emergence; needs surveillance; not durable if established"
    FLOOR = "genotype-independent backstop; monitored years, not a clean lock"


@dataclass(frozen=True)
class Tier:
    genotype: str
    approx_frequency: str
    anchor_agent: str          # key into toxicity.PROFILES (or a description for the floor)
    kind: AnchorKind
    grade: Grade
    axis: Axis
    layer: Layer
    division_gated: bool
    brain_penetrant: bool
    note: str


#: Priority order: strongest anchor first. The best anchor a tumour qualifies for wins.
TIERS = (
    Tier("MTAP-deleted", "recurrent minority", "PRMT5 inhibitor (MTA-cooperative)",
         AnchorKind.SYNTHETIC_LETHAL, Grade.STRONG, Axis.CYTOTOXIC, Layer.RECEPTOR, False, True,
         "Synthetic lethal; not division-gated; the clean ten-year anchor."),
    Tier("PTEN-deleted", "minority", "paxalisib",
         AnchorKind.DEPENDENCY, Grade.STRONG, Axis.PI3K_PARALLEL, Layer.RECEPTOR, True, True,
         "PTEN loss forces PI3K/AKT dependence; paxalisib is already in induction and is oral, "
         "brain-penetrant, a P-gp/BCRP non-substrate."),
    Tier("CDKN2A-deleted, RB1-intact", "minority", "abemaciclib (CDK4/6, brain-penetrant)",
         AnchorKind.DEPENDENCY, Grade.MEDIUM_STRONG, Axis.CELL_CYCLE, Layer.RECEPTOR, True, True,
         "p16 loss removes the CDK4/6 brake; abemaciclib is the one BBB-crossing CDK4/6i. GATED ON "
         "RB1 -- an RB1-deleted tumour drops to the floor."),
    Tier("PTPN11/SHP2 or KRAS driver", "~59% (56% SHP2 + 3% KRAS)",
         "mirdametinib (MEK, brain-penetrant)",
         AnchorKind.PATHWAY_DRIVER, Grade.MEDIUM, Axis.MAPK_SERIAL, Layer.MEK, False, True,
         "The MAPK majority. NOT a new finding -- the early four-cell analysis already showed MEK "
         "CLOSES the lung site (cobimetinib 0.973, no barrier) and FAILS in brain on access "
         "(trametinib ~0.021-0.1, a P-gp/BCRP substrate). So it is SITE-DEPENDENT: solid for a "
         "lung/disseminated second primary, conditional for a brain one on mirdametinib, whose "
         "canine brain access is UNQUANTIFIED."),
    Tier("none targetable / unknown", "residual", "immune surveillance + cycled microtubule",
         AnchorKind.AGNOSTIC, Grade.FLOOR, Axis.IMMUNE_EFFECTOR, Layer.RECEPTOR, False, True,
         "Genotype-independent backstop so no case is left with nothing. Weakest; depends on the "
         "tumour being immunogenic and on continued cycled dosing."),
)


def anchor_agent(tier: Tier, potency: float = 0.15, access: float = 0.50) -> Agent:
    """The maintenance agent for a tier, as a model Agent. Access 0.50 is the maintenance threshold
    established in `breed_wide_durability`; the floor tier is scored separately."""
    return Agent(tier.anchor_agent, tier.axis, tier.layer, potency, access, 1.0, True,
                 division_gated=tier.division_gated, note=tier.note)


def founding_escape(tier: Tier) -> Escape:
    """The lesion a fresh second primary of this genotype presents with: its founding driver, on the
    tier's own axis and height, and -- crucially -- DIVIDING. A newly emerged primary is a
    proliferating cell that has not yet seeded any reroute lesion or gone dormant, which is exactly
    why a maintenance agent matched to the driver catches it."""
    # On the serial MAPK axis the FOUNDING driver (SHP2/PTPN11, an adaptor) sits UPSTREAM of where
    # the anchor acts (MEK); a MEK block covers lesions above it, which is exactly why MEK maintenance
    # kills a fresh SHP2-driven primary. On non-serial axes the layer does not affect coverage.
    founding_layer = Layer.ADAPTOR if tier.axis is Axis.MAPK_SERIAL else tier.layer
    return Escape(f"founding {tier.genotype}", tier.axis, founding_layer, seeding_rate=1e-9,
                  requires_division=True, antigen_intact=True)


def suppresses_at_emergence(tier: Tier, potency: float = 0.15, access: float = 0.50,
                            growth: float = GROWTH_PER_DAY) -> bool:
    """Does the tier's maintenance agent kill a fresh second primary of that genotype?"""
    agent = anchor_agent(tier, potency, access)
    if tier.kind is AnchorKind.SYNTHETIC_LETHAL:
        # genotype-locked: it must hold across EVERY real escape, like breed_wide's maintenance,
        # because the deletion dependency persists through any reroute.
        d = DormancyModel()
        return all((d.margin(Regimen("m", [agent]), e, growth) if "persister" in e.name
                    else agent.effective_kill - growth) > 0 for e in ESCAPES)
    e = founding_escape(tier)
    return agent.reaches(e) and (agent.effective_kill - growth > 0)


def maintenance_tolerable(tier: Tier) -> bool:
    """A single agent held indefinitely. The floor tier is a strategy, not one PROFILES key."""
    if tier.anchor_agent not in tox.PROFILES:
        return True   # floor: immune + cycled microtubule, priced elsewhere; not a single agent
    return tox.tolerable([tox.PROFILES[tier.anchor_agent]])


def best_tier_for(genotype: set) -> Tier:
    """Pick the strongest anchor a tumour qualifies for. `genotype` is a set of markers, e.g.
    {'MTAP_del'}, {'SHP2'}, {'CDKN2A_del','RB1_intact'}, {'PTEN_del'}, or empty for the floor."""
    if "MTAP_del" in genotype:
        return TIERS[0]
    if "PTEN_del" in genotype:
        return TIERS[1]
    if "CDKN2A_del" in genotype and "RB1_intact" in genotype:
        return TIERS[2]
    if genotype & {"SHP2", "PTPN11", "KRAS"}:
        return TIERS[3]
    return TIERS[4]


# --- computed results ---------------------------------------------------------------------------------

#: tier genotype -> (suppresses at emergence?, maintenance tolerable?, grade)
def summary() -> dict:
    return {t.genotype: (suppresses_at_emergence(t), maintenance_tolerable(t), t.grade.name)
            for t in TIERS}


MAPK_MAINTENANCE_BY_SITE = {
    "lung / disseminated second primary": "SOLID. No blood-brain barrier; the early four-cell work "
        "closed the lung site at 0.973 with a MEK inhibitor (cobimetinib) at a conservative fraction "
        "of its canine Cmax. Plain trametinib/cobimetinib suffices -- CNS penetration is not needed.",
    "brain second primary": "CONDITIONAL. The early work found MEK FAILS in brain on access "
        "(trametinib ~0.021-0.1, a confirmed P-gp/BCRP substrate). Closing this branch needs a "
        "CNS-penetrant MEK inhibitor -- mirdametinib, notable CSF penetration in NHP, in paediatric "
        "brain-cancer trials -- but NO canine brain:plasma ratio is measured. The access 0.50 in the "
        "model is the maintenance THRESHOLD, not a mirdametinib figure; treat this branch as a "
        "hypothesis.",
}

EARLY_WORK_ALREADY_ESTABLISHED = (
    "THE MAPK ANSWER IS NOT A NEW DISCOVERY. `core.answer` (the oldest module) already listed MEK "
    "inhibitors as potency-ok / access-0.021 / FAILS-ON-ACCESS and ranked PTPN11/KRAS genotyping #2.",
    "`v2.four_cells` already split CNS vs lung and found MEK CLOSES lung (0.973) while brain fails on "
    "the barrier -- the exact site-dependence restated here.",
    "`trametinib_direct_evidence` already worked through the Takada HS model (PMID 30135215), the "
    "PTPN11 E76K / KRAS Q61H sensitivity, and the canine PK trial (~16 nM steady state).",
    "WHAT IS GENUINELY NEW is only (1) the MAINTENANCE-AT-EMERGENCE role and (2) mirdametinib as the "
    "CNS-penetrant candidate for the brain branch the early work left open. The rest is my own "
    "earlier finding re-used -- which is why this tier is graded MEDIUM and site-split, not a lock.",
)

EVERY_CASE_HAS_AN_ANCHOR = (
    "INDUCTION is genotype-agnostic and already closes all eleven escapes at both sites, so EVERY "
    "case clears the first tumour regardless of driver.",
    "MAINTENANCE is tiered by genotype, and every branch -- including the residual -- has an anchor, "
    "so no case is left with 'clear it and hope'. What varies is the GRADE of durability.",
    "The MAPK majority (~59%) is the case the MTAP answer ignored; its anchor is mirdametinib, a "
    "CNS-penetrant MEK inhibitor, and its durability is MEDIUM: it kills a second primary at "
    "emergence but not established rerouted disease, so it leans on surveillance.",
)

WHY_IT_IS_NOT_AS_CLEAN_AS_THE_MTAP_ARM = (
    "Only the MTAP tier is genotype-LOCKED (non-reroutable). The dependency tiers are strong but have "
    "defined resistance routes; the MAPK tier is reroutable once established and depends on catching "
    "the second primary early.",
    "So 'ten-plus years for all cases' is HONEST as: a clean lock for the deletion tiers, and a "
    "surveillance-dependent hold for the MAPK majority, with a genotype-agnostic floor beneath "
    "everyone. It is not one uniform guarantee, and claiming it were would repeat the exact "
    "over-reach this project keeps catching.",
)

THE_ONE_TEST = (
    "A small NGS panel on the same tumour tissue: MTAP/CDKN2A/PTEN copy number and PTPN11/KRAS/RB1 "
    "sequence. It assigns the tier. One test, run once, decides the maintenance arm for any dog.",
)
