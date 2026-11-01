import numpy as np
import pytest

from canine_dsp import hsa_scenarios as hs
from canine_dsp.hsa_vaccine_maintenance import (
    BOOSTERS_DO_NOT_SUBSTITUTE_FOR_POTENCY, BOOSTER_REQUIREMENT_AT_THRESHOLD,
    DURABILITY_BAR_PER_DAY, EVIM_MAINTENANCE_INTERVAL_DAYS, REAL_TRIAL_IMPLIED_MAX_KILL,
    STOPPING_BOOSTERS_AT_THRESHOLD, immunity_schedule, required_booster_interval,
    run_with_schedule,
)
from canine_dsp.mapk_resistance import ramping_kill_schedule

HORIZON = 3650
START, RAMP = hs.HSA_VACCINE_START_DAY, hs.HSA_VACCINE_RAMP_DAYS
APPLICABLE = np.array([1.0, 1.0, 1.0, 1.0, 0.0])


def _durable(max_kill, half_life=None, interval=None, n_boosters=None, trials=250):
    model, css, seeding, _ = hs.hsa_vaccine_followon_scenarios(
        vaccine_max_kill_values=[max_kill])[max_kill]
    schedule = immunity_schedule(HORIZON, START, RAMP, max_kill, APPLICABLE,
                                 half_life_days=half_life, booster_interval_days=interval,
                                 n_boosters=n_boosters)
    progressed = run_with_schedule(
        model, css, HORIZON, seeding, schedule, START,
        hs.HSA_IMMUNE_ESCAPE_SEEDING_RATE, trials=trials,
        preexisting_prob=hs._PREEXISTING_PROB_CENTRAL, seed=7)
    return 1 - progressed.mean()


def test_no_waning_single_dose_reproduces_the_engine_schedule_exactly():
    """The backward-compatibility anchor: without decay this is the engine's own ramp."""
    mine = immunity_schedule(HORIZON, START, RAMP, 0.06, APPLICABLE)
    theirs = ramping_kill_schedule(HORIZON, START, RAMP, 0.06, APPLICABLE)
    assert np.allclose(mine, theirs)


def test_schedule_never_exceeds_max_kill_and_spares_the_escape_clone():
    schedule = immunity_schedule(HORIZON, START, RAMP, 0.06, APPLICABLE,
                                 half_life_days=180, booster_interval_days=60)
    assert schedule.max() <= 0.06 + 1e-12
    assert schedule[:, 4].max() == 0.0
    assert schedule[:START].max() == 0.0


def test_boosting_restores_height_that_waning_removes():
    unboosted = immunity_schedule(HORIZON, START, RAMP, 0.06, APPLICABLE, half_life_days=180)
    boosted = immunity_schedule(HORIZON, START, RAMP, 0.06, APPLICABLE, half_life_days=180,
                                booster_interval_days=60)
    late = slice(HORIZON - 365, HORIZON)
    assert unboosted[late, 0].mean() < 0.005, "unboosted immunity should be near-gone by year 10"
    assert boosted[late, 0].mean() > 0.05, "boosting should hold it near max"


def test_schedule_rejects_invalid_parameters():
    with pytest.raises(ValueError):
        immunity_schedule(HORIZON, START, 0.0, 0.06, APPLICABLE)
    with pytest.raises(ValueError):
        immunity_schedule(HORIZON, START, RAMP, 0.06, APPLICABLE, half_life_days=-1)


@pytest.mark.parametrize("max_kill", [0.03, 0.06])
def test_boosters_do_not_substitute_for_potency(max_kill):
    """The load-bearing result: below the bar, boosting forever changes nothing."""
    recorded = BOOSTERS_DO_NOT_SUBSTITUTE_FOR_POTENCY[max_kill]
    never = _durable(max_kill)
    boosted = _durable(max_kill, half_life=180, interval=60)
    assert never == pytest.approx(recorded["never_wanes"], abs=0.06)
    assert boosted == pytest.approx(recorded["wanes_180d_boosted_q60d"], abs=0.06)
    assert abs(never - boosted) < 0.06, "boosting must not move a schedule already at its ceiling"


def test_the_real_trial_implied_potency_sits_below_the_bar_and_boosting_cannot_lift_it():
    assert REAL_TRIAL_IMPLIED_MAX_KILL < DURABILITY_BAR_PER_DAY
    sub = BOOSTERS_DO_NOT_SUBSTITUTE_FOR_POTENCY[REAL_TRIAL_IMPLIED_MAX_KILL]
    assert sub["never_wanes"] == pytest.approx(sub["wanes_180d_boosted_q60d"], abs=0.02)
    assert sub["never_wanes"] < 0.6, "sub-threshold potency is not durability at any schedule"


def test_at_threshold_potency_waning_without_boosters_collapses_ten_year_durability():
    """The engine's no-waning default is carrying the headline 1.000."""
    unboosted = _durable(0.06, half_life=180)
    boosted = _durable(0.06, half_life=180, interval=60)
    assert unboosted == pytest.approx(BOOSTER_REQUIREMENT_AT_THRESHOLD[180]["no_boosters"],
                                      abs=0.08)
    assert boosted == pytest.approx(1.0, abs=0.03)
    assert boosted - unboosted > 0.5


def test_shorter_immunity_needs_a_shorter_booster_interval():
    fast = BOOSTER_REQUIREMENT_AT_THRESHOLD[90]
    slow = BOOSTER_REQUIREMENT_AT_THRESHOLD[365]
    assert fast["q180d"] < slow["q180d"], "q180d is not enough when immunity halves in 90 days"
    assert fast["q60d"] == slow["q60d"] == 1.000


def test_stopping_maintenance_forfeits_durability():
    assert STOPPING_BOOSTERS_AT_THRESHOLD[None] == 1.000
    for years in (1, 2, 5):
        assert STOPPING_BOOSTERS_AT_THRESHOLD[years] < 0.6
    values = [STOPPING_BOOSTERS_AT_THRESHOLD[y] for y in (1, 2, 5)]
    assert values == sorted(values), "stopping later should not be worse than stopping earlier"


def test_stopping_after_two_years_is_recomputed_not_just_recorded():
    stopped = _durable(0.06, half_life=180, interval=60, n_boosters=int(2 * 365 / 60))
    assert stopped == pytest.approx(STOPPING_BOOSTERS_AT_THRESHOLD[2], abs=0.10)
    assert stopped < 0.7


def test_required_booster_interval_scales_with_half_life():
    assert required_booster_interval(180) == pytest.approx(57.9, abs=0.5)
    assert required_booster_interval(90) == pytest.approx(29.0, abs=0.5)
    assert required_booster_interval(360) > required_booster_interval(180)
    with pytest.raises(ValueError):
        required_booster_interval(180, retained_fraction=1.0)
    with pytest.raises(ValueError):
        required_booster_interval(0)


def test_evim_real_interval_lands_right_at_the_threshold_not_clear_of_it():
    """eVim boosts every two months. Against a 180-day half-life that holds 79.4% of peak -- just
    under an 80% retention target, so the real schedule sits at the threshold rather than above it.
    Recorded because an earlier draft claimed it cleared the bar comfortably."""
    needed = required_booster_interval(180, retained_fraction=0.8)
    assert needed == pytest.approx(57.9, abs=0.5)
    assert EVIM_MAINTENANCE_INTERVAL_DAYS > needed, "60 d is marginally longer than 57.9 d"
    retained = 0.5 ** (EVIM_MAINTENANCE_INTERVAL_DAYS / 180)
    assert retained == pytest.approx(0.794, abs=0.005)
    # A 90-day half-life would leave the same schedule far short.
    assert 0.5 ** (EVIM_MAINTENANCE_INTERVAL_DAYS / 90) < 0.65
