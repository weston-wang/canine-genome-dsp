# Persistent GvL sweep (started 2026-10-04). Labels: [REC] = already in record (where), [NEW] = new.
Tools: PubMed via eutils helper scratchpad/pms.sh, pmsum.sh (abstracts fetched this session).

## Record read first
- LYMPHOMA_UNIVERSE.md F, G; SWEEP_hct_model.md (full), SWEEP_stemcell.md (grep).
- [REC] allo K_graft 2.6 e-folds, 166 d window, gross 0.106/d (SWEEP_hct_model s2.5-2.6, s7.1); "credit after window: none by default; late-relapse hazard bound 0.18/yr upper 95%, point 0" (s7.1 row, s2.8).
- [REC] chimerism: >95% donor within 2 wk 12/12 (35789057 s4.2); Lupu case >=58 wk (16506937); RIC 2 Gy durable 5/6 (12931117); 16/17 DLA-identical GVHD-free (22945, 1977; SWEEP_outside_model l.70). "12/19" in LYMPHOMA_UNIVERSE l.304.
- [REC] human DLI responses: DLBCL 60% (18684698), PTCL 66% (21904377), FL 77% (20606089); dog DLI: no outcome series (SWEEP_hct_model s4, s7.4, s8).
- [REC] CNS: SCNSL allo n=20, relapse 25% (34293518); CNS access 0.5 derived; T cells in CSF NOT FOUND; one PCNSL allo; IELSG30 late extranodal (38181782).
- [REC] quiescent: low-proliferation human tumours (FL 20107156, CLL) TRANSFER; direct assay NOT FOUND (s3.1, s8). MHC-loss refs 25371177, 30380364, 19641204, 42348822.
- [REC] NK dogs: 42461253 (3 dogs, solid tumour), 37852175 iNKT >=78 d, 33225057 CD94 NK haplo (SWEEP_stemcell l.220); canine NK phenotype 27933061 (SWEEP_exists l.91); CD52 Ab AT-005 null RCT 36329876 + target-binding doubt (SWEEP_pk s8); IL-15 canine: nothing found (LYMPHOMA_STATUS l.107); autologous T-cell add-back OUTCOME 34950726; Texas A&M AKC (SWEEP_near_future_cell l.30).
- [REC] late-hazard bound: 8 dogs x 2.1 y = 16.8 dog-y, 0 events -> <0.18/yr (s2.8); human FL RIC relapse 8% at 52 mo (20107156).

## Findings (human, late relapse / plateau)
- [NEW] 32259827 (Acta Haematol 2021) T-PLL allo (n=10): 3 pts in CR with DURABLE FULL-DONOR CHIMERISM relapsed at 12, 59, 84 months; CD52+ at relapse; DLI/alemtuzumab only transient PR. -> persistent donor immune system does NOT guarantee ongoing kill of T-lymphoid disease. CONTRADICTS persistence (T-cell).
- [NEW] 42253631 (EJHaem 2026) MCL allo n=29, median FU 143 mo: relapse 38%, >25% late (>12 mo), mostly localised; salvage RT +/- BTKi durable in ~2/3.
- [NEW] 24787231 (Leuk Res 2014) FL BEAM-alemtuzumab allo vs auto, n=171: 10-y cum. incidence of relapse 31.4% vs 55.1% (p=.042); "trend to plateau in survival"; DLI in 29%, all but 2 remain CR.
- [NEW] 29424927 (Cancer 2018) EBMT/CIBMTR FL allo n=1567: 5-y relapse/progression 29%, TRM 19%, FU 55 mo.  26961149 (Ann Oncol 2016) FL RIC-allo after auto n=183: 5-y relapse 16%.
- [NEW] 21536145 (BBMT 2011) RIC allo lymphoma n=280: 101 relapses, median time to relapse 90 d (3-1275 d) i.e. nearly all early; 29410340 (BBMT 2018) n=495 lymphoma allo, 35% relapsed; late relapse (>=130 d) HR death 0.25.
- [NEW] 17671231 (BMTSS Blood 2007) 2-y survivors n=1479 allo: relapse of primary disease = 29% of premature deaths, still leading cause of death; 19573079 (BJH 2009) auto 2-y CR survivors: relapse most common cause of death at 10 y (NHL) -> late relapse exists in both arms.
- [NEW] 12456505 (Blood 2002) lymphoblastic lymphoma allo vs auto: relapse at 5 y 34% vs 56% (p=.004).
- [NEW] 18922853 (Blood 2008) CML: quiescent CD34+ cells LESS susceptible than cycling to lysis by HLA-identical-sibling donor NK cells (TRAIL receptors up on quiescent; bortezomib sensitises) -> quiescent cells are NOT simply killed equally; authors infer GvL still eliminates quiescent cells in long-term CML survivors.
- [NEW] 10350348 (Leuk Lymphoma 1999) single PCNSL case, HLA-identical sibling nonmyeloablative allo, GVHD gr II, 100% donor, CR 30 mo: GvL in the brain (n=1).
- [NEW] 28140754 (Chimerism 2015, Fred Hutch dogs) DLI into stable MIXED-chimeric dogs had no effect; 18940673 (BBMT 2008) sensitised DLI in trichimeric dogs -> graft rejection + GVHD.

## More findings (all abstracts fetched via PubMed eutils this session)
### Late relapse / plateau (leukaemia transfer)
- [NEW] 36849078 (TCT 2023, SFGM-TC, 7582 allo for acute leukaemia): late relapse (>=2 y) = 4.2% of all transplants (12.4% of relapses), median 38.2 mo; ONE-THIRD of late relapses had persistent FULL DONOR chimerism; 27% extramedullary (17% exclusively); cGVHD protective (OR 0.64).
- [NEW] 38611097 (Cancers 2024, AML n=376): 142 relapsed (38%), 68% in year 1; >2 y: 26 pts = 6.9% of cohort; extensive cGVHD predicted no late relapse. Derived (persist_bracket.py): crude hazard yr1 0.30/yr, yr2 0.07/yr, >=2y ~0.011-0.018/yr -> hazard falls ~4x yr1->yr2, a further 4-7x later; e-fold decline 0.004/d (yr1-2), ~0.0008/d later. Selection-confounded; leukaemia; TRANSFER only.
- [NEW] 25348512 (Clin Cancer Res 2015, CIBMTR 7489 pts, leukaemia-free at 12 mo): cGVHD protects against late relapse ONLY in CML (RR 0.47), NOT in AML/ALL/MDS. -> ongoing alloreactivity buys little late protection outside CML; (and dogs had 0/13 cGVHD).
- [NEW] 42697904 (Sci Rep 2026, AML n=388): mixed T-cell chimerism at 3 mo -> higher late relapse (5-y CIR 29% vs 17%); residual disease drives early relapse, impaired donor immune reconstitution drives late relapse. Supports "donor immunity is what holds late".
- [NEW] 23333776 (BBMT 2013, CML post-allo, n=63): 83% had detectable BCR-ABL at least once, only 6/52 relapsed; transcripts fluctuate as late as >=10 y -> donor immune system holds persistent, quiescent-stem-cell disease for a decade (direct evidence of a "hold", CML). 11025600 (Haematologica 2000) same conclusion: eradication not required for long-term remission.
- [NEW] lymphoma-specific: 39660415 (Leuk Lymphoma 2025, n=150 identical MAC): landmark >=d100 5-y PFS PTCL 76% vs DLBCL 30%; relapse mortality 10% vs 36%; "strong GvL against PTCL but not DLBCL"; limited cGVHD did not help DLBCL. -> supports persistence for T-cell lymphoma, weaker for large B.
- [NEW] 32890747 (BBMT 2020, BEAM-Campath, n=52 lymphoma): 62% long-term mixed T-cell chimerism; DLI at median d225 (to 5.3 y) converted 47-50% to full donor; 10-y PFS-and-no-extensive-GVHD 45%, OS 66% at median FU 6 y; no excess relapse with mixed chimerism at 1-y landmark.
- [NEW contradiction] 32259827 T-PLL (3/10 relapse at 12, 59, 84 mo despite durable full donor chimerism). [NEW] 42253631 MCL late localised relapses (>25% >12 mo).
- [NEW] 21536145: median relapse time after RIC-allo lymphoma 90 d; relapse >6 mo survival 77% at 1 y -> relapses front-loaded.
### CNS
- [NEW] 41832229 (BMT 2026) ALL allo n=748: CNS relapse 5.1% at median 10.6 mo (Ph+ 9.7% vs 1.4%); 25017763 (BBMT 2014) n=457: 4% CNS relapse, no effect of post-HCT CNS prophylaxis or conditioning intensity; 29191665 cranial boost 0/30 CNS relapse vs 21% (2-y) w/o. -> GvL alone does not secure CNS.
- [NEW] 26586462 (Int J Hematol 2016) intrathecal DLI: donor mononuclear cells detected in CSF after IDLI, no GVHD, but efficacy limited (n=1 + 4 literature). 9823940 (Leukemia 1998): DLI -> marrow molecular CR yet extramedullary relapse (sites reached late).
- [NEW] 10350348 PCNSL one case durable GvL 30 mo (n=1). [REC] 34293518 SCNSL n=20.
### Quiescent cells / MHC
- [NEW] 18922853 CML quiescent CD34+ less lysed by HLA-identical-sibling NK than cycling (TRAIL-R up in quiescent; bortezomib sensitises). [NEW] 15536145 (Blood 2005, mouse AML) dormant cells resist CTL (B7-H1) but are killed by CXCL10-activated NK. [NEW] 38194912 (Cancer Cell 2024) dormant DTC evasion = scarcity, overcome by T-cell immunotherapy (breast, mouse). [NEW] 37847565 (JCI Insight 2023) dormant tumour cells lysed by T cells in vitro but Treg niche in vivo.
- [NEW] 12601144 (PNAS 2003) HA-1/HA-2 haematopoiesis-restricted miHA T cells give CR of relapsed leukaemia after DLI (lineage-restricted GvL separable from GVHD). Dogs: 23126655 (UTY CTL lysis of DLA-identical male BM), 25965411 / 27430015 (miHA vaccine-sensitised DLI changes chimerism in 1/3 dogs; T-cell response not sufficient in vivo).
### Canine DLI / chimerism / GvT
- [NEW] 12774055 (BMT 2003) + 28140754 + 27430015: in stable MIXED chimeric dogs unmodified DLI does NOT convert chimerism; only donors sensitised to host miHA convert (tolerant coexistence); IL-2 doesn't help. 18940673/22929594: sensitised DLI -> rejection + GVHD. No canine lymphoma DLI series (REC s8 stays true).
- [NEW, secondary citation] Weiden/Storb canine allo-vs-auto after 9.2 Gy: dogs surviving >14 d tumour-free at necropsy 88% allo vs 12% auto (cited in Graves&Storb 34390541, already read in record; the 14/15 unrelated-marrow figure is [REC] SWEEP_hct_model s1.3; the 88-vs-12 comparison is not). Primary PMID 28420 has no abstract.
- [NEW] 25875671 (JAVMA 2015) dog LGL leukaemia, DLA-matched sibling allo: full donor chimerism stable >=2 y, healthy. [REC] 16506937, 12931117, 6750877 (19/19 engrafted, 12 long-term chimeras = the "12/19").
### Other persistent immune routes for dogs
- [NEW] 40520425 (Front Vet Sci 2025) rcIL-15 + chemo, 61 dogs lymphoma (37 completed), 12 wk: ORR 77.8% vs 57.9%, PD 16.7 vs 31.6%; no durability data. [NEW] 40203669 (VIII 2025) rcIL-15 + metronomic CTX, 15 dogs, DCR 66.6%, PR 33% of haematological. [NEW] 37006127 rCaIFN-g CETCL n=20: no survival gain. [NEW] 42526683 canine CIK vs melanoma in vitro only. [REC] 38631708/42461253 NK first-in-dog (solid tumours); 37852175 iNKT; CD52 AT-005 null; autologous T add-back; vaccines flat. [NEW, low relevance] 41844944 canine DLBCL anti-CD20+dox+immunomodulator trial PBMC signatures.
- No canine alemtuzumab-like lineage antibody beyond AT-005 [REC]. No canine NK/CIK/gd-T lymphoma trial found.
### Bracket (scratchpad/persist_bracket.py)
- Window net rate (REC): 0.0039/0.0157/0.0253 per d; mu after program (REC) 0.66 (upper)/0.118/0.003.
- Dog late hazard upper 95% (0 events): 0.104/yr after d180 (28.8 dog-y), 0.121/yr after yr1, 0.178/yr after yr2 (REC 0.18; first two are NEW arithmetic). Dog data fix mu, NOT the continued kill: a lineage alive at d180 and not held would have regrown by ~d100-700 (REC s2.6) so zero relapses after d268 in 8 dogs to >=4.1 y = non-regrowth (hold or extinction); cannot separate.
- Required persistent net kill kp for mu(10y)<=X: central mu 0.118: 0.00025 (X=.05), 0.00071 (.01), 0.00137 (.001)/d; upper-CI mu 0.66: 0.00074, 0.0012, 0.0019/d (= 2-12% of the window rate).
- Human leukaemia hazard-decline transfer: 0.0008-0.004/d (5-25% of window rate): above the requirement for central mu, at the margin for upper-CI mu at X=0.001.
- Floor: net 0 (hold) = gross credit = growth bar 0.0903/d: no regrowth, no clearance; the clock needs margin>0 to clear.
- standard_audit run: failing() = [] ; wrongly_reported_as_gaps lists 5 items; persistence of GvL past d166 is in neither list (not previously graded) -> parent must decide grade (my reading: TRANSFERRED for hold; no dog measurement; contradicted for CNS and T-PLL).
