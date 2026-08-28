"""Tests for the search for a cheaper or different closure of route 8.

Two jobs here. The usual one: stop the module claiming more than its sources support. And a second
one specific to this module: stop it claiming LESS than it found, because three of its four sections
are negative results and negative results are easy to soften later into "inconclusive".
"""
import math

import pytest

from canine_dsp import hsa_persister_evidence as pe
from canine_dsp import hsa_route8_alternatives as ra


# ---------------------------------------------------------------------------------------------
# The structural result: smaller or slower is not enough.
# ---------------------------------------------------------------------------------------------

def test_days_to_detection_is_zero_for_a_blind_spot_already_above_the_floor():
    # The 95% coverage case: 0.3 * 0.05 = 0.015, above the 0.01 floor. Macroscopic on day one.
    assert ra.days_to_detection(0.015) == 0.0


def test_days_to_detection_is_logarithmic_in_size():
    """A hundred-fold smaller blind spot buys only ln(100)/rate days."""
    a = ra.days_to_detection(0.003)
    b = ra.days_to_detection(0.00003)
    assert b - a == pytest.approx(math.log(100) / ra.BLIND_SPOT_NET_GROWTH_PER_DAY, abs=1e-6)


def test_even_extreme_coverage_buys_far_less_than_the_horizon():
    """The claim that coverage is not the lever."""
    for fraction in (0.003, 0.0003, 0.00003):
        assert ra.days_to_detection(fraction) < 0.10 * ra.HORIZON_DAYS


def test_a_heavy_fitness_penalty_still_does_not_reach_the_horizon():
    """99.99% coverage plus a 70% growth penalty: the module quotes 581 days."""
    slowed = ra.BLIND_SPOT_NET_GROWTH_PER_DAY * 0.30
    d = ra.days_to_detection(0.3 * 0.0001, net_growth=slowed)
    assert d == pytest.approx(581, abs=5)
    assert d < ra.HORIZON_DAYS


def test_days_to_detection_rejects_nonpositive_inputs():
    with pytest.raises(ValueError):
        ra.days_to_detection(0.0)
    with pytest.raises(ValueError):
        ra.days_to_detection(0.001, net_growth=0.0)


def test_the_coverage_numbers_recorded_match_the_function():
    for coverage, days in ra.COVERAGE_DOES_NOT_CLOSE_IT_EITHER["the_numbers"].items():
        assert ra.days_to_detection(0.3 * (1 - coverage)) == pytest.approx(days, abs=1.0)


def test_the_three_failures_are_attributed_to_one_shared_cause():
    d = ra.THE_ONE_REASON_ALL_THREE_FAIL
    assert "SMALLER or SLOWER" in d["the_result"]
    assert "NET GROWTH NEGATIVE" in d["the_structural_statement"]
    assert "581 days" in d["the_arithmetic"]


def test_the_structural_result_is_recorded_as_strengthening_the_expensive_answer():
    """This is the uncomfortable direction, so it must be stated rather than buried."""
    d = ra.THE_ONE_REASON_ALL_THREE_FAIL
    assert "NECESSARY" in d["why_this_is_worth_more_than_the_three_negatives"]
    assert "not the outcome I was hoping for" in d["the_honest_note"]


def test_containment_failure_names_both_reasons_including_the_disease_specific_one():
    d = ra.WHY_CONTAINMENT_IS_NOT_AVAILABLE_HERE
    assert "macroscopic on day one" in d["why_it_does_not_work_here"]
    assert "haemorrhage" in d["the_second_reason_specific_to_this_disease"]
    assert "route 5" in d["the_second_reason_specific_to_this_disease"]


def test_containment_is_credited_with_the_insight_it_does_supply():
    d = ra.WHY_CONTAINMENT_IS_NOT_AVAILABLE_HERE
    assert "0.0334" in d["what_it_is_still_good_for"]
    assert "consequence of the nadir" in d["what_it_is_still_good_for"]


def test_the_fitness_cost_inconsistency_is_recorded_as_my_error_not_a_finding():
    d = ra.THE_FITNESS_COST_INCONSISTENCY_I_HAD_NOT_NOTICED
    assert "0% when it is present at baseline" in d["the_inconsistency"]
    assert "assumption, not a finding" in d["is_the_asymmetry_defensible"]
    assert "favoured my own" in d["why_it_is_recorded_anyway"]
    assert "0.000" in d["what_correcting_it_does"]


# ---------------------------------------------------------------------------------------------
# The prior-art negative.
# ---------------------------------------------------------------------------------------------

def test_metronomic_is_recorded_as_tested_in_this_disease_and_failed():
    d = ra.METRONOMIC_CHEMOTHERAPY_WAS_TESTED_AND_FAILED
    assert "DOES NOT IMPROVE OUTCOME" in d["the_result"]
    assert "clear the duration criterion" in d["why_it_was_the_best_candidate"]
    assert "Passing the gates on paper is not the same as working" in d["why_it_matters"]


# ---------------------------------------------------------------------------------------------
# The third mechanism.
# ---------------------------------------------------------------------------------------------

def test_ebat_clears_both_orthogonality_gates_for_stated_reasons():
    d = ra.EBAT_IS_THE_THIRD_MECHANISM
    assert "elongation factor 2" in d["how_it_kills"]
    gate = d["why_it_clears_the_orthogonality_gate"]
    assert "no shared node" in gate
    assert "unrelated to the vaccine antigens" in gate


def test_ebat_setting_matches_what_the_model_simulates():
    d = ra.EBAT_IS_THE_THIRD_MECHANISM
    assert "SPLENIC HEMANGIOSARCOMA" in d["the_trial"]
    assert "MINIMAL RESIDUAL DISEASE" in d["the_trial"]
    assert "the disease, the species and the setting" in d["why_the_setting_is_exactly_right"]


def test_ebat_coverage_question_is_admitted_not_hidden():
    d = ra.EBAT_IS_THE_THIRD_MECHANISM
    t = d["the_coverage_question_it_reintroduces"]
    assert "does not escape the coverage problem" in t
    assert "independence is assumed" in t


def test_the_negative_trial_is_recorded_and_rules_out_scaling_up():
    d = ra.EBAT_ALSO_HAS_A_NEGATIVE_TRIAL_AND_IT_IS_INFORMATIVE
    assert "was NOT seen" in d["the_result"]
    assert "GREATER TOXICITY AND REDUCED EFFICACY" in d["the_result"]
    assert "ruled out by data, not by argument" in d["so_more_is_worse"]


def test_the_convergence_with_the_model_is_flagged_as_confounded():
    d = ra.EBAT_ALSO_HAS_A_NEGATIVE_TRIAL_AND_IT_IS_INFORMATIVE
    assert "changed three things at once" in d["why_that_convergence_must_not_be_oversold"]
    assert "confounded" in d["why_that_convergence_must_not_be_oversold"]


# ---------------------------------------------------------------------------------------------
# The conversion, which is the module's one quantitative claim.
# ---------------------------------------------------------------------------------------------

def test_one_off_logs_matches_hand_arithmetic():
    # 6-month survival 0.40 -> 0.70. Medians 138 and 354 days; delay 216; times 0.0334 = 7.2 logs.
    assert ra.one_off_logs_from_survival(0.40, 0.70) == pytest.approx(7.21, abs=0.05)


def test_one_off_logs_rises_with_the_benefit():
    seq = [ra.one_off_logs_from_survival(0.40, s) for s in (0.55, 0.65, 0.70, 0.80)]
    assert seq == sorted(seq)


def test_one_off_logs_rejects_a_non_benefit_and_bad_fractions():
    with pytest.raises(ValueError):
        ra.one_off_logs_from_survival(0.70, 0.40)
    with pytest.raises(ValueError):
        ra.one_off_logs_from_survival(0.0, 0.70)
    with pytest.raises(ValueError):
        ra.one_off_logs_from_survival(0.40, 1.0)


def test_ebat_supplies_a_minority_of_the_required_logs_under_every_variant():
    lo, hi = ra.HOW_MUCH_OF_THE_JOB_EBAT_DOES["fraction_of_the_job"]
    assert 0.2 < lo < hi < 0.5
    assert "not a closure on its own" in ra.HOW_MUCH_OF_THE_JOB_EBAT_DOES["the_reading"]


def test_the_total_logs_required_is_the_same_number_the_other_module_uses():
    assert ra.TOTAL_LOGS_REQUIRED == pytest.approx(
        math.log(pe.blind_spot_initial_cells()))
    assert ra.TOTAL_LOGS_REQUIRED == pytest.approx(18.83, abs=0.01)


def test_the_weakest_assumption_is_named_as_the_historical_control():
    t = ra.HOW_MUCH_OF_THE_JOB_EBAT_DOES["the_assumptions_this_rests_on"]
    assert "not a control arm" in t


# ---------------------------------------------------------------------------------------------
# The combination.
# ---------------------------------------------------------------------------------------------

def test_a_head_start_reduces_the_subsequent_requirement():
    rates = [ra.required_rate_after_a_head_start(x) for x in (0.0, 5.2, 7.2, 10.8)]
    assert rates == sorted(rates, reverse=True)


def test_a_head_start_of_everything_leaves_nothing_to_do():
    assert ra.required_rate_after_a_head_start(ra.TOTAL_LOGS_REQUIRED + 1) == 0.0


def test_no_head_start_reproduces_the_standalone_requirement():
    assert ra.required_rate_after_a_head_start(0.0) == pytest.approx(
        pe.required_rate_for_course(335))


def test_the_combination_table_matches_the_function_and_the_quoted_discount():
    tbl = ra.THE_COMBINATION_THAT_IS_NOW_LEGITIMATE["what_it_buys"]
    for logs, rate in tbl.items():
        assert rate == pytest.approx(ra.required_rate_after_a_head_start(logs))
    alone = tbl[0.0]
    assert tbl[5.2] / alone == pytest.approx(0.83, abs=0.02)     # ~17% discount
    assert tbl[10.8] / alone == pytest.approx(0.64, abs=0.02)    # ~36% discount
    assert "0.055-0.074/day" in ra.THE_COMBINATION_THAT_IS_NOW_LEGITIMATE["the_reading"]


def test_the_combination_says_why_it_is_allowed_now_and_was_not_before():
    d = ra.THE_COMBINATION_THAT_IS_NOW_LEGITIMATE
    assert "two unmeasured quantities" in d["what_was_refused_before"]
    assert "one measured quantity with one unmeasured one" in d["why_this_combination_is_different"]
    assert "still weaker than combining two measured ones" in d["why_this_combination_is_different"]
    assert "never been tested" in d["what_has_never_been_tested"]


# ---------------------------------------------------------------------------------------------
# The anecdote, and the verdict.
# ---------------------------------------------------------------------------------------------

def test_the_oncolytic_case_is_quarantined_as_an_anecdote():
    d = ra.ONCOLYTIC_VIRUS_IS_AN_ANECDOTE_NOT_EVIDENCE
    assert "n = 1" in d["why_it_is_recorded_as_an_anecdote"]
    assert "No rate is derived from it and none should be" in d["why_it_is_recorded_as_an_anecdote"]
    # And no number from it may leak into any calculation in this module.
    assert "seven years" not in repr(ra.HOW_MUCH_OF_THE_JOB_EBAT_DOES)
    assert "seven years" not in repr(ra.THE_COMBINATION_THAT_IS_NOW_LEGITIMATE)


def test_the_verdict_does_not_upgrade_the_route_to_closed():
    v = ra.VERDICT_ON_THE_SEARCH
    assert "CLOSED CONDITIONAL ON A NAMED EXPERIMENT" in v["the_net_effect_on_the_verdict"]
    assert v["the_thing_i_still_cannot_say"].startswith("that route 8 is closed")
    assert "nobody has ever shown that such a" in v["the_thing_i_still_cannot_say"]


def test_the_verdict_reports_the_negative_side_of_the_search_first():
    v = ra.VERDICT_ON_THE_SEARCH
    assert v["what_was_found_on_the_cheap_side"].startswith("nothing")


def test_the_next_experiment_is_a_stain_not_a_programme():
    v = ra.VERDICT_ON_THE_SEARCH["what_would_change_it_most_now"]
    assert "EGFR and uPAR" in v
    assert "stain, not a programme" in v


def test_the_combination_does_not_describe_the_ferroptosis_side_as_measured():
    """This caught a real contradiction: the entry claimed two measured effects, which is false."""
    d = ra.THE_COMBINATION_THAT_IS_NOW_LEGITIMATE
    t = d["what_has_never_been_tested"]
    assert "one measured effect and one assumed one" in t
    assert "two separately measured effects', which is false" in t
    # And it must not be reintroduced anywhere in the entry.
    assert "arithmetic on two separately measured effects" not in repr(d)


def test_the_sweep_is_uniformly_zero_across_every_combination():
    """Twenty of twenty. If any cell ever becomes non-zero, the structural claim needs revisiting."""
    for coverage, row in ra.COVERAGE_TIMES_FITNESS_COST.items():
        for cost, value in row.items():
            assert value == 0.0, f"coverage {coverage}, cost {cost}"


def test_the_sweep_spans_a_wide_enough_range_to_mean_something():
    covs = sorted(ra.COVERAGE_TIMES_FITNESS_COST)
    assert min(covs) <= 0.95 and max(covs) >= 0.995
    costs = sorted(next(iter(ra.COVERAGE_TIMES_FITNESS_COST.values())))
    assert min(costs) == 0.0 and max(costs) >= 0.50
    # The engine's own antigen-loss penalty must be one of the values tested.
    assert 0.15 in costs


def test_the_sweep_conclusion_does_not_overreach_into_vaccine_design():
    d = ra.WHAT_THE_SWEEP_SETTLES
    assert "nothing to tune toward" in d["why_a_uniformly_null_table_is_the_strongest_form_of_this_result"]
    assert "not about vaccine design" in d["the_one_reading_it_does_not_support"]
    assert "WHEN the blind spot arrives, not WHETHER" in \
        d["why_a_uniformly_null_table_is_the_strongest_form_of_this_result"]


# ---------------------------------------------------------------------------------------------
# The stability requirement, the plasticity drain, and the two-term decomposition.
# ---------------------------------------------------------------------------------------------

def test_the_horizon_costs_hundreds_of_generations():
    assert ra.GENERATIONS_OVER_HORIZON == pytest.approx(263, abs=2)
    assert ra.BLIND_SPOT_DOUBLING_DAYS == pytest.approx(13.9, abs=0.2)


def test_null_lineage_survival_collapses_with_modest_reversion():
    assert ra.null_lineage_surviving(0.10) < 1e-10
    assert ra.null_lineage_surviving(0.01) == pytest.approx(0.071, abs=0.01)
    assert ra.null_lineage_surviving(0.0) == 1.0


def test_null_lineage_survival_is_monotone_and_validated():
    seq = [ra.null_lineage_surviving(p) for p in (0.0, 0.001, 0.01, 0.1)]
    assert seq == sorted(seq, reverse=True)
    with pytest.raises(ValueError):
        ra.null_lineage_surviving(1.0)
    with pytest.raises(ValueError):
        ra.null_lineage_surviving(-0.1)


def test_the_recorded_stability_table_matches_the_function():
    for p, frac in ra.THE_STABILITY_THE_DANGEROUS_CASE_REQUIRES["how_fragile_that_requirement_is"].items():
        assert frac == pytest.approx(ra.null_lineage_surviving(p), rel=1e-9)


def test_the_stability_question_records_both_sides():
    d = ra.THE_STABILITY_THE_DANGEROUS_CASE_REQUIRES
    assert "TRANSIENT" in d["what_the_persister_literature_says"]
    assert "JAK1/JAK2" in d["what_cuts_the_other_way"]
    assert "B2M" in d["what_cuts_the_other_way"]
    assert "so_the_question_has_a_binary_answer" in d
    assert "Both exist in real tumours" in d["so_the_question_has_a_binary_answer"]


def test_plasticity_is_labelled_a_log_remover_not_a_closure():
    d = ra.PLASTICITY_DRAINS_THE_SANCTUARY_BUT_ONLY_THE_EPIGENETIC_PART
    assert "why_this_is_not_a_closure_on_its_own" in d
    assert "genetically deleted one" in d["why_this_is_not_a_closure_on_its_own"]
    assert "unless the genetic fraction is exactly zero" in d["why_this_is_not_a_closure_on_its_own"]
    assert "log-remover" in d["what_it_therefore_is"]


def test_the_plasticity_threshold_matches_the_holding_rate():
    """The one-way claim stands; the two-way estimate is marked wrong rather than deleted."""
    d = ra.PLASTICITY_DRAINS_THE_SANCTUARY_BUT_ONLY_THE_EPIGENETIC_PART
    assert "0.0334" in d["the_mechanism"]
    assert ra.BLIND_SPOT_NET_GROWTH_PER_DAY / 0.042 == pytest.approx(0.795, abs=0.005)
    # The superseded estimate must still be quoted, and marked as superseded.
    assert "0.795" in d["the_two_way_version"]
    assert "THAT ESTIMATE IS WRONG" in d["the_two_way_version"]
    assert "THE_TWO_WAY_RESULT_INVERTS_THE_IDEA" in d["the_two_way_version"]


def test_bystander_failure_is_attributed_to_supply_not_to_potency():
    d = ra.BYSTANDER_KILLING_FAILS_FOR_A_REASON_WORTH_RECORDING
    assert "DISSIPATE" in d["the_finding_that_kills_it"]
    assert "factory" in d["the_shape_this_shares_with_containment"]
    assert "category of false answer worth naming" in d["the_shape_this_shares_with_containment"]


def test_bystander_and_containment_are_linked_as_the_same_trap():
    d = ra.BYSTANDER_KILLING_FAILS_FOR_A_REASON_WORTH_RECORDING
    t = d["the_shape_this_shares_with_containment"]
    assert "competitive release" in t.lower() or "competition" in t.lower()
    assert "the very population the plan is designed to destroy" in t


# ---------------------------------------------------------------------------------------------
# The decomposition.
# ---------------------------------------------------------------------------------------------

def test_the_decomposition_reproduces_the_standalone_requirement():
    r = ra.required_rate_decomposed(ra.BLIND_SPOT_NET_GROWTH_PER_DAY, ra.blind_spot_initial_cells())
    assert r == pytest.approx(pe.required_rate_for_course(335), rel=1e-9)


def test_the_decomposition_floors_at_the_holding_rate():
    """No amount of up-front removal takes the requirement below the floor."""
    for cells in (1e8, 1e4, 10.0, 1.0):
        r = ra.required_rate_decomposed(ra.BLIND_SPOT_NET_GROWTH_PER_DAY, cells)
        assert r >= ra.BLIND_SPOT_NET_GROWTH_PER_DAY
    assert ra.required_rate_decomposed(ra.BLIND_SPOT_NET_GROWTH_PER_DAY, 1.0) == pytest.approx(
        ra.BLIND_SPOT_NET_GROWTH_PER_DAY)


def test_the_decomposition_returns_zero_only_when_nothing_survives():
    assert ra.required_rate_decomposed(ra.BLIND_SPOT_NET_GROWTH_PER_DAY, 0.5) == 0.0
    with pytest.raises(ValueError):
        ra.required_rate_decomposed(0.03, 1e5, course_days=0)


def test_a_longer_course_lowers_the_requirement_toward_the_floor():
    long = ra.required_rate_decomposed(ra.BLIND_SPOT_NET_GROWTH_PER_DAY, 1e5, course_days=100000)
    assert long == pytest.approx(ra.BLIND_SPOT_NET_GROWTH_PER_DAY, abs=1e-3)


def test_the_floor_is_only_moved_by_lowering_growth():
    tbl = ra.THE_TWO_TERMS_AND_THEIR_DIFFERENT_LEVERS["what_actually_lowers_the_floor"]
    vals = [tbl[c] for c in sorted(tbl)]
    assert vals == sorted(vals, reverse=True)
    # 0% penalty must equal a 9.5% three-day kill at the measured holding rate.
    assert tbl[0.0] == pytest.approx(1 - pe.viability_after(ra.BLIND_SPOT_NET_GROWTH_PER_DAY), abs=0.002)


def test_the_decomposition_reconciles_the_earlier_rejections():
    d = ra.THE_TWO_TERMS_AND_THEIR_DIFFERENT_LEVERS
    t = d["the_reconciliation_this_provides"]
    assert "not worthless" in t
    assert "rejected as a CLOSURE" in t and "real as a TERM" in t


def test_the_stack_is_monotone_and_never_reaches_zero():
    entries = sorted(ra.THE_STACK.values())
    logs = [v[0] for v in ra.THE_STACK.values()]
    rates = [v[1] for v in ra.THE_STACK.values()]
    # More logs removed must never mean a higher requirement.
    pairs = sorted(zip(logs, rates))
    assert [r for _, r in pairs] == sorted([r for _, r in pairs], reverse=True)
    # And every entry stays above the irreducible floor.
    for r in rates:
        assert r > ra.BLIND_SPOT_NET_GROWTH_PER_DAY


def test_the_stack_numbers_match_the_quoted_summary():
    assert ra.THE_STACK["nothing"][1] == pytest.approx(0.090, abs=0.002)
    assert ra.THE_STACK["eBAT alone"][1] == pytest.approx(0.068, abs=0.002)
    assert ra.THE_STACK["eBAT plus plasticity to 1e5"][1] == pytest.approx(0.046, abs=0.002)
    assert "0.046/day, 13%" in ra.WHAT_THE_STACK_MEANS["the_numbers"]


def test_the_stack_does_not_claim_to_remove_the_need_for_a_killing_agent():
    d = ra.WHAT_THE_STACK_MEANS
    assert "does not remove the need" in d["what_it_still_does_not_do"]
    assert "neither holds the floor" in d["what_it_still_does_not_do"]
    assert "no amount of stacking changes that" in d["what_it_still_does_not_do"]


def test_the_deciding_experiment_is_a_sequencing_question():
    t = ra.WHAT_THE_STACK_MEANS["the_single_experiment_that_decides_the_most"]
    assert "sequence" in t.lower()
    assert "Genetic loss" in t and "Epigenetic silencing" in t


# ---------------------------------------------------------------------------------------------
# The floor-holder question, and the final position.
# ---------------------------------------------------------------------------------------------

def test_the_floor_holder_argument_is_structural_not_enthusiastic():
    d = ra.ONLY_IMMUNITY_IS_PERMANENT
    assert "duration criterion" in d["the_structural_argument"]
    assert "week 22" in d["the_structural_argument"]
    assert "ANTIGEN-DIRECTED" in d["what_is_left"]


def test_the_nk_arm_is_antigen_independent_for_a_stated_reason():
    d = ra.ONLY_IMMUNITY_IS_PERMANENT
    t = d["the_one_immune_arm_that_does_not_need_the_antigen"]
    assert "STRESS markers, not lineage" in t
    assert "independent of the vaccine target and of MHC-I" in t


def test_the_canine_nk_evidence_is_scoped_to_the_wrong_tumour():
    d = ra.ONLY_IMMUNITY_IS_PERMANENT
    assert "29254507" in d["the_canine_evidence"]
    assert "osteosarcoma rather than" in d["why_that_evidence_is_the_right_species_and_the_wrong_tumour"]
    assert "resistant antigen-null" in d["why_that_evidence_is_the_right_species_and_the_wrong_tumour"]


def test_nk_is_explicitly_not_claimed_as_a_closure():
    d = ra.WHY_NK_STILL_DOES_NOT_CLOSE_IT
    assert "log-remover, not a" in d["the_first_problem_is_that_transferred_cells_are_a_pulse"]
    assert "soluble MIC" in d["the_second_problem_is_the_documented_escape"]
    assert "No number is derived from it here" in d["the_third_problem_is_that_no_rate_exists"]


def test_no_rate_is_derived_from_the_in_vitro_nk_cytotoxicity():
    """80% at 10:1 in a short assay must not become a per-day rate anywhere."""
    blob = repr(ra.ONLY_IMMUNITY_IS_PERMANENT) + repr(ra.WHY_NK_STILL_DOES_NOT_CLOSE_IT)
    assert "/day" not in blob
    assert "category error" in ra.WHY_NK_STILL_DOES_NOT_CLOSE_IT[
        "the_third_problem_is_that_no_rate_exists"]


def test_the_final_position_separates_log_removers_from_floor_holders():
    d = ra.WHAT_LOOKING_DEEPER_ACTUALLY_FOUND
    t = d["the_two_kinds_of_answer"]
    assert "LOG-REMOVERS" in t and "FLOOR-HOLDERS" in t
    for name in ("eBAT", "plasticity", "bystander"):
        assert name in t


def test_the_supply_trap_is_named_and_covers_both_ideas():
    t = ra.WHAT_LOOKING_DEEPER_ACTUALLY_FOUND["the_trap_that_caught_two_good_ideas"]
    assert "competitive release" in t and "bystander" in t
    assert "supply is the thing you are eliminating" in t


def test_the_final_status_is_not_upgraded():
    d = ra.WHAT_LOOKING_DEEPER_ACTUALLY_FOUND
    assert "CLOSED CONDITIONAL ON A NAMED EXPERIMENT" in d["the_status_i_will_not_upgrade"]
    assert "it is not closed" in d["the_status_i_will_not_upgrade"]
    assert "exists in canine hemangiosarcoma at all" in d["the_status_i_will_not_upgrade"]


def test_the_closure_condition_is_stated_as_a_checkable_sentence():
    t = ra.WHAT_LOOKING_DEEPER_ACTUALLY_FOUND["what_would_make_me_call_it_closed"]
    for element in ("per-day kill rate", "canine hemangiosarcoma", "antigen-null",
                    "holding rate", "sustainable"):
        assert element in t
    assert "currently missing" in t


def test_the_headline_does_not_claim_a_fourth_mechanism_was_found():
    h = ra.WHAT_LOOKING_DEEPER_ACTUALLY_FOUND["the_honest_headline"]
    assert h.startswith("no single mechanism closes")
    assert "better than a fourth candidate" in h


# ---------------------------------------------------------------------------------------------
# The plasticity simulation, which inverted the idea it was built to test.
# ---------------------------------------------------------------------------------------------

def test_one_way_plasticity_rescues_only_partially_and_saturates():
    t = ra.PLASTICITY_RESCUE
    assert t[0.034]["one_way"] == 0.0, "at the holding rate net growth is zero, not negative"
    assert t[0.050]["one_way"] > 0.2, "past the holding rate it should rescue"
    # Doubling the reversion rate again does not help: same within Monte Carlo noise.
    assert abs(t[0.080]["one_way"] - t[0.050]["one_way"]) < 0.10
    # And it never approaches the ~0.84 available with no blind spot at all.
    assert t[0.050]["one_way"] < 0.5


def test_back_conversion_destroys_the_rescue():
    """The finding that inverts the idea: reversibility is symmetric and the refill wins."""
    t = ra.PLASTICITY_RESCUE
    assert t[0.050]["one_way"] > 0.2 and t[0.050]["q_in_0.005"] == 0.0
    for q_out, row in t.items():
        if row["q_in_0.02"] is not None:
            assert row["q_in_0.02"] == 0.0, f"q_out={q_out} should fail entirely at q_in=0.02"


def test_the_rescue_is_monotone_in_back_conversion():
    for q_out, row in ra.PLASTICITY_RESCUE.items():
        if row["q_in_0.005"] is None:
            continue
        assert row["one_way"] >= row["q_in_0.005"] >= row["q_in_0.02"], q_out


def test_the_eigenvalue_sign_predicts_every_simulated_cell():
    """Positive dominant eigenvalue must correspond to total failure."""
    for q_out, row in ra.PLASTICITY_RESCUE.items():
        for key, q_in in (("one_way", 0.0), ("q_in_0.005", 0.005), ("q_in_0.02", 0.02)):
            val = row[key]
            if val is None:
                continue
            lam = ra.two_compartment_growth_rate(q_out, q_in)
            if lam > 0:
                assert val == 0.0, f"q_out={q_out} q_in={q_in} lambda={lam:+.4f} but sim={val}"


def test_the_eigenvalue_saturates_at_the_visible_clones_own_decline():
    """Why faster reversion stops helping: the drain is no longer rate-limiting."""
    fast = ra.two_compartment_growth_rate(0.05, 0.0)
    faster = ra.two_compartment_growth_rate(0.50, 0.0)
    assert fast == pytest.approx(faster, abs=1e-6)
    assert fast == pytest.approx(ra.BLIND_SPOT_NET_GROWTH_PER_DAY - 0.042, abs=1e-6)


def test_the_eigenvalue_rises_with_back_conversion():
    seq = [ra.two_compartment_growth_rate(0.05, q) for q in (0.0, 0.005, 0.02, 0.05)]
    assert seq == sorted(seq)


def test_no_plasticity_reproduces_the_bare_holding_rate():
    assert ra.two_compartment_growth_rate(0.0, 0.0) == pytest.approx(
        ra.BLIND_SPOT_NET_GROWTH_PER_DAY)


def test_the_inversion_is_stated_as_against_my_own_expectation():
    d = ra.THE_TWO_WAY_RESULT_INVERTS_THE_IDEA
    assert "LIABILITY" in d["so_plasticity_is_not_a_free_gift"]
    assert "expecting plasticity to be the cheap" in d["so_plasticity_is_not_a_free_gift"]
    assert "MANUFACTURES" in d["why_that_happens"]


def test_the_superseded_estimate_is_owned_with_its_number():
    d = ra.THE_TWO_WAY_RESULT_INVERTS_THE_IDEA
    t = d["the_estimate_this_corrects"]
    assert "79.5%" in t
    assert "my own time-averaging argument" in t
    assert "wrong side" in t


def test_the_saturation_explanation_names_the_limiting_step():
    d = ra.THE_TWO_WAY_RESULT_INVERTS_THE_IDEA
    assert "-0.0086/day" in d["but_it_saturates_immediately"]
    assert "ANTIGEN-POSITIVE resistant clone" in d["but_it_saturates_immediately"]


# ---------------------------------------------------------------------------------------------
# The pincer. These tests exist because this is the strongest result in the module, which makes it
# the one most likely to be overstated later.
# ---------------------------------------------------------------------------------------------

def test_the_pincer_reaches_the_no_blind_spot_baseline():
    t = ra.PINCER_RESCUE
    assert t[0.060]["no_escape"] == pytest.approx(ra.NO_BLIND_SPOT_BASELINE, abs=0.05)


def test_the_pincer_saturates_rather_than_climbing_past_the_baseline():
    """A closure removes the problem; it does not overshoot. Overshoot would mean something else."""
    t = ra.PINCER_RESCUE
    assert t[0.090]["no_escape"] <= t[0.060]["no_escape"] + 0.05
    assert t[0.090]["no_escape"] <= ra.NO_BLIND_SPOT_BASELINE + 0.05


def test_the_pincer_threshold_sits_on_the_independently_derived_floor():
    t = ra.PINCER_RESCUE
    # At or below the holding rate, nothing happens.
    assert t[0.020]["no_escape"] == 0.0
    assert t[0.034]["no_escape"] == 0.0
    assert 0.034 >= ra.BLIND_SPOT_NET_GROWTH_PER_DAY
    # Just above it, the rescue begins.
    assert t[0.042]["no_escape"] > 0.2


def test_the_pincer_is_monotone_in_nk_rate_up_to_saturation():
    rates = sorted(ra.PINCER_RESCUE)
    vals = [ra.PINCER_RESCUE[r]["no_escape"] for r in rates]
    assert vals == sorted(vals[:-1]) + [vals[-1]]
    assert vals[0] == 0.0


def test_the_pincer_ask_is_the_smallest_in_the_analysis():
    """16.5% three-day kill against 24% standalone and 13% for the best finite stack."""
    pincer = 1 - pe.viability_after(0.060)
    assert pincer == pytest.approx(0.165, abs=0.005)
    standalone = 1 - pe.viability_after(pe.required_rate_for_course(335))
    assert pincer < standalone
    # And it must still be above the irreducible floor.
    assert pincer > 1 - pe.viability_after(ra.BLIND_SPOT_NET_GROWTH_PER_DAY)


def test_why_the_permanent_holder_is_cheaper_is_stated():
    d = ra.THE_PINCER_CLOSES_IT
    assert "never stops" in d["why_it_is_cheaper_than_everything_else"]
    assert "no ln(N0)/days work term" in d["why_it_is_cheaper_than_everything_else"]


def test_the_complementarity_is_structural_not_additive():
    d = ra.MISSING_SELF_IS_THE_COMPLEMENT_OF_THE_VACCINE
    assert "PAVES WAY" in d["the_statement"]
    assert "not two agents stacked" in d["why_it_matters_here"]
    assert "does not provide an escape from both" in d["the_logical_pincer"]


def test_the_hla_e_hole_is_measured_and_its_harmlessness_is_explained():
    d = ra.THE_HLA_E_HOLE_AND_WHAT_IT_ACTUALLY_COSTS
    t = ra.PINCER_RESCUE
    # Measured: the hole barely moves the result.
    assert abs(t[0.060]["hla_e_20pct"] - t[0.060]["no_escape"]) < 0.05
    # Explained: because those cells remain drug-sensitive.
    assert "DRUG-SENSITIVE" in d["why_not_and_this_is_the_important_part"]


def test_the_dangerous_triple_overlap_is_named_and_not_claimed_covered():
    d = ra.THE_HLA_E_HOLE_AND_WHAT_IT_ACTUALLY_COSTS
    t = d["the_case_that_would_be_dangerous"]
    assert "AND drug-resistant" in t
    assert "returns 0.000" in t
    assert "OVERLAP_IS_THE_WHOLE_BALLGAME" in d["the_pattern_this_repeats"]


def test_the_platelet_link_is_flagged_as_matching_this_disease():
    d = ra.THE_HLA_E_HOLE_AND_WHAT_IT_ACTUALLY_COSTS
    t = d["why_that_paper_is_uncomfortably_well_matched_to_this_disease"]
    assert "PLATELET" in t
    assert "intravascular coagulation" in t


def test_the_strongest_objection_is_recorded_and_is_the_authors_own():
    d = ra.WHY_THIS_IS_STILL_NOT_A_CLOSURE_I_WILL_CLAIM
    t = d["endogenous_nk_is_already_present_and_the_tumour_grew_anyway"]
    assert "mine rather than a paper's" in t
    assert "AUGMENTED, not merely present" in t
    assert "reintroduces an intervention" in t


def test_the_pincer_is_not_claimed_as_demonstrated():
    d = ra.WHY_THIS_IS_STILL_NOT_A_CLOSURE_I_WILL_CLAIM
    assert "requirement, not an observation" in d["no_rate_has_been_measured"]
    assert "not a demonstrated closure" in d["the_honest_status"]
    assert "DLA-E" in d["dla_e_is_unknown"]


def test_the_status_change_is_stated_as_a_change_of_kind_not_of_certainty():
    t = ra.WHY_THIS_IS_STILL_NOT_A_CLOSURE_I_WILL_CLAIM["the_honest_status"]
    assert "needs a drug nobody has" in t
    assert "immune arm everyone has" in t


def test_the_pincer_threshold_is_exact_at_every_seed():
    """No partial values at the holding rate: a real threshold, not a noisy one."""
    assert ra.PINCER_REPRODUCIBILITY[0.034] == (0.0, 0.0, 0.0)


def test_the_pincer_closure_reproduces_at_the_baseline():
    vals = ra.PINCER_REPRODUCIBILITY[0.060]
    assert len(vals) == 3
    for v in vals:
        assert abs(v - ra.NO_BLIND_SPOT_BASELINE) < 0.08, v
    # And the seed-7 value recorded here must match the main table.
    assert vals[0] == ra.PINCER_RESCUE[0.060]["no_escape"]


def test_the_partial_rescue_reproduces_too():
    vals = ra.PINCER_REPRODUCIBILITY[0.042]
    assert max(vals) - min(vals) < 0.06
    assert vals[0] == ra.PINCER_RESCUE[0.042]["no_escape"]


def test_the_reseed_is_not_claimed_to_validate_the_biology():
    d = ra.WHY_THE_RESEED_MATTERS
    assert "tests the simulation, not the biology" in d["what_it_does_not_establish"]
    assert "A stable wrong answer is still wrong" in d["what_it_does_not_establish"]


# ---------------------------------------------------------------------------------------------
# The prior-art check on the pincer itself. These matter most: the pincer was the cleanest result
# in the module until this trial was found, which is exactly when a claim is easiest to overstate.
# ---------------------------------------------------------------------------------------------

def test_the_canine_nk_augmentation_trial_is_recorded_as_a_failure():
    d = ra.AUGMENTING_NK_WAS_TRIED_IN_DOGS_AND_MADE_THINGS_WORSE
    assert "HALTED FOR FUTILITY" in d["the_result"]
    assert "INFERIOR" in d["the_result"]
    assert "WORSE OUTCOMES" in d["the_authors_conclusion"]


def test_the_trial_is_matched_to_the_pincers_own_setting_and_strategy():
    d = ra.AUGMENTING_NK_WAS_TRIED_IN_DOGS_AND_MADE_THINGS_WORSE
    t = d["why_this_is_the_right_trial_to_check"]
    assert "minimal residual disease after surgery" in t
    assert "raise NK activity" in t
    assert "strongest negative" in d["how_this_lands_on_the_pincer"]


def test_the_trials_scope_limit_is_also_recorded():
    d = ra.AUGMENTING_NK_WAS_TRIED_IN_DOGS_AND_MADE_THINGS_WORSE
    t = d["what_it_does_not_show"]
    assert "osteosarcoma rather than hemangiosarcoma" in t
    assert "ONE way of trying" in t


def test_the_failure_mechanism_is_quantified():
    d = ra.WHY_IT_FAILED_IS_MEASURED_AND_IT_MATTERS
    assert "-18.2" in d["the_setting_suppresses_the_very_arm_the_pincer_needs"]
    assert "TIGIT" in d["the_second_mechanism_is_exhaustion"]


def test_the_model_limitation_the_trial_exposes_is_admitted():
    d = ra.WHY_IT_FAILED_IS_MEASURED_AND_IT_MATTERS
    t = d["why_that_is_a_problem_the_model_does_not_capture"]
    assert "constant NK kill" in t
    assert "weakest exactly when it is most needed" in t


def test_the_supporting_signal_inside_the_failure_is_kept():
    """The premise is supported even though the execution failed; both must be recorded."""
    d = ra.WHY_IT_FAILED_IS_MEASURED_AND_IT_MATTERS
    assert "r = 0.62" in d["the_signal_inside_the_failure"]
    assert "IMPROVED dog survival" in d["the_signal_inside_the_failure"]
    assert "separates the premise from the execution" in d["why_that_line_is_the_most_important_one_here"]


def test_the_reading_is_neither_refutation_nor_rescue():
    t = ra.WHY_IT_FAILED_IS_MEASURED_AND_IT_MATTERS["the_honest_reading"]
    assert "neither a refutation" in t and "nor a rescue" in t


def test_the_corrected_version_names_agents_and_the_timing_problem():
    d = ra.WHAT_THE_CORRECTED_VERSION_WOULD_HAVE_TO_BE
    assert "TIGIT blockade" in d["release_the_brake_rather_than_only_pressing_the_accelerator"]
    assert "Monalizumab" in d["and_the_hole_in_the_pincer_has_its_own_agent"]
    assert "worst possible schedule" in d["the_timing_implication_the_trial_forces"]
    untested = d["what_has_never_been_tested"]
    assert "in any dog" in untested
    assert "nobody has shown exists in this disease" in untested


def test_the_post_trial_verdict_separates_structure_from_deliverability():
    d = ra.THE_PINCER_VERDICT_AFTER_THE_TRIAL
    assert "the structure" in d["what_survives"]
    assert "halted for futility" in d["what_does_not"]
    assert "CLOSED CONDITIONAL ON A NAMED EXPERIMENT" in d["the_status"]


def test_the_verdict_does_not_call_the_pincer_a_closure():
    d = ra.THE_PINCER_VERDICT_AFTER_THE_TRIAL
    t = d["the_sentence_i_would_stand_behind"]
    assert "no demonstrated way to deliver it" in t
    assert "it is not a closure" in t


def test_the_reason_for_doing_the_prior_art_check_is_recorded():
    t = ra.THE_PINCER_VERDICT_AFTER_THE_TRIAL["why_finding_this_was_worth_more_than_not_finding_it"]
    assert "no prior-art search" in t
    assert "one rank stronger than the evidence" in t


def test_the_earlier_pincer_optimism_is_not_left_unqualified():
    """THE_PINCER_CLOSES_IT must not be the module's last word on the pincer."""
    names = [n for n in dir(ra) if "PINCER" in n]
    assert "THE_PINCER_VERDICT_AFTER_THE_TRIAL" in names
    assert "AUGMENTING_NK_WAS_TRIED_IN_DOGS_AND_MADE_THINGS_WORSE" in dir(ra)


# ---------------------------------------------------------------------------------------------
# The correlation error, and the empirical verdict on floor-holding in this disease.
# ---------------------------------------------------------------------------------------------

def test_double_negative_cells_matches_hand_arithmetic():
    # 0.3 burden * 5% null * 8.56e-6 resistant * 1e10 cells = ~1284 cells.
    assert ra.double_negative_cells() == pytest.approx(1284, abs=5)


def test_double_negative_cells_scales_with_both_factors():
    base = ra.double_negative_cells()
    assert ra.double_negative_cells(resistant_fraction=8.56e-5) == pytest.approx(base * 10)
    assert ra.double_negative_cells(coverage=0.90) == pytest.approx(base * 2)


def test_double_negative_cells_rejects_impossible_coverage():
    with pytest.raises(ValueError):
        ra.double_negative_cells(coverage=1.0)
    with pytest.raises(ValueError):
        ra.double_negative_cells(coverage=-0.1)


def test_the_inflation_is_about_five_orders_of_magnitude():
    d = ra.THE_CORRELATION_ASSUMPTION_WAS_MINE_AND_IT_WAS_WRONG
    assert d["the_inflation"] > 1e4
    assert d["in_logs"] == pytest.approx(11.7, abs=0.2)
    # And it must be computed from the two sizes, not asserted.
    assert d["the_inflation"] == pytest.approx(1.5e8 / 1284.0, rel=1e-6)


def test_the_corrected_work_term_is_much_smaller_but_the_floor_is_not():
    corrected = ra.required_rate_decomposed(ra.BLIND_SPOT_NET_GROWTH_PER_DAY,
                                            ra.double_negative_cells())
    as_modelled = ra.required_rate_decomposed(ra.BLIND_SPOT_NET_GROWTH_PER_DAY,
                                              pe.blind_spot_initial_cells())
    assert corrected < as_modelled
    assert corrected == pytest.approx(0.055, abs=0.002)
    # The floor is untouched: both remain above it, and neither can go below.
    assert corrected > ra.BLIND_SPOT_NET_GROWTH_PER_DAY


def test_the_error_is_owned_as_mine_and_route_specific():
    d = ra.THE_CORRELATION_ASSUMPTION_WAS_MINE_AND_IT_WAS_WRONG
    assert "what_i_assumed" in d
    assert "ON DAY ZERO" in d["why_independence_is_the_right_default_for_ROUTE_8"]
    assert "applied route 4's assumption to route 8" in \
        d["why_independence_is_the_right_default_for_ROUTE_8"]
    assert "FIVE ORDERS OF MAGNITUDE short" in d["what_the_earlier_module_did_test"]


def test_correcting_the_error_is_not_claimed_to_close_route_8():
    d = ra.THE_CORRELATION_ASSUMPTION_WAS_MINE_AND_IT_WAS_WRONG
    t = d["what_this_does_not_change"]
    assert "the floor" in t
    assert "progresses just as surely" in t
    assert "does not by itself close route 8" in t


def test_the_measured_resistant_fraction_is_recorded_with_its_method():
    d = ra.MEASURED_PREEXISTING_RESISTANT_FRACTION
    assert d["median"] < d["mean"]
    assert "sample_initial_state" in d["how_it_was_obtained"]
    assert 0.0 < d["fraction_of_draws_with_any_resistant_cell"] < 1.0


def test_toceranib_maintenance_is_recorded_as_the_direct_floor_holder_test():
    d = ra.TOCERANIB_MAINTENANCE_WAS_TRIED_AND_FAILED
    assert "DOES NOT IMPROVE" in d["the_result"]
    assert "SPLENIC hemangiosarcoma" in d["the_trial"]
    assert "clears the duration criterion" in d["why_it_was_a_strong_floor_holder_candidate"]
    assert "closest thing to a direct test" in d["why_it_matters_most_of_all_the_negatives"]


def test_the_tally_covers_four_failures_and_one_success():
    d = ra.EVERY_MAINTENANCE_STRATEGY_IN_THIS_DISEASE_HAS_FAILED
    assert len(d["the_tally"]) == 4
    assert "SINGLE SHORT CYCLE" in d["the_one_thing_that_worked"]
    assert "Four negatives and one positive" in d["THE_PATTERN"]


def test_the_pattern_is_flagged_as_uncontrolled():
    d = ra.EVERY_MAINTENANCE_STRATEGY_IN_THIS_DISEASE_HAS_FAILED
    t = d["the_caution"]
    assert "not tests of route 8" in t
    assert "not a controlled comparison" in t


def test_the_empirical_verdict_is_linked_to_the_simulation_finding():
    d = ra.EVERY_MAINTENANCE_STRATEGY_IN_THIS_DISEASE_HAS_FAILED
    assert "agree on the shape of the answer" in d["and_it_matches_what_the_model_found_independently"]
    # The simulation claim it refers to must still exist.
    assert ra.PLASTICITY_RESCUE is not None


def test_the_correlation_sweep_is_uniformly_zero():
    """Five orders of magnitude of compartment size, all total failure."""
    for frac, row in ra.CORRELATION_SWEEP.items():
        for key in ("no_agent", "ebat_5_2", "ebat_7_2"):
            assert row[key] == 0.0, f"frac_res={frac} {key}"


def test_the_sweep_spans_five_orders_of_magnitude():
    cells = [row["cells"] for row in ra.CORRELATION_SWEEP.values()]
    assert max(cells) / min(cells) == pytest.approx(1e5, rel=0.01)
    # And the smallest is the independence estimate.
    assert min(cells) == pytest.approx(ra.double_negative_cells(), rel=0.2)


def test_rarity_is_explicitly_not_treated_as_a_defence():
    d = ra.RARITY_IS_NOT_A_DEFENCE
    assert "Rarity is not a defence. Only absence is." in d["the_sharpest_statement_of_route_8"]
    assert "binary in EXISTENCE, not graded in SIZE" in d["WHAT_THIS_CORRECTS_IN_MY_OWN_ACCOUNT"]


def test_the_self_correction_does_not_let_the_correlation_fix_off_the_hook():
    """The work-term saving is real; the danger reduction is not. Both must be stated."""
    d = ra.RARITY_IS_NOT_A_DEFENCE
    t = d["WHAT_THIS_CORRECTS_IN_MY_OWN_ACCOUNT"]
    assert "0.090 to 0.055/day" in t
    assert "did not create the danger and correcting it does not reduce it" in t


def test_the_ebat_knife_edge_is_stated_quantitatively():
    d = ra.RARITY_IS_NOT_A_DEFENCE
    t = d["why_eBAT_does_not_rescue_even_the_smallest"]
    assert "1.1" in t
    assert "same size is not the same as being enough" in t
    # Check the arithmetic it asserts.
    import math
    assert 1500 * math.exp(-7.2) == pytest.approx(1.1, abs=0.15)


def test_the_concern_is_scoped_to_existence_not_frequency():
    d = ra.RARITY_IS_NOT_A_DEFENCE
    assert "yes/no question" in d["what_that_means_for_whether_this_scenario_is_real"]
    assert "never been observed" in d["the_honest_scope_of_the_concern"]


# ---------------------------------------------------------------------------------------------
# The second omission and the closure it exposed.
# ---------------------------------------------------------------------------------------------

def test_the_engine_really_has_no_third_agent():
    """The omission this section is about must be verifiable, not asserted."""
    from canine_dsp import hsa_scenarios as hs
    m5, _, _, _ = hs.hsa_vaccine_followon_scenarios(vaccine_max_kill_values=[0.03])[0.03]
    assert not hasattr(m5, "ic50_nM_3")
    assert not hasattr(m5, "max_kill_3")


def test_the_omission_is_named_as_an_unjustified_assumption():
    d = ra.DOXORUBICIN_WAS_NEVER_IN_THE_MODEL
    t = d["the_assumption_this_exposes"]
    assert "no dog actually receives" in t
    assert "complete cross-resistance" in t
    assert "not conservatism" in t


def test_both_route_8_errors_are_characterised_the_same_way():
    d = ra.DOXORUBICIN_WAS_NEVER_IN_THE_MODEL
    t = d["the_pattern_with_the_first_error"]
    assert "CONSTRUCTED" in t and "OMITTED" in t
    assert "Parameter audits do not catch either" in t


def test_doxorubicin_logs_match_the_recorded_medians():
    d = ra.DOXORUBICIN_EFFECT_IN_LOGS
    g = ra.BLIND_SPOT_NET_GROWTH_PER_DAY
    assert d["logs_typical"] == pytest.approx((180 - 86) * g)
    assert d["logs_timely"] == pytest.approx((238 - 86) * g)
    assert d["logs_delayed"] < d["logs_typical"] < d["logs_timely"]
    assert d["logs_typical"] == pytest.approx(3.1, abs=0.1)


def test_the_doxorubicin_conversion_carries_the_same_caveat_as_ebat():
    d = ra.DOXORUBICIN_EFFECT_IN_LOGS
    t = d["the_conversion_caveat"]
    assert "WHOLE tumour" in t
    assert "not a measurement of what it does to this compartment" in t


def test_neither_agent_alone_closes_it():
    t = ra.CLOSURE_BY_WHAT_THEY_ALREADY_GET
    assert t[3.1] == 0.0, "doxorubicin alone must not close it"
    assert t[5.1] == 0.0, "doxorubicin at its best alone must not close it"
    assert t[7.2] == 0.0, "eBAT alone must not close it"


def test_the_combination_closes_it_at_the_pessimistic_end():
    t = ra.CLOSURE_BY_WHAT_THEY_ALREADY_GET
    assert t[8.3] == pytest.approx(ra.NO_BLIND_SPOT_BASELINE, abs=0.05)
    # And it saturates rather than climbing past the baseline.
    assert t[12.9] == pytest.approx(t[8.3])


def test_the_threshold_brackets_the_closed_form_requirement():
    need = math.log(ra.double_negative_cells())
    t = ra.CLOSURE_BY_WHAT_THEY_ALREADY_GET
    failed = [k for k, v in t.items() if v == 0.0]
    passed = [k for k, v in t.items() if v > 0.5]
    assert max(failed) >= need - 0.2
    assert min(passed) > need
    assert need == pytest.approx(7.16, abs=0.05)


def test_the_pessimistic_sum_is_actually_the_pessimistic_sum():
    """8.3 must be doxorubicin's weakest plus eBAT's weakest, not a favourable pick."""
    dox_worst = ra.DOXORUBICIN_EFFECT_IN_LOGS["logs_typical"]
    ebat_worst = min(ra.EBAT_EFFECT_IN_LOGS.values())
    assert dox_worst + ebat_worst == pytest.approx(8.3, abs=0.2)


def test_the_closure_requires_no_new_agent():
    d = ra.THIS_IS_THE_CLOSURE_AND_IT_NEEDS_NO_NEW_DRUG
    assert "no new agent" in d["why_this_is_different_from_every_other_candidate"]
    assert "standard of care" in d["why_this_is_different_from_every_other_candidate"]
    assert "does not depend on optimistic readings" in d["and_it_clears_at_the_pessimistic_end"]


def test_the_load_bearing_caveat_is_anthracycline_resistance():
    c = ra.THIS_IS_THE_CLOSURE_AND_IT_NEEDS_NO_NEW_DRUG["THE_CAVEATS_THAT_STILL_STAND"]
    t = c["the_compartment_may_also_resist_doxorubicin"]
    assert "load-bearing" in t
    assert "TRIPLE negative" in t
    assert "clinically chemoresistant" in t


def test_the_closure_is_scoped_to_the_model_and_to_an_unverified_compartment():
    d = ra.THIS_IS_THE_CLOSURE_AND_IT_NEEDS_NO_NEW_DRUG
    assert "CLOSED IN THE MODEL" in d["the_honest_status"]
    c = d["THE_CAVEATS_THAT_STILL_STAND"]
    assert "never been observed" in c["and_the_compartment_itself_is_unverified"]
    assert len(c) == 4
