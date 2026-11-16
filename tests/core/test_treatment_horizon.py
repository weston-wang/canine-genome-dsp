"""The cure prediction required a treatment duration the drug does not permit."""

from __future__ import annotations

import math

import pytest

from canine_dsp.core import microtubule_route as mt
from canine_dsp.core import response_duration as rd
from canine_dsp.core import treatment_horizon as th
from canine_dsp.core.catalogue import LEPTOMENINGEAL, PARENCHYMA

BOTH = (PARENCHYMA, LEPTOMENINGEAL)


# --- it is not curative ------------------------------------------------------------------------------------

@pytest.mark.parametrize("compartment", BOTH)
def test_it_is_not_curative_inside_the_tolerable_window(compartment):
    assert not th.is_curative(compartment)


def test_the_window_is_a_small_fraction_of_what_cure_needs():
    o = th.outcome(PARENCHYMA)
    assert o["fraction_of_the_way_to_cure"] == pytest.approx(0.17, abs=0.02)
    assert th.TOLERABLE_WINDOW_DAYS == 84
    assert rd.days_to_clear(th.full_dose_margin()) == pytest.approx(498, abs=2)


def test_the_margin_cure_would_need_is_far_out_of_reach():
    needed = th.margin_required_for_cure()
    assert needed == pytest.approx(0.247, abs=0.005)
    assert needed / th.full_dose_margin() > 5.5
    from canine_dsp.core.catalogue import GROWTH_PER_DAY
    assert needed / GROWTH_PER_DAY > 4.0


def test_a_longer_window_would_still_not_be_curative():
    """Even doubling the tolerable window does not get there."""
    assert not th.is_curative(PARENCHYMA, window=168)
    assert not th.is_curative(PARENCHYMA, window=400)
    assert th.is_curative(PARENCHYMA, window=500)


# --- the predicted course is response then relapse -----------------------------------------------------------

def test_the_tumour_becomes_radiographically_undetectable_first():
    o = th.outcome(PARENCHYMA)
    assert o["radiographically_undetectable"]
    assert o["burden_at_window"] < rd.IMAGING_DETECTION_LIMIT
    assert o["burden_at_window"] == pytest.approx(3.0e7, rel=0.15)


def test_a_fifty_percent_dose_reduction_tips_the_margin_negative():
    assert th.margin_at_dose_fraction(0.75) > 0
    assert th.margin_at_dose_fraction(0.50) < 0
    assert th.margin_at_dose_fraction(0.50) == pytest.approx(-0.0064, abs=5e-4)


def test_the_dose_reduction_table_is_re_derived():
    for fraction, (margin, shrinks) in th.AFTER_DOSE_REDUCTION.items():
        got = th.margin_at_dose_fraction(fraction)
        assert got == pytest.approx(margin, abs=5e-4)
        assert (got > 0) is shrinks


def test_the_verdict_is_response_then_relapse():
    o = th.outcome(PARENCHYMA)
    assert o["relapses"]
    assert o["verdict"] == "RESPONSE THEN RELAPSE"
    assert o["doubling_time_on_relapse"] == pytest.approx(109, abs=5)


# --- the model previously could not express this --------------------------------------------------------------

def test_the_underlying_model_has_only_two_outcomes():
    """Cure or death. No relapse state, which is what real dogs actually do."""
    assert rd.days_to_clear(0.01) < float("inf")      # any positive margin -> cure
    assert rd.days_to_clear(-0.01) == float("inf")    # any negative margin -> unbounded growth
    joined = " ".join(th.THE_MODEL_HAD_NO_RELAPSE_STATE)
    assert "TRUE BY DEFAULT" in joined
    assert "SIGN OF A SUBTRACTION" in joined


def test_ten_year_durability_was_true_by_default_for_any_closing_regimen():
    """The question was never being answered -- it was implied by the sign."""
    for duty in (0.60, 0.80, 1.00):
        m = mt.worst_margin(PARENCHYMA, duty=duty)
        assert m > 0
        assert rd.days_to_clear(m) < 10 * 365, "every closing regimen 'cures' well inside ten years"


def test_the_model_now_reproduces_the_one_real_case():
    """Response inside ~3 months, relapse after dose reduction. The this breed: day 99 / day 124."""
    o = th.outcome(PARENCHYMA)
    assert o["radiographically_undetectable"]
    assert o["days_at_full_dose"] < 99
    assert o["relapses"]
    w = th.WHAT_THE_CLOCK_CHANGES
    assert "DAY 99" in w["the_real_case"] and "DAY 124" in w["the_real_case"]
    assert "WEAK EVIDENCE" in w["the_honest_weight"]


# --- the error class ------------------------------------------------------------------------------------------

def test_this_is_recorded_as_the_fifth_instance():
    assert len(th.THE_FIFTH_INSTANCE) == 5
    assert "TIME dimension" in th.THE_FIFTH_INSTANCE[-1]


def test_the_prior_fix_only_covered_the_instantaneous_case():
    """schedule_coherence checked access vs duty at an instant, not sustainability over time."""
    from canine_dsp.core import schedule_coherence as sc
    assert sc.is_coherent(sc.Route.ORAL_CONTINUOUS, 0.8, uses_disruption_gain=False)
    # coherent at an instant, and still not sustainable for the 498 days cure would need
    assert not th.is_curative(PARENCHYMA)


# --- what would actually be needed ----------------------------------------------------------------------------

def test_the_three_routes_to_cure_are_named():
    joined = " ".join(th.WHAT_WOULD_ACTUALLY_BE_CURATIVE)
    assert "LONGER WINDOW" in joined
    assert "SMALLER STARTING BURDEN" in joined
    assert "CONTROL RATHER THAN CURE" in joined


def test_surgery_is_rejected_as_a_burden_reduction_for_the_right_reason():
    joined = " ".join(th.WHAT_WOULD_ACTUALLY_BE_CURATIVE)
    assert "wrong place" in joined


def test_retreatment_on_relapse_is_flagged_as_unmodelled():
    """Neuropathy is reversible in 5-6 weeks, which permits re-treatment -- never modelled here."""
    joined = " ".join(th.WHAT_WOULD_ACTUALLY_BE_CURATIVE)
    assert "REVERSIBILITY" in joined
    assert "never modelled" in joined


def test_burden_decay_is_exponential_and_consistent():
    m = th.full_dose_margin()
    assert th.burden_after(0, m) == pytest.approx(th.STARTING_BURDEN)
    assert th.burden_after(rd.days_to_clear(m), m) == pytest.approx(1.0, rel=0.01)
    assert th.burden_after(100, m) == pytest.approx(
        th.STARTING_BURDEN * math.exp(-m * 100), rel=1e-9)
