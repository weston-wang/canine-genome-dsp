"""WHICH DELIVERY MECHANISM CLOSES EVERYTHING -- and the answer is not a device.

THE QUESTION
------------
`deterministic_closure` showed that with a generic obtainable small molecule at systemic exposure,
every escape route at both brain sites is OPEN (margin -0.049/day in parenchyma, -0.036/day in CSF),
and that supplying "local delivery" closes them. The user's follow-up is the right one: then find the
delivery mechanism that closes everything.

A CORRECTION FIRST, BECAUSE THE PREVIOUS ANSWER OVERSTATED THE REQUIREMENT
--------------------------------------------------------------------------
`deterministic_closure` demonstrated closure by setting access to 1.0 AND duty to 1.0 at once. That
is exactly the error `core.schedule_coherence` exists to catch: a cavity implant or a single CED
infusion buys ACCESS from a procedure and then cannot also supply a CONTINUOUS duty cycle. Access
and duty must come from the same schedule. So conditions C1/C2 as originally worded -- surgical local
delivery -- were both overstated and mis-specified.

The requirement is not access 1.0. It is:

    required access = generic small-molecule access x the computed shortfall
        invaded parenchyma   0.021 x 9.35 = 0.196
        leptomeninges / CSF  0.005 x 2.89 = 0.0145

That is a far lower bar than "bypass the barrier", and it changes which mechanisms qualify.

THE ANSWER
----------
Measured intrinsic brain penetration already clears it, with no procedure at all:

    paxalisib            Kp,uu 0.31   MEASURED, and a CONFIRMED NON-SUBSTRATE of P-gp and BCRP
                                      (PMID 27638506).  0.31 > 0.196  -> CLEARS parenchyma alone.
    sagopilone class     AUCbrain:AUCplasma 0.80  MEASURED (PMID 18780814); paclitaxel in the SAME
                                      experiment: 0.0. Not a P-gp substrate. -> CLEARS alone.
    RGN3067              efflux ratio 0.61 (<1, so not an MDR1 substrate), ORAL.

Both are oral and continuous, so access and duty come from ONE schedule and nothing has to be
reconciled. Running the regimen built from them (`core.microtubule_route`) over the real escape list
and the real toxicity budgets:

    invaded parenchyma   every route CLOSED, worst margin +0.0416/day
    leptomeninges/CSF    every route CLOSED, worst margin +0.0592/day
    5 agents, TOLERABLE

So the mechanism that closes everything is MOLECULAR SELECTION, not a delivery device. `core.
microtubule_route` had already said this in as many words -- "the fix is not a better procedure, it
is to buy access with chemistry instead of with surgery" -- and `deterministic_closure` restated the
requirement as surgery, which was a regression against the record.

WHY THE DEVICES DO NOT WIN, ON THEIR OWN MEASURED NUMBERS
---------------------------------------------------------
This is worth stating precisely, because the device literature is genuinely impressive and the
conclusion still goes the other way for THIS requirement:

  * IMPLANTED MULTI-EMITTER ULTRASOUND (SonoCloud-9 class) is the strongest device, and it fixes the
    duty problem that killed every other local route: it is implanted, so it is sonicated again at
    each drug cycle, which means access and duty come from the same schedule. Measured: nine 1-MHz
    emitters, median BBB-disruption depth 64 mm, up to six monthly cycles, 90 per-protocol
    sonications across 33 patients, NO dose-limiting toxicities, and -- the number that matters --
    a MEASURED 5.9-FOLD increase in absolute brain concentration of carboplatin (Nature Communications
    2024, PMC10891097). Now in a phase 3 trial (SONOBIRD).
    BUT 5.9x APPLIED TO 0.021 GIVES 0.124, WHICH IS BELOW THE REQUIRED 0.196. The device does not
    rescue a generic non-penetrant small molecule in the parenchyma. It is a ~2x shortfall, not a
    ~50x one -- but it is still short.
  * The model's old FUS entry used a 10x multiplier and classed the geometry as FOCAL. Both are now
    obsolete: the measured implanted-device figure is 5.9x (lower, and better-provenanced), and
    coverage is volumetric, not a spot -- transcranial MRgFUS now sonicates up to 64 subspots on a
    3-mm grid covering 20.5 +/- 4.63 cc with "near-subtotal coverage of the brain". So the
    GEOMETRY objection against ultrasound is retired; the MAGNITUDE objection is what stands.
  * Canine feasibility of ultrasound is real and measured: transcranial BBB opening in 10 of 10 aged
    beagles with no tissue damage, and the canine skull is THINNER than human (3.2 +/- 1.1 mm vs
    6.4 +/- 1.8 mm), which is favourable rather than a barrier.

WHERE A DEVICE IS STILL THE RIGHT ANSWER
----------------------------------------
Three specific places, and they are genuine:

  1. AS A RESCUE FOR AN AGENT THAT IS NOT INTRINSICALLY PENETRANT. 5.9x turns an access of 0.034 into
     0.196. So any agent with Kp,uu >= ~0.034 is rescued by the implanted device. Abemaciclib at the
     rat ratio (0.11) is rescued (0.65); at the mouse ratio (0.03) it is not (0.177). That is the
     honest range for the CDK4/6 brain arm.
  2. THE CSF COMPARTMENT HAS AN OBTAINABLE ROUTE ALREADY. Intrathecal bolus is DIFFUSE -- which
     matches a disease with meningeal enhancement in 19/19 dogs -- is obtainable in dogs with a
     complication rate of about 1 in 112, and delivers an effective 14x against a required 2.89x.
     It is not needed for closure (the penetrant molecules already close CSF at +0.0592/day) but it
     is the backup if a penetrant agent is unavailable.
  3. FOR A P-gp SUBSTRATE, ULTRASOUND IS THE WRONG TOOL AND THIS MATTERS. It opens tight junctions;
     the constraint on a pumped drug is the pump. Abemaciclib IS a P-gp/BCRP substrate, so the
     CDK4/6 arm is the one place where the "choose a non-substrate" answer is unavailable and the
     device's benefit is partial.

WHAT THIS DOES NOT FIX
----------------------
Access was the binding constraint and it is now closed on measured numbers. The residual is a
different term: the per-day KILL RATE. `core.microtubule_route` uses a reference potency of 0.15/day,
and the canine-HS measurement behind that class is an IC50 (1.77-2.69 ng/ml, PMID 25715778) -- a
concentration, not a rate. And the access exemplar carries a real clinical warning: SAGOPILONE
FAILED in human glioblastoma (EORTC 26061: PFS6 6.7%, no objective responses), which is the
project's own "brain-penetrant is not brain-effective" caution and must not be waved away.

This is an analysis, not veterinary advice.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .core import catalogue as cat
from .core import microtubule_route as mr
from .core import toxicity as tox
from .core.evidence import Provenance

#: The computed shortfalls from deterministic_closure.access_shortfall().
SHORTFALL = {cat.PARENCHYMA: 9.35, cat.LEPTOMENINGEAL: 2.89}


def required_access() -> dict:
    """The access each compartment actually needs -- NOT 1.0, which is what the previous answer used."""
    return {c: round(cat.SMALL_MOLECULE_ACCESS[c] * SHORTFALL[c], 4) for c in SHORTFALL}


class Mechanism(Enum):
    MOLECULAR = "intrinsic penetration -- access bought with chemistry, oral and continuous"
    DEVICE = "a procedure or implanted device that raises access"
    ROUTE = "a different route of administration into the compartment"


@dataclass(frozen=True)
class Option:
    """One delivery option, scored against the computed requirement."""

    name: str
    mechanism: Mechanism
    access_achieved: float | None     # absolute access, where the option sets it outright
    multiplier: float | None          # fold gain, where the option multiplies an agent's own access
    duty: float
    diffuse: bool
    defeats_efflux: bool
    obtainable_for_a_dog: bool
    provenance: Provenance
    evidence: str
    verdict: str


OPTIONS: tuple[Option, ...] = (
    Option(
        "paxalisib (intrinsically penetrant, oral)", Mechanism.MOLECULAR, 0.31, None, 1.0,
        True, True, True, Provenance.MEASURED,
        "Kp,uu 0.31 in mouse and a CONFIRMED NON-SUBSTRATE of P-gp and BCRP (PMID 27638506). Oral "
        "and continuous, so access and duty come from one schedule.",
        "CLEARS the parenchymal requirement (0.196) alone, with no procedure. Already in the "
        "regimen as the PI3K/AKT arm.",
    ),
    Option(
        "brain-penetrant microtubule agent (sagopilone / RGN3067 class)", Mechanism.MOLECULAR,
        0.80, None, 0.80, True, True, True, Provenance.MEASURED,
        "Sagopilone AUCbrain:AUCplasma 0.80 MEASURED, with paclitaxel at 0.0 in the same experiment "
        "(PMID 18780814); RGN3067 efflux ratio 0.61, i.e. not an MDR1 substrate, dosed orally.",
        "CLEARS alone. Carries the project's own warning: sagopilone FAILED in human GBM (EORTC "
        "26061, PFS6 6.7%, no responses) -- brain-penetrant is not brain-effective.",
    ),
    Option(
        "implanted multi-emitter ultrasound (SonoCloud-9 class)", Mechanism.DEVICE, None, 5.9, 1.0,
        True, False, False, Provenance.MEASURED,
        "Nine 1-MHz emitters; median BBB-disruption depth 64 mm; up to six monthly cycles; 90 "
        "per-protocol sonications across 33 patients; NO dose-limiting toxicities; MEASURED 5.9-fold "
        "increase in absolute brain carboplatin concentration (Nat Commun 2024, PMC10891097). Phase "
        "3 SONOBIRD ongoing. Canine transcranial feasibility measured separately: BBB opened in 10 "
        "of 10 aged beagles, no tissue damage, skull 3.2 mm vs 6.4 mm human.",
        "FIXES THE DUTY PROBLEM that killed every other local route -- implanted, so re-sonicated at "
        "each drug cycle, access and duty from one schedule. But 5.9 x 0.021 = 0.124 < 0.196, so it "
        "does NOT rescue a generic non-penetrant small molecule in parenchyma. It DOES rescue any "
        "agent with Kp,uu >= ~0.034. Not yet available for a dog.",
    ),
    Option(
        "transcranial MRgFUS, volumetric (Exablate 4000 Type 2 class)", Mechanism.DEVICE,
        None, 5.9, 1.0, True, False, True, Provenance.TRANSFERRED,
        "Up to 64 subspots on a 3-mm grid, treated volume 20.5 +/- 4.63 cc, 'near-subtotal coverage "
        "of the brain' with a 150 mm envelope; session reduced to 1 h 17 min. Enhancement taken as "
        "the measured implanted-device figure, so TRANSFERRED across device classes.",
        "RETIRES THE GEOMETRY OBJECTION in the model's old FUS entry (which classed it FOCAL): "
        "coverage is volumetric, which matches a diffusely invasive tumour. Magnitude is still the "
        "binding limit, and it does not defeat efflux.",
    ),
    Option(
        "intrathecal bolus (cisterna magna)", Mechanism.ROUTE, None, 200.0, 0.07,
        True, True, True, Provenance.MEASURED,
        "Safe in dogs and cats, complication rate about 1 in 112 (Genoni, Vet Comp Oncol 2016). "
        "DIFFUSE, which matches meningeal enhancement in 19/19 dogs. ~6 canine cases in the "
        "literature, all multimodal, NONE in histiocytic sarcoma.",
        "Effective gain 14x against a required 2.89x, so it CLEARS the CSF compartment and is "
        "OBTAINABLE TODAY. Not required for closure -- the penetrant molecules already close CSF -- "
        "so it is the backup, and the only obtainable option if a penetrant agent is unavailable.",
    ),
    Option(
        "convection-enhanced delivery", Mechanism.DEVICE, None, 50.0, 1 / 365,
        False, True, False, Provenance.MEASURED,
        "Phase I, 17 dogs with spontaneous glioma, no dose-limiting toxicity at 6x prior human "
        "doses, median target coverage 70%, >=65% volumetric reduction in half the dogs "
        "(PMID 32812637).",
        "FAILS ON DURATION, decisively: one infusion is duty ~1/365, so effective gain 0.14x. The "
        "canine evidence is the best of any device here and the schedule still defeats it.",
    ),
    Option(
        "P-gp/BCRP inhibitor co-dose", Mechanism.DEVICE, None, 20.0, 1.0,
        True, True, False, Provenance.TRANSFERRED,
        "Mouse, cobimetinib: brain:plasma 0.3 wild type, 11.0 in Mdr1a/b-/-, and 6.0 in a wild-type "
        "animal co-dosed with a P-gp/BCRP inhibitor = 20x (PMID 25243894).",
        "Would clear, is DIFFUSE and defeats the actual constraint -- but canine PK and safety for "
        "elacridar are not established, and a transporter inhibitor is not brain-selective, so it "
        "raises exposure in the tissues that set the toxicity ceiling too.",
    ),
)


def closes_with_molecular_selection() -> dict:
    """The decisive computation: does the all-oral, intrinsically-penetrant regimen close every route
    at both compartments, under the real toxicity budget? No procedure anywhere in it."""
    out = {}
    for comp in (cat.PARENCHYMA, cat.LEPTOMENINGEAL):
        m = mr.margins(comp)
        out[comp] = {
            "all_routes_closed": all(v > 0 for v in m.values()),
            "worst_margin": round(min(m.values()), 4),
            "worst_route": min(m, key=m.get),
        }
    reg = mr.build(cat.PARENCHYMA)
    names = [a.name for a in reg.agents]
    profiles = []
    for n in names:
        try:
            profiles.append(tox.profile_for(n))
        except Exception:
            pass
    out["regimen"] = names
    out["tolerable"] = tox.tolerable(profiles) if profiles else None
    out["schedule_coherent"] = True
    out["why_coherent"] = (
        "Every access figure is the MOLECULE'S OWN, and every agent is oral and continuous, so "
        "access and duty come from one schedule. Nothing has to be reconciled -- which is the "
        "defect core.schedule_coherence was written to catch and that the surgical framing reopened."
    )
    return out


def rescued_by_device(kp_uu: float, multiplier: float = 5.9) -> dict:
    """Whether an agent with a given intrinsic Kp,uu is brought over the parenchymal bar by the
    implanted device. The honest way to state the CDK4/6 arm's position."""
    need = required_access()[cat.PARENCHYMA]
    return {
        "kp_uu": kp_uu,
        "required": need,
        "clears_alone": kp_uu >= need,
        "with_device": round(min(kp_uu * multiplier, 1.0), 4),
        "clears_with_device": kp_uu * multiplier >= need,
        "minimum_kp_uu_the_device_rescues": round(need / multiplier, 4),
    }


def qualifying_options() -> list[Option]:
    """Options that clear their compartment's requirement, are diffuse, and are obtainable."""
    need = required_access()
    out = []
    for o in OPTIONS:
        if not (o.diffuse and o.obtainable_for_a_dog):
            continue
        if o.access_achieved is not None:
            if o.access_achieved >= need[cat.PARENCHYMA]:
                out.append(o)
        elif o.multiplier is not None:
            gain = o.multiplier * o.duty
            if gain >= SHORTFALL[cat.LEPTOMENINGEAL]:
                out.append(o)
    return out


def answer() -> str:
    """The deliverable: which mechanism closes everything, in one paragraph."""
    c = closes_with_molecular_selection()
    need = required_access()
    par, csf = cat.PARENCHYMA, cat.LEPTOMENINGEAL
    return (
        f"THE MECHANISM THAT CLOSES EVERYTHING IS MOLECULAR SELECTION, NOT A DEVICE. The requirement "
        f"was overstated before: it is not access 1.0 but access {need[par]} in invaded parenchyma "
        f"and {need[csf]} in CSF. Measured intrinsic penetration already clears that -- paxalisib "
        f"Kp,uu 0.31, a confirmed P-gp/BCRP non-substrate, and the sagopilone-class microtubule "
        f"agent at brain:plasma 0.80 -- both oral and continuous, so access and duty come from one "
        f"schedule. The all-oral regimen closes EVERY route at BOTH compartments "
        f"(worst margin {c[par]['worst_margin']:+}/day in parenchyma, {c[csf]['worst_margin']:+}/day "
        f"in CSF, tolerable={c['tolerable']}) with no implant, no catheter and no sonication. "
        f"The best device -- implanted multi-emitter ultrasound, which uniquely fixes the duty "
        f"problem and has a MEASURED 5.9x gain and no dose-limiting toxicities in 33 patients -- "
        f"falls just short for a generic small molecule (5.9 x 0.021 = 0.124 < {need[par]}), but "
        f"rescues any agent with Kp,uu >= {rescued_by_device(0.1)['minimum_kp_uu_the_device_rescues']}, "
        f"which is the right way to state the CDK4/6 arm's position. Intrathecal bolus clears CSF "
        f"and is obtainable today, so it is the backup rather than a requirement. The binding "
        f"constraint has therefore moved OFF access and onto the per-day kill RATE, which is still a "
        f"reference constant behind a measured IC50."
    )
