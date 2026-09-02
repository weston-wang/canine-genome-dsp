"""Durable maintenance for every genotype, not only the MTAP-deleted one."""

from __future__ import annotations

import pytest

from canine_dsp.core import genotype_tiered_durability as gt
from canine_dsp.core import toxicity as tox
from canine_dsp.core.genotype_tiered_durability import AnchorKind, Grade


def test_every_genotype_tier_suppresses_a_second_primary_at_emergence():
    """The whole point: no genotype is left with 'clear it and hope'."""
    for t in gt.TIERS:
        assert gt.suppresses_at_emergence(t), t.genotype


def test_every_maintenance_anchor_is_tolerable_as_a_single_indefinite_agent():
    for t in gt.TIERS:
        assert gt.maintenance_tolerable(t), t.genotype


def test_the_mapk_majority_is_covered_and_is_the_case_the_mtap_answer_missed():
    """~59% of cases are MAPK-driven -- the branch the MTAP-only answer did nothing for."""
    mapk = next(t for t in gt.TIERS if "SHP2" in t.genotype)
    assert gt.suppresses_at_emergence(mapk)
    assert "mirdametinib" in mapk.anchor_agent
    assert mapk.brain_penetrant
    assert "59" in mapk.approx_frequency


def test_only_the_mtap_tier_is_genotype_locked():
    """Grades must be honest: exactly one tier is non-reroutable synthetic lethality."""
    locked = [t for t in gt.TIERS if t.kind is AnchorKind.SYNTHETIC_LETHAL]
    assert len(locked) == 1
    assert locked[0].genotype == "MTAP-deleted"
    assert locked[0].grade is Grade.STRONG


def test_the_mapk_tier_is_graded_medium_not_strong():
    """A reroutable pathway block must not be sold as a clean lock."""
    mapk = next(t for t in gt.TIERS if "SHP2" in t.genotype)
    assert mapk.kind is AnchorKind.PATHWAY_DRIVER
    assert mapk.grade is Grade.MEDIUM


def test_the_synthetic_lethal_anchor_holds_across_all_escapes():
    """MTAP/PRMT5 must suppress regardless of which escape a cell carries."""
    mtap = gt.TIERS[0]
    assert mtap.kind is AnchorKind.SYNTHETIC_LETHAL
    assert gt.suppresses_at_emergence(mtap)


def test_the_mek_anchor_kills_an_upstream_driver_but_not_at_its_own_layer():
    """A MEK block covers a SHP2/RAS founding lesion (above it), which is why emergence works."""
    from canine_dsp.core.regimen import Axis, Layer
    mapk = next(t for t in gt.TIERS if "SHP2" in t.genotype)
    agent = gt.anchor_agent(mapk)
    founding = gt.founding_escape(mapk)
    assert agent.axis is Axis.MAPK_SERIAL and agent.layer is Layer.MEK
    assert founding.layer < Layer.MEK, "founding driver must sit upstream of the MEK block"
    assert agent.covers(founding)


# --- routing ---------------------------------------------------------------------------------------------

def test_best_tier_prefers_the_strongest_available_anchor():
    assert gt.best_tier_for({"MTAP_del", "SHP2"}).genotype == "MTAP-deleted"      # locked beats driver
    assert gt.best_tier_for({"PTEN_del"}).genotype == "PTEN-deleted"
    assert gt.best_tier_for({"CDKN2A_del", "RB1_intact"}).genotype == "CDKN2A-deleted, RB1-intact"
    assert gt.best_tier_for({"SHP2"}).genotype == "PTPN11/SHP2 or KRAS driver"
    assert gt.best_tier_for({"KRAS"}).genotype == "PTPN11/SHP2 or KRAS driver"


def test_cdkn2a_without_intact_rb1_drops_to_the_floor():
    """CDK4/6 inhibition needs RB1; without it the tier is not available."""
    assert gt.best_tier_for({"CDKN2A_del"}).kind is AnchorKind.AGNOSTIC


def test_an_unknown_genotype_still_gets_the_floor_not_nothing():
    floor = gt.best_tier_for(set())
    assert floor.kind is AnchorKind.AGNOSTIC
    assert gt.suppresses_at_emergence(floor)


# --- honesty ---------------------------------------------------------------------------------------------

def test_induction_is_stated_as_genotype_agnostic():
    joined = " ".join(gt.EVERY_CASE_HAS_AN_ANCHOR)
    assert "genotype-agnostic" in joined
    assert "eleven escapes" in joined


def test_the_non_uniformity_is_stated_rather_than_hidden():
    joined = " ".join(gt.WHY_IT_IS_NOT_AS_CLEAN_AS_THE_MTAP_ARM)
    assert "genotype-LOCKED" in joined
    assert "not one uniform guarantee" in joined
    assert "over-reach" in joined


def test_the_tier_test_is_one_ngs_panel():
    joined = " ".join(gt.THE_ONE_TEST)
    assert "NGS panel" in joined
    assert "PTPN11" in joined and "MTAP" in joined


def test_the_frequencies_and_their_provenance_are_recorded():
    doc = gt.__doc__
    assert "56%" in doc and "3%" in doc
    assert "recurrent minority" in doc


def test_every_named_anchor_has_a_toxicity_profile():
    """A maintenance agent with no priced toxicity would be silently free for years of dosing."""
    for t in gt.TIERS:
        if t.kind is AnchorKind.AGNOSTIC:
            continue  # the floor is a strategy (immune + cycled), priced in its own modules
        assert t.anchor_agent in tox.PROFILES, t.anchor_agent


# --- consistency with the early MAPK work (the user's challenge) ------------------------------------------

def test_the_mapk_tier_credits_the_early_work_rather_than_claiming_discovery():
    joined = " ".join(gt.EARLY_WORK_ALREADY_ESTABLISHED)
    assert "NOT A NEW DISCOVERY" in joined
    assert "answer" in joined and "four_cells" in joined and "trametinib_direct_evidence" in joined
    assert "GENUINELY NEW" in joined


def test_mapk_maintenance_is_site_split_not_uniform():
    """The early four-cell work: MEK closes lung, fails in brain on access. Must be preserved."""
    d = gt.MAPK_MAINTENANCE_BY_SITE
    assert "SOLID" in d["lung / disseminated second primary"]
    assert "0.973" in d["lung / disseminated second primary"]
    assert "CONDITIONAL" in d["brain second primary"]
    assert "UNQUANTIFIED" in d["brain second primary"] or "not a mirdametinib figure" in d["brain second primary"]


def test_the_brain_mapk_access_is_flagged_as_unmeasured_not_asserted():
    """The model's 0.50 is the maintenance threshold, not a measured mirdametinib canine figure."""
    assert "0.50" in gt.MAPK_MAINTENANCE_BY_SITE["brain second primary"]
    assert "threshold" in gt.MAPK_MAINTENANCE_BY_SITE["brain second primary"].lower()
