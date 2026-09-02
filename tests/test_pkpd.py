import math

import pytest

from canine_dsp import pkpd


def test_kill_rate_is_ln2_over_assay_at_ic50():
    k = pkpd.emax_kill_rate(ic50_nM=100.0, concentration_nM=100.0, assay_days=3.0)
    assert k == pytest.approx(math.log(2) / 3.0)


def test_kill_rate_is_zero_at_zero_concentration_and_monotonic():
    assert pkpd.emax_kill_rate(100.0, 0.0) == 0.0
    lo = pkpd.emax_kill_rate(100.0, 50.0)
    hi = pkpd.emax_kill_rate(100.0, 500.0)
    assert 0.0 < lo < hi


def test_kill_rate_rejects_bad_inputs():
    for bad in ({"ic50_nM": 0.0, "concentration_nM": 1.0},
                {"ic50_nM": 1.0, "concentration_nM": -1.0}):
        with pytest.raises(ValueError):
            pkpd.emax_kill_rate(**bad)


def test_free_cns_concentration_scales_by_kp_uu():
    assert pkpd.free_cns_concentration(1000.0, 0.3) == pytest.approx(300.0)


def test_model_can_fail_when_exposure_is_below_ic50():
    """Integrity: a drug that barely reaches its IC50 in the compartment must NOT close.
    C = 10 nM against IC50 500 nM over 3 days -> k ~ ln(1.02)/3 ~ 0.0066/day < 0.055 growth."""
    k = pkpd.emax_kill_rate(ic50_nM=500.0, concentration_nM=10.0)
    assert pkpd.margin(k) < 0


def test_cobimetinib_closes_from_measured_canine_inputs():
    """Both IC50 and Cmax measured in canine HS (PMID 39202410): the derived kill rate must beat
    growth at full exposure AND at a conservative brain access of 0.30."""
    d = pkpd.PARAMS["cobimetinib"]
    assert d.closes_at(1.0)
    assert d.closes_at(0.30)
    # and it should only need a small fraction of exposure to close
    assert d.min_access_to_close() < 0.15


def test_min_access_to_close_matches_the_closed_form():
    d = pkpd.PARAMS["cobimetinib"]
    kp = d.min_access_to_close()
    # at exactly the threshold access, the derived kill rate equals growth
    assert d.kill_rate_at(kp) == pytest.approx(pkpd.GROWTH_PER_DAY, abs=1e-9)


def test_prmt5i_potency_is_not_the_binding_constraint():
    """TNG908 potency is high enough that a tiny access closes -- so the ten-year arm's limit is
    access/duty/MTAP-status, not potency. (Cmax is a documented placeholder; this reads the hinge.)"""
    d = pkpd.PARAMS["tng908"]
    assert d.min_access_to_close() < 0.05


def test_derived_closures_reports_provenance():
    out = pkpd.derived_closures()
    assert out["cobimetinib"]["ic50_provenance"] == "measured"
    assert out["tng908"]["ic50_provenance"] == "transferred from another population"


def test_target_attainment_matches_the_trial_at_the_mtd():
    """Gap 2: the model is calibrated to the trametinib trial -- ~70% reach the efficacy exposure at
    the MTD, so ~30% are underdosed."""
    r = pkpd.target_attainment(pkpd.TRAMETINIB_MTD_MG_M2)
    assert abs(r["p_attain_target"] - 0.70) < 0.02
    assert abs(r["fraction_underdosed"] - 0.30) < 0.02
    assert r["provenance"] == "measured"


def test_attainment_rises_with_dose():
    lo = pkpd.target_attainment(pkpd.TRAMETINIB_MTD_MG_M2)["p_attain_target"]
    hi = pkpd.target_attainment(2 * pkpd.TRAMETINIB_MTD_MG_M2)["p_attain_target"]
    assert hi > lo


def test_dose_for_90pct_attainment_is_above_the_mtd():
    """Reaching 90% attainment requires dosing above the MTD -- which is dose-limited -- so the model
    flags that dose alone may not close the gap (monitoring/individualisation needed)."""
    d = pkpd.dose_for_attainment(0.90)
    assert d["dose_multiple_of_mtd"] > 1.0


def test_maintenance_bar_is_far_below_achievable_exposure():
    """The workaround's core: the maintenance kill bar is well under achievable exposure, so the
    treatment-benchmark attainment gap does not bind the maintenance use."""
    hr = pkpd.maintenance_headroom("cobimetinib")
    assert hr["headroom_x"] > 5          # many-fold headroom
    assert hr["maintenance_target_nM"] < hr["achievable_cmax_nM"]
    assert hr["provenance"] == "derived from measured parameters"


def test_synergistic_partner_pulls_the_90pct_dose_under_the_mtd():
    c = pkpd.combination_dose_reduction(3.0)
    assert c["dose_multiple_for_90pct_with_partner"] < 1.0   # below the MTD, ceiling no longer binding
    assert c["dose_multiple_for_90pct_with_partner"] < c["dose_multiple_for_90pct_alone"]


def test_dosing_workaround_reports_all_three_levers():
    w = pkpd.dosing_workaround()
    assert set(w) >= {"lever_1_maintenance_bar_is_lower", "lever_2_individualise_dose_TDM",
                      "lever_3_synergistic_combination", "bottom_line"}
