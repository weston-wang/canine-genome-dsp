"""Durable response in canine hemangiosarcoma: the mechanism, the escape routes, and their closure.

The histiocytic-sarcoma (HS) work in this project asked a specific sequence of questions -- what
carries durability, what is the per-day bar a persistent mechanism must clear, is that bar
achievable against real trial data, which escape routes survive, and what closes each one. This
module asks the same sequence of HSA, reusing `hsa_scenarios`' own presets and real anchors rather
than introducing new ones. Every number below was computed from this repo's engine; the
provenance of each is named in place.

THE HEADLINE, STATED FIRST BECAUSE IT REVERSES THE MODULE'S OWN FRAMING
-----------------------------------------------------------------------
`hsa_scenarios` presents a PI3K/mTOR inhibitor as the backbone and the vaccine as a follow-on
layered on top. The margin arithmetic says the opposite: the drug is very nearly irrelevant to
durability, and the vaccine carries essentially all of it.

`clone_growth_margins` at the module's own preset, with no vaccine:

    exposure assumption            sensitive   pi3k_akt   mapk_cross   target_site   BAR
    assumed 5x IC50 (default)        -0.0919    +0.0490      +0.0230       +0.0515   0.0515
    de-rated to 40% (toxicity)       -0.0632    +0.0497      +0.0291       +0.0519   0.0519
    REAL rapamycin trough            +0.0545    +0.0500      +0.0499       +0.0520   0.0545
    NO DRUG AT ALL                   +0.0550    +0.0500      +0.0500       +0.0520   0.0550

The bar -- the largest growth margin a persistent mechanism has to out-kill -- is 0.0515/day with
the drug at full assumed exposure and 0.0550/day with no drug whatsoever. A 7% difference. The
inhibitor drives the SENSITIVE clone deeply negative (+0.055 -> -0.092) and moves the three
resistant clones by 1-2% between them, so it decides how fast the bulk tumour shrinks and almost
nothing about whether the disease comes back.

THE REAL DRUG, AT ITS REAL DOSE, DOES NOT CLEAR ITS OWN IC50
-------------------------------------------------------------
`dog_hsa_preset` sets `css_reference = 5.0 * ic50_sensitive`, an explicitly assumed margin. The
real clinically-used drug in this class is rapamycin, and its real measured canine exposure is a
median trough above 10 ng/mL (Paoloni et al. 2010, PMID 20543980) = 10.9 nM against VDC-597's real
543 nM mean cell-line IC50 (Pyuen et al. 2018, PMID 30011343) -- 50x BELOW IC50, which is the
mismatch `dog_hsa_preset`'s docstring already names and resolves by keeping exposure illustrative.

What the docstring does not say is the consequence, which the margin table above makes explicit:
at the real drug's real exposure the sensitive clone is not suppressed at all (+0.0545 vs +0.0550
untreated). The modelled inhibitor is not rapamycin at any achievable dose; it is a hypothetical
agent roughly 250x more potent. This is the HSA analogue of the HS pipeline's real-potency
correction, and it lands harder: there, real potency changed the durability projection's character;
here, it removes the backbone's contribution almost entirely.

Note the direction of the error. Because the drug was never carrying durability, over-stating its
exposure inflates the SPEED of the response, not the durability conclusion. The vaccine threshold
is nearly unchanged. That is why this is a scoping correction rather than a retraction.

ACHIEVABILITY: WHAT THE TWO REAL CANINE HSA VACCINE TRIALS IMPLY
-----------------------------------------------------------------
Unlike the HS module -- which has no vaccine trial in its disease at all and had to reason from a
human platform -- HSA has two real Phase 2 trials in the actual disease, and they can be used to
bound what `vaccine_max_kill` a real vaccine buys. 1-year survival, vaccinated vs control:

    ERstrePs  (Marconato et al. 2023, PMID 37686485, n=28 vs 32):  35.7%  vs  6.3%   (+29.4 pp)
    eVim      (Engbersen et al. 2025, PMID 41009669, n=23):        44%    vs  14%    (+30   pp)

Both real vaccines buy about +30 percentage points of 1-year survival. In the engine, 1-year
durable response as a function of `vaccine_max_kill` at `_PREEXISTING_PROB_CENTRAL = 0.70`:

    vaccine_max_kill   0.0     0.01    0.02    0.03    0.04    0.05    0.06
    1-yr durable       0.338   0.443   0.508   0.647   0.848   1.000   1.000

A +30 pp gain over the no-vaccine baseline lands at `vaccine_max_kill` ~= 0.03 (0.647 - 0.338 =
+30.9 pp). The bar is 0.0515-0.0550/day. **The two real vaccines imply roughly 0.03/day; the
durability bar is ~0.052/day. Real HSA vaccination is short by about 1.7x.**

That is the single most decision-relevant number in this module, and it is grounded in real trials
in the real disease rather than extrapolated -- which is why it is worth stating even though the
comparison is loose in two named ways (below).

TWO WAYS THIS ACHIEVABILITY COMPARISON IS LOOSE, NEITHER OF WHICH IS HIDDEN
---------------------------------------------------------------------------
1. ENDPOINT. The trials report overall SURVIVAL; the engine reports RECIST-style progression from
   nadir. These differ, and HSA is the disease where they differ most, because its signature
   complication -- splenic rupture and acute internal haemorrhage -- kills independently of
   whether a resistant clone is regrowing. `hsa_scenarios` already names this missing mechanism.
   The direction is knowable: survival <= progression-free, so matching the engine's durable
   response to a real SURVIVAL figure OVERSTATES the implied vaccine potency. The 0.03/day figure
   is therefore an upper bound, and the 1.7x shortfall a lower bound on the shortfall.
2. BASELINE. The engine's no-vaccine 1-year figure (0.338) is roughly five times the real control
   arms (6.3%, 14%). Matching the INCREMENT rather than the level is what makes the comparison
   usable at all, and it assumes the increment transfers across a baseline mismatch of that size.

WHY THE COMPARISON IS STILL WORTH MAKING: it is the same move `_PREEXISTING_PROB_CENTRAL` was
already recentered on (against eBAT's 1-year survival), applied to the parameter that actually
carries the result instead of the one that carries the baseline.

THE ESCAPE ROUTES, AND WHAT CLOSES EACH
-----------------------------------------
See `ESCAPE_ROUTES`. Summarised: three of the four modelled routes are closed by the vaccine
BY CONSTRUCTION rather than by potency -- none of `pi3k_akt_feedback_reactivation`,
`mapk_crosstalk_bypass`, or `target_site_mutation` requires shedding the antigen a real HSA
vaccine targets, exactly as `antigen_convergence` argues for HS. The fourth, antigen/MHC-I loss,
is the one the vaccine cannot see, and the model treats it as unclosable at any potency.

THAT TREATMENT IS WRONG FOR HSA, FOR THREE INDEPENDENT REASONS
----------------------------------------------------------------
The engine's 5th clone is defined as "antigen/MHC-I loss" -- inherited unchanged from the HS
module, where the vaccine is a hypothetical peptide/MHC-I mRNA construct against a driver hotspot.
Neither real HSA vaccine works that way, and `hsa_scenarios` itself establishes the first reason
while modelling as though it did not:

1. eVim RAISES ANTIBODIES, NOT MHC-RESTRICTED T-CELLS. It is a conjugate vaccine against
   EXTRACELLULAR vimentin (Engbersen 2025). `hsa_scenarios` lines 500-513 get this exactly right
   -- it is why the module correctly refuses to run NetMHCpan against eVim's antigen, calling that
   a category error. But the escape clone it then simulates is MHC-I loss, which an antibody
   response does not use and therefore cannot be evaded by. eVim's real escape route is loss of
   SURFACE VIMENTIN, a structural cytoskeletal protein, which is a different and plausibly much
   costlier event. The module makes the right call in one place and the wrong one in another.
2. ERstrePs RAISES BOTH. Marconato 2023 reports "a tumor-specific humoral response along with a
   vaccine-specific T-cell response." Only the T-cell half is MHC-restricted, so MHC-I loss
   degrades that vaccine rather than evading it.
3. MHC-I LOSS UPREGULATES THE BACKUP TARGET. Lerner et al., Nat Cancer 2023;4(9):1258-1272 (PMID
   37537301) show primed CD8 T-cells still kill MHC-I-null tumour cells through NKG2D engaging
   stress ligands, which are HIGHLY EXPRESSED ON MHC-LOSS VARIANTS specifically; killing was
   completely abrogated by anti-NKG2D blockade. The event that creates the blind spot creates the
   backup target, and prior antigen-specific priming licenses it -- so this is a property of the
   vaccine-primed population, not an extra agent. (This mechanism was identified by the HS work in
   this project; it transfers to HSA's T-cell-inducing vaccine unchanged.)

Setting the escape clone's vaccine coverage to exactly 0.0 is therefore PESSIMISTIC for HSA, not
neutral -- the same conclusion the HS pipeline reached, arrived at here by a different and, for
eVim, stronger route.

AND THE SIMULATION AGREES IT IS A MINOR ROUTE EVEN AT COVERAGE 0.0
-------------------------------------------------------------------
At and above the bar, with the escape clone entirely uncovered (10-year horizon, 300 trials):

    vaccine_max_kill 0.05 -> 0.920 durable, 24 relapses, only 1 of them antigen-loss
    vaccine_max_kill 0.06 -> 1.000 durable, 0 relapses
    vaccine_max_kill 0.08 -> 1.000 durable, 0 relapses

and raising the unmeasured `HSA_IMMUNE_ESCAPE_SEEDING_RATE` by 10x/100x/1000x at potency 0.06
gives 1.000 / 0.990 / 0.963. Above the bar the antigen-positive population collapses before it can
supply the mutation, so the route starves rather than being out-killed. Below the bar (0.05), 23
of 24 relapses are ordinary drug-resistance clones clearing the margin -- the bar, not antigen
loss, is what is binding.

CLOSING THE ROUTE ANYWAY: WHAT IT TAKES
-----------------------------------------
Forcing the worst case (escape rate x1000, potency 0.06) and adding a PERSISTENT
mechanism-agnostic kill term -- what eBAT already is, minus its 28-day cap:

    persistent agnostic kill   0.0     0.02    0.05    0.08
    10-yr durable              0.963   0.983   1.000   1.000

0.05/day closes it completely, against an escape-clone margin of +0.0415/day. The mechanism does
not have to be new: eBAT is already modelled as mechanism-agnostic (a scalar `max_kill_2` applied
to every clone including the escape clone), because it targets EGFR and uPAR -- cell-surface
receptors, not MHC-presented peptides. What eBAT lacks is not coverage but PERSISTENCE:
`HSA_EBAT_EXPOSURE_DURATION_DAYS = 28`, and ~30% of dogs develop neutralising anti-toxin antibodies
despite deimmunisation (Borgatti et al. 2017, PMID 28193671), which is a real ceiling on re-dosing.

Note what eVim does that eBAT cannot: its real protocol includes MAINTENANCE VACCINATIONS EVERY
TWO MONTHS (Engbersen 2025). A re-dosed antibody-inducing vaccine against a surface antigen is
simultaneously persistent AND antigen-independent in the MHC sense -- the only mechanism in this
module's inventory that is both.

SURGERY BUYS TIME, NOT DURABILITY (AND A HYPOTHESIS THAT FAILED)
------------------------------------------------------------------
Every trial this module calibrates against is POST-SPLENECTOMY adjuvant therapy on minimal
residual disease. The HSA scenarios never model that: they use `run_monte_carlo`'s default
`initial_burden=0.3` with no `debulking_fraction`, unlike the HS module, which applies
`DEBULKING_FRACTION = 0.97` for its resectable presentations.

The obvious hypothesis -- that `_PREEXISTING_PROB_CENTRAL`'s 0.30 -> 0.70 recentering was
compensating for the missing resection -- was tested and is FALSE. Modelling splenectomy makes
durable response HIGHER, moving further from the eBAT benchmark the recentering was argued on:

    preexisting_prob      1-yr, no resection    1-yr, post-splenectomy
    0.30                       0.665                  0.750
    0.70                       0.385                  0.500
    ---                   2-yr, no resection    2-yr, post-splenectomy
    0.30                       0.635                  0.672
    0.70                       0.305                  0.320

So the recentering is if anything UNDER-corrected, and the module's own preferred explanation --
a real, unmodelled rupture/haemorrhage death pathway -- survives this test. The independently
useful result is the second table: resection moves the 1-year figure by 8-11 points and the 2-year
figure by 1.5-4 points, because `initial_burden` changes where a clone starts and not the sign of
its growth margin. In this model surgery is a delay mechanism. That matches the real disease, where
splenectomy alone gives a median survival of 1.6 months (Wendelburg et al. 2015, PMID 26225611).
"""

import numpy as np

# The bar, by drug-exposure assumption. Computed via mapk_resistance.clone_growth_margins against
# hsa_scenarios.dog_hsa_preset; reproduced by test_hsa_durable_response_analysis.
DURABILITY_BAR_PER_DAY = {
    "assumed_5x_ic50_module_default": 0.0515,
    "derated_to_40pct_for_toxicity": 0.0519,
    "real_rapamycin_trough_10_9nM": 0.0545,
    "no_drug_at_all": 0.0550,
    "set_by_clone": "target_site_mutation under drug; sensitive once drug pressure is removed",
    "interpretation": "A 7% spread between full assumed drug exposure and no drug at all. The "
                     "inhibitor decides how fast the bulk tumour shrinks, not whether it returns.",
}

RAPAMYCIN_REAL_EXPOSURE = {
    "citation": "Paoloni et al. 2010, PLOS ONE 5(6):e11013, PMID 20543980",
    "measured": "median trough > 10 ng/mL at 0.06-0.08 mg/kg IM daily in dogs with cancer, no MTD "
               "reached, target inhibition confirmed (>2-fold tumoral phospho-S6RP reduction, 8/10)",
    "molecular_weight_g_per_mol": 914.17,
    "trough_nM": 10.94,
    "vdc597_ic50_nM": 543.33,
    "fold_below_ic50": 49.7,
    "consequence": "At real exposure the sensitive clone's margin is +0.0545/day versus +0.0550/day "
                  "untreated -- the real drug at its real dose does essentially nothing in this "
                  "model. The modelled inhibitor is a hypothetical agent ~250x more potent than "
                  "rapamycin, not rapamycin.",
    "why_this_is_scoping_not_retraction": "The drug was never carrying durability, so over-stating "
                                         "its exposure inflates response SPEED, not the vaccine "
                                         "threshold. The bar moves 0.0515 -> 0.0545.",
}

VACCINE_ACHIEVABILITY = {
    "real_trials": [
        {"name": "ERstrePs", "citation": "Marconato et al. 2023, Cancers 15(17):4209, PMID 37686485",
         "n_vaccinated": 28, "n_control": 32, "one_year_survival": 0.357,
         "one_year_survival_control": 0.063, "gain_pp": 29.4,
         "mechanism": "peptide-based; humoral AND vaccine-specific T-cell response both reported"},
        {"name": "eVim", "citation": "Engbersen et al. 2025, Int J Mol Sci 26(18):9096, PMID 41009669",
         "n_vaccinated": 23, "one_year_survival": 0.44, "one_year_survival_control": 0.14,
         "gain_pp": 30.0,
         "mechanism": "iBoost conjugate vaccine against EXTRACELLULAR vimentin; antibody-mediated; "
                     "maintenance vaccinations every two months"},
    ],
    "engine_one_year_durable_by_potency": {0.0: 0.338, 0.01: 0.443, 0.02: 0.508, 0.03: 0.647,
                                           0.04: 0.848, 0.05: 1.000, 0.06: 1.000},
    "implied_vaccine_max_kill": 0.03,
    "bar_to_clear": 0.0515,
    "verdict": "Real canine HSA vaccination implies roughly 0.03/day. The durability bar is "
              "~0.052/day. Short by about 1.7x -- and because the trials report SURVIVAL while the "
              "engine reports progression-free, 0.03/day is an upper bound and 1.7x a lower bound "
              "on the shortfall.",
}

ESCAPE_ROUTES = [
    {
        "id": 1,
        "name": "pi3k_akt_feedback_reactivation",
        "status": "CLOSED by construction, not by potency",
        "detail": "Loss of mTORC1-mediated negative feedback reactivating upstream PI3K/AKT. The "
                 "clone adds a signalling lesion; it does not stop expressing vimentin, ER-stress "
                 "peptides, or whole-tumour antigen. A real HSA vaccine still sees it. Same "
                 "antigen-convergence argument `antigen_convergence` makes for HS, and stronger "
                 "here because real HSA vaccines target genotype-agnostic antigens rather than a "
                 "driver mutation that a resistance lesion might co-select against.",
    },
    {
        "id": 2,
        "name": "mapk_crosstalk_bypass",
        "status": "CLOSED by construction, not by potency",
        "detail": "Parallel MAPK/ERK activation routing around mTORC1. Same reasoning as route 1. "
                 "Note this clone is also the one the drug suppresses best in relative terms "
                 "(margin +0.0230 vs +0.0500 untreated), so it is the least dangerous of the three.",
    },
    {
        "id": 3,
        "name": "target_site_mutation",
        "status": "CLOSED by construction -- AND IT SETS THE BAR",
        "detail": "FKBP12-mTOR binding-site alteration. Antigen retained, so the vaccine covers it; "
                 "but its margin (+0.0515/day under full assumed drug) is the largest of any "
                 "antigen-positive clone, so it is what any persistent mechanism must out-kill. "
                 "Below the bar it is what actually relapses: at vaccine_max_kill 0.05, 23 of 24 "
                 "ten-year relapses are ordinary drug-resistance clones, not antigen loss.",
    },
    {
        "id": 4,
        "name": "antigen / MHC-I loss (the modelled immune_escape clone)",
        "status": "MODELLED AS UNCLOSABLE; that is wrong for HSA, and it is minor in simulation too",
        "detail": "Coverage hard-coded to exactly 0.0, inherited from the HS module's peptide/MHC-I "
                 "vaccine. Three independent reasons it does not transfer: (i) eVim is an "
                 "ANTIBODY response against extracellular vimentin, which does not use MHC-I at all "
                 "-- `hsa_scenarios` establishes this itself when refusing to run NetMHCpan on it, "
                 "then models MHC-I loss anyway; (ii) ERstrePs raises humoral AND T-cell responses, "
                 "so MHC-I loss degrades rather than evades it; (iii) MHC-loss variants "
                 "upregulate NKG2D ligands and primed CD8 T-cells kill them through NKG2D "
                 "(Lerner et al. 2023, PMID 37537301). Simulation agrees it is minor: at potency "
                 "0.06 it never fires even at 10x its assumed rate, and costs 1.0-3.7 points at "
                 "100x-1000x.",
        "how_to_close_it_anyway": "A PERSISTENT mechanism-agnostic kill term at >= 0.05/day closes "
                                 "it completely even at 1000x the assumed seeding rate (escape-clone "
                                 "margin +0.0415/day). eBAT already has the right coverage (EGFR/uPAR "
                                 "are surface receptors, modelled as a scalar applied to every clone) "
                                 "and the wrong duration (28 days, plus ~30% neutralising-antibody "
                                 "development). eVim's real two-monthly maintenance schedule is the "
                                 "only mechanism here that is persistent AND MHC-independent at once.",
    },
    {
        "id": 5,
        "name": "Splenic rupture / acute internal haemorrhage",
        "status": "OPEN, NOT MODELLED AT ALL, and the module says so",
        "detail": "HSA's signature complication: death independent of whether a resistant clone is "
                 "regrowing. No parameter fixes a missing mechanism, and no real rate exists to "
                 "calibrate one to. This is the module's own preferred explanation for why its "
                 "durable-response figures sit well above real survival, and the splenectomy test "
                 "above supports it: modelling resection moves durable response the WRONG WAY "
                 "relative to the benchmark, so the gap is not a burden-accounting error.",
    },
    {
        "id": 6,
        "name": "Vaccine failure without antigen loss",
        "status": "OPEN, NOT MODELLED",
        "detail": "T-cell exhaustion, immunosuppressive microenvironment, failure to prime at all, "
                 "or -- for eVim specifically -- an antibody titre that never reaches a functional "
                 "threshold. The engine's vaccine is a kill rate that always arrives on schedule "
                 "once `vaccine_start_day` passes. Every mechanism that makes a real vaccine simply "
                 "not work is outside the state vector. Directly relevant here: the xenogeneic "
                 "VEGFR-2 DNA vaccine `hsa_scenarios` cites raised reliable anti-VEGFR-2 antibodies "
                 "in healthy dogs and produced NO increase in cytotoxic response against a canine "
                 "HSA line -- a real, in-disease instance of exactly this route firing.",
    },
    {
        "id": 7,
        "name": "Micrometastatic disease outside any modelled compartment",
        "status": "OPEN, NOT MODELLED -- and this is the asymmetry with HS",
        "detail": "The HS pipeline built `run_monte_carlo_two_compartment` for localized pulmonary "
                 "Corgi HS specifically because regional nodal disease may already have spread "
                 "before surgery. HSA never calls it -- every HSA demo is single-compartment -- "
                 "even though splenic HSA is the paradigm case of a tumour that has already "
                 "disseminated at diagnosis (splenectomy alone: median 48 days, Wendelburg 2015). "
                 "The less-disseminated disease got the two-compartment treatment; the "
                 "more-disseminated one did not.",
    },
]

MECHANISM_LEDGER = {
    "what_durability_actually_requires": "A kill term that is (a) PERSISTENT -- no cumulative-dose "
                                        "cap, no fixed exposure window -- and (b) covers every "
                                        "clone that can arise, at >= the bar of ~0.052/day.",
    "candidates": [
        {"mechanism": "PI3K/mTOR inhibitor (rapamycin / VDC-597)",
         "persistent": True, "covers_all_clones": False, "clears_the_bar": False,
         "verdict": "Backbone for response SPEED. Moves the bar by 7%. At real rapamycin exposure "
                   "it does not suppress even the sensitive clone."},
        {"mechanism": "eBAT (EGF/uPAR bispecific immunotoxin)",
         "persistent": False, "covers_all_clones": True, "clears_the_bar": "at >=0.05/day, while dosed",
         "verdict": "Right coverage, wrong duration. 28-day window; ~30% of dogs develop "
                   "neutralising antibodies. Alone it gives 0% durable response at every potency "
                   "and every horizon -- which is arithmetic, not a finding: once its window closes "
                   "nothing applies any kill term and every clone margin is positive."},
        {"mechanism": "Cancer vaccine (ERstrePs / eVim class)",
         "persistent": True, "covers_all_clones": "all but the modelled MHC-I-loss clone",
         "clears_the_bar": "not at real-trial-implied potency (~0.03 vs ~0.052)",
         "verdict": "The only mechanism carrying durability, and the only one whose real-world "
                   "potency can be bounded from trials in this disease. Short by ~1.7x."},
        {"mechanism": "NKG2D killing by vaccine-primed CD8 T-cells",
         "persistent": "inherits the vaccine's persistence", "covers_all_clones": True,
         "clears_the_bar": "unquantified -- magnitude never measured",
         "verdict": "Closes route 4 at no added agent, because it is a property of the primed "
                   "population rather than a separate therapy. Requires the T-cell arm, so it "
                   "applies to ERstrePs and not to eVim -- which does not need it."},
        {"mechanism": "Splenectomy",
         "persistent": False, "covers_all_clones": True, "clears_the_bar": False,
         "verdict": "Delay, not durability. Moves 1-year durable response by 8-11 points and "
                   "2-year by 1.5-4, because it changes where clones start and not the sign of "
                   "their growth margins."},
    ],
    "the_gap_that_matters": "Nothing in this inventory is both persistent and demonstrated to clear "
                           "0.052/day in a dog. The nearest thing is a re-dosed antibody-inducing "
                           "vaccine against a surface antigen -- eVim's real design -- which is "
                           "persistent by protocol and MHC-independent by mechanism, and which "
                           "real data puts at roughly 0.03/day.",
}

WHAT_WOULD_CHANGE_THE_ANSWER = [
    "Measure a canine HSA vaccine's kill rate directly rather than inferring it from survival: "
    "serial imaging or ctDNA on a vaccinated cohort gives a progression-free readout the engine "
    "consumes natively, removing the survival-vs-progression mismatch that makes the 1.7x "
    "shortfall a lower bound rather than an estimate.",
    "Re-run every HSA time-course at real rapamycin exposure (10.9 nM), the way the HS pipeline "
    "re-ran branch D. The bar barely moves, so the durability conclusions should survive -- but "
    "'should survive' is a prediction, and the HS pipeline's equivalent prediction was wrong.",
    "Replace the inherited MHC-I-loss escape clone with a mechanism matched to the actual vaccine: "
    "surface-vimentin loss for eVim, which needs a fitness cost of its own, since vimentin is "
    "structural rather than a passenger antigen.",
    "Model the second compartment. Splenic HSA is disseminated at diagnosis more often than the "
    "Corgi pulmonary presentation that already has a two-compartment model.",
    "Give the module a rupture/haemorrhage hazard once any real rate exists. Until then every "
    "durable-response figure here is conditional on the dog not dying of the thing this disease "
    "is most likely to kill it with.",
]
