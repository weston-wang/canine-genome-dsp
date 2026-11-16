"""Carrying the uncertainty through, and reinforcing the joints that turned out to be thin.

An earlier statement of the exposure margin used point estimates and read "1.48x, clears". Carried
through the reported uncertainty it is 0.96x-3.25x -- the plan fails inside one standard deviation.
This module states the margin as a range, identifies which anchor the protein-binding objection
actually applies to, and replaces the weakest joint (a swept kill rate justified by analogy) with a
figure derived from measured tumour growth curves.

See docs/HSA_DURABLE_RESPONSE.md.
"""

import numpy as np

# ---------------------------------------------------------------------------------------------
# 1. THE MARGIN, WITH THE UNCERTAINTY CARRIED THROUGH.
COMBINATION_IC50_nM = 11.0
COMBINATION_IC50_SD_nM = 6.0
TRAMETINIB_ACHIEVED_nM = 16.25
FRACTION_OF_DOGS_REACHING_IT = 0.70


def margin(achieved_nM: float, required_nM: float) -> float:
    """How far achieved exposure clears the requirement. Below 1.0 means it does not."""
    if required_nM <= 0:
        raise ValueError("required_nM must be positive")
    if achieved_nM < 0:
        raise ValueError("achieved_nM must be nonnegative")
    return float(achieved_nM / required_nM)


MARGIN_ACROSS_THE_REPORTED_UNCERTAINTY = {
    "at_ic50_minus_1sd": margin(TRAMETINIB_ACHIEVED_nM, COMBINATION_IC50_nM - COMBINATION_IC50_SD_nM),
    "at_point_estimate": margin(TRAMETINIB_ACHIEVED_nM, COMBINATION_IC50_nM),
    "at_ic50_plus_1sd": margin(TRAMETINIB_ACHIEVED_nM, COMBINATION_IC50_nM + COMBINATION_IC50_SD_nM),
    "honest_statement": "3.25x at best, 1.48x at the point estimate, 0.96x at one standard "
                        "deviation the wrong way. The margin is INSIDE the measurement noise, and "
                        "only 70% of dogs reach even the point-estimate exposure.",
    "what_this_is_not": "this does not say the combination fails. It says a single-number margin was "
                        "the wrong way to report it, and 'clears with 1.5x to spare' overstated what "
                        "the data support.",
    "and_a_margin_below_one_is_not_a_cliff": "reading 0.96x as 'fails' is itself too binary. Effect "
                                             "is an Emax curve, not a switch: sitting AT the IC50 "
                                             "gives half-maximal effect rather than none. Run "
                                             "through the engine, the +1 SD case gives 0.748 "
                                             "durability -- worse than 0.888, not collapse. See "
                                             "DURABILITY_ACROSS_THE_IC50_UNCERTAINTY.",
}

# What the IC50 uncertainty actually costs, run through the engine rather than argued from the
# ratio. This is the number that matters, and it is far less brittle than the bare margin suggests.
DURABILITY_ACROSS_THE_IC50_UNCERTAINTY = {
    5.0:  0.996,   # IC50 - 1 SD
    11.0: 0.888,   # point estimate
    17.0: 0.748,   # IC50 + 1 SD -- the case where the bare margin reads "fails"
    34.0: 0.528,   # twice the worst case
    "reading": "across the full reported uncertainty durability spans 0.748-0.996. Even at twice "
               "the worst-case IC50 it is 0.528, still above the 0.500 the correction alone gives. "
               "The plan degrades gracefully rather than failing at a threshold.",
}

# Sensitivity to the swept kill rate itself. Steeper, and the real fragility.
DURABILITY_ACROSS_THE_KILL_RATE = {
    0.0: 0.500, 0.011: 0.576, 0.0225: 0.888, 0.034: 0.996, 0.045: 1.000,
    "reading": "this is the steep axis. Halving the kill rate to 0.011/day loses most of the "
               "benefit (0.576). The plan needs the second drug to be roughly as effective as "
               "required, not merely present -- which is why the in vivo growth-curve derivation "
               "matters more than the IC50 ratio.",
}

# Can the second drug be stopped once the resistant clones should be gone? No.
STOPPING_THE_SECOND_DRUG = {
    1: 0.464, 2: 0.460, 3: 0.488, 5: 0.576, None: 0.888,
    "reading": "there is no escape hatch. Stopping at one, two or three years lands BELOW the 0.500 "
               "that the cross-resistance correction alone delivers -- the clones are suppressed, "
               "not eliminated, and they resume when the drug stops. Five years still only reaches "
               "0.576.",
    "why_it_matters": "this closes off the obvious answer to the chronic-toxicity objection. The "
                      "second drug has to run for the full ten years, exactly like the boosters, "
                      "which makes cumulative renal and marrow toxicity the sharpest remaining "
                      "weakness rather than a manageable one -- and makes the staggered schedule "
                      "(STAGGERED_DOSING_IS_THE_PUBLISHED_OPTIMUM) load-bearing rather than a "
                      "refinement.",
}

# ---------------------------------------------------------------------------------------------
# 2. THE PROTEIN-BINDING OBJECTION APPLIES TO ONE ANCHOR AND NOT THE OTHER.
#
# This is the reinforcement rather than a defence: lean on the anchor the objection cannot reach.
THE_TWO_ANCHORS_ARE_NOT_EQUALLY_VULNERABLE = {
    "the_objection": "16.25 nM is TOTAL plasma trametinib. Trametinib is extensively protein bound, "
                     "so free drug at the tumour is a fraction of that. Comparing a total plasma "
                     "concentration to an in vitro IC50 is not like for like.",
    "in_vitro_anchor": {
        "value_nM": COMBINATION_IC50_nM,
        "assay_conditions": "DMEM with 10% heat-inactivated FBS, 72 h exposure (Andersen et al. "
                            "2015)",
        "why_it_is_vulnerable": "10% FBS carries roughly a tenth of plasma protein. An IC50 measured "
                                "in that medium is a total concentration in a LOW-protein "
                                "environment, so the equivalent total PLASMA concentration needed is "
                                "higher, not lower. The correction runs AGAINST the plan, and its "
                                "size is not quantified here.",
        "status": "vulnerable -- should not carry the argument",
    },
    "clinical_anchor": {
        "value_ng_per_ml": 10.0,
        "value_nM": TRAMETINIB_ACHIEVED_nM,
        "what_it_is": "the trametinib plasma concentration Takada et al. 2024 identify as associated "
                      "with CLINICAL EFFICACY in humans, and which ~70% of dogs reach at the "
                      "maximum tolerated dose",
        "why_the_objection_cannot_reach_it": "it was derived from clinical outcomes in real plasma "
                                             "with real protein binding. Whatever the bound fraction "
                                             "is, it is already inside the number. A "
                                             "free-fraction correction applied to an "
                                             "efficacy-anchored threshold would double-count it.",
        "status": "robust -- this is the anchor the argument should rest on",
    },
    "the_reinforcement": "the two anchors agree at ~16 nM, but they are not equally strong. Stating "
                         "the case on the clinical anchor alone removes the protein-binding "
                         "objection entirely, at the cost of the canine-tumour specificity the in "
                         "vitro number provided. That is the right trade: a robust human-efficacy "
                         "threshold beats a species-matched number that needs a correction nobody "
                         "has made.",
}

# ---------------------------------------------------------------------------------------------
# 3. THE WEAKEST JOINT, REPLACED. The model needs a per-day kill; nothing measured connected an
# IC50 to a kill rate, so the requirement was justified by analogy to other clones. It does not
# have to be: the same paper reports in vivo tumour growth curves in the right species and tumour.
IN_VIVO_DERIVED_EFFECT_SIZE = {
    "source": "Andersen et al. 2015, PMID 25955301 -- canine angiosarcoma tumorgrafts",
    "treatment_started_at_mm3": (50.0, 100.0),
    "vehicle_reached_mm3": 1000.0,
    "vehicle_reached_by_day": 21,
    "combination_result": "virtually no growth by week 3; significantly smaller than either "
                          "monotherapy at day 38",
    "implied_vehicle_net_growth_per_day": (0.1096, 0.1427),
    "implied_growth_removed_per_day": (0.110, 0.143),
    "what_the_model_needs_per_day": 0.0225,
    "margin_against_the_measured_envelope": (4.9, 6.3),
    "why_this_is_better_than_the_analogy": "the swept 0.0225/day was defended by noting it sits "
                                           "inside the range the model already grants the primary "
                                           "drug against resistant clones. That is an argument from "
                                           "internal consistency. This is an argument from a "
                                           "measured growth curve in canine angiosarcoma.",
    "the_honest_limits": "the 0.110-0.143/day is the COMBINATION's total effect, so attributing all "
                         "of it to the second drug would double-count what the model already gives "
                         "the first. And a subcutaneous mouse tumorgraft grows far faster than "
                         "residual micrometastatic disease in a dog, so the absolute rate does not "
                         "transfer. What transfers is that the required effect sits well inside the "
                         "measured envelope rather than at its edge.",
}


def implied_exponential_rate(start_volume: float, end_volume: float, days: float) -> float:
    """Net per-day exponential rate implied by two tumour volumes and the interval between."""
    if start_volume <= 0 or end_volume <= 0 or days <= 0:
        raise ValueError("volumes and days must be positive")
    return float(np.log(end_volume / start_volume) / days)


# ---------------------------------------------------------------------------------------------
# 4. THE DRUG INTERACTION. The two reports disagree, and the disagreement is species-shaped.
THE_INTERACTION_EVIDENCE_IS_SPLIT = {
    "in_dogs": "Wei et al. 2022 (PMID 36590793): sapanisertib exposure FELL when combined, "
               "attributed to trametinib inducing CYP3A4. Trametinib itself accumulated 3-4x on "
               "daily dosing.",
    "in_mice": "Wei et al. 2020 (PMID 32943547): 'The combination did not significantly change "
               "plasma sapanisertib pharmacokinetics; however, trametinib area under the curve was "
               "INCREASED in the presence of sapanisertib.'",
    "why_it_matters_for_the_margin": "the 16.25 nM figure comes from trametinib given ALONE in a "
                                     "phase I. Both reports agree trametinib exposure rises in "
                                     "combination or on repeat dosing, which pushes the achieved "
                                     "concentration UP relative to the number the margin was "
                                     "computed from. That is a real, if unquantified, cushion on the "
                                     "thin side of the margin.",
    "what_is_not_resolved": "whether the canine loss of sapanisertib exposure undercuts the mTORC2 "
                            "arm. It is the drug the mechanism argument depends on, and in dogs it "
                            "is the one the pairing weakens.",
}

# ---------------------------------------------------------------------------------------------
# 5. THE TOXICITY FIX IS ALREADY PUBLISHED, and it was in the evidence without being used.
STAGGERED_DOSING_IS_THE_PUBLISHED_OPTIMUM = {
    "citation": "Wei et al. 2020, Mol Cancer Ther 19(11):2308-2318, PMID 32943547",
    "finding": "'a staggered sapanisertib dose, coupled with daily trametinib, was optimal for "
               "limiting primary mucosal melanoma xenograft growth in mice, and tumor dissemination "
               "in a metastasis model, WHILE MINIMIZING HEMATOLOGIC AND RENAL SIDE EFFECTS'",
    "why_it_answers_two_objections_at_once": "the chronic-toxicity worry for this regimen is "
                                             "cumulative renal and marrow injury -- trametinib's "
                                             "dose-limiting toxicities in dogs were hypertension, "
                                             "proteinuria and elevated ALP. Staggering is the "
                                             "schedule the authors found minimises exactly those, "
                                             "and it also reduces the window in which the CYP3A4 "
                                             "interaction operates.",
    "status": "this was already in the cited evidence and was recorded but not used. The regimen "
              "should specify staggered sapanisertib with daily trametinib rather than both daily.",
}

VERDICT = {
    "what_was_overstated": "the exposure margin. Reported as 1.48x from point estimates; it is "
                           "0.96x-3.25x across the reported uncertainty, and 30% of dogs do not "
                           "reach even the point estimate.",
    "what_got_stronger": (
        "the kill-rate requirement is now derived from measured canine angiosarcoma tumorgraft "
        "growth (4.9-6.3x margin) rather than from analogy",
        "the protein-binding objection is answered by demoting the in vitro anchor rather than "
        "defending it -- the clinical anchor already embeds protein binding",
        "trametinib exposure rises in combination and on repeat dosing, cushioning the thin side of "
        "the margin",
        "staggered dosing is the published optimum and minimises the exact toxicities at issue",
    ),
    "what_remains_genuinely_weak": (
        "the margin is still inside measurement noise on the pessimistic side, though the engine "
        "shows that costs 0.888 -> 0.748 rather than collapse",
        "the second drug CANNOT be stopped -- 1, 2 and 3 year stops all land below 0.500 -- so "
        "cumulative toxicity over a decade is the sharpest remaining objection",
        "in dogs specifically, the combination REDUCES sapanisertib exposure -- weakening the arm "
        "the mechanism argument depends on",
        "tolerability data are 17 days in healthy laboratory beagles, against a regimen intended to "
        "run for years",
        "no toxicity data exist for the full stack of two kinase inhibitors plus vaccine plus "
        "cell therapy",
    ),
    "the_honest_summary": "the framework is defensible and the weakest joint has been replaced with "
                          "a measurement. The claim that the combination clears its requirement in a "
                          "dog remains a range that includes failure, and should be stated that way.",
}
