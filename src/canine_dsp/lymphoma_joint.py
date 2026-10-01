"""Joint body + brain programs under the widened universe, with the human-grounded CAR-T inputs.

A real program is ONE regimen given to ONE dog, so toxicity is charged on the UNION of its agents, and the body and the brain
must both clear every escape on that union. This module evaluates a named set of agents in both compartments, charging every
agent's organ load in both (an agent that is not delivered to a compartment is carried there at access 0, so only its load counts),
and runs the fault-tolerance tests on the whole union: all potencies halved, and any one agent removed.

Inputs (docs/universe/SWEEP_cart_kill.md, SWEEP_cart_human.md): CAR-T in-vivo kill low 0.12 / central 0.35 / high 1.1 per day (TRANSFER
from human models); CSF duty of a CSF-delivered CAR-T low 0.15 / central 0.4 / high 0.7 (derived from human CNS-tumour trials).
"""

from __future__ import annotations

from dataclasses import replace

from .core import lymphoma_grounded as G
from .core.lymphoma_catalogue import CNS, SYSTEMIC

IT = "intraventricular/intrathecal"
CENTRAL = {"kill": 0.35, "duty": 0.4}
LOW = {"kill": 0.12, "duty": 0.15}


def _pools(ip: str, kill: float, duty: float):
    out = {}
    for comp in (SYSTEMIC, CNS):
        d = {}
        for a in G.sound_pool(G.available(G.grounded_agents(comp, ip), "any")):
            if "CAR-T" in a.name and G.potency_grade(a) == "TRANSFER-OUTCOME":
                a = replace(a, potency=kill)
                if IT in a.name:
                    a = replace(a, duty=duty)
            d[a.name] = a
        out[comp] = d
    return out


def _escapes(ip: str):
    return tuple(e for e in G.FULL_ESCAPES
                 if not (ip == "T" and e.removes_antigen in ("CD19", "CD20"))
                 and not (ip == "B" and e.removes_antigen == "CD7"))


def _resolve(prefix: str, pools) -> str:
    for comp in (SYSTEMIC, CNS):
        for n in pools[comp]:
            if n.startswith(prefix):
                return n
    raise KeyError(prefix)


def joint_report(ip: str, prefixes, *, kill: float = CENTRAL["kill"], duty: float = CENTRAL["duty"], **ev_kw) -> dict:
    """Clears / halved / any-one-removed for the union, in both compartments."""
    pools = _pools(ip, kill, duty)
    esc = _escapes(ip)
    names = list(dict.fromkeys(_resolve(p, pools) for p in prefixes))

    def regimen(ns, comp):
        out = []
        for n in ns:
            if n in pools[comp]:
                out.append(pools[comp][n])
            else:
                other = pools[CNS if comp == SYSTEMIC else SYSTEMIC][n]
                out.append(replace(other, access=0.0))           # not delivered here; its organ load still counts
        return out

    def ok(ns, delta=1.0):
        for comp in (SYSTEMIC, CNS):
            r = regimen(ns, comp)
            if delta != 1.0:
                r = G.discounted(r, delta)
            kw = dict(ev_kw)
            if comp == SYSTEMIC:
                kw.pop("cns_fraction", None)
            if not G.clears(r, esc, compartment=comp, **kw):
                return False
        return True

    margins = {}
    for comp in (SYSTEMIC, CNS):
        ev = G.evaluate_best_schedule(regimen(names, comp), esc, compartment=comp,
                                      **({k: v for k, v in ev_kw.items() if not (comp == SYSTEMIC and k == "cns_fraction")}))
        margins[comp] = (ev.worst_derated, ev.weakest, ev.horizon_strict.verdict())
    clears = ok(names)
    halved = ok(names, 0.5)
    removed = {n: ok([m for m in names if m != n]) for n in names}
    return {"agents": names, "kill": kill, "duty": duty, "clears": clears, "halved_clears": halved,
            "any_one_removed_clears": all(removed.values()), "removal_breaks": [n for n, v in removed.items() if not v],
            "margins": margins}


#: The B-cell programs found by the search at the central human-grounded inputs (see docs/LYMPHOMA_UNIVERSE.md section E).
B_PROGRAMS = {
    "B-cell, 7 agents": ("anti-CD20 monoclonal antibody", "hydroxychloroquine", "persistence-engineered",
                         "autologous tumour vaccine", "panobinostat", "continuous intrathecal",
                         "tandem CD19/CD20 CAR-T, intra"),
    "B-cell, 8 agents with cytarabine CRI": ("anti-CD20 monoclonal antibody", "hydroxychloroquine", "verdinexor",
                                             "persistence-engineered", "autologous tumour vaccine",
                                             "cytarabine CRI (q7d)", "continuous intrathecal",
                                             "tandem CD19/CD20 CAR-T, intra"),
}

T_PROGRAMS = {
    "T-cell, 5 agents": ("hydroxychloroquine", "continuous intrathecal", "CD7-directed CAR-T (canine",
                         "CD5 + CD7 dual-target CAR-T (c", "verdinexor"),
    "T-cell, 8 agents with spinal-fluid CAR-T": ("hydroxychloroquine", "continuous intrathecal",
                                                 "CD7-directed CAR-T (canine", "CD5 + CD7 dual-target CAR-T (c",
                                                 "CD7-directed CAR-T, intra", "CD5 + CD7 dual-target CAR-T, intra",
                                                 "verdinexor", "venetoclax"),
}
