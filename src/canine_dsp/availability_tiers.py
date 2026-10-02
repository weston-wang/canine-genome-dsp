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
        substitute_covers=("potency", "access", "duty"),
        properties_used=("potency", "access", "duty", "position-independent kill"),
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
        substitute_covers=(),
        properties_used=("genotype anchoring",),
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
            "why": "The catalogue's one small molecule that is neither division-gated nor "
                   "antigen-directed, and it is MEASURED in canine HS (kills lines and primary "
                   "cells, extends survival in a canine-HS mouse model). BUT IT IS TO-BUILD: "
                   "research-stage, no canine formulation. The cleanest statement of the residual.",
        },
    }
    covers = [n for n, r in rows.items()
              if not r["division_gated"] and r["reaches_invaded_parenchyma"]]
    exists_today_names = {a.name for a in exists_today()}
    covers_today = [n for n in covers if n in exists_today_names]
    return {
        "candidates": rows,
        "not_division_gated_and_reaches_the_site": covers,
        "of_those_that_exist_today": covers_today,
        "verdict": (
            "PARTIAL. Ribociclib closes access at the invading edge on a measured concentration, "
            "and hydroxychloroquine is the only exists-today agent there that is not "
            "division-gated -- but its margin contribution is ~2e-5/day, so it is cover rather "
            "than kill. The agent that would actually clear a persister in that compartment "
            "(DMAPT, the one measured in canine HS) is TO-BUILD. So the invading edge closes "
            "against the 10 margin-computed routes and leaves the persister route carried by "
            "schedule (continuous dosing, condition C3) rather than by a second kill mechanism."
        ),
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
    ribo = pk.ribociclib_nonenhancing_range()
    ribo_csf = pk.ribociclib_by_compartment()[cat.LEPTOMENINGEAL]
    para_mouse = abe[f"{cat.PARENCHYMA} (mouse Kp,uu 0.03)"]
    para_rat = abe[f"{cat.PARENCHYMA} (rat Kp,uu 0.11)"]
    bulk = abe[EXTRA_AXIAL]
    csf = exists_today_pkpd_by_site()[cat.LEPTOMENINGEAL]
    csf_oral_closes = [k for k, v in csf.items() if v["closes"]]

    sites = {
        EXTRA_AXIAL: {
            "verdict": Verdict.CLOSES.name,
            "carried_by": "abemaciclib (licensed today)",
            "margin_per_day": bulk["margin"],
            "basis": "MEASURED human resected-brain-lesion tissue concentration at 19x the CDK6 "
                     "IC50. This is the compartment the tumour is actually BASED in -- extra-axial "
                     "and meninges-based in 23/23 dogs -- and it closes with no to-build agent.",
        },
        cat.LEPTOMENINGEAL: {
            "verdict": (Verdict.CLOSES.name if csf_oral_closes
                        else Verdict.CLOSES_WITH_PROCEDURE.name),
            "carried_by": (f"ribociclib ORALLY on a MEASURED unbound CSF concentration "
                           f"({pk.RIBOCICLIB_CSF_NM} nM), with intrathecal bolus as the obtainable "
                           f"backup and {', '.join(csf_oral_closes)} also clearing the bar"
                           if csf_oral_closes
                           else "intrathecal bolus only (obtainable in dogs)"),
            "margin_per_day": ribo_csf["margin"],
            "basis": f"By mouth at the measured CSF access of "
                     f"{cat.SMALL_MOLECULE_ACCESS[cat.LEPTOMENINGEAL]}, the exists-today agents "
                     f"that clear the bar are: {csf_oral_closes or 'none'}. This is the one place "
                     f"the generic compartment access is the right figure to use, because the "
                     f"quantity needed is a CSF concentration rather than a tissue one. Intrathecal "
                     f"bolus remains available as a backup: access 1.0 in bulk CSF by "
                     f"construction, DIFFUSE (matching meningeal enhancement in 19/19 dogs), about "
                     f"1 complication in {int(1 / INTRATHECAL_COMPLICATION_RATE)} in dogs. The open "
                     f"quantity there is fluid-to-cell transfer, not whether the drug gets in.",
        },
        cat.PARENCHYMA: {
            "verdict": (Verdict.CLOSES.name if ribo["closes_at_every_measured_value"]
                        else Verdict.MARGINAL.name),
            "carried_by": "ribociclib (licensed today), on a MEASURED unbound concentration in "
                          "Gd-non-enhancing tumour",
            "margin_per_day": ribo["worst_measured_margin"],
            "basis": f"THIS WAS THE PROJECT'S LAST OPEN SITE AND IT CLOSES ON A LICENSED DRUG. "
                     f"Gd-non-enhancing tumour IS tissue behind an intact barrier, by definition, "
                     f"so a drug concentration measured there answers the access question directly "
                     f"instead of inferring it. Ribociclib's measured unbound concentration there "
                     f"clears the bar at EVERY reported value including the single lowest patient "
                     f"(65 nM, {ribo['fold_over_bar_at_worst']}x the growth bar, margin "
                     f"{ribo['worst_measured_margin']:+}/day), and the trial that reported it "
                     f"enrolled on CDKN2A/B deletion with wild-type Rb -- this tumour's lesion. "
                     f"Pharmacodynamics confirmed in the same tissue: RB phosphorylation and Ki-67 "
                     f"both significantly reduced. Oral and continuous, so access and duty come "
                     f"from ONE schedule and no procedure is involved. "
                     f"WHAT IT DOES NOT DO: CDK4/6 inhibition is division-gated and cytostatic, so "
                     f"it closes ACCESS at this site, not every escape at it -- the drug-tolerant "
                     f"persister still needs a non-division-gated agent (see "
                     f"persister_cover_at_the_invading_edge()). "
                     f"Abemaciclib was the previous candidate here and is kept as the alternative; "
                     f"on its own measured rodent range it spans {para_mouse['margin']:+} to "
                     f"{para_rat['margin']:+}/day -- it fails at the mouse ratio -- which is "
                     f"exactly why a measured concentration beats an inferred ratio.",
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
                f"ACCESS CLOSES AT EVERY SITE WITH LICENSED AGENTS. All {len(sites)} occupied "
                f"sites clear the growth bar with no procedure on the critical path, each on a "
                f"MEASURED unbound drug concentration in the matching compartment: the extra-axial "
                f"bulk, the CSF, and -- the site that was open until ribociclib's Gd-non-enhancing "
                f"tumour measurements were brought in -- the invading edge behind an intact "
                f"barrier, at every reported value including the lowest single patient. "
                f"WHAT IS STILL NOT CLOSED BY A LICENSED AGENT: the drug-tolerant persister at the "
                f"invading edge, because CDK4/6 inhibition is division-gated. That route is carried "
                f"by SCHEDULE (continuous dosing, condition C3) rather than by a second kill "
                f"mechanism, and the agent that would carry it by kill -- DMAPT, the one measured "
                f"in canine HS -- is to-build. And the genotype-anchored arm remains to-build "
                f"(C7), so a second primary is met by reroute-and-switch rather than by a standing "
                f"anchor. So: the ACCESS problem that defined this project is closed with "
                f"obtainable drugs; two MECHANISM gaps remain, both named."
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
    sites = a["sites"]
    return (
        f"RULE-13 TIERING. The closing program has {len(PROGRAM)} named components: "
        f"{len(exists_today())} exist today and {len(to_build())} are to-build "
        f"({', '.join(x.name.split(' (')[0] for x in to_build())}). "
        f"PROGRAM A (licensed agents only) closes {len(a['sites_closed'])} of {len(sites)} occupied "
        f"sites with no procedure on the critical path, each on a MEASURED unbound drug "
        f"concentration in the matching compartment: extra-axial bulk "
        f"{sites[EXTRA_AXIAL]['margin_per_day']:+}/day, leptomeninges/CSF "
        f"{sites[cat.LEPTOMENINGEAL]['margin_per_day']:+}/day, and invaded parenchyma behind an "
        f"intact barrier {sites[cat.PARENCHYMA]['margin_per_day']:+}/day at the WORST reported "
        f"value. That third site was the project's last open one, and it closed on ribociclib -- "
        f"licensed, oral, continuous -- because gadolinium-non-enhancing tumour is tissue behind an "
        f"intact barrier by definition, and the concentration there is measured rather than "
        f"inferred, in a trial enrolling this tumour's own lesion (CDKN2A/B-deleted, Rb-wildtype). "
        f"PROGRAM B closes every route at both modelled sites at "
        f"{b['derived_induction_kill_per_day']}/day derived induction kill, surviving down to "
        f"{b['minimum_fraction_of_measured_exposure_needed'] * 100:.2f}% of the measured exposure, "
        f"and it requires {len(b['load_bearing_to_build'])} to-build agents. "
        f"THE GAP IS {the_gap()}"
    )
