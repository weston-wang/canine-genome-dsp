"""Three routes past the treatment horizon, and the model's first genuinely durable outcome."""

from __future__ import annotations

import math

import pytest

from canine_dsp.core import cycled_regimen as cr
from canine_dsp.core import response_duration as rd
from canine_dsp.core import toxicity as tox
from canine_dsp.core import treatment_horizon as th
from canine_dsp.core.catalogue import GROWTH_PER_DAY, LEPTOMENINGEAL, PARENCHYMA

BOTH = (PARENCHYMA, LEPTOMENINGEAL)


# --- route 1: the kind of toxicity, not the size -----------------------------------------------------------

def test_the_neuropathy_rates_differ_by_an_order_of_magnitude():
    assert cr.LISAVANBULIN_NEUROPATHY_RATE == pytest.approx(1 / 26, abs=1e-9)
    assert cr.SAGOPILONE_NEUROPATHY_RATE / cr.LISAVANBULIN_NEUROPATHY_RATE > 10


def test_higher_access_shortens_the_continuous_course_below_the_old_horizon():
    for access, (margin, days) in cr.ROUTE_1.items():
        assert cr.margin_for(access) == pytest.approx(margin, abs=5e-4)
        assert cr.continuous_days_to_clear(access) == pytest.approx(days, abs=2)
    assert cr.ROUTE_1[1.00][1] < cr.ROUTE_1[0.80][1]


def test_route_1_is_curative_only_because_nothing_caps_the_duration():
    """316 days is still far beyond the 84-day cumulative-neuropathy window."""
    days = cr.continuous_days_to_clear(1.00)
    assert days > th.TOLERABLE_WINDOW_DAYS
    assert not th.is_curative(PARENCHYMA, window=th.TOLERABLE_WINDOW_DAYS)
    # with an acute rather than cumulative DLT, the window is not the binding constraint
    assert days < 365


def test_the_acute_versus_cumulative_distinction_is_recorded():
    joined = " ".join(cr.WHY_THE_TOXICITY_KIND_MATTERS_MORE_THAN_ITS_SIZE)
    assert "ACUTE dose-limiting toxicity caps the DOSE" in joined
    assert "CUMULATIVE one caps the DURATION" in joined


def test_route_1_loads_the_organ_the_tumour_is_in():
    """The swap is not free: a peripheral-nerve clock becomes a CNS ceiling."""
    p = tox.PROFILES["lisavanbulin (oral)"]
    assert p.axis is tox.Organ.CNS_LOCAL
    assert p.secondary_axis is tox.Organ.SEIZURE
    joined = " ".join(cr.WHAT_ROUTE_1_COSTS)
    assert "same organ the tumour is in" in joined
    assert "GRADE 4 ASEPTIC MENINGOENCEPHALITIS" in joined


def test_the_lisavanbulin_regimen_is_tolerable():
    names = ["liposomal clodronate", "hydroxychloroquine (autophagy)", "anti-PD-1 (gilvetmab)",
             "paxalisib", "lisavanbulin (oral)"]
    profiles = [tox.PROFILES[n] for n in names]
    assert tox.tolerable(profiles)
    assert tox.headroom(profiles) == pytest.approx(0.30, abs=1e-9)


def test_the_peripheral_nerve_axis_is_no_longer_loaded_by_the_cytotoxic():
    """That axis at 0.85 was the binding constraint with sagopilone."""
    loads = tox.axis_loads([tox.PROFILES["lisavanbulin (oral)"]])
    assert tox.Organ.PERIPHERAL_NERVE not in loads


# --- route 2: accepted as an assumption, and it barely helps -------------------------------------------------

def test_debulking_buys_far_less_than_it_looks_like_it_should():
    for burden, days in cr.ROUTE_2.items():
        assert cr.continuous_days_to_clear(1.00, burden=burden) == pytest.approx(days, abs=2)
    assert cr.ROUTE_2[1e9] - cr.ROUTE_2[1e7] == pytest.approx(70, abs=3)


def test_debulking_saving_is_logarithmic_in_the_burden_removed():
    """Each order of magnitude removed buys the same fixed number of days."""
    one = cr.debulk_saving(1.00, 1)
    two = cr.debulk_saving(1.00, 2)
    assert two == pytest.approx(2 * one, rel=1e-9)
    assert one == pytest.approx(math.log(10) / cr.margin_for(1.00), rel=1e-9)


def test_a_hundredfold_cytoreduction_is_about_ten_weeks():
    assert cr.debulk_saving(1.00, 2) == pytest.approx(70, abs=3)


def test_the_reason_not_to_count_on_surgery_is_recorded():
    joined = " ".join(cr.ROUTE_2_VERDICT)
    assert "burden that mattered least" in joined
    assert "NOT WRONG TO DO IT" in joined


# --- route 3: the third outcome ------------------------------------------------------------------------------

def test_a_cycle_nets_down_when_kill_exceeds_regrowth():
    c = cr.Cycle(84, cr.NEUROPATHY_RESOLUTION_DAYS)
    assert c.net_logs_per_cycle(cr.margin_for(0.80)) > 0
    assert c.net_logs_per_cycle(0.001) < 0, "a tiny margin cannot outrun the rest period"


def test_a_cycle_that_does_not_net_down_never_clears():
    c = cr.Cycle(84, 200)
    assert c.cycles_to_clear(cr.margin_for(0.80)) == float("inf")
    assert c.days_to_clear(cr.margin_for(0.80)) == float("inf")


@pytest.mark.parametrize("agent,access", [("sagopilone", 0.80), ("lisavanbulin", 1.00)])
@pytest.mark.parametrize("rest", [28, 38, 56])
def test_the_cycling_table_is_re_derived(agent, access, rest):
    cycles, years = cr.ROUTE_3[(agent, rest)]
    c = cr.Cycle(84, rest)
    m = cr.margin_for(access)
    assert c.cycles_to_clear(m) == pytest.approx(cycles, abs=0.2)
    assert c.days_to_clear(m) / 365 == pytest.approx(years, abs=0.15)


def test_cycling_is_just_a_lower_duty_sustained_indefinitely():
    for rest, expected in ((28, 0.75), (38, 0.69), (56, 0.60)):
        assert cr.Cycle(84, rest).effective_duty == pytest.approx(expected, abs=0.01)


def test_a_longer_rest_costs_years_not_weeks():
    m = cr.margin_for(0.80)
    short = cr.Cycle(84, 28).days_to_clear(m)
    long = cr.Cycle(84, 56).days_to_clear(m)
    assert long / short > 5, "the rest period enters through the regrowth term, so it compounds"


def test_lisavanbulin_cycling_is_robust_where_sagopilone_cycling_is_not():
    """At a 56-day rest, sagopilone takes 19 years and lisavanbulin 3.3."""
    assert cr.ROUTE_3[("sagopilone", 56)][1] > 15
    assert cr.ROUTE_3[("lisavanbulin", 56)][1] < 4


def test_this_is_the_third_outcome_the_model_lacked():
    joined = " ".join(cr.THE_THIRD_OUTCOME)
    assert "TWO states" in joined
    assert "THIRD STATE" in joined
    # and the module it corrects really does record only the two
    prior = " ".join(th.THE_MODEL_HAD_NO_RELAPSE_STATE)
    assert "CURE" in prior and "DEATH" in prior
    assert "NO 'RESPONDS THEN RELAPSES'" in prior


def test_cycling_beats_the_horizon_that_defeated_continuous_dosing():
    """Continuous dosing failed because 84 days is 17% of the way. Cycling never stops."""
    m = cr.margin_for(0.80)
    assert th.burden_after(th.TOLERABLE_WINDOW_DAYS, m) > 1.0
    assert cr.Cycle(84, 38).days_to_clear(m) < float("inf")


# --- the limits ------------------------------------------------------------------------------------------------

def test_the_rodent_provenance_is_flagged_and_so_is_its_direction():
    joined = " ".join(cr.WHAT_IS_STILL_ASSUMED)
    assert "RODENT" in joined
    assert "FAVOURABLE" in joined, "the species correction runs the unusual way here and must say so"


def test_the_failed_biomarker_is_recorded():
    joined = " ".join(cr.WHAT_IS_STILL_ASSUMED)
    assert "EB1 BIOMARKER FAILED" in joined
    assert "13" in joined


def test_the_growth_rate_now_enters_twice():
    joined = " ".join(cr.WHAT_IS_STILL_ASSUMED)
    assert "TWICE" in joined
    c = cr.Cycle(84, 38)
    faster = c.net_logs_per_cycle(cr.margin_for(1.00), growth=0.0990)
    slower = c.net_logs_per_cycle(cr.margin_for(1.00, growth=0.0990), growth=0.0990)
    assert slower < faster, "growth must reduce the kill margin AND increase the regrowth term"


def test_full_recovery_between_cycles_is_flagged_as_an_assumption():
    joined = " ".join(cr.WHAT_IS_STILL_ASSUMED)
    assert "FULL RECOVERY" in joined


def test_obtainability_is_better_than_first_recorded_but_still_not_veterinary():
    """The status correction runs FAVOURABLY -- rare enough here to assert explicitly."""
    joined = " ".join(cr.WHAT_IS_STILL_ASSUMED)
    assert "NOT discontinued" in joined
    assert "GLIOBLASTOMA FOUNDATION" in joined
    assert "POST-TRIAL ACCESS" in joined
    assert "NO CANINE DATA EXISTS" in joined


def test_the_human_responses_are_not_what_this_model_predicts():
    """Two durable responders, both partial. This model predicts clearance."""
    joined = " ".join(cr.WHAT_IS_STILL_ASSUMED)
    assert "DURABLE PARTIAL RESPONSES ARE NOT CLEARANCE" in joined
    assert "58%" in joined and "44%" in joined
    assert "10.2%" in joined
