"""The HSA closure as a DECIDABLE CONJUNCTION, per `CLAUDE.md` rule 12.

The user: *"I don't want odds of achieving 10 years, the whole point about looking at all mechanisms
and escapes is to not leave it to odds."*

A probability is the right output only when the failure modes are unenumerated. Enumerating them is
what makes the question decidable. So the headline is this module's `conjunction()` -- every route
CLOSED or OPEN **at each anatomical site**, plus the finite list of conditions and each one's status.
The durability figures elsewhere in this analysis (0.888, 0.830, 0.966, 0.992) are SENSITIVITY
statements and must never be quoted as the verdict; `odds_are_secondary()` says why.

WHAT THE SITE DIMENSION EXPOSED
-------------------------------
Reporting a single durability number averages over anatomical compartments. Splitting by site showed
that **two routes previously reported as closed are open in the central nervous system**, because
their closing agents do not cross the blood-brain barrier:

  * route 8 (antigen-null AND drug-resistant) was closed by doxorubicin + eBAT. Neither reaches the
    CNS.
  * route 12 (a clone at the intrinsic-growth ceiling) was closed by the MEK + TORC1/2 combination
    arresting it while the vaccine clears it. The combination does not reach the CNS either, so the
    vaccine would have to hold a ceiling-rate clone alone, which needs 3.0-3.9x.

This analysis said "every escape path has a closure" without the site qualifier. That was wrong, and
the odds-based headline is what hid it. A candidate closure for both cells is named below.

See docs/HSA_DURABLE_RESPONSE.md and docs/HSA_STATUS.md.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

CLOSED = "CLOSED"
OPEN = "OPEN"
NOT_APPLICABLE = "N/A"

MEASURED = "measured"
DERIVED = "derived from measured parameters"
TRANSFERRED = "transferred from another population"
ASSUMED = "assumed"


class Site(Enum):
    """Anatomical compartments a residual hemangiosarcoma cell can occupy."""

    SPLEEN = "spleen (resected)"
    PERITONEUM = "peritoneum / omentum"
    LIVER = "liver"
    LUNG = "lung"
    HEART = "heart / pericardium"
    CNS = "central nervous system"


# =================================================================================================
# WHICH MECHANISMS REACH WHICH SITES. This is the table the single-number headline suppressed.
# =================================================================================================

# True = the mechanism acts on a cell in that site at a therapeutically relevant level.
REACH: dict[str, dict[Site, bool]] = {
    "surgery": {Site.SPLEEN: True, Site.PERITONEUM: False, Site.LIVER: False,
                Site.LUNG: False, Site.HEART: False, Site.CNS: False},
    "vaccine_T_cell_arm": {s: True for s in Site},
    "vaccine_antibody_arm": {**{s: True for s in Site}, Site.CNS: False},
    "doxorubicin": {**{s: True for s in Site}, Site.CNS: False},
    "eBAT": {**{s: True for s in Site}, Site.CNS: False},
    "losartan": {**{s: True for s in Site}, Site.CNS: False},
    "anti_PD_1": {s: True for s in Site},          # acts on T cells systemically; CNS activity shown
    "MEK_plus_TORC1_2": {**{s: True for s in Site}, Site.CNS: False},
    # CNS-penetrant alkylators. Promoted from candidate to credited once evidence was found that
    # (a) lomustine has already been given to dogs with stage II splenic HSA in this exact adjuvant
    # setting, alternating with the anthracycline, and (b) temozolomide has angiosarcoma-specific
    # CNS response evidence. Both are alkylating agents, so they are independent of the vaccine
    # antigen and of the PI3K/MAPK axis by mechanism -- which is what these cells require.
    "lomustine": {**{s: True for s in Site}, Site.CNS: True},
    "temozolomide": {**{s: True for s in Site}, Site.CNS: True},
    # Brain-directed stereotactic radiotherapy: maximal reach, but only to a deposit you can SEE.
    # Useless against occult CNS seeding, which is what routes 8 and 12b describe, so it is kept
    # out of closed_by and recorded as covering detected deposits only.
    "brain_SRT": {**{s: False for s in Site}, Site.CNS: True},
}

REACH_BASIS = {
    "vaccine_T_cell_arm": "activated T cells cross the blood-brain barrier as ordinary immune "
                          "surveillance; central memory T cells enter CSF via the choroid plexus. "
                          "TRANSFERRED (human/rodent immunology, not canine HSA).",
    "vaccine_antibody_arm": "a monoclonal antibody reaches ~0.1% of serum concentration in CSF. "
                            "This is why ERstrePs (humoral AND T-cell) and eVim (antibody vs "
                            "surface vimentin) are NOT interchangeable.",
    "doxorubicin": "P-glycoprotein substrate, effectively excluded from the CNS.",
    "eBAT": "a ~55 kDa bispecific protein toxin; does not cross.",
    "losartan": "deliberately not CNS-penetrant.",
    "anti_PD_1": "checkpoint inhibitors are documented to have CNS activity DESPITE poor "
                 "penetration, because the antibody acts on T cells systemically and the T cells "
                 "do the crossing.",
    "MEK_plus_TORC1_2": "trametinib is a P-gp/BCRP substrate with limited CNS exposure; the "
                        "combination's measured arrest was in a subcutaneous tumorgraft.",
    "lomustine": "a lipophilic nitrosourea that crosses the blood-brain barrier and is used for "
                 "canine intracranial disease. Critically for this plan, it has ALREADY been given "
                 "to dogs with stage II splenic hemangiosarcoma after splenectomy, ALTERNATING "
                 "WITH AN ANTHRACYCLINE -- the exact setting, sequence and backbone proposed here "
                 "(Moore, Rassnick & Frimberger 2017, JAVMA 251(5):559-565, PMID 28828962, "
                 "doi 10.2460/javma.251.5.559; 30 dogs, median survival 158 d, 1-year 16%; in the "
                 "low-mitotic-rate subgroup n=9, median 292 d and 1-year 42%). It is an alkylating "
                 "agent, so it is independent of the vaccine antigen and of the PI3K/MAPK axis by "
                 "mechanism. Duration: cumulative hepatotoxicity caps total exposure near "
                 "350 mg/m2, so at 50-110 mg/m2 per cycle this is strictly a FINITE-COURSE "
                 "log-remover (~3-5 cycles) and NOT a chronic floor-holder -- which is exactly the "
                 "shape routes 8 and 12b need.",
    "temozolomide": "an oral blood-brain-barrier-penetrant alkylating agent with "
                    "ANGIOSARCOMA-SPECIFIC CNS evidence, which lomustine lacks: a primary cerebral "
                    "angiosarcoma resolved on concurrent chemoradiotherapy with temozolomide "
                    "(PMID 37811120, doi 10.1097/MS9.0000000000001158), and a breast angiosarcoma "
                    "with skull-base and dural metastasis achieved a durable response on "
                    "anlotinib + temozolomide after multimodal failure, a report that explicitly "
                    "frames the strategy as leveraging CNS-penetrating agents against "
                    "sanctuary-site angiosarcoma (PMID 42125685, doi 10.3389/fonc.2026.1619754). "
                    "Mechanistic support: PARP1 is expressed in 46/47 angiosarcoma samples and "
                    "SLFN11 in 80%, and olaparib + temozolomide is synergistic in angiosarcoma "
                    "cell lines (PMID 34085099, doi 10.1007/s00432-021-03678-4).",
    "brain_SRT": "maximal CNS reach and fully mechanism-independent, but it can only treat a "
                 "deposit that has been imaged. Routes 8 and 12b describe OCCULT seeding, so SRT "
                 "is deliberately excluded from closed_by and recorded as covering detected "
                 "deposits only.",
}


def reaches(mechanism: str, site: Site) -> bool:
    if mechanism not in REACH:
        raise ValueError(f"unknown mechanism {mechanism!r}; expected one of {sorted(REACH)}")
    return REACH[mechanism][site]


# =================================================================================================
# THE ROUTE LEDGER. Each route names the mechanisms that close it; a route is CLOSED at a site only
# if at least one of its closing mechanisms reaches that site.
# =================================================================================================

@dataclass(frozen=True)
class Route:
    number: str
    name: str
    closed_by: tuple[str, ...]          # any ONE of these suffices
    grade: str
    note: str = ""
    site_independent: bool = False      # host-level, not a property of a tumour deposit


ROUTES: tuple[Route, ...] = (
    Route("1", "PI3K/AKT feedback reactivation", ("vaccine_T_cell_arm", "vaccine_antibody_arm"),
          DERIVED, "resistance to a drug does not change what the immune system was trained to see"),
    Route("2", "MAPK crosstalk bypass", ("vaccine_T_cell_arm", "vaccine_antibody_arm"), DERIVED),
    Route("3", "target-site mutation", ("vaccine_T_cell_arm", "vaccine_antibody_arm"), DERIVED,
          "also sets the bar; bounded above by the no-drug ceiling at +6.8%"),
    Route("4", "antigen / MHC-I loss", ("vaccine_antibody_arm", "anti_PD_1"), TRANSFERRED,
          "eVim's target needs no MHC; MHC-loss variants upregulate NKG2D ligands"),
    Route("5", "rupture / haemorrhage", ("surgery",), TRANSFERRED,
          "closed by screening converting an emergency into an elective splenectomy. "
          "INTRACRANIAL haemorrhage is a separate lethal event no component treats"),
    Route("6", "vaccine failure without antigen loss", ("anti_PD_1", "losartan"), TRANSFERRED),
    Route("7", "disease outside the resected compartment",
          ("vaccine_T_cell_arm", "vaccine_antibody_arm"), MEASURED,
          "22% of liver lesions found at surgery were missed on pre-op ultrasound"),
    Route("8", "antigen inadequacy on day zero (antigen-null AND drug-resistant)",
          ("doxorubicin", "eBAT", "lomustine", "temozolomide"), TRANSFERRED,
          "~1,300 cells needing 7.2 logs; doxorubicin 3.1-5.1 plus one early eBAT cycle 5.2-7.8"),
    Route("9", "anatomical sanctuary", ("vaccine_T_cell_arm", "anti_PD_1"), TRANSFERRED,
          "HSA is the largest single source of secondary brain tumours in dogs, 51/177"),
    Route("10", "host immunosenescence", ("vaccine_T_cell_arm",), TRANSFERRED,
          "attacks the PRIMARY response; memory is spared, and re-dosing is the documented fix",
          site_independent=True),
    Route("12a", "clonal evolution to a new RESISTANCE driver",
          ("vaccine_T_cell_arm", "vaccine_antibody_arm"), DERIVED,
          "bounded by the no-drug ceiling: at most +6.8% on the bar, costing one rung"),
    Route("12b", "a clone at the intrinsic-growth ceiling",
          ("MEK_plus_TORC1_2", "lomustine", "temozolomide"), TRANSFERRED,
          "the drug arrests it at net zero and the vaccine clears it; needs an agent PRESENT at the "
          "site, because the vaccine alone would need 3.0-3.9x"),
    Route("13", "dormancy / quiescence", ("vaccine_T_cell_arm", "vaccine_antibody_arm"), TRANSFERRED,
          "immune killing is not growth-dependent"),
    Route("14", "B2M / TAP loss", ("vaccine_antibody_arm", "anti_PD_1"), TRANSFERRED,
          "the strongest case for the missing-self backup"),
    Route("15", "Tregs and MDSCs", ("losartan", "eBAT", "anti_PD_1"), TRANSFERRED,
          "CCR2 recruitment and uPAR+ myeloid depletion; COX-2 inhibition for the Treg axis"),
)


def route_status(route: Route, site: Site) -> str:
    """CLOSED at this site iff at least one closing mechanism reaches it.

    Two special cases, both about route 5. Splenic rupture is a property of the primary organ, so
    it is NOT APPLICABLE at a distant deposit rather than open there -- scoring it OPEN at the lung
    would be counting one hazard five times. The CNS is the exception: a vascular brain metastasis
    can haemorrhage, and nothing in this plan treats that, so it is genuinely OPEN there.
    """
    if route.site_independent:
        return CLOSED
    if route.number == "5":
        if site is Site.SPLEEN:
            return CLOSED                 # screening converts emergency rupture to elective surgery
        if site is Site.CNS:
            return OPEN                   # intracranial haemorrhage: no treating component
        return NOT_APPLICABLE
    return CLOSED if any(reaches(m, site) for m in route.closed_by) else OPEN


def conjunction() -> dict:
    """THE HEADLINE. Every route, at every site, CLOSED or OPEN -- and what is open.

    This is the output to quote. It is decidable: no probability appears in it.
    """
    matrix = {r.number: {s.value: route_status(r, s) for s in Site} for r in ROUTES}
    open_cells = [(r.number, r.name, s.value)
                  for r in ROUTES for s in Site if route_status(r, s) == OPEN]
    return {
        "matrix": matrix,
        "sites": [s.value for s in Site],
        "routes": len(ROUTES),
        "open_cells": open_cells,
        "all_closed": not open_cells,
        "verdict": (
            "every route CLOSED at every site"
            if not open_cells else
            f"{len(open_cells)} route-site cell{'s' if len(open_cells) != 1 else ''} OPEN, "
            f"all in the {Site.CNS.value}: "
            + ", ".join(f"route {n}" for n, _, _ in open_cells)
        ),
    }


# =================================================================================================
# THE FINITE CONDITION LIST. Rule 12 requires the conditions and each one's status, not a number.
# =================================================================================================

@dataclass(frozen=True)
class Condition:
    what: str
    on_which_routes: tuple[str, ...]
    status: str
    how_to_settle: str


CONDITIONS: tuple[Condition, ...] = (
    Condition("the vaccine platform must have a T-cell arm", ("1", "2", "3", "7", "9", "10", "13"),
              "SELECTABLE NOW -- ERstrePs qualifies, eVim does not",
              "choose the platform; no experiment needed"),
    Condition("vaccine height must reach ~1.40x measured (1.50x at the conservative bar)",
              ("1", "2", "3", "7", "12b"),
              "TRANSFERRED -- four levers, one randomised anchor in the matched setting",
              "five-arm growth-rate readout in ISOS-1; run the eBAT arm first"),
    Condition("the route-8 compartment must be anthracycline-sensitive", ("8",),
              "UNEXAMINED, not contradicted",
              "sequence the antigen locus and resistance loci in the drug-tolerant fraction"),
    Condition("the route-8 compartment must exist at all", ("8",),
              "UNVERIFIED -- nobody has looked",
              "stain HSA for the vaccine antigen before and after PI3K/mTOR inhibition"),
    Condition("a CNS-penetrant, antigen- and pathway-independent agent must be added",
              ("8", "12b"),
              "MET at TRANSFERRED -- lomustine (already given in canine stage II splenic HSA "
              "alternating with the anthracycline) and temozolomide (angiosarcoma-specific CNS "
              "response evidence). Neither needs a new molecule. UNQUANTIFIED on logs delivered "
              "against these compartments",
              "measure alkylator log-kill against the antigen-null drug-tolerant fraction; and "
              "note the lomustine trial's OVERALL survival was not better than the anthracycline "
              "alone, so this buys REACH, not potency"),
    Condition("immunity half-life must support the booster interval", ("1", "2", "3", "7"),
              "FAILS the stated bar -- a bare assumption, and the answer swings on it",
              "serial immune monitoring on an existing vaccinated cohort"),
    Condition("the post-remission rupture hazard must be bounded", ("5",),
              "FAILS the stated bar -- swept with no anchor",
              "follow a screened cohort; this is the one number screening policy turns on"),
    Condition("intracranial haemorrhage has no treating component", ("5",),
              "OPEN and unaddressed -- a competing event, not a cancer-control failure",
              "nothing in this plan; it belongs with the rupture hazard"),
)


def failing_conditions() -> list[Condition]:
    return [c for c in CONDITIONS if c.status.startswith(("OPEN", "FAILS"))]


# =================================================================================================
# WHY THE ODDS ARE NOT THE VERDICT.
# =================================================================================================

def odds_are_secondary() -> dict:
    """Rule 12: the durability figures are a sensitivity statement, never the headline."""
    return {
        "the_users_instruction": "I don't want odds of achieving 10 years, the whole point about "
                                 "looking at all mechanisms and escapes is to not leave it to odds.",
        "why_a_probability_is_the_wrong_output_here": "a probability is right when the failure modes "
                                                      "are unenumerated. Enumerating them is what "
                                                      "makes the question decidable -- so producing "
                                                      "a number after enumerating them throws away "
                                                      "the work.",
        "what_the_number_hid_in_this_analysis": "a single durability figure averages over anatomical "
                                               "compartments. 0.830 for the route-8 closure is an "
                                               "average over sites in which doxorubicin and eBAT are "
                                               "present. In the CNS they are absent and the cell is "
                                               "OPEN. The conjunction shows that; the average does "
                                               "not.",
        "what_the_numbers_are_still_good_for": "sensitivity. 'The requirement is a ramp not a cliff', "
                                               "'the bar moves 7% from full dose to no drug', and "
                                               "'0.966-1.000 across four orders of magnitude of "
                                               "seeding' are all statements about how hard a "
                                               "conclusion is to break. That is their proper use.",
        "the_rule": "quote conjunction(). Never quote a durability figure as the verdict.",
    }


VERDICT = {
    "headline": "Of 15 routes across 6 anatomical sites, ONE cell is OPEN: route 5 in its CNS form "
                "-- intracranial haemorrhage from a vascular brain metastasis, which no component "
                "of this plan treats. Every other route is CLOSED at every site.",
    "how_the_cns_cells_closed": "routes 8 and 12b were open in the CNS because doxorubicin, eBAT "
                                "and the MEK + TORC1/2 combination do not cross the blood-brain "
                                "barrier. Two CNS-penetrant alkylators close them, and between "
                                "them they cover each other's weakness: LOMUSTINE has been given "
                                "to dogs with stage II splenic hemangiosarcoma after splenectomy "
                                "alternating with an anthracycline -- same species, same disease, "
                                "same setting, different compartment -- and TEMOZOLOMIDE has "
                                "angiosarcoma-specific CNS response evidence -- same tumour type, "
                                "same compartment, different species. Both are alkylating agents, "
                                "so antigen- and pathway-independence follows from mechanism.",
    "what_this_does_NOT_claim": "that lomustine improves survival in this disease. The 30-dog "
                                "trial's overall median (158 days) was not better than the "
                                "anthracycline alone. What it establishes is DELIVERABILITY and "
                                "REACH in the right setting -- the same thing the eBAT trial "
                                "establishes for the systemic compartment. The number of logs "
                                "either alkylator removes from the antigen-null drug-tolerant "
                                "fraction is UNMEASURED.",
    "the_duration_constraint_that_shapes_the_regimen": "lomustine's cumulative hepatotoxicity caps "
                                                       "total exposure near 350 mg/m2, which at "
                                                       "50-110 mg/m2 per cycle is roughly 3-5 "
                                                       "cycles. So it is strictly a finite-course "
                                                       "log-remover and cannot be a chronic "
                                                       "floor-holder. That is the shape routes 8 "
                                                       "and 12b need, and it is the same shape the "
                                                       "eBAT closure takes -- one short early "
                                                       "course, not maintenance.",
    "what_remains_open_and_why_it_is_not_a_cancer_control_failure": "intracranial haemorrhage. It "
        "belongs with splenic rupture as a COMPETING EVENT: the cancer-control ledger can be "
        "complete while a dog still dies of bleeding into a vascular brain deposit. Nothing in "
        "this plan treats it, and the honest counterpart to the splenic screening answer would be "
        "CNS imaging in the surveillance protocol -- which is a detection measure, not a drug.",
    "brain_SRT_is_deliberately_not_credited": "it has maximal CNS reach and is fully "
                                              "mechanism-independent, but it can only treat an "
                                              "imaged deposit. Routes 8 and 12b describe OCCULT "
                                              "seeding, so crediting SRT against them would be "
                                              "crediting a mechanism against a target it cannot "
                                              "find. It covers detected deposits only.",
}
