import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .io import read_first_fasta, read_vcf_positions
from .signals import eiip, variant_density, windowed_gc
from .spectral import coherence, multitaper_psd, spectral_entropy, welch_psd
from .wavelets import cwt_power
from .volterra_cli import run_volterra, synthetic_table


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
    else:
        table = args.out / "synthetic_tracks.csv"
        synthetic_table(table)
        run_volterra(table, args.out, ["gc", "repeat"], "variant_count", "chromosome",
                     "callable_bases", 7, 3, 2, "poisson", .001, .5)


if __name__ == "__main__":
    main()
