"""Stop rescuing poorly-penetrant drugs. Use drugs that cross on their own.

WHY THE PREVIOUS ANSWER HAD TO BE REPLACED

The regimen in `brain_closing_regimen` closed all ten escapes -- and rested entirely on a P-gp/BCRP
inhibitor co-dose to give two small molecules a 20x access boost. Strip that co-dose and both agents
lose the access carrying the brain compartment, and the compartment reopens. No canine protocol for
such a co-dose exists. THE WHOLE BRAIN RESULT HAD A SINGLE POINT OF FAILURE, and it was the one
component nobody has ever given a dog.

The fix is not a better co-dose. IT IS TO STOP CHOOSING AGENTS THAT NEED ONE.

Every access figure this project has fought with -- 0.021, 0.027, 0.001 -- belongs to a molecule that
was selected for something else and then asked to cross a barrier it was never designed for. There is
a whole class of oncology agents selected FOR CNS exposure, and this analysis had not costed one.

THE STRUCTURAL RESULT, AND IT IS CLEAN

With a backbone a dog can actually be given -- radiation, liposomal clodronate, hydroxychloroquine,
anti-PD-1, NO efflux co-dose -- adding ONE continuously dosed agent with INTRINSIC brain access at
potency 0.15/day:

    intrinsic access   parenchyma   leptomeninges
        0.05             -0.0296       -0.0120
        0.10             -0.0221       -0.0045
        0.20             -0.0071       +0.0105
        0.30             +0.0079       +0.0255     BOTH CLOSE
        0.35             +0.0154       +0.0330     BOTH CLOSE
        0.40             +0.0229       +0.0405     BOTH CLOSE

ACCESS OF ROUGHLY 0.30 IS THE THRESHOLD, and it closes BOTH compartments with no transporter
inhibitor anywhere in the regimen.

That number is not exotic. It is approximately temozolomide's reported CSF:plasma ratio -- an oral
agent, dosed continuously as standard practice, already used in dogs, and specifically valued in
neuro-oncology for the property this analysis needs. Its exact figure is under verification and is
NOT asserted here; what is asserted is the REQUIREMENT.

AND UNLIKE THE PREVIOUS ANSWER, IT DEGRADES INSTEAD OF COLLAPSING

Minimum potency to close both compartments at access 0.35, by tumour doubling time:

    doubling    growth/day    potency needed    multiple of 0.15
     12.6d        0.0550          0.15               1.0x
     10.0d        0.0693          0.15               1.0x
      7.0d        0.0990          0.25               1.7x
      5.0d        0.1386          0.35               2.3x
      4.0d        0.1733          0.45               3.0x
      3.0d        0.2310          0.65               4.3x

At the bottom of the plausible access range (0.30) the asks rise to 2.0x at a seven-day doubling and
2.7x at five days. Every row is a bet, but the bets are on POTENCY -- a bench-measurable property of
a specific drug against specific cell lines -- rather than on a delivery adjunct nobody has given a
dog.

WHAT THIS BUYS OVER THE PREVIOUS REGIMEN

    single point of failure       WAS the efflux co-dose      NOW none
    agents a dog cannot be given  WAS two of five             NOW depends on the chosen agent
    behaviour at faster growth    WAS collapse                NOW a rising potency requirement
    unmeasured inputs             WAS 4 potencies + growth    NOW 1 access + 1 potency + growth

THE BUG THAT EXPOSED ALL THIS, AND IT WAS MINE

The first version of this sweep produced rows that were FLAT -- the added agent's access made no
difference at any value, which is impossible if it is contributing anything. The cause was a default
in the `Agent` dataclass: `antigen_directed` defaulted to TRUE, so every agent that had not been
explicitly annotated inherited an immune-effector property. LOMUSTINE WAS BEING DEFEATED BY ANTIGEN
LOSS. A DNA-damaging agent does not care what the cell displays.

The default is now FALSE, and `antigen_directed=True` is set explicitly on the one agent for which it
is true -- anti-PD-1, whose effector step genuinely requires the tumour to display something. A
default that silently applies a property to everything unannotated is the same class of error as a
number that silently migrates between drugs, and this project has now made both.

WHAT IS STILL ASSUMED

  * The intrinsic access figure. It is the whole result, and it is under verification rather than
    settled. If the real number is 0.10 rather than 0.30, this regimen fails exactly as the others did.
  * The potency, 0.15/day against canine histiocytic sarcoma. Unmeasured, like every potency here.
  * The growth rate, still. Every row of the table above is indexed on it.
  * That an agent with good CNS exposure is also ACTIVE in this disease. Penetration is necessary and
    not sufficient -- `therapies.upstream_nodes` already records BLZ945 as brain-penetrant and
    reporting LIMITED EFFICACY in glioblastoma. Brain-penetrant is not brain-effective.
"""

from __future__ import annotations

from .catalogue import ESCAPES, GROWTH_PER_DAY, LEPTOMENINGEAL, PARENCHYMA, agents_in
from .dormancy import DormancyModel
from .regimen import Agent, Axis, Layer, Regimen

REFERENCE_POTENCY = 0.15
ACCESS_THRESHOLD = 0.30


def backbone(compartment: str) -> list:
    """Obtainable, and NOTHING here needs a transporter inhibitor."""
    p = {a.name: a for a in agents_in(compartment)}
    return [p["radiation"], p["liposomal clodronate"], p["hydroxychloroquine (autophagy)"],
            p["anti-PD-1 (gilvetmab)"]]


def build(compartment: str, access: float, potency: float = REFERENCE_POTENCY,
          with_second_agent: bool = False) -> Regimen:
    """Backbone plus one continuously dosed agent with INTRINSIC brain access."""
    agents = backbone(compartment) + [
        Agent("brain-native cytotoxic", Axis.CYTOTOXIC, Layer.RECEPTOR, potency, access, 1.0, True,
              note="Selected FOR CNS exposure rather than rescued into it. Continuous dosing, so "
                   "duty 1.0 -- which is what reaches a persister at re-entry.")]
    if with_second_agent:
        agents.append(
            Agent("brain-native proteasome", Axis.SURVIVAL_SIGNAL, Layer.RECEPTOR, potency, access,
                  1.0, True, division_gated=False,
                  note="A brain-penetrant proteasome inhibitor is not division-gated, so it acts on "
                       "the dormant cell directly as well as at re-entry."))
    return Regimen("brain-native", agents)


def worst_margin(compartment: str, access: float, potency: float = REFERENCE_POTENCY,
                 growth: float = GROWTH_PER_DAY, **kw) -> float:
    r = build(compartment, access, potency, **kw)
    d = DormancyModel()
    return min(d.margin(r, e, growth) if "persister" in e.name
               else r.effective_kill_against(e) - growth for e in ESCAPES)


def closes(access: float, potency: float = REFERENCE_POTENCY, growth: float = GROWTH_PER_DAY,
           **kw) -> bool:
    return all(worst_margin(c, access, potency, growth, **kw) > 0
               for c in (PARENCHYMA, LEPTOMENINGEAL))


# --- computed results -------------------------------------------------------------------------------

# intrinsic access -> (parenchyma margin, leptomeningeal margin) at potency 0.15
ACCESS_SWEEP = {
    0.05: (-0.0296, -0.0120),
    0.10: (-0.0221, -0.0045),
    0.20: (-0.0071, 0.0105),
    0.30: (0.0079, 0.0255),
    0.35: (0.0154, 0.0330),
    0.40: (0.0229, 0.0405),
}

# doubling time (days) -> minimum potency per day at access 0.35
REQUIREMENT_BY_DOUBLING_TIME = {12.6: 0.15, 10.0: 0.15, 7.0: 0.25, 5.0: 0.35, 4.0: 0.45, 3.0: 0.65}
REQUIREMENT_AT_ACCESS_030 = {12.6: 0.15, 7.0: 0.30, 5.0: 0.40}

WHY_THE_PREVIOUS_ANSWER_HAD_TO_GO = (
    "It closed all ten escapes and rested ENTIRELY on a P-gp/BCRP inhibitor co-dose giving two small "
    "molecules a 20x access boost. Strip the co-dose and the compartment reopens.",
    "No canine protocol for such a co-dose exists. THE WHOLE BRAIN RESULT HAD A SINGLE POINT OF "
    "FAILURE, and it was the one component nobody has ever given a dog.",
    "The fix is not a better co-dose. IT IS TO STOP CHOOSING AGENTS THAT NEED ONE.",
)

THE_REFRAME = (
    "Every access figure this project has fought with -- 0.021, 0.027, 0.001 -- belongs to a molecule "
    "SELECTED FOR SOMETHING ELSE and then asked to cross a barrier it was never designed for.",
    "There is a whole class of oncology agents selected FOR CNS exposure, and this analysis had not "
    "costed one.",
)

WHAT_THIS_BUYS = {
    "single point of failure": ("WAS the efflux co-dose", "NOW none"),
    "agents a dog cannot be given": ("WAS two of five", "NOW depends on the chosen agent"),
    "behaviour at faster growth": ("WAS collapse", "NOW a rising potency requirement"),
    "unmeasured inputs": ("WAS 4 potencies + growth", "NOW 1 access + 1 potency + growth"),
}

THE_BUG_THAT_EXPOSED_IT = {
    "the_symptom": "The first version of this sweep produced FLAT rows -- the added agent's access "
        "made no difference at any value, which is impossible if it contributes anything.",
    "the_cause": "`Agent.antigen_directed` defaulted to TRUE, so every agent not explicitly "
        "annotated inherited an immune-effector property. LOMUSTINE WAS BEING DEFEATED BY ANTIGEN "
        "LOSS. A DNA-damaging agent does not care what the cell displays.",
    "the_fix": "The default is now FALSE, and antigen_directed=True is set explicitly on the one "
        "agent for which it is true -- anti-PD-1, whose effector step genuinely requires the tumour "
        "to display something.",
    "THE_CLASS_OF_ERROR": "A default that silently applies a property to everything unannotated is "
        "the same class of error as a number that silently migrates between drugs. This project has "
        "now made both.",
}

WHAT_IS_STILL_ASSUMED = (
    "THE INTRINSIC ACCESS FIGURE. It is the whole result, and it is under verification rather than "
    "settled. If the real number is 0.10 rather than 0.30, this regimen fails exactly as the others "
    "did.",
    "The potency, 0.15/day against canine histiocytic sarcoma. Unmeasured, like every potency here.",
    "The growth rate, still. Every row of the requirement table is indexed on it.",
    "THAT AN AGENT WITH GOOD CNS EXPOSURE IS ALSO ACTIVE IN THIS DISEASE. Penetration is necessary "
    "and not sufficient -- `therapies.upstream_nodes` already records BLZ945 as brain-penetrant and "
    "reporting LIMITED EFFICACY in glioblastoma. BRAIN-PENETRANT IS NOT BRAIN-EFFECTIVE.",
)
