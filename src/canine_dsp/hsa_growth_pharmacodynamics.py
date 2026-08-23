"""Is the growth reduction the stack requires reachable at a tolerated dose?

`hsa_gap_stack` asks for a ~16% reduction in tumour growth rate and names beta-blockade as the
candidate. That is a requirement, not a measurement. This module turns it into a pharmacodynamic
question with real numbers on both sides: measured in vitro potency, and the plasma exposure a real
canine trial actually achieved.

See docs/HSA_DURABLE_RESPONSE.md.
"""

import numpy as np

PROPRANOLOL_MW_G_PER_MOL = 259.34  # C16H21NO2, free base

# ---------------------------------------------------------------------------------------------
# What propranolol does to vascular-tumour proliferation, measured.
PROPRANOLOL_IN_VITRO_ANTIPROLIFERATIVE = {
    "citation": "Stiles et al. 2013, PLOS ONE 8(3):e60021, PMID 23555867",
    "design": "panel of angiosarcoma and hemangioendothelioma lines, 0-200 uM propranolol, 48 h",
    "at_25_uM_proliferation_reduction": (0.15, 0.67),  # range across lines; EOMA most sensitive
    "at_100_uM": "significant cell death across all tumour lines -- cytotoxic, not cytostatic",
    "normal_endothelium": "primary HDMVECs show reduced proliferation at 50 uM, no apoptosis below "
                          "150 uM -- the selectivity window is real but sits far above 25 uM",
    "in_vivo_mouse": {"dose": "10 mg/kg intraperitoneal every 2 days",
                      "tumour_mass_reduction": 0.637, "n_treated": 17, "n_control": 15},
}

# The one in-human measurement of a proliferation change under beta-blockade in angiosarcoma.
PROPRANOLOL_CLINICAL_PROLIFERATION_SIGNAL = {
    "citation": "Chow et al. 2015, JAMA Dermatol 151(11):1226-9, PMID 26375166",
    "design": "single patient, stage T2 multifocal cutaneous angiosarcoma, propranolol 40 mg twice "
              "daily as monotherapy, proliferative index measured before and after one week",
    "proliferative_index_reduction": 0.34,
    "n": 1,
    "why_it_is_weak": "n=1, uncontrolled, and Ki-67 proliferative index is not the same quantity as "
                      "net population growth rate -- but it is the only in-vivo proliferation "
                      "readout under beta-blockade in this tumour type.",
}

# What a real canine trial achieved at the dose dogs tolerate three times a day.
PROPRANOLOL_CANINE_EXPOSURE = {
    "citation": "Borgatti et al. 2025, PMID 40386412 (PRO-DOX), plasma from 19 of 20 dogs",
    "dose_cohorts_mg_per_kg": (0.8, 1.0, 1.3),
    "schedule": "orally three times per day; 14 of 20 dogs in the 1.3 mg/kg cohort",
    "propranolol_cmax_ng_per_ml": 18.7,
    "propranolol_auc_0_24h_ng_h_per_ml": 163.7,
    "four_oh_propranolol_cmax_ng_per_ml": 13.3,
    "caveat": "total plasma concentration. Propranolol is extensively protein bound, so the free "
              "concentration a tumour cell sees is lower still, and only the S(-) enantiomer is "
              "receptor-active -- both push the comparison below in the same direction.",
}

# A different mechanism for the same drug, measured in the right species and tumour.
PROPRANOLOL_IS_NOT_ONLY_ANTIPROLIFERATIVE = {
    "citation": "Saha et al. 2021, Front Oncol 10:614288, PMID 33598432",
    "finding": "in canine hemangiosarcoma and human angiosarcoma lines, propranolol raises "
               "cytoplasmic doxorubicin by reducing lysosomal sequestration and cellular efflux",
    "receptor_independent": "the receptor-INACTIVE R-(+) enantiomer produced effects equivalent to "
                            "the receptor-active S-(-) enantiomer, so this action is not "
                            "beta-adrenergic",
    "implication": "beta-blockade is modelled here as a growth modifier, but propranolol's "
                   "best-evidenced action in canine HSA is chemosensitisation -- a multiplier on a "
                   "partner drug's kill term, not a reduction in growth rate. The two are different "
                   "model objects and only the first is what the stack asks for.",
}


def ng_per_ml_to_micromolar(ng_per_ml: float, mw_g_per_mol: float = PROPRANOLOL_MW_G_PER_MOL
                            ) -> float:
    """ng/mL -> uM. 1 ng/mL = 1 ug/L, so uM = (ug/L) / (g/mol)."""
    if ng_per_ml < 0 or mw_g_per_mol <= 0:
        raise ValueError("concentration must be nonnegative and molecular weight positive")
    return float(ng_per_ml / mw_g_per_mol)


def emax_growth_suppression(concentration_uM, ec50_uM: float, hill: float = 1.0,
                            max_suppression: float = 1.0):
    """Fraction of growth removed at a given concentration, as a Hill/Emax curve.

    Returns a value in [0, max_suppression] suitable for
    `hsa_antiproliferative.antiproliferative_schedule(suppression=...)`.
    """
    if ec50_uM <= 0 or hill <= 0:
        raise ValueError("ec50_uM and hill must be positive")
    if not 0 <= max_suppression <= 1:
        raise ValueError("max_suppression must lie in [0, 1]")
    c = np.asarray(concentration_uM, dtype=float)
    if np.any(c < 0):
        raise ValueError("concentration must be nonnegative")
    ratio = (c / ec50_uM) ** hill
    result = max_suppression * ratio / (1.0 + ratio)
    return float(result) if np.isscalar(concentration_uM) or result.ndim == 0 else result


def ec50_from_single_point(concentration_uM: float, suppression: float, hill: float = 1.0,
                           max_suppression: float = 1.0) -> float:
    """Invert the Emax curve: the EC50 implied by one measured (concentration, effect) pair."""
    if not 0 < suppression < max_suppression:
        raise ValueError("suppression must lie strictly between 0 and max_suppression")
    if concentration_uM <= 0:
        raise ValueError("concentration must be positive")
    fraction = suppression / max_suppression
    return float(concentration_uM * ((1.0 - fraction) / fraction) ** (1.0 / hill))


def concentration_for_suppression(target_suppression: float, ec50_uM: float, hill: float = 1.0,
                                  max_suppression: float = 1.0) -> float:
    """The concentration needed to remove `target_suppression` of growth. Inverse of the Emax."""
    if not 0 < target_suppression < max_suppression:
        raise ValueError("target_suppression must lie strictly between 0 and max_suppression")
    fraction = target_suppression / max_suppression
    return float(ec50_uM * (fraction / (1.0 - fraction)) ** (1.0 / hill))


# EC50s implied by the two ends of Stiles' measured 25 uM range, plus its midpoint.
_LOW, _HIGH = PROPRANOLOL_IN_VITRO_ANTIPROLIFERATIVE["at_25_uM_proliferation_reduction"]
IMPLIED_EC50_uM = {
    "least_sensitive_line": ec50_from_single_point(25.0, _LOW),
    "midpoint": ec50_from_single_point(25.0, 0.5 * (_LOW + _HIGH)),
    "most_sensitive_line": ec50_from_single_point(25.0, _HIGH),
}

# Achievable growth suppression at PRO-DOX's measured Cmax, by EC50 anchor. Recomputed in tests.
ACHIEVABLE_SUPPRESSION_AT_CANINE_CMAX = {
    "least_sensitive_line": 0.00051,
    "midpoint": 0.00200,
    "most_sensitive_line": 0.00582,
}

# Plasma concentration the stack's 16.3% would require, against what PRO-DOX measured.
EXPOSURE_GAP = {
    "required_suppression": 0.163,
    "achieved_cmax_ng_per_ml": 18.7,
    "required_cmax_ng_per_ml_midpoint_anchor": 1817.0,
    "fold_short": 97.0,
    "using_most_sensitive_line": {"required_ng_per_ml": 622.0, "fold_short": 33.0},
    "using_least_sensitive_line": {"required_ng_per_ml": 7155.0, "fold_short": 383.0},
}

VERDICT = {
    "question": "Can beta-blockade deliver the ~16% growth reduction the stack requires, at a dose "
                "a dog tolerates?",
    "answer": "No, on the in vitro anchor. Propranolol reduces vascular-tumour proliferation at "
              "25 uM and above; PRO-DOX achieved a mean Cmax of 18.7 ng/mL, which is 0.072 uM. "
              "That is roughly 350x below the lowest concentration with a measured "
              "antiproliferative effect, and the implied growth suppression is 0.05-0.6% against "
              "the 16.3% required. Reaching 16.3% would need about 97x the plasma concentration "
              "the trial achieved.",
    "the_contradicting_datum": "Chow et al. 2015 measured a 34% fall in proliferative index in a "
                               "human angiosarcoma after one week of 40 mg twice daily -- an "
                               "exposure no higher than the dogs received. Either the in vitro "
                               "threshold badly overstates what is needed in vivo, or the n=1 "
                               "observation is noise. The two anchors disagree by about two orders "
                               "of magnitude and this module does not resolve them.",
    "what_it_explains": "PRO-DOX was negative in 20 dogs. The in vitro anchor says the drug never "
                        "reached an active concentration, which is a simpler explanation than the "
                        "partner-drug hypothesis in hsa_antiproliferative -- and unlike that "
                        "hypothesis it predicts that propranolol with vinblastine would fail too.",
    "what_would_change_it": "a measured growth-rate or Ki-67 change in canine HSA at a known plasma "
                            "concentration. No such measurement exists; PRO-DOX collected the "
                            "pharmacokinetics and the tumour transcriptomes but did not report a "
                            "proliferation readout against exposure.",
    "consequence_for_the_stack": "the 16.3% requirement stands, but propranolol is not shown to "
                                 "deliver it. The growth-reduction component needs an agent whose "
                                 "achievable exposure clears its own antiproliferative EC50, and "
                                 "that is now a quantitative screening criterion rather than a "
                                 "plausibility argument.",
}
