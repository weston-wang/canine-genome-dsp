"""ACCESS AND DUTY MUST COME FROM THE SAME SCHEDULE. They did not, and that invalidates the answer.

THE DEFECT, STATED PLAINLY

Effective kill is `potency x access x duty`. This project has repeated that identity in almost every
module as the discipline that keeps coverage honest. It never checked that ACCESS AND DUTY CAN BE
PRODUCED BY THE SAME DOSING SCHEDULE.

They cannot, for every agent in the published regimen:

    temozolomide    access 0.7333   =  0.20 intrinsic  x  3.667 osmotic-disruption gain
                    duty   1.0      =  present above threshold 24 hours a day, every day

The 3.667 requires INTRA-ARTERIAL INFUSION PAST AN OSMOTICALLY OPENED BARRIER. That is a procedure:
arterial catheterisation, general anaesthesia, hypertonic mannitol. Neuwelt's protocol runs it in
MONTHLY cycles. The duty of 1.0 requires the drug to be present continuously.

A DRUG CANNOT BE SIMULTANEOUSLY DELIVERED BY A MONTHLY PROCEDURE AND PRESENT EVERY HOUR OF EVERY DAY.
The regimen's headline margin was the product of two numbers drawn from schedules that exclude each
other.

WHAT IT COSTS, AND IT IS THE WHOLE RESULT

Worst margin in the parenchyma, holding everything else fixed:

    schedule                                    access   duty    kill    worst margin
    oral continuous, intrinsic access only       0.200   1.000   0.0300     -0.0244   OPEN
    IA-boosted, monthly procedure (1 of 28d)     0.733   0.036   0.0039     -0.0505   OPEN
    IA-boosted, weekly procedure (1 of 7d)       0.733   0.143   0.0157     -0.0387   OPEN
    IA-boosted, every third day                  0.733   0.333   0.0367     -0.0177   OPEN
    AS PUBLISHED (IA access x continuous duty)   0.733   1.000   0.1100     +0.0556   closed

ONLY THE INCOHERENT ROW CLOSES. Every physically achievable schedule is open. And the every-third-day
row is not achievable either -- repeated arterial catheterisation with osmotic disruption under
general anaesthesia, twice a week, in an elderly dog, is not a thing that can be done.

A COMBINED SCHEDULE DOES NOT RESCUE IT. Dosing orally every day AND adding a monthly intra-arterial
boost gives a time-averaged access of about 0.20 x 27/28 + 0.733 x 1/28 = 0.219 -- barely above the
oral-only case, because the boost applies on one day in twenty-eight.

WHAT THE COHERENT VERSION LOOKS LIKE

Every agent given orally and continuously, at its OWN measured CNS access, no procedure anywhere:

    parenchyma      -0.0244   OPEN
    leptomeninges   -0.0070   OPEN

It closes only if the cytotoxic's potency is roughly DOUBLE the reference figure -- 0.30/day in the
parenchyma, 0.25/day in the leptomeninges, against an assumed 0.15/day. That is not a result. It is a
statement of what would have to be true, and the number it depends on has never been measured in this
disease.

THIS IS THE SAME ERROR THE PROJECT KEEPS MAKING, IN ITS PUREST FORM

  * a potency measured in mice paired with a dose from dogs
  * one drug's penetration multiplied by another drug's plasma level
  * a coverage claim written in prose that the arithmetic could not see
  * AND NOW: an access term from one schedule multiplied by a duty term from an incompatible one

Every instance is two numbers from different contexts multiplied together. The object model was built
to stop exactly this, and it did not, because `Agent` stores `access` and `duty` as independent
floats WITH NO OBJECT REPRESENTING THE SCHEDULE THAT WOULD HAVE TO PRODUCE BOTH.

WHAT SURVIVES

  * The SITES. The this breed presentation work is untouched -- it is anatomy, not pharmacology.
  * The ESCAPE STRUCTURE. Eleven routes, and the rule that coverage is derived from position.
  * `hs_drug_sensitivity`. Measured in the right species and disease, and independent of scheduling.
  * The FACT that osmotic disruption raises tissue concentration in dogs. What is retracted is the
    right to multiply that gain by a continuous duty cycle.

WHAT IS RETRACTED

  * The published margins of +0.0556 and +0.0732, and every statement that eleven escapes are closed.
  * The claim that the regimen holds at a seven-day doubling. It does not hold at ANY doubling time
    on a schedule that can be delivered.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Route(Enum):
    """How a dose is delivered. THIS is what bounds duty and access together."""

    ORAL_CONTINUOUS = "oral, daily, continuous exposure"
    IV_INTERMITTENT = "intravenous bolus on a cycle"
    IA_WITH_DISRUPTION = "intra-arterial past an osmotically opened barrier -- A PROCEDURE"
    IMPLANT_LOCAL = "implanted or locally infused depot"


#: Route -> the maximum duty cycle that route can physically sustain.
#: A procedure requiring arterial catheterisation and general anaesthesia cannot be run daily.
MAX_DUTY = {
    Route.ORAL_CONTINUOUS: 1.0,
    Route.IV_INTERMITTENT: 0.50,
    Route.IA_WITH_DISRUPTION: 1.0 / 28.0,   # Neuwelt's protocol runs monthly cycles
    Route.IMPLANT_LOCAL: 1.0,
}

#: Route -> whether it confers the osmotic-disruption access gain.
GRANTS_DISRUPTION_GAIN = {
    Route.ORAL_CONTINUOUS: False,
    Route.IV_INTERMITTENT: False,
    Route.IA_WITH_DISRUPTION: True,
    Route.IMPLANT_LOCAL: False,
}


@dataclass(frozen=True)
class Schedule:
    """A route and a duty, checked against each other rather than assumed independent."""

    route: Route
    duty: float

    @property
    def coherent(self) -> bool:
        return 0.0 < self.duty <= MAX_DUTY[self.route]

    @property
    def grants_gain(self) -> bool:
        return GRANTS_DISRUPTION_GAIN[self.route]


def is_coherent(route: Route, duty: float, uses_disruption_gain: bool) -> bool:
    """The check that was missing.

    An agent may claim the osmotic-disruption access gain ONLY if its route is the procedure that
    produces it -- and that route caps duty at roughly one day in twenty-eight.
    """
    if uses_disruption_gain and not GRANTS_DISRUPTION_GAIN[route]:
        return False
    return Schedule(route, duty).coherent


THE_INCOHERENT_COMBINATION = {
    "agent": "temozolomide, as published",
    "access": 0.7333,
    "access_is": "0.20 intrinsic CSF:plasma x 3.667 osmotic-disruption gain",
    "duty": 1.0,
    "duty_is": "present above threshold 24 hours a day, every day",
    "WHY_IT_CANNOT_BOTH_BE_TRUE": "The 3.667 requires arterial catheterisation, general anaesthesia "
        "and hypertonic mannitol -- a PROCEDURE, run monthly in Neuwelt's protocol. The 1.0 requires "
        "continuous presence. No single schedule produces both.",
}

#: schedule label -> (access, duty, worst parenchymal margin)
SCHEDULE_SWEEP = {
    "oral continuous, intrinsic access": (0.200, 1.0, -0.0244),
    "IA-boosted, monthly (1 of 28d)": (0.733, 1 / 28, -0.0505),
    "IA-boosted, weekly (1 of 7d)": (0.733, 1 / 7, -0.0387),
    "IA-boosted, every third day": (0.733, 1 / 3, -0.0177),
    "AS PUBLISHED -- INCOHERENT": (0.733, 1.0, 0.0556),
}

ONLY_THE_INCOHERENT_ROW_CLOSES = (
    "Every physically achievable schedule leaves the parenchyma OPEN.",
    "The every-third-day row is not achievable either: repeated arterial catheterisation with "
    "osmotic disruption under general anaesthesia, twice a week, in an elderly dog.",
    "A COMBINED SCHEDULE DOES NOT RESCUE IT. Oral daily plus a monthly intra-arterial boost gives a "
    "time-averaged access near 0.219, because the boost applies on one day in twenty-eight.",
)

#: compartment -> (coherent all-oral worst margin, cytotoxic potency that would be required)
COHERENT_ALL_ORAL = {
    "parenchyma": (-0.0244, 0.30),
    "leptomeninges": (-0.0070, 0.25),
}
REFERENCE_POTENCY = 0.15

WHAT_IS_RETRACTED = (
    "THE PUBLISHED MARGINS of +0.0556 (parenchyma) and +0.0732 (leptomeninges), and every statement "
    "that all eleven escapes are closed.",
    "THE CLAIM THAT IT HOLDS AT A SEVEN-DAY DOUBLING. It does not hold at ANY doubling time on a "
    "schedule that can actually be delivered.",
    "THE CARBOPLATIN SWAP AND THE MICROTUBULE UPDATE INHERIT THE SAME DEFECT. Both were scored with "
    "an intra-arterial access term and a continuous duty term. Changing the drug does not repair a "
    "scheduling contradiction.",
)

WHAT_SURVIVES = (
    "THE SITES. The this breed presentation work is anatomy, not pharmacology, and is untouched.",
    "THE ESCAPE STRUCTURE. Eleven routes, and the rule that coverage is DERIVED from pathway "
    "position rather than asserted.",
    "`hs_drug_sensitivity`. Measured in the right species and the right disease, and independent of "
    "scheduling. The alkylator class really is the wrong class.",
    "THAT OSMOTIC DISRUPTION RAISES TISSUE CONCENTRATION IN DOGS. What is retracted is the right to "
    "multiply that gain by a continuous duty cycle.",
)

WHY_THE_OBJECT_MODEL_DID_NOT_CATCH_IT = (
    "`Agent` stores `access` and `duty` as INDEPENDENT FLOATS. There is no object representing the "
    "schedule that would have to produce both, so nothing could compare them.",
    "The model was built to stop a coverage claim outrunning its delivery. It did that. It never "
    "considered that the DELIVERY TERM ITSELF could be internally contradictory.",
    "THE GENERAL FORM, and this project has now hit it four times: TWO NUMBERS FROM DIFFERENT "
    "CONTEXTS MULTIPLIED TOGETHER. A mouse potency with a dog dose. One drug's penetration with "
    "another's plasma level. A prose coverage claim the arithmetic could not see. And now an access "
    "term from one schedule with a duty term from an incompatible one.",
)
