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


def test_every_tier_has_a_graded_pkpd_entry():
    """A tier with no PK/PD entry falls back to a flat ordinal site prior, which fails the bar."""
    from canine_dsp import maintenance_durability as md, pkpd as pk

    for tier in md.TIERS:
        assert tier.pkpd_key in pk.PARAMS, tier.genotype


def test_no_pkpd_entry_asserts_closure_on_an_assumed_exposure():
    """An ASSUMED Cmax may only be used to expose an access threshold, never to claim a margin."""
    from canine_dsp import pkpd as pk
    from canine_dsp.core.evidence import Provenance

    for key, d in pk.PARAMS.items():
        if d.cmax_provenance is Provenance.ASSUMED:
            assert "min_access_to_close" in d.note, key


def test_abemaciclib_records_the_metastasis_versus_intact_barrier_distinction():
    """The 96x/19x tissue multiple is from brain metastases with a disrupted barrier. Using it for
    invaded parenchyma would be the exact class of provenance error core.evidence exists to stop."""
    from canine_dsp import pkpd as pk

    note = pk.PARAMS["abemaciclib"].note
    assert "METASTAS" in note.upper()
    assert "intact" in note.lower()


# --- the cytostatic correction ---------------------------------------------------------------------

def test_a_pure_cytostatic_never_reaches_zero_net_growth():
    """The error this correction fixes: arrest is bounded below by zero, so no concentration of a
    cytostatic agent clears a tumour. Reading its exposure as a kill rate overstated it."""
    from canine_dsp import pkpd as pk

    for conc in (10.0, 100.0, 1_000.0, 1_000_000.0):
        net = pk.cytostatic_net_growth(40.0, conc)
        assert net > 0.0, conc
    # monotonically decreasing, approaching but never reaching zero
    assert pk.cytostatic_net_growth(40.0, 1e6) < pk.cytostatic_net_growth(40.0, 10.0)


def test_the_cytostatic_reading_is_less_favourable_than_the_kill_reading():
    """If the correction were not in the conservative direction it would be suspect."""
    from canine_dsp import pkpd as pk

    conc = pk.RIBOCICLIB_NONENHANCING_NM["400 mg QD, median"][0]
    kill_margin = pk.emax_kill_rate(40.0, conc) - pk.GROWTH_PER_DAY
    net = pk.cytostatic_net_growth(40.0, conc)
    assert kill_margin > 0 > -net, "the kill reading claims regression; the correct one does not"


def test_ribociclib_effect_is_reported_as_suppression_not_clearance():
    from canine_dsp import pkpd as pk

    eff = pk.ribociclib_cytostatic_effect()
    assert all(not r["clears_the_tumour"] for r in eff["by_site"].values())
    for row in eff["by_site"].values():
        assert row["doubling_time_days"] > eff["untreated_doubling_days"]
    assert "NOT clear" in eff["reading"]


def test_the_correction_itself_is_recorded_rather_than_silently_applied():
    """CLAUDE.md rule 5 and rule 8: a withdrawn number stays in the record with what replaced it."""
    from canine_dsp import pkpd as pk

    c = pk.ribociclib_margin_correction()
    assert "artifact" in c["what_was_published"]
    assert "cytotoxic reading" in c["why_it_was_wrong"]
    assert "does NOT close the invading edge by itself" in c["consequence"]
    # the measured access result must be explicitly preserved, since only the reading was wrong
    assert "stands untouched" in c["consequence"]


def test_the_direction_of_the_rodent_to_dog_access_transfer_is_recorded():
    """Kido 2022, recovered from a superseded page: 7 of 12 P-gp substrates had dog brain:plasma
    more than 3x mouse. It scales nothing -- it records that rodent-derived access figures in this
    project err conservatively, which is part of grading those transfers."""
    s = pkpd.RODENT_TO_DOG_EFFLUX_DIRECTION
    assert "UNDER-estimate" in s
    assert "7 of 12" in s
