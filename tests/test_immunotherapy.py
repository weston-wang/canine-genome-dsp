import numpy as np

from canine_dsp.evolution import volterra_response
from canine_dsp.immunotherapy import (optimize_immunotherapy, reference_immunotherapy_system,
                                      simulate_immunotherapy, synergy_surface)


def test_combination_kernel_has_positive_timing_synergy():
    _, kernels = reference_immunotherapy_system()
    surface = synergy_surface(kernels)
    assert surface.shape == (10, 10)
    assert surface.max() > 0


def test_bounded_inverse_reduces_tumor_and_reports_safety_output():
    system, kernels = reference_immunotherapy_system()
    initial = np.array([.28, .018])
    result = optimize_immunotherapy([system], kernels, initial, 24, [0, 7, 14],
                                    np.array([1., .8, .7]), maxiter=8)
    untreated = simulate_immunotherapy(system, np.zeros((24, 3)), initial)
    assert result["states"][0, -1].sum() < untreated[-1].sum()
    assert result["immune"].shape == (24, 3)
    assert np.all(result["schedule"] >= 0)
