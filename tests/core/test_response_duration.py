"""Rates converted to time, and the resistance check that decides whether the time means anything."""

from __future__ import annotations

import math

import pytest

from canine_dsp.core import microtubule_route as mt
from canine_dsp.core import response_duration as rd
from canine_dsp.core.catalogue import LEPTOMENINGEAL, PARENCHYMA
from canine_dsp.core.dormancy import CYCLING_FRACTION_SWEEP

BOTH = (PARENCHYMA, LEPTOMENINGEAL)


# --- the conversion --------------------------------------------------------------------------------------

def test_a_positive_margin_gives_a_finite_clearance_time():
    assert rd.days_to_clear(0.0416) == pytest.approx(498, abs=1)
    assert rd.days_to_clear(0.0592) == pytest.approx(350, abs=1)


def test_a_zero_or_negative_margin_never_clears():
    assert rd.days_to_clear(0.0) == float("inf")
    assert rd.days_to_clear(-0.01) == float("inf")


def test_the_duration_table_is_re_derived_from_the_live_margins():
    table = rd.duration_table()
    for compartment, label in ((PARENCHYMA, "brain tissue"), (LEPTOMENINGEAL, "linings")):
        margin, days, _ = table[compartment]
        exp_margin, exp_days, exp_months, _ = rd.DURATION[label]
        assert margin == pytest.approx(exp_margin, abs=5e-4)
        assert days == pytest.approx(exp_days, abs=2)
        assert days / 30.4 == pytest.approx(exp_months, abs=0.2)


def test_undetectable_comes_well_before_cleared():
    """Imaging goes quiet at ~1e8 cells -- about a tenth of the way to the last cell.

    This assertion caught a transcription slip: DURATION recorded the GAP between the two times
    (443 days) in the slot meant for the time to become undetectable (55 days).
    """
    for compartment, label in ((PARENCHYMA, "brain tissue"), (LEPTOMENINGEAL, "linings")):
        margin, cleared, undetectable = rd.duration_table()[compartment]
        assert undetectable < cleared
        assert undetectable == pytest.approx(math.log(10) / margin, abs=1)
        assert undetectable == pytest.approx(rd.DURATION[label][3], abs=1)


def test_duration_is_inversely_proportional_to_margin():
    """Halve the margin, double the months. A modest rate error is a large time error."""
    for margin, days in rd.DURATION_BY_MARGIN.items():
        assert rd.days_to_clear(margin) == pytest.approx(days, abs=2)
    assert rd.days_to_clear(0.0200) == pytest.approx(2 * rd.days_to_clear(0.0400), abs=2)


def test_a_bigger_tumour_costs_surprisingly_little_time():
    """Exponential decay: ten times the burden is one extra doubling-worth of days, not ten."""
    small = rd.days_to_clear(0.0416, 1e9)
    big = rd.days_to_clear(0.0416, 1e10)
    assert big - small == pytest.approx(math.log(10) / 0.0416, abs=1)
    assert big < small * 1.2


# --- resistance: what actually bounds durability -------------------------------------------------------------

@pytest.mark.parametrize("compartment", BOTH)
def test_no_double_escape_combination_is_uncovered(compartment):
    assert rd.uncovered_combinations(compartment, order=2) == []


@pytest.mark.parametrize("compartment", BOTH)
def test_no_triple_escape_combination_is_uncovered(compartment):
    assert rd.uncovered_combinations(compartment, order=3) == []


@pytest.mark.parametrize("cycling", CYCLING_FRACTION_SWEEP)
def test_coverage_holds_across_the_whole_cycling_fraction_sweep(cycling):
    """The persister term depends on this, and it is unmeasured, so it must hold everywhere."""
    assert rd.uncovered_combinations(PARENCHYMA, order=2, cycling_fraction=cycling) == []


def test_resistance_is_covered_end_to_end():
    assert all(rd.resistance_is_covered(c) for c in BOTH)


def test_the_combination_counts_are_what_the_module_records():
    import itertools
    from canine_dsp.core.catalogue import ESCAPES
    assert len(list(itertools.combinations(ESCAPES, 2))) == rd.COMBINATION_COVERAGE["doubles_total"]
    assert len(list(itertools.combinations(ESCAPES, 3))) == rd.COMBINATION_COVERAGE["triples_total"]
    assert rd.COMBINATION_COVERAGE["doubles_uncovered"] == 0
    assert rd.COMBINATION_COVERAGE["triples_uncovered"] == 0


# --- the pessimistic bug, kept on the record -------------------------------------------------------------------

def test_the_naive_reaches_rule_reports_spurious_persister_holes():
    """Reproduces the wrong answer, so the correction cannot be quietly undone."""
    import itertools
    from canine_dsp.core.catalogue import ESCAPES, GROWTH_PER_DAY
    r = mt.build(PARENCHYMA)
    naive = [c for c in itertools.combinations(ESCAPES, 2)
             if sum(a.effective_kill for a in r.agents
                    if a.reaches(c[0]) and a.reaches(c[1])) - GROWTH_PER_DAY <= 0]
    assert len(naive) == 9
    assert all(any("persister" in e.name for e in c) for c in naive), \
        "every spurious hole was a persister pairing -- that pattern is what exposed the bug"
    assert rd.uncovered_combinations(PARENCHYMA, order=2) == []


def test_the_pessimistic_error_is_recorded():
    c = rd.THE_CHECK_THAT_RAN_PESSIMISTIC
    assert "9 of 45" in c["what_it_reported"]
    assert "`Agent.reaches`" in c["the_bug"]
    assert "PESSIMISTIC" in c["why_it_is_recorded"]


# --- the honest framing ------------------------------------------------------------------------------------------

def test_the_model_predicts_cure_and_says_to_distrust_it():
    joined = " ".join(rd.WHAT_DURABLE_MEANS_HERE)
    assert "CURE" in joined
    assert "DISTRUSTED" in joined
    assert "44 DAYS" in joined


def test_the_prediction_is_stated_against_the_measured_benchmark():
    """498 days is more than eleven times the 44-day benchmark. That ratio must be visible."""
    _, days, _, _ = rd.DURATION["brain tissue"]
    assert days / 44 > 11


def test_the_real_limit_is_named_as_the_growth_rate_not_resistance():
    joined = " ".join(rd.WHAT_DECIDES_THE_REAL_DURATION)
    assert "NOT the resistance arithmetic" in joined
    assert "GROWTH RATE" in joined
    assert "INFINITE" in joined


def test_the_growth_rate_boundary_really_does_flip_the_duration():
    """Between a ten-day and a seven-day doubling the margin crosses zero."""
    assert mt.closes(0.693 / 10)
    assert not mt.closes(0.693 / 7)
    assert rd.days_to_clear(mt.worst_margin(PARENCHYMA, 0.693 / 7)) == float("inf")


def test_obtainability_is_named_as_a_limit_on_duration_too():
    joined = " ".join(rd.WHAT_DECIDES_THE_REAL_DURATION)
    assert "DISCONTINUED" in joined
    assert "never been in a dog" in joined
