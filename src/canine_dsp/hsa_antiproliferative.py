"""Antiproliferative agents in canine HSA: the real trial record, and a back-test against it.

See docs/HSA_DURABLE_RESPONSE.md.
"""

import numpy as np

# Every growth-directed agent with a real canine splenic-HSA readout. Four of the five are
# negative or uncontrolled, and all five were given WITHOUT a vaccine.
CANINE_ANTIPROLIFERATIVE_TRIALS = [
    {
        "agent": "toceranib (VEGFR/PDGFR/KIT inhibitor)",
        "citation": "Gardner et al. 2015, BMC Vet Res 11:131, PMID 26062540",
        "design": "43 dogs enrolled, 31 reached toceranib maintenance after splenectomy + 5 cycles "
                  "doxorubicin; stage I-II splenic HSA",
        "median_dfi_days": 161, "median_os_days": 172,
        "verdict": "NEGATIVE -- 'does not improve either disease free interval or overall survival'",
    },
    {
        "agent": "propranolol (beta-adrenergic antagonist) + doxorubicin",
        "citation": "Borgatti et al. 2025, PMID 40386412 (PRO-DOX)",
        "design": "phase I, 20 dogs, stage 1-2 splenic HSA",
        "median_dfi_days": None, "median_os_days": None,
        "verdict": "NEGATIVE -- 'propranolol did not appear to influence treatment outcomes'",
    },
    {
        "agent": "thalidomide (antiangiogenic)",
        "citation": "Bray et al. 2018, J Small Anim Pract 59(2):85-91, PMID 29210452",
        "design": "15 dogs, splenic HSA, continuous thalidomide after splenectomy, NO control arm",
        "median_dfi_days": None, "median_os_days": 172,
        "verdict": "UNCONTROLLED -- median OS 172 d, 5/15 (33%) past one year; identical median to "
                   "the negative toceranib arm",
    },
    {
        "agent": "metronomic cyclophosphamide/etoposide/piroxicam",
        "citation": "Lana et al. 2007, J Vet Intern Med 21(4):764-9, PMID 17708397",
        "design": "9 dogs stage II splenic HSA vs 24 retrospective doxorubicin controls",
        "median_dfi_days": 178, "median_os_days": 178,
        "verdict": "SUGGESTIVE, UNRANDOMISED -- 178 d vs 126 d DFI and 133 d OS on doxorubicin",
    },
    {
        "agent": "propranolol + vinblastine (+ radiotherapy)",
        "citation": "Moirano et al. 2023, Vet Radiol Ultrasound 64(6):1099-1102, PMID 37800663",
        "design": "7 dogs, right atrial tumours -- cardiac site, not splenic",
        "median_dfi_days": 290, "median_os_days": 326,
        "verdict": "POSITIVE, SMALL, DIFFERENT SITE -- effusions resolved in all seven",
    },
]

# The one human result that motivates the class, and the partner distinction it turns on.
HUMAN_ANGIOSARCOMA_ANCHOR = {
    "citation": "Pasquier et al. 2016, EBioMedicine 6:87-95, PMID 27211551",
    "design": "7 patients, advanced/metastatic/recurrent angiosarcoma, propranolol + "
              "vinblastine-based metronomic chemotherapy",
    "response_rate": 1.0, "median_pfs_months": 11, "median_os_months": 16,
    "partner_specificity": "propranolol strongly synergized with VINBLASTINE in vitro but showed "
                           "only additivity or slight antagonism with paclitaxel and DOXORUBICIN",
    "why_it_matters": "The two negative canine trials paired a growth-directed agent with "
                      "doxorubicin. The two encouraging readouts used vinblastine.",
}

# Fraction by which growth must fall for the bar to drop under the real vaccine's 0.03/day.
GROWTH_REDUCTION_REQUIRED = {"with_cross_resistance_correction": 0.163, "without": 0.414}


def antiproliferative_schedule(horizon_days: int, start_day: int, ramp_days: float,
                               suppression: float, applicable_clones: np.ndarray,
                               stop_day: int | None = None) -> np.ndarray:
    """Multiplier array for `simulate_resistance(growth_modifier=...)`.

    `suppression` is the fraction of growth removed at full effect (0.163 means growth falls to
    83.7% of baseline). Rises as `1 - exp(-elapsed/ramp_days)` from `start_day`, returns to 1.0
    after `stop_day`. Clones flagged 0 in `applicable_clones` are unaffected.

    A multiplier can never take net growth below zero, which is the cytostatic ceiling: this is an
    antiproliferative agent, not a cytotoxic one.
    """
    if not 0 <= suppression <= 1:
        raise ValueError("suppression must lie in [0, 1]")
    if ramp_days <= 0:
        raise ValueError("ramp_days must be positive")
    days = np.arange(horizon_days)
    ramp = np.where(days >= start_day, 1 - np.exp(-(days - start_day) / ramp_days), 0.0)
    if stop_day is not None:
        ramp = np.where(days >= stop_day, 0.0, ramp)
    mask = np.asarray(applicable_clones, dtype=float)
    return 1.0 - np.outer(ramp * suppression, mask)


# Back-test: 10-year durable response for a growth-directed agent given WITHOUT a vaccine -- the
# configuration every real canine trial above actually used. Recomputed in the test module.
# Monte Carlo noise is about +/-3 points at 250 trials, so 0.336 vs 0.324 is not a real inversion.
BACKTEST_NO_VACCINE = {0.0: 0.284, 0.163: 0.336, 0.30: 0.324, 0.50: 0.524}

# The stack, with the antiproliferative agent scheduled through the engine's growth_modifier
# rather than by permanently rewriting model.growth.
STACK_WITH_SCHEDULED_AGENT = {
    "vaccine_only": 0.492,
    "vaccine_plus_correction": 0.640,
    "vaccine_plus_20pct_no_correction": 0.532,
    "vaccine_plus_correction_plus_16pct": 0.992,
    "vaccine_plus_correction_plus_20pct": 1.000,
}

# Starting the agent on day 0, 60 or 180 all give 1.000 -- it does not have to be given up front.
STACK_TOLERATES_A_DELAYED_START = {0: 1.000, 60: 1.000, 180: 1.000}

BACKTEST_VERDICT = {
    "prediction": "Growth reduction without a vaccine buys almost nothing: 0.284 -> 0.336 at the "
                  "levels in play, because slowing a clone that still has a positive margin delays "
                  "relapse rather than preventing it. Even 50% suppression only reaches 0.524.",
    "observed": "Toceranib negative in 43 dogs; propranolol+doxorubicin negative in 20; "
                "thalidomide uncontrolled at a median identical to the negative arm.",
    "consistency": "The model reproduces the real record. That is a check on the model, not "
                   "evidence for the stack.",
    "what_it_does_not_show": "None of these trials included a vaccine, and none used the corrected "
                             "cross-resistance backbone. The stack's prediction is about a "
                             "combination that has never been given to a dog, so the negative "
                             "record neither confirms nor refutes it.",
}

ANSWER_TO_IS_PROPRANOLOL_THE_ONLY_OPTION = (
    "No. Four other growth-directed agents have canine splenic-HSA readouts (toceranib, "
    "thalidomide, metronomic cyclophosphamide/etoposide/piroxicam, and propranolol with "
    "doxorubicin). The problem is not a shortage of candidates -- it is that the class has a poor "
    "record in this disease. Where a partner drug is involved the split runs along the partner: both "
    "clear negatives used doxorubicin, while the one positive canine readout (Moirano) and the human "
    "angiosarcoma result (Pasquier) both used vinblastine."
)
