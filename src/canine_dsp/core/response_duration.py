"""How long, in days. Every previous answer gave RATES and never converted them to TIME.

WHY THIS MODULE EXISTS

This project has reported margins -- +0.0416/day, +0.0592/day -- in every version, and never once
said what they mean for a dog. A margin is a rate. "Durable response" is a duration. NOTHING HERE
CONNECTED THEM, and the omission let a positive margin read as an unbounded promise.

THE CONVERSION IS ELEMENTARY AND SHOULD HAVE BEEN THERE FROM THE START

A regimen whose kill exceeds growth shrinks the tumour exponentially:

    N(t) = N0 * exp(-margin * t)      so      t = ln(N0) / margin

At the computed margins, from a 1 cm3 tumour (~1e9 cells, the standard figure at diagnosis):

    brain tissue    margin +0.0416/day      498 days      16.4 months
    linings         margin +0.0592/day      350 days      11.5 months

That is TIME TO THE LAST CELL, not time to a visible response -- a tumour becomes undetectable on
imaging long before it is gone, at roughly 1e8 cells, which is about 55 days sooner.

WHAT "DURABLE" MEANS IN THIS MODEL, STATED EXACTLY

If every assumption held, the answer is not "a duration" -- it is CURE, in about sixteen months, and
the tumour never comes back because there is nothing left. That is what a permanently positive margin
means, and saying it plainly is more useful than hiding behind the rate.

WHICH IS ALSO WHY IT SHOULD BE DISTRUSTED. A model that predicts cure from four unmeasured numbers is
telling you about the model, not about the dog. The duration below is what the arithmetic says; the
limits section is what actually decides.

THE DURABILITY LIMIT IS NOT THE ARITHMETIC, IT IS RESISTANCE -- AND IT WAS CHECKED

A single escape is covered by construction: all eleven close. But a real tumour of 1e9 cells seeds
resistant clones constantly, and the question is whether a clone carrying TWO lesions at once escapes.

    45 double-escape combinations       0 uncovered
    120 triple-escape combinations      0 uncovered

Checked across the full cycling-fraction sweep (0.05 to 1.00), because the persister term depends on
it.

AND THE FIRST VERSION OF THAT CHECK WAS WRONG, IN MY FAVOUR'S OPPOSITE DIRECTION

It reported 9 of 45 uncovered, every one of them a persister pairing, and the pattern looked like a
real structural hole: a dormant cell cannot be touched by a mitotic poison, so dormancy plus anything
else escapes.

The check was using `Agent.reaches`, which excludes a division-gated agent from a non-dividing escape
ENTIRELY. That is the rule `dormancy` exists to correct: persistence is a TRANSIENT STATE, so a
continuously present division-gated agent reaches the cell AT RE-ENTRY, scaled by duty. Applying the
right rule, nothing is uncovered.

Recorded because the error was mine and because it ran PESSIMISTIC -- the direction this project's
errors usually do not run.
"""

from __future__ import annotations

import itertools
import math

from . import microtubule_route as mt
from .catalogue import ESCAPES, GROWTH_PER_DAY, LEPTOMENINGEAL, PARENCHYMA
from .dormancy import CYCLING_FRACTION_SWEEP, DormancyModel

#: Cells in a 1 cm3 tumour. The standard oncology figure.
CELLS_PER_CM3 = 1e9
#: Below roughly this burden a tumour is not visible on imaging.
IMAGING_DETECTION_LIMIT = 1e8

PERSISTER = next(e for e in ESCAPES if "persister" in e.name)


def days_to_clear(margin: float, burden: float = CELLS_PER_CM3,
                  endpoint: float = 1.0) -> float:
    """Exponential decay at `margin` per day, from `burden` cells down to `endpoint`."""
    if margin <= 0:
        return float("inf")
    return math.log(burden / endpoint) / margin


def duration_table(burden: float = CELLS_PER_CM3) -> dict:
    """compartment -> (margin, days to last cell, days to imaging-undetectable)."""
    out = {}
    for compartment in (PARENCHYMA, LEPTOMENINGEAL):
        m = mt.worst_margin(compartment)
        out[compartment] = (m, days_to_clear(m, burden),
                            days_to_clear(m, burden, IMAGING_DETECTION_LIMIT))
    return out


def uncovered_combinations(compartment: str = PARENCHYMA, order: int = 2,
                           cycling_fraction: float = 0.20,
                           growth: float = GROWTH_PER_DAY) -> list:
    """Escape combinations a single clone could carry that the regimen does NOT cover.

    The persister is handled by the DORMANCY rule, not by `reaches`: a division-gated agent is not
    excluded from a dormant cell, it acts at re-entry scaled by duty. Using `reaches` here reported
    9 spurious holes.
    """
    d = DormancyModel(cycling_fraction)
    r = mt.build(compartment)
    bad = []
    for combo in itertools.combinations(ESCAPES, order):
        if PERSISTER in combo:
            others = [e for e in combo if e is not PERSISTER]
            kill = sum(d.kill_from(a) for a in r.agents
                       if all(a.covers(o) for o in others))
            margin = kill - d.effective_growth(growth)
        else:
            kill = sum(a.effective_kill for a in r.agents
                       if all(a.reaches(e) for e in combo))
            margin = kill - growth
        if margin <= 0:
            bad.append((tuple(e.name for e in combo), margin))
    return bad


def resistance_is_covered(compartment: str = PARENCHYMA) -> bool:
    """No single clone, carrying up to three lesions, escapes -- at any cycling fraction."""
    return all(not uncovered_combinations(compartment, order, cyc)
               for order in (2, 3) for cyc in CYCLING_FRACTION_SWEEP)


# --- computed results ---------------------------------------------------------------------------------

#: compartment label -> (margin/day, days to last cell, months, days to become UNDETECTABLE)
#: The last figure is the time to fall to ~1e8 cells, not the gap between the two. It was first
#: written as 443/311 -- the GAP -- which is the same class of transcription slip this project keeps
#: making, caught here by a test asserting the two figures against each other.
DURATION = {
    "brain tissue": (0.0416, 498, 16.4, 55),
    "linings": (0.0592, 350, 11.5, 39),
}

#: margin/day -> days to clear 1e9 cells. What a smaller margin costs in TIME.
DURATION_BY_MARGIN = {0.0416: 498, 0.0300: 691, 0.0200: 1036, 0.0100: 2072, 0.0050: 4145}

COMBINATION_COVERAGE = {"doubles_total": 45, "doubles_uncovered": 0,
                        "triples_total": 120, "triples_uncovered": 0}

WHAT_DURABLE_MEANS_HERE = (
    "IF EVERY ASSUMPTION HELD, the answer is not a duration -- it is CURE, in roughly sixteen months, "
    "because a permanently positive margin drives the burden to zero and nothing is left to regrow.",
    "THAT IS ALSO WHY IT SHOULD BE DISTRUSTED. A model predicting cure from four unmeasured numbers "
    "is telling you about the model, not about the dog.",
    "The measured benchmark for this disease remains 44 DAYS with full conventional treatment. This "
    "model's own prediction is more than eleven times that, and no living dog has received it.",
)

THE_CHECK_THAT_RAN_PESSIMISTIC = {
    "what_it_reported": "9 of 45 double-escape combinations uncovered, EVERY ONE a persister pairing. "
        "It looked like a clean structural hole: a dormant cell cannot be touched by a mitotic "
        "poison, so dormancy plus anything else escapes.",
    "the_bug": "It used `Agent.reaches`, which excludes a division-gated agent from a non-dividing "
        "escape ENTIRELY -- the exact rule `dormancy` exists to correct. Persistence is a TRANSIENT "
        "STATE; a continuously present agent reaches the cell at RE-ENTRY, scaled by duty.",
    "corrected": "0 of 45 doubles and 0 of 120 triples uncovered, across the full cycling-fraction "
        "sweep.",
    "why_it_is_recorded": "The error was mine and it ran PESSIMISTIC -- the direction this project's "
        "errors usually do not run. A model that only ever errs optimistically is not being checked.",
}

WHAT_DECIDES_THE_REAL_DURATION = (
    "NOT the resistance arithmetic. Every single, double and triple escape combination is covered, "
    "so within the model nothing regrows.",
    "THE GROWTH RATE. Unmeasured. Between a ten-day and a seven-day doubling the margin crosses zero "
    "and the duration goes from sixteen months to INFINITE -- the tumour never clears at all.",
    "THE POTENCY, 0.15/day, and the DUTY, 0.8. Both assumed. Halve the margin and the clearance time "
    "doubles; the relationship is exactly inverse, so a modest error in either is a large error in "
    "months.",
    "WHETHER AN OBTAINABLE AGENT HAS THESE PROPERTIES AT ALL. Sagopilone's development was "
    "DISCONTINUED for the neuropathy this model prices at 0.85, and the two newer compounds have "
    "never been in a dog.",
)
