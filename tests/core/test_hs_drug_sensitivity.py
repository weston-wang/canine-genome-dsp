"""Measured in the right species and the right disease -- and it falsifies the carboplatin swap."""

from __future__ import annotations

import pytest

from canine_dsp.core import hs_drug_sensitivity as hs
from canine_dsp.core import mgmt_escape as mg
from canine_dsp.core.hs_drug_sensitivity import DrugClass


def test_the_alkylators_are_resistant_and_the_microtubule_agents_are_not():
    assert hs.BY_NAME["nimustine (ACNU)"].resistant
    assert hs.BY_NAME["melphalan"].resistant
    for drug in ("vincristine", "vinblastine", "paclitaxel"):
        assert not hs.BY_NAME[drug].resistant


def test_resistance_spans_the_class_not_just_mgmts_substrate():
    """The whole point. Both alkylator lesion types are resisted."""
    resistant = hs.resistant_classes()
    assert DrugClass.O6_ALKYLATOR in resistant
    assert DrugClass.N7_CROSSLINKER in resistant
    assert hs.sensitive_classes() == (DrugClass.MICROTUBULE,)


def test_the_o6_alkylator_resistance_dwarfs_the_mgmt_effect_size():
    """`mgmt_escape` models 4.3x. The measured class resistance is 134-670x."""
    lo, hi = hs.BY_NAME["nimustine (ACNU)"].fold_vs_comparator
    assert lo == pytest.approx(133.8, abs=0.5)
    assert hi == pytest.approx(670.1, abs=1.0)
    assert lo > mg.FOLD_RESISTANCE * 20


def test_the_n7_crosslinker_is_resisted_too_which_is_what_kills_the_swap():
    lo, hi = hs.BY_NAME["melphalan"].fold_vs_comparator
    assert lo == pytest.approx(42.1, abs=0.5)
    assert hi == pytest.approx(411.4, abs=1.0)
    assert lo > 1.0, "if this were <=1 the carboplatin swap would survive"


def test_the_absolute_concentrations_separate_by_orders_of_magnitude():
    """Ratios understate it. Only one of these is a concentration an animal can be held at."""
    alkylator_worst = hs.BY_NAME["nimustine (ACNU)"].hs_ic50_ng_ml[1]
    microtubule_best = hs.BY_NAME["vinblastine"].hs_ic50_ng_ml[0]
    assert alkylator_worst / microtubule_best > 1e5


@pytest.mark.parametrize("drug", ["vincristine", "vinblastine", "paclitaxel"])
def test_microtubule_agents_work_at_clinically_plausible_concentrations(drug):
    assert hs.BY_NAME[drug].hs_ic50_ng_ml[1] < 100.0


def test_vinblastine_and_paclitaxel_beat_the_chemosensitive_comparator():
    """HS is not merely 'not resistant' to these -- it is MORE sensitive than a lymphoma line."""
    for drug in ("vinblastine", "paclitaxel"):
        s = hs.BY_NAME[drug]
        assert s.hs_ic50_ng_ml[1] < s.comparator_ic50_ng_ml[0]


# --- what it does to the previous answer ---------------------------------------------------------------

def test_the_falsification_is_recorded_rather_than_quietly_dropped():
    f = hs.IT_FALSIFIES_THE_CARBOPLATIN_SWAP
    assert "N7 CROSSLINKER" in f["what_this_measurement_says"]
    assert "THE CHEMISTRY IS CORRECT" in f["what_mgmt_escape_argued"]
    assert "MEASUREMENT IN THE RIGHT SPECIES" in f["the_error_class"]


def test_the_residual_transfer_is_admitted():
    """Carboplatin itself was not tested. Melphalan -> carboplatin is still an inference."""
    assert "CARBOPLATIN ITSELF WAS NOT TESTED" in hs.IT_FALSIFIES_THE_CARBOPLATIN_SWAP[
        "the_residual_transfer"]


def test_the_delivery_half_is_explicitly_preserved():
    """The route is independent of what it carries -- that part of the work is not lost."""
    assert "DELIVERY" in hs.IT_FALSIFIES_THE_CARBOPLATIN_SWAP["what_survives"]
    assert "route" in hs.IT_FALSIFIES_THE_CARBOPLATIN_SWAP["what_survives"]


def test_the_mgmt_favourable_branch_is_now_the_less_likely_one():
    """These HS lines are NOT MGMT-silenced, which settles part of an open question."""
    note = hs.CANDIDATE_MECHANISMS_THE_PAPER_REPORTS["MGMT: no significant difference vs lymphoma"]
    assert "NOT MGMT-silenced" in note
    assert "UNKNOWN" in mg.REFERENCE_CLASSES_DISAGREE["THE_HONEST_POSITION"]


def test_mismatch_repair_loss_is_recorded_as_class_wide():
    """MSH6 loss explains why swapping alkylators does not help -- MMR is what makes O6 lethal."""
    note = hs.CANDIDATE_MECHANISMS_THE_PAPER_REPORTS["MSH6 significantly LOWER in HS lines"]
    assert "NOT FIXED BY CHANGING WHICH ALKYLATOR IS USED" in note


# --- the objections must not be dropped either -----------------------------------------------------------

def test_both_objections_to_microtubule_agents_are_recorded():
    o = hs.THE_TWO_OBJECTIONS_TO_MICROTUBULE_AGENTS
    assert "P-gp substrates" in o["EFFLUX"]
    assert "ABCB1/ABCG2 ELEVATED" in o["EFFLUX"]
    assert "division-gated" in o["DIVISION-GATED"].lower()


def test_the_division_gated_objection_is_consistent_with_the_dormancy_model():
    """A mitotic poison cannot reach a cell that has stopped dividing. The model already says so."""
    from canine_dsp.core.regimen import Agent, Axis, Layer
    from canine_dsp.core.catalogue import ESCAPES
    mitotic = Agent("vinblastine", Axis.CYTOTOXIC, Layer.RECEPTOR, 0.15, 0.5, 1.0, True,
                    division_gated=True)
    persister = next(e for e in ESCAPES if "persister" in e.name)
    assert persister.requires_division is False
    assert not mitotic.reaches(persister)


def test_the_breed_case_report_is_recorded_with_its_limits():
    c = hs.IT_EXPLAINS_THE_BREED_CASE_REPORT
    assert "THE PREDISPOSED BREED" in c["the_case"]
    assert "ANOTHER O6-ALKYLATOR" in c["WHY_IT_MATTERS"]
    assert "single dog" in c["what_it_does_NOT_show"]
    assert "195 days" in c["what_it_does_NOT_show"]


def test_the_provenance_is_the_strongest_in_the_project():
    assert "SPECIES: DOG" in hs.CITATION
    assert "DISEASE: HISTIOCYTIC SARCOMA" in hs.CITATION
    assert "25715778" in hs.CITATION


def test_the_limits_of_cell_culture_are_stated():
    doc = hs.__doc__
    assert "cell culture" in doc
    assert "cell lines drift" in doc
