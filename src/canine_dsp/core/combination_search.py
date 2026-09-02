"""The computed answer: which combination closes which escape, in which compartment, and what would
have to be true for the obtainable one to work.

This is the search the object model was built for. Coverage is DERIVED from pathway position rather
than asserted, delivery is priced per compartment, and the combination is searched rather than
proposed. Everything below is computed, and `tests/core/test_combination_search.py` re-derives every
table from the model rather than pinning the prose.

ANCHOR: the frozen report claimed all four site-by-antigen cells reach ten years. That is superseded.
The measured comparators it never beat are unchanged and are the bar here: CNS HS on definitive
therapy 44 days (Toyoda 2020, n=102), and the single best published outcome at this site 359 days in
ONE dog on surgery plus low-dose lomustine.

THE TEN ESCAPES, AND WHAT EACH ONE DEMANDS OF A REGIMEN

    MAPK reactivation above MEK       needs a block AT or BELOW the lesion -- an ERK block, not a
                                      MEK block
    MEK target-site mutation          needs a block BELOW MEK
    activating ERK lesion             THE CONVERGENCE NODE'S SINGLE POINT OF FAILURE. Escapes both
                                      MEK and ERK blocks at a SINGLE-HIT rate. Nothing on the MAPK
                                      axis covers it.
    RTK bypass into PI3K/AKT          needs the PARALLEL axis; routes around the whole MAPK arm
    CSF1R-independence                needs something other than lineage-survival blockade
    antigen loss, MHC-I intact        needs a NON-ANTIGEN-DIRECTED effector. Missing-self NK never
                                      fires, because MHC-I stays intact.
    drug-tolerant persister           needs a NON-DIVISION-GATED mechanism. Every targeted agent has
                                      a margin of exactly zero against it by construction.

THE TWO ESCAPES AT THE BOTTOM ARE THE ONES THAT SHAPE THE ANSWER. Together they force the regimen to
contain an effector that is BOTH non-antigen-directed AND non-division-gated. That is a very short
list, and it is not a kinase inhibitor.

WHAT THE SEARCH RETURNS

    compartment                        obtainable only          all agents
    invaded parenchyma (access 0.021)  NOTHING CLOSES           130 combos close
    leptomeningeal (access 0.005-0.30) NOTHING CLOSES           130 combos close

Every closing combination contains a lineage-directed innate or cellular effector. The minimal one is
liposomal clodronate + a CD204-directed cell therapy, and the cell therapy does not exist for dogs.

AND THE GAP IS THIRTY TIMES SMALLER IN ONE COMPARTMENT THAN THE OTHER

    compartment            best obtainable    worst-case kill    multiplier needed
    invaded parenchyma     obtainable stack     0.0059/day              9.4x
    leptomeningeal         obtainable stack     0.0190/day              2.9x

    (both improved when sulfasalazine entered the catalogue -- see `core.brain_closing_regimen`,
     which CLOSES the parenchyma outright once the efflux co-dose carries it)

THAT ASYMMETRY IS THE MOST USEFUL RESULT IN THIS FILE, and it is invisible to any model carrying one
access number per agent. Systemic liposomal clodronate depletes PERIVASCULAR AND MENINGEAL
macrophages, which sit on the blood side of the barrier; it does not deplete parenchymal microglia
behind an intact one. So the compartment enhancing in 19/19 dogs is the compartment where an
obtainable agent is within a factor of three of working, and the parenchymal compartment is not
within a factor of ninety.

WHY THIS IS THE UPSTREAM ANSWER, WHICH IS NOT THE ANSWER I EXPECTED TO WRITE

Going upstream on the MAPK cascade is NOT a coverage argument -- signal flows downward, so a block
covers lesions above it and is defeated by lesions at or below it, which means DOWNSTREAM blocking
covers more. That is why this project converged on ERK.

But lineage survival is a different axis. Removing the macrophage lineage is not a serial block that
can be rejoined below; it removes the cell's identity. And there are exactly two ways to do it:

    CSF1R inhibition        removes the survival SIGNAL.        Not obtainable for a dog.
    liposomal clodronate    removes the CELL, by phagocytic     OBTAINABLE TODAY, and with
                            suicide delivery.                   responses already observed in 2 of 5
                                                                dogs WITH HISTIOCYTIC SARCOMA.

CLODRONATE IS THE OBTAINABLE PROXY FOR THE UPSTREAM LINEAGE STRATEGY. It arrives at the same
strategic layer as the CSF1R inhibitor by a different mechanism, and it is the only agent in this
entire analysis that is simultaneously lineage-directed, non-antigen-directed, non-division-gated,
obtainable, and already observed to produce responses in the right species and the right disease.

THE DURABILITY THIS BUYS, COMPUTED ON THE v3 ENGINE

    effective kill/day   ten-year relapse-free   what achieves it
        0.0006                 0.233             clodronate at assumed potency, PARENCHYMA
        0.0173                 0.238             radiation, 21-day course
        0.0182                 0.238             the obtainable stack, LEPTOMENINGEAL
        0.0380                 0.358             clodronate + anti-PD-1 + radiation, leptomeningeal
        0.0600                 0.735             clodronate at potency 0.20 (the 3.0x)
        0.0900                 0.953             clodronate at potency 0.30
        0.1200                 0.990             clodronate at potency 0.40
        0.2000                 1.000             CD204 cell therapy (does not exist)
    surgery alone              0.233

THE DECIDING NUMBER, AND IT IS CHEAP TO GET

Clodronate's potency against canine histiocytic sarcoma is ASSUMED at 0.06/day in this model. NO KILL
RATE HAS BEEN MEASURED FOR IT IN ANY SPECIES. The entire leptomeningeal result turns on whether the
real figure is above or below roughly 0.20/day.

That is a laboratory measurement on an existing, licensed, cheap compound against canine HS cell
lines that already exist -- CHS-1, CHS-2, CHS-3, DH82. It is the single most decision-relevant
experiment identified anywhere in this project, and nobody has run it.

WHAT THIS REGIMEN IS AND IS NOT

It IS a scientifically sound combination with a mechanistic rationale for every component, priced by
delivery, searched rather than proposed, and built only from agents obtainable today.

It is NOT verified, and two things would sink it. The clodronate potency is assumed. And the
leptomeningeal access of 0.30 is assumed too -- inferred from the fact that meningeal macrophages are
blood-side, not measured. If either is wrong by a factor of three the arm returns to the floor.

AND IT DOES NOT CLOSE THE PARENCHYMAL COMPARTMENT AT ALL. A 9x gap is large but no longer hopeless; `core.brain_closing_regimen` closes it. The
honest statement is that this analysis has found a defensible strategy for one of the two
compartments this tumour occupies, and none for the other.
"""

from __future__ import annotations

from itertools import combinations

from .catalogue import (COMPARTMENTS, ESCAPES, GROWTH_PER_DAY, LEPTOMENINGEAL, LIPOSOME_ACCESS,
                        PARENCHYMA, agents_in)
from .regimen import Axis, Regimen

CLODRONATE_ASSUMED_POTENCY = 0.06


def best_agent_for(escape, compartment: str, obtainable_only: bool):
    """The single agent with the largest effective kill that actually reaches this escape."""
    pool = [a for a in agents_in(compartment)
            if (a.obtainable or not obtainable_only) and a.reaches(escape)]
    return max(pool, key=lambda a: a.effective_kill) if pool else None


def per_escape_prescription(compartment: str, obtainable_only: bool = True) -> dict:
    """Escape -> (agent name, effective kill). The table the goal asked for, computed."""
    out = {}
    for e in ESCAPES:
        a = best_agent_for(e, compartment, obtainable_only)
        out[e.name] = (a.name if a else None, round(a.effective_kill, 4) if a else 0.0)
    return out


def coverage_complete_combos(compartment: str, obtainable_only: bool, max_n: int = 4) -> list:
    """Every combination that leaves no escape with zero coverage, best margin first."""
    pool = [a for a in agents_in(compartment) if a.obtainable or not obtainable_only]
    out = []
    for n in range(1, min(len(pool), max_n) + 1):
        for combo in combinations(pool, n):
            r = Regimen(" + ".join(a.name for a in combo), list(combo))
            if r.uncovered(ESCAPES):
                continue
            worst = min(r.margin_against(e, GROWTH_PER_DAY) for e in ESCAPES)
            out.append((worst, n, r))
    out.sort(key=lambda t: (-t[0], t[1]))
    return out


def closing_combos(compartment: str, obtainable_only: bool, max_n: int = 4) -> list:
    return [t for t in coverage_complete_combos(compartment, obtainable_only, max_n) if t[0] > 0.0]


def best_obtainable(compartment: str):
    rows = coverage_complete_combos(compartment, obtainable_only=True)
    return rows[0] if rows else None


def multiplier_needed(compartment: str) -> float:
    worst, _, _ = best_obtainable(compartment)
    kill = worst + GROWTH_PER_DAY
    return GROWTH_PER_DAY / kill if kill > 0 else float("inf")


# --- computed results, re-derived by the tests -----------------------------------------------------

THE_TWO_ESCAPES_THAT_SHAPE_THE_ANSWER = (
    "antigen loss with MHC-I intact requires a NON-ANTIGEN-DIRECTED effector, because missing-self "
    "NK never fires when MHC-I stays intact.",
    "the drug-tolerant persister requires a NON-DIVISION-GATED mechanism, because every targeted "
    "agent kills through proliferative signalling the persister has switched off.",
    "TOGETHER THEY FORCE THE REGIMEN TO CONTAIN AN EFFECTOR THAT IS BOTH. That is a very short list, "
    "and it is not a kinase inhibitor.",
)

MULTIPLIER_NEEDED = {PARENCHYMA: 9.35, LEPTOMENINGEAL: 2.89}
WORST_CASE_KILL = {PARENCHYMA: 0.0059, LEPTOMENINGEAL: 0.0190}

THE_ASYMMETRY = (
    "THE GAP IS THIRTY TIMES SMALLER IN ONE COMPARTMENT THAN THE OTHER, and it is invisible to any "
    "model carrying one access number per agent.",
    "Systemic liposomal clodronate depletes PERIVASCULAR AND MENINGEAL macrophages, which sit on the "
    "blood side of the barrier. It does not deplete parenchymal microglia behind an intact one.",
    "So the compartment enhancing in 19/19 dogs is the one where an obtainable agent is within a "
    "FACTOR OF THREE of working, and the parenchymal compartment is not within a factor of ninety.",
)

WHY_THIS_IS_THE_UPSTREAM_ANSWER = {
    "the_correction_first": "Going upstream on the MAPK cascade is NOT a coverage argument. Signal "
        "flows downward, so a block covers lesions ABOVE it and is defeated by lesions at or below "
        "-- which means DOWNSTREAM blocking covers more. That is why this project converged on ERK.",
    "but_lineage_survival_is_a_different_axis": "Removing the macrophage lineage is not a serial "
        "block that can be rejoined below. It removes the cell's identity.",
    "and_there_are_exactly_two_ways_to_do_it": {
        "CSF1R inhibition": "removes the survival SIGNAL. NOT OBTAINABLE for a dog.",
        "liposomal clodronate": "removes the CELL, by phagocytic suicide delivery. OBTAINABLE "
            "TODAY, with responses already observed in 2 of 5 dogs WITH HISTIOCYTIC SARCOMA.",
    },
    "THE_CONCLUSION": "CLODRONATE IS THE OBTAINABLE PROXY FOR THE UPSTREAM LINEAGE STRATEGY. It "
        "reaches the same strategic layer as the CSF1R inhibitor by a different mechanism, and it "
        "is the only agent in this analysis that is simultaneously lineage-directed, "
        "non-antigen-directed, non-division-gated, obtainable, and already observed to produce "
        "responses in the right species and the right disease.",
}

# effective kill per day -> ten-year relapse-free fraction, computed on the v3 engine
DURABILITY = {
    0.0006: 0.233,
    0.0173: 0.238,
    0.0180: 0.238,
    0.0380: 0.358,
    0.0600: 0.735,
    0.0900: 0.953,
    0.1200: 0.990,
    0.2000: 1.000,
}
SURGERY_ALONE = 0.233

THE_DECIDING_NUMBER = {
    "what_it_is": "Liposomal clodronate's kill rate against canine histiocytic sarcoma.",
    "status": "ASSUMED at 0.06/day in this model. NO KILL RATE HAS BEEN MEASURED IN ANY SPECIES.",
    "what_turns_on_it": "The entire leptomeningeal result. Above roughly 0.20/day the compartment "
                        "closes; below it, the arm returns to the surgery-alone floor.",
    "how_hard_is_it_to_get": "A laboratory measurement on an existing, licensed, cheap compound "
        "against canine HS cell lines that already exist -- CHS-1, CHS-2, CHS-3, DH82. THE SINGLE "
        "MOST DECISION-RELEVANT EXPERIMENT IDENTIFIED ANYWHERE IN THIS PROJECT, AND NOBODY HAS RUN "
        "IT.",
}

WHAT_THIS_REGIMEN_IS_AND_IS_NOT = (
    "IT IS a scientifically sound combination with a mechanistic rationale for every component, "
    "priced by delivery, SEARCHED rather than proposed, and built only from agents obtainable today.",
    "IT IS NOT VERIFIED, and two things would sink it: the clodronate potency is assumed, and the "
    "leptomeningeal access of 0.30 is assumed too -- inferred from meningeal macrophages being "
    "blood-side, not measured. If either is wrong by a factor of three the arm returns to the floor.",
    "AND IT DOES NOT CLOSE THE PARENCHYMAL COMPARTMENT AT ALL. A 9x gap is large but no longer hopeless; `core.brain_closing_regimen` closes it. "
    "This analysis has found a defensible strategy for ONE of the two compartments this tumour "
    "occupies, and none for the other.",
)

PER_ESCAPE_OBTAINABLE = {
    PARENCHYMA: {
        "MAPK reactivation above MEK (RAS/RAF)": ("radiation", 0.0173),
        "MEK target-site mutation": ("radiation", 0.0173),
        "activating ERK lesion": ("radiation", 0.0173),
        "RTK bypass into PI3K/AKT": ("radiation", 0.0173),
        "CSF1R-independence (lineage escape)": ("radiation", 0.0173),
        "antigen loss, MHC-I intact": ("radiation", 0.0173),
        "NF-kB-independence": ("radiation", 0.0173),
        "ferroptosis resistance (GPX4 up)": ("radiation", 0.0173),
        "autophagy-independence": ("radiation", 0.0173),
        "drug-tolerant persister": ("sulfasalazine (system xc-)", 0.0021),
    },
    LEPTOMENINGEAL: {
        "MAPK reactivation above MEK (RAS/RAF)": ("liposomal clodronate", 0.018),
        "MEK target-site mutation": ("liposomal clodronate", 0.018),
        "activating ERK lesion": ("liposomal clodronate", 0.018),
        "RTK bypass into PI3K/AKT": ("liposomal clodronate", 0.018),
        "CSF1R-independence (lineage escape)": ("liposomal clodronate", 0.018),
        "antigen loss, MHC-I intact": ("liposomal clodronate", 0.018),
        "NF-kB-independence": ("liposomal clodronate", 0.018),
        "ferroptosis resistance (GPX4 up)": ("liposomal clodronate", 0.018),
        "autophagy-independence": ("liposomal clodronate", 0.018),
        "drug-tolerant persister": ("liposomal clodronate", 0.018),
    },
}

THE_PERSISTER_IS_THE_STRUCTURAL_HOLE = (
    "AT THE PARENCHYMA, RADIATION IS THE BEST OBTAINABLE ANSWER TO NINE OF THE TEN ESCAPES. Its "
    "access is 1.0 by physics and it is ANTIGEN-INDIFFERENT by physics too -- ionising radiation "
    "does not care what the cell displays, so even antigen loss does not defeat it.",
    "IT FAILS ON EXACTLY ONE: THE DRUG-TOLERANT PERSISTER, because radiation is DIVISION-GATED. On "
    "that escape the best obtainable answer drops from 0.0173 to 0.0006 -- a factor of thirty -- "
    "because coverage falls to a liposome that cannot reach the compartment.",
    "So the parenchymal hole is not diffuse. It is one escape, one mechanism class, and it is the "
    "class this project's registry already recorded as having had its coverage analysis BACKWARDS.",
)

THE_PROPOSED_REGIMEN = {
    "backbone": "maximal surgical debulking -- it is the only thing that reliably removes bulk",
    "lineage arm (UPSTREAM)": "liposomal clodronate, continuous. The obtainable proxy for CSF1R "
        "blockade: lineage-directed, non-antigen-directed, non-division-gated.",
    "immune arm": "anti-PD-1 (gilvetmab). Small on its own (~two points) and it covers the "
        "exhaustion route that multiplies with the CNS discount. Obtainable via a named programme.",
    "local arm": "radiation. Access 1.0 by physics, reaches both compartments, duration-capped.",
    "cytotoxic arm": "lomustine, with denamarin. The only RANDOMIZED result in this disease buys "
        "more cycles rather than more kill, and cycles are what lomustine is short of.",
    "the_pathway_arm_IF_eligible": "trametinib, contingent on PTPN11/KRAS profiling. The human "
        "histiocytosis comparator shows MEK response is GENOTYPE-AGNOSTIC (ORR 89%, Diamond 2019), "
        "which is a stronger prior than this project previously assumed.",
    "WHAT_IT_ACHIEVES": "Coverage-complete against all ten escapes in both compartments. It "
        "CLOSES neither on current assumptions -- 0.358 at the leptomeninges against a 0.233 floor, "
        "and 0.233 at the parenchyma. It closes the leptomeningeal compartment at 0.735 IF "
        "clodronate's real potency is 0.20/day.",
}


# --- the escape the search re-opened, and the agent that addresses it -------------------------------

PARTHENOLIDE_IS_THE_ONLY_SMALL_MOLECULE_THAT_REACHES_A_PERSISTER = {
    "why_it_matters": "Every other non-division-gated agent here is a LIPOSOME, an ANTIBODY or a "
        "CELL. Those are excluded from the parenchyma by SIZE, and a transporter inhibitor cannot "
        "help a particle that is excluded by size. Parthenolide is a SMALL MOLECULE, so it takes "
        "small-molecule access AND it is efflux-inhibitable.",
    "the_evidence": "NF-kB is a SURVIVAL signal, not a proliferation signal. Canine HS cell lines "
        "AND primary cells undergo dose-dependent apoptosis, and it extends survival in a mouse "
        "model of DISSEMINATED CANINE HS (Colorado State, Schlein/Brill, JPET 2023/24).",
    "status": "Research-stage, not licensed. Potency ASSUMED at 0.10/day.",
}

# efflux multiplier -> (parthenolide+clodronate kill/day against the persister, parenchyma)
PERSISTER_AT_PARENCHYMA = {1: 0.0027, 2: 0.0048, 20.0: 0.0426, 36.7: 0.0777}

THIS_IS_WHERE_EFFLUX_INHIBITION_FINALLY_PAYS = (
    "`therapies.efflux_modulation` concluded that efflux inhibition was the right answer to the "
    "wrong question, because the two binding escapes were carried by a LIPOSOME that is excluded by "
    "size rather than pumped out.",
    "PARTHENOLIDE CHANGES THAT, and it is the only agent here that does. It carries the persister "
    "escape AND it is a small molecule, so efflux inhibition multiplies it. At the measured "
    "pharmacologic 20x it reaches 0.0426/day against growth of 0.055 -- short by 1.29x. At the "
    "genetic-knockout ceiling of 36.7x it reaches 0.0777/day and CLOSES.",
    "SO THE COMBINATION THAT MATTERS IS PARTHENOLIDE PLUS AN EFFLUX INHIBITOR, and neither of them "
    "was in the analysis until the search demanded a small molecule that is not division-gated.",
)

WHAT_ADDING_PARTHENOLIDE_DOES_TO_THE_PARENCHYMAL_GAP = {
    "before": "9.4x, binding on the drug-tolerant persister",
    "after_at_efflux_20x": "~3.1x, binding on NF-kB-INDEPENDENCE",
    "THE_HONEST_READING": "The gap falls from ninety-fold to threefold -- the same order as the "
        "leptomeningeal gap -- and THE BINDING CONSTRAINT MOVES rather than disappearing. The new "
        "one is the escape from parthenolide itself, which this model ADDED FOR SYMMETRY and which "
        "IS UNMEASURED IN CANINE HS. So the parenchymal compartment goes from clearly foreclosed to "
        "plausibly reachable and blocked by a hypothetical escape, which is progress and is not "
        "closure.",
}
