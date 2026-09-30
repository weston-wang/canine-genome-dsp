"""The lymphoma catalogue and search rebuilt on the HS method's potency, toxicity, provenance and
treatment-clock machinery.

This module answers one question, the user's: "did we cover all mechanisms and potential escapes, with
potency and toxicity considered?" It does NOT replace `lymphoma_catalogue` / `lymphoma_search`; those
remain the recorded v1 results, and this is run beside them so the difference is visible.

WHAT IS DIFFERENT FROM v1, EACH ITEM TRACEABLE TO AN HS COMPONENT

  potency      graded per agent by `potency_evidence` (DERIVED / PARTIAL / HINGE / BRACKET / OUTCOME /
               ASSUMED) from `lymphoma_grounded_inputs` (HS `pkpd.py`, `evidence.py`). The v1 potency is
               kept where nothing was measured, and labelled ASSUMED.
  toxicity     every regimen is charged organ-axis budgets (HS `toxicity.py`, `tolerable_search.py`);
               same-axis agents add; an over-budget axis forces a cut and the regimen is RE-SCORED at the
               de-rated kill; a P-gp reverser multiplies its partners' load.
  persister    scored as a two-state pool (`lymphoma_dormancy`, HS `dormancy.py` corrected), swept over
               awake fraction f and retained tolerance r; v1's wall is the f=1, r=1 corner.
  clock        `lymphoma_horizon` (HS `response_duration.py`, `treatment_horizon.py`): can each agent that
               carries a margin be given for as long as clearing takes? Otherwise response-then-relapse.
  reversal     P-gp reversal is a MECHANISM (substrates regain coverage of the pump clone when a reverser
               is present) rather than a free-standing 0.08/day agent.
  escapes      two more, from the completeness check: loss of antigen PRESENTATION (defeats endogenous-
               T-cell agents) and MGMT repair (defeats lomustine). Host rejection of a mouse-derived
               CAR is NOT an escape lineage; it is a measured cap on that agent's duration, carried in the
               toxicity/horizon table.
  founders     escapes with a measured FOUNDER prevalence (TP53 ~26%, TRAF3 ~58% of B-cell dogs) are kept
               in the set to close even at an early-detection burden, because earlier detection cannot
               remove a lesion the tumour was born with.

WHAT IT CANNOT DO. Potencies that are ASSUMED are still assumed; the search says how many a regimen
rests on. Toxicity budgets are ordinal judgements, not predictions. The clock is mean-field. See
docs/LYMPHOMA_STATUS.md and docs/LYMPHOMA_COVERAGE_LEDGER.md for the accounting.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field, replace
from itertools import combinations

from .. import lymphoma_grounded_inputs as gi
from . import lymphoma_toxicity_profiles  # noqa: F401  (populates PROFILES)
from .lymphoma_catalogue import (BURDEN_CLINICALLY_OBVIOUS, BURDEN_EARLY_DETECTED, BURDEN_MRD, CELL_ACCESS,
                                 CNS, ESCAPES as V1_ESCAPES, GLUCOCORTICOID_ACCESS, GROWTH_PER_DAY,
                                 RADIATION_ACCESS, SMALL_MOLECULE_ACCESS, SYSTEMIC, agents_for,
                                 B_LINEAGE_ANTIGENS)
from .lymphoma_dormancy import (CYCLING_FRACTION_DEFAULT, RETAINED_TOLERANCE_DEFAULT, persister_margin)
from .lymphoma_horizon import HorizonResult, horizon
from .lymphoma_toxicity import (PROFILES, axis_loads, derating_for, headroom, oversubscribed, profile_for,
                                with_efflux_co_dose)
from .regimen import Agent, Axis, Escape, Layer, escape_presence_probability

# --- availability tiers ---------------------------------------------------------------------------
LICENSED, OFF_LABEL, TRIAL, PRECLINICAL, NONE = ("licensed", "off-label", "trial in dogs",
                                                 "preclinical", "does not exist")
TIER_ALLOWS = {"off-label": {LICENSED, OFF_LABEL}, "trial": {LICENSED, OFF_LABEL, TRIAL},
               "any": {LICENSED, OFF_LABEL, TRIAL, PRECLINICAL, NONE}}

AVAILABILITY = {
    "doxorubicin": LICENSED, "vincristine": LICENSED, "cyclophosphamide": LICENSED,
    "cyclophosphamide (metronomic)": OFF_LABEL,
    "prednisolone (glucocorticoid)": LICENSED, "prednisolone (maintenance dose)": OFF_LABEL,
    "rabacfosadine": LICENSED, "lomustine (CNS-penetrant nitrosourea)": LICENSED,
    "high-dose methotrexate": OFF_LABEL, "intrathecal cytarabine": OFF_LABEL,
    "craniospinal radiotherapy": OFF_LABEL, "half-body irradiation (low-dose-rate)": OFF_LABEL,
    "total body irradiation + transplant": OFF_LABEL,
    "anti-CD20 monoclonal antibody": TRIAL, "CD20 CAR-T": TRIAL,
    "tandem CD19/CD20 CAR-T": PRECLINICAL,
    "CD20 CAR-T with PD-1/CD28 switch receptor": PRECLINICAL,
    "persistence-engineered canine-binder CAR-T (specification)": NONE,
    "anti-PD-1 / anti-PD-L1 checkpoint blockade": OFF_LABEL,
    "hydroxychloroquine (autophagy)": OFF_LABEL, "venetoclax (BCL2 inhibitor)": OFF_LABEL,
    "acalabrutinib (BTK)": OFF_LABEL, "verdinexor (XPO1 inhibitor)": LICENSED,
    "cytarabine CRI (q14d)": OFF_LABEL, "cytarabine CRI (q7d)": OFF_LABEL,
    "continuous intrathecal cytarabine (pump) [buildable]": NONE,
    "CD7-directed CAR-T (canine binder, fratricide-resistant) [buildable]": NONE,
    "CD5 + CD7 dual-target CAR-T (canine binder) [buildable]": NONE,
    "P-gp / TGF-beta-inhibitor chemosensitiser": TRIAL,
    "CD5/CD52-directed cellular effector (T-lineage)": NONE,
}

REVERSER = "P-gp / TGF-beta-inhibitor chemosensitiser"
#: escapes with a measured founder prevalence; kept in the set even at an early-detection burden.
FOUNDER_ESCAPES = ("TP53 / intrinsic-apoptosis evasion", "BCR / NF-kB signal independence")

NEW_ESCAPES = (
    Escape("antigen-presentation loss (MHC-I/II, B2M, CD58)", Axis.IMMUNE_EFFECTOR, Layer.RECEPTOR, 1e-8,
           defeats=frozenset({"antigen_presentation"}),
           evidence="Low MHC-II predicts relapse in 160 dogs (PMID 21781170); B2M/CD58 lesions acquired "
                    "at relapse are HUMAN (PMID 25123191). Rate ASSUMED.",
           note="Defeats agents that need an endogenous T-cell to recognise the tumour (checkpoint "
                "blockade, non-CAR adoptive T cells). Does not defeat a CAR or an antibody, which are "
                "MHC-independent."),
    Escape("MGMT alkylator repair (nitrosourea resistance)", Axis.CYTOTOXIC, Layer.RECEPTOR, 1e-8,
           defeats=frozenset({"mgmt_repair"}),
           evidence="MGMT activity may influence nitrosourea sensitivity in canine lymphoma cell lines "
                    "(PMID 26130852). Rate ASSUMED.",
           note="Matters only if lomustine is a closing agent."),
)
CD7_LOSS = Escape("CD7 antigen loss (T-lineage CAR relapse)", Axis.IMMUNE_EFFECTOR, Layer.RECEPTOR, 1e-8,
                  antigen_intact=False, removes_antigen="CD7", evidence="HUMAN: 4 of 6 relapses after donor-derived "
                  "CD7 CAR-T had lost CD7 (PMID 37020231); lineage-switch relapses also seen (PMID 42810712).",
                  note="Only meaningful for T-cell disease with a CD7-directed agent; a CD5+CD7 construct covers it.")
GROUNDED_ESCAPES = tuple(V1_ESCAPES) + NEW_ESCAPES + (CD7_LOSS,)
PGP = next(e for e in V1_ESCAPES if "P-glycoprotein" in e.name)
PERSISTER = next(e for e in V1_ESCAPES if not e.requires_division)


# --- the grounded agents --------------------------------------------------------------------------

_POTENCY_TEXT = {
    "doxorubicin": "REGIMEN-CALIBRATED: only the CHOP SUM is anchored to outcome (PMID 26279153); this "
                   "agent's own kill is not measured. The plasma-AUC/IC50 method gives ~0.24 e-folds per "
                   "dose and cannot reproduce CHOP's activity, so it is a lower bound.",
    "vincristine": "REGIMEN-CALIBRATED (as doxorubicin); ~0.37 e-folds/dose by the plasma method.",
    "cyclophosphamide": "REGIMEN-CALIBRATED. 4-HC LD50 in CLBL-1 differs 87x between laboratories "
                        "(0.14 vs 12.19 uM), so no derivation is defensible; its kill on the P-gp lineage "
                        "is not separately measured.",
    "prednisolone (glucocorticoid)": "BRACKET: 0.0098-0.144 /day from two canine measurements that "
                                     "disagree ~15x; 0.10 neither derived nor contradicted.",
    "rabacfosadine": "ASSUMED: no canine IC50 or PK found; clinical ORR 87%, median PFI 122 d.",
    "lomustine (CNS-penetrant nitrosourea)": "ASSUMED: one line IC50 (27 uM), no canine PK found.",
    "high-dose methotrexate": "ASSUMED (human transfer).",
    "intrathecal cytarabine": "ASSUMED.",
    "craniospinal radiotherapy": "ASSUMED (radiobiology transfer).",
    "anti-PD-1 / anti-PD-L1 checkpoint blockade": "ASSUMED (melanoma transfer).",
    "hydroxychloroquine (autophagy)": "HINGE: tumour ~31 uM measured (100x plasma); closes only if the "
                                      "canine-lymphoma IC50 is <= ~100 uM. IC50 NOT FOUND.",
    "acalabrutinib (BTK)": "ASSUMED: BTK occupancy >90% measured but killing 'modest'; no cell-killing "
                           "IC50; clinical PFS 22.5 d.",
    "total body irradiation + transplant": "OUTCOME: durable remission fractions measured "
                                           "(PMID 34950726, 22882500, 24467413); no kill rate.",
    "anti-CD20 monoclonal antibody": "MEASURED in dogs: CD21+ B cells fall 0.099 /day (day 7-21) after "
                                     "the first 0.46 /day (PMID 38662527). Normal B cells in blood, "
                                     "with chemotherapy; nodal tumour access not measured.",
    "CD20 CAR-T": "ASSUMED in vivo. In-vitro lysis near-complete at E:T 5:1 (PMID 42480604); no objective "
                  "response in vivo at the persistence achieved (PMID 32002286).",
    "tandem CD19/CD20 CAR-T": "ASSUMED; in vitro only (PMID 42480604).",
}


def _potency_text(a: Agent) -> str:
    return _POTENCY_TEXT.get(a.name, a.potency_evidence)


def _ground(a: Agent, immunophenotype: str) -> Agent:
    """Apply the grounded corrections to one v1 agent."""
    kw = {"potency_evidence": _potency_text(a)}
    if a.name.startswith("venetoclax"):
        if immunophenotype == "T":
            kw["potency_evidence"] = ("PARTIAL: T-cell EC50 23 nM measured (24 h, PMID 36433867); canine "
                                      "exposure second-hand and free fraction unmeasured. Derived kill "
                                      f"{gi.venetoclax_T_kill(10, 0.001):.2f}-{gi.venetoclax_T_kill(10, 0.01):.2f} "
                                      "/day at 10 mg/kg; v1's 0.15 sits inside.")
        else:
            kw["potency_evidence"] = ("MEASURED-NEGATIVE: B-cell EC50 mean 288 uM (PMID 36433867); "
                                      "derived kill ~1e-4 /day at 20 mg/kg.")
    if a.name == "lomustine (CNS-penetrant nitrosourea)":
        kw["vulnerable_to"] = frozenset({"mgmt_repair"})
    if a.name.startswith("anti-PD-1"):
        kw["vulnerable_to"] = frozenset({"antigen_presentation"})
    if a.name.startswith("hydroxychloroquine"):
        h = gi.hcq_transfer()
        kw["potency"] = h.kill_per_day
        kw["efflux_substrate"] = True      # P-gp-overexpressing cells 5.2x more resistant (PMID 32992777)
        kw["potency_evidence"] = (f"TRANSFER: {h.kill_per_day:.2f}/day = human CLL IC50 ~95 uM (24 h, PMID "
                                  "11167827) against the MEASURED canine tumour concentration ~31 uM (100x "
                                  "plasma, PMID 24991836). Human ATLL IC50 13-26 uM would give more. A P-gp "
                                  "substrate (PMID 32992777), so it does not cover the pump clone.")
    if a.name.startswith("venetoclax"):
        kw["efflux_substrate"] = True      # sources conflict (PMID 29441961, 26927160 vs 34475043): conservative
    # CNS access replaced by non-canine MEASUREMENTS where they exist (each written as a transfer):
    if a.name.startswith("prednisolone") and a.access < 1.0:
        kw["access"] = 0.08
        kw["note"] = a.note + (" CNS access 0.08 = primate CSF:plasma of prednisolone (PMID 3806166); the "
                               "earlier 0.40 was assumed.")
    if a.name.startswith("venetoclax") and a.access < 1.0:
        kw["access"] = 0.0074
        kw["note"] = a.note + (" CNS access 0.0074 = human CSF/plasma 0.74% (PMID 39286959, adult leukemia); "
                               "the earlier 0.05 was assumed.")
    if a.name == REVERSER:
        kw["potency"] = 0.0     # acts by REVERSING efflux (see _kill_against), not as a free-standing kill
        kw["evidence"] = ("in vitro: PSC833 fully reversed dox/vincristine resistance (PMID 24975508); "
                          "TGF-beta inhibitor cut P-gp and restored doxorubicin in CLBL-1 8.0 (PMID "
                          "33961622). IN VIVO canine RCT, valspodar + doxorubicin, n=20: safe, NO "
                          "difference in event-free or overall survival (PMID 28357033).")
        kw["potency_evidence"] = "MECHANISM (reversal); no kill rate."
    if a.name == "anti-CD20 monoclonal antibody":
        kw["potency"] = gi.antibody_depletion_rates()["day_7_to_21"]
        kw["evidence"] = ("MEASURED in canine lymphoma with chemotherapy: CR 79% (33/42), 100% ORR, "
                          "PMID 38662527; 13 dogs, PFS 340 d, two remissions >4 years, PMID 41742528.")
        kw["note"] = ("Older catalogue text said no efficacious caninized anti-CD20 product is established; "
                      "two canine trials since show B-cell depletion and responses. The antibody's own "
                      "contribution is not isolated from the chemotherapy given with it.")
    return replace(a, **kw)


def _new_agents(compartment: str, immunophenotype: str) -> tuple:
    sm = SMALL_MOLECULE_ACCESS[compartment]
    steroid = GLUCOCORTICOID_ACCESS[compartment]
    rad = RADIATION_ACCESS[compartment]
    cell = CELL_ACCESS[compartment]
    verd = gi.verdinexor(immunophenotype)
    out = [
        Agent("verdinexor (XPO1 inhibitor)", Axis.APOPTOSIS, Layer.RECEPTOR, verd.kill_per_day, sm, 1.0,
              True, division_gated=True, efflux_substrate=False,
              evidence="MEASURED in canine lymphoma: Phase I/II, ORR 37% (T-cell 71%), median DOR 18 d, "
                       "TTP 29 d (PMID 30143046); licensed.",
              potency_evidence=("DERIVED: IC50 in canine lymphoma lines (PMID 40872651) x time-averaged "
                                "exposure in lymphoma dogs (PMID 30143046). Derived kill "
                                f"{verd.kill_per_day:.2f}/day exceeds the bar, yet the clinical duration is "
                                "18 d -- derived kill and clinical durability disagree."),
              note="Not a canine P-gp substrate (PMID 36924353). Modelled division-gated because "
                   "cycle-independence is not shown."),
        Agent("cyclophosphamide (metronomic)", Axis.CYTOTOXIC, Layer.RECEPTOR, 0.05, sm, 1.0, True,
              division_gated=True, efflux_substrate=False,
              evidence="MEASURED in dogs (continuous dosing, median 272 d, PMID 27901449).",
              potency_evidence="ASSUMED: dose-fraction of the pulse potency.",
              note="The HS dormancy lever: a division-gated agent that is PRESENT at every re-entry."),
        Agent("prednisolone (maintenance dose)", Axis.APOPTOSIS, Layer.RECEPTOR, 0.10 * 0.25 / 2.0, steroid,
              1.0, True, division_gated=False, efflux_substrate=False,
              evidence="ASSUMED from the full-dose agent.",
              potency_evidence="ASSUMED: dose-proportional (0.25 of 2 mg/kg); long-term canine tolerability "
                               "of this dose NOT FOUND."),
        Agent("half-body irradiation (low-dose-rate)", Axis.DELIVERY, Layer.RECEPTOR, 0.30, rad, 28 / 365,
              True, efflux_substrate=False,
              evidence="MEASURED in canine lymphoma: with L-CHOP, PFS 532 vs 296 d; first-remission rate "
                       "39% vs 8.7% at 2 y and 18% vs 4.4% at 5 y (n=75 vs 115, PMID 42525883); B-cell PFI "
                       "2127 d vs T-cell 292 d (PMID 40088118).",
              potency_evidence="OUTCOME: remission fractions measured; no kill rate.",
              note="A one-time consolidation with REAL multi-year remission data. See the model-conflict "
                   "note in docs/LYMPHOMA_STATUS.md."),
    ]
    # Cytarabine by CRI: kill computed per compartment from the MEASURED plasma or CSF steady state, so
    # access is 1.0 here (the CSF:plasma ratio 0.62 is inside the concentration, not a multiplier).
    ara = gi.cytarabine_cri(immunophenotype, "cns" if compartment == CNS else "systemic")
    for name, interval in (("cytarabine CRI (q14d)", 14.0), ("cytarabine CRI (q7d)", 7.0)):
        out.append(Agent(
            name, Axis.CYTOTOXIC, Layer.RECEPTOR, ara.kill_per_day, 1.0, (gi.ARAC_INFUSION_H / 24.0) / interval,
            True, division_gated=True, efflux_substrate=False,
            evidence="MEASURED in dogs: CSF:plasma 0.62 at a 12 h infusion, healthy dogs (PMID 1742843); "
                     "IC50 in canine lymphoma lines (PMID 25715778); used in canine CNS lymphoma (PMID 22210944, "
                     "37732143).",
            potency_evidence=(f"DERIVED: {ara.kill_per_day:.2f}/day during a 12 h infusion, from the measured "
                              f"{'CSF' if compartment == CNS else 'plasma'} steady state and the "
                              f"{'Ema' if immunophenotype == 'T' else 'CLBL-1'} IC50 (48 h); duty 12 h per "
                              f"{interval:.0f} d."),
            note="Division-gated (S-phase). P-gp substrate status in dogs NOT FOUND; human cytarabine is not "
                 "a classical P-gp substrate (transfer)."))
    if compartment == CNS:
        it = gi.continuous_it_cytarabine(immunophenotype)
        out.append(Agent(
            "continuous intrathecal cytarabine (pump) [buildable]", Axis.CYTOTOXIC, Layer.RECEPTOR,
            it["kill_per_day"], 1.0, 1.0, False, division_gated=True, efflux_substrate=False,
            evidence="DESIGN. Continuous intrathecal pump infusion is done in dogs for other drugs (PMID 8164885); "
                     "canine CSF cytarabine half-life measured (PMID 1742843); human sustained-release "
                     "intrathecal cytarabine holds cytotoxic CSF levels >= 14 d (PMID 10506606).",
            potency_evidence=(f"TRANSFER: {it['kill_per_day']:.2f}/day at a held CSF setpoint of "
                              f"{it['setpoint_nM']/1000:.0f} uM against the canine-lymphoma-line IC50 "
                              f"({it['ic50_nM']/1000:.2f} uM, 48 h, PMID 25715778). The setpoint is a design "
                              f"choice; holding it needs about {it['infusion_mg_per_day']:.2f} mg/day if canine CSF "
                              "volume is ~30 mL (assumed) and clearance follows the measured 113 min half-life."),
            note="Division-gated; chronic intrathecal exposure toxicity in dogs NOT FOUND."))
    if immunophenotype == "T":
        tl = ("TRANSFER-OUTCOME: human CD7 CAR-T gives MRD-negative remission in 19/20 (PMID 35500125) and "
              "94% (PMID 37740926); CD5 CAR-T avoids fratricide by CD5 down-modulation (PMID 38145560, "
              "38986621). Canine biology assumed to match; the kill rate itself is not measured.")
        out += [
            Agent("CD7-directed CAR-T (canine binder, fratricide-resistant) [buildable]", Axis.IMMUNE_EFFECTOR,
                  Layer.RECEPTOR, 0.12, cell, 1.0, False, division_gated=False, antigen_targets=("CD7",),
                  resists_axis_independence=True,
                  evidence="HUMAN clinical data only; no canine product. Relapse by CD7 loss in 4 of 6 "
                           "relapses (PMID 37020231).", potency_evidence=tl),
            Agent("CD5 + CD7 dual-target CAR-T (canine binder) [buildable]", Axis.IMMUNE_EFFECTOR,
                  Layer.RECEPTOR, 0.12, cell, 1.0, False, division_gated=False,
                  antigen_targets=("CD5", "CD7"), resists_axis_independence=True,
                  evidence="HUMAN clinical data only for each target; dual construct is a design that answers "
                           "CD7-loss relapse.", potency_evidence=tl),
        ]
    if immunophenotype == "B":
        out += [
            Agent("CD20 CAR-T with PD-1/CD28 switch receptor", Axis.IMMUNE_EFFECTOR, Layer.RECEPTOR, 0.12,
                  cell, 1.0, False, division_gated=False, antigen_targets=("CD20",),
                  resists_axis_independence=True,
                  evidence="PRECLINICAL: dog T cells in vitro only; restored cytotoxicity against PD-L1+ "
                           "targets (PMID 39314237).",
                  potency_evidence="ASSUMED.",
                  note="Armoured against exhaustion. Still carries a mouse-derived binder and the "
                       "persistence cap that goes with it."),
            Agent("persistence-engineered canine-binder CAR-T (specification)", Axis.IMMUNE_EFFECTOR,
                  Layer.RECEPTOR, 0.12, cell, 1.0, False, division_gated=False, antigen_targets=("CD20",),
                  resists_axis_independence=True,
                  evidence="NONE (does not exist). A specification: what the CAR-T would have to do.",
                  potency_evidence=("TRANSFER-OUTCOME: human CD19 CAR-T trafficks to the CNS and gives ORR 58-62% "
                                    "in CNS lymphoma (PMID 35167655, 36537908); detectable to 270 d with a "
                                    "human-compatible binder (PMID 35435984). Canine kill rate not measured.")),
        ]
    return tuple(out)


def _apply_rt(a: Agent) -> Agent:
    """Radiation potency from measured canine lymphoid-line survival (see lymphoma_grounded_inputs)."""
    if a.name not in gi.RT_COURSES:
        return a
    lo, mid, hi = (gi.rt_kill_per_day(a.name, ln) for ln in ("CLL1390", "1771", "CLBL1"))
    d, n, days = gi.RT_COURSES[a.name]
    return replace(
        a, potency=lo, duty=days / 365.0,
        potency_evidence=(f"PARTIAL: derived from measured clonogenic survival of canine lymphoid lines (PMID "
                          f"27257868): {lo:.3f}/day for the most resistant line (used), {mid:.3f} for the median "
                          f"line, {hi:.3f} for the most sensitive, over a {days:.0f}-day course of {n} x {d} Gy. "
                          "Assumes the prescribed dose reaches the tumour cell."))


def grounded_agents(compartment: str, immunophenotype: str = "B") -> tuple:
    base = [_ground(a, immunophenotype) for a in agents_for(compartment, immunophenotype)]
    return tuple(_apply_rt(a) for a in tuple(base) + _new_agents(compartment, immunophenotype))


def available(agents, tier: str) -> tuple:
    allowed = TIER_ALLOWS[tier]
    return tuple(a for a in agents if AVAILABILITY.get(a.name, NONE) in allowed)


#: Evidence tiers for a potency, strictest first. The user's bar is 'real data or a rigorous model':
#: STRICT = a kill rate derived from a measured potency and a measured exposure, or measured in vivo.
#: OUTCOME adds agents whose benefit is a measured clinical outcome but whose kill rate is not measured.
STRICT_GRADES = frozenset({"DERIVED", "PARTIAL", "MEASURED"})
OUTCOME_GRADES = STRICT_GRADES | {"OUTCOME", "REGIMEN-CALIBRATED", "MECHANISM"}
#: 'Scientifically sound' (the user's standard, 2026-09-30): adds potency, exposure or access figures
#: TRANSFERRED from another species or disease with a written justification. A number with no basis
#: stays ASSUMED and is not in this set.
SOUND_GRADES = OUTCOME_GRADES | {"TRANSFER", "TRANSFER-OUTCOME", "BRACKET"}
#: A BRACKET agent is admitted at the LOW end of its measured bracket; a HINGE agent (no potency at all)
#: is not admitted until an IC50 is transferred for it.
BRACKET_LOW = {"prednisolone (glucocorticoid)": 0.0098}


def sound_pool(agents) -> list:
    out = []
    for a in agents:
        g = potency_grade(a)
        if g not in SOUND_GRADES:
            continue
        if g == "BRACKET":
            a = replace(a, potency=BRACKET_LOW.get(a.name, a.potency))
        out.append(a)
    return out

#: Fraction of the pre-treatment burden that seeds the CNS (lymphoma_scenarios.LYMPHOMA_CNS_SEED_FRACTION).
CNS_SEED_FRACTION = 0.05


def potency_grade(a: Agent) -> str:
    """The leading keyword of the potency evidence: DERIVED/PARTIAL/HINGE/BRACKET/OUTCOME*/MEASURED*/
    MECHANISM/ASSUMED."""
    return a.potency_evidence.split(":")[0].split(" ")[0].strip(",.;").upper()


#: One-time courses: `duty` in the catalogue is the course averaged over a year (course days / 365).
#: The time-resolved clock uses full in-course strength and lets the course END, which is how a
#: consolidation can leave a lineage extinct even though its annual average looks small.
COURSE_AGENTS = frozenset({"craniospinal radiotherapy", "total body irradiation + transplant",
                           "half-body irradiation (low-dose-rate)"})


def in_window(a: Agent) -> Agent:
    return replace(a, duty=1.0) if a.name in COURSE_AGENTS else a


# --- coverage with P-gp reversal -------------------------------------------------------------------

def _has_reverser(agents) -> bool:
    return any(a.name == REVERSER for a in agents)


def _effective_agents_for(agents, escape):
    """Against the P-gp clone, a reverser turns the pump's substrates back into ordinary agents."""
    if escape is PGP and _has_reverser(agents):
        return [replace(a, efflux_substrate=False) if a.efflux_substrate else a for a in agents]
    return list(agents)


def kill_against(agents, escape) -> float:
    return sum(a.effective_kill for a in _effective_agents_for(agents, escape) if a.reaches(escape))


def covered(agents, escape) -> bool:
    if not escape.requires_division:
        return any(a.effective_kill > 0.0 and a.covers(escape) for a in agents)
    return any(a.reaches(escape) for a in _effective_agents_for(agents, escape))


def margin_for(agents, escape, growth=GROWTH_PER_DAY, f=CYCLING_FRACTION_DEFAULT,
               r=RETAINED_TOLERANCE_DEFAULT) -> float:
    if not escape.requires_division:
        return persister_margin(_effective_agents_for(agents, escape), escape, growth, f, r)
    return kill_against(agents, escape) - growth


# --- toxicity --------------------------------------------------------------------------------------

def regimen_profiles(agents, efflux_multiplier: float):
    """One profile per agent; a reverser charges every P-gp substrate's load."""
    reverse = _has_reverser(agents)
    out = []
    for a in agents:
        p = profile_for(a.name)
        if reverse and a.efflux_substrate:
            p = with_efflux_co_dose(p, efflux_multiplier)
        out.append(p)
    return out


def derate(agents, efflux_multiplier: float):
    """(derated agents, per-agent factors, profiles). De-rating is not free."""
    profs = regimen_profiles(agents, efflux_multiplier)
    factors = [derating_for(p, profs) for p in profs]
    return [replace(a, potency=a.potency * f) for a, f in zip(agents, factors)], factors, profs


# --- evaluation ------------------------------------------------------------------------------------

@dataclass
class Evaluation:
    agents: tuple
    escapes: tuple
    factors: dict
    loads: dict
    over: dict
    headroom: float
    margins_full: dict
    margins_derated: dict
    worst_full: float
    worst_derated: float
    weakest: str
    assumed: int
    horizon_strict: HorizonResult | None = None
    horizon_extended: HorizonResult | None = None
    availability: tuple = ()
    schedule: str = "all agents from day 0"

    @property
    def names(self) -> tuple:
        return tuple(a.name for a in self.agents)

    @property
    def closes(self) -> bool:
        return self.worst_derated > 0.0

    @property
    def derated(self) -> bool:
        return any(f < 0.999 for f in self.factors.values())


def escapes_to_close(burden: float, escapes=GROUNDED_ESCAPES, threshold: float = 0.5):
    return tuple(e for e in escapes
                 if e.name in FOUNDER_ESCAPES or escape_presence_probability(e, burden) >= threshold)


def evaluate(agents, escapes, *, growth=GROWTH_PER_DAY, f=CYCLING_FRACTION_DEFAULT,
             r=RETAINED_TOLERANCE_DEFAULT, efflux_multiplier=gi.EFFLUX_CO_DOSE_MULTIPLIER_CANINE_PROXY,
             burden=BURDEN_EARLY_DETECTED, clock=False, compartment=SYSTEMIC, starts=None,
             schedule="all agents from day 0", cns_fraction=None) -> Evaluation:
    agents = tuple(agents)
    d_agents, factors, profs = derate(agents, efflux_multiplier)
    mf = {e.name: margin_for(agents, e, growth, f, r) for e in escapes}
    md = {e.name: margin_for(d_agents, e, growth, f, r) for e in escapes}
    weakest = min(md, key=md.get)
    ev = Evaluation(
        agents=agents, escapes=tuple(escapes), factors={a.name: fc for a, fc in zip(agents, factors)},
        loads={o.value: round(v, 3) for o, v in axis_loads(profs).items()},
        over={o.value: round(v, 3) for o, v in oversubscribed(profs).items()},
        headroom=headroom(profs), margins_full=mf, margins_derated=md,
        worst_full=min(mf.values()), worst_derated=md[weakest], weakest=weakest,
        assumed=sum(1 for a in agents if potency_grade(a) in ("ASSUMED", "BRACKET", "HINGE")),
        availability=tuple(AVAILABILITY.get(a.name, NONE) for a in agents))
    ev.schedule = schedule
    if clock:
        h_fraction = (CNS_SEED_FRACTION if cns_fraction is None else cns_fraction) if compartment == CNS else 1.0
        for label, key in (("horizon_strict", "sustainable_days"), ("horizon_extended", "hard_cap_days")):
            sustain = {a.name: getattr(profile_for(a.name), key) for a in agents}
            # De-rating is decided per PHASE: only the agents given together share organ budgets.
            transform = lambda act: [in_window(a) for a in derate(act, efflux_multiplier)[0]]
            hz = horizon(agents, escapes, sustain, burden, growth, f=f, r=r, fraction=h_fraction,
                         margin_fn=lambda act, esc: margin_for(act, esc, growth, f, r),
                         always_present=FOUNDER_ESCAPES, kill_of=lambda a: a.effective_kill,
                         starts=starts, transform=transform)
            setattr(ev, label, hz)
    return ev


#: Agents that are delivered as a discrete course or a cell product, and so are naturally given AFTER
#: cytoreduction rather than stacked on it.
STAGEABLE = COURSE_AGENTS | {"CD20 CAR-T", "tandem CD19/CD20 CAR-T",
                             "CD20 CAR-T with PD-1/CD28 switch receptor",
                             "persistence-engineered canine-binder CAR-T (specification)",
                             "CD5/CD52-directed cellular effector (T-lineage)"}
STAGE_DAYS = (28, 56, 84)


def schedule_options(names) -> list:
    """(label, starts) options: everything from day 0, or the stageable agents started later."""
    opts = [("all agents from day 0", None)]
    stage = [n for n in names if n in STAGEABLE]
    if stage and len(stage) < len(names):
        for d in STAGE_DAYS:
            opts.append((f"course/cell agents start day {d}", {n: float(d) for n in stage}))
    return opts


def evaluate_best_schedule(agents, escapes, **kw) -> Evaluation:
    """Run the clock under each schedule option and keep the one that clears everything earliest
    (or, failing that, the first)."""
    best = None
    for label, starts in schedule_options([a.name for a in agents]):
        ev = evaluate(agents, escapes, clock=True, starts=starts, schedule=label, **kw)
        ok = ev.horizon_strict.cure_inside_window
        key = (not ok, ev.horizon_strict.clear_day if ok else 0.0)
        if best is None or key < best[0]:
            best = (key, ev)
    return best[1]


#: Versions of one drug or one construct exclude each other: a regimen cannot contain two schedules of
#: cytarabine, both cyclophosphamide regimens, two prednisolone doses, two CD20 CARs, or whole-body plus
#: half-body irradiation (the first contains the second). Without this the search double-counted a drug.
FAMILY = {
    "cytarabine CRI (q14d)": "cytarabine CRI", "cytarabine CRI (q7d)": "cytarabine CRI",
    "cyclophosphamide": "cyclophosphamide", "cyclophosphamide (metronomic)": "cyclophosphamide",
    "prednisolone (glucocorticoid)": "prednisolone", "prednisolone (maintenance dose)": "prednisolone",
    "CD20 CAR-T": "CD20 CAR", "tandem CD19/CD20 CAR-T": "CD20 CAR",
    "CD20 CAR-T with PD-1/CD28 switch receptor": "CD20 CAR",
    "persistence-engineered canine-binder CAR-T (specification)": "CD20 CAR",
    "intrathecal cytarabine": "IT cytarabine", "continuous intrathecal cytarabine (pump) [buildable]": "IT cytarabine",
    "CD7-directed CAR-T (canine binder, fratricide-resistant) [buildable]": "T CAR",
    "CD5 + CD7 dual-target CAR-T (canine binder) [buildable]": "T CAR",
    "CD5/CD52-directed cellular effector (T-lineage)": "T CAR",
    "total body irradiation + transplant": "whole/half-body RT",
    "half-body irradiation (low-dose-rate)": "whole/half-body RT",
}


def one_per_family(combo) -> bool:
    fams = [FAMILY.get(a.name, a.name) for a in combo]
    return len(set(fams)) == len(fams)


MAX_COMBO = 5
EVALUATE_ALL_UP_TO = 6000
SMALL_N = 3     # every closing regimen up to this size gets the clock, whatever its margin


def search(compartment: str, immunophenotype: str = "B", tier: str = "off-label", *,
           burden: float = BURDEN_EARLY_DETECTED, max_n: int = MAX_COMBO,
           f=CYCLING_FRACTION_DEFAULT, r=RETAINED_TOLERANCE_DEFAULT,
           efflux_multiplier=gi.EFFLUX_CO_DOSE_MULTIPLIER_CANINE_PROXY, top: int = 8,
           extra_agents=(), pool=None) -> dict:
    """Every combination of up to `max_n` agents that COVERS every escape, evaluated with toxicity
    de-rating; the best by worst de-rated margin get the clock run on them."""
    escapes = escapes_to_close(burden)
    if immunophenotype == "T":
        escapes = tuple(e for e in escapes if e.removes_antigen not in B_LINEAGE_ANTIGENS)
    pool = list(pool) if pool is not None else list(available(grounded_agents(compartment, immunophenotype), tier))
    pool += list(extra_agents)
    n_pool = len(pool)
    rows = []
    n_cov = 0
    for n in range(1, min(n_pool, max_n) + 1):
        for combo in combinations(pool, n):
            if not one_per_family(combo):
                continue
            if not all(covered(combo, e) for e in escapes):
                continue
            n_cov += 1
            raw = min(margin_for(combo, e, GROWTH_PER_DAY, f, r) for e in escapes)
            if raw <= 0.0:
                continue
            d_agents, factors, _ = derate(combo, efflux_multiplier)
            worst = min(margin_for(d_agents, e, GROWTH_PER_DAY, f, r) for e in escapes)
            rows.append((worst, n, combo, raw))
    rows.sort(key=lambda t: (-t[0], t[1]))
    closing = [t for t in rows if t[0] > 0.0]
    # The clock runs on (a) the best-margin regimens, (b) every closing regimen of <= SMALL_N agents,
    # and (c) regimens that close only WITHOUT de-rating (they may be tolerable if staged).
    picked, seen = [], set()
    by_raw = sorted(rows, key=lambda t: (-t[3], t[1]))
    if len(rows) <= EVALUATE_ALL_UP_TO:
        picked = [c for _, _, c, _ in rows]          # small enough: run the clock on every closing regimen
    else:
        for source in (rows, by_raw):
            count = 0
            for worst, n, c, raw in source:
                if id(c) in seen:
                    continue
                if n <= SMALL_N or count < max(top * 6, 40):
                    seen.add(id(c)); picked.append(c); count += 1
    evaluated = [evaluate_best_schedule(c, escapes, f=f, r=r, efflux_multiplier=efflux_multiplier,
                                        burden=burden, compartment=compartment) for c in picked]
    evaluated.sort(key=lambda ev: -ev.worst_derated)
    return {"compartment": compartment, "immunophenotype": immunophenotype, "tier": tier,
            "burden": burden, "escapes": tuple(e.name for e in escapes), "pool": tuple(a.name for a in pool),
            "coverage_complete": n_cov, "closing_without_derating": len(rows),
            "closing_after_derating": len(closing),
            "best_uncleared_margin": rows[0][0] if rows else None,
            "top_by_margin": evaluated[:top],
            "cured_inside_window": [e for e in evaluated if e.horizon_strict.cure_inside_window],
            "all_rows": rows}


# --- fault tolerance --------------------------------------------------------------------------------

def discounted(agents, delta: float):
    """Every potency multiplied by `delta` (a global 'the real world is weaker than the derivation')."""
    return [replace(a, potency=a.potency * delta) for a in agents]


def clears(agents, escapes, **kw) -> bool:
    ev = evaluate_best_schedule(agents, escapes, **kw)
    return ev.closes and ev.horizon_strict.cure_inside_window


def fault_tolerant(agents, escapes, delta: float = 0.5, **kw) -> bool:
    """True if the regimen still clears every lineage inside the documented windows (a) with all potencies
    multiplied by `delta` and (b) after removing ANY ONE agent (also at `delta`). This is the test that a
    'closing' combination does not hang on a single agent or a single potency."""
    agents = list(agents)
    if not clears(discounted(agents, delta), escapes, **kw):
        return False
    for i in range(len(agents)):
        rest = agents[:i] + agents[i + 1:]
        if not rest or not clears(discounted(rest, delta), escapes, **kw):
            return False
    return True


def cns_capacity(agents, escapes, burden: float = BURDEN_EARLY_DETECTED, **kw) -> float:
    """The largest number of CNS tumour cells this regimen clears inside its documented windows (every
    present lineage keeps at least one cell). The sanctuary's real size at early detection is unmeasured,
    so this is reported as a capacity rather than a yes/no. Returns 0 if it clears even one cell only
    with a negative margin, i.e. cannot clear at all."""
    def ok(frac):
        ev = evaluate_best_schedule(list(agents), escapes, burden=burden, compartment=CNS,
                                    cns_fraction=frac, **kw)
        return ev.closes and ev.horizon_strict.cure_inside_window
    lo_exp, hi_exp = -8.0, 0.0                      # fraction of the whole-tumour burden, log10
    if not ok(10 ** lo_exp):
        return 0.0
    if ok(10 ** hi_exp):
        return burden * 1.0
    for _ in range(14):
        mid = (lo_exp + hi_exp) / 2
        if ok(10 ** mid):
            lo_exp = mid
        else:
            hi_exp = mid
    return burden * 10 ** lo_exp
