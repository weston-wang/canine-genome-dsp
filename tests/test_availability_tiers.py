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


def test_the_induction_agent_is_near_future_not_pretended_obtainable_nor_called_theoretical():
    """RGN3067 is preclinical as a molecule, so it is not obtainable -- but the MODALITY is licensed
    in dogs and canine HS is measured sensitive to it, so it is not theoretical either. Rule 13
    after the user's clarification requires that middle tier to exist and to be tested, not asserted."""
    rgn = next(a for a in at.PROGRAM if "RGN3067" in a.name)
    assert rgn.availability is Availability.NEAR_FUTURE
    assert "preclinical" in rgn.basis.lower()
    t = at.near_future_test(rgn.name)
    assert t["counts_toward_closure"]
    assert t["modality_is_clinical_stage"].startswith("YES")
    assert t["stated_path_to_the_dog"].startswith("YES")
    assert t["derived_or_transferred_dose_kill"].startswith("YES")


def test_no_agent_in_the_programme_is_theoretical():
    assert at.theoretical() == []


def test_every_near_future_agent_is_tested_not_assumed():
    for a in at.near_future():
        assert a.name in at.NEAR_FUTURE_TEST, a.name
        assert at.near_future_test(a.name)["counts_toward_closure"], a.name


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
    assert unc["RGN3067"] == ["a DERIVED kill rate from a measured tumour concentration"]
    # access, duty, the non-division-gated kill and a cytocidal mechanism are all now supplied by
    # licensed agents (ribociclib, dordaviprone, niraparib). Only the derived RATE is uncovered.
    for supplied in ("access", "duty", "position-independent kill", "a cytocidal mechanism"):
        assert supplied not in unc["RGN3067"], supplied
    # and the PRMT5 arm is now wanted only for MTA-dependent selectivity: a licensed PARP inhibitor
    # anchors the MTAP half through PRMT5 inactivation, Rb-independently.
    assert unc["MTA-cooperative PRMT5 inhibitor"] == [
        "MTA-dependent selectivity for MTAP-null cells"]


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
    assert "CLOSES WITH LICENSED AGENTS" in v
    # the good news must arrive with the weaker form of closure stated in the same breath
    assert "WEAKER" in v.upper()
    assert "STRUCTURALLY" in v
    assert "Programme B" in v
    assert at.program_a()["persister_cover"].startswith("CLOSED STRUCTURALLY")


def test_the_persister_cover_is_computed_over_the_candidate_list_not_asserted():
    """The candidate list must still show its working, including what is NOT the carrier."""
    cover = at.persister_cover_at_the_invading_edge()
    # DMAPT remains the best-evidenced candidate IN THIS DISEASE, and remains to-build.
    assert "parthenolide / DMAPT (NF-kB)" in cover["not_division_gated_and_reaches_the_site"]
    assert "parthenolide / DMAPT (NF-kB)" not in cover["of_those_that_exist_today"]
    # hydroxychloroquine exists today but is cover, not kill, so it must not count as the carrier.
    assert "hydroxychloroquine" in cover["of_those_that_exist_today"]
    assert "hydroxychloroquine" not in cover[
        "licensed_agents_supplying_a_real_non_division_gated_kill"]
    # radiation reaches the site but is division-gated, so it must not count either.
    assert cover["candidates"]["radiation"]["division_gated"] is True


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


def test_the_licensed_pair_is_marrow_limited_and_that_is_reported():
    """Both licensed maintenance agents sit on the marrow axis; the collision must not be hidden."""
    from canine_dsp.core import toxicity as tox

    pair = [tox.profile_for("niraparib (PARP)"), tox.profile_for("ribociclib (CDK4/6)")]
    loads = tox.axis_loads(pair)
    assert loads[tox.Organ.MARROW] > 0.9, "the collision is the point"
    assert tox.tolerable(pair), "tight, but it must still fit or the programme is not prescribable"
    assert tox.headroom(pair) < 0.1


def test_niraparib_is_tiered_and_its_limits_are_stated():
    agent = next(a for a in at.PROGRAM if a.name == "niraparib")
    assert agent.availability is Availability.EXISTS_TODAY
    assert agent.pkpd_key is None, "no published unbound tumour concentration to derive a rate from"
    for phrase in ("CYTOCIDAL", "no canine-HS", "replication-coupled", "PRMT5"):
        assert phrase in agent.basis, phrase


# --- the licensed-only programme, route by route (rule 12 form) -----------------------------------

def test_the_route_ledger_accounts_for_every_audited_route():
    """A per-route claim over a subset of the routes is the rule-9 failure in a new costume."""
    from canine_dsp import escape_audit as ea

    led = at.program_a_route_ledger()
    assert led["routes_total"] == ea.audited_escape_count()
    assert led["accounts_for_every_audited_route"]


def test_no_route_is_left_open_in_the_licensed_programme():
    assert at.program_a_route_ledger()["open"] == []


def test_the_ledger_distinguishes_margin_from_structural_closure():
    """CLAUDE.md rule 5: 'the lesion cannot apply' is a weaker claim than 'we out-kill it', and the
    ledger must keep them apart rather than reporting 16 closures as if they were equivalent."""
    led = at.program_a_route_ledger()
    kinds = led["by_kind"]
    assert kinds["MARGIN"] >= 1 and kinds["STRUCTURAL"] >= 1
    # and the verdict must say out loud that structural closure is the weaker form
    assert "weaker form" in led["verdict"]
    assert "Programme B" in led["verdict"]


def test_every_route_names_a_carrier_and_a_basis():
    for route, (kind, carrier, basis) in at.PROGRAM_A_ROUTES.items():
        assert kind in {"MARGIN", "STRUCTURAL", "GATED", "OPEN"}, route
        assert carrier.strip(), route
        assert len(basis) > 60, route


def test_the_weakest_row_is_named_rather_than_averaged_away():
    """The PI3K row closes on a transferred access with a measured negative on the same axis."""
    led = at.program_a_route_ledger()
    assert "RTK bypass" in led["weakest_row"]
    assert at.PROGRAM_A_ROUTES["4 RTK bypass into PI3K/AKT"][0] == "MARGIN"
    assert "TRANSFERRED" in at.PROGRAM_A_ROUTES["4 RTK bypass into PI3K/AKT"][2]


def test_the_persister_route_is_carried_by_a_licensed_agent_now():
    kind, carrier, _ = at.PROGRAM_A_ROUTES["10 Drug-tolerant persister"]
    assert "dordaviprone" in carrier
    assert kind == "STRUCTURAL", "no unbound tumour concentration is published, so not MARGIN"
    cover = at.persister_cover_at_the_invading_edge()
    assert cover["licensed_agents_supplying_a_real_non_division_gated_kill"]
    assert cover["verdict"].startswith("CLOSED STRUCTURALLY")


def test_the_genotype_anchor_exists_today_for_the_cdkn2a_half():
    a = at.is_cdk46_a_genotype_anchor()
    assert a["licensed"] is True
    assert "ribociclib" in a["agents"]
    assert a["verdict"].startswith("CLOSED")
    # and the Rb caveat must be stated, not buried
    assert "RB1" in a["why_the_mtap_arm_is_still_wanted"]


def test_rb1_loss_has_a_named_rb_independent_successor():
    """A15 defeats the licensed anchor, so it needs a successor or the anchor claim is hollow."""
    kind, carrier, basis = at.PROGRAM_A_ROUTES[
        "A15 RB1 loss / CDK2-cyclin E bypass of the CDK4/6 arm"]
    # the successor is now LICENSED and also germline-matched, which it was not before
    assert "niraparib" in carrier
    assert "dordaviprone" in carrier
    assert "Rb-independent" in basis
    assert "LICENSED" in basis


def test_clpp_transfer_rests_on_the_catalytic_region_not_the_average():
    """The raw 92.65% understates it; the claim must rest on the partition and the active sites."""
    from canine_dsp import sequence_conservation as sc

    part = sc.clpp_domain_partition()
    assert part["active_sites"]["both_identical"]
    assert part["mature_ordered_57_245"]["identity_percent"] > 98
    assert part["transit_peptide_1_56_cleaved"]["n"] > part["mature_ordered_57_245"]["n"]


def test_dordaviprone_closes_structurally_and_says_why_not_by_margin():
    """Overstating a structural closure as a computed one is CLAUDE.md failure 4."""
    agent = next(a for a in at.PROGRAM if "dordaviprone" in a.name)
    assert agent.availability is Availability.EXISTS_TODAY
    assert agent.pkpd_key is None, "no unbound tumour concentration is published to derive a rate"
    for phrase in ("no canine-HS", "ONCE-WEEKLY", "CLASS-MECHANISM"):
        assert phrase in agent.basis, phrase
