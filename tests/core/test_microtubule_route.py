"""The first regimen whose access and duty come from one schedule."""

from __future__ import annotations

import pytest

from canine_dsp.core import hs_drug_sensitivity as hs
from canine_dsp.core import microtubule_route as mt
from canine_dsp.core import schedule_coherence as sc
from canine_dsp.core import toxicity as tox
from canine_dsp.core.catalogue import ESCAPES, LEPTOMENINGEAL, PARENCHYMA
from canine_dsp.core.hs_drug_sensitivity import DrugClass

BOTH = (PARENCHYMA, LEPTOMENINGEAL)


# --- the point of the module: coherence ------------------------------------------------------------------

def test_no_agent_claims_the_osmotic_disruption_gain():
    """Access is bought with chemistry, not surgery. That is the whole fix."""
    from canine_dsp.core import intraarterial_route as ia
    for compartment in BOTH:
        for agent in mt.build(compartment).agents:
            assert agent.access <= 1.0
            assert agent.access != pytest.approx(
                ia.TEMOZOLOMIDE_CSF_PLASMA * ia.CONSERVATIVE_GAIN, abs=1e-9)


def test_every_agent_is_on_a_coherent_schedule():
    for compartment in BOTH:
        for agent in mt.build(compartment).agents:
            assert sc.is_coherent(sc.Route.ORAL_CONTINUOUS, agent.duty, uses_disruption_gain=False)


def test_the_procedure_is_absent_from_the_toxicity_profile():
    """No catheter, no anaesthesia, no seizure axis -- and no need for a reachable artery."""
    loads = tox.axis_loads(mt.toxicity_profiles(PARENCHYMA))
    assert tox.Organ.PROCEDURAL not in loads
    assert tox.Organ.SEIZURE not in loads


def test_access_and_duty_are_independent_choices_only_because_there_is_one_route():
    """A systemic agent's access does not depend on how often it is given."""
    a = next(x for x in mt.build(PARENCHYMA, duty=0.4).agents if x.name == mt.MICROTUBULE_AGENT)
    b = next(x for x in mt.build(PARENCHYMA, duty=1.0).agents if x.name == mt.MICROTUBULE_AGENT)
    assert a.access == b.access == pytest.approx(mt.SAGOPILONE_BRAIN_PLASMA_AUC, abs=1e-12)


# --- the answer -------------------------------------------------------------------------------------------

@pytest.mark.parametrize("compartment", BOTH)
def test_all_eleven_escapes_close(compartment):
    m = mt.margins(compartment)
    assert len(m) == len(ESCAPES)
    assert all(v > 0 for v in m.values()), {k: v for k, v in m.items() if v <= 0}


def test_the_published_margins_are_reproduced():
    assert mt.worst_margin(PARENCHYMA) == pytest.approx(0.0416, abs=5e-4)
    assert mt.worst_margin(LEPTOMENINGEAL) == pytest.approx(0.0592, abs=5e-4)


def test_the_duty_sweep_is_re_derived():
    for duty, (par, lep) in mt.BY_DUTY.items():
        assert mt.worst_margin(PARENCHYMA, duty=duty) == pytest.approx(par, abs=5e-4)
        assert mt.worst_margin(LEPTOMENINGEAL, duty=duty) == pytest.approx(lep, abs=5e-4)


def test_the_duty_threshold_is_where_the_parenchyma_turns_over():
    assert mt.worst_margin(PARENCHYMA, duty=mt.DUTY_THRESHOLD) > 0
    assert mt.worst_margin(PARENCHYMA, duty=0.4) < 0


def test_the_persister_is_covered_despite_a_division_gated_cytotoxic():
    """A mitotic poison cannot touch a dormant cell -- something else has to, and does."""
    m = mt.margins(PARENCHYMA)
    assert m["drug-tolerant persister"] > 0
    non_gated = [a.name for a in mt.build(PARENCHYMA).agents if not a.division_gated]
    assert non_gated, "the persister margin must not rest on a mitotic poison alone"


# --- it is WEAKER than what it replaces, and must say so ---------------------------------------------------

def test_it_reopens_at_a_seven_day_doubling():
    """The retracted regimen claimed it held to seven days. This one does not."""
    assert not mt.closes(0.693 / 7)
    assert mt.closes(0.693 / 10)


def test_it_is_more_fragile_than_the_incoherent_regimen_it_replaces():
    _, retracted = 0, 0.0556
    assert mt.worst_margin(PARENCHYMA) < retracted
    assert "MORE FRAGILE" in mt.WHAT_IT_COSTS_TO_BE_HONEST["the_lesson"]


def test_the_doubling_time_table_is_re_derived():
    for dbl, (par, lep) in mt.BY_DOUBLING_TIME.items():
        growth = 0.693 / dbl
        assert mt.worst_margin(PARENCHYMA, growth) == pytest.approx(par, abs=5e-4)
        assert mt.worst_margin(LEPTOMENINGEAL, growth) == pytest.approx(lep, abs=5e-4)


# --- the negative trial must not be buried ------------------------------------------------------------------

def test_the_glioblastoma_failure_is_recorded_with_its_numbers():
    g = mt.THE_GLIOBLASTOMA_FAILURE
    assert "PFS6 6.7%" in g["what_happened"]
    assert "NO OBJECTIVE RESPONSES" in g["what_happened"]
    assert "21321091" in g["what_happened"]


def test_the_transfer_argument_is_labelled_as_an_argument_not_proof():
    g = mt.THE_GLIOBLASTOMA_FAILURE
    assert "NOT PROOF" in g["THE_HONEST_STATUS"]
    assert "FAILS THE WAY EVERY OTHER ONE DID" in g["THE_HONEST_STATUS"]


def test_the_pk_pd_split_is_the_basis_of_the_transfer_argument():
    g = mt.THE_GLIOBLASTOMA_FAILURE
    assert "PHARMACODYNAMIC" in g["what_the_trial_establishes"]
    assert "PHARMACOKINETIC" in g["what_the_model_needs"]


def test_the_measured_penetration_beats_paclitaxel_by_construction():
    assert mt.SAGOPILONE_BRAIN_PLASMA_AUC == 0.80
    assert mt.PACLITAXEL_BRAIN_PLASMA_AUC == 0.0
    assert mt.RGN3067_EFFLUX_RATIO < 1.0, "efflux ratio below 1 means not an MDR1 substrate"


# --- what it closes for free ---------------------------------------------------------------------------------

def test_mgmt_does_not_apply_to_a_microtubule_agent():
    from canine_dsp.core import mgmt_escape as mg
    assert not mg.defeated_by_mgmt(mt.MICROTUBULE_AGENT)
    assert mg.lesion_of(mt.MICROTUBULE_AGENT) is mg.Lesion.NONE


def test_the_mechanism_matches_the_only_class_the_disease_is_sensitive_to():
    assert hs.sensitive_classes() == (DrugClass.MICROTUBULE,)
    assert DrugClass.O6_ALKYLATOR in hs.resistant_classes()
    assert DrugClass.N7_CROSSLINKER in hs.resistant_classes()


def test_the_marrow_ceiling_is_released():
    loads = tox.axis_loads(mt.toxicity_profiles(PARENCHYMA))
    assert loads[tox.Organ.MARROW] == pytest.approx(0.70, abs=1e-9)
    assert tox.Organ.PERIPHERAL_NERVE in loads


def test_the_regimen_is_tolerable_but_neuropathy_now_binds():
    """Headroom fell 0.30 -> 0.15 when the neuropathy budget was raised 0.55 -> 0.85.

    The raise is not conservatism for its own sake: sagopilone's development was DISCONTINUED
    because of neuropathy at effective doses. A toxicity that ends a drug is not a 0.55.
    """
    assert tox.tolerable(mt.toxicity_profiles(PARENCHYMA))
    assert mt.headroom() == pytest.approx(0.15, abs=1e-9)
    loads = tox.axis_loads(mt.toxicity_profiles(PARENCHYMA))
    assert max(loads, key=loads.get) is tox.Organ.PERIPHERAL_NERVE


# --- the limits ------------------------------------------------------------------------------------------------

def test_obtainability_is_flagged_as_a_class_argument_not_a_prescription():
    joined = " ".join(mt.WHAT_IS_STILL_ASSUMED)
    assert "CLASS ARGUMENT, NOT A PRESCRIPTION" in joined
    assert "preclinical" in joined


def test_the_ic50_to_kill_rate_gap_is_admitted():
    joined = " ".join(mt.WHAT_IS_STILL_ASSUMED)
    assert "IC50s" in joined and "not" in joined and "how fast it kills" in joined


def test_the_duty_assumption_is_flagged_as_unmeasured():
    assert any("NOT MEASURED" in a for a in mt.WHAT_IS_STILL_ASSUMED)


def test_an_unpriced_agent_raises_rather_than_being_silently_free():
    """The strict lookup is the safety property. It caught a real name mismatch on first run."""
    import canine_dsp.core.toxicity as t
    for agent in mt.build(PARENCHYMA).agents:
        assert agent.name in t.PROFILES, f"{agent.name} would be silently free"
