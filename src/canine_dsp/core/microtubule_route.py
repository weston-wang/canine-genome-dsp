"""The first answer whose access and duty come from the SAME schedule.

WHAT WENT WRONG BEFORE, IN ONE LINE

Every previous regimen bought its brain access from a PROCEDURE -- intra-arterial infusion past an
osmotically opened barrier -- and then scored it with a duty cycle that only CONTINUOUS DOSING can
produce. `schedule_coherence` shows only the physically impossible row closes. A drug cannot be
delivered monthly under general anaesthesia and be present every hour of every day.

THE FIX IS NOT A BETTER PROCEDURE. IT IS TO BUY ACCESS WITH CHEMISTRY INSTEAD OF WITH SURGERY.

An agent that crosses on its own carries its access with it at every dose. Access and duty then come
from ONE schedule, because there is only one schedule -- take the drug. Nothing has to be reconciled
because nothing is in tension.

WHY MICROTUBULE AGENTS, AND THIS IS THE ONE PLACE THE EVIDENCE IS ACTUALLY STRONG

`hs_drug_sensitivity` (PMID 25715778) is the only pharmacology in this project measured in the RIGHT
SPECIES AND THE RIGHT DISEASE: four canine histiocytic sarcoma lines.

    alkylators (nimustine, melphalan)   134-670x and 42-411x RESISTANT   micrograms per ml
    microtubule agents (vinca, taxane)  as sensitive or MORE sensitive   NANOGRAMS per ml

Five orders of magnitude, and the authors' own conclusion is "microtubule inhibitors may be
considered potential drug candidates for the treatment of canine HS". This analysis spent its entire
history on the class the tumour resists.

THE OBJECTION THAT USED TO KILL THIS, AND WHY IT NO LONGER DOES

Vincas and taxanes are canonical P-gp substrates with essentially no CNS penetration -- and the same
paper reports ABCB1/ABCG2 ELEVATED in these cells. The class that works is the class most likely to
be pumped away from the target.

BUT THAT IS A PROPERTY OF THOSE MOLECULES, NOT OF THE MECHANISM. Agents exist with the same
mechanism and the opposite transport behaviour:

    sagopilone (ZK-EPO)   synthetic epothilone B analogue. AUCbrain:AUCplasma = 0.8, MEASURED
                          (PMID 18780814). Paclitaxel in the same experiment: 0.0, below detection.
                          Not a P-gp substrate. Longer half-life in BRAIN than in other organs.
    RGN3067               oral tubulin destabiliser, colchicine site. EFFLUX RATIO 0.61 -- not an
                          MDR1 substrate. Brain Cmax 7807 ng/ml in rodent after ORAL dosing.
    RGN6024               same programme, low-to-mid nanomolar against GBM lines.

An access figure of 0.8 that arrives by ORAL OR SYSTEMIC DOSING is worth more than a 3.7x gain that
arrives by catheter once a month, even though 0.8 < 0.733 x anything. The gain is not the point. THE
SCHEDULE IS THE POINT.

THE WARNING THAT HAS TO BE STATED BEFORE THE RESULT

SAGOPILONE FAILED IN GLIOBLASTOMA, and it failed cleanly. EORTC 26061 (PMID 21321091), phase II,
recurrent GBM: PFS6 6.7%, median PFS just over six weeks, NO OBJECTIVE RESPONSES, and the authors'
own words -- "no evidence of relevant clinical antitumour activity ... could be detected".

That is exactly the trap `brain_native_regimen` already recorded as BRAIN-PENETRANT IS NOT
BRAIN-EFFECTIVE. It must not be waved away.

THE ARGUMENT THAT IT DOES NOT TRANSFER, AND IT IS A REAL ARGUMENT RATHER THAN AN EXCUSE

The trial and the model are about DIFFERENT THINGS:

    what the trial establishes    sagopilone does not control GLIOBLASTOMA -- a PHARMACODYNAMIC
                                  statement about glioblastoma's sensitivity to microtubule
                                  disruption
    what the model needs          that a microtubule agent reaches brain tissue -- a PHARMACOKINETIC
                                  question, and the SAME programme measured it directly at 0.8

The trial does not show poor delivery. It shows delivery without effect IN THAT TUMOUR. And the
tumour here is not that tumour: canine histiocytic sarcoma has MEASURED microtubule sensitivity at
nanomolar concentrations, which glioblastoma has never been shown to have.

Stated as the provenance rule this project uses everywhere else: the Kp of 0.8 transfers as
pharmacokinetics; the null efficacy is indexed to glioblastoma and does not transfer to a disease
with its own measured sensitivity. THAT IS THE ARGUMENT. IT IS NOT PROOF, AND IF IT IS WRONG THIS
REGIMEN FAILS THE WAY EVERY OTHER ONE DID.

WHAT IS ACTUALLY CLAIMED

All eleven escapes closed at BOTH occupied sites, at a microtubule duty of 0.8, on a schedule with no
internal contradiction and no procedure anywhere in it.

AND IT IS WEAKER THAN WHAT IT REPLACES, WHICH IS THE POINT

    reopens at a doubling time of        7 days   (the retracted regimen claimed it held to 7d)
    worst margin, parenchyma             +0.0416  (the retracted figure was +0.0556)

The honest regimen is more fragile than the incoherent one. That is what happens when a free
parameter is taken away.
"""

from __future__ import annotations

from . import intraarterial_route as ia
from . import toxicity as tox
from .catalogue import ESCAPES, GROWTH_PER_DAY, LEPTOMENINGEAL, PARENCHYMA
from .dormancy import DormancyModel
from .durable_regimen import build as _tmz_build
from .regimen import Agent, Axis, Layer, Regimen

#: Measured brain:plasma AUC ratio for sagopilone. PMID 18780814. Paclitaxel in the same experiment: 0.
SAGOPILONE_BRAIN_PLASMA_AUC = 0.80
PACLITAXEL_BRAIN_PLASMA_AUC = 0.0
RGN3067_EFFLUX_RATIO = 0.61          # <1 means not an MDR1 substrate
REFERENCE_POTENCY = 0.15
REFERENCE_DUTY = 0.80

MICROTUBULE_AGENT = "brain-penetrant microtubule agent"

#: Agents carried over. NOTE what is absent: no procedure, so no seizure or anaesthesia axis at all.
CARRIED_OVER = ("liposomal clodronate", "anti-PD-1 (gilvetmab)", "hydroxychloroquine (autophagy)")


def build(compartment: str, duty: float = REFERENCE_DUTY, potency: float = REFERENCE_POTENCY,
          access: float = SAGOPILONE_BRAIN_PLASMA_AUC) -> Regimen:
    """Everything systemic. Every access figure is the agent's OWN, not a procedure's."""
    others = [a for a in _tmz_build(compartment).agents if a.name in CARRIED_OVER]
    return Regimen("microtubule (schedule-coherent)", others + [
        Agent("paxalisib", Axis.PI3K_PARALLEL, Layer.RECEPTOR, potency, ia.PAXALISIB_KPUU,
              1.0, True, note="ORAL AND CONTINUOUS. Kp,uu 0.31 MEASURED, and a confirmed non-substrate of P-gp and BCRP. "
                              "Oral and continuous, so access and duty come from one schedule."),
        Agent(MICROTUBULE_AGENT, Axis.CYTOTOXIC, Layer.RECEPTOR, potency, access, duty, True,
              note="Access is the MOLECULE'S OWN (sagopilone AUCbrain:AUCplasma 0.8, PMID 18780814; "
                   "RGN3067 efflux ratio 0.61, orally dosed). NO PROCEDURE, so nothing has to be "
                   "reconciled between the access term and the duty term."),
    ])


def margins(compartment: str, growth: float = GROWTH_PER_DAY, **kw) -> dict:
    r = build(compartment, **kw)
    d = DormancyModel()
    return {e.name: (d.margin(r, e, growth) if "persister" in e.name
                     else r.effective_kill_against(e) - growth) for e in ESCAPES}


def worst_margin(compartment: str, growth: float = GROWTH_PER_DAY, **kw) -> float:
    return min(margins(compartment, growth, **kw).values())


def closes(growth: float = GROWTH_PER_DAY, **kw) -> bool:
    return all(worst_margin(c, growth, **kw) > 0 for c in (PARENCHYMA, LEPTOMENINGEAL))


def toxicity_profiles(compartment: str = PARENCHYMA) -> list:
    """No procedure appears here. That absence is a result, not an omission.

    The lookup is STRICT ON PURPOSE. An agent whose name does not match a profile key would
    otherwise be silently free of toxicity, which is the failure mode `toxicity` exists to prevent --
    and this raised a KeyError the first time it ran, on an agent named "paxalisib (oral)" against a
    profile keyed "paxalisib". A `.get(name, NO_TOXICITY)` would have hidden it.
    """
    names = [a.name for a in build(compartment).agents]
    missing = [n for n in names if n not in tox.PROFILES]
    if missing:
        raise KeyError(f"no toxicity profile for {missing} -- an unpriced agent is not free")
    return [tox.PROFILES[n] for n in names]


def headroom(compartment: str = PARENCHYMA) -> float:
    return tox.headroom(toxicity_profiles(compartment))


# --- computed results ---------------------------------------------------------------------------------

#: microtubule duty -> (parenchyma worst, leptomeningeal worst) at reference potency and access
BY_DUTY = {0.4: (-0.0064, 0.0112), 0.6: (0.0176, 0.0352), 0.8: (0.0416, 0.0592),
           1.0: (0.0656, 0.0832)}
DUTY_THRESHOLD = 0.6   # parenchyma closes at or above this; leptomeninges closes lower

#: doubling time -> (parenchyma worst, leptomeningeal worst) at duty 0.8
BY_DOUBLING_TIME = {12.6: (0.0416, 0.0592), 10.0: (0.0273, 0.0449), 7.0: (-0.0024, 0.0152),
                    5.0: (-0.0420, -0.0244), 4.0: (-0.0766, -0.0590)}

WHY_THE_SCHEDULE_IS_COHERENT = {
    "the_previous_defect": "Access 0.733 required a MONTHLY PROCEDURE; duty 1.0 required CONTINUOUS "
        "PRESENCE. No schedule produces both, and `schedule_coherence` shows only that impossible "
        "row closed.",
    "the_fix": "BUY ACCESS WITH CHEMISTRY INSTEAD OF WITH SURGERY. An agent that crosses on its own "
        "carries its access at every dose, so there is only one schedule and nothing to reconcile.",
    "why_0_8_beats_a_3_7x_gain": "The gain is not the point. A 3.7x boost delivered by catheter once "
        "a month buys a duty of 1/28. An access of 0.8 delivered orally buys whatever duty the "
        "dosing interval supports. THE SCHEDULE IS THE POINT.",
    "what_disappears_with_the_procedure": "The seizure axis, the anaesthesia axis, the catheter risk, "
        "and the requirement that this dog's tumour have an artery a catheter can reach.",
}

THE_GLIOBLASTOMA_FAILURE = {
    "what_happened": "EORTC 26061 (PMID 21321091), phase II, recurrent glioblastoma. PFS6 6.7%, "
        "median PFS just over six weeks, NO OBJECTIVE RESPONSES. Authors: 'no evidence of relevant "
        "clinical antitumour activity ... could be detected'.",
    "it_is_the_trap_this_project_already_named": "`brain_native_regimen.WHAT_IS_STILL_ASSUMED` "
        "records BRAIN-PENETRANT IS NOT BRAIN-EFFECTIVE. This is that, in a randomised setting.",
    "what_the_trial_establishes": "A PHARMACODYNAMIC fact about GLIOBLASTOMA's sensitivity to "
        "microtubule disruption. It does NOT show poor delivery -- the same programme measured "
        "brain:plasma AUC at 0.8 directly.",
    "what_the_model_needs": "A PHARMACOKINETIC fact -- that the agent reaches brain tissue. That is "
        "measured, and it is the half that transfers.",
    "why_it_may_not_transfer": "Canine histiocytic sarcoma has MEASURED microtubule sensitivity at "
        "NANOMOLAR concentrations (PMID 25715778). Glioblastoma has never been shown to have it. A "
        "null result in an insensitive tumour is not evidence about a sensitive one.",
    "THE_HONEST_STATUS": "THAT IS AN ARGUMENT, NOT PROOF. If it is wrong -- if the brain environment "
        "defeats microtubule agents for reasons beyond target sensitivity -- THIS REGIMEN FAILS THE "
        "WAY EVERY OTHER ONE DID.",
}

WHAT_IT_COSTS_TO_BE_HONEST = {
    "reopens_at": "a SEVEN-day doubling. The retracted regimen claimed it held to seven days.",
    "worst_parenchymal_margin": "+0.0416, against the retracted +0.0556.",
    "the_lesson": "The coherent regimen is MORE FRAGILE than the incoherent one. That is what "
        "happens when a free parameter is taken away, and it is the correct direction for a "
        "correction to move a result.",
}

WHAT_THIS_CLOSES_FOR_FREE = {
    "MGMT (the eleventh escape)": "A microtubule agent is not an alkylator, so MGMT has no substrate "
        "to repair. The escape that broke the temozolomide regimen does not apply.",
    "the whole alkylator-class resistance": "134-670x on O6 agents and 42-411x on N7 agents "
        "(PMID 25715778) is irrelevant to a drug that does not damage DNA at all.",
    "efflux (ABCB1/ABCG2 up in HS cells)": "Sagopilone is not a P-gp substrate; RGN3067's efflux "
        "ratio is 0.61. The pumps the tumour overexpresses do not carry these molecules.",
    "the marrow ceiling": "The microtubule class's dose-limiting toxicity is PERIPHERAL NEUROPATHY, "
        "a different axis. Marrow drops to 0.70 and total headroom is +0.15.",
}

WHAT_IS_STILL_ASSUMED = (
    "THE POTENCY, 0.15/day, as everywhere else in this project. `hs_drug_sensitivity` gives IC50s, "
    "which are concentrations rather than kill rates -- they establish that the class is ACTIVE, not "
    "how fast it kills in vivo.",
    "THE DUTY of 0.8. Sagopilone has a longer half-life in brain than in other organs and was dosed "
    "roughly weekly in the models, but the fraction of the interval spent above threshold in a "
    "canine brain tumour is NOT MEASURED.",
    "THAT AN AGENT WITH THESE PROPERTIES IS OBTAINABLE FOR A DOG. Sagopilone's development was not "
    "carried forward after the glioma trials; RGN3067 and RGN6024 are preclinical and rodent-only. "
    "THIS IS A CLASS ARGUMENT, NOT A PRESCRIPTION.",
    "THE GROWTH RATE, still, and it now bites harder -- the answer flips between a ten-day and a "
    "seven-day doubling rather than between seven and five.",
)
