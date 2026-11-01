# CNS-lymphoma regimens: real-data routes to durable CNS remission (FINAL)

Success criteria (user's words, verbatim, graded against exactly these): "make sure every mechanism and every escape is closed by either real data or rigorous model, potency, toxicity etc all need to be considered"; "looking for 10+ years of durability"; "assuming early detection"; "I'm okay with no specific data but if scientifically sound" (transfer allowed if justified in writing and graded TRANSFER; no-basis numbers stay ASSUMED). Brain-agent requirement from the task: non-division-gated, not a P-gp/BCRP substrate, not dCK-dependent, not CD20/CD19-alone, kill >= ~0.10/day (>= 0.19/day at half access).

Method: PubMed MCP (search + get_article_metadata). Every PMID below was fetched in this session. Quotes are from returned abstracts. Two non-PubMed sources are labelled WEB (FDA clinical-pharmacology review of Tepadina, NDA 208264). Anything from memory is labelled RECALLED-UNVERIFIED and must not be cited.

Record check (CLAUDE.md rule 1), on origin/claude/duplicate-codex-prefix-branch-lt1qh6 (docs/LYMPHOMA_*.md, src/**/lymphoma_*.py):
- ALREADY COVERED: canine allogeneic DLA-identical HCT (UNIVERSE: "8 of 9 first-remission dogs >4 y ... longest 2920 d"; matches PMID 35789057 here); autologous TBI+HSCT; cytarabine (IT, CRI; PMID 1742843 CSF:plasma 0.62 is in the model); PMIDs 22210944, 37732143, 8164885 are cited in lymphoma_grounded.py; lomustine in catalogue (ASSUMED, "one line IC50, no canine PK"); CAR-T persistence 14-50 d in dogs; CNS sanctuary section and "CNS B-cell closure only with CD20 CAR-T + craniospinal RT + HBI on assumed potencies".
- NOT COVERED (grep of those files returns zero hits): thiotepa, busulfan, carmustine/BCNU, nimustine, PMID 37756055 (two canine CNS-lymphoma long-term survivors on nimustine + prednisolone), lenalidomide/pomalidomide, HDC-ASCT as a CNS-directed consolidation, reduced-dose WBRT trial data, human late-relapse / clonal-persistence data. These are the new items below.

======================================================================
## 0. HEADLINE (read this first)

1. The only real-data human regimens with documented 5-10+ year CNS remissions are (a) HD-MTX/ara-C-based chemo +/- intraventricular therapy, (b) the same plus WBRT (standard or reduced dose), (c) the same plus thiotepa-containing HDC-ASCT. None has a >10-year plateau shown for HDC-ASCT specifically (longest follow-up found: PRECIS median 8 y). Decade-plus survivors exist only in pre-ASCT cohorts (Bonn 20 y: 17% alive; MATILDE+WBRT 12 y: 8/41 disease-free >10 y; C5R: 3/43 disease-free at 27-44 y) and they ALSO show late relapses to 21 y, i.e. the quiescent clone is not eliminated in everyone.
2. Thiotepa is the best-supported brain agent on every criterion the model asks for EXCEPT transporter status and canine data. CSF:plasma AUC ~1 (n=1 patient with reservoir), alkylator (acts independent of dCK; division-independence is general pharmacology, not shown by a PMID here), protein binding <=20%. P-gp/BCRP substrate status: NOT FOUND (FDA review lists "Substrate transporter systems [in vitro]: Not provided"). Canine thiotepa PK/transplant use: NOT FOUND.
3. The strongest quantitative object that can go into the model is OUTCOME-graded and independent of any potency assumption: three separate randomised comparisons all show each strong consolidation adds ~0.85-1.0 e-fold of residual-cell kill over the next-best alternative, and the whole human program (MATRix + BCNU/TT ASCT) implies an average effective brain kill of about 0.13-0.21/day over ~115 days for assumed residual burdens 1e6-1e10 cells (section 9). That sits at the user's 0.10-0.19/day bar, but it is an average over a multi-agent program with the brain access already inside it; it is not a per-agent potency and not division-gating evidence.
4. Real canine durable CNS survivors: n=2 (nimustine + prednisolone, >2583 d and 1218 d, PMID 37756055). Case-report strength.
5. Which CNS cells survive: no study isolates them. Indirect human data: same IG clone at relapse 13.8 y later (n=1 of 3 tested), relapses at 9.8, 10.3, 13.3, 21.0 y that re-respond to HD-MTX (dormancy/persistence, not selected resistance), and PCNSL-specific escapes: HLA loss/6p LOH, RFC promoter methylation (MTX transport), TP53/BTG1/ETV6, CARD11/CD79B for BTK inhibitors.

======================================================================
## 1. HDC-ASCT with thiotepa (MATRix/IELSG43, IELSG32, TBC, BEAM-variants)

### Verified citations and numbers
| PMID | design | key numbers (quoted/derived from abstract) |
|---|---|---|
| 42486133 (Lancet 2026, DOI 10.1016/S0140-6736(26)00917-7) | MATRix/IELSG43 RCT, n=229, ASCT (BCNU-TT) n=114 vs R-DeVIC n=115, median FU 45.3 mo | "3-year progression-free survival was 78% (95% CI 69-85) in the HCT-ASCT group compared with 51% (41-60) in the R-DeVIC group"; HR 0.43 (0.27-0.68). Fatal SAEs after consolidation: 5 ASCT (4 infections, 1 PE) vs 2 R-DeVIC (both AML). |
| 35562406 (Leukemia 2022) | IELSG32, FU 88 mo | "7-year OS of 21%, 37%, and 56% respectively for arms A, B, and C ... patients treated with MATRix and consolidation had a 7-year OS of 70%". "Salvage therapy was ineffective; benefit was recorded only in patients with late relapse re-treated with methotrexate. Eight (4%) patients developed a second cancer." |
| 29054815 (Lancet Haematol 2017) | IELSG32 second randomisation n=118 | 2-y PFS WBRT 80% vs ASCT 69% (HR 1.50, p=0.17); conditioning carmustine 400 mg/m2 d-6 + thiotepa 5 mg/kg q12h d-5,-4; two toxic deaths (infection), both ASCT. |
| 35834762 (JCO 2022) PRECIS | randomised phase II, TBC-ASCT n=44 vs 40 Gy WBRT n=53, median FU 8 y | "8-year event-free survival ... 67% and 39% in the ASCT and WBRT arms (p=.03) ... risk of relapse after ASCT (HR 0.13; p<.001)". "Five and four patients died of ASCT and WBRT-related toxicities, respectively." 8-y OS 69% vs 65% (NS). "Balance (52% vs 10%) and neurocognition (64% vs 13%) significantly deteriorated after WBRT compared with ASCT". |
| 22023529 (Leuk Lymphoma 2011) | TBC upfront, n=21, no WBRT | "11 of 21 (52%) alive and progression-free at median follow-up 60 (7-125) months"; "Treatment-induced neurotoxicity was not observed"; 3 early TRM, all >60 y and poor PS. |
| 12692608 (BMT 2003) | TBC, n=7 | 5 alive relapse-free at 5-42 mo; no neurotoxicity; "high-dose chemotherapy for PCNSL should include drugs that penetrate the CNS such as busulfan and thiotepa rather than standard lymphoma regimens such as BEAM" (authors' opinion; BEAM data themselves NOT FOUND in this search). |
| 42139822 (Eur J Cancer 2026) | BET (carmustine-etoposide-thiotepa), n=60, FU 51 mo | 4-y PFS 66%, OS 74%; TRM 3.3%; of 15 relapses "10 within the first 12 months, while 2 patients (13.3%) 3.6 years and 7 years after ASCT". |
| 41108618 (Hematol Oncol 2025) | Czech real-world MATRix | 4-y PFS 53%, OS 55%; "treatment-related mortality was 8%". |
| 40275355 (J Hematol Oncol 2025) | MATRix-like, n=146 | "51.1% reached PFS24, with a subsequent 5-year OS of 96.7%. ... the annual hazard rate for progression and death decreased to under 5% after 24 months, remaining stable thereafter." |
| 37563283 (BMT 2023) | CIBMTR, TT-BCNU n=218 | thiotepa 10 vs 20 mg/kg total: 3-y PFS 71% vs 80% (NS), NRM 6% vs 4%: "thiotepa dose-intensity ... does not impact ASCT outcomes". |
| 35459424 (Leuk Lymphoma 2022) | SECONDARY CNS lymphoma, TBMR, n=62 | median FU 5.7 y; 5-y PFS 53%, OS 65% overall; 62% / 73% for those transplanted. |
| 33513372 (Lancet Haematol 2021) MARIETTA | secondary CNS DLBCL, MATRix-RICE then BCNU-TT ASCT | 1-y PFS 58%; 2-y OS 46%; TRM 5% (4 sepsis deaths). |
| 28581466 (BMT 2017) | UK, n=70 | TRM 6%; 2-y PFS 71.5%. |

Durable fraction / plateau: 3-y PFS 78% (IELSG43), 7-y OS 70% (IELSG32 consolidated), 8-y EFS 67% (PRECIS TBC). Plateau beyond 5 y: partial. No cohort with >=10 y of follow-up for thiotepa-HDC found (NOT FOUND). Late relapse after ASCT exists (2 of 60 at 3.6 and 7 y, PMID 42139822).
Treatment-related mortality: 3-8% across series (3.3%, 5%, 6%, 8%); older/poor-PS >60 y drive it.
Neurotoxicity: not increased vs. non-ASCT; PRECIS and IELSG32 show cognition preserved or improved after ASCT; PMID 39615656 (MSK atrophy, n=139) found accelerated atrophy after ANY consolidation (4.3% vs 1.8%/y healthy) with no difference by strategy.
Marrow: obligatory aplasia (needs graft). Second cancers 4% (IELSG32) .
Pharmacology see section 8.

======================================================================
## 2. WBRT (standard and reduced dose)

| PMID | numbers |
|---|---|
| 20970380 (Lancet Oncol 2010) G-PCNSL-SG1, 551 randomised | HD-MTX +/- 45 Gy WBRT: median PFS 18.3 vs 11.9 mo (p=0.14), median OS 32.4 vs 37.1 mo (HR 1.06); "Treatment-related neurotoxicity in patients with sustained complete response was more common in patients receiving whole brain radiotherapy (22/45, 49% by clinical assessment; 35/49, 71% by neuroradiology) than in those who did not (9/34, 26%; 16/35, 46%)". |
| 25716362 (Neurology 2015) | final report, FU 81.2 mo: ITT PFS 15.4 vs 9.9 mo (p=0.034); OS no difference. |
| 28434043 | QoL and MMSE worse in early-WBRT arm in year 2. |
| 24101038 (JCO 2013) R-MPV + rdWBRT 23.4 Gy + ara-C | n=52; CR pts (n=31) 2-y PFS 77%, median PFS 7.7 y; median OS not reached (FU of survivors 5.9 y); "Fazekas score <=3 in all 28 MRIs"; cognition stable. |
| 41189315 (Neuro Oncol 2026) R-MPV-A +/- LD-WBRT 23.4 Gy, randomised n=91 | median PFS not reached vs 2.1 y, HR 0.47 (p=.007); 2-y PFS 78.7% vs 54%; OS NS (HR 0.71); "no differences in cognitive outcomes". |
| 39167801 (Blood Adv 2024) MSK n=559 | RD-WBRT/AHCT median PFS and OS not reached in RPA class 1; "No significant adjusted survival differences were seen across consolidation strategies". |
| 39615656 (IJROBP 2024) | atrophy not different for RD-WBRT (<=24 Gy) vs ASCT vs nonmyeloablative. |
| 24634458 (Neurology 2014) MATILDE + WBRT | n=41, median FU 144 mo, 5-y PFS 24%, 9 alive and disease-free (8 at >10 y); late relapses at 100 and 101 mo; MMSE >=29 in all but one at 10 y. |
| 42685570 (Eur J Cancer 2026) C5R, 20 Gy WBRT + 30 Gy boost | n=43, median FU 35 y: 3 disease-free at 27, 28, 44 y; neurocognitive deterioration projected 60% at 20 y; second cancers 28% at 20 y; deaths: PCNSL 24, neurotoxicity 5, second cancer 5 of 43. |

Mechanism: ionising radiation kills by DNA damage independent of cell cycle phase (division-gating weak), tissue access 1.0 (no BBB). It adds ~0.9-1.0 e-fold over the next-best consolidation (section 9). Weakness: standard-dose neurotoxicity (49-71% in sustained CR; PRECIS 64% neurocognitive decline at 8 y). In a dog the cognitive endpoint is unmeasurable and lifespan shorter, so neurotoxicity weighs less, but radiation potency in the repo is already DERIVED (and lower than assumed 0.30).
Dog translatability: canine radiotherapy infrastructure exists (TBI 10 Gy with 6 MV photons implemented, PMID 31146304; brain RT used for glioma in dogs, PMID 40216556 case). Craniospinal canine lymphoma data: NOT FOUND.

======================================================================
## 3. HD-MTX-based induction and durable fractions (no ASCT/WBRT)

- 32989105 (Neurology 2020) Bonn protocol (systemic + intraventricular MTX/ara-C, no WBRT), n=65, median FU of survivors 19.6 y: "11 (17%) were still alive. Six of those never experienced any relapse ... 10-year OS rate ... 29% and the estimated 20-year OS rate was 19%. Four late relapses were observed after 9.8, 10.3, 13.3, and 21.0 years." Class III evidence. => ~6/65 (9%) relapse-free at ~20 y.
- 39902392 (Neurooncol Adv 2025) modified Bonn (R/HD-MTX/IFO + intrathecal MTX/ara-C), n=43: median PFS 102.8 mo, 5-y OS 76%; of 18 who relapsed and got second-line, a second relapse in 11/18.
- 35562406 arm A (MTX + ara-C): 7-y OS 21%; arm B (+R) 37%; arm C (MATRix, +thiotepa) 56%. Quote: the thiotepa/rituximab additions improved 7-y OS stepwise. Arm C includes only ONE thiotepa dose (30 mg/m2) per cycle.
- 38037691 (Neuro Oncol 2024) HOVON 105: 5-y OS 49% (MBVP) / 53% (R-MBVP), FU 82.3 mo; rituximab added nothing; cognition stable to 60 mo except motor speed.
- 26951382 (LOC, 563 first-line): 46% relapsed/refractory (16.5% relapsed, 29.0% refractory).
- 40275355: plateau after PFS24 (hazard <5%/y).
Late relapse (the persistence signal): 21372070 (Neuro Oncol 2011): "10 of 230 relapsed patients ... relapse >=5 years ... Late relapses accounted for 4% of all recurrences"; "1 had the identical clone at initial diagnosis and relapse 13.8 years later, and the other 2 were uninformative"; "Nine achieved a complete response to salvage therapy". 21868233: relapse 13 y after Bonn re-responded to HD-MTX again. 24634458: relapses at 100, 101 mo.

======================================================================
## 4. BTK inhibitors, IMiDs

| agent | PMID | numbers | CNS penetration | P-gp |
|---|---|---|---|---|
| ibrutinib (r/r) | 38995739 (Clin Cancer Res 2024) | n=46 (31 PCNSL, 15 SCNSL), FU 49.9/62.1 mo: ORR 74% PCNSL, 60% SCNSL; "median PFS for PCNSL was 4.5 months ... 1-year PFS at 23.7% ... median duration of response in the 23 PCNSL responders was 5.5 months"; TBL1XR1 mutation associated with long-term response; "Clearance of ctDNA from cerebrospinal fluid was associated with complete and long-term ibrutinib responses." | CSF/brain numbers: NOT FOUND in PubMed abstracts retrieved (Grommes 2017, PMID 28619981, reports 10/13 PCNSL responses, 5 CR; abstract gives no CSF levels). Mantle-cell paper states ibrutinib "penetrates the blood-brain barrier" without a number (PMID 35789260). | NOT FOUND |
| ibrutinib resistance | 28619981 (Cancer Discov 2017) | "The only PCNSL with complete ibrutinib resistance harbored a mutation within the coiled-coil domain of CARD11"; CD79B mutation = incomplete responses. | | |
| tirabrutinib | 38690230 (Neurooncol Adv 2024) | n=44, FU 37.1 mo: ORR 63.6%, median DOR 9.2 mo, median PFS 2.9 mo, PFS rate 13.9%, OS rate 56.7% at the cut; "deep and durable response in a subset". | NOT FOUND | NOT FOUND |
| BTKi maintenance | 41770393 (J Neurooncol 2026), retrospective n=71 | BTKi (n=23) 6-y PFS 91.3% vs lenalidomide (n=48) 41.5%; FU 41.2 mo. Small, selected, retrospective. | | |
| ibrutinib + R + HD-MTX | 41114362 (Front Oncol 2025) | pilot n=9, FU 77.6 mo, 5-y PFS and OS 77.8%, 8 in sustained CR. | | |
| lenalidomide | 29986852 (Blood Adv 2018) | 14 refractory pts: 9 better than PR; 6 response >=9 mo, 4 >=18 mo; median PFS (len/R) 6 mo; "The CSF/plasma partition coefficient of lenalidomide was >=20% at 15- and 20-mg dose levels". | 35732975: 1.3-2.4% CSF:plasma in 3 non-CNS heme patients (20 mg); 22109830: rhesus 11% (2 of 3 animals) | NOT FOUND |
| pomalidomide | 30262659 (Blood 2018) | n=25 evaluable: ORR 48%, median PFS 5.3 mo (9 mo responders); grade 3/4 neutropenia 21%. | 23940785: rat CNS penetration "~39%" ; mouse CNS-lymphoma activity via macrophage M2->M1 and NK | NOT FOUND |

Interpretation: BTKi and IMiDs act through signalling/immune mechanisms (not mitosis-dependent) so they are plausibly non-division-gated, but the data show responses of months, not durable cure, as monotherapy. The durable-looking BTKi results (6-y PFS 91%, n=23; 5-y 77.8%, n=9) are tiny, uncontrolled, combined with chemo. Resistance (CARD11) is a pre-existing-clone escape. Not suitable as a closing brain agent on current evidence.
Dog: the repo already carries acalabrutinib (killing modest). No canine CNS BTKi data found. Zanubrutinib canine/rat safety in PMID 32484067 (nonclinical, dogs: no toxicologically significant changes at up to 15x human AUC over 39 weeks). Not CNS-specific.

======================================================================
## 5. CAR-T in CNS lymphoma

- 38586986 (Am J Hematol 2024, LOC): 25 PCNSL infused (tisa-cel 16, axi-cel 9), FU 20.8 mo: CR 64%; "One-year progression-free survival from leukapheresis was 43% with a plateau afterward"; CRS 23/25, neurotoxicity 17/25 (68%; five grade >=3); control (n=247) median PFS 3 mo.
- 35167655 (Blood 2022): tisagenlecleucel PCNSL phase 1/2 n=12, FU 12.2 mo: CR 6/12; ICANS 41.6%, one grade 3; "sustained remission in 3/7 (42.9%) of initial responders"; "Tisagenlecleucel expanded in the peripheral blood and trafficked to the CNS."
- 40400509 (Hemasphere 2025, EBMT): 100 pts, 67 active CNS disease: 24-mo PFS 28%, OS 37%, relapse incidence 59%; NRM at 1 y 7%; CRS 83%, ICANS 42% (grade 3-4 in 17); two died of neurotoxicity.
- 37946255 (JHO 2023, SCNSL, n=61): CR 57%; 12-mo PFS 16%; ICANS 57% any, 44% grade >=3.
- 42746886 (Immunotherapy 2026 meta-analysis, 194 pts PCNSL): ORR 68%, CR 57%; PFS 52% at 6 mo and 42% at 12 mo; ICANS grade >=3 16%; TRM 5%; "long-term durability remains limited".
Longest follow-up found ~2 y; 5-10 y plateau: NOT FOUND. Mechanism: antigen-dependent (CD19), cellular, not division-gated; traffics into CSF. Escapes covered: dormant progenitors yes (if antigen+), antigen loss NO, MHC loss yes (CAR is MHC-independent). Canine: repo already records measured canine CAR-T persistence 14-50 d (anti-mouse antibodies), so durable CNS closure via CAR-T is not transferable now.

======================================================================
## 6. Allogeneic transplant

- 34293518 (Transplant Cell Ther 2021): 20 consecutive SCNSL, nonmyeloablative Flu/Cy/200 cGy TBI + PTCy: median FU 4.1 y, median PFS 3.8 y, "cumulative incidence of relapse was 25% ... nonrelapse mortality was 30% at 4 years. Of the 5 patients who relapsed, 2 were CNS only, 1 was systemic only, and 2 were combined CNS/systemic."
- 10350348 (1999): single PCNSL case, non-myeloablative alloPBSCT, disease-free 30 mo, "development of a durable graft-versus-lymphoma effect in this brain tumor" (n=1). 29559300: one case.
- 30671909 (Int J Hematol 2019): review of HSCT in PCNSL (abstract not retrieved in detail).
Graft-versus-lymphoma acts in the CNS in at least some patients (n small). NRM 30% is prohibitive for a routine route.
Canine: 35789057 (Vet Comp Oncol 2022): 15 dogs, DLA-identical allogeneic HCT: "Eight of nine remaining dogs lived >4 yrs post-alloHCT, leading to a cure rate of 89%"; median OS 1115 d (range 9-2920); "allogeneic HCT can cure ~50% more dogs than those treated with autologous HCT" (autologous "cures 33%-40%"). No CNS-specific data in the abstract. ALREADY COVERED in repo UNIVERSE (same 8/9, 2920 d).

======================================================================
## 7. Intrathecal / intraventricular

- Bonn protocol (section 3) is the best long-term dataset with intraventricular MTX/ara-C: 20-y OS 19%.
- 31466902: continuous intraventricular MTX 10 mg over 5 d, biweekly x5, n=26 (all with HD-MTX/WBRT): median PFS 59.4 mo, OS 93.8 mo; "stable concentration of methotrexate in the cerebrospinal fluid".
- 15634030 (Clin Pharmacokinet 2005): "using low drug doses, very high drug concentrations can be achieved in the CSF and relatively high concentrations in the leptomeninges but not in the brain tissue and the plasma. Therefore, this approach is not an effective treatment for bulky disease of brain tissue". Parenchymal tissue penetration limited.
- 810575 (JPET 1975, rhesus ventriculocisternal perfusion): periventricular distribution space (uL/100 mg): hydroxyurea 56, MTX 27, thiotepa 28, BCNU 64, ara-C >170; "extracellular fluid-transcapillary half-time was measured for thiotepa and BCNU (1.0 and 0.8 minute, respectively)"; ara-C "low capillary permeability".
- 38884819 (Med Oncol 2024): review of IT thiotepa: "Thiotepa has effective CNS penetration but its popularity has waned ... concerns about its efficacy and potential systemic toxicity".
- 35789260 (Blood 2022, MCL CNS relapse): "addition of intrathecal chemotherapy to systemic CNS-directed therapy was not associated with superior OS".
- Dog: 37732143 IT ara-C + MTX: "short-lasting CNS clinical remission (3 weeks)". 8164885 (beagle, 28-d continuous lumbar intrathecal baclofen via SC pump): no spinal neurotoxicity, a pump precedent only (not oncologic).
Interpretation: IT therapy is division-gated (MTX, ara-C) and CSF-compartment only; in the model it covers leptomeningeal cells, not parenchymal quiescent cells. Evidence of durability with it is confounded by systemic therapy. Real but not a stand-alone closer.

======================================================================
## 8. Thiotepa (and BCNU/busulfan/nimustine) pharmacology

| attribute | value | source | grade |
|---|---|---|---|
| CSF:plasma | thiotepa AUC ratio 1.01 and TEPA 0.95; "lumbar and ventricular concentrations which were nearly identical to simultaneous plasma concentrations" | PMID 2491958 (Cancer Res 1989, pediatric phase I; the AUC ratio is from ONE patient with a Rickham reservoir) | MEASURED (n=1; human) -> TRANSFER to dog |
| brain capillary exchange | extracellular-fluid-transcapillary half-time 1.0 min (thiotepa), 0.8 min (BCNU), rhesus | PMID 810575 | MEASURED (primate) |
| TEPA activity | "ThioTEPA and TEPA have similar alkylating activity and both exhibit outstanding central nervous system penetration" | PMID 38036843 (assay chapter, secondary) | secondary |
| plasma PK | thiotepa t1/2 0.14-0.32 h and 1.34-2.0 h; TEPA t1/2 4.3-5.6 h; dose-dependent clearance 28.6 -> 11.9 L/m2/h (25 -> 75 mg/m2); MTD bolus 65 mg/m2 (myelosuppression) | PMID 2491958; 1710167 (Phase I reevaluation: no neurological toxicity at 30-75 mg/m2) | MEASURED |
| distribution | protein binding <=20%; Vd 1.0-1.9 L/kg adults; blood:plasma 0.7-0.8; mean thiotepa t1/2 1.4-3.7 h, TEPA 4.9-17.6 h | WEB: FDA Clinical Pharmacology review of Tepadina, NDA 208264 (Reference ID 4032884) | MEASURED (label review) |
| metabolism | CYP3A4 and CYP2B6 -> TEPA; thiotepa inhibits CYP2B6 (Ki 4.8 uM, in vitro) | same FDA review; 19076156 (GST/CYP2B6/CYP3A polymorphisms affect PK) | MEASURED |
| P-gp / BCRP substrate | **NOT FOUND.** FDA review row: "Substrate transporter systems [in vitro]: Not provided." PubMed queries "thiotepa P-glycoprotein substrate", "thiotepa ABCB1 ABCG2 transporter" returned 0 records. Indirect: CSF:plasma ~1 and 1-min capillary exchange argue AGAINST strong efflux limiting access, but do not show it is not a substrate. | | UNKNOWN (indirect: DERIVED weak) |
| dCK dependence | none in the activation chemistry (direct DNA alkylation after CYP desulfuration); the dCK dependence of cytarabine is why ara-C fails | general pharmacology (RECALLED-UNVERIFIED for dCK specifically; mechanism noted in PMID 11431349: thioTEPA "induces the formation of amino-ethyl adducts of guanine" repaired by base-excision repair) | TRANSFER / mechanistic |
| division gating | alkylators crosslink DNA irrespective of cycle phase; no PubMed paper in this session measured thiotepa on quiescent lymphoma cells (query "alkylating agents quiescent cells cell-cycle independent cytotoxicity" returned only PMID 20658650, DNA interstrand cross-link repair initiation, which is not a kill measurement). Indirect outcome evidence: thiotepa-HDC reduces relapse after HD-MTX/ara-C (S-phase specific) CR (PRECIS HR 0.13 vs WBRT). | | TRANSFER (mechanism) + OUTCOME (indirect) |
| resistance escapes | base-excision repair capacity protects marrow cells from thioTEPA (11431349); acute in vivo cross-resistance after one high-dose alkylator 7-12 d earlier in EMT-6 mouse tumour: tumour "resistant to melphalan and thiotepa" after cyclophosphamide (9516940) -> do not stack alkylators too closely | | MEASURED (mouse) |
| toxicity | marrow ablation (grafted), mucositis, infections; TRM 3-8% (section 1); skin/CNS at very high dose (RECALLED-UNVERIFIED, not cited). Dose-intensity beyond 10 mg/kg adds nothing (37563283). | | |
| busulfan (dog) | IV busulfan 20 mg/kg ablates marrow, "A busulfan dose of 40 mg/kg resulted in severe central nervous system toxicity"; autologous marrow rescue worked in 4/4 dogs | PMID 10534062 (Biol Blood Marrow Transplant 1999); 7756656 (canine PK of DMSO-solubilised IV busulfan, 1 mg/kg, peak 730-1000 ng/mL); 16182176 (10 mg/kg IV before matched littermate BMT, 3 dogs, mixed chimerism) | MEASURED (dog) |
| carmustine (dog) | NOT FOUND (PubMed returned a different nitrosourea, SarCNU, PMID 11592341) | | |
| thiotepa (dog) | **NOT FOUND**: PubMed "thiotepa dogs pharmacokinetics" and "thiotepa canine" return only bladder instillation and intra-arterial tissue-distribution studies from 1964-1987 (e.g., 3117396, 4954314, 6773282). No canine systemic, CSF PK or transplant-conditioning use located. | | NOT FOUND |
| nimustine (dog) | 2 dogs, 25-30 mg/m2 IV q3-4 wk x4 plus prednisolone, "complete or nearly complete remission ... long-term survival (>2583 days and 1218 days), but with problematic adverse effects"; described in the abstract as having "high permeability across the blood-brain barrier" | PMID 37756055 (Vet Sci 2023) | OUTCOME (n=2, case report) |
| cytarabine (dog) | CSF:plasma 0.62 +/- 0.14 at steady state, 12-h infusion 50 mg/m2/h, plasma 14.1 uM, CSF 8.3 uM | PMID 1742843 | MEASURED (dog); ALREADY COVERED |
| cytarabine CRI (dogs, BM or CNS involvement) | n=26: "Gastrointestinal toxicity occurred in 17 dogs (65.3%), with 5 (19.2%) experiencing grade III or IV"; thrombocytopenia 11.5%; no outcome numbers in abstract | PMID 31769013 | MEASURED (toxicity) |
| canine blood-tumour barrier | P-gp and BCRP absent before chemotherapy and induced in capillary endothelium after, in 3 recurrent canine lymphomas | PMID 33518631 | MEASURED (n=3) |

Canine availability: thiotepa and busulfan IV are human generics (off-label in dogs); canine IV busulfan and canine TBI-supported autologous/allogeneic HCT are established (PMIDs 10534062, 22882500, 31146304, 35789057). Lomustine is in the repo catalogue as LICENSED. Nimustine: Japan-only usage in the case report (availability otherwise RECALLED-UNVERIFIED, not stated). A dog thiotepa-BCNU or busulfan-based conditioning would be "buildable" (known drugs, new schedule), needing a canine thiotepa PK/MTD study first.

======================================================================
## 9. Model inputs that are defensible

### 9a. Outcome-derived e-folds (Poisson cure model). Grade: DERIVED from OUTCOME, burden ASSUMED
Assumptions (must be stated with the numbers): residual cells at start of therapy N0 (ASSUMED; sensitivity below), each surviving cell regrows independently, so P(no relapse) = exp(-S) where S = expected surviving relapse-capable cells. Then e-folds killed = ln(N0/S). Ignores heterogeneity and late relapses (so S is a lower bound on the true quiescent residual).

Incremental e-folds of one consolidation over the alternative, from the abstracts' PFS/EFS (computed ln[(-ln S_alt)/(-ln S_new)]):
- IELSG43: ASCT 3-y PFS 78% vs R-DeVIC 51%: **1.00 e-fold**
- PRECIS: ASCT 8-y EFS 67% vs 40 Gy WBRT 39%: **0.85 e-fold**
- R-MPV-A: +LD-WBRT 2-y PFS 78.7% vs 54%: **0.94 e-fold**
Reading: three independent trials, three different consolidation modalities, same ~1 e-fold. The residual after HD-MTX-based induction behaves like a pool that one strong consolidation reduces by ~2.5-fold (~1 e-fold) in the surviving-clone count. Dependence on N0 cancels in these (they are differences).

Program-level effective brain kill (MATRix 4 cycles x 21 d + ~30 d to ASCT = ~115 d; 3-y PFS 78% or 8-y EFS 67%):
| N0 (ASSUMED) | e-folds needed (S=0.25 for 78%) | per day over 115 d | per day over 84 d (induction only) |
|---|---|---|---|
| 1e6 | 15.2 | 0.13 | 0.18 |
| 1e8 | 19.8 | 0.17 | 0.24 |
| 1e9 | 22.1 | 0.19 | 0.26 |
| 1e10 | 24.4 | 0.21 | 0.29 |
(S=0.40 for 67%: 14.7 / 19.3 / 21.6 / 23.9 e-folds; 0.13-0.21/day over 115 d.)
Meaning: the human program that achieves ~70-80% 3-8 y PFS delivers an average effective brain-compartment kill of order 0.13-0.21/day, i.e., right at the 0.10-0.19/day bar the model uses. Access is already inside this number (outcome measured in brain). Weaknesses: (i) N0 is assumed and only log-sensitive; (ii) it is the whole multi-agent program (HD-MTX + ara-C + thiotepa + rituximab, then BCNU + thiotepa), not a per-agent potency; (iii) the mean-field average hides that most kill is of the proliferating bulk by induction; (iv) late relapse (below) says S is not zero beyond 3 y.

### 9b. Late-relapse (dormant persister) hazard. Grade: DERIVED arithmetic from OUTCOME
Bonn (PMID 32989105): 10-y OS 29% of 65 = ~19 alive at 10 y; 4 relapses at 9.8, 10.3, 13.3, 21.0 y. Roughly 4/19 = ~21% of 10-y survivors relapsed in the following decade, ~2%/y (rough; at-risk number is not stated in the abstract). MATILDE (24634458): 2 relapses at 100-101 mo. MSK (21372070): >=5 y relapse = 4% of recurrences. After 24 mo, hazard of progression+death <5%/y (40275355). Implication for the model: in non-ASCT, non-WBRT, HD-MTX/ara-C-based patients roughly one in five 10-year survivors still carries a viable dormant clone; it re-responds to the same drug on relapse (13 y case, 21868233; 9/10 CR to salvage in 21372070), pointing to dormancy/persistence rather than selected resistance. Whether thiotepa-HDC removes these cells cannot be answered: ASCT cohorts have <=8 y of follow-up (2/60 late relapses at 3.6 and 7 y, 42139822).

### 9c. Per-agent kill-rate sketch for thiotepa (+BCNU) as the "closing brain agent" for the dog
Transfer logic (written for grading TRANSFERRED, not MEASURED): 
1. Exposure: human thiotepa 5 mg/kg q12h x2 (days -5,-4) + carmustine 400 mg/m2 (day -6) gives a 3-day course; thiotepa t1/2 1.4-3.7 h, TEPA 5-18 h, so active exposure window ~3-4 days.
2. Access: CSF:plasma 0.95-1.01 (n=1) and transcapillary half-time ~1 min (rhesus) -> brain access fraction ~1.0 for the drug (TRANSFER from human/primate; no canine value). This beats the "0.5" the bar assumes.
3. Potency: no IC50 or canine kill measured. The consolidation course's contribution is bounded by outcome: ~1 e-fold over the best non-myeloablative alternative (9a) delivered in ~3-4 days. As a course-integrated number: ~1.0 e-fold / ~3.5 d = ~0.3/day equivalent for the INCREMENT, but this increment is only the part not already killed by induction, so it is a lower bound on thiotepa+BCNU alone (the course also killed whatever induction would have killed). Upper bound from program-level total: 15-24 e-folds in ~3-4 days if ALL kill were attributed to conditioning (clearly wrong). The honest statement: the conditioning kills at least ~1 e-fold of the induction-resistant residual in a few days; the actual figure is unmeasured.
4. Dog transfer: relies on dog = human CSF penetration of a small lipophilic alkylator, plus dog busulfan CNS penetration as a proxy (busulfan 40 mg/kg IV causes "severe central nervous system toxicity" in dogs, which shows brain exposure in dogs, though neurotoxic).
5. Weaknesses: (a) transporter status unknown; (b) n=1 CSF AUC ratio, pediatric; (c) division-independence is class pharmacology; (d) TRM 3-8% with marrow rescue needed (autologous graft available in dogs, 22882500), plus TBI 10 Gy not needed if chemo-conditioned (10534062 shows busulfan 20 mg/kg is myeloablative in dogs); (e) alkylator cross-resistance in sequence (9516940) and MGMT for nitrosoureas (repo already has MGMT escape); (f) late dormant clones may not be cleared (9b).
Suggested evidence grade for the model: access OUTCOME/TRANSFER; kill OUTCOME (program-level, ~1 e-fold increment); never MEASURED. Do not enter as a potency with an IC50.

### 9d. Escape coverage table (humans; thiotepa-HDC unless noted)
| escape | covered? | evidence |
|---|---|---|
| dormant progenitor / quiescent residual | PARTLY | ASCT relapse HR 0.13 vs WBRT (PRECIS); late relapses still occur in non-ASCT cohorts; ASCT >8 y unknown |
| dCK loss (ara-C) | YES (thiotepa/BCNU/busulfan do not need dCK) | mechanism, not PMID-verified here |
| P-gp/BCRP pump | UNKNOWN for thiotepa; busulfan and BCNU not assessed | NOT FOUND |
| antigen loss CD20/CD19 | YES (not antigen-dependent) | alkylator; CD20-negative PCNSL case exists (36644138) |
| MHC loss | YES (not immune-dependent) ; fails for CAR-T? (CAR is MHC-independent) | HLA aberrant in 77% of PCNSL (28507804, n=39); 6p21.3 loss + low HLA-DR linked to progression (39536287) |
| MTX transport loss (RFC methylation) | not relevant to thiotepa | 30% of PCNSL, lower CR rate (15327516) |
| TP53/BTG1/ETV6/6p aberration | still relapse | associated with 91% of progression events in 39536287 (n=78); thiotepa-HDC effect by genotype NOT FOUND |
| DNA repair (BER/NER/HR, MGMT for nitrosoureas) | possible escape | 11431349 (BER protects from thioTEPA, marrow cells); MGMT not tested for thiotepa |
| sanctuary access (CNS) | YES (access ~1) | 2491958, 810575 |

======================================================================
## 10. Which CNS cells survive, and what kills them (what was and was not found)
Found (all indirect):
- Persistence: same IG clone 13.8 y later (n=1 of 3 testable; 21372070); clonal evolution at relapse with shared + private mutations (15249632, single case) implies a persisting ancestor, not a re-seeding.
- Dormancy rather than resistance: relapses at 9.8-21 y re-respond to HD-MTX (32989105, 21868233, 21372070).
- Host/site: relapse mostly in the brain (8 of 10 late relapses brain, 1 ocular, 1 systemic; 21372070); the canine spermatic cord lymphoma relapsed to the brain 5 months after orchiectomy (37265807), and CNS relapses occur during chemotherapy in dogs (22210944).
- Microenvironment: astrocytic CCL19-CCR7 retention of lymphoma cells in gliotic brain (mouse, 31526758); repeated passage in the mouse brain selects more aggressive cells (23481709).
- Genomic: 6p CN-LOH / 6p21.3 homozygous deletion (HLA), BTG1, ETV6, TP53 aberrations associated with 91% of progression events and all 15 deaths (39536287, n=78); RFC promoter methylation in 30% (15327516); CARD11 coiled-coil resistance to ibrutinib (28619981).
- What kills them: only outcome-level evidence (thiotepa/BCNU HDC > WBRT or non-myeloablative chemo; LD-WBRT adds ~1 e-fold; CAR-T gives responses of months for most patients, plateau ~43% 1-y PFS).
NOT FOUND: any study of quiescent/stem-like PCNSL cells; any MRD/ctDNA study of thiotepa-HDC (PubMed query "PCNSL minimal residual disease cerebrospinal fluid ctDNA" returned 0; the ibrutinib paper 38995739 reports CSF ctDNA clearance associated with long-term response); any measured thiotepa kill on non-dividing lymphoma cells.

======================================================================
## 11. Canine CNS lymphoma: what exists
- Treatment outcome series: NOT FOUND (no PubMed series of dogs with CNS lymphoma treated with lomustine, cytarabine CRI or radiation with survival numbers). Closest: 31769013 cytarabine CRI toxicity in 26 dogs with BM or CNS involvement (no outcome); 37756055 nimustine (n=2); 37732143 IT (n=1, 3 weeks); 22210944 CNS relapse (n=3, no numbers); 41495378 (n=1, died despite lomustine); 36899719 neuropathology of 45 canine and 47 feline nervous-system lymphoma (no treatment data); 23115372 (primary CNS B-cell lymphoma, young Maltese; "about 4% of all intracranial primary neoplasms"); 40216556 extranodal adnexal lymphoma with suspected intracranial involvement treated with modified CHOP-15 (euthanised ~3 months).
- Durable canine survivors: 37756055 only (>2583 d, 1218 d), both on nimustine + prednisolone (alkylator + glucocorticoid; two non-division-gated agent classes), "problematic adverse effects".
- Canine non-CNS durability benchmark: alloHCT 89% cure of nine first-remission dogs (35789057, already in repo); autologous HCT 33-40% cure (35789057 intro; 22882500: 5/15 (33%) in remission at median OS 524 d); T-cell autologous HCT 2/13 alive at 741 and 772 d (24467413).

======================================================================
## 12. Evidence-grade summary for model entry
| item | proposed grade |
|---|---|
| HDC-ASCT (thiotepa/BCNU) 3-8 y PFS 67-78% in human brain lymphoma | OUTCOME (human) |
| ~1 e-fold increment per consolidation (3 trials) | DERIVED from OUTCOME |
| program average effective brain kill 0.13-0.21/day | DERIVED (needs N0 ASSUMED) |
| thiotepa brain access ~1.0 | MEASURED human n=1 + MEASURED rhesus, TRANSFER to dog |
| thiotepa P-gp/BCRP status | NOT FOUND (do not enter as "not a substrate") |
| thiotepa/BCNU division-independence | TRANSFER (class mechanism), not PMID-verified here |
| thiotepa kill per day (IC50) | ASSUMED/none; use program-level OUTCOME only |
| canine thiotepa PK | NOT FOUND |
| canine IV busulfan PK and myeloablative dose | MEASURED (dog) |
| canine durable CNS survivors | OUTCOME n=2 (nimustine + prednisolone) |
| BTKi / IMiD CNS efficacy | OUTCOME (months), not closing |
| CAR-T CNS | OUTCOME (1-y PFS ~43%, plateau reported, FU ~2 y); canine persistence 14-50 d already measured |
| allo-HCT | OUTCOME (human NRM 30%, relapse 25%; dogs 8/9 >4 y, not CNS-specific) |

======================================================================
## 13. What I searched and did NOT find
- 10-year follow-up cohorts of thiotepa-based HDC-ASCT in PCNSL: NOT FOUND (max 8 y, PRECIS; 7.3 y IELSG32).
- Thiotepa P-gp/BCRP substrate status (PubMed zero hits; FDA review "Not provided"); ibrutinib, tirabrutinib, lenalidomide, pomalidomide P-gp status: NOT FOUND (PubMed query returned 0).
- Ibrutinib CSF/brain concentration numbers: NOT FOUND in retrieved abstracts.
- BEAM data in PCNSL: NOT FOUND (only the PMID 12692608 authors' statement).
- Canine thiotepa PK/toxicity/conditioning; canine carmustine PK; canine CNS-lymphoma series with outcome numbers for lomustine/cytarabine/radiation: NOT FOUND.
- MRD / persister characterisation of PCNSL after HDC: NOT FOUND.
- PubMed search note: this PubMed tool ANDs every token; long natural-language queries returned 0 hits (e.g., "primary CNS lymphoma long-term survivors 10 years ..."), so many queries were repeated in short form. Searches were not exhaustive (relevance order, 10-25 hits each); papers beyond the first page for large result sets (e.g., "PCNSL ibrutinib" 73 hits, "lenalidomide CNS lymphoma" 54 hits, "CNS lymphoma CAR T-cell" 167 hits) were not all read.
- Items fetched but irrelevant and not used: 3117396, 4954314 etc. (1960s-80s thiotepa bladder studies), 41695824, 40312952, 39427470 (dolphin), 37921752, 40526210.
