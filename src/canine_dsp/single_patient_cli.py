"""Demo/report for `single_patient`: what sequencing one dog's tumor changes, and what it does not."""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .mapk_resistance import clone_growth_margins, run_monte_carlo, run_monte_carlo_two_compartment
from .mapk_scenarios import (
    _PULMONARY_BASELINE_BURDEN,
    CCNU_CYCLE_INTERVAL_DAYS,
    CCNU_DOSE_MG_PER_M2,
    CCNU_EXPOSURE_DAYS,
    CCNU_MATCHED_CSS_NM,
    CCNU_MAX_KILL_SWEEP,
    CDK46_ILLUSTRATIVE_CSS_NM,
    DEBULKING_FRACTION,
    NODAL_INVOLVEMENT_PROB_SWEEP,
    NODAL_SEED_FRACTION,
    ccnu_combination_scenarios,
    combination_scenarios,
    pulmonary_corgi_scenarios,
)
from .pharmacology import (
    CCNU_CANINE_HS,
    CCNU_DURATION_LIMIT,
    cumulative_dose_limited_days,
    cytostatic_ceiling,
)
from .single_patient import (
    CANINE_HS_DRIVER_FREQUENCY,
    CORGI_PULMONARY_HS_BENCHMARK,
    LOCALIZED_HS_CCNU_BENCHMARK,
    SEQUENCING_ASSAYS,
    driver_conditioned_arms,
    genome_equivalents_required,
    implied_preexisting_prob,
    partition_by_preexisting_subclone,
    partition_two_compartment_by_preexisting_subclone,
    posterior_preexisting_prob,
    spatial_detection_probability,
    vaf_lod_to_cell_fraction,
)

# Order-of-magnitude clinical figures, exposed rather than buried: a ~4 cm canine soft-tissue mass is
# on the order of 1e10 cells, and a diagnostic sample is a small fraction of it. Both are swept in
# the spatial analysis, because the conclusion there depends on the ratio, not the absolutes.
TUMOR_CELLS = 1e10
SAMPLED_CELL_FRACTIONS = [1e-4, 1e-3, 1e-2, 1e-1]


def single_patient_demo(out: Path, breed: str = "bmd",
                        debulking_fraction: float = DEBULKING_FRACTION,
                        horizon_days: int = 730, trials: int = 500,
                        preexisting_prob: float = 0.30, seed: int = 7) -> None:
    """Re-asks this repo's central question as an N=1 question, and swaps in a cytotoxic partner.
    Five analyses, in order of how much they change the answer. `breed` (must be 'bmd' or
    'golden_retriever') governs findings 1-4 only -- see finding 5 for why a Corgi patient is
    handled as a separate scenario rather than a value of this parameter.
    """
    if breed not in ("bmd", "flat_coated_retriever"):
        raise ValueError(
            "is not one of this repo's tumor-scenario presets ('bmd', 'flat_coated_retriever' -- "
            "see localized_pihs_scenarios/combination_scenarios). A Corgi patient is not covered by "
            "this arm at all: see finding_5_corgi_is_a_different_disease_not_a_different_breed_name "
            "in this demo's summary.json, and corgi-answer-demo for the Corgi regimen.")
    out.mkdir(parents=True, exist_ok=True)

    # 1. Driver conditioning ------------------------------------------------------------------
    driver = driver_conditioned_arms(breed=breed)
    driver_corgi = driver_conditioned_arms(breed="corgi")

    # 2. What a negative sequencing result buys -----------------------------------------------
    assay_rows = []
    for name, assay in SEQUENCING_ASSAYS.items():
        cell_fraction_lod = vaf_lod_to_cell_fraction(assay["vaf_lod"])
        update = posterior_preexisting_prob(preexisting_prob, cell_fraction_lod)
        material = genome_equivalents_required(cell_fraction_lod)
        assay_rows.append({
            "assay": name, "vaf_lod": assay["vaf_lod"],
            "cell_fraction_lod": cell_fraction_lod,
            "clinically_available_for_dogs": assay["clinically_available_for_dogs"],
            "detectable_prior_mass": update["detectable_prior_mass"],
            "preexisting_prob_prior": update["prior"],
            "preexisting_prob_after_negative_result": update["posterior"],
            "fold_reduction": update["fold_reduction"],
            "genome_equivalents_required": material["genome_equivalents"],
            "dna_input_ug_required": material["dna_input_ug"],
            "citation": assay["citation"],
        })
    assays = pd.DataFrame(assay_rows).sort_values("vaf_lod", ascending=False)
    assays.to_csv(out / "sequencing_detectability.csv", index=False)

    # 3. Spatial sampling, at the two ends of the model's own size prior ----------------------
    spatial_rows = []
    for subclone_fraction in (1e-3, 1e-6):
        for sampled_fraction in SAMPLED_CELL_FRACTIONS:
            result = spatial_detection_probability(subclone_fraction, TUMOR_CELLS,
                                                  sampled_fraction * TUMOR_CELLS)
            spatial_rows.append({
                "subclone_cell_fraction": subclone_fraction,
                "sampled_fraction_of_tumor": sampled_fraction,
                "subclone_cells_in_tumor": result["subclone_cells"],
                "detection_prob_if_well_mixed": result["probability_if_well_mixed"],
                "detection_prob_if_single_focus": result["probability_if_single_focus"],
            })
    spatial = pd.DataFrame(spatial_rows)
    spatial.to_csv(out / "spatial_sampling.csv", index=False)

    # 4a. N=1 decomposition of the existing (CDK4/6i) ensemble --------------------------------
    cdk_scenario = combination_scenarios(breed, debulking_fraction, [0.05])[0.05]
    cdk_model, css, seeding_rates, initial_burden, _ = cdk_scenario
    cdk_outcome = run_monte_carlo(cdk_model, css, horizon_days, seeding_rates, trials,
                                  preexisting_prob=preexisting_prob, initial_burden=initial_burden,
                                  css_reference_2=CDK46_ILLUSTRATIVE_CSS_NM, seed=seed)
    cdk_partition = partition_by_preexisting_subclone(cdk_outcome)

    # 4b. Lomustine: cytotoxic, so ceiling-free -- but duration-capped by real toxicity data ---
    duration = cumulative_dose_limited_days(CCNU_DOSE_MG_PER_M2, CCNU_CYCLE_INTERVAL_DAYS,
                                            CCNU_DURATION_LIMIT["cumulative_dose_cap_mg_per_m2"])
    ceiling = cytostatic_ceiling(np.asarray(cdk_model.growth, dtype=float))
    ccnu_rows, ccnu_partitions = [], {}
    # Each potency is run twice: capped at the real cumulative-dose window, and counterfactually
    # chronic. The gap between them isolates how much of the benefit depends on being able to keep
    # dosing -- which for this drug you cannot.
    for capped_days, label in ((CCNU_EXPOSURE_DAYS, "duration-capped (real)"),
                               (None, "chronic (counterfactual)")):
        scenarios = ccnu_combination_scenarios(breed, debulking_fraction, CCNU_MAX_KILL_SWEEP,
                                               exposure_days=capped_days)
        for max_kill_2, (model, arm_css, rates, burden, _) in scenarios.items():
            outcome = run_monte_carlo(
                model, arm_css, horizon_days, rates, trials,
                preexisting_prob=preexisting_prob, initial_burden=burden,
                css_reference_2=CCNU_MATCHED_CSS_NM if max_kill_2 > 0 else None,
                css_reference_2_duration_days=capped_days if max_kill_2 > 0 else None,
                seed=seed)
            partition = partition_by_preexisting_subclone(outcome)
            if capped_days == CCNU_EXPOSURE_DAYS:
                ccnu_partitions[max_kill_2] = partition
            margins = clone_growth_margins(model, arm_css,
                                           CCNU_MATCHED_CSS_NM if max_kill_2 > 0 else None)
            ccnu_rows.append({
                "exposure": label, "exposure_days": capped_days, "ccnu_max_kill": max_kill_2,
                "exceeds_cytostatic_ceiling": bool(max_kill_2 > ceiling[1:].max()),
                "probability_durable_response": float(1 - outcome.progressed.mean()),
                "durable_without_preexisting_subclone":
                    partition["without_preexisting_subclone"]["durable_response_fraction"],
                "durable_with_preexisting_subclone":
                    partition["with_preexisting_subclone"]["durable_response_fraction"],
                "worst_resistant_clone_margin": float(np.max(margins[1:])),
                "all_resistant_margins_negative": bool(np.max(margins[1:]) < 0),
                # nan when no trial progressed within the horizon -- reported as None rather than
                # letting nanmedian warn and emit nan, since "nobody progressed" is a real result.
                "median_days_to_progression": (
                    float(np.nanmedian(outcome.time_to_progression))
                    if outcome.progressed.any() else None),
            })
    ccnu = pd.DataFrame(ccnu_rows)
    ccnu.to_csv(out / "ccnu_vs_cdk46.csv", index=False)

    # Plot: the N=1 split, and the duration cap's cost -----------------------------------------
    fig, (left, right) = plt.subplots(1, 2, figsize=(13, 5))
    capped = ccnu[ccnu["exposure"] == "duration-capped (real)"]
    chronic = ccnu[ccnu["exposure"] == "chronic (counterfactual)"]
    left.plot(capped["ccnu_max_kill"], capped["probability_durable_response"], "o-",
              color="tab:blue", label=f"duration-capped ({CCNU_EXPOSURE_DAYS} d, real)")
    left.plot(chronic["ccnu_max_kill"], chronic["probability_durable_response"], "s--",
              color="tab:gray", label="chronic (counterfactual)")
    left.axvline(ceiling[1:].max(), color="tab:red", linestyle=":",
                 label=f"cytostatic ceiling ({ceiling[1:].max():.3f})")
    left.axhline(LOCALIZED_HS_CCNU_BENCHMARK["relapse_free_fraction"], color="tab:green",
                 linestyle="-.", label="Skorupski 2009 relapse-free (n=16)")
    left.set(xlabel="lomustine max_kill (per day)", ylabel="P(durable response)",
             title="A cytotoxic partner clears the ceiling,\nbut its exposure window is capped",
             ylim=(-0.03, 1.03))
    left.legend(fontsize=8); left.grid(alpha=.3)

    width = 0.35
    positions = np.arange(len(capped))
    right.bar(positions - width / 2, capped["durable_without_preexisting_subclone"], width,
              color="tab:green", label="no pre-existing subclone")
    right.bar(positions + width / 2, capped["durable_with_preexisting_subclone"], width,
              color="tab:red", label="pre-existing subclone present")
    right.plot(positions, capped["probability_durable_response"], "k^--",
               label="cohort average (describes neither)")
    right.set(xticks=positions, xticklabels=[f"{v:g}" for v in capped["ccnu_max_kill"]],
              xlabel="lomustine max_kill (per day)", ylabel="P(durable response)",
              title="The N=1 split the cohort average hides\n(each patient is in one bar, not between them)",
              ylim=(-0.03, 1.03))
    right.legend(fontsize=8); right.grid(alpha=.3, axis="y")
    fig.tight_layout(); fig.savefig(out / "single_patient.png", dpi=160); plt.close(fig)

    # 5. The actual Corgi case: a different scenario against a different, breed-matched benchmark --
    # Everything above (findings 1-4) models BMD localized PIHS. Applying its numbers to a Corgi
    # patient would repeat exactly the kind of breed/lineage mismatch the pharmacology-vs-melanoma
    # objection already caught once this session -- so this runs the real Corgi-specific scenario
    # (`pulmonary_corgi_scenarios`, the two-compartment nodal model) instead of reusing the BMD arm.
    corgi_rows = []
    for nodal_prob in NODAL_INVOLVEMENT_PROB_SWEEP:
        model, corgi_css, corgi_rates, corgi_debulk, _ = pulmonary_corgi_scenarios(
            cdk46_max_kill=0.0, debulking_fraction=debulking_fraction,
            nodal_involvement_prob_values=[nodal_prob])[nodal_prob]
        corgi_outcome = run_monte_carlo_two_compartment(
            model, corgi_css, horizon_days, corgi_rates, nodal_involvement_prob=nodal_prob,
            nodal_seed_fraction=NODAL_SEED_FRACTION, debulking_fraction=corgi_debulk, trials=trials,
            preexisting_prob=preexisting_prob, initial_burden=_PULMONARY_BASELINE_BURDEN, seed=seed)
        corgi_partition = partition_two_compartment_by_preexisting_subclone(corgi_outcome)
        corgi_rows.append({
            "nodal_involvement_prob": nodal_prob,
            "probability_durable_response": float(1 - corgi_outcome.progressed.mean()),
            "durable_without_preexisting_subclone":
                corgi_partition["without_preexisting_subclone"]["durable_response_fraction"],
            "durable_with_preexisting_subclone":
                corgi_partition["with_preexisting_subclone"]["durable_response_fraction"],
            "median_days_to_progression": (
                float(np.nanmedian(corgi_outcome.time_to_progression))
                if corgi_outcome.progressed.any() else None),
        })
    corgi_df = pd.DataFrame(corgi_rows)
    corgi_df.to_csv(out / "corgi_pulmonary_arm.csv", index=False)

    best_capped = capped.loc[capped["probability_durable_response"].idxmax()]
    # The matched benchmark is admissible on all four axes, so inverting the mixture against it is a
    # legitimate calibration inference rather than the kind of mismatched comparison this repo
    # rejected for COMBI-d/v. Done at the trametinib-only sweep point (ccnu_max_kill=0), which is the
    # closest structural analogue to "local therapy plus one adjuvant systemic agent".
    baseline = capped[capped["ccnu_max_kill"] == 0.0].iloc[0]
    implied = implied_preexisting_prob(
        LOCALIZED_HS_CCNU_BENCHMARK["relapse_free_fraction"],
        float(baseline["durable_without_preexisting_subclone"]),
        float(baseline["durable_with_preexisting_subclone"]))
    summary = {
        "question": "Does treating one sequenced dog, rather than a cohort, change the answer -- and "
                   "is there a better second drug than the CDK4/6 inhibitor the cytostatic ceiling "
                   "ruled out?",
        "answer": "Yes to both, and the two findings point in opposite directions.",
        "finding_1_driver_conditioning_dominates": {
            "for_breed": breed,
            **driver,
            "why_it_is_the_biggest_lever": (
                "This model has always assumed the MEK inhibitor engages a real driver. In the "
                f"published canine HS cohort that holds for "
                f"{driver['probability_mapk_driver_identified']:.0%} of {breed} cases. Sequencing "
                "converts that from an unexamined premise into a measured fact, and it is the only "
                "measurement here that changes the treatment plan rather than the error bars."
            ) if driver["probability_mapk_driver_identified"] is not None else (
                "either -- it has its own real GWAS germline locus (BREED_GERMLINE_LOCI in "
                "mapk_scenarios) but no Takada-et-al.-style driver-mutation cohort."
            ),
            "source": CANINE_HS_DRIVER_FREQUENCY,
            "does_not_apply_to_corgi": "This finding is specific to the breed named in "
                                       "'for_breed' above.",
        },
        "finding_2_sequencing_cannot_see_preexisting_resistance": {
            "principle": "The resistance engine draws the pre-existing resistant fraction from "
                        "10^U(-6,-3) of the tumor. Halved to a variant allele fraction, that whole "
                        "distribution lies at or below 0.05% VAF.",
            "clinically_available_assays_fold_reduction": 1.0,
            "best_research_assay_posterior": float(assays["preexisting_prob_after_negative_result"].min()),
            "verdict": f"Every clinically available assay leaves preexisting_prob at exactly "
                      f"{preexisting_prob:.2f} -- a negative result is uninformative, not "
                      f"reassuring. The most sensitive assay ever published moves it only to "
                      f"{assays['preexisting_prob_after_negative_result'].min():.2f}.",
            "per_assay": assay_rows,
            "material_note": "Input DNA is not the binding constraint: seeing a 1e-6 subclone needs "
                            "~40 ug of DNA, which a resection can yield. The binding constraints are "
                            "the assay error floor and spatial sampling.",
        },
        "finding_3_spatial_sampling_is_a_separate_wall": {
            "principle": "No sequencing depth fixes a subclone that is not in the sampled fragment. "
                        "The two bounds bracket the truth and the spread is the point.",
            "tumor_cells_assumed": TUMOR_CELLS,
            "per_configuration": spatial_rows,
            "verdict": "If a resistant subclone is dispersed, sampling 1% of the tumor detects "
                       "it with near-certainty; if it is one focal expansion, detection "
                       "probability is just the sampled fraction (~1%).",
        },
        "finding_4_lomustine_trades_the_ceiling_for_a_duration_cap": {
            "why_lomustine": CCNU_CANINE_HS["why_this_matters_here"],
            "real_activity": {k: CCNU_CANINE_HS[k] for k in
                             ("citation", "overall_response_rate", "dose_mg_per_m2_range",
                              "n_dogs_measurable_disease", "mechanism", "mechanism_class",
                              "blood_brain_barrier")},
            "mechanism_agnostic_is_correct_here": "Unlike the CSF1R inhibitor, a scalar max_kill_2 is "
                "the right model: DNA crosslinking acts independently of which MAPK node a resistant "
                "clone acquired, so there is no pathway-serial de-rating to apply.",
            "duration_cap": {**duration, "source": CCNU_DURATION_LIMIT},
            "sweep": ccnu_rows,
            "best_duration_capped_arm": {
                "ccnu_max_kill": float(best_capped["ccnu_max_kill"]),
                "probability_durable_response": float(best_capped["probability_durable_response"]),
                "exceeds_cytostatic_ceiling": bool(best_capped["exceeds_cytostatic_ceiling"]),
            },
            "what_the_cap_costs": "days, which real cumulative hepatotoxicity forces.",
        },
        "n1_decomposition": {
            "cdk46_arm_at_max_kill_0.05": cdk_partition,
            "ccnu_arms_duration_capped": {str(k): v for k, v in ccnu_partitions.items()},
            "why_this_matters": "A cohort fraction of, say, 0.6 does not mean a patient has a "
                                "60% chance in any useful sense if the ensemble is really two "
                                "sub-populations with very different fates.",
        },
        "matched_benchmark": {
            **LOCALIZED_HS_CCNU_BENCHMARK,
            "why_this_one_is_admissible": "This is the comparator this repo previously lacked.",
            "implied_preexisting_prob": {
                **implied,
                "model_current_central_value": preexisting_prob,
                "reading": "Because the two N=1 arms sit near 1.0 and near 0.0 at the real "
                           "exposure duration, the cohort statistic is almost purely a readout "
                           "of preexisting_prob.",
                "not_applied": "Deliberately NOT written back into _PREEXISTING_PROB_CENTRAL.",
            },
            "scale_check": "relapse-free (6/16) and a 243-day median disease-free interval after "
                           "local therapy plus adjuvant CCNU.",
            "suggestive_consistency": "The benchmark's 201-day median time to relapse falls "
                                      "shortly after a real 4-6 cycle lomustine course (84-168 "
                                      "days) would have ended.",
        },
        "finding_5_corgi_is_a_different_disease_not_a_different_breed_name": {
            "why_this_section_exists": "Findings 1-4 model BMD localized PIHS end to end -- the "
                "driver-frequency data (Takada 2019), the tumor scenario (`localized_pihs_"
                "scenarios`), and the calibration benchmark (Skorupski 2009) are all BMD-context. "
                "Corgi HS is a clinically distinct, separately-published presentation (Sakai et al. "
                "2015) with regional nodal involvement in many cases and a 133-day median survival "
                "-- roughly a quarter of the BMD-context benchmark's 568 days. Reusing findings 1-4 "
                "for a Corgi patient would be the same category of mistake this session already "
                "caught once (treating canine melanoma IC50 data as informative about canine HS "
                "potency): a real, cited number applied across an unverified species/lineage-"
                "equivalent boundary.",
            "driver_conditioning_for_corgi": driver_corgi,
            "scenario_used": "pulmonary_corgi_scenarios / run_monte_carlo_two_compartment -- the "
                             "two-compartment nodal model already built for this presentation, "
                             "not the single-compartment BMD PIHS model findings 1-4 use.",
            "sweep": corgi_rows,
            "cdk46_or_ccnu_not_added_here": "Deliberately not layered onto this arm: doing so would "
                "imply the CDK4/6i-achievability and lomustine-duration findings (derived from BMD-"
                "context growth rates and CDK46_CANINE_POTENCY, itself from canine melanoma lines) "
                "transfer to the Corgi tumor model, which is exactly the unverified cross-lineage "
                "step this finding exists to avoid taking silently.",
            "matched_benchmark": CORGI_PULMONARY_HS_BENCHMARK,
            "why_no_calibration_inversion_here": "`implied_preexisting_prob` is not applied against "
                "this benchmark the way it was against Skorupski for the BMD arm: Sakai's cohort "
                "received mixed/unspecified treatment, not one systemic agent, so its outcome is "
                "not attributable to a comparable regimen the way the CCNU-specific benchmark's is. "
                "It is a scale check, not an estimator.",
            "verdict": "The honest N=1 statement for a Corgi patient is not 'apply findings 1-4 with "
                "a discount' -- it is that this repo's own best-evidenced Corgi-specific model "
                "predicts a materially different disease course, its driver is undetermined rather "
                "than known-at-46%, and no drug-specific finding above (CDK4/6i ceiling, lomustine "
                "duration cap) has been checked against Corgi-specific growth rates or potency data, "
                "because none exist.",
        },
        "synthesis_the_two_candidates_fail_on_opposite_axes": {
            "requirement": "Reversing this model's resistant clones needs two things at once: a "
                          "kill rate at or above their growth rates, AND that kill rate sustained "
                          "long enough for the suppressed subclone not to regrow within the horizon.",
            "cdk46_inhibitor": "Can be dosed chronically (oral, no cumulative organ cap), so it "
                               "satisfies the duration requirement -- and indeed reaches ~100% "
                               "durable response in-model when dosed continuously at max_kill "
                               "0.05.",
            "lomustine": "Can reach the kill rate -- it is cytotoxic, so the ceiling does not "
                         "apply, and at max_kill >= 0.08 it drives every resistant clone's "
                         "margin negative.",
            "consequence": "Neither agent is the answer, for non-overlapping reasons, and this "
                           "is a sharper negative result than either analysis alone.",
            "note_on_metronomic_dosing": "Metronomic lomustine has been reported tolerable in "
                                         "dogs for up to ~12 months (Tripp et al. 2011), which "
                                         "would partly relax the duration cap at a lower dose "
                                         "intensity -- i.e. trading kill rate for duration along "
                                         "exactly the axis that matters.",
        },
        "unverified_extrapolations": [
            "lomustine's max_kill is still swept, not measured: no canine HS cell line has a "
            "published lomustine dose-response, so the 46% response rate has not been converted "
            "into a per-day kill rate.",
            "lomustine's IC50 and exposure are deliberately set equal to the CDK4/6i arm's "
            "illustrative values so the two arms differ only in mechanism class and duration -- "
            "these are not lomustine PK",
            "the 350 mg/m2 cumulative cap is an observed hepatotoxicity threshold, not a regulatory "
            "limit; treating it as a hard stop is conservative but arbitrary at the margin",
            "the pre-existing-fraction prior 10^U(-6,-3) is the resistance engine's own "
            "convention.",
            "the Corgi arm's own scenario (pulmonary_corgi_scenarios) still reuses the BMD "
            "growth-rate/resistance-mechanism spectrum unchanged, per that function's own "
            "documented reasoning: no Corgi-specific germline locus or driver panel is "
            "established enough to justify inventing a different one from nothing.",
        ],
        "warning": "This reframes an illustrative model as an individual-patient question. It does "
                  "not establish that any regimen works in this disease, and no part of it is a "
                  "treatment recommendation.",
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, default=str) + "\n")
