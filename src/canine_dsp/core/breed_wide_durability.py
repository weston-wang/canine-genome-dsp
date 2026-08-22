"""Ten-year durability for this breed, across all its cases -- by targeting the lesion they share.

THE GOAL, RESTATED AS THE MODEL MUST MEET IT

    a durable response FOR THIS BREED, FOR ALL CASES, holding for TEN-PLUS YEARS,
    curative if possible

Three requirements, and the previous answer met none of them:

    FOR ALL CASES        `microtubule_route` treats one presentation -- primary CNS. The breed also
                         gets pulmonary and disseminated histiocytic sarcoma.
    TEN-PLUS YEARS       the model cleared one tumour and had NO TERM for another arising. The breed
                         predisposition is GERMLINE and survives cure, so a second primary is the
                         thing ten years actually has to survive.
    CURATIVE             clearance was 316 days continuous or two years cycled, and rested on a drug
                         whose human responses are PARTIAL rather than complete.

WHAT MAKES ALL THREE THE SAME PROBLEM

The most recurrent genomic aberration in canine histiocytic sarcoma is DELETION OF CDKN2A/B AND MTAP
at CFA11q16 -- found across 104 histiocytic malignancy cases, and evolutionarily conserved with the
human disease. The predisposing haplotype in affected breeds sits at that same MTAP-CDKN2A locus.

    IT IS THE SAME LESION IN THE BRAIN TUMOUR, IN THE LUNG TUMOUR, AND IN THE NEXT TUMOUR.

So a therapy aimed at the shared lesion is automatically breed-wide, automatically site-independent,
and -- because the germline background does not change -- automatically active against a second
primary. The three requirements collapse into one target.

AND THAT LESION HAS A SYNTHETIC-LETHAL PARTNER THAT IS BRAIN-PENETRANT AND IN THE CLINIC

MTAP deletion makes a cell dependent on PRMT5 in a way an MTAP-intact cell is not: losing MTAP raises
intracellular MTA, MTA partially inhibits PRMT5, and the cell is left with almost no reserve. An
MTA-COOPERATIVE PRMT5 inhibitor exploits exactly that -- it binds PRMT5 together with MTA, so it is
far more active where MTA is high, which is precisely and only in MTAP-deleted cells.

    TNG908    brain-penetrant by design, MTA-cooperative, phase I/II in MTAP-deleted solid tumours
              INCLUDING GLIOBLASTOMA (NCT05275478)
    TNG462    more potent, also brain-penetrant, clinical stage
              five MTA-cooperative PRMT5 inhibitors were clinical-stage as of 2025

WHY THIS IS DIFFERENT FROM EVERY AGENT THIS PROJECT HAS CONSIDERED

Every previous agent attacked a PATHWAY, and `catalogue.ESCAPES` is a list of ways to reroute around
a pathway. A synthetic-lethal agent attacks a GENOTYPE. The tumour cannot reroute around having
deleted MTAP -- restoring it would mean re-acquiring a homozygously deleted locus, which is not a
mutation, it is a reversal.

That is why it is not division-gated either: the dependency is on mRNA splicing and DNA-damage
handling, which a dormant cell still needs.

THE ARCHITECTURE

    INDUCTION     the microtubule regimen PLUS the PRMT5 inhibitor, until clearance
    MAINTENANCE   the PRMT5 inhibitor ALONE, indefinitely

    induction, worst margin      +0.111 to +0.186 depending on CNS access
    clearance                    112 to 187 days -- against 316 for the previous answer
    maintenance alone            suppresses at CNS access >= 0.50; DOES NOT at 0.30

Maintenance is what ten years is made of. It is not treating a tumour -- it is holding a genotype
under selection so that any clone arising from the same germline background is killed at emergence,
before it is a tumour at all.

TOXICITY IS THE PART THAT MAKES INDEFINITE DOSING PLAUSIBLE

    induction      headroom 0.20    marrow binds at 0.80
    MAINTENANCE    HEADROOM 0.65    marrow alone at 0.35

A conventional cytotoxic cannot be given for years. A drug that is only active in cells carrying a
deletion that normal tissue does not have is a different proposition -- and that selectivity is the
entire premise of the class rather than an assumption bolted on here.

WHAT WOULD FALSIFY THE WHOLE THING

If this dog's tumour is MTAP-INTACT, the maintenance arm does nothing and the ten-year claim
collapses to the previous answer. THAT IS A SINGLE STAIN ON TISSUE THAT MAY ALREADY BE IN A FREEZER.
It is the cheapest decisive test in this entire project.
"""

from __future__ import annotations

from dataclasses import dataclass

from . import microtubule_route as mt
from . import response_duration as rd
from . import toxicity as tox
from .catalogue import ESCAPES, GROWTH_PER_DAY, LEPTOMENINGEAL, PARENCHYMA
from .dormancy import DormancyModel
from .regimen import Agent, Axis, Layer, Regimen

PRMT5 = "PRMT5 inhibitor (MTA-cooperative)"
#: The microtubule agent must be named, not generic. See THE_AGENT_IDENTITY_MATTERS below.
LISAVANBULIN = "lisavanbulin (oral)"

#: CNS access for a brain-penetrant MTA-cooperative PRMT5 inhibitor. NOT measured; swept.
ACCESS_SWEEP = (0.30, 0.50, 0.80)
CONSERVATIVE_ACCESS = 0.30
#: Below this the maintenance arm cannot hold a new clone down on its own.
MAINTENANCE_ACCESS_THRESHOLD = 0.50

#: The presentations this breed actually gets. All carry the same recurrent lesion.
BREED_PRESENTATIONS = ("primary CNS", "pulmonary", "disseminated")


def prmt5_agent(access: float = CONSERVATIVE_ACCESS, potency: float = 0.15) -> Agent:
    """Synthetic lethal on GENOTYPE, so no pathway escape defeats it, and not division-gated."""
    return Agent(PRMT5, Axis.CYTOTOXIC, Layer.RECEPTOR, potency, access, 1.0, True,
                 division_gated=False,
                 note="MTA-cooperative PRMT5 inhibition is synthetic lethal with MTAP DELETION. The "
                      "tumour cannot reroute around a homozygous deletion -- escaping would require "
                      "re-acquiring the locus, which is a reversal rather than a mutation. Not "
                      "division-gated: the dependency is splicing and DNA-damage handling, which a "
                      "dormant cell still needs.")


def induction(compartment: str, access: float = CONSERVATIVE_ACCESS) -> Regimen:
    """Everything, until clearance.

    THE MICROTUBULE AGENT IS NAMED RATHER THAN GENERIC, AND THAT IS LOAD-BEARING. Built on
    `microtubule_route`'s placeholder agent -- whose profile carries sagopilone's peripheral-nerve
    0.85 plus a marrow 0.25 -- adding the PRMT5 inhibitor takes MARROW TO 1.05 AND THE REGIMEN IS
    NOT TOLERABLE. Built on lisavanbulin, whose dose-limiting axis is CNS rather than nerve or
    marrow, it fits with headroom 0.20.

    So the synthetic-lethal arm does not combine with the microtubule class in general. It combines
    with THIS MOLECULE, because of which organ axis this molecule happens to load.
    """
    others = [a for a in mt.build(compartment, duty=0.8, access=1.0).agents
              if a.name != mt.MICROTUBULE_AGENT]
    generic = next(a for a in mt.build(compartment, duty=0.8, access=1.0).agents
                   if a.name == mt.MICROTUBULE_AGENT)
    named = Agent(LISAVANBULIN, generic.axis, generic.layer, generic.potency, generic.access,
                  generic.duty, True, generic.division_gated, generic.antigen_directed,
                  note="Named explicitly so the toxicity lookup resolves to the CNS-limited profile "
                       "rather than the nerve-limited placeholder. The distinction decides whether "
                       "the PRMT5 arm fits at all.")
    return Regimen("induction", others + [named, prmt5_agent(access)])


def maintenance(access: float = CONSERVATIVE_ACCESS) -> Regimen:
    """The synthetic-lethal agent alone, indefinitely. This is what ten years is made of."""
    return Regimen("maintenance", [prmt5_agent(access)])


def _worst(regimen: Regimen, growth: float = GROWTH_PER_DAY) -> float:
    d = DormancyModel()
    return min(d.margin(regimen, e, growth) if "persister" in e.name
               else regimen.effective_kill_against(e) - growth for e in ESCAPES)


def induction_margin(compartment: str, access: float = CONSERVATIVE_ACCESS,
                     growth: float = GROWTH_PER_DAY) -> float:
    return _worst(induction(compartment, access), growth)


def days_to_clear(compartment: str, access: float = CONSERVATIVE_ACCESS) -> float:
    return rd.days_to_clear(induction_margin(compartment, access))


def maintenance_margin(access: float = CONSERVATIVE_ACCESS,
                       growth: float = GROWTH_PER_DAY) -> float:
    return _worst(maintenance(access), growth)


def suppresses_second_primary(access: float = CONSERVATIVE_ACCESS,
                              growth: float = GROWTH_PER_DAY) -> bool:
    """A new clone from the same germline background carries the same deletion, so the same agent
    that cleared the first tumour kills it at emergence."""
    return maintenance_margin(access, growth) > 0


def induction_profiles(compartment: str = PARENCHYMA) -> list:
    return [tox.PROFILES[a.name] for a in induction(compartment).agents]


def maintenance_profiles() -> list:
    return [tox.PROFILES[PRMT5]]


# --- computed results ---------------------------------------------------------------------------------

#: CNS access -> (parenchymal induction margin, days to clear, maintenance margin, suppresses?)
BY_ACCESS = {
    0.30: (0.1106, 187, -0.0100, False),
    0.50: (0.1406, 147, 0.0200, True),
    0.80: (0.1856, 112, 0.0650, True),
}

THE_SHARED_LESION = {
    "what": "Deletion of CDKN2A/B and MTAP at CFA11q16.",
    "how_common": "THE MOST RECURRENT genomic aberration in canine histiocytic sarcoma, across 104 "
        "histiocytic malignancy cases, and evolutionarily conserved with the human disease.",
    "germline_link": "The predisposing haplotype in affected breeds sits at the SAME MTAP-CDKN2A "
        "locus. In dogs of the predisposed breed specifically, 4 of 7 cases also carried TP53 variants.",
    "WHY_IT_UNIFIES_THE_GOAL": "It is the same lesion in the brain tumour, in the lung tumour, and in "
        "the NEXT tumour. A therapy aimed at it is automatically breed-wide, automatically "
        "site-independent, and automatically active against a second primary.",
}

WHY_SYNTHETIC_LETHALITY_IS_A_DIFFERENT_KIND_OF_TARGET = (
    "Every previous agent here attacked a PATHWAY, and `catalogue.ESCAPES` is a list of ways to "
    "reroute around a pathway.",
    "A SYNTHETIC-LETHAL AGENT ATTACKS A GENOTYPE. The tumour cannot reroute around having deleted "
    "MTAP -- escaping would require RE-ACQUIRING A HOMOZYGOUSLY DELETED LOCUS, which is a reversal "
    "rather than a mutation.",
    "It is also NOT DIVISION-GATED: the dependency is on mRNA splicing and DNA-damage handling, "
    "which a dormant cell still needs. So it reaches the persister directly rather than at re-entry.",
)

THE_ARCHITECTURE = {
    "induction": "the microtubule regimen PLUS the PRMT5 inhibitor, until clearance -- 112 to 187 "
        "days depending on CNS access, against 316 for the previous answer",
    "maintenance": "the PRMT5 inhibitor ALONE, indefinitely",
    "what_maintenance_actually_is": "NOT treating a tumour. Holding a GENOTYPE under selection, so "
        "that any clone arising from the same germline background is killed AT EMERGENCE, before it "
        "is a tumour at all.",
    "toxicity_induction": "headroom 0.20, marrow binding at 0.80",
    "toxicity_maintenance": "HEADROOM 0.65, marrow alone at 0.35",
    "why_indefinite_dosing_is_plausible": "A conventional cytotoxic cannot be given for years. A drug "
        "active only in cells carrying a deletion normal tissue does not have is a different "
        "proposition, and that selectivity is the premise of the class rather than an assumption "
        "added here.",
}

THE_AGENT_IDENTITY_MATTERS = {
    "the_finding": "The PRMT5 arm does NOT combine with the microtubule class in general. It "
        "combines with LISAVANBULIN specifically.",
    "why": "Marrow. Hydroxychloroquine 0.45 + PRMT5 0.35 = 0.80. Sagopilone's profile adds a marrow "
        "0.25 on top of its peripheral-nerve 0.85, taking marrow to 1.05 -- OVERSUBSCRIBED. "
        "Lisavanbulin's dose-limiting axis is CNS instead, so it adds nothing to marrow and the "
        "regimen fits at headroom 0.20.",
    "how_it_was_caught": "A test asserted the induction regimen was tolerable and it FAILED, because "
        "`induction` had been built on `microtubule_route`'s GENERIC placeholder agent rather than a "
        "named drug. The generic name resolved to the wrong toxicity profile.",
    "THE_LESSON": "An agent is not its mechanism. Two drugs of the same class, both brain-penetrant, "
        "both microtubule-directed, differ on the axis that decides whether a fourth drug can be "
        "added at all.",
}

WHAT_WOULD_FALSIFY_IT = (
    "IF THIS TUMOUR IS MTAP-INTACT, the maintenance arm does nothing and the ten-year claim collapses "
    "to the previous answer.",
    "THAT IS A SINGLE STAIN ON TISSUE THAT MAY ALREADY BE IN A FREEZER -- MTAP immunohistochemistry "
    "is a routine surrogate for the deletion. It is the cheapest decisive test in this project.",
    "The CNS access figure is the other hinge: at 0.30 the maintenance arm does NOT hold, and it has "
    "never been measured for these compounds in a dog.",
)

WHAT_IS_STILL_ASSUMED = (
    "THAT CANINE HS CARRIES MTAP DELETION AT THE RATE THE COPY-NUMBER LITERATURE REPORTS, and that "
    "this individual's tumour is among them. Recurrent is not universal.",
    "THE POTENCY, 0.15/day, as everywhere else. Synthetic lethality says a cell DIES; it does not say "
    "how fast.",
    "THE CNS ACCESS. TNG908 and TNG462 are designed brain-penetrant and studied in glioblastoma, but "
    "no figure for a dog exists. The sweep spans the value that decides the maintenance arm.",
    "THAT MTA-COOPERATIVE SELECTIVITY HOLDS IN VIVO WELL ENOUGH FOR INDEFINITE DOSING. The whole "
    "maintenance argument rests on normal tissue being spared, and the toxicity budget of 0.35 is an "
    "ordinal judgement with NO CANINE DATA behind it.",
    "THAT A SECOND PRIMARY ARISES FROM THE SAME LESION. The germline haplotype is shared, but a new "
    "tumour could in principle be driven by one of the secondary loci (CFA 2, 5, 12, 14, 20, 26, X) "
    "without the MTAP deletion -- in which case maintenance would not see it.",
)
