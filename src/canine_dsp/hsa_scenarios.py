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

Cancer-vaccine work in canine HSA turns out to be more extensive than a first pass found, and
checking it directly (not trusting a search summary) corrected a real mistake in an earlier draft
of this module, which had misattributed one trial's numbers to a different, unrelated vaccine
under the wrong name. There are at least four real, distinct programs, none of which targets a
specific driver-mutation neoantigen the way the histiocytic-sarcoma module's mRNA-vaccine
hypothesis does -- a real, deliberate design choice by vaccine developers that independently
confirms this module's own earlier scoping decision: HSA has no single shared hotspot to build a
mutation-specific vaccine around the way HS's PTPN11/KRAS does, so real HSA vaccine programs
target broader, genotype-agnostic tumor antigens instead.

- **ERstrePs** (endoplasmic-reticulum-stress-related peptides released from Salmonella-infected
  HSA cells): the strongest real result found. Marconato et al. 2023, Cancers (Basel) 15(17):4402,
  PMID 37686485 -- Phase 2, single-arm, 28 vaccinated dogs (post-splenectomy, adjuvant to standard
  chemotherapy) vs. 32 historical controls. Median overall survival 276 vs. 175 days (p=0.002);
  1-year survival 35.7% vs. 6.3%.
- **eVim** (extracellular vimentin, delivered via "iBoost" conjugate technology): a second, later,
  independent real trial. Engbersen et al. 2025, Int J Mol Sci, PMID 41009669 -- Phase 2,
  single-arm, 23 vaccinated dogs vs. 22 historical controls (Stage I+II). Median overall survival
  235 vs. 136 days -- *not* statistically significant on its own; but 1-year survival 44% vs. 14%
  (p=0.0344) and a restricted-mean-survival-time advantage of 81 days at one year (p=0.02) both
  were. Read alongside ERstrePs, not in place of it: two different real vaccines, two different
  significance profiles, on overlapping but not identical patient populations.
- **Autologous whole-cell vaccine** (mechanically dissociated, chemically inactivated tumor cells
  plus a small-intestine-submucosa-derived adjuvant): real but far weaker evidence. Lucroy et al.
  2020, BMC Vet Res 16:447, PMID 33208160 -- a small (n=8), uncontrolled, Stage III (metastatic)
  cohort; median survival 142 days against a historical 41-day surgery-alone reference, no
  concurrent control arm.
- **Xenogeneic VEGFR-2 DNA vaccine**: a real, informative negative signal, included for the same
  reason the NRAS/trametinib negative result is included above -- not omitted because it's
  inconvenient. Real immunogenicity/safety study in *healthy* dogs (not an HSA efficacy trial):
  vaccination reliably raised anti-VEGFR-2 antibodies, but co-incubating vaccinated dogs' PBMCs
  with a real canine HSA cell line showed *no increase* in cytotoxic response after the final
  vaccination (Oncotarget, DOI 10.18632/oncotarget.7265, PMC4905448, 2016). Antibody response
  did not translate to the specific cell-killing readout that would predict tumor efficacy.
- **Calviri frameshift-peptide vaccine**: a real, currently enrolling therapeutic trial (adjuvant,
  post-splenectomy, same design pattern as ERstrePs/eVim) across three US veterinary schools
  (Wisconsin, Colorado State, UC Davis) as of late 2024, targeting "frame-shift peptides" --
  neoantigens shared across patients and tumor types, arising from RNA processing errors rather
  than point mutations. No results published yet -- the same "real trial running, no readout yet"
  situation as the canine trametinib-for-histiocytic-sarcoma trial.

`hsa_vaccine_followon_scenarios`/`hsa_cli.hsa_vaccine_followon_demo` layer a vaccine kill term on
top of the PI3K/mTOR resistance model above, reusing `mapk_resistance.run_monte_carlo_with_vaccine`
unchanged. The antigen-persistence argument is, if anything, more secure here than in the
histiocytic-sarcoma module, precisely because real HSA vaccines don't target a driver mutation:
none of this module's three modeled resistance mechanisms (all *drug*-resistance routes, evading
rapamycin/VDC-597 specifically) has any documented reason to alter vimentin expression, ER-stress
signaling, or whole-tumor antigen presentation, so a vaccine built around any of those real targets
should keep recognizing cells using any of the three routes. Only genuine antigen/MHC-I loss --
modeled, as in the histiocytic-sarcoma module, as a 5th clone -- would evade it.
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


# Real, distinct HSA cancer-vaccine programs -- see module docstring for what's real, what's
# strong vs. weak evidence, and why none targets a driver-mutation neoantigen the way the
# histiocytic-sarcoma module's vaccine hypothesis does.
HSA_VACCINE_TRIALS = {
    "erstreps": {
        "citation": "Marconato et al. 2023, Cancers (Basel) 15(17):4402, PMID 37686485",
        "antigen": "endoplasmic-reticulum-stress-related peptides (ERstrePs) from "
                  "Salmonella-infected HSA cells -- not a driver-mutation neoantigen",
        "design": "Phase 2 single-arm; 28 vaccinated dogs (post-splenectomy, adjuvant to "
                 "standard chemotherapy) vs. 32 historical controls",
        "median_survival_vaccinated_days": 276, "median_survival_control_days": 175,
        "p_value_overall_survival": 0.002,
        "one_year_survival_vaccinated": 0.357, "one_year_survival_control": 0.063,
        "strength": "strongest real result of the four -- significant on median OS itself, "
                   "not only on a secondary endpoint",
    },
    "evim": {
        "citation": "Engbersen et al. 2025, Int J Mol Sci, PMID 41009669",
        "antigen": "extracellular vimentin (eVim), iBoost conjugate technology -- a "
                  "mesenchymal/tumor-vasculature marker, not a driver-mutation neoantigen",
        "design": "Phase 2 single-arm; 23 vaccinated dogs vs. 22 historical controls, Stage I+II",
        "median_survival_vaccinated_days": 235, "median_survival_control_days": 136,
        "p_value_overall_survival": None,  # not statistically significant on its own
        "one_year_survival_vaccinated": 0.44, "one_year_survival_control": 0.14,
        "p_value_one_year_survival": 0.0344,
        "restricted_mean_survival_advantage_at_1yr_days": 81, "p_value_rmst": 0.02,
        "strength": "real and significant on 1-year survival/RMST, but median OS itself did "
                   "not reach significance -- weaker than ERstrePs on that specific endpoint",
    },
    "autologous_whole_cell": {
        "citation": "Lucroy et al. 2020, BMC Vet Res 16:447, PMID 33208160",
        "antigen": "whole, chemically-inactivated autologous tumor cells -- non-genotype-specific",
        "design": "small (n=8), uncontrolled, Stage III (metastatic) HSA; compared only to a "
                 "historical 41-day surgery-alone reference, no concurrent control arm",
        "median_survival_vaccinated_days": 142,
        "strength": "weakest real evidence of the four -- real but small, uncontrolled, and in "
                   "a more advanced (metastatic) population than the other three",
    },
    "vegfr2_dna_negative_control": {
        "citation": "Oncotarget, DOI 10.18632/oncotarget.7265, PMC4905448, 2016",
        "antigen": "xenogeneic human VEGFR-2 DNA vaccine",
        "design": "immunogenicity/safety study in healthy dogs, not an HSA efficacy trial",
        "finding": "reliably raised anti-VEGFR-2 antibodies, but produced no increase in "
                  "cytotoxic response against a real canine HSA cell line after vaccination",
        "note": "included deliberately, not omitted: a real negative signal on the specific "
               "readout (does this actually help kill HSA cells) that would predict efficacy",
    },
    "calviri_frameshift_peptide": {
        "status": "real, currently enrolling therapeutic trial (adjuvant, post-splenectomy) "
                 "across University of Wisconsin, Colorado State University, and UC Davis as "
                 "of late 2024; no results published yet",
        "antigen": "frame-shift peptides -- neoantigens shared across patients and tumor types, "
                  "arising from RNA processing errors rather than point mutations",
    },
}

# Illustrative, not measured: no canine cancer vaccine trial reports the kind of granular timing
# data (start day relative to when immune response develops, ramp kinetics) this module's engine
# needs -- the same situation the histiocytic-sarcoma module's own vaccine constants are in.
HSA_VACCINE_CLONE_NAMES = HSA_CLONE_NAMES + ["immune_escape"]
HSA_VACCINE_START_DAY = 30   # illustrative: all four real trials vaccinate starting shortly
                             # after splenectomy, alongside chemotherapy, not after a drug-only lead-in
HSA_VACCINE_RAMP_DAYS = 21
HSA_VACCINE_MAX_KILL_SWEEP = [0.0, 0.01, 0.03, 0.05, 0.08]

# Illustrative fitness cost of antigen/MHC-I loss, and its seeding rate an order of magnitude
# below the rarest existing drug-resistance mechanism -- the same conventions, and the same
# "not measured for this or any hemangiosarcoma" caveat, as the histiocytic-sarcoma module's
# IMMUNE_ESCAPE_GROWTH_PENALTY/IMMUNE_ESCAPE_SEEDING_RATE.
HSA_IMMUNE_ESCAPE_GROWTH_PENALTY = 0.85
HSA_IMMUNE_ESCAPE_SEEDING_RATE = _SEEDING_RATE_TOTAL * 0.2 * 0.1

# eBAT: a real, mechanistically distinct third option -- a bispecific EGF/uPAR-targeted
# immunotoxin, not a small-molecule pathway inhibitor -- with real Phase I/II dose-finding data
# (Kim et al. 2017, Mol Cancer Ther 16(9):1996-2006, PMID 28193671): a single IV cycle at 50
# ug/kg (the biologically active dose identified across an adaptive 23-dog dose-finding cohort),
# 6-month survival ~70% (n=17 at that dose) vs. <40% in historical controls, with 6 long-term
# survivors past 450 days. Unlike VDC-597/rapamycin, no multi-dose-level response curve was
# reported -- a single active dose, not a titratable Emax relationship -- so there is no real
# number to anchor an IC50/kill-rate to the way VDC-597's cell-line IC50 anchors the sensitive
# clone above. ebat_max_kill is swept across an illustrative range for that reason, the same
# discipline `mapk_scenarios.CDK46_MAX_KILL_SWEEP` uses for histiocytic sarcoma's own real-but-
# unquantified second agent. EGFR and uPAR are both broadly expressed on tumor vasculature and
# are not documented targets of any of this scenario's three modeled drug-resistance mechanisms
# (all of which evade rapamycin/VDC-597's pathway inhibition specifically, not receptor
# expression), so eBAT is modeled the same "mechanism-agnostic, applies to every non-escape
# clone identically" way CDK4/6i is modeled for histiocytic sarcoma.
HSA_EBAT_TRIAL = {
    "citation": "Kim et al. 2017, Mol Cancer Ther 16(9):1996-2006, PMID 28193671",
    "agent": "eBAT (bispecific EGF/uPAR-targeted immunotoxin)",
    "design": "adaptive Phase I/II dose-finding, 23 dogs with splenic HSA; single IV cycle",
    "biologically_active_dose_ug_per_kg": 50.0,
    "n_at_active_dose": 17,
    "six_month_survival_at_active_dose": 0.70, "six_month_survival_historical_control": "<0.40",
    "long_term_survivors_past_450_days": 6,
    "caveat": "A single active dose was identified, not a multi-level dose-response curve -- "
             "unlike VDC-597, there is no real IC50/kill-rate number to anchor to, so this "
             "scenario's ebat_max_kill remains a swept illustrative range, not a fitted value.",
}
HSA_EBAT_ILLUSTRATIVE_IC50_NM = 100.0
HSA_EBAT_ILLUSTRATIVE_CSS_NM = 500.0  # ~5x the illustrative IC50; an assumed, not measured, margin
HSA_EBAT_MAX_KILL_SWEEP = [0.0, 0.02, 0.05, 0.08, 0.12]


def hsa_combination_scenarios(inhibitor_active: bool = True,
                              ebat_max_kill_values: list[float] = HSA_EBAT_MAX_KILL_SWEEP,
                              ) -> dict[float, tuple[ResistanceModel, float, np.ndarray, dict]]:
    """PI3K/mTOR inhibitor (`dog_hsa_preset`) +/- a swept-potency, mechanism-agnostic eBAT term,
    mirroring `mapk_scenarios.combination_scenarios`'s structure. `inhibitor_active=False` zeroes
    the inhibitor's reference concentration, isolating eBAT as monotherapy -- see module docstring
    for why eBAT is modeled as a mechanism-agnostic second node rather than a vaccine-style
    time-gated kill term.
    """
    model, css, seeding_rates, provenance = dog_hsa_preset()
    if not inhibitor_active:
        css = 0.0
    scenarios = {}
    for ebat_max_kill in ebat_max_kill_values:
        if ebat_max_kill > 0:
            combo_model = ResistanceModel(growth=model.growth, ic50_nM=model.ic50_nM,
                                          max_kill=model.max_kill, mutation=model.mutation,
                                          hill=model.hill, carrying_capacity=model.carrying_capacity,
                                          ic50_nM_2=HSA_EBAT_ILLUSTRATIVE_IC50_NM, max_kill_2=ebat_max_kill)
        else:
            combo_model = model
        scenarios[ebat_max_kill] = (combo_model, css, seeding_rates,
                                    {**provenance, "ebat_max_kill": ebat_max_kill,
                                     "inhibitor_active": inhibitor_active})
    return scenarios


def hsa_vaccine_followon_scenarios(ebat_max_kill: float = 0.0,
                                   vaccine_max_kill_values: list[float] = HSA_VACCINE_MAX_KILL_SWEEP,
                                   ) -> dict[float, tuple[ResistanceModel, float, np.ndarray, dict]]:
    """PI3K/mTOR inhibitor + eBAT (fixed at `ebat_max_kill`) plus a swept-potency cancer vaccine
    layered on top, mirroring `mapk_scenarios.vaccine_followon_scenarios`'s structure exactly
    (same 5th-clone antigen/MHC-I-loss mechanic, reusing `mapk_resistance.run_monte_carlo_with_vaccine`
    unchanged) but built for a genotype-agnostic real vaccine antigen rather than a
    driver-mutation-specific one -- see module docstring for why that makes the
    antigen-persistence argument, if anything, more secure here. `ebat_max_kill=0.0` (the
    default) gives an inhibitor-plus-vaccine-only baseline with no eBAT contribution.
    """
    combo_scenarios = hsa_combination_scenarios(ebat_max_kill_values=[ebat_max_kill])
    model, css, seeding_rates, provenance = combo_scenarios[ebat_max_kill]
    escape_growth = model.growth[1] * HSA_IMMUNE_ESCAPE_GROWTH_PENALTY
    model5 = ResistanceModel(
        growth=np.append(model.growth, escape_growth),
        ic50_nM=np.append(model.ic50_nM, model.ic50_nM[1]),
        max_kill=np.append(model.max_kill, model.max_kill[1]),
        mutation=np.eye(len(model.growth) + 1),
        hill=model.hill, carrying_capacity=model.carrying_capacity,
        ic50_nM_2=model.ic50_nM_2, max_kill_2=model.max_kill_2, hill_2=model.hill_2,
    )
    scenarios = {}
    for vaccine_max_kill in vaccine_max_kill_values:
        scenarios[vaccine_max_kill] = (model5, css, seeding_rates, {
            **provenance, "vaccine_max_kill": vaccine_max_kill,
            "vaccine_start_day": HSA_VACCINE_START_DAY, "vaccine_ramp_days": HSA_VACCINE_RAMP_DAYS,
            "immune_escape_seeding_rate": HSA_IMMUNE_ESCAPE_SEEDING_RATE,
            "immune_escape_growth_penalty": HSA_IMMUNE_ESCAPE_GROWTH_PENALTY,
        })
    return scenarios
