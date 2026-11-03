"""The cross-validator must actually block the six errors this project has already committed."""

from __future__ import annotations

import pytest

from canine_dsp.core.evidence import (BarrierState, Disease, Measurement, Population,
                                      ProvenanceError, Provenance, Quantity, Registry, Species)

DOG_HS = Population(Species.DOG, Disease.HISTIOCYTIC_SARCOMA)
DOG_HS_DASATINIB = Population(Species.DOG, Disease.HISTIOCYTIC_SARCOMA, agent="dasatinib")
DOG_HS_TRAMETINIB = Population(Species.DOG, Disease.HISTIOCYTIC_SARCOMA, agent="trametinib")
DOG_OSTEOSARCOMA = Population(Species.DOG, Disease.OSTEOSARCOMA)
MOUSE_HS = Population(Species.MOUSE, Disease.HISTIOCYTIC_SARCOMA)


def _ic50(agent: str, value: float = 9.0) -> Measurement:
    return Measurement(value, Quantity.IC50_NM,
                       Population(Species.DOG, Disease.HISTIOCYTIC_SARCOMA, agent=agent),
                       source="PMC5831740")


# --- the six historical errors, each of which must now raise -------------------------------------

def test_an_ic50_cannot_migrate_between_drugs():
    """250 nM was cobimetinib's, used as trametinib's."""
    cobimetinib = _ic50("cobimetinib", 179.0)
    assert cobimetinib.value_for(Population(Species.DOG, Disease.HISTIOCYTIC_SARCOMA,
                                            agent="cobimetinib")) == 179.0
    with pytest.raises(ProvenanceError, match="cobimetinib"):
        cobimetinib.value_for(DOG_HS_TRAMETINIB)


def test_a_penetration_ratio_cannot_migrate_between_drugs():
    """0.15 was trametinib's brain:plasma, applied to cobimetinib."""
    trametinib = Measurement(0.15, Quantity.TISSUE_PLASMA_RATIO,
                             Population(Species.DOG, Disease.NONE, agent="trametinib",
                                        barrier=BarrierState.INTACT),
                             source="trametinib brain:plasma")
    with pytest.raises(ProvenanceError):
        trametinib.value_for(Population(Species.DOG, Disease.NONE, agent="cobimetinib",
                                        barrier=BarrierState.INTACT))


def test_a_number_cannot_migrate_between_diseases():
    """PI3K IC50s from canine hemangiosarcoma were used for histiocytic sarcoma."""
    hsa = Measurement(230.0, Quantity.IC50_NM,
                      Population(Species.DOG, Disease.HEMANGIOSARCOMA, agent="VDC-597"),
                      source="PMID 30011343")
    with pytest.raises(ProvenanceError, match="hemangiosarcoma"):
        hsa.value_for(Population(Species.DOG, Disease.HISTIOCYTIC_SARCOMA, agent="VDC-597"))


def test_a_regimen_cannot_migrate_between_diseases():
    """0.75 mg/kg dasatinib is a canine OSTEOSARCOMA regimen."""
    dose = Measurement(0.75, Quantity.DOSE_MG_PER_KG,
                       Population(Species.DOG, Disease.OSTEOSARCOMA, agent="dasatinib"),
                       source="Marley 2015, PMID 26310368", n=4)
    assert dose.value_for(Population(Species.DOG, Disease.OSTEOSARCOMA, agent="dasatinib")) == 0.75
    with pytest.raises(ProvenanceError, match="osteosarcoma"):
        dose.value_for(DOG_HS_DASATINIB)


def test_a_mouse_result_cannot_be_read_as_canine():
    """Mouse xenografts of canine cells were described as canine efficacy data."""
    mouse = Measurement(1.0, Quantity.RELAPSE_FREE_FRACTION, MOUSE_HS,
                        source="PMID 30717820, orthotopic mouse xenograft")
    with pytest.raises(ProvenanceError, match="mouse"):
        mouse.value_for(DOG_HS)


def test_a_disrupted_barrier_ratio_cannot_be_read_as_intact_barrier_access():
    """0.37 in enhancing glioma was nearly used as access across an intact barrier."""
    disrupted = Measurement(0.37, Quantity.TISSUE_PLASMA_RATIO,
                            Population(Species.DOG, Disease.GLIOMA, agent="chlorambucil",
                                       barrier=BarrierState.DISRUPTED),
                            source="PMID 29775768")
    with pytest.raises(ProvenanceError):
        disrupted.value_for(Population(Species.DOG, Disease.GLIOMA, agent="chlorambucil",
                                       barrier=BarrierState.INTACT))


# --- the escape hatch must exist, and must leave a mark ------------------------------------------

def test_transfer_is_allowed_but_demands_a_justification():
    dose = Measurement(0.75, Quantity.DOSE_MG_PER_KG,
                       Population(Species.DOG, Disease.OSTEOSARCOMA, agent="dasatinib"),
                       source="PMID 26310368")
    with pytest.raises(ProvenanceError, match="justification"):
        dose.transfer_to(DOG_HS_DASATINIB, justification="")

    borrowed = dose.transfer_to(DOG_HS_DASATINIB,
                                justification="Tolerability is a property of the animal, not the "
                                              "tumour; the schedule transfers, the efficacy does not.")
    assert borrowed.value_for(DOG_HS_DASATINIB) == 0.75
    assert borrowed.provenance is Provenance.TRANSFERRED
    assert "transferred from" in borrowed.source


def test_a_transferred_number_is_never_indistinguishable_from_a_measured_one():
    m = _ic50("dasatinib")
    t = m.transfer_to(DOG_HS_TRAMETINIB, justification="same target class")
    assert m.provenance is Provenance.MEASURED
    assert t.provenance is Provenance.TRANSFERRED
    assert t.provenance is not m.provenance


def test_transferred_provenance_cannot_be_constructed_without_justification():
    with pytest.raises(ProvenanceError, match="TRANSFERRED"):
        Measurement(1.0, Quantity.IC50_NM, DOG_HS, source="x",
                    provenance=Provenance.TRANSFERRED)


# --- structural guarantees -----------------------------------------------------------------------

def test_no_measurement_can_exist_without_a_source():
    with pytest.raises(ProvenanceError, match="no source"):
        Measurement(9.0, Quantity.IC50_NM, DOG_HS, source="")


def test_a_superseded_number_raises_rather_than_returning_quietly():
    m = _ic50("cobimetinib", 250.0)
    dead = m.supersede("250 nM was cobimetinib's, inflated from a mean of 179")
    with pytest.raises(ProvenanceError, match="SUPERSEDED"):
        dead.value_for(Population(Species.DOG, Disease.HISTIOCYTIC_SARCOMA, agent="cobimetinib"))


def test_an_agentless_population_matches_any_agent():
    """A survival figure belongs to a disease, not to a drug."""
    survival = Measurement(44, Quantity.MEDIAN_SURVIVAL_DAYS,
                           Population(Species.DOG, Disease.HISTIOCYTIC_SARCOMA_CNS),
                           source="Toyoda 2020")
    assert survival.value_for(Population(Species.DOG, Disease.HISTIOCYTIC_SARCOMA_CNS,
                                         agent="lomustine")) == 44


def test_unknown_barrier_state_does_not_block_a_read():
    m = Measurement(0.5, Quantity.TISSUE_PLASMA_RATIO,
                    Population(Species.DOG, Disease.NONE, agent="x", barrier=BarrierState.UNKNOWN),
                    source="s")
    assert m.value_for(Population(Species.DOG, Disease.NONE, agent="x",
                                  barrier=BarrierState.INTACT)) == 0.5


# --- the registry audit --------------------------------------------------------------------------

def test_registry_audit_flags_non_canine_and_non_hs_measurements():
    r = Registry()
    r.add(_ic50("dasatinib"))
    r.add(Measurement(1.0, Quantity.RELAPSE_FREE_FRACTION, MOUSE_HS, source="PMID 30717820"))
    r.add(Measurement(0.75, Quantity.DOSE_MG_PER_KG, DOG_OSTEOSARCOMA, source="PMID 26310368"))
    audit = r.audit()
    assert audit["total"] == 3
    assert len(audit["not_measured_in_dogs"]) == 1, "the mouse xenograft"
    # The mouse result IS histiocytic sarcoma, so it is flagged on species and not on disease.
    # The two axes are independent, which is the point: a number can be wrong on either.
    assert audit["not_measured_in_histiocytic_sarcoma"] == [
        "dose (mg/kg) = 0.75 [dog, osteosarcoma] -- measured, PMID 26310368"]
    assert audit["unsourced"] == []


def test_registry_flags_one_quantity_recorded_for_several_agents():
    r = Registry()
    r.add(_ic50("dasatinib", 9.0))
    r.add(_ic50("cobimetinib", 179.0))
    flagged = r.audit()["same_quantity_recorded_for_multiple_agents"]
    assert len(flagged) == 1
    assert sorted(flagged[0]["agents"]) == ["cobimetinib", "dasatinib"]


def test_the_audit_states_the_limit_of_what_it_guarantees():
    text = Registry().audit()["what_this_guarantees"]
    assert "does NOT" in text and "correct" in text
