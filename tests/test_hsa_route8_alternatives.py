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
