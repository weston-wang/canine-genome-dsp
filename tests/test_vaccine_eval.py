import numpy as np

from canine_dsp.vaccine_eval import impulse_features


def test_state_volterra_features_add_boost_interactions():
    days = np.array([1, 2, 3, 1, 2, 3])
    boost = np.array([0, 0, 0, 1, 1, 1])
    common = impulse_features(days, 5, 2, 2)
    state = impulse_features(days, 5, 2, 2, boost)
    assert state.shape[1] == 2 * common.shape[1]
    np.testing.assert_allclose(state[:3, common.shape[1]:], 0)
    np.testing.assert_allclose(state[3:, common.shape[1]:], common[3:])


def test_third_order_contains_hierarchical_lower_terms():
    days = np.arange(5)
    second = impulse_features(days, 5, 2, 2)
    third = impulse_features(days, 5, 2, 3)
    np.testing.assert_allclose(third[:, :second.shape[1]], second)
    assert third.shape[1] == second.shape[1] + 4  # C(2 + 3 - 1, 3)
