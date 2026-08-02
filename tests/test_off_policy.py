import numpy as np
import pandas as pd

from canine_dsp.off_policy import OPEThresholds, evaluate_logged_policy


def logged_table(patients=40, behavior_probability=.5, target_probability=.5):
    rows = []
    for patient in range(patients):
        for step in range(3):
            rows.append({"patient": patient, "step": step, "reward": 1.0,
                         "behavior_probability": behavior_probability,
                         "target_probability": target_probability,
                         "q_logged": 0.0, "v_next": 0.0, "v_initial": 0.0})
    return pd.DataFrame(rows)


def test_on_policy_estimators_agree_and_do_not_invent_advantage():
    result = evaluate_logged_policy(logged_table(), cross_fitted_nuisance=True, seed=2)
    np.testing.assert_allclose([result["behavior_policy_value"], result["pdis_target_value"],
                                result["snips_target_value"], result["sequential_dr_target_value"]], 3)
    assert result["evidence_status"] == "NO_RETROSPECTIVE_ADVANTAGE"
    assert result["effective_sample_size"] == 40
    assert not result["clinical_superiority_supported"]


def test_off_policy_evaluation_fails_closed_without_overlap():
    data = logged_table(behavior_probability=.001, target_probability=.5)
    result = evaluate_logged_policy(data, OPEThresholds(min_effective_sample_size=1),
                                    cross_fitted_nuisance=True)
    assert result["evidence_status"] == "NOT_EVALUABLE_NO_OVERLAP"


def test_off_policy_evaluation_requires_cross_fitting():
    result = evaluate_logged_policy(logged_table(), cross_fitted_nuisance=False)
    assert result["evidence_status"] == "NOT_EVALUABLE_NUISANCE_NOT_CROSS_FITTED"
