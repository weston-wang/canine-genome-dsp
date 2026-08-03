"""Reusable visualizations for the osteosarcoma RNA-vaccine program."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch


STATE_COLORS = (
    "#4c78a8", "#f2cf5b", "#54a24b", "#eeca3b", "#e45756", "#b279a2",
)


def plot_state_posteriors(time: np.ndarray, posterior: np.ndarray,
                          state_names: list[str] | tuple[str, ...], out: str | Path,
                          treatment_days: list[int] | None = None,
                          title: str = (
                              "Illustrative simulated dog: filtered hidden-state probabilities"
                          )) -> None:
    """Plot state probabilities with optional treatment impulses."""
    time = np.asarray(time, float); posterior = np.asarray(posterior, float)
    if posterior.shape != (len(time), len(state_names)):
        raise ValueError("posterior must be time by state")
    fig, ax = plt.subplots(figsize=(11, 5.5))
    ax.stackplot(time, posterior.T, labels=state_names,
                 colors=STATE_COLORS[:len(state_names)], alpha=.88)
    for index, day in enumerate(treatment_days or []):
        ax.axvline(day, color="black", linewidth=.8, linestyle="--",
                   label="vaccine input" if index == 0 else None)
    ax.set(xlabel="Days from surgery/model origin", ylabel="Posterior probability",
           ylim=(0, 1), title=title)
    ax.legend(loc="upper center", bbox_to_anchor=(.5, -0.16), ncol=3, fontsize=8)
    fig.tight_layout(); fig.savefig(out, dpi=170, bbox_inches="tight"); plt.close(fig)


def plot_volterra_memory(first_order: np.ndarray, second_order: np.ndarray,
                         channel_names: list[str] | tuple[str, ...], out: str | Path,
                         title: str = (
                             "Bundled illustrative Volterra transition-memory prior"
                         )) -> None:
    """Plot channel impulse memories and one low-rank second-order interaction surface."""
    first_order = np.asarray(first_order, float); second_order = np.asarray(second_order, float)
    if first_order.ndim != 2 or first_order.shape[0] != len(channel_names):
        raise ValueError("first_order must be channel by lag")
    if second_order.ndim != 2 or second_order.shape[0] != second_order.shape[1]:
        raise ValueError("second_order must be a square lag surface")
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    for index, name in enumerate(channel_names):
        axes[0].plot(np.arange(first_order.shape[1]), first_order[index], marker="o",
                     markersize=3, label=name)
    axes[0].axhline(0, color="black", linewidth=.7)
    axes[0].set(xlabel="Lag (model time steps)", ylabel="Transition-logit contribution",
                title="First-order memory")
    axes[0].legend(fontsize=8)
    image = axes[1].imshow(second_order, origin="lower", aspect="auto", cmap="coolwarm")
    axes[1].set(xlabel="Second input lag", ylabel="First input lag",
                title="Low-rank second-order interaction")
    fig.colorbar(image, ax=axes[1], shrink=.82, label="Interaction contribution")
    fig.suptitle(title); fig.tight_layout(); fig.savefig(out, dpi=170); plt.close(fig)


def plot_cargo_selection(ranking: pd.DataFrame, out: str | Path,
                         score_column: str = "robust_score",
                         selected_column: str = "selected") -> None:
    """Plot robust antigen scores while making selected versus rejected cargo explicit."""
    required = {"candidate_id", score_column, selected_column}
    if not required.issubset(ranking.columns):
        raise ValueError(f"cargo ranking requires {sorted(required)}")
    table = ranking.sort_values(score_column).copy()
    colors = np.where(table[selected_column].astype(bool), "#54a24b", "#bab0ac")
    fig, ax = plt.subplots(figsize=(9, max(4, .31 * len(table))))
    ax.barh(table.candidate_id.astype(str), table[score_column].astype(float), color=colors)
    ax.axvline(0, color="black", linewidth=.7)
    ax.set(xlabel="Robust research score (unitless)", ylabel="Candidate",
           title="Multivalent RNA cargo research ranking")
    ax.text(.99, .01, "Green = selected; not a patient recommendation", transform=ax.transAxes,
            ha="right", va="bottom", fontsize=8, color="#555555")
    fig.tight_layout(); fig.savefig(out, dpi=170); plt.close(fig)


def plot_real_data_predictions(predictions: pd.DataFrame, out: str | Path) -> None:
    """Plot held-out GSE76127 DFI predictions against observed outcomes."""
    required = {"dfi_days", "predicted_dfi_days", "training_median_dfi_days"}
    if not required.issubset(predictions.columns):
        raise ValueError(f"prediction table requires {sorted(required)}")
    observed = predictions.dfi_days.to_numpy(float)
    fitted = predictions.predicted_dfi_days.to_numpy(float)
    baseline = predictions.training_median_dfi_days.to_numpy(float)
    limit = max(observed.max(), fitted.max(), baseline.max()) * 1.05
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    axes[0].scatter(observed, fitted, color="#4c78a8", alpha=.8, label="expression/PCA/ridge")
    axes[0].plot([0, limit], [0, limit], color="black", linestyle="--", linewidth=.8)
    axes[0].set(xlabel="Observed DFI (days)", ylabel="Held-out predicted DFI (days)",
                xlim=(0, limit), ylim=(0, limit), title="One dog held out per fold")
    ordered = np.argsort(observed)
    axes[1].plot(observed[ordered], color="black", marker="o", markersize=3,
                 label="observed")
    axes[1].plot(fitted[ordered], color="#4c78a8", label="expression prediction")
    axes[1].plot(baseline[ordered], color="#f58518", linestyle="--",
                 label="training median")
    axes[1].set(xlabel="Dogs ordered by observed DFI", ylabel="DFI (days)",
                title="Static tumor-expression baseline")
    axes[1].legend(fontsize=8)
    fig.tight_layout(); fig.savefig(out, dpi=170); plt.close(fig)


def plot_clinical_anchors(anchors: pd.DataFrame, out: str | Path) -> None:
    """Separate current care, non-RNA analogs, and human landmarks visually."""
    required = {
        "record_id", "species", "study", "arm", "endpoint", "estimate", "unit",
        "design", "intervention_class",
    }
    if not required.issubset(anchors.columns):
        raise ValueError(f"clinical anchors require {sorted(required)}")
    table = anchors.copy()
    table["estimate"] = pd.to_numeric(table.estimate, errors="coerce")
    table["ci_low"] = pd.to_numeric(table.get("ci_low"), errors="coerce")
    table["ci_high"] = pd.to_numeric(table.get("ci_high"), errors="coerce")
    time_endpoints = {
        "median_dfi", "median_os", "median_pfs", "median_disease_free_interval",
        "median_overall_survival", "median_progression_free_survival",
    }
    days = table.loc[
        table.species.eq("dog") & table.unit.eq("days") & table.estimate.notna()
        & table.endpoint.isin(time_endpoints)
    ].copy()
    landmarks = table.loc[
        table.unit.eq("percent")
        & table.estimate.notna()
        & table.endpoint.str.contains("landmark", case=False, na=False)
    ].copy()
    current = days.loc[days.intervention_class.eq("current_standard_care")].copy()
    non_rna = days.loc[
        days.intervention_class.astype(str).str.startswith("non_RNA_")
    ].copy()
    if current.empty or non_rna.empty or landmarks.empty:
        raise ValueError("no comparable day-scale clinical anchors")

    endpoint_colors = {
        "median_disease_free_interval": "#4c78a8",
        "median_overall_survival": "#f58518",
        "landmark_event_free_survival_from_surgery": "#4c78a8",
        "landmark_overall_survival_from_surgery": "#f58518",
    }

    def endpoint_label(endpoint: str) -> str:
        return "DFI" if "disease_free" in endpoint else (
            "EFS" if "event_free" in endpoint else "OS"
        )

    def canine_study_label(record_id: str, fallback: str) -> str:
        prefixes = {
            "cotc022_": "COTC022 SOC",
            "cotc021_": "COTC021 + sirolimus",
            "cotc026_": "COTC026 Listeria",
            "cotc030_": "COTC030 IL-15",
            "rt_listeria_2026_": "2026 RT + Listeria",
        }
        return next(
            (label for prefix, label in prefixes.items() if record_id.startswith(prefix)),
            fallback,
        )

    def plot_canine_panel(ax: plt.Axes, frame: pd.DataFrame, title: str) -> None:
        frame = frame.sort_values(["study", "endpoint"]).reset_index(drop=True)
        frame["label"] = frame.apply(
            lambda row: (
                f"{canine_study_label(row.record_id, row.study)}"
                f" | {endpoint_label(row.endpoint)}"
                + (" | palliative setting"
                   if row.record_id == "rt_listeria_2026_median_os" else "")
            ),
            axis=1,
        )
        historical = frame.design.str.contains("historical", case=False, na=False)
        bars = ax.barh(
            frame.label,
            frame.estimate,
            color=[endpoint_colors[value] for value in frame.endpoint],
            edgecolor="#333333",
            linewidth=.5,
        )
        for bar, is_historical in zip(bars, historical, strict=True):
            if is_historical:
                bar.set_hatch("//")
        valid_ci = frame.ci_low.notna() & frame.ci_high.notna()
        if valid_ci.any():
            selected = frame.loc[valid_ci]
            ax.errorbar(
                selected.estimate,
                np.flatnonzero(valid_ci),
                xerr=np.vstack([
                    selected.estimate - selected.ci_low,
                    selected.ci_high - selected.estimate,
                ]),
                fmt="none", ecolor="#222222", capsize=3, linewidth=.8,
            )
        ax.set(xlabel="Published median (days)", ylabel="", title=title)

    landmarks["label"] = landmarks.endpoint.map(endpoint_label)
    landmarks = landmarks.sort_values("endpoint").reset_index(drop=True)
    fig, axes = plt.subplots(
        1, 3,
        figsize=(18, max(5.3, .48 * len(non_rna))),
        gridspec_kw={"width_ratios": [1, 1.65, 1]},
    )
    plot_canine_panel(
        axes[0], current, "Canine current-care arm\n(randomized COTC022)"
    )
    plot_canine_panel(
        axes[1], non_rna, "Completed non-RNA studies\n(mixed designs and settings)"
    )
    axes[0].set_xlim(left=0); axes[1].set_xlim(left=0)
    axes[2].barh(
        landmarks.label,
        landmarks.estimate,
        color=[endpoint_colors[value] for value in landmarks.endpoint],
        edgecolor="#333333",
        linewidth=.5,
    )
    valid_ci = landmarks.ci_low.notna() & landmarks.ci_high.notna()
    if valid_ci.any():
        selected = landmarks.loc[valid_ci]
        axes[2].errorbar(
            selected.estimate,
            np.flatnonzero(valid_ci),
            xerr=np.vstack([
                selected.estimate - selected.ci_low,
                selected.ci_high - selected.estimate,
            ]),
            fmt="none", ecolor="#222222", capsize=3, linewidth=.8,
        )
    axes[2].set(
        xlabel="Five-year outcome (%)", xlim=(0, 100), ylabel="",
        title="Human current-care landmark\n(EURAMOS M0-CSR)",
    )
    fig.legend(
        handles=[
            Patch(facecolor="#4c78a8", label="DFI / EFS"),
            Patch(facecolor="#f58518", label="OS"),
            Patch(facecolor="white", edgecolor="#333333", hatch="//",
                  label="Historical-control design"),
        ],
        loc="lower center", ncol=3, frameon=False,
    )
    fig.suptitle(
        "Published aggregate anchors—panels are not direct efficacy comparisons"
    )
    fig.tight_layout(rect=(0, .08, 1, .95))
    fig.savefig(out, dpi=170, bbox_inches="tight")
    plt.close(fig)
