"""Access earned intrinsically, not borrowed from a co-dose nobody has given a dog."""

from __future__ import annotations

import math

from canine_dsp.core import brain_native_regimen as bn
from canine_dsp.core.catalogue import ESCAPES, GROWTH_PER_DAY, LEPTOMENINGEAL, PARENCHYMA, agents_in
from canine_dsp.core.delivery import EFFLUX_INHIBITION


# --- the single point of failure is gone --------------------------------------------------------------

def test_no_agent_in_the_regimen_depends_on_an_efflux_co_dose():
    for comp in (PARENCHYMA, LEPTOMENINGEAL):
        for a in bn.build(comp, 0.35).agents:
            assert "P-gp" not in a.name and "BCRP" not in a.name, a.name


def test_the_backbone_is_entirely_obtainable():
    for comp in (PARENCHYMA, LEPTOMENINGEAL):
        assert all(a.obtainable for a in bn.backbone(comp)), comp


def test_the_efflux_route_is_not_needed_to_reach_the_threshold():
    assert EFFLUX_INHIBITION.obtainable_for_a_dog is False
    assert bn.closes(bn.ACCESS_THRESHOLD), "closes without it"


# --- the access threshold, re-derived -------------------------------------------------------------------

def test_the_access_sweep_is_reproducible():
    for access, (par, lep) in bn.ACCESS_SWEEP.items():
        assert abs(bn.worst_margin(PARENCHYMA, access) - par) < 1e-3, access
        assert abs(bn.worst_margin(LEPTOMENINGEAL, access) - lep) < 1e-3, access


def test_thirty_percent_access_is_the_threshold():
    assert bn.closes(0.30)
    assert not bn.closes(0.20)
    assert bn.ACCESS_THRESHOLD == 0.30


def test_margins_rise_monotonically_with_access():
    values = [bn.worst_margin(PARENCHYMA, a) for a in sorted(bn.ACCESS_SWEEP)]
    assert values == sorted(values)


def test_the_leptomeninges_closes_before_the_parenchyma():
    """The barrier is the harder compartment, and the model should say so."""
    for access in bn.ACCESS_SWEEP:
        assert bn.worst_margin(LEPTOMENINGEAL, access) > bn.worst_margin(PARENCHYMA, access)


# --- it degrades instead of collapsing --------------------------------------------------------------------

def test_every_row_of_the_requirement_table_closes():
    for dt, potency in bn.REQUIREMENT_BY_DOUBLING_TIME.items():
        assert bn.closes(0.35, potency, math.log(2) / dt), dt


def test_the_requirement_never_falls_as_the_tumour_speeds_up():
    rows = sorted(bn.REQUIREMENT_BY_DOUBLING_TIME.items(), reverse=True)
    potencies = [p for _, p in rows]
    assert potencies == sorted(potencies)


def test_a_lower_access_costs_more_potency_at_the_same_growth():
    for dt in bn.REQUIREMENT_AT_ACCESS_030:
        assert bn.REQUIREMENT_AT_ACCESS_030[dt] >= bn.REQUIREMENT_BY_DOUBLING_TIME[dt], dt


def test_the_asks_stay_modest_across_realistic_growth():
    for dt in (12.6, 10.0, 7.0, 5.0):
        assert bn.REQUIREMENT_BY_DOUBLING_TIME[dt] / bn.REFERENCE_POTENCY <= 2.5, dt


# --- the bug that exposed it --------------------------------------------------------------------------------

def test_antigen_direction_is_now_off_by_default():
    from canine_dsp.core.regimen import Agent, Axis, Layer
    a = Agent("x", Axis.CYTOTOXIC, Layer.RECEPTOR, 0.1, 0.1, 1.0, True)
    assert a.antigen_directed is False


def test_only_the_t_cell_agent_is_antigen_directed():
    directed = [a.name for a in agents_in(PARENCHYMA) if a.antigen_directed]
    assert directed == ["anti-PD-1 (gilvetmab)"]


def test_a_dna_damaging_agent_is_no_longer_defeated_by_antigen_loss():
    lom = next(a for a in agents_in(PARENCHYMA) if "lomustine" in a.name)
    loss = next(e for e in ESCAPES if "antigen loss" in e.name)
    assert lom.covers(loss), "chemotherapy does not care what the cell displays"


def test_the_bug_is_recorded_with_its_symptom_and_class():
    b = bn.THE_BUG_THAT_EXPOSED_IT
    assert "FLAT rows" in b["the_symptom"]
    assert "LOMUSTINE WAS BEING DEFEATED BY ANTIGEN LOSS" in b["the_cause"]
    assert "This project has now made both." in b["THE_CLASS_OF_ERROR"]


# --- what it buys, and what it still assumes ------------------------------------------------------------------

def test_the_comparison_against_the_previous_regimen_is_recorded():
    w = bn.WHAT_THIS_BUYS
    assert w["single point of failure"] == ("WAS the efflux co-dose", "NOW none")
    assert w["behaviour at faster growth"][1] == "NOW a rising potency requirement"


def test_the_access_figure_is_named_as_the_whole_result_and_unverified():
    joined = " ".join(bn.WHAT_IS_STILL_ASSUMED)
    assert "It is the whole result" in joined
    assert "fails exactly as the others did" in joined


def test_penetration_is_distinguished_from_efficacy():
    joined = " ".join(bn.WHAT_IS_STILL_ASSUMED)
    assert "BRAIN-PENETRANT IS NOT BRAIN-EFFECTIVE" in joined
    assert "BLZ945" in joined


def test_the_reframe_names_why_every_earlier_access_figure_was_bad():
    joined = " ".join(bn.THE_REFRAME)
    assert "SELECTED FOR SOMETHING ELSE" in joined
    assert "had not costed one" in joined
