"""The culminating question: is a durable response achievable for one Corgi with this disease?

Assembles every constraint this repo established into a single conditional answer, rather than another
sweep. Deliberately built as its own demo because the Corgi arm of `single_patient_demo` was
trametinib monotherapy in a 4-clone model -- it could not express a vaccine at all, which is the
component the entire endurance case turned out to rest on.
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .antigen_convergence import (
    CONVERGENCE_ARGUMENT,
    mechanism_constraint_matrix,
    vaccine_potency_threshold,
)
from .mapk_resistance import run_monte_carlo_two_compartment
from .mapk_scenarios import (
    _PULMONARY_BASELINE_BURDEN,
    CCNU_EXPOSURE_DAYS,
    CCNU_MATCHED_CSS_NM,
    DEBULKING_FRACTION,
    DURABILITY_HORIZON_SWEEP,
    IMMUNE_ESCAPE_SEEDING_RATE,
    NODAL_INVOLVEMENT_PROB_SWEEP,
    NODAL_SEED_FRACTION,
    VACCINE_CLONE_NAMES,
    VACCINE_RAMP_DAYS,
    VACCINE_START_DAY,
    corgi_full_regimen_scenarios,
)
from .pharmacology import CCNU_CANINE_HS
from .single_patient import (
    CORGI_PULMONARY_HS_BENCHMARK,
    SEQUENCING_ASSAYS,
    driver_conditioned_arms,
    vaf_lod_to_cell_fraction,
)

# For ONE dog, the model's uncertain inputs split into two groups that could not be more different in
# what they imply for a treatment decision. This partition is the core N=1 contribution here: it is
# not "everything is uncertain", it is that the Corgi-specific structural risk happens to be
# measurable per patient while the generic one is not.
MEASURABLE_IN_ONE_DOG = {
    "driver_mutation_status": {
        "how": "tumor sequencing of the resection/biopsy specimen; a driver lesion is clonal or "
              "near-clonal (~25-50% VAF), orders of magnitude above every assay floor",
        "decides": "whether a MEK inhibitor is on-target at all AND whether a hotspot vaccine has an "
                  "antigen to target -- both halves of the regimen depend on the same answer",
        "status_for_corgi": "NEVER MEASURED IN ANY CORGI. This is the gate, and it is open.",
    },
    "regional_nodal_involvement": {
        "how": "staging: thoracic imaging, node aspirate/biopsy at diagnosis",
        "decides": "whether debulking can reach all disease, i.e. which compartment structure applies",
        "status_for_corgi": "unmeasured as a population RATE (Sakai et al. report 'many cases', no "
                           "percentage) but directly measurable in an individual patient -- so the "
                           "Corgi-specific structural risk is resolvable for one dog even though the "
                           "cohort rate is not",
    },
    "tumor_burden_and_resectability": {
        "how": "imaging plus surgical/histopathological margin assessment",
        "decides": "the model's initial_burden and debulking_fraction",
        "status_for_corgi": "routinely measurable",
    },
}

NOT_MEASURABLE_IN_ONE_DOG = {
    "preexisting_resistant_subclone": {
        "why_not": "the model's own size prior is 10^U(-6,-3) of tumor, i.e. <=0.05% VAF -- at or "
                  "below the detection floor of every clinically available assay, and mostly below "
                  "the best research assays too (see single_patient.posterior_preexisting_prob). "
                  "Spatial sampling is an independent second wall no sequencing depth fixes.",
        "consequence": "cannot be resolved before treatment, so a regimen whose outcome depends on it "
                      "is a regimen whose outcome cannot be predicted for this patient",
    },
    "vaccine_potency_in_this_dog": {
        "why_not": "no canine cancer vaccine trial exists for this disease; vaccine_max_kill is a "
                  "swept, unfitted parameter with no measured anchor in any species for this antigen",
        "consequence": "the threshold below is a target, not an achieved value -- exactly the "
                      "achievability question pharmacology.py asked of a CDK4/6 inhibitor and "
                      "answered NO for",
    },
    "antigen_loss_rate": {
        "why_not": "IMMUNE_ESCAPE_SEEDING_RATE is an illustrative constant ~200x below the "
                  "drug-resistance total; nothing in this repo or the literature constrains it for "
                  "canine HS",
        "consequence": "the one escape route no vaccine potency can cover, so its rate sets a ceiling "
                      "on durability that raising potency cannot lift",
    },
}


def corgi_answer_demo(out: Path, debulking_fraction: float = DEBULKING_FRACTION,
                      ccnu_max_kill: float = 0.08, trials: int = 250,
                      seed: int = 7) -> None:
    """Runs the full three-component regimen in the Corgi two-compartment scenario and answers.

    Sweeps nodal involvement x vaccine potency x `preexisting_prob` (0.30 central, 0.62 as implied by
    the matched BMD-context benchmark) x horizon, because the answer for one dog is a conditional
    statement, not a number: what is achievable given what can be measured, and what remains
    unresolvable regardless.
    """
    out.mkdir(parents=True, exist_ok=True)
    reference = corgi_full_regimen_scenarios(debulking_fraction, ccnu_max_kill,
                                            NODAL_INVOLVEMENT_PROB_SWEEP)
    any_model = next(iter(reference.values()))[0]
    threshold = vaccine_potency_threshold(np.asarray(any_model.growth), VACCINE_CLONE_NAMES)
    # Rounded so the swept value is a clean number, then used as the canonical threshold for the
    # >= comparison below. Comparing the rounded potency against the unrounded threshold would fail
    # on float representation (0.06 >= 0.058 + 0.002 is False), silently marking every arm as
    # sub-threshold and reporting the headline sensitivity fields as null.
    just_above = round(threshold["threshold_vaccine_max_kill"], 4)
    potencies = [0.0, 0.03, 0.05, just_above]

    rows = []
    for nodal_prob, (model, css, rates, debulk, _) in reference.items():
        for preexisting_prob in (0.30, 0.62):
            for vaccine_max_kill in potencies:
                for horizon_days in DURABILITY_HORIZON_SWEEP:
                    outcome = run_monte_carlo_two_compartment(
                        model, css, horizon_days, rates, nodal_involvement_prob=nodal_prob,
                        nodal_seed_fraction=NODAL_SEED_FRACTION, debulking_fraction=debulk,
                        trials=trials, preexisting_prob=preexisting_prob,
                        initial_burden=_PULMONARY_BASELINE_BURDEN,
                        css_reference_2=CCNU_MATCHED_CSS_NM if ccnu_max_kill > 0 else None,
                        css_reference_2_duration_days=(CCNU_EXPOSURE_DAYS if ccnu_max_kill > 0
                                                       else None),
                        vaccine_start_day=VACCINE_START_DAY, vaccine_ramp_days=VACCINE_RAMP_DAYS,
                        vaccine_max_kill=vaccine_max_kill,
                        immune_escape_seeding_rate=IMMUNE_ESCAPE_SEEDING_RATE,
                        clone_names=VACCINE_CLONE_NAMES, seed=seed)
                    compartments = pd.Series(outcome.dominant_compartment).value_counts(
                        normalize=True)
                    mechanisms = pd.Series(outcome.dominant_mechanism).value_counts(normalize=True)
                    rows.append({
                        "nodal_involvement_prob": nodal_prob,
                        "preexisting_prob": preexisting_prob,
                        "vaccine_max_kill": vaccine_max_kill,
                        "above_threshold": bool(vaccine_max_kill >= just_above),
                        "years": round(horizon_days / 365, 1),
                        "probability_durable_response": float(1 - outcome.progressed.mean()),
                        "nodal_relapse_share": float(compartments.get("nodal", 0.0)),
                        "immune_escape_share": float(mechanisms.get("immune_escape", 0.0)),
                    })
    grid = pd.DataFrame(rows)
    grid.to_csv(out / "corgi_regimen_grid.csv", index=False)

    ten_year = grid[grid["years"] == 10.0]
    # Does the answer survive the worst measurable configuration a Corgi could present with?
    worst = ten_year[(ten_year["nodal_involvement_prob"] == max(NODAL_INVOLVEMENT_PROB_SWEEP))
                     & (ten_year["preexisting_prob"] == 0.62)]
    worst_above = worst[worst["above_threshold"]]
    worst_below = worst[worst["vaccine_max_kill"] == 0.0]
    # Sensitivity to the unmeasurable parameter, above vs below threshold.
    def _spread(above: bool):
        subset = ten_year[(ten_year["above_threshold"] == above)
                          & (ten_year["nodal_involvement_prob"] == 0.4)]
        if above:
            pick = subset
        else:
            pick = subset[subset["vaccine_max_kill"] == 0.0]
        by_p = pick.groupby("preexisting_prob")["probability_durable_response"].mean()
        return float(by_p.max() - by_p.min()) if len(by_p) > 1 else None

    fig, (left, right) = plt.subplots(1, 2, figsize=(13, 5))
    for nodal_prob, style in zip(NODAL_INVOLVEMENT_PROB_SWEEP, ["o-", "s--", "^-.", "v:"]):
        arm = ten_year[(ten_year["nodal_involvement_prob"] == nodal_prob)
                       & (ten_year["preexisting_prob"] == 0.62)]
        left.plot(arm["vaccine_max_kill"], arm["probability_durable_response"], style,
                  label=f"nodal involvement {nodal_prob:g}")
    left.axvline(threshold["threshold_vaccine_max_kill"], color="tab:red", linestyle=":",
                 label=f"threshold {threshold['threshold_vaccine_max_kill']:.3f}/day")
    left.set(xlabel="vaccine max_kill (per day)", ylabel="P(durable response) at 10 years",
             ylim=(-0.03, 1.03),
             title="Corgi pulmonary, two-compartment, worst preexisting_prob (0.62)\n"
                   "nodal involvement barely matters above the threshold")
    left.legend(fontsize=8); left.grid(alpha=.3)

    for above, color, label in ((False, "tab:red", "vaccine off"), (True, "tab:blue",
                                                                    "above threshold")):
        arm = grid[(grid["above_threshold"] == above)
                   & (grid["nodal_involvement_prob"] == 0.4)
                   & (grid["preexisting_prob"] == 0.62)]
        if not above:
            arm = arm[arm["vaccine_max_kill"] == 0.0]
        right.plot(arm["years"], arm["probability_durable_response"], "o-", color=color, label=label)
    right.axhline(CORGI_PULMONARY_HS_BENCHMARK["median_survival_days"] / 3650, color="tab:green",
                  linestyle="-.",
                  label="Sakai 2015 median survival (133 d) as a fraction of 10 yr")
    right.set(xlabel="horizon (years)", ylabel="P(durable response)", ylim=(-0.03, 1.03),
              title="Endurance over time, nodal 0.4 / preexisting_prob 0.62")
    right.legend(fontsize=8); right.grid(alpha=.3)
    fig.tight_layout(); fig.savefig(out / "corgi_answer.png", dpi=160); plt.close(fig)

    summary = {
        "question": "If the goal is a durable response for the Corgi niche presentation, in ONE dog, "
                   "what is the answer?",
        "short_answer": (
            "Conditionally yes, and the condition is unusually clean: IF this dog's tumor is "
            "sequenced and carries a targetable MAPK hotspot, AND a vaccine against that hotspot "
            "reaches roughly "
            f"{threshold['threshold_vaccine_max_kill']:.3f}/day of kill, THEN the model gives a "
            "durable response that is robust to everything else -- including the two things that "
            "cannot be measured in this dog (pre-existing resistance) and the Corgi-specific "
            "structural risk (nodal disease surgery cannot reach). Below that potency the answer is "
            "no, and no amount of drug optimization substitutes. Neither condition is currently "
            "established for any Corgi."),
        "the_gate_is_sequencing": {
            **driver_conditioned_arms(breed="corgi"),
            "why_it_is_a_gate_and_not_a_discount": "Both halves of the regimen depend on the same "
                "answer. Without a MAPK driver the MEK inhibitor is off-target AND the hotspot "
                "vaccine has no antigen -- so antigen convergence, which is what makes the endurance "
                "case work, has nothing to converge on. This is the one measurement that changes "
                "whether to attempt the strategy at all rather than adjusting its odds.",
            "cost_of_being_wrong": "If sequenced and negative, the correct action is a different "
                                  "primary agent, not this regimen at lower expected value.",
        },
        "what_can_and_cannot_be_measured_in_one_dog": {
            "measurable": MEASURABLE_IN_ONE_DOG,
            "not_measurable": NOT_MEASURABLE_IN_ONE_DOG,
            "the_useful_asymmetry": "Nodal involvement -- the risk specific to the Corgi pulmonary "
                "presentation -- IS measurable in an individual patient by staging, even though its "
                "cohort rate was never published. Pre-existing subclonal resistance, the generic "
                "risk, is not measurable at any depth. So for one dog the Corgi-specific uncertainty "
                "is resolvable and the generic one is not, which is the opposite of how the "
                "population model treats them.",
            "clinical_assay_floors_for_reference": {
                name: {"vaf_lod": a["vaf_lod"],
                       "cell_fraction_lod": vaf_lod_to_cell_fraction(a["vaf_lod"])}
                for name, a in SEQUENCING_ASSAYS.items() if a["clinically_available_for_dogs"]},
        },
        "the_threshold_is_the_whole_answer": {
            **threshold,
            "why_it_dominates": "Above it, a pre-existing subclone is suppressed indefinitely rather "
                "than eventually outgrowing, so the outcome stops depending on whether one exists -- "
                "the single parameter no assay can resolve. That converts an unanswerable question "
                "into an irrelevant one, which is a stronger result than any better estimate of it.",
            "sensitivity_to_unmeasurable_preexisting_prob_at_10yr": {
                "vaccine_off": _spread(False),
                "above_threshold": _spread(True),
            },
        },
        "does_nodal_disease_break_it": {
            "why_this_is_the_corgi_specific_question": "Sakai et al. report regional nodal involvement "
                "in many cases, so the single-compartment 'debulking reaches everything' premise does "
                "not hold. The nodal compartment is seeded from the PRE-debulking primary (carrying "
                "any pre-existing resistant clone) and surgery cannot touch it.",
            "answer": "No, above threshold. The vaccine and both drugs are systemic, so the "
                     "compartment surgery misses is still fully exposed -- debulking is the only "
                     "modality with a reach problem here. Nodal involvement matters most in the "
                     "regime where the rest of the regimen is nearly working, and essentially not at "
                     "all once potency clears the threshold.",
            "worst_measurable_configuration_10yr": {
                "nodal_involvement_prob": max(NODAL_INVOLVEMENT_PROB_SWEEP),
                "preexisting_prob": 0.62,
                "durable_response_vaccine_off": (
                    float(worst_below["probability_durable_response"].iloc[0])
                    if len(worst_below) else None),
                "durable_response_above_threshold": (
                    float(worst_above["probability_durable_response"].iloc[0])
                    if len(worst_above) else None),
            },
        },
        "regimen_that_the_model_supports": {
            "1_local_therapy": f"surgical resection / focal radiation of the primary lung mass "
                              f"({debulking_fraction:.0%} burden reduction modeled). Necessary but "
                              "on its own worthless -- both untreated arms regrow within ~150-200 "
                              "days in this model.",
            "2_sequence_the_specimen": "the gate. Establishes whether a MAPK hotspot exists, which "
                                      "both the MEK inhibitor and the vaccine antigen depend on.",
            "3_mek_inhibitor": "trametinib (the drug actually in canine trials), at full systemic "
                              "exposure -- the pulmonary presentation has no blood-brain-barrier "
                              "discount, unlike the CNS presentation.",
            "4_optional_cytotoxic_bridge": {
                "agent": "lomustine (CCNU)",
                "rationale": CCNU_CANINE_HS["why_this_matters_here"],
                "role": "insurance, not additive benefit. It is nearly redundant once vaccine potency "
                       "clears the threshold, and its value concentrates in the sub-threshold regime "
                       f"-- bounded to ~{CCNU_EXPOSURE_DAYS} days by real cumulative hepatotoxicity, "
                       "which happens to bridge to the vaccine's ramp.",
            },
            "5_hotspot_vaccine": "the component the endurance case rests on, and the only mechanism "
                                "subject to neither the cytostatic ceiling nor a cumulative-dose "
                                "duration cap while still covering every drug-resistance route.",
            "mechanism_constraints": mechanism_constraint_matrix(),
            "convergence_argument": CONVERGENCE_ARGUMENT,
        },
        "matched_benchmark": {
            **CORGI_PULMONARY_HS_BENCHMARK,
            "what_it_says_about_the_bar": "133-day median survival across 19 Corgis on mixed/"
                "unspecified treatment. That is the standard any of this would have to beat, and it "
                "is low -- which cuts both ways: a large relative improvement is plausible from a "
                "low base, and a 10-year durable-response figure is far outside anything this "
                "disease has been observed to do.",
        },
        "the_honest_bottom_line": [
            "The model does contain a durable-response regime for this presentation, and it is not "
            "fragile inside its own assumptions: above the vaccine potency threshold it holds at 10 "
            "years across every nodal-involvement rate and both preexisting_prob values tested.",
            "The entire result hinges on two unmeasured quantities, and they are different in kind. "
            "The driver hotspot is measurable and simply has not been measured in any Corgi -- that "
            "is a funding/tissue problem, resolvable by sequencing one tumor. Vaccine potency is not "
            "measurable in advance at all, and the analogous achievability question, asked of a "
            "CDK4/6 inhibitor by pharmacology.py, came back NO.",
            "So the defensible statement is: this is a well-posed strategy with a clearly identified "
            "single point of failure and a clearly identified first experiment, not a predicted "
            "outcome. The first experiment is cheap relative to the rest (sequence a Corgi HS "
            "specimen) and it gates everything downstream.",
            "Antigen loss remains outside the threshold by construction. Its rate is an unmeasured "
            "constant, and it is the one failure mode where raising vaccine potency does not help.",
        ],
        "unverified_extrapolations": [
            "no Corgi HS tumor has ever been sequenced for driver mutations, so the PTPN11/KRAS "
            "premise underlying both the drug and the vaccine antigen is unconfirmed for this breed",
            "the Corgi scenario reuses the BMD growth-rate and resistance-mechanism spectrum "
            "unchanged (pulmonary_corgi_scenarios' own documented reasoning: no Corgi-specific "
            "germline locus exists to justify a different one), so 'the threshold is 0.058/day' is "
            "inherited, not Corgi-measured",
            "vaccine_max_kill has no measured anchor in any species for this antigen; the threshold "
            "is a target, and nothing here establishes it is reachable",
            "nodal_seed_fraction and the nodal-involvement sweep are illustrative -- Sakai et al. "
            "report 'many cases' without a percentage",
            "the favourable lomustine-to-vaccine handoff timing is a coincidence of two "
            "independently-set constants, not a designed schedule",
            "IMMUNE_ESCAPE_SEEDING_RATE, which sets the one leak no potency covers, is unmeasured",
        ],
        "warning": "This is an illustrative model assembled from real citations and labeled "
                  "placeholders. It is not a treatment plan, and no figure here is a prediction for "
                  "any real dog.",
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, default=str) + "\n")
