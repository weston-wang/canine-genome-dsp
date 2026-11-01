# "Stem cell" sweep for the canine multicentric lymphoma durable-response model

Sources: PubMed (E-utilities via the PubMed MCP tool). Every PMID/DOI below was fetched with `get_article_metadata` in this session; nothing is cited from memory. "Full text read" means PMC full text was retrieved; otherwise only the abstract was read and only abstract-level facts are used.
bioRxiv: its MCP tool has no keyword search (date/category filter only), so it was not used to hunt; see "Not searched / not found".
No files in the repo were changed or committed.

## 0. Bar and record check

User's bar, verbatim: "real data OR a rigorous/scientifically sound model; a transferred input (other species/disease/class mechanism) is acceptable IF the transfer is justified in writing. Unsupported numbers are just 'assumed'." Also "assuming early detection", "10+ years of durability". Graded against exactly that. I do not grade against "demonstrated in dogs".

Record check (`origin/claude/duplicate-codex-prefix-branch-lt1qh6`, docs + src):
- ALREADY COVERED: TBI+transplant as one OUTCOME-graded entry (`LYMPHOMA_COVERAGE_LEDGER.md` l.133); PMIDs 22882500, 24467413, 34950726, 38695516 and TRM as a competing hazard (`LYMPHOMA_DURABLE_RESPONSE.md` s5 route 7, s6); radiation potency DERIVED by LQ from canine lymphoid-line SF2/SF5 (PMID 27257868; `lymphoma_grounded_inputs.py` RT_SURVIVAL); chemo-selected stem-like cells as a variant of the persister (PMID 30238600, 23820219; ledger l.80); half-body irradiation (PMID 19627472, 42525883); CD20 CAR-T persistence 14-50 d (PMID 35898541).
- NOT COVERED (new here): allogeneic DLA-identical HCT outcome (PMID 35789057); the canine lymphoid-progenitor paper (PMID 21777289); TBI dose-escalation showing no relapse benefit (PMID 3887690, 3901841); radiation-chimera second-cancer risk (PMID 6355021); human AATT allo-vs-auto data (PMID 39270145); MSC / iPSC / NK / iNKT status in dogs; 211At anti-CD45 conditioning; GVHD in dog haplo-HCT.
- CORRECTION to the record: `LYMPHOMA_DURABLE_RESPONSE.md` s3 says Gareau 2021 "reached their cure fraction by adding adoptive T-cell therapy" and the layman page says "the immune step is what carries it". The paper itself concludes the opposite: ACT "does not provide a clinical benefit over CHOP chemotherapy and autoPBHSCT alone" (DFI 199.5 vs 565 d, p=0.567; OS 752 vs 531 d, p=0.72; historical n=15; no randomisation). The 40% (4/10) is a cure fraction of the transplant cohort, not evidence that ACT contributes. Full text read.

## 1. Bottom line (strength stated per item)

1. Real long-term data exist in dogs, all retrospective or case series, all NCSU-centred in the modern era: autologous TBI+HCT cures roughly 15-40% depending on phenotype and definition; DLA-identical allogeneic HCT has 8/9 evaluable first-remission B-cell dogs living more than 4 years without dying of lymphoma, 6 still alive and disease-free at report (n=15 total, n=10 in first remission, 4 centres). Longest documented disease-free dog: 2920 d (about 8 y). No dog in the verified literature has documented 10-year follow-up. [OUTCOME]
2. Stem cells themselves are not the kill mechanism. In autologous HCT the stem-cell graft is marrow rescue (removes the marrow toxicity ceiling so a ~10 Gy TBI is survivable). The kill is the TBI. In allogeneic HCT the donor immune system is the kill (graft-versus-lymphoma). Model them as (a) a toxicity-budget modifier plus a TRM hazard, and (b) for allo, a persistent immune effector. Neither fits a chemo-style per-day kill rate cleanly.
3. The strongest inference in the sweep: dose escalation of TBI did not reduce relapse (8.4 Gy vs 13.5 Gy vs 11.8-14.7 Gy, Seattle; 10 vs 12 Gy, NCSU) while TRM doubled, yet the LQ model built on canine lymphoid lines predicts 2-5 extra logs of kill at 13.5 Gy. So relapse after TBI is not limited by uniform radiation cell kill. Allo-HCT at only 2 x 4 Gy (less cytoreduction than 10-12 Gy auto) gives far fewer relapses. Both point to an immune effector, not radiation, carrying durability. Inference, not measured mechanism; n is small.
4. "Cancer stem cell" in canine lymphoma = a flow/ALDH/efflux phenotype (CD34/CD90/CD117/Oct3/4 high, ALDH high, dox efflux high; side-population cells have higher ABCB1). It is enriched by chemotherapy in vitro and in relapsed dogs. Nobody has shown these cells are dormant, exclusively tumour-initiating, or the source of relapse in dogs. It overlaps the model's P-gp/efflux lineage more than a dormancy pool.
5. MSC: no anti-lymphoma role found; supportive/immunomodulatory only, and in the one canine GVHD test they failed. iPSC-derived, HSC-gene-modified CAR, and stem-cell-derived NK/T products: nothing found in dogs for lymphoma.
6. Human analogs transfer a consistent message: allo-HCT cuts relapse (AATT, PTCL: relapse 8% vs 55%) but non-relapse mortality eats the gain (31% vs 3%).

## 2. Verified citation table

All fetched this session. DOIs given as links.

| PMID | Cite | DOI | Read |
|---|---|---|---|
| 22882500 | Willcox, Pruitt, Suter 2012, JVIM 26:1155. autoPBHCT, B-cell, n=24 | https://doi.org/10.1111/j.1939-1676.2012.00980.x | abstract |
| 24467413 | Warry, Willcox, Suter 2014, JVIM 28:529. autoPBHCT, T-cell, n=15 | https://doi.org/10.1111/jvim.12302 | full text |
| 34950726 | Gareau, Ripoll, Suter 2021, Front Vet Sci 8:787373. autoHCT + ACT, B-cell, n=10 | https://doi.org/10.3389/fvets.2021.787373 | full text |
| 35789057 | Gareau et al 2022, Vet Comp Oncol 20:862. DLA-identical alloHCT, B-cell, n=15 | https://doi.org/10.1111/vco.12847 | full text |
| 38695516 | Benedict, Suter, Meritet 2024, Vet Pathol 61:765. Post-mortem, 94 TBI+HCT dogs | https://doi.org/10.1177/03009858241249114 | abstract |
| 31146304 | Gieger et al 2019, Vet Radiol Ultrasound 60:586. TBI protocol dosimetry (2 x 5 Gy, 16 h apart) | https://doi.org/10.1111/vru.12776 | abstract |
| 21670196 | Escobar et al 2011, Vet Pathol 49:341. Hematology after TBI + PBPC in 10 dogs | https://doi.org/10.1177/0300985811410721 | abstract |
| 3887690 | Appelbaum et al 1985, Transplantation 39:499. 95 dogs, TBI + marrow | https://doi.org/10.1097/00007890-198505000-00008 | abstract |
| 3901841 | Deeg et al 1985, Am J Vet Res 46:2016. TBI regimens, 40 dogs | no DOI in record | abstract |
| 2873669 | Appelbaum et al 1986, Transplantation 42:19. PBSC, 12 dogs | https://doi.org/10.1097/00007890-198607000-00004 | abstract |
| 400683 | Weiden et al 1979, Exp Hematol 7 Suppl 5:160. 1100 R + marrow, 17 dogs vs 8 controls | no DOI in record | abstract |
| 1095380 | Weiden et al 1975, Exp Hematol 3:124. 1200 R + marrow, 25 L dogs | no DOI in record | abstract |
| 16594594 | Frimberger et al 2006, JVIM 20:355. VELCAP-HDC, high-dose cyclophosphamide + autologous marrow, n=28 | https://doi.org/10.1892/0891-6640(2006)20[355:accpwd]2.0.co;2 | abstract |
| 22620705 | Lane, Chan, Wyatt 2012, Am J Vet Res 73:894. G-CSF before autoBMT, 21 dogs | https://doi.org/10.2460/ajvr.73.6.894 | abstract |
| 16506937 | Lupu et al 2006, JAVMA 228:728. Case: allo-HCT, T-cell lymphoma, 2 x 4 Gy, donor chimerism >=58 wk | https://doi.org/10.2460/javma.228.5.728 | abstract |
| 12931117 | Hogan et al 2003, BBMT 9:489. 2 Gy/1 Gy TBI + SRL/CSP, DLA-identical, mixed chimerism | https://doi.org/10.1016/s1083-8791(03)00148-4 | abstract |
| 8605371 | Sandmaier et al 1996, Blood 87:3508. Allo PBSC, 920 cGy, no post-graft IS | no DOI in record | abstract |
| 11719387 | Georges et al 2001, Blood 98:3447. DLA-haplo + transduced CTL, GVHD in all engrafted | https://doi.org/10.1182/blood.v98.12.3447 | abstract |
| 19446000 | Zorn et al 2009, Exp Hematol 37:998. DLA-haplo, CD6-depleted marrow, DLT causes GVHD | https://doi.org/10.1016/j.exphem.2009.05.001 | abstract |
| 39025648 | Nonmyeloablative 211At-anti-CD45 for canine DLA-haplo HCT, J Nucl Med 2024 | https://doi.org/10.2967/jnumed.124.267540 | abstract |
| 26338894 | Frost et al 2015, J Nucl Med 56:1766. 211At-anti-CD45 + autoHCT in 8 normal dogs | https://doi.org/10.2967/jnumed.115.162388 | abstract |
| 6355021 | Deeg et al 1983, IJROBP 9:1505. Malignancy after TBI + marrow, 153 dogs | https://doi.org/10.1016/0360-3016(83)90325-5 | abstract |
| 1521085 | Kolb et al 1992, Bone Marrow Transplant 10 Suppl 1:135. Cancer after BMT, incl. dogs | no DOI in record | abstract |
| 32686109 | Masciana et al 2020, JVIM 34:2096. Factor V inhibitor after alloHCT in a dog | https://doi.org/10.1111/jvim.15845 | abstract |
| 19754817 | Low-dose TBI 1 Gy for relapsed canine lymphoma, Vet Comp Oncol 2006, n=7 | https://doi.org/10.1111/j.1476-5810.2006.00095.x | abstract |
| 7262204 | Low-dose TBI 150 rad x10 canine lymphoma, Exp Hematol 1981 | no DOI in record | abstract |
| 19627472 | Lurie et al 2009, JVIM 23:1064. LDR half-body RT + chemo, n=38 | https://doi.org/10.1111/j.1939-1676.2009.0353.x | abstract |
| 37700548 | Best et al 2023, JVIM 37:2368. LDR half-body RT, B-cell, case-control | https://doi.org/10.1111/jvim.16840 | abstract |
| 42525883 | Colosi et al 2026, JVIM 40(4). L-CHOP + LDR HBRT vs L-CHOP, n=75 vs 115 | https://doi.org/10.1093/jvimsj/aalag144 | abstract |
| 22355761 | O'Connor et al 2012, Sci Rep 2:249. Autologous expanded T cells after CHOP, persisted 49 d | https://doi.org/10.1038/srep00249 | abstract |
| 27257868 | Maeda et al 2016, PLoS One 11:e0156689. Radiosensitivity of 27 canine lines | https://doi.org/10.1371/journal.pone.0156689 | full text |
| 21777289 | Ito et al 2011, JVIM 25:890. Lymphoid progenitor cells in canine B-cell lymphoma | https://doi.org/10.1111/j.1939-1676.2011.0756.x | full text |
| 30238600 | Hartley et al 2018, Vet Comp Oncol 17:69. CSC populations and chemotherapy | https://doi.org/10.1111/vco.12447 | full text |
| 23820219 | Kim et al 2013, J Vet Sci 14:481. Side population, canine lymphoma | https://doi.org/10.4142/jvs.2013.14.4.481 | abstract |
| 23167606 | Tomiyasu et al 2012, Leuk Lymphoma 54:1309. ABCB1/LRP in SP cells | https://doi.org/10.3109/10428194.2012.751529 | abstract |
| 25964560 | Liu et al 2015, Anticancer Res 35:2805. Stem-marker expression, B-cell lines, spheres | no DOI in record | abstract |
| 15963817 | Wilkerson et al 2005, Vet Immunol Immunopathol 106:179. 3 CD34+ B-cell cases of 30 | https://doi.org/10.1016/j.vetimm.2005.02.020 | abstract |
| 21781170 | Rao et al 2011, JVIM 25:1097. Low MHC-II predicts poor outcome, canine B-cell lymphoma | https://doi.org/10.1111/j.1939-1676.2011.0767.x | abstract |
| 27856424 | Weiskopf et al 2016, Cancer Immunol Res 4:1072. CD47 blockade + canine anti-CD20, mouse xenograft | https://doi.org/10.1158/2326-6066.CIR-16-0105 | abstract |
| 20816818 | MSC fail to prevent GVHD after DLA-haplo BMT, BBMT 2010 | https://doi.org/10.1016/j.bbmt.2010.08.015 | abstract |
| 23723082 | Safety of MSC in DLA-identical canine BMT, Chimerism 2013 | https://doi.org/10.4161/chim.25110 | abstract |
| 41319893 | Rana, Choudhary 2025, Vet J 315:106520. SVF/MSC suppress PBMC proliferation in vitro, incl. lymphoma dogs | https://doi.org/10.1016/j.tvjl.2025.106520 | abstract |
| 37852175 | Allogeneic iNKT persist >=78 d in MHC-mismatched dogs, Cell Rep Med 2023 | https://doi.org/10.1016/j.xcrm.2023.101241 | abstract |
| 42461253 | Weisnicht et al 2026, Vet Comp Oncol. Allogeneic expanded NK in 3 dogs, solid tumours | https://doi.org/10.1111/vco.70091 | abstract |
| 39314237 | PD-1/CD28 switch receptor, canine CAR-T, iScience 2024 | https://doi.org/10.1016/j.isci.2024.110863 | abstract |
| 42472629 | Canine iPSC to red cells, Stem Cells Transl Med 2026 | https://doi.org/10.1093/stcltm/szag058 | abstract |
| 23409943 | Canine iPSC to platelets, Stem Cells Dev 2013 | https://doi.org/10.1089/scd.2012.0701 | abstract |
| 1429095 | Uckun et al 1992, IJROBP 24:705. Human T-ALL/NHL clonogenic SF2, CD3 predicts relapse after TBI-ASCT | https://doi.org/10.1016/0360-3016(92)90718-w | abstract |
| 8443393 | Uckun, Song 1993, Blood 81:1323. B-lineage ALL radioresistance (CD24-) | no DOI in record | abstract |
| 3009370 | Malaise et al 1986, IJROBP 12:617. Radiosensitivity 1.9x lower in vivo than in vitro | https://doi.org/10.1016/0360-3016(86)90071-4 | abstract |
| 20970029 | Ganem et al 2010, IJROBP 78:975. Low-dose RT in follicular lymphoma | https://doi.org/10.1016/j.ijrobp.2010.06.056 | abstract |
| 7477169 | Philip et al 1995 (PARMA), NEJM 333:1540 | https://doi.org/10.1056/NEJM199512073332305 | abstract |
| 20660832 | Gisselbrecht et al 2010 (CORAL), JCO 28:4184 | https://doi.org/10.1200/JCO.2010.28.1618 | abstract |
| 22851556 | d'Amore et al 2012 (NLG-T-01), JCO 30:3093 | https://doi.org/10.1200/JCO.2011.40.2719 | abstract |
| 19029417 | Reimer et al 2009, JCO 27:106 | https://doi.org/10.1200/JCO.2008.17.4870 | abstract |
| 27471868 | Nordic/German long-term PTCL autoSCT, Blood Cancer J 2016 | https://doi.org/10.1038/bcj.2016.63 | abstract |
| 18541192 | Stanford PTCL autoHCT, BBMT 2008 | https://doi.org/10.1016/j.bbmt.2008.04.004 | abstract |
| 15169805 | Corradini et al 2004, JCO 22:2172. RIC allo, relapsed PTCL | https://doi.org/10.1200/JCO.2004.12.050 | abstract |
| 39270145 | Tournilhac et al 2024, JCO 42:3788. AATT long-term follow-up | https://doi.org/10.1200/JCO.24.00554 | abstract |
| 34792 | Weiden et al 1979, NEJM 300:1068. GVHD and relapse, human leukaemia | https://doi.org/10.1056/NEJM197905103001902 | abstract |
| 19641204 | Vago et al 2009, NEJM 361:478. Loss of mismatched HLA after haplo-HCT | https://doi.org/10.1056/NEJMoa0811036 | abstract |
| 32158444 | Rovatti et al 2020, Front Immunol 11:147. Immune evasion after haplo-HCT (HLA loss, class II down-regulation) | https://doi.org/10.3389/fimmu.2020.00147 | abstract |

Additional PMIDs cited in text (metadata fetched, abstract or title only used): 19747631 (Ding 2009, BBMT 15:1244, delayed haplo-HCT after TBI, https://doi.org/10.1016/j.bbmt.2009.06.004); 2397754 (Carter 1990, Exp Hematol 18:995, marrow culture purging cytogenetics); 33225057 (Abrams 2020, Transplant Direct 6:e632, CD94 NK in haplo BMT, https://doi.org/10.1097/TXD.0000000000001082); 17442404 and 17139538 (Suter, canine CD34+ gene transfer, X-SCID); 32664672, 24040358, 26254365 (canine MSC as oncolytic-virus or IFN-beta vehicles, solid tumours); 22674797 (Hematol Oncol 2012 review, dog as NHL model).

Not usable as data (abstract not available in PubMed): Weiden 1978 allogeneic grafts in dogs with spontaneous tumours (PMID 28420), Weiden 1979 Blood (PMID 387112, "prolonged disease-free survival ... TBI and autologous marrow"), Bowles 1980 (PMID 6997586). Their titles and MeSH terms were seen; no numbers were extracted.

## 3. (A) Dog HSCT for lymphoma: what was found

### 3.1 Cohorts

| Study | n; phenotype | Conditioning | TRM | Outcome |
|---|---|---|---|---|
| Appelbaum 1985 (3887690) Seattle | 95 dogs in chemo remission; 38 at 8.4 Gy (4 cGy/min) | TBI 8.4 Gy LDR + autologous marrow | 26% (10/38) at 8.4 Gy; 55% at 13.5 Gy | 9/38 (24%) long-term disease-free (follow-up length not in abstract); actuarial relapse about 65%. 13.5 Gy: TRM up, relapse not reduced. Unrelated allo marrow (n=8): 6 died <2 wk of infection, 2 of GVHD. |
| Deeg 1985 (3901841) Seattle | 40 dogs, MOPA-6 remission | 13.5 Gy at 4 cGy/min (n=20), 11.8-14.7 Gy at 2 cGy/min (n=20) | 8/20 (40%) at 13.5 Gy (2 VOD, 3 pneumonia, 3 haemorrhage); second group not stated | 7/16 relapsed at median 169 d; 9/14 at median 117 d; 5 survivors killed 110-680 d with no lymphoma at necropsy. Authors: higher dose did not cut recurrence; contaminated remission marrow is an alternative cause. |
| Weiden 1979 (400683) | 17 dogs, 1100 R (11 Gy) + autologous marrow vs 8 chemo-remission controls | TBI + marrow | 2 failed to regain marrow function | 5 alive in unmaintained CR 200-663 d after chemo start. Comparator: none of 8 controls stayed in remission beyond 113 d. |
| Weiden 1975 (1095380) | 25 L dogs, 1200 R, no prior remission requirement | TBI + marrow | - | 8 survived >14 d; 7 of 8 survivors relapsed. Conclusion: TBI alone does not cure; immune function impaired ~10 wk. |
| Appelbaum 1986 (2873669) | 12 dogs, PBSC | 8.4 Gy type | 33% (4/12) | 5 relapsed (41%); 3 (25%) long-term disease-free. |
| Willcox 2012 (22882500) NCSU | 24 B-cell; 15 transplanted before relapse | 10 Gy TBI; high-dose cyclophosphamide + G-CSF mobilised PBSC | 2 in-hospital (8.3%); 1 late graft failure death d45 | Median DFI 271 d; OS 463 d; 5/15 (33%) in remission at median OS 524 d (range 361-665). 1 TBI pulmonary fibrosis at ~8 mo. |
| Warry 2014 (24467413) NCSU | 15 T-cell (13 in first CR) | 10-12 Gy in 2-3 days, 7 cGy/min | 2 (13%) | DFI 184 d; OS 240 d; relapses 3 (23%) <4 mo, 3 (23%) 4-8 mo, 5 (38%) >8 mo (8.3, 10, 12.9, 18.3, 24.6 mo), 1 still disease-free at 24.7 mo; 2 alive at 741 and 772 d (15%). 1 second cancer (cutaneous B-cell, d120). 1 dog re-transplanted with 6 Gy: 225 more days. |
| Gareau 2021 (34950726) NCSU | 10 B-cell, CHOP + autoHCT + expanded autologous T cells | 10 Gy (n=5) or 12 Gy (n=5), 2 x on consecutive days | 0 | 6 relapsed at 4, 4, 5, 8, 13, 15 mo; 4 (40%) alive >=2 y; median DFI 199.5 d; no benefit vs historical autoHCT alone; 10 vs 12 Gy no difference. |
| Gareau 2022 (35789057) | 15 B-cell, DLA-identical allo-PBSC (10 in first remission), 4 centres, 2006-2018 | 2 x 4 Gy (7.5-10 cGy/min), cyclosporine to ~d30 | 2/15 (13%), both not in remission | Median DFI 1095 d (range 9-2920), OS 1115 d. First-remission dogs: median DFI 1235 d. One of 10 died d19 (presumed GDV); 1 died of lymphoma at 268 d; of the other 8, one euthanised ~8 y and one died ~4.5 y for non-lymphoma reasons, six alive and disease-free. Authors' cure = >4 y and/or not dying of lymphoma: about 89% (8/9). |
| Benedict 2024 (38695516) | 94 multicentric-lymphoma dogs with TBI+HCT at NCSU over 10 y (phenotype split not given; the 5 necropsied were B-cell, 4 auto, 1 haploidentical allo) | TBI + HCT | 7/94 (7%) died before discharge | All 5 necropsied: marrow depletion, 3 systemic candidiasis, 2 bacterial infection. |
| Frimberger 2006 (16594594) | 28 dogs, 5-drug + high-dose cyclophosphamide + autologous marrow, no TBI | cyclophosphamide 300-500 mg/m2 | 0 | Group 3 (500 mg/m2, n=13): median remission 54 wk, survival 139 wk (vs 21 and 43-68 wk). |

Comparator arms: only two direct ones exist. (i) 8 chemo-remission controls in Weiden 1979 (none in remission beyond 113 d), a 1970s protocol; (ii) Gareau 2022 and 2021 compare against NCSU historical autoHCT, not against CHOP alone. No randomised or concurrent CHOP-alone comparator for transplant exists in dogs. The HBRT case-control (PMID 42525883: PFS 532 vs 296 d, n=75 vs 115) is the nearest modern "consolidation vs CHOP" comparison but is not a transplant.

Unverified discrepancies inside the sources (flagged, not resolved): Gareau 2021 quotes cure of "30% and 19%" for B and T cells while Willcox/Warry give 33% and 15%; Gareau 2021 lists the four "cured" dogs with OS range 86-1317 d although cure is defined as >=2 y; Gareau 2022 gives disease-specific mortality 27% (would be 4/15) while naming three euthanised for progression.

### 3.2 Immunophenotype split
B-cell: auto 24 + 10 + 15 (NCSU), allo 15. T-cell: auto 15 (NCSU) only; one allo T-cell case report (PMID 16506937; 2 x 4 Gy, full donor chimerism and clinical remission at 58 wk, then no further follow-up in the abstract). No T-cell data series for allo. T-cell is clearly worse with auto (median DFI 184 d vs 271-565 d; 15% vs 33% alive at 2 y).

### 3.3 Durability tail and relapse timing (honest)
- Auto B-cell: relapses concentrate in the first 15 months (Gareau 2021: 4-15 mo); Gareau 2022 states that every dog across all three NCSU series (auto, auto+ACT, allo) that lived >2 y post-transplant has lived >4 y (trial end-point 4.1 y). Longest DFI in first-remission auto series 2920 d.
- Auto T-cell: relapses out to 24.6 mo; 1 of 13 disease-free at 24.7 mo; 2 alive at 741-772 d. Nothing longer.
- Allo B-cell: 6 dogs alive and disease-free at time of writing; span to 8 y.
- "2 y disease-free" is not 10-year data. The only things actually known: (a) no documented relapse between 2 and 4 y in the small NCSU surviving set; (b) a few dogs to 8 y. The number of dogs contributing to (a) is about 4-6 auto B-cell dogs plus about 8 allo dogs. The record cannot support a 2 y to 10 y inference from dog data. Human 2-to-10 y inference was NOT verified in this sweep (no PMID fetched), so do not cite one from this report.
- Late harm competes: Deeg 1983 (6355021): radiation chimeras (6.1-21.3 Gy, n=153) had about 5-fold relative malignancy risk vs 242 controls; Kolb 1992 (1521085): cancer deaths in treated dogs began at age ~5 y vs ~9 y in untreated. So a 10-year horizon includes second-cancer hazard that TBI raises.

### 3.4 What predicts relapse, and MRD
- Not in first remission at transplant: much shorter DFI (Gareau 2022: the 3 not-in-remission survivors had median DFI 25 d; 2 of 5 relapsed-before dogs died in hospital).
- Stage/substage: no effect on OS in T-cell (p=0.59/0.13).
- TBI dose: no effect between 8.4 and 13.5 Gy (Appelbaum 1985, Deeg 1985) or 10 vs 12 Gy (Gareau 2021) or 10 vs 11 Gy (Warry), while TRM rises.
- Harvest contamination is an unresolved alternative: PARR-negative harvest in 8/8 (Gareau 2021) and 13/14 (Warry) of PARR+ tumours, yet about 65-70% relapse; one dog with PARR+ blood at harvest was cured. PARR is not a sensitive purge assay, so "PARR-negative graft" does not exclude contaminating cells. No canine purging paper for lymphoma HCT was found beyond a cytogenetic long-term-culture report (PMID 2397754: 6 of 6 lymphoma marrows showed no persisting clone in 3-wk culture-derived CFU-GM; not applied clinically).
- MRD after transplant: no canine post-transplant MRD series found (only PARR at harvest).

### 3.5 Other transplant types
- Haploidentical: a single haploidentical recipient appears (in the Benedict necropsy series, died). Research-dog data are poor: Sandmaier 1996 (8605371): all 9 DLA-haplo PBSC recipients died of fatal hyperacute GVHD without post-graft IS, and 3/9 DLA-identical recipients had fatal GVHD without IS; Georges 2001 (11719387): all engrafted haplo dogs developed multiorgan GVHD; Zorn 2009 (19446000): donor lymphocyte infusion on days 3, 7, 14 post haplo produced fatal GVHD (CD6-depleted marrow tolerised). Haplo-HCT in dogs is a research setting.
- Nonmyeloablative: Hogan 2003 (12931117): 2 Gy TBI + SRL/CSP gives stable mixed chimerism in DLA-identical dogs (5/6 durable); 1 Gy fails (5/5 rejected). No dog lymphoma outcome with nonmyeloablative HCT found.
- Cord blood: nothing in dogs found.
- Donor lymphocyte infusion: donor aliquots cryopreserved for relapse (Gareau 2022); no DLI outcome series found.
- 211At-anti-CD45 conditioning: healthy dogs only (PMID 26338894, 39025648): lymph-node absorbed dose 3.4 Gy per 166 MBq, marrow 2.4, blood 3.1 (PMID 26338894); all 17 dogs engrafted haplo PBSC but durability variable, 12/17 alive >30 d (39025648); transient hepatic toxicity, one dog euthanised d136 with ascites. Not tested on lymphoma.

## 4. (B) Mechanism and how to put each piece in a per-day-kill model

### 4.1 Radiation (TBI) as a dormancy-independent kill
Evidence for cycle independence: Maeda 2016 (27257868, full text): across 27 canine lines SF2 had no correlation with S-phase fraction, doubling time, ploidy or chromosome number; 4 lymphoid lines (1771 / OSW / CLBL1 / CLL1390): plating efficiency 0.65/0.44/0.37/0.63, SF2 0.75/0.61/0.53/0.85, SF5 0.27/0.15/0.06/0.36 (matches the repo inputs). Suspension lines were scored by limiting dilution, not colonies. The paper notes human lymphoid lines reach SF2 as low as 0.038, so four canine lines may understate lymphoma radiosensitivity. All tested lines are log-phase and cycling; no quiescent-cell canine assay exists. Human support: indolent (low-proliferation) follicular lymphoma responds to 2 x 2 Gy (55% CR in irradiated sites, apoptosis; PMID 20970029). That is a TRANSFER from a bcl-2-driven apoptosis-prone indolent disease and does not show that an aggressive canine persister is killed equally.

Kill numbers derived here with the repo's LQ solver on those four lines (acute fractions, no repair between, no dose-rate sparing, no repopulation; upper bounds):

| TBI | e-folds, four canine lymphoid lines (CLBL1 / OSW / 1771 / CLL1390) | same with in-vivo dose-modifying factor 1.9 (PMID 3009370) |
|---|---|---|
| 2 x 4 Gy (alloHCT) | 3.85 / 2.68 / 1.78 / 1.30 | 1.37 / 1.06 / 0.62 / 0.36 |
| 2 x 5 Gy (NCSU auto) | 5.63 / 3.79 / 2.62 / 2.03 | 1.94 / 1.45 / 0.89 / 0.56 |
| 2 x 6 Gy | 7.73 / 5.08 / 3.61 / 2.93 | 2.60 / 1.88 / 1.20 / 0.81 |
| 1 x 13.5 Gy | 16.98 / 10.18 / 8.05 / 7.40 | 5.22 / 3.36 / 2.45 / 2.05 |

So 10 Gy TBI is a pulse of about 2-5.6 e-folds (0.9-2.4 log10) in vitro, and about 0.6-1.9 e-folds if the 1.9x in-vivo penalty applies. Grade: DERIVED (canine cell measurement, LQ arithmetic) with a TRANSFER component for the in-vivo factor (human xenografts, Malaise 1986).

Reality check that the derivation FAILS: LQ predicts about +5 to +11 e-folds (2.3-5 log10) going from 2 x 5 Gy to a single 13.5 Gy; clinical relapse did not fall (Appelbaum 1985, Deeg 1985; dose rates differed, 2-4 cGy/min, which lowers effective kill and is a caveat). So the LQ-derived kill is not what limits TBI outcome. Explanations not distinguishable from the record: graft contamination (raised by Deeg 1985), non-uniform dose or sanctuary sites, a radioresistant clone/subpopulation, or high-dose LQ extrapolation breaking down. Human clonogenic data lean toward the radioresistant clone explanation: primary T-lineage ALL/NHL cells have SF2 0.36 +/- 0.04 (CD3+ 0.44 vs CD3- 0.19), and after TBI-ASCT 16 of 19 CD3+ patients relapsed vs 3 of 8 CD3- (PMID 1429095). Also B-lineage ALL CD24- blasts have D0 median 239 cGy (PMID 8443393). Not tested for dog lymphoma.

Representation: TBI is a pulse (2 days), not a 14-day rate. The repo spreads it over 14 d (0.145/day for the most resistant line). Either is an arithmetic convention; the clock should apply the e-folds once. Do not let the model credit TBI with marginal kill above about 10 Gy: it is contradicted by outcome data.

### 4.2 The stem-cell graft as marrow rescue (autologous)
- No kill; the graft lets the marrow axis tolerate TBI that would otherwise be lethal (dogs survive 700 cGy with care, die at >=800 cGy without HCT: PMID 19747631). CD34+ dose: adequate engraftment with >2 x 10^6 CD34+/kg; neutrophils >1000/uL by day 9-18; thrombocytopenia persists weeks (PMID 21670196, 22882500, 24467413).
- Represent as: toxicity-budget modifier on marrow (raises the marrow ceiling for a TBI pulse) plus a transplant-related-mortality competing hazard, not an agent with potency. Repo already has TRM; add the modern figure (Section 7).
- Risk the graft re-seeds disease: unresolved (Section 3.4).

### 4.3 Purging
Nothing clinical. A cytogenetic study (PMID 2397754) found no marker clone in CFU-GM after 3-week marrow culture in 6 lymphoma dogs (plus 1 leukaemia); it was never tested as an HCT purge. Grade: not evidenced for clinical use.

### 4.4 Lymphodepletion enabling adoptive cells and immune reconstitution
- After TBI+autoHCT, humoral and cellular immune reactivity was impaired for about 10 weeks (PMID 1095380, old Seattle series).
- Autologous expanded T cells after CHOP persisted about 49 d and gave DFI 338 vs 71 d vs 12 historical dogs (PMID 22355761 as quoted in PMID 34950726; n=8).
- After TBI + autoHCT, expanded T cells infused at median d74 gave no added benefit (PMID 34950726). Product differences (CD4:CD8 about 2:1 vs about 1:9), dose and schedule make comparison unsafe. So lymphodepletion-enabled ACT has no positive canine evidence within transplant.
- Represent as in the existing ACT/CAR-T entries (persistence cap 14-50 d); do not credit TBI with extra ACT potency.

### 4.5 Allogeneic graft-versus-lymphoma (GVL)
Dog evidence: Gareau 2022 (full text): donor cells reach >95% chimerism within 2 weeks; acute GVHD mild (grade 2 skin, 3/13 discharged dogs), no chronic GVHD; lymphoma death in first-remission dogs 1/9 vs about 65% relapse after auto; conditioning was only 2 x 4 Gy. The authors' own prior: DLA-identical GVL is "beneficial", mediated by minor histocompatibility antigens (DLA-identical, so not MHC-mismatch).
Human transfer: AATT (39270145): cumulative progression/relapse 8% (alloSCT, n=26) vs 55% (autoSCT, n=41), NRM 31% vs 3%, 7-y EFS 38% vs 34%; Corradini 2004 (15169805): RIC alloSCT in relapsed PTCL, 3-y OS 81%, PFS 64%, NRM 6% at 2 y (n=17); Weiden 1979 (34792): relapse 2.5x lower with GVHD in human leukaemia.

| Escape | Covered by DLA-identical alloHCT? | Basis |
|---|---|---|
| P-gp / efflux | Yes (T/NK killing is not drug-dependent) | mechanism, TRANSFER |
| CD20/CD19 loss | Yes (not antigen-specific to B lineage targets) | mechanism, TRANSFER |
| Non-cycling persister | Plausibly yes (T cells kill non-cycling cells; needs MHC + minor-H antigen display) | TRANSFER; no canine data |
| MHC-I loss | No for DLA-identical (minor-H presentation needs MHC); NK missing-self in graft might help but no data | TRANSFER (Vago 2009, PMID 19641204 for HLA loss after haplo) |
| MHC-II loss / low | Partly no: low class II predicts poor outcome in canine B-cell lymphoma (PMID 21781170); class II down-regulation is a documented post-allo relapse route in humans (PMID 32158444) | TRANSFER |
| CNS / testis sanctuary | Unknown; no canine data found | not found |
| Apoptosis evasion (TP53, BCL2 family) | Likely yes: perforin/granzyme, Fas (no canine data) | TRANSFER |
| Founder TP53/TRAF3 lesions | Not relevant to immune kill | - |

Haploidentical/mismatched GVL would cover MHC-mismatch antigens but has lethal GVHD in dogs without protocols that are still research. GVHD cost in DLA-identical dogs: mild in the 15-dog series; DLI given early after transplant is lethal in haplo dogs (PMID 19446000); cyclosporine toxicity in 1 dog (diabetes); factor V inhibitor in 1 (PMID 32686109). MSC did not prevent GVHD (Section 6).

### 4.6 Human autologous-consolidation analogs (plateau and cure fraction)
- DLBCL relapsed, chemosensitive, PARMA (7477169): 109 randomised; 5-y EFS 46% vs 12%, OS 53% vs 32% (63 mo follow-up); 3 toxic deaths in 55 transplanted. Rituximab era, CORAL (20660832): 3-y EFS 21% if prior rituximab, 20% if relapse <12 mo, 45% if >12 mo. So in the modern era the transplant plateau is lower and early-relapse dependent.
- PTCL first-remission ASCT: NLG-T-01 (22851556): n=160, 5-y OS 51%, PFS 44%, TRM 4%; German prospective (19029417): 3-y PFS 36% ITT; extension (27471868): 5-y OS 44%, DFS 54%, PFS 39% (n=111); Stanford (18541192): 5-y PFS 51% if CR1/PR1 (n=15), 12% if CR2+.
- Take-home for dog transfer: human auto-HCT plateaus at about 35-50% in favourable settings, similar to the dog 33-40%; allo reduces relapse to single digits in T-cell lymphoma but with about 31% NRM.

## 5. (C) "Cancer stem cell" / lymphoma-initiating cell in canine lymphoma

What exists:
- Ito 2011 (21777289, full text): lymphoid progenitor cells (CD34/KIT/CD133 with CD45 and CD22) were 0.16-2.10% (mean 0.89%) of nodal lymphocytes in 24 B-cell lymphoma dogs vs 0.12-0.25% (mean 0.20%) in 6 normal dogs (p=0.0022). They carry the same clonal IgH rearrangement as bulk tumour. Side-population cells were separate (did not express the progenitor markers). 3 of 3 attempted primary tumours engrafted in NSG mice and kept the progenitor fraction. Not shown: that these cells alone initiate tumour, are quiescent, or drive relapse. Authors say the sample is too small for prognostic significance.
- Hartley 2018 (30238600, full text): 44 untreated lymphoma dogs, 11 relapsed, 13 normal. Malignant B cells have more CD34/CD90/CD117/Oct3/4-positive cells; T-cell tumours differ (mainly Oct3/4, CD90 down). In vitro selection with doxorubicin/vincristine/dexamethasone raises CSC markers, ALDH activity and doxorubicin efflux; spheres in OSW but not 1771; Oct3/4 expression 33% in relapsed vs 15% in untreated B-cell (preliminary, small n).
- Side population: Kim 2013 (23820219) found SP fractions in canine lymphoma lines with Bmi-1, ABCG2, phospho-P-gp, but SP was not reduced by verapamil or fumitremorgin C. Tomiyasu 2012 (23167606): SP cells had higher ABCB1 and LRP than main population, MAPK/ERK-dependent.
- Liu 2015 (25964560): Melk high in CLBL-1 and primary B-cell lymphoma; spheres have higher Myc. Wilkerson 2005 (15963817): 3 of 30 B-cell cases CD34+. Rao 2011 (21781170): CD34 expression not associated with outcome in 160 dogs.

Is it the same as the model's drug-tolerant persister pool? Partly, not wholly:
- Overlap: efflux (ABCB1/LRP) and ALDH are drug-tolerance mechanisms that the model already carries as the P-gp lineage (the "bar", about 0.09/day). The ledger already classes chemo-selected stem-like cells as a variant of the persister (ledger l.80).
- Not shown: dormancy. No canine study measured cell-cycle state, label retention or drug tolerance in vivo for the CSC-marker-positive cells. The "persister awake fraction f" in the model stays unmeasured.
- So CSC markers are a phenotype; they do not add a new escape class beyond efflux/ALDH/dormancy as already modelled. Do not add a separate "stem cell" escape without a mechanism that the current 13 lineages miss.

What kills them, from this sweep: no canine study tested killing of the marker-defined cells. Candidates already in the catalogue apply by mechanism (radiation: cycle-independent in canine lines; venetoclax; XPO1 inhibition; HCQ; immune effectors). New item found: CD47 blockade + canine anti-CD20 cured 100% of mice bearing canine lymphoma xenografts (PMID 27856424; macrophage effector, mouse xenograft only, n not given in abstract). Graded TRANSFER for dogs at best; it is an antigen-dependent (CD20) combination, so CD20 loss still escapes the anti-CD20 arm, while CD47 blockade alone had single-agent activity.

## 6. (D) Mesenchymal and other stem-cell-derived products

- MSC: no canine lymphoma therapeutic role found. Dog data are supportive/immune only: MSC did not prevent GVHD or rejection after DLA-haplo BMT (PMID 20816818: 50% rejected, 50% fatal GVHD, survival about superimposable with controls, 18 vs 15 d); MSC were safe in DLA-identical HCT (PMID 23723082); canine adipose SVF suppressed PBMC proliferation (including PBMC from lymphoma dogs) in vitro (PMID 41319893). Effect direction on GVL is unknown; immunosuppression could blunt GVL. MSC are being used as vehicles for oncolytic virus or IFN-beta gene in solid-tumour models (PMIDs 32664672, 24040358, 26254365), not lymphoma.
- iPSC: canine iPSC differentiate to red cells (PMID 42472629) and platelets (PMID 23409943). No iPSC-derived canine NK/T cell product found.
- Gene-modified HSC for CAR in dogs: not found. Dog HSC gene transfer exists only for X-SCID (PMID 17442404, 17139538).
- Off-the-shelf effectors: allogeneic iNKT persisted >=78 d in MHC-mismatched dogs (PMID 37852175; healthy dogs, not cancer, not stem-cell-derived); allogeneic expanded NK cells, 3 dogs with solid tumours, well tolerated (PMID 42461253); canine CD94-selected NK did not reliably promote engraftment or avert GVHD in haplo (PMID 33225057). Autologous CAR-T in canine B-cell lymphoma: CRS case (PMID 35898541); PD-1/CD28 switch receptor validated in vitro (PMID 39314237). None is stem-cell-derived.

## 7. Agents for the catalogue (proposals; nothing added to the repo)

Toxicity and mortality ledger: 7% in-hospital death across 94 NCSU TBI+HCT dogs (Benedict); 8.3-13% in the earlier single series (auto B, auto T, allo); Seattle era 26-55%. Main modes: sepsis incl. Candida (3 of 5 necropsied), marrow aplasia, GI toxicity, TBI pulmonary fibrosis (1 dog at 8 mo), later second cancers (5x relative risk, Deeg 1983). Hospital stay mean 22 d (allo series); grade 4 neutropenia in all dogs from about day 6 post-TBI, neutrophils >1000/uL by day 9-18; thrombocytopenia weeks; allo needs cyclosporine ~30 d plus GVHD watch. Procedural axis in the repo gives TBI 0.85 and marrow 0.60; that remains consistent. 10-year budgets should add a second-cancer hazard term.

| Candidate | Representation | Potency and grade | Escapes covered / not | Access | Availability |
|---|---|---|---|---|---|
| TBI pulse (2 x 5 Gy) | one-time pulse of 0.6-5.6 e-folds | DERIVED (LQ, canine lines) + TRANSFER (in-vivo factor); cannot raise above ~10 Gy per outcome data | P-gp: covered; CD20/CD19 loss: covered; persister: TRANSFER only; MHC: covered (antigen-independent); CNS/testis: not shown | whole-body photon field; dosimetry verified at 5 sites (PMID 31146304) | routine at NCSU, few specialty centres; private practice sites use it |
| Autologous HSC rescue | marrow-axis modifier + TRM hazard | no potency; engraftment measured | none directly | n/a | routine at those centres; apheresis needs machine, cyclophosphamide/G-CSF mobilisation |
| Auto-HCT outcome entry (existing) | 2 y remission 33-40% B, 15% T | OUTCOME | - | - | as above |
| DLA-identical allo-HCT + 2 x 4 Gy | persistent donor immune effector; per-year relapse hazard about 0.03/yr crude vs about 0.5/yr auto | OUTCOME only. Crude: 1 lymphoma death in about 31 dog-years (9 dogs x ~3.4 y median); exact Poisson 95% CI about 0.001-0.18/yr. Auto about 0.5/yr from 65% relapse over 2 y. Both crude; n tiny | P-gp, CD20 loss: yes by mechanism; MHC-I/II loss: no; CNS: unknown | donor cells traffic widely; no canine CNS data | buildable/centre-specific: commercial DLA typing exists; needs matched sibling (25% chance per sibling), 4 centres have done it |
| DLI from cryopreserved apheresis | rescue effector | no outcome series | as GVL | - | possible, unverified |
| Reduced-intensity allo (2 Gy) | as alloHCT, less conditioning kill | not tested in lymphoma dogs; chimerism OUTCOME in healthy (PMID 12931117) | same | - | research |
| Haploidentical | - | GVHD fatal without protocols (8605371, 11719387, 19446000) | - | - | research only |
| 211At-anti-CD45 conditioning | targeted alpha pulse | TRANSFER; dosimetry measured in normal dogs (3.4 Gy/166 MBq to node) | covers CD20/CD19 loss (CD45 pan-leukocyte) | lymph node/marrow uptake | research; hepatic toxicity |
| MSC | none | none | none | - | supportive only |
| Stem-cell-derived NK/T, gene-modified HSC CAR | none exist for dog lymphoma | - | - | - | not found |

Dormancy: TBI and alloreactive T cells are the only stem-cell-linked mechanisms that are not division-gated; neither has been measured against a canine quiescent pool.

## 8. What each mechanism does and does not close (escape matrix, strength stated)

- Closes at OUTCOME strength only: a subset of dogs stays disease-free >=2-8 y after TBI+auto (15-40%) or alloHCT (8/9 in first remission). No per-escape attribution exists.
- Covered by mechanism (TRANSFER): TBI vs P-gp, CD20/CD19 loss; allo-GVL vs P-gp, CD20 loss, persister.
- Not covered: MHC-I/II loss with DLA-identical GVL; CNS sanctuary (no canine evidence for either TBI dose to brain or GVL there); T-cell disease (auto 15%; allo no series); the unexplained radiation-independent relapse after TBI (Section 4.1).
- The model's closure logic should not be told "TBI closes the persister": that is ASSUMED/TRANSFER, contradicted by dose-escalation outcomes.

## 9. Searched and NOT found

- Canine lymphoma: any 5-year or 10-year actuarial transplant survival; any dog with documented 10-year disease-free follow-up; relapse-site pattern (nodal vs CNS vs marrow) after TBI; MRD kinetics after HCT; concurrent CHOP-alone controls for transplant; randomised transplant trials; T-cell alloHCT series; haploidentical or cord-blood HCT in client dogs; nonmyeloablative/RIC HCT in lymphoma dogs; DLI outcome series; canine purging study; Japanese, Italian or Spanish HCT series for canine lymphoma (only Perth/Australia PMID 22620705, Tufts PMID 16594594 found besides NCSU and Seattle); canine quiescent-lymphoma-cell radiosensitivity; in vivo canine lymphoma SF2; canine MHC-loss relapse after allo; CNS GVL in dogs.
- CSC: any canine functional test that marker-defined cells are solely tumour-initiating, quiescent, or responsible for relapse; any drug tested against canine lymphoma CSC-marker cells; human DLBCL CSC hierarchy literature (search returned only generic hits; not reviewed).
- Stem-cell products: MSC with anti-lymphoma effect; iPSC-derived canine immune cells; HSC-engineered CAR dogs; stem-cell-derived NK/T in dogs.
- Human: a verified citation that 2-year disease-free implies 10-year (not retrieved); human DLBCL ASCT plateau at 10 y (not retrieved).
- Tools: bioRxiv search has no keyword function, so preprints were not hunted; search engine behaved poorly on multi-term queries (automatic AND), so some literature may have been missed. PMIDs 28420, 387112, 6997586 have no abstracts in PubMed, so their numbers are unknown. Willcox 2012 full text is not in PMC and was read only as an abstract; the EDEN MCP server needs authorisation and was not used.

## 10. Suggested follow-up (for the user's decision, not done)

1. Add `allogeneic DLA-identical HCT (2 x 4 Gy)` as a separate catalogue object with outcome-only grade, persistence unlimited, mismatch/MHC escapes left open. Do not call it closure.
2. Correct the Gareau/ACT sentence in `LYMPHOMA_DURABLE_RESPONSE.md` and the layman page.
3. Change the TBI agent: pulse form (not 14-day rate) and a cap on credited kill above about 10 Gy; state the failed-LQ check in the ledger.
4. Add modern TRM (7%; 8-13%) and a second-cancer hazard for long horizons (5x relative risk in dogs, PMID 6355021).
5. Ask the NCSU group (not literature) for 5- and 10-year status of the first-remission alloHCT and autoHCT cohorts; that is the only way to replace the 2-year definition.
