"""Rule 13: search the program from exists-today agents first, and report a to-build program as such.

These tests exist because the lapse they guard against was invisible: every agent in
`core.microtubule_route.build()` carries `obtainable=True`, so a program resting on a preclinical
compound read as a program a vet could dispense. Nothing in the suite caught it.
"""

import pytest

from canine_dsp import availability_tiers as at
from canine_dsp import pkpd as pk
from canine_dsp.candidate_universe import Availability
from canine_dsp.core import catalogue as cat


def test_every_program_component_is_tiered():
    """An untiered agent is the lapse rule 13 names, so there is no default."""
    for a in at.PROGRAM:
        assert a.availability in set(Availability), a.name
        assert len(a.basis) > 40, a.name


def test_the_program_contains_both_tiers():
    assert at.exists_today()
    assert at.to_build()
    assert len(at.exists_today()) + len(at.to_build()) == len(at.PROGRAM)


def test_the_induction_agent_is_to_build_and_is_not_pretended_otherwise():
    """RGN3067 is preclinical and rodent-only. The report called the regimen obtainable."""
    rgn = next(a for a in at.PROGRAM if "RGN3067" in a.name)
    assert rgn.availability is Availability.TO_BUILD
    assert "preclinical" in rgn.basis.lower()


def test_the_optimistic_obtainable_flag_is_reported_not_hidden():
    """The lint for the actual defect: agents flagged obtainable in the regimen that are to-build."""
    mislabelled = at.mislabelled_as_obtainable()
    assert mislabelled, "if this is empty the flag was silently changed instead of reported"
    assert "brain-penetrant microtubule agent" in mislabelled


def test_every_to_build_agent_names_its_substitute_or_says_there_is_none():
    for a in at.to_build():
        assert a.exists_today_substitute, a.name
        assert a.properties_used, a.name


def test_load_bearing_is_decided_from_fields_not_from_prose():
    """Reading it out of the prose miscounted paxalisib, which duvelisib partly substitutes for."""
    unc = at.uncovered_properties()
    assert unc["paxalisib"] == ["access"], "duvelisib covers the potency, not the access"
    # Ribociclib's measured Gd-non-enhancing concentrations substitute for RGN3067's ACCESS and
    # DUTY. What no licensed agent substitutes for is its non-division-gated kill.
    assert unc["RGN3067"] == ["position-independent kill"]
    assert "access" not in unc["RGN3067"]
    assert "duty" not in unc["RGN3067"]


def test_abemaciclib_is_scored_on_its_own_numbers_not_the_generic_access():
    """Using the generic 0.021 (chlorambucil's figure) would flatter abemaciclib about fivefold."""
    own = at.abemaciclib_by_site()
    generic = pk.PARAMS["abemaciclib"].kill_rate_at(cat.SMALL_MOLECULE_ACCESS[cat.PARENCHYMA])
    mouse = own[f"{cat.PARENCHYMA} (mouse Kp,uu 0.03)"]["kill_per_day"]
    rat = own[f"{cat.PARENCHYMA} (rat Kp,uu 0.11)"]["kill_per_day"]
    assert mouse < rat < generic, "the agent's own measured range must be the less flattering one"


def test_the_invading_edge_is_marginal_on_the_agents_own_measured_range():
    """The honest result: closes at the rat ratio, fails at the mouse ratio. Not one or the other."""
    own = at.abemaciclib_by_site()
    assert not own[f"{cat.PARENCHYMA} (mouse Kp,uu 0.03)"]["closes"]
    assert own[f"{cat.PARENCHYMA} (rat Kp,uu 0.11)"]["closes"]


def test_the_extra_axial_bulk_closes_with_licensed_agents():
    """This tumour is extra-axial in 23/23 dogs, so this is the compartment it is actually based in."""
    bulk = at.abemaciclib_by_site()[at.EXTRA_AXIAL]
    assert bulk["closes"]
    assert bulk["margin"] > 0.5
    assert "MEASURED" in bulk["provenance"]


def test_program_a_closes_access_at_every_site_with_licensed_agents():
    """The ribociclib finding: all three occupied sites close, no procedure, licensed agents only."""
    a = at.program_a()
    assert a["closes_everywhere"] is True
    assert a["sites_not_closed"] == []
    for site in (at.EXTRA_AXIAL, cat.LEPTOMENINGEAL, cat.PARENCHYMA):
        assert site in a["sites_closed"], site


def test_program_a_does_not_overstate_that_into_full_closure():
    """CLAUDE.md failure 4: closing ACCESS everywhere is not closing every ESCAPE everywhere.

    CDK4/6 inhibition is division-gated, so the drug-tolerant persister at the invading edge is held
    by schedule rather than by a second kill mechanism. The verdict must say so in the same breath
    as the good news, or it is the same overstatement the project has been corrected for before.
    """
    v = at.program_a()["verdict"]
    assert "ACCESS CLOSES" in v
    assert "NOT CLOSED" in v
    assert "persister" in v
    assert "division-gated" in v
    assert at.program_a()["persister_cover"].startswith("PARTIAL")


def test_the_persister_at_the_invading_edge_has_no_exists_today_kill():
    """The honest residual, stated as a computation over the candidate list rather than a claim."""
    cover = at.persister_cover_at_the_invading_edge()
    # DMAPT is the agent measured in canine HS for this job, and it is to-build.
    assert "parthenolide / DMAPT (NF-kB)" in cover["not_division_gated_and_reaches_the_site"]
    assert "parthenolide / DMAPT (NF-kB)" not in cover["of_those_that_exist_today"]
    assert cover["of_those_that_exist_today"] == ["hydroxychloroquine"]


def test_the_parallel_pathway_residual_is_a_measured_negative_not_a_missing_number():
    """The strongest caveat the ribociclib trials carry. Burying it would be the failure to avoid."""
    p = at.the_parallel_pathway_problem()
    assert "UNDETECTABLE" in p["measured_negative"]
    assert "PI3K/mTOR" in p["named_reroute"]
    assert p["status"].startswith("OPEN ON ACCESS")


def test_program_a_contains_no_to_build_agent():
    """If a to-build agent leaks into Program A the whole exercise is void."""
    to_build_names = {a.name for a in at.to_build()}
    assert not to_build_names & set(at.program_a()["agents"])


def test_program_b_is_reported_separately_and_as_needing_to_build_agents():
    b = at.program_b()
    assert "TO-BUILD" in b["tier"]
    assert b["load_bearing_to_build"]
    assert b["closes_at_full_measured_exposure"]
    assert all(m > 0 for m in b["worst_margins"].values())


def test_program_b_margins_match_the_live_regimen():
    """The two programs must be computed over the same machinery, or the comparison is theatre."""
    from canine_dsp.core import microtubule_route as mr

    b = at.program_b()
    p = mr.derived_potency()
    for comp, reported in b["worst_margins"].items():
        assert reported == pytest.approx(mr.worst_margin(comp, potency=p), abs=1e-4)


def test_the_gap_is_generated_from_the_fields_not_written_as_prose():
    """This function has been stale twice: 'one property' when the fields said two, then 'access at
    the invading edge' after ribociclib closed exactly that. So assert it tracks the data."""
    gap = at.the_gap()
    props = sorted({p for ps in at.uncovered_properties().values() for p in ps})
    for prop in props:
        assert prop in gap, prop
    assert f"{len(props)} PROPERTIES" in gap
    # and the thing that is no longer a gap must be named as no longer a gap
    assert "NO LONGER IN THIS LIST" in gap


def test_ribociclib_closes_the_invading_edge_at_every_measured_value():
    """The finding itself, asserted on the worst reported value rather than the mean."""
    r = pk.ribociclib_nonenhancing_range()
    assert r["closes_at_every_measured_value"]
    assert r["worst_measured_margin"] > 0
    assert r["fold_over_bar_at_worst"] > 3
    assert r["provenance"] == "measured"


def test_ribociclib_access_is_measured_in_each_compartment_not_inferred():
    """The reason this beats abemaciclib here: three measured concentrations, not three inferences."""
    by_site = pk.ribociclib_by_compartment()
    assert len(by_site) == 3
    assert all(v["closes"] for v in by_site.values())


def test_ribociclib_is_priced_on_the_toxicity_ledger():
    """An unpriced agent is not free -- and its QT burden gets a real axis, not a footnote."""
    from canine_dsp.core import toxicity as tox

    prof = tox.profile_for("ribociclib (CDK4/6)")
    assert prof.axis is tox.Organ.MARROW
    assert prof.secondary_axis is tox.Organ.CARDIAC
    assert prof.measured_in_dogs is False, "the whole profile is a human-label transfer"


def test_the_statement_reports_both_programs_and_the_counts_agree():
    s = at.statement()
    assert "PROGRAM A" in s and "PROGRAM B" in s
    assert str(len(at.exists_today())) in s
    assert str(len(at.to_build())) in s
