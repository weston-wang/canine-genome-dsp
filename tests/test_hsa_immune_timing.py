import pytest

from canine_dsp.hsa_immune_timing import (
    NK_CELLS_HAVE_BEEN_GIVEN_INTRAVENOUSLY, SURGERY_AND_CHEMOTHERAPY_SUPPRESS_THE_EFFECTOR,
    TRAMETINIB_ENGAGES_ITS_TARGET_IN_CANINE_TUMOURS, TWO_INDEPENDENT_FAILURES_WITH_THE_SAME_SHAPE,
    VERDICT,
)
from canine_dsp.hsa_antiproliferative import STACK_TOLERATES_A_DELAYED_START
from canine_dsp.hsa_open_item_closures import SUMMARY as PRIOR_SUMMARY


def test_trametinib_target_engagement_was_demonstrated_before_the_trial_that_missed_it():
    t = TRAMETINIB_ENGAGES_ITS_TARGET_IN_CANINE_TUMOURS
    assert "30135215" in t["citation"]
    assert "38889903" in t["same_investigator"], "same first author as the trial that looked early"
    assert "ERK" in t["target_engagement"] and "downregulated" in t["target_engagement"]
    assert "NEOPLASTIC TISSUES" in t["drug_reached_the_tumour"]
    assert t["status"].startswith("CLOSED")
    assert "wrong tumour type" in t["what_it_does_and_does_not_settle"], "residual kept explicit"


def test_nk_cells_were_given_intravenously_not_only_into_tumours():
    n = NK_CELLS_HAVE_BEEN_GIVEN_INTRAVENOUSLY
    assert "38631708" in n["citation"]
    for arm in ("autologous_trial", "allogeneic_trial"):
        assert "INTRAVENOUS" in n[arm]["route"], arm
        assert "no serious" in n[arm]["safety"] or "no treatment-related serious" in n[arm]["safety"]
    assert n["autologous_trial"]["n_dogs"] == 9
    assert n["allogeneic_trial"]["n_dogs"] == 5
    assert n["status"].startswith("CLOSED")
    assert "hemangiosarcoma" in n["status"], "the disease residual survives the closure"


def test_the_prior_summary_called_both_of_these_unmeasured():
    """These are exactly the two items the previous pass left open."""
    left = PRIOR_SUMMARY["what_is_genuinely_left"]
    assert "engaging its target inside a canine" in left
    assert "systemically" in left


def test_the_phase_2_failure_measured_why_it_failed():
    s = SURGERY_AND_CHEMOTHERAPY_SUPPRESS_THE_EFFECTOR
    assert "41209004" in s["citation"]
    assert "INFERIOR" in s["result"] and "futility" in s["result"]
    assert "-18.2" in s["the_measured_mechanism"]
    assert "P<0.001" in s["the_measured_mechanism"]
    assert "r=0.62" in s["the_biomarker_runs_both_ways"]
    assert "go/no-go" in s["the_biomarker_runs_both_ways"]


def test_two_independent_trials_failed_the_same_way():
    c = TWO_INDEPENDENT_FAILURES_WITH_THE_SAME_SHAPE
    assert "32187827" in c["failure_1"] and "41209004" in c["failure_2"]
    assert "peri-surgical" in c["what_they_share"]
    assert "neither failed because the mechanism was wrong" in c["what_they_share"].lower()
    assert "AVOID" in c["the_design_consequence"]
    assert "cytotoxicity" in c["the_design_consequence"], "a measured gate, not a vague caution"


def test_the_model_already_says_delay_is_nearly_free():
    """The design consequence is affordable: the engine loses little to a late start."""
    at_once = STACK_TOLERATES_A_DELAYED_START[0]
    at_six_months = STACK_TOLERATES_A_DELAYED_START[180]
    assert at_six_months > at_once - 0.05
    assert "0.932" in TWO_INDEPENDENT_FAILURES_WITH_THE_SAME_SHAPE["consistency_with_the_model"]
    assert "0.896" in TWO_INDEPENDENT_FAILURES_WITH_THE_SAME_SHAPE["consistency_with_the_model"]


def test_the_verdict_trades_two_gaps_for_one_constraint():
    assert "no longer whether" in VERDICT["what_replaced_them"]
    assert "WHEN" in VERDICT["what_replaced_them"]
    assert "hemangiosarcoma" in VERDICT["the_residual"]
    assert "after the chemotherapy backbone" in VERDICT["the_experiment_this_now_points_at"]
