"""Tests for the finite-course result.

This module contradicts the frozen findings, which makes it the one most likely to be quietly
softened later. The tests pin the contradiction, the robustness claim that justifies taking it
seriously, and the two caveats that stop it being over-read -- the deterministic-threshold artifact
and the coincidental resemblance to Skorupski's 0.375.
"""

from canine_dsp.validation.finite_course_durability import (
    PRACTICAL_DOSING_DURATION_DAYS,
    TEN_YEAR_RELAPSE_FREE_BY_DOSING_DURATION,
    WITHOUT_THE_EXTINCTION_STATE,
    verdict,
)


def test_three_years_captures_almost_all_of_indefinite_dosing():
    rows = TEN_YEAR_RELAPSE_FREE_BY_DOSING_DURATION
    three_year = rows[PRACTICAL_DOSING_DURATION_DAYS]["one_cell_1e9"]
    indefinite = rows[None]["one_cell_1e9"]
    assert three_year >= 0.99
    assert indefinite - three_year <= 0.01


def test_short_courses_genuinely_fail():
    """If everything worked the result would be suspicious rather than useful."""
    for days in (90, 180, 365):
        assert TEN_YEAR_RELAPSE_FREE_BY_DOSING_DURATION[days]["one_cell_1e9"] == 0.0


def test_durability_is_monotone_in_dosing_duration():
    rows = {k: v for k, v in TEN_YEAR_RELAPSE_FREE_BY_DOSING_DURATION.items() if k is not None}
    series = [rows[d]["one_cell_1e9"] for d in sorted(rows)]
    assert series == sorted(series)


def test_the_result_does_not_depend_on_the_carrying_capacity_anchor():
    """The free parameter that had to be moved to make the lomustine fit land. Here it is inert,
    which is why this result deserves more weight than that one."""
    for row in TEN_YEAR_RELAPSE_FREE_BY_DOSING_DURATION.values():
        assert row["one_cell_1e9"] == row["one_cell_1e12"]


def test_the_extinction_state_is_what_makes_the_answer_visible():
    """0.003 vs 0.380 at two years. Without this comparison the finding reads as a modelling
    choice rather than a correction."""
    assert WITHOUT_THE_EXTINCTION_STATE[730] < 0.01
    assert TEN_YEAR_RELAPSE_FREE_BY_DOSING_DURATION[730]["one_cell_1e9"] > 0.3


def test_the_contradiction_with_the_frozen_findings_is_stated_explicitly():
    text = verdict()["what_it_contradicts"]
    assert "never stoppable" in text
    assert "0.060/day" in text
    assert "measuring the wrong thing" in text


def test_the_knock_on_effect_on_the_endurance_work_is_named():
    text = verdict()["the_knock_on_effect"]
    assert "0.045/day" in text
    assert "persister argument for it is untouched" in text


def test_the_deterministic_threshold_artifact_is_disclosed():
    """The cliff shape is an implementation artifact. Saying so is what stops three years being
    quoted as a precise requirement."""
    direction = verdict()["the_direction_of_the_remaining_error"]
    assert "deterministic" in direction.lower()
    assert "shorter than three years" in direction
    assert "artifact" in verdict()["what_would_settle_it"]


def test_the_resemblance_to_the_observed_figure_is_refused():
    import canine_dsp.validation.finite_course_durability as m

    assert "not a second validation" in m.__doc__


def test_it_does_not_claim_more_than_a_model_output():
    import canine_dsp.validation.finite_course_durability as m

    assert "No dog has received" in m.__doc__
    assert "illustrative rather than fitted" in m.__doc__


# --- where the ten-year figure comes from ---

def test_the_ablation_attributes_the_whole_gap_to_continuous_dosing():
    from canine_dsp.validation.finite_course_durability import ABLATION_FROM_WHAT_WAS_TRIED as A

    assert A["0_chemo_finite_course"] == 0.0
    assert A["1_plus_remove_the_duration_cap"] == 1.0
    assert "entire gap" in A["THE_UNCOMFORTABLE_FINDING"]


def test_the_ablation_declares_its_own_confound():
    """Continuous dosing is the axis the engine handles wrongly, so the ablation cannot separate a
    real therapeutic advantage from the engine rewarding indefinite dosing."""
    from canine_dsp.validation.finite_course_durability import ABLATION_FROM_WHAT_WAS_TRIED as A

    text = A["why_that_is_a_problem_and_not_a_result"]
    assert "cannot distinguish" in text
    assert "saturated ceiling" in text


def test_potency_saturates_and_the_earlier_guess_is_retracted():
    from canine_dsp.validation.finite_course_durability import (
        POTENCY_DOES_NOT_SHORTEN_THE_COURSE as P,
    )

    # Emax is essentially saturated: identical at the durations that decide the answer, and within
    # Monte Carlo noise at 18 months. Asserting exact equality everywhere would overstate it.
    for day in (180, 365, 730, 1095):
        assert P[day][1] == P[day][2], day
    assert abs(P[547][1] - P[547][2]) < 0.03
    assert "WRONG" in P["BUT_IT_DOES_NOT_SHORTEN_THE_REQUIRED_COURSE"]


def test_potency_still_helps_at_two_years():
    """The finding is 'saturates', not 'irrelevant'. Both halves matter."""
    from canine_dsp.validation.finite_course_durability import (
        POTENCY_DOES_NOT_SHORTEN_THE_COURSE as P,
    )

    assert P[730][1] > 2 * P[730][0]


def test_the_binding_parameter_is_named_as_the_least_defensible_one():
    from canine_dsp.validation.finite_course_durability import (
        POTENCY_DOES_NOT_SHORTEN_THE_COURSE as P,
    )

    text = P["WHAT_ACTUALLY_BINDS"]
    assert "max_kill" in text
    assert "solving backwards from recorded margins" in text
