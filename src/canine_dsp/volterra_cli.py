"""File-oriented fitting and chromosome-held-out evaluation for Volterra models."""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .volterra import (
    dct_lag_basis,
    fit_volterra,
    predict,
    regression_metrics,
    volterra_design,
)


def run_volterra(
    table_path: Path,
    out: Path,
    inputs: list[str],
    target: str,
    group: str,
    exposure_name: str | None,
    memory: int,
    n_basis: int,
    order: int,
    family: str,
    alpha: float,
    l1_ratio: float,
) -> None:
    table = pd.read_csv(table_path)
    required = inputs + [target, group] + ([exposure_name] if exposure_name else [])
    missing = [name for name in required if name not in table]
    if missing:
        raise ValueError(f"missing columns: {missing}")
    if table[required].isna().any().any():
        raise ValueError("model columns contain missing values; impute or remove them explicitly")
    groups = table[group].astype(str).to_numpy()
    x = table[inputs].to_numpy(float)
    y = table[target].to_numpy(float)
    exposure = table[exposure_name].to_numpy(float) if exposure_name else None
    design, names, valid = volterra_design(x, groups, inputs, memory, n_basis, order)
    if len(np.unique(groups[valid])) < 2:
        raise ValueError("chromosome-aware evaluation requires at least two groups")
    basis = dct_lag_basis(memory, n_basis)
    predictions = np.full(len(y), np.nan)
    fold_metrics = []
    for held_out in dict.fromkeys(groups[valid].tolist()):
        test = valid & (groups == held_out)
        train = valid & (groups != held_out)
        fit = fit_volterra(design[train], y[train], names, basis, inputs, order, family,
                           alpha, l1_ratio, exposure[train] if exposure is not None else None)
        predictions[test] = predict(fit, design[test], exposure[test] if exposure is not None else None)
        fold_metrics.append({"held_out_group": held_out, "n_test": int(test.sum()),
                             **regression_metrics(y[test], predictions[test], family)})
    final = fit_volterra(design[valid], y[valid], names, basis, inputs, order, family,
                         alpha, l1_ratio, exposure[valid] if exposure is not None else None)
    h1, h2 = final.reconstruct_kernels()
    out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(fold_metrics).to_csv(out / "held_out_group_metrics.csv", index=False)
    output = table[[group]].copy()
    output["observed"] = y
    output["held_out_prediction"] = predictions
    output.to_csv(out / "predictions.csv", index=False)
    coefficients = pd.DataFrame({"term": names, "coefficient": final.coefficients})
    coefficients["absolute_coefficient"] = coefficients.coefficient.abs()
    coefficients.sort_values("absolute_coefficient", ascending=False).to_csv(
        out / "coefficients.csv", index=False
    )
    np.savez_compressed(out / "kernels.npz", basis=basis, h1=h1,
                        h2=np.array([]) if h2 is None else h2, input_names=np.asarray(inputs))
    overall = regression_metrics(y[valid], predictions[valid], family)
    summary = {"family": family, "order": order, "memory_windows": memory,
               "basis_rank": n_basis, "alpha": alpha, "l1_ratio": l1_ratio,
               "n_rows_used": int(valid.sum()), "n_terms": len(names),
               "nonzero_terms": int(np.count_nonzero(final.coefficients)),
               "held_out_overall": overall}
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    fig, axes = plt.subplots(len(inputs), 1, figsize=(8, max(3, 2.2 * len(inputs))), squeeze=False)
    for channel, name in enumerate(inputs):
        axes[channel, 0].plot(np.arange(memory), h1[channel])
        axes[channel, 0].set(ylabel=name, xlabel="causal lag (windows)")
    fig.suptitle("First-order Volterra kernels"); fig.tight_layout()
    fig.savefig(out / "first_order_kernels.png", dpi=160); plt.close(fig)


def synthetic_table(path: Path, seed: int = 42) -> None:
    """Generate chromosomes with a known quadratic GC/repeat response for a smoke test."""
    rng = np.random.default_rng(seed)
    frames = []
    for chromosome in ["chr1", "chr2", "chr3", "chr4", "chr5"]:
        n = 500
        gc = np.clip(0.42 + np.cumsum(rng.normal(0, .008, n)), .25, .7)
        repeats = np.clip(0.3 + np.cumsum(rng.normal(0, .012, n)), .02, .85)
        callable_bases = rng.integers(8500, 10001, n)
        log_rate = -7.1 + 2.0 * gc + 1.4 * repeats + 3.5 * (gc - .45) * (repeats - .3)
        counts = rng.poisson(callable_bases * np.exp(log_rate))
        frames.append(pd.DataFrame({"chromosome": chromosome, "gc": gc, "repeat": repeats,
                                    "callable_bases": callable_bases, "variant_count": counts}))
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.concat(frames, ignore_index=True).to_csv(path, index=False)

