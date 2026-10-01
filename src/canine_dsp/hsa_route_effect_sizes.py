"""What the routes to a taller vaccine are actually worth, in the engine's units.

`hsa_alternative_approach` establishes that the plan turns on raising vaccine height from the
measured 0.030/day to about 0.042/day -- an increment of 0.012/day -- and names three routes to it:
release the brake (anti-PD-L1), stop the recruitment (losartan), re-dose the non-responders. Those
were citations. None of them was a number.

This module converts each route's published result into a per-day rate, using the same method
`hsa_margin_analysis` already applies to the MEK anchor: take a measured change in tumour burden or
time-to-event and back out the exponential rate implied by it. Then it asks the only question that
matters for a cross-species, cross-tumour extrapolation -- what FRACTION of the measured effect has
to survive the transfer for the plan to work.

The answer separates the routes sharply, which the citation-level treatment did not.

A fourth route was added after the fact. eBAT was classified elsewhere in this analysis as a
cytotoxic log-remover against the route-8 compartment. Its originating group has since shown it
works primarily by depleting suppressive stroma -- benefiting a tumour it cannot kill -- which makes
it a lever on vaccine height rather than only a clearance term, and puts it in this module.

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
# ROUTE 4. DEPLETE THE SUPPRESSIVE STROMA -- eBAT, reclassified.
#
# eBAT entered this analysis in hsa_route8_alternatives as a CYTOTOXIC log-remover: a bispecific
# angiotoxin credited with 5.2-7.8 logs against the antigen-null drug-resistant compartment, on the
# strength of its trial in 23 dogs. That classification carried a stated open assumption -- that
# eBAT's targets, EGFR and uPAR, are present ON that compartment, which nobody has measured.
#
# The originating group has now shown the assumption is largely beside the point. eBAT's antitumour
# effect does not require the tumour cell to be killable by it.
# =============================================================================================

EBAT_READOUT_DAY = 21.0        # tumour volumes measured day 21 after inoculation
EBAT_TREATMENT_WINDOW_DAYS = 16.0   # dosing ran day 5 to day 21, 3x weekly for 2 weeks
EBAT_CONTROL_VOLUME_MM3 = 163.1
EBAT_TREATED_VOLUME_MM3 = 55.5

ROUTE_4_EBAT_STROMAL = {
    "citation": "Schulte et al. 2025, J Pharmacol Exp Ther 392(9):103674, PMID 40914989, "
                "doi 10.1016/j.jpet.2025.103674",
    "design": "MC17 mouse fibrosarcoma, chosen BECAUSE the tumour cells are resistant to eBAT "
              "(ED50 >50-100 nM against picomolar killing of other sarcomas), so any antitumour "
              "effect must come from the microenvironment rather than direct cytotoxicity. "
              "meBAT 50 ug/kg three times weekly for two weeks from day 5, in uPAR-knockout bone "
              "marrow chimeras that separate host stroma from tumour.",
    "result": {
        "median_tumour_volume_mm3": (EBAT_CONTROL_VOLUME_MM3, EBAT_TREATED_VOLUME_MM3),
        "tumour_volume_p": 0.03,
        "tam_infiltration_percent": (14.7, 5.1),
        "tam_p": 0.01,
        "phagocytic_myeloid_percent": (3.6, 22.3),
        "phagocytic_myeloid_p": 0.019,
        "cd3_t_cell_percent": (0.13, 3.68),
        "survival": "3 of 4 meBAT-treated uPAR-replete chimeras survived to endpoint against "
                    "0 of 5 uPAR-deficient chimeras",
    },
    "the_mechanism_is_pinned_down": "every effect was reduced or abolished in uPAR-deficient bone "
                                    "marrow chimeras. The target is host uPAR-expressing stroma, "
                                    "not the tumour cell -- which is why a tumour eBAT cannot kill "
                                    "still responds to it.",
    "implied_rate_per_day": {
        "readout_day": rate_from_burden_reduction(
            EBAT_TREATED_VOLUME_MM3 / EBAT_CONTROL_VOLUME_MM3, EBAT_READOUT_DAY),
        "treatment_window": rate_from_burden_reduction(
            EBAT_TREATED_VOLUME_MM3 / EBAT_CONTROL_VOLUME_MM3, EBAT_TREATMENT_WINDOW_DAYS),
    },
    "why_this_belongs_beside_the_other_three": "the effects measured are TAM depletion and T-cell "
                                               "infiltration. That is the same suppression Gulay "
                                               "2022 (PMID 35136176) measured as capping vaccine "
                                               "potency in canine HSA -- CD204+ PD-L1+ macrophages "
                                               "excluding T cells. Routes 1 and 2 act on that "
                                               "suppression by releasing the brake and blocking "
                                               "recruitment; this one depletes the cells outright.",
    "what_makes_it_better_placed_than_the_other_three": "its RATE is as cross-species as losartan's "
                                                        "-- a mouse fibrosarcoma. Everything else "
                                                        "about it is not. eBAT has measured exposure "
                                                        "at a tolerated canine dose, measured "
                                                        "tolerability, and a positive trial in 23 "
                                                        "dogs with stage I-II splenic "
                                                        "hemangiosarcoma, in the adjuvant setting, "
                                                        "in the single-early-cycle sequence the "
                                                        "finite-course simulation independently "
                                                        "derived. No other candidate lever clears "
                                                        "exposure and duration IN THIS DISEASE.",
    "what_it_rescues": "hsa_route8_alternatives assumed eBAT reaches the antigen-null drug-resistant "
                       "compartment and flagged the EGFR/uPAR stain on that compartment as the check "
                       "on whether the 0.830 closure is real. A drug that benefits a tumour it "
                       "cannot kill does not need the compartment to express its targets. That "
                       "experiment drops from load-bearing to secondary.",
    "the_limits": "a mouse fibrosarcoma, not canine hemangiosarcoma, so the rate carries no better "
                  "than losartan's. The volume conversion assumes a constant rate difference over "
                  "the interval, which the dosing schedule (two weeks of a ten-week model) does not "
                  "honour. And eBAT's own intensification trial was negative (Borgatti 2021, PMID "
                  "32187827) -- three cycles at a shortened interval produced more toxicity and less "
                  "benefit, so this lever cannot simply be turned up.",
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
    "route_4_ebat_stromal": {
        "effect_span_per_day": _span(ROUTE_4_EBAT_STROMAL["implied_rate_per_day"]),
        "transfer_needed": (
            transfer_required(max(ROUTE_4_EBAT_STROMAL["implied_rate_per_day"].values())),
            transfer_required(min(ROUTE_4_EBAT_STROMAL["implied_rate_per_day"].values()))),
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
    "route_4": "needs roughly 18-23%, which places it between losartan and anti-PD-L1 on the "
               "transfer axis. What separates it is not the rate -- that is a mouse fibrosarcoma, "
               "as distant as losartan's -- but that it is the only one of the four with measured "
               "exposure, measured tolerability and a positive trial in canine splenic "
               "hemangiosarcoma itself.",
    "the_correction_route_4_forces": "eBAT was classified in this analysis as a cytotoxic "
                                     "log-remover for route 8. Its originating group has since "
                                     "shown it works primarily by remodelling the microenvironment, "
                                     "which makes it a lever on vaccine HEIGHT -- the quantity the "
                                     "whole plan turns on -- and not only a one-off clearance term. "
                                     "It was filed in the wrong section.",
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

# What the checkpoint lever now costs, which is more than the 51-dog study implied.
WHAT_THE_CHECKPOINT_LEVER_COSTS = {
    "the_figure_this_analysis_used": "gilvetmab in 51 client-owned dogs, serious adverse events in "
                                     "5.9%, one of which was tumour haemorrhage (Chon 2026, "
                                     "PMID 42247661).",
    "the_figure_that_has_since_appeared": "Martin, Thamm & Weishaar 2026, Vet Comp Oncol, "
                                          "PMID 42680555, doi 10.1111/vco.70110: gilvetmab with "
                                          "hypofractionated radiotherapy in 18 dogs with mast cell "
                                          "tumour. Nine adverse events attributed to gilvetmab in "
                                          "seven dogs (39%), five dogs (28%) with Grade 3, and the "
                                          "authors conclude the combination 'did not provide "
                                          "durable tumour control' and that 'the AE profile "
                                          "warrants further evaluation'.",
    "why_it_is_not_a_straight_replacement": "mast cell tumour with concurrent radiotherapy is not "
                                            "post-splenectomy hemangiosarcoma, and radiation "
                                            "contributes its own toxicity. The 5.9% figure remains "
                                            "the right one for the antibody given alone.",
    "what_it_does_change": "the claim that a q14-28d antibody sits in the same tolerability class "
                           "as a q60d booster was resting on the monotherapy figure alone. In "
                           "combination the profile is worse, and this plan proposes the antibody "
                           "in combination. The claim is weakened, not withdrawn -- and it "
                           "compounds the tumour-haemorrhage signal already recorded as open in a "
                           "tumour made of endothelium.",
    "the_offsetting_development": "gilvetmab now holds conditional licensure in the United States "
                                  "and is the only commercially available veterinary checkpoint "
                                  "inhibitor (Chon, Greene & Stock 2026, JAVMA, PMID 42710546, "
                                  "doi 10.2460/javma.26.06.0517). The plan had treated it as a "
                                  "trial agent.",
}

# A randomised negative in the matched human setting, which the vaccine calibration should carry.
THE_PRECEDENT_THAT_CUTS_AGAINST_THE_VACCINE_CALIBRATION = {
    "citation": "randomised phase II trivalent ganglioside vaccine (GM2/GD2/GD3) with OPT-821 "
                "against OPT-821 alone, metastatic sarcoma rendered disease-free by surgery, "
                "PMID 36215947, doi 10.1016/j.ejca.2022.09.003",
    "the_finding": "a sustained serologic response to vaccination was induced, and there was NO "
                   "difference in recurrence-free or overall survival between arms.",
    "why_it_is_the_right_comparison": "the setting is the one this plan targets -- measurable "
                                      "disease removed by surgery, vaccine given against residual "
                                      "burden. And a randomised, placebo-controlled GD3 liposomal "
                                      "vaccine trial is now running in canine splenic "
                                      "hemangiosarcoma, so the same antigen class is about to be "
                                      "tested in the actual disease.",
    "what_it_does_to_the_calibration": "the 0.030/day vaccine height is back-calculated from "
                                       "survival gains in two single-arm or historical-control "
                                       "trials. This is a randomised trial in the matched setting "
                                       "where immunogenicity rose and survival did not. It does not "
                                       "invalidate the peptide-vaccine figure -- different antigen "
                                       "class, different species -- but it is the strongest "
                                       "available evidence that immunogenicity in this setting need "
                                       "not convert, which is exactly the endpoint mismatch this "
                                       "analysis names.",
}

VERDICT = {
    "the_question": "can the routes be backed with real numbers rather than citations?",
    "the_answer": "three of the four, yes, with margin. Re-dosing is quantified and found "
                  "insufficient alone -- which is itself a result the citation-level treatment "
                  "could not have produced.",
    "the_required_increment": REQUIRED_INCREMENT,
    "what_is_genuinely_established": "each route's published result converts to a per-day rate by "
                                     "the same method already used for the MEK anchor, and the "
                                     "required increment sits inside the measured envelope for "
                                     "three of the four with a large tolerance for transfer loss.",
    "which_one_to_measure_first": "eBAT. Not because its transfer fraction is the best -- losartan's "
                                  "is -- but because it is the only lever whose exposure and "
                                  "duration are already settled in canine splenic hemangiosarcoma, "
                                  "so a positive increment would be immediately actionable rather "
                                  "than the start of a dose-finding programme.",
    "what_is_not": "no measurement exists of any of these levers acting on VACCINE kill, in "
                   "hemangiosarcoma, in a dog. Converting a burden reduction into a rate is "
                   "arithmetic, not evidence that the rate carries across species and tumour. The "
                   "transfer fractions say how wrong the extrapolation can afford to be; they do "
                   "not say it is right.",
}


# =============================================================================================
# CLOSING THE LOOP: from a transfer fraction to a durability number.
#
# The transfer fractions above say whether a route can meet the requirement. They do not say what
# happens if it only partly does. That question the engine can answer, because the height grid is
# a ramp: every increment maps to a durability. Merging the coarse, fine and tail sweeps gives one
# curve, and each route's measured effect can be walked along it.
#
# All rows: same engine, same seed, same 250 trials, same corrected IC50 and waning-immunity
# schedule. Keyed by increment over the measured 0.030/day.
# =============================================================================================

DURABILITY_BY_INCREMENT = {
    #  increment: (stop drug at year 1, stop at year 2)
    0.0000: (0.464, 0.460),
    0.0030: (0.488, 0.516),
    0.0060: (0.592, 0.652),
    0.0075: (0.652, 0.696),
    0.0090: (0.684, 0.736),
    0.0105: (0.732, 0.864),
    0.0120: (0.872, 0.960),
    0.0135: (0.968, 0.992),
    0.0150: (0.992, 1.000),
    0.0200: (1.000, 1.000),
    0.0250: (1.000, 1.000),
}

# The figure any alternative has to beat: the measured vaccine with the drug given forever.
REFERENCE_DRUG_FOREVER = 0.888


def durability_at_increment(increment: float, stop_year: int = 1) -> float:
    """Ten-year durability for a given gain in vaccine kill, interpolated along the grid.

    Linear interpolation between Monte Carlo points, clamped at both ends. The grid is dense
    enough through the steep stretch that interpolation is a fair reading of it, but the returned
    value is an interpolation of simulated points, not a simulated point.
    """
    if stop_year not in (1, 2):
        raise ValueError("the grid covers withdrawal at year 1 or year 2")
    if increment < 0:
        raise ValueError("increment must be nonnegative")
    column = 0 if stop_year == 1 else 1
    points = sorted(DURABILITY_BY_INCREMENT)
    if increment <= points[0]:
        return float(DURABILITY_BY_INCREMENT[points[0]][column])
    if increment >= points[-1]:
        return float(DURABILITY_BY_INCREMENT[points[-1]][column])
    for low, high in zip(points, points[1:]):
        if low <= increment <= high:
            span = high - low
            weight = 0.0 if span == 0 else (increment - low) / span
            a = DURABILITY_BY_INCREMENT[low][column]
            b = DURABILITY_BY_INCREMENT[high][column]
            return float(a + weight * (b - a))
    raise AssertionError("increment fell outside the grid despite the bounds checks")


_ROUTE_EFFECTS = {
    "route_1_checkpoint": ROUTE_1_CHECKPOINT["implied_rate_per_day"],
    "route_2_losartan": ROUTE_2_LOSARTAN["implied_rate_per_day"],
    "route_3_redosing": ROUTE_3_REDOSING["implied_rate_per_day"],
    "route_4_ebat_stromal": ROUTE_4_EBAT_STROMAL["implied_rate_per_day"],
}


def durability_at_transfer(route: str, transfer: float, stop_year: int = 1,
                           conservative: bool = True) -> float:
    """Durability if `transfer` of a route's measured effect survives the species/tumour jump.

    `conservative` walks the LOW end of the route's effect range, which is the honest default for
    an extrapolation; pass False for the optimistic end.
    """
    if route not in _ROUTE_EFFECTS:
        raise ValueError(f"unknown route {route!r}; expected one of {sorted(_ROUTE_EFFECTS)}")
    if not 0.0 <= transfer <= 1.0:
        raise ValueError("transfer is a fraction of the measured effect, between 0 and 1")
    rates = _ROUTE_EFFECTS[route].values()
    effect = min(rates) if conservative else max(rates)
    return durability_at_increment(effect * transfer, stop_year)


# What each route buys at a range of transfer efficiencies, walking the conservative end of its
# measured effect and withdrawing the second drug after one year.
DURABILITY_BY_TRANSFER = {
    route: {t: round(durability_at_transfer(route, t), 3) for t in (0.10, 0.25, 0.50, 0.75, 1.00)}
    for route in _ROUTE_EFFECTS
}

WHAT_THE_MODEL_SAYS_ABOUT_PARTIAL_TRANSFER = {
    "route_2_at_a_quarter": "losartan's conservative effect, discounted to a quarter, still lands "
                            "above the drug-forever reference. Three-quarters of the effect can be "
                            "lost in the species jump and the plan is still better off.",
    "route_1_at_a_half": "the checkpoint route needs roughly half its conservative effect to reach "
                         "the reference -- which is the same answer the transfer fractions gave, "
                         "now expressed as a durability rather than a ratio.",
    "route_3_at_full": "re-dosing, even at full transfer of its optimistic effect, does not reach "
                       "the reference. The engine and the arithmetic agree.",
    "route_4_at_a_quarter": "eBAT's conservative effect at a quarter transfer lands above the "
                            "drug-forever reference, alongside losartan and ahead of the "
                            "checkpoint route. The distinguishing fact is not the durability "
                            "number but that this is the only lever whose exposure and duration "
                            "are already settled in this disease.",
    "why_this_is_worth_having": "the transfer fractions answer a yes/no question. This answers the "
                                "question a trial designer actually has: if the effect is half what "
                                "was measured, what does the dog get? On a ramp that has an answer, "
                                "and it is not zero.",
    "the_interpolation_caveat": "values between grid points are linear interpolations of simulated "
                                "points, not simulations. The grid is dense through the steep "
                                "stretch (0.0075 to 0.0150 in steps of 0.0015), so the reading is "
                                "fair, but it should not be quoted to three decimals as though it "
                                "were a run.",
}
