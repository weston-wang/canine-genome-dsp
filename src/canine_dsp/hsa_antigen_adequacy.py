"""The antigen gap: the model assumed the vaccine's target was on every cell to begin with.

Escape route 4 has always been antigen LOSS -- a variant arises by mutation, stops displaying the
target, and outgrows the response. That is a real route and it is modelled. What was never modelled
is antigen INADEQUACY: the target being absent from part of the tumour, or from the tumour
entirely, on day zero.

The distinction was easy to miss because both end with cells the vaccine cannot see. It matters
because the two have completely different arithmetic. A loss variant starts at zero and has to be
seeded at 1e-8/day against a shrinking antigen-positive population. An inadequacy fraction starts
at whatever fraction of the tumour it is -- possibly a fifth, possibly all of it -- and never had
to arise at all.

It also matters because every route this analysis proposes for raising vaccine height -- checkpoint
blockade, monocyte-recruitment blockade, re-dosing non-responders -- assumes the antigen works. If
the antigen is wrong, all three are worth nothing, and the model would not notice.

Calviri's VACCS trial is the reason this is not hypothetical: 800+ dogs, a defined 31-antigen
vaccine that listed hemangiosarcoma among its eight target cancers, and hemangiosarcoma was not
among the tumours it reduced.

See docs/HSA_DURABLE_RESPONSE.md.
"""
from __future__ import annotations

# =============================================================================================
# THREE WAYS AN ANTIGEN CAN BE INADEQUATE, WHICH ARE NOT THE SAME PROBLEM.
# =============================================================================================

THREE_MODES_OF_INADEQUACY = {
    "uniform": "every tumour cell displays the target, but at a fraction phi of the density the "
               "response needs. The vaccine is dimmer everywhere. This is EXACTLY a reduction in "
               "vaccine height, so the existing height grid already prices it and the three "
               "height-raising routes still apply.",
    "heterogeneous": "a fraction (1-phi) of cells never display the target at all. They are "
                     "ordinary tumour cells in every other respect -- same growth, same drug "
                     "sensitivity -- simply invisible to the vaccine, and present from day zero at "
                     "high frequency rather than arising by mutation. This is NOT a height "
                     "reduction and no amount of extra height fixes it.",
    "inter_patient": "the target fits some dogs' tumours and not others'. Within the model this is "
                     "indistinguishable from vaccine take-rate, which is already the second-largest "
                     "lever in the analysis -- but the remedy is different. Take-rate failure is "
                     "answered by checkpoint blockade or re-dosing; antigen misfit is answered only "
                     "by changing the antigen.",
    "why_the_split_matters": "the first is a dial the plan already knows how to turn. The second is "
                             "a floor the plan cannot reach. The third is a patient-selection "
                             "problem masquerading as a potency problem.",
}


def effective_height_uniform(height: float, coverage: float) -> float:
    """Vaccine height after uniform partial expression: the target is dimmer on every cell.

    This mode reduces to a height change, which is why it needs no new machinery -- feed the result
    into the existing height grid. The heterogeneous mode has no such reduction and must be
    simulated with a separate antigen-null compartment.
    """
    if height < 0:
        raise ValueError("height must be nonnegative")
    if not 0.0 <= coverage <= 1.0:
        raise ValueError("coverage is a fraction between 0 and 1")
    return float(height * coverage)


# =============================================================================================
# WHAT THE LITERATURE ACTUALLY REPORTS -- AND WHAT IT DOES NOT.
#
# Every antigen study in this disease reports SAMPLE-level positivity: does this tumour stain.
# None reports CELL-level coverage: what fraction of cells within the tumour stain. Sample-level
# positivity bounds the inter-patient mode and says nothing at all about the heterogeneous mode,
# which is the one that cannot be fixed by turning the plan's dials.
# =============================================================================================

WHAT_IS_MEASURED_IS_SAMPLE_LEVEL = {
    "vimentin_and_cd31": {
        "citation": "Janus et al. 2016, Acta Vet Hung 64(1):90-102, PMID 26919146",
        "finding": "in canine cardiac haemangiosarcoma, 'CD31, vimentin, and beta-catenin showed a "
                   "positive reaction in all 11 samples examined'",
        "what_it_settles": "vimentin -- the antigen the eVim vaccine targets -- is present in every "
                           "tumour tested. That closes the inter-patient mode for this antigen, on "
                           "a small sample.",
        "what_it_does_not_settle": "11 of 11 tumours staining positive is not 100% of cells within "
                                   "each tumour staining positive. Immunohistochemistry reported as "
                                   "'positive' is compatible with a substantial antigen-null "
                                   "subpopulation.",
    },
    "b7_h3": {
        "citation": "De Maria et al. 2025, Cancer Immunol Immunother 74(10):306, PMID 40944715",
        "finding": "'B7-H3 was consistently detected across all analyzed canine sarcoma subtypes, "
                   "including osteosarcoma, soft tissue sarcoma, and hemangiosarcoma, although with "
                   "VARIABLE LEVELS OF EXPRESSION INTENSITY'",
        "why_that_phrase_is_the_whole_problem": "variable intensity is exactly the ambiguity this "
                                                "module exists to separate. It is consistent with "
                                                "the uniform mode (every cell dimmer, recoverable) "
                                                "and equally consistent with the heterogeneous mode "
                                                "(some cells absent, not recoverable). The "
                                                "measurement that distinguishes them was not made.",
        "the_platform": "canine B7-H3-CAR.CIK lymphocytes killed canine sarcoma lines 45% vs 8% at "
                        "E:T 1:1 and 3D spheroids 58% vs 13% -- a canine antigen-directed cell "
                        "therapy with hemangiosarcoma coverage, if the antigen holds up",
    },
    "the_tumour_is_definitionally_mixed": {
        "citation": "Cheng et al. 2021, Brief Bioinform 22(4):bbaa252, PMID 33078825",
        "finding": "the pathognomonic feature of this tumour is 'irregular vascular channels that "
                   "are filled with blood and are lined by a MIXTURE of malignant and nonmalignant "
                   "endothelial cells', and diagnosis is complicated 'when tumor cells are "
                   "undetectable due to the presence of excessive amounts of nontumor cells'",
        "why_it_belongs_here": "a tumour whose defining histology is a mixed cell population is a "
                              "poor candidate for the assumption that one antigen covers every "
                              "cell. This is not proof of a blind spot; it is a reason not to "
                              "assume its absence.",
    },
    "the_measurement_nobody_has_made": "for any candidate hemangiosarcoma antigen -- vimentin, "
                                       "B7-H3, CD31, or Calviri's RNA-error-derived neoantigens -- "
                                       "no published study reports the FRACTION OF CELLS within a "
                                       "canine hemangiosarcoma that display it. That single number "
                                       "decides which of the two modes applies, and it is a "
                                       "quantitative immunohistochemistry or flow experiment on "
                                       "tissue that already sits in biobanks.",
}

# ---------------------------------------------------------------------------------------------
# THE TRIAL THAT MAKES THIS CONCRETE.
VACCS_FAILED_ON_THIS_DISEASE_SPECIFICALLY = {
    "trial": "Vaccination Against Canine Cancer Study (VACCS), Calviri Inc.",
    "design_citation": "Burton et al. 2024, Vet Immunol Immunopathol 267:110691, PMID 38056066",
    "design": "randomized, placebo-controlled, 800+ healthy dogs aged 5.5-11.5 years at Colorado "
              "State, Wisconsin-Madison and UC Davis; 31 shared RNA-error-derived neoantigens drawn "
              "from eight canine cancers INCLUDING hemangiosarcoma; four priming doses two weeks "
              "apart then annual boosters; five-year follow-up; primary endpoint cumulative "
              "incidence of malignant neoplasia of any type",
    "the_scale": "the largest interventional cancer clinical trial ever conducted in companion dogs",
    "reported_outcome": "mast cell tumours and adrenal tumours were reduced. Hemangiosarcoma was "
                        "not.",
    "the_investigator_on_why": "Stephen Johnston, quoted: 'We now know why -- we just didn't put "
                               "the right components in. So, the next version will have components "
                               "for hemangiosarcoma.'",
    "the_provenance_caveat": "this outcome is reported from an interview with the company's chief "
                             "executive in a consumer outlet, not from a peer-reviewed publication. "
                             "The primary efficacy analysis remained unpublished more than two "
                             "years after the trial closed in May 2024, and the accompanying claim "
                             "of 'a reduction in the number of tumors for about 65 percent of dogs "
                             "vaccinated' is not a standard endpoint. Treat as directionally "
                             "informative, not established.",
    "why_it_is_decisive_for_this_module": "it is a failure attributed by the people who ran it to "
                                          "ANTIGEN CHOICE rather than to potency, persistence or "
                                          "the microenvironment -- the three things this analysis "
                                          "had been optimising. A model with no antigen-adequacy "
                                          "term cannot represent that failure at all.",
}

# ---------------------------------------------------------------------------------------------
# AND THE PATTERN THE FOUR HSA VACCINE RESULTS MAKE, ONCE COVERAGE IS THE ORGANISING VARIABLE.
COVERAGE_EXPLAINS_WHICH_VACCINES_WORKED = {
    "evim": {
        "antigen": "DEFINED -- recombinant vimentin",
        "coverage_evidence": "vimentin positive in 11 of 11 canine hemangiosarcomas (Janus 2016)",
        "outcome": "positive: 44% vs 14% one-year survival",
    },
    "er_stress_peptides": {
        "antigen": "POLYVALENT -- the secretome of canine hemangiosarcoma cells infected with "
                   "Salmonella typhi Ty21a, releasing ER-stress peptides through CX43 hemichannels",
        "coverage_evidence": "not applicable: the vaccine is derived from the tumour, so it covers "
                             "whatever the tumour expresses",
        "outcome": "positive: TTP 195 vs 160 days (p=0.001), OS 276 vs 175 days (p=0.002), "
                   "one-year 35.7% vs 6.3%, 28 vaccinated against 32 controls "
                   "(Cancers 2023, PMID 37686485)",
    },
    "autologous_dendritic_cell": {
        "antigen": "POLYVALENT -- autologous, tumour-derived",
        "coverage_evidence": "not applicable, same reason",
        "outcome": "positive: median survival 256 days with >=3 vaccines, 29% one-year, adjusted "
                   "hazard ratio 0.30; 452 dogs screened, 42 stage II entered "
                   "(Spiller et al. 2024, Vet J 306:106196, PMID 39004264)",
        "a_manufacturing_correlate_worth_noting": "the same study found that DENDRITIC CELL YIELD "
                                                  "at the start of treatment was significantly "
                                                  "related to survival. These are autologous "
                                                  "monocyte-derived cells, and Gulay 2022 shows "
                                                  "hemangiosarcoma polarises monocytes toward an "
                                                  "M2, PD-L1-positive state -- so poor yield may be "
                                                  "the same monocyte hijacking that route 2 targets "
                                                  "showing up in the manufacturing step. That is a "
                                                  "mechanistic hypothesis, not a demonstrated link.",
    },
    "vaccs": {
        "antigen": "DEFINED -- 31 shared RNA-error-derived neoantigens",
        "coverage_evidence": "never reported for hemangiosarcoma",
        "outcome": "negative for hemangiosarcoma, attributed by the investigators to antigen choice",
    },
    "the_pattern": "it is not defined-versus-polyvalent. eVim is defined and it worked -- because "
                   "its antigen happens to have near-total coverage in this tumour. VACCS is "
                   "defined and it failed on this tumour -- and its coverage here was never "
                   "established. The polyvalent vaccines sidestep the question entirely by taking "
                   "their antigens from the tumour itself. Coverage, not platform, is the variable "
                   "that sorts these four results.",
    "the_prediction_this_makes": "SOCH -- Calviri's therapeutic hemangiosarcoma trial, up to 80 "
                                 "dogs with stage 1-2 disease randomised against mock vaccine on "
                                 "top of surgery and chemotherapy -- uses defined RNA-error-derived "
                                 "neoantigens. On this account its result turns on whether the "
                                 "revised antigen set covers hemangiosarcoma cells, and it is a "
                                 "real test of the argument rather than a restatement of it.",
    "the_honest_status": "four results is not a dataset and the sorting is retrospective. This is a "
                         "hypothesis that happens to make a falsifiable prediction, not a finding.",
}


# =============================================================================================
# WHAT THE ENGINE SAYS -- AND IT IS NOT WHAT THE MODULE'S AUTHOR EXPECTED.
#
# Both modes run at the plan's own operating point: vaccine height 0.042/day, second drug withdrawn
# after one year. Same engine, same seed, 250 trials, six clones (the five as before plus an
# antigen-null compartment). At full coverage the two modes are identical, which is the check that
# the comparison is fair.
# =============================================================================================

DURABILITY_BY_COVERAGE = {
    #  coverage: (A uniform -- every cell dimmer, B heterogeneous -- some cells blind)
    1.00: (0.864, 0.864),
    0.95: (0.708, 0.864),
    0.90: (0.648, 0.864),
    0.80: (0.496, 0.864),
    0.60: (0.500, 0.860),
    0.40: (0.276, 0.848),
}

THE_RESULT_INVERTS_THE_EXPECTATION = {
    "what_was_expected": "that the heterogeneous blind spot would be far worse than uniform "
                         "dimming, because a pre-existing antigen-null population starts at high "
                         "frequency instead of having to be seeded at 1e-8/day.",
    "what_happened": "the opposite. Uniform dimming falls 0.864 -> 0.496 by 80% coverage. The blind "
                     "spot does not move at all: 0.864 down to 0.848 across the entire range, including at 40% coverage where uniform dimming has fallen to 0.276.",
    "why": "the antigen-null cells in this specification are DRUG-SENSITIVE, and the first drug -- "
           "the PI3K/mTOR inhibitor -- runs continuously for the whole ten years. It holds them "
           "whatever the vaccine can or cannot see. Uniform dimming, by contrast, weakens the "
           "vaccine everywhere INCLUDING on the drug-resistant clones, and covering those clones is "
           "the vaccine's entire job in this plan.",
    "the_reframing": "antigen coverage per se is not what matters. What matters is whether the "
                     "antigen covers the DRUG-RESISTANT cells. Coverage of drug-sensitive cells is "
                     "largely redundant with the drug that is already killing them.",
    "the_honest_caveat": "this is a consequence of a modelling choice -- that the antigen-null "
                         "fraction inherits the sensitive clone's drug response. That choice is "
                         "doing the work, and the case it excludes is the dangerous one: a blind "
                         "spot that overlaps drug resistance, covered by nothing.",
}

# The design rule that falls out, which is the useful part.
WHAT_TO_MEASURE_INSTEAD = {
    "the_wrong_experiment": "quantitative immunohistochemistry for antigen coverage across bulk "
                            "hemangiosarcoma tissue. It answers a question the model says is not "
                            "decisive.",
    "the_right_experiment": "measure antigen coverage IN THE DRUG-RESISTANT FRACTION -- cells "
                            "surviving PI3K/mTOR inhibition. If the antigen is retained on the "
                            "cells the drug cannot kill, incomplete coverage elsewhere is largely "
                            "absorbed. If it is lost on exactly those cells, the plan has no cover "
                            "at all.",
    "why_this_is_cheap": "it is the same stain on a treated versus untreated cell line or "
                         "tumorgraft, not a new trial. Andersen's canine angiosarcoma tumorgrafts "
                         "and the ISOS-1 syngeneic model both already exist for it.",
    "the_precedent_that_makes_it_plausible": "antigen retention under targeted-therapy pressure is "
                                             "not guaranteed in either direction -- drug-tolerant "
                                             "persister states are widely reported to shift surface "
                                             "phenotype. Assuming retention is exactly the kind of "
                                             "unexamined assumption this module was written to stop "
                                             "making.",
}


# =============================================================================================
# CLOSING THE ROUTE.
#
# Route 8 is closable, and unusually the closers do not require knowing the antigen -- which is the
# point, because the failure mode is not knowing the antigen. Four legs, ordered by how much of the
# evidence sits in dogs.
# =============================================================================================

CLOSURE_LEG_1_THE_DRUG_ABSORBS_IT = {
    "claim": "a blind spot among drug-sensitive cells is held by the first drug, which runs "
             "continuously regardless of the vaccine.",
    "evidence": "DURABILITY_BY_COVERAGE: heterogeneous coverage from 1.00 down to 0.60 leaves "
                "ten-year durability at 0.864-0.860, flat.",
    "the_condition_it_depends_on": "the blind spot must not overlap drug resistance, and the first "
                "drug must not be withdrawn. This analysis already requires the first drug "
                "continuously; it is the SECOND drug that becomes a one-year induction.",
    "status": "CLOSED for a purely drug-sensitive blind spot and WORTHLESS otherwise -- see "
              "OVERLAP_IS_THE_WHOLE_BALLGAME. Any resistant component takes durability to 0.000, "
              "and continuous dosing does not rescue it. This leg describes the benign case; it "
              "is not a defence against the dangerous one.",
}

CLOSURE_LEG_2_POLYVALENT_VACCINES_SIDESTEP_IT = {
    "claim": "a vaccine whose antigens come from the tumour itself cannot have a coverage gap "
             "against that tumour, because its antigen set is defined by what the tumour expresses.",
    "evidence_in_this_disease": "both polyvalent hemangiosarcoma vaccines were positive. The "
                                "ER-stress-peptide secretome vaccine gave TTP 195 vs 160 days "
                                "(p=0.001) and OS 276 vs 175 days (p=0.002) in 28 vaccinated "
                                "against 32 controls; autologous monocyte-derived dendritic cells "
                                "gave median survival 256 days with an adjusted hazard ratio of "
                                "0.30.",
    "the_cost": "polyvalent tumour-derived products are manufactured per dog from that dog's own "
                "tumour, which is exactly the logistics Calviri cites as 'impractical to build and "
                "prohibitively expensive for use in dogs'. Sidestepping the antigen problem "
                "reintroduces a manufacturing one.",
    "status": "CLOSED at the cost of per-dog manufacture -- an availability problem, not a biology "
              "problem.",
}

CLOSURE_LEG_3_EPITOPE_SPREADING_REPAIRS_COVERAGE = {
    "claim": "killing antigen-positive cells releases the tumour's other antigens, and the response "
             "broadens to targets the vaccine never contained. A coverage gap can close itself.",
    "clinical_evidence": "NEO-PV-01, a personalised neoantigen vaccine given with chemotherapy and "
                         "anti-PD-1 to 38 patients with non-squamous NSCLC: 'Epitope spread to "
                         "NON-VACCINATING neoantigens, including responses to KRAS G12C and G12V "
                         "mutations, were detected post-vaccination.' "
                         "(Awad et al. 2022, Cancer Cell 40(9):1010-1026, PMID 36027916)",
    "why_it_bears_on_route_8": "it is direct evidence that a DEFINED-antigen vaccine can end up "
                               "covering antigens it did not contain -- which is the failure mode "
                               "route 8 describes, repairing itself over time.",
    "the_limits": "human lung cancer, given alongside checkpoint blockade and chemotherapy, so the "
                  "spreading is not attributable to the vaccine alone; and spreading was detected, "
                  "not shown to be sufficient.",
    "status": "PARTIAL -- a real mechanism with clinical demonstration, no dose-response and "
              "nothing in this species or tumour.",
}

CLOSURE_LEG_4_FORCE_THE_SPREADING_WITHOUT_KNOWING_THE_ANTIGEN = {
    "claim": "epitope spreading can be induced deliberately, using RNA that codes for "
             "TUMOUR-UNSPECIFIC antigens -- so the intervention does not need to know the target "
             "at all.",
    "mechanism": "multi-lamellar RNA lipid particle aggregates (RNA-LPAs) given systemically "
                 "activate RIG-I in stromal cells rather than TLRs in immune cells, producing a "
                 "large cytokine and chemokine response with dendritic cell and lymphocyte "
                 "trafficking",
    "the_canine_evidence": "'In client-owned canines with terminal gliomas, RNA-LPAs improved "
                           "survivorship and reprogrammed the TME, which became \"hot\" within days "
                           "of a single infusion.' "
                           "(Mendez-Gomez et al. 2024, Cell 187(10):2521-2535, PMID 38697107)",
    "the_human_evidence": "a first-in-human glioblastoma trial showed rapid cytokine release, "
                          "immune trafficking, tissue-confirmed pseudoprogression and "
                          "glioma-specific immune responses",
    "the_epitope_spreading_link": "the companion study shows early type-I interferon responses "
                                  "mediate epitope spreading in poorly immunogenic tumours and that "
                                  "boosting them with tumour-unspecific RNA enables it "
                                  "(Qdaisat et al. 2025, Nat Biomed Eng 9(9):1437-1452, "
                                  "PMID 40681861)",
    "why_this_is_the_most_interesting_leg": "it attacks route 8 and routes 1-2 with one agent. The "
                                            "coverage gap is repaired by spreading, and the "
                                            "suppressive microenvironment this analysis spent three "
                                            "routes trying to lift is reprogrammed directly -- in "
                                            "dogs, systemically, after a single infusion.",
    "the_limits": "glioma, not hemangiosarcoma. Survivorship in terminal disease, not an adjuvant "
                  "setting. No coverage measurement, and nothing about how long the effect lasts, "
                  "which is the axis this analysis has repeatedly found to be the weak one.",
    "status": "PARTIAL -- the strongest antigen-agnostic candidate, with canine in-vivo data, in "
              "the wrong tumour.",
}

# NK cells were already in the regimen for route 4. How much do they help here?
THE_NK_COMPONENT_ONLY_PARTLY_TRANSFERS = {
    "the_tempting_argument": "NK cells are antigen-agnostic, so they should cover any cell the "
                             "vaccine cannot see, closing route 8 for free with a component the "
                             "regimen already contains.",
    "why_it_does_not_fully_work": "NK recognition here is MISSING-SELF: it is triggered by MHC-I "
                                  "downregulation. A cell that lost the antigen by losing antigen "
                                  "presentation is NK-visible. A cell that never displayed the "
                                  "vaccine's target while keeping normal MHC-I is not.",
    "what_it_does_cover": "route 4 -- antigen loss through MHC-I downregulation -- which is what it "
                          "was added for.",
    "what_it_does_not_cover": "route 8's heterogeneous mode, where the target was simply never "
                              "there and antigen presentation is intact.",
    "the_correction": "listing NK cells as a route 8 closer would be exactly the conflation this "
                      "module exists to undo.",
}

VERDICT = {
    "the_route": "8 -- antigen inadequacy on day zero, distinct from route 4's antigen loss.",
    "is_it_closable": "yes, and by more than one route, but not by the component that closes "
                      "route 4.",
    "the_free_closer_only_covers_the_benign_case": "the first drug absorbs a drug-SENSITIVE blind "
                                    "spot down to 40% coverage for nothing, because it runs "
                                    "continuously and does not care what the vaccine sees. The "
                                    "moment any of the blind spot is drug-resistant, durability "
                                    "is 0.000 at 95% coverage and continuous dosing does not "
                                    "change that.",
    "the_condition_that_decides_it": "whether the blind spot overlaps drug resistance -- and it is "
                                     "not a spectrum but a cliff between 0.84 and 0.00. One stain "
                                     "on treated versus untreated cells in models that already "
                                     "exist settles it, which makes it a GO/NO-GO gate that has "
                                     "to precede a trial rather than accompany one.",
    "the_only_answers_if_it_does_overlap": "polyvalent tumour-derived vaccines close it outright at the "
                                      "cost of per-dog manufacture; epitope spreading repairs "
                                      "coverage and has been demonstrated clinically; RNA-LPAs "
                                      "induce that spreading without needing to know the antigen "
                                      "and have improved survival in client-owned dogs.",
    "what_this_does_not_claim": "none of the four legs has been tested in canine hemangiosarcoma. "
                                "The route is closable on paper and on mechanism, in the same sense "
                                "and with the same caveats as every other route in this analysis.",
}


# =============================================================================================
# THE CASE THE FIRST RESULT EXCLUDED, RUN. IT IS NOT A DEGRADATION -- IT IS A CLIFF.
#
# The flat 0.864 above depended on the antigen-null fraction being drug-sensitive. Here the same
# grid is run with that fraction specified three ways: drug-sensitive, half-and-half, and carrying
# clone 1's resistance. Seven clones, same seed, 250 trials. At full coverage all three agree, which
# is again the fairness check.
# =============================================================================================

DURABILITY_BY_WHERE_THE_BLIND_SPOT_LANDS = {
    #  coverage: (null drug-sensitive, null mixed 50/50, null drug-resistant)
    1.00: (0.840, 0.840, 0.840),
    0.95: (0.840, 0.000, 0.000),
    0.90: (0.828, 0.000, 0.000),
    0.80: (0.836, 0.000, 0.000),
}

# And the obvious rescue -- never withdraw the second drug -- does not work either.
CONTINUOUS_DOSING_DOES_NOT_RESCUE_AN_OVERLAPPING_BLIND_SPOT = {
    0.95: {"stop_at_year_1": 0.000, "never_stop": 0.000},
    0.90: {"stop_at_year_1": 0.000, "never_stop": 0.000},
    0.80: {"stop_at_year_1": 0.000, "never_stop": 0.000},
}

OVERLAP_IS_THE_WHOLE_BALLGAME = {
    "the_finding": "a blind spot that overlaps drug resistance is not a worse outcome, it is a "
                   "total one. At 95% coverage -- five percent of the sensitive compartment both "
                   "antigen-null and drug-resistant -- ten-year durability is 0.000. Not 0.5, not "
                   "the correction-alone floor. Zero, in 250 of 250 trials.",
    "the_mixed_case_is_no_softer": "splitting the null fraction half drug-sensitive and half "
                                   "drug-resistant gives 0.000 as well. It takes only the resistant "
                                   "half to do it; the sensitive half being covered buys nothing.",
    "why_it_is_absolute": "such a cell is covered by nothing. The vaccine cannot see it, the first "
                          "drug cannot kill it, and the second drug's 0.0225/day does not close the "
                          "gap to its growth rate. Net growth stays positive, and positive net "
                          "growth over ten years is arithmetic, not chance.",
    "continuous_dosing_does_not_save_it": "withdrawing the second drug at year one and never "
                                          "withdrawing it give the same 0.000. This is the one place "
                                          "in the entire analysis where the toxicity trade-off is "
                                          "irrelevant, because neither arm works.",
    "what_this_does_to_leg_1": "the first closure leg -- 'the drug absorbs it' -- is not a general "
                               "result. It holds for a purely drug-sensitive blind spot and fails "
                               "completely the moment any part of the blind spot is resistant. It "
                               "is a description of the benign case, not a defence against the "
                               "dangerous one.",
    "what_this_does_to_the_measurement": "coverage in the drug-resistant fraction stops being the "
                                         "cheapest informative experiment and becomes a GO/NO-GO "
                                         "GATE. There is no version of this plan that survives an "
                                         "antigen-null resistant subpopulation at even five "
                                         "percent, so the measurement has to precede the trial "
                                         "rather than accompany it.",
    "what_this_does_to_legs_2_to_4": "polyvalent tumour-derived vaccines, epitope spreading and "
                                     "RNA-LPA-induced spreading stop being backups and become the "
                                     "only candidate answers, because they are the only ones that "
                                     "can put an antigen on a cell whose antigen was never there. "
                                     "None of them has been tested against a resistant "
                                     "subpopulation specifically.",
    "the_honest_reading": "route 8 is closed in the benign case and open in the dangerous one, and "
                          "nothing currently distinguishes which case canine hemangiosarcoma is. "
                          "Recording it as 'closed conditionally' without that emphasis would "
                          "understate it: the condition is not a caveat, it is the entire result.",
}
