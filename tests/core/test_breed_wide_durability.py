"""Breed-wide, all-presentations, ten-year durability via the lesion every case shares."""

from __future__ import annotations

import pytest

from canine_dsp.core import breed_wide_durability as bw
from canine_dsp.core import microtubule_route as mt
from canine_dsp.core import response_duration as rd
from canine_dsp.core import toxicity as tox
from canine_dsp.core.catalogue import ESCAPES, LEPTOMENINGEAL, PARENCHYMA

BOTH = (PARENCHYMA, LEPTOMENINGEAL)


# --- the shared lesion -------------------------------------------------------------------------------------

def test_the_lesion_is_the_most_recurrent_one_in_the_disease():
    s = bw.THE_SHARED_LESION
    assert "CDKN2A/B and MTAP" in s["what"]
    assert "MOST RECURRENT" in s["how_common"]
    assert "104" in s["how_common"]


def test_it_links_the_germline_predisposition_to_the_tumour_lesion():
    s = bw.THE_SHARED_LESION
    assert "SAME MTAP-CDKN2A locus" in s["germline_link"]
    assert "4 of 7" in s["germline_link"]


def test_one_target_satisfies_all_three_requirements():
    why = bw.THE_SHARED_LESION["WHY_IT_UNIFIES_THE_GOAL"]
    assert "breed-wide" in why
    assert "site-independent" in why
    assert "second primary" in why
    assert len(bw.BREED_PRESENTATIONS) == 3


# --- why it is a different kind of target ---------------------------------------------------------------------

def test_a_synthetic_lethal_agent_is_not_defeated_by_any_pathway_escape():
    """The escape catalogue lists ways to reroute a pathway. A deletion cannot be rerouted."""
    agent = bw.prmt5_agent()
    for escape in ESCAPES:
        if escape.requires_division is False:
            continue
        assert agent.covers(escape), f"{escape.name} must not defeat a genotype-directed agent"


def test_it_reaches_the_dormant_cell_directly_rather_than_at_re_entry():
    agent = bw.prmt5_agent()
    assert not agent.division_gated
    persister = next(e for e in ESCAPES if "persister" in e.name)
    assert agent.reaches(persister)


def test_the_reason_is_recorded_as_genotype_versus_pathway():
    joined = " ".join(bw.WHY_SYNTHETIC_LETHALITY_IS_A_DIFFERENT_KIND_OF_TARGET)
    assert "ATTACKS A GENOTYPE" in joined
    assert "RE-ACQUIRING A HOMOZYGOUSLY DELETED LOCUS" in joined


# --- induction ------------------------------------------------------------------------------------------------

@pytest.mark.parametrize("compartment", BOTH)
def test_induction_closes_every_escape(compartment):
    r = bw.induction(compartment)
    assert bw.induction_margin(compartment) > 0
    assert len(r.agents) == len(mt.build(compartment).agents) + 1


def test_induction_beats_the_previous_answer_at_every_access(compartment=PARENCHYMA):
    previous = mt.worst_margin(compartment, duty=0.8, access=1.0)
    for access in bw.ACCESS_SWEEP:
        assert bw.induction_margin(compartment, access) > previous


def test_the_access_sweep_is_re_derived():
    for access, (margin, days, maint, suppresses) in bw.BY_ACCESS.items():
        assert bw.induction_margin(PARENCHYMA, access) == pytest.approx(margin, abs=5e-4)
        assert bw.days_to_clear(PARENCHYMA, access) == pytest.approx(days, abs=2)
        assert bw.maintenance_margin(access) == pytest.approx(maint, abs=5e-4)
        assert bw.suppresses_second_primary(access) is suppresses


def test_clearance_is_faster_than_the_previous_answer():
    previous = rd.days_to_clear(mt.worst_margin(PARENCHYMA, duty=0.8, access=1.0))
    assert previous == pytest.approx(316, abs=3)
    for access in bw.ACCESS_SWEEP:
        assert bw.days_to_clear(PARENCHYMA, access) < previous


# --- maintenance: what ten years is actually made of -------------------------------------------------------------

def test_maintenance_alone_suppresses_above_the_access_threshold():
    assert bw.suppresses_second_primary(bw.MAINTENANCE_ACCESS_THRESHOLD)
    assert bw.suppresses_second_primary(0.80)


def test_maintenance_does_NOT_hold_at_conservative_access():
    """The honest hinge. At 0.30 the ten-year arm fails, and the module must not hide it."""
    assert bw.CONSERVATIVE_ACCESS == 0.30
    assert not bw.suppresses_second_primary(0.30)
    assert bw.maintenance_margin(0.30) < 0


def test_maintenance_is_what_the_ten_year_claim_rests_on():
    a = bw.THE_ARCHITECTURE
    assert "AT EMERGENCE" in a["what_maintenance_actually_is"]
    assert "NOT treating a tumour" in a["what_maintenance_actually_is"]


def test_maintenance_is_tolerable_enough_for_indefinite_dosing():
    profiles = bw.maintenance_profiles()
    assert tox.tolerable(profiles)
    assert tox.headroom(profiles) == pytest.approx(0.65, abs=1e-9)


def test_induction_is_tolerable_but_tighter():
    profiles = bw.induction_profiles(PARENCHYMA)
    assert tox.tolerable(profiles)
    assert tox.headroom(profiles) == pytest.approx(0.20, abs=1e-9)
    loads = tox.axis_loads(profiles)
    assert max(loads, key=loads.get) is tox.Organ.MARROW


def test_maintenance_has_far_more_headroom_than_induction():
    assert tox.headroom(bw.maintenance_profiles()) > tox.headroom(bw.induction_profiles(PARENCHYMA))


# --- the falsifier ------------------------------------------------------------------------------------------------

def test_the_single_decisive_test_is_named():
    joined = " ".join(bw.WHAT_WOULD_FALSIFY_IT)
    assert "MTAP-INTACT" in joined
    assert "immunohistochemistry" in joined
    assert "cheapest decisive test" in joined


def test_the_access_hinge_is_disclosed_as_a_falsifier_too():
    joined = " ".join(bw.WHAT_WOULD_FALSIFY_IT)
    assert "0.30 the maintenance arm does NOT hold" in joined


def test_the_secondary_loci_escape_is_admitted():
    """A second primary driven by another locus would be invisible to maintenance."""
    joined = " ".join(bw.WHAT_IS_STILL_ASSUMED)
    assert "secondary loci" in joined
    assert "maintenance would not see it" in joined


def test_recurrent_is_not_claimed_to_be_universal():
    joined = " ".join(bw.WHAT_IS_STILL_ASSUMED)
    assert "Recurrent is not universal" in joined


def test_the_selectivity_premise_is_flagged_as_load_bearing():
    joined = " ".join(bw.WHAT_IS_STILL_ASSUMED)
    assert "NO CANINE DATA" in joined
    assert "ordinal judgement" in joined
