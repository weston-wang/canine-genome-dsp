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


# =================================================================================================
# The deterministic conjunction (rule 12). Kept in this file so the two audits are run together.
# =================================================================================================

def test_the_conjunction_contains_no_probability():
    """Rule 12: the headline must be decidable. No float may appear in the verdict."""
    from canine_dsp import hsa_deterministic_closure as dc
    c = dc.conjunction()
    assert not any(isinstance(v, float) for v in c.values())
    for row in c["matrix"].values():
        assert set(row.values()) <= {dc.CLOSED, dc.PARTIALLY_CLOSED, dc.OPEN, dc.NOT_APPLICABLE}


def test_brain_SRT_is_not_credited_because_it_cannot_find_an_occult_deposit():
    """SRT has maximal CNS reach but only against an imaged target. Crediting it against occult
    seeding would be crediting a mechanism against a target it cannot locate."""
    from canine_dsp import hsa_deterministic_closure as dc
    assert dc.reaches("brain_SRT", dc.Site.CNS) is True   # reasoned about
    for r in dc.ROUTES:                                    # but never counted
        assert "brain_SRT" not in r.closed_by, r.number
    assert "occult" in dc.VERDICT["brain_SRT_is_deliberately_not_credited"].lower()


def test_the_alkylator_closure_does_not_claim_a_survival_benefit():
    """The 30-dog lomustine trial's overall median was NOT better than the anthracycline alone."""
    from canine_dsp import hsa_deterministic_closure as dc
    note = dc.VERDICT["what_this_does_NOT_claim"]
    assert "not better than" in note
    assert "UNMEASURED" in note
    assert "DELIVERABILITY and REACH" in note


def test_lomustine_is_recorded_as_a_finite_course_agent_not_a_floor_holder():
    from canine_dsp import hsa_deterministic_closure as dc
    assert "350 mg/m2" in dc.REACH_BASIS["lomustine"]
    assert "FINITE-COURSE" in dc.REACH_BASIS["lomustine"]
    assert "NOT a chronic floor-holder" in dc.REACH_BASIS["lomustine"]


def test_the_two_alkylators_cover_each_others_weakness():
    from canine_dsp import hsa_deterministic_closure as dc
    assert "stage II splenic hemangiosarcoma" in dc.REACH_BASIS["lomustine"]
    assert "ANGIOSARCOMA-SPECIFIC CNS evidence" in dc.REACH_BASIS["temozolomide"]
    assert "lomustine lacks" in dc.REACH_BASIS["temozolomide"]


def test_nothing_is_open_and_the_one_partial_cell_is_a_competing_event():
    """Routes 8 and 12b closed once two CNS-penetrant alkylators were evidenced. Route 5's CNS form
    then moved OPEN -> PARTIALLY CLOSED on a canine intracranial resection series. 'Partial' is
    reported as its own category: rounding it up would overstate, rounding it down would discard
    same-species evidence."""
    from canine_dsp import hsa_deterministic_closure as dc
    c = dc.conjunction()
    assert c["open_cells"] == []
    assert c["nothing_open"] is True
    assert c["all_closed"] is False          # partial is not closed
    assert len(c["partially_closed_cells"]) == 1
    (number, _, site), = c["partially_closed_cells"]
    assert number == "5" and site == dc.Site.CNS.value
    assert "COMPETING EVENT" in dc.VERDICT[
        "what_remains_open_and_why_it_is_not_a_cancer_control_failure"]


def test_the_partial_cell_states_both_reasons_it_is_not_closed():
    """A partial grade is only honest if it names what is missing: no survival benefit shown, and
    reach limited to a solitary imaged deposit."""
    from canine_dsp import hsa_deterministic_closure as dc
    basis = dc.ROUTE_5_CNS_PARTIAL_BASIS
    assert "PMID 42038052" in basis
    assert "no survival benefit" in basis
    assert "SOLITARY IMAGED" in basis
    assert "occult or multifocal" in basis
    assert dc.VERDICT["why_that_cell_is_partial_and_not_closed"] == basis


def test_the_regrade_is_reported_with_the_condition_it_exposed():
    """The CNS regrade is only admissible alongside the new open condition it creates: every CNS
    closure here needs the deposit imaged, and the assumed surveillance is abdominal and thoracic."""
    from canine_dsp import hsa_deterministic_closure as dc
    cond = next(c for c in dc.CONDITIONS if "brain" in c.what)
    assert cond.status.startswith("OPEN")
    assert cond in dc.failing_conditions()
    assert "did not simply get better" in dc.VERDICT["the_cost_of_that_regrade"]


def test_routes_8_and_12b_close_in_the_cns_only_via_an_alkylator():
    """The systemic closers still do not cross; what closes these cells is the alkylator."""
    from canine_dsp import hsa_deterministic_closure as dc
    for number in ("8", "12b"):
        route = next(r for r in dc.ROUTES if r.number == number)
        assert dc.route_status(route, dc.Site.CNS) == dc.CLOSED
        crossers = [m for m in route.closed_by if dc.reaches(m, dc.Site.CNS)]
        assert set(crossers) == {"lomustine", "temozolomide"}, number
        # and the original systemic closers genuinely still do not reach
        for blocked in ("doxorubicin", "eBAT", "MEK_plus_TORC1_2"):
            if blocked in route.closed_by:
                assert not dc.reaches(blocked, dc.Site.CNS)


def test_splenic_rupture_is_not_counted_five_times():
    """Scoring route 5 OPEN at every distant site would count one hazard once per compartment."""
    from canine_dsp import hsa_deterministic_closure as dc
    r5 = next(r for r in dc.ROUTES if r.number == "5")
    assert dc.route_status(r5, dc.Site.SPLEEN) == dc.CLOSED
    assert dc.route_status(r5, dc.Site.LUNG) == dc.NOT_APPLICABLE
    assert dc.route_status(r5, dc.Site.CNS) == dc.PARTIALLY_CLOSED   # resectable if imaged


def test_the_t_cell_arm_is_what_reaches_the_cns_and_the_antibody_arm_is_not():
    from canine_dsp import hsa_deterministic_closure as dc
    assert dc.reaches("vaccine_T_cell_arm", dc.Site.CNS) is True
    assert dc.reaches("vaccine_antibody_arm", dc.Site.CNS) is False
    for agent in ("doxorubicin", "eBAT", "losartan", "MEK_plus_TORC1_2"):
        assert dc.reaches(agent, dc.Site.CNS) is False, agent


def test_the_verdict_corrects_the_earlier_overclaim():
    from canine_dsp import hsa_deterministic_closure as dc
    assert "NO cell is OPEN and one is PARTIALLY" in dc.VERDICT["headline"]
    assert "intracranial haemorrhage" in dc.VERDICT["headline"]


def test_the_odds_are_explicitly_demoted_to_sensitivity():
    from canine_dsp import hsa_deterministic_closure as dc
    o = dc.odds_are_secondary()
    assert "Never quote a durability figure as the verdict" in o["the_rule"]
    assert "averages over anatomical compartments" in o["what_the_number_hid_in_this_analysis"]
    assert "sensitivity" in o["what_the_numbers_are_still_good_for"].lower()


def test_the_condition_list_is_finite_and_names_what_fails():
    from canine_dsp import hsa_deterministic_closure as dc
    assert 5 <= len(dc.CONDITIONS) <= 20
    failing = dc.failing_conditions()
    assert len(failing) == 3
    joined = " ".join(c.what for c in failing)
    assert "CNS-penetrant" not in joined, "that condition is now met"
    assert "half-life" in joined and "rupture hazard" in joined
    # The haemorrhage condition is no longer failing -- it went to PARTIAL on PMID 42038052 -- and a
    # brain-imaging condition opened in the same move. The count did not improve.
    assert "haemorrhage" not in joined
    assert "include the brain" in joined
    haem = next(c for c in dc.CONDITIONS if "haemorrhage" in c.what)
    assert haem.status.startswith("PARTIAL")
    for c in dc.CONDITIONS:
        assert c.how_to_settle, c.what


def test_reaches_rejects_an_unknown_mechanism():
    from canine_dsp import hsa_deterministic_closure as dc
    with pytest.raises(ValueError):
        dc.reaches("stem cell transplant", dc.Site.CNS)


def test_the_increment_is_never_in_the_failing_list():
    """Failure 10: the increment was presented as a failing item for a third time, in softened words
    ("has never been measured in this tumour"). It is graded PASSES on KEYNOTE-942 plus four transfer
    derivations. This test makes the grading machine-checkable in both directions: present in
    wrongly_reported_as_gaps(), and absent from failing()."""
    from canine_dsp import hsa_standard_audit as sa
    inc = next(g for g in sa.GRADES if "increment" in g.name)
    assert inc.verdict is sa.Verdict.PASSES
    assert inc.provenance == sa.TRANSFERRED
    assert inc.previously_reported_as_gap is True
    assert inc.load_bearing is True              # load-bearing AND closed are not in tension
    assert inc not in sa.failing()
    assert inc in sa.wrongly_reported_as_gaps()
    assert "KEYNOTE-942" in inc.why
    assert "grading against demonstration" in inc.why


def test_failing_is_exactly_the_two_bare_numbers():
    """The answer to "what is still open" is this list and nothing else. If a third item belongs here
    it has to be added deliberately, not narrated into an answer."""
    from canine_dsp import hsa_standard_audit as sa
    failing = sa.failing()
    assert len(failing) == 2
    names = " ".join(g.name for g in failing)
    assert "immunity half-life" in names
    assert "rupture hazard" in names
    for g in failing:
        assert g.verdict is sa.Verdict.FAILS_NO_BASIS, g.name
        assert g.provenance == sa.ASSUMED, g.name
        assert g.load_bearing is True, g.name


def test_the_stacking_worry_is_closed_and_not_a_live_gap():
    """"Do the four levers stack?" is the increment objection in another costume. It was tested
    against the existing grid: the plan does not depend on stacking."""
    from canine_dsp import hsa_escape_audit as ea
    d = ea.DOES_THE_PLAN_DEPEND_ON_THE_LEVERS_STACKING
    assert d["grade"] == "TRANSFERRED"
    needed = d["transfer_needed_to_beat_the_drug_forever_reference"]
    assert needed["winner_takes_all_best_lever_only"] == 0.25
    assert needed["full_addition_all_four"] == 0.10
    assert "does NOT depend" in d["what_this_closes"]
    # and the caveat that genuinely survives is antagonism, not overlap
    assert "ANTAGONISTIC" in d["the_caveat_that_survives"]
