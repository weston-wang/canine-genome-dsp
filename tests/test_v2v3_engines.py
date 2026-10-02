"""Smoke tests for the v2 and v3 simulation engines.

The v2/v3 packages were reduced to their engines (the narrative retraction write-ups that
used to sit alongside them were removed). These tests keep the surviving engines exercised:
they must import and run a minimal scenario and return a well-formed relapse-free fraction.
"""

from __future__ import annotations

from canine_dsp.v2 import engine as v2
from canine_dsp.v3 import engine as v3


def test_v2_engine_runs_and_returns_a_bounded_relapse_free_fraction():
    regimen = {"mapk_concentration_nM": 120.0, "mapk_ic50_nM": 60.0}
    res = v2.run(regimen, trials=40, horizon_days=365, seed=1)
    assert set(res) >= {"relapse_free", "median_days_to_progression"}
    assert 0.0 <= res["relapse_free"] <= 1.0


def test_v2_engine_kills_harder_at_higher_concentration():
    low = v2.run({"mapk_concentration_nM": 20.0, "mapk_ic50_nM": 60.0}, trials=60, seed=3)
    high = v2.run({"mapk_concentration_nM": 400.0, "mapk_ic50_nM": 60.0}, trials=60, seed=3)
    assert high["relapse_free"] >= low["relapse_free"]


def test_v3_engine_runs_a_minimal_scenario():
    clone = v3.Clone(name="driver", growth=0.05, mapk_driver=True,
                     antigen_present=True, mhc_intact=True)
    agent = v3.Agent(name="mek", concentration_nM=200.0, ic50_nM=50.0, max_kill=0.3,
                     penetration={"brain": 1.0}, requires_mapk_driver=True)
    reg = v3.Regimen(name="mono", agents=[agent])
    res = v3.run([clone], reg, "brain", trials=40, horizon_days=365, seed=1)
    assert isinstance(res, dict) and res
