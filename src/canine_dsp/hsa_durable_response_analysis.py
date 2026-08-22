"""Durable response in canine hemangiosarcoma: the mechanism, the escape routes, and their closure.
The histiocytic-sarcoma (HS) work in this project asked a specific sequence of questions -- what
carries durability, what is the per-day bar a persistent mechanism must clear, is that bar
achievable against real trial data, which escape routes survive, and what closes each one. This
module asks the same sequence of HSA, reusing `hsa_scenarios`' own presets and real anchors rather
than introducing new ones. See docs/HSA_DURABLE_RESPONSE.md.
"""

import numpy as np

# The bar, by drug-exposure assumption. Computed via mapk_resistance.clone_growth_margins against
# hsa_scenarios.dog_hsa_preset; reproduced by test_hsa_durable_response_analysis.
DURABILITY_BAR_PER_DAY = {
    "assumed_5x_ic50_module_default": 0.0515,
    "derated_to_40pct_for_toxicity": 0.0519,
    "real_rapamycin_trough_10_9nM": 0.0545,
    "no_drug_at_all": 0.0550,
    "set_by_clone": "target_site_mutation under drug; sensitive once drug pressure is removed",
    "interpretation": "A 7% spread between full assumed drug exposure and no drug at all. The "
                     "inhibitor decides how fast the bulk tumour shrinks, not whether it returns.",
}

RAPAMYCIN_REAL_EXPOSURE = {
    "citation": "Paoloni et al. 2010, PLOS ONE 5(6):e11013, PMID 20543980",
    "measured": "median trough > 10 ng/mL at 0.06-0.08 mg/kg IM daily in dogs with cancer, no MTD "
               "reached, target inhibition confirmed (>2-fold tumoral phospho-S6RP reduction, 8/10)",
    "molecular_weight_g_per_mol": 914.17,
    "trough_nM": 10.94,
    "vdc597_ic50_nM": 543.33,
    "fold_below_ic50": 49.7,
    "consequence": "At real exposure the sensitive clone's margin is +0.0545/day versus "
                   "+0.0550/day untreated -- the real drug at its real dose does essentially "
                   "nothing in this model.",
    "why_this_is_scoping_not_retraction": "The drug was never carrying durability, so over-stating "
                                         "its exposure inflates response SPEED, not the vaccine "
                                         "threshold. The bar moves 0.0515 -> 0.0545.",
}

VACCINE_ACHIEVABILITY = {
    "real_trials": [
        {"name": "ERstrePs", "citation": "Marconato et al. 2023, Cancers 15(17):4209, PMID 37686485",
         "n_vaccinated": 28, "n_control": 32, "one_year_survival": 0.357,
         "one_year_survival_control": 0.063, "gain_pp": 29.4,
         "mechanism": "peptide-based; humoral AND vaccine-specific T-cell response both reported"},
        {"name": "eVim", "citation": "Engbersen et al. 2025, Int J Mol Sci 26(18):9096, PMID 41009669",
         "n_vaccinated": 23, "one_year_survival": 0.44, "one_year_survival_control": 0.14,
         "gain_pp": 30.0,
         "mechanism": "iBoost conjugate vaccine against EXTRACELLULAR vimentin; antibody-mediated; "
                     "maintenance vaccinations every two months"},
    ],
    "engine_one_year_durable_by_potency": {0.0: 0.338, 0.01: 0.443, 0.02: 0.508, 0.03: 0.647,
                                           0.04: 0.848, 0.05: 1.000, 0.06: 1.000},
    "implied_vaccine_max_kill": 0.03,
    "bar_to_clear": 0.0515,
    "verdict": "Real canine HSA vaccination implies roughly 0.03/day.",
}

ESCAPE_ROUTES = [
    {
        "id": 1,
        "name": "pi3k_akt_feedback_reactivation",
        "status": "CLOSED by construction, not by potency",
        "detail": "Loss of mTORC1-mediated negative feedback reactivating upstream PI3K/AKT.",
    },
    {
        "id": 2,
        "name": "mapk_crosstalk_bypass",
        "status": "CLOSED by construction, not by potency",
        "detail": "Parallel MAPK/ERK activation routing around mTORC1.",
    },
    {
        "id": 3,
        "name": "target_site_mutation",
        "status": "CLOSED by construction -- AND IT SETS THE BAR",
        "detail": "FKBP12-mTOR binding-site alteration.",
    },
    {
        "id": 4,
        "name": "antigen / MHC-I loss (the modelled immune_escape clone)",
        "status": "MODELLED AS UNCLOSABLE; that is wrong for HSA, and it is minor in simulation too",
        "detail": "Coverage hard-coded to exactly 0.0, inherited from the HS module's "
                  "peptide/MHC-I vaccine. Three independent reasons it does not transfer: (i) "
                  "eVim is an ANTIBODY response against extracellular vimentin, which does not "
                  "use MHC-I at all -- `hsa_scenarios` establishes this itself when refusing to "
                  "run NetMHCpan on it, then models MHC-I loss anyway; (ii) ERstrePs raises "
                  "humoral AND T-cell responses, so MHC-I loss degrades rather than evades it; "
                  "(iii) MHC-loss variants upregulate NKG2D ligands and primed CD8 T-cells kill "
                  "them through NKG2D (Lerner et al. 2023, PMID 37537301).",
        "how_to_close_it_anyway": "A PERSISTENT mechanism-agnostic kill term at >= 0.05/day closes "
                                 "it completely even at 1000x the assumed seeding rate (escape-clone "
                                 "margin +0.0415/day). eBAT already has the right coverage (EGFR/uPAR "
                                 "are surface receptors, modelled as a scalar applied to every clone) "
                                 "and the wrong duration (28 days, plus ~30% neutralising-antibody "
                                 "development). eVim's real two-monthly maintenance schedule is the "
                                 "only mechanism here that is persistent AND MHC-independent at once.",
    },
    {
        "id": 5,
        "name": "Splenic rupture / acute internal haemorrhage",
        "status": "OPEN, NOT MODELLED AT ALL, and the module says so",
        "detail": "HSA's signature complication: death independent of whether a resistant clone "
                  "is regrowing.",
    },
    {
        "id": 6,
        "name": "Vaccine failure without antigen loss",
        "status": "OPEN, NOT MODELLED",
        "detail": "T-cell exhaustion, immunosuppressive microenvironment, failure to prime at "
                  "all, or -- for eVim specifically -- an antibody titre that never reaches a "
                  "functional threshold.",
    },
    {
        "id": 7,
        "name": "Micrometastatic disease outside any modelled compartment",
        "status": "OPEN, NOT MODELLED -- and this is the asymmetry with HS",
        "detail": "The HS pipeline built `run_monte_carlo_two_compartment` for localized "
                  "pulmonary Corgi HS specifically because regional nodal disease may already "
                  "have spread before surgery.",
    },
]

MECHANISM_LEDGER = {
    "what_durability_actually_requires": "A kill term that is (a) PERSISTENT -- no cumulative-dose "
                                        "cap, no fixed exposure window -- and (b) covers every "
                                        "clone that can arise, at >= the bar of ~0.052/day.",
    "candidates": [
        {"mechanism": "PI3K/mTOR inhibitor (rapamycin / VDC-597)",
         "persistent": True, "covers_all_clones": False, "clears_the_bar": False,
         "verdict": "Backbone for response SPEED. Moves the bar by 7%. At real rapamycin exposure "
                   "it does not suppress even the sensitive clone."},
        {"mechanism": "eBAT (EGF/uPAR bispecific immunotoxin)",
         "persistent": False, "covers_all_clones": True, "clears_the_bar": "at >=0.05/day, while dosed",
         "verdict": "Right coverage, wrong duration. 28-day window; ~30% of dogs develop "
                    "neutralising antibodies."},
        {"mechanism": "Cancer vaccine (ERstrePs / eVim class)",
         "persistent": True, "covers_all_clones": "all but the modelled MHC-I-loss clone",
         "clears_the_bar": "not at real-trial-implied potency (~0.03 vs ~0.052)",
         "verdict": "The only mechanism carrying durability, and the only one whose real-world "
                   "potency can be bounded from trials in this disease. Short by ~1.7x."},
        {"mechanism": "NKG2D killing by vaccine-primed CD8 T-cells",
         "persistent": "inherits the vaccine's persistence", "covers_all_clones": True,
         "clears_the_bar": "unquantified -- magnitude never measured",
         "verdict": "Closes route 4 at no added agent, because it is a property of the primed "
                    "population rather than a separate therapy."},
        {"mechanism": "Splenectomy",
         "persistent": False, "covers_all_clones": True, "clears_the_bar": False,
         "verdict": "Delay, not durability. Moves 1-year durable response by 8-11 points and "
                   "2-year by 1.5-4, because it changes where clones start and not the sign of "
                   "their growth margins."},
    ],
    "the_gap_that_matters": "Nothing in this inventory is both persistent and demonstrated to "
                            "clear 0.052/day in a dog.",
}

WHAT_WOULD_CHANGE_THE_ANSWER = [
    "Measure a canine HSA vaccine's kill rate directly rather than inferring it from survival: "
    "serial imaging or ctDNA on a vaccinated cohort gives a progression-free readout the engine "
    "consumes natively, removing the survival-vs-progression mismatch that makes the 1.7x "
    "shortfall a lower bound rather than an estimate.",
    "Re-run every HSA time-course at real rapamycin exposure (10.9 nM), the way the HS pipeline "
    "re-ran branch D.",
    "Replace the inherited MHC-I-loss escape clone with a mechanism matched to the actual vaccine: "
    "surface-vimentin loss for eVim, which needs a fitness cost of its own, since vimentin is "
    "structural rather than a passenger antigen.",
    "Model the second compartment. Splenic HSA is disseminated at diagnosis more often than the "
    "Corgi pulmonary presentation that already has a two-compartment model.",
    "Give the module a rupture/haemorrhage hazard once any real rate exists.",
]
