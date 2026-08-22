import numpy as np
import pytest
from dataclasses import replace

from canine_dsp import hsa_scenarios as hs
from canine_dsp.hsa_antiproliferative import (
    ANSWER_TO_IS_PROPRANOLOL_THE_ONLY_OPTION, BACKTEST_NO_VACCINE, BACKTEST_VERDICT,
    CANINE_ANTIPROLIFERATIVE_TRIALS, GROWTH_REDUCTION_REQUIRED, HUMAN_ANGIOSARCOMA_ANCHOR,
    STACK_TOLERATES_A_DELAYED_START, STACK_WITH_SCHEDULED_AGENT, antiproliferative_schedule,
)
from canine_dsp.hsa_gap_stack import corrected_ic50
from canine_dsp.hsa_vaccine_maintenance import immunity_schedule
from canine_dsp.mapk_resistance import (
    PROGRESSION_THRESHOLD, merge_injections, perturb_resistance_model,
    poisson_mutation_injections, ramping_kill_schedule, sample_initial_state, simulate_resistance,
)

H = 3650
S, R = hs.HSA_VACCINE_START_DAY, hs.HSA_VACCINE_RAMP_DAYS
APPLICABLE = np.array([1.0, 1.0, 1.0, 1.0, 0.0])
ALL_CLONES = np.ones(5)
REAL = 0.03


# ---------- the engine upgrade ----------

def test_growth_modifier_of_ones_is_identical_to_not_passing_one():
    """Backward compatibility: every existing caller is untouched."""
    model, css, _, _ = hs.dog_hsa_preset()
    initial = np.array([0.3, 0.0, 0.0, 0.0])
    concentration = np.full(365, css)
    without = simulate_resistance(model, concentration, initial)
    with_ones = simulate_resistance(model, concentration, initial,
                                    growth_modifier=np.ones(365))
    assert np.allclose(without, with_ones)


def test_growth_modifier_accepts_per_clone_arrays_and_rejects_negatives():
    model, css, _, _ = hs.dog_hsa_preset()
    initial = np.array([0.3, 0.0, 0.0, 0.0])
    per_clone = np.tile(np.array([1.0, 0.5, 1.0, 1.0]), (100, 1))
    result = simulate_resistance(model, np.full(100, css), initial, growth_modifier=per_clone)
    assert result.shape == (101, 4)
    with pytest.raises(ValueError):
        simulate_resistance(model, np.full(100, css), initial,
                            growth_modifier=np.full(100, -0.1))


def test_a_growth_modifier_cannot_make_a_population_shrink_but_a_kill_term_can():
    """The cytostatic ceiling, expressed structurally: arrest is not death."""
    model, _, _, _ = hs.dog_hsa_preset()
    initial = np.array([0.05, 0.0, 0.0, 0.0])
    zero_drug = np.zeros(200)
    arrested = simulate_resistance(model, zero_drug, initial, growth_modifier=np.zeros(200))
    # A kill term has to clear the clone's own growth rate before anything shrinks.
    kill_rate = float(np.max(model.growth)) * 2
    killed = simulate_resistance(model, zero_drug, initial,
                                 additional_kill=np.full((200, 4), kill_rate))
    assert arrested[-1].sum() == pytest.approx(initial.sum(), rel=1e-6), "arrest holds steady"
    assert killed[-1].sum() < initial.sum() * 0.01, "a kill term above growth removes it"


def test_antiproliferative_schedule_ramps_stops_and_spares_masked_clones():
    schedule = antiproliferative_schedule(H, S, 14.0, 0.2, APPLICABLE)
    assert np.allclose(schedule[:S], 1.0), "no effect before the start day"
    assert schedule[-1, 0] == pytest.approx(0.8, abs=0.01), "settles at 1 - suppression"
    assert np.allclose(schedule[:, 4], 1.0), "masked clone is untouched"
    stopped = antiproliferative_schedule(H, S, 14.0, 0.2, ALL_CLONES, stop_day=400)
    assert np.allclose(stopped[500:], 1.0), "returns to baseline after stop_day"
    with pytest.raises(ValueError):
        antiproliferative_schedule(H, S, 14.0, 1.5, ALL_CLONES)
    with pytest.raises(ValueError):
        antiproliferative_schedule(H, S, 0.0, 0.2, ALL_CLONES)


# ---------- the trial record ----------

def test_the_record_contains_more_agents_than_propranolol_and_mostly_negatives():
    agents = [t["agent"] for t in CANINE_ANTIPROLIFERATIVE_TRIALS]
    assert len(agents) >= 5
    assert any("toceranib" in a for a in agents)
    assert any("thalidomide" in a for a in agents)
    assert any("metronomic" in a for a in agents)
    negatives = [t for t in CANINE_ANTIPROLIFERATIVE_TRIALS if t["verdict"].startswith("NEGATIVE")]
    assert len(negatives) >= 2
    assert "26062540" in [t["citation"] for t in CANINE_ANTIPROLIFERATIVE_TRIALS][0]
    assert "No." in ANSWER_TO_IS_PROPRANOLOL_THE_ONLY_OPTION


def test_the_two_negatives_used_doxorubicin_and_the_positives_used_vinblastine():
    assert "DOXORUBICIN" in HUMAN_ANGIOSARCOMA_ANCHOR["partner_specificity"]
    assert "VINBLASTINE" in HUMAN_ANGIOSARCOMA_ANCHOR["partner_specificity"]
    assert "27211551" in HUMAN_ANGIOSARCOMA_ANCHOR["citation"]
    assert HUMAN_ANGIOSARCOMA_ANCHOR["response_rate"] == 1.0


def test_thalidomides_uncontrolled_median_matches_the_negative_toceranib_arm():
    by_agent = {t["agent"].split()[0]: t for t in CANINE_ANTIPROLIFERATIVE_TRIALS}
    assert by_agent["thalidomide"]["median_os_days"] == by_agent["toceranib"]["median_os_days"]
    assert by_agent["thalidomide"]["verdict"].startswith("UNCONTROLLED")


# ---------- the back-test ----------

def _run(vmk, suppression=0.0, corrected=False, start=S, trials=250, seed=7):
    m5, css, seeding, _ = hs.hsa_vaccine_followon_scenarios(vaccine_max_kill_values=[REAL])[REAL]
    if corrected:
        m5 = replace(m5, ic50_nM=corrected_ic50(m5.ic50_nM[0]))
    gm = antiproliferative_schedule(H, start, 14.0, suppression, ALL_CLONES) if suppression else None
    vk = immunity_schedule(H, S, R, vmk, APPLICABLE) if vmk else None
    rng = np.random.default_rng(seed)
    identity = replace(m5, mutation=np.eye(5))
    weights = np.concatenate([np.asarray(seeding, float), [0.0]])
    idx = np.arange(H + 1)
    progressed = np.zeros(trials, dtype=bool)
    for i in range(trials):
        pm = perturb_resistance_model(identity, rng)
        conc = np.full(H, css * rng.lognormal(0, .3))
        init = sample_initial_state(rng, 5, hs._PREEXISTING_PROB_CENTRAL,
                                    mechanism_weights=weights, initial_burden=.3)
        so = np.zeros(5); so[0] = init[0]
        traj = simulate_resistance(pm, conc, so, growth_modifier=gm)[:, 0]
        jit = np.asarray(seeding, float) * rng.lognormal(0, .5, len(seeding))
        drug = poisson_mutation_injections(rng, traj, jit, 1e-8, clone_indices=range(1, 4), k=5)
        prov = simulate_resistance(pm, conc, init, drug, additional_kill=vk, growth_modifier=gm)
        ap = np.where(idx >= S, prov[:, :4].sum(axis=1), 0.0)
        esc = poisson_mutation_injections(
            rng, ap, np.array([hs.HSA_IMMUNE_ESCAPE_SEEDING_RATE * rng.lognormal(0, .5)]),
            1e-8, clone_indices=[4], k=5)
        st = simulate_resistance(pm, conc, init, merge_injections(drug, esc),
                                 additional_kill=vk, growth_modifier=gm)
        tot = st.sum(axis=1)
        nad = int(np.argmin(tot))
        hits = np.flatnonzero(tot[nad:] >= max(PROGRESSION_THRESHOLD * tot[nad], 0.01))
        progressed[i] = hits.size > 0 and hits[0] > 0
    return 1 - progressed.mean()


@pytest.mark.parametrize("suppression", [0.0, 0.163])
def test_backtest_growth_reduction_without_a_vaccine_buys_almost_nothing(suppression):
    """The configuration every real canine trial used -- and they were negative."""
    assert _run(0.0, suppression=suppression) == pytest.approx(
        BACKTEST_NO_VACCINE[suppression], abs=0.07)


def test_the_backtest_spread_is_small_across_the_plausible_range():
    at_play = [BACKTEST_NO_VACCINE[s] for s in (0.0, 0.163, 0.30)]
    assert max(at_play) - min(at_play) < 0.10, "no meaningful benefit without a vaccine"
    assert BACKTEST_NO_VACCINE[0.50] > max(at_play), "only implausibly large suppression helps"


def test_the_verdict_says_what_the_backtest_does_and_does_not_show():
    assert "reproduces the real record" in BACKTEST_VERDICT["consistency"]
    assert "not evidence for the stack" in BACKTEST_VERDICT["consistency"]
    assert "never been given to a dog" in BACKTEST_VERDICT["what_it_does_not_show"]


# ---------- the stack, rebuilt on the scheduled agent ----------

@pytest.mark.parametrize("key,kw", [
    ("vaccine_only", dict(vmk=REAL)),
    ("vaccine_plus_correction", dict(vmk=REAL, corrected=True)),
    ("vaccine_plus_correction_plus_20pct", dict(vmk=REAL, corrected=True, suppression=0.20)),
])
def test_stack_reproduces_through_the_scheduled_agent(key, kw):
    assert _run(**kw) == pytest.approx(STACK_WITH_SCHEDULED_AGENT[key], abs=0.08)


def test_the_scheduled_agent_confirms_neither_half_works_alone():
    assert STACK_WITH_SCHEDULED_AGENT["vaccine_only"] < 0.6
    assert STACK_WITH_SCHEDULED_AGENT["vaccine_plus_correction"] < 0.7
    assert STACK_WITH_SCHEDULED_AGENT["vaccine_plus_20pct_no_correction"] < 0.6
    assert STACK_WITH_SCHEDULED_AGENT["vaccine_plus_correction_plus_20pct"] == pytest.approx(
        1.0, abs=0.02)


def test_the_required_suppression_is_the_one_the_stack_uses():
    required = GROWTH_REDUCTION_REQUIRED["with_cross_resistance_correction"]
    assert required == pytest.approx(0.163, abs=0.005)
    assert STACK_WITH_SCHEDULED_AGENT["vaccine_plus_correction_plus_16pct"] > 0.95


def test_the_agent_does_not_have_to_start_immediately():
    """Practically important: it can be added after the chemotherapy backbone finishes."""
    for start, recorded in STACK_TOLERATES_A_DELAYED_START.items():
        assert recorded == pytest.approx(1.0, abs=0.02)
    assert _run(REAL, suppression=0.20, corrected=True, start=180) == pytest.approx(1.0, abs=0.05)
