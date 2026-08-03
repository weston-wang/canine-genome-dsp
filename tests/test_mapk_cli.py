import json

import numpy as np
import pandas as pd
import pytest

from canine_dsp.mapk_cli import (
    BRAIN_PENETRATION_FRACTION,
    canine_cns_hs_scenarios,
    localized_control_demo,
    localized_pihs_scenarios,
    mapk_cns_demo,
)
from canine_dsp.mapk_resistance import run_monte_carlo


def test_cns_scenarios_scale_css_by_brain_penetration_fraction():
    scenarios = canine_cns_hs_scenarios(breed="bmd")
    _, systemic_css, _, _ = scenarios["systemic_reference"]
    for drug, fraction in BRAIN_PENETRATION_FRACTION.items():
        _, css, _, provenance = scenarios[drug]
        assert css == systemic_css * fraction
        assert provenance["brain_penetration_reference_drug"] == drug


def test_cns_scenarios_location_multiplier_scales_all_drugs():
    baseline = canine_cns_hs_scenarios(breed="bmd", location_penetration_multiplier=1.0)
    halved = canine_cns_hs_scenarios(breed="bmd", location_penetration_multiplier=0.5)
    for drug in BRAIN_PENETRATION_FRACTION:
        _, css_base, _, _ = baseline[drug]
        _, css_half, _, _ = halved[drug]
        assert css_half == css_base * 0.5


def test_flat_coated_retriever_shifts_weight_toward_rtk_bypass():
    _, _, rates_bmd, _ = canine_cns_hs_scenarios(breed="bmd")["systemic_reference"]
    _, _, rates_fcr, provenance = canine_cns_hs_scenarios(breed="flat_coated_retriever")["systemic_reference"]
    assert np.argmax(rates_bmd) == 0  # pathway_reactivation dominates for bmd
    assert np.argmax(rates_fcr) == 1  # rtk_bypass dominates for flat_coated_retriever
    assert provenance["breed_germline_locus"] is not None


def test_mapk_cns_demo_writes_expected_outputs(tmp_path):
    mapk_cns_demo(tmp_path, breed="bmd", trials=20, horizon_days=90, seed=1)
    summary = json.loads((tmp_path / "summary.json").read_text())
    assert len(summary["scenarios"]) == len(BRAIN_PENETRATION_FRACTION)
    assert (tmp_path / "cns_penetration_sensitivity.csv").exists()
    assert (tmp_path / "cns_penetration.png").exists()
    assert "unverified_extrapolations" in summary


def test_localized_pihs_scenarios_debulking_shrinks_initial_burden_only():
    arms = localized_pihs_scenarios(breed="bmd", debulking_fraction=0.9)
    _, css_intact, _, burden_intact, _ = arms["intact_trametinib"]
    _, css_debulked, _, burden_debulked, _ = arms["debulked_trametinib"]
    assert burden_debulked == pytest.approx(burden_intact * 0.1)
    assert css_intact == css_debulked  # debulking must not change drug exposure
    _, css_untreated, _, _, _ = arms["intact_untreated"]
    assert css_untreated == 0.0


def test_localized_control_demo_writes_four_arms_with_mechanism_columns(tmp_path):
    localized_control_demo(tmp_path, breed="bmd", trials=20, horizon_days=90, seed=1)
    table = pd.read_csv(tmp_path / "localized_control_arms.csv")
    assert set(table["arm"]) == {"intact_untreated", "intact_trametinib",
                                 "debulked_untreated", "debulked_trametinib"}
    assert "mechanism_pathway_reactivation" in table.columns
    summary = json.loads((tmp_path / "summary.json").read_text())
    assert "reasoning_chain" in summary and "unverified_extrapolations" in summary
    assert (tmp_path / "localized_control.png").exists()


def test_debulking_delays_but_does_not_eliminate_relapse_risk():
    """The model's key qualitative claim: debulking shrinks a pre-existing resistant subclone
    proportionally (delaying when it's detected) but does not change *whether* one exists, so
    it should meaningfully extend median time-to-progression without much changing the
    probability of eventually progressing."""
    arms = localized_pihs_scenarios(breed="bmd")
    outcomes = {}
    for name in ("intact_trametinib", "debulked_trametinib"):
        model, css, seeding_rates, initial_burden, _ = arms[name]
        outcomes[name] = run_monte_carlo(model, css, 730, seeding_rates, trials=150,
                                         preexisting_prob=.3, initial_burden=initial_burden, seed=3)
    intact_ttp = outcomes["intact_trametinib"].time_to_progression
    debulked_ttp = outcomes["debulked_trametinib"].time_to_progression
    intact_median = np.nanmedian(intact_ttp)
    debulked_median = np.nanmedian(debulked_ttp)
    assert debulked_median > intact_median
    intact_durable = 1 - outcomes["intact_trametinib"].progressed.mean()
    debulked_durable = 1 - outcomes["debulked_trametinib"].progressed.mean()
    assert abs(debulked_durable - intact_durable) < 0.15
