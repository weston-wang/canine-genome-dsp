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
