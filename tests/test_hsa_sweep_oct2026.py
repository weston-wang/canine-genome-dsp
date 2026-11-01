"""Tests for the 2026-10-31 sweep dispositions.

The point of these is the same as the sweep's: a candidate may be set aside only on a scientific
reason, an empty result is only reportable once a control query has passed, and a sweep that
changes nothing must say so rather than manufacture a finding.
"""

import pytest

from canine_dsp import hsa_sweep_oct2026 as sw


def test_the_sweep_credited_nothing_and_says_so():
    assert sw.credited() == []
    assert "no new agent changes the conjunction" in sw.VERDICT["headline"]


def test_no_candidate_is_set_aside_for_want_of_canine_data():
    """Rule 13's hard constraint. Every withheld credit names a permitted reason kind."""
    assert sw.excluded_for_absent_canine_data() == []
    for f in sw.findings_by_disposition(sw.ASSESSED_NOT_CREDITED):
        assert f.reason_kind in (sw.KILL_CONTRADICTED, sw.DEFEATED_BY_ESCAPE,
                                 sw.WRONG_COMPARTMENT, sw.NOT_A_KILL), f.candidate
        assert "canine data are absent" not in f.why.lower(), f.candidate


def test_every_finding_carries_a_citation_a_report_and_a_reason():
    assert len(sw.FINDINGS) == 12
    for f in sw.FINDINGS:
        assert f.citation, f.candidate
        assert len(f.what_it_reports) > 60, f.candidate
        assert len(f.why) > 100, f.candidate
        assert f.disposition in (sw.ALREADY_IN_RECORD, sw.CREDITED,
                                 sw.ASSESSED_NOT_CREDITED, sw.CORRECTS_THE_RECORD), f.candidate


def test_all_eleven_angles_were_searched():
    assert len(sw.ANGLES_SEARCHED) == 11
    for angle, result in sw.ANGLES_SEARCHED.items():
        assert len(result) > 40, angle


def test_the_programs_own_vaccine_was_not_reported_as_a_new_find():
    """The sweep re-found eVim, which the program is built on. Reporting that as news would be
    exactly CLAUDE.md failure 4 and 6. It is dispositioned as already held."""
    evim = [f for f in sw.FINDINGS if "eVim" in f.candidate][0]
    assert evim.disposition == sw.ALREADY_IN_RECORD
    assert "the program's own vaccine arm" in evim.why
    assert "negative result for the sweep" in evim.why


def test_bnct_is_excluded_on_geometry_although_canine_kill_data_exist():
    """The interesting case: canine, disease-matched kill data DO exist, so the only admissible
    reason is the escape. If this ever flips to an absence the rule-13 test above should catch it."""
    b = [f for f in sw.FINDINGS if "boron" in f.candidate.lower()][0]
    assert b.reason_kind == sw.DEFEATED_BY_ESCAPE
    assert "not excluded for absent canine data" in b.why
    assert "no field to aim at" in b.why
    assert "2.60" in b.what_it_reports          # the measured CBE is on the record


def test_the_59_percent_is_not_recorded_as_an_effect_size():
    """An ORR in measurable disease is not a log-kill against micrometastases. The sweep's
    strongest-looking number is the one most at risk of being quoted as a closure input."""
    c = [f for f in sw.FINDINGS if "cabozantinib" in f.candidate][0]
    assert c.disposition == sw.ASSESSED_NOT_CREDITED
    assert c.reason_kind == sw.WRONG_COMPARTMENT
    assert "does not transfer to a log-kill" in c.why
    assert "NOT as an effect size" in c.why


def test_the_stacking_negative_does_not_reopen_a_settled_item():
    """A091902's first-line negative touches the levers-stacking question, which is graded
    TRANSFERRED. Rule 11 forbids re-listing it as open under any phrasing."""
    p = [f for f in sw.FINDINGS if "paclitaxel" in f.candidate][0]
    assert "already settled" in p.why
    assert "TRANSFERRED" in p.why
    assert "must not be read as reopening it" in p.why
    # and the audit still does not list it
    from canine_dsp import hsa_standard_audit as audit
    assert audit.failing() == []


def test_the_radiation_correction_fixes_a_reason_not_a_verdict():
    r = [f for f in sw.FINDINGS if "hypofractionated" in f.candidate][0]
    assert r.disposition == sw.CORRECTS_THE_RECORD
    assert "2,059" in r.what_it_reports
    assert "does not change the radiation disposition" in r.why
    # the class is still excluded, and now for the geometry alone
    from canine_dsp import hsa_agent_tiers as t
    body = [c for c in t.CLASS_LEDGER
            if c.modality_class == "radiation -- EXTERNAL BEAM to the body"][0]
    assert body.status == t.EXCLUDED
    assert "CORRECTED 2026-10-31" in body.the_evidence
    assert "PMID 42903052" in body.the_evidence
    assert "BOTH CLAUSES WERE FALSIFIED" in body.the_evidence
    assert "no transferable canine dataset exists" not in body.reason


def test_bnct_is_in_the_class_ledger_and_the_mix_still_has_no_theoretical_agent():
    from canine_dsp import hsa_agent_tiers as t
    classes = [c.modality_class for c in t.CLASS_LEDGER]
    assert any("boron neutron capture" in c for c in classes)
    assert t.classes_excluded_for_absent_canine_data() == []
    assert t.tier_mix()["theoretical"] == 0


def test_the_search_method_correction_names_the_control_that_caught_it():
    """A false negative of record. The lesson is only useful if it says how to catch the next one."""
    c = sw.SEARCH_METHOD_CORRECTION
    assert "SRC_TYPE is not a Europe PMC field" in c["why_it_was_wrong"]
    assert "hitCount 0" in c["why_it_was_wrong"]
    assert "cancer AND SRC_TYPE:PPR" in c["how_it_was_caught"]
    assert "SRC:PPR" in c["how_it_was_caught"]
    assert "control query" in c["the_general_rule"]
    assert "167" in c["what_it_cost"]


def test_the_only_claimed_empty_set_is_the_one_a_control_verified():
    """ferroptosis/GPX4 is reported empty and was control-verified; the preprint angle is NOT
    reported empty, because its zero turned out to be a query artefact."""
    assert sw.ANGLES_SEARCHED["ferroptosis / GPX4"].startswith("ZERO")
    assert "verified against" in sw.ANGLES_SEARCHED["ferroptosis / GPX4"]
    assert "167 records once the query was fixed" in sw.ANGLES_SEARCHED["preprints"]


def test_candid_provenance_is_corrected_in_both_modules():
    """0.784/0.909 is one point estimate's 95% CI, not two measurements. The sweep stays
    conservative because it keeps using the interval's low end."""
    from canine_dsp import hsa_open_route_closure as orc
    from canine_dsp import hsa_condition_closure as cc
    assert orc.CANDID_SCREENING["detection_rate_three_most_aggressive_cancers"] == pytest.approx(
        0.854)
    assert orc.CANDID_SCREENING["detection_rate_three_most_aggressive_95ci"] == (0.784, 0.909)
    # the point estimate sits inside its own interval, and the swept low end is the pessimistic one
    lo, hi = orc.CANDID_SCREENING["detection_rate_three_most_aggressive_95ci"]
    assert lo < orc.CANDID_SCREENING["detection_rate_three_most_aggressive_cancers"] < hi
    assert cc.CANDID_SENSITIVITY == (lo, hi)
    assert min(cc.CANDID_SENSITIVITY) == lo


def test_the_completeness_claim_is_bounded_and_names_its_one_gap():
    """The sweep claims completeness over REACHABLE sources, not over the literature. One document
    is unreadable, and it is enumerated rather than glossed so the claim carries its own limit."""
    u = sw.THE_ONE_UNREADABLE_SOURCE
    assert "42767940" in u["what_it_is"]
    assert "10.1111/vco.70098" in u["what_it_is"]
    assert "complete over REACHABLE sources" in u["scope_of_the_completeness_claim"]
    assert "cannot be claimed exhaustive" in u["scope_of_the_completeness_claim"]
    assert "property" in u["scope_of_the_completeness_claim"]
    # the blocker is diagnosed, not assumed -- including that the proxy was ruled out
    assert "recentRelayFailures: []" in u["why_it_is_unreadable"]
    assert "[Abstract not available]" in u["why_it_is_unreadable"]
    assert "no PMCID" in u["why_it_is_unreadable"]
    assert "forbidden" in u["the_only_thing_that_closes_it"]


def test_no_figure_depends_on_the_unreadable_source():
    """The point of enumerating it: the verdict must be invariant to whether it is ever read. Its
    numbers must not appear in any graded input anywhere in the package."""
    u = sw.THE_ONE_UNREADABLE_SOURCE
    assert "excluded from every input" in u["why_no_conclusion_rests_on_it"]
    assert "unchanged whether the abstract is read or not" in u["why_no_conclusion_rests_on_it"]
    assert "PREVENTION" in u["why_it_could_not_change_a_cell_anyway"]
    # the eBAT angle points at it instead of claiming exhaustiveness
    assert "UNREADABLE" in sw.ANGLES_SEARCHED["eBAT / uPAR"]
    assert "no conclusion here depends on it" in sw.ANGLES_SEARCHED["eBAT / uPAR"]
    # and the figures really are absent from the graded modules
    import pathlib
    src = pathlib.Path(sw.__file__).parent
    for mod in ("hsa_standard_audit.py", "hsa_deterministic_closure.py",
                "hsa_condition_closure.py", "hsa_route_effect_sizes.py"):
        text = (src / mod).read_text()
        assert "52/78" not in text, mod
        assert "2/15" not in text, mod


def test_nothing_in_the_sweep_moved_a_cell_or_a_condition():
    """The sweep's own claim, checked against the live conjunction rather than asserted."""
    from canine_dsp import hsa_deterministic_closure as dc
    from canine_dsp import hsa_condition_closure as cc
    conj = dc.conjunction()
    assert conj["nothing_open"]
    assert len(conj["partially_closed_cells"]) == 1
    assert dc.failing_conditions() == []
    assert cc.unmet() == []
