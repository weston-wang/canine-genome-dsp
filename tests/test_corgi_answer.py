import numpy as np
import pytest

from canine_dsp.antigen_convergence import vaccine_potency_threshold
from canine_dsp.mapk_resistance import run_monte_carlo_two_compartment
from canine_dsp.mapk_scenarios import (
    CCNU_EXPOSURE_DAYS,
    CCNU_MATCHED_CSS_NM,
    IMMUNE_ESCAPE_SEEDING_RATE,
    NODAL_SEED_FRACTION,
    VACCINE_CLONE_NAMES,
    VACCINE_RAMP_DAYS,
    VACCINE_START_DAY,
    _PULMONARY_BASELINE_BURDEN,
    corgi_full_regimen_scenarios,
    pulmonary_corgi_scenarios,
)


def test_two_compartment_vaccine_defaults_preserve_exact_prior_behaviour():
    """The engine upgrade must not perturb any existing caller, including RNG draw order -- the same
    discipline applied when css_reference_2_duration_days was added. Checked against the 4-clone
    Corgi scenario, which is what the pre-upgrade callers use."""
    model, css, rates, debulk, _ = pulmonary_corgi_scenarios(
        nodal_involvement_prob_values=[0.4])[0.4]
    kwargs = dict(nodal_involvement_prob=0.4, nodal_seed_fraction=NODAL_SEED_FRACTION,
                  debulking_fraction=debulk, trials=60, preexisting_prob=0.30,
                  initial_burden=_PULMONARY_BASELINE_BURDEN, seed=7)
    baseline = run_monte_carlo_two_compartment(model, css, 365, rates, **kwargs)
    # explicitly passing the vaccine-off defaults must be byte-identical
    explicit = run_monte_carlo_two_compartment(model, css, 365, rates, vaccine_start_day=None,
                                               vaccine_max_kill=0.0, **kwargs)
    np.testing.assert_array_equal(baseline.progressed, explicit.progressed)
    np.testing.assert_allclose(baseline.primary_trajectories, explicit.primary_trajectories)
    np.testing.assert_allclose(baseline.nodal_trajectories, explicit.nodal_trajectories)


def test_corgi_five_clone_scenario_is_vaccine_capable_and_pulmonary():
    """pulmonary_corgi_scenarios is 4-clone and therefore cannot express a vaccine at all -- which is
    how the Corgi arm came to be built as monotherapy. This is the fix, and it must stay on the
    pulmonary preset (full systemic exposure, no brain-penetration discount)."""
    model, css, rates, debulk, provenance = corgi_full_regimen_scenarios(
        ccnu_max_kill=0.08, nodal_involvement_prob_values=[0.4])[0.4]
    assert len(model.growth) == len(VACCINE_CLONE_NAMES) == 5
    assert provenance["second_drug"] == "lomustine (CCNU)"
    assert provenance["second_drug_exposure_days"] == CCNU_EXPOSURE_DAYS
    assert "pulmonary" in provenance["site"]
    assert model.max_kill_2 == pytest.approx(0.08)
    # the 5th clone inherits pathway_reactivation's drug susceptibility with a growth penalty
    assert model.growth[4] < model.growth[1]
    assert model.ic50_nM[4] == pytest.approx(model.ic50_nM[1])
    # a 4-clone caller must still get no second drug when ccnu_max_kill is 0
    plain = corgi_full_regimen_scenarios(nodal_involvement_prob_values=[0.4])[0.4][0]
    assert plain.max_kill_2 is None


def _durable(vaccine_max_kill, nodal_prob, preexisting_prob, horizon=1825, trials=120):
    model, css, rates, debulk, _ = corgi_full_regimen_scenarios(
        ccnu_max_kill=0.08, nodal_involvement_prob_values=[nodal_prob])[nodal_prob]
    outcome = run_monte_carlo_two_compartment(
        model, css, horizon, rates, nodal_involvement_prob=nodal_prob,
        nodal_seed_fraction=NODAL_SEED_FRACTION, debulking_fraction=debulk, trials=trials,
        preexisting_prob=preexisting_prob, initial_burden=_PULMONARY_BASELINE_BURDEN,
        css_reference_2=CCNU_MATCHED_CSS_NM, css_reference_2_duration_days=CCNU_EXPOSURE_DAYS,
        vaccine_start_day=VACCINE_START_DAY, vaccine_ramp_days=VACCINE_RAMP_DAYS,
        vaccine_max_kill=vaccine_max_kill,
        immune_escape_seeding_rate=IMMUNE_ESCAPE_SEEDING_RATE,
        clone_names=VACCINE_CLONE_NAMES, seed=7)
    return float(1 - outcome.progressed.mean())


def test_vaccine_reaches_the_compartment_surgery_cannot():
    """The mechanistically important asymmetry for the Corgi presentation: debulking cannot touch the
    nodal compartment, but every systemic mechanism can. With guaranteed nodal disease the vaccine
    must still deliver a large improvement -- if it did not, the vaccine would be being applied to the
    primary only, which would be a modeling bug rather than a finding."""
    off = _durable(0.0, nodal_prob=1.0, preexisting_prob=0.62)
    on = _durable(0.08, nodal_prob=1.0, preexisting_prob=0.62)
    assert on - off > 0.3
    assert on > 0.85


def test_threshold_result_survives_the_corgi_two_compartment_structure():
    """The whole endurance claim for a Corgi: above the vaccine potency threshold the outcome stops
    depending on preexisting_prob -- the parameter no assay can measure -- even with undebulked nodal
    disease present. Verified in the two-compartment engine rather than inherited from the
    single-compartment BMD result."""
    model = corgi_full_regimen_scenarios(
        ccnu_max_kill=0.08, nodal_involvement_prob_values=[0.6])[0.6][0]
    threshold = vaccine_potency_threshold(
        np.asarray(model.growth), VACCINE_CLONE_NAMES)["threshold_vaccine_max_kill"]

    below_spread = abs(_durable(0.0, 0.6, 0.30) - _durable(0.0, 0.6, 0.62))
    above_spread = abs(_durable(threshold, 0.6, 0.30) - _durable(threshold, 0.6, 0.62))
    assert below_spread > 0.15      # vaccine off: dominated by the unmeasurable parameter
    assert above_spread < 0.06      # above threshold: dependence essentially gone
    assert above_spread < below_spread


def test_nodal_involvement_barely_matters_above_threshold_but_does_below():
    """The Corgi-specific risk is real in the regime where the regimen is nearly working, and
    essentially absent once potency clears the threshold. Both halves matter: if nodal disease were
    irrelevant everywhere, the two-compartment model would be pointless."""
    threshold = vaccine_potency_threshold(
        np.asarray(corgi_full_regimen_scenarios(
            ccnu_max_kill=0.08, nodal_involvement_prob_values=[0.0])[0.0][0].growth),
        VACCINE_CLONE_NAMES)["threshold_vaccine_max_kill"]
    above_none = _durable(threshold, 0.0, 0.62)
    above_all = _durable(threshold, 1.0, 0.62)
    assert abs(above_none - above_all) < 0.08     # above threshold: nodal disease nearly irrelevant
    assert above_all > 0.85
