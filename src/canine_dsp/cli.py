import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .alphafold_cli import analyze_structure, fetch_structure
from .hsa_cli import (
    hsa_combination_control_demo,
    hsa_combination_search_demo,
    hsa_combination_toxicity_demo,
    hsa_durability_horizon_demo,
    hsa_receptor_conservation_demo,
    hsa_resistance_demo,
    hsa_vaccine_antigen_design_demo,
    hsa_vaccine_followon_demo,
)
from .antigen_convergence_cli import antigen_convergence_demo
from .endurance_answer_cli import endurance_answer_demo
from .histiocytic_cli import driver_hypothesis_demo
from .hsa_scenarios import HSA_EBAT_EXPOSURE_DURATION_DAYS
from .hsa_scenarios import _PREEXISTING_PROB_CENTRAL as HSA_PREEXISTING_PROB_CENTRAL
from .hybrid_cli import inverse_demo, prepare_dog10k_aging, prepare_gse9794
from .immunotherapy_cli import immunotherapy_demo
from .io import read_first_fasta, read_vcf_positions
from .mapk_cli import (
    combination_control_demo,
    combination_toxicity_demo,
    compare_orthologs,
    durability_horizon_demo,
    localized_control_demo,
    mapk_cns_demo,
    mapk_resistance_demo,
    pulmonary_two_compartment_demo,
    single_patient_feasibility_demo,
    vaccine_epitope_binding_demo,
    vaccine_followon_demo,
)
from .lymphoma_cli import (
    lymphoma_durability_horizon_demo,
    lymphoma_immunotherapy_demo,
    lymphoma_resistance_demo,
    lymphoma_sanctuary_demo,
)
from .mapk_scenarios import DEBULKING_FRACTION
from .mapk_scenarios import _PREEXISTING_PROB_CENTRAL as MAPK_PREEXISTING_PROB_CENTRAL
from .melanoma_benchmark import run_melanoma_benchmark
from .mutational_supply_cli import mutational_supply_demo
from .off_policy_cli import evaluate_logged_policy_file
from .osteosarcoma_benchmark import run_osteosarcoma_benchmark
from .osteosarcoma_data import prepare_gse76127
from .pharmacology_cli import cdk46_achievability_demo
from .signals import eiip, variant_density, windowed_gc
from .single_patient_cli import single_patient_demo
from .spectral import coherence, multitaper_psd, spectral_entropy, welch_psd
from .stochastic_cli import stochastic_immunotherapy_demo
from .superiority_cli import policy_superiority_benchmark
from .vaccine_eval import run_gse102459, run_gse190001
from .volterra_cli import run_volterra, synthetic_table
from .wavelets import cwt_power


def _save_spectrum(x: np.ndarray, out: Path, title: str, sample_spacing: float = 1.0) -> dict:
    fs = 1 / sample_spacing
    fw, pw = welch_psd(x, fs)
    fm, pm = multitaper_psd(x, fs)
    pd.DataFrame({"frequency": fm, "multitaper_psd": pm}).to_csv(out / "spectrum.csv", index=False)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.semilogy(fw[1:], pw[1:] + np.finfo(float).eps, label="Welch")
    ax.semilogy(fm[1:], pm[1:] + np.finfo(float).eps, label="Multitaper", alpha=.8)
    ax.set(xlabel="cycles / bp" if sample_spacing == 1 else "cycles / bp", ylabel="PSD", title=title)
    ax.legend(); fig.tight_layout(); fig.savefig(out / "spectrum.png", dpi=160); plt.close(fig)
    peak = int(np.argmax(pm[1:]) + 1)
    return {"spectral_entropy": spectral_entropy(pm), "peak_frequency": float(fm[peak]),
            "peak_period_bp": float(1 / fm[peak]) if fm[peak] > 0 else None}


def analyze(sequence: str, out: Path, window: int, positions: np.ndarray | None = None) -> None:
    out.mkdir(parents=True, exist_ok=True)
    summary = {"sequence_length": len(sequence), "window_bp": window}
    summary["eiip"] = _save_spectrum(eiip(sequence), out, "EIIP sequence spectrum")
    gc = windowed_gc(sequence, window)
    pd.DataFrame({"window_start_0based": np.arange(len(gc)) * window, "gc_fraction": gc}).to_csv(
        out / "gc_track.csv", index=False)
    scales, frequencies, power = cwt_power(eiip(sequence))
    np.savez_compressed(out / "wavelet_power.npz", scales=scales, frequencies=frequencies, power=power)
    fig, ax = plt.subplots(figsize=(9, 4)); ax.imshow(np.log1p(power), aspect="auto", origin="lower",
        extent=[0, len(sequence), scales.min(), scales.max()]); ax.set(xlabel="base index", ylabel="scale",
        title="EIIP Morlet wavelet power"); fig.tight_layout(); fig.savefig(out / "wavelet.png", dpi=160); plt.close(fig)
    if positions is not None:
        vd = variant_density(positions, len(sequence), window)[:len(gc)]
        pd.DataFrame({"window_start_0based": np.arange(len(vd)) * window,
                      "variant_count": vd}).to_csv(out / "variant_track.csv", index=False)
        if len(vd) >= 8:
            f, c = coherence(gc[:len(vd)], vd, fs=1 / window)
            pd.DataFrame({"frequency_cycles_per_bp": f, "coherence": c}).to_csv(
                out / "gc_variant_coherence.csv", index=False)
            summary["max_gc_variant_coherence"] = float(np.max(c[1:])) if len(c) > 1 else None
        summary["variant_count"] = int(len(positions))
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="DSP analysis of canine genomic signals")
    sub = parser.add_subparsers(dest="command", required=True)
    demo = sub.add_parser("demo"); demo.add_argument("--out", type=Path, default=Path("results/demo"))
    run = sub.add_parser("analyze"); run.add_argument("--fasta", type=Path, required=True)
    run.add_argument("--vcf", type=Path); run.add_argument("--window", type=int, default=1000)
    run.add_argument("--out", type=Path, required=True)
    volterra = sub.add_parser("volterra-fit", help="fit a chromosome-validated Volterra model")
    volterra.add_argument("--table", type=Path, required=True)
    volterra.add_argument("--inputs", nargs="+", required=True)
    volterra.add_argument("--target", required=True)
    volterra.add_argument("--group", default="chromosome")
    volterra.add_argument("--exposure")
    volterra.add_argument("--memory", type=int, default=11)
    volterra.add_argument("--basis", type=int, default=4)
    volterra.add_argument("--order", type=int, choices=[1, 2], default=2)
    volterra.add_argument("--family", choices=["gaussian", "poisson"], default="poisson")
    volterra.add_argument("--alpha", type=float, default=.01)
    volterra.add_argument("--l1-ratio", type=float, default=.5)
    volterra.add_argument("--out", type=Path, required=True)
    synth = sub.add_parser("volterra-demo", help="generate and fit a known nonlinear system")
    synth.add_argument("--out", type=Path, default=Path("results/volterra-demo"))
    expression = sub.add_parser("prepare-gse9794", help="prepare a real canine RNA time course")
    expression.add_argument("--matrix", type=Path, required=True)
    expression.add_argument("--modules", type=int, default=8)
    expression.add_argument("--out", type=Path, required=True)
    aging = sub.add_parser("prepare-dog10k-aging", help="prepare real Dog10K aging expression")
    aging.add_argument("--expression", type=Path, required=True)
    aging.add_argument("--information", type=Path, required=True)
    aging.add_argument("--modules", type=int, default=8)
    aging.add_argument("--out", type=Path, required=True)
    inverse = sub.add_parser("inverse-demo", help="run robust vaccine inverse-control benchmark")
    inverse.add_argument("--scenarios", type=int, default=8)
    inverse.add_argument("--maxiter", type=int, default=60)
    inverse.add_argument("--out", type=Path, default=Path("results/inverse-demo"))
    immunotherapy = sub.add_parser("immunotherapy-demo", help="run combination-therapy inverse benchmark")
    immunotherapy.add_argument("--scenarios", type=int, default=12)
    immunotherapy.add_argument("--maxiter", type=int, default=60)
    immunotherapy.add_argument("--out", type=Path, default=Path("results/immunotherapy-demo"))
    stochastic = sub.add_parser("stochastic-immunotherapy-demo",
                                help="run stochastic state-space inverse benchmark")
    stochastic.add_argument("--draws", type=int, default=256)
    stochastic.add_argument("--particles", type=int, default=384)
    stochastic.add_argument("--maxiter", type=int, default=24)
    stochastic.add_argument("--seed", type=int, default=42)
    stochastic.add_argument("--out", type=Path,
                            default=Path("results/stochastic-immunotherapy-demo"))
    benchmark = sub.add_parser("immunotherapy-policy-benchmark",
                               help="compare locked PK/PD-QSP and Volterra policies")
    benchmark.add_argument("--draws", type=int, default=96)
    benchmark.add_argument("--scenarios", type=int, default=12)
    benchmark.add_argument("--maxiter", type=int, default=18)
    benchmark.add_argument("--seed", type=int, default=73)
    benchmark.add_argument("--reference-schedule", type=Path)
    benchmark.add_argument("--out", type=Path,
                           default=Path("results/immunotherapy-policy-benchmark"))
    logged = sub.add_parser("evaluate-logged-policy",
                            help="run fail-closed longitudinal off-policy evaluation")
    logged.add_argument("--table", type=Path, required=True)
    logged.add_argument("--gamma", type=float, default=1.0)
    logged.add_argument("--cross-fitted", action="store_true")
    logged.add_argument("--out", type=Path, required=True)
    melanoma = sub.add_parser(
        "melanoma-neoadjuvant-benchmark",
        help="benchmark a nonlinear stochastic DSP policy against OpACIN-neo and NADINA",
    )
    melanoma.add_argument("--anchors", type=Path,
                          default=Path("data/clinical/melanoma_clinical_anchors.csv"))
    melanoma.add_argument("--draws", type=int, default=192)
    melanoma.add_argument("--candidates", type=int, default=96)
    melanoma.add_argument("--seed", type=int, default=142)
    melanoma.add_argument("--out", type=Path,
                          default=Path("results/melanoma-neoadjuvant-benchmark"))
    osteo_data = sub.add_parser(
        "prepare-gse76127",
        help="prepare the real 33-dog osteosarcoma tumor/DFI cohort",
    )
    osteo_data.add_argument("--matrix", type=Path, required=True)
    osteo_data.add_argument("--supplements", type=Path, required=True)
    osteo_data.add_argument("--components", type=int, default=5)
    osteo_data.add_argument("--out", type=Path, required=True)
    osteo = sub.add_parser(
        "osteosarcoma-rna-design",
        help="run the comparative Volterra-HSMM RNA-vaccine design benchmark",
    )
    osteo.add_argument("--anchors", type=Path,
                       default=Path("data/clinical/osteosarcoma_clinical_anchors.csv"))
    osteo.add_argument(
        "--candidates", type=Path,
        help="deidentified candidate-feature CSV; requires --design-spec",
    )
    osteo.add_argument(
        "--design-spec", type=Path,
        help="schema-v1 JSON with patient-specific DLA/clone constraints and scenarios",
    )
    osteo.add_argument(
        "--gse76127-matrix", type=Path,
        default=Path("data/raw/gse76127/GSE76127_series_matrix.txt.gz"),
    )
    osteo.add_argument(
        "--gse76127-supplements", type=Path,
        default=Path("data/raw/gse76127/PMC4759767_SupplementaryFiles.zip"),
    )
    osteo.add_argument("--skip-real-data", action="store_true")
    osteo.add_argument("--draws", type=int, default=192)
    osteo.add_argument("--seed", type=int, default=2608)
    osteo.add_argument("--out", type=Path,
                       default=Path("results/osteosarcoma-rna-design"))
    vaccine_eval = sub.add_parser("evaluate-gse190001", help="validate vaccine-response kernels")
    vaccine_eval.add_argument("--prime", type=Path, required=True)
    vaccine_eval.add_argument("--boost", type=Path, required=True)
    vaccine_eval.add_argument("--soft", type=Path, required=True)
    vaccine_eval.add_argument("--out", type=Path, required=True)
    external = sub.add_parser("evaluate-gse102459", help="external two-dose vaccine replication")
    external.add_argument("--matrix", type=Path, required=True)
    external.add_argument("--modules", type=int, default=3)
    external.add_argument("--out", type=Path, required=True)
    af_fetch = sub.add_parser("alphafold-fetch", help="download an AlphaFold DB model by UniProt accession")
    af_fetch.add_argument("--uniprot", required=True)
    af_fetch.add_argument("--out", type=Path, required=True)
    af_analyze = sub.add_parser("alphafold-analyze", help="spectral analysis of an AlphaFold confidence track")
    af_analyze.add_argument("--struct", type=Path, required=True)
    af_analyze.add_argument("--variants", type=Path)
    af_analyze.add_argument("--flank", type=int, default=5)
    af_analyze.add_argument("--out", type=Path, required=True)
    mapk_demo = sub.add_parser("mapk-resistance-demo",
                               help="Monte Carlo MAPK-inhibitor escape simulation for histiocytic sarcoma")
    mapk_demo.add_argument("--species", choices=["dog", "human"], default="dog")
    mapk_demo.add_argument("--trials", type=int, default=300)
    mapk_demo.add_argument("--horizon-days", type=int, default=730)
    mapk_demo.add_argument("--seed", type=int, default=7)
    mapk_demo.add_argument("--out", type=Path, required=True)
    hsa_demo = sub.add_parser("hsa-resistance-demo",
                              help="Monte Carlo PI3K/mTOR-inhibitor escape simulation for the "
                                   "PIK3CA/PTEN-driven subtype of canine hemangiosarcoma")
    hsa_demo.add_argument("--trials", type=int, default=300)
    hsa_demo.add_argument("--horizon-days", type=int, default=730)
    hsa_demo.add_argument("--seed", type=int, default=7)
    hsa_demo.add_argument("--out", type=Path, required=True)
    hsa_combo_demo = sub.add_parser("hsa-combination-control-demo",
                                    help="PI3K/mTOR inhibitor vs. eBAT vs. their combination "
                                         "for canine hemangiosarcoma")
    hsa_combo_demo.add_argument("--trials", type=int, default=300)
    hsa_combo_demo.add_argument("--horizon-days", type=int, default=730)
    hsa_combo_demo.add_argument("--preexisting-prob", type=float, default=HSA_PREEXISTING_PROB_CENTRAL)
    hsa_combo_demo.add_argument("--ebat-exposure-duration-days", type=int,
                                default=HSA_EBAT_EXPOSURE_DURATION_DAYS)
    hsa_combo_demo.add_argument("--seed", type=int, default=7)
    hsa_combo_demo.add_argument("--out", type=Path, required=True)
    hsa_vaccine_demo = sub.add_parser("hsa-vaccine-followon-demo",
                                      help="PI3K/mTOR inhibitor (+/- eBAT) plus a "
                                           "real-vaccine-inspired follow-on for canine "
                                           "hemangiosarcoma")
    hsa_vaccine_demo.add_argument("--ebat-max-kill", type=float, default=0.0)
    hsa_vaccine_demo.add_argument("--no-inhibitor", action="store_true",
                                  help="test vaccine (+/- eBAT) with no PI3K/mTOR inhibitor at all")
    hsa_vaccine_demo.add_argument("--trials", type=int, default=300)
    hsa_vaccine_demo.add_argument("--horizon-days", type=int, default=730)
    hsa_vaccine_demo.add_argument("--preexisting-prob", type=float, default=HSA_PREEXISTING_PROB_CENTRAL)
    hsa_vaccine_demo.add_argument("--ebat-exposure-duration-days", type=int,
                                  default=HSA_EBAT_EXPOSURE_DURATION_DAYS)
    hsa_vaccine_demo.add_argument("--seed", type=int, default=7)
    hsa_vaccine_demo.add_argument("--out", type=Path, required=True)
    hsa_search_demo = sub.add_parser("hsa-combination-search-demo",
                                     help="grid search over eBAT x vaccine potency for canine "
                                          "hemangiosarcoma, to find which combination(s) reach "
                                          "durable response rather than assuming one")
    hsa_search_demo.add_argument("--trials", type=int, default=300)
    hsa_search_demo.add_argument("--horizon-days", type=int, default=730)
    hsa_search_demo.add_argument("--preexisting-prob", type=float, default=HSA_PREEXISTING_PROB_CENTRAL)
    hsa_search_demo.add_argument("--ebat-exposure-duration-days", type=int,
                                 default=HSA_EBAT_EXPOSURE_DURATION_DAYS)
    hsa_search_demo.add_argument("--seed", type=int, default=7)
    hsa_search_demo.add_argument("--out", type=Path, required=True)
    hsa_receptor_demo = sub.add_parser("hsa-receptor-conservation-demo",
                                       help="human-vs-dog whole-protein conservation for eBAT's "
                                            "and eVim's real molecular targets (EGFR, PLAUR, VIM)")
    hsa_receptor_demo.add_argument("--genes", nargs="+", default=None)
    hsa_receptor_demo.add_argument("--out", type=Path, required=True)
    hsa_antigen_demo = sub.add_parser("hsa-vaccine-antigen-design-demo",
                                      help="structure-based candidate B-cell epitope selection "
                                           "on a real HSA vaccine antigen (default: VIM/eVim)")
    hsa_antigen_demo.add_argument("--gene", default="VIM")
    hsa_antigen_demo.add_argument("--window", type=int, default=9)
    hsa_antigen_demo.add_argument("--top-n", type=int, default=3)
    hsa_antigen_demo.add_argument("--out", type=Path, required=True)
    hsa_tox_demo = sub.add_parser("hsa-combination-toxicity-demo",
                                  help="does the inhibitor+eBAT combination for canine "
                                       "hemangiosarcoma survive realistic combined-dose de-rating")
    hsa_tox_demo.add_argument("--ebat-max-kill", type=float, default=0.05)
    hsa_tox_demo.add_argument("--trials", type=int, default=300)
    hsa_tox_demo.add_argument("--horizon-days", type=int, default=730)
    hsa_tox_demo.add_argument("--preexisting-prob", type=float, default=HSA_PREEXISTING_PROB_CENTRAL)
    hsa_tox_demo.add_argument("--ebat-exposure-duration-days", type=int,
                              default=HSA_EBAT_EXPOSURE_DURATION_DAYS)
    hsa_tox_demo.add_argument("--seed", type=int, default=7)
    hsa_tox_demo.add_argument("--out", type=Path, required=True)
    hsa_durability_demo = sub.add_parser("hsa-durability-horizon-demo",
                                         help="how long does \"durable response\" mean for a given "
                                              "HSA combination -- sweeps 1/2/5/10-year horizons")
    hsa_durability_demo.add_argument("--ebat-max-kill", type=float, default=0.05)
    hsa_durability_demo.add_argument("--vaccine-max-kill", type=float, default=0.0)
    hsa_durability_demo.add_argument("--no-inhibitor", action="store_true",
                                     help="test vaccine (+/- eBAT) with no PI3K/mTOR inhibitor at all")
    hsa_durability_demo.add_argument("--trials", type=int, default=300)
    hsa_durability_demo.add_argument("--preexisting-prob", type=float, default=HSA_PREEXISTING_PROB_CENTRAL)
    hsa_durability_demo.add_argument("--ebat-exposure-duration-days", type=int,
                                     default=HSA_EBAT_EXPOSURE_DURATION_DAYS)
    hsa_durability_demo.add_argument("--seed", type=int, default=7)
    hsa_durability_demo.add_argument("--out", type=Path, required=True)
    cdk46_feas = sub.add_parser("cdk46-achievability-demo",
                                help="is the second-drug potency the resistance model needs "
                                     "pharmacologically reachable by a real CDK4/6 inhibitor?")
    cdk46_feas.add_argument("--breed", choices=["bmd", "flat_coated_retriever"], default="bmd")
    cdk46_feas.add_argument("--target-max-kill", type=float, default=0.08)
    cdk46_feas.add_argument("--location-penetration-multiplier", type=float, default=1.0)
    cdk46_feas.add_argument("--out", type=Path, required=True)
    endurance_answer = sub.add_parser("endurance-answer-demo",
                                  help="the culminating question: is a durable response achievable "
                                       "for one dog, with everything this repo established")
    endurance_answer.add_argument("--debulking-fraction", type=float, default=DEBULKING_FRACTION)
    endurance_answer.add_argument("--ccnu-max-kill", type=float, default=0.08)
    endurance_answer.add_argument("--trials", type=int, default=250)
    endurance_answer.add_argument("--seed", type=int, default=7)
    endurance_answer.add_argument("--out", type=Path, required=True)
    antigen_conv = sub.add_parser("antigen-convergence-demo",
                                  help="re-runs the three-component regimen with the vaccine ON: "
                                       "every drug-resistance route keeps the driver antigen, so a "
                                       "hotspot vaccine covers all of them")
    antigen_conv.add_argument("--breed", choices=["bmd", "flat_coated_retriever"], default="bmd")
    antigen_conv.add_argument("--debulking-fraction", type=float, default=DEBULKING_FRACTION)
    antigen_conv.add_argument("--ccnu-max-kill", type=float, default=0.08)
    antigen_conv.add_argument("--trials", type=int, default=400)
    antigen_conv.add_argument("--preexisting-prob", type=float, default=0.30)
    antigen_conv.add_argument("--seed", type=int, default=7)
    antigen_conv.add_argument("--out", type=Path, required=True)
    mut_supply = sub.add_parser("mutational-supply-demo",
                                help="does a low-mutation-burden tumor endure better in this model, "
                                     "and which parameter actually carries the effect?")
    mut_supply.add_argument("--breed", choices=["bmd", "flat_coated_retriever"], default="bmd")
    mut_supply.add_argument("--debulking-fraction", type=float, default=DEBULKING_FRACTION)
    mut_supply.add_argument("--ccnu-max-kill", type=float, default=0.08)
    mut_supply.add_argument("--horizon-days", type=int, default=730)
    mut_supply.add_argument("--trials", type=int, default=400)
    mut_supply.add_argument("--preexisting-prob", type=float, default=0.30)
    mut_supply.add_argument("--seed", type=int, default=7)
    mut_supply.add_argument("--out", type=Path, required=True)
    single_patient = sub.add_parser("single-patient-demo",
                                    help="N=1 reframing: what sequencing one dog's tumor resolves, "
                                         "plus lomustine (real, cytotoxic, CNS-penetrant) as the "
                                         "second agent instead of a CDK4/6 inhibitor")
    single_patient.add_argument("--breed", choices=["bmd", "flat_coated_retriever"], default="bmd")
    single_patient.add_argument("--debulking-fraction", type=float, default=DEBULKING_FRACTION)
    single_patient.add_argument("--horizon-days", type=int, default=730)
    single_patient.add_argument("--trials", type=int, default=500)
    single_patient.add_argument("--preexisting-prob", type=float, default=0.30)
    single_patient.add_argument("--seed", type=int, default=7)
    single_patient.add_argument("--out", type=Path, required=True)
    driver_hypothesis = sub.add_parser("driver-hypothesis-demo",
                                  help="structural/DSP triage of candidate driver genes for "
                                       "localized primary CNS / pulmonary histiocytic sarcoma")
    driver_hypothesis.add_argument("--genes", nargs="+", default=None)
    driver_hypothesis.add_argument("--bicoherence-nperseg", type=int, default=64)
    driver_hypothesis.add_argument("--permutations", type=int, default=10000)
    driver_hypothesis.add_argument("--seed", type=int, default=7)
    driver_hypothesis.add_argument("--out", type=Path, required=True)
    mapk_structure = sub.add_parser("mapk-structure-compare",
                                    help="compare human vs. dog AlphaFold confidence at MAPK-gene hotspots")
    mapk_structure.add_argument("--gene", required=True)
    mapk_structure.add_argument("--hotspots", type=int, nargs="+", required=True)
    mapk_structure.add_argument("--out", type=Path, required=True)
    mapk_cns = sub.add_parser("mapk-cns-demo",
                              help="extrapolated primary CNS histiocytic sarcoma MAPK-inhibitor scenarios")
    mapk_cns.add_argument("--breed", choices=["bmd", "flat_coated_retriever"], default="bmd")
    mapk_cns.add_argument("--trials", type=int, default=300)
    mapk_cns.add_argument("--horizon-days", type=int, default=730)
    mapk_cns.add_argument("--preexisting-prob", type=float, default=MAPK_PREEXISTING_PROB_CENTRAL)
    mapk_cns.add_argument("--location-penetration-multiplier", type=float, default=1.0)
    mapk_cns.add_argument("--seed", type=int, default=7)
    mapk_cns.add_argument("--out", type=Path, required=True)
    mapk_local = sub.add_parser("mapk-localized-control-demo",
                                help="local debulking x adjuvant trametinib for primary CNS HS")
    mapk_local.add_argument("--breed", choices=["bmd", "flat_coated_retriever"], default="bmd")
    mapk_local.add_argument("--debulking-fraction", type=float, default=0.97)
    mapk_local.add_argument("--trials", type=int, default=300)
    mapk_local.add_argument("--horizon-days", type=int, default=730)
    mapk_local.add_argument("--preexisting-prob", type=float, default=MAPK_PREEXISTING_PROB_CENTRAL)
    mapk_local.add_argument("--location-penetration-multiplier", type=float, default=1.0)
    mapk_local.add_argument("--seed", type=int, default=7)
    mapk_local.add_argument("--out", type=Path, required=True)
    mapk_combo = sub.add_parser("mapk-combination-demo",
                                help="trametinib +/- swept-potency CDK4/6 inhibitor, debulked CNS context")
    mapk_combo.add_argument("--breed", choices=["bmd", "flat_coated_retriever"], default="bmd")
    mapk_combo.add_argument("--debulking-fraction", type=float, default=0.97)
    mapk_combo.add_argument("--trials", type=int, default=300)
    mapk_combo.add_argument("--horizon-days", type=int, default=730)
    mapk_combo.add_argument("--preexisting-prob", type=float, default=MAPK_PREEXISTING_PROB_CENTRAL)
    mapk_combo.add_argument("--location-penetration-multiplier", type=float, default=1.0)
    mapk_combo.add_argument("--seed", type=int, default=7)
    mapk_combo.add_argument("--out", type=Path, required=True)
    mapk_tox = sub.add_parser("mapk-combination-toxicity-demo",
                              help="stress-test the combination benefit against combined-dose de-rating")
    mapk_tox.add_argument("--breed", choices=["bmd", "flat_coated_retriever"], default="bmd")
    mapk_tox.add_argument("--debulking-fraction", type=float, default=0.97)
    mapk_tox.add_argument("--max-kill-2", type=float, default=0.05)
    mapk_tox.add_argument("--trials", type=int, default=300)
    mapk_tox.add_argument("--horizon-days", type=int, default=730)
    mapk_tox.add_argument("--preexisting-prob", type=float, default=MAPK_PREEXISTING_PROB_CENTRAL)
    mapk_tox.add_argument("--location-penetration-multiplier", type=float, default=1.0)
    mapk_tox.add_argument("--seed", type=int, default=7)
    mapk_tox.add_argument("--out", type=Path, required=True)
    mapk_durability = sub.add_parser("mapk-durability-horizon-demo",
                                     help="how does durable-response probability change with years of follow-up?")
    mapk_durability.add_argument("--breed", choices=["bmd", "flat_coated_retriever"], default="bmd")
    mapk_durability.add_argument("--debulking-fraction", type=float, default=0.97)
    mapk_durability.add_argument("--max-kill-2", type=float, default=0.05)
    mapk_durability.add_argument("--trials", type=int, default=300)
    mapk_durability.add_argument("--preexisting-prob", type=float, default=MAPK_PREEXISTING_PROB_CENTRAL)
    mapk_durability.add_argument("--location-penetration-multiplier", type=float, default=1.0)
    mapk_durability.add_argument("--seed", type=int, default=7)
    mapk_durability.add_argument("--out", type=Path, required=True)
    mapk_vaccine = sub.add_parser("mapk-vaccine-followon-demo",
                                  help="does a follow-on mRNA vaccine close the long-horizon durability gap?")
    mapk_vaccine.add_argument("--breed", choices=["bmd", "flat_coated_retriever"], default="bmd")
    mapk_vaccine.add_argument("--debulking-fraction", type=float, default=0.97)
    mapk_vaccine.add_argument("--cdk46-max-kill", type=float, default=0.05)
    mapk_vaccine.add_argument("--trials", type=int, default=300)
    mapk_vaccine.add_argument("--horizon-days", type=int, default=1825)
    mapk_vaccine.add_argument("--preexisting-prob", type=float, default=MAPK_PREEXISTING_PROB_CENTRAL)
    mapk_vaccine.add_argument("--location-penetration-multiplier", type=float, default=1.0)
    mapk_vaccine.add_argument("--seed", type=int, default=7)
    mapk_vaccine.add_argument("--out", type=Path, required=True)
    mapk_single = sub.add_parser("mapk-single-patient-feasibility-demo",
                                 help="feasibility of curing one specific dog: between-dog vs. "
                                      "within-dog uncertainty, and a worst/best-case bracket")
    mapk_single.add_argument("--breed", choices=["bmd", "flat_coated_retriever"], default="bmd")
    mapk_single.add_argument("--debulking-fraction", type=float, default=0.97)
    mapk_single.add_argument("--cdk46-max-kill", type=float, default=0.05)
    mapk_single.add_argument("--horizon-days", type=int, default=1825)
    mapk_single.add_argument("--n-dogs", type=int, default=40)
    mapk_single.add_argument("--repeats-per-dog", type=int, default=60)
    mapk_single.add_argument("--preexisting-prob", type=float, default=MAPK_PREEXISTING_PROB_CENTRAL)
    mapk_single.add_argument("--location-penetration-multiplier", type=float, default=1.0)
    mapk_single.add_argument("--seed", type=int, default=7)
    mapk_single.add_argument("--out", type=Path, required=True)
    mapk_epitope = sub.add_parser("mapk-vaccine-epitope-binding-demo",
                                  help="check candidate vaccine peptides against real, "
                                       "published canine DLA-I alleles via the live IEDB API")
    mapk_epitope.add_argument("--out", type=Path, required=True)
    mapk_pulmonary = sub.add_parser("mapk-pulmonary-two-compartment-demo",
                                    help="localized pulmonary HS: does undetected regional "
                                         "nodal disease erase the surgery benefit?")
    mapk_pulmonary.add_argument("--cdk46-max-kill", type=float, default=0.0)
    mapk_pulmonary.add_argument("--debulking-fraction", type=float, default=0.97)
    mapk_pulmonary.add_argument("--trials", type=int, default=300)
    mapk_pulmonary.add_argument("--horizon-days", type=int, default=730)
    mapk_pulmonary.add_argument("--preexisting-prob", type=float, default=MAPK_PREEXISTING_PROB_CENTRAL)
    mapk_pulmonary.add_argument("--seed", type=int, default=7)
    mapk_pulmonary.add_argument("--out", type=Path, required=True)
    lym_res = sub.add_parser("lymphoma-resistance-demo",
                             help="CHOP-only chemoresistance model for canine multicentric "
                                  "lymphoma: the durability bar (set by P-glycoprotein efflux) and "
                                  "durable-response sensitivity to pre-existing resistance")
    lym_res.add_argument("--immunophenotype", choices=["B", "T"], default="B")
    lym_res.add_argument("--trials", type=int, default=300)
    lym_res.add_argument("--horizon-days", type=int, default=730)
    lym_res.add_argument("--seed", type=int, default=7)
    lym_res.add_argument("--out", type=Path, required=True)
    lym_immuno = sub.add_parser("lymphoma-immunotherapy-demo",
                                help="CHOP + a swept-potency CD20-directed immune effector for "
                                     "canine lymphoma; where the durability threshold sits and "
                                     "how CD20 antigen loss behaves")
    lym_immuno.add_argument("--immunophenotype", choices=["B", "T"], default="B")
    lym_immuno.add_argument("--rab-max-kill", type=float, default=0.0,
                            help="optional mechanism-agnostic rabacfosadine second node")
    lym_immuno.add_argument("--trials", type=int, default=300)
    lym_immuno.add_argument("--horizon-days", type=int, default=730)
    lym_immuno.add_argument("--seed", type=int, default=7)
    lym_immuno.add_argument("--out", type=Path, required=True)
    lym_sanct = sub.add_parser("lymphoma-sanctuary-demo",
                               help="the CNS sanctuary: two-compartment model with swept drug "
                                    "penetration, chemo-only vs. chemo + a systemic CD20 effector")
    lym_sanct.add_argument("--immunotherapy-max-kill", type=float, default=0.09)
    lym_sanct.add_argument("--trials", type=int, default=300)
    lym_sanct.add_argument("--horizon-days", type=int, default=1825)
    lym_sanct.add_argument("--nodal-involvement-prob", type=float, default=0.30)
    lym_sanct.add_argument("--seed", type=int, default=7)
    lym_sanct.add_argument("--out", type=Path, required=True)
    lym_horizon = sub.add_parser("lymphoma-durability-horizon-demo",
                                 help="how long is durable? CHOP + CD20 effector out to 1/2/5/10 "
                                      "years, the horizon at which cure/10-year durability is tested")
    lym_horizon.add_argument("--immunotherapy-max-kill", type=float, default=0.09)
    lym_horizon.add_argument("--immunophenotype", choices=["B", "T"], default="B")
    lym_horizon.add_argument("--trials", type=int, default=300)
    lym_horizon.add_argument("--seed", type=int, default=7)
    lym_horizon.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "demo":
        rng = np.random.default_rng(42)
        motif = "ATGCGT"; sequence = (motif * 1000) + "".join(rng.choice(list("ACGT"), 6000))
        analyze(sequence, args.out, 100)
    elif args.command == "analyze":
        contig, sequence = read_first_fasta(args.fasta)
        positions = read_vcf_positions(args.vcf, contig) if args.vcf else None
        analyze(sequence, args.out, args.window, positions)
    elif args.command == "volterra-fit":
        run_volterra(args.table, args.out, args.inputs, args.target, args.group, args.exposure,
                     args.memory, args.basis, args.order, args.family, args.alpha, args.l1_ratio)
    elif args.command == "volterra-demo":
        table = args.out / "synthetic_tracks.csv"
        synthetic_table(table)
        run_volterra(table, args.out, ["gc", "repeat"], "variant_count", "chromosome",
                     "callable_bases", 7, 3, 2, "poisson", .001, .5)
    elif args.command == "prepare-gse9794":
        prepare_gse9794(args.matrix, args.out, args.modules)
    elif args.command == "prepare-dog10k-aging":
        prepare_dog10k_aging(args.expression, args.information, args.out, args.modules)
    elif args.command == "inverse-demo":
        inverse_demo(args.out, args.scenarios, args.maxiter)
    elif args.command == "immunotherapy-demo":
        immunotherapy_demo(args.out, args.scenarios, args.maxiter)
    elif args.command == "stochastic-immunotherapy-demo":
        stochastic_immunotherapy_demo(args.out, args.draws, args.particles,
                                      args.maxiter, args.seed)
    elif args.command == "immunotherapy-policy-benchmark":
        policy_superiority_benchmark(args.out, args.draws, args.scenarios,
                                     args.maxiter, args.seed, args.reference_schedule)
    elif args.command == "evaluate-logged-policy":
        evaluate_logged_policy_file(args.table, args.out, args.gamma, args.cross_fitted)
    elif args.command == "melanoma-neoadjuvant-benchmark":
        run_melanoma_benchmark(args.out, args.anchors, args.draws, args.candidates, args.seed)
    elif args.command == "prepare-gse76127":
        prepare_gse76127(args.matrix, args.supplements, args.out, args.components)
    elif args.command == "osteosarcoma-rna-design":
        matrix = None if args.skip_real_data else args.gse76127_matrix
        supplements = None if args.skip_real_data else args.gse76127_supplements
        run_osteosarcoma_benchmark(
            out=args.out,
            anchors=args.anchors,
            candidate_file=args.candidates,
            design_spec_file=args.design_spec,
            gse76127_matrix=matrix,
            gse76127_supplements=supplements,
            draws=args.draws,
            seed=args.seed,
        )
    elif args.command == "evaluate-gse190001":
        run_gse190001(args.prime, args.boost, args.soft, args.out)
    elif args.command == "evaluate-gse102459":
        run_gse102459(args.matrix, args.out, args.modules)
    elif args.command == "alphafold-fetch":
        fetch_structure(args.uniprot, args.out)
    elif args.command == "alphafold-analyze":
        analyze_structure(args.struct, args.out, args.variants, args.flank)
    elif args.command == "mapk-resistance-demo":
        mapk_resistance_demo(args.out, args.species, args.trials, args.horizon_days, args.seed)
    elif args.command == "hsa-resistance-demo":
        hsa_resistance_demo(args.out, args.trials, args.horizon_days, args.seed)
    elif args.command == "hsa-combination-control-demo":
        hsa_combination_control_demo(args.out, args.trials, args.horizon_days,
                                     args.preexisting_prob,
                                     ebat_exposure_duration_days=args.ebat_exposure_duration_days,
                                     seed=args.seed)
    elif args.command == "hsa-vaccine-followon-demo":
        hsa_vaccine_followon_demo(args.out, args.ebat_max_kill, not args.no_inhibitor,
                                  args.horizon_days, args.trials, args.preexisting_prob,
                                  ebat_exposure_duration_days=args.ebat_exposure_duration_days,
                                  seed=args.seed)
    elif args.command == "hsa-combination-search-demo":
        hsa_combination_search_demo(args.out, args.trials, args.horizon_days,
                                    args.preexisting_prob,
                                    ebat_exposure_duration_days=args.ebat_exposure_duration_days,
                                    seed=args.seed)
    elif args.command == "hsa-receptor-conservation-demo":
        if args.genes is None:
            hsa_receptor_conservation_demo(args.out)
        else:
            hsa_receptor_conservation_demo(args.out, args.genes)
    elif args.command == "hsa-vaccine-antigen-design-demo":
        hsa_vaccine_antigen_design_demo(args.out, args.gene, args.window, args.top_n)
    elif args.command == "hsa-combination-toxicity-demo":
        hsa_combination_toxicity_demo(args.out, args.ebat_max_kill, args.trials, args.horizon_days,
                                      args.preexisting_prob,
                                      ebat_exposure_duration_days=args.ebat_exposure_duration_days,
                                      seed=args.seed)
    elif args.command == "hsa-durability-horizon-demo":
        hsa_durability_horizon_demo(args.out, args.ebat_max_kill, args.vaccine_max_kill,
                                    not args.no_inhibitor, args.trials, args.preexisting_prob,
                                    ebat_exposure_duration_days=args.ebat_exposure_duration_days,
                                    seed=args.seed)
    elif args.command == "cdk46-achievability-demo":
        cdk46_achievability_demo(args.out, args.breed, target_max_kill=args.target_max_kill,
                                 location_penetration_multiplier=args.location_penetration_multiplier)
    elif args.command == "endurance-answer-demo":
        endurance_answer_demo(args.out, args.debulking_fraction, args.ccnu_max_kill, args.trials,
                          args.seed)
    elif args.command == "antigen-convergence-demo":
        antigen_convergence_demo(args.out, args.breed, args.debulking_fraction, args.ccnu_max_kill,
                                 args.trials, args.preexisting_prob, args.seed)
    elif args.command == "mutational-supply-demo":
        mutational_supply_demo(args.out, args.breed, args.debulking_fraction, args.ccnu_max_kill,
                               args.horizon_days, args.trials, args.preexisting_prob, args.seed)
    elif args.command == "single-patient-demo":
        single_patient_demo(args.out, args.breed, args.debulking_fraction, args.horizon_days,
                            args.trials, args.preexisting_prob, args.seed)
    elif args.command == "driver-hypothesis-demo":
        driver_hypothesis_demo(args.out, args.genes, args.bicoherence_nperseg,
                                     args.permutations, args.seed)
    elif args.command == "mapk-structure-compare":
        compare_orthologs(args.gene, args.hotspots, args.out)
    elif args.command == "mapk-cns-demo":
        mapk_cns_demo(args.out, args.breed, args.trials, args.horizon_days,
                     args.preexisting_prob, args.location_penetration_multiplier, args.seed)
    elif args.command == "mapk-localized-control-demo":
        localized_control_demo(args.out, args.breed, args.debulking_fraction, args.trials,
                               args.horizon_days, args.preexisting_prob,
                               args.location_penetration_multiplier, args.seed)
    elif args.command == "mapk-combination-demo":
        combination_control_demo(args.out, args.breed, args.debulking_fraction, args.trials,
                                 args.horizon_days, args.preexisting_prob,
                                 args.location_penetration_multiplier, args.seed)
    elif args.command == "mapk-combination-toxicity-demo":
        combination_toxicity_demo(args.out, args.breed, args.debulking_fraction, args.max_kill_2,
                                  args.trials, args.horizon_days, args.preexisting_prob,
                                  args.location_penetration_multiplier, args.seed)
    elif args.command == "mapk-durability-horizon-demo":
        durability_horizon_demo(args.out, args.breed, args.debulking_fraction, args.max_kill_2,
                                args.trials, args.preexisting_prob,
                                args.location_penetration_multiplier, args.seed)
    elif args.command == "mapk-vaccine-followon-demo":
        vaccine_followon_demo(args.out, args.breed, args.debulking_fraction, args.cdk46_max_kill,
                              args.trials, args.horizon_days, args.preexisting_prob,
                              args.location_penetration_multiplier, args.seed)
    elif args.command == "mapk-single-patient-feasibility-demo":
        single_patient_feasibility_demo(args.out, args.breed, args.debulking_fraction,
                                        args.cdk46_max_kill, args.horizon_days, args.n_dogs,
                                        args.repeats_per_dog, args.preexisting_prob,
                                        args.location_penetration_multiplier, args.seed)
    elif args.command == "mapk-vaccine-epitope-binding-demo":
        vaccine_epitope_binding_demo(args.out)
    elif args.command == "lymphoma-resistance-demo":
        lymphoma_resistance_demo(args.out, args.immunophenotype, args.trials, args.horizon_days,
                                 args.seed)
    elif args.command == "lymphoma-immunotherapy-demo":
        lymphoma_immunotherapy_demo(args.out, args.immunophenotype, args.rab_max_kill, args.trials,
                                    args.horizon_days, args.seed)
    elif args.command == "lymphoma-sanctuary-demo":
        lymphoma_sanctuary_demo(args.out, args.immunotherapy_max_kill, args.trials,
                                args.horizon_days, args.nodal_involvement_prob, args.seed)
    elif args.command == "lymphoma-durability-horizon-demo":
        lymphoma_durability_horizon_demo(args.out, args.immunotherapy_max_kill,
                                         args.immunophenotype, args.trials, args.seed)
    else:
        pulmonary_two_compartment_demo(args.out, args.cdk46_max_kill, args.debulking_fraction,
                                       args.trials, args.horizon_days, args.preexisting_prob,
                                       args.seed)


if __name__ == "__main__":
    main()
