"""The cure prediction assumed a treatment duration the drug does not permit. IT IS NOT CURATIVE.

THE QUESTION THAT EXPOSED THIS

"So these are potentially curative? Does that mean durability beyond ten years is true by default?"

The honest answer is that ">10 years" WAS true by default -- and that is a defect in the model, not a
finding about the dog. `response_duration` computes clearance from a fixed margin, and a fixed
positive margin drives the burden to zero and keeps it there. The model has exactly TWO outcomes:

    margin > 0    the tumour clears completely and never returns      CURE
    margin <= 0   the tumour grows without bound                      DEATH

THERE IS NO "RESPONDS, THEN RELAPSES" IN IT. That is the outcome almost every real cancer patient and
every real dog in this literature actually has, and the model could not produce it at all. A model
whose only outcomes are cure and death is not answering a durability question -- it is restating the
sign of a subtraction.

WHAT WAS MISSING: THE TREATMENT CLOCK

`schedule_coherence` fixed access and duty at an INSTANT -- a drug cannot be delivered monthly and be
present continuously. It never asked the next question: CAN THE SCHEDULE BE SUSTAINED FOR AS LONG AS
THE CURE CALCULATION REQUIRES?

It cannot, and the reason is the toxicity this analysis had already identified:

    cure requires                     498 days of uninterrupted full-dose exposure
    epothilone neuropathy is          CUMULATIVE, worsening especially after FOUR CYCLES
    four cycles at q3wk is            84 days
    fraction of the way to cure       17%

There is no neuroprotective agent that works. The only management is dose reduction or delay.

AND THE DOSE REDUCTION IS WHAT KILLS IT

    after 84 days at full dose:  1e9 cells -> 3.0e7 cells    IMAGING-UNDETECTABLE
    then held at 75% dose:       margin +0.0176   still shrinking, 978 more days
    then held at 50% dose:       margin -0.0064   REGROWS, doubling every 109 days
    then held at 25% dose:       margin -0.0304   REGROWS, doubling every 23 days

A 50% reduction tips the margin negative. So the predicted course is not cure. It is:

    COMPLETE RADIOGRAPHIC RESPONSE, THEN RELAPSE.

THE MODEL NOW REPRODUCES THE ONE REAL CASE, WHICH IT PREVIOUSLY CONTRADICTED

The October 2024 predisposed dog breed with intracranial histiocytic sarcoma: response and tumour
reduction by DAY 99, regrowth confirmed by DAY 124, dead at day 195.

That is the shape this model produces once the treatment clock is in it -- undetectable inside three
months, regrowth once the dose comes down. Before the clock, the model said cure at sixteen months
and had no way to express what that dog actually did. AGREEING WITH THE ONE OBSERVATION AVAILABLE IS
WEAK EVIDENCE, BUT DISAGREEING WITH IT WAS A REASON TO DISBELIEVE THE MODEL, AND THAT REASON IS NOW
GONE.

THE FIFTH INSTANCE OF THE SAME ERROR

    a mouse potency with a dog dose
    one drug's penetration with another drug's plasma level
    a coverage claim in prose the arithmetic could not see
    an access term from one schedule with a duty term from another
    AND NOW: A CLEARANCE TIME FROM ONE HORIZON WITH A TOLERABLE DOSE FROM ANOTHER

Every one is two numbers from different contexts multiplied together. This one is the same error in
the TIME dimension rather than the instantaneous one.

WHAT WOULD ACTUALLY BE CURATIVE, STATED AS A REQUIREMENT RATHER THAN A CLAIM

Cure needs the burden driven to zero INSIDE the tolerable window. At an 84-day window that requires a
margin of ln(1e9)/84 = 0.247/day -- roughly SIX TIMES what this regimen achieves, and 4.5x the
tumour's own growth rate. Nothing in this analysis is within an order of magnitude of that.

The alternatives are a longer window (a drug whose toxicity is not cumulative), or a smaller starting
burden (surgery first -- which `presentation` establishes leaves both occupied compartments behind),
or accepting control rather than cure and re-treating on relapse.
"""

from __future__ import annotations

import math

from . import microtubule_route as mt
from . import response_duration as rd
from .catalogue import PARENCHYMA

#: Cycles before epothilone neuropathy severity climbs materially. Reported, not measured in dogs.
CYCLES_BEFORE_NEUROPATHY_BINDS = 4
DAYS_PER_CYCLE_Q3WK = 21
#: The tolerable full-dose window, in days.
TOLERABLE_WINDOW_DAYS = CYCLES_BEFORE_NEUROPATHY_BINDS * DAYS_PER_CYCLE_Q3WK   # 84

STARTING_BURDEN = rd.CELLS_PER_CM3
IMAGING_LIMIT = rd.IMAGING_DETECTION_LIMIT


def burden_after(days: float, margin: float, burden: float = STARTING_BURDEN) -> float:
    return burden * math.exp(-margin * days)


def full_dose_margin(compartment: str = PARENCHYMA) -> float:
    return mt.worst_margin(compartment, duty=mt.REFERENCE_DUTY)


def margin_at_dose_fraction(fraction: float, compartment: str = PARENCHYMA) -> float:
    """Dose reduction scales duty, which scales kill linearly."""
    return mt.worst_margin(compartment, duty=mt.REFERENCE_DUTY * fraction)


def is_curative(compartment: str = PARENCHYMA,
                window: float = TOLERABLE_WINDOW_DAYS) -> bool:
    """Cure requires the burden driven below one cell INSIDE the tolerable window."""
    return burden_after(window, full_dose_margin(compartment)) < 1.0


def margin_required_for_cure(window: float = TOLERABLE_WINDOW_DAYS,
                             burden: float = STARTING_BURDEN) -> float:
    return math.log(burden) / window


def outcome(compartment: str = PARENCHYMA, window: float = TOLERABLE_WINDOW_DAYS,
            dose_fraction_after: float = 0.50) -> dict:
    """What the model predicts once the treatment clock is included."""
    m = full_dose_margin(compartment)
    at_window = burden_after(window, m)
    after = margin_at_dose_fraction(dose_fraction_after, compartment)
    return {
        "days_at_full_dose": window,
        "burden_at_window": at_window,
        "radiographically_undetectable": at_window < IMAGING_LIMIT,
        "fraction_of_the_way_to_cure": window / rd.days_to_clear(m),
        "margin_after_reduction": after,
        "relapses": after <= 0,
        "doubling_time_on_relapse": (0.693 / abs(after)) if after < 0 else float("inf"),
        "verdict": "RESPONSE THEN RELAPSE" if after <= 0 else "continued control",
    }


# --- computed results ---------------------------------------------------------------------------------

CURE_REQUIREMENT = {
    "days_of_full_dose_cure_needs": 498,
    "tolerable_full_dose_window_days": TOLERABLE_WINDOW_DAYS,
    "fraction_achievable": 0.17,
    "margin_that_would_be_needed": 0.247,
    "margin_achieved": 0.0416,
    "shortfall": "roughly SIX TIMES, and 4.5x the tumour's own growth rate. Nothing in this analysis "
                 "is within an order of magnitude of it.",
}

#: dose fraction after the window -> (margin, shrinks?)
AFTER_DOSE_REDUCTION = {1.00: (0.0416, True), 0.75: (0.0176, True), 0.50: (-0.0064, False),
                        0.25: (-0.0304, False)}

THE_MODEL_HAD_NO_RELAPSE_STATE = (
    "`response_duration` computes clearance from a FIXED margin, so the only outcomes are CURE "
    "(margin > 0) and DEATH (margin <= 0).",
    "THERE IS NO 'RESPONDS THEN RELAPSES' IN IT -- which is what almost every real dog in this "
    "literature actually does.",
    "So '>10 years' was TRUE BY DEFAULT for any regimen that closed at all. That is not a finding "
    "about durability. IT IS A RESTATEMENT OF THE SIGN OF A SUBTRACTION.",
)

WHAT_THE_CLOCK_CHANGES = {
    "before": "Cure at 16 months, and no way to express what the one real this breed actually did.",
    "after": "COMPLETE RADIOGRAPHIC RESPONSE INSIDE THREE MONTHS, THEN RELAPSE once the dose comes "
        "down. 1e9 -> 3.0e7 cells by day 84, which is below the imaging limit; then a 50% dose "
        "reduction takes the margin to -0.0064 and the tumour doubles every 109 days.",
    "the_real_case": "October 2024, predisposed dog breed, intracranial HS: response and tumour "
        "reduction by DAY 99, regrowth by DAY 124, dead day 195.",
    "the_honest_weight": "AGREEING WITH ONE OBSERVATION IS WEAK EVIDENCE. But DISAGREEING with it "
        "was a reason to disbelieve the model, and that reason is now gone.",
}

WHAT_WOULD_ACTUALLY_BE_CURATIVE = (
    "A LONGER WINDOW -- an agent whose dose-limiting toxicity is not cumulative. Neuropathy is; that "
    "is what ended sagopilone.",
    "A SMALLER STARTING BURDEN -- surgery first. But `presentation` establishes that surgery removes "
    "the one compartment drugs can reach and leaves both occupied ones behind, so it reduces the "
    "burden in the wrong place.",
    "OR ACCEPTING CONTROL RATHER THAN CURE, and re-treating on relapse -- which is what the "
    "neuropathy's REVERSIBILITY (median 5-6 weeks to resolve) actually permits, and which this "
    "analysis has never modelled.",
)

THE_FIFTH_INSTANCE = (
    "a mouse potency with a dog dose",
    "one drug's penetration with another drug's plasma level",
    "a coverage claim in prose the arithmetic could not see",
    "an access term from one schedule with a duty term from another",
    "AND NOW: A CLEARANCE TIME FROM ONE HORIZON WITH A TOLERABLE DOSE FROM ANOTHER -- the same error "
    "in the TIME dimension rather than the instantaneous one.",
)
