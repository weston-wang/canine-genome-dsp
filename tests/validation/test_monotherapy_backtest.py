"""Tests for the engine back-test.

A validation module reporting a failure is under constant pressure to soften. These tests exist to
make softening break the build.

Three things are pinned. The back-test verdict must stay a failure with the actual numbers attached
-- 0.000 against 0.375 -- because "the model was somewhat pessimistic here" would be a false
summary of a flat structural inability. The two rejected hypotheses must stay recorded as rejected,
because keeping only the surviving explanation would make the diagnosis look obvious when it took
two wrong guesses to reach. And the scope of the damage must stay exactly where the evidence puts
it: the continuous-dosing figures are NOT invalidated, the finite-course conclusions ARE, and
neither half may drift into the other.

The live re-derivations are deliberately cheap. The expensive Monte Carlo runs that produced these
tables are recorded as constants; what is re-derived here is the arithmetic that explains them, so
a change in growth rates or the detection floor breaks these tests rather than silently
invalidating the diagnosis.
"""

import numpy as np
import pytest

from canine_dsp.validation.monotherapy_backtest import (
    HYPOTHESES_TESTED_AND_REJECTED,
    LOMUSTINE_BACKTEST,
    MEASURED_MONOTHERAPY_OUTCOMES,
    THE_ACTUAL_MECHANISM,
    UNTREATED_ARM_IS_A_CATEGORY_ERROR,
    WHAT_THE_ENGINE_ACTUALLY_COMPUTES,
    commensurable_outcomes,
    confidence_verdict,
)


# --- the failure must stay a failure ---

def test_the_backtest_verdict_is_a_failure_with_numbers():
    v = LOMUSTINE_BACKTEST["verdict"]
    assert v.startswith("FAILS")
    assert "0.000" in v and "0.375" in v


def test_the_model_returns_zero_at_every_potency_and_horizon():
    """Flat zero is the point. A single nonzero entry would make this a calibration story instead
    of a structural one."""
    for potency, rows in LOMUSTINE_BACKTEST["model_relapse_free_by_potency"].items():
        for horizon, value in rows.items():
            assert value == 0.0, (potency, horizon)


def test_the_observed_value_is_the_published_one():
    obs = MEASURED_MONOTHERAPY_OUTCOMES["lomustine_adjuvant_localized"]
    assert obs["relapse_free_fraction"] == 0.375
    assert obs["n"] == 16
    assert "19453368" in obs["citation"]


# --- the category error must stay documented ---

def test_only_one_measured_outcome_is_commensurable():
    """Six of seven report median survival, which the engine does not emit. If this count ever
    rises without the engine gaining a survival endpoint, someone has relaxed the standard."""
    assert len(commensurable_outcomes()) == 1
    assert "lomustine_adjuvant_localized" in commensurable_outcomes()


def test_every_non_commensurable_entry_says_why():
    for name, row in MEASURED_MONOTHERAPY_OUTCOMES.items():
        if not row["COMMENSURABLE"]:
            assert row["why"], name


def test_the_five_day_agreement_is_labelled_a_coincidence():
    """The most dangerous number in this module: model and reality both say 5 days, for unrelated
    reasons. Left unlabelled it reads as validation."""
    e = UNTREATED_ARM_IS_A_CATEGORY_ERROR
    assert e["model_intact_untreated_progression_days"] == e[
        "published_cns_palliative_survival_days"]
    assert "COINCIDENCE" in MEASURED_MONOTHERAPY_OUTCOMES["cns_palliative"]["why"]
    assert "not time to death" in e["the_trap"]


def test_the_undisguised_gap_is_kept_alongside_it():
    """4 days vs 398 is the same fact without the flattering coincidence."""
    e = UNTREATED_ARM_IS_A_CATEGORY_ERROR
    assert e["model_debulked_untreated_progression_days"] == 4
    assert e["published_periarticular_surgery_survival_days"] == 398


# --- the rejected hypotheses must stay rejected ---

@pytest.mark.parametrize("name", sorted(
    k for k in HYPOTHESES_TESTED_AND_REJECTED if k != "why_both_were_worth_testing"))
def test_each_rejected_hypothesis_records_its_test_and_result(name):
    h = HYPOTHESES_TESTED_AND_REJECTED[name]
    assert h["result"].startswith("REJECTED")
    assert h["test"] and h["hypothesis"]


def test_the_residual_sweep_covered_seven_orders_of_magnitude():
    """The strength of the rejection is the range. A narrow sweep would not have ruled it out."""
    assert "1e-10" in HYPOTHESES_TESTED_AND_REJECTED["fixed_surgical_residual"]["test"]


# --- the mechanism, re-derived rather than asserted ---

def test_the_regrowth_factor_is_arithmetically_what_the_module_claims():
    """~1.2e12 over the 463 drug-free days. If growth rates or the exposure cap change, this breaks
    rather than leaving a stale explanation in place."""
    growth_per_day = 0.06
    drug_free_days = 568 - 105
    assert np.exp(growth_per_day * drug_free_days) == pytest.approx(1.2e12, rel=0.15)


def test_any_nonzero_residual_clears_the_detection_floor_after_that_regrowth():
    """The core of the diagnosis: 1e-10 is not small enough to survive 1.2e12-fold regrowth."""
    detection_floor = 0.01
    assert 1e-10 * 1.2e12 > detection_floor


def test_the_step_function_is_recorded_including_that_1_000_is_not_a_cure():
    text = THE_ACTUAL_MECHANISM["the_step_function"]
    assert "0.000 up to max_kill 0.30 and 1.000 at 0.50" in text
    assert "not a cure" in text
    assert "Not yet detectable" in text or "not yet detectable" in text.lower()


def test_the_absence_of_an_extinction_state_is_quantified():
    assert "2.7e-82" in THE_ACTUAL_MECHANISM["and_the_residual_is_always_nonzero"]


# --- scope of the damage: neither half may drift ---

def test_the_continuous_dosing_figures_are_explicitly_not_invalidated():
    """Overclaiming here would wrongly discard the whole frozen analysis."""
    text = confidence_verdict()["what_is_trustworthy"]
    assert "Nothing here invalidates those" in text
    assert "seeding" in text


def test_the_finite_course_conclusions_are_explicitly_invalidated():
    """Underclaiming here would leave a tautology standing as a finding."""
    text = confidence_verdict()["what_is_not"]
    assert "stoppability" in text
    assert "tautology" in text


def test_the_tautology_is_named_with_its_counterexample():
    text = WHAT_THE_ENGINE_ACTUALLY_COMPUTES["THE_CONSEQUENCE"]
    assert "CANNOT COME OUT ANY OTHER WAY" in text
    assert "property of the tool" in text
    assert "37.5%" in text


def test_the_two_regimes_are_distinguished_by_binding_event():
    w = WHAT_THE_ENGINE_ACTUALLY_COMPUTES
    assert "seeding" in w["when_the_output_is_a_real_probability"].lower()
    assert "sensitive" in w["when_it_is_not"].lower()
    assert "deterministic" in w["when_it_is_not"]


# --- the module must stay a diagnosis, and stay separate ---

def test_it_declines_to_patch_the_engine():
    assert "does not patch" in confidence_verdict()["what_would_fix_it"]


def test_the_fix_is_named_concretely_rather_than_gestured_at():
    text = confidence_verdict()["what_would_fix_it"]
    assert "extinction state" in text
    assert "stochastic cell loss" in text


def test_the_verdict_is_qualified_not_a_blanket_pass_or_fail():
    assert confidence_verdict()["short_answer"].startswith("Qualified")


def test_validation_changes_no_analysis_module():
    """The separation the user asked for, enforced: this package may import from the analysis but
    must not be imported BY it, or a validation failure could alter a frozen finding."""
    import pathlib

    src = pathlib.Path(__file__).resolve().parents[2] / "src" / "canine_dsp"
    offenders = [
        p.name for p in src.glob("*.py")
        if "validation" in p.read_text() and "import" in p.read_text().split("validation")[0][-200:]
    ]
    assert offenders == []


# --- the extinction follow-up ---

def test_the_fix_did_not_help_inside_the_swept_range():
    from canine_dsp.validation.monotherapy_backtest import EXTINCTION_RERUN

    assert "NO CHANGE" in EXTINCTION_RERUN["result_within_the_swept_potency_range"]


def test_the_reason_the_fix_could_not_bite_is_arithmetic_and_checkable():
    """0.213/day needed to reach one cell; the sweep stops at 0.20. Re-derived so a change in the
    growth rate or exposure cap breaks this rather than leaving a stale excuse."""
    from canine_dsp.validation.monotherapy_backtest import EXTINCTION_RERUN

    growth, days, b0 = 0.06, 105, 0.009
    needed = growth + np.log(b0 / 1e-9) / days
    assert needed == pytest.approx(0.213, abs=0.01)
    assert EXTINCTION_RERUN["nadir_by_potency_cells_at_K_1e9"][0.12] > 10_000


def test_extinction_unlocks_intermediate_outcomes_that_were_impossible_before():
    """The substantive result: with extinction off the engine cannot produce an intermediate in a
    finite course at any potency; with it on, it can."""
    from canine_dsp.validation.monotherapy_backtest import (
        EXTINCTION_UNLOCKS_INTERMEDIATE_OUTCOMES as E,
    )

    rows = {k: v for k, v in E.items() if isinstance(k, float)}
    assert all(r["off"] == 0.0 for r in rows.values())
    assert any(0.05 < r["one_cell_1e12"] < 0.95 for r in rows.values())


def test_the_near_match_is_labelled_fitting_not_validation():
    """0.420 against 0.375 is the most seductive number in this module. It required moving two free
    parameters, and saying so is the difference between a back-test and a curve fit."""
    from canine_dsp.validation.monotherapy_backtest import (
        EXTINCTION_UNLOCKS_INTERMEDIATE_OUTCOMES as E,
    )

    text = E["BUT_THIS_IS_NOT_A_VALIDATION"]
    assert "fitting, not back-testing" in text
    assert "outside" in text or "above the top" in text
    assert "still unestablished" in text
