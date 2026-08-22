"""[SUPERSEDED HEADLINE — AUDIT BANNER] The temozolomide + intra-arterial regimen headlined here was
retracted by core.schedule_coherence. build() still constructs the impossible access*duty temozolomide
object and closes() still self-reports True in isolation, but the live chain consumes ONLY the three
coherent backbone agents (liposomal clodronate, hydroxychloroquine, anti-PD-1) via a filter and drops
the rest. Live answer: core.breed_wide_durability.

The answer, assembled under the toxicity gate rather than by hand.

WHY THIS MODULE HAD TO EXIST

The published plain-language report quoted margins of +0.056 (parenchyma) and +0.073
(leptomeninges). Those numbers were real, and they were produced by an AD-HOC COMPUTATION IN A
SHELL -- `intraarterial_route.build()` minus radiation, assembled by hand at the moment of writing.
No committed code path produced them, no test re-derived them, and the reason radiation was absent
lived in the report's prose rather than in the model.

That is the same defect this project has now made four times in four different places:

    coverage    asserted in prose      -> fixed by `regimen.Agent.covers`
    provenance  asserted in prose      -> fixed by `evidence.Measurement.value_for`
    seizure     asserted in prose      -> fixed by `Organ.SEIZURE` (see below)
    the ANSWER  assembled in a shell   -> fixed here

A headline figure that no test can re-derive is a headline figure that will drift.

WHAT THE TOXICITY GATE ACTUALLY DECIDES

Radiation is not hand-removed here. It is offered to the gate along with everything else and the
gate rejects it, because `toxicity` now carries a SEIZURE axis that both brain irradiation and
osmotic barrier disruption load:

    with radiation       seizure axis 1.15   OVERSUBSCRIBED   -> rejected
    without radiation    seizure axis 0.60   inside budget    -> accepted

Before that axis existed, radiation sat on CNS_LOCAL and osmotic disruption on PROCEDURAL, so the
two could never add, and the model would have called the radiation-containing stack tolerable. The
collision was written in the profile's `source` string -- a sentence the arithmetic could not read.

THE CONSTRAINT THAT ACTUALLY BINDS, AND THE REPORT UNDERSTATED IT

    myelosuppression   1.00   temozolomide 0.55 + hydroxychloroquine 0.45

Headroom is 0.00. Not "roughly a third unspent" -- that claim was wrong, and it was wrong in the
optimistic direction. The marrow axis is pinned exactly at its ceiling by two agents that are both
load-bearing: temozolomide is the only agent with intrinsic CNS access carrying kill against every
pathway escape, and hydroxychloroquine is the only agent closing autophagy-independence. Neither can
be dropped to buy margin, so ANY adverse variance in either -- a dog that myelosuppresses harder
than the reference, a concurrent infection, cumulative dosing -- forces a de-rate, and `toxicity
.derated_potency` says a de-rate costs kill proportionally.

WHERE IT BREAKS

At the assumed 12.6-day doubling both compartments close. At a seven-day doubling both still close.
AT A FIVE-DAY DOUBLING BOTH COMPARTMENTS REOPEN -- not just the parenchymal one. The report said
only the brain-tissue site reopened, which understated it.
"""

from __future__ import annotations

from . import intraarterial_route as ia
from . import toxicity as tox
from .catalogue import ESCAPES, GROWTH_PER_DAY, LEPTOMENINGEAL, PARENCHYMA
from .dormancy import DormancyModel
from .regimen import Regimen

#: The procedure is not an `Agent` -- it carries no kill of its own -- but it does carry toxicity,
#: so it has to be priced even though it never appears in the kill arithmetic.
PROCEDURE = "intra-arterial + osmotic disruption"

REFERENCE_POTENCY = 0.15


def candidates(compartment: str) -> list:
    """Everything on offer, radiation included. The gate decides, not this function."""
    return list(ia.build(compartment, ia.CONSERVATIVE_GAIN).agents)


def toxicity_rejects(agents) -> tuple:
    """Agents that must be dropped for the stack to fit inside every organ budget.

    Greedy by budget cost: repeatedly drop the agent whose removal relieves the most oversubscribed
    axis, until nothing is oversubscribed. Returns the dropped names in the order dropped.
    """
    kept = [a.name for a in agents]
    dropped: list = []
    while True:
        profiles = [tox.PROFILES[n] for n in kept + [PROCEDURE]]
        over = tox.oversubscribed(profiles)
        if not over:
            return tuple(dropped)
        worst_axis = max(over, key=over.get)
        # The procedure itself is not droppable -- it is the delivery route the whole result rests
        # on. Drop the agent carrying the most load on the offending axis.
        on_axis = [n for n in kept if worst_axis in tox.PROFILES[n].load()]
        if not on_axis:
            return tuple(dropped)
        victim = max(on_axis, key=lambda n: tox.PROFILES[n].load()[worst_axis])
        kept.remove(victim)
        dropped.append(victim)


def build(compartment: str) -> Regimen:
    """The regimen that survives the toxicity gate."""
    offered = candidates(compartment)
    rejected = set(toxicity_rejects(offered))
    return Regimen("durable (toxicity-gated)", [a for a in offered if a.name not in rejected])


def margins(compartment: str, growth: float = GROWTH_PER_DAY) -> dict:
    """Per-escape margin. Persisters are priced through the dormancy model, everything else
    directly, because a dormant cell is not growing either."""
    r = build(compartment)
    d = DormancyModel()
    return {e.name: (d.margin(r, e, growth) if "persister" in e.name
                     else r.effective_kill_against(e) - growth) for e in ESCAPES}


def worst_margin(compartment: str, growth: float = GROWTH_PER_DAY) -> float:
    return min(margins(compartment, growth).values())


def closes(growth: float = GROWTH_PER_DAY) -> bool:
    return all(worst_margin(c, growth) > 0 for c in (PARENCHYMA, LEPTOMENINGEAL))


def worst_margin_for_subset(compartment: str, names, growth: float = GROWTH_PER_DAY) -> float:
    """Worst margin using only the named agents. This is how load-bearing is measured."""
    kept = [a for a in build(compartment).agents if a.name in set(names)]
    r = Regimen("subset", kept)
    d = DormancyModel()
    return min(d.margin(r, e, growth) if "persister" in e.name
               else r.effective_kill_against(e) - growth for e in ESCAPES)


def load_bearing(compartment: str, growth: float = GROWTH_PER_DAY) -> tuple:
    """Agents whose removal reopens at least one escape.

    Ran on the five-agent regimen this returns exactly ONE name. That is the finding the published
    report missed: the other four are not carrying the result.
    """
    full = build(compartment)
    out = []
    for a in full.agents:
        rest = tuple(b.name for b in full.agents if b.name != a.name)
        if worst_margin_for_subset(compartment, rest, growth) <= 0:
            out.append(a.name)
    return tuple(out)


def organ_loads(compartment: str = PARENCHYMA) -> dict:
    names = [a.name for a in build(compartment).agents] + [PROCEDURE]
    return {axis.value: round(load, 2)
            for axis, load in tox.axis_loads([tox.PROFILES[n] for n in names]).items()}


def headroom(compartment: str = PARENCHYMA) -> float:
    names = [a.name for a in build(compartment).agents] + [PROCEDURE]
    return tox.headroom([tox.PROFILES[n] for n in names])


# --- computed results, re-derived by the tests rather than transcribed ------------------------------

#: doubling time (days) -> (parenchyma worst margin, leptomeningeal worst margin)
BY_DOUBLING_TIME = {12.6: (0.0556, 0.0732), 10.0: (0.0413, 0.0589), 7.0: (0.0116, 0.0292),
                    5.0: (-0.0280, -0.0104), 4.0: (-0.0626, -0.0450)}

WHY_RADIATION_IS_ABSENT = {
    "it_is_not_hand_removed": "It is offered to the gate with everything else and REJECTED, because "
        "brain irradiation and osmotic disruption both load Organ.SEIZURE.",
    "with_radiation": "seizure axis 1.15 -- OVERSUBSCRIBED",
    "without_radiation": "seizure axis 0.60 -- inside budget",
    "what_changed_in_the_model": "Before Organ.SEIZURE existed, radiation sat on CNS_LOCAL and "
        "osmotic disruption on PROCEDURAL, so they could never add and the model called the "
        "radiation-containing stack TOLERABLE. The collision lived in a `source` string.",
    "why_it_costs_nothing": "Radiation was in earlier regimens SOLELY to get treatment into the "
        "brain. Intra-arterial delivery does that job directly, so removing radiation removes a "
        "component whose reason had already expired.",
}

THE_SINGLE_POINT_OF_FAILURE = {
    "what_it_is": "TEMOZOLOMIDE, DELIVERED INTRA-ARTERIALLY AFTER OSMOTIC DISRUPTION. Nothing else "
        "in the regimen is carrying the result.",
    "the_report_was_wrong": "The published report said 'Five components. Each is there because it "
        "closes something nothing else in the list closes.' FALSE. Drop any agent except "
        "temozolomide and all ten escapes still close at both sites.",
    "temozolomide_alone": "+0.0550 at BOTH compartments -- every escape closed.",
    "what_the_other_four_buy": "+0.0006 in the parenchyma and +0.0182 in the leptomeninges. In the "
        "parenchyma that is roughly ONE PERCENT of the margin.",
    "anti_PD_1_is_decoration": "Its effective kill in the parenchyma is 0.00002/day -- more than "
        "three orders of magnitude below the growth rate, because an antibody does not cross. It "
        "costs 30% of an immune toxicity axis and buys effectively nothing. NOT exactly zero: a "
        "four-decimal readout showed its rows unchanged and was briefly read as 'literally "
        "nothing', which was the READOUT rounding, not the agent.",
    "paxalisib_is_not_redundant_but_is_not_load_bearing": "It carries 0.1425/day, but only against "
        "the ONE escape on its axis -- and temozolomide already closes that escape, being "
        "position-independent. It widens a margin that was already positive.",
    "WHY_THIS_MATTERS": "`brain_native_regimen` rejected the previous answer FOR HAVING A SINGLE "
        "POINT OF FAILURE -- an efflux co-dose nobody had given a dog. That objection was correct "
        "and the fix did not eliminate the property, IT MOVED IT. The result now rests on two "
        "numbers: temozolomide's potency (0.15/day, UNMEASURED in this disease) and the 3.7x "
        "osmotic gain (measured in dogs, 1981, with a different drug).",
    "the_delivery_gain_is_the_other_half": "Without it, temozolomide's kill is 0.15 x 0.20 = "
        "0.030/day against growth of 0.055. IT FAILS. Access is not a contributor to this result, "
        "it IS the result.",
}

THE_FREE_TRADE = {
    "what": "DROP HYDROXYCHLOROQUINE. Headroom goes from 0.00 to 0.40 for a worst-margin cost of "
        "0.00002/day in the parenchyma and 0.00021/day in the leptomeninges.",
    "what_the_cost_actually_is": "NOT zero. With hydroxychloroquine gone the WEAKEST LINK MOVES "
        "from autophagy-independence to ANTIGEN LOSS, which hydroxychloroquine did cover. The cost "
        "is the size of that shift, and it is the same order as anti-PD-1's entire contribution.",
    "why_it_is_free_and_it_is_STRUCTURAL": "The binding escape is AUTOPHAGY-INDEPENDENCE, and "
        "hydroxychloroquine is the autophagy agent. `regimen.Agent.covers` refuses an agent against "
        "an escape ON ITS OWN AXIS -- removing autophagy dependence defeats an autophagy blocker "
        "exactly as CSF1R-independence defeats a CSF1R inhibitor. So hydroxychloroquine is "
        "STRUCTURALLY INCAPABLE of helping the weakest link, while carrying 45% of the axis that "
        "binds the whole regimen.",
    "what_it_costs": "0.0021/day of kill against the nine escapes it does cover, none of which are "
        "the binding one.",
    "the_general_lesson": "An agent can be simultaneously the reason a constraint binds and "
        "incapable of relieving the escape that constraint is protecting against. Nothing flags "
        "that except computing coverage and toxicity in the same place.",
}

THE_BINDING_CONSTRAINT = {
    "axis": "myelosuppression",
    "load": 1.00,
    "headroom": 0.00,
    "carried_by": ("temozolomide 0.55", "hydroxychloroquine (autophagy) 0.45"),
    "THE_REPORT_WAS_WRONG": "The published report said 'roughly a third of the total budget "
        "unspent'. THE TIGHTEST AXIS HAS ZERO HEADROOM. The error was in the optimistic direction.",
    "why_neither_can_be_dropped": "Temozolomide is the only agent with intrinsic CNS access carrying "
        "kill against every pathway escape; hydroxychloroquine is the only agent closing "
        "autophagy-independence. Dropping either reopens escapes.",
    "consequence": "Any adverse variance forces a de-rate, and `toxicity.derated_potency` prices a "
        "de-rate as a proportional loss of kill. The margins here assume FULL dose in both.",
}

WHAT_THIS_MODULE_FIXES = (
    "The published margins were produced by an AD-HOC SHELL COMPUTATION -- "
    "`intraarterial_route.build()` minus radiation, assembled by hand. No committed code path "
    "produced them and no test re-derived them.",
    "The reason radiation was absent lived in the REPORT'S PROSE rather than in the model, so the "
    "model would still have called the radiation-containing stack tolerable.",
    "A headline figure that no test can re-derive is a headline figure that will drift. This "
    "project has now made that mistake for coverage, for provenance, for seizure risk, and for the "
    "answer itself.",
)

WHAT_IS_STILL_ASSUMED = (
    "The reference potency, 0.15/day, for every agent here. UNMEASURED in canine histiocytic "
    "sarcoma, and it is the deciding number.",
    "The growth rate. Every row of BY_DOUBLING_TIME is indexed on it, and the sign flips between a "
    "seven-day and a five-day doubling.",
    "That the 3.7x osmotic-disruption gain measured with methotrexate at the posterior fossa in 1981 "
    "transfers to these agents at this location. It is a property of the BARRIER rather than of the "
    "drug, which is the argument -- and this project has been wrong about exactly that kind of "
    "transfer before.",
    "That the budget fractions in `toxicity` are the right sizes. They are ordinal judgements, not "
    "measurements, and the marrow axis landing at EXACTLY 1.00 is an artefact of two round numbers "
    "rather than a measured ceiling.",
)
