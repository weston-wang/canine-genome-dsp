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
    """HBI alone: 0.30/day inside a 28-day course clears the 1-cell pump lineage in days, though its
    annual-average duty (28/365) would suggest it does almost nothing."""
    hbi = next(a for a in G.grounded_agents(SYSTEMIC, B) if a.name.startswith("half-body"))
    hz = horizon([G.in_window(hbi)], [G.PGP], {hbi.name: 28.0}, 1e8, 0.0903,
                 margin_fn=lambda act, e: G.margin_for(act, e), always_present=(G.PGP.name,),
                 kill_of=lambda a: G.in_window(a).effective_kill)
    pgp = next(o for o in hz.outcomes if o.name == G.PGP.name)
    assert pgp.outcome == "cleared" and pgp.day < 5
    assert hbi.effective_kill < 0.03            # the annual average that hid this


def test_chop_alone_at_clinical_burden_is_not_predicted_to_cure():
    """Calibration against real outcome: median PFS 176 d (PMID 26279153), ~10% alive at 2 y
    (PMID 21320018). The model must predict response then relapse, in the right order of days."""
    c = L.calibration_chop()
    assert not c["cured"]
    days = dict(c["relapse_days"])
    assert 100 <= days["drug-sensitive bulk"] <= 200


# ---------- what changed from v1 ----------

def test_v1_recorded_margins_are_reproduced_for_the_regimens_v1_recorded():
    for (comp, ip), rec in S1.MOST_ROBUST.items():
        if rec is None or (comp, ip) == (SYSTEMIC, T):
            continue
        s = L.regimen_summary(comp, ip, rec["agents"])
        assert s["worst_margin"] == pytest.approx(rec["worst_margin"], abs=0.002)


def test_every_v1_minimal_closing_regimen_fails_the_clock():
    for (comp, ip), rec in S1.MINIMAL_CLOSING.items():
        if rec[0] is None:
            continue
        names = [n.strip() for n in rec[0].split(" + ")]
        s = L.regimen_summary(comp, ip, names)
        assert "RESPONSE THEN RELAPSE" in s["strict_window"], (comp, ip, rec[0])


def test_v1_cns_b_cell_closure_relapses_when_the_car_t_must_stop():
    comp, ip = CNS, B
    s = L.regimen_summary(comp, ip, S1.MOST_ROBUST[(comp, ip)]["agents"])
    assert "RESPONSE THEN RELAPSE" in s["strict_window"]


def test_v1_t_cell_robust_regimen_needs_derating_under_organ_budgets():
    rec = S1.MOST_ROBUST[(SYSTEMIC, T)]
    s = L.regimen_summary(SYSTEMIC, T, rec["agents"])
    assert s["derated"] and s["tightest_axis_headroom"] < 0
    assert s["worst_margin"] < rec["worst_margin"]


# ---------- the answer, at the strength shown ----------

@pytest.mark.parametrize("comp,ip,tier", [(SYSTEMIC, B, "off-label"), (SYSTEMIC, T, "off-label"),
                                          (SYSTEMIC, T, "trial"), (CNS, B, "off-label"),
                                          (CNS, T, "off-label")])
def test_no_regimen_closes_every_escape_using_strict_grade_potencies_alone(comp, ip, tier):
    res = G.search(comp, ip, tier, pool=_pool(comp, ip, tier, G.STRICT_GRADES))
    assert res["closing_after_derating"] == 0 and not res["cured_inside_window"]


def test_two_strict_agents_cover_b_cell_but_do_not_clear_inside_the_windows():
    res = G.search(SYSTEMIC, B, "trial", pool=_pool(SYSTEMIC, B, "trial", G.STRICT_GRADES))
    assert res["closing_after_derating"] == 1 and not res["cured_inside_window"]
    only = res["top_by_margin"][0]
    assert set(only.names) == {"anti-CD20 monoclonal antibody", "verdinexor (XPO1 inhibitor)"}
    assert only.worst_derated == pytest.approx(0.009, abs=0.003)     # razor thin
    assert "verdinexor" in only.horizon_strict.verdict()             # it must stop at its 56-day window


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


def test_cns_is_open_at_every_evidence_grade():
    """With potencies limited to strict or outcome grade no regimen closes the sanctuary at all."""
    for ip in (B, T):
        for tier in ("off-label", "trial"):
            outcome = G.search(CNS, ip, tier, pool=_pool(CNS, ip, tier, G.OUTCOME_GRADES))
            assert outcome["closing_after_derating"] == 0


def test_cns_closes_in_the_model_only_through_a_trial_stage_cell_therapy_on_assumed_potency():
    off = G.search(CNS, B, "off-label")
    assert not off["cured_inside_window"]                       # nothing licensed or off-label clears it
    trial = G.search(CNS, B, "trial")
    assert trial["cured_inside_window"]
    for ev in trial["cured_inside_window"]:
        assert "CD20 CAR-T" in ev.names                          # the cell that crosses the barrier
        assert ev.assumed >= 4                                   # and four of five potencies assumed
    # T-cell: no obtainable agent does it, even trial-stage; only the non-existent T-lineage effector
    for tier in ("off-label", "trial"):
        assert not G.search(CNS, T, tier)["cured_inside_window"]
    any_t = G.search(CNS, T, "any")
    assert any_t["cured_inside_window"]
    assert all(any(n.startswith("CD5/CD52") for n in ev.names) for ev in any_t["cured_inside_window"])


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
