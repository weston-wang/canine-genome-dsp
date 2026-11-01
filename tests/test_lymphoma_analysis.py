"""Monte Carlo recomputes for the canine-lymphoma durable-response analysis. Every figure quoted in
the analysis modules and docs/LYMPHOMA_DURABLE_RESPONSE.md is reproduced here from the engine at the
same trials=300, seed=7 it was recorded at. Tolerances are loose enough to absorb platform Monte
Carlo jitter and tight enough that the qualitative claims (thresholds, crossings) are real."""
import numpy as np
import pytest

from canine_dsp import lymphoma_scenarios as ls
from canine_dsp.lymphoma_durable_response_analysis import (
    CHEMO_IS_NOT_DURABILITY, IMMUNOTHERAPY_ACHIEVABILITY,
)
from canine_dsp.lymphoma_gap_closure import (
    DUAL_TARGET, LOWER_THE_BAR, TBI_CONSOLIDATION_IS_NOT_PERSISTENT,
)
from canine_dsp.lymphoma_open_route_closure import (
    CNS_SANCTUARY_CHEMO_ONLY, CNS_SANCTUARY_WITH_IMMUNOTHERAPY,
    MRD_TIMING_IS_NOT_DURABILITY, T_CELL_IS_HARDER,
)
from canine_dsp.mapk_resistance import (
    run_monte_carlo, run_monte_carlo_two_compartment, run_monte_carlo_with_vaccine,
)

TRIALS = 300
P = ls._PREEXISTING_PROB_CENTRAL
S, R = ls.LYMPHOMA_IMMUNOTHERAPY_START_DAY, ls.LYMPHOMA_IMMUNOTHERAPY_RAMP_DAYS


def _chemo(H, ip="B"):
    model, css, seeding, _ = ls.dog_lymphoma_preset(ip)
    o = run_monte_carlo(model, css, H, seeding, TRIALS, preexisting_prob=P, seed=7)
    return 1 - o.progressed.mean()


def _immuno(vmk, H, rab=0.0, ip="B", ib=0.30, escape_mult=1.0):
    scen = ls.lymphoma_immunotherapy_followon_scenarios(rab_max_kill=rab, immunophenotype=ip,
                                                        immunotherapy_max_kill_values=[vmk])
    model, css, seeding, _ = scen[vmk]
    c2 = ls.LYMPHOMA_RAB_ILLUSTRATIVE_CSS_NM if rab > 0 else None
    o = run_monte_carlo_with_vaccine(
        model, css, H, seeding, vaccine_start_day=S, vaccine_ramp_days=R, vaccine_max_kill=vmk,
        immune_escape_seeding_rate=ls.LYMPHOMA_CD20_LOSS_SEEDING_RATE * escape_mult,
        clone_names=ls.LYMPHOMA_IMMUNOTHERAPY_CLONE_NAMES, trials=TRIALS, preexisting_prob=P,
        css_reference_2=c2, initial_burden=ib, seed=7)
    from collections import Counter
    return 1 - o.progressed.mean(), Counter(o.dominant_mechanism).get("cd20_antigen_loss", 0)


# ---------- chemo is not durability ----------

def test_chemo_only_is_low_and_flat_across_horizons():
    two = _chemo(730)
    ten = _chemo(3650)
    assert two == pytest.approx(CHEMO_IS_NOT_DURABILITY["chemo_only_durable_response"]["2yr"], abs=0.06)
    assert ten == pytest.approx(CHEMO_IS_NOT_DURABILITY["chemo_only_durable_response"]["10yr"], abs=0.06)
    assert abs(two - ten) < 0.06  # relapse happens early; extra follow-up does not change the split
    assert two < 0.30             # near-universal relapse, matching the real median PFS of 176 d


# ---------- immunotherapy threshold at the bar ----------

@pytest.mark.parametrize("vmk", [0.06, 0.09])
def test_immunotherapy_threshold_2yr(vmk):
    got, _ = _immuno(vmk, 730)
    assert got == pytest.approx(IMMUNOTHERAPY_ACHIEVABILITY["engine_durable_by_potency_2yr"][vmk],
                                abs=0.06)


def test_immunotherapy_crosses_the_bar_between_0_06_and_0_09():
    below, _ = _immuno(0.06, 730)
    at, _ = _immuno(0.09, 730)
    assert below < 0.35 and at > 0.9   # a genuine threshold at the ~0.090/day bar


def test_immunotherapy_at_the_bar_holds_to_ten_years():
    got, _ = _immuno(0.09, 3650)
    assert got == pytest.approx(IMMUNOTHERAPY_ACHIEVABILITY["engine_durable_by_potency_10yr"][0.09],
                                abs=0.06)
    assert got > 0.9


# ---------- CD20 antigen loss: converted below the bar, starved at it ----------

def test_subthreshold_immunotherapy_converts_relapse_to_antigen_loss():
    _, loss = _immuno(0.03, 3650)
    assert loss > 40   # weak effector turns drug-resistance relapse into CD20-loss relapse


def test_antigen_loss_starves_at_threshold_and_is_robust_to_its_rate():
    durable_1x, loss_1x = _immuno(0.09, 3650, escape_mult=1.0)
    durable_100x, _ = _immuno(0.09, 3650, escape_mult=100.0)
    assert loss_1x <= 5                       # the route starves at threshold potency
    assert durable_100x > 0.9                 # robust even at 100x the assumed antigen-loss rate


# ---------- gap closure: lower the bar ----------

@pytest.mark.parametrize("rab", [0.0, 0.05])
def test_lowering_the_bar_rescues_a_subthreshold_effector(rab):
    got, _ = _immuno(0.06, 3650, rab=rab)
    assert got == pytest.approx(LOWER_THE_BAR[rab]["ten_year_durable"], abs=0.07)


def test_lowering_the_bar_is_monotone():
    values = [LOWER_THE_BAR[a]["ten_year_durable"] for a in sorted(LOWER_THE_BAR)]
    assert values == sorted(values)
    assert values[-1] > values[0] + 0.5


# ---------- gap closure: a one-time consolidation is not persistence ----------

def test_capped_duration_tbi_does_not_buy_ten_year_durability():
    scen = ls.lymphoma_immunotherapy_followon_scenarios(rab_max_kill=0.35,
                                                        immunotherapy_max_kill_values=[0.06])
    model, css, seeding, _ = scen[0.06]
    o = run_monte_carlo_with_vaccine(
        model, css, 3650, seeding, vaccine_start_day=S, vaccine_ramp_days=R, vaccine_max_kill=0.06,
        immune_escape_seeding_rate=ls.LYMPHOMA_CD20_LOSS_SEEDING_RATE,
        clone_names=ls.LYMPHOMA_IMMUNOTHERAPY_CLONE_NAMES, trials=TRIALS, preexisting_prob=P,
        css_reference_2=ls.LYMPHOMA_TBI_ILLUSTRATIVE_CSS_NM,
        css_reference_2_duration_days=ls.LYMPHOMA_TBI_EXPOSURE_DURATION_DAYS, seed=7)
    tbi = 1 - o.progressed.mean()
    baseline = TBI_CONSOLIDATION_IS_NOT_PERSISTENT["on_chop_plus_subthreshold_immunotherapy_10yr"][0.35]
    assert tbi == pytest.approx(baseline, abs=0.07)
    assert tbi < 0.4   # a duration-capped consolidation does not carry durability by itself


# ---------- gap closure: dual target ----------

def test_dual_target_closes_antigen_loss_but_only_matters_at_threshold():
    # below the bar: closing antigen loss does not rescue durability (drug-resistance relapse wins)
    single_06, loss_06 = _immuno(0.06, 3650, escape_mult=1.0)
    tandem_06, tloss_06 = _immuno(0.06, 3650, escape_mult=0.0)
    assert loss_06 > 20 and tloss_06 == 0
    assert tandem_06 < 0.4
    # at the bar: single antigen already starves the route, tandem confirms zero loss
    _, tloss_09 = _immuno(0.09, 3650, escape_mult=0.0)
    assert tloss_09 == 0


# ---------- open route: CNS sanctuary ----------

def test_cns_sanctuary_dominates_relapse_under_chemo_and_is_closed_by_immunotherapy():
    model, css, seeding, _ = ls.dog_lymphoma_preset("B")
    # chemo only, drug largely excluded from the CNS
    chemo = run_monte_carlo_two_compartment(
        model, css, 1825, seeding, nodal_involvement_prob=0.30,
        nodal_seed_fraction=ls.LYMPHOMA_CNS_SEED_FRACTION, trials=TRIALS, preexisting_prob=P,
        sanctuary_penetration_multiplier=0.15, clone_names=ls.LYMPHOMA_CLONE_NAMES, seed=7)
    chemo_nodal = sum(c == "nodal" for c in chemo.dominant_compartment)
    assert chemo_nodal == pytest.approx(CNS_SANCTUARY_CHEMO_ONLY[0.15]["cns_relapses"], abs=20)
    assert chemo_nodal > 50   # the sanctuary is where relapse happens when the drug can't reach it

    # a systemic CD20 effector reaches the sanctuary regardless of drug penetration
    scen = ls.lymphoma_immunotherapy_followon_scenarios(immunotherapy_max_kill_values=[0.09])[0.09]
    m5, c5, s5, _ = scen
    immu = run_monte_carlo_two_compartment(
        m5, c5, 1825, s5, nodal_involvement_prob=0.30,
        nodal_seed_fraction=ls.LYMPHOMA_CNS_SEED_FRACTION, trials=TRIALS, preexisting_prob=P,
        sanctuary_penetration_multiplier=0.15, vaccine_start_day=S, vaccine_ramp_days=R,
        vaccine_max_kill=0.09, immune_escape_seeding_rate=ls.LYMPHOMA_CD20_LOSS_SEEDING_RATE,
        clone_names=ls.LYMPHOMA_IMMUNOTHERAPY_CLONE_NAMES, seed=7)
    immu_durable = 1 - immu.progressed.mean()
    immu_nodal = sum(c == "nodal" for c in immu.dominant_compartment)
    assert immu_durable == pytest.approx(CNS_SANCTUARY_WITH_IMMUNOTHERAPY[0.15]["durable"], abs=0.06)
    assert immu_durable > 0.9 and immu_nodal <= 5


# ---------- open route: MRD timing is not durability ----------

def test_mrd_early_retreatment_is_flat_without_a_bar_clearing_agent():
    high, _ = _immuno(0.06, 3650, ib=0.30)
    low, _ = _immuno(0.06, 3650, ib=0.05)
    assert abs(high - low) < 0.06   # lowering burden alone does not change durability
    assert low == pytest.approx(
        MRD_TIMING_IS_NOT_DURABILITY["durable_by_intervention_burden_immuno_0_06_10yr"][0.05],
        abs=0.06)


# ---------- the T-cell case is harder ----------

def test_t_cell_needs_more_potency_than_b_cell_for_the_same_durability():
    t09, _ = _immuno(0.09, 3650, ip="T")
    t12, _ = _immuno(0.12, 3650, ip="T")
    assert t09 == pytest.approx(T_CELL_IS_HARDER["immunotherapy_sweep_10yr"][0.09], abs=0.08)
    assert t09 < 0.6          # the B-cell-curing 0.09 potency is sub-threshold for T-cell
    assert t12 > 0.9          # only higher potency clears the higher T-cell bar
