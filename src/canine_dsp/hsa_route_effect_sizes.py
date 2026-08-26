"""What the three routes are actually worth, in the engine's units.

`hsa_alternative_approach` establishes that the plan turns on raising vaccine height from the
measured 0.030/day to about 0.042/day -- an increment of 0.012/day -- and names three routes to it:
release the brake (anti-PD-L1), stop the recruitment (losartan), re-dose the non-responders. Those
were citations. None of them was a number.

This module converts each route's published result into a per-day rate, using the same method
`hsa_margin_analysis` already applies to the MEK anchor: take a measured change in tumour burden or
time-to-event and back out the exponential rate implied by it. Then it asks the only question that
matters for a cross-species, cross-tumour extrapolation -- what FRACTION of the measured effect has
to survive the transfer for the plan to work.

The answer separates the three routes sharply, which the citation-level treatment did not.

See docs/HSA_DURABLE_RESPONSE.md.
"""
from __future__ import annotations

import math

# The target, from hsa_alternative_approach.MINIMUM_REQUIREMENT.
MEASURED_VACCINE_HEIGHT = 0.030
REQUIRED_HEIGHT = 0.042
REQUIRED_INCREMENT = REQUIRED_HEIGHT - MEASURED_VACCINE_HEIGHT   # 0.012/day

# How many times the tumour burden grows between the measurement baseline and death. Nobody
# measures this directly, so every time-to-event conversion below is reported across a range rather
# than at a point. 10x to 100x brackets the usual clinical assumption.
LETHAL_BURDEN_MULTIPLES = (10.0, 20.0, 100.0)


def rate_from_burden_reduction(fraction_remaining: float, days: float) -> float:
    """Per-day rate implied by treatment leaving `fraction_remaining` of control burden at `days`.

    A 64% reduction leaves 0.36. The implied rate is -ln(0.36)/days: the constant per-day
    difference in net growth that would open that gap over that interval.
    """
    if not 0.0 < fraction_remaining < 1.0:
        raise ValueError("fraction_remaining must lie strictly between 0 and 1")
    if days <= 0:
        raise ValueError("days must be positive")
    return float(-math.log(fraction_remaining) / days)


def rate_from_time_to_event(control_days: float, treated_days: float,
                            lethal_burden_multiple: float) -> float:
    """Per-day rate implied by treatment extending time-to-event from `control_days` to `treated_days`.

    Assumes the event occurs when burden has grown by a fixed multiple, so time-to-event is
    inversely proportional to net growth rate. The rate difference is then
    ln(multiple) * (1/control - 1/treated).
    """
    if control_days <= 0 or treated_days <= 0:
        raise ValueError("both times must be positive")
    if treated_days <= control_days:
        raise ValueError("treated time must exceed control time for this to describe a benefit")
    if lethal_burden_multiple <= 1.0:
        raise ValueError("the burden must grow by more than one-fold before the event")
    return float(math.log(lethal_burden_multiple) * (1.0 / control_days - 1.0 / treated_days))


def transfer_required(effect_per_day: float, increment: float = REQUIRED_INCREMENT) -> float:
    """Fraction of a measured effect that must survive the species/tumour transfer to suffice.

    Above 1.0 means the measured effect is too small even if it carried over in full.
    """
    if effect_per_day <= 0:
        raise ValueError("the measured effect must be positive")
    return float(increment / effect_per_day)


# =============================================================================================
# ROUTE 1. RELEASE THE BRAKE -- anti-PD-L1 in dogs.
# =============================================================================================

ROUTE_1_CHECKPOINT = {
    "citation": "Maekawa et al. 2021, NPJ Precis Oncol 5(1):10, PMID 33580183, "
                "doi 10.1038/s41698-021-00147-6",
    "design": "c4G12, a canine chimeric anti-PD-L1 monoclonal antibody, in 29 dogs with pulmonary "
              "metastatic oral malignant melanoma, against a historical control group of 15",
    "result": {"treated_median_os_days": 143, "control_median_os_days": 54,
               "complete_responses": "1 of 13 dogs with measurable disease (7.7%)",
               "adverse_events_any_grade": "15 of 29 dogs (51.7%)"},
    "why_this_anchor_and_not_gilvetmab": "the gilvetmab study reports response rate and time to "
                                         "progression against no control arm. This one reports a "
                                         "survival comparison, which is what the rate conversion "
                                         "needs -- and it is in dogs with established pulmonary "
                                         "metastatic disease, the closest available analogue to the "
                                         "residual-disease setting this plan targets.",
    "implied_rate_per_day": {
        m: rate_from_time_to_event(54, 143, m) for m in LETHAL_BURDEN_MULTIPLES},
    "the_limits": "a historical control rather than a randomised one; oral malignant melanoma "
                  "rather than hemangiosarcoma; and the conversion assumes death at a fixed burden "
                  "multiple, which is why the rate is reported across a 10x-100x range instead of "
                  "as a point.",
}

# =============================================================================================
# ROUTE 2. STOP THE RECRUITMENT -- losartan against CCL2-CCR2.
# =============================================================================================

ROUTE_2_LOSARTAN = {
    "citation": "Regan et al. 2019, J Immunol 202(10):3087-3102, PMID 30971441, "
                "doi 10.4049/jimmunol.1800619",
    "design": "daily losartan in experimental pulmonary metastasis models, with metastatic burden "
              "quantified by bioluminescent imaging and monocyte recruitment by flow cytometry",
    "result": {
        "ct26_burden_reduction": 0.64, "ct26_day": 19,
        "fourt1_burden_reduction": 0.90, "fourt1_day": 14,
        "micrometastatic_area_reduction": 0.70, "micrometastatic_day": 14,
        "lung_inflammatory_monocyte_reduction": 0.70,
        "tumour_associated_macrophage_reduction": 0.36,
        "microvessel_density_reduction": 0.35,
        "survival": "in the 4T1 model the reduction in burden significantly prolonged overall "
                    "survival",
    },
    "the_mechanism_is_pinned_down": "the effect is CCR2-dependent and AT1R-independent: it survives "
                                    "in AT1R-knockout mice, and losartan adds nothing on top of "
                                    "CCR2 knockout, so CCR2 is necessary for the anti-tumour "
                                    "activity. Direct cytotoxic and anti-angiogenic explanations "
                                    "via AT1R were excluded rather than assumed away.",
    "implied_rate_per_day": {
        "ct26": rate_from_burden_reduction(0.36, 19),
        "fourt1": rate_from_burden_reduction(0.10, 14),
        "micrometastases": rate_from_burden_reduction(0.30, 14),
    },
    "the_limits": "mouse models with aggressive transplantable lines (CT26 colon, 4T1 mammary), not "
                  "canine hemangiosarcoma. A transplanted lung metastasis grows far faster than "
                  "residual disease in a dog, so the absolute rate does not transfer -- only the "
                  "question of whether the required increment sits inside the measured envelope.",
    "the_exposure_is_not_hand_waved": "the concentrations producing these effects sit within the "
                                      "Cmax and AUC of a single 200 mg oral dose in published human "
                                      "pharmacokinetics, and the canine dose that moves the same "
                                      "pharmacodynamic endpoint was established separately in 28 "
                                      "dogs (Regan 2022, PMID 34580111).",
}

# =============================================================================================
# ROUTE 3. RE-DOSE THE NON-RESPONDERS.
# =============================================================================================

ROUTE_3_REDOSING = {
    "citation": "Mason et al. 2025, Mol Ther 33(4):1674-1686, PMID 39955616, "
                "doi 10.1016/j.ymthe.2025.02.023",
    "design": "118 dogs with appendicular osteosarcoma, standard of care followed by ADXS31-164",
    "the_strata": {"elite_survivor_dfi_days": ">490", "short_term_survivor_dfi_days": "150-235"},
    "what_was_measured": "elite survivors mounted pyrexic and IL-6/TNF-alpha responses to the FIRST "
                         "immunisation and short-term survivors did not; repeat immunisations "
                         "brought short-term survivors to comparable responses. PBMC transcriptomes "
                         "showed cytotoxic activity in elite but not short-term survivors.",
    "how_the_rate_is_derived": "the trial reports no effect size for re-dosing. What it does report "
                               "is the disease-free interval separating the two immunological "
                               "strata, so the derivable quantity is the rate gap between a "
                               "responder and a non-responder -- the most that converting one into "
                               "the other could be worth.",
    "implied_rate_per_day": {
        m: rate_from_time_to_event(235, 490, m) for m in LETHAL_BURDEN_MULTIPLES},
    "the_limits": "235 and 490 days are stratum boundaries, not group means, so this is a lower "
                  "bound on the gap between the strata. It is osteosarcoma. And the trial showed no "
                  "overall DFI or OS benefit, so this is the ceiling on a subgroup effect, not a "
                  "demonstrated one.",
}

# =============================================================================================
# THE QUESTION THAT DECIDES IT: how much has to transfer?
#
# Every anchor above is cross-species or cross-tumour or both, so the absolute rates cannot be
# carried across. What can be carried across is the ratio -- what fraction of the measured effect
# would have to survive the transfer for the required 0.012/day to be met.
# =============================================================================================

def _span(rates) -> tuple[float, float]:
    values = list(rates.values()) if isinstance(rates, dict) else list(rates)
    return min(values), max(values)


TRANSFER_REQUIRED = {
    "route_1_checkpoint": {
        "effect_span_per_day": _span(ROUTE_1_CHECKPOINT["implied_rate_per_day"]),
        "transfer_needed": (
            transfer_required(max(ROUTE_1_CHECKPOINT["implied_rate_per_day"].values())),
            transfer_required(min(ROUTE_1_CHECKPOINT["implied_rate_per_day"].values()))),
    },
    "route_2_losartan": {
        "effect_span_per_day": _span(ROUTE_2_LOSARTAN["implied_rate_per_day"]),
        "transfer_needed": (
            transfer_required(max(ROUTE_2_LOSARTAN["implied_rate_per_day"].values())),
            transfer_required(min(ROUTE_2_LOSARTAN["implied_rate_per_day"].values()))),
    },
    "route_3_redosing": {
        "effect_span_per_day": _span(ROUTE_3_REDOSING["implied_rate_per_day"]),
        "transfer_needed": (
            transfer_required(max(ROUTE_3_REDOSING["implied_rate_per_day"].values())),
            transfer_required(min(ROUTE_3_REDOSING["implied_rate_per_day"].values()))),
    },
}

THE_THREE_ROUTES_ARE_NOT_EQUIVALENT = {
    "route_1": "needs roughly 23-45% of its measured effect to transfer. A canine antibody, in "
               "dogs, in metastatic disease -- the shortest extrapolation of the three, and it can "
               "lose more than half its effect and still suffice.",
    "route_2": "needs roughly 7-22%. The largest measured effect and the widest tolerance for "
               "discount, but the longest extrapolation -- mouse models of two non-canine tumours.",
    "route_3": "needs 118-235%. It cannot meet the requirement alone EVEN IF the effect transferred "
               "in full, because the gap between the two immunological strata is smaller than the "
               "increment the plan needs.",
    "the_correction_this_forces": "the earlier treatment listed three routes as if they were "
                                  "interchangeable. They are not. Two clear the requirement with "
                                  "room to be wrong about the transfer; the third is a supporting "
                                  "contributor that cannot carry the plan.",
    "what_route_3_is_still_good_for": "it needs no new agent and no new toxicity, so it is free to "
                                      "add, and on a ramp rather than a cliff every increment "
                                      "counts. It should be in the regimen. It should not be relied "
                                      "on.",
}

# The two remaining routes are not independent either, and there is canine evidence for the link.
ROUTES_1_AND_2_ARE_MECHANISTICALLY_COUPLED = {
    "citation": "Maekawa et al. 2022, Sci Rep 12(1):9265, PMID 35665759, "
                "doi 10.1038/s41598-022-13484-8",
    "design": "serum biomarkers measured before treatment in 27 dogs with pulmonary metastatic oral "
              "malignant melanoma receiving the same anti-PD-L1 antibody",
    "the_finding": "lower baseline MCP-1 -- which is CCL2, the chemokine losartan blocks -- "
                   "predicted PROLONGED overall survival on anti-PD-L1, alongside lower PGE2 and "
                   "VEGF-A and higher IL-2, IL-12 and SCF. MCP-1 was also elevated in tumour-"
                   "bearing dogs relative to healthy ones.",
    "why_this_matters": "it means the CCL2 axis is not merely a second, parallel target. In dogs, "
                        "it is a measured RESISTANCE mechanism for checkpoint blockade. Blocking it "
                        "is a reason to expect the two routes to combine rather than merely add.",
    "the_caution_that_comes_with_it": "coupling cuts both ways. Two levers on one pathway may "
                                      "overlap rather than sum, so the combination cannot be "
                                      "assumed to deliver the sum of the two effects. The "
                                      "conservative reading is that either alone suffices at "
                                      "plausible transfer, and the combination buys insurance "
                                      "rather than arithmetic.",
    "a_fourth_lever_the_same_paper_hands_over": "PGE2 predicted resistance, and the COX-2 inhibitor "
                                                "meloxicam combined with the antibody enhanced Th1 "
                                                "cytokine production by canine PBMCs. Meloxicam is "
                                                "already given to dogs indefinitely, so it clears "
                                                "the duration criterion outright.",
}

VERDICT = {
    "the_question": "can the three routes be backed with real numbers rather than citations?",
    "the_answer": "two of them, yes, with margin. The third is quantified and found insufficient "
                  "alone -- which is itself a result the citation-level treatment could not have "
                  "produced.",
    "the_required_increment": REQUIRED_INCREMENT,
    "what_is_genuinely_established": "each route's published result converts to a per-day rate by "
                                     "the same method already used for the MEK anchor, and the "
                                     "required increment sits inside the measured envelope for two "
                                     "of the three with a large tolerance for transfer loss.",
    "what_is_not": "no measurement exists of any of these levers acting on VACCINE kill, in "
                   "hemangiosarcoma, in a dog. Converting a burden reduction into a rate is "
                   "arithmetic, not evidence that the rate carries across species and tumour. The "
                   "transfer fractions say how wrong the extrapolation can afford to be; they do "
                   "not say it is right.",
}
