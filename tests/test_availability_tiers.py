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
    assert set(unc["RGN3067"]) == {"access", "duty"}


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


def test_program_a_does_not_claim_to_close_everywhere():
    """Overstating closure is CLAUDE.md failure 4. Program A closes 2 of 3 sites, and says so."""
    a = at.program_a()
    assert a["closes_everywhere"] is False
    assert cat.PARENCHYMA in a["sites_not_closed"]
    assert at.EXTRA_AXIAL in a["sites_closed"]
    assert cat.LEPTOMENINGEAL in a["sites_closed"]
    assert a["verdict"].startswith("PARTIAL")


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


def test_the_gap_is_stated_from_the_computation():
    """An earlier draft asserted 'one property'; the field data says two, on different agents."""
    gap = at.the_gap()
    for prop in ("access", "duty", "genotype anchoring"):
        assert prop in gap, prop
    assert "TWO PROPERTIES" in gap


def test_the_statement_reports_both_programs_and_the_counts_agree():
    s = at.statement()
    assert "PROGRAM A" in s and "PROGRAM B" in s
    assert str(len(at.exists_today())) in s
    assert str(len(at.to_build())) in s
