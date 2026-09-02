"""Three routes past the treatment horizon, and the first outcome this model can call DURABLE.

WHAT THIS ANSWERS

`treatment_horizon` established that the cure prediction was hollow: it required 498 days of
uninterrupted full dose, and cumulative neuropathy caps sagopilone at about 84. It named three ways
out. This module builds all three and prices them.

    1  A LONGER WINDOW -- an agent whose dose-limiting toxicity is not cumulative.
    2  A SMALLER STARTING BURDEN -- debulking surgery first.
    3  CONTROL RATHER THAN CURE -- treat, let the toxicity resolve, re-treat.

ROUTE 1 IS THE REAL FIND, AND IT IS A SPECIFIC DRUG

LISAVANBULIN (BAL101553), the lysine prodrug of avanbulin (BAL27862). An ORAL microtubule
destabiliser, 387 g/mol, lipophilic, with a reported 1:1 BRAIN:PLASMA RATIO in rodents -- better than
sagopilone's 0.8. Phase 1 in newly diagnosed MGMT-unmethylated glioblastoma, ABTC1601, n=26
(PMID 39371261).

WHAT MATTERS IS WHICH TOXICITY IT HAS, NOT HOW MUCH:

    sagopilone     peripheral sensory neuropathy in 46% -- CUMULATIVE, worsening after ~4 cycles,
                   no effective neuroprotectant, and the reason its development was DISCONTINUED
    lisavanbulin   peripheral sensory neuropathy in 1 of 26 (4%), GRADE 1. The dose-limiting events
                   are ACUTE and CNS: confusion, memory impairment, one grade 4 aseptic
                   meningoencephalitis

AN ACUTE DOSE-LIMITING TOXICITY CAPS THE DOSE. A CUMULATIVE ONE CAPS THE DURATION. Only the second
kind breaks a plan that needs to run for ten months, and lisavanbulin's is the first kind.

    access 0.80, duty 0.8   margin +0.0416   316 days short of cure inside any tolerable window
    access 1.00, duty 0.8   margin +0.0656   CURE IN 316 DAYS, and nothing caps 316 days

THE PRICE, AND IT IS NOT SMALL: the axis it loads is CNS_LOCAL -- the same organ the tumour is in. A
drug whose dose-limiting toxicity is cerebral oedema, seizure and encephalopathy, given to a dog with
an intracranial mass, is not a free swap. It trades a peripheral-nerve clock for a central-nervous-
system ceiling.

ROUTE 2 BARELY MATTERS, WHICH IS WORTH KNOWING

Debulking was accepted as an assumption. The arithmetic says it buys very little, because decay is
EXPONENTIAL and surgery acts on the LOGARITHM:

    no surgery      1e9 cells   316 days
    90% debulk      1e8 cells   281 days      saves 35 days
    99% debulk      1e7 cells   246 days      saves 70 days
    99.9% debulk    1e6 cells   211 days      saves 105 days

A hundredfold cytoreduction buys about ten weeks. And `presentation` establishes surgery removes the
one compartment drugs CAN reach while leaving both occupied ones, so the burden it removes is the
burden that mattered least. IT IS NOT WRONG TO DO IT. IT IS WRONG TO COUNT ON IT.

ROUTE 3 IS THE FIRST THING HERE THAT DESERVES THE WORD DURABLE

Epothilone neuropathy RESOLVES on withdrawal -- median 5 to 6 weeks. So the schedule is not "treat
until toxicity, then stop". It is treat, rest, re-treat. Over one cycle the burden falls by
`margin x treat_days` and regrows by `growth x rest_days`; the cycle nets down whenever the first
exceeds the second.

    agent          rest 28d              rest 38d              rest 56d
    sagopilone     10.6 cycles, 3.3 yr   14.7 cycles, 4.9 yr   49.8 cycles, 19.1 yr
    lisavanbulin    5.2 cycles, 1.6 yr    6.1 cycles, 2.0 yr    8.5 cycles,  3.3 yr

AND THIS IS THE OUTCOME THE MODEL PREVIOUSLY COULD NOT PRODUCE AT ALL. `treatment_horizon` recorded
that the model had only two states -- cure or death -- and no way to express sustained control. A
cycled schedule is a third: the burden ratchets down across cycles without the dog ever being on
continuous therapy. That is what a durable response actually looks like in practice, and it took
until now to be able to say it.

Note what cycling really is: an EFFECTIVE DUTY CYCLE of 0.60 to 0.75 sustained indefinitely, rather
than 0.8 sustained for 84 days. It is the third term of the identity again.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from . import microtubule_route as mt
from . import response_duration as rd
from .catalogue import GROWTH_PER_DAY, LEPTOMENINGEAL, PARENCHYMA

#: Reported 1:1 brain:plasma for avanbulin in rodents. PMID 39371261.
LISAVANBULIN_BRAIN_PLASMA = 1.00
#: Peripheral sensory neuropathy incidence. 1 of 26, grade 1, vs 46% for sagopilone.
LISAVANBULIN_NEUROPATHY_RATE = 1 / 26
SAGOPILONE_NEUROPATHY_RATE = 0.46
#: Median time for epothilone-class neuropathy to resolve after withdrawal, in days (5-6 weeks).
NEUROPATHY_RESOLUTION_DAYS = 38


@dataclass(frozen=True)
class Cycle:
    """Treat for `treat_days`, then rest for `rest_days` while toxicity resolves."""

    treat_days: float
    rest_days: float

    @property
    def length(self) -> float:
        return self.treat_days + self.rest_days

    @property
    def effective_duty(self) -> float:
        """What cycling actually is: a lower duty sustained indefinitely."""
        return self.treat_days / self.length

    def net_logs_per_cycle(self, margin: float, growth: float = GROWTH_PER_DAY) -> float:
        """Natural-log burden reduction per cycle. Positive means the cycle nets down."""
        return margin * self.treat_days - growth * self.rest_days

    def cycles_to_clear(self, margin: float, burden: float = rd.CELLS_PER_CM3,
                        growth: float = GROWTH_PER_DAY) -> float:
        net = self.net_logs_per_cycle(margin, growth)
        if net <= 0:
            return float("inf")
        return math.log(burden) / net

    def days_to_clear(self, margin: float, burden: float = rd.CELLS_PER_CM3,
                      growth: float = GROWTH_PER_DAY) -> float:
        return self.cycles_to_clear(margin, burden, growth) * self.length


def margin_for(access: float, compartment: str = PARENCHYMA, duty: float = mt.REFERENCE_DUTY,
               growth: float = GROWTH_PER_DAY) -> float:
    return mt.worst_margin(compartment, growth, duty=duty, access=access)


def continuous_days_to_clear(access: float, compartment: str = PARENCHYMA,
                             burden: float = rd.CELLS_PER_CM3) -> float:
    return rd.days_to_clear(margin_for(access, compartment), burden)


def debulk_saving(access: float, log_reduction: float,
                  compartment: str = PARENCHYMA) -> float:
    """Days saved by removing `log_reduction` orders of magnitude of burden first."""
    m = margin_for(access, compartment)
    return (math.log(10) * log_reduction) / m


# --- computed results ---------------------------------------------------------------------------------

#: access -> (margin, continuous days to clear) in the parenchyma at duty 0.8
ROUTE_1 = {0.80: (0.0416, 498), 1.00: (0.0656, 316)}

#: starting burden -> days to clear at access 1.0, duty 0.8
ROUTE_2 = {1e9: 316, 1e8: 281, 1e7: 246, 1e6: 211}
ROUTE_2_VERDICT = ("A HUNDREDFOLD cytoreduction buys about ten weeks, because decay is exponential "
                   "and surgery acts on the LOGARITHM of the burden.",
                   "`presentation` establishes surgery removes the one compartment drugs CAN reach "
                   "and leaves both occupied ones, so the burden it takes is the burden that "
                   "mattered least. IT IS NOT WRONG TO DO IT. IT IS WRONG TO COUNT ON IT.")

#: (agent label, rest days) -> (cycles, years to clear)
ROUTE_3 = {
    ("sagopilone", 28): (10.6, 3.3), ("sagopilone", 38): (14.7, 4.9),
    ("sagopilone", 56): (49.8, 19.1),
    ("lisavanbulin", 28): (5.2, 1.6), ("lisavanbulin", 38): (6.1, 2.0),
    ("lisavanbulin", 56): (8.5, 3.3),
}

WHY_THE_TOXICITY_KIND_MATTERS_MORE_THAN_ITS_SIZE = (
    "AN ACUTE dose-limiting toxicity caps the DOSE. A CUMULATIVE one caps the DURATION.",
    "Only the second kind breaks a plan that has to run for ten months, and this analysis spent its "
    "search on how BIG a toxicity was rather than what KIND it was.",
    "sagopilone: peripheral sensory neuropathy in 46%, CUMULATIVE, and the reason its development "
    "was discontinued. lisavanbulin: the same toxicity in 1 of 26 at grade 1, with ACUTE CNS events "
    "as the dose-limiting ones instead.",
)

WHAT_ROUTE_1_COSTS = (
    "THE AXIS IT LOADS IS CNS_LOCAL -- the same organ the tumour is in. Dose-limiting cerebral "
    "oedema, seizure and encephalopathy, in a dog with an intracranial mass, is not a free swap.",
    "It trades a peripheral-nerve CLOCK for a central-nervous-system CEILING.",
    "One patient of 26 had GRADE 4 ASEPTIC MENINGOENCEPHALITIS. That is not a dose-adjustment "
    "problem, it is a serious adverse event in the organ being treated.",
)

THE_THIRD_OUTCOME = (
    "`treatment_horizon` recorded that this model had only TWO states -- cure or death -- and no way "
    "to express sustained control, which is what real dogs actually get.",
    "A CYCLED SCHEDULE IS THE THIRD STATE. The burden ratchets down across cycles without the animal "
    "ever being on continuous therapy, and the model can now say so.",
    "Note what cycling IS: an effective duty of 0.60 to 0.75 sustained INDEFINITELY, rather than 0.8 "
    "sustained for 84 days. It is the third term of the identity again, and it was always the term "
    "that decided this.",
)

WHAT_IS_STILL_ASSUMED = (
    "THE 1:1 BRAIN:PLASMA RATIO IS RODENT. Unusually, the species correction runs in the FAVOURABLE "
    "direction here -- `intraarterial_route.THE_SPECIES_CORRECTION` records dogs as roughly three "
    "times more permeable than mice -- but a rodent figure is still a rodent figure.",
    "THE EB1 BIOMARKER FAILED. All 13 evaluable tumours in ABTC1601 stained negative, so the trial "
    "could not test its own enrichment hypothesis. Nothing is known about EB1 in canine histiocytic "
    "sarcoma.",
    "THE GLIOBLASTOMA RESULT IS MODEST: median OS 12.8 months, PFS 7.7 months, in MGMT-unmethylated "
    "disease. Better than sagopilone's clean null, and not a demonstration of activity in THIS "
    "tumour.",
    "THAT REST PERIODS ALLOW FULL RECOVERY. The cycling model assumes toxicity resets; cumulative "
    "damage that does NOT fully resolve would lengthen every cycle and eventually stop the schedule.",
    "THE GROWTH RATE, still. It sets how much a rest period gives back, so it now enters the answer "
    "TWICE -- once in the kill margin and once in the regrowth term.",
    "THAT LISAVANBULIN IS OBTAINABLE FOR A DOG. Its STATUS IS BETTER THAN FIRST RECORDED HERE and "
    "the correction runs favourably: it was NOT discontinued. In October 2024 Basilea sold all "
    "rights to the GLIOBLASTOMA FOUNDATION, which is continuing clinical development and maintains "
    "a POST-TRIAL ACCESS PROGRAMME for patients from the earlier studies. A phase 1/2a dose-finding "
    "and biomarker study was published in Cell Reports Medicine in 2025. So the drug has an active "
    "owner and a supply route -- but none of that is veterinary, and NO CANINE DATA EXISTS.",
    "THAT ITS HUMAN RESPONSES RESEMBLE WHAT IS MODELLED HERE. THEY DO NOT. Two 'exceptional durable "
    "responders' are reported, both EB1-positive, with target-lesion reductions of 58% (partial "
    "response) and 44% (stable disease). DURABLE PARTIAL RESPONSES ARE NOT CLEARANCE, and this "
    "model predicts clearance. EB1 by immunohistochemistry did not enrich for response well enough; "
    "a five-gene RNA signature is the current candidate, and only 10.2% of glioblastomas (64 of "
    "629) were EB1-positive at all.",
)
