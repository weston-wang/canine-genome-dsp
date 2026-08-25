"""The items left open by hsa_parallel_pathway, and what closes each.

Four things were flagged as unresolved when the two-node combination was proposed. Three close on
evidence or on arithmetic already in hand; the fourth narrows to a specific, stated residual.

See docs/HSA_DURABLE_RESPONSE.md.
"""

# ---------------------------------------------------------------------------------------------
# 1. "The kinase-domain mutation is not covered." It is. This was a bookkeeping error.
KINASE_DOMAIN_IS_COVERED = {
    "the_claim_that_was_wrong": "hsa_parallel_pathway.VERDICT listed kinase_domain_mutation as NOT "
                                "covered while separately listing pi3k_akt_feedback_reactivation as "
                                "covered. In the model those are the same clone: index 1, which "
                                "carries the 9.5x fold-shift measured for M2327I.",
    "why_it_is_covered": "a mutation in mTOR's own kinase domain confers no protection against MEK "
                         "inhibition. It is a different node on a different pathway. That is the "
                         "entire point of hitting two parallel nodes -- a lesion in one does not "
                         "shelter the clone from the other.",
    "supporting_measurement": "Wei et al. 2020, PMID 32943547 -- the MEK + dual TORC1/2 pair "
                              "suppressed pathway RECIPROCAL crosstalk in vivo, which is the "
                              "cross-coverage this argument depends on.",
    "verified_in_the_engine": "clone 1 sets the bar at 0.0445 without the second drug and falls to "
                              "0.0300 with it at the swept requirement -- the MEK inhibitor is "
                              "precisely what brings the kinase-domain clone to the vaccine's kill "
                              "rate.",
    "status": "CLOSED -- no residual. The pair covers all four modelled drug-resistance mechanisms.",
}

# ---------------------------------------------------------------------------------------------
# 2. "The obvious closure for route 4 was tried and made things worse."
#
# It did. But reading the trial carefully, it was not the experiment the requirement describes.
EBAT_REDOSING_TESTED_SOMETHING_ELSE = {
    "citation": "Borgatti et al. 2020, Vet Comp Oncol 18(4):664-674, PMID 32187827 (SRCBST-2), "
                "doi 10.1111/vco.12590",
    "what_changed_between_the_trials": (
        "three cycles instead of one",
        "the interval from doxorubicin was REDUCED -- eBAT scheduled one week before chemotherapy, "
        "against a DELAYED chemotherapy start in the trial that worked",
        "eligibility widened to stage 3, against a minimal-residual-disease setting originally",
    ),
    "result": "25 dogs; six acute hypotension, two hospitalised; no significant survival benefit "
              "against a contemporary stage 1-3 standard-of-care group.",
    "the_authors_own_reading": "'repeated dosing cycles of eBAT STARTING 1 WEEK PRIOR TO DOXORUBICIN "
                               "chemotherapy led to greater toxicity and reduced efficacy compared "
                               "with a single cycle given between surgery and a DELAYED START of "
                               "chemotherapy' -- the failure is attributed to schedule relative to "
                               "chemotherapy, not to dose or to duration.",
    "what_it_therefore_does_not_refute": "the requirement is a persistent kill term that antigen "
                                         "loss does not affect. SRCBST-2 varied schedule, chemo "
                                         "interval and disease stage simultaneously. It never tested "
                                         "persistence in the population the requirement is about.",
    "status": "the negative result stands as a fact about that regimen and is NOT evidence against "
              "the requirement. A supplier is still needed -- see below.",
}

# ---------------------------------------------------------------------------------------------
# 3. A supplier for route 4 whose repeat dosing has no such failure mode.
#
# Antigen loss is the escape where the tumour stops displaying what the vaccine trained against.
# NK cells are the one effector class for which that escape is an ATTRACTANT rather than a shield.
NK_CELLS_INVERT_THE_ESCAPE = {
    "principle": "NK cells are restrained by MHC class I. A tumour cell that downregulates MHC-I to "
                 "hide from T cells removes the very signal that was holding NK cells back -- "
                 "'missing self'. The act of escaping one effector exposes the cell to another.",
    "human_evidence": "Malmberg et al. 2017, Immunogenetics 69(8-9):547-556, PMID 28699110 -- immune "
                      "selection under checkpoint blockade paves the way for NK-cell missing-self "
                      "recognition.",
    "does_the_mechanism_exist_in_DOGS": {
        "citation": "Gingrich et al. 2023, ImmunoHorizons 7(11):760-770, PMID 37971282, "
                    "doi 10.4049/immunohorizons.2300092",
        "the_prior_doubt": "canine Ly49 had been reported as mutated and nonfunctional, which would "
                           "mean dogs lack the conventional missing-self mechanism entirely",
        "what_they_found": "Ly49/KLRA1 is expressed in resting and activated canine NK cells and "
                           "almost exclusively in the NK cluster at single-cell level; the modelled "
                           "tertiary structure shows significant similarity to the murine system; "
                           "docking with MHC-I was favourable, converging on a single low-energy "
                           "conformation",
        "strength_of_this_evidence": "expression plus computational structure and docking. It "
                                     "resolves the prior doubt in favour of the mechanism existing, "
                                     "but it is PREDICTED binding, not a functional demonstration "
                                     "that canine NK cells kill MHC-I-low targets preferentially. "
                                     "That experiment has not been reported.",
    },
    "why_repeat_dosing_does_not_repeat_the_ebat_failure": "eBAT is a foreign bacterial toxin "
                                                          "construct; its redosing problems were "
                                                          "hypotension and immunogenicity. "
                                                          "Autologous NK cells are the dog's own "
                                                          "cells, so neither failure mode applies.",
}

CANINE_NK_HAS_BEEN_GIVEN_TO_DOGS = {
    "citation": "Canter et al. 2017, J Immunother Cancer 5(1):98, PMID 29254507, "
                "doi 10.1186/s40425-017-0305-7",
    "manufacturing": "NK cells isolated from PBMCs and expanded with irradiated feeder cells and "
                     "IL-2: 19.0-fold expansion and 258.9 x 10^6 cells by day 14",
    "first_in_dog_trial": "10 dogs with spontaneous osteosarcoma, focal radiotherapy plus "
                          "intra-tumoral autologous NK transfer: 5 of 10 metastasis-free at the "
                          "6-month primary endpoint, with resolution of suspicious pulmonary "
                          "nodules in one dog",
    "follow_up": "Judge et al. 2020, PLOS ONE 15(2):e0224775, PMID 32084139 -- updated survival "
                 "included one dog at 17.9 months; the injected product reached near 100% granzyme B "
                 "and NKp46 expression at day 17-19",
    "what_is_missing_for_HSA": "every canine NK trial to date is in osteosarcoma, and delivery was "
                               "intra-tumoral alongside radiotherapy. Hemangiosarcoma after "
                               "splenectomy is a minimal-residual-disease setting with no target to "
                               "inject, so this would need systemic delivery -- a different problem "
                               "with its own evidence gap.",
    "status": "a real, manufacturable, dog-tested effector class exists for route 4, and its "
              "mechanism is the one that inverts antigen loss rather than being defeated by it. It "
              "has not been given for hemangiosarcoma and not given systemically.",
}

# ---------------------------------------------------------------------------------------------
# 4. "Target engagement was not observed." It was assayed a week before the drug reached steady state.
TARGET_ENGAGEMENT_WAS_ASSAYED_TOO_EARLY = {
    "the_flag": "Takada et al. 2024 (PMID 38889903) looked for trametinib target engagement in "
                "tumour biospecimens and did not find it.",
    "when_they_looked": "days 0 and 7",
    "when_the_drug_reaches_steady_state": "approximately 14 days, reported in the same paper",
    "the_arithmetic": "the day-7 biopsy precedes steady state by a week. Trametinib also accumulates "
                      "3-4x on daily dosing (Wei et al. 2022, PMID 36590793), so a day-7 sample sits "
                      "well below the concentration the efficacy claim rests on.",
    "what_this_does_and_does_not_settle": "it removes the finding as evidence AGAINST engagement -- "
                                          "the assay ran before the exposure existed. It does not "
                                          "supply positive evidence FOR engagement, which remains "
                                          "unmeasured in canine tumours.",
    "status": "CLOSED as an objection, OPEN as a confirmation. A biopsy at day 21-28 would settle it.",
}

# ---------------------------------------------------------------------------------------------
# 5. "The lab work used a different MEK inhibitor from the one dosed in dogs."
#
# The exposure conclusion does not actually depend on the substitution: trametinib has its own
# threshold, reported by the same trial that measured what dogs reach.
TWO_INDEPENDENT_EXPOSURE_ANCHORS = {
    "anchor_1_cross_drug": "Andersen's canine angiosarcoma combination IC50 of 11 nM, measured with "
                           "PD0325901, against the 16.2 nM trametinib reaches in dogs -- a 1.48x "
                           "margin, but carried across two different MEK inhibitors.",
    "anchor_2_same_drug": "Takada et al. 2024 identify 10 ng/mL as the trametinib concentration "
                          "associated with clinical efficacy in humans, and report that about 70% of "
                          "dogs reach it at the maximum tolerated dose. That is trametinib's own "
                          "threshold against trametinib's own measured exposure, with no "
                          "substitution at all.",
    "they_agree": "10 ng/mL IS 16.2 nM. The two anchors are the same number reached two ways: one "
                  "from canine tumour pharmacology, one from the drug's own clinical threshold.",
    "residual": "what is still not measured is trametinib's combination IC50 in canine HSA cells "
                "specifically. Trametinib is the more potent MEK1/2 inhibitor of the two, so "
                "carrying PD0325901's requirement across is conservative.",
    "status": "CLOSED -- the exposure claim no longer rests on the substitution.",
}

# ---------------------------------------------------------------------------------------------
# 6. "The rupture hazard is a swept range, not a measurement."
RUPTURE_IS_NOW_GROUNDED_IN_A_REAL_COHORT = {
    "citation": "Ruffoni et al. 2025, J Am Vet Med Assoc 263(8):985-990, PMID 40334697, "
                "doi 10.2460/javma.25.01.0044",
    "design": "prospective, nationwide, 345 dogs presenting with spontaneous haemoperitoneum from a "
              "ruptured splenic tumour, October 2020 to June 2024 -- the largest prospective series "
              "of its kind",
    "composition": {"hemangiosarcoma": 0.562, "benign": 0.357, "other_malignant": 0.081},
    "what_it_closes": "rupture is not a rare complication to be swept over a wide range -- it is how "
                      "the majority of these tumours announce themselves, and the denominator is now "
                      "a real prospective cohort rather than an assumption.",
    "what_it_does_not_close": "this measures the composition of dogs who ALREADY ruptured. The "
                              "quantity the survival conversion needs is the annual rupture hazard "
                              "for a treated dog in remission, which is a different number and still "
                              "unmeasured.",
    "why_the_screening_conclusion_survives_anyway": "screening removes the detected fraction of "
                                                    "whatever the hazard is, so the case for "
                                                    "surveillance does not depend on pinning the "
                                                    "rate down. The 345-dog cohort also shows 35.7% "
                                                    "of ruptures are benign, which means a screening "
                                                    "programme's false-positive cost is partly a "
                                                    "real-disease cost rather than a wasted one.",
    "status": "NARROWED -- the pathway is grounded in real prospective data; the post-remission "
              "hazard remains the one swept quantity, and the conclusion it feeds is insensitive to "
              "it.",
}

SUMMARY = {
    "kinase_domain_mutation": "CLOSED -- covered by the MEK inhibitor; the gap was a bookkeeping "
                              "error, verified against the engine.",
    "therapy_that_made_things_worse": "CLOSED as an objection -- SRCBST-2 varied schedule, chemo "
                                      "interval and disease stage at once, and its authors attribute "
                                      "the harm to chemotherapy timing. It did not test the "
                                      "requirement.",
    "route_4_supplier": "IDENTIFIED -- autologous NK cells, whose missing-self mechanism inverts "
                        "antigen loss, expanded and given to dogs in first-in-dog trials. Not yet "
                        "given for HSA and not yet systemically.",
    "target_engagement": "CLOSED as an objection -- assayed at day 7 against a 14-day steady state.",
    "mek_inhibitor_substitution": "CLOSED -- trametinib's own efficacy threshold and the cross-drug "
                                  "requirement are the same 16 nM.",
    "rupture_hazard": "NARROWED -- grounded in a 345-dog prospective cohort; the post-remission rate "
                      "stays swept and the screening conclusion does not depend on it.",
    "what_is_genuinely_left": "two things, both positive-evidence gaps rather than contradictions: "
                              "nobody has shown trametinib engaging its target inside a canine "
                              "tumour, and nobody has given NK cells systemically for "
                              "hemangiosarcoma. Neither is refuted; both are unmeasured.",
}
