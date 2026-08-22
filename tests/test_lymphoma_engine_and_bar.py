"""Fast tests: the two-compartment sanctuary-penetration upgrade, the bar (deterministic), and the
pure-function levers. The heavier Monte Carlo recomputes live in test_lymphoma_analysis.py."""
import numpy as np
import pytest

from canine_dsp import lymphoma_scenarios as ls
from canine_dsp.lymphoma_durable_response_analysis import DURABILITY_BAR_PER_DAY
from canine_dsp.lymphoma_gap_closure import (
    DURABILITY_BAR_PER_DAY as GAP_BAR, LOWER_THE_BAR, bar_after_persistent_kill,
)
from canine_dsp.lymphoma_open_route_closure import (
    TRANSPLANT_TRM, joint_survival, take_weighted_durable,
)
from canine_dsp.mapk_resistance import (
    clone_growth_margins, drug_kill_rate, run_monte_carlo_two_compartment,
)


# ---------- the durability bar (deterministic) ----------

def test_the_bar_is_set_by_pgp_efflux_and_barely_moved_by_chemo():
    model, css, _, _ = ls.dog_lymphoma_preset("B")
    full = clone_growth_margins(model, css)
    no_drug = clone_growth_margins(model, 0.0)
    names = ls.LYMPHOMA_CLONE_NAMES
    # the sensitive clone is driven deeply negative -> deep remission
    assert full[0] < -0.1
    assert full[0] == pytest.approx(DURABILITY_BAR_PER_DAY["sensitive_clone_margin_under_full_chop"],
                                    abs=0.01)
    # the fastest surviving clone under CHOP is the P-gp efflux clone, and it sets the bar
    assert names[1 + int(np.argmax(full[1:]))] == "mdr1_pgp_efflux"
    assert full[1:].max() == pytest.approx(DURABILITY_BAR_PER_DAY["full_chop_5x_ic50"], abs=0.002)
    # chemo moves the resistant bar by only ~2%
    assert no_drug[1:].max() == pytest.approx(DURABILITY_BAR_PER_DAY["no_drug_at_all"], abs=0.002)
    assert abs(no_drug[1:].max() - full[1:].max()) / no_drug[1:].max() < 0.05


def test_the_two_gap_closure_bar_constants_agree():
    model, css, _, _ = ls.dog_lymphoma_preset("B")
    assert GAP_BAR == pytest.approx(clone_growth_margins(model, css)[1:].max(), abs=0.002)


def test_t_cell_bar_is_higher_than_b_cell():
    b, css_b, _, _ = ls.dog_lymphoma_preset("B")
    t, css_t, _, _ = ls.dog_lymphoma_preset("T")
    assert clone_growth_margins(t, css_t)[1:].max() > clone_growth_margins(b, css_b)[1:].max()


# ---------- the sanctuary-penetration engine upgrade ----------

def test_sanctuary_multiplier_validates_range():
    model, css, seeding, _ = ls.dog_lymphoma_preset("B")
    for bad in (-0.1, 1.1):
        with pytest.raises(ValueError):
            run_monte_carlo_two_compartment(model, css, 120, seeding, nodal_involvement_prob=0.3,
                                            nodal_seed_fraction=ls.LYMPHOMA_CNS_SEED_FRACTION,
                                            trials=5, sanctuary_penetration_multiplier=bad)


def test_full_penetration_is_backward_compatible():
    """sanctuary_penetration_multiplier=1.0 must reproduce the default (unset) behaviour exactly."""
    model, css, seeding, _ = ls.dog_lymphoma_preset("B")
    kw = dict(nodal_involvement_prob=0.4, nodal_seed_fraction=ls.LYMPHOMA_CNS_SEED_FRACTION,
              trials=40, preexisting_prob=0.5, seed=11, clone_names=ls.LYMPHOMA_CLONE_NAMES)
    default = run_monte_carlo_two_compartment(model, css, 365, seeding, **kw)
    explicit = run_monte_carlo_two_compartment(model, css, 365, seeding,
                                               sanctuary_penetration_multiplier=1.0, **kw)
    assert np.array_equal(default.progressed, explicit.progressed)
    assert default.dominant_compartment == explicit.dominant_compartment


def test_lower_penetration_makes_the_sanctuary_the_relapse_site():
    """Chemo-only: as CNS drug penetration falls, more relapses come from the sanctuary compartment."""
    model, css, seeding, _ = ls.dog_lymphoma_preset("B")
    kw = dict(nodal_involvement_prob=0.5, nodal_seed_fraction=ls.LYMPHOMA_CNS_SEED_FRACTION,
              trials=120, preexisting_prob=ls._PREEXISTING_PROB_CENTRAL, seed=7,
              clone_names=ls.LYMPHOMA_CLONE_NAMES)
    full = run_monte_carlo_two_compartment(model, css, 730, seeding,
                                           sanctuary_penetration_multiplier=1.0, **kw)
    excluded = run_monte_carlo_two_compartment(model, css, 730, seeding,
                                               sanctuary_penetration_multiplier=0.05, **kw)
    nodal_full = sum(c == "nodal" for c in full.dominant_compartment)
    nodal_excluded = sum(c == "nodal" for c in excluded.dominant_compartment)
    assert nodal_excluded > nodal_full


# ---------- pure-function levers ----------

def test_bar_after_persistent_kill_is_one_for_one():
    for agnostic, row in LOWER_THE_BAR.items():
        assert bar_after_persistent_kill(row["agnostic_kill"]) == pytest.approx(row["bar_after"],
                                                                                abs=0.002)


def test_recorded_agnostic_kill_matches_the_emax_model():
    """The kill rates recorded in LOWER_THE_BAR are the real Emax outputs at the rab css/ic50."""
    for rab, row in zip([0.0, 0.02, 0.03, 0.05], LOWER_THE_BAR.values()):
        kill = drug_kill_rate(ls.LYMPHOMA_RAB_ILLUSTRATIVE_CSS_NM,
                              ls.LYMPHOMA_RAB_ILLUSTRATIVE_IC50_NM, 1.5, rab) if rab else 0.0
        assert float(kill) == pytest.approx(row["agnostic_kill"], abs=0.002)


def test_take_weighted_durable_is_linear_and_bounded():
    assert take_weighted_durable(0.97, 0.18, 1.0) == pytest.approx(0.97)
    assert take_weighted_durable(0.97, 0.18, 0.0) == pytest.approx(0.18)
    assert take_weighted_durable(0.97, 0.18, 0.5) == pytest.approx(0.575, abs=1e-6)
    with pytest.raises(ValueError):
        take_weighted_durable(0.97, 0.18, 1.5)


def test_transplant_trm_competing_hazard_matches_recorded():
    for hazard, recorded in TRANSPLANT_TRM["joint_5yr_by_hazard"].items():
        got = joint_survival(TRANSPLANT_TRM["tumour_control"], hazard, years=5.0)["joint"]
        assert got == pytest.approx(recorded, abs=0.002)
    with pytest.raises(ValueError):
        joint_survival(0.97, 1.5)
