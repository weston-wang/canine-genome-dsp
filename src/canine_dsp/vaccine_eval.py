"""Real-data evaluation of reduced Volterra vaccine-response models on GSE190001."""

import gzip
import json
import re
from itertools import combinations_with_replacement
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.fft import dct
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GroupKFold

from .vaccine_viz import (
    plot_model_comparison,
    plot_residual_heatmap,
    plot_response_trajectories,
    plot_sampling_ablation,
)
from .expression import pca_modules, read_geo_series_matrix


GENE_MODULES = {
    "interferon": ["ENSG00000185745", "ENSG00000119922", "ENSG00000119917",
                    "ENSG00000187608", "ENSG00000157601", "ENSG00000089127",
                    "ENSG00000111335", "ENSG00000111331", "ENSG00000137959",
                    "ENSG00000134321"],
    "inflammation": ["ENSG00000125538", "ENSG00000232810", "ENSG00000100906",
                     "ENSG00000169245", "ENSG00000108691"],
    "plasmablast": ["ENSG00000170476", "ENSG00000100219", "ENSG00000057657",
                    "ENSG00000132465", "ENSG00000048462"],
}


def read_soft_metadata(path: Path) -> pd.DataFrame:
    """Map featureCounts sample identifiers to subject, phase, and study day."""
    records, current = [], {}
    with gzip.open(path, "rt") as handle:
        for line in handle:
            if line.startswith("^SAMPLE"):
                if current: records.append(current)
                current = {}
            elif line.startswith("!Sample_title"):
                current["title"] = line.split(" = ", 1)[1].strip()
            elif line.startswith("!Sample_description"):
                current["count_id"] = line.split(" = ", 1)[1].strip()
            elif line.startswith("!Sample_characteristics_ch1"):
                value = line.split(" = ", 1)[1].strip()
                if ": " in value:
                    key, item = value.split(": ", 1); current[key] = item
        if current: records.append(current)
    table = pd.DataFrame(records)
    table["subject"] = table["patientid"]
    table["phase"] = table["vaccine_dose"].str.lower()
    # GEO labels D01 as the pre-vaccination/same-day sample (study day 0).
    table["day"] = table["timepoint"].str.extract(r"D(\d+)$")[0].astype(int) - 1
    return table.set_index("count_id")


def read_counts(prime: Path, boost: Path) -> pd.DataFrame:
    parts = [pd.read_csv(path, sep="\t", index_col=0) for path in [prime, boost]]
    result = pd.concat(parts, axis=1)
    result.columns = result.columns.astype(str)
    return result.loc[:, ~result.columns.duplicated()]


def module_scores(counts: pd.DataFrame) -> pd.DataFrame:
    library = counts.sum(axis=0)
    log_cpm = np.log2(counts.divide(library, axis=1) * 1_000_000 + 1)
    scores = {}
    for name, genes in GENE_MODULES.items():
        present = [gene for gene in genes if gene in log_cpm.index]
        if len(present) < 3:
            raise ValueError(f"too few genes available for {name} module")
        standardized = log_cpm.loc[present].T
        standardized = (standardized - standardized.mean()) / standardized.std().replace(0, 1)
        scores[name] = standardized.mean(axis=1)
    return pd.DataFrame(scores)


def module_scores_from_membership(counts: pd.DataFrame, membership: pd.DataFrame,
                                  gene_column: str = "gene_id",
                                  module_column: str = "module") -> pd.DataFrame:
    """Score any curated repertoire, including BloodGen3, from a gene/module table."""
    library = counts.sum(axis=0)
    log_cpm = np.log2(counts.divide(library, axis=1) * 1_000_000 + 1)
    output = {}
    for module, rows in membership.groupby(module_column):
        genes = [str(gene).split(".")[0] for gene in rows[gene_column] if str(gene).split(".")[0] in log_cpm.index]
        if len(genes) < 3:
            continue
        values = log_cpm.loc[genes].T
        output[str(module)] = ((values - values.mean()) / values.std().replace(0, 1)).mean(axis=1)
    if not output:
        raise ValueError("no curated modules had at least three genes in the count matrix")
    return pd.DataFrame(output)


def impulse_features(days: np.ndarray, memory: int, rank: int, order: int,
                     boost: np.ndarray | None = None) -> np.ndarray:
    basis = dct(np.eye(memory), type=2, norm="ortho", axis=0)[:rank]
    day_index = np.clip(np.asarray(days, int), 0, memory - 1)
    linear = basis[:, day_index].T
    features = [linear]
    if order == 2:
        pairs = combinations_with_replacement(range(rank), 2)
        features.append(np.column_stack([linear[:, a] * linear[:, b] for a, b in pairs]))
    elif order == 3:
        pairs = combinations_with_replacement(range(rank), 2)
        triples = combinations_with_replacement(range(rank), 3)
        features.append(np.column_stack([linear[:, a] * linear[:, b] for a, b in pairs]))
        features.append(np.column_stack([linear[:, a] * linear[:, b] * linear[:, c]
                                         for a, b, c in triples]))
    base = np.column_stack(features)
    if boost is not None:
        features.append(base * np.asarray(boost)[:, None])
        base = np.column_stack([base, features[-1]])
    return base


def _baseline_relative(scores: pd.DataFrame, metadata: pd.DataFrame) -> pd.DataFrame:
    table = metadata.join(scores, how="inner")
    for module in scores.columns:
        table[f"absolute_{module}"] = table[module]
    for (_, _), rows in table.groupby(["subject", "phase"]).groups.items():
        ordered = table.loc[rows].sort_values("day")
        table.loc[ordered.index, scores.columns] -= ordered.iloc[0][scores.columns].to_numpy(float)
    for module in scores.columns:
        memory = {}
        for subject, rows in table.groupby("subject"):
            phase0 = rows.sort_values("day").groupby("phase").first()
            memory[subject] = (phase0.at["boost", f"absolute_{module}"] -
                               phase0.at["prime", f"absolute_{module}"]) if set(
                                   ["prime", "boost"]).issubset(phase0.index) else 0.0
        table[f"memory_{module}"] = table.subject.map(memory) * (table.phase == "boost")
    return table


def _nested_alpha(design: np.ndarray, y: np.ndarray, groups: np.ndarray) -> float:
    choices = [.03, .1, .3, 1., 3., 10.]
    unique = np.unique(groups)
    splitter = GroupKFold(min(4, len(unique)))
    losses = []
    for alpha in choices:
        fold = []
        for train, test in splitter.split(design, y, groups):
            scaler = StandardScaler().fit(design[train])
            model = Ridge(alpha=alpha).fit(scaler.transform(design[train]), y[train])
            fold.append(np.mean((y[test] - model.predict(scaler.transform(design[test]))) ** 2))
        losses.append(np.mean(fold))
    return choices[int(np.argmin(losses))]


def evaluate_models(table: pd.DataFrame, modules: list[str], memory: int = 14,
                    rank: int = 5, alpha: float = 1.0) -> tuple[pd.DataFrame, pd.DataFrame]:
    configurations = {"linear": (1, "none"), "volterra2": (2, "none"),
                      "state_volterra2": (2, "phase"), "latent_volterra2": (2, "latent"),
                      "mixed_volterra2": (2, "mixed"), "volterra3": (3, "none"),
                      "latent_volterra3": (3, "latent")}
    predictions, metrics = [], []
    subjects = table.subject.unique()
    for model_name, (order, state_mode) in configurations.items():
        base = impulse_features(table.day.to_numpy(), memory, rank, order)
        for held_out in subjects:
            train = table.subject != held_out; test = ~train
            for module in modules:
                if state_mode == "phase":
                    design = np.column_stack([base, base * (table.phase == "boost").to_numpy()[:, None]])
                elif state_mode == "latent":
                    design = np.column_stack([base, base * table[f"memory_{module}"].to_numpy()[:, None]])
                elif state_mode == "mixed":
                    # Penalized subject intercepts absorb training-subject baselines; the unseen
                    # subject receives the population intercept only, as in random-effects prediction.
                    subject_columns = pd.get_dummies(table.subject, dtype=float).to_numpy()
                    design = np.column_stack([base, subject_columns])
                else:
                    design = base
                scaler = StandardScaler().fit(design[train])
                selected_alpha = _nested_alpha(design[train], table.loc[train, module].to_numpy(),
                                               table.loc[train, "subject"].to_numpy())
                model = Ridge(alpha=selected_alpha).fit(scaler.transform(design[train]), table.loc[train, module])
                estimate = model.predict(scaler.transform(design[test]))
                observed = table.loc[test, module].to_numpy()
                metrics.append({"model": model_name, "subject": held_out, "module": module,
                                "r2": r2_score(observed, estimate) if len(observed) > 1 else np.nan,
                                "mae": mean_absolute_error(observed, estimate),
                                "selected_alpha": selected_alpha})
                for index, value, truth in zip(table.index[test], estimate, observed):
                    predictions.append({"model": model_name, "sample": index, "subject": held_out,
                                        "module": module, "phase": table.at[index, "phase"],
                                        "day": int(table.at[index, "day"]), "observed": truth,
                                        "predicted": value})
    return pd.DataFrame(predictions), pd.DataFrame(metrics)


def landmark_checks(predictions: pd.DataFrame) -> pd.DataFrame:
    expected = {("interferon", "prime"): 2, ("interferon", "boost"): 1,
                ("inflammation", "boost"): 1, ("plasmablast", "boost"): 4}
    rows = []
    chosen = predictions[predictions.model == "latent_volterra2"]
    for (module, phase), expected_day in expected.items():
        subset = chosen[(chosen.module == module) & (chosen.phase == phase)]
        actual = subset.groupby("day")["observed"].mean()
        predicted = subset.groupby("day")["predicted"].mean()
        rows.append({"module": module, "phase": phase, "expected_peak_day": expected_day,
                     "observed_peak_day": int(actual.idxmax()),
                     "predicted_peak_day": int(predicted.idxmax()),
                     "predicted_peak_error_days": abs(int(predicted.idxmax()) - expected_day)})
    return pd.DataFrame(rows)


def sampling_ablation(table: pd.DataFrame, modules: list[str]) -> pd.DataFrame:
    schedules = {"dense": set(range(0, 14)), "five_point": {0, 1, 3, 6, 13},
                 "four_point": {0, 2, 6, 13}}
    rows = []
    for name, days in schedules.items():
        subset = table[table.day.isin(days)]
        predictions, _ = evaluate_models(subset, modules)
        chosen = predictions[predictions.model == "latent_volterra2"]
        for module in modules:
            part = chosen[chosen.module == module]
            rows.append({"schedule": name, "module": module,
                         "r2": r2_score(part.observed, part.predicted)})
    return pd.DataFrame(rows)


def run_gse190001(prime: Path, boost: Path, soft: Path, out: Path) -> None:
    counts = read_counts(prime, boost)
    metadata = read_soft_metadata(soft)
    scores = module_scores(counts)
    table = _baseline_relative(scores, metadata)
    modules = list(GENE_MODULES)
    predictions, metrics = evaluate_models(table, modules)
    landmarks = landmark_checks(predictions)
    ablation = sampling_ablation(table, modules)
    out.mkdir(parents=True, exist_ok=True)
    table.to_csv(out / "module_scores.csv")
    predictions.to_csv(out / "loso_predictions.csv", index=False)
    metrics.to_csv(out / "loso_metrics.csv", index=False)
    landmarks.to_csv(out / "landmark_checks.csv", index=False)
    ablation.to_csv(out / "sampling_ablation.csv", index=False)
    chosen = predictions[predictions.model == "latent_volterra2"]
    pooled_r2 = {name: float(r2_score(group.observed, group.predicted))
                 for name, group in predictions.groupby("model")}
    summary = {"source": "GSE190001", "subjects": int(table.subject.nunique()),
               "profiles": len(table), "modules": modules,
               "latent_volterra2_overall_r2": float(r2_score(chosen.observed, chosen.predicted)),
               "pooled_loso_r2_by_model": pooled_r2,
               "best_model_by_mean_subject_r2": metrics.groupby("model").r2.mean().idxmax(),
               "outcome_gap": "The public antibody supplement uses participant identifiers that "
               "are not cross-walked to GEO RNA identifiers, preventing leakage-safe individual "
               "RNA-to-antibody validation without author-provided mapping.",
               "identifiability_warning": "Fixed-dose prime/boost data validate response kernels "
               "but do not identify an optimal alternative dosing schedule."}
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    plot_response_trajectories(chosen, out / "response_trajectories.png")
    plot_model_comparison(predictions, out / "model_comparison.png")
    plot_residual_heatmap(chosen, out / "residual_heatmap.png")
    plot_sampling_ablation(ablation, out / "sampling_ablation.png")


def run_gse102459(matrix: Path, out: Path, n_modules: int = 3) -> None:
    """External post-dose-2 replication using whole-blood PCA modules."""
    expression, metadata = read_geo_series_matrix(matrix)
    metadata = metadata[metadata.title.str.startswith("WB,")].copy()
    metadata["subject"] = metadata.title.str.extract(r"PID (\d+)")[0]
    metadata["global_day"] = metadata.title.str.extract(r"Day (\d+)")[0].astype(int)
    metadata = metadata[metadata.global_day >= 30]
    metadata["day"] = metadata.global_day - 30
    metadata["phase"] = "boost"
    expression = expression[metadata.index]
    scores, loadings = pca_modules(expression, n_modules)
    table = metadata.join(scores)
    modules = list(scores.columns)
    for module in modules:
        table[f"absolute_{module}"] = table[module]
        baseline = table.sort_values("day").groupby("subject")[module].first()
        table[module] -= table.subject.map(baseline)
        table[f"memory_{module}"] = 0.0
    predictions, metrics = evaluate_models(table, modules, memory=31, rank=5)
    out.mkdir(parents=True, exist_ok=True)
    table.to_csv(out / "module_scores.csv")
    loadings.to_csv(out / "probe_loadings.csv")
    predictions.to_csv(out / "loso_predictions.csv", index=False)
    metrics.to_csv(out / "loso_metrics.csv", index=False)
    pooled = {name: float(r2_score(group.observed, group.predicted))
              for name, group in predictions.groupby("model")}
    summary = {"source": "GSE102459", "subjects": int(table.subject.nunique()),
               "profiles": len(table), "modules": modules, "pooled_loso_r2_by_model": pooled,
               "scope": "External post-dose-2 whole-blood trajectory replication; PCA modules "
               "are platform-local and not direct biological module labels."}
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    chosen = predictions[predictions.model == max(pooled, key=pooled.get)]
    plot_response_trajectories(chosen, out / "response_trajectories.png")
    plot_model_comparison(predictions, out / "model_comparison.png")
    plot_residual_heatmap(chosen, out / "residual_heatmap.png")
