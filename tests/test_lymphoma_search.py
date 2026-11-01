"""Re-derives every table in `core.lymphoma_search` from the object model rather than pinning the
prose. Deterministic and fast -- no Monte Carlo here."""
import pytest

from canine_dsp.core.lymphoma_catalogue import (BURDEN_CLINICALLY_OBVIOUS, BURDEN_EARLY_DETECTED,
                                                BURDEN_MRD, CNS, ESCAPES, GROWTH_PER_DAY, SYSTEMIC,
                                                THE_FALSE_POSITIVE_THIS_FILE_CAUGHT, agents_for,
                                                venetoclax_potency_for)
from canine_dsp.core import lymphoma_search as S
from canine_dsp.core.regimen import Agent, Axis, Escape, Layer, Regimen, escape_presence_probability


# ---------- the derived-coverage rules ----------

def test_efflux_defeats_substrates_and_spares_non_substrates():
    pump = next(e for e in ESCAPES if "P-glycoprotein" in e.name)
    pool = {a.name: a for a in agents_for(SYSTEMIC, "B")}
    assert not pool["doxorubicin"].covers(pump)        # a P-gp substrate is pumped out
    assert not pool["vincristine"].covers(pump)
    assert pool["cyclophosphamide"].covers(pump)       # not a classical substrate
    # prednisolone's efflux-independence is the MEASURED fact (PMID 24975508)
    assert pool["prednisolone (glucocorticoid)"].covers(pump)


def test_a_tandem_construct_survives_losing_one_antigen_and_a_single_car_does_not():
    cd20_loss = next(e for e in ESCAPES if e.removes_antigen == "CD20")
    cd19_loss = next(e for e in ESCAPES if e.removes_antigen == "CD19")
    pool = {a.name: a for a in agents_for(SYSTEMIC, "B")}
    single, tandem = pool["CD20 CAR-T"], pool["tandem CD19/CD20 CAR-T"]
    assert not single.covers(cd20_loss)   # its only target is gone
    assert tandem.covers(cd20_loss)       # CD19 remains
    assert tandem.covers(cd19_loss)       # CD20 remains
    assert single.covers(cd19_loss)       # CD19 loss does not touch a CD20-directed CAR


def test_no_agent_gets_a_free_pass_against_an_escape_on_its_own_axis():
    for a in agents_for(SYSTEMIC, "B"):
        for e in ESCAPES:
            if e.axis is a.axis and e.antigen_intact and not e.effluxes_substrates:
                assert not a.covers(e), f"{a.name} should not cover own-axis {e.name}"


def test_division_gated_agents_never_reach_the_persister():
    persister = next(e for e in ESCAPES if not e.requires_division)
    for a in agents_for(SYSTEMIC, "B"):
        if a.division_gated:
            assert not a.reaches(persister), f"{a.name} is division-gated"
    # and at least one obtainable agent does reach it, or nothing could ever close
    assert any(a.reaches(persister) for a in agents_for(SYSTEMIC, "B", obtainable_only=True))


def test_serial_axis_block_covers_above_and_is_defeated_below():
    nfkb_escape = next(e for e in ESCAPES if e.axis is Axis.BCR_SIGNAL)
    btk = next(a for a in agents_for(SYSTEMIC, "B") if "acalabrutinib" in a.name)
    assert btk.layer < nfkb_escape.layer          # the lesion sits BELOW the block
    assert not btk.covers(nfkb_escape)            # so the block is defeated -- derived, not asserted


def test_effective_kill_is_potency_times_access_times_duty():
    a = Agent("x", Axis.CYTOTOXIC, Layer.RECEPTOR, 0.4, 0.5, 0.25, True)
    assert a.effective_kill == pytest.approx(0.05)


# ---------- the immunophenotype corrections ----------

def test_b_lineage_antigen_agents_are_unavailable_to_t_cell_disease():
    """The false positive this catalogue caught: a CD20 CAR has no target on a CD20-negative tumour."""
    names = {a.name for a in agents_for(SYSTEMIC, "T")}
    assert not any("CD20" in n or "CD19" in n for n in names)
    assert any("CD5/CD52" in n for n in names)   # the T-lineage arm exists in the model...
    assert not any("CD5/CD52" in a.name for a in agents_for(SYSTEMIC, "T", obtainable_only=True))
    assert THE_FALSE_POSITIVE_THIS_FILE_CAUGHT   # ...and is recorded as not obtainable


def test_venetoclax_potency_splits_by_immunophenotype_as_measured():
    assert venetoclax_potency_for("T") > 10 * venetoclax_potency_for("B")
    with pytest.raises(ValueError):
        venetoclax_potency_for("X")


# ---------- the searched regimens ----------

@pytest.mark.parametrize("compartment,phenotype", [(SYSTEMIC, "B"), (SYSTEMIC, "T"), (CNS, "B")])
def test_recorded_minimal_closing_regimens_are_reproduced(compartment, phenotype):
    recorded_name, recorded_n, recorded_margin = S.MINIMAL_CLOSING[(compartment, phenotype)]
    got = S.minimal_closing(compartment, phenotype, obtainable_only=True)
    assert got is not None
    worst, n, regimen = got
    assert n == recorded_n
    assert worst == pytest.approx(recorded_margin, abs=0.002)
    assert regimen.closes(ESCAPES, GROWTH_PER_DAY)


def test_the_cns_t_cell_cell_does_not_close_with_anything_obtainable():
    pool = list(agents_for(CNS, "T", obtainable_only=True))
    everything = Regimen("all obtainable", pool)
    assert not everything.closes(ESCAPES, GROWTH_PER_DAY)
    weakest = everything.weakest_link(ESCAPES, GROWTH_PER_DAY)
    assert not weakest.requires_division          # it is the persister that binds
    assert S.MINIMAL_CLOSING[(CNS, "T")][0] is None


def test_the_cns_t_cell_cell_closes_if_a_t_lineage_cellular_effector_exists():
    got = S.minimal_closing(CNS, "T", obtainable_only=False)
    assert got is not None
    _, _, regimen = got
    assert any("CD5/CD52" in a.name for a in regimen.agents)


@pytest.mark.parametrize("compartment,phenotype", [(SYSTEMIC, "B"), (SYSTEMIC, "T"), (CNS, "B")])
def test_recorded_most_robust_regimens_are_reproduced(compartment, phenotype):
    recorded = S.MOST_ROBUST[(compartment, phenotype)]
    rows = S.closing_combos(compartment, phenotype, obtainable_only=True, max_n=5)
    assert rows
    worst, _, regimen = rows[0]
    assert worst == pytest.approx(recorded["worst_margin"], abs=0.005)
    assert {a.name for a in regimen.agents} == set(recorded["agents"])
    assert regimen.weakest_link(ESCAPES, GROWTH_PER_DAY).name == recorded["weakest_link"]


def test_the_robust_systemic_regimen_still_includes_effluxed_drugs():
    """They earn their place against the other escapes even though the pump clone defeats them --
    the model must not throw a drug away for failing ONE escape."""
    recorded = S.MOST_ROBUST[(SYSTEMIC, "B")]["agents"]
    assert "doxorubicin" in recorded and "vincristine" in recorded


# ---------- the early-detection premise ----------

def test_escape_presence_rises_with_burden_and_is_bounded():
    e = ESCAPES[0]
    assert escape_presence_probability(e, 0) == pytest.approx(0.0)
    assert escape_presence_probability(e, BURDEN_CLINICALLY_OBVIOUS) == pytest.approx(1.0, abs=1e-6)
    early = escape_presence_probability(e, BURDEN_EARLY_DETECTED)
    assert 0.5 < early < 0.7
    assert escape_presence_probability(e, BURDEN_MRD) < 0.05
    with pytest.raises(ValueError):
        escape_presence_probability(e, -1)


def test_early_detection_removes_only_the_rare_mutational_escapes():
    present = S.escapes_at_burden(BURDEN_EARLY_DETECTED, 0.5)
    absent = [e.name for e in ESCAPES if e not in present]
    assert set(absent) == set(S.EARLY_DETECTION_RESULT["escapes_absent_at_1e8"])
    assert len(present) == S.EARLY_DETECTION_RESULT["escapes_to_close"]
    # the PHENOTYPIC escapes survive early detection -- that is the load-bearing caveat
    for e in present:
        if not e.requires_division:
            assert escape_presence_probability(e, BURDEN_EARLY_DETECTED) > 0.99


def test_early_detection_does_not_open_the_sanctuary():
    """The CNS answer is identical early and late, because the escapes that bind there are present
    at both burdens."""
    early = S.escapes_at_burden(BURDEN_EARLY_DETECTED, 0.5)
    assert S.minimal_closing(CNS, "T", obtainable_only=True, escapes=early) is None
    late_b = S.minimal_closing(CNS, "B", obtainable_only=True)
    early_b = S.minimal_closing(CNS, "B", obtainable_only=True, escapes=early)
    assert late_b is not None and early_b is not None
    assert early_b[1] == late_b[1]        # same number of agents needed


def test_the_fragile_single_agent_result_is_flagged_not_recommended():
    early = S.escapes_at_burden(BURDEN_EARLY_DETECTED, 0.5)
    got = S.minimal_closing(SYSTEMIC, "B", obtainable_only=True, escapes=early)
    assert got is not None and got[1] == 1          # the model really does return one agent
    assert "knife-edge" in S.EARLY_DETECTION_RESULT["THE_SINGLE_AGENT_RESULT_IS_FRAGILE"]


# ---------- honesty accounting ----------

def test_the_search_reports_how_many_potencies_are_assumed():
    _, _, regimen = S.minimal_closing(SYSTEMIC, "B", obtainable_only=True)
    assert regimen.assumed_inputs() == len(regimen.agents)   # all of them, and it says so
    # venetoclax is the one agent with a MEASURED potency anchor
    ven = next(a for a in agents_for(SYSTEMIC, "T") if a.name.startswith("venetoclax"))
    assert ven.potency_evidence != "ASSUMED"
