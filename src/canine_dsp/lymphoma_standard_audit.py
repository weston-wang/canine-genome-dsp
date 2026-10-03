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


def failing() -> list:
    """Every input that fails the stated bar. Empty means nothing fails; this is what to quote."""
    out = []
    gb = growth_bar_item()
    if not gb.passes:
        out.append(gb)
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
             "the rule-14 proxy was searched; no measurement exists for any agent; access factors are transferred from CSF/plasma and trial data "
             "(docs/LYMPHOMA_UNIVERSE.md section G) and every brain route has at least four covering agents"),
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
