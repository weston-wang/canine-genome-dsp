import numpy as np

from canine_dsp.control import ControlWeights, optimize_vaccine, trajectory_cost
from canine_dsp.evolution import EvolutionModel, ImmuneKernels, simulate_evolution, volterra_response


def small_system():
    model = EvolutionModel(
        growth=np.array([0.12, 0.10]),
        antigen_expression=np.array([[1.0, 0.2], [0.0, 1.0]]),
        presentation=np.ones((2, 2)),
        mutation=np.array([[0.999, 0.001], [0.0, 1.0]]),
        carrying_capacity=2.0,
        immune_kill=.25,
    )
    h1 = np.zeros((2, 2, 3)); h1[0, 0] = [.8, .5, .2]; h1[1, 1] = [.8, .5, .2]
    return model, ImmuneKernels(h1), np.array([.2, .01])


def test_volterra_memory_and_evolution_response():
    model, kernels, initial = small_system()
    schedule = np.zeros((12, 2)); schedule[0, 0] = 1
    response = volterra_response(schedule, kernels)
    np.testing.assert_allclose(response[:4, 0], [.8, .5, .2, 0])
    untreated = simulate_evolution(model, initial, np.zeros_like(response))
    treated = simulate_evolution(model, initial, response)
    assert treated[-1, 0] < untreated[-1, 0]


def test_inverse_control_improves_worst_case():
    model, kernels, initial = small_system()
    result = optimize_vaccine([model], kernels, initial, 14, [0, 5], np.ones(2),
                              np.array([1]), ControlWeights(dose=.001), maxiter=12)
    zero = np.zeros((14, 2))
    baseline = trajectory_cost(simulate_evolution(model, initial, zero), zero, np.array([1]),
                               ControlWeights(dose=.001))
    assert result["worst_cost"] < baseline
    assert result["schedule"].sum() > 0
