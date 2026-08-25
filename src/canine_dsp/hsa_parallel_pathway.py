"""A two-node combination that clears the exposure criterion, unlike every candidate before it.

`hsa_growth_pharmacodynamics` established the rule: an agent qualifies only if the exposure a dog
actually reaches clears the concentration at which the agent does something. Propranolol misses by
~350x. Toceranib clears its own bar and fails on biology.

This module tests a third candidate, and it is the first to pass both halves: MEK inhibition
combined with a dual TORC1/2 inhibitor. The combination has been measured in canine angiosarcoma
cells, and both drugs have been dosed together in dogs with pharmacokinetics reported.

See docs/HSA_DURABLE_RESPONSE.md.
"""

import numpy as np
from dataclasses import replace

TRAMETINIB_MW_G_PER_MOL = 615.39
SAPANISERTIB_MW_G_PER_MOL = 309.33

# ---------------------------------------------------------------------------------------------
# Why the primary drug must hit mTORC2, and why rapamycin cannot.
#
# This is the mechanistic reason the FidoCure rapamycin signal is real but small, and the reason
# an ATP-competitive dual inhibitor is the right class rather than a modelling convenience.
CANINE_HSA_RUNS_ON_mTORC2 = {
    "citation": "Murai et al. 2012, BMC Vet Res 8:128, PMID 22839755, doi 10.1186/1746-6148-8-128",
    "finding": "in 6 of 7 newly derived canine HSA cell lines, phosphorylation of Akt Ser473, "
               "mTORC1 Ser2448 and 4E-BP1 Ser65 was high in serum-starved conditions and did not "
               "change on stimulation -- the mTORC2/Akt/4E-BP1 pathway is CONSTITUTIVELY active",
    "tumour_confirmation": "Murai et al. 2012, J Comp Pathol 147(4):430-40, PMID 22789858 -- in 37 "
                           "canine haemangiosarcomas, ~80% expressed p-Akt Ser473, p-Akt Thr308 and "
                           "p-4E-BP1, but only 35% expressed p-mTORC1 Ser2448",
    "authors_conclusion": "the mTORC2/Akt/4E-BP1 pathway, regulated independently of mTORC1, may be "
                          "important for targeting therapy in canine HSAs",
    "why_it_matters": "rapamycin and its analogues inhibit mTORC1. The pathway canine HSA actually "
                      "runs on is mTORC2, which rapalogs do not block. That predicts a rapalog will "
                      "underperform in this disease -- and it does.",
    "independent_confirmation": "Andersen et al. 2015 state flatly that 'angiosarcomas are "
                                "insensitive to mTOR inhibition', measured rather than inferred.",
}

# ---------------------------------------------------------------------------------------------
# The measured synergy, in the right species and the right tumour.
MEK_PLUS_mTOR_SYNERGY = {
    "citation": "Andersen et al. 2015, Int J Oncol 47(1):71-80, PMID 25955301, "
                "doi 10.3892/ijo.2015.2989",
    "system": "canine angiosarcoma cell isolate VCT261e, plus canine angiosarcoma tumorgrafts",
    "mek_inhibitor": "PD0325901",
    "ic50_nM": {"mek_alone": 150.0, "mek_alone_sd": 30.0,
                "rapamycin_alone": ">50 (insensitive)",
                "combined_4to1": 11.0, "combined_4to1_sd": 6.0},
    "potency_shift_fold": 150.0 / 11.0,
    "combination_index": 0.07,
    "combination_index_interpretation": "CI < 1 is synergy; 0.07 is strong synergy by "
                                        "Chou-Talalay. All reported CIs were <= 0.08.",
    "subnanomolar_note": "rapamycin showed strong synergy with the MEK inhibitor even at "
                         "subnanomolar concentrations",
    "in_vivo": "canine AS tumorgrafts: vehicle reached 1000 mm3 by day 21; the combination showed "
               "virtually no growth by week 3 and was significantly smaller than either monotherapy "
               "at day 38, with no weight loss over 38 days",
    "the_shape_of_it": "neither node works alone. Blocking one pathway makes the tumour depend on "
                       "the other, which is what makes the pair supra-additive rather than merely "
                       "additive -- the same shape as the vaccine/growth-cut interaction.",
}

# The MAPK arm alone does nothing, measured separately in canine HSA specifically.
MEK_ALONE_FAILS_IN_CANINE_HSA = {
    "citation": "Adachi et al. 2016, Can J Vet Res 80(3):209-16, PMID 27408334",
    "system": "canine splenic and hepatic HSA cell lines",
    "finding": "inhibitors of the MAPK pathway did not affect canine HSA cell viability; inhibitors "
               "of VEGFR2 and of the PI3K/Akt/mTOR pathway did reduce viability and induced "
               "apoptosis",
    "consistency": "agrees with Andersen: the MAPK node is not a monotherapy target in this "
                   "disease. It becomes one only once the parallel pathway is blocked.",
}

# ---------------------------------------------------------------------------------------------
# Both drugs have been given to dogs. This is what they reach.
TRAMETINIB_CANINE_EXPOSURE = {
    "citation": "Takada et al. 2024, Vet Comp Oncol 22(3):410-421, PMID 38889903, "
                "doi 10.1111/vco.12989",
    "design": "phase I 3+3 dose escalation, 18 dogs with cancer",
    "maximum_tolerated_dose": "0.5 mg/m2/day PO",
    "steady_state_ng_per_ml": 10.0,
    "fraction_of_dogs_reaching_it": 0.70,
    "time_to_steady_state_days": 14,
    "human_threshold_note": "the authors identify 10 ng/mL as the concentration associated with "
                            "clinical efficacy in humans",
    "dose_limiting_toxicities": "systemic hypertension, proteinuria, lethargy and elevated ALP, all "
                                "Grade 3",
    "verdict": "trametinib was considered safe in dogs with cancer; 0.5 mg/m2/day recommended for "
               "phase II",
    "the_honest_gap": "target engagement was NOT observed in tumour biospecimens collected on days "
                      "0 and 7. Exposure is documented; pharmacodynamic confirmation is not. That "
                      "is weaker than toceranib, where a rising plasma VEGF confirmed engagement.",
}

COMBINATION_HAS_BEEN_DOSED_IN_DOGS = {
    "citation": "Wei et al. 2022, Front Vet Sci 9:1056408, PMID 36590793, "
                "doi 10.3389/fvets.2022.1056408",
    "design": "12 dogs, sapanisertib (dual TORC1/2) with trametinib, single dose and 17-day repeat",
    "tolerability": "the combination was tolerated without dose limiting toxicity",
    "adverse_effects": "body weight loss, maldigestion and cutaneous discoloration; laboratory "
                       "changes were drug-induced acute-phase inflammation, proteinuria and reduced "
                       "reticulocytes -- described as mild changes not necessitating intervention",
    "sapanisertib_cmax_ng_per_ml": 26.3,
    "sapanisertib_note": "resembled levels in human therapeutic trials",
    "drug_drug_interaction": "sapanisertib exposure fell when combined, trametinib being a CYP3A4 "
                             "inducer; trametinib accumulated 3-4x on daily dosing",
    "efficacy_precedent": "Wei et al. 2020, Mol Cancer Ther 19(11):2308-2318, PMID 32943547 -- the "
                          "same pair synergistically reduced survival of canine mucosal melanoma "
                          "lines and suppressed pathway reciprocal crosstalk in vivo",
    "why_it_matters": "this is not a proposed combination. It has been given to dogs together, the "
                      "pharmacokinetics are published, and it was tolerated.",
}


def ng_per_ml_to_nM(ng_per_ml: float, mw_g_per_mol: float) -> float:
    """ng/mL -> nM. 1 ng/mL = 1 ug/L; nM = (ug/L) / (g/mol) * 1000."""
    if ng_per_ml < 0 or mw_g_per_mol <= 0:
        raise ValueError("concentration must be nonnegative and molecular weight positive")
    return float(1000.0 * ng_per_ml / mw_g_per_mol)


TRAMETINIB_STEADY_STATE_nM = ng_per_ml_to_nM(
    TRAMETINIB_CANINE_EXPOSURE["steady_state_ng_per_ml"], TRAMETINIB_MW_G_PER_MOL)
SAPANISERTIB_CMAX_nM = ng_per_ml_to_nM(
    COMBINATION_HAS_BEEN_DOSED_IN_DOGS["sapanisertib_cmax_ng_per_ml"], SAPANISERTIB_MW_G_PER_MOL)

# The exposure criterion, applied to this candidate. This is the first agent in the analysis to
# pass it -- and it passes only as a combination, which is the point.
EXPOSURE_CRITERION = {
    "achieved_trametinib_nM": TRAMETINIB_STEADY_STATE_nM,
    "needed_as_monotherapy_nM": MEK_PLUS_mTOR_SYNERGY["ic50_nM"]["mek_alone"],
    "needed_in_combination_nM": MEK_PLUS_mTOR_SYNERGY["ic50_nM"]["combined_4to1"],
    "monotherapy_fold_short": MEK_PLUS_mTOR_SYNERGY["ic50_nM"]["mek_alone"]
                              / TRAMETINIB_STEADY_STATE_nM,
    "combination_fold_margin": TRAMETINIB_STEADY_STATE_nM
                               / MEK_PLUS_mTOR_SYNERGY["ic50_nM"]["combined_4to1"],
    "reading": "at the tolerated canine dose trametinib reaches about 16 nM. MEK inhibition alone "
               "needs about 150 nM in canine angiosarcoma cells, so monotherapy is roughly 9x "
               "short -- which is exactly what Adachi measured when MAPK inhibitors did nothing. "
               "In combination the requirement falls to about 11 nM, and 16 nM clears it with "
               "roughly 1.5x to spare.",
    "why_this_is_the_first_pass": "propranolol fails the criterion by ~350x. Toceranib passes on "
                                  "exposure and fails on biology. This pair passes on exposure AND "
                                  "has measured anti-tumour activity in canine angiosarcoma "
                                  "tumorgrafts.",
    "the_substitution_caveat": "Andersen measured PD0325901; Takada dosed trametinib. Both inhibit "
                               "MEK1/2 and trametinib is generally the more potent, so carrying the "
                               "150/11 nM requirement across is directionally conservative but not "
                               "rigorous. The number that would settle it -- trametinib's own "
                               "combination IC50 in canine HSA cells -- has not been measured.",
}


def with_mek_inhibitor(model, per_clone_max_kill: np.ndarray, ic50_nM_2: float | np.ndarray):
    """Attach a MEK inhibitor as the engine's second drug, with per-clone efficacy.

    Per-clone rather than scalar because MEK inhibition is NOT mechanism-agnostic: it acts at a
    specific node, so it must be strongest against the clone that escapes through that node
    (`mapk_crosstalk_bypass`) and weaker against clones escaping elsewhere.
    """
    per_clone_max_kill = np.asarray(per_clone_max_kill, dtype=float)
    if per_clone_max_kill.shape != model.growth.shape:
        raise ValueError("per_clone_max_kill must have one entry per clone")
    if np.any(per_clone_max_kill < 0):
        raise ValueError("per_clone_max_kill must be nonnegative")
    return replace(model, ic50_nM_2=ic50_nM_2, max_kill_2=per_clone_max_kill)


# Relative MEK-inhibitor efficacy by clone. The MAPK-bypass clone escapes through the very node the
# drug blocks, so it is the most exposed; the sensitive clone is already being killed by the primary
# drug. Values are RELATIVE weights, scaled by a swept ceiling below -- the absolute per-clone kill
# a MEK inhibitor achieves against these subclones has never been measured.
MEK_RELATIVE_EFFICACY_BY_CLONE = {
    "sensitive": 1.0,
    "pi3k_akt_feedback_reactivation": 1.0,
    "mapk_crosstalk_bypass": 1.0,
    "target_site_mutation": 1.0,
    "immune_escape": 1.0,
    "rationale": "held flat deliberately. Wei et al. 2020 report that the pair suppresses pathway "
                 "RECIPROCAL crosstalk, so MEK inhibition is not a private answer to the MAPK clone "
                 "alone -- it withdraws the alternative route every clone would otherwise fall back "
                 "on. Weighting it towards the MAPK clone would flatter the result by assuming the "
                 "mechanism-specificity the crosstalk data argues against.",
}

# Bar under measured cross-resistance ratios, before any second drug (hsa_gap_stack).
BAR_BEFORE_SECOND_DRUG = 0.0445
BAR_SET_BY = "pi3k_akt_feedback_reactivation, capped by max_kill 0.02/day"
VACCINE_REAL = 0.03

# Second-drug kill needed to bring the bar under the real vaccine's 0.03/day. Recomputed in tests.
# At the achievable trametinib exposure (16.2 nM against an 11 nM combination IC50) the Emax term
# is about 0.64, so the requirement is higher than it would be at a saturating dose. Both are
# recorded because the difference is the whole reason exposure is tracked separately from potency.
MEK_KILL_NEEDED_PER_DAY = 0.0225
MEK_KILL_NEEDED_AT_SATURATING_EXPOSURE = 0.0145

VERDICT = {
    "candidate": "dual TORC1/2 inhibitor (sapanisertib) + MEK inhibitor (trametinib), on top of the "
                 "vaccine and its q60d boosters",
    "passes_the_exposure_criterion": True,
    "mechanism_coverage": {
        "pi3k_akt_feedback_reactivation": "the dual TORC1/2 inhibitor blocks the arm the feedback "
                                          "reactivates. This is the class's design purpose, not a "
                                          "hopeful reading -- and it is the clone that sets the bar.",
        "mapk_crosstalk_bypass": "MEK inhibition acts directly on the bypass node.",
        "target_site_mutation": "an FRB/FKBP12-site mutation is invisible to an ATP-competitive "
                                "inhibitor (Rodrik-Outmezguine 2016, measured).",
        "kinase_domain_mutation": "NOT covered. Measured at 3-30x against ATP-competitive drugs, "
                                  "and the one mechanism this pair does not answer. Third-generation "
                                  "bivalent inhibitors (RapaLink-1) exist precisely for it, with no "
                                  "canine data at all.",
        "immune_escape": "not a drug-resistance route; handled by the vaccine and the open-route "
                         "analysis, not here.",
    },
    "what_is_measured": "the synergy (CI 0.07), the combination IC50 in canine angiosarcoma cells "
                        "(11 nM), tumorgraft efficacy, canine exposure for both drugs, and "
                        "tolerability of the pair in 12 dogs.",
    "what_is_not_measured": "per-clone kill rates for either drug against these specific resistance "
                            "mechanisms; trametinib's own combination IC50 in canine HSA; and "
                            "target engagement in canine tumours, which Takada looked for and did "
                            "not find.",
    "honest_status": "this is the strongest candidate the analysis has produced and the first to "
                     "clear the exposure criterion, but it is a well-supported hypothesis rather "
                     "than a demonstrated closure. The claim is that a defensible combination "
                     "EXISTS and is deliverable, not that durability has been proven.",
}
