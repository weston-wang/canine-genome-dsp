"""Tests for `hsa_orthogonal_kill`.

The module answers the one case in the analysis with no answer: a subpopulation that is both
antigen-null and drug-resistant. These tests check that the orthogonality requirement is stated
before any candidate is proposed, that each candidate is held to it, and that the module corrects
rather than quietly reverses the earlier refusal of NK cells.
"""
import pytest

from canine_dsp import hsa_orthogonal_kill as ok


# ---------------------------------------------------------------------------------------------
# The requirement, stated first.

def test_the_requirement_rules_out_the_two_obvious_non_answers():
    req = ok.THE_ORTHOGONALITY_REQUIREMENT
    assert "circular" in req["must_not_need_the_antigen"]
    assert "buys nothing" in req["must_not_act_through_the_kinase_pathway"]
    assert "duration criterion" in req["must_be_givable_for_the_horizon"]


def test_a_second_antigen_is_explicitly_not_a_solution():
    """Swapping in another CAR or vaccine target just relocates the coverage question."""
    why = ok.THE_ORTHOGONALITY_REQUIREMENT["why_this_is_a_narrow_gate"]
    assert "different molecule" in why
    assert "another kinase inhibitor fails" in why


# ---------------------------------------------------------------------------------------------
# The mechanism.

def test_the_dependency_is_a_property_of_the_state_not_the_antigen():
    entry = ok.PERSISTERS_ACQUIRE_A_DEPENDENCY
    assert "29088702" in entry["citation"]
    assert "GPX4" in entry["the_finding"]
    assert "orthogonal to both axes by construction" in entry["why_it_satisfies_the_gate"]


def test_the_cited_endpoint_is_the_one_the_model_measures():
    entry = ok.PERSISTERS_ACQUIRE_A_DEPENDENCY
    assert "PREVENTS TUMOUR RELAPSE IN MICE" in entry["the_consequence"]
    assert "relapse is the endpoint" in entry["why_the_endpoint_matters_here"]


def test_selectivity_is_recorded_as_the_reason_a_modest_rate_can_work():
    reason = ok.PERSISTERS_ACQUIRE_A_DEPENDENCY["the_selectivity_is_the_point"]
    assert "does not need to cover the whole tumour" in reason


def test_the_species_bridge_is_cited_with_its_preprint_status():
    entry = ok.CANINE_CELLS_ARE_FERROPTOSIS_COMPETENT
    assert "38746359" in entry["citation"]
    assert "INDISTINGUISHABLE FROM HUMAN CANCER CELLS" in entry["the_finding"]
    assert "not peer-reviewed" in entry["the_status_caveat"]


# ---------------------------------------------------------------------------------------------
# The agent.

def test_parthenolide_was_tested_in_this_disease_on_purpose():
    entry = ok.PARTHENOLIDE_WAS_TESTED_IN_CANINE_HEMANGIOSARCOMA
    assert "38135509" in entry["citation"]
    assert "HEMANGIOSARCOMA" in entry["why_this_paper_exists"]
    assert "PRIMARY" in entry["the_result"]


def test_the_synergy_property_a_fourth_agent_needs_is_recorded():
    entry = ok.PARTHENOLIDE_WAS_TESTED_IN_CANINE_HEMANGIOSARCOMA
    assert "SYNERGIZE" in entry["the_combination_finding"]
    assert "already has three" in entry["the_combination_finding"]


def test_parthenolide_is_linked_to_the_same_axis_not_offered_as_a_separate_idea():
    link = ok.PARTHENOLIDE_WAS_TESTED_IN_CANINE_HEMANGIOSARCOMA["the_link_to_the_dependency"]
    assert "not a different idea" in link
    assert "lipid-peroxidation" in link


def test_dmapt_clears_exposure_in_dogs():
    entry = ok.DMAPT_IS_THE_ORAL_FORM_AND_HAS_BEEN_GIVEN_TO_DOGS
    assert "17804695" in entry["citation"]
    assert entry["oral_bioavailability"] == pytest.approx(0.70)
    assert "SPONTANEOUS ACUTE CANINE LEUKEMIAS" in entry["the_canine_evidence"]


def test_dmapt_is_not_waved_through_on_the_duration_criterion():
    """The same gap that disqualified the MEK/mTOR pair must not get a pass here."""
    missing = ok.DMAPT_IS_THE_ORAL_FORM_AND_HAS_BEEN_GIVEN_TO_DOGS["what_is_still_missing"]
    assert "NOT been shown to clear the duration criterion" in missing
    assert "should not be waved through" in missing


def test_dmapt_targets_the_right_class_of_cell():
    entry = ok.DMAPT_IS_THE_ORAL_FORM_AND_HAS_BEEN_GIVEN_TO_DOGS
    assert "STEM AND PROGENITOR" in entry["the_target_class"]
    assert "persisters" in entry["the_target_class"]


# ---------------------------------------------------------------------------------------------
# The NK correction.

def test_the_earlier_nk_refusal_is_corrected_not_reversed():
    entry = ok.NK_CELLS_ARE_PARTLY_REHABILITATED
    assert "missing-self" in entry["what_was_said_before"]
    assert "NKG2D" in entry["what_that_missed"]
    correction = entry["the_honest_correction"]
    assert "right about missing-self" in correction
    assert "not a complete answer either" in correction


def test_the_nk_arm_has_canine_evidence_and_its_own_escape():
    entry = ok.NK_CELLS_ARE_PARTLY_REHABILITATED
    assert "37672843" in entry["the_canine_evidence"]
    assert "MIC-A and MIC-B are present in dogs" in entry["the_canine_evidence"]
    assert "SOLUBLE MIC-A" in entry["the_escape_that_comes_with_it"]


def test_the_nk_arm_names_a_settling_experiment():
    entry = ok.NK_CELLS_ARE_PARTLY_REHABILITATED
    assert "before and after PI3K/mTOR inhibition" in entry["what_would_settle_it"]


def test_this_module_does_not_contradict_the_adequacy_module():
    """Route 8's refusal of NK as a *missing-self* closer still stands; this adds a second arm."""
    from canine_dsp import hsa_antigen_adequacy as ag
    assert "MISSING-SELF" in ag.THE_NK_COMPONENT_ONLY_PARTLY_TRANSFERS["why_it_does_not_fully_work"]
    assert "missing-self" in ok.NK_CELLS_ARE_PARTLY_REHABILITATED["the_honest_correction"]
