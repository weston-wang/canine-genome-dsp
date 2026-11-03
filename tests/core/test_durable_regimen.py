"""The published margins must come from committed code, and the toxicity gate must do the deciding."""

from __future__ import annotations

import pytest

from canine_dsp.core import durable_regimen as dr
from canine_dsp.core import toxicity as tox
from canine_dsp.core.catalogue import ESCAPES, GROWTH_PER_DAY, LEPTOMENINGEAL, PARENCHYMA

BOTH = (PARENCHYMA, LEPTOMENINGEAL)


# --- the gate decides, not the author ---------------------------------------------------------------

def test_radiation_is_rejected_by_the_gate_not_removed_by_hand():
    """It must be OFFERED and then rejected. A hand-curated list proves nothing."""
    offered = [a.name for a in dr.candidates(PARENCHYMA)]
    assert "radiation" in offered
    assert dr.toxicity_rejects(dr.candidates(PARENCHYMA)) == ("radiation",)
    assert "radiation" not in [a.name for a in dr.build(PARENCHYMA).agents]


def test_radiation_is_rejected_because_of_the_shared_seizure_axis():
    """Before Organ.SEIZURE existed the two sat on different axes and could never add."""
    kept = [a.name for a in dr.build(PARENCHYMA).agents] + [dr.PROCEDURE]
    with_rad = [tox.PROFILES[n] for n in kept + ["radiation"]]
    over = tox.oversubscribed(with_rad)
    assert tox.Organ.SEIZURE in over
    assert over[tox.Organ.SEIZURE] == pytest.approx(1.15, abs=1e-9)
    assert tox.tolerable([tox.PROFILES[n] for n in kept])


def test_both_colliding_components_actually_load_the_seizure_axis():
    """The collision has to be in the arithmetic, not in a prose `source` string."""
    for name in ("radiation", dr.PROCEDURE):
        assert tox.Organ.SEIZURE in tox.PROFILES[name].load()


def test_the_procedure_is_never_dropped():
    """It carries no kill, so a naive gate would drop it first -- and it is the whole result."""
    assert dr.PROCEDURE not in dr.toxicity_rejects(dr.candidates(PARENCHYMA))


# --- the answer -------------------------------------------------------------------------------------

@pytest.mark.parametrize("compartment", BOTH)
def test_every_escape_is_closed_at_the_assumed_growth_rate(compartment):
    m = dr.margins(compartment)
    assert len(m) == len(ESCAPES)
    assert all(v > 0 for v in m.values()), {k: v for k, v in m.items() if v <= 0}


def test_the_published_margins_are_reproduced_exactly():
    """These are the figures in docs/PLAIN_LANGUAGE_REPORT.md. They must be re-derivable."""
    assert dr.worst_margin(PARENCHYMA) == pytest.approx(0.0556, abs=5e-5)
    assert dr.worst_margin(LEPTOMENINGEAL) == pytest.approx(0.0732, abs=5e-5)


def test_the_weakest_escape_is_autophagy_independence_at_both_sites():
    for compartment in BOTH:
        m = dr.margins(compartment)
        assert min(m, key=m.get) == "autophagy-independence"


def test_the_parenchyma_is_the_tighter_compartment():
    assert dr.worst_margin(PARENCHYMA) < dr.worst_margin(LEPTOMENINGEAL)


# --- where it breaks --------------------------------------------------------------------------------

def test_it_holds_at_a_seven_day_doubling():
    assert dr.closes(0.693 / 7)


def test_BOTH_compartments_reopen_at_a_five_day_doubling():
    """The report said only the brain-tissue site reopened. Both do."""
    assert not dr.closes(0.693 / 5)
    assert dr.worst_margin(PARENCHYMA, 0.693 / 5) < 0
    assert dr.worst_margin(LEPTOMENINGEAL, 0.693 / 5) < 0


@pytest.mark.parametrize("doubling,expected", sorted(dr.BY_DOUBLING_TIME.items()))
def test_the_sensitivity_table_is_not_transcribed(doubling, expected):
    growth = 0.693 / doubling
    assert dr.worst_margin(PARENCHYMA, growth) == pytest.approx(expected[0], abs=5e-4)
    assert dr.worst_margin(LEPTOMENINGEAL, growth) == pytest.approx(expected[1], abs=5e-4)


def test_the_assumed_growth_rate_sits_between_the_closing_and_failing_cases():
    assert 0.693 / 7 > GROWTH_PER_DAY > 0.693 / 20


# --- the constraint that actually binds -------------------------------------------------------------

def test_the_marrow_axis_has_zero_headroom():
    """The report claimed 'roughly a third of the total budget unspent'. It is pinned at 1.00."""
    assert dr.headroom() == pytest.approx(0.0, abs=1e-9)
    assert dr.organ_loads()["myelosuppression"] == pytest.approx(1.00, abs=1e-9)


def test_the_marrow_load_is_carried_by_exactly_two_agents():
    assert tox.PROFILES["temozolomide"].axis is tox.Organ.MARROW
    assert tox.PROFILES["hydroxychloroquine (autophagy)"].axis is tox.Organ.MARROW
    assert (tox.PROFILES["temozolomide"].budget_fraction
            + tox.PROFILES["hydroxychloroquine (autophagy)"].budget_fraction
            == pytest.approx(1.00, abs=1e-9))


def test_the_regimen_is_tolerable_on_every_axis():
    names = [a.name for a in dr.build(PARENCHYMA).agents] + [dr.PROCEDURE]
    assert tox.tolerable([tox.PROFILES[n] for n in names])


# --- the single point of failure --------------------------------------------------------------------
#
# These tests exist because the published report claimed "Five components. Each is there because it
# closes something nothing else in the list closes." THAT IS FALSE, and the tests below are what
# falsified it.

def test_only_temozolomide_is_load_bearing():
    """Drop any other agent and all ten escapes still close. Drop temozolomide and everything opens."""
    assert dr.load_bearing(PARENCHYMA) == ("temozolomide",)
    assert dr.load_bearing(LEPTOMENINGEAL) == ("temozolomide",)


def test_temozolomide_alone_closes_every_escape_at_both_sites():
    """The other four agents are not what makes the result work."""
    for compartment in BOTH:
        assert dr.worst_margin_for_subset(compartment, ("temozolomide",)) == pytest.approx(
            0.0550, abs=5e-5)


def test_the_other_four_agents_buy_almost_nothing_in_the_parenchyma():
    """+0.0006 on a margin of +0.0556 -- roughly one percent of the result."""
    solo = dr.worst_margin_for_subset(PARENCHYMA, ("temozolomide",))
    assert dr.worst_margin(PARENCHYMA) - solo == pytest.approx(0.0006, abs=1e-4)


def test_anti_pd1_contributes_a_negligible_but_nonzero_amount():
    """0.00002/day in the parenchyma -- more than three orders of magnitude below the growth rate it
    is meant to help beat, for 30% of an organ axis.

    NOT exactly zero. An earlier readout of these margins showed the anti-PD-1 rows as unchanged and
    was read as 'contributes literally nothing'; that was a ROUNDING ARTEFACT at four decimal places,
    not a property of the agent. The distinction matters because 'exactly zero' would imply a
    coverage bug, whereas this is just an antibody failing to cross.
    """
    for compartment, expected in ((PARENCHYMA, 0.00002), (LEPTOMENINGEAL, 0.00020)):
        agent = next(a for a in dr.build(compartment).agents if a.name == "anti-PD-1 (gilvetmab)")
        assert agent.effective_kill == pytest.approx(expected, abs=1e-6)
        assert 0.0 < agent.effective_kill < GROWTH_PER_DAY / 100
    assert tox.PROFILES["anti-PD-1 (gilvetmab)"].budget_fraction == 0.30


def test_the_whole_result_rests_on_the_delivery_gain():
    """Strip the osmotic gain and temozolomide falls below the growth rate. Access IS the answer."""
    import canine_dsp.core.intraarterial_route as ia
    unassisted = dr.REFERENCE_POTENCY * ia.TEMOZOLOMIDE_CSF_PLASMA
    assert unassisted < GROWTH_PER_DAY
    assert dr.REFERENCE_POTENCY * ia.TEMOZOLOMIDE_CSF_PLASMA * ia.CONSERVATIVE_GAIN > GROWTH_PER_DAY


WITHOUT_HCQ = ("liposomal clodronate", "anti-PD-1 (gilvetmab)", "temozolomide", "paxalisib")


def test_dropping_hydroxychloroquine_costs_almost_nothing_at_the_binding_escape():
    """It carries 45% of the axis that binds, and cannot help the escape that binds it.

    The cost is not exactly zero: with hydroxychloroquine gone the WEAKEST LINK MOVES from
    autophagy-independence to antigen loss, because hydroxychloroquine did cover antigen loss. The
    difference is 0.00002/day in the parenchyma -- the same order as anti-PD-1's entire
    contribution.
    """
    for compartment, cost in ((PARENCHYMA, 0.00002), (LEPTOMENINGEAL, 0.00021)):
        delta = dr.worst_margin(compartment) - dr.worst_margin_for_subset(compartment, WITHOUT_HCQ)
        assert delta == pytest.approx(cost, abs=1e-5)
        assert delta < GROWTH_PER_DAY / 100


def test_dropping_hydroxychloroquine_moves_the_weakest_link_rather_than_opening_one():
    for compartment in BOTH:
        assert dr.worst_margin_for_subset(compartment, WITHOUT_HCQ) > 0


def test_dropping_hydroxychloroquine_returns_most_of_the_headroom():
    profiles = [tox.PROFILES[n] for n in WITHOUT_HCQ + (dr.PROCEDURE,)]
    assert dr.headroom() == pytest.approx(0.0, abs=1e-9)
    assert tox.headroom(profiles) == pytest.approx(0.40, abs=1e-9)


def test_hydroxychloroquine_structurally_cannot_cover_the_binding_escape():
    """Not a dosing accident -- `covers` refuses an agent against an escape on its own axis."""
    from canine_dsp.core.regimen import Axis
    hcq = next(a for a in dr.build(PARENCHYMA).agents
               if a.name == "hydroxychloroquine (autophagy)")
    binding = next(e for e in ESCAPES if e.name == "autophagy-independence")
    assert hcq.axis is Axis.AUTOPHAGY and binding.axis is Axis.AUTOPHAGY
    assert not hcq.covers(binding)


def test_the_single_point_of_failure_is_recorded_in_the_module():
    """The previous regimen was rejected for having one. This one has one too."""
    assert "temozolomide" in dr.THE_SINGLE_POINT_OF_FAILURE["what_it_is"].lower()
    assert dr.THE_SINGLE_POINT_OF_FAILURE["the_report_was_wrong"]


def test_the_regimen_is_obtainable():
    assert dr.build(PARENCHYMA).obtainable


def test_every_agent_carries_a_toxicity_profile():
    """An agent with no profile would be silently free, which is how toxicity got ignored before."""
    for compartment in BOTH:
        for agent in dr.build(compartment).agents:
            assert agent.name in tox.PROFILES
