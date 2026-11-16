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


# ---------------------------------------------------------------------------------------------
# From a transfer fraction to a durability number.

def test_durability_grid_is_monotone_in_the_increment():
    increments = sorted(eff.DURABILITY_BY_INCREMENT)
    for column in (0, 1):
        values = [eff.DURABILITY_BY_INCREMENT[i][column] for i in increments]
        assert values == sorted(values), f"non-monotone column {column}: {values}"


def test_durability_interpolation_reproduces_the_grid_points():
    for increment, (at_y1, at_y2) in eff.DURABILITY_BY_INCREMENT.items():
        assert eff.durability_at_increment(increment, 1) == pytest.approx(at_y1)
        assert eff.durability_at_increment(increment, 2) == pytest.approx(at_y2)


def test_durability_interpolation_lands_between_its_neighbours():
    below = eff.durability_at_increment(0.0120, 1)
    above = eff.durability_at_increment(0.0135, 1)
    middle = eff.durability_at_increment(0.01275, 1)
    assert below < middle < above


def test_durability_interpolation_clamps_outside_the_grid():
    top = max(eff.DURABILITY_BY_INCREMENT)
    assert eff.durability_at_increment(top * 10, 1) == pytest.approx(
        eff.DURABILITY_BY_INCREMENT[top][0])
    assert eff.durability_at_increment(0.0, 1) == pytest.approx(
        eff.DURABILITY_BY_INCREMENT[0.0][0])


def test_durability_helpers_reject_bad_arguments():
    with pytest.raises(ValueError):
        eff.durability_at_increment(0.01, stop_year=3)
    with pytest.raises(ValueError):
        eff.durability_at_increment(-0.01)
    with pytest.raises(ValueError):
        eff.durability_at_transfer("route_9", 0.5)
    for bad in (-0.1, 1.1):
        with pytest.raises(ValueError):
            eff.durability_at_transfer("route_2_losartan", bad)


def test_the_conservative_default_is_actually_conservative():
    for route in eff.DURABILITY_BY_TRANSFER:
        cautious = eff.durability_at_transfer(route, 0.5, conservative=True)
        hopeful = eff.durability_at_transfer(route, 0.5, conservative=False)
        assert cautious <= hopeful, route


def test_losartan_beats_the_drug_forever_reference_at_a_quarter_transfer():
    """Three-quarters of the measured effect can be lost and the dog is still better off."""
    assert (eff.durability_at_transfer("route_2_losartan", 0.25)
            > eff.REFERENCE_DRUG_FOREVER)


def test_the_checkpoint_route_needs_about_half_its_conservative_effect():
    assert eff.durability_at_transfer("route_1_checkpoint", 0.25) < eff.REFERENCE_DRUG_FOREVER
    assert eff.durability_at_transfer("route_1_checkpoint", 0.50) > eff.REFERENCE_DRUG_FOREVER


def test_redosing_never_reaches_the_reference_at_any_transfer():
    for optimism in (True, False):
        assert (eff.durability_at_transfer("route_3_redosing", 1.0, conservative=not optimism)
                < eff.REFERENCE_DRUG_FOREVER)


def test_the_engine_and_the_arithmetic_agree_about_route_3():
    """Two independent statements of the same conclusion, checked against each other."""
    assert min(eff.TRANSFER_REQUIRED["route_3_redosing"]["transfer_needed"]) > 1.0
    assert eff.durability_at_transfer("route_3_redosing", 1.0) < eff.REFERENCE_DRUG_FOREVER


def test_the_interpolation_caveat_is_recorded():
    note = eff.WHAT_THE_MODEL_SAYS_ABOUT_PARTIAL_TRANSFER["the_interpolation_caveat"]
    assert "not simulations" in note


# =================================================================================================
# ROUTE 4 -- eBAT reclassified from cytotoxic log-remover to stromal lever.
# =================================================================================================

def test_ebat_effect_is_derived_from_a_tumour_it_cannot_kill():
    """The whole point of the MC17 model is that direct cytotoxicity is excluded by design."""
    design = eff.ROUTE_4_EBAT_STROMAL["design"]
    assert "resistant to eBAT" in design
    assert "microenvironment rather than direct cytotoxicity" in design


def test_ebat_transfer_sits_between_losartan_and_the_checkpoint_route():
    ebat = eff.TRANSFER_REQUIRED["route_4_ebat_stromal"]["transfer_needed"]
    losartan = eff.TRANSFER_REQUIRED["route_2_losartan"]["transfer_needed"]
    checkpoint = eff.TRANSFER_REQUIRED["route_1_checkpoint"]["transfer_needed"]
    assert min(losartan) < min(ebat) < min(checkpoint)
    assert max(ebat) < max(checkpoint)


def test_ebat_needs_less_than_a_quarter_of_its_measured_effect():
    assert max(eff.TRANSFER_REQUIRED["route_4_ebat_stromal"]["transfer_needed"]) < 0.25


def test_ebat_beats_the_drug_forever_reference_at_a_quarter_transfer():
    assert (eff.durability_at_transfer("route_4_ebat_stromal", 0.25)
            > eff.REFERENCE_DRUG_FOREVER)


def test_ebat_falls_short_of_the_reference_at_a_tenth_transfer():
    """It clears with margin, but it is not immune to the transfer question."""
    assert (eff.durability_at_transfer("route_4_ebat_stromal", 0.10)
            < eff.REFERENCE_DRUG_FOREVER)


def test_the_ebat_rate_is_computed_from_the_published_volumes():
    expected = eff.rate_from_burden_reduction(
        eff.EBAT_TREATED_VOLUME_MM3 / eff.EBAT_CONTROL_VOLUME_MM3, eff.EBAT_READOUT_DAY)
    assert eff.ROUTE_4_EBAT_STROMAL["implied_rate_per_day"]["readout_day"] == pytest.approx(expected)


def test_the_ebat_rate_is_as_cross_species_as_losartans_and_says_so():
    limits = eff.ROUTE_4_EBAT_STROMAL["the_limits"]
    assert "mouse fibrosarcoma" in limits
    assert "no better than losartan" in limits
    assert "intensification trial was negative" in limits


def test_what_distinguishes_ebat_is_not_the_rate():
    claim = eff.ROUTE_4_EBAT_STROMAL["what_makes_it_better_placed_than_the_other_three"]
    assert "as cross-species as losartan" in claim
    assert "exposure and duration IN THIS DISEASE" in claim


def test_ebat_rescues_the_route_8_stain_rather_than_closing_it():
    rescue = eff.ROUTE_4_EBAT_STROMAL["what_it_rescues"]
    assert "does not need the compartment to express its targets" in rescue
    assert "secondary" in rescue


def test_the_misclassification_is_recorded_rather_than_quietly_fixed():
    correction = eff.THE_THREE_ROUTES_ARE_NOT_EQUIVALENT["the_correction_route_4_forces"]
    assert "wrong section" in correction


def test_the_first_lever_to_measure_is_not_the_one_with_the_best_transfer():
    pick = eff.VERDICT["which_one_to_measure_first"]
    assert "eBAT" in pick
    assert "losartan's is" in pick
    best_transfer = min(
        eff.TRANSFER_REQUIRED[r]["transfer_needed"][0] for r in eff.TRANSFER_REQUIRED)
    assert best_transfer == eff.TRANSFER_REQUIRED["route_2_losartan"]["transfer_needed"][0]


# =================================================================================================
# What the checkpoint lever costs, revised upward.
# =================================================================================================

def test_the_checkpoint_toxicity_update_is_not_overstated():
    cost = eff.WHAT_THE_CHECKPOINT_LEVER_COSTS
    appeared = cost["the_figure_that_has_since_appeared"]
    assert "28%" in appeared and "Grade 3" in appeared
    assert "mast cell tumour" in appeared          # the reason it does not simply replace 5.9%
    assert "5.9% figure remains" in cost["why_it_is_not_a_straight_replacement"]
    assert "weakened, not withdrawn" in cost["what_it_does_change"]


def test_the_conditional_licensure_is_recorded_alongside_the_toxicity():
    assert "conditional licensure" in eff.WHAT_THE_CHECKPOINT_LEVER_COSTS["the_offsetting_development"]


def test_the_randomised_negative_in_the_matched_setting_is_recorded():
    p = eff.THE_PRECEDENT_THAT_CUTS_AGAINST_THE_VACCINE_CALIBRATION
    assert "NO" in p["the_finding"] and "difference in recurrence-free" in p["the_finding"]
    assert "does not invalidate" in p["what_it_does_to_the_calibration"]
    assert "endpoint mismatch" in p["what_it_does_to_the_calibration"]
