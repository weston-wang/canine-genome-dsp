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
    TUMOR_CELLS,
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


# =============================================================================================
# THE ASSUMPTION UNDER THE STRUCTURAL RESULT: THAT THE BLIND SPOT IS A FIXED COMPARTMENT.
#
# Every route-8 probe passed `mutation=np.eye(7)` -- an identity transition matrix, asserting that
# no cell ever changes phenotype. The engine supports interconversion natively
# (`state[t+1] = grown @ model.mutation`), so this was never a limitation of the tooling. It was an
# assumption, it was never examined, and it does enormous work: under it the antigen-null state is
# a permanent sanctuary, and the only exit is death.
# =============================================================================================

BLIND_SPOT_DOUBLING_DAYS = math.log(2) / 0.050
GENERATIONS_OVER_HORIZON = HORIZON_DAYS / BLIND_SPOT_DOUBLING_DAYS


def null_lineage_surviving(per_generation_reversion: float,
                           generations: float = GENERATIONS_OVER_HORIZON) -> float:
    """Fraction of an antigen-null lineage still null after `generations`, given per-division reversion."""
    if not 0.0 <= per_generation_reversion < 1.0:
        raise ValueError("per_generation_reversion must lie in [0, 1)")
    return float((1.0 - per_generation_reversion) ** generations)


THE_STABILITY_THE_DANGEROUS_CASE_REQUIRES = {
    "the_arithmetic": "the blind spot doubles about every 14 days, so reaching the ten-year horizon "
                      "takes roughly 263 cell generations. For route 8's dangerous case to be real, "
                      "the antigen-null state has to be heritable and stable across every one of "
                      "them.",
    "generations": GENERATIONS_OVER_HORIZON,
    "how_fragile_that_requirement_is": {
        # per-generation reversion probability: fraction of the lineage still null at ten years
        0.100: null_lineage_surviving(0.100),
        0.010: null_lineage_surviving(0.010),
        0.001: null_lineage_surviving(0.001),
    },
    "the_reading": "a per-division reversion probability of one in ten leaves essentially none of "
                   "the lineage still invisible at ten years. One in a hundred leaves seven percent. "
                   "The dangerous case does not merely require antigen loss -- it requires antigen "
                   "loss that does not drift for 263 divisions.",
    "why_this_is_the_right_question": "it converts 'is the blind spot dangerous' from a question "
                                      "about size or coverage, which the sweep showed is worthless, "
                                      "into a question about STABILITY, which is a different "
                                      "physical property with a different experiment behind it.",
    "what_the_persister_literature_says": "the analogous drug-tolerant state is explicitly not "
                                          "stable: 'their partial resistance phenotype is TRANSIENT "
                                          "AND REVERSIBLE upon removal of the drug', and persisters "
                                          "'are not necessarily preexisting dormant cells; in fact, "
                                          "they may be INDUCED'. If the resistance half of the "
                                          "overlap is a transient state, the overlap has to be "
                                          "maintained by two independent unstable properties at "
                                          "once.",
    "what_cuts_the_other_way": "antigen-presentation loss is sometimes genetic and then it does not "
                               "drift at all. Zaretsky's melanomas acquired resistance through "
                               "loss-of-function JAK1/JAK2 mutations 'concurrent with deletion of "
                               "the wild-type allele', and B2M truncating mutations are a recurrent "
                               "immune-escape lesion. A deleted gene is stable for 263 generations "
                               "and for any number after that.",
    "so_the_question_has_a_binary_answer": "if the blind spot's antigen-null state is epigenetic, it "
                                           "leaks and cannot persist. If it is genetic, it is a "
                                           "permanent sanctuary. Both exist in real tumours. Nobody "
                                           "has looked in canine hemangiosarcoma.",
}

PLASTICITY_DRAINS_THE_SANCTUARY_BUT_ONLY_THE_EPIGENETIC_PART = {
    "the_mechanism": "if an antigen-null cell regains the antigen at rate q per day, it becomes "
                     "visible to the 0.042/day vaccine already in the regimen and is killed. No new "
                     "agent is involved. The null compartment's net growth becomes its growth minus "
                     "q, so it SHRINKS once q exceeds the holding rate of 0.0334/day -- a mean "
                     "residence in the null state of about thirty days.",
    "the_two_way_version": "if the state is reversible it is reversible both ways, so cells also "
                           "re-enter the null state at q_in. I first estimated closure by a "
                           "time-averaging argument -- the lineage spends q_out/(q_out + q_in) of "
                           "its time visible, so closure needs that fraction to exceed "
                           "0.0334/0.042 = 0.795. THAT ESTIMATE IS WRONG and is superseded by "
                           "`THE_TWO_WAY_RESULT_INVERTS_THE_IDEA`. Time-averaging treats the "
                           "lineage as well-mixed; the correct object is the dominant eigenvalue of "
                           "the two-compartment system, and it is stricter. At q_out = 0.08 and "
                           "q_in = 0.02 the lineage is visible 80% of the time -- comfortably past "
                           "0.795 -- and the exact eigenvalue is +0.0034/day, positive. The "
                           "simulation agrees: 0.000.",
    "why_this_is_not_a_closure_on_its_own": "it drains the epigenetically silenced fraction and does "
                                            "nothing whatever to a genetically deleted one. If any "
                                            "part of the blind spot is genetically null, that part "
                                            "behaves exactly like the original clone -- and the "
                                            "structural result says a compartment with positive net "
                                            "growth reaches carrying capacity from ANY starting "
                                            "size. Plasticity shrinks the sanctuary; it does not "
                                            "abolish it unless the genetic fraction is exactly zero.",
    "what_it_therefore_is": "a log-remover, in exactly the same currency as eBAT. Draining a 1.5e8 "
                            "blind spot down to a genetically-null remnant of 1e5 removes 7.3 "
                            "natural logs; down to 1e3 removes 11.9.",
    "and_it_is_free": "no drug, no dosing, no duration criterion. It is a property the tumour either "
                      "has or does not have, and it is the only lever in this entire analysis that "
                      "costs nothing if it happens to be true.",
}

BYSTANDER_KILLING_FAILS_FOR_A_REASON_WORTH_RECORDING = {
    "the_idea": "antibody-drug conjugates with cleavable linkers and membrane-permeable payloads "
                "kill antigen-NEGATIVE cells by payload diffusion from antigen-positive neighbours. "
                "It is the established answer to heterogeneous antigen expression, it is clinically "
                "validated in HER2-low and heterogeneous disease, and it clears both gates here: it "
                "does not need the antigen on the target cell, and MMAE-class payloads act on "
                "tubulin rather than through the kinase pathway.",
    "citation": "Singh & Shah 2017, J Pharmacokinet Pharmacodyn, PMID 27670282",
    "the_finding_that_kills_it": "'the bystander effect of ADC INCREASES WITH INCREASING FRACTION OF "
                                 "Ag+ CELLS', and 'the bystander effect of the ADC can DISSIPATE "
                                 "OVER THE PERIOD OF TIME AS THE POPULATION OF Ag+ CELLS DECLINES'.",
    "why_that_is_fatal_in_this_setting": "bystander killing is manufactured by the antigen-positive "
                                         "cells. This regimen's entire purpose is to eliminate them. "
                                         "So the mechanism is strongest at the start and gone "
                                         "precisely when the blind spot is all that is left. It "
                                         "shrinks the compartment early and cannot hold it down "
                                         "late.",
    "the_shape_this_shares_with_containment": "competitive release fails because killing the "
                                              "sensitive cells removes the competition suppressing "
                                              "the blind spot. Bystander killing fails because "
                                              "killing the sensitive cells removes the factory "
                                              "making the payload. Both are mechanisms whose supply "
                                              "is the very population the plan is designed to "
                                              "destroy. That is a category of false answer worth "
                                              "naming, because it is not obvious in advance and two "
                                              "separate good ideas fell into it.",
    "what_it_still_is": "a log-remover applied early, like eBAT. Not a floor-holder.",
}

# =============================================================================================
# THE DECOMPOSITION THAT THE WHOLE SEARCH HAS BEEN CONVERGING ON.
# =============================================================================================

def required_rate_decomposed(holding_rate: float, surviving_cells: float,
                             course_days: float = 335.0) -> float:
    """The route-8 requirement, split into the two terms that have different levers.

        required = holding_rate + ln(surviving_cells) / course_days

    The first term is irreducible by anything that removes cells: whatever is left must be killed
    faster than it grows, for as long as it exists. The second is the cost of clearing what remains
    in the time available, and every "log-remover" in this analysis reduces it.
    """
    if surviving_cells < 1.0:
        return 0.0
    if course_days <= 0:
        raise ValueError("course_days must be positive")
    return float(holding_rate + math.log(surviving_cells) / course_days)


THE_TWO_TERMS_AND_THEIR_DIFFERENT_LEVERS = {
    "the_form": "required rate = HOLDING RATE + ln(surviving cells) / course days.",
    "term_1_the_floor": "the holding rate, 0.0334/day at the nadir density this regimen achieves. "
                        "Whatever survives has to be killed faster than it grows, for as long as it "
                        "exists. NO amount of up-front cell removal touches this term. It is the "
                        "irreducible ask, and in assay units it is a 9.5% three-day kill.",
    "what_actually_lowers_the_floor": {
        # antigen-null growth penalty: resulting irreducible three-day kill
        0.00: 0.095,
        0.15: 0.082,
        0.30: 0.068,
        0.50: 0.049,
    },
    "the_reconciliation_this_provides": "the three levers dismissed earlier are not worthless -- "
                                        "they are terms in this equation that are insufficient on "
                                        "their own. A fitness cost lowers the floor. Containment "
                                        "lowers the floor by raising density, at a burden cost this "
                                        "disease cannot pay. Coverage lowers the second term, "
                                        "logarithmically and therefore feebly. Each was correctly "
                                        "rejected as a CLOSURE and each is real as a TERM.",
    "term_2_the_work": "ln(surviving cells) over the course length. Every log-remover reduces it: "
                       "eBAT by a measured 5.2-7.8, plasticity by however far it drains the "
                       "epigenetic fraction, bystander killing by whatever it achieves before the "
                       "antigen-positive population is gone.",
    "why_this_is_the_answer_to_looking_deeper": "there is no fourth mechanism hiding. There is a "
                                                "two-term requirement, one term that only killing "
                                                "can satisfy and one that several things can chip "
                                                "at, and the honest closure is a STACK rather than a "
                                                "single agent. That is a more useful statement than "
                                                "any of the individual mechanisms, because it says "
                                                "what would have to be true rather than what might "
                                                "work.",
}

THE_STACK = {
    # description: (logs removed up front, resulting one-year requirement per day)
    "nothing": (0.0, required_rate_decomposed(BLIND_SPOT_NET_GROWTH_PER_DAY, blind_spot_initial_cells())),
    "eBAT alone": (7.2, required_rate_decomposed(BLIND_SPOT_NET_GROWTH_PER_DAY,
                                                 blind_spot_initial_cells() * math.exp(-7.2))),
    "plasticity to a 1e5 genetic remnant": (
        math.log(blind_spot_initial_cells()) - math.log(1e5),
        required_rate_decomposed(BLIND_SPOT_NET_GROWTH_PER_DAY, 1e5)),
    "eBAT plus plasticity to 1e5": (
        7.2 + math.log(blind_spot_initial_cells()) - math.log(1e5),
        required_rate_decomposed(BLIND_SPOT_NET_GROWTH_PER_DAY, 1e5 * math.exp(-7.2))),
}

WHAT_THE_STACK_MEANS = {
    "the_numbers": "nothing: 0.090/day, a 24% three-day kill. eBAT alone: 0.068/day, 18%. Plasticity "
                   "down to a 1e5 genetic remnant: 0.068/day, 18%. Both together: 0.046/day, 13%.",
    "the_floor_they_converge_on": "0.0334/day, a 9.5% three-day kill, which no stacking can go "
                                  "below because something must still out-run the compartment's own "
                                  "growth.",
    "why_this_is_progress": "the standalone ask was a 24% three-day kill from an agent with no "
                            "chronic canine dosing record. The stacked ask is 13%, approaching a "
                            "floor of 9.5%. That is not a different kind of answer, but it is a "
                            "materially smaller one, and two of the three contributions are things "
                            "that either already exist or cost nothing.",
    "what_it_still_does_not_do": "it does not remove the need for a sustained killing agent. Both "
                                 "log-removers act up front; neither holds the floor. If no agent "
                                 "can sustain 0.0334/day against this compartment, route 8's "
                                 "dangerous case does not close, and no amount of stacking changes "
                                 "that.",
    "the_single_experiment_that_decides_the_most": "sequence the antigen locus and the "
                                                   "antigen-presentation machinery in the "
                                                   "drug-tolerant fraction of canine "
                                                   "hemangiosarcoma. Genetic loss means a permanent "
                                                   "sanctuary and the full stack is needed. "
                                                   "Epigenetic silencing means the sanctuary leaks, "
                                                   "and the vaccine already in the plan drains it "
                                                   "for free.",
}


# =============================================================================================
# WHAT CAN HOLD THE FLOOR?
#
# The decomposition splits the requirement into a term that up-front killing reduces and a term
# that nothing reduces. eBAT, plasticity and bystander killing are all up-front: they remove logs
# and stop. The floor -- out-running the compartment's own growth for as long as it exists -- needs
# something PERMANENT.
#
# Every drug in this analysis fails that on the duration criterion, and the criterion is not a
# technicality: it disqualified the MEK/mTOR pair at 215x and icFSP1 at 261x, and it killed the one
# chronically-dosed ferroptosis-adjacent agent on canine keratoconjunctivitis sicca at week 22.
#
# There is exactly one class of killer that is permanently present by construction.
# =============================================================================================

ONLY_IMMUNITY_IS_PERMANENT = {
    "the_structural_argument": "the floor requires a kill rate sustained for as long as the "
                               "compartment exists, which on this horizon is a decade. No small "
                               "molecule in this analysis has cleared a duration criterion at that "
                               "scale, and the one agent that is dosed chronically in dogs failed on "
                               "a canine-specific toxicity at study week 22. A drug that must be "
                               "given for ten years is the shape of answer this analysis keeps "
                               "rejecting.",
    "what_is_left": "the immune system, which is present for the life of the animal at no recurring "
                    "toxicity cost. That is why the vaccine carries the plan in the first place. The "
                    "problem is specific and narrow: the vaccine is ANTIGEN-DIRECTED, and this "
                    "compartment is defined by not having the antigen.",
    "the_one_immune_arm_that_does_not_need_the_antigen": "NKG2D-mediated NK recognition. NKG2D "
                                                         "ligands -- MIC-A and MIC-B among eight -- "
                                                         "are 'poorly expressed on normal cells but "
                                                         "become upregulated on the surface of "
                                                         "damaged, transformed or infected cells'. "
                                                         "They are STRESS markers, not lineage "
                                                         "antigens, so they are independent of the "
                                                         "vaccine target and of MHC-I.",
    "why_the_persister_state_is_the_right_target_for_it": "the compartment this has to cover is a "
                                                          "cell surviving sustained therapeutic "
                                                          "pressure. Stress-ligand induction is "
                                                          "exactly what that state should produce. "
                                                          "The mechanism and the target are matched "
                                                          "rather than borrowed -- which is not true "
                                                          "of anything else proposed for this "
                                                          "compartment.",
    "the_canine_evidence": "Canter et al. 2018, J Immunother Cancer, PMID 29254507: dog NK cells "
                           "(CD5dim, NKp46+) expanded 19-fold to 2.6e8 cells; post-radiotherapy "
                           "cytotoxicity reached about 80% at effector:target ratios of 10:1 in "
                           "vitro; allogeneic NK cells 'produced significant PDX tumour growth delay "
                           "in vivo'; and there was a FIRST-IN-DOG clinical trial in spontaneous "
                           "osteosarcoma combining radiotherapy with intratumoral autologous NK "
                           "transfer.",
    "why_that_evidence_is_the_right_species_and_the_wrong_tumour": "canine, sarcoma, in vivo, and "
                                                                   "into a real clinical trial. It "
                                                                   "is osteosarcoma rather than "
                                                                   "hemangiosarcoma, and nothing "
                                                                   "here was measured against a "
                                                                   "resistant antigen-null "
                                                                   "compartment.",
}

WHY_NK_STILL_DOES_NOT_CLOSE_IT = {
    "the_first_problem_is_that_transferred_cells_are_a_pulse": "adoptively transferred NK cells do "
                                                               "not persist indefinitely without "
                                                               "cytokine support. A course of NK "
                                                               "transfer is another log-remover, not "
                                                               "a floor-holder. The floor argument "
                                                               "only works for ENDOGENOUS "
                                                               "surveillance, which is permanent by "
                                                               "construction but is also whatever it "
                                                               "already is in a dog whose tumour "
                                                               "grew anyway.",
    "the_second_problem_is_the_documented_escape": "tumours shed soluble MIC-A and MIC-B, which decoy "
                                                   "NKG2D and impede NK cytotoxicity -- already "
                                                   "recorded in `hsa_orthogonal_kill."
                                                   "NK_CELLS_ARE_PARTLY_REHABILITATED`. An arm that "
                                                   "the tumour can disable by secretion is not a "
                                                   "reliable floor-holder.",
    "the_third_problem_is_that_no_rate_exists": "80% cytotoxicity at 10:1 in a short in vitro assay "
                                               "is not a per-day rate in a living animal, and "
                                               "converting it would be the same category error this "
                                               "analysis already retracted once. No number is "
                                               "derived from it here.",
    "what_it_nonetheless_changes": "it identifies the shape of the only answer that can satisfy the "
                                   "floor term without a ten-year drug. Everything else on offer is "
                                   "up-front. If route 8's dangerous case closes durably rather than "
                                   "by a finite course, it closes through antigen-independent innate "
                                   "surveillance, and the question becomes whether that can be tuned "
                                   "high enough rather than whether a new molecule can be found.",
}

# =============================================================================================
# THE FINAL POSITION.
# =============================================================================================

WHAT_LOOKING_DEEPER_ACTUALLY_FOUND = {
    "the_honest_headline": "no single mechanism closes route 8's dangerous case, and the search "
                           "produced something better than a fourth candidate: a decomposition that "
                           "says what any closure must supply, and a reason why several attractive "
                           "ideas cannot supply it.",
    "the_requirement": "required rate = holding rate + ln(surviving cells) / course days. The second "
                       "term is negotiable and several things reduce it. The first is not, and it is "
                       "a 9.5% three-day kill sustained for as long as the compartment exists.",
    "the_two_kinds_of_answer": "LOG-REMOVERS act up front and stop -- eBAT (measured, 5.2-7.8 logs, "
                               "cannot be scaled), plasticity (free if the loss is epigenetic, "
                               "useless if genetic), bystander killing (dissipates as its own supply "
                               "is destroyed). FLOOR-HOLDERS must be permanent, which rules out "
                               "every drug here on the duration criterion and leaves only "
                               "antigen-independent innate surveillance.",
    "the_trap_that_caught_two_good_ideas": "competitive release and ADC bystander killing both "
                                           "depend on the antigen-positive population the regimen "
                                           "exists to destroy. A mechanism whose supply is the thing "
                                           "you are eliminating cannot hold a late compartment. That "
                                           "is not obvious in advance and it is worth naming.",
    "the_two_experiments_that_decide_it": "first, sequence the antigen locus and the presentation "
                                          "machinery in the drug-tolerant fraction -- genetic loss "
                                          "means a permanent sanctuary and the full stack is needed, "
                                          "epigenetic silencing means the sanctuary leaks and the "
                                          "vaccine drains it for free. Second, stain that same "
                                          "fraction for EGFR, uPAR and NKG2D ligands, which decides "
                                          "whether the two agents that already exist can reach it.",
    "the_status_i_will_not_upgrade": "route 8's dangerous case remains CLOSED CONDITIONAL ON A NAMED "
                                     "EXPERIMENT. It is better supported than it was -- the ask has "
                                     "come down from a 24% three-day kill to about 13% stacked, "
                                     "against a floor of 9.5% -- and it is not closed. Nobody has "
                                     "yet shown that the compartment this is all about exists in "
                                     "canine hemangiosarcoma at all.",
    "what_would_make_me_call_it_closed": "a measured per-day kill rate, in canine hemangiosarcoma, "
                                         "against a drug-tolerant antigen-null fraction, exceeding "
                                         "the holding rate and sustainable for the horizon. Every "
                                         "element of that sentence is currently missing, and the "
                                         "decomposition is what makes it a checkable sentence rather "
                                         "than an aspiration.",
}


# =============================================================================================
# THE PLASTICITY SIMULATION, WHICH INVERTED THE IDEA IT WAS BUILT TO TEST.
# =============================================================================================

PLASTICITY_RESCUE = {
    # q_out (antigen-null -> antigen-positive, per day):
    #   {"one_way": durability with no back-conversion, "q_in_0.005": ..., "q_in_0.02": ...}
    0.000: {"one_way": 0.000, "q_in_0.005": None, "q_in_0.02": None},
    0.005: {"one_way": 0.000, "q_in_0.005": 0.000, "q_in_0.02": 0.000},
    0.010: {"one_way": 0.000, "q_in_0.005": 0.000, "q_in_0.02": 0.000},
    0.020: {"one_way": 0.000, "q_in_0.005": 0.000, "q_in_0.02": 0.000},
    0.034: {"one_way": 0.000, "q_in_0.005": 0.000, "q_in_0.02": 0.000},
    0.050: {"one_way": 0.267, "q_in_0.005": 0.000, "q_in_0.02": 0.000},
    0.080: {"one_way": 0.233, "q_in_0.005": 0.008, "q_in_0.02": 0.000},
}


def two_compartment_growth_rate(q_out: float, q_in: float,
                                net_growth: float = BLIND_SPOT_NET_GROWTH_PER_DAY,
                                vaccine_kill: float = 0.042) -> float:
    """Dominant eigenvalue of the antigen-positive / antigen-null resistant pair, per day.

    The visible compartment grows at `net_growth` and is killed at `vaccine_kill`; the null one
    grows at `net_growth` and is killed by nothing. Cells move null -> visible at q_out and back at
    q_in. The lineage's fate is the dominant eigenvalue of

        [[g - k - q_in,   q_out ],
         [     q_in,     g - q_out]]

    which is the correct object. A time-averaged "fraction of life spent visible" estimate is not,
    and gave the wrong answer at the one place the two disagree.
    """
    g, k = net_growth, vaccine_kill
    tr = (g - k - q_in) + (g - q_out)
    det = (g - k - q_in) * (g - q_out) - q_out * q_in
    disc = tr * tr - 4.0 * det
    if disc < 0:
        return float(tr / 2.0)
    return float((tr + math.sqrt(disc)) / 2.0)


THE_TWO_WAY_RESULT_INVERTS_THE_IDEA = {
    "what_the_one_way_case_shows": "with no back-conversion, plasticity does partially rescue: "
                                   "durability rises from 0.000 to 0.267 once the null state's mean "
                                   "residence falls to about twenty days. That is a real effect from "
                                   "no new agent at all.",
    "but_it_saturates_immediately": "faster reversion does not help. q_out = 0.080 gives 0.233 "
                                    "against 0.267 at 0.050 -- the same within Monte Carlo noise at "
                                    "120 trials. The eigenvalue explains why: once the null "
                                    "compartment drains quickly, the rate-limiting step stops being "
                                    "the drain and becomes the ANTIGEN-POSITIVE resistant clone's "
                                    "own net decline, which is only g - k = -0.0086/day. Plasticity "
                                    "can at best make the blind spot as controllable as a visible "
                                    "resistant clone, and that clone is barely controlled.",
    "and_it_never_reaches_the_no_blind_spot_baseline": "0.267 against roughly 0.84 with no blind "
                                                       "spot at all. Even perfect one-way plasticity "
                                                       "recovers about a third of what the blind "
                                                       "spot costs.",
    "THE_FINDING_THAT_MATTERS": "back-conversion destroys it. At q_in = 0.005/day -- a mean "
                                "residence of 200 days in the VISIBLE state, which is slow -- the "
                                "rescue collapses from 0.267 to 0.000. At q_in = 0.02 every "
                                "q_out tested gives 0.000, including one where cells spend 80% of "
                                "their life visible.",
    "why_that_happens": "reversibility is symmetric. A state that can be exited can be entered, and "
                        "the antigen-positive resistant population is a standing reservoir that "
                        "continuously MANUFACTURES new blind-spot cells. The same property that "
                        "drains the sanctuary also refills it, and the model says the refilling "
                        "wins at strikingly low rates.",
    "so_plasticity_is_not_a_free_gift": "I went into this expecting plasticity to be the cheap "
                                        "closure -- no drug, no duration criterion, just a property "
                                        "the tumour might happen to have. The simulation says the "
                                        "opposite: a plastic antigen phenotype is a LIABILITY, "
                                        "because it gives the tumour a route into the sanctuary that "
                                        "a fixed phenotype does not. The only configuration that "
                                        "helps is one-way escape from the null state, which is "
                                        "biologically the least likely of the three.",
    "the_estimate_this_corrects": "my own time-averaging argument put the threshold at 79.5% of life "
                                  "spent visible. At 80% visible the exact eigenvalue is +0.0034/day "
                                  "and the simulation returns 0.000. The naive estimate sits right "
                                  "on the boundary and falls on the wrong side of it, which is the "
                                  "worst place for an approximation to be.",
    "how_the_eigenvalue_tracks_the_simulation": "every sign matches. Positive eigenvalue gives 0.000 "
                                                "in all five such cells; negative gives non-zero in "
                                                "two of three, the exception being q_out = 0.08 with "
                                                "q_in = 0.005 at -0.0042/day, which returns 0.008 -- "
                                                "a marginal eigenvalue where other escape routes "
                                                "dominate before the drain finishes.",
}


# =============================================================================================
# THE PINCER: WHAT ESCAPES THE T-CELL ARM IS THE ENTRY CONDITION FOR THE NK ARM.
#
# The decomposition demands a floor-holder, and only immunity is permanent. That is a constraint,
# not yet an answer. The answer needs a reason why the immune system should cover THIS compartment
# specifically, and there is a structural one.
#
#   - Lose only the vaccine's antigen and keep MHC-I: the cell still presents everything else, so
#     polyvalent antigens and epitope spreading reach it. Already in the analysis.
#   - Lose MHC-I to escape T cells altogether: that is exactly what "missing self" describes.
#
# The two arms are complementary rather than redundant, and the escape from one is the entry
# condition for the other. There is no phenotype that evades both by antigen status alone.
# =============================================================================================

MISSING_SELF_IS_THE_COMPLEMENT_OF_THE_VACCINE = {
    "citation": "Malmberg et al. 2017, Immunogenetics, PMID 28699110",
    "the_statement": "'Immune selection during tumor checkpoint inhibition therapy PAVES WAY FOR "
                     "NK-cell missing self recognition'. Loss of HLA class I 'may result from immune "
                     "selection of escape variants by tumor-specific CD8 T cells'.",
    "why_it_matters_here": "the pressure that creates route 8's dangerous case is the same pressure "
                           "that makes it an NK target. The vaccine selects for cells that cannot "
                           "present; cells that cannot present are missing-self. This is not two "
                           "agents stacked, it is one escape route feeding another mechanism's "
                           "recognition criterion.",
    "the_logical_pincer": "a cell can drop the vaccine's antigen and keep MHC-I -- then polyvalent "
                          "antigens and epitope spreading reach it. Or it can drop MHC-I -- then "
                          "missing-self reaches it. Antigen status alone does not provide an escape "
                          "from both.",
    "and_why_this_is_the_only_candidate_that_fits_the_floor": "NK surveillance is endogenous and "
                                                              "permanent. It carries no duration "
                                                              "criterion, which every drug in this "
                                                              "analysis has failed. A floor-holder "
                                                              "has to be permanent, and this is the "
                                                              "only permanent thing on the list.",
}

PINCER_RESCUE = {
    # NK kill/day on the antigen-null compartments:
    #   {"no_escape": durability, "hla_e_5pct": ..., "hla_e_20pct": ...}
    0.000: {"no_escape": 0.000, "hla_e_5pct": None, "hla_e_20pct": None},
    0.020: {"no_escape": 0.000, "hla_e_5pct": 0.000, "hla_e_20pct": 0.000},
    0.034: {"no_escape": 0.000, "hla_e_5pct": 0.000, "hla_e_20pct": 0.000},
    0.042: {"no_escape": 0.308, "hla_e_5pct": 0.308, "hla_e_20pct": 0.308},
    0.060: {"no_escape": 0.833, "hla_e_5pct": 0.833, "hla_e_20pct": 0.825},
    0.090: {"no_escape": 0.825, "hla_e_5pct": 0.825, "hla_e_20pct": 0.825},
}

NO_BLIND_SPOT_BASELINE = 0.84

THE_PINCER_CLOSES_IT = {
    "the_result": "an NK kill of 0.060/day applied to the antigen-null compartments takes ten-year "
                  "durability from 0.000 to 0.833 -- which IS the no-blind-spot baseline of about "
                  "0.84. Route 8's dangerous case is not mitigated, it is removed.",
    "the_signature_that_it_is_a_real_closure": "it saturates at the baseline rather than climbing "
                                               "past it. 0.090/day gives 0.825, the same. You cannot "
                                               "do better than removing the problem, and a mechanism "
                                               "that stops exactly there is behaving like a closure "
                                               "rather than like an extra source of kill.",
    "the_threshold_is_exactly_where_the_decomposition_said": "0.034/day -- a 9.7% three-day kill, "
                                                             "essentially the 0.0334 holding rate -- "
                                                             "still gives 0.000, because at the "
                                                             "holding rate net growth is zero rather "
                                                             "than negative. 0.042 gives 0.308 and "
                                                             "0.060 gives 0.833. The transition sits "
                                                             "on the floor the decomposition "
                                                             "predicted, derived independently.",
    "what_it_costs": "a 16.5% three-day kill sustained on the antigen-null compartment. That is "
                     "roughly twice the irreducible floor and it is the SMALLEST ask any candidate "
                     "in this analysis has produced for this compartment -- against 24% for a "
                     "one-year ferroptosis course and 13% for the best stack.",
    "why_it_is_cheaper_than_everything_else": "because it never stops. A permanent holder carries no "
                                              "ln(N0)/days work term at all -- it only has to beat "
                                              "the floor. Every finite course has to clear the "
                                              "backlog as well, and that is what made the other asks "
                                              "larger.",
}

THE_HLA_E_HOLE_AND_WHAT_IT_ACTUALLY_COSTS = {
    "the_documented_escape": "a tumour can drop classical MHC-I to evade T cells while retaining or "
                             "upregulating HLA-E, which engages the inhibitory CD94/NKG2A receptor "
                             "and switches NK off. That is the hole in the pincer.",
    "citation": "Cancer Cell 2023, PMID 36706761: 'Immune checkpoint HLA-E:CD94-NKG2A mediates "
                "evasion of CIRCULATING TUMOR CELLS from NK cell surveillance', with "
                "platelet-derived RGS18 driving HLA-E expression.",
    "why_that_paper_is_uncomfortably_well_matched_to_this_disease": "it is about circulating tumour "
                                                                    "cells and the driver is "
                                                                    "PLATELET-derived. "
                                                                    "Hemangiosarcoma is a tumour of "
                                                                    "blood vessels that disseminates "
                                                                    "haematogenously and consumes "
                                                                    "platelets to the point of "
                                                                    "causing disseminated "
                                                                    "intravascular coagulation. If "
                                                                    "there is a tumour where a "
                                                                    "platelet-driven NK escape "
                                                                    "should be expected, it is this "
                                                                    "one.",
    "what_the_simulation_says_it_costs": "almost nothing, at 5% or 20% of the null compartment: "
                                         "0.833 against 0.833, and 0.825 against 0.833. The hole is "
                                         "not load-bearing.",
    "why_not_and_this_is_the_important_part": "because the NK-evading cells in this test are "
                                              "DRUG-SENSITIVE. The primary agent runs throughout and "
                                              "covers them. A cell that evades the vaccine and NK but "
                                              "still answers to the drug is not a sanctuary.",
    "the_case_that_would_be_dangerous": "a compartment that is antigen-null AND NK-evading AND "
                                        "drug-resistant. That is not tested above, and it does not "
                                        "need to be: it is by construction the original blind spot "
                                        "with the NK arm removed, which returns 0.000. The pincer "
                                        "closes route 8 exactly to the extent that the triple "
                                        "overlap is absent.",
    "the_pattern_this_repeats": "`hsa_antigen_adequacy.OVERLAP_IS_THE_WHOLE_BALLGAME` found that a "
                                "blind spot only matters where it overlaps drug resistance. The same "
                                "rule reappears one level up: an NK escape only matters where it "
                                "overlaps the other two. Every level of this analysis has turned on "
                                "an intersection rather than on any single property.",
}

WHY_THIS_IS_STILL_NOT_A_CLOSURE_I_WILL_CLAIM = {
    "no_rate_has_been_measured": "0.060/day against an antigen-null drug-tolerant compartment in "
                                 "canine hemangiosarcoma is a requirement, not an observation. The "
                                 "canine NK evidence is osteosarcoma, and the in vitro cytotoxicity "
                                 "figures are not per-day rates in an animal.",
    "endogenous_nk_is_already_present_and_the_tumour_grew_anyway": "the strongest objection, and it "
                                                                   "is mine rather than a paper's. "
                                                                   "Every dog with hemangiosarcoma "
                                                                   "already has NK cells, and the "
                                                                   "disease killed it. Whatever "
                                                                   "surveillance exists at baseline "
                                                                   "is evidently below the threshold "
                                                                   "in the compartments that matter. "
                                                                   "The pincer therefore requires NK "
                                                                   "function to be AUGMENTED, not "
                                                                   "merely present -- and that "
                                                                   "reintroduces an intervention "
                                                                   "with its own duration question.",
    "the_shedding_escape_is_unaddressed": "soluble MIC-A and MIC-B decoy NKG2D. Missing-self and "
                                          "NKG2D are different recognition modes and shedding "
                                          "attacks the second, but a tumour under NK pressure has "
                                          "documented routes to blunt both.",
    "dla_e_is_unknown": "the HLA-E hole is characterised in humans. The canine equivalent, DLA-E, has "
                        "not been examined in hemangiosarcoma, so the size of the hole in the species "
                        "this analysis is about is simply unknown.",
    "the_honest_status": "this is the first mechanism in the analysis that is structurally the RIGHT "
                         "SHAPE -- permanent, antigen-independent, complementary to the vaccine by "
                         "construction rather than by addition, and cheapest in required potency "
                         "precisely because it never stops. It is not a demonstrated closure. It "
                         "moves route 8 from 'needs a drug nobody has' to 'needs an immune arm "
                         "everyone has, working harder than it evidently does'.",
}


PINCER_REPRODUCIBILITY = {
    # NK kill/day: durability at three independent Monte Carlo seeds (7, 101, 202)
    0.034: (0.000, 0.000, 0.000),
    0.042: (0.308, 0.290, 0.290),
    0.060: (0.833, 0.860, 0.890),
}

WHY_THE_RESEED_MATTERS = {
    "what_was_checked": "the headline pincer result is the strongest claim in this analysis, so it "
                        "was re-run at two further seeds rather than reported from one.",
    "the_threshold_is_exact_in_all_three": "0.034/day -- the holding rate -- returns 0.000 at every "
                                           "seed, with no partial values. That is what a genuine "
                                           "threshold looks like, and it is the point the "
                                           "decomposition predicted before this simulation was "
                                           "written.",
    "the_closure_lands_at_the_baseline_every_time": "0.060/day gives 0.833, 0.860 and 0.890 against "
                                                    "a no-blind-spot baseline of about 0.84. The "
                                                    "spread is Monte Carlo noise around the "
                                                    "baseline, not a trend.",
    "what_it_does_not_establish": "reproducibility across seeds tests the simulation, not the "
                                  "biology. Every seed shares the same model, the same holding rate "
                                  "and the same assumption that missing-self recognition reaches "
                                  "this compartment at all. A stable wrong answer is still wrong.",
}


# =============================================================================================
# THE PINCER HAS BEEN ATTEMPTED IN DOGS. IT FAILED, AND THE FAILURE IS INSTRUCTIVE.
#
# The model says the pincer closes route 8 if NK activity can be sustained at 0.060/day against the
# antigen-null compartment. The obvious objection was mine: every dog already has NK cells and dies
# anyway, so the arm must be AUGMENTED. That is a testable proposition, and it has been tested.
# =============================================================================================

AUGMENTING_NK_WAS_TRIED_IN_DOGS_AND_MADE_THINGS_WORSE = {
    "citation": "NCI-COTC030 phase 2, Frontiers in Immunology 2025, PMID 41209004",
    "why_this_is_the_right_trial_to_check": "adjuvant inhaled recombinant human IL-15 after "
                                            "amputation and before chemotherapy in dogs with "
                                            "appendicular osteosarcoma. That is the pincer's exact "
                                            "setting -- minimal residual disease after surgery, on "
                                            "chemotherapy -- and its exact strategy: raise NK "
                                            "activity to control what surgery left behind.",
    "the_hypothesis": "two weeks of inhaled rhIL-15 would cut metastatic failure at the end of "
                      "chemotherapy from a historical 40% to 20%, powered at 80% with 40 dogs.",
    "the_result": "'Unexpectedly, disease-free survival and overall survival were statistically "
                  "INFERIOR for dogs in the intent-to-treat population compared to a well-validated "
                  "historical control cohort, so the trial was HALTED FOR FUTILITY.'",
    "the_authors_conclusion": "'Inhaled rhIL-15 combined with amputation and chemotherapy is "
                              "associated with WORSE OUTCOMES in dogs with OSA.'",
    "how_this_lands_on_the_pincer": "it is the strongest negative in this entire analysis, because "
                                    "it is not a mechanism that was never tried -- it is the pincer's "
                                    "own premise, executed in the right species and the right "
                                    "clinical setting, producing worse survival than doing nothing.",
    "what_it_does_not_show": "it does not show missing-self recognition cannot reach an antigen-null "
                             "compartment, and it is osteosarcoma rather than hemangiosarcoma. It "
                             "shows that ONE way of trying to raise NK activity, in a "
                             "surgery-plus-chemotherapy setting, failed.",
}

WHY_IT_FAILED_IS_MEASURED_AND_IT_MATTERS = {
    "the_setting_suppresses_the_very_arm_the_pincer_needs": "'Cytotoxicity assays of PBMCs showed "
                                                            "significant DECREASES after both "
                                                            "surgery and chemotherapy with an "
                                                            "overall decrease from the start to end "
                                                            "of therapy (-18.2 +/- 16.1%, "
                                                            "P<0.001).' Inflammatory cytokines "
                                                            "including IL-6 rose after amputation "
                                                            "and after chemotherapy, correlating "
                                                            "with the fall in cytotoxicity.",
    "why_that_is_a_problem_the_model_does_not_capture": "the simulation applies a constant NK kill "
                                                        "from the start of therapy. The trial says "
                                                        "the real trajectory in this setting is "
                                                        "DOWNWARD, and that the treatment the plan "
                                                        "already includes -- surgery, then "
                                                        "chemotherapy -- is what drives it down. The "
                                                        "pincer's floor-holder is weakest exactly "
                                                        "when it is most needed.",
    "the_second_mechanism_is_exhaustion": "IL-15 stimulation raises activation AND exhaustion "
                                          "markers, TIGIT in particular, in human soft tissue "
                                          "sarcoma specimens and in dogs receiving inhaled IL-15 "
                                          "(PMID 33158916). Pushing the accelerator also engages the "
                                          "brake.",
    "the_signal_inside_the_failure": "'Some dogs demonstrated POSITIVE fold change in PBMC "
                                     "cytotoxicity, which correlated significantly with IMPROVED dog "
                                     "survival (P = 0.004, r = 0.62).' Where NK cytotoxicity "
                                     "actually rose, dogs lived longer.",
    "why_that_line_is_the_most_important_one_here": "it separates the premise from the execution. "
                                                    "The pincer's premise -- that NK activity "
                                                    "against residual disease translates into "
                                                    "survival -- is SUPPORTED by this trial, at r = "
                                                    "0.62 in the right species. What failed is the "
                                                    "attempt to deliver that rise with inhaled IL-15 "
                                                    "in a setting that was pushing it down.",
    "the_honest_reading": "this is neither a refutation of the pincer nor a rescue of it. It is "
                          "evidence that the mechanism matters and that the obvious way of engaging "
                          "it does not work, which is a more specific position than either.",
}

WHAT_THE_CORRECTED_VERSION_WOULD_HAVE_TO_BE = {
    "release_the_brake_rather_than_only_pressing_the_accelerator": "'Ex vivo, combined IL-15 and "
                                                                   "TIGIT blockade using soft tissue "
                                                                   "sarcoma blood and tumour "
                                                                   "specimens significantly "
                                                                   "increased cytotoxicity against "
                                                                   "STS targets', and the same group "
                                                                   "built a novel anti-TIGIT "
                                                                   "antibody and ran the canine work "
                                                                   "alongside the human "
                                                                   "(PMID 33158916).",
    "and_the_hole_in_the_pincer_has_its_own_agent": "anti-NKG2A. Monalizumab 'enhanced NK cell "
                                                    "activity against various tumor cells and "
                                                    "rescued CD8+ T cell function', with a 31% "
                                                    "objective response rate in a phase II "
                                                    "combination (PMID 30503213). That is the "
                                                    "documented HLA-E escape addressed by a drug "
                                                    "that exists.",
    "the_timing_implication_the_trial_forces": "if surgery and chemotherapy suppress NK cytotoxicity "
                                               "by about 18%, then delivering a floor-holder in that "
                                               "window is the worst possible schedule. Either the "
                                               "immune arm is engaged before that suppression, or "
                                               "after it recovers, or the suppression itself has to "
                                               "be mitigated. The model has no opinion on this "
                                               "because it applies a constant rate.",
    "what_has_never_been_tested": "IL-15 with TIGIT blockade in vivo in any dog; NKG2A blockade in "
                                  "any dog; either against hemangiosarcoma; and none of it against "
                                  "an antigen-null drug-tolerant compartment, which remains a "
                                  "compartment nobody has shown exists in this disease.",
}

THE_PINCER_VERDICT_AFTER_THE_TRIAL = {
    "what_survives": "the structure. Missing-self is still the complement of the vaccine by "
                     "construction, NK is still the only permanent floor-holder available, the "
                     "required rate is still the smallest ask in the analysis, and the trial's own "
                     "correlation between rising cytotoxicity and survival supports the premise in "
                     "the right species.",
    "what_does_not": "any suggestion that this is close to deliverable. The one prospective "
                     "multicentre canine trial of adjuvant NK augmentation was halted for futility "
                     "with worse survival than controls, and the setting the pincer occupies is the "
                     "setting that suppresses NK function most.",
    "the_status": "route 8's dangerous case remains CLOSED CONDITIONAL ON A NAMED EXPERIMENT. The "
                  "pincer changes what kind of experiment that is -- from finding a molecule to "
                  "measuring and then sustaining an immune function -- and the trial above shows "
                  "that second thing is harder than it sounds, not easier.",
    "the_sentence_i_would_stand_behind": "the eighth escape route has a structurally correct answer "
                                         "with correlative canine support for its premise, no "
                                         "demonstrated way to deliver it, and one failed attempt "
                                         "that explains itself. That is a real position and it is "
                                         "not a closure.",
    "why_finding_this_was_worth_more_than_not_finding_it": "the pincer looked like the cleanest "
                                                           "result in the analysis until this trial "
                                                           "was checked. Reporting it without "
                                                           "checking whether anyone had tried it "
                                                           "would have repeated the exact failure "
                                                           "mode this whole project keeps catching: "
                                                           "an attractive mechanism, no prior-art "
                                                           "search, and a conclusion one rank "
                                                           "stronger than the evidence.",
}


# =============================================================================================
# THE CORRELATION I ASSUMED, WHICH INFLATED THE PROBLEM BY FIVE ORDERS OF MAGNITUDE.
#
# Every route-8 probe, including the ones in `hsa_antigen_adequacy`, built the blind spot as
#
#     init[6] = positive * (1 - phi)
#
# which asserts that the ENTIRE antigen-null fraction is also drug-resistant -- a resistant fraction
# of five percent. The model's own pre-existing resistance seeding produces a resistant fraction of
# about 8.6e-6 (median over 2000 draws). I overrode the model's own parameter by roughly 6000-fold
# and never noticed, because the override was implicit in how the compartment was constructed.
# =============================================================================================

MEASURED_PREEXISTING_RESISTANT_FRACTION = {
    "median": 8.56e-6,
    "mean": 1.06e-4,
    "how_it_was_obtained": "2000 draws of `mapk_resistance.sample_initial_state` with this "
                           "analysis's own seeding weights and pre-existing probability, summing "
                           "clones 1-3 and dividing by total burden.",
    "fraction_of_draws_with_any_resistant_cell": 0.72,
}


def double_negative_cells(coverage: float = 0.95, resistant_fraction: float = 8.56e-6,
                          burden: float = 0.3, tumour_cells: float = TUMOR_CELLS) -> float:
    """Cells that are BOTH antigen-null and drug-resistant, if the two are independent."""
    if not 0.0 <= coverage < 1.0:
        raise ValueError("coverage must lie in [0, 1)")
    return float(burden * (1.0 - coverage) * resistant_fraction * tumour_cells)


THE_CORRELATION_ASSUMPTION_WAS_MINE_AND_IT_WAS_WRONG = {
    "what_i_assumed": "that antigen-nullity and drug resistance are perfectly correlated -- every "
                      "cell lacking the vaccine antigen also carries a resistance mechanism. That "
                      "gives a dangerous compartment of 0.3 * 0.05 * 1e10 = 1.5e8 cells.",
    "what_the_model_itself_says": "the pre-existing resistant fraction is about 8.6e-6. Under "
                                  "independence the double-negative compartment is 0.3 * 0.05 * "
                                  "8.6e-6 * 1e10, about 1300 cells.",
    "the_inflation": 1.5e8 / 1284.0,
    "in_logs": math.log(1.5e8 / 1284.0),
    "why_independence_is_the_right_default_for_ROUTE_8": "route 8 is antigen inadequacy ON DAY ZERO "
                                                         "-- baseline heterogeneity in expression "
                                                         "level -- not antigen loss acquired under "
                                                         "immune pressure. A cell that happens not "
                                                         "to express surface vimentin has no "
                                                         "mechanistic reason to also carry a "
                                                         "pre-existing PIK3CA-pathway mutation. "
                                                         "Correlation is the right default for ROUTE "
                                                         "4, where loss is acquired under selection, "
                                                         "and I applied route 4's assumption to "
                                                         "route 8.",
    "what_the_earlier_module_did_test": "`hsa_antigen_adequacy` reports that 'splitting the null "
                                        "fraction half drug-sensitive and half drug-resistant gives "
                                        "0.000 as well'. That is true, and it stopped FIVE ORDERS OF "
                                        "MAGNITUDE short of the independent value. Testing 0.5 when "
                                        "the model implies 8.6e-6 is not a sensitivity analysis.",
    "what_this_changes": "the work term. ln(1.5e8) = 18.8 natural logs becomes ln(1300) = 7.2. The "
                         "one-year course requirement falls from 0.090/day to 0.055/day, a 15.2% "
                         "three-day kill.",
    "what_this_does_not_change": "the floor. A compartment of 1300 cells growing at 0.0334/day "
                                 "reaches the detection threshold in about 330 days and progresses "
                                 "just as surely as one of 1.5e8. Size sets the work, never the "
                                 "floor -- which is the structural result restated, and it is why "
                                 "correcting this error does not by itself close route 8.",
    "the_uncomfortable_part": "this error made the problem look five orders of magnitude harder than "
                              "the model's own parameters imply, and it survived every previous pass "
                              "including one explicitly hunting for assumptions that favoured my "
                              "conclusions. It was invisible because it lived in how the compartment "
                              "was CONSTRUCTED rather than in a number anyone would think to check.",
}

# =============================================================================================
# THE PATTERN ACROSS EVERY ADJUVANT TRIAL IN THIS DISEASE.
# =============================================================================================

TOCERANIB_MAINTENANCE_WAS_TRIED_AND_FAILED = {
    "citation": "Gardner et al. 2015, BMC Vet Res, PMID 26062540",
    "why_it_was_a_strong_floor_holder_candidate": "toceranib is an approved canine tyrosine kinase "
                                                  "inhibitor given chronically for years, so it "
                                                  "clears the duration criterion outright. It hits "
                                                  "VEGFR2/PDGFR/KIT -- a different kinase axis from "
                                                  "the PI3K/mTOR resistance this compartment "
                                                  "carries -- in a tumour of endothelial origin that "
                                                  "should depend on that axis.",
    "the_trial": "43 dogs, stage I-II SPLENIC hemangiosarcoma, splenectomy then five cycles of "
                 "doxorubicin, then toceranib MAINTENANCE at 3.25 mg/kg every other day in the 31 "
                 "dogs still free of metastasis.",
    "the_result": "median disease-free interval 161 days and median survival 172 days in the "
                  "toceranib-treated dogs. 'The use of toceranib following DOX chemotherapy DOES NOT "
                  "IMPROVE either disease free interval or overall survival in dogs with stage I or "
                  "II HSA.'",
    "why_it_matters_most_of_all_the_negatives": "this is a chronic maintenance agent, in this exact "
                                                "disease, in this exact adjuvant setting, doing "
                                                "exactly what a floor-holder is supposed to do. It "
                                                "is the closest thing to a direct test of the "
                                                "floor-holding strategy that exists, and it "
                                                "produced nothing.",
}

EVERY_MAINTENANCE_STRATEGY_IN_THIS_DISEASE_HAS_FAILED = {
    "the_tally": {
        "metronomic chemotherapy (61 dogs, splenic HSA)": "no improvement in outcome",
        "toceranib maintenance (43 dogs, splenic HSA)": "no improvement in DFI or survival",
        "inhaled IL-15 NK augmentation (canine OSA, phase 2)": "survival INFERIOR, halted for futility",
        "eBAT intensified to three cycles (25 dogs, splenic HSA)": "greater toxicity, reduced efficacy",
    },
    "the_one_thing_that_worked": "eBAT as a SINGLE SHORT CYCLE given early, between splenectomy and "
                                 "chemotherapy: 6-month survival from under 40% to about 70% in 23 "
                                 "dogs, with six long-term survivors.",
    "THE_PATTERN": "every attempt to add a sustained or intensified agent after surgery and "
                   "chemotherapy in canine splenic hemangiosarcoma has failed. The only intervention "
                   "that improved survival was one short course given early. Four negatives and one "
                   "positive, all pointing the same way.",
    "why_this_is_the_most_important_finding_in_the_module": "it is an EMPIRICAL verdict on the "
                                                            "floor-holding strategy, and it is "
                                                            "negative. The decomposition said route "
                                                            "8 needs a permanent holder; the "
                                                            "clinical record of this disease says "
                                                            "permanent holders do not work here and "
                                                            "early elimination does.",
    "and_it_matches_what_the_model_found_independently": "the finite-course simulation found that a "
                                                         "short continuous course closes route 8 and "
                                                         "that pulsing or repeating does not. Four "
                                                         "trials and one simulation, arrived at "
                                                         "separately, agree on the shape of the "
                                                         "answer.",
    "the_caution": "these trials are not tests of route 8. None of them measured an antigen-null "
                   "drug-tolerant compartment, and their failure has many possible explanations "
                   "besides the one being drawn here. This is a pattern across endpoints, not a "
                   "controlled comparison.",
}


CORRELATION_SWEEP = {
    # fraction of the antigen-null compartment that is also drug-resistant:
    #   {"cells": double-negative cells, "no_agent": durability, "ebat_5_2": ..., "ebat_7_2": ...}
    1e-0: {"cells": 1.5e8, "no_agent": 0.000, "ebat_5_2": 0.000, "ebat_7_2": 0.000},
    1e-1: {"cells": 1.5e7, "no_agent": 0.000, "ebat_5_2": 0.000, "ebat_7_2": 0.000},
    1e-2: {"cells": 1.5e6, "no_agent": 0.000, "ebat_5_2": 0.000, "ebat_7_2": 0.000},
    1e-3: {"cells": 1.5e5, "no_agent": 0.000, "ebat_5_2": 0.000, "ebat_7_2": 0.000},
    1e-4: {"cells": 1.5e4, "no_agent": 0.000, "ebat_5_2": 0.000, "ebat_7_2": 0.000},
    1e-5: {"cells": 1.5e3, "no_agent": 0.000, "ebat_5_2": 0.000, "ebat_7_2": 0.000},
}

RARITY_IS_NOT_A_DEFENCE = {
    "the_result": "durability is 0.000 at every correlation tested, from perfect down to "
                  "independent -- a compartment of 1.5e8 cells and a compartment of 1500 cells give "
                  "identically total failure. eBAT's 5.2 or 7.2 logs do not rescue any of them.",
    "why_eBAT_does_not_rescue_even_the_smallest": "1500 cells reduced by 7.2 logs leaves about 1.1 "
                                                  "cells, which is above the one-cell extinction "
                                                  "floor and regrows. The requirement and the "
                                                  "measured effect are the same size, and being the "
                                                  "same size is not the same as being enough.",
    "WHAT_THIS_CORRECTS_IN_MY_OWN_ACCOUNT": "having found that I inflated the compartment by five "
                                            "orders of magnitude, the natural inference is that the "
                                            "danger was correspondingly overstated. It was not. The "
                                            "correlation error inflated the WORK TERM -- the "
                                            "one-year ask falls from 0.090 to 0.055/day, which is "
                                            "real and worth having -- but it did not create the "
                                            "danger and correcting it does not reduce it. Route 8's "
                                            "dangerous case is binary in EXISTENCE, not graded in "
                                            "SIZE.",
    "the_sharpest_statement_of_route_8": "a compartment that nothing kills reaches carrying capacity "
                                         "within the horizon from any starting size above zero. "
                                         "Rarity is not a defence. Only absence is.",
    "what_that_means_for_whether_this_scenario_is_real": "the question is not 'how big is the "
                                                         "compartment' and never was. It is 'does a "
                                                         "compartment exist that is both invisible "
                                                         "to the vaccine and resistant to the drug'. "
                                                         "That is a yes/no question, nobody has "
                                                         "asked it in this disease, and it is "
                                                         "answerable by staining tissue that already "
                                                         "exists.",
    "the_honest_scope_of_the_concern": "this remains a compartment that has never been observed. "
                                       "What the sweep establishes is that if it is there at all, "
                                       "its scarcity will not save the animal -- so the "
                                       "justification for caring about it rests entirely on whether "
                                       "it exists, and not at all on how common it is.",
}


# =============================================================================================
# THE SECOND OMISSION: THE MODEL NEVER CONTAINED THE CHEMOTHERAPY EVERY ONE OF THESE DOGS GETS.
#
# The engine carries exactly two agents, both targeted: the PI3K/mTOR inhibitor and the MEK
# inhibitor. Doxorubicin is discussed in half a dozen modules and is in NONE of the simulations.
# Every dog in the eBAT trial, the toceranib trial, the metronomic trial and the standard of care
# receives five cycles of it.
#
# So "the blind spot is drug-resistant" has always meant resistant to the TARGETED agents. An
# anthracycline is neither antigen-directed nor kinase-directed, and PI3K-pathway resistance confers
# no anthracycline resistance -- that is a third, independent property. Giving the compartment zero
# anthracycline exposure was an assumption I never made explicit and never justified.
# =============================================================================================

DOXORUBICIN_WAS_NEVER_IN_THE_MODEL = {
    "what_the_engine_contains": "two agents. `ic50_nM`/`max_kill` for the PI3K/mTOR inhibitor and "
                                "`ic50_nM_2`/`max_kill_2` for the MEK inhibitor. There is no third "
                                "concentration channel and no cytotoxic.",
    "what_every_dog_actually_receives": "splenectomy, then five cycles of single-agent doxorubicin. "
                                        "That is the standard of care and it is the backbone of "
                                        "every trial cited in this module.",
    "why_the_omission_matters_specifically_for_route_8": "the compartment is defined by resisting "
                                                         "the targeted agents and by lacking the "
                                                         "vaccine antigen. Doxorubicin is neither "
                                                         "antigen-directed nor kinase-directed, so "
                                                         "route 8's defining properties give it no "
                                                         "protection at all from the one drug these "
                                                         "dogs certainly get.",
    "the_assumption_this_exposes": "every route-8 result in this analysis was computed for a regimen "
                                   "no dog actually receives, in which the dangerous compartment "
                                   "gets zero anthracycline. That is not conservatism -- it is an "
                                   "unstated and unjustified assumption of complete cross-resistance "
                                   "between a kinase inhibitor and a DNA-damaging cytotoxic.",
    "the_pattern_with_the_first_error": "both of my route-8 errors were the same kind. Neither was a "
                                        "wrong number: one was in how the compartment was "
                                        "CONSTRUCTED and the other in what the regimen OMITTED. "
                                        "Parameter audits do not catch either.",
}

DOXORUBICIN_EFFECT_IN_LOGS = {
    "surgery_alone_median_days": 86,
    "with_adjuvant_doxorubicin_median_days": 180,
    "timely_adjuvant_median_days": 238,
    "delayed_adjuvant_median_days": 146,
    "citations": "timely-versus-delayed adjuvant chemotherapy in non-metastatic splenic "
                 "hemangiosarcoma, 70 dogs, PMID 36633399: median overall survival 238 days when "
                 "chemotherapy started within 21 days of surgery against 146 days when later.",
    "logs_typical": (180 - 86) * BLIND_SPOT_NET_GROWTH_PER_DAY,
    "logs_timely": (238 - 86) * BLIND_SPOT_NET_GROWTH_PER_DAY,
    "logs_delayed": (146 - 86) * BLIND_SPOT_NET_GROWTH_PER_DAY,
    "the_conversion_caveat": "this is the same delay-times-growth-rate conversion used for eBAT, and "
                             "it inherits the same weakness: the survival benefit is measured on the "
                             "WHOLE tumour, which is mostly drug-sensitive, and is being applied to "
                             "a subcompartment. It is an estimate of what doxorubicin does in this "
                             "disease, not a measurement of what it does to this compartment.",
}

CLOSURE_BY_WHAT_THEY_ALREADY_GET = {
    # logs removed up front: 10-year durability at the corrected compartment size (1284 cells)
    0.0: 0.000,
    3.1: 0.000,          # doxorubicin alone, typical
    5.1: 0.000,          # doxorubicin alone, timely
    7.2: 0.000,          # eBAT alone
    8.3: 0.830,          # doxorubicin + eBAT, both at their PESSIMISTIC ends
    10.4: 0.830,
    12.9: 0.830,
}

THIS_IS_THE_CLOSURE_AND_IT_NEEDS_NO_NEW_DRUG = {
    "the_result": "at the corrected compartment size, neither doxorubicin alone nor eBAT alone "
                  "closes route 8's dangerous case -- both give 0.000. Together, at the PESSIMISTIC "
                  "end of both effect estimates, durability is 0.830, which is the no-blind-spot "
                  "baseline. It saturates there rather than climbing, the same signature the pincer "
                  "showed.",
    "the_threshold": "between 7.2 and 8.3 logs, which is ln(1284) = 7.16 plus the margin needed to "
                     "cross below one cell. The simulation reproduces the closed-form requirement "
                     "for a third time, derived independently each time.",
    "why_this_is_different_from_every_other_candidate": "no new agent. Doxorubicin is the standard of "
                                                        "care in this disease. eBAT has a positive "
                                                        "trial in 23 dogs with stage I-II splenic "
                                                        "hemangiosarcoma in the minimal-residual-"
                                                        "disease setting, and the sequencing that "
                                                        "works -- a single eBAT cycle between "
                                                        "splenectomy and chemotherapy -- is the "
                                                        "sequencing already used.",
    "and_it_clears_at_the_pessimistic_end": "8.3 logs is doxorubicin at its weakest published "
                                            "estimate plus eBAT at its weakest. Every more "
                                            "favourable combination also clears. The closure does "
                                            "not depend on optimistic readings of either.",
    "what_had_to_be_corrected_to_see_it": "two of my own errors, compounding. Assuming perfect "
                                          "correlation between antigen-nullity and kinase resistance "
                                          "inflated the requirement from 7.2 to 18.8 logs. Omitting "
                                          "doxorubicin removed 3-5 logs from the answer. Together "
                                          "they made a closable problem look unclosable, and neither "
                                          "was visible as a wrong parameter.",
    "THE_CAVEATS_THAT_STILL_STAND": {
        "the_compartment_may_also_resist_doxorubicin": "this is the load-bearing one. If the "
                                                       "compartment is anthracycline-resistant as "
                                                       "well, it is a TRIPLE negative and nothing in "
                                                       "the regimen covers it. Hemangiosarcoma is "
                                                       "clinically chemoresistant -- doxorubicin "
                                                       "roughly doubles a short median -- so a high "
                                                       "anthracycline-resistant fraction is entirely "
                                                       "plausible in this disease.",
        "the_conversion_is_from_bulk_survival": "both the doxorubicin and eBAT log estimates come "
                                                "from whole-tumour median survival applied to a "
                                                "subcompartment.",
        "ebat_targets_on_this_compartment_are_unmeasured": "EGFR and uPAR have not been stained on "
                                                           "the vaccine-blind fraction.",
        "and_the_compartment_itself_is_unverified": "nobody has shown that an antigen-null "
                                                    "drug-tolerant population exists in canine "
                                                    "hemangiosarcoma. This closes a compartment that "
                                                    "has never been observed.",
    },
    "the_honest_status": "route 8's dangerous case is CLOSED IN THE MODEL by the standard of care "
                         "plus one agent that already has a positive trial in this disease, at the "
                         "pessimistic end of both effect estimates, requiring no new molecule. That "
                         "is a materially stronger position than anything earlier in this analysis. "
                         "It is still conditional on the compartment being anthracycline-sensitive "
                         "and on it existing at all, and both are stains rather than programmes.",
}
