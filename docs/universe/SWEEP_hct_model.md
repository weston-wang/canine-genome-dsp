# Transplant (HCT) as a scientifically sound model input: canine multicentric lymphoma

STATUS: COMPLETE (sections 1-10). Arithmetic: scratchpad/poisson.py (cure-model numbers; run it to reproduce section 2).
Sources: PubMed MCP (metadata fetched this session for every PMID listed; "FT" = PMC full text read; "abs" = abstract only). Web items labelled WEB. Nothing cited from memory. Per CLAUDE.md rule 1 the existing record (docs/universe/SWEEP_stemcell.md, SWEEP_cnsregimens.md, LYMPHOMA_STATUS.md) was read first; items already there are marked "already in record".

User's bar, verbatim: "make sure every mechanism and every escape is closed by either real data or rigorous model, potency, toxicity etc all need to be considered"; "looking for 10+ years of durability"; "assuming early detection"; "I'm okay with no specific data but if scientifically sound" (transfer allowed if justified in writing, graded TRANSFER; no-basis = ASSUMED). Latest: "I needed scientifically sound, not totally theoretical. And I think you are dismissing vaccines, ebats, inhibitors, stem cells too easily." Graded against exactly this; "not demonstrated in dogs" is not a finding.

## 1. Canine transplant data re-extracted (numbers needed for an outcome-calibrated kill)

### 1.1 Allogeneic DLA-identical HCT, PMID 35789057 (Gareau et al., Vet Comp Oncol 2022; doi 10.1111/vco.12847; PMC9796125, FT)
Every number below is from the full text; section named in brackets.

| Item | Value (verbatim source) |
|---|---|
| Dogs, phenotype | 15 dogs, "high-grade B-cell lymphoma", 2006-2018, 4 facilities: NCSU + 3 private specialty hospitals (Bellingham Veterinary, VCA West LA, MedVet Columbus) [2.1] |
| Stage at diagnosis | Stage I 2, III 6, IV 3, V 4; substage a 11, b 4; PARR+ 12 [Table 2] |
| Remission status at transplant | "Five dogs relapsed before the procedure: three dogs once, one dog twice, and one dog 3 times. Four of the relapsed dogs were not in remission when transplanted." Remission before alloHCT 11. 10 dogs "had not relapsed" (first remission). [4.1, 5.2] |
| Induction | multiagent chemotherapy "such as CHOP" at referring vet discretion, to remission before transplant [2.1]. Mean diagnosis-to-transplant 118 d (29-379) |
| Conditioning | TBI "two 4 Gy fractions at a dose rate of 7.5-10 cGy/min", 6 MV photons; TBI = day 0 [2.5]. Cyclosporine 5-10 mg/kg from day -1 to ~day +30 [2.6]. No other conditioning drug. |
| Graft | DLA-identical (8/8 alleles DLA-88, DRB1, DQA1, DQB1) mobilised donor PBSC (filgrastim +/- plerixafor); mean 8.0 x 10^? CD34+/kg (range 2.08 to 2.9 x 10^?; the exponents are lost in the PMC text, probably 10^6 to 10^7 given the paper's ~5 x 10^6/kg human target and 11/15 donors above it) ; 2-3 DLI aliquots (1-2 x 10^? CD3+/kg) cryopreserved for relapse [2.4] |
| Donor chimerism | 12/12 tested ">95% donor WBC within 2 weeks" [4.2] |
| TRM | "Two dogs (13%), both not in remission when treated, died in the hospital, presumably secondary to TBI toxicity" (day 7 septic shock; day 13 after slow engraftment and DLI x2 on d12-13) [4.4]. One further death d19 "presumptive Grade 5 gastric-dilatation volvulus" in a first-remission dog [5.2] |
| GVHD | acute: "Three out of thirteen dogs (23%) who left the hospital developed cutaneous signs consistent with acute Grade 2 aGvHD"; one after DLI at 8 wk; none life-threatening. "no dogs developed clinical signs associated with chronic GvHD" [4.5, 6]. Cyclosporine toxicity: 1 dog (diabetes, lifelong); Factor V inhibitor 1 dog [4.6, 4.7] |
| Acute toxicity | all dogs Grade 4 neutropenia at mean day 6, ANC >1000/uL in 9-18 d (mean 11); Grade 3-4 thrombocytopenia all; mean hospital stay 22 d; no Grade 4 GI AE [4.3] |
| ITT outcome | median DFI 1095 d (range 9-2920); median OS 1115 d (9-2920). All-cause mortality 40% (2 in hospital, 3 euthanised for progression, 1 GDV). "disease specific mortality was 27%, with 3/15 dogs developing progressive disease" [5.1, 5.2] |
| First-remission (n = 10) | median DFI 1235 d (19-2920); with the GDV dog censored median DFI 1285 d (range 268-2290), median OS 1285 d (268-2920). "Of the remaining nine dogs, only one dog died from lymphoma <2 yrs post-alloHCT (268 days). Of the remaining eight, one was killed ~8 yrs after transplant, while another died ~4.5 yrs after transplant - neither due to recurrent BCL. The remaining six dogs are still alive and disease-free." "The cure rate of alloHCT, as defined as living >4 yrs after the procedure and/or not dying from lymphoma, in these dogs was ~89%." [5.2, 5.3] |
| Not in remission at transplant (n = 5) | 2 died in hospital; other 3: median DFI 25 d (15-250), median OS 1100 d (66-1980); one of these died ~5.3 yr post-transplant "for reasons unrelated to lymphoma" (so survived long after a relapse; salvage unspecified) [5.2, 5.3] |
| Comparators (historical, NCSU) | autoHCT n = 24 (Willcox 2012) + autoHCT+ACT n = 10 (Gareau 2021) = 34 dogs (24 + 10); the first-remission comparison is stated as "27 dogs" in the paper (the paper does not itemise the split; autoHCT 15 are named in 34950726, so the other 12 is not reconciled with the 10-dog ACT cohort, 8 of whom were in CR; flagged). First-remission: autoHCT median DFI 565 d (59-2920), OS 531 d (97-2920); autoHCT+ACT DFI 424 d (98-1500), OS 608 d (150-1500); alloHCT DFI 1235 d, OS 1285 d; log-rank p = 0.0407 (DFI), 0.0284 (OS). ITT (all dogs) p = 0.2953 and 0.3029 (NOT significant). [Fig 2, Fig 3 legends] |
| Trial end-point | "a trial end-point of 4.1 yrs, since all dogs from all 3 studies who lived >2 yrs post-transplant have lived >4 yrs" [2.8] |
| Donor logistics | "all siblings, the bitch/sire, and any other dogs produced by the same mating pair, have a 25% chance of matching. More distantly related dogs, such as cousins, have a 12.5% chance". "no bone marrow donor registries exist for dogs". "10 cases required DLA-genotyping of <=3 related dogs to identify a matched donor"; mean donors screened 5 (range 1-28) [Discussion, 3.1] |

KM numbers at 1, 2, 3, 4, 5 years: NOT FOUND as numbers. The paper gives KM curves only as figures (Fig 2, Fig 3; PMC figure images not machine-readable here) and medians. What can be reconstructed from the text for the 10 first-remission dogs is below (reconstruction, not extraction):

| Event (first-remission, n = 10) | time | source sentence |
|---|---|---|
| death, presumed GDV (non-lymphoma, censored) | day 19 | 5.2 |
| lymphoma death | day 268 | 5.3 |
| death non-lymphoma | ~4.5 yr | 5.3 |
| euthanised non-lymphoma | ~8 yr | 5.3 |
| alive, disease-free (at report) | 6 dogs, follow-up to >=4.1 yr (end-point) up to 2920 d | 5.3 |

So reconstructed relapse-free fraction (9 evaluable dogs): 1 relapse at 0.73 yr; 8/9 = 0.89 relapse-free at 1, 2, 3, 4 yr and (for the 2 non-lymphoma deaths censored at 4.5 and 8 yr) at 5 yr in those still at risk. Inconsistency flagged (not resolved): the first-remission DFI range with GDV dog censored is "268-2290" whereas OS range is "268-2920"; if a dog with DFI 2290 was alive/disease-free, DFI should equal OS unless censored for death; the paper does not explain. Second flag: abstract says "Eight of nine remaining dogs lived >4 yrs ... cure rate of 89%" but follow-up for the six living dogs is not individually stated beyond the 4.1 yr end-point.

Exact binomial 95% CI (Clopper-Pearson) for 8/9 is computed in section 2 (about 0.52 to 0.997).

### 1.2 Autologous TBI + PBSC (all NCSU, same group; B-cell and T-cell)

| Study | n; phenotype; status | Conditioning | Relapse timing | Cure fraction | TRM / toxicity |
|---|---|---|---|---|---|
| PMID 22882500 Willcox 2012 JVIM (doi 10.1111/j.1939-1676.2012.00980.x), abs only (no PMC) | 24 B-cell; 15 transplanted before relapse | cyclophosphamide + G-CSF mobilisation; TBI 10 Gy | median DFI 271 d, OS 463 d (all 24) | "Five of 15 (33%) dogs transplanted before they relapsed remain in clinical remission ... at a median OS of 524 days (range, 361-665 days)". Gareau 2021 quotes median OS 531 d for these dogs | "2 dogs (8.3%) died in the hospital. One (5%) dog exhibited delayed engraftment and died 45 days"; 1 dog TBI pulmonary fibrosis ~8 mo |
| PMID 24467413 Warry 2014 JVIM (doi 10.1111/jvim.12302; PMC4857993, FT) | 15 T-cell; 13 in first CR | HDC 500-750 mg/m2; TBI 10 Gy (3 dogs), 11 Gy (9), 12 Gy (1), mis-dosed 8 Gy + 6 Gy at d93 (1), 12 Gy (1) | of 13 in CR: 3 (23%) relapsed <4 mo; 3 (23%) at 4-8 mo; 5 (38%) after 8 mo (8.3, 10, 12.9, 18.3, 24.6 mo); 1 (8%) no relapse at 24.7 mo. NOTE these sum to 12 of 13; the text does not account for the 13th | median DFI 184 d (28-738), OS 239.5 d (4-738); "2 (14%) dogs still alive at 741 and 772 days" | "Two (13%) dogs died shortly after PBHCT" (sepsis d13; GI toxicity d4); 1 second cancer (cutaneous B-cell lymphoma d120). No DFI difference 10 vs 11 Gy (p = .7665) |
| PMID 34950726 Gareau 2021 Front Vet Sci (doi 10.3389/fvets.2021.787373; PMC8688351, FT) | 10 B-cell, autoHCT + expanded T cells; 8 in CR, 2 in PR/relapse at apheresis | CHOP, HDC 500-650 mg/m2, TBI 10 Gy (n=5) or 12 Gy (n=5), 2 fractions, 8.5 cGy/min | 6 of 10 relapsed: two at 4 mo, 5 and 8 mo, 13 and 15 mo; median DFI 199.5 d (40-449) | "Four dogs (40%) are still alive >=2 years ... considered cured"; 2 of each TBI dose cured | 0 deaths in hospital reported. Conclusion: ACT "does not provide a clinical benefit over CHOP chemotherapy and autoPBHSCT alone" (record correction already in SWEEP_stemcell s0) |
| Historical NCSU auto B-cell first remission (quoted in 34950726) | 15 dogs | CHOP + autoPBHCT | median DFI 565 d (59-2920), OS 531 d (97-2920) | Gareau 2021 text: cure "30% and 19%" for B- and T-cell; 2022 paper: "33% and 40%" | - |

Internal discrepancies: Gareau 2021 lists the 4 "cured" dogs with OS range 86-1317 d although cure is defined as >=2 y (a dog with OS 86 d cannot be one of 4 dogs alive >=2 y); Warry relapse counts sum to 12 of 13. These cap how tightly the auto plateau can be stated.

Pooled NCSU auto B-cell (first remission or transplanted before relapse) cure counts, strictly from the sentences above: 5/15 (33%, Willcox) + 4/10 (40%, Gareau 2021, includes 2 not in full CR) = 9/25 = 36% (95% CI computed in section 2). The 2022 paper says "~65%" relapse and "33-40%" cure. Auto T-cell: 2/13 alive at 741-772 d, 1 of 13 relapse-free at 24.7 mo; no >=2 y plateau can be called for T-cell.

### 1.3 Other canine series (all searched via PubMed; modern-era client-owned dogs)
- Tufts/Colorado/Perth: PMID 22620705 (Lane, Chan, Wyatt 2012, AJVR 73:894; doi 10.2460/ajvr.73.6.894; Perth Veterinary Oncology, abs): 21 dogs with lymphoma, intensified chemotherapy + autologous BMT, G-CSF safety only; median follow-up 4 months; NO outcome (relapse/survival) data. PMID 16594594 (Frimberger 2006; Tufts; already in record) high-dose cyclophosphamide + autologous marrow, no TBI (n = 28, 13 at 500 mg/m2: median remission 54 wk, survival 139 wk). PMID 24762013 (Bucknoff 2014 AJVR 75:425; doi 10.2460/ajvr.75.5.425; Tufts/NCSU authors): 10 client-owned lymphoma dogs, TBI + BMT, thromboelastography only; no outcome. "Colorado" (CSU) transplant series for lymphoma dogs: NOT FOUND in PubMed (searches "dog lymphoma hematopoietic stem cell transplantation", "canine lymphoma autologous transplantation total body irradiation", author Suter). Seattle (Fred Hutch) series: historical (1970s-80s), already in record (3887690, 3901841, 400683, 1095380, 2873669): auto B/T mixed lymphoma, TBI 8.4-13.5 Gy, long-term disease-free 24% (9/38) at 8.4 Gy (3887690), 5/17 in unmaintained CR 200-663 d at 11 Gy (400683).
- Case reports: PMID 16506937 (Lupu 2006 JAVMA 228:728; doi 10.2460/javma.228.5.728): T-cell lymphoma, DLA-identical cousin donor, 2 x 4 Gy, donor chimerism >=58 wk (abs). Graves & Storb review (PMID 34390541; Vet Med Sci 2021; doi 10.1002/vms3.601; PMC8604109, FT) cites: Epstein 1971, 29 dogs, 9.2 Gy TBI + allograft, 7 with lymphosarcoma survived >d8, 2 tumour-free at necropsy d46/d60; Weiden: unrelated marrow 9.2 Gy, 16 dogs survived >14 d, 14/15 disease-free at necropsy; Appelbaum: 2 of 8 chemo-remission dogs, 8.4 Gy + unrelated marrow, died of GVHD. These are secondary citations (in the review text), primary papers not re-read.
- Availability statement in the review: "HCT for the treatment of lymphoma in dogs is available as a therapeutic option at a selected number of institutions within the United States": NCSU, MedVet Columbus ("recently completed its seventh transplantation in dogs with lymphoma"), Bellingham Veterinary Clinic (PMID 34390541, FT).
- Ocular/CNS relapse after canine HCT: CNS relapse rate after canine TBI+HCT: NOT FOUND (no relapse-site data in any of the above papers).

## 2. Poisson cure-model derivation of the effective residual-cell kill (graded OUTCOME-calibrated; arithmetic reproducible with poisson.py)

### 2.1 Model and why transplant CAN be a kill input
Why the earlier "cannot be modelled as a kill rate" was wrong: relapse after a curative-intent program is the event "at least one clonogen survives and regrows". If the number of surviving clonogens is Poisson with mean mu, the plateau (cure) fraction is

  pi = exp(-mu),   mu = N * S,   effective kill  K = ln(1/S) = ln N - ln mu,   mu = -ln(pi)

N = clonogens the step starts from, S = per-clonogen surviving probability of the step (net of regrowth in the window). A plateau fraction measured in dogs therefore fixes mu (the mean number of surviving clonogens per dog) with no kill-rate assumption at all; K then needs only N. The transplant is a pulse (TBI, 2 d) plus a persistent donor effector; both are summarised by K (e-folds) and a window T. This is the same arithmetic the repo clock uses (days to clear = (ln n0 + 0.577)/margin), run in reverse from outcomes.

Assumptions (stated): (A1) clonogens independent and homogeneous (a resistant subclone makes K an "equivalent homogeneous kill"); (A2) plateau = cured; the measured "cure" is a 2-4 y plateau, not 10 y (section 2.6); (A3) relapse-free fraction is read among dogs that survived the early TRM period (TRM is a separate competing term, section 7); (A4) the first-remission populations are comparable (they are not randomised; selection bias favours transplant, so K is an upper-leaning estimate); (A5) burden N is a range, not a measurement.

### 2.2 Plateau fractions -> mu (exact binomial 95% CI, Clopper-Pearson, computed)

| Cohort | k/n | pi (95% CI) | mu = -ln pi (CI-limits) | source |
|---|---|---|---|---|
| CHOP-type chemotherapy alone, B-cell/mixed, first remission, 5-y | control 5-y first-remission rate 4.4% (CI 0.9-12.2) | 0.044 | 3.12 (range 2.1-4.7) | PMID 42525883 Table 9 (FT): control dogs 1/2/3/5-y first remission 31% / 8.7% / 4.4% / 4.4% |
| chemotherapy alone, other series | 13/127 alive >2 y; 5-y survival 1% | 0.01-0.10 | 4.6-2.3 | PMID 21320018 (abs; 4/3/1% at 3/4/5 y) |
| CHOP + low-dose-rate half-body RT (6 Gy per half), 5-y | 18% (CI 10-28), 3-y 30% | 0.18 | 1.71 (range 1.27-2.30) | PMID 42525883 Table 9 (n = 75) |
| Auto TBI-HCT, B-cell, pooled NCSU first-remission | 9/25 (5/15 Willcox + 4/10 Gareau) | 0.36 (0.18-0.58) | 1.02 (0.55-1.72) | 22882500, 34950726 |
| Auto TBI-HCT, T-cell | 2/13 alive 741-772 d (not a >2 y plateau) | 0.15 (0.02-0.45) | 1.87 | 24467413 |
| Allo DLA-identical, B-cell, first remission, GDV death excluded | 8/9 | 0.889 (0.518-0.997) | 0.118 (0.003-0.659) | 35789057 |
| same, GDV death counted as failure | 8/10 | 0.80 (0.44-0.975) | 0.223 (0.026-0.81) | 35789057 |
| Allo, intent-to-treat incl. 5 not-in-remission dogs | 8/15 | 0.53 (0.27-0.79) | 0.63 (0.24-1.33) | 35789057 (not the early-detection population) |

Read-out in plain terms: after the auto program the mean number of surviving clonogens per dog is about 1.0 (0.5-1.7); after DLA-identical allo it is about 0.12 (0.003-0.66). Chemotherapy alone leaves about 3 (2-5).

### 2.3 Absolute effective kill K = ln N - ln mu (burden is a range)
Burden N: clinical stage III-V multicentric lymphoma 1e11 cells (the repo's calibration burden, docs/LYMPHOMA_COVERAGE_LEDGER.md s7); early-detection burden 1e9 (1 cm^3 ~ 1e9 cells; assumption, user: "assuming early detection"); after clinical CR the PARR/flow-undetectable residual is 1e6-1e9 (ASSUMED range; no canine MRD series found, section 8). Whole-program K from diagnosis:

| N at diagnosis | chemo alone (mu 3.12) | auto TBI-HCT (mu 1.02) | allo DLA-identical (mu 0.118) |
|---|---|---|---|
| 1e9 | 19.6 e-folds (8.5 log10) | 20.7 (9.0) | 22.9 (9.9) |
| 1e10 | 21.9 (9.5) | 23.0 (10.0) | 25.2 (10.9) |
| 1e11 | 24.2 (10.5) | 25.3 (11.0) | 27.5 (11.9) |

Check that the absolute reading cannot be used for the transplant step alone: if the TBI pulse were the only kill in auto-HCT, mu = N_res * exp(-K_TBI) = 1.02 would imply N_res = 1.02 * exp(K_TBI) = 1.5-285 clonogens for K_TBI = 0.36-5.63 e-folds (LQ range, SWEEP_stemcell s4.1). A dog in CR carries far more than 285 clonogens (>=1e6 by any detection limit), so the absolute step-kill cannot be recovered from outcomes without a measured N_res. This is the reason the scientifically defensible input is the DIFFERENTIAL one below (it cancels N). Absolute K is reported only as the whole-program total.

### 2.4 Differential (N-free) kill: ln(mu_ref / mu_x). Central, low, high
For two programs on comparable first-remission dogs with the same N, ln(mu_ref/mu_x) = K_x - K_ref, independent of N and of the pre-transplant CHOP.

| Increment | central | low | high | arithmetic (mu values from 2.2) |
|---|---|---|---|---|
| Half-body RT (6 Gy x 2 halves, LDR) over CHOP alone | 0.60 e-folds | 0.0 (CIs overlap) | 0.99 | ln(3.12/1.71) = 0.60; high uses chemo 1%: ln(4.61/1.71) = 0.99 |
| Auto TBI-HCT (B-cell) over CHOP alone | 1.12 | 0.21 (auto lower CI 0.18 vs chemo upper CI 0.122: ln(2.10/1.71)) | 1.61 | ln(3.12/1.02) = 1.12; auto 0.40: ln(3.12/0.916) = 1.23; chemo 1%, auto 0.40: ln(4.61/0.916) = 1.61 |
| Allo DLA-identical (CR1) over CHOP alone | 3.29 | 1.56 | 4.63 (5.02 vs chemo 1%) | ln(3.12/0.1165) = 3.29; low: allo 0.52 (lower CI): ln(3.12/0.654) = 1.56; high: allo 0.97: ln(3.12/0.0305) = 4.63 |
| Allo over auto (same cohort type) | 2.17 | 0.34-0.45 (allo lower-CI 0.52 vs auto 0.36-0.40) | 3.51 (allo 0.97 vs auto 0.36); 3.59 vs auto 0.33 | ln(1.022/0.1165) = 2.17; ln(1.022/0.654) = 0.45; ln(1.022/0.0305) = 3.51 |

The high end is bounded by the exact upper CI limit (0.997 -> 5.8 e-folds over auto) which is not credible given n = 9; 0.97 is used as "high".

### 2.5 Allograft effect separated from TBI and HDC (what the model needs for the new agent)
The allo cohort got 2 x 4 Gy and no high-dose cyclophosphamide; the auto cohorts got 2 x 5-6 Gy plus HDC (500-750 mg/m2) and an autologous graft. So

  K_graft(allo) = [K_allo - K_auto] + [K_TBI(2x5) - K_TBI(2x4)] + K_HDC(auto) - K_contam(auto graft)

with the first bracket from 2.4, the second from the repo LQ radiobiology (in-vivo-corrected, factor 1.9, PMID 3009370 as used in SWEEP_stemcell: 2x5 minus 2x4 Gy = 0.57 / 0.39 / 0.27 / 0.20 e-folds for CLBL1 / OSW / 1771 / CLL1390; in vitro 1.78 / 1.11 / 0.84 / 0.73). K_HDC is unmeasured (>=0, adds to K_graft), K_contam (tumour cells re-infused with the auto graft) is unmeasured (>=0, subtracts). Both are left out of the numbers below; they push in opposite directions and are the reason the allo effect is labelled "graft effect = donor immune effector + tumour-free graft", not GVL alone.

| | LOW | CENTRAL | HIGH |
|---|---|---|---|
| allo over auto | 0.45 (allo 0.52 vs auto 0.36) | 2.17 (0.89 vs 0.36) | 3.59 (0.97 vs 0.33) |
| + TBI dose difference (in-vivo-corrected, lines mean-ish) | +0.20 | +0.40 | +0.57 |
| K_graft (e-folds, net) | 0.65 | 2.6 | 4.2 |
| in log10 | 0.28 | 1.13 | 1.82 |

### 2.6 Time dimension: window and per-day rate
Evidence for the window: donor chimerism >95% within 2 weeks (35789057 s4.2); cyclosporine to ~day 30; GVHD signs ~2 weeks after cyclosporine stops (so effector activity ~day 30-60); the one lymphoma death in 9 first-remission dogs at day 268 and none later; Warry auto relapses 120-750 d. Window used: day 14 to day 180 (166 d) central; sensitivity day 30-120 (90 d) and 330 d.

| | LOW | CENTRAL | HIGH |
|---|---|---|---|
| net decline rate K/T, T = 166 d | 0.0039 /d | 0.0157 /d | 0.0253 /d |
| T = 90 d | 0.0072 | 0.0289 | 0.0467 |
| T = 330 d | 0.0020 | 0.0079 | 0.0127 |
| gross kill in the repo convention (kill - growth = net; growth g = 0.0903/d, GROWTH_PER_DAY) T = 166 d | 0.0942 | 0.1060 | 0.1156 |
| gross kill, T = 90 d | 0.0975 | 0.1192 | 0.1370 |

Convention warning (this matters for how it is loaded): K is a net lineage-survival e-fold, so the clock must be fed either (i) the net decline K/T directly (do not subtract growth again), or (ii) gross = g + K/T as in the last two rows. The mean-field "kill must exceed 0.0903/d" bar is met by the allograft in the gross reading only because K>0 is a net decline that outcome data show; it is not a measured potency, and should not be combined with a separate 0.09/d bar test.

Relapse-timing consistency check (a model test, not a fit): a surviving lineage regrows from n cells to the 1e9-cell detection size in t = ln(1e9/n)/g. At g = 0.0903/d: 229 d for n = 1, 153 d for n = 1e3, 102 d for n = 1e5; at net g = 0.03-0.04/d (slower, immune-restrained): 518-691 d for n = 1. Observed auto relapses at 4-15 mo (120-450 d; 34950726) and 8.3-24.6 mo (Warry), and the single allo relapse at 268 d, all fall inside 100-700 d. So mu of order 1 (a few lineages) is time-consistent with when dogs actually relapse; mu of order 1e6 would give relapse inside ~10 weeks, which is not seen.

### 2.7 Cross-checks of the derived increments (consistency, not independent proof)
1. Radiation: LQ in-vivo-corrected e-folds from the repo's canine lymphoid lines for 6 Gy x1 are 0.77-2.04 (in vitro 1.46-3.87); the plateau-derived HBRT increment 0.60 (0.99 with chemo at 1%) sits at the bottom of that range. For 2 x 5 Gy TBI the in-vivo-corrected LQ values are 0.56-1.94, and the auto-HCT plateau increment is 1.12 (0.5-1.6): inside the range. So the derived outcome increments and the radiobiology are mutually consistent at the in-vivo-corrected level, and the SWEEP concern (LQ predicts large gains from dose escalation that outcomes did not show) is not contradicted: the plateau is set by a few resistant lineages, not by uniform LQ kill.
2. Human consolidation increments: record SWEEP_cnsregimens s9 gives 0.85-1.0 e-fold for thiotepa-ASCT over next-best alternatives (PRECIS, IELSG43); the canine auto-HCT increment 1.12 is of the same order.
3. Human allo vs auto in T-cell lymphoma (AATT, PMID 39270145, abstract): cumulative progression/relapse 8% (CI 0-19) allo vs 55% (CI 35-74) auto -> relapse-free 0.92 vs 0.45 -> mu 0.083 vs 0.80 -> ln ratio = 2.26 e-folds (low 0.72 using 19% vs 35%; 2.78 using 8% vs 74%). Canine B-cell allo-over-auto = 2.17 (0.34-3.6). Same order across species, disease, immunophenotype; CIs overlap widely so this is corroboration of magnitude, not a test.

### 2.8 2-year to 10-year inference for this input (rule 12: bound, not odds)
Dogs: 8 first-remission dogs lived >4 y; the only lymphoma death was day 268; zero relapses after year 1 among nine evaluable dogs. Minimum at-risk time after year 2 = 8 dogs x (4.1 - 2.0) = 16.8 dog-years with 0 events -> exact Poisson 95% upper bound on late relapse hazard = 2.996/16.8 = 0.18 per year (point 0). With actual follow-up (6 alive to up to 2920 d, one killed ~8 y) the denominator is larger; individual follow-up is not reported (NOT FOUND). This bound is too weak to assert 10-year closure; it supports "no relapse seen after the first year, hazard < 0.18/yr". Human RIC allo in follicular lymphoma has the lowest relapse of any human lymphoma series found: 8% (CI 2-23) at median follow-up 52 mo (PMID 20107156). Long-horizon competing risks (not relapse): second cancer after TBI (radiation chimeras ~5x malignancy, PMID 6355021, in record) and ordinary dog lifespan (donor-recipient mean age 55 mo; a 10-y horizon reaches age ~14.6 y).

## 3. Graft-versus-lymphoma: mechanism and escape coverage (human data TRANSFERRED; every PMID fetched this session)

Mechanism, stated for the dog case: in a DLA-identical recipient the donor and host share MHC, so donor T cells (and NK cells) recognise host minor histocompatibility antigens presented on shared MHC (and tumour-associated antigens); this is why GVL and GVHD are linked and why the 15-dog series saw only mild skin GVHD (3/13, grade 2) and no chronic GVHD (35789057 s4.5, s6). Source statement for the dog case in the paper: DLA-matched donor T cells "cause ... GvHD, leading to a beneficial secondary graft-versus-lymphoma (GvL) response" (Introduction). Minor-H antigen vaccination to boost this is demonstrated in the canine HCT model (PMID 25965411, FT not read, abstract: priming with adenovirus SMCY/SRY constructs plus plasmid DC boost induced antigen-specific CD4 and CD8 responses in donors; DLI changed chimerism in 1 of 3 male recipients without GVHD) - relevant to the user's "vaccines" point (section 7).

### 3.1 Evidence by property

| Property | Evidence (exact) | Grade |
|---|---|---|
| Immune-mediated kill of lymphoma after allo | Direct clinical proof of a GVL effect: DLBCL, 15 patients not in CR at d+100 or relapsing: after immunosuppression withdrawal (n = 10) or DLI, "Nine (60%) patients subsequently responded (complete = 8, partial = 1) ... Six patients are alive (range 42-83+ months) in complete remission without further treatment" (PMID 18684698, Bishop 2008, abs). Relapsed PTCL, RIC allo, 52 pts: "8 out of 12 patients (66%) who received donor-lymphocytes infusions for disease progression had a response" (PMID 21904377, abs). Follicular lymphoma: "10 (77%) of 13 patients given DLI for relapse after transplantation experienced remission, with nine of these responses being sustained" (PMID 20606089, abs). Mature lymphoid malignancies RIC-alemtuzumab 288 pts: presence of GVHD protective of relapse (P = 0.03) (PMID 30467838, abs) | TRANSFER (human); dog: OUTCOME in the same direction (35789057) |
| Not a drug-efflux (P-gp) mechanism | The tested clinical correlate is chemo-refractory disease: PTCL RIC-allo cohort above: 27 of 52 had failed a previous autoSCT (i.e. were chemo-resistant in effect), 5-y PFS 40% (PMID 21904377). DLBCL responses above were in patients with disease persisting through transplant. DIRECT test of CTL/NK killing of P-gp-expressing lymphoma cells: NOT FOUND (PubMed queries returned only unrelated papers). Class mechanism: perforin/granzyme and Fas killing are not substrates of ABCB1. | TRANSFER (mechanism + chemorefractory outcome); direct assay NOT FOUND |
| Independent of the targeted B antigen (CD20/CD19 loss) | Allo works in T-cell lymphoma, which has no CD20/CD19 target: AATT, allo relapse 8% vs auto 55% (PMID 39270145). Target = alloantigens (minor-H/MHC), not a lineage antigen. One human PCNSL case: relapse after CD19-CAR-T then allo gave a temporary response, relapse day 98 (PMID 39098011, n = 1, abstract) - consistent with "partly covers, not a closure" | TRANSFER (strong for mechanism; n = 1 for CAR-T-escape setting) |
| Kills slowly-dividing / non-cycling cells | Indolent, low-proliferation tumours where S-phase-gated chemo fails are cured or controlled by allo: follicular lymphoma RIC sibling allo relapse 8% (CI 2-23) median FU 52 mo (PMID 20107156); FL (n = 82) 4-y PFS 76% for the whole cohort, relapse 26% (PMID 20606089); CLL RIC allo 5-y PFS 83% for the best prognostic group (PMID 22955330) and CR in 20/43 (47%) of CLL patients after immunomanipulation (withdrawal/rituximab/DLI) (PMID 21455998). Direct canine quiescent-cell assay: NOT FOUND. | TRANSFER (outcome in low-proliferation human tumours) |
| MHC dependence / escape by MHC loss | Genomic loss of mismatched HLA: "HLA loss variants accounted for 33% of the relapses (23/69)" after partially-matched related HSCT, "all the HLA loss relapses occurred after MMRD HSCT, and 20/23 in patients with acute myeloid leukemia", later than classical relapse (median 307 vs 88 d) (PMID 25371177, abs; AML, indirect). 5 of 17 relapses after haplo + donor T cells (PMID 19641204). MHC class II down-regulation at relapse in 17 of 34 post-transplant AML relapses (PMID 30380364, abs). For DLA-IDENTICAL donors "mismatched-haplotype loss" does not apply (no mismatched haplotype), but loss or down-regulation of the shared MHC still hides minor-H peptides. Canine B-cell lymphoma: low MHC-II predicts poor outcome (PMID 21781170, in record). Frequency of MHC loss after allo in LYMPHOMA: NOT FOUND (all quantification above is myeloid). | TRANSFER (indirect, myeloid) |
| CNS | Secondary CNS lymphoma, nonmyeloablative Flu/Cy/200 cGy TBI + PTCy allo, n = 20 (PMID 34293518, abs): median FU 4.1 y, median PFS 3.8 y, cumulative relapse 25% (CI 5-45), NRM 30% (CI 5-54) at 4 y; 5 relapses: 2 CNS-only, 1 systemic-only, 2 combined. Authors' question "whether a graft-versus-lymphoma effect could maintain remission in CNS disease". T cells in CSF after allo: NOT FOUND (query returned no records). CNS relapse rate after allo in lymphoma beyond this series: NOT FOUND. Dog CNS relapse after HCT: NOT FOUND (no relapse-site data). | TRANSFER (n = 20) |
| Apoptosis evasion (TP53, BCL2 family) | Mechanistic (perforin-granzyme, Fas) and outcome (GVL effective in chemo-refractory disease); no dog or TP53-stratified allo data retrieved | TRANSFER (mechanism), no PMID |
| Persistence of the effector | Dog: "All 12 dogs who had VNTR chimerism analysis post-alloBMT achieved >95% donor WBC cells within 2 weeks"; case report donor chimerism >=58 weeks (PMID 16506937, abs); 6 dogs alive and disease-free at report (to 2920 d). Donor graft is a lifelong immune system, unlike CAR-T persistence 14-50 d | OUTCOME (dog) |

### 3.2 Escape-by-escape: closes / does not close (allo DLA-identical HCT; scope = canine multicentric B-cell lymphoma, first remission, DLA-identical donor)

| Escape (existing 23-escape set) | Closed by allo graft? | Basis | Residual |
|---|---|---|---|
| P-gp / efflux, ABCB1 | closed | class mechanism + chemo-refractory outcomes (TRANSFER) | direct assay NOT FOUND |
| CD20 / CD19 loss, antigen escape | closed (does not use the antigen) | mechanism + T-cell lymphoma outcomes (TRANSFER) | - |
| non-cycling persister / dormancy | plausibly closed | low-proliferation human tumours (TRANSFER); also TBI kills non-cycling cells (radiation, DERIVED) | no canine quiescent-cell assay |
| apoptosis evasion (BCL2 family, TP53 downstream) | closed by mechanism | TRANSFER | TP53-stratified allo outcome NOT FOUND |
| dCK loss / antimetabolite resistance, MGMT, other drug-handling | closed (drug-independent) | mechanism | - |
| BCR/NF-kB signalling escapes (TRAF3 etc.) | closed (kill not signalling-dependent) | mechanism | - |
| MHC-I loss / antigen presentation loss | NOT closed by the T-cell arm; NK (missing-self) arm of the graft unproven | HLA/MHC-II loss data (myeloid) | open; the one escape allo is structurally exposed to |
| MHC-II down-regulation | partly | AML data; low MHC-II is a poor-prognosis feature in dogs | open |
| CNS sanctuary | closed at a reduced access (0.5, 0.25-1.0, section 7) | n = 20 human SCNSL | CNS-only relapses were 2 of 5 |
| testis, eye sanctuaries | unknown | not found | open (not assessed) |
| founder TP53/TRAF3 lesions (present before treatment) | irrelevant to an immune kill | mechanism | - |

Per CLAUDE.md rule 5 and 12, "closed" here means "the model has an effector that reaches this escape at an outcome-calibrated or transferred strength", not "shown in dogs per escape". No per-escape attribution exists in any transplant series.

## 4. Availability in dogs TODAY (2026-10-02)

| Item | Finding | Source |
|---|---|---|
| Procedure exists in client-owned dogs | 15 allo (DLA-identical) transplants 2006-2018 at 4 facilities; ~100 NCSU transplants since 2008 (mostly autologous) as of 2023; 94 TBI+HCT dogs in 10 y at NCSU (7 died before discharge) | 35789057 (FT); WRAL 2023 (WEB, "Since 2008, a hundred dogs have been treated"); 38695516 (record) |
| Centres | Performing: NCSU (university), Bellingham Veterinary (WA, private; pioneer: Dr Sullivan, named in the allo paper's affiliations), VCA West LA, MedVet Columbus OH ("recently completed its seventh transplantation in dogs with lymphoma", Graves & Storb review PMID 34390541 FT); "available ... at a selected number of institutions within the United States" | 35789057 affiliations; 34390541 |
| NCSU status | Program paused: "we are not accepting new bone marrow transplant patients at this time as we pause" for an external review; ~Feb 2023; 13 waitlisted; no resumption date. Current status 2024-2026: NOT FOUND (searches returned nothing newer) | WRAL (WEB), Change.org petition 2023-02-19 (WEB) |
| Bellingham today | Page states transplant "from either a donor or from the pet's own bone marrow"; no cost, number or DLA detail given | bhamvet.com (WEB) |
| Cost | NCSU ~US$35,000 (2023 report); ~US$26,000 average (2022 article); US$13-17k (earlier); Bellingham ~US$25,000 planned fee / US$45,000 documented case. Includes all except ICU, transfusions, extra diagnostics. Donor-finding extra: some owners spent >US$6,000 on matching | WRAL, DogCancer.com/WholeDogJournal (WEB; secondary) |
| Donor | "no bone marrow donor registries exist for dogs"; commercial DLA genotyping exists (Fred Hutch Canine Resource Development lab did typing in the series); each full sibling or parent-offspring-from-same-mating dog has a 25% chance of a DLA-identical match, cousins 12.5%; 10 of 15 cases needed typing of <=3 relatives; mean 5 (range 1-28) dogs screened; donors in the series: 6 female siblings, 6 male siblings, 2 bitches (dam), 1 same-mating male | 35789057 Discussion, Table 1 |
| Match probability with k siblings | 1-(0.75)^k = 0.25 (k=1), 0.44 (2), 0.58 (3), 0.68 (4), 0.76 (5), 0.82 (6) (Mendelian; assumes four distinct parental haplotype combinations; cousins 1-(0.875)^k = 0.125, 0.23, 0.33, 0.49 for k=1,2,3,5) | derived from the paper's 25%/12.5% |
| Fraction of lymphoma dogs with an available relative | NOT FOUND | - |
| Donor safety | filgrastim +/- plerixafor mobilisation; apheresis 180-401 min; "no AE noted"; same-day discharge; donor must be healthy, 2-9 y (mean 57 mo) | 35789057 |
| Haploidentical | Research only; lethal GVHD without special manipulation: DLA-haplo PBSC without post-graft immunosuppression, all died (8605371, record); DLA-haplo with transduced CTL, GVHD in all engrafted (11719387, record); DLT on days 3, 7, 14 after CD6-depleted haplo marrow fatal GVHD, day 20 fatal in 2 of 4 (PMID 19446000, abs, fetched). One haplo recipient among 5 NCSU necropsied dogs, died (38695516, record). | record + 19446000 |
| Reduced-intensity | 2 Gy TBI + sirolimus/cyclosporine DLA-identical: durable chimerism 5/6 evaluable (median follow-up >48 wk); 1 Gy: 5/5 rejected (PMID 12931117, abs, fetched). No lymphoma outcome with RIC in dogs found | 12931117 |
| DLI | Cryopreserved donor CD3+ aliquots made routinely (2-3 doses) "for the purpose of inducing GvL in the setting of relapsed disease"; given to 1 dog on d12-13 (died d13) and 1 at 8 wk (cutaneous GVHD, resolved); no outcome series for relapse-DLI in dogs found. Seattle dog data: DLT within 3 weeks of T-depleted DLA-identical marrow fatal GVHD, at 2 months or later tolerated (from PMID 19446000 abstract) | 35789057; 19446000 |
| MSC for GVHD | MSC did not prevent GVHD or rejection after DLA-haplo BMT (PMID 20816818, record); safe in DLA-identical (23723082, record) | record |
| Radiation capacity | 2 x 4 Gy at 7.5-10 cGy/min on a 6 MV linac; dosimetry/protocol verified across 5 sites (PMID 31146304, record) | 35789057; record |
| Tier (CLAUDE.md rule 13) | allo DLA-identical HCT = exists-today (client-owned dogs, off-label procedure, 15 cases) but donor- and centre-limited (not generally available; NCSU paused). Auto TBI-HCT = exists-today, centre-limited. Haplo, DLI-for-relapse, RIC, MSC-for-GVHD = research / to-build | this report |

## 5. Autologous HSCT: dog data, rescue role, conditioning intensification, TRM

Dog data: section 1.2 (B-cell plateau 5/15 and 4/10 = 36% pooled; T-cell 2/13 alive at ~2 y, no plateau; relapse hazard concentrated 4-15 mo; dogs >2 y alive all >4 y in the NCSU sets, PMID 35789057 s2.8). Role of the graft: no kill; it removes the marrow ceiling so a 10-12 Gy TBI is survivable (dogs survive ~7 Gy with care, die at >=8 Gy without graft: PMID 19747631 in record; supralethal 6-8 Gy TBI + marrow/LTMC survival in dogs: PMID 8490811, Abrams-Ogg 1993, abs fetched: "dogs can recover following supralethal TBI ... if they receive intensive platelet and antimicrobial therapy"). Represent as marrow-axis modifier + procedural TRM, not a potency.

What TBI adds per dose (from the existing derived radiobiology, SWEEP_stemcell s4.1, repo LQ): 2 x 4 Gy in vitro 3.85/2.68/1.78/1.30 e-folds (CLBL1/OSW/1771/CLL1390), in vivo-corrected 1.37/1.06/0.62/0.36; 2 x 5 Gy in vitro 5.63/3.79/2.62/2.03, in vivo 1.94/1.45/0.89/0.56; 2 x 6 Gy in vitro 7.73/5.08/3.61/2.93. Marginal e-folds per extra Gy at 8-12 Gy in vivo: ~0.2-0.3/Gy by LQ, but outcomes show no benefit from escalation (10 vs 12 Gy: DFI p = 0.296, PMID 34950726; 10 vs 11 Gy p = 0.7665, PMID 24467413; 8.4 vs 13.5 Gy Seattle, record) while TRM rises (Seattle 26% to 55%, record). Conclusion for the model: credit TBI one pulse of 0.4-1.9 e-folds (DERIVED, in-vivo-corrected 2x5 Gy: 0.56-1.94), cap at ~10 Gy, and do not credit dose escalation. The auto plateau increment over CHOP alone (1.12 e-folds, section 2.4) is consistent with this pulse.

Intensification by drug conditioning (HDC thiotepa/busulfan/BCNU as an alternative to TBI): human CNS-lymphoma data in record (3-y PFS 78% IELSG43; 8-y EFS 67% PRECIS; ASCT adds ~0.85-1.0 e-fold over next-best consolidation; MATRix program 0.13-0.21/d over ~115 d at assumed N0); canine IV busulfan 20 mg/kg is myeloablative with autologous rescue (PMID 10534062, record); canine thiotepa PK NOT FOUND; canine cyclophosphamide 500 mg/m2 + autologous marrow no TBI: median remission 54 wk vs 21 wk lower dose (PMID 16594594, record). So a TBI-free auto-HCT with drug conditioning is "buildable" with TRANSFER inputs, but nothing in dogs yet for CNS lymphoma.

TRM (exact binomial CI): NCSU 7/94 = 7.4% (3.0-14.7) before discharge (PMID 38695516, record); Willcox 2/24 = 8.3% (1.0-27); Warry 2/15 = 13% (1.7-41); Gareau 2021 0/10; allo 2/15 = 13% (1.7-41), both dogs not in remission; allo first-remission 0/10 TBI-toxicity deaths (0-31%), 1/10 incl. the d19 GDV death (10%, 0.3-44%). Modes: sepsis incl. candidiasis, marrow aplasia, severe GI toxicity (3 of 5 necropsied dogs candidiasis, 38695516). Long-term: 1 TBI pulmonary fibrosis (22882500), 1 second cancer (24467413).

## 6. Human T-cell lymphoma allo vs auto, and CNS allo (verified metadata, abstract numbers)

AATT (PMID 39270145, JCO 2024, doi 10.1200/JCO.24.00554, randomised phase III, PTCL): "Seven-year EFS of patients randomly assigned to alloSCT was 38% (95% CI, 25 to 52) compared with 34% (95% CI, 22 to 47) for ... autoSCT; OS was 55% (95% CI, 41 to 69) and 61% (95% CI, 47 to 74). Among patients undergoing alloSCT (n = 26) or autoSCT (n = 41) on study, the cumulative progression/relapse rate was 8% (95% CI, 0 to 19) and 55% (95% CI, 35 to 74). Nonrelapse mortality (NRM) was 31% (95% CI, 13 to 49) and 3% (95% CI, 0 to 8)". Salvage alloSCT after auto failure (15/30 early progression, 11/20 relapse): "Seven-year OS after salvage alloSCT was 61%; NRM was 23%". "Long-term follow-up documents the strong graft versus lymphoma effect of alloSCT independent of the timing of transplantation ... AlloSCT is currently not recommended as part of first-line consolidation." Poisson reading: section 2.7 (2.26 e-folds). Reading for the dog: the relapse-kill benefit is real and large; the human net benefit is erased by NRM 31%; the dog series NRM is 13% (ITT, both not in remission) with no chronic GVHD, so the net trade is more favourable in the DLA-identical dog (n = 15, weak).
Secondary CNS lymphoma allo (PMID 34293518): numbers in section 3.1.


## 7. MODEL INPUTS (what to load into the catalogue / clock; each number states grade and source section)

Scope: canine multicentric B-cell lymphoma (T-cell: auto-HCT only 2/13 alive ~2 y, no allo series; T-cell allo is a TRANSFER from AATT, section 6), first remission (early detection), DLA-identical donor for allo. Grades use the repo scale: OUTCOME (calibrated to dog plateau data), DERIVED (arithmetic on measured canine cell data), TRANSFER (human or class mechanism, justified in section 3), ASSUMED (no basis).

### 7.1 New agent: "allogeneic DLA-identical HCT, graft effect (donor immune effector + tumour-free graft)"
Replaces the previous "cannot be modelled as a kill rate". It is modelled as a net e-fold removal over a window, which the clock can use as a margin.

| Field | LOW | CENTRAL | HIGH | Grade / source |
|---|---|---|---|---|
| K_graft, net e-folds of residual-clonogen kill over the window | 0.65 | 2.6 | 4.2 | OUTCOME-calibrated (Poisson cure model, 2.4-2.5); human AATT corroboration 2.26 (TRANSFER, 2.7) |
| same in log10 | 0.28 | 1.13 | 1.82 | |
| Window | day 14 to day 180 (166 d); sensitivity 90 d and 330 d | | | window = chimerism day 14 + cyclosporine to d30 + onset of effector; ASSUMED within the evidence (no canine kinetics) |
| Net decline rate over 166 d | 0.0039 /d | 0.0157 /d | 0.0253 /d | derived |
| Gross kill if the clock subtracts growth g = 0.0903 /d (GROWTH_PER_DAY) | 0.0942 | 0.1060 | 0.1156 | derived; use ONE convention only (net or gross) |
| Same, 90-d window | net 0.0072 / gross 0.0975 | 0.0289 / 0.1192 | 0.0467 / 0.1370 | |
| Credit after the window | none by default (conservative); late-relapse hazard bound 0.18 /yr upper 95%, point 0 (zero relapses after year 1; section 2.8) | | | OUTCOME (bound only) |
| Mean surviving clonogens left after the whole allo program (mu) | 0.63 | 0.118 | 0.003-0.03 | OUTCOME |
| Division-gated | no (f-weighting not applied) | | | TRANSFER: low-proliferation human tumours (FL, CLL; section 3.1) and drug-independent mechanism; no canine quiescent-cell assay |
| Efflux (P-gp/BCRP) substrate | no | | | TRANSFER (mechanism; chemo-refractory outcomes); direct assay NOT FOUND |
| Antigen targets | none lineage-specific (alloantigens: minor-H presented on shared DLA) -> covers CD20/CD19 loss | | | TRANSFER (works in T-cell lymphoma, AATT) |
| MHC dependence | YES: needs DLA-I/II-presenting tumour cells; escape = MHC loss/down-regulation (open) | | | TRANSFER (AML HLA loss 33% of mismatched-related relapses; MHC-II down 17/34) |
| Access, systemic | 1.0 | 1.0 | 1.0 | cell trafficking; dog OUTCOME |
| Access, CNS (fraction of systemic K delivered) | 0.25 | 0.5 | 1.0 | TRANSFER, derivation below |
| Access, testis / eye | not assessed | | | NOT FOUND |
| Course | conditioning day 0 (2 x 4 Gy, 7.5-10 cGy/min), hospital mean 22 d, cyclosporine to ~d30, GVHD watch to ~d100; donor apheresis 3-6.7 h | | | 35789057 |

CNS access derivation (arithmetic): human secondary-CNS-lymphoma allo, 4-y cumulative relapse 25% (CI 5-45) -> relapse-free 0.75 -> mu_CNS = -ln(0.75) = 0.288 (CI 0.051-0.598) (PMID 34293518). Human systemic allo comparator (AATT, T-cell): relapse 8% (0-19) -> mu_sys = -ln(0.92) = 0.083 (0-0.21). If both sets had the same pre-graft burden, the extra clonogen survival in CNS is ln(0.288/0.083) = 1.24 e-folds (CI: ln(0.598/0.083) = 1.97 at worst; negative at best). Applied to the dog K_graft: K_CNS = 2.6 - 1.24 = 1.36 (central; access 0.52 of 2.6), worst 2.6 - 1.97 = 0.63 (access 0.24), best >= 2.6 (access capped at 1.0). Weakness stated: different diseases, conditioning (Flu/Cy/2 Gy TBI + PTCy) and prior therapy; n = 20; so TRANSFER, central 0.5. 4 of 5 relapses involved CNS (2 CNS-only, 2 combined) in a cohort selected for CNS disease: consistent with CNS being the least-cleared site. Mechanism support for non-zero access: donor T cells are circulating effector cells that enter CNS under surveillance (T cells in CSF after allo: NOT FOUND in this session; the in-record CAR-T CNS human data apply the same cell-trafficking argument). Use the CNS value as access multiplier on K, not on the kill rate.

### 7.2 Revised agent: "total body irradiation pulse (allo conditioning, 2 x 4 Gy)" and "TBI + autologous HCT (2 x 5 Gy + HDC)"
Replace the repo's 14-day rate with a 2-day pulse and cap at ~10 Gy.

| Field | LOW | CENTRAL | HIGH | Grade |
|---|---|---|---|---|
| TBI 2 x 4 Gy, e-folds, in-vivo-corrected (factor 1.9) | 0.36 (CLL1390) | 0.8 (OSW/1771 mean ~0.84) | 1.37 (CLBL1) | DERIVED (canine lymphoid lines, PMID 27257868) + TRANSFER (in vivo factor, PMID 3009370) |
| in vitro, upper bound | 1.30 | 2.68 | 3.85 | DERIVED |
| TBI 2 x 5 Gy auto, in-vivo-corrected | 0.56 | 1.0-1.45 | 1.94 | DERIVED+TRANSFER |
| Delivery | 2 days -> 0.18 / 0.40 / 0.69 per day (2 x 4 Gy) | | | arithmetic |
| Auto-HCT program increment over CHOP alone (outcome) | 0.21 | 1.12 | 1.61 e-folds | OUTCOME (2.4) |
| Dose escalation above ~10 Gy | credit 0 additional | | | OUTCOME: no benefit, TRM up |
| Division gating | no (radiation cycle-independent in 27 canine lines) | | | DERIVED (PMID 27257868) |
| Efflux substrate | no | | | physics |
| Access | whole-body photons; CNS dose delivered by the whole-body field (brain dose not separately measured; transfer 1.0 with the "relapse after TBI" note) | | | TRANSFER |

### 7.3 Toxicity budget (repo axes: Organ.MARROW, Organ.PROCEDURAL, Organ.IMMUNE_MEDIATED, Organ.GI, ...)
| Axis | Input | Source |
|---|---|---|
| PROCEDURAL (TRM) | allo ITT 13% (2/15; 95% CI 1.7-41); allo first remission 0% from TBI toxicity (0/10; CI 0-31) or 10% counting the d19 GDV death (1/10; CI 0.3-44); auto 7.4% (7/94; CI 3.0-14.7), 8.3% (2/24), 13% (2/15). Keep the existing profile `total body irradiation + transplant` (procedural 0.85, marrow 0.60) | 35789057; 38695516; 22882500; 24467413 |
| MARROW | all dogs grade 4 neutropenia (mean day 6), ANC >1000/uL at day 9-18 (mean 11); grade 3-4 thrombocytopenia in all, platelet recovery delayed (11/15 got platelet products); stem-cell rescue is what makes this axis survivable: model the graft as a marrow-axis modifier, not an agent | 35789057 s4.3 |
| IMMUNE_MEDIATED (GVHD) | acute grade 2 skin 3/13 (23%), none grade >=3, no liver/GI GVHD reported, chronic 0/13; human matched-sibling comparators quoted in the paper: 38% acute, 33% chronic. Suggested fraction of axis: 0.30 central (low 0.10 dog, high 0.60 human-like) | 35789057 s4.5, s6 |
| Cyclosporine / other | diabetes (1/15), Factor V inhibitor (1/15); cyclosporine ~30 d | 35789057 s4.6-4.7 |
| GI | no grade 4 GI AE in allo (2 x 4 Gy at 7.5-10 cGy/min) vs 8 grade-4 anorexia and parenteral nutrition in 8 dogs in the cited auto series; auto 14/15 GI AE (T-cell series) | 35789057 s4.3; 24467413 |
| Late | second cancer (1/15 T-cell auto, 1 dog); TBI-associated malignancy ~5x relative risk in radiation chimeras (PMID 6355021, in record; their dose 6.1-21.3 Gy, higher than 2 x 4 Gy); pulmonary fibrosis 1/24 | 24467413; 22882500 |
| Time | course 14-30 d on the procedural axis; GVHD vigilance to ~d100; not repeatable (reversible = False in the existing profile) | |

### 7.4 Rescue and add-on objects
- DLI rescue: cryopreserved donor CD3+ aliquots (1-2 x 10^? cells/kg, 2-3 doses). Outcome series NOT FOUND (dog); human: FL 77% response (PMID 20606089), PTCL 66% (PMID 21904377), DLBCL 60% responses to IS withdrawal/DLI (PMID 18684698). Timing: not within 3 weeks after transplant (fatal GVHD in DLA-identical/haplo dogs; PMID 19446000). Grade TRANSFER. Not a separate potency; a re-arming of the same effector.
- HSC rescue graft: no potency; marrow-axis modifier; CD34+ >= 2 x 10^6/kg engraftment threshold (24467413: "More than 2 x 10(6) CD34+ cells/kg were harvested from 15/15 dogs"; allo mean 8.0 x 10^?/kg (exponent lost in text; see section 1.1)).

### 7.5 Combinability (design logic; grade: all TRANSFER or ASSUMED unless a PMID is given)
| Partner | Combinable? | Basis and conflict |
|---|---|---|
| CHOP induction | yes, standard (every transplanted dog) | 35789057 s2.1 |
| Anti-CD20 antibody / CD20 CAR-T | yes in principle; orthogonal escapes (antigen-directed arm closes MHC-loss, graft closes antigen-loss) | human RIC allo with rituximab: 40 CLL pts, 5-y OS 55%, rituximab protective for GVHD (p = 0.02) and for OS/EFS (PMID 23089183). Canine: expanded autologous T cells after TBI-auto gave no benefit (PMID 34950726), so no synergy is credited; CAR-T persistence 14-50 d (record) |
| Vaccines (minor-H or tumour) | yes, after cyclosporine ends and T cells reconstitute (>= ~day 60) | canine miHA vaccine regimen in DLA-matched HCT model: antigen-specific CD4/CD8 responses; DLI changed chimerism in 1/3 recipients with no GVHD (PMID 25965411, abstract only). Timing constraint from the 10-week immune impairment after TBI-auto (record) |
| Checkpoint blockade | candidate to boost GVL: review notes PD-L1 on canine lymphoma lines (PMID 34390541 FT, citing Shosu); GVHD risk in the transplant setting not verified here | ASSUMED/TRANSFER, no PMID for risk |
| Targeted inhibitors (BTK, BCL2, XPO1) | post-engraftment maintenance; additive marrow axis; no data on T-cell/GVL interaction retrieved | NOT FOUND (interaction) |
| Radiation consolidation (HBRT) | replaces rather than adds: HBRT 6 Gy x2 halves + TBI both draw on marrow/GI; no stacking above ~10 Gy-equivalent | OUTCOME (no escalation benefit) |
| CNS-directed drugs (thiotepa/BCNU/busulfan HDC) | can replace TBI in the AUTO arm (conditioning with CNS-penetrant alkylators); in the allo arm = research | record SWEEP_cnsregimens s1, s8; canine thiotepa PK NOT FOUND |
| DLI | yes, rescue | section 7.4 |

### 7.6 Availability tier (dogs today)
allo DLA-identical HCT: exists-today (off-label procedure in client-owned dogs; specialty-centre-limited, donor-limited: 25% per sibling, no registry, NCSU paused since early 2023, Bellingham/MedVet/VCA West LA reported as performing; US$25-45k). Auto TBI-HCT: exists-today, same centres. Haploidentical, RIC allo, DLI-for-relapse series, MSC-for-GVHD, drug-conditioned CNS-targeted HCT: to-build / research.

### 7.7 Closure statement for the transplant arm as a decidable conjunction (rule 12; scope = canine multicentric B-cell lymphoma, first remission, DLA-identical donor; "closed within this catalogue of one transplant agent against the 23-escape set, at OUTCOME/TRANSFER strength")
| Condition | Status | Strength |
|---|---|---|
| effective kill number exists and has a stated basis | CLOSED | OUTCOME (n = 9 evaluable dogs, CI 0.52-0.997) + human corroboration |
| P-gp/efflux escape reached | CLOSED | TRANSFER (mechanism, chemo-refractory outcomes) |
| CD20/CD19 loss reached | CLOSED | TRANSFER |
| dormant/non-cycling cells reached | CLOSED at TRANSFER strength | TRANSFER (human low-proliferation tumours) |
| apoptosis-evasion escapes reached | CLOSED by mechanism | TRANSFER |
| MHC-I/II loss reached | OPEN | no agent in the transplant arm reaches it (NK missing-self unproven) |
| CNS sanctuary reached | CLOSED at access 0.5 (0.25-1.0) | TRANSFER (n = 20) |
| testis/eye sanctuaries | OPEN (not assessed) | NOT FOUND |
| toxicity affordable | CLOSED within the budget above (TRM 13% ITT; 0-10% first remission) | OUTCOME |
| effect lasts >= 2 y / >= 4 y | CLOSED (8/9 dogs > 4 y) | OUTCOME; n = 9 |
| effect lasts 10 y | NOT DECIDABLE from dog data: bound hazard <= 0.18/yr (95%), 0 events after year 1 | OUTCOME bound only; second-cancer and lifespan competing risks |
| donor + centre obtainable | CONDITIONAL (25% per sibling; centre availability reduced) | availability, not science |

## 8. Searched and NOT found (this session; search tool misparsed several long queries, so absence is of what was retrievable)
- Canine: KM numbers at 1-5 y for allo/auto (only medians and figures); relapse site (nodal/CNS/marrow) after HCT; any CNS relapse rate after canine HCT; post-transplant MRD; Colorado State transplant series; purging study; DLI-for-relapse outcome series; individual follow-up lengths of the 6 living allo dogs; T-cell lymphoma allo series; fraction of lymphoma dogs with an eligible relative; NCSU program status after 2023.
- Mechanism: direct assay of CTL/NK killing of P-gp-expressing lymphoma cells; direct assay of GVL against quiescent lymphoma cells; donor T-cell content of CSF after allo; frequency of MHC loss/down-regulation after allo in LYMPHOMA (data found are myeloid); TP53-stratified allo outcome.
- Human: AATT median follow-up and relapse-free 10-y fraction; human long-term (>= 10 y) relapse hazard after allo for lymphoma; Mika 2019 PCNSL allo (PMID 31399528) has no abstract or full text, so its numbers are not used.
- Discrepancies inside sources, unresolved: Gareau 2021 "four cured dogs" OS range 86-1317 d vs the >= 2 y definition; Warry relapse counts sum to 12 of 13; Gareau 2022 first-remission DFI range 268-2290 vs OS range 268-2920; the "27 first-remission dogs" comparator split is not itemised.

## 9. Verified citation table (every PMID below was fetched with get_article_metadata in this session unless marked "record")
35789057 (10.1111/vco.12847, FT PMC9796125); 24467413 (10.1111/jvim.12302, FT PMC4857993); 34950726 (10.3389/fvets.2021.787373, FT PMC8688351); 22882500 (10.1111/j.1939-1676.2012.00980.x, abs); 22620705 (10.2460/ajvr.73.6.894, abs); 24762013 (10.2460/ajvr.75.5.425, abs); 34390541 (10.1002/vms3.601, FT PMC8604109); 42525883 (10.1093/jvimsj/aalag144, FT PMC13419073); 26279153 (10.1111/vco.12163, abs); 21320018 (10.2460/javma.238.4.480, abs); 39270145 (10.1200/JCO.24.00554, abs); 34293518 (10.1016/j.jtct.2021.07.015, abs); 25371177 (10.1038/leu.2014.314, abs); 30380364 (10.1056/NEJMoa1808777, abs); 19641204 (10.1056/NEJMoa0811036, abs); 18684698 (10.1093/annonc/mdn404, abs); 21904377 (10.1038/leu.2011.240, abs); 20606089 (10.1200/JCO.2009.26.9100, abs); 30467838 (10.1111/bjh.15685, abs); 20107156 (10.3324/haematol.2009.017608, abs); 22955330 (10.1038/leu.2012.228, abs); 21455998 (10.1002/cncr.26091, abs); 23089183 (10.1016/j.exphem.2012.10.008, abs); 39098011 (10.11406/rinketsu.65.622, abs, n = 1 case); 25965411 (10.1097/TP.0000000000000744, abs); 12931117 (10.1016/s1083-8791(03)00148-4, abs); 19446000 (10.1016/j.exphem.2009.05.001, abs); 8490811 (no DOI, abs). Record-verified (earlier sweep, not re-fetched): 16506937, 6355021, 27257868, 3009370, 31146304, 38695516, 16594594, 19747631, 10534062, 20816818, 23723082, 21781170, 8605371, 11719387, 3887690, 3901841, 400683. Web: WRAL 2023 (wral.com/story/lives-depend-on-it-families-fight-for-access-to-life-saving-vet-procedure-at-nc-state/20742385), change.org petition 2023-02-19, bhamvet.com/service/bone-marrow-transplant, Whole Dog Journal / DogCancer.com / Seattle Times cost figures (secondary).

## 10. Bottom line (strength stated)
1. Transplant is now a model input, not an exclusion. The allograft effect is OUTCOME-calibrated: net 2.6 e-folds (0.65-4.2) over a 166-day window (0.016 /d net; 0.106 /d gross vs growth 0.0903), with human AATT (2.26 e-folds allo-over-auto) as TRANSFER corroboration. Auto TBI-HCT adds 1.12 e-folds (0.2-1.6) over CHOP alone, consistent with the in-vivo-corrected radiobiology (0.56-1.94 for 2 x 5 Gy).
2. It closes P-gp, CD20/CD19 loss, dormancy (at TRANSFER strength), apoptosis evasion and, at reduced access (0.5), the CNS; it does not close MHC loss; testis/eye unassessed.
3. Cost: TRM 13% ITT (0-10% first remission), mild GVHD in 23%; donor 25% per sibling; centre-limited, NCSU paused; US$25-45k.
4. Weak points that are statistical, not "undemonstrated": n = 9 evaluable dogs (CI 0.52-0.997), historical controls, no 10-year denominator.
