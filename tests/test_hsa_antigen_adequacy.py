"""Tests for `hsa_antigen_adequacy`.

The module closes a gap the analysis carried for its whole life: it modelled antigen LOSS and never
antigen INADEQUACY. These tests check that the three modes stay distinguished, that the module does
not quietly collapse the unrecoverable mode into the recoverable one, and that the evidence is
recorded with its provenance and its limits rather than as settled fact.
"""
import pytest

from canine_dsp import hsa_antigen_adequacy as ag


# ---------------------------------------------------------------------------------------------
# The three modes.

def test_three_modes_are_distinguished_and_only_one_is_a_height_change():
    modes = ag.THREE_MODES_OF_INADEQUACY
    assert "EXACTLY a reduction in vaccine height" in modes["uniform"]
    assert "NOT a height reduction" in modes["heterogeneous"]
    assert "no amount of extra height fixes it" in modes["heterogeneous"]
    assert "take-rate" in modes["inter_patient"]


def test_the_modes_are_not_treated_as_interchangeable():
    assert "a dial the plan already knows how to turn" in modes_why()
    assert "a floor the plan cannot reach" in modes_why()


def modes_why():
    return ag.THREE_MODES_OF_INADEQUACY["why_the_split_matters"]


# ---------------------------------------------------------------------------------------------
# The one mode that does reduce to arithmetic.

def test_uniform_coverage_scales_height_linearly():
    assert ag.effective_height_uniform(0.042, 1.0) == pytest.approx(0.042)
    assert ag.effective_height_uniform(0.042, 0.5) == pytest.approx(0.021)
    assert ag.effective_height_uniform(0.042, 0.0) == pytest.approx(0.0)


def test_uniform_coverage_rejects_impossible_arguments():
    for bad in (-0.1, 1.1):
        with pytest.raises(ValueError):
            ag.effective_height_uniform(0.042, bad)
    with pytest.raises(ValueError):
        ag.effective_height_uniform(-1.0, 0.5)


def test_full_coverage_is_a_no_op():
    """The identity that makes the uniform mode safe to fold into the existing height grid."""
    for height in (0.030, 0.042, 0.0515):
        assert ag.effective_height_uniform(height, 1.0) == pytest.approx(height)


# ---------------------------------------------------------------------------------------------
# What the evidence does and does not say.

def test_sample_level_positivity_is_not_claimed_as_cell_level_coverage():
    vim = ag.WHAT_IS_MEASURED_IS_SAMPLE_LEVEL["vimentin_and_cd31"]
    assert "all 11 samples" in vim["finding"]
    assert "not 100% of cells" in vim["what_it_does_not_settle"]
    assert "antigen-null subpopulation" in vim["what_it_does_not_settle"]


def test_the_variable_intensity_ambiguity_is_named_rather_than_resolved():
    b7 = ag.WHAT_IS_MEASURED_IS_SAMPLE_LEVEL["b7_h3"]
    assert "VARIABLE LEVELS OF EXPRESSION INTENSITY" in b7["finding"]
    reasoning = b7["why_that_phrase_is_the_whole_problem"]
    assert "uniform mode" in reasoning and "heterogeneous mode" in reasoning
    assert "was not made" in reasoning


def test_the_mixed_histology_is_offered_as_a_reason_not_a_proof():
    mixed = ag.WHAT_IS_MEASURED_IS_SAMPLE_LEVEL["the_tumour_is_definitionally_mixed"]
    assert "MIXTURE" in mixed["finding"]
    assert "not proof of a blind spot" in mixed["why_it_belongs_here"]


def test_the_missing_measurement_is_named_and_is_actionable():
    gap = ag.WHAT_IS_MEASURED_IS_SAMPLE_LEVEL["the_measurement_nobody_has_made"]
    assert "FRACTION OF CELLS" in gap
    assert "biobank" in gap


# ---------------------------------------------------------------------------------------------
# The trial that makes it concrete, and its provenance.

def test_the_vaccs_failure_is_recorded_with_its_design_and_scale():
    v = ag.VACCS_FAILED_ON_THIS_DISEASE_SPECIFICALLY
    assert "38056066" in v["design_citation"]
    assert "INCLUDING hemangiosarcoma" in v["design"]
    assert "Hemangiosarcoma was" in v["reported_outcome"]


def test_the_vaccs_provenance_caveat_is_not_optional():
    """A CEO interview is not a peer-reviewed result and the module has to say so."""
    caveat = ag.VACCS_FAILED_ON_THIS_DISEASE_SPECIFICALLY["the_provenance_caveat"]
    assert "not from a peer-reviewed publication" in caveat
    assert "not established" in caveat


def test_the_failure_is_attributed_to_antigen_choice_not_the_optimised_variables():
    why = ag.VACCS_FAILED_ON_THIS_DISEASE_SPECIFICALLY["why_it_is_decisive_for_this_module"]
    assert "ANTIGEN CHOICE" in why
    for optimised in ("potency", "persistence", "microenvironment"):
        assert optimised in why


# ---------------------------------------------------------------------------------------------
# The pattern across the four HSA vaccine results.

def test_all_four_vaccine_results_carry_antigen_and_outcome():
    trials = {k: v for k, v in ag.COVERAGE_EXPLAINS_WHICH_VACCINES_WORKED.items()
              if isinstance(v, dict)}
    assert len(trials) == 4
    for name, entry in trials.items():
        assert entry["antigen"].startswith(("DEFINED", "POLYVALENT")), name
        assert entry["outcome"], name


def test_the_pattern_is_coverage_not_platform():
    """The tempting reading is defined-vs-polyvalent. eVim refutes it and the module says so."""
    pattern = ag.COVERAGE_EXPLAINS_WHICH_VACCINES_WORKED["the_pattern"]
    assert "not defined-versus-polyvalent" in pattern
    assert "eVim is defined and it worked" in pattern
    evim = ag.COVERAGE_EXPLAINS_WHICH_VACCINES_WORKED["evim"]
    assert evim["antigen"].startswith("DEFINED")
    assert "11 of 11" in evim["coverage_evidence"]


def test_the_polyvalent_vaccines_are_marked_as_sidestepping_the_question():
    for key in ("er_stress_peptides", "autologous_dendritic_cell"):
        entry = ag.COVERAGE_EXPLAINS_WHICH_VACCINES_WORKED[key]
        assert entry["antigen"].startswith("POLYVALENT")
        assert "not applicable" in entry["coverage_evidence"]


def test_the_hypothesis_makes_a_falsifiable_prediction_and_says_it_is_a_hypothesis():
    entry = ag.COVERAGE_EXPLAINS_WHICH_VACCINES_WORKED
    assert "SOCH" in entry["the_prediction_this_makes"]
    assert "real test" in entry["the_prediction_this_makes"]
    status = entry["the_honest_status"]
    assert "four results is not a dataset" in status
    assert "not a finding" in status


# ---------------------------------------------------------------------------------------------
# What the engine says about the two modes.

def test_full_coverage_gives_identical_results_in_both_modes():
    """The fairness check: at phi = 1 the two specifications describe the same tumour."""
    uniform, heterogeneous = ag.DURABILITY_BY_COVERAGE[1.00]
    assert uniform == pytest.approx(heterogeneous)


def test_uniform_dimming_degrades_as_coverage_falls():
    """Monotone to within Monte Carlo noise.

    0.80 and 0.60 coverage give 0.496 and 0.500 -- inverted by 0.004, against a standard error of
    roughly 0.03 at 250 trials. Both have plateaued on the ~0.50 floor the cross-resistance
    correction delivers on its own, so there is nothing left to separate them. The test allows
    noise-scale inversions rather than asserting a cleanliness the sample size cannot support.
    """
    coverages = sorted(ag.DURABILITY_BY_COVERAGE)
    uniform = [ag.DURABILITY_BY_COVERAGE[c][0] for c in coverages]
    noise = 0.05
    for lower, higher in zip(uniform, uniform[1:]):
        assert lower <= higher + noise, f"uniform reversed by more than noise: {uniform}"
    # And the trend across the full range is unambiguous even if adjacent steps are not.
    assert uniform[-1] - uniform[0] > 0.5


def test_the_blind_spot_barely_moves_across_the_whole_range():
    values = [v[1] for v in ag.DURABILITY_BY_COVERAGE.values()]
    assert max(values) - min(values) < 0.05


def test_the_two_modes_diverge_and_uniform_is_the_worse_one():
    """The counterintuitive result: dimming everywhere beats a blind spot, not the other way round."""
    for coverage, (uniform, heterogeneous) in ag.DURABILITY_BY_COVERAGE.items():
        if coverage < 1.0:
            assert uniform < heterogeneous, f"at coverage {coverage}"
    assert ag.DURABILITY_BY_COVERAGE[0.40][0] < 0.35
    assert ag.DURABILITY_BY_COVERAGE[0.40][1] > 0.80


def test_the_inverted_expectation_is_recorded_rather_than_quietly_fixed():
    entry = ag.THE_RESULT_INVERTS_THE_EXPECTATION
    assert "the opposite" in entry["what_happened"]
    assert "DRUG-SENSITIVE" in entry["why"]
    assert "DRUG-RESISTANT" in entry["the_reframing"]


def test_the_modelling_choice_doing_the_work_is_named():
    caveat = ag.THE_RESULT_INVERTS_THE_EXPECTATION["the_honest_caveat"]
    assert "modelling choice" in caveat
    assert "overlaps drug resistance" in caveat


def test_the_experiment_is_redirected_to_the_resistant_fraction():
    entry = ag.WHAT_TO_MEASURE_INSTEAD
    assert "bulk" in entry["the_wrong_experiment"]
    assert "DRUG-RESISTANT FRACTION" in entry["the_right_experiment"]
    assert "ISOS-1" in entry["why_this_is_cheap"]


# ---------------------------------------------------------------------------------------------
# The closure.

def test_all_four_closure_legs_carry_a_status():
    legs = [ag.CLOSURE_LEG_1_THE_DRUG_ABSORBS_IT, ag.CLOSURE_LEG_2_POLYVALENT_VACCINES_SIDESTEP_IT,
            ag.CLOSURE_LEG_3_EPITOPE_SPREADING_REPAIRS_COVERAGE,
            ag.CLOSURE_LEG_4_FORCE_THE_SPREADING_WITHOUT_KNOWING_THE_ANTIGEN]
    for leg in legs:
        assert leg["status"].startswith(("CLOSED", "PARTIAL"))
        assert leg["claim"]


def test_leg_1_states_the_condition_it_depends_on():
    leg = ag.CLOSURE_LEG_1_THE_DRUG_ABSORBS_IT
    assert "must not overlap drug resistance" in leg["the_condition_it_depends_on"]
    assert "WORTHLESS otherwise" in leg["status"], (
        "leg 1 must not read as a general closure -- it fails completely on overlap")


def test_leg_2_records_the_cost_it_reintroduces():
    leg = ag.CLOSURE_LEG_2_POLYVALENT_VACCINES_SIDESTEP_IT
    assert "per dog" in leg["the_cost"]
    assert "manufacturing" in leg["the_cost"]


def test_leg_3_epitope_spreading_has_the_clinical_citation_and_its_limits():
    leg = ag.CLOSURE_LEG_3_EPITOPE_SPREADING_REPAIRS_COVERAGE
    assert "36027916" in leg["clinical_evidence"]
    assert "NON-VACCINATING" in leg["clinical_evidence"]
    assert "not shown to be sufficient" in leg["the_limits"]


def test_leg_4_is_antigen_agnostic_and_has_canine_evidence():
    leg = ag.CLOSURE_LEG_4_FORCE_THE_SPREADING_WITHOUT_KNOWING_THE_ANTIGEN
    assert "TUMOUR-UNSPECIFIC" in leg["claim"]
    assert "client-owned canines" in leg["the_canine_evidence"]
    assert "38697107" in leg["the_canine_evidence"]
    assert "not hemangiosarcoma" in leg["the_limits"]


def test_nk_cells_are_explicitly_refused_as_a_route_8_closer():
    """Listing NK as a closer would repeat exactly the conflation this module undoes."""
    entry = ag.THE_NK_COMPONENT_ONLY_PARTLY_TRANSFERS
    assert "MISSING-SELF" in entry["why_it_does_not_fully_work"]
    assert "route 4" in entry["what_it_does_cover"]
    assert "route 8" in entry["what_it_does_not_cover"]
    assert "conflation" in entry["the_correction"]


def test_the_verdict_keeps_the_route_honest():
    v = ag.VERDICT
    assert "not by the component that closes" in v["is_it_closable"]
    assert "overlaps drug resistance" in v["the_condition_that_decides_it"]
    assert "none of the four legs has been tested in canine hemangiosarcoma" in v[
        "what_this_does_not_claim"]


# ---------------------------------------------------------------------------------------------
# The dangerous case: a blind spot that overlaps drug resistance.

def test_all_three_specifications_agree_at_full_coverage():
    """Fairness check again: at phi = 1 there is no blind spot to place anywhere."""
    sensitive, mixed, resistant = ag.DURABILITY_BY_WHERE_THE_BLIND_SPOT_LANDS[1.00]
    assert sensitive == pytest.approx(mixed) == pytest.approx(resistant)


def test_a_drug_sensitive_blind_spot_stays_harmless():
    for coverage, row in ag.DURABILITY_BY_WHERE_THE_BLIND_SPOT_LANDS.items():
        assert row[0] > 0.80, f"sensitive blind spot should not bite at coverage {coverage}"


def test_any_resistant_component_is_total_failure_not_degradation():
    """0.000, not a reduced number -- the distinction the module has to preserve."""
    for coverage, (_sens, mixed, resistant) in ag.DURABILITY_BY_WHERE_THE_BLIND_SPOT_LANDS.items():
        if coverage < 1.0:
            assert resistant == 0.0, f"coverage {coverage}"
            assert mixed == 0.0, f"coverage {coverage}: half-resistant is no softer"


def test_the_cliff_is_between_neighbouring_specifications_not_across_coverage():
    """Coverage barely matters; where the blind spot lands is everything."""
    at_95 = ag.DURABILITY_BY_WHERE_THE_BLIND_SPOT_LANDS[0.95]
    assert at_95[0] - at_95[2] > 0.8


def test_continuous_dosing_does_not_rescue_an_overlapping_blind_spot():
    for coverage, arms in ag.CONTINUOUS_DOSING_DOES_NOT_RESCUE_AN_OVERLAPPING_BLIND_SPOT.items():
        assert arms["stop_at_year_1"] == 0.0, coverage
        assert arms["never_stop"] == 0.0, coverage


def test_the_module_refuses_to_soften_the_result():
    entry = ag.OVERLAP_IS_THE_WHOLE_BALLGAME
    assert "not a worse outcome, it is a total one" in entry["the_finding"]
    assert "250 of 250 trials" in entry["the_finding"]
    assert "GO/NO-GO GATE" in entry["what_this_does_to_the_measurement"]
    assert "the condition is not a caveat, it is the entire result" in entry["the_honest_reading"]


def test_the_backup_legs_are_promoted_to_the_only_answers():
    entry = ag.OVERLAP_IS_THE_WHOLE_BALLGAME
    assert "stop being backups" in entry["what_this_does_to_legs_2_to_4"]
    assert "None of them has been tested" in entry["what_this_does_to_legs_2_to_4"]
    assert "the_only_answers_if_it_does_overlap" in ag.VERDICT
