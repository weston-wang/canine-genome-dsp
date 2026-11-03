"""The search re-run with toxicity and delivery as objects rather than prose. It changes the answer.

WHAT PROMPTED THIS

Two objections, and they are the same objection. This project had ALREADY established that dose is
the binding constraint -- `v2.the_tolerability_retraction` found the headline operating point sitting
at the Cmax of the canine MINIMUM LETHAL DOSE. And it had ALREADY examined focused ultrasound, CED
and intrathecal delivery at length. Then `core.regimen` was built with no toxicity term at all, and
`core.catalogue` gave each agent a bare access float with no way to express that an intervention can
CHANGE access. The catalogue and the search contained ZERO occurrences of "ultrasound".

So a refactor whose stated purpose was to stop findings from being lost reproduced the loss, in the
two places the project had spent the most effort. The fix is the one the objection names: a toxicity
class and a delivery class.

WHAT CHANGES WHEN DELIVERY BECOMES AN OBJECT

Composing every agent with every route at the parenchyma, effective kill per day against growth of
0.055 -- and with GEOMETRY ENFORCED rather than left to the reader:

    agent                      bare     +FUS    +CED     +IT bolus  +IT sustained  +efflux
    trametinib (MEK)         0.0042   0.0042  0.0042      0.0140       0.2000      0.0840
    parthenolide             0.0021   0.0021  0.0021      0.0070       0.1000      0.0420
    lomustine                0.0006   0.0006  0.0006      0.0021       0.0300      0.0126

FOCUSED ULTRASOUND CHANGES NOTHING, and the model now says why structurally rather than in prose:
it is FOCAL, and this disease is diffuse -- 23 of 23 poorly demarcated and invading parenchyma, with
meningeal enhancement remote from the mass in 19 of 19 dogs. `DeliveryRoute.apply()` returns the
agent unimproved against diffuse disease. Even granting a focal tumour it reaches only 0.042/day,
still under growth, because it opens TIGHT JUNCTIONS and the constraint is a PUMP.

Two routes do clear growth: intrathecal SUSTAINED release, whose formulation does not exist, and
EFFLUX INHIBITION, which does.

AND THEN TOXICITY TAKES THE SECOND ONE BACK

A P-gp/BCRP inhibitor is NOT SELECTIVE FOR THE BRAIN. The transporter sits in gut, liver and kidney
as well as at the barrier, so co-dosing raises the partner drug's oral bioavailability and lowers its
clearance: SYSTEMIC EXPOSURE RISES ALONGSIDE BRAIN EXPOSURE. `therapies.efflux_modulation` recorded
exactly this in its WHAT_IS_NOT_KNOWN prose -- and then never charged for it.

Charging for it at 2.5x on the partner's organ axis:

    regimen                                    without co-dose        with co-dose
    trametinib + efflux                        tolerable, +0.40   NOT TOLERABLE, -0.50
                                                                  skin/vascular 1.50
    parthenolide + efflux                      tolerable, +0.65   tolerable, +0.12
    six-agent stack + efflux                   tolerable, +0.20   NOT TOLERABLE, -0.62
                                                                  hepatic 1.57, marrow 1.62,
                                                                  skin/vascular 1.50, GI 1.38

A LOOKUP BUG FOUND WHILE WRITING THE TESTS, AND IT MATTERED. `profile_for` matched key-prefix
against agent name in one direction only, so "parthenolide" against the key "parthenolide / DMAPT
(NF-kB)" silently returned NO_TOXICITY -- which makes any regimen containing it look tolerable FOR
FREE. The first version of this module therefore reported parthenolide + efflux at headroom +1.00
and the six-agent stack oversubscribing three axes. The true figures are +0.12 and FOUR axes. A
lookup miss that FAILS OPEN is worse than one that raises, because it produces a favourable answer
rather than an error; `profile_for` now raises.

AND THE HEADLINE NUMBER DOES NOT SURVIVE INTACT

    trametinib + efflux, no toxicity charge     0.0840/day     comfortably beats growth
    skin/vascular load with the co-dose         1.50           oversubscribed
    forced de-rating                            x0.67
    trametinib + efflux, DE-RATED               0.0560/day     beats growth by 0.001

A margin of one thousandth of a day is not a therapy. It is a rounding error sitting on top of an
assumed potency, an assumed toxicity budget and a mouse-derived multiplier. THAT IS THE HONEST STATE
OF THE ROUTE I PROPOSED BEFORE TOXICITY WAS AN OBJECT.

WHAT SURVIVES IS SMALLER THAN WHAT WAS PROPOSED

    parthenolide + efflux co-dose + liposomal clodronate + radiation
        TOLERABLE, headroom +0.12, no de-rating forced -- GI 0.88, hepatic 0.20, CNS-local 0.80

    escape                                   kill/day    margin
    MAPK reactivation above MEK                0.0599    +0.0049
    MEK target-site mutation                   0.0599    +0.0049
    activating ERK lesion                      0.0599    +0.0049
    RTK bypass into PI3K/AKT                   0.0599    +0.0049
    CSF1R-independence                         0.0599    +0.0049
    antigen loss, MHC-I intact                 0.0599    +0.0049
    NF-kB-independence                         0.0179    -0.0371
    drug-tolerant persister                    0.0426    -0.0124

SIX OF EIGHT CLOSE, AT A MARGIN OF FIVE THOUSANDTHS OF A DAY. Two do not. So the regimen that
survives the toxicity constraint is a THREE-AGENT one rather than the six-agent stack proposed
before toxicity was an object -- and it still does not close.

AND THE SAME AGENT SURVIVES FOR A NEW REASON

PARTHENOLIDE + EFFLUX INHIBITION IS THE ONLY COMBINATION THAT STAYS TOLERABLE, because parthenolide's
dose-limiting toxicity sits on the GI axis while the MEK class sits on skin/vascular and lomustine on
marrow and liver. It does not stack with the things it would be given alongside.

That is a second, independent argument for the same agent. The first was mechanistic -- it is the
only small molecule here that is neither division-gated nor antigen-directed, so it is the only
carrier of a binding escape that efflux inhibition can multiply. The second is toxicological -- it is
the only one whose axis is free. Two different constraints selecting the same agent is the closest
thing to corroboration this analysis has produced.

WHAT THIS DOES NOT FIX

The toxicity budgets are ASSUMED. Canine cumulative-toxicity data does not exist for most of these
agents, and the 2.5x efflux multiplier is a reasoned estimate rather than a measurement. This gives
HEADROOM, which is a sensitivity analysis, not a prediction. And pairing a ten-year durability figure
with a toxicity model that has no time dimension remains the cross-assumption error
`persisters_by_cell_and_tolerability` recorded, which no amount of object modelling repairs.
"""

from __future__ import annotations

from .catalogue import GROWTH_PER_DAY, PARENCHYMA, agents_in
from .delivery import EFFLUX_INHIBITION, FOCUSED_ULTRASOUND, Geometry
from .regimen import Regimen
from .toxicity import (EFFLUX_INHIBITOR_TOXICITY_MULTIPLIER, ToxicityProfile, axis_loads,
                       derating_required, headroom, oversubscribed, profile_for, tolerable)


def with_efflux_co_dose(profile: ToxicityProfile) -> ToxicityProfile:
    """The partner drug's systemic exposure rises with its brain exposure. Charge for it."""
    m = EFFLUX_INHIBITOR_TOXICITY_MULTIPLIER
    return ToxicityProfile(
        profile.axis, profile.budget_fraction * m, profile.measured_in_dogs,
        profile.dose_limiting_event + " [efflux co-dose: systemic exposure raised too]",
        profile.source, profile.secondary_axis, profile.secondary_fraction * m)


def regimen_toxicity(agent_names, efflux_co_dose: bool = False,
                     efflux_substrates=("trametinib", "parthenolide", "lomustine")) -> dict:
    profiles = []
    for name in agent_names:
        p = profile_for(name)
        if efflux_co_dose and any(s in name for s in efflux_substrates):
            p = with_efflux_co_dose(p)
        profiles.append(p)
    return {
        "loads": {a.value: round(v, 2) for a, v in axis_loads(profiles).items()},
        "tolerable": tolerable(profiles),
        "headroom": round(headroom(profiles), 2),
        "oversubscribed": {a.value: round(v, 2) for a, v in oversubscribed(profiles).items()},
        "derating": {a.value: round(f, 2) for a, f in derating_required(profiles).items() if f < 1.0},
    }


def derated_kill(agent_name: str, compartment: str = PARENCHYMA) -> dict:
    """What an agent + efflux inhibitor actually delivers once its own axis is charged."""
    agent = next(a for a in agents_in(compartment) if a.name.startswith(agent_name))
    boosted = with_efflux_co_dose(profile_for(agent.name))
    factor = derating_required([boosted]).get(boosted.axis, 1.0)
    raw = EFFLUX_INHIBITION.apply(agent)
    return {
        "raw": round(raw.effective_kill, 4),
        "axis_load": round(axis_loads([boosted])[boosted.axis], 2),
        "derating": round(factor, 2),
        "derated": round(raw.effective_kill * factor, 4),
        "beats_growth": raw.effective_kill * factor > GROWTH_PER_DAY,
        "margin": round(raw.effective_kill * factor - GROWTH_PER_DAY, 4),
    }


# --- recorded results, re-derived by the tests -----------------------------------------------------

ULTRASOUND_IS_FORECLOSED_BY_GEOMETRY = {
    "the_route_exists_and_is_measured_in_dogs": "PMC5596444 / PMID 28912896 -- 10 aged beagles, "
        "TRANSCRANIAL with no craniectomy, barrier opened in ALL TEN, mean enhancement 19+/-11%, no "
        "tissue damage. The this breed is the right size and skull class.",
    "and_it_changes_nothing_here": "It is FOCAL and this disease is DIFFUSE -- 23 of 23 poorly "
        "demarcated and invading parenchyma, meningeal enhancement remote from the mass in 19 of 19. "
        "`DeliveryRoute.apply()` returns the agent unimproved, and the model now enforces that "
        "rather than leaving it to the reader.",
    "even_granting_a_focal_tumour": "trametinib reaches 0.042/day, still under growth of 0.055 -- "
        "because ultrasound opens TIGHT JUNCTIONS and the constraint is a PUMP.",
}

THE_LOOKUP_BUG_THAT_FAILED_OPEN = (
    "`profile_for` matched key-prefix against agent name in ONE DIRECTION ONLY, so 'parthenolide' "
    "against the key 'parthenolide / DMAPT (NF-kB)' silently returned NO_TOXICITY -- and NO_TOXICITY "
    "makes any regimen containing that agent look tolerable FOR FREE.",
    "The first version of this module therefore reported parthenolide + efflux at headroom +1.00 and "
    "the six-agent stack oversubscribing three axes. The true figures are +0.12 and FOUR axes.",
    "A LOOKUP MISS THAT FAILS OPEN IS WORSE THAN ONE THAT RAISES, because it produces a favourable "
    "answer rather than an error. `profile_for` now raises.",
)

# the three-agent regimen that survives the toxicity constraint
TOLERABLE_SURVIVOR = {
    "regimen": "parthenolide + efflux co-dose + liposomal clodronate + radiation",
    "headroom": 0.12,
    "derating_forced": None,
    "escapes_closed": 6,
    "escapes_total": 8,
    "margin_on_those_closed": 0.0049,
    "still_open": ("NF-kB-independence", "drug-tolerant persister"),
    "VERDICT": "The regimen that survives the toxicity constraint is a THREE-AGENT one rather than "
        "the six-agent stack proposed before toxicity was an object -- and it still does not close. "
        "Six of eight escapes close at a margin of FIVE THOUSANDTHS of a day.",
}

TOXICITY_TAKES_BACK_THE_EFFLUX_ROUTE = {
    "trametinib + efflux, no charge": 0.0840,
    "skin_vascular_load_with_co_dose": 1.50,
    "forced_derating": 0.67,
    "trametinib + efflux, DE-RATED": 0.0560,
    "margin_against_growth": 0.0010,
    "VERDICT": "A margin of one thousandth of a day is not a therapy. It is a rounding error sitting "
        "on top of an assumed potency, an assumed toxicity budget and a mouse-derived multiplier. "
        "That is the honest state of the route proposed before toxicity was an object.",
}

WHAT_SURVIVES_AND_WHY_IT_IS_THE_SAME_AGENT = (
    "PARTHENOLIDE + EFFLUX INHIBITION IS THE ONLY COMBINATION THAT STAYS TOLERABLE, because "
    "parthenolide's dose-limiting toxicity sits on the GI axis while the MEK class sits on "
    "skin/vascular and lomustine on marrow and liver. It does not stack with what it would be given "
    "alongside.",
    "That is a SECOND, INDEPENDENT argument for the same agent. The first was mechanistic -- the "
    "only small molecule here that is neither division-gated nor antigen-directed, and therefore the "
    "only carrier of a binding escape that efflux inhibition can multiply. The second is "
    "toxicological -- the only one whose axis is free.",
    "TWO DIFFERENT CONSTRAINTS SELECTING THE SAME AGENT is the closest thing to corroboration this "
    "analysis has produced.",
)

WHAT_THIS_DOES_NOT_FIX = (
    "The toxicity budgets are ASSUMED. Canine cumulative-toxicity data does not exist for most of "
    "these agents, and the 2.5x efflux multiplier is a reasoned estimate rather than a measurement.",
    "This gives HEADROOM, which is a sensitivity analysis and not a prediction.",
    "Pairing a ten-year durability figure with a toxicity model that has NO TIME DIMENSION remains "
    "the cross-assumption error `persisters_by_cell_and_tolerability` recorded, and no amount of "
    "object modelling repairs it.",
)

THE_LESSON_ABOUT_THE_REFACTOR = (
    "A refactor whose stated purpose was to stop findings from being lost REPRODUCED THE LOSS, in "
    "the two places this project had spent the most effort -- toxicity and delivery.",
    "Both had been established, both were written down, and both were left as PROSE while coverage "
    "was made structural. Anything not represented as an object was free to be ignored by the "
    "search, and it was.",
    "The test of an object model is not whether it holds what you were thinking about when you built "
    "it. It is whether it holds what you already knew and had stopped thinking about.",
)
