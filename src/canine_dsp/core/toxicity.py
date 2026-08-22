"""Toxicity as a first-class constraint, because leaving it in prose let it be ignored.

WHY THIS EXISTS, STATED BLUNTLY

This project established, twice and painfully, that dose is the binding constraint:

  * `v2.the_tolerability_retraction` found that the headline operating point of 410 nM sits AT THE
    Cmax OF THE CANINE MINIMUM LETHAL DOSE (FDA NDA 206192, 13-week dog study). "Conservative 25% of
    Cmax" was inverted -- it was not conservative, it was lethal.
  * `four_open_questions_answered.Q1_SHARED_AXIS_TOXICITY` found that applying ONE de-rating factor
    to every agent is only valid when their dose-limiting toxicities sit in DIFFERENT organ systems.
    Stack two marrow-suppressing agents and the de-ratings do not stay independent.

Then `core.regimen` was built with `potency`, `access`, `duty` and `obtainable` -- AND NO TOXICITY
TERM AT ALL. The search could therefore return "six agents at 0.30/day each", which is arithmetic
rather than a regimen, and the objection lived only in a commit message. The object model was
supposed to make that class of mistake impossible and instead it institutionalised it.

WHAT THIS MODULE ENFORCES

Every agent carries a `ToxicityProfile` naming the ORGAN AXIS its dose-limiting toxicity sits on and
how much of that axis's budget it consumes at full dose. A regimen is tolerable only if NO AXIS IS
OVERSUBSCRIBED. Agents on different axes combine freely; agents on the same axis add.

That single rule reproduces the finding the prose version kept losing: trametinib plus an ERK
inhibitor is a vertical MAPK pair on a shared skin/GI/vascular axis, while trametinib plus radiation
is not. And it forces a real cost on the six-agent stack rather than letting it pass silently.

DE-RATING IS NOT FREE

An agent held below full dose delivers proportionally less kill. `derated_potency` is the honest
consequence: if the marrow axis is oversubscribed and every marrow agent is cut to fit, the kill
rates fall with them. A regimen that becomes tolerable only by de-rating must be re-scored at the
de-rated kill, not at the full one. That is the step this project skipped when it paired a ten-year
tumour figure with a toxicity scalar that had no time dimension at all.

WHAT THIS MODULE DOES NOT CLAIM

It does not predict toxicity. Canine cumulative-toxicity data does not exist for most of these
agents, and `persisters_by_cell_and_tolerability` already records that pairing a ten-year durability
figure with a single de-rating scalar is a cross-assumption error. What this gives is HEADROOM --
how much a regimen absorbs before an organ axis is oversubscribed -- which is a sensitivity analysis
and not a prediction.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Organ(Enum):
    """The axis a dose-limiting toxicity sits on. Agents on different axes combine freely."""

    MARROW = "myelosuppression"
    HEPATIC = "hepatotoxicity"
    GI = "gastrointestinal"
    SKIN_VASCULAR = "skin / vascular (MEK-class)"
    CNS_LOCAL = "local CNS / normal-brain tolerance"
    RENAL = "renal"
    OCULAR = "ocular (tear production)"
    IMMUNE_MEDIATED = "immune-mediated adverse events"
    METABOLIC = "hyperglycaemia / insulin resistance (PI3K-class)"
    PROCEDURAL = "vascular access, anaesthesia, catheter and vessel injury"
    SEIZURE = "seizure threshold in an already-irritable brain"
    PERIPHERAL_NERVE = "peripheral neuropathy (microtubule-class)"
    NONE = "no dose-limiting toxicity identified"


@dataclass(frozen=True)
class ToxicityProfile:
    """What an agent costs, on which axis, and whether the figure is measured.

    `budget_fraction` is the share of that organ's tolerable burden consumed at FULL dose. Two agents
    at 0.6 on the same axis oversubscribe it; one at 0.6 and one at 0.6 on different axes do not.
    """

    axis: Organ
    budget_fraction: float
    measured_in_dogs: bool
    dose_limiting_event: str
    source: str = ""
    secondary_axis: Organ | None = None
    secondary_fraction: float = 0.0

    def load(self) -> dict:
        out = {self.axis: self.budget_fraction}
        if self.secondary_axis is not None:
            out[self.secondary_axis] = out.get(self.secondary_axis, 0.0) + self.secondary_fraction
        return out


NO_TOXICITY = ToxicityProfile(Organ.NONE, 0.0, True, "none identified")


def axis_loads(profiles) -> dict:
    """Total budget consumed on each organ axis. Same-axis agents ADD."""
    totals: dict = {}
    for p in profiles:
        for axis, frac in p.load().items():
            if axis is Organ.NONE:
                continue
            totals[axis] = totals.get(axis, 0.0) + frac
    return totals


def oversubscribed(profiles) -> dict:
    """Axes loaded above 1.0, with how far over."""
    return {axis: load for axis, load in axis_loads(profiles).items() if load > 1.0}


def tolerable(profiles) -> bool:
    return not oversubscribed(profiles)


def headroom(profiles) -> float:
    """How much of the tightest axis remains. Negative means it is already oversubscribed."""
    loads = axis_loads(profiles)
    if not loads:
        return 1.0
    return 1.0 - max(loads.values())


def derating_required(profiles) -> dict:
    """Per-axis factor every agent on that axis must be cut by to fit. 1.0 means no cut needed."""
    return {axis: (1.0 / load if load > 1.0 else 1.0) for axis, load in axis_loads(profiles).items()}


def derated_potency(agent_potency: float, profile: ToxicityProfile, profiles) -> float:
    """Kill rate after the cut its own axis demands. De-rating is not free."""
    factor = derating_required(profiles).get(profile.axis, 1.0)
    return agent_potency * factor


WHY_THIS_MODULE_EXISTS = (
    "`v2.the_tolerability_retraction`: the headline operating point of 410 nM sits AT THE Cmax OF "
    "THE CANINE MINIMUM LETHAL DOSE (FDA NDA 206192, 13-week dog study). 'Conservative 25% of Cmax' "
    "was INVERTED -- not conservative, lethal.",
    "`four_open_questions_answered.Q1_SHARED_AXIS_TOXICITY`: applying ONE de-rating factor to every "
    "agent is valid only when their dose-limiting toxicities sit in DIFFERENT organ systems.",
    "AND THEN `core.regimen` WAS BUILT WITH NO TOXICITY TERM AT ALL, so the search could return six "
    "agents at 0.30/day each -- arithmetic rather than a regimen -- with the objection living only "
    "in a commit message. The object model was supposed to make that impossible and instead "
    "institutionalised it.",
)

THE_RULE = (
    "Every agent names the ORGAN AXIS its dose-limiting toxicity sits on and the share of that "
    "axis's budget it consumes at full dose.",
    "A regimen is tolerable only if NO AXIS IS OVERSUBSCRIBED. Different axes combine freely; the "
    "same axis ADDS.",
    "DE-RATING IS NOT FREE. An agent held below full dose delivers proportionally less kill, and a "
    "regimen that becomes tolerable only by de-rating must be RE-SCORED at the de-rated kill.",
)

WHAT_THIS_DOES_NOT_CLAIM = (
    "It does not PREDICT toxicity. Canine cumulative-toxicity data does not exist for most of these "
    "agents.",
    "What it gives is HEADROOM -- how much a regimen absorbs before an organ axis is oversubscribed "
    "-- which is a sensitivity analysis and not a prediction.",
    "Pairing a ten-year durability figure with a single de-rating scalar that has no time dimension "
    "is a cross-assumption error this project already recorded in "
    "`persisters_by_cell_and_tolerability`, and this module does not fix it.",
)


# --- the profiles this analysis actually has -------------------------------------------------------

PROFILES = {
    "trametinib (MEK)": ToxicityProfile(
        Organ.SKIN_VASCULAR, 0.60, True,
        "MEK-class skin, vascular and ocular toxicity",
        source="Class effect. AND THE HARD LIMIT: cobimetinib at 410 nM sits AT THE Cmax OF THE "
               "CANINE MINIMUM LETHAL DOSE (FDA NDA 206192, 13-week dog study).",
        secondary_axis=Organ.GI, secondary_fraction=0.20),
    "ERK inhibitor": ToxicityProfile(
        Organ.SKIN_VASCULAR, 0.60, False,
        "shares the MAPK-class axis with a MEK inhibitor",
        source="Vertical MEK+ERK blockade is a known human toxicity problem. NOT measured in dogs."),
    "PI3K/AKT inhibitor": ToxicityProfile(
        Organ.GI, 0.50, False, "hyperglycaemia, GI", source="NOT measured in dogs for this class."),
    "CSF1R inhibitor": ToxicityProfile(
        Organ.HEPATIC, 0.70, False, "hepatotoxicity -- pexidartinib carries a BOXED WARNING",
        source="Human label. NO canine PK or safety data at all."),
    "lomustine (nitrosourea)": ToxicityProfile(
        Organ.MARROW, 0.65, True,
        "neutropenia at day 7 in 65-76% of dogs; hepatotoxicity is the CUMULATIVE limit",
        source="Treggiari 2022 PMID 35249267 (65%, and HISTIOCYTIC SARCOMA DIAGNOSIS ITSELF is a "
               "risk factor); Gumash 2025 PMID 39467014 (76.5%); Kristal 2004 PMID 14765735 "
               "(hepatic toxicity at a median of 4 doses / 350 mg/m2 cumulative)",
        secondary_axis=Organ.HEPATIC, secondary_fraction=0.55),
    "radiation": ToxicityProfile(
        Organ.CNS_LOCAL, 0.80, True, "normal-brain tolerance -- the reason a 120-day course is "
        "foreclosed", source="The course length that would work cannot be given. SECONDARY SEIZURE "
        "LOAD: brain irradiation lowers the seizure threshold, and that load is now CARRIED ON A "
        "SHARED AXIS with osmotic disruption rather than described in a note.",
        secondary_axis=Organ.SEIZURE, secondary_fraction=0.55),
    "anti-PD-1 (gilvetmab)": ToxicityProfile(
        Organ.IMMUNE_MEDIATED, 0.30, True, "immune-mediated adverse events",
        source="JVIM 2026 PMID 42247661"),
    "liposomal clodronate": ToxicityProfile(
        Organ.HEPATIC, 0.20, False, "reticuloendothelial depletion; liver and spleen take the load",
        source="Mechanism-based. No canine dose-limiting toxicity established."),
    "parthenolide / DMAPT (NF-kB)": ToxicityProfile(
        Organ.GI, 0.35, False, "GI; NF-kB inhibition is broadly immunosuppressive",
        source="Research-stage. NOT measured in dogs."),
    "sulfasalazine (system xc-)": ToxicityProfile(
        Organ.OCULAR, 0.85, True,
        "KERATOCONJUNCTIVITIS SICCA -- and it is PERMANENT. RETRACTED: this profile previously said "
        "'reversible on withdrawal', which is FALSE and was a safety claim. Bjerkas 1985 (PMID "
        "2860750) documents iatrogenic bilateral KCS in dogs from sulfasalazine that was PERMANENT "
        "IN ALL BUT ONE CASE. It is monitorable by Schirmer tear test, which is what makes early "
        "withdrawal possible -- but monitoring limits the number of dogs affected, it does not undo "
        "the injury in one that is.",
        source="Bjerkas 1985, PMID 2860750. Budget raised 0.55 -> 0.85 because an irreversible "
               "dose-limiting toxicity cannot be spent as freely as a reversible one."),
    "hydroxychloroquine (autophagy)": ToxicityProfile(
        Organ.MARROW, 0.45, True,
        "cytopenias at the top of the range; GI and lethargy below it",
        source="CANINE PHASE I EXISTS: PMC4203518 / doi 10.4161/auto.29165 -- spontaneous canine "
               "lymphoma, HCQ up to 12.5 mg/kg/day PO tolerated with doxorubicin, HCQ alone causing "
               "only mild lethargy and GI signs. Human GBM MTD 600 mg/day; at 800 mg 3/3 had "
               "dose-limiting grade 3 neutropenia and thrombocytopenia."),
    "lipophilic statin (mevalonate)": ToxicityProfile(
        Organ.HEPATIC, 0.30, True,
        "transaminase rise; myopathy at high dose",
        source="Cheap, safe in dogs, and lipophilic statins are brain-penetrant. Mechanism hits "
               "GPX4 BIOSYNTHESIS (selenocysteine tRNA) AND the FSP1/CoQ10 bypass."),
    "anti-CD47": ToxicityProfile(
        Organ.MARROW, 0.45, False, "ON-TARGET ANAEMIA -- red cells carry CD47",
        source="Class effect in humans. No canine product exists."),
    "CD204 cell therapy": ToxicityProfile(
        Organ.IMMUNE_MEDIATED, 0.50, False,
        "cytokine release, and ON-TARGET depletion of normal macrophage lineage",
        source="Does not exist for dogs."),
    "temozolomide": ToxicityProfile(
        Organ.MARROW, 0.55, True,
        "MYELOSUPPRESSION -- thrombocytopenia and neutropenia are the dose-limiting toxicities, and "
        "thrombocytopenia is characteristically the one that ends treatment",
        source="Standard alkylator DLT, consistent across species including dogs. NOTE THE "
               "COLLISION: hydroxychloroquine is also on this axis."),
    "paxalisib": ToxicityProfile(
        Organ.METABOLIC, 0.60, True,
        "HYPERGLYCAEMIA -- an ON-TARGET class effect of PI3K inhibition, not an off-target "
        "surprise. Insulin resistance follows from inhibiting the pathway insulin signals through. "
        "Stomatitis and rash below it.",
        source="PI3K/mTOR class effect. The axis is otherwise UNUSED by this regimen, which is why "
               "paxalisib combines cleanly -- but hyperglycaemia in a dog needs monitoring and may "
               "need insulin."),
    "intra-arterial + osmotic disruption": ToxicityProfile(
        Organ.PROCEDURAL, 0.50, True,
        "SEIZURES are the classic complication of osmotic blood-brain-barrier disruption. Plus "
        "general anaesthesia per dose, arterial catheterisation, and vessel injury or embolic risk.",
        source="Neuwelt's canine work (PMID 6796658) and the modern canine feasibility study (PMID "
               "24932854, stable vitals/bloods/neuro status and artery patency through one month) "
               "report it as tolerable -- but 'tolerable in a feasibility study' is not the same as "
               "'free'. THE COLLISION WITH RADIATION IS NOW COMPUTED: both carry load on "
               "Organ.SEIZURE, so stacking them oversubscribes that axis. This sentence previously "
               "SAID they collide while the model put them on separate axes where they could never "
               "add -- an assertion the arithmetic could not see, which is the exact failure mode "
               "`core.regimen` was built to eliminate for coverage and had not yet been applied "
               "here.",
        secondary_axis=Organ.SEIZURE, secondary_fraction=0.60),
    "carboplatin (intra-arterial)": ToxicityProfile(
        Organ.MARROW, 0.60, True,
        "MYELOSUPPRESSION, thrombocytopenia characteristically first. This is the DOSE-LIMITING "
        "toxicity of carboplatin with osmotic barrier disruption as well as systemically.",
        source="Thoroughly established in dogs (standard of care in canine osteosarcoma). "
               "Intra-arterial with barrier disruption: PMID 8587686 (carboplatin/etoposide with "
               "disruption, predictable dose-limiting myelosuppression) and PMID 20023537 "
               "(temozolomide-REFRACTORY patients, carboplatin 200 mg/m2/day intra-arterially). "
               "NOTE THE COLLISION: it lands on the SAME axis temozolomide occupies, which is "
               "harmless when it REPLACES temozolomide and not when it joins it.",
        secondary_axis=Organ.RENAL, secondary_fraction=0.20),
    "O6-benzylguanine": ToxicityProfile(
        Organ.MARROW, 0.85, False,
        "MYELOSUPPRESSION, and it is the whole toxicity signature. With carmustine it forced the MTD "
        "from 200 down to 40 mg/m2 -- an 80% cut blamed for that combination's phase II failure. "
        "With temozolomide, phase II grade 4 haematologic events in 48% (grade 4 neutropenia 47%).",
        source="It WORKS -- it is the agent that restored lomustine sensitivity in canine lines "
               "(PMID 26130852). It is rejected here on the TOXICITY AXIS, not on mechanism: this "
               "regimen's marrow axis is already at exactly 1.00 with ZERO headroom, so a pure "
               "marrow agent is the worst possible addition."),
    "brain-penetrant microtubule agent": ToxicityProfile(
        Organ.PERIPHERAL_NERVE, 0.85, False,
        "PERIPHERAL NEUROPATHY -- the class-defining dose-limiting toxicity of microtubule agents, "
        "and THE REASON SAGOPILONE'S DEVELOPMENT WAS DISCONTINUED. Not merely reported: it ended "
        "the drug.",
        source="RAISED 0.55 -> 0.85. The original figure was set from the EORTC glioma trial's "
               "46% any-grade neuropathy (32% grade 1), which reads as tolerable. It understated "
               "the constraint: sagopilone's development was HALTED across its whole programme "
               "because of neuropathy at effective doses. A toxicity that ends a drug is not a 0.55. "
               "Sagopilone EORTC 26061 (PMID 21321091). NOTE WHAT "
               "AXIS THIS IS: peripheral nerve, NOT marrow. It does not collide with the axis that "
               "pinned every previous version of this regimen -- which is a real structural "
               "advantage and not a modelling convenience.",
        secondary_axis=Organ.MARROW, secondary_fraction=0.25),
    "lisavanbulin (oral)": ToxicityProfile(
        Organ.CNS_LOCAL, 0.70, False,
        "ACUTE NEUROCOGNITIVE TOXICITY -- confusion and memory impairment, and one grade 4 aseptic "
        "meningoencephalitis. Neurocognitive change was protocol-defined as dose-limiting even at "
        "grade 2. Grade 3 events also included cerebral oedema and seizure.",
        source="ABTC1601 phase 1, MGMT-unmethylated glioblastoma (PMID 39371261), n=26. THE POINT "
               "OF THIS PROFILE IS WHAT IS *NOT* ON IT: peripheral sensory neuropathy occurred in "
               "1 of 26 (4%), grade 1, against 46% for sagopilone. The dose-limiting axis is ACUTE "
               "and CNS, not CUMULATIVE and peripheral -- so it caps DOSE without capping DURATION. "
               "The cost is that the loaded organ is the same one the tumour is in.",
        secondary_axis=Organ.SEIZURE, secondary_fraction=0.35),
    "PRMT5 inhibitor (MTA-cooperative)": ToxicityProfile(
        Organ.MARROW, 0.35, False,
        "ANAEMIA and THROMBOCYTOPENIA -- the PRMT5-class toxicity. Set LOW relative to a "
        "conventional cytotoxic because MTA-cooperative inhibitors are designed to spare "
        "MTAP-INTACT cells: normal tissue retains MTAP, so the drug is far less active there. That "
        "selectivity is the entire premise of the class, not a modelling convenience.",
        source="Class effect for PRMT5 inhibition. TNG908 and TNG462 are MTA-cooperative and "
               "brain-penetrant, in phase I/II including glioblastoma (NCT05275478). NO CANINE "
               "DATA. The budget is an ordinal judgement, and if the selectivity does not hold in "
               "vivo this figure is far too low."),
    "mirdametinib (MEK, brain-penetrant)": ToxicityProfile(
        Organ.SKIN_VASCULAR, 0.55, False,
        "MEK-class rash / mucocutaneous, plus the class CK/ocular signals. Brain-penetrant (FDA-"
        "approved for NF1-PN, dosed continuously).",
        source="Class effect; canine data absent. Chosen because most MEK inhibitors (trametinib, "
               "cobimetinib) are P-gp substrates with poor CNS entry; mirdametinib is the CNS-"
               "penetrant one, which is what a brain second-primary maintenance needs.",
        secondary_axis=Organ.GI, secondary_fraction=0.20),
    "abemaciclib (CDK4/6, brain-penetrant)": ToxicityProfile(
        Organ.MARROW, 0.45, False,
        "Neutropenia and diarrhoea are the class dose-limiting toxicities. Abemaciclib is the one "
        "CDK4/6 inhibitor that crosses the blood-brain barrier efficiently; dosed continuously.",
        source="Class effect; canine data absent. Depends on RB1 being INTACT -- an RB1-deleted "
               "tumour (a recurrent minority) is refractory, which is why this tier is gated on Rb.",
        secondary_axis=Organ.GI, secondary_fraction=0.30),
    "intrathecal sustained release": ToxicityProfile(
        Organ.CNS_LOCAL, 0.40, False, "arachnoiditis", source="Formulation does not exist."),
}


def profile_for(agent_name: str) -> ToxicityProfile:
    """Match on the leading token, in either direction.

    The first version did `key.split(" (")[0] in agent_name`, which silently returned NO_TOXICITY
    for "parthenolide" against the key "parthenolide / DMAPT (NF-kB)" -- and NO_TOXICITY makes any
    regimen containing it look tolerable for free. A lookup miss that fails OPEN is worse than one
    that raises, because it produces a favourable answer rather than an error.
    """
    needle = agent_name.split(" (")[0].split(" / ")[0].strip().lower()
    for key, prof in PROFILES.items():
        head = key.split(" (")[0].split(" / ")[0].strip().lower()
        if head == needle or head in needle or needle in head:
            return prof
    raise KeyError(
        f"no toxicity profile for {agent_name!r}. Add one to PROFILES rather than letting the "
        "lookup fail open -- an agent with no profile makes any regimen containing it look "
        "tolerable for free.")


# A P-gp/BCRP inhibitor is NOT SELECTIVE FOR THE BRAIN. P-gp sits in gut, liver and kidney too, so
# co-dosing raises oral bioavailability and lowers clearance -- systemic exposure of the partner drug
# rises alongside its brain exposure. THIS IS THE ANSWER TO "HOW ARE WE BACK AT AN INTOLERABLE DOSE":
# the intervention that buys brain access buys systemic toxicity with it, and the earlier module
# recorded that in prose without ever charging for it.
EFFLUX_INHIBITOR_TOXICITY_MULTIPLIER = 2.5

EFFLUX_CO_DOSE_IS_NOT_FREE = (
    "A P-gp/BCRP inhibitor is NOT SELECTIVE FOR THE BRAIN. The transporter sits in gut, liver and "
    "kidney as well as at the blood-brain barrier, so co-dosing raises the partner drug's oral "
    "bioavailability and lowers its clearance. SYSTEMIC EXPOSURE RISES ALONGSIDE BRAIN EXPOSURE.",
    "So the intervention that buys brain access buys systemic toxicity with it, and the partner's "
    "organ-axis load must be multiplied accordingly. `therapies.efflux_modulation` recorded this in "
    "its WHAT_IS_NOT_KNOWN prose and then never charged for it.",
    "THAT IS HOW AN ANALYSIS THAT HAD ALREADY RETRACTED A LETHAL DOSE ARRIVED BACK AT AN "
    "UNTOLERATED ONE: the constraint was written down, and it was not made structural.",
)
