import json
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
