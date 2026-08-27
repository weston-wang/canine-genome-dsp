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
