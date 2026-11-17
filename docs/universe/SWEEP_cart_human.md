# Human CAR-T data to replace the CNS CAR-T assumptions (canine multicentric lymphoma durable-response model)

Status: COMPLETE (written progressively, final 2026-10-01). All 127 PMIDs cited were fetched from PubMed records in this session and every DOI printed in a table row was machine-checked against the record (0 mismatches). Numbers are quoted from the PubMed abstract unless marked "FULL TEXT".

## Success criteria (user's words, quoted verbatim; graded against exactly these)
- "make sure every mechanism and every escape is closed by either real data or rigorous model, potency, toxicity etc all need to be considered"
- "looking for 10+ years of durability"; "assuming early detection"
- "I'm okay with no specific data but if scientifically sound" -> a transferred number is acceptable IF the transfer is justified in writing and graded TRANSFER; no-basis numbers stay ASSUMED.
- "keep going by more research or modeling to fully close every mechanism and escape then. I know car t has human results for CNS"
- Not asked: "demonstrated in dogs" (user knows it is unmet; not reported as a finding).

Record check (CLAUDE.md rule 1): `docs/LYMPHOMA_STATUS.md` on origin/claude/duplicate-codex-prefix-branch-lt1qh6 lists CAR-T properties as ASSUMED ("CD20 CAR-T in vivo" potency, CNS access, CSF persistence) and canine CAR-T persistence 14-50 days (PMID 32002286, 35898541). No human CAR-T numbers are recorded there. So everything below is "not covered" in the record.

Search note: the PubMed MCP maps the bare string "CAR T" to an author tag and returns 0; use "CAR-T" or "chimeric antigen receptor".

## SUMMARY (read this first; details, quotes and weaknesses follow)

| Model input | Proposed value (range) | Grade as human data / as applied to dog | One-line basis |
|---|---|---|---|
| (a) IV CAR-T CNS access, kill multiplier vs systemic | 0.5 (0.1-1.0) | OUTCOME-DERIVED / TRANSFER | CR in CNS lymphoma 47-57% vs systemic LBCL 40-54% (ratio ~1), durability ~0.5 (2-y PFS 28%, relapse 59%) |
| (a') IV CAR-T CSF:blood concentration ratio | 0.003-0.04 (central ~0.01-0.03) | DERIVED (cross-study) / TRANSFER | CSF peak 0.19-0.50 cells/uL vs blood peak 12-66 cells/uL; do NOT use 0.5 as a concentration ratio |
| (a'') IT/ICV route access | >1 vs blood (~50x DNA-normalised, cross-trial) | MEASURED (n=6, solid tumour) / TRANSFER | 109,235 copies/ug CSF vs <=2,000 blood in IV trials |
| (b) durable fraction, CNS B-cell, CAR-T alone | 0.28 at 2 y (0.16-0.43) | OUTCOME / TRANSFER | EBMT n=100: 24-mo PFS 28%; LOC 1-y PFS 43% plateau |
| (b) durable fraction, systemic B-cell | 0.30-0.40 long term | MEASURED human / TRANSFER | ZUMA-1 31% ongoing at 63 mo; 10-y lymphoma-free survival 32% (LBCL), 47% (FL) |
| (b) CNS + ASCT-like consolidation | ~0.65 at 2 y (retrospective) | OUTCOME / TRANSFER | 65.5% vs 30.0% CAR-T alone |
| (b) 2 y disease-free -> 10 y | supported in systemic humans (ZUMA-1 5-y OS 92.3% if EFS at 24 mo; no relapse beyond 5.4 y in 38 pts) but competing risks (second cancer 21%, NRM 18% at 10 y) | MEASURED systemic / TRANSFER | CNS-specific plateau NOT FOUND |
| (c) persistence needed | functional CAR-T >= 28-90 d (clearance), 6-12 mo margin | DERIVED / TRANSFER | ctDNA-negative by day 7 in 70% of durable responders, all by 3 mo; most failures in year 1 |
| (c) human persistence achieved | terminal half-life 220 d; >5-10 y in subsets; CSF to 17 mo | MEASURED human | not transferable to dog (canine 14-50 d measured) |
| (c) CSF-delivered single dose | ~14 d (7-28 d) | TRANSFER (solid tumours only) | CSF peak d1-7, cytokines baseline <2 wk |
| (d) CNS_LOCAL (TIAN) axis | 0.18 (0.10-0.30), fatal 0.02-0.04; volume-dependent | MEASURED human incidence / TRANSFER | 10/56 (17.9%), 1 fatal; threshold >3.4 cm3 |
| (d) immune-mediated ICANS grade>=3 | 0.17 (0.10-0.26); neurotoxicity death ~2% | MEASURED human / TRANSFER | EBMT 17/100; meta 17.4%; SCNSL up to 26-44% |
| (e) antigen-loss share of B-cell CAR-T failures | 0.30 (0.28-0.63); T-lineage >=0.5 | MEASURED small n / DERIVED | 5/18 paired biopsies; 10/16; ALL 30% of relapses; CD7 loss in 10/10 relapse specimens |
| Quiescent-cell kill, duty factor f for CAR-T | 1 (not division-gated) | TRANSFER (mechanism; no human measurement) | CTL kill in G1/S/G2/M and arrested cells; senescent-cell kill incl. NHP; mouse counter-examples |
| MHC/HLA loss | CAR-T unaffected (MHC-independent) | TRANSFER + indirect OUTCOME | abnormal HLA 62% DLBCL, 77% PCNSL yet CR 50-57% |
| CAR-T potency 0.12/day | stays ASSUMED | ASSUMED | no measured human net kill rate found; human data not in conflict |

Most important counter-evidence: in humans, thiotepa-ASCT beats CAR-T for secondary CNS lymphoma after propensity matching (PFS HR 0.45, OS HR 0.41; n=1139) and CAR-T alone leaves 59% relapse by 24 months, so CAR-T alone does not close the CNS escape at the strength the model assumed; combinations are what the human data support.

## TOPIC 1: CAR-T in CNS lymphoma / CNS leukaemia (human)

| PMID | DOI | Study | n | Efficacy (exact, from abstract) | ICANS / CRS | Notes |
|---|---|---|---|---|---|---|
| 35167655 | 10.1182/blood.2021014738 | Frigault, Blood 2022. Tisagenlecleucel in PCNSL, phase 1/2 (NCT02445248) | 12 relapsed PCNSL | "Seven of 12 patients (58.3%) demonstrated response, including a complete response in 6/12 patients (50%)... Three patients had ongoing complete remission at data cutoff... sustained remission in 3/7 (42.9%) of initial responders." Median follow-up 12.2 mo (3.64-23.5) | "Grade 1 CRS in 7/12 (58.3%), low-grade ICANS in 5/12 (41.6%) patients, and only 1 patient experienced grade 3 ICANS." | "Tisagenlecleucel expanded in the peripheral blood and trafficked to the CNS. Exploratory analysis identified T-cell, CAR T, and macrophage gene signatures in CSF following infusion" |
| 34492703 | 10.1182/bloodadvances.2020004106 | Siddiqi, Blood Adv 2021. CD19CAR (City of Hope, NCT02153580) in PCNSL | 5 PCNSL | "3 of 5 patients (60%; 90% CI 19-92%) seemed to achieve complete remission... remaining 2 stable disease" | "All patients developed grade >=1 CRS and neurotoxicity; reversible; no treatment-related deaths" | Abstract: "CD19CAR T cells administered IV are detectable in CSF, suggesting CAR T cells can migrate from the periphery into the CNS" |
| 38586986 | 10.1002/ajh.27316 | Choquet, Am J Hematol 2024 (LOC network), relapsed PCNSL, real-life | 27 leukapheresed, 25 infused | "best response ... CR in 16 patients (64%). One-year PFS from leukapheresis was 43% with a plateau afterward. One-year RFS was 79% for patients in CR or PR at infusion." Median OS 21.2 mo; median follow-up 20.8 mo; controls (n=247) median PFS 3 mo, OS 4.7 mo | CRS 23/25; neurotoxicity 17/25 (68%), 5 grade >=3 | Plateau at 1 y. Follow-up too short for 2-5 y |
| 36260735 | 10.1182/bloodadvances.2022008525 | Cook, Blood Adv 2023 meta-analysis | 128 (30 PCNSL, 98 SCNSL) | PCNSL: 56% CR, 37% in remission at 6 mo. SCNSL: 47% CR, 37% in remission at 6 mo | PCNSL: CRS any 70% (13% gr 3-4), ICANS any 53% (18% gr 3-4). SCNSL: CRS 72% (11% gr3-4), ICANS 48% (26% gr 3-4) | "toxicity... similar to registrational studies in systemic LBCL" |
| 40400509 | 10.1002/hem3.70146 | Ossami Saidy, HemaSphere 2025 (EBMT/GoCART) | 100 CNS-manifest, 67 with active CNS disease at CART | "Overall and PFS at 24 months were 37% and 28%. Relapse incidence at 24 months was 59%, NRM at 1 y 7%" | "CRS and ICANS any grade 83% and 42%. CRS gr3 in 11, ICANS gr3-4 in 17 patients. Two patients died of neurotoxicity." | LDH elevated: HR 2.4 for RI. ECOG 2-3 HR 2.68 for ICANS |
| 40146949 | 10.1212/WNL.0000000000213501 | Hernandez-Tost, Neurology 2025, French LOC | 48 (28 PCNSL, 20 SCNSL) isolated CNS relapse | n/a (neurotoxicity study) | "31 patients (65%) neurotoxicity, 11 grade 3-4 (23%). Onset median day 5 (1-10)." "Brain MRI pseudoprogression in 7/26 (27%); transient increase in CSF IL-10 in 7/29 (24%)". Grade 3-4 neurotoxicity median duration 100 d (4 d-18 mo) | |
| 41948499 | 10.3389/fonc.2026.1790444 | Shawabkeh, Front Oncol 2026 meta-analysis | 38 studies | "pooled ORR 0.75 [0.70-0.79]; CR 0.52 [0.46-0.58]; PR 0.18" | "CRS 83.5%, gr>=3 5.77%. ICANS 44.9% [36-54], gr>=3 17.4% [12-23]" | No difference PCNSL vs SCNSL |
| 41701972 | 10.1182/bloodadvances.2025018604 | Rankin, Blood Adv 2026, CD19-CAR in B-ALL with EMD/CNS | 308 children/young adults: CNS n=36, EMD n=21, iBM n=251 | 24-mo OS iBM 71.5%, EMD 66.7%, CNS 57.0% (P=.032); EFS 51.8%, 45.8%, 35.2% (P=.035). "Eight patients (80%) with isolated CNS disease (n=10) had clearing of the CNS, and 3 (37.5%) subsequently relapsed." CNS-LD vs CNS-HD (low vs high marrow burden): OS 92.3% vs 33.3%; EFS 63.6% vs 14.3% | ICANS not in abstract | CNS disease with low marrow burden did well (EFS 63.6%) |
| 32888407 | 10.1016/S0140-6736(20)31366-0 | Abramson, Lancet 2020 TRANSCEND NHL 001 (liso-cel) | 269 treated, 7 (3%) secondary CNS | systemic: ORR 73%, CR 53%. Neuro events 30%, gr>=3 10% | - | Reference ICANS rate in systemic LBCL |


### 1b. Additional CNS lymphoma / CNS leukaemia studies (abstract numbers)

| PMID | DOI | Study | n | Key numbers (quoted) |
|---|---|---|---|---|
| 41530773 | 10.1186/s13045-025-01761-8 | MGH, J Hematol Oncol 2026: patterns of CD19-CAR failure in CNSL | 60 recurrent CNSL | "ORR 60% (45% CR, 15% PR)... Median CNS-PFS1 was 4 months with radiographic PD in 36 patients (local 23.3%; local and distant 16.7%; distant 20%)... Distant relapse typically occurred after CR whereas local PD followed CD19-CAR refractory disease... Leptomeningeal involvement (LMD) was associated with recurrence after CR... At progression, peripheral CD19+-B-cell aplasia suggested CD19-CAR persistence in 93% of patients. Median CNS-PFS2 after CAR failure one month." |
| 37946255 | 10.1186/s13045-023-01508-3 | SCNSL multicentre retrospective, J Hematol Oncol 2023 | 61 | "ORR 68%, CR 57%. Median PFS 3.3 mo, 6- and 12-month PFS 35% and 16%. OS 6/12 mo 59%/41%. CRS any 70%, ICANS any 57%, grade>=3 CRS 16%, ICANS 44%." Leptomeningeal +/- parenchymal involvement raised ICANS risk |
| 35351785 | 10.1212/WNL.0000000000200608 | Neurology 2022, SCNSL after CD19 CAR-T | 10 | "disease response in 7 (70%), including 2 cases of long-lasting CR (20%)... Neurotoxic symptoms in 6, severe (grade>=3) in 3". "CNS response reflects systemic response" |
| 35796863 | 10.1007/s00262-022-03246-w | Cancer Immunol Immunother 2023 meta-analysis | 63 (8 studies) | "pooled OR 69%, CR 51%. Pooled rate of progressive disease after remission was 38% (21-55%). Grade >=3 neurotoxicity 12% (3-24%)" |
| 38328579 | 10.3389/fphar.2023.1331844 | Front Pharmacol 2023, individual-patient meta-analysis of duration of response | 69 (12 studies) | "pooled relapse rate was 45% [35-56]... ASCT plus CAR-T associated with lower relapse (HR 0.26 for DoR)" |
| 41490516 | 10.1182/blood.2025031455 | Alderuccio, Blood 2026, SCNSL international cohort | 1139 | "Higher survival with thiotepa-ASCT than CAR-T was observed after PSM (PFS HR 0.45; P=.005; OS HR 0.41; P=.014)". 2-y PFS 40.4% de novo, 43.9% CNS-isolated relapse, 16.2% synchronous relapse. COUNTER-EVIDENCE: CAR-T inferior to thiotepa-ASCT in this comparison |
| 40663771 | 10.1182/blood.2025028964 | Blood 2025: tumour inflammation-associated neurotoxicity (TIAN) in CNSL with CD19-CAR | 56 | "TIAN occurred in 10/56 (17.9%), onset median 3.5 d (1-9)... distinct from ICANS... larger CNS tumour volume at baseline (>3.4 cm3: 87.5% sens, 80.5% spec)... TIAN correlated with higher ORR (90% vs 52%) and improved PFS (HR 0.22)... Postmortem: dense macrophage population with central necrosis and peripheral reactive gliosis". Model relevance: a CNS_LOCAL on-tumour axis separate from systemic ICANS |
| 34560014 | 10.1016/S2352-3026(21)00238-6 | Leahy, Lancet Haematol 2021 (CHOP pooled 5 trials; CNS ALL) | 195 (66 CNS-positive, 129 CNS-negative; 43 isolated CNS) | "CR at 28 d: 97% (64/66) CNS-positive vs 94% (121/129) CNS-negative (p=0.74). 2-y RFS 60% (49-74) vs 60% (51-71) p=0.50; 2-y OS 83% vs 71% p=0.39. Neurotoxicity any grade 41% (CNS-neg) vs 58% (CNS-pos), grade 3: 9% vs 9%, grade 4: 2% vs 3% (p=0.20). Median follow-up 39 mo (CNS+), 36 mo (CNS-)". Trials required CNS control at infusion. ANSWER to "do CNS outcomes equal non-CNS": in paediatric ALL, YES at 2 y |
| 35468946 | 10.1038/s41375-022-01546-9 | Leukemia 2022, international retrospective, active CNS BCP-ALL | 55 | "51/54 (94%) CR... Relapse occurred in 22 patients: 19/43 after 4-1BB CARs (12 CNS relapses), 3/12 after CD28 CARs with subsequent HSCT (no CNS relapse). Patients treated with tisagenlecleucel for an isolated CNS relapse had a high incidence of subsequent CNS relapse (6 of 8)... CRS 65%, neurotoxicity 38%." COUNTER-EVIDENCE: CNS relapse risk not eliminated |
| 40334068 | 10.1182/bloodadvances.2024015779 | Brexu-cel ROCCA, adult B-ALL CNS-2/3 | 31 | "21/24 (87.5%) achieved CNS-1... grade 3/4 ICANS 35.5% with CNS disease vs 30% without; no significant PFS/OS difference" |
| 42702862 | 10.1002/cam4.72262 | Cancer Med 2026, R/R B-ALL | 113 (22 CNS+, 91 CNS-) | "Day-28 CR 81.8%, no difference. 3-y CIR, EFS, OS similar. However CNSL patients exhibit a higher cumulative relapse rate following CAR-T-induced remission with increased risk of CNS relapse... CAR-T not sufficient to maintain sustained remission; consolidative allo-HSCT protective" |
| 36346962 | 10.1200/JCO.22.01214 | Wang, JCO 2023, CD19+CD22 co-administered CAR-T paeds B-ALL | 225 evaluable; 194 refractory/haematologic relapse | CR 99.0% (all MRD-neg); 12-mo EFS 73.5%; "Relapse occurred in 43 patients (24 CD19+/CD22+ relapse, 16 CD19-/CD22+, one CD19-/CD22-, two unknown)"; isolated CNS relapse (n=10) 12-mo EFS 68.6% (44.5-100); isolated testicular (n=20) 12-mo EFS 95.0%; CRS 88.0%, neurotoxicity 20.9%, 3 deaths |
| 27526682 | 10.1186/s13045-016-0299-5 | Hu 2016, J Hematol Oncol, single case ALL | 1 | "qPCR for CAR constructs showed 3,032,265 copies/ug DNA in CSF and 988,747 copies/ug DNA in blood" (ratio of 3.07 per ug DNA, day 5, in a patient with cerebral CRS; this is per DNA mass, NOT per volume) |

### 2. CSF PHARMACOLOGY OF IV CAR-T (human)

| PMID | DOI | Study | n | Numbers (quoted) |
|---|---|---|---|---|
| 37345469 | 10.3324/haematol.2023.282875 | Haematologica 2023, Pitie-Salpetriere, tisa-cel/axi-cel in CNSL; FULL TEXT read (PMC10690903) | 21 (13 PCNSL, 8 SCNSL) | "We first assessed the expansion of CAR T cells in the CSF for 16 patients. All tested patients demonstrated CSF positivity for CAR T cells regardless of clinical outcome with an initial phase of rapid expansion followed by a slow decrease with long-term persistence. On D30, the median number of CAR-T cells in the CSF was 0.17/mm3, reflecting 19% (range, 4-45) of CD3+ T cells, and the median CD4/CD8 CAR T-cells ratio was 4.2. The later CSF analysis assessed 17 months after the infusion in one R patient still demonstrated the presence of CAR T cells (41% of CD3)... the expansion peak in the CSF was significantly higher in R than in NR patients (0.50/mm3 vs. 0.19/mm3 (P=0.01))... a transient increase in IL-6 dosage was detectable during the first month for 76% cases." Clinical: D28 ORR 67% (29% CR, 38% PR); M3 ORR 43%; median PFS 3 months; median OS 15 mo; 8/21 (38%) persistent response at final follow-up (median 12 mo); CRS 16 (1 grade 3), ICANS 7 (2 grade>=3). CSF sampling: every 2 weeks first month then monthly. |
| 29025771 | 10.1158/2159-8290.CD-17-0698 | Gust, Cancer Discov 2017; FULL TEXT read (PMC5718945) | 133 adults | "Both CD4+ and CD8+ CAR-T cells were detected in the CSF by flow cytometry (CD4+/EGFRt+, median 2.6 cells/uL; CD8+/EGFRt+, median 2.1 cells/uL). CAR-T cells comprised a higher fraction of the CD4+ T cell subset in CSF compared to blood... CAR-T persisted in CSF at high frequency in a subset of patients after recovery from neurotoxicity, but were infrequent in CSF from patients who had not previously developed neurotoxicity." AUTOPSY (fatal neurotoxicity, d13): "T cells constituted 56.9% of CD45+ cells and most of the T cells in the brain were CAR-T cells, with 93% of the T cells in the pons expressing the EGFRt transduction marker." Measured in patients with BBB disruption (selection bias toward toxicity) |
| 29880584 | 10.1158/2159-8290.CD-17-1319 | Santomasso, Cancer Discov 2018 (19-28z CAR, adult ALL); FULL TEXT read | 53 | "In 19 of 21 patients (95%), including patients with mild or no neurotoxicity, CAR T cells were detected in CSF (qPCR), and the quantity of CAR T cells in CSF did not correlate with neurotoxicity severity (p=0.404)." CSF IL6, IL8, MCP1, IP10 disproportionately high in CSF (suggesting CNS-specific production). Blood-CSF barrier disruption (protein, Qalb) scaled with grade. |
| 27526682 | 10.1186/s13045-016-0299-5 | Hu 2016 (above) | 1 | CSF 3,032,265 vs blood 988,747 copies/ug DNA; CSF IFN-g and IL-6 "extremely higher than serum" (cerebral CRS, in situ production) |
| 34496024 | 10.1182/bloodadvances.2021004889 | Fatal late-onset CAR-T encephalitis after axi-cel, case | 1 | "High CAR T-cell DNA copy numbers and elevated IL-1 and IL-6 in the CSF... CAR T-cell brain infiltration was observed on autopsy" (month 9; late) |
| 39152952 | 10.1016/j.jcyt.2024.07.015 | Brexu-cel late neurotoxicity case | 1 | "new CAR T-cell expansion with an unexpectedly elevated CSF/blood ratio" (day +58) |
| 35950534 | 10.3324/haematol.2022.281110 | Haematologica 2023 ddPCR CSF kinetics in severe ICANS | n/a (abstract) | "CAR T-cell enrichment within CSF in ICANS patients with further progressive accumulation despite intense corticosteroid-containing immunochemotherapies in a subset with prolonged grade 3-4 neurotoxicity... a major fraction of hyperexpanded T-cell clones were of non-CAR derivation" |
| 35152726 | 10.1089/hum.2021.249 | Hum Gene Ther 2022, CD19 or CD20 CAR-T in CNSL | 7 (6 SCNSL, 1 PCNSL) | "All responded; 4 CR, 3 PR; CD19 or CD20 CAR T cells could be detected in the CSF of four patients... median duration of CR 22.4 months... disease progression in 3 (median f/u 10.4 mo), and the antigen loss of CD20 was confirmed as the reason for relapse in one patient." |
| 35167655 | 10.1182/blood.2021014738 | Frigault 2022 | 12 | "expanded in the peripheral blood and trafficked to the CNS... CAR T gene signatures in CSF following infusion" (no counts in abstract) |
| 34492703 | 10.1182/bloodadvances.2020004106 | Siddiqi 2021 | 5 | "CD19CAR T cells administered IV are detectable in CSF" |
| 31074527 | (not yet read) | Glial injury in neurotoxicity after paediatric CD19 CAR | | (to read) |


### 2b. Blood-side comparators needed to turn CSF counts into a CSF:blood ratio
| PMID | DOI | Study | Numbers (quoted) |
|---|---|---|---|
| 34100900 | 10.1182/bloodadvances.2020003959 | Blood Adv 2021, real-world axi-cel, n=21 | "Median peak CAR-T-cell count was 16.14 CAR-T cells/uL" |
| 36821768 | 10.1182/blood.2022018893 | ZUMA-1 5-y (FULL TEXT PMC10646788) | "median peak CAR T-cell level higher in patients whose response was ongoing at month 60 (65.76 cells per uL) than in those who relapsed (35.27) or did not respond (12.08)" |
| 33021872 | 10.1200/JCO.20.01467 | Cappell, JCO 2020 (NCT00924326, FMC63-28z) | "Median peak blood CAR-positive cell levels were higher among patients with DOR >3 y (98/uL; range 9-1,217) than DOR <3 y (18/uL; range 0-308)" |
| 37345469 | (above) | CSF (tisa-cel mostly) | day-30 median 0.17/mm3 (19% of CD3+); peak R 0.50/mm3 vs NR 0.19/mm3 |
| 29025771 | (above) | Gust (CD19 CAR, EGFRt marker, during neurotoxicity) | CSF CD4+ CAR 2.6/uL, CD8+ CAR 2.1/uL (BBB-leaky patients) |
| 38968138 | 10.1182/blood.2024024952 | Blood 2024, NKTR-255 + CAR19-22 phase 1, B-ALL | "increase in chemokines (CXCL9, CXCL10)... decreases in blood CD8+ CAR T cells and 10-fold increases in CSF CAR-T cells, suggesting lymphocyte trafficking to tissue" => CSF CAR-T count is chemokine-modifiable |
| 38554710 | 10.1016/j.medj.2024.03.002 | Med 2024, CD19 CAR-T (KYV-101) in 2 MS patients | "No ICANS despite detection of CD19 CAR-T cells in CSF... CAR-T presence and expansion were observed in the CSF... intrathecal antibody production decreased" |
| 38728414 | 10.1126/sciimmunol.adj9730 | Sci Immunol 2024, BCMA CAR-T in NMOSD, paired CSF/blood single-cell | "CAR T cells with enhanced chemotaxis efficiently crossed the blood-CSF barrier, eliminated plasmablasts and plasma cells in the CSF" (non-malignant CNS target; CSF-compartment kill shown) |
| 41101309 | 10.1016/j.cell.2025.09.020 | Cell 2025, BCMA CAR-T in progressive MS | "plasma cell depletion in CNS compartments, prolonged expansion and relieved exhaustion of CAR-T in CSF" (5 patients) |
| 36681817 | 10.1186/s13045-023-01402-y | gamma/delta TCR-T anti-CD19 (ET019003), n=8 DLBCL incl. 1 PCNSL | "PCNSL patient: ongoing CR >3 years, with detectable ET019003 cells in CSF" (single patient; a TCR-T not CAR-T) |

### 3. DURABILITY / PERSISTENCE (human)

| PMID | DOI | Study | n | Numbers (quoted) |
|---|---|---|---|---|
| 42341302 | 10.1056/NEJMoa2518035 | NEJM 2026, 10-year outcomes after tisa-cel (CTL019, NCT02030834; first author Ruella) | 38 (24 LBCL, 14 FL) | "At a median follow-up of 10.1 years (range 7.9-11.5), no relapses had occurred beyond 5.4 years. The 10-year lymphoma-free survival was 32% (95% CI 14-51) among LBCL and 47% (20-71) among FL. 10-year PFS 17% (5-34) LBCL, 29% (9-52) FL; 10-year OS 17% LBCL, 50% FL... A second primary cancer developed in 9 patients (10-year cumulative incidence 21%). 10-year NRM 18%. Higher CAR-transgene persistence appeared associated with long-term response. B-cell aplasia persisted in 44% of patients with a long-term response." |
| 42575986 | 10.1038/s41591-026-04578-1 | Nat Med 2026, decade-long persistence of CART19 in lymphoma | 38 | "Beyond year five, the CAR19 transgene was detectable in five of eight long-term responders (7.0-10.1 years), with three maintaining B cell aplasia... In one patient with PFS of 10.1 years, CART19 cells comprised 1.2% of circulating T cells 9.3 years after infusion... persisting cells predominantly double-negative (CD4-CD8-) effector-memory-like." |
| 35110735 | 10.1038/s41586-021-04390-6 | Melenhorst, Nature 2022, CLL | 2 patients | "CAR T cells remained detectable more than ten years after infusion, with sustained remission in both patients... highly activated CD4+ population dominated later time points... cytotoxic characteristics along with ongoing functional activation and proliferation." |
| 33021872 | 10.1200/JCO.20.01467 | Cappell, JCO 2020 (NCT00924326) | 43 pts, 46 treatments (28 DLBCL/PMBCL, 8 low-grade, 7 CLL) | ">3-year DOR in 51% (35-67) all evaluable; 48% (28-69) DLBCL/PMBCL; median EFS 55 mo. Remissions up to 9 years ongoing. Long-term adverse effects rare except B-cell depletion and hypogammaglobulinemia." |
| 36821768 | 10.1182/blood.2022018893 | ZUMA-1 5-y (FULL TEXT) | 101 | "ORR 83% (CR 58%); median follow-up 63.1 mo; responses ongoing in 31%. 5-y OS 42.6% (32.8-51.9); DSS 51.0%. Among those with no EFS event by 24 mo, 5-y OS 92.3% (78.0-97.5) vs 11.3% with an event. Deaths by year (of 101): yr1 40, yr2 10, yr3 4, yr4 3, yr5 1, >5: 1 (a secondary malignancy). Deaths from progressive disease: yr1 32, yr2 9, yr3 3, yr4 0, yr5 1, >5 0." CR patients: 5-y OS 64.4% |
| 41765136 | 10.1016/j.jtct.2026.02.058 | Landmark analysis, 479 commercial CD19 CAR-T LBCL | 479 | "indicating a trend toward cure, though longer follow-up is needed" (no plateau numbers in abstract) |
| 41804087 | 10.1002/ajh.70281 | TanCAR7 (CD19/CD20) 5-year, single-centre phase 2 | 87 | "ORR 78% (CR 70%), median follow-up 63.4 mo, 40% remain in remission; 5-y OS 60.1%; median PFS 33 months" |
| 41512222 | 10.1182/bloodadvances.2025018073 | zamto-cel (CD20/19 tandem) 5 y | 12 | "5 of 12 (42%) CR until month 12 with no relapse in clinical evaluation up to 5 years" |
| 40631584 | 10.1111/ejh.70003 | HemoBase registry LBCL late relapse (not CAR-T) | 877 | systemic LBCL comparator: 5-y OS 18-20% for relapsed, pre-CAR-T era |

(note: ALL durability papers (ELIANA 5-y etc.) still to search)

### 4. ANTIGEN-LOSS RELAPSE AND DUAL-TARGET CAR-T (human)

| PMID | DOI | Study | n | Numbers (quoted) |
|---|---|---|---|---|
| 34041526 | 10.1182/blood.2021010930 | Plaks, Blood 2021 (ZUMA-1 biopsies; FULL TEXT PMC8462361) | 100 pre-treatment, 20 post-relapse biopsies | "Among 18 paired biopsies, 5 (28%) exhibited substantially lower CD19 protein levels at relapse... CD19- relapse occurs in ~30% of patients after axi-cel in LBCL... CD19- (vs CD19+) relapses enriched in patients with lower pretreatment TB with high CAR-T expansion (50% vs 21%) or longest time to relapse (9 vs 3 months)... Among 20 relapsed tumours, most expressed other B-cell antigens (95% CD20, 90% CD22, 95% CD79a)... suboptimal in vivo CAR-T expansion relative to tumour burden (CD19+ relapses)." Pre-treatment: 90% CD19+, 93% CD20+, 98% CD19+ and/or CD20+. |
| 34312556 | 10.1038/s41591-021-01436-0 | Spiegel, Nat Med 2021, CD19/22 CAR in adults B-ALL (n=17) and LBCL (n=21) | 38 | "Ten of 16 patients with LBCL with progressive disease after CAR19 had absent or low CD19. Lower surface CD19 density pretreatment was associated with PD... Relapses were CD19-/lo in 50% (5/10) of B-ALL and 29% (4/14) of LBCL after the dual CAR, but were not associated with CD22-/lo disease." B-ALL: 100% response, 88% MRD-neg CR; LBCL: 62% response, 29% CR. "More than 50% of patients treated with CAR19 experience progressive disease." |
| 36346962 | 10.1200/JCO.22.01214 | Wang, JCO 2023, co-administered CD19+CD22 CAR-T paediatric B-ALL | 225 | "Relapse in 43: 24 CD19+/CD22+, 16 CD19-/CD22+, 1 CD19-/CD22-, 2 unknown" => 16/41 (39%) of classified relapses were CD19-/CD22+ (antigen loss with escape of one target), only 1/41 (2.4%) lost both. 12-mo EFS 73.5% |
| 37647647 | 10.1182/blood.2023020621 | Blood 2024, CARPALL cotransduced CD19/22 CAR | 12 | "10/12 (83%) MRD-neg CR... of 10 responders 5 had MRD(2) or relapse(3) with CD19+ CD22+ disease associated with loss of CAR T-cell persistence... no cases of relapse due to antigen-negative escape (median follow-up 8.7 mo)" => relapses with dual-target were persistence loss, not antigen loss |
| 34642489 | 10.1038/s41591-021-01497-1 | Nat Med 2021, AUTO3 CD19/22 paediatric B-ALL | 15 | "remission rate 86% (13/15); 1-y OS 60%, EFS 32%. Relapses were probably due to limited long-term AUTO3 persistence" |
| 33020647 | 10.1038/s41591-020-1081-3 | Shah, Nat Med 2020, LV20.19 (CD20/CD19) | 22 | "ORR 82% (CR 64%)... Notably, loss of the CD19 antigen was not seen in patients who relapsed or experienced treatment failure. grade 3-4 neurotoxicity 14%" |
| 32556247, 34272481 | 10.1182/blood.2020005278; 10.1038/s41375-021-01345-8 | TanCAR7 CD19/CD20 phase 1/2 Blood 2020; Leukemia 2022 | 28; 87 | ORR 79% / 78%; 12-mo PFS 64%; median PFS 27.6 mo; "CRES grade 3 in 2 (2%)" |
| 39813680 | 10.1182/blood.2024026401 | prizlon-cel (CD19/CD20) Blood 2025 | 48 (44 LBCL) | ORR 91.5%, CR 85.1%; 2-y PFS 62.6%; ICANS 6.3%, none >=gr3 |
| 37526512 | 10.1080/10428194.2023.2232496 | Review, CD19-negative relapse after CD19 therapy in BCP-ALL | 23 CAR-T publications | "CD19-negative relapse ... after CAR-T vs blinatumomab: 8.7% vs 4.5% of all treated patients; 30% vs 22.5% of relapsing patients" |
| 30275569 | 10.1038/s41591-018-0146-z | Orlando, Nat Med 2018 | | CD19 mutations + LOH at CD19- relapse: "irreversible loss of CD19" (genetic mechanism) |
| 40578903 | 10.1158/2643-3230.BCD-24-0176 | Blood Cancer Discov 2025 (preclinical, DLBCL lines + 2 clinical trial signatures) | | "DLBCL cells surviving CD19 CAR T-cells develop a resistance phenotype... cross-resistance between CAR T cells targeting different antigens (CD20, CD22)" (non-antigen resistance: apoptosis resistance) |
| 35152726 | 10.1089/hum.2021.249 | CNSL CD19 or CD20 CAR-T | 7 | one of three progressions due to CD20 antigen loss |


### 3b. More durability / persistence / kinetics (human)

| PMID | DOI | Study | n | Numbers (quoted) |
|---|---|---|---|---|
| 42525896 | 10.1200/JCO-25-01471 | ELIANA 5-year, JCO 2026 (tisa-cel, paediatric/YA B-ALL) | 79 infused; 70 responders | "median follow-up 79.4 months. Estimated 5-year RFS among responders (n=70) with and without inclusion of SCT in censoring: 47.3% and 51.0%. Estimated OS at 5 years 55.0% and 62.4%. 17 responders received post-infusion SCT, 14 in CR." |
| 36399695 | 10.1200/JCO.22.00642 | ELIANA 3-year, JCO 2023 | 79 | "EFS 44% and OS 63% at 3 years overall (most events occur within the first 2 years)... 3-year RFS 52% / 48%" |
| 29385370 | 10.1056/NEJMoa1709866 | ELIANA primary, NEJM 2018 | 75 | "overall remission rate within 3 months 81%, all MRD-negative... Persistence of tisagenlecleucel in the blood was observed for as long as 20 months. CRS 77%; Neurologic events occurred in 40%, no cerebral edema." |
| 41252666 | 10.1200/JCO-25-00507 | JULIET 5-year, JCO 2026 (tisa-cel LBCL) | 115 | "median follow-up 74.3 months... 60-month relapse-free probability was 61% among responders. PFS at 60 months 28%. OS at 60 months 32% for all infused and 56% for those achieving CR or PR." |
| 37272527 | 10.1056/NEJMoa2301665 | ZUMA-7 OS, NEJM 2023 (axi-cel 2nd line) | 359 (180 axi-cel) | "median follow-up 47.2 months... estimated 4-year OS 54.6% vs 46.0%... 4-year PFS 41.8% vs 24.4%" |
| 29226797 | 10.1056/NEJMoa1707447 | ZUMA-1 primary, NEJM 2017 | 101 treated | "ORR 82%, CR 54%... grade >=3 CRS 13% and neurologic events 28%. Higher CAR T-cell levels in blood were associated with response." |
| 30501490 | 10.1056/NEJMoa1804980 | JULIET primary, NEJM 2019 | 93 | "best ORR 52%, CR 40%... grade 3/4 CRS 22%, neurologic events 12%... No differences between response groups in tumor expression of CD19" |
| 37879047 | 10.1182/blood.2023021243 | ZUMA-5 3-year (axi-cel iNHL) | 127 FL, 31 MZL | "ORR FL 94%; median PFS 40.2 months in FL... very few relapses beyond 2 years" |
| 38194692 | 10.1182/blood.2023021567 | ELARA update (tisa-cel FL) | 97 | "24-month PFS 57.4%, DOR 66.4%, OS 87.7%; CR 68.1%" |
| 37774014 | 10.1182/bloodadvances.2023011399 | Liang 2023, CD19 CAR CLL long-term (NCT01865617) | 47 | "median follow-up 79.6 months. Median PFS 8.9 months, 6-year PFS 17.8%... 6-year DOR 26.4%, OS 31.2%. Day +28 MRD negativity by flow HR 0.08; longer CAR T-cell persistence HR 0.56 for PFS" |
| 42036693 | 10.1186/s13045-026-01797-4 | ZUMA-2 5-year (MCL) | 68 | "median follow-up 67.8 months; median DOR 36.5 mo (n=60); 5-year cumulative relapse-related mortality 40% (24/60), non-relapse mortality 22% (13/60) in responders" |
| 30848084 | 10.1002/psp4.12388 | Stein, CPT-PSP 2019, tisa-cel population CAR-T kinetics (ALL, 2 phase II studies) | pooled | "The doubling time, initial decline half-life, and terminal half-life for tisagenlecleucel were 0.78, 4.3, and 220 days, respectively." |
| 28935694 | 10.1182/blood-2017-06-786129 | Mueller, Blood 2017 CTL019 cellular kinetics | 103 (ALL+CLL) | "peaked at 10 to 14 days... CTL019 transgene levels were measurable up to 780 days in peripheral blood. CTL019 trafficking and persistence were observed in bone marrow and cerebrospinal fluid." |
| 34133196 | 10.1200/JCO.21.00377 | Frank, JCO 2021 ctDNA after axi-cel | 72 | "Twenty-three of 33 (70%) durably responding patients versus 4 of 31 (13%) progressing patients demonstrated nondetectable ctDNA 1 week after axi-cel infusion... All durably responding patients had undetectable ctDNA at or before 3 months... ctDNA detected at or before radiographic relapse in 29/30 (94%)." (Human data on how fast durable responders clear tumour) |
| 37723652 | 10.1111/ejh.14078 | Case series, late isolated CNS relapse after CAR-T in LBCL | 3 | "Late relapse composed of 1/3 to 1/2 of CAR-T cell therapy failure" (abstract's wording; definition of late not in abstract) |

Interpretation notes (not data):
- ZUMA-1 full text (PMC10646788): "Among patients with (n=57) and without (n=44) an EFS event by 12 months, 5-year OS rates were 5.3% and 90.9%; with (n=62) and without (n=39) an EFS event by 24 months, 5-year OS 11.3% and 92.3%." "91% (21/23) of patients in ongoing response at 3 y showed polyclonal B-cell recovery" ("Protracted B-cell aplasia was not required for durable responses", abstract). This says durable responders were not dependent on persistent CAR activity => elimination rather than suppression in those patients.
- Ki-67 paper (PMID 42134593, n=79, single centre): "CAR-T cell persistence was not significantly associated with long-term remission or survival" but the 10-year CTL019 series (42341302) and the CLL series (37774014) (37774014: HR 0.56) say higher persistence associates with response. Conflict stated, not resolved.

### 5. CAR-T AND QUIESCENT / SLOW-CYCLING / PERSISTER CELLS

Directly measured in humans: NOT FOUND (no study measured CAR-T kill of G0/dormant tumour cells in patients). Evidence is indirect, graded below.

| PMID | DOI | Evidence | Species / level | Quote |
|---|---|---|---|---|
| 42134593 | 10.1016/j.jtct.2026.05.010 | Ki-67 and CD19 CAR-T outcome, n=79 R/R B-NHL (single centre) | human, clinical | "high tumor Ki-67 (>60%) was associated with lower peak CAR-T cell expansion (P<.01)... and inferior complete response rate, DOR, and PFS (all P<.05)". 3-y DOR 44.9%, PFS 40.2%, OS 48.3%. => high proliferation HURTS CAR-T; slow-cycling tumours are not CAR-T-resistant |
| 42341302 | 10.1056/NEJMoa2518035 | CTL019 10-y (Ruella): FL (indolent, slow-cycling) 10-y lymphoma-free survival 47% vs LBCL 32% | human, clinical | (see section 3); small n (14 FL, 24 LBCL) |
| 37879047, 38194692 | see 3b | FL: ZUMA-5 median PFS 40.2 mo, "very few relapses beyond 2 years"; ELARA 24-mo PFS 57.4% | human | |
| 37774014 | see 3b | CLL (slowly dividing): day +28 MRD-negativity by NGS HR 0.21 for PFS; 6-year PFS 17.8% | human | CLL relapses still occur; CAR-T does not uniformly eradicate |
| 35110735 | 10.1038/s41586-021-04390-6 | CLL, 2 patients in remission >10 years with CAR T cells persisting | human, n=2 | "sustained remission in both patients" |
| 10382741 | 10.1002/(SICI)1521-4141(199906)29:06<1793::AID-IMMU1793>3.0.CO;2-3 | CTL-mediated apoptosis of synchronised fibroblast targets | in vitro (mouse CTL clone F5, LDb fibroblasts) | "apoptosis occurred with similar morphology during G1, S/G2 and M phase" |
| 11380680 | 10.1046/j.1440-1711.2001.01008.x | Alloreactive CTL, granule exocytosis or Fas, targets arrested by olomoucine | in vitro, mouse | "inhibition of p34cdc2 kinase affects neither the Fas nor the perforin/granzyme pathways... After cell cycle arrest, target cells now showed enhanced 51Cr release... accompanied by increase in cell surface Fas expression" |
| 37585504 | 10.1126/scitranslmed.add1951 | NKG2D-CAR T cells vs senescent (stably cell-cycle-arrested) cells | human cells in vitro; aged mice; nonhuman primates | "CAR T cells targeting human NKG2DLs selectively and effectively diminish human cells undergoing senescence... delete naturally occurring senescent cells in aged nonhuman primates" |
| 38194912 | 10.1016/j.ccell.2023.12.011 | Dormant disseminated tumour cells (breast, mouse) | mouse | "DTCs downregulate MHC-I, this does not preclude recognition by conventional T cells... scarcity... overcome by T cell vaccination, TCR or CAR T cells. Each approach achieves robust DTC elimination" |
| 40762432 | 10.1158/2159-8290.CD-24-1515 | TROP2 CAR-T vs osimertinib drug-tolerant persisters (NSCLC) | cell lines, PDX mice | "a single infusion of TROP2 CAR T cells significantly prolonged relapse-free survival, with evidence of cure" (ADC only modestly delayed) |
| 15536145 | 10.1182/blood-2004-09-3458 | COUNTER-EVIDENCE: dormant AML cells (DA1-3b) resist CTL via B7-H1 | mouse | "dormant tumor cells resist CTL-mediated killing because they overexpress B7-H1" |
| 42481500 | 10.1038/s41467-026-75883-z | COUNTER-EVIDENCE: quiescent PDAC cells increase after CAR-T, EREG-driven suppression | mouse | "rare quiescent PDAC cells that increase after CAR-T cell therapy" |
| 41895257 | 10.1016/j.devcel.2026.02.020 | Quiescent persister CRC cells, EpCAM CAR-T | mouse | "EpCAM-targeted human CAR-T cells deficient in CD96... robustly target PTCs" |

### 6. CAR-T AND MHC/HLA LOSS

Direct human trial data stratified by B2M/HLA-I status: NOT FOUND (searched PubMed with HLA/B2M/MHC x CAR x lymphoma/leukaemia; the Sworder 2023 Cancer Cell paper, PMID 36584673, whose full text was checked, lists PAX5, IRF8, CD274 (PD-L1) and TMEM30A as resistance genes and has no B2M/HLA/MHC mention in the extracted text). Indirect:

| PMID | DOI | Evidence | Quote |
|---|---|---|---|
| 28507804 | 10.1080/2162402X.2017.1295202 | HLA expression in B-cell lymphomas (IHC; n=137 DLBCL, 39 PCNSL, 19 testicular) | "Considering HLA class I, HLA class II and HLA-DM together, ... 62% of DLBCL, 77% of PCNSL and 87% of testicular lymphoma cases had abnormal HLA expression patterns." |
| 35538064 | 10.1038/s41467-022-30050-y | WGS of 51 CNS lymphomas | "PCNSLs exhibit significantly more focal deletions of HLA-D (6p21) locus as a potential mechanism of immune evasion" |
| 34065471 | 10.3390/cancers13102503 | Review | "CARs endow an autologous T-cell population with MHC-unrestricted effectivity against tumor target antigens such as the pan B-cell marker CD19" (design statement) |
| (outcomes) | 36260735, 41948499, 42746886 | CAR-T CR in PCNSL 52-57% pooled, in tumours where 77% have abnormal HLA | indirect: high CR despite common HLA aberration. Inference only; no per-patient HLA status |
| 34860572 | 10.1200/JCO.21.02143 | TP53-altered LBCL: 1-y OS 44% vs 76% (n=153); TP53 alterations tied to dysregulated interferon and death-receptor signalling and reduced CD8 infiltration | tumour-intrinsic non-antigen resistance is real; MHC not shown to be one |

### 7. T-LINEAGE CAR-T (CD7, CD5) incl. CNS

| PMID | DOI | Study | n | Numbers (quoted) |
|---|---|---|---|---|
| 37740926 | 10.1002/ajh.27094 | NS7CAR (naturally selected CD7 CAR), AJH 2023 | 60 (35 T-ALL, 25 T-LBL) | "On day 28, 94.4% achieved deep CR in bone marrow. Among 32 patients with extramedullary disease, 78.1% showed response (56.3% CR, 21.9% PR). 2-year OS 63.5% and PFS 53.7%. PFS 1-year 67.2% in 37 CR patients with consolidation transplant vs 15.0% in 10 without; of 10 CR patients without transplants, eight relapsed. CRS 91.7% (grade 3/4 11.7%); neurotoxicity 5%." |
| 35500125 | 10.1182/blood.2021014498 | NS7CAR first-in-human | 20 | "19 achieved MRD-negative CR in BM by day 28, and 5 of 9 patients achieved extramedullary CR... 14 patients allo-HSCT with no relapses to date. Neurotoxicity: 2 grade 1" |
| 34324392 | 10.1200/JCO.21.00389 | Donor-derived CD7 CAR, JCO 2021 | 20 | "90% achieved CR... neurotoxicity grade 1-2 in 15% (n=3)... At median follow-up 6.3 mo, 15 remained in remission. CAR T cells still detectable in 5/5 at month 6" |
| 38657244 | 10.1056/NEJMoa2313812 | Sequential CD7 CAR + haplo-HSCT, NEJM 2024 | 10 | "all 10 CR... Six remained MRD-negative CR, 2 relapsed with CD7-negative leukaemia, 1 died... 1-year OS 68%, DFS 54%" |
| 41363805 | 10.1056/NEJMoa2505478 | Base-edited CAR7, NEJM 2026 | 11 | "7 of 11 (64%) in ongoing remission at 3 to 36 months after transplantation, and leukemia with loss of CD7 expression was documented in 2 patients" |
| 42418709 | 10.1158/2643-3230.BCD-25-0489 | Antigen-negative relapse mechanisms after CD7 CAR, 2026 | 10 paired specimens | "CD7 truncating mutation in 2 of 10; promoter hypermethylation in 7 of 10 without mutation; both in 1 of 10" => antigen loss in all 10 relapsed specimens analysed (a selected relapse cohort, not an incidence) |
| 42810712 | 10.1016/j.jtct.2026.09.036 | Recyclable CD7 CAR, 2026 | 14 | "Peak CAR copies 62,389.69/ug DNA... median day 12... ICANS 2 (14.3%; grade 2 and 3)... objective response for extramedullary disease 78.6%... lineage switch relapse in two patients with ETP immunophenotype" |
| 39354195 | 10.1038/s41591-024-03282-2 | Allogeneic CD5 CAR, Nat Med 2025 | 19 enrolled/16 infused, mostly post-CD7 failure | "100% CR/CRi by day 30... Of 12 untransplanted patients: 2 in remission, 3 relapsed, 5 died of infection and 2 of thrombotic microangiopathy"; "relapse with CD7 loss is common" |
| 38145560 | 10.1182/blood.2023022204 | Autologous CD5.CAR in mature TCL | 9 treated | "ORR 44% (CR in 2)... no grade >=3 CRS or neurologic events" |
| 33410096 | 10.1007/s12015-020-10092-9 | CD5-IL15/IL15sushi CAR in T-LBL with CNS infiltration | 1 | "rapidly ablate the CNS lymphoblasts within a few weeks, resulting in remission" (case) |
| 33234511 | 10.1158/1078-0432.CCR-20-1271 | GC027 CD7 allogeneic CAR (T-ALL), 2 case reports | 2 | "rapid eradication of CD7+ T lymphoblasts in the peripheral blood, bone marrow, and cerebrospinal fluid. Both patients achieved CR with no detectable MRD; 1 of 2 in ongoing remission >1 year" |
| 40777017 | 10.3389/fimmu.2025.1570214 | Sequential CD30/CD7 CAR-T for primary cerebellar ALK-negative ALCL | 1 | "15-month follow-up revealed no evidence of tumor recurrence... grade 2 CRS" |
| 42638216 | 10.1002/ajh.70482 | Naturally selected CD7 CAR-T in T-ALL/LBL with CNS leukaemia (AJH 2026, Letter) | ? | PubMed abstract NOT AVAILABLE (no numbers retrievable) |
| 41290542 | 10.1002/advs.202509259 | Immune dysregulation after CD5 or CD7 CAR | | "5CAR and 7CAR therapies carry the risk of life-threatening infection" |

### 8. CSF-DELIVERED (intrathecal / intraventricular) CAR-T in humans (model assumes CSF-delivered persistence)

Only solid-tumour data found; no lymphoma IT/ICV CAR-T human series found.
| PMID | DOI | Study | n | Numbers (quoted) |
|---|---|---|---|---|
| 38480922 | 10.1038/s41591-024-02893-z | Intrathecal CART-EGFR-IL13Ra2 in recurrent GBM, Nat Med 2024 (FULL TEXT PMC13123313) | 6 | "Peaks of CAR T cells in the CSF were observed between days 1 and 7 and reached an average of 109,235 copies of CAR per microgram gDNA... substantially higher than our prior trials using peripheral blood infusion for GBM (not exceeding 2,000 copies per ug gDNA in blood)... CSF cytokines (IFNg, IL-2, TNFa, IL-6) showed rapid increases before subsiding to baseline within 2 weeks." "administration was associated with early-onset neurotoxicity, most consistent with ICANS, managed with high-dose dexamethasone and anakinra" (all 6 patients, both dose levels); "peak CAR T cell engraftment in CSF was lower in patients at the higher dose level". No objective response by mRANO; tumour shrinkage in all 6 |
| 36259971 | 10.1158/2159-8290.CD-22-0750 | Intraventricular repeated B7-H3 CAR-T, DIPG, Cancer Discov 2023 (FULL TEXT) | 3 evaluable (40 infusions) | "We detected circulating EGFRt+ CAR T cells in the CSF of two of three evaluable patients... Peak detection in S008 at course 1 week 3 after infusion, 64% of detectable lymphocytes in the CSF were B7-H3 CARs... CAR T cells persisted in S008 through course 9, after which only preinfusion biospecimens were collected and we did not detect CAR T-cell DNA (via qPCR) in the peripheral blood of any" patient. (Repeated dosing was needed to sustain CSF presence) |
| 35130560 | 10.1038/s41586-022-04489-4 | GD2-CAR, DIPG/DMG, IV then ICV, Nature 2022 | 4 | "Pro-inflammatory cytokine levels were increased in plasma and CSF; on-target off-tumour toxicity not observed; 3 of 4 clinical and radiographic improvement" |
| 31712432 | 10.1073/pnas.1903854116 | MOUSE (immunodeficient, PCNSL xenograft, 2-photon) | mouse | "Intravenous injection resulted in poor tumor infiltration of anti-CD19 CAR T cells and could not sufficiently control tumor growth. After intracerebral injection, CAR T cells invaded deeply... remained detectable intracranially and intravascularly for up to 159 d." (counter-evidence for IV parenchymal access; not human) |

### 9. NHP / autopsy evidence that CAR-T enter parenchyma
| PMID | DOI | Evidence |
|---|---|---|
| 29025771 | 10.1158/2159-8290.CD-17-0698 | Human autopsy (fatal CD19 CAR neurotoxicity day 13): "T cells constituted 56.9% of CD45+ cells (pons) and most of the T cells in the brain were CAR-T cells, with 93% of the T cells in the pons expressing the EGFRt transduction marker" |
| 34496024 | 10.1182/bloodadvances.2021004889 | Human, fatal late encephalitis month 9 after axi-cel: "CAR T-cell brain infiltration was observed on autopsy" |
| 30060228 | 10.1093/jnen/nly064 | CONFLICTING human autopsy (ALL, fatal cerebral oedema): "within the brain parenchyma, we identified only infrequent T cells and did not identify ALL cells or CAR T cells" |
| 29563103 | 10.1158/2159-8290.CD-17-1368 | Rhesus macaque, CD20 CAR T: "CD20 CAR T cells expand to 272 to 4,450 cells/uL after 7 to 8 days... During neurotoxicity, both CD20 CAR and non-CAR T cells accumulate in the CSF and in the brain parenchyma" |
| 40663771 | 10.1182/blood.2025028964 | Human, TIAN postmortem lesion: "dense macrophage population with central necrosis and peripheral reactive gliosis" (CAR-T cells in lesion not reported in abstract) |

### 10. ICANS / neurotoxicity benchmark table (human, grade >=3 unless stated)

| Population | any-grade neurotox | grade >=3 | source |
|---|---|---|---|
| Systemic LBCL, axi-cel (ZUMA-1, n=101) | not in abstract | 28% | 29226797 |
| Systemic LBCL, tisa-cel (JULIET, n=93) | not in abstract | 12% | 30501490 |
| Systemic LBCL, liso-cel (TRANSCEND, n=269) | 30% | 10% | 32888407 |
| First-line high-risk LBCL axi-cel (ZUMA-12, n=40) | not in abstract | 23% | 35314842 |
| Paediatric/YA ALL tisa-cel (ELIANA, n=75) | 40% | not in abstract | 29385370 |
| Paediatric ALL, CNS-negative / CNS-positive (CHOP, n=129/66) | 41% / 58% | gr3 9% / 9%; gr4 2% / 3% (p=0.20) | 34560014 |
| Adult B-ALL brexu-cel, CNS vs non-CNS | not in abstract | 35.5% vs 30% | 40334068 |
| PCNSL (meta, 30 pts) | 53% | 18% | 36260735 |
| SCNSL (meta, 98 pts) | 48% | 26% | 36260735 |
| CNSL pooled (38 studies) | 44.9% [36-54] | 17.4% [12-23] | 41948499 |
| PCNSL pooled (15 studies, 194 pts) | 46% | 16% | 42746886 |
| CNSL, EBMT n=100 | 42% | 17/100 (17%); 2 deaths from neurotoxicity | 40400509 |
| SCNSL multicentre n=61 | 57% | 44% | 37946255 |
| French LOC, isolated CNS relapse n=48 | 65% | 23% (11/48); median duration of grade 3-4 neurological impairment 100 d (4 d-18 mo); onset median day 5 | 40146949 |
| PCNSL tisa-cel trial n=12 | 41.6% low-grade | 1/12 (8%) | 35167655 |
| TIAN (tumour-local) in CNSL n=56 | 17.9% (10/56), onset median 3.5 d; 1 fatal | | 40663771 |
| Intrathecal EGFR/IL13Ra2 CAR (GBM, n=6) | 6/6 "early and moderate-severe neurotoxicity with elements of both ICANS and TIAN" | | 38480922 (full text) |
| T-ALL CD7 NS7CAR (n=60) | 5% neurotoxicity | | 37740926 |

Risk modifiers (human): high pre-treatment disease burden (Santomasso: "association of severe neurotoxicity with high pretreatment disease burden, higher peak CAR T-cell expansion"; Gust: "high CD19+ cells in bone marrow, high CAR-T cell dose, CRS, preexisting neurologic comorbidities"; Rankin: CNS+high-marrow-burden EFS 14.3% vs 63.6% low burden); ECOG 2-3 HR 2.68 for ICANS (EBMT); age >=65 and MoCA <26 for grade 3-4 neurotoxicity (French LOC); tumour volume >3.4 cm3 for TIAN; leptomeningeal involvement for ICANS (SCNSL study). Mechanism: Gust 2017 -- BBB disruption with endothelial activation, systemic cytokines (IFNg, IL-6) enter CSF; Santomasso 2018 -- CSF IL6/IL8/MCP1/IP10 disproportionately high, "CAR T-cell quantity in CSF" not associated with severity (p=0.404); Ann Neurol 2019 (31074527, 43 paediatric ALL pts): "Neurotoxicity occurred in 19 of 43 (44%)... 9 (21%) grade 3 or 4... correlated with ... higher peak CAR-T cell numbers in blood, but not CSF... astrocyte injury".

---------------------------------------------------------------------

# MODEL INPUTS (defensible transfers)

Grade key (the user's): MEASURED = the exact quantity measured in humans; DERIVED = arithmetic on measured human numbers (assumptions stated); TRANSFER = human value applied to dog, with written basis; OUTCOME = calibrated to clinical outcomes, not a mechanism measurement; ASSUMED = no basis. EVERYTHING below is human data, so as applied to the canine model the best possible grade is TRANSFER (never MEASURED in dogs). Items are reported at the strength shown. None of this is demonstrated in dogs (user knows).

## (a) CNS access fraction of IV CAR-T relative to blood

Two different quantities; the old assumption of 0.5 conflates them.

1. Concentration ratio CSF:blood (what "access" means if kill is proportional to local effector density).
   - Measured pieces: CSF CAR-T "peak" 0.19/uL in non-responders and 0.50/uL in responders (median, first month; PMID 37345469, n=16 CSF-tested; mostly tisa-cel, 19 of 21); day-30 median 0.17/uL (= 19% of CD3+ T cells, range 4-45%). Blood peak comparators: 16.14 cells/uL (axi-cel real-world n=21, PMID 34100900); 12.08 (non-responders) / 35.27 (relapsers) / 65.76 (ongoing responders) cells/uL (ZUMA-1, PMID 36821768); 18/uL vs 98/uL (NCI, PMID 33021872).
   - DERIVED peak-to-peak ratio: 0.19/65.76 = 0.003 to 0.50/12.08 = 0.041; using the axi-cel real-world median 0.19/16.14 = 0.012 and 0.50/16.14 = 0.031. => CSF:blood absolute CAR-T concentration approx 0.003-0.04, central ~0.01-0.03.
   - Weaknesses: different products (CSF cohort tisa-cel, whose blood peaks are lower than axi-cel's, so the true ratio is probably higher); peaks not simultaneous (authors: "interpreted with caution due to far apart time points"); CSF is not parenchyma; CSF sampled every 2 weeks then monthly; Gust 2017 values during neurotoxicity were roughly 4-15-fold higher (2.1-2.6 cells/uL, BBB leak) so ratio depends on BBB state; normal CSF holds <5 WBC/uL by clinical definition (CNS-2/CNS-3 definitions in PMID 40334068), so a CSF with 0.17 CAR cells/uL is ~19% of a very small T-cell pool.
   - Enrichment: CAR-T are 19% of CSF CD3 at D30 and "comprised a higher fraction of the CD4+ T cell subset in CSF compared to blood" (Gust) => CAR-T enter CSF at least as well as endogenous T cells (per-cell trafficking is not impaired), and CSF presence is near-universal: 19/21 (95%) qPCR-positive (Santomasso), 16/16 flow-positive (PMID 37345469).
   - Route comparison: intrathecal CAR (GBM) reached 109,235 CAR copies/ug gDNA in CSF vs <=2,000 copies/ug in blood for the same group's IV trials (cross-trial, DNA-normalised, solid tumour; PMID 38480922) => ~50x; ICV B7-H3 CAR in DIPG: no CAR DNA in blood in any patient (PMID 36259971). So IT/ICV access relative to blood is >1 (compartmentalised), the opposite of IV.
2. Effective (outcome-level) access = ratio of kill achieved in the CNS to kill achieved systemically.
   - CR in CNS lymphoma (PCNSL 56%, SCNSL 47%, PMID 36260735; pooled CNSL 52%, PMID 41948499; PCNSL 57%, PMID 42746886) vs CR in systemic LBCL (JULIET 40%, ZUMA-1 54%, TRANSCEND 53%) => ratio about 0.9-1.4 (central ~1). "CNS response reflects systemic response" (PMID 35351785). CNS ALL CR 97% vs 94% (PMID 34560014).
   - Durability is lower: CNSL 24-month PFS 28%, relapse incidence 59% (EBMT, n=100, PMID 40400509); SCNSL 12-month PFS 16% (PMID 37946255); median CNS-PFS 4 months (n=60, PMID 41530773); vs systemic LBCL 60-month PFS 28% (JULIET). CNSL reaches at 2 years the PFS that systemic LBCL reaches at 5 years. Leptomeningeal disease predicts recurrence after CR; peripheral CD19+ B-cell aplasia (a marker of CAR-T persisting) at progression in 93% => CNS failures are mostly NOT lack of CAR-T persistence.
   - Proposed value: effective CNS kill multiplier (IV route) = 0.5, range 0.1-1.0. Grade: OUTCOME (kill) / DERIVED. As applied to dog: TRANSFER. This matches the old ASSUMED 0.5 in value but is now justified by clinical CR parity (~1) discounted for durability (~0.5). Do NOT describe it as a concentration ratio; the measured concentration ratio is 0.003-0.04, and the human CR data show the CNS is cleared at that low density, probably because tumour burden is small there, CAR-T expand locally on antigen (CSF "initial phase of rapid expansion followed by slow decrease"), and CD19/CD20-driven kill is catalytic. If the model forces kill proportional to density, run a stress case at 0.01-0.05 and expect failure.
   - Parenchymal vs CSF: parenchymal penetration is supported by imaging-defined CR of parenchymal PCNSL and autopsy CAR-T in pons (Gust, 93% of T cells EGFRt+; month-9 encephalitis with CAR-T infiltrate), contradicted by one autopsy with none (PMID 30060228); mouse IV CAR-T poorly infiltrates PCNSL xenograft (PMID 31712432). Human parenchymal CAR-T density: NOT MEASURED. Leptomeningeal vs parenchymal: leptomeningeal involvement associated with recurrence after CR (PMID 41530773), consistent with weaker control in some CNS sub-compartments.
   - Counter-evidence that matters for closure: thiotepa-ASCT beats CAR-T in SCNSL after propensity matching (PFS HR 0.45, OS HR 0.41, PMID 41490516) and in Beijing GoBroad Hospital single-centre cohorts of R/R CNSL in CR (3-y PFS 80% vs 64.8%, PMID 41874671; relapse sHR 0.236 favouring ASCT, PMID 42468825). CAR-T alone is not best-in-class for the CNS.

## (b) Durable fraction / plateau (human)

| Setting | durable fraction (exact) | plateau evidence | source |
|---|---|---|---|
| Systemic LBCL, all infused | ZUMA-1 31% ongoing response at 63.1 mo; 5-y OS 42.6%; 5-y disease-specific survival 51.0%; JULIET 5-y PFS 28%, OS 32%; ZUMA-7 4-y PFS 41.8%; CTL019 10-y lymphoma-free survival 32% (95% CI 14-51; n=24) | ZUMA-1: 5-y OS 92.3% if no EFS event by 24 months; JULIET 61% of responders relapse-free at 60 mo | 36821768, 41252666, 37272527, 42341302 |
| LBCL, patients who reached CR | ZUMA-1 5-y OS 64.4% | | 36821768 |
| Follicular lymphoma | CTL019 10-y LFS 47% (14-pt cohort); ELARA 24-mo PFS 57.4%; ZUMA-5 median PFS 40.2 mo | "very few relapses beyond 2 years" (ZUMA-5) | 42341302, 38194692, 37879047 |
| B-ALL paediatric/YA | ELIANA 5-y RFS in responders 47.3-51.0%, 5-y OS 55.0-62.4% | "most events occur within the first 2 years" | 42525896, 36399695 |
| CLL | 6-y PFS 17.8%; 6-y DOR 26.4% (n=47); Cappell >3-y DOR 51% overall, 50% in CLL | | 37774014, 33021872 |
| CNS lymphoma (CAR-T alone) | EBMT 24-mo PFS 28% (RI 59%); LOC 1-y PFS 43% "with a plateau afterward", 1-y RFS 79% if CR/PR at infusion; pooled relapse after remission 38-45%; pooled 12-mo PFS 42% | plateau only 1 year long, follow-up median 12-21 mo | 40400509, 38586986, 35796863, 38328579, 42746886 |
| CNS lymphoma, ASCT + CAR-T | 2-y PFS 65.5% (n~29) vs 30.0% CAR-T alone vs 23.5% chemoimmunotherapy | retrospective, one centre | 39397022 |
| CNS ALL | 2-y RFS 60% (CNS+) = 60% (CNS-); 2-y OS 83% vs 71% | | 34560014 |
| T-ALL/LBL CD7 without consolidation | 1-y PFS 15.0% without transplant (8 of 10 CR patients relapsed) vs 67.2% with transplant | | 37740926 |

- Proposed durable fraction: B-cell, CNS-involved, CAR-T alone: 0.28 at 2 y (range 0.16-0.43); systemic B-cell lymphoma CAR-T alone: 0.30-0.40 long-term (ZUMA-1 31% ongoing, CTL019 32% LFS); with consolidation (ASCT-like) CNS 2-y 0.65 (retrospective). T-lineage with CAR-T alone: ~0.15 at 1 y; needs HSCT. Grade: OUTCOME (human) / TRANSFER (dog).
- Is "2+ years disease-free" a reasonable inference for 10+? In human CAR-T data, yes with caveats: ZUMA-1 5-y OS 92.3% if EFS at 24 mo (n=39); ZUMA-5 "very few relapses beyond 2 years"; ELIANA events mostly in first 2 y; CTL019 10-y series "no relapses had occurred beyond 5.4 years" (n=38; median FU 10.1 y), i.e., relapse hazard collapses after 2-5 y. Caveats: (i) small numbers, (ii) late relapses do occur (3 late isolated CNS relapses in LBCL, PMID 37723652; abstract states late relapse is 1/3 to 1/2 of failures with an undefined cut-off), (iii) competing risks: second primary cancer 21% and non-relapse mortality 18% at 10 y (CTL019 series), so 10-y PFS was 17% in LBCL against LFS 32%; any "10-year durability" claim must say whether it is lymphoma-free or overall; (iv) CNS-specific plateau beyond 2 y is NOT FOUND. Grade: MEASURED in systemic human; TRANSFER to CNS/dog.

## (c) Persistence window

- Human CAR-T PK: tisagenlecleucel doubling 0.78 d, initial decline half-life 4.3 d, terminal half-life 220 d (PMID 30848084; ALL, pooled phase II; MEASURED human). Peak at day 10-14, transgene up to 780 days (PMID 28935694, n=103). Blood persistence up to 20 months (ELIANA primary). Beyond year 5: transgene in 5/8 long-term lymphoma responders (7.0-10.1 y); 1.2% of T cells at 9.3 y (PMID 42575986); CLL >10 y in 2 patients (PMID 35110735). CSF: CAR-T present at day 30 in 16/16 tested, 17 months in one responder (PMID 37345469).
- Required window (what durability needs): durable responders clear tumour fast: ctDNA undetectable 1 week after infusion in 70% (23/33) of durable responders (13% (4/31) of progressors), and in all by 3 months (PMID 34133196). CAR-T peak by day 8 (ZUMA-12) to 14. Most failures occur within the first 12 months (ZUMA-1: 32 of 45 progression deaths in year 1; ELIANA "most events within first 2 years"). Long-term CAR-T activity was not required for durable response in ZUMA-1: 21/23 (91%) of ongoing responders at 3 y had polyclonal B-cell recovery; but CTL019 series: 44% of long-term responders had persisting B-cell aplasia; CLL series: longer persistence HR 0.56 for PFS. => DERIVED window: functional CAR-T for >= 28-90 days to reach clearance in responders, with 6-12 months as a margin for the minority needing sustained control. Grade: DERIVED (human), TRANSFER (dog).
- The canine measured persistence (14-50 d, repo status; PMID 32002286, 35898541, murine scFv antibodies) is shorter than the human terminal half-life (220 d) by 4-15x, but is of the same order as the human time to clearance in durable responders (7-28 d to ctDNA-negative). So human data say 14-50 d might clear early disease with a small burden but leaves no margin for slow-clearing compartments (CNS, persisters) -- this is a statement about margin, not proof.
- CSF-delivered CAR-T persistence (human, solid tumours only): CSF peak days 1-7, cytokines baseline within 2 weeks, CAR-T in CSF persisted through 9 repeated courses in 1 DIPG patient but undetectable in 1 of 3 (PMID 38480922, 36259971). So a single IT dose gives a weeks-long window, not months, absent target-driven expansion. Lymphoma IT/ICV CAR-T human data: NOT FOUND. Proposed: CSF-delivered persistence = 14 d (range 7-28 d) for one dose, TRANSFER from glioma/DIPG (non-B-cell target, which expands less than CD19/CD20 on a B-cell/lymphoma target in IV experience); do not assume months.

## (d) ICANS budget (use the benchmark table in section 10)

- CNS_LOCAL axis (tumour-local neuroinflammation, on-target in the CNS lesion = TIAN): incidence 17.9% (10/56) in CNSL; onset median day 3.5; fatal in 1 (1.8%); scales with CNS tumour volume (threshold >3.4 cm3: sensitivity 87.5%, specificity 80.5%, AUC 0.847); associated with better response (ORR 90% vs 52%; PFS HR 0.22); MRI pseudoprogression in 27% (7/26), transient CSF IL-10 rise in 24% (7/29) (PMID 40146949). Proposed: CNS_LOCAL grade>=3-equivalent burden 0.18 (range 0.10-0.30) with volume dependence (early detection reduces it); fatal fraction 0.02-0.04. IT delivery: 6/6 moderate-severe neurotoxicity with ICANS+TIAN features at 1x10^7-2.5x10^7 cells (PMID 38480922), i.e., IT route concentrates this axis -- do not give IT CAR-T the IV budget.
- Immune-mediated (ICANS, systemic cytokine/endothelial) axis: any grade 42-53% (CNSL) vs 30-41% (systemic/CNS-negative); grade>=3 17% (pooled CNSL, EBMT 17/100, meta 17.4%, PCNSL 16-18%), up to 26% (SCNSL meta) and 44% (SCNSL n=61); systemic LBCL 10-28%; CNS vs non-CNS ALL grade>=3 equal (35.5% vs 30%; 9% vs 9%; PMID 34560014 shows "no increased risk" in children). Proposed immune-mediated grade>=3 burden: 0.17 (range 0.10-0.26); mortality from neurotoxicity 2% (EBMT 2/100) in CNSL. Sequelae: median duration of grade 3-4 impairment 100 d (up to 18 mo; PMID 40146949).
- Early detection: neurotoxicity risk rises with disease burden (Santomasso; Gust; Rankin CNS-HD vs LD; TIAN volume), so assuming early detection (low burden) the CNS_LOCAL and ICANS budgets should be set at the lower end of the ranges (0.10 and 0.10-0.12). Grade: MEASURED in humans for incidence; the burden-dependence is MEASURED qualitatively (associations), not as a dose-response function. As applied to dog: TRANSFER, with canine ICANS epidemiology NOT FOUND (not searched).

## (e) Failure mode split: antigen loss vs other

| Setting | antigen-loss share of failures | other mechanisms | source |
|---|---|---|---|
| LBCL after axi-cel (paired biopsies) | 5/18 (28%) CD19-low/negative at relapse (text: "~30%") | CD19+ relapses (~70%): suboptimal expansion relative to tumour burden, exhaustion, TME | 34041526 |
| LBCL progressing after CAR19 | 10/16 (62.5%) had absent or low CD19 | | 34312556 |
| B-ALL, all CD19 CAR-T studies (review) | CD19-negative relapse in 30% of relapses (22.5% blinatumomab); 8.7% of all treated | rest CD19+: persistence loss etc | 37526512 |
| B-ALL CD19+CD22 co-administered | of 41 classified relapses: 24 (59%) CD19+/CD22+, 16 (39%) CD19-/CD22+, 1 (2.4%) CD19-/CD22- | | 36346962 |
| B-ALL CARPALL cotransduced CD19/22 | 0 antigen-negative relapses; 5/10 responders had MRD/relapse with CD19+CD22+ disease "associated with loss of CAR T-cell persistence" | | 37647647 |
| B-ALL/LBCL after CD19/22 bispecific | relapses CD19-/lo in 50% (5/10) B-ALL, 29% (4/14) LBCL; none CD22-lo | | 34312556 |
| B-ALL after AUTO3 | "Relapses were probably due to limited long-term AUTO3 persistence" | | 34642489 |
| CD7 CAR-T, T-ALL | CD7-loss at relapse in 10/10 analysed specimens (mutation 2, methylation 7, both 1); NEJM 2024: 2 relapses both CD7-negative; BE-CAR7: CD7 loss in 2 of 4 failures | lineage switch (ETP, 2/14) | 42418709, 38657244, 41363805, 42810712 |
| CNSL | CD20 loss confirmed in 1 of 3 progressions (n=7); case report of isolated CD19-negative CNS recurrence (PMID 35713946); 93% of progressions had peripheral B-cell aplasia (CAR-T alive) | local/leptomeningeal escape, peripheral contrast enhancement (HR 2.75), leptomeningeal disease (HR 2.72) | 35152726, 41530773 |
| LBCL tumour-intrinsic non-antigen | TP53-altered 1-y OS 44% vs 76% (n=153); IFN signalling/MDSC; PAX5, IRF8, CD274, TMEM30A; apoptosis-resistance cross-resistance to CD20/CD22 CAR (preclinical) | | 34860572, 33512407, 36584673, 40578903 |

- Proposed: antigen loss accounts for 0.30 of CAR-T failures in B-cell disease (range 0.28-0.63), the remainder (0.37-0.72) from exhaustion/limited expansion/persistence/TME/apoptosis resistance. In T-lineage CAR-T antigen loss is the dominant escape (>=0.5). For CNS lymphoma no antigen-loss fraction is measured (1 of 3 progressions in n=7; CD19-negative CNS relapse reported as a case); use 0.3 TRANSFER from systemic LBCL, flagged. Grade: MEASURED (LBCL, small paired n=18) / DERIVED (ranges) ; TRANSFER (CNS, dog).
- Dual-target benefit: human evidence shows relapses with single-antigen loss still occur on dual CAR (CD19-/CD22+ in 39% of classified relapses) unless both arms persist; both-antigen loss was rare (1/41, 2.4%). Benefit on durability not shown in a randomised comparison; cross-trial: TanCAR7 (CD19/CD20) 5-y: 40% still in remission, median PFS 33 mo, 5-y OS 60.1% (n=87) vs single-target 5-y data (ZUMA-1 31% ongoing; JULIET 5-y PFS 28%) -- non-randomised, different populations and centres. CD22 CAR-T after CD19 failure: ORR 68%, CR 53% (n=38; Lancet 2024), CD22 CAR in ALL: CR 73% (11/15), median remission 6 months, relapse via CD22-site-density loss (PMID 29155426): second-antigen CARs themselves lose by antigen density. Grade: DERIVED/OUTCOME, weak.

## (f) Other inputs asked in the brief

- Quiescent/slow-cycling cells: CAR-T kill is not division-gated (in vitro: kills in G1, S/G2, M and in CDK-arrested cells; senescent cells killed in human cell cultures, mice, NHP). So duty factor f = 1 for CAR-T on the antigen-positive persister pool IS a TRANSFER (mechanism, non-lymphoma, non-human-patient), supported indirectly by human outcomes in slow-cycling disease (FL 10-y LFS 47% > LBCL 32%; high Ki-67 worse: PMID 42134593) -- but also by mouse counter-evidence (B7-H1-driven resistance of dormant AML cells; quiescent PDAC cells enriched after CAR-T). Not MEASURED in patients. The CAR kills only if the dormant cell keeps the antigen: no human data on CD19/CD20 expression in dormant lymphoma cells.
- MHC/HLA loss: CAR is MHC-independent by construction (design statement, review PMID 34065471); abnormal HLA is present in 62% of DLBCL and 77% of PCNSL, yet CAR-T CR rates are 50-57%, so MHC loss does not abolish CAR-T activity (indirect; per-patient HLA-status stratified outcomes NOT FOUND). Grade: TRANSFER (mechanism) + indirect OUTCOME.
- Potency (replacing 0.12/day): no directly MEASURED human net tumour kill rate found in the abstracts/full texts reviewed. Human constraints: CAR-T doubling 0.78 d (expansion, not kill), ctDNA undetectable at day 7 in 70% of durable responders (clearance of >=2-3 logs in <=7 d is needed in them, but no baseline concentration is given, so a rate cannot be computed without assumption), CR at day 28 in 94-97% of ALL (Leahy), PET-CR 40-58% in LBCL at ~1-3 months. Intrathecal GBM CAR: MRI enhancement reduction in 24-48 h in all 6 patients (could include inflammatory change). Verdict: 0.12/day remains ASSUMED (not contradicted; the human data say clearance in durable responders is faster than 0.12/day at the bulk level but give no rate). Do not relabel it TRANSFER.

---------------------------------------------------------------------

# WHAT I SEARCHED AND DID NOT FIND

Searched (PubMed via MCP search/metadata and NCBI E-utilities esearch/efetch, PMC full text via efetch): CAR-T x PCNSL/SCNSL/CNSL/CNS leukaemia/ALL CNS-2/3; CSF CAR-T counts/ratio/copies/ddPCR/IL-6/autopsy/parenchyma/NHP; long-term persistence/10-year/5-year/late relapse; CD19-negative/antigen-loss relapse, CD19/CD20/CD22 dual/tandem trials; quiescent/dormant/senescent/persister/cell-cycle x CAR/CTL; HLA/B2M/MHC x CAR x lymphoma/PCNSL; CD7/CD5 CAR-T and CNS; intrathecal/intraventricular CAR-T; ctDNA/MRD kinetics; PK/PD models; Ki-67.

NOT FOUND (do not cite as found):
1. Simultaneous paired CSF vs blood CAR-T absolute concentrations in malignancy patients with a published CSF:blood ratio in cells/uL. Only: CSF-only absolute counts (PMID 37345469), per-DNA copies in one case (Hu 2016, PMID 27526682: CSF 3,032,265 vs blood 988,747 copies/ug DNA = 3.07, cerebral CRS), CD4/CD8 fraction comparisons (Gust). The ratio in (a) is DERIVED across studies.
2. Human parenchymal CAR-T density (imaging or biopsy) in lymphoma; autopsy evidence is two for, one against (PMIDs 29025771, 34496024 vs 30060228); only toxicity cases.
3. CSF MRD-negativity rate after CAR-T in CNS lymphoma (flow-negative CSF rates). Only imaging CR; for CNS ALL: 97% CR (CHOP), 87.5% CNS-1 (brexu-cel), 8/10 isolated-CNS cleared (Rankin), 100% flow-negative CSF in 3 children.
4. CNS-lymphoma CAR-T 5-year or longer follow-up; the longest medians are 12-21 months (a 3-y PFS exists only in a small single-centre consolidation comparison, PMID 41874671). Direct CNS-specific plateau fraction: NOT FOUND.
5. Population-level incidence of CNS relapse after CAR-T in systemic LBCL without baseline CNS disease (only case series; PMID 37723652).
6. Direct human evidence that CAR-T eliminates quiescent (G0) tumour cells; direct measurement of CD19/CD20 on dormant lymphoma cells.
7. Human outcome data stratified by B2M/HLA-I status after CAR-T.
8. Measured human net tumour kill rate per day after CAR-T.
9. Intrathecal/intraventricular CAR-T in human lymphoma/leukaemia (only solid tumours). One IT CD19 CAR-T-after-IT-chemo in adult ALL CNS leukaemia paper exists (PMID 30846865) but was not read.
10. Numbers for the CD7 CAR-T in T-ALL/LBL with CNS leukaemia letter (PMID 42638216): PubMed abstract unavailable.
11. Canine-specific CAR-T data were deliberately not searched (user knows it is unmet; repo already records canine persistence of 14-50 d).
12. Dual-target CAR-T in PCNSL: only small series/case reports (13 pts, 1-y PFS 74.59%, median follow-up 14.2 mo, PMID 34267187; 1 case with 35-month CR, PMID 37321275; cohort retrospective 2-y PFS 65.52% vs 30.00%, PMID 39397022). No trial with 2+ y follow-up.

# KEY CAVEATS (for the closure claim)
- Strength: human outcome data, mostly retrospective/single-arm; CNSL series heavily confounded by bridging chemo/RT/steroids, ASCT, BTKi and PD-1 co-therapy, and by selection (CAR-T eligibility). Mark every CNS number OUTCOME, not mechanism.
- The best CNS-lymphoma comparison (Alderuccio 2026, n=1139) says thiotepa-ASCT outperforms CAR-T after matching: CAR-T alone does not close the CNS sanctuary in humans (2-y PFS 28%, relapse 59%).
- 10-year durability: even in systemic humans, 10-y PFS 17% (LBCL) because of competing second cancers (21%) and NRM (18%); the CNS-specific 10-year plateau is NOT FOUND.
- Canine dog transfer risks: murine scFv immunogenicity (persistence), canine lymphoma proliferation (high Ki-67 correlates with worse human CAR-T results, PMID 42134593), BBB/CSF physiology, CD19/CD20 expression and antigen-loss rates, ICANS epidemiology unknown.

# VERIFICATION NOTE
Each PMID above was retrieved from PubMed in this session (PubMed MCP get_article_metadata for PMIDs 42814177, 42807827, 41948499, 41701972, 40474366, 40400509, 40146949, 40078990, 36260735, 38586986, 37294963, 34065471, 32888407, 35167655, 39674850, 34492703, 39466477, 36328891, 39898872, 36286546, 41490516, 35314842, 36205806, 40777017, 42638216; the remainder through NCBI E-utilities efetch, the same PubMed records, with DOIs read from the record). Numbers in quotes are from the PubMed abstract unless the row says FULL TEXT (PMC full text read: 37345469, 29025771, 29880584, 36821768, 34041526, 38480922, 36259971, 36584673 grep).
