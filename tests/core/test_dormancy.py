"""The persister is a duty-cycle problem before it is a mechanism problem."""

from __future__ import annotations

from canine_dsp.core import dormancy
from canine_dsp.core.catalogue import ESCAPES, GROWTH_PER_DAY, PARENCHYMA, agents_in
from canine_dsp.core.dormancy import CYCLING_FRACTION_SWEEP, DormancyModel
from canine_dsp.core.regimen import Regimen

PERS = next(e for e in ESCAPES if "persister" in e.name)


def test_a_dormant_cell_does_not_grow_at_the_dividing_population_rate():
    d = DormancyModel(0.20)
    assert d.effective_growth(GROWTH_PER_DAY) < GROWTH_PER_DAY
    assert d.effective_growth(GROWTH_PER_DAY) == GROWTH_PER_DAY * 0.20


def test_a_continuous_division_gated_agent_reaches_persisters_at_re_entry():
    d = DormancyModel(0.20)
    continuous = next(a for a in agents_in(PARENCHYMA) if a.name == "trametinib (MEK)")
    assert continuous.division_gated and continuous.duty == 1.0
    assert d.kill_from(continuous) == continuous.effective_kill


def test_a_transient_agent_is_discounted_by_its_duty_cycle():
    d = DormancyModel(0.20)
    radiation = next(a for a in agents_in(PARENCHYMA) if a.name == "radiation")
    assert radiation.duty < 0.1
    assert d.kill_from(radiation) < radiation.effective_kill


def test_the_one_line_states_the_correction():
    assert "A DIVISION-GATED AGENT DOES NOT FAIL AGAINST PERSISTERS. A TRANSIENT ONE DOES." == \
        dormancy.THE_ERROR_THIS_CORRECTS["THE_ONE_LINE"]


def test_the_error_names_where_it_led():
    e = dormancy.THE_ERROR_THIS_CORRECTS
    assert "NEVER PRODUCED AN APPROVED THERAPY IN ANY SPECIES" in e["where_that_led"]
    assert "compares a rate to a state" in e["first_thing_wrong"]


def test_the_persister_margin_holds_across_the_cycling_sweep():
    for cf, (par, lep) in dormancy.PERSISTER_MARGIN_BY_CYCLING.items():
        if cf == 1.00:
            continue
        assert par > 0 and lep > 0, cf


def test_the_only_failing_row_is_degenerate_and_labelled_so():
    assert dormancy.PERSISTER_MARGIN_BY_CYCLING[1.00][1] < 0
    joined = " ".join(dormancy.THE_ONE_ROW_WHERE_IT_FAILS)
    assert "DEGENERATE" in joined
    assert "is not a persister pool" in joined


def test_the_correction_improves_the_worst_margin_in_the_analysis():
    joined = " ".join(dormancy.WHAT_THE_CORRECTION_BUYS)
    assert "-0.0544" in joined and "+0.0771" in joined
    assert "2.0x TO 1.7x" in joined


def test_the_answer_is_named_as_a_schedule_not_a_mechanism():
    joined = " ".join(dormancy.THE_ANSWER_IS_A_SCHEDULE)
    assert "IT IS A SCHEDULE" in joined
    assert "DUTY-CYCLE PROBLEM BEFORE IT IS A MECHANISM PROBLEM" in joined


def test_metronomic_is_obtainable_and_was_already_in_the_notes():
    m = dormancy.METRONOMIC_IS_THE_SCHEDULE_THAT_DOES_IT
    assert "ROUTINE IN VETERINARY ONCOLOGY" in m["status"]
    assert "already identified metronomic dosing" in m["AND_IT_WAS_IN_THIS_REPOSITORY_FROM_THE_START"]
    assert "not a free gain" in m["the_cost"]


def test_the_cycling_fraction_is_swept_rather_than_asserted():
    joined = " ".join(dormancy.WHAT_THIS_DOES_NOT_CLAIM)
    assert "SWEPT rather than asserted" in joined
    assert len(CYCLING_FRACTION_SWEEP) >= 4
