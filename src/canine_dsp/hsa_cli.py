import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .alphafold import (
    align_residue_numbers,
    contact_number_burial,
    download_structure,
    find_exposed_linear_epitopes,
    read_plddt_track,
    whole_sequence_identity,
)
from .hsa_scenarios import (
    HSA_CLONE_NAMES,
    HSA_COMBINED_EXPOSURE_DERATING,
    HSA_DURABILITY_HORIZON_SWEEP,
    HSA_EBAT_ILLUSTRATIVE_CSS_NM,
    HSA_EBAT_MAX_KILL_SWEEP,
    HSA_EBAT_TRIAL,
    HSA_IMMUNE_ESCAPE_SEEDING_RATE,
    HSA_RAPAMYCIN_BENCHMARK,
    HSA_RECEPTOR_CONSERVATION_TARGETS,
    HSA_STANDARD_OF_CARE_BENCHMARK,
    HSA_TOXICITY_EXTRAPOLATION_NOTE,
    HSA_VACCINE_CLONE_NAMES,
    HSA_VACCINE_MAX_KILL_SWEEP,
    HSA_VACCINE_RAMP_DAYS,
    HSA_VACCINE_START_DAY,
    HSA_VACCINE_TRIALS,
    _PREEXISTING_PROB_CENTRAL,
    _PREEXISTING_PROB_SWEEP,
    dog_hsa_preset,
    hsa_combination_scenarios,
    hsa_vaccine_followon_scenarios,
)
from .mapk_resistance import run_monte_carlo, run_monte_carlo_with_vaccine
from .uniprot import DOG_TAXID, HUMAN_TAXID, resolve_uniprot_accession


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


def hsa_combination_control_demo(out: Path, trials: int = 300, horizon_days: int = 730,
                                 preexisting_prob: float = _PREEXISTING_PROB_CENTRAL,
                                 seed: int = 7) -> None:
    """PI3K/mTOR inhibitor vs. eBAT vs. their combination, mirroring
    `mapk_cli.combination_control_demo`'s side-by-side monotherapy/combination comparison.

    eBAT has no real multi-dose-level response curve (see `HSA_EBAT_TRIAL`), so its potency is
    swept across an illustrative range the same way `mapk_scenarios.CDK46_MAX_KILL_SWEEP` sweeps
    histiocytic sarcoma's own real-but-unquantified second agent.
    """
    out.mkdir(parents=True, exist_ok=True)
    regimens = [("combination", True), ("ebat_monotherapy", False)]

    rows, outcomes = [], {}
    for regimen, inhibitor_active in regimens:
        scenarios = hsa_combination_scenarios(inhibitor_active, HSA_EBAT_MAX_KILL_SWEEP)
        for ebat_max_kill, (model, css, seeding_rates, _) in scenarios.items():
            css_2 = HSA_EBAT_ILLUSTRATIVE_CSS_NM if ebat_max_kill > 0 else None
            outcome = run_monte_carlo(model, css, horizon_days, seeding_rates, trials,
                                      preexisting_prob=preexisting_prob,
                                      css_reference_2=css_2, seed=seed)
            outcomes[(regimen, ebat_max_kill)] = outcome
            ttp = outcome.time_to_progression[outcome.progressed]
            mechanism_counts = pd.Series(outcome.dominant_mechanism).value_counts()
            mechanism_fractions = (mechanism_counts.reindex(["durable_response"] + HSA_CLONE_NAMES[1:],
                                                            fill_value=0)
                                  / len(outcome.dominant_mechanism))
            rows.append({
                "regimen": regimen, "ebat_max_kill": ebat_max_kill,
                "probability_durable_response": float(1 - outcome.progressed.mean()),
                "probability_progression": float(outcome.progressed.mean()),
                "median_time_to_progression_days": float(np.median(ttp)) if ttp.size else None,
                **{f"mechanism_{mechanism}": float(value) for mechanism, value in mechanism_fractions.items()},
            })
    table = pd.DataFrame(rows)
    table.to_csv(out / "hsa_combination_sensitivity.csv", index=False)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    for regimen, color in (("combination", "tab:blue"), ("ebat_monotherapy", "tab:red")):
        subset = table[table["regimen"] == regimen]
        ax.plot(subset["ebat_max_kill"], subset["probability_durable_response"],
               marker="o", label=regimen, color=color)
    ax.set(xlabel="eBAT max_kill (illustrative, unmeasured)", ylabel="P(durable response)",
          title="HSA: inhibitor+eBAT combination vs. eBAT monotherapy", ylim=(0, 1))
    ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(out / "hsa_combination_sensitivity.png", dpi=160); plt.close(fig)

    summary = {
        "preexisting_prob_used": preexisting_prob, "sensitivity": rows,
        "real_ebat_trial": HSA_EBAT_TRIAL,
        "unverified_extrapolations": [
            ("eBAT is modeled as a mechanism-agnostic second node (like CDK4/6i for histiocytic "
             "sarcoma), applied identically to every clone -- real, but not measured for eBAT "
             "specifically; see hsa_scenarios module docstring for the mechanistic rationale"),
            ("ebat_max_kill has no real dose-response curve to anchor to (HSA_EBAT_TRIAL "
             "identified one active dose, not a titratable relationship) -- swept, not fitted"),
            ("stacks on top of every extrapolation already listed in hsa_resistance_demo's "
             "summary.json"),
        ],
        "warning": (
            "eBAT's real trial data (~70% vs. <40% 6-month survival) is not restricted to, or "
            "reported by, PIK3CA/PTEN driver status, and was never tested in combination with a "
            "PI3K/mTOR inhibitor -- this demo tests the *shape* of whether a mechanism-agnostic "
            "second node closes this scenario's own modeled resistance routes, not a validated "
            "prediction for the real combination."
        ),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


def hsa_vaccine_followon_demo(out: Path, ebat_max_kill: float = 0.0, inhibitor_active: bool = True,
                              horizon_days: int = 730, trials: int = 300,
                              preexisting_prob: float = _PREEXISTING_PROB_CENTRAL,
                              seed: int = 7) -> None:
    """Does layering a cancer vaccine on top of PI3K/mTOR-inhibitor (+/- eBAT) therapy close the
    gap left by drug resistance alone, the same question `mapk_cli.vaccine_followon_demo` asks for
    histiocytic sarcoma? `ebat_max_kill=0.0` (the default) tests inhibitor+vaccine only, with no
    eBAT contribution -- pass a nonzero value to test the full three-way combination instead.
    `inhibitor_active=False` tests vaccine (+/- eBAT) with no PI3K/mTOR inhibitor at all -- the
    combination actually closest to how the four real HSA vaccine trials were tested (surgery
    +/- doxorubicin-based chemo, never with a PI3K/mTOR inhibitor).

    Real HSA vaccines don't target this scenario's driver mutation (PIK3CA/PTEN) at all -- see
    `hsa_scenarios` module docstring for the real trials (ERstrePs, eVim, autologous whole-cell,
    a real vaccine that failed on a key readout, and one still-enrolling trial) and why targeting
    a genotype-agnostic antigen instead makes the antigen-persistence argument more secure here,
    not less.
    """
    out.mkdir(parents=True, exist_ok=True)
    scenarios = hsa_vaccine_followon_scenarios(ebat_max_kill, inhibitor_active, HSA_VACCINE_MAX_KILL_SWEEP)
    css_2 = HSA_EBAT_ILLUSTRATIVE_CSS_NM if ebat_max_kill > 0 else None

    rows, outcomes = [], {}
    for vaccine_max_kill, (model, css, seeding_rates, _) in scenarios.items():
        outcome = run_monte_carlo_with_vaccine(
            model, css, horizon_days, seeding_rates, vaccine_start_day=HSA_VACCINE_START_DAY,
            vaccine_ramp_days=HSA_VACCINE_RAMP_DAYS, vaccine_max_kill=vaccine_max_kill,
            immune_escape_seeding_rate=HSA_IMMUNE_ESCAPE_SEEDING_RATE,
            clone_names=HSA_VACCINE_CLONE_NAMES, trials=trials,
            preexisting_prob=preexisting_prob, css_reference_2=css_2, seed=seed)
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
        "ebat_max_kill_used": ebat_max_kill, "inhibitor_active": inhibitor_active, "sensitivity": rows,
        "real_hsa_vaccine_trials": HSA_VACCINE_TRIALS,
        "unverified_extrapolations": [
            ("no canine hemangiosarcoma vaccine trial measures this scenario's own PIK3CA/PTEN "
             "driver mutation status in its enrolled dogs, as far as could be determined -- "
             "the real trials above are not restricted to (or even reported by) genotype, so "
             "they cannot directly validate a subtype-specific model like this one"),
            ("vaccine_start_day, vaccine_ramp_days, vaccine_max_kill, and the immune-escape "
             "clone's seeding rate and fitness penalty are all illustrative placeholders, not "
             "fit to any of the four real trials in HSA_VACCINE_TRIALS"),
            ("if ebat_max_kill > 0: eBAT's real trial (HSA_EBAT_TRIAL) was never tested "
             "alongside a PI3K/mTOR inhibitor or a vaccine -- this tests the shape of a "
             "three-way combination none of the real trials above evaluated"),
            ("stacks on top of every extrapolation already listed in hsa_resistance_demo's and "
             "hsa_combination_control_demo's summary.json"),
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


def hsa_combination_search_demo(out: Path, trials: int = 300, horizon_days: int = 730,
                                preexisting_prob: float = _PREEXISTING_PROB_CENTRAL,
                                seed: int = 7) -> None:
    """Searches combination space directly rather than assuming which pairing wins: a full grid
    over eBAT potency x vaccine potency, inhibitor always present as the base -- reports which
    combinations reach durable response and which don't, plus the eBAT-monotherapy (no inhibitor)
    comparison point, so "does the inhibitor matter at all" is also answered rather than assumed.

    This exists because it's easy to build one combination, declare it good enough, and never
    check whether a simpler alternative does just as well, or whether a piece assumed necessary
    actually is -- exactly the check that found histiocytic sarcoma's drug+vaccine (no CDK4/6i)
    alternative performed almost as well as the full three-drug combination there.
    """
    out.mkdir(parents=True, exist_ok=True)
    rows = {}
    for ebat_max_kill in HSA_EBAT_MAX_KILL_SWEEP:
        scenarios = hsa_vaccine_followon_scenarios(ebat_max_kill, HSA_VACCINE_MAX_KILL_SWEEP)
        css_2 = HSA_EBAT_ILLUSTRATIVE_CSS_NM if ebat_max_kill > 0 else None
        for vaccine_max_kill, (model, css, seeding_rates, _) in scenarios.items():
            outcome = run_monte_carlo_with_vaccine(
                model, css, horizon_days, seeding_rates, vaccine_start_day=HSA_VACCINE_START_DAY,
                vaccine_ramp_days=HSA_VACCINE_RAMP_DAYS, vaccine_max_kill=vaccine_max_kill,
                immune_escape_seeding_rate=HSA_IMMUNE_ESCAPE_SEEDING_RATE,
                clone_names=HSA_VACCINE_CLONE_NAMES, trials=trials,
                preexisting_prob=preexisting_prob, css_reference_2=css_2, seed=seed)
            rows[(ebat_max_kill, vaccine_max_kill)] = float(1 - outcome.progressed.mean())

    grid = pd.DataFrame(
        [{"ebat_max_kill": e, "vaccine_max_kill": v, "probability_durable_response": p}
         for (e, v), p in rows.items()])
    grid.to_csv(out / "hsa_combination_search_grid.csv", index=False)
    pivot = grid.pivot(index="ebat_max_kill", columns="vaccine_max_kill",
                       values="probability_durable_response")

    ebat_alone_scenarios = hsa_combination_scenarios(inhibitor_active=False,
                                                     ebat_max_kill_values=HSA_EBAT_MAX_KILL_SWEEP)
    ebat_alone_durable = {}
    for ebat_max_kill, (model, css, seeding_rates, _) in ebat_alone_scenarios.items():
        css_2 = HSA_EBAT_ILLUSTRATIVE_CSS_NM if ebat_max_kill > 0 else None
        outcome = run_monte_carlo(model, css, horizon_days, seeding_rates, trials,
                                  preexisting_prob=preexisting_prob, css_reference_2=css_2, seed=seed)
        ebat_alone_durable[ebat_max_kill] = float(1 - outcome.progressed.mean())

    fig, ax = plt.subplots(figsize=(7, 5.5))
    im = ax.imshow(pivot.values, origin="lower", aspect="auto", vmin=0, vmax=1, cmap="viridis")
    ax.set_xticks(range(len(pivot.columns))); ax.set_xticklabels(pivot.columns)
    ax.set_yticks(range(len(pivot.index))); ax.set_yticklabels(pivot.index)
    ax.set(xlabel="vaccine max_kill", ylabel="eBAT max_kill",
          title="P(durable response): inhibitor always on")
    fig.colorbar(im, ax=ax, label="P(durable response)")
    fig.tight_layout(); fig.savefig(out / "hsa_combination_search_grid.png", dpi=160); plt.close(fig)

    durable_threshold = 0.95
    sufficient = grid[grid["probability_durable_response"] >= durable_threshold]
    minimal_combinations = []
    if len(sufficient):
        for ebat_max_kill in sorted(sufficient["ebat_max_kill"].unique()):
            min_vaccine = sufficient[sufficient["ebat_max_kill"] == ebat_max_kill]["vaccine_max_kill"].min()
            minimal_combinations.append({"ebat_max_kill": float(ebat_max_kill),
                                        "min_vaccine_max_kill_needed": float(min_vaccine)})

    minimal_combinations_display = (minimal_combinations if minimal_combinations
                                    else "no grid point tested reached this threshold")
    summary = {
        "trials": trials, "horizon_days": horizon_days, "preexisting_prob_used": preexisting_prob,
        "durable_response_threshold": durable_threshold,
        "grid": grid.to_dict(orient="records"),
        "ebat_monotherapy_no_inhibitor": ebat_alone_durable,
        "minimal_combinations_reaching_threshold": minimal_combinations,
        "interpretation": (
            f"At >= {durable_threshold:.0%} durable response ({horizon_days}-day horizon, "
            f"inhibitor always present): {minimal_combinations_display}. Compare against "
            "inhibitor+eBAT alone (vaccine_max_kill=0 rows above) and inhibitor+vaccine alone "
            "(ebat_max_kill=0 rows) to see whether either single addition suffices, or whether "
            "both are needed -- "
            "read the grid, not just this summary line, since the minimal-combination search "
            "only reports the *first* vaccine potency that clears the threshold per eBAT level, "
            "not the full shape. ebat_monotherapy_no_inhibitor answers a different question: "
            "does the PI3K/mTOR inhibitor matter at all, or could eBAT alone substitute for it."
        ),
        "unverified_extrapolations": [
            ("this grid answers 'which combination closes this scenario's own modeled "
             "resistance routes,' not 'which combination cures a real dog' -- every "
             "extrapolation listed in hsa_resistance_demo's, hsa_combination_control_demo's, "
             "and hsa_vaccine_followon_demo's summary.json applies here too"),
            ("no real trial has tested inhibitor+eBAT+vaccine together, or reported outcomes "
             "by PIK3CA/PTEN driver status, so nothing in this grid can be checked against real "
             "combination data the way histiocytic sarcoma's single-agent scenarios could be "
             "checked against real case reports"),
        ],
        "warning": (
            "A search over this module's own parameter space, not a search over real treatment "
            "options -- it can only ever be as good as the illustrative growth/kill/seeding-rate "
            "constants underneath it. Read 'combination X reaches 95% durable response here' as "
            "'given everything else this module assumes, X closes the gap in this model,' not "
            "as a treatment recommendation."
        ),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


def hsa_receptor_conservation_demo(out: Path,
                                   genes: list[str] = list(HSA_RECEPTOR_CONSERVATION_TARGETS)
                                   ) -> None:
    """Checks whether the real drugs' molecular targets are conserved enough between human and
    dog for a human precedent to plausibly transfer, using genomics/structure directly rather
    than depending on clinical-trial outcome data (which the eBAT comparison found to be
    confounded by a real, unmodeled mechanism). See `HSA_RECEPTOR_CONSERVATION_TARGETS` and the
    `hsa_scenarios` module docstring for what each gene means and what was found.

    Requires network access (UniProt, AlphaFold DB). Genes with no UniProt entry for either
    species are reported as `"found": false` rather than raising -- a real data gap (confirmed
    live, e.g. PLAUR has no curated dog entry at all) is a finding, not an error to hide.
    """
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for gene in genes:
        row = {"gene": gene, "context": HSA_RECEPTOR_CONSERVATION_TARGETS[gene], "found": False}
        try:
            human_accession = resolve_uniprot_accession(gene, HUMAN_TAXID)
            dog_accession = resolve_uniprot_accession(gene, DOG_TAXID)
            human_struct = download_structure(human_accession, out / "structures" / f"{gene}_human")
            dog_struct = download_structure(dog_accession, out / "structures" / f"{gene}_dog")
            human_seq = "".join(read_plddt_track(human_struct)["residue_type"])
            dog_seq = "".join(read_plddt_track(dog_struct)["residue_type"])
            stats = whole_sequence_identity(human_seq, dog_seq)
            row.update(found=True, human_uniprot=human_accession, dog_uniprot=dog_accession, **stats)
        except (ValueError, OSError) as error:
            row["error"] = str(error)
        rows.append(row)
    table = pd.DataFrame(rows)
    table.to_csv(out / "receptor_conservation.csv", index=False)

    summary = {
        "genes_checked": list(genes), "results": rows,
        "unverified_extrapolations": [
            ("sequence identity is not the same as functional conservation -- a receptor could "
             "be highly identical overall but differ at the specific ligand-binding residues "
             "that determine whether a human-designed ligand/toxin actually binds, or vice "
             "versa; this checks whole-protein identity, not the binding interface specifically"),
            ("a gene with no UniProt entry for dog (found=false) does not mean the gene is "
             "absent from the dog genome -- it means UniProt has no curated/predicted entry "
             "under that exact gene symbol as of this check, which could reflect an annotation "
             "gap rather than biology"),
        ],
        "warning": (
            "This checks molecular conservation, not efficacy -- it can support or undercut the "
            "plausibility of a human-designed drug/vaccine's mechanism transferring to dogs, but "
            "it cannot confirm the real trials' reported outcomes are caused by the mechanism "
            "this module assumes, or rule out other explanations."
        ),
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


def hsa_vaccine_antigen_design_demo(out: Path, gene: str = "VIM", window: int = 9,
                                    top_n: int = 3) -> None:
    """Replaces "vaccine antigen: generic placeholder" with an actual structure-based candidate:
    which part of the real dog antigen is solvent-exposed enough to plausibly be reachable by a
    circulating antibody, using the dog structure already fetched for `hsa_receptor_conservation_
    demo` (default gene VIM -- eVim's real antigen, the one HSA vaccine confirmed to work through
    an antibody, not a T-cell, mechanism).

    This does not, and cannot, produce a `vaccine_max_kill` number: no structural tool predicts
    immunogenicity, antibody titer, or in vivo efficacy from a folded structure alone. What it
    can do is answer a narrower, checkable question -- is there a real, contiguous, solvent-
    exposed loop on the actual dog protein to target at all, as opposed to only buried residues a
    real antibody could never reach -- and whether that loop is conserved with the human ortholog
    (relevant if a human vaccine's exact epitope is meant to transfer to dogs) or dog-specific.

    Requires network access (UniProt, AlphaFold DB).
    """
    out.mkdir(parents=True, exist_ok=True)
    dog_accession = resolve_uniprot_accession(gene, DOG_TAXID)
    human_accession = resolve_uniprot_accession(gene, HUMAN_TAXID)
    dog_struct = download_structure(dog_accession, out / "structures" / f"{gene}_dog")
    human_struct = download_structure(human_accession, out / "structures" / f"{gene}_human")
    dog_track = read_plddt_track(dog_struct)
    human_seq = "".join(read_plddt_track(human_struct)["residue_type"])
    dog_seq = "".join(dog_track["residue_type"])

    burial = contact_number_burial(dog_track)
    candidates = find_exposed_linear_epitopes(burial, window=window, top_n=top_n)
    dog_to_human = align_residue_numbers(dog_seq, human_seq)
    conservation = []
    for _, candidate in candidates.iterrows():
        positions = list(range(int(candidate["start_residue"]), int(candidate["end_residue"]) + 1))
        aligned = [dog_to_human[p] for p in positions if p in dog_to_human]
        identical = sum(1 for _, is_identical in aligned if is_identical)
        conservation.append({
            "fraction_aligned_to_human": len(aligned) / len(positions),
            "fraction_identical_to_human": identical / len(aligned) if aligned else None,
        })
    candidates = pd.concat([candidates, pd.DataFrame(conservation)], axis=1)
    candidates.to_csv(out / "candidate_epitopes.csv", index=False)

    fig, axes = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
    axes[0].plot(burial["residue_number"], burial["contact_number"], color="tab:blue")
    axes[1].plot(burial["residue_number"], burial["plddt"], color="tab:orange")
    for _, candidate in candidates.iterrows():
        for ax in axes:
            ax.axvspan(candidate["start_residue"], candidate["end_residue"], color="tab:green", alpha=.3)
    axes[0].set(ylabel="CA contact number\n(lower = more exposed)")
    axes[1].set(ylabel="pLDDT", xlabel="residue number",
               title="pLDDT (shaded bands = candidate exposed epitope windows)")
    axes[0].set_title(f"{gene} (dog, {dog_accession}): burial track with candidate epitope windows")
    fig.tight_layout(); fig.savefig(out / "candidate_epitopes.png", dpi=160); plt.close(fig)

    summary = {
        "gene": gene, "dog_uniprot": dog_accession, "human_uniprot": human_accession,
        "window": window, "top_n": top_n, "method": "CA contact-number burial (radius=10 A)",
        "candidate_epitopes": candidates.to_dict(orient="records"),
        "unverified_extrapolations": [
            "solvent exposure (even true SASA, which this coarse CA-only proxy approximates) is "
            "necessary but not sufficient for a good antibody epitope -- it says nothing about "
            "immunogenicity, whether the region is glycosylated or otherwise shielded in vivo, or "
            "whether raising antibodies against it actually disrupts the antigen's function or "
            "helps clear the tumor",
            "this ranks windows within one structure; it is not validated against any real "
            "epitope-mapping experiment for VIM or any other HSA antigen",
            "does not produce a vaccine_max_kill value or any other Monte Carlo model parameter -- "
            "vaccine_max_kill remains an illustrative, swept potency number regardless of which "
            "epitope a real vaccine construct targets",
        ],
        "warning": "Structural plausibility for antibody accessibility, not a vaccine design tool "
                  "and not an efficacy prediction. AlphaFold predicts structure from a known "
                  "sequence; it does not generate or invent new antigen sequences.",
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


def hsa_combination_toxicity_demo(out: Path, ebat_max_kill: float = 0.05, trials: int = 300,
                                  horizon_days: int = 730,
                                  preexisting_prob: float = _PREEXISTING_PROB_CENTRAL,
                                  seed: int = 7) -> None:
    """Stress-tests the inhibitor+eBAT combination against realistic combined-dosing de-rating,
    mirroring `mapk_cli.combination_toxicity_demo` -- but grounded in real, documented, same-
    organ-system (hepatic/GI) toxicity for both drugs specifically, not an extrapolated
    mechanism-class argument. See `HSA_TOXICITY_EXTRAPOLATION_NOTE`.

    Fixes eBAT potency at `ebat_max_kill` (default 0.05, the threshold that reached durable
    response in `hsa_combination_search_demo`) and sweeps `HSA_COMBINED_EXPOSURE_DERATING`,
    applying it multiplicatively to both the inhibitor and eBAT reference concentrations.
    """
    out.mkdir(parents=True, exist_ok=True)
    scenarios = hsa_combination_scenarios(True, [ebat_max_kill])
    model, css, seeding_rates, _ = scenarios[ebat_max_kill]

    rows, outcomes = [], {}
    for derating in HSA_COMBINED_EXPOSURE_DERATING:
        outcome = run_monte_carlo(model, css * derating, horizon_days, seeding_rates, trials,
                                  preexisting_prob=preexisting_prob,
                                  css_reference_2=HSA_EBAT_ILLUSTRATIVE_CSS_NM * derating, seed=seed)
        outcomes[derating] = outcome
        ttp = outcome.time_to_progression[outcome.progressed]
        mechanism_counts = pd.Series(outcome.dominant_mechanism).value_counts()
        mechanism_fractions = (mechanism_counts.reindex(["durable_response"] + HSA_CLONE_NAMES[1:],
                                                        fill_value=0)
                              / len(outcome.dominant_mechanism))
        rows.append({
            "combined_exposure_derating": derating,
            "inhibitor_css_nM": css * derating,
            "ebat_css_nM": HSA_EBAT_ILLUSTRATIVE_CSS_NM * derating,
            "probability_durable_response": float(1 - outcome.progressed.mean()),
            "probability_progression": float(outcome.progressed.mean()),
            "median_time_to_progression_days": float(np.median(ttp)) if ttp.size else None,
            **{f"mechanism_{mechanism}": float(value) for mechanism, value in mechanism_fractions.items()},
        })
    table = pd.DataFrame(rows)
    table.to_csv(out / "hsa_toxicity_derating_sensitivity.csv", index=False)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(table["combined_exposure_derating"], table["probability_durable_response"],
           marker="o", color="tab:purple")
    ax.set(xlabel="fraction of illustrative full exposure (both drugs)", ylabel="P(durable response)",
          title=f"does inhibitor+eBAT (max_kill={ebat_max_kill}) survive realistic dose reduction?",
          ylim=(0, 1.02))
    fig.tight_layout(); fig.savefig(out / "hsa_toxicity_derating.png", dpi=160); plt.close(fig)

    summary = {
        "ebat_max_kill_tested": ebat_max_kill, "preexisting_prob_used": preexisting_prob,
        "sensitivity": rows, "toxicity_extrapolation_rationale": HSA_TOXICITY_EXTRAPOLATION_NOTE,
        "unverified_extrapolations": [
            "no canine dose-finding trial has combined a PI3K/mTOR inhibitor with eBAT; "
            "HSA_COMBINED_EXPOSURE_DERATING is a plausible range grounded in the drugs' separate "
            "real toxicity profiles overlapping on organ system, not a measured combination-trial "
            "de-escalation schedule",
            "assumes both drugs de-rate by the same fraction simultaneously; a real Phase Ib "
            "trial could de-escalate one drug more than the other depending on which toxicity "
            "proves dose-limiting first",
        ],
        "warning": "A parameter-space stress test of this module's own illustrative model, not a "
                  "real combined-dosing safety study.",
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


def hsa_durability_horizon_demo(out: Path, ebat_max_kill: float = 0.05, vaccine_max_kill: float = 0.0,
                                inhibitor_active: bool = True, trials: int = 300,
                                preexisting_prob: float = _PREEXISTING_PROB_CENTRAL,
                                seed: int = 7) -> None:
    """How long does "durable response" actually mean for a given HSA combination, the same
    question `mapk_cli.durability_horizon_demo` asks for histiocytic sarcoma? No HSA demo had
    ever been run past the default 730-day horizon before this was added -- every "durable
    response" figure quoted for HSA up to this point meant only "no relapse detected within 2
    years," unverified at longer horizons.

    Sweeps `HSA_DURABILITY_HORIZON_SWEEP` (1, 2, 5, 10 years) at a fixed `(ebat_max_kill,
    vaccine_max_kill)` combination, reusing `hsa_vaccine_followon_scenarios` (vaccine_max_kill=0.0
    still runs the 5-clone vaccine model with a harmless immune-escape clone, so eBAT-only and
    vaccine-only regimens can both be tested through the same code path as the full combination).
    """
    out.mkdir(parents=True, exist_ok=True)
    scenarios = hsa_vaccine_followon_scenarios(ebat_max_kill, inhibitor_active, [vaccine_max_kill])
    model, css, seeding_rates, _ = scenarios[vaccine_max_kill]
    css_2 = HSA_EBAT_ILLUSTRATIVE_CSS_NM if ebat_max_kill > 0 else None

    rows = []
    for horizon_days in HSA_DURABILITY_HORIZON_SWEEP:
        outcome = run_monte_carlo_with_vaccine(
            model, css, horizon_days, seeding_rates, vaccine_start_day=HSA_VACCINE_START_DAY,
            vaccine_ramp_days=HSA_VACCINE_RAMP_DAYS, vaccine_max_kill=vaccine_max_kill,
            immune_escape_seeding_rate=HSA_IMMUNE_ESCAPE_SEEDING_RATE,
            clone_names=HSA_VACCINE_CLONE_NAMES, trials=trials,
            preexisting_prob=preexisting_prob, css_reference_2=css_2, seed=seed)
        ttp = outcome.time_to_progression[outcome.progressed]
        mechanism_counts = pd.Series(outcome.dominant_mechanism).value_counts()
        mechanism_fractions = (mechanism_counts.reindex(["durable_response"] + HSA_VACCINE_CLONE_NAMES[1:],
                                                        fill_value=0)
                              / len(outcome.dominant_mechanism))
        rows.append({
            "horizon_days": horizon_days, "horizon_years": horizon_days / 365,
            "probability_durable_response": float(1 - outcome.progressed.mean()),
            "probability_progression": float(outcome.progressed.mean()),
            "median_time_to_progression_days": float(np.median(ttp)) if ttp.size else None,
            **{f"mechanism_{mechanism}": float(value) for mechanism, value in mechanism_fractions.items()},
        })
    table = pd.DataFrame(rows)
    table.to_csv(out / "hsa_durability_horizon_sensitivity.csv", index=False)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(table["horizon_years"], table["probability_durable_response"], marker="o", color="tab:green")
    ax.set(xlabel="years of follow-up simulated", ylabel="P(no relapse detected by this horizon)",
          title=f"how long is \"durable\"? ebat={ebat_max_kill}, vaccine={vaccine_max_kill}, "
                f"inhibitor_active={inhibitor_active}",
          ylim=(0, 1.02))
    fig.tight_layout(); fig.savefig(out / "hsa_durability_horizon.png", dpi=160); plt.close(fig)

    summary = {
        "ebat_max_kill_tested": ebat_max_kill, "vaccine_max_kill_tested": vaccine_max_kill,
        "inhibitor_active": inhibitor_active, "preexisting_prob_used": preexisting_prob,
        "sensitivity": rows,
        "unverified_extrapolations": [
            "this scenario has never been followed anywhere near 5 or 10 years in any real dog; "
            "every horizon beyond the ~2 years the real eBAT/vaccine trials actually followed "
            "patients is a pure extrapolation of this module's own illustrative growth/kill rates",
            "HSA's real-world catastrophic-event mechanism (tumor rupture/hemorrhage) is still not "
            "modeled at any horizon -- a long simulated horizon with no relapse detected is not "
            "the same claim as a real dog surviving that long without a fatal bleed",
        ],
        "warning": "Extends this module's own parameter space to horizons no real trial has "
                  "observed; not a projection of what any real dog's long-term outcome would be.",
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
