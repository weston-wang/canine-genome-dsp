import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .hsa_scenarios import (
    HSA_CLONE_NAMES,
    HSA_IMMUNE_ESCAPE_SEEDING_RATE,
    HSA_RAPAMYCIN_BENCHMARK,
    HSA_STANDARD_OF_CARE_BENCHMARK,
    HSA_VACCINE_CLONE_NAMES,
    HSA_VACCINE_MAX_KILL_SWEEP,
    HSA_VACCINE_RAMP_DAYS,
    HSA_VACCINE_START_DAY,
    HSA_VACCINE_TRIALS,
    _PREEXISTING_PROB_CENTRAL,
    _PREEXISTING_PROB_SWEEP,
    dog_hsa_preset,
    hsa_vaccine_followon_scenarios,
)
from .mapk_resistance import run_monte_carlo, run_monte_carlo_with_vaccine


def hsa_resistance_demo(out: Path, trials: int = 300, horizon_days: int = 730, seed: int = 7) -> None:
    """Runs the PI3K/mTOR-pathway resistance model across a `preexisting_prob` sweep, the same
    discipline `mapk_cli.mapk_resistance_demo` uses for histiocytic sarcoma: whether a resistant
    subclone already exists at treatment start has no HSA-specific source either, so a single
    asserted value would mostly reflect that choice, not a finding.

    See `hsa_scenarios` module docstring for why this models the PIK3CA/PTEN-driven subtype
    specifically (not HSA generically), and for why the reference concentration is illustrative
    rather than rapamycin's real trough concentration paired against a different drug's real IC50.
    """
    out.mkdir(parents=True, exist_ok=True)
    model, css_reference, seeding_rates, provenance = dog_hsa_preset()

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
    mechanism_table = mechanism_counts.reindex(["durable_response"] + HSA_CLONE_NAMES[1:], fill_value=0)
    mechanism_table = (mechanism_table / len(outcome.dominant_mechanism)).rename("trial_fraction")
    mechanism_table.to_csv(out / "escape_mechanism_breakdown.csv")

    fig, axes = plt.subplots(1, 3, figsize=(15.5, 4.5))
    axes[0].fill_between(days, quantiles[0], quantiles[2], alpha=.25, color="tab:blue")
    axes[0].plot(days, quantiles[1], color="tab:blue")
    axes[0].axhline(model.carrying_capacity, color="gray", linestyle="--", linewidth=.8)
    axes[0].set(xlabel="day", ylabel="total tumor burden",
               title=f"HSA (PI3K/mTOR subtype): burden at preexisting_prob={_PREEXISTING_PROB_CENTRAL}")
    mechanism_table.plot(kind="bar", ax=axes[1], color="tab:orange")
    axes[1].set(ylabel="fraction of trials", title="dominant outcome (this preexisting_prob only)")
    axes[1].tick_params(axis="x", rotation=30)
    axes[2].plot(sweep_table["preexisting_prob"], sweep_table["probability_durable_response"],
                marker="o", color="tab:blue")
    axes[2].set(xlabel="assumed P(pre-existing resistant subclone)", ylabel="P(durable response)",
               title="sensitivity to the least-grounded input", ylim=(0, 1))
    fig.tight_layout(); fig.savefig(out / "hsa_resistance_monte_carlo.png", dpi=160); plt.close(fig)

    progressor_medians = [row["median_time_to_progression_days"] for row in sweep_rows
                         if row["median_time_to_progression_days"] is not None]
    summary = {
        "trials": trials, "horizon_days": horizon_days,
        "preexisting_prob_sensitivity": sweep_table.to_dict(orient="records"),
        "central_scenario": {
            "preexisting_prob": _PREEXISTING_PROB_CENTRAL,
            **{k: v for k, v in sweep_rows[_PREEXISTING_PROB_SWEEP.index(_PREEXISTING_PROB_CENTRAL)].items()
               if k != "preexisting_prob"},
            "escape_mechanism_breakdown": mechanism_table.to_dict(),
        },
        "hsa_rapamycin_real_world_benchmark": HSA_RAPAMYCIN_BENCHMARK,
        "hsa_standard_of_care_benchmark": HSA_STANDARD_OF_CARE_BENCHMARK,
        "human_benchmark_comparison": (
            f"This scenario's own median_time_to_progression_days among progressors ranges "
            f"{min(progressor_medians):.0f}-{max(progressor_medians):.0f} days across the "
            f"preexisting_prob values swept, versus real median survival differences of "
            "75-79 days (rapamycin vs. not, in the TP53- and PIK3CA-mutant FidoCure subgroups -- "
            "see hsa_rapamycin_real_world_benchmark) and a real standard-of-care range of "
            "48 days (surgery alone) to ~120-180 days (surgery+doxorubicin, see "
            "hsa_standard_of_care_benchmark). These aren't directly comparable endpoints "
            "(this module's median_time_to_progression_days is RECIST-style progression from "
            "nadir in a synthetic model; the real benchmarks are overall survival, mix "
            "unstandardized concurrent treatments, and are not restricted to any driver "
            "subtype the same way this scenario is) -- read as scale, not agreement or "
            "disagreement, the same caveat MAPK_INHIBITOR_HUMAN_BENCHMARK carries in the "
            "histiocytic-sarcoma module."
            if progressor_medians else
            "No trial in this run had any progressor to compare against the real benchmarks."
        ),
        "provenance": provenance,
        "unverified_extrapolations": [
            ("this scenario models only the PIK3CA/PTEN-driven, PI3K/mTOR-pathway subtype of "
             "HSA -- see hsa_scenarios module docstring for why an NRAS/MEK-inhibitor subtype "
             "was deliberately not modeled (a real result already argues against it)"),
            ("the three escape mechanisms (pi3k_akt_feedback_reactivation, mapk_crosstalk_bypass, "
             "target_site_mutation) are this module's own speculative extension of general "
             "mTORC1-inhibitor-resistance biology from other cancers, not measured in HSA"),
            ("css_reference is an illustrative 5x-IC50 margin, not rapamycin's real trough "
             "concentration -- see dog_hsa_preset's docstring for why those two real numbers "
             "cannot be paired directly without self-contradiction"),
            ("growth rates, resistant-clone potency shifts, kill ceilings, and seeding rates are "
             "all illustrative placeholders with no HSA-specific case-report anchor to even "
             "loosely tune against, unlike histiocytic sarcoma's handful of durable-response "
             "case reports"),
            ("whether this specific dog's tumor carries PIK3CA/PTEN mutations at all would need "
             "real sequencing to confirm -- this scenario assumes that subtype, it doesn't "
             "diagnose it"),
        ],
        "warning": (
            "Synthetic Monte Carlo exploration of plausible escape dynamics for one molecularly "
            "defined HSA subtype; only sensitive_clone_ic50_nM under provenance."
            "calibrated_from_data is anchored to a published measurement. Not a validated "
            "predictive or clinical model. The real rapamycin PK/PD and FidoCure survival "
            "numbers are reported for scale, not fit into this scenario's own parameters -- see "
            "human_benchmark_comparison."
        ),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


def hsa_vaccine_followon_demo(out: Path, horizon_days: int = 730, trials: int = 300,
                              preexisting_prob: float = _PREEXISTING_PROB_CENTRAL,
                              seed: int = 7) -> None:
    """Does layering a cancer vaccine on top of PI3K/mTOR-inhibitor therapy close the gap left by
    drug resistance alone, the same question `mapk_cli.vaccine_followon_demo` asks for
    histiocytic sarcoma?

    Real HSA vaccines don't target this scenario's driver mutation (PIK3CA/PTEN) at all -- see
    `hsa_scenarios` module docstring for the real trials (ERstrePs, eVim, autologous whole-cell,
    a real vaccine that failed on a key readout, and one still-enrolling trial) and why targeting
    a genotype-agnostic antigen instead makes the antigen-persistence argument more secure here,
    not less.
    """
    out.mkdir(parents=True, exist_ok=True)
    scenarios = hsa_vaccine_followon_scenarios(vaccine_max_kill_values=HSA_VACCINE_MAX_KILL_SWEEP)

    rows, outcomes = [], {}
    for vaccine_max_kill, (model, css, seeding_rates, _) in scenarios.items():
        outcome = run_monte_carlo_with_vaccine(
            model, css, horizon_days, seeding_rates, vaccine_start_day=HSA_VACCINE_START_DAY,
            vaccine_ramp_days=HSA_VACCINE_RAMP_DAYS, vaccine_max_kill=vaccine_max_kill,
            immune_escape_seeding_rate=HSA_IMMUNE_ESCAPE_SEEDING_RATE,
            clone_names=HSA_VACCINE_CLONE_NAMES, trials=trials,
            preexisting_prob=preexisting_prob, seed=seed)
        outcomes[vaccine_max_kill] = outcome
        ttp = outcome.time_to_progression[outcome.progressed]
        mechanism_counts = pd.Series(outcome.dominant_mechanism).value_counts()
        mechanism_fractions = (mechanism_counts.reindex(["durable_response"] + HSA_VACCINE_CLONE_NAMES[1:],
                                                        fill_value=0)
                              / len(outcome.dominant_mechanism))
        rows.append({
            "vaccine_max_kill": vaccine_max_kill,
            "probability_durable_response": float(1 - outcome.progressed.mean()),
            "probability_progression": float(outcome.progressed.mean()),
            "median_time_to_progression_days": float(np.median(ttp)) if ttp.size else None,
            **{f"mechanism_{mechanism}": float(value) for mechanism, value in mechanism_fractions.items()},
        })
    table = pd.DataFrame(rows)
    table.to_csv(out / "hsa_vaccine_followon_sensitivity.csv", index=False)

    days = np.arange(horizon_days + 1)
    fig, axes = plt.subplots(1, 3, figsize=(15.5, 4.5))
    for vaccine_max_kill in HSA_VACCINE_MAX_KILL_SWEEP:
        outcome = outcomes[vaccine_max_kill]
        median_burden = np.median(outcome.trajectories.sum(axis=2), axis=0)
        axes[0].plot(days, median_burden, label=f"vaccine max_kill={vaccine_max_kill}")
    axes[0].axvline(HSA_VACCINE_START_DAY, color="gray", linestyle=":", linewidth=.9)
    axes[0].set(xlabel="day", ylabel="median total tumor burden",
               title="HSA (PI3K/mTOR subtype): drug + vaccine")
    axes[0].legend(fontsize=7)
    axes[1].plot(table["vaccine_max_kill"], table["probability_durable_response"],
                marker="o", color="tab:green")
    axes[1].set(xlabel="vaccine max_kill (illustrative, unmeasured)", ylabel="P(durable response)",
               title="does the vaccine close the resistance gap?", ylim=(0, 1))
    mechanism_columns = [f"mechanism_{name}" for name in ["durable_response"] + HSA_VACCINE_CLONE_NAMES[1:]]
    table.set_index("vaccine_max_kill")[mechanism_columns].plot(kind="bar", stacked=True, ax=axes[2])
    axes[2].set(ylabel="fraction of trials",
               title="closing drug-resistance routes vs. opening immune_escape")
    axes[2].legend(fontsize=6)
    fig.tight_layout(); fig.savefig(out / "hsa_vaccine_followon.png", dpi=160); plt.close(fig)

    summary = {
        "horizon_days": horizon_days, "preexisting_prob_used": preexisting_prob,
        "sensitivity": rows,
        "real_hsa_vaccine_trials": HSA_VACCINE_TRIALS,
        "unverified_extrapolations": [
            ("no canine hemangiosarcoma vaccine trial measures this scenario's own PIK3CA/PTEN "
             "driver mutation status in its enrolled dogs, as far as could be determined -- "
             "the real trials above are not restricted to (or even reported by) genotype, so "
             "they cannot directly validate a subtype-specific model like this one"),
            ("vaccine_start_day, vaccine_ramp_days, vaccine_max_kill, and the immune-escape "
             "clone's seeding rate and fitness penalty are all illustrative placeholders, not "
             "fit to any of the four real trials in HSA_VACCINE_TRIALS"),
            ("this scenario has no second drug (CDK4/6i-equivalent) layer -- unlike the "
             "histiocytic-sarcoma module's full drug+drug+vaccine combination, this tests "
             "single-drug (PI3K/mTOR inhibitor) plus vaccine only"),
            ("stacks on top of every extrapolation already listed in hsa_resistance_demo's "
             "summary.json"),
        ],
        "warning": (
            "The real vaccines in HSA_VACCINE_TRIALS are real, but none of them were tested "
            "specifically in combination with a PI3K/mTOR inhibitor, and none report outcomes "
            "by driver mutation -- they establish that cancer vaccines have real, in some cases "
            "statistically significant, benefit in canine HSA generally, not that this specific "
            "scenario's vaccine_max_kill sweep is calibrated to match any of them. Read this as "
            "a demonstration of the antigen-persistence argument's *shape*, the same role "
            "vaccine_followon_demo plays for histiocytic sarcoma, not a probability estimate."
        ),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
