"""The widened universe: audit escapes and sweep agents (core/lymphoma_universe.py)."""

import pytest

from canine_dsp.core import lymphoma_grounded as G
from canine_dsp.core import lymphoma_universe as U
from canine_dsp.core.lymphoma_catalogue import CNS, SYSTEMIC



# --- historical characterisation tests -------------------------------------------------------------------------------------------
# Sections F-J were written when the CNS seeding fraction was an "illustrative" 0.05. Section M.11 derived it as 1.2e-3 (high branch),
# which cuts every brain magnitude those sections reported. The findings they pin are still worth regression-testing, but only against
# the input they were computed from, so they are pinned to the superseded value rather than re-fitted to numbers they never asserted.
# Current-truth brain numbers are tested by the M.11 tests below, which run the derived fraction.
SUPERSEDED_CNS_SEED_FRACTION = 0.05


def at_superseded_seeding(fn):
    """Run a section F-J characterisation test at the seeding fraction it was written against (see note above)."""
    import functools

    @functools.wraps(fn)
    def wrapper(*a, **kw):
        from canine_dsp.core import lymphoma_grounded as G
        saved = G.CNS_SEED_FRACTION
        G.CNS_SEED_FRACTION = SUPERSEDED_CNS_SEED_FRACTION
        try:
            return fn(*a, **kw)
        finally:
            G.CNS_SEED_FRACTION = saved
    return wrapper


def _ag(comp, ip):
    return {a.name: a for a in G.grounded_agents(comp, ip)}


def _esc(prefix):
    return next(e for e in U.UNIVERSE_ESCAPES if e.name.startswith(prefix))


def test_full_escape_set_is_the_fifteen_plus_the_audits_nine():
    # 15, not 14: the CD5-loss escape was added 2026-11-16 (section M.17) to fill the rule-9 gap that had been carrying the
    # T-cell deep closure -- the catalogue had CD7 loss but no CD5 loss, so a CD5+CD7 construct could never lose both targets.
    assert len(G.GROUNDED_ESCAPES) == 15
    assert len(G.FULL_ESCAPES) == 24
    assert len({e.name for e in G.FULL_ESCAPES}) == 24


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


@at_superseded_seeding
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
    for ip, names, n_rows in (("B", B_PROGRAMS["B-cell, 7 agents"], 46), ("T", T_PROGRAMS["T-cell, 5 agents"], 44)):
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

@at_superseded_seeding
def test_near_future_programs_close_body_and_brain_even_at_the_pessimistic_inputs():
    """B- and T-cell programs built from exists-today and clinical-stage agents clear every escape in both compartments at the LOW
    CAR-T inputs, and no single agent is load-bearing; at the central inputs they also survive halving every potency."""
    from canine_dsp.lymphoma_joint import CENTRAL, LOW, NEAR_FUTURE_PROGRAMS, escape_matrix, joint_report, tier_mix
    for ip, n_rows, n_cover in (("B", 46, 4), ("T", 44, 5)):
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


@at_superseded_seeding
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


def test_audit_fails_only_on_the_cns_seeding_fraction_and_the_growth_bar_is_derived():
    """History of `failing()`: empty until 31 Oct (M), then the B-cell dose count (M), empty again on 1 Nov once the long-course
    intrathecal transfer landed (M.5), and from 16 Nov the CNS seeding fraction, which the port question exposed (M.7)."""
    from canine_dsp import lymphoma_standard_audit as A
    # CNS seeding fraction closed by derivation on 16 Nov (M.11); the escape-independence assumption then became the one
    # failing item when M.14 found that depth-3+ escape combinations cannot be closed inside the toxicity budget.
    assert A.failing() == []
    assert A.GROWTH_BAR_BASIS["grade"] == "DERIVED" and A.GROWTH_BAR_BASIS["band"][1] >= A.GROWTH_BAR_BASIS["value"]
    assert all(i.passes for i in A.wrongly_reported_as_gaps())


@at_superseded_seeding
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


@at_superseded_seeding
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

@at_superseded_seeding
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
    # ...but this route is NOT lawfully available in the US: the oral prodrug is approved only in Japan, so extra-label use does not
    # reach it (21 CFR 530 covers FDA-APPROVED drugs only). Section K replaces it with intrathecal methotrexate. Tied together here
    # so neither fact can drift from the other.
    assert S.legal_status(S.OCFOSFATE)[0] == S.NO_US_APPROVAL


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
    assert len(r) == 4 and not any(i.passes for i in r)        # 4th added 2026-10-31: the every-21-day brain schedule (section M)
    assert any(i.name.startswith("brain closure on 20 (B)") and i.grade == "ASSUMED" for i in r)   # not CONTRADICTED (section M.4)


# --- radiation as a cycle-independent agent (/goal 2026-10-04, "realistic ways") -------------------------------------------------------

@at_superseded_seeding
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

@at_superseded_seeding
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


@at_superseded_seeding
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


@at_superseded_seeding
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


@at_superseded_seeding
def test_the_brain_closure_has_two_independent_inputs_either_of_which_suffices():
    """The fragility the user suspected is real if only ONE input carries the brain: with intrathecal methotrexate at half reach
    (0.06/day) and verdinexor at the model's generic brain access 0.05, neither brain ever clears. It becomes redundant because
    verdinexor's own brain access is not 0.05: its sister compound selinexor measures brain:plasma 0.60-0.72 across an INTACT barrier in
    mouse, rat and monkey (PMID 27323910). At verdinexor access 0.3 -- below that transfer and above the human disrupted-tumour value
    0.09 -- half-strength methotrexate closes both brains. So the closure holds if EITHER the methotrexate reaches the whole compartment
    OR verdinexor reaches the brain at 0.3 or more."""
    from dataclasses import replace
    from canine_dsp import lymphoma_sustained as S, lymphoma_joint as J
    from canine_dsp.core import lymphoma_grounded as G
    from canine_dsp.core.lymphoma_catalogue import CNS
    med = S.rt_efolds_in_vivo("1771 (median)")

    def ok(ip, mtx_kill, verdinexor_access, window):
        pool = S.lawful_pool(ip, CNS)
        with S.with_windows({S.VERDINEXOR: window, S.IT_MTX: window}):
            reg = []
            for n in S.LAWFUL_PROGRAMS[ip]:
                a = [v for k, v in pool.items() if k.startswith(n)][0]
                if a.name.startswith("verdinexor"):
                    a = replace(a, access=verdinexor_access)
                reg.append(a)
            reg.append(S.rt_agent(ip, CNS, med))
            if mtx_kill > 0:
                reg.append(S.it_mtx_agent(mtx_kill))
            return G.evaluate_best_schedule(reg, J._escapes(ip), compartment=CNS).horizon_strict.cure_inside_window

    for ip in ("B", "T"):
        assert ok(ip, 0.12, 0.05, 730)            # route 1: methotrexate reaches the whole compartment
        assert not ok(ip, 0.06, 0.05, 3650)       # neither input adequate -> never clears, even over 10 years
        assert ok(ip, 0.06, 0.30, 730)            # route 2: verdinexor reaches the brain, methotrexate at half
        assert not ok(ip, 0.0, 0.05, 3650)        # radiation alone never clears


@at_superseded_seeding
def test_the_t_cell_radiation_input_was_conservative_because_a_canine_t_cell_line_was_sitting_unlabelled():
    """OSW was established from a dog with peripheral T-cell lymphoma (PMID 17532464); the radiosensitivity table that supplied the
    model's lines (PMID 27257868) labels it only "Lymphoid". Using it as the lineage-matched value for T-cell disease gives 2.94 in-vivo
    e-folds against the 1.67 the earlier T-cell windows used, so those windows were conservative and the matched one is shorter."""
    from canine_dsp import lymphoma_sustained as S
    osw = S.rt_efolds_in_vivo("OSW (canine peripheral T-cell lymphoma)")
    assert 2.8 <= osw <= 3.1
    assert osw > S.rt_efolds_in_vivo("1771 (median)")
    with_median = S.minimal_lawful_window("T", CNS, rt_efolds=S.rt_efolds_in_vivo("1771 (median)"),
                                          it_mtx_kill=S.IT_MTX_MEAN_KILL_DEFAULT)
    with_osw = S.minimal_lawful_window("T", CNS, rt_efolds=osw, it_mtx_kill=S.IT_MTX_MEAN_KILL_DEFAULT)
    assert with_osw < with_median and 200 <= with_osw <= 300


def test_the_methotrexate_kill_does_not_depend_on_the_uncertain_ic50():
    """The weakest input in section J was a secondary-citation canine IC50 (2-3 nM). It turns out not to matter: the peak CSF level after
    a 2.5 mg intrathecal dose into the MEASURED canine CSF volume is about 121 uM, which is 10^3-10^4 times any plausible IC50, so the
    kill is set by how long the level stays above threshold. Sweeping the IC50 across its entire range (2.5 nM, the human T-ALL anchor
    14 nM, and the pessimistic 118 nM) moves the answer by about 1.6x, and the closure holds at the pessimistic end."""
    from canine_dsp import lymphoma_sustained as S
    assert 44.0 <= S.dog_csf_volume_ml(20.0) <= 46.0                    # 1.39 x BW + 17.5, MRI in 12 dogs
    lo = S.it_mtx_derived_kill(14, ic50_nM=118.0)
    hi = S.it_mtx_derived_kill(14, ic50_nM=2.5)
    assert 1.3 <= hi / lo <= 2.0, (lo, hi)
    assert S.it_mtx_derived_kill(7, ic50_nM=118.0) > 0.12 > S.it_mtx_derived_kill(21, ic50_nM=118.0)


@at_superseded_seeding
def test_both_brains_close_at_the_pessimistic_ic50_with_a_dose_count_dogs_have_tolerated():
    """The closure stated so it can be checked against canine experience. At the PESSIMISTIC IC50 (118 nM), intrathecal methotrexate
    every 21 days, with verdinexor brain access 0.30 (below the 0.60-0.72 measured for its sister compound across an intact barrier) and
    the lineage-matched canine radiosensitivity: the T-cell brain needs 12 doses over 250 days and the B-cell brain 20 over 417 days.
    Dogs have carried subcutaneous CSF ports dosed every other week for 8-11 months, i.e. 20-28 doses, so both are inside precedent.

    SUPERSEDED 2026-10-31 (section M): the 0.30 brain reach was read off a total brain:plasma ratio; measured human selinexor CSF gives
    0.09, at which this schedule never clears. Kept as the record of what the earlier claim depended on; see the test below."""
    from dataclasses import replace
    from canine_dsp import lymphoma_sustained as S, lymphoma_joint as J
    from canine_dsp.core import lymphoma_grounded as G
    from canine_dsp.core.lymphoma_catalogue import CNS
    k = S.it_mtx_derived_kill(21, ic50_nM=118.0)
    assert 0.035 <= k <= 0.055

    def window(ip, efolds):
        def ok(w):
            pool = S.lawful_pool(ip, CNS)
            with S.with_windows({S.VERDINEXOR: w, S.IT_MTX: w}):
                reg = []
                for n in S.LAWFUL_PROGRAMS[ip]:
                    a = [v for kk, v in pool.items() if kk.startswith(n)][0]
                    if a.name.startswith("verdinexor"):
                        a = replace(a, access=0.30)
                    reg.append(a)
                reg.append(S.rt_agent(ip, CNS, efolds))
                reg.append(S.it_mtx_agent(k))
                return G.evaluate_best_schedule(reg, J._escapes(ip), compartment=CNS).horizon_strict.cure_inside_window
        lo, hi = 84, 3650
        assert ok(hi)
        while hi - lo > 30:
            mid = (lo + hi) // 2
            if ok(mid):
                hi = mid
            else:
                lo = mid
        return hi

    t = window("T", S.rt_efolds_in_vivo("OSW (canine peripheral T-cell lymphoma)"))
    b = window("B", S.rt_efolds_in_vivo("1771 (median)"))
    assert 200 <= t <= 300 and round(t / 21) <= 14          # ~12 doses
    assert 380 <= b <= 460 and round(b / 21) <= 24          # ~20 doses


def test_the_japanese_prodrug_is_recorded_as_being_discontinued_not_merely_unapproved():
    """Checked across jurisdictions: the obstacle is no longer only legal. The manufacturer told the Japanese regulator demand had
    ceased and withdrew the larger strength, the label is intermittent with an explicit long-term-use warning, and the indications are
    leukaemia and MDS rather than lymphoma. So it stays out of the programs on supply and label grounds as well as legal ones."""
    from canine_dsp import lymphoma_sustained as S
    status, why = S.legal_status("cytarabine ocfosfate, oral continuous")
    assert status == S.NO_US_APPROVAL
    for phrase in ("discontinued", "INTERMITTENT", "not lymphoma", "Sch 4 para 7", "21 CFR 511"):
        assert phrase in why, phrase


def test_measured_selinexor_csf_removed_the_brain_redundancy():
    """Section M (31 Oct), with its dose-count half superseded by M.11. The human CSF measurement of selinexor replaced a verdinexor
    brain reach of 0.30 that had been read off a TOTAL brain:plasma ratio, so the brain is no longer covered by two independent routes
    and rests on the intrathecal methotrexate. The claim M made about dose counts (29-45, above canine precedent) fell away when the
    CNS seeding fraction was derived; both brains now close inside precedent at the floor."""
    from canine_dsp import lymphoma_sustained as S
    assert S.VERDINEXOR_CNS_ACCESS_MEASURED == 0.09
    for ip in ("B", "T"):
        w = S.lawful_brain_window(ip, interval_days=14, ic50_nM=118.0, rt_scale=S.RT_BRAIN_ESCALATION_FACTOR)
        assert w is not None and w[1] <= S.DOG_IT_DOSES_PRECEDENT_MAX


def test_b_cell_dose_count_passes_on_the_long_course_transfer_and_its_procedural_cost_is_reported():
    """Section M.5. 29-45 intrathecal doses at >= 10-day spacing is TRANSFERRED (human long courses to 36+ doses; same CSF half-life;
    neurotoxicity tracks peak/cumulative concentration, not count; dogs dosed intrathecally for 20 months). It passes the bar, but
    the procedure is a reported cost: ~7-18% cumulative mortality at 30 doses and ~11-25% at 45 if each dose needs an anaesthetic."""
    from canine_dsp import lymphoma_standard_audit as A
    items = {i.name[:2]: i for i in A.lawful_brain_items()}
    # M.11 improved this: with the seeding fraction derived, BOTH cases now sit inside canine dose precedent, so both grade
    # MEASURED-PRECEDENT rather than relying on the long-course transfer. The transfer remains available as headroom.
    assert items["B:"].passes and items["T:"].passes
    assert items["B:"].grade in ("MEASURED-PRECEDENT", "TRANSFERRED")
    assert A.procedural_cost()["mortality_by_route"]["general anaesthesia for every dose, 45 doses"][1] >= 0.2


def test_selinexor_csf_is_a_floor_for_verdinexor_not_its_value():
    """Section M.4 (after the user challenged the sister-drug transfer), with its consequence updated by M.11. Selinexor and verdinexor
    differ by one ring atom; verdinexor is less polar, more lipophilic and not a canine P-gp substrate, so selinexor's human
    CSF/unbound-plasma 0.09 transfers only as a FLOOR, and the superseded 0.30 is unsupported rather than contradicted. The dose-count
    consequence that M.4 recorded (29-45 doses, above canine precedent) no longer holds: once the CNS seeding fraction was derived in
    M.11, the brain closes inside precedent even at the floor, so verdinexor's unmeasured brain reach is no longer decisive."""
    from canine_dsp import lymphoma_sustained as S
    assert S.VERDINEXOR_CNS_ACCESS_FLOOR == S.VERDINEXOR_CNS_ACCESS_MEASURED < S.VERDINEXOR_CNS_ACCESS_SUPERSEDED
    assert abs(S.VERDINEXOR_CNS_ACCESS_MEASURED - 0.919 / (204.67 * 0.05)) < 0.005
    at_floor = S.lawful_brain_window("B", interval_days=14, ic50_nM=118.0, rt_scale=S.RT_BRAIN_ESCALATION_FACTOR)
    assert at_floor is not None and at_floor[1] <= S.DOG_IT_DOSES_PRECEDENT_MAX


def test_36_gy_whole_brain_brings_the_brain_inside_canine_precedent_but_the_23_4_gy_spine_still_governs():
    """Section M.5. 36 Gy / 20 fx whole brain (TRANSFERRED; 1.54x the e-folds of 23.4 Gy) closes the B-cell BRAIN on 17-18 intrathecal
    doses every 14 days even at the pessimistic IC50 and verdinexor's floor -- inside canine precedent. The spine stays at 23.4 Gy
    (cord tolerance with the transplant's TBI), and a spinal sub-compartment at 23.4 Gy still needs the 34-45 doses. So escalation adds
    margin where intrathecal drug reaches least (parenchyma) but does not cut the injection count while the spine is counted separately."""
    from canine_dsp import lymphoma_sustained as S
    f = S.RT_BRAIN_ESCALATION_FACTOR
    for ic50 in (14.0, 118.0):
        w = S.lawful_brain_window("B", interval_days=14, ic50_nM=ic50, rt_scale=f)
        assert w is not None and w[1] <= S.DOG_IT_DOSES_PRECEDENT_MAX, (ic50, w)
    # The M.5/M.6 claim that the 23.4 Gy spine forced a count above precedent no longer holds after M.11 derived the seeding
    # fraction; both are inside precedent now, so what is tested is that escalation does not make it worse.


def test_dosing_the_port_under_sedation_rather_than_anaesthesia_is_what_makes_the_injection_count_affordable():
    """Section M.6. The injections themselves are not the risk: the anaesthetic for each one is. A subcutaneous CSF port was dosed under
    SEDATION through 8-20 months of biweekly infusions in dogs (PMID 24938720), and human Ommaya reservoirs are tapped in clinic with no
    anaesthetic (PMID 25017328, 5,472 accesses, 1 infection). Removing the per-dose anaesthetic cuts cumulative mortality ~20-80x. The risk
    then moves to the device, where technique swings infection ~100-fold -- so strict asepsis is a CONDITION of this route. Dose-sparing by
    bigger or less frequent boluses is ruled out separately, on both toxicity and the model's own schedule sweep."""
    from canine_dsp import lymphoma_sustained as S
    ga = S.PROCEDURAL_MORTALITY_BY_ROUTE["general anaesthesia for every dose, 45 doses"]
    port = S.PROCEDURAL_MORTALITY_BY_ROUTE["port dosed awake/sedated throughout, anaesthesia only to implant + 1 revision"]
    assert port[0] < ga[0] / 20 and port[1] < ga[1] / 15
    strict = S.PORT_INFECTION_PER_ACCESS["strict aseptic protocol, trained staff only"]
    ordinary = S.PORT_INFECTION_PER_ACCESS["ordinary practice"]
    assert ordinary[1] > 0.5 > strict[1]                      # ordinary practice would lose the gain; asepsis is load-bearing
    assert len(S.IT_DOSE_SPARING_RULED_OUT) >= 5          # bigger boluses, depot and pump routes stay ruled out (M.6)


def test_full_craniospinal_36_gy_halves_the_injection_count_but_only_with_reduced_intensity_conditioning():
    """Section M.6. The spine was held at 23.4 Gy because the transplant's 2 x 4-5 Gy conditioning consumed cord budget. With ~2 Gy
    reduced-intensity conditioning the cord sits at 66% of the canine 5%-myelopathy level -- below the 68% already accepted -- so a full
    36 Gy craniospinal course is affordable, and the B-cell brain needs 17-18 doses instead of 34. The open condition is that 2 Gy gives
    mixed rather than full donor chimerism, and the graft's kill was calibrated on >95% donor dogs."""
    from canine_dsp import lymphoma_sustained as S
    assert S.CRANIOSPINAL_36GY_NEEDS_RIC and S.RIC_TBI_GY == 2.0 and S.RIC_OPEN_CONDITION
    full = S.lawful_brain_window("B", interval_days=14, ic50_nM=118.0, rt_scale=S.RT_BRAIN_ESCALATION_FACTOR)
    spine_held = S.lawful_brain_window("B", interval_days=14, ic50_nM=118.0)
    # M.11: both counts fell with the derived seeding fraction, and both are now inside canine precedent. What the escalation still
    # buys is the margin, so the 36 Gy count must be no worse than the 23.4 Gy one.
    assert full[1] <= spine_held[1] <= S.DOG_IT_DOSES_PRECEDENT_MAX


def test_no_port_is_needed_once_the_cns_seeding_fraction_is_derived():
    """Sections M.7 then M.11. The port question exposed an "illustrative" 0.05 seeding fraction that set every brain dose count. Derived,
    it is 1.2e-3 at the conservative high branch -- ~40x lower -- and the brain then needs 8-10 intrathecal doses rather than 16-18.
    Ordinary percutaneous cisternal practice covers that (112 dogs, PMID 25041580), so the implanted port, its infection risk and its
    anaesthetic burden all fall away. Both BODY cases still need no intrathecal dose at all."""
    from canine_dsp import lymphoma_sustained as S, lymphoma_standard_audit as A
    from canine_dsp.core import lymphoma_grounded as G
    from canine_dsp.core.lymphoma_catalogue import SYSTEMIC
    for ip in ("B", "T"):
        assert S.minimal_lawful_window(ip, SYSTEMIC) is not None          # body closes with no intrathecal agent at all
    assert G.CNS_SEED_FRACTION == G.CNS_SEED_FRACTION_BRACKET["high"] < 0.01
    item = A.cns_seeding_item()
    assert item.grade == "DERIVED" and item.passes
    for ip in ("B", "T"):
        w = S.lawful_brain_window(ip, interval_days=14, ic50_nM=118.0, rt_scale=S.RT_BRAIN_ESCALATION_FACTOR)
        assert w is not None and w[1] <= S.DOG_IT_DOSES_PRECEDENT_MAX, (ip, w)


def test_the_model_does_not_contradict_the_canine_maintenance_null():
    """Section M.9, correcting a same-day error. A 2-year maintenance phase in 75 dogs was no better than discontinuous therapy in 333
    (PMID 28100766). An earlier test claimed the model contradicts this because sustained CHOP clears at 365 d -- but that test forced
    the window with with_windows, overriding toxicity caps the model itself sets (doxorubicin hard cap 126 d, prednisolone 150 d). At
    the DOCUMENTED windows CHOP never clears, matching the dogs. The one real override in the programme is verdinexor, justified by its
    label and a 17-month canine case."""
    from canine_dsp import lymphoma_sustained as S, lymphoma_joint as J, lymphoma_standard_audit as A
    from canine_dsp.core import lymphoma_grounded as G, lymphoma_toxicity as T
    from canine_dsp.core.lymphoma_catalogue import SYSTEMIC
    pool = {a.name: a for a in G.grounded_agents(SYSTEMIC, "B")}
    chop = ["doxorubicin", "vincristine", "cyclophosphamide", "prednisolone (glucocorticoid)"]
    # the model caps the regimen well below the window the earlier test forced
    assert T.profile_for("doxorubicin").hard_cap_days == 126.0
    assert T.profile_for("prednisolone (glucocorticoid)").hard_cap_days == 68.0   # M.10: now the measured resistance onset
    # at its own documented windows CHOP does not clear
    assert not G.evaluate([pool[n] for n in chop], J._escapes("B"), compartment=SYSTEMIC,
                          clock=True).horizon_strict.cure_inside_window
    # and weaker combinations never clear at any duration, which is also correct
    for names in (["cyclophosphamide", "prednisolone (glucocorticoid)"], ["prednisolone (glucocorticoid)", "vincristine"]):
        with S.with_windows({n: 1460 for n in names}):
            assert not G.evaluate([pool[n] for n in names], J._escapes("B"), compartment=SYSTEMIC,
                                  clock=True).horizon_strict.cure_inside_window
    item = A.sustained_additivity_item()
    assert item.grade == "RESOLVED" and item.passes and item not in A.failing()
    # the single justified override: verdinexor's documented window is a study duration, not a toxicity cap
    assert T.profile_for("verdinexor (XPO1 inhibitor)").hard_cap_days is None

def test_resistance_emergence_cannot_leave_an_escape_uncovered():
    """Section M.12, settling the question the goal raised. The model has no term for resistance ARISING under treatment (escape
    presence comes from the baseline burden; canine P-gp goes 25% -> 83% by relapse, PMID 8646690). That absence is real but cannot
    open an uncovered route: the programmes are scored against the FULL escape set rather than the presence-filtered subset, the three
    escapes a presence filter would drop are exactly the ones emergence would create, and with every escape forced present from day 0
    every margin is still positive. Emergence changes when an escape appears, not whether it is covered."""
    from canine_dsp import lymphoma_standard_audit as A, lymphoma_joint as J
    from canine_dsp.core import lymphoma_grounded as G
    for ip in ("B", "T"):
        full = J._escapes(ip)
        assert len(G.escapes_to_close(G.BURDEN_EARLY_DETECTED, escapes=full)) < len(full)   # require-all is doing work
    item = A.emergence_is_not_an_uncovered_escape()
    assert item.passes and item.grade == "DERIVED" and item not in A.failing()
    # M.14/M.16 refined this: single-escape coverage holds, but multi-escape DEPTH is the real question. Depth 1-4 is now closed
    # by a near-future dual-antigen CAR-T; what remains failing is B-cell depth 5+ (escape independence) and the CD5-loss
    # catalogue gap that carries the T-cell deep closure.
    assert A.failing() == []


def test_treatment_closes_multi_escape_cells_one_level_deeper_than_they_can_occur():
    """Section M.14, the corrected version of M.13. Enumerating co-occurring escapes gives, per depth:
      depth 1: margin +0.066 to +0.363 /day, and 1-10 expected cells at a burden of 1e8 -- the only REACHABLE depth
      depth 2: margin +0.019 to +0.088 /day -- closed by treatment, expects 1e-8 to 1e-7 cells
      depth 3: margin -0.004 to -0.042 /day -- NOT closed by treatment, expects 1e-15 to 1e-14 cells
      depth 4+: coverage itself fails in the body cases (16 quadruples)
    So treatment closure reaches depth 2 while only depth 1 can occur: one level of headroom. Beyond that the dismissal rests on
    escapes being independent, which is unmeasured in canine lymphoma and is the single failing audit item."""
    from itertools import combinations
    from canine_dsp import lymphoma_standard_audit as A, lymphoma_sustained as S, lymphoma_joint as J
    from canine_dsp.core import lymphoma_grounded as G
    from canine_dsp.core.lymphoma_catalogue import SYSTEMIC

    # depth 1-2 closed by treatment in all four cases
    d = A.multi_escape_depth(max_k=2)
    assert len(d) == 4 and all(v["worst_margin_to_depth"] > 0 for v in d.values()), d
    assert A.multi_escape_item().passes

    # depth 3 is not closed by the LAWFUL-TODAY programme (M.14); M.16 closes it by adding a near-future dual-antigen CAR-T,
    # which multi_escape_depth() deliberately does not include since it scores the lawful programme only.
    d3 = A.multi_escape_depth(max_k=3)
    assert any(v["worst_margin_to_depth"] <= 0 for v in d3.values())
    assert A.depth3_item().passes          # ... and the near-future addition does close it

    # and only depth 1 is reachable: the worst depth-2 combination cannot produce even one cell
    esc = J._escapes("B")
    pool = S.lawful_pool("B", SYSTEMIC)
    reg = [[v for k, v in pool.items() if k.startswith(n)][0] for n in S.LAWFUL_PROGRAMS["B"]]
    worst = min(((sum(a.effective_kill for a in reg if G.covered([a], e1) and G.covered([a], e2)),
                  G.BURDEN_EARLY_DETECTED * e1.seeding_rate * e2.seeding_rate)
                 for e1, e2 in combinations(esc, 2)), key=lambda t: t[0])
    assert worst[0] > G.GROWTH_PER_DAY and worst[1] < 1.0

    # the open item is the independence assumption, and it is the ONLY failing item
    # M.17 closed this: the independence assumption was replaced by a computed correlation bound, so the item now passes.
    assert A.escape_correlation_item().passes

def test_depth_3_escape_combinations_are_closed_by_a_named_near_future_agent():
    """Section M.15 -- the closing work, after M.14 found depth 3 margin-negative and reported it open.

    Lawful-today agents cannot close depth 3: the five that cover every escape alone (cyclophosphamide, craniospinal radiotherapy,
    TBI+transplant, half-body radiation, thiotepa consolidation) sit on the already-loaded marrow axis with kills of 0.004-0.042/day
    against a 0.0903 growth bar, and four of them together give +0.0029/day at toxicity headroom -2.5.
    A canine CAR-T does close it, on the immune axis which carries only 0.30 of its budget. Tier C under rule 13 (clinical-stage
    modality in humans, a stated path to the dog, a derived kill), and the canine CD20 CAR-T trial is enrolling again.
    All margins below are AFTER the model's toxicity de-rating, which is what its verdict uses."""
    from itertools import combinations
    from canine_dsp import lymphoma_standard_audit as A, lymphoma_joint as J, lymphoma_sustained as S
    from canine_dsp import lymphoma_grounded_inputs as gi
    from canine_dsp.core import lymphoma_grounded as G
    from canine_dsp.core.lymphoma_catalogue import SYSTEMIC

    def worst_derated(ip, extra_prefix, kmax):
        esc = J._escapes(ip)
        pool = S.lawful_pool(ip, SYSTEMIC)
        allag = J._pools(ip, J.CENTRAL["kill"], J.CENTRAL["duty"])[SYSTEMIC]
        reg = [[v for k, v in pool.items() if k.startswith(x)][0] for x in S.LAWFUL_PROGRAMS[ip]]
        if extra_prefix:
            reg.append(next(a for k, a in allag.items() if k.startswith(extra_prefix)))
        d, _, _ = G.derate(reg, gi.EFFLUX_CO_DOSE_MULTIPLIER_CANINE_PROXY)
        masks = [(sum(1 << i for i, e in enumerate(esc) if G.covered([a], e)), a.effective_kill) for a in d]
        worst = None
        for k in range(1, kmax + 1):
            for combo in combinations(range(len(esc)), k):
                need = sum(1 << i for i in combo)
                m = sum(kl for mk, kl in masks if mk & need == need) - G.GROWTH_PER_DAY
                worst = m if worst is None else min(worst, m)
        return worst

    # the programme alone does not reach depth 3
    for ip in ("B", "T"):
        assert worst_derated(ip, None, 3) < 0

    # adding the named CAR-T does, in both lineages
    assert worst_derated("B", "persistence-engineered", 3) > 0
    assert worst_derated("T", "CD5 + CD7 dual-target", 3) > 0
    # and for T-cell the dual-target agent also carries depth 4
    assert worst_derated("T", "CD5 + CD7 dual-target", 4) > 0
    # the persistence-engineered single-target construct still leaves B-cell depth 4 open; M.16 closes it with the
    # tandem CD19/CD20 construct instead, which is why that agent was added.
    assert worst_derated("B", "persistence-engineered", 4) < 0
    assert worst_derated("B", "tandem CD19/CD20", 4) > 0

    # agents that are NOT enough, recorded so they are not re-tried
    assert worst_derated("B", "CD3xCD20", 3) < 0
    assert worst_derated("B", "anti-CD20 monoclonal", 3) < 0
    assert worst_derated("T", "CD7-directed CAR-T (canine", 3) < 0
    assert len(A.DEPTH3_INSUFFICIENT) == 3

    assert A.depth3_item().passes and A.depth3_item().grade == "TRANSFERRED"


def test_a_dual_antigen_car_t_closes_the_deep_escape_ladder_and_the_coverage_bug_is_fixed():
    """Section M.16 -- closing B-cell depth 4, which M.15 left open, and fixing a coverage bug found while doing it.

    THE BUG: `covered()` is per escape, so a tandem CD19/CD20 CAR-T "covered" CD19 loss (it still had CD20) and "covered" CD20 loss
    (it still had CD19); per-escape AND therefore credited it against a cell that had lost BOTH and presents no target at all.
    `covers_conjunction()` fixes it by removing every antigen the escape set removes and requiring the agent to retain a target.
    Fixing it cut the B-cell depth-4 margin from +0.2597 to +0.0256 -- so it mattered, and the closure still holds.

    THE CLOSURE: a tandem CD19/CD20 canine CAR-T (tier C, built as the B-lineage analogue of the catalogue's CD5+CD7 construct)
    closes B-cell to depth 4; depth 5 opens at -0.0559 with a worst case expecting ~1e-31 cells.
    THE CAVEAT: T-cell closes at every depth only because the escape catalogue has CD7 loss but NO CD5 loss, so its construct can
    never lose both targets. That is a rule-9 catalogue gap, recorded as a failing item, not a stronger result."""
    from canine_dsp import lymphoma_standard_audit as A, lymphoma_joint as J, lymphoma_sustained as S
    from canine_dsp import lymphoma_grounded_inputs as gi
    from canine_dsp.core import lymphoma_grounded as G
    from canine_dsp.core.lymphoma_catalogue import SYSTEMIC

    esc = J._escapes("B")
    allag = J._pools("B", J.CENTRAL["kill"], J.CENTRAL["duty"])[SYSTEMIC]
    tandem = next(a for k, a in allag.items() if k.startswith("tandem CD19/CD20"))
    cd20 = next(e for e in esc if e.name.startswith("CD20 antigen loss"))
    cd19 = next(e for e in esc if e.name.startswith("CD19 antigen loss"))

    # the bug, and the fix: per-escape says yes to both, the conjunction says no
    assert G.covered([tandem], cd19) and G.covered([tandem], cd20)
    assert not G.covers_conjunction(tandem, (cd19, cd20))
    # a non-antigen-directed agent is unaffected by the fix
    pool = S.lawful_pool("B", SYSTEMIC)
    graft = [v for k, v in pool.items() if k.startswith("allogeneic DLA")][0]
    assert G.covers_conjunction(graft, (cd19, cd20)) == all(G.covered([graft], e) for e in (cd19, cd20))

    # the closure, conjunction-aware and after de-rating: B-cell holds to depth 4
    reg = [[v for k, v in pool.items() if k.startswith(x)][0] for x in S.LAWFUL_PROGRAMS["B"]] + [tandem]
    d, _, _ = G.derate(reg, gi.EFFLUX_CO_DOSE_MULTIPLIER_CANINE_PROXY)
    from itertools import combinations
    for k in (2, 3, 4):
        worst = min(sum(a.effective_kill for a in d if G.covers_conjunction(a, c)) for c in combinations(esc, k))
        assert worst - G.GROWTH_PER_DAY > 0, (k, worst)

    assert A.DEPTH_LADDER_CONJUNCTION_AWARE["B"]["closed_to_depth"] == 4
    assert A.depth3_item().passes

    # the T-cell caveat was recorded as failing in M.16 and then CLOSED in M.17 by adding the missing CD5-loss escape,
    # after which T-cell opens at depth 5 exactly like B-cell instead of appearing closed at every depth.
    assert any(getattr(e, "removes_antigen", "") == "CD5" for e in J._escapes("T"))


def test_the_depth5_conclusion_is_a_bound_not_an_independence_assumption():
    """Section M.17 -- closing the last two open items by work rather than by argument.

    1. The CD5-loss escape is now IN the catalogue, filling the rule-9 gap that had carried the T-cell deep closure. Consequence,
       stated rather than hidden: T-cell no longer closes at every depth, it now opens at depth 5 (-0.0635) exactly like B-cell.
    2. The independence ASSUMPTION is replaced by a computed bound. The most probable depth-5 combination that treatment does not
       close would need ~1.8e6-fold (B) or 5.6e5-fold (T) correlation at EVERY conditional step to reach one expected cell. The
       strongest elevation of mutation rate measured in any tumour (mismatch-repair-deficient cancers) is ~1000-fold, at which the
       worst combination still expects 1e-13 (B) / 1e-11 (T) cells. The conclusion is insensitive to correlation by 11-13 orders of
       magnitude, so it is a rigorous model with a stated bound, not an assumption."""
    from canine_dsp import lymphoma_standard_audit as A, lymphoma_joint as J

    # 1. the catalogue gap is filled, in both lineages
    for ip in ("B", "T"):
        assert any(getattr(e, "removes_antigen", "") == "CD5" for e in J._escapes(ip))

    # 2. the bound, and that it survives the strongest measured mutator level with room to spare
    fold = A.STRONGEST_MEASURED_MUTATOR_FOLD
    for lineage, d in A.DEPTH5_CORRELATION_BOUND.items():
        assert d["needed_per_step"] > 1e5                      # the required correlation is enormous
        assert d["expected_independent"] * fold ** 4 < 1e-10   # and the conclusion holds far beyond it
    item = A.escape_correlation_item()
    assert item.grade == "DERIVED" and item.passes
    # nothing fails the bar any more
    assert A.failing() == []
