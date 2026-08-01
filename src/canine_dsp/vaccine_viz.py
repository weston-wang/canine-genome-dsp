"""Reusable visual diagnostics for longitudinal vaccine system identification."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_response_trajectories(predictions: pd.DataFrame, out: Path) -> None:
    modules = predictions["module"].unique()
    fig, axes = plt.subplots(len(modules), 2, figsize=(11, 2.7 * len(modules)),
                             squeeze=False, sharex=True)
    for row, module in enumerate(modules):
        subset = predictions[predictions.module == module]
        for column, phase in enumerate(["prime", "boost"]):
            panel = subset[subset.phase == phase]
            grouped = panel.groupby("day")[["observed", "predicted"]].agg(["mean", "sem"])
            ax = axes[row, column]
            ax.errorbar(grouped.index, grouped[("observed", "mean")],
                        yerr=grouped[("observed", "sem")], marker="o", label="observed")
            ax.plot(grouped.index, grouped[("predicted", "mean")], marker="s", label="LOSO predicted")
            ax.axhline(0, color="gray", linewidth=.7)
            ax.set(title=f"{module}: {phase}", ylabel="baseline-relative module score")
            if row == len(modules) - 1: ax.set_xlabel("study day label")
            if row == 0 and column == 1: ax.legend()
    fig.tight_layout(); fig.savefig(out, dpi=180); plt.close(fig)


def plot_model_comparison(predictions: pd.DataFrame, out: Path) -> None:
    from sklearn.metrics import r2_score
    summary = pd.Series({name: r2_score(group["observed"], group["predicted"])
                         for name, group in predictions.groupby("model")}).sort_values()
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.barh(summary.index, summary.to_numpy(), alpha=.8)
    ax.axvline(0, color="gray", linewidth=.8)
    ax.set(xlabel="pooled leave-one-subject-out R²", title="Model generalization")
    fig.tight_layout(); fig.savefig(out, dpi=180); plt.close(fig)


def plot_residual_heatmap(predictions: pd.DataFrame, out: Path) -> None:
    table = predictions.assign(residual=lambda frame: frame.observed - frame.predicted).pivot_table(
        index=["module", "phase"], columns="day", values="residual", aggfunc="mean")
    limit = np.nanmax(np.abs(table.to_numpy())) or 1
    fig, ax = plt.subplots(figsize=(9, max(3, .7 * len(table))))
    image = ax.imshow(table, aspect="auto", cmap="coolwarm", vmin=-limit, vmax=limit)
    ax.set(yticks=np.arange(len(table)), yticklabels=[f"{a} · {b}" for a, b in table.index],
           xticks=np.arange(len(table.columns)), xticklabels=table.columns,
           xlabel="study day label", title="Mean held-out residual: observed − predicted")
    fig.colorbar(image, ax=ax, label="module-score residual")
    fig.tight_layout(); fig.savefig(out, dpi=180); plt.close(fig)


def plot_sampling_ablation(ablation: pd.DataFrame, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 4))
    for name, group in ablation.groupby("schedule"):
        ax.plot(group["module"], group["r2"], marker="o", label=name)
    ax.axhline(0, color="gray", linewidth=.8)
    ax.set(ylabel="held-out R²", xlabel="module", title="Sampling-schedule sensitivity")
    ax.tick_params(axis="x", rotation=25); ax.legend()
    fig.tight_layout(); fig.savefig(out, dpi=180); plt.close(fig)
