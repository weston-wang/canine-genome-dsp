"""Delivery as a first-class, composable object, because leaving it as a float on the agent hid the
whole modality.

WHY THIS EXISTS

`core.catalogue` gave each agent a bare `access` float resolved per compartment. That is enough to
say a small molecule reaches 2.1% of invaded parenchyma. It is not enough to express the thing this
project spent weeks on: THAT ACCESS CAN BE CHANGED BY AN INTERVENTION.

The consequence was concrete and the user caught it. `therapies/local_delivery.py` describes focused
ultrasound, convection-enhanced delivery, intrathecal routes and radiation in careful prose -- and
the SEARCH could not use any of them, because there was no object to combine with an agent. The
catalogue and the combination search contain ZERO occurrences of "ultrasound". A route that had been
examined at length was invisible to the machinery built to examine routes.

WHAT A ROUTE IS

A `DeliveryRoute` transforms an agent's access in a compartment, and carries its own constraints:

    access_multiplier   what it does to the access term
    access_ceiling      what it cannot exceed, regardless of multiplier
    duty                how much of the time the agent is actually there -- a wafer that elutes for
                        five days against a year has duty 0.014, and that is what killed it
    applies_to          which agent classes it can carry. Ultrasound opens TIGHT JUNCTIONS, so it
                        moves small molecules and, at its upper range, antibodies. It does nothing
                        for a P-gp PUMP, and it does not make a cell therapy traffic.
    geometry            FOCAL or DIFFUSE. A sub-millimetric sonication spot against a tumour that is
                        diffusely invasive with meningeal enhancement remote from the mass is the
                        wrong shape, and no multiplier fixes a shape error.

COMPOSING THEM IS THE POINT

    route.apply(agent, compartment) -> a new Agent with modified access and duty

so the search can evaluate "trametinib + focused ultrasound" as a candidate rather than as a
paragraph. THIS IS WHAT MAKES THE EARLIER ULTRASOUND WORK REACHABLE AGAIN.

THE THREE THINGS A ROUTE CAN GET WRONG, ALL OF WHICH THIS PROJECT HIT

  1. WRONG BARRIER. Ultrasound opens tight junctions; the constraint on a P-gp substrate is a pump.
     Modelled by `defeats_efflux`.
  2. WRONG GEOMETRY. A focal spot against diffuse disease. Modelled by `geometry`.
  3. WRONG DURATION. A wafer eluting for five days, a single CED infusion, a 21-day radiation course.
     Modelled by `duty`, and it is the term that killed every local route in this analysis.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .regimen import Agent, Axis


class Geometry(Enum):
    FOCAL = "focal -- a spot or a cavity"
    DIFFUSE = "diffuse -- reaches the whole compartment"


SMALL_MOLECULE_AXES = (Axis.MAPK_SERIAL, Axis.PI3K_PARALLEL, Axis.LINEAGE_SURVIVAL,
                       Axis.CYTOTOXIC, Axis.SURVIVAL_SIGNAL, Axis.FERROPTOSIS,
                       Axis.AUTOPHAGY)

# Agents on an efflux-substrate AXIS that are nonetheless NOT pumped. Lomustine is the case that
# matters: Radtke 2022 (PMID 36252775) found ABCB1 knockout altered response to temozolomide and
# carmustine but NOT to lomustine, and Halsey 2014 (PMID 24885200) found canine sublines retained
# lomustine sensitivity with no functional P-gp. A P-gp inhibitor does nothing for a drug the pump
# does not carry, and applying the 20x to it overstated the metronomic arm by a factor of twenty.
NOT_EFFLUX_SUBSTRATES = ("lomustine", "metronomic lomustine")


@dataclass(frozen=True)
class DeliveryRoute:
    """An intervention that changes an agent's access, with its own constraints attached."""

    name: str
    access_multiplier: float
    access_ceiling: float
    duty: float
    geometry: Geometry
    defeats_efflux: bool
    carries: tuple
    obtainable_for_a_dog: bool
    evidence: str
    note: str = ""

    def can_carry(self, agent: Agent) -> bool:
        """Whether this route can raise THIS agent's access.

        An efflux-inhibition route is gated on the agent actually BEING an efflux substrate. Being
        on a substrate AXIS is not enough -- lomustine sits on the cytotoxic axis and is not pumped
        (Radtke 2022, PMID 36252775), so a P-gp inhibitor does nothing for it. Applying the 20x to
        it overstated the metronomic arm by a factor of twenty.
        """
        if self.access_multiplier > 1.0 and any(
                k in agent.name.lower() for k in NOT_EFFLUX_SUBSTRATES):
            return False
        return agent.axis in self.carries

    def apply(self, agent: Agent, disease_is_diffuse: bool = True) -> Agent | None:
        """A new Agent with access and duty transformed, or None if the route cannot carry it.

        Geometry is enforced here rather than left to the reader: a FOCAL route against DIFFUSE
        disease returns the agent unimproved, because covering part of a compartment is not covering
        the compartment.
        """
        if not self.can_carry(agent):
            return None
        if self.geometry is Geometry.FOCAL and disease_is_diffuse:
            return agent
        access = min(agent.access * self.access_multiplier, self.access_ceiling)
        return Agent(f"{agent.name} + {self.name}", agent.axis, agent.layer, agent.potency,
                     access, agent.duty * self.duty, agent.obtainable and self.obtainable_for_a_dog,
                     agent.division_gated, agent.antigen_directed, agent.note)


FOCUSED_ULTRASOUND = DeliveryRoute(
    name="focused ultrasound",
    access_multiplier=10.0,
    access_ceiling=0.30,
    duty=1.0,
    geometry=Geometry.FOCAL,
    defeats_efflux=False,
    carries=SMALL_MOLECULE_AXES,
    obtainable_for_a_dog=True,
    evidence="MEASURED in dogs: PMC5596444 / PMID 28912896 -- 10 aged beagles, 10.1-13.8 kg, "
             "TRANSCRANIAL with no craniectomy, blood-brain barrier opened in ALL TEN, mean "
             "enhancement 19+/-11%, no tissue damage, one transient adverse event. Canine skull "
             "3.2+/-1.1 mm against human 6.4+/-1.8 mm. Reported enhancement for small molecules "
             "2-10x.",
    note="TWO FAILURES, BOTH STRUCTURAL. WRONG BARRIER: it opens tight junctions, and the constraint "
         "on a P-gp substrate is a PUMP -- so it raises access without defeating efflux. WRONG "
         "GEOMETRY: a sub-millimetric sonication spot against a tumour that is diffusely invasive "
         "(23/23 poorly demarcated) with meningeal enhancement remote from the mass in 19/19 dogs. "
         "The this breed is the right size and skull class and it has never been measured in one.",
)

CONVECTION_ENHANCED_DELIVERY = DeliveryRoute(
    name="convection-enhanced delivery",
    access_multiplier=50.0,
    access_ceiling=1.0,
    duty=1 / 365,
    geometry=Geometry.FOCAL,
    defeats_efflux=True,
    carries=SMALL_MOLECULE_AXES + (Axis.IMMUNE_EFFECTOR,),
    obtainable_for_a_dog=False,
    evidence="Dickinson/Bentley 2020, PMID 32812637: PHASE I, 17 dogs, spontaneous glioma, NO "
             "dose-limiting toxicity at 6x prior human doses, median target coverage 70% (40-94%), "
             "a single treatment giving >=65% volumetric reduction in 50% of dogs.",
    note="Bypasses the barrier entirely, and fails on DURATION -- a single infusion, duty ~1/365. "
         "Also FOCAL: it delivers to a convection volume, and this disease has no edge.",
)

INTRATHECAL_BOLUS = DeliveryRoute(
    name="intrathecal bolus (cisterna magna)",
    access_multiplier=200.0,
    access_ceiling=1.0,
    duty=0.07,
    geometry=Geometry.DIFFUSE,
    defeats_efflux=True,
    carries=SMALL_MOLECULE_AXES,
    obtainable_for_a_dog=True,
    evidence="Safe in dogs and cats (Genoni, Vet Comp Oncol 2016), complication rate 1 in 112. "
             "~6 canine cases in the literature, all multimodal, NONE in histiocytic sarcoma.",
    note="DIFFUSE, which matches this disease, and it is the only obtainable route that reaches the "
         "compartment enhancing in 19/19 dogs. Fails on DUTY CYCLE at 0.07.",
)

INTRATHECAL_SUSTAINED = DeliveryRoute(
    name="intrathecal sustained release",
    access_multiplier=200.0,
    access_ceiling=1.0,
    duty=1.0,
    geometry=Geometry.DIFFUSE,
    defeats_efflux=True,
    carries=SMALL_MOLECULE_AXES,
    obtainable_for_a_dog=False,
    evidence="The schedule that would work: q14d sustained gives 0.897 at 0.08/day and 0.998 at "
             "0.12/day.",
    note="THE FORMULATION DOES NOT EXIST. DepoCyt, the only approved sustained-release intrathecal "
         "cytotoxic, was permanently discontinued 29 June 2017 for manufacturing reasons.",
)

EFFLUX_INHIBITION = DeliveryRoute(
    name="P-gp/BCRP inhibitor co-dose",
    access_multiplier=20.0,
    access_ceiling=0.77,
    duty=1.0,
    geometry=Geometry.DIFFUSE,
    defeats_efflux=True,
    carries=SMALL_MOLECULE_AXES,
    obtainable_for_a_dog=False,
    evidence="Choo 2014, PMID 25243894, MOUSE, cobimetinib: brain:plasma 0.3 wild type, 11.0 in "
             "Mdr1a/b-/-, and 6.0 IN A WILD-TYPE ANIMAL CO-DOSED WITH A P-gp/BCRP INHIBITOR = 20x.",
    note="DIFFUSE and defeats the actual constraint, which is what ultrasound does not. Carries "
         "SMALL MOLECULES ONLY -- a liposome is excluded by size, not pumped out. Canine PK and "
         "safety for elacridar were not established, and a transporter inhibitor is NOT SELECTIVE "
         "FOR THE BRAIN, so it raises exposure in the tissues that set the toxicity ceiling too.",
)

RADIATION_AS_ROUTE = DeliveryRoute(
    name="radiation",
    access_multiplier=1e6,
    access_ceiling=1.0,
    duty=21 / 365,
    geometry=Geometry.DIFFUSE,
    defeats_efflux=True,
    carries=(Axis.DELIVERY,),
    obtainable_for_a_dog=True,
    evidence="Access 1.0 by physics. Measured canine intracranial medians 524/536/512 days.",
    note="Fails on DURATION, and that failure is VALIDATED against measured data.",
)

ROUTES = (FOCUSED_ULTRASOUND, CONVECTION_ENHANCED_DELIVERY, INTRATHECAL_BOLUS,
          INTRATHECAL_SUSTAINED, EFFLUX_INHIBITION, RADIATION_AS_ROUTE)


def obtainable_routes() -> tuple:
    return tuple(r for r in ROUTES if r.obtainable_for_a_dog)


def routes_defeating_efflux() -> tuple:
    return tuple(r for r in ROUTES if r.defeats_efflux)


THE_DEFECT_THIS_FIXES = (
    "`core.catalogue` gave each agent a bare access float. That can say a small molecule reaches "
    "2.1% of invaded parenchyma. It CANNOT say that access is changeable by an intervention.",
    "So `therapies/local_delivery.py` described focused ultrasound, CED, intrathecal routes and "
    "radiation in careful prose, and THE SEARCH COULD NOT USE ANY OF THEM -- the catalogue and the "
    "combination search contained ZERO occurrences of 'ultrasound'.",
    "A route examined at length was invisible to the machinery built to examine routes. That is the "
    "same failure as leaving toxicity in prose, and it has the same fix: make it an object.",
)

THE_THREE_THINGS_A_ROUTE_CAN_GET_WRONG = {
    "wrong barrier": "Ultrasound opens TIGHT JUNCTIONS; the constraint on a P-gp substrate is a "
                     "PUMP. Modelled by `defeats_efflux`.",
    "wrong geometry": "A focal spot against diffuse disease. Modelled by `geometry`, and enforced "
                      "in `apply()` rather than left to the reader.",
    "wrong duration": "A wafer eluting five days, a single CED infusion, a 21-day radiation course. "
                      "Modelled by `duty`, and it is the term that killed every local route here.",
}
