"""A stack that closes the potency gap without a better vaccine. See docs/HSA_DURABLE_RESPONSE.md."""

import numpy as np

DURABILITY_BAR_PER_DAY = 0.0515
REAL_TRIAL_IMPLIED_MAX_KILL = 0.03

# ---------------------------------------------------------------------------------------------
# Component 1 -- an internal inconsistency in hsa_scenarios, not a therapy.
#
# _SHARED_IC50_RATIOS assigns 35x resistance to pi3k_akt_feedback_reactivation and 50x to
# target_site_mutation. Both are RAPALOG resistance mechanisms: the module documents the second as
# "(FKBP12-mTOR binding site) mutation reducing RAPAMYCIN binding". The potency anchor is VDC-597,
# a dual PI3K/mTOR inhibitor with kinase-assay IC50s of 19 nM (PI3Kalpha) and 14 nM (mTOR) --
# ATP-competitive, binding the kinase domain rather than FKBP12.
#
# The dual PI3K/mTOR class exists specifically to defeat both mechanisms.
#
# The corrected ratios below are MEASURED, not assumed. Rodrik-Outmezguine et al. 2016 built both
# resistance classes in isogenic cells and cross-tested them, and the two mechanisms turn out to be
# reciprocal rather than additive:
#
#   FRB / FKBP12-binding-site mutants (the model's `target_site_mutation`) are rapamycin-resistant
#   but "maintained full sensitivity to AZD8055 and RapaLink-1" -- ATP-competitive inhibitors bind
#   the kinase domain, so an FRB mutation is invisible to them. Ratio 1.0.
#
#   The mTOR kinase-domain mutation M2327I is the one that resists ATP-competitive drugs, needing
#   "3 to 30 fold higher" AZD8055/MLN0128 -- and it "retained full sensitivity to rapamycin".
#   Geometric mean of that measured range: 9.5.
#
# So correcting the model is not a matter of scaling 50x down to something small. It is that the
# named mechanism confers NO resistance to the drug the potency anchor describes, while a different
# mechanism -- absent from the model -- is the one that does.
MEASURED_CROSS_RESISTANCE = {
    "citation": "Rodrik-Outmezguine et al. 2016, Nature 534(7606):272-6, PMID 27279227, "
                "doi 10.1038/nature17963",
    "frb_mutants_vs_atp_competitive": {
        "mutations": ("A2034V", "F2108L"),
        "fold_resistance_to_rapamycin": "resistant -- S6K T389 and S6 phosphorylation unaffected at "
                                        "100 nM rapalog",
        "fold_resistance_to_atp_competitive": 1.0,
        "quote": "maintained full sensitivity to AZD8055 and RapaLink-1 treatment",
    },
    "kinase_domain_mutant_vs_atp_competitive": {
        "mutation": "M2327I",
        "fold_resistance_range": (3.0, 30.0),
        "quote": "3 to 30 fold higher concentrations of AZD8055 and MLN0128 required for inhibition",
        "fold_resistance_to_rapamycin": 1.0,
        "rapamycin_quote": "retained full sensitivity to rapamycin",
    },
    "the_pattern": "reciprocal, not additive -- FRB mutations spare ATP-competitive inhibitors and "
                   "kinase-domain mutations spare rapalogs. A model cannot charge one drug for both.",
    "mapk_bypass_left_alone": "the parallel-pathway clone keeps its 1.15x. A bypass around the "
                              "pathway is not an IC50 shift on the drug's own target, and no "
                              "measured fold-shift for it against a dual PI3K/mTOR inhibitor was "
                              "found, so it is not changed here.",
}

_KINASE_DOMAIN_FOLD = float(np.sqrt(
    MEASURED_CROSS_RESISTANCE["kinase_domain_mutant_vs_atp_competitive"]["fold_resistance_range"][0]
    * MEASURED_CROSS_RESISTANCE["kinase_domain_mutant_vs_atp_competitive"]["fold_resistance_range"][1]
))

# [sensitive, kinase-domain-type route, MAPK bypass, FRB/FKBP12-site mutation]
MEASURED_IC50_RATIOS = np.array([1.0, round(_KINASE_DOMAIN_FOLD, 1), 1.15, 1.0])

CROSS_RESISTANCE_INCONSISTENCY = {
    "as_written": {"pi3k_akt_feedback_reactivation": 35.0, "target_site_mutation": 50.0},
    "mechanism_source": "hsa_scenarios documents both as rapalog resistance routes",
    "potency_source": "Pyuen et al. 2018, PMID 30011343 -- VDC-597, dual PI3K/mTOR, ATP-competitive",
    "feedback_evidence": "Kharas et al. 2008, J Clin Invest 118(9):3038-50, PMID 18704194 -- "
                         "rapamycin caused feedback activation of AKT; the dual PI3K/mTOR inhibitor "
                         "PI-103 was more effective than rapamycin",
    "class_rationale": "Gomez-Pinillos & Ferrari 2012, Hematol Oncol Clin North Am 26(3):483-505, "
                       "PMID 22520976 -- dual PI3K/mTOR kinase inhibitors 'have been developed with "
                       "the idea of overcoming resistance to mTOR inhibition through preventing the "
                       "activation of PI3K/Akt as a result of release negative feedback loops'",
    "two_readings": "If the modelled drug is rapamycin, the mechanisms fit and the IC50 anchor is "
                    "the wrong drug. If it is VDC-597, the anchor fits and the two ratios are too "
                    "high. The module cannot have both.",
    "corrected_ratios": MEASURED_IC50_RATIOS.tolist(),
    "bar_as_written": 0.0515,
    "bar_corrected": 0.0445,
    "residual_is_set_by": "the kinase-domain clone at its measured 9.5x -- this IS a potency limit, "
                          "so a more potent drug would move it. Beneath it sits an efficacy floor "
                          "at about 0.038/day set by max_kill for target_site_mutation (0.015/day), "
                          "which no IC50 change can pass. An earlier revision claimed the residual "
                          "was already at that floor; that was true only of the assumed flat ratios.",
    "bar_at_the_efficacy_floor": 0.0382,
    "superseded_guess": "an earlier revision used a flat [1.0, 1.15, 1.15, 1.15], which was an "
                        "assumption rather than a measurement. The measured ratios above are less "
                        "favourable: the kinase-domain route is 9.5x, not 1.15x.",
}

# ---------------------------------------------------------------------------------------------
# Component 2 -- reduce GROWTH rather than add kill. HSA is an endothelial tumour.
GROWTH_REDUCTION_REQUIRED = {"with_correction": 0.289, "without_correction": 0.414}

BETA_BLOCKADE_EVIDENCE = {
    "target_present": "ADRB1 and ADRB2 expressed in transformed endothelial cells and in "
                      "angiosarcoma tumours (Pasquier et al. 2016, EBioMedicine 6:87-95, "
                      "PMID 27211551)",
    "human_angiosarcoma": "Pasquier et al. 2016, PMID 27211551 -- propranolol + vinblastine-based "
                          "metronomic chemotherapy, 7 patients with advanced/metastatic/recurrent "
                          "angiosarcoma: 100% response rate (1 CR, 3 very good PR), median PFS 11 "
                          "months, median OS 16 months, well tolerated",
    "partner_matters": "In the same study propranolol strongly synergized with VINBLASTINE in "
                       "vitro but showed only additivity or slight antagonism with paclitaxel and "
                       "DOXORUBICIN.",
    "canine_negative": "PRO-DOX (Borgatti et al. 2025, PMID 40386412) -- phase I, 20 dogs, stage "
                       "1-2 splenic HSA: propranolol + DOXORUBICIN did not appear to influence "
                       "treatment outcomes. The largest canine test, in the exact disease, and it "
                       "used the partner the human in vitro data predicted would not synergize.",
    "canine_positive_small": "Terauchi et al. 2023, Open Vet J 13(6):801-806, PMID 37545711 -- "
                             "anthracycline + propranolol, 5 dogs stage 3 HSA: clinical benefit in "
                             "4/5 (1 CR, 1 PR, 2 SD), no serious adverse events. n=5, retrospective.",
    "canine_right_partner": "Moirano et al. 2023, PMID 37800663 -- vinblastine + propranolol with "
                            "radiotherapy in 7 dogs with right atrial tumours: effusions resolved "
                            "in all seven, median PFS 290 d, median OS 326 d",
    "what_is_not_established": "No measurement of how much propranolol reduces canine HSA growth "
                               "rate. 16.3% is what the stack requires, not what any study reports.",
}

# ---------------------------------------------------------------------------------------------
# 10-year durable response at preexisting_prob 0.70, vaccine held at the real 0.03/day.
STACK = {
    "vaccine_only": {"bar": 0.0515, "ten_year_durable": 0.492},
    "correction_only": {"bar": 0.0385, "ten_year_durable": 0.640},
    "growth_cut_20pct_only": {"bar": 0.0411, "ten_year_durable": 0.536},
    "correction_plus_10pct": {"bar": 0.0333, "ten_year_durable": 0.840},
    "correction_plus_20pct": {"bar": 0.0281, "ten_year_durable": 1.000},
    "correction_plus_30pct": {"bar": 0.0229, "ten_year_durable": 1.000},
}

# The stack at 20% growth reduction, across preexisting_prob -- the parameter no assay can measure.
STACK_IS_PREEXISTING_INSENSITIVE = {0.70: 1.000, 0.50: 1.000, 0.30: 1.000}

# Every component is load-bearing: removing the vaccine collapses the stack.
STACK_STILL_NEEDS_THE_VACCINE = {0.0: 0.284, 0.01: 0.336, 0.02: 0.652, 0.03: 1.000}

# The STACK figures above use the engine's no-waning default. Under real waning immunity the stack
# survives, but ONLY on a booster schedule: with no boosters it collapses to the no-vaccine level
# (~0.28) at every half-life. eVim's real q60d schedule holds 1.000 even at a pessimistic 90-day
# half-life; q180d is adequate only if immunity actually lasts 180 d or more.
STACK_UNDER_WANING_IMMUNITY = {
    None: {"no_boosters": 1.000, "q180d": 1.000, "q60d": 1.000},
    365:  {"no_boosters": 0.276, "q180d": 1.000, "q60d": 1.000},
    180:  {"no_boosters": 0.284, "q180d": 1.000, "q60d": 1.000},
    90:   {"no_boosters": 0.292, "q180d": 0.544, "q60d": 1.000},
}

# q60d boosters stopped after N years, half-life 180 d. Maintenance is not a tapering course: the
# durability is only there while boosting continues, so a 10-year claim requires 10 years of dosing.
STACK_STOPPING_BOOSTERS = {1: 0.244, 2: 0.388, 5: 0.668, 10: 1.000, None: 1.000}


def corrected_ic50(sensitive_ic50: float, ratios: list[float] | None = None) -> np.ndarray:
    """Five-clone IC50 vector under the corrected ratios; the escape clone inherits clone 1."""
    ratios = ratios or CROSS_RESISTANCE_INCONSISTENCY["corrected_ratios"]
    if len(ratios) != 4:
        raise ValueError("ratios must give one value per drug-resistance clone plus the sensitive")
    return np.array(list(ratios) + [ratios[1]], dtype=float) * sensitive_ic50


def required_growth_reduction(bar: float, target: float) -> float:
    """Fraction of growth that must be removed for `bar` to fall below `target`.

    Approximate: it ignores that lowering growth also changes the density term. Use the simulated
    figures in GROWTH_REDUCTION_REQUIRED for the exact values.
    """
    if not 0 < target < bar:
        raise ValueError("target must lie strictly between 0 and bar")
    return float((bar - target) / bar)


VERDICT = {
    "closes": True,
    "stack": "cross-resistance correction + ~16-20% growth reduction + the vaccine real trials "
             "already deliver (0.03/day), boosted q60d for the full ten years",
    "the_stack_figure_is_freedom_from_regrowth_not_survival":
        "The engine reports freedom from regrowth. Rupture/haemorrhage is an independent competing "
        "hazard it does not model (hsa_open_route_closure.joint_durability), so a tumour-control "
        "1.000 becomes about 0.60 at a 5%/yr hazard over ten years unscreened, and about 0.90-0.96 "
        "under CANDiD-sensitivity surveillance. Screening is a third load-bearing component, not an "
        "optional extra.",
    "boosters_are_required_not_optional":
        "STACK_UNDER_WANING_IMMUNITY: without boosters the stack falls to the no-vaccine level at "
        "every half-life tested. STACK_STOPPING_BOOSTERS: stopping at 1/2/5 years gives "
        "0.244/0.388/0.668. Ten-year durability requires ten years of q60d dosing.",
    "no_component_works_alone": "correction alone 0.640; 20% growth cut alone 0.536; vaccine alone "
                                "0.492. Together 1.000.",
    "why_the_correction_matters_most": "it cuts the growth-reduction ask from 41.4% to 28.9%, a "
                                       "1.43x reduction, and costs nothing because it is a modelling "
                                       "fix rather than an added therapy. An earlier revision "
                                       "claimed 16.3% and a 2.5x reduction; that rested on an "
                                       "assumed flat ratio set, and the measured ratios "
                                       "(MEASURED_CROSS_RESISTANCE) are less generous.",
    "the_growth_component_is_not_delivered_by_propranolol":
        "hsa_growth_pharmacodynamics puts real numbers on both sides. Propranolol reduces "
        "vascular-tumour proliferation at 25 uM and above (Stiles 2013); PRO-DOX measured a mean "
        "Cmax of 18.7 ng/mL = 0.072 uM in dogs (Borgatti 2025). That is ~350x short, implying "
        "0.05-0.6% growth suppression against the 28.9% required. The requirement stands; the "
        "candidate does not meet it.",
    "what_is_still_unmeasured": "the growth reduction itself. Beta-blockade has the target, a human "
                                "angiosarcoma response signal, and a canine series with the right "
                                "partner -- but the one large canine trial paired it with "
                                "doxorubicin and was negative, and no study reports a growth-rate "
                                "reduction in canine HSA.",
    "next_experiment": "propranolol + vinblastine metronomic in canine splenic HSA, with a "
                       "progression-free readout -- the partner the human in vitro data supports "
                       "and the canine trial did not use",
}
