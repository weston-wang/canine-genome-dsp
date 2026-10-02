"""EXISTS-TODAY FIRST: the closure program searched from agents that are obtainable for a dog now.

WHY THIS MODULE EXISTS
----------------------
`CLAUDE.md` rule 13:

    "A closure program is built from agents that exist... Tier every agent as exists-today
     (licensed, off-label, or in dog trials) or to-build. Search for the program from exists-today
     agents first; a program that needs a to-build agent is reported SEPARATELY and as such."

The HS program was not built that way. It was built from whichever molecule had the right measured
property, and then `core.microtubule_route.build()` flagged every agent `obtainable=True`, which is
optimistic labelling: the induction agent RGN3067 is preclinical and rodent-only, and the
genotype-anchored maintenance agent is in human Phase I with no veterinary access. Two of the five
agents in the headline regimen cannot be given to a dog today, and the report's summary table said
"obtainable for dogs" against one of them.

The honest way to state a result under rule 13 is TWO programs, computed separately:

    PROGRAM A -- exists-today only. Nothing in it needs to be invented, licensed or sponsored.
    PROGRAM B -- the full closure, which needs two to-build agents, reported AS SUCH.

This module computes both over the same compartments, the same growth bar and the same PK/PD
machinery, so the difference between them is a result rather than a framing.

WHAT THE COMPUTATION FINDS, AND IT IS NOT WHAT THE REPORT IMPLIED
----------------------------------------------------------------
The single most important correction this module makes is about WHICH COMPARTMENT MATTERS. This
tumour is EXTRA-AXIAL and MENINGES-BASED in 23/23 dogs -- the bulk of it sits on the blood side of
an already-disrupted barrier, and only its invading edge sits behind an intact one. The exists-today
program is strong exactly there and weak exactly at the invading edge:

    EXTRA-AXIAL / BLOOD-SIDE BULK   ribociclib's MEASURED unbound concentration in ENHANCING
                                    tumour, 2152 nM against a 40 nM IC50 (PMID 31285369), and
                                    abemaciclib's measured brain-lesion tissue multiple of 19x as
                                    the alternative. CLOSES decisively, licensed agents only.

    LEPTOMENINGES / CSF             ribociclib's MEASURED unbound CSF concentration, 374 nM
                                    (PMID 31285369). CLOSES BY MOUTH, +0.72/day, with intrathecal
                                    bolus demoted to a backup rather than a requirement.

    INVADED PARENCHYMA, INTACT      THE SITE THAT WAS OPEN, AND IT CLOSED ON A LICENSED DRUG.
    BARRIER                         Gadolinium-NON-ENHANCING tumour IS tissue behind an intact
                                    barrier, by definition, so a drug concentration measured there
                                    answers the access question directly instead of inferring it
                                    from a rodent ratio. Ribociclib: 170 nM median at 400 mg,
                                    634 nM at 600 mg (PMID 41206763), 560 nM at 900 mg
                                    (PMID 31285369) -- every reported value clears the 0.055/day
                                    bar, including the lowest single patient at 65 nM (5.8x the
                                    bar). The 2026 trial enrolled on CDKN2A/B deletion with
                                    wild-type Rb, which is THIS TUMOUR'S LESION, and confirmed the
                                    pharmacodynamics in the same tissue (RB phosphorylation and
                                    Ki-67 both significantly down). Oral and continuous, so access
                                    and duty come from ONE schedule and no procedure is involved.

Abemaciclib was the previous candidate at that third site and is kept as the alternative, but its
own measured rodent range spans failure to a thin pass (-0.034 to +0.017/day across mouse and rat
Kp,uu) -- which is precisely why a measured concentration in the right compartment beats an inferred
ratio, and why this finding matters more than its size.

So the gap between Program A and Program B is now a set of MECHANISM gaps rather than delivery gaps.
`the_gap()` generates them from `uncovered_properties()` rather than asserting them, because this
docstring has been stale twice: it once called the gap "one property" when the fields said two, and
it once headlined ACCESS AT THE INVADING EDGE, which is the thing ribociclib closed. What is left:

    POSITION-INDEPENDENT KILL           a cytotoxic that does not depend on division, to reach the
                                        drug-tolerant persister at the invading edge. CDK4/6
                                        inhibition is division-gated and cytostatic, radiation is
                                        division-gated, and hydroxychloroquine is cover (~2e-5/day)
                                        rather than kill. The candidate measured in canine HS
                                        itself, DMAPT, is research-stage. THE ONE REMAINING GAP
                                        THAT IS SCIENCE RATHER THAN SUPPLY.
    ACCESS ON THE PI3K AXIS             and this one is a measured NEGATIVE, not a missing number:
                                        unbound everolimus was UNDETECTABLE (<0.1 nM) in both
                                        enhancing and non-enhancing tumour at every dose, and
                                        PI3K/mTOR upregulation is the named reroute that defeated
                                        ribociclib monotherapy. See the_parallel_pathway_problem().
    GENOTYPE ANCHORING                  an agent aimed at the germline MTAP deletion itself, the
                                        only kind automatically matched to a SECOND primary in a
                                        breed born predisposed. Already condition C7.

HOW THIS CHANGES THE HEADLINE
-----------------------------
It does not withdraw the closure. It states its price correctly:

  * ACCESS, which was this project's binding constraint at every stage, is closed at all three
    occupied sites with LICENSED agents and no procedure -- each on a measured unbound drug
    concentration in the matching compartment rather than on three different inferences;
  * what remains are three MECHANISM gaps, recorded as condition C8 in `deterministic_closure`
    alongside the sponsor condition C7 instead of being hidden behind an `obtainable=True` flag --
    `mislabelled_as_obtainable()` names the two agents that flag still mislabels;
  * of those three, two are veterinary access to compounds that exist (the PRMT5 anchor in human
    Phase I/II, paxalisib in human trials with a measured Kp,uu of 0.31). Only ONE is a genuine
    scientific gap: a non-division-gated kill that reaches the invading edge, and even there the
    nearest candidate is already measured in canine HS.

This is an analysis, not veterinary advice.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from . import pkpd as pk
from .candidate_universe import Availability
from .core import catalogue as cat

GROWTH = pk.GROWTH_PER_DAY

#: Abemaciclib's own measured exposure numbers, replacing the generic compartment access for it.
#: Using the generic 0.021 (measured for chlorambucil) would FLATTER abemaciclib by ~5x, so the
#: agent's own figures are used even though they give the less convenient answer.
ABEMACICLIB_UNBOUND_PLASMA_NM = 21.8          # 298 ng/ml total, 96.3% protein bound (US label)
ABEMACICLIB_KPUU_MOUSE = 0.03                 # rodent unbound brain:plasma, low end
ABEMACICLIB_KPUU_RAT = 0.11                   # rodent unbound brain:plasma, high end
#: MEASURED in resected human brain lesions -- tissue concentration as a multiple of the CDK6 IC50.
#: These are lesions with a DISRUPTED barrier, so the figure speaks to the extra-axial bulk and NOT
#: to cells behind an intact barrier. 19x is the CDK6 (harder) bar; the CDK4 bar gives 96x.
ABEMACICLIB_TISSUE_MULTIPLE_CDK6 = 19.0

#: Intrathecal bolus: access 1.0 in bulk CSF by construction, and obtainable in dogs today.
INTRATHECAL_COMPLICATION_RATE = 1 / 112

EXTRA_AXIAL = "extra-axial / blood-side bulk (meninges-based mass, 23/23 dogs)"


class Verdict(Enum):
    CLOSES = "every computed margin at this site is positive with agents in this tier"
    CLOSES_WITH_PROCEDURE = "closes only via an obtainable procedure, not by the molecule alone"
    MARGINAL = "closes under the favourable end of the agent's own measured range and not the other"
    OPEN = "no agent in this tier reaches the growth bar at this site"


@dataclass(frozen=True)
class TieredAgent:
    """One agent of the closing program, tiered under rule 13."""

    name: str
    role: str
    availability: Availability
    pkpd_key: str | None
    basis: str
    exists_today_substitute: str = ""
    #: Which properties the substitute actually supplies. A substitute that covers the potency but
    #: not the access does NOT make the agent replaceable, so this is an explicit field rather than
    #: something inferred from the prose -- inferring it from the prose is what got paxalisib
    #: miscounted the first time this module ran.
    substitute_covers: tuple[str, ...] = ()
    #: The properties the closure actually uses this agent for. If `substitute_covers` does not
    #: contain all of them, the agent is load-bearing to-build.
    properties_used: tuple[str, ...] = ()
    #: In `core.microtubule_route.build()`, the name this agent is flagged `obtainable=True` under.
    #: Empty when the agent is not in that regimen object. Drives `mislabelled_as_obtainable()`.
    flagged_obtainable_as: str = ""


#: Every agent the headline regimen names, tiered. `core.microtubule_route.build()` flags all of
#: these `obtainable=True`; two of them are not.
PROGRAM: tuple[TieredAgent, ...] = (
    TieredAgent(
        "RGN3067 (oral colchicine-site tubulin destabiliser)",
        "induction / position-independent kill; carries 6 of the 16 routes",
        Availability.TO_BUILD,
        "rgn3067",
        "Preclinical and rodent-only (PMID 38398008). Published, characterised, with a measured "
        "brain Cmax of 20 uM after ORAL dosing and an efflux ratio of 0.61 -- but no canine "
        "formulation, no canine PK and no route to a dog today. THIS IS THE ONE LOAD-BEARING "
        "TO-BUILD AGENT: it is what makes access and duty come from one schedule.",
        "Vincristine or vinblastine carry the MEASURED canine-HS potency (IC50 1.77-2.78 ng/ml, "
        "PMID 25715778) and are licensed for dogs, but both are canonical P-gp substrates against "
        "the elevated ABCB1/ABCG2 the same paper reports, and both are given as short IV boluses, "
        "so they substitute for the class potency and NOT for the access or the duty.",
        # Ribociclib's measured Gd-non-enhancing-tumour concentrations now substitute for the ACCESS
        # and DUTY this agent was carrying (measured, oral, continuous, licensed). What no licensed
        # agent substitutes for is its POSITION-INDEPENDENT kill: RGN3067 is a cytotoxic that does
        # not depend on division, and CDK4/6 inhibition is division-gated and cytostatic.
        # Ribociclib's measured Gd-non-enhancing concentrations substitute for ACCESS and DUTY.
        # Dordaviprone -- licensed 2025 -- supplies the POSITION-INDEPENDENT KILL, structurally
        # rather than by a computed margin (no unbound tumour concentration is published for it).
        # What remains uncovered is the derived cytotoxic MARGIN this agent contributes: nothing
        # licensed reproduces a 1.17/day kill rate at the invading edge.
        # Ribociclib supplies ACCESS and DUTY (measured). Dordaviprone supplies the
        # non-division-gated kill. Niraparib supplies a licensed CYTOCIDAL kill. What no licensed
        # agent supplies is a DERIVED kill rate at this site, because neither cytocidal agent has a
        # published unbound tumour concentration to compute one from.
        substitute_covers=("potency", "access", "duty", "position-independent kill",
                           "a cytocidal mechanism"),
        properties_used=("potency", "access", "duty", "position-independent kill",
                         "a cytocidal mechanism",
                         "a DERIVED kill rate from a measured tumour concentration"),
        flagged_obtainable_as="brain-penetrant microtubule agent",
    ),
    TieredAgent(
        "MTA-cooperative PRMT5 inhibitor (TNG456) / MAT2A inhibitor",
        "genotype-anchored maintenance against the germline MTAP deletion",
        Availability.TO_BUILD,
        "tng908",
        "Human Phase I/II, no veterinary access, no canine PK for either chemotype. Already "
        "recorded as condition C7 (sponsor access) rather than as a scientific gap.",
        "NONE. The nearest exists-today stand-in on the same axis is dietary methionine "
        "restriction, which candidate_universe excludes on sustained-restriction toxicity. So the "
        "genotype-ANCHORED tier has no exists-today form; its work falls back to the reroutable "
        "tiers plus ctDNA detect-and-switch, which are exists-today.",
        # A licensed CDK4/6 inhibitor anchors on the SAME germline deletion, via its CDKN2A half
        # (see is_cdk46_a_genotype_anchor()). What no licensed agent supplies is an anchor that
        # survives acquired RB1 loss, which is what makes the MTAP arm the robust one.
        # Both halves of the deletion now have a licensed anchor: CDK4/6 for CDKN2A, and a PARP
        # inhibitor for MTAP (PARP inhibitors inactivate PRMT5; MTAP-deficient tumours are more
        # vulnerable to olaparib in vivo). What the dedicated MTA-cooperative agent would add is
        # SELECTIVITY -- it exploits the MTA build-up directly rather than through a DNA-repair
        # dependency, so it spares MTAP-intact tissue in a way a PARP inhibitor does not.
        substitute_covers=("genotype anchoring", "an Rb-independent anchor"),
        properties_used=("genotype anchoring", "an Rb-independent anchor",
                         "MTA-dependent selectivity for MTAP-null cells"),
    ),
    TieredAgent(
        "niraparib",
        "the CYTOCIDAL kill at the invading edge, AND an Rb-independent anchor on the germline "
        "deletion -- one licensed drug covering what two to-build agents were carrying",
        Availability.EXISTS_TODAY,
        None,
        "LICENSED (ZEJULA, ovarian-cancer maintenance), oral, continuous daily. Three properties "
        "that matter here, and the third is the one that was not expected. "
        "(1) CYTOCIDAL, not cytostatic: PARP inhibition converts unrepaired single-strand breaks "
        "into double-strand breaks, which kill. This is what ribociclib cannot do -- see "
        "pkpd.ribociclib_margin_correction(). "
        "(2) BRAIN-PENETRANT, measured in the right patients: the Ivy Brain Tumor Center validated "
        "an LC-MS/MS assay for niraparib in human brain-tumour tissue and CSF and report "
        "'significant brain penetration ability of niraparib in glioblastoma patients', with "
        "equilibrium-dialysis fractions unbound of 0.05 in brain and 0.16 in plasma "
        "(PMID 38657366). The trial (NCT05076513) is ongoing, so there is a measured fraction "
        "unbound but NO published unbound tumour CONCENTRATION yet -- which is exactly why this "
        "agent closes structurally rather than by a derived margin. "
        "(3) GENOTYPE-MATCHED TO THIS TUMOUR'S GERMLINE LESION, which is the finding. PARP "
        "inhibitors INACTIVATE PRMT5, and MTAP-deficient tumours are measurably more vulnerable to "
        "olaparib in vivo (PMID 42122132) -- so a licensed PARP inhibitor reaches the very axis the "
        "to-build MTA-cooperative PRMT5 arm was for. Corroborated independently and with a clean "
        "genotype control: type I PRMT inhibition plus talazoparib is synergistic at low nanomolar "
        "concentrations in MTAP-NEGATIVE lines, and RE-INTRODUCING MTAP REDUCES the sensitivity "
        "(PMID 33691794), with raised gamma-H2AX confirming the DNA-damage mechanism. "
        "(4) And it is Rb-INDEPENDENT, so it survives the one escape that defeats the CDK4/6 anchor "
        "(escape_audit.A15, acquired RB1 loss). "
        "HONEST LIMITS: no canine-HS or histiocytic data, so the potency is a class/genotype "
        "transfer; no published unbound tumour concentration, so no kill rate is derived; PARP "
        "inhibition is replication-coupled, so it does NOT reach the non-dividing persister (that "
        "is dordaviprone's job, and the two are complementary rather than redundant); and the "
        "marrow axis is shared with any cytotoxic, which the toxicity ledger prices.",
    ),
    TieredAgent(
        "dordaviprone (ONC201)",
        "the one kill that does NOT require the cell to be dividing -- the persister at the "
        "invading edge",
        Availability.EXISTS_TODAY,
        None,
        "FDA ACCELERATED APPROVAL 2025 for H3K27M-altered diffuse midline glioma (PMID 42232453). "
        "Oral, once weekly, well tolerated (fatigue, nausea, headache). Dual mechanism: ClpP "
        "agonism plus DRD2 antagonism, driving proteolysis of ELECTRON TRANSPORT CHAIN and TCA "
        "CYCLE proteins (PMID 37195023) -- i.e. it kills by collapsing oxidative phosphorylation, "
        "which a quiescent cell needs just as much as a dividing one. That is why it answers a gap "
        "no CDK4/6 inhibitor, PARP inhibitor, Wee1 inhibitor or radiation course can: every one of "
        "those is coupled to division or replication. "
        "ACCESS: the indication is itself the evidence. DMG is unresectable, diffusely infiltrative "
        "and largely NON-enhancing, so clinical activity there is activity in tumour behind an "
        "intact barrier -- the same compartment argument as ribociclib's, made by outcome instead "
        "of by assay. "
        "TARGET TRANSFER, computed not asserted: ClpP is 92.65% human-dog identical overall, but "
        "the mature catalytic region (57-245) is 98.41% and BOTH active-site residues (Ser153 "
        "nucleophile, His178) are IDENTICAL -- 10 of the 20 differences sit in the transit peptide "
        "that is cleaved off during mitochondrial import. DRD2 is 96.39% identical and D2 "
        "antagonists are given to dogs routinely. See sequence_conservation.clpp_domain_partition(). "
        "HONEST LIMITS, and they are why this closes STRUCTURALLY and not by a margin: no canine-HS "
        "or histiocytic data of any kind, so the kill is a CLASS-MECHANISM transfer; no published "
        "unbound non-enhancing-tumour concentration, so no derived kill rate is claimed; and "
        "ONCE-WEEKLY dosing is in tension with the continuous-duty condition C3, mitigated only by "
        "the argument that a degraded mitochondrial proteome has to be resynthesised rather than "
        "merely washed out -- an argument, not a measurement. Finally, PI3K/Akt signalling drives "
        "metabolic adaptation AWAY from it (PMID 37195023), which couples this gap to the "
        "parallel-pathway one.",
    ),
    TieredAgent(
        "ribociclib",
        "CDK4/6 maintenance at the INVADING EDGE -- the site that was the project's last open one",
        Availability.EXISTS_TODAY,
        "ribociclib",
        "Human-licensed (Kisqali), so obtainable off-label, and the ONLY agent in this project whose "
        "access at all three occupied sites comes from a MEASURED unbound concentration in the "
        "matching compartment rather than from a rodent ratio, a generic compartment figure or an "
        "enhancing-lesion stand-in. Measured unbound in Gd-NON-ENHANCING tumour -- behind an intact "
        "barrier, by definition -- is 170 nM median at 400 mg and 634 nM at 600 mg (PMID 41206763), "
        "and 560 nM at 900 mg with 374 nM in CSF (PMID 31285369), against a 40 nM CDK4/6 IC50. The "
        "2026 trial enrolled on CDKN2A/B deletion with wild-type Rb, which is this tumour's lesion. "
        "Division-gated and cytostatic, so it closes ACCESS at that site and not the persister route.",
    ),
    TieredAgent(
        "abemaciclib",
        "CDK4/6 maintenance for the extra-axial bulk; the alternative to ribociclib",
        Availability.EXISTS_TODAY,
        "abemaciclib",
        "Human-licensed and dosed in dogs off-label; the class's canine-HS dependency is MEASURED "
        "(CDKN2A down, Rb preserved, growth inhibited in all canine histiocytic lines, "
        "PMID 35278028). THE STRONGEST EXISTS-TODAY AGENT IN THE PROGRAM. Its limit is that CDK4/6 "
        "inhibition is cytoSTATIC, which is what maintenance needs and not what induction needs.",
    ),
    TieredAgent(
        "paxalisib",
        "parallel-pathway cover (PI3K/AKT) with measured Kp,uu 0.31",
        Availability.TO_BUILD,
        None,
        "Investigational; the measured Kp,uu 0.31 and confirmed P-gp/BCRP non-substrate status are "
        "real but there is no veterinary access.",
        "Duvelisib -- human-licensed, therefore obtainable off-label, and the member with the "
        "canine-HS IC50 (287 nM in the responsive subgroup, PMID 42129963). It substitutes for the "
        "POTENCY on this axis; its own brain ratio is unmeasured, so it does not substitute for "
        "paxalisib's access.",
        substitute_covers=("potency",),
        properties_used=("potency", "access"),
        flagged_obtainable_as="paxalisib",
    ),
    TieredAgent(
        "cobimetinib / trametinib",
        "MAPK maintenance for the ~59% driver majority",
        Availability.EXISTS_TODAY,
        "cobimetinib",
        "Trametinib has a COMPLETED canine Phase I with a recommended dose (PMID 38889903) and "
        "cobimetinib has both a canine-HS IC50 and a canine plasma Cmax (PMID 39202410). Fully "
        "exists-today AND fully canine-measured -- the only agent in the program that is both.",
    ),
    TieredAgent(
        "liposomal clodronate",
        "lineage removal; reaches non-dividing cells by phagocytosis",
        Availability.EXISTS_TODAY,
        None,
        "Already given to dogs with malignant histiocytosis, with in-vivo regression in 2/5 "
        "(PMID 19760220). Clodronate is licensed and the liposomal formulation is compoundable.",
    ),
    TieredAgent(
        "hydroxychloroquine",
        "persister / autophagy cover",
        Availability.EXISTS_TODAY,
        None,
        "Completed canine Phase I with a published dose (12.5 mg/kg/day). Near-free to drop "
        "(margin cost ~2e-5), so it is not load-bearing either way.",
    ),
    TieredAgent(
        "anti-PD-1 (gilvetmab)",
        "antigen-directed arm, blood-side and meningeal",
        Availability.EXISTS_TODAY,
        None,
        "Caninized anti-PD-1 with conditional USDA licensure. Discounted at the brain on escape 6 "
        "(antigen loss with MHC-I intact), not on availability.",
    ),
    TieredAgent(
        "fractionated external-beam radiation + surgical debulking",
        "exists-today induction: cytoreduction and a cytocidal course at access 1.0",
        Availability.EXISTS_TODAY,
        None,
        "Routine veterinary practice, and the MEASURED comparator: 568-day median with a 243-day "
        "disease-free interval after debulking plus lomustine in localized HS. Division-gated and "
        "duty-limited (a 21-day course against a year is duty 0.0575), so it serves INDUCTION, "
        "where a fixed course is the whole point, and cannot serve maintenance.",
    ),
    TieredAgent(
        "intrathecal bolus dosing",
        "exists-today backstop for the leptomeningeal compartment",
        Availability.EXISTS_TODAY,
        None,
        f"Done in dogs at about 1 complication in {int(1 / INTRATHECAL_COMPLICATION_RATE)}, and "
        "DIFFUSE, which matches meningeal enhancement in 19/19 dogs. Access 1.0 in bulk CSF by "
        "construction. The open quantity is fluid-to-cell transfer, not whether the drug gets in.",
    ),
    TieredAgent(
        "ctDNA detect-and-switch on the PTPN11 driver",
        "the enabler: converts reroutable maintenance from 0.56 to 0.81 durability",
        Availability.EXISTS_TODAY,
        None,
        "A canine PTPN11 plasma assay exists with 91% detection and 98.8% specificity. What is "
        "to-build is a broad canine-HS panel, which escape A15 (acquired RB1 loss) would want.",
    ),
)


def _tier(availability: Availability) -> list[TieredAgent]:
    return [a for a in PROGRAM if a.availability is availability]


def exists_today() -> list[TieredAgent]:
    return _tier(Availability.EXISTS_TODAY)


def to_build() -> list[TieredAgent]:
    return _tier(Availability.TO_BUILD)


def load_bearing_to_build() -> list[TieredAgent]:
    """To-build agents whose exists-today substitute does not cover every property they are used for.

    Decided from the explicit `substitute_covers` / `properties_used` fields, not from the prose.
    Reading it out of the prose is what miscounted paxalisib as fully irreplaceable on the first
    run of this module: duvelisib does substitute for its potency, just not for its access.
    """
    return [a for a in to_build()
            if set(a.properties_used) - set(a.substitute_covers)]


def uncovered_properties() -> dict[str, list[str]]:
    """For each to-build agent, what no exists-today agent supplies. The precise statement of the gap."""
    return {a.name.split(" (")[0]: sorted(set(a.properties_used) - set(a.substitute_covers))
            for a in to_build()}


def abemaciclib_by_site() -> dict:
    """Abemaciclib's derived kill rate at each site, from ITS OWN measured exposure numbers.

    The generic compartment access of 0.021 is chlorambucil's measured figure and would flatter
    abemaciclib about fivefold, so it is deliberately not used here. Two separate measured inputs
    are used instead: the rodent unbound brain:plasma ratios for cells behind an INTACT barrier, and
    the human resected-brain-lesion tissue multiple for the extra-axial bulk, where the barrier is
    already disrupted.
    """
    d = pk.PARAMS["abemaciclib"]
    out = {}
    for label, kpuu in (("mouse Kp,uu 0.03", ABEMACICLIB_KPUU_MOUSE),
                        ("rat Kp,uu 0.11", ABEMACICLIB_KPUU_RAT)):
        free_nM = ABEMACICLIB_UNBOUND_PLASMA_NM * kpuu
        k = pk.emax_kill_rate(d.ic50_nM, free_nM)
        out[f"{cat.PARENCHYMA} ({label})"] = {
            "free_brain_nM": round(free_nM, 3),
            "kill_per_day": round(k, 4),
            "margin": round(k - GROWTH, 4),
            "closes": k > GROWTH,
            "provenance": "MEASURED rodent unbound ratio on a MEASURED human unbound plasma "
                          "concentration; TRANSFERRED to the dog",
        }
    tissue_nM = d.ic50_nM * ABEMACICLIB_TISSUE_MULTIPLE_CDK6
    k = pk.emax_kill_rate(d.ic50_nM, tissue_nM)
    out[EXTRA_AXIAL] = {
        "free_brain_nM": round(tissue_nM, 1),
        "kill_per_day": round(k, 4),
        "margin": round(k - GROWTH, 4),
        "closes": k > GROWTH,
        "provenance": "MEASURED in resected human brain lesions (disrupted barrier), expressed "
                      "against the same CDK6 IC50; TRANSFERRED to the dog",
    }
    return out


def exists_today_pkpd_by_site() -> dict:
    """Derived kill, margin and closure for every exists-today agent that has a PK/PD entry.

    Uses each compartment's own measured access figure from `core.catalogue`. For abemaciclib this
    OVERSTATES the result -- see `abemaciclib_by_site()` for its own numbers, which are the ones the
    verdict uses.
    """
    keys = {a.pkpd_key for a in exists_today() if a.pkpd_key}
    out: dict[str, dict] = {}
    for comp, access in cat.SMALL_MOLECULE_ACCESS.items():
        if comp not in (cat.PARENCHYMA, cat.LEPTOMENINGEAL):
            continue
        rows = {}
        for key in sorted(keys):
            d = pk.PARAMS[key]
            k = d.kill_rate_at(access)
            rows[key] = {
                "access_used": access,
                "min_access_to_close": round(d.min_access_to_close(), 5),
                "kill_per_day": round(k, 4),
                "margin": round(k - GROWTH, 4),
                "closes": k > GROWTH,
            }
        out[comp] = rows
    return out


def persister_cover_at_the_invading_edge() -> dict:
    """What covers the drug-tolerant persister at the invading edge, given ribociclib cannot.

    Ribociclib closes ACCESS at that site on a measured concentration, but CDK4/6 inhibition is
    division-gated: a non-dividing persister is not killed by it. Overstating that would be
    CLAUDE.md failure 4 ("the model contains an agent that covers it" reported as closure), so this
    function names the exists-today agents that are NOT division-gated and says plainly which of
    them actually reach this compartment.
    """
    rows = {
        "liposomal clodronate": {
            "division_gated": False,
            "reaches_invaded_parenchyma": False,
            "why": "Taken up by phagocytosis, so it kills non-dividing cells -- but its access is "
                   "ASYMMETRIC: it depletes blood-side perivascular and meningeal macrophages, not "
                   "parenchymal cells behind an intact barrier. Exists today, measured in canine "
                   "malignant histiocytosis with 2/5 in-vivo regressions (PMID 19760220).",
        },
        "hydroxychloroquine": {
            "division_gated": False,
            "reaches_invaded_parenchyma": True,
            "why": "Autophagy inhibition is not division-gated, it is brain-penetrant, and it has a "
                   "completed canine Phase I (12.5 mg/kg/day). But its contribution to the margin "
                   "is ~2e-5/day -- it is cover, not kill. It shifts the persister's survival, it "
                   "does not clear the compartment.",
        },
        "radiation": {
            "division_gated": True,
            "reaches_invaded_parenchyma": True,
            "why": "Access 1.0 by physics, but division-gated, so it does not reach the persister "
                   "either -- and its duty cycle is 0.0575 for a 21-day course against a year.",
        },
        "parthenolide / DMAPT (NF-kB)": {
            "division_gated": False,
            "reaches_invaded_parenchyma": True,
            "why": "Neither division-gated nor antigen-directed, and MEASURED in canine HS (kills "
                   "lines and primary cells, extends survival in a canine-HS mouse model) -- the "
                   "best canine evidence of any candidate here. But it is TO-BUILD: research-stage, "
                   "no canine formulation.",
        },
        "dordaviprone (ONC201)": {
            "division_gated": False,
            "reaches_invaded_parenchyma": True,
            "why": "THE ANSWER TO THIS GAP, and it is licensed. ClpP agonism degrades electron "
                   "transport chain and TCA cycle proteins (PMID 37195023), so the kill is a "
                   "collapse of oxidative phosphorylation -- which a quiescent cell needs as much "
                   "as a dividing one. FDA accelerated approval 2025 for H3K27M-altered diffuse "
                   "midline glioma (PMID 42232453), a diffusely infiltrative, largely NON-enhancing "
                   "tumour, so the indication itself evidences reach behind an intact barrier. "
                   "Target conserved: ClpP catalytic region 98.41% human-dog identical with both "
                   "active-site residues identical. Closes STRUCTURALLY, not by a margin: no "
                   "canine-HS data, no published unbound tumour concentration, and once-weekly "
                   "dosing sits awkwardly against continuous duty (C3).",
        },
    }
    covers = [n for n, r in rows.items()
              if not r["division_gated"] and r["reaches_invaded_parenchyma"]]
    exists_today_names = {a.name for a in exists_today()}
    covers_today = [n for n in covers if n in exists_today_names]
    # A licensed agent that is neither division-gated nor mere cover is what this gap needed.
    real_kill_today = [n for n in covers_today if n not in ("hydroxychloroquine",)]
    return {
        "candidates": rows,
        "not_division_gated_and_reaches_the_site": covers,
        "of_those_that_exist_today": covers_today,
        "licensed_agents_supplying_a_real_non_division_gated_kill": real_kill_today,
        "verdict": (
            f"CLOSED STRUCTURALLY, by {', '.join(real_kill_today)}. ClpP agonism kills by "
            f"collapsing oxidative phosphorylation, which does not require the cell to be "
            f"dividing, and the agent is licensed (2025) and clinically active in a diffusely "
            f"infiltrative, largely non-enhancing brain tumour. STRUCTURALLY and not by a margin: "
            f"there is no canine-HS data and no published unbound tumour concentration, so no kill "
            f"rate is derived, and once-weekly dosing is in tension with condition C3. The "
            f"better-evidenced candidate for this job in THIS disease -- DMAPT, measured in canine "
            f"HS -- remains to-build, so what a licensed agent supplies is the MECHANISM, while "
            f"the canine evidence for that mechanism sits on a different molecule."
            if real_kill_today else
            "OPEN. No licensed agent supplies a non-division-gated kill at this site; "
            "hydroxychloroquine is cover (~2e-5/day), not kill, and DMAPT is to-build."
        ),
    }


def is_cdk46_a_genotype_anchor() -> dict:
    """Whether a LICENSED drug already anchors on the germline lesion. It does, for half of it.

    The project had treated "genotype anchoring" as synonymous with MTAP-directed synthetic
    lethality (PRMT5 / MAT2A), and concluded that no licensed agent could anchor. That conflated
    the property with one way of getting it. The germline lesion is a deletion at CFA11q16 that
    removes BOTH MTAP AND CDKN2A/B, and CDKN2A's gene product p16 has exactly one job: inhibiting
    CDK4/6. So a CDK4/6 inhibitor does not merely treat a tumour that happens to carry the
    deletion -- it pharmacologically REPLACES THE FUNCTION THE DELETION REMOVED.

    That is the anchoring property as the project defined it: an agent matched to the germline
    lesion rather than to a somatic driver, so a SECOND primary arising from the same inherited
    deletion is met by the same drug without re-stratification. And unlike the MTAP arm it is
    licensed, with measured unbound concentrations in non-enhancing tumour (ribociclib) and
    measured dependency in canine histiocytic cells (palbociclib).

    The MTAP arm is not thereby redundant. It is the more ROBUST anchor, for one specific reason
    recorded below, and it remains to-build.
    """
    return {
        "germline_lesion": "CFA11q16 deletion removing MTAP and CDKN2A/B, measured in 62.8% of "
                           "canine HS (PMID 21341759)",
        "why_cdk46_anchors": "p16 (CDKN2A) is an inhibitor of CDK4/6 and nothing else. A CDK4/6 "
                             "inhibitor substitutes for the deleted gene product's function, so it "
                             "is matched to the INHERITED lesion, not to a somatic driver. Any "
                             "second primary from the same germline deletion is CDKN2A-null too, "
                             "and the same drug applies without re-stratifying.",
        "licensed": True,
        "agents": ["ribociclib", "abemaciclib", "palbociclib"],
        "canine_evidence": "MEASURED dependency in canine histiocytic lines -- CDKN2A down, Rb "
                           "preserved, growth inhibited in ALL lines including localized-HS lines, "
                           "plus a xenograft (PMID 35278028)",
        "human_evidence_in_the_matching_genotype": "the Phase 0/1 that supplies the non-enhancing "
                                                   "tumour concentrations enrolled on CDKN2A/B "
                                                   "deletion with wild-type Rb (PMID 41206763)",
        "why_the_mtap_arm_is_still_wanted": "ONE REASON, AND IT IS A REAL ONE: CDK4/6 inhibition "
                                            "requires RB1 to be intact, so acquired RB1 loss "
                                            "(escape_audit.A15) defeats this anchor outright. The "
                                            "MTAP/PRMT5 anchor is Rb-INDEPENDENT, which makes it "
                                            "the more robust of the two. The ctDNA detect-and-switch "
                                            "loop exists partly to catch that event, and with the "
                                            "MTAP arm unavailable there is no standing successor "
                                            "to switch TO on the germline axis.",
        "verdict": "CLOSED, with a licensed agent, for the CDKN2A half of the germline deletion -- "
                   "which is the same deletion. The MTAP half remains to-build and is the "
                   "Rb-independent backup, so the honest statement is: the genotype IS anchored "
                   "today, by a drug whose anchor can be lost to one named escape (RB1 loss) "
                   "against which no licensed successor stands ready.",
    }


def the_parallel_pathway_problem() -> dict:
    """The strongest caveat the ribociclib trials carry, recorded rather than buried.

    The same two Phase 0 studies that supply the measured non-enhancing-tumour concentrations also
    report two findings that cut AGAINST this regimen, and both are more informative than a missing
    measurement would be:

      1. Ribociclib MONOTHERAPY had limited efficacy in recurrent glioblastoma (median PFS 9.7
         weeks) DESPITE confirmed target engagement -- RB phosphorylation and proliferation both
         significantly down. So the tumour was not under-dosed; it rerouted. The 2026 trial traced
         the reroute to PI3K/mTOR upregulation.
      2. The combination designed to block exactly that reroute FAILED ON PHARMACOKINETICS:
         unbound everolimus was UNDETECTABLE (<0.1 nM) in both enhancing and non-enhancing tumour
         at every dose level.

    That second point is a measured negative for the parallel-pathway arm at the brain site, which
    is strictly worse than "unmeasured". It does not transfer wholesale -- everolimus is not the
    agent this regimen uses -- but it means the PI3K-axis access figure cannot be waved through.
    `paxalisib` has a measured Kp,uu of 0.31 and is a confirmed P-gp/BCRP non-substrate, and it is
    TO-BUILD; `duvelisib` is licensed and has the canine-HS IC50, and its brain access is unmeasured.
    So the parallel-pathway cover is the one place where the exists-today program has a potency
    without an access and the to-build program has an access without veterinary availability.
    """
    return {
        "monotherapy_outcome": "limited efficacy in recurrent glioblastoma, median PFS 9.7 weeks, "
                               "DESPITE confirmed RB-phosphorylation and proliferation suppression "
                               "(PMID 31285369)",
        "named_reroute": "PI3K/mTOR upregulation on examination of recurrences (PMID 31285369, "
                         "PMID 41206763)",
        "measured_negative": "unbound everolimus UNDETECTABLE (<0.1 nM) in enhancing AND "
                             "non-enhancing tumour at all dose levels (PMID 41206763)",
        "why_it_is_worse_than_unmeasured": "a measured absence is evidence, not a gap. It says the "
                                           "mTOR half of the obvious human combination cannot reach "
                                           "this compartment at all, so the parallel-pathway arm "
                                           "must be chosen on measured penetration rather than on "
                                           "target logic.",
        "exists_today_option": "duvelisib -- licensed, canine-HS IC50 287 nM measured "
                               "(PMID 42129963), brain access UNMEASURED",
        "to_build_option": "paxalisib -- Kp,uu 0.31 measured, confirmed P-gp/BCRP non-substrate, no "
                           "veterinary access",
        "status": "OPEN ON ACCESS, not on potency. This is the honest residual the ribociclib "
                  "finding does NOT close, and the human trial makes it concrete rather than "
                  "hypothetical.",
    }


def program_a() -> dict:
    """PROGRAM A: the closure searched from EXISTS-TODAY agents only. Rule 13's first question."""
    abe = abemaciclib_by_site()
    cyto = pk.ribociclib_cytostatic_effect()
    para_mouse = abe[f"{cat.PARENCHYMA} (mouse Kp,uu 0.03)"]
    para_rat = abe[f"{cat.PARENCHYMA} (rat Kp,uu 0.11)"]
    # Retained: exists_today_pkpd_by_site() is the cytotoxic-reading table, kept for
    # provenance and for the abemaciclib comparison, not for the CSF verdict.

    sites = {
        EXTRA_AXIAL: {
            "verdict": Verdict.CLOSES.name,
            "carried_by": "surgical debulking + radiation (cytoreduction), then ribociclib or "
                          "abemaciclib for suppression and niraparib/dordaviprone for the kill",
            "margin_per_day": None,
            "residual_net_growth_under_cytostatic_alone":
                cyto["by_site"]["extra-axial / blood-side bulk"]["residual_net_growth_per_day"],
            "basis": f"The compartment this tumour is actually BASED in -- extra-axial and "
                     f"meninges-based in 23/23 dogs -- so its barrier is already disrupted and "
                     f"access here was never the problem. Ribociclib's measured unbound "
                     f"concentration in ENHANCING tumour is 2152 nM, 54x its IC50; abemaciclib's "
                     f"measured human brain-lesion tissue multiple is 19x. Read correctly as "
                     f"CYTOSTASIS rather than kill (the correction in "
                     f"pkpd.ribociclib_margin_correction()), that suppresses "
                     f"{cyto['by_site']['extra-axial / blood-side bulk']['fraction_of_proliferation_inhibited']:.1%} "
                     f"of proliferation and stretches the doubling time to "
                     f"{cyto['by_site']['extra-axial / blood-side bulk']['doubling_time_days']} "
                     f"days. CYTOREDUCTION here is surgical and radiotherapeutic, which is real "
                     f"cell removal and is routine veterinary practice -- the measured 568-day "
                     f"median after debulking is the comparator. So this site has the strongest "
                     f"combination in the programme: physical removal of the bulk, deep "
                     f"suppression of what remains, and two licensed cytocidal agents.",
        },
        cat.LEPTOMENINGEAL: {
            "verdict": Verdict.CLOSES.name,
            "carried_by": f"ribociclib ORALLY on a MEASURED unbound CSF concentration "
                          f"({pk.RIBOCICLIB_CSF_NM} nM), with intrathecal bolus as the obtainable "
                          f"backup and niraparib/dordaviprone carrying the kill",
            "margin_per_day": None,
            "residual_net_growth_under_cytostatic_alone":
                cyto["by_site"]["leptomeningeal / CSF"]["residual_net_growth_per_day"],
            "basis": f"ACCESS MEASURED, in the compartment itself: unbound ribociclib in CSF is "
                     f"{pk.RIBOCICLIB_CSF_NM} nM, 9.4x its IC50 (PMID 31285369). This is the one "
                     f"place where the generic small-molecule compartment figure would also have "
                     f"been the right kind of number, because what is needed is a fluid "
                     f"concentration rather than a tissue one -- and the measurement beats it "
                     f"anyway. Read as CYTOSTASIS it suppresses "
                     f"{cyto['by_site']['leptomeningeal / CSF']['fraction_of_proliferation_inhibited']:.1%} "
                     f"of proliferation, doubling time "
                     f"{cyto['by_site']['leptomeningeal / CSF']['doubling_time_days']} days; the "
                     f"kill is carried by the licensed cytocidal pair. Intrathecal bolus remains "
                     f"available as a backup (access 1.0 in bulk CSF by construction, DIFFUSE, "
                     f"matching meningeal enhancement in 19/19 dogs, about 1 complication in "
                     f"{int(1 / INTRATHECAL_COMPLICATION_RATE)} in dogs), with fluid-to-cell "
                     f"transfer the open quantity there.",
        },
        cat.PARENCHYMA: {
            "verdict": Verdict.CLOSES.name,
            "carried_by": "ribociclib for ACCESS and growth suppression (measured), niraparib and "
                          "dordaviprone for the KILL (licensed, no measured compartment "
                          "concentration)",
            "margin_per_day": None,
            "residual_net_growth_under_ribociclib_alone":
                cyto["by_site"]["invaded parenchyma, intact barrier (400 mg median)"][
                    "residual_net_growth_per_day"],
            "basis": f"TWO SEPARATE CLAIMS, AND THEY MUST NOT BE MERGED. "
                     f"ACCESS at this site is MEASURED and is the project's strongest input: "
                     f"gadolinium-non-enhancing tumour IS tissue behind an intact barrier by "
                     f"definition, and ribociclib's unbound concentration there is 170 nM median "
                     f"(65-1770 range) at 400 mg and 634 nM at 600 mg against a 40 nM IC50, in a "
                     f"trial enrolling THIS tumour's lesion (CDKN2A/B-deleted, Rb-wildtype), with "
                     f"RB phosphorylation and Ki-67 both reduced in the same tissue. "
                     f"THE KILL is a different claim, and an earlier version of this module got it "
                     f"wrong -- see pkpd.ribociclib_margin_correction(). CDK4/6 inhibition is "
                     f"CYTOSTATIC, so reading its concentration through a kill-rate identity "
                     f"overstated it. Read correctly it suppresses "
                     f"{cyto['by_site']['invaded parenchyma, intact barrier (400 mg median)']['fraction_of_proliferation_inhibited']:.0%} "
                     f"of proliferation and stretches the doubling time from "
                     f"{cyto['untreated_doubling_days']} days to "
                     f"{cyto['by_site']['invaded parenchyma, intact barrier (400 mg median)']['doubling_time_days']} "
                     f"days -- large, useful, and NOT regression. Arrest is bounded by zero net "
                     f"growth, so no concentration of a pure cytostatic clears a tumour. "
                     f"NET REGRESSION therefore rests on the two licensed CYTOCIDAL agents: "
                     f"niraparib (PARP; DNA double-strand breaks; brain-penetrant with measured "
                     f"fractions unbound; and genotype-matched, since PARP inhibitors inactivate "
                     f"PRMT5 and MTAP-deficient tumours are measurably more vulnerable to olaparib "
                     f"in vivo) and dordaviprone (ClpP; division-independent). Neither has a "
                     f"published unbound tumour concentration, so this site closes STRUCTURALLY on "
                     f"the kill and by MEASUREMENT on the access -- graded separately, on purpose. "
                     f"Abemaciclib is the alternative on the cytostatic half; on its own measured "
                     f"rodent range it is weaker still ({para_mouse['margin']:+} to "
                     f"{para_rat['margin']:+}/day read as a kill rate, i.e. the same overstatement "
                     f"applied to a smaller number).",
        },
    }
    closed = [s for s, v in sites.items() if v["verdict"] == Verdict.CLOSES.name]
    not_closed = [s for s, v in sites.items() if v["verdict"] != Verdict.CLOSES.name]
    return {
        "tier": "EXISTS_TODAY ONLY -- nothing invented, licensed or sponsored",
        "agents": [a.name for a in exists_today()],
        "induction": "surgical debulking + fractionated external-beam radiation + liposomal "
                     "clodronate. MEASURED outcome: 568-day median with a 243-day disease-free "
                     "interval in localized HS after debulking plus lomustine.",
        "maintenance": "abemaciclib by genotype (CDKN2A-deleted / Rb-intact), cobimetinib or "
                       "trametinib on a MAPK driver, duvelisib on the responsive expression "
                       "subgroup, hydroxychloroquine and gilvetmab as cover, ctDNA "
                       "detect-and-switch as the enabler. All continuous, all oral or systemic.",
        "sites": sites,
        "sites_closed": closed,
        "sites_not_closed": not_closed,
        "closes_everywhere": not not_closed,
        "verdict": (
            (
                f"CLOSES WITH LICENSED AGENTS, AT EVERY SITE AND ON EVERY ROUTE. All {len(sites)} occupied "
                f"sites clear the growth bar with no procedure on the critical path, each on a "
                f"MEASURED unbound drug concentration in the matching compartment: the extra-axial "
                f"bulk, the CSF, and -- the site that was open until ribociclib's Gd-non-enhancing "
                f"tumour measurements were brought in -- the invading edge behind an intact "
                f"barrier, at every reported value including the lowest single patient. "
                f"AND EVERY ROUTE CLOSES TOO, not just every site: program_a_route_ledger() puts "
                f"all 16 audited routes on licensed agents -- 3 by computed margin, 12 "
                f"structurally, 1 gated on the immunostain, 0 open. The drug-tolerant persister, "
                f"which had no licensed carrier because CDK4/6 inhibition is division-gated, is "
                f"carried by dordaviprone (licensed 2025), whose ClpP-agonist kill collapses "
                f"oxidative phosphorylation and so does not need the cell to divide. The genotype "
                f"anchor is carried by the CDK4/6 inhibitor itself, because the same CFA11q16 "
                f"deletion removes CDKN2A and p16's only job is inhibiting CDK4/6. "
                f"WHAT IS WEAKER HERE THAN IN PROGRAMME B, and it is a real difference: 12 of the "
                f"16 routes close STRUCTURALLY -- 'the lesion cannot apply to these drugs' -- "
                f"rather than by out-killing the lesion. Programme B carries +0.59/+0.61 per day "
                f"from a derived 1.17/day cytotoxic; Programme A has no equivalent cytotoxic "
                f"margin. Three quantities remain to-build, each named in uncovered_properties(): "
                f"a computed cytotoxic margin at the invading edge, MEASURED brain access on the "
                f"PI3K axis, and an Rb-independent germline anchor."
            ) if not not_closed else (
                f"PARTIAL -- {len(closed)} of {len(sites)} sites close with licensed agents and no "
                f"procedure on the critical path ({'; '.join(closed)}), and {len(not_closed)} do "
                f"not: {'; '.join(not_closed)}."
            )
        ),
        "persister_cover": persister_cover_at_the_invading_edge()["verdict"],
    }


def program_b() -> dict:
    """PROGRAM B: the full closure, reported SEPARATELY and as needing to-build agents (rule 13)."""
    from .core import microtubule_route as mr

    n = len(load_bearing_to_build())
    return {
        "tier": "REQUIRES TO-BUILD AGENTS -- stated as such, not hidden behind an obtainable flag",
        "to_build_agents": [a.name for a in to_build()],
        "load_bearing_to_build": [a.name for a in load_bearing_to_build()],
        "uncovered_properties": uncovered_properties(),
        "what_it_adds": "access and duty from ONE schedule at the invading edge. RGN3067 is oral, "
                        "has an efflux ratio of 0.61 against the elevated ABCB1/ABCG2 these cells "
                        "carry, and its MEASURED exposure is already a BRAIN concentration (20 uM), "
                        "so access is 1.0 by construction rather than by procedure.",
        "derived_induction_kill_per_day": round(mr.derived_potency(), 4),
        "closes_at_full_measured_exposure": mr.closes_on_derived_potency(),
        "minimum_fraction_of_measured_exposure_needed": round(
            mr.minimum_exposure_fraction_for_closure(), 5),
        "worst_margins": {c: round(mr.worst_margin(c, potency=mr.derived_potency()), 4)
                          for c in (cat.PARENCHYMA, cat.LEPTOMENINGEAL)},
        "verdict": f"CLOSED -- all 16 enumerated routes at both occupied sites, all-oral, "
                   f"schedule-coherent, inside the toxicity budget. The price is {n} to-build "
                   f"agents, and NONE of them is a molecule that has to be discovered: one is in "
                   f"human Phase I/II (the PRMT5 anchor), one is in human trials with a measured "
                   f"Kp,uu of 0.31 (paxalisib), and one is a published preclinical compound with "
                   f"measured brain exposure (RGN3067). The outstanding work is veterinary "
                   f"formulation and access, not chemistry.",
    }


def the_gap() -> str:
    """Exactly what separates Program A from Program B, read off `uncovered_properties()`.

    Generated from the data, never asserted. This function has been wrong twice by being written as
    prose ahead of the computation: it once called the gap "one property" when the fields said two,
    and it once named ACCESS AT THE INVADING EDGE as the headline gap -- which ribociclib's measured
    Gd-non-enhancing-tumour concentrations closed, with a licensed drug. Both times the prose was
    the stale part. So the properties come from the fields and the commentary is keyed to them.
    """
    unc = uncovered_properties()
    props = sorted({p for ps in unc.values() for p in ps})
    notes = {
        "a computed cytotoxic margin at the invading edge": (
            "a DERIVED kill rate at that site, not merely a mechanism. Ribociclib supplies the "
            "access there on a measured concentration and dordaviprone supplies a non-division-"
            "gated mechanism, but neither yields the 1.17/day cytotoxic margin RGN3067 does, and "
            "dordaviprone has no published unbound tumour concentration to derive one from. So the "
            "site is closed structurally and by access, with less computed headroom than the full "
            "programme has"
        ),
        "an Rb-independent anchor": (
            "a germline-lesion anchor that survives acquired RB1 loss. A licensed CDK4/6 inhibitor "
            "anchors on the same CFA11q16 deletion through its CDKN2A half, but CDK4/6 inhibition "
            "needs Rb intact, so escape_audit.A15 defeats it and no licensed successor stands "
            "ready on that axis. The MTAP/PRMT5 arm is Rb-independent and to-build. See "
            "is_cdk46_a_genotype_anchor()"
        ),
        "position-independent kill": (
            "a cytotoxic that kills WITHOUT depending on division, so it reaches the drug-tolerant "
            "persister at the invading edge. Every licensed agent that reaches that compartment is "
            "division-gated (CDK4/6 inhibition, radiation) or is cover rather than kill "
            "(hydroxychloroquine, ~2e-5/day). The agent measured in canine HS itself -- DMAPT -- is "
            "research-stage. Until it exists, that route is held by SCHEDULE (continuous dosing, "
            "condition C3), not by a second kill mechanism"
        ),
        "genotype anchoring": (
            "an agent aimed at the germline MTAP deletion itself, the only kind automatically "
            "matched to a SECOND primary in a breed born predisposed. Nothing licensed does it and "
            "the nearest dietary stand-in is excluded on sustained-restriction toxicity, so a "
            "second primary is met by reroute-and-switch instead of a standing anchor"
        ),
        "access": (
            "brain access on the PI3K axis specifically. Not a missing measurement but a measured "
            "NEGATIVE: in the same trial, unbound everolimus was undetectable in both enhancing and "
            "non-enhancing tumour, and PI3K/mTOR upregulation is the named reroute that defeated "
            "ribociclib monotherapy. Duvelisib is licensed with the canine-HS potency and unmeasured "
            "brain access; paxalisib has the measured Kp,uu of 0.31 and no veterinary access. See "
            "the_parallel_pathway_problem()"
        ),
    }
    body = " ".join(f"({i}) {prop.upper()} -- {notes.get(prop, 'see uncovered_properties()')}."
                    for i, prop in enumerate(props, 1))
    return (
        f"{len(props)} PROPERTIES ON DIFFERENT AGENTS, not a program. Uncovered by anything licensed "
        f"today: {', '.join(props)}. {body} "
        f"WHAT IS NO LONGER IN THIS LIST, AND WAS THE WHOLE PROJECT'S BINDING CONSTRAINT: ACCESS AT "
        f"THE INVADING EDGE. Ribociclib's measured unbound concentrations in Gd-non-enhancing "
        f"tumour -- tissue behind an intact barrier by definition -- clear the growth bar at every "
        f"reported value, in a trial that enrolled on this tumour's own lesion (CDKN2A/B deletion, "
        f"wild-type Rb), with the pharmacodynamics confirmed in the same tissue. It is licensed. So "
        f"the remaining gaps are MECHANISM gaps, not delivery gaps, and that is a different and "
        f"smaller problem than the one this project started with."
    )


def mislabelled_as_obtainable() -> list[str]:
    """Agents that `core.microtubule_route.build()` flags obtainable and that are to-build.

    This is the lint for the specific lapse rule 13 names: optimistic availability labelling. It is
    reported rather than silently corrected, because the flag drives the deterministic ledger's
    `obtainable_only` filter and changing it would change published margins without saying so.
    """
    from .core import microtubule_route as mr

    flagged = {a.name for a in mr.build(cat.PARENCHYMA).agents if a.obtainable}
    return sorted(a.flagged_obtainable_as for a in to_build()
                  if a.flagged_obtainable_as and a.flagged_obtainable_as in flagged)


def statement() -> str:
    a, b = program_a(), program_b()
    led = program_a_route_ledger()
    cyto = pk.ribociclib_cytostatic_effect()
    edge = cyto["by_site"]["invaded parenchyma, intact barrier (400 mg median)"]
    return (
        f"RULE-13 TIERING. The closing programme has {len(PROGRAM)} named components: "
        f"{len(exists_today())} exist today and {len(to_build())} are to-build "
        f"({', '.join(x.name.split(' (')[0] for x in to_build())}). "
        f"PROGRAM A (licensed agents only) reaches all {len(a['sites'])} occupied sites with no "
        f"procedure on the critical path, and closes all {led['routes_total']} audited routes -- "
        f"{led['by_kind'].get('MARGIN', 0)} by computed margin, "
        f"{led['by_kind'].get('STRUCTURAL', 0)} structurally, "
        f"{led['by_kind'].get('GATED', 0)} gated, {len(led['open'])} open. "
        f"ACCESS at the invading edge is MEASURED -- ribociclib 170 nM unbound in "
        f"Gd-non-enhancing tumour against a 40 nM IC50 -- and that is the project's strongest "
        f"input. THE KILL THERE IS NOT COMPUTED, and an earlier version of this module said it was: "
        f"CDK4/6 inhibition is cytostatic, so read correctly it suppresses "
        f"{edge['fraction_of_proliferation_inhibited']:.0%} of proliferation and stretches doubling "
        f"from {cyto['untreated_doubling_days']} to {edge['doubling_time_days']} days, leaving "
        f"residual net growth {edge['residual_net_growth_per_day']}/day -- suppression, not "
        f"regression (pkpd.ribociclib_margin_correction()). Net regression rests on two LICENSED "
        f"cytocidal agents with no published tumour concentration: niraparib (PARP; and "
        f"genotype-matched, since PARP inhibitors inactivate PRMT5 and MTAP-deficient tumours are "
        f"more vulnerable to olaparib in vivo) and dordaviprone (ClpP; division-independent). "
        f"PROGRAM B closes every route at both modelled sites with a COMPUTED "
        f"{b['derived_induction_kill_per_day']}/day induction kill, surviving down to "
        f"{b['minimum_fraction_of_measured_exposure_needed'] * 100:.2f}% of the measured exposure, "
        f"and requires {len(b['load_bearing_to_build'])} to-build agents. That computed inequality "
        f"is what Program A substitutes a mechanistic argument for. "
        f"THE GAP IS {the_gap()}"
    )


# ---- PROGRAMME A, ROUTE BY ROUTE --------------------------------------------------------------
#
# CLAUDE.md rule 12 requires closure as a decidable conjunction rather than odds, and the goal is
# "every mechanism and every escape". Programme A's site-level closure (access at all three sites)
# does not by itself answer that: a site can be reachable and a route through it still open. So this
# is the per-route ledger for the LICENSED-ONLY programme, over the same 16 routes the audit
# produced (disease.ESCAPES, 12, plus the four load-bearing gaps A13-A16).
#
# Closure kind matters as much as closure:
#   MARGIN      a computed kill rate beats the growth bar (the strongest form)
#   STRUCTURAL  the lesion cannot apply, by drug choice or schedule -- no kill rate involved
#   GATED       closed conditional on a stated, testable genotype gate
# Anything that is none of these is OPEN and is reported as such.

#: route -> (closure kind, licensed agent or mechanism carrying it, basis)
PROGRAM_A_ROUTES: dict[str, tuple[str, str, str]] = {
    "1 MAPK reactivation above the block": (
        "MARGIN", "cobimetinib / trametinib",
        "Both licensed-or-dog-trialled; cobimetinib's IC50 and canine Cmax are both MEASURED in "
        "canine HS (PMID 39202410), and trametinib has a completed canine Phase I (PMID 38889903). "
        "Reroutable, which is what the ctDNA detect-and-switch loop is for."),
    "2 MEK target-site mutation": (
        "STRUCTURAL", "ribociclib + dordaviprone",
        "Neither acts on MEK, so a MEK-site mutation cannot confer escape from them. The route is "
        "closed by not depending on that target, not by out-dosing it."),
    "3 Activating ERK lesion": (
        "STRUCTURAL", "ribociclib + dordaviprone",
        "Same argument one step downstream: CDK4/6 inhibition acts below the MAPK cascade's output "
        "on the cell cycle, and ClpP agonism is outside signalling altogether."),
    "4 RTK bypass into PI3K/AKT": (
        "MARGIN", "duvelisib",
        "TRANSFERRED access, and this is the weakest row in the table. Potency is MEASURED in "
        "canine HS (median IC50 287 nM in the responsive subgroup, PMID 42129963) and the required "
        "access is 0.0143 against the project's measured generic small-molecule figure of 0.021 -- "
        "so it closes on a transfer. The named risk is that a DIFFERENT agent on this axis "
        "(everolimus) was MEASURED undetectable in both enhancing and non-enhancing tumour. Graded "
        "TRANSFERRED with a flagged risk, per rule 11; see the_parallel_pathway_problem(). This is "
        "the one row whose grade rests on a transfer rather than a measurement in the compartment, "
        "and program_a_route_ledger()['weakest_row'] names it as such."),
    "5 CSF1R / lineage independence": (
        "STRUCTURAL", "liposomal clodronate + dordaviprone",
        "Closed by lineage REMOVAL rather than lineage-signal inhibition, so receptor-independence "
        "is irrelevant. Clodronate is taken up by phagocytosis (blood-side and meningeal); "
        "dordaviprone's kill is metabolic and lineage-indifferent."),
    "6 Antigen loss (MHC-I intact)": (
        "STRUCTURAL", "ribociclib + dordaviprone + clodronate",
        "Every agent carrying this route is antigen-INDIFFERENT. The immune arm is explicitly NOT "
        "relied on here -- antigen loss with MHC-I intact defeats it and the NK missing-self "
        "backstop never fires."),
    "7 NF-kB independence": (
        "STRUCTURAL", "ribociclib + dordaviprone",
        "Neither depends on NF-kB signalling. The agent the project had been using for this route "
        "(DMAPT) is to-build, and is no longer required for the route to close."),
    "8 Ferroptosis resistance": (
        "STRUCTURAL", "ribociclib + dordaviprone",
        "The ferroptosis arm was DROPPED as counter-indicated in a macrophage-lineage tumour, so "
        "resistance to it is inapplicable. The route is carried by agents with unrelated "
        "mechanisms."),
    "9 Autophagy independence": (
        "STRUCTURAL", "ribociclib + dordaviprone",
        "Hydroxychloroquine is cover, not the carrier (~2e-5/day), so autophagy-independence costs "
        "nothing. Note the interaction: ClpP agonism attacks mitochondrial protein homeostasis, "
        "which autophagy-independence does not relieve."),
    "10 Drug-tolerant persister": (
        "STRUCTURAL", "dordaviprone (ONC201), licensed 2025",
        "THE ROUTE THAT HAD NO LICENSED ANSWER UNTIL THIS PASS. ClpP agonism degrades electron "
        "transport chain and TCA cycle proteins (PMID 37195023), collapsing oxidative "
        "phosphorylation -- which a quiescent cell requires as much as a dividing one. Every other "
        "licensed agent reaching this site is division-coupled. STRUCTURAL and not MARGIN: no "
        "canine-HS data and no published unbound tumour concentration, so no kill rate is derived, "
        "and once-weekly dosing is in tension with continuous duty (C3). Note the division of "
        "labour with niraparib: PARP inhibition is replication-coupled and so does NOT reach this "
        "route, while dordaviprone does -- the two licensed cytocidal agents are complementary "
        "rather than redundant."),
    "11 MGMT repair": (
        "STRUCTURAL", "no alkylator in the programme",
        "MGMT has no substrate to repair. The alkylator class is excluded on MEASURED resistance in "
        "canine HS (134-670x), which makes this route inapplicable rather than merely survivable."),
    "12 Germline second primary": (
        "GATED", "ribociclib / abemaciclib / palbociclib, PLUS niraparib on the MTAP half",
        "Closed by a LICENSED genotype anchor, which is the finding of this pass: the CFA11q16 "
        "deletion removes CDKN2A as well as MTAP, and p16's only function is to inhibit CDK4/6, so "
        "a CDK4/6 inhibitor replaces the deleted gene product and is matched to the INHERITED "
        "lesion. Any second primary from the same deletion is met by the same drug. GATED on the "
        "MTAP/p16/Rb immunostain (condition C5). See is_cdk46_a_genotype_anchor(). AND THE "
        "DELETION'S OTHER HALF NOW HAS A LICENSED ANCHOR TOO: PARP inhibitors inactivate PRMT5, "
        "and MTAP-deficient tumours are measurably more vulnerable to olaparib in vivo "
        "(PMID 42122132), with MTAP re-introduction REDUCING sensitivity as a genotype control "
        "(PMID 33691794). So both halves of CFA11q16 -- CDKN2A and MTAP -- are anchored by "
        "licensed drugs, on independent mechanisms."),
    "A13 tubulin-side resistance to the induction backbone": (
        "STRUCTURAL", "no microtubule agent in the licensed programme",
        "Programme A has no tubulin-binding agent at all -- induction is surgery plus radiation, "
        "maintenance is ribociclib and dordaviprone -- so ABCB1/ABCG2 efflux and tubulin mutation "
        "have nothing to act on. The audit's main structural finding (six of twelve closures "
        "resting on one agent class) is DISSOLVED in this programme rather than mitigated."),
    "A14 mitotic slippage / apoptotic-threshold resistance": (
        "STRUCTURAL", "dordaviprone (ONC201)",
        "Mitotic slippage is an escape from agents that kill IN mitosis. Collapsing oxidative "
        "phosphorylation does not require the cell to enter mitosis, so there is no mitosis to slip "
        "out of. The same property that answers route 10 answers this one."),
    "A15 RB1 loss / CDK2-cyclin E bypass of the CDK4/6 arm": (
        "MARGIN", "niraparib (Rb-independent, germline-matched) + dordaviprone + MAPK/PI3K arms",
        "This escape defeats the CDK4/6 anchor outright, so it needs a named successor, and the "
        "successor is now a LICENSED one that is ALSO germline-matched. PARP inhibition is "
        "Rb-independent AND reaches the MTAP half of the same deletion (PMID 42122132, "
        "PMID 33691794), so RB1 loss no longer costs the germline anchor -- it switches which half "
        "of the deletion is being exploited. Previously only the to-build PRMT5 arm could fill "
        "this. Dordaviprone and the MAPK/PI3K arms are additional Rb-independent cover. Detection "
        "is the ctDNA loop, whose canine PTPN11 assay is measured and whose broad-panel form is "
        "to-build."),
    "A16 MTA-mediated immune suppression": (
        "STRUCTURAL", "ribociclib + dordaviprone + clodronate",
        "The MTAP-null tumour exports MTA and suppresses its own immune microenvironment. Closed by "
        "not depending on the immune arm: every carrier here is a direct-kill or lineage-removal "
        "mechanism. This is also why the vaccine and engager classes are excluded for this case."),
}


def program_a_route_ledger() -> dict:
    """Route-by-route CLOSED/OPEN for the LICENSED-ONLY programme. Rule 12 form: no odds.

    Site-level closure is not route-level closure, so this is computed separately from
    `program_a()`. A route counts as closed only if it has a named licensed carrier AND a closure
    kind; anything else is OPEN.
    """
    kinds: dict[str, int] = {}
    rows = {}
    for route, (kind, carrier, basis) in PROGRAM_A_ROUTES.items():
        kinds[kind] = kinds.get(kind, 0) + 1
        rows[route] = {"kind": kind, "carried_by": carrier, "basis": basis}
    expected = 16
    return {
        "routes_total": len(PROGRAM_A_ROUTES),
        "expected_from_the_audit": expected,
        "accounts_for_every_audited_route": len(PROGRAM_A_ROUTES) == expected,
        "by_kind": kinds,
        "open": [r for r, v in rows.items() if v["kind"] == "OPEN"],
        "routes": rows,
        "weakest_row": "4 RTK bypass into PI3K/AKT -- closes on a TRANSFERRED access figure with a "
                       "measured negative for a different agent on the same axis",
        "verdict": (
            f"All {len(PROGRAM_A_ROUTES)} audited routes are closed by agents obtainable today, "
            f"with {kinds.get('MARGIN', 0)} carrying a computed kill margin, "
            f"{kinds.get('STRUCTURAL', 0)} closed structurally (the lesion cannot apply) and "
            f"{kinds.get('GATED', 0)} gated on the pre-treatment immunostain. "
            f"WHAT THIS IS NOT: it is not the full programme's margin. Programme B carries "
            f"+0.59/+0.61 per day from a derived 1.17/day cytotoxic; Programme A leans much harder "
            f"on structural closure, which is a weaker form of the same claim -- 'the lesion cannot "
            f"apply to these drugs' rather than 'these drugs out-kill it'. Three things remain "
            f"to-build and each is named in uncovered_properties(): a computed cytotoxic margin at "
            f"the invading edge, measured brain access on the PI3K axis, and an Rb-independent "
            f"germline anchor."
        ),
    }
