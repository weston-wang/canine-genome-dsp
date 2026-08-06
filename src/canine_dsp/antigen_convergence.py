"""Antigen convergence: why a vaccine catches every drug-resistance route, and why that was missed.

WHY THIS MODULE EXISTS
----------------------
This project derived a specific structural argument early on and then dropped it from three
consecutive analyses. The argument, stated in `run_monte_carlo_with_vaccine`'s own docstring and at
length in the README:

    None of the three modeled drug-resistance escape mechanisms requires losing the driver-mutation
    antigen a vaccine would target. `pathway_reactivation` adds a secondary RAS/RAF hit on top of the
    original mutation, `rtk_bypass` reactivates parallel signaling around it, and
    `target_site_mutation` only alters the MEK-inhibitor binding site. All three keep expressing the
    original PTPN11/KRAS hotspot peptide, so a vaccine against that hotspot still recognizes them.

That is a *convergence* claim, and it is different in kind from the pharmacological convergence
argument about a shared downstream node (CDK4/6). The pharmacological version says the escape routes
share a dependency that one drug can block. The immunological version says the escape routes share an
*antigen* they cannot shed while remaining what they are -- so the vaccine is escape-route-agnostic
by construction rather than by potency.

WHAT WENT WRONG
---------------
`single_patient_cli`, `pharmacology_cli`, and `mutational_supply_cli` all call `run_monte_carlo`, not
`run_monte_carlo_with_vaccine`. Every headline conclusion in those three analyses was computed with
the vaccine at zero -- including:

  * "the with-pre-existing-subclone arm is 0.0% durable, lost to lomustine's duration cap regardless
    of any mutation rate." That arm is precisely what the convergence argument says a vaccine
    rescues, because a pre-existing drug-resistant subclone still carries the driver antigen.
  * "neither agent is the answer... what this regimen would need is a ceiling-free partner without a
    cumulative-dose duration cap. Whether such an agent exists for canine HS is not established
    here." It was already implemented in this repo. A vaccine satisfies both requirements:

        - NOT cytostatic-ceiling-limited (`pharmacology.cytostatic_ceiling`): immune cytolysis
          removes cells, so its kill term may legitimately exceed a clone's growth rate.
        - NOT duration-capped (`pharmacology.cumulative_dose_limited_days`): immunological memory
          persists after dosing ends; there is no cumulative-organ-toxicity analogue to lomustine's
          irreversible hepatotoxicity forcing a stop.

So the "two candidates fail on opposite axes" framing was not wrong about the two drugs -- it was
wrong to conclude from them that nothing satisfies both constraints, while a third component that
does was sitting unused in the same codebase.

THE TIMING IS THE NON-OBVIOUS PART
----------------------------------
Lomustine's cumulative-dose cap forces its exposure to end at day ~105 (`CCNU_EXPOSURE_DAYS`). The
vaccine ramps from `VACCINE_START_DAY = 90` and reaches full effect around day 111
(`+ VACCINE_RAMP_DAYS`). The immune term takes over almost exactly as the cytotoxic window closes,
which is why "time-limited cytotoxic, then persistent immune pressure" is a coherent architecture
rather than two drugs that happen to be co-administered. `handoff_timing` computes that overlap so it
is a reported number rather than a coincidence noticed in prose.

WHAT IS REAL HERE VS. ASSUMED
-----------------------------
The convergence claim itself is a mechanistic deduction from what each modeled resistance mechanism
does -- it is checkable against the engine's own kill mask (`verify_antigen_convergence`) and this
module does exactly that rather than restating it. What is NOT established: that Corgi HS carries a
PTPN11/KRAS hotspot at all (this repo's oldest and largest open premise), that a canine vaccine
against such a hotspot would achieve any particular kill rate (`vaccine_max_kill` remains a swept,
unfitted knob -- no canine cancer vaccine trial exists for this disease), and the immune-escape
clone's seeding rate and fitness cost, both illustrative.
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
                 "MHC-I-downregulation event. Modeled as a separate 5th clone with its own Poisson "
                 "seeding process, since it is mechanistically unrelated to drug resistance and "
                 "confers no advantage before immune pressure exists",
    },
}

CONVERGENCE_ARGUMENT = {
    "claim": "Every drug-resistance route in this model retains the driver-mutation antigen, so a "
            "vaccine against that hotspot is escape-route-agnostic -- it covers all three routes by "
            "construction rather than by being potent enough to out-kill each one separately.",
    "distinct_from": "The pharmacological convergence argument (all three routes share a downstream "
                    "CDK4/6 dependency, so one drug at that node closes them simultaneously). That "
                    "one is about a shared *dependency* and depends on reaching a potency threshold; "
                    "this one is about a shared *antigen* and does not.",
    "why_it_matters_for_endurance": "The two constraints that defeated both small-molecule second "
                                   "agents -- the cytostatic ceiling and the cumulative-dose "
                                   "duration cap -- do not apply to an immune mechanism. Combined "
                                   "with route-agnostic coverage, that is why the endurance case "
                                   "rests on the vaccine rather than on either drug.",
    "load_bearing_unverified_premise": "That Corgi HS carries a PTPN11/KRAS hotspot at all. The "
                                      "convergence argument is a deduction about what resistance "
                                      "mechanisms do to an antigen; it says nothing about whether "
                                      "the antigen is there to begin with.",
}


def verify_antigen_convergence(clone_names: list[str], vaccine_kill_schedule: np.ndarray) -> dict:
    """Check the engine's own kill mask against the convergence claim, rather than trusting prose.

    `ramping_kill_schedule` returns a (horizon, k) array whose per-clone columns are zero for clones
    the vaccine cannot see. The convergence argument predicts a specific pattern: every
    drug-resistance clone receives nonzero vaccine kill, and exactly one clone (`immune_escape`) does
    not. If a future change to the mask silently broke that -- e.g. excluding a drug-resistance clone
    from vaccine coverage -- the argument would no longer hold and this returns `consistent=False`.

    Verifying the *mask* rather than an outcome is deliberate: the claim is structural, so it should
    be checked structurally instead of inferred from a durable-response number that many other
    parameters also move.
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
    """Does persistent immune pressure arrive before a duration-capped cytotoxic has to stop?

    The lomustine analysis found the duration cap to be the binding constraint on durability -- the
    benefit collapsed purely from stopping. That framing implicitly assumed nothing replaced it. This
    computes whether the vaccine's ramp closes the gap, and reports the uncovered interval when it
    does not, so "the cap is the binding constraint" becomes a statement conditional on the schedule
    rather than an unconditional finding.

    `vaccine_full_effect_day` uses `start + ramp_days`, at which the `1 - exp(-t/ramp)` schedule has
    reached ~63% of maximum; the label is a convention for "substantially on", not saturation.
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
            f"The vaccine begins at day {vaccine_start_day}, while the cytotoxic window runs to day "
            f"{cytotoxic_exposure_days} -- an overlap of {elapsed_at_stop:.0f} days, so immune "
            f"pressure is already at {fraction_at_stop:.0%} of its maximum when the cumulative-dose "
            "cap forces the drug to stop. There is no interval with nothing acting, so the duration "
            "cap is only binding in the absence of a persistent second mechanism. Note the ramp is "
            f"still climbing for another {max(0.0, gap):.0f} days after the drug ends -- coverage is "
            "continuous but not instantaneously full."
            if vaccine_start_day <= cytotoxic_exposure_days else
            f"There is a {gap:.0f}-day window with neither mechanism at strength, which is exactly "
            "when a suppressed subclone regrows unopposed."),
    }


def mechanism_constraint_matrix() -> dict:
    """Which of the two hard constraints each candidate second mechanism is subject to.

    The compact form of why the endurance case rests on the vaccine. Both constraints were derived
    elsewhere in this repo and neither is a modeling convention: the cytostatic ceiling is arithmetic
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
                      "immunological memory persists after dosing ends. Covers every drug-resistance "
                      "route by antigen convergence rather than by potency. This is the component "
                      "the endurance case actually rests on, and the three analyses that concluded "
                      "'neither agent is the answer' had it switched off.",
            "its_own_escape_route": "antigen loss / MHC-I downregulation (the immune_escape clone) -- "
                                   "a real, separate mechanism, modeled with its own Poisson seeding "
                                   "process. Note this is the only route that CAN evade the vaccine, "
                                   "which is not the same as it being the route that actually fires: "
                                   "at the swept potencies tested it never establishes, and "
                                   "long-horizon erosion instead comes from a drug-resistance clone "
                                   "whose growth rate exceeds the vaccine potency being swept",
        },
    }
