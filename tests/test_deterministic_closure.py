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
    # C8 became MET once the user clarified that near-future agents count toward closure.
    assert outstanding == {"C5", "C7"}
    # neither is engineering: a per-tumour test and sponsor access
    for c in dc.failing_conditions():
        assert c.status in (dc.Status.GATE, dc.Status.SPONSOR)


def test_c8_records_the_availability_lapse_rather_than_quietly_fixing_the_flag():
    """Rule 13. The margins are real; what was wrong was the implied availability, so it is named."""
    from canine_dsp import availability_tiers as at

    c8 = next(c for c in dc.CONDITIONS if c.tag == "C8")
    assert c8.status is dc.Status.MET
    assert "MIS-SCOPED TWICE BY ME, IN OPPOSITE DIRECTIONS" in c8.why_required
    assert "STRICTER bar than the user set" in c8.why_required
    assert "theoretical" in c8.requirement
    mix = at.tier_mix()
    assert mix["theoretical_agents_used"] == []
    assert mix["all_near_future_pass_the_three_part_test"]
    assert at.mislabelled_as_obtainable(), "C8's premise is that the flag is still optimistic"
    # C8 narrowed once ribociclib closed the access half of it: it is now about MECHANISMS, and the
    # requirement must say that access at the invading edge is no longer part of it.
    # C8 narrowed twice: access at the invading edge, the non-division-gated kill and the genotype
    # anchor have each since closed on a licensed drug, so what it gates is three QUANTITIES.
    assert at.program_a()["closes_everywhere"], "C8's scope rests on Programme A closing access"
    led = at.program_a_route_ledger()
    assert led["open"] == [], "C8 must not be hiding an open route"


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


# --- the goal, graded against the user's verbatim criteria (rule 2) --------------------------------

def test_the_criteria_are_quoted_verbatim_not_paraphrased():
    """Rule 2. The bar drifted in my own reporting three times; pinning the words stops that."""
    joined = " ".join(dc.CRITERIA)
    for phrase in ("every mechanism and every escape",
                   "10+ years of durability",
                   "I'm not asking if it's been demonstrated",
                   "I'm okay with no specific data but if scientifically sound",
                   "I don't want odds"):
        assert phrase in joined, phrase


def test_the_goal_verdict_grades_every_criterion():
    v = dc.goal_verdict()
    for term in ("every_mechanism_and_escape_closed", "by_real_data_or_rigorous_model",
                 "potency_and_toxicity_both_considered", "not_odds_but_a_conjunction"):
        assert term in v, term
    assert v["by_real_data_or_rigorous_model"]["inputs_failing_the_bar"] == []


def test_absence_of_canine_demonstration_is_not_graded_as_a_failure():
    """Rule 11 / failure 7: the user disclaimed this bar twice, so it must not reappear as a gap."""
    v = dc.goal_verdict()
    assert v["demonstration_not_required"]["verdict"].startswith("N/A")


def test_the_verdict_separates_the_two_tiers_rather_than_collapsing_them():
    """Rule 13: a programme needing a to-build agent is reported separately and as such."""
    e = dc.goal_verdict()["every_mechanism_and_escape_closed"]
    assert e["full_programme"]["verdict"] == "MET"
    assert "WEAKER" in e["licensed_only_programme"]["verdict"]


def test_the_one_unquantified_quantity_is_named_not_buried():
    """Overstating closure is failure 4. The verdict must name what it cannot compute."""
    v = dc.goal_verdict()
    q = v["the_licensed_only_variant_retained_as_information"]
    assert "NOT because it is the bar" in q
    assert "cytostatic" in q
    assert "HONEST QUALIFICATION REMAINS" in v["verdict"]


def test_nothing_theoretical_counts_toward_the_closure():
    """Rule 13 after the clarification: near-future counts, theoretical never does."""
    t = dc.goal_verdict()["agent_tiers"]
    assert t["theoretical_agents_used"] == []
    assert t["all_near_future_pass_the_three_part_test"]
    assert t["mix"]["NEAR_FUTURE"] > 0, "if 0, the tier split would be decorative"


def test_the_near_future_clarification_is_quoted_verbatim():
    joined = " ".join(dc.CRITERIA)
    assert "near future ones" in joined
    assert "nothing that's pure theoretical" in joined


def test_strengthening_items_are_not_relabelled_as_open_gaps():
    """Rule 11: a transferred or structurally-closed item is not open. But it must still be listed
    as something that would strengthen the result, or the report hides its own soft spots."""
    v = dc.goal_verdict()
    assert len(v["what_would_strengthen_it_rather_than_what_is_open"]) == 3
