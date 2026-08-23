import numpy as np
import pytest

from canine_dsp.hsa_growth_pharmacodynamics import (
    ACHIEVABLE_SUPPRESSION_AT_CANINE_CMAX, EXPOSURE_GAP, IMPLIED_EC50_uM,
    PROPRANOLOL_CANINE_EXPOSURE, PROPRANOLOL_CLINICAL_PROLIFERATION_SIGNAL,
    PROPRANOLOL_IN_VITRO_ANTIPROLIFERATIVE, PROPRANOLOL_IS_NOT_ONLY_ANTIPROLIFERATIVE,
    PROPRANOLOL_MW_G_PER_MOL, VERDICT, concentration_for_suppression, ec50_from_single_point,
    emax_growth_suppression, ng_per_ml_to_micromolar,
)
from canine_dsp.hsa_gap_stack import GROWTH_REDUCTION_REQUIRED


# ---------- the pharmacodynamic machinery ----------

def test_unit_conversion_is_a_plain_molarity_calculation():
    assert ng_per_ml_to_micromolar(259.34) == pytest.approx(1.0)
    assert ng_per_ml_to_micromolar(18.7) == pytest.approx(0.0721, abs=0.0005)
    assert ng_per_ml_to_micromolar(0.0) == 0.0
    with pytest.raises(ValueError):
        ng_per_ml_to_micromolar(-1.0)
    with pytest.raises(ValueError):
        ng_per_ml_to_micromolar(10.0, mw_g_per_mol=0.0)


def test_emax_is_bounded_monotone_and_half_maximal_at_the_ec50():
    assert emax_growth_suppression(0.0, 10.0) == 0.0
    assert emax_growth_suppression(10.0, 10.0) == pytest.approx(0.5)
    assert emax_growth_suppression(1e6, 10.0) == pytest.approx(1.0, abs=1e-4)
    curve = emax_growth_suppression(np.array([0.0, 1.0, 10.0, 100.0]), 10.0)
    assert curve.shape == (4,)
    assert np.all(np.diff(curve) > 0)
    assert emax_growth_suppression(10.0, 10.0, max_suppression=0.6) == pytest.approx(0.3)
    for bad in (dict(ec50_uM=0.0), dict(ec50_uM=10.0, hill=0.0),
                dict(ec50_uM=10.0, max_suppression=1.5)):
        with pytest.raises(ValueError):
            emax_growth_suppression(1.0, **bad)
    with pytest.raises(ValueError):
        emax_growth_suppression(-1.0, 10.0)


def test_the_two_inverses_round_trip_against_the_forward_curve():
    ec50 = ec50_from_single_point(25.0, 0.4)
    assert emax_growth_suppression(25.0, ec50) == pytest.approx(0.4)
    conc = concentration_for_suppression(0.4, ec50)
    assert conc == pytest.approx(25.0)
    for hill in (0.5, 1.0, 2.0):
        e = ec50_from_single_point(25.0, 0.4, hill=hill)
        assert emax_growth_suppression(25.0, e, hill=hill) == pytest.approx(0.4)
    with pytest.raises(ValueError):
        ec50_from_single_point(25.0, 1.0)
    with pytest.raises(ValueError):
        concentration_for_suppression(1.0, 10.0)


# ---------- the two measured anchors ----------

def test_the_in_vitro_anchor_is_the_stiles_dose_response():
    low, high = PROPRANOLOL_IN_VITRO_ANTIPROLIFERATIVE["at_25_uM_proliferation_reduction"]
    assert (low, high) == (0.15, 0.67)
    assert "23555867" in PROPRANOLOL_IN_VITRO_ANTIPROLIFERATIVE["citation"]
    assert PROPRANOLOL_IN_VITRO_ANTIPROLIFERATIVE["in_vivo_mouse"]["tumour_mass_reduction"] > 0.6
    # The EC50s are inverted from that one measured point, so they must reproduce it.
    for key, target in (("least_sensitive_line", low), ("most_sensitive_line", high)):
        assert emax_growth_suppression(25.0, IMPLIED_EC50_uM[key]) == pytest.approx(target)
    assert IMPLIED_EC50_uM["most_sensitive_line"] < IMPLIED_EC50_uM["midpoint"] \
        < IMPLIED_EC50_uM["least_sensitive_line"]


def test_the_exposure_anchor_is_the_prodox_measurement():
    assert PROPRANOLOL_CANINE_EXPOSURE["propranolol_cmax_ng_per_ml"] == 18.7
    assert "40386412" in PROPRANOLOL_CANINE_EXPOSURE["citation"]
    assert max(PROPRANOLOL_CANINE_EXPOSURE["dose_cohorts_mg_per_kg"]) == 1.3
    assert "protein bound" in PROPRANOLOL_CANINE_EXPOSURE["caveat"]


# ---------- the finding ----------

def test_the_achievable_concentration_is_hundreds_of_fold_below_the_active_one():
    cmax_uM = ng_per_ml_to_micromolar(PROPRANOLOL_CANINE_EXPOSURE["propranolol_cmax_ng_per_ml"])
    assert 25.0 / cmax_uM == pytest.approx(347, abs=5)
    for key, recorded in ACHIEVABLE_SUPPRESSION_AT_CANINE_CMAX.items():
        assert emax_growth_suppression(cmax_uM, IMPLIED_EC50_uM[key]) == pytest.approx(
            recorded, abs=0.0001)
        assert recorded < 0.01, "under one percent on every anchor"


def test_the_stack_requirement_needs_about_a_hundredfold_higher_plasma_level():
    required = GROWTH_REDUCTION_REQUIRED["with_correction"]
    conc = concentration_for_suppression(EXPOSURE_GAP["required_suppression"],
                                         IMPLIED_EC50_uM["midpoint"])
    ng = conc * PROPRANOLOL_MW_G_PER_MOL
    assert ng == pytest.approx(EXPOSURE_GAP["required_cmax_ng_per_ml_midpoint_anchor"], rel=0.01)
    assert ng / EXPOSURE_GAP["achieved_cmax_ng_per_ml"] == pytest.approx(
        EXPOSURE_GAP["fold_short"], rel=0.02)
    # And the real requirement is larger still than the 16.3% this gap was computed at.
    assert required > EXPOSURE_GAP["required_suppression"]
    assert concentration_for_suppression(required, IMPLIED_EC50_uM["midpoint"]) > conc


def test_even_the_most_favourable_anchor_leaves_a_large_gap():
    best = EXPOSURE_GAP["using_most_sensitive_line"]
    worst = EXPOSURE_GAP["using_least_sensitive_line"]
    assert best["fold_short"] > 30
    assert worst["fold_short"] > best["fold_short"]
    assert best["required_ng_per_ml"] > 30 * EXPOSURE_GAP["achieved_cmax_ng_per_ml"]


# ---------- what the module refuses to resolve ----------

def test_the_contradicting_clinical_datum_is_recorded_not_discarded():
    """Chow 2015 measured a 34% proliferation drop at an exposure no higher than the dogs got."""
    signal = PROPRANOLOL_CLINICAL_PROLIFERATION_SIGNAL
    assert signal["proliferative_index_reduction"] == 0.34
    assert signal["n"] == 1
    assert "26375166" in signal["citation"]
    assert signal["proliferative_index_reduction"] > GROWTH_REDUCTION_REQUIRED["with_correction"]
    assert "two orders of magnitude" in VERDICT["the_contradicting_datum"]
    assert "does not resolve them" in VERDICT["the_contradicting_datum"]


def test_the_canine_evidence_says_the_mechanism_may_not_even_be_antiproliferative():
    other = PROPRANOLOL_IS_NOT_ONLY_ANTIPROLIFERATIVE
    assert "33598432" in other["citation"]
    assert "R-(+)" in other["receptor_independent"]
    assert "chemosensitisation" in other["implication"]


def test_the_verdict_answers_no_and_says_what_would_change_it():
    assert VERDICT["answer"].startswith("No")
    assert "0.072 uM" in VERDICT["answer"]
    assert "97x" in VERDICT["answer"]
    assert "never reached an active concentration" in VERDICT["what_it_explains"]
    assert "vinblastine would fail too" in VERDICT["what_it_explains"]
    assert "No such measurement exists" in VERDICT["what_would_change_it"]
    assert "requirement stands" in VERDICT["consequence_for_the_stack"]
