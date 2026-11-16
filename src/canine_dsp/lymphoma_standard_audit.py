"""Grades every live input of the lymphoma closing programs against THE USER'S STATED BAR (CLAUDE.md rules 2 and 11),
not against "has it been shown in a dog".

The bar: real data OR a rigorous model; a cross-species / cross-disease / class transfer is acceptable when justified in
writing; a number with no basis at all, or whose basis is circular, tuned or contradicted, FAILS. Absence of a canine
measurement is not a failure.

`failing()` is the answer to "what is still open"; `wrongly_reported_as_gaps()` lists items that earlier answers called
open and that pass the bar (so they may not be presented as open again). Both are executed by tests.
"""

from __future__ import annotations

from dataclasses import dataclass

from .core import lymphoma_grounded as G
from .core.lymphoma_catalogue import CNS, GROWTH_PER_DAY, SYSTEMIC
from . import lymphoma_joint as J

#: Growth-rate bar (docs/universe/SWEEP_growth_bar.md). It was a bare illustrative literal (lymphoma_scenarios: "illustrative, not
#: fitted") gating every margin: the same failure as CLAUDE.md failure 7 in the HS work. It is now DERIVED as a bracket from dog data.
GROWTH_BAR_BASIS = {
    "value": GROWTH_PER_DAY,
    "grade": "DERIVED",
    "basis": ("0.0903/day is the upper end of the net in-vivo band (0.015-0.12/day) implied by dog relapse regrowth (PMIDs 21320021, "
              "17338160, 18196747) and untreated/prednisone natural history (PMIDs 9839202, 34125606), and 44% of the dog-measured gross "
              "potential rate (Tpot median 3.4 d, 42 dogs, PMID 10598945; 0.204/day). Conservative against observed net regrowth; NOT an "
              "upper bound if cell loss is small, so growth_sensitivity() reports the closure at 0.12, 0.15 and 0.204."),
    "band": (0.015, 0.12),
    "gross_ceiling": 0.204,
}

#: Access / duty numbers used by the programs that have no measured source of their own. Each is checked for whether any
#: program depends on it (drop-one and halving). A number with no source that nothing depends on is inert, not a gap.
UNSOURCED_ACCESS = {
    "hydroxychloroquine": "brain access 0.3 (no source; tumour level measured in dogs, brain not)",
}


@dataclass(frozen=True)
class Item:
    name: str
    grade: str
    passes: bool
    reason: str


def program_potency_items(ip: str) -> list:
    pools = J._pools(ip, **{"kill": J.CENTRAL["kill"], "duty": J.CENTRAL["duty"]})
    out = []
    for p in J.NEAR_FUTURE_PROGRAMS[ip]:
        name = J._resolve(p, pools)
        comp = CNS if name in pools[CNS] else SYSTEMIC
        a = pools[comp][name]
        g = G.potency_grade(a)
        out.append(Item(f"{ip}: {name}", g, g in G.SOUND_GRADES,
                        f"potency {a.potency:.3g}/day, access {a.access}, tier {J.READINESS[p][0]}: {a.potency_evidence[:160]}"))
    return out


def load_bearing_unsourced(ip: str) -> list:
    """Unsourced access numbers a program actually depends on: the program minus that agent no longer clears."""
    items = []
    for prefix, why in UNSOURCED_ACCESS.items():
        if prefix not in J.NEAR_FUTURE_PROGRAMS[ip]:
            continue
        rest = tuple(p for p in J.NEAR_FUTURE_PROGRAMS[ip] if p != prefix)
        r = J.joint_report(ip, rest, **J.LOW)
        items.append(Item(f"{ip}: {prefix} access", "UNSOURCED", r["clears"],
                          f"{why}; program without it {'clears' if r['clears'] else 'does NOT clear'} at the low inputs"))
    return items


def growth_bar_item() -> Item:
    b = GROWTH_BAR_BASIS
    return Item("growth-rate bar", b["grade"], b["grade"] in ("DERIVED", "TRANSFERRED", "MEASURED"), b["basis"])


def lawful_brain_items() -> list:
    """Inputs the LAWFUL brain programs depend on at verdinexor's brain-reach FLOOR 0.09 (sections M.2-M.5).
    The intrathecal dose count is load-bearing. Inside canine precedent (<= 28 doses): MEASURED-PRECEDENT. Up to 45 doses at >= 10-day
    spacing: TRANSFERRED (written transfer from human long-course and canine repeated-dosing series, SWEEP_it_longcourse.md). Beyond
    that: ASSUMED. The procedural mortality of that many injections is a cost reported by procedural_cost(), not a pass/fail input."""
    from . import lymphoma_sustained as S
    out = []
    for ip, candidates in (("T", ((10, 118.0), (14, 14.0))), ("B", ((10, 118.0), (14, 14.0), (14, 2.5)))):
        found = [(w, i) for w, i in ((S.lawful_brain_window(ip, interval_days=i, ic50_nM=c), i) for i, c in candidates) if w]
        best, worst = min(found, key=lambda x: x[0][1]), max(found, key=lambda x: x[0][1])
        if worst[0][1] <= S.DOG_IT_DOSES_PRECEDENT_MAX:
            grade = "MEASURED-PRECEDENT"
        elif worst[0][1] <= S.DOG_IT_DOSES_TRANSFERRED_MAX and min(i for _, i in found) >= S.DOG_IT_MIN_INTERVAL_DAYS:
            grade = "TRANSFERRED"
        else:
            grade = "ASSUMED"
        out.append(Item(f"{ip}: tolerability of {best[0][1]}-{worst[0][1]} intrathecal methotrexate doses over {best[0][0]}-{worst[0][0]} d",
                        grade, grade != "ASSUMED",
                        f"closing schedules across the IC50 range at verdinexor brain-reach floor {S.VERDINEXOR_CNS_ACCESS_FLOOR}; canine "
                        f"precedent 20-{S.DOG_IT_DOSES_PRECEDENT_MAX} doses; written transfer to {S.DOG_IT_DOSES_TRANSFERRED_MAX} doses at "
                        f">= {S.DOG_IT_MIN_INTERVAL_DAYS} d spacing (SWEEP_it_longcourse.md)"))
    return out


def procedural_cost() -> dict:
    """The cost the closure carries that is not a pass/fail input: cumulative procedural mortality, BY ROUTE (section M.6). Dosing a
    subcutaneous CSF port under sedation rather than general anaesthesia cuts it ~20-80x, and is TRANSFERRED from the canine port
    programme (sedation for 8-20 months of biweekly infusions) and human in-clinic Ommaya taps. The risk then moves to the device:
    reservoir infection per access swings ~100-fold with technique, so strict aseptic protocol is a condition, not a detail."""
    from . import lymphoma_sustained as S
    return {"mortality_by_route": dict(S.PROCEDURAL_MORTALITY_BY_ROUTE),
            "port_infection_per_access_and_cumulative_at_45": dict(S.PORT_INFECTION_PER_ACCESS),
            "dose_sparing_ruled_out": S.IT_DOSE_SPARING_RULED_OUT}


def cns_seeding_item() -> Item:
    """The fraction of pre-treatment burden assumed to seed the CNS. It is `lymphoma_scenarios.LYMPHOMA_CNS_SEED_FRACTION = 0.05`,
    labelled "illustrative" in its own source line, and it is LOAD-BEARING: it sets how many intrathecal doses the brain needs, and so
    whether a dog needs an implanted CSF port at all. At 0.05 the brain takes 16-18 doses (port); at 0.001 it takes 10 and at 0.0001
    seven, which canine practice gives by percutaneous cisternal puncture without a port (112 dogs, PMID 25041580). No canine measurement
    of occult CNS seeding at diagnosis was found. `LYMPHOMA_DURABLE_RESPONSE.md:242` separately models "30% CNS involvement", a different
    quantity (share of dogs, not share of burden), so the record does not supply this number either.
    This is the same failure pattern as CLAUDE.md failure 7: a bare illustrative literal gating a conclusion."""
    from .core import lymphoma_grounded as G
    return Item("CNS seeding fraction (sets the intrathecal dose count, and whether a port is needed)", "ASSUMED", False,
                f"{G.CNS_SEED_FRACTION} is 'illustrative' in lymphoma_scenarios.py, not fitted or cited; load-bearing because the brain "
                "dose count scales with it (0.05 -> 16-18 doses, needs a port; 0.0001 -> 7 doses, within percutaneous practice). "
                "Closed by either a canine occult-CNS-seeding measurement or a written transfer from human CNS-relapse-risk data")


def sustained_additivity_item() -> Item:
    """OUTCOME TEST THE MODEL FAILS (section M.8, found 2026-11-16 from the prior-art sweep).

    A canine trial compared a 2-year maintenance phase (75 dogs) with discontinuous therapy (333 dogs) and found NO difference
    (PMID 28100766). The model, run on the same regimen, says otherwise: sustained CHOP clears inside the window at 365 days and
    beyond. Localising it shows the error is in ADDITIVITY UNDER SUSTAIN, not in the division-gated logic, which is right on its own:
      - CHOP cytotoxics alone (doxorubicin + vincristine + cyclophosphamide), all division-gated: never clears at 126/365/730 d. Correct.
      - prednisolone alone (not division-gated): never clears. Correct -- real median survival on prednisolone is 1-2 months.
      - the two TOGETHER, sustained: clears at 365 d. Contradicted by the 408-dog comparison.
    So summing a non-gated agent's kill with gated agents' kill and then extending the window crosses the clearance threshold in the
    model where it does not in dogs. This is the SAME construction every window in sections J-M.7 rests on (hydroxychloroquine and the
    graft non-gated, verdinexor and cytarabine gated, sustained for 147-483 days), so it puts a question over all of those windows, in
    the direction of the model being too optimistic. Magnitude not yet bounded.

    Not a reason to discard the programme: the escape-coverage conjunction and the toxicity budget are unaffected, and the brain arm's
    radiation and intrathecal terms are separately derived. But the DURATION numbers are now graded CONTRADICTED until this is
    reconciled -- by calibrating the additivity against the maintenance null, or by showing why the trial's maintenance (reduced-dose,
    spaced cytotoxics) is not what the model simulated."""
    return Item("sustained additive kill vs the canine maintenance null", "CONTRADICTED", False,
                "model: sustained CHOP clears at >=365 d; dogs: 2-year maintenance (n=75) no better than discontinuous (n=333), "
                "PMID 28100766. Error localised to additivity under sustain (cytotoxics alone and prednisolone alone both correctly "
                "never clear). Every quoted window in sections J-M.7 uses the same construction, so all are suspect in the optimistic "
                "direction; magnitude unbounded. Closed by calibrating additivity to the maintenance null, or by showing the trial's "
                "reduced-dose spaced maintenance is not what the model simulates")


def failing() -> list:
    """Every input that fails the stated bar. Empty means nothing fails; this is what to quote."""
    out = []
    gb = growth_bar_item()
    if not gb.passes:
        out.append(gb)
    out += [i for i in lawful_brain_items() if not i.passes]
    for extra in (cns_seeding_item(), sustained_additivity_item()):
        if not extra.passes:
            out.append(extra)
    for ip in ("B", "T"):
        out += [i for i in program_potency_items(ip) if not i.passes]
        out += [i for i in load_bearing_unsourced(ip) if not i.passes]
    return out


def wrongly_reported_as_gaps() -> list:
    """Items earlier answers listed as open that pass the bar. Do not present these as open under any phrasing."""
    return [
        Item("no canine CAR-T efficacy measured", "TRANSFERRED", True,
             "human CAR-T kill 0.12/0.35/1.1 per day (PMIDs 33757357, 33565700) and the exact threshold the programs need (0.08-0.2) are stated; "
             "dog CAR-T non-expansion (7 dogs) is a condition with a route (in-vivo CAR-T; the B-cell program also has a CAR-T-free route)"),
        Item("no drug level in gadolinium-non-enhancing lymphoma", "TRANSFERRED", True,
             "the rule-14 proxy was searched; no lymphoma measurement exists; one exists for high-dose IV methotrexate in human glioma "
             "(non-enhancing tissue 22-24 uM peak, unbound ratio ~0.07-0.21, PMID 18787762; SWEEP_lawful_cns_agents.md); access factors are "
             "transferred from CSF/plasma and trial data (docs/LYMPHOMA_UNIVERSE.md section G)"),
        Item("no canine engager exists", "TRANSFERRED", True,
             "class is licensed or late-stage in humans; potency 0.16/day TRANSFER-OUTCOME; the B-cell program closes without CAR-T on it and "
             "clears without it at CAR-T kill >= 0.08/day"),
        Item("MHC loss under a DLA-identical graft", "DERIVED", True,
             "HLA loss is a mismatch mechanism (PMID 42348822); MHC-II loss only weakens T-cell arms; antibody/CAR-T/engager are MHC-independent"),
        Item("unattributed multidrug resistance (E12)", "TRANSFERRED", True,
             "axi-cel 31% ongoing at ~5 y in chemo-refractory LBCL (PMID 36821768): the resistant state does not defeat the immune routes"),
    ]


def growth_sensitivity(growths=(0.0903, 0.12, 0.15, 0.204)) -> list:
    """Closure of the near-future programs when the growth bar is raised, potencies held fixed (adverse: outcome-calibrated kills would
    rise with the bar). Returns rows (growth, immunophenotype, input set, clears, halved, drop-one). Restores the model afterwards."""
    from .core import lymphoma_horizon as H
    base = GROWTH_PER_DAY
    saved = (G.GROWTH_PER_DAY, G.margin_for.__defaults__, dict(G.evaluate.__kwdefaults__), H.BULK_GROWTH_PER_DAY)

    def set_g(g):
        G.GROWTH_PER_DAY = g
        d = list(saved[1]); d[0] = g
        G.margin_for.__defaults__ = tuple(d)
        G.evaluate.__kwdefaults__["growth"] = g
        H.BULK_GROWTH_PER_DAY = saved[3] * g / base

    rows = []
    try:
        for g in growths:
            set_g(g)
            for ip in ("B", "T"):
                for lab, kw in (("low", J.LOW), ("central", J.CENTRAL)):
                    r = J.joint_report(ip, J.NEAR_FUTURE_PROGRAMS[ip], **kw)
                    rows.append({"growth": g, "ip": ip, "inputs": lab, "clears": r["clears"], "halved": r["halved_clears"],
                                 "drop_one": r["any_one_removed_clears"]})
    finally:
        G.GROWTH_PER_DAY, G.margin_for.__defaults__ = saved[0], saved[1]
        G.evaluate.__kwdefaults__.update(saved[2])
        H.BULK_GROWTH_PER_DAY = saved[3]
    return rows


def routes_not_counted() -> list:
    """Closure routes found by the drawing-board pass that carry an ASSUMED input and are therefore NOT counted as closing anything
    (docs/LYMPHOMA_UNIVERSE.md section H). `failing()` covers the inputs of the counted programs; this lists what was set aside and why."""
    return [
        Item("B-cell brain by sustaining oral cytarabine ~1,500 days", "ASSUMED", False,
             "needs a CSF time-average >= ~0.11 uM (measured troughs 0.04-0.27 uM; time-average 0.3-1.4 uM is derived, never measured) and "
             "multi-year tolerability (no source: human use is 10-14 days per 28; longest dog dosing is 7 days continuous / pulsed IV for 24 months)"),
        Item("persistent graft-versus-lymphoma past day 166 closing the dormant progenitor", "TRANSFERRED hold, no rate", False,
             "supports a hold (dog plateau, CML transcripts) but the model needs 0.06-0.12 /day against a 0.0008-0.004 /day bracket"),
        Item("brain closure on 20 (B) / 11-12 (T) intrathecal doses every 21 days", "ASSUMED", False,
             "needs verdinexor brain reach >= ~0.24 (B) / 0.25-0.30 (T) in the dog. The 0.30 used was read off a TOTAL brain:plasma "
             "ratio and has no basis in the right compartment; the only compartment measurement is selinexor's human CSF / unbound "
             "plasma 0.09 (Blood 2025;146 Suppl 1:3550), a FLOOR for verdinexor (less polar, not a canine P-gp substrate), at which this "
             "schedule never clears. Not contradicted for verdinexor; unsupported (sections M.2, M.4)"),
        Item("T-cell brain by the section-I route (sustained oral cytarabine or CD7/CD5 CAR-T, no intrathecal methotrexate)", "OPEN", False,
             "dormant lineage needs ~8 years of oral cytarabine in T-cell disease; CD7/CD5 CAR-T has no dog program found. The T-cell "
             "brain itself closes by radiation + intrathecal methotrexate (sections J, M); this lists only the set-aside route"),
    ]
