import numpy as np
import pytest

from canine_dsp.qsp import (ExposureModel, protocol_is_feasible, protocol_violations,
                            reference_exposure_model, reference_protocol_constraints,
                            simulate_exposure)


def test_one_compartment_half_life_and_target_engagement():
    model = ExposureModel(half_life=np.array([2.]), bioavailability=np.array([1.]),
                          tumor_penetration=np.array([1.]), tumor_equilibration=np.array([1.]),
                          ec50=np.array([.5]), linear_channel=np.array([False]))
    doses = np.zeros((5, 1)); doses[0] = 1
    result = simulate_exposure(doses, model)
    np.testing.assert_allclose(result.plasma[:, 0], 2 ** (-np.arange(5) / 2))
    np.testing.assert_allclose(result.effective_input[:, 0],
                               result.tumor[:, 0] / (.5 + result.tumor[:, 0]))


def test_exposure_rejects_negative_or_nonfinite_doses():
    model = reference_exposure_model()
    with pytest.raises(ValueError):
        simulate_exposure(np.full((4, 3), -1.), model)
    with pytest.raises(ValueError):
        simulate_exposure(np.full((4, 3), np.nan), model)


def test_protocol_checks_dose_cumulative_cmax_and_auc_bounds():
    model = reference_exposure_model(); constraints = reference_protocol_constraints()
    schedule = np.zeros((42, 3)); schedule[[0, 7, 14, 21]] = [.75, .60, .45]
    assert protocol_is_feasible(schedule, model, constraints)
    schedule[1, 0] = 2
    violations = protocol_violations(schedule, model, constraints)
    assert violations["disallowed_dose"][0] > 0
    assert violations["per_dose"][0] > 0
    assert not protocol_is_feasible(schedule, model, constraints)
