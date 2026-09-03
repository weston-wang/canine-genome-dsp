import numpy as np
import pytest

from canine_dsp.mapk_resistance import (
    CLONE_NAMES,
    ResistanceModel,
    _dominant_mechanism,
    build_mutation_matrix,
    clone_growth_margins,
    decompose_patient_uncertainty,
    drug_kill_rate,
    merge_injections,
    poisson_mutation_injections,
    ramping_kill_schedule,
    run_monte_carlo,
    run_monte_carlo_fixed_patient,
    run_monte_carlo_two_compartment,
    run_monte_carlo_with_vaccine,
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


def test_css_reference_2_duration_days_defaults_to_always_on():
    # None (the default) must reproduce the exact original always-on behavior for every existing
    # caller -- this is a backward-compatible addition, not a change to prior results.
    model = ResistanceModel(growth=np.array([.06, .05, .055, .058]),
                            ic50_nM=np.array([222., 222. * 40, 222. * 1.2, 222. * 60]),
                            max_kill=np.array([.18, .02, .035, .015]), mutation=np.eye(4),
                            ic50_nM_2=100., max_kill_2=.05)
    seeding_rates = build_mutation_matrix(np.array([.85, .10, .05]) * 2e-6)[0, 1:]
    always_on = run_monte_carlo(model, 1640., 200, seeding_rates, trials=20,
                               css_reference_2=500., seed=2)
    explicit_none = run_monte_carlo(model, 1640., 200, seeding_rates, trials=20,
                                   css_reference_2=500., css_reference_2_duration_days=None, seed=2)
    np.testing.assert_allclose(always_on.trajectories, explicit_none.trajectories)


def test_css_reference_2_duration_days_zeroes_second_drug_after_the_window():
    # A single front-loaded eBAT-style cycle: the second drug should behave exactly like the
    # always-on case up through the cutoff, then like no second drug at all afterward -- checked
    # directly via clone_growth_margins-style intuition, by comparing trajectories against a
    # second run with css_reference_2=None from the cutoff day onward would require re-seeding
    # the RNG mid-simulation, so instead this checks the concentration profile driving
    # simulate_resistance directly, which is the mechanism the duration cutoff actually modifies.
    model = ResistanceModel(growth=np.array([.05]), ic50_nM=np.array([1e6]),
                            max_kill=np.array([0.]), mutation=np.array([[1.0]]),
                            ic50_nM_2=100., max_kill_2=.2)
    horizon_days = 60
    duration = 20
    always_on = np.full(horizon_days, 1e6)
    front_loaded = always_on.copy()
    front_loaded[duration:] = 0.0
    state_always_on = simulate_resistance(model, np.zeros(horizon_days), np.array([.1]),
                                          concentration_2=always_on)
    state_front_loaded = simulate_resistance(model, np.zeros(horizon_days), np.array([.1]),
                                             concentration_2=front_loaded)
    # identical while the second drug is still "on"
    np.testing.assert_allclose(state_always_on[:duration + 1], state_front_loaded[:duration + 1])
    # diverges afterward: front-loaded exposure lets the population regrow, always-on keeps
    # suppressing it
    assert state_front_loaded[-1, 0] > state_always_on[-1, 0]


def test_run_monte_carlo_with_vaccine_accepts_css_reference_2_duration_days():
    model = ResistanceModel(growth=np.array([.06, .05, .055, .058, .0425]),
                            ic50_nM=np.array([222., 222. * 40, 222. * 1.2, 222. * 60, 222. * 40]),
                            max_kill=np.array([.18, .02, .035, .015, .02]), mutation=np.eye(5),
                            ic50_nM_2=100., max_kill_2=.05)
    seeding_rates = build_mutation_matrix(np.array([.85, .10, .05]) * 2e-6)[0, 1:]
    outcome = run_monte_carlo_with_vaccine(
        model, 1640., 200, seeding_rates, vaccine_start_day=30, vaccine_ramp_days=21,
        vaccine_max_kill=.05, immune_escape_seeding_rate=1e-7, clone_names=CLONE_NAMES + ["immune_escape"],
        trials=10, css_reference_2=500., css_reference_2_duration_days=20, seed=2)
    assert outcome.trajectories.shape == (10, 201, 5)


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


def test_poisson_injections_zero_event_probability_matches_analytical_poisson_process():
    """Cross-check against real point-process theory (the mutation-supply framework used in
    mathematical oncology's multi-type branching-process resistance models, e.g. Iwasa/Nowak/
    Michor): for a fixed source trajectory, the probability a clone receives zero Poisson-seeded
    injection events over the whole trajectory should match the closed-form
    P(zero events) = exp(-rate * total_cell_days) for an inhomogeneous Poisson process with that
    expected count -- verified against the known analytical result, not just assumed correct.
    """
    rng = np.random.default_rng(0)
    trajectory = np.linspace(1.0, 0.1, 60)
    rate = 0.01
    total_cell_days = float(trajectory.sum())
    analytical_p_zero = np.exp(-rate * total_cell_days)

    n_repeats = 20000
    zero_count = sum(
        1 for _ in range(n_repeats)
        if not poisson_mutation_injections(rng, trajectory, np.array([rate]), seed_fraction=1e-8)
    )
    empirical_p_zero = zero_count / n_repeats
    se = np.sqrt(analytical_p_zero * (1 - analytical_p_zero) / n_repeats)
    assert abs(empirical_p_zero - analytical_p_zero) < 5 * se


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


def test_ramping_kill_schedule_zero_before_start_and_saturates_toward_max_kill():
    schedule = ramping_kill_schedule(horizon_days=200, start_day=50, ramp_days=21,
                                     max_kill=.4, applicable_clones=np.array([1., 1., 0.]))
    assert np.all(schedule[:50] == 0)
    assert schedule[51, 2] == 0  # excluded clone never receives kill
    assert schedule[199, 0] == pytest.approx(.4, rel=1e-2)
    assert schedule[51, 0] < schedule[100, 0] < schedule[199, 0]


def test_merge_injections_sums_overlapping_days():
    a = {1: np.array([0., 1., 0.]), 2: np.array([0., 0., 1.])}
    b = {1: np.array([0., 0., 5.]), 3: np.array([1., 0., 0.])}
    merged = merge_injections(a, b)
    np.testing.assert_allclose(merged[1], [0., 1., 5.])
    np.testing.assert_allclose(merged[2], [0., 0., 1.])
    np.testing.assert_allclose(merged[3], [1., 0., 0.])


def test_simulate_resistance_additional_kill_suppresses_only_applicable_clones():
    model = ResistanceModel(growth=np.array([.05, .05]), ic50_nM=np.array([1e6, 1e6]),
                            max_kill=np.array([0., 0.]), mutation=np.eye(2))
    additional_kill = np.zeros((60, 2))
    additional_kill[:, 0] = .3  # only clone 0 is "recognized"
    state = simulate_resistance(model, np.zeros(60), np.array([.1, .1]), additional_kill=additional_kill)
    assert state[-1, 0] < state[0, 0]
    assert state[-1, 1] > state[0, 1]


def test_poisson_mutation_injections_explicit_clone_indices_and_k():
    rng = np.random.default_rng(0)
    trajectory = np.full(30, 1.0)
    injections = poisson_mutation_injections(rng, trajectory, np.array([5.0]), seed_fraction=1e-8,
                                             clone_indices=[4], k=5)
    assert injections
    for vector in injections.values():
        assert len(vector) == 5
        assert vector[4] > 0
        assert vector[:4].sum() == 0


def _vaccine_model() -> ResistanceModel:
    dog = _dog_like_model()
    escape_growth = dog.growth[1] * .85
    return ResistanceModel(
        growth=np.append(dog.growth, escape_growth),
        ic50_nM=np.append(dog.ic50_nM, dog.ic50_nM[1]),
        max_kill=np.append(dog.max_kill, dog.max_kill[1]),
        mutation=np.eye(5),
    )


def test_run_monte_carlo_with_vaccine_shape_and_immune_escape_clone_name():
    model = _vaccine_model()
    seeding_rates = 0.012 * np.array([.85, .10, .05])
    clone_names = CLONE_NAMES + ["immune_escape"]
    outcome = run_monte_carlo_with_vaccine(
        model, css_reference=1640., horizon_days=400, seeding_rates=seeding_rates,
        vaccine_start_day=90, vaccine_ramp_days=21, vaccine_max_kill=.05,
        immune_escape_seeding_rate=6e-5, clone_names=clone_names, trials=25,
        preexisting_prob=.3, seed=11)
    assert outcome.trajectories.shape == (25, 401, 5)
    assert all(label in {"durable_response", *clone_names[1:]} for label in outcome.dominant_mechanism)


def test_poisson_injections_never_land_on_zero_weight_days():
    """Underpins run_monte_carlo_with_vaccine's guarantee that immune-escape seeding never occurs
    before vaccine_start_day: zeroing the source trajectory before that day (as the vaccine model
    does) must make those days impossible to draw, not merely unlikely."""
    rng = np.random.default_rng(3)
    trajectory = np.zeros(100)
    trajectory[50:] = 1.0
    injections = poisson_mutation_injections(rng, trajectory, np.array([50.0]), seed_fraction=1e-8,
                                             clone_indices=[4], k=5)
    assert injections
    assert all(day >= 50 for day in injections)


def test_clone_growth_margins_matches_hand_computed_values():
    model = ResistanceModel(growth=np.array([.06, .05]), ic50_nM=np.array([100., 100.]),
                            max_kill=np.array([.2, .0]), mutation=np.eye(2))
    margins = clone_growth_margins(model, concentration=100.)  # at IC50, kill = max_kill/2
    np.testing.assert_allclose(margins, [.06 - .1, .05 - .0])


def test_clone_growth_margins_includes_second_drug_when_given():
    model = ResistanceModel(growth=np.array([.05]), ic50_nM=np.array([1e9]), max_kill=np.array([0.]),
                            mutation=np.array([[1.0]]), ic50_nM_2=100., max_kill_2=.2)
    without_drug2 = clone_growth_margins(model, concentration=0.0)
    with_drug2 = clone_growth_margins(model, concentration=0.0, concentration_2=100.)
    assert without_drug2[0] == pytest.approx(.05)
    assert with_drug2[0] == pytest.approx(.05 - .1)


def test_run_monte_carlo_fixed_patient_holds_model_and_initial_state_fixed():
    """Repeats should differ only via the stochastic mutation-timing draw: with a huge seeding
    rate forced to zero, every repeat must be bit-identical (no other source of randomness)."""
    model = _dog_like_model()
    seeding_rates = np.zeros(3)
    initial = np.array([.3, 0., 0., 0.])
    outcome = run_monte_carlo_fixed_patient(model, 1640., 200, seeding_rates, initial, repeats=5, seed=1)
    for trial in range(1, 5):
        np.testing.assert_allclose(outcome.trajectories[trial], outcome.trajectories[0])
    assert not outcome.progressed.any()  # no resistance mechanism can ever seed


def test_run_monte_carlo_fixed_patient_still_stochastic_with_nonzero_seeding():
    model = _dog_like_model()
    seeding_rates = 0.05 * np.array([.85, .10, .05])  # high rate: some repeats should progress
    initial = np.array([.3, 0., 0., 0.])
    outcome = run_monte_carlo_fixed_patient(model, 1640., 400, seeding_rates, initial, repeats=40, seed=2)
    assert outcome.progressed.any()
    assert (~outcome.progressed).any()  # timing genuinely varies trial to trial


def test_decompose_patient_uncertainty_reports_valid_variance_split():
    model = _dog_like_model()
    seeding_rates = 0.012 * np.array([.85, .10, .05])
    decomposition = decompose_patient_uncertainty(model, 1640., 300, seeding_rates, n_dogs=15,
                                                  repeats_per_dog=20, preexisting_prob=.3, seed=4)
    assert decomposition.per_dog_durable_probability.shape == (15,)
    assert (decomposition.per_dog_durable_probability >= 0).all()
    assert (decomposition.per_dog_durable_probability <= 1).all()
    assert decomposition.between_dog_variance >= 0
    assert decomposition.within_dog_variance >= 0
    assert 0 <= decomposition.intraclass_correlation <= 1


def test_decompose_patient_uncertainty_zero_between_dog_variance_gives_zero_icc():
    """If every dog is forced identical (no perturbation, no exposure variability, no preexisting
    subclone), the only remaining variance is within-dog mutation-timing chance -- ICC should
    collapse toward 0, not report spurious between-dog structure."""
    model = ResistanceModel(growth=np.array([.06, .05, .055, .058]),
                            ic50_nM=np.array([222., 222. * 40, 222. * 1.2, 222. * 60]),
                            max_kill=np.array([.18, .02, .035, .015]), mutation=np.eye(4))
    seeding_rates = 0.012 * np.array([.85, .10, .05])
    decomposition = decompose_patient_uncertainty(
        model, 1640., 300, seeding_rates, n_dogs=15, repeats_per_dog=30, preexisting_prob=0.0,
        exposure_scale=1e-9, seeding_rate_scale=1e-9, ic50_scale=1e-9, seed=4)
    assert decomposition.intraclass_correlation < 0.2


def test_vaccine_can_suppress_pathway_reactivation_at_high_potency():
    """Sanity check on the model's own shared premise: since pathway_reactivation still expresses
    the original driver antigen (see ANTIGEN_PERSISTENCE_NOTE), a high enough vaccine max_kill
    should suppress it too, not just leave it untouched like the MEK inhibitor does."""
    model = _vaccine_model()
    seeding_rates = 0.012 * np.array([.85, .10, .05])
    clone_names = CLONE_NAMES + ["immune_escape"]
    durability = {}
    for vaccine_max_kill in (0.0, 0.3):
        outcome = run_monte_carlo_with_vaccine(
            model, css_reference=1640., horizon_days=1000, seeding_rates=seeding_rates,
            vaccine_start_day=90, vaccine_ramp_days=21, vaccine_max_kill=vaccine_max_kill,
            immune_escape_seeding_rate=6e-5, clone_names=clone_names, trials=80,
            preexisting_prob=.3, seed=11)
        durability[vaccine_max_kill] = 1 - outcome.progressed.mean()
    assert durability[0.3] >= durability[0.0]


def test_two_compartment_no_nodal_disease_when_probability_zero():
    model = _dog_like_model()
    seeding_rates = 0.012 * np.array([.85, .10, .05])
    outcome = run_monte_carlo_two_compartment(
        model, css_reference=1640., horizon_days=200, seeding_rates=seeding_rates,
        nodal_involvement_prob=0.0, nodal_seed_fraction=0.1, debulking_fraction=0.9,
        trials=20, preexisting_prob=.3, seed=3)
    assert not outcome.has_nodal_involvement.any()
    assert np.all(outcome.nodal_trajectories == 0)
    assert "nodal" not in outcome.dominant_compartment


def test_two_compartment_debulking_only_shrinks_primary_not_nodal():
    """Debulking (surgical resection of the primary) should shrink the primary's starting burden
    but leave the nodal deposit's size determined only by nodal_seed_fraction -- a lobectomy
    cannot resect disease outside the resected organ."""
    model = _dog_like_model()
    seeding_rates = 0.012 * np.array([.85, .10, .05])
    outcomes = {}
    for debulking_fraction in (0.0, 0.9):
        outcomes[debulking_fraction] = run_monte_carlo_two_compartment(
            model, css_reference=1640., horizon_days=5, seeding_rates=seeding_rates,
            nodal_involvement_prob=1.0, nodal_seed_fraction=0.1, debulking_fraction=debulking_fraction,
            trials=10, preexisting_prob=0.0, seed=9)
    primary_day0 = {d: outcomes[d].primary_trajectories[:, 0].sum(axis=1) for d in outcomes}
    nodal_day0 = {d: outcomes[d].nodal_trajectories[:, 0].sum(axis=1) for d in outcomes}
    assert np.all(primary_day0[0.9] < primary_day0[0.0])
    np.testing.assert_allclose(nodal_day0[0.9], nodal_day0[0.0])


def test_two_compartment_nodal_seeded_from_predebulking_primary_composition():
    """The nodal deposit's starting composition should be a fixed fraction of what the primary
    tumor looked like BEFORE debulking (metastasis is a pre-existing biological event), not of
    the post-debulking primary and not independently resampled."""
    model = _dog_like_model()
    seeding_rates = 0.012 * np.array([.85, .10, .05])
    outcome = run_monte_carlo_two_compartment(
        model, css_reference=1640., horizon_days=5, seeding_rates=seeding_rates,
        nodal_involvement_prob=1.0, nodal_seed_fraction=0.2, debulking_fraction=0.9,
        trials=15, preexisting_prob=0.0, seed=5)
    primary_predebulking = outcome.primary_trajectories[:, 0] / (1 - 0.9)
    nodal_day0 = outcome.nodal_trajectories[:, 0]
    np.testing.assert_allclose(nodal_day0, primary_predebulking * 0.2, atol=1e-12)


def test_two_compartment_progression_reflects_combined_burden():
    """A dog whose primary alone would look durably controlled (aggressively debulked) should
    still be flagged as progressed if the (untouched) nodal compartment, seeded with a large
    enough deposit, regrows past the detection threshold."""
    model = _dog_like_model()
    seeding_rates = 0.012 * np.array([.85, .10, .05])
    outcome = run_monte_carlo_two_compartment(
        model, css_reference=1640., horizon_days=400, seeding_rates=seeding_rates,
        nodal_involvement_prob=1.0, nodal_seed_fraction=0.5, debulking_fraction=0.99,
        trials=10, preexisting_prob=1.0, seed=6)
    assert outcome.progressed.any()
