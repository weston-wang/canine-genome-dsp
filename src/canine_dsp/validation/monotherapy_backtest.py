"""Do the modelling tools reproduce outcomes that are already known?

DELIBERATELY SEPARATE FROM THE HS THERAPY ANALYSIS. This module validates the ENGINE. It imports
from the analysis modules to build scenarios and it changes none of them. Nothing here is a
therapeutic claim and nothing in the frozen findings depends on it.

THE FIRST FINDING IS THAT NO VALIDATION EXISTED
98 modules, 1,340 tests, and not one checked the engine against a case where the answer is already
published. Every existing test verifies internal consistency -- that a number matches what its
module says it should be -- which catches drift and cannot catch the model being wrong about the
disease.

FINDING 1: MOST PUBLISHED ENDPOINTS ARE NOT COMMENSURABLE WITH THE ENGINE'S OUTPUT
The engine reports progression-from-nadir at a 1%-of-carrying-capacity detection floor. Almost all
the canine HS literature reports median SURVIVAL. A dog can progress radiographically and live a
long time, so these are different quantities and comparing them is a category error.

The untreated arms make the trap concrete:

    arm                     model                    published
    intact, untreated       progresses in 5 days     CNS palliative: 5-day median survival
    debulked, no drug       progresses in 4 days     periarticular surgery alone: 398-day median

The first row looks like a triumph and is a coincidence -- with no drug the tumour clears a 1%
detection floor almost immediately at 0.06/day growth, which has nothing to do with time to death.
The second row is the same fact with the coincidence removed: 4 days against 398.

So the back-test has to be restricted to the one endpoint that genuinely matches: RELAPSE-FREE
FRACTION.

FINDING 2: THE ONE AVAILABLE APPLES-TO-APPLES BACK-TEST FAILS
Skorupski 2009 (PMID 19453368), 16 dogs, lomustine adjuvant after local therapy in localized canine
HS: 0.375 relapse-free, 568-day median survival. Same endpoint the engine emits, same disease, same
species, and lomustine is a drug this repo already parameterizes from real data (70 mg/m^2, q3wk,
105-day exposure cap derived from the documented cumulative-hepatotoxicity threshold).

Run as the sole agent, the model returns 0.000 relapse-free at every potency in
`CCNU_MAX_KILL_SWEEP` and at 568, 730 and 1825 days. Not "optimistic" or "pessimistic" -- flatly
unable to produce the observed number.

FINDING 3: THE REASON, WHICH IS STRUCTURAL AND NOT A CALIBRATION ERROR
Two hypotheses were tested and BOTH ARE WRONG, which is worth recording because each is the
plausible first guess:

  (a) "the tumour never gets small enough for an extinction threshold to catch" -- tested by
      applying floors at 1000 cells, 1 cell (K=1e9) and 1 cell (K=1e12). Cured fraction 0.000 at
      every one.
  (b) "every simulated dog starts with the same surgical residual, so a mixture outcome like
      37.5%/62.5% is unreachable" -- tested by sweeping the residual across SEVEN ORDERS OF
      MAGNITUDE, 9e-3 down to 1e-10. Relapse-free stayed 0.000 at every value.

The actual mechanism is arithmetic. Lomustine's course is capped at 105 days. Whatever nadir it
reaches, the drug then stops and the tumour regrows at ~0.06/day for the remaining 463 days of the
window -- a factor of e^(0.06*463) ~ 1.2e12. Any nonzero residual multiplied by 1.2e12 clears the
1% detection floor. And the residual is ALWAYS nonzero: the engine has no extinction state, so a
burden of 1e-82 is still a live population that regrows.

The potency sweep shows the same thing from the other side. Relapse-free is 0.000 up to max_kill
0.30 and 1.000 at 0.50 -- a step, with nothing in between. And the 1.000 is not a cure either: at
0.50 the nadir is ~1e-20, which after 1.2e12-fold regrowth is ~1e-8, still under the detection
floor at day 568. It is "has not become detectable yet", not "gone".

FINDING 4: WHAT THE ENGINE ACTUALLY COMPUTES
Relapse-free fraction is a genuine probability ONLY when the binding event is stochastic seeding of
a resistant clone. That is the continuous-drug-pressure regime, and it is the regime every headline
figure in this project sits in -- which is why those figures show real intermediate values (0.530,
0.893, 0.985).

When the binding event is instead regrowth of residual SENSITIVE disease -- which is what happens
in any finite course, i.e. every real adjuvant protocol -- regrowth is deterministic, there is no
trial-to-trial variation, and the output collapses to a step function of potency and horizon.

THE CONSEQUENCE THAT REACHES BACK INTO THE ANALYSIS
This project repeatedly concludes that duration-capped agents "buy delay rather than durability"
(`DURATION_CAP_GENERALIZATION`, and the stoppability bar of 0.060/day for the lung/no-antigen cell).
That conclusion cannot come out any other way. An engine with no extinction state and deterministic
regrowth of residual disease will ALWAYS say a finite course fails, regardless of the drug, the
dose, or the disease. It is a property of the tool, not a finding about histiocytic sarcoma.

Skorupski's 37.5% is the direct counterexample: a real finite course, in this exact disease, after
which more than a third of dogs did not relapse.

WHAT THIS DOES AND DOES NOT SAY ABOUT THE FROZEN FINDINGS
Does NOT invalidate the continuous-dosing durability figures. They live in the seeding-limited
regime the engine handles, and the failure here is in a regime they do not occupy.

DOES invalidate every statement about finite courses and stoppability, including the drugs-off bar
this project has quoted repeatedly. Those were generated by a mechanism that cannot produce any
other answer.

WHAT WOULD FIX IT
An extinction state -- burden below one cell becomes zero and stays zero -- plus stochastic cell
loss at low burden so that clearance becomes a probability rather than an asymptote. That is
standard in stochastic tumour models. It is a change to the engine, not to any analysis module, and
it is NOT made here: this module diagnoses, it does not patch.
"""

from __future__ import annotations

# --- the measured record, assembled from the citations already carried in this repo ---
# Only outcomes for a SINGLE agent or a single modality. Combination results are excluded.

MEASURED_MONOTHERAPY_OUTCOMES = {
    "lomustine_adjuvant_localized": {
        "citation": "Skorupski et al. 2009, Vet Comp Oncol 7:139-144, PMID 19453368",
        "n": 16, "setting": "localized canine HS, lomustine adjuvant after local therapy",
        "relapse_free_fraction": 0.375, "median_survival_days": 568,
        "COMMENSURABLE": True,
        "why": "Relapse-free fraction is the one endpoint the engine also emits.",
    },
    "lomustine_first_line_disseminated": {
        "citation": "Rassnick et al. 2010, J Vet Intern Med, PMID 21155191",
        "n": 21, "setting": "previously untreated, single-agent CCNU 90 mg/m^2 q4wk",
        "overall_response_rate": 0.29, "median_response_duration_days": 96,
        "COMMENSURABLE": False,
        "why": "RECIST-style response rate, not a relapse-free fraction at a horizon.",
    },
    "lomustine_mixed": {
        "citation": "Skorupski et al. 2007, J Vet Intern Med, PMID 17338159",
        "n": 58, "setting": "canine HS, CCNU 60-90 mg/m^2",
        "overall_response_rate": 0.46, "median_survival_days": 106,
        "COMMENSURABLE": False, "why": "Survival endpoint; also disagrees with Rassnick on ORR.",
    },
    "cns_definitive_local_therapy": {
        "citation": "primary CNS HS series", "n": 12,
        "setting": "definitive local therapy", "median_survival_days": 43,
        "COMMENSURABLE": False, "why": "Survival, not progression-from-nadir.",
    },
    "cns_palliative": {
        "citation": "primary CNS HS series", "n": 17,
        "setting": "palliative", "median_survival_days": 5,
        "COMMENSURABLE": False,
        "why": "Survival. Numerically close to the model's 5-day untreated progression, which is a "
               "COINCIDENCE -- see UNTREATED_ARM_IS_A_CATEGORY_ERROR.",
    },
    "periarticular_surgery_alone": {
        "citation": "periarticular HS series", "n": 49,
        "setting": "surgery alone", "median_survival_days": 398,
        "COMMENSURABLE": False,
        "why": "Survival. The model's debulked-untreated arm progresses in 4 days -- a 100x gap "
               "that means nothing, because the endpoints differ.",
    },
    "periarticular_radiation_alone": {
        "citation": "periarticular HS series", "n": 49,
        "setting": "radiation alone", "median_survival_days": 240,
        "COMMENSURABLE": False, "why": "Survival, and the engine has no radiation modality.",
    },
}

UNTREATED_ARM_IS_A_CATEGORY_ERROR = {
    "model_intact_untreated_progression_days": 5,
    "model_debulked_untreated_progression_days": 4,
    "published_cns_palliative_survival_days": 5,
    "published_periarticular_surgery_survival_days": 398,
    "the_trap": "The first pair matches to the day and it is meaningless. With no drug a tumour "
                "clears a 1%-of-carrying-capacity detection floor almost immediately at 0.06/day "
                "growth. That is not time to death. The second pair -- 4 days against 398 -- is the "
                "same fact with nothing to disguise it.",
    "the_rule_it_establishes": "Only relapse-free FRACTION may be compared. Every survival-median "
                               "comparison in this table is marked non-commensurable for that "
                               "reason, which leaves exactly one usable back-test.",
}

# Lomustine as sole agent, 105-day exposure cap, against the 0.375 observed.
LOMUSTINE_BACKTEST = {
    "observed_relapse_free": 0.375,
    "model_relapse_free_by_potency": {
        # max_kill_2 -> {horizon_days: relapse_free}
        0.00: {568: 0.000, 730: 0.000, 1825: 0.000},
        0.05: {568: 0.000, 730: 0.000, 1825: 0.000},
        0.08: {568: 0.000, 730: 0.000, 1825: 0.000},
        0.12: {568: 0.000, 730: 0.000, 1825: 0.000},
        0.20: {568: 0.000, 730: 0.000, 1825: 0.000},
    },
    "verdict": "FAILS. 0.000 at every potency and every horizon, against an observed 0.375.",
}

HYPOTHESES_TESTED_AND_REJECTED = {
    "extinction_threshold_missing": {
        "hypothesis": "The tumour never reaches a size where a one-cell extinction floor would "
                      "declare it cured, so adding that floor would fix the back-test.",
        "test": "Applied floors at 1000 cells, 1 cell (K=1e9) and 1 cell (K=1e12) to the lomustine "
                "arm's per-trial nadir.",
        "result": "REJECTED -- 0.000 cured at every threshold. The lomustine nadir is ~1.6e-5, far "
                  "above any of them.",
    },
    "fixed_surgical_residual": {
        "hypothesis": "Every simulated dog starts from the same post-surgical residual (0.009), so "
                      "a mixture outcome like 37.5%/62.5% is structurally unreachable.",
        "test": "Swept the residual across seven orders of magnitude, 9e-3 to 1e-10.",
        "result": "REJECTED -- relapse-free stayed 0.000 at every value, including 1e-10.",
    },
    "why_both_were_worth_testing": "Each is the plausible first guess, and reporting only the "
                                   "surviving explanation would make the diagnosis look more "
                                   "obvious than it was.",
}

THE_ACTUAL_MECHANISM = {
    "the_arithmetic": "Lomustine's course is capped at 105 days. Whatever nadir it reaches, the "
                      "drug stops and the tumour regrows at ~0.06/day for the remaining 463 days "
                      "of the window -- a factor of e^(0.06*463) ~ 1.2e12. Any nonzero residual "
                      "multiplied by 1.2e12 clears the 1% detection floor.",
    "and_the_residual_is_always_nonzero": "The engine has no extinction state. Across 200 five-year "
                                          "trials the minimum burden observed was 2.7e-82, and the "
                                          "model treats that as a live population that regrows.",
    "the_step_function": "Relapse-free is 0.000 up to max_kill 0.30 and 1.000 at 0.50, with nothing "
                         "between. The 1.000 is not a cure either: at 0.50 the nadir is ~1e-20, "
                         "which after 1.2e12-fold regrowth is ~1e-8 -- still under the detection "
                         "floor at day 568. 'Not yet detectable', not 'gone'.",
}

WHAT_THE_ENGINE_ACTUALLY_COMPUTES = {
    "when_the_output_is_a_real_probability": "Only when the binding event is stochastic SEEDING of "
        "a resistant clone. That is the continuous-drug-pressure regime, where trial-to-trial "
        "variation is real and the engine produces genuine intermediate values -- 0.530, 0.893, "
        "0.985 all came from there.",
    "when_it_is_not": "When the binding event is regrowth of residual SENSITIVE disease, which is "
        "what happens in any finite course -- i.e. every real adjuvant protocol. Regrowth is "
        "deterministic, there is no trial-to-trial variation, and the output collapses to a step "
        "function of potency and horizon.",
    "THE_CONSEQUENCE": "This project repeatedly concludes that duration-capped agents buy delay "
        "rather than durability, and quotes a 0.060/day drugs-off bar for the lung/no-antigen cell. "
        "That conclusion CANNOT COME OUT ANY OTHER WAY. An engine with no extinction state and "
        "deterministic regrowth of residual disease will always say a finite course fails, "
        "whatever the drug, dose or disease. It is a property of the tool, not a finding about "
        "histiocytic sarcoma -- and Skorupski's 37.5% is the direct counterexample: a real finite "
        "course, in this exact disease, after which more than a third of dogs did not relapse.",
}


def confidence_verdict() -> dict:
    """Do we have confidence in the modelling tools?"""
    return {
        "short_answer": "Qualified. The engine is sound in the regime its headline figures occupy "
                        "and structurally unable to model the regime it has been used to make "
                        "claims about.",
        "what_is_trustworthy": "Continuous-drug-pressure durability, where resistant-clone seeding "
                               "is the binding event. That regime produces genuine probabilities "
                               "and is where every 0.99/1.00 in the frozen findings sits. Nothing "
                               "here invalidates those.",
        "what_is_not": "Anything about finite courses, stoppability, or withdrawal of therapy. The "
                       "engine cannot represent a course that ends in cure, so it always concludes "
                       "one does not. Every such statement in the analysis is a tautology of the "
                       "tool.",
        "the_one_available_backtest_fails": LOMUSTINE_BACKTEST["verdict"],
        "and_most_comparisons_are_not_even_possible": "Six of the seven measured outcomes in this "
            "repo report median survival, which the engine does not emit. Only relapse-free "
            "fraction is commensurable, which leaves exactly one usable back-test out of seven.",
        "what_would_fix_it": "An extinction state -- burden below one cell becomes zero and stays "
                             "zero -- plus stochastic cell loss at low burden, so clearance becomes "
                             "a probability rather than an asymptote. Standard in stochastic tumour "
                             "models. It is an engine change, not an analysis change, and it is NOT "
                             "made here: this module diagnoses, it does not patch.",
        "the_honest_summary": "The project has been running an engine that can answer 'how long "
                              "until resistance emerges under continuous pressure' and cannot "
                              "answer 'can this dog be cured'. It has been asked both questions.",
    }


def commensurable_outcomes() -> dict:
    """The subset of the measured record that can legitimately be compared to engine output."""
    return {k: v for k, v in MEASURED_MONOTHERAPY_OUTCOMES.items() if v["COMMENSURABLE"]}


# ---------------------------------------------------------------------------------------------
# Follow-up: an extinction state was added to the engine and the back-test re-run.
# ---------------------------------------------------------------------------------------------

EXTINCTION_RERUN = {
    "what_was_changed": "`simulate_resistance` and `run_monte_carlo_two_compartment` gained an "
                        "opt-in `extinction_threshold`. Below it a clone goes to zero and stays "
                        "there. Default off, so no previously computed figure moved.",
    "result_within_the_swept_potency_range": "NO CHANGE. 0.000 at every potency in "
        "`CCNU_MAX_KILL_SWEEP` and at both cell anchors.",
    "why_it_could_not_bite": "Extinction only matters if the tumour actually reaches one cell. At "
        "max_kill 0.12 against growth 0.06 the nadir is 1.65e-5 -- about 16,500 surviving cells at "
        "a carrying capacity of 1e9 -- four orders of magnitude above the 1e-9 threshold. The "
        "potency needed to reach one cell is 0.213/day and the sweep tops out at 0.20. It was "
        "arithmetically impossible for the fix to show up inside the swept range.",
    "nadir_by_potency_cells_at_K_1e9": {0.12: 16527, 0.20: 4, 0.25: 0, 0.30: 0, 0.40: 0},
}

# Relapse-free at 568 d once potency is pushed past the point where extinction can act.
EXTINCTION_UNLOCKS_INTERMEDIATE_OUTCOMES = {
    # max_kill -> {anchor: relapse_free}
    0.20: {"off": 0.000, "one_cell_1e9": 0.000, "one_cell_1e12": 0.000},
    0.25: {"off": 0.000, "one_cell_1e9": 0.910, "one_cell_1e12": 0.000},
    0.28: {"off": 0.000, "one_cell_1e9": 0.997, "one_cell_1e12": 0.000},
    0.30: {"off": 0.000, "one_cell_1e9": 0.993, "one_cell_1e12": 0.420},
    "THE_FINDING": "With extinction OFF the column is 0.000 everywhere -- the engine cannot produce "
        "an intermediate relapse-free fraction in a finite-course setting at ANY potency, because "
        "regrowth of residual sensitive disease is deterministic. With extinction ON it can: 0.420 "
        "at max_kill 0.30 and the 1e12 anchor, against an observed 0.375. The step-function "
        "behaviour was a consequence of the missing extinction state, exactly as diagnosed.",
    "BUT_THIS_IS_NOT_A_VALIDATION": "Reaching 0.420 required a lomustine potency of 0.30/day -- 1.5x "
        "above the top of the drug's own swept range -- AND selecting the 1e12 carrying-capacity "
        "anchor over 1e9, which gives 0.993 at the same potency. Two free parameters moved to land "
        "near the target. That is fitting, not back-testing. What it demonstrates is CAPABILITY: "
        "the machinery can now produce the right kind of answer. Whether it produces the right "
        "answer at honest parameter values is still unestablished.",
    "the_upgrade_in_status": "Before: structurally incapable of matching the one known outcome, at "
        "any parameter value. After: capable, and matching it requires assumptions outside the "
        "project's own swept ranges. The first is a defect. The second is a calibration gap.",
}
