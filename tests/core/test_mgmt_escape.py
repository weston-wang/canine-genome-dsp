"""The eleventh escape: it breaks the temozolomide answer, and a lesion swap closes it."""

from __future__ import annotations

import pytest

from canine_dsp.core import durable_regimen as dr
from canine_dsp.core import mgmt_escape as mg
from canine_dsp.core import toxicity as tox
from canine_dsp.core.catalogue import GROWTH_PER_DAY, LEPTOMENINGEAL, PARENCHYMA

BOTH = (PARENCHYMA, LEPTOMENINGEAL)


def _tmz_agents(compartment):
    return dr.build(compartment).agents


# --- what MGMT does and does not defeat ---------------------------------------------------------------

@pytest.mark.parametrize("agent", ["temozolomide", "lomustine (nitrosourea)", "carmustine"])
def test_o6_alkylators_are_defeated(agent):
    assert mg.lesion_of(agent) is mg.Lesion.O6_ALKYLGUANINE
    assert mg.defeated_by_mgmt(agent)


@pytest.mark.parametrize("agent", ["carboplatin (intra-arterial)", "cisplatin", "radiation",
                                   "paxalisib", "liposomal clodronate", "anti-PD-1 (gilvetmab)"])
def test_everything_else_is_untouched(agent):
    assert not mg.defeated_by_mgmt(agent)


def test_being_chemotherapy_is_not_the_criterion():
    """Carboplatin and temozolomide are both cytotoxics. Only one is MGMT's substrate."""
    assert mg.defeated_by_mgmt("temozolomide")
    assert not mg.defeated_by_mgmt("carboplatin (intra-arterial)")
    assert mg.lesion_of("carboplatin") is mg.Lesion.N7_PLATINUM_CROSSLINK


def test_lomustine_is_defeated_and_it_is_the_standard_of_care():
    """An MGMT-competent tumour resists what this dog would be given anyway."""
    assert mg.defeated_by_mgmt("lomustine (nitrosourea)")
    joined = " ".join(mg.WHAT_THIS_MODULE_ESTABLISHES)
    assert "STANDARD OF CARE" in joined


# --- it breaks the current answer ---------------------------------------------------------------------

@pytest.mark.parametrize("compartment", BOTH)
def test_the_temozolomide_regimen_closes_only_if_mgmt_is_silenced(compartment):
    assert mg.worst_margin(_tmz_agents(compartment), mg.SILENCED) > 0


@pytest.mark.parametrize("compartment", BOTH)
def test_the_temozolomide_regimen_OPENS_under_competent_mgmt(compartment):
    assert mg.worst_margin(_tmz_agents(compartment), mg.COMPETENT) < 0


def test_both_sites_open_not_just_one():
    """The failure is not confined to the tighter compartment."""
    assert all(mg.worst_margin(_tmz_agents(c), mg.COMPETENT) < 0 for c in BOTH)


def test_the_breaking_point_is_below_the_measured_effect():
    """Measured canine effect is 4.3-4.9x. The regimen breaks between 2.0x and 2.5x."""
    par = PARENCHYMA
    assert mg.worst_margin(_tmz_agents(par), mg.MGMTState(True, 2.0)) > 0
    assert mg.worst_margin(_tmz_agents(par), mg.MGMTState(True, 2.5)) < 0
    assert mg.FOLD_RESISTANCE > 2.5


def test_the_sensitivity_table_is_re_derived():
    for fold, expected in mg.TEMOZOLOMIDE_BREAKS_AT.items():
        state = mg.SILENCED if fold == 1.0 else mg.MGMTState(True, fold)
        assert mg.worst_margin(_tmz_agents(PARENCHYMA), state) == pytest.approx(expected, abs=5e-4)


def test_the_measured_fold_resistance_is_conservative():
    """Both canine lines gave a larger effect than the figure used."""
    m = mg.CANINE_MGMT_LOMUSTINE
    assert mg.FOLD_RESISTANCE <= m["fold_resistance_conservative"]
    assert m["lines_with_mgmt_activity"] == 2 and m["lines_tested"] == 5


# --- the rescues that do not work ----------------------------------------------------------------------

def test_dose_dense_is_recorded_as_falsified_not_available():
    """It is already in the regimen at duty 1.0, so recording it as working would have been free."""
    d = mg.DOSE_DENSE_IS_FALSIFIED
    assert "FALSIFIED" in d["verdict"]
    assert "RTOG 0525" in d["the_evidence_against"]
    assert "NO BENEFIT BY METHYLATION STATUS" in d["the_evidence_against"]
    tmz = next(a for a in _tmz_agents(PARENCHYMA) if "temozolomide" in a.name)
    assert tmz.duty == 1.0, "the rescue really is already in the regimen"


def test_o6_benzylguanine_is_rejected_on_toxicity_not_mechanism():
    names = [a.name for a in _tmz_agents(PARENCHYMA)] + [dr.PROCEDURE, "O6-benzylguanine"]
    over = tox.oversubscribed([tox.PROFILES[n] for n in names])
    assert tox.Organ.MARROW in over
    assert over[tox.Organ.MARROW] == pytest.approx(1.85, abs=1e-9)
    assert "REJECTED ON THE TOXICITY AXIS" in mg.O6_BENZYLGUANINE_COLLIDES["verdict"]


def test_the_swap_alone_does_not_fit_either():
    """Carboplatin lands on the same pinned marrow axis, so the swap needs the free trade too."""
    names = [a.name for a in _tmz_agents(PARENCHYMA) if "temozolomide" not in a.name]
    names += [dr.PROCEDURE, "carboplatin (intra-arterial)"]
    over = tox.oversubscribed([tox.PROFILES[n] for n in names])
    assert over[tox.Organ.MARROW] == pytest.approx(1.05, abs=1e-9)


# --- the rescue that works ------------------------------------------------------------------------------

@pytest.mark.parametrize("compartment", BOTH)
def test_the_swap_closes_every_escape_under_competent_mgmt(compartment):
    assert mg.survives_mgmt(compartment)
    assert mg.worst_margin(mg.mgmt_proof(compartment).agents, mg.COMPETENT) > 0


@pytest.mark.parametrize("compartment", BOTH)
def test_the_answer_no_longer_depends_on_the_unknown(compartment):
    """The point of closing this escape: competent and silenced give the SAME margin."""
    agents = mg.mgmt_proof(compartment).agents
    assert mg.worst_margin(agents, mg.COMPETENT) == pytest.approx(
        mg.worst_margin(agents, mg.SILENCED), abs=1e-12)


def test_the_swap_recovers_the_original_margins_exactly():
    """It does not improve on the temozolomide answer -- it makes MGMT irrelevant to it."""
    for compartment, expected in ((PARENCHYMA, 0.0556), (LEPTOMENINGEAL, 0.0730)):
        assert mg.worst_margin(mg.mgmt_proof(compartment).agents, mg.COMPETENT) == pytest.approx(
            expected, abs=5e-5)


def test_the_swap_is_tolerable_with_more_headroom_than_before():
    names = [a.name for a in mg.mgmt_proof(PARENCHYMA).agents] + [dr.PROCEDURE]
    profiles = [tox.PROFILES[n] for n in names]
    assert tox.tolerable(profiles)
    assert tox.headroom(profiles) == pytest.approx(0.40, abs=1e-9)
    assert tox.headroom(profiles) > dr.headroom()


def test_the_two_dropped_agents_are_the_expected_ones():
    kept = {a.name for a in mg.mgmt_proof(PARENCHYMA).agents}
    assert "temozolomide" not in kept
    assert "hydroxychloroquine (autophagy)" not in kept
    assert "carboplatin (intra-arterial)" in kept


def test_the_swap_uses_the_route_already_costed():
    """No new delivery method is introduced -- that was the previous answer's failure mode."""
    carbo = next(a for a in mg.mgmt_proof(PARENCHYMA).agents if "carboplatin" in a.name)
    tmz = next(a for a in _tmz_agents(PARENCHYMA) if "temozolomide" in a.name)
    assert carbo.access == pytest.approx(tmz.access, abs=1e-12)
    assert "20023537" in mg.SWAP_THE_LESION["run_in_the_population_that_matters"]


def test_the_swap_still_fails_at_a_five_day_doubling():
    """It closes MGMT. It does not fix the growth-rate sensitivity, and must not claim to."""
    assert mg.survives_mgmt(PARENCHYMA, 0.693 / 7)
    assert not mg.survives_mgmt(PARENCHYMA, 0.693 / 5)


# --- provenance ------------------------------------------------------------------------------------------

def test_the_two_reference_classes_are_recorded_as_disagreeing():
    r = mg.REFERENCE_CLASSES_DISAGREE
    assert "UNKNOWN" in r["THE_HONEST_POSITION"]
    assert any("glioma" in k for k in r)
    assert any("soft tissue sarcoma" in k for k in r)


def test_neither_reference_class_is_silently_adopted():
    """Picking one would be the transfer error `evidence.Measurement` exists to block."""
    r = mg.REFERENCE_CLASSES_DISAGREE
    assert "wrong cell" in r["canine glioma -- FAVOURABLE"]["why_it_may_not_transfer"]
    assert "wrong species" in r["human soft tissue sarcoma -- UNFAVOURABLE"]["why_it_may_not_transfer"]


def test_the_platinum_independence_claim_is_bounded():
    """'MGMT-independent' is about direct reversal only, and the module must say so."""
    assert "DIRECT REVERSAL" in mg.SWAP_THE_LESION["THE_CAVEAT"]
    assert "homologous recombination" in mg.SWAP_THE_LESION["THE_CAVEAT"]


def test_growth_rate_is_the_shared_denominator():
    assert GROWTH_PER_DAY == 0.055
