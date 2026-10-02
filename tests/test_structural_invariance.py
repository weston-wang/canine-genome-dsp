import numpy as np
import pytest

from canine_dsp.structural_invariance import (
    PREMISE_STATUS,
    RAMP_WINDOW_RESIDUAL,
    margins_under_vaccine,
    run_invariance_suite,
    sample_random_model,
    threshold_for_model,
)


def test_random_models_are_genuinely_different_not_variations_on_the_shipped_one():
    """The invariance test is worthless if the sampled models cluster near this repo's own
    parameterization -- the ranges must produce materially different diseases."""
    rng = np.random.default_rng(3)
    models = [sample_random_model(rng) for _ in range(200)]
    growths = np.array([m.growth[1:4] for m in models]).ravel()
    assert growths.min() < 0.02 and growths.max() > 0.13     # spans the full declared range
    hills = np.array([m.hill for m in models])
    assert hills.min() < 1.0 and hills.max() > 2.5
    # every sampled model must still be structurally valid (5 clones, immune escape last)
    for m in models[:20]:
        assert len(m.growth) == 5
        assert m.growth[4] <= m.growth[1]        # immune escape carries a fitness penalty


def test_threshold_is_computed_from_the_model_not_asserted():
    rng = np.random.default_rng(5)
    model = sample_random_model(rng)
    info = threshold_for_model(model, 246.0)
    # the threshold must be the max over vaccine-COVERED clones only: not clone 0, not immune escape
    assert info["threshold"] == pytest.approx(float(np.max(info["covered_margins"])))
    assert len(info["covered_margins"]) == 3


def test_vaccine_above_threshold_drives_every_covered_clone_negative_across_random_models():
    """The core claim, and the reason this module exists: the durability conclusion is arithmetic
    given its premises, not a property of the illustrative numbers. A pass rate below 1.0 would mean
    the conclusion is tuned."""
    report = run_invariance_suite(n_trials=800, seed=11)
    assert report["pass_rate"] == 1.0
    assert report["n_failures"] == 0
    assert report["n_applicable"] > 700


def test_the_threshold_value_itself_is_parameter_dependent_even_though_the_conditional_is_not():
    """The distinction that keeps this honest: 0.058/day is specific to this repo's growth rates and
    must not be quoted as a general number. What generalizes is the inequality, not its value."""
    report = run_invariance_suite(n_trials=800, seed=11)
    low, high = report["threshold_range_across_random_models"]
    assert high / low > 5.0                  # the threshold varies severalfold across models
    assert "parameter-dependent" in report["interpretation"]


def test_immune_escape_stays_uncovered_by_construction_in_nearly_every_model():
    """The one route no vaccine potency covers. If this ever came back low, the invariance result
    would be resting on the escape clone being accidentally suppressed rather than on the covered
    clones being genuinely reversed."""
    report = run_invariance_suite(n_trials=800, seed=11)
    assert report["immune_escape_uncovered_rate"] > 0.95


def test_margins_under_vaccine_excludes_the_immune_escape_clone():
    rng = np.random.default_rng(9)
    model = sample_random_model(rng)
    no_vaccine = margins_under_vaccine(model, 246.0, 0.0)
    with_vaccine = margins_under_vaccine(model, 246.0, 0.05)
    # every covered clone's margin must drop by exactly the vaccine kill; the last must not move
    np.testing.assert_allclose(no_vaccine[:-1] - with_vaccine[:-1], 0.05, atol=1e-9)
    assert with_vaccine[-1] == pytest.approx(no_vaccine[-1])


def test_premise_status_separates_supported_from_unmeasured():
    """Parameter-invariance makes the CONDITIONAL trustworthy and says nothing about the premises.
    The module must keep those separate, and must not mark the unmeasured ones as supported."""
    assert "SUPPORTED" in PREMISE_STATUS["premise_1_covers_every_resistance_route"]["status"]
    assert "UNMEASURED" in PREMISE_STATUS["premise_3_exceeds_the_threshold"]["status"]
    assert "UNMEASURED" in PREMISE_STATUS["prior_premise_a_targetable_driver_exists"]["status"]
    for premise in PREMISE_STATUS.values():
        assert premise["residual_risk"]      # nothing is allowed to be risk-free


def test_ramp_window_residual_is_recorded_as_a_schedule_lever_not_a_parameter_sensitivity():
    """The honest imperfection: the deterministic condition is exact, the stochastic outcome is not
    quite, and the gap is the pre-vaccine interval rather than parameter tuning -- which makes
    vaccine_start_day an actionable lever. Recorded so the 100% margin pass rate is not read as a
    claim of 100% simulated durability."""
    assert "pre-vaccine" in RAMP_WINDOW_RESIDUAL["finding"]
    assert "0.883" in RAMP_WINDOW_RESIDUAL["evidence"]
    assert "vaccine_start_day" in RAMP_WINDOW_RESIDUAL["actionable_consequence"]
    assert RAMP_WINDOW_RESIDUAL["caveat"]
