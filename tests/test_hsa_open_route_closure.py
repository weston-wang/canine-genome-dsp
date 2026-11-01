"""Recompute every modelled closure in `hsa_open_route_closure` from the engine."""
import numpy as np
import pytest

from canine_dsp import hsa_scenarios as hs
from canine_dsp.hsa_open_route_closure import (
    CANDID_SCREENING, CLOSURE_SUMMARY, EBAT_REDOSING_REFUTATION, RUPTURE_CANDIDATES,
    SECOND_COMPARTMENT, TUMOUR_CONTROL_DURABLE_5YR, VACCINE_TAKE,
    joint_durability, screened_rupture_hazard,
)
from canine_dsp.mapk_resistance import run_monte_carlo_two_compartment, run_monte_carlo_with_vaccine

VMK = 0.05
P = hs._PREEXISTING_PROB_CENTRAL


def _five_clone(vmk=VMK):
    return hs.hsa_vaccine_followon_scenarios(vaccine_max_kill_values=[vmk])[vmk]


def _single_compartment(vaccine_max_kill, horizon=1825, trials=300):
    m5, css5, seeding, _ = _five_clone(vaccine_max_kill)
    out = run_monte_carlo_with_vaccine(
        m5, css5, horizon, seeding, vaccine_start_day=hs.HSA_VACCINE_START_DAY,
        vaccine_ramp_days=hs.HSA_VACCINE_RAMP_DAYS, vaccine_max_kill=vaccine_max_kill,
        immune_escape_seeding_rate=hs.HSA_IMMUNE_ESCAPE_SEEDING_RATE,
        clone_names=hs.HSA_VACCINE_CLONE_NAMES, trials=trials, preexisting_prob=P, seed=7)
    return 1 - out.progressed.mean()


# ---------- route 5: rupture as a competing hazard ----------

def test_recorded_tumour_control_figure_matches_the_engine():
    assert _single_compartment(VMK) == pytest.approx(TUMOUR_CONTROL_DURABLE_5YR, abs=0.05)


def test_rupture_hazard_is_multiplicative_and_can_erase_the_vaccine_benefit():
    """A dog that bleeds to death with a controlled tumour counts as a durable response to the
    engine and as a dead dog to everyone else."""
    clean = joint_durability(TUMOUR_CONTROL_DURABLE_5YR, 0.0)
    assert clean["joint_durability"] == pytest.approx(TUMOUR_CONTROL_DURABLE_5YR)

    ten = joint_durability(TUMOUR_CONTROL_DURABLE_5YR, 0.10)
    assert ten["joint_durability"] == pytest.approx(0.571, abs=0.005)
    assert ten["points_lost"] == pytest.approx(39.6, abs=1.0)

    twenty = joint_durability(TUMOUR_CONTROL_DURABLE_5YR, 0.20)
    assert twenty["joint_durability"] < 0.35, "a 20%/yr hazard costs more than the vaccine buys"


def test_joint_durability_is_monotone_and_bounded():
    previous = 1.1
    for hazard in (0.0, 0.05, 0.10, 0.20, 0.40, 1.0):
        value = joint_durability(TUMOUR_CONTROL_DURABLE_5YR, hazard)["joint_durability"]
        assert 0.0 <= value <= TUMOUR_CONTROL_DURABLE_5YR
        assert value < previous
        previous = value


def test_joint_durability_rejects_out_of_range_inputs():
    with pytest.raises(ValueError):
        joint_durability(0.9, 1.5)
    with pytest.raises(ValueError):
        joint_durability(1.5, 0.1)


def test_screening_reduces_the_hazard_by_its_real_validated_sensitivity():
    low, high = CANDID_SCREENING["sensitivity_three_most_aggressive_cancers"]
    assert 0.78 <= low < high <= 0.91

    residual_low = screened_rupture_hazard(0.20, low)["residual_hazard"]
    residual_high = screened_rupture_hazard(0.20, high)["residual_hazard"]
    assert residual_high < residual_low < 0.20

    # At the optimistic end of the real sensitivity range, a 20%/yr hazard drops far enough that
    # joint durability recovers most of what the hazard took.
    rescued = joint_durability(TUMOUR_CONTROL_DURABLE_5YR, residual_high)["joint_durability"]
    unrescued = joint_durability(TUMOUR_CONTROL_DURABLE_5YR, 0.20)["joint_durability"]
    assert rescued > unrescued + 0.4


def test_the_failed_haemostatic_candidate_is_recorded_as_failed():
    """Reporting the negative at the same weight as the positives is the point."""
    failed = [c for c in RUPTURE_CANDIDATES if c["id"] == "5a"][0]
    assert "FAILED" in failed["verdict"]
    assert "27669112" in failed["citation"]
    assert "in_vitro_contrast" in failed, "the in vitro/clinical split is the lesson"


# ---------- route 6: vaccine take ----------

def test_take_rate_mixes_linearly_between_the_two_engine_outcomes():
    takes = _single_compartment(VMK)
    fails = _single_compartment(0.0)
    assert fails < takes, "a vaccine that does not take must do nothing"

    for take_rate, recorded in VACCINE_TAKE["population_durable_by_take_rate"].items():
        assert take_rate * takes + (1 - take_rate) * fails == pytest.approx(recorded, abs=0.06)


def test_take_is_the_second_largest_lever_after_potency():
    per_ten_points = VACCINE_TAKE["points_of_durability_per_10_points_of_take"]
    curve = VACCINE_TAKE["population_durable_by_take_rate"]
    measured = (curve[1.0] - curve[0.4]) / 6.0 * 100
    assert measured == pytest.approx(per_ten_points, abs=0.5)


def test_the_route_6_candidate_carries_an_in_disease_mechanism_and_a_dosed_agent():
    checkpoint = [c for c in VACCINE_TAKE["candidates"] if c["id"] == "6a"][0]
    assert "35136176" in checkpoint["hsa_specific_mechanism"], "mechanism measured in canine HSA"
    assert "33580183" in checkpoint["therapy_evidence"], "and a real dosed canine antibody"
    assert "Never given for hemangiosarcoma" in checkpoint["limits"]


# ---------- route 7: the second compartment ----------

def _two_compartment(vaccine_max_kill, nodal_prob, trials=200):
    m5, css5, seeding, _ = _five_clone(VMK)
    out = run_monte_carlo_two_compartment(
        m5, css5, 1825, seeding, nodal_involvement_prob=nodal_prob, nodal_seed_fraction=0.1,
        debulking_fraction=0.97, trials=trials, preexisting_prob=P,
        vaccine_start_day=hs.HSA_VACCINE_START_DAY, vaccine_ramp_days=hs.HSA_VACCINE_RAMP_DAYS,
        vaccine_max_kill=vaccine_max_kill,
        immune_escape_seeding_rate=hs.HSA_IMMUNE_ESCAPE_SEEDING_RATE,
        clone_names=hs.HSA_VACCINE_CLONE_NAMES, seed=7)
    nodal = sum(1 for c in out.dominant_compartment if c == "nodal")
    return 1 - out.progressed.mean(), nodal


def test_a_systemic_persistent_agent_reaches_the_compartment_surgery_cannot():
    for nodal_prob, recorded in SECOND_COMPARTMENT["with_systemic_persistent_agent"].items():
        durable, nodal_relapses = _two_compartment(VMK, nodal_prob)
        assert durable == pytest.approx(recorded, abs=0.03)
        assert nodal_relapses == SECOND_COMPARTMENT["nodal_relapses_with_agent"]


def test_without_a_systemic_agent_the_unreached_compartment_is_where_relapse_happens():
    durable_none, nodal_none = _two_compartment(0.0, 0.0)
    durable_high, nodal_high = _two_compartment(0.0, 0.6)
    assert durable_none == pytest.approx(SECOND_COMPARTMENT["vaccine_off"][0.0], abs=0.05)
    assert durable_high == pytest.approx(SECOND_COMPARTMENT["vaccine_off"][0.6], abs=0.05)
    assert nodal_none == 0, "with no second site there can be no relapse in it"
    assert nodal_high > 30, "with one, it carries a large share of relapses"


def test_hsa_still_does_not_call_the_two_compartment_engine_itself():
    """The closure works; the pipeline has not adopted it. Keep that visible."""
    from pathlib import Path
    src = Path(__file__).resolve().parents[1] / "src" / "canine_dsp"
    for name in ("hsa_cli.py", "hsa_scenarios.py"):
        assert "run_monte_carlo_two_compartment" not in (src / name).read_text()


# ---------- the self-refutation ----------

def test_the_ebat_redosing_proposal_is_recorded_as_refuted_not_quietly_dropped():
    assert "32187827" in EBAT_REDOSING_REFUTATION["citation"]
    assert "REDUCED efficacy" in EBAT_REDOSING_REFUTATION["result"]
    assert "requirement" in EBAT_REDOSING_REFUTATION["what_survives"].lower()


def test_every_open_route_has_a_status_and_a_named_lever():
    assert {c["route"] for c in CLOSURE_SUMMARY} == {5, 6, 7}
    for entry in CLOSURE_SUMMARY:
        assert entry["status"] and entry["best_lever"] and entry["note"]
    rupture = [c for c in CLOSURE_SUMMARY if c["route"] == 5][0]
    assert rupture["status"] == "PARTIALLY CLOSED", "no pharmacological closure exists for it"
