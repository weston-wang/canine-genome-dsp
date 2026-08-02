import numpy as np
import pytest

from canine_dsp.melanoma_dsp import (
    LATEST_TREATMENT_DAY,
    MelanomaSimulationConfig,
    NADINA_TOTAL_MG,
    clinical_metrics,
    nadina_schedule,
    reference_melanoma_model,
    schedule_is_feasible,
    search_constrained_schedule,
    simulate_antibody_exposure,
    simulate_melanoma,
    volterra_cross_residual,
)


def test_nadina_schedule_and_exposure_are_bounded_and_disease_specific():
    schedule = nadina_schedule()
    np.testing.assert_array_equal(schedule.sum(axis=0), NADINA_TOTAL_MG)
    assert schedule_is_feasible(schedule)
    assert schedule[LATEST_TREATMENT_DAY + 1:].sum() == 0

    exposure = simulate_antibody_exposure(schedule)
    assert exposure.occupancy.shape == schedule.shape
    assert np.all((0 <= exposure.occupancy) & (exposure.occupancy <= 1))
    assert exposure.occupancy[21].sum() > exposure.occupancy[20].sum()


def test_cross_kernel_and_stochastic_simulation_are_reproducible():
    model = reference_melanoma_model(memory=8)
    schedule = nadina_schedule()
    exposure = simulate_antibody_exposure(schedule, model.exposure)
    residual = volterra_cross_residual(exposure.occupancy, model.cross_kernel)
    assert residual.shape == (len(schedule),)
    assert np.all(residual >= 0)
    assert residual.max() <= model.cross_kernel.bound

    config = MelanomaSimulationConfig(draws=20, effective_population=1_000)
    first = simulate_melanoma(schedule, model, config, seed=17)
    second = simulate_melanoma(schedule, model, config, seed=17)
    np.testing.assert_array_equal(first.immune, second.immune)
    np.testing.assert_array_equal(first.tumor, second.tumor)
    assert first.immune.shape == (20, 43, 3)
    assert first.tumor.shape == (20, 43, 2)
    assert np.all(first.tumor >= 0)


def test_unconstrained_simulation_is_available_only_when_explicit():
    high_ipilimumab = nadina_schedule()
    high_ipilimumab[[0, 21], 0] = 240.0
    config = MelanomaSimulationConfig(draws=8, effective_population=500)
    with pytest.raises(ValueError, match="NADINA-derived"):
        simulate_melanoma(high_ipilimumab, config=config)
    run = simulate_melanoma(
        high_ipilimumab, config=config, seed=4, enforce_constraints=False)
    assert run.schedule[:, 0].sum() == 480.0


def test_metrics_are_explicitly_model_conditional_and_search_stays_feasible():
    config = MelanomaSimulationConfig(draws=12, effective_population=700)
    run = simulate_melanoma(nadina_schedule(), config=config, seed=9)
    metrics = clinical_metrics(run, config)
    probability_names = [
        "modeled_major_pathologic_response_probability",
        "modeled_complete_pathologic_response_probability",
        "modeled_escape_dominance_probability",
        "modeled_toxicity_proxy_exceedance_probability",
    ]
    assert all(0 <= metrics[name] <= 1 for name in probability_names)
    assert not metrics["clinical_superiority_established"]
    assert "Synthetic" in metrics["claim_scope"]

    first = search_constrained_schedule(config=config, candidates=7, seed=5)
    second = search_constrained_schedule(config=config, candidates=7, seed=5)
    np.testing.assert_array_equal(first["schedule"], second["schedule"])
    assert first["schedule_feasible"]
    assert np.all(first["schedule"].sum(axis=0) <= NADINA_TOTAL_MG + 1e-9)
    assert first["schedule"][LATEST_TREATMENT_DAY + 1:].sum() == 0
    assert not first["clinical_superiority_established"]
