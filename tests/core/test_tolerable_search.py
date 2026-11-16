"""Toxicity and delivery must be enforced by the model, not asserted in prose."""

from __future__ import annotations

from canine_dsp.core import tolerable_search as ts
from canine_dsp.core.catalogue import GROWTH_PER_DAY, PARENCHYMA, agents_in
from canine_dsp.core.delivery import (CONVECTION_ENHANCED_DELIVERY, EFFLUX_INHIBITION,
                                      FOCUSED_ULTRASOUND, Geometry, ROUTES, obtainable_routes)
from canine_dsp.core.toxicity import (EFFLUX_INHIBITOR_TOXICITY_MULTIPLIER, Organ, PROFILES,
                                      axis_loads, headroom, profile_for, tolerable)


# --- delivery is now composable, which was the whole complaint --------------------------------------

def test_the_search_can_now_see_ultrasound_at_all():
    assert any("ultrasound" in r.name for r in ROUTES)
    assert FOCUSED_ULTRASOUND.obtainable_for_a_dog is True


def test_a_focal_route_does_nothing_against_diffuse_disease_and_the_model_enforces_it():
    tram = next(a for a in agents_in(PARENCHYMA) if a.name.startswith("trametinib"))
    assert FOCUSED_ULTRASOUND.geometry is Geometry.FOCAL
    unchanged = FOCUSED_ULTRASOUND.apply(tram, disease_is_diffuse=True)
    assert unchanged.effective_kill == tram.effective_kill, "geometry, not a multiplier"


def test_even_a_focal_tumour_does_not_rescue_ultrasound():
    tram = next(a for a in agents_in(PARENCHYMA) if a.name.startswith("trametinib"))
    improved = FOCUSED_ULTRASOUND.apply(tram, disease_is_diffuse=False)
    assert improved.effective_kill > tram.effective_kill
    assert improved.effective_kill < GROWTH_PER_DAY, "tight junctions, not the pump"


def test_ultrasound_does_not_defeat_efflux_but_the_co_dose_does():
    assert FOCUSED_ULTRASOUND.defeats_efflux is False
    assert EFFLUX_INHIBITION.defeats_efflux is True


def test_a_route_cannot_carry_an_agent_class_it_has_no_mechanism_for():
    clod = next(a for a in agents_in(PARENCHYMA) if "clodronate" in a.name)
    assert FOCUSED_ULTRASOUND.apply(clod) is None, "a liposome is excluded by size"


def test_duration_is_carried_on_the_route_and_is_what_kills_ced():
    assert CONVECTION_ENHANCED_DELIVERY.duty < 0.01
    tram = next(a for a in agents_in(PARENCHYMA) if a.name.startswith("trametinib"))
    ced = CONVECTION_ENHANCED_DELIVERY.apply(tram, disease_is_diffuse=False)
    assert ced.effective_kill < GROWTH_PER_DAY


def test_the_recorded_ultrasound_verdict_matches_the_model():
    u = ts.ULTRASOUND_IS_FORECLOSED_BY_GEOMETRY
    assert "FOCAL and this disease is DIFFUSE" in u["and_it_changes_nothing_here"]
    assert "TIGHT JUNCTIONS and the constraint is a PUMP" in u["even_granting_a_focal_tumour"]


# --- toxicity is now enforced ------------------------------------------------------------------------

def test_every_agent_in_the_catalogue_has_a_toxicity_profile():
    for a in agents_in(PARENCHYMA):
        assert profile_for(a.name).axis is not None, a.name


def test_agents_on_different_axes_combine_freely():
    combo = ["radiation", "anti-PD-1", "liposomal clodronate"]
    assert tolerable([profile_for(n) for n in combo])


def test_same_axis_agents_add_which_is_the_shared_axis_finding():
    both = [profile_for("trametinib"), profile_for("ERK inhibitor")]
    load = axis_loads(both)[Organ.SKIN_VASCULAR]
    assert load > 1.0, "a vertical MAPK pair shares an axis and oversubscribes it"
    assert not tolerable(both)


def test_the_proposed_six_agent_regimen_is_tolerable_without_the_co_dose():
    r = ts.regimen_toxicity(["radiation", "anti-PD-1", "liposomal clodronate", "lomustine",
                             "trametinib", "parthenolide"])
    assert r["tolerable"] is True
    assert r["headroom"] > 0


# --- the efflux co-dose is charged for, which is the point --------------------------------------------

def test_the_efflux_co_dose_raises_systemic_exposure_and_is_charged():
    assert EFFLUX_INHIBITOR_TOXICITY_MULTIPLIER > 1.0
    base = profile_for("trametinib")
    boosted = ts.with_efflux_co_dose(base)
    assert boosted.budget_fraction > base.budget_fraction
    assert "systemic exposure raised too" in boosted.dose_limiting_event


def test_trametinib_plus_efflux_becomes_intolerable_once_charged():
    without = ts.regimen_toxicity(["trametinib"], efflux_co_dose=False)
    with_ = ts.regimen_toxicity(["trametinib"], efflux_co_dose=True)
    assert without["tolerable"] is True
    assert with_["tolerable"] is False
    assert "skin / vascular (MEK-class)" in with_["oversubscribed"]


def test_the_six_agent_stack_plus_efflux_oversubscribes_four_axes():
    r = ts.regimen_toxicity(["radiation", "anti-PD-1", "liposomal clodronate", "lomustine",
                             "trametinib", "parthenolide"], efflux_co_dose=True)
    assert r["tolerable"] is False
    assert len(r["oversubscribed"]) == 4


def test_the_headline_number_barely_survives_derating():
    d = ts.derated_kill("trametinib")
    assert d["raw"] == ts.TOXICITY_TAKES_BACK_THE_EFFLUX_ROUTE["trametinib + efflux, no charge"]
    assert d["derated"] == ts.TOXICITY_TAKES_BACK_THE_EFFLUX_ROUTE["trametinib + efflux, DE-RATED"]
    assert d["beats_growth"] is True
    assert d["margin"] < 0.002, "a rounding error, not a therapy"


def test_the_verdict_calls_the_thin_margin_what_it_is():
    v = ts.TOXICITY_TAKES_BACK_THE_EFFLUX_ROUTE["VERDICT"]
    assert "is not a therapy" in v
    assert "rounding error" in v


# --- what survives -----------------------------------------------------------------------------------

def test_parthenolide_plus_efflux_is_the_one_that_stays_tolerable():
    assert ts.regimen_toxicity(["parthenolide"], efflux_co_dose=True)["tolerable"] is True
    assert ts.regimen_toxicity(["trametinib"], efflux_co_dose=True)["tolerable"] is False


def test_parthenolide_sits_on_an_axis_nothing_else_it_pairs_with_uses():
    part = profile_for("parthenolide")
    assert part.axis is Organ.GI
    for other in ("trametinib", "lomustine", "radiation", "liposomal clodronate", "anti-PD-1"):
        assert profile_for(other).axis is not Organ.GI, other


def test_two_independent_constraints_select_the_same_agent():
    joined = " ".join(ts.WHAT_SURVIVES_AND_WHY_IT_IS_THE_SAME_AGENT)
    assert "SECOND, INDEPENDENT argument" in joined
    assert "TWO DIFFERENT CONSTRAINTS SELECTING THE SAME AGENT" in joined


# --- the honest limits ---------------------------------------------------------------------------------

def test_the_budgets_are_flagged_as_assumed():
    joined = " ".join(ts.WHAT_THIS_DOES_NOT_FIX)
    assert "ASSUMED" in joined
    assert "NO TIME DIMENSION" in joined
    unmeasured = [n for n, p in PROFILES.items() if not p.measured_in_dogs]
    assert len(unmeasured) >= 5, "most of these have no canine toxicity data"


def test_the_lesson_about_the_refactor_is_recorded():
    joined = " ".join(ts.THE_LESSON_ABOUT_THE_REFACTOR)
    assert "REPRODUCED THE LOSS" in joined
    assert "left as PROSE while coverage was made structural" in joined
    assert "what you already knew and had stopped thinking about" in joined


def test_the_lookup_now_raises_rather_than_failing_open():
    import pytest
    from canine_dsp.core.toxicity import profile_for as pf
    with pytest.raises(KeyError, match="fail open"):
        pf("an agent with no profile")


def test_the_lookup_bug_is_recorded_with_both_the_wrong_and_right_figures():
    joined = " ".join(ts.THE_LOOKUP_BUG_THAT_FAILED_OPEN)
    assert "FAILS OPEN IS WORSE" in joined
    assert "+1.00" in joined and "+0.12" in joined


def test_the_tolerable_survivor_is_three_agents_and_still_does_not_close():
    s = ts.TOLERABLE_SURVIVOR
    assert s["escapes_closed"] < s["escapes_total"]
    assert s["margin_on_those_closed"] < 0.006
    assert set(s["still_open"]) == {"NF-kB-independence", "drug-tolerant persister"}
    assert "still does not close" in s["VERDICT"]


def test_the_survivor_regimen_really_is_tolerable_in_the_model():
    r = ts.regimen_toxicity(["parthenolide", "liposomal clodronate", "radiation"],
                            efflux_co_dose=True)
    assert r["tolerable"] is True
    assert r["headroom"] == ts.TOLERABLE_SURVIVOR["headroom"]
    assert r["derating"] == {}
