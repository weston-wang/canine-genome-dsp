import numpy as np
import pytest

from canine_dsp.pharmacology import (
    CDK46_CANINE_POTENCY,
    CYTOSTATIC,
    CYTOTOXIC,
    DrugPotency,
    achievability_report,
    cytostatic_ceiling,
    feasibility_frontier,
    max_kill_from_emax,
    required_max_kill,
    saturation_fraction,
    steady_state_css_nM,
)


def test_cytostatic_drug_cannot_declare_emax_above_the_growth_rate():
    """The central constraint, enforced at construction rather than left to the caller: arrest
    drives net growth to zero at best, so a cytostatic Emax above 1.0x growth is incoherent."""
    kwargs = dict(name="x", ic50_nM=100.0, provenance="test")
    DrugPotency(**kwargs, emax_fraction_of_growth=1.0, mechanism_class=CYTOSTATIC)
    with pytest.raises(ValueError, match="cannot exceed the clone's own growth rate"):
        DrugPotency(**kwargs, emax_fraction_of_growth=1.4, mechanism_class=CYTOSTATIC)
    # the same Emax is legitimate once a death mechanism is declared
    DrugPotency(**kwargs, emax_fraction_of_growth=1.4, mechanism_class=CYTOTOXIC)


def test_cytostatic_ceiling_is_the_growth_rate_and_target_potency_exceeds_it():
    """max_kill_2=0.08 -- the value at which the resistance model reports 100% durable response --
    sits above every resistant clone's ceiling, so no dose of a cytostatic drug reaches it."""
    growth = np.array([.06, .05, .055, .058])
    ceiling = cytostatic_ceiling(growth)
    np.testing.assert_allclose(ceiling, growth)
    assert (0.08 > ceiling).all()


def test_saturation_fraction_is_half_at_the_ic50_and_monotone():
    assert saturation_fraction(100.0, 100.0) == pytest.approx(0.5)
    assert saturation_fraction(0.0, 100.0) == 0.0
    rising = [saturation_fraction(c, 100.0) for c in (10, 50, 100, 500, 5000)]
    assert rising == sorted(rising)
    assert rising[-1] > 0.99


def test_max_kill_from_emax_scales_with_growth_rate():
    assert max_kill_from_emax(0.05, 1.0) == pytest.approx(0.05)   # perfect arrest
    assert max_kill_from_emax(0.05, 0.5) == pytest.approx(0.025)  # halves net growth only
    assert max_kill_from_emax(0.05, 2.0) == pytest.approx(0.10)   # cytotoxic


def test_required_max_kill_inflates_below_saturation_and_handles_edges():
    """Being below saturation raises the Emax needed (scales as 1/saturation_fraction), which is why
    a weaker-than-assumed IC50 compounds the ceiling problem instead of trading against it."""
    margin = 0.05
    at_saturation = required_max_kill(margin, 100_000.0, 100.0)
    below = required_max_kill(margin, 100.0, 100.0)          # exactly at IC50 -> half effect
    assert at_saturation == pytest.approx(margin, rel=1e-2)
    assert below == pytest.approx(2 * margin, rel=1e-2)
    assert required_max_kill(-0.01, 500.0, 100.0) == 0.0     # already suppressed
    assert required_max_kill(margin, 0.0, 100.0) == float("inf")


def test_real_canine_ic50_is_far_weaker_than_the_modules_illustrative_value():
    """Guards the finding itself: the illustrative 100 nM is 9-31x more potent than the only real
    canine measurement for the class, so this is not a rounding-level discrepancy."""
    from canine_dsp.mapk_scenarios import CDK46_ILLUSTRATIVE_IC50_NM

    low, high = CDK46_CANINE_POTENCY["ic50_nM_range"]
    assert low / CDK46_ILLUSTRATIVE_IC50_NM > 9
    assert high / CDK46_ILLUSTRATIVE_IC50_NM > 30
    assert CDK46_CANINE_POTENCY["mechanism_class"] == CYTOSTATIC


def test_steady_state_css_conversion_and_unbound_scaling():
    # 1 mg/L of a 447.5 g/mol drug is ~2235 nM; check the unit conversion end to end.
    result = steady_state_css_nM(dose_mg_per_kg=1.0, dosing_interval_h=24.0,
                                 clearance_L_per_h_per_kg=1.0 / 24.0, bioavailability=1.0,
                                 molecular_weight=447.5)
    assert result["css_total_mg_per_L"] == pytest.approx(1.0)
    assert result["css_total_nM"] == pytest.approx(1e6 / 447.5, rel=1e-6)
    assert result["css_free_nM"] == result["css_total_nM"]      # no correction applied by default
    bound = steady_state_css_nM(1.0, 24.0, 1.0 / 24.0, 1.0, 447.5, fraction_unbound=0.1)
    assert bound["css_free_nM"] == pytest.approx(0.1 * result["css_total_nM"])
    with pytest.raises(ValueError):
        steady_state_css_nM(1.0, 24.0, 1.0 / 24.0, 1.5, 447.5)   # bioavailability > 1


def test_achievability_report_flags_mechanism_ceiling_separately_from_potency_shortfall():
    """The two failure modes must stay distinguishable: "not potent enough" is a chemistry problem,
    "above the ceiling for this mechanism" cannot be fixed by any dose or any better molecule of
    the same class."""
    growth = np.array([.06, .05, .055, .058])
    margins = np.array([-0.05, 0.05, 0.036, 0.058])
    potency = DrugPotency(name="perfect arrest", ic50_nM=3090.0, emax_fraction_of_growth=1.0,
                          mechanism_class=CYTOSTATIC, provenance="test")
    report = achievability_report(growth, margins, potency, 500.0,
                                 ["sensitive", "a", "b", "c"])
    assert report["all_clones_reversed"] is False
    assert report["any_blocked_by_mechanism"] is True
    assert report["per_clone"][0]["reversed"] is True          # sensitive clone already suppressed
    for row in report["per_clone"][1:]:
        assert row["blocked_by_cytostatic_ceiling"] is True
        assert row["shortfall"] > 0


def test_achievability_report_rejects_misaligned_inputs():
    with pytest.raises(ValueError, match="must align"):
        achievability_report(np.array([.06, .05]), np.array([.01]),
                             DrugPotency(name="x", ic50_nM=100.0, emax_fraction_of_growth=1.0,
                                        mechanism_class=CYTOSTATIC, provenance="t"),
                             500.0, ["a", "b"])


def test_feasibility_frontier_requirement_falls_with_potency_and_exposure():
    ic50 = np.array([100.0, 1000.0, 3000.0])
    exposure = np.array([100.0, 1000.0, 10000.0])
    grid = feasibility_frontier(0.05, ic50, exposure)
    assert grid.shape == (3, 3)
    for row in grid:                       # more exposure -> lower requirement
        assert row[0] > row[1] > row[2]
    for column in grid.T:                  # weaker IC50 (larger) -> higher requirement
        assert column[0] < column[1] < column[2]
