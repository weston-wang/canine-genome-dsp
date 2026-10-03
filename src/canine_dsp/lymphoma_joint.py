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


def escape_matrix(ip: str, prefixes, *, kill: float = CENTRAL["kill"], duty: float = CENTRAL["duty"]) -> list:
    """One row per escape per compartment for a program: the agents that reach it after toxicity de-rating, the strongest
    evidence grade among them, the number of independent covering agents, and the net margin (kill minus the growth bar, or
    the persister margin). A row is CLOSED only if at least one agent reaches it and the margin is positive."""
    pools = _pools(ip, kill, duty)
    esc = _escapes(ip)
    names = list(dict.fromkeys(_resolve(p, pools) for p in prefixes))
    rows = []
    order = {"MEASURED": 0, "DERIVED": 1, "PARTIAL": 2, "TRANSFER": 3, "TRANSFER-OUTCOME": 4, "OUTCOME": 5, "BRACKET": 6}
    for comp in (SYSTEMIC, CNS):
        reg = []
        for n in names:
            if n in pools[comp]:
                reg.append(pools[comp][n])
            else:
                other = pools[CNS if comp == SYSTEMIC else SYSTEMIC][n]
                reg.append(replace(other, access=0.0))
        d_agents, _, _ = G.derate(reg, G.gi.EFFLUX_CO_DOSE_MULTIPLIER_CANINE_PROXY)
        for e in esc:
            if e.requires_division:
                cover = [a for a in d_agents if a.reaches(e)]
            else:
                cover = [a for a in G._effective_agents_for(d_agents, e) if a.effective_kill > 0.0 and a.covers(e)]
            grades = [G.potency_grade(next(x for x in reg if x.name == a.name)) for a in cover]
            best = min(grades, key=lambda g: order.get(g, 9)) if grades else "-"
            margin = G.margin_for(d_agents, e)
            rows.append({"compartment": comp, "escape": e.name, "covering": [a.name for a in cover],
                         "n_cover": len(cover), "best_grade": best, "margin": margin,
                         "closed": bool(cover) and margin > 0.0})
    return rows


def clock_table(ip: str, prefixes, *, kill: float = CENTRAL["kill"], duty: float = CENTRAL["duty"]) -> dict:
    """Per escape and compartment, the treatment-clock outcome for the whole program on the union of its agents: the day the
    lineage is cleared, or 'relapses' (response then regrowth when the documented exposure windows end), or 'never'."""
    pools = _pools(ip, kill, duty)
    esc = _escapes(ip)
    names = list(dict.fromkeys(_resolve(p, pools) for p in prefixes))
    out = {}
    for comp in (SYSTEMIC, CNS):
        reg = []
        for n in names:
            if n in pools[comp]:
                reg.append(pools[comp][n])
            else:
                reg.append(replace(pools[CNS if comp == SYSTEMIC else SYSTEMIC][n], access=0.0))
        ev = G.evaluate_best_schedule(reg, esc, compartment=comp)
        out[comp] = {"verdict": ev.horizon_strict.verdict(), "clears": ev.horizon_strict.cure_inside_window,
                     "lineages": {o.name: (o.outcome, o.day) for o in ev.horizon_strict.outcomes}}
    return out


#: Programs built only from agents that exist today (licensed, off-label, or in dog trials; docs/LYMPHOMA_UNIVERSE.md section F).
EXISTING_PROGRAMS = {
    "B": ("anti-CD20 monoclonal antibody", "hydroxychloroquine", "verdinexor", "allogeneic DLA", "cytarabine ocfosfate"),
    "T": ("prednisolone (glucocorticoid)", "hydroxychloroquine", "verdinexor", "allogeneic DLA", "cytarabine ocfosfate",
          "romidepsin"),
}


# --- near-future programs (user, 2026-10-02: "include near future ones that are scientifically sound; nothing pure theoretical") ----
#: Readiness of each agent a closing program uses. A = exists today for dogs (licensed or off-label); B = clinical-stage in dogs;
#: C = clinical-stage in humans with a stated path to the dog (the canine construct or route still has to be built); D = preclinical
#: only; E = no clinical evidence of the mechanism anywhere. A program may use A-C; D and E are THEORETICAL and never count
#: (CLAUDE.md rule 13). docs/universe/SWEEP_near_future.md has the citations.
READINESS = {
    "anti-CD20 monoclonal antibody": ("B", "canine anti-CD20 antibody in dogs; B-cell depletion rate measured (PMID 38662527)"),
    "anti-CD20 monoclonal antibody, intra": ("C", "human intraventricular rituximab clears CSF lymphoma cells (PMID 24190981); Ommaya routine"),
    "hydroxychloroquine": ("A", "off-label"),
    "verdinexor": ("A", "licensed for canine lymphoma"),
    "prednisolone": ("A", "licensed"),
    "allogeneic DLA": ("A", "performed at referral centres; first-remission dogs 8 of 9 alive >4 y (PMID 35789057)"),
    "cytarabine ocfosfate": ("B", "oral continuous in dogs, CSF 1.0-3.6 uM (PMID 37670479)"),
    "romidepsin": ("A", "human-licensed for PTCL; off-label"),
    "CD3xCD20": ("C", "human CD3xCD20 engagers licensed or late-stage (epcoritamab, glofitamab); anti-canine CD3 and canine CD20 binders "
                      "exist, no canine engager yet; dog cytokine storm to a T-cell agonist antibody (PMID 25988188) => step-up dosing"),
    "persistence-engineered": ("C", "canine CD20 CAR-T given to 7 dogs (PMIDs 32002286, 35898541) but did not expand or persist; in-vivo "
                                    "CAR-T (human first-in-human, PMID 41882404) removes ex-vivo expansion"),
    "tandem CD19/CD20 CAR-T, intra": ("C", "human intrathecal CD19/CD22 CAR-T in B-ALL with CNS disease, CR 21/22 (ASH 2024); peer-reviewed "
                                           "intrathecal CAR-T in humans PMIDs 41495049, 42207176, 41798119"),
    "CD7-directed CAR-T (canine": ("C", "human CD7 CAR-T in T-ALL/lymphoma incl. CNS-involved (PMIDs 37020231, 37740926)"),
    "CD5 + CD7 dual-target CAR-T (c": ("C", "dual-target CD7/CD5 CAR-T prevents CD7-loss relapse (PMID 37020231)"),
    "CD7-directed CAR-T, intra": ("C", "intrathecal CAR-T in humans (above) with a CD7 binder"),
    "continuous intrathecal": ("C", "Ommaya/intrathecal cytarabine infusion in humans"),
}

#: The programs that close body AND brain at the LOW (pessimistic) human-grounded inputs, found by direct evaluation and by the
#: exhaustive brain search (docs/LYMPHOMA_UNIVERSE.md section G). The redundancy is deliberate: two independent antigen-directed
#: routes (antibody + CAR-T + engager for B) so that no single agent is load-bearing.
NEAR_FUTURE_PROGRAMS = {
    "B": ("anti-CD20 monoclonal antibody", "anti-CD20 monoclonal antibody, intra", "hydroxychloroquine", "verdinexor",
          "allogeneic DLA", "cytarabine ocfosfate", "CD3xCD20", "persistence-engineered", "tandem CD19/CD20 CAR-T, intra"),
    "T": ("hydroxychloroquine", "continuous intrathecal", "CD7-directed CAR-T (canine", "CD5 + CD7 dual-target CAR-T (c",
          "verdinexor", "allogeneic DLA", "CD7-directed CAR-T, intra", "cytarabine ocfosfate"),
}


def tier_mix(prefixes) -> dict:
    """Readiness level of every agent in a program; any D or E (theoretical) makes the program inadmissible."""
    levels = {p: READINESS[p][0] for p in prefixes}
    return {"levels": levels, "admissible": all(v in ("A", "B", "C") for v in levels.values()),
            "to_build": [p for p, v in levels.items() if v == "C"]}
