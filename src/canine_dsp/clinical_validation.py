"""Fail-closed validation helpers for small aggregate clinical treatment-arm data."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.special import expit
from scipy.stats import spearmanr
from sklearn.linear_model import LogisticRegression


def _arm_rows(table: pd.DataFrame, features: list[str], events: str,
              total: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Represent each binomial arm as event/non-event rows with frequency weights."""
    x, y, weight = [], [], []
    for _, row in table.iterrows():
        values = row[features].to_numpy(dtype=float)
        event_count = int(row[events]); sample_count = int(row[total])
        if not 0 <= event_count <= sample_count or sample_count <= 0:
            raise ValueError("clinical event counts must lie between zero and the arm size")
        if event_count:
            x.append(values); y.append(1); weight.append(event_count)
        if sample_count - event_count:
            x.append(values); y.append(0); weight.append(sample_count - event_count)
    return np.asarray(x), np.asarray(y), np.asarray(weight, float)


def leave_one_arm_out_binomial(table: pd.DataFrame, features: list[str], events: str,
                               total: str, arm: str = "arm",
                               regularization: float = 0.35) -> tuple[pd.DataFrame, dict]:
    """Predict each randomized arm from all other arms using a ridge-logistic link.

    This validates transport across *treatment arms*, not across patients.  The distinction is
    important because published aggregate counts do not recover patient-level heterogeneity.
    """
    required = {arm, events, total, *features}
    missing = required.difference(table.columns)
    if missing:
        raise ValueError(f"missing aggregate clinical columns: {sorted(missing)}")
    if table[arm].duplicated().any() or len(table) < 3:
        raise ValueError("at least three uniquely named treatment arms are required")
    rows = []
    for heldout in table[arm]:
        train = table.loc[table[arm] != heldout]
        x, y, weights = _arm_rows(train, features, events, total)
        if len(np.unique(y)) != 2:
            raise ValueError("each training fold needs both events and non-events")
        model = LogisticRegression(C=regularization, solver="lbfgs", max_iter=2_000)
        model.fit(x, y, sample_weight=weights)
        test = table.loc[table[arm] == heldout].iloc[0]
        probability = float(model.predict_proba(
            test[features].to_numpy(dtype=float)[None, :])[0, 1])
        rows.append({arm: heldout, "observed_probability": float(test[events] / test[total]),
                     "predicted_probability": probability, "events": int(test[events]),
                     "total": int(test[total]), "fold": f"held_out_{heldout}"})
    predictions = pd.DataFrame(rows)
    observed = predictions.observed_probability.to_numpy()
    predicted = np.clip(predictions.predicted_probability.to_numpy(), 1e-8, 1 - 1e-8)
    weights = predictions.total.to_numpy(dtype=float)
    brier = np.average(np.square(predicted - observed), weights=weights)
    log_loss = -np.average(observed * np.log(predicted)
                           + (1 - observed) * np.log(1 - predicted), weights=weights)
    metrics = {"arm_level_weighted_brier": float(brier),
               "arm_level_weighted_log_loss": float(log_loss),
               "arms": int(len(predictions)),
               "validation_unit": "randomized_treatment_arm",
               "patient_level_validation": False}
    return predictions, metrics


def calibrated_arm_predictions(table: pd.DataFrame, features: list[str], events: str,
                               total: str, regularization: float = 0.35) -> np.ndarray:
    """Fit all aggregate arms for descriptive calibration after cross-validation is complete."""
    model = fit_binomial_link(table, features, events, total, regularization)
    return model.predict_proba(table[features].to_numpy(float))[:, 1]


def fit_binomial_link(table: pd.DataFrame, features: list[str], events: str,
                      total: str, regularization: float = 0.35) -> LogisticRegression:
    """Fit a ridge-logistic link to aggregate binomial arms using frequency weights."""
    x, y, weights = _arm_rows(table, features, events, total)
    if len(np.unique(y)) != 2:
        raise ValueError("calibration needs both events and non-events")
    model = LogisticRegression(C=regularization, solver="lbfgs", max_iter=2_000)
    model.fit(x, y, sample_weight=weights)
    return model


def clinical_utility_rank(table: pd.DataFrame, predicted_response: np.ndarray,
                          predicted_toxicity: np.ndarray, response_events: str,
                          toxicity_events: str, total: str,
                          toxicity_weight: float = 0.5,
                          response_noninferiority_margin: float = 0.10) -> dict:
    """Check whether a model recovers the trial's efficacy-toxicity arm ordering."""
    observed_utility = (table[response_events].to_numpy(float) / table[total]
                        - toxicity_weight * table[toxicity_events].to_numpy(float) / table[total])
    predicted_utility = (np.asarray(predicted_response, float)
                         - toxicity_weight * np.asarray(predicted_toxicity, float))
    correlation = spearmanr(observed_utility, predicted_utility).statistic
    observed_best = str(table.iloc[int(np.argmax(observed_utility))].arm)
    predicted_best = str(table.iloc[int(np.argmax(predicted_utility))].arm)
    observed_response = table[response_events].to_numpy(float) / table[total]
    observed_toxicity = table[toxicity_events].to_numpy(float) / table[total]
    predicted_response = np.asarray(predicted_response, float)
    predicted_toxicity = np.asarray(predicted_toxicity, float)
    observed_eligible = observed_response >= observed_response.max() - response_noninferiority_margin
    predicted_eligible = predicted_response >= predicted_response.max() - response_noninferiority_margin
    observed_tradeoff = int(np.flatnonzero(observed_eligible)[
        np.argmin(observed_toxicity[observed_eligible])])
    predicted_tradeoff = int(np.flatnonzero(predicted_eligible)[
        np.argmin(predicted_toxicity[predicted_eligible])])
    observed_tradeoff_arm = str(table.iloc[observed_tradeoff].arm)
    predicted_tradeoff_arm = str(table.iloc[predicted_tradeoff].arm)
    return {"observed_best_arm": observed_best, "predicted_best_arm": predicted_best,
            "best_arm_recovered": bool(observed_best == predicted_best),
            "spearman_rank_correlation": float(correlation) if np.isfinite(correlation) else None,
            "toxicity_weight": float(toxicity_weight),
            "response_noninferiority_margin": float(response_noninferiority_margin),
            "observed_noninferior_lowest_toxicity_arm": observed_tradeoff_arm,
            "predicted_noninferior_lowest_toxicity_arm": predicted_tradeoff_arm,
            "clinical_tradeoff_arm_recovered": bool(
                observed_tradeoff_arm == predicted_tradeoff_arm)}


def binomial_probability(score: np.ndarray, intercept: float, slope: float) -> np.ndarray:
    """Small public helper used to map latent DSP scores to trial-scale probabilities."""
    return expit(intercept + slope * np.asarray(score, float))
