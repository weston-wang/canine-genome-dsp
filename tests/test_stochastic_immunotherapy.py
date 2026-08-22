import numpy as np
import pandas as pd

from canine_dsp.immunotherapy import reference_immunotherapy_system
from canine_dsp.stochastic_immunotherapy import (
    StochasticConfig,
    comparative_metrics,
    optimize_stochastic_immunotherapy,
    particle_filter,
    predictive_quantiles,
    risk_metrics,
    sample_observations,
    simulate_stochastic,
)


def small_run(seed=7):
    system, kernels = reference_immunotherapy_system()
    schedule = np.zeros((18, 3)); schedule[[0, 7, 14], 0] = .7
    schedule[[0, 7, 14], 1] = .5
    config = StochasticConfig(draws=24, effective_population=2_000)
    return system, kernels, schedule, config, simulate_stochastic(
        system, kernels, schedule, np.array([.28, .018]), config, seed)


def test_stochastic_simulation_is_reproducible_and_nonnegative():
    system, kernels, schedule, config, first = small_run()
    second = simulate_stochastic(system, kernels, schedule, np.array([.28, .018]), config, 7)
    np.testing.assert_array_equal(first.states, second.states)
    assert np.all(first.states >= 0)
    assert np.std(first.states[:, -1].sum(axis=1)) > 0


def test_risk_metrics_are_probabilities_and_ordered_intervals():
    _, _, _, config, run = small_run()
    metrics = risk_metrics(run, config)
    for name in ["response_probability", "escape_probability",
                 "inflammation_exceedance_probability"]:
        assert 0 <= metrics[name] <= 1
        interval = metrics[f"{name}_mc95"]
        assert 0 <= interval[0] <= metrics[name] <= interval[1] <= 1
    assert metrics["terminal_tumor_p05"] <= metrics["median_terminal_tumor"]
    assert metrics["median_terminal_tumor"] <= metrics["terminal_tumor_p95"]


def test_observation_model_and_particle_filter_have_valid_shapes():
    system, kernels, schedule, config, run = small_run()
    observations = sample_observations(run, [0, 4, 9, 18], config)
    assert (observations.ctdna_alt <= observations.ctdna_depth).all()
    filtered = particle_filter(system, kernels, schedule, np.array([.28, .018]),
                               observations, config, particles=48)
    assert len(filtered) == len(schedule) + 1
    assert filtered.tumor_p05.le(filtered.tumor_median).all()
    assert filtered.tumor_median.le(filtered.tumor_p95).all()
    assert filtered.cytotoxic_p05.le(filtered.cytotoxic_median).all()
    assert filtered.cytotoxic_median.le(filtered.cytotoxic_p95).all()
    assert filtered.effective_sample_size.between(1, 48).all()
    assert filtered.observed.sum() == len(observations)


def test_particle_filter_accepts_missing_modalities_and_duplicate_days():
    system, kernels, schedule, config, run = small_run()
    observations = sample_observations(run, [0, 4, 9], config)
    imaging_only = observations[["day", "imaging_burden"]]
    duplicated = np.repeat(imaging_only.to_numpy(), 2, axis=0)
    filtered = particle_filter(system, kernels, schedule, np.array([.28, .018]),
                               pd.DataFrame(duplicated, columns=imaging_only.columns),
                               config, particles=48)
    assert filtered.observed.sum() == len(imaging_only)
    assert filtered.effective_sample_size.between(1, 48).all()


def test_predictive_quantiles_cover_each_median():
    _, _, schedule, _, run = small_run()
    values = predictive_quantiles(run)
    assert len(values) == len(schedule) + 1
    assert values.tumor_p05.le(values.tumor_median).all()
    assert values.tumor_median.le(values.tumor_p95).all()


def test_matched_counterfactual_comparison_reports_bounded_probabilities():
    system, kernels, schedule, config, treated = small_run()
    untreated = simulate_stochastic(system, kernels, np.zeros_like(schedule),
                                    np.array([.28, .018]), config, 7)
    metrics = comparative_metrics(treated, untreated)
    assert 0 <= metrics["probability_lower_burden_than_untreated"] <= 1
    assert 0 <= metrics["probability_at_least_50pct_lower_than_untreated"] <= 1


def test_stochastic_inverse_respects_channel_bounds():
    system, kernels = reference_immunotherapy_system()
    config = StochasticConfig(draws=8, effective_population=1_000)
    bounds = np.array([.6, .4, .3])
    fit = optimize_stochastic_immunotherapy(system, kernels, np.array([.28, .018]),
                                            10, [0, 5], bounds, config,
                                            seed=3, maxiter=1)
    assert fit["schedule"].shape == (10, 3)
    assert np.all(fit["schedule"] >= 0)
    assert np.all(fit["schedule"] <= bounds[None, :] + 1e-12)
