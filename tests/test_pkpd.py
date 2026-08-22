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
