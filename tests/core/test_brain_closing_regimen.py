"""The revised brain-closing regimen. Every number re-derived; every retraction pinned."""

from __future__ import annotations

from canine_dsp.core import brain_closing_regimen as bcr
from canine_dsp.core import tolerable_search as ts
from canine_dsp.core.catalogue import ESCAPES, GROWTH_PER_DAY, LEPTOMENINGEAL, PARENCHYMA, agents_in
from canine_dsp.core.regimen import Axis
from canine_dsp.core.toxicity import Organ, profile_for

MIN = bcr.MINIMUM_POTENCIES
KW = dict(parthenolide_potency=MIN["parthenolide"], statin_potency=MIN["statin"],
          hcq_potency=MIN["hydroxychloroquine"], clodronate_potency=MIN["clodronate"])


# --- the safety retraction, which is the most important thing in this file --------------------------

def test_the_reversibility_claim_is_retracted_everywhere():
    prof = profile_for("sulfasalazine")
    assert "PERMANENT" in prof.dose_limiting_event
    assert "RETRACTED" in prof.dose_limiting_event
    assert "2860750" in prof.source
    assert "reversible on withdrawal" not in prof.dose_limiting_event.lower().replace(
        "'reversible on withdrawal'", "")


def test_an_irreversible_toxicity_costs_more_budget():
    assert profile_for("sulfasalazine").budget_fraction == 0.85


def test_the_retraction_is_recorded_as_a_safety_claim_in_the_module():
    v = bcr.WHAT_VERIFICATION_DID_TO_THE_FIRST_VERSION
    assert "PERMANENT IN ALL BUT ONE CASE" in v["the_safety_claim_I_got_wrong"]
    assert "does not undo the injury" in v["the_safety_claim_I_got_wrong"]


def test_the_terminated_trial_is_recorded():
    v = bcr.WHAT_VERIFICATION_DID_TO_THE_FIRST_VERSION
    assert "ZERO clinical responses" in v["its_glioma_trial_was_terminated"]
    assert "10 of 10" in v["its_glioma_trial_was_terminated"]


def test_the_mechanism_is_separated_from_the_molecule():
    v = bcr.WHAT_VERIFICATION_DID_TO_THE_FIRST_VERSION
    assert "THE MECHANISM WORKS; THE MOLECULE IS THE WRONG VEHICLE" in v["and_one_favourable_finding"]


# --- the invented escape turned out to be real -------------------------------------------------------

def test_the_invented_escape_was_confirmed_by_the_literature():
    joined = " ".join(bcr.THE_INVENTED_ESCAPE_TURNED_OUT_TO_BE_REAL)
    assert "added a FERROPTOSIS-RESISTANCE escape for symmetry" in joined
    assert "IT IS REAL" in joined
    assert "40909720" in joined


def test_the_statin_is_chosen_because_it_covers_the_bypass():
    joined = " ".join(bcr.THE_INVENTED_ESCAPE_TURNED_OUT_TO_BE_REAL)
    assert "GPX4 BIOSYNTHESIS" in joined and "CoQ10" in joined
    statin = next(a for a in agents_in(PARENCHYMA) if "statin" in a.name)
    assert statin.axis is Axis.FERROPTOSIS
    assert statin.division_gated is False and statin.antigen_directed is False


# --- the revised agents ------------------------------------------------------------------------------

def test_hcq_is_the_only_agent_with_a_canine_phase_one():
    joined = " ".join(bcr.WHY_HCQ_REPLACES_SULFASALAZINE)
    assert "ONLY agent anywhere in this project with a CANINE PHASE I" in joined
    assert "100x PLASMA" in joined
    hcq = next(a for a in agents_in(PARENCHYMA) if "hydroxychloroquine" in a.name)
    assert hcq.obtainable is True and hcq.division_gated is False


def test_parthenolide_is_the_only_agent_with_data_in_the_right_species_and_disease():
    joined = " ".join(bcr.PARTHENOLIDE_HAS_DIRECT_CANINE_HS_DATA)
    assert "38135509" in joined
    assert "CELL LINES AND PRIMARY CELLS" in joined
    assert "GLUTATHIONE DEPLETION AND ROS" in joined


def test_every_arm_that_carries_a_persister_is_non_division_gated():
    pers = next(e for e in ESCAPES if "persister" in e.name)
    r = bcr.build(PARENCHYMA)
    carriers = [a for a in r.agents if a.reaches(pers)]
    assert carriers
    assert all(not a.division_gated for a in carriers)


def test_each_axis_specific_escape_is_uncovered_by_its_own_agent():
    r = bcr.build(PARENCHYMA)
    for agent_key, escape_key in (("parthenolide", "NF-kB-independence"),
                                  ("statin", "ferroptosis resistance"),
                                  ("hydroxychloroquine", "autophagy-independence")):
        agent = next(a for a in r.agents if agent_key in a.name)
        escape = next(e for e in ESCAPES if escape_key in e.name)
        assert not agent.covers(escape), agent_key


# --- the closure ---------------------------------------------------------------------------------------

def _worst_with_dormancy(comp):
    """The persister is priced by the corrected re-entry model, not the old binary exclusion."""
    from canine_dsp.core.dormancy import DormancyModel
    d = DormancyModel()
    r = bcr.build(comp, **KW)
    return min(d.margin(r, e, GROWTH_PER_DAY) if "persister" in e.name
               else r.effective_kill_against(e) - GROWTH_PER_DAY for e in ESCAPES)


def test_all_escapes_close_in_both_compartments_at_the_stated_minimum():
    for comp in (PARENCHYMA, LEPTOMENINGEAL):
        assert _worst_with_dormancy(comp) > 0, comp


def test_the_recorded_margins_are_reproducible():
    for comp, key in ((PARENCHYMA, "parenchyma"), (LEPTOMENINGEAL, "leptomeningeal")):
        assert abs(_worst_with_dormancy(comp) - bcr.MARGINS[key]) < 1e-3, comp


def test_the_asks_are_small_and_the_largest_is_clodronate():
    assert max(bcr.ASKS.values()) == bcr.ASKS["clodronate"] == 1.7
    assert bcr.ASKS["parthenolide"] == 1.0 and bcr.ASKS["hydroxychloroquine"] == 1.0


def test_the_regimen_is_tolerable():
    r = ts.regimen_toxicity(["parthenolide", "lipophilic statin", "hydroxychloroquine",
                             "liposomal clodronate", "radiation"], efflux_co_dose=True,
                            efflux_substrates=("parthenolide", "lipophilic statin"))
    assert r["tolerable"] is True
    assert abs(r["headroom"] - bcr.TOXICITY_HEADROOM) < 0.02
    assert r["derating"] == {}


def test_the_five_agents_sit_on_four_distinct_organ_axes():
    axes = {profile_for(n).axis for n in ("parthenolide", "lipophilic statin",
                                         "hydroxychloroquine", "liposomal clodronate", "radiation")}
    assert Organ.OCULAR not in axes, "no agent carrying a permanent injury"
    assert len(axes) >= 4


def test_it_still_degrades_with_growth_rate():
    import math
    from canine_dsp.core.dormancy import DormancyModel
    d = DormancyModel()
    r = bcr.build(PARENCHYMA, **KW)
    fast = math.log(2) / 5
    worst_fast = min(d.margin(r, e, fast) if "persister" in e.name
                     else r.effective_kill_against(e) - fast for e in ESCAPES)
    assert _worst_with_dormancy(PARENCHYMA) > 0
    assert worst_fast < 0, "it degrades, it just degrades gracefully"


# --- the limits ------------------------------------------------------------------------------------------

def test_the_single_most_important_caveat_is_first():
    assert "HAS EVER REACHED CLINICAL APPROVAL IN ANY SPECIES" in bcr.WHAT_STILL_SINKS_IT[0]
    assert "42284402" in bcr.WHAT_STILL_SINKS_IT[0]


def test_ferroptosis_has_never_been_studied_in_this_disease():
    joined = " ".join(bcr.WHAT_STILL_SINKS_IT)
    assert "NEVER BEEN STUDIED IN CANINE HISTIOCYTIC SARCOMA. Not once." in joined


def test_the_lineage_argument_is_recorded_as_pointing_against():
    joined = " ".join(bcr.WHAT_STILL_SINKS_IT)
    assert "ANTI-ferroptotic defences" in joined
    assert "ferroptosis-RESISTANT cell" in joined
    assert "cuts the OTHER way" in joined


def test_the_species_caveat_about_cell_death_wiring_is_kept():
    joined = " ".join(bcr.WHAT_STILL_SINKS_IT)
    assert "lack MLKL" in joined
    assert "PREPRINT" in joined


def test_the_position_does_not_overclaim():
    joined = " ".join(bcr.THE_POSITION)
    assert "CLOSES ALL TEN ESCAPES" in joined
    assert "NEVER PRODUCED AN APPROVED THERAPY" in joined
    assert "NEVER BEEN TESTED IN THIS DISEASE" in joined
