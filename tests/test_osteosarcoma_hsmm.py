from dataclasses import replace

import numpy as np
import pytest

from canine_dsp.osteosarcoma_hsmm import (
    OsteosarcomaState,
    OsteosarcomaVolterraHSMM,
    Species,
    SpeciesParameters,
    VolterraTransitionKernels,
    discrete_weibull_hazards,
    reference_osteosarcoma_hsmm,
)


def test_reference_model_has_named_states_species_specific_clocks_and_emissions():
    model = reference_osteosarcoma_hsmm()
    assert model.states == (
        OsteosarcomaState.NED_MRD,
        OsteosarcomaState.INNATE_PRIMED,
        OsteosarcomaState.ADAPTIVE_CONTROL,
        OsteosarcomaState.OCCULT_ESCAPE,
        OsteosarcomaState.VISIBLE_RELAPSE,
        OsteosarcomaState.EXHAUSTED,
    )
    dog = model.species_parameters[Species.DOG]
    human = model.species_parameters[Species.HUMAN]
    assert dog.max_duration != human.max_duration
    assert not np.array_equal(dog.emission_means, human.emission_means)
    assert np.ptp(dog.duration_hazards[0]) > 0


def test_discrete_weibull_hazards_are_explicit_duration_probabilities():
    hazards = discrete_weibull_hazards(scale=5.0, shape=1.8, max_duration=10)
    assert hazards.shape == (10,)
    assert np.all((hazards >= 0) & (hazards <= 1))
    assert hazards[-1] == 1
    assert np.ptp(hazards[:-1]) > 0.05


def test_volterra_transition_probabilities_are_bounded_and_row_stochastic():
    model = reference_osteosarcoma_hsmm(memory=3, rank=2)
    zero = np.zeros((8, len(model.input_names)))
    large = np.full_like(zero, 1e9)
    base = model.transition_probabilities(zero, 4, Species.DOG)
    driven = model.transition_probabilities(large, 4, Species.DOG)
    adjustment = model.volterra_logit_adjustment(large, 4)
    np.testing.assert_allclose(base.sum(axis=1), 1.0)
    np.testing.assert_allclose(driven.sum(axis=1), 1.0)
    np.testing.assert_array_equal(np.diag(driven), np.zeros(len(model.states)))
    assert np.max(np.abs(adjustment)) <= model.kernels.logit_bound
    assert not np.allclose(base, driven)


def test_simulation_is_reproducible_and_filter_is_normalized_with_missing_values():
    model = reference_osteosarcoma_hsmm()
    inputs = np.zeros((36, len(model.input_names)))
    inputs[[0, 7, 14], 0] = .8
    inputs[[0, 7, 14], 1] = .6
    first = model.simulate(inputs, Species.DOG, seed=19)
    second = model.simulate(inputs, "dog", seed=19)
    np.testing.assert_array_equal(first.observations, second.observations)
    np.testing.assert_array_equal(first.state_indices, second.state_indices)
    assert np.all(first.elapsed_durations >= 1)
    observations = first.observations.copy()
    observations[3:8, 1] = np.nan
    observations[20] = np.nan
    filtered = model.filter(observations, inputs, Species.DOG)
    assert filtered.state_posterior.shape == (len(inputs), len(model.states))
    assert filtered.duration_posterior.shape[0:2] == filtered.state_posterior.shape
    np.testing.assert_allclose(filtered.state_posterior.sum(axis=1), 1.0, atol=1e-12)
    np.testing.assert_allclose(
        filtered.duration_posterior.sum(axis=(1, 2)), 1.0, atol=1e-12
    )
    assert np.isfinite(filtered.log_likelihood)


def test_viterbi_decodes_a_valid_explicit_duration_path():
    model = reference_osteosarcoma_hsmm()
    inputs = np.zeros((30, len(model.input_names)))
    simulated = model.simulate(inputs, Species.HUMAN, seed=22)
    decoded = model.most_likely_path(simulated.observations, inputs, Species.HUMAN)
    assert decoded.state_indices.shape == (len(inputs),)
    assert decoded.elapsed_durations.shape == (len(inputs),)
    assert len(decoded.state_path) == len(inputs)
    assert np.isfinite(decoded.log_probability)
    assert set(decoded.state_path).issubset(set(OsteosarcomaState))
    for index in range(1, len(inputs)):
        if decoded.state_indices[index] == decoded.state_indices[index - 1]:
            assert decoded.elapsed_durations[index] == decoded.elapsed_durations[index - 1] + 1
        else:
            assert decoded.elapsed_durations[index] == 1


def test_species_parameters_and_kernel_shapes_are_validated():
    model = reference_osteosarcoma_hsmm()
    dog = model.species_parameters[Species.DOG]
    bad_hazards = np.array(dog.duration_hazards, copy=True)
    bad_hazards[:, -1] = .5
    with pytest.raises(ValueError, match="final duration hazard"):
        replace(dog, duration_hazards=bad_hazards)

    kernels = model.kernels
    with pytest.raises(ValueError, match="same shape"):
        VolterraTransitionKernels(
            input_names=kernels.input_names,
            first_order=kernels.first_order,
            second_left=kernels.second_left,
            second_right=kernels.second_right[..., :-1],
            input_scale=kernels.input_scale,
        )
    with pytest.raises(ValueError, match="required for"):
        OsteosarcomaVolterraHSMM(kernels, [dog])


def test_species_parameter_constructor_rejects_invalid_emission_scale():
    model = reference_osteosarcoma_hsmm()
    human = model.species_parameters[Species.HUMAN]
    bad_sds = np.array(human.emission_sds, copy=True)
    bad_sds[0, 0] = 0
    with pytest.raises(ValueError, match="finite and positive"):
        SpeciesParameters(
            species=human.species,
            observation_names=human.observation_names,
            initial_probabilities=human.initial_probabilities,
            base_transition_logits=human.base_transition_logits,
            duration_hazards=human.duration_hazards,
            emission_means=human.emission_means,
            emission_sds=bad_sds,
        )
