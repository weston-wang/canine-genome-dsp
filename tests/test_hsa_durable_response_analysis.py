"""Every quantitative claim in `hsa_durable_response_analysis` is recomputed here from the engine,
so the module's prose cannot drift away from what the code actually produces."""
import numpy as np
import pytest
from dataclasses import replace

from canine_dsp import hsa_scenarios as hs
from canine_dsp import mapk_scenarios as ms
from canine_dsp.hsa_durable_response_analysis import (
    DURABILITY_BAR_PER_DAY, ESCAPE_ROUTES, MECHANISM_LEDGER, RAPAMYCIN_REAL_EXPOSURE,
    VACCINE_ACHIEVABILITY, WHAT_WOULD_CHANGE_THE_ANSWER,
)
from canine_dsp.mapk_resistance import clone_growth_margins, run_monte_carlo, run_monte_carlo_with_vaccine


def _bar(css):
    """Largest growth margin over the antigen-positive clones -- what a vaccine must out-kill."""
    model, _, _, _ = hs.dog_hsa_preset()
    return float(clone_growth_margins(model, css).max())


def test_the_bar_is_nearly_unchanged_by_the_drug():
    """The load-bearing claim: the inhibitor moves the durability bar by ~7%, so it decides
    response speed and almost nothing about whether the disease returns."""
    _, css, _, _ = hs.dog_hsa_preset()
    full = _bar(css)
    no_drug = _bar(0.0)
    assert full == pytest.approx(DURABILITY_BAR_PER_DAY["assumed_5x_ic50_module_default"], abs=1e-3)
    assert no_drug == pytest.approx(DURABILITY_BAR_PER_DAY["no_drug_at_all"], abs=1e-3)
    assert (no_drug - full) / no_drug < 0.08


def test_toxicity_derating_barely_moves_the_bar_because_the_drug_was_not_carrying_it():
    _, css, _, _ = hs.dog_hsa_preset()
    derated = _bar(css * min(hs.HSA_COMBINED_EXPOSURE_DERATING))
    assert derated == pytest.approx(DURABILITY_BAR_PER_DAY["derated_to_40pct_for_toxicity"], abs=1e-3)
    assert abs(derated - _bar(css)) < 0.001


def test_real_rapamycin_trough_is_50x_below_the_real_cell_line_ic50():
    """Paoloni 2010's >10 ng/mL trough against Pyuen 2018's 543 nM mean IC50."""
    model, _, _, _ = hs.dog_hsa_preset()
    trough_nM = (10e-9 / 1e-3) / RAPAMYCIN_REAL_EXPOSURE["molecular_weight_g_per_mol"] * 1e9
    assert trough_nM == pytest.approx(RAPAMYCIN_REAL_EXPOSURE["trough_nM"], abs=0.05)
    assert model.ic50_nM[0] == pytest.approx(RAPAMYCIN_REAL_EXPOSURE["vdc597_ic50_nM"], abs=0.1)
    assert model.ic50_nM[0] / trough_nM == pytest.approx(RAPAMYCIN_REAL_EXPOSURE["fold_below_ic50"],
                                                         rel=0.02)


def test_at_real_rapamycin_exposure_even_the_sensitive_clone_is_not_suppressed():
    """The consequence the preset's docstring names the mismatch for but does not state."""
    model, _, _, _ = hs.dog_hsa_preset()
    trough = RAPAMYCIN_REAL_EXPOSURE["trough_nM"]
    treated = clone_growth_margins(model, trough)[0]
    untreated = clone_growth_margins(model, 0.0)[0]
    assert treated > 0, "real exposure should leave the sensitive clone growing"
    assert (untreated - treated) / untreated < 0.02, "and barely distinguishable from no drug"


def _one_year_durable(vaccine_max_kill, trials=400):
    m5, css5, seeding, _ = hs.hsa_vaccine_followon_scenarios(
        vaccine_max_kill_values=[vaccine_max_kill])[vaccine_max_kill]
    out = run_monte_carlo_with_vaccine(
        m5, css5, 365, seeding, vaccine_start_day=hs.HSA_VACCINE_START_DAY,
        vaccine_ramp_days=hs.HSA_VACCINE_RAMP_DAYS, vaccine_max_kill=vaccine_max_kill,
        immune_escape_seeding_rate=hs.HSA_IMMUNE_ESCAPE_SEEDING_RATE,
        clone_names=hs.HSA_VACCINE_CLONE_NAMES, trials=trials,
        preexisting_prob=hs._PREEXISTING_PROB_CENTRAL, seed=7)
    return 1 - out.progressed.mean()


@pytest.mark.parametrize("vaccine_max_kill", [0.0, 0.03])
def test_recorded_one_year_curve_matches_the_engine(vaccine_max_kill):
    expected = VACCINE_ACHIEVABILITY["engine_one_year_durable_by_potency"][vaccine_max_kill]
    assert _one_year_durable(vaccine_max_kill) == pytest.approx(expected, abs=0.05)


def test_real_trial_implied_potency_falls_short_of_the_bar():
    """Both real canine HSA vaccine trials buy ~+30pp of 1-year survival. The engine reaches
    +30pp at ~0.03/day. The bar is ~0.052/day."""
    gains = [t["gain_pp"] for t in VACCINE_ACHIEVABILITY["real_trials"]]
    assert all(28 <= g <= 32 for g in gains), "both trials should sit near +30pp"

    baseline = _one_year_durable(0.0)
    implied = _one_year_durable(VACCINE_ACHIEVABILITY["implied_vaccine_max_kill"])
    assert (implied - baseline) * 100 == pytest.approx(np.mean(gains), abs=6.0)

    _, css, _, _ = hs.dog_hsa_preset()
    assert VACCINE_ACHIEVABILITY["implied_vaccine_max_kill"] < _bar(css), "implied potency is short"
    assert _bar(css) / VACCINE_ACHIEVABILITY["implied_vaccine_max_kill"] == pytest.approx(1.7, abs=0.2)


def test_below_the_bar_relapses_are_drug_resistance_not_antigen_loss():
    """Route 3 sets the bar; route 4 is not what is binding."""
    vmk = 0.05
    m5, css5, seeding, _ = hs.hsa_vaccine_followon_scenarios(vaccine_max_kill_values=[vmk])[vmk]
    out = run_monte_carlo_with_vaccine(
        m5, css5, 3650, seeding, vaccine_start_day=hs.HSA_VACCINE_START_DAY,
        vaccine_ramp_days=hs.HSA_VACCINE_RAMP_DAYS, vaccine_max_kill=vmk,
        immune_escape_seeding_rate=hs.HSA_IMMUNE_ESCAPE_SEEDING_RATE,
        clone_names=hs.HSA_VACCINE_CLONE_NAMES, trials=300,
        preexisting_prob=hs._PREEXISTING_PROB_CENTRAL, seed=7)
    relapses = int(out.progressed.sum())
    antigen_loss = sum(1 for m in out.dominant_mechanism if m == "immune_escape")
    assert relapses > 5, "0.05 sits below the bar, so some relapses must occur"
    assert antigen_loss / relapses < 0.15, "and they should overwhelmingly not be antigen loss"


def test_a_persistent_agnostic_term_closes_the_antigen_loss_route_at_the_recorded_potency():
    """Worst case: 1000x the assumed antigen-loss rate, at threshold vaccine potency."""
    vmk = 0.06
    m5, css5, seeding, _ = hs.hsa_vaccine_followon_scenarios(vaccine_max_kill_values=[vmk])[vmk]
    with_agnostic = replace(m5, ic50_nM_2=hs.HSA_EBAT_ILLUSTRATIVE_IC50_NM, max_kill_2=0.05)
    out = run_monte_carlo_with_vaccine(
        with_agnostic, css5, 3650, seeding, vaccine_start_day=hs.HSA_VACCINE_START_DAY,
        vaccine_ramp_days=hs.HSA_VACCINE_RAMP_DAYS, vaccine_max_kill=vmk,
        immune_escape_seeding_rate=hs.HSA_IMMUNE_ESCAPE_SEEDING_RATE * 1000,
        clone_names=hs.HSA_VACCINE_CLONE_NAMES, trials=300,
        preexisting_prob=hs._PREEXISTING_PROB_CENTRAL,
        css_reference_2=hs.HSA_EBAT_ILLUSTRATIVE_CSS_NM, seed=7)
    assert 1 - out.progressed.mean() == pytest.approx(1.0, abs=0.02)


def test_the_escape_clone_margin_is_positive_regardless_of_drug_exposure():
    """Why route 4 needs a mechanism-agnostic term rather than more vaccine or more drug."""
    m5, css, _, _ = hs.hsa_vaccine_followon_scenarios(vaccine_max_kill_values=[0.05])[0.05]
    for exposure in (css, RAPAMYCIN_REAL_EXPOSURE["trough_nM"], 0.0):
        assert clone_growth_margins(m5, exposure)[4] > 0.04


def test_splenectomy_raises_durable_response_so_it_cannot_explain_the_recentering():
    """The hypothesis that preexisting_prob 0.30->0.70 was compensating for unmodelled resection
    is FALSE -- modelling resection moves durable response away from the eBAT benchmark."""
    model, css, seeding, _ = hs.dog_hsa_preset()
    post_splenectomy = 0.3 * (1 - ms.DEBULKING_FRACTION)
    results = {}
    for burden in (0.3, post_splenectomy):
        out = run_monte_carlo(model, css, 365, seeding, trials=400, preexisting_prob=0.30,
                              initial_burden=burden, seed=7)
        results[burden] = 1 - out.progressed.mean()
    assert results[post_splenectomy] > results[0.3]


def test_hsa_never_uses_the_two_compartment_model_the_hs_pipeline_built():
    """Escape route 7: the less-disseminated disease got two compartments, the more-disseminated
    one did not."""
    from pathlib import Path
    source = Path(__file__).resolve().parents[1] / "src" / "canine_dsp" / "hsa_cli.py"
    assert "run_monte_carlo_two_compartment" not in source.read_text()


def test_every_escape_route_carries_a_status_and_the_closable_one_says_how():
    assert len(ESCAPE_ROUTES) == 7
    for route in ESCAPE_ROUTES:
        assert route["status"] and route["detail"]
    antigen_loss = [r for r in ESCAPE_ROUTES if r["id"] == 4][0]
    assert "how_to_close_it_anyway" in antigen_loss
    open_routes = [r for r in ESCAPE_ROUTES if r["status"].startswith("OPEN")]
    assert len(open_routes) == 3, "rupture, vaccine-failure-without-antigen-loss, micrometastasis"


def test_the_ledger_names_no_mechanism_that_is_both_persistent_and_over_the_bar():
    clearing = [c for c in MECHANISM_LEDGER["candidates"] if c["clears_the_bar"] is True]
    assert clearing == [], "nothing in the inventory is demonstrated to clear the bar in a dog"
    assert WHAT_WOULD_CHANGE_THE_ANSWER
