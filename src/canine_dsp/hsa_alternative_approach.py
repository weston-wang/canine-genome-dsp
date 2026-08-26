"""The second drug cannot be stopped. So does the plan need a different second drug?

`hsa_margin_analysis` closed the obvious escape hatch: withdrawing the MEK/mTOR pair at one, two or
three years drops ten-year durability *below* what the cross-resistance correction delivers on its
own. The clones are suppressed, not eliminated. That leaves a decade of continuous dual kinase
inhibition as a requirement rather than a preference, and makes cumulative toxicity the sharpest
objection to the whole plan.

This module asks the question that follows -- given the toxicity, is a different approach needed --
and answers it in three steps rather than by assertion:

  1. Can the same drug be given LESS? Three schedule families, run through the engine. All fail,
     and they fail in an informative direction.
  2. What criterion does the pair actually fail? Not potency -- it cleared the exposure criterion.
     It fails a second, weaker criterion nobody had written down: documented tolerability must
     cover the treatment horizon.
  3. If no drug clears both criteria, the persistent work has to move off the drug entirely. The
     model can say exactly how much it has to move.

See docs/HSA_DURABLE_RESPONSE.md.
"""
from __future__ import annotations

# =============================================================================================
# STEP 1. NO SCHEDULE RESCUES THE DRUG.
#
# Every alternative to continuous full-dose exposure was run through the same engine, same seed,
# same 250 trials, same waning-immunity schedule, at the corrected IC50 -- so the only variable is
# how the second drug is delivered. Continuous full dose is 0.888.
# =============================================================================================

# A. Duty cycling: full dose while on, nothing while off. Three periods x three on-fractions, so a
# period effect (if there were one) would separate from a cumulative-dose effect.
DUTY_CYCLING = {
    (14, 0.75): 0.760, (14, 0.50): 0.576, (14, 0.25): 0.488,
    (28, 0.75): 0.740, (28, 0.50): 0.576, (28, 0.25): 0.460,
    (56, 0.75): 0.740, (56, 0.50): 0.576, (56, 0.25): 0.460,
}

# B. Dose reduction: continuous, at a fraction of the tolerated dose.
DOSE_REDUCTION = {1.00: 0.888, 0.75: 0.784, 0.50: 0.668, 0.25: 0.468}

# C. De-escalation: full dose for a two-year lead-in, reduced thereafter. Keyed by the fraction
# given after year two; the value is (cumulative dose fraction, ten-year durability).
DE_ESCALATION = {0.50: (0.60, 0.696), 0.25: (0.40, 0.532), 0.00: (0.20, 0.460)}

CONTINUOUS_FULL_DOSE = 0.888

# The pattern across all three families is the finding, not any single row.
CONTINUOUS_BEATS_INTERMITTENT_AT_MATCHED_DOSE = {
    "at_75_percent": {"continuous": 0.784, "duty_cycled": (0.740, 0.760)},
    "at_50_percent": {"continuous": 0.668, "duty_cycled": (0.576, 0.576)},
    "at_25_percent": {"continuous": 0.468, "duty_cycled": (0.460, 0.488)},
    "the_rule": "where the schedules separate at all, giving less drug continuously beats giving "
                "full doses intermittently: 0.784 vs 0.740-0.760 at three-quarter dose, and 0.668 "
                "vs 0.576 at half dose.",
    "where_the_rule_stops_holding": "at quarter dose the two are indistinguishable -- 0.468 "
                                    "continuous against 0.460-0.488 pulsed, a spread inside "
                                    "Monte Carlo noise at 250 trials. That is not a counterexample "
                                    "so much as a floor: by quarter dose every arm has collapsed "
                                    "to roughly the 0.500 that the correction alone delivers, and "
                                    "there is nothing left for the schedule to differentiate.",
    "period_does_not_matter": "at a fixed on-fraction the three periods are within noise of each "
                              "other (0.740-0.760 at 75%, 0.576 three times at 50%). What matters "
                              "is the fraction of time the drug is absent, not how that absence is "
                              "chopped up.",
    "why_this_is_not_the_adaptive_therapy_result": "adaptive therapy works when a drug-sensitive "
                                                   "population, kept alive on purpose, competes "
                                                   "the resistant one down during the off "
                                                   "intervals. The engine has logistic growth, so "
                                                   "that competition is represented -- and it "
                                                   "still loses. In this tumour the resistant "
                                                   "clones regrow during the gaps faster than "
                                                   "competition suppresses them.",
    "the_design_consequence": "if cumulative exposure has to come down for tolerability, take it "
                              "out of the dose and not out of the calendar. That is the opposite "
                              "of the usual clinical instinct, which is drug holidays.",
}

SCHEDULE_VERDICT = {
    "finding": "no schedule preserves the decade at reduced cumulative dose. Durability tracks "
               "cumulative exposure roughly monotonically, and every schedule that gives less "
               "gives less protection.",
    "what_it_rules_out": "the comfortable answer -- keep the same regimen, just give it less "
                         "often. It does not survive contact with the model.",
    "what_it_leaves": "either the drug is given continuously for ten years, or the persistent "
                      "work moves off the drug.",
}


# =============================================================================================
# STEP 2. THE CRITERION THE PAIR ACTUALLY FAILS.
#
# The exposure criterion (hsa_parallel_pathway) asks whether achievable exposure clears the
# concentration the effect needs. Trametinib + sapanisertib passes it -- that is why it replaced
# propranolol. It fails a different and much simpler test, one that was never written down because
# nothing before it had a ten-year dosing requirement.
# =============================================================================================

TREATMENT_HORIZON_DAYS = 3650

# The tolerability record for the pair in dogs, from Wei et al. 2022 (PMID 36590793).
DOCUMENTED_TOLERABILITY_DAYS = 17


def duration_shortfall(documented_days: float, horizon_days: float = TREATMENT_HORIZON_DAYS
                       ) -> float:
    """How many times longer than the evidence the regimen would have to be given.

    Deliberately the same shape as the exposure criterion's fold-short: a ratio of what is
    required to what has been demonstrated, so the two failures are directly comparable.
    """
    if documented_days <= 0:
        raise ValueError("documented tolerability must be a positive number of days")
    if horizon_days <= 0:
        raise ValueError("the treatment horizon must be a positive number of days")
    return float(horizon_days) / float(documented_days)


def clears_duration_criterion(documented_days: float,
                              horizon_days: float = TREATMENT_HORIZON_DAYS) -> bool:
    """True when tolerability has been demonstrated over at least the horizon it will be used for."""
    return duration_shortfall(documented_days, horizon_days) <= 1.0


THE_DURATION_CRITERION = {
    "statement": "an agent intended for continuous administration over a horizon qualifies only if "
                 "its tolerability has been demonstrated over a comparable horizon.",
    "why_it_is_needed": "the exposure criterion screens on potency at an achievable concentration. "
                        "It is silent about time. Nothing earlier in this analysis needed a time "
                        "axis, because nothing earlier had established that the drug can never be "
                        "stopped.",
    "applied_to_the_pair": {
        "documented_days": DOCUMENTED_TOLERABILITY_DAYS,
        "required_days": TREATMENT_HORIZON_DAYS,
        "fold_short": duration_shortfall(DOCUMENTED_TOLERABILITY_DAYS),
        "and_in_healthy_dogs": "the 17 days were in healthy laboratory beagles, not in tumour-"
                               "bearing dogs carrying the acute-phase inflammation, proteinuria "
                               "and marrow suppression the study itself recorded.",
    },
    "the_symmetry_that_makes_this_hard_to_wave_away": "propranolol was rejected from this analysis "
                                                     "for being about 200x short on exposure. The "
                                                     "MEK/mTOR pair is about 200x short on "
                                                     "duration. Applying the first standard and "
                                                     "not the second would be special pleading.",
    "what_it_does_not_say": "not that the pair is unsafe over ten years. That it is unknown over "
                            "ten years, in a regimen whose whole claim is a ten-year outcome. The "
                            "recorded toxicities -- proteinuria, reduced reticulocytes, acute-"
                            "phase inflammation -- are renal and marrow signals, which are exactly "
                            "the organs where seventeen days of mild change carries no information "
                            "about a decade.",
}


# =============================================================================================
# WHY THE OBVIOUS DRUG SWAPS DO NOT WORK.
#
# The natural response is to keep the structure and substitute a better-tolerated agent into the
# chronic-suppression role. Three candidates have real chronic-dosing records in dogs. Each fails,
# and each fails for a different reason -- which is what makes the structural alternative
# necessary rather than merely convenient.
# =============================================================================================

WHY_THE_OBVIOUS_SWAPS_DO_NOT_WORK = {
    "metronomic_chemotherapy": {
        "the_appeal": "designed for chronic administration, decades of use in dogs, oral, cheap, "
                      "and antiangiogenic -- which is mechanistically apt for an endothelial "
                      "tumour.",
        "why_it_fails": "the canine hemangiosarcoma evidence is negative, not merely thin. In a "
                        "66-dog multicentre series, dogs with hepatic metastases given metronomic "
                        "therapy survived 65 days against 255 for anthracycline-based treatment "
                        "(P=0.02).",
        "citation": "Valenti et al. 2026, J Vet Intern Med 40(1), PMID 41742582",
        "corroboration": "the 2026 review of canine splenic hemangiosarcoma concludes that "
                         "metronomic chemotherapy, immunotherapy and targeted therapies 'have not "
                         "demonstrated consistent clinical benefit' (PMID 41828985).",
        "verdict": "clears the duration criterion, fails on effect in this disease.",
    },
    "a_rapalog_alone": {
        "the_appeal": "sirolimus has the best chronic-dosing record of any mTOR agent in dogs.",
        "why_it_fails": "canine hemangiosarcoma signals through mTORC2/Akt, and rapalogs inhibit "
                        "mTORC1. The measured cross-resistance (Rodrik-Outmezguine 2016) is "
                        "reciprocal rather than additive: rapalog resistance sits in FRB/FKBP12 "
                        "and ATP-competitive resistance in the kinase domain, so a rapalog does "
                        "not cover the escape the ATP-competitive agent covers.",
        "verdict": "clears the duration criterion, targets the wrong complex.",
    },
    "toceranib": {
        "the_appeal": "licensed for dogs, given continuously for years in practice, and the "
                      "chronic toxicity profile is better characterised than for any other kinase "
                      "inhibitor in the species.",
        "why_it_fails": "already screened earlier in this analysis. It clears the exposure "
                        "criterion and then fails on biology -- the target engagement is real and "
                        "the anti-tumour effect in hemangiosarcoma is not.",
        "verdict": "clears the duration criterion, fails the biology.",
    },
    "the_pattern": "every agent with a decade-scale canine safety record fails on effect in this "
                   "tumour, and the one agent with measured effect in canine angiosarcoma has "
                   "seventeen days of safety data. The two criteria are in tension and no single "
                   "available agent clears both.",
}


# =============================================================================================
# STEP 3. THE STRUCTURAL ALTERNATIVE.
#
# If no drug clears both criteria, the persistent work cannot sit on a drug. It has to sit on the
# component that is already given on a schedule tolerable for a decade -- the vaccine, boosted
# every sixty days. The model can put a number on how much taller that component has to be before
# the drug becomes stoppable.
#
# =============================================================================================

MEASURED_VACCINE_HEIGHT = 0.030   # per day, the height real canine vaccines deliver
THE_BAR = 0.0515                  # per day, what a lone persistent mechanism would have to exceed

# Ten-year durability on a grid of vaccine height x when the second drug is withdrawn. Same engine,
# same seed, same 250 trials, same corrected IC50 and waning-immunity schedule as everywhere else,
# so the only variables are the two being crossed. Keys are (vaccine_max_kill_per_day, stop_year),
# with a stop_year of None meaning the drug is never stopped.
VACCINE_HEIGHT_VS_DRUG_STOP = {
    (0.0300, 1): 0.464, (0.0300, 2): 0.460, (0.0300, 3): 0.488, (0.0300, 5): 0.576,
    (0.0300, None): 0.888,
    (0.0375, 1): 0.652, (0.0375, 2): 0.696, (0.0375, 3): 0.740, (0.0375, 5): 0.920,
    (0.0375, None): 1.000,
    (0.0450, 1): 0.992, (0.0450, 2): 1.000, (0.0450, 3): 1.000, (0.0450, 5): 1.000,
    (0.0450, None): 1.000,
    (0.0515, 1): 1.000, (0.0515, 2): 1.000, (0.0515, 3): 1.000, (0.0515, 5): 1.000,
    (0.0515, None): 1.000,
    (0.0600, 1): 1.000, (0.0600, 2): 1.000, (0.0600, 3): 1.000, (0.0600, 5): 1.000,
    (0.0600, None): 1.000,
}


def drug_days(stop_year: int | None, horizon_days: int = TREATMENT_HORIZON_DAYS) -> int:
    """Days of second-drug exposure for a given withdrawal time. None means never withdrawn."""
    if stop_year is None:
        return int(horizon_days)
    if stop_year <= 0:
        raise ValueError("stop_year must be positive, or None for continuous dosing")
    return min(int(stop_year * 365), int(horizon_days))


def exposure_fraction(stop_year: int | None, horizon_days: int = TREATMENT_HORIZON_DAYS) -> float:
    """Fraction of the treatment horizon spent on the second drug."""
    return drug_days(stop_year, horizon_days) / float(horizon_days)


# The exchange rate, which is the whole point of the grid: what a taller vaccine buys in drug-days.
THE_EXCHANGE_RATE = {
    "at_the_measured_height": {
        "height": 0.0300, "height_multiple": 1.0,
        "best_stoppable_option": "none -- every withdrawal time lands at or below 0.576, and the "
                                 "one-, two- and three-year stops land below the 0.500 that the "
                                 "cross-resistance correction delivers on its own",
        "durability_if_never_stopped": 0.888,
        "drug_days_required": 3650,
    },
    "at_1_25x": {
        "height": 0.0375, "height_multiple": 1.25,
        "durability_stopping_at_year_2": 0.696,
        "durability_stopping_at_year_5": 0.920,
        "durability_if_never_stopped": 1.000,
        "reading": "a quarter taller is not enough to stop early. It is enough to make late "
                   "withdrawal survivable and to make continuous dosing essentially certain.",
    },
    "at_1_5x": {
        "height": 0.0450, "height_multiple": 1.5,
        "durability_stopping_at_year_1": 0.992,
        "durability_stopping_at_year_2": 1.000,
        "drug_days_required": 365,
        "reading": "half again as tall and the second drug becomes a one-year induction rather "
                   "than a life sentence.",
    },
    "the_trade": "raising vaccine height by 1.5x cuts second-drug exposure from 3650 drug-days to "
                 "365 -- a 90% reduction in the exposure driving the cumulative toxicity -- while "
                 "RAISING ten-year durability from 0.888 to 0.992. It is not a trade at all. Both "
                 "axes improve.",
    "the_threshold_is_below_the_bar": "0.045/day is less than the 0.0515/day bar. The vaccine does "
                                      "not have to be able to hold the tumour alone. It only has "
                                      "to be tall enough that one year of drug plus a taller "
                                      "vaccine finishes what a decade of drug plus the measured "
                                      "vaccine could not.",
    "why_the_curve_is_so_steep": "between 0.0375 and 0.045 the year-one stop moves 0.652 -> 0.992. "
                                 "That is a threshold, not a slope, and it sits inside the range a "
                                 "1.25-1.5x improvement covers. The practical consequence is that "
                                 "a modest gain in vaccine potency is worth far more than any "
                                 "further work on the drug schedule.",
}

# An honest note on the mechanism behind the 1.000s, because a perfect number invites suspicion.
WHY_A_TALLER_VACCINE_ALSO_SUPPRESSES_THE_ESCAPE_CLONE = {
    "the_apparent_problem": "the vaccine does not act on the antigen-loss clone at all -- it is "
                            "excluded by construction (the applicability vector is [1,1,1,1,0]). "
                            "So durability reaching 1.000 looks like the escape route has been "
                            "quietly dropped.",
    "the_actual_mechanism": "it has not. Escape-clone seeding is proportional to the "
                            "ANTIGEN-POSITIVE burden, because that is the population the "
                            "antigen-loss variant arises from. A taller vaccine crushes that "
                            "population faster, so there is less of it to throw off an escape "
                            "variant. The suppression is indirect and it is real.",
    "why_this_is_not_a_modelling_convenience": "the same structure is what made the escape route "
                                               "look unclosable at the measured height: a vaccine "
                                               "that only holds the antigen-positive population "
                                               "flat leaves it seeding escape variants for a "
                                               "decade. Height changes the seeding integral, not "
                                               "just the kill.",
    "the_limit_of_the_claim": "1.000 over 250 trials means no trial progressed, not that "
                              "progression is impossible. It bounds the escape probability below "
                              "roughly 1% at this sample size and says nothing finer.",
}


# ---------------------------------------------------------------------------------------------
# The disease-specific reason a taller vaccine is a real target rather than a wish. Canine
# hemangiosarcoma does not merely fail to attract T cells -- it actively excludes them, through a
# named and druggable axis.
HSA_ACTIVELY_SUPPRESSES_THE_ARM_THE_VACCINE_USES = {
    "citation": "Gulay et al. 2022, Sci Rep 12(1):2124, PMID 35136176, "
                "doi 10.1038/s41598-022-06203-w",
    "what_is_in_the_tumour": "macrophages are a major constituent of the canine hemangiosarcoma "
                             "microenvironment, and they are CD204+ (M2-polarised) and PD-L1+",
    "the_functional_consequence": "'Canine HSA with macrophages expressing PD-L1 had a smaller "
                                  "number of T-cells in tumour tissues than tumours with PD-L1 "
                                  "negative macrophages.' The suppression is measured inside the "
                                  "tumour, not inferred from another disease.",
    "the_tumour_drives_it": "conditioned medium from a hemangiosarcoma line induced M2 "
                            "polarisation and PD-L1 expression in naive macrophages -- the tumour "
                            "creates the suppression rather than arriving in a suppressed site",
    "why_this_matters_for_vaccine_height": "the vaccine's ceiling in this analysis was treated as "
                                           "a fixed property of the product. This says a "
                                           "substantial part of it is a property of the "
                                           "microenvironment, which is a different kind of "
                                           "problem -- one with an existing intervention.",
    "a_testbed_that_did_not_exist_before": "the same paper qualifies ISOS-1 as a syngeneic mouse "
                                           "model matching canine HSA morphology and KDM2B target "
                                           "expression. Every immune question in this analysis was "
                                           "previously stuck with xenografts, which have no host "
                                           "immune system to suppress.",
}

# ---------------------------------------------------------------------------------------------
# And the intervention exists, in dogs, on a schedule in the same tolerability class as a booster.
A_CANINE_CHECKPOINT_ANTIBODY_IS_AVAILABLE = {
    "citation": "Chon et al. 2026, J Vet Intern Med 40(3), PMID 42247661, doi 10.1093/jvimsj/aalag098",
    "agent": "gilvetmab, a caninized anti-PD-1 monoclonal antibody",
    "design": "multi-institutional open-label study, 51 client-owned dogs (25 melanoma stages "
              "II-III, 26 mast cell tumour stages I-III), plus 15 with lymphoma",
    "dosing": "6 mg/kg IV q28d or 10 mg/kg IV q14d",
    "efficacy": {"melanoma_orr": 0.20, "melanoma_orr_ci": (0.07, 0.41), "melanoma_median_ttp_days": 56,
                 "mct_orr": 0.46, "mct_orr_ci": (0.27, 0.67), "mct_median_ttp": "not reached",
                 "lymphoma_orr": 0.0},
    "safety": "serious adverse events in 3 of 51 dogs (5.9%): anaphylaxis, hypotension, or tumour "
              "haemorrhage",
    "why_the_schedule_matters_here": "a q14-28d intravenous antibody is in the same administration "
                                     "and tolerability class as the q60d vaccine booster, and a "
                                     "different class from daily dual kinase inhibition. Moving "
                                     "persistent work onto it does not reintroduce the problem "
                                     "this module exists to solve.",
    "the_earlier_canine_precedent": "Igase et al. 2020, Sci Rep 10(1):18311, PMID 33110170 -- a "
                                    "caninized anti-canine PD-1 antibody, safe and with responses "
                                    "in advanced canine cancers. Oh et al. 2023 (PMID 37377896) "
                                    "adds an anti-canine PD-L1 antibody with an initial safety "
                                    "profile in laboratory dogs.",
}

# The specific risk this carries in THIS tumour, which is not the generic checkpoint-toxicity risk.
THE_HAEMORRHAGE_SIGNAL = {
    "the_observation": "one of the three serious adverse events in the gilvetmab study was tumour "
                       "haemorrhage.",
    "why_it_is_not_generic_here": "splenic rupture and haemoperitoneum are the competing hazard "
                                  "that dominates early mortality in this disease, and the tumour "
                                  "is made of endothelium. A therapy whose recorded serious "
                                  "toxicity includes tumour haemorrhage is being proposed for the "
                                  "one tumour where haemorrhage is already the leading cause of "
                                  "death.",
    "what_this_does_to_the_trade": "it does not cancel the swap. It changes what the swap is "
                                   "trading: a decade of cumulative renal and marrow toxicity "
                                   "against an acute bleeding risk concentrated in the "
                                   "peri-treatment window. Those are different hazards with "
                                   "different shapes and the second one is at least measurable "
                                   "early.",
    "the_mitigating_detail": "the checkpoint component is proposed post-splenectomy, once the "
                             "primary bleeding tumour has been removed. The published event was in "
                             "dogs with tumours in place.",
    "status": "OPEN -- this is a real, disease-specific risk with no data in hemangiosarcoma, and "
              "it should be stated as such rather than reasoned away.",
}

# ---------------------------------------------------------------------------------------------
# A third timing constraint, on top of the two in `hsa_immune_timing`.
CORTICOSTEROIDS_ARE_A_THIRD_TIMING_CONSTRAINT = {
    "citation": "Zimmermann et al. 2025, Front Immunol 16:1544949, PMID 40342421, "
                "doi 10.3389/fimmu.2025.1544949",
    "design": "PBMCs from 24 healthy, 44 cancer-bearing untreated and 33 cancer-bearing "
              "corticosteroid-pretreated dogs, stimulated with SEB plus either atezolizumab "
              "(anti-PD-L1) or rhIL-12; gilvetmab gave comparable results to atezolizumab",
    "result": "corticosteroid treatment significantly affected immune profile -- primarily the "
              "monocytic compartment -- and the functional interferon-gamma response",
    "authors_conclusion": "'prior corticosteroid therapy may compromise the efficacy of PD-1/PD-L1 "
                          "axis blockade and IL-12 in dogs with cancer', while noting responses "
                          "were highly individual and that this would not justify withholding the "
                          "therapy",
    "why_it_lands_on_this_disease": "corticosteroids are routinely given around splenectomy and "
                                    "haemoabdomen. The suppressed compartment is the monocytic "
                                    "one, and the Gulay finding says the monocyte/macrophage "
                                    "compartment is exactly where hemangiosarcoma's PD-L1 "
                                    "suppression lives.",
    "the_third_of_a_set": "surgery and chemotherapy suppress effector function (Rebhun 2025); "
                          "dosing an immune agent inside that window went backwards twice (Rebhun "
                          "2025, Borgatti 2020); and now corticosteroids blunt the specific axis "
                          "this swap depends on. All three point the same way: the immune "
                          "components belong after the surgical and chemotherapy backbone, gated "
                          "on recovered effector function, not inside it.",
}


# =============================================================================================
# THE REVISED REGIMEN, AND WHAT IT COSTS.
# =============================================================================================

REVISED_REGIMEN = {
    "unchanged": [
        "splenectomy, then the doxorubicin backbone",
        "the PI3K/mTOR inhibitor as the first drug, continuously",
        "the vaccine with q60d boosters -- boosters buy persistence, which is still mandatory",
        "an NK component for the antigen-loss clone, scheduled outside the peri-operative window",
    ],
    "changed": [
        "the MEK inhibitor becomes a ONE-YEAR INDUCTION rather than indefinite therapy",
        "checkpoint blockade (anti-PD-1) is added to raise the vaccine's height, on a q14-28d "
        "schedule, started after the chemotherapy backbone and gated on recovered PBMC "
        "cytotoxicity",
        "corticosteroids are minimised before and during the checkpoint component",
    ],
    "the_requirement_this_creates": "the vaccine-plus-checkpoint combination must deliver "
                                    "0.045/day of effective kill against the antigen-positive "
                                    "population -- 1.5x what vaccines alone have measured. That is "
                                    "the single number the revised plan stands or falls on.",
    "what_makes_that_requirement_testable": "it is a potency measurement in a syngeneic model that "
                                            "now exists (ISOS-1), against an axis measured to be "
                                            "active in this tumour (PD-L1+ M2 macrophages "
                                            "excluding T cells), using an antibody that is already "
                                            "dosed in dogs. Every component of the experiment is "
                                            "available.",
}

WHAT_THE_ALTERNATIVE_COSTS = {
    "removed": "roughly 3285 of 3650 drug-days of dual kinase inhibition, and with them the "
               "cumulative renal and marrow toxicity that had no supporting data beyond 17 days",
    "added": "a checkpoint antibody with a 5.9% serious-adverse-event rate in dogs, one instance "
             "of which was tumour haemorrhage in a disease where haemorrhage is the leading cause "
             "of death",
    "added_uncertainty": "no measurement of what checkpoint blockade adds to vaccine height in any "
                         "species for this tumour. The 1.5x is a requirement derived from the "
                         "model, not an effect size taken from data.",
    "the_honest_comparison": "the previous plan needed an unmeasured decade of safety. This one "
                             "needs an unmeasured 1.5x of potency. The second is the better bet "
                             "because it can be measured in months, in a model that exists, before "
                             "any dog is committed to it -- and because failing to reach it "
                             "degrades to the previous plan rather than to nothing.",
}

VERDICT = {
    "the_question": "given the toxicity, do you need to find an alternative approach?",
    "the_answer": "yes -- but not an alternative drug. An alternative place to put the persistent "
                  "work.",
    "step_1": "no schedule rescues the drug. Duty cycling, dose reduction and de-escalation all "
              "lose durability roughly in proportion to the exposure they give up, and continuous "
              "low dose beats pulsed full dose at every matched cumulative dose.",
    "step_2": "the pair fails a criterion that was never written down: 17 days of documented "
              "tolerability against a 3650-day requirement, a 215x shortfall of the same "
              "magnitude and the same form as the exposure shortfall that disqualified "
              "propranolol.",
    "step_3": "no available agent clears both the exposure and duration criteria -- everything "
              "with a decade-scale canine safety record fails on effect in this tumour. So the "
              "persistent work moves onto the vaccine, which is already given on a decade-"
              "tolerable schedule.",
    "the_quantified_target": "1.5x vaccine height (0.030 -> 0.045/day) converts the second drug "
                             "from indefinite therapy into a one-year induction, cutting drug "
                             "exposure by 90% while raising ten-year durability from 0.888 to "
                             "0.992.",
    "what_is_genuinely_new_here": "the toxicity objection was previously answered by arguing about "
                                  "the drug. This says the drug was never the right place to "
                                  "argue. The binding constraint is vaccine potency, and that is a "
                                  "constraint with an existing mechanism (PD-L1+ macrophages), an "
                                  "existing intervention (a caninized anti-PD-1 in 51 dogs), and "
                                  "an existing testbed (ISOS-1).",
    "what_remains_open": "the 1.5x is unmeasured; checkpoint blockade in a bleeding endothelial "
                         "tumour carries a haemorrhage signal with no hemangiosarcoma data; and "
                         "three independent findings now constrain the immune components to a "
                         "window after surgery, after chemotherapy, and away from "
                         "corticosteroids.",
}
