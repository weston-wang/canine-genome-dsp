"""What kills a cell the vaccine cannot see AND the drug cannot kill?

`hsa_antigen_adequacy` found the one case in this analysis with no answer: a subpopulation that is
both antigen-null and drug-resistant. Five percent of the tumour in that state takes ten-year
durability to 0.000, and continuous dosing does not rescue it.

The three closures offered there -- polyvalent antigens, epitope spreading, RNA-LPA-induced
spreading -- all try to make the vaccine SEE the cell. That is not an answer if it cannot. What is
needed is a kill mechanism orthogonal to BOTH axes: one that does not require the antigen and does
not act through the kinase pathway.

There is one, and its logic is the useful part: resistance is not free. A cell that survives
targeted therapy does so by entering a drug-tolerant persister state, and that state carries its own
dependency. You do not have to see the cell. You exploit what it had to become in order to survive.

See docs/HSA_DURABLE_RESPONSE.md.
"""
from __future__ import annotations

# =============================================================================================
# THE REQUIREMENT, STATED BEFORE ANY CANDIDATE IS PROPOSED.
# =============================================================================================

THE_ORTHOGONALITY_REQUIREMENT = {
    "must_not_need_the_antigen": "the failure mode is that the target is absent, so any answer "
                                 "routed through the vaccine's antigen is circular.",
    "must_not_act_through_the_kinase_pathway": "the cell is already resistant to PI3K/mTOR "
                                               "inhibition, so a third agent on the same axis buys "
                                               "nothing.",
    "must_be_givable_for_the_horizon": "the duration criterion from `hsa_alternative_approach` "
                                       "applies here too -- an agent with seventeen days of "
                                       "tolerability data does not qualify.",
    "why_this_is_a_narrow_gate": "most combination proposals fail one of the first two by "
                                 "construction. Adding another kinase inhibitor fails the second; "
                                 "adding another vaccine or a CAR against a second antigen fails "
                                 "the first, since it simply moves the coverage question to a "
                                 "different molecule.",
}

# =============================================================================================
# THE MECHANISM: RESISTANCE COSTS A DEPENDENCY.
# =============================================================================================

PERSISTERS_ACQUIRE_A_DEPENDENCY = {
    "citation": "Hangauer et al. 2017, Nature 551(7679):247-250, PMID 29088702, "
                "doi 10.1038/nature24297",
    "the_finding": "drug-tolerant persister cells derived from a WIDE RANGE OF CANCERS AND DRUG "
                   "TREATMENTS occupy a common high-mesenchymal therapy-resistant state, and that "
                   "state acquires a dependency on the lipid hydroperoxidase GPX4.",
    "the_consequence": "'Loss of GPX4 function results in selective persister cell ferroptotic "
                       "death in vitro and PREVENTS TUMOUR RELAPSE IN MICE.'",
    "why_the_endpoint_matters_here": "preventing relapse is the endpoint this entire analysis "
                                     "measures. Most combination data reports response or survival "
                                     "in bulk disease; this reports the thing the model actually "
                                     "simulates.",
    "why_it_satisfies_the_gate": "GPX4 dependency is a property of the persister STATE, not of any "
                                 "surface antigen and not of the kinase lesion that produced the "
                                 "resistance. It is orthogonal to both axes by construction rather "
                                 "than by luck.",
    "the_selectivity_is_the_point": "the kill is selective FOR persisters. It does not need to "
                                    "cover the whole tumour -- the rest is already covered -- which "
                                    "is why a modest rate applied to the right compartment can "
                                    "close a gap that no amount of untargeted cytotoxicity would.",
}

CANINE_CELLS_ARE_FERROPTOSIS_COMPETENT = {
    "citation": "Chatterji et al. 2024, bioRxiv 2024.04.28.591561, PMID 38746359, "
                "doi 10.1101/2024.04.28.591561",
    "the_finding": "'canine cancer cells exhibit sensitivity to a wide range of ferroptosis-inducing "
                   "perturbations in a manner INDISTINGUISHABLE FROM HUMAN CANCER CELLS, and "
                   "recapitulate characteristic patterns of ferroptotic response across tumor types "
                   "seen in the human setting'",
    "who_wrote_it": "Viswanathan, a co-author of the Hangauer persister-GPX4 paper, with Thamm at "
                    "Colorado State -- the same institution running VACCS and the losartan trial. "
                    "The species bridge was built deliberately by the people who found the "
                    "dependency.",
    "the_status_caveat": "a preprint, not peer-reviewed at the time of writing.",
    "what_it_removes": "the obvious first objection -- that ferroptosis biology might not transfer "
                       "to dogs. It does, across tumour types.",
}

# =============================================================================================
# THE AGENT: TESTED IN THIS DISEASE, AND ORALLY DOSED IN THIS SPECIES.
# =============================================================================================

PARTHENOLIDE_WAS_TESTED_IN_CANINE_HEMANGIOSARCOMA = {
    "citation": "Schlein et al. 2024, J Pharmacol Exp Ther 388(3):774-787, PMID 38135509, "
                "doi 10.1124/jpet.123.001851",
    "why_this_paper_exists": "it was written for exactly the three canine cancers with dismal "
                             "prognoses -- histiocytic sarcoma, HEMANGIOSARCOMA and disseminated "
                             "mast cell tumour -- rather than reaching hemangiosarcoma by accident.",
    "mechanism": "parthenolide inhibits canonical NF-kB signalling and alters cellular "
                 "reduction-oxidation balance; in canine cells it produced glutathione depletion, "
                 "reactive oxygen species generation and NF-kB inhibition",
    "the_result": "canine cell lines and PRIMARY cells are sensitive, undergoing dose-dependent "
                  "apoptosis",
    "the_combination_finding": "'Standard-of-care therapeutics broadly SYNERGIZE with PTL' -- which "
                               "is the property a fourth agent has to have to be addable to a "
                               "regimen that already has three.",
    "in_vivo": "parthenolide inhibited NF-kB activity and extended survival time in a mouse model "
               "of DISSEMINATED canine histiocytic sarcoma -- disseminated being the setting this "
               "analysis models",
    "the_link_to_the_dependency": "glutathione depletion is upstream of the same lipid-peroxidation "
                                  "axis GPX4 defends. This is not a different idea from the "
                                  "persister dependency; it is a druggable entry point into it.",
}

DMAPT_IS_THE_ORAL_FORM_AND_HAS_BEEN_GIVEN_TO_DOGS = {
    "citation": "Guzman et al. 2007, Blood 110(13):4427-4435, PMID 17804695, "
                "doi 10.1182/blood-2007-05-090621",
    "the_problem_it_solves": "'PTL has relatively poor pharmacologic properties that limit its "
                             "potential clinical use' -- so a family of analogues was made to "
                             "improve solubility and bioavailability.",
    "the_agent": "dimethylamino-parthenolide (DMAPT)",
    "oral_bioavailability": 0.70,
    "the_canine_evidence": "'pharmacologic studies using both mouse xenograft models and "
                           "SPONTANEOUS ACUTE CANINE LEUKEMIAS demonstrate in vivo bioactivity as "
                           "determined by functional assays and multiple biomarkers'",
    "the_target_class": "DMAPT 'selectively eradicates acute myelogenous leukemia STEM AND "
                        "PROGENITOR cells' -- a quiescent, therapy-surviving population of the same "
                        "class as the persisters this module is aiming at.",
    "why_this_closes_the_exposure_question": "an oral agent at 70% bioavailability with demonstrated "
                                             "in vivo bioactivity in spontaneous canine disease is "
                                             "not a compound that only works in a dish.",
    "what_is_still_missing": "no chronic canine tolerability data at the horizon this plan needs, so "
                             "DMAPT clears the exposure criterion and has NOT been shown to clear "
                             "the duration criterion. That is the same gap that disqualified the "
                             "MEK/mTOR pair, and it should not be waved through here because the "
                             "mechanism is attractive.",
}

# =============================================================================================
# THE SECOND ORTHOGONAL ARM, WHICH ALSO CORRECTS AN EARLIER OVER-CORRECTION.
# =============================================================================================

NK_CELLS_ARE_PARTLY_REHABILITATED = {
    "what_was_said_before": "`hsa_antigen_adequacy` refused NK cells as a route 8 closer because "
                            "missing-self recognition requires MHC-I downregulation, which an "
                            "antigen-null cell with intact presentation does not have.",
    "what_that_missed": "missing-self is not the only activating route. NKG2D recognises "
                        "STRESS-INDUCED ligands -- MIC-A and MIC-B -- which are induced by cellular "
                        "stress rather than by loss of presentation, and are therefore independent "
                        "of both the vaccine antigen and MHC-I status.",
    "the_canine_evidence": "MIC-A and MIC-B are present in dogs and significantly increased in "
                           "canine lymphomas, and canine NK cells carry NKG2D and NKp46 "
                           "(Lopez-Montano et al. 2023, Vet Immunol Immunopathol 264:110647, "
                           "PMID 37672843)",
    "why_it_fits_the_persister_logic": "a drug-tolerant cell under sustained therapeutic stress is "
                                       "a plausible stress-ligand expressor. The same state that "
                                       "creates the GPX4 dependency may also make the cell "
                                       "NK-visible without the vaccine ever seeing it.",
    "the_escape_that_comes_with_it": "the same study reports SOLUBLE MIC-A and MIC-B, which tumours "
                                     "shed to decoy NKG2D and impede NK cytotoxicity. So this arm "
                                     "has its own resistance mechanism, measurable in serum.",
    "the_honest_correction": "the earlier refusal was right about missing-self and wrong to treat "
                             "missing-self as the whole of NK recognition. NK cells are a partial "
                             "orthogonal arm, not a non-answer -- and not a complete answer either.",
    "what_would_settle_it": "stain canine hemangiosarcoma for MIC-A/MIC-B, before and after PI3K/"
                            "mTOR inhibition. If the drug-tolerant cells up-regulate stress ligands, "
                            "the NK component already in the regimen covers part of route 8 for "
                            "free.",
}


# =============================================================================================
# DOES IT ACTUALLY RESCUE THE ZERO? YES -- BUT THE ASK IS THE LARGEST IN THIS ANALYSIS.
#
# Persister-directed kill applied to the drug-tolerant clones only (the three resistance
# mechanisms, the antigen-loss escape clone, and the antigen-null resistant compartment), against a
# blind spot that is both invisible to the vaccine and drug-resistant at 95% coverage. The sensitive
# clones are untouched, which is what makes it persister-directed rather than a third cytotoxic.
# Seven clones, 150 trials, second drug withdrawn at year one.
# =============================================================================================

RESCUE_BY_PERSISTER_KILL = {
    #  kill/day on tolerant clones: 10-year durability at 95% antigen coverage
    0.000: 0.000,
    0.025: 0.000,
    0.030: 0.000,
    0.035: 0.000,
    0.040: 0.107,
    0.050: 1.000,
}

IT_WORKS_BUT_IT_IS_A_KNIFE_EDGE = {
    "the_good_news": "the mechanism does rescue the case nothing else touched. At 0.050/day on the "
                     "tolerant compartment, ten-year durability goes from 0.000 to 1.000 against a "
                     "blind spot that is both antigen-null and drug-resistant.",
    "the_bad_news": "the threshold is between 0.035 and 0.050/day, and below it the rescue is worth "
                    "exactly nothing -- 0.035/day still gives 0.000. This is not a ramp like the "
                    "vaccine-height curve. It is a step.",
    "why_it_is_a_step_here_and_a_ramp_there": "the antigen-null resistant clone is covered by "
                                              "nothing else, so its net growth is either positive "
                                              "or negative and there is no partial credit. Below "
                                              "the threshold it grows for ten years; above it, it "
                                              "is eliminated.",
    "how_big_the_ask_is": {
        "required_per_day": 0.045,
        "as_a_multiple_of_the_mek_requirement": 0.045 / 0.0225,
        "as_a_fraction_of_the_bar": 0.045 / 0.0515,
        "reading": "roughly twice what the MEK inhibitor is asked for, and about seven eighths of "
                   "the bar itself. The persister agent would have to deliver, on its own and "
                   "against one compartment, nearly what the entire regimen delivers against the "
                   "whole tumour.",
    },
    "the_comparison_that_does_not_work": "an earlier draft argued the ask was less daunting than it "
                                         "looks because the MEK/mTOR combination was measured "
                                         "removing 0.110-0.143/day in canine angiosarcoma, so rates "
                                         "of this magnitude are achievable in this tumour. That is a "
                                         "CATEGORY ERROR and it is withdrawn. Andersen's envelope "
                                         "was measured on drug-SENSITIVE bulk tumour, and it was "
                                         "achieved BY THE VERY DRUGS this cell is resistant to. What "
                                         "a drug does to cells that respond to it says nothing about "
                                         "what any agent does to cells that do not.",
    "the_other_mitigation_that_does_not_work": "nor does 'it only has to cover a small compartment'. "
                                               "The requirement is a RATE, per cell per day: net "
                                               "growth has to go negative regardless of how many "
                                               "cells there are. Population size affects delivery "
                                               "and toxicity, not the threshold.",
    "what_actually_remains_true": "ferroptosis is a complete death mechanism rather than a "
                                  "cytostatic one, so it is at least the KIND of mechanism that can "
                                  "produce a negative net rate rather than merely slowing growth. "
                                  "That is a statement about mechanism class, not about magnitude, "
                                  "and it is the only mitigation that survives.",
    "the_position_this_leaves": "weaker than the earlier draft claimed. There is no anchor at all "
                                "for the rate a ferroptosis inducer achieves against persisters in "
                                "vivo -- not a demanding bar with a reassuring comparison, but a bar "
                                "with nothing to compare it to.",
    "how_this_compares_to_the_other_routes": "the three vaccine-height routes needed only 7-45% of "
                                             "their measured effect to transfer. This one has no "
                                             "measured effect size at all in this compartment, and "
                                             "would need essentially all of whatever it has. It is "
                                             "the least comfortable answer in the analysis, and it "
                                             "is the only answer to this case.",
    "the_honest_verdict": "route 8's dangerous case is closable rather than closed. The mechanism is "
                          "right, the species and disease evidence exists, an orally dosed agent "
                          "exists -- and the rate required has never been measured for any of them. "
                          "Claiming this as solved would repeat the mistake this whole module was "
                          "written to catch.",
}

THE_EXPERIMENT_THIS_POINTS_AT = {
    "step_1": "stain canine hemangiosarcoma for the vaccine antigen before and after PI3K/mTOR "
              "inhibition. If coverage is retained on the drug-tolerant cells, none of this is "
              "needed and route 8 stays in its benign form.",
    "step_2": "if coverage is lost there, measure ferroptosis sensitivity of the drug-tolerant "
              "fraction specifically -- not the bulk line -- since the Hangauer claim is about the "
              "persister state, not the parental population.",
    "step_3": "convert that sensitivity into a per-day rate by the same method used for every other "
              "anchor in this analysis, and compare it against 0.045/day.",
    "why_this_ordering_matters": "step 1 is one stain and can make steps 2 and 3 unnecessary. Doing "
                                 "it first is the difference between a cheap answer and an "
                                 "expensive programme.",
    "the_models_already_exist": "Andersen's canine angiosarcoma tumorgrafts, the ISOS-1 syngeneic "
                                "line, and the canine ferroptosis panel Chatterji validated.",
}


# =============================================================================================
# THE BETTER ANSWER: DO NOT OUT-KILL THE INVISIBLE CELL, MAKE IT VISIBLE.
#
# The persister route needs ~0.045/day of new killing with no anchor for it. There is a cheaper
# target: the antigen is often SILENCED rather than absent. Antigen-presentation loss in cancer is
# frequently transcriptional and epigenetic, not deletional -- the machinery is present and switched
# off. If it can be switched back on, the 0.042/day vaccine already in the regimen does the work,
# and no new killing is required at all.
# =============================================================================================

ANTIGEN_LOSS_IS_OFTEN_REVERSIBLE = {
    "citation": "Shukla et al. 2021, Int J Mol Sci 22(4):1964, PMID 33671123, "
                "doi 10.3390/ijms22041964",
    "the_mechanism": "'A key mechanism of cancer immune evasion is downregulation of MHC-I and key "
                     "proteins of the antigen processing and presentation machinery (APM).' NLRC5 "
                     "is the master transcriptional activator of those genes, and 'genetic lesions "
                     "and EPIGENETIC MODIFICATIONS of NLRC5 are the most common cause of MHC-I "
                     "defects in cancers'.",
    "why_that_matters_here": "an epigenetically silenced antigen is present in the genome and "
                             "switched off. It can in principle be switched back on, which converts "
                             "route 8's catastrophic case into its benign one rather than requiring "
                             "a new kill mechanism.",
    "the_authors_own_caution": "'reversing the MHC-I defects remains the LEAST ADVANCED AREA of "
                               "tumor immunology.' This is a real mechanism in an immature field, "
                               "and it should not be quoted as a solved problem.",
    "the_limit_of_the_claim": "'genetic lesions AND epigenetic modifications' -- some fraction of "
                              "antigen loss is deletional and irreversible. Nothing here tells us "
                              "the split in canine hemangiosarcoma, and that split bounds how much "
                              "of the blind spot is recoverable.",
}

# The obvious epigenetic agent, tested in this disease, and it does not work.
HDAC_INHIBITION_WAS_TRIED_IN_CANINE_HSA_AND_FAILED = {
    "citation": "Suzuki et al. 2022, Vet Comp Oncol 20(4):805-816, PMID 35568976, "
                "doi 10.1111/vco.12840",
    "what_was_tested": "two HDAC inhibitors (SAHA, valproic acid) and one BET inhibitor (JQ1) in "
                       "canine hemangiosarcoma cell lines, in vitro and in vivo",
    "the_in_vitro_promise": "SAHA and JQ1 induced apoptosis; SAHA and VPA upregulated "
                            "inflammatory-related genes",
    "the_in_vivo_result": "'JQ1 suppressed HSA tumour cell proliferation in vivo ALTHOUGH SAHA AND "
                          "VPA DID NOT AFFECT TUMOUR GROWTH.' The two HDAC inhibitors -- the agents "
                          "that would be used for antigen re-expression -- failed the in vivo test "
                          "in this disease.",
    "the_second_problem": "SAHA and VPA 'attracted macrophage cell line RAW264 cells'. Given that "
                          "canine HSA macrophages are M2-polarised and PD-L1-positive and associate "
                          "with FEWER T cells (Gulay 2022), recruiting more macrophages into this "
                          "particular tumour is a plausible harm rather than a neutral side effect.",
    "the_honest_conclusion": "the most obvious antigen-re-expression agents were tried in the right "
                            "disease and did not work, and may make the microenvironment worse. "
                            "This route is not closed by reaching for an HDAC inhibitor.",
    "what_survives": "JQ1 worked in vivo, but BET inhibition is a proliferation and autophagy "
                     "effect here, not an antigen-restoration mechanism. It does not address route "
                     "8.",
}

# =============================================================================================
# WHAT DOES RESTORE PRESENTATION -- AND HAS BEEN GIVEN SYSTEMICALLY TO DOGS, TWICE.
# =============================================================================================

TYPE_I_INTERFERON_IS_THE_CONVERGENCE_POINT = {
    "the_mechanism": "type I interferon signalling upregulates MHC-I and the antigen-processing "
                     "machinery, which is the transcriptional programme whose loss produces the "
                     "invisible cell in the first place. Inducing it is antigen-agnostic -- it does "
                     "not require knowing which antigen was lost.",
    "why_this_unifies_three_separate_findings": "the RNA-LPA result that improved survivorship in "
                                                "client-owned dogs with glioma works through early "
                                                "type-I interferon responses; the same group showed "
                                                "those responses are what ENABLE epitope spreading; "
                                                "and STING agonism is a third entry point to the "
                                                "same axis. Restoring presentation, spreading the "
                                                "response beyond the vaccine's antigens, and "
                                                "reprogramming the suppressive microenvironment are "
                                                "one intervention, not three.",
    "canine_evidence_1_sting_in_client_owned_dogs": {
        "citation": "Lenz et al. 2025, J Immunother Cancer 13(12):e013715, PMID 41381219, "
                    "doi 10.1136/jitc-2025-013715",
        "design": "GSK856, a small-molecule dimeric amidobenzimidazole STING agonist, given "
                  "INTRAVENOUSLY to 19 client-owned dogs with naturally developing solid tumours; "
                  "two doses a week apart, then definitive-intent surgery",
        "the_result": "'Transcriptional analyses of pretreatment and post-treatment blood AND TUMOR "
                      "TISSUE revealed robust induction of ISGs' -- intratumoral target engagement, "
                      "not just a blood signal",
        "safety": "transient fever, lethargy and nausea, with IL-6 elevation consistent with "
                  "cytokine release syndrome; tolerated dose levels were identified",
        "why_it_matters_here": "this is the same class of target-engagement evidence this analysis "
                               "demanded of trametinib, delivered in the right species and in "
                               "tumour tissue.",
    },
    "canine_evidence_2_a_formulation_without_the_toxicity": {
        "citation": "Zhou et al. 2026, Science 392(6798):eadx1893, PMID 42096576, "
                    "doi 10.1126/science.adx1893",
        "the_agent": "CRYSTAL, a structurally ordered intermetallic nanoparticle self-assembled "
                     "from manganese ions intercalated with cyclic dinucleotides",
        "the_result": "'At an ultralow intravenous dose (0.003 milligrams per kilogram), CRYSTAL "
                      "activated STING in mice, DOGS, and nonhuman primates WITHOUT CYTOKINE "
                      "RELEASE SYNDROME'",
        "the_additional_effect": "'remodeled immunosuppressive environments, and promoted host "
                                 "STING-dependent CD8+ T cell priming' -- the same suppressive "
                                 "microenvironment routes 1 and 2 were built to lift",
        "why_it_matters_here": "the cytokine release syndrome seen with GSK856 is the obvious "
                               "objection to chronic STING agonism. This is a formulation that "
                               "reports avoiding it, across three species including dogs.",
    },
    "what_is_not_established": "no STING agonist or RNA-LPA has been given for hemangiosarcoma, "
                               "none has been dosed over the horizon this plan needs, and neither "
                               "canine study measured MHC-I or antigen re-expression directly -- "
                               "they measured interferon-stimulated genes, which is upstream of the "
                               "effect this route depends on. The mechanism is right and the "
                               "specific link is inferred.",
}


# =============================================================================================
# AND THE RE-EXPRESSION ROUTE, RUN. IT IS NOT ENOUGH ON ITS OWN.
#
# Vaccine applicability on the antigen-null resistant clone raised from 0 to a fraction, at the
# plan's operating point with the second drug withdrawn at year one. 150 trials, seven clones.
# =============================================================================================

DURABILITY_BY_RESTORED_REACH = {
    #  fraction of vaccine reach restored: (phi=0.95, phi=0.90, phi=0.80)
    0.00: (0.000, 0.000, 0.000),
    0.25: (0.000, 0.000, 0.000),
    0.50: (0.000, 0.000, 0.000),
    0.75: (0.000, 0.000, 0.000),
    1.00: (0.273, 0.293, 0.253),
}

RESTORATION_ALONE_DOES_NOT_CLOSE_IT = {
    "the_result": "even at FULL restoration of the vaccine's reach, durability reaches only "
                  "0.253-0.293. Against 0.840 with no blind spot and the 0.888 reference, that is "
                  "not a closure. Below full restoration it is a flat zero.",
    "why": "restoring the antigen moves the cell from 'covered by nothing' to 'covered by the "
           "vaccine only'. It is still DRUG-RESISTANT, and the vaccine wanes between two-monthly "
           "boosters, so its time-averaged kill is well below the 0.042/day peak. A drug-resistant "
           "clone starting at five percent of the tumour outruns that.",
    "what_it_does_change": "it converts an unsolvable case into a nearly-solvable one. Zero to 0.27 "
                           "is not a fix, but it is the difference between a cell nothing touches "
                           "and a cell that is merely short of cover.",
    "the_correction_this_forces": "the re-expression route was written up before this was run, and "
                                  "presented as the better answer because it needed no new killing. "
                                  "That was premature. It needs no new killing and it does not "
                                  "work alone.",
    "what_it_implies_about_the_regimen": "if a blind spot exists, the second drug cannot be "
                                         "withdrawn -- restoring visibility gives the vaccine a "
                                         "target but not enough margin without the drug's "
                                         "0.0225/day on top. That reconnects this route to the "
                                         "toxicity finding rather than escaping it.",
}


# =============================================================================================
# THE COMBINATION THAT CLOSES IT.
#
# Restoration alone tops out at 0.273 because the cell is still drug-resistant and the vaccine wanes
# between boosters. The missing 0.0225/day is already in the regimen -- it is the second drug, which
# the toxicity work had converted into a one-year induction. Putting it back closes the route.
# =============================================================================================

RESTORED_REACH_TIMES_DRUG_SCHEDULE = {
    #  restored reach: {second drug withdrawn at year 1, second drug never withdrawn}
    0.50: {"stop_at_year_1": 0.000, "never_stop": 0.020},
    0.75: {"stop_at_year_1": 0.000, "never_stop": 0.873},
    1.00: {"stop_at_year_1": 0.273, "never_stop": 1.000},
}

THIS_IS_THE_CLOSURE = {
    "the_result": "75% restoration of vaccine reach with the second drug CONTINUED gives 0.873, "
                  "which beats the 0.840 no-blind-spot baseline and essentially matches the 0.888 "
                  "reference. Full restoration with the drug continued gives 1.000.",
    "what_each_part_contributes": "neither half works alone. Restoration alone tops out at 0.273; "
                                  "continuing the drug alone was measured earlier at 0.000. "
                                  "Together they clear it, because the vaccine supplies a target "
                                  "the drug cannot kill and the drug supplies the margin the "
                                  "waning vaccine cannot hold.",
    "the_threshold_is_between_50_and_75_percent": "at half restoration with the drug continued the "
                                                  "figure is 0.020 -- still a failure. The usable "
                                                  "range starts somewhere between 50% and 75%, and "
                                                  "the grid does not resolve it more finely than "
                                                  "that.",
    "why_this_is_a_softer_ask_than_the_persister_route": "0.045/day of novel killing against "
                                                         "persisters has no measured anchor "
                                                         "anywhere. Restoring three quarters of "
                                                         "antigen presentation is a transcriptional "
                                                         "effect with an established mechanism "
                                                         "(type I interferon on MHC-I and the "
                                                         "antigen-processing machinery) and two "
                                                         "independent systemic canine "
                                                         "demonstrations of the upstream trigger.",
    "the_price_and_it_is_not_small": "the second drug goes back to indefinite dosing for these "
                                     "dogs. The one-year induction that solved the toxicity problem "
                                     "is only available to dogs WITHOUT a blind spot. This route "
                                     "does not escape the toxicity finding -- it reopens it for a "
                                     "subgroup, and says so.",
    "what_this_makes_the_stain_worth": "the single antigen-retention stain now decides which of two "
                                       "regimens a dog gets: a one-year induction if the antigen "
                                       "survives on drug-tolerant cells, or indefinite dosing plus "
                                       "an interferon-axis agent if it does not. That is a "
                                       "treatment-assignment decision resting on one measurement.",
}

VERDICT_ON_ROUTE_8 = {
    "is_the_dangerous_case_closed": "yes, in the model, by a combination that needs no new agent "
                                    "class beyond the interferon-axis one -- 75% restored antigen "
                                    "presentation plus the second drug continued reaches 0.873.",
    "what_had_to_be_abandoned_to_get_there": "the one-year induction. Every version of this route "
                                             "that withdraws the second drug fails, at every level "
                                             "of restoration tested.",
    "the_two_routes_compared": "NEITHER DOMINATES, and an earlier draft that called restoration the "
                               "better bet and the persister route the fallback was wrong, because "
                               "it ignored the axis the whole toxicity section exists to protect. "
                               "The persister route reached 1.000 WITH THE SECOND DRUG STOPPED AT "
                               "YEAR ONE -- it preserves the one-year induction. The restoration "
                               "route requires the drug indefinitely. So the persister route is "
                               "better on toxicity and worse on evidence; restoration is better on "
                               "evidence and worse on toxicity.",
    "how_to_choose_between_them": "by what the antigen-retention stain shows, and then by which "
                                  "cost is acceptable. If antigen loss is epigenetic, restoration "
                                  "is available and costs lifelong dosing. If it is deletional, "
                                  "restoration is impossible and the persister route is the only "
                                  "option -- which is also the one that keeps the induction short. "
                                  "They are alternatives with different prices, not a preference "
                                  "and a backup.",
    "the_combination_nobody_has_costed": "partial restoration plus partial persister kill was not "
                                         "simulated. Both are unanchored effects and combining two "
                                         "unmeasured quantities to clear a threshold would be "
                                         "exactly the kind of arithmetic this analysis has "
                                         "repeatedly refused elsewhere.",
    "what_is_still_unmeasured": "how much antigen presentation a STING agonist or RNA-LPA actually "
                                "restores in canine hemangiosarcoma. Both canine studies measured "
                                "interferon-stimulated genes, which is upstream. Nobody has "
                                "measured the 75%.",
    "the_honest_status": "closed in the model, on a mechanism with real canine evidence for its "
                         "trigger and none for its magnitude. Same standard as every other route "
                         "here: a defensible plan, not a demonstrated result.",
}
