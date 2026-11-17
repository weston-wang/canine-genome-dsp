# Prior art per escape: has anyone measured it in a dog, and has anyone ever treated it?

Date 2026-11-16. Scope: the 23 escapes of the canine multicentric lymphoma model, plus the CNS sanctuary as a
site. This file answers four questions the record does not hold: **(i)** is the mechanism measured in canine
lymphoma, naive versus relapsed; **(ii)** has any treatment been chosen deliberately to counter it **in dogs**;
**(iii)** has it been deliberately countered in **human lymphoma practice** (the transfer anchor); **(iv)** can a
practising veterinary oncologist measure it today. It is the lymphoma analogue of the HS branch's
`docs/PRIOR_ART_COMBINATIONS.md`, which `LYMPHOMA_STATUS.md` line 50 lists as "Not covered here yet".

## 0. Bar, record check, method

**Success criteria quoted (CLAUDE.md rule 2), graded against exactly these:**
- Task: "has anyone measured this mechanism in dogs, and has any treatment ever been chosen deliberately to
  counter it -- in dogs, or in human lymphoma practice?"
- "Where a mechanism has no canine data, say so as a fact about the literature, not as a criticism of the model."
- Standing standard: "I'm not asking if it's been demonstrated, I know it's not." So **absence of a canine study
  or of a canine treatment is reported here as a property of the published literature, never as a gap in the
  model.** Nothing in this file is an input to closure and nothing here changes a grade in
  `lymphoma_standard_audit`. Under rule 11 this file is prior art, not an audit.

**Record check (rule 1). Read in full before searching:** `docs/universe/SWEEP_escapes.md` (the independent
escape audit, 157 lines, which already holds the DOG / HUMAN / THEORY evidence tier per escape),
`docs/LYMPHOMA_COVERAGE_LEDGER.md`, `docs/LYMPHOMA_UNIVERSE.md`, `docs/LYMPHOMA_STATUS.md`, plus `git grep` of
all four branches for `assay|flow cytometr|immunohistochem|commercial|PARR|valspodar|verapamil|prior art`.
Result of that grep: **the record holds no "has anyone treated it" and no "is it assayable" information for any
escape.** The one exception is the valspodar trial (`LYMPHOMA_COVERAGE_LEDGER.md:204`,
`LYMPHOMA_STATUS.md:76`). So every row below is labelled on the measurement side (ALREADY IN RECORD, with
file:line) and on the prior-art side (almost always NEW).

**Row index into the record**, so no row is re-raised as new evidence:
| escape | measurement already in record at |
|---|---|
| 1-14 (the original list) | `docs/universe/SWEEP_escapes.md:99`-`:112` (one numbered paragraph each); `docs/LYMPHOMA_COVERAGE_LEDGER.md:272`-`:282` |
| E1-E10 (the audit's additions) | `docs/universe/SWEEP_escapes.md:34`-`:43` (Table A); `docs/LYMPHOMA_UNIVERSE.md:58`-`:67` |
| CNS sanctuary | `docs/LYMPHOMA_STATUS.md:14`, `:387`; `docs/LYMPHOMA_UNIVERSE.md` sections D-M |

**Verification.** Every PMID below was fetched from PubMed in this session unless marked
"(record)" (carried from `SWEEP_escapes.md`'s verified list, not re-fetched) or "(web)" (vendor or news source,
no PMID exists). "Searched, not found" means my queries returned nothing whose abstract supports the claim; it
does not mean the thing is absent from the literature. Sources: PubMed (NCBI); DOIs as returned by PubMed.

---

## 1. The 23 escapes, one row each

### 1. P-glycoprotein / ABCB1 efflux
- **Measured in dogs?** Yes, more thoroughly than any other escape, **including naive versus relapsed**.
  **PMID 8646690** (Lee 1996, *Cancer*, [DOI](https://doi.org/10.1002/(SICI)1097-0142(19960501)77:9<1892::AID-CNCR20>3.0.CO;2-U)):
  91 canine lymphomas (76 retrospective + 15 prospective) stained with anti-human Pgp clones C494 and C219 --
  61/91 (67%) negative, 16/91 (17.5%) strong in >50% of cells, 14/91 (15.5%) positive in 10-50%. **Pgp
  expression was higher after relapse than before treatment: 83% vs 25% (C494, p=0.012) and 73% vs 27% (C219,
  p=0.04)**; pretreatment Pgp was an independent negative predictor of overall survival (225 vs 367 d, p=0.02).
  **NEW** -- the record cites 25475167 and 36010910 (47% high activity in 79 dogs, not predictive) but holds no
  paired naive-vs-relapse comparison. Supporting: **PMID 29958524** ([DOI](https://doi.org/10.1556/004.2018.028))
  33 untreated dogs, 18/33 (54.5%) Pgp-positive, T-cell types stained more intensely, Pgp >=35% gave OST 240 d
  vs 428 d and relapse-free 95 vs 232 d; **PMID 23535752** ([DOI](https://doi.org/10.5326/JAAHA-MS-5843)) 31
  untreated dogs, 24/31 (80%) Pgp-positive, not associated with remission or survival; **PMID 23834200**
  ([DOI](https://doi.org/10.1111/vco.12051)) blood MDR1 RT-PCR in 27 dogs, the 4 dogs with >2-fold
  up-regulation during treatment were the only ones to progress.
- **Treated deliberately in dogs?** **Yes, once, in a randomised trial, and it failed.** **PMID 28357033**
  ([DOI](https://doi.org/10.12688/f1000research.6055.3)): valspodar (PSC833, a selective ABCB1 inhibitor) 7.5
  mg/kg twice daily for 5 days neoadjuvant, then 5 doxorubicin doses; 20 dogs, double-blind, placebo-controlled;
  no difference in event-free or overall survival. Already in record at `LYMPHOMA_COVERAGE_LEDGER.md:204`.
  Also in dogs: a P-gp / TGF-beta-inhibitor chemosensitiser is listed as "trial in dogs, MECHANISM, no kill rate"
  (`LYMPHOMA_COVERAGE_LEDGER.md:132`). In vitro only: verapamil and fumitremorgin C failed to shift the canine
  side population (PMID 23820219, record).
- **Countered in human lymphoma practice?** **Attempted across two decades and abandoned.** **PMID 20716770**
  (ECOG 3999, *Blood* 2010, [DOI](https://doi.org/10.1182/blood-2010-04-277269)): zosuquidar 550 mg vs placebo
  added to cytarabine/daunorubicin in 449 adults; median OS 7.2 vs 9.4 months, 2-year 20% vs 23%, p=0.281;
  remission 51.9% vs 48.9%. **PMID 19949935** ([DOI](https://doi.org/10.1007/978-1-60761-416-6_19)): cyclosporin A
  reversal was positive in phase II in myeloma and acute leukaemia but "less convincing" in phase III; PSC833
  was tenfold more potent but "required reductions in the dose of the concurrently administered anticancer
  agents". **No P-gp modulator is in human lymphoma practice.**
- **Why nobody targets it now (reasons stated in sources).** (i) Futility attributed to a competing mechanism:
  "zosuquidar did not improve outcome in older acute myeloid leukemia, in part, because of the presence [of]
  P-gp independent mechanisms of resistance" (20716770). (ii) Pharmacokinetic interaction forcing dose reduction
  of the partner cytotoxic (19949935). (iii) In dogs, a null randomised result (28357033) and expression that
  does not predict outcome (36010910, 25475167, 23535752).
- **Assayable in practice today?** Partly. Pgp immunohistochemistry with the human C494/C219 clones works on
  canine formalin-fixed tissue (8646690, 29958524, 23535752) and veterinary histopathology laboratories can run
  it on request, but **no standardised cut-off exists** (29958524 proposes 35%; 23535752 found no prognostic
  effect at all). Germline *ABCB1-1Delta* (MDR1) genotyping is a widely sold canine test and is reported as a
  pharmacogenomic marker on the 120-gene SearchLight DNA panel (web, Vidium/Antech) -- but that is a **host
  toxicity** test, not a tumour-resistance test. Tumour MDR1 mRNA (23834200) and rhodamine-efflux activity
  (36010910, record) are research assays.

### 2. BCRP / ABCG2 efflux
- **Measured in dogs?** Yes, but only as lineage-restricted mRNA change. **PMID 25475167** (record): 63 dogs,
  drug resistance in 35/63 (55.6%); ABCG2 up-regulation seen **only in the T-cell subset** (ABCB1 up in a B-cell
  subset); pre-treatment ABC expression not predictive. **PMID 23820219** (record): the canine side population
  expresses ABCG2 and phospho-P-gp. No paired naive-vs-relapse ABCG2 protein series found. ALREADY IN RECORD
  (`SWEEP_escapes.md:100`), including the finding that the model's single `efflux_substrate` flag hides the
  ABCB1/ABCG2 split.
- **Treated deliberately in dogs?** **None found.** Fumitremorgin C (a BCRP inhibitor) was used in canine cells
  in vitro and did not reduce the side population (23820219); valspodar, the only reverser given to dogs, is
  described in its own trial as "a selective inhibitor of the ATP binding cassette B1 transporter" (28357033), so
  the one canine reverser trial did not address BCRP at all.
- **Countered in human lymphoma practice?** **None found.** No BCRP inhibitor has reached licensed oncology
  practice in any indication.
- **Why nobody has.** No reason stated for BCRP specifically in the lymphoma literature. The only
  transferable stated reason is the class-wide one from 20716770 (efflux inhibition did not improve outcome
  because resistance is efflux-independent in part).
- **Assayable in practice today?** **No.** No commercial canine BCRP/ABCG2 test found; detection is by research
  antibody or qPCR.

### 3. TP53 / intrinsic-apoptosis evasion
- **Measured in dogs?** Yes, by four methods, and it is now on a commercial panel. **PMID 26678182** (record):
  7/43 (16%) p53-mutant by SSCP of exons 4-8; response 33% vs 88%, OS 67 vs 264 d. **PMID 39282821** (record):
  p53 IHC-positive in 27% of 37 dogs, IHC predicting mutation with 97.3% accuracy, but not significant in
  multivariable analysis against treatment. **PMID 39922874** (record): 25.6% by whole-genome sequencing, n=43,
  founder-clonal. **PMID 23535752**: 7/31 (22%) p53 IHC-positive in untreated dogs, and p53 "was statistically
  correlated with survival". **NEW: PMID 39134766** (*Sci Rep* 2024, [DOI](https://doi.org/10.1038/s41598-024-69716-6)),
  the 31-gene "K9 lymphoma assay": "TP53 mutations demonstrated universal adverse prognostic implications across
  B-cell lymphomas". **Naive versus relapsed: not measured** -- no paired canine diagnosis/relapse sequencing
  exists (`SWEEP_escapes.md:131`).
- **Treated deliberately in dogs?** **None found.** No canine study assigns, withholds or escalates a drug on
  p53 status. 39134766 argues for "tailored therapeutic approaches based on the genetic profile" but reports no
  treatment assignment.
- **Countered in human lymphoma practice?** **Yes, but in CLL rather than in large-cell lymphoma.** In CLL,
  TP53 disruption / del(17p) is routinely tested and routinely diverts therapy away from chemoimmunotherapy to
  BTK- and BCL2-inhibitor based regimens and, on later failure, to CD19 CAR-T (TRANSCEND CLL 004); detection rises
  from roughly 5-10% at diagnosis to over 30% at relapse (web review sources). In **DLBCL** TP53 is a
  poor-prognosis marker that does not formally select an agent, and the CAR-T data are inconsistent -- a cohort
  in the CAR-T era found worse outcomes (PMID 34830747, title/metadata only) while a 29-patient single-centre
  series found no effect (web). So the transfer anchor is real but is a CLL practice, not a DLBCL one. Record
  already holds the human relapse genetics (32589730: TP53 and KMT2D clonally persistent from diagnosis).
- **Why nobody targets it in dogs.** **No reason stated in the literature.** Two facts in the sources bear on
  it: there is no canine agent whose selection turns on p53, and p53 IHC lost significance once treatment was
  in the model (39282821).
- **Assayable in practice today?** **Yes -- the best-covered escape of the 23.** p53 IHC on canine
  formalin-fixed tissue is offered by veterinary histopathology services and concords with mutation at 97.3%
  (39282821). TP53 is on the 31-gene K9 lymphoma NGS panel (39134766, co-authored from a commercial diagnostic
  laboratory), on the 308-gene canine panel used in 238 dogs (PMID 40506464, record), and on the 120-gene
  SearchLight DNA panel distributed in North America by Antech (web; 482,000 bp, 9-12 day turnaround).

### 4. CD20 antigen loss
- **Measured in dogs?** **Yes, and specifically in relapse after CD20-directed therapy -- the only escape with
  that design in dogs.** **PMID 32002286** (Panjwani 2019, *Oncoimmunology*,
  [DOI](https://doi.org/10.1080/2162402X.2019.1676615)): first-in-species trial, 5 dogs with DLBCL given
  CD20-targeting second-generation canine CAR T cells -- "Specific selection pressure on CD20+ tumors was
  observed following CAR T cell therapy, culminating in antigen escape and emergence of CD20-[negative]
  disease"; CAR loss was associated with canine anti-mouse antibodies. The record has this PMID for "exons 4 and
  5 absent" (`LYMPHOMA_STATUS.md:81`); the **selection-pressure-to-escape sequence is NEW here.** Confirmed and
  extended by **NEW PMID 42480604** (Peng 2026, *Mol Cancer Ther*,
  [DOI](https://doi.org/10.1158/1535-7163.MCT-26-0365)): "We previously reported CD20 loss in canine DLBCL
  patients treated with CD20-specific CAR T cells, consistent with mechanisms of antigen escape in humans", and
  canine B-cell lymphoma "co-expresses CD19 and CD20 with heterogeneous expression patterns similar to those
  observed in humans". **No measurement of CD20 loss after chemotherapy alone in dogs was found.**
- **Treated deliberately in dogs?** **Yes -- and this is the single clearest case in the table of a canine
  treatment designed against a named escape.** PMID 42480604: tandem CD19/CD20 canine CAR T cells were built
  *because* of the observed CD20 escape, and kill canine DLBCL cells expressing CD19 and/or CD20 specifically.
  Status: in vitro; no dog treated. Enabling work towards dosing it: **NEW PMID 42969556** (Lenz 2026, *JVIM*,
  [DOI](https://doi.org/10.1093/jvimsj/aalag283)), bendamustine lymphodepletion in **11 dogs with relapsed
  lymphoma**, two-dose regimens to 90 mg/m2, no dose-limiting toxicity, lymphocytes 880 -> 310 cells/uL, IL-6
  5.32 -> 1.33 pg/mL, nodal shrinkage in 8/11, "to support further evaluation of bendamustine as a
  preconditioning agent before autologous canine CAR T-cell infusion". This postdates the record's 2026-10-31
  new-treatment sweep (`LYMPHOMA_STATUS.md:345`) and is **NEW**. Separately, the best canine anti-CD20 result is
  **PMID 41742528** (record, re-fetched): afucosylated chimeric anti-canine CD20 (4E1-7-B_f) + CHOP in 13 dogs
  -- 13/13 complete response, median time to CR 3 weeks, median PFS 340 d (95% CI 87-417), OS 458 d, 1- and
  2-year survival 69.2% and 38.9%, B-cell depletion >200 d in most dogs. Afucosylation is deliberate Fc
  engineering for antibody-dependent cytotoxicity, i.e. aimed at effector strength, not at antigen loss.
- **Countered in human lymphoma practice?** **Yes, and it is close to routine**: re-biopsy at relapse and switch
  to a target other than CD20 -- CD19 (tafasitamab, loncastuximab, CD19 CAR-T) or CD79b (polatuzumab). The
  evidence base is retrospective plus expert consensus rather than a prospective comparison (web; CD20 loss at
  relapse reported in roughly 12% of a cohort, all previously rituximab-exposed, median survival 4 months after
  loss). The agent choice within CD20 also matters, which is a deliberate practice point:
  **PMID 37645778/37683180** (record; [DOI](https://doi.org/10.1101/2023.02.19.529123)) show the
  translation-deficient *MS4A1* 5'-UTR V1 isoform makes cells resistant to the CD3xCD20 engager mosunetuzumab but
  **still killable by CD20 CAR T cells**, and the V3-to-V1 shift was found in 2 of 4 post-mosunetuzumab
  follicular-lymphoma relapses. **PMID 36093297** ([DOI](https://doi.org/10.18632/oncotarget.28258)) names it
  outright for its own regimen in 13 blastic mantle-cell patients: "The major resistance mechanisms to SCR
  therapy are loss of CD20 expression and evasion of treatment by sanctuary in the CNS."
- **Why the canine counter is still preclinical.** Stated: "there is no clinically available canine CAR-T cell
  therapy" (PMID 32329214, [DOI](https://doi.org/10.1111/vco.12602)); no licensed canine CD19 or CD79b agent
  exists; the canine CD20 antibody Blontress was licensed in 2015 and discontinued in 2017 (`LYMPHOMA_STATUS.md:306`).
- **Assayable in practice today?** **Yes.** CD20 immunohistochemistry on canine tissue is routine at commercial
  veterinary diagnostic laboratories -- PMID 33000710 ([DOI](https://doi.org/10.1177/1040638720963132)) and
  PMID 36552451 ([DOI](https://doi.org/10.3390/ani12243531)) both run CD3/CD20/PAX5/CD79acy panels through
  commercial labs. Caveat: canine flow panels use CD21 and CD79acy rather than CD20 (PMID 25512102), so CD20
  specifically is an immunohistochemistry question, and a quantitative density is not reported.

### 5. CD19 antigen loss
- **Measured in dogs?** **Expression yes, loss no.** PMID 42480604 measured CD19 and CD20 in canine lymphoma
  patient samples and found heterogeneous co-expression; **no canine relapse CD19-loss data exist**
  (`SWEEP_escapes.md:103`; ledger grades the escape TRANSFER from human CAR-T, `:276`).
- **Treated deliberately in dogs?** **No dog has received any CD19-directed agent.** The tandem CD19/CD20
  construct of 42480604 is the first canine CD19 binder and is preclinical.
- **Countered in human lymphoma practice?** **Yes, by three deliberate routes**: CD22-directed CAR T cells after
  CD19 CAR failure; CD20-directed bispecifics (glofitamab, mosunetuzumab, epcoritamab) selected after CD19 CAR-T
  failure; and tandem or dual CD19/CD20 CARs designed to pre-empt it -- which is the design 42480604 ports to
  dogs. The target has shifted from null to low: **PMID 42671910** (record), n=301 LBCL, CD19-low 1-year PFS 16%
  vs 64% for CD19-high, CD19-low share rising 17% -> 35% after CAR-T relapse while genetic locus loss moved only
  8% -> 11% (p=.82) with no coding mutations.
- **Why nobody has in dogs.** Stated: no clinically available canine CAR-T (32329214); no canine CD19 reagent
  existed before 42480604.
- **Assayable in practice today?** **No.** Canine CD19 antibodies are recent research reagents (42480604); no
  commercial canine CD19 flow or immunohistochemistry test found. The routine B-markers are CD21, CD79acy and
  PAX5 (25512102, 33000710).

### 6. BCR / NF-kB signal independence
- **Measured in dogs?** Yes, as recurrent founder genetics, and now on a commercial panel. TRAF3 mutated in 44%
  (30% somatic) of 84 tumours (PMID 25468570, record), 36% of 24 (33323169, record), 58.1% by WGS in 43
  (39922874, record); **NEW: "TRAF3 emerg[ed] as the most frequently mutated gene across B-cell lymphoma
  subtypes" on the 31-gene K9 assay (39134766)**. Counter-direction already in record: in 238 dogs TRAF3
  mutation was associated with **prolonged** PFS and OS in B-cell lymphoma (40506464). Naive versus relapsed:
  not measured.
- **Treated deliberately in dogs?** **No -- treated, but not directed.** Acalabrutinib has been given to dogs
  with lymphoma (objective response 25%, median PFS 22.5 d; PMID 27434128, carried from the project record and
  not re-fetched this pass), to **unselected** dogs; no dog has been given or denied a BTK inhibitor because of
  its TRAF3 or NF-kB status. BTK + PI3K combination work is in canine cells only (34884478, 40351764, record,
  titles only).
- **Countered in human lymphoma practice?** **Yes, by cell-of-origin and by pathway stacking.** Ibrutinib
  benefit in DLBCL is restricted to non-germinal-centre disease, and the clearest deliberate instance is
  **PMID 38899693** (Melani 2024, *NEJM*, [DOI](https://doi.org/10.1056/NEJMoa2401532)): the ViPOR regimen
  targets BCR signalling with ibrutinib, lenalidomide and prednisone *and* BCL2 with venetoclax *and* innate
  immunity with obinutuzumab; in 48 evaluable DLBCL patients objective response was 54% and complete response
  38%, and **complete responses were exclusively in non-germinal-centre DLBCL and in high-grade B-cell lymphoma
  with MYC/BCL2 rearrangements**; 2-year PFS 34%, OS 36%, median follow-up 40 months. On-target BTK escape is
  also deliberately countered: BTK C481S / PLCG2 (records 30760464, 33154951) prompts a switch to a non-covalent
  BTK inhibitor or to venetoclax.
- **Why nobody selects on it in dogs.** Two stated facts: BTK-inhibitor activity in dogs was poor (25% response,
  22.5-day PFS; record 27434128), and TRAF3 loss in dogs is **prognostically favourable** on CHOP (40506464), so
  there is no case for selecting against it.
- **Assayable in practice today?** **Partly.** TRAF3 is on the 31-gene K9 panel (39134766) and the 308-gene panel
  (40506464), so the genotype is purchasable. **Cell-of-origin (germinal-centre vs activated-B) is not routinely
  assigned in dogs**, and no functional NF-kB readout is offered.

### 7. PI3K / AKT bypass
- **Measured in dogs?** Partly. **PIK3CD mutations were associated with inferior outcome in canine T-cell
  lymphoma** in 238 dogs (40506464, record); BTK and PI3K inhibitors synergise in canine DLBCL cells (34884478,
  40351764, record, titles only). No canine PTEN result found (`SWEEP_escapes.md:138`). Naive versus relapsed:
  not measured. Ledger grades it "MEASURED expression only" (`:278`).
- **Treated deliberately in dogs?** **None found.** The project's own exposure sweep records that PI3K-delta
  inhibitors have no canine IC50 and therefore no kill rate (`docs/universe/SWEEP_pk.md`,
  `LYMPHOMA_STATUS.md:186`).
- **Countered in human lymphoma practice?** **Tried, licensed, then withdrawn.** The PI3K-delta inhibitor class
  (idelalisib, duvelisib, copanlisib, umbralisib) obtained lymphoma indications and the indications were then
  withdrawn or restricted on benefit-risk grounds, so there is **no routine PI3K-directed practice in DLBCL**. I
  did not retrieve a primary citation for each withdrawal in this pass -- **treat the withdrawal detail as
  unverified here**; the verified part is that no PI3K agent appears in current DLBCL practice and that the class
  has no canine potency measurement.
- **Why nobody targets it in dogs.** Stated: no canine IC50 for any PI3K-delta inhibitor (SWEEP_pk).
- **Assayable in practice today?** **Partly.** PIK3CD is on the 308-gene canine panel (40506464); it is not among
  the genes 39134766 reports for the 31-gene panel. Phospho-AKT immunohistochemistry is research-only.

### 8. Drug-tolerant persister (non-dividing)
- **Measured in dogs?** **Proxy only.** PMID 30238600 (record): cancer-stem-cell markers are enriched in canine
  B- and T-cell lymphoma and **CHOP-selected resistant cells up-regulate those markers, form spheroids and show
  high ALDH** -- the closest canine naive-versus-selected comparison, but in vitro. No canine measurement of a
  quiescent fraction, of a Ki67-negative residual clone in tissue, or of persister switching kinetics. The
  model's awake fraction f, retained tolerance r and switching rate are unmeasured in canine lymphoma
  (`LYMPHOMA_STATUS.md:104`). The audit's dissent -- that 30238600 is a hierarchy, not a persister -- is already
  recorded (`SWEEP_escapes.md:106`).
- **Treated deliberately in dogs?** **None found.** No dog with lymphoma has been given an agent chosen for a
  dormant or drug-tolerant state. Hydroxychloroquine, the model's non-division-gated candidate, has never been
  given to a dog with lymphoma and its canine-lymphoma IC50 has not been measured
  (`LYMPHOMA_COVERAGE_LEDGER.md:396`).
- **Countered in human lymphoma practice?** **Not deliberately.** The nearest practices -- maintenance rituximab
  in follicular lymphoma, continuous BTK-inhibitor dosing in CLL, fixed-duration deep-remission strategies --
  are chosen for relapse risk, not because a persister population was measured. Human lymphoma persisters are
  characterised (record 40700581: pirtobrutinib-tolerant mantle-cell "giant cell" persisters, non-proliferative,
  TCA-cycle-addicted, reversible on drug withdrawal) but no agent is selected on them.
- **Why nobody has.** **No reason stated for lymphoma.** The operative facts in the sources are that no patient-
  level assay for the state exists and no agent has a demonstrated kill against non-dividing lymphoma cells.
- **Assayable in practice today?** **No.** Ki67 is measurable in dogs and is reported in canine lymphoma
  (29958524 measured Ki67% alongside Pgp), so a low-proliferation fraction is visible in principle -- but a
  Ki67-low fraction is not a persister assay and no canine threshold for one exists.

### 9. Autophagy independence
- **Measured in dogs?** **No.** No canine lymphoma autophagy study found in this pass; the record reached the
  same result and grades the escape a "symmetry placeholder" with no canine **or** human lymphoma evidence that
  autophagy-independent survival drives relapse (`SWEEP_escapes.md:107`).
- **Treated deliberately in dogs?** **None found.**
- **Countered in human lymphoma practice?** **No.** Searched for autophagy-inhibition (hydroxychloroquine/
  chloroquine) trials in lymphoma and CLL and found none in the result set. Autophagy inhibition is not part of
  human lymphoma practice.
- **Why nobody has.** **No reason stated in the literature.** The operative fact is upstream of therapy: the
  mechanism has never been shown to drive lymphoma relapse in either species.
- **Assayable in practice today?** **No.** LC3-II / p62 flux is a research assay; no commercial canine test.

### 10. T-cell exhaustion / immunosuppressive microenvironment
- **Measured in dogs?** Yes, across several components, with one near-paired result. PD-L1 high in 81% of canine
  B-cell lymphomas, MFI ratio 1.50 (39132435, record); higher PD-L1/PD-1 scores predicted relapse and death in 33
  chemotherapy-only dogs (34209830, record); **chemotherapy-resistant canine lines up-regulate PD-1/PD-L1**
  (29380929, record) -- the closest canine sensitive-versus-resistant comparison; tumour extracellular vesicles
  kill CD8 cells (37884996, record); regulatory-T-cell data conflict (22293625 up vs 28735665 down, record);
  M2-type macrophages more frequent in high-grade B-cell disease (34438760, record).
- **Treated deliberately in dogs?** **Yes -- and it is a measured negative.** **NEW PMID 42247661** (Chon 2026,
  *JVIM*, [DOI](https://doi.org/10.1093/jvimsj/aalag098)): gilvetmab, a caninized anti-PD-1 monoclonal antibody
  from Merck Animal Health, 6 mg/kg q28d or 10 mg/kg q14d, multi-institutional open-label; **15 dogs with stage
  III-V lymphoma had no objective responses**, against 20% (95% CI 7-41) in 25 melanoma dogs and 46% (27-67) in
  26 mast-cell-tumour dogs; serious adverse events in 3/51 (5.9%). The record states the finding
  (`LYMPHOMA_STATUS.md:184`, "anti-PD-1 has no responses in 15 lymphoma dogs"); **the trial citation is NEW.**
  Context: 39042399 ([DOI](https://doi.org/10.1158/1078-0432.CCR-23-2266)) reviews the wider canine
  checkpoint-inhibitor and vaccine effort.
- **Countered in human lymphoma practice?** **Yes, but only in two subtypes.** PD-1 blockade is standard in
  classical Hodgkin lymphoma and in primary mediastinal B-cell lymphoma; it is not used in DLBCL or peripheral
  T-cell lymphoma outside trials. So the transfer anchor exists and is subtype-restricted, which matters because
  canine multicentric lymphoma is the DLBCL/PTCL analogue, not the Hodgkin one. Record already holds the human
  CAR-T resistance genetics that are **not** exhaustion (36584673: PAX5, IRF8, CD274, TMEM30A).
- **Why nobody pursues it further in dogs.** Stated plainly in the trial: no objective responses in lymphoma
  (42247661). Its own conclusion restricts the drug's expectation of efficacy to mast-cell tumour and melanoma.
- **Assayable in practice today?** **Partly, and not commercially.** PD-L1 immunohistochemistry and flow are
  published in dogs (39132435, 34209830) but I found no commercial canine PD-L1 test, and PD-1/PD-L1 are not in
  the routine canine flow panel (25512102).

### 11. B-lineage identity switch
- **Measured in dogs?** **Not as a relapse event. Documented at diagnosis.** Dual-phenotype canine lymphomas are
  reported with full lineage proof: a CD3+CD20+ nodal lymphoma with clonal rearrangements of **both** TCR-gamma
  and the B-cell receptor (PMID 33000710, [DOI](https://doi.org/10.1177/1040638720963132)); a CD3+CD20+
  intestinal lymphoma with monoclonal TCR-gamma rearrangement, finally classed as type-2 enteropathy-associated
  T-cell lymphoma (PMID 36552451, [DOI](https://doi.org/10.3390/ani12243531)); 10/10 CD3+/CD20+ large-cell
  lymphomas monoclonal for TCR-gamma, 3/10 also IgH (37837199, record). **No paired diagnosis-to-relapse lineage
  switch in a dog was found.** Record grades the escape ASSUMED at 1e-9 and proposes regrading to HUMAN-transfer
  (`SWEEP_escapes.md:109`).
- **Treated deliberately in dogs?** **None found.**
- **Countered in human lymphoma practice?** **Reactively, yes; pre-emptively, no.** Lineage-switch relapses after
  CD19-directed therapy are treated as the new lineage -- myeloid-directed therapy and transplant (PMID
  31577606; and records 40193715: 75 lineage-switch relapses after CD19/CD22/CD38/CD7 therapy, 71% B-ALL to AML;
  34799485: 2 of 9 post-CD19-CAR relapses switched with identical clonal Ig rearrangement). No regimen is
  designed in advance against it.
- **Why nobody has in dogs.** **No reason stated.** The operative fact: only six dogs in the world have received
  a lineage-directed cellular immunotherapy for lymphoma (5 in 32002286, 1 in 27401141), and none long enough or
  deep enough to select for a switch.
- **Assayable in practice today?** **Yes -- and it is one of the few escapes a practising veterinary oncologist
  could demonstrate today with catalogue tests.** PARR clonality PCR for TCR-gamma and IgH is a routine
  commercial canine test, and a CD3/CD20/PAX5/CD79acy immunohistochemistry panel is routine; those two together
  are exactly what the canine case reports used (33000710, 36552451, and 40842370
  [DOI](https://doi.org/10.1111/vde.70021) for the clonality methodology in 12 dogs). The missing piece is not
  the assay but the paired sample at relapse.

### 12. Antigen-presentation loss (MHC-I/II, B2M, CD58)
- **Measured in dogs?** Yes for class II MHC, and prognostically, in a large series: **low class II MHC predicted
  relapse and death in 160 dogs** (21781170, record). Serum beta-2-microglobulin and IL-2R were higher in
  relapsed dogs (36635848, record) -- a serum marker, which the record already warns must not be read as
  cell-surface loss. No canine surface B2M or CD58 study found. Naive versus relapsed surface measurement: not
  found.
- **Treated deliberately in dogs?** **None found.** No dog has been assigned or denied a therapy because of its
  MHC status. The point is live for this project because its allogeneic-transplant, vaccine and engager arms are
  all MHC-dependent and are listed as reopened by MHC loss (`LYMPHOMA_STATUS.md:248`, `:259`).
- **Countered in human lymphoma practice?** **Yes, by design rather than by measurement.** The whole T-cell
  engager class (glofitamab, mosunetuzumab, epcoritamab) and CAR T cells are **MHC-independent effectors**, and
  that independence is the stated reason they are preferred over approaches needing intact antigen presentation.
  EZH2 inhibition restores silenced CD58 (31962268, record, title only). CD58 aberrations are frequent across
  lymphoma subtypes (n=748, 37391168, record) and trend higher in CAR-T progressors (37391168). **No routine
  assay triggers the choice** -- the agents are chosen for other reasons and happen to bypass the escape.
- **Why no measurement-triggered therapy exists.** **No reason stated.** The operative fact is the one above: the
  agents that bypass it are already being used for unrelated indications.
- **Assayable in practice today?** **Yes -- this is the most routinely assayed escape in canine practice.** Class
  II MHC is a standard tube of the canine lymph-node flow panel (Class II MHC-FITC paired with CD34-PE in the
  eight-tube panel used by the Colorado State University Clinical Immunology Laboratory; web), is reported on
  commercial canine lymphoma flow reports, and has prognostic value in 160 dogs (21781170). B2M and CD58 are not
  assayed in dogs.

### 13. MGMT alkylator repair
- **Measured in dogs?** **In cell lines only.** PMID 26130852 (record): 2 of 5 canine lymphoma lines were
  lomustine-resistant, an MGMT inhibitor sensitised them, and **expression was not explained by promoter
  methylation**. No canine patient MGMT measurement, naive or relapsed. Mismatch-repair protein loss is reported
  across canine tumours with lymphoma lower than melanoma (34538134, record).
- **Treated deliberately in dogs?** **None found in patients.** The MGMT inhibitor (O6-benzylguanine class) was
  used in vitro (26130852). No dog has had lomustine withheld, or an MGMT inhibitor added, on MGMT status.
- **Countered in human lymphoma practice?** **No.** MGMT promoter methylation routinely directs temozolomide use
  in **glioblastoma**, and that is where the practice lives. In human lymphoma, alkylator choice is not
  MGMT-guided; temozolomide in primary CNS lymphoma is given without MGMT selection.
- **Why nobody targets it.** A reason **is** stated for dogs: in canine lymphoma lines MGMT expression did not
  track promoter methylation (26130852), so the human glioma assay would not predict it. For lymphoma generally,
  no agent choice turns on it.
- **Assayable in practice today?** **No.** No commercial canine MGMT test found, and 26130852 shows the
  transferable human assay would not work in this tumour anyway.

### 14. CD7 antigen loss (T-lineage)
- **Measured in dogs?** **No.** CD7 is not in the published canine flow panel (25512102 lists CD11a, CD3,
  CD3-12, CD5, CD21, CD79acy, CD56, CD14, CD4, CD8). Aberrant T-lineage antigen expression in canine lymphoma is
  reported generally (17981339, record) but not CD7 loss. No canine CD7 reagent or trial found.
- **Treated deliberately in dogs?** **None found.** No CD7-directed agent exists for dogs; the record's own
  search concluded "Not found: canine CD3 engager, CD7/CD5 CAR-T" (`LYMPHOMA_STATUS.md:276`).
- **Countered in human lymphoma practice?** **Yes, in two deliberate ways.** CD7 CAR T cells are in clinical use
  for T-ALL/lymphoblastic lymphoma: **PMID 37674391** ([DOI](https://doi.org/10.1080/10428194.2023.2254428)), 14
  patients with t(8;14) T-ALL/LBL -- all 7 given chemotherapy or transplant alone died, median OS 3 months,
  whereas 5 of 6 given CD7 CAR-T achieved complete remission and **all 4 who then had allogeneic transplant
  remained disease-free**. So the deliberate counter to CD7 loss is **consolidative allogeneic transplant after
  CD7 CAR-T**, plus the "naturally selected CD7-negative" CAR design. CD7 loss itself is documented at relapse
  (record 37020231: 4 of 6 post-CD7-CAR relapses lost CD7). A different T-lineage target with its own loss route
  is TRBC1/TRBC2 (records 39528665, 41236719, titles only).
- **Why nobody has in dogs.** **No reason stated beyond the absence of a product.** Canine TRBC1/2 diversity has
  been characterised (41236719, record) but no canine T-lineage effector exists.
- **Assayable in practice today?** **No.** No commercial canine CD7 flow or immunohistochemistry reagent found.

### E1. Glucocorticoid-receptor loss (NR3C1)
- **Measured in dogs?** **Yes, and this is the best longitudinal canine measurement of any escape.** PMID
  31943234 (record): 7 treatment-naive dogs; prednisone resistance "develops rapidly and essentially
  universally", median onset 68 days (range 7-348); **NR3C1-alpha mRNA fell in 6 of 6 high-grade cases (p=.031)**
  while ABCB1 and 11beta-HSD1/2 did not consistently change -- i.e. a within-dog naive-to-resistant measurement.
  PMID 38471970 (record): 30 dogs, 14 with serum cortisol >=6 ug/dL had lower response, PFS, OS and fewer
  glucocorticoid-receptor-positive cells (P-gp-positive rate did not differ). PMID 20362310 (record): two canine
  lines were GR-low and dexamethasone-resistant. ALREADY IN RECORD (`SWEEP_escapes.md:34`).
- **Treated deliberately in dogs?** **Yes, but by omission rather than with an agent -- and it is the only
  mechanism-directed act that is actually routine veterinary advice.** PMID 21320018 (record): 11 of 13 dogs
  surviving beyond 2 years **had not been pre-treated with corticosteroids**, which is the evidential basis for
  the standing recommendation to avoid steroids before referral. That recommendation is a deliberate clinical
  measure directed at this escape. **No pharmacological reversal has been given to a dog**: the NF-kB inhibitor
  IMD-0354, which raised GR and restored dexamethasone sensitivity, was in canine cells only (20362310).
- **Countered in human lymphoma practice?** **Not by reversal; yes by measurement-and-escalation.** In acute
  lymphoblastic leukaemia, the day-8 glucocorticoid response is a formal risk-stratification variable and a poor
  response escalates the regimen; dexamethasone is preferred over prednisone partly for potency and CNS reach. So
  the resistance is measured and answered with intensity, not with an anti-resistance agent. Record holds the
  human genetics (32066867: ~30% of dexamethasone-relapsed T-ALL clones GR-low; 31697823: NR3C1 among 12
  relapse-enriched genes in 103 trios).
- **Why no agent.** Stated: no agent restores GR in a patient; the available handle is avoiding pre-exposure
  (21320018).
- **Assayable in practice today?** **Functionally yes, molecularly no.** The clinical surrogate -- does this dog
  still respond to prednisone -- is universally available and is exactly the quantity 31943234 measured (median
  68 days to resistance). NR3C1 expression and the GR-positive cell fraction are research assays; NR3C1 is not
  among the genes reported for the 31-gene (39134766) or 308-gene (40506464) canine panels.

### E2. Nucleoside-activation loss (dCK down)
- **Measured in dogs?** **No.** Canine dCK was searched and not found (`SWEEP_escapes.md:138`); the record's
  evidence is human (24972933: DCK down-regulation the "single most important molecular event" in all
  cytarabine-resistant mantle-cell lines and **50% of primary post-cytarabine samples**, with 20-1000x
  cross-resistance to gemcitabine, fludarabine and cladribine).
- **Treated deliberately in dogs?** **None found.**
- **Countered in human lymphoma practice?** **No agent, but a rational class switch that is not assay-triggered.**
  24972933 shows dCK loss does **not** cross-resist doxorubicin, cyclophosphamide, bendamustine, bortezomib or
  rituximab and **increases** ibrutinib sensitivity, so abandoning the nucleoside class at cytarabine failure is
  the sound move and is what happens -- but it follows clinical failure, not a dCK measurement. No agent restores
  dCK.
- **Why nobody has.** Stated: no assay in clinical use; no agent restores the enzyme. The 50% figure is from a
  research cohort, not a diagnostic service.
- **Assayable in practice today?** **No.** *DCK* is not on any canine panel reported.

### E3. Topoisomerase-IIalpha loss
- **Measured in dogs?** **No.** "canine lymphoma topoisomerase" returned nothing (`SWEEP_escapes.md:36`); the
  evidence is a mouse Emu-myc model in which Top2A level sets doxorubicin response and relapsed lymphomas show
  spontaneous changes in topoisomerase levels (18574145, record).
- **Treated deliberately in dogs?** **None found.**
- **Countered in human lymphoma practice?** **No.** TOP2A copy number is used in **breast cancer** to predict
  anthracycline benefit; in lymphoma TOP2A is not measured and does not direct therapy.
- **Why nobody has.** **No reason stated in the lymphoma literature.**
- **Assayable in practice today?** **No.** No canine TOP2A test; the human assay is a breast-cancer FISH/IHC
  product.

### E4. BCL2-family rewiring (MCL1 / BCL-xL / phospho-BCL2)
- **Measured in dogs?** **Yes, functionally, and it is the strongest negative result among the canine
  measurements.** PMID 36433867 (record): 18 dogs; neoplastic T cells were venetoclax-sensitive (EC50 0.023 uM)
  but **6 of 7 (86%) non-indolent B-cell cancers were resistant to venetoclax (288 uM) and also to navitoclax
  (BCL2/BCL-xL, 225 uM)**, and **BCL2 protein did not predict sensitivity**; MCL1 dependence was not tested. So
  canine B-cell resistance is not simple BCL-xL compensation. Indirect and in another tumour: in canine
  transmissible venereal tumour, BCL2 was over-expressed in the slowest chemotherapy responders (PMID 31777108,
  [DOI](https://doi.org/10.1111/vcp.12805)) -- label as indirect, different disease.
- **Treated deliberately in dogs?** **None found. Measured, never treated.** Venetoclax has not been given to
  dogs with lymphoma in any published trial; the canine data are ex vivo (36433867), and the model's T-cell
  venetoclax exposure is second-hand with an unmeasured free fraction (`LYMPHOMA_STATUS.md:99`).
- **Countered in human lymphoma practice?** **Yes -- the most directly mechanism-driven practice in the table.**
  Venetoclax combinations are standard (venetoclax + obinutuzumab in CLL), and in DLBCL venetoclax enters ViPOR
  **specifically as the BCL2 arm** of a five-agent pathway-targeting regimen (38899693). BH3 profiling is used in
  research to distinguish BCL2, BCL-xL and MCL1 dependence. **MCL1 inhibitors have not reached practice**; the
  commonly cited reason is cardiac toxicity, for which **I did not retrieve a primary citation in this pass --
  treat it as unverified.** Record holds the human rewiring mechanism (37751299: hyperphosphorylation of MCL-1,
  BCL-2, BAD and BAX underlies intrinsic and acquired venetoclax resistance; 32708132: resistant DLBCL
  re-sensitised by BCL-xL inhibition).
- **Why nobody treats it in dogs.** A reason **is** stated, and it is in the canine data themselves: 86%
  intrinsic resistance at achievable concentrations in canine B-cell disease (36433867).
- **Assayable in practice today?** **Partly, and with the wrong assay.** BCL2 immunohistochemistry is available
  on canine tissue (used in 13 canine Burkitt-like lymphomas, both BCL2- and MYC-negative, 33816589, record) --
  but 36433867 shows BCL2 protein does not predict BH3-mimetic sensitivity, so the purchasable assay does not
  answer the question. The functional alternative **is** commercially available for dogs: ex vivo
  chemosensitivity testing on live cells from a node aspirate, validated in 261 dogs across five drugs
  (PMID 33025640, [DOI](https://doi.org/10.1111/vco.12656); vendor panel now 13 drugs, web) -- venetoclax is not
  among the five validated agents.

### E5. Quiescent, efflux-high lymphoid progenitor ("conjunction clone")
- **Measured in dogs?** **Yes, directly, and this escape is better measured in dogs than in humans.** PMID
  21777289 (record): CD34+/CD117+/CD133+ lymphoid progenitor cells expanded in 28 dogs versus 6 controls
  (p=.0022), carrying **the same clonal rearrangement as the bulk tumour** and maintained on serial xenograft.
  PMID 30238600 (record): CHOP selection up-regulates stem-cell markers, spheroid formation and ALDH -- a
  naive-versus-selected comparison. PMIDs 23167606 and 23820219 (record): the side population is ABCB1/ABCG2-high
  and was **not** reduced by verapamil or fumitremorgin C. ALREADY IN RECORD (`SWEEP_escapes.md:38`;
  `LYMPHOMA_UNIVERSE.md:62`).
- **Treated deliberately in dogs?** **Yes -- and this is the single most informative piece of prior art in the
  whole table.** PMID 28357033's **primary endpoint was literally the reduction of CD34/CD117/CD133 lymphoma
  progenitor cells**: 20 dogs, double-blinded, placebo-controlled, neoadjuvant valspodar then doxorubicin, with
  progenitor cells counted in lymph node and blood at diagnosis, on neoadjuvant day 4, and one week after the
  first chemotherapy dose. Result: "There were no differences between groups in total LPCs in lymph nodes or
  peripheral blood, nor in event-free survival or overall survival." So the escape the project's closure turns on
  has already been attacked deliberately in a randomised canine trial, and the attack **did not move the cell
  population it was aimed at**. That is prior art, not a model result, and it is the strongest external support
  for the record's conclusion that E5 is the hard escape (`LYMPHOMA_STATUS.md:174`, `:238`).
- **Countered in human lymphoma practice?** **No.** There is no lymphoid-progenitor-directed agent in human
  lymphoma practice. The nearest analogue is allogeneic transplant as cell replacement, which is given for
  disease risk, never because a progenitor population was measured.
- **Why the canine attempt stopped.** Reasons stated in the sources: ABCB1 inhibition did not deplete the
  population (28357033) and neither verapamil nor fumitremorgin C shifted the side population (23820219). No
  agent is known to kill it. The project's own agent search reached the same place (`LYMPHOMA_STATUS.md:260`).
- **Assayable in practice today?** **Partly -- and more than the record implies.** **CD34 is in the routine canine
  lymphoma flow panel** (paired with class II MHC in the standard eight-tube panel; web), CD34 positivity is
  reported on commercial canine flow reports, and it carries prognostic weight. So a practising oncologist can
  see the CD34-positive fraction today. CD117, CD133, ALDH activity and the side-population assay are
  research-only, so the *conjunction* (quiescent **and** pump-high) is not measurable in practice.

### E7. Antigen-low (sub-threshold CD20/CD19), as distinct from antigen-null
- **Measured in dogs?** **Qualitatively only.** PMID 42480604: canine B-cell lymphoma co-expresses CD19 and CD20
  "with heterogeneous expression patterns similar to those observed in humans". No canine quantitative density
  distribution and no canine relapse-time down-modulation data.
- **Treated deliberately in dogs?** **Indirectly, and not by measurement.** The afucosylated anti-canine CD20
  antibody (41742528) is Fc-engineered to raise antibody-dependent cellular cytotoxicity, which raises kill at a
  given antigen density -- but it was not chosen because a density was measured. The tandem CAR (42480604)
  addresses antigen-null, not antigen-low.
- **Countered in human lymphoma practice?** **Yes, and this is becoming the main antigen practice rather than a
  side issue.** PMID 42671910 (record), n=301: CD19-low 1-year PFS 16% vs 64%, CD19-low share 17% -> 35% after
  CAR-T relapse **with no coding mutations and no significant locus loss**, so the target is density. The
  deliberate counters are density-robust effectors (bispecifics, dual-antigen CARs) and the isoform work showing
  the CD20 CAR kills translation-deficient cells that the engager cannot (37645778/37683180). Flow MFI is
  measured clinically. Record also holds the complement threshold result (22228637).
- **Why nobody measures it in dogs.** **No reason stated.** The operative fact: no canine agent's use would
  change on density, and no canine antigen-density threshold is published.
- **Assayable in practice today?** **Partly, and already produced without being interpreted.** Every commercial
  canine flow report carries fluorescence intensity for CD21 and CD79acy, and ImpriMed's platform explicitly
  uses "antigen expression profiles" as model inputs (33025640). What is missing is a canine threshold, and the
  markers reported are not CD20 or CD19.

### E8. XPO1 C528S (verdinexor target-site mutation)
- **Measured in dogs?** **No.** XPO1 expression did not correlate with verdinexor (KPT-335) efficacy across 8
  canine lines, IC50 89.8-418 nM (40872651, record). No canine XPO1 mutation screen exists.
- **Treated deliberately in dogs?** **None found.** Verdinexor (Laverdia-CA1) is licensed for canine lymphoma and
  is load-bearing in every program in the record, yet **no dog has been genotyped at XPO1 before, during or after
  treatment.**
- **Countered in human lymphoma practice?** **No, and the stated reason is that the escape has not appeared.**
  PMID 27634897 (record): an engineered heterozygous C528S is sufficient for resistance in leukaemia lines, but
  "resistance against selinexor has not yet been observed in the clinic", and in-vitro selection for resistance
  produced **no** XPO1 mutation.
- **Why nobody has.** This is the one escape with a clean, source-stated reason: **the mechanism is considered
  not (yet) clinically relevant** because it has not been observed in patients (27634897).
- **Assayable in practice today?** **No.** XPO1 is not among the genes reported for the 31-gene (39134766) or
  308-gene (40506464) canine panels. A single-codon Sanger or allele-specific PCR assay would be trivial to
  build; none exists.

### E9. Antifolate transport / retention loss (reduced folate carrier, SLC19A1)
- **Measured in dogs?** **No.** RFC and FPGS were searched and not found in dogs (`SWEEP_escapes.md:42`); the
  evidence is human (15327516: RFC promoter methylation in **30% of primary CNS lymphoma versus 8% of systemic
  DLBCL**; 18028428: RFC hypermethylation in 2/25 untreated DLBCL, both record).
- **Treated deliberately in dogs?** **None found.** Methotrexate is given intrathecally to dogs -- PMID 25041580
  ([DOI](https://doi.org/10.1111/vco.12109)), 112 dogs and 8 cats -- but never with a transporter measurement.
- **Countered in human lymphoma practice?** **No assay-triggered switch; a dose strategy instead.** High-dose
  methotrexate saturates low-affinity transport and is the standard CNS regimen for exactly that reason, so the
  practice answers the mechanism with dose rather than with a measurement or a different drug.
- **Why nobody has.** **No reason stated.** The operative fact is that high-dose dosing arguably obviates the
  measurement.
- **Assayable in practice today?** **No.** *SLC19A1* methylation is a research assay; no canine test found.

### E10. Macrophage checkpoint (CD47 / SIRP-alpha)
- **Measured in dogs?** **Pathway conserved and functional; prevalence not measured.** PMID 27856424 (record):
  the canine CD47/SIRP-alpha axis is conserved and functional, SIRP-alpha Fc variants raise phagocytosis of
  canine lymphoma cells, and anti-CD20 plus CD47 blockade **cured 100% of xenografted mice**. **No canine CD47
  expression series in patients** exists, so the fraction of dogs affected is unknown.
- **Treated deliberately in dogs?** **None found in dogs.** Dog-active reagents exist (27856424) and were tested
  in mice bearing canine cells, not in dogs.
- **Countered in human lymphoma practice?** **Attempted, then abandoned in haematology.** Hu5F9-G4 (magrolimab)
  plus rituximab was taken into non-Hodgkin lymphoma (record 30380386, *NEJM* 2018, title only), and CD47/SIRPa
  is prognostic in DLBCL (32342603, record). The sponsor then **ended all haematological development**: the phase
  3 ENHANCE study in higher-risk myelodysplastic syndrome was stopped for futility, and ENHANCE-3 in acute
  myeloid leukaemia showed an **increased risk of death** (infections and respiratory failure) plus futility
  (web: Gilead statements reported by FierceBiotech, BioCentury, BioPharma Dive; **no peer-reviewed primary
  citation retrieved in this pass -- treat the discontinuation detail as web-sourced**). A next-generation
  CD47 fusion protein is being positioned explicitly against CD20 resistance in preclinical models (**NEW**
  PMID 41737272, [DOI](https://doi.org/10.2147/ITT.S572396): CO-005 active in rituximab-resistant lymphoma
  xenografts) -- preclinical, mouse.
- **Why nobody pursues it.** Reasons stated: sponsor discontinuation for futility and excess deaths in the lead
  haematological indications (web); no CD47 agent is licensed anywhere.
- **Assayable in practice today?** **No.** No commercial canine CD47 test found.

### CNS sanctuary (a site, not a mechanism)
- **Measured in dogs?** **Overt involvement yes; occult seeding no -- and the record's own open item is exactly
  this.** PMID 6547126 (Couto 1984, *JAVMA*): 8 dogs with CNS lymphosarcoma, seizures and multifocal signs;
  cerebrospinal fluid showed high white-cell counts with abnormal lymphoid cells in **all 8** and high protein in
  5. `LYMPHOMA_STATUS.md:387` records that `LYMPHOMA_CNS_SEED_FRACTION = 0.05` is labelled "illustrative" in its
  own source line, that **no canine occult-seeding measurement exists**, and that the record's "30% CNS
  involvement" is a different quantity. Nothing found in this pass changes that; **no canine prospective study of
  occult CNS seeding was found.**
- **Treated deliberately in dogs?** **Yes -- the oldest deliberate counter-measure in the canine literature, and
  only ever for established disease.** PMID 6547126: 4 of the 8 dogs received systemic chemotherapy **plus
  intrathecal cytosine arabinoside plus craniospinal irradiation**, "resulting in marked improvement of the
  clinical signs" (1984; no doses, no follow-up -- this is the "one 4-dog 1984 report" of
  `LYMPHOMA_STATUS.md:324`, now with its PMID). PMID 25041580: intrathecal cytarabine alone or with methotrexate
  in **112 dogs and 8 cats** with brain or spinal disease, with one generalized tonic-clonic seizure in 120
  animals during anaesthetic recovery, responsive to diazepam; "intrathecal administration ... is a safe
  procedure in dogs and cats". **No canine CNS *prophylaxis* study was found** -- nobody has given a dog
  intrathecal or high-dose methotrexate to prevent a CNS relapse.
- **Countered in human lymphoma practice?** **Yes, routinely and risk-stratified -- and the efficacy evidence is
  weak, which matters for the transfer.** Prophylaxis is in NCCN and ESMO guidance and in wide use (an Italian
  national survey found 58% of centres using intrathecal chemotherapy only and 40% using intravenous
  methotrexate 1.5-3 g/m2, with or without intrathecal; web). But **PMID 38497149** (Tolley 2024, *Haematologica*,
  [DOI](https://doi.org/10.3324/haematol.2023.284281)): systematic review and meta-analysis, 1,812 studies
  screened, **no randomised controlled trial identified**, 7 observational studies and 1,661 patients;
  high-dose methotrexate gave relative risk **0.54 (95% CI 0.27-1.07)** for CNS relapse and **0.70 (0.44-1.11)**
  for death; risk of bias "serious", GRADE quality "low"; conclusion: "HD-MTX does not prevent or, at best, only
  slightly reduces the risk of CNS relapse and confers no survival benefit." The *working* anchor is paediatric,
  not adult: in TT16, 598 children received 13-27 intrathecal doses each with no cranial irradiation and CNS
  relapse was 1.5% (`LYMPHOMA_STATUS.md` K.5). CNS sanctuary is also named as a resistance mechanism in its own
  right by a human regimen report (36093297).
- **Why no canine prophylaxis.** **No reason stated in the literature.** Facts in the sources that bear on it:
  canine CNS relapse incidence has not been quantified prospectively; intrathecal dosing in dogs needs anaesthesia
  or an implanted port (`LYMPHOMA_STATUS.md:374`); and cerebrospinal-fluid cytology is not part of routine
  staging.
- **Assayable in practice today?** **Partly, and only once suspected.** Cerebrospinal-fluid collection with
  cytology is available in referral practice and is what both canine series rest on (6547126, 25041580), and MRI
  is available at referral centres. Neither is part of routine lymphoma staging, and **occult seeding is below
  the detection limit of both** -- which is precisely why the record's seeding fraction has no measurement
  behind it.

---

## 2. Cross-cutting answers

### 2.1 Has anyone, in any species, enumerated all relapse mechanisms for a lymphoma and designed a combination to close every one?

**Not at this resolution, as far as my searches reach.** I searched resistance-mechanism enumeration, "all
mechanisms of relapse", rational combination design, evolutionary and adaptive therapy, and "resistance-proof"
combination. I found **no paper, in any species or tumour, that enumerates a catalogue of relapse mechanisms of a
stated size and then reports a combination tested against every member.** "Not found" here means my queries
returned nothing of that shape; it is not a claim that none exists.

The closest precedents, and exactly what each covered:

| precedent | what it is | what it covered | what it did not |
|---|---|---|---|
| **ViPOR** -- PMID 38899693, [DOI](https://doi.org/10.1056/NEJMoa2401532) (Melani 2024, *NEJM*); editorial PMID 38899699 "ViPOR's Venom -- Rationally Targeting DLBCL with Precision" | The closest **clinical** precedent. Phase 1b-2, single centre. Framed in its own abstract as "whether targeting multiple survival pathways may be curative in DLBCL is unknown" | **Four or five survival pathways** chosen by mechanism: BCR signalling (ibrutinib, lenalidomide, prednisone), BCL2 (venetoclax), innate immune effector (obinutuzumab). 6 cycles x 21 days, fixed duration. 48 evaluable DLBCL: response 54%, complete 38%, complete responses exclusively in non-GCB and high-grade MYC/BCL2-rearranged disease; circulating tumour DNA undetectable in 33% at end of therapy; 2-year PFS 34%, OS 36% at 40 months' follow-up | **Pathways, not relapse mechanisms.** No efflux, no antigen loss or antigen density, no sanctuary site, no quiescent or progenitor compartment, no antigen-presentation loss, no toxicity-budget ledger, no per-escape coverage claim. It does not state a catalogue size or claim any escape is closed |
| **Komarova & Wodarz** -- PMID 15980154, [DOI](https://doi.org/10.1073/pnas.0501870102) (*PNAS* 2005); review PMID 16154360 | The **count** argument, and the precedent that predates Bozic/Nowak eLife 2013 | A stochastic framework on measurable parameters (turnover rate, mutant generation rate). Two results this project rests on implicitly: resistance "arises mainly before the start of treatment", and for chronic myeloid leukaemia "a combination of **three** targeted drugs with different specificities might overcome the problem of resistance" | Counts independent mutational routes; **does not enumerate mechanisms**, has no compartments, no potency or toxicity, and is single-driver |
| **Saputra et al.** -- PMID 29686021, [DOI](https://doi.org/10.1158/0008-5472.CAN-17-1201) (*Cancer Res* 2018) | The precedent that **bears directly on this project's known weakness**, and the one I would read next | Simulated sensitive, singly-resistant and fully-resistant pools under two-drug combinations. At **equal initial efficacy, antagonistic combinations suppressed singly-resistant clones better than synergistic ones**, because synergistic combinations are "inherently fragile toward the development of single resistance" -- "proefficacy" versus "antiresistance" strategies | Two drugs, one abstract resistance axis, no mechanism catalogue. But it names in the literature the same object as the record's recurring "every agent is load-bearing / no redundancy" weakness (`LYMPHOMA_STATUS.md:137`, `:236`) |
| **Adaptive / evolutionary therapy** (Gatenby, Zhang; prostate) | A different design goal | Containment by dose modulation, retaining sensitive cells to compete with resistant ones; clinical proof-of-principle in metastatic castrate-resistant prostate cancer | Explicitly **not closure**. Not a precedent for "every escape closed", and not applied to lymphoma |
| **Bozic/Nowak eLife 2013**, [DOI](https://doi.org/10.7554/eLife.00747) | Already known to this project; listed for completeness | Evolutionary dynamics under targeted combination therapy | As above: mutation-count, no mechanism catalogue |

**So the project's method -- an enumerated escape catalogue, an escape-by-compartment matrix, and a per-escape
closure claim with a stated catalogue size -- has no published counterpart I could find.** The clinical
precedent (ViPOR) is a four-pathway regimen; the theoretical precedents count mutations rather than name
mechanisms. The one piece of published theory the project should reckon with is 29686021, because it predicts
that a combination optimised for efficacy is the one most fragile to single resistance -- which is the shape of
the record's own fault-tolerance findings.

### 2.2 In canine lymphoma, what IS routinely measured before treatment?

| routinely measured | how, and source |
|---|---|
| Cytology or histopathology of a node | universal |
| **Immunophenotype by flow cytometry on a node aspirate** | "Flow cytometric immunophenotyping of lymph node aspirates has become a standard practice of canine lymphoma diagnostic workup" (PMID 25512102, [DOI](https://doi.org/10.1111/vcp.12221)), which gives the normal-node reference set in 26 dogs across 11 markers: CD11a 92.2%, CD3 55.0%, CD3-12 57.3%, CD5 52.3%, CD21 33.9%, CD79acy 46.9%, CD56 4.9%, CD14 5.5%, with CD4 58.7% and CD8 21.3% inside the CD3 gate |
| **Class II MHC and CD34**, and cell size | part of the standard eight-tube canine panel (Class II MHC-FITC / CD34-PE); class II MHC prognostic in 160 dogs (21781170, record) |
| **PARR clonality PCR** (TCR-gamma, IgH) | commercial; 25512102, 33000710, 40842370 |
| Immunohistochemistry panel on fixed tissue: CD3, CD20, CD79a, PAX5, **Ki67**, BCL2, MYC, **p53**, and **P-gp on request** | 33000710, 36552451, 29958524 (Ki67 and Pgp together), 33816589 (BCL2/MYC), 39282821 (p53) |
| WHO stage and substage; complete blood count and chemistry; imaging; marrow or blood involvement by flow | standard; marrow infiltration >3% by flow gave time-to-progression 69 vs 149 d (23735731, record) |
| **Optional, purchasable today**: 31-gene K9 lymphoma NGS panel (TP53, TRAF3, SETD2, SATB1, FBXW7 among them) | PMID 39134766, run with a commercial diagnostic laboratory co-author |
| **Optional**: 120-gene SearchLight DNA panel, 482,000 bp, distributed in North America by Antech, 9-12 day turnaround, reporting MDR1 as a host pharmacogenomic marker | web (Vidium Animal Health / Antech) |
| **Optional**: ex vivo live-cell drug-sensitivity testing plus flow plus PARR | PMID 33025640, [DOI](https://doi.org/10.1111/vco.12656): 261 dogs, 5 agents (doxorubicin, vincristine, cyclophosphamide, lomustine, rabacfosadine), random-forest models, test-set ROC-AUC mostly >0.65, score >50% associated with shorter time to complete response (log-rank p<.05); vendor panel now 13 drugs (web) |

**How much of the escape list is visible to a practising veterinary oncologist?** Of the 23 escapes plus the CNS
site, **six** are visible with catalogue tests (class II MHC, CD34, CD20, TP53/p53, TRAF3, and lineage switch via
PARR + immunohistochemistry); **five** have an assay that is available but not interpretable for this purpose
(P-gp immunohistochemistry with no agreed cut-off, BCL2 immunohistochemistry shown not to predict BH3-mimetic
response, antigen density as uninterpreted flow intensity, PIK3CD on the larger panel only, cerebrospinal-fluid
cytology for overt CNS disease only); **thirteen** cannot be measured in practice at all.

The practically important point is orthogonal to the list: **the one commercially available canine assay that
addresses all 23 at once measures the consequence, not the mechanism.** Ex vivo chemosensitivity (33025640)
reports whether this dog's cells die when exposed to this drug, without naming why. That is why a practising
veterinary oncologist does not need the escape catalogue in order to act, and it is the main reason the
mechanism list has never been operationalised in dogs.

### 2.3 Which of the 23 are human-lymphoma constructs with no canine evidence at all?

**Six with no canine evidence of any kind**, so a canine clinician would have no reason to consider them:
E2 nucleoside-activation loss (dCK); E3 topoisomerase-IIalpha loss; E8 XPO1 C528S; E9 antifolate transport loss
(RFC); CD7 antigen loss; autophagy independence. For E8 the absence extends to human patients too -- the
mechanism has not been observed clinically in any species (27634897).

**Three more are partial** -- the molecule is now measured in dogs but the escape event is not: CD19 loss
(expression measured, 42480604; loss never observed in a dog), E7 antigen-low (heterogeneous expression measured,
42480604; no density distribution or relapse down-modulation), and B-lineage identity switch (dual-phenotype
disease documented at diagnosis in dogs, 33000710 / 36552451 / 37837199; no switch at relapse).

**Two are canine-dominant, i.e. better evidenced in dogs than in humans**, which is worth stating because it
runs the other way: E1 glucocorticoid-receptor loss (a within-dog naive-to-resistant NR3C1 measurement,
31943234, which has no human lymphoma equivalent of that design) and E5 the quiescent efflux-high progenitor
(a clonally-matched, serially transplantable canine hierarchy, 21777289, plus a randomised canine trial aimed at
it, 28357033).

---

## 3. Synthesis

Of the **24 rows** (23 escapes plus the CNS site):

**(a) Measured in dogs AND deliberately treated in dogs -- 6 rows.** P-glycoprotein (measured 8646690 including
relapse-vs-naive; treated 28357033); E5 quiescent efflux-high progenitor (measured 21777289; treated 28357033,
where it was the primary endpoint); CD20 antigen loss (measured at relapse after CD20 CAR-T, 32002286; counter
designed, 42480604, with 42969556 preparing the dosing); T-cell exhaustion (measured 39132435 / 34209830;
treated 42247661); E1 glucocorticoid-receptor loss (measured 31943234; countered by steroid avoidance,
21320018 -- treatment by omission, and the only one of the six that is routine advice); CNS sanctuary (measured
6547126; treated 6547126 and 25041580). **In four of these six the canine attempt has a published negative or
null result** (valspodar null twice over, for P-gp and for the progenitor population; gilvetmab 0/15 in
lymphoma; the CD20 CAR-T selected for escape), and in one the counter-measure is still preclinical. That is the
most useful fact in this file: where the model's escapes have been attacked in dogs, the attacks are documented
and they failed, which is independent support for the record's conclusions rather than a reason to revise them.

**(b) Measured in dogs but never treated in dogs -- 12 rows.** BCRP/ABCG2; TP53; BCR/NF-kB independence (a BTK
inhibitor has been given to **unselected** dogs, which is not direction); PI3K/AKT bypass; drug-tolerant
persister (proxy only); antigen-presentation loss; MGMT (cell lines only); E4 BCL2-family rewiring; E10
CD47/SIRP-alpha (pathway only, prevalence unmeasured); E7 antigen-low (expression only); CD19 loss (expression
only); B-lineage switch (diagnosis only).

**(c) Known only from human or mouse lymphoma, no canine evidence -- 6 rows.** E2, E3, E8, E9, CD7 loss,
autophagy independence.

**(d) Assayable in ordinary veterinary practice today -- 6 fully, 5 partly, 13 not at all.** Fully: class II MHC
(flow, routine, prognostic in 160 dogs), CD34 (flow, routine), CD20 (immunohistochemistry, routine), TP53 and
p53 (immunohistochemistry at 97.3% concordance, plus two commercial NGS panels), TRAF3 (commercial NGS panels),
B-lineage switch (PARR plus immunohistochemistry -- the assays exist and the missing piece is the relapse
sample). Partly: P-gp, BCL2, antigen density, PIK3CD, cerebrospinal-fluid cytology. Not at all: BCRP/ABCG2,
persister state, autophagy flux, PD-L1 (published but not commercial), MGMT, CD7, dCK, TOP2A, XPO1 codon 528,
RFC, CD47, CD19, occult CNS seeding.

**The asymmetry worth recording.** The escapes a veterinary oncologist can see are not the escapes that decide
the model's closure. Class II MHC, CD34, CD20, TP53 and TRAF3 are purchasable; E5's conjunction, the persister
state, dCK, XPO1 C528S and occult CNS seeding are not -- and E5 and the CNS seeding fraction are precisely the
two items the record identifies as carrying the brain arm (`LYMPHOMA_STATUS.md:238`, `:387`). An escape nobody
can measure is one nobody treats, and the converse also holds here: the one escape that **has** been measured
and attacked in a randomised canine trial (E5, in 28357033) is the one the model also finds hardest. Nothing in
this file is an input to a closure claim, and nothing in it changes a grade: it is the prior-art column the
record did not have.

---

## 4. Reference list (PMID, DOI) -- fetched in this session unless marked

Canine: 8646690 10.1002/(SICI)1097-0142(19960501)77:9<1892::AID-CNCR20>3.0.CO;2-U; 29958524 10.1556/004.2018.028;
23535752 10.5326/JAAHA-MS-5843; 23834200 10.1111/vco.12051; 28357033 10.12688/f1000research.6055.3;
25512102 10.1111/vcp.12221; 39134766 10.1038/s41598-024-69716-6; 33025640 10.1111/vco.12656;
32002286 10.1080/2162402X.2019.1676615; 42480604 10.1158/1535-7163.MCT-26-0365; 42969556 10.1093/jvimsj/aalag283;
41742528 10.1093/jvimsj/aalaf039; 27401141 10.1038/mt.2016.146; 32329214 10.1111/vco.12602;
42247661 10.1093/jvimsj/aalag098; 39042399 10.1158/1078-0432.CCR-23-2266; 33000710 10.1177/1040638720963132;
36552451 10.3390/ani12243531; 40842370 10.1111/vde.70021; 31777108 10.1111/vcp.12805;
25041580 10.1111/vco.12109; 6547126 (no DOI, JAVMA 1984;184:809-13).

Human and other: 20716770 10.1182/blood-2010-04-277269; 19949935 10.1007/978-1-60761-416-6_19;
38899693 10.1056/NEJMoa2401532; 38899699 10.1056/NEJMe2405437; 38497149 10.3324/haematol.2023.284281;
15980154 10.1073/pnas.0501870102; 16154360 10.1016/j.semcancer.2005.07.002; 29686021 10.1158/0008-5472.CAN-17-1201;
37674391 10.1080/10428194.2023.2254428; 36093297 10.18632/oncotarget.28258; 37645778 10.1101/2023.02.19.529123;
41737272 10.2147/ITT.S572396; 31577606 (lineage switch after CD19 CAR-T; metadata only, not read this pass).

Carried from the project record (`docs/universe/SWEEP_escapes.md` section 6), not re-fetched in this session:
canine 25475167, 36010910, 23820219, 23167606, 21777289, 30238600, 26678182, 39282821, 39922874, 25468570,
33323169, 40506464, 21781170, 36635848, 26130852, 34538134, 31943234, 38471970, 20362310, 21320018, 36433867,
40872651, 33816589, 23735731, 37837199, 17981339, 27856424, 39132435, 34209830, 29380929, 37884996, 22293625,
28735665, 34438760, 14627096, 20337920, 27434128 (from the catalogue, not the sweep list);
human 24972933, 18574145, 15327516, 18028428, 27634897, 42671910, 37683180, 22228637, 37391168, 31962268,
32589730, 30380386, 32342603, 40700581, 37751299, 32708132, 34799485, 40193715, 30760464, 33154951, 36584673,
39528665, 41236719, 34830747 (title/metadata only).

Web, no PMID (labelled as such in the rows above): Vidium Animal Health SearchLight DNA panel via Antech
(120 genes, 482,000 bp, MDR1 host marker, 9-12 day turnaround); Colorado State University Clinical Immunology
Laboratory eight-tube canine flow panel including Class II MHC-FITC / CD34-PE; ImpriMed 13-drug commercial
panel; Gilead statements on discontinuing magrolimab haematology development (ENHANCE, ENHANCE-3); Fondazione
Italiana Linfomi national survey of CNS prophylaxis practice; CD20-loss-at-relapse frequency (~12%) in a
rituximab-exposed cohort; PI3K-delta inhibitor lymphoma indication withdrawals.

Source: PubMed (NCBI). DOIs as returned by PubMed.
