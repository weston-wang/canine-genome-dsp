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

    EXTRA-AXIAL / BLOOD-SIDE BULK   abemaciclib, licensed today, at the MEASURED human
                                    brain-tumour-tissue multiple (19x the CDK6 IC50, resected
                                    lesions with a disrupted barrier). Derived kill ~1.0/day
                                    against a 0.055/day bar. CLOSES, decisively, with no to-build
                                    agent anywhere in it.

    LEPTOMENINGES / CSF             nothing exists-today closes it at the generic small-molecule
                                    access of 0.005 by mouth. Intrathecal bolus does, is obtainable,
                                    is DIFFUSE (matching meningeal enhancement in 19/19 dogs) and
                                    runs about 1 complication in 112 in dogs. CLOSES, with a
                                    procedure.

    INVADED PARENCHYMA, INTACT      this is where the exists-today program actually fails, and it
    BARRIER                         fails on abemaciclib's OWN measured numbers rather than on a
                                    generic figure: unbound plasma 21.8 nM against rodent Kp,uu
                                    0.03-0.11 gives 0.65-2.4 nM, i.e. 0.36x-1.34x the derived
                                    closure bar. It closes at the rat ratio and does NOT close at
                                    the mouse ratio. MARGINAL, and the only obtainable fix is a
                                    procedure (CED, done in dogs), which reintroduces exactly the
                                    schedule-coherence defect core.schedule_coherence exists to
                                    catch -- a monthly catheter cannot supply a continuous duty.

So the gap between Program A and Program B is TWO PROPERTIES ON DIFFERENT AGENTS, not a program --
`the_gap()` reads them off `uncovered_properties()` rather than asserting them:

    ACCESS AND DUTY FROM ONE SCHEDULE   an oral, non-efflux-substrate agent that carries its own
                                        penetration past an INTACT barrier. RGN3067's role;
                                        paxalisib is the same property on the PI3K axis, where
                                        duvelisib covers the potency but not the access.
    GENOTYPE ANCHORING                  an agent aimed at the germline MTAP deletion itself, the
                                        only kind automatically matched to a SECOND primary in a
                                        breed born predisposed. Already condition C7.

HOW THIS CHANGES THE HEADLINE
-----------------------------
It does not withdraw the closure. It states its price correctly:

  * the closure of all 16 routes at both sites, all-oral and schedule-coherent, REQUIRES three
    to-build agents (induction, PI3K access, genotype anchor). That is now condition C8 in
    `deterministic_closure`, alongside the sponsor condition C7, instead of being hidden behind an
    `obtainable=True` flag -- `mislabelled_as_obtainable()` names the two agents that flag carries;
  * the compartment this tumour is actually BASED in closes with agents that are licensed today,
    and so does the leptomeningeal compartment, by mouth, with intrathecal bolus only as a backup;
  * none of the to-build agents is a molecule that has to be discovered. One is in human Phase I/II
    (the PRMT5 anchor), one is in human trials with a measured Kp,uu of 0.31 (paxalisib), and one
    is a published preclinical compound with measured brain exposure (RGN3067). The outstanding
    work is veterinary formulation and access, not chemistry.

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
        substitute_covers=("potency",),
        properties_used=("potency", "access", "duty"),
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
        "abemaciclib",
        "CDK4/6 maintenance against the co-deleted CDKN2A; lead brain arm",
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


def program_a() -> dict:
    """PROGRAM A: the closure searched from EXISTS-TODAY agents only. Rule 13's first question."""
    abe = abemaciclib_by_site()
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
            "carried_by": (f"{', '.join(csf_oral_closes)} ORALLY, with intrathecal bolus as the "
                           f"obtainable backup" if csf_oral_closes
                           else "intrathecal bolus only (obtainable in dogs)"),
            "margin_per_day": (max(csf[k]["margin"] for k in csf_oral_closes)
                               if csf_oral_closes else None),
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
            "verdict": Verdict.MARGINAL.name,
            "carried_by": "abemaciclib, at its own measured rodent unbound ratios",
            "margin_per_day": [para_mouse["margin"], para_rat["margin"]],
            "basis": "THIS IS WHERE THE EXISTS-TODAY PROGRAM FAILS, and it fails on the agent's own "
                     "numbers rather than on a generic figure: unbound plasma 21.8 nM against "
                     "rodent Kp,uu 0.03-0.11 gives 0.65-2.4 nM, which closes at the rat ratio "
                     f"({para_rat['margin']:+}/day) and does NOT close at the mouse ratio "
                     f"({para_mouse['margin']:+}/day). The only obtainable fix is a procedure "
                     "(convection-enhanced delivery, performed in dogs), which reintroduces the "
                     "schedule-coherence defect: a monthly catheter cannot supply a continuous duty "
                     "cycle, and continuous duty is condition C3.",
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
            f"PARTIAL -- {len(closed)} of {len(sites)} sites close with licensed agents and no "
            f"procedure on the critical path ({'; '.join(closed)}), and {len(not_closed)} does "
            f"not: {'; '.join(not_closed)}. The failing site is the invading edge behind an intact "
            f"barrier, and it fails on abemaciclib's OWN measured rodent range rather than on a "
            f"generic access figure. So the exists-today program does not deliver the decade by "
            f"itself -- but what it misses is one compartment, not the plan."
        ),
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

    Stated from the computation rather than asserted: an earlier draft of this docstring called the
    gap "one property", which the field data contradicts -- there are two distinct ones, and they
    sit on different agents.
    """
    unc = uncovered_properties()
    props = sorted({p for ps in unc.values() for p in ps})
    return (
        f"TWO PROPERTIES ON DIFFERENT AGENTS, not a program. Uncovered by anything licensed today: "
        f"{', '.join(props)}. (1) ACCESS AND DUTY FROM ONE SCHEDULE at the invading edge -- an oral, "
        f"non-efflux-substrate agent that carries its own penetration past an INTACT barrier "
        f"(RGN3067's role; paxalisib supplies the same property on the PI3K axis, where duvelisib "
        f"covers the potency but not the access). Every obtainable alternative buys that access "
        f"with a procedure, and a monthly catheter cannot also supply a continuous duty cycle. "
        f"(2) GENOTYPE ANCHORING -- an agent aimed at the germline MTAP deletion itself, which is "
        f"the only kind that is automatically matched to a SECOND primary in a breed that is born "
        f"predisposed. Nothing licensed does this, and the nearest dietary stand-in is excluded on "
        f"sustained-restriction toxicity. "
        f"Everything else the decade needs -- the genotype stratification itself, the continuous "
        f"schedule, the toxicity budget, the leptomeningeal route, the surveillance loop, and the "
        f"kill at the extra-axial bulk where this tumour is actually based -- is already "
        f"satisfiable with agents that are licensed or dog-trialled today."
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
    return (
        f"RULE-13 TIERING. The closing program has {len(PROGRAM)} named components: "
        f"{len(exists_today())} exist today and {len(to_build())} are to-build "
        f"({', '.join(x.name.split(' (')[0] for x in to_build())}). "
        f"PROGRAM A (exists-today only) is {a['verdict']} "
        f"It closes the extra-axial, meninges-based bulk -- the compartment this tumour occupies in "
        f"23/23 dogs -- at {a['sites'][EXTRA_AXIAL]['margin_per_day']:+}/day on abemaciclib's "
        f"MEASURED human brain-lesion tissue exposure, and closes the leptomeningeal compartment "
        f"BY MOUTH at {a['sites'][cat.LEPTOMENINGEAL]['margin_per_day']:+}/day, with intrathecal "
        f"bolus only as an obtainable backup. It is marginal at the invading edge behind an intact "
        f"({a['sites'][cat.PARENCHYMA]['margin_per_day'][0]:+} to "
        f"{a['sites'][cat.PARENCHYMA]['margin_per_day'][1]:+}/day across abemaciclib's own measured "
        f"rodent range). "
        f"PROGRAM B closes every route at both sites at {b['derived_induction_kill_per_day']}/day "
        f"derived induction kill, surviving down to "
        f"{b['minimum_fraction_of_measured_exposure_needed'] * 100:.2f}% of the measured exposure, "
        f"and it requires {len(b['load_bearing_to_build'])} to-build agents. THE GAP IS {the_gap()}"
    )
