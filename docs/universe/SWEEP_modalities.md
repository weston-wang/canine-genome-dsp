# Systematic modality sweep (everything except vaccines and stem-cell/transplant): canine multicentric lymphoma

Date: 2026-09-30. Scope: the 13 sweep categories in the brief. Sources: PubMed (title/abstract search, metadata fetched for every
PMID cited below; full text read for two papers only: PMC5915681 RV1001, PMC3278154 adoptive T cells). Every PMID here was returned by a
metadata fetch in this session; DOI is given where the fetch returned one. bioRxiv MCP has no keyword search (one 30-record
scan of "cancer biology", last 90 days, found nothing canine). Not veterinary advice.

## 0. Success criteria, quoted (CLAUDE.md rule 2) and how grades are used

- "make sure every mechanism and every escape is closed by either real data or rigorous model, potency, toxicity etc all need to be considered"
- "looking for 10+ years of durability" ; "assuming early detection"
- "I'm not asking if it's been demonstrated, I know it's not." So "not demonstrated in dogs" is NOT reported below as a finding.
- "I'm okay with no specific data but if scientifically sound" : a transferred figure is acceptable if the transfer is justified in
  writing and graded TRANSFER (never MEASURED). A number with no basis stays ASSUMED and does not count as closure.

Grades used here: MEASURED (canine in vitro or canine in vivo measurement of that quantity), DERIVED (IC50 x exposure; none achieved in this
sweep, see section 4), TRANSFER (human or other species, with stated basis), OUTCOME (clinical result, not a kill rate), ASSUMED (no basis).
"Covers escape N" below means covered by pathway position (mechanism argued), not measured kill; the 14 escapes are numbered
1 P-gp, 2 BCRP, 3 TP53/intrinsic-apoptosis evasion, 4 CD20 loss, 5 CD19 loss, 6 BCR/NF-kB independence, 7 PI3K/AKT bypass,
8 drug-tolerant persister (non-dividing), 9 autophagy independence, 10 T-cell exhaustion/immunosuppressive microenvironment,
11 B-lineage identity switch, 12 antigen-presentation loss, 13 MGMT repair, 14 CD7 loss.

## 1. Record check (CLAUDE.md rule 1): what was already covered vs new

Read: `docs/LYMPHOMA_STATUS.md`, `docs/LYMPHOMA_COVERAGE_LEDGER.md` (origin/claude/duplicate-codex-prefix-branch-lt1qh6), grep of docs/src.

| item | status | where |
|---|---|---|
| anti-CD20 antibody (PMID 38662527, 41742528), CD20 CAR-T (32002286), tandem CAR-T (42480604), PD-1/CD28 switch CAR-T (39314237 as catalogue entry), verdinexor (40872651, 30143046), venetoclax (36433867), acalabrutinib (27434128), HCQ+dox dog trial (24991836), valspodar RCT (28357033) | already covered | LYMPHOMA_COVERAGE_LEDGER.md sections 3-5 |
| anti-PD-1/PD-L1 | already covered but as ASSUMED 0.040/day "melanoma transfer"; **new dog lymphoma data contradict it** (section 2.1) | ledger line 128 |
| CD52 antibody | only the non-existent "CD5/CD52-directed cellular effector" is in the catalogue; a CD52 **antibody** is not. STATUS.md line 159 lists "CD52/ADC/bispecific/proteasome/HDAC sweep" as not done | not covered |
| PI3Kd, JAK1, HDACi, proteasome inhibitor, CDK9, CD47, oncolytic virus, adoptive T cells, NK, IL-15, 211At-RIT, plerixafor, ATR/PARP/BET/EZH2/BCL6 | not in catalogue (grep for RV1001, panobinostat, oclacitinib, CD47, flavopiridol, bortezomib, vorinostat, gilvetmab, EZH2, masitinib, plerixafor, VSV, astatine returned nothing) | not covered |
| STATUS.md "T-cell kinase inhibitors and canine IL-15 armouring: nothing found to model" | **partly superseded**: PI3Kd (RV1001) and JAK1 (oclacitinib) are T-cell-relevant kinase inhibitors with dog data; a canine rIL-15 clinical trial exists (40520425). IL-15 *armouring* of CAR-T: still nothing found | STATUS.md line 107 |
| vaccines, transplant | handed to other agents | - |

## 2. Findings that change existing catalogue entries (check these first)

### 2.1 Anti-PD-1: dog lymphoma data exist and are negative
- Gilvetmab (caninized anti-PD-1, Merck Animal Health), multicentre open-label, PMID 42247661 (doi 10.1093/jvimsj/aalag098): 15 dogs with stage III-V
  lymphoma evaluated; **"No objective responses were observed in dogs with lymphoma."** (melanoma ORR 20% n=25; mast cell tumour ORR 46% n=26; 6 mg/kg q28d or 10 mg/kg q14d).
- c4G12 canine chimeric anti-PD-L1, PMID 37792729 (doi 10.1371/journal.pone.0291727): n=12 mixed tumours, includes 1 B-cell lymphoma; the two PRs
  were nasal adenocarcinoma and osteosarcoma (ORR 25%, 2/8 with target disease), so the lymphoma dog did not respond.
- Expression: PD-1/PD-L1 is low-to-negative on canine T-cell lymphoma tumour cells and raised on B-cell lymphoma cells and on tumour-infiltrating lymphocytes (PMID 29380929, doi 10.1111/vco.12386);
  PD-L1 protein/mRNA is detected in canine B-cell lymphoma and is reduced by MEK1/2 inhibitors in one line (28111882).
  Atezolizumab cross-reacts with canine PD-L1 and lymphoma-patient PBMCs respond in vitro (33668625, doi 10.3390/cancers13040785).
- Consequence: ledger value "anti-PD-1 ASSUMED 0.040/day (melanoma transfer)" is contradicted for lymphoma by an OUTCOME-negative (0/15). Re-grade MEASURED-NEGATIVE (clinical, n=15, monotherapy, mixed stages); it does not show PD-1 is irrelevant in combination, but it removes the basis for a transferred potency.
- Other checkpoints (CTLA-4, LAG-3, TIM-3): **no dog lymphoma trial or canine antibody found**. Only CTLA-4 upregulation on CD8 T cells exposed to lymphoma-derived vesicles in vitro (37884996, doi 10.1186/s12935-023-03104-4) and cross-reactivity testing (33668625).

### 2.2 Venetoclax is reported to be a P-gp and BCRP substrate
- PMID 39620327 (clinical pharmacology review): "a substrate for CYP3A4, P-glycoprotein, and breast cancer resistance protein". The ledger makes venetoclax the T-cell single point of failure for the pump escapes (1, 2). If it is a P-gp substrate, the pump lineage may defeat it; the canine T-cell EC50 (0.023 uM, 36433867) was measured on primary cells with whatever basal pump they had.
- Supporting tension: MDR-1 mRNA is detectable in ~80% of untreated canine multicentric lymphomas (n=29) and is highest in CD45-negative T-cell lymphomas (41406705, doi 10.1016/j.vetimm.2025.111048). Intrinsic P-gp activity at diagnosis did not predict outcome in 79 dogs with B-cell lymphoma (36010910, doi 10.3390/cancers14163919), which is about baseline activity, not acquired resistance.
- Not verified here: venetoclax free fraction, whether the ledger's canine EC50 already accounts for pump.

### 2.3 Single-agent oral targeted drugs in dogs all show a 3-4 week time-to-progression
- acalabrutinib ORR 25% (5/20), median PFS 22.5 d (27434128); RV1001 (PI3Kd) ORR 62% and 77%, median TTP 21 and 25.5 d (29689086); verdinexor median response duration 18 d in the record, although phase I responders had TTP 66-83 d (24503695, doi 10.1371/journal.pone.0087585).
- Observation, not explanation: derived kill rates (verdinexor 0.27/day) sit beside clinical durations of weeks for three mechanistically different drugs. This supports treating "kill rate from IC50" as an upper bound for oral single agents and keeps the persister/relapse parameters (f, r, switching) load-bearing. Hypothesis only.

## 3. Sweep by category (canine first, then human transfer)

### 3.1 Antibodies
| target | dog data found | verdict |
|---|---|---|
| **CD52** | Only review statements: caninized anti-CD20 "full" and anti-CD52 "conditional" USDA licence for B- and T-cell lymphoma (PMID 26545847, Vet J 2015, doi 10.1016/j.tvjl.2015.10.008); repeated in a probiotics review (39954194, doi 10.1007/s12602-025-10468-8). **No primary canine CD52 efficacy/PK/safety paper found** (PubMed `CD52 AND dog/dogs/canine` = 8 records: 2 relevant, both reviews; 20580067 bovine and 19238728 rat irrelevant; 4 older records not inspected). Current marketing status not verified. | The one T-lineage antibody in the brief. ASSUMED potency; verify the primary source (USDA summary of basis is not in PubMed) before any use. Mechanism (ADCC/CDC, not cycle-gated, not a pump substrate as a large protein) is argued, not shown. |
| CD20 | in record (38662527 n=42; 41742528 n=13: 13/13 CR, median PFS 340 d, 2-y survival 38.9%) | covered |
| CD22 | mouse mAbs to canine CD22 made; one dog with DLBCL imaged by SPECT-CT; RIT "planned" (32117707, doi 10.3389/fonc.2020.00020) | imaging only; no therapy data |
| CD19 | anti-canine CD19 antibody generated and validated (32081102, doi 10.1177/0300985819900352); rabbit anti-canine CD19 mAb for CAR-T feasibility (41847725) | reagents only; no dog therapy data |
| CD79b, CD25, CD30 ADCs (polatuzumab/brentuximab type) | **none found in dogs.** CD25 only as prognostic marker (36111442, 36635848); CD30 by IHC in one canine ALCL (29455626) | not found; human ADC transfer not verified in this pass |
| **CD47/SIRPa** | Canine CD47/SIRPa axis is conserved; canine-specific high-affinity SIRPa-Fc variants; with anti-CD20 (1E4-cIgGB) **cures in 100% of mice** with canine lymphoma xenografts (27856424, doi 10.1158/2326-6066.CIR-16-0105). No dog trial found. Human: Hu5F9-G4 + rituximab phase 1b, 22 pts, ORR 50% (DLBCL 40%, n=15), 91% of responses ongoing at 6-8 mo (30380386, doi 10.1056/NEJMoa1807315); 46 pts iNHL, ORR 52.2%, median DOR 15.9 mo (39213421, doi 10.1182/bloodadvances.2024013277) | TRANSFER + MEASURED (mouse, canine cells). Candidate (section 5) |
| radioimmunotherapy | dog data are for CD45 (conditioning, not lymphoma therapy): 211At-anti-CD45 in 8 normal dogs (26338894, doi 10.2967/jnumed.115.162388) and 17 dogs (39025648, doi 10.2967/jnumed.124.267540); 131I/90Y/177Lu anti-CD20 or CD37 in dogs: **none found**; 131I-type CD22 RIT: imaging only (above) | hand-off to transplant agent; no anti-lymphoma RIT efficacy in dogs |

### 3.2 T-cell engagers / bispecifics
PubMed `dogs/canine AND (bispecific OR T cell engager OR BiTE)` was dominated by irrelevant hits; a tight `canine AND bispecific AND CD3 AND lymphoma` query returned 0. **No canine CD3xCD20 or CD3xCD19 engager found.** Human bispecific literature was searched but the returned records were not verified, so no human figure is cited. Buildable in principle (canine CD3, CD20 and CD19 reagents exist: 32081102, 38662527).

### 3.3 Cell therapies and cytokines
| modality | dog data | verdict |
|---|---|---|
| **Polyclonal autologous CD8 T-cell add-back after CHOP** (aAPC-expanded, IL-2/IL-21) | 8 dogs infused vs 12 stage- and remission-matched historical controls: median OS 392 vs 167 d (HR 4.3, p=0.03), tumour-free survival 338 vs 71 d (p=0.005); cells persisted up to 49 d, trafficked into tumour lymph node; grade III GI event in 1 dog (22355761, doi 10.1038/srep00249; full text read) | OUTCOME (historical control, B-lineage only). Antigen-independent; relies on MHC-I |
| CAR-T (CD20, tandem, switch receptor) | in record. New: first-in-canine anti-CD20 CAR-T with canine 4-1BB-CD3z "induced CD20-negative lymphoma outgrowth but did not persist or deplete B cells"; human-BBz version superior in xenograft (41376156, doi 10.1016/j.ymthe.2025.12.010). RNA CD20 CAR-T: transient activity in 1 dog (27401141, doi 10.1038/mt.2016.146) | covered; no CAR-T for T-cell lymphoma (CD5/CD7/CD52) found |
| **NK cells (adoptive)** | first-in-dog: autologous/allogeneic PBMC-expanded NK in melanoma and osteosarcoma, no serious AEs (38631708, doi 10.1136/jitc-2023-007963); allogeneic expanded NK, 3 dogs with metastatic solid tumours, safe (42461253, doi 10.1111/vco.70091). **No NK trial in lymphoma found.** Review 30563208 | no lymphoma data |
| allo iNKT | unedited allogeneic iNKT persisted >=78 d in MHC-mismatched dogs (37852175, doi 10.1016/j.xcrm.2023.101241) | persistence precedent only |
| CAR-NK, CAR-macrophage, gamma-delta T, TIL | **none found for dog lymphoma** (gamma-delta T-cell LGL lymphoma case report 25965815 is disease, not therapy) | not found |
| **recombinant canine IL-15 + chemotherapy** | 61 dogs enrolled, 37 completed 12 weeks; ORR 77.8% vs 57.9% (chemo alone); TK-1, LDH, b2-microglobulin lower; AEs mild GI (40520425, doi 10.3389/fvets.2025.1596084) | OUTCOME, weak (attrition 24/61, 12-week horizon, design unclear from abstract) |
| canine IFN-gamma | cutaneous epitheliotropic T-cell lymphoma, 15 treated vs 5 prednisolone: no survival difference, better QoL (37006127, doi 10.1111/vde.13161); in vitro only 1 of 9 lymphoma lines died (32799170, doi 10.1016/j.rvsc.2020.08.007) | weak; no direct kill |
| IL-2 / IL-12 plasmid / suicide gene / in vivo CAR | IL-2 only as vaccine adjuvant (21569195, phase I LMI + IL-2 + GM-CSF, vaccine hand-off). **No IL-12 gene/plasmid, suicide-gene or in vivo CAR lymphoma study found** | not found |

### 3.4 Small molecules
Canine IC50s (all in vitro, canine lymphoma lines unless stated). "Exposure" = dog plasma/tissue concentration found; none of these reached DERIVED (see section 4).

| agent | target | canine in vitro | dog clinical | P-gp (verified source) | CNS | grade |
|---|---|---|---|---|---|---|
| **RV1001 (PI3Kd)** | PI3Kd | ex vivo 1 uM: pAKT inhibited in 5/7 primary samples; no IC50 | Ph I n=21 ORR 62% (3 CR, 10 PR); Ph II n=35 ORR 77% (1 CR, 26 PR); B and T, naive and relapsed; T naive ORR 5/5, T relapsed 5/8; median TTP 21 / 25.5 d; oral F good; Cmax ~6 ug/mL at 15 mg/kg (11.3 ug/mL at 25 mg/kg M-F); DLT hepatotoxicity with trough 20-30 uM (29689086, doi 10.1371/journal.pone.0195357) | not found | related PI3Kd ME-401 detected in mouse brain (31506873); RV1001 not found | OUTCOME (dog); potency not derivable |
| **panobinostat (HDACi)** | class I/II HDAC | CLBL-1 IC50 18.32 nM (free), 12.9 nM (PEG liposome), 10.9 nM (folate liposome); CLBL-1 xenograft growth inhibited with H3 acetylation and apoptosis (29983882, doi 10.18632/oncotarget.25580; 37711439, doi 10.3389/fvets.2023.1236136) | none | **substrate of P-gp and BCRP** in transporter-deficient mice; brain Kp,uu 0.32, spinal cord 0.21 (37827699) | P-gp/BCRP-limited | MEASURED (IC50); exposure not found |
| **vorinostat / OSU-HDAC42** | HDAC | 9 canine lines: SAHA IC50 0.6-4.8 uM, OSU-HDAC42 0.4-1.3 uM; T-cell lymphoma, MCT, OSA, HS lines most sensitive (<5 uM SAHA) (18593248, doi 10.2460/ajvr.69.7.938) | valproate (weak HDACi) + doxorubicin phase I, n=21: tumour and PBMC histone hyperacetylation, no added myelosuppression (20705615, doi 10.1158/1078-0432.CCR-10-1238) | "not a P-glycoprotein substrate" (33079733, vorinostat + fenretinide in T-cell malignancies); CNS delivery not limited by P-gp/BCRP in mice (39893010). Romidepsin IS a P-gp substrate in vitro (38151817, 27564097) | vorinostat reaches CNS in mice | TRANSFER (P-gp, CNS); MEASURED (IC50) |
| **bortezomib / ixazomib** | proteasome | CLBL-1 IC50 bortezomib 15.1 nM, ixazomib 59.14 nM; synergy with doxorubicin, variable with vincristine, **antagonism with 4-hydroperoxycyclophosphamide** (38237918, doi 10.1111/vco.12957). NF-kB p50/p65 constitutively nuclear in GL-1, CLBL-1, CL-1; bortezomib removes it and inhibits proliferation in 5/6 lines (23337362, doi 10.1292/jvms.12-0168). High proteasome-subunit mRNA associated with poor CHOP response (n=15 dogs) (38237918) | none for lymphoma | carfilzomib: ABCB1-mediated resistance in myeloma lines (41923105, 41373605) and a P-gp inhibitor raised intracellular carfilzomib (38969867); bortezomib: P-gp up-regulation cited as a resistance route (38072962, secondary statement) | not found | MEASURED (IC50); exposure not found |
| **flavopiridol (CDK9/CDK4/6)** | CDK | "profound cell death in all 8 lines at 400 nM", apoptosis, loss of Mcl-1 and XIAP, tumour shrinkage in xenografts (25623777, doi 10.1111/vco.12130) | none | not found | not found | MEASURED (in vitro, mouse xenograft) |
| palbociclib / abemaciclib | CDK4/6 | active, but lines with high p16 and low pRb are less sensitive (36450591, doi 10.1292/jvms.22-0498); p16 inactivated in canine T-cell lymphoma (17606508) | none | not found | - | MEASURED (resistance biomarker) |
| **oclacitinib (JAK1)** | JAK1/STAT5 | 5 of 9 lines (cutaneous EO-1 plus 8 high-grade) sensitive; pJAK1/pSTAT5 dependence (41680286, doi 10.1038/s41598-026-40066-9) | CETL retrospective 12 oclacitinib vs 11 CCNU: no significant difference in response, survival or relapse, fewer AEs (42554028, doi 10.1111/vde.70115); separate series of 8: 1/8 improved (40525607, doi 10.1111/vde.13366); Sezary case with dose-dependent response, relapse d63 (41473101). Dog oral bioavailability 89%, Tmax <1 h (24330031) | not found | not found | MEASURED (in vitro); OUTCOME thin and conflicting |
| ibrutinib | BTK | CLBL-1 and GL-1 proliferation inhibited; synergistic with a PI3Kg inhibitor (AS-605240) (34884478, doi 10.3390/ijms222312673; 40351764, doi 10.3389/fvets.2025.1577028) | original ibrutinib paper states objective responses in dogs with B-NHL (20615965, doi 10.1073/pnas.1004594107); **n and ORR not retrievable** (full text empty in PMC fetch) | - | - | OUTCOME unquantified |
| zanubrutinib, idelalisib, duvelisib, lenalidomide, SYK | - | SYK inhibitor entospletinib: no added effect with BET inhibitors (32620617, doi 10.21873/anticanres.14367). Zanubrutinib appears only as a nonclinical safety paper (32484067, species not checked); duvelisib as dog PK (32442869). **No dog lymphoma efficacy data for zanubrutinib, idelalisib, duvelisib or lenalidomide** | none | - | - | not found in dogs |
| **duvelisib (human, PI3Kd/g)** | - | - | human PTCL: PRIMO phase II N=123, ORR 48.0%, CR 33.3%, mPFS 3.4 mo, mDOR 7.9 mo; AITL ORR 62.2% (42018969, doi 10.1200/JCO-25-03120); phase 1, PTCL ORR 50% (n=16), CTCL 32% (n=19) (29191916, doi 10.1182/blood-2017-05-786566); duvelisib + romidepsin real-world ORR 61%, CR 47%, n=38 (40526834, doi 10.1182/bloodadvances.2025016347) | - | - | TRANSFER for T-cell |
| mTOR (rapamycin) | - | **nothing on canine lymphoma therapy found** | - | - | - | not found |
| EZH2 | EZH2 | overexpression suppresses apoptosis and increases colony formation in canine T-cell lymphoma lines (42368342, doi 10.3389/fvets.2026.1823343). **No canine EZH2-inhibitor experiment found** | none | - | - | target evidence only |
| BCL6 | BCL6 | no canine lymphoma experiment; BCL6 PROTAC ARV-393 dog PK only: low clearance, F 64.7% (42187333, doi 10.1002/bmc.70498) | none | - | - | dog PK only |
| MDM2 (TP53-wt) | - | **none found** for canine lymphoma | - | - | - | not found |
| MCL-1 inhibitors | - | **none found** in canine lymphoma; MCL-1 down-regulated by flavopiridol (25623777); human MCL-1 inhibitors are subject to MDR1 efflux (34478517) | - | yes (human myeloma) | - | not found |
| navitoclax / BH3 mimetics | BCL2/BCL-XL | tested on primary canine cells (36433867); beyond venetoclax the EC50 was not extracted | - | venetoclax: substrate (39620327) | - | covered |
| **ATR (berzosertib)** | ATR | cytotoxic in 4 canine lymphoma/leukaemia lines at concentrations harmless to non-cancer canine cells, sensitivity variable; synergy with chlorambucil (39300906, doi 10.1111/vco.13014) | none | - | - | MEASURED; acts in S-phase (not persisters) |
| PARP (olaparib) | PARP | works at tens of uM (12.5-50 uM; 30-40% annexin-positive at 48 h, 50 uM); chemosensitiser for doxorubicin (40616061, doi 10.1186/s12917-025-04880-z; 41728128) | none | - | - | weak potency |
| BET (I-BET151, AZD5153) | BRD2/3/4 | dose- and time-dependent inhibition in CLBL-1 (32620617). MYC gain on CFA13 is the dominant copy-number lesion in 90 canine high-grade nodal lymphomas (42754084, doi 10.1016/j.tvjl.2026.106881) | none | - | - | MEASURED (qualitative) |
| azacitidine / decitabine | DNMT | CLBL-1 IC50-dose regimen lowered promoter methylation; HDACi (valproate best) restored mRNA further; decitabine did **not** arrest xenograft growth (30533020, doi 10.1371/journal.pone.0208709); hypermethylation-silenced tumour suppressors in cDLBCL (35409379, doi 10.3390/ijms23074021) | none | - | - | no anti-tumour effect shown in vivo |
| VCP inhibitors (CB-5083, eeyarestatin) | p97/VCP | preferential kill of canine lymphoma over PBMC, proteotoxic stress, DNA damage (29314493; 26104798, doi 10.1186/s12885-015-1489-1) | none | - | - | MEASURED (in vitro) |
| simvastatin | HMG-CoA | kills canine T-cell lines Ema and UL-1 via autophagy/JNK, not B-cell lines (38340381, doi 10.1016/j.rvsc.2024.105174) | none | - | - | MEASURED (T-cell, in vitro) |
| arsenic trioxide, ferroptosis inducers | - | **none found in canine lymphoma.** A 1,824-compound screen at 5 uM in GL-1, UL-1, CLBL-1 found artesunate, niclosamide, pentamidine, itraconazole, dronedarone with IC50 comparable to or below reported dog Cmax (41044621, doi 10.1186/s12917-025-05053-8); IC50 values not extracted | none | - | - | hypothesis-generating |
| cannabinoids | - | AEA, CBD, WIN-55 212-22 synergise with CHOP components and lomustine in canine B-cell line 1771 (41595541, doi 10.3390/biomedicines14010003) | none | - | - | in vitro only |
| anti-angiogenic (TSP-1 peptide ABT-526) | - | - | randomised placebo-controlled, n=94 first-relapse dogs, ABT-526 + CeeNu vs CeeNu: ORR 23/49 vs 23/37 (NS), median response duration 35 vs 15 d, TTP 41 vs 21 d (p<0.05) (17189419, doi 10.1158/1078-0432.CCR-06-0110) | - | - | OUTCOME (response duration only) |
| toceranib / masitinib / imatinib / celecoxib | KIT/PDGFR/VEGFR ; P-gp modulation | toceranib in multidrug-resistant lymphoma: 2/5 PR (28592719, doi 10.1292/jvms.16-0457); masitinib 10 epitheliotropic dogs: CR 2 (median 85 d), PR 5 (60.5 d) (26364581, doi 10.1111/vco.12157); **masitinib inhibits P-gp at >=1 uM and reverses doxorubicin resistance in canine lymphoid cells** (23363222, doi 10.1111/jvp.12039); imatinib does the same in CLBL1-8.0 (31836165, doi 10.1016/j.tvjl.2019.105398); celecoxib prevents induction of P-gp resistance in canine and mouse lines (32365663, doi 10.3390/cancers12051117) | see left | - | - | alternative P-gp reversers (MEASURED in vitro) |

Canine rescue cytotoxics (real dog numbers; all OUTCOME; none durable; P-gp substrate status **not verified** for any):
| regimen | n | result | source |
|---|---|---|---|
| actinomycin D single agent | 49 | CR 41% (20/49), median disease-free interval 129 d in CR; thrombocytopenia 45% | 18673031, doi 10.2460/javma.233.3.446 |
| dacarbazine single agent (800-1000 mg/m2) | 40 | ORR 35%, median PFI 43 d; thrombocytopenia dose-limiting. (PMID 20391633 carries the same title: duplicate record) | 19709354, doi 10.1111/j.1939-1676.2009.0376.x |
| mitoxantrone 5 mg/m2 + DTIC 600 mg/m2 | 44 | ORR 34%, median duration 97 d; grade 4 neutropenia 18%, sepsis 5% | 30653362, doi 10.5326/JAAHA-MS-6878 |
| temozolomide or DTIC + anthracycline | 63 | response 72% / 71%, duration 40 / 50 d | 17696856, doi 10.2460/javma.231.4.563 |
| MOMP (mechlorethamine, vincristine, melphalan, prednisone) | 88 | ORR 51.1%, median 56 d; OS 183 d; T-cell 55%, B-cell 57% | 23910023, doi 10.1111/vco.12055 |
| DMAC (dexamethasone, melphalan, actinomycin D, cytarabine) | 54 / 86 / 100 | ORR 72% (median remission 61 d); 43% (PFS 24 d); 35% (UK cohort) | 17063713; 24489398; 30666777 (doi 10.1111/vco.12457) |
| oral melphalan single agent | 19 | PR 3, SD 3; TTP 14-103 d | 28941072, doi 10.1111/vco.12356 |
| MOC (melphalan, vincristine, cytarabine) | 26 | ORR 38%, CR 19%, median PFS 29 d | 38175982, doi 10.5326/JAAHA-MS-7372 |
| continuous L-asparaginase (GI large-cell) | 32 | ORR 56% (US), median PFS 50 d, OS 147 d | 34213084, doi 10.1111/vco.12749 |
| lomustine + prednisolone first line | 30 | RR 87%, TTP 42 d, MST 90 d | 38890811, doi 10.1111/vco.12990 |
| lomustine- vs anthracycline-based, mediastinal (95.6% T-cell) | 70 | ORR 97.9%, CR 76.6%, PFS 132 d, OS 223 d, 2-y survival 15.7% | 41914636, doi 10.1111/vco.70062 |
| early CHOP progression | 187 | short first PFI predicts poor response, PFI and survival after rescue (lomustine, LAP, rabacfosadine) | 38961691, doi 10.1111/jvim.17139 |
Liposomal/nanoparticle: only panobinostat liposomes (CLBL-1, mouse biodistribution; 37711439). Liposomal doxorubicin in dogs with lymphoma: none found. Nelarabine, clofarabine, cladribine, gemcitabine, bendamustine in dog lymphoma: none found (rabacfosadine only). Autophagy inhibition beyond HCQ: only statin/VCP in vitro above. XPO1: in record; verdinexor canine IC50 2-42 nM in lymphoma lines (24503695) vs 89.8-418 nM (40872651); phase II n=58 ORR 37%, T-cell 71% (30143046, doi 10.1186/s12917-018-1587-9); KPT-335 + doxorubicin/vincristine combinations in vitro (41285475).

### 3.5 Checkpoints beyond PD-1, see 2.1. 3.6 Oncolytic viruses
| virus | dog data | verdict |
|---|---|---|
| **VSV-IFNb-NIS (IV)** | 9 dogs, one IV dose; **2 dogs with high-grade peripheral T-cell lymphoma had rapid but transient remission** of disseminated disease; transient hepatotoxicity; no infectious virus shed; VSV RNA in blood correlated with response (29158470, doi 10.1158/1535-7163.MCT-17-0432) | OUTCOME, n=2, T-cell relevant |
| reovirus | 4 of 10 canine lymphoma lines susceptible; one intratumoral injection suppressed xenograft (25319493, doi 10.1111/vco.12124) | weak (lymphoma "less susceptible") |
| canine distemper virus | infects 40-70% of three canine lymphoid lines and 50-90% of neoplastic lymphocytes from B and T lymphoma dogs, causes apoptosis (15746063, doi 10.1158/1078-0432.CCR-04-1944); no in vivo dog data | in vitro only |
| Newcastle disease virus | review title only (26703717) | not evaluated |

### 3.7 Other categories
- **Metronomic/antiangiogenic**: metronomic cyclophosphamide already in catalogue; no further canine lymphoma data beyond ABT-526 (above). Microvessel density/VEGF expression described (17888471, 17467003).
- **Microbiome/diet/vitamin D/fasting**: only observational (chemotherapy alters gut microbiota 40326149; microbiome comparisons 36853067, 38788999; a high-protein, high-fibre, omega-3 diet study measured quality of life in dogs on chemotherapy 37933436; titles only read, effect direction not read, endpoint is not anti-tumour). No intervention with a tumour endpoint, no vitamin D or fasting-mimicking canine lymphoma study found.
- **Hyperthermia/PDT/electrochemotherapy/focused ultrasound**: nothing relevant retrieved (hits were imaging and unrelated). Systemic multicentric disease: expected irrelevant.
- **Gene therapy**: none in canine lymphoma (see 3.3); oncolytic VSV above is the nearest.
- **Antigen-presentation rescue**: human DLBCL, EZH2 inhibitors restore MHC-I/II expression in EZH2-mutant lines (30705065, doi 10.1158/2159-8290.CD-18-1090). **No canine experiment** restoring MHC with EZH2 inhibitor, HDACi or IFN-gamma found (canine IFN-gamma caused death in 1/9 lymphoma lines, 32799170). Canine EZH2 mutation status in lymphoma: not searched.
- **Marrow-niche / CXCR4**: plerixafor mobilises stem cells in healthy dogs (9 dogs, 30221450, doi 10.1111/vco.12446; autologous and DLA-identical engraftment after AMD3100-mobilised PBMC, 16105977, doi 10.1182/blood-2005-05-1937). CCR4 or CCR7 knock-out reduces migration and growth of a canine cutaneous lymphoma xenograft (41224331, doi 10.1292/jvms.25-0185). **No plerixafor chemosensitisation or niche-release experiment in canine lymphoma found.** CD47/SIRPa: 3.1.

## 4. Why no per-day kill rate is DERIVED in this sweep

The model's method is IC50 x exposure. In this pass I found canine IC50s (section 3.4) but **no dog exposure** for panobinostat, bortezomib/ixazomib, flavopiridol, vorinostat, berzosertib, or the CDK4/6 and JAK1 agents except oclacitinib bioavailability (no Cmax in the abstract). RV1001 has an exposure (Cmax ~6 ug/mL at 15 mg/kg) but no IC50. Nothing here therefore qualifies as DERIVED or STRICT. Fastest path to new STRICT entries, in order: (1) dog or human PK for panobinostat and bortezomib (human PK is TRANSFER if the transfer is argued in writing; the panobinostat clinical PK review PMID 28667459 exists but its numbers were not captured here); (2) an RV1001 (or idelalisib/duvelisib) IC50 in canine lymphoma lines; (3) vorinostat dog PK at lymphoma-relevant dose.

## 5. Candidates most likely to change the result

Ranking weighs: (a) second independent route to an escape that is currently single-covered, (b) acts on non-dividing persisters, (c) not a P-gp substrate, (d) reaches CNS, (e) T-cell relevant. Escape numbers are "argued by pathway position".

**T0. CD52 antibody (verify first, not rankable).** Only evidence is a review statement of conditional licensure for T-cell lymphoma (26545847). If real and obtainable, it is the only T-lineage-directed agent on the list (the catalogue's CD5/CD52 effector is marked non-existent), covers 14 (CD7 loss) by a different target, and is pump-independent as a large protein. Grade ASSUMED until a primary source (n, ORR, duration, dose) is found. CNS: antibodies reach CSF poorly (not verified here).

**1. PI3Kd inhibitor class (RV1001; duvelisib/idelalisib as human-licensed forms).** Dog: n=56, ORR 62-77%, 100% ORR in 5 naive T-cell dogs, works in chemo-resistant disease (29689086). Human T-cell transfer: duvelisib PTCL ORR 48-50% (42018969, 29191916). Covers 7 (PI3K/AKT bypass) directly, plausibly 6 and, via Treg modulation discussed in the paper, 10. Persisters: no (signalling inhibitor; TTP 21-25 d). P-gp: not found. CNS: not found (related ME-401 entered mouse brain). Toxicity axis: hepatic (DLT; trough 20-30 uM), GI, marrow rare; intermittent 4-on/3-off dosing removed accumulation. Availability: RV1001 trial compound (Rhizen); duvelisib/idelalisib human-licensed, off-label (licence status not verified here). Grade OUTCOME (dog) / TRANSFER (T-cell). Caution: short TTP means single-agent kill is not durable; value is as a component.

**2. HDAC inhibitor (panobinostat, vorinostat).** Canine IC50 18 nM (panobinostat, CLBL-1; xenograft inhibited) and SAHA 0.6-4.8 uM with T-cell lines most sensitive. Vorinostat: reported not a P-gp substrate and CNS delivery not P-gp/BCRP-limited (mice); panobinostat IS a P-gp/BCRP substrate and CNS-limited. Possible cover of 3 (BCL2-family effects: not verified), 12 (MHC restoration by epigenetic agents: shown for EZH2 inhibitors only, not HDACi), 8 (epigenetic, not division-gated: mechanism argued, no data). Toxicity axis: marrow/GI/cardiac (QTc) in humans (not verified here); dog valproate phase I showed no added marrow toxicity. Availability: vorinostat human-licensed (off-label); panobinostat human. Grade: MEASURED (IC50) + TRANSFER (P-gp, CNS); exposure needed to become DERIVED. Best candidate to add a STRICT-grade, pump-independent (vorinostat) entry for T-cell.

**3. CD47-SIRPa blockade with an opsonising antibody.** Macrophage phagocytosis does not depend on cell cycle, so it can reach non-dividing persisters (8) and is pump-independent (1, 2); also targets macrophage checkpoint (10). Canine components exist; mouse xenograft cures 100% with anti-CD20 (27856424); human DLBCL ORR 40% (30380386). Limits: needs an opsonin, so does not cover 4 unless paired with a non-CD20 antibody (CD19/CD52/CD22: reagents exist or claimed); anaemia is an expected on-target effect, mitigated by a priming dose, in the human trial (30380386). No dog trial. CNS: antibody access poor. Grade MEASURED (mouse, canine cells) + TRANSFER.

**4. Autologous CD8 T-cell add-back after CHOP.** The only dog immunotherapy in this sweep with a survival benefit over matched controls (OS 392 vs 167 d; tumour-free 338 vs 71 d; n=8 vs 12). Antigen-independent, so a second route around 4 and 5 (CD20/CD19 loss) and pump-independent (1, 2); can reach non-dividing cells in principle (8). Does not cover 12 (needs MHC-I) or T-lineage disease. Persistence 49 d. Toxicity axis: immune, mild. Availability: buildable (aAPC K562 + IL-2/IL-21; dog-specific manufacturing shown). Grade OUTCOME (historical controls). Directly addresses the ledger's weakness that the only closing B-cell program needs a trial-stage antibody.

**5. Proteasome inhibitor (bortezomib, ixazomib).** Canine IC50 15.1 nM and 59.1 nM; NF-kB constitutively active in canine lines and abolished by bortezomib (covers 6, plausibly 3). Acts on non-dividing cells mechanistically (proteotoxic, not cycle-gated), argued not shown in lymphoma (8). Design constraint: antagonistic with 4-HC (cyclophosphamide) in vitro, synergistic with doxorubicin (38237918). Carfilzomib shows ABCB1-mediated efflux/resistance; bortezomib P-gp role is reported only as a secondary statement. CNS: not found. Toxicity axis: neuropathy, GI, marrow (human; not verified here). Availability: human-licensed, off-label. Grade MEASURED (IC50); exposure needed. Good STRICT-grade candidate once PK is sourced.

**6. CDK9/MCL-1 axis (flavopiridol).** All 8 canine lines killed at 400 nM with loss of Mcl-1 and XIAP and xenograft shrinkage: a second, transcription-level route to 3 (intrinsic-apoptosis evasion, today closes by only +0.009/day on strict potency) independent of BCL2 (canine B-cell lines are venetoclax-resistant, EC50 288 uM). Transcriptional blockade is not cycle-gated (8, argued). P-gp not found; no dog PK or toxicity. Availability: human trial drug. Grade MEASURED (in vitro, mouse xenograft). Highest upside for the thin TP53/apoptosis margin; highest uncertainty on exposure/toxicity.

**7. Oclacitinib (JAK1) for T-cell disease.** Veterinary-licensed (atopic dermatitis), oral, 89% bioavailable in dogs, cheap. 5 of 9 lines sensitive through JAK1/STAT5; clinical data in epitheliotropic lymphoma only and conflicting (12 vs 11 CCNU comparable; 1/8 responded). Adds a T-cell route not among the 14 escapes (JAK/STAT independence would be a new escape). Not a persister agent; no multicentric clinical data; P-gp and CNS not found. Toxicity axis: mild (immune/infection). Grade MEASURED (in vitro) + OUTCOME thin.

**8. Intravenous oncolytic VSV-IFNb-NIS.** Two dogs with high-grade peripheral T-cell lymphoma had rapid transient remission after one IV dose; pump-independent; replicates regardless of cell cycle; no shedding; transient hepatotoxicity (29158470). Antigen- and lineage-independent (covers 4, 5, 11, 14 by construction). Limits: transient, n=2, neutralising immunity on repeat dosing (argued, not shown). Availability: investigational. Grade OUTCOME (n=2).

**Hand-offs and lower tier.** 211At/131I anti-CD45 radioimmunotherapy (dog data in healthy dogs for conditioning: pan-lymphoid incl. T, alpha emitter not cycle-gated, pump-independent) belongs with the transplant agent. Masitinib (vet-licensed, inhibits P-gp at >=1 uM in canine lymphoid cells) and celecoxib (prevents P-gp induction) are second-source P-gp reversers for escape 1, relevant because the only dog RCT of valspodar was null (28357033, in record). ATR, BET, PARP, CDK4/6, VCP and simvastatin are in-vitro-only and cycle- or replication-dependent or narrow. Rescue alkylators (melphalan, DTIC/temozolomide, actinomycin D, mitoxantrone) are available and have dog numbers but give 14-130 day responses; useful as sequential non-cross-resistant lines, not as closure.

## 6. Escapes: where new candidates add coverage (argued by pathway position)

| escape | currently covered by (record) | new independent candidate routes |
|---|---|---|
| 1, 2 P-gp / BCRP | antibody, verdinexor, reverser (null in dog RCT) | vorinostat (not a substrate), CD47 + antibody, VSV, T-cell add-back; masitinib/celecoxib as alternative reversers. Note panobinostat, venetoclax (reported substrates) and carfilzomib (ABCB1-mediated resistance) are pump-exposed |
| 3 TP53 / apoptosis evasion | doxorubicin, antibody (thin +0.009) | flavopiridol (MCL-1/XIAP), bortezomib, VSV |
| 4, 5 CD20 / CD19 loss | doxorubicin, verdinexor, tandem CAR-T | T-cell add-back, VSV, CD47 + non-CD20 opsonin, CD19 antibody (reagent only) |
| 6 BCR/NF-kB independence | acalabrutinib (ASSUMED) | bortezomib (NF-kB), PI3Kd |
| 7 PI3K/AKT bypass | "MEASURED expression only" | PI3Kd (dog ORR 62-77%) |
| 8 persister | division-gated agents weighted by awake fraction f | CD47/phagocytosis, T-cell add-back, VSV, flavopiridol/proteasome (mechanism argued, no data) |
| 10 exhaustion / microenvironment | PD-1/CD28 switch CAR-T (ASSUMED) | CD47 (macrophage), PI3Kd (Treg), IL-15 adjunct (weak) |
| 12 antigen-presentation loss | (added later; agent per ledger) | EZH2/HDAC epigenetic rescue: human evidence only (30705065) |
| 14 CD7 loss | - | CD52 antibody (unverified), VSV, 211At anti-CD45 |
| T-lineage CNS | none (open at every grade) | none found; vorinostat is the only candidate with a CNS-delivery argument (mouse) |

## 7. Searched and NOT found (do not re-search without a new idea)

- Canine CD52 therapy primary data; canine CD79b/CD22/CD30 antibody-drug conjugates; canine CD3xCD20/CD3xCD19 bispecifics; canine anti-CD25 therapy; canine anti-CD47 antibody (only SIRPa-Fc, mouse).
- 131I/90Y/177Lu radioimmunotherapy in dog lymphoma (only CD45 conditioning in healthy dogs, CD22 imaging in one dog).
- CAR-NK, CAR-macrophage, gamma-delta T cells, TIL, cytokine-induced killer cells in dog lymphoma; any NK-cell trial in lymphoma (NK trials are solid tumours, n=3 and melanoma/OSA).
- IL-12 gene/plasmid, suicide gene, in vivo CAR, IL-15 superagonist in dog lymphoma (a recombinant canine IL-15 adjunct trial exists; armoured CAR not).
- CTLA-4, LAG-3, TIM-3 antibodies or trials in dogs with lymphoma.
- mTOR/rapamycin, MDM2/nutlin, MCL-1 inhibitors, ferroptosis inducers, arsenic trioxide, lenalidomide/IMiDs, idelalisib, duvelisib, zanubrutinib efficacy in dog lymphoma; tazemetostat/EZH2 inhibitor in dogs.
- Nelarabine, clofarabine, cladribine, gemcitabine, bendamustine, liposomal doxorubicin in dog lymphoma.
- Vitamin D, fasting-mimicking or diet intervention with tumour endpoint; probiotic intervention; hyperthermia/PDT/electrochemotherapy for lymphoma.
- Plerixafor or any niche-releasing agent combined with chemotherapy in canine lymphoma.
- Dog exposure (Cmax/AUC) for panobinostat, bortezomib, flavopiridol, vorinostat at lymphoma doses.
- P-gp substrate status for melphalan, dacarbazine, actinomycin D, mitoxantrone, RV1001, oclacitinib, flavopiridol, ixazomib (not verified; do not assume).
- Human data not verified in this pass: CD3xCD20 bispecifics, polatuzumab/brentuximab ADCs, alemtuzumab in T-cell lymphoma (searches returned unverified or irrelevant records, so none is cited).
- bioRxiv: tool has no keyword search; only a 30-record window scanned. The EDEN_by_Basecamp_Research MCP server needs authorisation and was not used.

## 8. Limits and cautions (rule 5)

- Abstract-level reading for all but two papers; n, ORR and IC50 values are as printed in abstracts. Ibrutinib dog result (20615965): n and ORR not retrievable.
- Historical-control comparisons (adoptive T cells n=8 vs 12; dTERT-type results belong to the vaccine agent) are OUTCOME at best.
- Dog single-arm response rates (RV1001, rIL-15, rescue protocols) are not kill rates; they are inputs for regimen calibration, not STRICT grade.
- "Acts on persisters" and "covers escape N" are mechanism statements unless a citation says otherwise; the only persister-related primary item retrieved is human (sublethal cytochrome c release generates drug-tolerant persisters, 36055199, title only read). No canine lymphoma persister-directed experiment found.
- Conflicting dog data: oclacitinib 12-dog CETL comparison (comparable to CCNU) vs 8-dog series (1/8 responded).

## 9. Suggested next actions for the parent thread (not done here)

1. Re-grade anti-PD-1 to MEASURED-NEGATIVE (0/15, PMID 42247661) and remove the melanoma transfer.
2. Resolve the venetoclax P-gp question (39620327) before calling venetoclax the T-cell pump closer.
3. Add candidate entries with explicit grades: RV1001/PI3Kd (OUTCOME), vorinostat and panobinostat (MEASURED IC50, TRANSFER PK), bortezomib (MEASURED IC50, TRANSFER PK), CD47+antibody (TRANSFER), T-cell add-back (OUTCOME), flavopiridol (MEASURED in vitro), VSV (OUTCOME n=2), oclacitinib (T-cell).
4. Find the CD52 primary source (USDA summary of basis) before any CD52 entry.
5. Record in STATUS.md: sweep done for these categories, the not-found list in section 7, and the record-vs-new table in section 1.

## 10. Reference index (PMID, DOI where the fetch returned one)

26545847 10.1016/j.tvjl.2015.10.008 | 39954194 10.1007/s12602-025-10468-8 | 38662527 10.1111/jvim.17080 | 41742528 10.1093/jvimsj/aalaf039 | 37624862 10.1371/journal.pone.0290428 | 41844944 10.1038/s41598-026-44677-0 | 29689086 10.1371/journal.pone.0195357 | 27856424 10.1158/2326-6066.CIR-16-0105 | 42247661 10.1093/jvimsj/aalag098 | 37792729 10.1371/journal.pone.0291727 | 33668625 10.3390/cancers13040785 | 29380929 10.1111/vco.12386 | 27107075 (no DOI) | 28111882 10.1111/vco.12297 | 37884996 10.1186/s12935-023-03104-4 | 39314237 10.1016/j.isci.2024.110863 | 32002286 (title only) | 41376156 10.1016/j.ymthe.2025.12.010 | 42480604 10.1158/1535-7163.MCT-26-0365 | 27401141 10.1038/mt.2016.146 | 22355761 10.1038/srep00249 | 38631708 10.1136/jitc-2023-007963 | 42461253 10.1111/vco.70091 | 37852175 10.1016/j.xcrm.2023.101241 | 30563208 10.3390/vetsci5040100 | 40520425 10.3389/fvets.2025.1596084 | 37006127 10.1111/vde.13161 | 32799170 10.1016/j.rvsc.2020.08.007 | 21569195 10.1111/j.1476-5829.2010.00234.x | 29158470 10.1158/1535-7163.MCT-17-0432 | 25319493 10.1111/vco.12124 | 15746063 10.1158/1078-0432.CCR-04-1944 | 26703717 (title only) | 38237918 10.1111/vco.12957 | 23337362 10.1292/jvms.12-0168 | 29983882 10.18632/oncotarget.25580 | 37711439 10.3389/fvets.2023.1236136 | 18593248 10.2460/ajvr.69.7.938 | 20705615 10.1158/1078-0432.CCR-10-1238 | 30533020 10.1371/journal.pone.0208709 | 35409379 10.3390/ijms23074021 | 33079733 (abstract sentence only) | 39893010, 37827699, 38151817, 27564097, 41923105, 41373605, 38072962, 38969867, 34478517, 39620327 (abstract sentences on transporters; DOIs not captured) | 36433867 10.1111/jvim.16587 | 25623777 10.1111/vco.12130 | 36450591 10.1292/jvms.22-0498 | 17606508 (title only) | 39300906 10.1111/vco.13014 | 40616061 10.1186/s12917-025-04880-z | 41728128 10.3389/fvets.2026.1725824 | 32620617 10.21873/anticanres.14367 | 42187333 10.1002/bmc.70498 | 42368342 10.3389/fvets.2026.1823343 | 41680286 10.1038/s41598-026-40066-9 | 42554028 10.1111/vde.70115 | 40525607 10.1111/vde.13366 | 41473101 10.3389/fvets.2025.1645059 | 24330031 (dog oclacitinib PK, abstract) | 34884478 10.3390/ijms222312673 | 40351764 10.3389/fvets.2025.1577028 | 27434128 10.1371/journal.pone.0159607 | 20615965 10.1073/pnas.1004594107 | 42018969 10.1200/JCO-25-03120 | 29191916 10.1182/blood-2017-05-786566 | 40526834 10.1182/bloodadvances.2025016347 | 30380386 10.1056/NEJMoa1807315 | 39213421 10.1182/bloodadvances.2024013277 | 30705065 10.1158/2159-8290.CD-18-1090 | 29314493 (abstract) | 26104798 10.1186/s12885-015-1489-1 | 38340381 10.1016/j.rvsc.2024.105174 | 41044621 10.1186/s12917-025-05053-8 | 41595541 10.3390/biomedicines14010003 | 17189419 10.1158/1078-0432.CCR-06-0110 | 28592719 10.1292/jvms.16-0457 | 26364581 10.1111/vco.12157 | 23363222 10.1111/jvp.12039 | 31836165 10.1016/j.tvjl.2019.105398 | 32365663 10.3390/cancers12051117 | 36010910 10.3390/cancers14163919 | 41406705 10.1016/j.vetimm.2025.111048 | 26678182 10.1111/jvim.13807 | 18673031 10.2460/javma.233.3.446 | 19709354 10.1111/j.1939-1676.2009.0376.x | 30653362 10.5326/JAAHA-MS-6878 | 17696856 10.2460/javma.231.4.563 | 23910023 10.1111/vco.12055 | 17063713 | 24489398 | 30666777 10.1111/vco.12457 | 28941072 10.1111/vco.12356 | 38175982 10.5326/JAAHA-MS-7372 | 34213084 10.1111/vco.12749 | 38890811 10.1111/vco.12990 | 41914636 10.1111/vco.70062 | 38961691 10.1111/jvim.17139 | 30143046 10.1186/s12917-018-1587-9 | 24503695 10.1371/journal.pone.0087585 | 40872651 10.3390/vetsci12080700 | 41285475 10.1292/jvms.25-0478 | 24991836 10.4161/auto.29165 | 26338894 10.2967/jnumed.115.162388 | 39025648 10.2967/jnumed.124.267540 | 32117707 10.3389/fonc.2020.00020 | 32081102 10.1177/0300985819900352 | 30221450 10.1111/vco.12446 | 16105977 10.1182/blood-2005-05-1937 | 41224331 10.1292/jvms.25-0185 | 42754084 10.1016/j.tvjl.2026.106881 | 36055199 (title only) | 31506873 10.1007/s11523-019-00668-y | 28357033 (from record, not re-fetched)
