"""Antigen convergence: why a vaccine catches every drug-resistance route, and why that was missed.
WHY THIS MODULE EXISTS ---------------------- This project derived a specific structural argument
early on and then dropped it from three consecutive analyses. The argument, stated in
`run_monte_carlo_with_vaccine`'s own docstring and at length in the README: None of the three
modeled drug-resistance escape mechanisms requires losing the driver-mutation antigen a vaccine
would target. See docs/HS_MAPK_RESISTANCE.md.
"""

import numpy as np

# Which modeled resistance mechanisms retain the vaccine's target antigen, and why. This is the
# content of the convergence argument, written as data so `verify_antigen_convergence` can check the
# engine actually behaves this way instead of the claim living only in a docstring.
ANTIGEN_RETENTION = {
    "sensitive": {
        "retains_driver_antigen": True,
        "reason": "expresses the original driver hotspot; no resistance lesion at all",
    },
    "pathway_reactivation": {
        "retains_driver_antigen": True,
        "reason": "adds a secondary RAS/RAF hit ON TOP of the original mutation -- the hotspot "
                 "peptide is still expressed, so an anti-hotspot response still sees this clone",
    },
    "rtk_bypass": {
        "retains_driver_antigen": True,
        "reason": "reactivates parallel survival signaling AROUND the inhibited node; nothing about "
                 "bypassing a pathway requires shedding the driver mutation",
    },
    "target_site_mutation": {
        "retains_driver_antigen": True,
        "reason": "alters the MEK-inhibitor binding site only -- a change to the drug target, not to "
                 "the antigen the vaccine is directed against",
    },
    "immune_escape": {
        "retains_driver_antigen": False,
        "reason": "the one route that does evade the vaccine, by definition: an antigen-loss / "
                  "MHC-I-downregulation event.",
    },
}

CONVERGENCE_ARGUMENT = {
    "claim": "Every drug-resistance route in this model retains the driver-mutation antigen, so a "
            "vaccine against that hotspot is escape-route-agnostic -- it covers all three routes by "
            "construction rather than by being potent enough to out-kill each one separately.",
    "distinct_from": "The pharmacological convergence argument (all three routes share a "
                     "downstream CDK4/6 dependency, so one drug at that node closes them "
                     "simultaneously).",
    "why_it_matters_for_endurance": "The two constraints that defeated both small-molecule "
                                    "second agents -- the cytostatic ceiling and the "
                                    "cumulative-dose duration cap -- do not apply to an immune "
                                    "mechanism.",
    "load_bearing_unverified_premise": "That localized HS carries a PTPN11/KRAS hotspot at all.",
}


def verify_antigen_convergence(clone_names: list[str], vaccine_kill_schedule: np.ndarray) -> dict:
    """Check the engine's own kill mask against the convergence claim, rather than trusting prose.
    `ramping_kill_schedule` returns a (horizon, k) array whose per-clone columns are zero for
    clones the vaccine cannot see. The convergence argument predicts a specific pattern: every
    drug-resistance clone receives nonzero vaccine kill, and exactly one clone (`immune_escape`)
    does not.
    """
    schedule = np.asarray(vaccine_kill_schedule, dtype=float)
    if schedule.ndim != 2 or schedule.shape[1] != len(clone_names):
        raise ValueError("vaccine_kill_schedule must be (horizon_days, len(clone_names))")
    covered = schedule.max(axis=0) > 0
    rows, mismatches = [], []
    for index, name in enumerate(clone_names):
        expectation = ANTIGEN_RETENTION.get(name)
        expected = None if expectation is None else expectation["retains_driver_antigen"]
        actual = bool(covered[index])
        rows.append({"clone": name, "expected_vaccine_coverage": expected,
                     "actual_vaccine_coverage": actual,
                     "reason": None if expectation is None else expectation["reason"]})
        if expected is not None and expected != actual:
            mismatches.append(name)
    drug_resistance_clones = [n for n in clone_names
                              if n not in ("sensitive", "immune_escape")
                              and n in ANTIGEN_RETENTION]
    return {
        "per_clone": rows,
        "mismatches": mismatches,
        "consistent": not mismatches,
        "all_drug_resistance_routes_covered": all(
            covered[clone_names.index(n)] for n in drug_resistance_clones),
        "n_routes_evading_vaccine": int((~covered).sum()),
        "interpretation": (
            "The kill mask matches the convergence argument: every drug-resistance route is covered "
            "and only the antigen-loss clone escapes."
            if not mismatches else
            f"MASK DOES NOT MATCH THE ARGUMENT for {mismatches} -- the convergence claim cannot be "
            "relied on with this schedule."),
    }


def handoff_timing(cytotoxic_exposure_days: int, vaccine_start_day: int,
                   vaccine_ramp_days: float) -> dict:
    """Does persistent immune pressure arrive before a duration-capped cytotoxic has to stop? The
    lomustine analysis found the duration cap to be the binding constraint on durability -- the
    benefit collapsed purely from stopping. That framing implicitly assumed nothing replaced it.
    """
    for name, value in (("cytotoxic_exposure_days", cytotoxic_exposure_days),
                        ("vaccine_ramp_days", vaccine_ramp_days)):
        if value <= 0:
            raise ValueError(f"{name} must be positive")
    if vaccine_start_day < 0:
        raise ValueError("vaccine_start_day must be nonnegative")
    full_effect = vaccine_start_day + vaccine_ramp_days
    gap = full_effect - cytotoxic_exposure_days
    # How much of the vaccine's maximum kill is actually online at the instant the cytotoxic stops --
    # the number that matters, and more informative than either the binary or the day-count, since the
    # ramp is 1 - exp(-elapsed/ramp_days) and reaches only ~63% at `full_effect` by construction.
    elapsed_at_stop = cytotoxic_exposure_days - vaccine_start_day
    fraction_at_stop = float(np.clip(1 - np.exp(-max(elapsed_at_stop, 0.0) / vaccine_ramp_days),
                                     0.0, 1.0))
    return {
        "cytotoxic_exposure_days": int(cytotoxic_exposure_days),
        "vaccine_start_day": int(vaccine_start_day),
        "vaccine_full_effect_day": float(full_effect),
        "overlap_days": float(elapsed_at_stop),
        "vaccine_fraction_of_max_at_cytotoxic_stop": fraction_at_stop,
        "uncovered_gap_days": float(max(0.0, gap)),
        "continuous_pressure": bool(vaccine_start_day <= cytotoxic_exposure_days),
        "interpretation": (
            "of its maximum when the cumulative-dose cap forces the drug to stop. There is no "
            "interval with nothing acting, so the duration cap is only binding in the absence of "
            "a persistent second mechanism."
            if vaccine_start_day <= cytotoxic_exposure_days else
            f"There is a {gap:.0f}-day window with neither mechanism at strength, which is exactly "
            "when a suppressed subclone regrows unopposed."),
    }


def vaccine_potency_threshold(growth_rates: np.ndarray, clone_names: list[str],
                              margin: float = 0.002) -> dict:
    """The vaccine potency at which pre-existing resistance stops mattering at all. This is the
    sharpest consequence of antigen convergence, and it is a *structural* result rather than a
    better number. Because the vaccine covers every drug-resistance clone (see
    `verify_antigen_convergence`) and is subject to neither the cytostatic ceiling nor a
    cumulative-dose duration cap (`mechanism_constraint_matrix`), a potency exceeding the fastest
    covered clone's growth rate drives every such clone to a negative net margin *permanently* --
    not for a dosing window.
    """
    growth_rates = np.asarray(growth_rates, dtype=float)
    if len(growth_rates) != len(clone_names):
        raise ValueError("growth_rates and clone_names must align")
    if margin < 0:
        raise ValueError("margin must be nonnegative")
    covered = [(name, float(rate)) for name, rate in zip(clone_names, growth_rates)
               if ANTIGEN_RETENTION.get(name, {}).get("retains_driver_antigen")
               and name != "sensitive"]
    if not covered:
        raise ValueError("no vaccine-covered drug-resistance clones found in clone_names")
    fastest_name, fastest_rate = max(covered, key=lambda item: item[1])
    return {
        "covered_drug_resistance_clones": dict(covered),
        "fastest_covered_clone": fastest_name,
        "fastest_covered_growth_rate": fastest_rate,
        "threshold_vaccine_max_kill": fastest_rate + margin,
        "margin": float(margin),
        "below_threshold_behaviour": "outcome ~= 1 - preexisting_prob; dominated by a parameter no "
                                    "assay can measure",
        "at_or_above_threshold_behaviour": "outcome insensitive to preexisting_prob -- a pre-existing "
                                          "subclone is suppressed indefinitely rather than outgrowing",
        "why_this_is_the_real_result": "Crossing this threshold does not improve an estimate of "
                                       "an unmeasurable quantity; it removes the model's "
                                       "dependence on it.",
        "still_outside_it": "the antigen-loss / immune-escape route, which the vaccine cannot cover "
                           "by construction and whose seeding rate is an unmeasured constant",
    }


def mechanism_constraint_matrix() -> dict:
    """Which of the two hard constraints each candidate second mechanism is subject to. The compact
    form of why the endurance case rests on the vaccine. Both constraints were derived elsewhere
    in this repo and neither is a modeling convention: the cytostatic ceiling is arithmetic
    (`pharmacology.cytostatic_ceiling`), and the duration cap comes from measured cumulative
    hepatotoxicity (`pharmacology.CCNU_DURATION_LIMIT`).
    """
    return {
        "cdk46_inhibitor": {
            "cytostatic_ceiling_applies": True,
            "cumulative_dose_duration_cap": False,
            "covers_all_drug_resistance_routes": True,
            "verdict": "can be sustained indefinitely but cannot reach the required kill rate -- "
                      "arrest cannot exceed the clone's own growth rate at any dose",
        },
        "lomustine": {
            "cytostatic_ceiling_applies": False,
            "cumulative_dose_duration_cap": True,
            "covers_all_drug_resistance_routes": True,
            "verdict": "reaches the kill rate (cytotoxic, DNA crosslinking acts "
                      "downstream-independently) but cannot be sustained -- cumulative irreversible "
                      "hepatotoxicity caps exposure at ~105 days",
        },
        "hotspot_vaccine": {
            "cytostatic_ceiling_applies": False,
            "cumulative_dose_duration_cap": False,
            "covers_all_drug_resistance_routes": True,
            "verdict": "subject to NEITHER constraint -- immune cytolysis removes cells, and "
                       "immunological memory persists after dosing ends.",
            "its_own_escape_route": "antigen loss / MHC-I downregulation (the immune_escape "
                                    "clone) -- a real, separate mechanism, modeled with its own "
                                    "Poisson seeding process.",
        },
    }
