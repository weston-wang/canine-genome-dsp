# IT-MTX derivation sweep 2 (agent notes, 2026-10-06) -- extends docs/universe/SWEEP_nm600_itmtx.md
Record check basis: SWEEP_nm600_itmtx.md sections B + DERIVATION; LYMPHOMA_UNIVERSE.md J.2/J.3, K.2/K.3.
Already in record: 28992489 (title/abstract only, NO numbers), 31561563 (secondary 2-3 nM), 6109397 (ID50 118/122/28 nM),
581360 (dog cisternal t1/2 5.20 h), 25041580 (112 dogs safety), 37732143 (dog IT case, 2.5 mg MTX), 2809687 (human intra-Ommaya),
9347977, 38416167, 31657981, 39269476, 9920857, 36230611, 25017328, 32989105.

## 1. Canine MTX IC50 -- primary verification
- PMID 28992489 (Pawlak 2017, Res Vet Sci 114:518-523, doi 10.1016/j.rvsc.2017.09.026): ABSTRACT RE-VERIFIED this pass.
  Lines: CLBL-1, GL-1, CL-1. "most methotrexate sensitive cells belonged to CL-1 cell line derived from T CELL NEOPLASIA
  and previously characterized by high resistance to the majority of anticancer drugs". NO IC50 NUMBER, NO EXPOSURE TIME,
  NO ASSAY NAME in the abstract. FULL TEXT: sciencedirect 403 (paywalled); not in PMC (no PMCID in PubMed record).
  => the 2-3 nM remains SECONDARY-ONLY.
- PMID 31561563 (Cancers 2019, PMC6827003) full text READ this pass. Exact sentence: "Canine lymphoma cell lines were found
  to be 10 times more sensitive to MTX (IC50 values of 2-3 nM) than the human Raji B cell lymphoma and Jurkat T-ALL cell
  lines [ref=Pawlak 2017]." So the secondary statement is confirmed verbatim, AND it implies Raji/Jurkat IC50 ~20-30 nM
  (same source, same comparison). That paper's own IC50s are for the B5/B5-MTX ANTIBODY (5-6.25 nM vs 9.53-11.5 nM),
  48 h, propidium-iodide viability by flow cytometry -- NOT free MTX.
- PMID 6109397 (Torres 1980, Virchows Arch B 33:139-53, doi 10.1007/BF02899177) RE-VERIFIED from the PubMed abstract this pass:
  canine lymphoma lines DT-5 / 11028 / 11028+FeLV MTX **ID50 118 / 122 / 28 nM**; generation time 15.2 / 13.6 / 11.2 h;
  S-phase 8.2 / 7.7 / 8.3 h; at ID50 TC prolonged ~2 h via S-phase lengthening. Lineage of DT-5 / 11028: NOT STATED (1980 lines,
  pre-immunophenotyping). So "T-lineage canine MTX IC50 measured" = CL-1 only, and that number is not in any text I could open.
- LINEAGE of the named lines (from the sources read this pass): CL-1 = T-cell neoplasia (28992489 abstract, explicit);
  CLBL-1 = B-cell DLBCL and CLB70 = B-CLL (31561563 full text, explicit); GL-1 = DLA-DR-NEGATIVE, used as the B-negative control
  (31561563). 17-71 / OSW / Ema / UL-1 / 3132: NOT addressed by either paper -- no IC50 and no lineage statement found this pass.
- HUMAN T-LINEAGE / LYMPHOID MTX IC50 for an explicit written transfer (all MEASURED, primary abstracts verified this pass; NEW to record):
  * PMID 10568835 (McGuire 1999, Int J Oncol 15:1245-50, doi 10.3892/ijo.15.6.1245): **CCRF-CEM (human T-ALL) MTX EC50 = 14 nM**
    under 120-h CONTINUOUS exposure. Same paper: 24-h intermittent MTX EC50 0.3 uM (FaDu) to 17 uM (A253) -- i.e. a PULSE is
    ~20-1000x weaker than continuous exposure in the lines where both were measured. Exposure duration is the dominant variable.
  * PMID 12854905 (Wang/O'Connor 2003, Leuk Lymphoma 44:1027-35, doi 10.1080/1042819031000077124): 5-day continuous exposure,
    **MTX IC50 = 30-50 nM** in 5 human lymphoma lines (RL, HT, SKI-DLBCL-1, Raji, Hs445); pralatrexate 3-5 nM.
  * PMID 9920857 (Rots 1999, Blood 93:1067-74; already in record): no absolute TSI50 in the abstract; T-ALL 3.4x more MTX-resistant
    than c/preB-ALL after a 3-h pulse + 18-h washout (p=.001), no difference after 21-h continuous (p=.46). MTT shows no MTX kill at all
    (nucleoside rescue) -- so every in-vitro MTX "IC50" is a CYTOSTATIC/TS-inhibition bar, not a kill rate.
  * PMID 20668838 (Youns 2010): IC50s for MTX in 5 T-ALL lines (Jurkat, J-Jhan, J16, HUT78, Karpas 45) exist but are NOT in the abstract;
    paper not opened (Springer).
  => RECOMMENDED GRADE: canine-line MTX IC50 **2-3 nM = SECONDARY, unverifiable** (primary paywalled, no PMC). Use a
  TRANSFERRED planning range **14-120 nM** (human T-ALL CCRF-CEM 14 nM continuous; human lymphoma lines 30-50 nM; canine lines
  28-122 nM ID50) and show the closure at the TOP (worst) end. See section 4: the derived kill is nearly IC50-independent.

## 2. Dog CSF volume + intrathecal MTX PK (what is measured IN THE DOG)
- **CSF VOLUME, MEASURED IN DOGS, NEW to record and it replaces every assumed value:**
  * PMID 28244335 (Reinitz 2017, Acta Vet Hung 65:1-12, doi 10.1556/004.2017.001) -- full text obtained as PDF and read.
    12 healthy male mongrels, 3-5 y, 7.5-35.0 kg; 1.5 T 3D SPACE MRI, semiautomatic segmentation, phantom accuracy 99.96% /
    99.8 +/- 3.1%. INTRACRANIAL: ventricular 0.97-2.94 mL; IC subarachnoid 8.44-22.62 mL; TOTAL IC CSF per dog 9.41 mL (13 kg),
    10.93 (16.5), 11.69 (14), 11.82 (13), 11.85 (19), 13.80 (19), 14.04 (7.5), 14.16 (26), 14.57 (20), 16.72 (20.2), 21.65 (26.5),
    23.68 (35). Eq 1: V_ICSA = 0.62*BW + 0.12 (adj r2 0.468).
    **Eq 2 (IC + extracranial combined): V_TOTAL (mL) = 1.39 x BW(kg) + 17.5, adj r2 = 0.836, P = 1.94e-5.**
  * PMID 26311617 (Reinitz 2015, Vet Radiol Ultrasound 56:658-65, doi 10.1111/vru.12283): same 12 dogs, EXTRACRANIAL (spinal) CSF
    **20.21-44.06 mL**, MRI accuracy 99.8% against phantoms; proportional volume (mL/kg) falls with body weight.
  => dog total CSF: 13 kg 35.6 mL, 20 kg 45.3 mL, 30 kg 59.2 mL (Eq 2). The record's "assume 30 mL" and the
     "V_dog = V_human apparent (31 mL)" of the last pass are both LOW by ~1.2-1.5x; 20 kg dog = 45 mL. MEASURED, n=12, one lab.
  * Dickson 2007's "approximately 20 mL of CSF in an MPS I dog" (PMC3009387, read) carries **NO citation** -- it is an uncited
    working figure, not a measurement. Do not use it.
- **CSF production/turnover, MEASURED IN DOGS (NEW):** PMID 6846881 (Artru 1983, Anesth Analg 62:581-5) open ventriculocisternal
  perfusion: **0.047 +/- 0.006 mL/min** awake-equivalent control; **halothane 0.8% cuts it to 0.033 +/- 0.005** (persisted 3-3.5 h,
  reversible in 45-50 min); fentanyl no change. PMID 1119314 (Sato/Bering 1975, Acta Neurol Scand 51:1-11) inulin bulk-flow
  perfusions, dogs 12-17 kg: **total CSF formation 0.065 mL/min**, 58.5% from extraventricular space, pressure-independent.
  => 68-94 mL/day; against V_total 36-45 mL that is **1.5-2.6 CSF turnovers/day** (my arithmetic). Note anaesthesia (every IT dose in a
  dog is under GA) REDUCES production ~30%, which lengthens drug residence -- conservative to ignore.
  Yaksh (PMC3514653, read) states the dog CSF-turnover half-life "has been calculated to be on the order of approximately 2 hr";
  MTX's measured dog CSF t1/2 of 5.2 h is LONGER than bulk turnover, consistent with its reported probenecid-sensitive active efflux.
- **MTX CSF PK in the dog:** PMID 581360 (Ramu 1978, Cancer Treat Rep 62:1465-70) abstract re-verified: DOGS, INTRACISTERNAL MTX,
  CSF + plasma followed 72 h, biexponential, second-phase half-disappearance **5.20 +/- 0.89 h** (7.09 +/- 0.23 h with probenecid);
  plasma 7.60 h (11.32 h with probenecid). **The DOSE, the n, and the peak CSF concentration are NOT in the abstract and the full text
  could not be opened (1978 Cancer Treat Rep; no PMC, no DOI).** Companion papers PMID 731407 (no abstract) and 582316 (model only).
  So the dog contributes the CLEARANCE RATE only; the peak must come from dose/volume arithmetic.
- **Human measured anchor (unchanged):** PMID 2809687, 6 mg intra-Ommaya, peak 423 uM, 4.6 uM at 24 h, 1.05 uM at 48 h, t1/2 5.7 h
  => apparent mixing volume 31.2 mL (my arithmetic) = 21% of the 150 mL human total; 24->48 h tail t1/2 = 11.3 h (my arithmetic).
- **Clinical dog IT dose:** PMID 25041580 (Genoni 2014) abstract re-verified: 112 dogs + 8 cats, IT cytarabine alone or with MTX,
  Sept 2008-Dec 2013, SHORT-TERM safety only, 1 of 120 animals had a generalised seizure during anaesthetic recovery (diazepam-responsive).
  **The abstract does NOT state the dose or the route**; the 2.5 mg MTX + 100 mg cytarabine flat dose, cisterna magna, 1 mL CSF withdrawn,
  injected over 1 min under GA, comes from PMID 37732143's full text (PMC10507905) citing Genoni -- i.e. the dose is SECONDARY,
  though from a paper by the same hospital. Genoni full text still not opened (Wiley 403).

## 3. Re-derivation of the dog CSF exposure and the time-averaged kill (script: scratchpad/mtx2.py, all arithmetic mine)
Inputs and their grades:
| input | value | grade |
|---|---|---|
| dose | 2.5 mg MTX flat, cisterna magna, under GA | SECONDARY (37732143 citing 25041580) |
| MTX MW | 454.44 => 2.5 mg = 5.501 umol | definitional |
| dog total CSF volume | 1.39*BW + 17.5 mL (20 kg -> 45.3 mL) | **MEASURED IN DOG** (28244335 + 26311617) |
| dog intracranial CSF | 0.62*BW + ~1.7 mL (20 kg -> 14.1 mL) | **MEASURED IN DOG** |
| dog CSF MTX terminal t1/2 | 5.20 h | **MEASURED IN DOG** (581360) |
| slow-tail alternative | 11.3 h (human 24-48 h segment) | TRANSFERRED/EXTRAPOLATED |
| mixing fraction | full mix in V_total (conservative) / IC-only / human-like 21% | ASSUMED, bracketed |
| IC50 | 14-120 nM transferred (2.5 nM secondary) | TRANSFERRED |
| formula | k = min( ln(1+C/IC50)/assay_days , cap ) time-averaged over the interval; `lymphoma_pkpd.emax_kill_rate` | model |
| assay_days | 2 (as the model uses) or 5 (matches the 120-h continuous human IC50) | ASSUMED / matched |
| cap (cycling-cell rate) | 0.45 (slow) to 0.88 /day | record, SWEEP_growth_bar D1 |

Peak CSF concentration after 2.5 mg (my arithmetic): 20 kg dog **121 uM** full mix in 45.3 mL / 390 uM if it mixes only in the
intracranial 14.1 mL / 578 uM at the human-like 21% mixing fraction. (13 kg: 155 / 563 / 736 uM.) The last pass used 176 uM --
inside this bracket. Human measured peak 423 uM after 6 mg. **Even the most conservative case is 1,000-50,000x the IC50 range.**

Time above threshold, 20 kg dog, full mix, t1/2 5.2 h: C > 25 nM for 63.7 h (2.7 d), > 118 nM for 52.0 h (2.2 d),
> 2.5 nM for 80.9 h (3.4 d). With the 11.3 h tail: 138 h (5.8 d) / 113 h (4.7 d) / 176 h (7.3 d).

**Time-averaged kill per dosing interval (/day), 20 kg dog, conservative full mixing, dog-measured t1/2 5.2 h:**
| IC50 | assay_days, cap | weekly | 2-weekly | 3-weekly | 4-weekly |
|---|---|---|---|---|---|
| 25 nM | 2, 0.88 | 0.332 | 0.166 | 0.111 | 0.083 |
| 118 nM | 2, 0.88 | 0.271 | 0.135 | 0.090 | 0.068 |
| 2.5 nM | 2, 0.88 | 0.422 | 0.211 | 0.141 | 0.106 |
| 25 nM | 5, 0.45 | 0.162 | 0.081 | 0.054 | 0.040 |
| 118 nM | 5, 0.45 (WORST) | 0.130 | 0.065 | 0.043 | 0.033 |
With the 11.3 h tail instead (same full mixing, IC50 25 nM, ad 2): weekly 0.713, 2-weekly 0.360, 3-weekly 0.240, 4-weekly 0.180.

**The single most important result: the derived kill is almost IC50-INDEPENDENT.** Going from 2.5 nM (the weak secondary number)
to 118 nM (the worst measured canine line) changes the time-averaged kill by only ~1.5x, because the peak is 3-5 log10 above IC50
and the ln(1+C/IC50) term is logarithmic. What actually sets the number is the DOSING INTERVAL (linear) and the clearance tail.
=> the "weak input (1)" is NOT load-bearing for the brain closures. The load-bearing inputs are the interval and the mixing/tail.

**Implied interval for the model's 0.12 /day:** every 2-3 weeks under the mid assumptions (IC50 25 nM, ad 2, cap 0.88 -> 0.111 at
3-weekly, 0.166 at 2-weekly), i.e. 26-30 doses over 13 months, which matches section J.2's "28 to 36 doses". Under the WORST
combination (IC50 118 nM, assay_days 5, cap 0.45, dog t1/2, full mixing) 0.12 /day needs **weekly** dosing = 52-61 doses over
12-14 months. Under the slow-tail case even monthly dosing (13-15 doses) clears 0.12. So the honest statement is:
**0.12 /day is between every-week and every-3-weeks depending on mixing and tail; 2-weekly is the mid-case, and the dose count the
program must fund is 26-61, not 20-30.**
All of it remains a kill of CYCLING cells in the CSF/perivascular compartment only (division-gated), unchanged from the record.

## 4. Repeated / long-term intrathecal dosing in dogs -- the practical crux (ALL NEW to the record)
| precedent | what was actually done | complications |
|---|---|---|
| **PMID 17321776 / PMC3009387** (Dickson 2007, MPS I dogs, IT rhIDU; full text read) | **CISTERNA MAGNA puncture, 22 G spinal needle, propofol + isoflurane GA, 0.5-1.0 mL CSF withdrawn then 2.3 or 6.9 mL injected; monthly x4 over 4 months, or quarterly x3 over 6 months; 19 treated dogs, ~56 injections in the study** | per-injection: hyperventilation in 10 dogs, twitching 5, seizures 5 (diazepam-responsive); **1 dog died of a brainstem haematoma during the injection** |
| **PMID 25257657** (Vuillemenot 2014) + **PMC4263309** (Katz 2014, both read; the second is open access) | TPP1-null Dachshunds implanted at ~4 months with **two catheters to SUBCUTANEOUS TITANIUM ACCESS PORTS** -- one to a lateral ventricle (dosing), one to the L5 subarachnoid space (serial CSF sampling); infusions **every other week** from ~2.5 months of age until end-stage at **51-67 weeks of age** => **~20-28 biweekly CSF-route doses per dog over 8-11 months** (my arithmetic from the stated ages; the papers give no cumulative count; one dog is described as having "15 subsequent biweekly infusions" during escalation to 48 mg) | **2 dogs developed meningitis + obstructive hydrocephalus early and were euthanised**; ICV catheters occluded or migrated into parenchyma; ITL catheters "often became occluded"; one catheter-track lesion causing obstructive hydrocephalus |
| **PMID 24694254** (West 2014, J Invest Surg 27:226-33) | **chronic LUMBAR intrathecal catheter + VASCULAR ACCESS PORT in conscious dogs** for repeated CSF collection, 3.5 Fr open-ended polyurethane catheter | patency **67% beyond 30 days** after the first surgery, **86% beyond 30 days** if repaired/replaced -- so the port route needs revision surgery in a third of dogs by one month |
| PMID 12826858 / 16931994 (Yaksh, Anesthesiology) + PMC3514653 | beagles with chronic lumbar IT catheters, vest pumps, **28 days of continuous IT infusion**; all 5 dogs in the PK study completed the protocol with patent catheters | morphine >=9-12 mg/day produced **intradural inflammatory granulomas with cord compression in 100% of dogs** (drug-specific, not procedural); saline and fentanyl none |
| PMID 36906911 (Fentem 2023, Vet Rec 193:e2787) | prospective multicentre, **102 dogs, 108 CSF collections** (cerebellomedullary and/or lumbar) | CSF obtained on 100/108 (92.6%); **no dog deteriorated neurologically**; no pain-score change |
| record (SWEEP_nm600_itmtx B) | the previous longest IT-chemo precedent: 6 doses twice weekly in 1 dog (anecdote via 37732143's reference 13), 112 single doses (Genoni) | 1 dog died of tentorial herniation after IT chemo (same reference, "believed") |
| PMID 36382395 (Beckmann 2022, JVIM 37:204) + 38519448, 26704658 | **ventriculoperitoneal shunts are established in dogs**: 12 dogs/cats with intraventricular tumours, VPS+RT median survival **1103 days**; one dog carried a VP shunt 18 months then a second shunt and was neurologically normal at 40 months | VPS complications in 4/6, all but one managed surgically; shunt infection/blockage/mechanical failure are the known modes (26704658) |
=> **FEASIBLE ROUTE FOR 20-60 DOSES: an implanted ventricular (or lumbar) catheter to a subcutaneous port -- and this exact
configuration has been run in dogs for 8-11 months at a biweekly interval (Katz/Vuillemenot).** It is NOT free: 2/9-ish dogs lost
to meningitis + hydrocephalus, frequent catheter occlusion/migration, and a third needing port revision by 30 days (West).
Repeated percutaneous cisternal puncture is documented only to 4 doses over 4 months (Dickson) and 6 doses over 3 weeks (anecdote),
with a fatal brainstem haematoma in 1/19 dogs; per-puncture risk is low (Fentem 0/108 deteriorations) but not zero, and 30-60
anaesthetics is its own burden. **Ommaya use in a dog: still NOT FOUND. Canine arachnoiditis or myelopathy specifically after
intrathecal chemotherapy: NOT FOUND (no canine report; the granuloma data are opioid-infusion, the human data are in the record).**

## 5. The human outcome anchor (verified in the primary this pass)
PMID 31657981 (Jeha 2019, JCO 37:3377, PMC7351342; abstract + PMC text read):
- 598 consecutive children, 2007-2017, St Jude Total Therapy 16, risk-directed chemo **with NO prophylactic cranial irradiation**.
- **Cumulative risk of any CNS relapse 1.5% (95% CI 0.5-2.5)**; isolated CNS 1.3%; only 8 CNS events. 5-y EFS 88.2%, OS 94.1%.
- **T-cell phenotype was the only independent risk factor for CNS relapse, HR 5.15 (1.3-20.6), p=.021.**
- **Dose counts (the real-world precedent for repeat dosing): "Patients with low-risk ALL received a total of 13 to 21 intrathecal
  treatments, and those with standard-risk ALL received 16 to 27 treatments"** over ~2.5 years of therapy. High-risk features got
  2 extra IT doses in the first 2 weeks (days 4, 8, 11, 22) -> CNS relapse 1.8% vs 5.7% in TT15 (p=.008), with no excess seizure/infection.
- **Eradication, not just control, of ESTABLISHED CNS disease: only 1 of 21 children who were CNS-3 at diagnosis (blasts in CSF)
  had an isolated CNS relapse** -- under IT therapy plus systemic high-dose MTX, no cranial RT. That is the strongest available
  evidence that IT therapy can clear lymphoid disease from the CSF compartment rather than merely suppress it; it is still a
  COMBINED-modality result (systemic HD-MTX + 13-27 IT doses), never IT alone.
- Counter-evidence already in record and unchanged: in mature T-cell lymphoma (PTCL/NK-T), IT prophylaxis did not change CNS rates
  (27046135) and median OS after CNS relapse is 2.6-17 mo (27046135, 35646641, 34061378). The ALL anchor transfers to a
  LYMPHOBLASTIC/T-ALL-like presentation, which is what the brain cases model.

## 6. What remains unmeasured after this pass
1. The canine T-line MTX IC50 primary numbers (Pawlak 2017 is paywalled, no PMC, no repository copy found). Mitigated: the derived
   kill is nearly IC50-independent over 2.5-120 nM, and human T-ALL CCRF-CEM 14 nM / lymphoma 30-50 nM give a written transfer.
2. The DOSE and the measured CSF PEAK in the only dog IT-MTX PK study (581360, 1978) -- full text unobtainable. Only its t1/2 is usable.
3. Genoni's own dose/route statement (Wiley 403); the 2.5 mg flat dose rests on Lyseight's citation of it.
4. Mixing fraction after a cisternal bolus in a dog: no dog has had cisternal and lumbar MTX measured simultaneously. The nearest
   measurement is Yaksh's LUMBAR-to-cisternal ratio for a 2.5 kDa peptide, 1:0.017 at steady state (PMC3514653) -- which says a
   LUMBAR injection barely reaches the brain CSF and is an argument for dosing CISTERNALLY (as dogs are dosed) or intraventricularly.
5. No canine series of whole-brain radiation PLUS repeated intrathecal methotrexate (unchanged); late canine leukoencephalopathy
   after either remains unmeasured.
6. Nothing newer than 2023 on IT chemotherapy in dogs: PubMed "intrathecal dogs lymphoma methotrexate" returns exactly 1 record (37732143).
