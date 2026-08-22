import json
from dataclasses import replace
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .alphafold import align_residue_numbers, download_structure, read_plddt_track
from .dla_binding import CHARACTERIZED_DLA_I_ALLELES, CONSENSUS_METHODS, fetch_consensus_binding_predictions
from .mapk_resistance import (
    CLONE_NAMES,
    clone_growth_margins,
    decompose_patient_uncertainty,
    run_monte_carlo,
    run_monte_carlo_fixed_patient,
    run_monte_carlo_two_compartment,
    run_monte_carlo_with_vaccine,
)
from .mapk_scenarios import (
    ANTIGEN_PERSISTENCE_NOTE,
    BRAIN_PENETRATION_FRACTION,
    CDK46_ILLUSTRATIVE_CSS_NM,
    CDK46_ILLUSTRATIVE_IC50_NM,
    CDK46_MAX_KILL_SWEEP,
    COMBINED_EXPOSURE_DERATING,
    DEBULKING_FRACTION,
    DENDRITIC_CELL_ORIGIN_NOTE,
    DENDRITIC_CELL_VACCINE_CAVEAT,
    DIVISION_OF_LABOR_NOTE,
    DURABILITY_HORIZON_SWEEP,
    IMMUNE_ESCAPE_SEEDING_RATE,
    LOCALIZED_THERAPY_PRECEDENT,
    LOMUSTINE_BENCHMARK,
    MAPK_INHIBITOR_HUMAN_BENCHMARK,
    MECHANISM_AGNOSTIC_RATIONALE,
    NODAL_INVOLVEMENT_PROB_SWEEP,
    NODAL_SEED_FRACTION,
    PULMONARY_HS_CASE_SERIES,
    SPECIES_PRESETS,
    TOXICITY_EXTRAPOLATION_NOTE,
    VACCINE_ANTIGEN_TARGETS,
    VACCINE_CLONE_NAMES,
    VACCINE_MAX_KILL_SWEEP,
    VACCINE_PRECEDENT_NOTE,
    VACCINE_RAMP_DAYS,
    VACCINE_START_DAY,
    _PREEXISTING_PROB_CENTRAL,
    _PREEXISTING_PROB_SWEEP,
    _PULMONARY_BASELINE_BURDEN,
    canine_cns_hs_scenarios,
    combination_scenarios,
    localized_pihs_scenarios,
    localized_pulmonary_scenarios,
    vaccine_antigen_peptides,
    vaccine_followon_scenarios,
)
from .uniprot import DOG_TAXID, HUMAN_TAXID, resolve_uniprot_accession

# Representative pre-existing-subclone size if a deep-sequencing/ctDNA diagnostic on a specific
# dog were to detect one: the upper end of sample_initial_state's own 1e-6 to 1e-3 illustrative
# range, i.e. a subclone large enough to plausibly be detectable with current sequencing depth.
_DETECTABLE_SUBCLONE_FRACTION = 1e-3

# 5th/95th-percentile z-score for a standard normal distribution, used to convert this module's
# own lognormal uncertainty parameters (exposure_scale, seeding_rate_scale, ic50 jitter) into
# concrete "pessimistic dog" / "optimistic dog" multipliers for the worst/best-case bracket below
# -- a stress test of the *edges* of the uncertainty this module already assumes, not a new one.
_PERCENTILE_Z = 1.645


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
        "localized_pihs_context": (
            "Kishimoto et al. 2020 (J Vet Med Sci 82(1):77-83, University of Tokyo, 186 "
            "intracranial tumors, 9,270 dogs screened) found one breed carries by "
            "far the strongest breed association of any tumor type in the study: 16 of 422 "
            "dogs of that breed had a primary intracranial tumor, 10 of which were PIHS specifically -- 50% "
            "of all 20 PIHS cases in the cohort, odds ratio 21.5 (95% CI 8.9-51.8, P<0.001). "
            "Combined with the cerebrum-only, temporal/frontal-lobe-predominant localization "
            "above, this is a genuinely striking clinical concentration -- but it is anatomic "
            "and epidemiologic, not molecular: this paper is histopathology/epidemiology only "
            "and reports no PTPN11/KRAS/BRAF mutation data for these or any other CNS cases. "
            "No canine study has sequenced localized PIHS specifically. A 'unsequenced_breed' breed option is "
            "deliberately not offered here (unlike bmd/flat_coated_retriever): those two rest on "
            "published germline GWAS loci this module extrapolates from; localized PIHS has no "
            "published germline or somatic locus to extrapolate from at all, so adding one would "
            "be fabricating a number rather than extending a real one."
        ),
        "unverified_extrapolations": [
            ("canine primary CNS HS carries the same PTPN11/KRAS-dominated driver spectrum as "
             "systemic HS -- no canine CNS-specific sequencing exists to confirm this, this presentation "
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
            ("Kishimoto et al. 2020: one breed accounts for 50% of all PIHS cases (OR 21.5), and "
             "100% of location-known PIHS cases were cerebral -- an anatomic/breed concentration "
             "on the same order as BMD's known germline-driven systemic-HS association."),
            ("That magnitude of concentration in a closed breed population is the signature of "
             "an as-yet-unidentified, high-frequency germline variant (geneticist's reading); no "
             "GWAS has been done for localized PIHS to confirm this."),
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
            ("localized PIHS is less prone to dissemination than other breeds' HS -- plausible from "
             "the primary-vs-disseminated breed skew literature, but not directly measured, "
             "and this model has no explicit dissemination/metastasis mechanic to test it with"),
            ("the FLT3/BATF3/IRF8/ID2 candidate-gene hypothesis is extrapolated from mouse "
             "biology, never tested in dogs, and not linked to any presentation-specific variant"),
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
            ("assumes localized PIHS carries a MAPK driver at all (the premise of every scenario in "
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
    """Stress-tests the combination finding against realistic combined-dosing de-rating. Fixes
    CDK4/6i potency at `max_kill_2` (default 0.05, the threshold that closed off all escape routes
    at full illustrative dose in `combination_control_demo`) and sweeps
    COMBINED_EXPOSURE_DERATING, applying it multiplicatively to *both* the trametinib and CDK4/6i
    reference concentrations, to see whether the benefit survives the kind of dose reduction real
    combination trials commonly require -- see TOXICITY_EXTRAPOLATION_NOTE -- rather than silently
    assuming full, unconstrained dosing of both drugs holds.
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

    progressor_medians = [row["median_time_to_progression_days"] for row in rows
                          if row["median_time_to_progression_days"] is not None]
    summary = {
        "breed_context": breed, "max_kill_2_tested": max_kill_2,
        "preexisting_prob_used": preexisting_prob, "sensitivity": rows,
        "human_mapk_inhibitor_benchmark": MAPK_INHIBITOR_HUMAN_BENCHMARK,
        "human_benchmark_comparison": (
            f"This module's own median_time_to_progression_days among progressors ranges "
            f"{min(progressor_medians):.0f}-{max(progressor_medians):.0f} days across the "
            f"horizons tested, versus a real 111-day [95% CI 98-124] median in "
            "MAPK_INHIBITOR_HUMAN_BENCHMARK's human BRAF+MEK-inhibitor melanoma cohort -- this "
            "module's progressors take far longer to progress once a resistant clone exists "
            "than that real human cohort did. Plausible, non-exclusive reasons: a debulked, "
            "adjuvant-therapy canine scenario against a smaller disease burden than metastatic "
            "melanoma; a different driver mutation and resistance-mechanism spectrum; or this "
            "module's own growth/kill-rate margins being tuned looser than real resistant-clone "
            "kinetics actually are. Not evidence either model is right -- read it as one more "
            "reason to treat this module's specific day-counts as illustrative, the same "
            "caveat LOMUSTINE_BENCHMARK's response-rate comparison already carries."
            if progressor_medians else
            "No trial in this run had any progressor to compare against "
            "MAPK_INHIBITOR_HUMAN_BENCHMARK's 111-day human median."
        ),
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


def vaccine_followon_demo(out: Path, breed: str = "bmd", debulking_fraction: float = DEBULKING_FRACTION,
                          cdk46_max_kill: float = 0.05, trials: int = 300, horizon_days: int = 1825,
                          preexisting_prob: float = _PREEXISTING_PROB_CENTRAL,
                          location_penetration_multiplier: float = 1.0, seed: int = 7) -> None:
    """Does a follow-on mRNA vaccine close the long-horizon durability gap `durability_horizon_demo`
    found (durable-response probability eroding out to 5-10 years, driven by
    pathway_reactivation)? Defaults to a 5-year (1825-day) horizon specifically because that is
    where the gap this demo is testing shows up; a 2-year run would not exercise the effect being
    investigated. Sweeps VACCINE_MAX_KILL_SWEEP at fixed combination-drug potency
    (`cdk46_max_kill`).
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
            ("assumes localized PIHS carries a PTPN11/KRAS hotspot mutation at all (the premise of "
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


def single_patient_feasibility_demo(out: Path, breed: str = "bmd",
                                    debulking_fraction: float = DEBULKING_FRACTION,
                                    cdk46_max_kill: float = 0.05, horizon_days: int = 1825,
                                    n_dogs: int = 40, repeats_per_dog: int = 60,
                                    preexisting_prob: float = _PREEXISTING_PROB_CENTRAL,
                                    location_penetration_multiplier: float = 1.0, seed: int = 7) -> None:
    """Reframes the full-potency combination model (trametinib + CDK4/6i at `cdk46_max_kill`) around
    a single dog rather than a population, with three analyses: 1.
    `decompose_patient_uncertainty`'s between-vs-within-dog variance split: how much of the
    outcome is "which dog you are" (in principle knowable about a specific dog) versus pure chance
    (not knowable about any dog, no matter how well characterized).
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

    margins = clone_growth_margins(model, css, css_2)
    clone_margins = dict(zip(CLONE_NAMES, (float(m) for m in margins)))

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

    positive_margin_clones = [name for name, margin in clone_margins.items()
                             if name != "sensitive" and margin > 0]
    summary = {
        "breed_context": breed, "cdk46_max_kill_used": cdk46_max_kill, "horizon_days": horizon_days,
        "population_average_durable_response": population_average,
        "central_model_clone_growth_margins_per_day": clone_margins,
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
            "happens to arise -- a Poisson process, not a deterministic property of the dog. In "
            "this parameterization, ICC came out extremely high (near 1): the per-dog histogram "
            "is sharply bimodal (most simulated dogs land at ~100% or ~0% durable response, few "
            "in between), because `central_model_clone_growth_margins_per_day` shows the "
            f"combination reduces but does not reverse every resistant clone's growth advantage: "
            f"{', '.join(positive_margin_clones) if positive_margin_clones else 'none'} still "
            "have a small POSITIVE net margin at the central (unperturbed) parameter estimate, "
            "meaning that if such a clone is present at all (whether pre-existing or acquired) "
            "and large enough for the remaining follow-up window, it will deterministically "
            "regrow regardless of mutation-timing luck -- explaining why 'subclone present' "
            "below is not merely worse but essentially guaranteed to progress. This is a more "
            "precise statement than earlier framing elsewhere in this module describing the "
            "combination as merely 'slowing' these routes: at this illustrative potency, for two "
            "of three resistant clones, it slows the sensitive bulk and shrinks (without "
            "reversing) the resistant clones' own advantage -- whether a specific dog experiences "
            "that as a cure or a delayed relapse depends almost entirely on whether one of those "
            "clones gets a large enough foothold, not on chance once it has. A high ICC therefore "
            "means personalized diagnostics (biopsy, deep/ctDNA sequencing for a pre-existing "
            "subclone, therapeutic drug monitoring) could be unusually informative for this "
            "specific combination and dose -- not a general property of all cancer therapies."
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


def vaccine_epitope_binding_demo(out: Path, lengths: list[int] = (9, 10, 11)) -> None:
    """Runs each `vaccine_antigen_peptides` candidate against every `CHARACTERIZED_DLA_I_ALLELES`
    allele via IEDB's two real MHC-I methods confirmed to support any canine allele
    (`CONSENSUS_METHODS`: netmhcpan_el and netmhcpan_ba), reporting the best (by the EL method's
    ranking, kept as the primary method for consistency with earlier phases of this module) window
    per (peptide, allele) pair, both methods' percentile rank/class for that window, and whether
    the two independently-trained methods agree.
    """
    out.mkdir(parents=True, exist_ok=True)
    structure_cache = out / "structures"
    peptides = vaccine_antigen_peptides(structure_cache)
    lengths = list(lengths)
    primary_method = CONSENSUS_METHODS[0]

    rows = []
    all_predictions = []
    for mutation_label, peptide in peptides.items():
        predictions = fetch_consensus_binding_predictions(peptide, list(CHARACTERIZED_DLA_I_ALLELES), lengths)
        predictions.insert(0, "mutation", mutation_label)
        predictions.insert(1, "vaccine_peptide", peptide)
        all_predictions.append(predictions)
        for allele, info in CHARACTERIZED_DLA_I_ALLELES.items():
            allele_predictions = predictions[predictions["allele"] == allele]
            best = allele_predictions.loc[allele_predictions[f"percentile_rank_{primary_method}"].idxmin()]
            rows.append({
                "mutation": mutation_label, "vaccine_peptide": peptide,
                "dla_allele": info["common_name"], "best_predicted_9to11mer": best["peptide"],
                **{f"percentile_rank_{m}": float(best[f"percentile_rank_{m}"]) for m in CONSENSUS_METHODS},
                **{f"binding_class_{m}": best[f"binding_class_{m}"] for m in CONSENSUS_METHODS},
                "methods_agree": bool(best["methods_agree"]),
            })
    summary_table = pd.DataFrame(rows)
    summary_table.to_csv(out / "vaccine_epitope_binding.csv", index=False)
    pd.concat(all_predictions, ignore_index=True).to_csv(out / "vaccine_epitope_binding_raw.csv", index=False)

    summary = {
        "peptides": peptides,
        "antigen_targets": VACCINE_ANTIGEN_TARGETS,
        "alleles_tested": CHARACTERIZED_DLA_I_ALLELES,
        "methods_tested": list(CONSENSUS_METHODS),
        "lengths_tested": lengths,
        "results": rows,
        "consensus_agreement_rate": float(summary_table["methods_agree"].mean()) if len(summary_table) else None,
        "tool_provenance": (
            "Real, live query to two of IEDB's MHC-I binding-prediction methods "
            "(tools-cluster-interface.iedb.org/tools_api/mhci/): netmhcpan_el (trained on mass-"
            "spectrometry-eluted ligand data) and netmhcpan_ba (trained on quantitative binding-"
            "affinity data) -- the only two of IEDB's several MHC-I methods confirmed live to "
            "support any canine DLA allele at all (ann, smm, smmpmbec, pickpocket, consensus, "
            "and netmhccons were all checked and return none). A real, if narrower-than-"
            "pVACtools'-13-algorithm-ensemble, consensus check: two genuinely different training "
            "objectives, not the same predictor queried twice. Vaccine peptides are built fresh "
            "from the real canine AlphaFold/UniProt sequence via vaccine_antigen_peptides, not "
            "hardcoded. Canine MHC class II (CD4+ T-cell axis) was checked and found to have no "
            "supporting method at all in IEDB for any DLA class II allele -- not attempted here "
            "rather than approximated with a human-allele substitute."
        ),
        "unverified_extrapolations": [
            ("no specific dog's actual DLA genotype was typed -- no such tool exists in "
             "reusable, off-the-shelf form (see dla_binding module docstring), and no dog's "
             "sequencing reads exist in this project to type; the three alleles tested are the "
             "most-studied, published DLA-88 allotypes standing in for 'a dog', not any "
             "particular dog's real, unmeasured genotype"),
            ("a strong predicted binding percentile rank is necessary but not sufficient for "
             "actual T-cell immunogenicity in vivo -- it predicts peptide-MHC affinity, not "
             "whether a functional T-cell repertoire against that peptide-MHC complex exists, "
             "escapes central tolerance, or survives suppression in the tumor microenvironment"),
            ("the CD4+/MHC class II axis is entirely unchecked here (no tool exists for canine "
             "class II alleles), despite real human precedent for CD4+-T-cell-mediated tumor "
             "regression against a KRAS-mutant peptide independent of MHC-I presentation"),
            ("whether localized PIHS specifically carries any of these three mutations remains "
             "entirely unconfirmed, as flagged throughout this module"),
        ],
        "warning": (
            "This checks whether the candidate vaccine peptides *could* plausibly be presented "
            "by real, characterized canine MHC-I molecules, and whether two independently-"
            "trained methods agree on that -- a real, structurally meaningful question -- not "
            "whether the vaccine would work in any given dog, which also depends on that dog's "
            "own (untyped) DLA genotype, T-cell repertoire (including the unchecked CD4+ axis), "
            "and tumor immune microenvironment, none of which this checks."
        ),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


def pulmonary_two_compartment_demo(out: Path, cdk46_max_kill: float = 0.0,
                                   debulking_fraction: float = DEBULKING_FRACTION,
                                   trials: int = 300, horizon_days: int = 730,
                                   preexisting_prob: float = _PREEXISTING_PROB_CENTRAL,
                                   seed: int = 7) -> None:
    """Sweeps `NODAL_INVOLVEMENT_PROB_SWEEP` for the localized pulmonary HS scenario, and
    contrasts the result against what a single-compartment model (as used throughout this
    module's CNS/PIHS scenarios) would have naively predicted by implicitly assuming debulking
    reaches all disease -- i.e. `nodal_involvement_prob=0` -- showing concretely how much that
    assumption can overstate the benefit of surgery once undetected regional disease is plausible.
    """
    out.mkdir(parents=True, exist_ok=True)
    scenarios = localized_pulmonary_scenarios(cdk46_max_kill, debulking_fraction, NODAL_INVOLVEMENT_PROB_SWEEP)
    css_2 = CDK46_ILLUSTRATIVE_CSS_NM if cdk46_max_kill > 0 else None

    rows, outcomes = [], {}
    for nodal_prob, (model, css, seeding_rates, debulk, _) in scenarios.items():
        outcome = run_monte_carlo_two_compartment(
            model, css, horizon_days, seeding_rates, nodal_involvement_prob=nodal_prob,
            nodal_seed_fraction=NODAL_SEED_FRACTION, debulking_fraction=debulk, trials=trials,
            preexisting_prob=preexisting_prob, initial_burden=_PULMONARY_BASELINE_BURDEN,
            css_reference_2=css_2, seed=seed)
        outcomes[nodal_prob] = outcome
        ttp = outcome.time_to_progression[outcome.progressed]
        mechanism_counts = pd.Series(outcome.dominant_mechanism).value_counts()
        mechanism_fractions = (mechanism_counts.reindex(["durable_response"] + CLONE_NAMES[1:], fill_value=0)
                              / len(outcome.dominant_mechanism))
        compartment_counts = pd.Series(outcome.dominant_compartment).value_counts()
        compartment_fractions = (compartment_counts.reindex(["none", "primary", "nodal"], fill_value=0)
                                / len(outcome.dominant_compartment))
        rows.append({
            "nodal_involvement_prob": nodal_prob,
            "probability_durable_response": float(1 - outcome.progressed.mean()),
            "probability_progression": float(outcome.progressed.mean()),
            "median_time_to_progression_days": float(np.median(ttp)) if ttp.size else None,
            "fraction_trials_with_nodal_disease": float(outcome.has_nodal_involvement.mean()),
            **{f"mechanism_{mechanism}": float(value) for mechanism, value in mechanism_fractions.items()},
            **{f"relapse_from_{compartment}": float(value) for compartment, value in compartment_fractions.items()
               if compartment != "none"},
        })
    table = pd.DataFrame(rows)
    table.to_csv(out / "pulmonary_two_compartment_sensitivity.csv", index=False)

    naive_durable = float(1 - outcomes[0.0].progressed.mean())

    days = np.arange(horizon_days + 1)
    fig, axes = plt.subplots(1, 3, figsize=(15.5, 4.5))
    for nodal_prob, outcome in outcomes.items():
        combined = outcome.primary_trajectories.sum(axis=2) + outcome.nodal_trajectories.sum(axis=2)
        axes[0].plot(days, np.median(combined, axis=0), label=f"P(nodal)={nodal_prob}")
    axes[0].set(xlabel="day", ylabel="median combined tumor burden",
               title="localized pulmonary HS: primary + nodal")
    axes[0].legend(fontsize=7)
    axes[1].plot(table["nodal_involvement_prob"], table["probability_durable_response"],
                marker="o", color="tab:blue")
    axes[1].axhline(naive_durable, color="gray", linestyle="--", linewidth=1,
                    label="naive single-compartment (assumes surgery reaches everything)")
    axes[1].set(xlabel="P(regional nodal involvement at diagnosis)", ylabel="P(durable response)",
               title="does undetected nodal disease erase the surgery benefit?", ylim=(0, 1))
    axes[1].legend(fontsize=6)
    relapse_columns = [c for c in table.columns if c.startswith("relapse_from_")]
    table.set_index("nodal_involvement_prob")[relapse_columns].plot(kind="bar", stacked=True, ax=axes[2])
    axes[2].set(ylabel="fraction of trials that relapsed",
               title="relapse source: primary regrowth vs. nodal disease")
    axes[2].legend(fontsize=7)
    fig.tight_layout(); fig.savefig(out / "pulmonary_two_compartment.png", dpi=160); plt.close(fig)

    summary = {
        "cdk46_max_kill_used": cdk46_max_kill, "debulking_fraction": debulking_fraction,
        "preexisting_prob_used": preexisting_prob, "nodal_seed_fraction": NODAL_SEED_FRACTION,
        "sensitivity": rows, "case_series": PULMONARY_HS_CASE_SERIES,
        "full_systemic_exposure_note": (
            "Uses dog_preset's full systemic trametinib exposure (Cmax ~1640 nM), not the "
            "15%-brain-penetration-discounted concentration used in the CNS/PIHS scenarios -- "
            "lung tissue has no comparable barrier. Verified directly (clone_growth_margins) "
            "that this does not, by itself, resolve the same two-of-three-clones-still-positive-"
            "margin problem found in the CNS scenarios: those clones resist trametinib via a "
            "capped maximum kill rate, not merely insufficient concentration, so removing the "
            "brain-penetration penalty does not remove the need for a higher-potency CDK4/6i or "
            "a vaccine -- it mainly affects how quickly the drug-sensitive bulk of the tumor "
            "responds, not whether the resistant routes are closed."
        ),
        "regimen_dependence_note": (
            "At this demo's default (trametinib monotherapy, cdk46_max_kill=0.0), the effect of "
            "nodal_involvement_prob on overall durable-response probability is small and can be "
            "within ordinary Monte Carlo noise (see the mechanism_pathway_reactivation/"
            "relapse_from_nodal columns for the underlying, more visible per-mechanism signal): "
            "at full systemic exposure without a second drug, two of three resistant clones' "
            "growth margins are strongly positive (see clone_growth_margins), so an existing "
            "subclone is already close to guaranteed to reach detectable size within a "
            "multi-year horizon regardless of which compartment it started in -- debulking "
            "placement barely matters when relapse is already nearly certain either way. Rerun "
            "with the CDK4/6i-combination arm (cdk46_max_kill=0.05, where margins sit close to "
            "the suppression threshold) to see the effect clearly: in one earlier check at "
            "different trial parameters this showed durable response consistently and robustly "
            "lower with nodal_involvement_prob=1.0 than with 0.0; a follow-up rerun at "
            "trials=1000/seed=7 found a much smaller gap (99.7% vs 99.3%) than that earlier "
            "check reported (94.4% vs 88.4%) -- treat the direction (undebulked regional disease "
            "matters most when the rest of the regimen is otherwise close to working) as more "
            "reliable than either specific magnitude, and rerun before quoting a number."
        ),
        "unverified_extrapolations": [
            ("no precise nodal-involvement rate was published for this case series ('many "
             "cases', not a percentage) -- NODAL_INVOLVEMENT_PROB_SWEEP is swept across an "
             "illustrative range, not fit to a reported number"),
            ("NODAL_SEED_FRACTION (relative size of a nodal deposit vs. the primary at "
             "diagnosis) is an illustrative placeholder; no measurement of this exists for "
             "canine HS"),
            ("assumes lymphadenectomy is not performed alongside lobectomy -- if regional nodal "
             "dissection is standard practice for this presentation, the nodal compartment "
             "would also be partially debulked, which this scenario does not model"),
            ("assumes localized pulmonary HS carries the same PTPN11/KRAS-dominated driver spectrum "
             "as systemic HS -- unconfirmed, no sequencing of this presentation has been "
             "published, the same caveat attached to every scenario in this module"),
            ("reuses dog_preset's baseline mechanism-weight spectrum unchanged; no this presentation-"
             "specific germline locus exists to justify reweighting it, deliberately, for the "
             "same reason canine_cns_hs_scenarios does not offer an unsequenced-breed option"),
        ],
        "warning": (
            "Demonstrates how much a single-compartment model (implicitly assuming surgery "
            "reaches all disease, as used throughout this module's CNS/PIHS scenarios) can "
            "overstate durable-response probability once regional disease the surgeon can't "
            "reach becomes plausible -- read the gap between the dashed naive line and the "
            "swept curve as the size of that overstatement, not as a calibrated real-world "
            "estimate for any specific dog."
        ),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


def mapk_resistance_demo(out: Path, species: str = "dog", trials: int = 300,
                         horizon_days: int = 730, seed: int = 7) -> None:
    """Run the Monte Carlo escape model across a `preexisting_prob` sweep, not one fixed value.
    `preexisting_prob` (whether a resistant subclone already exists at treatment start) is the
    single most influential parameter in this model and has no HS-specific source; reporting a
    durable-response probability at one asserted value would mostly reflect that choice, not a
    result.
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
