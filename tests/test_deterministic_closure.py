"""The headline must be a decidable conjunction, not a probability."""

from canine_dsp import deterministic_closure as dc
from canine_dsp.core import catalogue as cat


def test_the_verdict_contains_no_probability():
    """The whole point: enumerating every route converts odds into a checklist."""
    v = dc.verdict()
    flat = repr(v).lower()
    for banned in ("p_median", "probab", "90% ci", "percentile"):
        assert banned not in flat, banned


def test_without_local_delivery_every_route_is_open_at_both_brain_sites():
    """The hard deterministic fact the probability was smearing: not 'unlikely', OPEN."""
    for comp in cat.COMPARTMENTS:
        led = dc.margin_ledger(comp, obtainable_only=True, local_delivery=False)
        assert led["closed"] == 0, comp
        assert led["worst_margin"] < 0, comp


def test_with_local_delivery_every_route_closes_on_obtainable_agents():
    """And the fix is delivery, not a new drug -- same agents, different route of administration."""
    for comp in cat.COMPARTMENTS:
        led = dc.margin_ledger(comp, obtainable_only=True, local_delivery=True)
        assert led["open"] == [], (comp, led["open"])
        assert led["worst_margin"] > 0, comp


def test_no_engineering_condition_remains():
    """This test previously asserted that C1 and C2 were engineering blockers -- i.e. that surgical
    local delivery was required. That was wrong twice over: it set access AND duty to 1.0 at once
    (the defect core.schedule_coherence exists to catch), and it overstated the requirement, which
    is access 0.196 rather than 1.0. Measured intrinsic penetration meets it orally, so nothing here
    is an engineering blocker. See delivery_answer.

    C8 was added later, under CLAUDE.md rule 13: the agents C1 and C4 depend on are not obtainable
    for a dog, which `core.microtubule_route.build()` had hidden behind `obtainable=True`. It is
    outstanding but it is NOT engineering either -- it is veterinary availability of compounds that
    already exist, and availability_tiers.program_a() reports what the obtainable program closes
    without them."""
    assert dc.blocking_conditions() == []
    outstanding = {c.tag for c in dc.failing_conditions()}
    assert outstanding == {"C5", "C7", "C8"}
    # none is engineering: a per-tumour test, sponsor access, and veterinary availability
    for c in dc.failing_conditions():
        assert c.status in (dc.Status.GATE, dc.Status.SPONSOR, dc.Status.TO_BUILD)


def test_c8_records_the_availability_lapse_rather_than_quietly_fixing_the_flag():
    """Rule 13. The margins are real; what was wrong was the implied availability, so it is named."""
    from canine_dsp import availability_tiers as at

    c8 = next(c for c in dc.CONDITIONS if c.tag == "C8")
    assert c8.status is dc.Status.TO_BUILD
    assert at.mislabelled_as_obtainable(), "C8's premise is that the flag is still optimistic"
    assert "chemistry" in c8.what_would_establish_it.lower()


def test_access_is_closed_by_molecules_rather_than_a_procedure():
    """The positive form of the same claim, cross-checked against the delivery module."""
    from canine_dsp import delivery_answer as da

    c = da.closes_with_molecular_selection()
    assert c["tolerable"] is True
    assert all(c[comp]["all_routes_closed"] for comp in cat.COMPARTMENTS)


def test_every_condition_states_what_opens_if_it_fails():
    """A condition with no consequence is decoration, not a term in a conjunction."""
    for c in dc.CONDITIONS:
        assert len(c.why_required) > 60, c.tag
        assert len(c.what_would_establish_it) > 30, c.tag


def test_access_shortfall_is_quantified_per_compartment():
    s = dc.access_shortfall()
    for comp in cat.COMPARTMENTS:
        assert s[comp]["fold_short"] > 1.0
        assert s[comp]["growth_bar"] == cat.GROWTH_PER_DAY


def test_the_probabilistic_module_is_explicitly_demoted():
    """So a later thread cannot quote P(10-year) as the verdict again."""
    s = dc.emergence_is_secondary()
    assert "not the result" in s.lower()
    assert "double-count" in s.lower()


def test_route_inventory_matches_the_independent_audit():
    r = dc.route_count()
    assert r["routes_after_independent_audit"] > r["routes_in_disease_enumeration"]
