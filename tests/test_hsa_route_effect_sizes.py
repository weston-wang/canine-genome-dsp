"""Tests for `hsa_route_effect_sizes`.

The module's job is to turn three citations into three numbers and then say how much of each has to
survive a cross-species transfer. These tests check the arithmetic, check that the derived values
are recomputed from the recorded trial figures rather than hard-coded, and check that the module
does not let a ratio read as evidence.
"""
import math

import pytest

from canine_dsp import hsa_route_effect_sizes as eff


# ---------------------------------------------------------------------------------------------
# The conversion helpers.

def test_burden_reduction_converts_to_a_rate():
    """Leaving 1/e of control burden after one day is exactly 1.0/day."""
    assert eff.rate_from_burden_reduction(1 / math.e, 1.0) == pytest.approx(1.0)
    # Halving the burden over ten days.
    assert eff.rate_from_burden_reduction(0.5, 10.0) == pytest.approx(math.log(2) / 10)


def test_burden_reduction_rejects_impossible_fractions():
    for bad in (0.0, 1.0, -0.1, 1.5):
        with pytest.raises(ValueError):
            eff.rate_from_burden_reduction(bad, 10.0)
    with pytest.raises(ValueError):
        eff.rate_from_burden_reduction(0.5, 0.0)


def test_a_bigger_reduction_over_the_same_interval_implies_a_bigger_rate():
    assert (eff.rate_from_burden_reduction(0.10, 14)
            > eff.rate_from_burden_reduction(0.36, 14))


def test_time_to_event_conversion_matches_its_stated_formula():
    got = eff.rate_from_time_to_event(54, 143, 20.0)
    assert got == pytest.approx(math.log(20.0) * (1 / 54 - 1 / 143))


def test_time_to_event_conversion_rejects_non_benefits():
    with pytest.raises(ValueError):
        eff.rate_from_time_to_event(143, 54, 20.0)   # treated shorter than control
    with pytest.raises(ValueError):
        eff.rate_from_time_to_event(54, 143, 1.0)    # no growth before the event
    with pytest.raises(ValueError):
        eff.rate_from_time_to_event(0, 143, 20.0)


def test_the_lethal_burden_assumption_is_carried_as_a_range_not_a_point():
    """Every time-to-event conversion is reported across the bracket, never at one value."""
    assert len(eff.LETHAL_BURDEN_MULTIPLES) >= 3
    for route in (eff.ROUTE_1_CHECKPOINT, eff.ROUTE_3_REDOSING):
        rates = route["implied_rate_per_day"]
        assert set(rates) == set(eff.LETHAL_BURDEN_MULTIPLES)
        assert min(rates.values()) < max(rates.values())


def test_transfer_required_is_the_ratio_it_claims_to_be():
    assert eff.transfer_required(eff.REQUIRED_INCREMENT) == pytest.approx(1.0)
    assert eff.transfer_required(2 * eff.REQUIRED_INCREMENT) == pytest.approx(0.5)
    with pytest.raises(ValueError):
        eff.transfer_required(0.0)


# ---------------------------------------------------------------------------------------------
# The derived values, recomputed from the recorded trial figures.

def test_the_target_matches_the_alternative_approach_module():
    from canine_dsp import hsa_alternative_approach as alt
    assert eff.MEASURED_VACCINE_HEIGHT == pytest.approx(alt.MEASURED_VACCINE_HEIGHT)
    assert eff.REQUIRED_HEIGHT == pytest.approx(
        alt.MINIMUM_REQUIREMENT["for_a_two_year_induction"]["height"])
    assert eff.REQUIRED_INCREMENT == pytest.approx(0.012)


def test_route_1_rates_are_recomputed_from_its_own_recorded_survival_figures():
    result = eff.ROUTE_1_CHECKPOINT["result"]
    for multiple, rate in eff.ROUTE_1_CHECKPOINT["implied_rate_per_day"].items():
        assert rate == pytest.approx(eff.rate_from_time_to_event(
            result["control_median_os_days"], result["treated_median_os_days"], multiple))


def test_route_2_rates_are_recomputed_from_its_own_recorded_burden_reductions():
    result = eff.ROUTE_2_LOSARTAN["result"]
    rates = eff.ROUTE_2_LOSARTAN["implied_rate_per_day"]
    assert rates["ct26"] == pytest.approx(eff.rate_from_burden_reduction(
        1 - result["ct26_burden_reduction"], result["ct26_day"]))
    assert rates["fourt1"] == pytest.approx(eff.rate_from_burden_reduction(
        1 - result["fourt1_burden_reduction"], result["fourt1_day"]))


def test_route_3_rates_are_recomputed_from_the_reported_strata():
    for multiple, rate in eff.ROUTE_3_REDOSING["implied_rate_per_day"].items():
        assert rate == pytest.approx(eff.rate_from_time_to_event(235, 490, multiple))


# ---------------------------------------------------------------------------------------------
# The result that separates the three.

def test_two_routes_clear_the_requirement_with_the_effect_discounted():
    for name in ("route_1_checkpoint", "route_2_losartan"):
        low, high = eff.TRANSFER_REQUIRED[name]["transfer_needed"]
        assert 0.0 < low <= high < 1.0, f"{name} should need less than full transfer"


def test_route_3_cannot_meet_the_requirement_even_at_full_transfer():
    low, _high = eff.TRANSFER_REQUIRED["route_3_redosing"]["transfer_needed"]
    assert low > 1.0, "route 3's best case should still fall short"


def test_losartan_has_the_largest_effect_and_the_widest_discount_tolerance():
    spans = {k: v["effect_span_per_day"] for k, v in eff.TRANSFER_REQUIRED.items()}
    assert max(spans["route_2_losartan"]) == max(max(s) for s in spans.values())
    needs = {k: min(v["transfer_needed"]) for k, v in eff.TRANSFER_REQUIRED.items()}
    assert needs["route_2_losartan"] == min(needs.values())


def test_the_module_records_that_the_three_are_not_interchangeable():
    entry = eff.THE_THREE_ROUTES_ARE_NOT_EQUIVALENT
    assert "cannot meet the requirement alone" in entry["route_3"]
    assert "are not" in entry["the_correction_this_forces"]
    assert "should not be relied" in entry["what_route_3_is_still_good_for"]


# ---------------------------------------------------------------------------------------------
# Coupling, and the limits.

def test_the_ccl2_link_is_recorded_with_its_two_sided_consequence():
    entry = eff.ROUTES_1_AND_2_ARE_MECHANISTICALLY_COUPLED
    assert "35665759" in entry["citation"]
    assert "MCP-1" in entry["the_finding"] and "CCL2" in entry["the_finding"]
    assert "RESISTANCE mechanism" in entry["why_this_matters"]
    assert "overlap rather than sum" in entry["the_caution_that_comes_with_it"]


def test_a_fourth_lever_is_noted_but_not_counted_among_the_three():
    entry = eff.ROUTES_1_AND_2_ARE_MECHANISTICALLY_COUPLED
    assert "meloxicam" in entry["a_fourth_lever_the_same_paper_hands_over"]
    assert "route_4" not in eff.TRANSFER_REQUIRED


def test_every_route_records_its_own_limits():
    for route in (eff.ROUTE_1_CHECKPOINT, eff.ROUTE_2_LOSARTAN, eff.ROUTE_3_REDOSING):
        assert route["the_limits"]
        assert "hemangiosarcoma" in route["the_limits"] or "osteosarcoma" in route["the_limits"]


def test_the_verdict_refuses_to_let_a_ratio_read_as_evidence():
    assert "arithmetic, not evidence" in eff.VERDICT["what_is_not"]
    assert "they do not say it is right" in eff.VERDICT["what_is_not"]
    assert eff.VERDICT["the_required_increment"] == pytest.approx(eff.REQUIRED_INCREMENT)
