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
        assert low["clears"], ip
        if ip == "B":
            assert low["any_one_removed_clears"], low["removal_breaks"]
        else:   # T-cell at the pessimistic inputs: the intrathecal cytarabine is load-bearing (oral cytarabine's CSF level was corrected down)
            assert low["removal_breaks"] == ["continuous intrathecal cytarabine (pump) [buildable]"]
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


def test_audit_nothing_fails_the_stated_bar_and_the_growth_bar_is_derived():
    from canine_dsp import lymphoma_standard_audit as A
    assert A.failing() == []
    assert A.GROWTH_BAR_BASIS["grade"] == "DERIVED" and A.GROWTH_BAR_BASIS["band"][1] >= A.GROWTH_BAR_BASIS["value"]
    assert all(i.passes for i in A.wrongly_reported_as_gaps())


def test_closure_against_a_faster_growth_bar_is_reported_not_retuned():
    """The bar is the upper end of the dog-derived net band, below the gross ceiling (0.204/day). Raising it, with potencies held fixed:
    both programs still clear at the central inputs all the way to the gross ceiling; at the pessimistic inputs the B-cell program
    still clears at the ceiling but the T-cell program needs the bar <= about 0.10/day. Model state is restored afterwards."""
    from canine_dsp import lymphoma_standard_audit as A
    from canine_dsp.core import lymphoma_grounded as G
    before = G.margin_for.__defaults__
    rows = {(r["growth"], r["ip"], r["inputs"]): r for r in A.growth_sensitivity((0.0903, 0.12, 0.204))}
    assert G.margin_for.__defaults__ == before
    for g in (0.0903, 0.12, 0.204):
        assert rows[(g, "B", "central")]["clears"] and rows[(g, "T", "central")]["clears"]
    assert rows[(0.204, "B", "low")]["clears"]
    assert rows[(0.0903, "T", "low")]["clears"] and not rows[(0.12, "T", "low")]["clears"]
    assert rows[(0.0903, "B", "low")]["drop_one"] and not rows[(0.0903, "T", "low")]["drop_one"]


# --- dog programs (/goal 2026-10-04) -------------------------------------------------------------------------------------------

def test_near_future_programs_depend_on_agents_with_no_dog_program_found():
    """Record the finding rather than hide it: the near-future B and T programs include agents whose canine version was searched for
    and not found (CD3 engager, CD7/CD5 CAR-T, intrathecal routes)."""
    from canine_dsp.lymphoma_joint import NEAR_FUTURE_PROGRAMS, dog_program_gaps
    assert "CD3xCD20" in dog_program_gaps(NEAR_FUTURE_PROGRAMS["B"])
    assert {"CD7-directed CAR-T (canine", "CD5 + CD7 dual-target CAR-T (c"} <= set(dog_program_gaps(NEAR_FUTURE_PROGRAMS["T"]))


def test_b_cell_closes_from_agents_with_a_dog_program_if_the_car_t_works():
    """No engager and no CSF route: anti-CD20, HCQ, verdinexor, matched transplant, oral cytarabine + a systemic CAR-T (Penn program).
    It clears body and brain from CAR-T kill 0.12/day; it is NOT fault tolerant (the CAR-T is load-bearing); halving holds from 0.35."""
    from canine_dsp.lymphoma_joint import DOG_PROGRAM_PROGRAMS, dog_program_gaps, joint_report
    prog = DOG_PROGRAM_PROGRAMS["B"]
    assert dog_program_gaps(prog) == []
    assert not joint_report("B", prog, kill=0.10, duty=0.4)["clears"]
    r12 = joint_report("B", prog, kill=0.12, duty=0.4)
    assert r12["clears"] and not r12["any_one_removed_clears"]
    r35 = joint_report("B", prog, kill=0.35, duty=0.4)
    assert r35["clears"] and r35["halved_clears"] and r35["removal_breaks"] == ["persistence-engineered canine-binder CAR-T (specification)"]


# --- sustained existing agents (/goal 2026-10-04) ------------------------------------------------------------------------------

def test_b_cell_brain_closes_with_existing_agents_only_if_oral_cytarabine_is_sustained_about_four_years():
    """Corrects the section-F claim that longer dosing cannot close the brain (it had been tested only to 730 days). The binding agent is
    oral cytarabine ocfosfate (not a pump substrate, reaches CSF); the others stay at their documented windows. 730 days is not enough,
    about 1,470 days is (worst swept switching rate)."""
    from canine_dsp import lymphoma_sustained as S
    from canine_dsp.core.lymphoma_catalogue import CNS
    prog = S.EXISTING["B"]
    assert not S.clock("B", prog, CNS)[0]                                   # as documented (84 d): E5 regrows
    with S.with_windows({S.OCFOSFATE: 730}):
        assert not S.clock("B", prog, CNS)[0]
    with S.with_windows({S.OCFOSFATE: 1825}):
        assert S.clock("B", prog, CNS)[0]
    assert 1350 <= S.minimal_window("B", prog, CNS, S.OCFOSFATE, lo=730, hi=1825) <= 1650
    assert not S.clock("B", prog, CNS)[0]                                   # context manager restored the default


def test_t_cell_body_closes_with_existing_agents_if_verdinexor_is_sustained_about_six_months():
    from canine_dsp import lymphoma_sustained as S
    from canine_dsp.core.lymphoma_catalogue import SYSTEMIC
    prog = S.EXISTING["T"]
    assert not S.clock("T", prog, SYSTEMIC)[0]
    with S.with_windows({S.VERDINEXOR: 600}):
        assert S.clock("T", prog, SYSTEMIC)[0]
    with S.with_windows({S.OCFOSFATE: 600}):       # T-cell cytarabine kill is lower; not enough on its own
        assert not S.clock("T", prog, SYSTEMIC)[0]


def test_t_cell_brain_is_not_closed_by_sustaining_existing_agents():
    """Thiotepa closes the dCK-loss lineage (E2) in the window, but the dormant lineage then needs oral cytarabine for about 8 years in T-cell
    disease (lower CSF kill than B): not a credible duration, so the T-cell brain stays open without a new effector."""
    from canine_dsp import lymphoma_sustained as S
    from canine_dsp.core.lymphoma_catalogue import CNS
    from canine_dsp.core import lymphoma_grounded as G
    saved = G.AVAILABILITY.get(S.THIOTEPA)
    G.AVAILABILITY[S.THIOTEPA] = G.OFF_LABEL
    try:
        prog = S.EXISTING["T"] + ("high-dose thiotepa",)
        with S.with_windows({S.OCFOSFATE: 1825}):
            assert not S.clock("T", prog, CNS)[0]
    finally:
        G.AVAILABILITY[S.THIOTEPA] = saved


def test_audit_lists_the_routes_that_were_set_aside_with_their_grades():
    from canine_dsp import lymphoma_standard_audit as A
    r = A.routes_not_counted()
    assert len(r) == 3 and not any(i.passes for i in r)


# --- radiation as a cycle-independent agent (/goal 2026-10-04, "realistic ways") -------------------------------------------------------

def test_brain_radiation_plus_sustained_oral_cytarabine_closes_the_b_cell_brain_from_existing_agents():
    """Existing agents only (anti-CD20 antibody, HCQ, verdinexor, matched-donor transplant, oral cytarabine) plus a 23.4 Gy craniospinal /
    whole-brain course, graded cycle-independent with the in-vivo dose-modifying factor 1.9. The needed sustained window falls as the radiation
    e-folds rise: 1,560 days with none, about 1,250 / 975 / 250 days at the resistant / median / sensitive canine line."""
    from canine_dsp import lymphoma_sustained as S
    from canine_dsp.core.lymphoma_catalogue import CNS
    prog = S.EXISTING["B"]
    none = S.minimal_window("B", prog, CNS, S.OCFOSFATE, lo=100, hi=3000)
    assert 1400 <= none <= 1700
    got = {ln: S.minimal_window_with_rt("B", prog, CNS, S.rt_efolds_in_vivo(ln)) for ln in S.RT_EFOLDS_IN_VITRO}
    assert 1100 <= got["CLL1390 (most resistant)"] <= 1400
    assert 850 <= got["1771 (median)"] <= 1100
    assert 150 <= got["CLBL1 (most sensitive)"] <= 400
    assert got["CLBL1 (most sensitive)"] < got["1771 (median)"] < got["CLL1390 (most resistant)"] < none


def test_t_cell_body_closes_with_radiation_free_existing_agents_after_about_six_months_and_t_cell_brain_does_not_close():
    """T-cell brain: even with radiation at the sensitive-line value and two-year windows... the sweep to 3,650 days never clears it."""
    from canine_dsp import lymphoma_sustained as S
    from canine_dsp.core.lymphoma_catalogue import CNS, SYSTEMIC
    assert 100 <= S.minimal_window_with_rt("T", S.EXISTING["T"], SYSTEMIC, S.rt_efolds_in_vivo("1771 (median)")) <= 250
    for ln in S.RT_EFOLDS_IN_VITRO:
        assert S.minimal_window_with_rt("T", S.EXISTING["T"], CNS, S.rt_efolds_in_vivo(ln)) is None


# --- intrathecal methotrexate closes the T-cell brain (/goal 2026-10-05) ------------------------------------------------------------------

def test_t_cell_brain_closes_with_radiation_plus_repeated_intrathecal_methotrexate_for_about_a_year_with_matched_transplant():
    """Existing T-cell program (matched-donor transplant, verdinexor, ...) at documented windows + a 23.4 Gy course + repeated intrathecal methotrexate
    (mean kill 0.12 /day, about every 2-3 weeks). The binding quantity is the duration of the methotrexate: about 400 days at the median canine line,
    840 days at the most resistant, 230 days at the most sensitive, about 1,350 days with no radiation; and it needs a mean kill of at least ~0.1."""
    from canine_dsp import lymphoma_sustained as S
    from canine_dsp.core.lymphoma_catalogue import CNS
    prog = S.EXISTING["T"]
    med = S.minimal_it_mtx_window("T", prog, CNS, rt_efolds=S.rt_efolds_in_vivo("1771 (median)"))
    res = S.minimal_it_mtx_window("T", prog, CNS, rt_efolds=S.rt_efolds_in_vivo("CLL1390 (most resistant)"))
    sen = S.minimal_it_mtx_window("T", prog, CNS, rt_efolds=S.rt_efolds_in_vivo("CLBL1 (most sensitive)"))
    none = S.minimal_it_mtx_window("T", prog, CNS)
    assert 330 <= med <= 470 and 750 <= res <= 950 and 180 <= sen <= 280 and 1200 <= none <= 1500
    assert S.minimal_it_mtx_window("T", prog, CNS, rt_efolds=S.rt_efolds_in_vivo("1771 (median)"), it_mtx_kill=0.06) is None


def test_the_transplant_is_load_bearing_for_the_methotrexate_route():
    """Without the matched-donor transplant (which clears the remaining lineages in its window) radiation + methotrexate alone does not close it in a credible time."""
    from canine_dsp import lymphoma_sustained as S
    from canine_dsp.core.lymphoma_catalogue import CNS
    prog = tuple(p for p in S.EXISTING["T"] if p != "allogeneic DLA")
    w = S.minimal_it_mtx_window("T", prog, CNS, rt_efolds=S.rt_efolds_in_vivo("1771 (median)"))
    assert w is None or w > 3000


def test_b_cell_brain_also_closes_in_about_a_year_with_the_same_methotrexate_route():
    """A much shorter alternative to the 2.7-3.4 years of oral cytarabine."""
    from canine_dsp import lymphoma_sustained as S
    from canine_dsp.core.lymphoma_catalogue import CNS
    w = S.minimal_it_mtx_window("B", S.EXISTING["B"], CNS, rt_efolds=S.rt_efolds_in_vivo("1771 (median)"))
    assert 330 <= w <= 470


# --- lawful availability for a pet dog (/goal 2026-10-06) --------------------------------------------------------------------------------

def test_the_two_agents_with_no_lawful_route_are_recorded_and_excluded():
    """21 CFR 530 extra-label use covers only FDA-APPROVED animal or human drugs, so a Japan-only product has no route, and an
    investigational biologic is not a routine therapy. Both were load-bearing in the earlier programs."""
    from canine_dsp import lymphoma_sustained as S
    assert S.legal_status("cytarabine ocfosfate, oral continuous")[0] == S.NO_US_APPROVAL
    assert S.legal_status("anti-CD20 monoclonal antibody")[0] == S.INVESTIGATIONAL
    for ip in ("B", "T"):
        pool = S.lawful_pool(ip, CNS)
        assert not any("ocfosfate" in n or n.startswith("anti-CD20") for n in pool)
        assert all(S.legal_status(n)[0] in S.LAWFUL for n in pool)


def test_intrathecal_methotrexate_has_the_strongest_legal_footing_of_the_closing_agents():
    """Preservative-free methotrexate is FDA-approved WITH intrathecal as a labelled human route; verdinexor is an approved ANIMAL drug
    whose label is continuous twice-weekly dosing, so sustaining it is on-label."""
    from canine_dsp import lymphoma_sustained as S
    assert S.legal_status(S.IT_MTX)[0] == S.APPROVED_HUMAN_ELU
    assert "INTRATHECAL is a labelled human" in S.legal_status(S.IT_MTX)[1]
    assert S.legal_status("verdinexor")[0] == S.APPROVED_ANIMAL
    assert "ON-LABEL" in S.legal_status("verdinexor")[1]


def test_all_four_cases_close_on_lawful_agents_only():
    """Body: about 6 months of verdinexor (on-label continuous dosing). Brain: one 23.4 Gy course plus repeated intrathecal methotrexate,
    for about 420 days (B) and 378 days (T) at the median canine radiosensitivity. The methotrexate is indispensable: with the radiation
    course but no methotrexate neither brain ever clears."""
    from canine_dsp import lymphoma_sustained as S
    from canine_dsp.core.lymphoma_catalogue import CNS, SYSTEMIC
    med = S.rt_efolds_in_vivo("1771 (median)")
    for ip, expect in (("B", 420), ("T", 378)):
        assert 120 <= S.minimal_lawful_window(ip, SYSTEMIC) <= 220
        got = S.minimal_lawful_window(ip, CNS, rt_efolds=med, it_mtx_kill=S.IT_MTX_MEAN_KILL_DEFAULT)
        assert abs(got - expect) <= 60, (ip, got)
        assert S.minimal_lawful_window(ip, CNS, rt_efolds=med) is None            # radiation without methotrexate never clears
        assert 1100 <= S.minimal_lawful_window(ip, CNS, it_mtx_kill=S.IT_MTX_MEAN_KILL_DEFAULT) <= 1500   # methotrexate without radiation
