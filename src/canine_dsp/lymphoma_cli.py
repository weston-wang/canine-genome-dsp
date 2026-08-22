"""CLI demos for the canine lymphoma durable-response analysis. Each writes CSV tracks, a
machine-readable summary.json, and a plot. Mirrors hsa_cli's structure. See
docs/LYMPHOMA_DURABLE_RESPONSE.md. Nothing here is a treatment recommendation; potency and growth
constants are illustrative and swept.
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .lymphoma_scenarios import (
    LYMPHOMA_CHOP_BENCHMARK,
    LYMPHOMA_CLONE_NAMES,
    LYMPHOMA_CNS_INVOLVEMENT_PROB_SWEEP,
    LYMPHOMA_CNS_SANCTUARY,
    LYMPHOMA_CNS_SEED_FRACTION,
    LYMPHOMA_DURABILITY_HORIZON_SWEEP,
    LYMPHOMA_IMMUNOTHERAPY_CLONE_NAMES,
    LYMPHOMA_IMMUNOTHERAPY_MAX_KILL_SWEEP,
    LYMPHOMA_IMMUNOTHERAPY_RAMP_DAYS,
    LYMPHOMA_IMMUNOTHERAPY_START_DAY,
    LYMPHOMA_IMMUNOTHERAPY_TRIALS,
    LYMPHOMA_CD20_LOSS_SEEDING_RATE,
    LYMPHOMA_RESISTANCE_EVIDENCE,
    LYMPHOMA_TRANSPLANT_BENCHMARK,
    _PREEXISTING_PROB_CENTRAL,
    _PREEXISTING_PROB_SWEEP,
    dog_lymphoma_preset,
    lymphoma_immunotherapy_followon_scenarios,
)
from .mapk_resistance import (
    clone_growth_margins,
    run_monte_carlo,
    run_monte_carlo_two_compartment,
    run_monte_carlo_with_vaccine,
)

_WARNING = ("Synthetic Monte Carlo exploration of plausible clonal-escape dynamics for canine "
            "multicentric lymphoma. The resistance mechanisms (P-gp/ABCB1 and BCRP/ABCG2 efflux) "
            "and the trial/transplant anchors are real; every growth rate, kill ceiling, IC50 "
            "ratio, immunotherapy potency, and CNS penetration fraction is illustrative and swept. "
            "No combination described has been given to a dog on the strength of this model.")


def lymphoma_resistance_demo(out: Path, immunophenotype: str = "B", trials: int = 300,
                             horizon_days: int = 730, seed: int = 7) -> None:
    """CHOP-only chemoresistance model: the bar, and durable-response sensitivity to the
    preexisting-resistance probability (the least-grounded input), mirroring hsa_resistance_demo."""
    out.mkdir(parents=True, exist_ok=True)
    model, css, seeding_rates, provenance = dog_lymphoma_preset(immunophenotype)

    bar_rows = []
    for label, c in [("full_chop_5x_ic50", css), ("derated_40pct", css * 0.4), ("no_drug", 0.0)]:
        margins = clone_growth_margins(model, c)
        bar_rows.append({"exposure": label,
                         **{name: float(m) for name, m in zip(LYMPHOMA_CLONE_NAMES, margins)},
                         "bar_resistant": float(margins[1:].max())})
    pd.DataFrame(bar_rows).to_csv(out / "durability_bar.csv", index=False)

    sweep_rows = []
    for prob in _PREEXISTING_PROB_SWEEP:
        outcome = run_monte_carlo(model, css, horizon_days, seeding_rates, trials,
                                  preexisting_prob=prob, seed=seed)
        sweep_rows.append({"preexisting_prob": prob,
                           "probability_durable_response": float(1 - outcome.progressed.mean())})
    pd.DataFrame(sweep_rows).to_csv(out / "preexisting_prob_sensitivity.csv", index=False)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot([r["preexisting_prob"] for r in sweep_rows],
            [r["probability_durable_response"] for r in sweep_rows], marker="o", color="tab:blue")
    ax.set(xlabel="P(pre-existing resistant subclone)", ylabel="P(durable response)",
           title=f"CHOP-only durable response, {immunophenotype}-cell lymphoma", ylim=(0, 1))
    fig.tight_layout(); fig.savefig(out / "lymphoma_resistance.png", dpi=160); plt.close(fig)

    summary = {"immunophenotype": immunophenotype, "trials": trials, "horizon_days": horizon_days,
               "durability_bar": bar_rows, "preexisting_prob_sensitivity": sweep_rows,
               "real_grounding": LYMPHOMA_RESISTANCE_EVIDENCE,
               "standard_of_care_benchmark": LYMPHOMA_CHOP_BENCHMARK, "warning": _WARNING}
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


def lymphoma_immunotherapy_demo(out: Path, immunophenotype: str = "B", rab_max_kill: float = 0.0,
                                trials: int = 300, horizon_days: int = 730, seed: int = 7) -> None:
    """Layer a swept-potency CD20-directed immune effector on CHOP; does it close the resistance gap
    and where is the threshold? Mirrors hsa_vaccine_followon_demo."""
    out.mkdir(parents=True, exist_ok=True)
    scenarios = lymphoma_immunotherapy_followon_scenarios(
        rab_max_kill, immunophenotype, LYMPHOMA_IMMUNOTHERAPY_MAX_KILL_SWEEP)

    rows = []
    for vmk, (model, css, seeding_rates, _) in scenarios.items():
        outcome = run_monte_carlo_with_vaccine(
            model, css, horizon_days, seeding_rates,
            vaccine_start_day=LYMPHOMA_IMMUNOTHERAPY_START_DAY,
            vaccine_ramp_days=LYMPHOMA_IMMUNOTHERAPY_RAMP_DAYS, vaccine_max_kill=vmk,
            immune_escape_seeding_rate=LYMPHOMA_CD20_LOSS_SEEDING_RATE,
            clone_names=LYMPHOMA_IMMUNOTHERAPY_CLONE_NAMES, trials=trials,
            preexisting_prob=_PREEXISTING_PROB_CENTRAL, seed=seed)
        counts = pd.Series(outcome.dominant_mechanism).value_counts()
        rows.append({"immunotherapy_max_kill": vmk,
                     "probability_durable_response": float(1 - outcome.progressed.mean()),
                     "cd20_antigen_loss_relapses": int(counts.get("cd20_antigen_loss", 0))})
    table = pd.DataFrame(rows)
    table.to_csv(out / "lymphoma_immunotherapy_sensitivity.csv", index=False)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(table["immunotherapy_max_kill"], table["probability_durable_response"],
            marker="o", color="tab:green")
    ax.axvline(0.0903, color="gray", linestyle="--", linewidth=.9, label="the bar (~0.090/day)")
    ax.set(xlabel="CD20 effector max_kill (illustrative, unmeasured)", ylabel="P(durable response)",
           title=f"CHOP + CD20 immunotherapy, {immunophenotype}-cell, {horizon_days/365:.0f}y",
           ylim=(0, 1.02))
    ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(out / "lymphoma_immunotherapy.png", dpi=160); plt.close(fig)

    summary = {"immunophenotype": immunophenotype, "rab_max_kill": rab_max_kill, "trials": trials,
               "horizon_days": horizon_days, "bar_per_day": 0.0903, "sensitivity": rows,
               "real_immunotherapy_evidence": LYMPHOMA_IMMUNOTHERAPY_TRIALS, "warning": _WARNING}
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


def lymphoma_sanctuary_demo(out: Path, immunotherapy_max_kill: float = 0.09, trials: int = 300,
                            horizon_days: int = 1825, nodal_involvement_prob: float = 0.30,
                            seed: int = 7) -> None:
    """The CNS sanctuary: two-compartment model with a swept drug-penetration multiplier, chemo-only
    vs. chemo + a systemic CD20 effector. Demonstrates the penetration upgrade to the engine."""
    out.mkdir(parents=True, exist_ok=True)
    model, css, seeding_rates, _ = dog_lymphoma_preset("B")
    immuno = lymphoma_immunotherapy_followon_scenarios(
        immunotherapy_max_kill_values=[immunotherapy_max_kill])[immunotherapy_max_kill]
    model5, css5, seeding5, _ = immuno

    rows = []
    for pen in LYMPHOMA_CNS_SANCTUARY["penetration_multiplier_sweep"]:
        chemo = run_monte_carlo_two_compartment(
            model, css, horizon_days, seeding_rates, nodal_involvement_prob=nodal_involvement_prob,
            nodal_seed_fraction=LYMPHOMA_CNS_SEED_FRACTION, trials=trials,
            preexisting_prob=_PREEXISTING_PROB_CENTRAL, sanctuary_penetration_multiplier=pen,
            clone_names=LYMPHOMA_CLONE_NAMES, seed=seed)
        immu = run_monte_carlo_two_compartment(
            model5, css5, horizon_days, seeding5, nodal_involvement_prob=nodal_involvement_prob,
            nodal_seed_fraction=LYMPHOMA_CNS_SEED_FRACTION, trials=trials,
            preexisting_prob=_PREEXISTING_PROB_CENTRAL, sanctuary_penetration_multiplier=pen,
            vaccine_start_day=LYMPHOMA_IMMUNOTHERAPY_START_DAY,
            vaccine_ramp_days=LYMPHOMA_IMMUNOTHERAPY_RAMP_DAYS, vaccine_max_kill=immunotherapy_max_kill,
            immune_escape_seeding_rate=LYMPHOMA_CD20_LOSS_SEEDING_RATE,
            clone_names=LYMPHOMA_IMMUNOTHERAPY_CLONE_NAMES, seed=seed)
        rows.append({
            "cns_penetration_multiplier": pen,
            "chemo_only_durable": float(1 - chemo.progressed.mean()),
            "chemo_only_cns_relapses": int(sum(c == "nodal" for c in chemo.dominant_compartment)),
            "with_immunotherapy_durable": float(1 - immu.progressed.mean()),
            "with_immunotherapy_cns_relapses": int(sum(c == "nodal" for c in immu.dominant_compartment)),
        })
    table = pd.DataFrame(rows)
    table.to_csv(out / "lymphoma_sanctuary_sensitivity.csv", index=False)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(table["cns_penetration_multiplier"], table["chemo_only_durable"],
            marker="o", label="chemo only", color="tab:red")
    ax.plot(table["cns_penetration_multiplier"], table["with_immunotherapy_durable"],
            marker="o", label="chemo + CD20 effector", color="tab:green")
    ax.set(xlabel="CNS drug penetration multiplier", ylabel="P(durable response)",
           title="CNS sanctuary: immunotherapy reaches what the drug cannot", ylim=(0, 1.02))
    ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(out / "lymphoma_sanctuary.png", dpi=160); plt.close(fig)

    summary = {"immunotherapy_max_kill": immunotherapy_max_kill, "trials": trials,
               "horizon_days": horizon_days, "nodal_involvement_prob": nodal_involvement_prob,
               "sensitivity": rows, "cns_sanctuary": LYMPHOMA_CNS_SANCTUARY, "warning": _WARNING}
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


def lymphoma_durability_horizon_demo(out: Path, immunotherapy_max_kill: float = 0.09,
                                     immunophenotype: str = "B", trials: int = 300,
                                     seed: int = 7) -> None:
    """How long is "durable"? Runs the CHOP + CD20-effector combination out to 1, 2, 5 and 10 years,
    the horizon at which "cure or 10-year durability" is actually tested. Mirrors
    hsa_durability_horizon_demo."""
    out.mkdir(parents=True, exist_ok=True)
    scenario = lymphoma_immunotherapy_followon_scenarios(
        immunophenotype=immunophenotype,
        immunotherapy_max_kill_values=[immunotherapy_max_kill])[immunotherapy_max_kill]
    model, css, seeding_rates, _ = scenario

    rows = []
    for horizon_days in LYMPHOMA_DURABILITY_HORIZON_SWEEP:
        outcome = run_monte_carlo_with_vaccine(
            model, css, horizon_days, seeding_rates,
            vaccine_start_day=LYMPHOMA_IMMUNOTHERAPY_START_DAY,
            vaccine_ramp_days=LYMPHOMA_IMMUNOTHERAPY_RAMP_DAYS, vaccine_max_kill=immunotherapy_max_kill,
            immune_escape_seeding_rate=LYMPHOMA_CD20_LOSS_SEEDING_RATE,
            clone_names=LYMPHOMA_IMMUNOTHERAPY_CLONE_NAMES, trials=trials,
            preexisting_prob=_PREEXISTING_PROB_CENTRAL, seed=seed)
        rows.append({"horizon_days": horizon_days, "horizon_years": horizon_days / 365,
                     "probability_durable_response": float(1 - outcome.progressed.mean())})
    table = pd.DataFrame(rows)
    table.to_csv(out / "lymphoma_durability_horizon.csv", index=False)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(table["horizon_years"], table["probability_durable_response"], marker="o",
            color="tab:green")
    ax.set(xlabel="years of follow-up simulated", ylabel="P(no relapse by this horizon)",
           title=f"how long is durable? {immunophenotype}-cell, effector={immunotherapy_max_kill}",
           ylim=(0, 1.02))
    fig.tight_layout(); fig.savefig(out / "lymphoma_durability_horizon.png", dpi=160); plt.close(fig)

    summary = {"immunotherapy_max_kill": immunotherapy_max_kill, "immunophenotype": immunophenotype,
               "trials": trials, "sensitivity": rows,
               "transplant_benchmark": LYMPHOMA_TRANSPLANT_BENCHMARK, "warning": _WARNING}
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
