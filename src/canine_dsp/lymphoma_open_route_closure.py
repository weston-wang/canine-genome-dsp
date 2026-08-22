"""Therapies and levers that close the OPEN escape routes in `lymphoma_durable_response_analysis`.

Routes 1-3 (chemoresistance) are closed by any CD20 effector by construction; route 4 (antigen
loss) is closable with a tandem construct (see `lymphoma_gap_closure`). This module handles the
three that were left OPEN: the CNS sanctuary (5), immunotherapy failure without antigen loss (6),
and the treatment-related mortality of the curative consolidation (7) -- plus the T-cell case, which
is harder on both the bar and the antigen. See docs/LYMPHOMA_DURABLE_RESPONSE.md.
"""

import numpy as np

# --- Route 5: the CNS sanctuary. The reason the two-compartment engine gained a penetration knob.
# run_monte_carlo_two_compartment with a sanctuary_penetration_multiplier < 1 on the second
# compartment, 30% CNS-involvement, 5-year horizon. Chemo-only: as CNS drug penetration falls, the
# sanctuary becomes the dominant relapse site (nodal relapses climb from 20 to ~90). With a CD20
# effector at the bar (0.09) layered on -- and NOT penetration-discounted, because a cellular
# effector traffics on its own -- CNS relapse collapses to ~0 at every penetration level.
# Recomputed by the test module.
CNS_SANCTUARY_CHEMO_ONLY = {
    1.00: {"durable": 0.207, "cns_relapses": 20},
    0.30: {"durable": 0.207, "cns_relapses": 80},
    0.15: {"durable": 0.167, "cns_relapses": 91},
    0.05: {"durable": 0.170, "cns_relapses": 83},
}
CNS_SANCTUARY_WITH_IMMUNOTHERAPY = {
    1.00: {"durable": 0.983, "cns_relapses": 0},
    0.30: {"durable": 0.973, "cns_relapses": 3},
    0.15: {"durable": 0.963, "cns_relapses": 1},
    0.05: {"durable": 0.973, "cns_relapses": 0},
}
CNS_SANCTUARY = {
    "route": "5 -- disease in a pharmacologic sanctuary the drug cannot reach",
    "mechanism": "The blood-brain barrier excludes most CHOP cytotoxics (doxorubicin especially), "
                 "so a CNS clone sees a fraction of systemic exposure and regrows there.",
    "the_finding": "Under chemotherapy, lowering CNS drug penetration turns the sanctuary into the "
                   "dominant relapse site. A systemic CD20 effector reaches it regardless of drug "
                   "penetration and closes it -- the single sharpest argument for immunotherapy "
                   "over chemotherapy intensification, and the one thing dose escalation "
                   "structurally cannot do.",
    "real_grounding": "CNS is a recognised sanctuary and relapse site; human CAR-T has documented "
                      "CNS activity. The specific penetration fractions here are illustrative and "
                      "swept, not measured for the actual CHOP drugs in dogs.",
    "the_asymmetry_is_the_point": "Modelled as a separate compartment with discounted drug but "
                                  "full immune access, not as lower overall exposure -- because the "
                                  "whole claim is that one modality is excluded and the other is not.",
}

# --- Route 6: immunotherapy failure without antigen loss -> a take rate. The fraction of dogs whose
# CD20 effector actually reaches its potency (manufacturing/expansion succeeded, no exhaustion, no
# excluding microenvironment). Non-takers get the no-immunotherapy outcome. This is a lever that is
# directly measurable in a running trial, unlike the kill rate itself.
VACCINE_TAKE = {
    "route": "6 -- the effector never reaches potency in a given dog",
    "modelled_as": "a take rate applied to the threshold-clearing durable fraction; non-takers "
                   "revert to the chemo-only outcome (~0.18-0.25).",
    "levers": [
        "measure MRD response as the read-out of take (Aresu et al. 2014, PMID 24698669; Sato et "
        "al. 2016, PMID 27339366) -- a dog whose MRD clears took the effector, one whose does not "
        "did not, and that is knowable within weeks rather than from a survival curve",
        "checkpoint blockade or lymphodepletion to raise the take rate, as in human CAR-T",
    ],
    "why_it_matters": "After potency itself, take rate is the largest lever on the population "
                      "durable fraction, and it is the cheapest to measure.",
}


def take_weighted_durable(threshold_durable: float, chemo_only_durable: float,
                          take_rate: float) -> float:
    """Population durable response when only `take_rate` of dogs mount the threshold-clearing
    effector and the rest get the chemo-only outcome. Linear in take rate."""
    if not 0.0 <= take_rate <= 1.0:
        raise ValueError("take_rate must lie in [0, 1]")
    return float(take_rate * threshold_durable + (1 - take_rate) * chemo_only_durable)


# --- Route 7: treatment-related mortality of the curative consolidation -> a competing hazard.
# Transplant cures dogs and kills dogs. The tumour-control figure and the TRM hazard multiply,
# exactly as rupture did for HSA: a durable tumour response in a dog that dies of transplant sepsis
# is not a cure.
def joint_survival(tumour_control: float, annual_trm_hazard: float, years: float = 5.0) -> dict:
    """Tumour control x survival of an independent treatment-related-mortality hazard."""
    if not 0 <= annual_trm_hazard <= 1:
        raise ValueError("annual_trm_hazard must lie in [0, 1]")
    if not 0 <= tumour_control <= 1:
        raise ValueError("tumour_control must lie in [0, 1]")
    hazard_survival = (1 - annual_trm_hazard) ** years
    return {
        "tumour_control": float(tumour_control),
        "annual_trm_hazard": float(annual_trm_hazard),
        "years": float(years),
        "hazard_survival": float(hazard_survival),
        "joint": float(tumour_control * hazard_survival),
    }


# Tumour control anchored to the CD20-effector-at-the-bar 10-year figure (0.970); TRM hazards from
# the real in-hospital mortality (7% one-centre 94-dog series; 8-13% in the smaller cohorts).
TRANSPLANT_TRM = {
    "tumour_control": 0.970,
    "annual_trm_hazard_sweep": [0.0, 0.07, 0.13],
    "joint_5yr_by_hazard": {0.0: 0.970, 0.07: 0.675, 0.13: 0.483},
    "real_mortality": "7% died before discharge across 94 transplants (Benedict et al. 2024, PMID "
                      "38695516); 8.3% (B-cell) and 13% (T-cell) in-hospital in the cohort studies "
                      "(Willcox et al. 2012, PMID 22882500; Warry et al. 2014, PMID 24467413).",
    "interpretation": "The consolidation's own mortality is the largest single subtraction from a "
                      "curative regimen's real-world success. It is the price of the one lever with "
                      "documented cures, and lowering it (reduced-intensity conditioning, better "
                      "infection prophylaxis) is a durability lever in its own right.",
}


# --- The lever that is only a timing lever: MRD-guided early re-treatment. Detecting relapse at MRD
# level and re-treating at low burden does NOT by itself improve durability -- burden changes where
# a clone starts, not the sign of its growth margin, so with a sub-threshold effector the durable
# fraction is flat across a 6x change in intervention burden. MRD's value is in deciding WHEN to
# deploy a bar-clearing mechanism (and in reading out take), not in substituting for one. Same role
# surgery/debulking played for HSA. Recomputed by the test module.
MRD_TIMING_IS_NOT_DURABILITY = {
    "durable_by_intervention_burden_immuno_0_06_10yr": {0.30: 0.240, 0.15: 0.247, 0.05: 0.240},
    "interpretation": "Early detection is a timing and take-readout lever, not a durability "
                      "mechanism. Re-treating a P-glycoprotein clone at low burden with the same "
                      "effluxed drugs still fails; MRD tells you when to act and whether the "
                      "effector took, but the mechanism you deploy still has to clear the bar.",
    "real_grounding": "PARR out-predicts flow cytometry for time to relapse and RT-qPCR reaches ~1 "
                      "malignant cell in 10,000 (Aresu et al. 2014, PMID 24698669; Sato et al. "
                      "2016, PMID 27339366).",
}


# --- The T-cell case: harder on both the bar and the antigen. Higher growth raises the bar, so the
# same immune potency that reaches durable response for B-cell (0.09) is sub-threshold for T-cell
# (0.380); only 0.12 reaches 1.000. And CD20 is a B-cell antigen -- T-cell lymphoma is CD20-negative,
# so the CD20 effector does not even apply and a different target (e.g. CD5, CD52) is required. The
# T-cell immunotherapy sweep below is therefore hypothetical-target, recorded to show the bar is
# higher, NOT a claim that CD20 immunotherapy treats T-cell disease.
T_CELL_IS_HARDER = {
    "immunotherapy_sweep_10yr": {0.0: 0.267, 0.03: 0.227, 0.06: 0.230, 0.09: 0.380, 0.12: 1.000},
    "chemo_only_10yr": 0.177,
    "two_reasons_it_is_harder": [
        "the bar is higher: faster growth means the same effector potency that cures B-cell (0.09) "
        "leaves T-cell at 0.38; it takes 0.12 to reach durable response",
        "CD20 is a B-cell antigen -- T-cell lymphoma is CD20-negative, so the entire CD20 "
        "immunotherapy route does not apply and a T-cell-directed effector (CD5/CD52) is required, "
        "which is far less developed in dogs",
    ],
    "the_antigen_caveat": "The sweep above assumes a hypothetical equally-potent T-cell-directed "
                          "effector exists; it does not model CD20 immunotherapy against T-cell "
                          "disease, which would be a category error.",
    "real_grounding": "T-cell immunophenotype is a consistent negative prognostic factor "
                      "(Curran & Thamm 2015, PMID 26279153; Mutz et al. 2013, PMID 23786518; "
                      "Saba et al. 2020, PMID 32346934).",
}

CLOSURE_SUMMARY = [
    {"route": 5, "name": "CNS sanctuary",
     "status": "CLOSED by immunotherapy (needs the two-compartment penetration upgrade)",
     "best_lever": "a systemic CD20 effector, which reaches the sanctuary the drug cannot",
     "note": "The sharpest argument for immunotherapy over dose escalation."},
    {"route": 6, "name": "Immunotherapy failure without antigen loss",
     "status": "MEASURABLE, WITH REAL READ-OUTS",
     "best_lever": "MRD response as the take read-out; lymphodepletion/checkpoint to raise take",
     "note": "The largest lever after potency, and the cheapest to measure."},
    {"route": 7, "name": "Treatment-related mortality of the consolidation",
     "status": "AN INDEPENDENT COMPETING HAZARD, PARTLY REDUCIBLE",
     "best_lever": "reduced-intensity conditioning; infection prophylaxis",
     "note": "The real 7-13% in-hospital mortality is the biggest subtraction from a curative "
             "regimen's real success."},
]
