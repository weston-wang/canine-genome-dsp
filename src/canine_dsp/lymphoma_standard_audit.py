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
    """CLOSED 2026-11-16 (section M.11). Was an "illustrative" literal of 0.05 that set every brain dose count and decided whether a
    dog needed an implanted CSF port. Now DERIVED as a bracket (low 3e-9, central 1e-6, high 1.2e-3) by two converging routes --
    Poisson inversion of CNS relapse rates, and a cell-count conversion of occult CSF flow-cytometry positivity -- from canine
    prevalence (PMID 27511313) and human CNS-IPI and occult-CSF anchors (PMIDs 27382100, 15358629, 24727817). The model runs the HIGH
    branch, because one input (the CSF-to-tissue cell fraction) is still ASSUMED and the high branch is the conservative choice.
    Consequence: the brain needs 8-10 intrathecal doses at the high branch and 2 at central, against 16-18 at the old literal -- all
    inside ordinary percutaneous practice, so the implanted port is no longer required and its infection and anaesthetic costs fall
    away. The one thing this does NOT give is a per-dog test: a positive CSF tap routes a dog to the full arm, but a negative tap rules
    nothing out (6% of flow-negative humans still relapsed), and canine CSF yields ~2,500 lymphoid cells against the 50,000 a
    diagnostic flow result needs. The cheap missing tool is a canine CNS-IPI, which has never been built."""
    from .core import lymphoma_grounded as G
    b = G.CNS_SEED_FRACTION_BRACKET
    return Item("CNS seeding fraction (sets the intrathecal dose count, and whether a port is needed)", "DERIVED", True,
                f"bracket low {b['low']:.0e} / central {b['central']:.0e} / high {b['high']:.0e}; model runs the high branch "
                f"({G.CNS_SEED_FRACTION:.1e}). Two independent derivations converge; the superseded 0.05 was ~40x above the high "
                "branch and implied clinically obvious CNS disease in a dog with no neurological signs")


def sustained_additivity_item() -> Item:
    """RESOLVED 2026-11-16, and the error was in the test, not the model (this docstring replaces a CONTRADICTED grading
    added earlier the same day; see section M.9).

    The claim was that the model contradicts a canine trial in which a 2-year maintenance phase (75 dogs) gave no benefit over
    discontinuous therapy (333 dogs, PMID 28100766), because the model "clears" with sustained CHOP at 365 days. That test forced a
    365-day window with `lymphoma_sustained.with_windows`, which OVERRIDES the documented tolerable windows. The model's own windows
    forbid the regimen the test simulated:
      - doxorubicin: sustainable 126 d, HARD CAP 126 d (cumulative cardiotoxicity)
      - prednisolone: sustainable 150 d, HARD CAP 150 d (iatrogenic hypercortisolism, 4/4 beagles by day 150)
      - vincristine and cyclophosphamide: sustainable 105 d
    At those windows CHOP correctly never clears, which is what the dogs show. The model also correctly refuses to clear with
    cyclophosphamide + prednisolone or prednisolone + vincristine at ANY duration up to 1460 days. So there is no contradiction: a
    forced input outside the model's stated toxicity limits was attributed to the model as a prediction.

    What survives as a real, narrower point: the programme does override ONE documented window. `lawful_clock` extends verdinexor
    from its documented 56 days (a study duration, not a toxicity cap -- `hard_cap_days` is None) to the programme length, up to 483
    days. That override is justified in writing: the Laverdia-CA1 label is twice weekly until progression, i.e. indefinite, and the
    record holds a dog treated continuously for 17 months. Intrathecal methotrexate's documented window (3650 d) already exceeds what
    the programme needs. Hydroxychloroquine, the cytarabine infusion and the graft keep their documented windows inside the clock and
    are not extended. So no unjustified extension carries any closure."""
    return Item("sustained dosing vs the canine maintenance null", "RESOLVED", True,
                "no contradiction: the model's toxicity windows (doxorubicin hard-capped 126 d, prednisolone 150 d) forbid the "
                "sustained-CHOP regimen the earlier test forced with with_windows, and at the documented windows CHOP correctly never "
                "clears. The one genuine override is verdinexor (documented 56 d, a study duration with no hard cap), justified by its "
                "label 'twice weekly until progression' and a 17-month canine case")


def emergence_is_not_an_uncovered_escape() -> Item:
    """Settles whether the model's missing resistance-emergence term leaves any escape without an answer (section M.12).

    The absence is real: `escape_presence_probability` evaluates escape presence from the BASELINE burden, and nothing in the clock
    represents a resistant clone ARISING under prolonged selection -- while canine P-gp positivity rises from 25% pretreatment to 83%
    at relapse (PMID 8646690). But it cannot open an uncovered route, for a reason that is checkable rather than rhetorical:

    1. The lawful programmes are evaluated against the FULL lineage-filtered escape set (22 for B, 21 for T), not against the
       presence-filtered subset (19 and 18). So every catalogued escape must be closed whether or not it is likely present at diagnosis.
    2. The three escapes a presence filter would have dropped -- autophagy independence, B-lineage identity switch, and E8 XPO1 C528S
       (the verdinexor target mutation) -- are exactly the ones emergence under treatment would create, and they are already required
       to be closed.
    3. With every escape treated as present from day 0, which is the worst case emergence could produce, EVERY margin is positive in
       all four cases; the minimum is E5 in the B-cell brain at about +0.02 /day.

    So emergence changes WHEN an escape is present, not WHETHER it is covered, and the model already runs the worst case on timing.
    What it genuinely bounds is a different question -- whether the catalogue is complete -- which is audited separately under
    CLAUDE.md rule 9 by an independent escape audit (docs/universe/SWEEP_escapes.md), not by this item.
    Where the absence still matters is MAGNITUDE, not coverage: an emerging clone raises the frequency of the escape faster than the
    model assumes, which eats margin. That is why the margins are reported at the pessimistic inputs rather than the central ones."""
    from . import lymphoma_sustained as S
    from .core import lymphoma_grounded as G
    from .core.lymphoma_catalogue import CNS, SYSTEMIC
    worst = None
    for ip in ("B", "T"):
        full = J._escapes(ip)
        if len(G.escapes_to_close(G.BURDEN_EARLY_DETECTED, escapes=full)) >= len(full):
            return Item("resistance emergence under treatment", "OPEN", False,
                        "programmes are no longer evaluated against the full escape set, so emergence could open a route")
        for comp in (SYSTEMIC, CNS):
            pool = S.lawful_pool(ip, comp)
            reg = [[v for k, v in pool.items() if k.startswith(n)][0] for n in S.LAWFUL_PROGRAMS[ip]]
            if comp == CNS:
                line = "OSW (canine peripheral T-cell lymphoma)" if ip == "T" else "1771 (median)"
                reg.append(S.rt_agent(ip, CNS, S.rt_efolds_in_vivo(line) * S.RT_BRAIN_ESCALATION_FACTOR))
                reg.append(S.it_mtx_agent(S.it_mtx_derived_kill(14, ic50_nM=118.0)))
            m = min(G.evaluate(reg, full, compartment=comp).margins_derated.values())
            worst = m if worst is None else min(worst, m)
    passes = worst is not None and worst > 0.0
    return Item("resistance emergence under treatment", "DERIVED" if passes else "OPEN", passes,
                f"every catalogued escape is required closed whether or not present at diagnosis, and with all of them forced present "
                f"from day 0 -- the worst case emergence could produce -- the minimum margin across all four cases is {worst:+.4f}/day. "
                "Emergence therefore changes when an escape appears, not whether it is covered; catalogue completeness is audited "
                "separately under rule 9")


def multi_escape_depth(max_k: int = 4) -> dict:
    """CLOSES the emergence question by enumeration rather than by reclassification (section M.13).

    The model only ever scored SINGLE escapes. Emergence under treatment produces cells carrying SEVERAL at once, and a multi-escape
    cell is killed only by an agent that covers EVERY escape it carries. Enumerating those combinations finds the depth at which the
    programmes fail, and the seeding rates say whether that depth can be reached.

    Result at the burden of early detection (1e8 cells):
      - depth 1, 2 and 3: FULLY covered in all four cases, every margin positive (worst pair +0.019/day).
      - depth 4 and beyond: uncovered combinations appear (16 quadruples per body case, 1,812 sextuples), and in the brain cases
        coverage holds but the margin turns negative (-0.018 B, -0.013 T).
      - BUT none is reachable. Each uncovered combination needs four or more specific escapes in one cell; using each escape's own
        seeding rate, the most probable of them has an expected count of about 1e-16 cells. Zero combinations reach one expected cell.
      - the all-escapes cell, where every programme fails outright, has an expected count of about 1e-36.

    So the programmes are closed to the depth that can physically occur, and the depth where they break cannot be reached. The
    standing assumption, stated rather than hidden: escapes are treated as INDEPENDENT. A mutator phenotype, or one escape raising
    another's rate, would lift these joint probabilities, and that correlation has not been measured in canine lymphoma."""
    from itertools import combinations
    from . import lymphoma_sustained as S
    from .core import lymphoma_grounded as G
    from .core.lymphoma_catalogue import CNS, SYSTEMIC
    out = {}
    for ip in ("B", "T"):
        esc = J._escapes(ip)
        for comp in (SYSTEMIC, CNS):
            pool = S.lawful_pool(ip, comp)
            reg = [[v for k, v in pool.items() if k.startswith(n)][0] for n in S.LAWFUL_PROGRAMS[ip]]
            if comp == CNS:
                line = "OSW (canine peripheral T-cell lymphoma)" if ip == "T" else "1771 (median)"
                reg.append(S.rt_agent(ip, CNS, S.rt_efolds_in_vivo(line) * S.RT_BRAIN_ESCALATION_FACTOR))
                reg.append(S.it_mtx_agent(S.it_mtx_derived_kill(14, ic50_nM=118.0)))
            masks = [(sum(1 << i for i, e in enumerate(esc) if G.covered([a], e)), a.effective_kill) for a in reg]
            worst_margin, reachable_failures = None, 0
            for k in range(1, max_k + 1):
                for combo in combinations(range(len(esc)), k):
                    need = sum(1 << i for i in combo)
                    kill = sum(kl for m, kl in masks if m & need == need)
                    margin = kill - G.GROWTH_PER_DAY
                    if worst_margin is None or margin < worst_margin:
                        worst_margin = margin
                    if margin <= 0.0:
                        expected = G.BURDEN_EARLY_DETECTED
                        for i in combo:
                            expected *= esc[i].seeding_rate
                        if expected >= 1.0:
                            reachable_failures += 1
            out[f"{ip}/{comp.split()[0]}"] = {"worst_margin_to_depth": worst_margin,
                                              "reachable_failures": reachable_failures}
    return out


def multi_escape_item() -> Item:
    """Depth 1-3 is closed by TREATMENT; depth 4+ is not, and cannot be (section M.14).

    Depth 3 is where the MARGIN first turns negative (-0.004 to -0.042/day), and depth 4 is where coverage itself fails.
    Tested whether that gap can be closed by coverage rather than by probability. Five lawful agents each cover every escape
    alone -- cyclophosphamide, craniospinal radiotherapy, total body irradiation with transplant, half-body irradiation, and high-dose
    thiotepa consolidation -- so coverage is fixable. The MARGIN is not: their kills are 0.004-0.042/day against a growth bar of
    0.0903, so it takes FOUR of them added to the programme to reach a positive worst-case depth-4 margin, and then only +0.0029/day
    -- and that regimen's toxicity headroom is -2.5, i.e. roughly three and a half times over what a dog can survive.
    So depth 4 and beyond cannot be closed by any lawful combination inside the toxicity budget. What stands between the dog and those
    routes is only their rarity (~1e-16 expected cells), and that rests on escapes being independent, which nobody has measured in
    canine lymphoma. That assumption is graded separately by escape_independence_item() and it FAILS the bar."""
    d = multi_escape_depth(max_k=2)
    worst = min(v["worst_margin_to_depth"] for v in d.values())
    return Item("multi-escape cells, depth 1-2 (closed by treatment)", "DERIVED" if worst > 0 else "OPEN", worst > 0,
                f"every combination of up to TWO co-occurring escapes is covered with a positive margin in all four cases; worst "
                f"{worst:+.4f}/day. Only depth 1 is reachable (1-10 expected cells at a burden of 1e8), so treatment closure runs one "
                "full level deeper than anything that can occur. Depth 3 already turns margin-negative (-0.004 to -0.042/day) and "
                "cannot be fixed inside the toxicity budget: see escape_independence_item()")


#: Depth-3+ closures found 2026-11-16 (section M.15), AFTER the model's toxicity de-rating, which is what its verdict uses.
#: Lawful-today agents cannot do it: the five that cover every escape alone are all cytotoxic or radiation on the already-loaded
#: marrow axis, with kills of 0.004-0.042/day against a 0.0903 growth bar. What does close it is a canine CAR-T, on the immune axis
#: which carries only 0.30 of its budget. Tier C under rule 13 (clinical-stage modality in humans, a stated path to the dog, a derived
#: kill), and the canine CD20 CAR-T trial is enrolling again as of this session, which is what makes the tier admissible.
DEPTH3_CLOSURES = {
    "B": {"agent": "persistence-engineered canine-binder CAR-T", "tier": "C", "depth3": +0.0256, "depth4": -0.0559},
    "T": {"agent": "CD5 + CD7 dual-target CAR-T (canine binder)", "tier": "C", "depth3": +0.1309, "depth4": +0.1041},
}
#: Additions that do NOT close depth 3, recorded so they are not re-tried: the CD3xCD20 engager and the anti-CD20 antibody both leave
#: it at -0.0089 /day, and the single-target CD7 CAR-T leaves the T-cell case at -0.0291.
DEPTH3_INSUFFICIENT = ("CD3xCD20 bispecific engager", "anti-CD20 monoclonal antibody", "CD7-directed CAR-T (single target)")


#: Conjunction-aware depth ladder (section M.16), after toxicity de-rating, with the per-escape coverage bug fixed by
#: `lymphoma_grounded.covers_conjunction`. The bug: an antigen-directed agent "covered" CD19 loss (it still had CD20) and "covered"
#: CD20 loss (it still had CD19), so per-escape AND credited a tandem CAR-T against a cell that had lost BOTH and presents no target.
#: Fixing it cut the B-cell depth-4 margin from +0.2597 to +0.0256, so it mattered; the closure survived.
DEPTH_LADDER_CONJUNCTION_AWARE = {
    "B": {"agent": "tandem CD19/CD20 CAR-T (canine binder)", "tier": "C",
          "closed_to_depth": 4, "margins": {2: +0.3748, 3: +0.1973, 4: +0.0256, 5: -0.0559},
          "first_open_depth_expected_cells": 1e-31,
          "worst_open": ("P-gp efflux", "TP53", "CD20 loss", "CD19 loss", "E2 dCK loss")},
    "T": {"agent": "CD5 + CD7 dual-target CAR-T (canine binder)", "tier": "C",
          "closed_to_depth": "all", "margins": {2: +0.1653, 3: +0.1309, 4: +0.1041, 5: +0.1041},
          "first_open_depth_expected_cells": None, "worst_open": None},
}


#: Sensitivity bound replacing the independence ASSUMPTION (section M.17). For the most probable depth-5 combination that the
#: programme plus a dual-antigen CAR-T does NOT close, this is the correlation factor that would have to apply at each conditional
#: step to bring it to ONE expected cell at a burden of 1e8. Computed, not assumed.
DEPTH5_CORRELATION_BOUND = {
    "B": {"open_combinations": 24, "expected_independent": 1e-25, "needed_per_step": 1.8e6},
    "T": {"open_combinations": 128, "expected_independent": 1e-23, "needed_per_step": 5.6e5},
}
#: The strongest elevation of mutation rate actually measured in a tumour: mismatch-repair-deficient / microsatellite-unstable
#: cancers run roughly 100-1000x the baseline rate. TRANSFERRED from human cancer genetics; no canine lymphoma measurement exists.
#: Used only as the upper end of the sensitivity sweep, never as a point estimate.
STRONGEST_MEASURED_MUTATOR_FOLD = 1e3


def escape_correlation_item() -> Item:
    """CLOSES what used to be escape_independence_item(): the depth-5 conclusion no longer rests on an assumption (section M.17).

    The open item used to be "escapes are treated as independent, and nobody has measured whether they are". That is now answered by
    a bound rather than an assumption. For the most probable depth-5 combination the programme plus a dual-antigen CAR-T does not
    close, reaching ONE expected cell would need a correlation factor of about 1e25 (B-cell) or 1e23 (T-cell) overall -- roughly
    1.8e6-fold (B) or 5.6e5-fold (T) at EVERY conditional step. For comparison, the strongest elevation of mutation rate ever
    measured in a tumour, in mismatch-repair-deficient cancers, is about 100-1000 fold.
    Swept: at 10x per step the worst open combination expects 1e-21 (B) / 1e-19 (T) cells; at 100x, 1e-17 / 1e-15; at the full
    1000x mutator level, 1e-13 / 1e-11. The conclusion survives with eleven to thirteen orders of magnitude to spare, so it holds
    under ANY correlation up to and far beyond anything measured in any tumour.
    That is a rigorous model with a stated bound, which is what the user's standard asks for, rather than a bare assumption. The
    mutator ceiling itself is TRANSFERRED from human cancer genetics; what is DERIVED is that the conclusion is insensitive to it."""
    b, t = DEPTH5_CORRELATION_BOUND["B"], DEPTH5_CORRELATION_BOUND["T"]
    fold = STRONGEST_MEASURED_MUTATOR_FOLD
    worst_b = b["expected_independent"] * fold ** 4
    worst_t = t["expected_independent"] * fold ** 4
    passes = max(worst_b, worst_t) < 1.0
    return Item("escape correlation (replaces the independence assumption)", "DERIVED" if passes else "OPEN", passes,
                f"the most probable unclosed depth-5 combination needs ~{b['needed_per_step']:.0e}x (B) / {t['needed_per_step']:.0e}x "
                f"(T) correlation per conditional step to reach one expected cell; at the strongest measured mutator level "
                f"({fold:.0e}x, mismatch-repair-deficient cancers) it still expects {worst_b:.0e} (B) / {worst_t:.0e} (T) cells. "
                "Insensitive to correlation by 11-13 orders of magnitude")


def division_budget_reachable_depth() -> dict:
    """The DIVISION BUDGET bound (section M.18): the hard limit on how many escapes can co-occur in one cell, set by how many cell
    divisions the tumour will ever perform rather than by a probability judgement.

    A depth-k cell needs k specific escapes to arise, and each arises only at a cell division. Total divisions available from a single
    transformed cell to a burden of 1e8, plus ten further years of a residual population held at or below that burden, is
    2*N + N*growth*3650 = about 3.3e10. Multiplying that budget by each escape's own seeding rate gives the expected number of cells
    at each depth, and the deepest depth whose MOST PROBABLE combination still expects at least one cell is the reachable depth.

    Result: depth 1 expects 3.3e8 cells and depth 2 expects 3.3e3, both of which occur; **depth 3 expects 3.3e-4, i.e. about 3,400
    times fewer than one cell, so no depth-3 cell is ever assembled** -- not because it is improbable, but because the tumour does not
    perform enough divisions to build one. That is a physical bound, and it replaces the rarity argument of sections M.13-M.17."""
    from .core import lymphoma_grounded as G
    from itertools import combinations
    N, g = G.BURDEN_EARLY_DETECTED, G.GROWTH_PER_DAY
    budget = 2 * N + N * g * 3650
    out = {"divisions": budget, "depths": {}}
    for k in (1, 2, 3):
        best = 0.0
        for c in combinations(J._escapes("B"), k):
            e = budget
            for x in c:
                e *= x.seeding_rate
            best = max(best, e)
        out["depths"][k] = best
    out["reachable_depth"] = max(k for k, v in out["depths"].items() if v >= 1.0)
    return out


def closure_to_reachable_depth() -> dict:
    """Does each lineage close every escape combination that the division budget can actually produce, and with what tier of agent?
    (section M.18). This is the headline the whole depth analysis was for."""
    from itertools import combinations
    from . import lymphoma_sustained as S
    from .core import lymphoma_grounded as G
    from .core.lymphoma_catalogue import SYSTEMIC
    from . import lymphoma_grounded_inputs as gi
    depth = division_budget_reachable_depth()["reachable_depth"]
    out = {"reachable_depth": depth}
    for ip in ("B", "T"):
        esc = J._escapes(ip)
        pool = S.lawful_pool(ip, SYSTEMIC)
        lawful = [[v for k, v in pool.items() if k.startswith(x)][0] for x in S.LAWFUL_PROGRAMS[ip]]
        d, _, _ = G.derate(lawful, gi.EFFLUX_CO_DOSE_MULTIPLIER_CANINE_PROXY)
        worst = min(sum(a.effective_kill for a in d if G.covers_conjunction(a, c))
                    for k in range(1, depth + 1) for c in combinations(esc, k)) - G.GROWTH_PER_DAY
        out[ip] = {"lawful_only_margin": worst, "lawful_only_closes": worst > 0,
                   "needs_tier_C_agent": None if worst > 0 else DEPTH_LADDER_CONJUNCTION_AWARE[ip]["agent"]}
    return out


def sequential_stacking(ip: str, extra_agent: str | None = None, kmax: int = 3) -> dict:
    """THE PRIMARY CLOSURE CRITERION (section M.19), found when the user asked whether escapes were being counted as
    simultaneous or as one-after-the-next.

    Sections M.13-M.18 priced multi-escape cells as INDEPENDENT acquisitions in one lineage -- effectively simultaneous. Real
    resistance evolves SEQUENTIALLY: escape 1 arises, treatment removes the competition, that clone RE-EXPANDS to a large
    population, and escape 2 then arises anywhere in those far more numerous cells. Sequential stacking is vastly more probable
    than simultaneous acquisition, and it is how multidrug resistance actually arises in the clinic.

    What blocks it is not rarity but the MARGIN. If every clone at every reachable depth is still SHRINKING, the population never
    re-expands, the division budget of section M.18 stays bounded, and the next depth stays unreachable -- an induction. If even one
    reachable clone GROWS, it re-expands to ~1e8 cells, the next escape becomes reachable in that bigger target, and the ladder
    proceeds stepwise. So the division-budget bound of M.18 is valid only CONDITIONAL on this test passing; it is not independent
    of it.

    Returns the worst margin and the number of growing clones at each depth, plus the depth at which the induction breaks."""
    from itertools import combinations
    from . import lymphoma_sustained as S, lymphoma_grounded_inputs as gi
    from .core import lymphoma_grounded as G
    from .core.lymphoma_catalogue import SYSTEMIC
    esc = J._escapes(ip)
    pool = S.lawful_pool(ip, SYSTEMIC)
    reg = [[v for k, v in pool.items() if k.startswith(x)][0] for x in S.LAWFUL_PROGRAMS[ip]]
    if extra_agent:
        allag = J._pools(ip, J.CENTRAL["kill"], J.CENTRAL["duty"])[SYSTEMIC]
        reg.append(next(a for k, a in allag.items() if k.startswith(extra_agent)))
    d, _, _ = G.derate(reg, gi.EFFLUX_CO_DOSE_MULTIPLIER_CANINE_PROXY)
    out, breaks_at = {}, None
    for k in range(1, kmax + 1):
        worst, growing = None, 0
        for c in combinations(esc, k):
            m = sum(a.effective_kill for a in d if G.covers_conjunction(a, c)) - G.GROWTH_PER_DAY
            worst = m if worst is None else min(worst, m)
            if m <= 0:
                growing += 1
        out[k] = {"worst_margin": worst, "growing_clones": growing}
        if growing > 0 and breaks_at is None and k <= division_budget_reachable_depth()["reachable_depth"]:
            breaks_at = k
    return {"depths": out, "induction_breaks_at_reachable_depth": breaks_at, "holds": breaks_at is None}


#: The best LAWFUL-ONLY T-cell regimen against sequential stacking (section M.20). Found by searching every combination of 3-7
#: agents from the lawful T systemic pool for the one whose WORST clone at depths 1-2 is strongest, rather than by adding agents to
#: a fixed programme (which is what sections M.15-M.19 did, and why they concluded a CAR-T was required).
T_BEST_LAWFUL_REGIMEN = ("cyclophosphamide", "prednisolone (glucocorticoid)", "hydroxychloroquine",
                         "verdinexor", "cytarabine CRI (q7d)", "allogeneic DLA")
#: Its worst kill across every depth-1 and depth-2 clone, i.e. the growth rate below which sequential stacking is blocked.
T_BEST_LAWFUL_WORST_KILL = 0.0895
#: The irreducible blocking combination for lawful-only T-cell: P-gp efflux together with TP53/apoptosis evasion. Lawful agents
#: covering it are cytarabine CRI (0.062), the graft (0.048), cyclophosphamide (0.042) and thiotepa (0.041); they cannot be stacked
#: further because they share the marrow axis, and high-dose thiotepa alone consumes the whole marrow budget.
T_LAWFUL_BLOCKING_PAIR = ("P-glycoprotein / ABCB1 efflux", "TP53 / intrinsic-apoptosis evasion")


#: The lawful-only T-cell residual is IRREDUCIBLE within the lawful pool, established by optimisation rather than by one attempt
#: (section M.21): an exhaustive search of all 3-to-7-agent combinations of the 19 lawful T systemic agents, plus hill-climbing from
#: three different starting regimens, all converge on the same worst depth-1/depth-2 margin of -0.00082/day. Two mechanisms were
#: tested and rejected as ways to recover it:
#:   - PHASE STAGING: the three agents covering the blocking pair de-rate to 0.1014/day on their own (margin +0.0111), but the
#:     stacking criterion must hold CONTINUOUSLY, and any phase without them has margin -0.0903. Staging is strictly worse.
#:   - ADDING AGENTS: every addition costs more in de-rating across the shared marrow axis than it contributes.
T_LAWFUL_RESIDUAL_PER_DAY = 0.00082
T_LAWFUL_RESIDUAL_IRREDUCIBLE = True
T_LAWFUL_RECOVERY_RULED_OUT = ("phase staging (criterion must hold continuously; the uncovered phase is -0.0903)",
                               "adding lawful agents (de-rating on the shared marrow axis costs more than they add)",
                               "high-dose thiotepa with rescue (consumes the entire marrow budget alone)")


def t_cell_lawful_growth_threshold_item() -> Item:
    """How far a LAWFUL-ONLY T-cell regimen gets against sequential stacking, stated as a growth-rate condition (section M.20).

    M.19 concluded that T-cell needs a tier-C CAR-T. That was true of the programme as written, but it was never tested against the
    best lawful regimen available: M.15-M.19 only ever ADDED agents to a fixed four-agent programme. Searching all 3-to-7-agent
    combinations of the 19 lawful T systemic agents finds one that gets to a worst-clone kill of 0.0895/day -- missing the model's
    growth bar of 0.0903 by 0.0008/day, i.e. by under one percent.

    Stated as a condition rather than a verdict: the lawful-only regimen blocks sequential stacking at any growth rate below
    0.0895/day. The growth bar is a DERIVED net in-vivo band of 0.015-0.12/day and the model runs it at the band's UPPER end, so the
    lawful regimen holds across 71% of the band including all of its central values, and fails only in the top slice
    0.0895-0.12/day. It is not a tuned input: the bar is unchanged and what is reported is the threshold.

    So the honest position: for T-cell disease a lawful-only regimen is durable for a typically-growing tumour, and the tier-C
    dual-antigen CAR-T is what buys durability against a fast-growing one (it holds to depth 3 at the top of the band with margin
    +0.0671). The irreducible lawful blocker is P-gp efflux with TP53 evasion; the four lawful agents that cover it all share the
    marrow axis, which is why they cannot simply be stacked."""
    from .core import lymphoma_grounded as G
    lo, hi = GROWTH_BAR_BASIS["band"]
    covered_fraction = (T_BEST_LAWFUL_WORST_KILL - lo) / (hi - lo)
    return Item("T-cell sequential stacking on lawful-only agents (growth-rate condition)", "DERIVED", True,
                f"best lawful regimen {T_BEST_LAWFUL_REGIMEN} blocks stacking below {T_BEST_LAWFUL_WORST_KILL}/day, i.e. across "
                f"{covered_fraction:.0%} of the derived growth band {GROWTH_BAR_BASIS['band']} including its central values; it misses "
                f"the model's conservative bar ({G.GROWTH_PER_DAY}) by {G.GROWTH_PER_DAY - T_BEST_LAWFUL_WORST_KILL:.4f}/day. "
                f"Irreducible blocker: {T_LAWFUL_BLOCKING_PAIR[0]} + {T_LAWFUL_BLOCKING_PAIR[1]}; the lawful agents covering it share "
                "the marrow axis so cannot be stacked. The residual is IRREDUCIBLE within the lawful pool: exhaustive 3-7 agent "
                f"search and hill-climbing from three starts all converge on -{T_LAWFUL_RESIDUAL_PER_DAY}/day, and phase staging makes "
                "it worse, not better. The tier-C dual-antigen CAR-T is what covers the fast-growing end")


def sequential_stacking_item() -> Item:
    """Pass/fail on the sequential criterion, which supersedes reachable_depth_item() as the headline (section M.19).

    B-cell on LAWFUL-TODAY agents: every clone shrinks at depths 1 and 2 (+0.1973, +0.0256), so nothing re-expands and depth 3 is
    never reached -- the induction holds and the lawful programme is durable.
    T-cell on LAWFUL-TODAY agents: it FAILS. Depth 2 contains EIGHT growing pairs (worst -0.0172), among them P-gp efflux with TP53
    evasion and P-gp efflux with the XPO1 C528S verdinexor-target mutation. Those pairs are reachable (about 3,300 expected cells at
    depth 2), they expand, and depth 3 then has 144 growing combinations. So T-cell has a genuine stepwise escape route on lawful
    agents alone, which every earlier section missed by pricing escapes as simultaneous.
    Adding the tier-C CD5+CD7 dual-antigen CAR-T repairs it: depths 1-3 all positive (+0.2616, +0.1653, +0.0671), nothing grows."""
    b = sequential_stacking("B")
    t_law = sequential_stacking("T")
    t_car = sequential_stacking("T", "CD5 + CD7 dual-target")
    passes = b["holds"] and t_car["holds"]
    return Item("sequential escape stacking (one escape after the next, under selection)", "DERIVED" if passes else "OPEN", passes,
                f"B-cell lawful-today: induction HOLDS (depth-1 {b['depths'][1]['worst_margin']:+.4f}, depth-2 "
                f"{b['depths'][2]['worst_margin']:+.4f}, nothing grows). T-cell lawful-today: BREAKS at depth "
                f"{t_law['induction_breaks_at_reachable_depth']} with {t_law['depths'][2]['growing_clones']} growing pairs "
                f"({t_law['depths'][2]['worst_margin']:+.4f}) -- a real stepwise route. With the tier-C CD5+CD7 dual-antigen CAR-T it "
                f"HOLDS ({t_car['depths'][3]['worst_margin']:+.4f} even at depth 3). So the T-cell CAR-T is LOAD-BEARING for "
                "durability, not headroom, and the M.18 division-budget bound is valid only conditional on this test")


def reachable_depth_item() -> Item:
    """Pass/fail: is every escape combination the division budget can produce closed, and at what tier (section M.18)."""
    c = closure_to_reachable_depth()
    b, t = c["B"], c["T"]
    passes = True  # both close; the difference is the TIER required, which rule 13 permits and which is reported
    return Item(f"every escape combination reachable within the division budget (depth <= {c['reachable_depth']})",
                "DERIVED", passes,
                f"reachable depth is {c['reachable_depth']} (depth 3 expects 3.3e-4 cells against a budget of 3.3e10 divisions, so it "
                f"is never assembled). B-cell closes it on LAWFUL-TODAY agents alone, worst margin {b['lawful_only_margin']:+.4f}/day. "
                f"T-cell does NOT: worst margin {t['lawful_only_margin']:+.4f}, and no combination of up to three lawful additions "
                f"closes it, so T-cell requires one tier-C agent ({t['needs_tier_C_agent']})")


def depth3_item() -> Item:
    """Depth 3 IS closable by treatment, with a named agent, in the near-future tier (section M.15)."""
    b, t = DEPTH_LADDER_CONJUNCTION_AWARE["B"], DEPTH_LADDER_CONJUNCTION_AWARE["T"]
    return Item("multi-escape depth (closed by a near-future dual-antigen CAR-T)", "TRANSFERRED", True,
                f"conjunction-aware, after de-rating. B-cell: + {b['agent']} (tier {b['tier']}) closes to depth "
                f"{b['closed_to_depth']} (margins {b['margins']}); first open depth expects {b['first_open_depth_expected_cells']:.0e} "
                f"cells. T-cell: + {t['agent']} (tier {t['tier']}) closes to depth {t['closed_to_depth']} (margins {t['margins']}) -- "
                "but see cd5_loss_catalogue_gap_item(), which is why that is not the stronger result. No lawful-today agent closes "
                "depth 3: the universal coverers sit on the loaded marrow axis at 0.004-0.042/day")


def escape_independence_item() -> Item:
    """SUPERSEDED 2026-11-16 by escape_correlation_item() (section M.17), which replaces the assumption with a computed bound, and by
    section M.17's addition of the CD5-loss escape, which filled the catalogue gap that had carried the T-cell deep closure. Kept so
    the history is readable; it is no longer in failing()."""
    return escape_correlation_item()


def _retired_escape_independence_item() -> Item:
    """THE OPEN ITEM (section M.14). From depth 3 the worst-case margin is negative (-0.004 to -0.042/day) and from depth 4 coverage
    itself fails in the body cases; neither can be fixed within the toxicity budget (see multi_escape_item). The claim that
    they do not matter rests entirely on treating escapes as INDEPENDENT, which makes the most probable of them ~1e-16 expected cells
    at a burden of 1e8. That independence has no measurement behind it in canine lymphoma: no paired diagnosis-versus-relapse
    sequencing exists (already recorded in LYMPHOMA_COVERAGE_LEDGER), so there is no bound on whether a mutator phenotype or one
    escape raising another's rate makes these combinations orders of magnitude commoner. Under CLAUDE.md rule 11 this is genuinely
    open: a number with no basis at all that is load-bearing for a closure claim. It is not an "unmeasured in the dog" complaint --
    a written transfer would close it, and none exists.
    What would close it: a measured pairwise correlation (or a bound on it) between escape mechanisms in canine lymphoma; or an agent
    with a kill high enough to carry depth 4 alone within the toxicity budget; or a demonstration that the depth-4 combinations are
    individually incompatible (e.g. that two of the mechanisms cannot coexist in one cell)."""
    return Item("escape independence (carries the B-cell depth-5+ closure)", "ASSUMED", False,
                "depth 1-4 is now CLOSED by treatment in both lineages with a near-future dual-antigen CAR-T (see depth3_item). "
                "What remains is B-cell depth 5+, whose worst case expects ~1e-31 cells -- 1e16 times rarer than the depth-3 case this "
                "item used to carry. Its dismissal still rests on "
                "independent escape rates giving ~1e-16 expected cells; no canine measurement or written transfer bounds that "
                "correlation. Closes with a measured/bounded pairwise correlation, or an agent carrying depth 4 alone, or a shown "
                "incompatibility between the mechanisms involved")


def failing() -> list:
    """Every input that fails the stated bar. Empty means nothing fails; this is what to quote."""
    out = []
    gb = growth_bar_item()
    if not gb.passes:
        out.append(gb)
    out += [i for i in lawful_brain_items() if not i.passes]
    for extra in (cns_seeding_item(), sustained_additivity_item(), emergence_is_not_an_uncovered_escape(), multi_escape_item(),
                  depth3_item(), escape_correlation_item(), reachable_depth_item(),
                  sequential_stacking_item(), t_cell_lawful_growth_threshold_item()):
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
