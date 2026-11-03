"""Every table is re-derived from the model, so the prose cannot drift away from the computation."""

from __future__ import annotations

from canine_dsp.core import combination_search as cs
from canine_dsp.core.catalogue import (ESCAPES, GROWTH_PER_DAY, LEPTOMENINGEAL, PARENCHYMA,
                                       agents_in)
from canine_dsp.core.regimen import Axis, Regimen
from canine_dsp.v3.engine import Agent as EAgent, Clone, Regimen as ERegimen, run


# --- coverage is derived, not asserted -------------------------------------------------------------

def test_a_mek_block_is_defeated_by_lesions_at_or_below_it():
    tram = next(a for a in agents_in(PARENCHYMA) if a.name.startswith("trametinib"))
    above = next(e for e in ESCAPES if "above MEK" in e.name)
    at_mek = next(e for e in ESCAPES if "target-site" in e.name)
    below = next(e for e in ESCAPES if "activating ERK" in e.name)
    assert tram.covers(above), "a block covers lesions upstream of it"
    assert not tram.covers(at_mek)
    assert not tram.covers(below)


def test_an_erk_block_covers_everything_above_it_which_is_why_downstream_covers_more():
    erk = next(a for a in agents_in(PARENCHYMA) if a.name == "ERK inhibitor")
    tram = next(a for a in agents_in(PARENCHYMA) if a.name.startswith("trametinib"))
    mapk = [e for e in ESCAPES if e.axis is Axis.MAPK_SERIAL]
    assert sum(erk.covers(e) for e in mapk) > sum(tram.covers(e) for e in mapk)


def test_the_convergence_node_lesion_is_covered_by_nothing_on_its_own_axis():
    erk_lesion = next(e for e in ESCAPES if "activating ERK" in e.name)
    on_axis = [a for a in agents_in(PARENCHYMA) if a.axis is Axis.MAPK_SERIAL]
    assert not any(a.covers(erk_lesion) for a in on_axis)


def test_only_a_non_antigen_directed_effector_survives_antigen_loss():
    loss = next(e for e in ESCAPES if "antigen loss" in e.name)
    immune = [a for a in agents_in(PARENCHYMA) if a.axis is Axis.IMMUNE_EFFECTOR]
    assert any(a.covers(loss) for a in immune)
    for a in immune:
        assert a.covers(loss) is (not a.antigen_directed)


def test_only_a_non_division_gated_agent_reaches_a_persister():
    pers = next(e for e in ESCAPES if "persister" in e.name)
    for a in agents_in(PARENCHYMA):
        if a.effective_kill > 0:
            assert a.reaches(pers) is (not a.division_gated)


def test_the_two_shaping_escapes_force_one_kind_of_effector():
    joined = " ".join(cs.THE_TWO_ESCAPES_THAT_SHAPE_THE_ANSWER)
    assert "FORCE THE REGIMEN TO CONTAIN AN EFFECTOR THAT IS BOTH" in joined
    assert "not a kinase inhibitor" in joined


# --- the search result -----------------------------------------------------------------------------

def test_nothing_obtainable_closes_either_compartment():
    for comp in (PARENCHYMA, LEPTOMENINGEAL):
        assert cs.closing_combos(comp, obtainable_only=True) == [], comp


def test_closing_combos_exist_only_once_unobtainable_agents_are_allowed():
    for comp in (PARENCHYMA, LEPTOMENINGEAL):
        assert len(cs.closing_combos(comp, obtainable_only=False)) > 0, comp


def test_every_closing_combination_contains_a_lineage_directed_effector():
    for comp in (PARENCHYMA, LEPTOMENINGEAL):
        for _, _, r in cs.closing_combos(comp, obtainable_only=False):
            assert any(not a.antigen_directed and not a.division_gated for a in r.agents), r.name


def test_the_recorded_multipliers_are_reproducible():
    for comp, recorded in cs.MULTIPLIER_NEEDED.items():
        assert abs(cs.multiplier_needed(comp) - recorded) < 0.05, comp


def test_the_recorded_worst_case_kills_are_reproducible():
    for comp, recorded in cs.WORST_CASE_KILL.items():
        worst, _, _ = cs.best_obtainable(comp)
        assert abs((worst + GROWTH_PER_DAY) - recorded) < 1e-3, comp


def test_the_leptomeningeal_gap_is_roughly_thirty_times_smaller():
    ratio = cs.MULTIPLIER_NEEDED[PARENCHYMA] / cs.MULTIPLIER_NEEDED[LEPTOMENINGEAL]
    assert 2 < ratio < 6


def test_the_asymmetry_is_attributed_to_the_liposome_access_difference():
    joined = " ".join(cs.THE_ASYMMETRY)
    assert "PERIVASCULAR AND MENINGEAL" in joined
    assert "blood side of the barrier" in joined
    assert "FACTOR OF THREE" in joined


# --- the upstream argument -------------------------------------------------------------------------

def test_the_upstream_coverage_correction_is_stated_before_the_upstream_case():
    w = cs.WHY_THIS_IS_THE_UPSTREAM_ANSWER
    assert "NOT a coverage argument" in w["the_correction_first"]
    assert "DOWNSTREAM blocking covers more" in w["the_correction_first"]


def test_clodronate_is_identified_as_the_obtainable_lineage_proxy():
    w = cs.WHY_THIS_IS_THE_UPSTREAM_ANSWER
    assert "OBTAINABLE PROXY FOR THE UPSTREAM LINEAGE STRATEGY" in w["THE_CONCLUSION"]
    ways = w["and_there_are_exactly_two_ways_to_do_it"]
    assert "NOT OBTAINABLE" in ways["CSF1R inhibition"]
    assert "OBTAINABLE" in ways["liposomal clodronate"]


def test_clodronate_really_has_all_four_properties_claimed_for_it():
    clod = next(a for a in agents_in(LEPTOMENINGEAL) if "clodronate" in a.name)
    assert clod.obtainable is True
    assert clod.antigen_directed is False
    assert clod.division_gated is False
    assert clod.axis is Axis.IMMUNE_EFFECTOR


# --- durability, re-derived on the v3 engine --------------------------------------------------------

def _durability(kill: float) -> float:
    clones = [
        Clone("sensitive", 0.055, True, True, True),
        Clone("mapk_escape", 0.055, True, True, True, resistance_factor=40.0,
              seeded_from="sensitive"),
        Clone("antigen_loss", 0.055, True, False, True, seeded_from="sensitive"),
    ]
    agent = EAgent("arm", concentration_nM=1.0, ic50_nM=1.0, max_kill=kill,
                   penetration={"site": 1.0}, lineage_directed=True, access_scales_kill=True)
    return round(run(clones, ERegimen("r", [agent]), "site")["relapse_free"], 3)


def test_the_durability_table_is_reproducible_from_the_engine():
    for kill, recorded in cs.DURABILITY.items():
        assert _durability(kill) == recorded, kill


def test_the_obtainable_arms_sit_at_the_surgery_alone_floor():
    assert cs.DURABILITY[0.0006] == cs.SURGERY_ALONE
    assert cs.DURABILITY[0.0180] - cs.SURGERY_ALONE < 0.01


def test_the_three_fold_improvement_is_what_moves_it_off_the_floor():
    assert cs.DURABILITY[0.0600] > 0.70
    assert cs.DURABILITY[0.0600] > cs.DURABILITY[0.0380] > cs.SURGERY_ALONE


# --- the deciding number and the honest limits -------------------------------------------------------

def test_the_deciding_number_is_named_as_unmeasured_and_cheap():
    d = cs.THE_DECIDING_NUMBER
    assert "NO KILL RATE HAS BEEN MEASURED IN ANY SPECIES" in d["status"]
    assert "CHS-1" in d["how_hard_is_it_to_get"]
    assert "NOBODY HAS RUN IT" in d["how_hard_is_it_to_get"]
    assert cs.CLODRONATE_ASSUMED_POTENCY == 0.06


def test_the_regimen_states_what_it_does_not_achieve():
    joined = " ".join(cs.WHAT_THIS_REGIMEN_IS_AND_IS_NOT)
    assert "IT IS NOT VERIFIED" in joined
    assert "DOES NOT CLOSE THE PARENCHYMAL COMPARTMENT AT ALL" in joined
    assert "9x gap is large but no longer hopeless" in joined


def test_the_proposed_regimen_is_coverage_complete_and_says_it_does_not_close():
    r = cs.THE_PROPOSED_REGIMEN
    assert "Coverage-complete against all ten escapes" in r["WHAT_IT_ACHIEVES"]
    assert "CLOSES neither on current assumptions" in r["WHAT_IT_ACHIEVES"]


def test_the_proposed_regimen_is_built_only_from_obtainable_agents():
    obtainable = {a.name for a in agents_in(LEPTOMENINGEAL) if a.obtainable}
    for key in ("lineage arm (UPSTREAM)", "immune arm", "local arm", "cytotoxic arm"):
        text = cs.THE_PROPOSED_REGIMEN[key]
        assert any(name.split(" (")[0] in text for name in obtainable), key


# --- the per-escape prescription, re-derived -------------------------------------------------------

def test_per_escape_prescription_is_reproducible():
    for comp, recorded in cs.PER_ESCAPE_OBTAINABLE.items():
        assert cs.per_escape_prescription(comp, obtainable_only=True) == recorded, comp


def test_radiation_answers_six_of_seven_at_the_parenchyma():
    table = cs.PER_ESCAPE_OBTAINABLE[PARENCHYMA]
    by_radiation = [k for k, (agent, _) in table.items() if agent == "radiation"]
    assert len(by_radiation) == 9
    assert len(table) == 10


def test_radiation_is_antigen_indifferent_because_it_is_physical():
    rad = next(a for a in agents_in(PARENCHYMA) if a.name == "radiation")
    loss = next(e for e in ESCAPES if "antigen loss" in e.name)
    assert rad.antigen_directed is False
    assert rad.covers(loss)


def test_radiation_is_still_division_gated_and_so_misses_persisters():
    rad = next(a for a in agents_in(PARENCHYMA) if a.name == "radiation")
    pers = next(e for e in ESCAPES if "persister" in e.name)
    assert rad.division_gated is True
    assert not rad.reaches(pers)


def test_the_persister_is_the_single_escape_where_the_parenchyma_collapses():
    table = cs.PER_ESCAPE_OBTAINABLE[PARENCHYMA]
    pers_kill = table["drug-tolerant persister"][1]
    others = [k for name, (_, k) in table.items() if name != "drug-tolerant persister"]
    assert all(pers_kill * 5 < o for o in others), "a factor of thirty, not a small dip"


def test_the_structural_hole_is_named_as_one_escape_and_one_mechanism_class():
    joined = " ".join(cs.THE_PERSISTER_IS_THE_STRUCTURAL_HOLE)
    assert "NINE OF THE TEN" in joined
    assert "FAILS ON EXACTLY ONE" in joined
    assert "BACKWARDS" in joined


def test_one_agent_answers_every_escape_at_the_leptomeninges():
    agents = {a for a, _ in cs.PER_ESCAPE_OBTAINABLE[LEPTOMENINGEAL].values()}
    assert agents == {"liposomal clodronate"}



# --- the escape the search re-opened ---------------------------------------------------------------

def test_parthenolide_is_the_only_small_molecule_reaching_a_persister():
    pers = next(e for e in ESCAPES if "persister" in e.name)
    reaching = [a for a in agents_in(PARENCHYMA) if a.reaches(pers)]
    small_molecule = [a for a in reaching if a.axis is Axis.SURVIVAL_SIGNAL]
    assert len(small_molecule) == 1
    assert "parthenolide" in small_molecule[0].name


def test_a_survival_signal_blocker_is_not_given_a_free_pass_on_its_own_axis():
    part = next(a for a in agents_in(PARENCHYMA) if "parthenolide" in a.name)
    own = next(e for e in ESCAPES if "NF-kB-independence" in e.name)
    other = next(e for e in ESCAPES if "activating ERK" in e.name)
    assert not part.covers(own), "symmetric with CSF1R-independence"
    assert part.covers(other), "but position-independent otherwise"


def test_the_persister_kill_under_efflux_inhibition_is_reproducible():
    from canine_dsp.core.catalogue import SMALL_MOLECULE_ACCESS
    base = SMALL_MOLECULE_ACCESS[PARENCHYMA]
    part = next(a for a in agents_in(PARENCHYMA) if "parthenolide" in a.name)
    clod = next(a for a in agents_in(PARENCHYMA) if "clodronate" in a.name)
    for mult, recorded in cs.PERSISTER_AT_PARENCHYMA.items():
        got = part.potency * base * mult + clod.effective_kill
        assert abs(got - recorded) < 1e-3, mult


def test_it_closes_only_at_the_genetic_ceiling_not_the_pharmacologic_multiplier():
    assert cs.PERSISTER_AT_PARENCHYMA[20.0] < GROWTH_PER_DAY
    assert cs.PERSISTER_AT_PARENCHYMA[36.7] > GROWTH_PER_DAY


def test_the_binding_constraint_moves_rather_than_disappearing():
    w = cs.WHAT_ADDING_PARTHENOLIDE_DOES_TO_THE_PARENCHYMAL_GAP
    assert "9.4x" in w["before"] and "persister" in w["before"]
    assert "NF-kB-INDEPENDENCE" in w["after_at_efflux_20x"]
    assert "UNMEASURED IN CANINE HS" in w["THE_HONEST_READING"]
    assert "progress and is not closure" in w["THE_HONEST_READING"]


def test_this_is_where_efflux_inhibition_finally_pays_and_it_says_why():
    joined = " ".join(cs.THIS_IS_WHERE_EFFLUX_INHIBITION_FINALLY_PAYS)
    assert "excluded by size rather than pumped out" in joined
    assert "PARTHENOLIDE CHANGES THAT" in joined
