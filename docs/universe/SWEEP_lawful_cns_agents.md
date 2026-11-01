# Lawful CNS agents for the canine B-cell brain sanctuary (sweep 2026-11-01) -- WORKING DRAFT, written incrementally

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
- Alkylator (phosphoramide mustard): dCK/RFC-independent; not P-gp-limited by class (not verified); dormant-cell kill not shown.
  Neurotoxicity (encephalopathy, chloroacetaldehyde) and nephrotoxicity are the budget axes; dog use: sarcoma, 375 mg/m2 with mesna
  (not verified this sweep).

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
