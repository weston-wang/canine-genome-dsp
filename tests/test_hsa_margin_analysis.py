import numpy as np
import pytest

from canine_dsp.hsa_margin_analysis import (
    COMBINATION_IC50_SD_nM, COMBINATION_IC50_nM, IN_VIVO_DERIVED_EFFECT_SIZE,
    MARGIN_ACROSS_THE_REPORTED_UNCERTAINTY, STAGGERED_DOSING_IS_THE_PUBLISHED_OPTIMUM,
    THE_INTERACTION_EVIDENCE_IS_SPLIT, THE_TWO_ANCHORS_ARE_NOT_EQUALLY_VULNERABLE,
    TRAMETINIB_ACHIEVED_nM, VERDICT, implied_exponential_rate, margin,
)
from canine_dsp.hsa_parallel_pathway import MEK_KILL_NEEDED_PER_DAY, MEK_PLUS_mTOR_SYNERGY


def test_the_margin_includes_failure_within_one_standard_deviation():
    """The point estimate clears; one SD the wrong way does not."""
    m = MARGIN_ACROSS_THE_REPORTED_UNCERTAINTY
    assert m["at_point_estimate"] == pytest.approx(1.48, abs=0.02)
    assert m["at_ic50_plus_1sd"] < 1.0, "the honest headline: it can fail"
    assert m["at_ic50_minus_1sd"] > 3.0
    assert "INSIDE the measurement noise" in m["honest_statement"]
    assert "overstated" in m["what_this_is_not"]


def test_the_margin_is_recomputed_from_the_source_numbers():
    assert COMBINATION_IC50_nM == MEK_PLUS_mTOR_SYNERGY["ic50_nM"]["combined_4to1"]
    assert COMBINATION_IC50_SD_nM == MEK_PLUS_mTOR_SYNERGY["ic50_nM"]["combined_4to1_sd"]
    recomputed = margin(TRAMETINIB_ACHIEVED_nM, COMBINATION_IC50_nM + COMBINATION_IC50_SD_nM)
    assert recomputed == pytest.approx(MARGIN_ACROSS_THE_REPORTED_UNCERTAINTY["at_ic50_plus_1sd"])
    with pytest.raises(ValueError):
        margin(10.0, 0.0)


def test_the_protein_binding_objection_hits_only_the_in_vitro_anchor():
    a = THE_TWO_ANCHORS_ARE_NOT_EQUALLY_VULNERABLE
    assert a["in_vitro_anchor"]["status"].startswith("vulnerable")
    assert "10%" in a["in_vitro_anchor"]["assay_conditions"] and "FBS" in a["in_vitro_anchor"]["assay_conditions"]
    assert "AGAINST the plan" in a["in_vitro_anchor"]["why_it_is_vulnerable"]
    assert a["clinical_anchor"]["status"].startswith("robust")
    assert "already inside the number" in a["clinical_anchor"]["why_the_objection_cannot_reach_it"]
    assert a["clinical_anchor"]["value_nM"] == TRAMETINIB_ACHIEVED_nM


def test_the_kill_requirement_now_comes_from_a_measured_growth_curve():
    v = IN_VIVO_DERIVED_EFFECT_SIZE
    assert v["what_the_model_needs_per_day"] == MEK_KILL_NEEDED_PER_DAY
    lo_start, hi_start = v["treatment_started_at_mm3"]
    # recompute both ends of the implied vehicle growth rate
    fast = implied_exponential_rate(lo_start, v["vehicle_reached_mm3"], v["vehicle_reached_by_day"])
    slow = implied_exponential_rate(hi_start, v["vehicle_reached_mm3"], v["vehicle_reached_by_day"])
    assert slow == pytest.approx(v["implied_vehicle_net_growth_per_day"][0], abs=0.001)
    assert fast == pytest.approx(v["implied_vehicle_net_growth_per_day"][1], abs=0.001)
    lo_margin = slow / v["what_the_model_needs_per_day"]
    assert lo_margin == pytest.approx(v["margin_against_the_measured_envelope"][0], abs=0.15)
    assert lo_margin > 4.0, "the requirement sits well inside the measured envelope"


def test_the_in_vivo_bridge_keeps_its_own_limits_visible():
    limits = IN_VIVO_DERIVED_EFFECT_SIZE["the_honest_limits"]
    assert "double-count" in limits
    assert "does not transfer" in limits
    with pytest.raises(ValueError):
        implied_exponential_rate(0.0, 100.0, 21)


def test_the_interaction_evidence_disagrees_between_species_and_is_recorded_both_ways():
    i = THE_INTERACTION_EVIDENCE_IS_SPLIT
    assert "FELL" in i["in_dogs"]
    assert "INCREASED" in i["in_mice"]
    assert "cushion" in i["why_it_matters_for_the_margin"]
    assert "not resolved" in " ".join(i.keys()) or i["what_is_not_resolved"]
    assert "the pairing weakens" in i["what_is_not_resolved"]


def test_the_toxicity_fix_was_already_in_the_evidence():
    s = STAGGERED_DOSING_IS_THE_PUBLISHED_OPTIMUM
    assert "32943547" in s["citation"]
    assert "MINIMIZING HEMATOLOGIC AND RENAL SIDE EFFECTS" in s["finding"]
    assert "proteinuria" in s["why_it_answers_two_objections_at_once"]
    assert "recorded but not used" in s["status"]


def test_the_verdict_separates_what_improved_from_what_is_still_weak():
    assert "0.96x-3.25x" in VERDICT["what_was_overstated"]
    assert "30% of dogs" in VERDICT["what_was_overstated"]
    assert len(VERDICT["what_got_stronger"]) >= 4
    assert len(VERDICT["what_remains_genuinely_weak"]) >= 4
    assert any("sapanisertib exposure" in w for w in VERDICT["what_remains_genuinely_weak"])
    assert "includes failure" in VERDICT["the_honest_summary"]
