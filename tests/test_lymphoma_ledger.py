"""Re-derives the numbers recorded in docs/LYMPHOMA_COVERAGE_LEDGER.md and docs/LYMPHOMA_STATUS.md
from the grounded model. Deterministic; no Monte Carlo. Each test states the claim it protects."""
import pytest

from canine_dsp import lymphoma_coverage_ledger as L
from canine_dsp import lymphoma_grounded_inputs as gi
from canine_dsp.core import lymphoma_grounded as G
from canine_dsp.core import lymphoma_search as S1
from canine_dsp.core.evidence import Population, ProvenanceError, Species
from canine_dsp.core.lymphoma_catalogue import (B_LINEAGE_ANTIGENS, BURDEN_EARLY_DETECTED, CNS, ESCAPES,
                                                SYSTEMIC, agents_in)
from canine_dsp.core.lymphoma_horizon import horizon
from canine_dsp.core.lymphoma_toxicity import (Organ, PROFILES, axis_loads, profile_for,
                                               with_efflux_co_dose)

B, T = "B", "T"


@pytest.fixture(autouse=True)
def _v1_catalogue(monkeypatch):
    """These tests protect the ledger's claims, which were derived on the v1 catalogue (before the universe widening of
    docs/LYMPHOMA_UNIVERSE.md added vaccines, transplant, engagers, inhibitors, oral cytarabine and the brain agents). The
    widened catalogue has its own tests in test_lymphoma_universe.py, and its results supersede these claims there."""
    from canine_dsp.core import lymphoma_universe as U
    orig = G.grounded_agents

    def v1(compartment, immunophenotype="B"):
        added = {a.name for fn in (U.universe_agents, U.brain_agents, U.reassessed_agents, U.inhibitor_agents)
                 for a in fn(compartment, immunophenotype)}
        return tuple(a for a in orig(compartment, immunophenotype) if a.name not in added)

    monkeypatch.setattr(G, "grounded_agents", v1)


def _pool(comp, ip, tier, grades=None):
    return [a for a in G.available(G.grounded_agents(comp, ip), tier)
            if grades is None or G.potency_grade(a) in grades]


# ---------- provenance: numbers cannot migrate between populations ----------

def test_a_b_cell_ic50_cannot_be_read_for_t_cell_without_a_transfer():
    with pytest.raises(ProvenanceError):
        gi.VENETOCLAX_EC50_B.value_for(gi.VENETOCLAX_EC50_T.population)
    assert gi.VENETOCLAX_EC50_T.value_for(gi.VENETOCLAX_EC50_T.population) == 23.0


def test_transfer_is_explicit_and_marked():
    m = gi.VERDINEXOR_IC50_B.transfer_to(gi.VERDINEXOR_IC50_T.population, "test: borrow across phenotype")
    assert m.provenance.value == "transferred from another population"
    with pytest.raises(ProvenanceError):
        gi.VERDINEXOR_IC50_B.transfer_to(gi.VERDINEXOR_IC50_T.population, "")


# ---------- potency: what could and could not be derived ----------

def test_verdinexor_is_derived_from_two_canine_lymphoma_measurements():
    b, t = gi.verdinexor(B), gi.verdinexor(T)
    assert b.kill_per_day == pytest.approx(0.275, abs=0.01) and b.closes
    assert t.kill_per_day == pytest.approx(0.154, abs=0.01) and t.closes
    assert b.ic50 is not None and b.concentration is not None


def test_venetoclax_t_cell_closes_within_the_tolerated_beagle_dose_range_but_b_cell_never_does():
    assert gi.venetoclax_T_min_dose_to_close(0.01) == pytest.approx(1.23, abs=0.1)
    assert gi.venetoclax_T_min_dose_to_close(0.001) == pytest.approx(12.3, abs=0.6)
    assert gi.venetoclax_T_min_dose_to_close(0.001) < 20.0            # inside the 2-20 mg/kg range
    assert gi.venetoclax_B_kill(20.0, 0.01) < 1e-3


def test_hcq_gives_a_hinge_not_a_kill_rate():
    h = gi.hcq_hinge()
    assert h.kill_per_day is None and h.basis == "NOT DERIVABLE"
    assert h.required_ic50_nM_to_close / 1000.0 == pytest.approx(100.6, abs=1.5)   # uM


def test_prednisolone_potency_is_a_bracket_of_two_disagreeing_measurements():
    b = gi.prednisolone_bracket()
    assert b["low_per_day"] == pytest.approx(0.0098, abs=0.001)
    assert b["high_per_day"] == pytest.approx(0.144, abs=0.005)
    assert 10 < b["ratio"] < 20


def test_antibody_depletion_rate_is_measured_in_dogs():
    r = gi.antibody_depletion_rates()
    assert r["day_0_to_7"] == pytest.approx(0.46, abs=0.01)
    assert r["day_7_to_21"] == pytest.approx(0.099, abs=0.005)


def test_plasma_method_underpredicts_chop_so_chop_potencies_are_regimen_calibrated():
    c = gi.cytotoxic_integrated_exposure()
    assert c["doxorubicin"]["e_folds_per_dose"] < 0.5 and c["vincristine"]["e_folds_per_dose"] < 0.5
    grades = {a.name: G.potency_grade(a) for a in G.grounded_agents(SYSTEMIC, B)}
    for n in ("doxorubicin", "vincristine", "cyclophosphamide"):
        assert grades[n] == "REGIMEN-CALIBRATED"


# ---------- toxicity: no fail-open, charged co-dose, time dimension ----------

def test_every_grounded_agent_has_a_toxicity_profile_and_unknown_raises():
    for comp in (SYSTEMIC, CNS):
        for ip in (B, T):
            for a in G.grounded_agents(comp, ip):
                profile_for(a.name)
    with pytest.raises(KeyError):
        profile_for("made-up agent that has no profile")


def test_a_reverser_multiplies_its_partners_load_but_not_other_agents():
    ag = {a.name: a for a in G.grounded_agents(SYSTEMIC, B)}
    dox, cyc = ag["doxorubicin"], ag["cyclophosphamide"]
    rev = ag[G.REVERSER]
    base = axis_loads(G.regimen_profiles([dox, cyc], 2.0))
    withrev = axis_loads(G.regimen_profiles([dox, cyc, rev], 2.0))
    # doxorubicin is a P-gp substrate: its marrow load doubles; cyclophosphamide's does not
    assert withrev[Organ.MARROW] - base[Organ.MARROW] == pytest.approx(
        profile_for("doxorubicin").budget_fraction * (2.0 - 1.0) + profile_for(G.REVERSER).budget_fraction)


def test_reversal_lets_a_substrate_cover_the_pump_clone_and_absence_does_not():
    ag = {a.name: a for a in G.grounded_agents(SYSTEMIC, B)}
    dox = ag["doxorubicin"]
    assert G.kill_against([dox], G.PGP) == 0.0
    assert G.kill_against([dox, ag[G.REVERSER]], G.PGP) == pytest.approx(dox.effective_kill)


def test_lookup_of_the_two_cyclophosphamides_is_by_exact_name():
    assert profile_for("cyclophosphamide").axis is Organ.MARROW
    assert profile_for("cyclophosphamide (metronomic)").axis is Organ.BLADDER


def test_time_windows_carry_the_documented_canine_caps():
    assert profile_for("doxorubicin").sustainable_days == 126.0          # 6 doses, 180 mg/m2 (PMID 30697816)
    assert profile_for("lomustine (CNS-penetrant nitrosourea)").hard_cap_days == 84.0
    assert profile_for("CD20 CAR-T").sustainable_days == 50.0            # persistence (PMID 32002286)
    assert profile_for("prednisolone (glucocorticoid)").hard_cap_days == 150.0   # PMID 40696374


# ---------- the new defeat mechanics ----------

def test_antigen_presentation_loss_defeats_checkpoint_blockade_but_not_a_car_or_an_antibody():
    esc = next(e for e in G.NEW_ESCAPES if "presentation" in e.name)
    ag = {a.name: a for a in G.grounded_agents(SYSTEMIC, B)}
    assert not ag["anti-PD-1 / anti-PD-L1 checkpoint blockade"].covers(esc)
    assert ag["CD20 CAR-T"].covers(esc) and ag["anti-CD20 monoclonal antibody"].covers(esc)


def test_mgmt_repair_defeats_lomustine_only():
    esc = next(e for e in G.NEW_ESCAPES if "MGMT" in e.name)
    ag = {a.name: a for a in G.grounded_agents(SYSTEMIC, B)}
    assert not ag["lomustine (CNS-penetrant nitrosourea)"].covers(esc)
    assert ag["cyclophosphamide"].covers(esc) and ag["doxorubicin"].covers(esc)


def test_only_an_engineered_car_covers_exhaustion():
    exh = next(e for e in ESCAPES if "exhaustion" in e.name)
    ag = {a.name: a for a in G.grounded_agents(SYSTEMIC, B)}
    assert not ag["CD20 CAR-T"].covers(exh)
    assert ag["CD20 CAR-T with PD-1/CD28 switch receptor"].covers(exh)


def test_founder_escapes_stay_in_the_set_at_an_early_detection_burden():
    early = {e.name for e in G.escapes_to_close(BURDEN_EARLY_DETECTED)}
    for n in G.FOUNDER_ESCAPES:
        assert n in early


# ---------- the clock ----------

def test_a_course_agent_clears_small_lineages_inside_its_course():
    """TBI alone: its derived in-course kill (0.145/day) beats the 0.0903 bar, so the 1-cell pump lineage is
    gone in ~11 days, though its annual-average duty (14/365) would suggest it does almost nothing.
    (Half-body irradiation's DERIVED kill, 0.052/day, is below the bar: alone it cannot.)"""
    tbi = next(a for a in G.grounded_agents(SYSTEMIC, B) if a.name.startswith("total body"))
    hz = horizon([G.in_window(tbi)], [G.PGP], {tbi.name: 14.0}, 1e8, 0.0903,
                 margin_fn=lambda act, e: G.margin_for(act, e), always_present=(G.PGP.name,),
                 kill_of=lambda a: G.in_window(a).effective_kill)
    pgp = next(o for o in hz.outcomes if o.name == G.PGP.name)
    assert pgp.outcome == "cleared" and pgp.day < 14
    assert tbi.effective_kill < 0.02            # the annual average that hid this
    hbi = next(a for a in G.grounded_agents(SYSTEMIC, B) if a.name.startswith("half-body"))
    assert G.in_window(hbi).effective_kill < 0.0903


def test_chop_alone_at_clinical_burden_is_not_predicted_to_cure():
    """Calibration against real outcome: median PFS 176 d (PMID 26279153), ~10% alive at 2 y
    (PMID 21320018). The model must predict response then relapse, in the right order of days."""
    c = L.calibration_chop()
    assert not c["cured"]
    days = dict(c["relapse_days"])
    assert 100 <= days["drug-sensitive bulk"] <= 200


# ---------- what changed from v1 ----------

def test_grounded_model_differs_from_v1_only_by_the_documented_corrections():
    """v1's own numbers are reproduced by tests/test_lymphoma_search.py against the v1 catalogue. The grounded
    catalogue changes these, each with a source: HCQ potency 0.10 -> 0.28 (transfer) and P-gp substrate,
    venetoclax a substrate (conflicting sources), radiation potencies from canine survival data, prednisolone
    and venetoclax CNS access from primate/human CSF data."""
    v1 = {a.name: a for a in agents_in(SYSTEMIC)}
    g = {a.name: a for a in G.grounded_agents(SYSTEMIC, B)}
    assert v1["hydroxychloroquine (autophagy)"].potency == pytest.approx(0.10)
    assert g["hydroxychloroquine (autophagy)"].potency == pytest.approx(0.284, abs=0.01)
    assert g["hydroxychloroquine (autophagy)"].efflux_substrate and not v1["hydroxychloroquine (autophagy)"].efflux_substrate
    assert g["craniospinal radiotherapy"].potency < v1["craniospinal radiotherapy"].potency
    assert g["total body irradiation + transplant"].potency < v1["total body irradiation + transplant"].potency
    cns_v1 = {a.name: a for a in agents_in(CNS)}
    cns_g = {a.name: a for a in G.grounded_agents(CNS, B)}
    assert cns_v1["prednisolone (glucocorticoid)"].access == pytest.approx(0.40)
    assert cns_g["prednisolone (glucocorticoid)"].access == pytest.approx(0.08)


def test_v1_cns_b_cell_closure_still_relapses_when_the_cell_therapy_ends():
    rec = S1.MOST_ROBUST[(CNS, B)]
    s = L.regimen_summary(CNS, B, rec["agents"])
    assert "RESPONSE THEN RELAPSE" in s["strict_window"]


def test_v1_minimal_closing_regimens_relapse_except_the_t_cell_pair_that_hcq_now_rescues():
    """v1's two-agent B-cell regimen and its CNS regimen still relapse when a drug must stop. The T-cell
    prednisolone + hydroxychloroquine pair now CLEARS, and the reason is one transferred number: HCQ's potency
    (0.10 assumed -> 0.28 from a human IC50 and the measured canine tumour concentration)."""
    out = {}
    for (comp, ip), rec in S1.MINIMAL_CLOSING.items():
        if rec[0] is None:
            continue
        names = [n.strip() for n in rec[0].split(" + ")]
        out[(comp, ip)] = "RESPONSE THEN RELAPSE" in L.regimen_summary(comp, ip, names)["strict_window"]
    assert out[(SYSTEMIC, B)] and out[(CNS, B)]
    assert not out[(SYSTEMIC, T)]


def test_v1_t_cell_robust_regimen_needs_derating_under_organ_budgets():
    rec = S1.MOST_ROBUST[(SYSTEMIC, T)]
    s = L.regimen_summary(SYSTEMIC, T, rec["agents"])
    assert s["derated"] and s["tightest_axis_headroom"] < 0
    assert s["worst_margin"] < rec["worst_margin"]


# ---------- the answer, at the strength shown ----------

@pytest.mark.parametrize("comp,ip,tier", [(SYSTEMIC, B, "off-label"), (SYSTEMIC, T, "off-label"),
                                          (SYSTEMIC, T, "trial"), (CNS, B, "off-label"),
                                          (CNS, T, "off-label"), (CNS, T, "trial"), (CNS, B, "trial")])
def test_these_cells_have_no_strict_grade_regimen_that_clears_every_lineage(comp, ip, tier):
    res = G.search(comp, ip, tier, pool=_pool(comp, ip, tier, G.STRICT_GRADES))
    assert not res["cured_inside_window"]


def test_systemic_b_cell_has_a_regimen_of_only_strict_grade_agents_once_cytarabine_is_derived():
    """Canine anti-CD20 antibody (measured) + verdinexor (derived) + cytarabine CRI (derived from the
    measured plasma steady state and canine-lymphoma-line IC50). Needs the trial-stage antibody."""
    res = G.search(SYSTEMIC, B, "trial", pool=_pool(SYSTEMIC, B, "trial", G.STRICT_GRADES))
    assert res["cured_inside_window"]
    best = min(res["cured_inside_window"], key=lambda e: (len(e.agents), -e.worst_derated))
    assert {n.split(" (")[0] for n in best.names} == {"anti-CD20 monoclonal antibody", "verdinexor",
                                                      "cytarabine CRI"}
    assert best.worst_derated == pytest.approx(0.101, abs=0.01)
    assert best.assumed == 0


def test_no_regimen_may_contain_two_versions_of_one_drug():
    for res in (G.search(SYSTEMIC, B, "trial", max_n=5), G.search(CNS, B, "trial", max_n=5)):
        for ev in res["cured_inside_window"] + res["top_by_margin"]:
            assert G.one_per_family(ev.agents), ev.names


def test_cytarabine_is_derived_in_the_cns_from_the_measured_csf_concentration():
    """CSF steady state 8.3 uM, CSF:plasma 0.62 (PMID 1742843) against the canine-lymphoma-line IC50."""
    b = gi.cytarabine_cri(B, "cns")
    t = gi.cytarabine_cri(T, "cns")
    assert b.kill_per_day == pytest.approx(1.57, abs=0.03) and t.kill_per_day == pytest.approx(0.66, abs=0.03)
    assert b.fully_measured and t.fully_measured
    assert gi.ARAC_CSF_SS.value / gi.ARAC_PLASMA_SS.value == pytest.approx(0.62, abs=0.14)   # paper: mean of ratios 0.62 +/- 0.14


def test_b_cell_smallest_anchored_set_is_doxorubicin_antibody_verdinexor():
    sets = L.minimal_sets(SYSTEMIC, B, "trial", G.OUTCOME_GRADES)
    best = sets[0]
    assert set(best.names) == {"doxorubicin", "anti-CD20 monoclonal antibody", "verdinexor (XPO1 inhibitor)"}
    assert best.worst_derated == pytest.approx(0.101, abs=0.005)
    assert best.horizon_strict.clear_day == pytest.approx(51, abs=4)
    assert not best.derated and best.assumed == 0


def test_b_cell_off_label_agents_with_anchored_potency_do_not_clear_inside_the_windows():
    assert L.minimal_sets(SYSTEMIC, B, "off-label", G.OUTCOME_GRADES) == []


def test_t_cell_smallest_anchored_set_needs_venetoclax():
    sets = L.minimal_sets(SYSTEMIC, T, "off-label", G.OUTCOME_GRADES)
    assert sets and all(any(n.startswith("venetoclax") for n in s.names) for s in sets[:5])
    assert sets[0].worst_derated < 0.02          # 2-agent set is thin; the 3-agent set has +0.06


def test_cns_has_no_regimen_of_measured_or_outcome_grade_potency_that_clears():
    for ip in (B, T):
        for tier in ("off-label", "trial"):
            res = G.search(CNS, ip, tier, pool=_pool(CNS, ip, tier, G.OUTCOME_GRADES))
            assert not res["cured_inside_window"]


def test_cns_clears_in_the_model_only_on_unmeasured_potencies_and_t_cell_needs_a_buildable_effector():
    for ip in (B, T):
        for tier in ("off-label", "trial"):
            for ev in G.search(CNS, ip, tier)["cured_inside_window"]:
                assert any(n.startswith("cytarabine CRI") for n in ev.names)      # the derived CNS agent
                assert ev.assumed >= 2 and any("radi" in n for n in ev.names)     # radiation is not measured
                if ip == T:
                    assert any(n.startswith(("CD5", "CD7")) for n in ev.names)     # only a T-lineage effector
    for tier in ("off-label", "trial"):
        assert not G.search(CNS, T, tier)["cured_inside_window"]                  # none of it exists
    assert G.search(CNS, T, "any")["cured_inside_window"]                         # ... unless it is built


def test_the_anchored_b_cell_regimen_has_no_single_point_of_failure_and_headroom():
    comp, ip, names = L.LEDGER_REGIMENS["B-cell, best with no assumed potency (trial-stage antibody)"]
    rows = L.escape_ledger(comp, ip, names)
    assert all(not r["single_points_of_failure"] for r in rows)
    assert all(r["closed_on"] != "NOT CLOSED" for r in rows)
    assert any("THIN" in r["closed_on"] for r in rows)         # the TP53 row is +0.009 on strict potency
    hr = L.potency_headroom(comp, ip, names)
    assert all(v < 1.0 for v in hr.values())
    s = L.regimen_summary(comp, ip, names)
    assert s["tightest_axis_headroom"] == pytest.approx(0.25, abs=0.02) and not s["derated"]


def test_the_assumed_potency_b_cell_regimen_is_closed_only_on_assumed_kill():
    comp, ip, names = L.LEDGER_REGIMENS["B-cell, off-label agents only, some potencies ASSUMED"]
    rows = L.escape_ledger(comp, ip, names)
    pgp = next(r for r in rows if "P-glycoprotein" in r["escape"])
    assert pgp["closed_on"].startswith("ASSUMED potency only") and pgp["margin_strict_only"] < 0


def test_dormancy_sweep_shows_the_old_wall_model_is_the_only_corner_that_relapses():
    comp, ip, names = L.LEDGER_REGIMENS["B-cell, best with no assumed potency (trial-stage antibody)"]
    sweep = L.dormancy_sweep(comp, ip, names)
    relapse = [k for k, (_, cleared) in sweep.items() if not cleared]
    assert relapse == [(1.0, 1.0)]


# ---------- the sound-grade rebuild: transfers, radiobiology, the pump, and the closing programs ----------

from dataclasses import replace as _replace


def _esc(ip):
    return tuple(e for e in G.GROUNDED_ESCAPES if not (ip == T and e.removes_antigen in B_LINEAGE_ANTIGENS)
                 and not (ip == B and e.removes_antigen == "CD7"))


def _pick(comp, ip, names):
    ag = {a.name: a for a in G.grounded_agents(comp, ip)}
    return [ag[next(k for k in ag if k.startswith(n))] for n in names if any(k.startswith(n) for k in ag)]


def test_hcq_potency_is_a_labelled_transfer_with_a_written_justification():
    h = gi.hcq_transfer()
    assert h.kill_per_day == pytest.approx(0.284, abs=0.01)
    assert h.ic50.provenance.value == "transferred from another population" and h.ic50.justification
    assert h.concentration.provenance.value == "derived from measured parameters"   # canine tumour conc
    assert G.potency_grade(_pick(SYSTEMIC, B, ["hydroxychloroquine"])[0]) == "TRANSFER"


def test_sound_pool_admits_transfers_but_not_hinges_or_bare_assumptions_and_uses_the_bracket_low_end():
    names = {a.name: a for a in G.sound_pool(G.grounded_agents(SYSTEMIC, B))}
    assert "hydroxychloroquine (autophagy)" in names                 # transfer
    assert "rabacfosadine" not in names and "high-dose methotrexate" not in names   # assumed, no basis
    assert names["prednisolone (glucocorticoid)"].potency == pytest.approx(0.0098)   # bracket LOW end


def test_radiation_kill_is_derived_from_canine_lymphoid_line_survival_and_is_below_what_was_assumed():
    alpha, beta = gi.lq_alpha_beta(*gi.RT_SURVIVAL["CLBL1"])
    assert alpha == pytest.approx(0.154, abs=0.005) and beta == pytest.approx(0.082, abs=0.005)
    assert gi.lq_alpha_beta(*gi.RT_SURVIVAL["CLL1390"])[0] == 0.0     # alpha floored
    assert gi.rt_kill_per_day("craniospinal radiotherapy") == pytest.approx(0.095, abs=0.005)
    assert gi.rt_kill_per_day("craniospinal radiotherapy", "CLBL1") == pytest.approx(0.39, abs=0.02)
    assert gi.rt_kill_per_day("half-body irradiation (low-dose-rate)") < GROWTH_BAR if (GROWTH_BAR := 0.0903) else True
    assert G.potency_grade(_pick(SYSTEMIC, B, ["craniospinal"])[0]) == "PARTIAL"


def test_continuous_intrathecal_cytarabine_requirement_is_small_and_computed():
    b, t = gi.continuous_it_cytarabine(B), gi.continuous_it_cytarabine(T)
    assert b["kill_per_day"] == pytest.approx(1.10, abs=0.03) and t["kill_per_day"] == pytest.approx(0.34, abs=0.03)
    assert b["infusion_mg_per_day"] == pytest.approx(0.19, abs=0.02)      # C x V x k_elim, measured t1/2 113 min


def test_body_regimen_hcq_plus_verdinexor_clears_every_escape_for_b_and_t_with_off_label_and_licensed_agents():
    for ip, margin in ((B, 0.185), (T, 0.064)):
        r = _pick(SYSTEMIC, ip, ["hydroxychloroquine", "verdinexor"])
        ev = G.evaluate_best_schedule(r, _esc(ip), burden=BURDEN_EARLY_DETECTED, compartment=SYSTEMIC)
        assert ev.closes and ev.horizon_strict.cure_inside_window
        assert ev.worst_derated == pytest.approx(margin, abs=0.01)
        assert {G.AVAILABILITY[a.name] for a in r} <= {G.LICENSED, G.OFF_LABEL}
        assert ev.weakest.startswith("P-glycoprotein")        # verdinexor alone carries the pump clones


def test_hcq_plus_verdinexor_depends_on_verdinexor_for_the_pump_clone_and_fails_if_verdinexor_is_a_quarter():
    r = _pick(SYSTEMIC, B, ["hydroxychloroquine", "verdinexor"])
    weak = [r[0], _replace(r[1], potency=r[1].potency * 0.25)]
    assert not G.clears(weak, _esc(B), burden=BURDEN_EARLY_DETECTED, compartment=SYSTEMIC)
    assert not G.clears(G.discounted(r, 0.5), _esc(B), burden=BURDEN_EARLY_DETECTED, compartment=SYSTEMIC)


def test_adding_the_canine_antibody_makes_the_b_cell_body_regimen_survive_halved_potencies():
    r = _pick(SYSTEMIC, B, ["hydroxychloroquine", "verdinexor", "anti-CD20"])
    assert G.clears(G.discounted(r, 0.5), _esc(B), burden=BURDEN_EARLY_DETECTED, compartment=SYSTEMIC)


def test_cns_existing_products_clear_only_a_few_thousand_cells_and_t_cell_nothing():
    esc = _esc(B)
    r = _pick(CNS, B, ["craniospinal", "hydroxychloroquine", "cytarabine CRI (q7"])
    assert 1e2 < G.cns_capacity(r, esc) < 1e4                 # about 1.7e3 cells, far below the 5e6 illustrative
    for tier in ("off-label", "trial"):
        p = G.sound_pool(G.available(G.grounded_agents(CNS, T), tier))
        assert G.search(CNS, T, tier, pool=p, max_n=5)["closing_without_derating"] == 0


def test_the_intrathecal_pump_lets_the_cns_clear_the_whole_assumed_burden_and_is_robust_to_hcq_access():
    for ip, names in ((B, ["hydroxychloroquine", "continuous intrathecal"]),
                      (T, ["hydroxychloroquine", "venetoclax", "continuous intrathecal"])):
        esc, r = _esc(ip), _pick(CNS, ip, names)
        assert G.cns_capacity(r, esc) >= 0.99e8
        weak = [_replace(a, access=0.03) if a.name.startswith("hydroxychloroquine") else a for a in r]
        assert G.cns_capacity(weak, esc) > 1e7                # even at 3% HCQ CNS access


def test_t_cell_cns_program_is_sensitive_to_the_intrathecal_setpoint_unless_a_t_lineage_car_t_is_added():
    esc = _esc(T)
    ven = _pick(CNS, T, ["hydroxychloroquine", "venetoclax", "continuous intrathecal"])
    low = [_replace(a, potency=gi.continuous_it_cytarabine(T, 300.0)["kill_per_day"])
           if a.name.startswith("continuous") else a for a in ven]
    assert G.cns_capacity(low, esc) < 1e4
    car = _pick(CNS, T, ["hydroxychloroquine", "verdinexor", "continuous intrathecal", "CD7-directed"])
    lowc = [_replace(a, potency=gi.continuous_it_cytarabine(T, 1000.0)["kill_per_day"])
            if a.name.startswith("continuous") else a for a in car]
    assert G.cns_capacity(lowc, esc) >= 0.99e8


def test_the_b_cell_program_union_is_within_every_organ_budget():
    from canine_dsp.core.lymphoma_toxicity import axis_loads
    r = _pick(CNS, B, ["hydroxychloroquine", "verdinexor", "continuous intrathecal", "anti-CD20"])
    loads = axis_loads(G.regimen_profiles(r, 1.43))
    assert max(loads.values()) <= 1.0


def test_programs_close_body_and_cns_at_model_level():
    from canine_dsp.lymphoma_coverage_ledger import PROGRAMS, program_report
    for label in PROGRAMS:
        r = program_report(label)
        assert r["body"]["closes"] and r["cns"]["closes"], label
        assert r["cns"]["capacity_cells"] >= 1e7, label
        # honesty check: no program is redundant to losing an agent
        assert not r["body"]["any_one_removed_clears"], label
    assert program_report("B-cell")["body"]["halved_potency_clears"]
    assert not program_report("T-cell, existing drugs plus the pump")["body"]["halved_potency_clears"]
