"""Therapies that close the three OPEN escape routes in `hsa_durable_response_analysis`. That module
enumerated seven escape routes for canine hemangiosarcoma. Routes 1-3 are closed by any vaccine by
construction; route 4 (antigen/MHC-I loss) was shown to be over-weighted and closable. Three were
left OPEN and unmodelled: rupture/haemorrhage (5), vaccine failure without antigen loss (6), and
micrometastatic disease outside any modelled compartment (7). See docs/HSA_DURABLE_RESPONSE.md.
"""

import numpy as np

EBAT_REDOSING_REFUTATION = {
    "what_this_repo_proposed": "hsa_durable_response_analysis proposed closing route 4 with a "
                              "persistent mechanism-agnostic kill term, and named eBAT minus its "
                              "28-day cap as the natural supplier.",
    "citation": "Borgatti et al. 2020, Vet Comp Oncol 18(4):664-674, PMID 32187827 (SRCBST-2)",
    "what_was_actually_tried": "Three cycles of eBAT at the biologically active dose (50 ug/kg, "
                              "Mon/Wed/Fri) at a reduced interval from doxorubicin, in 25 dogs, "
                              "versus the earlier single-cycle trial that did show benefit.",
    "result": "Greater toxicity (six dogs acute hypotension, two hospitalised) and REDUCED "
             "efficacy; no statistically significant survival benefit against a contemporary "
             "standard-of-care group. More eBAT was worse than less eBAT.",
    "what_survives": "The modelled REQUIREMENT is unaffected -- a persistent agnostic kill term "
                     "at >=0.05/day still closes route 4 at 1000x the assumed antigen-loss rate.",
}

# P(no regrowth) x P(surviving an independent haemorrhage hazard). Tumour-control figure from
# hsa_vaccine_followon_scenarios at threshold potency, 5-year horizon; see the test module.
TUMOUR_CONTROL_DURABLE_5YR = 0.967


def joint_durability(tumour_control: float, annual_rupture_hazard: float, years: float = 5.0
                     ) -> dict:
    """Rupture as an independent competing risk, not a modifier of any growth margin.

    The engine reports freedom from regrowth. A dog that bleeds to death with a controlled tumour
    is a durable response by that definition and a dead dog by any other, which is why this is
    multiplicative rather than a parameter adjustment.
    """
    if not 0 <= annual_rupture_hazard <= 1:
        raise ValueError("annual_rupture_hazard must lie in [0, 1]")
    if not 0 <= tumour_control <= 1:
        raise ValueError("tumour_control must lie in [0, 1]")
    hazard_survival = (1 - annual_rupture_hazard) ** years
    return {
        "tumour_control": float(tumour_control),
        "annual_rupture_hazard": float(annual_rupture_hazard),
        "years": float(years),
        "hazard_survival": float(hazard_survival),
        "joint_durability": float(tumour_control * hazard_survival),
        "points_lost": float(tumour_control - tumour_control * hazard_survival) * 100,
    }


def screened_rupture_hazard(annual_rupture_hazard: float, screening_sensitivity: float) -> dict:
    """Early detection as a hazard multiplier: a tumour found before it ruptures is resected
    electively, so the detected fraction contributes no rupture hazard. `screening_sensitivity` is
    the real, validated CANDiD figure for this cancer class -- not an assumed screening
    performance. It is bounded by two things this function does NOT model: screening only helps if
    it happens before rupture (a test is not a schedule), and a 98.5% specificity applied to a
    low-prevalence screening population yields false positives whose cost is real and not
    represented here.
    """
    if not 0 <= screening_sensitivity <= 1:
        raise ValueError("screening_sensitivity must lie in [0, 1]")
    return {
        "unscreened_hazard": float(annual_rupture_hazard),
        "screening_sensitivity": float(screening_sensitivity),
        "residual_hazard": float(annual_rupture_hazard * (1 - screening_sensitivity)),
    }


CANDID_SCREENING = {
    "citation": "Flory et al. 2022, PLOS ONE 17(4):e0266623, PMID 35471999 -- the CANDiD study",
    "design": "international multi-centre validation, 1,358 dogs enrolled, 1,100 analysed",
    "overall_sensitivity": 0.547,
    "specificity": 0.985,
    "sensitivity_three_most_aggressive_cancers": (0.784, 0.909),
    "aggressive_group_includes_hemangiosarcoma": True,
    "presymptomatic_detections": 4,
    "why_it_closes_route_5": "Rupture hazard is a consequence of late detection, not a fixed "
                            "property of the tumour. Screening converts emergency rupture into "
                            "elective splenectomy, changing the hazard rather than treating it.",
    "limits": "A test is not a screening schedule; 98.5% specificity in a low-prevalence "
             "population still produces false positives, whose cost is not modelled here.",
}

RUPTURE_CANDIDATES = [
    {
        "id": "5a", "therapy": "Yunnan Baiyao +/- epsilon-aminocaproic acid",
        "verdict": "FAILED IN A REAL TRIAL -- do not model as a closure",
        "citation": "Murphy et al. 2017, J Vet Emerg Crit Care 27(1):121-126, PMID 27669112",
        "evidence": "16 dogs YB alone, 8 YB+EACA, 43 controls, all with right atrial masses and "
                    "pericardial effusion.",
        "in_vitro_contrast": "Yunnan Baiyao does kill canine HSA cell lines via caspase-mediated "
                            "apoptosis (Wirth et al. 2016, Vet Comp Oncol 14(3):281-94, PMID "
                            "24976212) -- a clean example of in vitro activity not transferring.",
    },
    {
        "id": "5b", "therapy": "Hypofractionated IMRT + vinblastine + propranolol (cardiac site)",
        "verdict": "REAL, POSITIVE, SMALL -- direct readout on the failure mode",
        "citation": "Moirano et al. 2023, Vet Radiol Ultrasound 64(6):1099-1102, PMID 37800663",
        "evidence": "Seven dogs with right atrial tumours.",
        "limits": "Seven dogs, retrospective, no control arm, and it addresses the cardiac site "
                 "only -- splenic rupture is a different compartment.",
    },
    {
        "id": "5c", "therapy": "Liquid-biopsy screening -> elective splenectomy",
        "verdict": "STRONGEST LEVER -- changes the hazard rather than treating its consequence",
        "citation": "Flory et al. 2022, PLOS ONE 17(4):e0266623, PMID 35471999",
        "evidence": "78.4-90.9% sensitivity for the three most aggressive canine cancers, a group "
                   "including hemangiosarcoma; 98.5% specificity; four presymptomatic detections.",
        "limits": "See CANDID_SCREENING['limits'].",
    },
]

VACCINE_TAKE = {
    "route": "6 -- vaccine failure without antigen loss",
    "modelled_as": "a take rate: the fraction of dogs mounting any response. Non-takers receive "
                  "exactly the no-vaccine outcome.",
    "population_durable_by_take_rate": {1.0: 0.967, 0.8: 0.833, 0.6: 0.699, 0.4: 0.565},
    "points_of_durability_per_10_points_of_take": 6.7,
    "why_it_matters": "After vaccine potency itself this is the largest lever in the model, and "
                     "unlike potency it is directly measurable in a running trial.",
    "candidates": [
        {
            "id": "6a", "therapy": "Canine anti-PD-L1 antibody (c4G12 class)",
            "hsa_specific_mechanism": "Canine HSA induces M2 polarisation and PD-L1 expression in "
                                     "tumour-associated macrophages, and HSA tumours with PD-L1+ "
                                     "macrophages contained FEWER T-cells than those with PD-L1- "
                                     "macrophages (Gulay et al. 2022, Sci Rep 12(1):2124, PMID "
                                     "35136176). Route 6 with a named mechanism, in this disease.",
            "therapy_evidence": "c4G12 in 29 dogs with pulmonary metastatic oral malignant "
                               "melanoma: median survival 143 d vs 54 d historical control; 1/13 "
                               "complete response among measurable disease; any-grade "
                               "treatment-related AEs in 51.7% (Maekawa et al. 2021, NPJ Precis "
                               "Oncol 5(1):10, PMID 33580183).",
            "limits": "Never given for hemangiosarcoma; melanoma comparison is against "
                      "historical controls.",
        },
        {
            "id": "6b", "therapy": "Measure the take -- an immune endpoint powered for outcome",
            "rationale": "Neither real HSA vaccine trial powered an analysis of whether immune "
                         "responders survived longer than non-responders.",
            "note": "A trial-design closure, not a drug -- and the cheapest item in this module.",
        },
    ],
}

SECOND_COMPARTMENT = {
    "route": "7 -- disease already outside the resected compartment",
    "how_often": "22% of liver lesions found at surgery had been missed on preoperative "
                "ultrasound, across 99 dogs with non-traumatic haemoperitoneum from splenic "
                "tumour rupture (Ramirez et al. 2024, JAVMA 262(11):1499-1503, PMID 39111340).",
    "closure": "No new agent. `run_monte_carlo_two_compartment` -- built for the histiocytic "
              "sarcoma work and never called by HSA -- shows the vaccine already reaches it.",
    "with_systemic_persistent_agent": {0.0: 1.000, 0.3: 1.000, 0.6: 1.000},
    "nodal_relapses_with_agent": 0,
    "vaccine_off": {0.0: 0.340, 0.6: 0.325},
    "nodal_relapses_vaccine_off_at_0_6": 46,
    "interpretation": "Surgery structurally cannot reach the second compartment; a systemic "
                     "persistent mechanism reaches it exactly as well as the first. This is the "
                     "sharpest argument for the vaccine in the whole analysis.",
    "backstop_if_the_vaccine_does_not_take": {
        "id": "7b", "therapy": "Metronomic oral chemotherapy (cyclophosphamide/etoposide/piroxicam)",
        "citation": "Lana et al. 2007, J Vet Intern Med 21(4):764-9, PMID 17708397",
        "evidence": "Nine dogs with stage II splenic HSA: median overall survival AND median "
                   "disease-free interval both 178 d, against 133 d and 126 d for 24 dogs on "
                   "conventional doxorubicin.",
        "limits": "Nine dogs, non-randomised, retrospective comparator.",
    },
}

CLOSURE_SUMMARY = [
    {"route": 5, "name": "Rupture / haemorrhage",
     "status": "PARTIALLY CLOSED", "best_lever": "5c liquid-biopsy screening",
     "note": "No pharmacological closure exists -- the one agent tried failed. Screening changes "
            "the hazard; radiotherapy treats one site. Still the most dangerous open route."},
    {"route": 6, "name": "Vaccine failure without antigen loss",
     "status": "CLOSABLE, WITH A REAL MECHANISM AND A REAL AGENT",
     "best_lever": "6a anti-PD-L1, selected by PD-L1 IHC; 6b measure the take",
     "note": "The only route whose mechanism has been measured in canine HSA specifically."},
    {"route": 7, "name": "Disease outside the resected compartment",
     "status": "CLOSED BY THE REGIMEN ALREADY PROPOSED",
     "best_lever": "the vaccine itself; metronomic chemotherapy as backstop",
     "note": "Needs no new agent. Proven by running HSA through an engine function it never used."},
]
