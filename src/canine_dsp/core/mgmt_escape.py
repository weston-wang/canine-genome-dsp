"""[SUPERSEDED CONCLUSION — AUDIT BANNER] The carboplatin lesion-swap proposed at the end of this
module is FALSIFIED by core.hs_drug_sensitivity: melphalan, an N7 crosslinker like carboplatin, is
resisted 42-411x in measured canine histiocytic sarcoma, so the resistance is alkylator-CLASS-wide,
not MGMT-shaped, and swapping within the class does not escape it. The MGMT MECHANISM described here
(a non-DNA-damaging drug has no O6 substrate) remains valid and is reused by the live answer. Live
answer: core.breed_wide_durability.

The eleventh escape, and it is aimed at the one drug the answer rests on.

WHY THIS WAS MISSED, AND WHY THAT MATTERS

The ten escapes in `catalogue.ESCAPES` are all SIGNALLING escapes -- pathway reroutes, lineage
independence, immune evasion, dormancy. Temozolomide closes nine of them by being INDIFFERENT to
signalling: a DNA-damaging agent does not care which wire the cell has rerouted.

That indifference is exactly why the model could not see this one. MGMT is not a signalling escape.
It is a REPAIR ENZYME THAT REMOVES THE SPECIFIC CHEMICAL GROUP TEMOZOLOMIDE ADDS. Being indifferent
to signalling is no defence against it.

The project's own codebase already knew about MGMT -- `cns_vaccine_trial_evidence` carefully
stratifies a human trial by MGMT status. IT WAS USED AS A CONTROL VARIABLE FOR SOMEONE ELSE'S DATA
AND NEVER TURNED ON THIS ANALYSIS'S OWN ANSWER.

WHAT MGMT IS

A suicide enzyme. It transfers the alkyl group from the O6 position of guanine onto a cysteine in
its own active site, which INACTIVATES AND CONSUMES the enzyme. One molecule per lesion. Recovery
requires new protein synthesis.

That chemistry decides which drugs it defeats, and the answer is not "chemotherapy":

    DEFEATED -- the lesion is O6-alkylguanine, which is MGMT's substrate
        temozolomide          O6-methylguanine
        lomustine (CCNU)      O6-chloroethylguanine
        carmustine (BCNU)     O6-chloroethylguanine

    NOT DEFEATED -- a different lesion entirely, not MGMT's substrate
        carboplatin/cisplatin N7-guanine intrastrand crosslinks
        radiation             strand breaks
        everything non-cytotoxic in this regimen

LOMUSTINE IS ON THE DEFEATED LIST, AND LOMUSTINE IS THE STANDARD OF CARE FOR CANINE HISTIOCYTIC
SARCOMA. So an MGMT-competent tumour is not merely resistant to the regimen proposed here; it is
resistant to what it would be given anyway.

WHAT IS MEASURED, AND IN WHICH SPECIES

The canine number is real and it is the right drug class:

    PMID 26130852. Five canine lymphoma lines. TWO OF FIVE (CL-1, Nody-1) had MGMT activity by
    fluorometric assay and high MGMT mRNA. Lomustine IC50:

        CL-1     >50 uM  ->  11.5 uM with O6-benzylguanine   >=4.3x
        Nody-1   36.5 uM ->   7.5 uM with O6-benzylguanine     4.9x
        sensitive lines   14.0-23.5 uM baseline

    So in canine tumour cells MGMT confers roughly a 4-5x loss of alkylator potency, AND AN MGMT
    INHIBITOR REVERSES IT.

WHETHER THIS TUMOUR HAS IT IS UNKNOWN, AND THE TWO ADJACENT ANSWERS DISAGREE

    canine glioma            FAVOURABLE   PMID 34477324. Three canine glioma lines, MGMT promoter
                                          highly methylated in all three, MGMT protein UNDETECTABLE
                                          in all three. Silenced -- temozolomide works.
    human soft tissue        UNFAVOURABLE PMID 23110891. 75 sarcomas. Silencing (methylation AND
    sarcoma                               negative IHC) in only 6/75 = 8%. Authors conclude the rate
                                          is "too low to use as a selection criterion".

WHICH REFERENCE CLASS APPLIES DECIDES THE ANSWER, AND THIS MODULE REFUSES TO PICK ONE. Histiocytic
sarcoma is neither a glioma nor any of the six subtypes in that sarcoma series (liposarcoma,
MFH/NOS, leiomyosarcoma, myxofibrosarcoma, MPNST, synovial sarcoma). Transferring either figure is
the exact error `evidence.Measurement` exists to block. What CAN be said is that the favourable
reading rests on a different lineage, and the unfavourable reading rests on a different species.

THE TWO OBVIOUS RESCUES, AND ONE OF THEM IS ALREADY IN THE REGIMEN

  1. DOSE-DENSE / CONTINUOUS TEMOZOLOMIDE. MGMT is stoichiometric, so dosing faster than it can be
     resynthesised should deplete it. This regimen ALREADY doses temozolomide continuously at duty
     1.0, so the rescue is free if it works.

     IT DOES NOT WORK, and the evidence against it is as good as evidence gets. RTOG 0525, randomised
     phase III, newly diagnosed glioblastoma, MGMT status a STRATIFICATION FACTOR: dose-dense did not
     improve overall survival (16.6 vs 14.9 months, p=0.63), did not improve PFS, AND SHOWED NO
     BENEFIT BY METHYLATION STATUS -- which is precisely the subgroup the depletion argument
     predicts should benefit. It also cost more toxicity (grade >=3, 27% vs 19%, p=0.008).

     THE FREE RESCUE IS FALSIFIED. Recording it as available would have been the single most
     convenient error in this file.

  2. O6-BENZYLGUANINE. Direct MGMT inactivator. It WORKS pharmacologically -- it is the agent that
     restored lomustine sensitivity in PMID 26130852 above. But it makes the marrow toxicity of its
     partner drug dramatically worse: with carmustine it forced the MTD from 200 down to 40 mg/m2,
     an 80% dose reduction that is itself blamed for the phase II failure. With temozolomide, phase
     II saw grade 4 haematologic events in 48% of patients (grade 4 neutropenia 47%).

     THIS REGIMEN'S MARROW AXIS IS ALREADY AT EXACTLY 1.00 WITH ZERO HEADROOM. O6-benzylguanine is
     the worst possible thing to add to it.

WHAT ACTUALLY CLOSES IT: CHANGE THE LESION, NOT THE DOSE

Carboplatin's principal lesion is an N7-guanine intrastrand crosslink. MGMT does not reverse it,
because it is not MGMT's substrate. And it does not need a new delivery route -- INTRA-ARTERIAL
CARBOPLATIN WITH OSMOTIC BARRIER DISRUPTION IS NEUWELT'S OWN PROTOCOL, the same route this analysis
already costed, and it has been run specifically in TEMOZOLOMIDE-REFRACTORY patients (PMID 20023537,
13 patients, TMZ-refractory anaplastic oligodendroglioma/oligoastrocytoma; carboplatin 200 mg/m2/day
intra-arterially). Carboplatin is also thoroughly established in dogs.

The honest caveat: "MGMT-independent" is a statement about DIRECT REVERSAL. MGMT has been reported
to modulate cisplatin response indirectly via homologous recombination, and platinums have been
reported to downregulate MGMT. This module claims only that MGMT DOES NOT REPAIR THE PLATINUM LESION
-- not that platinum is untouched by anything MGMT-adjacent.

WHAT THE SUBSTITUTION COSTS: NOTHING ON THE TOXICITY AXIS, BECAUSE IT IS A SWAP

Carboplatin's dose-limiting toxicity is myelosuppression -- the same axis temozolomide loads. Because
carboplatin REPLACES temozolomide rather than joining it, the axis does not double up.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .catalogue import ESCAPES, GROWTH_PER_DAY, LEPTOMENINGEAL, PARENCHYMA
from .dormancy import DormancyModel
from .regimen import Agent, Axis, Layer, Regimen


class Lesion(Enum):
    """The DNA damage an agent leaves. THIS is what decides whether MGMT defeats it."""

    O6_ALKYLGUANINE = "O6-alkylguanine -- MGMT's substrate, directly reversed"
    N7_PLATINUM_CROSSLINK = "N7-guanine intrastrand crosslink -- not MGMT's substrate"
    STRAND_BREAK = "strand breaks -- not MGMT's substrate"
    NONE = "not a DNA-damaging agent"


#: agent name fragment -> lesion. Only DNA-damaging agents appear.
LESION_BY_AGENT = {
    "temozolomide": Lesion.O6_ALKYLGUANINE,
    "lomustine": Lesion.O6_ALKYLGUANINE,
    "carmustine": Lesion.O6_ALKYLGUANINE,
    "carboplatin": Lesion.N7_PLATINUM_CROSSLINK,
    "cisplatin": Lesion.N7_PLATINUM_CROSSLINK,
    "radiation": Lesion.STRAND_BREAK,
}


def lesion_of(agent_name: str) -> Lesion:
    low = agent_name.lower()
    for key, lesion in LESION_BY_AGENT.items():
        if key in low:
            return lesion
    return Lesion.NONE


def defeated_by_mgmt(agent_name: str) -> bool:
    """MGMT reverses O6-alkylguanine and nothing else. Being 'chemo' is not the criterion."""
    return lesion_of(agent_name) is Lesion.O6_ALKYLGUANINE


# --- the measured effect size -----------------------------------------------------------------------

CANINE_MGMT_LOMUSTINE = {
    "citation": "PMID 26130852. SPECIES: DOG. Canine lymphoma lines; lomustine, a nitrosourea.",
    "lines_tested": 5,
    "lines_with_mgmt_activity": 2,
    "CL_1_ic50_uM": (">50", 11.5),      # (no inhibitor, with O6-benzylguanine)
    "Nody_1_ic50_uM": (36.5, 7.5),
    "sensitive_line_ic50_range_uM": (14.0, 23.5),
    "fold_resistance_conservative": 36.5 / 7.5,   # 4.87 -- from the line with a bounded numerator
    "why_it_is_the_right_number_here": "CANINE cells, and a drug whose lesion is O6-chloroethyl"
        "guanine -- the same MGMT substrate temozolomide produces. Species and chemistry both match.",
    "what_it_does_not_establish": "It is LYMPHOMA, not histiocytic sarcoma. The FRACTION of tumours "
        "carrying MGMT activity does not transfer; the EFFECT SIZE GIVEN ACTIVITY is what is used.",
}

#: Conservative: use the lower of the two measured fold-changes.
FOLD_RESISTANCE = 4.3


# --- whether this tumour has it: unresolved, and the neighbours disagree -----------------------------

REFERENCE_CLASSES_DISAGREE = {
    "canine glioma -- FAVOURABLE": {
        "citation": "PMID 34477324",
        "finding": "Three canine glioma lines. MGMT promoter highly methylated in all three; MGMT "
                   "protein UNDETECTABLE in all three. Temozolomide additive with radiation.",
        "why_it_may_not_transfer": "GLIAL lineage. Histiocytic sarcoma is a macrophage/dendritic "
                                   "lineage tumour. Right species, wrong cell.",
    },
    "human soft tissue sarcoma -- UNFAVOURABLE": {
        "citation": "PMID 23110891",
        "finding": "75 sarcomas. Silencing (promoter methylation AND negative IHC) in 6/75 = 8%. "
                   "Authors: the rate is too low to use as a selection criterion. So ~92% MGMT-"
                   "COMPETENT.",
        "why_it_may_not_transfer": "HUMAN, and histiocytic sarcoma is none of the six subtypes in "
                                   "the series. Right tumour class, wrong species.",
    },
    "THE_HONEST_POSITION": "UNKNOWN for canine histiocytic sarcoma. The favourable reading rests on "
        "a different lineage; the unfavourable reading rests on a different species. Picking either "
        "is the transfer error `evidence.Measurement` exists to block.",
    "WHY_IT_STILL_MATTERS_THAT_IT_IS_UNKNOWN": "An unknown that can multiply the deciding agent's "
        "potency by 1/4.3 is not neutral. It is an OPEN escape, and the regimen must be scored both "
        "ways rather than assuming the favourable branch.",
}


# --- the rescues -------------------------------------------------------------------------------------

DOSE_DENSE_IS_FALSIFIED = {
    "the_argument": "MGMT is stoichiometric and consumed per lesion, so dosing faster than "
        "resynthesis should deplete it. THIS REGIMEN ALREADY DOSES TEMOZOLOMIDE CONTINUOUSLY at "
        "duty 1.0, so the rescue would have been FREE.",
    "the_evidence_against": "RTOG 0525. Randomised PHASE III, newly diagnosed glioblastoma, MGMT "
        "status a STRATIFICATION FACTOR. Dose-dense vs standard: median OS 16.6 vs 14.9 months "
        "(p=0.63), no PFS benefit, AND NO BENEFIT BY METHYLATION STATUS -- the exact subgroup the "
        "depletion argument predicts. Grade >=3 toxicity WORSE on dose-dense (27% vs 19%, p=0.008).",
    "verdict": "FALSIFIED. The convenient rescue, the one already built into the regimen at no cost, "
        "is the one the best-powered trial specifically looked for and did not find.",
}

O6_BENZYLGUANINE_COLLIDES = {
    "it_works_pharmacologically": "It is the agent that restored lomustine sensitivity in the canine "
        "lines above -- CL-1 >50 -> 11.5 uM, Nody-1 36.5 -> 7.5 uM.",
    "what_it_costs": "With carmustine it forced the MTD from 200 down to 40 mg/m2 -- an 80% dose "
        "reduction, itself blamed for that combination's phase II failure. With temozolomide, phase "
        "II saw grade 4 haematologic events in 48% of patients (grade 4 neutropenia 47%, grade 4 "
        "thrombocytopenia 12%).",
    "why_it_is_unavailable_HERE": "THE MARROW AXIS IS ALREADY AT EXACTLY 1.00 WITH ZERO HEADROOM. "
        "An agent whose entire toxicity signature is marrow is the worst possible addition.",
    "verdict": "REJECTED ON THE TOXICITY AXIS, not on mechanism.",
}

SWAP_THE_LESION = {
    "the_move": "Replace temozolomide with CARBOPLATIN. Its principal lesion is an N7-guanine "
        "intrastrand crosslink, which is NOT MGMT's substrate, so MGMT has nothing to reverse.",
    "it_needs_no_new_route": "INTRA-ARTERIAL CARBOPLATIN WITH OSMOTIC DISRUPTION IS NEUWELT'S OWN "
        "PROTOCOL -- the same route already costed here.",
    "run_in_the_population_that_matters": "PMID 20023537. Phase I, 13 patients, TEMOZOLOMIDE-"
        "REFRACTORY anaplastic oligodendroglioma/oligoastrocytoma. Carboplatin 200 mg/m2/day "
        "intra-arterially with barrier disruption. That is the population where temozolomide has "
        "ALREADY FAILED, which is the population an MGMT-competent tumour puts this dog in.",
    "canine_availability": "Carboplatin is thoroughly established in dogs.",
    "toxicity_is_a_SWAP_not_an_ADDITION": "Carboplatin's dose-limiting toxicity is myelosuppression, "
        "the same axis temozolomide loads. Because it REPLACES temozolomide the axis does not double.",
    "THE_CAVEAT": "'MGMT-independent' is a claim about DIRECT REVERSAL only. MGMT has been reported "
        "to modulate cisplatin response indirectly through homologous recombination, and platinums "
        "have been reported to downregulate MGMT. The claim here is that MGMT DOES NOT REPAIR THE "
        "PLATINUM LESION -- not that platinum is untouched by everything MGMT-adjacent.",
}


# --- scoring ------------------------------------------------------------------------------------------

@dataclass(frozen=True)
class MGMTState:
    """Whether the tumour repairs O6-alkylguanine. UNKNOWN is not the same as absent."""

    competent: bool
    fold_resistance: float = FOLD_RESISTANCE


SILENCED = MGMTState(False)
COMPETENT = MGMTState(True)


def under_mgmt(agents, state: MGMTState) -> list:
    """Re-price a regimen's agents for an MGMT-competent tumour.

    Only agents whose lesion IS MGMT's substrate lose potency. Everything else is untouched -- which
    is the whole point, and the reason a lesion swap works where a dose increase does not.
    """
    if not state.competent:
        return list(agents)
    out = []
    for a in agents:
        if defeated_by_mgmt(a.name):
            a = Agent(a.name, a.axis, a.layer, a.potency / state.fold_resistance, a.access, a.duty,
                      a.obtainable, a.division_gated, a.antigen_directed, a.note)
        out.append(a)
    return out


def worst_margin(agents, state: MGMTState, growth: float = GROWTH_PER_DAY) -> float:
    r = Regimen("under-mgmt", under_mgmt(agents, state))
    d = DormancyModel()
    return min(d.margin(r, e, growth) if "persister" in e.name
               else r.effective_kill_against(e) - growth for e in ESCAPES)


def carboplatin_swap(agents, potency: float, access: float) -> list:
    """Temozolomide out, carboplatin in. Same route, same axis, different lesion."""
    kept = [a for a in agents if "temozolomide" not in a.name.lower()]
    return kept + [
        Agent("carboplatin (intra-arterial)", Axis.CYTOTOXIC, Layer.RECEPTOR, potency, access, 1.0,
              True, note="N7-guanine intrastrand crosslink -- NOT MGMT's substrate. Delivered by "
                         "the route already costed (PMID 20023537, run in temozolomide-refractory "
                         "patients). Established in dogs.")]


#: Agents dropped from the temozolomide regimen to make the swap fit.
DROPPED_FOR_THE_SWAP = ("temozolomide", "hydroxychloroquine (autophagy)")


def mgmt_proof(compartment: str, potency: float = 0.15) -> Regimen:
    """The regimen that holds whether or not the tumour repairs O6-alkylguanine.

    TWO CHANGES FROM THE TEMOZOLOMIDE VERSION, AND THEY SOLVE EACH OTHER.

    Carboplatin lands on the SAME marrow axis temozolomide occupied, at a slightly higher cost
    (0.60 vs 0.55). Since that axis was already pinned at exactly 1.00, the swap alone pushes it to
    1.05 -- OVERSUBSCRIBED. Dropping hydroxychloroquine returns 0.45 of that axis and, as
    `durable_regimen.THE_FREE_TRADE` established independently, costs 0.00002/day because it is
    structurally barred from covering the escape that binds.

    So the toxicity constraint and the efficacy analysis point at the SAME move, arrived at from
    opposite directions. Final headroom +0.40, against +0.00 before.
    """
    from .durable_regimen import build as _build
    agents = [a for a in _build(compartment).agents
              if not any(d in a.name for d in ("hydroxychloroquine",))]
    tmz = next(a for a in _build(compartment).agents if "temozolomide" in a.name)
    return Regimen("MGMT-proof (carboplatin)", carboplatin_swap(agents, potency, tmz.access))


def survives_mgmt(compartment: str, growth: float = GROWTH_PER_DAY) -> bool:
    return worst_margin(mgmt_proof(compartment).agents, COMPETENT, growth) > 0


# --- computed results ---------------------------------------------------------------------------------

#: fold resistance -> worst margin of the TEMOZOLOMIDE regimen in the parenchyma
TEMOZOLOMIDE_BREAKS_AT = {1.0: 0.0556, 1.5: 0.0190, 2.0: 0.0006, 2.5: -0.0104, 3.0: -0.0177,
                          4.3: -0.0288, 4.9: -0.0319}
BREAKING_POINT = "Between 2.0x and 2.5x. THE MEASURED CANINE EFFECT IS 4.3-4.9x, so even the most "\
                 "generous reading of the measurement breaks the temozolomide regimen."

#: (parenchyma, leptomeninges) worst margins, MGMT COMPETENT
UNDER_COMPETENT_MGMT = {
    "temozolomide regimen": (-0.0288, -0.0112),      # BOTH OPEN
    "carboplatin swap, HCQ dropped": (0.0556, 0.0730),  # both closed
}

TOXICITY_OF_THE_RESCUES = {
    "temozolomide regimen (current)": "marrow 1.00, headroom +0.00 -- tolerable but pinned",
    "+ O6-benzylguanine": "marrow 1.85 -- OVERSUBSCRIBED. Rejected.",
    "carboplatin swap alone": "marrow 1.05 -- OVERSUBSCRIBED. Does not fit on its own.",
    "carboplatin swap + drop hydroxychloroquine": "marrow 0.60, HEADROOM +0.40. Fits, with more "
        "room than the regimen ever had.",
}


WHAT_THIS_MODULE_ESTABLISHES = (
    "MGMT IS AN ELEVENTH ESCAPE and it was missing. The ten in the catalogue are all SIGNALLING "
    "escapes, which temozolomide beats by being indifferent to signalling. MGMT is a repair enzyme "
    "aimed at temozolomide's own lesion, so indifference is no defence.",
    "IT DEFEATS LOMUSTINE TOO -- O6-chloroethylguanine is the same substrate -- AND LOMUSTINE IS THE "
    "STANDARD OF CARE FOR CANINE HISTIOCYTIC SARCOMA. An MGMT-competent tumour resists what it would "
    "be given anyway.",
    "THE FREE RESCUE IS FALSIFIED. Continuous dosing is already in the regimen and RTOG 0525 looked "
    "specifically for its benefit by methylation status and did not find it.",
    "THE PHARMACOLOGICAL RESCUE COLLIDES. O6-benzylguanine works and is pure marrow toxicity, on the "
    "axis that already has ZERO headroom.",
    "THE RESCUE THAT SURVIVES IS A LESION SWAP, NOT A DOSE CHANGE. Carboplatin's lesion is not "
    "MGMT's substrate, it uses the route already costed, it has been run in temozolomide-refractory "
    "patients, and it is established in dogs.",
)
