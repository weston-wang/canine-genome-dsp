# Canine lymphoma treatment trials and publications, 2025 to 31 Oct 2026 (post-sweep check, written 2026-10-31)

Scope and method. PubMed MCP: (a) dog AND lymphoma AND treatment terms, entry date 2026-06-01..2026-10-31 (43 hits, all titles screened); (b) dog AND lymphoma, entry date 2026-10-01..2026-10-31 (13 hits, all screened); (c) immunotherapy terms (CAR-T, bispecific, anti-CD20/CD52, PD-1/PD-L1, gilvetmab, vaccine), pub date 2025-2026 (25 hits); (d) design terms (prospective/trial/pilot/retrospective/case series), entry 2025-01..2026-05 (46 hits; metadata retrieved for all 46); (e) rabacfosadine/verdinexor/asparaginase/lomustine/transplant/intrathecal/irradiation/metronomic (18 hits); (f) CNS/CSF/intrathecal/HCT/NM600/radioimmunotherapy (11 hits). Web: VCS 2026 and 2025 abstract supplements, ESVONC 2026 supplement, ACVIM Forum 2026, UMN / LEAH Labs / Tufts / Purdue / Colorado Animal Specialty trial pages. Europe PMC REST used to identify the abstract-supplement PMIDs. The Wiley supplement full texts returned HTTP 403 to both WebFetch and curl, so every VCS/ESVONC item below is at **search-engine-snippet strength** (I could not read the abstract).

Record check. Every item was grepped (case-insensitive) for PMID, first author and agent in docs/LYMPHOMA_UNIVERSE.md, LYMPHOMA_STATUS.md, LYMPHOMA_DURABLE_RESPONSE.md, LYMPHOMA_COVERAGE_LEDGER.md and docs/universe/*.md. Labels: "ALREADY IN RECORD (file:line)" or "NOT IN RECORD". "Post-sweep" = published, presented or changed after 1 Oct 2026.

Case key: BB = B-cell body; TB = T-cell body; BC = B-cell brain/CNS; TC = T-cell brain/CNS. Escape codes follow docs/universe/SWEEP_escapes.md (E5 quiescent efflux-high progenitor; E7 antigen-low/antigen escape; E3 topo IIa; E8 XPO1; E10 CD47; E11 barrier compartments; E13 epigenetic; E15 asparaginase; E17 BTK; E18 weak immune modifiers; E19 host/logistic).

## Q0. Inventory: every canine lymphoma treatment study found in the window

### Takeaway
Six items are new to the record and matter for treatment: (1) a post-sweep JAVMA series of 82 dogs with B-cell lymphoma given adoptive T cells after CHOP at Bellingham; (2) a post-sweep status change: the LEAH Labs-sponsored UMN CAR-T pilot now reads "Open and enrolling", where the record says ON HOLD; (3) the UMN ORBIT trial (VSV + anti-PD-1, relapsed or refractory aggressive lymphoma, B or T); (4) a Zoetis fully canine anti-CD20 mAb given subcutaneously (VCS 2026 abstract, n=16); (5) the NCI/Tufts anti-CD20 + doxorubicin + immunomodulator trial, with outcome figures from a news release (>70 dogs, median OS 455 vs 180 d, about 20% long-term survivors); (6) several protocol papers (mechlorethamine MTD, THOP, 15- vs 19-week LHOP). None of them shows durable (10+ year) control or closes E5. Most other high-value items (half-body RT, afucosylated anti-CD20, tandem CAR-T, gilvetmab, IL-15, mediastinal LOPP/CHOP) are already in the record.

### Cited Findings

**A. NOT IN RECORD: treatment studies (peer-reviewed)**

| # | Item | Date | Design, n, lineage | Key numbers | Toxicity | Case / escape | Status |
|---|---|---|---|---|---|---|---|
| 1 | Westfall & Impellizeri, adoptive T-cell therapy (ACT) after CHOP | JAVMA 2026-10-05 | retrospective, 82 dogs, B-cell, 2017-2025 | median OS from diagnosis 660 d (95% CI 539-781); post-ACT survival 368 d (261-474); time to next treatment 317 d (284-350). No control arm; durable-remission fraction not given in the abstract | AEs in 4/82 (5%), mostly grade 1-2, one grade 3 | BB; consolidation after CHOP; does not address E5 or E7 by design (unengineered T cells) | **NOT IN RECORD; POST-SWEEP** — [PubMed 42833272](https://pubmed.ncbi.nlm.nih.gov/42833272/), [DOI](https://doi.org/10.2460/javma.26.05.0419). Westfall is the Bellingham Veterinary / Aurelius Biotherapeutics ACT developer ([Northern Light](https://www.thenorthernlight.com/stories/innovative-therapy-puts-blaine-dogs-cancer-into-remission,9264)); the record lists Bellingham only as an HCT centre (SWEEP_hct_model.md:191) |
| 2 | Chadsey, Hess, Intile, mechlorethamine phase 1 | Vet Comp Oncol 2025-11 | 3+3 dose escalation, 30 dogs, intermediate/large-cell (lineage not split in abstract) | MTD 10.7 mg/m2 (vs usual 3 mg/m2); DLT grade 4 neutropenia at 12.3 mg/m2; 6/10 naive dogs at MTD had PR at day 7 | low-grade GI | BB/TB rescue (MOMP backbone); alkylator, E3-independent | NOT IN RECORD — [PubMed 41198583](https://pubmed.ncbi.nlm.nih.gov/41198583/), [DOI](https://doi.org/10.1111/vco.70025) |
| 3 | Tellez Silva et al., THOP (temozolomide replaces cyclophosphamide) | Vet Sci 2025-03 | prospective pilot, 14 dogs, intermediate-large B-cell, first line | 14/14 CR; median TTP 269 d; median OS 433 d | 5 grade III + 4 grade IV haematologic; 1 grade III GI | BB. Temozolomide crosses the BBB in humans, so of interest for BC (no CSF data in dogs) | NOT IN RECORD (temozolomide is listed generically as EXCLUDED in LYMPHOMA_UNIVERSE.md:22) — [PubMed 40266942](https://pubmed.ncbi.nlm.nih.gov/40266942/), [DOI](https://doi.org/10.3390/vetsci12030251) |
| 4 | Lin & Wang, 15- vs 19-week LHOP (L-asparaginase replaces cyclophosphamide) | Animals 2025-02 | historical comparison, 18 vs 20 dogs, multicentric (T-cell included) | 19-week TTP and LSS significantly longer (p=0.004, p=0.008); ORR equal | not detailed in abstract | BB/TB; E15 | NOT IN RECORD — [PubMed 40003004](https://pubmed.ncbi.nlm.nih.gov/40003004/), [DOI](https://doi.org/10.3390/ani15040522) |
| 5 | Walker...Modiano, Sarver, single IV oncolytic VSV, then CHOP at day 30; serial scRNA-seq | bioRxiv 2026-09-14 (PubMed-indexed preprint) | n=1, stage 5A marginal zone (B) | VSV reached B cells, but the transcriptional response sat mostly in T cells (proliferation, cytotoxicity); 3 stable B-cell subclones; "downregulation of the quiescence program" | — | BB; heterogeneity / E12; precursor of the ORBIT trial (Q1) | NOT IN RECORD (record has only the 2017 VSV n=2 T-cell data, SWEEP_modalities.md:138) — [PubMed 42779884](https://pubmed.ncbi.nlm.nih.gov/42779884/), [DOI](https://doi.org/10.64898/2026.09.10.750253) |
| 6 | Lejeune et al., CBD/CBDA hemp oil with CHOP | JVIM 2025 | double-blind RCT, 25 enrolled / 19 completed, high-grade | no effect on doxorubicin AUC at week 0; at week 5 placebo 572.6 vs CBD 406.8 nM·h (reported as different) | no serious AEs | BB/TB host modifier (E19), PK interaction | NOT IN RECORD — [PubMed 40622742](https://pubmed.ncbi.nlm.nih.gov/40622742/), [DOI](https://doi.org/10.1111/jvim.70179) |
| 7 | Madden et al., prophylactic trimethoprim-sulfadiazine with first doxorubicin | Vet Comp Oncol 2026-09-21 | retrospective, 60 dogs (21 TMS, 39 none), high-grade multicentric | GI toxicity 66.7% vs 33.3% (p=0.013); adjusted OR 3.69 | no difference in neutropenia or hospitalisation | supportive care (E19) | NOT IN RECORD — [PubMed 42767796](https://pubmed.ncbi.nlm.nih.gov/42767796/), [DOI](https://doi.org/10.1111/vco.70113) |
| 8 | Treggiari et al., doxorubicin vs epirubicin GI adverse events (CHOP/CEOP) | JSAP 2026-10-27 | retrospective, 4 institutions, 178 dogs (114 epirubicin, 64 doxorubicin) | GI AEs 56.3% vs 34.2%; doxorubicin adjusted OR 2.70 | — | supportive (E19) | NOT IN RECORD; POST-SWEEP — [PubMed 42947482](https://pubmed.ncbi.nlm.nih.gov/42947482/), [DOI](https://doi.org/10.1111/jsap.70211). The same title and cohort were published in JSAP 2025-05 ([PubMed 40320245](https://pubmed.ncbi.nlm.nih.gov/40320245/), [DOI](https://doi.org/10.1111/jsap.13880)), also NOT IN RECORD; the 2026 record may be a re-publication or correction, not an independent cohort |
| 9 | Ke et al., MBCL in Taiwan | Front Vet Sci 2026-08 | retrospective, 441 lymphomas reviewed, CHOP-treated B-cell subset | median OS substage b 140 d vs a 186 d; CR/PR 196 vs SD/PD 182 d; HR 2.27 (signs), 2.09 (no response) | — | BB prognostic | NOT IN RECORD — [PubMed 42676414](https://pubmed.ncbi.nlm.nih.gov/42676414/), [DOI](https://doi.org/10.3389/fvets.2026.1870235) |
| 10 | Shen et al., oclacitinib vs CCNU in epitheliotropic T-cell lymphoma | Vet Dermatol 2026-08 | retrospective, 23 (12 vs 11) | no difference in response, OS (log-rank p=0.20) or relapse; fewer AEs with oclacitinib | — | TB (cutaneous) | ALREADY IN RECORD (universe/SWEEP_tcell_agents.md:3) — [PubMed 42554028](https://pubmed.ncbi.nlm.nih.gov/42554028/) |
| 11 | Low-dose naltrexone case series (Garza) | Int J Pharm Compd 2026 | case series, mixed cancers | abstract not screened in detail | — | E18 | NOT IN RECORD — [PubMed 41819128](https://pubmed.ncbi.nlm.nih.gov/41819128/) |
| 12 | Case reports: Kodama, MZL with neutropenia, dose-reduced multi-agent then L-asparaginase + nimustine, 2 CRs (JVMS 2026-05, [PubMed 42108088](https://pubmed.ncbi.nlm.nih.gov/42108088/)); Roh, vulvar relapse at day 181 after CHOP with discordant PARR (Vet Sci 2026-10-16, **post-sweep**, [PubMed 42944196](https://pubmed.ncbi.nlm.nih.gov/42944196/), [DOI](https://doi.org/10.3390/vetsci13101102)); Akiyoshi, bleomycin electrochemotherapy, oral CD8+ epitheliotropic T-cell lymphoma, durable local control (Front Vet Sci 2026-09, [PubMed 42866495](https://pubmed.ncbi.nlm.nih.gov/42866495/)); Nowell, fluorescent light energy in CTCL (Vet Dermatol 2026-06, [PubMed 42363651](https://pubmed.ncbi.nlm.nih.gov/42363651/)) | — | n=1 each | — | — | Roh bears on E11-type extranodal (genital) relapse in BB | all NOT IN RECORD |

**B. Already in record: treatment studies in window (re-confirmed, not new)**
- L-CHOP + low-dose-rate half-body RT, 75 vs 115 dogs, PFS 532 vs 296 d, OS 752 vs 457 d (JVIM 2026-07) — ALREADY IN RECORD (universe/SWEEP_stemcell.md:59; LYMPHOMA_STATUS.md:85) — [PubMed 42525883](https://pubmed.ncbi.nlm.nih.gov/42525883/)
- Lai 2025 HBI after 2 CHOP cycles, 14 vs 11; PFI 1143 vs 316 d; T-cell PFI 292 vs B 2127 d — ALREADY IN RECORD (universe/SWEEP_exists.md:122) — [PubMed 40088118](https://pubmed.ncbi.nlm.nih.gov/40088118/)
- Goto 2025, 2 relapsed B-cell dogs, L-CHOP then HBI, CR at 483 and 490 d — ALREADY IN RECORD (universe/SWEEP_exists.md:123) — [PubMed 41183984](https://pubmed.ncbi.nlm.nih.gov/41183984/)
- Mizuno 2026, afucosylated anti-canine CD20 4E1-7-B_f + CHOP, 13 B-cell dogs: 13/13 CR, PFS 340 d, OS 458 d, 2-y survival 38.9%, B-cell depletion >200 d — ALREADY IN RECORD (universe/SWEEP_bispecific.md:142; LYMPHOMA_STATUS.md:78) — [PubMed 41742528](https://pubmed.ncbi.nlm.nih.gov/41742528/)
- Machado 2026, mediastinal lymphoma 70 dogs (95.6% T), LOPP vs CHOP not different, PFS 132 d, OS 223 d — ALREADY IN RECORD (universe/SWEEP_exists.md:113) — [PubMed 41914636](https://pubmed.ncbi.nlm.nih.gov/41914636/)
- Kang 2025, recombinant canine IL-15 + chemo, 61 enrolled / 37 completed, ORR 77.8% vs 57.9% — ALREADY IN RECORD (universe/SWEEP_modalities.md:82) — [PubMed 40520425](https://pubmed.ncbi.nlm.nih.gov/40520425/)
- Gilvetmab, 15 lymphoma dogs, zero objective responses — ALREADY IN RECORD (LYMPHOMA_UNIVERSE.md:33) — [PubMed 42247661](https://pubmed.ncbi.nlm.nih.gov/42247661/)
- TKI meta-analysis, 101 dogs / 11 trials, ORR 42%, T 0.63 vs B 0.27 — ALREADY IN RECORD (universe/SWEEP_tcell_agents.md:14) — [PubMed 42656497](https://pubmed.ncbi.nlm.nih.gov/42656497/)
- Oclacitinib with other drugs in 8 dogs with epitheliotropic lymphoma (Vet Dermatol 2025-06) — ALREADY IN RECORD (universe/SWEEP_tcell_agents.md:3) — [PubMed 40525607](https://pubmed.ncbi.nlm.nih.gov/40525607/)

**C. Preclinical / biomarker items in window**
- Cabazitaxel in canine LCAL lines and xenograft — ALREADY IN RECORD (universe/SWEEP_tcell_agents.md:34) — [PubMed 42225556](https://pubmed.ncbi.nlm.nih.gov/42225556/)
- KPT-335 (verdinexor) + doxorubicin or vincristine in canine lines (JVMS 2025-11) — ALREADY IN RECORD (universe/SWEEP_modalities.md:133) — [PubMed 41285475](https://pubmed.ncbi.nlm.nih.gov/41285475/)
- EZH2 overexpression protects canine T-lymphoma lines — ALREADY IN RECORD (universe/SWEEP_modalities.md:102) — [PubMed 42368342](https://pubmed.ncbi.nlm.nih.gov/42368342/)
- Copy-number map of 90 high-grade nodal lymphomas (77 B, 13 T), CFA13/MYC gain, proteasome and HDAC candidates — ALREADY IN RECORD (universe/SWEEP_modalities.md:109) — [PubMed 42754084](https://pubmed.ncbi.nlm.nih.gov/42754084/)
- PBMC gene signatures predicting >400-day survival in the anti-CD20 trial — ALREADY IN RECORD (universe/SWEEP_escapes.md:139) — [PubMed 41844944](https://pubmed.ncbi.nlm.nih.gov/41844944/)
- NOT IN RECORD: oxibendazole in LCAL cells ([PubMed 42778368](https://pubmed.ncbi.nlm.nih.gov/42778368/)); anti-DLA-DR Fab fragments suppress canine lymphoma lines and a mouse xenograft (Cancers 2025-12, [PubMed 41514561](https://pubmed.ncbi.nlm.nih.gov/41514561/), [DOI](https://doi.org/10.3390/cancers18010048)); canine B-cell PDX and 2 new cell lines (Cells 2026-09, Leung/Weiss, Cornell, [PubMed 42782785](https://pubmed.ncbi.nlm.nih.gov/42782785/), [DOI](https://doi.org/10.3390/cells15181684)); PD-L1 membrane positivity trending to shorter TTP in 58 nodal lymphomas (BCL 136 vs 306 d; T-NOS 48 vs 228 d; not significant) (Res Vet Sci 2026-06, [PubMed 42365729](https://pubmed.ncbi.nlm.nih.gov/42365729/), [DOI](https://doi.org/10.1016/j.rvsc.2026.106309)); liquid-biopsy monitoring pilot ([PubMed 42277760](https://pubmed.ncbi.nlm.nih.gov/42277760/)); erythrocyte lipidomics, 39 dogs (Front Vet Sci 2026-09, [PubMed 42857385](https://pubmed.ncbi.nlm.nih.gov/42857385/)).

### Inferences
- The only post-sweep peer-reviewed treatment paper with outcome data is the Bellingham ACT series. Its median OS of 660 d from diagnosis is above typical CHOP-alone figures (the Taiwan CHOP cohort above: 140-196 d; L-CHOP controls in PMID 42525883: OS 457 d). But it is retrospective, selected (dogs had to finish CHOP and reach ACT) and uncontrolled, and post-ACT TTNT of 317 d means most dogs relapsed. It is not evidence of durable cure. It does not displace half-body RT (PFS 532 d, n=75, case-control) as the best-supported consolidation.
- The mechlorethamine MTD (3.6x the usual dose) and THOP are rescue/first-line chemotherapy refinements. They do not bear on E5 (pump-high quiescent progenitor). Temozolomide in THOP is the one agent that could matter for BC, but there are no canine CSF data.

### Gaps
- The Bellingham ACT paper: full text not read. Unknown: cell product (expansion method, dose), whether any dogs had HCT, how many stayed in remission beyond 2-5 years, and how many were censored.
- The low-dose naltrexone series abstract was not read in detail.

## Q1. Canine CAR-T, bispecifics, anti-CD20/CD52 and checkpoint antibodies: new results or new trials?

### Takeaway
There is still no canine CD3 or CD20xCD3 engager, no canine CD5/CD7/CD52 CAR-T, and no in-dog CD19 CAR-T result. New: (a) post-sweep, the UMN page for the LEAH Labs xenogeneic CAR-T pilot reads "Open and enrolling", and LEAH lists three sites (UMN, Ohio State, Missouri); the record says ON HOLD; (b) the UMN ORBIT trial pairs VSV with anti-PD-1 in aggressive lymphoma, B or T; (c) Zoetis has a fully canine anti-CD20 mAb given subcutaneously (VCS 2026 abstract, 16 dogs, no DLT, B-cell depletion at 5-10 mg/kg); (d) Penn has "bivalent loop" CD19/CD20 CAR-T (ESVONC 2026 abstract, in vitro), and a VCS 2025 abstract reports CD5-negative CAR+ cells arising during canine CAR-T manufacture.

### Cited Findings
- **UMN CAR-T for canine CD20+ B-cell lymphoma (LEAH Labs sponsor)**: page read 2026-10-31 says "Open and enrolling". PI Mike Henson, co-I Caitlin Feiock. CAR-T given by IV infusion and by injection into lymph nodes. Lymphodepletion: pentostatin bolus, plus cyclophosphamide and furosemide infusion on day -3. Eligibility: ≥10 kg, not boxers, ≥4 evaluable peripheral nodes, naive or relapsed, substage A, prednisone tapered off 72 h before. Product not named; no dose or date shown — [UMN trial page](https://vetmed.umn.edu/departments/centers-and-programs/clinical-investigation-center/current-clinical-trials/car-t-cell). **Conflicts with the record**: universe/SWEEP_dog_programs.md:12 and :30 say ON HOLD (read 2026-10-04), and LYMPHOMA_UNIVERSE.md:340 says "on hold". A search-engine snippet of the same page (cached) still said "on hold" ([search result for the same URL](https://vetmed.umn.edu/departments/centers-and-programs/clinical-investigation-center/current-clinical-trials/car-t-cell)). Status change is **POST-SWEEP (registered/institutional page)**. Pentostatin lymphodepletion is NOT IN RECORD (grep zero).
- **LEAH Labs**: "Our next clinical trial launches in May 2026"; also shows "Trial open — actively enrolling". Partner sites: University of Minnesota, **Ohio State University**, University of Missouri. "Treatment is provided at no cost to enrolled families." Claims "1st team in the world to achieve canine CAR-T remissions", with no numbers — company claim, unverified — [leahlabs.com](https://leahlabs.com/). The Ohio State site and the May 2026 relaunch are NOT IN RECORD; the record has LEAH on hold at Missouri and UMN (SWEEP_dog_programs.md:30).
- **ORBIT (UMN, PI Jaime Modiano)**: "VSV and an anti-PD-1 inhibitor for Canine Lymphoma". Phase 1 (VSV alone) COMPLETED, no results shown. Phase 2 (VSV + anti-PD-1) "Open and enrolling". VSV IV day 0; anti-PD-1 IV days 2, 16, 44, 100; node resection day 10. Naive or relapsed/refractory aggressive lymphoma, "B or T cell", ≥7.5 kg. Study costs covered up to about US$10,500. The VSV construct and antibody are not named — [UMN ORBIT page](https://vetmed.umn.edu/departments/centers-and-programs/clinical-investigation-center/current-clinical-trials/orbit-vsv). Linked NCI/Mayo project "Translation of a novel combination therapy approach for non-Hodgkin lymphoma", grant period listed as ending Aug 2024 — [Mayo Clinic project page](https://mayoclinic.elsevierpure.com/en/projects/translation-of-a-novel-combination-therapy-approach-for-non-hodgk-2). NOT IN RECORD (grep "ORBIT" zero; the record has VSV 2017 n=2 at SWEEP_modalities.md:138 and says anti-PD-1 gave zero responses in lymphoma, LYMPHOMA_UNIVERSE.md:33). Registered trial; no outcome data.
- **Zoetis fully canine anti-CD20 mAb, subcutaneous, VCS 2026 abstract** (Vet Comp Oncol 24 Suppl 3, PMID 42767940): 16 client-owned dogs with substage-a B-cell lymphoma at 3 hospitals; 3+3 escalation over 0.5, 1.0, 5.0 and 10.0 mg/kg; no hypersensitivity or DLT; B-cell depletion in all dogs at 5 and 10 mg/kg; "anti-tumor activity" claimed, numbers not seen — [VCS 2026 abstracts, DOI 10.1111/vco.70098](https://onlinelibrary.wiley.com/doi/full/10.1111/vco.70098). **Snippet strength only** (Wiley 403). NOT IN RECORD; the record treats a Zoetis canine lymphoma mAb as an UNVERIFIED market-research claim (universe/SWEEP_tcell_agents.md:37), and this abstract is the first primary-source sighting. Presented 24-26 Sep 2026 (before the sweep), but the supplement is not in the record.
- **ESVONC 2026 (Vet Comp Oncol supplement, PMID 42767961)**: "Bivalent Loop CAR T Cells Exert Specific Effector Function Against Canine B Cells". It describes CD20 loss in a canine patient after anti-CD20 CAR-T and two bivalent constructs engaging CD19, CD20 or both. Presenter Luiza Cesar Conti (Penn); won the Wim Misdorp Resident Award; presented 22 May 2026 — [ESVONC abstracts DOI 10.1111/vco.70095](https://onlinelibrary.wiley.com/doi/10.1111/vco.70095), [ESVONC programme](https://www.esvonc.com/congress/vets_program/friday_22_may_2026), [ESVONC awards](https://www.esvonc.com/congress/awards). The same supplement reportedly has a fully canine anti-CD20 mAb binding lymphoma cells in 221/225 samples (snippet). NOT IN RECORD as an abstract; the tandem CD19/CD20 concept is ALREADY IN RECORD as PMID 42480604 (universe/SWEEP_dog_programs.md:6). In vitro only.
- **VCS 2025 abstracts (Vet Comp Oncol 2026, PMID 41796044)**: a CAR-T abstract reports "a population of CD5neg CAR-expressing cells develop during canine CAR-T cell manufacturing" — [VCS 2025 abstracts, DOI 10.1111/vco.70050](https://onlinelibrary.wiley.com/doi/10.1111/vco.70050). Snippet strength. NOT IN RECORD. Relevant to any future canine CD5 CAR (fratricide/selection) and to TB.
- Already in record, re-confirmed: Penn TCAR in vitro (PMID 42480604, SWEEP_dog_programs.md:6); canine CAR with human 4-1BB-CD3z (PMID 41376156, :8); rabbit anti-canine CD19 (PMID 41847725, :9); camel VHH anti-CD20 (PMID 41160360, SWEEP_cart_kill.md:102); 4E1-7-B_f characterisation, rituximab non-binding (PMID 40577406, SWEEP_bispecific.md:151); afucosylated anti-CD20 + CHOP (PMID 41742528); gilvetmab 0/15 in lymphoma (PMID 42247661).
- NOT IN RECORD (minor): DLA-DR Fab fragments (in vitro and xenograft) as a class-II-directed antibody concept — [PubMed 41514561](https://pubmed.ncbi.nlm.nih.gov/41514561/).

### Inferences
- If the LEAH/UMN pilot has truly reopened (now at 3 sites), the project's "trial-stage CD20 CAR-T" input changes from "paused" to "enrolling". There is still no efficacy number, so its ASSUMED potency stays ASSUMED. Pentostatin + cyclophosphamide lymphodepletion is a stronger regimen than the cyclophosphamide-only one in the 2022 Penn dog, which is relevant to the persistence failure noted in SWEEP_cart_kill.md.
- ORBIT is the first open canine lymphoma trial found that adds PD-1 blockade to an immunogenic agent. Given 0/15 responses to gilvetmab alone, any ORBIT signal would come from VSV priming. It accepts T-cell lymphoma, the case the project currently cannot close.
- The Zoetis SC anti-CD20 matters for the BB program: a fully canine (not chimeric) antibody should lower anti-drug-antibody risk for repeated long-term dosing, and SC dosing is practical. It covers E7 only while CD20 is retained, and it does not reach BC.

### Gaps
- No canine CD3, CD20xCD3 or other T-cell engager; no canine CD5/CD7/CD52 CAR-T; no in-dog CD19 CAR-T data. Searched: PubMed (query c, 25 hits), ESVONC/VCS supplement snippets, UMN/Penn/LEAH pages. Nothing new beyond the record's SWEEP_dog_programs.md.
- The actual text of the VCS 2026, VCS 2025 and ESVONC 2026 abstracts could not be read (Wiley 403; Europe PMC lists them as subscription, no abstract text). Response rates for the Zoetis mAb are unknown.
- The UMN index page and the CAR-T subpage both say "Open and enrolling" today; a cached search snippet says "on hold". The project should confirm by phone or email (UMN CIC) before relying on it.

## Q2. Canine lymphoma vaccines (autologous, dTERT, mRNA, dendritic cell, HSP)

### Takeaway
No new canine lymphoma vaccine trial results were found in the window. The only new item is a systematic review that is already in the record.

### Cited Findings
- Leitão et al. 2026 systematic review of 24 canine autologous tumour-vaccine studies: lymphoma has the most evidence and the only randomised studies; exploratory pooled trend toward less progression; heterogeneous — ALREADY IN RECORD (universe/SWEEP_vaccines.md:80) — [PubMed 42284812](https://pubmed.ncbi.nlm.nih.gov/42284812/), [DOI](https://doi.org/10.1016/j.vaccine.2026.128836)
- Greenberg 2025 review of autologous cancer vaccines (Torigen) — ALREADY IN RECORD (SWEEP_dog_programs.md:42) — [PubMed 41006003](https://pubmed.ncbi.nlm.nih.gov/41006003/)
- Virus-like-particle immunotherapy review, human and veterinary (J Nanobiotechnology 2026) — review only, NOT IN RECORD, no dog lymphoma data identified in the title/abstract screen — [PubMed 42351104](https://pubmed.ncbi.nlm.nih.gov/42351104/)
- Dall'Ara 2026, neoplastic disease and core-vaccine antibody titres — not a cancer vaccine — [PubMed 42797642](https://pubmed.ncbi.nlm.nih.gov/42797642/)

### Inferences
- The record's autologous-vaccine credit (LYMPHOMA_UNIVERSE.md:39) is still based only on older APAVAC data; nothing in 2025-2026 strengthens or weakens it.

### Gaps
- dTERT (Impellizeri Tel-eVax), mRNA, dendritic-cell and HSP vaccines for canine lymphoma: no 2025-2026 publications found in PubMed queries (c) and (d). The UF RNA-LPA mRNA vaccine is glioma, not lymphoma (already in record, SWEEP_dog_programs.md:23).

## Q3. Small molecules and chemotherapy protocols

### Takeaway
Nothing new on verdinexor combinations in dogs (beyond in-vitro KPT-335 combos already in record), rabacfosadine combinations, BTK, venetoclax, proteasome, HDAC, PI3K or EZH2 inhibitors given to dogs. New protocol data: mechlorethamine MTD, THOP, 15- vs 19-week LHOP, plus supportive-care findings. One VCS 2025 abstract (snippet) reports verdinexor benefit in T-cell lymphoma, including cutaneous epitheliotropic disease.

### Cited Findings
- Mechlorethamine MTD 10.7 mg/m2; 6/10 naive PRs at day 7 — NOT IN RECORD — [PubMed 41198583](https://pubmed.ncbi.nlm.nih.gov/41198583/)
- THOP pilot, 14/14 CR, TTP 269 d, OS 433 d — NOT IN RECORD — [PubMed 40266942](https://pubmed.ncbi.nlm.nih.gov/40266942/)
- 19-week LHOP beats 15-week LHOP on TTP and LSS — NOT IN RECORD — [PubMed 40003004](https://pubmed.ncbi.nlm.nih.gov/40003004/)
- VCS 2025 abstract: verdinexor "has a benefit in the treatment of T cell lymphoma ... may be considered for treatment of cutaneous epitheliotropic lymphoma, though AEs are common" — snippet strength — [VCS 2025 abstracts](https://onlinelibrary.wiley.com/doi/10.1111/vco.70050). NOT IN RECORD as this abstract (verdinexor T-cell ORR 71% from PMID 30143046 is in record, SWEEP_modalities.md:133). Bears on TB, E8.
- KPT-335 + doxorubicin/vincristine in vitro — ALREADY IN RECORD (SWEEP_modalities.md:133) — [PubMed 41285475](https://pubmed.ncbi.nlm.nih.gov/41285475/)
- BI 705564 (BTK inhibitor) field trial in B-cell lymphoma still listed as enrolling at Colorado Animal Specialty — [Colorado Animal Specialty clinical studies](https://www.coloradoanimalspecialty.com/clinical-studies) (search snippet) — ALREADY IN RECORD (SWEEP_tcell_agents.md:37; SWEEP_dog_programs.md:13). No results published (E17).
- Laverdia-CA1 full FDA approval 2026-06-26 — ALREADY IN RECORD (SWEEP_dog_programs.md:65).
- Rabacfosadine: 2025-2026 searches returned only 2020-2022 data (pivotal PFS 82 vs 21 d; rabacfosadine/doxorubicin ORR 84%; + L-asparaginase ORR 67%, PFS 63 d) — [PMC7754483](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7754483/), [PubMed 34952995](https://pubmed.ncbi.nlm.nih.gov/34952995/). No new rabacfosadine combination study in the window.
- Supportive: prophylactic TMS raises GI toxicity (OR 3.69) — [PubMed 42767796](https://pubmed.ncbi.nlm.nih.gov/42767796/); doxorubicin vs epirubicin GI AEs (post-sweep re-publication) — [PubMed 42947482](https://pubmed.ncbi.nlm.nih.gov/42947482/); upfront steroid dose/duration has no prognostic effect in multicentric DLBCL (Vet Comp Oncol 2025-07) — [PubMed 40624957](https://pubmed.ncbi.nlm.nih.gov/40624957/), NOT IN RECORD (bears on E1); tumour lysis risk factor (JVIM 2026-01) — [PubMed 41742550](https://pubmed.ncbi.nlm.nih.gov/41742550/), NOT IN RECORD.

### Inferences
- The upfront-steroid null result (PMID 40624957) slightly weakens the idea that steroid pre-treatment induces E1/MDR resistance in multicentric DLBCL. It is retrospective; trial pages (e.g., Purdue) still exclude prednisone-pretreated dogs.
- No new agent in the window acts on E5 in dogs.

### Gaps
- No canine data in the window for venetoclax, ibrutinib/acalabrutinib, HDAC, PI3K, JAK (other than oclacitinib), EZH2 inhibitors or proteasome inhibitors (PubMed queries d and e). Metronomic protocols for lymphoma: none found.

## Q4. Transplant, total- and half-body irradiation, radiopharmaceuticals

### Takeaway
Half-body RT has the strongest new data and is already in the record. No new canine HCT (auto or allo) outcome paper, no TBI paper and no 90Y-NM600 lymphoma result was found in 2025-Oct 2026. The Bellingham group published adoptive T cells after CHOP (82 dogs, post-sweep; see Q0) rather than transplant data.

### Cited Findings
- L-CHOP + LDR HBRT PFS 532 vs 296 d (PMID 42525883), Lai HBI (PMID 40088118), Goto relapsed HBI (PMID 41183984) — all ALREADY IN RECORD (see Q0-B).
- Bellingham ACT after CHOP, 82 dogs — NOT IN RECORD; POST-SWEEP — [PubMed 42833272](https://pubmed.ncbi.nlm.nih.gov/42833272/). The record's earlier ACT data come from transplant + ACT (Gareau 2021/2022, LYMPHOMA_UNIVERSE.md:72).
- PubMed query (f) (HCT / stem cell transplant / bone marrow transplant / NM600 / radioimmunotherapy, 2025-2026): 11 hits, none a canine lymphoma transplant or radiopharmaceutical treatment study.

### Inferences
- For the T-cell programme (DLA-identical allo HCT), nothing in the window adds data. The Lai T-cell HBI subgroup (PFI 292 d vs 2127 d for B-cell) remains the only recent lineage-split consolidation signal, and it argues that RT consolidation helps B-cell much more than T-cell disease.

### Gaps
- NC State, Fred Hutch and Bellingham transplant outcomes 2025-2026: none found in PubMed. Not checked: NC State and Bellingham websites for new case counts.

## Q5. Canine CNS lymphoma treatment

### Takeaway
No canine CNS-lymphoma treatment study (intrathecal chemotherapy, CSF port, brain RT series, or CNS-relapse incidence cohort) was published in the window. There are only case reports, which bear on diagnosis and CSF risk, not treatment.

### Cited Findings
- Extranodal B-cell lymphoma with adnexal and suspected intracranial involvement, given modified CHOP-15; response, then cutaneous relapse at 3 months (Vet Ophthalmol 2025) — ALREADY IN RECORD (universe/SWEEP_cnsregimens.md:208; SWEEP_exists.md:125) — [PubMed 40216556](https://pubmed.ncbi.nlm.nih.gov/40216556/), [DOI](https://doi.org/10.1111/vop.70016)
- T-cell neurolymphomatosis, CSF-diagnosed, no response to chemotherapy (JVIM 2025) — NOT IN RECORD (grep zero) — [PubMed 40702997](https://pubmed.ncbi.nlm.nih.gov/40702997/), [DOI](https://doi.org/10.1111/jvim.70189). Bears on TC: peripheral-nerve/root infiltration lies outside a whole-brain field and may be outside the IT drug distribution.
- Major complications of CSF collection, 11 in 7545 collections (0.15%) (JVIM 2025) — ALREADY IN RECORD (universe/SWEEP_regional.md:233; SWEEP_brain_access.md:9) — [PubMed 40526210](https://pubmed.ncbi.nlm.nih.gov/40526210/), [DOI](https://doi.org/10.1111/jvim.70165)
- Retrobulbar large B-cell lymphoma with multifocal involvement, died despite lomustine (Vet Med Sci 2026) — ALREADY IN RECORD (universe/SWEEP_cnsregimens.md:208) — [PubMed 41495378](https://pubmed.ncbi.nlm.nih.gov/41495378/)

### Inferences
- The project's BC/TC programmes (23.4 Gy whole-brain/craniospinal RT plus IT methotrexate every 21 days) still have no new canine outcome data. The only CNS item new to the record is the T-cell neurolymphomatosis case (n=1). It is a reminder that T-cell nervous-system disease can sit in nerve roots and ganglia (E11-type compartment) rather than in brain parenchyma.

### Gaps
- Canine CNS relapse rate after systemic therapy: no 2025-2026 cohort found. Intrathecal chemotherapy series in dogs: none in the window.

## Q6. Trials currently recruiting (as of 31 Oct 2026)

### Takeaway
Recruiting lymphoma trials confirmed on institutional pages: UMN LEAH CAR-T (B-cell, status changed, post-sweep), UMN ORBIT (VSV + anti-PD-1, B or T), UMN LYRA 3 (screening blood test), BI 705564 BTK field trial (Colorado Animal Specialty; in record), Purdue multicentric lymphoma studies including a focused-ultrasound trial (snippet only). The Tufts/NCI anti-CD20 chemo-immunotherapy trial is complete, with outcome numbers in a February 2026 news release.

### Cited Findings
- UMN index lists: CAR-T for B-cell lymphoma "Open and enrolling"; ORBIT "Open and enrolling"; LYRA 1 enrollment closed; LYRA 3 (healthy dogs ≥5 y, DLBCL risk blood test) "Open and enrolling" — [UMN current trials](https://vetmed.umn.edu/departments/centers-and-programs/clinical-investigation-center/current-clinical-trials). LYRA NOT IN RECORD.
- Tufts news 2026-02-11: NCI-funded trial (PI Cheryl London) of doxorubicin + anti-CD20 + one of KPT-9274, RV1001 or TAK-981 in >70 dogs with DLBCL. Remission about 90%; median OS 455 vs 180 d (chemo alone); >35% alive at 2 y vs 15%; long-term survivorship about 20%; one German Shepherd (TAK-981 arm) in remission 5 years after diagnosis — [Tufts news](https://vet.tufts.edu/news-events/news/german-shepherd-clinical-trial-still-remission-five-years-after-lymphoma-diagnosis). News-release strength; the comparator is unclear. The trial's PBMC-signature paper is ALREADY IN RECORD (PMID 41844944), but these outcome figures and the 5-year remission are NOT IN RECORD (grep "TAK-981"/"KPT-9274" zero).
- Purdue: recruiting dogs with multicentric lymphoma for several studies, including high-intensity focused ultrasound; prior prednisone can exclude dogs — [Purdue canine lymphoma trials](https://www.vet.purdue.edu/wcorc/clinical-trials/canine-lymphoma.php), [Purdue B-cell trial](https://vet.purdue.edu/wcorc/clinical-trials/canine-b-cell-lymphoma.php) (search snippets; pages not fetched). NOT IN RECORD for lymphoma (the record lists Purdue only for CTCL gemcitabine and FUS in osteosarcoma).
- Penn Comparative Immunotherapy Program (autologous CAR-T for B-cell lymphoma/leukaemia) — ALREADY IN RECORD (SWEEP_dog_programs.md:19); not re-read today.

### Inferences
- The TAK-981 (SUMOylation inhibitor) arm producing a 5-year remission is the only report in the window of a lymphoma dog in remission at 5 or more years. It is n=1 and news-level, but it is the closest thing to "durable control" found. The paper with per-arm outcomes should be found and checked.

### Gaps
- AVMA AHSD, veterinarycancertrials.org, NCI COTC, Morris Animal Foundation, CSU, NC State, UC Davis, Cornell, Ohio State, Wisconsin trial pages were not individually fetched in this pass, because of the tool-call budget. The record's 2026-10-04 reads cover Penn, Missouri, CSU and UMN. Ohio State now appears as a LEAH site.

## Q7. VCS 2026 and ACVIM Forum 2026 abstracts

### Takeaway
VCS 2026 (24-26 Sep 2026) abstracts are published as Vet Comp Oncol 24 Suppl 3 (PMID 42767940, DOI 10.1111/vco.70098), and ESVONC 2026 (21-23 May) as PMID 42767961. Neither supplement is in the record, and neither could be read in full (Wiley 403). The lymphoma items seen in snippets: the Zoetis SC fully canine anti-CD20 escalation (n=16), a lymphoma session on prediction/economics/AI, liquid-biopsy (IDEXX Cancer Dx) monitoring posters, early post-treatment hyperphosphataemia in high-risk lymphoma, and a 21-dog Tokyo plasma study. No 2026 ACVIM Forum (Seattle, June 2026) lymphoma abstract was found; the JVIM abstract supplement was not located.

### Cited Findings
- VCS 2026 supplement exists and dates confirmed via Europe PMC (PMID 42767940; "Conference Proceedings"; subscription) — [Wiley DOI 10.1111/vco.70098](https://onlinelibrary.wiley.com/doi/full/10.1111/vco.70098); [Wiley TOC Vol 24 S3](https://onlinelibrary.wiley.com/toc/14765829/current)
- Lymphoma session "From prediction to practice: Clinical outcomes, treatment economics, and the evolving role of AI in canine lymphoma care", Thu 24 Sep 2026 — [VCS schedule](https://vetcancersociety.org/annual-conference/general-information/schedule-at-a-glance/) (snippet)
- ESVONC 2026 supplement PMID 42767961 — [Wiley DOI 10.1111/vco.70095](https://onlinelibrary.wiley.com/doi/10.1111/vco.70095)
- VCS 2025 supplement PMID 41796044 (published Mar 2026) — [Wiley DOI 10.1111/vco.70050](https://onlinelibrary.wiley.com/doi/10.1111/vco.70050)
- ACVIM 2026 Forum held in Seattle; 15 resident abstract awards; no lymphoma winner identified — [dvm360 2026-06-12](https://www.dvm360.com/view/acvim-celebrates-award-winning-2026-resident-research-abstracts); [eventscribe agenda](https://2026acvimforum.eventscribe.net/agenda.asp?all=1)

### Inferences
- The VCS 2026 supplement is the most likely place for unreported treatment data (e.g., HBRT, CAR-T, rabacfosadine combinations). Reading it with institutional access is the highest-yield next step.

### Gaps
- Full texts of the VCS 2026, VCS 2025 and ESVONC 2026 lymphoma abstracts: not read (HTTP 403). Every number cited from them is snippet-level and should be re-verified.
- ACVIM 2026 research abstract programme (JVIM): not located; no lymphoma abstracts identified.
