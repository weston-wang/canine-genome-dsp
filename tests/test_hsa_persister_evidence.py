"""Tests for the measured-effect-size case behind the persister-directed kill.

The job of these tests is the same as everywhere else in this analysis: catch the module claiming
more than its sources support. Several of them exist specifically to fail if someone later upgrades
a hedge into an assertion.
"""
import math

import pytest

from canine_dsp import hsa_orthogonal_kill as ok
from canine_dsp import hsa_persister_evidence as pe
from canine_dsp.hsa_route_effect_sizes import rate_from_burden_reduction


# ---------------------------------------------------------------------------------------------
# The conversion helpers.
# ---------------------------------------------------------------------------------------------

def test_viability_after_inverts_rate_from_burden_reduction():
    for rate in (0.01, 0.045, 0.2, 0.8):
        v = pe.viability_after(rate, days=3.0)
        assert rate_from_burden_reduction(v, 3.0) == pytest.approx(rate)


def test_viability_after_is_one_at_zero_rate_and_decreasing():
    assert pe.viability_after(0.0) == pytest.approx(1.0)
    seq = [pe.viability_after(r) for r in (0.01, 0.02, 0.05, 0.1)]
    assert seq == sorted(seq, reverse=True)


def test_viability_after_rejects_bad_inputs():
    with pytest.raises(ValueError):
        pe.viability_after(-0.1)
    with pytest.raises(ValueError):
        pe.viability_after(0.045, days=0)


def test_transfer_required_from_viability_matches_hand_arithmetic():
    # A 50% kill over three days is -ln(0.5)/3 = 0.2310/day; 0.045 / 0.2310 = 0.1948.
    assert pe.transfer_required_from_viability(0.5) == pytest.approx(0.1948, abs=5e-4)


def test_transfer_required_falls_as_the_assay_kill_deepens():
    ts = [pe.transfer_required_from_viability(v) for v in (0.75, 0.5, 0.3, 0.2, 0.1)]
    assert ts == sorted(ts, reverse=True)


# ---------------------------------------------------------------------------------------------
# The requirement restated in assay units. This is the module's central arithmetic claim.
# ---------------------------------------------------------------------------------------------

def test_the_requirement_in_assay_units_is_a_small_three_day_kill():
    d = pe.THE_REQUIREMENT_IN_ASSAY_UNITS
    assert d["required_per_day"] == 0.045
    assert d["three_day_viability_that_corresponds_to"] == pytest.approx(math.exp(-0.045 * 3))
    assert d["as_a_three_day_kill"] == pytest.approx(0.1263, abs=5e-4)
    # The whole point: the ask is under a fifth of the persisters over the assay window.
    assert d["as_a_three_day_kill"] < 0.20


def test_the_optimistic_end_of_the_threshold_is_an_even_smaller_kill():
    inner = pe.THE_REQUIREMENT_IN_ASSAY_UNITS["at_the_optimistic_end_of_the_threshold"]
    assert inner["required_per_day"] == pe.FIRST_NONZERO_PERSISTER_RATE_PER_DAY
    assert inner["as_a_three_day_kill"] < pe.THE_REQUIREMENT_IN_ASSAY_UNITS["as_a_three_day_kill"]


def test_the_requirement_matches_the_threshold_the_simulation_found():
    """The rate used here must be the one hsa_orthogonal_kill's sweep actually located."""
    table = ok.RESCUE_BY_PERSISTER_KILL
    assert table[0.035] == 0.0, "0.035/day must still be a total failure"
    assert table[0.040] > 0.0, "0.040/day must be where durability first becomes non-zero"
    assert pe.FIRST_NONZERO_PERSISTER_RATE_PER_DAY == 0.040
    assert 0.040 < pe.REQUIRED_PERSISTER_RATE_PER_DAY < 0.050


def test_the_module_does_not_claim_the_requirement_got_easier():
    text = pe.THE_REQUIREMENT_IN_ASSAY_UNITS["what_this_does_not_do"].lower()
    assert "does not lower the requirement" in text
    assert "still a step" in text


def test_the_module_names_where_the_difficulty_moves_rather_than_dropping_it():
    text = pe.THE_REQUIREMENT_IN_ASSAY_UNITS["where_the_difficulty_moves_to"].lower()
    assert "duration" in text and "not potency" in text


# ---------------------------------------------------------------------------------------------
# The in vivo result, and the distinction from the comparison that was retracted.
# ---------------------------------------------------------------------------------------------

def test_the_in_vivo_result_is_measured_on_residual_disease():
    d = pe.THE_IN_VIVO_RESULT_AT_THE_MODELS_OWN_ENDPOINT
    assert "RESIDUAL" in d["the_experiment"]
    assert "RELAPSED" in d["the_result"] and "DID NOT" in d["the_result"]


def test_the_distinction_from_the_retracted_comparison_is_stated_explicitly():
    d = pe.THE_IN_VIVO_RESULT_AT_THE_MODELS_OWN_ENDPOINT
    text = d["why_this_is_not_the_category_error_that_was_retracted"]
    assert "Andersen" in text
    assert "SENSITIVE" in text          # what the retracted comparison measured
    assert "RESIDUAL" in text           # what this one measures
    # And the retraction it refers to must still be present in the other module.
    assert "CATEGORY ERROR" in ok.IT_WORKS_BUT_IT_IS_A_KNIFE_EDGE["the_comparison_that_does_not_work"]


def test_the_genetic_limitation_is_stated_before_any_drug_claim():
    d = pe.THE_IN_VIVO_RESULT_AT_THE_MODELS_OWN_ENDPOINT
    first = d["the_limitation_that_must_be_stated_first"]
    assert "GENETIC" in first
    assert "not a drug" in first
    assert "does not prove any molecule can hit it in vivo" in first
    assert "upper" in d["the_second_limitation"] and "bound" in d["the_second_limitation"]


# ---------------------------------------------------------------------------------------------
# The bioavailability gap: both halves of it.
# ---------------------------------------------------------------------------------------------

def test_the_gap_records_the_toxicology_problem_not_only_the_chemistry_one():
    d = pe.THE_BIOAVAILABILITY_GAP_AS_ORIGINALLY_STATED
    assert "URGENT PRIORITY" in d["the_authors_own_words"]
    assert "LETHAL IN ADULT MICE" in d["the_safety_question_they_also_raised"]
    assert "independent" in d["why_both_are_recorded"]


def test_tubastatin_is_recorded_as_existence_evidence_not_effect_size():
    d = pe.WHAT_HAS_CLOSED_ON_THE_GPX4_ARM
    assert "existence evidence, not effect-size evidence" in d["the_honest_weight"]
    assert "403" in d["what_could_not_be_verified"]
    assert "No effect size from this paper is used" in d["what_could_not_be_verified"]


def test_no_tubastatin_number_leaks_into_any_calculation():
    """If a dose or effect size is ever added, it must not silently become an anchor."""
    blob = repr(pe.WHAT_HAS_CLOSED_ON_THE_GPX4_ARM)
    assert "mg/kg" not in blob and "mg kg" not in blob


def test_the_hdac_tension_is_flagged_rather_than_resolved_in_either_direction():
    d = pe.WHAT_HAS_CLOSED_ON_THE_GPX4_ARM
    t = d["the_tension_with_this_analysis"]
    assert "HDAC_INHIBITION_WAS_TRIED_IN_CANINE_HSA_AND_FAILED" in t
    assert "not automatically inherited" in t
    assert "not automatically escaped" in t
    # The referenced record must actually exist.
    assert ok.HDAC_INHIBITION_WAS_TRIED_IN_CANINE_HSA_AND_FAILED


def test_icfsp1_records_its_controls_and_its_route_limitation():
    d = pe.WHAT_HAS_CLOSED_ON_THE_PARALLEL_ARM
    assert "Q319K" in d["the_on_target_control"]
    assert "liproxstatin" in d["the_rescue_control"]
    assert "INTRAPERITONEAL" in d["the_dosing_that_was_actually_used"]
    assert "mouse route" in d["the_delivery_problem_it_does_not_solve"]


def test_the_persister_fsp1_link_is_labelled_untested():
    d = pe.WHAT_HAS_CLOSED_ON_THE_PARALLEL_ARM
    t = d["the_inference_that_is_tempting_and_is_not_made_here"]
    assert "UNTESTED" in t
    assert "hypothesis, not counted as evidence" in t


def test_the_in_vivo_versus_in_vitro_finding_is_used_conservatively():
    d = pe.WHAT_HAS_CLOSED_ON_THE_PARALLEL_ARM
    assert "IN VIVO, BUT NOT IN VITRO" in d["the_finding_that_changes_the_picture"]
    assert "conservative direction" in d["why_that_matters"]


# ---------------------------------------------------------------------------------------------
# The disease-specific anchor.
# ---------------------------------------------------------------------------------------------

def test_three_named_canine_hemangiosarcoma_lines_are_recorded():
    d = pe.CANINE_HEMANGIOSARCOMA_IS_IN_THE_FERROPTOSIS_PANEL
    assert d["the_hemangiosarcoma_lines"] == ("Cindy-HSA", "Den-HSA", "SB")
    assert set(d["line_provenance"]) == set(d["the_hemangiosarcoma_lines"])


def test_the_breed_and_the_targeted_lesion_both_appear_in_the_panel():
    prov = pe.CANINE_HEMANGIOSARCOMA_IS_IN_THE_FERROPTOSIS_PANEL["line_provenance"]
    assert "Golden Retriever" in prov["Den-HSA"]
    assert "PIK3CA" in prov["SB"]


def test_the_lineage_result_is_class_level_and_the_line_level_gap_is_admitted():
    d = pe.CANINE_HEMANGIOSARCOMA_IS_IN_THE_FERROPTOSIS_PANEL
    assert "SARCOMAS" in d["the_lineage_result"]
    gap = d["what_this_does_not_establish"]
    assert "NOT established" in gap
    assert "inference dressed as a measurement" in gap


def test_the_selectivity_is_attributed_to_the_gpx4_inhibitor_not_to_cytotoxicity():
    d = pe.CANINE_HEMANGIOSARCOMA_IS_IN_THE_FERROPTOSIS_PANEL
    assert "ML210" in d["the_lineage_result"]
    assert "doxorubicin" in d["why_that_lands_on_this_disease"]


def test_the_parental_versus_persister_gap_is_named_as_the_missing_experiment():
    d = pe.CANINE_HEMANGIOSARCOMA_IS_IN_THE_FERROPTOSIS_PANEL
    t = d["and_the_wrong_test"]
    assert "PARENTAL" in t
    assert "Nobody has derived persisters" in t
    for line in d["the_hemangiosarcoma_lines"]:
        assert line in t


def test_the_preprint_status_is_restated_here_not_only_in_the_other_module():
    d = pe.CANINE_HEMANGIOSARCOMA_IS_IN_THE_FERROPTOSIS_PANEL
    assert "preprint" in d["the_status_caveat"]
    assert "preprint" in ok.CANINE_CELLS_ARE_FERROPTOSIS_COMPETENT["the_status_caveat"]


# ---------------------------------------------------------------------------------------------
# The transfer table.
# ---------------------------------------------------------------------------------------------

def test_transfer_table_covers_a_pessimistic_and_an_optimistic_end():
    ks = sorted(pe.TRANSFER_REQUIRED_BY_ASSUMED_POTENCY)
    assert min(ks) <= 0.10 and max(ks) >= 0.75


def test_transfer_table_entries_are_internally_consistent():
    for v, row in pe.TRANSFER_REQUIRED_BY_ASSUMED_POTENCY.items():
        assert row["implied_rate_per_day"] == pytest.approx(rate_from_burden_reduction(v, 3.0))
        assert row["transfer_required_for_0_045"] == pytest.approx(
            0.045 / row["implied_rate_per_day"])
        # The easier target must always need less transfer.
        assert row["transfer_required_for_0_040"] < row["transfer_required_for_0_045"]


def test_every_assumed_potency_needs_a_minority_of_the_measured_effect():
    """The claim in HOW_THE_TRANSFER_ASK_COMPARES depends on this holding across the whole range."""
    for row in pe.TRANSFER_REQUIRED_BY_ASSUMED_POTENCY.values():
        assert row["transfer_required_for_0_045"] < 0.5


def test_the_pessimistic_end_is_still_the_worst_case_and_is_quoted_as_such():
    worst = pe.TRANSFER_REQUIRED_BY_ASSUMED_POTENCY[0.75]["transfer_required_for_0_045"]
    assert worst == pytest.approx(0.469, abs=2e-3)
    assert "47%" in pe.HOW_THE_TRANSFER_ASK_COMPARES["the_range"]


def test_the_withdrawal_of_the_earlier_overstatement_is_explicit():
    d = pe.HOW_THE_TRANSFER_ASK_COMPARES
    assert "WRONG" in d["what_this_overturns"]
    assert "withdrawn" in d["what_this_overturns"]
    assert "essentially all of whatever it has" in d["what_this_overturns"]
    # The sentence being withdrawn must still be findable in the module it came from,
    # so the correction has something to point at.
    assert "essentially all of whatever it has" in \
        ok.IT_WORKS_BUT_IT_IS_A_KNIFE_EDGE["how_this_compares_to_the_other_routes"]


def test_the_half_that_still_stands_is_kept():
    d = pe.HOW_THE_TRANSFER_ASK_COMPARES
    t = d["what_it_does_not_overturn"]
    assert "no measured in vivo per-day rate" in t
    assert "sensitivity analysis rather than a measurement" in t


# ---------------------------------------------------------------------------------------------
# The duration criterion applied to this agent. These tests exist because a criterion that is only
# ever applied to rejected options is not a criterion.
# ---------------------------------------------------------------------------------------------

def test_the_chronic_shortcut_is_disqualified_on_canine_evidence():
    d = pe.THE_CHRONIC_ENTRY_POINT_AND_WHY_IT_FAILS_IN_DOGS
    assert "PERMANENT" in d["the_canine_finding"]["the_result"]
    assert "cannot be dodged by patient selection" in d["the_canine_finding"]["no_susceptible_subgroup"]


def test_the_toxicity_timescale_is_inside_the_modelled_horizon():
    d = pe.THE_CHRONIC_ENTRY_POINT_AND_WHY_IT_FAILS_IN_DOGS["the_timescale_that_makes_it_a_duration_problem"]
    assert "STUDY WEEK 22" in d["the_result"]
    assert "PROGRESSED" in d["the_result"]
    # Week 22 is ~154 days, far inside the 3650-day horizon this analysis models.
    assert 22 * 7 < 3650
    assert "3650" in d["why_this_is_the_decisive_number"]


def test_the_species_specific_signal_records_the_mechanism_not_just_the_finding():
    d = pe.THE_CHRONIC_ENTRY_POINT_AND_WHY_IT_FAILS_IN_DOGS["the_second_dog_specific_signal_in_the_same_class"]
    assert "ONLY IN DOGS" in d["the_result"]
    assert "3400" in d["the_mechanism_of_the_species_difference"]
    assert "does not transfer to dogs" in d["why_it_is_recorded"]


def test_the_ruling_out_is_scoped_to_the_shortcut_not_the_mechanism():
    d = pe.THE_CHRONIC_ENTRY_POINT_AND_WHY_IT_FAILS_IN_DOGS
    assert "sulfasalazine" in d["what_this_rules_out"]
    assert "rules out one shortcut into the axis, not the axis" in d["what_it_does_not_rule_out"]


def test_the_criterion_is_applied_to_the_favoured_mechanism_not_only_the_rejected_one():
    """The whole point of recording this: the duration criterion must cut both ways."""
    d = pe.THE_CHRONIC_ENTRY_POINT_AND_WHY_IT_FAILS_IN_DOGS
    sym = d["the_uncomfortable_symmetry"]
    assert "same failure mode" in sym
    assert "second drug" in sym
    # And the criterion it is being borrowed from must still exist and still be about the horizon.
    from canine_dsp import hsa_alternative_approach as aa
    assert aa.THE_DURATION_CRITERION


def test_the_field_level_contradiction_of_the_optimistic_gpx4_reading_is_kept():
    d = pe.WHAT_HAS_CLOSED_ON_THE_GPX4_ARM
    c = d["THE_FIELD_DOES_NOT_AGREE_THAT_THIS_IS_SETTLED"]
    assert "HIGH TOXICITY" in c and "LOW-TO-LIMITED BIOAVAILABILITY" in c
    assert "pessimistic side as the operating assumption" in c
    # The optimistic sentence it contradicts must still be present, not quietly deleted.
    assert "no longer entirely" in d["why_it_matters_here"]


def test_the_fsp1_therapeutic_window_argument_is_genetic_not_pharmacological():
    w = pe.WHAT_HAS_CLOSED_ON_THE_PARALLEL_ARM[
        "THE_THERAPEUTIC_WINDOW_ARGUMENT_THAT_ANSWERS_HANGAUERS_SECOND_PROBLEM"]
    assert "NOT VIABLE" in w["the_statement"]
    assert "VIABLE WITH NO NOTABLE PHYSIOLOGICAL DEFECTS" in w["the_statement"]
    assert "does NOT establish chronic tolerability" in w["what_it_does_and_does_not_establish"]


def test_the_duration_shortfall_is_computed_and_is_worse_than_the_rejected_pair():
    w = pe.WHAT_HAS_CLOSED_ON_THE_PARALLEL_ARM[
        "THE_THERAPEUTIC_WINDOW_ARGUMENT_THAT_ANSWERS_HANGAUERS_SECOND_PROBLEM"]
    assert w["the_documented_tolerability_days"] == 14
    assert w["the_horizon_days"] == 3650
    assert w["the_shortfall_multiple"] == pytest.approx(3650 / 14)
    # The analysis must not flatter its own preferred mechanism.
    assert w["the_shortfall_multiple"] > 215
    assert "worse shape than the one the analysis rejected" in \
        w["how_that_compares_to_the_disqualified_pair"]


def test_the_duration_shortfall_uses_the_same_horizon_as_the_original_criterion():
    from canine_dsp import hsa_alternative_approach as aa
    w = pe.WHAT_HAS_CLOSED_ON_THE_PARALLEL_ARM[
        "THE_THERAPEUTIC_WINDOW_ARGUMENT_THAT_ANSWERS_HANGAUERS_SECOND_PROBLEM"]
    assert str(w["the_horizon_days"]) in repr(aa.THE_DURATION_CRITERION)


# ---------------------------------------------------------------------------------------------
# The finite course: the closed form, the exchange rate, and the assumption carrying all of it.
# ---------------------------------------------------------------------------------------------

def test_required_rate_falls_as_the_course_lengthens():
    rates = [pe.required_rate_for_course(d) for d in (152, 335, 700, 3620)]
    assert rates == sorted(rates, reverse=True)


def test_required_rate_tends_to_the_holding_rate_for_an_endless_course():
    assert pe.required_rate_for_course(10_000_000) == pytest.approx(
        pe.BLIND_SPOT_NET_GROWTH_PER_DAY, abs=1e-4)
    # And can never fall below it: holding the compartment still is the floor on the ask.
    for d in (10, 152, 3620):
        assert pe.required_rate_for_course(d) > pe.BLIND_SPOT_NET_GROWTH_PER_DAY


def test_required_rate_is_the_holding_rate_plus_the_work_over_the_time():
    d = 335
    expected = pe.BLIND_SPOT_NET_GROWTH_PER_DAY + math.log(pe.blind_spot_initial_cells()) / d
    assert pe.required_rate_for_course(d) == pytest.approx(expected)


def test_required_rate_rejects_a_nonpositive_course():
    with pytest.raises(ValueError):
        pe.required_rate_for_course(0)


def test_the_blind_spot_size_matters_only_logarithmically():
    """The claim in the sensitivity section: a ten-fold size error is small next to the ask."""
    base = pe.required_rate_for_course(335)
    tenfold = pe.required_rate_for_course(335, fraction=pe.BLIND_SPOT_INITIAL_FRACTION * 10)
    assert tenfold - base == pytest.approx(math.log(10) / 335, abs=1e-6)
    assert tenfold - base < 0.01
    assert (tenfold - base) / base < 0.10


def test_the_closed_form_predicts_every_simulated_threshold():
    """Each schedule's predicted rate must sit inside the interval the simulation brackets.

    Three outcomes, not two. The closed form predicts a single deterministic threshold, but the
    growth offset varies between Monte Carlo trials, so a rate sitting on the threshold returns an
    intermediate durability rather than 0 or 1. An intermediate value is therefore evidence that the
    true threshold is AT that rate -- it must bracket the prediction, not fall on one side of it.
    Treating it as a failure (the first version of this test) wrongly failed the continuous
    schedule, whose 0.040 -> 0.117 is the clearest boundary point in the table.
    """
    table = pe.FINITE_COURSE_RESCUE
    rates = sorted(table)
    tol = 2e-3
    for name in pe.PERSISTER_COURSE_AGENT_DAYS:
        predicted = pe.required_rate_for_course(pe.PERSISTER_COURSE_AGENT_DAYS[name])
        succeeded = [r for r in rates if table[r][name] >= 0.99]
        failed = [r for r in rates if table[r][name] <= 0.01]
        boundary = [r for r in rates if 0.01 < table[r][name] < 0.99]
        if succeeded:
            assert min(succeeded) >= predicted - tol, f"{name}: cleared below the predicted threshold"
        if failed:
            assert max(failed) <= predicted + tol, f"{name}: failed above the predicted threshold"
        for r in boundary:
            # A partial result means the prediction should be sitting essentially on this rate.
            assert abs(r - predicted) < 0.01, f"{name}: partial result far from the prediction"


def test_the_boundary_case_is_the_one_the_module_calls_out():
    """The continuous schedule is the only partial entry, and the module says so explicitly."""
    partials = [(r, n) for r, row in pe.FINITE_COURSE_RESCUE.items()
                for n, v in row.items() if 0.01 < v < 0.99]
    assert partials == [(0.040, "continuous")]
    assert "0.117" in pe.THE_CLOSED_FORM_PREDICTS_THE_SIMULATION["the_check"]["continuous"]


def test_the_two_short_schedules_fail_at_every_rate_tested():
    for rate, row in pe.FINITE_COURSE_RESCUE.items():
        assert row["six_months"] == 0.0
        assert row["pulsed_14_28_during_drug_year"] == 0.0


def test_durability_is_monotone_in_rate_for_every_schedule():
    rates = sorted(pe.FINITE_COURSE_RESCUE)
    for name in pe.PERSISTER_COURSE_AGENT_DAYS:
        col = [pe.FINITE_COURSE_RESCUE[r][name] for r in rates]
        assert col == sorted(col), name


def test_a_longer_course_is_never_worse_at_a_fixed_rate():
    order = ["six_months", "pulsed_14_28_during_drug_year", "drug_year", "two_years", "continuous"]
    # six_months (152d) and the pulsed schedule (167d) are close enough to tie; the rest must rise.
    for rate, row in pe.FINITE_COURSE_RESCUE.items():
        vals = [row[n] for n in order]
        assert vals == sorted(vals), rate


def test_agent_days_are_ordered_the_way_the_schedules_claim():
    d = pe.PERSISTER_COURSE_AGENT_DAYS
    assert d["continuous"] > d["two_years"] > d["drug_year"] > d["pulsed_14_28_during_drug_year"]
    assert d["pulsed_14_28_during_drug_year"] > d["six_months"]
    # The pulsed schedule really is about half the drug year's exposure.
    assert d["pulsed_14_28_during_drug_year"] / d["drug_year"] == pytest.approx(0.5, abs=0.02)


def test_the_exchange_rate_claim_matches_the_computed_rates():
    one_year = pe.REQUIRED_RATE_BY_COURSE["drug_year"]
    forever = pe.REQUIRED_RATE_BY_COURSE["continuous"]
    # "roughly a doubling"
    assert 1.8 < one_year["required_rate_per_day"] / forever["required_rate_per_day"] < 2.6
    # "a three-day kill rising from about 14% to about 26%" -- both still modest.
    assert 0.09 < forever["as_a_three_day_kill"] < 0.16
    assert 0.20 < one_year["as_a_three_day_kill"] < 0.30


def test_the_shortfall_improvement_the_exchange_rate_claims():
    one_year_days = pe.PERSISTER_COURSE_AGENT_DAYS["drug_year"]
    icfsp1_days = pe.WHAT_HAS_CLOSED_ON_THE_PARALLEL_ARM[
        "THE_THERAPEUTIC_WINDOW_ARGUMENT_THAT_ANSWERS_HANGAUERS_SECOND_PROBLEM"][
        "the_documented_tolerability_days"]
    assert one_year_days / icfsp1_days == pytest.approx(24.0, abs=0.5)
    assert "261x to 24x" in pe.THE_EXCHANGE_RATE_BETWEEN_DURATION_AND_POTENCY["what_it_buys"]


def test_the_pulsing_failure_is_reported_against_the_authors_own_convenience():
    d = pe.THE_EXCHANGE_RATE_BETWEEN_DURATION_AND_POTENCY
    assert "does NOT license a duty cycle" in d["where_it_stops_buying"]
    assert "result against my own convenience" in d["the_honest_reading_of_the_pulsing_failure"]


def test_the_control_shows_the_floor_carries_the_entire_finite_result():
    ctl = pe.FINITE_COURSE_WITHOUT_THE_EXTINCTION_FLOOR
    assert ctl["continuous"] == 1.0
    for name in ("two_years", "drug_year", "pulsed_14_28_during_drug_year"):
        assert ctl[name] == 0.0
    # ...while the floored table has two of those succeeding at the same rate.
    assert pe.FINITE_COURSE_RESCUE[0.100]["two_years"] == 1.0
    assert pe.FINITE_COURSE_RESCUE[0.100]["drug_year"] == 1.0


def test_the_dependence_on_the_floor_is_stated_as_load_bearing_not_marginal():
    d = pe.EVERYTHING_IN_SECTION_7_DEPENDS_ON_THE_FLOOR
    assert "not a caveat at the" in d["so_the_result_is_entirely_a_consequence_of_the_assumption"]
    w = d["where_the_choice_could_still_be_wrong"]
    assert "has NOT run one" in w["stochasticity_at_low_numbers"]
    assert "two-log window" in w["how_close_the_calls_are"]
    assert "sanctuary" in w["sanctuary_sites"]


def test_the_open_items_outnumber_the_closures_and_include_the_cheap_alternative():
    items = pe.WHAT_IS_STILL_NOT_CLOSED
    assert len(items) >= 8
    joined = " ".join(items.values())
    assert "genetic knockout" in joined
    assert "PARENTAL" in joined
    assert "sensitivity analysis" in joined
    assert "stain" in joined


def test_the_verdict_refuses_to_call_it_closed():
    v = pe.VERDICT
    assert v["the_status"].startswith("CLOSED CONDITIONAL ON A NAMED EXPERIMENT")
    assert "weaker one than 'closed'" in v["the_status"]
    assert "no drug has been shown to do it" in v["what_did_not_change"].lower()
    assert "'Nearly solvable' is not closed" in v["what_this_module_refuses_to_say"]


def test_the_verdict_names_the_experiment_concretely_enough_to_run():
    v = pe.VERDICT["the_status"]
    for line in pe.CANINE_HEMANGIOSARCOMA_IS_IN_THE_FERROPTOSIS_PANEL["the_hemangiosarcoma_lines"]:
        assert line in v
    assert "rate_from_burden_reduction" in v
    assert "required_rate_for_course(335)" in v
    # And the number it quotes must be the one the function returns.
    assert pe.required_rate_for_course(335) == pytest.approx(0.090, abs=5e-4)


def test_the_cheap_step_still_comes_first():
    assert "stain first" in pe.VERDICT["the_order_to_do_it_in"].replace("\n", " ") or \
        "stain" in pe.VERDICT["the_order_to_do_it_in"]
    assert "unnecessary" in pe.VERDICT["the_order_to_do_it_in"]
