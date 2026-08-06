import numpy as np
import pytest

from canine_dsp.mapk_resistance import MonteCarloOutcome
from canine_dsp.pharmacology import CCNU_CANINE_HS, CYTOTOXIC, cumulative_dose_limited_days
from canine_dsp.single_patient import (
    CANINE_HS_DRIVER_FREQUENCY,
    CORGI_PULMONARY_HS_BENCHMARK,
    LOCALIZED_HS_CCNU_BENCHMARK,
    SEQUENCING_ASSAYS,
    detectable_prior_mass,
    driver_conditioned_arms,
    genome_equivalents_required,
    implied_preexisting_prob,
    partition_by_preexisting_subclone,
    partition_two_compartment_by_preexisting_subclone,
    posterior_preexisting_prob,
    spatial_detection_probability,
    vaf_lod_to_cell_fraction,
)


def test_vaf_floor_converts_to_a_cell_fraction_floor_twice_as_large():
    """The direction of this conversion is load-bearing: getting it backwards would make every
    assay look twice as sensitive as it is, which is exactly the error that would rescue the
    "sequence the tumor to rule out resistance" conclusion."""
    assert vaf_lod_to_cell_fraction(0.01) == pytest.approx(0.02)
    # a copy-amplified or homozygous variant sits higher in VAF for the same cell fraction
    assert vaf_lod_to_cell_fraction(0.01, mutant_copies=2) == pytest.approx(0.01)
    for bad in (0.0, 1.0, -0.1):
        with pytest.raises(ValueError):
            vaf_lod_to_cell_fraction(bad)


def test_detectable_prior_mass_is_computed_in_log_space_not_linear_space():
    """The prior is log-uniform, so the detectable fraction is a ratio of log-widths. Linear
    reasoning would say a 1e-4 floor sees ~90% of a [1e-6, 1e-3] range; in log terms it sees a
    third, and that difference is the whole result."""
    assert detectable_prior_mass(1e-4, -6, -3) == pytest.approx(1 / 3)
    assert detectable_prior_mass(1e-3, -6, -3) == 0.0      # floor at the top of the prior
    assert detectable_prior_mass(1e-2, -6, -3) == 0.0      # floor above the entire prior
    assert detectable_prior_mass(1e-7, -6, -3) == 1.0      # floor below the entire prior
    with pytest.raises(ValueError):
        detectable_prior_mass(1e-4, -3, -6)


def test_negative_sequencing_leaves_preexisting_prob_untouched_for_every_clinical_assay():
    """The central negative result of the module: every assay a clinician can actually order has a
    floor above the model's entire pre-existing-subclone size prior, so a negative result carries
    exactly zero information. This must be asserted, not merely described in prose, because it is
    the claim most likely to be softened by accident later."""
    clinical = [name for name, a in SEQUENCING_ASSAYS.items()
                if a["clinically_available_for_dogs"]]
    assert clinical, "the panel must contain at least one clinically available assay to test"
    for name in clinical:
        lod = vaf_lod_to_cell_fraction(SEQUENCING_ASSAYS[name]["vaf_lod"])
        update = posterior_preexisting_prob(0.30, lod)
        assert update["detectable_prior_mass"] == 0.0
        assert update["posterior"] == pytest.approx(0.30)
        assert update["fold_reduction"] == pytest.approx(1.0)


def test_best_research_assay_shrinks_but_does_not_resolve_preexisting_prob():
    lod = vaf_lod_to_cell_fraction(SEQUENCING_ASSAYS["duplex_research_best"]["vaf_lod"])
    update = posterior_preexisting_prob(0.30, lod)
    assert 0 < update["detectable_prior_mass"] < 1
    assert update["posterior"] < 0.30            # it does help
    assert update["posterior"] > 0.15            # but nowhere near resolving it
    assert 1.0 < update["fold_reduction"] < 2.0


def test_posterior_is_monotone_in_assay_sensitivity_and_respects_bounds():
    lods = [vaf_lod_to_cell_fraction(v) for v in (0.02, 1e-3, 1e-4, 3.1e-5)]
    posteriors = [posterior_preexisting_prob(0.30, lod)["posterior"] for lod in lods]
    assert posteriors == sorted(posteriors, reverse=True)   # better assay -> lower posterior
    assert posterior_preexisting_prob(0.0, 1e-9)["posterior"] == 0.0
    with pytest.raises(ValueError):
        posterior_preexisting_prob(1.5, 1e-4)


def test_input_dna_is_not_the_binding_constraint():
    """Distinguishing the three independent walls matters: if DNA input were the limit, a bigger
    biopsy would fix it. It is not -- seeing a 1e-6 subclone needs tens of micrograms, which a
    resection can yield, so the real limits are the error floor and spatial sampling."""
    required = genome_equivalents_required(1e-6)
    assert required["genome_equivalents"] > 1e6
    assert required["dna_input_ug"] < 100      # achievable from a surgical specimen
    assert genome_equivalents_required(1e-3)["dna_input_ug"] < 1
    with pytest.raises(ValueError):
        genome_equivalents_required(0.0)


def test_spatial_sampling_bounds_diverge_by_orders_of_magnitude():
    """Well-mixed and single-focus are not a technicality -- they bracket near-certain detection
    against detection at the sampled-volume fraction, and which regime holds is unmeasured. The
    spread is why a negative result cannot be interpreted."""
    result = spatial_detection_probability(1e-6, tumor_cells=1e10, sampled_cells=1e8)
    assert result["probability_if_well_mixed"] > 0.99
    assert result["probability_if_single_focus"] == pytest.approx(0.01)
    with pytest.raises(ValueError):
        spatial_detection_probability(1e-6, tumor_cells=1e6, sampled_cells=1e9)


def test_driver_conditioning_reports_the_real_cohort_split_not_a_certainty():
    """The model has always assumed the MEK inhibitor engages a driver. Real canine HS sequencing
    says that holds for well under two thirds of BMD cases, and this must surface as a two-arm
    conditioning rather than a discount factor on one arm."""
    arms = driver_conditioned_arms(breed="bmd")
    assert arms["probability_mapk_driver_identified"] == pytest.approx(44 / 96)
    assert arms["probability_mapk_driver_identified"] < 0.5
    assert (arms["probability_mapk_driver_identified"]
            + arms["probability_no_mapk_driver_identified"]) == pytest.approx(1.0)
    bmd = CANINE_HS_DRIVER_FREQUENCY["bmd"]
    assert bmd["PTPN11"] + bmd["KRAS"] == pytest.approx(44 / 96)


def test_driver_conditioning_refuses_to_apply_bmd_frequency_to_a_corgi():
    """The regression this test guards against is a real mistake this module made once: presenting
    BMD driver frequency as though it were generically informative for 'one sequenced dog'. Corgi
    HS is a separately-published, clinically distinct presentation with zero sequenced cases, so
    breed='corgi' must return an explicit unknown rather than a borrowed number."""
    corgi = driver_conditioned_arms(breed="corgi")
    assert corgi["probability_mapk_driver_identified"] is None
    assert "no published canine HS driver sequencing exists" in corgi["source"]
    assert "category error" in corgi["do_not_borrow_bmd_frequency"]
    # flat-coated retriever is a real tumor-scenario preset elsewhere in this repo (its own GWAS
    # germline locus) but was never in Takada et al.'s sequenced cohort either -- this must return
    # the same "no data" branch as corgi, generically, not raise or silently borrow BMD's number.
    flat_coated = driver_conditioned_arms(breed="flat_coated_retriever")
    assert flat_coated["probability_mapk_driver_identified"] is None


def test_driver_conditioning_golden_retriever_uses_its_own_smaller_cohort():
    arms = driver_conditioned_arms(breed="golden_retriever")
    assert arms["probability_mapk_driver_identified"] == pytest.approx(3 / 13)
    assert arms["cohort_n"] == 13


def _fake_outcome(initial_states, progressed, ttp):
    trajectories = np.zeros((len(initial_states), 3, initial_states.shape[1]))
    trajectories[:, 0, :] = initial_states
    return MonteCarloOutcome(trajectories=trajectories, progressed=np.asarray(progressed),
                             time_to_progression=np.asarray(ttp, dtype=float),
                             dominant_mechanism=["x"] * len(initial_states))


def test_partition_recovers_the_two_patient_types_the_cohort_average_hides():
    """A cohort fraction of 0.5 built from a 100%-durable arm and a 0%-durable arm describes no
    patient at all. Recovering the split from an existing ensemble's day-0 state is what makes the
    N=1 reframing possible without re-simulating anything."""
    initial = np.array([[0.3, 0.0, 0.0, 0.0],      # no pre-existing subclone
                        [0.3, 0.0, 0.0, 0.0],
                        [0.3, 1e-5, 0.0, 0.0],     # pre-existing subclone present
                        [0.3, 0.0, 1e-4, 0.0]])
    outcome = _fake_outcome(initial, [False, False, True, True], [np.nan, np.nan, 200.0, 300.0])
    report = partition_by_preexisting_subclone(outcome)
    assert report["population_durable_response_fraction"] == pytest.approx(0.5)
    assert report["without_preexisting_subclone"]["durable_response_fraction"] == pytest.approx(1.0)
    assert report["with_preexisting_subclone"]["durable_response_fraction"] == pytest.approx(0.0)
    assert report["with_preexisting_subclone"]["n_trials"] == 2
    assert report["spread_attributable_to_preexisting_resistance"] == pytest.approx(1.0)
    assert report["without_preexisting_subclone"]["median_time_to_progression_days"] is None


def test_implied_preexisting_prob_inverts_the_mixture_and_flags_ill_conditioning():
    """When the two arms are far apart the cohort statistic is almost purely a readout of
    preexisting_prob, which is what makes a matched benchmark informative about it. When they are
    close the inversion is meaningless, and that has to be reported rather than returned as a
    confident number."""
    report = implied_preexisting_prob(0.375, durable_without_subclone=1.0,
                                      durable_with_subclone=0.0)
    assert report["implied_preexisting_prob"] == pytest.approx(0.625)
    assert report["in_range"]
    degenerate = implied_preexisting_prob(0.5, 0.8, 0.8)
    assert degenerate["implied_preexisting_prob"] is None
    # out-of-range observations are clipped but flagged, not silently accepted
    clipped = implied_preexisting_prob(1.0, 0.9, 0.0)
    assert clipped["implied_preexisting_prob"] == 0.0
    assert not clipped["in_range"]


def test_matched_benchmark_implies_roughly_double_the_models_central_preexisting_prob():
    """The substantive calibration finding, pinned so it cannot drift: against a benchmark that
    matches on species, disease, presentation and treatment structure, this model is optimistic on
    durable-response fraction by about a factor of two."""
    implied = implied_preexisting_prob(LOCALIZED_HS_CCNU_BENCHMARK["relapse_free_fraction"],
                                      durable_without_subclone=0.99, durable_with_subclone=0.0)
    assert 0.55 < implied["implied_preexisting_prob"] < 0.70
    assert implied["implied_preexisting_prob"] > 2 * 0.30 * 0.9   # ~2x the model's 0.30


def test_the_matched_benchmark_declares_both_its_matches_and_its_mismatches():
    """The COMBI-d/v rejection established that a comparator is only admissible if every axis is
    checked. A benchmark asserting matches without also naming its mismatches would reintroduce
    exactly the failure mode that rejection was meant to prevent."""
    assert len(LOCALIZED_HS_CCNU_BENCHMARK["matches_on"]) == 4
    assert LOCALIZED_HS_CCNU_BENCHMARK["mismatches_on"]
    assert LOCALIZED_HS_CCNU_BENCHMARK["n_dogs"] == 16
    assert LOCALIZED_HS_CCNU_BENCHMARK["relapse_free_fraction"] == pytest.approx(6 / 16)


def test_corgi_benchmark_is_breed_matched_and_tells_a_materially_worse_story():
    """The BMD-context benchmark is explicitly flagged as breed-UNRESOLVED. This one is the only
    breed-matched comparator in the module, and its outcome must not be quietly similar to the BMD
    one -- if it were, there would be no finding here at all."""
    assert CORGI_PULMONARY_HS_BENCHMARK["breed"] == "Pembroke Welsh Corgi (all 19)"
    assert CORGI_PULMONARY_HS_BENCHMARK["n_dogs"] == 19
    assert CORGI_PULMONARY_HS_BENCHMARK["median_survival_days"] == 133
    assert (CORGI_PULMONARY_HS_BENCHMARK["median_survival_days"]
            < LOCALIZED_HS_CCNU_BENCHMARK["median_survival_days"] / 2)
    assert "unresolved on breed" in LOCALIZED_HS_CCNU_BENCHMARK["caveat"].lower()
    assert CORGI_PULMONARY_HS_BENCHMARK["mismatches_on"]


def test_two_compartment_partition_reads_the_primary_compartments_day0_state():
    """`run_monte_carlo_two_compartment` returns a differently-shaped outcome than `run_monte_carlo`
    (primary/nodal trajectories instead of one array), so this needs its own adapter rather than
    silently reusing `partition_by_preexisting_subclone`, which would crash on the missing
    `.trajectories` attribute rather than mis-reading data -- but the adapter's *logic* must still
    match: same split, same interpretation."""
    from canine_dsp.mapk_resistance import TwoCompartmentOutcome

    primary = np.array([[0.3, 0.0, 0.0, 0.0],
                        [0.3, 0.0, 0.0, 0.0],
                        [0.3, 1e-5, 0.0, 0.0]])
    trajectories = np.zeros((3, 2, 4))
    trajectories[:, 0, :] = primary
    outcome = TwoCompartmentOutcome(
        primary_trajectories=trajectories, nodal_trajectories=np.zeros_like(trajectories),
        has_nodal_involvement=np.array([False, False, True]),
        progressed=np.array([False, False, True]),
        time_to_progression=np.array([np.nan, np.nan, 150.0]),
        dominant_mechanism=["x"] * 3, dominant_compartment=["none", "none", "primary"])
    report = partition_two_compartment_by_preexisting_subclone(outcome)
    assert report["without_preexisting_subclone"]["durable_response_fraction"] == pytest.approx(1.0)
    assert report["with_preexisting_subclone"]["durable_response_fraction"] == pytest.approx(0.0)
    assert report["with_preexisting_subclone"]["n_trials"] == 1


def test_single_patient_demo_refuses_to_run_the_bmd_arm_for_a_corgi():
    """The regression this guards: findings 1-4 are BMD-context tumor-scenario code
    (`combination_scenarios`, `ccnu_combination_scenarios`) reused unchanged. Silently accepting
    breed='corgi' here would run the BMD tumor model and merely mislabel its output, which is worse
    than refusing -- a wrong number with the right label looks validated."""
    from pathlib import Path

    from canine_dsp.single_patient_cli import single_patient_demo
    with pytest.raises(ValueError, match="finding_5"):
        single_patient_demo(Path("/tmp/should-not-be-created"), breed="corgi")


def test_lomustine_is_cytotoxic_so_the_cytostatic_ceiling_does_not_bind():
    """The reason lomustine replaces the CDK4/6 inhibitor at all: it is the one candidate whose
    mechanism class permits max_kill above a clone's growth rate."""
    assert CCNU_CANINE_HS["mechanism_class"] == CYTOTOXIC
    assert CCNU_CANINE_HS["overall_response_rate"] == pytest.approx(0.46)
    assert "histiocytic sarcoma" in CCNU_CANINE_HS["citation"]


def test_cumulative_dose_cap_converts_to_the_engines_exposure_duration_parameter():
    """What lomustine gives back for escaping the ceiling: a finite exposure window, derived from
    the real cumulative hepatotoxicity threshold rather than chosen."""
    limit = cumulative_dose_limited_days(70.0, 21.0, 350.0)
    assert limit["cycles_permitted"] == 5
    assert limit["exposure_days"] == 105
    # a lower dose per cycle buys more cycles and a longer window -- the metronomic trade
    assert cumulative_dose_limited_days(35.0, 21.0, 350.0)["exposure_days"] == 210
    for bad in ((0.0, 21.0, 350.0), (70.0, 0.0, 350.0), (70.0, 21.0, 0.0)):
        with pytest.raises(ValueError):
            cumulative_dose_limited_days(*bad)


def test_duration_cap_not_potency_is_what_limits_the_cytotoxic_arm():
    """The model's substantive claim about lomustine, checked end to end: at a potency that clears
    every clone's growth margin, chronic dosing rescues the pre-existing-subclone arm and the real
    duration cap does not. If this ever inverts, the synthesis in the demo is wrong."""
    from canine_dsp.mapk_resistance import clone_growth_margins, run_monte_carlo
    from canine_dsp.mapk_scenarios import (
        CCNU_EXPOSURE_DAYS,
        CCNU_MATCHED_CSS_NM,
        ccnu_combination_scenarios,
    )

    potency = 0.12
    model, css, rates, burden, provenance = ccnu_combination_scenarios(
        max_kill_2_values=[potency])[potency]
    assert provenance["cytostatic_ceiling_applies"] is False
    # the potency genuinely reverses every resistant clone while the drug is present
    margins = clone_growth_margins(model, css, CCNU_MATCHED_CSS_NM)
    assert np.max(margins[1:]) < 0

    def _with_subclone_durable(duration):
        outcome = run_monte_carlo(model, css, 730, rates, trials=120, preexisting_prob=0.5,
                                  initial_burden=burden, css_reference_2=CCNU_MATCHED_CSS_NM,
                                  css_reference_2_duration_days=duration, seed=3)
        return partition_by_preexisting_subclone(
            outcome)["with_preexisting_subclone"]["durable_response_fraction"]

    assert _with_subclone_durable(None) > 0.9              # chronic rescues it
    assert _with_subclone_durable(CCNU_EXPOSURE_DAYS) < 0.3  # the real cap does not
