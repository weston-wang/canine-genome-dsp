"""Is there another way to close route 8, or is the expensive answer the only one?

`hsa_orthogonal_kill` and `hsa_persister_evidence` between them landed on two closures for route 8's
dangerous case -- restore antigen presentation, or kill the cell through the dependency it acquired
by becoming resistant. Both are expensive, neither has a drug behind it in this disease, and both
amount to the same instruction: see it or kill it.

That is a narrow pair of answers, and a narrow pair of answers usually means a narrow framing. This
module deliberately attacks the framing instead of the problem. It asks four questions the earlier
work never asked:

  1. Does the blind spot have to be ELIMINATED, or could it be CONTAINED? Competitive release is a
     real phenomenon and this engine models density-dependent growth, so containment is available in
     principle and was never tried.
  2. Does the answer depend on ANTIGEN COVERAGE, which was fixed at 95% and never varied?
  3. Does the blind spot really grow as fast as a normal cell? The engine already charges the
     acquired antigen-loss clone a fitness cost and the baseline antigen-null clone none, which is
     an inconsistency in my own model rather than a finding.
  4. Is there a THIRD kill mechanism, orthogonal to both axes, that has actually been given to dogs
     with this disease?

The first three all fail, and they fail for one shared reason that is worth more than any of them
individually. The fourth succeeds, and the agent turns out to have both a positive trial and a
negative one.

See docs/HSA_DURABLE_RESPONSE.md.
"""
from __future__ import annotations

import math

from .hsa_persister_evidence import (
    BLIND_SPOT_NET_GROWTH_PER_DAY,
    blind_spot_initial_cells,
    required_rate_for_course,
    viability_after,
)

DETECTION_FLOOR_FRACTION = 0.01          # mapk_resistance detection_floor_fraction, K = 1.0
HORIZON_DAYS = 3650


def days_to_detection(blind_spot_fraction: float,
                      net_growth: float = BLIND_SPOT_NET_GROWTH_PER_DAY) -> float:
    """How long a blind spot of `blind_spot_fraction` takes to reach the model's detection floor.

    The number that decides whether making the blind spot smaller or slower is worth anything. It is
    a logarithm of the size divided by the growth rate, which is why neither lever buys much.
    """
    if blind_spot_fraction <= 0 or net_growth <= 0:
        raise ValueError("fraction and net_growth must be positive")
    if blind_spot_fraction >= DETECTION_FLOOR_FRACTION:
        return 0.0
    return float(math.log(DETECTION_FLOOR_FRACTION / blind_spot_fraction) / net_growth)


# =============================================================================================
# 1-3. THE THREE CHEAP ANSWERS, AND THE ONE REASON THEY ALL FAIL.
# =============================================================================================

WHY_CONTAINMENT_IS_NOT_AVAILABLE_HERE = {
    "the_idea": "Gatenby's competitive release: maximum cell kill is not maximum benefit, because "
                "eliminating the sensitive population lets resistant clones 'proliferate unopposed "
                "by competitors'. Adaptive therapy deliberately keeps sensitive cells alive to "
                "suppress the resistant ones, and it has a positive randomised trial behind it.",
    "citation": "Enriquez-Navas et al. 2016, Sci Transl Med, PMID 26912903",
    "why_it_should_have_worked_here": "this engine grows every clone at growth * (1 - density), so "
                                      "competitive release is already in it. Driving total burden to "
                                      "nadir is exactly what releases the blind spot: at nadir "
                                      "density its net growth is 0.0334/day, and at density near "
                                      "carrying capacity it would be near zero. The plan's own "
                                      "success at shrinking the tumour is what accelerates the one "
                                      "compartment it cannot touch.",
    "why_it_does_not_work_here": "the blind spot is not a small resistant minority waiting to be "
                                 "suppressed. At 95% coverage and an initial burden of 0.3 it is "
                                 "0.015 of carrying capacity -- 1.5e8 cells -- which is ABOVE this "
                                 "model's own 0.01 detection floor. It is macroscopic on day one. "
                                 "Containment manages a subclinical reservoir; there is no "
                                 "subclinical reservoir here to manage.",
    "the_second_reason_specific_to_this_disease": "adaptive therapy buys time by carrying a larger "
                                                  "tumour. In hemangiosarcoma the tumour burden is "
                                                  "itself lethal through haemorrhage -- route 5, the "
                                                  "one escape with no drug answer. Trading cancer "
                                                  "control for burden is a worse trade in this "
                                                  "disease than in almost any other.",
    "what_it_is_still_good_for": "it correctly identifies that the holding rate the ferroptosis "
                                 "agent must out-run, 0.0334/day, is a consequence of the nadir the "
                                 "rest of the regimen achieves rather than a property of the clone. "
                                 "That is a real insight and it is why the requirement is stated as "
                                 "a rate against a specific regimen, not as an absolute.",
}

COVERAGE_DOES_NOT_CLOSE_IT_EITHER = {
    "the_idea": "coverage was fixed at 95% throughout and never varied. If the blind spot were "
                "small enough it might not matter, and raising coverage is what polyvalent antigens "
                "and epitope spreading actually do.",
    "the_seductive_arithmetic": "the blind spot drops below the 0.01 detection floor above 96.7% "
                                "coverage, which looks like a threshold worth chasing and sits "
                                "suspiciously close to the 95% the analysis assumed.",
    "why_it_is_a_mirage": "starting below the detection floor only delays arrival at it. Time to "
                          "detection is logarithmic in the starting size and linear in the growth "
                          "rate, so the lever is almost worthless against a ten-year horizon.",
    "the_numbers": {
        # coverage: days for the blind spot to reach the detection floor at 0.0334/day
        0.95: 0.0,
        0.99: 36.0,
        0.999: 105.0,
        0.9999: 174.0,
    },
    "the_reading": "going from 95% to 99.99% antigen coverage -- a five-hundred-fold reduction in "
                   "the size of the blind spot -- buys 174 days against a 3650-day horizon. "
                   "Coverage is not the lever.",
}

THE_FITNESS_COST_INCONSISTENCY_I_HAD_NOT_NOTICED = {
    "the_inconsistency": "the engine charges the ACQUIRED antigen-loss escape clone a growth penalty "
                         "-- 0.0425 against 0.055 for the sensitive clone, and about 15% against the "
                         "0.050 resistance clone it derives from. The route-8 blind spot was built "
                         "with the resistance clone's growth unmodified and NO antigen-loss penalty "
                         "at all. The same biological state is charged 15% when it is acquired and "
                         "0% when it is present at baseline.",
    "is_the_asymmetry_defensible": "partly. A cell that lost the antigen by mutation plausibly took "
                                   "collateral damage; a cell that never expressed it may be a "
                                   "stable lineage variant with no damage. But the antigens at issue "
                                   "-- surface vimentin, CD31, B7-H3 -- are functional endothelial "
                                   "proteins, and an endothelial tumour cell that does without them "
                                   "is not obviously paying nothing. Zero was an assumption, not a "
                                   "finding, and it was the assumption that made the blind spot "
                                   "maximally dangerous.",
    "what_correcting_it_does": "nothing decisive. Charging the blind spot the engine's own 15% "
                              "penalty, or 30%, or 50%, leaves ten-year durability at 0.000. A "
                              "slower exponential is still an exponential.",
    "what_it_does_do": "it lowers the holding rate the orthogonal agent must out-run, which lowers "
                       "the required rate slightly. It is a discount on the answer, not an "
                       "alternative to it.",
    "why_it_is_recorded_anyway": "because it was an error in my own model that favoured my own "
                                 "conclusion -- it made the problem look harder and therefore made "
                                 "the expensive answer look more necessary. Errors in that direction "
                                 "are the ones worth writing down.",
}

THE_ONE_REASON_ALL_THREE_FAIL = {
    "the_result": "containment, coverage and fitness cost all fail, and they fail identically. Each "
                  "makes the blind spot SMALLER or SLOWER. Neither is enough, because over 3650 days "
                  "any positive net growth rate reaches carrying capacity from any starting size.",
    "the_arithmetic": "at the most extreme combination tested -- 99.99% coverage, a 70% growth "
                      "penalty -- the blind spot still reaches the detection floor in 581 days.",
    "the_structural_statement": "route 8's dangerous case admits exactly one kind of answer: "
                                "something that makes the blind spot's NET GROWTH NEGATIVE. Nothing "
                                "that merely slows it qualifies, at any magnitude short of total.",
    "why_this_is_worth_more_than_the_three_negatives": "it converts an open-ended search into a "
                                                       "closed one. The question is no longer 'is "
                                                       "there another angle' but 'what else kills "
                                                       "this cell', and that is answerable. It also "
                                                       "means the expensive answer is NECESSARY "
                                                       "rather than an artifact of the assumptions I "
                                                       "happened to pick -- which is the opposite of "
                                                       "what I expected to find when I went looking.",
    "the_honest_note": "I went looking for a cheaper answer and found a proof that there isn't one "
                       "of that kind. That is a better outcome than a fourth unanchored mechanism, "
                       "but it is not the outcome I was hoping for.",
}

# =============================================================================================
# 4. THE THIRD KILL MECHANISM -- WHICH EXISTS, AND HAS BEEN GIVEN TO DOGS WITH THIS DISEASE.
# =============================================================================================

METRONOMIC_CHEMOTHERAPY_WAS_TESTED_AND_FAILED = {
    "citation": "Matsuyama et al. 2020, J Small Anim Pract, PMID 30209807",
    "why_it_was_the_best_candidate": "metronomic cyclophosphamide is given to dogs continuously for "
                                     "months to years, so it is the one agent in this whole analysis "
                                     "that would clear the duration criterion outright. It kills by "
                                     "alkylation, needs no antigen, and does not act through "
                                     "PI3K/mTOR. On paper it passes every gate.",
    "the_result": "'The addition of metronomic chemotherapy DOES NOT IMPROVE OUTCOME for canine "
                  "splenic haemangiosarcoma.' 39 dogs on splenectomy plus maximum-tolerated-dose "
                  "chemotherapy against 22 dogs with metronomic added; median progression-free "
                  "survival 165 days and median overall survival 180 days in the comparison group.",
    "why_it_matters": "this is the disease, the species and the setting. It is not a mechanism that "
                      "has never been tried -- it is one that was tried here and did not work. "
                      "Passing the gates on paper is not the same as working.",
}

EBAT_IS_THE_THIRD_MECHANISM = {
    "citation": "Borgatti et al. 2017, Mol Cancer Ther 16(5):956-965, PMID 28193671",
    "what_it_is": "eBAT, a bispecific angiotoxin: truncated deimmunized Pseudomonas exotoxin fused "
                  "to EGF and the amino-terminal fragment of urokinase, so it binds EGFR and uPAR "
                  "and targets tumour and tumour neovasculature simultaneously.",
    "how_it_kills": "Pseudomonas exotoxin A ADP-ribosylates elongation factor 2, arresting protein "
                    "synthesis. The receptor binding is delivery; the kill is ribosomal.",
    "why_it_clears_the_orthogonality_gate": "a cell resistant to PI3K/mTOR inhibition has no reason "
                                            "to resist elongation-factor inactivation -- there is no "
                                            "shared node. And EGFR/uPAR are unrelated to the vaccine "
                                            "antigens (surface vimentin, CD31, B7-H3), so a cell "
                                            "null for one has no reason to be null for the other.",
    "the_trial": "SRCBST-1: 23 dogs with spontaneous stage I-II SPLENIC HEMANGIOSARCOMA, "
                 "splenectomised, MINIMAL RESIDUAL DISEASE, given one cycle of eBAT (50 ug/kg, "
                 "Monday/Wednesday/Friday) followed by adjuvant doxorubicin.",
    "the_result": "'eBAT improved 6-month survival from <40% in a comparison population to "
                  "approximately 70% in dogs treated at a biologically active dose. Six dogs were "
                  "LONG-TERM SURVIVORS, living >450 days.'",
    "why_the_setting_is_exactly_right": "minimal residual disease after splenectomy is precisely what "
                                        "this model simulates. Almost every other anchor in this "
                                        "analysis had to be transported from another species, "
                                        "another tumour, or another clinical setting. This one is "
                                        "the disease, the species and the setting.",
    "the_cancer_stem_cell_claim": "'the data indicate that eBAT targets cancer stem cells' -- a "
                                  "quiescent therapy-surviving population of the same class the "
                                  "persister argument is aimed at, reached by a completely different "
                                  "mechanism.",
    "the_coverage_question_it_reintroduces": "eBAT needs its own targets, so it does not escape the "
                                             "coverage problem -- it replaces one coverage question "
                                             "with a second, INDEPENDENT one. That is a real "
                                             "improvement rather than a shuffle: two independent 95% "
                                             "coverages leave 0.25% doubly blind rather than 5%. But "
                                             "nobody has measured EGFR or uPAR expression on the "
                                             "vaccine-blind fraction, so the independence is assumed.",
}

EBAT_ALSO_HAS_A_NEGATIVE_TRIAL_AND_IT_IS_INFORMATIVE = {
    "citation": "Borgatti et al. 2021, Vet Comp Oncol, PMID 32187827 (SRCBST-2)",
    "what_was_changed": "eligibility expanded to stage 3, the interval between eBAT and chemotherapy "
                        "reduced, and the course expanded from one cycle to THREE cycles at the same "
                        "biologically active dose.",
    "the_result": "'A statistically significant survival benefit was NOT seen'. 25 dogs; six had "
                  "acute hypotension with two requiring hospitalisation. The authors conclude that "
                  "repeated cycles 'led to GREATER TOXICITY AND REDUCED EFFICACY compared with a "
                  "single cycle'.",
    "so_more_is_worse": "the obvious way to get more log-kill out of eBAT -- give more of it -- has "
                        "been tried and is ruled out by data, not by argument. Any plan that assumes "
                        "eBAT can simply be scaled up is contradicted by the only trial that tried.",
    "the_convergence_with_the_model": "the finite-course simulation found that a short CONTINUOUS "
                                      "course works and that pulsing or repeating does not. eBAT's "
                                      "two trials found single-cycle benefit and three-cycle harm. "
                                      "Those are the same shape of answer arrived at independently.",
    "why_that_convergence_must_not_be_oversold": "SRCBST-2 changed three things at once -- stage "
                                                 "eligibility, the chemotherapy interval, and the "
                                                 "number of cycles -- so the failure cannot be "
                                                 "attributed to cycle number alone. It is "
                                                 "suggestive, and it is confounded.",
}


def one_off_logs_from_survival(control_6mo: float, treated_6mo: float,
                               net_growth: float = BLIND_SPOT_NET_GROWTH_PER_DAY,
                               readout_days: float = 182.0) -> float:
    """Natural logs of one-off kill implied by a shift in six-month survival.

    A single short course does not change the growth rate; it removes a fixed amount of tumour and
    the curve resumes. So the right currency is LOGS REMOVED, not a per-day rate. Assuming
    exponential survival, the median shifts by some delay, and a delay of D days against a
    compartment regrowing at `net_growth` per day means the course removed D * net_growth logs.
    """
    for s in (control_6mo, treated_6mo):
        if not 0.0 < s < 1.0:
            raise ValueError("survival fractions must lie strictly between 0 and 1")
    if treated_6mo <= control_6mo:
        raise ValueError("treated survival must exceed control for this to describe a benefit")
    median_control = math.log(2) * readout_days / -math.log(control_6mo)
    median_treated = math.log(2) * readout_days / -math.log(treated_6mo)
    return float((median_treated - median_control) * net_growth)


TOTAL_LOGS_REQUIRED = math.log(blind_spot_initial_cells())

EBAT_EFFECT_IN_LOGS = {
    # (control 6-month survival, treated 6-month survival): logs of one-off kill implied
    "reported": one_off_logs_from_survival(0.40, 0.70),
    "if_the_comparison_arm_was_worse": one_off_logs_from_survival(0.35, 0.70),
    "if_the_treated_arm_was_weaker": one_off_logs_from_survival(0.40, 0.65),
}

HOW_MUCH_OF_THE_JOB_EBAT_DOES = {
    "logs_required": TOTAL_LOGS_REQUIRED,
    "logs_delivered_range": (min(EBAT_EFFECT_IN_LOGS.values()), max(EBAT_EFFECT_IN_LOGS.values())),
    "fraction_of_the_job": tuple(v / TOTAL_LOGS_REQUIRED for v in
                                 (min(EBAT_EFFECT_IN_LOGS.values()),
                                  max(EBAT_EFFECT_IN_LOGS.values()))),
    "the_reading": "eBAT's measured canine hemangiosarcoma benefit corresponds to roughly 5-8 "
                   "natural logs of one-off kill against the 18.8 the blind spot requires -- about "
                   "a quarter to two fifths of the job. It is not a closure on its own, and the one "
                   "trial that tried to scale it up made things worse.",
    "the_assumptions_this_rests_on": "exponential survival in both arms, a historical rather than "
                                     "randomised comparison group, and the model's own net growth "
                                     "rate for the blind spot. The middle one is the weakest: "
                                     "'<40% in a comparison population' is not a control arm.",
    "why_it_is_still_the_best_anchored_number_here": "every other effect size in this route came "
                                                     "from another species, another tumour or a "
                                                     "genetic knockout. This one came from dogs with "
                                                     "splenic hemangiosarcoma after splenectomy.",
}


def required_rate_after_a_head_start(logs_removed: float, course_days: float = 335.0) -> float:
    """Rate a ferroptosis course needs once something else has already removed `logs_removed`."""
    remaining = TOTAL_LOGS_REQUIRED - logs_removed
    if remaining <= 0:
        return 0.0
    return float(BLIND_SPOT_NET_GROWTH_PER_DAY + remaining / course_days)


THE_COMBINATION_THAT_IS_NOW_LEGITIMATE = {
    "what_was_refused_before": "`hsa_orthogonal_kill` declined to model partial restoration plus "
                               "partial persister kill, on the grounds that 'combining two "
                               "unmeasured quantities to clear a threshold would be exactly the "
                               "arithmetic this analysis has refused elsewhere'. That was right.",
    "why_this_combination_is_different": "eBAT's contribution is MEASURED, in this disease, in this "
                                         "species, in this clinical setting. Combining one measured "
                                         "quantity with one unmeasured one is not the same "
                                         "arithmetic as combining two unmeasured ones. It is still "
                                         "weaker than combining two measured ones.",
    "what_it_buys": {
        # logs supplied by eBAT: rate a subsequent one-year ferroptosis course then needs
        0.0: required_rate_after_a_head_start(0.0),
        5.2: required_rate_after_a_head_start(5.2),
        7.2: required_rate_after_a_head_start(7.2),
        10.8: required_rate_after_a_head_start(10.8),
    },
    "the_reading": "eBAT's measured effect cuts the one-year ferroptosis requirement from 0.090/day "
                   "to 0.055-0.074/day -- a 17-39% discount -- or equivalently shortens the course "
                   "needed at a fixed 0.060/day from 708 days to 300-510.",
    "the_sequencing_that_the_data_supports": "eBAT is given as a single cycle between surgery and "
                                             "chemotherapy, in minimal residual disease. That is the "
                                             "moment the blind spot is smallest and the head start "
                                             "is cheapest to deliver. It is also, per SRCBST-2, the "
                                             "only schedule that has worked.",
    "what_has_never_been_tested": "eBAT with anything on the ferroptosis axis, in any species. This "
                                  "combination has never been tested. It is arithmetic laid over one "
                                  "measured effect and one assumed one, not an observed synergy, and "
                                  "the toxicity of the pair is unknown. An earlier draft of this "
                                  "entry said 'two separately measured effects', which is false -- "
                                  "the ferroptosis side is exactly the thing that has never been "
                                  "measured, and saying otherwise would have quietly promoted the "
                                  "whole combination a rank above what it is.",
}

ONCOLYTIC_VIRUS_IS_AN_ANECDOTE_NOT_EVIDENCE = {
    "citation": "2025, Veterinary Sciences, PMID 41150061",
    "the_case": "a three-year-old dog with primary BONE hemangiosarcoma received oncolytic vesicular "
                "stomatitis virus in an osteosarcoma trial before the HSA diagnosis was made, then "
                "amputation and doxorubicin. It survived more than seven years and was alive at "
                "writing.",
    "why_it_is_mechanistically_interesting": "viral tropism does not require the vaccine antigen and "
                                             "lysis does not act through the kinase pathway, so an "
                                             "oncolytic virus clears both gates by construction, and "
                                             "immunogenic lysis could restore visibility as well as "
                                             "kill.",
    "why_it_is_recorded_as_an_anecdote": "n = 1, a different anatomical form of the disease, and the "
                                         "virus was given for a misdiagnosis. A single long survivor "
                                         "in a disease with a six-month median is exactly the "
                                         "observation that is most likely to be selection rather "
                                         "than effect. No rate is derived from it and none should be.",
}

VERDICT_ON_THE_SEARCH = {
    "what_was_looked_for": "a cheaper or fundamentally different way to close route 8's dangerous "
                           "case than 'see the cell or kill the cell'.",
    "what_was_found_on_the_cheap_side": "nothing, and a structural reason why. Containment, coverage "
                                        "and fitness cost all make the blind spot smaller or slower, "
                                        "and over a ten-year horizon neither is enough. The case "
                                        "admits only answers that make net growth negative.",
    "what_was_found_on_the_kill_side": "a third mechanism, better anchored than either of the "
                                       "existing two: eBAT is orthogonal to both axes by "
                                       "construction, and it is the only agent in this entire "
                                       "analysis with a published effect size in dogs with splenic "
                                       "hemangiosarcoma in the minimal-residual-disease setting. It "
                                       "supplies roughly a quarter to two fifths of the required "
                                       "log-kill and cannot be scaled up, because the trial that "
                                       "tried made outcomes worse.",
    "the_net_effect_on_the_verdict": "route 8's dangerous case stays CLOSED CONDITIONAL ON A NAMED "
                                     "EXPERIMENT, but the closure is better supported and the "
                                     "remaining ask is smaller. It is no longer a single unanchored "
                                     "mechanism; it is a measured partial answer plus a smaller "
                                     "unanchored remainder.",
    "what_would_change_it_most_now": "measure EGFR and uPAR on the vaccine-blind fraction of canine "
                                     "hemangiosarcoma. If the cells the vaccine cannot see still "
                                     "express eBAT's targets, then an agent that already exists and "
                                     "has already been given to these dogs attacks the exact "
                                     "compartment with no answer -- and that is a stain, not a "
                                     "programme.",
    "the_thing_i_still_cannot_say": "that route 8 is closed. Three independent mechanisms now point "
                                    "at it and one of them has canine trial data, but no combination "
                                    "of them has been tested against a resistant antigen-null "
                                    "subpopulation, because nobody has ever shown that such a "
                                    "subpopulation exists in this disease.",
}


# =============================================================================================
# THE SIMULATED CONFIRMATION.
#
# The structural argument above is arithmetic: any positive net growth reaches carrying capacity
# from any starting size over 3650 days. Arithmetic can be wrong about a simulation, so the
# simulation was run. Twenty combinations, no persister kill and no restored presentation, drug
# stopped at year one -- the same setup that gave 0.000 at 95% coverage in `hsa_antigen_adequacy`.
# =============================================================================================

COVERAGE_TIMES_FITNESS_COST = {
    # antigen coverage: {antigen-null growth penalty: 10-year durability}
    0.950: {0.00: 0.000, 0.15: 0.000, 0.30: 0.000, 0.50: 0.000},
    0.970: {0.00: 0.000, 0.15: 0.000, 0.30: 0.000, 0.50: 0.000},
    0.980: {0.00: 0.000, 0.15: 0.000, 0.30: 0.000, 0.50: 0.000},
    0.990: {0.00: 0.000, 0.15: 0.000, 0.30: 0.000, 0.50: 0.000},
    0.995: {0.00: 0.000, 0.15: 0.000, 0.30: 0.000, 0.50: 0.000},
}

WHAT_THE_SWEEP_SETTLES = {
    "the_result": "twenty of twenty combinations return 0.000. Coverage from 95% to 99.5%, "
                  "antigen-null growth penalty from none to half, and every cell is a total loss.",
    "why_a_uniformly_null_table_is_the_strongest_form_of_this_result": "a sweep that found a "
                                                                      "threshold somewhere would "
                                                                      "invite tuning -- push "
                                                                      "coverage a little further, "
                                                                      "assume a slightly larger "
                                                                      "fitness cost. There is "
                                                                      "nothing to tune toward. The "
                                                                      "table has no gradient because "
                                                                      "the mechanism has no "
                                                                      "gradient: these levers change "
                                                                      "WHEN the blind spot arrives, "
                                                                      "not WHETHER.",
    "the_one_reading_it_does_not_support": "that the levers are worthless in general. A ninety-nine "
                                           "percent coverage vaccine is a better vaccine and a "
                                           "fitness cost is real biology. They are worthless "
                                           "AGAINST THIS SPECIFIC FAILURE, which is a claim about "
                                           "route 8's dangerous case and not about vaccine design.",
    "and_it_confirms_the_arithmetic_rather_than_replacing_it": "the structural argument predicted "
                                                               "exactly this, including that the "
                                                               "highest coverage tested would still "
                                                               "fail. The simulation was run because "
                                                               "an argument that predicts a uniform "
                                                               "result is the easiest kind to be "
                                                               "quietly wrong about.",
}
