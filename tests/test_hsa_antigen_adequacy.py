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
