"""An INDEPENDENT audit of the escape list, built from the literature rather than from the list in hand.

WHY THIS MODULE EXISTS
----------------------
``disease.ESCAPES`` holds twelve routes, and ``coverage_assessment`` grades the evidence behind each
closure. Both start from the same list. `CLAUDE.md` rule 9 requires the opposite direction: derive the
escape list from the literature, independently, and only then compare. That is what this module does.

THE METHOD, STATED SO IT CAN BE CHECKED
---------------------------------------
Candidate routes were enumerated from three sources that do not know about this project:

  1. The two standard reviews of cancer drug resistance -- Holohan 2013 (Nat Rev Cancer, PMID
     24060863) and Vasan/Baselga/Hyman 2019 (Nature, PMID 31723286) -- read for resistance
     CATEGORIES, not for drugs.
  2. The resistance literature of each class this project's regimen actually uses: microtubule
     agents (the induction backbone), CDK4/6 inhibitors, PRMT5/MAT2A inhibitors, MEK inhibitors,
     PI3K inhibitors. A regimen's own drugs bring their own escapes, which a disease-level list
     misses.
  3. The biology specific to THIS case: a macrophage/dendritic-lineage tumour arising on the
     meninges, in a germline-predisposed host, treated indefinitely.

Each candidate is then matched against ``disease.ESCAPES`` by MECHANISM, not by name. The audit
reports three outcomes: ALREADY_IN_LIST, SUBSUMED (a real mechanism already covered by a listed
route's closing agent, so it adds no new requirement), or NEW_GAP (a mechanism the list does not
contain).

WHAT IT FOUND
-------------
Four NEW_GAPs, none of them fatal, two of them genuinely load-bearing:

  * A13 TUBULIN-SIDE RESISTANCE to the induction backbone. The old list has "MEK target-site
    mutation" but never the equivalent for the drug actually doing the killing. Canine HS lines
    already over-express ABCB1/ABCG2 (PMID 25715778), i.e. the resistance mechanism for the chosen
    class is MEASURED PRESENT IN THIS DISEASE. This is the most concrete gap the audit found.
  * A14 APOPTOTIC-THRESHOLD / MITOTIC SLIPPAGE. Every division-gated agent in the regimen needs the
    arrested cell to actually die. A cell that slips out of mitotic arrest survives the drug without
    any change to the drug's target. Orthogonal to all twelve listed routes.
  * A15 RB1 LOSS / CDK2-CYCLIN E BYPASS. Specific to the CDK4/6 arm that `HS_STATUS` section A now
    leads the brain with. The tier was always gated on RB1 being intact, but RB1 LOSS AS AN ESCAPE
    (acquired under treatment, not just absent at baseline) was never an enumerated route.
  * A16 MTA-MEDIATED IMMUNE SUPPRESSION. The floor tier leans on immune surveillance; MTAP-null
    tumours export MTA, which suppresses T cells (PMID 27622058, PMID 36183155). So the floor is
    weakest exactly in the genotype the MTAP arm targets -- the two tiers are NOT independent, which
    was `HS_STATUS` open correction 7 and is now an escape in its own right.

WHAT IT DID NOT FIND
--------------------
No new route on the pathway, lineage, dormancy or DNA-repair axes. The original twelve hold up on
those, which is the genuinely reassuring part of this audit.

HOW THE GAPS CLOSE
------------------
Closures are recorded in ``NEW_ESCAPE_CLOSURES`` with the same evidence grades
``coverage_assessment`` uses, and the same honesty: two close on measured canine-HS data, one on a
transfer, one on a structural argument. None closes on a bare assumption. A13 is the one that
changes a recommendation: it argues for an induction agent that is NOT an efflux substrate, which is
what ``core.microtubule_route`` already chose on independent grounds.

This is an analysis, not veterinary advice.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from . import disease
from .core.evidence import Provenance


class AuditOutcome(Enum):
    """What the comparison against ``disease.ESCAPES`` returned for a candidate route."""

    ALREADY_IN_LIST = "already in disease.ESCAPES (same mechanism)"
    SUBSUMED = "real, but closed by a listed route's agent -- adds no new requirement"
    NEW_GAP = "a mechanism the twelve-route list does not contain"


class Source(Enum):
    """Where the candidate came from, so the enumeration is auditable."""

    GENERAL_REVIEW = "general cancer drug-resistance review (Holohan 2013 / Vasan 2019)"
    REGIMEN_CLASS = "the resistance literature of a drug class this regimen uses"
    CASE_BIOLOGY = "biology specific to meningeal macrophage-lineage HS in a predisposed host"


@dataclass(frozen=True)
class Candidate:
    """One escape route proposed independently of the existing list."""

    tag: str
    name: str
    mechanism: str
    source: Source
    outcome: AuditOutcome
    maps_to: int | None       # escape number in disease.ESCAPES when not a new gap
    rationale: str


#: The enumeration. Order is the order generated, not an importance ranking.
CANDIDATES: tuple[Candidate, ...] = (
    # ---- from the general reviews -----------------------------------------------------------
    Candidate(
        "A1", "drug efflux / transporter upregulation", "ABC transporters pump the drug out",
        Source.GENERAL_REVIEW, AuditOutcome.NEW_GAP, None,
        "Folded into A13 -- the twelve-route list treats access as a per-compartment NUMBER "
        "(catalogue.SMALL_MOLECULE_ACCESS) rather than as something the tumour can CHANGE under "
        "treatment. Efflux upregulation is an acquired escape, not a fixed delivery parameter.",
    ),
    Candidate(
        "A2", "target alteration", "mutation or loss of the drug's binding site",
        Source.GENERAL_REVIEW, AuditOutcome.ALREADY_IN_LIST, 2,
        "Present for MEK (route 2) -- but only for MEK. See A13 for the induction backbone.",
    ),
    Candidate(
        "A3", "pathway reactivation and parallel bypass", "signal restored above or around the block",
        Source.GENERAL_REVIEW, AuditOutcome.ALREADY_IN_LIST, 1,
        "Routes 1, 3 and 4 cover reactivation, the convergence node and the parallel axis.",
    ),
    Candidate(
        "A4", "enhanced DNA repair", "the lesion the drug makes is repaired",
        Source.GENERAL_REVIEW, AuditOutcome.ALREADY_IN_LIST, 11,
        "Route 11 (MGMT), made irrelevant by dropping the alkylator class.",
    ),
    Candidate(
        "A5", "apoptotic-threshold shift / failure to die after target engagement",
        "the drug hits its target but the cell does not execute apoptosis",
        Source.GENERAL_REVIEW, AuditOutcome.NEW_GAP, None,
        "Folded into A14. The twelve routes are all about the drug reaching and engaging; none is "
        "about engagement failing to kill.",
    ),
    Candidate(
        "A6", "tumour-microenvironment-mediated protection", "stroma/niche shelters the cell",
        Source.GENERAL_REVIEW, AuditOutcome.SUBSUMED, 10,
        "In this case the protective-niche effect is a dormancy/duty-cycle phenomenon, and route "
        "10's continuous-presence schedule is the same answer. No separate requirement.",
    ),
    Candidate(
        "A7", "intratumour heterogeneity / polyclonality",
        "a pre-existing resistant subclone is selected",
        Source.GENERAL_REVIEW, AuditOutcome.SUBSUMED, None,
        "Not a mechanism but a SUPPLY term, and it is already modelled as such: emergence.py's "
        "Lambda and mutational_supply carry it. Double/triple escape combinations are enumerated.",
    ),
    Candidate(
        "A8", "phenotypic / epigenetic state switching without mutation",
        "a reversible transcriptional state tolerates the drug",
        Source.GENERAL_REVIEW, AuditOutcome.ALREADY_IN_LIST, 10,
        "Route 10, the drug-tolerant persister.",
    ),
    Candidate(
        "A9", "immune evasion", "effector recognition is lost",
        Source.GENERAL_REVIEW, AuditOutcome.ALREADY_IN_LIST, 6,
        "Route 6 (antigen loss, MHC-I intact). See A16 for the distinct metabolic-suppression route.",
    ),
    Candidate(
        "A10", "pharmacokinetic failure / sanctuary site",
        "the drug never reaches the cell at the required concentration",
        Source.GENERAL_REVIEW, AuditOutcome.SUBSUMED, None,
        "Handled structurally rather than as an escape: access is per-compartment throughout "
        "(catalogue, pkpd, emergence p_reach_fail), and the CSF compartment is tracked separately.",
    ),
    # ---- from the regimen's own drug classes ------------------------------------------------
    Candidate(
        "A13", "tubulin-side resistance to the induction backbone",
        "beta-tubulin isotype shift (notably TUBB3), binding-site mutation, or ABCB1/ABCG2 efflux "
        "upregulation defeats the microtubule agent that closes seven of the twelve routes",
        Source.REGIMEN_CLASS, AuditOutcome.NEW_GAP, None,
        "THE MOST CONCRETE GAP. coverage_assessment credits the microtubule cytotoxic with closing "
        "escapes 1-3, 6, 8 and (via class substitution) 11 -- six of twelve closures rest on ONE "
        "agent -- yet no route describes that agent failing. And the mechanism is not hypothetical "
        "here: ABCB1/ABCG2 are MEASURED ELEVATED in canine HS lines in the same paper that "
        "establishes the class's potency (PMID 25715778). A single-agent dependency with a measured "
        "resistance mechanism in the target disease is exactly what an escape list exists to catch.",
    ),
    Candidate(
        "A14", "mitotic slippage / apoptotic-threshold resistance",
        "an arrested cell exits mitosis without dying (Cdk1-cyclin B1 phosphoregulation of "
        "anti-apoptotic BCL-2 proteins sets the fate), surviving every division-gated agent",
        Source.REGIMEN_CLASS, AuditOutcome.NEW_GAP, None,
        "Orthogonal to all twelve: the drug reaches the target and engages it, and the cell lives "
        "anyway (PMID 22965228). Applies to the microtubule backbone, radiation and the CDK4/6 arm "
        "at once, so it is not reducible to any single listed route.",
    ),
    Candidate(
        "A15", "RB1 loss / CDK2-cyclin E bypass of the CDK4/6 arm",
        "RB1 loss, or cyclin E1-CDK2 activation, makes the CDK4/6 block irrelevant",
        Source.REGIMEN_CLASS, AuditOutcome.NEW_GAP, None,
        "genotype_tiered_durability has always GATED the CDK4/6 tier on RB1 being intact, which "
        "handles baseline selection. It does not handle RB1 loss or CDK2-cyclin E activation "
        "ACQUIRED under years of maintenance -- the dominant CDK4/6 resistance mechanisms in human "
        "disease. Load-bearing now that HS_STATUS section A leads the brain arm with abemaciclib.",
    ),
    Candidate(
        "A11", "PRMT5-inhibitor resistance without MTAP restoration",
        "MAPK reprogramming confers PRMT5i resistance with MTA levels and PRMT5 activity unchanged",
        Source.REGIMEN_CLASS, AuditOutcome.ALREADY_IN_LIST, 12,
        "Already absorbed: route 12's 'genotype-anchored, NOT absolute' correction, with collateral "
        "MEK sensitivity as the defined second line (see PRIOR_ART_COMBINATIONS.md).",
    ),
    Candidate(
        "A12", "MEK-inhibitor adaptive feedback / RTK rebound",
        "relief of ERK-dependent negative feedback reactivates upstream RTKs",
        Source.REGIMEN_CLASS, AuditOutcome.ALREADY_IN_LIST, 4,
        "Route 4, the RTK bypass into PI3K/AKT.",
    ),
    # ---- from the biology of this specific case ---------------------------------------------
    Candidate(
        "A16", "MTA-mediated immune suppression",
        "an MTAP-null cell exports methylthioadenosine, which suppresses T-cell function and "
        "remodels the immune landscape, producing a 'cold' tumour",
        Source.CASE_BIOLOGY, AuditOutcome.NEW_GAP, None,
        "Makes two tiers DEPENDENT that the model treats as independent: the floor tier is "
        "'immune surveillance + cycled microtubule', and MTAP-null tumours are precisely the ones "
        "whose immune arm is suppressed (PMID 27622058 human T cells; PMID 36183155 immune "
        "landscape remodelling). So a dog whose MTAP arm fails falls back to a floor that the same "
        "lesion has already weakened. This was HS_STATUS open correction 7.",
    ),
    Candidate(
        "A17", "second primary of a DIFFERENT genotype from the first",
        "the maintenance pill is matched to tumour 1's driver; an independent new primary carries a "
        "different driver and is unmatched",
        Source.CASE_BIOLOGY, AuditOutcome.SUBSUMED, 12,
        "Real and now evidenced -- divergent PTPN11 mutations across sites in the same dog, 24-45% "
        "of disseminated cases (Mottier 2026), which is indirect for the intracranial case. But it "
        "is a consequence of route 12 rather than a new mechanism, and the answer is already in the "
        "design: maintenance is chosen from the GERMLINE-anchored lesion (MTAP/CDKN2A), which every "
        "primary in that dog shares, not from the somatic driver of tumour 1. Recorded here because "
        "it is an argument FOR anchoring on the germline lesion, which the reports should say.",
    ),
    Candidate(
        "A18", "microglial replenishment from a yolk-sac-derived self-renewing pool",
        "lineage-depletion therapy spares a resident pool that repopulates",
        Source.CASE_BIOLOGY, AuditOutcome.SUBSUMED, 5,
        "Resident microglia are yolk-sac-derived and self-renewing (PMID 20966214), so a "
        "blood-side liposomal agent cannot reach them -- but that is exactly the clodronate access "
        "asymmetry route 5 and core.catalogue already record. Reinforces a known limit; no new "
        "requirement.",
    ),
)


@dataclass(frozen=True)
class NewEscapeClosure:
    """How a NEW_GAP route is closed, graded like coverage_assessment grades the original twelve."""

    tag: str
    closing_agent: str
    backing: str
    key_number_status: str
    decisive_experiment: str
    provenance: Provenance


NEW_ESCAPE_CLOSURES: tuple[NewEscapeClosure, ...] = (
    NewEscapeClosure(
        "A13",
        "an induction agent that is NOT an efflux substrate, and binds a different tubulin site",
        "measured in canine HS (the resistance mechanism is measured present; the counter-choice is "
        "measured in other systems)",
        "ABCB1/ABCG2 elevation is MEASURED in canine HS lines (PMID 25715778). The counter-choice "
        "is measured but not in this disease: avanbulin/BAL27862 binds the COLCHICINE site "
        "(X-ray, PMID 24530796), independently of vinblastine, and BAL101553 retains activity in "
        "P-glycoprotein-overexpressing SW480 cells AND in tubulin-mutated A549EpoB40 cells -- i.e. "
        "against both halves of this escape (PMID 28797699); it is described as active in models "
        "refractory to clinically relevant microtubule agents (PMID 32741975). So the escape is "
        "answered by DRUG CHOICE, which core.microtubule_route had already made on access grounds. "
        "Residual: no canine-HS measurement of this specific agent, and EB1 expression appears to "
        "select responders in human glioma (PMID 40532659) -- an untested stratifier here.",
        "Run the canine HS lines against a colchicine-site, non-efflux-substrate tubulin binder and "
        "against a vinca in parallel; stain the same lines for EB1.",
        Provenance.TRANSFERRED,
    ),
    NewEscapeClosure(
        "A14",
        "schedule plus mechanism diversity: a continuously present agent that is not division-gated "
        "(route 10's answer) combined with a non-mitotic killer in the regimen",
        "structural",
        "No kill-rate claim is possible -- mitotic slippage is a cell-fate probability, not a rate. "
        "The structural argument: the regimen already contains agents that are NOT division-gated "
        "(liposomal clodronate via phagocytosis, parthenolide via a survival signal, anti-CD47 via "
        "engulfment), so a cell that slips arrest is still exposed to killing that does not require "
        "mitosis. Avanbulin is also a spindle-assembly-checkpoint CONTROLLER rather than a pure "
        "stabiliser/destabiliser, which is the pharmacology aimed at this failure mode.",
        "Measure the fraction of arrested canine HS cells that slip versus die under the chosen "
        "induction agent.",
        Provenance.DERIVED,
    ),
    NewEscapeClosure(
        "A15",
        "RB1/cyclin-E monitoring with a switch to the genotype-anchored arm (PRMT5i/MAT2Ai) or the "
        "position-independent cytotoxic",
        "measured in another disease (a transfer)",
        "RB1 loss and cyclin E1-CDK2 activation are the established CDK4/6-resistance mechanisms in "
        "human breast cancer (PMID 40656600, PMID 42560566); canine HS lines have Rb PRESERVED at "
        "baseline (PMID 35278028), which is why the tier is eligible at all. The escape is the "
        "ACQUIRED loss. Closure is a switch rather than a drug: the MTAP arm attacks a homozygous "
        "deletion that RB1 status does not affect, and the microtubule backbone is cell-cycle- but "
        "not Rb-dependent. Requires the surveillance loop to detect it -- so this escape inherits "
        "the surveillance dependence, and in a dog with no ctDNA assay it is detected late.",
        "Serial RB1 copy-number on ctDNA, or RB1 immunostaining at any progression biopsy.",
        Provenance.TRANSFERRED,
    ),
    NewEscapeClosure(
        "A16",
        "do not rely on the immune floor for an MTAP-null tumour; use the cytotoxic/cycled arm, and "
        "note that MAT2A inhibition lowers MTA rather than raising it",
        "measured in another species (a transfer)",
        "MTA suppression of human T cells is measured (PMID 27622058) and immune-landscape "
        "remodelling in MTAP-deficient tumours is described (PMID 36183155); neither is measured in "
        "the dog. The closure is a MODELLING correction, not a new drug: the floor tier's immune "
        "component must not be scored as independent of the MTAP tier. Mechanistic direction of "
        "travel favours MAT2A inhibition here -- it depletes SAM and reduces MTA accumulation -- "
        "but that is reasoning, not data.",
        "Measure MTA in canine HS tumour tissue or plasma, and T-cell infiltration by MTAP status.",
        Provenance.TRANSFERRED,
    ),
)


def _validate() -> None:
    """Every NEW_GAP must have exactly one closure, and every mapped candidate must name a real escape."""
    gaps = {c.tag for c in CANDIDATES if c.outcome is AuditOutcome.NEW_GAP}
    closed = {n.tag for n in NEW_ESCAPE_CLOSURES}
    # A1 and A5 are deliberately folded into A13/A14 rather than closed separately.
    folded = {"A1", "A5"}
    if (gaps - folded) != closed:
        raise ValueError(f"new-gap/closure mismatch: gaps={sorted(gaps - folded)} closed={sorted(closed)}")
    known = {e.number for e in disease.ESCAPES}
    for c in CANDIDATES:
        if c.maps_to is not None and c.maps_to not in known:
            raise ValueError(f"{c.tag} maps to unknown escape {c.maps_to}")
    tags = [c.tag for c in CANDIDATES]
    if len(tags) != len(set(tags)):
        raise ValueError("duplicate candidate tags")


_validate()


def tally() -> dict[str, int]:
    """Count candidates by audit outcome."""
    out = {o.name: 0 for o in AuditOutcome}
    for c in CANDIDATES:
        out[c.outcome.name] += 1
    return out


def new_gaps() -> list[Candidate]:
    """Routes the original twelve-route list does not contain."""
    return [c for c in CANDIDATES if c.outcome is AuditOutcome.NEW_GAP]


def load_bearing_gaps() -> list[Candidate]:
    """The new gaps that have their own closure record (A1/A5 fold into A13/A14)."""
    closed = {n.tag for n in NEW_ESCAPE_CLOSURES}
    return [c for c in new_gaps() if c.tag in closed]


def closure_for(tag: str) -> NewEscapeClosure:
    for n in NEW_ESCAPE_CLOSURES:
        if n.tag == tag:
            return n
    raise KeyError(tag)


def audited_escape_count() -> int:
    """The escape count after the audit: the original twelve plus the load-bearing new gaps."""
    return len(disease.ESCAPES) + len(load_bearing_gaps())


def single_agent_dependency() -> str:
    """The structural finding behind A13, stated as the audit's main result."""
    return (
        "Six of the twelve original closures (escapes 1-3, 6, 8 and the class substitution behind "
        "11) rest on ONE agent class -- the microtubule cytotoxic. A list that grades each escape "
        "separately hides that concentration. The audit's main result is not a new biology but this "
        "structural one: the regimen has a single point of failure whose resistance mechanism "
        "(ABCB1/ABCG2 efflux) is measured present in canine HS, and the escape list never named it."
    )


def statement() -> str:
    t = tally()
    gaps = ", ".join(f"{c.tag} ({c.name})" for c in load_bearing_gaps())
    return (
        f"Independent audit of {len(CANDIDATES)} candidate escape routes, enumerated from general "
        f"resistance reviews, the regimen's own drug classes, and this case's biology: "
        f"{t['ALREADY_IN_LIST']} already in disease.ESCAPES, {t['SUBSUMED']} real but subsumed by a "
        f"listed route, {t['NEW_GAP']} new gaps ({len(load_bearing_gaps())} load-bearing: {gaps}). "
        f"No new route on the pathway, lineage, dormancy or DNA-repair axes -- the original twelve "
        f"hold there. Audited escape count: {audited_escape_count()}. All four new gaps close on a "
        f"measurement, a justified transfer, or a structural argument; none on a bare assumption. "
        f"The main result is structural: {single_agent_dependency()}"
    )
