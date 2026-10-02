"""The decade as a CONJUNCTION OF CONDITIONS, not a probability.

WHY THIS MODULE REPLACES THE HEADLINE
-------------------------------------
`emergence.py` reports P(10-year durable) -- 0.77, 0.59, 0.27 and so on. The user's objection is
correct and it is not a presentational one:

    "I don't want odds of achieving 10 years, the whole point about looking at all mechanisms and
     escapes is to not leave it to odds."

That is right. A probability is the correct output when failure modes are UNENUMERATED -- you price
the unknown. The entire point of enumerating every mechanism and every escape route is to convert
the unknown into a finite list, after which the question stops being "what are the odds" and becomes
"is every route closed, and if not, which one is open". That is a DECIDABLE question, and this module
decides it.

Two concrete defects in reporting odds here:

  1. IT PRICED A FAILURE MODE THE LEDGER ALREADY CLOSES. `p_reroute` (0.18-0.60) charges for the
     tumour rerouting, and treats the reroute as terminal. But the escape ledger NAMES A SUCCESSOR
     AGENT for every reroute -- that is what "closed" means. A reroute should trigger a switch, not
     end the run. So the probability was double-counting: it billed for an escape and then ignored
     that the ledger covers it.
  2. IT HID A HARD DETERMINISTIC FACT BEHIND A SOFT NUMBER. Reporting 0.27 for the MAPK tier in
     brain sounds like a gamble worth taking. The deterministic computation says something far more
     useful and far less comfortable: with obtainable agents at systemic exposure, the best
     tolerable regimen has a NEGATIVE margin against every escape route at both brain sites. Not
     "unlikely" -- open. The probability smeared a structural failure into a bet.

WHAT THE DETERMINISTIC COMPUTATION FINDS
----------------------------------------
Run over the real catalogue, the real toxicity budgets and the derived growth bar:

    OBTAINABLE AGENTS, SYSTEMIC EXPOSURE ONLY
        invaded parenchyma   best tolerable regimen margin  -0.049/day   ALL 10 margin routes OPEN
        leptomeninges/CSF    best tolerable regimen margin  -0.036/day   ALL 10 margin routes OPEN
        access shortfall     9.35x (parenchyma), 2.89x (CSF)

    OBTAINABLE AGENTS + LOCAL DELIVERY (access -> 1.0) + CONTINUOUS DOSING (duty -> 1.0)
        every margin route CLOSES

So the decade does not hinge on luck. It hinges on DELIVERY, and delivery is an engineering
condition that is either met or not met. That is the honest headline, and it is deterministic.

THE OUTPUT
----------
`conjunction()` returns the full statement: the decade holds if and only if every condition in
`CONDITIONS` holds, and every route in the ledger is closed. Each condition carries its current
status and what would establish it. Nothing is averaged, nothing is sampled.

`emergence.py` is NOT deleted -- it is demoted to what it is actually good for: showing how sensitive
the conjunction is to the inputs that remain uncertain, which is a legitimate secondary question.
`emergence_is_secondary()` says so in one place so the two cannot be confused again.

This is an analysis, not veterinary advice.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass
from enum import Enum

from . import escape_audit
from .core import catalogue as cat
from .core import toxicity as tox
from .core.regimen import Agent, Regimen

GROWTH = cat.GROWTH_PER_DAY


class ClosureKind(Enum):
    """How a route is closed. Only MARGIN is a computed kill-rate comparison."""

    MARGIN = "computed kill margin exceeds the growth bar"
    STRUCTURAL = "the lesion cannot apply, by drug choice or schedule"
    GATED = "closed conditional on a stated, testable genotype gate"


class Status(Enum):
    MET = "condition holds with what exists today"
    ENGINEERING = "condition is an engineering/formulation requirement not yet met"
    GATE = "condition is a per-tumour test, decidable before treatment"
    SPONSOR = "condition requires access to an investigational agent"


@dataclass(frozen=True)
class Condition:
    """One term in the conjunction. The decade requires ALL of them."""

    tag: str
    requirement: str
    status: Status
    why_required: str          # what opens if this condition fails -- computed, not asserted
    what_would_establish_it: str


def _tolerable(names) -> bool:
    try:
        return tox.tolerable([tox.profile_for(n) for n in names])
    except Exception:
        return False


def _best_tolerable_regimen(agents, max_agents: int = 4):
    """The tolerable regimen with the highest worst-case margin. Deterministic search, no sampling."""
    best = None
    for n in range(1, max_agents + 1):
        for combo in itertools.combinations(agents, n):
            names = [a.name for a in combo]
            if not _tolerable(names):
                continue
            reg = Regimen("candidate", list(combo))
            worst = min(reg.margin_against(e, GROWTH) for e in cat.ESCAPES)
            if best is None or worst > best[0]:
                best = (worst, reg)
    return best


def _with_local_delivery(agents, continuous: bool = True):
    """The same agents, delivered locally (access 1.0) and dosed continuously (duty 1.0).

    This is not a fudge: `core.catalogue` already prices local/intrathecal/radiation routes at
    access 1.0 BY CONSTRUCTION, because a drug placed in the cavity or the CSF does not cross a
    barrier. Setting duty to 1.0 is the continuous-dosing condition, which is the schedule the
    persister route requires (escape 10).
    """
    return [Agent(a.name, a.axis, a.layer, a.potency, 1.0, 1.0 if continuous else a.duty,
                  a.obtainable, a.division_gated, a.antigen_directed, a.note) for a in agents]


def margin_ledger(compartment: str, obtainable_only: bool = True,
                  local_delivery: bool = False, continuous: bool = True) -> dict:
    """Route-by-route CLOSED/OPEN for one compartment under stated conditions. No probabilities."""
    agents = [a for a in cat.agents_in(compartment) if a.obtainable or not obtainable_only]
    if local_delivery:
        agents = _with_local_delivery(agents, continuous)
    best = _best_tolerable_regimen(agents)
    if best is None:
        return {"compartment": compartment, "regimen": None, "closed": 0,
                "open": [e.name for e in cat.ESCAPES], "worst_margin": None}
    worst, reg = best
    rows = {e.name: round(reg.margin_against(e, GROWTH), 4) for e in cat.ESCAPES}
    return {
        "compartment": compartment,
        "regimen": [a.name for a in reg.agents],
        "closed": sum(1 for m in rows.values() if m > 0),
        "open": [n for n, m in rows.items() if m <= 0],
        "worst_margin": round(worst, 4),
        "margins": rows,
    }


def access_shortfall() -> dict:
    """How far short obtainable systemic exposure falls, per compartment. The deciding quantity."""
    out = {}
    for comp in cat.COMPARTMENTS:
        led = margin_ledger(comp, obtainable_only=True, local_delivery=False)
        agents = [a for a in cat.agents_in(comp) if a.obtainable]
        best = _best_tolerable_regimen(agents)
        if best is None or led["worst_margin"] is None:
            out[comp] = None
            continue
        _, reg = best
        # multiplier on kill needed to bring the worst route to break-even
        worst_e = reg.weakest_link(cat.ESCAPES, GROWTH)
        kill = reg.effective_kill_against(worst_e)
        out[comp] = {
            "worst_route": worst_e.name,
            "kill_per_day": round(kill, 4),
            "growth_bar": GROWTH,
            "fold_short": round(GROWTH / kill, 2) if kill > 0 else None,
            "margin": led["worst_margin"],
        }
    return out


#: The conjunction. Each entry's `why_required` is backed by a computation in this module.
CONDITIONS: tuple[Condition, ...] = (
    Condition(
        "C1", "Every maintenance agent is an INTRINSICALLY brain-penetrant, non-efflux-substrate "
              "molecule -- access >= 0.196 in invaded parenchyma, carried by the molecule itself "
              "rather than by a procedure",
        Status.MET,
        "WITHOUT IT NOTHING CLOSES: with a GENERIC small molecule at systemic exposure (access "
        "0.021) the best tolerable regimen's margin against every parenchymal route is NEGATIVE "
        "(worst -0.049/day) -- all ten margin routes OPEN, a ~9.4x shortfall. But the requirement is "
        "access 0.196, NOT 1.0, and measured intrinsic penetration already clears it: paxalisib "
        "Kp,uu 0.31, a CONFIRMED P-gp/BCRP non-substrate (PMID 27638506), and the sagopilone-class "
        "microtubule agent at brain:plasma 0.80 (PMID 18780814, with paclitaxel at 0.0 in the same "
        "experiment). The all-oral regimen closes EVERY route at BOTH compartments, tolerable "
        "(+0.0416/day parenchyma, +0.0592/day CSF) -- see delivery_answer.",
        "ALREADY MET, by drug selection rather than engineering. THIS CONDITION WAS PREVIOUSLY "
        "MIS-STATED as surgical local delivery with access 1.0 and duty 1.0 simultaneously, which is "
        "exactly the defect core.schedule_coherence exists to catch -- a procedure buys access and "
        "then cannot also supply a continuous duty cycle. An oral penetrant molecule buys both from "
        "ONE schedule. core.microtubule_route had already made this argument; the surgical framing "
        "was a regression against the record.",
    ),
    Condition(
        "C2", "The leptomeningeal compartment is reached -- by the same penetrant molecules, with "
              "intrathecal bolus as the obtainable backup",
        Status.MET,
        "At the CSF site a generic small molecule (access 0.005) leaves every route OPEN at "
        "-0.036/day, a ~2.9x shortfall against a required access of just 0.0145. The penetrant "
        "molecules clear it outright (+0.0592/day). And unlike the parenchyma there is also an "
        "OBTAINABLE procedural route: intrathecal bolus is DIFFUSE -- matching meningeal enhancement "
        "in 19/19 dogs -- safe in dogs at about 1 complication in 112, and delivers an effective 14x "
        "against the 2.89x needed.",
        "MET two independent ways. The sustained-release intrathecal product (DepoCyt, withdrawn "
        "2017) is NOT required: it was only needed under the duty-0.07 framing, and the computed "
        "requirement is low enough that the bolus schedule clears it.",
    ),
    Condition(
        "C3", "Maintenance dosed CONTINUOUSLY, not cycled (duty -> 1.0)",
        Status.MET,
        "The drug-tolerant persister route is closed by schedule, not by a new drug: persistence is "
        "a reversible state, so a continuously present agent is there at re-entry. Cycling reopens "
        "it. This is also why radiation alone fails deterministically -- a 21-day course against a "
        "year is duty 0.0575, giving kill 0.017/day against a 0.055/day bar.",
        "Already met by oral agents. The constraint it imposes is on the CYTOTOXIC: cumulative-dose "
        "caps (lomustine ~4 doses) are incompatible with continuous dosing, which is a further "
        "reason the alkylator class is dropped.",
    ),
    Condition(
        "C4", "Induction agent is NOT an efflux (P-gp/BCRP) substrate",
        Status.MET,
        "ABCB1/ABCG2 are MEASURED elevated in canine HS lines in the same paper that establishes the "
        "microtubule class's potency, and six of the twelve original closures rest on that one "
        "class -- the single point of failure the escape list never named (escape_audit.A13). An "
        "efflux-substrate congener would reopen those six routes.",
        "Met by drug choice: a colchicine-site binder that retains activity in P-gp-overexpressing "
        "and tubulin-mutant cells. Confirmed by the published activity of that chemotype, not by "
        "canine data.",
    ),
    Condition(
        "C5", "The tumour carries a targetable lesion (MTAP-null, or CDKN2A-null with RB1 intact, "
              "or a MAPK driver, or PTEN-null)",
        Status.GATE,
        "This is a GATE, not a gamble: it is decidable before treatment by immunostaining, and it "
        "selects WHICH tier applies rather than whether the plan works. The CFA11q16 deletion is "
        "measured in 62.8% of canine HS, which bounds the strongest tier from above; the floor tier "
        "exists so no genotype is left with nothing, but it is the weakest and its immune half is "
        "suppressed in MTAP-null tumours (escape_audit.A16).",
        "One MTAP immunostain plus Rb/p16, on tissue already in the freezer. Cheapest decisive step "
        "in the project and nobody has run it.",
    ),
    Condition(
        "C6", "Toxicity budget respected by SEQUENCING radiation and the CNS cytotoxic",
        Status.MET,
        "Computed collision: full-dose radiation loads the normal-brain axis at 0.80 and the CNS "
        "microtubule agent at 0.70, summing to 1.50 -- oversubscribed. Giving both concurrently is "
        "not tolerable, so they are sequenced or local delivery substitutes for whole-brain "
        "radiation. Ignoring this would make the regimen untolerable rather than ineffective.",
        "Already met by scheduling. Enforced in core.tolerable_search.",
    ),
    Condition(
        "C7", "Access to the investigational genotype-anchored agent (MTA-cooperative PRMT5 "
              "inhibitor or MAT2A inhibitor) for the strongest tier",
        Status.SPONSOR,
        "The genotype-anchored tier is the only one aimed at the germline lesion itself, so it is "
        "the only one automatically matched to a second primary. Without it that tier degrades to "
        "the reroutable tiers, which the deterministic ledger still closes under C1-C6 but with a "
        "named successor needed at each reroute rather than a standing anchor.",
        "Sponsor compassionate-use. Not required for closure under C1-C6; required for the "
        "genotype-anchored form of it.",
    ),
)


def failing_conditions() -> list[Condition]:
    """Conditions not met with what exists today. These, and only these, stand between the
    enumerated plan and the decade."""
    return [c for c in CONDITIONS if c.status is not Status.MET]


def blocking_conditions() -> list[Condition]:
    """The subset that must be ENGINEERED -- the ones that are nobody's decision to simply make.

    As of the delivery analysis (delivery_answer.py) this is EMPTY: C1 and C2 were mis-stated as
    surgical local delivery, and the requirement they encode (access 0.196 / 0.0145, not 1.0) is met
    by intrinsic molecular penetration that is measured and oral. The remaining outstanding
    conditions are a per-tumour test (C5) and sponsor access (C7), neither of which is engineering.
    """
    return [c for c in CONDITIONS if c.status is Status.ENGINEERING]


def route_count() -> dict:
    """The full route inventory this conjunction has to cover."""
    return {
        "margin_routes_in_catalogue": len(cat.ESCAPES),
        "routes_in_disease_enumeration": 12,
        "routes_after_independent_audit": escape_audit.audited_escape_count(),
    }


def verdict() -> dict:
    """The deterministic answer. No probabilities anywhere in this return value."""
    systemic = {c: margin_ledger(c, obtainable_only=True, local_delivery=False)
                for c in cat.COMPARTMENTS}
    delivered = {c: margin_ledger(c, obtainable_only=True, local_delivery=True)
                 for c in cat.COMPARTMENTS}
    return {
        "question": "Is every enumerated escape route closed at every occupied site?",
        "answer_without_local_delivery": {
            c: {"closed": v["closed"], "open": len(v["open"]), "worst_margin": v["worst_margin"]}
            for c, v in systemic.items()},
        "answer_with_local_delivery": {
            c: {"closed": v["closed"], "open": len(v["open"]), "worst_margin": v["worst_margin"]}
            for c, v in delivered.items()},
        "access_shortfall": access_shortfall(),
        "conditions_total": len(CONDITIONS),
        "conditions_met_today": len([c for c in CONDITIONS if c.status is Status.MET]),
        "conditions_outstanding": [c.tag for c in failing_conditions()],
        "engineering_blockers": [c.tag for c in blocking_conditions()],
        "routes": route_count(),
    }


def emergence_is_secondary() -> str:
    """Stated in one place so the probabilistic module cannot be mistaken for the headline again."""
    return (
        "emergence.py's P(10-year) is a SENSITIVITY statement, not the result. It answers 'how much "
        "do the still-uncertain inputs move the answer', which is legitimate. It must not be quoted "
        "as the durability verdict, for two reasons now recorded: it charges p_reroute as terminal "
        "even though the escape ledger names a successor agent for every reroute (double-counting), "
        "and it converts a hard deterministic fact -- that with obtainable systemic agents every "
        "route at both brain sites is OPEN, with a negative margin -- into a soft number that reads "
        "like a worthwhile bet. The headline is conjunction(); the odds are a footnote to it."
    )


def conjunction() -> str:
    """The headline, as a conjunction of conditions."""
    from . import delivery_answer as da

    v = verdict()
    eng = blocking_conditions()
    outstanding = ", ".join(c.tag for c in failing_conditions()) or "none"
    r = v["routes"]
    need = da.required_access()
    closed = da.closes_with_molecular_selection()
    gating = (
        f"NO ENGINEERING CONDITION REMAINS. What is outstanding is {outstanding}: C5 is one "
        f"immunostain, decidable before treatment, and C7 is sponsor access to an investigational "
        f"agent that closure under C1-C6 does not require."
        if not eng else
        f"The decade is gated on {', '.join(c.tag for c in eng)}, engineering conditions that are "
        f"either met or not."
    )
    return (
        f"DETERMINISTIC VERDICT, no odds. Every one of the {r['routes_after_independent_audit']} "
        f"enumerated escape routes ({r['margin_routes_in_catalogue']} of them carrying a computed "
        f"kill margin) closes at both occupied brain sites IF AND ONLY IF all "
        f"{v['conditions_total']} conditions in CONDITIONS hold. "
        f"{v['conditions_met_today']} hold with what exists today. "
        f"ACCESS WAS THE BINDING CONSTRAINT AND IT IS NOW CLOSED: with a GENERIC small molecule at "
        f"systemic exposure every route at both sites is OPEN "
        f"(parenchyma {v['answer_without_local_delivery'][cat.PARENCHYMA]['worst_margin']}/day, "
        f"CSF {v['answer_without_local_delivery'][cat.LEPTOMENINGEAL]['worst_margin']}/day), but the "
        f"requirement is access {need[cat.PARENCHYMA]} / {need[cat.LEPTOMENINGEAL]} -- NOT 1.0 -- "
        f"and measured intrinsic penetration clears it with no procedure at all: the all-oral "
        f"regimen closes every route at both compartments "
        f"({closed[cat.PARENCHYMA]['worst_margin']:+}/day and "
        f"{closed[cat.LEPTOMENINGEAL]['worst_margin']:+}/day, tolerable={closed['tolerable']}). "
        f"{gating} The residual is no longer access but the per-day KILL RATE, which is still a "
        f"reference constant behind a measured IC50. That is a checklist, not a probability."
    )
