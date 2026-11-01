# Lawful CNS agents for the canine B-cell brain sanctuary (sweep 2026-11-01)
Labels: [REC] = already in record (file named); [NEW] = not in record (grep of docs/ and src/ by PMID). PubMed via MCP; web where stated.

Question: which drugs a US veterinarian can lawfully give a dog (FDA-approved animal drug, or FDA-approved human drug used
extra-label under 21 CFR 530) reach the brain/CSF at UNBOUND levels that kill canine B-cell lymphoma, so they could form an
independent second brain route alongside intrathecal methotrexate + one 23.4 Gy course?

Bar (CLAUDE.md, user's words): "real data OR a rigorous model"; "I'm okay with no specific data but if scientifically sound";
cross-species/compound transfer only with a written comparison of what differs and which way it pushes, usually as a floor or
ceiling (rule 15). Absence of canine data is not a reason to exclude (rule 13).

## 0. Record check (rule 1) -- why each candidate is or is not in the CNS pool today

How the pool is built: `lymphoma_sustained.lawful_pool(ip, CNS)` = `G.sound_pool(G.available(G.grounded_agents(CNS, ip)))`
filtered by `LEGAL_STATUS`. `sound_pool` admits only potency grades in SOUND_GRADES (DERIVED, PARTIAL, MEASURED, OUTCOME,
REGIMEN-CALIBRATED, MECHANISM, TRANSFER, TRANSFER-OUTCOME, BRACKET). Running it (B-cell, CNS) returns: doxorubicin 0.05,
vincristine 0.05, cyclophosphamide 0.05, prednisolone 0.08, craniospinal RT 1.0, HCQ 0.3, TBI+transplant 1.0, verdinexor 0.05,
HBI 1.0, cytarabine CRI q14d/q7d 1.0, panobinostat 0.25, vorinostat 0.0, bortezomib 0.0, thiotepa-HDC 1.0, allo-DLA HCT 0.5,
zanubrutinib 0.43 (numbers = CNS access factor in the catalogue).

| candidate | in catalogue? | why absent from the CNS pool (record) |
|---|---|---|
| lomustine | yes, access 0.50, kill 0.12 | potency grade **ASSUMED** ("one line IC50 (27 uM), no canine PK found", `lymphoma_grounded.py:141`) -> filtered by `sound_pool`. SWEEP_regrade s3 already derived k 0.004-0.04/d (central 0.015), CSF radioactivity >=50% of plasma (Gleostine label), NOT an ABCB1 substrate (PMID 36252775), dormant-cell kill not shown (mouse HSC negative, 7917905), dog hepatotoxicity 6.1% cumulative (14765735). The derived k was never written back into the catalogue. |
| high-dose IV methotrexate | yes, access 0.30, kill 0.22 | potency **ASSUMED (human transfer)** -> filtered. Human HD-MTX CSF >1 uM (PMID 18282, SWEEP_outside_model item 5). Defeated by E9 (RFC loss). |
| acalabrutinib | yes, access 0.05, kill 0.06 | **ASSUMED** (dog occupancy >90% but ORR 25%, PFS 22.5 d, PMID 27434128). Labelled P-gp + BCRP substrate. |
| venetoclax | yes, access 0.0074 | **MEASURED-NEGATIVE** for B-cell (canine B-cell EC50 288 +- 700 uM); CSF/plasma 0.74% (39286959). |
| rabacfosadine | yes, access 0.05 | ASSUMED; CSF access NOT FOUND; resting cells 127x less sensitive (18451250). |
| intrathecal cytarabine | yes | ASSUMED. |
| temozolomide | no | LYMPHOMA_UNIVERSE row A "EVALUATED, EXCLUDED": canine rescue responses 14-130 d, "no exposure-derived kill; P-gp status unverified"; SWEEP_nongated B: NCI-60 GI50 84/>100/78 uM "far above CSF levels: not a closer". Canine TMZ+anthracycline rescue n=63 (17696856) in SWEEP_modalities. |
| procarbazine | no | LYMPHOMA_UNIVERSE I.4 lead only ("dCK-independent; 50 dogs on a continuous regimen, CSF not found"). |
| carmustine | no | NCI-60 33/14/19 uM, no P-gp cross-resistance 1.1x (SWEEP_nongated B); canine PK NOT FOUND (SWEEP_cnsregimens s8); BCNU-thiotepa is the human ASCT conditioning (in record as OUTCOME). |
| ibrutinib | no | SWEEP_cnsregimens s4, SWEEP_inhibitors_partial C: canine CLBL-1 IC50 1.3 uM (34884478); human PCNSL ORR 74%, median PFS 4.5 mo (38995739); mouse Abcb1 KO brain:plasma 4.5x (30247919); "detectable in CSF" (31279304) but CSF NUMBER NOT FOUND. Excluded in UNIVERSE as "responses last months". |
| zanubrutinib | IN POOL, access 0.43 | CSF/free plasma 42.7 +- 27.7% (35004280). Kill grade TRANSFER (human BCR-dependent lines); canine CLBL-1 is BCR-independent for ibrutinib. |
| lenalidomide / pomalidomide | no | canine CRBN carries the mouse-type Ile at human V388 -> predicted IMiD-resistant (SWEEP_inhibitors_partial D, sequence inference); CSF: lenalidomide >=20% (29986852) vs 1.3-2.4% (35732975), rhesus 11% (22109830); pomalidomide rat ~39% (23940785). |
| dexamethasone | no | canine lines CL-1/GL-1 dex-resistant with low GR (20362310); E1 GR loss (31943234, median onset 68 d). |
| ifosfamide | no | not in record (grep 0). |
| thiotepa | IN POOL (HDC with graft) | CSF:plasma AUC ~1 (2491958), NCI-60 6-10 uM, P388/ADR 1.07x, derived k 0.13-0.37/d per pulse (SWEEP_nongated A); no canine PK. |
| cytarabine (IV CRI / HD) | IN POOL | dog CSF 8.3 uM, CSF:plasma 0.62 (1742843); human HD 3 g/m2 CSF 7.8 uM (7075116). Defeated by E2. |
| verdinexor | IN POOL, access 0.05 (floor 0.09 transferred) | SWEEP_xpo1_cns. |
| busulfan, treosulfan, cladribine, artesunate, ONC201, arsenic | evaluated in SWEEP_nongated | busulfan CSF:plasma 1.3 but lymphoid GI50 124-145 uM; treosulfan rat CSF 0.11 parent; cladribine BCRP + dCK; ATO CSF 14-19%. |

Not in record anywhere (grep of docs/ returns zero): ifosfamide, pemetrexed, topotecan, dexamethasone CSF ratio, ibrutinib CSF
number, temozolomide CSF/brain ECF numbers, THOP (PMID 40266942), TMZ single-agent canine rescue (28766920).

## 1. Findings by agent (appended below)

### Temozolomide [NEW numbers]
- Human CSF: AUC_CSF/AUC_plasma 20% (35 glioma pts, pop-PK; PMID 15173079, DOI 10.1158/1078-0432.CCR-03-0807). Children metronomic
  24-77 mg/m2/d: median plasma 0.96, CSF 0.37 ug/mL; simulated AUC ratio 37% (n=11; PMID 35355137, DOI 10.1007/s00280-022-04424-4).
  Rhesus IV 150 mg/m2: plasma peak 104 uM, CSF peak 26 uM, AUC ratio 0.33 +- 0.06 (n=3; PMID 12675312); rhesus IV 22% (PMID 28290002).
- **Rule-14 proxy (peritumoral brain interstitium, barrier largely intact)**: intracerebral microdialysis in PERITUMORAL brain, 150 mg/m2 PO:
  AUC plasma 17.1, brain ECF 2.7 ug.h/mL, **ratio 17.8%**, brain Cmax 0.6 +- 0.3 ug/mL (~3 uM), Tmax 2 h (n=7; PMID 19861433,
  DOI 10.1158/1078-0432.CCR-09-1349). TMZ protein binding ~15% (label), so CSF/total ~= CSF/unbound: **Kp,uu(CSF) ~0.2-0.37,
  brain ECF/unbound plasma ~0.21** (DERIVED, human).
- Potency: NCI-60 lymphoid GI50 78-100+ uM [REC SWEEP_nongated B]; brain ECF peak ~3 uM is 25-30x below. Canine single-agent rescue
  n=26: ORR 32%, median TTP 15 d (PMID 28766920, DOI 10.1111/vco.12335) [NEW]; THOP first-line (TMZ replaces cyclophosphamide in CHOP) in
  14 dogs with B-cell lymphoma: all CR, median TTP 269 d, MST 433 d (PMID 40266942, DOI 10.3390/vetsci12030251) [NEW; pilot, uncontrolled].
- Escapes: MGMT (direct repair of O6-meG), MMR loss (tolerance); kill requires replication through O6-meG:T mispairs -> DIVISION-GATED by
  mechanism; ABCB1 knock-out changed TMZ response in GBM cells (36252775 [REC]); BCRP effluxes TMZ in BCRP-MDCKII (PMID 31493543 abstract
  wording). dCK/RFC independent.
- Verdict: reaches brain (Kp,uu ~0.2) but kill is ~0 at that exposure and gated; cannot cover E5. NOT a second route.

### Ibrutinib [NEW: the CSF number the record lacked]
- Grommes 2017 Cancer Discov (PMID 28619981, DOI 10.1158/2159-8290.CD-17-0613; full text PMC5581705 read): CSF 2 h post-dose day 1 mean
  0.77 ng/mL (1.7 nM) at 560 mg, 1.95 ng/mL (4.4 nM) at 840 mg; day 29 1.65 and 3.18 ng/mL (3.7, 7.2 nM); n=18 day 1, 14 day 29. Authors:
  ~10 nM needed for PCNSL cell death in vitro, "not achieved in cerebrospinal fluid for many PCNSL patients". Paired plasma ratios not in
  the main text. Protein-binding-corrected CSF penetration 28.7-43.4% by dose cohort appears only in a trial-protocol summary
  (clinicaltrials.gov NCT05211336 protocol PDF, secondary; UNVERIFIED against primary).
- Canine potency: CLBL-1 IC50 1.3 uM [REC 34884478] -> CSF 2-7 nM is ~200-700x below. Kill on canine BCR-independent disease ~0.
- Verdict: reaches CSF at Kp,uu ~0.3-0.4 (TRANSFER), but canine potency excludes it. Not a second route.

### Dexamethasone [NEW]
- DOG: tritiated dexamethasone IV, CSF/plasma radioactivity 30.9% at 15 min rising to 91.5% (cranial) and 93.5% (spinal) at 3 h (mongrel
  dogs; PMID 944876, No Shinkei Geka 1976, Japanese, abstract only; radioactivity = parent + metabolites, total plasma).
- Rhesus: IV CSF/plasma 0.15 +- 0.02 (dex) vs 0.08 +- 0.03 (prednisolone); dex 70% bound; "CSF concentrations of dexamethasone and
  prednisolone approximated free plasma concentrations" -> **Kp,uu(CSF) ~0.5-1** (PMID 3806166, DOI 10.1200/JCO.1987.5.2.202).
  At oral prednisone doses prednisolone is >90% bound, so dexamethasone delivers proportionally more free drug to CSF than the
  prednisolone already in the pool.
- Lawful: dexamethasone is FDA-approved for dogs (veterinary dexamethasone injection/tablets) -> on-label class use.
- Potency/escapes: glucocorticoid apoptosis is not division-gated, but canine lines CL-1/GL-1 are dex-resistant with low GR (20362310
  [REC]) and E1 (GR loss) develops in essentially all dogs, median 68 d (31943234 [REC]); dex is a P-gp substrate (class knowledge; not
  re-verified here). Verdict: better CSF reach than prednisolone, same mechanism and same escape (E1) -> NOT independent of prednisolone.

### Ifosfamide [NEW]
- Human CSF 10 min after 3-h infusion 1.3-2 g/m2: parent median 79 uM, CSF/plasma 0.38 (0.18-0.72); active 4-OH-IFO median 4.1 uM, CSF/plasma
  3.07 (0.62-29), undetectable in 6/17 samples (n=12; PMID 20182727, DOI 10.1007/s00280-010-1274-4). Children: IFO and 4-OH-IFO CSF "almost as
  high as plasma" (PMID 9677448, n=4); CSF:plasma greater for IFO than CP; isophosphoramide mustard highest ratio (PMID 9815588, n=25).
  Low protein binding -> CSF/unbound ~0.4 (parent).
- Contrast with cyclophosphamide in the pool (access 0.05): children on CP had NO detectable metabolites in CSF (9815588) -> ifosfamide is
  the oxazaphosphorine that reaches CSF.
- Alkylator (phosphoramide mustard): dCK/RFC-independent; not P-gp-limited by class (not verified). Class evidence on non-cycling B cells:
  mafosfamide (activated oxazaphosphorine) alone triggers apoptosis ex vivo in circulating CLL cells, which are non-dividing (PMID 23744431,
  abstract; human CLL, indirect for E5).
- **DOG OUTCOME CONTRADICTS KILL**: 72 dogs, 350-375 mg/m2 IV + mesna; of the 40 with LYMPHOMA, **one partial response (112 d)**; dose-limiting
  neutropenia day 7; no haemorrhagic cystitis (PMID 10830540, Rassnick 2000 JVIM, DOI 10.1892/0891-6640(2000)014<0271:eoifto>2.3.co;2).
  OSA salvage 375-425 mg/m2: 2/19 hospitalised (PMID 22985083). The canine tolerated dose (~375 mg/m2) is ~1/4-1/5 of one human daily dose
  (1.3-2 g/m2), so canine CSF exposure would also scale down (direction: lowers the transferred CSF level).
- Verdict: EXCLUDED with a stated reason (rule 13): kill contradicted by canine lymphoma outcome at the tolerable dose.

### Procarbazine [label + canine outcome; NEW pmids]
- Lawful: Matulane (human, FDA-approved), extra-label in dogs; used routinely in LOPP/MOPP/PPC.
- CNS: label "crosses the blood-brain barrier and rapidly equilibrates between plasma and cerebrospinal fluid after oral administration"
  (Matulane PI via drugs.com/medlibrary; qualitative, no ratio); parent t1/2 ~10 min IV; activity needs hepatic CYP activation to azo/azoxy
  methylating species -> CSF level of the PARENT does not measure the active species. Kp,uu: NOT FOUND (no number in any source read).
- Canine: oral procarbazine + prednisolone + cyclophosphamide daily, n=50 failed/intolerant dogs: ORR 70% (CR 46%), "very well tolerated"
  (PMID 35338560, DOI 10.1111/vco.12814); LOPP naive T-cell n=35 median PFS 431 d (30117253), n=31 ORR 97% (28508557), n=67 PFS 118 d
  (34464024); UF-LOPP rescue n=33 ORR 61% (21756176); MPP rescue n=41 ORR 34% (19222829). [all NEW pmids; record had only "50 dogs, CSF not found"]
- Human CNS lymphoma: procarbazine is the "P" of R-MPV (+ rdWBRT 23.4 Gy: CR pts median PFS 7.7 y, PMID 24101038 [REC]).
- Escapes: MGMT (O6-methylguanine; same escape as lomustine/TMZ), MMR loss; dCK/RFC-independent; P-gp: NOT FOUND. Cycle dependence: NOT FOUND.
- Kill: not derivable (prodrug, no IC50 meaningful in vitro) -> OUTCOME-only (multi-agent). Grade: access MECHANISM/label-qualitative.

### Agents whose CNS facts are already in the record (not re-searched; summarised for the table)
- Lomustine: SWEEP_regrade s3 (CSF radioactivity >=50% of plasma, Gleostine label; NOT ABCB1 substrate 36252775; derived k 0.004-0.04/d;
  canine hepatotoxicity 6.1%, cumulative, 14765735; MGMT in 2/5 canine lines 26130852; dog intracranial glioma MST 138 vs 35 d, 29797768).
  NEW: lomustine CSF in dogs still NOT FOUND (PubMed "lomustine cerebrospinal fluid", 31 hits, none a measurement).
- Thiotepa: SWEEP_cnsregimens s8, SWEEP_nongated A.  Zanubrutinib: 35004280.  Lenalidomide/pomalidomide: SWEEP_inhibitors_partial D.
  Venetoclax: SWEEP_outside_model item 5.  Cytarabine: 1742843, 7075116.  Busulfan/treosulfan/cladribine/ATO/artesunate: SWEEP_nongated.
- Acalabrutinib: NEW search "acalabrutinib central nervous system lymphoma cerebrospinal" returned one case (PMID 35732356: MCL leptomeningeal
  relapse in CR 3 y on acalabrutinib maintenance after ibrutinib + IT cytarabine + dex induction; n=1). No CSF level found. Labelled P-gp + BCRP
  substrate [REC] -> the pump escape defeats it at the BBB and in E5.
- Bendamustine: PubMed "bendamustine cerebrospinal fluid" (20 hits) contains no CSF measurement; not assessed further.

## 2. Table

Kp,uu = CSF (or brain ECF) / UNBOUND plasma unless marked "total". Grades: MEASURED / DERIVED / TRANSFER / OUTCOME / ASSUMED / NOT FOUND.
Escapes: E2 dCK loss, E5 quiescent P-gp-high progenitor, E9 RFC loss, E1 GR loss, MGMT, BCL2 rewiring (E4), P-gp/BCRP.

| agent | lawful status (US vet) | unbound CNS ratio + source + species | potency on canine / human lymphoma | cycle-independent? | defeated by | canine tolerability | grade / record |
|---|---|---|---|---|---|---|---|
| **thiotepa (HD, graft)** | human-approved, ELU | CSF:plasma AUC 1.01, fu ~0.8-1 -> ~1 (human n=1, 2491958); NHP transcapillary t1/2 1 min (810575) | NCI-60 lymphoid 6-10 uM; derived k 0.13-0.37/d per pulse; human PCNSL ASCT 3-y PFS 78% | class mechanism yes; dormant kill not shown | GST/MRP conjugate efflux (9788613); BER; NOT P-gp (P388/ADR 1.07x); not E2/E9/MGMT-primary | NO canine thiotepa PK; needs autologous graft (dog HCT exists) | TRANSFER access + OUTCOME; IN POOL; [REC] |
| **lomustine** | human-approved (Gleostine), routine in dogs | CSF radioactivity >=50% of plasma (label, total incl. metabolites) -> ~0.5 floor (human) | canine line 27 uM; NCI-60 8-18 uM; derived k 0.004-0.04/d; dog RR 87% first line (38890811) | alkylator; mouse late-HSC data negative (7917905) | MGMT (2/5 canine lines); not P-gp; not E2/E9 | 60-90 mg/m2 q3w; cumulative hepatotoxicity 6.1% (14765735), marrow | ASSUMED in catalogue (excluded by sound_pool); DERIVED-low in SWEEP_regrade; [REC] |
| procarbazine | human-approved (Matulane), ELU, routine in LOPP/PPC | "rapidly equilibrates" plasma-CSF (label, qualitative); no ratio | prodrug, no IC50; dog PPC ORR 70% n=50 (35338560); R-MPV in PCNSL | NOT FOUND | MGMT, MMR; not E2/E9 | daily oral for months tolerated (35338560) | access label-qualitative; kill OUTCOME (multi-agent) [NEW pmids] |
| temozolomide | human-approved, ELU | CSF/plasma AUC 0.20 (15173079), 0.37 children (35355137), NHP 0.33 (12675312); **peritumoral brain ECF 0.178** (19861433); fu ~0.85 -> Kp,uu ~0.2-0.4 | NCI-60 lymphoid 78->100 uM vs brain ECF Cmax ~3 uM -> kill ~0; dog rescue ORR 32%, TTP 15 d (28766920); THOP 14/14 CR (40266942, in docs/reports) | NO (needs replication/MMR) | MGMT, MMR loss, ABCB1/BCRP (36252775, 31493543) | well tolerated orally | MEASURED access (human); kill ~0 -> EXCLUDED [NEW numbers] |
| HD IV methotrexate | human-approved, ELU | **non-enhancing brain ECF AUC 0.032-0.094 total, Cmax 22-24 uM; enhancing 0.28-0.31** (18787762, glioma, n=4); fu ~0.45 -> Kp,uu ~0.07-0.21; CSF >1 uM (18282) | canine IC50 2-3 nM (secondary); ECF >2 uM for 20-26 h | NO (S-phase) | **E9**, E5 | no canine HD-MTX (12 g/m2) series found | MEASURED access in barrier-intact tissue (human glioma) [NEW]; kill ASSUMED in catalogue |
| HD/CRI cytarabine | human-approved, ELU | dog CSF:plasma 0.62 (1742843); human HD CSF 7.8 uM (7075116) | canine IC50 ~0.4 uM | NO | **E2**, E5 | CRI GI tox 65% (31769013) | IN POOL [REC] |
| ifosfamide | human-approved, ELU | CSF/plasma 0.38 parent (0.18-0.72); 4-OH-IFO 0.6-29, absent in 6/17 (20182727, human) | **dog lymphoma 1 PR in 40 at 350-375 mg/m2** (10830540) | alkylator; mafosfamide kills non-cycling CLL (23744431) | not E2/E9; P-gp not verified | neutropenia d7; tolerated with mesna | access MEASURED (human); kill CONTRADICTED in dogs -> EXCLUDED [NEW] |
| carmustine | human-approved, ELU | CSF 15-70% of plasma (BC Cancer monograph; label radioactivity >=50%) | NCI-60 14-33 uM | as lomustine | MGMT | canine PK NOT FOUND; pulmonary/marrow | access label-level; conditioning partner only [REC + web] |
| dexamethasone | **FDA-approved for dogs** | dog CSF/plasma radioactivity 0.31 at 15 min -> 0.92-0.94 at 3 h (944876, total); rhesus CSF 0.15 total ~= free plasma -> Kp,uu ~0.5-1 (3806166, already used in code for prednisolone 0.08) | canine CL-1/GL-1 dex-resistant, low GR (20362310) | yes (GR apoptosis) | **E1** (GR loss, ~universal by 68 d, 31943234); P-gp substrate (class, not re-verified) | routine | access MEASURED (dog, total) [NEW]; same mechanism as prednisolone -> not independent |
| ibrutinib | human-approved, ELU | CSF 1.7-4.4 nM day 1, 3.7-7.2 nM day 29 (28619981, n=18); corrected penetration 29-43% (protocol PDF, unverified) | canine CLBL-1 IC50 1.3 uM (34884478) -> CSF 200-700x below; human PCNSL ORR 74%, PFS 4.5 mo | cytostatic outside BCR dependence | BTK C481S, CARD11, CD79B; weak ABCB1 | dog: responses stated, n not retrievable (20615965) | access MEASURED (human); canine kill ~0 -> EXCLUDED [CSF number NEW] |
| zanubrutinib | human-approved, ELU | CSF/free plasma 0.43 +- 0.28 (35004280, human) | human BCR-dependent lines nM; canine BCR-independent | cytostatic | P-gp "likely" (label); BCR-independence | no canine data; dog tox study clean (32484067) | IN POOL as TRANSFER [REC]; canine kill unsupported (flag) |
| acalabrutinib | human-approved, ELU | CSF NOT FOUND | dog ORR 25%, PFS 22.5 d (27434128) | cytostatic | **P-gp + BCRP substrate** (label) | grade 1-2 GI, no DLT | ASSUMED; EXCLUDED by pump escape [REC] |
| lenalidomide / pomalidomide | human-approved (REMS), ELU | len CSF 1.3-2.4% (35732975) or >=20% (29986852); rhesus 11%; pom rat ~39% (23940785) | canine CRBN Ile at hV388 -> predicted IMiD-resistant; direct kill 0.0004-0.025/d | NOT FOUND | CRBN (species), P-gp weak | no canine data | EXCLUDED (named species reason) [REC] |
| venetoclax | human-approved, ELU | CSF/plasma 0.0026-0.0074 (37215448, 39286959) | canine B-cell EC50 288 uM | likely yes | E4 BCL2 rewiring; P-gp/BCRP | - | MEASURED-NEGATIVE for B-cell [REC] |
| topotecan | human-approved, ELU | CSF lactone 0.2-0.42 (children; search-level, primary not opened) | - | NO (S-phase) | BCRP, P-gp | - | EXCLUDED (pump + gated) |
| pemetrexed | human-approved, ELU | CSF <2-5% of plasma; rat unbound brain 0.078 (15987831, abstract-level) | - | NO | **E9** (RFC) | - | EXCLUDED |
| verdinexor | **FDA-approved for dogs** | floor 0.09 (selinexor transfer) | canine IC50 2-42 / 90-418 nM | likely | XPO1 mut | on-label continuous | IN POOL [REC] |

## 3. Ranked shortlist for an independent second brain route (B-cell), covering E5 and not defeated by E2/E9

Criteria applied: lawful; measured or transferred unbound brain reach >= ~0.3; kill not contradicted in dogs; not division-gated; not a
P-gp/BCRP substrate; not E2- or E9-dependent; escape set disjoint from IT MTX (E9, E5) and radiation.

1. **Thiotepa, high-dose with autologous graft** (already in the lawful pool). Only lawful drug that meets every mechanistic criterion with
   numbers: access ~1 (human n=1 + NHP), no P-gp cross-resistance, dCK/RFC/MGMT-independent, human CNS-lymphoma outcome. Its escapes (GST/MRP,
   BER) are disjoint from MTX and radiation. Weak points: dormant-cell kill is class mechanism only; a PULSE (one course), not sustained;
   canine thiotepa PK/MTD not found. Grade: TRANSFER + OUTCOME.
2. **Lomustine** (lawful, oral, routine in dogs). Reach >=0.5 (label, total radioactivity -> a floor on parent+metabolites, not a Kp,uu),
   not ABCB1, dCK/RFC-independent -> escape set disjoint from MTX/cytarabine. Fails on size: derived kill 0.004-0.04/d is below the 0.06/d
   bar; MGMT defeats it in 2/5 canine lines; cumulative hepatotoxicity caps the number of doses; nitrosoureas spare late quiescent HSC in mice.
   **Action for the model**: replace the ASSUMED 0.12 with the DERIVED 0.004-0.04 (SWEEP_regrade s3) so `sound_pool` admits it at its real
   number, then test whether it changes the B-cell brain window. Expectation from the numbers: it does not close E5 alone.
3. **Procarbazine** (lawful, oral, months-long daily dosing tolerated in dogs). Reaches CSF (qualitative), MGMT shares the escape with
   lomustine, kill OUTCOME-only. Adds a sustained, home-dosed alkylator but not an escape-independent one from lomustine.
4. **HD IV methotrexate** -- not independent (E9, gated), but it is the only lawful agent with a MEASURED concentration in barrier-intact
   (non-enhancing) tissue (22-24 uM, Kp,uu ~0.07-0.21): it extends the IT-MTX route from CSF/meninges into parenchyma for RFC-intact cycling
   cells. Treat as depth for route 1 (IT MTX), not as route 2.
5. **Dexamethasone instead of prednisolone in the CNS phase** -- higher free CSF level (dog CSF/plasma ~0.9 at 3 h, total; rhesus CSF ~= free
   plasma), cycle-independent kill, approved for dogs; same mechanism and same escape (E1) as prednisolone, so it strengthens an existing
   agent rather than adding a route.

Excluded with stated reasons (rule 13): temozolomide (lymphoid GI50 25-30x above brain ECF peak; gated; MGMT), ifosfamide (dog lymphoma 1 PR
in 40), ibrutinib/zanubrutinib/acalabrutinib (canine B-cell is BCR-independent for ibrutinib, CLBL-1 1.3 uM; acalabrutinib pumped),
lenalidomide/pomalidomide (canine CRBN), venetoclax (canine B EC50 288 uM), topotecan (pumps, gated), pemetrexed (E9, CSF <5%),
carmustine (IV member of the lomustine class; no canine data; kept only as thiotepa conditioning partner).

**Bottom line (at the strength shown):** among lawful drugs, the only class with the mechanism to reach E5 without E2/E9 is the
non-methylating alkylator, and its one member with brain reach ~1 and no pump liability -- thiotepa -- is already in the pool. No lawful agent
outside the current pool adds an independent route with a derived brain kill at the 0.06/day bar; lomustine and procarbazine add a
mechanistically independent but numerically weak alkylator layer (MGMT-limited). This is a finding within the catalogue of 18 agents above,
not a proof that none exists: hydroxyurea, bendamustine, melphalan and busulfan-class agents were not re-assessed here (see SWEEP_nongated).

## 4. Could not verify / not found
- Ibrutinib protein-binding-corrected CSF penetration (28.7-43.4%): only in a trial-protocol PDF summary (NCT05211336), not the primary paper.
- Topotecan and pemetrexed CSF ratios: web-search summaries; primary papers not opened.
- Carmustine CSF 15-70%: drug monograph, not a primary PK paper; FDA BiCNU label not opened.
- Procarbazine: no numeric CSF or Kp,uu value in any source read; cycle dependence and P-gp status not found.
- Dexamethasone dog CSF (944876): Japanese paper, abstract only, tritium radioactivity (parent + metabolites), total plasma.
- Lomustine CSF in dogs, thiotepa PK in dogs, acalabrutinib CSF: NOT FOUND.
- No measurement in Gd-non-enhancing LYMPHOMA for any agent; the MTX and TMZ numbers are glioma / peritumoral tissue (indirect, rule 10).
- Canine CNS-lymphoma outcome series beyond the record (LaRue 30022475, nimustine 37756055): none new found (PubMed 2023+ search: 3 hits, all in record).


### High-dose IV methotrexate [NEW: rule-14 proxy measurement in NON-ENHANCING tissue]
- Blakeley 2008/9 J Neurooncol (PMID 18787762; PMC4029102 read): MTX 12 g/m2 4-h IV, microdialysis in recurrent high-grade glioma, probe in
  contrast-ENHANCING tumour (2 pts) vs NON-ENHANCING tissue (2 pts). Brain ECF Cmax 380/407 uM (enhancing) vs **22/24 uM (non-enhancing)**;
  AUC_ECF/AUC_plasma 0.281/0.305 vs **0.032/0.094**; ECF >2 uM "for 20-26 h in both regions"; MTX 54-59% bound (so non-enhancing
  **Kp,uu ~0.07-0.21**, my arithmetic). n=4 evaluable; glioma, not lymphoma (indirect: same barrier phenotype is the point of the proxy).
- This is the first barrier-intact (non-enhancing) concentration for any lymphoma agent; the record (LYMPHOMA_UNIVERSE l.305, SWEEP_outside_model
  item 5) says none exists -> that statement is now superseded for MTX (glioma tissue).
- Potency: canine MTX IC50 2-3 nM (secondary citation, flagged in LYMPHOMA_STATUS l.298); CL-1 most sensitive (28992489 [REC]). 22 uM is
  ~10^4 x that, for ~1 day per dose -> kill of CYCLING cells in the non-enhancing edge is not exposure-limited.
- Limits: S-phase-specific (division-gated) -> does not reach E5 dormant cells; defeated by **E9** (RFC loss; RFC promoter methylation in
  30% of PCNSL, 15327516 [REC]); MTX is a weak BCRP/MRP substrate (not re-verified). Dog: 12 g/m2 with leucovorin rescue and urine
  alkalinisation has NO canine series found (see below); lawful (approved human drug).
- Verdict: closes the BULK, cycling, RFC-intact brain edge with measured access; it is the SAME mechanism and SAME escape (E9) as the
  intrathecal MTX already in the program, so it is not an independent route against E9 or E5.

### Topotecan / pemetrexed [NEW; web-search level, primary not opened]
- Topotecan: CSF/plasma lactone ~0.29 (24 h) to 0.42 (72 h) in children on continuous infusion; ~20% of total plasma in a phase I; NHP 32%
  (search summaries of PMIDs 20107803 and related; NOT verified against primary). Topoisomerase-I poison, S-phase-dependent; BCRP and
  P-gp substrate (class knowledge, not re-verified) -> defeated by the pump escape and by quiescence. Not a candidate.
- Pemetrexed: CSF <5% (clinical) or <2% (review) of plasma; rat unbound brain/plasma AUC 0.078 (PMID 15987831, abstract-level via search).
  Enters via RFC -> defeated by E9 exactly like MTX. Not a candidate.

### Carmustine (BiCNU) [label-level only]
- BC Cancer monograph: CSF 15-70% of concurrent plasma; label: CSF radioactivity >=50% of plasma (web search summary; FDA label not opened).
  Plasma t1/2 beta 18-69 min. NCI-60 14-33 uM, no P-gp cross-resistance [REC]. MGMT is the named escape; BCNU/CY minimal effect on late
  quiescent HSC (7917905 [REC]); lomustine is the oral member of the same class already in the catalogue. Canine carmustine PK NOT FOUND
  [REC]. Role: conditioning partner of thiotepa (in record), not a stand-alone brain route.
