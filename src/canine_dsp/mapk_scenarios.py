"""Illustrative scenario presets for the generic MAPK-resistance engine in `mapk_resistance.py`.

Everything in this module is "the exact scenarios we have traded" -- specific breed/drug/disease-
site parameterizations, case-series citations, and illustrative placeholder constants -- kept
deliberately separate from the reusable simulation engine (`mapk_resistance.py`: `ResistanceModel`,
`run_monte_carlo*`, `decompose_patient_uncertainty`, etc.) and from the demo/report functions that
consume a scenario and produce CSV/plot/summary.json output (`mapk_cli.py`).

The split exists so that once real data lands for this disease (tumor sequencing, canine-specific
drug PK, DLA genotyping, vaccine immunogenicity, relapse-timing/ctDNA kinetics), a new scenario
module built from that data can reuse every demo function and every line of the engine unchanged --
only the presets here need to be swapped or added to.
"""

from dataclasses import replace
from pathlib import Path

import numpy as np

from .alphafold import download_structure, extract_mutant_peptide, read_plddt_track
from .mapk_resistance import CLONE_NAMES, ResistanceModel
from .uniprot import DOG_TAXID, resolve_uniprot_accession

_SHARED_GROWTH = np.array([.06, .05, .055, .058])  # per-day; illustrative, not fitted
# Per-day kill-rate ceiling per clone: sensitive is driven well past its growth rate (real
# regression); rtk_bypass keeps the same drug potency (IC50) but a much lower kill ceiling
# (survival signal bypasses the inhibited target); the other two resistant clones both shift
# IC50 and cap kill low, leaving them with net-positive growth throughout treatment.
_SHARED_MAX_KILL = np.array([.18, .02, .035, .015])
_SHARED_IC50_RATIOS = np.array([1.0, 40.0, 1.2, 60.0])
_SHARED_MUTATION = np.eye(4)  # acquired resistance is scheduled stochastically, not via this matrix

# Loosely tuned so the dog preset's durable-response probability is in the same ballpark as the
# handful of published MAPK-inhibitor HS case reports at ~2 years follow-up (Gounder et al. 2018,
# NEJM, PMID 29768143: >2 years, no relapse; a KRAS-mutant case at 31 months without relapse; a
# BRAF-mutant case in partial remission at 3 years) -- not a fit: n=3 case reports, all published
# specifically because the response was durable (survivorship/publication bias), so the true rate
# is almost certainly lower than "3 of 3 durable." Treat this constant as a dial, not a result.
_SEEDING_RATE_TOTAL = 0.012

# probability that a resistant subclone already exists at treatment start is the single most
# influential, least-grounded parameter in this model (see mapk_resistance_demo). Swept rather
# than fixed to one asserted value, because a point estimate here was found to be effectively
# tuning the headline result rather than discovering it.
_PREEXISTING_PROB_SWEEP = [0.05, 0.15, 0.30, 0.50, 0.70]
# NOT recentered against COMBI_D_V_FIVE_YEAR_BENCHMARK below, on reflection -- an earlier version
# of this comment did recenter it to 0.70 on that basis, which was a mistake caught on further
# scrutiny of how weak that comparison actually is. The two situations look superficially similar
# but are not: HSA's equivalent constant (hsa_scenarios.py) was recentered against the real eBAT
# trial, which differs from that module's modeled drug in *mechanism only* -- same species (dog),
# same disease (HSA), same drug class question (does a real HSA treatment's outcome data suggest
# more pre-existing resistance than assumed). COMBI_D_V_FIVE_YEAR_BENCHMARK stacks four mismatches
# at once: different species (human), different disease/cell lineage (melanoma, not histiocytic
# sarcoma), different driver mutation/pathway node (BRAF V600 vs. this module's PTPN11/KRAS), and
# a mechanistically different drug pairing (COMBI-d/v is two real MAPK-pathway inhibitors blocking
# the *same* pathway at sequential nodes, versus this module's MAPK inhibitor + an illustrative,
# deliberately mechanism-agnostic second-node drug hitting a *different* pathway entirely). It is
# also specifically a bad source for calibrating *this* parameter: melanoma has an unusually high,
# UV-mutagenesis-driven tumor mutational burden, so whatever rate of pre-existing resistant clones
# it implies is not evidence about a UV-unrelated canine sarcoma's clonal heterogeneity. This is
# exactly the same "different disease and different mechanism" mismatch MAPK_INHIBITOR_HUMAN_
# BENCHMARK below was already written to avoid stacking onto any fitted constant -- reusing a
# closely related paper from the same trials to justify moving a parameter anyway was inconsistent
# with that standard. COMBI_D_V_FIVE_YEAR_BENCHMARK is kept as a scale-only reference (see its own
# caveat), the same role LOMUSTINE_BENCHMARK and MAPK_INHIBITOR_HUMAN_BENCHMARK already play, not
# as a recentering basis.
_PREEXISTING_PROB_CENTRAL = 0.30

# Two published lomustine (non-targeted chemotherapy) studies in unselected canine HS, included
# as an automatic sanity check against this module's synthetic MAPK-inhibitor projections. The
# two studies disagree with each other (29% vs 46% response rate) and report different endpoints
# (response duration vs. overall survival) -- a reminder that even a "real" benchmark here is not
# one settled number, before comparing it to an entirely uncalibrated synthetic model.
LOMUSTINE_BENCHMARK = {
    "population": "unselected canine HS (not restricted to MAPK-pathway-mutant cases)",
    "studies": [
        {"citation": "Rassnick et al. 2010, J Vet Intern Med, PMID 21155191",
         "design": "21 previously untreated dogs, single-agent CCNU 90 mg/m^2 every 4 weeks",
         "overall_response_rate": 0.29, "median_response_duration_days": 96},
        {"citation": "Skorupski et al. 2007, J Vet Intern Med, PMID 17338159",
         "design": "56-59 dogs, CCNU 60-90 mg/m^2",
         "overall_response_rate": 0.46, "median_overall_survival_days": 106,
         "median_survival_responders_days": 172, "median_survival_nonresponders_days": 60},
    ],
    "caveat": "Provided for scale, not as a like-for-like comparator: lomustine's population is "
             "not restricted to MAPK-mutant dogs, and neither study's endpoint matches this "
             "module's RECIST-style progression-from-nadir definition.",
}

# A second real sanity-check benchmark, this time from the human side of the same driver pathway:
# real patients, a real MAPK-inhibitor combination, real measured time-to-progression -- found by
# searching for published mathematical-oncology models fit to real clinical resistance-timing
# data for BRAF/MEK-inhibitor therapy (the search that also turned up KPR above). Most candidates
# found either weren't fit to human clinical data at all (one systems-pharmacology BRAF/MEK +
# checkpoint-inhibitor model was calibrated against mouse xenograft experiments, not patients, and
# doesn't model resistance dynamics) or were inaccessible to verify -- this is the one number that
# held up on direct inspection of the source paper, not a model parameter, and is used the same
# way LOMUSTINE_BENCHMARK is: a labeled reference line to compare this module's own
# median_time_to_progression_days against, not something fit into any growth/kill/seeding-rate
# constant above (mapping a human-melanoma, BRAF-mutant, ctDNA-monitored cohort onto a canine-HS,
# PTPN11/KRAS-mutant, imaging-monitored model would stack a cross-species and cross-mutation
# extrapolation on top of an already-illustrative one).
MAPK_INHIBITOR_HUMAN_BENCHMARK = {
    "citation": "Schreuer et al. 2016, J Transl Med 14:95, PMID 27095081",
    "population": "36 metastatic (mostly stage IVc) BRAF-V600-mutant melanoma patients on "
                  "dabrafenib+trametinib (BRAF+MEK inhibitor combination -- a real precedent for "
                  "combining a MEK inhibitor with a second MAPK-pathway-targeted agent, though "
                  "the second agent, mutation, tumor type, and species all differ from this "
                  "module's own scenarios)",
    "median_days_to_clinical_progression": 111,  # 95% CI 98-124; 27 of 36 patients progressed
    "confidence_interval_days": [98, 124],
    "progressed_fraction": 27 / 36,
    "caveat": "A different species, mutation (BRAF, not PTPN11/KRAS), drug pair, and disease "
             "stage than any scenario in this module -- provided for scale (does this module's "
             "own median_time_to_progression_days land in a remotely plausible range once a "
             "resistant clone is present, compared to a real MAPK-inhibitor-treated cohort), not "
             "as a validation of this module's specific numbers. Weaker than that framing implies "
             "on its own terms, too: this is a ctDNA-biomarker-monitoring report, not a full "
             "efficacy trial writeup -- no objective response rate, no PFS measured from "
             "treatment start, no overall survival, and no systematic toxicity data are given in "
             "the source paper. The 111-day figure is time from when ctDNA monitoring began to "
             "clinical progression, and monitoring 'began at variable timepoints relative to "
             "treatment initiation' (the paper's own wording) -- some patients may already have "
             "been on drug before entering ctDNA monitoring, so real time-from-treatment-start-"
             "to-progression could run longer than 111 days for at least some of the cohort.",
}

# The comparator actually used to stress-test this module's own "durable response" combination-
# therapy claim (mapk_durability_horizon_demo): the pivotal, pooled 5-year follow-up of the same
# BRAF+MEK inhibitor combination in human metastatic melanoma. Verified directly against the
# source paper (not taken from a summary or a research agent). Same species/disease/drug-pair
# caveats as MAPK_INHIBITOR_HUMAN_BENCHMARK apply -- this is a different, later paper from the
# same trials (COMBI-d, COMBI-v), reporting durability endpoints instead of ctDNA-based
# progression timing.
COMBI_D_V_FIVE_YEAR_BENCHMARK = {
    "citation": "Robert C, Grob JJ, Stroyakovskiy D, et al. Five-Year Outcomes with Dabrafenib "
               "plus Trametinib in Metastatic Melanoma. N Engl J Med. 2019;381:626-636, "
               "PMID 31166680",
    "population": "563 previously untreated, unresectable/metastatic BRAF V600E/K-mutant "
                  "melanoma patients, pooled from the COMBI-d and COMBI-v phase III trials, "
                  "first-line dabrafenib (BRAF inhibitor) + trametinib (MEK inhibitor)",
    "five_year_progression_free_survival_full_population": 0.19,
    "five_year_overall_survival_full_population": 0.34,
    "complete_response_fraction": 109 / 563,
    "five_year_overall_survival_complete_responders": 0.71,
    "caveat": "Provided for scale only, not as a calibration target -- do not use this to justify "
             "moving any constant above. Stacks four mismatches against this module's own "
             "scenarios at once: different species (human vs. dog), different disease/cell "
             "lineage (melanocyte-derived metastatic melanoma vs. histiocyte-derived HS), "
             "different driver mutation/pathway node (BRAF V600E/K vs. this module's PTPN11/"
             "KRAS), and a mechanistically different drug pairing (two real MAPK-pathway "
             "inhibitors blocking the *same* pathway at sequential nodes here, vs. this module's "
             "MAPK inhibitor + an illustrative, deliberately mechanism-agnostic second-node drug "
             "hitting a *different* pathway). It is also a poor source specifically for "
             "calibrating a pre-existing-resistant-clone-prevalence parameter: melanoma carries "
             "an unusually high, UV-mutagenesis-driven tumor mutational burden, so whatever rate "
             "of pre-existing resistant clones it implies says little about a UV-unrelated canine "
             "sarcoma's clonal heterogeneity. Even the fairer of its two headline numbers (71% "
             "5-year OS among the 19% of patients who achieved a complete response, versus the "
             "full population's cruder 19% 5-year PFS / 34% 5-year OS) does not change this -- "
             "the mismatch is in what disease and mutation produced the number, not in which "
             "endpoint was picked.",
}

# Fraction of plasma drug concentration reached in brain tissue -- real, drug-specific PK
# measurements (P-gp/BCRP-limited), not distinguished below by brain region (rostrotentorial
# cerebrum, the common presentation, vs. infratentorial cerebellum/brainstem, the minority one).
# Regional BBB heterogeneity is real and documented -- cerebellum is specifically named as one of
# several differentially specialized regions in recent single-cell BBB profiling -- but no
# quantified cerebrum-vs-cerebellum comparison was found; asserting a numeric difference would be
# less honest than treating them the same and exposing `location_penetration_multiplier` below
# for anyone who wants to stress-test an assumed difference.
BRAIN_PENETRATION_FRACTION = {
    "systemic_reference": 1.0,
    "trametinib": 0.15,    # the drug actually in canine clinical trials
    "cobimetinib": 0.027,  # the drug this model's cellular IC50s are measured from
}

# Two germline GWAS findings, included because they argue for *breed-level* homogeneity through
# a different mechanism than anatomic location does (see the conversation this module resulted
# from): a shared inherited background, not a shared acquired driver mutation. Both loci are real
# (published GWAS); the mechanism-weight link to acquired-resistance routes below is this
# module's own speculative extension, not a published association -- flagged in each preset's
# provenance rather than presented as a finding.
BREED_GERMLINE_LOCI = {
    "bmd": "CFA11 haplotype spanning MTAP/CDKN2A, present in 96% of affected Bernese Mountain "
          "Dogs (GWAS) -- a cell-cycle/tumor-suppressor locus. CDKN2A/MTAP loss is a known "
          "cooperating lesion with RAS/MAPK activation in several human cancers; if that holds "
          "here, it is a plausible (unproven) mechanistic link to BMD HS's PTPN11/KRAS-dominated "
          "acquired-driver spectrum.",
    "flat_coated_retriever": "Two distinct loci on CFA5 and CFA19 (GWAS); the CFA5 locus "
          "implicates PIK3R6, a PI3K-pathway gene -- a different germline background entirely "
          "from BMD's. Speculative extension used here: weight this breed's acquired-resistance "
          "spectrum toward the PI3K/AKT-linked rtk_bypass mechanism rather than PTPN11-like "
          "pathway_reactivation.",
}


def canine_cns_hs_scenarios(breed: str = "bmd", location_penetration_multiplier: float = 1.0
                            ) -> dict[str, tuple[ResistanceModel, float, np.ndarray, dict]]:
    """Primary CNS histiocytic sarcoma scenarios, one per reference drug's brain penetration.

    This is doubly extrapolated relative to `dog_preset`: no canine CNS-specific mutation study
    exists, so it still assumes the systemic PTPN11/KRAS-dominated spectrum applies intracranially
    (unverified), and effective drug exposure is discounted by each drug's real brain-to-plasma
    ratio applied to the same cellular potency numbers (which are cobimetinib's, not trametinib's
    -- see `dog_preset`). `location_penetration_multiplier` defaults to 1.0 (no assumed cerebrum
    vs. cerebellum difference); override it only to explore a hypothesis, not because a real
    number supports one direction over the other.
    """
    base_model, systemic_css, base_rates, base_provenance = dog_preset()
    if breed == "flat_coated_retriever":
        seeding_rates = _SEEDING_RATE_TOTAL * np.array([.20, .60, .20])
    else:
        seeding_rates = base_rates

    scenarios = {}
    for drug, fraction in BRAIN_PENETRATION_FRACTION.items():
        effective_css = systemic_css * fraction * location_penetration_multiplier
        provenance = {
            **base_provenance, "site": "primary CNS (extrapolated from systemic data)",
            "breed_context": breed, "breed_germline_locus": BREED_GERMLINE_LOCI.get(breed),
            "brain_penetration_reference_drug": drug, "brain_penetration_fraction": fraction,
            "location_penetration_multiplier": location_penetration_multiplier,
        }
        scenarios[drug] = (base_model, effective_css, seeding_rates, provenance)
    return scenarios


# Fraction of tumor burden removed by local therapy (surgery and/or focal radiation) ahead of
# systemic drug treatment. Illustrative -- not fit to a specific reported canine
# resection-completeness statistic -- chosen to represent a real neurosurgical gross-total
# resection while leaving microscopic residual disease, which is why adjuvant systemic therapy
# still matters in this scenario rather than replacing it.
DEBULKING_FRACTION = 0.97

DENDRITIC_CELL_ORIGIN_NOTE = (
    "Primary intracranial histiocytic sarcoma (PIHS) arises from dendritic cells resident in "
    "the meninges and choroid plexus -- a population that is developmentally and anatomically "
    "distinct from the body-wide interstitial dendritic cells that give rise to disseminated "
    "HS (Kishimoto et al. 2020; Moore 2014, Vet Pathol 51:167-184). In mice, this specific "
    "CNS-resident dendritic-cell population has a documented dependency on FLT3-ligand "
    "signaling and the transcription factors BATF3, IRF8, and ID2 for its development "
    "(Anandasabapathy et al. 2011, J Exp Med 208:1695-1705) -- not verified in dogs, and "
    "included here as this module's own candidate-gene hypothesis for what a breed-restricted germline "
    "PIHS-risk variant might affect, distinct from BMD's generic CDKN2A/MTAP tumor-suppressor "
    "mechanism. If real, a lineage-restricted germline mechanism would explain both the "
    "anatomic restriction to the cerebrum and the near-absence of dissemination with one "
    "mechanism, rather than requiring two independent explanations."
)

LOCALIZED_THERAPY_PRECEDENT = (
    "Combining local therapy with systemic therapy is not speculative for canine HS generally: "
    "Skorupski et al. 2009 (Vet Comp Oncol) reported a 568-day median survival across 16 dogs "
    "with localized HS treated with aggressive local therapy (surgery/radiation) plus adjuvant "
    "CCNU, versus 96-106 days for disseminated/unresectable disease on CCNU alone (Rassnick et "
    "al. 2010; Skorupski et al. 2007). A single CNS-specific case report (frontal-lobe PIHS, "
    "surgical resection plus low-dose CCNU) survived recurrence-free past one year. "
    "DEBULKING_FRACTION substitutes a MAPK inhibitor (trametinib, the real canine trial drug) for "
    "CCNU as the adjuvant in this scenario. "
    "CORRECTED -- DO NOT QUOTE THE 568-DAY FIGURE AS A CNS BENCHMARK: this paragraph previously "
    "hedged that 'that cohort's CNS-specific fraction is not confirmed', which was true but left "
    "the mismatched number as the only one on the page, and it began functioning here as a de facto "
    "intracranial durability precedent. The matched figures exist and are worse by an order of "
    "magnitude. Toyoda et al. 2020 (J Vet Intern Med 34(2):828-837, PMID 31919895, n=102 CNS HS) "
    "reports primary CNS HS on DEFINITIVE local therapy at a 43-day median (n=12, 95% CI 5-127), a "
    "maximum survival anywhere in the series of <8 months, and only 8 of 96 dogs past 4 months. "
    "Skorupski's own cohort was also not relapse-free-durable: median disease-free interval 243 "
    "days, 10 of 16 dogs relapsed at a median 201 days, so 568 days is survival WITH relapse. The "
    "site-matched pulmonary counterpart is Murray et al. 2022 (Vet Comp Oncol, PMID 34878710, n=27, "
    "curative-intent lobectomy plus adjuvant CCNU): 432-day median. See "
    "`local_therapy_durability_audit` for the full audit and for the computed demonstration that "
    "debulking does not lower the vaccine's potency bar at any resection completeness."
)


def localized_pihs_scenarios(breed: str = "bmd", debulking_fraction: float = DEBULKING_FRACTION,
                             location_penetration_multiplier: float = 1.0
                             ) -> dict[str, tuple[ResistanceModel, float, np.ndarray, float, dict]]:
    """Four-arm comparison: local debulking x adjuvant MAPK-inhibitor therapy for primary CNS HS.

    Debulking is modeled by lowering `initial_burden` alone (see
    `mapk_resistance.run_monte_carlo`), which also proportionally shrinks any pre-existing
    resistant subclone -- a resection removes resistant and sensitive cells alike, it doesn't
    selectively spare resistant ones. This is a hypothesis-generating comparison, not a
    validated prediction: see DENDRITIC_CELL_ORIGIN_NOTE and LOCALIZED_THERAPY_PRECEDENT for
    what is and isn't established.
    """
    cns_scenarios = canine_cns_hs_scenarios(breed, location_penetration_multiplier)
    _, trametinib_css, seeding_rates, base_provenance = cns_scenarios["trametinib"]
    baseline_burden = .3

    arms = {}
    for debulked in (False, True):
        initial_burden = baseline_burden * (1 - debulking_fraction) if debulked else baseline_burden
        for treated in (False, True):
            css = trametinib_css if treated else 0.0
            name = f"{'debulked' if debulked else 'intact'}_{'trametinib' if treated else 'untreated'}"
            provenance = {**base_provenance, "debulked": debulked, "treated": treated,
                         "initial_burden": initial_burden}
            arms[name] = (cns_scenarios["trametinib"][0], css, seeding_rates, initial_burden, provenance)
    return arms


# Everything below is illustrative placeholder pharmacology, not a measurement: no canine, and
# no confirmed human, potency/exposure number exists for a CDK4/6 inhibitor in this disease.
# CDK46_MAX_KILL_SWEEP is swept rather than fixed to one value for the same reason
# _PREEXISTING_PROB_SWEEP is: presenting a single chosen potency as if it were the answer would
# mostly reflect that choice, not a finding.
CDK46_ILLUSTRATIVE_IC50_NM = 100.0
CDK46_ILLUSTRATIVE_CSS_NM = 500.0  # ~5x the illustrative IC50; an assumed, not measured, margin
CDK46_MAX_KILL_SWEEP = [0.0, 0.02, 0.05, 0.08, 0.12]

MECHANISM_AGNOSTIC_RATIONALE = (
    "A CDK4/6 inhibitor is modeled as a single scalar (ic50_nM_2/max_kill_2) applied identically "
    "to every clone, rather than per-clone values like the MEK inhibitor -- the premise being "
    "tested is that cyclin D/CDK4/6 sits downstream of, and is shared by, all three modeled "
    "escape routes (a secondary RAS/RAF hit, RTK/PI3K bypass, or reduced MEK-inhibitor binding "
    "all still have to drive the cell cycle through cyclin D/CDK4/6/Rb/E2F to actually divide), "
    "so blocking that node should suppress growth regardless of which upstream route a clone "
    "used, unlike the MEK inhibitor itself, which each escape route was specifically built to "
    "evade. This is a real, published rationale for MEK+CDK4/6 combination therapy in RAS/RAF-"
    "mutant human cancers (adaptive resistance to MEK inhibitors commonly proceeds through "
    "cyclin D1 upregulation and CDK4/6 dependence). Palbociclib specifically has real, published "
    "in vitro efficacy against canine histiocytic disease cell lines -- localized HS, "
    "disseminated HS, systemic histiocytosis, and Langerhans cell histiocytosis all showed "
    "growth inhibition, with significant activity also demonstrated in a disseminated-HS mouse "
    "xenograft model (Hirabayashi et al. 2022, Vet Comp Oncol 20(3):587-601) -- real evidence "
    "this drug class works on this cell type, though no canine dosing/toxicity study "
    "accompanied it and no specific IC50 was extracted from that paper for this module. See "
    "TOXICITY_EXTRAPOLATION_NOTE and combination_toxicity_demo for what is and isn't known "
    "about combined-regimen safety."
)


DIVISION_OF_LABOR_NOTE = (
    "Combination and CDK4/6i monotherapy are not interchangeable at the same potency, and the "
    "reason is visible directly in the model's own parameters. Trametinib's job is suppressing "
    "the *bulk* tumor: the sensitive clone's net growth under trametinib alone is already "
    "strongly negative (growth 0.06/day minus its 0.18/day kill = -0.12/day). The three "
    "resistant clones trametinib can't touch have much smaller growth margins (0.02-0.043/day), "
    "so a modest additional CDK4/6i kill-rate is enough to tip all of them negative too -- that "
    "is the combination's job: mopping up what's already nearly suppressed. CDK4/6i "
    "monotherapy has no help on the bulk tumor, so it must single-handedly beat the sensitive "
    "clone's own growth rate (0.06/day) before it does anything -- a higher potency bar than "
    "combination needs (roughly 0.06-0.08 vs. roughly 0.05 in testing). Practically: combination "
    "reaches full suppression at a lower required CDK4/6i dose than monotherapy would, which "
    "matters because CDK4/6 inhibitors carry their own dose-limiting toxicity (myelosuppression "
    "in human use) -- the combination's advantage here is dose-sparing the less-characterized "
    "drug, not a mechanistic requirement that both drugs be present."
)

# Real combination-trial dose-finding practice: even with non-overlapping toxicity organ
# systems, Phase I/Ib combination trials commonly still de-escalate BOTH agents below their
# single-agent MTDs when starting a combination, reflecting patient-level cumulative burden
# beyond any one organ system -- a general, well-documented empirical pattern in combination
# oncology trial design, not a number measured for this specific drug pair. Swept, not fixed,
# for the same reason every other genuinely unknown quantity in this module is swept.
# NOTE: this applies ONE factor to every agent, which is right only for agents whose
# dose-limiting toxicities sit in different organ systems. For two agents blocking the SAME
# pathway (e.g. a MEK inhibitor plus an ERK inhibitor) their on-target toxicities coincide and a
# uniform factor FLATTERS the combination -- see
# `four_open_questions_answered.Q1_SHARED_AXIS_TOXICITY`, which splits it into a shared-axis and an
# independent-axis factor and finds the vertical+parallel regimen far more fragile than this
# constant implies (0.73 at shared 0.6; 0.44 at shared 0.5, i.e. worse than no third agent at all).
COMBINED_EXPOSURE_DERATING = [1.0, 0.8, 0.6, 0.4]

TOXICITY_EXTRAPOLATION_NOTE = (
    "Trametinib's canine dose-limiting toxicities are vascular/hepatic (hypertension, "
    "proteinuria, elevated ALP; Takada et al. 2024). CDK4/6 inhibitors' dose-limiting toxicity "
    "in human use is neutropenia -- an on-target, mechanism-driven effect (CDK4/6 inhibition "
    "halts proliferation of any rapidly dividing cell, including marrow progenitors), not an "
    "idiosyncratic host reaction, so extrapolating this specific toxicity to dogs is reasonable "
    "even without canine-specific confirmation: the same cell-cycle machinery is being blocked "
    "regardless of species. These are different organ systems -- the standard rationale for why "
    "combinations are often feasible near full dose -- but real combination Phase I/Ib trials "
    "still typically de-escalate both agents below their single-agent MTDs when starting out, "
    "reflecting patient-level cumulative burden beyond any one organ system. "
    "COMBINED_EXPOSURE_DERATING applies that possibility to both css_reference and "
    "css_reference_2 simultaneously (see combination_toxicity_demo), to test whether the "
    "combination's benefit survives realistic dose reduction rather than silently assuming "
    "full, unconstrained dosing of both drugs holds."
)


def combination_scenarios(breed: str = "bmd", debulking_fraction: float = DEBULKING_FRACTION,
                          max_kill_2_values: list[float] = CDK46_MAX_KILL_SWEEP,
                          location_penetration_multiplier: float = 1.0,
                          trametinib_active: bool = True,
                          ) -> dict[float, tuple[ResistanceModel, float, np.ndarray, float, dict]]:
    """Trametinib (debulked CNS context) +/- a swept-potency mechanism-agnostic CDK4/6 inhibitor.

    `trametinib_active=False` zeroes trametinib's reference concentration, isolating CDK4/6i as
    monotherapy -- see DIVISION_OF_LABOR_NOTE for why that needs meaningfully higher potency to
    reach the same endpoint as the combination.

    max_kill_2=0.0 leaves ic50_nM_2/max_kill_2 unset (None) rather than setting a zero-effect
    value, so that sweep point is an exact RNG-for-RNG match to the trametinib-only arm -- a
    true null baseline, not just a mathematically-inert-but-differently-perturbed one (setting
    ic50_nM_2 at all, even to a value with no pharmacological effect, still consumes an extra
    random draw in perturb_resistance_model's per-trial jitter).
    """
    arms = localized_pihs_scenarios(breed, debulking_fraction, location_penetration_multiplier)
    model, css, seeding_rates, initial_burden, provenance = arms["debulked_trametinib"]
    if not trametinib_active:
        css = 0.0
    scenarios = {}
    for max_kill_2 in max_kill_2_values:
        if max_kill_2 > 0:
            combo_model = replace(model, ic50_nM_2=CDK46_ILLUSTRATIVE_IC50_NM, max_kill_2=max_kill_2)
        else:
            combo_model = model
        scenarios[max_kill_2] = (combo_model, css, seeding_rates, initial_burden,
                                 {**provenance, "cdk46_max_kill": max_kill_2,
                                  "trametinib_active": trametinib_active})
    return scenarios


# Lomustine (CCNU) as the second agent ------------------------------------------------------
# Built after the CDK4/6-inhibitor arm was shown to be pharmacologically unreachable: a purely
# cytostatic drug cannot exceed a clone's own growth rate (pharmacology.cytostatic_ceiling), which
# rules out max_kill_2 >= 0.05 for this model's clones on mechanism alone, at any dose. Lomustine is
# the natural replacement and is a better-evidenced choice on three independent counts, all real:
#   * it is a DNA-alkylating nitrosourea -- genuinely cytotoxic, so the ceiling does not bind;
#   * it has measured single-agent activity in the actual disease and species (46% ORR in canine HS,
#     pharmacology.CCNU_CANINE_HS) rather than in a proxy lineage;
#   * it is CNS-penetrant, which addresses the ~15%-of-plasma brain exposure problem that is the
#     worst structural weakness of the MEK inhibitor in the primary-CNS presentation.
# A scalar (mechanism-agnostic) max_kill_2 is the *correct* modeling choice here, unlike for the
# CSF1R inhibitor: DNA crosslinking acts downstream-independently, so it does not care which MAPK
# node a resistant clone acquired, and there is no pathway-serial de-rating to apply.
# What it buys in mechanism it gives back in duration -- see CCNU_EXPOSURE_DAYS.
CCNU_DOSE_MG_PER_M2 = 70.0                # mid-range of the real 60-90 mg/m2 canine HS dosing
CCNU_CYCLE_INTERVAL_DAYS = 21             # real q3wk schedule
# Derived from the real cumulative-hepatotoxicity threshold via
# pharmacology.cumulative_dose_limited_days(70, 21, 350) -> 5 cycles, 105 days. This is the whole
# point of modeling lomustine rather than asserting a chronic cytotoxic: the exposure window is
# finite for a documented physiological reason, so the engine's css_reference_2_duration_days is
# populated from real toxicity data instead of being left at None (always-on).
CCNU_EXPOSURE_DAYS = 105
# Deliberately identical to the CDK4/6i arm's values so the two arms differ *only* in mechanism
# class and exposure duration. No lomustine IC50 exists for any canine HS cell line, so matching
# them is not a claim about lomustine's potency -- it holds the saturation term constant to isolate
# the two things that are actually evidenced as different.
CCNU_MATCHED_IC50_NM = CDK46_ILLUSTRATIVE_IC50_NM
CCNU_MATCHED_CSS_NM = CDK46_ILLUSTRATIVE_CSS_NM
# Swept above the cytostatic ceiling on purpose: 0.08 and 0.12 exceed every clone's growth rate and
# are therefore meaningless for a cytostatic drug but legitimate for a cytotoxic one.
CCNU_MAX_KILL_SWEEP = [0.0, 0.05, 0.08, 0.12, 0.20]


def ccnu_combination_scenarios(breed: str = "bmd", debulking_fraction: float = DEBULKING_FRACTION,
                               max_kill_2_values: list[float] = CCNU_MAX_KILL_SWEEP,
                               location_penetration_multiplier: float = 1.0,
                               exposure_days: int | None = CCNU_EXPOSURE_DAYS,
                               ) -> dict[float, tuple[ResistanceModel, float, np.ndarray, float, dict]]:
    """Trametinib (debulked CNS context) +/- lomustine, a real, cytotoxic, duration-capped partner.

    Structurally identical to `combination_scenarios` except that the second drug's exposure stops
    after `exposure_days` (default `CCNU_EXPOSURE_DAYS`, derived from the real cumulative-dose
    toxicity threshold). Pass `exposure_days=None` to model a counterfactual chronic cytotoxic --
    useful only to isolate how much of the outcome depends on the duration cap, since no such drug
    exists in this class.

    The returned provenance records `exposure_days` and the mechanism class so downstream reports
    cannot silently reuse a cytostatic-ceiling interpretation on a cytotoxic arm.
    """
    arms = localized_pihs_scenarios(breed, debulking_fraction, location_penetration_multiplier)
    model, css, seeding_rates, initial_burden, provenance = arms["debulked_trametinib"]
    scenarios = {}
    for max_kill_2 in max_kill_2_values:
        if max_kill_2 > 0:
            combo_model = replace(model, ic50_nM_2=CCNU_MATCHED_IC50_NM, max_kill_2=max_kill_2)
        else:
            combo_model = model
        scenarios[max_kill_2] = (combo_model, css, seeding_rates, initial_burden,
                                 {**provenance, "ccnu_max_kill": max_kill_2,
                                  "second_drug": "lomustine (CCNU)",
                                  "second_drug_mechanism_class": "cytotoxic",
                                  "second_drug_exposure_days": exposure_days,
                                  "cytostatic_ceiling_applies": False})
    return scenarios


# "Durable response" everywhere else in this module means only "no detected relapse within
# whatever horizon_days that specific run used" -- typically 730 days (2 years). It is not a
# claim of permanence, and testing at longer horizons shows it is not flat: the combination
# slows the pathway_reactivation escape route (its net growth margin goes from clearly positive
# without CDK4/6i to only slightly negative with it, in this parameterization) rather than
# eliminating it, so per-trial parameter variability lets a slowly growing minority cross the
# detection threshold given enough years. DURABILITY_HORIZON_SWEEP makes that horizon-dependence
# an explicit, checkable output instead of an unstated assumption baked into a fixed 2-year run.
DURABILITY_HORIZON_SWEEP = [365, 730, 1825, 3650]  # 1, 2, 5, 10 years


# mRNA vaccine follow-on --------------------------------------------------------------------
# Real precedent for a shared/hotspot-mutation-targeted ("off-the-shelf", not fully personalized)
# mRNA cancer vaccine: mRNA-5671 (Moderna/Merck), a Phase 1 lipid-nanoparticle vaccine targeting
# four frequent KRAS mutations (G12D, G13D, G12C, G12V) as monotherapy or with pembrolizumab, in
# KRAS-mutant NSCLC/CRC/pancreatic cancer; and a KRAS G12V-specific mRNA vaccine + pembrolizumab
# combination reporting clinical benefit in advanced solid tumors (Cell Research 2024). This
# PIHS's own PTPN11/KRAS hotspot mutations, if confirmed present (unverified -- see
# canine_cns_hs_scenarios), would be the same kind of small, recurrent, shareable target: this is
# what makes a vaccine plausible without per-patient neoantigen sequencing/manufacture, unlike a
# fully personalized vaccine, which would be impractical for a rare veterinary disease.
VACCINE_PRECEDENT_NOTE = (
    "Shared/hotspot-mutation mRNA vaccines are a real, active human-oncology approach, not "
    "something this module invents: mRNA-5671 targets four recurrent KRAS mutations "
    "(G12D/G13D/G12C/G12V) as monotherapy or with pembrolizumab (Phase 1, KRAS-mutant NSCLC/CRC/"
    "pancreatic cancer); a KRAS G12V-specific mRNA vaccine plus pembrolizumab reported clinical "
    "benefit in advanced solid tumors (Cell Research 2024). No canine cancer vaccine trial of "
    "any kind was found for this disease -- everything below is this module's own extension of "
    "that human precedent onto PIHS's own (unconfirmed) PTPN11/KRAS driver hypothesis."
)

ANTIGEN_PERSISTENCE_NOTE = (
    "None of this module's three drug-resistance escape mechanisms requires losing the driver-"
    "mutation antigen a vaccine would target: pathway_reactivation adds a secondary RAS/RAF hit "
    "on top of the original mutation, rtk_bypass reactivates parallel signaling around it, and "
    "target_site_mutation only changes the MEK-inhibitor binding site -- all three keep "
    "expressing the original PTPN11/KRAS hotspot peptide. A vaccine targeting that hotspot should "
    "therefore still recognize cells using any of those three routes; only a genuinely new, "
    "separate antigen-loss/immune-evasion event (the immune_escape clone modeled here) would "
    "evade it. This is why the model adds a 5th clone rather than assuming the existing three "
    "drug-resistance mechanisms already confer vaccine resistance."
)

DENDRITIC_CELL_VACCINE_CAVEAT = (
    "PIHS is itself a tumor of dendritic cells -- the same lineage that antigen presentation "
    "(and therefore vaccine efficacy) depends on. This is worth flagging as an open biological "
    "question, not dismissing: however, it is the patient's normal, non-malignant dendritic "
    "cells (and other professional antigen-presenting cells) that would actually process and "
    "present the vaccine antigen to T cells, not the malignant clone itself, which only partially "
    "-- not fully -- allays the concern, since it is not established whether malignant "
    "transformation of this lineage locally impairs normal antigen presentation nearby (e.g. via "
    "local immunosuppression). A human primary CNS HS case report noted PD-L1/PD-L2 expression "
    "on tumor cells, consistent with a broader T-cell-exhaustion phenotype that could blunt "
    "vaccine-induced killing independent of antigen loss -- not modeled explicitly here, and a "
    "reason a checkpoint-inhibitor combination (as in the real KRAS G12V vaccine + pembrolizumab "
    "trial above) might matter for this application specifically, not just as a generic add-on."
)

# --- CSF1R inhibitor: a pathway-SERIAL second drug, not a mechanism-agnostic one ---------------
#
# Motivated by `histiocytic_origin`'s tissue-resident-macrophage hypothesis, which nominates CSF1R
# as a candidate driver/dependency for primary CNS and pulmonary HS specifically, and
# pexidartinib as a real, FDA-approved, BBB-penetrant agent against it. Adding it here is NOT a
# straightforward swap for the CDK4/6 inhibitor, and the reason is the whole point:
#
# CSF1R sits at the TOP of the same serial cascade the resistance lesions live on:
#     CSF1R -> SHP2/PTPN11 -> RAS (KRAS/NRAS) -> RAF (BRAF) -> MEK (MAP2K1) -> ERK
# Every resistance mechanism this module models, and every Tier A/B candidate driver in
# `histiocytic_origin.CANDIDATE_DRIVERS`, is constitutively active *downstream* of the receptor.
# A downstream activating lesion is by definition insensitive to blocking an upstream receptor, so
# a CSF1R inhibitor is predicted to be near-inert against exactly the clones that drive relapse,
# however potent it is against the receptor-dependent bulk population. That is the opposite of
# CDK4/6i's modeled role: the cyclin D/CDK4/6 node sits on a *parallel* axis (cell cycle) and so
# genuinely does not care how upstream signaling was reactivated -- which is why CDK46 is a scalar
# (all clones) and this is a per-clone array.
#
# CSF1R_INHIBITOR_IC50_NM is one of very few REAL potency numbers anywhere in this module:
# pexidartinib's measured CSF1R IC50. Two caveats keep it from being a clean anchor. It is measured
# against HUMAN CSF1R, and `histiocytic_cli`'s own structural triage found dog CSF1R to be the
# least conserved candidate checked (85.3% identity, and by far the lowest human-dog pLDDT
# coherence at 0.21) -- so this is the candidate where cross-species potency transfer is *least*
# assured, not most. And IC50 is not a kill ceiling: max_kill remains swept and unfitted, exactly
# as for CDK4/6i and eBAT.
CSF1R_INHIBITOR_IC50_NM = 20.0   # real: pexidartinib vs. human CSF1R
CSF1R_INHIBITOR_ILLUSTRATIVE_CSS_NM = 100.0  # ~5x IC50; assumed margin, no canine PK exists
CSF1R_MAX_KILL_SWEEP = [0.0, 0.02, 0.05, 0.08, 0.12]

# Fraction of the CSF1R inhibitor's kill rate that still applies to a clone carrying a lesion
# downstream of the receptor. Not zero, because a downstream-mutant clone may retain partial
# dependence on receptor-driven survival input beyond the mutated node -- but small, because the
# defining property of an activating downstream mutation is receptor independence. Illustrative;
# swept via `downstream_escape_fraction` rather than asserted.
CSF1R_DOWNSTREAM_ESCAPE_FRACTION = 0.15

# Pexidartinib depletes essentially all microglia in healthy animals at tolerated doses, which is
# functional in vivo proof of CNS target engagement -- a qualitatively different and stronger
# statement than trametinib's measured 15% brain:plasma ratio (BRAIN_PENETRATION_FRACTION). Modeled
# as full CNS availability, the most favorable defensible reading, and flagged as such: no
# quantitative canine brain:plasma ratio for pexidartinib was found.
CSF1R_INHIBITOR_BRAIN_PENETRATION = 1.0


def csf1r_combination_scenarios(breed: str = "bmd",
                                debulking_fraction: float = DEBULKING_FRACTION,
                                csf1r_max_kill_values: list[float] = CSF1R_MAX_KILL_SWEEP,
                                downstream_escape_fraction: float = CSF1R_DOWNSTREAM_ESCAPE_FRACTION,
                                location_penetration_multiplier: float = 1.0,
                                trametinib_active: bool = True,
                                ) -> dict[float, tuple[ResistanceModel, float, np.ndarray, float, dict]]:
    """MAPK inhibitor +/- a swept-potency CSF1R inhibitor modeled as PATHWAY-SERIAL, i.e. with its
    kill term de-rated to `downstream_escape_fraction` on every clone whose resistance lesion lies
    downstream of the receptor.

    Deliberately parallel in shape to `combination_scenarios` so the two second drugs can be
    compared at matched assumed potency -- which is the only fair comparison, since neither drug's
    max_kill is fitted. The difference between them in that comparison is then attributable to
    pathway topology (serial vs. parallel node) rather than to one having been handed a more
    flattering potency.
    """
    arms = localized_pihs_scenarios(breed, debulking_fraction, location_penetration_multiplier)
    model, css, seeding_rates, initial_burden, provenance = arms["debulked_trametinib"]
    if not trametinib_active:
        css = 0.0
    k = len(model.growth)
    scenarios = {}
    for csf1r_max_kill in csf1r_max_kill_values:
        if csf1r_max_kill > 0:
            # clone 0 (drug-sensitive, receptor-dependent) gets the full kill; every resistant clone
            # carries a downstream lesion and keeps only `downstream_escape_fraction` of it.
            per_clone_max_kill = np.full(k, csf1r_max_kill * downstream_escape_fraction)
            per_clone_max_kill[0] = csf1r_max_kill
            combo = replace(model, ic50_nM_2=CSF1R_INHIBITOR_IC50_NM,
                            max_kill_2=per_clone_max_kill)
        else:
            combo = model
        scenarios[csf1r_max_kill] = (combo, css, seeding_rates, initial_burden,
                                     {**provenance, "csf1r_max_kill": csf1r_max_kill,
                                      "downstream_escape_fraction": downstream_escape_fraction,
                                      "second_drug_topology": "pathway-serial (upstream receptor)"})
    return scenarios


VACCINE_CLONE_NAMES = CLONE_NAMES + ["immune_escape"]

# Illustrative, not measured: no canine cancer vaccine trial exists to time this from.
# vaccine_start_day allows time for post-debulking recovery plus an initial MAPK(+CDK4/6)-
# inhibitor course before layering on a second modality; vaccine_ramp_days reflects general
# T-cell priming/expansion kinetics (a real ~1-3 week immunology timescale), not vaccine- or
# antigen-specific measured data.
VACCINE_START_DAY = 90
VACCINE_RAMP_DAYS = 21
VACCINE_MAX_KILL_SWEEP = [0.0, 0.01, 0.03, 0.05, 0.08]

# Illustrative fitness cost of antigen/MHC-I loss (a real, general immunoediting phenomenon, not
# a number measured for this disease): the immune_escape clone otherwise inherits
# pathway_reactivation's drug susceptibility, reflecting the assumption that an antigen-loss
# variant most plausibly arises from a lineage that already survived MAPK-inhibitor selection,
# rather than arising independently from the drug-sensitive population.
IMMUNE_ESCAPE_GROWTH_PENALTY = 0.85

# Illustrative, not measured: set an order of magnitude below the rarest of the three existing
# acquired-resistance mechanisms (target_site_mutation, weight .05 of _SEEDING_RATE_TOTAL for the
# bmd/systemic-reference spectrum), reflecting that antigen/MHC loss is generally considered a
# rarer route to immune escape than pathway-level drug-resistance mutations, not a fitted value.
IMMUNE_ESCAPE_SEEDING_RATE = _SEEDING_RATE_TOTAL * 0.05 * 0.1


def vaccine_followon_scenarios(breed: str = "bmd", debulking_fraction: float = DEBULKING_FRACTION,
                               cdk46_max_kill: float = 0.05,
                               vaccine_max_kill_values: list[float] = VACCINE_MAX_KILL_SWEEP,
                               location_penetration_multiplier: float = 1.0,
                               ) -> dict[float, tuple[ResistanceModel, float, np.ndarray, float, dict]]:
    """Trametinib + CDK4/6i (fixed at `cdk46_max_kill`, the combination's near-full-suppression
    potency from `combination_control_demo`) plus a swept-potency mRNA vaccine layered on top.

    Builds a 5th clone (`immune_escape`) onto the 4-clone combination model, inheriting
    `pathway_reactivation`'s drug-susceptibility with `IMMUNE_ESCAPE_GROWTH_PENALTY` applied --
    see the module-level notes above for why. `vaccine_max_kill=0.0` gives a drug-only baseline
    with the 5th clone present but never seeded before `VACCINE_START_DAY` and never subject to
    vaccine kill (the mask always excludes it) -- i.e. behaviorally identical to the 4-clone
    combination model, just carried in a 5-wide state vector for a consistent comparison.
    """
    combo_scenarios = combination_scenarios(breed, debulking_fraction, [cdk46_max_kill],
                                            location_penetration_multiplier)
    model, css, seeding_rates, initial_burden, provenance = combo_scenarios[cdk46_max_kill]
    escape_growth = model.growth[1] * IMMUNE_ESCAPE_GROWTH_PENALTY
    model5 = ResistanceModel(
        growth=np.append(model.growth, escape_growth),
        ic50_nM=np.append(model.ic50_nM, model.ic50_nM[1]),
        max_kill=np.append(model.max_kill, model.max_kill[1]),
        mutation=np.eye(len(model.growth) + 1),
        hill=model.hill, carrying_capacity=model.carrying_capacity,
        ic50_nM_2=model.ic50_nM_2, max_kill_2=model.max_kill_2, hill_2=model.hill_2,
    )
    scenarios = {}
    for vaccine_max_kill in vaccine_max_kill_values:
        scenarios[vaccine_max_kill] = (model5, css, seeding_rates, initial_burden, {
            **provenance, "vaccine_max_kill": vaccine_max_kill,
            "vaccine_start_day": VACCINE_START_DAY, "vaccine_ramp_days": VACCINE_RAMP_DAYS,
            "immune_escape_seeding_rate": IMMUNE_ESCAPE_SEEDING_RATE,
            "immune_escape_growth_penalty": IMMUNE_ESCAPE_GROWTH_PENALTY,
        })
    return scenarios


# Concrete vaccine antigen design ---------------------------------------------------------------
# Formalizes "what the vaccine actually is" as three synthetic long-peptide antigens (mirroring
# the real mRNA-5671 multi-epitope design pattern) built fresh from each gene's actual canine
# AlphaFold/UniProt sequence -- not hardcoded strings. See dla_binding module docstring for what
# is and isn't a real, existing tool for the binding-prediction check built on top of this.
VACCINE_ANTIGEN_TARGETS = [
    {"gene": "PTPN11", "position": 76, "wt_residue": "E", "mut_residue": "K",
     "mutation_label": "PTPN11 p.E76K",
     "domain_context": "N-SH2 domain -- disrupts the autoinhibitory N-SH2/PTP interface, the "
                       "canonical activating mechanism for this hotspot"},
    {"gene": "PTPN11", "position": 503, "wt_residue": "G", "mut_residue": "V",
     "mutation_label": "PTPN11 p.G503V", "domain_context": "PTP catalytic domain"},
    {"gene": "KRAS", "position": 61, "wt_residue": "Q", "mut_residue": "H",
     "mutation_label": "KRAS p.Q61H",
     "domain_context": "switch II region -- impairs intrinsic and GAP-stimulated GTP hydrolysis, "
                       "the canonical RAS-activating mechanism for this hotspot"},
]

VACCINE_ANTIGEN_FLANK = 12  # 25-mer peptides, matching mRNA-5671's synthetic long-peptide design


def vaccine_antigen_peptides(structure_cache: Path) -> dict[str, str]:
    """Fetches the real canine AlphaFold structures for PTPN11 and KRAS (via UniProt accession
    resolution) and builds the mutant 25-mer peptide for each `VACCINE_ANTIGEN_TARGETS` entry.

    Built fresh from the actual structure-derived sequence each call (with a hard wild-type-
    residue check in `extract_mutant_peptide`), not hardcoded, so it stays correct if either
    database is ever revised. Requires network access; structures are cached under
    `structure_cache` so repeated calls for the same gene reuse the download.
    """
    peptides = {}
    tracks = {}
    for target in VACCINE_ANTIGEN_TARGETS:
        gene = target["gene"]
        if gene not in tracks:
            accession = resolve_uniprot_accession(gene, DOG_TAXID)
            struct = download_structure(accession, structure_cache / gene)
            tracks[gene] = read_plddt_track(struct)
        peptides[target["mutation_label"]] = extract_mutant_peptide(
            tracks[gene], target["position"], target["wt_residue"], target["mut_residue"],
            flank=VACCINE_ANTIGEN_FLANK)
    return peptides


# Localized pulmonary histiocytic sarcoma ------------------------------
# A real, independently-described HS presentation, distinct from PIHS above: a
# case series of localized pulmonary HS (Sakai et al. 2015, J Vet Med Sci 77(12):1667-1670, PMID
# 26155931). Two things are concretely different from the PIHS scenarios and worth modeling
# rather than reusing those numbers unchanged: (1) lung tissue has no blood-brain-barrier-type
# restriction, so drug reaches it at full systemic concentration, not the 15% brain-penetration
# fraction used above -- verified (clone_growth_margins) that this alone does not close the
# same two-of-three-clones-still-positive-margin gap found in the PIHS scenarios, since those
# clones resist trametinib via a capped maximum kill rate, not merely insufficient concentration;
# (2) unlike Kishimoto's near-zero-dissemination PIHS cohort, this case series reports regional
# lymph node involvement in many cases, with median survival of only 133 days across all 19 dogs
# -- meaning "debulk the primary, then treat systemically" cannot assume surgery reaches the
# whole disease burden the way it was modeled for PIHS.
PULMONARY_CASE_SERIES = (
    "Sakai et al. 2015, J Vet Med Sci 77(12):1667-1670 (PMID 26155931): 19 dogs of the predisposed breed "
    "with histiocytic sarcoma involving lung and/or regional lymph nodes; median survival 133 "
    "days across the cohort; no prognostic factor examined (including surgical resection status) "
    "reached statistical significance in that small series -- not a claim those factors don't "
    "matter, just that this series was underpowered to detect it."
)

# No precise nodal-involvement rate was reported (the paper describes "many cases", not a
# percentage); swept rather than fixed to one value for the same reason every other genuinely
# unknown parameter in this module is swept.
NODAL_INVOLVEMENT_PROB_SWEEP = [0.0, 0.2, 0.4, 0.6]

# Illustrative: a clinically-detected nodal deposit is unlikely to be a handful of cells (unlike
# the microscopic 1e-6-1e-3 pre-existing-subclone fractions used elsewhere in this module), but
# no measurement of relative nodal-to-primary tumor burden at diagnosis exists for this disease --
# chosen as a round, clinically-plausible "meaningful but still a minority of total burden" value.
NODAL_SEED_FRACTION = 0.1

_PULMONARY_BASELINE_BURDEN = .3  # same illustrative pre-debulking baseline used elsewhere


def pulmonary_hs_scenarios(cdk46_max_kill: float = 0.0, debulking_fraction: float = DEBULKING_FRACTION,
                              nodal_involvement_prob_values: list[float] = NODAL_INVOLVEMENT_PROB_SWEEP,
                              ) -> dict[float, tuple[ResistanceModel, float, np.ndarray, float, dict]]:
    """Trametinib (+/- CDK4/6i) at full systemic exposure (no CNS brain-penetration discount) for
    a resectable primary lung mass, swept over how likely regional nodal disease already is.

    Uses `dog_preset`'s baseline mechanism-weight spectrum unchanged -- no presentation-specific germline
    locus exists to justify reweighting it, deliberately, for the same reason
    `canine_cns_hs_scenarios` does not offer a breed option for it: extending real GWAS loci from
    bmd/flat_coated_retriever is a reasonable extrapolation; inventing a presentation-specific one from
    nothing would not be.
    """
    model, systemic_css, seeding_rates, base_provenance = dog_preset()
    if cdk46_max_kill > 0:
        model = replace(model, ic50_nM_2=CDK46_ILLUSTRATIVE_IC50_NM, max_kill_2=cdk46_max_kill)
    scenarios = {}
    for nodal_involvement_prob in nodal_involvement_prob_values:
        provenance = {**base_provenance, "site": "localized pulmonary",
                     "cdk46_max_kill": cdk46_max_kill, "debulking_fraction": debulking_fraction,
                     "nodal_involvement_prob": nodal_involvement_prob,
                     "nodal_seed_fraction": NODAL_SEED_FRACTION,
                     "case_series": PULMONARY_CASE_SERIES}
        scenarios[nodal_involvement_prob] = (model, systemic_css, seeding_rates, debulking_fraction, provenance)
    return scenarios


def pulmonary_full_regimen_scenarios(debulking_fraction: float = DEBULKING_FRACTION,
                                 ccnu_max_kill: float = 0.0,
                                 nodal_involvement_prob_values: list[float] = NODAL_INVOLVEMENT_PROB_SWEEP,
                                 ) -> dict[float, tuple[ResistanceModel, float, np.ndarray, float, dict]]:
    """The localized pulmonary scenario carried in a 5-clone (vaccine-capable) state vector.

    Exists because `pulmonary_hs_scenarios` is 4-clone and therefore cannot express a vaccine at
    all -- which is how the pulmonary arm of `single_patient_demo` came to be built as trametinib
    monotherapy while the whole endurance case rests on the vaccine. This is the pulmonary equivalent of
    `vaccine_followon_scenarios`, built on the pulmonary (full systemic exposure, no brain-penetration
    discount) preset rather than the CNS one, and intended for
    `run_monte_carlo_two_compartment(vaccine_start_day=...)` so the nodal compartment surgery cannot
    reach is still exposed to both the systemic drug and the systemic immune mechanism.

    `ccnu_max_kill > 0` adds lomustine as the second drug (real activity in canine HS, cytotoxic, and
    CNS/tissue-penetrant); pair it with `css_reference_2_duration_days=CCNU_EXPOSURE_DAYS` at the call
    site so its real cumulative-dose cap is respected rather than modeling chronic dosing.

    The 5th clone inherits `pathway_reactivation`'s drug susceptibility with
    `IMMUNE_ESCAPE_GROWTH_PENALTY` applied, matching `vaccine_followon_scenarios` exactly -- the same
    illustrative, labeled assumption, not a presentation-specific measurement (none exists).
    """
    model, systemic_css, seeding_rates, base_provenance = dog_preset()
    escape_growth = model.growth[1] * IMMUNE_ESCAPE_GROWTH_PENALTY
    model5 = ResistanceModel(
        growth=np.append(model.growth, escape_growth),
        ic50_nM=np.append(model.ic50_nM, model.ic50_nM[1]),
        max_kill=np.append(model.max_kill, model.max_kill[1]),
        mutation=np.eye(len(model.growth) + 1),
        hill=model.hill, carrying_capacity=model.carrying_capacity,
    )
    if ccnu_max_kill > 0:
        model5 = replace(model5, ic50_nM_2=CCNU_MATCHED_IC50_NM, max_kill_2=ccnu_max_kill)
    scenarios = {}
    for nodal_involvement_prob in nodal_involvement_prob_values:
        scenarios[nodal_involvement_prob] = (model5, systemic_css, seeding_rates, debulking_fraction, {
            **base_provenance, "site": "localized pulmonary, 5-clone vaccine-capable",
            "debulking_fraction": debulking_fraction,
            "nodal_involvement_prob": nodal_involvement_prob,
            "nodal_seed_fraction": NODAL_SEED_FRACTION,
            "ccnu_max_kill": ccnu_max_kill,
            "second_drug": "lomustine (CCNU)" if ccnu_max_kill > 0 else None,
            "second_drug_exposure_days": CCNU_EXPOSURE_DAYS if ccnu_max_kill > 0 else None,
            "vaccine_start_day": VACCINE_START_DAY, "vaccine_ramp_days": VACCINE_RAMP_DAYS,
            "immune_escape_seeding_rate": IMMUNE_ESCAPE_SEEDING_RATE,
            "immune_escape_growth_penalty": IMMUNE_ESCAPE_GROWTH_PENALTY,
            "case_series": PULMONARY_CASE_SERIES,
        })
    return scenarios


# Primary intracranial HS (Kishimoto et al. 2020), as the vaccine-capable counterpart to
# `pulmonary_full_regimen_scenarios`. Two things differ from the pulmonary construct, and they pull in
# opposite directions:
#
#   1. Drug exposure is cut to trametinib's real 15% brain:plasma ratio. This is the obvious
#      disadvantage -- and `clone_growth_margins` shows it is almost entirely confined to the
#      SENSITIVE clone (margin -0.114 -> -0.051, still strongly negative). The resistant clones
#      barely move (pathway_reactivation +0.0480 -> +0.0499, target_site_mutation +0.0572 ->
#      +0.0579), because they resist via a capped maximum kill rate rather than via insufficient
#      concentration. The BBB therefore withholds drug from the clone the drug was already killing
#      and withholds almost nothing from the clones that actually cause relapse.
#   2. No nodal compartment. Kishimoto's cohort was 100% cerebral with no dissemination, so the
#      compartment surgery cannot reach -- the pulmonary case's central problem, and the reason
#      `run_monte_carlo_two_compartment` exists -- is simply absent here.
#
# The consequence that matters for the endurance question: because
# `antigen_convergence.vaccine_potency_threshold` is computed from the fastest covered clone's
# GROWTH rate and not from drug exposure, the required vaccine potency is IDENTICAL at both sites
# (0.060/day). The blood-brain barrier does not raise the vaccine's bar. It lowers the backbone
# drug's contribution to holding the line before the vaccine arrives.
CNS_CASE_SERIES = (
    "Kishimoto et al. 2020, J Vet Med Sci 82(1):77-83 (University of Tokyo, 186 intracranial "
    "tumors, 9,270 dogs): predisposed dog breed accounted for 10 of 20 primary intracranial "
    "histiocytic sarcoma cases, odds ratio 21.5 (95% CI 8.9-51.8, P<0.001). Of the 16 PIHS cases "
    "with known location, 100% were cerebral (temporal 25.0%, frontal 18.8%, parietal and "
    "occipital 12.5% each, 31.3% diffuse); zero cerebellar or brainstem. Histopathology and "
    "epidemiology only -- this paper reports no mutation data, and no canine study has sequenced "
    "PIHS."
)

# Kishimoto's cohort showed no dissemination, unlike the pulmonary series' frequent regional nodal
# involvement. Modeled as a genuine zero rather than swept: this is the one place the two
# presentations differ in a direction that is actually reported, not assumed.
CNS_NODAL_INVOLVEMENT_PROB = 0.0


def cns_full_regimen_scenarios(debulking_fraction: float = DEBULKING_FRACTION,
                                ccnu_max_kill: float = 0.0,
                                reference_drug: str = "trametinib",
                                location_penetration_multiplier: float = 1.0,
                                ) -> tuple[ResistanceModel, float, np.ndarray, float, dict]:
    """The primary intracranial scenario in the same 5-clone vaccine-capable state vector as
    `pulmonary_full_regimen_scenarios`, so the two disease sites can be compared arm for arm.

    Returns a single scenario rather than a nodal-probability-keyed dict, because the nodal sweep
    the pulmonary version needs has nothing to sweep here (see `CNS_NODAL_INVOLVEMENT_PROB`).

    Carries every extrapolation `canine_cns_hs_scenarios` already carries -- the systemic
    PTPN11/KRAS driver spectrum is assumed to hold intracranially with no canine CNS sequencing to
    confirm it, and the brain-penetration fraction is trametinib's own measurement applied to
    potency numbers measured from cobimetinib -- plus one more specific to the vaccine arm: whether
    an antigen-specific T-cell response reaches an intracranial tumor at the same effective kill
    rate it would reach a pulmonary one is NOT modeled here as a discount, because no measurement
    exists to set one. The relevant real biology is that activated effector T-cells cross the
    blood-brain barrier as a function of their activation state rather than their antigen
    specificity, so the vaccine's mechanism is far less BBB-restricted than a P-gp/BCRP-effluxed
    small molecule -- but "far less restricted" is not "unrestricted", and treating it as 1.0 here
    is an assumption, not a finding. Sweep it at the call site to test it.

    A second, more specific real finding sharpens that same caveat rather than resolving it: this
    tumor is not merely intracranial, it is anatomically concentrated (Kishimoto et al. 2020 --
    100% cerebral, temporal 25.0% / frontal 18.8% / parietal 12.5% / occipital 12.5% / diffuse
    31.3%, ZERO cerebellar or brainstem). Real human dural anatomy shows meningeal lymphatic
    vessels are NOT uniform across the skull: they are widely distributed but smaller in caliber
    over the dorsal cerebral convexity -- exactly where temporal/frontal/parietal/occipital sit --
    than at the skull base and craniocervical junction (Vera Quesada et al. 2023, Front Cell Dev
    Biol, human cadaveric dura). Separately, real mouse glioma/melanoma-brain-tumor work shows
    these DORSAL meningeal lymphatics are not passive plumbing: disrupting them measurably reduces
    dendritic-cell trafficking to cervical lymph nodes and significantly reduces anti-PD-1/CTLA-4
    checkpoint immunotherapy efficacy, while boosting dorsal lymphangiogenesis (VEGF-C) improves it
    via the CCL21/CCR7 axis (Hu et al. 2020, Cell Res 30(3):229-243, PMID 32094452). So the exact anatomic
    compartment this tumor occupies is the one a real, functional, immunotherapy-relevant drainage
    pathway has been shown to run through -- which argument this cuts in favor of is NOT resolvable
    from what exists: smaller vessel caliber at the convexity could mean weaker drainage there
    specifically, or the mouse disruption experiments could mean this pathway functions
    perfectly well in an intact system regardless of caliber. No study has directly compared
    convexity-vs-basal tumors on this axis, and no canine meningeal lymphatic anatomy has been
    published at all. Recorded as a sharper, better-cited version of the same "no measurement
    exists to set a discount" caveat above, not as a resolution of it.
    """
    model, systemic_css, seeding_rates, base_provenance = dog_preset()
    if reference_drug not in BRAIN_PENETRATION_FRACTION:
        raise ValueError(f"unknown reference drug {reference_drug!r}; known: "
                         f"{sorted(BRAIN_PENETRATION_FRACTION)}")
    penetration = BRAIN_PENETRATION_FRACTION[reference_drug] * location_penetration_multiplier
    escape_growth = model.growth[1] * IMMUNE_ESCAPE_GROWTH_PENALTY
    model5 = ResistanceModel(
        growth=np.append(model.growth, escape_growth),
        ic50_nM=np.append(model.ic50_nM, model.ic50_nM[1]),
        max_kill=np.append(model.max_kill, model.max_kill[1]),
        mutation=np.eye(len(model.growth) + 1),
        hill=model.hill, carrying_capacity=model.carrying_capacity,
    )
    if ccnu_max_kill > 0:
        model5 = replace(model5, ic50_nM_2=CCNU_MATCHED_IC50_NM, max_kill_2=ccnu_max_kill)
    provenance = {
        **base_provenance, "site": "primary intracranial, 5-clone vaccine-capable",
        "debulking_fraction": debulking_fraction,
        "nodal_involvement_prob": CNS_NODAL_INVOLVEMENT_PROB,
        "brain_penetration_reference_drug": reference_drug,
        "brain_penetration_fraction": penetration,
        "ccnu_max_kill": ccnu_max_kill,
        "vaccine_start_day": VACCINE_START_DAY, "vaccine_ramp_days": VACCINE_RAMP_DAYS,
        "immune_escape_seeding_rate": IMMUNE_ESCAPE_SEEDING_RATE,
        "immune_escape_growth_penalty": IMMUNE_ESCAPE_GROWTH_PENALTY,
        "case_series": CNS_CASE_SERIES,
        "dendritic_cell_origin": DENDRITIC_CELL_ORIGIN_NOTE,
    }
    return model5, systemic_css * penetration, seeding_rates, debulking_fraction, provenance


def dog_preset() -> tuple[ResistanceModel, float, np.ndarray, dict]:
    """Cobimetinib vs. canine PTPN11/KRAS-mutant HS; sensitive-clone IC50 and Cmax are real.

    The drug actually in canine clinical development is trametinib, not cobimetinib -- see the
    "clinical_development" provenance field. Cobimetinib is used here because it is the only MEK
    inhibitor with a published cellular IC50 this repo could extract as a clean number: real
    trametinib-specific canine HS potency data DOES exist (Takada et al. 2018, Mol Cancer Ther,
    PMID 30135215 -- confirmed via direct abstract fetch, not assumed absent), including apoptotic
    killing of the exact PTPN11 E76K and KRAS Q61H lines this repo's driver panel targets, but the
    numeric IC50/EC50 values could not be extracted from any source this session's tools could
    reach (see `trametinib_direct_evidence.RETRACTED_CLAIM` for the six access attempts and why one
    of them -- the paper's own open-access supplementary figure -- almost certainly has the real
    numbers behind an unpassable bot-challenge). Converting cobimetinib's IC50 to a trametinib
    estimate would stack an unverified conversion on top of a proxy substance, so this preset does
    not attempt that; see `trametinib_direct_evidence` for what IS confirmed without a number.
    """
    cell_line_ic50_nM = {"BD": 74.0, "OD": 91.0, "DH82": 372.0}
    ic50_sensitive = float(np.mean(list(cell_line_ic50_nM.values())))
    seeding_rates = _SEEDING_RATE_TOTAL * np.array([.85, .10, .05])
    model = ResistanceModel(growth=_SHARED_GROWTH, ic50_nM=ic50_sensitive * _SHARED_IC50_RATIOS,
                            max_kill=_SHARED_MAX_KILL, mutation=_SHARED_MUTATION)
    css_reference = 1640.0
    provenance = {
        "species": "dog", "drug": "cobimetinib (MEK1/2 inhibitor)",
        "calibrated_from_data": {
            "sensitive_clone_ic50_nM": cell_line_ic50_nM,
            "css_reference_nM": "canine plasma Cmax at 5 mg/kg",
        },
        "illustrative_only": ["growth rates", "resistant-clone IC50 shifts and kill ceilings",
                              "seeding rates (loosely tuned to case-report durability, not fit)",
                              "carrying capacity"],
        "citation": "Genes 2024;15(8):1050, PMID 39202410",
        "clinical_development": (
            "Two Phase II trials of trametinib (not cobimetinib) for canine HS are open "
            "(University of Florida; Michigan State University, VCT24005793 per the Veterinary "
            "Clinical Trials Registry), following a "
            "completed Phase I dose-escalation PK/safety study (Takada et al. 2024, Vet Comp "
            "Oncol) that set the recommended dose at 0.5 mg/m^2/day PO (dose-limiting grade 3 "
            "hypertension, proteinuria, lethargy, elevated ALP), reaching a steady-state "
            "concentration of ~10 ng/mL (~16 nM) in ~70% of dogs after ~2 weeks -- a threshold "
            "associated with efficacy in human trials, not derived from canine HS response data."
        ),
    }
    return model, css_reference, seeding_rates, provenance


def human_preset() -> tuple[ResistanceModel, float, np.ndarray, dict]:
    """Same illustrative pharmacodynamic shape; broader resistance-mutation spectrum, no fitted PK."""
    ic50_sensitive = 150.0
    seeding_rates = _SEEDING_RATE_TOTAL * np.array([.40, .35, .25])
    model = ResistanceModel(growth=_SHARED_GROWTH, ic50_nM=ic50_sensitive * _SHARED_IC50_RATIOS,
                            max_kill=_SHARED_MAX_KILL, mutation=_SHARED_MUTATION)
    css_reference = ic50_sensitive * 10
    provenance = {
        "species": "human", "drug": "MEK inhibitor (e.g. trametinib)",
        "calibrated_from_data": {},
        "illustrative_only": [("all pharmacodynamic and pharmacokinetic values in this preset; "
                              "no published human HS in vitro IC50 or Cmax was found; seeding "
                              "rates are loosely tuned to case-report durability, not fit")],
        "resistance_spectrum_rationale": "broader mutation seeding across mechanisms reflects "
            "MAPK-pathway mutations spread across BRAF/MAP2K1/KRAS/NRAS/PTPN11/NF1/CBL in human "
            "HS, versus PTPN11-dominated canine HS",
        "citation": "Mod Pathol. 2019;32(6):830-843 (mutation spectrum); "
                    "N Engl J Med. 2018;378(20):1945-1947, PMID 29768143 (trametinib response)",
    }
    return model, css_reference, seeding_rates, provenance


SPECIES_PRESETS = {"dog": dog_preset, "human": human_preset}
