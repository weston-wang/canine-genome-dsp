import numpy as np
import pandas as pd

from canine_dsp.clinical_validation import (
    clinical_utility_rank,
    leave_one_arm_out_binomial,
)


def aggregate_arms():
    return pd.DataFrame({
        "arm": ["A", "B", "C"], "n": [30, 30, 26],
        "response_events": [24, 23, 17], "toxicity_events": [12, 6, 13],
        "efficacy_score": [.8, .75, .58], "toxicity_score": [.7, .25, .9],
    })


def test_leave_one_arm_out_uses_aggregate_counts_without_pseudoreplication():
    predictions, metrics = leave_one_arm_out_binomial(
        aggregate_arms(), ["efficacy_score"], "response_events", "n")
    assert len(predictions) == 3
    assert predictions.predicted_probability.between(0, 1).all()
    assert metrics["validation_unit"] == "randomized_treatment_arm"
    assert not metrics["patient_level_validation"]


def test_clinical_rank_requires_the_same_best_arm():
    table = aggregate_arms()
    result = clinical_utility_rank(table, np.array([.78, .76, .62]),
                                   np.array([.4, .2, .5]),
                                   "response_events", "toxicity_events", "n")
    assert result["observed_best_arm"] == "B"
    assert result["predicted_best_arm"] == "B"
    assert result["best_arm_recovered"]
    assert result["clinical_tradeoff_arm_recovered"]
