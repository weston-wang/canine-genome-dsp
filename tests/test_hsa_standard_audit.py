"""Tests for the HSA standard audit.

These enforce the thing the narrative cannot: that the bar is graded before anything is graded
against it, that the derivation is conservative rather than tuned, and that `failing()` reports
only genuine (a)/(b)-class failures rather than every absence.
"""
from __future__ import annotations

import math

import pytest

from canine_dsp import hsa_standard_audit as sa


# =================================================================================================
# The growth bar -- the input that had never been graded.
# =================================================================================================

def test_the_derivation_reproduces_from_the_published_intervals():
    d = sa.growth_bar_derivation()
    for n0 in sa.RESIDUAL_RANGE:
        for days, label in ((sa.DFI_DOXORUBICIN_DAYS, "dox_dfi"),
                            (sa.DFI_METRONOMIC_DAYS, "metronomic_dfi")):
            expected = math.log(sa.DETECTABLE_CELLS / n0) / days
            assert d["implied_net_regrowth_per_day"][f"{label}@{n0:.0e}"] == pytest.approx(
                expected, abs=5e-5)


def test_the_bar_in_use_is_conservative_not_flattering():
    """The whole point: a conservative bar cannot manufacture a closure."""
    d = sa.growth_bar_derivation()
    lo, hi = d["implied_range"]
    assert d["bar_in_use"] > hi, "the bar must sit above the clinically implied range"
    assert d["bar_is_conservative"] is True
    assert d["conservatism_factor"][0] >= 1.0


def test_the_detectable_threshold_is_the_harder_choice_not_the_easier_one():
    """Using the engine's lethal burden instead would imply faster rates and flatter the bar."""
    from canine_dsp.hsa_persister_evidence import TUMOR_CELLS
    assert sa.DETECTABLE_CELLS < TUMOR_CELLS
    harder = math.log(sa.DETECTABLE_CELLS / 1e6) / sa.DFI_DOXORUBICIN_DAYS
    easier = math.log(TUMOR_CELLS / 1e6) / sa.DFI_DOXORUBICIN_DAYS
    assert harder < easier


def test_the_range_is_declared_a_floor_because_the_rates_are_already_suppressed():
    why = sa.growth_bar_derivation()["why_the_range_is_a_floor_not_a_point"]
    assert "UNDER chemotherapy" in why
    assert "not that it is exact" in why


def test_the_derivation_does_not_claim_to_replace_the_value():
    """It reports a direction, not a new point estimate -- that distinction is the honest part."""
    d = sa.growth_bar_derivation()
    assert d["provenance"] == sa.DERIVED
    assert isinstance(d["implied_range"], tuple) and len(d["implied_range"]) == 2
    assert d["bar_in_use"] == sa.BAR_IN_USE, "the derivation must not silently change the bar"
    assert "DIRECTION" in (sa.growth_bar_derivation.__doc__ or "")


def test_the_derivation_independently_reinforces_the_route_12_closure():
    d = sa.growth_bar_derivation()
    note = d["and_it_reinforces_the_route_12_closure"]
    assert "0.110-0.143" in note
    from canine_dsp.hsa_escape_audit import THE_INTRINSIC_GROWTH_CEILING as c
    lo_t, hi_t = c["implied_ceiling_per_day"]
    lo_c, hi_c = d["implied_range"]
    assert lo_t / hi_c >= 2.0        # at least 2x the top of the clinical range
    assert hi_t / lo_c >= 10.0       # and ~11x the bottom


# =================================================================================================
# Sensitivity -- does the headline survive a different bar?
# =================================================================================================

def test_the_plan_survives_up_to_the_bar_in_use_but_not_far_beyond():
    s = sa.growth_sensitivity()
    assert s[0.0515]["required_multiple_of_measured"] == pytest.approx(1.40, abs=0.01)
    assert s[0.055]["inside_the_measured_ramp"] is True
    assert s[0.080]["inside_the_measured_ramp"] is False


def test_the_requirement_scales_linearly_with_the_bar():
    s = sa.growth_sensitivity((0.0515, 0.103))
    a = s[0.0515]["required_vaccine_kill_per_day"]
    b = s[0.103]["required_vaccine_kill_per_day"]
    assert b == pytest.approx(2 * a, rel=1e-3)


# =================================================================================================
# failing() -- the rule-11 discipline.
# =================================================================================================

def test_only_two_inputs_genuinely_fail():
    bad = sa.failing()
    assert len(bad) == 2
    names = {g.name for g in bad}
    assert names == {"immunity half-life", "post-remission annual rupture hazard"}


def test_both_failures_are_no_basis_and_both_are_load_bearing():
    for g in sa.failing():
        assert g.verdict is sa.Verdict.FAILS_NO_BASIS
        assert g.provenance == sa.ASSUMED
        assert g.load_bearing is True


def test_the_growth_bar_is_no_longer_among_the_failures():
    assert "growth bar" not in " ".join(g.name for g in sa.failing())
    bar = next(g for g in sa.GRADES if "growth bar" in g.name)
    assert bar.provenance == sa.DERIVED
    assert bar.verdict is sa.Verdict.PASSES
    assert "WAS a bare literal" in bar.why       # the history stays visible


def test_the_items_wrongly_called_gaps_are_recorded_rather_than_quietly_dropped():
    wrong = sa.wrongly_reported_as_gaps()
    assert len(wrong) == 3
    names = " ".join(g.name for g in wrong)
    assert "increment" in names
    assert "brain-metastasis" in names
    assert "Treg" in names
    for g in wrong:
        assert "that was wrong" in g.why or "grading against demonstration" in g.why


def test_inert_placeholders_are_marked_not_load_bearing():
    for g in sa.GRADES:
        if g.provenance == sa.ASSUMED and g.verdict is sa.Verdict.PASSES:
            assert g.load_bearing is False, g.name


def test_the_kill_ceilings_pass_because_the_conclusion_is_insensitive_to_them():
    g = next(x for x in sa.GRADES if "kill ceilings" in x.name)
    assert g.load_bearing is False
    assert "7%" in g.why                     # the bar barely moves across drug exposure


def test_no_grade_claims_measured_for_something_transferred():
    for g in sa.GRADES:
        assert g.provenance in (sa.MEASURED, sa.DERIVED, sa.TRANSFERRED, sa.ASSUMED)
    measured = [g for g in sa.GRADES if g.provenance == sa.MEASURED]
    # the only MEASURED input is the tumorgraft curve, which is a real measurement
    assert len(measured) == 1 and "tumorgraft" in measured[0].name


def test_the_statement_names_the_failures_rather_than_counting_absences():
    s = sa.statement()
    assert "2 genuinely fail" in s
    assert "immunity half-life" in s and "rupture hazard" in s
    assert "conservative" in s


def test_the_verdict_distinguishes_failing_inputs_from_open_escape_routes():
    v = sa.VERDICT
    assert "not escape routes" in v["the_answer"]
    assert "case (a)" in v["why_those_two_are_different_from_the_rest"]
    assert "rule 11" in v["why_those_two_are_different_from_the_rest"]
