# CAR-T in-vivo kill rate and canine translation: verified research report

Date 2026-10-01. Scope: canine multicentric lymphoma durable-response model. Output of the `SWEEP_cart_kill` task.

## 0. Criteria, method, grading

User's success criteria, verbatim: "make sure every mechanism and every escape is closed by either real data or rigorous model, potency, toxicity etc all need to be considered"; "looking for 10+ years of durability"; "assuming early detection"; "I'm okay with no specific data but if scientifically sound" (transfer allowed if justified in writing, graded TRANSFERRED; no basis = ASSUMED); "keep going by more research or modeling to fully close every mechanism and escape then. I know car t has human results for CNS". Not graded against "demonstrated in dogs" (the user knows that is unmet).

Method. Every PMID below was fetched back from PubMed: titles/journals/DOIs by MCP `get_article_metadata` (first batch) and NCBI esummary (same PubMed record, used for bulk checks); abstracts via Europe PMC (PubMed abstract text); full-text numbers/tables from PMC / Europe PMC XML. Where only an abstract could be read this is stated. "DERIVED" = my arithmetic from the quoted numbers (shown). "NOT FOUND" = searched, absent. The PubMed MCP full-text tool strips equations and tables, so tables were read from the Europe PMC/PMC XML instead.

Grades used: MEASURED (in the target species/disease), TRANSFERRED (other species/disease, transfer justified), MODEL (rigorous model fit to data, parameters weakly identified), ASSUMED (no basis).

Repo context checked first: `docs/LYMPHOMA_STATUS.md` records CD20 CAR-T = 0.12 /day ASSUMED, canine persistence "about 14 to 50 days", CNS access 0.5 ASSUMED, and the two launched sweeps (`SWEEP_cart_human`, `SWEEP_cart_kill`). This report is the kill/dog/dosing half. Nothing here contradicts the recorded 14-50 day dog persistence; it is corroborated (section D).

---

## A. Mathematical / PKPD models of CAR-T killing in patients (and the animal/in-vitro anchors)

| PMID | DOI | Paper | Setting | Verbatim numbers | Grade/caveat |
|---|---|---|---|---|---|
| 33757357 | 10.1098/rspb.2021.0229 | Kimmel, Locke, Altrock 2021, Proc Biol Sci | human LBCL, ZUMA-1 axi-cel | Eq 2.3 (PMC XML): dB/dt = rB*B - gammaB*B*C/(kB + C). Table 1: "tumour-killing rate (by effector CAR) gammaB 1.15 x 10^0 day-1, quartile range [0.64, 1.35] x 10^0"; "killing rate saturation parameter kB 2.024 x 10^9 cells [1.40, 3.125] x 10^9"; "initial CAR T cell number C(0) 1.80 x 10^8 cells"; "initial median tumour cell number B(0) 9.486 x 10^10"; tumour growth "rB (1-50) x 10^-2 day-1". "seven parameters ... 11 data points ... and one measurement for the tumour state at day 30". "Strong Pearson correlations between kB and rB (0.94), and between kB and gammaB (-0.96) ... not identifiable". "Most stochastic simulations resulted in cure between days 20 and 80". CAR counts (Moffitt, cells/uL): 27.5 (d7), 9.1 (d14), 2.1 (d28), 0.1 (d90). | MODEL, human. Weakly identified (one tumour time point). It is a MAXIMUM saturating rate. |
| 33565700 | 10.1002/psp4.12598 | Singh et al 2021, CPT PSP, bb2121 anti-BCMA bench-to-bedside | human myeloma | "KKillMax ... 0.353 (14) 1/hour" in vitro; preclinical in vivo "0.612 (28.2) 1/day"; clinical: "KKillMax was estimated to be 0.343 1/day (2-day half-life), which was < 2-fold higher than the preclinical estimate"; KC50 "~2.24 CAR-Target complexes per tumor cell"; tumour growth KgTumor "0.008 (Fixed) 1/day"; "Unlike preclinical TGI studies, the direct tumor cell depletion data set was unavailable in the clinical settings" (readout = M-protein) | MODEL, human. Readout is M-protein (lag, long half-life) so the true kill may be higher. |
| 31852337 | 10.1080/19420862.2019.1688616 | Singh et al 2020, mAbs, multiscale PK-PD | mouse xenografts, in vitro | in vivo KkillmaxCAR-T "0.0486 (BCMA) / 0.093 (CD19) / 0.009 (HER2) / 0.0323 (EGFR)" 1/h; tumour exp growth "0.00305 / 0.00473 / ... 0.00367" 1/h; transit time tau "21.6 (BCMA), 56.6 (CD19)" h; in vitro KKillMax "EGFR CAR-T 1.89 1/h; HER2 CAR-T 0.09 1/h" | MEASURED in mice (immunodeficient). DERIVED conversion: 0.0486/h = 1.17/day; 0.093/h = 2.23/day; 0.0323/h = 0.78/day; 0.009/h = 0.22/day. Hill-saturated maxima. |
| 30848084 | 10.1002/psp4.12388 | Stein et al 2019, tisagenlecleucel cellular kinetics | human paediatric/young-adult B-ALL | "The doubling time, initial decline half-life, and terminal half-life for tisagenlecleucel were 0.78, 4.3, and 220 days" | MEASURED/MODEL (CAR-T pool, not tumour) |
| 31937234 | 10.1098/rsif.2019.0734 | Sahoo et al 2020, CARRGO | in vitro glioma | "CAR T-cell dose correlates inversely with the killing rate and correlates directly with the net rate of proliferation and exhaustion" | per-cell kill falls as E:T rises: supports a saturating, not constant, rate |
| 36428671 / 34198713 / 40203243 / 34208323 / 39191245 | 10.3390/cancers14225576 / 10.3390/ijms22126371 / 10.1371/journal.pcbi.1012908 / 10.3390/cancers13122941 / 10.1063/5.0206341 | Paixao 2022; Martinez-Rubio 2021; Santurio 2025 (25 patient time courses); Barros 2021; Serrano 2024 | human ALL/lymphoma models | abstracts only read; no per-cell kill constant extracted | NOT MINED for numbers; listed so the search is on record |
| 26872694 | 10.1016/j.immuni.2016.01.010 | Halle et al 2016, Immunity | mouse CD8 CTL, two-photon | "On average, one CTL killed 2-16 virus-infected cells per day as determined by real-time imaging and by mathematical modeling." | MEASURED, mouse, TCR-driven, not CAR. Gives the per-effector cap used in the mechanistic cross-check below. |
| 21832238 | 10.1126/scitranslmed.3002842 | Kalos et al 2011, Sci Transl Med | human CLL | "each patient had on the order of 10^12 CLL cells (that is, about 1 kg of tumor load)"; UPN 03 "infused with only 1.4 x 10^7 CART19 cells ... no CLL cells were detectable after treatment, we achieved a marked 1:93,000 E/T ratio ... 1:2200 and 1:1000 ... for UPN 01 and 02"; "serial killing ... combined with in vivo CART19 expansion of >1000-fold"; mouse comparator "2.2 x 10^7 CAR T cells could eradicate tumors composed of 1 x 10^9 cells ... E/T ratio of 1:42" | MEASURED, human. Effective E:T is infusion-based (expansion ignored). |
| 21830940 | 10.1056/NEJMoa1103849 | Porter et al 2011, NEJM | human CLL | "expanded to a level that was more than 1000 times as high as the initial engraftment level"; tumour lysis syndrome ~day 14-19; "persisted ... at least 6 months, with a decay half-life of 34 days" (marrow) | MEASURED, n=1 |

NOT FOUND: a published per-CAR-T-cell in-vivo kill rate constant (kills/CAR-T/day) for patients. The literature gives saturating population rates (above) and E:T arithmetic, not a per-cell constant. Searched: PKPD/mathematical model + chimeric antigen receptor + killing/kinetics/tumor burden (PubMed, ~10 query forms); Hardiansyah/Ng, Liu 2021 CPT (PMID 33002189 exists: "Model-Based Cellular Kinetic Analysis of Chimeric Antigen Receptor-T Cells in Humans", full text not retrievable here, not mined).

### A1. Derived cross-checks (all DERIVED by me)
1. Reading the existing 0.12/day inside Kimmel's saturating form: gamma*C/(kB+C) = 0.12 when C = 0.12*2.024e9/(1.15-0.12) = 2.4e8 cells, i.e. essentially the INFUSED dose (C(0)=1.8e8, giving 0.094/day) with NO expansion. Kimmel per-capita kill at other pool sizes: C=1e9 -> 0.38/day; 2e9 -> 0.57/day; 5e9 -> 0.82/day; 2e10 -> 1.04/day; 7e10 -> 1.12/day. In patients the pool expands >1000-fold (Porter), so the human number is the saturated one (0.4-1.1) not 0.12.
2. Mechanistic cap (per-effector kill x E:T, linear regime): Halle 2-16 kills/CTL/day x E:T. 0.12/day needs E:T = 0.06 (at 2/day) to 0.0075 (at 16/day). E:T of 0.1 gives 0.2-1.6/day. Human peak E:T is plausibly >0.01 (Kimmel carrying capacity KC 6.96e10 vs B(0) 9.5e10), so 0.12 is the bottom of the mechanistic envelope. TRANSFERRED (mouse virus-CTL to CAR-T is a stretch; CARs may kill faster or slower per cell).

---

## B. Clinical tumour-decline kinetics after CAR-T (lymphoma, ALL, CLL)

| PMID | DOI | Data (verbatim) | Derived rate |
|---|---|---|---|
| 36584673 | 10.1016/j.ccell.2022.12.005 (Sworder 2023 Cancer Cell, axi-cel LBCL, ctDNA) | "on the day of CAR19 T cell infusion ... (median, 540.4 versus 11.8 hGE/mL [progressors vs ongoing responders])"; "1 week (median 30.4 versus 0.12 hGE/mL, p = 0.003) and at 4 weeks (median 7.2 hGE/mL versus not detected, p < 0.001)"; "MMR; 2.5 log10 ctDNA fold decrease [week 4] ... significantly superior outcomes (p < 0.001)" | responders: 11.8->0.12 = 1.99 log10 in 7 d = 0.66/day NET; progressors: 540->30.4 = 1.25 log10 in 7 d = 0.41/day NET; progressors wk1->wk4 30.4->7.2 = 0.07/day (rate collapses after week 1, i.e. escape/exhaustion); MMR threshold 2.5 log in 28 d = 0.21/day |
| 34133196 | 10.1200/JCO.21.00377 (Frank 2021 JCO, axi-cel, VDJ ctDNA; abstract only) | "Twenty-three of 33 (70%) durably responding patients versus 4 of 31 (13%) progressing patients demonstrated nondetectable ctDNA 1 week after axi-cel infusion"; "All durably responding patients had undetectable ctDNA at or before 3 months" | in durable responders ctDNA reaches the assay floor within 7 days |
| 38443094 | 10.1136/jitc-2023-008450 (JITC 2024, n=23 r/r LBCL, CAR19) | "median ctDNA concentration was 2.23 ... Log hGE/mL" pre; "dropped rapidly to 1.01, 0.93, 0.97, and 0.24 Log hGE/mL at D14, D28, D60, and D90"; ctDNA- at D14: 3-month CR 77.8% vs 11.1% | 1.22 log10 by D14 = 0.20/day (floor-limited: LOWER bound); D14->D90 0.05/day |
| 25319501 | 10.1016/S0140-6736(14)61403-3 (Lee 2015 Lancet, NCI paediatric ALL) | "Response assessment was done on day 28 ... MRD negative ... less than 0.01% marrow blasts"; "12 of 20 patients with B-ALL achieving MRD-negative complete response"; "peak expansion occurring around day 14 ... coincided with disappearance of circulating blasts in responding patients"; circulating B cells "nadired between days 14 and 28" | blasts gone from blood by ~day 14 |
| 25317870 | 10.1056/NEJMoa1407222 (Maude 2014 NEJM, CTL019 ALL) | "Twenty-seven of 30 patients (90%) were in a morphologic complete remission at the first assessment 1 month"; MRD negative in 22 | MRD-negativity assessed at day 28; time-to-MRD-negativity per patient NOT FOUND |
| 21832238 / 21830940 | (above) | CLL, ~10^12 cells to no detectable CLL; tumour lysis day 14-19, CR ~3 weeks | DERIVED: >=3 log in <=28 d = >=0.25/day average; 6 log in 28 d = 0.49/day |
| 32702097 | 10.1182/bloodadvances.2020001900 | MTV cutoff 147.5 mL: low MTV "superior OS (HR 0.25; 95% CI 0.10-0.66) and PFS (HR 0.40; 0.18-0.89)", validated (OS HR 0.14, PFS 0.29) | early detection / low burden helps (supports the "assuming early detection" premise) |
| 29385376 | 10.1056/NEJMoa1709919 (Park 2018 NEJM, adult ALL) | "Patients with a low disease burden ... median overall survival was 20.1 months" vs 12.9 months whole cohort; severe CRS 26% | burden effect |

DERIVED ALL arithmetic: marrow blasts 50% -> MRD<0.01% is 3.7 log10 (ln 8.5); in 28 d = 0.30/day; if compressed into the ~14 d around peak expansion = 0.61/day. These include lymphodepleting chemotherapy (Flu/Cy), which has its own activity; none of the numbers isolates CAR-T from LD, and ctDNA is a shedding proxy (cfDNA half-life is short), so ctDNA slope is an apparent burden slope, not a cell count.

Time to nadir (verbatim/derived): CAR-T expansion doubling time 0.78 d, peak ~day 10-14 (Stein, Lee); blasts/ctDNA nadir within 1-4 weeks; cure events "between days 20 and 80" (Kimmel model); canine dog: CAR-T peak day 3, below detection day 14 (Atherton 2022).

NOT FOUND: serial LDH half-life after CAR-T; per-patient serial-PET log-reduction per week; a clinical paper giving "tumour burden half-life after CAR-T" as a number. Searched PubMed (LDH/ctDNA/MTV/tumor-burden x kinetics x CAR-T x lymphoma).

---

## C. Does CAR-T kill non-dividing / slowly dividing targets?

| PMID | DOI | Evidence (verbatim) | Reading |
|---|---|---|---|
| 15711642 | 10.1172/JCI23409 (Messmer 2005 JCI) | "birth rates ... varying from 0.1% to greater than 1.0% of the entire clone per day" in CLL | CLL is mostly non-cycling: premise for the next row |
| 21832238 (Kalos) | above | ~10^12 CLL cells eradicated, no detectable CLL by ~1 month | DERIVED inference: at <=1%/day birth rate at most ~25% of the clone could pass through S phase in 28 days, yet >99.9% was cleared, so killing cannot be confined to cycling cells. Inference, not a direct measurement. |
| 35110735 | 10.1038/s41586-021-04390-6 (Melenhorst 2022 Nature) | CD19 CAR T cells "remained detectable more than ten years after infusion, with sustained remission in both patients" (CLL) | persistence + remission at 10 y, n=2 |
| 36109639 | 10.1038/s41591-022-02017-5 (Mackensen 2022 Nat Med, lupus) | anti-CD19 CAR T "led to deep depletion of B cells"; B cells reappeared "after a mean (+/-s.d.) of 110 +/- 32 d" | normal resting/memory B cells (largely non-cycling) are depleted in humans |
| 32555459 | 10.1038/s41586-020-2403-9 (Amor 2020 Nature) | senescence "characterized by stable cell-cycle arrest"; uPAR CAR T cells "efficiently ablate senescent cells in vitro and in vivo" | MEASURED in mice: CAR-T kills cell-cycle-arrested cells in vivo |
| 38194912 | 10.1016/j.ccell.2023.12.011 (Correia 2024 Cancer Cell) | dormant disseminated tumour cells persist because of "scarcity of interactions"; "overcome by ... adoptive transfer of T cell receptor or chimeric antigen receptor T cells. Each approach achieves robust DTC elimination" | MEASURED in mice: dormant cells are killable once effectors are numerous |
| 30514753 | 10.1158/0008-5472.CAN-18-1078 | IL1RAP CAR T cells "exhibited cytotoxicity against both leukemic stem cells" (quiescent CML stem cells) "in vitro and in a xenograft murine model" | in vitro/mouse |
| 9620169 | (J Cell Biochem 1998; DOI not returned) | "arrest of the cell cycle at the G1/S interface markedly reduced the susceptibility of target cells to perforin-mediated lysis ... Susceptibility to lysis by intact CTLs was not affected significantly" | counter-evidence at the granule level, but intact effector killing unaffected |
| 11380680 | 10.1046/j.1440-1711.2001.01008.x | alloreactive CTL killing "independent of p34cdc2 kinase"; cell-cycle-arrested targets showed "enhanced 51Cr release" via Fas | killing does not need cycling |
| 35447074 | 10.1016/j.cell.2022.03.033 (Baldominos 2022 Cell) | in TNBC "tumor cells that resist T cell attack are quiescent ... form clusters with reduced immune infiltration ... hypoxic immune-suppressive milieu" | COUNTER-evidence: quiescent cells can resist endogenous T cells via a niche |
| 29466757 | 10.1016/j.immuni.2018.02.001 (Agudo 2018 Immunity) | "quiescent stem cells in the hair follicle and muscle were resistant to T cell killing ... systemic downregulation of the antigen presentation machinery, including MHC class I" | COUNTER-evidence for TCR/MHC-I-dependent killing; a CAR is MHC-independent, so this mechanism should not apply, but that is an inference |
| 27015306 | 10.1016/j.cell.2016.02.025 (Malladi 2016 Cell) | latent cancer cells evade immunity (NK) via autocrine WNT inhibition | NK-specific; not CAR |

Net: the kill is not cell-cycle dependent in the clinical CLL/B-cell-aplasia/senescence data; the failure modes seen for quiescent cells (MHC-I loss, hypoxic niche, scarcity of effectors) are access/number problems, not an intrinsic inability of CAR-T to kill G0 cells. NOT FOUND: a direct head-to-head measurement of CAR-T killing of G0 vs cycling lymphoma cells in vitro (searched PubMed: chimeric antigen receptor x quiescent/dormant/cell cycle/G0/slowly proliferating); no data from dogs.

---

## D. Canine CAR-T (all published studies found)

| PMID | DOI | Design / antigen | Verbatim key facts | Role |
|---|---|---|---|---|
| 27401141 | 10.1038/mt.2016.146 (Panjwani 2016) | CD20, first-gen zeta, mRNA (transient), 1 dog with relapsed B-cell lymphoma (abstract only; full text unavailable) | "Treatment was well tolerated and led to a modest, but transient, antitumor activity, suggesting that stable CAR expression will be necessary for durable clinical remissions" | first-in-dog |
| 32002286 | 10.1080/2162402X.2019.1676615 (Panjwani 2020, Penn) | CD20, lentiviral; 4 dogs CD28-zeta, 1 dog BB-zeta; DLBCL | "A first-in-species trial of five dogs"; "Circulating CAR T cells were detectable post-infusion, however, induction of canine anti-mouse antibodies (CAMA) was associated with CAR T cell loss"; "selection pressure on CD20+ tumors ... culminating in antigen escape"; doses CAR T/kg "0.97x10^5, 0.28x10^5, 6.60x10^5, 5.01x10^5" vs target 10^6; surface CAR 1.51-6.62% of CD5+; pre-conditioning busulfan 4 mg/kg or cyclophosphamide 50 mg/m2 PO x4; "all dogs required rescue chemotherapy for disease progression within one month" except 429-003; CAR copies low and "could not be detected after day 28"; BB-zeta dog (429-006): 2.18x10^6 T cells/kg (~10^5 CAR/kg), CAR peaked in node day 50 then disappeared, CAMA from day 18 peaking day 50, euthanized day 182; "survival did not correlate with total T cell dose or CAR T cell dose" but with ex vivo doublings; "'Caninization' of the scFv represents a potential future approach to prevent the induction of CAMA" | the only multi-dog efficacy dataset |
| 35898541 | 10.3389/fvets.2022.824982 (Atherton 2022) | CD20 BB-zeta lentiviral, 1 dog, cyclophosphamide 500 mg/m2 IV 4 d before | "CAR-T cell levels peaked 3 days post-CAR-T administration"; "below the limit of detection on day 14 at which point the lymph nodes were increasing in dimension consistent with relapse"; CRS grade 2: IL-6, MCP-1, IFNg, IL-10 rose at/after peak | PK in dog + CRS occurs. Nodal shrinkage by day 3 is CONFOUNDED by the cyclophosphamide given 4 d earlier. |
| 41376156 | 10.1016/j.ymthe.2025.12.010 (Mol Ther 2026) | canine CD20 CAR; cBBz vs human BBz vs c28z; NSG xenograft of canine leukaemia | "In a first-in-canine trial, anti-CD20 CART with canine 4-1BB-CD3z (cBBz) domains induced CD20-negative lymphoma outgrowth but did not persist or deplete B cells"; "CART therapeutic efficacy in dogs has not yet been achieved"; hBBz "greater cytolysis and CD8 T cell outgrowth" via FcepsilonRgammaI; mouse model 3.5x10^6 CAR+ cells, "elimination of canine GL1 leukemia" with hBBz; "hBBz demonstrates 83% sequence identity to cBBz"; authors flag possible "immunogenicity of human sequences in canine CARTs" | canine-specific costimulation barrier; solution only shown in mice |
| 42480604 | 10.1158/1535-7163.MCT-26-0365 (Mol Cancer Ther 2026) | tandem CD19/CD20 canine CAR, in vitro | "We previously reported CD20 loss in canine DLBCL patients treated with CD20-specific CAR T cells"; "TCAR-engineered canine T cells effectively and specifically eliminate cells expressing CD19 and/or CD20" | antigen-escape countermeasure, in vitro only |
| 39314237 | 10.1016/j.isci.2024.110863 | PD-1/CD28 chimeric switch receptor in canine CAR-T | in vitro; "paves the way for in vivo studies" | exhaustion |
| 32329214 | 10.1111/vco.12602 | CD20 CAR manufacturing (Japan) | "more than 70% transduction efficiency" retroviral RetroNectin; in vitro cytotoxicity only | manufacturing |
| 35241532 / 34408098 / 33087808 / 34746864 | 10.21873/invivo.12763 / 10.1292/jvms.21-0326 / 10.1038/s41598-020-74927-8 / 10.1016/j.xpro.2021.100905 | culture conditions (ConA memory, Akt inhibitor); anti-canine-CD20-CAR detection mAb; qPCR cellular kinetics in copies/uL; retroviral protocol "CAR expression is typically higher and more stable compared with previous protocols" | manufacturing/PK tooling |
| 35405743 | 10.1158/1535-7163.MCT-21-0726 | B7-H3 CAR T (human MGA271 scFv cross-reactive), 2 purpose-bred healthy dogs after "cyclophosphamide and fludarabine" | "No severe adverse events were observed" | Flu/Cy lymphodepletion tolerated in dogs |
| 38554158 | 10.1007/s00262-024-03642-4 | B7-H3 +/- CXCR2 canine OS, mouse xenograft | "little anti-tumor activity ... B7-H3 CAR T cells; whereas B7-H3-CXCR2 ... complete tumor elimination in most treated mice" | solid tumour, mouse |
| 36765608 | 10.3390/cancers15030648 | anti-HER2 CAR-TIL, 4 companion dogs (melanoma) | "tolerable and showed signs of anti-tumor activity" | dog safety |
| 30306125 | 10.1016/j.omto.2018.08.002 | IL13Ra2 CAR, canine glioma line and "orthotopic model of canine glioma" (xenograft) | planned dog trial; no dog CNS dosing reported | the nearest dog-CNS item; NOT a dog CNS result |
| 41847725 / 32081102 | 10.1111/vco.70061 / 10.1177/0300985819900352 | canine CD19 binders (rabbit mAb; CD19 mAb + scFv) | CD19 CAR gene HUA-1 in Jurkat cells only | CD19 binders exist; no in-dog CD19 CAR-T found |
| 37852175 | 10.1016/j.xcrm.2023.101241 | allogeneic iNKT cells in MHC-mismatched dogs | "remain detectable for at least 78 days" without MHC ablation | only allogeneic-effector persistence datum in dogs (not CAR-T, not lymphoma) |
| 38573683 / 41169235 / 30563208 / 30963322 / 38621412 / 27687136 / 24936037 | CCR 2024 / J Immunol 2025 / Vet Sci 2018 / AAPS J 2019 / JAVMA 2024 / Mol Ther 2016 / ILAR J 2014 | reviews | context only |
| 40734704 | 10.1016/j.omtm.2025.101526 | CDV-pseudotype adapter lentivector, in vivo transduction in human-PBMC NSG mice | not canine in vivo CAR-T despite the name | NOT relevant to dogs |

Canine binders that exist (for the "what is needed" question): rat anti-canine CD20 (4E1-7-B, rat-canine chimeric, plus afucosylated 4E1-7-B_f) PMID 32651429 (DOI 10.1038/s41598-020-68470-9) and its clinical use with CHOP in 13 dogs, PMID 41742528 (10.1093/jvimsj/aalaf039): "All 13 dogs achieved complete response (CR), with a median time to CR of 3 weeks ... B-cell depletion lasted for > 200 days"; rabbit single-domain anti-canine CD20 (PMID 35177658, 10.1038/s41598-022-06549-1); camel VHH-canine chimeric (PMID 41160360, 10.1186/s13568-025-01974-7); canine CD20 six amino-acid variants in patients "C77Y, L147F, I159M, L198V, A201T and G273E" (35177658). CAMA prevalence is breed- and individual-dependent: PMID 31601945 (10.1038/s41598-019-51228-3) "prevalence differed between two dog breeds".

NOT FOUND (searched, absent): any published dog CAR-T efficacy; any dog CAR-T in CNS or CSF; fully canine (caninized) scFv CAR; canine gamma-delta T CAR; canine CAR-NK; canine allogeneic / TCR-edited CAR-T; any in-dog CD19 CAR-T; canine CD22 CAR-T. (PubMed queries: canine/dog x CAR/chimeric antigen receptor x gamma delta, NK, allogeneic/off-the-shelf/CRISPR, anti-mouse antibodies, caninized/fully canine scFv, CD19/CD20/CD22, intrathecal/intraventricular/CSF, glioma, lymphoma CNS.)

---

## E. Human CAR-T for T-cell malignancy: fratricide solutions and CNS

| PMID | DOI | Strategy | Verbatim result |
|---|---|---|---|
| 35500125 | 10.1182/blood.2021014498 | naturally selected CD7 CAR (NS7CAR): CD7 masked/sequestered by the CAR, no editing | 20 pts T-ALL/T-LBL: "Nineteen patients achieved MRD negative complete remission (CR) in the bone marrow by day 28, and 5 of 9 patients achieved extramedullary CR" |
| 39227445 | 10.1038/s41591-024-03228-8 | CD7 CAR + PEBL (protein expression blocker, ER retention) | "16 of the 17 patients attained MRD-negative complete remission within 1 month"; "first patient is in remission 55 months after infusion"; CAR T cells "detectable for 2 years"; regenerating T cells "lacked CD7 expression, were polyclonal" |
| 35435984 | 10.1158/1078-0432.CCR-21-4097 | nanobody CD7 CAR with ER/Golgi-retention | "complete remission (CR) rate was 87.5% (7/8) 3 months"; "median maximum concentration of CAR T cells was 857.2 cells/uL at approximately 12 days and remained detectable up to 270 days" |
| 37314354 | 10.1056/NEJMoa2300709 | base-edited allogeneic CAR7 (CD7, CD52, TCRab edited) | first patient "molecular remission within 28 days"; fatal fungal infection in one of three |
| 40445850 | 10.1182/blood.2025028387 | allogeneic CD7 WU-CART-007 | RP2D composite CR "72.7%" (ORR 90.9%, n=11) |
| 37095094 | 10.1038/s41408-023-00822-w | allogeneic vs autologous CD7 | "Patients treated with allogeneic CAR-T cells had higher remission rate, less recurrence and more durable CAR-T survival" |
| 38145560 | 10.1182/blood.2023022204 | CD5.CAR (CD5 downmodulated, unedited), mature T-cell lymphoma | ORR 44%, CR 2/9; no grade >=3 CRS |
| 39528665 | 10.1038/s41591-024-03326-7 | TRBC1 CAR (spares TRBC2 normal T cells), PTCL | complete metabolic response 4/10, durable >1 year in 2 |
| 42638216 | 10.1002/ajh.70482 | NS7CAR in T-ALL/LBL with CNS leukaemia | TITLE ONLY (no abstract retrievable) |
| 42229585 | 10.1016/j.jtct.2026.05.045 | NS7CAR after allo-HSCT relapse | 21/23 MRD-neg CR; EMD CR 8/13 (61.5%); 3-yr OS 46.4% after second transplant |

Grade for dog T-cell lymphoma: TRANSFERRED, human, no dog data. Fratricide-sparing designs work clinically; all high-response series are heavily consolidated by transplant, so durability of CAR-T alone for T-cell disease is not established (early follow-up, e.g. NS7CAR "median follow-up 142.5 days"; Nat Med PEBL "median follow-up, 15 months", 9 of 11 relapse-free were allotransplanted).

Human CNS involvement with systemic CD19 CAR-T (B-cell): PMID 36260735 (10.1182/bloodadvances.2022008525, meta-analysis 128 patients): PCNSL "56% achieved a complete remission (CR) with 37% remaining in remission at 6 months"; SCNSL 47% CR, 37% at 6 months. PMID 41530773 (10.1186/s13045-025-01761-8, MGH 60 pts): "60% overall response rate (45% complete ...)"; "Median CNS-PFS1 was 4 months"; "Leptomeningeal involvement (LMD) was associated with recurrence after CR"; "peripheral CD19+ B-cell aplasia suggested CD19-CAR persistence in 93% of patients" at progression (so CNS failure occurs with CAR-T still present). In Lee 2015 (PMC7065359): "11 (65%) of 17 patients with B-ALL with CSF specimens adequate for analysis had detectable CSF CAR T cells (median 2790 absolute CAR T cells (IQR 0-23 715)"; "Two patients had evidence of CNS leukaemia at the time of cell infusion that disappeared coincident with a rise in CSF CD19-CAR T cells". PMID 37723652 (10.1111/ejh.14078): late-onset isolated CNS relapses after CD19 CAR-T in LBCL (case series, 3). ZUMA-1 5-year (PMC10646788): "1 event of central nervous system lesion". Interpretation: IV CAR-T reaches CSF and clears CNS disease in a fraction, but CNS durability is poor (median ~4 months) in the CNS-lymphoma populations, which are not early-detection populations.

---

## F. CSF-delivered CAR-T: dose, interval, persistence (human trials, CNS tumours; no CNS-lymphoma intrathecal CAR-T trial found)

| PMID | DOI | Route / schedule | Dose | CSF persistence / kinetics (verbatim) |
|---|---|---|---|---|
| 38454126 | 10.1038/s41591-024-02875-1 (Brown 2024, IL13Ra2, 65 pts) | ICT, ICV, or dual; "three dose schedules of weekly infusions"; DLT window "1 week after the third cycle"; further cycles "no more frequent than once a week" | max feasible "200 x 10^6 CAR-T cells per infusion cycle" (arm 5) | "CAR-T cells were detected in the CSF and TCF for the majority of patients 1 day post infusion ... and, for a subset of patients, >=7 days post infusion ... which is noteworthy since CSF volume turns over approximately four times per day" |
| 39775044 | 10.1038/s41591-024-03451-3 (Vitanza 2025, B7-H3, DIPG, 21 pts) | ICV, "without previous lymphodepletion every 14 days over 8 weeks", then "every 2-4 weeks"; 253 doses total; "multiyear repeated dosing" | 1, 2.5, 5, 10 x 10^7 per dose (MTDR up to 10 x 10^7) | "detected ... in 38.1% (40 of 105) of CSF biospecimens in courses 1 and 2 ... 13 of 18 (72%) evaluable patients having detectable CAR T cells in at least one timepoint. The median peak ... at ... course 2 week 3 post-infusion"; blood vector detected in 2 of 96 samples |
| 40451950 | 10.1038/s41591-025-03745-0 (Bagley 2025, EGFR/IL13Ra2 ICV, 18 pts) | single ICV dose, CSF qPCR days 0,1,4,7,10,14,21,28 | MTD "2.5 x 10^7 cells" | "inflection point seen at Day 5 post-infusion"; cytokines "resolution to baseline levels by day +14"; one patient CAR transgene detectable "at 12 months", another "at 5 months"; "10 (56%) experienced grade 3 neurotoxicity" |
| 38480922 | 10.1038/s41591-024-02893-z (Bagley 2024, intrathecal, 6 pts) | intrathecal single dose | 1 x 10^7 and 2.5 x 10^7 | "substantial CAR T cell abundance and cytokine release in the cerebrospinal fluid were detected in all six patients"; early neurotoxicity |
| 42207176 | 10.1158/1078-0432.CCR-26-0738 (QH104 allogeneic B7-H3 CAR gamma-delta T, intrathecal, 3 pts) | lumbar puncture or Ommaya | "fixed dose of 3 x 10^7 cells per infusion" | "persisted in CSF for at least one week"; CSF cytology converted negative in the 1 patient positive at baseline |
| 39537919 / 38978673 | 10.1038/s41586-024-08171-9 / 10.1101/2024.06.25.24309146 | GD2 CAR sequential IV then ICV (DMG) | not extracted | context |

Model-relevant read-out. Antigen-driven expansion in CSF peaks ~day 5 and cytokine activity returns to baseline by ~day 14 after a single ICV dose; trials re-dose every 7 days (Brown) to 14 days (Vitanza) for the first 8 weeks, then every 2-4 weeks. The "active window" is therefore ~5-14 days per dose and detection falls fast thereafter except in a minority (>=7 d in "a subset"; 12-month persistence in 1 of 18).

NOT FOUND: intrathecal/intraventricular CD19 or CD20 CAR-T for CNS lymphoma/leukaemia (the intrathecal CAR trials are for glioma, DIPG, medulloblastoma, leptomeningeal solid tumours); dog CSF CAR-T kinetics; dog CSF turnover rate in this search.

---

## G. Durability beyond 5 years (human B-cell malignancy)

| PMID | DOI | Verbatim data |
|---|---|---|
| 42341302 | 10.1056/NEJMoa2518035 (NEJM 2026, tisagenlecleucel, single centre, n=38) | "At a median follow-up of 10.1 years (range, 7.9 to 11.5), no relapses had occurred beyond 5.4 years. The 10-year lymphoma-free survival was 32% (95% CI, 14 to 51) among patients with large B-cell lymphoma and 47% (95% CI, 20 to 71) among those with follicular lymphoma"; 10-year PFS 17% LBCL, 29% FL; "10-year non-relapse-related mortality was 18%"; "second primary cancer ... 10-year cumulative incidence, 21%"; "Higher CAR-transgene persistence appeared to be associated with long-term response. B-cell aplasia persisted in 44% of patients with a long-term response" (abstract only; 24 LBCL, 14 FL) |
| 36821768 | 10.1182/blood.2022018893 (ZUMA-1 5-year, n=101; full text read) | "responses were ongoing in 31% of patients"; median follow-up 63.1 months; "5-year OS rate was 42.6%"; 5-year EFS 30.3% (95% CI 21.5-39.6); CR subgroup 5-year OS 64.4%; "Among patients with (n = 62) and without (n = 39) an EFS event by 24 months, 5-year OS rates were 11.3% ... and 92.3% (95% CI, 78.0-97.5)"; "Protracted B-cell aplasia was not required for durable responses" |
| 41252666 | 10.1200/JCO-25-00507 (JULIET 5-year, n=115) | "60-month relapse-free probability was 61% among responders"; "probability of progression-free survival at 60 months was 28%"; OS at 60 months 32% (56% in responders) |
| 33021872 | 10.1200/JCO.20.01467 (Cappell 2020, NCI) | ">3-year duration of response (DOR) were 51% ... for DLBCL/PMBCL 48%, low-grade 63%, CLL 50%"; "Remissions of up to 9 years are ongoing"; peak CAR cells higher with DOR >3 y (98/uL vs lower) |
| 35110735 | 10.1038/s41586-021-04390-6 | CLL, CAR T "detectable more than ten years", two patients in remission |
| 32298202 | 10.1200/JCO.19.03237 (Frey 2020 CLL) | CR 28%, ORR 44% at 4 weeks; PFS 40.2 months in CR |
| 36399695 | 10.1200/JCO.22.00642 (ELIANA 3-yr, paediatric ALL) | "Event-free survival was 44% ... overall survival 63% at 3 years (most events occur within the first 2 years)"; 3-yr RFS 52% censored / 48% not |
| 42036693 | 10.1186/s13045-026-01797-4 (ZUMA-2 5-yr MCL) | median DOR 36.5 months; "5-year incidence of cumulative relapse-related ... mortality 40% (24/60) in responders" |
| 36963592 | 10.1016/j.phrs.2023.106742 | meta-analysis: "pooled prevalence of relapse within the first 12 months ... 61% (95% CI, 43%-78%) ... one year after the infusion ... 24% (95% CI, 11%-42%)" (abstract ambiguous on denominator; use cautiously) |
| 37723652 | 10.1111/ejh.14078 | "Late relapse composed of 1/3 to 1/2 of CAR-T cell therapy failure" (case-series statement), late isolated CNS relapses |
| 40554413 | 10.1182/bloodadvances.2024014995 | in vivo CAR transgene levels in tisagenlecleucel patients (context for persistence) |

Late relapses exist (>2 y) but are a minority; ZUMA-1 shows that 2-year event-free status carries 5-year OS 92.3% (n=39, CI 78.0-97.5), and the 10-year series shows no relapse after 5.4 y (n=38). That supports the user's inference that 2+ years disease-free is a reasonable (not proven) proxy for 10+; the denominator at risk beyond 5 y is small (24 LBCL, 14 FL starting; far fewer remain at risk).

---

# MODEL INPUTS

## (a) Per-day CAR-T kill rate

Definition. Gross per-day kill rate on antigen-positive tumour cells while a functional CAR-T pool is present (tumour growth is subtracted separately; ctDNA slopes below are NET so they under-state gross kill by the growth rate, rB 0.01-0.5/day in Kimmel).

| | rate (/day) | derivation | grade |
|---|---|---|---|
| LOW | 0.12 | Equals Kimmel's saturating kill at an UNEXPANDED pool (C ~ 2.4e8 cells ~ the infused 1.8e8, per-capita 0.094); equals Halle's 16 kills/CTL/day x E:T 0.0075 (or 2/day x E:T 0.06). Bottom of the empirical envelope: median ctDNA fall to D14 gives 0.20/day (floor-limited). So the existing ASSUMED 0.12 is not wrong as a floor; it is the no-expansion value | TRANSFERRED (human model + mouse CTL arithmetic) |
| CENTRAL | 0.35 | Singh 2021 clinical KKillMax 0.343/day (human myeloma, 2-day half-life); consistent with minimum average needed for human ALL/CLL clearance (0.25-0.30/day over 28 d) and with MMR-threshold ctDNA slope 0.21/day (net) and Sworder progressors 0.41/day (net) | TRANSFERRED/MODEL (human) |
| HIGH | 1.1 | Kimmel gammaB 1.15 (range 0.64-1.35) at saturating pool (C > 2e10); mouse xenograft maxima 0.78-2.2/day (Singh 2020); Sworder responders 0.66/day NET + growth | MODEL/MEASURED(mouse) |

Recommended functional form instead of a constant: k(t) = kmax * C(t) / (C50 + C(t)), with kmax 0.34 / 0.7 / 1.15 (low = Singh clinical 0.343; central 0.7 = between Kimmel's lower quartile 0.64 and Singh's preclinical 0.612; high = Kimmel 1.15), C50 = 2.0e9 total CAR-T cells for a ~90 kg human (range 1.4-3.1e9, strongly correlated with kmax, -0.96, so vary them together). Dose in the human trial: C(0)=1.8e8 (2e6/kg). Dog scaling by body mass is ASSUMED (C50 ~ 2.2e7/kg -> ~5.5e8 cells at 25 kg). At the measured canine doses (0.28-6.6e5 CAR/kg, i.e. 7e5-1.7e7 cells at 25 kg) the initial pool is 0.1-3% of that C50, giving per-capita kill 0.0014-0.032/day with kmax 1.15 (0.05/day even at the 1e6/kg target dose, 2.5e7 cells) UNLESS the pool expands. Put the other way (DERIVED, ASSUMED mass scaling): 0.12/day needs a pool of ~6.5e7 cells (~2.6e6 CAR-T/kg at 25 kg), i.e. 4-90x above the doses actually infused, so the ASSUMED 0.12/day already presupposes in-dog expansion that has not been measured. Human pools expand >1000-fold; dog expansion is measured as poor (CAR copies low, undetectable by day 14-28). So the dog value is set by expansion, not by potency: treat "kill rate" as k(C(t)) with a dog C(t) curve (peak day 3-14, gone by day 14-50; Atherton 2022; Panjwani 2020).

Log-kill budget (DERIVED, gross, no regrowth): 0.12/day over 14/28/50 d = 0.73/1.46/2.61 log10; 0.35/day = 2.1/4.3/7.6 log10; 1.1/day = 6.7/13.4/23.9 log10. A residual burden of 1e8-1e10 cells needs 8-10 log10 to reach one cell. With the dog persistence of 14-50 d, only the central-to-high rates AND an expanded pool can close it; at 0.12/day over 14-50 d the CAR-T arm cannot eradicate more than ~2.6 log10 on its own.

Structural finding (important for the durable-response claim). Human data say CAR-T behaves as cure-or-fail within the first ~3 months, not as a slowly acting constant agent: cure "between days 20 and 80" (Kimmel model), ctDNA undetectable by week 1-4 in durable responders, kill rate collapses after week 1 in progressors (0.41 -> 0.07/day), and no relapse after 5.4 y in the 10-y series. So the model should treat CAR-T as a short high-rate pulse that either reaches extinction or leaves a resistant remnant (antigen-loss escape handled elsewhere), followed by a plateau, rather than applying a low constant rate for years.

Weaknesses: kmax and C50 are from one tumour-state time point (Kimmel) and from M-protein (Singh); no per-CAR-cell constant exists; ctDNA is a shedding proxy; all clinical numbers include Flu/Cy lymphodepletion; dog values for kmax are TRANSFERRED with no in-dog tumour decline measurement (the one dog node-shrinkage observation is confounded by cyclophosphamide).

## (b) Kill of non-dividing cells

Grade: TRANSFERRED, supported, moderate. Evidence for: human CLL (birth rate 0.1-1%/day, ~10^12 cells cleared); human normal-B-cell aplasia (lupus, CLL patients); mouse CAR-T kill of senescent (cycle-arrested) cells in vivo; mouse DTC dormancy eliminated by CAR/TCR T cells; in-vitro CTL killing of cycle-arrested targets unaffected. Evidence against / limits: quiescent TNBC cells resist endogenous T cells through a hypoxic niche; quiescent stem cells evade TCR killing by MHC-I loss (not applicable to CARs, inference); G1/S-arrested cells are less sensitive to isolated perforin but not to intact CTLs. Net: use kill independent of cell cycle, with the failure mode being access/effector numbers (scarcity) and niche, not intrinsic resistance. No dog data. Do not assume an additional penalty for dormancy beyond the access factor already in the model.

## (c) Dog-specific barriers and what a canine binder solves

| barrier | evidence | solved by a canine/caninized binder? |
|---|---|---|
| anti-CAR (CAMA) immunity -> CAR loss | Panjwani 2020: "induction of canine anti-mouse antibodies (CAMA) was associated with CAR T cell loss"; CAMA from day 18, peak day 50 (BB-zeta dog) | PLAUSIBLY, not demonstrated: no fully canine/caninized scFv CAR found; binders exist (rat-canine chimeric 4E1-7-B, rabbit sdAb, camel VHH) but all xeno-derived variable regions; costimulatory domain from human would be a second xeno sequence |
| canine costimulatory domain inferior | 2026 Mol Ther: cBBz "did not persist or deplete B cells"; hBBz better in mouse | NO (a binder does not fix signalling); hBBz is the proposed fix but immunogenicity in dogs untested |
| low dose / poor expansion | doses 0.28-6.6e5 CAR/kg; surface CAR 1.5-6.6%; ex-vivo doublings correlate with survival | NO (manufacturing: later retroviral protocols >70% transduction, memory-favouring IL-7/IL-15; Akt inhibition, ConA) |
| antigen escape (CD20 loss) | CD20-negative outgrowth in 2 dogs; CD20 loss | PARTLY: a canine CD19 binder enables tandem CD19/CD20 CAR (in vitro only, 2026); CD19 binders exist (32081102) |
| persistence 14-50 d | CAR undetectable day 14 (Atherton), day 28 (Panjwani node peak d50) | NO (needs signalling + anti-CAR immunity + LD) |
| CRS | grade 2 CRS in a dog, IL-6/MCP-1/IFNg/IL-10; tocilizumab cross-reactivity unknown | NO |
| exhaustion/PD-1 | PD-1/CD28 CSR in vitro | NO |
| efficacy | "CART therapeutic efficacy in dogs has not yet been achieved" (41376156) | n/a |

What a persistence-capable canine CAR-T needs (from the evidence, not yet done in dogs): canine-derived/caninized binder (or a nonimmunogenic format) + human 4-1BB/CD3z (or a canine domain proven equivalent) + IL-7/IL-15 memory-skewed manufacture + full-dose (>=1e6/kg) with Flu/Cy-type lymphodepletion (Flu/Cy tolerated in 2 healthy dogs) + a dual-antigen CD19/CD20 binder. Allogeneic/off-the-shelf: only iNKT (78 d in MHC-mismatched dogs); canine gamma-delta CAR and canine CAR-NK NOT FOUND. Manufacturing feasibility: demonstrated (retro/lentiviral, 12-15 d culture, 22-169x expansion in 3 products; >70% transduction).

## (d) Dosing duty for CSF-delivered CAR-T

From human CSF trials (all TRANSFERRED; antigen/tumour differ; no lymphoma intrathecal CAR-T found; dog CSF kinetics NOT FOUND):
- Dose: 1e7-1e8 cells per infusion (MTD 2.5e7 for EGFR/IL13Ra2 ICV; up to 1e8 per dose B7-H3 ICV; 2e8 per cycle IL13Ra2).
- Interval: weekly x3 (Brown) or q14 days x 8 weeks then q2-4 weeks (Vitanza, 253 doses, multi-year).
- Per-dose active window: expansion inflection ~day 5, cytokine activity back to baseline by ~day 14 (Bagley); detectable >=7 d in "a subset" (Brown); only 38.1% of scheduled CSF samples positive in a q14d regimen (Vitanza).
Suggested duty fraction (fraction of dosing interval with functional CAR-T in CSF), as inputs for the sweep: low 0.15 (q14d, detection in ~38% of samples incl. pre-dose troughs), central 0.4 (q14d, ~5-6 day active window; q7d would be ~0.7-1.0), high 0.7 (q7d). This is DERIVED from the stated windows (not measured as a duty fraction anywhere), so grade ASSUMED-with-basis (TRANSFERRED window lengths). It supports the model's "CSF CAR-T active >= ~35% of each interval" threshold only for the central q14d case or for weekly dosing; at the low value the CNS arm fails. Toxicity: neurotoxicity is dose-limiting at the CSF route (10 of 18 grade 3 neurotoxicity at MTD 2.5e7, Bagley 2025), not a negligible cost.
CNS clearance by IV CD19 CAR-T is real (11/17 CSF CAR-T detected; 2 CNS leukaemias cleared) but durability in CNS lymphoma is short (median CNS-PFS 4 months), so CSF re-dosing is more defensible than a single IV dose for CNS closure.

## (e) Durable fraction at 5+ years, human analog

| scenario | fraction | source | grade / weakness |
|---|---|---|---|
| all-comer LBCL, 5 y event-free | 28-30% (ZUMA-1 EFS 30.3%; JULIET PFS 28%) | 36821768; 41252666 | MEASURED human; heavily pretreated, refractory, high burden, not early detection |
| LBCL 10-y lymphoma-free | 32% (CI 14-51); FL 47% (20-71) | 42341302 | MEASURED human, n=24/14, single centre, one product |
| responders, 5 y relapse-free | 61% (JULIET); CR subgroup 5-y OS 64.4% (ZUMA-1) | 41252666; 36821768 | conditional on response; closest to the "early detection, low burden" case but no early-detection-specific number found |
| conditional on 2-y event-free | 5-y OS 92.3% (CI 78.0-97.5), n=39 | 36821768 | OS not EFS; supports 2+ y -> long durability |
| relapse after 5.4 y | none in 10.1 y median follow-up (n=38) | 42341302 | small numbers at risk |
| NCI cohort DOR >3 y | 51% (CI 35-67) of treatments; remissions to 9 y | 33021872 | small, early product |
Central value for "durable plateau at 5+ y": ~30% of all treated; ~60% of responders; early-detection scenario plausibly toward the responder figure (low MTV gives HR 0.25-0.14 for OS and 0.40-0.29 for PFS, 32702097) but that uplift is NOT quantified as a plateau. Competing risks matter: 10-y NRM 18% and second primary cancers 21% (42341302). No dog durable fraction exists (MEASURED = 0 in dogs; the dog CAR-T efficacy bar is unmet, known to the user).

---

## What was searched and NOT found (consolidated)
- Per-CAR-T-cell in-vivo kill rate constant for patients; serial LDH half-life; per-patient serial PET log-reduction; tumour-burden half-life after CAR-T as a stated number.
- Time-to-MRD-negativity as a distribution (only day-28 snapshots).
- Direct measurement of CAR-T killing of G0 vs cycling lymphoma cells; any dog data on this.
- Any published dog CAR-T efficacy; dog CNS/CSF CAR-T; caninized/fully canine scFv CAR; canine CD22 CAR; canine gamma-delta CAR; canine CAR-NK; canine allogeneic/TCR-edited CAR-T; in-dog CD19 CAR-T.
- Intrathecal/intraventricular CD19/CD20 CAR-T trials for CNS lymphoma/leukaemia (humans). Dog CSF turnover.
- Not retrievable: Panjwani 2016 full text (abstract only); Frank 2021 full text; Liu 2021 CPT full text; 42638216 and 30846865 have no abstract; NEJM 2026 ten-year paper is abstract-only (no tables).

## Weaknesses of the whole derivation
1. All kill rates are population-level, saturating, and from humans or mice; none is measured in dogs.
2. Clinical declines include lymphodepleting chemotherapy; ctDNA is a proxy.
3. Kimmel's gamma/kB are non-identifiable (r = -0.96) and fitted to one tumour measurement.
4. The 10-year durability evidence is one single-centre series (n=38) of one product, small numbers at risk after 5 y.
5. Mouse CTL kill-per-day (Halle) and xenograft rates are transferred to CAR-T in an outbred dog.
6. CSF duty is derived from CNS-tumour trials with different antigens; lymphoma cells in CSF are suspended, not parenchymal, which could raise access but is unmeasured.
