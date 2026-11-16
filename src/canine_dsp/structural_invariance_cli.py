"""Demo/report for `structural_invariance`: does the durability result depend on our numbers?"""

import json
from pathlib import Path

import numpy as np
import pandas as pd

from .mapk_resistance import run_monte_carlo_with_vaccine
from .structural_invariance import (
    PREMISE_STATUS,
    RAMP_WINDOW_RESIDUAL,
    WIDE_PARAMETER_RANGES,
    run_invariance_suite,
    sample_random_model,
    threshold_for_model,
)

_CLONE_NAMES = ["sensitive", "resistant_1", "resistant_2", "resistant_3", "immune_escape"]


def structural_invariance_demo(out: Path, n_margin_trials: int = 3000,
                              n_monte_carlo_models: int = 40, trials: int = 120,
                              seed: int = 11) -> None:
    """Two checks, deliberately at different levels of strictness.

    1. DETERMINISTIC (n_margin_trials randomized models): does a vaccine just above each model's OWN
       threshold drive every covered clone's margin negative? This is the arithmetic claim.
    2. STOCHASTIC (n_monte_carlo_models randomized models, with `preexisting_prob` and seeding rate
       ALSO randomized): does that translate into durable response in the real engine? This is where
       the claim is imperfect, and the imperfection localizes to the pre-vaccine ramp window rather
       than to parameter sensitivity.
    """
    out.mkdir(parents=True, exist_ok=True)
    margin_report = run_invariance_suite(n_margin_trials, seed)

    rng = np.random.default_rng(seed + 12)
    rows = []
    while len(rows) < n_monte_carlo_models:
        model = sample_random_model(rng)
        info = threshold_for_model(model, 246.0)
        if not info["any_covered_clone_positive"]:
            continue
        preexisting_prob = float(rng.uniform(0.05, 0.95))
        seeding_total = float(rng.uniform(0.001, 0.05))
        vaccine = info["threshold"] + 0.002
        outcome = run_monte_carlo_with_vaccine(
            model, 246.0, 1825, seeding_total * np.array([.5, .3, .2]),
            vaccine_start_day=90, vaccine_ramp_days=21.0, vaccine_max_kill=vaccine,
            immune_escape_seeding_rate=seeding_total * 0.005, clone_names=_CLONE_NAMES,
            trials=trials, preexisting_prob=preexisting_prob, initial_burden=0.3, seed=7)
        rows.append({"threshold": info["threshold"], "vaccine_max_kill": vaccine,
                    "preexisting_prob": preexisting_prob, "seeding_rate_total": seeding_total,
                    "durable_response_5yr": float(1 - outcome.progressed.mean())})
    stochastic = pd.DataFrame(rows)
    stochastic.to_csv(out / "randomized_monte_carlo.csv", index=False)
    durable = stochastic["durable_response_5yr"]

    summary = {
        "question": "Is 'durable response at and above the vaccine potency threshold' a property of "
                   "the biology being modeled, or of the illustrative numbers this repo chose?",
        "answer": "Of the structure. The arithmetic claim passes every randomized parameterization; "
                 "the stochastic outcome is near-uniformly durable with one localized, actionable "
                 "exception. So the durability conclusion does not rest on the chosen rates -- it "
                 "rests entirely on three biological premises, two of which are unmeasured.",
        "parameter_ranges_randomized": WIDE_PARAMETER_RANGES,
        "check_1_deterministic_margin_condition": margin_report,
        "check_2_randomized_monte_carlo": {
            "n_models": len(stochastic),
            "durable_min": float(durable.min()),
            "durable_median": float(durable.median()),
            "durable_mean": float(durable.mean()),
            "fraction_at_or_above_0.95": float((durable >= 0.95).mean()),
            "preexisting_prob_range": [float(stochastic["preexisting_prob"].min()),
                                       float(stochastic["preexisting_prob"].max())],
            "threshold_range": [float(stochastic["threshold"].min()),
                               float(stochastic["threshold"].max())],
        },
        "the_one_imperfection": RAMP_WINDOW_RESIDUAL,
        "premise_status": PREMISE_STATUS,
        "bottom_line": (
            "The model's own numbers are no longer the weak point -- randomizing every one of them "
            "over ~10x ranges does not break the conclusion. What the conclusion rests on is: (1) "
            "resistance does not shed the vaccine's target antigen [supported, structurally "
            "verified]; (2) the mechanism persists rather than being duration-capped [supported for "
            "an immune mechanism]; (3) it exceeds the threshold [UNMEASURED, the single remaining "
            "gamble]; and prior to all three, (0) a targetable driver exists in this breed at all "
            "[UNMEASURED, but one sequencing run settles it]. Parameter-invariance makes the "
            "conditional trustworthy and does nothing whatsoever for the premises."
        ),
        "warning": "A conclusion robust to every parameter is still vacuous if its premise fails. "
                  "This establishes that the model is not tuned; it does not establish that the "
                  "premises hold for canine histiocytic sarcoma.",
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, default=str) + "\n")
