"""The measured inputs behind each agent's potency, and what can and cannot be derived from them.

Every number here was read from the cited source by a literature agent this session and the sentence
quoted; conversions to molar units are arithmetic and are marked. A `Measurement` refuses to be read
for a population it was not measured in, so an IC50 from a B-cell line cannot silently become a T-cell
number.

WHAT THE INPUTS SUPPORT (grade each agent by these, not by the catalogue's hand-set potency)

  DERIVED     IC50 in canine lymphoma cells AND an exposure in dogs, both measured  -> a kill rate
  PARTIAL     one input measured, the other second-hand or assumed                   -> a kill rate, flagged
  HINGE       exposure measured, IC50 not found                                      -> the IC50 it NEEDS
  BRACKET     two measurements that disagree                                         -> a range, no point
  OUTCOME     no IC50 (cell therapy, radiation, antibody); measured clinical or in-vivo depletion data
  ASSUMED     nothing measured                                                       -> catalogue value

The plasma-concentration-versus-in-vitro-IC50 method is a LOWER BOUND for tissue-accumulating
cytotoxics (doxorubicin, hydroxychloroquine): `CYTOTOXIC_INTEGRATED_EXPOSURE` below shows it
predicts a per-dose kill an order of magnitude below what CHOP demonstrably does, so the CHOP potencies
in the catalogue stay outcome-calibrated (PFS 176 d, PMID 26279153) rather than derived.
"""

from __future__ import annotations

import math

from .core.evidence import Disease, Measurement, Population, Provenance, Quantity, Species
from .lymphoma_pkpd import (GROWTH_PER_DAY, DerivedPotency, derive, emax_kill_rate,
                            ng_per_ml_to_nM, required_ic50_nM, time_average_nM)

M = Measurement
IN_VITRO = Species.IN_VITRO
DOG = Species.DOG
LYM = Disease.CANINE_LYMPHOMA
LYM_B = Disease.CANINE_LYMPHOMA_B
LYM_T = Disease.CANINE_LYMPHOMA_T


def _cells(agent, disease=LYM, note=""):
    return Population(IN_VITRO, disease, agent=agent, note=note or "canine lymphoma cell line / primary cells")


def _dog(agent, disease=LYM):
    return Population(DOG, disease, agent=agent)


# ---- verdinexor: the one agent with BOTH inputs measured in canine lymphoma ----------------------------
_VERD_MW = 442.3      # g/mol (verdinexor); conversion only
_VERD_AUC_ng_h_ml = 1970.6     # Phase II day-14 AUC, dogs with lymphoma, 1.25-1.5 mg/kg MWF (PMID 30143046)
_VERD_INTERVAL_H = 56.0        # Mon-Wed-Fri: mean gap (48+48+72)/3

VERDINEXOR_IC50_B = M(108.6, Quantity.IC50_NM, _cells("verdinexor", LYM_B), "PMID 40872651",
                      n=3, spread=(89.8, 294.3),
                      justification="", provenance=Provenance.MEASURED)
VERDINEXOR_IC50_T = M(220.5, Quantity.IC50_NM, _cells("verdinexor", LYM_T), "PMID 40872651",
                      n=5, spread=(147.8, 418.0), provenance=Provenance.MEASURED)
#: A second laboratory measured the SAME B-cell line (CLBL-1) 13x more sensitive (72 h MTS vs 48 h
#: WST-8). Carried, not averaged away.
VERDINEXOR_IC50_CLBL1_OTHER_LAB = M(8.5, Quantity.IC50_NM, _cells("verdinexor", LYM_B), "PMID 24503695",
                                    n=1, spread=None, provenance=Provenance.MEASURED)
VERDINEXOR_CAVG = M(time_average_nM(ng_per_ml_to_nM(_VERD_AUC_ng_h_ml, _VERD_MW), 1.0) / _VERD_INTERVAL_H,
                    Quantity.CTROUGH_NM, _dog("verdinexor"),
                    "PMID 30143046 (AUC 1970.6 h*ng/mL per dose, dogs with lymphoma); averaged over a "
                    "56 h MWF interval (calculation)", n=7, provenance=Provenance.DERIVED)


def verdinexor(immunophenotype: str) -> DerivedPotency:
    ic50 = VERDINEXOR_IC50_T if immunophenotype == "T" else VERDINEXOR_IC50_B
    return derive("verdinexor (XPO1 inhibitor)", ic50, VERDINEXOR_CAVG, assay_days=2.0,
                  note="48 h assay; exposure is the time-averaged plasma concentration. Total (not "
                       "free) concentration; protein binding not applied.")


# ---- venetoclax: T-cell EC50 measured; canine exposure only second-hand ------------------------------
VENETOCLAX_EC50_T = M(23.0, Quantity.IC50_NM, _cells("venetoclax", LYM_T), "PMID 36433867",
                      n=7, spread=(5.0, 41.0), provenance=Provenance.MEASURED)   # 0.023 +/- 0.018 uM
VENETOCLAX_EC50_B = M(288_000.0, Quantity.IC50_NM, _cells("venetoclax", LYM_B), "PMID 36433867",
                      n=7, spread=None, provenance=Provenance.MEASURED)          # mean 288 uM, SD 700
#: Canine AUC 73.6 ug*h/mL at 20 mg/kg/day is quoted in the Jegatheeson discussion WITHOUT a primary
#: citation. Treated as measured-but-second-hand; free fraction is ASSUMED because it was not found.
VENETOCLAX_AUC_20MGKG_UG_H_ML = 73.6
_VEN_MW = 868.4
VENETOCLAX_FREE_FRACTION_SWEEP = (0.01, 0.001)     # ASSUMED (high protein binding); not found


def venetoclax_T_kill(dose_mg_kg: float = 10.0, free_fraction: float = 0.01) -> float:
    """Kill rate against canine T-cell lymphoma from the measured EC50 and the second-hand canine AUC,
    linear in dose (an assumption), 24 h assay."""
    auc = VENETOCLAX_AUC_20MGKG_UG_H_ML * dose_mg_kg / 20.0
    cavg_nM = ng_per_ml_to_nM(auc * 1000.0 / 24.0, _VEN_MW)      # ug*h/mL -> ng*h/mL, over 24 h
    return emax_kill_rate(VENETOCLAX_EC50_T.value, cavg_nM * free_fraction, assay_days=1.0)


def venetoclax_T_min_dose_to_close(free_fraction: float = 0.01, target: float = GROWTH_PER_DAY) -> float:
    """Smallest daily dose (mg/kg) at which the derived kill reaches the bar."""
    lo, hi = 1e-4, 200.0
    for _ in range(80):
        mid = math.sqrt(lo * hi)
        if venetoclax_T_kill(mid, free_fraction) >= target:
            hi = mid
        else:
            lo = mid
    return hi


def venetoclax_B_kill(dose_mg_kg: float = 10.0, free_fraction: float = 0.01) -> float:
    auc = VENETOCLAX_AUC_20MGKG_UG_H_ML * dose_mg_kg / 20.0
    cavg_nM = ng_per_ml_to_nM(auc * 1000.0 / 24.0, _VEN_MW)
    return emax_kill_rate(VENETOCLAX_EC50_B.value, cavg_nM * free_fraction, assay_days=1.0)


# ---- hydroxychloroquine: exposure and accumulation measured, IC50 NOT FOUND -> the hinge ---------------
_HCQ_MW = 335.9
HCQ_PLASMA = M(ng_per_ml_to_nM(105.1, _HCQ_MW), Quantity.CTROUGH_NM, _dog("hydroxychloroquine"),
               "PMID 24991836 (105.1 +/- 73.1 ng/mL, day 4 pre-doxorubicin, 12.5 mg/kg/day; a single "
               "time point, not a Cmax)", n=15, provenance=Provenance.MEASURED)
HCQ_TUMOUR_TO_PLASMA = 100.0        # PMID 24991836: 100-fold in tumour biopsy vs plasma
HCQ_TUMOUR = M(HCQ_PLASMA.value * HCQ_TUMOUR_TO_PLASMA, Quantity.TISSUE_PLASMA_RATIO, _dog("hydroxychloroquine"),
               "PMID 24991836 (100-fold tumour:plasma) x plasma above (calculation)", n=15,
               provenance=Provenance.DERIVED)


def hcq_hinge(assay_days: float = 3.0, target: float = GROWTH_PER_DAY) -> DerivedPotency:
    """No canine-lymphoma IC50 exists in the record; report the IC50 HCQ would need."""
    return derive("hydroxychloroquine (autophagy)", None, HCQ_TUMOUR, assay_days, target_kill=target)


# ---- prednisolone: two measurements that disagree ---------------------------------------------------
PRED_CMAX_1_TO_2_MGKG_NM = (ng_per_ml_to_nM(268.1, 360.4), ng_per_ml_to_nM(314.3, 360.4))   # healthy beagles
PRED_IC50_LINE_1771_UM = M(44.0, Quantity.IC50_NM, _cells("prednisolone", LYM_B), "PMID 41595541",
                           n=1, provenance=Provenance.MEASURED)   # 44 uM = 44,000 nM below
PRED_PROLIFERATION_DROP_72H = 0.35    # PMID 24975508: 'mild (35%)' in GL-1 and GL-40; concentration not stated


def prednisolone_bracket() -> dict:
    """(low, high) per-day kill from the two disagreeing measurements. NOT a point estimate."""
    low = emax_kill_rate(44_000.0, PRED_CMAX_1_TO_2_MGKG_NM[1], assay_days=2.0)     # IC50 + healthy-beagle Cmax
    high = -math.log(1.0 - PRED_PROLIFERATION_DROP_72H) / 3.0                        # 35% in 72 h, conc unstated
    return {"low_per_day": low, "high_per_day": high,
            "ratio": high / low,
            "basis": "low: IC50 44 uM (line 1771, PMID 41595541) with a 2 mg/kg Cmax (healthy beagles, "
                     "PMID 33195563); high: 35% proliferation drop in 72 h at an UNSTATED concentration "
                     "(GL-1/GL-40, PMID 24975508). Both are canine lymphoid cells. They disagree ~15x, so "
                     "the catalogue's 0.10 is neither derived nor contradicted."}


# ---- acalabrutinib: exposure measured; signalling inhibited, killing 'modest' ------------------------
ACALA_CMAX_PER_MGKG_NM = 419.0     # PMID 27434128 'C/Dose 195 ng/ml or 419 nM' (per mg/kg; subscript lost)
ACALA_NOTE = ("BTK signalling inhibited at 10 nM-1 uM in CLBL1 and 4 primary canine lymphomas and BTK "
              "occupancy >90% in nodes, but viability change was 'modest' and not significant; clinical "
              "ORR 25%, median PFS 22.5 d (PMID 27434128). Signalling block is measured; a cell-killing "
              "IC50 is NOT FOUND, so no kill rate is derived.")


# ---- antibody: in-vivo depletion of the target lineage is measured ---------------------------------
CD21_FRACTION_OF_BASELINE = {7: 0.04, 21: 0.01}     # PMID 38662527 (1E4-cIgGB + doxorubicin, 42 dogs)


def antibody_depletion_rates() -> dict:
    """Per-day exponential decline of CD21+ B cells in the dog: day 0-7, and day 7-21 (the slower,
    more conservative phase, which also reflects B-cell recovery)."""
    early = -math.log(CD21_FRACTION_OF_BASELINE[7]) / 7.0
    late = -math.log(CD21_FRACTION_OF_BASELINE[21] / CD21_FRACTION_OF_BASELINE[7]) / 14.0
    return {"day_0_to_7": early, "day_7_to_21": late,
            "basis": "median fraction of baseline 0.04 (day 7) and 0.01 (day 21), PMID 38662527. These "
                     "are NORMAL B cells in blood, in dogs also given doxorubicin; nodal tumour access "
                     "is not measured. The slower phase is used for the model."}


# ---- CAR-T: persistence is what was measured --------------------------------------------------------
CAR_T_PERSISTENCE_DAYS = {
    "circulating, 5-dog trial": 28, "lymph-node peak (one dog)": 50, "CRS case, undetectable by": 14,
}   # PMIDs 32002286, 35898541, 38573683


# ---- the plasma-vs-IC50 method under-predicts cytotoxics: shown, not asserted -----------------------
def cytotoxic_integrated_exposure() -> dict:
    """Kill per dose from plasma AUC against the in-vitro IC50 x assay-duration exposure. If this were
    the whole story CHOP would do almost nothing; it demonstrably does not (98% response, PMID
    26279153). So plasma-derived kill is a LOWER BOUND for these drugs."""
    # doxorubicin: AUC0-6h 547.3 nM*h in lymphoma dogs (PMID 30638304); CLBL-1 IC50 24.8 ng/mL = 42.8 nM, 48 h
    dox_ratio = 547.3 / (42.8 * 48.0)
    # vincristine: AUC 2349 ng*min/mL (PMID 25649934, a non-lymphoma dog); CLBL-1 IC50 2.0 nM, 48 h
    vcr_auc_nM_h = ng_per_ml_to_nM(2349.0 / 60.0, 923.0)
    vcr_ratio = vcr_auc_nM_h / (2.0 * 48.0)
    return {"doxorubicin": {"exposure_ratio": dox_ratio, "e_folds_per_dose": math.log1p(dox_ratio)},
            "vincristine": {"exposure_ratio": vcr_ratio, "e_folds_per_dose": math.log1p(vcr_ratio)},
            "reading": "about 0.2-0.4 e-folds of kill per dose against ~1.9 e-folds of regrowth per "
                       "21-day cycle at 0.0903/day: the plasma method cannot reproduce CHOP's known "
                       "activity, so it is a lower bound for tissue-accumulating cytotoxics."}


# ---- P-gp reversal: the exposure multiplier the toxicity model needs ---------------------------------
#: valspodar let doxorubicin be cut 30% with 'equivalent therapeutic exposure' (osteosarcoma dogs,
#: PMID 15492788) and the lymphoma trial cut the first dose 30% as a precaution (PMID 28357033). Both
#: imply ~1/0.7. Human myeloma data show a doubling of doxorubicin AUC (quoted in PMID 28357033, HUMAN).
EFFLUX_CO_DOSE_MULTIPLIER_CANINE_PROXY = 1.0 / 0.7
EFFLUX_CO_DOSE_MULTIPLIER_SWEEP = (1.43, 2.0, 2.5)


# ---- recurrent-lesion prevalence in canine lymphoma (bears on 'early detection removes it') -----------
#: These are FOUNDER lesions in WGS/panel series, i.e. present in the tumour from the start in that
#: fraction of dogs -- an escape present in the founder clone is NOT removed by earlier detection.
RECURRENT_LESIONS = {
    "TRAF3 (NF-kB regulator)": {"B_cell_fraction": 0.581, "n": 43, "pmid": "39922874",
                                "note": "52.7% in 205 B-cell (PMID 39134766). TRAF3 mutation is "
                                        "associated with LONGER survival (PMID 40506464): not a "
                                        "uniform adverse signal."},
    "TP53": {"B_cell_fraction": 0.256, "n": 43, "pmid": "39922874",
             "note": "aggressive B-cell time-to-progression 52 vs 202 days (mutant vs wild-type), "
                     "PMID 39134766; tied to shorter OS in 238 dogs, PMID 40506464."},
    "FBXW7": {"B_cell_fraction": 0.302, "n": 43, "pmid": "39922874", "note": ""},
    "POT1": {"B_cell_fraction": 0.302, "n": 43, "pmid": "39922874",
             "note": "not predictive of worse prognosis (PMID 36016811)."},
    "NFKBIA (intestinal T-cell)": {"T_cell_fraction": 31 / 54, "n": 54, "pmid": "40877743", "note": ""},
}


# ---- cytarabine by continuous infusion: CNS access is MEASURED in dogs -------------------------------
_ARAC_MW = 243.2
#: Scott-Moncrieff 1991 (PMID 1742843), ten healthy dogs, 600 mg/m2 as a 12 h infusion (50 mg/m2/h):
#: plasma steady state 14.1 +/- 4.2 uM, CSF steady state 8.3 +/- 1.1 uM, CSF:plasma 0.62 +/- 0.14.
ARAC_PLASMA_SS = M(14_100.0, Quantity.CTROUGH_NM, _dog("cytarabine"), "PMID 1742843", n=4,
                   provenance=Provenance.MEASURED)
ARAC_CSF_SS = M(8_300.0, Quantity.CTROUGH_NM, _dog("cytarabine"), "PMID 1742843 (CSF, intact barrier)",
                n=4, provenance=Provenance.MEASURED)
#: IC50 in canine lymphoma lines, 48 h (PMID 25715778 Table 1): CLBL-1 (B) 91.7 ng/mL, Ema (T,
#: P-gp-active) 736 ng/mL.
ARAC_IC50_B = M(ng_per_ml_to_nM(91.7, _ARAC_MW), Quantity.IC50_NM, _cells("cytarabine", LYM_B),
                "PMID 25715778 (CLBL-1, 48 h)", n=1, provenance=Provenance.MEASURED)
ARAC_IC50_T = M(ng_per_ml_to_nM(736.0, _ARAC_MW), Quantity.IC50_NM, _cells("cytarabine", LYM_T),
                "PMID 25715778 (Ema, 48 h)", n=1, provenance=Provenance.MEASURED)
ARAC_INFUSION_H = 12.0


def cytarabine_cri(immunophenotype: str, compartment: str = "systemic") -> DerivedPotency:
    """Kill per day DURING the infusion, from the measured steady-state concentration in the named
    compartment (plasma or CSF) against the canine-lymphoma-line IC50. Duty (12 h per interval) is
    applied by the caller."""
    ic50 = ARAC_IC50_T if immunophenotype == "T" else ARAC_IC50_B
    conc = ARAC_CSF_SS if compartment == "cns" else ARAC_PLASMA_SS
    return derive("cytarabine CRI", ic50, conc, assay_days=2.0,
                  note="steady-state concentration during a 12 h infusion; total not free (cytarabine is "
                       "little protein bound). Whether cytarabine is a canine P-gp substrate is NOT FOUND.")


# ---- hydroxychloroquine: TRANSFERRED potency, canine tumour concentration ---------------------------------
#: No canine-lymphoma IC50 exists. Human lymphoid IC50s: primary B-CLL 32 +/- 7 ug/mL = ~95 uM at 24 h
#: (PMID 11167827); adult T-cell leukaemia/lymphoma lines 25.9 +/- 15.1 uM at 48 h (PMID 34407152). The
#: canine TUMOUR concentration is measured (about 31 uM, PMID 24991836). Justification for the transfer: the
#: mechanism is lysosomal accumulation (a physicochemical property, PMID 32389720), not a species-specific
#: target; the conservative (CLL, 24 h) IC50 is used. Caveat that reduces coverage: HCQ is a P-gp substrate
#: (P-gp-overexpressing cells 5.2x more resistant, PMID 32992777), so it is marked a substrate.
HCQ_IC50_HUMAN_CLL_NM = M(32.0 / _HCQ_MW * 1e6, Quantity.IC50_NM,
                          Population(Species.HUMAN, Disease.NONE, agent="hydroxychloroquine",
                                     note="primary B-CLL cells, 24 h"), "PMID 11167827", n=20,
                          provenance=Provenance.MEASURED)
HCQ_IC50_TRANSFERRED = HCQ_IC50_HUMAN_CLL_NM.transfer_to(
    _cells("hydroxychloroquine"),
    "lysosomotropic accumulation is a physicochemical property shared across species; the most conservative "
    "human lymphoid IC50 (CLL, 24 h) is used; human ATLL lines are 4-7x more sensitive", scale=1.0)


def hcq_transfer() -> DerivedPotency:
    """Kill per day: transferred human IC50 x measured canine tumour concentration, 24 h assay."""
    return derive("hydroxychloroquine (autophagy)", HCQ_IC50_TRANSFERRED, HCQ_TUMOUR, assay_days=1.0,
                  note="TRANSFERRED IC50 (human CLL) with a measured canine tumour concentration")


# ---- radiation: kill DERIVED from measured canine lymphoid-line survival ---------------------------------
#: Clonogenic survival of canine lymphoid lines after gamma irradiation, SF2 and SF5 from linear-quadratic
#: fits (PMID 27257868, Table 1). Alpha and beta are solved from the two points (arithmetic, not in the paper).
#: Canine lymphoid lines are NOT highly radiosensitive (SF2 0.53-0.85), and human PCNSL shows a similar
#: 'relative radioresistance' (PMID 1572835, 10563430). The most resistant line is the CONSERVATIVE input.
RT_SURVIVAL = {"CLBL1": (0.53, 0.06), "OSW": (0.61, 0.15), "1771": (0.75, 0.27), "CLL1390": (0.85, 0.36)}


def lq_alpha_beta(sf2: float, sf5: float) -> tuple:
    """Solve ln SF(D) = -alpha*D - beta*D^2 from SF2 and SF5; alpha is floored at 0 (a negative alpha has no
    meaning), in which case beta is refit to SF2 alone."""
    a, b = -math.log(sf2), -math.log(sf5)          # a = 2 alpha + 4 beta ; b = 5 alpha + 25 beta
    beta = (b - 2.5 * a) / 15.0
    alpha = a / 2.0 - 2.0 * beta
    if alpha < 0.0:
        alpha, beta = 0.0, a / 4.0
    return alpha, beta


def rt_efolds(line: str, dose_per_fraction_gy: float, fractions: int) -> float:
    """e-folds of kill for a course of `fractions` acute fractions (no repair between them beyond the LQ
    single-fraction model, and no repopulation: both favour the tumour less than reality)."""
    alpha, beta = lq_alpha_beta(*RT_SURVIVAL[line])
    d = dose_per_fraction_gy
    return fractions * (alpha * d + beta * d * d)


#: Courses: craniospinal 23.4 Gy in 13 x 1.8 Gy (the human reduced-dose WBRT schedule, PMID 24101038; canine
#: whole-brain 10 x 4 Gy is tolerated, PMID 41420297); half-body 6 Gy per half in one fraction (PMID 19627472,
#: 42525883); total body 10 Gy as 2 x 5 Gy (PMID 22882500, 31146304). Course length in days sets the per-day rate.
RT_COURSES = {
    "craniospinal radiotherapy": (1.8, 13, 18.0),
    "half-body irradiation (low-dose-rate)": (6.0, 1, 28.0),
    "total body irradiation + transplant": (5.0, 2, 14.0),
}


def rt_kill_per_day(agent_name: str, line: str = "CLL1390") -> float:
    d, n, days = RT_COURSES[agent_name]
    return rt_efolds(line, d, n) / days


# ---- continuous intrathecal cytarabine: a DESIGN specification with computed requirements -------------------
#: Free cytarabine leaves the canine CSF with a half-life of 113 +/- 26 min (PMID 1742843), so a bolus gives
#: hours of exposure. A pump holds a setpoint instead. Continuous intrathecal pump infusion is done in dogs
#: for other drugs (baclofen up to 28 d, PMID 8164885; morphine caused catheter-tip masses, PMID 31124198).
#: Human sustained-release intrathecal cytarabine keeps CSF above the cytotoxic threshold 0.1 mg/L (= 411 nM)
#: for >= 14 d (PMID 10506606, 24129691, 17112293). Dog CSF volume is NOT FOUND here; 30 mL is an assumed
#: round number and only scales the infusion rate, not the derived kill.
ARAC_CSF_HALF_LIFE_MIN = 113.0
DOG_CSF_VOLUME_ML = 30.0


def continuous_it_cytarabine(immunophenotype: str, csf_setpoint_nM: float = 3000.0) -> dict:
    """Kill per day at a held CSF concentration (canine lymphoma-line IC50, 48 h) and the infusion rate the
    canine CSF half-life implies for that setpoint: rate = C x V x k_elim."""
    ic50 = ARAC_IC50_T if immunophenotype == "T" else ARAC_IC50_B
    kill = emax_kill_rate(ic50.value, csf_setpoint_nM, 2.0)
    k_elim_per_h = math.log(2) / (ARAC_CSF_HALF_LIFE_MIN / 60.0)
    mg_per_day = csf_setpoint_nM * 1e-9 * _ARAC_MW * (DOG_CSF_VOLUME_ML / 1000.0) * k_elim_per_h * 24.0 * 1000.0
    return {"kill_per_day": kill, "ic50_nM": ic50.value, "setpoint_nM": csf_setpoint_nM,
            "infusion_mg_per_day": mg_per_day}
