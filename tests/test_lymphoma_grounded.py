"""Tests for the potency / toxicity / provenance / dormancy layer that was ported or adapted from the
histiocytic-sarcoma branch. Deterministic and fast -- no Monte Carlo."""
import math

import pytest

from canine_dsp.core import lymphoma_dormancy as D
from canine_dsp.core.lymphoma_catalogue import CNS, ESCAPES, GROWTH_PER_DAY, SYSTEMIC, agents_for
from canine_dsp.core.regimen import Agent, Axis, Layer

PERSISTER = next(e for e in ESCAPES if not e.requires_division)


def _exact_pool_growth(g, k_nd, k_dg_awake, f, switch_scale):
    """Exact dominant eigenvalue of the two-state pool (awake C, dormant D), 2x2 closed form.
    awake: grows g, killed k_nd + k_dg_awake; dormant: killed k_nd; C->D at b, D->C at a; f = a/(a+b)."""
    b = switch_scale * g
    a = b * f / (1.0 - f) if f < 1.0 else 1e9
    m11, m12, m21, m22 = g - k_nd - k_dg_awake - b, a, b, -k_nd - a
    tr, det = m11 + m22, m11 * m22 - m12 * m21
    disc = tr * tr / 4.0 - det
    return tr / 2.0 + math.sqrt(disc) if disc >= 0 else tr / 2.0


# ---------- dormancy: the adapted persister model ----------

def test_old_wall_model_is_the_f1_r1_corner():
    """The previous lymphoma persister model (division-gated agents contribute nothing; bar = full
    growth) is contained as a special case, so the rebuild replaces nothing silently."""
    pool = agents_for(SYSTEMIC, "B", obtainable_only=True)
    for combo in (pool[:3], pool[3:8], pool):
        wall = sum(a.effective_kill for a in combo if a.covers(PERSISTER) and not a.division_gated)
        assert D.persister_margin(combo, PERSISTER, GROWTH_PER_DAY, f=1.0, r=1.0) == pytest.approx(
            wall - GROWTH_PER_DAY)


def test_division_gated_agents_count_f_times_not_full_strength():
    """The point of departure from the HS formula. One division-gated agent, kill 0.05/day."""
    dg = Agent("dg", Axis.CYTOTOXIC, Layer.RECEPTOR, 0.05, 1.0, 1.0, True)
    g, f = GROWTH_PER_DAY, 0.2
    growth = D.pool_growth_fast([dg], PERSISTER, g, f, r=0.0)
    assert growth == pytest.approx(f * g - f * 0.05)
    assert growth > 0                      # still growing
    # the HS-style margin says this closes; that is the discrepancy
    assert D.hs_style_margin([dg], PERSISTER, g, f) > 0


@pytest.mark.parametrize("f", [0.05, 0.2, 0.5])
@pytest.mark.parametrize("k_nd,k_dg", [(0.0, 0.05), (0.02, 0.0), (0.02, 0.05), (0.0, 0.095), (0.05, 0.05)])
def test_module_matches_the_independent_eigenvalue_and_worst_case_bounds_the_sweep(f, k_nd, k_dg):
    g = GROWTH_PER_DAY
    nd = Agent("nd", Axis.APOPTOSIS, Layer.RECEPTOR, k_nd, 1.0, 1.0, True, division_gated=False) if k_nd else None
    dg = Agent("dg", Axis.CYTOTOXIC, Layer.RECEPTOR, k_dg, 1.0, 1.0, True) if k_dg else None
    agents = [a for a in (nd, dg) if a is not None]
    worst = D.pool_growth_worst(agents, PERSISTER, g, f, r=0.0)
    for b in D.SWITCH_RATE_SWEEP:
        mine = D.pool_growth_exact(agents, PERSISTER, g, f, 0.0, b)
        assert mine == pytest.approx(_exact_pool_growth(g, k_nd, k_dg, f, b / g), abs=1e-9)
        assert mine <= worst + 1e-12


def test_division_gated_only_regimen_can_close_but_only_very_slowly():
    """The finding that overturned my first bound: with slow switching and no non-division-gated
    agent the dormant reservoir drains only as fast as cells wake."""
    dg = Agent("dg", Axis.CYTOTOXIC, Layer.RECEPTOR, 0.095, 1.0, 1.0, True)   # kill just above growth
    margin = D.persister_margin([dg], PERSISTER, GROWTH_PER_DAY, f=0.2, r=0.0)
    assert 0.0 < margin < 0.003             # closes, but a decline of <0.3%/day
    assert math.log(10) / margin > 800      # ~10 cells take more than two years to clear


def test_fast_limit_matches_exact_eigenvalue_when_switching_is_fast():
    g, f = GROWTH_PER_DAY, 0.2
    for k_nd, k_dg in ((0.0, 0.05), (0.02, 0.05), (0.05, 0.0)):
        fast = f * g - k_nd - f * k_dg
        assert _exact_pool_growth(g, k_nd, k_dg, f, 500.0) == pytest.approx(fast, abs=5e-4)


def test_threshold_cycling_fraction_is_where_the_sign_flips():
    nd = Agent("nd", Axis.APOPTOSIS, Layer.RECEPTOR, 0.0776, 1.0, 1.0, True, division_gated=False)
    sweep = D.DormancySweep((nd,), PERSISTER, GROWTH_PER_DAY)
    f_star = sweep.threshold_cycling_fraction(r=0.0)
    assert f_star == pytest.approx(0.0776 / GROWTH_PER_DAY)
    assert D.pool_growth_fast([nd], PERSISTER, GROWTH_PER_DAY, f_star * 0.99, 0.0) < 0
    assert D.pool_growth_fast([nd], PERSISTER, GROWTH_PER_DAY, min(1.0, f_star * 1.01), 0.0) > 0


# ---------- the treatment clock ----------

from canine_dsp.core import lymphoma_horizon as H


def _agent(name, kill, division_gated=True, axis=Axis.CYTOTOXIC, **kw):
    return Agent(name, axis, Layer.RECEPTOR, kill, 1.0, 1.0, True, division_gated=division_gated, **kw)


def test_days_to_clear_is_log_count_over_margin():
    assert H.days_to_clear(1e8, 0.1) == pytest.approx((math.log(1e8) + H.EULER_GAMMA) / 0.1)
    assert H.days_to_clear(1e8, 0.0) == math.inf
    assert H.days_to_clear(1e8, -0.1) == math.inf


def test_a_stronger_margin_clears_faster_and_thin_margin_needs_years():
    thin, strong = H.days_to_clear(1e8, 0.0097), H.days_to_clear(1e8, 0.23)
    assert strong < 100 < 365 * 2 < thin


def test_response_then_relapse_when_the_load_bearing_agent_must_stop():
    """Two agents; the second alone cannot beat growth. The first is capped at 60 days, which is
    shorter than the time to clear. The model must call this response-then-relapse, not cure."""
    big = _agent("big", 0.30)
    small = _agent("small", 0.05, division_gated=False, axis=Axis.APOPTOSIS)
    sustain = {"big": 60.0}
    res = H.horizon([big, small], [], sustain, burden=1e11, growth=GROWTH_PER_DAY)
    bulk = res.outcomes[0]
    assert bulk.name == "drug-sensitive bulk"
    assert bulk.outcome == "relapses" and bulk.day == 60.0
    assert not res.cure_inside_window
    assert "RESPONSE THEN RELAPSE" in res.verdict()


def test_cured_inside_the_window_when_the_agent_lasts_long_enough():
    big = _agent("big", 0.30)
    res = H.horizon([big], [], {"big": 400.0}, burden=1e8, growth=GROWTH_PER_DAY)
    assert res.cure_inside_window
    assert res.clear_day == pytest.approx((math.log(1e8) + H.EULER_GAMMA) / (0.30 - H.BULK_GROWTH_PER_DAY))


def test_uncapped_agent_clears_eventually_if_its_margin_is_positive():
    nd = _agent("nd", 0.15, division_gated=False, axis=Axis.APOPTOSIS)
    res = H.horizon([nd], [], {}, burden=1e8, growth=GROWTH_PER_DAY)
    assert res.cure_inside_window and res.clear_day > 300     # feasible but long: 18.4+0.6 / 0.05
