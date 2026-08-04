import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .alphafold_cli import analyze_structure, fetch_structure
from .hsa_cli import hsa_resistance_demo, hsa_vaccine_followon_demo
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
from .signals import eiip, variant_density, windowed_gc
from .spectral import coherence, multitaper_psd, spectral_entropy, welch_psd
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
    hsa_vaccine_demo = sub.add_parser("hsa-vaccine-followon-demo",
                                      help="PI3K/mTOR inhibitor plus a real-vaccine-inspired "
                                           "follow-on for canine hemangiosarcoma")
    hsa_vaccine_demo.add_argument("--trials", type=int, default=300)
    hsa_vaccine_demo.add_argument("--horizon-days", type=int, default=730)
    hsa_vaccine_demo.add_argument("--preexisting-prob", type=float, default=0.30)
    hsa_vaccine_demo.add_argument("--seed", type=int, default=7)
    hsa_vaccine_demo.add_argument("--out", type=Path, required=True)
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
    mapk_cns.add_argument("--preexisting-prob", type=float, default=0.30)
    mapk_cns.add_argument("--location-penetration-multiplier", type=float, default=1.0)
    mapk_cns.add_argument("--seed", type=int, default=7)
    mapk_cns.add_argument("--out", type=Path, required=True)
    mapk_local = sub.add_parser("mapk-localized-control-demo",
                                help="local debulking x adjuvant trametinib for primary CNS HS")
    mapk_local.add_argument("--breed", choices=["bmd", "flat_coated_retriever"], default="bmd")
    mapk_local.add_argument("--debulking-fraction", type=float, default=0.97)
    mapk_local.add_argument("--trials", type=int, default=300)
    mapk_local.add_argument("--horizon-days", type=int, default=730)
    mapk_local.add_argument("--preexisting-prob", type=float, default=0.30)
    mapk_local.add_argument("--location-penetration-multiplier", type=float, default=1.0)
    mapk_local.add_argument("--seed", type=int, default=7)
    mapk_local.add_argument("--out", type=Path, required=True)
    mapk_combo = sub.add_parser("mapk-combination-demo",
                                help="trametinib +/- swept-potency CDK4/6 inhibitor, debulked CNS context")
    mapk_combo.add_argument("--breed", choices=["bmd", "flat_coated_retriever"], default="bmd")
    mapk_combo.add_argument("--debulking-fraction", type=float, default=0.97)
    mapk_combo.add_argument("--trials", type=int, default=300)
    mapk_combo.add_argument("--horizon-days", type=int, default=730)
    mapk_combo.add_argument("--preexisting-prob", type=float, default=0.30)
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
    mapk_tox.add_argument("--preexisting-prob", type=float, default=0.30)
    mapk_tox.add_argument("--location-penetration-multiplier", type=float, default=1.0)
    mapk_tox.add_argument("--seed", type=int, default=7)
    mapk_tox.add_argument("--out", type=Path, required=True)
    mapk_durability = sub.add_parser("mapk-durability-horizon-demo",
                                     help="how does durable-response probability change with years of follow-up?")
    mapk_durability.add_argument("--breed", choices=["bmd", "flat_coated_retriever"], default="bmd")
    mapk_durability.add_argument("--debulking-fraction", type=float, default=0.97)
    mapk_durability.add_argument("--max-kill-2", type=float, default=0.05)
    mapk_durability.add_argument("--trials", type=int, default=300)
    mapk_durability.add_argument("--preexisting-prob", type=float, default=0.30)
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
    mapk_vaccine.add_argument("--preexisting-prob", type=float, default=0.30)
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
    mapk_single.add_argument("--preexisting-prob", type=float, default=0.30)
    mapk_single.add_argument("--location-penetration-multiplier", type=float, default=1.0)
    mapk_single.add_argument("--seed", type=int, default=7)
    mapk_single.add_argument("--out", type=Path, required=True)
    mapk_epitope = sub.add_parser("mapk-vaccine-epitope-binding-demo",
                                  help="check candidate vaccine peptides against real, "
                                       "published canine DLA-I alleles via the live IEDB API")
    mapk_epitope.add_argument("--out", type=Path, required=True)
    mapk_pulmonary = sub.add_parser("mapk-pulmonary-two-compartment-demo",
                                    help="localized pulmonary Corgi HS: does undetected regional "
                                         "nodal disease erase the surgery benefit?")
    mapk_pulmonary.add_argument("--cdk46-max-kill", type=float, default=0.0)
    mapk_pulmonary.add_argument("--debulking-fraction", type=float, default=0.97)
    mapk_pulmonary.add_argument("--trials", type=int, default=300)
    mapk_pulmonary.add_argument("--horizon-days", type=int, default=730)
    mapk_pulmonary.add_argument("--preexisting-prob", type=float, default=0.30)
    mapk_pulmonary.add_argument("--seed", type=int, default=7)
    mapk_pulmonary.add_argument("--out", type=Path, required=True)
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
    elif args.command == "hsa-vaccine-followon-demo":
        hsa_vaccine_followon_demo(args.out, args.horizon_days, args.trials,
                                  args.preexisting_prob, args.seed)
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
    else:
        pulmonary_two_compartment_demo(args.out, args.cdk46_max_kill, args.debulking_fraction,
                                       args.trials, args.horizon_days, args.preexisting_prob,
                                       args.seed)


if __name__ == "__main__":
    main()
