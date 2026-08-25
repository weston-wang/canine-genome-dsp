import numpy as np
import pytest
from dataclasses import replace

from canine_dsp import hsa_scenarios as hs
from canine_dsp.hsa_gap_stack import corrected_ic50
from canine_dsp.hsa_growth_pharmacodynamics import TWO_KINDS_OF_NEGATIVE_TRIAL
from canine_dsp.hsa_parallel_pathway import (
    BAR_BEFORE_SECOND_DRUG, CANINE_HSA_RUNS_ON_mTORC2, COMBINATION_HAS_BEEN_DOSED_IN_DOGS,
    EXPOSURE_CRITERION, MEK_ALONE_FAILS_IN_CANINE_HSA, MEK_KILL_NEEDED_PER_DAY,
    MEK_KILL_NEEDED_AT_SATURATING_EXPOSURE, MEK_PLUS_mTOR_SYNERGY,
    MEK_RELATIVE_EFFICACY_BY_CLONE, SAPANISERTIB_CMAX_nM,
    TRAMETINIB_CANINE_EXPOSURE, TRAMETINIB_MW_G_PER_MOL, TRAMETINIB_STEADY_STATE_nM, VERDICT,
    ng_per_ml_to_nM, with_mek_inhibitor,
)
from canine_dsp.mapk_resistance import clone_growth_margins

VACCINE_REAL = 0.03


def _corrected():
    m5, css, seeding, _ = hs.hsa_vaccine_followon_scenarios(
        vaccine_max_kill_values=[VACCINE_REAL])[VACCINE_REAL]
    return replace(m5, ic50_nM=corrected_ic50(m5.ic50_nM[0])), css


def _bar(mek_kill, concentration_2=None):
    model, css = _corrected()
    if not mek_kill:
        return float(clone_growth_margins(model, css)[:4].max())
    model = with_mek_inhibitor(model, np.full(5, mek_kill), ic50_nM_2=11.0)
    conc2 = TRAMETINIB_STEADY_STATE_nM if concentration_2 is None else concentration_2
    return float(clone_growth_margins(model, css, concentration_2=conc2)[:4].max())


# ---------- unit conversion ----------

def test_ng_per_ml_to_nM_and_its_validation():
    assert ng_per_ml_to_nM(10.0, TRAMETINIB_MW_G_PER_MOL) == pytest.approx(16.25, abs=0.05)
    assert ng_per_ml_to_nM(0.0, 500.0) == 0.0
    with pytest.raises(ValueError):
        ng_per_ml_to_nM(-1.0, 500.0)
    with pytest.raises(ValueError):
        ng_per_ml_to_nM(10.0, 0.0)


# ---------- why rapamycin is the wrong drug for this disease ----------

def test_canine_hsa_runs_on_mtorc2_which_rapalogs_do_not_block():
    m = CANINE_HSA_RUNS_ON_mTORC2
    assert "22839755" in m["citation"]
    assert "22789858" in m["tumour_confirmation"]
    assert "35%" in m["tumour_confirmation"], "only a third of tumours show active mTORC1"
    assert "independently of mTORC1" in m["authors_conclusion"]
    assert "insensitive to mTOR inhibition" in m["independent_confirmation"]


# ---------- the measured synergy ----------

def test_the_synergy_is_measured_in_canine_angiosarcoma_and_is_strong():
    s = MEK_PLUS_mTOR_SYNERGY
    assert "25955301" in s["citation"]
    assert "canine" in s["system"]
    assert s["combination_index"] < 1.0, "CI below 1 is synergy"
    assert s["combination_index"] <= 0.08
    assert s["potency_shift_fold"] == pytest.approx(150.0 / 11.0, rel=1e-6)
    assert s["potency_shift_fold"] > 13
    assert s["ic50_nM"]["combined_4to1"] < s["ic50_nM"]["mek_alone"]


def test_neither_node_is_a_monotherapy_target_in_this_disease():
    """Two independent groups, same conclusion: the MAPK arm alone does nothing here."""
    assert "27408334" in MEK_ALONE_FAILS_IN_CANINE_HSA["citation"]
    assert "did not affect canine HSA cell viability" in MEK_ALONE_FAILS_IN_CANINE_HSA["finding"]
    assert "not a monotherapy target" in MEK_ALONE_FAILS_IN_CANINE_HSA["consistency"]
    assert MEK_PLUS_mTOR_SYNERGY["ic50_nM"]["rapamycin_alone"].startswith(">50")


# ---------- the exposure criterion, applied to a third candidate ----------

def test_trametinib_misses_as_monotherapy_and_clears_in_combination():
    """The whole point: the synergy is what pulls the requirement into reach."""
    e = EXPOSURE_CRITERION
    assert TRAMETINIB_STEADY_STATE_nM == pytest.approx(16.25, abs=0.1)
    assert e["monotherapy_fold_short"] > 9, "9x short alone"
    assert e["combination_fold_margin"] > 1.0, "clears in combination"
    assert e["combination_fold_margin"] == pytest.approx(
        TRAMETINIB_STEADY_STATE_nM / 11.0, rel=1e-6)
    assert e["needed_as_monotherapy_nM"] > TRAMETINIB_STEADY_STATE_nM
    assert e["needed_in_combination_nM"] < TRAMETINIB_STEADY_STATE_nM


def test_this_is_the_first_candidate_to_pass_the_criterion():
    """Propranolol fails on exposure, toceranib on biology, this one passes both so far."""
    assert TWO_KINDS_OF_NEGATIVE_TRIAL["propranolol"]["cleared_its_exposure_bar"] is False
    assert TWO_KINDS_OF_NEGATIVE_TRIAL["toceranib"]["cleared_its_exposure_bar"] is True
    assert VERDICT["passes_the_exposure_criterion"] is True
    assert "tumorgrafts" in EXPOSURE_CRITERION["why_this_is_the_first_pass"]


def test_the_substitution_between_mek_inhibitors_is_flagged_not_hidden():
    caveat = EXPOSURE_CRITERION["the_substitution_caveat"]
    assert "PD0325901" in caveat and "trametinib" in caveat
    assert "not\nrigorous" in caveat or "not rigorous" in caveat


def test_the_missing_target_engagement_is_recorded():
    """Unlike toceranib, engagement was looked for in canine tumours and not found."""
    gap = TRAMETINIB_CANINE_EXPOSURE["the_honest_gap"]
    assert "NOT observed" in gap
    assert "weaker than toceranib" in gap
    assert TRAMETINIB_CANINE_EXPOSURE["fraction_of_dogs_reaching_it"] < 1.0


def test_the_pair_has_actually_been_given_to_dogs_together():
    c = COMBINATION_HAS_BEEN_DOSED_IN_DOGS
    assert "36590793" in c["citation"]
    assert "without dose limiting toxicity" in c["tolerability"]
    assert "32943547" in c["efficacy_precedent"]
    assert SAPANISERTIB_CMAX_nM == pytest.approx(85.0, abs=1.0)
    assert "not a proposed combination" in c["why_it_matters"]


# ---------- the second drug in the engine ----------

def test_with_mek_inhibitor_attaches_a_per_clone_second_drug_and_validates():
    model, _ = _corrected()
    combined = with_mek_inhibitor(model, np.full(5, 0.02), ic50_nM_2=11.0)
    assert combined.max_kill_2.shape == (5,)
    assert combined.ic50_nM_2 == 11.0
    assert model.ic50_nM_2 is None, "the original model is not mutated"
    with pytest.raises(ValueError):
        with_mek_inhibitor(model, np.full(3, 0.02), ic50_nM_2=11.0)
    with pytest.raises(ValueError):
        with_mek_inhibitor(model, np.full(5, -0.01), ic50_nM_2=11.0)


def test_the_relative_efficacy_weights_are_deliberately_flat():
    """Weighting towards the MAPK clone would flatter the result; the crosstalk data argues
    against that specificity, so the weights stay flat and the rationale says why."""
    weights = [v for k, v in MEK_RELATIVE_EFFICACY_BY_CLONE.items() if isinstance(v, float)]
    assert len(weights) == 5
    assert all(w == 1.0 for w in weights)
    assert "would flatter the result" in MEK_RELATIVE_EFFICACY_BY_CLONE["rationale"]


def test_the_second_drug_lowers_the_bar_monotonically():
    assert _bar(0.0) == pytest.approx(BAR_BEFORE_SECOND_DRUG, abs=0.002)
    bars = [_bar(mk) for mk in (0.0, 0.005, 0.010, 0.020, 0.030)]
    assert all(b > n for b, n in zip(bars, bars[1:])), "more kill, lower bar"
    assert bars[-1] < VACCINE_REAL, "enough MEK kill clears the vaccine's real potency"


def test_the_required_mek_kill_is_recomputed_and_sits_in_a_plausible_range():
    """The ask must be checked against what the model already grants the primary drug."""
    required = MEK_KILL_NEEDED_PER_DAY
    assert _bar(required * 1.05) < VACCINE_REAL
    assert _bar(required * 0.5) > VACCINE_REAL
    model, _ = _corrected()
    assert required < float(model.max_kill[0]), "far below the sensitive-clone kill rate"
    assert required <= float(model.max_kill.max())


def test_a_saturating_dose_would_ask_less_which_is_why_exposure_matters():
    """At 16 nM the Emax term is about 0.64, so the achievable ask exceeds the saturating one."""
    at_achievable = MEK_KILL_NEEDED_PER_DAY
    lo, hi = 0.0, 0.1
    for _ in range(50):
        mid = (lo + hi) / 2
        if _bar(mid, concentration_2=100_000.0) > VACCINE_REAL:
            lo = mid
        else:
            hi = mid
    assert hi < at_achievable, "saturating exposure would need less kill than we can deliver at"
    assert hi == pytest.approx(MEK_KILL_NEEDED_AT_SATURATING_EXPOSURE, abs=0.002)


# ---------- what the verdict claims, and what it refuses to claim ----------

def test_the_verdict_covers_each_mechanism_and_names_the_one_it_does_not():
    cover = VERDICT["mechanism_coverage"]
    for mechanism in ("pi3k_akt_feedback_reactivation", "mapk_crosstalk_bypass",
                      "target_site_mutation"):
        assert mechanism in cover
    assert "NOT covered" in cover["kinase_domain_mutation"]
    assert "RapaLink-1" in cover["kinase_domain_mutation"]
    assert "no canine data" in cover["kinase_domain_mutation"]
    assert "sets the bar" in cover["pi3k_akt_feedback_reactivation"]


def test_the_verdict_does_not_overclaim():
    assert "hypothesis rather" in VERDICT["honest_status"]
    assert "not that durability has been proven" in VERDICT["honest_status"]
    assert "per-clone kill rates" in VERDICT["what_is_not_measured"]
    assert "target engagement" in VERDICT["what_is_not_measured"]
