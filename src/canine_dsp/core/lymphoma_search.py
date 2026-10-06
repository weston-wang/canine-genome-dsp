"""The computed answer: which combination closes which escape, in which compartment, for which
immunophenotype, and what early detection changes.

This is the search the object model was built for. Coverage is DERIVED from mechanism position,
delivery is priced per compartment, and the combination is SEARCHED rather than proposed. Every
table here is re-derived by tests/test_lymphoma_search.py rather than pinned as prose.

See docs/LYMPHOMA_DURABLE_RESPONSE.md section 11.
"""

from __future__ import annotations

from itertools import combinations

from .lymphoma_catalogue import (BURDEN_CLINICALLY_OBVIOUS, BURDEN_EARLY_DETECTED, BURDEN_MRD, CNS,
                                 COMPARTMENTS, ESCAPES, GROWTH_PER_DAY, SYSTEMIC, agents_for)
from .regimen import Regimen, escape_presence_probability

MAX_COMBO = 5


def best_agent_for(escape, compartment: str, immunophenotype: str = "B",
                   obtainable_only: bool = True):
    """The single agent with the largest effective kill that actually reaches this escape."""
    pool = [a for a in agents_for(compartment, immunophenotype, obtainable_only)
            if a.reaches(escape)]
    return max(pool, key=lambda a: a.effective_kill) if pool else None


def per_escape_prescription(compartment: str, immunophenotype: str = "B",
                            obtainable_only: bool = True) -> dict:
    """Escape -> (best agent, its effective kill). The per-escape table, computed."""
    out = {}
    for e in ESCAPES:
        a = best_agent_for(e, compartment, immunophenotype, obtainable_only)
        out[e.name] = (a.name if a else None, round(a.effective_kill, 4) if a else 0.0)
    return out


def uncovered_escapes(compartment: str, immunophenotype: str = "B",
                      obtainable_only: bool = True) -> tuple:
    """Escapes for which NO available agent has any reach at all -- coverage holes, before any
    question of whether the kill is big enough."""
    return tuple(name for name, (agent, _) in
                 per_escape_prescription(compartment, immunophenotype, obtainable_only).items()
                 if agent is None)


def coverage_complete_combos(compartment: str, immunophenotype: str = "B",
                             obtainable_only: bool = True, max_n: int = MAX_COMBO,
                             escapes=ESCAPES) -> list:
    """Every combination leaving no escape with zero coverage, best worst-case margin first."""
    pool = list(agents_for(compartment, immunophenotype, obtainable_only))
    out = []
    for n in range(1, min(len(pool), max_n) + 1):
        for combo in combinations(pool, n):
            r = Regimen(" + ".join(a.name for a in combo), list(combo))
            if r.uncovered(escapes):
                continue
            worst = min(r.margin_against(e, GROWTH_PER_DAY) for e in escapes)
            out.append((worst, n, r))
    out.sort(key=lambda t: (-t[0], t[1]))
    return out


def closing_combos(compartment: str, immunophenotype: str = "B", obtainable_only: bool = True,
                   max_n: int = MAX_COMBO, escapes=ESCAPES) -> list:
    """Combinations that not only cover every escape but out-kill growth against all of them."""
    return [t for t in coverage_complete_combos(compartment, immunophenotype, obtainable_only,
                                                max_n, escapes) if t[0] > 0.0]


def minimal_closing(compartment: str, immunophenotype: str = "B", obtainable_only: bool = True,
                    escapes=ESCAPES):
    """The smallest closing combination (ties broken by best margin)."""
    rows = closing_combos(compartment, immunophenotype, obtainable_only, escapes=escapes)
    if not rows:
        return None
    fewest = min(n for _, n, _ in rows)
    return max((t for t in rows if t[1] == fewest), key=lambda t: t[0])


def best_obtainable(compartment: str, immunophenotype: str = "B", escapes=ESCAPES):
    rows = coverage_complete_combos(compartment, immunophenotype, obtainable_only=True,
                                    escapes=escapes)
    return rows[0] if rows else None


def multiplier_needed(compartment: str, immunophenotype: str = "B", escapes=ESCAPES) -> float:
    """How many times stronger the best obtainable stack would have to be to close."""
    row = best_obtainable(compartment, immunophenotype, escapes)
    if row is None:
        return float("inf")
    worst, _, regimen = row
    weakest = regimen.weakest_link(escapes, GROWTH_PER_DAY)
    kill = regimen.effective_kill_against(weakest)
    return GROWTH_PER_DAY / kill if kill > 0 else float("inf")


# --- the early-detection premise, quantified ------------------------------------------------------

def escapes_likely_present(tumour_cells: float, threshold: float = 0.5) -> tuple:
    """Which escapes have probably ALREADY ARISEN at a given tumour burden.

    This is what early detection actually buys, and it is a mechanism argument rather than a timing
    one: an escape that has not yet arisen does not need to be out-killed, it needs only to be
    prevented from arising -- which a regimen that keeps the burden low does for free.
    """
    return tuple(e.name for e in ESCAPES
                 if escape_presence_probability(e, tumour_cells) >= threshold)


def presence_table() -> dict:
    """Escape -> P(already present) at clinically obvious, early-detected and MRD burdens."""
    return {
        e.name: {
            "clinically_obvious_1e11": round(escape_presence_probability(e, BURDEN_CLINICALLY_OBVIOUS), 4),
            "early_detected_1e8": round(escape_presence_probability(e, BURDEN_EARLY_DETECTED), 4),
            "mrd_1e6": round(escape_presence_probability(e, BURDEN_MRD), 4),
        }
        for e in ESCAPES
    }


def escapes_at_burden(tumour_cells: float, threshold: float = 0.5) -> tuple:
    """The Escape objects (not names) likely present at a burden -- the set a regimen must close."""
    return tuple(e for e in ESCAPES
                 if escape_presence_probability(e, tumour_cells) >= threshold)


# --- what the search returns ----------------------------------------------------------------------

WHAT_THE_SEARCH_RETURNS = (
    "SYSTEMICALLY, obtainable agents close every escape -- but only combinations that contain an "
    "agent surviving all three filters at once (not division-gated, not antigen-directed, not an "
    "efflux substrate). Prednisolone and hydroxychloroquine are the obtainable ones.",
    "IN THE CNS SANCTUARY the same regimen collapses, because the antibody arm is excluded (access "
    "0.002) and the small-molecule arms drop to 5%. What survives is the CELL therapy, which "
    "traffics across on its own power, plus the two agents that enter by lipophilicity or "
    "lysosomotropism -- lomustine and hydroxychloroquine.",
    "SO THE SANCTUARY DOES NOT NEED A BIGGER DOSE, IT NEEDS A DIFFERENT MODALITY. That asymmetry is "
    "invisible to any model carrying one access number per agent.",
)

THE_IMMUNOPHENOTYPE_SPLIT = {
    "finding": "Venetoclax is the right drug for canine T-CELL lymphoma and the wrong one for "
               "B-cell, and this is MEASURED, not inferred: mean EC50 0.023 uM in neoplastic canine "
               "T lymphocytes versus 288 uM in most non-indolent B-cell cancers, with BCL2 protein "
               "level failing to predict sensitivity (Jegatheeson et al. 2022, PMID 36433867).",
    "why_it_matters": "The earlier analysis called T-cell simply 'harder' -- faster growth, higher "
                      "bar, and no CD20 to target. That is true and incomplete. T-cell disease has "
                      "an APOPTOSIS-AXIS vulnerability that B-cell disease does not, and it is "
                      "available in a licensed oral drug. So the two immunophenotypes need "
                      "genuinely different regimens, not the same regimen at different doses.",
    "b_cell_route": "CD20/CD19-directed cellular immunity carries durability; venetoclax does not.",
    "t_cell_route": "Venetoclax carries a real, measured apoptosis-axis kill; there is no CD20 to "
                    "target, so the immune arm must be lineage- or CD5/CD52-directed.",
}

THE_THREE_FILTERS = (
    "PERSISTER -> the agent must not be division-gated. Excludes doxorubicin, vincristine, "
    "cyclophosphamide, rabacfosadine, lomustine and total body irradiation -- every conventional "
    "cytotoxic in the disease.",
    "ANTIGEN LOSS -> the agent must not be antigen-directed, or the regimen must carry two "
    "independent antigens. Excludes the anti-CD20 antibody and a single-antigen CAR.",
    "EFFLUX -> the agent must not be a P-glycoprotein substrate. Excludes doxorubicin and "
    "vincristine, the two most active drugs in CHOP, and this filter is MEASURED in this disease.",
    "THE INTERSECTION IS SHORT AND CONTAINS NO CONVENTIONAL CHEMOTHERAPY: prednisolone, "
    "hydroxychloroquine, venetoclax (T-cell), a BTK inhibitor, and a cellular immune effector.",
)

# --- what the search actually returned, re-derived by tests/test_lymphoma_search.py ---------------

#: Smallest obtainable combination that closes EVERY escape, against established disease.
MINIMAL_CLOSING = {
    (SYSTEMIC, "B"): ("prednisolone (glucocorticoid) + CD20 CAR-T", 2, 0.0097),
    (SYSTEMIC, "T"): ("prednisolone (glucocorticoid) + hydroxychloroquine (autophagy)", 2, 0.0097),
    (CNS, "B"): ("prednisolone + intrathecal cytarabine + CD20 CAR-T + hydroxychloroquine",
                 4, 0.0097),
    (CNS, "T"): (None, None, None),   # nothing obtainable closes it
}

#: Best worst-case margin achievable with <=5 obtainable agents -- the regimen to actually want,
#: because a minimal combination sitting +0.0097 over the bar has no headroom for a wrong potency.
MOST_ROBUST = {
    (SYSTEMIC, "B"): {
        "agents": ("doxorubicin", "vincristine", "prednisolone (glucocorticoid)", "CD20 CAR-T",
                   "hydroxychloroquine (autophagy)"),
        "worst_margin": 0.2297, "times_bar": 3.54, "weakest_link": "P-glycoprotein / ABCB1 efflux"},
    (SYSTEMIC, "T"): {
        "agents": ("doxorubicin", "vincristine", "anti-PD-1 / anti-PD-L1 checkpoint blockade",
                   "hydroxychloroquine (autophagy)", "venetoclax (BCL2 inhibitor)"),
        "worst_margin": 0.1997, "times_bar": 3.21, "weakest_link": "P-glycoprotein / ABCB1 efflux"},
    (CNS, "B"): {
        "agents": ("prednisolone (glucocorticoid)", "intrathecal cytarabine",
                   "craniospinal radiotherapy", "CD20 CAR-T", "hydroxychloroquine (autophagy)"),
        "worst_margin": 0.0270, "times_bar": 1.30, "weakest_link": "CD20 antigen loss"},
    (CNS, "T"): None,
}

#: The one cell the search cannot close, and exactly why.
THE_ONE_THAT_DOES_NOT_CLOSE = {
    "cell": "CNS sanctuary, T-cell immunophenotype",
    "status": "NOTHING OBTAINABLE CLOSES IT. Every obtainable agent combined leaves a worst margin "
              "of -0.0127.",
    "binding_escape": "drug-tolerant persister, reached at 0.0776/day against a bar of 0.0903 "
                      "(0.86x) -- short by a factor of 1.16.",
    "why": "The persister demands a NON-DIVISION-GATED agent, and in the CNS the non-division-gated "
           "agents available to T-cell disease are only prednisolone (0.04), hydroxychloroquine "
           "(0.03) and venetoclax at small-molecule access (0.008). B-cell disease clears the same "
           "bar because CD20 CAR-T adds 0.06 by TRAFFICKING ACROSS THE BARRIER UNDER ITS OWN POWER. "
           "T-lineage has no obtainable equivalent.",
    "the_counterfactual": "If a CD5/CD52-directed cellular effector existed for dogs, the cell "
                          "closes immediately: prednisolone + intrathecal cytarabine + "
                          "hydroxychloroquine + that effector, worst margin +0.0097, and the "
                          "all-agent margin rises to +0.0473.",
    "so_the_gap_is_one_missing_thing": "Not a dose, not a schedule, and not a delivery trick -- a "
                                       "T-lineage cellular effector that traffics into the CNS. "
                                       "That is a single, nameable, buildable object, and it is the "
                                       "most decision-relevant absence this analysis found.",
    "the_fratricide_hazard_it_does_not_price": "A CD5-directed T-cell product attacks T cells, "
                                               "including itself. The model does not represent "
                                               "fratricide, so the counterfactual above is an upper "
                                               "bound on how easy that agent would be to build.",
}

#: Against early-detected disease (~1e8 cells), two escapes have not yet arisen and the picture
#: changes -- but not in the sanctuary.
EARLY_DETECTION_RESULT = {
    "escapes_absent_at_1e8": ("autophagy independence", "B-lineage identity switch"),
    "escapes_to_close": 9,
    (SYSTEMIC, "B"): ("hydroxychloroquine (autophagy)", 1, 0.0097),
    (SYSTEMIC, "T"): ("hydroxychloroquine (autophagy)", 1, 0.0097),
    (CNS, "B"): ("prednisolone + intrathecal cytarabine + CD20 CAR-T + hydroxychloroquine",
                 4, 0.0097),
    (CNS, "T"): None,
    "THE_SINGLE_AGENT_RESULT_IS_FRAGILE": "At an early-detected burden the search returns "
        "hydroxychloroquine ALONE as sufficient systemically. That is true inside the model and "
        "must not be read as a recommendation: it holds only because the one escape that defeats it "
        "-- autophagy independence -- has not yet arisen at that burden, and it rests on an ASSUMED "
        "potency sitting +0.0097 over the bar. A single agent with no headroom and one unarisen "
        "counter-escape is a knife-edge, not a plan. The robust multi-agent regimens are what the "
        "analysis actually supports.",
    "what_early_detection_genuinely_buys": "It removes the RARE MUTATIONAL escapes and leaves every "
        "PHENOTYPIC one untouched. The persister and immune exhaustion arise at ~1e-7 per cell and "
        "are still effectively certain at 1e8 cells, so the non-division-gated agent stays "
        "mandatory no matter how early the disease is found. Early detection shrinks the problem; "
        "it does not change its shape.",
    "and_it_does_not_open_the_sanctuary": "The CNS result is IDENTICAL early and late, because the "
        "escapes that bind there -- antigen loss and the persister -- are present at both burdens. "
        "Finding the disease earlier does not help with the compartment the drug cannot reach.",
}

WHAT_EARLY_DETECTION_BUYS = (
    "Early detection is usually argued as a timing lever -- treat sooner, smaller burden. The "
    "model says the real prize is different and larger: AT A SMALL ENOUGH BURDEN, SEVERAL ESCAPES "
    "HAVE NOT YET ARISEN AT ALL.",
    "An escape arising at rate r per cell is present with probability 1 - exp(-r x N). At a "
    "clinically obvious burden (~1e11 cells) every lesion modelled here is effectively CERTAIN to "
    "be present already. At an early-detected burden (~1e8) the rarer ones are not, and at MRD "
    "level (~1e6) most are not.",
    "So early detection does not merely start the clock sooner -- IT REDUCES THE NUMBER OF ESCAPES "
    "THE REGIMEN HAS TO CLOSE, which is why a regimen that fails against established disease can "
    "succeed against screen-detected disease without any increase in potency.",
    "THE CAVEAT THAT SURVIVES: the persister state and immune exhaustion are PHENOTYPIC, not "
    "mutational -- they arise at high rate and are present at essentially any burden. Early "
    "detection does not remove them, which is why the non-division-gated agent stays mandatory.",
)
