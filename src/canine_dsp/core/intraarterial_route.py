"""[SUPERSEDED HEADLINE — AUDIT BANNER] The intra-arterial access GAIN claimed here was retracted by
core.schedule_coherence: a monthly-procedure access multiplied by a continuous duty cycle is
physically impossible, so "closes all escapes" does not hold. The live chain imports this module
ONLY for the surviving measured constant PAXALISIB_KPUU (an oral, intrinsic, P-gp/BCRP non-substrate
value). CONSERVATIVE_GAIN is never applied in the live answer. Live answer: core.breed_wide_durability.

The one delivery route with a MEASURED effect size in dogs -- and what it costs to give.

TOXICITY WAS NOT PRICED, AND THAT WAS A REAL GAP

This module originally proposed a regimen and never ran it through `core.toxicity` -- the class
built specifically so that a regimen could not be proposed without its cost. NONE of the three new
components had a toxicity profile at all: temozolomide, paxalisib, and the intra-arterial procedure
itself. The object model was supposed to make that impossible and it did not, because a missing
profile fails as a KeyError at the call site rather than as a refusal at construction.

Profiles added, and TWO COLLISIONS FALL OUT IMMEDIATELY:

    MARROW      temozolomide 0.55 + hydroxychloroquine 0.45 = EXACTLY 1.00. Zero headroom. Both
                agents suppress marrow and the budget is spent to the last percent.
    CNS         radiation 0.80 + osmotic-disruption seizure risk. Seizures are the classic
                complication of osmotic BBB opening, and radiation raises seizure risk in an
                already-irritable brain. Scored on a shared CNS axis this reaches 1.10 --
                OVERSUBSCRIBED -- and forces radiation down to 91% of dose.

ONE HONEST COUNTER-ARGUMENT, WHICH IS REAL

Intra-arterial delivery is dose-SPARING by construction: the same brain concentration comes from a
smaller systemic dose, because the drug is not diluted through the whole animal first. At roughly a
third of systemic exposure, temozolomide's marrow load falls 0.55 -> 0.18 and the marrow axis goes
from 1.00 to 0.63. The route pays for part of its own toxicity.

But that does not fix the CNS axis, because the seizure risk is LOCAL and dose-sparing is SYSTEMIC.

AND THE FIX IS TO DROP RADIATION

Radiation was in the regimen to supply access -- 1.0 by physics, when nothing else could get in.
Intra-arterial delivery after osmotic disruption now supplies that access directly, so radiation is
carrying a toxicity load for a job that has been taken over. Removing it:

    toxicity        TOLERABLE, headroom 0.37. Marrow 0.63, metabolic 0.60, immune 0.30, CNS 0.30.
    assumed growth  brain 10/10 closed (worst +0.0556)   linings 10/10 (worst +0.0732)
    7-day doubling  brain 10/10 closed (worst +0.0116)   linings 10/10 (worst +0.0292)

EVERYTHING STILL CLOSES, WITH MORE TOXICITY HEADROOM THAN BEFORE. The regimen got smaller and
better at the same time, which happens when an agent is present for a reason that has expired.

WHAT THE REMAINING TOXICITIES ACTUALLY ARE, IN PLAIN TERMS

    temozolomide    marrow suppression -- low platelets and white cells. Monitorable by blood count,
                    and the classic reason alkylator treatment stops.
    paxalisib       HIGH BLOOD SUGAR. An ON-TARGET class effect of PI3K inhibition rather than an
                    off-target surprise: the pathway being blocked is the one insulin signals
                    through. May need monitoring and possibly insulin.
    hydroxychloroquine  marrow, sharing the axis with temozolomide -- which is why the two together
                    are the tightest constraint in the regimen.
    clodronate      liver.
    anti-PD-1       immune-mediated events.
    THE PROCEDURE   general anaesthesia PER DOSE, arterial catheterisation, vessel injury or embolic
                    risk, and seizures from the osmotic opening. This is the toxicity that is not a
                    drug, and it is the one a model priced in organ-axis budgets represents worst.



WHAT VERIFICATION RETURNED, AND IT IS THE STRONGEST RESULT IN THIS PROJECT

Every access figure fought over here has been assumed, modelled, borrowed from a rodent, or measured
in the wrong drug. This one is none of those.

    Neuwelt et al., PMID 6796658. SPECIES: DOG. n=33.
    Percutaneous vertebral-artery catheter, hypertonic mannitol, posterior fossa.

        methotrexate via vertebral artery ALONE          100 - 300 ng/g brain tissue
        same dose AFTER osmotic BBB disruption         1,100 - 5,000 ng/g brain tissue

    A MEASURED GAIN OF ROUGHLY 3.7x AT THE CONSERVATIVE END AND UP TO 50x AT THE OPTIMISTIC ONE,
    IN THE RIGHT SPECIES, IN VIVO, WITH TISSUE CONCENTRATIONS RATHER THAN A RATIO INFERRED FROM PK.

    Corroborated: PMID 6809316 (dog, 25% mannitol into the internal carotid; methotrexate levels
    significantly higher than controls, with a human phase I in the same paper), and PMID 24932854
    (modern canine feasibility -- vitals, bloods, neurologic status and major-artery patency stable
    through one month after mannitol-induced transient opening).

WHY IT MATTERS MORE THAN ANY PHARMACOLOGICAL FIX CONSIDERED HERE

  - IT NEEDS NO TRANSPORTER INHIBITOR. The previous regimen's single point of failure was a
    P-gp/BCRP co-dose with no canine protocol. This removes that dependency rather than routing
    around it.
  - THE EFFECT SIZE IS MEASURED IN DOGS. Every competing access number in this project is rodent,
    human, or modelled. This is the only one that is neither.
  - IT IS TERRITORY-SELECTIVE, which suits a focal intracranial mass -- and unlike focused
    ultrasound's sub-millimetric spot, an arterial territory is a volume.
  - THE MAGNITUDE DWARFS THE ALTERNATIVES. 3.7x to 50x against a pharmacological 20x that was
    measured in a mouse, with a different drug, and needs a co-dose nobody has given a dog.

WHAT IT COSTS: interventional catheter capability and general anaesthesia per dose. That is a real
constraint and it is a different KIND of constraint from "the drug does not exist".

THE COMPUTED RESULT

Backbone a dog can be given -- radiation, liposomal clodronate, hydroxychloroquine, anti-PD-1 -- plus
temozolomide and paxalisib delivered intra-arterially after osmotic disruption:

    disruption gain     worst margin at a SEVEN-DAY doubling
        x3.7  (conservative end of the measured canine range)      +0.0299   CLOSES
        x11   (midpoint)                                           +0.0614   CLOSES
        x20                                                        +0.0614   CLOSES

AT THE CONSERVATIVE END OF A MEASURED CANINE RANGE, ALL TEN ESCAPES CLOSE IN BOTH COMPARTMENTS AT A
SEVEN-DAY DOUBLING TIME -- a faster tumour than this project has assumed anywhere, and the growth
rate that broke every previous regimen.

AND A SEPARATE FINDING THAT MAKES THE WHOLE PROJECT LESS PESSIMISTIC

    PMID 34974334. Nineteen drugs, twelve of them P-gp substrates, measured head-to-head in MOUSE,
    CYNOMOLGUS MONKEY and BEAGLE DOG.

        Kp,brain in DOG and MONKEY was MORE THAN THREE-FOLD HIGHER THAN MOUSE for 7 of 12 P-gp
        substrates, with the same direction for unbound ratios. Dog and monkey agreed with each
        other. THE RODENT WAS THE OUTLIER.

        P-gp expression at the blood-brain barrier is roughly THREE-FOLD HIGHER in rat and pig than
        in dog, non-human primate or human.

THIS PROJECT'S 0.021 AND 0.027 ARE RODENT-DERIVED. If the canine correction applies, parenchymal
access for a P-gp substrate is nearer 0.06 than 0.02, and this analysis has been systematically
too pessimistic about every small molecule it foreclosed. That does not rescue any specific agent --
the potencies are still unmeasured -- but it means the barrier was modelled from the species that
has the most of it.

    ONE CAVEAT THAT CUTS THE OTHER WAY: the same work reports canine P-gp contributing to the
    blood-BRAIN barrier but NOT the blood-CSF barrier. So a CSF:plasma ratio OVERSTATES parenchymal
    exposure in a dog, and temozolomide's 0.20 is a CSF figure. The two corrections partly cancel.

WHAT WAS REJECTED, ON EVIDENCE

    marizomib          Genuinely crosses -- 30% of blood in rat, and brain proteasome inhibition
                       confirmed in cynomolgus monkey. But PHASE 3 NEGATIVE in glioblastoma (OS 16.5
                       vs 17.0 months, HR 1.04, n=749, PMID 38502052), and its dose-limiting
                       toxicities are ATAXIA AND HALLUCINATION -- which in a dog are unreportable,
                       unmonitorable, and clinically indistinguishable from tumour progression.
                       Development effectively stopped.
    disulfiram/copper  Mechanism is NPL4, not ALDH (PMID 31391554), and plausibly not division-gated.
                       But the one RANDOMISED trial in recurrent glioblastoma showed NO survival
                       benefit and SIGNIFICANTLY INCREASED TOXICITY (PMID 37000452). No measured
                       brain ratio exists in any species. Copper storage hepatopathy is a real canine
                       liability.
    ANG1005            LRP1 transcytosis is real and measured -- brain influx 86-fold above free
                       paclitaxel (PMID 19774344). But the phase II in recurrent glioma returned ORR
                       5.8% and PFS 1.4 months, the authors state no further glioma studies are
                       planned (PMID 39713041), and the phase 3 is dormant. THE DELIVERY WORKED AND
                       THE DRUG DID NOT, which is the cleanest available demonstration that
                       BRAIN-PENETRANT IS NOT BRAIN-EFFECTIVE.

WHAT IS STILL ASSUMED

  * The potencies. Still unmeasured, still the deciding numbers.
  * That mannitol disruption in the POSTERIOR FOSSA (where the canine measurement was made)
    transfers to a supratentorial territory.
  * That a 1981 measurement of METHOTREXATE transfers to temozolomide and paxalisib. It is a
    property of the BARRIER rather than of the drug, which is the argument for transfer -- but this
    project has been wrong about exactly that kind of transfer before.
  * That the tumour's arterial supply is catheterisable and identifiable, which is a radiological
    question about this specific dog.
"""

from __future__ import annotations

from .catalogue import ESCAPES, GROWTH_PER_DAY, LEPTOMENINGEAL, PARENCHYMA, agents_in
from .dormancy import DormancyModel
from .regimen import Agent, Axis, Layer, Regimen

# Neuwelt, PMID 6796658, n=33 DOGS. ng/g brain tissue.
WITHOUT_DISRUPTION = (100, 300)
WITH_DISRUPTION = (1100, 5000)
CONSERVATIVE_GAIN = WITH_DISRUPTION[0] / WITHOUT_DISRUPTION[1]   # 1100/300 = 3.7x
OPTIMISTIC_GAIN = WITH_DISRUPTION[1] / WITHOUT_DISRUPTION[0]     # 5000/100 = 50x

# Measured intrinsic access, before any disruption
PAXALISIB_KPUU = 0.31          # PMID 27638506, mouse. CONFIRMED NON-SUBSTRATE of P-gp and BCRP.
TEMOZOLOMIDE_CSF_PLASMA = 0.20  # PMID 15173079, human, malignant glioma
REFERENCE_POTENCY = 0.15


def backbone(compartment: str) -> list:
    p = {a.name: a for a in agents_in(compartment)}
    return [p["radiation"], p["liposomal clodronate"], p["hydroxychloroquine (autophagy)"],
            p["anti-PD-1 (gilvetmab)"]]


def build(compartment: str, disruption_gain: float = 1.0,
          potency: float = REFERENCE_POTENCY) -> Regimen:
    """Backbone plus two agents with MEASURED intrinsic access, optionally delivered after
    osmotic disruption."""
    return Regimen("intra-arterial + osmotic disruption", backbone(compartment) + [
        Agent("temozolomide", Axis.CYTOTOXIC, Layer.RECEPTOR, potency,
              min(TEMOZOLOMIDE_CSF_PLASMA * disruption_gain, 0.95), 1.0, True,
              note="CSF:plasma ~0.20 measured in human glioma (PMID 15173079). A WEAK dual P-gp/"
                   "BCRP substrate -- full double knockout gains only 1.5x -- so it works unassisted."),
        Agent("paxalisib", Axis.PI3K_PARALLEL, Layer.RECEPTOR, potency,
              min(PAXALISIB_KPUU * disruption_gain, 0.95), 1.0, True,
              note="Kp,uu 0.31 and a CONFIRMED NON-SUBSTRATE of P-gp and BCRP (PMID 27638506). "
                   "Access by design rather than by margin."),
    ])


def worst_margin(compartment: str, disruption_gain: float = 1.0,
                 growth: float = GROWTH_PER_DAY, potency: float = REFERENCE_POTENCY) -> float:
    r = build(compartment, disruption_gain, potency)
    d = DormancyModel()
    return min(d.margin(r, e, growth) if "persister" in e.name
               else r.effective_kill_against(e) - growth for e in ESCAPES)


def closes(disruption_gain: float = 1.0, growth: float = GROWTH_PER_DAY,
           potency: float = REFERENCE_POTENCY) -> bool:
    return all(worst_margin(c, disruption_gain, growth, potency) > 0
               for c in (PARENCHYMA, LEPTOMENINGEAL))


NEUWELT_1981 = {
    "citation": "PMID 6796658. SPECIES: DOG. n=33. Percutaneous vertebral-artery catheter, "
                "hypertonic mannitol, posterior fossa.",
    "methotrexate_without_disruption_ng_per_g": WITHOUT_DISRUPTION,
    "methotrexate_with_disruption_ng_per_g": WITH_DISRUPTION,
    "conservative_gain": round(CONSERVATIVE_GAIN, 1),
    "optimistic_gain": round(OPTIMISTIC_GAIN, 1),
    "why_it_is_the_strongest_number_here": "TISSUE CONCENTRATIONS, IN VIVO, IN THE RIGHT SPECIES. "
        "Every competing access figure in this project is rodent, human, or modelled.",
    "corroboration": "PMID 6809316 (dog, internal carotid, 25% mannitol) and PMID 24932854 (modern "
                     "canine feasibility -- stable through one month).",
}

# disruption gain -> worst margin at a SEVEN-DAY doubling
RESULT_AT_SEVEN_DAY_DOUBLING = {3.7: 0.0299, 11.0: 0.0614, 20.0: 0.0614}

WHY_IT_BEATS_THE_PHARMACOLOGICAL_FIX = (
    "IT NEEDS NO TRANSPORTER INHIBITOR. The previous regimen's single point of failure was a "
    "P-gp/BCRP co-dose with no canine protocol. This removes the dependency rather than routing "
    "around it.",
    "THE EFFECT SIZE IS MEASURED IN DOGS. Every competing access number here is rodent, human or "
    "modelled.",
    "IT IS TERRITORY-SELECTIVE, which suits a focal mass -- and unlike focused ultrasound's "
    "sub-millimetric spot, an arterial territory is a VOLUME.",
    "THE MAGNITUDE DWARFS THE ALTERNATIVES: 3.7x to 50x measured in dogs, against a pharmacological "
    "20x measured in a mouse with a different drug.",
)

WHAT_IT_COSTS = ("Interventional catheter capability and general anaesthesia per dose. That is a "
                 "real constraint, and it is a different KIND of constraint from 'the drug does not "
                 "exist'.")

THE_SPECIES_CORRECTION = {
    "citation": "PMID 34974334. Nineteen drugs, twelve of them P-gp substrates, head-to-head in "
                "MOUSE, CYNOMOLGUS MONKEY and BEAGLE DOG.",
    "finding": "Kp,brain in DOG and MONKEY was MORE THAN THREE-FOLD HIGHER THAN MOUSE for 7 of 12 "
               "P-gp substrates. Dog and monkey agreed with each other. THE RODENT WAS THE OUTLIER.",
    "and_the_mechanism": "P-gp expression at the blood-brain barrier is roughly THREE-FOLD HIGHER in "
                         "rat and pig than in dog, non-human primate or human.",
    "WHAT_IT_MEANS_HERE": "This project's 0.021 and 0.027 are RODENT-DERIVED. Under the canine "
        "correction, parenchymal access for a P-gp substrate is nearer 0.06 than 0.02, and this "
        "analysis has been SYSTEMATICALLY TOO PESSIMISTIC about every small molecule it foreclosed. "
        "It does not rescue any specific agent -- the potencies are still unmeasured -- but the "
        "barrier was modelled from the species that has the most of it.",
    "THE_CAVEAT_THAT_CUTS_BACK": "The same work reports canine P-gp contributing to the blood-BRAIN "
        "barrier but NOT the blood-CSF barrier. So a CSF:plasma ratio OVERSTATES parenchymal "
        "exposure in a dog -- and temozolomide's 0.20 is a CSF figure. The two corrections partly "
        "cancel.",
}

REJECTED_ON_EVIDENCE = {
    "marizomib": "Genuinely crosses -- 30% of blood in rat, brain proteasome inhibition confirmed in "
        "cynomolgus monkey. But PHASE 3 NEGATIVE in glioblastoma (OS 16.5 vs 17.0 months, HR 1.04, "
        "n=749, PMID 38502052), and its dose-limiting toxicities are ATAXIA AND HALLUCINATION -- "
        "which in a dog are unreportable, unmonitorable, and clinically indistinguishable from "
        "tumour progression.",
    "disulfiram + copper": "Mechanism is NPL4, not ALDH (PMID 31391554), and plausibly not "
        "division-gated. But the one RANDOMISED trial in recurrent glioblastoma showed NO survival "
        "benefit and SIGNIFICANTLY INCREASED TOXICITY (PMID 37000452). No measured brain ratio in "
        "any species. Copper storage hepatopathy is a real canine liability.",
    "ANG1005": "LRP1 transcytosis is real and measured -- brain influx 86-fold above free paclitaxel "
        "(PMID 19774344). But phase II in recurrent glioma returned ORR 5.8%, PFS 1.4 months, no "
        "further glioma studies planned (PMID 39713041), and the phase 3 is dormant. THE DELIVERY "
        "WORKED AND THE DRUG DID NOT -- the cleanest available demonstration that BRAIN-PENETRANT IS "
        "NOT BRAIN-EFFECTIVE.",
}

WHAT_IS_STILL_ASSUMED = (
    "The potencies. Still unmeasured, still the deciding numbers.",
    "That mannitol disruption in the POSTERIOR FOSSA, where the canine measurement was made, "
    "transfers to a supratentorial territory.",
    "That a 1981 measurement of METHOTREXATE transfers to temozolomide and paxalisib. It is a "
    "property of the BARRIER rather than of the drug, which is the argument for transfer -- but this "
    "project has been wrong about exactly that kind of transfer before.",
    "That the tumour's arterial supply is catheterisable and identifiable, which is a radiological "
    "question about this specific dog.",
)
