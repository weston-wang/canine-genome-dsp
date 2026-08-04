"""Illustrative scenario presets for a PI3K/mTOR-pathway resistance model of canine hemangiosarcoma.

Canine hemangiosarcoma (HSA) is genetically heterogeneous, not a single-hotspot disease the way
histiocytic sarcoma (PTPN11/KRAS) is: real, published somatic-mutation cohorts find TP53
loss-of-function in up to ~66% of cases, activating PIK3CA mutations (H1047R is the dominant
hotspot residue) in ~30-46%, PTEN loss-of-function in 3-10%, and NRAS Q61 hotspot mutations
(largely restricted to splenic HSA and mostly mutually exclusive with TP53) in ~7-24% (Megquier
et al. 2019, Mol Cancer Res, whole-exome sequencing of 47 golden retriever HSA cases + RNA-seq of
74 tumors, Broad/NHGRI Lindblad-Toh lab; Estabrooks et al. 2023, Vet Comp Oncol, PMID 37734854;
Wong et al. 2017, PLOS ONE, PMID 29190660). This module deliberately does not attempt one model
covering "HSA" generically -- it scopes to the PIK3CA/PTEN-driven, PI3K/mTOR-pathway subtype
specifically, both because that is where the real anchors below exist and because a real,
directly relevant negative result argues against building the most obvious alternative (an
NRAS-driven, MEK-inhibitor scenario mirroring the histiocytic-sarcoma module): a large real-world
cohort found trametinib conferred no survival benefit in NRAS-mutant HSA (241 vs. 259 days,
p=0.7775, n=71 vs. 26 -- Rodrigues et al. 2025, Sci Rep, PMID 40368987, PMC12078565, the FidoCure
precision-medicine platform's real-world-evidence study of 508 dogs with splenic HSA), despite
real in vitro MEK-dependence data for NRAS-mutant HSA cell lines existing (Andrade et al., PMC3769440).
Building an optimistic hypothetical scenario there would contradict a real result already in hand.

The PI3K/mTOR angle, by contrast, has three real anchors this module can build on, each verified
directly against its source rather than taken from a summary: a real in vitro cellular potency
measurement (Pyuen et al. 2018, PLOS ONE 13(7):e0200634, PMID 30011343: the dual PI3K/mTOR
inhibitor VDC-597 gave IC50 0.23, 0.69, and 0.71 uM on three canine HSA cell lines -- CIN-, SB-,
and DEN-HSA respectively -- additive with doxorubicin); real canine PK/PD data for the clinically
relevant drug in this class, rapamycin/sirolimus (Paoloni et al. 2010, PLOS ONE 5(6):e11013, PMID
20543980: a comparative-oncology dose-escalation study in dogs *with cancer* (osteosarcoma, not
HSA) found median trough concentrations exceeding 10 ng/mL at 0.06-0.08 mg/kg IM daily -- matching
human transplant target levels -- with no MTD reached and confirmed target inhibition
(>2-fold reduction in tumoral phospho-S6RP in 8/10 dogs)); and a real-world survival benchmark
specifically in HSA (the same FidoCure study above): TP53-mutant dogs given rapamycin had a median
survival of 193 vs. 118 days without it (p<0.0001), and PIK3CA-mutant dogs 179 vs. 119 days
(p=0.005). VDC-597 itself has no published canine dosing; rapamycin is the real clinically-used
drug with no published HSA-cell-line potency number of its own -- a more severe version of the
proxy-drug mismatch `mapk_scenarios.dog_preset` documents for cobimetinib/trametinib. There, both
numbers were the same drug's own measurements; here, naively pairing VDC-597's real IC50 with
rapamycin's real trough would put achievable exposure ~50x *below* IC50, predicting the drug
barely works -- directly contradicting the real survival benefit just cited. `dog_hsa_preset`
resolves this by keeping the reference concentration illustrative rather than publishing that
self-contradictory pairing; see its own docstring for the exact reasoning.
"""

import numpy as np

from .mapk_resistance import ResistanceModel

# Display labels for the 4 clones this scenario tracks (sensitive + 3 resistance mechanisms),
# analogous in role to mapk_resistance.CLONE_NAMES but HSA/mTOR-inhibitor-specific, not reused
# from the histiocytic-sarcoma module's own labels.
HSA_CLONE_NAMES = ["sensitive", "pi3k_akt_feedback_reactivation", "mapk_crosstalk_bypass",
                   "target_site_mutation"]

# Three synthetic escape mechanisms, chosen for general applicability to any mTORC1 inhibitor
# rather than HSA-specific evidence (none exists): (1) loss of mTORC1-mediated negative feedback
# on PI3K/AKT/mTORC2 reactivating upstream survival signaling around the drug -- a real, general
# mechanism of rapalog resistance documented across human cancers, not measured in HSA; (2)
# parallel MAPK/ERK pathway activation providing an alternative proliferative route independent of
# mTORC1 -- real, documented PI3K-MAPK pathway crosstalk, general oncology literature, not
# HSA-specific; (3) on-target (FKBP12-mTOR binding site) mutation reducing rapamycin binding, the
# generic resistance category seen across kinase/allosteric inhibitors. As with the histiocytic-
# sarcoma module, these are this module's own speculative extension of general resistance biology,
# not a finding, and every growth rate, potency shift, and kill ceiling below is illustrative,
# clearly labeled as such, and not fit to any HSA-specific measurement.
_SHARED_GROWTH = np.array([.055, .05, .05, .052])   # per-day; illustrative, not fitted
_SHARED_MAX_KILL = np.array([.16, .02, .03, .015])  # per-day kill-rate ceiling per clone
_SHARED_IC50_RATIOS = np.array([1.0, 35.0, 1.15, 50.0])
_SHARED_MUTATION = np.eye(4)  # acquired resistance is scheduled stochastically, not via this matrix

# Loosely illustrative, not fit to any HSA-specific measurement -- there is no equivalent of HS's
# handful of durable-response case reports to loosely tune against here, so this is a bare
# placeholder rather than even a loose anchor. Swept, not fixed, for the same reason every other
# genuinely unknown quantity in the histiocytic-sarcoma module is swept.
_SEEDING_RATE_TOTAL = 0.012
_PREEXISTING_PROB_SWEEP = [0.05, 0.15, 0.30, 0.50, 0.70]
_PREEXISTING_PROB_CENTRAL = 0.30

# Real-world survival benchmark from the same 508-dog FidoCure cohort the module docstring
# describes -- retrospective, not a controlled trial, and mixes whatever other concurrent
# treatments (chemotherapy, other targeted drugs) individual dogs happened to receive, so this is
# provided for scale, not a like-for-like comparator, the same role LOMUSTINE_BENCHMARK plays for
# histiocytic sarcoma.
HSA_RAPAMYCIN_BENCHMARK = {
    "citation": "Rodrigues et al. 2025, Sci Rep 15, PMID 40368987, PMC12078565 -- FidoCure "
               "real-world-evidence study, 508 dogs with splenic hemangiosarcoma",
    "subgroups": [
        {"mutation": "TP53", "median_survival_with_rapamycin_days": 193,
         "median_survival_without_rapamycin_days": 118, "p_value": 0.0001},
        {"mutation": "PIK3CA", "median_survival_with_rapamycin_days": 179,
         "median_survival_without_rapamycin_days": 119, "p_value": 0.005},
    ],
    "negative_control": {
        "mutation": "NRAS", "drug": "trametinib (MEK inhibitor)",
        "median_survival_with_drug_days": 241, "median_survival_without_drug_days": 259,
        "p_value": 0.7775, "n_with_drug": 71, "n_without_drug": 26,
        "note": "Included deliberately, not omitted: a real negative result is why this module "
               "does not build an NRAS/MEK-inhibitor HSA scenario alongside this one.",
    },
    "caveat": "Retrospective real-world evidence, not a controlled trial -- dogs were not "
             "randomized to rapamycin, dosing was not standardized within this cohort, and "
             "survival reflects whatever other concurrent treatments each dog received. Provided "
             "for scale (does this module's own median_time_to_progression_days land in a "
             "remotely plausible range), not as validation of this module's specific numbers.",
}

# Two real published studies bracketing standard-of-care survival without any targeted drug --
# the same disagreeing-studies-provided-for-scale role LOMUSTINE_BENCHMARK plays for HS.
# Ogilvie et al. 1996's exact figure is cited via a 2026 review (MDPI Animals 16(5):778), not
# independently verified against the primary 1996 paper -- flagged rather than presented as
# directly checked, unlike every PMID cited above.
HSA_STANDARD_OF_CARE_BENCHMARK = {
    "studies": [
        {"citation": "Wendelburg et al. 2015, JAVMA 247(4):393-403, PMID 26225611",
         "design": "208 dogs with splenic HSA, splenectomy with or without adjuvant "
                  "chemotherapy (154 surgery alone; 54 surgery + chemotherapy)",
         "median_survival_surgery_alone_days": 48},  # 1.6 months
        {"citation": "Ogilvie et al. 1996, cited via Animals (MDPI) 2026;16(5):778 -- not "
                    "independently verified against the primary 1996 paper",
         "design": "surgery followed by doxorubicin-based chemotherapy",
         "median_survival_days_range": [120, 180]},  # ~4-6 months
    ],
    "caveat": "Provided for scale, not a like-for-like comparator: neither study's population is "
             "restricted to any specific driver mutation, and neither endpoint matches this "
             "module's RECIST-style progression-from-nadir definition.",
}


def dog_hsa_preset() -> tuple[ResistanceModel, float, np.ndarray, dict]:
    """PI3K/mTOR-inhibitor vs. canine PIK3CA/PTEN-mutant HSA; sensitive-clone IC50 anchored to
    real cell-line data (VDC-597); reference plasma concentration illustrative, not rapamycin's
    real trough concentration.

    A more severe version of the cellular-potency-vs-clinical-drug mismatch
    `mapk_scenarios.dog_preset` documents for cobimetinib/trametinib: there, both numbers came
    from the same drug's own real measurements (cobimetinib IC50 and cobimetinib Css), so pairing
    them was internally consistent. Here, no drug has both halves: VDC-597 has a real HSA-cell-line
    IC50 but no published canine dosing; rapamycin has real canine PK/PD (>10 ng/mL trough, ~10.9
    nM, at 0.06-0.08 mg/kg IM daily) and a real HSA survival benchmark, but no published
    HSA-cell-line potency of its own. Naively pairing VDC-597's real IC50 (mean 543 nM) with
    rapamycin's real ~10.9 nM trough would put achievable exposure roughly 50x *below* the
    sensitive clone's IC50 -- predicting the drug barely works at all, which would directly
    contradict the real, statistically significant FidoCure survival benefit this same module
    cites for rapamycin. Rather than publish that self-contradictory pairing, `css_reference`
    here is illustrative (5x the mean measured IC50, the same "assumed, not measured, margin"
    convention `mapk_cli.CDK46_ILLUSTRATIVE_CSS_NM` uses), and rapamycin's real PK/PD and survival
    numbers are kept as separate, real-world context -- used to sanity-check this scenario's
    *output* durability numbers, the same role `MAPK_INHIBITOR_HUMAN_BENCHMARK` plays for
    histiocytic sarcoma, not fed into the concentration-vs-IC50 kill-rate calculation itself.
    """
    cell_line_ic50_nM = {"CIN": 230.0, "SB": 690.0, "DEN": 710.0}
    ic50_sensitive = float(np.mean(list(cell_line_ic50_nM.values())))
    seeding_rates = _SEEDING_RATE_TOTAL * np.array([.5, .3, .2])
    model = ResistanceModel(growth=_SHARED_GROWTH, ic50_nM=ic50_sensitive * _SHARED_IC50_RATIOS,
                            max_kill=_SHARED_MAX_KILL, mutation=_SHARED_MUTATION)
    css_reference = 5.0 * ic50_sensitive  # illustrative margin, not rapamycin's real trough -- see docstring
    provenance = {
        "species": "dog", "drug": "PI3K/mTOR inhibitor (illustrative exposure; real clinical "
                                  "drug in this class is rapamycin/sirolimus)",
        "calibrated_from_data": {
            "sensitive_clone_ic50_nM": cell_line_ic50_nM,
        },
        "illustrative_only": ["css_reference (see docstring for why rapamycin's real trough "
                              "concentration is not used here)",
                              "growth rates", "resistant-clone IC50 shifts and kill ceilings",
                              "seeding rates (bare placeholders, not even loosely tuned against "
                              "a durable-response case report the way histiocytic sarcoma's are)",
                              "carrying capacity"],
        "citation": "Pyuen et al. 2018, PLOS ONE 13(7):e0200634, PMID 30011343 (cell-line IC50)",
        "real_world_context_not_fit_to_model": {
            "rapamycin_canine_pk": "Paoloni et al. 2010, PLOS ONE 5(6):e11013, PMID 20543980: "
                "trough concentration >10 ng/mL (~10.9 nM) at 0.06-0.08 mg/kg IM daily in dogs "
                "with cancer (osteosarcoma, not HSA), confirmed target inhibition, no MTD reached",
            "rapamycin_hsa_survival_benchmark": "see HSA_RAPAMYCIN_BENCHMARK",
        },
        "cellular_potency_vs_clinical_drug_mismatch": (
            "VDC-597 (the cellular-potency anchor) has no published canine dosing; rapamycin "
            "(the real, clinically relevant drug, with real canine PK/PD and a real HSA "
            "real-world survival benchmark) has no published HSA-cell-line potency number of its "
            "own. Both are PI3K/mTOR-pathway inhibitors but different molecules -- pairing their "
            "real numbers directly would be self-contradictory (see docstring), so this preset "
            "keeps css_reference illustrative instead."
        ),
    }
    return model, css_reference, seeding_rates, provenance
