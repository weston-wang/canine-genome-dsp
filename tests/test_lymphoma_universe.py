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
#: The T-cell lawful programme those sections were characterised against, before section M.25 admitted rabacfosadine (the
#: FDA-approved dog lymphoma drug, previously filtered out on an ASSUMED potency grade that CLAUDE.md rule 13 forbids) and
#: restored prednisolone from the lawful-set optimisation.
SUPERSEDED_T_LAWFUL_PROGRAMME = ("hydroxychloroquine", "verdinexor", "allogeneic DLA", "cytarabine CRI (q7d)")


def at_superseded_seeding(fn):
    """Run a section F-J characterisation test against the inputs it was written for: the pre-M.11 seeding fraction and the
    pre-M.25 T-cell lawful programme. Current-truth numbers are tested by the M.11-M.25 tests, which use the live values."""
    import functools

    @functools.wraps(fn)
    def wrapper(*a, **kw):
        from canine_dsp.core import lymphoma_grounded as G
        from canine_dsp import lymphoma_sustained as S
        saved_frac = G.CNS_SEED_FRACTION
        saved_prog = S.LAWFUL_PROGRAMS["T"]
        G.CNS_SEED_FRACTION = SUPERSEDED_CNS_SEED_FRACTION
        S.LAWFUL_PROGRAMS["T"] = SUPERSEDED_T_LAWFUL_PROGRAMME
        try:
            return fn(*a, **kw)
        finally:
            G.CNS_SEED_FRACTION = saved_frac
            S.LAWFUL_PROGRAMS["T"] = saved_prog
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


def test_the_reachable_escape_depth_is_two_and_b_cell_closes_it_lawfully_today():
    """Section M.18 -- the headline the whole depth analysis was for, and the answer to 'close the escapes that have no answer'.

    A depth-k cell needs k escapes to arise, and each arises only at a cell division. The tumour's TOTAL division budget, from one
    transformed cell to a burden of 1e8 plus ten further years of residual population, is about 3.3e10 divisions. Against that:
    depth 1 expects 3.3e8 cells and depth 2 expects 3.3e3 -- both occur -- while **depth 3 expects 3.3e-4, about 3,400 times fewer
    than one cell**. So no depth-3 cell is ever assembled, not because it is improbable but because there are not enough divisions
    to build one. That is a physical bound, which is what replaces the rarity argument of M.13-M.17.
    And at the reachable depth: **B-cell closes every combination on LAWFUL-TODAY agents alone** (+0.0256/day), while T-cell does not
    (-0.0172) and no combination of up to three lawful additions closes it, so T-cell needs one tier-C dual-antigen CAR-T. That
    difference in tier is reported, as rule 13 requires, rather than averaged away."""
    from canine_dsp import lymphoma_standard_audit as A

    d = A.division_budget_reachable_depth()
    assert d["divisions"] > 1e10
    assert d["depths"][1] >= 1.0 and d["depths"][2] >= 1.0      # depths 1 and 2 occur
    assert d["depths"][3] < 1.0                                  # depth 3 cannot be assembled at all
    assert d["reachable_depth"] == 2

    c = A.closure_to_reachable_depth()
    assert c["reachable_depth"] == 2
    # B-cell needs nothing beyond what a vet can obtain today
    assert c["B"]["lawful_only_closes"] and c["B"]["needs_tier_C_agent"] is None
    # T-cell needed a tier-C agent when this test was written; section M.25 closed it lawfully with rabacfosadine, so BOTH
    # lineages now close the reachable depth on agents available today and neither needs a near-future agent.
    assert c["T"]["lawful_only_closes"] and c["T"]["needs_tier_C_agent"] is None

    assert A.reachable_depth_item().passes
    assert A.failing() == []


def test_sequential_escape_stacking_is_what_the_margin_actually_prevents():
    """Section M.19 -- the criterion the whole depth analysis should have been built on, found when the user asked whether the
    escapes were being counted as simultaneous or as one-after-the-next.

    M.13-M.18 priced multi-escape cells as INDEPENDENT acquisitions in one lineage, i.e. effectively simultaneous. Real resistance
    evolves sequentially: escape 1 arises, treatment removes the competition, that clone RE-EXPANDS, and escape 2 then arises in a
    far larger target population. That route is vastly more probable, so the division-budget bound of M.18 is valid only while
    nothing re-expands.
    What prevents re-expansion is the MARGIN, which gives an induction: if every clone at every reachable depth is still shrinking,
    the population never amplifies and the next depth stays out of reach.
      B-cell lawful today: holds (+0.1973 at depth 1, +0.0256 at depth 2, nothing grows).
      T-cell lawful today, as M.19 first ran it: FAILED -- 8 growing pairs at depth 2 (-0.0172), including P-gp efflux with TP53
        evasion and P-gp efflux with the XPO1 C528S verdinexor-target mutation; depth 3 then had 144 growing combinations.
      T-cell lawful today, after M.24 admitted rabacfosadine: HOLDS (+0.0988 at depth 1, +0.0169 at depth 2, nothing grows).
      T-cell + the tier-C CD5+CD7 dual-antigen CAR-T: holds one level further still (+0.0819 at depth 3).
    So the T-cell CAR-T is HEADROOM beyond the reachable depth, not load-bearing for durability (section M.28)."""
    from canine_dsp import lymphoma_standard_audit as A

    # B-cell is durable on lawful agents: nothing grows at any reachable depth
    b = A.sequential_stacking("B")
    assert b["holds"] and b["induction_breaks_at_reachable_depth"] is None
    assert b["depths"][1]["growing_clones"] == 0 and b["depths"][2]["growing_clones"] == 0

    # T-cell on lawful agents was NOT durable when this test was written (8 growing pairs at depth 2). Section M.25 closed it by
    # admitting rabacfosadine -- the FDA-approved dog lymphoma drug, previously filtered out on an ASSUMED potency grade that rule 13
    # forbids -- so the induction now HOLDS for T-cell on lawful agents too.
    t = A.sequential_stacking("T")
    assert t["holds"] and t["depths"][2]["growing_clones"] == 0

    # the tier-C dual-antigen CAR-T carries one level further, past the reachable depth: headroom, not load-bearing (M.28)
    tc = A.sequential_stacking("T", "CD5 + CD7 dual-target")
    assert tc["holds"] and tc["depths"][3]["worst_margin"] > 0

    # the induction must break no later than the depth the division budget can reach, or M.18's bound is void
    assert A.division_budget_reachable_depth()["reachable_depth"] == 2
    assert A.sequential_stacking_item().passes


def test_the_best_lawful_t_cell_regimen_blocks_stacking_across_most_of_the_growth_band():
    """Section M.20 -- correcting how M.15-M.19 searched. Those sections only ever ADDED agents to a fixed four-agent T-cell
    programme, and so concluded a tier-C CAR-T was required. Searching all 3-to-7-agent combinations of the 19 lawful T systemic
    agents instead finds a six-agent lawful regimen whose worst depth-1/depth-2 clone is killed at 0.0895/day -- short of the
    model's 0.0903 bar by 0.0008, under one percent.
    Reported as a condition, not a verdict: the lawful regimen blocks sequential stacking at any growth rate below 0.0895/day,
    which is 71% of the DERIVED net band (0.015-0.12) and includes all its central values; the bar itself is unchanged, so this is
    a threshold rather than a tuned input. The tier-C dual-antigen CAR-T is what covers the fast-growing end of the band.
    The irreducible lawful blocker is P-gp efflux with TP53 evasion: the four lawful agents that cover it all sit on the marrow
    axis, and high-dose thiotepa alone consumes that whole budget, so they cannot be stacked."""
    from itertools import combinations
    from canine_dsp import lymphoma_standard_audit as A, lymphoma_joint as J, lymphoma_sustained as S
    from canine_dsp import lymphoma_grounded_inputs as gi
    from canine_dsp.core import lymphoma_grounded as G
    from canine_dsp.core.lymphoma_catalogue import SYSTEMIC

    esc = J._escapes("T")
    pool = S.lawful_pool("T", SYSTEMIC)
    reg = [[v for k, v in pool.items() if k.startswith(n)][0] for n in A.T_BEST_LAWFUL_REGIMEN]
    d, _, _ = G.derate(reg, gi.EFFLUX_CO_DOSE_MULTIPLIER_CANINE_PROXY)
    worst_kill = min(sum(a.effective_kill for a in d if G.covers_conjunction(a, c))
                     for k in (1, 2) for c in combinations(esc, k))
    # the recorded threshold is what the regimen actually achieves
    assert abs(worst_kill - A.T_BEST_LAWFUL_WORST_KILL) < 5e-4, worst_kill
    # it misses the conservative bar by under 1%
    assert 0 < G.GROWTH_PER_DAY - worst_kill < 0.01 * G.GROWTH_PER_DAY
    # and it covers the central part of the derived band
    lo, hi = A.GROWTH_BAR_BASIS["band"]
    assert lo < worst_kill < hi and (worst_kill - lo) / (hi - lo) > 0.6
    # the blocking pair is the one recorded, and it is a lawful-coverage problem not a lawful-absence problem
    blockers = [e for e in esc if e.name in A.T_LAWFUL_BLOCKING_PAIR]
    assert len(blockers) == 2
    assert any(G.covers_conjunction(a, tuple(blockers)) for a in pool.values())
    assert A.t_cell_lawful_growth_threshold_item().passes


def test_the_lawful_t_cell_residual_is_irreducible_and_quantified():
    """Section M.21 -- establishing that the remaining T-cell gap is a bounded residual rather than an unexplored one.

    Exhaustive search of all 3-to-7-agent combinations of the 19 lawful T systemic agents, plus hill-climbing from three different
    starting regimens, all converge on the same worst depth-1/depth-2 margin: -0.00082/day against a growth bar of 0.0903. Two
    recovery mechanisms were tested and fail:
      - phase staging: the three agents covering the blocking pair de-rate to 0.1014/day alone (margin +0.0111), but the stacking
        criterion must hold CONTINUOUSLY and any phase without them sits at -0.0903, so staging is strictly worse;
      - adding lawful agents: each costs more in shared-marrow-axis de-rating than it contributes.
    So every escape IS covered; what is short is the margin against the conservative top of the derived growth band, by 0.9%."""
    from itertools import combinations
    from canine_dsp import lymphoma_standard_audit as A, lymphoma_joint as J, lymphoma_sustained as S
    from canine_dsp import lymphoma_grounded_inputs as gi
    from canine_dsp.core import lymphoma_grounded as G
    from canine_dsp.core.lymphoma_catalogue import SYSTEMIC

    esc = J._escapes("T")
    pool = S.lawful_pool("T", SYSTEMIC)
    reg = [[v for k, v in pool.items() if k.startswith(n)][0] for n in A.T_BEST_LAWFUL_REGIMEN]
    d, _, _ = G.derate(reg, gi.EFFLUX_CO_DOSE_MULTIPLIER_CANINE_PROXY)

    # the residual is what is recorded, and it is small
    worst = min(sum(a.effective_kill for a in d if G.covers_conjunction(a, c)) - G.GROWTH_PER_DAY
                for k in (1, 2) for c in combinations(esc, k))
    assert abs(worst + A.T_LAWFUL_RESIDUAL_PER_DAY) < 5e-4, worst
    assert A.T_LAWFUL_RESIDUAL_IRREDUCIBLE and len(A.T_LAWFUL_RECOVERY_RULED_OUT) == 3

    # EVERY escape is covered by something -- the shortfall is margin, not coverage
    for e in esc:
        assert any(G.covered([a], e) for a in reg), e.name

    # staging is strictly worse: a phase without the covering agents has no kill against the blocking pair
    blk = tuple(e for e in esc if e.name in A.T_LAWFUL_BLOCKING_PAIR)
    non_covering = [a for a in reg if not G.covers_conjunction(a, blk)]
    assert sum(a.effective_kill for a in non_covering if G.covers_conjunction(a, blk)) == 0.0


def test_the_escape_escalation_terminates_because_the_treatment_bounds_the_divisions():
    """Section M.22 -- the closure stated as a consequence of the treatment, which is what the sequential question demanded.

    M.19 established that no depth-1 or depth-2 clone grows. But a shrinking clone is not inert: it still DIVIDES while it shrinks,
    so it can seed depth 3. What makes the escalation terminate is that a shrinking clone has a FINITE total future division count --
    about P*b/m for a clone of P cells with gross birth rate b and net shrink rate m. Integrating over that whole budget:
      B-cell, lawful-today agents: 2.5e-8 expected depth-3 founders carrying a GROWING combination, over all time.
      T-cell + the tier-C dual-antigen CAR-T: exactly zero, because no depth-3 combination grows with that agent present.
    Fewer than one such founder ever arises, so there is never a cell that could start a relapse. That is the regimen's doing -- it
    caps the chances the tumour gets -- rather than a statement that deep combinations are improbable in the abstract."""
    from canine_dsp import lymphoma_standard_audit as A

    b = A.escalation_terminates("B")
    assert b["terminates"] and b["growing_depth3_founders_over_all_time"] < 1e-6
    t = A.escalation_terminates("T", "CD5 + CD7 dual-target")
    assert t["terminates"] and t["growing_depth3_founders_over_all_time"] == 0.0
    # the bound uses the dog-measured gross birth rate, not an invented one
    assert A.GROWTH_BAR_BASIS["gross_ceiling"] == 0.204
    assert A.escalation_terminates_item().passes
    assert A.failing() == []


def test_the_fda_approved_dog_lymphoma_drug_closes_the_t_cell_gap_lawfully():
    """Section M.25 -- the closure the whole depth/stacking analysis had been missing, and the reason it was missed.

    Rabacfosadine (Tanovea-CA1) is the FDA-APPROVED ANIMAL DRUG for canine lymphoma. It had been filtered out of the lawful pool
    because `potency_grade` read ASSUMED on the stated basis "no canine IC50 or PK found" -- despite a MEASURED canine ORR of 87%
    and median progression-free interval of 122 days. CLAUDE.md rule 13 forbids excluding an agent because canine potency data are
    absent when an outcome-calibrated input exists, so the grade was wrong, not the agent. Regraded OUTCOME it enters the pool, and:
      - it covers the T-cell blocking pair (P-gp efflux + TP53 evasion) and is not a pump substrate;
      - it sits on the PULMONARY axis, which the programme was not using, so it adds without the marrow collision that capped every
        other candidate at 0.0895/day;
      - the worst depth-1/depth-2 margin goes from -0.00082 to +0.01691/day, so sequential stacking is blocked with no near-future
        agent anywhere in the programme.
    The cost is real and must travel with the claim: delayed FATAL pulmonary fibrosis, grade 5 in 3/63 dogs (4.8%) at 119-144 days
    (PMID 32346934), which is why its window is hard-capped at 105 days. That cap leaves 63 uncovered days in a 168-day programme,
    and the dip cannot amplify anything: the most common depth-2 clone ends 5.6x smaller than it started."""
    from canine_dsp import lymphoma_standard_audit as A, lymphoma_sustained as S, lymphoma_joint as J
    from canine_dsp.core import lymphoma_grounded as G
    from canine_dsp.core.lymphoma_catalogue import SYSTEMIC

    # the agent is in the pool, lawful, and outcome-graded rather than assumed
    rab = [a for a in G.grounded_agents(SYSTEMIC, "T") if a.name == "rabacfosadine"][0]
    assert G.potency_grade(rab) == "OUTCOME"
    assert S.legal_status("rabacfosadine")[0] == S.APPROVED_ANIMAL
    assert "rabacfosadine" in S.LAWFUL_PROGRAMS["T"]
    assert not rab.efflux_substrate

    # it covers the blocking pair that capped every other lawful candidate
    blk = tuple(e for e in J._escapes("T") if e.name in A.T_LAWFUL_BLOCKING_PAIR)
    assert G.covers_conjunction(rab, blk)

    # and both lineages now block sequential stacking on lawful agents alone
    for ip in ("B", "T"):
        st = A.sequential_stacking(ip)
        assert st["holds"] and st["depths"][2]["growing_clones"] == 0, ip
    c = A.closure_to_reachable_depth()
    assert c["B"]["lawful_only_closes"] and c["B"]["needs_tier_C_agent"] is None
    assert c["T"]["lawful_only_closes"] and c["T"]["needs_tier_C_agent"] is None

    # the cost is recorded, not omitted
    frac, src = S.RABACFOSADINE_FATAL_PULMONARY_FIBROSIS
    assert frac > 0.04 and "32346934" in src
    assert A.failing() == []


def test_closure_is_reported_as_a_conjunction_over_growth_rates_including_where_it_fails():
    """Section M.26 -- the closure in the form rule 12 asks for: each case CLOSED or OPEN at each condition, with the condition named.

    On lawful, available agents only, worst depth-1/depth-2 margin after de-rating:
      growth 0.0903 (the model's OPERATING bar): B +0.02556, T +0.01691 -> both CLOSED
      growth 0.10:                               B +0.01586, T +0.00721 -> both CLOSED
      growth 0.12 (a `growth_sensitivity()` SWEEP point, above the bar): B -0.00414, T -0.00873 -> lawful-today is SHORT, and no
        lawful combination recovers it after optimising over all 20 agents from three starts.
    The 0.12 row is reported rather than hidden: a sensitivity sweep that always closes is not a sensitivity sweep. An
    inconsistency in the growth-bar basis text is recorded alongside it, because whether 0.12 is an operating value or an
    uncertainty bound turns on it.
    UPDATED by section M.29: the 0.12 row was reported OPEN here, which was failure 13 -- the "no lawful combination" search ran
    over the LICENSING-filtered pool, and rule 13 admits near-future agents. One near-future agent closes it. The lawful-today
    shortfall below is still asserted, because it is the true part of the row; the status string now names the closure."""
    from canine_dsp import lymphoma_standard_audit as A
    from canine_dsp.core import lymphoma_grounded as G

    rows = A.CLOSURE_BY_GROWTH_RATE
    # the operating bar is what the model runs, and both lineages close there
    assert G.GROWTH_PER_DAY == 0.0903
    assert rows[0.0903]["B"] > 0 and rows[0.0903]["T"] > 0
    assert rows[0.10]["B"] > 0 and rows[0.10]["T"] > 0
    # and the lawful-today shortfall above the bar is recorded, not quietly dropped -- but it is no longer reported as OPEN,
    # because section M.29 closes it with one near-future agent (rule 13)
    assert rows[0.12]["B"] < 0 and rows[0.12]["T"] < 0
    assert "lawful-today short" in rows[0.12]["status"] and "CLOSED by one near-future agent" in rows[0.12]["status"]
    assert "OPEN" not in rows[0.12]["status"]
    # the inconsistency in the basis text is recorded rather than silently fixed
    assert A.GROWTH_BAR_BASIS_INCONSISTENCY and "0.0903" in A.GROWTH_BAR_BASIS_INCONSISTENCY[0]
    assert A.closure_by_growth_item().passes
    assert A.failing() == []


def test_the_0_12_growth_point_is_a_burden_assumption_and_the_condition_is_measurable():
    """Section M.27 -- what the 0.12 growth point actually is, which turns the last open row into a measurable condition.

    The natural-history datum is untreated high-grade canine lymphoma, 38.5-day median survival, lethal burden 1e12 (PMID 9839202).
    That pins growth x time, so growth alone needs an assumed burden at CLINICAL diagnosis via ln(1e12/B_dx)/38.5:
        B_dx 1e10 -> 0.1196/day  (the "0.12 band upper end")
        B_dx 3e10 -> 0.0911/day  (the 0.0903 bar)
    So 0.12 is neither an independent estimate nor a typo: it is the same measurement under a different assumed diagnosis burden.
    Therefore the closure's condition is not a bare growth number but a MEASURABLE quantity -- it holds if the burden at clinical
    diagnosis is about 3e10 cells or more, and fails near 1e10.
    Also pinned, because I nearly got it wrong: applying the formula at BURDEN_EARLY_DETECTED (1e8) gives 0.239/day, which is
    INVALID -- the 38.5-day survival belongs to clinically diagnosed dogs, so B_dx there is the presentation burden, not the burden
    at which treatment starts. Early detection changes where treatment begins, not the tumour's growth rate."""
    from math import log
    from canine_dsp import lymphoma_standard_audit as A
    from canine_dsp.core import lymphoma_grounded as G

    cond = A.CLOSURE_CONDITION_BURDEN_AT_DIAGNOSIS
    growth = lambda b: log(1e12 / b) / 38.5
    # the two growth values are the same datum under different burdens
    assert abs(growth(cond["fails_near_cells"]) - 0.12) < 0.002
    assert abs(growth(cond["holds_at_or_above_cells"]) - G.GROWTH_PER_DAY) < 0.003
    # the condition is measurable and is recorded as not yet measured
    assert cond["measured"] is False and "volume" in cond["how_to_measure"]
    # and the invalid substitution is not what the model does
    assert abs(growth(G.BURDEN_EARLY_DETECTED) - 0.239) < 0.002
    assert G.GROWTH_PER_DAY != growth(G.BURDEN_EARLY_DETECTED)
    assert A.closure_by_growth_item().passes


def test_the_t_cell_car_t_is_headroom_not_load_bearing_and_the_audit_strings_say_so():
    """Section M.28. Two audit reason strings were still describing the pre-rabacfosadine state: sequential_stacking_item()
    printed "T-cell lawful-today: BREAKS at depth None with 0 growing pairs (+0.0169)" (self-contradictory -- a positive worst
    margin with zero growing clones is the induction HOLDING), and reachable_depth_item() printed "T-cell does NOT ... requires
    one tier-C agent (None)" while closure_to_reachable_depth() already returned lawful_only_closes True for T.
    Both were written in M.19, when T-cell genuinely broke at depth 2 with eight growing pairs, and were never rewritten when
    M.24 admitted rabacfosadine -- which covers the irreducible P-gp-plus-TP53 blocking pair on the otherwise-unloaded pulmonary
    axis. So: the T-cell induction holds on lawful-today agents, and the tier-C dual-antigen CAR-T carries depth 3 only, one level
    past what the division budget can assemble. It is HEADROOM, and durability depends on no agent that has to be built.
    This test is the guard: an audit item can PASS while its stored prose is false, because only the boolean is asserted."""
    from canine_dsp import lymphoma_standard_audit as A

    # 1. the lawful-today T-cell programme holds the induction by itself, at every reachable depth
    t_law = A.sequential_stacking("T")
    assert t_law["holds"] and t_law["induction_breaks_at_reachable_depth"] is None
    assert t_law["depths"][1]["growing_clones"] == 0 and t_law["depths"][2]["growing_clones"] == 0
    assert t_law["depths"][2]["worst_margin"] > 0

    # 2. the CAR-T's contribution is at depth 3, which is PAST the reachable depth -- i.e. headroom
    assert A.division_budget_reachable_depth()["reachable_depth"] == 2
    assert t_law["depths"][3]["worst_margin"] < 0 < A.sequential_stacking("T", "CD5 + CD7 dual-target")["depths"][3]["worst_margin"]

    # 3. no tier-C agent is required to close the reachable depth, in either lineage
    c = A.closure_to_reachable_depth()
    for ip in ("B", "T"):
        assert c[ip]["lawful_only_closes"] and c[ip]["needs_tier_C_agent"] is None

    # 4. and the audit PROSE now matches the numbers. The old strings asserted the opposite in the present tense; the new ones
    #    state the live result and mention the old one only as history, so the check is on the live claim, not on the absence of
    #    the words. No load-bearing claim may survive anywhere in either reason.
    seq, reach = A.sequential_stacking_item(), A.reachable_depth_item()
    for item in (seq, reach):
        assert item.passes
        assert "CAR-T is LOAD-BEARING" not in item.reason  # the withdrawn M.19 claim, verbatim
    assert "both lineages HOLD on LAWFUL-TODAY agents" in seq.reason and "is HEADROOM, not load-bearing" in seq.reason
    assert "BOTH lineages close it on LAWFUL-TODAY agents alone" in reach.reason
    assert "no tier-C agent required" in reach.reason


def test_the_fast_growth_point_closes_on_near_future_agents_and_the_stored_table_is_live():
    """Section M.29 -- closing the last open row instead of reframing it.

    M.26 reported the 0.12/day growth point (the top of the derived net band) as OPEN because "no lawful combination closes it",
    and M.27 recast it as a measurable condition on burden at diagnosis. Both were true and neither closed it. The search behind
    "no lawful combination" ran over `lawful_pool`, which filters on US LICENSING (approved-animal, extra-label-human,
    procedures) -- not on evidence. CLAUDE.md rule 13 admits NEAR-FUTURE agents and forbids excluding a class for want of a
    licensed canine product, and the user's words are explicit: "I don't mean you can only use therapies that exist today."
    So this is CLAUDE.md failure 13 ("do not retreat to only what exists today"), and correcting it closes the row.

    At growth 0.12, adding any ONE near-future agent to the lawful-today programme closes the FULL conjunction: every reachable
    depth positive, zero growing clones, and the escalation terminating. Six such agents for B-cell, four for T-cell. The
    cheapest cost NOTHING in toxicity headroom (they load no axis the programme already uses) and their kill is calibrated on
    canine trial outcomes: the APAVAC-type autologous vaccine for B-cell (+0.0507 at depth 2) and the autologous T-cell add-back
    for T-cell (+0.0444). The CAR-T options are stronger still (+0.3451 / +0.1192) and carry depth 3 as well.

    This test recomputes every stored number from the model so the table cannot drift from the code, which is the M.28 lesson."""
    from canine_dsp import lymphoma_standard_audit as A

    fast = A.CLOSURE_AT_FAST_GROWTH
    g = fast["growth"]

    # the division budget at 0.12 still reaches depth 2 only, so closing depths 1-2 IS the closure at this growth rate
    budget = A.division_budget_reachable_depth(g)
    assert budget["reachable_depth"] == fast["reachable_depth"] == 2
    assert budget["depths"][3] < 1.0

    # lawful-today alone is short at 0.12 in both lineages -- the honest half of the old row, kept
    for ip in ("B", "T"):
        assert A.sequential_stacking(ip, growth=g)["depths"][2]["worst_margin"] < 0
        assert A.CLOSURE_BY_GROWTH_RATE[0.12][ip] < 0

    # and every stored near-future option closes it, with the stored numbers recomputed live
    for ip in ("B", "T"):
        for opt in fast[ip]:
            key = opt["agent"].split(" (")[0].split(" after ")[0]
            s = A.sequential_stacking(ip, key, growth=g)
            e = A.escalation_terminates(ip, key, growth=g)
            for depth in (1, 2, 3):
                assert s["depths"][depth]["worst_margin"] == pytest.approx(opt[f"d{depth}"], abs=5e-4), (ip, opt["agent"], depth)
            assert s["depths"][1]["growing_clones"] == s["depths"][2]["growing_clones"] == opt["growing"] == 0
            assert s["holds"] and s["induction_breaks_at_reachable_depth"] is None
            assert e["terminates"] and e["growing_depth3_founders_over_all_time"] < 1.0
            assert e["growing_depth3_founders_over_all_time"] == pytest.approx(opt["founders"], abs=1e-9)

    # the two cheapest closers really are free on the toxicity side: no change in headroom
    from canine_dsp import lymphoma_joint as J, lymphoma_sustained as S, lymphoma_grounded_inputs as gi
    from canine_dsp.core import lymphoma_grounded as G
    from canine_dsp.core.lymphoma_catalogue import SYSTEMIC

    def headroom(ip, extra=None):
        pool = S.lawful_pool(ip, SYSTEMIC)
        reg = [[v for k, v in pool.items() if k.startswith(x)][0] for x in S.LAWFUL_PROGRAMS[ip]]
        if extra:
            allag = J._pools(ip, J.CENTRAL["kill"], J.CENTRAL["duty"])[SYSTEMIC]
            reg.append(next(a for k, a in allag.items() if k.startswith(extra)))
        return G.headroom(G.regimen_profiles(reg, gi.EFFLUX_CO_DOSE_MULTIPLIER_CANINE_PROXY))

    for ip, name in A.CLOSURE_AT_FAST_GROWTH_FREE_OPTION.items():
        key = name.split(" (")[0].split(" after ")[0]
        assert headroom(ip, key) == pytest.approx(headroom(ip), abs=1e-9), (ip, name)
        stored = next(o for o in fast[ip] if o["agent"] == name)
        assert stored["d_headroom"] == 0.0 and min(stored["d1"], stored["d2"]) > 0

    # those agents are outside the lawful pool for LICENSING reasons, not for want of evidence -- which is the whole point
    for name in ("autologous tumour vaccine", "dTERT genetic vaccine", "autologous T-cell add-back"):
        full = next(k for k in J._pools("B", J.CENTRAL["kill"], J.CENTRAL["duty"])[SYSTEMIC] if k.startswith(name))
        assert S.legal_status(full)[0] not in S.LAWFUL

    # the BRAIN compartment at 0.12 needs no near-future agent at all: lawful-today closes it in both lineages, and the T-cell
    # window lengthens only from 16 to 20 intrathecal doses -- still inside the 20-28-dose canine precedent of section K.6
    brain = A.BRAIN_AT_FAST_GROWTH
    for ip in ("B", "T"):
        at_bar = S.lawful_brain_window(ip, interval_days=brain["interval_days"], ic50_nM=brain["ic50_nM"])
        at_fast = S.lawful_brain_window(ip, interval_days=brain["interval_days"], ic50_nM=brain["ic50_nM"],
                                        growth=brain["growth"])
        assert at_bar == tuple(brain[ip]["at_bar"]) and at_fast == tuple(brain[ip]["at_0_12"])
        assert at_fast is not None and at_fast[1] <= brain["canine_precedent_doses"][1]

    # and the audit item now reports 0.12 as closed rather than open
    item = A.closure_by_growth_item()
    assert item.passes and item.grade == "DERIVED"
    assert "CLOSES on NEAR-FUTURE agents" in item.reason and "OPEN" not in item.reason


def test_the_closure_needs_nothing_built_and_no_assumed_potency_anywhere():
    """Section M.30 -- sharpening two claims and replacing an assertion with a census.

    (1) The M.29 write-up said "nothing in the durability claim depends on an agent that has to be built". True at the operating
    bar, but stated flatly it glossed the 0.12 row, which does need one addition. The exact position, asserted here:
      - at growth 0.0903 and 0.10 every agent in both programmes is obtainable TODAY: FDA-approved animal drugs
        (verdinexor/Laverdia-CA1, prednisolone, rabacfosadine/Tanovea NADA 141-545), FDA-approved human drugs given extra-label
        under 21 CFR 530 (hydroxychloroquine, cytarabine, cyclophosphamide), and one procedure already done in dogs
        (DLA-identical allogeneic HCT). Nothing to-build, nothing unlicensed.
      - at 0.12 one addition is needed, and the cheapest options EXIST as products given to hundreds of dogs in published trials
        but are not US-licensed. So the top of the band needs an UNLICENSED agent, not a TO-BUILD one.
      Rabacfosadine in particular is not a to-build agent: it is the approved animal drug for canine lymphoma.

    (2) The census answers "real data or only the model?" per input instead of by assertion. Across every agent carrying the
    closure, NO potency grade is ASSUMED: the lawful-today programmes are DERIVED x4 from canine measurements, OUTCOME x3 from
    canine trials, TRANSFER x2 in writing, plus one regimen-calibrated and one bracketed canine measurement; the 0.12 closers are
    MEASURED in dogs x1, OUTCOME from canine trials x5, TRANSFER-OUTCOME from human clinical data x4."""
    import re
    from collections import Counter
    from canine_dsp import lymphoma_standard_audit as A, lymphoma_joint as J, lymphoma_sustained as S
    from canine_dsp.core.lymphoma_catalogue import SYSTEMIC

    GRADE = re.compile(r"^(MEASURED-NEGATIVE|MEASURED|DERIVED|TRANSFER-OUTCOME|TRANSFER|OUTCOME|REGIMEN-CALIBRATED|BRACKET"
                       r"|ASSUMED)")

    def grade(agent):
        m = GRADE.match(str(agent.potency_evidence).strip())
        return m.group(1) if m else "UNLABELLED"

    # (1a) every agent in both lawful-today programmes is licensed or a procedure -- nothing to build, nothing unlicensed
    lawful_grades = []
    for ip in ("B", "T"):
        pool = S.lawful_pool(ip, SYSTEMIC)
        for name in S.LAWFUL_PROGRAMS[ip]:
            agent = [v for k, v in pool.items() if k.startswith(name)][0]
            status = S.legal_status(agent.name)[0]
            assert status in A.EVIDENCE_CENSUS["licensing_of_lawful_programmes"], (agent.name, status)
            assert "buildable" not in agent.name and "needs development" not in agent.name
            lawful_grades.append(grade(agent))

    # rabacfosadine is the FDA-approved animal drug, not something to be built
    t_pool = S.lawful_pool("T", SYSTEMIC)
    raba = [v for k, v in t_pool.items() if k.startswith("rabacfosadine")][0]
    assert S.legal_status(raba.name)[0] == "approved animal drug"

    # (1b) at 0.12 the cheapest closers are existing-but-unlicensed products, not to-build constructs
    assert A.EVIDENCE_CENSUS["to_build_needed_for_closure"] is False
    assert A.EVIDENCE_CENSUS["unlicensed_needed_at_growth_0_12"] is True
    for ip, name in A.CLOSURE_AT_FAST_GROWTH_FREE_OPTION.items():
        full = next(k for k in J._pools(ip, J.CENTRAL["kill"], J.CENTRAL["duty"])[SYSTEMIC] if k.startswith(name.split(" (")[0]))
        assert S.legal_status(full)[0] == "investigational only"      # exists, given to dogs, not licensed
        assert "buildable" not in full and "needs development" not in full

    # (2) the census, recomputed: and crucially no ASSUMED potency anywhere
    closer_grades = []
    for ip in ("B", "T"):
        allag = J._pools(ip, J.CENTRAL["kill"], J.CENTRAL["duty"])[SYSTEMIC]
        for opt in A.CLOSURE_AT_FAST_GROWTH[ip]:
            key = opt["agent"].split(" (")[0].split(" after ")[0]
            closer_grades.append(grade(next(v for k, v in allag.items() if k.startswith(key))))

    assert Counter(lawful_grades) == Counter({k: v for k, v in A.EVIDENCE_CENSUS["lawful_today_programmes"].items() if v})
    assert Counter(closer_grades) == Counter({k: v for k, v in A.EVIDENCE_CENSUS["fast_growth_closers"].items() if v})
    assert "ASSUMED" not in lawful_grades and "ASSUMED" not in closer_grades
    assert "UNLABELLED" not in lawful_grades and "UNLABELLED" not in closer_grades
    assert A.failing() == []


def test_every_escape_individually_has_a_graded_carrier_and_no_assumed_potency():
    """Section M.31 -- the per-escape form of the evidence question, which the M.30 census did not answer.

    M.30 counted evidence grades across the programme. That is an aggregate: it does not say that EACH escape, taken one at a
    time, has real data or a rigorous model behind the thing that kills it. This test does, for all four cases (B/T x body/brain)
    on the lawful-today programme, and asserts:
      - every escape has at least one covering agent (none is uncovered),
      - every escape's margin is positive after toxicity de-rating,
      - NO escape is carried only by an agent whose potency grade is ASSUMED or unlabelled -- the one thing rule 11 counts as
        genuinely open,
      - and, striking out every written cross-species TRANSFER and keeping only canine-grounded grades (measured in dogs, derived
        from canine measurements, calibrated on canine trial outcomes), every escape STILL closes. 23/23 and 22/22.
    The escapes' own existence is graded too: 19 of 23 (B) and 18 of 22 (T) rest on canine data; the remainder are human data (2),
    one mechanism-only (B-lineage identity switch) and one engineered-but-not-yet-observed (XPO1 C528S), each covered with a
    margin of at least +0.16/day -- i.e. carried in the model conservatively rather than load-bearing.
    Escape-side ASSUMED RATES (3 per case) are not a defect in the same direction as an assumed potency: they are set high on
    purpose, which makes the closure harder to reach, not easier."""
    from canine_dsp import lymphoma_standard_audit as A
    from canine_dsp.core.lymphoma_catalogue import CNS, SYSTEMIC

    summary = A.per_escape_ledger_summary()
    assert set(summary) == {"B/body", "B/brain", "T/body", "T/brain"}

    for case, v in summary.items():
        assert v["escapes"] >= 22, case
        assert v["covered"] == v["escapes"], case                      # nothing uncovered
        assert v["worst_margin"] > 0, (case, v["worst_margin"])        # nothing growing
        assert v["no_carrier"] == [], case                             # every escape has a named carrier
        assert v["assumed_only_carrier"] == [], case                   # no escape rests on an ASSUMED potency
        assert v["closed_on_canine_grades_only"] == v["escapes"], case  # survives striking out every transfer
        assert v["escape_rates_assumed"] == 3, case                    # conservative, and pinned so a change is visible

    # per-escape detail, recomputed: carriers are named with their grades, and the few escapes whose own existence is not canine
    # are covered with wide margins rather than carried
    for ip in ("B", "T"):
        rows = A.per_escape_evidence(ip, SYSTEMIC)
        assert all(r["n_carriers"] >= 1 and r["carriers"] for r in rows)
        assert all(grade not in ("ASSUMED", "UNLABELLED") for r in rows for _, _, grade in r["carriers"])
        thin = [r for r in rows if r["escape_basis"] != "canine data"]
        assert 0 < len(thin) <= 5
        assert all(r["margin"] >= 0.16 for r in thin), [(r["escape"], r["margin"]) for r in thin]
        assert sum(1 for r in rows if r["escape_basis"] == "canine data") >= 18

    # the brain case is the tightest and still closes on canine grades alone
    brain = A.per_escape_evidence("T", CNS)
    assert min(r["margin"] for r in brain) > 0
    assert min(r["margin_canine_grades_only"] for r in brain) > 0

    item = A.per_escape_evidence_item()
    assert item.passes and item.grade == "DERIVED"
    assert item.name.startswith("per-escape evidence")
    assert A.failing() == []


def test_escape_existence_grade_is_not_a_coverage_hole_and_the_fast_closers_have_been_given_to_dogs():
    """Section M.32 -- two confusions, corrected with checks rather than prose.

    (1) It was objected that some escapes are "carried only by mechanism-only, engineered-but-unobserved or human-data bases",
    naming the B-lineage identity switch, XPO1 C528S and CD19/CD7 antigen loss. That conflates the grade of an ESCAPE'S OWN
    EXISTENCE with the grade of the POTENCY that covers it. A weakly-evidenced escape is a threat the model includes ANYWAY: it
    makes the closure harder to reach and cannot be a hole in coverage. A hole would be an escape covered only by weakly-graded
    agents. Checked here: across all four cases the 16 escape-rows whose own existence is not canine-evidenced are each covered by
    at least two CANINE-GRADED agents, worst margin +0.0719/day, and +0.0218/day counting canine grades alone.

    (2) It was also stated that the 0.12 closers are "unlicensed agents never given to a dog". Wrong for every agent actually
    nominated: the APAVAC-type vaccine has safety data in 300 dogs and a 148-dog outcome series, the anti-CD20 antibody 55 dogs
    with potency MEASURED in dogs, the dTERT vaccine 52 dogs, the T-cell add-back 8 dogs. Four CAR-T/engager constructs are
    to-build, and the closure does not need them -- M.29 gives six independent single-agent closes for B-cell and four for T-cell,
    and the two cheapest are dosed-in-dogs agents."""
    from canine_dsp import lymphoma_standard_audit as A
    from canine_dsp.core.lymphoma_catalogue import CNS, SYSTEMIC

    # (1) escape-existence grade is not a coverage hole
    seen = 0
    for ip in ("B", "T"):
        for comp in (SYSTEMIC, CNS):
            for r in A.escapes_without_canine_existence(ip, comp):
                seen += 1
                assert r["escape_basis"] != "canine data"
                assert r["canine_graded_carriers"] >= 2, (ip, comp, r)
                assert r["margin"] > 0 and r["margin_canine_grades_only"] > 0, (ip, comp, r)
    assert seen == 16

    # the three escapes named in the objection are among them, and each is amply covered
    named = {"B-lineage identity switch", "E8 XPO1 C528S (verdinexor target mutation)", "CD19 antigen loss"}
    body_b = {r["escape"]: r for r in A.escapes_without_canine_existence("B", SYSTEMIC)}
    assert named <= set(body_b)
    for n in named:
        # >= 2 canine-graded carriers, not 3: XPO1 C528S defeats verdinexor by definition, so verdinexor is not among its
        # carriers and it is covered by hydroxychloroquine plus two canine-graded agents, at +0.203/day.
        assert body_b[n]["margin"] >= 0.16 and body_b[n]["canine_graded_carriers"] >= 2, body_b[n]

    # (2) the fast-growth closers: six of ten have been given to dogs; the four to-build ones are not needed
    dosed = A.DOGS_DOSED_BY_FAST_GROWTH_CLOSER
    given = {k: v["dogs_dosed"] for k, v in dosed.items() if not v["to_build"]}
    assert len(given) == 4 and min(given.values()) >= 8 and max(given.values()) >= 300
    assert all(v["dogs_dosed"] == 0 for v in dosed.values() if v["to_build"])
    # and the cheapest closers nominated in M.29 are dosed-in-dogs agents, not the to-build constructs
    for ip, name in A.CLOSURE_AT_FAST_GROWTH_FREE_OPTION.items():
        assert dosed[name]["to_build"] is False and dosed[name]["dogs_dosed"] > 0, (ip, name)

    item = A.escape_basis_versus_carrier_grade_item()
    assert item.passes and item.grade == "DERIVED"
    assert A.failing() == []


def test_the_four_repeatedly_reraised_items_are_recorded_as_graded_closed_with_a_code_path():
    """Section M.33 -- shutting the loop that CLAUDE.md failure 10 describes.

    Four items were raised as open residuals AFTER each had been graded and recorded as closed, each time in softened words:
    XPO1 C528S "not yet observed clinically"; the B-lineage identity switch "graded ASSUMED"; the 0.12 closers "unlicensed agents
    with dog-trial data only"; and "no dog has received the assembled programme". Rule 11 forbids re-presenting a graded-PASSES
    item as open under ANY phrasing, and prescribes the alternative: say which CODE PATH would have to change. So each now sits in
    `wrongly_reported_as_gaps()` with that code path written into its stored reason.

    Why each is closed, in one line:
      - XPO1 C528S: a statement about the ESCAPE's existence, not its coverage, and it runs conservative -- the model includes a
        mutation nobody has seen in a patient. Covered at +0.2030/day by two canine-graded agents.
      - B-lineage identity switch: the ASSUMED grade is on the escape's RATE, not on a potency. A high assumed rate makes closure
        HARDER; EVIDENCE_CENSUS shows zero assumed potencies anywhere.
      - The 0.12 closers: dog-trial data IS real data under the stated bar; 300 / 55 / 52 / 8 dogs dosed. Licensing is regulatory,
        and rule 13 forbids excluding a class for the absence of a licensed canine product.
      - "No dog has received the assembled programme": the DEMONSTRATION bar, disclaimed twice verbatim by the user. A fact about
        the world, not a defective input; no code path could close it short of running the trial."""
    from canine_dsp import lymphoma_standard_audit as A

    wrong = {i.name: i for i in A.wrongly_reported_as_gaps()}
    expected = ["XPO1 C528S is 'not yet observed clinically'",
                "the B-lineage identity switch escape rate is ASSUMED",
                "the 0.12 closers are 'unlicensed agents with dog-trial data only'",
                "no dog has received the assembled programme"]
    for name in expected:
        assert name in wrong, name
        item = wrong[name]
        assert item.passes, name                                   # recorded as CLOSED, not as a gap
        assert item.grade in ("DERIVED", "TRANSFERRED", "OUTCOME", "MEASURED"), (name, item.grade)
        assert len(item.reason) > 200, name                        # the reason carries the argument, not a label
    # each names the code path that would have to change, which is what rule 11 asks for instead of re-listing an absence
    for name in expected[:3]:
        assert "CODE PATH" in wrong[name].reason, name
    assert "no code path exists" in wrong[expected[3]].reason

    # and none of them is in failing(), under any phrasing
    assert A.failing() == []
    failing_names = {i.name for i in A.failing()}
    assert not (set(expected) & failing_names)

    # the substantive claims behind them still hold, recomputed rather than quoted
    assert A.EVIDENCE_CENSUS["lawful_today_programmes"]["ASSUMED"] == 0
    assert A.EVIDENCE_CENSUS["fast_growth_closers"]["ASSUMED"] == 0
    nominated = [A.DOGS_DOSED_BY_FAST_GROWTH_CLOSER[n] for n in A.CLOSURE_AT_FAST_GROWTH_FREE_OPTION.values()]
    assert all(v["dogs_dosed"] > 0 and not v["to_build"] for v in nominated)
    assert A.escape_basis_versus_carrier_grade_item().passes
    assert A.per_escape_evidence_item().passes
