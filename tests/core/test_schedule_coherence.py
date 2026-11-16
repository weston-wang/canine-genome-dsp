"""Access and duty must come from the same schedule. The published answer's did not."""

from __future__ import annotations

import pytest

from canine_dsp.core import durable_regimen as dr
from canine_dsp.core import intraarterial_route as ia
from canine_dsp.core import schedule_coherence as sc
from canine_dsp.core.catalogue import ESCAPES, GROWTH_PER_DAY, LEPTOMENINGEAL, PARENCHYMA
from canine_dsp.core.dormancy import DormancyModel
from canine_dsp.core.regimen import Agent, Axis, Layer, Regimen

BOTH = (PARENCHYMA, LEPTOMENINGEAL)


def _worst(regimen, growth=GROWTH_PER_DAY):
    d = DormancyModel()
    return min(d.margin(regimen, e, growth) if "persister" in e.name
               else regimen.effective_kill_against(e) - growth for e in ESCAPES)


def _with_cytotoxic(compartment, access, duty, potency=0.15):
    others = [a for a in dr.build(compartment).agents
              if a.name not in ("temozolomide", "hydroxychloroquine (autophagy)")]
    agent = Agent("cytotoxic", Axis.CYTOTOXIC, Layer.RECEPTOR, potency, access, duty, True)
    return Regimen("scheduled", others + [agent])


# --- the contradiction ---------------------------------------------------------------------------------

def test_the_published_agent_claims_a_gain_its_route_cannot_sustain():
    tmz = next(a for a in dr.build(PARENCHYMA).agents if "temozolomide" in a.name)
    assert tmz.access == pytest.approx(ia.TEMOZOLOMIDE_CSF_PLASMA * ia.CONSERVATIVE_GAIN, abs=1e-9)
    assert tmz.duty == 1.0
    # The gain requires the procedure; the procedure cannot run daily.
    assert not sc.is_coherent(sc.Route.IA_WITH_DISRUPTION, tmz.duty, uses_disruption_gain=True)


def test_an_oral_route_cannot_claim_the_disruption_gain_at_all():
    assert not sc.is_coherent(sc.Route.ORAL_CONTINUOUS, 1.0, uses_disruption_gain=True)
    assert sc.is_coherent(sc.Route.ORAL_CONTINUOUS, 1.0, uses_disruption_gain=False)


def test_the_procedure_route_caps_duty_near_one_day_in_twenty_eight():
    assert sc.MAX_DUTY[sc.Route.IA_WITH_DISRUPTION] == pytest.approx(1 / 28, abs=1e-12)
    assert sc.is_coherent(sc.Route.IA_WITH_DISRUPTION, 1 / 28, uses_disruption_gain=True)
    assert not sc.is_coherent(sc.Route.IA_WITH_DISRUPTION, 0.5, uses_disruption_gain=True)


# --- only the incoherent row closes -----------------------------------------------------------------------

@pytest.mark.parametrize("label", [k for k in sc.SCHEDULE_SWEEP if "INCOHERENT" not in k])
def test_every_achievable_schedule_leaves_the_parenchyma_open(label):
    access, duty, expected = sc.SCHEDULE_SWEEP[label]
    got = _worst(_with_cytotoxic(PARENCHYMA, access, duty))
    assert got == pytest.approx(expected, abs=5e-4)
    assert got < 0, f"{label} was supposed to be open"


def test_the_only_closing_row_is_the_one_that_cannot_be_delivered():
    access, duty, expected = sc.SCHEDULE_SWEEP["AS PUBLISHED -- INCOHERENT"]
    got = _worst(_with_cytotoxic(PARENCHYMA, access, duty))
    assert got == pytest.approx(expected, abs=5e-4) and got > 0
    assert not sc.is_coherent(sc.Route.IA_WITH_DISRUPTION, duty, uses_disruption_gain=True)


def test_a_combined_oral_plus_monthly_boost_does_not_rescue_it():
    """The boost applies on one day in twenty-eight, so the time-average barely moves."""
    averaged = ia.TEMOZOLOMIDE_CSF_PLASMA * (27 / 28) + (
        ia.TEMOZOLOMIDE_CSF_PLASMA * ia.CONSERVATIVE_GAIN) / 28
    assert averaged == pytest.approx(0.219, abs=0.005)
    assert _worst(_with_cytotoxic(PARENCHYMA, averaged, 1.0)) < 0


# --- the coherent version ----------------------------------------------------------------------------------

@pytest.mark.parametrize("compartment,key", [(PARENCHYMA, "parenchyma"),
                                             (LEPTOMENINGEAL, "leptomeninges")])
def test_the_coherent_all_oral_regimen_is_open_at_reference_potency(compartment, key):
    others = [a for a in dr.build(compartment).agents
              if a.name not in ("temozolomide", "paxalisib", "hydroxychloroquine (autophagy)")]
    oral = [
        Agent("paxalisib (oral)", Axis.PI3K_PARALLEL, Layer.RECEPTOR, sc.REFERENCE_POTENCY,
              ia.PAXALISIB_KPUU, 1.0, True),
        Agent("cytotoxic (oral)", Axis.CYTOTOXIC, Layer.RECEPTOR, sc.REFERENCE_POTENCY,
              ia.TEMOZOLOMIDE_CSF_PLASMA, 1.0, True),
    ]
    expected, _ = sc.COHERENT_ALL_ORAL[key]
    got = _worst(Regimen("coherent", others + oral))
    assert got == pytest.approx(expected, abs=5e-4)
    assert got < 0


@pytest.mark.parametrize("compartment,key", [(PARENCHYMA, "parenchyma"),
                                             (LEPTOMENINGEAL, "leptomeninges")])
def test_it_would_need_roughly_double_the_reference_potency(compartment, key):
    others = [a for a in dr.build(compartment).agents
              if a.name not in ("temozolomide", "paxalisib", "hydroxychloroquine (autophagy)")]
    pax = Agent("paxalisib (oral)", Axis.PI3K_PARALLEL, Layer.RECEPTOR, sc.REFERENCE_POTENCY,
                ia.PAXALISIB_KPUU, 1.0, True)
    _, required = sc.COHERENT_ALL_ORAL[key]
    assert required >= sc.REFERENCE_POTENCY * 1.6
    cyto = Agent("cytotoxic (oral)", Axis.CYTOTOXIC, Layer.RECEPTOR, required,
                 ia.TEMOZOLOMIDE_CSF_PLASMA, 1.0, True)
    assert _worst(Regimen("x", others + [pax, cyto])) > 0


# --- the retraction must be explicit -----------------------------------------------------------------------

def test_the_published_margins_are_retracted_by_name():
    joined = " ".join(sc.WHAT_IS_RETRACTED)
    assert "0.0556" in joined and "0.0732" in joined
    assert "eleven escapes are closed" in joined


def test_the_seven_day_doubling_claim_is_retracted():
    assert any("SEVEN-DAY DOUBLING" in r for r in sc.WHAT_IS_RETRACTED)


def test_the_later_updates_are_retracted_too_rather_than_left_standing():
    """Changing the drug does not repair a scheduling contradiction."""
    joined = " ".join(sc.WHAT_IS_RETRACTED)
    assert "CARBOPLATIN SWAP" in joined and "MICROTUBULE" in joined


def test_what_survives_is_stated_and_does_not_include_the_margins():
    joined = " ".join(sc.WHAT_SURVIVES)
    assert "THE SITES" in joined
    assert "hs_drug_sensitivity" in joined
    assert "0.0556" not in joined


def test_the_root_cause_is_recorded_as_the_projects_recurring_error():
    joined = " ".join(sc.WHY_THE_OBJECT_MODEL_DID_NOT_CATCH_IT)
    assert "INDEPENDENT FLOATS" in joined
    assert "TWO NUMBERS FROM DIFFERENT CONTEXTS MULTIPLIED TOGETHER" in joined
