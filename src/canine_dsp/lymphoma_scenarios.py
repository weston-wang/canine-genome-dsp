"""Illustrative scenario presets for a chemoresistance model of canine multicentric lymphoma.

Canine multicentric lymphoma is the most common haematopoietic malignancy in dogs. Unlike the
solid tumours the rest of this project models (histiocytic sarcoma, hemangiosarcoma, osteosarcoma),
it is a *systemic* disease from the start: there is no primary mass to resect, and the standard of
care is multi-agent chemotherapy -- the CHOP protocol (cyclophosphamide, doxorubicin, vincristine,
prednisone). CHOP puts almost every dog into complete remission, and almost every dog relapses. The
question this module asks is the same one the histiocytic-sarcoma and hemangiosarcoma pipelines
asked: what carries a *lasting* remission, what per-day growth rate ("the bar") must be out-killed
to prevent relapse, how the disease escapes, and what closes each escape route -- with the explicit
target of cure or 10-year durability. See docs/LYMPHOMA_DURABLE_RESPONSE.md.

What is real here, and better grounded than in the HSA module, is the *resistance biology*: the
dominant relapse mechanism in canine lymphoma -- P-glycoprotein (ABCB1/MDR1) drug efflux -- is a
measured, published finding in the actual disease, not an extrapolation from human oncology. What
remains illustrative and swept, exactly as in every other module here, is every growth rate, kill
ceiling, and IC50 ratio: none is fitted to a canine-lymphoma measurement, and no combination
described here has been given to a dog on the strength of this model.

All PMIDs/DOIs below were verified against PubMed while this module was written.
"""

import numpy as np

from .mapk_resistance import ResistanceModel

# Four clones tracked by the chemoresistance model: drug-sensitive plus three resistance mechanisms.
# All three resistance mechanisms are real, published findings in canine lymphoma (see
# LYMPHOMA_RESISTANCE_EVIDENCE) -- unlike the HSA module's three speculative mTORC1-resistance
# mechanisms, these are measured in the disease. The illustrative part is their growth/kill numbers.
LYMPHOMA_CLONE_NAMES = ["sensitive", "mdr1_pgp_efflux", "abcg2_bcrp_efflux", "tp53_apoptosis_evasion"]

# Per-day intrinsic growth rates; illustrative, not fitted. Higher than the HSA presets because
# high-grade lymphoma regrows fast -- a resistant-clone doubling time of ln(2)/0.09 ~ 7.7 days is
# in the realistic range for relapsed high-grade disease, but the specific values are placeholders.
_SHARED_GROWTH = np.array([.100, .092, .090, .088])   # sensitive, mdr1, abcg2, tp53

# Per-day kill-rate ceilings under CHOP. The sensitive clone is killed hard (deep remission in
# ~90%+ of dogs); the two efflux clones retain a small ceiling; the apoptosis-evasion clone has an
# almost-zero ceiling because it fails to die even when the drug is present at saturating exposure.
_SHARED_MAX_KILL = np.array([.28, .04, .04, .012])

# IC50 ratios relative to the sensitive clone. The efflux clones need ~40x the drug concentration
# for the same effect, because P-gp/BCRP pump doxorubicin and vincristine back out (a shift in
# effective potency, the correct representation of an efflux pump). The apoptosis-evasion clone lets
# the drug in normally (ratio ~1) but cannot be killed by it -- so its resistance lives in max_kill,
# not IC50, exactly as target-site resistance did for the HSA module but through a different node.
_SHARED_IC50_RATIOS = np.array([1.0, 40.0, 40.0, 1.1])
_SHARED_MUTATION = np.eye(4)  # acquired resistance is scheduled stochastically, not via this matrix

# Illustrative seeding rates and pre-existing-resistance probability, swept rather than asserted for
# the same reason every other module here sweeps them: no canine-lymphoma study measures the
# probability that a resistant subclone is present at diagnosis. P-gp efflux is weighted highest
# because it is the most frequently observed acquired mechanism at relapse.
_SEEDING_RATE_TOTAL = 0.012
_PREEXISTING_PROB_SWEEP = [0.05, 0.15, 0.30, 0.50, 0.70]
_PREEXISTING_PROB_CENTRAL = 0.80  # near-universal relapse is the real observation; the central case
                                  # is deliberately pessimistic, matching that CHOP is not curative
                                  # (chemo-only durable response lands ~0.18, in the range of the
                                  # real 15-week CHOP median PFS of 176 days, LYMPHOMA_CHOP_BENCHMARK)

# --- Real standard-of-care benchmark: CHOP. Verified against PubMed. -----------------------------
LYMPHOMA_CHOP_BENCHMARK = {
    "citation": "Curran & Thamm 2015, Vet Comp Oncol 14 Suppl 1:147-55, PMID 26279153, "
                "DOI 10.1111/vco.12163",
    "design": "134 client-owned dogs, naive multicentric lymphoma, 15-week maintenance-free CHOP",
    "overall_response_rate": 0.98,
    "complete_responders": 104,
    "median_progression_free_survival_days": 176,
    "median_disease_specific_survival_days": 311,
    "prognostic_factors": "substage, immunophenotype (B vs T), CR as best response, among others",
    "interpretation": "CHOP is extremely good at inducing remission (98% respond) and does not "
                      "prevent relapse: median progression-free survival is under six months. "
                      "Response is not durability.",
    "immunophenotype_note": "Mutz et al. 2013, Vet Comp Oncol 13(4):337-47, PMID 23786518 -- on "
                            "multivariate analysis immunophenotype was the factor that stayed "
                            "significant for progression-free survival; T-cell does worse than "
                            "B-cell.",
    "early_relapse_note": "Parker et al. 2024, J Vet Intern Med 38(4):2282-2292, PMID 38961691, "
                          "DOI 10.1111/jvim.17139 -- dogs that progress during or soon after CHOP "
                          "respond poorly to rescue: short first remission predicts short "
                          "everything after. Resistance, once it shows, tends to be broad.",
}

# --- Real resistance biology. This is the module's strongest real grounding. ----------------------
LYMPHOMA_RESISTANCE_EVIDENCE = {
    "mdr1_pgp_efflux": {
        "gene": "ABCB1 (P-glycoprotein / MDR1)",
        "in_vitro": "Zandvliet et al. 2014, Toxicol In Vitro 28(8):1498-506, PMID 24975508, "
                    "DOI 10.1016/j.tiv.2014.06.004 -- a canine lymphoid line selected on "
                    "doxorubicin became resistant to doxorubicin AND vincristine but NOT "
                    "prednisolone, with high P-gp expression; resistance was fully reversed by the "
                    "P-gp inhibitor PSC833.",
        "why_it_sets_the_bar": "It is the most frequently observed acquired mechanism at relapse "
                               "and it covers the two most active CHOP cytotoxics at once.",
        "the_prednisolone_gap": "P-gp does NOT efflux prednisolone -- a real, measured drug-"
                                "specificity that means a pure P-gp clone stays glucocorticoid-"
                                "sensitive. Modelled in LYMPHOMA_RESISTANCE_EVIDENCE, discussed in "
                                "the open-route module, not silently ignored.",
    },
    "abcg2_bcrp_efflux": {
        "gene": "ABCG2 (BCRP)",
        "longitudinal": "Zandvliet et al. 2014, Vet J 205(2):263-71, PMID 25475167, "
                        "DOI 10.1016/j.tvjl.2014.11.002 -- in 63 dogs on doxorubicin-based "
                        "chemotherapy, drug resistance occurred in 35/63 (55.6%) and was "
                        "associated with increased ABCB1 (B-cell) and ABCG2 (T-cell) expression; "
                        "glucocorticoids did not change ABC-transporter expression.",
    },
    "tp53_apoptosis_evasion": {
        "gene": "TP53 / intrinsic apoptosis machinery",
        "rationale": "A clone that fails to execute drug-induced apoptosis is unkillable by any "
                     "cytotoxic regardless of how much drug reaches it -- the ceiling, not the "
                     "dose, is what binds. Modelled as a near-zero kill ceiling at normal drug "
                     "entry. Illustrative: TP53 status is not routinely genotyped in these dogs.",
    },
    "summary": "Two of the three modelled resistance clones are measured mechanisms in canine "
               "lymphoma (P-gp/ABCB1 and BCRP/ABCG2 efflux); the third (apoptosis evasion) is a "
               "generic cytotoxic-resistance category. This is firmer disease-specific grounding "
               "than the HSA module had for its resistance mechanisms.",
}


def dog_lymphoma_preset(immunophenotype: str = "B"
                        ) -> tuple[ResistanceModel, float, np.ndarray, dict]:
    """CHOP vs. canine multicentric lymphoma. `immunophenotype='B'` (default) or 'T'.

    T-cell lymphoma is modelled with modestly faster growth and higher resistance seeding, matching
    its consistently worse real prognosis (Curran & Thamm 2015; Mutz et al. 2013; Saba et al.
    2020) -- the direction is real, the magnitude of the bump is illustrative.
    """
    if immunophenotype not in ("B", "T"):
        raise ValueError("immunophenotype must be 'B' or 'T'")
    growth = _SHARED_GROWTH.copy()
    seeding_scale = 1.0
    if immunophenotype == "T":
        growth = growth * 1.06         # illustrative: T-cell regrows faster and relapses sooner
        seeding_scale = 1.5            # illustrative: more/earlier resistance

    # Nominal doxorubicin-equivalent reference potency. Illustrative: unlike the HSA module, which
    # anchored its sensitive-clone IC50 to a real cell-line measurement (VDC-597), no numeric canine-
    # lymphoma doxorubicin IC50 is asserted here. What is real is the *mechanism* (P-gp efflux
    # raising effective IC50 ~40x, reversible with PSC833), not this baseline number.
    ic50_sensitive = 100.0
    seeding_rates = _SEEDING_RATE_TOTAL * seeding_scale * np.array([.5, .3, .2])
    model = ResistanceModel(growth=growth, ic50_nM=ic50_sensitive * _SHARED_IC50_RATIOS,
                            max_kill=_SHARED_MAX_KILL, mutation=_SHARED_MUTATION)
    css_reference = 5.0 * ic50_sensitive  # illustrative 5x-IC50 CHOP exposure margin, as in HSA
    provenance = {
        "species": "dog", "disease": f"multicentric lymphoma ({immunophenotype}-cell)",
        "regimen": "CHOP (cyclophosphamide, doxorubicin, vincristine, prednisone)",
        "real_grounding": LYMPHOMA_RESISTANCE_EVIDENCE,
        "standard_of_care_benchmark": LYMPHOMA_CHOP_BENCHMARK,
        "illustrative_only": ["growth rates", "kill ceilings", "IC50 ratios", "css_reference",
                              "seeding rates", "carrying capacity",
                              "the T-cell growth/seeding bump (direction real, magnitude not)"],
        "not_a_treatment_recommendation": True,
    }
    return model, css_reference, seeding_rates, provenance


# --- Rabacfosadine (Tanovea): a real, distinct cytotoxic with a different mechanism than CHOP. ----
# Included as a real second cytotoxic option, the way eBAT is for HSA. It is NOT a durability
# mechanism (it is duration-capped and drug-resistance-prone like CHOP), but it is real and its kill
# is modelled as a mechanism-agnostic second node with a swept, illustrative potency.
LYMPHOMA_RABACFOSADINE_BENCHMARK = {
    "citation": "Saba et al. 2020, Vet Comp Oncol 18(4):763-769, PMID 32346934, "
                "DOI 10.1111/vco.12605",
    "design": "63 dogs, previously untreated intermediate/large-cell lymphoma, single-agent RAB q21d",
    "overall_response_rate": 0.87, "complete_response_rate": 0.52,
    "median_progression_free_interval_days": 122,
    "worse_subgroups": "T-cell immunophenotype and corticosteroid pre-treatment predicted inferior "
                       "outcome on multivariate analysis",
    "alternating_with_doxorubicin": "Thamm et al. 2017, J Vet Intern Med 31(3):872-878, "
                                    "PMID 28370378, DOI 10.1111/jvim.14700 -- alternating RAB/DOX "
                                    "in 54 naive dogs: ORR 84%, median PFI 194 days, fewer visits "
                                    "than full CHOP.",
    "caveat": "Real and active, but relapse remains the rule -- another way to induce remission, "
              "not a demonstrated route to durability. A serious, real toxicity signal (delayed "
              "grade-5 pulmonary fibrosis in a small number of dogs) is reported in both trials.",
}
LYMPHOMA_RAB_ILLUSTRATIVE_IC50_NM = 100.0
LYMPHOMA_RAB_ILLUSTRATIVE_CSS_NM = 500.0  # ~5x the illustrative IC50; assumed, not measured
LYMPHOMA_RAB_MAX_KILL_SWEEP = [0.0, 0.02, 0.05, 0.08, 0.12]
LYMPHOMA_RAB_EXPOSURE_DURATION_DAYS = 105  # ~5 cycles q21d; RAB is not given indefinitely


# --- The immunotherapy analog: anti-CD20 CAR-T / mAb. This is the durability candidate. ----------
# CD20-directed cellular/antibody immunity covers every chemoresistance clone at once, because CD20
# expression is independent of drug efflux or apoptosis machinery -- the same "resistance to a drug
# does not change what the immune system sees" argument the HSA and HS vaccine work made. Its own
# escape route -- CD20 antigen loss -- is real and documented in canine DLBCL treated with CD20
# CAR-T, and is modelled as the 5th clone (see lymphoma_immunotherapy_followon_scenarios).
LYMPHOMA_IMMUNOTHERAPY_TRIALS = {
    "cd20_car_t_in_vitro": {
        "citation": "Sakai, Igase, Mizuno 2020, Vet Comp Oncol 18(4):739-752, PMID 32329214, "
                    "DOI 10.1111/vco.12602",
        "finding": "Canine CD20 CAR-T cells killed CD20-expressing canine B-cell lymphoma cells "
                   "and had NO effect on cells lacking canine CD20 -- antigen-specific by "
                   "construction, which is exactly why CD20 loss is its escape route.",
        "strength": "in vitro only; establishes mechanism and antigen-dependence, not efficacy.",
    },
    "cd20_loss_and_tandem_car": {
        "citation": "Peng et al. (Mason/Atherton lab) 2026, Mol Cancer Ther, PMID 42480604, "
                    "DOI 10.1158/1535-7163.MCT-26-0365",
        "antigen_escape": "This group previously observed CD20 loss in canine DLBCL patients "
                          "treated with CD20-specific CAR-T -- real antigen escape in real dogs, "
                          "mirroring CD19/CD20-negative relapse in humans after CAR-T.",
        "closure": "They built a tandem CD19/CD20 CAR that eliminates cells expressing CD19 "
                   "and/or CD20; canine B-cell lymphoma co-expresses both with heterogeneous "
                   "patterns like the human disease. Two independent antigens on one construct -- "
                   "the direct analog of the HSA dual-vaccine route, but with real canine data.",
        "strength": "the load-bearing real result behind this module's antigen-loss closure.",
    },
}
LYMPHOMA_IMMUNOTHERAPY_CLONE_NAMES = LYMPHOMA_CLONE_NAMES + ["cd20_antigen_loss"]
LYMPHOMA_IMMUNOTHERAPY_START_DAY = 30   # illustrative: immune effector introduced after CHOP induction
LYMPHOMA_IMMUNOTHERAPY_RAMP_DAYS = 14   # T-cell expansion timescale; illustrative
LYMPHOMA_IMMUNOTHERAPY_MAX_KILL_SWEEP = [0.0, 0.03, 0.06, 0.09, 0.12]

# Fitness cost and seeding of CD20 antigen loss. CD20 (MS4A1) is a real, if not fully essential,
# B-cell surface molecule; loss is survivable but not free. Same conventions as the HSA module's
# immune-escape penalty/seeding.
LYMPHOMA_CD20_LOSS_GROWTH_PENALTY = 0.90
LYMPHOMA_CD20_LOSS_SEEDING_RATE = _SEEDING_RATE_TOTAL * 0.2 * 0.1


# --- The CNS sanctuary: the model upgrade. -------------------------------------------------------
# The central nervous system is a pharmacologic sanctuary: the blood-brain barrier excludes most
# CHOP cytotoxics (doxorubicin in particular penetrates the CNS very poorly), so a clone that has
# seeded the CNS sees only a fraction of the systemic drug concentration. This is the lymphoma
# analog of the HSA "second compartment," and it is why run_monte_carlo_two_compartment gained a
# sanctuary_penetration_multiplier: the sanctuary compartment's drug exposure is discounted while a
# systemic cellular immune effector (CAR-T) still traffics there. The multiplier value is
# illustrative and swept; no drug-specific canine CNS penetration fraction is asserted.
LYMPHOMA_CNS_SANCTUARY = {
    "site": "central nervous system (behind the blood-brain barrier)",
    "why_it_is_a_sanctuary": "CHOP cytotoxics, doxorubicin especially, penetrate the CNS poorly, "
                             "so CNS disease sees a small fraction of systemic drug exposure.",
    "involvement_note": "CNS involvement in canine multicentric lymphoma is uncommon at diagnosis "
                        "but is a recognised site of relapse; the involvement probability is swept, "
                        "not asserted.",
    "penetration_multiplier_sweep": [1.0, 0.3, 0.15, 0.05],
    "the_asymmetry": "The drug is excluded; a systemic CAR-T effector is not (cellular immunity "
                     "traffics on its own). That asymmetry is the argument for immunotherapy over "
                     "chemotherapy intensification for sanctuary disease, and it is why the "
                     "sanctuary is modelled as a separate compartment rather than as lower overall "
                     "drug exposure.",
}
LYMPHOMA_CNS_INVOLVEMENT_PROB_SWEEP = [0.0, 0.15, 0.30]
LYMPHOMA_CNS_SEED_FRACTION = 0.05  # illustrative fraction of pre-treatment burden seeding the CNS


# --- Minimal residual disease (MRD): the early-detection lever. ----------------------------------
# The lymphoma analog of HSA's liquid-biopsy screening. MRD monitoring by flow cytometry and PARR
# (PCR for antigen-receptor rearrangements), and RT-qPCR to ~1 cell in 10,000, detects relapse
# before it is clinically apparent -- letting re-treatment start while burden is low, which the
# engine represents as a lower effective initial burden at the point of intervention.
LYMPHOMA_MRD_EVIDENCE = {
    "flow_vs_parr": "Aresu et al. 2014, Vet J 200(2):318-24, PMID 24698669, "
                    "DOI 10.1016/j.tvjl.2014.03.006 -- in canine DLBCL, PARR was more sensitive "
                    "than flow cytometry at predicting time to relapse; flow missed MRD in 7 dogs "
                    "that relapsed. Combining the two was best.",
    "rt_qpcr_sensitivity": "Sato et al. 2016, Vet J 215:38-42, PMID 27339366, "
                           "DOI 10.1016/j.tvjl.2016.05.012 -- allele-specific RT-qPCR reaches ~1 "
                           "malignant cell in 10,000 and works as a predictor of relapse and an "
                           "objective marker of treatment efficacy.",
    "why_it_closes_the_route": "Relapse detected at MRD level is relapse re-treated at low burden. "
                               "Like liquid-biopsy screening for HSA, it changes when intervention "
                               "happens, not the biology of the clone.",
    "limits": "MRD tells you a clone is coming back, not which mechanism -- and re-treating a P-gp "
              "clone with the same effluxed drugs still fails. MRD guides timing; it does not by "
              "itself supply a mechanism that clears the bar.",
}


# --- The curative lever: hematopoietic cell transplant. This is the real 10-year-durability anchor.
# Autologous peripheral-blood hematopoietic cell transplant (autoPBHCT) with total body irradiation
# (TBI) is the one real canine-lymphoma therapy with documented long-term cures. It is the closest
# real analog to "what lasting control actually requires": a high-intensity, mechanism-agnostic
# consolidation (TBI kills regardless of efflux or apoptosis status) plus immune reconstitution.
LYMPHOMA_TRANSPLANT_BENCHMARK = {
    "b_cell": {
        "citation": "Willcox, Pruitt, Suter 2012, J Vet Intern Med 26(5):1155-63, PMID 22882500, "
                    "DOI 10.1111/j.1939-1676.2012.00980.x",
        "design": "24 dogs, B-cell lymphoma, autoPBHCT after 10 Gy total body irradiation",
        "engraftment": "21/24 (87.5%)", "in_hospital_mortality": "2/24 (8.3%)",
        "median_disease_free_interval_days": 271, "median_overall_survival_days": 463,
        "durable_signal": "5/15 (33%) dogs transplanted before relapse remained in remission at a "
                          "median OS of 524 days (range 361-665) -- a real long-remission fraction, "
                          "not just a median shift.",
    },
    "t_cell": {
        "citation": "Warry, Willcox, Suter 2014, J Vet Intern Med 28(2):529-37, PMID 24467413, "
                    "DOI 10.1111/jvim.12302",
        "design": "15 dogs, T-cell lymphoma, autoPBHCT after TBI",
        "engraftment": "13/15 (87%)", "in_hospital_mortality": "2/15 (13%)",
        "median_disease_free_interval_days": 184, "median_overall_survival_days": 240,
        "long_term": "2/13 alive at 741 and 772 days.",
    },
    "cure_fraction": {
        "citation": "Gareau, Ripoll, Suter 2021, Front Vet Sci 8:787373, PMID 34950726, "
                    "DOI 10.3389/fvets.2021.787373",
        "design": "10 dogs, high-grade B-cell lymphoma, CHOP + autoPBHSCT + adoptive T-cell therapy",
        "cured": "4/10 (40%) disease-free for >= 2 years post-transplant (their explicit cure "
                 "definition); ~70% of transplanted dogs otherwise relapse from residual disease.",
        "why_it_matters": "A real, documented cure fraction in canine lymphoma -- the empirical "
                          "anchor for what '10-year durability or cure' actually costs, and the "
                          "reason the engine's high-intensity-consolidation arm is calibrated to "
                          "land near, not far above, 40%.",
    },
    "cost": {
        "citation": "Benedict, Suter, Meritet 2024, Vet Pathol 61(5):765-770, PMID 38695516, "
                    "DOI 10.1177/03009858241249114",
        "finding": "Across 94 dogs transplanted over 10 years at one centre, 7% died before "
                   "discharge; post-mortems found systemic fungal and bacterial infection on a "
                   "background of marrow depletion -- the real, non-trivial treatment-related "
                   "mortality and morbidity of TBI + transplant.",
    },
    "modelled_as": "A high-intensity, mechanism-agnostic, DURATION-CAPPED consolidation kill "
                   "(TBI reaches every clone but is given once, not chronically) layered on top of "
                   "CHOP + immunotherapy -- see lymphoma_gap_closure. Treatment-related mortality "
                   "is applied as an independent competing hazard, the way rupture was for HSA.",
}
# Illustrative TBI consolidation: a strong kill applied to every clone for a short window, then off.
LYMPHOMA_TBI_MAX_KILL_SWEEP = [0.0, 0.10, 0.20, 0.35]
LYMPHOMA_TBI_ILLUSTRATIVE_IC50_NM = 100.0
LYMPHOMA_TBI_ILLUSTRATIVE_CSS_NM = 500.0
LYMPHOMA_TBI_EXPOSURE_DURATION_DAYS = 14  # a single conditioning window, not chronic dosing
LYMPHOMA_TRANSPLANT_TRM_ANNUAL_HAZARD_SWEEP = [0.0, 0.07, 0.13]  # from the real in-hospital figures

# Horizon sweep: 1, 2, 5, 10 years. The 10-year point is where "cure or durable" is actually tested.
LYMPHOMA_DURABILITY_HORIZON_SWEEP = [365, 730, 1825, 3650]


def lymphoma_combination_scenarios(rab_max_kill_values: list[float] = LYMPHOMA_RAB_MAX_KILL_SWEEP,
                                   immunophenotype: str = "B",
                                   ) -> dict[float, tuple[ResistanceModel, float, np.ndarray, dict]]:
    """CHOP (`dog_lymphoma_preset`) +/- a swept-potency, mechanism-agnostic rabacfosadine node,
    mirroring `hsa_scenarios.hsa_combination_scenarios`. RAB is modelled as a second cytotoxic that
    (unlike CD20 immunotherapy) does not escape antigen loss but does share drug-resistance-style
    limits and a capped duration.
    """
    model, css, seeding_rates, provenance = dog_lymphoma_preset(immunophenotype)
    scenarios = {}
    for rab_max_kill in rab_max_kill_values:
        if rab_max_kill > 0:
            combo_model = ResistanceModel(growth=model.growth, ic50_nM=model.ic50_nM,
                                          max_kill=model.max_kill, mutation=model.mutation,
                                          hill=model.hill, carrying_capacity=model.carrying_capacity,
                                          ic50_nM_2=LYMPHOMA_RAB_ILLUSTRATIVE_IC50_NM,
                                          max_kill_2=rab_max_kill)
        else:
            combo_model = model
        scenarios[rab_max_kill] = (combo_model, css, seeding_rates,
                                   {**provenance, "rab_max_kill": rab_max_kill})
    return scenarios


def lymphoma_immunotherapy_followon_scenarios(
        rab_max_kill: float = 0.0, immunophenotype: str = "B",
        immunotherapy_max_kill_values: list[float] = LYMPHOMA_IMMUNOTHERAPY_MAX_KILL_SWEEP,
        ) -> dict[float, tuple[ResistanceModel, float, np.ndarray, dict]]:
    """CHOP (+/- rabacfosadine) plus a swept-potency CD20-directed immune effector, with a 5th
    CD20-antigen-loss escape clone -- mirroring `hsa_scenarios.hsa_vaccine_followon_scenarios`
    exactly (same engine, `run_monte_carlo_with_vaccine`). The immune kill term applies to every
    clone except the antigen-loss clone; CD20 loss is the one route it cannot see.
    """
    combo_scenarios = lymphoma_combination_scenarios([rab_max_kill], immunophenotype)
    model, css, seeding_rates, provenance = combo_scenarios[rab_max_kill]
    escape_growth = model.growth[1] * LYMPHOMA_CD20_LOSS_GROWTH_PENALTY
    model5 = ResistanceModel(
        growth=np.append(model.growth, escape_growth),
        ic50_nM=np.append(model.ic50_nM, model.ic50_nM[1]),
        max_kill=np.append(model.max_kill, model.max_kill[1]),
        mutation=np.eye(len(model.growth) + 1),
        hill=model.hill, carrying_capacity=model.carrying_capacity,
        ic50_nM_2=model.ic50_nM_2, max_kill_2=model.max_kill_2, hill_2=model.hill_2,
    )
    scenarios = {}
    for immunotherapy_max_kill in immunotherapy_max_kill_values:
        scenarios[immunotherapy_max_kill] = (model5, css, seeding_rates, {
            **provenance, "immunotherapy_max_kill": immunotherapy_max_kill,
            "immunotherapy_start_day": LYMPHOMA_IMMUNOTHERAPY_START_DAY,
            "immunotherapy_ramp_days": LYMPHOMA_IMMUNOTHERAPY_RAMP_DAYS,
            "cd20_loss_seeding_rate": LYMPHOMA_CD20_LOSS_SEEDING_RATE,
            "cd20_loss_growth_penalty": LYMPHOMA_CD20_LOSS_GROWTH_PENALTY,
        })
    return scenarios
