# Bispecifics / T-cell engagers / armed T cells / eBAT for canine multicentric lymphoma: research report

Date: 2026-10-02. Case under analysis: canine multicentric (nodal) lymphoma, assuming early detection; target: 10+ year durability.
Verification method: every PMID/DOI below was fetched from the PubMed record (NCBI E-utilities efetch, the same database the PubMed MCP wraps; used because the MCP metadata call returns ~10k tokens per article, mostly author lists). DOIs were taken from each record's own ArticleIdList (not from reference lists). Full-text quotes are from PMC via efetch. Anything I could not retrieve is marked NOT FOUND / NOT READ. Sequence identities were computed here from UniProt FASTA (BLOSUM62 global alignment) and are labelled DERIVED, not measured.

## 0. Success criteria quoted verbatim (graded against exactly these)
- "make sure every mechanism and every escape is closed by either real data or rigorous model, potency, toxicity etc all need to be considered"
- "looking for 10+ years of durability"; "assuming early detection"
- "I'm okay with no specific data but if scientifically sound" (a transfer from another species or disease is acceptable if justified in writing and graded TRANSFER; no-basis numbers stay ASSUMED)
- Latest: "I needed scientifically sound, not totally theoretical. And I think you are dismissing vaccines, ebats, inhibitors, stem cells too easily."

## 1. Headline findings (read this first)

1. **"ebats" in this project almost certainly means eBAT, the EGF/uPA bispecific ANGIOTOXIN, not a T-cell engager.** In the record (README and `docs/HSA_DURABLE_RESPONSE.md` on branches `claude/codex-branch-audit-clfeiz` and `claude/duplicate-codex-prefix-branch-lt1qh6`) eBAT is the University of Minnesota (Modiano/Vallera) deimmunised Pseudomonas exotoxin fused to EGF and the urokinase amino-terminal fragment (PMID 28193671), given to dogs with splenic hemangiosarcoma. The user's list "vaccines, ebats, inhibitors, stem cells" matches the HSA branch's ingredient list. The task brief's two readings (CD3 engagers; antibody-armed T cells "BATs") are covered below as well, but eBAT is the reading with real canine clinical data. Not previously assessed for lymphoma on the lymphoma branch (`docs/universe/SWEEP_modalities.md` section 3.2 and `LYMPHOMA_UNIVERSE.md` line 31 only list CD3-bispecifics as "NOT ASSESSABLE"/"human data not verified").
2. **eBAT as built does not fit lymphoma**: the same paper that reports the dog trial shows EGFR and PLAUR (uPAR) mRNA were "significantly lower (p<2X10-5) in canine lymphoma samples as compared to canine sarcomas" (29 canine lymphomas, RNAseq; PMID 28193671, PMC5418099), and a human T-cell lymphoma line (HPB-MLT) that lacks EGFR/uPAR was not killed. Its class (a protein-synthesis-inhibiting toxin retargeted to a B-cell antigen) has human lymphoid data (DT2219 CD19xCD22, moxetumomab CD22), see section 4.
3. **The earlier claim "no canine data" is true for CD3 engagers and armed T cells, but it is not a scientific reason to exclude them.** Under the project bar, human clinical data are a justified TRANSFER. The human data are strong: CD3xCD20 engagers give CR 40% to 60% single-agent in relapsed disease and 85% to 98% CR with R-CHOP-type first-line combinations, with MRD negativity and CNS activity (section 2, 3).
4. **The decisive, previously unreported blocker is species cross-reactivity**: human CD3 arms and human CD20 arms are predicted not to work on dog cells (CD3 epsilon ectodomain only 43% identical human to dog; rituximab does not bind endogenous canine CD20; PMID 40577406). A human engager is therefore NOT usable off-label in a dog; a canine-specific engager must be built. Building blocks exist (canine CD20 antibodies given safely to dogs; anti-canine CD3 antibodies used for T-cell expansion; canine IgG subclass Fc characterisation).
5. **Durability is the weak point of engagers in relapsed LBCL**: epcoritamab R/R LBCL median duration of CR 36.1 months at 3 years (PMID 41634395); no 5-year plateau data for any CD3xCD20 engager were found. Fixed-duration first-line combinations show 2-year PFS 80% to 86% only. A 10-year inference is NOT supported by engager data. CAR-T has a demonstrated plateau (ZUMA-1: responses ongoing in 31% at 63 months; PMID 36821768).
6. **Escapes that remain open for a CD20-directed engager**: CD20 loss (59% of relapses after glofitamab in one series; PMID 38720530), T-cell dysfunction/TP53, no cover for T-cell lymphoma (target and fratricide). Not escapes: MHC-I loss, division gating, pump efflux (mechanistic and clinical corroboration, section 5).
7. **CNS**: human CNS lymphoma responses are real (CR 59% in 32 R/R PCNSL on glofitamab monotherapy, retrospective, PMID 42579821) despite antibody CSF:plasma ratio of only up to 0.44% (PMID 42035265). Duration in CNS is short (6-month CNS PFS 53%, PMID 42173834). CNS neurotoxicity is the cost (ICANS 25% in a CNS-involved cohort).

---------------------------------------------------------------------
## 2. HUMAN CLINICAL EFFICACY AND DURABILITY OF CD3 BISPECIFICS (B-cell lymphoma)
All numbers quoted from the abstract of the PMID shown.

| Agent / setting | PMID (DOI) | Numbers (from abstract) |
|---|---|---|
| Epcoritamab R/R LBCL, 2-yr (EPCORE NHL-1, N=157) | 39322711 (10.1038/s41375-024-02410-8) | ORR 63.1%, CR 40.1%; "Estimated 24-month PFS and OS rates were 27.8% and 44.6%... An estimated 64.2% of complete responders remained in CR at 24 months. Estimated 24-month PFS and OS rates among complete responders were 65.1% and 78.2%... Of 119 MRD-evaluable patients, 45.4% had MRD negativity"; CRS 51.0%; CR 36% in prior CAR-T, 32% primary refractory |
| Epcoritamab R/R LBCL, 3-yr update | 41634395 (10.1007/s00277-026-06798-4) | median follow-up 37.1 mo; ORR 59%, CR 41%; "Median duration of CR was 36.1 months (20.2-NR); the longest ongoing CR was > 43 months. Median PFS 37.3 months (26.0-NR) in patients with CR"; MRD-negative 54/119 (45%); CRS 51%; grade 3 infections 24% |
| Glofitamab R/R DLBCL (>=2 lines), pivotal | 36507690 (10.1056/NEJMoa2206913) | n=155; CR 39% (95% CI 32-48) at 12.6 mo; "The majority (78%) of complete responses were ongoing at 12 months"; median time to CR 42 days (95% CI 42-44); 12-mo PFS 37%; CRS 63% (grade>=3 4%); grade>=3 neurologic events 3%; 35% CR in 52 prior CAR-T |
| Glofitamab phase I | 33739857 (10.1200/JCO.20.03175) | 171 treated; CRS 50.3% (G3-4 3.5%); ICANS-like grade 3 in 2 (1.2%); "Of 63 patients with CR, 53 (84.1%) have ongoing CR with a maximum of 27.4 months observation" |
| Glofit-GemOx vs R-GemOx, R/R DLBCL, 3-yr (STARGLO, phase 3) | 42269085 (10.1182/bloodadvances.2026019764) | median OS 25.5 vs 12.5 mo (HR 0.60); median PFS 14.4 vs 3.3 mo (HR 0.41); CR 58.5% vs 25.3%; 2L 3-yr OS 54.6% |
| Epcoritamab + R-CHOP, 1L LBCL IPI 3-5 (n=47) | 42622258 (10.1182/blood.2026033839) | ORR 98%, CR 85%; median follow-up 44.2 mo, median DOCR/PFS/OS not reached; 2-yr PFS 80% (65-89), OS 87%; "MRD-negativity was achieved in 100% of MRD-evaluable patients"; CRS 60% (mostly G1-2) |
| Glofitamab + R-CHOP or Pola-R-CHP, 1L high-risk LBCL <=65y (COALITION, n=80) | 40532125 (10.1200/JCO-25-00481) | ORR 100%, CR 98%; median follow-up 20.7 mo; 2-yr PFS 86%, OS 92%; CRS 21% all <=G2; median TMTV 842 cm3 |
| Mosunetuzumab R/R FL (>=2 lines), 3-yr (n=90) | 39447094 (10.1182/blood.2024025454) | median follow-up 37.4 mo; CR 60.0%, ORR 77.8%; 49 of 54 CR patients still in CR at end of treatment; "Kaplan-Meier-estimated 30-month remission rate was 72.4%"; median CD19+ B-cell recovery 18.4 mo after 8 cycles; fixed duration |
| Epcoritamab vs axi-cel, matching-adjusted | 40903324 (10.1016/j.clml.2025.07.015) | ORR 73.5% vs 74.3%, CR 48.7% vs 54.5%; PFS HR 1.009 (0.572-1.778); OS HR 0.826 (0.444-1.536); no significant difference (indirect, MAIC) |
| CAR-T benchmark, ZUMA-1 5-yr | 36821768 (10.1182/blood.2022018893) | ORR 83%, CR 58%; "responses were ongoing in 31% of patients" at median follow-up 63.1 mo; 5-yr OS 42.6% |
| Odronextamab ELM-2 ctDNA | 40902079 (10.1182/bloodadvances.2025016332) | undetectable ctDNA at C4D15 associated with longer PFS (FL HR 0.31, 0.14-0.67; DLBCL HR 0.42, 0.24-0.75); among progressors most had detectable ctDNA (FL 15/19; DLBCL 28/35) |
| Epcoritamab FL MRD | 42431612 (10.1182/bloodadvances.2025017565) | "most MRD-evaluable patients reaching MRD negativity by cycle 3 day 1" (clonoSEQ, PBMC and/or ctDNA); MRD negativity at C3D1 associated with PFS median not reached |
| Real-world safety (255 pts, 14 centres) | 42782211 (10.1182/bloodadvances.2026020595) | CRS 31% (G3+ 5%), ICANS 8% (G3+ 2%); concurrent chemotherapy linked to grade 2+ CRS |

Assessment of durability beyond 2 years (strength shown): R/R LBCL monotherapy has continuing relapses after year 2 (epcoritamab median DOCR 36.1 mo; "longest ongoing CR > 43 months"). First-line combination data are short (median follow-up 20.7 to 44.2 mo). Indolent FL: 72.4% remission at 30 months. NOT FOUND: any 5-year or 10-year progression-free plateau for a CD3xCD20 engager (searched epcoritamab, glofitamab, mosunetuzumab, odronextamab "3-year/5-year/long-term"; the glofitamab 3-year monotherapy update is not in PubMed as retrievable). Therefore "2+ years disease-free implies 10+" is supported for CAR-T (31% ongoing at 63 mo) but NOT demonstrated for engagers.

### 2.1 T-cell lymphoma and T-ALL engagers
- UMG1/CD3epsilon bispecific engager (CD43 epitope): "High UMG1 expression in 62.3% of TCL samples... all T-PLL primary specimens (27/27)"; in vitro redirected cytotoxicity only (PMID 41834433, 10.1002/hon.70187). Preclinical.
- CD38xCD3 XmAb18968 phase 1 in R/R AML (n=13) and T-ALL (n=9): "In 6 patients with RR-T-ALL, 4 achieved meaningful improvement in disease burden with 1 clearance of MRD"; median OS 8.7 months in T-ALL; no G>=3 CRS or neurotoxicity (PMID 42736326, 10.1038/s41375-026-03130-x).
- Systematic review (PMID 42643454): "BsAbs in acute myeloid leukemia (AML) and Hodgkin/T-cell lymphoma (HL/TCL) remained early-phase with limited efficacy and no approvals to date."
- CD7/CD5 bispecific CAR (not engager) preclinical: 35332132. A CD20xCD5 tetravalent bispecific antibody preclinical: 34538717.
- Conclusion: no CD3 engager has human clinical efficacy in T-cell lymphoma. A CD3-arm engager for a T-cell tumour also engages the tumour's own T cells (fratricide/self-activation risk; not directly searched for data). **T-cell multicentric lymphoma is NOT covered by this class.**

---------------------------------------------------------------------
## 3. CNS ACTIVITY (CD3 engagers) AND NEUROTOXICITY

| Finding | PMID | Numbers |
|---|---|---|
| Glofitamab penetrates blood-brain barrier, stimulates immune-cell infiltration of CNS tumours, responses in secondary CNS lymphoma | 38484137 (10.1182/blood.2024024168) | abstract only retrievable (full text blocked by publisher): "glofitamab penetrates the blood-brain barrier, stimulates immune-cell infiltration of CNS tumors, and induces clinical responses in patients with secondary CNS [lymphoma]" |
| R/R PCNSL, glofitamab monotherapy (n=16), paired plasma and CSF | 42035265 (10.1002/ajh.70342) | ORR 75% (CR 50%); median PFS 15.4 mo; "Glofitamab was detectable in the CSF of 60% of patients, with CSF/plasma ratios up to 0.44%"; early CSF ctDNA clearance associated with response; grade>=3 neurotoxicity 2 (11%); 2 fatal ICANS after CAR-T consolidation |
| R/R CNS lymphoma, glofitamab-based, 84 pts | 42579821 (10.1158/2643-3230.BCD-26-0128) | PCNSL monotherapy (n=32) ORR 88%, CRR 59%; combination (n=21) ORR 100%, CRR 81%; SCNSL monotherapy (n=8) ORR 88% (CRR 75%); median PFS 19.5 mo PCNSL, 13.5 mo SCNSL at 14.7 mo follow-up; CRS 40% (all G1-2), ICANS 8% |
| CD3xCD20 engagers with CNS involvement, CUBIC, 28 pts (22 glofitamab) | 42173834 (10.1038/s41408-026-01519-6; full text read) | active CNS (n=18): systemic+CNS ORR 56%, CR 33%; **CNS ORR 65% (11), CNS CR 35% (6)**; parenchymal CNS CR 5/12 (42%); 6 CNS-CR patients had no relapse at median 12 mo (range 4-21). Whole cohort median follow-up 6 mo: 6-mo PFS 43%, 6-mo CNS PFS 53%, OS 77%. Whole cohort: CRS 43%, **ICANS 25% (7/28; grade 1 4, grades 2, 3, 4 one each)**; none of the 4 active-CNS patients with ICANS achieved CR |
| Blinatumomab in CNS ALL | 42437816 (10.1007/s11899-026-00782-5), 42549975 (10.1002/1545-5017.70600) | review: "CNS relapse is increasingly recognized in this context [blinatumomab/inotuzumab]... likely reflects... limited CNS penetration, improved disease control that unmasks previously subclinical CNS involvement, and the high-risk biology"; CD19 CAR-T "meaningful activity in CNS disease". Paediatric series (90 pts, 167 relapses): CNS relapses were 36/64 (56.3%) of extramedullary relapses; blinatumomab associated with isolated other-extramedullary relapse (HR 13.3). |
| CSF T cells with blinatumomab | 39155594 (10.1080/10428194.2024.2392823), 37807185 (10.1097/MPH.0000000000002765) | CSF pleocytosis in 51% (88 adults), median CD4:CD8 1.34; 66% pleocytosis after blinatumomab (71 CAR-T/blina patients). Pleocytosis was not linked to CNS relapse or neurotoxicity. |
| IT chemotherapy timing and neurotoxicity | 41550943 (10.3389/fimmu.2025.1690916) | 93 paediatric patients; neurotoxic events 8.8% overall; IT chemo on blinatumomab day 1 OR 15.6 (2.96-87.8) |
| Neurotoxicity pharmacovigilance | 42256396 (10.3389/fphar.2026.1819689) | FAERS: glofitamab longest median onset 82 days; blinatumomab most reported |

Intrathecal engager administration: NOT FOUND (searched "blinatumomab intrathecal"; results were intrathecal chemotherapy alongside blinatumomab only). Blinatumomab CSF concentration/CSF:serum ratio: NOT FOUND (searched). T-cell CAR trafficking into CSF (19% of CSF CD3+ at day 30; PMID 37345469) is already in the record (`docs/universe/SWEEP_cart_human.md`).

---------------------------------------------------------------------
## 4. eBAT (EGF bispecific angiotoxin) AND THE IMMUNOTOXIN CLASS

### 4.1 eBAT, canine data (all fetched)
| Item | PMID (DOI) | Numbers |
|---|---|---|
| Phase I-II, 23 dogs, stage I-II splenic HSA, one cycle then doxorubicin | 28193671 (10.1158/1535-7163.MCT-16-0637) | "eBAT improved 6-month survival from <40% in a comparison population to approximately 70% in dogs treated at a biologically active dose (50 ug/kg). Six dogs were long-term survivors, living >450 days"; 6/23 (26%) alive at 1 yr; 2 alive at 1245 and 963 days; no AEs at 25 ug/kg; reversible liver toxicity in 2 dogs (dose level 2); reversible hypotension in 2 dogs at level 2 and 2 at level 3; no EGFR-class skin/GI/ocular toxicity; maximum tolerated dose in mice: EGF-toxin alone 20 ug/kg vs 160 ug/kg eBAT with no deaths |
| Immunogenicity/PK | same | neutralising antibodies "sporadic"; drug detectable day 1 in 4/9 dogs with no antibody, 7/8 with antibody after eBAT, 1/4 with pre-existing antibody; detectable drug on day 1 associated with survival (404 vs 172 d, HR 0.20 (0.07-0.63), p=0.002); "Pharmacokinetic studies show that eBAT is metabolized quickly within a few hours" |
| Potency in vitro | same | release criterion IC50 <1.0 nM; RD rhabdomyosarcoma IC50 0.02 nM; other lines 0.06 pM to 0.08 nM; "inhibits both protein synthesis and DNA synthesis" |
| Redosing intensified, 25 dogs, 3 cycles | 32187827 (10.1111/vco.12590) | acute hypotension in 6 of 25 (2 hospitalised); ALT elevation in 1; no significant survival benefit; "greater toxicity and reduced efficacy compared with a single cycle" |
| Toxicity profile mice and dogs | 39330834 (10.3390/toxins16090376) | "toxicities were mild and self-limiting"; higher mouse doses: dose-dependent liver injury; "in dogs... given dosages found to be biologically active, eBAT was well tolerated" |
| HSA and stem-like cells | 23553371 (10.1002/ijc.28187) | cytotoxic in 4 HSA lines at <=100 nM; stem-like hemangiospheres IC50 about two orders higher but still nanomolar; a "threshold level of EGFR expression" required for monospecific EGF-toxin |
| Stromal re-modelling (meBAT) | 40914989 (10.1016/j.jpet.2025.103674) | in eBAT-resistant MC17 fibrosarcoma, eBAT/meBAT depleted tumour-associated macrophages and promoted T-cell infiltration (mouse); already in the HSA record |
| Targets in lymphoma | 28193671 | EGFR and PLAUR mRNA "significantly lower (p<2X10-5) in canine lymphoma samples as compared to canine sarcomas" (29 lymphoma samples; Figure 2F not extractable); HPB-MLT T-cell lymphoma line "do not express EGFR or uPAR and it showed no significant cytotoxicity" |

Not found: any eBAT use or EGFR/uPAR protein measurement (IHC/flow) in canine lymphoma; any canine CD19/CD20/CD22-targeted angiotoxin. (Searched "canine lymphoma EGFR", "canine lymphoma uPAR": 0 relevant.)

### 4.2 Class transfer: same-lab B-cell-targeted toxins in humans
- DT2219 (CD19xCD22 bispecific ligand-directed diphtheria toxin), phase I, 25 patients with relapsed/refractory B-cell lymphoma/leukaemia: "Durable objective responses occurred in 2 patients; one was complete remission after 2 cycles"; DLT at 40 and 60 ug/kg; biologically active dose 40 to 80 ug/kg/day x4; neutralising antibody only 30% (PMID 25770294, 10.1158/1078-0432.CCR-14-2877). Deimmunised dDT2219 preclinical (PMID 29316610, 10.3390/toxins10010032).
- Moxetumomab pasudotox (CD22-PE38) in hairy cell leukaemia, 80 pts: durable CR (>180 d) 36%; CR 41%; "Twenty-seven complete responders (82%) were MRD-negative"; "CR lasting >=60 months was 61%"; median PFS without loss of haematologic remission 71.7 mo; HUS and capillary leak each <=10% (PMID 33627164, 10.1186/s13045-020-01004-y). This shows a PE toxin can give MRD-negative, multi-year remission in a B-cell neoplasm (a leukaemia with low proliferation).

---------------------------------------------------------------------
## 5. MECHANISM FOR THE MODEL (CD3 engagers)

| Question | Answer | Evidence and strength |
|---|---|---|
| Needs MHC-I? | NO | Review: CD20xCD3 engagers redirect "endogenous T cells against malignant B cells independently of major histocompatibility complex-mediated antigen presentation" (PMID 42121895, 10.3390/cells15090794). Mechanistic, class-level. |
| Division-gated? | NO (T-cell perforin/granzyme kill; no cell-cycle requirement in the mechanism) | **Direct in-vitro "quiescent target" data NOT FOUND** (searched quiescent/dormant/resting/non-dividing with bispecific/blinatumomab). Clinical corroboration: indolent FL (low proliferation) gives CR 60% (mosunetuzumab, PMID 39447094), at least as high as DLBCL; MRD-negative conversions in FL (PMID 42431612). Grade: mechanistic + clinical corroboration (TRANSFER). |
| P-gp / pump substrate? | NO (a ~150 kDa antibody and a T-cell effector; not an efflux substrate) | **Direct "kills MDR lymphoma" paper NOT FOUND** (searched). Clinical corroboration: CR 32% in primary refractory and 36% after prior CAR-T (PMID 39322711); 75% of 3-yr cohort refractory to >=2 lines (PMID 41634395). Grade: mechanistic + outcome corroboration. |
| Antigen coverage | CD20 only (single target); dual CD19xCD20xCD3 trispecific is preclinical only | PMID 34463907 (Front Med 2022, preclinical, B-ALL). Human CD19-negative relapse after CD19/CD22 bispecific therapy is already in the record (PMID 34312556 via `SWEEP_cart_human.md`). |
| CD20 loss escape | REAL | "high rates of CD20 loss (59%) at the time of relapse" and median OS 4.1 months from progression after glofitamab (PMID 38720530); resistance review lists "CD20 loss driven by MS4A1 mutations, alternative splicing, and gene deletion" plus TP53, MYC, NOTCH1 (PMID 42121895); 11.9% CD20 loss at relapse after rituximab-era treatment, 243 patients (PMID 39697682). MS4A1 mutation frequency after engagers: exact figure NOT FOUND. |
| Antigen-low threshold | Single case only | One patient with routine-assay CD20-negative relapse, node 40 to 20 mm on epcoritamab (PMID 42816411). A CD20-density threshold for glofitamab/epcoritamab: NOT FOUND. |
| T-cell fitness / TP53 | Open escape | TP53 mutation, >1 extranodal site and low baseline lymphocytes poor prognostic (n=30; PMID 42141155); endogenous immune environment affects engager outcome more than CAR-T outcome (PMID 39869833); exhaustion markers PD-1, LAG-3, TIM-3, TIGIT (review PMID 42121895). In dogs, T-cell status after CHOP is an unmeasured dependency for engagers (autologous canine T-cell expansion after CHOP works: PMID 22355761). |

---------------------------------------------------------------------
## 6. KILL RATE, PK AND PD (derivation for the model)

Verified PK/PD facts:
- Epcoritamab dosing: 0.16 mg and 0.8 mg step-up, 48 mg full dose, weekly in cycles 1-3, every 2 weeks cycles 4-9, every 4 weeks cycle 10 onward; "higher exposure was associated with a higher ORR, CR rate, PFS and OS. A potential plateau of efficacy was observed at 48 mg or above"; "Most initial responses (94%) were observed during the weekly dosing period" (PMID 39935086, 10.1002/cpt.3588).
- Odronextamab PK (n=507): "bi-exponential decline with parallel linear and non-linear (Michaelis-Menten) elimination"; linear CL 0.189 L/day, Vss 9.41 L; target-mediated CL about 5 L/day at baseline falling to about 0.03 L/day, "consistent with the treatment-induced depletion of the B cells" (PMID 41351218, 10.1002/psp4.70162). Derived: terminal half-life roughly ln2 x 9.41 / 0.189 = about 35 days (DERIVED, crude, ignores the bi-exponential shape).
- Epcoritamab joint PK/tumour-burden/Deauville model (n=165): simulated 2-year CR rates 46.4% (continuous), 37.2% (fixed-duration), 27.0% (stop-at-CR); "elevated circulating tumor DNA levels" identify patients needing continuous treatment (PMID 42138365, 10.1002/cpt.70336). Model rate constants not retrievable (full text empty).
- Blinatumomab (first-in-human NHL): "Doses as low as 0.005 mg per square meter per day... led to an elimination of target cells in blood. Partial and complete tumor regressions were first observed at... 0.015 milligrams, and all seven patients treated at... 0.06 milligrams experienced a tumor regression" (PMID 18703743, 10.1126/science.1158545). Class property: picomolar-range potency; serum levels not extracted.
- Time to response: glofitamab median time to CR 42 days (95% CI 42-44, PMID 36507690; note this equals the first scheduled assessment, so it is a ceiling on speed); epcoritamab 94% of responders respond within the 12-week weekly period (PMID 39935086); FL MRD negative by C3D1 (PMID 42431612).

**Derived net tumour kill rate in responders (human, TRANSFER):**
Assumptions (stated): burden at start about 842 cm3 (COALITION median total metabolic tumour volume, PMID 40532125) at the textbook conversion 1 cm3 = 1e9 cells (ASSUMED convention, not verified here) = 8.4e11 cells; PET-CR needs residual below about 1 cm3 (1e9 cells), i.e. about 6.7 e-folds (2.9 log10).
- LOW 0.08/day: 6.7 e-folds over 84 days (end of weekly dosing; the slowest responders).
- CENTRAL 0.16/day: 6.7 e-folds over 42 days (glofitamab median time to CR).
- HIGH 0.30/day: MRD-negativity at about day 43 (epcoritamab FL, PMID 42431612) requiring about 13 e-folds (to about 1e-6 sensitivity of 8.4e11 cells).
Limits of this derivation: net of regrowth; not a per-cell hazard; covers only responders (CR 40% R/R LBCL, 85% to 98% with R-CHOP) so the model should use it with a responder fraction and treat non-response as the CD20-loss/T-cell-failure escapes; T-cell-limited and saturating (plateau at >=48 mg), lag of days to weeks during step-up. Not derivable: a direct per-day kill rate from tumour decline curves or ctDNA half-lives (the primary tumour-dynamics papers' rate constants were not retrievable), so this is DERIVED from clinical timing, graded TRANSFERRED (human to dog), not MEASURED. Grade for eBAT-class: the HSA record already carries 5.2 to 7.8 logs per cycle for sarcoma; it is not transferable to lymphoma because the targets are not expressed.

E:T and T-cell dependence: kill requires functional autologous T cells (low baseline lymphocytes and TP53 poor, PMID 42141155; "immune quadrant" correlates with engager benefit, N=74, PMID 39869833). No E:T ratio figures were extracted.

---------------------------------------------------------------------
## 7. BATs (bispecific-antibody-armed activated T cells)

Human: Lum lab and colleagues, activated T cells armed ex vivo with anti-CD3 x tumour-antigen bispecific antibody.
- CD20 BATs in myeloma, phase Ib, n=12 (CD138-/CD20+ clonogenic precursors), 2 infusions before autologous transplant: "reduced levels of CMPCs by up to 58%", safe; immune responses boosted (PMID 26827660, 10.1016/j.bbmt.2015.12.030). **No lymphoma BAT trial found.**
- EGFR BATs pancreatic cancer n=7: "no dose-limiting toxicities... median TTP 7 months, median OS 31 months"; 2 CRs after chemotherapy restart (PMID 32939319, 10.1080/2162402X.2020.1773201). EGFR BATs glioma, 80x10^9 cells feasible dose, limited T-cell expansion (PMID 38263486, 10.1007/s11060-024-04564-y). GD2 BATs (PMID 38519053, 10.1136/jitc-2023-008744): "Mild and manageable cytokine release syndrome occurred in all patients", OS 21.1 months. HER2 BATs breast, n=32: median OS 13.1 months (PMID 34117114, 10.1136/jitc-2020-002194). HER2 BATs + pembrolizumab prostate n=14: 6-mo PFS 38.5% (PMID 36255393, 10.1158/1078-0432.CCR-22-1601).
- Assessment: BATs are safe and induce endogenous immune responses but have no demonstrated cure-level kill; they are a weaker evidence base than soluble engagers. BAT persistence in vivo: NOT FOUND as a quantified half-life.

Dogs (relevant building blocks, all fetched):
- Autologous canine T-cell expansion is commercial: "Expansion of canine peripheral blood CD3+ T-cells for use as ACT... is currently available from two commercial US laboratories" and, in a 10-dog series, Aurelius Biotherapeutics expanded T cells (20 mL blood shipped overnight); 23 infusions, median 5.62 x10^6 cells/kg (range 2.59-8.55 x10^6), "administered with no complications or adverse events"; "4/10 (40%) of dogs were cured... (disease-free for >=2 years post-autoPBHSCT)" (PMID 34950726, 10.3389/fvets.2021.787373; combined with autologous stem-cell transplant). Earlier trial: autologous T cells on artificial APCs after CHOP "persisted for 49 days, homed to tumor, and significantly improved survival" (PMID 22355761, 10.1038/srep00249; OS 392 vs 167 days as summarised in PMC8688351).
- Canine T cells are activated and expanded with anti-canine CD3 antibody plus IL-2 (PMID 12679562, 18628598, 34246811; anti-canine CD3/CD28 microbeads PMID 33679741, 10.3389/fimmu.2021.604066).
- Therefore a canine BAT = commercially expanded autologous T cells + an arming step with a canine CD3 x CD20 bispecific. The arming step is not published for dogs: NOT FOUND.

---------------------------------------------------------------------
## 8. CANINE bispecific / engager / armed-cell literature: what exists (searched 2026-10-02)

| Class | Result |
|---|---|
| Canine CD3xCD20, CD3xCD19, blinatumomab-like, caninized BiTE | NOT FOUND. PubMed `canine[tiab] AND bispecific[tiab]` returned 9 records, none a T-cell engager; the 2026 review of companion-animal antibodies states the idea only as a proposal: "CD20-targeting bispecifics in canine B-cell lymphoma extend the same use-case logic... adding a T-cell- or NK-cell-engaging arm, such as anti-CD3 or anti-CD16, could increase the depth of response. Format selection should occur only after canine CD20 expression and heterogeneity, effector-cell activity, and pharmacodynamic B-cell-depletion endpoints have been defined" (PMID 42655798, 10.3390/vetsci13080778). |
| Other canine bispecifics | Anti-EGFR/HER2 bispecific (not T-cell) in a mouse xenograft of canine osteosarcoma (PMID 36432687, 10.3390/pharmaceutics14112494); eBAT and EGFuPA-toxin (section 4). |
| Canine NK engagers / TriKE | NOT FOUND. Canine CD16A and CD64 cloned and characterised, CD16A+ T and NK cells (PMID 35281028, 10.3389/fimmu.2022.841859); canine NK cells show ADCC against human cetuximab- and trastuzumab-coated cells (PMID 31610784, 10.1186/s12917-019-2068-5). Human TriKEs are preclinical/early (PMID 33299651, 30890546). |
| Canine CAR-T for lymphoma | exists as pilot/preclinical (PMID 32002286, 10.1080/2162402X.2019.1676615: 5 dogs, CD20 CAR-T, CD20-negative escape, canine anti-mouse antibodies; PMID 39314237; 41376156). Already in the record. |
| Canine anti-CD20 antibodies in dogs | 1E4-cIgGB with doxorubicin in 42 dogs: CD21+ B cells fell to median 0.04 of baseline at day 7, 1 hypersensitivity event (PMID 38662527, 10.1111/jvim.17080). Afucosylated 4E1-7-B_f + CHOP, 13 dogs: CR 13/13, median PFS 340 d, OS 458 d, 2-yr survival 38.9% (PMID 41742528, 10.1093/jvimsj/aalaf039). Antibody generation and characterisation: PMID 32651429 (10.1038/s41598-020-68470-9), 35177658 (10.1038/s41598-022-06549-1: canine CD20 overexpressed in B-cell lymphoma; six amino-acid variants C77Y, L147F, I159M, L198V, A201T, G273E). |
| Canine IgG backbone | "Canine subclasses A and D appear effector-function negative while subclasses B and C bind canine Fc gamma receptors and are positive for ADCC" (PMID 24268690, 10.1016/j.vetimm.2013.10.018): an effector-silent canine Fc exists for an engager format. |
| Licensed canine cancer antibodies | Only gilvetmab (anti-PD-1) is "currently the only veterinary ICI available commercially, has conditional licensure in the United States" (PMID 42710546, 10.2460/javma.26.06.0517). No licensed canine anti-CD20 found (Blontress search: 0 PubMed records). No licensed bispecific. |

---------------------------------------------------------------------
## 9. CROSS-REACTIVITY OF HUMAN REAGENTS WITH CANINE TARGETS (decides whether human engagers can be used in dogs)

| Target | Evidence | Verdict |
|---|---|---|
| CD20 (rituximab) | "since a previous report showed that rituximab did not react with canine CD20"; in this study rituximab "bound to canine CD20 overexpressed in NRK cells" but weakly (KD could not be calculated), "Endogenously expressed canine CD20 in CLBL-1/luc was not detected by rituximab", rituximab did not bind canine CD21+ B cells (PMID 40577406, PMC12204528) | does NOT bind endogenous canine CD20 |
| CD20 (obinutuzumab biosimilar) | bound overexpressed canine CD20 (KD 17.42 +/- 1.76 nM vs 4.2 +/- 2.6 nM for the canine antibody), "weakly detected" on CLBL-1/luc, "only bound weakly" on canine B cells; ADCC and CDC inferior to the canine antibody (PMID 40577406) | weak binder; glofitamab's CD20 arm origin from obinutuzumab: NOT VERIFIED in this pass |
| CD20 sequence | DERIVED: human CD20 large extracellular loop (aa 142-188) 68% identical to the canine MS4A1 entry A0A8I3PDC4 (32/47); full length 73.7% | consistent with weak/absent binding |
| CD3 epsilon (therapeutic arms) | DERIVED from UniProt P07766 (human), P27597 (dog), Q95LI5 (cynomolgus): ectodomain (human aa 23-126) identity dog 43.3% (45/104) vs cynomolgus 71.2%; N-terminal 23-45 dog 43.5% vs cynomolgus 91.3%. Dog N-terminus QDEDFKASDDLTSISPEKRFKVSI vs human QDGNEEMGGITQTPYKVSI (alignment). Glofitamab, teclistamab, talquetamab and tarlatamab use the SP34 family, whose epitopes are at "the N-terminal region of CD3epsilon" (HDX-MS), blinatumomab is OKT3-derived (PMID 40987715, 10.1053/j.seminhematol.2025.08.004) | **predicted not to engage canine CD3**; any therapeutic CD3 arm binding canine T cells: NOT FOUND (searched; polyclonal anti-CD3 cross-reactivity papers exist for IHC only, e.g. 17659784, not for extracellular therapeutic epitopes) |
| CD19 | DERIVED: human CD19 ectodomain 58.3% identical to canine entry A0A8I3MPF4 | likely not cross-reactive |
| Fc | human IgG1 Fc: canine NK ADCC works with cetuximab and trastuzumab (PMID 31610784), "the only human antibodies reported binding to canine cancer cells" | human Fc engages canine effectors, but human proteins in dogs are immunogenic; canine anti-drug antibody data for human engagers: NOT FOUND; canine anti-mouse antibodies caused CAR-T loss (PMID 32002286) |

Conclusion (grade DERIVED + MEASURED for CD20/rituximab): **human CD3xCD20 engagers cannot be used in dogs; a canine-specific engager is required.** Practical routes: canine CD20 binder (4E1-7-B_f/1E4, already in dogs) + anti-canine CD3 binder (exists for T-cell expansion; clone and epitope not identified here) on an effector-silent canine IgG-A or D backbone; or the engager arm via the armed-T-cell (BAT) route.

---------------------------------------------------------------------
## 10. MODEL INPUTS

Case: canine multicentric lymphoma, early detection; engagers evaluated as a class entry "CD3xCD20 T-cell engager" (B-cell only), "armed T cells (BAT)" and "eBAT/immunotoxin".

### 10.1 CD3 x CD20 T-cell engager (canine-specific, to be built)
| Input | Low / central / high | Derivation | Grade |
|---|---|---|---|
| Net tumour kill rate in responders | 0.08 / 0.16 / 0.30 per day | section 6: 2.9 log10 (6.7 e-folds) over 84 / 42 d; 13 e-folds over 43 d (MRD) | DERIVED from human clinical timing; TRANSFERRED human->dog. Not MEASURED. Requires a functional canine engager. |
| Responder fraction (probability the tumour is a responder) | R/R LBCL monotherapy 0.40 (CR 40.1%, 39%); 1L with chemo 0.85 to 0.98; FL 0.60 | PMIDs 39322711, 36507690, 42622258, 40532125, 39447094 | OUTCOME (human) |
| Division gating | none (0 gating factor) | T-cell perforin/granzyme kill; FL CR 60% corroborates | mechanistic + outcome corroboration; direct quiescent-cell kill data NOT FOUND |
| Pump (P-gp/ABCG2) substrate | NO | antibody + T-cell effector; CR 32% primary refractory | mechanistic + outcome corroboration; direct MDR data NOT FOUND |
| MHC-I dependence | NONE | PMID 42121895 | mechanistic class-level; closes the MHC-loss escape |
| Antigen coverage | CD20+ B-cell lymphoma only. Not T-cell lymphoma. Single target, so CD20 loss is an open escape | CD20 loss 59% of post-glofitamab relapses (PMID 38720530); canine CD20 overexpressed in B-cell lymphoma (PMID 35177658); dual CD19xCD20 trispecific preclinical only | OUTCOME (human) for escape rate; antigen escape in dogs after CD20 CAR-T seen (PMID 32002286) |
| CNS access, antibody | CSF:plasma 0.0044 (0.44%) maximum, detectable in 60% | PMID 42035265 | MEASURED (human, glofitamab); TRANSFERRED to dog |
| CNS effective kill multiplier (relative to systemic) | 0.2 / 0.5 / 0.85 | CNS CR 35% vs systemic CR 33% in the CUBIC cohort (PMID 42173834); PCNSL monotherapy CR 59% (PMID 42579821); but 6-mo CNS PFS 53% and CNS relapse after blinatumomab in ALL (PMIDs 42437816, 42549975); effector is the T cell, not antibody concentration | OUTCOME (human), short follow-up; a judgement-based range, not derived from CSF kinetics |
| Durability: fraction of CR remaining at 2 / 3 years | R/R LBCL mono: 0.64 at 24 mo (39322711); about 0.5 at 36 mo (median DOCR 36.1 mo, 41634395). FL mosun: 0.72 at 30 mo. 1L combos: 2-yr PFS 0.80 to 0.86 | cited trials | OUTCOME (human). **10-year plateau NOT demonstrated; do not extrapolate.** |
| Toxicity budget (human TRANSFER) | CRS any 31% to 63%, grade>=3 about 3% to 5%; ICANS any 8% (255 real-world), 3% grade 1 (n=30), grade>=3 neurologic 3% (pivotal glofitamab); in CNS-involved cohort ICANS 25% (grade 3-4 about 7%); grade 3 infection 24%; B-cell aplasia (recovery 18.4 mo after mosunetuzumab) | PMIDs 36507690, 42782211, 42173834, 41634395, 39447094, 42141155 | OUTCOME (human). No canine engager safety data. Canine anti-CD20 mAbs tolerated with B-cell depletion >200 d (PMIDs 38662527, 41742528). |
| PK | step-up then full dose (epcoritamab 0.16/0.8/48 mg, weekly then q2w then q4w); terminal half-life about 35 d (derived from odronextamab CL 0.189 L/d, Vss 9.41 L); efficacy plateau at exposure of 48 mg | PMIDs 39935086, 41351218 | MEASURED (human); half-life DERIVED crude |
| Availability tier for DOGS | **needs development** (no canine engager exists; human engagers human-licensed but not usable in dogs) | sections 8, 9 | -- |

What is needed to use it in a dog: (1) canine CD3 binder with defined epitope (anti-canine CD3 exists for T-cell expansion; engager-grade scFv not published); (2) canine CD20 binder (4E1-7-B_f, 1E4: already clinically used); (3) effector-silent canine IgG-A/D Fc (PMID 24268690) or scFv format; (4) potency screen against CLBL-1/GL-1 with canine PBMC at defined E:T; (5) healthy-beagle step-up safety/CRS study (no canine CRS data exist); (6) CHO manufacturing; (7) neutralising-antibody monitoring (canine proteins reduce but do not remove the risk). Cost and timeline: NOT FOUND.

### 10.2 BAT (canine CD3xCD20-armed autologous T cells)
| Input | Value | Grade |
|---|---|---|
| Kill rate | not derivable; no lymphoma BAT trial; human BAT solid-tumour outcomes are disease stabilisation, OS 13 to 31 months | ASSUMED if used; do not count toward closure |
| Manufacturing in dogs | feasible and commercial for autologous expanded T cells (two US commercial labs; 5.62 x10^6 cells/kg; no AEs in 10 dogs; PMID 34950726) | MEASURED (dog) for expansion; arming step NOT FOUND |
| Persistence | autologous canine T cells 49 days after CHOP (PMID 22355761) | MEASURED (dog), for unarmed T cells |
| Toxicity | human BATs: grade 1-2 infusion reactions, no DLT; GD2 BATs CRS grade 2-3 fevers in all (PMIDs 36255393, 38519053, 32939319) | OUTCOME (human) |
| Availability for dogs | **needs development** (T-cell product is available; armed bispecific is not) | -- |

### 10.3 eBAT / immunotoxin class
| Input | Value | Grade |
|---|---|---|
| eBAT (EGFR/uPAR) against lymphoma | targets low: lymphoma EGFR and PLAUR mRNA significantly below sarcoma (n=29); EGFR/uPAR-negative T-cell lymphoma line not killed | MEASURED (RNA, dog), protein NOT FOUND -> **eBAT as built is not a lymphoma kill agent; treat as stromal/TAM lever only at most** |
| Retargeted angiotoxin (CD19/CD20/CD22-directed PE or DT toxin) | human DT2219 phase I 2 durable responses of 25; moxetumomab durable CR 36%, CR>=60 months 61% of CR | OUTCOME (human), different disease; canine-targeted version does not exist -> needs development |
| Division gating | none (EF-2 ADP-ribosylation; inhibits protein and DNA synthesis) | mechanism (in HSA record; PMID 28193671) |
| Pump substrate | not found as a substrate; "overcome... resistance of cancer cells to conventional cytotoxic agents" is a statement, not a measurement (PMID 23553371) | mechanistic, direct data NOT FOUND |
| CNS access | not found; a ~70 kDa fusion protein; intracranial use has only been shown with convection-enhanced delivery in glioma models (PMID 19517064) | NOT FOUND |
| Toxicity (dog) | single cycle 50 ug/kg: hypotension 4/23 reversible, liver 2/23; 3 cycles: hypotension 6/25; no benefit on redosing; neutralising antibodies sporadic | MEASURED (dog) |
| Availability for dogs | eBAT: trial/research only (Minnesota-manufactured clinical lot; not licensed); retargeted: needs development | -- |

---------------------------------------------------------------------
## 11. WHAT I SEARCHED AND DID NOT FIND (strength: not found in PubMed titles/abstracts and the PMC full texts opened)
- Any canine CD3xCD20/CD19 bispecific, canine BiTE, caninized bispecific T-cell engager, canine TriKE/NK engager, canine armed-T-cell (BAT) study: NOT FOUND (only a 2026 review proposing it).
- Binding data for any therapeutic CD3 engager arm on canine T cells; anti-human CD3 (OKT3, UCHT1, SP34) binding to canine CD3 extracellular domain: NOT FOUND.
- Canine anti-drug antibody data for human bispecifics: NOT FOUND.
- EGFR/uPAR protein expression in canine lymphoma; eBAT in lymphoma: NOT FOUND (RNA only).
- Direct in-vitro killing of quiescent or P-gp-high lymphoma cells by CD3 engagers: NOT FOUND (inference from mechanism and clinical subgroups).
- Blinatumomab or any engager CSF:serum ratio (other than glofitamab 0.44% max): NOT FOUND; intrathecal engager use: NOT FOUND; full text of PMID 38484137 (publisher blocks XML and PMC web page): NOT READ beyond abstract.
- Per-day tumour kill-rate constants or ctDNA half-lives in the epcoritamab/glofitamab PK-PD papers: NOT RETRIEVABLE (full text empty); kill rate in section 6 is therefore derived from timing.
- Any 5-year or 10-year PFS plateau for CD3xCD20 engagers: NOT FOUND. MS4A1 mutation frequency after engagers: NOT FOUND (only qualitative and the 59% CD20-loss case series).
- CD3 engagers in T-cell lymphoma with clinical efficacy: NOT FOUND (preclinical UMG1; T-ALL phase 1 n=9).
- Glofitamab CD20-arm derivation from obinutuzumab and exact CD3-arm family of epcoritamab/mosunetuzumab/odronextamab: NOT VERIFIED (only the families listed in PMID 40987715's abstract were used).
- Unverified assumption: 1 cm3 of tumour = 1e9 cells and PET detection about 1 cm3 (used in section 6, flagged ASSUMED).

## 12. Record check (CLAUDE.md rule 1)
- Already covered (where): CD3-bispecifics listed "NOT ASSESSABLE ... no therapy data" (`docs/LYMPHOMA_UNIVERSE.md` line 31); "No canine CD3xCD20 or CD3xCD19 engager found. Human bispecific literature was searched but the returned records were not verified, so no human figure is cited" (`docs/universe/SWEEP_modalities.md` section 3.2 and lines 196, 207); status line 159 of `docs/LYMPHOMA_STATUS.md`. Canine CD20 antibodies 38662527 and CAR-T 41376156/32002286 are already in the record. CD19-negative relapse after bispecifics (PMID 34312556) and CSF CAR-T figures (PMID 37345469) are already in `SWEEP_cart_human.md`.
- eBAT: in HSA record (README sections, `docs/HSA_DURABLE_RESPONSE.md`: 5.2 to 7.8 logs, 6-month survival <40% to ~70%, redosing failure); not covered for lymphoma: new here (targets low in canine lymphoma).
- Not covered before this report (new): human CD3-engager efficacy/durability/CNS/MRD figures with verified PMIDs; CD3/CD20/CD19 human-dog sequence identity; commercial canine T-cell expansion citation for the BAT route; DT2219 and moxetumomab class transfer.
