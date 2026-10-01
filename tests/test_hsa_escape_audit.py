"""Tests for the independent escape audit.

These enforce two things the narrative cannot: that the grading vocabulary is used honestly (an
argument is never recorded as a measurement), and that the three newly found routes stay recorded
with the limits that came with them.
"""
from __future__ import annotations

import math

import pytest

from canine_dsp import hsa_escape_audit as audit
from canine_dsp import hsa_route_effect_sizes as eff


# =================================================================================================
# The audit method itself.
# =================================================================================================

def test_the_audit_enumerated_the_universe_before_grepping_the_record():
    how = audit.HOW_THE_ESCAPE_UNIVERSE_WAS_ENUMERATED
    assert "WITHOUT consulting the eight routes" in how["method"]
    assert len(how["classes_checked"]) >= 12


def test_the_keyword_trap_is_recorded():
    """The word 'sanctuary' was in the document 20 times and meant something else entirely."""
    trap = audit.HOW_THE_ESCAPE_UNIVERSE_WAS_ENUMERATED["the_trap_this_caught"]
    assert "PHENOTYPIC" in trap
    assert "not mentioned anywhere" in trap


def test_every_class_with_zero_hits_is_either_graded_or_explicitly_folded_elsewhere():
    """No class may be dropped silently between the enumeration and the grading."""
    zero = set(audit.HOW_THE_ESCAPE_UNIVERSE_WAS_ENUMERATED["classes_with_zero_hits_in_the_record"])
    accounted = {
        "anatomical sanctuary sites",            # route 9
        "immunosenescence",                      # route 10
        "competing all-cause mortality",         # route 11
        "second primary tumour",                 # folded into route 11
        "tumour-induced lymphopenia",            # folded into route 10
        "dormancy",                              # ROUTES_CLOSED_BY_EXISTING_ARGUMENTS
        "antigen-presentation machinery (B2M/TAP)",
        "regulatory T cells",
        "MDSC",
        "clonal evolution",
    }
    assert zero <= accounted, f"unaccounted: {zero - accounted}"


# =================================================================================================
# Route 9 -- CNS sanctuary.
# =================================================================================================

def test_the_cns_threat_is_measured_and_the_closure_is_only_transferred():
    assert audit.ROUTE_9_CNS_SANCTUARY["grade_of_the_threat"] == audit.MEASURED
    assert audit.ROUTE_9_CNS_SANCTUARY["grade_of_the_closure"] == audit.TRANSFERRED


def test_the_29_percent_is_not_allowed_to_be_misread_as_a_per_dog_incidence():
    """The denominator trap, recorded explicitly because it is easy to get backwards."""
    note = audit.ROUTE_9_CNS_SANCTUARY["what_the_29_percent_is_and_is_not"]
    assert "It is NOT the share of hemangiosarcoma" in note
    assert "NOT verified here" in note


def test_the_route_8_closure_is_stated_not_to_extend_to_the_brain():
    why = audit.ROUTE_9_CNS_SANCTUARY["why_it_breaks_the_plan"]
    assert "does NOT extend" in why
    for component in ("Doxorubicin", "eBAT", "Losartan"):
        assert component in why


def test_the_cns_route_selects_between_the_two_real_vaccine_trials():
    consequence = audit.ROUTE_9_CNS_SANCTUARY["the_consequence_that_is_actually_useful"]
    assert "ERstrePs" in consequence and "eVim" in consequence
    assert "does NOT" in consequence


def test_intracranial_haemorrhage_is_kept_with_the_competing_events():
    assert "competing event" in audit.ROUTE_9_CNS_SANCTUARY["what_remains_open"]


# =================================================================================================
# Route 10 -- immunosenescence.
# =================================================================================================

def test_immunosenescence_attacks_induction_and_spares_maintenance():
    assert "PRIMARY response" in audit.ROUTE_10_IMMUNOSENESCENCE["the_part_that_closes"]
    assert "Memory responses" in audit.ROUTE_10_IMMUNOSENESCENCE["the_part_that_closes"]


def test_redosing_is_rehabilitated_against_the_right_question_not_the_old_one():
    correction = audit.ROUTE_10_IMMUNOSENESCENCE["the_correction_this_forces"]
    assert "different question" in correction
    assert "Demoting" in correction and "was right" in correction
    # and the demotion itself must still stand in the other module
    assert min(eff.TRANSFER_REQUIRED["route_3_redosing"]["transfer_needed"]) > 1.0


def test_the_ten_year_booster_claim_is_marked_unevidenced():
    assert "ten years" in audit.ROUTE_10_IMMUNOSENESCENCE["what_remains_open"]


# =================================================================================================
# Route 11 -- the endpoint.
# =================================================================================================

def test_remaining_lifespan_is_short_or_negative_at_the_observed_age_at_diagnosis():
    for breed in audit.BREED_MEDIAN_LIFESPAN_YEARS:
        assert audit.remaining_natural_lifespan(breed) < 3.0


def test_the_german_shepherd_is_already_past_median_lifespan_at_diagnosis():
    assert audit.remaining_natural_lifespan("German Shepherd Dog") < 1.0


def test_early_detection_makes_the_goal_reachable_rather_than_unreachable():
    lo, hi = audit.EARLY_DETECTION_LEAD_YEARS
    for breed in audit.BREED_MEDIAN_LIFESPAN_YEARS:
        assert (audit.remaining_natural_lifespan(breed, lead_time_years=hi)
                > audit.remaining_natural_lifespan(breed))


def test_the_scoping_finding_makes_the_goal_easier_and_says_so():
    does = audit.ROUTE_11_THE_DOG_RUNS_OUT_OF_LIFE["what_it_DOES_mean"]
    assert "EASIER" in does
    assert "conservative" in audit.ROUTE_11_THE_DOG_RUNS_OUT_OF_LIFE[
        "what_this_does_NOT_mean"].lower()


def test_remaining_lifespan_rejects_an_unknown_breed_and_a_negative_lead():
    with pytest.raises(ValueError):
        audit.remaining_natural_lifespan("Corgi-sized mystery breed")
    with pytest.raises(ValueError):
        audit.remaining_natural_lifespan("Golden Retriever", lead_time_years=-1.0)


# =================================================================================================
# The increment, regraded.
# =================================================================================================

def test_the_naive_rate_conversion_is_recorded_as_an_artefact_not_a_result():
    conv = audit.KEYNOTE_942_RATE_CONVERSION
    assert min(conv["transfer_needed"]) > 1.0            # it does read as a failure
    assert "artefact" in conv["why_this_conversion_is_NOT_the_right_one"]
    assert "outside its domain" in conv["why_this_conversion_is_NOT_the_right_one"]


def test_the_arithmetic_check_against_the_trials_own_hazard_ratio():
    """Deriving the HR from the reported RFS rates must reproduce the reported HR."""
    t = 912.0
    combo, control = audit.KEYNOTE_942["result"]["rfs_at_2_5_years"]
    derived = (-math.log(combo) / t) / (-math.log(control) / t)
    assert derived == pytest.approx(audit.KEYNOTE_942["result"]["rfs_hazard_ratio"], abs=0.03)


def test_required_hazard_ratio_matches_the_recorded_plan_requirement():
    base = eff.durability_at_increment(0.0, stop_year=1)
    for multiple, expected in audit.SCALE_FREE_COMPARISON[
            "plan_requirement_by_vaccine_multiple"].items():
        increment = round((multiple - 1.0) * eff.MEASURED_VACCINE_HEIGHT, 6)
        got = audit.required_hazard_ratio(
            eff.durability_at_increment(increment, stop_year=1), base)
        assert got == pytest.approx(expected, abs=0.01), multiple


def test_one_lever_does_not_reach_the_headline_requirement():
    need = audit.SCALE_FREE_COMPARISON["plan_requirement_by_vaccine_multiple"][1.40]
    assert audit.SCALE_FREE_COMPARISON["measured_hazard_ratio_rfs"] > need
    assert audit.SCALE_FREE_COMPARISON["measured_hazard_ratio_dmfs"] > need


def test_one_lever_does_clear_the_rung_below_on_the_dmfs_endpoint():
    need_135 = audit.SCALE_FREE_COMPARISON["plan_requirement_by_vaccine_multiple"][1.35]
    assert audit.SCALE_FREE_COMPARISON["measured_hazard_ratio_dmfs"] < need_135
    assert audit.SCALE_FREE_COMPARISON["measured_hazard_ratio_rfs"] > need_135


def test_the_increment_was_upgraded_but_only_one_grade():
    assert audit.SCALE_FREE_COMPARISON["grade_before_this_audit"] == audit.ASSUMED
    assert audit.SCALE_FREE_COMPARISON["grade_after_this_audit"] == audit.TRANSFERRED
    assert audit.SCALE_FREE_COMPARISON["grade_after_this_audit"] != audit.MEASURED


def test_the_stacking_caveat_survives_the_upgrade():
    note = audit.SCALE_FREE_COMPARISON["what_it_does_NOT_change"]
    assert "overlap rather than sum" in note
    assert "four levers is not four times one" in note


def test_required_hazard_ratio_rejects_degenerate_durabilities():
    for bad in (0.0, 1.0, -0.1, 1.2):
        with pytest.raises(ValueError):
            audit.required_hazard_ratio(bad, 0.5)
        with pytest.raises(ValueError):
            audit.required_hazard_ratio(0.5, bad)


# =================================================================================================
# The verdict.
# =================================================================================================

def test_the_verdict_is_not_a_closure_claim():
    assert audit.VERDICT["is_it_covered"].startswith("NO")


def test_the_verdict_keeps_an_open_list_and_it_is_not_empty():
    assert len(audit.VERDICT["what_is_still_ASSUMED_and_therefore_still_open"]) >= 5


def test_resistance_driver_evolution_is_bounded_by_the_no_drug_row():
    """A resistance lesion cannot outrun the untreated rate; that row is already in the bar table."""
    entry = audit.ROUTES_CLOSED_BY_EXISTING_ARGUMENTS["clonal_evolution_to_a_new_resistance_driver"]
    assert entry["grade"] == audit.TRANSFERRED
    assert "0.0550" in entry["the_bound_that_closes_it_properly"]
    assert "6.8%" in entry["the_bound_that_closes_it_properly"]


def test_the_bound_costs_exactly_one_rung_on_the_ramp():
    cost = audit.ROUTES_CLOSED_BY_EXISTING_ARGUMENTS[
        "clonal_evolution_to_a_new_resistance_driver"]["what_that_costs_the_plan"]
    assert "1.40x" in cost and "1.50x" in cost
    # and that rung must actually exist in the simulated grid
    assert eff.durability_at_increment(0.015, stop_year=1) > 0.99


def test_the_intrinsic_proliferation_case_is_NOT_claimed_closed():
    entry = audit.ROUTES_CLOSED_BY_EXISTING_ARGUMENTS["clonal_evolution_to_a_new_resistance_driver"]
    assert "Mitigation, not closure" in entry["what_this_does_NOT_close"]


def test_the_treg_lever_is_credited_and_its_magnitude_is_not_claimed():
    entry = audit.ROUTES_CLOSED_BY_EXISTING_ARGUMENTS[
        "regulatory_T_cells_and_myeloid_derived_suppressor_cells"]
    assert "meloxicam" in entry["the_treg_lever_that_was_already_in_the_record_uncredited"]
    assert "magnitude is unmeasured" in entry["what_stays_open"]


def test_no_argument_in_this_module_is_graded_measured():
    """Closures here are arguments or transfers. Only threats are measured."""
    for entry in audit.ROUTES_CLOSED_BY_EXISTING_ARGUMENTS.values():
        assert entry["grade"] in (audit.TRANSFERRED, audit.ASSUMED)
