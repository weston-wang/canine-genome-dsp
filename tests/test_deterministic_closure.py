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


def test_delivery_is_the_binding_constraint_not_drug_discovery():
    """If swapping the route of administration closes everything, the gap is engineering."""
    blockers = dc.blocking_conditions()
    assert [c.tag for c in blockers] == ["C1", "C2"]
    for c in blockers:
        assert c.status is dc.Status.ENGINEERING


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
