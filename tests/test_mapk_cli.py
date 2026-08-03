import json

import numpy as np

from canine_dsp.mapk_cli import BRAIN_PENETRATION_FRACTION, canine_cns_hs_scenarios, mapk_cns_demo


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
