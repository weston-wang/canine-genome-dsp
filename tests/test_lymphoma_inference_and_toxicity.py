"""Tests for the 2yr->10yr durability inference and the toxicity/potency analysis. The
conditional_durability helper is checked deterministically on a hand-built outcome; the regime and
de-rating figures are recomputed from the engine at the trial counts they were recorded at."""
import numpy as np
import pytest

from canine_dsp import lymphoma_scenarios as ls
from canine_dsp.lymphoma_durability_inference import TWO_YEAR_INFERENCE, conditional_durability
from canine_dsp.lymphoma_toxicity import (
    CHEMO_DERATING_CHEMO_ONLY, CHEMO_DERATING_IN_COMBINATION,
    IMMUNOTHERAPY_POTENCY_IS_LOAD_BEARING, PGP_REVERSAL_DRUG_SIDE_CLOSURE, TOXICITY_LEDGER,
)
from canine_dsp.mapk_resistance import run_monte_carlo, run_monte_carlo_with_vaccine

P = ls._PREEXISTING_PROB_CENTRAL
S, R = ls.LYMPHOMA_IMMUNOTHERAPY_START_DAY, ls.LYMPHOMA_IMMUNOTHERAPY_RAMP_DAYS


# ---------- conditional_durability helper (deterministic) ----------

def test_conditional_durability_math_on_a_handbuilt_outcome():
    # 5 trials: [never, relapse@100, relapse@800, relapse@2000, never]
    progressed = np.array([False, True, True, True, False])
    ttp = np.array([np.nan, 100.0, 800.0, 2000.0, np.nan])
    mech = ["durable_response", "mdr1_pgp_efflux", "cd20_antigen_loss", "mdr1_pgp_efflux",
            "durable_response"]
    r = conditional_durability(progressed, ttp, mech, early_day=730, late_day=3650)
    # disease-free @730: not progressed OR ttp>730 -> trials 0,2,3,4 = 4/5
    assert r["disease_free_early"] == pytest.approx(0.8)
    # disease-free @3650: trials 0,4 -> 2/5
    assert r["disease_free_late"] == pytest.approx(0.4)
    assert r["conditional_late_given_early"] == pytest.approx(0.5)
    # late relapses (df@2y that relapse in (730,3650]): trials 2 (800) and 3 (2000) = 2
    assert r["late_relapse_count"] == 2
    assert r["late_relapse_mechanisms"] == {"cd20_antigen_loss": 1, "mdr1_pgp_efflux": 1}
    assert r["median_relapse_day"] == pytest.approx(800.0)


def test_conditional_durability_rejects_empty():
    with pytest.raises(ValueError):
        conditional_durability(np.array([], dtype=bool), np.array([]), [])


# ---------- the 2yr->10yr inference across regimes ----------

def _immuno_outcome(vmk, trials=400, escape_mult=1.0):
    scen = ls.lymphoma_immunotherapy_followon_scenarios(immunotherapy_max_kill_values=[vmk])
    m, c, s, _ = scen[vmk]
    return run_monte_carlo_with_vaccine(
        m, c, 3650, s, vaccine_start_day=S, vaccine_ramp_days=R, vaccine_max_kill=vmk,
        immune_escape_seeding_rate=ls.LYMPHOMA_CD20_LOSS_SEEDING_RATE * escape_mult,
        clone_names=ls.LYMPHOMA_IMMUNOTHERAPY_CLONE_NAMES, trials=trials, preexisting_prob=P, seed=7)


def test_below_the_bar_relapse_is_frontloaded_so_2yr_predicts_10yr():
    o = _immuno_outcome(0.06)
    r = conditional_durability(o.progressed, o.time_to_progression, o.dominant_mechanism)
    assert r["conditional_late_given_early"] == pytest.approx(1.0, abs=0.03)
    assert r["late_relapse_count"] <= 2
    assert r["p90_relapse_day"] < 730   # essentially all relapse within the first two years


def test_at_the_bar_has_a_small_late_tail_dominated_by_drug_resistance():
    o = _immuno_outcome(0.09)
    r = conditional_durability(o.progressed, o.time_to_progression, o.dominant_mechanism)
    rec = TWO_YEAR_INFERENCE["at_the_bar_immuno_0_09"]
    assert r["conditional_late_given_early"] == pytest.approx(rec["conditional"], abs=0.03)
    assert 0.0 < r["late_relapse_hazard"] < 0.08          # a real but small tail
    # the tail is drug resistance, not antigen loss
    loss = r["late_relapse_mechanisms"].get("cd20_antigen_loss", 0)
    pgp = r["late_relapse_mechanisms"].get("mdr1_pgp_efflux", 0)
    assert pgp > loss
    assert r["p90_relapse_day"] > 1500   # the tail is genuinely spread across the decade


def test_above_the_bar_has_no_late_tail_so_2yr_equals_10yr():
    o = _immuno_outcome(0.12)
    r = conditional_durability(o.progressed, o.time_to_progression, o.dominant_mechanism)
    assert r["conditional_late_given_early"] == pytest.approx(1.0, abs=0.01)
    assert r["late_relapse_count"] == 0


def test_tandem_removes_the_antigen_loss_late_relapse_but_not_the_drug_tail():
    o = _immuno_outcome(0.09, escape_mult=0.0)
    r = conditional_durability(o.progressed, o.time_to_progression, o.dominant_mechanism)
    assert r["late_relapse_mechanisms"].get("cd20_antigen_loss", 0) == 0
    assert r["late_relapse_mechanisms"].get("mdr1_pgp_efflux", 0) >= 3   # drug tail persists


# ---------- toxicity vs potency ----------

def test_chemo_derating_is_durability_neutral_alone():
    model, css, seeding, _ = ls.dog_lymphoma_preset("B")
    full = 1 - run_monte_carlo(model, css, 3650, seeding, 300, preexisting_prob=P, seed=7).progressed.mean()
    derated = 1 - run_monte_carlo(model, css * 0.4, 3650, seeding, 300, preexisting_prob=P,
                                  seed=7).progressed.mean()
    assert full == pytest.approx(CHEMO_DERATING_CHEMO_ONLY[1.0], abs=0.05)
    assert derated == pytest.approx(CHEMO_DERATING_CHEMO_ONLY[0.4], abs=0.05)
    assert abs(full - derated) < 0.06   # de-rating chemo alone barely moves durability


def test_chemo_derating_costs_durability_inside_the_curative_combination():
    scen = ls.lymphoma_immunotherapy_followon_scenarios(immunotherapy_max_kill_values=[0.09])
    m, c, s, _ = scen[0.09]

    def combo(d):
        o = run_monte_carlo_with_vaccine(
            m, c * d, 3650, s, vaccine_start_day=S, vaccine_ramp_days=R, vaccine_max_kill=0.09,
            immune_escape_seeding_rate=ls.LYMPHOMA_CD20_LOSS_SEEDING_RATE,
            clone_names=ls.LYMPHOMA_IMMUNOTHERAPY_CLONE_NAMES, trials=300, preexisting_prob=P, seed=7)
        return 1 - o.progressed.mean()

    full, derated = combo(1.0), combo(0.6)
    assert full == pytest.approx(CHEMO_DERATING_IN_COMBINATION[1.0], abs=0.05)
    assert derated == pytest.approx(CHEMO_DERATING_IN_COMBINATION[0.6], abs=0.06)
    assert full - derated > 0.07   # cytoreduction depth is partly load-bearing for durability


def test_immunotherapy_potency_is_a_cliff_not_a_gradient():
    # its potency cannot be de-rated the way a toxic small molecule can
    assert IMMUNOTHERAPY_POTENCY_IS_LOAD_BEARING[0.09] - IMMUNOTHERAPY_POTENCY_IS_LOAD_BEARING[0.06] > 0.5


def test_toxicity_ledger_and_pgp_reversal_carry_real_citations():
    assert len(TOXICITY_LEDGER) >= 5
    assert all("toxicity" in row and "potency_role" in row and "de_ratable" in row
               for row in TOXICITY_LEDGER)
    # the fatal pulmonary-fibrosis signal for rabacfosadine is recorded
    rab = next(r for r in TOXICITY_LEDGER if "Rabacfosadine" in r["agent"])
    assert "pulmonary fibrosis" in rab["toxicity"]
    # the drug-side P-gp closure cites the real disease-specific chemosensitization paper
    assert "33961622" in PGP_REVERSAL_DRUG_SIDE_CLOSURE["disease_specific_chemosensitization"]
    assert "24975508" in PGP_REVERSAL_DRUG_SIDE_CLOSURE["in_vitro_reversal"]
