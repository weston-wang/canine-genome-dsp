"""Attempts to close the vaccine-potency gap, and why they fail. See docs/HSA_DURABLE_RESPONSE.md."""

import numpy as np

DURABILITY_BAR_PER_DAY = 0.0515
REAL_TRIAL_IMPLIED_MAX_KILL = 0.03

# ---------------------------------------------------------------------------------------------
# Route A -- lower the bar with a persistent mechanism-agnostic agent.
# The arithmetic works. The anchoring does not: see ROUTE_A_ANCHORING_FAILS.
# Vaccine held at 0.03/day; 10-year durable response, 250 trials.
LOWER_THE_BAR = {
    0.0:  {"bar_after": 0.0515, "ten_year_durable": 0.492},
    0.01: {"bar_after": 0.0423, "ten_year_durable": 0.532},
    0.02: {"bar_after": 0.0331, "ten_year_durable": 0.832},
    0.03: {"bar_after": 0.0240, "ten_year_durable": 1.000},
    0.05: {"bar_after": 0.0056, "ten_year_durable": 1.000},
}

# Median time-to-progression by arm, against the real anchors this route needs to match.
# A mechanism-agnostic agent in this model either fails to clear the clone margins (progression in
# tens of days) or clears them (never progresses). No rate produces a 178-day median, so the real
# trial's outcome cannot be expressed as an agnostic kill rate at all.
ROUTE_A_ANCHORING_FAILS = {
    "target": "Lana et al. 2007, PMID 17708397 -- metronomic cyclophosphamide/etoposide/piroxicam, "
              "9 dogs stage II splenic HSA, median disease-free interval 178 d",
    "agnostic_alone_median_ttp_days": {0.02: 10, 0.03: 20, 0.035: 41, 0.04: 72, 0.045: 81,
                                       0.05: None},
    "max_reachable_median_ttp_days": 81,
    "modelled_inhibitor_alone_median_ttp_days": 174,
    "verdict": "The real metronomic result (178 d) matches the modelled INHIBITOR-ALONE arm "
               "(174 d), which moves the bar by 7% and does not clear it. Treating metronomic "
               "chemotherapy as a 0.03/day agnostic kill term is not supported by its own trial.",
    "what_would_change_it": "a metronomic arm with a progression-free readout far beyond 178 d, or "
                            "a measured per-day kill rate in canine HSA cells",
}

# The mechanism metronomic cyclophosphamide does have real canine evidence for is immunological,
# not cytotoxic -- which acts on vaccine HEIGHT, not as a separate kill term. Unquantified.
METRONOMIC_IMMUNE_MECHANISM = {
    "treg_depletion": "Burton et al. 2011, J Vet Intern Med 25(4):920-6, PMID 21736624 -- low-dose "
                      "cyclophosphamide selectively decreases regulatory T cells and inhibits "
                      "angiogenesis in dogs with soft tissue sarcoma (11 dogs, 21 healthy controls)",
    "clinical_signal": "Elmslie et al. 2008, J Vet Intern Med 22(6):1373-9, PMID 18976288 -- "
                       "metronomic cyclophosphamide + piroxicam, 30 dogs with incompletely resected "
                       "soft tissue sarcoma vs 55 matched controls, disease-free interval "
                       "prolonged at P < 0.0001",
    "toxicity": "sterile cystitis in 12/30 (40%); every-other-day dosing tolerated better than daily",
    "why_it_is_not_route_A": "Treg depletion raises the height of the vaccine already present "
                             "rather than supplying an independent kill term. Neither trial is in "
                             "hemangiosarcoma, and no per-day kill rate follows from either.",
}

# ---------------------------------------------------------------------------------------------
# Route B -- two vaccines with independent antigens. Fails under documented antigenic competition.
DUAL_VACCINE = {
    0.03:   {"label": "one vaccine", "ten_year_durable": 0.492},
    0.0303: {"label": "weaker arm suppressed 100x", "ten_year_durable": 0.516},
    0.033:  {"label": "weaker arm suppressed 10x", "ten_year_durable": 0.500},
    0.045:  {"label": "weaker arm suppressed 2x", "ten_year_durable": 0.540},
    0.06:   {"label": "perfect additivity", "ten_year_durable": 1.000},
}

# Fraction of the weaker arm's response that may be lost before the pair stops clearing the bar.
DUAL_VACCINE_TOLERANCE = 0.28

ANTIGENIC_COMPETITION = {
    "citation": "Woodruff et al. 2018, Cell Rep 25(2):321-327.e3, PMID 30304673 -- 'B Cell "
                "Competition for Restricted T Cell Help Suppresses Rare-Epitope Responses'",
    "suppression_at_2x_excess": 10,
    "suppression_at_10x_excess": 100,
    "resistant_to_boosting_and_adjuvants": True,
    "stable_over_antigen_dose_range_logs": 6,
    "why_it_hits_this_pair": "eVim is an antibody (B-cell) vaccine, which is exactly the arm this "
                             "competition suppresses; immunodominance is described in the source as "
                             "an obstacle to polyvalent responses through vaccination.",
    "verdict": "The pair tolerates a 28% loss in the weaker arm. The WEAKEST suppression Woodruff "
               "reports is 10-fold, a 90% loss. Route B fails under any documented level of "
               "competition, and the competition cannot be dosed or adjuvanted around.",
    "not_a_toxicity_problem": "Both trials individually reported no vaccine-related toxicity "
                              "(PMID 37686485, PMID 41009669). The failure is interference, "
                              "not safety.",
}

# ---------------------------------------------------------------------------------------------
# Route C -- booster-interval tolerance. NOT a way to close the gap: it is a consequence of having
# already closed it. tolerable_booster_interval returns 0.0 for any potency at or below the bar.
BOOSTER_INTERVAL_BY_HEADROOM = {
    0.06: {"may_decay_to": 0.858, 90: 20.0, 180: 40.0, 365: 80.0},
    0.08: {"may_decay_to": 0.644, 90: 57.0, 180: 114.0, 365: 232.0},
    0.10: {"may_decay_to": 0.515, 90: 86.0, 180: 172.0, 365: 349.0},
}


def tolerable_booster_interval(max_kill: float, bar: float, half_life_days: float) -> float:
    """Longest interval keeping immunity above `bar` at all times.

    Returns 0.0 when `max_kill` does not clear the bar, which is the whole point: interval
    tolerance is downstream of clearing the bar, not an alternative route to it.
    """
    if half_life_days <= 0:
        raise ValueError("half_life_days must be positive")
    if max_kill <= bar:
        return 0.0
    return float(-half_life_days * np.log(bar / max_kill) / np.log(2))


GAP_STATUS = {
    "open": True,
    "shortfall": "real HSA vaccination implies ~0.03/day against a bar of ~0.0515/day",
    "route_A": "NOT SUPPORTED -- the agent's own trial anchors it to the inhibitor-alone arm",
    "route_B": "NOT SUPPORTED -- fails under documented antigenic competition",
    "route_C": "NOT A ROUTE -- booster tolerance presupposes clearing the bar",
    "best_remaining_lead": "raise vaccine HEIGHT by removing immunosuppression -- metronomic "
                           "cyclophosphamide (Treg depletion, real canine evidence) or anti-PD-L1 "
                           "(PD-L1+ macrophages exclude T-cells in canine HSA, PMID 35136176). "
                           "Neither has a measured effect on kill rate, so neither is quantified "
                           "here and neither should be reported as a closure.",
}
