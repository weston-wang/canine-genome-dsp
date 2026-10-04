"""Tests for the C6-C9 closures.

These check the shape of each closure as much as its content: a closure is only admissible here if it
names the proxy it used, grades itself, and states what it does not claim. The last part is what
stops "the condition is met" drifting into "the number is measured".
"""

import pytest

from canine_dsp import hsa_condition_closure as cc


def test_all_four_conditions_close():
    assert cc.unmet() == []
    assert len(cc.CLOSURES) == 4
    conditions = " ".join(c.condition for c in cc.CLOSURES)
    assert "immunity half-life" in conditions
    assert "rupture hazard" in conditions
    assert "intracranial haemorrhage" in conditions
    assert "include the brain" in conditions


def test_every_closure_names_a_proxy_a_grade_and_a_non_claim():
    for c in cc.CLOSURES:
        assert c.status == cc.MET, c.condition
        assert c.grade in (cc.MEASURED, cc.DERIVED, cc.TRANSFERRED), c.condition
        assert c.grade != cc.ASSUMED, c.condition
        assert len(c.proxy) > 40, c.condition
        assert len(c.basis) > 150, c.condition
        assert len(c.does_not_claim) > 80, c.condition


def test_no_closure_claims_to_be_a_measurement_in_the_dog():
    """Nothing here moved from unmeasured to measured. Two conditions acquired a written basis and
    two were structural. The grades must reflect that: no MEASURED among them."""
    assert all(c.grade != cc.MEASURED for c in cc.CLOSURES)
    assert "nothing moved from 'unmeasured' to 'measured'" in cc.VERDICT["what_changed_in_kind"]


# =================================================================================================
# C6 -- and the precedent that constrains it.
# =================================================================================================

def test_c6_rejects_titre_as_the_proxy_because_the_record_disqualified_it():
    """The randomised ganglioside trial raised titre durably in surgically disease-free sarcoma and
    moved neither RFS nor OS. So a serological proxy is inadmissible, and the closure says so."""
    assert "NOT antibody titre" in cc.C6_IMMUNITY_HALF_LIFE.proxy
    assert "FUNCTIONAL" in cc.C6_IMMUNITY_HALF_LIFE.proxy
    assert "PMID 36215947" in cc.__doc__
    assert "Titre rose; survival did not" in cc.__doc__
    assert "PMID 36215947" in cc.C6_IMMUNITY_HALF_LIFE.does_not_claim


def test_c6_basis_is_the_matched_surgical_setting_not_measurable_disease():
    basis = cc.C6_IMMUNITY_HALF_LIFE.basis
    assert "PMID 33479501" in basis
    assert "SURGICALLY RESECTED" in basis
    assert "epitope spreading" in basis          # the functional corroboration
    assert "tumour infiltration" in basis
    assert cc.C6_IMMUNITY_HALF_LIFE.grade == cc.TRANSFERRED


def test_c6_does_not_claim_a_four_year_half_life():
    note = cc.C6_IMMUNITY_HALF_LIFE.does_not_claim
    assert note.startswith("that the half-life is 4 years")
    assert "n=8" in note
    assert "persistence equals protection" in note


def test_the_booster_margin_is_computed_and_wide():
    m = cc.booster_margin_against_measured_persistence()
    assert m["measured_persistence_days"] == pytest.approx(1460.0)
    assert m["margin_by_interval"]["q60d"] == pytest.approx(1460 / 60)
    assert m["margin_by_interval"]["q180d"] == pytest.approx(1460 / 180)
    # the condition is about outlasting the dosing interval, not about the half-life itself
    assert all(v >= 8 for v in m["margin_by_interval"].values())
    assert "without pinning the half-life" in m["why_this_form_of_the_argument"]


# =================================================================================================
# C7 -- the bound, and its thinness.
# =================================================================================================

def test_the_breaking_point_is_monotone_in_screening_sensitivity():
    """Better screening should tolerate a worse underlying hazard. If this inverts, the bisection or
    the screening model is wrong."""
    low = cc.breaking_point_hazard(0.888, 0.784)
    high = cc.breaking_point_hazard(0.888, 0.909)
    assert high > low
    better = cc.breaking_point_hazard(0.992, 0.784)
    assert better > low          # better tumour control also tolerates more hazard


def test_the_breaking_point_brackets_the_published_range():
    b = cc.c7_bound()
    assert 0.25 < b["worst_case_breaking_point"] < 0.27      # ~26%
    assert 0.70 < b["best_case_breaking_point"] < 0.75       # ~73%
    assert b["swept_range"] == (0.02, 0.10)
    assert b["margin_over_top_of_swept_range"] == pytest.approx(
        b["worst_case_breaking_point"] / 0.10)
    assert b["margin_over_top_of_swept_range"] > 2.0


def test_the_bisection_agrees_with_a_direct_evaluation():
    """Independent check of the solver: at the breaking point, joint durability should sit at the
    threshold; just inside it should be above, just outside below."""
    from canine_dsp.hsa_open_route_closure import joint_durability
    tc, sens = 0.888, 0.784
    bp = cc.breaking_point_hazard(tc, sens)
    at = joint_durability(tc, bp * (1 - sens), years=10.0)["joint_durability"]
    assert at == pytest.approx(0.50, abs=1e-3)
    inside = joint_durability(tc, (bp * 0.9) * (1 - sens), years=10.0)["joint_durability"]
    outside = joint_durability(tc, (bp * 1.1) * (1 - sens), years=10.0)["joint_durability"]
    assert inside > 0.50 > outside


def test_c7_does_not_claim_the_hazard_was_measured():
    note = cc.C7_RUPTURE_HAZARD.does_not_claim
    assert "has been measured" in note or "not" in note
    assert "not pretend otherwise" in note
    assert "2.6" in note                      # the thinness is stated, not buried
    assert cc.C7_RUPTURE_HAZARD.grade == cc.DERIVED
    assert "smallest margin anywhere in this ledger" in cc.VERDICT["the_one_that_is_thinnest"]


def test_the_ruffoni_ceiling_is_labelled_crude_not_tight():
    ceiling = cc.c7_bound()["the_ceiling_from_real_data"]
    assert "lifetime event" in ceiling
    assert "not an annual hazard" in ceiling
    assert "crude ceiling rather than a tight one" in ceiling


def test_a_dog_in_remission_has_no_spleen_and_the_argument_uses_that():
    assert "no spleen" in cc.C7_RUPTURE_HAZARD.basis
    assert "metastatic deposits" in cc.C7_RUPTURE_HAZARD.basis


# =================================================================================================
# C8 and C9 -- one problem, closed in the right order.
# =================================================================================================

def test_c9_closes_on_the_structure_of_the_claim_not_on_a_prevalence():
    """The conjunction is over sites as well as routes, so brain imaging is forced at any
    prevalence. Closing it on the unverified ~14% would make an ungraded number load-bearing."""
    basis = cc.C9_BRAIN_IMAGING.basis
    assert "conjunction over routes AND SITES" in basis
    assert "open at one site is open" in basis
    assert "14%" in cc.C9_BRAIN_IMAGING.does_not_claim
    assert "asserts nothing from it" in cc.C9_BRAIN_IMAGING.does_not_claim
    assert "load-bearing" in cc.C9_BRAIN_IMAGING.does_not_claim


def test_c9_specifies_an_actual_protocol():
    assert "brain MRI" in cc.C9_BRAIN_IMAGING.basis
    assert "same cadence" in cc.C9_BRAIN_IMAGING.basis


def test_c8_depended_on_c9_and_says_so():
    """C8 was partial only because its treating component reaches an imaged deposit. C9 supplies the
    imaging, so the dependency has to be explicit or the closure is circular-looking."""
    assert "C9" in cc.C8_INTRACRANIAL_HAEMORRHAGE.basis
    assert "IMAGED" in cc.C8_INTRACRANIAL_HAEMORRHAGE.basis
    assert "PMID 42038052" in cc.C8_INTRACRANIAL_HAEMORRHAGE.basis
    assert cc.C8_INTRACRANIAL_HAEMORRHAGE.grade == cc.TRANSFERRED


def test_c8_still_disclaims_survival_benefit():
    note = cc.C8_INTRACRANIAL_HAEMORRHAGE.does_not_claim
    assert "any survival benefit" in note
    assert "eleven months" in note
    assert "multifocal" in note


# =================================================================================================
# The honesty backstop.
# =================================================================================================

def test_what_is_still_unmeasured_survives_every_condition_closing():
    """This is the point of the module. No condition fails and five numbers are still unmeasured."""
    rem = cc.what_is_still_unmeasured()
    assert len(rem) == 5
    joined = " ".join(rem.values()).lower()
    assert "still unmeasured" in joined
    keys = " ".join(rem.keys())
    assert "immunity half-life" in keys
    assert "rupture hazard" in keys
    assert "brain-metastasis rate" in keys
    assert "vaccine height" in keys


def test_the_verdict_separates_closing_a_condition_from_measuring_a_number():
    v = cc.VERDICT
    assert "No condition" in v["headline"] or "no condition" in v["headline"].lower()
    assert "exactly as unmeasured as they" in v["what_changed_in_kind"]
    assert "C7" in v["the_one_that_is_thinnest"]


def test_the_screening_model_reproduces_the_documents_published_table():
    """The C7 bound is only meaningful if its screening model is the same one section 3b's published
    joint-durability table used. That table is tumour_control = 1.0 over ten years, with screening
    removing the detected fraction. All nine cells must come back exactly."""
    from canine_dsp.hsa_open_route_closure import joint_durability
    published = {
        0.02: (0.817, 0.958, 0.982),
        0.05: (0.599, 0.897, 0.955),
        0.10: (0.349, 0.804, 0.913),
    }
    for hazard, (unscreened, low_sens, high_sens) in published.items():
        assert joint_durability(1.0, hazard, years=10.0)["joint_durability"] == pytest.approx(
            unscreened, abs=1e-3)
        assert joint_durability(1.0, hazard * (1 - 0.784), years=10.0
                                )["joint_durability"] == pytest.approx(low_sens, abs=1e-3)
        assert joint_durability(1.0, hazard * (1 - 0.909), years=10.0
                                )["joint_durability"] == pytest.approx(high_sens, abs=1e-3)


def test_the_bound_is_stricter_than_the_published_table():
    """c7_bound applies tumour control on top of hazard survival, where the published table used 1.0.
    So the breaking points reported here are conservative relative to the figures in the document."""
    from canine_dsp.hsa_open_route_closure import joint_durability
    for tc in cc.TUMOUR_CONTROL_VARIANTS:
        assert tc < 1.0
        strict = joint_durability(tc, 0.05 * (1 - 0.784), years=10.0)["joint_durability"]
        published = joint_durability(1.0, 0.05 * (1 - 0.784), years=10.0)["joint_durability"]
        assert strict < published


def test_a_met_condition_does_not_promote_a_route_site_cell():
    """C8 is MET while route 5's CNS cell is still PARTIALLY CLOSED. That looks like a contradiction
    and is not: the condition asks whether a treating component exists, the cell asks whether the
    route is closed at that site. Upgrading the cell because a neighbouring condition closed would be
    a forced closure, so the ledger must keep them apart and say why."""
    from canine_dsp import hsa_deterministic_closure as dc
    d = cc.WHY_A_CELL_STAYS_PARTIAL_WHILE_C8_IS_MET
    # the states this test is about really do coexist
    conj = dc.conjunction()
    assert len(conj["partially_closed_cells"]) == 1
    assert dc.failing_conditions() == []
    assert cc.C8_INTRACRANIAL_HAEMORRHAGE.status == cc.MET
    # and the reason is recorded
    assert "different objects" in d["the_apparent_contradiction"]
    assert "SOLITARY" in d["what_the_cell_grades"]
    assert "forced closure" in d["why_the_cell_was_NOT_upgraded"]
    assert "never promotes" in d["the_rule_this_sets"]
