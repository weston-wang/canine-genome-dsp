import numpy as np
import pytest

from canine_dsp.mapk_resistance import (
    CLONE_NAMES,
    ResistanceModel,
    _dominant_mechanism,
    build_mutation_matrix,
    drug_kill_rate,
    poisson_mutation_injections,
    run_monte_carlo,
    simulate_resistance,
)


def test_second_drug_adds_uniform_kill_across_all_clones():
    model = ResistanceModel(growth=np.array([.05, .05]), ic50_nM=np.array([1e6, 1e6]),
                            max_kill=np.array([0., 0.]), mutation=np.eye(2),
                            ic50_nM_2=100., max_kill_2=.2)
    # drug 1 is set to have no effect (huge IC50, zero max_kill); drug 2 alone should still
    # suppress both clones identically since it applies uniformly, not per-clone.
    state = simulate_resistance(model, np.zeros(60), np.array([.1, .1]), concentration_2=np.full(60, 1e6))
    assert state[-1, 0] < state[0, 0]
    assert state[-1, 1] < state[0, 1]
    np.testing.assert_allclose(state[-1, 0], state[-1, 1])


def test_second_drug_absent_by_default():
    model = ResistanceModel(growth=np.array([.05]), ic50_nM=np.array([100.]),
                            max_kill=np.array([.01]), mutation=np.array([[1.0]]))
    with_none = simulate_resistance(model, np.zeros(30), np.array([.1]), concentration_2=None)
    without_arg = simulate_resistance(model, np.zeros(30), np.array([.1]))
    np.testing.assert_allclose(with_none, without_arg)


def test_run_monte_carlo_accepts_second_drug():
    model = ResistanceModel(growth=np.array([.06, .05, .055, .058]),
                            ic50_nM=np.array([222., 222. * 40, 222. * 1.2, 222. * 60]),
                            max_kill=np.array([.18, .02, .035, .015]), mutation=np.eye(4),
                            ic50_nM_2=100., max_kill_2=.05)
    seeding_rates = build_mutation_matrix(np.array([.85, .10, .05]) * 2e-6)[0, 1:]
    outcome = run_monte_carlo(model, 1640., 200, seeding_rates, trials=20,
                              css_reference_2=500., seed=2)
    assert outcome.trajectories.shape == (20, 201, 4)


def test_mutation_matrix_rows_sum_to_one():
    mutation = build_mutation_matrix(np.array([.1, .05, .02]))
    np.testing.assert_allclose(mutation.sum(axis=1), 1)
    np.testing.assert_allclose(mutation[1:, 1:], np.eye(3))


def test_resistance_model_rejects_bad_mutation_matrix():
    with pytest.raises(ValueError):
        ResistanceModel(growth=np.ones(2), ic50_nM=np.ones(2), max_kill=np.ones(2),
                        mutation=np.array([[1, 0], [0, 0]]))


def test_drug_kill_rate_saturates_at_max_kill():
    assert drug_kill_rate(0, np.array([100.]), 1.5, np.array([.2]))[0] == 0
    saturated = drug_kill_rate(1e9, np.array([100.]), 1.5, np.array([.2]))[0]
    assert saturated == pytest.approx(.2, rel=1e-3)
    half = drug_kill_rate(100., np.array([100.]), 1.0, np.array([.2]))[0]
    assert half == pytest.approx(.1)


def test_sensitive_clone_regresses_when_kill_exceeds_growth():
    model = ResistanceModel(growth=np.array([.05]), ic50_nM=np.array([100.]),
                            max_kill=np.array([.3]), mutation=np.array([[1.0]]), hill=1.5)
    state = simulate_resistance(model, np.full(60, 1000.), np.array([.3]))
    assert state[-1, 0] < state[0, 0]


def test_clone_grows_without_drug():
    model = ResistanceModel(growth=np.array([.05]), ic50_nM=np.array([100.]),
                            max_kill=np.array([.3]), mutation=np.array([[1.0]]), hill=1.5)
    state = simulate_resistance(model, np.zeros(60), np.array([.3]))
    assert state[-1, 0] > state[0, 0]
    assert state[-1, 0] < 1.0


def test_dominant_mechanism_reports_durable_response_when_not_progressed():
    assert _dominant_mechanism(np.array([.1, .8, .05, .05]), progressed=False) == "durable_response"


def test_dominant_mechanism_picks_largest_resistant_clone():
    label = _dominant_mechanism(np.array([.05, .1, .7, .15]), progressed=True)
    assert label == CLONE_NAMES[2]


def _dog_like_model() -> ResistanceModel:
    return ResistanceModel(
        growth=np.array([.06, .05, .055, .058]),
        ic50_nM=np.array([222., 222. * 40, 222. * 1.2, 222. * 60]),
        max_kill=np.array([.18, .02, .035, .015]),
        mutation=np.eye(4),
    )


def test_poisson_mutation_injections_can_be_empty_at_low_rate():
    rng = np.random.default_rng(0)
    trajectory = np.full(30, 1e-6)  # tiny population -> tiny cell-days -> usually zero events
    injections = poisson_mutation_injections(rng, trajectory, np.array([1e-4, 1e-4, 1e-4]))
    assert injections == {}


def test_poisson_mutation_injections_fires_at_high_rate():
    rng = np.random.default_rng(0)
    trajectory = np.full(30, 1.0)
    injections = poisson_mutation_injections(rng, trajectory, np.array([5.0, 0.0, 0.0]), seed_fraction=1e-8)
    assert injections
    total_seeded = sum(vector[1] for vector in injections.values())
    assert total_seeded > 0
    assert all(vector[2] == 0 and vector[3] == 0 for vector in injections.values())


def test_monte_carlo_forced_preexisting_resistance_eventually_progresses():
    k = 4
    model = _dog_like_model()
    seeding_rates = 0.012 * np.array([.85, .10, .05])
    outcome = run_monte_carlo(model, css_reference=1640., horizon_days=200, seeding_rates=seeding_rates,
                             trials=20, preexisting_prob=1.0, seed=3)
    assert outcome.trajectories.shape == (20, 201, k)
    assert outcome.progressed.any()
    assert all(label in {"durable_response", *CLONE_NAMES[1:]} for label in outcome.dominant_mechanism)


def test_monte_carlo_can_produce_durable_response_with_no_preexisting_clone():
    model = _dog_like_model()
    seeding_rates = 0.012 * np.array([.85, .10, .05])
    outcome = run_monte_carlo(model, css_reference=1640., horizon_days=730, seeding_rates=seeding_rates,
                             trials=60, preexisting_prob=0.0, seed=5)
    assert (~outcome.progressed).any()
