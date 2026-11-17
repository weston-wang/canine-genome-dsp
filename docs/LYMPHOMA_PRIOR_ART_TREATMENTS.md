# Prior art for the eight-treatment canine lymphoma durable-response programme

**Question answered:** for each of the eight treatments, has anyone actually used it **in dogs with lymphoma** — alone, in
combination with any of the other seven, and as **long-term maintenance** — and where the published use stopped short of
what this programme needs, what reason do the papers themselves give?

Date: 2026-11-16. Source of every citation: PubMed (searched and metadata/full text fetched this session) plus the
project record. Where a paper is quoted, the quote is from the abstract or the PMC full text as marked. Web-only
statements are labelled WEB.

**Record check (CLAUDE.md rule 1).** Every row below is labelled **ALREADY IN RECORD (file:line)** or **NEW**. The files
grepped were `docs/LYMPHOMA_UNIVERSE.md`, `docs/LYMPHOMA_STATUS.md`, `docs/LYMPHOMA_COVERAGE_LEDGER.md`,
`docs/LYMPHOMA_DURABLE_RESPONSE.md`, `docs/universe/*.md`, `docs/research_notes/**`, `docs/reports/**` and `src/`.
Grep was by PMID **and** by keyword, per rule 10.

**Success criteria this document is graded against (user's words, verbatim).** "make sure every mechanism and every
escape is closed by either real data or rigorous model, potency, toxicity etc all need to be considered"; "looking for
10+ years of durability"; "assuming early detection"; "I'm okay with no specific data but if scientifically sound";
"I'm not asking if it's been demonstrated, I know it's not." **This document is a prior-art census, not a gap list.**
Absence of a published canine precedent for a component is recorded here as *absence of precedent*, which is a fact
about the literature; it is **not** reported as an open gap in the model, because under the stated bar a written
transfer or derivation is closure (rule 11). Where the model's basis for a component is a transfer already graded in
the record, that is named.

---

## 1. Verdinexor (Laverdia-CA1, XPO1 inhibitor) — programme sustains ~168 d (body), longer in the brain arm

**Used in canine lymphoma? YES — this is the single best-evidenced agent of the eight, and the only one FDA-approved
for the indication.**

- Largest series: **phase II, n = 58** naive or progressive B- and T-cell lymphoma, single agent oral KPT-335.
  "Treatment with single-agent, orally administered KPT-335 resulted in an objective response rate (ORR) of 37%, of
  which dogs with T-cell lymphoma had an ORR of 71%." Most common AE grade 1–2 anorexia.
  PMID 30143046, [doi 10.1186/s12917-018-1587-9](https://doi.org/10.1186/s12917-018-1587-9).
  **ALREADY IN RECORD** (`docs/universe/SWEEP_inhibitors_partial.md:165`; `docs/universe/SWEEP_xpo1_cns.md:3`).
- Pivotal FDA field study: **134 dogs analysed (106 verdinexor, 28 control), TTP 37 d (CI 29–57) vs 23 d (CI 14–30),
  p = 0.011**; serious AEs 22% (28/127) vs 15.2%. FDA FOI, NADA 141-614 (WEB, FOI PDF opened in an earlier session).
  **ALREADY IN RECORD** (`docs/universe/SWEEP_sustain.md:48`).
- Phase I: responders' TTP 66–83 d; median response duration 18 d in the record's reading. PMID 24503695,
  [doi 10.1371/journal.pone.0087585](https://doi.org/10.1371/journal.pone.0087585).
  **ALREADY IN RECORD** (`docs/universe/SWEEP_modalities.md:55`).
- Cutaneous epitheliotropic T-cell lymphoma pilot, **n = 8**: 75% CR/PR/SD, **mean time to progression 56 ± 41 d**.
  PMID 39074816, [doi 10.1111/vde.13280](https://doi.org/10.1111/vde.13280).
  **ALREADY IN RECORD** (`docs/universe/SWEEP_tcell_agents.md:26`).

**Combination with any of the other seven — in dogs, in vivo: ONE, and only with prednisolone, informally.**

| pairing | published canine evidence | size | outcome |
|---|---|---|---|
| verdinexor + **prednisolone/prednisone** | phase II (PMID 30143046): anorexia "was responsive to symptomatic and supportive medications, **including prednisone**" — co-administration, not a designed arm, no separate efficacy readout. CETL pilot (PMID 39074816): "Adjunctive therapy with lokivetmab **or prednisone** was permitted after Day (D)14", and the paper reports verdinexor "given as a monotherapy or concurrently with lokivetmab ± glucocorticoids" | n = 58 and n = 8 | no combination-specific response rate reported in either paper | **NEW** (the co-administration detail; the PMIDs themselves are in record) |
| verdinexor + doxorubicin or vincristine | **in vitro only**, four canine lymphoma cell lines: "Combination treatments significantly suppressed cell proliferation compared with single agents." PMID 41285475, [doi 10.1292/jvms.25-0478](https://doi.org/10.1292/jvms.25-0478) | 4 cell lines | preclinical; doxorubicin/vincristine are **not** among the eight | **ALREADY IN RECORD** (`docs/universe/SWEEP_modalities.md:133`, `SWEEP_escapes.md:41`) |
| verdinexor + doxorubicin (canine osteosarcoma lines) | "demonstrated synergetic activity in three canine OS cell lines"; verdinexor IC50 21–74 nM. PMID 33438820, [doi 10.1111/vco.12680](https://doi.org/10.1111/vco.12680) | cell lines | not lymphoma | **NEW** |
| verdinexor + radiation | one dog, **refractory multiple myeloma** (not lymphoma): "Verdinexor achieved the longest period of stable remission with minimal toxicity **post-RT**". PMID 40867733, [doi 10.3390/ani15162405](https://doi.org/10.3390/ani15162405) | n = 1 | ~3 months stable, relapse day 190 | **ALREADY IN RECORD** (`docs/universe/SWEEP_xpo1_cns.md:45`) |
| verdinexor + cytarabine, + intrathecal methotrexate, + hydroxychloroquine, + romidepsin, + whole-brain RT, + allogeneic HCT | **NOT FOUND** in any species for the last five; no canine publication for any of them | — | — | **NEW (as an explicit negative)** |

**Maintenance use — YES, and it is the only one of the eight whose sustained use is on-label.**

- Label: 1.25 mg/kg PO **twice weekly** (≥72 h apart), up to 1.5 mg/kg, **continued until progression** — i.e. sustained
  dosing is the approved schedule. FDA full approval 2026-01-16 (conditional 2021-01-11). WEB/FOI.
  **ALREADY IN RECORD** (`docs/universe/SWEEP_legal.md:19`; `SWEEP_sustain.md:48`).
- Longest documented **continuous** canine exposure: **17 months in one dog** with cutaneous epitheliotropic T-cell
  lymphoma, still in CR at report. PMID 39235783, [doi 10.5326/JAAHA-MS-7443](https://doi.org/10.5326/JAAHA-MS-7443).
  **ALREADY IN RECORD** (`docs/universe/SWEEP_sustain.md:10,50`).
- FDA dose-expansion partial responses lasting **246 and 354 days**. WEB/FOI. **ALREADY IN RECORD** (`SWEEP_sustain.md:50`).
- Pivotal-study dogs were followed with CBC/chemistry **to day 56 only**; chronic toxicology is a **13-week** study in 32
  healthy beagles, which found "lower testes, thymus, thyroid/parathyroid weights with histologic lesions in testes,
  epididymides, thymus". So ~168 d is **just outside** the longest controlled safety observation and inside the
  single-dog clinical experience. **ALREADY IN RECORD** (`SWEEP_sustain.md:49-50`).

**Stated reason the published use stopped where it did.**
- Phase II authors, verbatim: the data "**support continued evaluation of SINE compounds such as KPT-335 in combination
  with standard chemotherapeutics in canine lymphoma**" — i.e. the combination study was named as future work and, as of
  this search, has not been published. PMID 30143046. **NEW** (as a stated reason).
- CETL pilot conclusion: "Verdinexor could be considered a **safe, palliative** treatment for canine CETL" —
  palliative framing, trial design was an open-label pilot with assessment "every 14 days for 3 months, then monthly"
  (mean 70 ± 43.4 days). PMID 39074816. **NEW** (as a stated reason).
- FDA FOI: "an anti-neoplastic drug treating a terminal disease; adverse reactions are expected"; no chronic (>13 wk)
  toxicology in the FOI. **ALREADY IN RECORD** (`SWEEP_sustain.md:49`).
- Myeloma case: verdinexor **stopped at day 224** for lethargy, nausea, fever, diarrhoea and cytopenia when combined
  with other agents — a toxicity stop. PMID 40867733. **ALREADY IN RECORD** (`SWEEP_xpo1_cns.md:45`).

**Lawful status for a US vet: FDA-approved ANIMAL drug for canine lymphoma.** Full approval; sustained twice-weekly home
dosing is on-label. **ALREADY IN RECORD** (`docs/universe/SWEEP_legal.md:19`).

---

## 2. Prednisolone (T-cell arm)

**Used in canine lymphoma? YES — the best-quantified single agent of the eight, and the quantification is of its
failure as a single agent.**

- Largest single-agent series: **Canine Lymphoma Steroid Only (CALYPSO/CLASS) trial, n = 109 client-owned dogs,
  15 US institutions**, previously untreated peripheral nodal intermediate/large-cell lymphoma, prednisone 40 mg/m²
  PO q24h × 7 d then 20 mg/m² q24h. "**Median overall survival time was 50 days (95% CI, 41 to 59 days)**"; survival
  associated with substage and immunophenotype; "**No variables were predictive of long-term (> 120 days) survival.**"
  PMID 34125606, [doi 10.2460/javma.259.1.62](https://doi.org/10.2460/javma.259.1.62).
  **ALREADY IN RECORD** (`docs/universe/SWEEP_growth_bar.md:23`; `docs/LYMPHOMA_UNIVERSE.md:317`).
- 992-dog pathology cohort with treatment stratified as "absence of treatment, chemotherapy with or without
  hydroxydaunorubicin, and **only prednisone**"; prednisone-only medians are not broken out in the abstract.
  PMID 23444036, [doi 10.1177/0300985813478210](https://doi.org/10.1177/0300985813478210). **NEW**.
- Upfront steroid exposure is a **negative** prognostic signal: in 67 steroid-pretreated DLBCL dogs (median dose
  1 mg/kg, median duration 8 d, range 1–1080 d), "TTP (p = 0.003) and LSS (p < 0.001) were significantly longer in
  non-pre-treated dogs", while dose and duration had no effect. PMID 40624957,
  [doi 10.1111/vco.70004](https://doi.org/10.1111/vco.70004). **ALREADY IN RECORD**
  (`docs/research_notes/Canine lymphoma new treatments 2026/canine_trials_publications.md`).

**Combination with the other seven — YES, more than any other agent, because prednisone/prednisolone is a component of
every canine CHOP-type backbone.**

| pairing | published canine evidence | size | outcome |
|---|---|---|---|
| prednisolone + **cytarabine CRI** | CEOP (cyclophosphamide, epirubicin, vincristine, **prednisolone**) + a single cytarabine CRI, dogs with BM or CNS involvement. PMID 31769013, [doi 10.1111/avj.12895](https://doi.org/10.1111/avj.12895) | **n = 26** | toxicity study: GI toxicity 65.3%, grade III/IV 19.2%; neutropenia 34.6%; no efficacy endpoint reported | **ALREADY IN RECORD** (`docs/universe/SWEEP_exists.md:41`, `SWEEP_cnsregimens.md:143`) |
| prednisolone + **cytarabine 5-day CRI** | VCAA ± ara-C 150 mg/m²/day IV CRI × 5 consecutive days, stage V (BM-involved) lymphoma: CR 8/9 (ara-C) vs 2/8 (p < 0.01); **median survival 243 d (73–635) vs 72.5 d (6–174), p < 0.001**. PMID 19178667, [doi 10.1111/j.1476-5829.2007.00141.x](https://doi.org/10.1111/j.1476-5829.2007.00141.x) | **n = 17** | the strongest canine evidence that adding cytarabine CRI to a multi-agent backbone helps. (VCAA = vincristine, cyclophosphamide, adriamycin, asparaginase; prednisolone is part of the protocol family but the abstract does not itemise it — flagged as not fully verified) | **NEW** |
| prednisolone + **intrathecal cytarabine + intrathecal methotrexate** | one dog: modified L-LOP (includes prednisolone) + systemic cytarabine, then IT cytarabine + methotrexate in the cisterna magna with **systemic dexamethasone**. PMID 37732143, [doi 10.3389/fvets.2023.1209935](https://doi.org/10.3389/fvets.2023.1209935) | **n = 1** | CNS remission 3.5 weeks; euthanised 9 weeks after diagnosis | **ALREADY IN RECORD** (`docs/universe/SWEEP_exists.md:106`, `SWEEP_itmtx2.md:4`) |
| prednisolone + **half-body RT (head in field)** | L-CHOP (**P = prednisone**) + low-dose-rate sequential HBRT. PMID 42525883, [doi 10.1093/jvimsj/aalag144](https://doi.org/10.1093/jvimsj/aalag144) | **n = 75 vs 115 controls** | PFS 532 d vs 296 d; OS 752 d vs 457 d (p < .0001) | **ALREADY IN RECORD** (`docs/LYMPHOMA_STATUS.md`; `SWEEP_exists.md:120`) |
| prednisolone + **half-body RT** (second protocol) | CHOP or MOPP + 4 Gy × 2 cranial then 4 Gy × 2 caudal. PMID 40088118, [doi 10.1111/vco.13050](https://doi.org/10.1111/vco.13050) | **n = 14 vs 11** | median PFI 1143 d vs 316 d; median ST 1924 d vs 566 d | **ALREADY IN RECORD** (`SWEEP_rt2.md`, `SWEEP_exists.md:122`) |
| prednisolone + **allogeneic DLA-identical HCT** | induction was "multiagent chemotherapy such as CHOP" before alloHCT; conditioning itself was TBI + cyclosporine, no prednisolone. PMID 35789057, [doi 10.1111/vco.12847](https://doi.org/10.1111/vco.12847) | n = 15 | prednisolone is pre-transplant induction only, not concurrent | **ALREADY IN RECORD** (`SWEEP_hct_model.md:19`) |
| prednisolone + **verdinexor** | permitted adjunct in two verdinexor studies (see §1) | n ≤ 8 reported | not analysed separately | **NEW** |
| prednisolone + **hydroxychloroquine** | **NOT FOUND**. The canine HCQ trial (PMID 24991836) is HCQ + doxorubicin; the abstract does not report concurrent prednisone, and the full text is not in PMC (PMC4203518 returns an empty body) | — | — | **NEW (negative)** |
| prednisolone + **romidepsin** | **NOT FOUND** in dogs | — | — | **NEW (negative)** |

**Maintenance use — YES, historically, and it was deliberately abandoned.** In the CHOP-type backbones prednisone is
given only as a **4-week taper** (Lai 2025 Table 1, read in PMC: "2 mg/kg PO q24 h for 7 days, then 1.5 … then 1.0 …
then 0.5 … then stop"), i.e. the canine literature contains essentially **no long-term prednisolone maintenance for
lymphoma**, by design. PMID 40088118 (PMC12082781, full text read). **NEW**.
The 1080-day steroid duration in one dog of PMID 40624957 is the longest canine lymphoma steroid exposure found, and it
was pre-treatment, not protocolised maintenance. **NEW**.

**Stated reasons.**
- CALYPSO authors: "Results suggested that **survival times were short** for dogs … treated with prednisone alone …
  Findings provide potentially important information **for clinicians to discuss with owners of dogs with lymphoma at
  the time treatment decisions are made**" — the trial existed to quantify a palliative option for owners declining
  chemotherapy, so a multi-year horizon was never its design. PMID 34125606. **NEW** (as a stated reason).
- PMID 40624957 authors: "**corticosteroids should be used with caution and reserved for cases where clinical benefits
  clearly outweigh the risks**" — an explicit argument against prolonging steroid exposure. **NEW** (as a stated reason).
- The record already carries the mechanistic counterpart: glucocorticoid-receptor loss (escape E1) is
  "Phenotypic, **exposure-driven** (rises with GC exposure, median 68 d)". **ALREADY IN RECORD**
  (`docs/universe/SWEEP_escapes.md:65`).

**Lawful status for a US vet:** prednisolone/prednisone tablets exist as **FDA-approved animal drugs**; oncologic use at
these doses and durations is **extra-label use of an approved animal drug** (lawful under AMDUCA with a valid VCPR). I
did not retrieve a specific NADA number this session — flagged as **not verified**. Prednisone/prednisolone is not in
`docs/universe/SWEEP_legal.md`'s table, so its status line is **NEW**.

---

## 3. Cytarabine as a constant-rate IV infusion (CRI) — programme uses weekly repetition

**Used in canine lymphoma? YES, in combination; essentially never as a single agent.**

| study | design | numbers |
|---|---|---|
| PMID 19178667 (Marconato 2008) **NEW** | VCAA ± ara-C **150 mg/m²/day IV CRI × 5 consecutive days**, stage V lymphoma with BM involvement | **n = 17** (8 vs 9). CR 2/8 vs **8/9** (p < 0.01). Median survival **72.5 d vs 243 d** (p < 0.001). "Both protocols were well tolerated, with a low incidence of adverse events." |
| PMID 31769013 (Guillen 2019) **ALREADY IN RECORD** (`SWEEP_exists.md:41`) | CEOP + **single** cytarabine CRI, BM or CNS involvement | **n = 26**. GI toxicity 17/26 (65.3%), grade III/IV 5 (19.2%); neutropenia 9 (34.6%); thrombocytopenia 3 (11.5%); 5 dogs (19.2%) hospitalised; treatment delays in 5 (median 4 d) |
| PMID 1742843 (Scott-Moncrieff 1991) **ALREADY IN RECORD** (`SWEEP_exists.md:37`) | healthy dogs, 12-h CRI 50 mg/m²/h — the PK basis for CSF reach | CSF steady state **8.3 ± 1.1 µM**, plasma 14.1 µM, **CSF:plasma 0.62 ± 0.14**; "No clinically significant toxicity was observed over a 21-day period" |

**Combination with the other seven — YES, two pairings, both with prednisolone-containing backbones, and one with
intrathecal methotrexate.**
- cytarabine CRI + prednisolone-containing multi-agent chemotherapy: PMIDs 19178667 and 31769013 above.
- cytarabine (IT, not CRI) + **intrathecal methotrexate**: PMID 25041580 (112 dogs + 8 cats, "cytosine arabinoside
  alone or in combination with methotrexate", one generalised seizure in 120 animals) and PMID 37732143 (n = 1).
  **ALREADY IN RECORD** (`docs/LYMPHOMA_STATUS.md`; `SWEEP_itmtx2.md:72`, `:4`).
- cytarabine CRI + **half-body or whole-brain RT**: **NOT FOUND**. **NEW (negative)**.
- cytarabine CRI + **verdinexor / hydroxychloroquine / romidepsin / allogeneic HCT**: **NOT FOUND** in dogs.
  (Cytarabine is not part of any published canine transplant conditioning; canine conditioning is TBI, high-dose
  cyclophosphamide or busulfan — `SWEEP_hct_model.md:19,212`.) **NEW (negative)**.

**Maintenance use — the longest canine cytarabine exposure found is PULSED and in a non-neoplastic disease.**
- **n = 43 dogs with meningoencephalomyelitis of unknown origin**, cytarabine 600 mg/m² **every 3–6 weeks for ≥6 months
  or until death**, minimum follow-up 24 months: 23/25 survived >24 months (median 1027 d, range 770–1277);
  "No serious adverse events were noted." PMID 41742567,
  [doi 10.1093/jvimsj/aalaf082](https://doi.org/10.1093/jvimsj/aalaf082). **ALREADY IN RECORD**
  (`docs/universe/SWEEP_sustain.md:30`). This is the only canine evidence that cytarabine can be given for years — but
  the interval is 3–6 weeks, not weekly, and the disease is inflammatory, not neoplastic.
- In **lymphoma**, every published canine cytarabine schedule is **one CRI** (PMID 31769013) or **one 5-day CRI block**
  (PMID 19178667). **Weekly repetition of a cytarabine CRI in a dog with lymphoma: NOT FOUND.** **NEW (negative)**.
- A rare tail hazard of repeated CRI exists: fatal drug-induced interstitial lung disease after a **4th** cytarabine CRI
  (300 mg/m²) in a dog with MUO. PMID 27062671. **ALREADY IN RECORD** (`SWEEP_sustain.md:34`).

**Stated reasons.**
- Guillen 2019 conclusion, verbatim: "Our findings suggest that **gastrointestinal toxicity should be expected** in
  lymphoma patients undergoing cytarabine CRI." The paper was designed as a **toxicity** study only — it reports no
  efficacy endpoint at all. PMID 31769013. **ALREADY IN RECORD** as a toxicity line (`SWEEP_exists.md:41`); the
  design-limit reading is **NEW**.
- Marconato 2008 conclusion: ara-C "appears to be safe and beneficial in dogs with stage V lymphoma. **Incorporation of
  the nucleoside analogue might be crucial for the development of future therapeutic strategies in dogs**" — again,
  further work named, n = 17, no maintenance arm. PMID 19178667. **NEW**.

**Lawful status for a US vet:** cytarabine injection is an **FDA-approved human drug**; use in a dog, and the CRI
route/schedule, is **extra-label**. Intrathecal use requires a preservative-free formulation (not verified this session).
**NEW** (cytarabine is not in `SWEEP_legal.md`'s table).

---

## 4. Methotrexate injected intrathecally (2.5 mg flat, every 10–14 days, 16–45 doses)

**Used in canine lymphoma? YES, but only once, in one dog, for one course.**

- **PMID 37732143** (Lyseight 2023): the only canine report of intrathecal methotrexate for lymphoma. 4-year-old dog,
  multicentric lymphoblastic B-cell lymphoma stage Vb with meningeal/spinal cord infiltration at L3. IT cytarabine +
  methotrexate into the **cisterna magna** with systemic dexamethasone. "Clinical signs were resolved within 24 h, and
  the patient remained asymptomatic for 3.5 weeks … intrathecal chemotherapy with methotrexate and cytarabine can
  induce a **short-lasting CNS clinical remission (3 weeks)**." Repeat IT chemotherapy was **declined**; euthanised at
  9 weeks. **ALREADY IN RECORD** (`docs/universe/SWEEP_exists.md:106`; `SWEEP_cnsregimens.md:119`; `SWEEP_itmtx2.md:4`).
- Safety denominator: **PMID 25041580** (Genoni 2014), 112 dogs + 8 cats given IT cytosine arabinoside alone or with
  methotrexate for suspected inflammatory or neoplastic CNS disease, Sept 2008–Dec 2013: one of 120 animals had a
  generalised tonic-clonic seizure in anaesthetic recovery, diazepam-responsive; authors conclude the procedure "is a
  safe procedure in dogs and cats". The abstract does **not** state the dose or the route; the 2.5 mg flat cisternal
  dose reaches the record **only** via Lyseight's citation of Genoni (secondary). **ALREADY IN RECORD**
  (`docs/universe/SWEEP_itmtx2.md:72`, which already flags the dose as SECONDARY and Genoni's full text as unobtainable).

**Combination with the other seven — YES, two: IT methotrexate + IT cytarabine, and both of those on top of a
prednisolone-containing systemic protocol (PMID 37732143, n = 1).** No published canine pairing of IT methotrexate with
verdinexor, hydroxychloroquine, romidepsin, brain radiotherapy or allogeneic HCT. **NEW (negative)**.

**Maintenance use — NO. The programme's 16–45 doses have no canine precedent at any interval.**
The record's own search of repeated intra-CSF dosing in dogs (`docs/universe/SWEEP_itmtx2.md:121-137`) found:
- repeated **percutaneous cisternal** puncture documented only to **4 doses over 4 months** (Dickson 2007, MPS I dogs,
  PMID 17321776) and **6 doses over 3 weeks** in one dog (anecdote via Lyseight's reference 13);
- the only configuration that has run for 8–11 months in dogs is an **implanted ventricular/lumbar catheter to a
  subcutaneous titanium port**, biweekly, in TPP1-null Dachshunds (≈20–28 CSF-route doses per dog; PMID 25257657 /
  PMC4263309) — a **non-oncologic enzyme-replacement** setting, with 2 dogs lost to meningitis plus obstructive
  hydrocephalus and frequent catheter occlusion/migration;
- chronic lumbar IT catheter + vascular access port patency **67% beyond 30 days** (PMID 24694254).

So the dose count the programme needs has a **device precedent** in dogs and **no drug precedent in lymphoma**.
**ALREADY IN RECORD** (`SWEEP_itmtx2.md:121-137`, including the conclusion "Ommaya use in a dog: still NOT FOUND" and
"Canine arachnoiditis or myelopathy specifically after intrathecal chemotherapy: NOT FOUND").

**Stated reasons the published use stopped where it did.**
- Lyseight 2023: the stop is explicit and is **owner declination**, not toxicity — "CNS relapse … was suspected, and
  **repeat intrathecal chemotherapy was declined**. The patient was humanely euthanized 9 weeks after the initial
  diagnosis." PMID 37732143. **NEW** (the reason itself; the case is in record).
- Genoni 2014: design limit stated in the title and objective — "**the short-term safety** of intrathecal
  administration"; AEs were recorded only "during administration while recovering from anaesthesia and during
  hospitalization period". No follow-up, no efficacy, no repeat-dosing data by design. PMID 25041580. **NEW**.
- The record adds: "Nothing newer than 2023 on IT chemotherapy in dogs: PubMed 'intrathecal dogs lymphoma methotrexate'
  returns exactly 1 record (37732143)" — re-verified this session, still 1. **ALREADY IN RECORD** (`SWEEP_itmtx2.md:165`).

**Lawful status for a US vet:** methotrexate injection is an **FDA-approved human drug**; canine use and the intrathecal
route are **extra-label** (preservative-free product required). **NEW**.

---

## 5. Hydroxychloroquine (autophagy inhibition)

**Used in canine lymphoma? YES — one phase I trial, in combination, and it is the only canine HCQ oncology study.**

- **PMID 24991836** (Barnard 2014, Autophagy): phase I single-arm dose escalation, **n = 30** dogs with spontaneous NHL
  at an academic teaching hospital. HCQ daily PO throughout, started 72 h before doxorubicin (IV, 21-day cycle).
  "HCQ alone was well tolerated with only mild lethargy and gastrointestinal-related adverse events. The **overall
  response rate (ORR) for dogs with lymphoma was 93.3%**, with **median progression-free interval (PFI) of 5 mo.**
  Pharmacokinetic analysis revealed a **100-fold increase in HCQ in tumors compared with plasma.**"
  **ALREADY IN RECORD** (`docs/universe/SWEEP_modalities.md:29`; `docs/LYMPHOMA_COVERAGE_LEDGER.md:129`).

**Combination with the other seven — NONE.** The published canine combination is **HCQ + doxorubicin**, and doxorubicin
is not one of the eight. No canine publication pairs HCQ with verdinexor, prednisolone, cytarabine, intrathecal
methotrexate, romidepsin, brain radiotherapy or transplant. **NEW (negative)** — the record carries the trial but had
not stated the combination census.

**Maintenance use — NO canine lymphoma maintenance; ~1–1.5 years exists in canine dermatology at a lower dose.**
- German Shorthaired Pointers with exfoliative cutaneous lupus: HCQ **5–10 mg/kg once daily for 8 weeks, 7 months and
  9 months**, "no side effects"; two male dogs "**maintained on hydroxychloroquine for another year**"; the authors say
  theirs is "the **first to address the safety of long-term administration of hydroxychloroquine, albeit in a small
  number of dogs**". PMID 20374572, [doi 10.1111/j.1365-3164.2010.00867.x](https://doi.org/10.1111/j.1365-3164.2010.00867.x).
  One further dog at 5 mg/kg/day for a year, "adverse drug events were not seen", PMID 21718370.
  **ALREADY IN RECORD** (`docs/universe/SWEEP_sustain.md:52-54`).
- The dermatology dose (5 mg/kg) is **not** the antineoplastic MTD (12.5 mg/kg/day, PMID 24991836), and canine retinal
  toxicity data are NOT FOUND. **ALREADY IN RECORD** (`SWEEP_sustain.md:54`).

**Stated reason.** Barnard 2014, verbatim: "The superior ORR and comparable PFI to single-agent DOX provide **strong
support for further evaluation via randomized, placebo-controlled trials** in canine and human NHL." The study was a
**dose-finding phase I** whose stated purpose was "to determine a maximum dose of HCQ that can be combined with a
standard chemotherapy" — so stopping at 30 dogs and 5 months is the design, and the randomised follow-up it calls for
has not been published (searched this session). **NEW** (as a stated reason).

**Lawful status for a US vet: FDA-approved human drug, extra-label.** **ALREADY IN RECORD**
(`docs/universe/SWEEP_legal.md:24`, which also notes HCQ is "not load-bearing" in the current model).

---

## 6. Romidepsin (HDAC inhibitor, T-cell arm)

**Used in canine lymphoma? NO. There is no in-vivo canine romidepsin study of any kind, in lymphoma or otherwise.**

- The only canine romidepsin data found: an **ex-vivo 3D spheroid screen** of FDA-approved oncology drugs in
  **osteosarcoma**. "sarcospheres derived from ∼30% of human and **50% of canine patient samples** responded to
  romidepsin at clinically tolerable concentrations (ED50s < 70 nmol/L)". PMID 40952917,
  [doi 10.1158/2767-9764.CRC-25-0121](https://doi.org/10.1158/2767-9764.CRC-25-0121); preprint PMID 40475499.
  **ALREADY IN RECORD** (`docs/universe/SWEEP_inhibitors_partial.md:198`, which already states "lymphoma: NOT FOUND").
- Human T-cell lymphoma anchor (the model's transfer source): pivotal PTCL study n = 130, ORR 25%, CR/CRu 15%,
  "median duration of response was 17 months, with the longest response ongoing at 34+ months". PMID 22271479.
  **ALREADY IN RECORD** (`SWEEP_inhibitors_partial.md:192`).
- The model's romidepsin kill (k = 0.23/day) is a **written TRANSFER** from human MOLT-4 GI50 2.06 nM × human label
  exposure, and its CSF:plasma AUC of **2% in rhesus** (PMID 15042312) is why it is not a brain agent.
  **ALREADY IN RECORD** (`SWEEP_inhibitors_partial.md:198,200`; `SWEEP_tcell_agents.md:4`). Under rule 11 this is
  graded closure, not a gap; it is listed here because the *prior-art* answer is "no dog has received it".

**Combination with any of the other seven in dogs: NONE.** No in-vivo canine romidepsin exists, so no pairing can.
**NEW (negative)**.

**Maintenance use in dogs: NONE.** **NEW (negative)**.

**Stated reason — and this one is a hard constraint, not a funding limit.** The reason romidepsin has never been given
to a dog is that **dogs were the species in which it failed on cardiotoxicity**: "Romidepsin, a drug initially
**abandoned because of serious cardiotoxicity in dogs**, was successfully rescued for clinical evaluation **by tailoring
the dose regimen to mitigate cardiac toxicity risks**." PMID 23668378,
[doi 10.1517/14740338.2013.798300](https://doi.org/10.1517/14740338.2013.798300) (Safety Pharmacology Society meeting
report, keynote summary — secondary, conference-proceedings grade). The human label carries a delayed heart-rate
increase and QT signal. **NEW — and this is the single most consequential new finding in this document for the
programme**, because it is a species-specific, mechanism-level objection to the romidepsin arm that the record's
transfer derivation does not account for. It is recorded here as prior art; what it implies for the model is for the
model's own grading to decide (the record already notes romidepsin is "**Not load-bearing (checked)**",
`docs/LYMPHOMA_STATUS.md:309`, so no closure currently rests on it).

**Lawful status for a US vet: FDA-approved human drug, extra-label.** The relapsed/refractory PTCL indication was
withdrawn in 2021–22 after Ro-CHOP missed its endpoint, but romidepsin remains approved and marketed for **cutaneous**
T-cell lymphoma, so it is still extra-label-eligible; a ready-to-use solution was approved 4 Jun 2026.
**ALREADY IN RECORD** (`docs/universe/SWEEP_legal.md:23`;
`docs/research_notes/Canine lymphoma new treatments 2026/human_tcell_lymphoma.md:12`).

---

## 7. Whole-brain / craniospinal radiotherapy (23.4–36 Gy, 1.8 Gy fractions)

**Used in canine lymphoma? NO — not as prescribed brain irradiation. But the canine brain HAS been irradiated to 8 Gy
incidentally, inside the cranial half-body field, in dozens of dogs with lymphoma.**

This is the correction this section contributes. The record states "Whole-brain or craniospinal radiotherapy for canine
CNS lymphoma, doses, late toxicity: NOT FOUND as a series" (`docs/universe/SWEEP_exists.md:125`), which remains true for
*prescribed* brain RT. But the Lai 2025 full text (PMC12082781, read this session) states the cranial half-body field
**includes the head**: "The **head** and limbs **in the treatment field** were secured to the body with tape and wedge
sponges for positioning … Parallel opposed fields were used to deliver a homogeneous dose to the entire PTV (cranial or
caudal half of the body), with **the xiphoid process of the sternum serving as the landmark dividing the cranial and
caudal body**." So the brain received **4 Gy × 2 consecutive days = 8 Gy** in 14 dogs. **NEW**.

| study | protocol | numbers |
|---|---|---|
| PMID 40088118 (Lai 2025) **ALREADY IN RECORD**; head-in-field detail **NEW** | CHOP or MOPP; cranial HBI 4 Gy × 2 d at week 13, L-asparaginase week 15, caudal HBI week 17, chemo continued to week 25–29 | **14 HBI vs 11 control.** Median PFI **1143 d vs 316 d** (p = 0.004); median ST **1924 d vs 566 d** (p = 0.008). T-cell PFI 292 d vs B-cell 2127 d (p = 0.0013). 1-/2-/3-year survival in HBI group **79% / 71% / 43%**. Toxicity: grade 3–4 thrombocytopenia in 17%/25% of dogs 2 weeks post-caudal HBI, "All cases of thrombocytopenia appeared to be subclinical"; GI toxicity 21.4%; alopecia 36%, leukotrichia 21%. One necropsy: "**No evidence of pathological changes related to radiation therapy**" |
| PMID 42525883 (Colosi 2026) **ALREADY IN RECORD** (`SWEEP_exists.md:120`) | L-CHOP + sequential low-dose-rate HBRT (6 Gy per half, 8–14 cGy/min), **"without maintenance chemotherapy"** | **75 vs 115.** PFS 532 d vs 296 d; OS 752 d vs 457 d (p < .0001). Grade 3–4 toxicity in 4.5% of treatments; 1 hospitalisation; 39 dose reductions and 74 delays over the 28-week protocol |
| PMID 15515588 (Williams 2004) **ALREADY IN RECORD** (`SWEEP_rt3_escalation.md:85`) | induction chemo then 4 Gy × 2 per half, 3-week interval, cobalt-60 | 94 dogs induced, 73 (78%) CR, **52 irradiated**. Median first remission **311 d**; median overall remission 486 d. Toxicoses "generally were mild and infrequent" |
| PMID 19379300 (Gustafson 2004) **ALREADY IN RECORD** (`SWEEP_rt3_escalation.md:87`) | 4 Gy × 2 per half interposed in a CHOP-based 25-week regimen | **n = 6.** Median remission 455 d, survival 560 d. "Late effects from RT were not evident" |
| PMID 28133821 (Santoro 2017) **NEW** | **total skin electron therapy** 6 Gy per half, 15 days apart, for canine mycosis fungoides | **n = 1.** CR, "kept in remission with no additional treatments for **19 months** before relapse and development of Sézary syndrome" — the longest single-course radiation remission in a canine lymphoid malignancy found |
| PMID 41929729 (Han 2026) **NEW** | RT to mediastinal and submandibular masses after L-CHOP relapse, T-cell | **n = 1.** Lesions regressed, but progression to multicentric disease; died after lomustine rescue |

**Combination with the other seven — YES, with prednisolone (as part of L-CHOP/CHOP/MOPP) and with L-asparaginase, in
all five RT series above.** No canine series combines brain-field radiation with verdinexor, cytarabine CRI,
intrathecal methotrexate, hydroxychloroquine, romidepsin or transplant. The only verdinexor+RT dog is the myeloma case
(PMID 40867733). **NEW (negative, except the prednisolone pairing which is in record).**

**Maintenance use — not applicable to RT itself, and the RT series are explicitly *maintenance-free*.** Colosi 2026's
title is "…L-CHOP **without maintenance chemotherapy**"; Lai 2025 stops chemotherapy at week 25–29.
**ALREADY IN RECORD** for Colosi (`SWEEP_exists.md:120`); the "RT series are deliberately maintenance-free" reading is
**NEW**.

**Stated reasons the published use stopped where it did.**
- **Williams 2004, the clearest stated reason in the whole canine lymphoma RT literature**: half-body RT "is well
  tolerated and **might increase remission duration** compared with conventional protocols that use chemotherapy alone,
  **but this increase might not be long enough to be clinically relevant or to justify application of the method
  described herein**." PMID 15515588. **NEW** (as a stated reason; the PMID is in record).
- Lai 2025: "an optimal protocol that **improves outcomes while minimising toxicity has not been established**"; dose
  escalation to total-body irradiation in one session "may significantly increase the bone marrow toxicity,
  necessitating a reduction in radiation dose and/or hospitalisation for monitoring"; and low dose rate "was expected
  to take 30–50 min to complete one fraction … **Prolonged anaesthesia time was considered a potential risk factor for
  complications**". PMC12082781. **NEW**. (This last point bears directly on the programme's 16–45 anaesthetics for
  intrathecal dosing — the same constraint, named by veterinary radiation oncologists.)
- Lai 2025 on why the question is not asked of poor responders: "this inclusion criterion **introduces a selection
  bias** because it excludes patients who did not respond to chemotherapy." **NEW**.
- Historical dose-finding reason: 1980s HBI at 7 Gy per half caused "bone marrow necrosis, tumour lysis syndrome and
  secondary haemorrhagic gastroenteritis"; 1960s whole-body 2 MV irradiation caused "significant bone marrow
  suppression and widespread bleeding secondary to thrombocytopenia in one dog" (Lai 2025 Introduction, citing the
  primary 1960s/1980s papers which I did not fetch — secondary). **NEW**.
- No canine paper gives a reason for *not* escalating to 23.4–36 Gy to the brain in 1.8 Gy fractions, because **no
  canine paper proposes it**. **No reason stated** (nothing to quote).

**Lawful status for a US vet: a procedure**, performed under a valid VCPR at a facility with a linear accelerator; not
a drug and not subject to AMDUCA. Canine linac infrastructure for exactly these fields exists (Varian 21EX, 6 MV,
PMC12082781) and canine TBI dosimetry is multi-site validated (PMID 31146304). **ALREADY IN RECORD**
(`SWEEP_hct_model.md:203`).

---

## 8. Allogeneic DLA-identical haematopoietic cell transplant (incl. reduced-intensity ~2 Gy conditioning)

**Used in canine lymphoma? YES — and this is the one treatment of the eight with a published multi-year, explicitly
curative-intent canine lymphoma result.**

- **Largest series: PMID 35789057** (Gareau 2022), **15 dogs** with high-grade B-cell lymphoma, 2006–2018, four
  facilities (NCSU, Bellingham Veterinary, VCA West LA, MedVet Columbus). DLA-identical (8/8) mobilised donor PBSC;
  conditioning **TBI 2 × 4 Gy at 7.5–10 cGy/min** plus cyclosporine day −1 to ~day +30; 2–3 cryopreserved DLI aliquots
  held for relapse.
  Numbers: median DFI **1095 d** (9–2920) and OS **1115 d** (9–2920) for all 15. First-remission subgroup (n = 10):
  median DFI and OS **1235 d**. "**Eight of nine remaining dogs lived >4 yrs post-alloHCT, leading to a cure rate of
  89%.**" Chimerism ">95% donor WBC within 2 weeks" in 12/12 tested. TRM 2/15 (13%), both not in remission at
  transplant. Acute grade 2 cutaneous GVHD 3/13 (23%); **no chronic GVHD**.
  **ALREADY IN RECORD, extensively** (`docs/universe/SWEEP_hct_model.md:10-42`).
- Case report, T-cell lymphoma, DLA-identical **cousin** donor found by multigeneration family typing, 2 × 4 Gy TBI at
  7 cGy/min, cyclosporine: "full donor engraftment that has been **maintained for at least 58 weeks**". PMID 16506937,
  [doi 10.2460/javma.228.5.728](https://doi.org/10.2460/javma.228.5.728). **ALREADY IN RECORD** (`SWEEP_hct_model.md:61`).
- Historical Seattle allogeneic arms were failures: of 8 dogs given 8.4 Gy + **unrelated** donor marrow with
  post-transplant methotrexate and cyclosporine, "6 died within 2 weeks of transplant of infection and 2 died later of
  graft-versus-host disease". PMID 3887690,
  [doi 10.1097/00007890-198505000-00008](https://doi.org/10.1097/00007890-198505000-00008).
  **ALREADY IN RECORD** (`SWEEP_hct_model.md:60`).
- Autologous comparator (same centres): 5/15 (33%) of dogs transplanted before relapse remained in remission
  (PMID 22882500); 4/10 (40%) "cured" at ≥2 y with added expanded T cells, which "**does not provide a clinical benefit
  over CHOP chemotherapy and autoPBHSCT alone**" (PMID 34950726); T-cell autologous 2/13 alive at 741 and 772 d
  (PMID 24467413). **ALREADY IN RECORD** (`SWEEP_hct_model.md:50-53`).
- Programme volume and mortality: **94 dogs** received HCT after TBI at NCSU over 10 years; 7/94 (7%) died before
  discharge; 3 of 5 necropsied had systemic candidiasis. PMID 38695516,
  [doi 10.1177/03009858241249114](https://doi.org/10.1177/03009858241249114). **ALREADY IN RECORD**
  (`SWEEP_hct_model.md:190`).

**Reduced-intensity ~2 Gy conditioning: exists in dogs, but NOT in dogs with lymphoma.**
- **PMID 12931117** (Hogan 2003): DLA-identical **littermate** marrow after **2 Gy TBI** with post-grafting sirolimus +
  cyclosporine. "Dogs received either **2 Gy (n = 7) or 1 Gy (n = 5)** total body irradiation … **Durable engraftment
  was seen in 5 of 6 remaining dogs, with a median follow-up of >48 (range, >32 to >56) weeks.** … In the second cohort,
  **all 5 dogs rejected the marrow graft** at a median of 9 weeks." So 2 Gy is the floor dose that holds a graft and
  1 Gy is not. Healthy research dogs; **no lymphoma, no tumour endpoint**.
  [doi 10.1016/S1083-8791(03)00148-4](https://doi.org/10.1016/S1083-8791(03)00148-4). **ALREADY IN RECORD**
  (`docs/universe/SWEEP_hct_model.md:200`; `SWEEP_stemcell.md`; `SWEEP_persistent_graft.md`).

**Combination with the other seven — only with prednisolone, as pre-transplant induction.** All transplanted dogs were
induced to remission with "multiagent chemotherapy such as CHOP" (so prednisolone, pre-transplant, mean
diagnosis-to-transplant 118 d). Conditioning is TBI ± high-dose cyclophosphamide or busulfan — **never** verdinexor,
cytarabine CRI, intrathecal methotrexate, hydroxychloroquine, romidepsin, or brain-directed radiotherapy. There is **no
canine transplant series reporting relapse site**, so whether any transplanted dog relapsed in the CNS is unknown:
"CNS relapse rate after canine TBI+HCT: NOT FOUND". **ALREADY IN RECORD** (`SWEEP_hct_model.md:63,19,212`).

**Maintenance use — not applicable; the graft IS the sustained effector.** The relevant canine number is persistence:
>95% donor chimerism by 2 weeks, maintained at ≥58 weeks in the case report, and six dogs alive and disease-free out to
2920 days. Post-transplant immunosuppression is cyclosporine to ~day 30 only. **ALREADY IN RECORD**
(`SWEEP_hct_model.md:166`).

**Stated reasons the published use stopped where it did.**
- **Trial endpoint, stated**: "a trial end-point of **4.1 yrs**, since all dogs from all 3 studies who lived >2 yrs
  post-transplant have lived >4 yrs" (PMID 35789057 §2.8) — the follow-up horizon was set by design at ~4 years, which
  is **why no canine 10-year number exists**. **ALREADY IN RECORD** (`SWEEP_hct_model.md:29`).
- **Donor logistics, stated**: "**no bone marrow donor registries exist for dogs**"; each full sibling or
  parent-offspring pair has a 25% chance of matching, cousins 12.5%; mean 5 donors screened (range 1–28).
  PMID 35789057 Discussion. **ALREADY IN RECORD** (`SWEEP_hct_model.md:30,195`).
- **Dose escalation was tried and abandoned for toxicity, not funding**: 13.5 Gy vs 8.4 Gy TBI "led to an increased
  incidence of transplant-related deaths (**55% vs. 26%**) and **did not reduce the actuarial relapse rate**"; and
  "post-transplant therapy with methotrexate and cyclosporine was **poorly tolerated** in these animals".
  PMID 3887690. **ALREADY IN RECORD** (`SWEEP_hct_model.md:210`).
- **Cost and availability, stated in a review** (see cross-cutting Q4 below).
- **Programme interruption, WEB-sourced**: the NCSU programme was paused ~Feb 2023 for external review ("we are not
  accepting new bone marrow transplant patients at this time as we pause"), 13 dogs waitlisted; no resumption date
  found. **ALREADY IN RECORD** (`SWEEP_hct_model.md:192`, labelled WEB).

**Lawful status for a US vet: a procedure**, lawful under a VCPR at the handful of centres with TBI, apheresis, DLA
typing and ICU capability — "HCT for the treatment of lymphoma in dogs is available as a therapeutic option at a
**selected number of institutions within the United States**" (PMID 34390541, PMC8604109, full text read).
**ALREADY IN RECORD** (`SWEEP_hct_model.md:62,191`). Component drugs (cyclosporine, filgrastim, busulfan) are
extra-label.

---

## Cross-cutting question 1 — Has ANY canine lymphoma study combined a CNS-directed arm (intrathecal chemotherapy or brain radiation) with a systemic maintenance drug? Any at all, however small?

**Answer: no study combined an intrathecal arm with a systemic *maintenance* drug. Four things come close, and the
closest is n = 1.**

1. **Intrathecal + systemic induction, n = 1.** PMID 37732143: IT cytarabine + IT methotrexate into the cisterna magna,
   on a dog already on modified L-LOP (prednisolone-containing) with systemic cytarabine, plus systemic dexamethasone.
   This is the **only** canine publication combining an intrathecal arm with any systemic agent in lymphoma. The
   systemic drug was induction, not maintenance; the course was a single IT administration; CNS remission 3.5 weeks.
   **ALREADY IN RECORD** (`SWEEP_exists.md:106`).
2. **Intrathecal in a mixed cohort, no systemic arm reported.** PMID 25041580: 112 dogs + 8 cats, IT cytarabine ±
   methotrexate, inflammatory or neoplastic CNS disease, short-term safety only; concurrent systemic therapy is not
   reported. **ALREADY IN RECORD** (`SWEEP_itmtx2.md:72`).
3. **Brain-in-field radiation + concurrent systemic chemotherapy, n = 14 and n = 75.** PMIDs 40088118 and 42525883: the
   cranial half-body field includes the head (verified in PMC12082781), delivering **8 Gy** (4 Gy × 2) or **6 Gy** to
   the brain, **while the dog is on a CHOP/L-CHOP protocol that continues for 12–16 weeks afterwards**. This is the only
   canine answer to "CNS-directed radiation plus a systemic drug". Two caveats: the brain dose is incidental, not
   prescribed, and it is **8 Gy, not 23.4–36 Gy**; and Colosi 2026 is explicitly "**without maintenance
   chemotherapy**". **NEW** (the head-in-field verification and this reading).
4. **Systemic CNS-directed drug + systemic chemotherapy, n = 26 and n = 17.** PMIDs 31769013 and 19178667: cytarabine
   CRI (which reaches dog CSF at 8.3 µM, CSF:plasma 0.62, PMID 1742843) inside CEOP or VCAA, in dogs with CNS or bone
   marrow involvement. If "CNS-directed arm" is read to include a CSF-penetrant systemic drug rather than only
   IT/brain-RT, then **yes, n = 43 dogs across two studies** — and the 5-day CRI arm roughly tripled median survival
   (243 vs 72.5 d). **PMID 19178667 is NEW; PMID 31769013 is ALREADY IN RECORD.**

**Nothing in dogs combines an intrathecal arm with brain radiation, and nothing combines either with a drug given for
months.**

## Cross-cutting question 2 — Has any canine lymphoma study attempted curative intent with a multi-year horizon, rather than remission-duration endpoints?

**Answer: yes — but only the transplant programmes, and their horizon is ~2–4 years, not 10.**

- **PMID 3887690** (1985), stated in the conclusions: "These studies thus demonstrated that **dogs with malignant
  lymphoma in remission can be cured** with high-dose TBI and autologous marrow transplantation" — 95 dogs, 9/38 (24%)
  "long-term disease-free survivors" at 8.4 Gy. **ALREADY IN RECORD**.
- **PMID 35789057** (2022) defines and reports a **cure rate**: "The cure rate of alloHCT, as defined as living **>4 yrs**
  after the procedure and/or not dying from lymphoma, in these dogs was ~89%", against a pre-set "trial end-point of
  4.1 yrs". **ALREADY IN RECORD** (`SWEEP_hct_model.md:26,29`).
- **PMID 34950726** (2021) defines cure as "**disease-free for ≥2 years** post-autoPBHSCT": 4/10 (40%).
  **ALREADY IN RECORD** (`SWEEP_exists.md:75`).
- **PMID 40088118** (2025) reports 1-/2-/**3-year** survival rates (79% / 71% / 43%) rather than medians alone — the
  longest-horizon rate reporting found in a canine lymphoma *radiation* study. **NEW** (the 3-year rate).
- Nothing else. No canine lymphoma study has a 5-year endpoint, let alone 10. The one 5-year canine lymphoma figure in
  the record is a **failure** rate: control dogs' 5-year first-remission rate 4.4% (PMID 42525883 Table 9), and
  "13/127 alive >2 y; 5-y survival 1%" (PMID 21320018). **ALREADY IN RECORD** (`SWEEP_hct_model.md:80-82`).

## Cross-cutting question 3 — Published median follow-up durations in canine lymphoma trials

Reported follow-up is short, and in many trials it is not stated at all. What I could verify:

| study | stated follow-up |
|---|---|
| PMID 40088118 (HBI, n = 25) **NEW** | "For those patients still in remission, the **median follow-up time was 1086 days** (range 749–2261)"; "median follow-up time for all censored patients was **1083 days**" |
| PMID 35789057 (alloHCT, n = 15) **ALREADY IN RECORD** | pre-set **trial end-point 4.1 years**; individual follow-up of the six living dogs not reported |
| PMID 12931117 (2 Gy RIC, research dogs) **ALREADY IN RECORD** | "median follow-up of **>48 (range, >32 to >56) weeks**" |
| PMID 22620705 (Lane 2012, 21 lymphoma dogs, intensified chemo + autologous BMT) **ALREADY IN RECORD** (`SWEEP_hct_model.md:60`) | "**median follow-up 4 months**", no relapse/survival data reported |
| PMID 39074816 (verdinexor CETL, n = 8) **ALREADY IN RECORD** | assessments every 14 d for 3 months then monthly, "**mean 70 ± 43.4 days**" |
| PMID 34125606 (prednisone alone, n = 109) **ALREADY IN RECORD** | median OS 50 d; "**No variables were predictive of long-term (> 120 days) survival**" — 120 d is the paper's own definition of long-term |
| PMID 31769013 (cytarabine CRI, n = 26) **ALREADY IN RECORD** | AEs during and shortly after one CRI; **no follow-up period stated** |
| PMID 25041580 (IT chemo, n = 120 animals) **ALREADY IN RECORD** | **"short-term"** by design: during anaesthetic recovery and hospitalisation only |
| PMID 38695516 (94 TBI+HCT dogs) **ALREADY IN RECORD** | a **10-year** institutional period, but the paper reports only pre-discharge deaths |
| PMID 41742567 (cytarabine in MUO, n = 43) **ALREADY IN RECORD** | "minimum follow-up **24 months**" — the longest prospectively mandated canine follow-up found for any cytarabine schedule, in a non-neoplastic disease |

**Reading, stated plainly.** Canine lymphoma follow-up clusters at **weeks to a few months** for drug studies and
**2–4 years** for the radiation and transplant studies that deliberately chase durability. A 10-year question cannot be
answered from this literature because, with the single exception of the NCSU transplant cohort's eight long survivors,
**no canine lymphoma cohort has been observed for 10 years**. The competing risk is also real: the alloHCT donors and
recipients had a mean age of 55 months, so a 10-year horizon reaches dog age ~14.6 years.
**ALREADY IN RECORD** (`SWEEP_hct_model.md:149`).

## Cross-cutting question 4 — Any veterinary consensus statement, review or editorial on WHY aggressive multimodal or curative-intent protocols are not pursued?

**Answer: no formal consensus statement found. Three reviews/papers state reasons explicitly, and I quote them.**

1. **Graves & Storb 2021, "Evolution of haematopoietic cell transplantation for canine blood disorders", Vet Med Sci
   7:1385** — PMID 34390541, [doi 10.1002/vms3.601](https://doi.org/10.1002/vms3.601) (PMC8604109, **full text read
   this session**). The closing paragraph is the most direct statement in the literature:
   > "Finally, **cost of HCT is a concern**. However, in many cases **the dog is considered a member of the family**,
   > and extending the life of the animal may not be a difficult decision to make **for those who can afford the
   > treatment**. Costs can be curtailed by using autologous marrow … For allogenic donors, genetic sequencing
   > efficiency and availability are improving, while costs are decreasing every year. Finally, **canine HCT in the
   > United States is covered by many major pet insurance policies, in some cases up to 80%–90% of costs**. In
   > conclusion, **it may be time to consider the benefits of HCT in mainstream veterinary medical practices.**"

   The same review names the structural, non-financial barriers: "**DLA typing in the general population is complicated**
   in cases where either one or both parents are not available for typing or the location of potential littermate
   donors is also limited"; "Multigenerational-family molecular DLA typing for clinical allogeneic HCT **needs to be a
   practical and routine laboratory procedure widely available to veterinary clinicians**"; "**In veterinary practices
   where TBI is not easily available**, chemotherapy conditioning may be a possible alternative"; and for
   radioimmunotherapy, "the cost of production of the isotope, its short t½ lives, and the complexity of conjugation
   methods **currently makes RIT impractical for standard veterinary practices**."
   The review's availability sentence — "a **selected number of institutions** within the United States" — is
   **ALREADY IN RECORD** (`SWEEP_hct_model.md:62,191`); **the cost/insurance/"member of the family" paragraph and the
   RIT and TBI-availability sentences are NEW.**

2. **Williams 2004 (half-body RT, PMID 15515588)** — the clearest statement of a *clinical-relevance* threshold rather
   than a cost one: the gain "**might not be long enough to be clinically relevant or to justify application of the
   method described herein**." **NEW** (as a quoted reason).

3. **Lautscham 2017 (PMID 28100766,
   [doi 10.1136/vr.104077](https://doi.org/10.1136/vr.104077))** — the paper that closes the maintenance question and
   states why the field standardised on short protocols: "The recommendation to treat canine lymphoma with a
   discontinuous protocol **is based on small case numbers and mostly historic controls**", and after comparing 75 dogs
   given a 2-year maintenance phase with 333 given induction only, "**This study supports the use of a discontinuous
   protocol for canine multicentric lymphoma.**" **NEW.**

**Quality-of-life literature, which is where the owner-acceptance reasoning actually lives (all NEW):**
- **PMID 22143660** (Bergmann 2011, owner survey, 123 of 207 owners responded): quality of life improved in 64 dogs
  (53.3%) during chemotherapy and declined in only 24 (20.0%); "**the majority of the owners (65.0%) were satisfied**
  by the chemotherapy of their dogs. Ninety owners (73.2%) **would have treated their animal with chemotherapy
  again**; for this decision **prolonged survival was an important factor**." So owner acceptance of *more* treatment
  is high where survival is extended — this cuts against "owners won't accept aggressive therapy" as the explanation.
- **PMID 27140826** (Vøls 2016 review, [doi 10.1111/vco.12242](https://doi.org/10.1111/vco.12242)):
  "**QoL-assessment of cats and dogs receiving chemotherapy is in its infancy** … **Each** of the identified
  publications … **applied a different method** of QoL-assessment … the veterinary QoL-assessments were mainly focused
  on physical clinical parameters … **Standardizing and including a complete range of potentially relevant parameters
  in future QoL assessments may benefit owner decision making.**" I.e. the QoL evidence that would be needed to
  justify or refuse an aggressive protocol does not yet exist in a standardised form.

**What I could not find, stated plainly:** no ACVIM/ECVIM or VCOG consensus statement, position paper or editorial that
addresses curative intent, reimbursement or ethics in canine lymphoma specifically. Searches run: "dog owners decision
chemotherapy quality of life" (15 hits, all screened), "canine lymphoma maintenance randomized", "quality of life
assessment dogs cats chemotherapy", plus the cost/ethics keyword scan of PMC8604109. If such a statement exists it is
likely in a textbook chapter (Withrow & MacEwen) or a non-indexed proceedings, neither of which is in PubMed.

---

## Summary table

| Treatment | Used in dog lymphoma? | Published canine combinations with any of the other seven | Maintenance use in dogs | Stated reason for stopping where they did | Lawful status for a US vet |
|---|---|---|---|---|---|
| **1. Verdinexor** | **YES.** Phase II n = 58, ORR 37% (T-cell 71%); FDA field study n = 134, TTP 37 vs 23 d; CETL pilot n = 8, TTP 56 ± 41 d | **prednisolone only**, and only as a permitted/supportive adjunct (n = 58, n = 8), no separate readout. In vitro with doxorubicin/vincristine (4 canine lines). +RT in one **myeloma** dog | **YES — on-label, continued to progression.** Longest continuous: **17 months, 1 dog**; PRs 246 and 354 d; controlled safety only to day 56 (field) / 13 weeks (beagle tox) | "support continued evaluation … **in combination with standard chemotherapeutics**" (combination trial named as future work, not done); CETL pilot framed as "safe, **palliative**"; FOI: no chronic toxicology >13 wk; one dog stopped day 224 for toxicity | **FDA-approved ANIMAL drug** for canine lymphoma (full approval Jan 2026); sustained dosing on-label |
| **2. Prednisolone** | **YES.** Single agent n = 109: median OS **50 d**; no variable predicted survival >120 d | **The most-combined of the eight**: with cytarabine CRI (n = 26; n = 17), with IT cytarabine+MTX (n = 1), with half-body/brain-in-field RT (n = 75; n = 14), pre-transplant induction (n = 15), adjunct to verdinexor | **Historically yes, deliberately abandoned.** CHOP backbones give a **4-week taper only**. Longest canine lymphoma steroid exposure found: 1080 d in one pre-treated dog | CALYPSO designed to quantify a **palliative** option "to discuss with owners … at the time treatment decisions are made"; PMID 40624957: "**should be used with caution and reserved** for cases where clinical benefits clearly outweigh the risks" | **FDA-approved animal drug**, oncologic use **extra-label** (specific NADA not verified) |
| **3. Cytarabine CRI** | **YES, in combination only.** 5-day CRI arm: CR 8/9 vs 2/8, median survival **243 vs 72.5 d** (n = 17). Single CRI in CEOP: toxicity only (n = 26). Dog CSF 8.3 µM, CSF:plasma 0.62 | **prednisolone-containing backbones** (n = 17, n = 26); **IT methotrexate** when given intrathecally (n = 120 animals; n = 1). None with verdinexor, HCQ, romidepsin, RT or transplant | **NO for lymphoma** — one CRI or one 5-day block. The only multi-year canine cytarabine is **pulsed q3–6 wk for ≥24 months in MUO** (n = 43, no serious AEs). **Weekly CRI in a lymphoma dog: not found** | "**gastrointestinal toxicity should be expected**" (study was toxicity-only, no efficacy endpoint); "incorporation of the nucleoside analogue **might be crucial for … future therapeutic strategies**" (further work named) | **FDA-approved human drug, extra-label**; CRI route/schedule extra-label |
| **4. Intrathecal methotrexate** | **YES — once. n = 1.** CNS remission **3.5 weeks**; 2.5 mg flat cisternal dose is **secondary** (via Lyseight citing Genoni) | **IT cytarabine** (same injection) **+ systemic prednisolone/dexamethasone**, n = 1. Nothing else | **NO.** Repeated cisternal puncture documented to **4 doses/4 months** (non-oncologic); an implanted ventricular port has run **biweekly for 8–11 months** in non-oncologic dogs. 16–45 doses: **no precedent** | **"repeat intrathecal chemotherapy was declined"** (owner declination, then euthanasia at 9 weeks); Genoni by design assessed "**the short-term safety**" only | **FDA-approved human drug, extra-label**; preservative-free product required (not verified) |
| **5. Hydroxychloroquine** | **YES — one phase I, n = 30.** ORR **93.3%**, median PFI **5 months**; 100-fold tumour:plasma accumulation | **NONE of the seven.** The published pairing is HCQ + **doxorubicin** | **NO for lymphoma.** ~1–1.5 years exists in canine **dermatology** at 5–10 mg/kg/d in ≤3 dogs ("first to address … long-term administration, albeit in a small number of dogs"); that is **not** the antineoplastic MTD of 12.5 mg/kg/d | Phase I by design ("to determine a maximum dose"); "provide **strong support for further evaluation via randomized, placebo-controlled trials**" — that trial has not been published | **FDA-approved human drug, extra-label** |
| **6. Romidepsin** | **NO.** No in-vivo canine study of any kind. Only an ex-vivo spheroid screen in **osteosarcoma** (50% of canine samples responded, ED50 <70 nM) | **NONE** — impossible, since no dog has received it | **NO** | **Dogs are the species in which it failed**: "a drug initially **abandoned because of serious cardiotoxicity in dogs**", rescued for humans only "by tailoring the dose regimen to mitigate cardiac toxicity risks" (conference-proceedings grade) | **FDA-approved human drug, extra-label** (CTCL indication live; PTCL indication withdrawn 2021–22) |
| **7. Whole-brain / craniospinal RT 23.4–36 Gy @ 1.8 Gy** | **NOT as prescribed brain RT.** But the brain IS in the cranial half-body field: **8 Gy (4 Gy × 2)** in 14 dogs, 6 Gy in 75 dogs. HBI series: PFI 1143 vs 316 d; PFS 532 vs 296 d; first remission 311 d (n = 52) | **prednisolone/L-CHOP/MOPP + L-asparaginase**, in all five RT series, with chemo continuing 12–16 weeks after RT. None with verdinexor, cytarabine CRI, IT MTX, HCQ, romidepsin or transplant | **N/A for RT**, and the series are deliberately maintenance-free ("…L-CHOP **without maintenance chemotherapy**") | **"might not be long enough to be clinically relevant or to justify application of the method described herein"**; "an optimal protocol that improves outcomes while minimising toxicity **has not been established**"; one-session TBI "may significantly increase the bone marrow toxicity"; "**Prolonged anaesthesia time was considered a potential risk factor**". For 23.4–36 Gy to the brain: **no reason stated — no canine paper proposes it** | **Procedure** (VCPR + linac facility); canine infrastructure and multi-site TBI dosimetry exist |
| **8. Allogeneic DLA-identical HCT (incl. ~2 Gy RIC)** | **YES — the only multi-year curative-intent canine lymphoma result.** n = 15, TBI 2 × 4 Gy; median DFI/OS **1095/1115 d**; first-remission DFI/OS **1235 d**; "**8 of 9 … lived >4 yrs … cure rate of 89%**"; TRM 13%; grade 2 aGVHD 23%, no chronic GVHD. **2 Gy RIC: engrafts durably (5/6) but only in healthy research dogs — no lymphoma** | **prednisolone-containing CHOP induction before transplant only.** Conditioning is TBI ± cyclophosphamide/busulfan. **No canine series reports relapse site**, so CNS relapse after canine HCT is unknown | **N/A — the graft is the sustained effector**: >95% donor chimerism by 2 weeks, ≥58 weeks in the case report, six dogs disease-free to 2920 d; immunosuppression only to ~day 30 | **Pre-set "trial end-point of 4.1 yrs"** (hence no 10-year canine number); "**no bone marrow donor registries exist for dogs**", mean 5 donors screened (1–28); dose escalation 8.4→13.5 Gy raised TRM 26%→55% with **no** relapse reduction; "cost of HCT is a concern"; programme paused ~2023 (WEB) | **Procedure** at "a **selected number of institutions** within the United States"; component drugs extra-label |

---

## Closing: which parts of the eight-treatment conjunction have canine precedent, and which have none

**The conjunction is eight treatments; the published canine prior art covers at most two of them at a time, and
never three.**

**What has real canine precedent, at the strength shown.**
- **Verdinexor as sustained monotherapy** is the only component whose intended use in this programme is *exactly* what
  is published and approved: twice-weekly oral dosing continued to progression, in 58 + 134 + 8 dogs, with one dog at
  17 months. The programme's ~168 days sits inside the single-dog clinical experience and just outside the 13-week
  controlled toxicology.
- **Prednisolone inside a multi-agent protocol** is universal canine practice; as a single agent its effect is
  quantified and small (median OS 50 d).
- **Cytarabine CRI added to a multi-agent, prednisolone-containing backbone** has a real canine efficacy result
  (n = 17: CR 8/9 vs 2/8, survival 243 vs 72.5 d) and a real canine toxicity result (n = 26: GI 65%, grade III/IV 19%),
  and the drug's CSF reach is measured in dogs (8.3 µM, CSF:plasma 0.62).
- **Half-body irradiation combined with concurrent CHOP** is published in 75 + 52 + 14 + 6 dogs, and — newly verified
  here — **the head is inside the cranial field**, so a canine lymphoma brain has received 6–8 Gy concurrently with
  systemic chemotherapy, in roughly 90 dogs.
- **Allogeneic DLA-identical HCT after CHOP induction** is published in 15 dogs with an explicit, multi-year
  curative-intent endpoint and an 89% four-year cure rate in the first-remission subgroup — the only component that has
  ever delivered the kind of durability the programme is aiming at.
- **Pairs with canine precedent (the central question):** prednisolone+cytarabine CRI (n = 43 across two studies);
  prednisolone+brain-in-field RT (n ≈ 90 across four studies); prednisolone+alloHCT as sequential induction (n = 15);
  IT cytarabine+IT methotrexate (n = 120 animals, one of them a lymphoma dog); verdinexor+prednisolone
  (co-administration only, n ≤ 66, no separate readout). **That is five pairs.**

**What has no canine precedent at all.**
- **Any triple** from the eight. Not one canine publication combines three of these eight treatments.
- **Romidepsin in a living dog** — and the reason is not cost or trial design: dogs are the species in which romidepsin
  was abandoned for serious cardiotoxicity. This is the one component whose absence from the canine record reflects a
  species-specific pharmacologic objection rather than a funding or follow-up limit.
- **Hydroxychloroquine with any of the other seven.** Its single canine trial pairs it with doxorubicin.
- **Repeated intrathecal methotrexate.** One dog, one course, 3.5 weeks, with the repeat declined. The programme's
  16–45 doses have a *device* precedent in dogs (implanted ventricular port, biweekly, 8–11 months, non-oncologic) and
  no drug precedent in lymphoma.
- **Weekly repetition of a cytarabine CRI** in a dog with lymphoma.
- **Prescribed whole-brain or craniospinal radiotherapy at 23.4–36 Gy in 1.8 Gy fractions.** The canine brain dose on
  record is 6–8 Gy in 2–4 Gy fractions, incidental to a body field. No canine paper proposes the programme's dose, so
  no canine paper gives a reason against it.
- **Reduced-intensity ~2 Gy conditioning in a dog with lymphoma.** The 2 Gy dose is established as the engraftment
  floor in healthy littermate pairs; every canine lymphoma transplant used 8–12 Gy.
- **Any CNS-directed arm combined with a systemic drug given for months**, and **any combination of an intrathecal arm
  with brain radiation**.
- **A 10-year, or even 5-year, follow-up horizon.** The longest pre-set canine lymphoma endpoint found is 4.1 years
  (and it was reached); the longest stated median follow-up is 1086 days; drug studies report weeks. The 10-year
  question is unanswered in dogs because it has never been asked, and the papers say why: endpoints set at 2–4 years,
  owner-facing palliative framing, toxicity-only designs, short-term safety designs, one owner declining a repeat dose,
  a "not clinically relevant" judgement on a real radiation benefit, and a maintenance phase that was tested in 75 dogs
  against 333 and found not to help.

**Final note on grading (rule 11).** Everything in the "no canine precedent" list above is a statement about the
*literature*, not a gap in the model. For several of these components the record already carries a written transfer or
derivation that constitutes closure under the stated bar — romidepsin's kill (TRANSFER from human MOLT-4 × label
exposure, `SWEEP_inhibitors_partial.md:198`), the IT methotrexate CSF exposure and dose count (DERIVED from
dog-measured CSF volume and dog-measured t½, `SWEEP_itmtx2.md:76-118`), the radiation e-folds (DERIVED from canine
line radiosensitivity with a transferred in-vivo factor, `SWEEP_hct_model.md:255-258`), and the allograft effect
(OUTCOME-calibrated from the 15-dog plateau, `SWEEP_hct_model.md:229-246`). The one item in this document that is new
*evidence against* a component rather than absence of evidence is the canine cardiotoxicity history of romidepsin, and
the record already records romidepsin as not load-bearing (`docs/LYMPHOMA_STATUS.md:309`).
