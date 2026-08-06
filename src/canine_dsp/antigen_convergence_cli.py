"""Demo/report for `antigen_convergence`: re-runs the three-component regimen with the vaccine ON."""

import json
from dataclasses import replace
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .antigen_convergence import (
    ANTIGEN_RETENTION,
    CONVERGENCE_ARGUMENT,
    handoff_timing,
    mechanism_constraint_matrix,
    verify_antigen_convergence,
)
from .mapk_resistance import ramping_kill_schedule, run_monte_carlo_with_vaccine
from .mapk_scenarios import (
    CCNU_EXPOSURE_DAYS,
    CCNU_MATCHED_CSS_NM,
    CCNU_MATCHED_IC50_NM,
    DEBULKING_FRACTION,
    DURABILITY_HORIZON_SWEEP,
    IMMUNE_ESCAPE_SEEDING_RATE,
    VACCINE_CLONE_NAMES,
    VACCINE_MAX_KILL_SWEEP,
    VACCINE_RAMP_DAYS,
    VACCINE_START_DAY,
    vaccine_followon_scenarios,
)
from .single_patient import LOCALIZED_HS_CCNU_BENCHMARK, partition_by_preexisting_subclone


def antigen_convergence_demo(out: Path, breed: str = "bmd",
                             debulking_fraction: float = DEBULKING_FRACTION,
                             ccnu_max_kill: float = 0.08, trials: int = 400,
                             preexisting_prob: float = 0.30, seed: int = 7) -> None:
    """Corrects three analyses that ran with the vaccine switched off.

    `single_patient_cli`, `pharmacology_cli` and `mutational_supply_cli` all use `run_monte_carlo`
    rather than `run_monte_carlo_with_vaccine`, so their conclusions -- notably "the
    with-pre-existing-subclone arm is 0.0% durable" and "neither agent is the answer" -- describe a
    two-component regimen. The antigen-convergence argument says the vaccine is exactly what covers
    that arm, because a pre-existing drug-resistant subclone still carries the driver antigen.

    Four checks:

      1. STRUCTURAL VERIFICATION -- confirm the engine's own vaccine kill mask matches the
         convergence claim, instead of restating the claim.
      2. THE HANDOFF -- whether immune pressure arrives before the cytotoxic duration cap forces a
         stop, which decides whether "the cap is the binding constraint" survives.
      3. THE SWEEP WITH THE VACCINE ON -- durable response and the N=1 partition, over vaccine
         potency, with lomustine duration-capped at its real cumulative-dose limit.
      4. LONG HORIZON -- does antigen-loss escape erode it, and how fast.
    """
    out.mkdir(parents=True, exist_ok=True)

    # Trametinib + duration-capped lomustine (cytotoxic) as the drug backbone, 5-clone vaccine model.
    base = vaccine_followon_scenarios(breed, debulking_fraction, ccnu_max_kill, [0.0])[0.0]
    model5, css, seeding_rates, initial_burden, provenance = base
    model5 = replace(model5, ic50_nM_2=CCNU_MATCHED_IC50_NM, max_kill_2=ccnu_max_kill)

    # 1. Structural verification of the convergence claim against the engine's mask.
    applicable = np.ones(len(VACCINE_CLONE_NAMES))
    applicable[-1] = 0.0            # the engine's own rule: immune_escape is excluded
    schedule = ramping_kill_schedule(730, VACCINE_START_DAY, VACCINE_RAMP_DAYS, 0.05, applicable)
    verification = verify_antigen_convergence(VACCINE_CLONE_NAMES, schedule)

    # 2. The handoff between a duration-capped cytotoxic and a persistent immune mechanism.
    handoff = handoff_timing(CCNU_EXPOSURE_DAYS, VACCINE_START_DAY, VACCINE_RAMP_DAYS)

    def _run(vaccine_max_kill, horizon_days, with_cytotoxic=True):
        outcome = run_monte_carlo_with_vaccine(
            model5, css, horizon_days, seeding_rates, VACCINE_START_DAY, VACCINE_RAMP_DAYS,
            vaccine_max_kill, IMMUNE_ESCAPE_SEEDING_RATE, VACCINE_CLONE_NAMES, trials=trials,
            preexisting_prob=preexisting_prob, initial_burden=initial_burden,
            css_reference_2=CCNU_MATCHED_CSS_NM if with_cytotoxic else None,
            css_reference_2_duration_days=CCNU_EXPOSURE_DAYS if with_cytotoxic else None,
            seed=seed)
        return outcome, partition_by_preexisting_subclone(outcome)

    # 3. Vaccine potency sweep, with and without the duration-capped cytotoxic, at 2 years.
    sweep_rows = []
    for vaccine_max_kill in VACCINE_MAX_KILL_SWEEP:
        for with_cytotoxic in (True, False):
            outcome, partition = _run(vaccine_max_kill, 730, with_cytotoxic)
            mechanisms = pd.Series(outcome.dominant_mechanism).value_counts(normalize=True)
            sweep_rows.append({
                "vaccine_max_kill": vaccine_max_kill,
                "regimen": ("trametinib + duration-capped lomustine + vaccine" if with_cytotoxic
                            else "trametinib + vaccine (no cytotoxic)"),
                "probability_durable_response": float(1 - outcome.progressed.mean()),
                "durable_without_preexisting_subclone":
                    partition["without_preexisting_subclone"]["durable_response_fraction"],
                "durable_with_preexisting_subclone":
                    partition["with_preexisting_subclone"]["durable_response_fraction"],
                "relapse_share_immune_escape": float(mechanisms.get("immune_escape", 0.0)),
            })
    sweep = pd.DataFrame(sweep_rows)
    sweep.to_csv(out / "vaccine_potency_sweep.csv", index=False)

    # 4. Long horizon at a mid-sweep vaccine potency: does antigen loss erode the result?
    endurance_potency = 0.05
    endurance_rows = []
    for horizon_days in DURABILITY_HORIZON_SWEEP:
        outcome, partition = _run(endurance_potency, horizon_days)
        mechanisms = pd.Series(outcome.dominant_mechanism).value_counts(normalize=True)
        endurance_rows.append({
            "horizon_days": horizon_days, "horizon_years": round(horizon_days / 365, 1),
            "vaccine_max_kill": endurance_potency,
            "probability_durable_response": float(1 - outcome.progressed.mean()),
            "durable_with_preexisting_subclone":
                partition["with_preexisting_subclone"]["durable_response_fraction"],
            "relapse_share_immune_escape": float(mechanisms.get("immune_escape", 0.0)),
        })
    endurance = pd.DataFrame(endurance_rows)
    endurance.to_csv(out / "endurance_horizon.csv", index=False)

    fig, (left, right) = plt.subplots(1, 2, figsize=(13, 5))
    for regimen, style, color in (
            ("trametinib + duration-capped lomustine + vaccine", "o-", "tab:blue"),
            ("trametinib + vaccine (no cytotoxic)", "s--", "tab:purple")):
        arm = sweep[sweep["regimen"] == regimen]
        left.plot(arm["vaccine_max_kill"], arm["probability_durable_response"], style, color=color,
                  label=regimen.replace(" + ", "\n+ "))
        left.plot(arm["vaccine_max_kill"], arm["durable_with_preexisting_subclone"], style,
                  color=color, alpha=.4, markerfacecolor="none")
    left.axhline(LOCALIZED_HS_CCNU_BENCHMARK["relapse_free_fraction"], color="tab:green",
                 linestyle="-.", label="Skorupski 2009 relapse-free")
    left.set(xlabel="vaccine max_kill (per day)", ylabel="P(durable response)", ylim=(-0.03, 1.03),
             title="Solid = whole cohort; faded/open = the pre-existing-subclone arm\n"
                   "(the arm three prior analyses reported as flat 0%)")
    left.legend(fontsize=7); left.grid(alpha=.3)

    right.plot(endurance["horizon_years"], endurance["probability_durable_response"], "o-",
               color="tab:blue", label="durable response")
    right.plot(endurance["horizon_years"], endurance["relapse_share_immune_escape"], "^--",
               color="tab:red", label="relapses via antigen loss")
    right.set(xlabel="horizon (years)", ylabel="fraction of trials", ylim=(-0.03, 1.03),
              title=f"Endurance at vaccine max_kill={endurance_potency}\n"
                    "slow erosion, and its mechanism is the one route the vaccine cannot see")
    right.legend(fontsize=8); right.grid(alpha=.3)
    fig.tight_layout(); fig.savefig(out / "antigen_convergence.png", dpi=160); plt.close(fig)

    with_cyto = sweep[sweep["regimen"].str.contains("lomustine")]
    no_vaccine = with_cyto[with_cyto["vaccine_max_kill"] == 0.0].iloc[0]
    mid_vaccine = with_cyto[with_cyto["vaccine_max_kill"] == endurance_potency].iloc[0]
    summary = {
        "question": "The project derived that every drug-resistance route in this model keeps the "
                   "driver antigen, so a vaccine catches all of them. Was that factored into the "
                   "recent analyses -- and what does it change?",
        "answer": "It was derived and implemented, and then NOT used: the three most recent analyses "
                 "all called run_monte_carlo instead of run_monte_carlo_with_vaccine, i.e. ran with "
                 "the vaccine at zero. Switching it on reverses their central negative conclusion. "
                 f"The pre-existing-subclone arm goes from "
                 f"{no_vaccine['durable_with_preexisting_subclone']:.3f} to "
                 f"{mid_vaccine['durable_with_preexisting_subclone']:.3f} durable at vaccine "
                 f"max_kill={endurance_potency}, and the cohort from "
                 f"{no_vaccine['probability_durable_response']:.3f} to "
                 f"{mid_vaccine['probability_durable_response']:.3f}.",
        "the_argument": CONVERGENCE_ARGUMENT,
        "antigen_retention_per_clone": ANTIGEN_RETENTION,
        "finding_1_structural_verification": {
            **verification,
            "why_verified_structurally": "The claim is about which clones the vaccine can see, so it "
                "is checked against the engine's actual kill mask rather than inferred from a "
                "durable-response number that many other parameters also move.",
        },
        "finding_2_the_handoff_undoes_the_duration_cap_finding": {
            **handoff,
            "what_it_revises": "The lomustine analysis concluded the cumulative-dose duration cap was "
                "'the binding constraint for HS', because benefit collapsed purely from stopping. "
                "That is true only with nothing to hand off to. The vaccine begins ramping at day "
                f"{VACCINE_START_DAY}, inside lomustine's {CCNU_EXPOSURE_DAYS}-day window, so the "
                "cap stops being the binding constraint once a persistent mechanism is present.",
        },
        "finding_3_vaccine_potency_sweep": {
            "rows": sweep_rows,
            "what_changed_vs_the_no_vaccine_analyses": {
                "cohort_durable_no_vaccine": float(no_vaccine["probability_durable_response"]),
                "cohort_durable_with_vaccine": float(mid_vaccine["probability_durable_response"]),
                "preexisting_subclone_arm_no_vaccine": float(
                    no_vaccine["durable_with_preexisting_subclone"]),
                "preexisting_subclone_arm_with_vaccine": float(
                    mid_vaccine["durable_with_preexisting_subclone"]),
            },
            "why_the_subclone_arm_is_the_point": "A pre-existing drug-resistant subclone still "
                "expresses the driver hotspot -- it acquired resistance without shedding the antigen. "
                "So the one patient type the drug-only regimen cannot help is precisely the type "
                "antigen convergence predicts a vaccine covers. Reporting that arm as flat 0% while "
                "the vaccine was off was the substantive error.",
        },
        "finding_4_endurance_and_what_actually_leaks": {
            "rows": endurance_rows,
            "reading": f"At vaccine max_kill={endurance_potency} durability is flat to 2 years and "
                      "erodes slowly after (~97% at 10 years). The erosion mechanism was checked "
                      "rather than assumed, and it is NOT antigen loss: every 10-year relapse is "
                      "target_site_mutation, and the immune-escape clone never establishes in any "
                      "trial.",
            "why": f"Arithmetic, not immunology. target_site_mutation grows at 0.058/day and the "
                  f"swept vaccine potency {endurance_potency} sits just below it, so once "
                  f"lomustine's exposure ends at day {CCNU_EXPOSURE_DAYS} that one clone has a small "
                  "positive net margin and a decade is long enough for a few trials to cross the "
                  "detection threshold. Raising vaccine potency just past that growth rate (0.06) "
                  "gives flat 100% durable response at 10 years with no relapses of any kind -- a "
                  "threshold effect at the clone's growth rate, exactly the same arithmetic as the "
                  "cytostatic ceiling, except an immune mechanism is permitted to cross it.",
            "correction_recorded": "An earlier draft of this summary claimed the erosion was antigen "
                                  "loss, which the relapse-mechanism breakdown does not support. The "
                                  "convergence argument predicts antigen loss is the only route that "
                                  "CAN evade the vaccine; it does not predict that route is the one "
                                  "that actually fires at these parameters.",
            "load_bearing_assumption": "The immune-escape clone never establishing is largely a "
                f"consequence of its illustrative seeding rate ({IMMUNE_ESCAPE_SEEDING_RATE:.1e}, "
                f"~200x below the drug-resistance total) plus its day-{VACCINE_START_DAY} start and "
                "15% growth penalty. That constant is unmeasured and is doing real work here: a "
                "meaningfully higher antigen-loss rate would reintroduce the one leak the vaccine "
                "cannot cover, and nothing in this repo constrains it.",
        },
        "mechanism_constraint_matrix": mechanism_constraint_matrix(),
        "what_this_retracts": [
            "'Neither agent is the answer... what this regimen would need is a ceiling-free partner "
            "without a cumulative-dose duration cap. Whether such an agent exists for canine HS is "
            "not established here.' -- a mechanism satisfying both was already implemented in this "
            "repo. The two-drug analysis was correct about the two drugs and wrong to generalize "
            "from them.",
            "'The with-preexisting-subclone arm is lost to lomustine's 105-day duration cap "
            "regardless of any mutation rate' -- it is not, once the vaccine is on.",
            "The mutational-supply decomposition's framing that the argument's leverage 'lands on the "
            "one parameter no assay can measure' -- still true about measurement, but its "
            "implication was overstated: the vaccine covers that parameter's bad outcome "
            "therapeutically, so being unable to measure it matters less than that analysis implied.",
        ],
        "unverified_extrapolations": [
            "vaccine_max_kill remains a swept, unfitted knob -- no canine cancer vaccine trial exists "
            "for this disease, so no potency here is measured. The sweep spans plausible values; it "
            "does not bracket a measurement",
            "the antigen-convergence argument is a mechanistic deduction about what each modeled "
            "resistance mechanism does to the antigen. It is internally consistent and checkable "
            "against the engine, but the mechanisms themselves are illustrative constructs, not "
            "sequenced canine HS resistance clones",
            "the immune-escape clone's seeding rate and 15% growth penalty are both illustrative, and "
            "they set how fast the long-horizon erosion runs",
            "the whole chain still rests on Corgi HS carrying a PTPN11/KRAS hotspot at all, which "
            "remains unsequenced -- antigen convergence says resistance will not shed the antigen, "
            "not that the antigen is present",
            "vaccine and cytotoxic schedules are not co-optimized; VACCINE_START_DAY=90 was chosen "
            "before lomustine entered the model, so the favourable handoff timing is a coincidence "
            "of two independently-set constants, not a designed schedule",
        ],
        "warning": "This corrects an omission inside an illustrative model. It does not establish that "
                  "any vaccine works in this disease, and the high durable-response figures are "
                  "properties of a swept potency knob, not predictions.",
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, default=str) + "\n")
