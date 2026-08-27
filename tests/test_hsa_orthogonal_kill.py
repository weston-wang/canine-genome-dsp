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


# ---------------------------------------------------------------------------------------------
# Does it actually rescue the zero?

def test_the_baseline_is_the_unrescued_zero():
    assert ok.RESCUE_BY_PERSISTER_KILL[0.000] == 0.0


def test_persister_kill_does_rescue_the_case_nothing_else_touched():
    assert ok.RESCUE_BY_PERSISTER_KILL[0.050] == pytest.approx(1.0)
    assert "does rescue" in ok.IT_WORKS_BUT_IT_IS_A_KNIFE_EDGE["the_good_news"]


def test_the_rescue_is_a_step_not_a_ramp():
    """Below threshold the rescue is worth exactly nothing -- unlike the vaccine-height curve."""
    below = [v for k, v in ok.RESCUE_BY_PERSISTER_KILL.items() if k <= 0.035]
    assert all(v == 0.0 for v in below), "everything at or below 0.035/day should be a flat zero"
    assert ok.RESCUE_BY_PERSISTER_KILL[0.040] > 0.0
    assert "It is a step" in ok.IT_WORKS_BUT_IT_IS_A_KNIFE_EDGE["the_bad_news"]


def test_the_grid_is_monotone():
    rates = sorted(ok.RESCUE_BY_PERSISTER_KILL)
    values = [ok.RESCUE_BY_PERSISTER_KILL[r] for r in rates]
    assert values == sorted(values)


def test_the_size_of_the_ask_is_computed_not_asserted():
    ask = ok.IT_WORKS_BUT_IT_IS_A_KNIFE_EDGE["how_big_the_ask_is"]
    assert ask["as_a_multiple_of_the_mek_requirement"] == pytest.approx(
        ask["required_per_day"] / 0.0225)
    assert ask["as_a_fraction_of_the_bar"] == pytest.approx(ask["required_per_day"] / 0.0515)
    assert ask["as_a_multiple_of_the_mek_requirement"] > 1.5, "this is a large ask, not a small one"


def test_the_reassuring_comparison_is_explicitly_withdrawn():
    """Andersen's 0.110-0.143/day was measured on drug-SENSITIVE tumour, by the drugs this cell
    resists. Citing it as evidence the ask is reachable is a category error, and the module has to
    say so rather than quietly drop it."""
    entry = ok.IT_WORKS_BUT_IT_IS_A_KNIFE_EDGE
    withdrawn = entry["the_comparison_that_does_not_work"]
    assert "CATEGORY ERROR" in withdrawn
    assert "withdrawn" in withdrawn
    assert "drug-SENSITIVE bulk tumour" in withdrawn
    assert "what_makes_it_less_implausible_than_it_sounds" not in entry


def test_the_population_size_mitigation_is_also_rejected():
    """A rate requirement does not get easier because the compartment is small."""
    other = ok.IT_WORKS_BUT_IT_IS_A_KNIFE_EDGE["the_other_mitigation_that_does_not_work"]
    assert "RATE, per cell per day" in other
    assert "not the threshold" in other


def test_only_a_mechanism_class_claim_survives():
    survives = ok.IT_WORKS_BUT_IT_IS_A_KNIFE_EDGE["what_actually_remains_true"]
    assert "not about magnitude" in survives
    assert "only mitigation that survives" in survives
    assert "nothing to compare it to" in ok.IT_WORKS_BUT_IT_IS_A_KNIFE_EDGE["the_position_this_leaves"]


def test_it_is_compared_honestly_against_the_easier_routes():
    comparison = ok.IT_WORKS_BUT_IT_IS_A_KNIFE_EDGE["how_this_compares_to_the_other_routes"]
    assert "7-45%" in comparison
    assert "least comfortable answer" in comparison
    assert "only answer to this case" in comparison


def test_the_verdict_says_closable_not_closed():
    verdict = ok.IT_WORKS_BUT_IT_IS_A_KNIFE_EDGE["the_honest_verdict"]
    assert "closable rather than closed" in verdict
    assert "never been measured" in verdict
    assert "Claiming this as solved" in verdict


def test_the_experiment_puts_the_cheap_step_first():
    exp = ok.THE_EXPERIMENT_THIS_POINTS_AT
    assert "before and after PI3K/mTOR inhibition" in exp["step_1"]
    assert "none of this is needed" in exp["step_1"]
    assert "drug-tolerant fraction specifically" in exp["step_2"]
    assert "0.045/day" in exp["step_3"]
    assert "cheap answer and an" in exp["why_this_ordering_matters"]


# ---------------------------------------------------------------------------------------------
# The better answer: restore visibility rather than out-kill the invisible cell.

def test_antigen_loss_is_recorded_as_often_but_not_always_reversible():
    entry = ok.ANTIGEN_LOSS_IS_OFTEN_REVERSIBLE
    assert "33671123" in entry["citation"]
    assert "EPIGENETIC MODIFICATIONS" in entry["the_mechanism"]
    assert "deletional and irreversible" in entry["the_limit_of_the_claim"]


def test_the_field_immaturity_is_quoted_from_the_authors_themselves():
    caution = ok.ANTIGEN_LOSS_IS_OFTEN_REVERSIBLE["the_authors_own_caution"]
    assert "LEAST ADVANCED AREA" in caution
    assert "not be quoted as a solved problem" in caution


def test_the_obvious_epigenetic_agents_are_recorded_as_having_failed_here():
    """SAHA and VPA were tried in canine HSA and did not work in vivo. That has to be said."""
    entry = ok.HDAC_INHIBITION_WAS_TRIED_IN_CANINE_HSA_AND_FAILED
    assert "35568976" in entry["citation"]
    assert "DID NOT AFFECT TUMOUR GROWTH" in entry["the_in_vivo_result"]
    assert "did not work" in entry["the_honest_conclusion"]


def test_the_hdac_macrophage_risk_is_flagged_against_the_hsa_specific_finding():
    entry = ok.HDAC_INHIBITION_WAS_TRIED_IN_CANINE_HSA_AND_FAILED
    assert "attracted macrophage" in entry["the_second_problem"]
    assert "Gulay 2022" in entry["the_second_problem"]
    assert "plausible harm" in entry["the_second_problem"]


def test_jq1_is_not_credited_as_an_antigen_restoration_answer():
    survives = ok.HDAC_INHIBITION_WAS_TRIED_IN_CANINE_HSA_AND_FAILED["what_survives"]
    assert "not an antigen-restoration mechanism" in survives
    assert "does not address route" in survives


def test_type_i_interferon_is_presented_as_antigen_agnostic():
    entry = ok.TYPE_I_INTERFERON_IS_THE_CONVERGENCE_POINT
    assert "antigen-agnostic" in entry["the_mechanism"]
    assert "does not require knowing which antigen was lost" in entry["the_mechanism"]


def test_it_unifies_three_findings_rather_than_adding_a_fourth_agent():
    why = ok.TYPE_I_INTERFERON_IS_THE_CONVERGENCE_POINT["why_this_unifies_three_separate_findings"]
    assert "one intervention, not three" in why
    assert "epitope spreading" in why


def test_both_canine_sting_studies_carry_design_and_result():
    entry = ok.TYPE_I_INTERFERON_IS_THE_CONVERGENCE_POINT
    first = entry["canine_evidence_1_sting_in_client_owned_dogs"]
    assert "41381219" in first["citation"]
    assert "19 client-owned dogs" in first["design"]
    assert "TUMOR TISSUE" in first["the_result"]
    second = entry["canine_evidence_2_a_formulation_without_the_toxicity"]
    assert "42096576" in second["citation"]
    assert "WITHOUT CYTOKINE RELEASE SYNDROME" in second["the_result"]


def test_the_toxicity_objection_and_its_candidate_answer_are_both_recorded():
    entry = ok.TYPE_I_INTERFERON_IS_THE_CONVERGENCE_POINT
    assert "cytokine release syndrome" in entry[
        "canine_evidence_1_sting_in_client_owned_dogs"]["safety"]
    assert "reports avoiding it" in entry[
        "canine_evidence_2_a_formulation_without_the_toxicity"]["why_it_matters_here"]


def test_the_inferred_step_is_named_as_inferred():
    """Both canine studies measured ISGs, not MHC-I. The module must not claim the last step."""
    gap = ok.TYPE_I_INTERFERON_IS_THE_CONVERGENCE_POINT["what_is_not_established"]
    assert "neither canine study measured MHC-I" in gap
    assert "the specific link is inferred" in gap


# ---------------------------------------------------------------------------------------------
# The re-expression route, measured.

def test_restoration_below_full_is_worth_nothing():
    for reach, row in ok.DURABILITY_BY_RESTORED_REACH.items():
        if reach < 1.0:
            assert all(v == 0.0 for v in row), f"reach {reach}"


def test_even_full_restoration_falls_short_of_the_reference():
    at_full = ok.DURABILITY_BY_RESTORED_REACH[1.00]
    assert all(0.2 < v < 0.35 for v in at_full)
    assert max(at_full) < 0.840, "full restoration must not be presented as a closure"


def test_the_module_says_restoration_alone_does_not_close_it():
    entry = ok.RESTORATION_ALONE_DOES_NOT_CLOSE_IT
    assert "not a closure" in entry["the_result"]
    assert "DRUG-RESISTANT" in entry["why"]
    assert "wanes between" in entry["why"]


def test_the_premature_writeup_is_owned():
    """The route was written up before it was run. That has to be recorded, not smoothed over."""
    correction = ok.RESTORATION_ALONE_DOES_NOT_CLOSE_IT["the_correction_this_forces"]
    assert "premature" in correction
    assert "does not work alone" in correction


def test_it_reconnects_to_the_toxicity_finding_rather_than_escaping_it():
    implication = ok.RESTORATION_ALONE_DOES_NOT_CLOSE_IT["what_it_implies_about_the_regimen"]
    assert "second drug cannot be withdrawn" in implication
