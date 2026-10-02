"""The widened universe: audit escapes and sweep agents (core/lymphoma_universe.py)."""

import pytest

from canine_dsp.core import lymphoma_grounded as G
from canine_dsp.core import lymphoma_universe as U
from canine_dsp.core.lymphoma_catalogue import CNS, SYSTEMIC


def _ag(comp, ip):
    return {a.name: a for a in G.grounded_agents(comp, ip)}


def _esc(prefix):
    return next(e for e in U.UNIVERSE_ESCAPES if e.name.startswith(prefix))


def test_full_escape_set_is_the_fourteen_plus_the_audits_nine():
    assert len(G.GROUNDED_ESCAPES) == 14
    assert len(G.FULL_ESCAPES) == 23
    assert len({e.name for e in G.FULL_ESCAPES}) == 23


@pytest.mark.parametrize("escape, agent, ip", [
    ("E1", "prednisolone (glucocorticoid)", "B"),
    ("E2", "cytarabine CRI (q7d)", "B"),
    ("E3", "doxorubicin", "B"),
    ("E4", "venetoclax (BCL2 inhibitor)", "T"),
    ("E8", "verdinexor (XPO1 inhibitor)", "B"),
    ("E9", "high-dose methotrexate", "B"),
    ("E7", "anti-CD20 monoclonal antibody", "B"),
    ("E10", "anti-CD20 monoclonal antibody", "B"),
])
def test_each_new_escape_defeats_exactly_its_named_agent_and_not_the_others(escape, agent, ip):
    ag = _ag(SYSTEMIC, ip)
    e = _esc(escape)
    assert not ag[agent].covers(e)
    survivors = [a for n, a in ag.items() if n != agent and not (a.vulnerable_to & e.defeats)]
    assert survivors, "an escape that defeats every agent would be a modelling bug"
    assert any(a.covers(e) for a in survivors)


def test_tagging_leaves_the_fourteen_escape_results_unchanged():
    """Adding vulnerability tags must not move any result against the original escapes."""
    r = [a for a in G.grounded_agents(SYSTEMIC, "B")
         if a.name.split(" (")[0] in ("hydroxychloroquine", "verdinexor")]
    ev = G.evaluate(r, G.GROUNDED_ESCAPES)
    assert ev.worst_derated == pytest.approx(0.185, abs=0.01)


def test_e5_conjunction_is_reached_only_by_nongated_nonsubstrate_agents():
    e5 = _esc("E5")
    assert e5.requires_division is False and e5.effluxes_substrates
    ag = _ag(SYSTEMIC, "B")
    reaching = {n for n, a in ag.items() if a.reaches(e5)}
    assert "prednisolone (glucocorticoid)" in reaching
    assert "anti-CD20 monoclonal antibody" in reaching
    for n in ("doxorubicin", "hydroxychloroquine (autophagy)", "verdinexor (XPO1 inhibitor)",
              "venetoclax (BCL2 inhibitor)"):
        assert n not in reaching


def test_old_closing_programs_do_not_survive_the_audit_widened_escape_set():
    """The honest consequence of the audit: the earlier four-part B-cell program is not closed once the
    quiescent efflux-high progenitor is counted (model result, not an observation in dogs)."""
    ip, names = "B", ("hydroxychloroquine", "verdinexor", "continuous intrathecal", "anti-CD20")
    ag = _ag(SYSTEMIC, ip)
    reg = [next(a for k, a in ag.items() if k.startswith(n)) for n in names if any(k.startswith(n) for k in ag)]
    esc = tuple(e for e in G.FULL_ESCAPES if e.removes_antigen != "CD7")
    ev = G.evaluate_best_schedule(reg, esc, compartment=SYSTEMIC)
    assert not (ev.closes and ev.horizon_strict.cure_inside_window)


def test_vaccine_and_tcell_addback_are_outcome_graded_with_the_stated_rule():
    assert U.outcome_kill(1.0) == pytest.approx(0.0)
    assert U.outcome_kill(2.55) == pytest.approx(0.0903 * (1 - 1 / 2.55))
    ag = _ag(SYSTEMIC, "B")
    for n in ("autologous tumour vaccine (APAVAC-type, HSPPC + hydroxyapatite)",
              "autologous T-cell add-back after chemotherapy"):
        assert G.potency_grade(ag[n]) == "OUTCOME"
        assert ag[n].division_gated and "antigen_presentation" in ag[n].vulnerable_to
        assert not ag[n].antigen_targets          # independent of CD20/CD19 loss
    assert _ag(CNS, "B")["autologous T-cell add-back after chemotherapy"].access == 0.0


def test_vaccine_gives_no_credit_against_persisters():
    ag = _ag(SYSTEMIC, "B")
    persister = G.PERSISTER
    assert not ag["autologous tumour vaccine (APAVAC-type, HSPPC + hydroxyapatite)"].reaches(persister)


def test_antiPD1_is_regraded_measured_negative():
    a = _ag(SYSTEMIC, "B")["anti-PD-1 / anti-PD-L1 checkpoint blockade"]
    assert a.potency == 0.0
    assert G.potency_grade(a) == "MEASURED-NEGATIVE"
    assert a not in G.sound_pool([a])


# ---- brain-closing candidates -------------------------------------------------------------------------------
from dataclasses import replace  # noqa: E402

_IT = "intraventricular/intrathecal"


def _brain_set(ip, names, duty):
    pool = G.grounded_agents(CNS, ip)
    out = []
    for n in names:
        a = next(a for a in pool if a.name.startswith(n))
        if _IT in a.name and "CAR-T" in a.name:
            a = replace(a, duty=duty)
        out.append(a)
    return out


def _brain_esc(ip):
    return tuple(e for e in G.FULL_ESCAPES
                 if not (ip == "T" and e.removes_antigen in ("CD19", "CD20"))
                 and not (ip == "B" and e.removes_antigen == "CD7"))


def test_spinal_fluid_antibody_is_b_cell_only_and_brain_only():
    assert not any(_IT in a.name for a in G.grounded_agents(SYSTEMIC, "B"))
    assert not any("anti-CD20" in a.name and _IT in a.name for a in G.grounded_agents(CNS, "T"))
    b = [a for a in G.grounded_agents(CNS, "B") if _IT in a.name]
    assert {G.potency_grade(a) for a in b} == {"TRANSFER", "TRANSFER-OUTCOME"}


def test_brain_closes_in_the_model_only_if_the_spinal_fluid_cart_lasts_long_enough():
    """The result the brain claim rests on: closure needs the intrathecal CAR-T active in the CSF for roughly a third or
    more of each dosing interval. At a duty of 0.1 it does not clear."""
    for ip, names in (("B", ("hydroxychloroquine", "continuous intrathecal", "persistence-engineered",
                             "tandem CD19/CD20 CAR-T, intra")),
                      ("T", ("hydroxychloroquine", "continuous intrathecal", "CD7-directed CAR-T (canine",
                             "CD7-directed CAR-T, intra"))):
        esc = _brain_esc(ip)
        assert not G.clears(_brain_set(ip, names, 0.1), esc, compartment=CNS)
        assert G.clears(_brain_set(ip, names, 1.0), esc, compartment=CNS)
        # and it is NOT robust: halving every potency breaks it even at full duty
        assert not G.clears(G.discounted(_brain_set(ip, names, 1.0), 0.5), esc, compartment=CNS)


def test_thiotepa_is_gated_but_not_a_pump_substrate_by_default():
    """Division-gating stays conservative (dormant-cell kill not shown); the pump-substrate default was dropped because the
    MDR1-overexpressing line shows no cross-resistance (GI50 1.07x parent)."""
    t = next(a for a in G.grounded_agents(CNS, "B") if a.name.startswith("high-dose thiotepa"))
    assert t.division_gated and not t.efflux_substrate and G.potency_grade(t) == "OUTCOME"
    assert "high-dose thiotepa-based consolidation with autologous stem-cell rescue [human regimen]" in G.COURSE_AGENTS


def test_joint_b_cell_program_is_model_robust_only_at_the_human_grounded_central_inputs():
    from canine_dsp.lymphoma_joint import B_PROGRAMS, CENTRAL, LOW, joint_report
    names = B_PROGRAMS["B-cell, 7 agents"]
    central = joint_report("B", names, **CENTRAL)
    assert central["clears"] and central["halved_clears"] and central["any_one_removed_clears"]
    low = joint_report("B", names, **LOW)
    assert not low["any_one_removed_clears"], "at the low kill and duty the program is not fault tolerant"


def test_escape_confirmation_matrix_every_row_closed_with_three_covering_agents():
    from canine_dsp.lymphoma_joint import B_PROGRAMS, T_PROGRAMS, escape_matrix
    for ip, names, n_rows in (("B", B_PROGRAMS["B-cell, 7 agents"], 44), ("T", T_PROGRAMS["T-cell, 5 agents"], 42)):
        rows = escape_matrix(ip, names)
        assert len(rows) == n_rows          # 22 or 21 escapes x 2 compartments (the antigen set differs by lineage)
        assert all(r["closed"] for r in rows), [r["escape"] for r in rows if not r["closed"]]
        assert min(r["n_cover"] for r in rows) >= 3


def test_existing_agent_programs_close_the_b_cell_body_and_leave_exactly_the_named_gaps():
    """Programs built only from agents that exist today (docs/LYMPHOMA_UNIVERSE.md section F)."""
    from canine_dsp.core.lymphoma_catalogue import CNS as _CNS, SYSTEMIC as _SYS
    from canine_dsp.lymphoma_joint import EXISTING_PROGRAMS, clock_table
    b = clock_table("B", EXISTING_PROGRAMS["B"])
    assert b[_SYS]["clears"]
    open_b = [k for k, v in b[_CNS]["lineages"].items() if v[0] != "cleared"]
    assert open_b == ["E5 quiescent efflux-high lymphoid progenitor"]
    t = clock_table("T", EXISTING_PROGRAMS["T"])
    open_t = [k for k, v in t[_SYS]["lineages"].items() if v[0] != "cleared"]
    assert open_t == ["E5 quiescent efflux-high lymphoid progenitor"]
    assert not t[_CNS]["clears"]


def test_reassessed_classes_are_in_the_model_at_outcome_or_transfer_grade():
    ag = _ag(SYSTEMIC, "B")
    assert G.potency_grade(ag["allogeneic DLA-identical HCT (graft-versus-lymphoma)"]) == "OUTCOME"
    assert G.potency_grade(ag["dTERT genetic vaccine (Tel-eVax-type)"]) == "OUTCOME"
    assert G.potency_grade(ag["CD3xCD20 bispecific T-cell engager (canine-specific) [needs development]"]) == "TRANSFER-OUTCOME"
    assert G.AVAILABILITY["allogeneic DLA-identical HCT (graft-versus-lymphoma)"] != G.NONE
    assert G.AVAILABILITY["CD3xCD20 bispecific T-cell engager (canine-specific) [needs development]"] == G.NONE


# --- near-future programs (/goal 2026-10-02) ---------------------------------------------------------------------------------

def test_near_future_programs_close_body_and_brain_even_at_the_pessimistic_inputs():
    """B- and T-cell programs built from exists-today and clinical-stage agents clear every escape in both compartments at the LOW
    CAR-T inputs, and no single agent is load-bearing; at the central inputs they also survive halving every potency."""
    from canine_dsp.lymphoma_joint import CENTRAL, LOW, NEAR_FUTURE_PROGRAMS, escape_matrix, joint_report, tier_mix
    for ip, n_rows, n_cover in (("B", 44, 4), ("T", 42, 5)):
        prog = NEAR_FUTURE_PROGRAMS[ip]
        assert tier_mix(prog)["admissible"]
        low = joint_report(ip, prog, **LOW)
        assert low["clears"] and low["any_one_removed_clears"], (ip, low["removal_breaks"])
        cen = joint_report(ip, prog, **CENTRAL)
        assert cen["clears"] and cen["halved_clears"] and cen["any_one_removed_clears"]
        for kw in (LOW, CENTRAL):
            rows = escape_matrix(ip, prog, **kw)
            assert len(rows) == n_rows and all(r["closed"] for r in rows)
            assert min(r["n_cover"] for r in rows) >= n_cover


def test_near_future_b_program_without_the_engager_needs_car_t_kill_of_about_0_08_to_0_2():
    """The exact input the closure turns on. Without the engager the B program clears at CAR-T kill >= 0.08 /day (duty 0.15) and
    is fault tolerant (halving + drop-one) from 0.2 /day; at 0.06 it does not clear."""
    from canine_dsp.lymphoma_joint import NEAR_FUTURE_PROGRAMS, joint_report
    prog = tuple(p for p in NEAR_FUTURE_PROGRAMS["B"] if p != "CD3xCD20")
    assert not joint_report("B", prog, kill=0.06, duty=0.15)["clears"]
    assert joint_report("B", prog, kill=0.08, duty=0.15)["clears"]
    rob = joint_report("B", prog, kill=0.2, duty=0.4)
    assert rob["clears"] and rob["halved_clears"] and rob["any_one_removed_clears"]


def test_theoretical_agents_are_inadmissible():
    from canine_dsp.lymphoma_joint import READINESS, tier_mix
    assert tier_mix(("hydroxychloroquine",))["admissible"]
    READINESS["__theory__"] = ("E", "no evidence")
    try:
        assert not tier_mix(("hydroxychloroquine", "__theory__"))["admissible"]
    finally:
        del READINESS["__theory__"]
