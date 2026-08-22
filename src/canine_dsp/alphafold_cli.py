import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .alphafold import download_structure, map_variants, read_plddt_track
from .spectral import multitaper_psd, spectral_entropy, welch_psd


def fetch_structure(uniprot_id: str, out: Path) -> None:
    target = download_structure(uniprot_id, out)
    print(f"Wrote {target}")


def analyze_structure(struct: Path, out: Path, variants: Path | None = None, flank: int = 5) -> None:
    out.mkdir(parents=True, exist_ok=True)
    track = read_plddt_track(struct)
    track.to_csv(out / "confidence_track.csv", index=False)
    plddt = track["plddt"].to_numpy()
    fw, pw = welch_psd(plddt)
    fm, pm = multitaper_psd(plddt)
    pd.DataFrame({"frequency_cycles_per_residue": fm, "multitaper_psd": pm}).to_csv(
        out / "confidence_spectrum.csv", index=False)

    fig, axes = plt.subplots(2, 1, figsize=(9, 6))
    axes[0].plot(track["residue_number"], plddt)
    axes[0].axhline(70, color="gray", linestyle="--", linewidth=.8)
    axes[0].set(xlabel="residue number", ylabel="pLDDT", title="Per-residue model confidence")
    axes[1].semilogy(fw[1:], pw[1:] + np.finfo(float).eps, label="Welch")
    axes[1].semilogy(fm[1:], pm[1:] + np.finfo(float).eps, label="Multitaper", alpha=.8)
    axes[1].set(xlabel="cycles / residue", ylabel="PSD", title="pLDDT spectrum")
    axes[1].legend(); fig.tight_layout(); fig.savefig(out / "confidence_spectrum.png", dpi=160)
    plt.close(fig)

    peak = int(np.argmax(pm[1:]) + 1)
    summary = {
        "residues": len(track), "mean_plddt": float(np.mean(plddt)),
        "fraction_confident_ge_70": float(np.mean(plddt >= 70)),
        "spectral_entropy": spectral_entropy(pm),
        "peak_frequency_cycles_per_residue": float(fm[peak]),
        "peak_period_residues": float(1 / fm[peak]) if fm[peak] > 0 else None,
        "note": "AlphaFold pLDDT is a per-residue model-confidence estimate, not a stability or "
                "functional score, and the structure is a single predicted static conformation.",
    }
    if variants is not None:
        variant_table = pd.read_csv(variants)
        mapped = map_variants(track, variant_table, flank)
        mapped.to_csv(out / "variant_confidence.csv", index=False)
        summary["variants"] = len(mapped)
        summary["variants_missing_from_structure"] = int(mapped["confidence_band"].isna().sum())
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
