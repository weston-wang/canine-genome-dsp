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
