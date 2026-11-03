"""The this breed presentation is the anchor. These tests keep it from drifting back to the assumed one."""

from __future__ import annotations

import pytest

from canine_dsp.core import presentation as p
from canine_dsp.core.evidence import (BarrierState, Disease, Population, ProvenanceError, Quantity,
                                      Species)


# --- what the disease actually is ---------------------------------------------------------------

def test_the_disease_occupies_parenchyma_and_leptomeninges_not_a_resectable_extra_axial_shell():
    assert set(p.occupied_compartments()) == {p.Compartment.INVADED_PARENCHYMA,
                                              p.Compartment.LEPTOMENINGEAL}


def test_the_extra_axial_compartment_is_recorded_as_not_occupied():
    extra_axial = next(o for o in p.OCCUPANCY if o.compartment is p.Compartment.EXTRA_AXIAL)
    assert extra_axial.occupied is False
    assert "DOES NOT EXIST FOR THIS TUMOUR" in extra_axial.note


def test_parenchymal_invasion_is_universal_in_the_most_breed_weighted_series():
    assert p.PARENCHYMAL_INVASION.value == 1.0
    assert p.PARENCHYMAL_INVASION.n == 23
    assert "dogs of the predisposed breed" in p.PARENCHYMAL_INVASION.population.note
    assert "all cases" in p.PARENCHYMAL_INVASION.source


def test_leptomeningeal_involvement_is_universal_not_a_thirteen_percent_minority():
    assert p.MENINGEAL_ENHANCEMENT.value == 1.0
    assert p.CSF_PLEOCYTOSIS.value == 1.0
    lepto = next(o for o in p.OCCUPANCY if o.compartment is p.Compartment.LEPTOMENINGEAL)
    assert "NOT the" in lepto.note and "13%" in lepto.note


def test_surgery_removes_the_reachable_compartment_and_leaves_the_others():
    by_compartment = {o.compartment: o for o in p.OCCUPANCY}
    assert by_compartment[p.Compartment.INVADED_PARENCHYMA].what_surgery_does == "LEAVES IT"
    assert "does not reach" in by_compartment[p.Compartment.LEPTOMENINGEAL].what_surgery_does
    assert "removes" in by_compartment[p.Compartment.EXTRA_AXIAL].what_surgery_does
    assert "removes the compartment where drugs reach" in p.the_problem_in_one_line()


# --- the access numbers, and the fact that the favourable one was never measured -----------------

def test_no_extra_axial_access_measurement_exists_in_any_canine_tumour():
    joined = " ".join(p.EXTRA_AXIAL_ACCESS_HAS_NEVER_BEEN_MEASURED)
    assert "No brain:plasma or tumour:plasma drug concentration measurement exists" in joined
    assert "not meningioma" in joined
    assert "0.70" in joined


def test_no_occupied_compartment_carries_an_access_measurement():
    """Every access figure this project has used for the occupied compartments is assumed."""
    for o in p.OCCUPANCY:
        if o.occupied:
            assert o.access is None, o.compartment


def test_the_glioma_ratio_cannot_be_read_for_this_disease():
    with pytest.raises(ProvenanceError):
        p.CHLORAMBUCIL_GLIOMA_INTRATUMOURAL.value_for(p.BREED_PIHS)


def test_the_glioma_ratio_cannot_be_read_as_intact_barrier_access():
    assert p.CHLORAMBUCIL_GLIOMA_INTRATUMOURAL.population.barrier is BarrierState.DISRUPTED
    with pytest.raises(ProvenanceError):
        p.CHLORAMBUCIL_GLIOMA_INTRATUMOURAL.value_for(
            Population(Species.DOG, Disease.GLIOMA, agent="chlorambucil",
                       barrier=BarrierState.INTACT))


def test_the_only_intact_barrier_measurement_is_a_rat_and_the_wrong_drug():
    m = p.CHLORAMBUCIL_NORMAL_BRAIN
    assert m.population.species is Species.RAT
    assert m.population.agent == "chlorambucil"
    assert m.value == 0.021
    with pytest.raises(ProvenanceError):
        m.value_for(p.BREED_PIHS)


# --- the survival benchmarks --------------------------------------------------------------------

def test_the_measured_survival_benchmarks_are_short_and_sourced():
    assert p.MEDIAN_SURVIVAL_DEFINITIVE.value == 44
    assert p.MEDIAN_SURVIVAL_PALLIATIVE.value == 5
    for m in (p.MEDIAN_SURVIVAL_DEFINITIVE, p.MEDIAN_SURVIVAL_PALLIATIVE):
        assert m.quantity is Quantity.MEDIAN_SURVIVAL_DAYS
        assert "Toyoda" in m.source and m.n == 102


def test_survival_reads_for_the_breed_population_because_it_is_agent_independent():
    assert p.MEDIAN_SURVIVAL_DEFINITIVE.value_for(p.BREED_PIHS) == 44


# --- the scope note that caused the original error -----------------------------------------------

def test_ide_2011_is_recorded_as_a_location_descriptor_not_an_interface_claim():
    flat = " ".join(p.__doc__.split())   # the docstring wraps; the claim must not depend on that
    assert "LOCATION descriptor" in flat
    assert "abstract contains NO description of the tumour-brain interface" in flat
    assert "This project read \"focal solitary subdural\" as \"discrete, peelable, resectable" in flat


def test_the_module_does_not_overreach_into_choosing_a_therapy():
    joined = " ".join(p.WHAT_THIS_MODULE_DOES_NOT_DO)
    assert "does not choose a therapy" in joined
    assert "Hidari 2025" in joined and "39761568" in joined
