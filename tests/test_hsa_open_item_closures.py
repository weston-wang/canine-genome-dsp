import pytest

from canine_dsp.hsa_open_item_closures import (
    CANINE_NK_HAS_BEEN_GIVEN_TO_DOGS, EBAT_REDOSING_TESTED_SOMETHING_ELSE,
    KINASE_DOMAIN_IS_COVERED, NK_CELLS_INVERT_THE_ESCAPE,
    RUPTURE_IS_NOW_GROUNDED_IN_A_REAL_COHORT, SUMMARY,
    TARGET_ENGAGEMENT_WAS_ASSAYED_TOO_EARLY, TWO_INDEPENDENT_EXPOSURE_ANCHORS,
)
from canine_dsp.hsa_parallel_pathway import (
    TRAMETINIB_CANINE_EXPOSURE, TRAMETINIB_STEADY_STATE_nM, MEK_PLUS_mTOR_SYNERGY,
)


def test_the_kinase_domain_gap_was_a_bookkeeping_error_not_a_real_gap():
    """The MEK inhibitor acts on a different node, so an mTOR lesion cannot shelter from it."""
    assert KINASE_DOMAIN_IS_COVERED["status"].startswith("CLOSED")
    assert "same clone" in KINASE_DOMAIN_IS_COVERED["the_claim_that_was_wrong"]
    assert "different node" in KINASE_DOMAIN_IS_COVERED["why_it_is_covered"]
    assert "32943547" in KINASE_DOMAIN_IS_COVERED["supporting_measurement"]
    assert "0.0445" in KINASE_DOMAIN_IS_COVERED["verified_in_the_engine"]


def test_the_kinase_domain_clone_really_is_brought_under_the_vaccine_by_the_second_drug():
    """Recomputed, not transcribed."""
    import numpy as np
    from dataclasses import replace
    from canine_dsp import hsa_scenarios as hs
    from canine_dsp.hsa_gap_stack import corrected_ic50
    from canine_dsp.hsa_parallel_pathway import with_mek_inhibitor, MEK_KILL_NEEDED_PER_DAY
    from canine_dsp.mapk_resistance import clone_growth_margins
    m5, css, _, _ = hs.hsa_vaccine_followon_scenarios(vaccine_max_kill_values=[0.03])[0.03]
    c = replace(m5, ic50_nM=corrected_ic50(m5.ic50_nM[0]))
    before = clone_growth_margins(c, css)
    assert int(np.argmax(before[:4])) == 1, "clone 1 carries the 9.5x shift and sets the bar"
    mod = with_mek_inhibitor(c, np.full(5, MEK_KILL_NEEDED_PER_DAY), ic50_nM_2=11.0)
    after = clone_growth_margins(mod, css, concentration_2=TRAMETINIB_STEADY_STATE_nM)
    assert after[1] < before[1], "the second drug acts on the clone the first cannot reach"
    assert after[1] == pytest.approx(0.030, abs=0.001)


def test_the_ebat_trial_changed_three_things_at_once():
    e = EBAT_REDOSING_TESTED_SOMETHING_ELSE
    assert len(e["what_changed_between_the_trials"]) == 3
    assert "32187827" in e["citation"]
    assert "DELAYED START" in e["the_authors_own_reading"]
    assert "never tested persistence" in e["what_it_therefore_does_not_refute"]
    assert "NOT evidence against" in e["status"]


def test_nk_cells_invert_antigen_loss_rather_than_being_defeated_by_it():
    n = NK_CELLS_INVERT_THE_ESCAPE
    assert "missing self" in n["principle"]
    assert "28699110" in n["human_evidence"]
    dog = n["does_the_mechanism_exist_in_DOGS"]
    assert "37971282" in dog["citation"]
    assert "nonfunctional" in dog["the_prior_doubt"], "the prior doubt is recorded, not skipped"
    assert "PREDICTED binding, not a functional demonstration" in dog["strength_of_this_evidence"]
    assert "foreign bacterial toxin" in n["why_repeat_dosing_does_not_repeat_the_ebat_failure"]


def test_canine_nk_therapy_is_real_but_not_yet_for_this_disease():
    c = CANINE_NK_HAS_BEEN_GIVEN_TO_DOGS
    assert "29254507" in c["citation"]
    assert "5 of 10" in c["first_in_dog_trial"]
    assert "32084139" in c["follow_up"]
    assert "osteosarcoma" in c["what_is_missing_for_HSA"]
    assert "not given systemically" in c["status"]


def test_target_engagement_was_looked_for_before_the_drug_had_arrived():
    t = TARGET_ENGAGEMENT_WAS_ASSAYED_TOO_EARLY
    assert t["when_they_looked"] == "days 0 and 7"
    assert TRAMETINIB_CANINE_EXPOSURE["time_to_steady_state_days"] == 14
    assert "before the exposure existed" in t["what_this_does_and_does_not_settle"]
    assert t["status"].startswith("CLOSED as an objection, OPEN as a confirmation")


def test_the_exposure_claim_no_longer_rests_on_the_drug_substitution():
    a = TWO_INDEPENDENT_EXPOSURE_ANCHORS
    assert "no substitution at all" in a["anchor_2_same_drug"]
    assert a["status"].startswith("CLOSED")
    # the two anchors are numerically the same concentration
    assert TRAMETINIB_STEADY_STATE_nM == pytest.approx(16.25, abs=0.1)
    assert MEK_PLUS_mTOR_SYNERGY["ic50_nM"]["combined_4to1"] < TRAMETINIB_STEADY_STATE_nM


def test_rupture_is_grounded_but_the_post_remission_rate_is_still_swept():
    r = RUPTURE_IS_NOW_GROUNDED_IN_A_REAL_COHORT
    assert "40334697" in r["citation"]
    assert r["composition"]["hemangiosarcoma"] == pytest.approx(0.562)
    assert sum(r["composition"].values()) == pytest.approx(1.0, abs=0.001)
    assert r["status"].startswith("NARROWED")
    assert "still" in r["what_it_does_not_close"]
    assert "does not depend on pinning the rate down" in r["why_the_screening_conclusion_survives_anyway"]


def test_the_summary_distinguishes_closed_objections_from_missing_evidence():
    closed = [v for v in SUMMARY.values() if v.startswith("CLOSED")]
    assert len(closed) >= 3
    left = SUMMARY["what_is_genuinely_left"]
    assert "positive-evidence gaps rather than contradictions" in left
    assert "Neither is refuted" in left
