import json
from dataclasses import replace
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .alphafold import align_residue_numbers, download_structure, read_plddt_track
from .mapk_resistance import CLONE_NAMES, ResistanceModel, run_monte_carlo
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
    "cyclin D1 upregulation and CDK4/6 dependence) -- but combined toxicity in human trials "
    "often forces both drugs below their single-agent doses, and no canine PK/safety data for "
    "any CDK4/6 inhibitor was found, so this scenario cannot be exposure-calibrated the way "
    "trametinib was."
)


def combination_scenarios(breed: str = "bmd", debulking_fraction: float = DEBULKING_FRACTION,
                          max_kill_2_values: list[float] = CDK46_MAX_KILL_SWEEP,
                          location_penetration_multiplier: float = 1.0
                          ) -> dict[float, tuple[ResistanceModel, float, np.ndarray, float, dict]]:
    """Trametinib (debulked CNS context) +/- a swept-potency mechanism-agnostic CDK4/6 inhibitor.

    max_kill_2=0.0 leaves ic50_nM_2/max_kill_2 unset (None) rather than setting a zero-effect
    value, so that sweep point is an exact RNG-for-RNG match to the trametinib-only arm -- a
    true null baseline, not just a mathematically-inert-but-differently-perturbed one (setting
    ic50_nM_2 at all, even to a value with no pharmacological effect, still consumes an extra
    random draw in perturb_resistance_model's per-trial jitter).
    """
    arms = localized_pihs_scenarios(breed, debulking_fraction, location_penetration_multiplier)
    model, css, seeding_rates, initial_burden, provenance = arms["debulked_trametinib"]
    scenarios = {}
    for max_kill_2 in max_kill_2_values:
        if max_kill_2 > 0:
            combo_model = replace(model, ic50_nM_2=CDK46_ILLUSTRATIVE_IC50_NM, max_kill_2=max_kill_2)
        else:
            combo_model = model
        scenarios[max_kill_2] = (combo_model, css, seeding_rates, initial_burden,
                                 {**provenance, "cdk46_max_kill": max_kill_2})
    return scenarios


def combination_control_demo(out: Path, breed: str = "bmd", debulking_fraction: float = DEBULKING_FRACTION,
                             trials: int = 300, horizon_days: int = 730,
                             preexisting_prob: float = _PREEXISTING_PROB_CENTRAL,
                             location_penetration_multiplier: float = 1.0, seed: int = 7) -> None:
    out.mkdir(parents=True, exist_ok=True)
    scenarios = combination_scenarios(breed, debulking_fraction, CDK46_MAX_KILL_SWEEP,
                                      location_penetration_multiplier)

    rows, outcomes = [], {}
    for max_kill_2, (model, css, seeding_rates, initial_burden, _) in scenarios.items():
        css_2 = CDK46_ILLUSTRATIVE_CSS_NM if max_kill_2 > 0 else None
        outcome = run_monte_carlo(model, css, horizon_days, seeding_rates, trials,
                                  preexisting_prob=preexisting_prob, initial_burden=initial_burden,
                                  css_reference_2=css_2, seed=seed)
        outcomes[max_kill_2] = outcome
        ttp = outcome.time_to_progression[outcome.progressed]
        mechanism_counts = pd.Series(outcome.dominant_mechanism).value_counts()
        mechanism_fractions = (mechanism_counts.reindex(["durable_response"] + CLONE_NAMES[1:], fill_value=0)
                              / len(outcome.dominant_mechanism))
        rows.append({
            "cdk46_max_kill": max_kill_2,
            "probability_durable_response": float(1 - outcome.progressed.mean()),
            "probability_progression": float(outcome.progressed.mean()),
            "median_time_to_progression_days": float(np.median(ttp)) if ttp.size else None,
            **{f"mechanism_{mechanism}": float(value) for mechanism, value in mechanism_fractions.items()},
        })
    table = pd.DataFrame(rows)
    table.to_csv(out / "combination_sensitivity.csv", index=False)

    days = np.arange(horizon_days + 1)
    fig, axes = plt.subplots(1, 3, figsize=(15.5, 4.5))
    for max_kill_2, outcome in outcomes.items():
        median_burden = np.median(outcome.trajectories.sum(axis=2), axis=0)
        axes[0].plot(days, median_burden, label=f"cdk46 max_kill={max_kill_2}")
    axes[0].set(xlabel="day", ylabel="median total tumor burden",
               title=f"debulked+trametinib +/- CDK4/6i: breed={breed}")
    axes[0].legend(fontsize=7)
    axes[1].plot(table["cdk46_max_kill"], table["probability_durable_response"], marker="o", color="tab:blue")
    axes[1].set(xlabel="CDK4/6i max_kill (illustrative, unmeasured)", ylabel="P(durable response)",
               title="sensitivity to unknown CDK4/6i potency", ylim=(0, 1))
    mechanism_columns = [f"mechanism_{name}" for name in ["durable_response"] + CLONE_NAMES[1:]]
    table.set_index("cdk46_max_kill")[mechanism_columns].plot(kind="bar", stacked=True, ax=axes[2])
    axes[2].set(ylabel="fraction of trials", title="does it close ALL escape routes, or just one?")
    axes[2].legend(fontsize=6)
    fig.tight_layout(); fig.savefig(out / "combination_sensitivity.png", dpi=160); plt.close(fig)

    summary = {
        "breed_context": breed, "debulking_fraction": debulking_fraction,
        "preexisting_prob_used": preexisting_prob, "cdk46_ic50_nM": CDK46_ILLUSTRATIVE_IC50_NM,
        "cdk46_css_nM": CDK46_ILLUSTRATIVE_CSS_NM, "sensitivity": rows,
        "mechanism_agnostic_rationale": MECHANISM_AGNOSTIC_RATIONALE,
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
