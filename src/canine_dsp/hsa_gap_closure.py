"""Closing the vaccine-potency gap and the booster-interval gap. See docs/HSA_DURABLE_RESPONSE.md."""

import numpy as np

DURABILITY_BAR_PER_DAY = 0.0515
REAL_TRIAL_IMPLIED_MAX_KILL = 0.03

# Route A: lower the bar with a persistent mechanism-agnostic agent rather than raising the vaccine.
# Vaccine held at the real achievable 0.03/day; 10-year durable response, 250 trials.
LOWER_THE_BAR = {
    0.0:  {"bar_after": 0.0515, "ten_year_durable": 0.492},
    0.01: {"bar_after": 0.0423, "ten_year_durable": 0.532},
    0.02: {"bar_after": 0.0331, "ten_year_durable": 0.832},
    0.03: {"bar_after": 0.0240, "ten_year_durable": 1.000},
    0.05: {"bar_after": 0.0056, "ten_year_durable": 1.000},
}

# The agent must be persistent. eBAT has the coverage and not the duration, and re-dosing it failed
# in a real trial (Borgatti et al. 2020, PMID 32187827). Metronomic oral chemotherapy has the right
# shape: continuously dosed, oral, systemic (Lana et al. 2007, PMID 17708397).
PERSISTENT_AGNOSTIC_CANDIDATE = {
    "therapy": "metronomic oral chemotherapy (cyclophosphamide/etoposide/piroxicam)",
    "citation": "Lana et al. 2007, J Vet Intern Med 21(4):764-9, PMID 17708397",
    "evidence": "nine dogs, stage II splenic HSA: median overall survival and median disease-free "
                "interval both 178 d, against 133 d and 126 d for 24 dogs on doxorubicin",
    "rejected_alternative": "eBAT -- 28-day window, and three cycles gave more toxicity and less "
                            "efficacy than one (Borgatti et al. 2020, PMID 32187827)",
    "limits": "nine dogs, non-randomised, retrospective comparator; the kill rate it supplies is "
              "not measured and is swept here, not asserted",
}

# Route B: two vaccines with independent antigens and independent effector arms.
DUAL_VACCINE = {
    0.03:  {"label": "one vaccine", "ten_year_durable": 0.492},
    0.045: {"label": "two, 25% loss", "ten_year_durable": 0.540},
    0.05:  {"label": "two, sub-additive", "ten_year_durable": 0.924},
    0.06:  {"label": "two, additive", "ten_year_durable": 1.000},
}

DUAL_VACCINE_RATIONALE = {
    "vaccine_a": "ERstrePs -- ER-stress peptides; humoral AND T-cell response (PMID 37686485)",
    "vaccine_b": "eVim -- extracellular vimentin; antibody-mediated (PMID 41009669)",
    "independence": "different antigens presented through different effector arms, so neither "
                    "competes for the other's target and MHC-I loss cannot disable both",
    "caveat": "additivity is assumed, not measured. At 25% loss of additivity the combination "
              "falls back to 0.540, so this is a threshold and not a gradient.",
}


def tolerable_booster_interval(max_kill: float, bar: float, half_life_days: float) -> float:
    """Longest interval that keeps immunity above `bar` at all times.

    Immunity only has to stay above the bar, not near its peak, so headroom above the bar buys
    interval tolerance directly. Returns 0.0 when `max_kill` does not clear the bar at all.
    """
    if half_life_days <= 0:
        raise ValueError("half_life_days must be positive")
    if max_kill <= bar:
        return 0.0
    return float(-half_life_days * np.log(bar / max_kill) / np.log(2))


# tolerable_booster_interval at DURABILITY_BAR_PER_DAY, by potency and immunity half-life (days).
# The analytic criterion is conservative: it requires immunity above the bar for the whole horizon,
# while the simulation tolerates longer intervals because the tumour is already near-extinct by the
# time immunity first dips. Both are recorded; the analytic one is the safe schedule.
BOOSTER_INTERVAL_BY_HEADROOM = {
    0.06: {"may_decay_to": 0.858, 90: 20.0, 180: 40.0, 365: 80.0},
    0.08: {"may_decay_to": 0.644, 90: 57.0, 180: 114.0, 365: 232.0},
    0.10: {"may_decay_to": 0.515, 90: 86.0, 180: 172.0, 365: 349.0},
}

# 10-year durable response, real vaccine potency plus a persistent agnostic agent at 0.03/day,
# across the immunity half-life nobody has measured and two booster schedules.
COMBINED_IS_HALF_LIFE_INSENSITIVE = {
    (90, 60): 1.000, (90, 90): 1.000, (180, 60): 1.000, (180, 90): 1.000,
}
