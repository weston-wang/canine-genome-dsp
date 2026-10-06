"""The coverage ledger: for every mechanism and escape, what closes it, at what evidence grade, and
what the toxicity and treatment clock do to that answer.

This is the lymphoma analogue of the HS branch's "coverage by evidence tier" table
(docs/THERAPY_STRATEGY.md there), built on `core/lymphoma_grounded.py`. It answers the user's question
"did we cover all mechanisms and potential escapes, with potency and toxicity considered?" and grades
the answer at the strength actually shown -- separating

    the mechanism is in the model and an agent covers it               (derived coverage)
    the agent's kill rate is derived or measured                       (STRICT)
    the agent's benefit is a measured clinical outcome                 (OUTCOME)
    the closure holds only if an ASSUMED potency holds                 (ASSUMED)

Everything recorded below is RE-DERIVED by tests/test_lymphoma_ledger.py from the model, not pinned as
prose. Numbers depend on assumed inputs where the ledger says so.
"""

from __future__ import annotations

from dataclasses import replace

from .core import lymphoma_grounded as G
from .core.lymphoma_catalogue import (B_LINEAGE_ANTIGENS, BURDEN_CLINICALLY_OBVIOUS, BURDEN_EARLY_DETECTED,
                                      CNS, SYSTEMIC)
from .core.lymphoma_dormancy import CYCLING_FRACTION_SWEEP, RETAINED_TOLERANCE_SWEEP
from .core.lymphoma_toxicity import profile_for

# --- what supports each mechanism's EXISTENCE (separate from whether we can close it) -----------------
EXISTENCE = {
    "P-glycoprotein / ABCB1 efflux": ("MEASURED in canine lymphoma",
        "P-gp-selected canine line resists doxorubicin 6.7x and vincristine 39.6x, prednisolone spared, "
        "fully reversed by PSC833 (PMID 24975508); 55.6% (35/63) of dogs drug-resistant, ABCB1 up in a "
        "subset of B-cell (PMID 25475167); host capillary endothelium turns ABCB1/BCRP-positive after "
        "chemotherapy in 3 relapsed dogs (PMID 33518631)."),
    "BCRP / ABCG2 efflux": ("MEASURED in canine lymphoma",
        "ABCG2 up in T-cell lymphoma at relapse (PMID 25475167)."),
    "TP53 / intrinsic-apoptosis evasion": ("MEASURED, and FOUNDER-CLONAL in a quarter of dogs",
        "TP53 lesion in 25.6% (11/43) of DLBCL by WGS (PMID 39922874); TP53-mutant aggressive B-cell "
        "time-to-progression 52 vs 202 days (PMID 39134766); shorter OS in 238 dogs (PMID 40506464). "
        "A lesion the tumour is born with is not removed by earlier detection."),
    "CD20 antigen loss": ("MEASURED in dogs after CD20 CAR-T",
        "CD20 exons 4-5 absent in the post-treatment tumour (PMID 32002286); CD20-negative clone expanded "
        "in one dog (PMID 38573683, 41376156)."),
    "CD19 antigen loss": ("TRANSFER (human CAR-T)", "Kept so a tandem construct gets no free pass."),
    "BCR / NF-kB signal independence": ("MEASURED lesions, but not uniformly adverse",
        "TRAF3 58.1% of DLBCL (PMID 39922874); NFKBIA in 31/54 intestinal T-cell (PMID 40877743). TRAF3 "
        "mutation is associated with LONGER survival in dogs (PMID 40506464). A BTK inhibitor is defeated "
        "by a lesion at or below it (derived); acalabrutinib PFS 22.5 d (PMID 27434128)."),
    "PI3K / AKT bypass": ("MEASURED expression only",
        "PI3K/AKT enrichment with PTEN down in canine CD4+ PTCL (PMID 38166662)."),
    "drug-tolerant persister (non-dividing)": ("TRANSFER, with a canine proxy",
        "Chemotherapy enriches ALDH-high stem-like cells in canine cell lines and relapsed dogs "
        "(PMID 30238600). The non-dividing state itself is not measured in canine lymphoma; f and r are swept."),
    "autophagy independence": ("ASSUMED", "No canine measurement."),
    "T-cell exhaustion / immunosuppressive microenvironment": ("MEASURED association, one counter-result",
        "PD-1/PD-L1 up in chemotherapy-resistant canine lines (PMID 29380929); higher PD-L1/PD-1 scores "
        "and higher relapse risk (PMID 34209830); PD-L1 mRNA not prognostic (PMID 30085860)."),
    "B-lineage identity switch": ("MEASURED-adjacent (diagnostic series, not relapse)",
        "Cross-lineage CD3+/CD20+ cases (PMID 37837199, 40331223); Richter transformation in CLL "
        "(PMID 26463596)."),
    "antigen-presentation loss (MHC-I/II, B2M, CD58)": ("MEASURED association in dogs; relapse lesions HUMAN",
        "Low MHC-II predicts relapse in 160 dogs (PMID 21781170); B2M/CD58 lesions acquired at relapse in "
        "humans (PMID 25123191)."),
    "MGMT alkylator repair (nitrosourea resistance)": ("MEASURED in canine cell lines",
        "MGMT activity may influence nitrosourea sensitivity (PMID 26130852)."),
}

#: The mechanisms the completeness check raised that are NOT escape lineages, and how each is handled.
NOT_LINEAGES = {
    "host rejection of a mouse-derived CAR (canine anti-mouse antibody)":
        ("MEASURED in dogs (PMID 32002286, 35898541)",
         "A cap on that agent's duration (CAR-T sustainable 50 d), not a lineage the regimen must kill."),
    "clonal evolution / pre-existing subclones":
        ("HUMAN only (PMID 25123191); no paired canine diagnosis-vs-relapse sequencing found",
         "Already the supply model behind the seeding rates and the Monte Carlo engine; not a new agent."),
    "host endothelial efflux ('blood-tumour barrier')":
        ("MEASURED in 3 dogs (PMID 33518631)", "Same rule as P-gp: non-substrate agents are unaffected."),
    "chemotherapy-selected stem-like cells":
        ("MEASURED in dogs (PMID 30238600, 23820219)", "A variant of the persister state."),
    "second cancers after cure":
        ("MEASURED: 4 of 6 long-term survivors died of another cancer, 3 osteosarcoma (PMID 21320018)",
         "A limit on durability the regimen does not touch; causation by chemotherapy or TBI not shown."),
    "genomic-instability predictors of CAR-T failure":
        ("HUMAN only (PMID 35476848)", "Not modelled; no canine data."),
}


def _regimen(comp, ip, names):
    ag = {a.name: a for a in G.grounded_agents(comp, ip)}
    return [ag[next(k for k in ag if k == n or k.startswith(n.split(" (")[0]))] for n in names]


def _escapes(ip, burden=BURDEN_EARLY_DETECTED):
    esc = G.escapes_to_close(burden)
    return tuple(e for e in esc if not (ip == "T" and e.removes_antigen in B_LINEAGE_ANTIGENS))


#: Recommended sets, chosen by the search (see `minimal_sets`), recorded here and re-derived by tests.
LEDGER_REGIMENS = {
    "B-cell, best with no assumed potency (trial-stage antibody)":
        (SYSTEMIC, "B", ("doxorubicin", "anti-CD20 monoclonal antibody", "verdinexor (XPO1 inhibitor)")),
    "B-cell, off-label agents only, some potencies ASSUMED":
        (SYSTEMIC, "B", ("doxorubicin", "prednisolone (glucocorticoid)", "hydroxychloroquine (autophagy)")),
    "T-cell, no assumed potency":
        (SYSTEMIC, "T", ("doxorubicin", "vincristine", "venetoclax (BCL2 inhibitor)")),
    "B-cell body, licensed and off-label agents only: HCQ + verdinexor":
        (SYSTEMIC, "B", ("hydroxychloroquine (autophagy)", "verdinexor (XPO1 inhibitor)")),
    "B-cell body with the trial-stage antibody: HCQ + verdinexor + antibody":
        (SYSTEMIC, "B", ("hydroxychloroquine (autophagy)", "verdinexor (XPO1 inhibitor)",
                         "anti-CD20 monoclonal antibody")),
    "T-cell body: HCQ + verdinexor + venetoclax":
        (SYSTEMIC, "T", ("hydroxychloroquine (autophagy)", "verdinexor (XPO1 inhibitor)",
                         "venetoclax (BCL2 inhibitor)")),
    "B-cell CNS: HCQ + continuous intrathecal cytarabine":
        (CNS, "B", ("hydroxychloroquine (autophagy)", "continuous intrathecal cytarabine")),
    "T-cell CNS: HCQ + venetoclax + continuous intrathecal cytarabine":
        (CNS, "T", ("hydroxychloroquine (autophagy)", "venetoclax (BCL2 inhibitor)",
                    "continuous intrathecal cytarabine")),
}


THIN = 0.02      # a margin under this many per day is inside the noise of every assumed input


def _closed_on(m_strict: float, m_outcome: float, m_all: float) -> str:
    """The strictest evidence tier on which the escape closes, flagged THIN when the margin there is
    smaller than the uncertainty of the inputs beneath it."""
    if m_strict > 0:
        label, m = "strict-grade potency alone", m_strict
    elif m_outcome > 0:
        label, m = "outcome-grade potency", m_outcome
    elif m_all > 0:
        label, m = "ASSUMED potency only", m_all
    else:
        return "NOT CLOSED"
    return label + (f" (THIN, <{THIN}/day)" if m < THIN else "")


#: The closing PROGRAMS: a body regimen and a CNS regimen given together. Found by the sound-grade search
#: (potencies measured, derived or transferred with a written basis; no bare assumptions), then stress-tested.
PROGRAMS = {
    "B-cell": ("B", ("hydroxychloroquine", "verdinexor", "continuous intrathecal", "anti-CD20")),
    "B-cell, no trial-stage antibody": ("B", ("hydroxychloroquine", "verdinexor", "continuous intrathecal")),
    "T-cell, existing drugs plus the pump": ("T", ("hydroxychloroquine", "verdinexor", "venetoclax",
                                                   "continuous intrathecal")),
    "T-cell, with a T-lineage CAR-T": ("T", ("hydroxychloroquine", "verdinexor", "continuous intrathecal",
                                             "CD7-directed")),
}


def _pick(comp, ip, names, mod=None):
    ag = {a.name: a for a in G.grounded_agents(comp, ip)}
    out = []
    for n in names:
        k = next((k for k in ag if k.startswith(n)), None)
        if k is None:
            continue                       # the agent does not exist in this compartment (e.g. the pump in the body)
        a = ag[k]
        out.append(mod(a) if mod else a)
    return out


def program_report(label: str) -> dict:
    """Body and CNS clearing, union organ loads, and the stress tests, for one program."""
    from .core.lymphoma_toxicity import axis_loads
    ip, names = PROGRAMS[label]
    esc = _escapes(ip, BURDEN_EARLY_DETECTED)
    esc = tuple(e for e in G.GROUNDED_ESCAPES if not (ip == "T" and e.removes_antigen in B_LINEAGE_ANTIGENS)
                and not (ip == "B" and e.removes_antigen == "CD7"))            # EVERY escape, not just the likely ones
    out = {"label": label, "agents": names}
    for comp, key in ((SYSTEMIC, "body"), (CNS, "cns")):
        r = _pick(comp, ip, names)
        ev = G.evaluate_best_schedule(r, esc, burden=BURDEN_EARLY_DETECTED, compartment=comp)
        out[key] = {"agents": tuple(a.name for a in r), "margin": ev.worst_derated, "weakest": ev.weakest,
                    "verdict": ev.horizon_strict.verdict(), "clear_day": ev.horizon_strict.clear_day,
                    "closes": ev.closes and ev.horizon_strict.cure_inside_window,
                    "halved_potency_clears": G.clears(G.discounted(r, 0.5), esc, burden=BURDEN_EARLY_DETECTED,
                                                      compartment=comp),
                    "any_one_removed_clears": all(G.clears(r[:i] + r[i + 1:], esc, burden=BURDEN_EARLY_DETECTED,
                                                           compartment=comp) for i in range(len(r)) if len(r) > 1)}
        if comp == CNS:
            out[key]["capacity_cells"] = G.cns_capacity(r, esc)
    r = _pick(SYSTEMIC, ip, names)
    clin = G.evaluate_best_schedule(r, esc, burden=BURDEN_CLINICALLY_OBVIOUS, compartment=SYSTEMIC)
    out["body_at_clinical_burden"] = clin.horizon_strict.verdict()
    union = _pick(CNS, ip, names) + [a for a in r if a.name not in {x.name for x in _pick(CNS, ip, names)}]
    out["union_loads"] = {k.name.lower(): round(v, 2) for k, v in
                          axis_loads(G.regimen_profiles(union, G.gi.EFFLUX_CO_DOSE_MULTIPLIER_CANINE_PROXY)).items()}
    out["grades"] = {a.name: G.potency_grade(a) for a in union}
    return out


def escape_ledger(comp: str, ip: str, names, burden: float = BURDEN_EARLY_DETECTED) -> list:
    """One row per escape for a named regimen: carriers, margins at three evidence strictnesses, and
    single points of failure. Margins are after toxicity de-rating."""
    reg = _regimen(comp, ip, names)
    esc = _escapes(ip, burden)
    d_agents, factors, _ = G.derate(reg, G.gi.EFFLUX_CO_DOSE_MULTIPLIER_CANINE_PROXY)
    grade = {a.name: G.potency_grade(a) for a in reg}
    rows = []
    for e in esc:
        carriers = []
        for a in d_agents:
            k = G.kill_against([a], e) if e.requires_division else (
                a.effective_kill if a.covers(e) and a.effective_kill > 0 else 0.0)
            if k > 0:
                carriers.append((a.name, round(k, 4), grade[a.name]))
        m_all = G.margin_for(d_agents, e)
        m_strict = G.margin_for([a for a in d_agents if grade[a.name] in G.STRICT_GRADES], e)
        m_outcome = G.margin_for([a for a in d_agents if grade[a.name] in G.OUTCOME_GRADES], e)
        spof = []
        for i, a in enumerate(d_agents):
            rest = [x for j, x in enumerate(d_agents) if j != i]
            if rest and G.margin_for(rest, e) <= 0.0 < m_all:
                spof.append(a.name)
        rows.append({
            "escape": e.name, "existence": EXISTENCE.get(e.name, ("", ""))[0],
            "existence_source": EXISTENCE.get(e.name, ("", ""))[1],
            "carriers": carriers, "margin_all": round(m_all, 4), "margin_strict_only": round(m_strict, 4),
            "margin_outcome_or_better": round(m_outcome, 4), "single_points_of_failure": spof,
            "founder": e.name in G.FOUNDER_ESCAPES,
            "closed_on": _closed_on(m_strict, m_outcome, m_all),
        })
    return rows


def regimen_summary(comp: str, ip: str, names, burden: float = BURDEN_EARLY_DETECTED) -> dict:
    reg = _regimen(comp, ip, names)
    ev = G.evaluate(reg, _escapes(ip, burden), burden=burden, clock=True, compartment=comp)
    return {"agents": ev.names, "worst_margin": ev.worst_derated, "weakest": ev.weakest,
            "derated": ev.derated, "axis_loads": ev.loads, "tightest_axis_headroom": ev.headroom,
            "strict_window": ev.horizon_strict.verdict(),
            "clear_day_strict": ev.horizon_strict.clear_day,
            "extended_window": ev.horizon_extended.verdict(),
            "assumed_potencies": ev.assumed, "availability": ev.availability,
            "windows": {a.name: (profile_for(a.name).sustainable_days, profile_for(a.name).hard_cap_days)
                        for a in reg}}


def potency_headroom(comp: str, ip: str, names, burden: float = BURDEN_EARLY_DETECTED) -> dict:
    """Smallest fraction of its own potency each agent can fall to (others fixed) before the regimen
    stops clearing inside the strict window. 1.0 means no room at all; 0.0 means it is redundant."""
    reg = _regimen(comp, ip, names)
    esc = _escapes(ip, burden)
    out = {}
    for i, a in enumerate(reg):
        lo, hi = 0.0, 1.0
        for _ in range(30):
            mid = (lo + hi) / 2
            trial = list(reg)
            trial[i] = replace(a, potency=a.potency * mid)
            ev = G.evaluate(trial, esc, burden=burden, clock=True, compartment=comp)
            if ev.closes and ev.horizon_strict.cure_inside_window:
                hi = mid
            else:
                lo = mid
        out[a.name] = round(hi, 3)
    return out


def dormancy_sweep(comp: str, ip: str, names, burden: float = BURDEN_EARLY_DETECTED) -> dict:
    """(f, r) -> (persister margin, cleared inside strict window?)."""
    reg = _regimen(comp, ip, names)
    esc = _escapes(ip, burden)
    out = {}
    for f in CYCLING_FRACTION_SWEEP:
        for r in RETAINED_TOLERANCE_SWEEP:
            ev = G.evaluate(reg, esc, f=f, r=r, burden=burden, clock=True, compartment=comp)
            out[(f, r)] = (round(ev.margins_derated["drug-tolerant persister (non-dividing)"], 4),
                           ev.horizon_strict.cure_inside_window)
    return out


def calibration_chop(prednisolone_potency: float | None = None) -> dict:
    """The check against known clinical outcome: CHOP alone at a clinically obvious burden must NOT
    be predicted to cure (median PFS 176 d, PMID 26279153; ~10% alive at 2 y, PMID 21320018)."""
    ag = {a.name: a for a in G.grounded_agents(SYSTEMIC, "B")}
    names = ("doxorubicin", "vincristine", "cyclophosphamide", "prednisolone (glucocorticoid)")
    reg = [replace(ag[n], potency=prednisolone_potency) if (prednisolone_potency is not None
                                                            and n.startswith("prednisolone")) else ag[n]
           for n in names]
    ev = G.evaluate(reg, G.escapes_to_close(BURDEN_CLINICALLY_OBVIOUS), burden=BURDEN_CLINICALLY_OBVIOUS,
                    clock=True)
    hz = ev.horizon_strict
    return {"cured": hz.cure_inside_window, "verdict": hz.verdict(),
            "pgp_margin": ev.margins_derated["P-glycoprotein / ABCB1 efflux"],
            "relapse_days": sorted((o.name, o.day) for o in hz.relapsing)}


def minimal_sets(comp: str, ip: str, tier: str, grades=None, max_n: int = 5, top: int = 400) -> list:
    """Smallest regimens the clock says clear every lineage inside the documented windows, fewest
    agents first, then best margin."""
    pool = [a for a in G.available(G.grounded_agents(comp, ip), tier)
            if grades is None or G.potency_grade(a) in grades]
    res = G.search(comp, ip, tier, pool=pool, max_n=max_n, top=top)
    cured = sorted(res["cured_inside_window"], key=lambda e: (len(e.agents), -e.worst_derated))
    return cured
