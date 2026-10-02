"""The toxicity profiles the lymphoma search actually uses, each with its canine source.

HOW TO READ A BUDGET. `budget_fraction` is the share of an organ axis's tolerable burden consumed at the
standard dose (1.0 = the standard dose already reaches the dose-limiting point in a typical dog).
Where a canine incidence exists it anchors the figure (a grade >= 3 or dose-modifying event rate of
~50% is ~0.5); the mapping is an ORDINAL JUDGEMENT, exactly as the HS branch's budgets are, and is
labelled `measured_in_dogs` only when the underlying event rate is a canine measurement. It gives
headroom, not a prediction.

TWO WINDOWS PER AGENT. `sustainable_days` is EVIDENCE-LIMITED: the longest continuous canine dosing or
practice cap actually documented. `hard_cap_days` is a toxicity cap where one is identified; None means
none identified, which is a statement about the evidence and NOT a safety claim. The horizon check
(core/lymphoma_horizon.py) runs strictly on the first and reports separately what needs the second.

Every citation below was opened by a literature agent this session and the sentence quoted; the
PMIDs are the same ones listed in docs/LYMPHOMA_STATUS.md. Items a search could not find are NOT
filled in from memory -- they are left `measured_in_dogs=False` and the note says NOT FOUND.
"""

from __future__ import annotations

from .lymphoma_toxicity import PROFILES, Organ as O, ToxicityProfile as P

# ---- CHOP backbone --------------------------------------------------------------------------------
# 15-week CHOP (PMID 26279153) is 105 days: the practice window for the pulsed cytotoxics.
_CHOP_DAYS = 105.0

PROFILES["doxorubicin"] = P(
    O.MARROW, 0.45, True,
    "myelosuppression and GI signs acutely (GI adverse events 56% on doxorubicin, PMID 40320245; "
    "dose reductions needed in 54% on dose-intensified CHOP, PMID 20691027); cumulative cardiotoxicity "
    "is the cap",
    source="Cardiotoxicity 20/494 (4.0%), higher cumulative dose associated, intended cap 180 mg/m2 "
           "(= 6 doses at 30 mg/m2), 'uncommon at <240 mg/m2, most institutions rarely exceed 180', "
           "PMID 30697816 (dog).",
    secondary_axis=O.CARDIAC, secondary_fraction=0.40, extra_loads=((O.GI, 0.30),),
    cumulative=True, sustainable_days=126.0, hard_cap_days=126.0, reversible=False)

PROFILES["vincristine"] = P(
    O.GI, 0.25, True,
    "GI signs and neutropenia; peripheral neuropathy incidence NOT FOUND in the canine abstracts read",
    source="Vomiting/diarrhoea/anorexia and day-7 neutropenia after vincristine in 335 doses, "
           "PMID 39305174 (dog).",
    secondary_axis=O.MARROW, secondary_fraction=0.15,
    sustainable_days=_CHOP_DAYS, hard_cap_days=None)

PROFILES["cyclophosphamide"] = P(
    O.MARROW, 0.30, True,
    "myelosuppression; sterile haemorrhagic cystitis (PULSE dosing inside CHOP)",
    source="SHC 12/133 (9%) without and 1/83 (1.2%) with furosemide, PMID 12762384; 4.6% overall "
           "PMID 24463993 (dog). Marrow axis shared with CHOP (PMID 26279153).",
    secondary_axis=O.BLADDER, secondary_fraction=0.15,
    sustainable_days=_CHOP_DAYS, hard_cap_days=None)

PROFILES["cyclophosphamide (metronomic)"] = P(
    O.BLADDER, 0.30, True,
    "sterile haemorrhagic cystitis on continuous dosing: 25/115 (21.7%; 30.3% without furosemide, "
    "10.2% with; PMID 28194917); 16/65 with median onset 110 days (PMID 28133740); 2/55 (3.6%) with "
    "furosemide (PMID 27901449). Longest continuous dosing: median 272 days, range 28-1393 "
    "(PMID 27901449).",
    source="Dog. Cumulative in time (median onset 110 d) though not associated with treatment count "
           "in one series (PMID 28194917).",
    secondary_axis=O.MARROW, secondary_fraction=0.10, cumulative=True,
    sustainable_days=272.0, hard_cap_days=1393.0, reversible=True)

PROFILES["prednisolone (glucocorticoid)"] = P(
    O.STEROID_CLASS, 0.55, True,
    "iatrogenic hypercortisolism at 2 mg/kg/day: 4/4 healthy Beagles by day 150, adrenal shrinkage "
    "partly reversed by day 211 (PMID 40696374); GI ulceration risk with steroid/NSAID (PMID 39426398)",
    source="Dog (healthy Beagles, n=4). Infection incidence attributable to prednisolone in lymphoma "
           "dogs: NOT FOUND.",
    secondary_axis=O.GI, secondary_fraction=0.10, cumulative=True,
    sustainable_days=150.0, hard_cap_days=150.0, reversible=True)

# A maintenance-dose prednisolone variant: the standard practice for a chronic steroid, and the
# honest way to ask whether the efflux-independent, non-division-gated carrier can be held for years.
# BOTH the potency (dose-proportional) and the long-term tolerability are ASSUMED, not measured.
PROFILES["prednisolone (maintenance dose)"] = P(
    O.STEROID_CLASS, 0.15, False,
    "long-term low-dose steroid: canine long-term tolerability NOT FOUND",
    source="ASSUMED: taper to 0.25 mg/kg (the taper used in PMID 40696374) with load scaled by dose "
           "ratio. Nothing here is a canine long-term measurement.",
    sustainable_days=150.0, hard_cap_days=None, reversible=True)

# ---- other cytotoxics ----------------------------------------------------------------------------
PROFILES["rabacfosadine"] = P(
    O.PULMONARY, 0.30, True,
    "delayed fatal pulmonary fibrosis: grade 5 in 3/63 (4.8%) at 119/133/144 days (PMID 32346934) and "
    "2/51 at 130/142 days (PMID 28370378); irreversible",
    source="Dog. 'Idiosyncratic', mechanism not understood. Cumulative-dose threshold NOT FOUND. "
           "Dermatopathy ~25% (mostly grade 1-2), grade 3 GI and grade 4 neutropenia also reported.",
    secondary_axis=O.SKIN, secondary_fraction=0.30,
    extra_loads=((O.GI, 0.30), (O.MARROW, 0.25)),
    cumulative=False, sustainable_days=105.0, hard_cap_days=105.0, reversible=False)

PROFILES["lomustine"] = P(
    O.MARROW, 0.60, True,
    "neutropenia in 65% (grade 3 29%, grade 4 27%; dose >70 mg/m2 and histiocytic sarcoma were risk "
    "factors, PMID 35249267); CUMULATIVE irreversible hepatotoxicity in 6.1%, seven of 11 died of "
    "liver failure, median 350 mg/m2 and 4 doses (PMID 14765735)",
    source="Dog.",
    secondary_axis=O.HEPATIC, secondary_fraction=0.50, cumulative=True,
    sustainable_days=84.0, hard_cap_days=84.0, reversible=False)

PROFILES["high-dose methotrexate"] = P(
    O.RENAL, 0.50, False,
    "renal and GI/mucosal toxicity needing leucovorin rescue; systemic high-dose methotrexate in "
    "dogs: NOT FOUND",
    source="TRANSFER from human CNS-lymphoma practice; budget is an assumption.",
    secondary_axis=O.GI, secondary_fraction=0.30, extra_loads=((O.MARROW, 0.30),),
    sustainable_days=84.0, hard_cap_days=None, reversible=True)

PROFILES["continuous intrathecal cytarabine (pump) [buildable]"] = P(
    O.CNS_LOCAL, 0.60, False,
    "chronic intrathecal exposure: chemical arachnoiditis / neurotoxicity; bolus IT cytarabine + methotrexate "
    "gave 1 seizure in 112 dogs and 8 cats (PMID 25041580); dog catheter-tip masses with continuous morphine "
    "(PMID 31124198)",
    source="ASSUMED budget; canine chronic intrathecal cytarabine toxicity NOT FOUND. Pump patency: 67% of "
           "catheters patent >30 d in dogs (PMID 24694254).",
    sustainable_days=84.0, hard_cap_days=None, reversible=True)

PROFILES["cytarabine CRI (q14d)"] = P(
    O.GI, 0.55, True,
    "GI toxicity in 17/26 (65.3%; grade III-IV in 19.2%), neutropenia in 9/26 (34.6%) after a single "
    "cytarabine CRI added to CEOP",
    source="Dog, PMID 31769013 (26 dogs). Healthy dogs: no clinically significant toxicity in 21 days "
           "after 600 mg/m2 over 12 h (PMID 1742843, n=10). A 14-day repeat interval is an ASSUMED schedule.",
    secondary_axis=O.MARROW, secondary_fraction=0.35,
    sustainable_days=84.0, hard_cap_days=None, reversible=True)

PROFILES["cytarabine CRI (q7d)"] = P(
    O.GI, 0.90, False,
    "as the q14d schedule, doubled for weekly repetition: NOT measured, weekly CRI tolerability not found",
    source="ASSUMED doubling of the single-dose incidence in PMID 31769013.",
    secondary_axis=O.MARROW, secondary_fraction=0.60,
    sustainable_days=84.0, hard_cap_days=None, reversible=True)

PROFILES["intrathecal cytarabine"] = P(
    O.CNS_LOCAL, 0.25, False,
    "chemical arachnoiditis / neurotoxicity; one canine case gave only a 3-week CNS remission "
    "(PMID 37732143) and reported no toxicity",
    source="Canine toxicity data essentially absent; budget assumed.",
    sustainable_days=84.0, hard_cap_days=None, reversible=True)

PROFILES["craniospinal radiotherapy"] = P(
    O.CNS_LOCAL, 0.60, False,
    "normal-tissue tolerance of brain and cord; marrow in the spinal field",
    source="Radiobiology transfer; no canine lymphoma craniospinal series found.",
    secondary_axis=O.MARROW, secondary_fraction=0.20,
    sustainable_days=21.0, hard_cap_days=21.0, reversible=False)

# ---- immune arms ---------------------------------------------------------------------------------
PROFILES["anti-CD20 monoclonal antibody"] = P(
    O.IMMUNE_MEDIATED, 0.30, True,
    "on-target B-cell aplasia (65% still depleted >4 months after the last infusion); one suspected "
    "type-I hypersensitivity in 160 doses; grade 1-2 azotemia in 5/42",
    source="1E4-cIgGB + doxorubicin, 42 dogs, PMID 38662527; 4E1-7-B_f + CHOP, 13 dogs, no anti-drug "
           "antibodies in 12 tested, PMID 41742528. Follow-up with data reaches ~300 days (6 dogs in "
           "CR at day 300, 4 with B-cell recovery). Consequences of years of B-cell aplasia: NOT FOUND.",
    cumulative=False, sustainable_days=300.0, hard_cap_days=None, reversible=True)

PROFILES["CD20 CAR-T"] = P(
    O.IMMUNE_MEDIATED, 0.35, True,
    "grade 2 cytokine release at ~5e6 CAR-T/kg (PMID 35898541); otherwise well tolerated at lower "
    "doses (PMID 27401141, 32002286); the limiting fact is not toxicity but PERSISTENCE",
    source="Dog, 5-6 dogs total. CAR-T detectable to ~day 28 in blood, lymph-node peak day 50, "
           "undetectable by day 14 in the CRS case; canine anti-mouse antibodies (CAMA) rose and were "
           "'associated with CAR T cell loss' (PMID 32002286, 35898541, 38573683).",
    cumulative=False, sustainable_days=50.0, hard_cap_days=50.0, reversible=True)

PROFILES["tandem CD19/CD20 CAR-T"] = P(
    O.IMMUNE_MEDIATED, 0.35, False,
    "in vitro only (PMID 42480604); toxicity and persistence in vivo NOT FOUND",
    source="Assumed to share the single-antigen CAR's class profile INCLUDING the mouse-binder "
           "persistence cap; nothing here is measured for the tandem construct.",
    cumulative=False, sustainable_days=50.0, hard_cap_days=50.0, reversible=True)

PROFILES["CD20 CAR-T with PD-1/CD28 switch receptor"] = P(
    O.IMMUNE_MEDIATED, 0.35, False,
    "in vitro dog T cells only (PMID 39314237)",
    source="Preclinical; class profile assumed; same mouse-binder persistence cap assumed.",
    cumulative=False, sustainable_days=50.0, hard_cap_days=50.0, reversible=True)

PROFILES["persistence-engineered canine-binder CAR-T (specification)"] = P(
    O.IMMUNE_MEDIATED, 0.40, False,
    "DOES NOT EXIST in dogs. Human CD19 CAR-T in CNS lymphoma: ICANS 44% (grade >=3 35%), severe CRS 7% "
    "(PMID 36537908)",
    source="TRANSFER from human. Persistence window 270 d is the longest detectable persistence in the human "
           "CD7 series (PMID 35435984); a canine-derived binder is assumed to remove the anti-mouse loss.",
    cumulative=False, sustainable_days=270.0, hard_cap_days=None, reversible=True)

PROFILES["CD7-directed CAR-T (canine binder, fratricide-resistant) [buildable]"] = P(
    O.IMMUNE_MEDIATED, 0.50, False,
    "HUMAN: CRS in 87-92% (grade 3/4 about 11%), neurotoxicity ~5%, grade 3-4 cytopenias 96-100%, severe "
    "infection late because non-CAR T and NK cells become CD7-negative (PMID 37020231, 37740926, 40712157)",
    source="TRANSFER from human T-ALL/T-LBL. Persistence to 270 d (PMID 35435984).",
    secondary_axis=O.MARROW, secondary_fraction=0.40,
    cumulative=False, sustainable_days=270.0, hard_cap_days=None, reversible=False)
PROFILES["CD5 + CD7 dual-target CAR-T (canine binder) [buildable]"] = P(
    O.IMMUNE_MEDIATED, 0.55, False,
    "as the CD7 CAR-T plus loss of CD5+ normal T cells (human CD5 CAR-T: no grade >=3 CRS or neurotoxicity "
    "in 9 treated, PMID 38145560)",
    source="TRANSFER from human; the dual construct itself has no clinical data.",
    secondary_axis=O.MARROW, secondary_fraction=0.40,
    cumulative=False, sustainable_days=270.0, hard_cap_days=None, reversible=False)

PROFILES["CD5/CD52-directed cellular effector"] = P(
    O.IMMUNE_MEDIATED, 0.50, False,
    "DOES NOT EXIST; a CD5-directed T-cell product attacks T cells including itself (fratricide) and "
    "causes profound T-cell aplasia",
    source="Specification only. No canine data.",
    cumulative=False, sustainable_days=None, hard_cap_days=None, reversible=False)

PROFILES["anti-PD-1"] = P(
    O.IMMUNE_MEDIATED, 0.20, False,
    "immune-mediated adverse events",
    source="Transfer (canine melanoma / HS-branch profile); no canine lymphoma safety series found.",
    sustainable_days=None, hard_cap_days=None)

# ---- position-independent, non-division-gated agents --------------------------------------------
PROFILES["hydroxychloroquine"] = P(
    O.MARROW, 0.20, True,
    "in combination with doxorubicin two treatment-related deaths (severe neutropenia, GI, sepsis) "
    "forced doxorubicin down from 30 to 25 mg/m2; HCQ alone gave only mild lethargy and GI signs",
    source="Dog Phase I, n=30, MTD 12.5 mg/kg/day PO, PMID 24991836. LONG-TERM: human retinopathy is "
           "cumulative and irreversible (<1% at 5 y, <2% at 10 y, ~20% at 20 y at <=5 mg/kg/day, "
           "PMID 26992838, HUMAN) and the canine dose is 2.5x the human ceiling; canine ocular data "
           "and longest canine duration NOT FOUND.",
    secondary_axis=O.GI, secondary_fraction=0.25, extra_loads=((O.OCULAR, 0.30),),
    cumulative=True, sustainable_days=150.0, hard_cap_days=None, reversible=False)

PROFILES["venetoclax"] = P(
    O.MARROW, 0.30, False,
    "neutropenia (human, 63-64% grade 3/4 in CLL); tumour lysis at initiation (human); in DOGS: "
    "testicular germ-cell loss at 0.5x human AUC, single-cell necrosis in gallbladder/pancreas/stomach "
    "(partly reversible), progressive hair depigmentation after ~3 months",
    source="Dog: FDA Venclexta label 13.1/13.2 preclinical statements. Beagles given 2-20 mg/kg for "
           "up to 9 months developed an average 81% lymphocyte reduction with no clinical signs "
           "(quoted second-hand in PMID 36433867). In-vivo canine lymphoma safety NOT FOUND.",
    secondary_axis=O.GI, secondary_fraction=0.10,
    cumulative=True, sustainable_days=270.0, hard_cap_days=None, reversible=False)

PROFILES["acalabrutinib"] = P(
    O.GI, 0.20, True,
    "grade 1-2 anorexia, weight loss, vomiting, diarrhoea, lethargy; two severe events (sepsis, "
    "prostatitis/cystitis) in 20 dogs; MTD not reached, up to 15 mg/kg BID tolerated",
    source="Dog trial, n=20, PMID 27434128. Bleeding / atrial fibrillation in dogs and longest "
           "continuous duration: NOT FOUND (partial responders ran 56 days).",
    sustainable_days=56.0, hard_cap_days=None)

PROFILES["verdinexor"] = P(
    O.GI, 0.45, True,
    "anorexia 45%, weight loss 31%, vomiting 26% (mostly grade 1-2); grade 3 ALT/AST/ALP rise and DLT "
    "in all 3 dogs at 2 mg/kg twice weekly; field study serious adverse events 22% (28/127) vs 15.2% "
    "control",
    source="Dog: PMID 24503695 (MTD 1.75 mg/kg twice weekly), PMID 30143046 (Phase II, 58 dogs), "
           "Laverdia label. 13-week beagle study: testicular degeneration, thymic lymphoid depletion. "
           "Longest continuous dosing: 17 months in a single dog (PMID 39235783); ~40% of Phase II "
           "dogs stayed on study >= 8 weeks.",
    secondary_axis=O.HEPATIC, secondary_fraction=0.20,
    sustainable_days=56.0, hard_cap_days=None, reversible=True)

# ---- efflux reversal -----------------------------------------------------------------------------
PROFILES["P-gp / TGF-beta-inhibitor chemosensitiser"] = P(
    O.MARROW, 0.20, True,
    "raises exposure of every co-administered P-gp substrate; the canine trial cut the first "
    "doxorubicin dose by 30% (30 to 21 mg/m2) to compensate",
    source="Valspodar 7.5 mg/kg PO q12h x5 days with doxorubicin, 20 dogs, no grade 4/5, one grade 2 "
           "marrow event, PMID 28357033 (dog). The inhibitor itself has little toxicity; its cost is "
           "the multiplier it puts on the PARTNER, charged by `with_efflux_co_dose`.",
    sustainable_days=126.0, hard_cap_days=126.0)

# ---- consolidation -------------------------------------------------------------------------------
PROFILES["total body irradiation + transplant"] = P(
    O.PROCEDURAL, 0.85, True,
    "treatment-related mortality 7/94 (7%) before discharge (PMID 38695516); 2/24 in-hospital deaths "
    "(PMID 22882500); 2/15 (PMID 24467413); grade 4 cytopenias in every dog; presumed TBI pulmonary "
    "fibrosis ~8 months",
    source="Dog.",
    secondary_axis=O.MARROW, secondary_fraction=0.60,
    sustainable_days=14.0, hard_cap_days=14.0, reversible=False)

PROFILES["half-body irradiation"] = P(
    O.MARROW, 0.30, True,
    "low-dose-rate half-body irradiation with L-CHOP: grade 3-4 toxicity in 4.5% of treatments; 39 dose "
    "reductions and 74 delays over 28 weeks (PMID 42525883); haematological toxicity worse at 8 Gy than "
    "6 Gy, one treatment death in 13 dogs (PMID 19178684)",
    source="Dog, PMIDs 42525883, 19178684, 40088118, 37700548.",
    secondary_axis=O.GI, secondary_fraction=0.30,
    sustainable_days=28.0, hard_cap_days=28.0, reversible=True)


def _check_no_gaps() -> None:
    """A registry with duplicate-looking heads would make `profile_for` ambiguous; fail at import."""
    heads = {}
    for k in PROFILES:
        h = k.split(" (")[0].split(" / ")[0].strip().lower()
        heads.setdefault(h, []).append(k)
    dup = {h: ks for h, ks in heads.items() if len(ks) > 1}
    # Deliberate near-duplicates are disambiguated by exact match in `profile_for`.
    allowed = {"cyclophosphamide", "prednisolone", "cd20 car-t", "cytarabine cri"}
    bad = {h: ks for h, ks in dup.items() if h not in allowed}
    assert not bad, f"ambiguous profile heads: {bad}"


_check_no_gaps()

# ---- widened universe (core/lymphoma_universe.py) ---------------------------------------------------------
PROFILES["autologous tumour vaccine (APAVAC-type, HSPPC + hydroxyapatite)"] = P(
    O.IMMUNE_MEDIATED, 0.05, True,
    "no adverse events recorded in 300 dogs; needs a surgical node excision at diagnosis (procedure risk not "
    "counted here)",
    source="Marconato et al., 300 dogs (PMID 31174615): 'no adverse events'. Follow-up with data reaches about 3 "
           "years. Long-term autoimmunity: NOT FOUND.",
    cumulative=False, sustainable_days=365.0, hard_cap_days=None, reversible=True)

PROFILES["autologous T-cell add-back after chemotherapy"] = P(
    O.IMMUNE_MEDIATED, 0.10, True,
    "no complications reported in 8 infused dogs; requires leukapheresis/expansion at a commercial laboratory",
    source="Mason et al., 8 dogs, cells persisted up to 49 d (PMID 22355761); infusions given without adverse events "
           "in 10 transplanted dogs (PMID 34950726). Persistence is the limit, so the window is 49 d.",
    cumulative=False, sustainable_days=49.0, hard_cap_days=None, reversible=True)

PROFILES["panobinostat (HDAC inhibitor)"] = P(
    O.MARROW, 0.50, False,
    "thrombocytopenia (67% grade 3/4 with bortezomib + dexamethasone in humans), neutropenia, diarrhoea; QTc "
    "prolongation at higher doses. NO canine toxicity data found (dog toxicology: testicular and marrow findings at 1.5 mg/kg)",
    source="HUMAN label and PANORAMA-1 (docs/universe/SWEEP_pk.md s13). Canine tolerability: NOT FOUND.",
    secondary_axis=O.GI, secondary_fraction=0.25, sustainable_days=84.0, hard_cap_days=None, reversible=True)
PROFILES["vorinostat (HDAC inhibitor)"] = P(
    O.GI, 0.30, False,
    "diarrhoea and nausea, thrombocytopenia, fatigue (human); dog target organ GI (NOAEL 60 mg/kg/d). Canine tolerability "
    "at therapeutic exposure: valproate + doxorubicin phase I in 21 dogs was well tolerated (PMID 20705615), a different drug.",
    source="HUMAN label (docs/universe/SWEEP_pk.md s13).", sustainable_days=84.0, hard_cap_days=None, reversible=True)
PROFILES["bortezomib (proteasome inhibitor)"] = P(
    O.MARROW, 0.35, False,
    "thrombocytopenia 32%, peripheral neuropathy 38% (human); in dogs only 2 treated animals were reported "
    "(conjunctivitis at ~90% inhibition, PMID 23579193)",
    source="HUMAN label (docs/universe/SWEEP_pk.md s13).", secondary_axis=O.PERIPHERAL_NERVE, secondary_fraction=0.30, sustainable_days=84.0, hard_cap_days=None, reversible=True)

PROFILES["high-dose thiotepa-based consolidation with autologous stem-cell rescue [human regimen]"] = P(
    O.MARROW, 1.0, False,
    "obligatory marrow aplasia needing autologous rescue; treatment-related mortality 3-8% in humans (infection, "
    "pulmonary embolism); no excess neurotoxicity vs other consolidation",
    source="HUMAN: PMID 42486133, 35834762, 22023529, 41108618. Canine thiotepa tolerance: NOT FOUND. Busulfan 40 mg/kg "
           "caused severe CNS toxicity in dogs (PMID 10534062).",
    secondary_axis=O.GI, secondary_fraction=0.30, sustainable_days=115.0, hard_cap_days=115.0, reversible=False)
PROFILES["anti-CD20 monoclonal antibody, intraventricular/intrathecal [buildable route]"] = P(
    O.CNS_LOCAL, 0.10, False,
    "grade 3 neurotoxicity ~4-8% in children after intraventricular rituximab; chronic CSF-access hazards "
    "(reservoir infection ~0.2% per device-year in one human series; 100x spread across series)",
    source="HUMAN: PMID 24190981 and the regional-delivery sweep (docs/universe/SWEEP_regional.md s11). Dogs: NOT FOUND. "
           "Window limited by access-device hazards, not by drug toxicity.",
    sustainable_days=365.0, hard_cap_days=None, reversible=True)
for _n in ("tandem CD19/CD20 CAR-T, intraventricular/intrathecal [buildable]",
           "CD7-directed CAR-T, intraventricular/intrathecal [buildable]",
           "CD5 + CD7 dual-target CAR-T, intraventricular/intrathecal [buildable]"):
    PROFILES[_n] = P(
        O.CNS_LOCAL, 0.30, False,
        "neurotoxicity (ICANS-type) 30-100% any grade, grade >=3 about 0-30% in human intraventricular/intrathecal CAR-T "
        "for CNS tumours (n=3-65 per trial); cytokine release",
        source="HUMAN solid-CNS trials (docs/universe/SWEEP_regional.md s11); lymphoma intrathecal CAR-T: NOT FOUND; dogs: NOT FOUND.",
        secondary_axis=O.IMMUNE_MEDIATED, secondary_fraction=0.30, sustainable_days=270.0, hard_cap_days=None, reversible=True)

PROFILES["allogeneic DLA-identical HCT (graft-versus-lymphoma)"] = P(
    O.IMMUNE_MEDIATED, 0.30, True,
    "procedure mortality 2/15 (13%, both dogs not in remission), acute grade 2 skin GVHD 3/13, no chronic GVHD, universal marrow aplasia "
    "with ANC >1000 by day 9-18; cyclosporine diabetes 1/15",
    source="DOG: PMID 35789057 (15 dogs). HUMAN comparator NRM 31% vs 3% allo vs auto in T-cell lymphoma (PMID 39270145). "
           "docs/universe/SWEEP_hct_model.md s5, s7.",
    secondary_axis=O.MARROW, secondary_fraction=0.60, sustainable_days=166.0, hard_cap_days=166.0, reversible=False)
PROFILES["dTERT genetic vaccine (Tel-eVax-type)"] = P(
    O.IMMUNE_MEDIATED, 0.05, True,
    "no adverse effects in 52 vaccinated dogs; electroporation under anaesthesia at each cycle",
    source="DOG: PMIDs 20531395, 23902422, 30537967. Long-term autoimmunity: NOT FOUND.",
    sustainable_days=365.0, hard_cap_days=None, reversible=True)
PROFILES["cytarabine ocfosfate, oral continuous"] = P(
    O.GI, 0.50, True,
    "GI toxicity 65% (grade 3-4 19%) and neutropenia 35% on cytarabine infusion in 26 dogs; oral prodrug tolerability in dogs: 4 dogs, no events reported",
    source="DOG: PMIDs 31769013, 37670479.", secondary_axis=O.MARROW, secondary_fraction=0.35,
    sustainable_days=84.0, hard_cap_days=None, reversible=True)
PROFILES["CD3xCD20 bispecific T-cell engager (canine-specific) [needs development]"] = P(
    O.IMMUNE_MEDIATED, 0.35, False,
    "cytokine release 31-63% (grade >=3 3-5%), ICANS 8% (25% with CNS involvement), grade 3 infections 24%, B-cell aplasia",
    source="HUMAN: PMIDs 39322711, 42622258, 42579821. No canine engager safety data.",
    sustainable_days=365.0, hard_cap_days=None, reversible=True)
