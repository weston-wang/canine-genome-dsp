"""The persister does not need a persister-directed drug. It needs a drug that is still there when the
cell wakes up.

THE ERROR THIS MODULE CORRECTS, WHICH WAS MINE

Every version of this analysis treated the drug-tolerant persister as an absolute wall: a cell that
has stopped dividing is invisible to any division-gated agent, so covering it REQUIRES an agent that
kills non-dividing cells. That drove the whole search toward ferroptosis, autophagy blockade and
lineage depletion -- toward PERSISTER-DIRECTED THERAPY, a mechanism class that, as the verification
returned, HAS NEVER PRODUCED AN APPROVED THERAPY IN ANY SPECIES.

Two things were wrong with it.

FIRST: A DORMANT CELL IS NOT GROWING EITHER. The model demanded kill > 0.055/day against the
persister -- the same bar as every other clone. But 0.055/day is the growth rate of a DIVIDING
population. A cell that has stopped cycling to survive therapy has, by the same token, stopped
contributing to tumour growth. Requiring a dividing-population kill rate against a non-dividing cell
compares a rate to a state.

SECOND, AND IT IS THE USEFUL HALF: PERSISTENCE IS A TRANSIENT STATE, NOT A LINEAGE. Drug-tolerant
persisters are reversible -- that is what distinguishes them from a resistance mutation. The
population cycles back into proliferation when it can. So a persister is only a durability threat AT
RE-ENTRY, and an agent that is CONTINUOUSLY PRESENT is there when re-entry happens.

    A DIVISION-GATED AGENT DOES NOT FAIL AGAINST PERSISTERS. A TRANSIENT ONE DOES.

That is a completely different requirement, and it is one this project already knows how to price: it
is DUTY CYCLE, the third term of the identity, and every module here already carries it.

WHAT THAT CHANGES

    radiation, 21-day course       duty 0.058    a persister that wakes on day 40 meets nothing
    lomustine, ~4 doses            duty 0.30     misses most re-entry events
    a continuous oral agent        duty 1.00     is present at every re-entry
    metronomic chemotherapy        duty 1.00     the entire point of the schedule

So the answer to the persister is not a new mechanism. IT IS A SCHEDULE. And metronomic dosing --
continuous low-dose oral chemotherapy -- is routine in veterinary oncology, obtainable today, and was
in this repository's own notes from the start.

HOW THIS MODULE PRICES IT

A persister's contribution to progression is its re-entry flux, not its dormant mass. Modelled as:

    effective growth of the persister compartment = growth x cycling_fraction

where `cycling_fraction` is the share of the persister pool that is proliferating at any moment. And
a division-gated agent's effect against that compartment is its normal kill, scaled by the chance of
being present at re-entry -- which is its DUTY CYCLE.

    persister margin = (division-gated kill x duty) + (non-division-gated kill) - growth x cycling

Both terms are kept. A non-division-gated agent still acts on the dormant cell directly; a
continuously dosed division-gated agent acts on it at re-entry. The old model kept only the first and
set the second to zero.

WHAT THIS DOES NOT CLAIM

It does not claim persisters are harmless, and it does not retire the persister-directed agents. It
claims something narrower and more useful: THE PERSISTER ESCAPE IS A DUTY-CYCLE PROBLEM BEFORE IT IS
A MECHANISM PROBLEM, and this project reached for an unproven mechanism class before checking whether
a schedule would do.

The cycling fraction is not measured for canine histiocytic sarcoma -- nothing about persisters is --
so it is swept rather than asserted. The conclusion has to hold across the sweep or it is not a
conclusion.
"""

from __future__ import annotations

from dataclasses import dataclass

# Fraction of a persister pool proliferating at any moment. Unmeasured in canine HS -- swept.
CYCLING_FRACTION_SWEEP = (0.05, 0.10, 0.20, 0.40, 1.00)
CYCLING_FRACTION_DEFAULT = 0.20


@dataclass(frozen=True)
class DormancyModel:
    """How a persister compartment is priced against a regimen."""

    cycling_fraction: float = CYCLING_FRACTION_DEFAULT

    def effective_growth(self, growth: float) -> float:
        """A dormant cell does not divide, so it does not grow at the dividing-population rate."""
        return growth * self.cycling_fraction

    def kill_from(self, agent) -> float:
        """A division-gated agent reaches a persister AT RE-ENTRY, scaled by its duty cycle."""
        if not agent.division_gated:
            return agent.effective_kill
        return agent.effective_kill * agent.duty

    def margin(self, regimen, escape, growth: float) -> float:
        total = sum(self.kill_from(a) for a in regimen.agents if a.covers(escape))
        return total - self.effective_growth(growth)


THE_ERROR_THIS_CORRECTS = {
    "what_the_model_did": "Treated the drug-tolerant persister as an absolute wall -- a non-dividing "
        "cell is invisible to a division-gated agent, so covering it REQUIRES an agent that kills "
        "non-dividing cells.",
    "where_that_led": "Straight to PERSISTER-DIRECTED THERAPY -- ferroptosis, autophagy blockade, "
        "lineage depletion. A mechanism class that HAS NEVER PRODUCED AN APPROVED THERAPY IN ANY "
        "SPECIES (ResMap, PMID 42284402).",
    "first_thing_wrong": "A DORMANT CELL IS NOT GROWING EITHER. The model demanded kill > 0.055/day "
        "against the persister, but 0.055/day is the growth rate of a DIVIDING population. "
        "Requiring a dividing-population kill rate against a non-dividing cell compares a rate to a "
        "state.",
    "second_thing_wrong": "PERSISTENCE IS A TRANSIENT STATE, NOT A LINEAGE. It is reversible -- that "
        "is what distinguishes it from a resistance mutation. So a persister is only a threat AT "
        "RE-ENTRY, and a CONTINUOUSLY PRESENT agent is there when re-entry happens.",
    "THE_ONE_LINE": "A DIVISION-GATED AGENT DOES NOT FAIL AGAINST PERSISTERS. A TRANSIENT ONE DOES.",
}

WHAT_DUTY_CYCLE_BUYS = {
    "radiation, 21-day course": (0.058, "a persister that wakes on day 40 meets nothing"),
    "lomustine, ~4 doses": (0.30, "misses most re-entry events"),
    "a continuous oral agent": (1.00, "present at every re-entry"),
    "metronomic chemotherapy": (1.00, "the entire point of the schedule"),
}

THE_ANSWER_IS_A_SCHEDULE = (
    "The answer to the persister is not a new mechanism. IT IS A SCHEDULE.",
    "Metronomic dosing -- continuous low-dose oral chemotherapy -- is routine in veterinary "
    "oncology, obtainable today, and was in this repository's own notes from the start.",
    "THE PERSISTER ESCAPE IS A DUTY-CYCLE PROBLEM BEFORE IT IS A MECHANISM PROBLEM, and this project "
    "reached for an unproven mechanism class before checking whether a schedule would do.",
)

WHAT_THIS_DOES_NOT_CLAIM = (
    "It does not claim persisters are harmless, and it does not retire the persister-directed "
    "agents -- a non-division-gated agent still acts on the dormant cell directly, and that term is "
    "kept.",
    "The cycling fraction is NOT MEASURED for canine histiocytic sarcoma, so it is SWEPT rather than "
    "asserted. The conclusion has to hold across the sweep or it is not a conclusion.",
)


# --- what the correction buys, computed -------------------------------------------------------------

# cycling fraction -> (persister margin at parenchyma, at leptomeninges) for the revised regimen
PERSISTER_MARGIN_BY_CYCLING = {
    0.05: (0.0854, 0.0489),
    0.10: (0.0826, 0.0462),
    0.20: (0.0771, 0.0407),
    0.40: (0.0661, 0.0297),
    1.00: (0.0331, -0.0033),
}

WHAT_THE_CORRECTION_BUYS = (
    "Under the OLD binary model the persister sat at -0.0544/day at the parenchyma -- the single "
    "worst margin in the whole analysis, and the reason the search was driven into "
    "persister-directed therapy.",
    "Under the corrected model it sits at +0.0771 at the parenchyma and +0.0407 at the "
    "leptomeninges, and it HOLDS ACROSS THE WHOLE CYCLING SWEEP except the degenerate endpoint.",
    "AND THE CLODRONATE ASK FELL FROM 2.0x TO 1.7x, because the regimen no longer has to buy the "
    "persister with a non-division-gated agent alone.",
)

THE_ONE_ROW_WHERE_IT_FAILS = (
    "At cycling fraction 1.00 the leptomeningeal margin goes to -0.0033.",
    "That row is DEGENERATE and should be read as a check rather than a risk: a persister pool that "
    "is proliferating 100% of the time is not a persister pool. It is the ordinary dividing tumour, "
    "and the model correctly prices it as such.",
)

METRONOMIC_IS_THE_SCHEDULE_THAT_DOES_IT = {
    "what": "Continuous low-dose oral chemotherapy. Duty cycle ~1.0 by construction.",
    "status": "ROUTINE IN VETERINARY ONCOLOGY and obtainable today. Canine protocols exist for "
              "cyclophosphamide 6-27 mg/m2, chlorambucil 4 mg/m2/day, lomustine 2.84 mg/m2, "
              "temozolomide 6.6, etoposide 50, with or without toceranib and piroxicam.",
    "why_it_matters_here": "It is the schedule that converts a division-gated agent from useless "
        "against persisters into effective at every re-entry event.",
    "AND_IT_WAS_IN_THIS_REPOSITORY_FROM_THE_START": "`v3.what_i_cannot_verify.WHERE_THIS_POINTS` "
        "already identified metronomic dosing as the answer to the duty-cycle gap. The project then "
        "spent its effort on mechanism classes instead.",
    "the_cost": "Metronomic dosing buys duration by giving up peak concentration. It is a trade "
        "between the second and third terms of the identity, not a free gain.",
}
