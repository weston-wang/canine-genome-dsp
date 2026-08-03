import json
from dataclasses import replace
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .alphafold import align_residue_numbers, download_structure, read_plddt_track
from .mapk_resistance import (
    CLONE_NAMES,
    ResistanceModel,
    decompose_patient_uncertainty,
    run_monte_carlo,
    run_monte_carlo_fixed_patient,
    run_monte_carlo_with_vaccine,
)
from .uniprot import DOG_TAXID, HUMAN_TAXID, resolve_uniprot_accession

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


def mapk_cns_demo(out: Path, breed: str = "bmd", trials: int = 300, horizon_days: int = 730,
                  preexisting_prob: float = _PREEXISTING_PROB_CENTRAL,
                  location_penetration_multiplier: float = 1.0, seed: int = 7) -> None:
    out.mkdir(parents=True, exist_ok=True)
    scenarios = canine_cns_hs_scenarios(breed, location_penetration_multiplier)

    rows, outcomes = [], {}
    for drug, (model, css_reference, seeding_rates, provenance) in scenarios.items():
        outcome = run_monte_carlo(model, css_reference, horizon_days, seeding_rates, trials,
                                  preexisting_prob=preexisting_prob, seed=seed)
        outcomes[drug] = outcome
        ttp = outcome.time_to_progression[outcome.progressed]
        rows.append({
            "scenario": drug, "brain_penetration_fraction": BRAIN_PENETRATION_FRACTION[drug],
            "effective_css_nM": css_reference,
            "probability_durable_response": float(1 - outcome.progressed.mean()),
            "probability_progression": float(outcome.progressed.mean()),
            "median_time_to_progression_days": float(np.median(ttp)) if ttp.size else None,
        })
    table = pd.DataFrame(rows)
    table.to_csv(out / "cns_penetration_sensitivity.csv", index=False)

    days = np.arange(horizon_days + 1)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    for drug, outcome in outcomes.items():
        median_burden = np.median(outcome.trajectories.sum(axis=2), axis=0)
        axes[0].plot(days, median_burden, label=f"{drug} (f={BRAIN_PENETRATION_FRACTION[drug]})")
    axes[0].set(xlabel="day", ylabel="median total tumor burden",
               title=f"CNS scenario: breed={breed}, preexisting_prob={preexisting_prob}")
    axes[0].legend(fontsize=8)
    table.plot(x="scenario", y="probability_durable_response", kind="bar", ax=axes[1],
              color="tab:blue", legend=False)
    axes[1].set(ylabel="P(durable response)", title="sensitivity to brain penetration", ylim=(0, 1))
    fig.tight_layout(); fig.savefig(out / "cns_penetration.png", dpi=160); plt.close(fig)

    summary = {
        "breed_context": breed, "preexisting_prob_used": preexisting_prob,
        "location_penetration_multiplier": location_penetration_multiplier,
        "scenarios": rows,
        "location_note": (
            "Rostrotentorial (cerebral) and infratentorial (cerebellar/brainstem) primary CNS "
            "HS are modeled identically here, but the largest breed-and-location-linked series "
            "found (Kishimoto et al. 2020, n=20 PIHS cases, 16 with known location) reports 0 "
            "cerebellar/brainstem cases: 100% were cerebral (temporal 25.0%, frontal 18.8%, "
            "parietal 12.5%, occipital 12.5%, 31.3% diffuse). Toyoda et al. 2020's larger, "
            "multi-institution series does report a real infratentorial minority, so cerebellar "
            "primary CNS HS is not fictional -- just rare wherever it has been counted, and "
            "apparently absent in Kishimoto's single-institution Japanese cohort specifically. "
            "Both locations are still modeled with the same brain_penetration_fraction here: "
            "regional BBB heterogeneity is real and cerebellum is one of the regions recent "
            "profiling calls a differentially specialized compartment, but no quantified "
            "cerebrum-vs-cerebellum comparison was found, so asserting a numeric difference "
            "would be less honest than exposing location_penetration_multiplier for anyone who "
            "wants to test a hypothesis about one."
        ),
        "corgi_pihs_context": (
            "Kishimoto et al. 2020 (J Vet Med Sci 82(1):77-83, University of Tokyo, 186 "
            "intracranial tumors, 9,270 dogs screened) found Pembroke Welsh Corgi carries by "
            "far the strongest breed association of any tumor type in the study: 16 of 422 "
            "Corgis had a primary intracranial tumor, 10 of which were PIHS specifically -- 50% "
            "of all 20 PIHS cases in the cohort, odds ratio 21.5 (95% CI 8.9-51.8, P<0.001). "
            "Combined with the cerebrum-only, temporal/frontal-lobe-predominant localization "
            "above, this is a genuinely striking clinical concentration -- but it is anatomic "
            "and epidemiologic, not molecular: this paper is histopathology/epidemiology only "
            "and reports no PTPN11/KRAS/BRAF mutation data for these or any other CNS cases. "
            "No canine study has sequenced Corgi PIHS specifically. A 'corgi' breed option is "
            "deliberately not offered here (unlike bmd/flat_coated_retriever): those two rest on "
            "published germline GWAS loci this module extrapolates from; Corgi PIHS has no "
            "published germline or somatic locus to extrapolate from at all, so adding one would "
            "be fabricating a number rather than extending a real one."
        ),
        "unverified_extrapolations": [
            ("canine primary CNS HS carries the same PTPN11/KRAS-dominated driver spectrum as "
             "systemic HS -- no canine CNS-specific sequencing exists to confirm this, Corgi "
             "PIHS included"),
            ("the breed-to-mechanism-weight link (bmd vs. flat_coated_retriever) is this "
             "module's own speculative extension of germline GWAS loci to acquired-resistance "
             "mechanisms; no published study connects them"),
            ("cellular potency is still cobimetinib's (dog_preset's proxy drug); the trametinib "
             "and cobimetinib brain-penetration fractions are each drug's own real measurement, "
             "applied here to a potency number measured from cobimetinib specifically"),
        ],
        "citations": {
            "location_and_breed_clinicopathology": "Kishimoto et al. 2020, J Vet Med Sci "
                "82(1):77-83 (n=20 PIHS, breed table); Toyoda et al. 2020, J Vet Intern Med "
                "34(2):828-837 (n=102 CNS HS, primary vs. disseminated comparison)",
            "bmd_germline_locus": "CFA11 MTAP/CDKN2A haplotype GWAS, 96% of affected BMDs",
            "flat_coated_retriever_germline_loci": "CFA5 (PIK3R6) and CFA19 GWAS loci",
            "brain_penetration_fractions": "trametinib ~15%, cobimetinib ~2.7% brain-to-plasma "
                "ratio; P-gp/BCRP-limited (melanoma brain-metastasis CNS-distribution literature)",
            "cns_undertreatment_precedent": "Erdheim-Chester disease (a related MAPK-driven "
                "histiocytic neoplasm): single-agent BRAF inhibitor can under-control CNS "
                "lesions despite systemic response; adding a MEK inhibitor rescued CNS "
                "responses in a small case series",
        },
        "warning": (
            "Doubly speculative relative to mapk_resistance_demo's systemic model: this "
            "extrapolates both the driver-mutation spectrum and the treatment response into a "
            "disease site and cell population that has never been directly studied in dogs. "
            "Read this as a structured hypothesis meant to motivate real CNS-specific canine "
            "sequencing and PK work, not as a prediction of how a dog with CNS HS will respond."
        ),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


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
    "included here as this module's own candidate-gene hypothesis for what a Corgi germline "
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
    "al. 2010; Skorupski et al. 2007) -- though that cohort's CNS-specific fraction is not "
    "confirmed, so this is a suggestive, not a location-matched, benchmark. A single CNS-specific "
    "case report (frontal-lobe PIHS, surgical resection plus low-dose CCNU) survived "
    "recurrence-free past one year. DEBULKING_FRACTION substitutes a MAPK inhibitor "
    "(trametinib, the real canine trial drug) for CCNU as the adjuvant in this scenario."
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


def localized_control_demo(out: Path, breed: str = "bmd", debulking_fraction: float = DEBULKING_FRACTION,
                           trials: int = 300, horizon_days: int = 730,
                           preexisting_prob: float = _PREEXISTING_PROB_CENTRAL,
                           location_penetration_multiplier: float = 1.0, seed: int = 7) -> None:
    out.mkdir(parents=True, exist_ok=True)
    arms = localized_pihs_scenarios(breed, debulking_fraction, location_penetration_multiplier)

    rows, outcomes = [], {}
    for name, (model, css, seeding_rates, initial_burden, _) in arms.items():
        outcome = run_monte_carlo(model, css, horizon_days, seeding_rates, trials,
                                  preexisting_prob=preexisting_prob, initial_burden=initial_burden,
                                  seed=seed)
        outcomes[name] = outcome
        ttp = outcome.time_to_progression[outcome.progressed]
        mechanism_counts = pd.Series(outcome.dominant_mechanism).value_counts()
        mechanism_fractions = (mechanism_counts.reindex(["durable_response"] + CLONE_NAMES[1:], fill_value=0)
                              / len(outcome.dominant_mechanism))
        rows.append({
            "arm": name, "initial_burden": initial_burden, "effective_css_nM": css,
            "probability_durable_response": float(1 - outcome.progressed.mean()),
            "probability_progression": float(outcome.progressed.mean()),
            "median_time_to_progression_days": float(np.median(ttp)) if ttp.size else None,
            **{f"mechanism_{mechanism}": float(value) for mechanism, value in mechanism_fractions.items()},
        })
    table = pd.DataFrame(rows)
    table.to_csv(out / "localized_control_arms.csv", index=False)

    days = np.arange(horizon_days + 1)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    for name, outcome in outcomes.items():
        median_burden = np.median(outcome.trajectories.sum(axis=2), axis=0)
        axes[0].plot(days, median_burden, label=name)
    axes[0].set(xlabel="day", ylabel="median total tumor burden",
               title=f"debulking x trametinib: breed={breed}")
    axes[0].legend(fontsize=7)
    table.plot(x="arm", y="probability_durable_response", kind="bar", ax=axes[1],
              color="tab:blue", legend=False)
    axes[1].set(ylabel="P(durable response)", title="four-arm comparison", ylim=(0, 1))
    axes[1].tick_params(axis="x", rotation=30)
    fig.tight_layout(); fig.savefig(out / "localized_control.png", dpi=160); plt.close(fig)

    summary = {
        "breed_context": breed, "debulking_fraction": debulking_fraction,
        "preexisting_prob_used": preexisting_prob, "arms": rows,
        "dendritic_cell_origin_hypothesis": DENDRITIC_CELL_ORIGIN_NOTE,
        "localized_therapy_precedent": LOCALIZED_THERAPY_PRECEDENT,
        "reasoning_chain": [
            ("Kishimoto et al. 2020: Corgi accounts for 50% of all PIHS cases (OR 21.5), and "
             "100% of location-known PIHS cases were cerebral -- an anatomic/breed concentration "
             "on the same order as BMD's known germline-driven systemic-HS association."),
            ("That magnitude of concentration in a closed breed population is the signature of "
             "an as-yet-unidentified, high-frequency germline variant (geneticist's reading); no "
             "GWAS has been done for Corgi PIHS to confirm this."),
            ("PIHS arises from a CNS-resident dendritic-cell population that is developmentally "
             "distinct from the interstitial DCs behind disseminated HS (cell biologist's "
             "reading); a lineage-restricted germline mechanism would unify the anatomic and "
             "non-disseminating observations rather than needing two explanations."),
            ("A tumor this anatomically predictable, and plausibly non-disseminating, is exactly "
             "the profile where local debulking plus systemic adjuvant therapy changes the "
             "prognosis ceiling -- already demonstrated for canine HS in general with CCNU "
             "(computational/clinical-translation reading); this scenario substitutes trametinib."),
        ],
        "unverified_extrapolations": [
            ("Corgi PIHS is less prone to dissemination than other breeds' HS -- plausible from "
             "the primary-vs-disseminated breed skew literature, but not directly measured, "
             "and this model has no explicit dissemination/metastasis mechanic to test it with"),
            ("the FLT3/BATF3/IRF8/ID2 candidate-gene hypothesis is extrapolated from mouse "
             "biology, never tested in dogs, and not linked to any Corgi-specific variant"),
            ("debulking_fraction=0.97 is illustrative, not fit to a reported canine "
             "resection-completeness statistic"),
            ("the 568-day localized-HS survival benchmark is not confirmed to be CNS-specific; "
             "it is suggestive context, not a location-matched number"),
        ],
        "warning": (
            "This stacks a local-therapy hypothesis on top of mapk_cns_demo's already-doubly-"
            "speculative CNS extrapolation. Read the four-arm comparison as a demonstration of "
            "*why* combining local and systemic therapy could plausibly matter more here than "
            "for disseminated disease, not as a survival prediction for an actual dog."
        ),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


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


def combination_control_demo(out: Path, breed: str = "bmd", debulking_fraction: float = DEBULKING_FRACTION,
                             trials: int = 300, horizon_days: int = 730,
                             preexisting_prob: float = _PREEXISTING_PROB_CENTRAL,
                             location_penetration_multiplier: float = 1.0, seed: int = 7) -> None:
    out.mkdir(parents=True, exist_ok=True)
    regimens = [("combination", True), ("cdk46_monotherapy", False)]

    rows, outcomes = [], {}
    for regimen, trametinib_active in regimens:
        scenarios = combination_scenarios(breed, debulking_fraction, CDK46_MAX_KILL_SWEEP,
                                          location_penetration_multiplier, trametinib_active)
        for max_kill_2, (model, css, seeding_rates, initial_burden, _) in scenarios.items():
            css_2 = CDK46_ILLUSTRATIVE_CSS_NM if max_kill_2 > 0 else None
            outcome = run_monte_carlo(model, css, horizon_days, seeding_rates, trials,
                                      preexisting_prob=preexisting_prob, initial_burden=initial_burden,
                                      css_reference_2=css_2, seed=seed)
            outcomes[(regimen, max_kill_2)] = outcome
            ttp = outcome.time_to_progression[outcome.progressed]
            mechanism_counts = pd.Series(outcome.dominant_mechanism).value_counts()
            mechanism_fractions = (mechanism_counts.reindex(["durable_response"] + CLONE_NAMES[1:], fill_value=0)
                                  / len(outcome.dominant_mechanism))
            rows.append({
                "regimen": regimen, "cdk46_max_kill": max_kill_2,
                "probability_durable_response": float(1 - outcome.progressed.mean()),
                "probability_progression": float(outcome.progressed.mean()),
                "median_time_to_progression_days": float(np.median(ttp)) if ttp.size else None,
                **{f"mechanism_{mechanism}": float(value) for mechanism, value in mechanism_fractions.items()},
            })
    table = pd.DataFrame(rows)
    table.to_csv(out / "combination_sensitivity.csv", index=False)

    days = np.arange(horizon_days + 1)
    fig, axes = plt.subplots(1, 3, figsize=(15.5, 4.5))
    combination_table = table[table["regimen"] == "combination"]
    for max_kill_2 in CDK46_MAX_KILL_SWEEP:
        outcome = outcomes[("combination", max_kill_2)]
        median_burden = np.median(outcome.trajectories.sum(axis=2), axis=0)
        axes[0].plot(days, median_burden, label=f"cdk46 max_kill={max_kill_2}")
    axes[0].set(xlabel="day", ylabel="median total tumor burden",
               title=f"combination trajectories: breed={breed}")
    axes[0].legend(fontsize=7)
    for regimen, color in (("combination", "tab:blue"), ("cdk46_monotherapy", "tab:red")):
        subset = table[table["regimen"] == regimen]
        axes[1].plot(subset["cdk46_max_kill"], subset["probability_durable_response"],
                    marker="o", label=regimen, color=color)
    axes[1].set(xlabel="CDK4/6i max_kill (illustrative, unmeasured)", ylabel="P(durable response)",
               title="combination vs. monotherapy", ylim=(0, 1))
    axes[1].legend(fontsize=8)
    mechanism_columns = [f"mechanism_{name}" for name in ["durable_response"] + CLONE_NAMES[1:]]
    combination_table.set_index("cdk46_max_kill")[mechanism_columns].plot(kind="bar", stacked=True, ax=axes[2])
    axes[2].set(ylabel="fraction of trials", title="combination: does it close ALL routes at once?")
    axes[2].legend(fontsize=6)
    fig.tight_layout(); fig.savefig(out / "combination_sensitivity.png", dpi=160); plt.close(fig)

    summary = {
        "breed_context": breed, "debulking_fraction": debulking_fraction,
        "preexisting_prob_used": preexisting_prob, "cdk46_ic50_nM": CDK46_ILLUSTRATIVE_IC50_NM,
        "cdk46_css_nM": CDK46_ILLUSTRATIVE_CSS_NM, "sensitivity": rows,
        "mechanism_agnostic_rationale": MECHANISM_AGNOSTIC_RATIONALE,
        "division_of_labor": DIVISION_OF_LABOR_NOTE,
        "unverified_extrapolations": [
            ("no canine or confirmed human CDK4/6-inhibitor potency/exposure number exists; "
             "cdk46_ic50_nM and cdk46_css_nM are round illustrative placeholders, and "
             "cdk46_max_kill is swept rather than fixed for the same reason "
             "preexisting_prob is swept in mapk_resistance_demo"),
            ("assumes Corgi PIHS carries a MAPK driver at all (the premise of every scenario in "
             "this module) AND that CDK4/6 dependence specifically (not just any downstream "
             "node) is the relevant shared mechanism -- neither is confirmed in dogs"),
            ("combined-drug toxicity is not modeled: real MEK+CDK4/6 combinations in human "
             "trials often require dose-reducing both agents below their monotherapy doses, "
             "which would lower css_reference/css_reference_2 below what is used here"),
            ("stacks on top of every extrapolation already listed in localized_control_demo's "
             "and mapk_cns_demo's summary.json"),
        ],
        "warning": (
            "The most speculative scenario in this module, by design: it exists to show the "
            "*shape* of the shared-downstream-node hypothesis (does closing one node suppress "
            "all three escape mechanisms at once, or only some?), not to estimate a real "
            "probability. Read the stacked-bar mechanism panel, not the single durable-response "
            "number at any one cdk46_max_kill value, as the result."
        ),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


def combination_toxicity_demo(out: Path, breed: str = "bmd", debulking_fraction: float = DEBULKING_FRACTION,
                              max_kill_2: float = 0.05, trials: int = 300, horizon_days: int = 730,
                              preexisting_prob: float = _PREEXISTING_PROB_CENTRAL,
                              location_penetration_multiplier: float = 1.0, seed: int = 7) -> None:
    """Stress-tests the combination finding against realistic combined-dosing de-rating.

    Fixes CDK4/6i potency at `max_kill_2` (default 0.05, the threshold that closed off all
    escape routes at full illustrative dose in `combination_control_demo`) and sweeps
    COMBINED_EXPOSURE_DERATING, applying it multiplicatively to *both* the trametinib and
    CDK4/6i reference concentrations, to see whether the benefit survives the kind of dose
    reduction real combination trials commonly require -- see TOXICITY_EXTRAPOLATION_NOTE --
    rather than silently assuming full, unconstrained dosing of both drugs holds.
    """
    out.mkdir(parents=True, exist_ok=True)
    scenarios = combination_scenarios(breed, debulking_fraction, [max_kill_2],
                                      location_penetration_multiplier)
    model, css, seeding_rates, initial_burden, _ = scenarios[max_kill_2]

    rows, outcomes = [], {}
    for derating in COMBINED_EXPOSURE_DERATING:
        outcome = run_monte_carlo(model, css * derating, horizon_days, seeding_rates, trials,
                                  preexisting_prob=preexisting_prob, initial_burden=initial_burden,
                                  css_reference_2=CDK46_ILLUSTRATIVE_CSS_NM * derating, seed=seed)
        outcomes[derating] = outcome
        ttp = outcome.time_to_progression[outcome.progressed]
        mechanism_counts = pd.Series(outcome.dominant_mechanism).value_counts()
        mechanism_fractions = (mechanism_counts.reindex(["durable_response"] + CLONE_NAMES[1:], fill_value=0)
                              / len(outcome.dominant_mechanism))
        rows.append({
            "combined_exposure_derating": derating,
            "trametinib_css_nM": css * derating, "cdk46_css_nM": CDK46_ILLUSTRATIVE_CSS_NM * derating,
            "probability_durable_response": float(1 - outcome.progressed.mean()),
            "probability_progression": float(outcome.progressed.mean()),
            "median_time_to_progression_days": float(np.median(ttp)) if ttp.size else None,
            **{f"mechanism_{mechanism}": float(value) for mechanism, value in mechanism_fractions.items()},
        })
    table = pd.DataFrame(rows)
    table.to_csv(out / "toxicity_derating_sensitivity.csv", index=False)

    days = np.arange(horizon_days + 1)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    for derating, outcome in outcomes.items():
        median_burden = np.median(outcome.trajectories.sum(axis=2), axis=0)
        axes[0].plot(days, median_burden, label=f"{int(derating * 100)}% of illustrative exposure")
    axes[0].set(xlabel="day", ylabel="median total tumor burden",
               title=f"combined-dose de-rating: breed={breed}, cdk46 max_kill={max_kill_2}")
    axes[0].legend(fontsize=7)
    axes[1].plot(table["combined_exposure_derating"], table["probability_durable_response"],
                marker="o", color="tab:purple")
    axes[1].set(xlabel="fraction of illustrative full exposure (both drugs)", ylabel="P(durable response)",
               title="does the benefit survive realistic dose reduction?", ylim=(0, 1))
    fig.tight_layout(); fig.savefig(out / "toxicity_derating.png", dpi=160); plt.close(fig)

    summary = {
        "breed_context": breed, "max_kill_2_tested": max_kill_2,
        "preexisting_prob_used": preexisting_prob, "sensitivity": rows,
        "toxicity_extrapolation_rationale": TOXICITY_EXTRAPOLATION_NOTE,
        "mechanism_agnostic_rationale": MECHANISM_AGNOSTIC_RATIONALE,
        "unverified_extrapolations": [
            ("no canine combination dose-finding trial exists for trametinib plus any CDK4/6 "
             "inhibitor; COMBINED_EXPOSURE_DERATING is a plausible range grounded in general "
             "combination-trial practice, not a measured value for this drug pair"),
            ("CDK4/6-inhibitor-induced neutropenia is extrapolated from human pharmacology on "
             "mechanistic (on-target, conserved cell-cycle biology) grounds; no canine "
             "hematologic toxicity data for any CDK4/6 inhibitor was found"),
            ("stacks on top of every extrapolation already listed in combination_control_demo's, "
             "localized_control_demo's, and mapk_cns_demo's summary.json"),
        ],
        "warning": (
            "Tests whether the combination's benefit is robust to realistic dose reduction, not "
            "whether the combination is actually safe: real toxicity depends on a combination "
            "dose-finding trial that has not been run in dogs for this drug pair. Read this as "
            "a sensitivity analysis stacked on an efficacy model, not a safety assessment."
        ),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


# "Durable response" everywhere else in this module means only "no detected relapse within
# whatever horizon_days that specific run used" -- typically 730 days (2 years). It is not a
# claim of permanence, and testing at longer horizons shows it is not flat: the combination
# slows the pathway_reactivation escape route (its net growth margin goes from clearly positive
# without CDK4/6i to only slightly negative with it, in this parameterization) rather than
# eliminating it, so per-trial parameter variability lets a slowly growing minority cross the
# detection threshold given enough years. DURABILITY_HORIZON_SWEEP makes that horizon-dependence
# an explicit, checkable output instead of an unstated assumption baked into a fixed 2-year run.
DURABILITY_HORIZON_SWEEP = [365, 730, 1825, 3650]  # 1, 2, 5, 10 years


def durability_horizon_demo(out: Path, breed: str = "bmd", debulking_fraction: float = DEBULKING_FRACTION,
                            max_kill_2: float = 0.05, trials: int = 300,
                            preexisting_prob: float = _PREEXISTING_PROB_CENTRAL,
                            location_penetration_multiplier: float = 1.0, seed: int = 7) -> None:
    """How long does "durable response" actually mean, for the best-performing combination arm?

    Sweeps DURABILITY_HORIZON_SWEEP at fixed full-dose combination therapy (max_kill_2, defaults
    to the threshold that closed off all escape routes at 2 years in combination_control_demo),
    reporting durable-response probability and which mechanism drives relapse at each horizon --
    since which mechanism dominates can itself change with horizon (see summary.json).
    """
    out.mkdir(parents=True, exist_ok=True)
    scenarios = combination_scenarios(breed, debulking_fraction, [max_kill_2],
                                      location_penetration_multiplier)
    model, css, seeding_rates, initial_burden, _ = scenarios[max_kill_2]

    rows = []
    for horizon_days in DURABILITY_HORIZON_SWEEP:
        outcome = run_monte_carlo(model, css, horizon_days, seeding_rates, trials,
                                  preexisting_prob=preexisting_prob, initial_burden=initial_burden,
                                  css_reference_2=CDK46_ILLUSTRATIVE_CSS_NM, seed=seed)
        ttp = outcome.time_to_progression[outcome.progressed]
        mechanism_counts = pd.Series(outcome.dominant_mechanism).value_counts()
        mechanism_fractions = (mechanism_counts.reindex(["durable_response"] + CLONE_NAMES[1:], fill_value=0)
                              / len(outcome.dominant_mechanism))
        rows.append({
            "horizon_days": horizon_days, "horizon_years": horizon_days / 365,
            "probability_durable_response": float(1 - outcome.progressed.mean()),
            "probability_progression": float(outcome.progressed.mean()),
            "median_time_to_progression_days": float(np.median(ttp)) if ttp.size else None,
            **{f"mechanism_{mechanism}": float(value) for mechanism, value in mechanism_fractions.items()},
        })
    table = pd.DataFrame(rows)
    table.to_csv(out / "durability_horizon_sensitivity.csv", index=False)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(table["horizon_years"], table["probability_durable_response"], marker="o", color="tab:green")
    ax.set(xlabel="years of follow-up simulated", ylabel="P(no relapse detected by this horizon)",
          title=f"how long is \"durable\"? breed={breed}, cdk46 max_kill={max_kill_2}", ylim=(0, 1.02))
    fig.tight_layout(); fig.savefig(out / "durability_horizon.png", dpi=160); plt.close(fig)

    summary = {
        "breed_context": breed, "max_kill_2_tested": max_kill_2,
        "preexisting_prob_used": preexisting_prob, "sensitivity": rows,
        "note": (
            "\"Durable response\" throughout this module means only \"no relapse detected "
            "within the horizon that specific run used,\" not permanence. In testing here, "
            "durable-response probability was not flat across horizons: it declined from the "
            "2-year figure reported elsewhere in this module as follow-up was extended to 5 and "
            "10 years, driven almost entirely by the same pathway_reactivation route that "
            "dominates escape without CDK4/6i -- the combination slows that route (its net "
            "growth margin goes from clearly positive to only slightly negative in this "
            "parameterization) rather than eliminating it, so per-trial parameter variability "
            "lets a slowly growing minority cross the detection threshold given enough years."
        ),
        "unverified_extrapolations": [
            ("stacks on top of every extrapolation already listed in combination_control_demo's "
             "and combination_toxicity_demo's summary.json"),
            ("long-horizon behavior is sensitive to the illustrative growth-rate/kill-rate "
             "margins chosen for each escape mechanism, which are not fit to any measured "
             "canine data"),
        ],
        "warning": (
            "Read probability_durable_response at any single horizon as a snapshot, not the "
            "answer -- the honest answer to \"how long is durable\" is the whole curve in "
            "durability_horizon_sensitivity.csv, not one number."
        ),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


# mRNA vaccine follow-on --------------------------------------------------------------------
# Real precedent for a shared/hotspot-mutation-targeted ("off-the-shelf", not fully personalized)
# mRNA cancer vaccine: mRNA-5671 (Moderna/Merck), a Phase 1 lipid-nanoparticle vaccine targeting
# four frequent KRAS mutations (G12D, G13D, G12C, G12V) as monotherapy or with pembrolizumab, in
# KRAS-mutant NSCLC/CRC/pancreatic cancer; and a KRAS G12V-specific mRNA vaccine + pembrolizumab
# combination reporting clinical benefit in advanced solid tumors (Cell Research 2024). Corgi
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
    "that human precedent onto Corgi PIHS's own (unconfirmed) PTPN11/KRAS driver hypothesis."
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


def vaccine_followon_demo(out: Path, breed: str = "bmd", debulking_fraction: float = DEBULKING_FRACTION,
                          cdk46_max_kill: float = 0.05, trials: int = 300, horizon_days: int = 1825,
                          preexisting_prob: float = _PREEXISTING_PROB_CENTRAL,
                          location_penetration_multiplier: float = 1.0, seed: int = 7) -> None:
    """Does a follow-on mRNA vaccine close the long-horizon durability gap `durability_horizon_demo`
    found (durable-response probability eroding out to 5-10 years, driven by pathway_reactivation)?

    Defaults to a 5-year (1825-day) horizon specifically because that is where the gap this demo
    is testing shows up; a 2-year run would not exercise the effect being investigated. Sweeps
    VACCINE_MAX_KILL_SWEEP at fixed combination-drug potency (`cdk46_max_kill`).
    """
    out.mkdir(parents=True, exist_ok=True)
    scenarios = vaccine_followon_scenarios(breed, debulking_fraction, cdk46_max_kill,
                                           VACCINE_MAX_KILL_SWEEP, location_penetration_multiplier)

    rows, outcomes = [], {}
    for vaccine_max_kill, (model, css, seeding_rates, initial_burden, _) in scenarios.items():
        outcome = run_monte_carlo_with_vaccine(
            model, css, horizon_days, seeding_rates, vaccine_start_day=VACCINE_START_DAY,
            vaccine_ramp_days=VACCINE_RAMP_DAYS, vaccine_max_kill=vaccine_max_kill,
            immune_escape_seeding_rate=IMMUNE_ESCAPE_SEEDING_RATE, clone_names=VACCINE_CLONE_NAMES,
            trials=trials, preexisting_prob=preexisting_prob, initial_burden=initial_burden,
            css_reference_2=CDK46_ILLUSTRATIVE_CSS_NM, seed=seed)
        outcomes[vaccine_max_kill] = outcome
        ttp = outcome.time_to_progression[outcome.progressed]
        mechanism_counts = pd.Series(outcome.dominant_mechanism).value_counts()
        mechanism_fractions = (mechanism_counts.reindex(["durable_response"] + VACCINE_CLONE_NAMES[1:], fill_value=0)
                              / len(outcome.dominant_mechanism))
        rows.append({
            "vaccine_max_kill": vaccine_max_kill,
            "probability_durable_response": float(1 - outcome.progressed.mean()),
            "probability_progression": float(outcome.progressed.mean()),
            "median_time_to_progression_days": float(np.median(ttp)) if ttp.size else None,
            **{f"mechanism_{mechanism}": float(value) for mechanism, value in mechanism_fractions.items()},
        })
    table = pd.DataFrame(rows)
    table.to_csv(out / "vaccine_followon_sensitivity.csv", index=False)

    days = np.arange(horizon_days + 1)
    fig, axes = plt.subplots(1, 3, figsize=(15.5, 4.5))
    for vaccine_max_kill in VACCINE_MAX_KILL_SWEEP:
        outcome = outcomes[vaccine_max_kill]
        median_burden = np.median(outcome.trajectories.sum(axis=2), axis=0)
        axes[0].plot(days, median_burden, label=f"vaccine max_kill={vaccine_max_kill}")
    axes[0].axvline(VACCINE_START_DAY, color="gray", linestyle=":", linewidth=.9)
    axes[0].set(xlabel="day", ylabel="median total tumor burden",
               title=f"drug + vaccine: breed={breed}, horizon={horizon_days / 365:.0f}y")
    axes[0].legend(fontsize=7)
    axes[1].plot(table["vaccine_max_kill"], table["probability_durable_response"],
                marker="o", color="tab:green")
    axes[1].set(xlabel="vaccine max_kill (illustrative, unmeasured)", ylabel="P(durable response)",
               title=f"does the vaccine close the {horizon_days / 365:.0f}-year gap?", ylim=(0, 1))
    mechanism_columns = [f"mechanism_{name}" for name in ["durable_response"] + VACCINE_CLONE_NAMES[1:]]
    table.set_index("vaccine_max_kill")[mechanism_columns].plot(kind="bar", stacked=True, ax=axes[2])
    axes[2].set(ylabel="fraction of trials",
               title="closing pathway_reactivation vs. opening immune_escape")
    axes[2].legend(fontsize=6)
    fig.tight_layout(); fig.savefig(out / "vaccine_followon.png", dpi=160); plt.close(fig)

    summary = {
        "breed_context": breed, "cdk46_max_kill_used": cdk46_max_kill, "horizon_days": horizon_days,
        "preexisting_prob_used": preexisting_prob, "sensitivity": rows,
        "vaccine_precedent": VACCINE_PRECEDENT_NOTE,
        "antigen_persistence_rationale": ANTIGEN_PERSISTENCE_NOTE,
        "dendritic_cell_vaccine_caveat": DENDRITIC_CELL_VACCINE_CAVEAT,
        "unverified_extrapolations": [
            ("no canine cancer vaccine trial of any kind exists for this disease; "
             "vaccine_start_day, vaccine_ramp_days, and vaccine_max_kill are all illustrative, "
             "not fit to measured data"),
            ("assumes Corgi PIHS carries a PTPN11/KRAS hotspot mutation at all (the premise of "
             "every scenario in this module) that would be shareable/targetable across cases -- "
             "unconfirmed, no canine CNS-specific sequencing exists"),
            ("immune_escape_seeding_rate and immune_escape_growth_penalty are illustrative "
             "placeholders, not measured for this or any histiocytic sarcoma"),
            ("PIHS's dendritic-cell lineage of origin (see dendritic_cell_vaccine_caveat) is a "
             "biologically real reason antigen-presentation efficacy could differ from other "
             "tumor types; not modeled quantitatively here"),
            ("stacks on top of every extrapolation already listed in combination_control_demo's "
             "and durability_horizon_demo's summary.json"),
        ],
        "warning": (
            "The most speculative scenario in this module: it exists to show the *shape* of "
            "whether a shared-neoantigen vaccine can suppress a slowly-emerging, antigen-"
            "preserving escape route (pathway_reactivation) at long horizons, and whether doing "
            "so trades that risk for a new, smaller antigen-loss risk -- not to estimate a real "
            "probability for an actual dog. Read the stacked mechanism panel and the vaccine_max_kill "
            "sensitivity curve together, not any single durable-response number, as the result."
        ),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


# Feasibility of curing a *single* dog, as opposed to a population-level response rate ----------
# Every demo above reports an ensemble probability across many different hypothetical dogs (a new
# perturbed model, drug exposure, and starting tumor state redrawn every trial) -- useful for a
# population-level question ("what fraction of dogs..."), but it does not by itself answer "what
# can be done for one specific dog." Two things a population ensemble doesn't separate matter for
# that framing: (1) how much of the outcome uncertainty is about *which* dog this is -- resolvable
# in principle by biopsy, deep/ctDNA sequencing, or serial imaging on that specific dog -- versus
# genuinely irreducible chance in how the tumor evolves even with perfect knowledge of that dog's
# biology (see decompose_patient_uncertainty); and (2) given the two knowable-but-currently-
# unmeasured facts that matter most for one dog -- does a resistant subclone already exist, and
# where does this dog's own drug exposure/mutation propensity fall in the plausible range -- what
# is the realistic best-to-worst-case bracket, rather than one blended population average.

# Representative pre-existing-subclone size if a deep-sequencing/ctDNA diagnostic on a specific
# dog were to detect one: the upper end of sample_initial_state's own 1e-6 to 1e-3 illustrative
# range, i.e. a subclone large enough to plausibly be detectable with current sequencing depth.
_DETECTABLE_SUBCLONE_FRACTION = 1e-3

# 5th/95th-percentile z-score for a standard normal distribution, used to convert this module's
# own lognormal uncertainty parameters (exposure_scale, seeding_rate_scale, ic50 jitter) into
# concrete "pessimistic dog" / "optimistic dog" multipliers for the worst/best-case bracket below
# -- a stress test of the *edges* of the uncertainty this module already assumes, not a new one.
_PERCENTILE_Z = 1.645


def single_patient_feasibility_demo(out: Path, breed: str = "bmd",
                                    debulking_fraction: float = DEBULKING_FRACTION,
                                    cdk46_max_kill: float = 0.05, horizon_days: int = 1825,
                                    n_dogs: int = 40, repeats_per_dog: int = 60,
                                    preexisting_prob: float = _PREEXISTING_PROB_CENTRAL,
                                    location_penetration_multiplier: float = 1.0, seed: int = 7) -> None:
    """Reframes the full-potency combination model (trametinib + CDK4/6i at `cdk46_max_kill`)
    around a single dog rather than a population, with three analyses:

    1. `decompose_patient_uncertainty`'s between-vs-within-dog variance split: how much of the
       outcome is "which dog you are" (in principle knowable about a specific dog) versus pure
       chance (not knowable about any dog, no matter how well characterized).
    2. The value of knowing, for one dog, whether a resistant subclone already exists before
       treatment (a real, if not yet clinically applied, diagnostic question -- deep/ctDNA
       sequencing for a known hotspot at low variant-allele frequency), compared against the
       population-average number reported elsewhere in this module.
    3. A worst-/best-case bracket at the edges of this module's own assumed exposure- and
       mutation-rate uncertainty (its 5th/95th percentiles), combined with subclone status --
       the realistic range for one dog, as opposed to a single blended average.
    """
    out.mkdir(parents=True, exist_ok=True)
    scenarios = combination_scenarios(breed, debulking_fraction, [cdk46_max_kill],
                                      location_penetration_multiplier)
    model, css, seeding_rates, initial_burden, provenance = scenarios[cdk46_max_kill]
    css_2 = CDK46_ILLUSTRATIVE_CSS_NM
    k = len(model.growth)

    population_outcome = run_monte_carlo(model, css, horizon_days, seeding_rates, trials=300,
                                         preexisting_prob=preexisting_prob, initial_burden=initial_burden,
                                         css_reference_2=css_2, seed=seed)
    population_average = float(1 - population_outcome.progressed.mean())

    decomposition = decompose_patient_uncertainty(
        model, css, horizon_days, seeding_rates, n_dogs=n_dogs, repeats_per_dog=repeats_per_dog,
        preexisting_prob=preexisting_prob, initial_burden=initial_burden,
        css_reference_2=css_2, seed=seed)

    no_subclone_initial = np.zeros(k)
    no_subclone_initial[0] = initial_burden
    dominant_index = 1 + int(np.argmax(seeding_rates))
    has_subclone_initial = no_subclone_initial.copy()
    has_subclone_initial[0] *= (1 - _DETECTABLE_SUBCLONE_FRACTION)
    has_subclone_initial[dominant_index] = initial_burden * _DETECTABLE_SUBCLONE_FRACTION
    subclone_outcomes = {}
    for label, initial in (("subclone_absent", no_subclone_initial), ("subclone_present", has_subclone_initial)):
        outcome = run_monte_carlo_fixed_patient(model, css, horizon_days, seeding_rates, initial,
                                                repeats=repeats_per_dog * 2, css_2=css_2, seed=seed)
        subclone_outcomes[label] = float(1 - outcome.progressed.mean())

    low_exposure = np.exp(-_PERCENTILE_Z * .3)   # 5th pctile css multiplier: less drug (worse)
    high_exposure = np.exp(_PERCENTILE_Z * .3)   # 95th pctile css multiplier: more drug (better)
    low_ic50 = np.exp(-_PERCENTILE_Z * .2)       # 5th pctile ic50 multiplier: more sensitive (better)
    high_ic50 = np.exp(_PERCENTILE_Z * .2)       # 95th pctile ic50 multiplier: less sensitive (worse)
    low_rate = np.exp(-_PERCENTILE_Z * .5)       # 5th pctile mutation-rate multiplier (better)
    high_rate = np.exp(_PERCENTILE_Z * .5)       # 95th pctile mutation-rate multiplier (worse)
    bracket_scenarios = {
        "worst_case": (low_exposure, high_ic50, high_rate, has_subclone_initial),
        "best_case": (high_exposure, low_ic50, low_rate, no_subclone_initial),
    }
    bracket_outcomes = {}
    for label, (css_mult, ic50_mult, rate_mult, initial) in bracket_scenarios.items():
        bracket_model = replace(model, ic50_nM=model.ic50_nM * ic50_mult)
        outcome = run_monte_carlo_fixed_patient(bracket_model, css * css_mult, horizon_days,
                                                seeding_rates * rate_mult, initial,
                                                repeats=repeats_per_dog * 2, css_2=css_2 * css_mult, seed=seed)
        bracket_outcomes[label] = float(1 - outcome.progressed.mean())

    fig, axes = plt.subplots(1, 3, figsize=(15.5, 4.5))
    axes[0].hist(decomposition.per_dog_durable_probability, bins=12, color="tab:blue", alpha=.85)
    axes[0].axvline(population_average, color="gray", linestyle="--", linewidth=1,
                    label=f"population average ({population_average:.2f})")
    axes[0].set(xlabel="a given dog's own true P(durable response)", ylabel="number of simulated dogs",
               title=f"between-dog spread (ICC={decomposition.intraclass_correlation:.2f})")
    axes[0].legend(fontsize=7)
    axes[1].bar(["subclone\nabsent", "population\naverage", "subclone\npresent"],
               [subclone_outcomes["subclone_absent"], population_average, subclone_outcomes["subclone_present"]],
               color=["tab:green", "tab:gray", "tab:red"])
    axes[1].set(ylabel="P(durable response)", title="value of knowing subclone status", ylim=(0, 1))
    axes[2].bar(["worst\ncase", "population\naverage", "best\ncase"],
               [bracket_outcomes["worst_case"], population_average, bracket_outcomes["best_case"]],
               color=["tab:red", "tab:gray", "tab:green"])
    axes[2].set(ylabel="P(durable response)", title="realistic range for one dog", ylim=(0, 1))
    fig.tight_layout(); fig.savefig(out / "single_patient_feasibility.png", dpi=160); plt.close(fig)

    pd.DataFrame([
        {"dog_index": i, "durable_response_probability": p}
        for i, p in enumerate(decomposition.per_dog_durable_probability)
    ]).to_csv(out / "per_dog_probability.csv", index=False)

    summary = {
        "breed_context": breed, "cdk46_max_kill_used": cdk46_max_kill, "horizon_days": horizon_days,
        "population_average_durable_response": population_average,
        "uncertainty_decomposition": {
            "between_dog_variance": decomposition.between_dog_variance,
            "within_dog_variance": decomposition.within_dog_variance,
            "intraclass_correlation": decomposition.intraclass_correlation,
            "n_dogs": n_dogs, "repeats_per_dog": repeats_per_dog,
        },
        "subclone_value_of_information": {
            **subclone_outcomes, "population_average": population_average,
            "detectable_subclone_fraction_assumed": _DETECTABLE_SUBCLONE_FRACTION,
        },
        "worst_best_case_bracket": {**bracket_outcomes, "population_average": population_average},
        "interpretation": (
            f"Intraclass correlation (ICC) = {decomposition.intraclass_correlation:.2f}: this "
            "fraction of the total outcome variance is 'which dog you are' (in principle "
            "resolvable by testing that specific dog), and the rest is chance that no test on "
            "that dog could predict, because it depends on whether/when a resistant mutation "
            "happens to arise -- a Poisson process, not a deterministic property of the dog. A "
            "high ICC means personalized diagnostics (biopsy, deep sequencing, drug-level "
            "monitoring) could meaningfully narrow this dog's individual prognosis; a low ICC "
            "means the outcome is dominated by chance no diagnostic could have predicted, and "
            "only a more broadly effective treatment (not better patient selection) would move "
            "the needle. Read the subclone and bracket panels as answering a related but "
            "distinct question: not how much uncertainty exists, but which direction it's "
            "plausible to expect for a dog whose actual biology and drug exposure could in "
            "principle be measured."
        ),
        "unverified_extrapolations": [
            ("no real diagnostic pipeline for pretreatment subclone detection, drug-exposure "
             "monitoring, or per-dog mutation-rate estimation exists for canine HS; this demo "
             "quantifies what such diagnostics *could* be worth if they existed and were "
             "accurate, not a claim that they are currently available or validated"),
            ("_DETECTABLE_SUBCLONE_FRACTION and the bracket's percentile multipliers are applied "
             "to this module's own already-illustrative uncertainty parameters (exposure_scale, "
             "ic50_scale, seeding_rate_scale); they inherit every caveat already attached to "
             "those in combination_control_demo and mapk_resistance_demo"),
            ("the between-dog/within-dog variance split is a method-of-moments estimate that can "
             "be noisy or biased toward zero (an artificially low ICC) when n_dogs and "
             "repeats_per_dog are small; increase both before trusting a precise ICC value"),
            ("stacks on top of every extrapolation already listed in combination_control_demo's "
             "summary.json"),
        ],
        "warning": (
            "This demo answers a different question than the rest of the module: not 'what "
            "fraction of dogs respond' but 'how much of one dog's fate is knowable in advance, "
            "and in which direction.' It is not a replacement for the population-level analyses "
            "elsewhere, and it does not identify a real diagnostic test -- it quantifies the "
            "hypothetical value of information a perfect one would provide, within this "
            "module's own already-speculative model."
        ),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


def dog_preset() -> tuple[ResistanceModel, float, np.ndarray, dict]:
    """Cobimetinib vs. canine PTPN11/KRAS-mutant HS; sensitive-clone IC50 and Cmax are real.

    The drug actually in canine clinical development is trametinib, not cobimetinib -- see the
    "clinical_development" provenance field. Cobimetinib is used here because it is the only MEK
    inhibitor with a published cellular IC50 measured directly on canine HS lines; no published
    trametinib-specific canine HS cellular potency number was found, and estimating one by
    converting from cobimetinib would stack an unverified assumption on top of a proxy substance,
    so this preset does not attempt that.
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
            "(University of Florida; Michigan State University, VCT25005905), following a "
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


def mapk_resistance_demo(out: Path, species: str = "dog", trials: int = 300,
                         horizon_days: int = 730, seed: int = 7) -> None:
    """Run the Monte Carlo escape model across a `preexisting_prob` sweep, not one fixed value.

    `preexisting_prob` (whether a resistant subclone already exists at treatment start) is the
    single most influential parameter in this model and has no HS-specific source; reporting a
    durable-response probability at one asserted value would mostly reflect that choice, not a
    result. The sweep is reported as a range; only the sweep value matching
    `_PREEXISTING_PROB_CENTRAL` is used for the illustrative trajectory and mechanism plots.
    """
    out.mkdir(parents=True, exist_ok=True)
    model, css_reference, seeding_rates, provenance = SPECIES_PRESETS[species]()

    sweep_rows, outcomes_by_prob = [], {}
    for prob in _PREEXISTING_PROB_SWEEP:
        outcome = run_monte_carlo(model, css_reference, horizon_days, seeding_rates, trials,
                                  preexisting_prob=prob, seed=seed)
        outcomes_by_prob[prob] = outcome
        ttp = outcome.time_to_progression[outcome.progressed]
        sweep_rows.append({
            "preexisting_prob": prob,
            "probability_durable_response": float(1 - outcome.progressed.mean()),
            "probability_progression": float(outcome.progressed.mean()),
            "median_time_to_progression_days": float(np.median(ttp)) if ttp.size else None,
        })
    sweep_table = pd.DataFrame(sweep_rows)
    sweep_table.to_csv(out / "preexisting_prob_sensitivity.csv", index=False)

    outcome = outcomes_by_prob[_PREEXISTING_PROB_CENTRAL]
    total = outcome.trajectories.sum(axis=2)
    days = np.arange(horizon_days + 1)
    quantiles = np.quantile(total, [.1, .5, .9], axis=0)
    pd.DataFrame({"day": days, "p10_total_burden": quantiles[0], "median_total_burden": quantiles[1],
                 "p90_total_burden": quantiles[2]}).to_csv(out / "trajectory_quantiles.csv", index=False)

    mechanism_counts = pd.Series(outcome.dominant_mechanism).value_counts()
    mechanism_table = mechanism_counts.reindex(["durable_response"] + CLONE_NAMES[1:], fill_value=0)
    mechanism_table = (mechanism_table / len(outcome.dominant_mechanism)).rename("trial_fraction")
    mechanism_table.to_csv(out / "escape_mechanism_breakdown.csv")

    fig, axes = plt.subplots(1, 3, figsize=(15.5, 4.5))
    axes[0].fill_between(days, quantiles[0], quantiles[2], alpha=.25, color="tab:blue")
    axes[0].plot(days, quantiles[1], color="tab:blue")
    axes[0].axhline(model.carrying_capacity, color="gray", linestyle="--", linewidth=.8)
    axes[0].set(xlabel="day", ylabel="total tumor burden",
               title=f"{species}: burden at preexisting_prob={_PREEXISTING_PROB_CENTRAL}")
    mechanism_table.plot(kind="bar", ax=axes[1], color="tab:orange")
    axes[1].set(ylabel="fraction of trials", title="dominant outcome (this preexisting_prob only)")
    axes[1].tick_params(axis="x", rotation=30)
    axes[2].plot(sweep_table["preexisting_prob"], sweep_table["probability_durable_response"],
                marker="o", color="tab:blue")
    for study in LOMUSTINE_BENCHMARK["studies"]:
        axes[2].axhline(study["overall_response_rate"], color="gray", linestyle=":", linewidth=.9)
    axes[2].set(xlabel="assumed P(pre-existing resistant subclone)", ylabel="P(durable response)",
               title="sensitivity to the least-grounded input\n(gray: lomustine response rates, different endpoint)",
               ylim=(0, 1))
    fig.tight_layout(); fig.savefig(out / "resistance_monte_carlo.png", dpi=160); plt.close(fig)

    summary = {
        "species": species, "trials": trials, "horizon_days": horizon_days,
        "preexisting_prob_sensitivity": sweep_table.to_dict(orient="records"),
        "central_scenario": {
            "preexisting_prob": _PREEXISTING_PROB_CENTRAL,
            **{k: v for k, v in sweep_rows[_PREEXISTING_PROB_SWEEP.index(_PREEXISTING_PROB_CENTRAL)].items()
               if k != "preexisting_prob"},
            "escape_mechanism_breakdown": mechanism_table.to_dict(),
        },
        "lomustine_benchmark": LOMUSTINE_BENCHMARK,
        "provenance": provenance,
        "warning": "Synthetic Monte Carlo exploration of plausible escape dynamics; only the "
                  "fields under provenance.calibrated_from_data are anchored to a published "
                  "dataset. Not a validated predictive or clinical model. Read the "
                  "preexisting_prob_sensitivity range, not any single number in central_scenario, "
                  "as the headline result -- a fixed point estimate here mostly reflects an "
                  "unsourced assumption, not a finding. The model also omits treatment-limiting "
                  "toxicity, non-adherence, and death from other causes, all of which would push "
                  "real-world durability below what is shown here.",
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


def compare_orthologs(gene: str, hotspots: list[int], out: Path) -> None:
    """Fetch human and dog AlphaFold models for `gene` and compare confidence at hotspot residues.

    Residue numbering is not assumed to match between species: hotspot positions (given in
    human UniProt numbering) are mapped onto the dog structure via global sequence alignment
    before their local confidence is read off, rather than compared at the same raw index.
    """
    out.mkdir(parents=True, exist_ok=True)
    accessions = {"human": resolve_uniprot_accession(gene, HUMAN_TAXID),
                 "dog": resolve_uniprot_accession(gene, DOG_TAXID)}
    tracks = {}
    for species, accession in accessions.items():
        struct = download_structure(accession, out / species)
        tracks[species] = read_plddt_track(struct)

    human_seq = "".join(tracks["human"]["residue_type"])
    dog_seq = "".join(tracks["dog"]["residue_type"])
    alignment = align_residue_numbers(human_seq, dog_seq)
    dog_plddt = tracks["dog"].set_index("residue_number")["plddt"]
    dog_residue = tracks["dog"].set_index("residue_number")["residue_type"]
    human_plddt = tracks["human"].set_index("residue_number")["plddt"]
    human_residue = tracks["human"].set_index("residue_number")["residue_type"]

    rows = []
    for position in hotspots:
        dog_position, identical = alignment.get(position, (None, False))
        rows.append({
            "gene": gene, "human_position": position,
            "human_residue": human_residue.get(position),
            "human_plddt": float(human_plddt.get(position, np.nan)),
            "dog_position": dog_position,
            "dog_residue": dog_residue.get(dog_position) if dog_position else None,
            "dog_plddt": float(dog_plddt.get(dog_position, np.nan)) if dog_position else np.nan,
            "residue_conserved": identical,
        })
    hotspot_table = pd.DataFrame(rows)
    hotspot_table.to_csv(out / "hotspot_comparison.csv", index=False)

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(tracks["human"]["residue_number"], tracks["human"]["plddt"], label="human", alpha=.85)
    ax.plot(tracks["dog"]["residue_number"], tracks["dog"]["plddt"], label="dog", alpha=.85)
    for position in hotspots:
        ax.axvline(position, color="gray", linestyle=":", linewidth=.8)
    ax.set(xlabel="residue number (own numbering per species)", ylabel="pLDDT",
          title=f"{gene}: AlphaFold confidence, human vs. dog")
    ax.legend(); fig.tight_layout(); fig.savefig(out / "ortholog_confidence.png", dpi=160)
    plt.close(fig)

    summary = {
        "gene": gene, "human_uniprot": accessions["human"], "dog_uniprot": accessions["dog"],
        "human_length": len(human_seq), "dog_length": len(dog_seq),
        "hotspots_checked": hotspots,
        "note": "pLDDT is model confidence, not stability or functional impact; hotspot "
               "positions are mapped across species by global sequence alignment, which can "
               "mismatch near indels or low-identity regions and should be spot-checked.",
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
