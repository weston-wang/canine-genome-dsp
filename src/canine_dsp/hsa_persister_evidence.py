"""The measured effect size behind the persister-directed kill, and the schedule it actually needs.

`hsa_orthogonal_kill` proposed exploiting the GPX4 dependency that drug-tolerant persister cells
acquire, found it rescues route 8's overlap case at about 0.045/day, and then said plainly that
there was "no anchor at all for the rate a ferroptosis inducer achieves against persisters in vivo".
That was the honest position at the time. It was also the position that made the route "closable
rather than closed", which is not the same thing as closed.

This module goes and gets the anchor. It does three things the earlier module did not:

  1. It restates the requirement in the units the persister experiments actually report. The
     requirement is a per-day rate; Hangauer's assays are three-day viability readouts. Converting
     between them is one line of arithmetic, and it changes the impression of the ask completely.

  2. It records that the disease-specific and species-specific test HAS been run. Three canine
     hemangiosarcoma lines sit inside the canine ferroptosis panel. That was missed the first time
     because the tumour type appears only in a supplementary table.

  3. It applies the duration criterion to the ferroptosis agent itself -- the criterion that
     disqualified the MEK/mTOR pair -- and tests whether the schedule the literature indicates is
     the ten-year one the earlier model assumed. It is not.

What it does NOT do is claim the route is finished. The section that matters most here is
`WHAT_IS_STILL_NOT_CLOSED`, and it is longer than the section that says what closed.

See docs/HSA_DURABLE_RESPONSE.md.
"""
from __future__ import annotations

import math

from .hsa_route_effect_sizes import rate_from_burden_reduction

# The rate `hsa_orthogonal_kill.RESCUE_BY_PERSISTER_KILL` located the threshold at: 0.035/day gives
# 0.000, 0.040/day gives 0.107, 0.050/day gives 1.000. The conservative reading is 0.045/day.
REQUIRED_PERSISTER_RATE_PER_DAY = 0.045

# The threshold's optimistic end, where durability first becomes non-zero.
FIRST_NONZERO_PERSISTER_RATE_PER_DAY = 0.040

# Hangauer read viability by CellTiter-Glo "after three days of small-molecule treatment".
PERSISTER_ASSAY_DAYS = 3.0


def viability_after(rate_per_day: float, days: float = PERSISTER_ASSAY_DAYS) -> float:
    """Fraction surviving after `days` of a sustained net kill of `rate_per_day`.

    The inverse of `rate_from_burden_reduction`. Present so the requirement can be quoted in the
    units a bench assay reports rather than only in the units the model consumes.
    """
    if rate_per_day < 0:
        raise ValueError("rate_per_day must be non-negative")
    if days <= 0:
        raise ValueError("days must be positive")
    return float(math.exp(-rate_per_day * days))


def transfer_required_from_viability(viability: float, days: float = PERSISTER_ASSAY_DAYS,
                                     required: float = REQUIRED_PERSISTER_RATE_PER_DAY) -> float:
    """Fraction of a measured in vitro kill that must survive transfer to clear the requirement.

    Same discipline as `hsa_route_effect_sizes.transfer_required`: convert the measured effect to a
    per-day rate, then divide the requirement by it. A value above 1.0 means the measured effect is
    not large enough even if all of it transferred.
    """
    return float(required / rate_from_burden_reduction(viability, days))


# =============================================================================================
# 1. THE REQUIREMENT, RESTATED IN THE UNITS THE EXPERIMENTS REPORT.
#
# This is the single most useful thing in this module, and it is arithmetic rather than a
# discovery. `hsa_orthogonal_kill` framed 0.045/day as "about seven eighths of the bar" and
# "roughly twice what the MEK inhibitor is asked for", which reads as a large ask. Both statements
# are true. But a sustained 0.045/day is, over the three days a persister viability assay runs,
# a 12.6% kill. Bench assays of this mechanism do not report 12.6%. They report near-elimination.
# =============================================================================================

THE_REQUIREMENT_IN_ASSAY_UNITS = {
    "required_per_day": REQUIRED_PERSISTER_RATE_PER_DAY,
    "three_day_viability_that_corresponds_to": viability_after(REQUIRED_PERSISTER_RATE_PER_DAY),
    "as_a_three_day_kill": 1.0 - viability_after(REQUIRED_PERSISTER_RATE_PER_DAY),
    "at_the_optimistic_end_of_the_threshold": {
        "required_per_day": FIRST_NONZERO_PERSISTER_RATE_PER_DAY,
        "as_a_three_day_kill": 1.0 - viability_after(FIRST_NONZERO_PERSISTER_RATE_PER_DAY),
    },
    "the_reading": "the model is asking for a 12.6% kill of the tolerant compartment over three "
                   "days -- SUSTAINED. It is not asking for a deep kill. It is asking for a shallow "
                   "one that never stops.",
    "why_the_earlier_framing_misled": "'seven eighths of the bar' compares the rate to the rate of "
                                      "the entire regimen, which makes it sound like the agent must "
                                      "do almost everything the regimen does. In per-day terms that "
                                      "is arithmetically right. In bench terms it is a weak effect, "
                                      "and the earlier module never converted it, so it never "
                                      "noticed. The conversion is the correction.",
    "what_this_does_not_do": "it does not lower the requirement. 0.045/day is still 0.045/day, and "
                             "the step function around it is still a step. What changes is which "
                             "experiments count as evidence for or against it, and how demanding "
                             "they look.",
    "where_the_difficulty_moves_to": "if the potency ask is small and the duration ask is ten years, "
                                     "then the binding constraint is duration, not potency. That is "
                                     "exactly the failure mode the duration criterion was invented "
                                     "for, and it is tested below rather than assumed away.",
}

# =============================================================================================
# 2. THE MEASURED EFFECT, AND WHY THIS ONE IS NOT THE COMPARISON THAT WAS RETRACTED.
# =============================================================================================

HANGAUER_ASSAY_PROTOCOL = {
    "citation": "Hangauer et al. 2017, Nature 551(7679):247-250, PMID 29088702, "
                "doi 10.1038/nature24297",
    "readout": "'Cell viability was assessed using CellTiter Glo (Promega) after THREE DAYS of "
               "small-molecule treatment'",
    "concentration": "1 uM RSL3",
    "persister_derivation": "two weeks of 2 uM lapatinib (BT474); persisters were also derived from "
                            "A375 melanoma/vemurafenib, PC9 lung/erlotinib and Kuramochi "
                            "ovarian/carboplatin-paclitaxel",
    "the_selectivity_statement": "GPX4 inhibitors RSL3 and ML210 were 'among the compounds most "
                                 "SELECTIVELY LETHAL to persister cells, with minimal effect on "
                                 "parental cells or nontransformed MCF10A cells'",
    "the_specificity_control": "'GPX4 inhibitors are NOT synergistic with lapatinib treatment of "
                               "parental BT474 cells, demonstrating that GPX4 dependence is specific "
                               "to the persister cell state'",
    "why_the_protocol_matters_here": "three days is the same three days the requirement converts to. "
                                     "The model's ask and the published readout are in the same "
                                     "units without any rescaling, which is rare in this analysis.",
    "the_number_that_is_missing": "the paper's per-line viability values are in figures rather than "
                                  "in text, and were not retrievable. So this module does NOT assert "
                                  "a specific measured viability. It computes the transfer required "
                                  "ACROSS a range of assumed potencies instead, and the reader can "
                                  "see which assumptions the conclusion survives.",
}

THE_IN_VIVO_RESULT_AT_THE_MODELS_OWN_ENDPOINT = {
    "the_experiment": "A375 melanoma xenografts, GPX4 knockout versus wild type, were shrunk with "
                      "dabrafenib plus trametinib while ferrostatin-1 masked any effect of GPX4 "
                      "deletion during the initial response. 'Once tumours had been reduced to their "
                      "minimal volume, ferrostatin-1 was withdrawn, unmasking the GPX4 KO effect in "
                      "these RESIDUAL tumours.'",
    "the_result": "'Upon further dosing of mice with dabrafenib and trametinib, without "
                  "ferrostatin-1, the GPX4 WT tumours RELAPSED and the GPX4 KO tumours DID NOT.'",
    "the_control": "'parental A375 GPX4 KO and WT cells both formed tumours without ferrostatin-1 "
                   "equally well' -- so the effect is on the residual population specifically, not a "
                   "general growth defect of the knockout.",
    "why_this_is_the_right_endpoint": "relapse-versus-no-relapse under continued targeted therapy is "
                                      "precisely what the Monte Carlo measures. Almost every other "
                                      "anchor in this analysis had to be converted from response "
                                      "rate or median survival. This one does not.",
    "why_this_is_not_the_category_error_that_was_retracted": "`hsa_orthogonal_kill` withdrew a "
                                                             "comparison that cited Andersen's "
                                                             "0.110-0.143/day as evidence a 0.045/day "
                                                             "ask was reachable. That was wrong "
                                                             "because Andersen measured drug-SENSITIVE "
                                                             "bulk tumour, killed by the very drugs "
                                                             "the resistant cell resists. This "
                                                             "experiment is the opposite: the "
                                                             "measurement is made on the RESIDUAL "
                                                             "population that survived the targeted "
                                                             "therapy, while that therapy continues. "
                                                             "It is the resistant compartment, "
                                                             "measured as the resistant compartment.",
    "the_limitation_that_must_be_stated_first": "the in vivo arm is a GENETIC knockout, not a drug. "
                                                "Hangauer says why in terms: 'Because neither RSL3 "
                                                "nor ML210 are systemically bioavailable, we instead "
                                                "adopted a recently developed genetic strategy.' This "
                                                "result proves the TARGET is right in vivo. It does "
                                                "not prove any molecule can hit it in vivo.",
    "the_second_limitation": "knockout is complete and permanent target removal. A drug gives partial "
                             "and intermittent inhibition. The knockout result is therefore an upper "
                             "bound on what pharmacology could achieve, not an estimate of it.",
}

# =============================================================================================
# 3. THE GAP HANGAUER NAMED, AND WHAT HAS AND HAS NOT CLOSED SINCE.
# =============================================================================================

THE_BIOAVAILABILITY_GAP_AS_ORIGINALLY_STATED = {
    "the_authors_own_words": "'While existing GPX4 inhibitors, including RSL3 and ML210, are valuable "
                             "tool compounds in cell culture settings, their poor pharmacokinetic "
                             "properties preclude their systemic use in vivo... the development of a "
                             "potent bioavailable GPX4 inhibitor is an URGENT PRIORITY.'",
    "the_safety_question_they_also_raised": "'Because GPX4 genetic deletion is LETHAL IN ADULT MICE, "
                                            "further study will be needed to determine whether a "
                                            "suitable therapeutic window exists for treatment with "
                                            "GPX4 inhibitors.'",
    "why_both_are_recorded": "the first is a medicinal-chemistry problem and the second is a "
                             "toxicology problem. They are independent, and closing the first does "
                             "not touch the second. An earlier draft of this work would have quoted "
                             "the first and quietly dropped the second.",
    "the_year": 2017,
}

WHAT_HAS_CLOSED_ON_THE_GPX4_ARM = {
    "citation": "Liu et al. 2023, Redox Biology 63:102677, PMID 36989572, "
                "doi 10.1016/j.redox.2023.102677",
    "the_agent": "Tubastatin A, an HDAC6 inhibitor identified by large-scale screening",
    "the_finding": "'Tubastatin A DIRECTLY BONDED to GPX4 and inhibited GPX4 enzymatic activity... "
                   "which is INDEPENDENT of its inhibition of HDAC6'",
    "the_bioavailability_claim": "'Tubastatin A has EXCELLENT BIOAVAILABILITY, as demonstrated by its "
                                 "ability to significantly promote radiotherapy-induced lipid "
                                 "peroxidation and tumour suppression in a mouse xenograft model'",
    "why_it_matters_here": "this is a direct answer to the compound Hangauer said did not exist: a "
                           "systemically dosable small molecule that binds GPX4 and inhibits it, with "
                           "in vivo activity. The urgent priority named in 2017 is no longer entirely "
                           "unmet.",
    "THE_FIELD_DOES_NOT_AGREE_THAT_THIS_IS_SETTLED": "the sentence above is the optimistic reading "
                                                     "and it is contradicted by a 2026 Nature paper "
                                                     "on the parallel arm, which states as background "
                                                     "'the HIGH TOXICITY, POOR SELECTIVITY and "
                                                     "LOW-TO-LIMITED BIOAVAILABILITY of GPX4 "
                                                     "inhibitors in vivo'. That is three years after "
                                                     "Tubastatin A and it does not treat the problem "
                                                     "as solved. Both statements are recorded because "
                                                     "picking the convenient one is how an analysis "
                                                     "talks itself into a conclusion. The weight of "
                                                     "the field is on the pessimistic side, and this "
                                                     "module takes the pessimistic side as the "
                                                     "operating assumption for the GPX4 arm.",
    "the_tension_with_this_analysis": "HDAC inhibition was tried in canine hemangiosarcoma and "
                                      "failed -- see `hsa_orthogonal_kill."
                                      "HDAC_INHIBITION_WAS_TRIED_IN_CANINE_HSA_AND_FAILED`. That "
                                      "failure is not automatically inherited here, because the GPX4 "
                                      "binding is explicitly stated to be independent of HDAC6 "
                                      "inhibition and the failed trial used a different agent on a "
                                      "different rationale. But it is not automatically escaped "
                                      "either, and this module does not pretend otherwise.",
    "what_could_not_be_verified": "the dose, schedule, and magnitude of tumour suppression are behind "
                                  "a publisher paywall that returned HTTP 403. Only the abstract's "
                                  "claims are recorded above. No effect size from this paper is used "
                                  "in any calculation in this module.",
    "the_honest_weight": "existence evidence, not effect-size evidence. It moves 'no bioavailable "
                         "GPX4 inhibitor exists' to 'one has been reported'. It does not supply a "
                         "number.",
}

WHAT_HAS_CLOSED_ON_THE_PARALLEL_ARM = {
    "citation": "Nature 2026, 'Targeting FSP1 triggers ferroptosis in lung cancer', PMID 41193800, "
                "doi 10.1038/s41586-025-09710-8",
    "the_biology": "GPX4 and FSP1 are the two arms of the same lipid-peroxidation defence. Tumour-"
                   "specific loss of EITHER 'increased lipid peroxidation and robust suppression of "
                   "tumorigenesis'.",
    "the_finding_that_changes_the_picture": "'FSP1 was required for ferroptosis protection IN VIVO, "
                                            "BUT NOT IN VITRO, underscoring a heightened need to "
                                            "buffer lipid peroxidation under physiological "
                                            "conditions.'",
    "why_that_matters": "it says in vitro assays UNDERSTATE how much a tumour depends on this defence "
                        "in a living animal. Every transfer estimate in this module is computed from "
                        "in vitro potency, so this cuts in the conservative direction.",
    "the_drug": "icFSP1, 'the first inhibitor of human FSP1 with IN VIVO STABILITY AND EFFICACY'",
    "the_dosing_that_was_actually_used": "'mice were dosed with 50 mg kg-1 icFSP1 or vehicle (45% "
                                         "PEG300 in sterile PBS) by INTRAPERITONEAL injection TWICE "
                                         "DAILY'",
    "the_result": "'FSP1 inhibition as a monotherapy improved overall survival of mice bearing lung "
                  "tumours, almost to the same extent as genetic Fsp1 deletion', and 'icFSP1 "
                  "treatment significantly decreased PDX tumour growth'",
    "the_on_target_control": "icFSP1 extended survival in tumours expressing wild-type human FSP1 but "
                             "NOT in tumours expressing the icFSP1-resistant FSP1(Q319K) mutant -- so "
                             "the benefit is inhibitor activity on the tumour cells, not an off-target "
                             "or microenvironmental effect.",
    "the_rescue_control": "liproxstatin-1 co-treatment abrogated the tumour suppression, confirming "
                          "the mechanism is lipid peroxidation.",
    "the_caveat_the_authors_state": "most FSP1 inhibitors 'are effective only in vitro against human "
                                    "FSP1 in the context of GPX4 loss or inhibition', and icFSP1's "
                                    "prior in vivo efficacy was 'solely in tumours with concomitant "
                                    "GPX4 loss'. This paper's contribution is showing monotherapy "
                                    "benefit where the tumour is already ferroptosis-primed.",
    "the_inference_that_is_tempting_and_is_not_made_here": "a persister is a cell in a state of "
                                                           "heightened GPX4 dependence, so it is "
                                                           "tempting to say it is exactly the "
                                                           "'GPX4-compromised' context where FSP1 "
                                                           "inhibitors work. That is a plausible "
                                                           "chain and it is UNTESTED. No experiment "
                                                           "in either paper puts an FSP1 inhibitor on "
                                                           "a drug-tolerant persister. It is written "
                                                           "down as a hypothesis, not counted as "
                                                           "evidence.",
    "the_delivery_problem_it_does_not_solve": "twice-daily intraperitoneal injection is a mouse "
                                              "route. It is not a ten-year canine route. This clears "
                                              "the exposure criterion in a rodent and says nothing "
                                              "about the duration criterion in a dog.",
    "THE_THERAPEUTIC_WINDOW_ARGUMENT_THAT_ANSWERS_HANGAUERS_SECOND_PROBLEM": {
        "the_statement": "'Given that germline Gpx4 KO mice are NOT VIABLE, whereas Fsp1 KO mice are "
                         "VIABLE WITH NO NOTABLE PHYSIOLOGICAL DEFECTS, the therapeutic window for "
                         "targeting FSP1 with fewer toxic side effects is expected to be MUCH GREATER "
                         "than for GPX4.'",
        "why_this_is_the_important_sentence_in_this_module": "Hangauer named two blockers in 2017: no "
                                                             "bioavailable inhibitor, and no known "
                                                             "therapeutic window because GPX4 "
                                                             "deletion is lethal in adult mice. The "
                                                             "second is the one the duration "
                                                             "criterion cares about, because an agent "
                                                             "with no therapeutic window cannot be "
                                                             "given for ten years at any dose. On the "
                                                             "FSP1 arm that blocker is absent by "
                                                             "genetics rather than by hope.",
        "what_it_does_and_does_not_establish": "it establishes that removing FSP1 is survivable in a "
                                               "healthy animal, which is the precondition for chronic "
                                               "dosing. It does NOT establish chronic tolerability of "
                                               "icFSP1 specifically, in any species, at any duration. "
                                               "The longest icFSP1 exposure reported is two weeks.",
        "the_documented_tolerability_days": 14,
        "the_horizon_days": 3650,
        "the_shortfall_multiple": 3650 / 14,
        "how_that_compares_to_the_disqualified_pair": "the MEK/mTOR pair was disqualified at a 215x "
                                                      "duration shortfall. icFSP1's is 261x. On the "
                                                      "criterion as written, this agent is in worse "
                                                      "shape than the one the analysis rejected, and "
                                                      "saying so is the price of having the "
                                                      "criterion. What differs is the direction of "
                                                      "travel: the MEK/mTOR shortfall was against a "
                                                      "DOSE-LIMITING TOXICITY that had already "
                                                      "appeared, while this one is simply an agent "
                                                      "nobody has yet dosed for longer.",
    },
}

# =============================================================================================
# 4. THE DISEASE-SPECIFIC ANCHOR THAT WAS THERE ALL ALONG.
#
# `hsa_orthogonal_kill` cited Chatterji for the general claim that canine cells are
# ferroptosis-competent, and treated the disease-specific question as open. A PubMed search for
# "hemangiosarcoma ferroptosis" returns ZERO results, which is what made it look open. The tumour
# type is in the panel; it is just recorded in a supplementary table that the indexed text does
# not cover.
# =============================================================================================

CANINE_HEMANGIOSARCOMA_IS_IN_THE_FERROPTOSIS_PANEL = {
    "citation": "Chatterji et al. 2024, bioRxiv 2024.04.28.591561, PMID 38746359, "
                "doi 10.1101/2024.04.28.591561",
    "the_panel": "31 canine cancer cell lines from the Flint Animal Cancer Center panel, profiled "
                 "against 14 compounds covering GPX4 modulators (RSL3, ML210, JKE-1674, FIN56), a "
                 "cystine transport inhibitor (IKE), glutathione biosynthesis inhibitors (L-BSO, "
                 "KOJ-1) and pro-oxidants (FINO2, jacaric acid)",
    "the_hemangiosarcoma_lines": ("Cindy-HSA", "Den-HSA", "SB"),
    "line_provenance": {
        "Den-HSA": "Golden Retriever, male castrate; VEGFR2, aVB3 integrin and fVIII-ra positive",
        "SB": "German Shepherd, male; TP53, PIK3CA and EP300 mutant",
        "Cindy-HSA": "female; further detail not collected",
    },
    "why_the_provenance_matters": "Den-HSA is from the breed this analysis is about, and SB carries "
                                  "a PIK3CA mutation -- the lesion the primary regimen targets. These "
                                  "are not distant proxies.",
    "the_lineage_result": "'Epithelial cancers (carcinomas) were enriched in the "
                          "ferroptosis-INSENSITIVE cluster, while SARCOMAS, undifferentiated "
                          "melanomas and hematological malignancies were ENRICHED FOR SENSITIVITY to "
                          "ferroptosis.' Separately: 'Rank ordering cell lines by sensitivity "
                          "indicates selectivity for killing NON-EPITHELIAL cells for ML210 but not "
                          "doxorubicin.'",
    "why_that_lands_on_this_disease": "hemangiosarcoma is a sarcoma of endothelial origin -- "
                                      "non-epithelial, mesenchymal. It sits in the class the panel "
                                      "found enriched for sensitivity, and the selectivity is "
                                      "specific to the GPX4 inhibitor rather than to cytotoxicity in "
                                      "general, since doxorubicin showed no such lineage pattern.",
    "the_mesenchymal_link_to_the_persister_state": "Hangauer's persisters occupy a 'high-mesenchymal "
                                                   "therapy-resistant state'. The lineage the canine "
                                                   "panel found most ferroptosis-sensitive is the "
                                                   "lineage the persister state resembles. In this "
                                                   "tumour the two arguments point the same way "
                                                   "instead of having to be bridged.",
    "the_conservation_claim": "'characteristic patterns of ferroptotic response across tumor types "
                              "seen in the human setting' are recapitulated, specifically including "
                              "'heightened sensitivity of mesenchymal tumor types'.",
    "what_this_does_not_establish": "per-line AUC values for the three hemangiosarcoma lines are in "
                                    "figure heatmaps and supplementary tables that could not be "
                                    "extracted, so it is NOT established that these three lines fell "
                                    "in the sensitive cluster. The class-level result is what is "
                                    "recorded. A line-level claim would be an inference dressed as a "
                                    "measurement.",
    "the_status_caveat": "still a preprint, not peer-reviewed at the time of writing. Recorded here "
                         "again rather than once, because this module leans on it harder than "
                         "`hsa_orthogonal_kill` did.",
    "and_the_wrong_test": "these are PARENTAL lines, not persisters derived from them. The Hangauer "
                          "claim is about the drug-tolerant state. Nobody has derived persisters from "
                          "Cindy-HSA, Den-HSA or SB and tested them. That is the missing experiment, "
                          "and it is now a specific one with named reagents rather than a wish.",
}

# =============================================================================================
# 5. TRANSFER REQUIRED, ACROSS THE RANGE OF POTENCIES THE ASSAY MIGHT HAVE SHOWN.
#
# Since the published per-line viability could not be read off, the requirement is computed against
# a spread of assumptions. The point is not to pick one; it is to show that the conclusion is the
# same across all of them, including the pessimistic end.
# =============================================================================================

_ASSUMED_THREE_DAY_VIABILITIES = (0.75, 0.50, 0.30, 0.20, 0.10)

TRANSFER_REQUIRED_BY_ASSUMED_POTENCY = {
    v: {
        "implied_rate_per_day": rate_from_burden_reduction(v, PERSISTER_ASSAY_DAYS),
        "transfer_required_for_0_045": transfer_required_from_viability(v),
        "transfer_required_for_0_040": transfer_required_from_viability(
            v, required=FIRST_NONZERO_PERSISTER_RATE_PER_DAY),
    }
    for v in _ASSUMED_THREE_DAY_VIABILITIES
}

HOW_THE_TRANSFER_ASK_COMPARES = {
    "the_range": "even at the most pessimistic assumption tested -- a three-day assay killing only a "
                 "quarter of persisters -- the transfer required is about 47%. At a 50% three-day "
                 "kill it is about 19%, and at the near-elimination the paper's language implies it "
                 "is under 10%.",
    "the_comparison": "the three vaccine-height routes needed 7-45% of their measured effect to "
                      "transfer, and routes 1 and 2 were judged plausible on that basis. The "
                      "persister route sits in the same band under any assumption except the very "
                      "weakest.",
    "what_this_overturns": "`hsa_orthogonal_kill.IT_WORKS_BUT_IT_IS_A_KNIFE_EDGE` says this route "
                           "'has no measured effect size at all in this compartment, and would need "
                           "essentially all of whatever it has'. The second half of that is WRONG and "
                           "is withdrawn. It needs a minority of what the assay shows, because the "
                           "requirement in assay units is small.",
    "what_it_does_not_overturn": "the first half stands in weakened form. There is still no measured "
                                 "in vivo per-day rate for a ferroptosis DRUG against persisters; "
                                 "there is an in vivo relapse-prevention result for target removal, "
                                 "and in vitro potency for tool compounds. The transfer figures above "
                                 "are computed from assumed in vitro numbers, and are therefore a "
                                 "sensitivity analysis rather than a measurement.",
    "the_direction_of_the_remaining_uncertainty": "in vitro-to-in vivo transfer for this mechanism is "
                                                  "argued by the FSP1 result to be BETTER than in "
                                                  "vitro suggests, since the lipid-peroxidation "
                                                  "defence matters more under physiological "
                                                  "conditions. That is one paper in one tumour type "
                                                  "and it is not treated as settled.",
}


# =============================================================================================
# 6. THE DURATION CRITERION, APPLIED TO THIS AGENT.
#
# `hsa_alternative_approach` invented the duration criterion to disqualify the MEK/mTOR pair:
# seventeen days of documented tolerability against a 3650-day horizon, a shortfall of 215x. The
# criterion is worth nothing if it is only applied to agents the analysis has already decided
# against. So it is applied here, to the mechanism this analysis is arguing FOR.
#
# The result is not comfortable. The one entry into this axis with a genuine chronic-dosing record
# in dogs has a dog-specific toxicity that emerges on exactly the timescale that matters.
# =============================================================================================

THE_CHRONIC_ENTRY_POINT_AND_WHY_IT_FAILS_IN_DOGS = {
    "the_tempting_shortcut": "the system xc- inhibitors -- sulfasalazine above all -- are the "
                             "ferroptosis-adjacent agents that already have decades of chronic human "
                             "dosing and established veterinary use. They deplete cysteine, hence "
                             "glutathione, hence GPX4's substrate. If any agent on this axis could "
                             "clear a ten-year duration criterion off the shelf, it would be this "
                             "one.",
    "the_canine_finding": {
        "citation": "Sansom, Barnett & Neumann 1985, Veterinary Record, PMID 2860750",
        "the_result": "thirteen dogs given sulphasalazine for colitis developed iatrogenic BILATERAL "
                      "keratoconjunctivitis sicca. 'The lacrimotoxic effect of sulphasalazine was "
                      "PERMANENT except in one case', and the authors recommend regular tear-secretion "
                      "monitoring for dogs on the drug.",
        "no_susceptible_subgroup": "'No breed, age or sex incidence was noted in this series, unlike "
                                   "in keratoconjunctivitis sicca cases due to other causes' -- so it "
                                   "cannot be dodged by patient selection.",
    },
    "the_timescale_that_makes_it_a_duration_problem": {
        "citation": "Barnett & Joseph 1988, Human Toxicology, PMID 3679245",
        "the_study": "a TWELVE-MONTH oral toxicity study of 5-aminosalicylic acid, sulfasalazine's "
                     "active metabolite, in dogs",
        "the_result": "'The condition was first diagnosed at STUDY WEEK 22 and subsequently PROGRESSED "
                      "both in incidence and severity', correlating with reduced Schirmer tear test "
                      "values. Treated females were more affected than males.",
        "why_this_is_the_decisive_number": "week 22 is about 154 days. A short course would never see "
                                           "it. The horizon this analysis models is 3650 days. The "
                                           "toxicity does not merely appear within the horizon -- it "
                                           "appears early in it and gets worse.",
    },
    "the_second_dog_specific_signal_in_the_same_class": {
        "citation": "Ekman et al. 1999, Pharmacology & Toxicology, PMID 10522751",
        "the_agent": "susalimod, a sulfasalazine analogue",
        "the_result": "'Dose-related bile duct hyperplasia appeared ONLY IN DOGS at doses >=75 "
                      "mg/kg/day, while in rats and monkeys it did not appear at doses up to 1500 and "
                      "2000 mg/kg/day respectively', after LONG-TERM administration",
        "the_mechanism_of_the_species_difference": "biliary concentration. The bile/plasma ratio was "
                                                   "3400 in the dog against 300 in the monkey and 50 "
                                                   "in the rat -- a roughly seventy-fold "
                                                   "concentration difference from rat to dog.",
        "why_it_is_recorded": "it is a second, independent, dog-specific chronic toxicity in this "
                              "chemical class, arising from canine biliary physiology rather than "
                              "from the pharmacology. Rodent safety data for this class does not "
                              "transfer to dogs, and this analysis is about dogs.",
    },
    "what_this_rules_out": "the cheap version of the answer. 'Use sulfasalazine, it is already given "
                           "to dogs long-term' does not survive contact with the canine literature. "
                           "Any plan that reaches for an off-the-shelf chronic system xc- inhibitor "
                           "for a ten-year horizon in a dog is wrong, and would have been caught by "
                           "the duration criterion if anyone had applied it.",
    "what_it_does_not_rule_out": "the mechanism. GPX4 and FSP1 inhibitors are not sulfonamides and do "
                                 "not share the lacrimal or biliary liabilities by construction. It "
                                 "rules out one shortcut into the axis, not the axis.",
    "the_uncomfortable_symmetry": "this is the same failure mode, in the same units, as the one that "
                                  "disqualified the second drug: a mechanism that works, an agent "
                                  "that exists, and a tolerability record that stops far short of the "
                                  "horizon. Recording it here rather than only there is the point of "
                                  "having the criterion at all.",
}


# =============================================================================================
# 7. DOES THE AGENT HAVE TO RUN FOR TEN YEARS?
#
# This is the question the 261x shortfall makes decisive, and Hangauer's own data say the answer
# should be no. Persisters are GENERATED by the targeted therapy, and the paper concludes:
# "pre- or post-treatment with GPX4 inhibitors, rather than co-treatment, may be adequate to
# deplete the pool of persister cells that survive targeted therapy or chemotherapy." Persisters
# also retain full RSL3 sensitivity "for at least two weeks but for less than two months" after
# drug washout, and 24h of RSL3 PRE-treatment reduces the pool that survives subsequent drug.
#
# So the schedule to test is a finite course, not a permanent one.
#
# ONE MODELLING DECISION DOES ALL THE WORK HERE, AND IT IS DECLARED BEFORE THE RESULT.
# `mapk_resistance.simulate_resistance` carries no extinction floor: state is a continuous fraction
# of carrying capacity, so a clone driven to 1e-30 regrows when the pressure stops. For a permanent
# kill that is harmless. For a finite course it is decisive, and it is an artifact -- a clone below
# one cell is gone, not waiting. So the finite schedules were run with a floor that zeroes any clone
# below one cell (1e-10 of carrying capacity, from `single_patient_cli.TUMOR_CELLS = 1e10`) at the
# end of the course, and also without it, as a control.
# =============================================================================================

PERSISTER_COURSE_AGENT_DAYS = {
    "continuous": 3620,
    "two_years": 700,
    "drug_year": 335,
    "pulsed_14_28_during_drug_year": 167,
    "six_months": 152,
}

FINITE_COURSE_RESCUE = {
    # applied kill/day on tolerant clones: {schedule: 10-year durability}, extinction floor applied.
    # phi = 0.95 antigen-null AND drug-resistant blind spot; baseline with no persister kill = 0.000.
    0.040: {"continuous": 0.117, "two_years": 0.000, "drug_year": 0.000,
            "pulsed_14_28_during_drug_year": 0.000, "six_months": 0.000},
    0.050: {"continuous": 1.000, "two_years": 0.000, "drug_year": 0.000,
            "pulsed_14_28_during_drug_year": 0.000, "six_months": 0.000},
    0.075: {"continuous": 1.000, "two_years": 1.000, "drug_year": 0.000,
            "pulsed_14_28_during_drug_year": 0.000, "six_months": 0.000},
    0.100: {"continuous": 1.000, "two_years": 1.000, "drug_year": 1.000,
            "pulsed_14_28_during_drug_year": 0.000, "six_months": 0.000},
}

# Measured directly from the simulation: the antigen-null resistant compartment starts at 0.015 of
# carrying capacity and its net growth under the regimen, with the vaccine unable to reach it, is
# this per day. Recovered consistently as (applied rate - observed log-decline) at three separate
# applied rates: 0.03329, 0.03345, 0.03350.
BLIND_SPOT_NET_GROWTH_PER_DAY = 0.0334
BLIND_SPOT_INITIAL_FRACTION = 0.015
TUMOR_CELLS = 1e10                      # single_patient_cli.TUMOR_CELLS, K = 1.0


def blind_spot_initial_cells(fraction: float = BLIND_SPOT_INITIAL_FRACTION) -> float:
    """How many cells the antigen-null resistant compartment starts with."""
    return float(fraction * TUMOR_CELLS)


def required_rate_for_course(course_days: float,
                             fraction: float = BLIND_SPOT_INITIAL_FRACTION,
                             net_growth: float = BLIND_SPOT_NET_GROWTH_PER_DAY) -> float:
    """Applied kill/day a course of `course_days` must deliver to extinguish the blind spot.

    The finite-course requirement has a closed form, because the course has to do a fixed amount of
    total work: drive the compartment from its starting size to below one cell before it stops. That
    is ln(N0) natural logs of net decline, and the agent must out-run the compartment's own growth
    to deliver them.

        applied >= net_growth + ln(N0) / course_days

    The first term is what it costs merely to hold the compartment still; the second is what it
    costs to clear it in the time available. As course_days grows the second term vanishes and the
    requirement falls to the holding rate -- which is why the continuous schedule is the cheapest
    per day and the most expensive in total exposure.
    """
    if course_days <= 0:
        raise ValueError("course_days must be positive")
    return float(net_growth + math.log(blind_spot_initial_cells(fraction)) / course_days)


REQUIRED_RATE_BY_COURSE = {
    name: {
        "agent_days": days,
        "required_rate_per_day": required_rate_for_course(days),
        "as_a_three_day_kill": 1.0 - viability_after(required_rate_for_course(days)),
        "duration_shortfall_vs_horizon": 3650 / days,
    }
    for name, days in PERSISTER_COURSE_AGENT_DAYS.items()
}

THE_CLOSED_FORM_PREDICTS_THE_SIMULATION = {
    "why_this_matters_more_than_the_table": "a table of five schedules is five data points. The "
                                            "closed form says WHY, predicts schedules that were "
                                            "never run, and can be checked against the table rather "
                                            "than merely summarising it.",
    "the_check": {
        # predicted threshold vs where the simulated table actually flips
        "continuous": "predicts 0.039; simulated 0.040 gives 0.117 and 0.050 gives 1.000 -- the "
                      "partial value sits exactly on the predicted boundary, which is what a "
                      "threshold looks like when the growth offset varies between trials",
        "two_years": "predicts 0.060; simulated 0.050 fails and 0.075 succeeds",
        "drug_year": "predicts 0.090; simulated 0.075 fails and 0.100 succeeds",
        "pulsed_14_28_during_drug_year": "predicts 0.146; simulated 0.100 fails",
        "six_months": "predicts 0.157; simulated 0.100 fails",
    },
    "the_verdict_on_the_check": "every simulated threshold falls in the interval the closed form "
                                "predicts, including the two schedules that fail at every rate "
                                "tested. The form is not fitted to the table -- its two constants "
                                "were measured from clone trajectories, not from durability values.",
    "what_it_reveals_that_the_table_hides": "the requirement is not really a rate. It is a fixed "
                                            "amount of total work -- about 19 natural logs, set by "
                                            "how many cells the blind spot starts with -- plus "
                                            "whatever it costs to out-run that compartment's growth "
                                            "while doing it. Duration and potency are "
                                            "interchangeable along that constraint, and the "
                                            "exchange rate is explicit.",
    "the_natural_logs_required": math.log(blind_spot_initial_cells()),
    "the_holding_rate": BLIND_SPOT_NET_GROWTH_PER_DAY,
}

THE_EXCHANGE_RATE_BETWEEN_DURATION_AND_POTENCY = {
    "the_trade": "cutting the course from ten years to one costs roughly a doubling of the rate: "
                 "0.050/day continuous becomes 0.090-0.100/day for a one-year course.",
    "in_the_units_the_assays_report": "that is a three-day kill rising from about 14% to about 26%. "
                                      "Both are modest against a mechanism whose tool compounds are "
                                      "described as 'among the compounds most selectively lethal to "
                                      "persister cells'.",
    "what_it_buys": "the duration shortfall against icFSP1's fourteen documented days falls from "
                    "261x to 24x. That is the difference between a category problem and an ordinary "
                    "drug-development one.",
    "where_it_stops_buying": "below about six months the required rate passes 0.15/day and both "
                             "short schedules fail at every rate tested. Pulsing 14-on/14-off "
                             "through the drug year halves the agent-days and fails, so the "
                             "two-weeks-of-retained-sensitivity window in Hangauer's washout "
                             "experiment does NOT license a duty cycle here. The course has to be "
                             "continuous while it runs; it just does not have to run forever.",
    "the_honest_reading_of_the_pulsing_failure": "this is a result against my own convenience. The "
                                                 "pulsed schedule was the one that would have made "
                                                 "the tolerability problem easiest, it is the one "
                                                 "Hangauer's washout data most tempts you toward, "
                                                 "and it does not work.",
}


# =============================================================================================
# 8. THE CONTROL, WHICH SHOWS THE WHOLE FINITE-COURSE RESULT RESTING ON ONE ASSUMPTION.
# =============================================================================================

FINITE_COURSE_WITHOUT_THE_EXTINCTION_FLOOR = {
    # Same 0.100/day, the highest rate tested, with the engine left as-is.
    "continuous": 1.000,
    "two_years": 0.000,
    "drug_year": 0.000,
    "pulsed_14_28_during_drug_year": 0.000,
}

EVERYTHING_IN_SECTION_7_DEPENDS_ON_THE_FLOOR = {
    "the_control_result": "without the extinction floor, EVERY finite schedule returns 0.000 at "
                          "0.100/day -- the rate at which the one-year course returns 1.000 with the "
                          "floor. The continuous schedule is unaffected, because a permanent kill "
                          "never lets the clone regrow whether or not it is formally extinct.",
    "so_the_result_is_entirely_a_consequence_of_the_assumption": "this is not a caveat at the "
                                                                 "margin. The difference between "
                                                                 "'a one-year course closes route 8' "
                                                                 "and 'only permanent dosing closes "
                                                                 "route 8' is exactly the floor.",
    "why_the_floor_is_nonetheless_the_right_choice": "`simulate_resistance` tracks a continuous "
                                                     "fraction of carrying capacity with no lower "
                                                     "bound, so a clone at 1e-30 of carrying "
                                                     "capacity -- 1e-20 of a single cell -- regrows "
                                                     "to detection. That is not conservatism, it is "
                                                     "a numerical artifact. Modelling clonal "
                                                     "extinction at one cell is standard and it is "
                                                     "what the biology does.",
    "where_the_choice_could_still_be_wrong": {
        "stochasticity_at_low_numbers": "the model is deterministic near extinction, so it treats "
                                        "one cell as a hard boundary. Real dynamics at ten or a "
                                        "hundred cells are stochastic: some trajectories die out "
                                        "above the threshold and some survive below the "
                                        "deterministic prediction. The sharp flip in the table would "
                                        "be a probability ramp in a birth-death model, and this "
                                        "analysis has NOT run one.",
        "how_close_the_calls_are": "at 0.075/day a one-year course leaves the compartment at about "
                                   "1.4e-8 of carrying capacity -- roughly 140 cells, two logs above "
                                   "the floor -- and returns 0.000. At 0.100/day it reaches about "
                                   "3.2e-12, roughly 0.03 of a cell, and returns 1.000. The decision "
                                   "is made in a two-log window, which is precisely the window where "
                                   "a deterministic model is least trustworthy.",
        "sanctuary_sites": "the compartment is modelled as well-mixed and uniformly exposed. Any "
                           "sanctuary -- a poorly perfused site, a site the agent does not reach -- "
                           "breaks the extinction argument outright, because ln(N0) is then the "
                           "wrong quantity and the surviving cells never see the rate at all.",
        "the_sensitivity_that_is_reassuring": "the requirement depends on the blind spot's starting "
                                              "size only through ln(N0). A ten-fold error in that "
                                              "size moves the required one-year rate by "
                                              "ln(10)/335 = 0.007/day, which is small next to the "
                                              "0.090 requirement. The result is robust to the "
                                              "quantity it is least sure of.",
    },
    "what_would_settle_it": "re-run the finite schedules in a stochastic birth-death formulation "
                            "rather than a deterministic one with a floor. That would replace the "
                            "step with an extinction probability and would give a defensible number "
                            "for the 0.075/day case instead of a 0.000 that is really 'about a "
                            "hundred cells left, deterministically'.",
}

# =============================================================================================
# 9. WHAT IS STILL NOT CLOSED.
#
# Longer than the section saying what closed, as promised in the module docstring.
# =============================================================================================

WHAT_IS_STILL_NOT_CLOSED = {
    "1_no_drug_has_the_in_vivo_result": "the relapse-prevention experiment is a genetic knockout. "
                                        "Every statement about a DRUG achieving this rate against "
                                        "persisters in vivo remains an extrapolation.",
    "2_no_persister_has_been_derived_from_this_disease": "the three canine hemangiosarcoma lines in "
                                                         "the ferroptosis panel are PARENTAL. The "
                                                         "Hangauer claim is about the drug-tolerant "
                                                         "state, and nobody has made persisters from "
                                                         "Cindy-HSA, Den-HSA or SB.",
    "3_the_potency_numbers_are_assumed_not_measured": "the transfer table sweeps assumed three-day "
                                                      "viabilities because the published per-line "
                                                      "values are in figures that could not be "
                                                      "extracted. It is a sensitivity analysis.",
    "4_the_gpx4_arm_is_judged_undruggable_by_the_field": "a 2026 statement of 'high toxicity, poor "
                                                         "selectivity and low-to-limited "
                                                         "bioavailability of GPX4 inhibitors in "
                                                         "vivo' is taken here as the operating "
                                                         "assumption.",
    "5_the_fsp1_arm_has_never_been_tested_on_a_persister": "the whole appeal of the parallel arm is "
                                                           "that FSP1 inhibitors work where GPX4 is "
                                                           "compromised, and a persister is arguably "
                                                           "such a context. No experiment tests it.",
    "6_no_agent_clears_the_duration_criterion_even_shortened": "a one-year course is 335 agent-days. "
                                                               "icFSP1's documented exposure is 14. "
                                                               "The shortfall falls from 261x to "
                                                               "24x, which is progress and is not "
                                                               "clearance.",
    "7_the_finite_course_result_rests_on_a_deterministic_extinction_floor": "see section 8. A "
                                                                           "stochastic model has not "
                                                                           "been run, and the "
                                                                           "decisive calls happen in "
                                                                           "a two-log window.",
    "8_none_of_this_is_needed_if_the_cheap_stain_comes_back_clean": "stain canine hemangiosarcoma "
                                                                    "for the vaccine antigen before "
                                                                    "and after PI3K/mTOR inhibition. "
                                                                    "If coverage is retained on "
                                                                    "drug-tolerant cells, route 8 "
                                                                    "stays benign and this entire "
                                                                    "module is unnecessary.",
}

VERDICT = {
    "what_changed": "the persister route was 'closable, not closed' because it had no anchor for its "
                    "rate and appeared to demand nearly everything the whole regimen delivers. Both "
                    "of those are now wrong. The requirement is a 12.6% three-day kill needing 6-47% "
                    "transfer; the in vivo endpoint match exists and is on residual disease; the "
                    "disease and species anchors exist with named cell lines; and the ten-year "
                    "dosing assumption that made the duration criterion fatal is not what the "
                    "biology indicates.",
    "what_did_not_change": "no drug has been shown to do it. Every closure above is a target-level "
                           "or class-level result plus a modelling argument, and the modelling "
                           "argument for the finite course depends on a deterministic extinction "
                           "floor.",
    "the_status": "CLOSED CONDITIONAL ON A NAMED EXPERIMENT, which is a stronger claim than "
                  "'closable' and a weaker one than 'closed'. The named experiment is specific, "
                  "cheap and uses reagents that already exist: derive persisters from Cindy-HSA, "
                  "Den-HSA and SB under PI3K/mTOR inhibition, measure their three-day viability "
                  "under a GPX4 or FSP1 inhibitor, convert it with `rate_from_burden_reduction`, and "
                  "compare against `required_rate_for_course(335)` = 0.090/day.",
    "the_order_to_do_it_in": "the antigen-retention stain first. It costs one experiment and it can "
                             "make all of the above unnecessary.",
    "what_this_module_refuses_to_say": "that the route is closed. 'Nearly solvable' is not closed, "
                                       "and neither is 'closed if a deterministic floor is the right "
                                       "model and a drug that has never been dosed past two weeks "
                                       "turns out to be chronically tolerable in dogs'. The gap is "
                                       "now a named and costed experiment rather than an unknown, "
                                       "and that is the honest description of the progress.",
}
