# SWEEP: lawful cytotoxics missing from the canine-lymphoma AGENT CATALOGUE (2026-11-16)

All literature claims below are **from PubMed**; each carries a PMID and, where one exists, a DOI link.
Label/regulatory claims carry a DailyMed or FDA source. Where a number does not exist in the sources I
read, this file says **NOT FOUND** rather than estimating it. **No kill rate is estimated here** (per the
task): what is reported is measured efficacy, dose, exposure and toxicity, plus a named statement of
which number a derivation would still need.

Bar in force (CLAUDE.md, user verbatim): "real data **or a rigorous model**", cross-species/class transfer
acceptable **if justified in writing**; "I'm okay with no specific data but if scientifically sound".
Grades used: MEASURED (dog) / MEASURED (other species) / TRANSFER / OUTCOME / ASSUMED / NOT FOUND.

---

## 0. RECORD CHECK FIRST — and a correction to this task's premise (rule 1, rule 4)

The task states: *"L-asparaginase appears in the record only incidentally (inside LHOP/CHOP protocol
descriptions and two case reports) and has never been evaluated as an agent — confirm that."*

**That is not confirmed. It is false.** L-asparaginase carries a dedicated, nine-part, numbers-level
evaluation in the record already:

| where | what is already recorded |
|---|---|
| `docs/universe/SWEEP_regrade.md:8-24` | **A full dedicated regrade section, "## 1. L-ASPARAGINASE / PEG-ASPARAGINASE"**, with sub-parts (a) potency (b) exposure (c) kill k (d) division (e) pump (f) CSF/brain (g) dCK (h) escapes (i) toxicity axis, and a GRADE line. It already contains PMIDs 3567863, 2145933, 27086733, 17338160, 19678892, 24033105, 23738234, 35781075, 24934864, 6895481, 34170389, 8485807, 14724653, 34863941, 23365669, 17380207, 34614505, 22961784, 8324873, 10334545, 31523835. |
| `docs/universe/SWEEP_regrade.md:6` | An explicit **"Settled that I must not re-raise"** list naming L-asp: no benefit as COP add-on (15995158), anti-asp antibodies (23253146), human CSF Asn 5.3 → ≤1.5 µM (24702187). |
| `docs/universe/SWEEP_inhibitors_partial.md:247` | Prior evaluation with mechanism, canine evidence, resistance, P-gp status, CNS, and an explicit kill-rate verdict. |
| `docs/LYMPHOMA_UNIVERSE.md:22` | Candidate-universe row: graded **EVALUATED, EXCLUDED** ("no exposure-derived kill; P-gp status unverified"). |
| `docs/LYMPHOMA_UNIVERSE.md:356`, `:402` | Re-grade result recorded: "enzyme, not pumped, depletes CSF asparagine in humans, but kill is cytostatic-then-apoptotic and dormant-cell evidence is negative; outcome-only rate 0.03-0.05 /day". |
| `docs/LYMPHOMA_STATUS.md:277` | Same conclusion carried into status. |
| `docs/universe/SWEEP_growth_bar.md:25` | PMID 17338160 used as growth-bar anchor C2. |
| `docs/LYMPHOMA_UNIVERSE.md:70` | Asparaginase named as escape lineage E13-E19, "OUTSIDE MODEL as separate lineages". |

**What IS a real gap, and the only one:** the *code* catalogue
`src/canine_dsp/core/lymphoma_catalogue.py` (19 `Agent(...)` constructions, lines 132-289) contains
**none of the 21 drugs in this task** — no asparaginase, platinum, mitoxantrone, actinomycin-D,
chlorambucil, melphalan, bendamustine, vinblastine, etoposide, hydroxyurea, procarbazine, dacarbazine or
bleomycin. So the gap is **docs-to-code**, not a gap in the record. Several of these drugs were
*evaluated in the docs and deliberately not entered in code*; re-presenting them as unexamined would
repeat CLAUDE.md failure #1 and #4.

Per-drug record status (file:line), established by grep before any search:

| drug | status |
|---|---|
| L-asparaginase / PEG-asp | **ALREADY IN RECORD, fully evaluated** — `SWEEP_regrade.md:8-24`; `SWEEP_inhibitors_partial.md:247`; `LYMPHOMA_UNIVERSE.md:22,70,356,402`; `LYMPHOMA_STATUS.md:277`; `SWEEP_growth_bar.md:25` |
| mitoxantrone | **PARTLY IN RECORD** — `LYMPHOMA_UNIVERSE.md:22`; mitox+DTIC `SWEEP_modalities.md:123,177`; P-gp "not verified" `SWEEP_modalities.md:206` |
| actinomycin-D / dactinomycin | **PARTLY IN RECORD** — `LYMPHOMA_UNIVERSE.md:22,723`; `SWEEP_modalities.md:177,206`; `SWEEP_additivity_calibration.md:19,49,83,389`; `LYMPHOMA_STATUS.md:416` |
| melphalan | **ALREADY IN RECORD with numbers** — `SWEEP_nongated.md:30,55,57` (NCI-60 GI50, Evomela PK, partial MDR 2.4x); `LYMPHOMA_UNIVERSE.md:22` |
| dacarbazine | **PARTLY IN RECORD** — `SWEEP_modalities.md:122,206`; `LYMPHOMA_UNIVERSE.md:22` |
| chlorambucil | **PARTLY IN RECORD** — CSF 0.1 ng/mL `SWEEP_exists.md:113`, `SWEEP_regrade.md:45`; maintenance arm `LYMPHOMA_UNIVERSE.md:723` |
| procarbazine | **ALREADY IN RECORD, evaluated** — `SWEEP_lawful_cns_agents.md:100-112` (label CNS text, 6 canine protocol PMIDs, escapes, kill verdict) |
| hydroxyurea | **IN RECORD as a named lead** — `LYMPHOMA_UNIVERSE.md:359,402`; `SWEEP_lawful_cns_agents.md:180`; `SWEEP_cnsregimens.md:116` |
| bendamustine | **IN RECORD, lymphodepletion only** — `LYMPHOMA_UNIVERSE.md:686`; `SWEEP_near_future_cell.md:22,160,171`; quiescence "not found" `SWEEP_outside_model.md:130` |
| carboplatin | **IN RECORD only as IA-BBBD adjunct** — `SWEEP_brain_access.md:18,72,82`. Canine lymphoma efficacy: NOT in record → **NEW below** |
| cisplatin | **IN RECORD only as a dCK-cross-resistance comparator** — `SWEEP_pk.md:155`. Canine lymphoma: NOT in record → **NEW** |
| etoposide | **IN RECORD only as intrathecal dog PK** — `SWEEP_regional.md:66,109,147,224` (PMID 1517797). Oral/systemic canine PK → **NEW** |
| vinblastine | **IN RECORD only as mouse P-gp-KO fold** — `SWEEP_brain_access.md:61`; normoblastemia `SWEEP_nongated`/`26109175`. Canine lymphoma: NOT in record |
| bleomycin | **IN RECORD only as a radiosensitivity assay agent** — `SWEEP_rt2.md:136` (PMID 23935952) |

---

## 1. L-ASPARAGINASE — TOP PRIORITY

**Record status: ALREADY IN RECORD and already EVALUATED.** Everything in (a)-(i) of
`SWEEP_regrade.md:8-24` stands. What follows marks **[REC]** for already-recorded and **[NEW]** only for
what this sweep adds. The mechanistic premise in the task — extracellular enzyme, therefore nothing for
P-gp to transport, and death by protein-synthesis starvation rather than p53-dependent apoptosis — is
**correct and is already the record's own finding** (`SWEEP_regrade.md:12` part (e); `:247` of
`SWEEP_inhibitors_partial.md`).

### Canine lymphoma efficacy

- **[NEW, and the single most important addition in this file] Randomised, double-blind, n=69 dogs.**
  PEG-L-asparaginase (n=35) vs native L-asparaginase (n=34), each **combined with vincristine,
  cyclophosphamide, doxorubicin and prednisone**: CR **85.7% (30/35)** with **median time to relapse 217
  days** vs CR **94.1% (32/34)** with **median time to relapse 214 days** (P > 0.05). "The asparaginase
  was well tolerated in both groups." Two native-arm dogs had severe allergic reactions; one PEG-arm dog
  had generalised urticaria after repeated injections. PMID **1522554**,
  [DOI](https://doi.org/10.1111/j.1939-1676.1992.tb00344.x). Grade: **MEASURED (dog), randomised**.
  *This is a 217-day CR-relapse anchor in dogs that the record did not hold* — the record's L-asp outcome
  figure was the 48-day single-agent median. Scope it correctly: 217 d is the **combination** (asparaginase
  + CHOP-equivalent) number, not an asparaginase single-agent number.
- **Single agent, n=20 dogs (8 chemotherapy-resistant).** PEG-asparaginase 10-30 IU/kg IP weekly: CR 7,
  PR 7, NR 5, NE 1; **duration of response (CR+PR) 14-102 days, median 48 days**. In the 8
  chemo-resistant dogs (7 previously resistant to native L-asparaginase) 4 responded (1 CR, 3 PR). In a
  separate arm of the same paper, PEG-asp + one cycle of VCMP then PEG-asp maintenance, n=17: CR 13, PR 2,
  NR 2, **duration 7 to 840+ days, median 126+ days**, 4 dogs still on maintenance at 16-28 months. PMID
  **3567863**, [DOI](https://doi.org/10.1002/1097-0142(19870615)59:12<2011::aid-cncr2820591207>3.0.co;2-m). **[REC]** Grade: **MEASURED (dog)**.
- **Randomised PEG vs native, n=42 (+20).** PEG 10 IU/kg IM vs native 400 IU/kg IP: "No significant
  differences were found between treatments in the response rates after 2 weeks of asparaginase therapy or
  in the time to relapse, the time to treatment failure or the remission period." PMID **2145933**,
  [DOI](https://doi.org/10.1016/0277-5379(90)90193-w). **[REC]**
- **Compounded L-asp 10,000 IU/m² SC + corticosteroid, n=73 dogs (75 treatments).** **ORR 80% (CR 24%,
  PR 56%).** PMID **27086733**, [DOI](https://doi.org/10.1111/jvp.12310). **[REC]**
- **No benefit as an add-on to COP** (34 dogs COP vs 42 COP+asparaginase, retrospective): "did not
  significantly increase the likelihood of a clinical remission or prolong the initial progression-free
  interval." PMID **15995158**. **[REC — and flagged in `SWEEP_regrade.md:6` as settled, must not be
  re-raised as new.]**
- Rescue L-asp + lomustine + prednisone, relapsed/refractory: **median TTP 63 d** (111 d if CR, 42 d if
  PR). PMID **17338160**. **[REC, = growth-bar anchor C2, `SWEEP_growth_bar.md:25`]**
- **[NEW pmid]** n=138 dogs, 10-week induction then **asparaginase weekly as maintenance**; prognostic-factor
  study (stage and immunophenotype predict time to relapse and survival). PMID **7744644**. Grade:
  OUTCOME (dog), multi-agent — no asparaginase-attributable effect size.

### Canine dose and schedule (as actually used in dogs)

| form | dose | route/schedule | source |
|---|---|---|---|
| native E. coli L-asp | **400 IU/kg** | IP | PMID 2145933 **[REC]** |
| native / compounded | **10,000 IU/m²** | SC (or IM), single or repeated | PMID 27086733 **[REC]** |
| PEG-asparaginase (1980s-90s conjugate) | **10-30 IU/kg** | IP or IM, weekly | PMIDs 3567863, 2145933 **[REC]** |
| PEG-asparaginase, beagle PK | 10 IU/kg (and 20, 40 on repeat) | — | PMID 35781075 **[REC]** |

Tolerability head-room: 4 normal dogs given **200 IU/kg and 1200 IU/kg** PEG-asp weekly ×2 "without any
significant toxicity" (PMID 3567863) — i.e. ~40-120× the 10 IU/kg clinical dose was given to healthy dogs
without significant toxicity. **[NEW emphasis; the number is in a REC paper but was not drawn out]**

### Dose-limiting toxicity and ORGAN AXIS — the decisive part

**Primary axis: IMMUNE / HYPERSENSITIVITY (anaphylaxis), with a secondary PANCREATIC (GI-adjacent but
distinct) axis and a minor HEPATIC axis. Myelosuppression is NOT dose-limiting and is not reported as an
asparaginase toxicity in any dog series read.**

- **Hypersensitivity/anaphylaxis, native enzyme: 14/29 = 48% of native-treated dogs had drug-related side
  effects** — anaphylactic shock **9**, anorexia/vomiting **4**, hypersensitivity oedema **3**, seizures
  **1**, acute pancreatitis **1**. **"No side-effects were noted in the dogs treated with
  PEG-L-asparaginase."** PMID **2145933** **[REC]**. So **pegylation moves this axis from 48% to ~0%** in
  a randomised comparison — directly relevant to a per-axis toxicity budget.
- **Coagulopathy: negative.** "No abnormalities in clotting times, fibrinogen levels or antithrombin-III
  levels were found in any of the **62** dogs." PMID 2145933 **[REC]**.
- **Pancreatitis incidence in dogs — [NEW, this is the number the task asked for]:** prospective pilot,
  **52 dogs**, cPLI measured before and after. **"No dogs receiving ASNase alone showed evidence of
  clinical pancreatitis after administration"**, and **"there was no statistically significant change in
  cPLI concentrations before or after treatment."** **14% of dogs that received vincristine AND ASNase
  concurrently had elevated cPLI** after treatment. Of 11 dogs with signs compatible with pancreatitis
  after any chemotherapy, none had cPLI > 400 µg/dL. PMID **19436578**,
  PMC2666314. Grade: **MEASURED (dog), n=52, prospective**. *Direction: asparaginase-alone pancreatitis
  incidence in dogs is 0/n in the only prospective cohort; the signal appears with concurrent vincristine.*
- **Pancreatitis does occur — single case report, [NEW pmid]:** vomiting, lethargy, abdominal pain 48 h
  after L-asparaginase, with elevated cPLI; the authors state "its pathophysiology and **incidence rate in
  veterinary patients are unknown and sparsely documented**." PMID **22379203**, PMC3157059. Grade:
  MEASURED (dog), n=1 — a case report, so it establishes existence, not rate.
- Lipase elevation: PMID 19436578 (above). Hepatic axis: named in the record (`SWEEP_regrade.md:21`).
- **Myelosuppression: confirmed NOT dose-limiting.** The record's own line states "No marrow toxicity =>
  cheap in the budget" (`SWEEP_regrade.md:21`, part (i)). This sweep adds that **no dog series read
  (PMIDs 1522554, 2145933, 3567863, 27086733, 19436578) reports neutropenia or thrombocytopenia as an
  asparaginase toxicity**, and that the single-agent toxicity list in PMID 3567863 is tumour-lysis death
  (2), DIC (1), hypersensitivity (1), vomiting (3), soft stools (3) — **no cytopenia**. Grade: **MEASURED
  (dog), negative finding across 5 series**. Caveat stated plainly: these are reported-AE lists, not
  protocol-mandated serial CBC denominators, so this is "not reported as dose-limiting", which is weaker
  than "measured and shown absent".
- **The real limiter is antibody-mediated loss of effect, not organ toxicity.** Anti-asparaginase
  antibodies in **3/10 dogs after one injection and 4/7 after repeats** (PMID **23253146** **[REC]**).
  Beagle: PEG-asp 10 IU/kg depleted plasma Asn for 9 d in 7/7, 15 d in 5, 21 d in 3, 29 d in 1; repeat
  doses (20, 40 IU/kg) **shortened** suppression to <9 d in 5/7 dogs with anti-PEG/anti-asp antibodies
  (PMID **35781075** **[REC]**). **Budget consequence: this agent is limited by an immunogenicity clock,
  not by a cumulative organ dose** — a different kind of constraint from every drug now in the catalogue.

### Is it a P-glycoprotein / ABCB1 substrate?

**No — and it cannot be, by chemistry.** L-asparaginase is a ~140 kDa bacterial tetrameric **enzyme**
(PEG forms larger) that acts **extracellularly**, hydrolysing serum asparagine; it never needs to cross
the plasma membrane to work. ABCB1 is an ATP-driven efflux pump for small, largely lipophilic membrane
permeants, so there is no transportable species. The record already states this: "Enzyme (~140 kDa
tetramer; PEG form larger): not a P-gp/BCRP/MRP substrate by class (no citation needed; not a membrane
permeant). **Pump-armour irrelevant**" (`SWEEP_regrade.md:12`) and "Not a P-gp substrate (protein; no
citation needed beyond class)" (`SWEEP_inhibitors_partial.md:247`). Grade: **MECHANISM, class-level
(not an assay)**. Honest limit: I found **no** published ABCB1 transport assay for asparaginase, because
none would be run; the claim rests on molecular class, not on a measurement. The *downstream* resistance
mechanism is instead **ASNS re-expression** (below), which is a genuinely different escape from efflux.

### Is its killing p53-dependent?

- **Mechanism, canine tissue [REC]:** apoptosis follows protein-synthesis arrest, in a mouse lymphoma line
  **and in a canine lymph node biopsy** — "massive destruction of neoplastic cells by what was consistent
  with apoptosis" at 4 h; "it seems unlikely that protein depletion per se ... is the triggering event ...
  It is more likely that the **suspension of cellular proliferation** commits cells to apoptosis." PMID
  **8485807**. Note what this says: the trigger is proliferation arrest, which is *also* the reason the
  dormant-cell case fails (below).
- **[NEW] Direct p53-null evidence.** PEG-asparaginase in a three-drug sequence (6-thioguanine → ara-C →
  PEG-ASNase) in myeloid and lymphoblastic leukaemia lines, where "The CEM clones, MOLT-4 and HL60/SN3
  cell lines expressed functional or measurable p53 protein, while the other cell lines did not":
  synergism 1.3- to 18.3-fold, and **"the three-drug combination was capable of downregulating bcl-2
  oncoprotein levels in these cell lines even when p53 was absent"**; the authors conclude the regimen "is
  highly synergistic in **p53-null** and p53-expressing leukemia cell lines." PMID **11561778**,
  [DOI](https://doi.org/10.1007/s002800100289). Grade: **MEASURED (human lines), but for the
  THREE-DRUG combination, not asparaginase alone** — reported at the strength shown (rule 5). It supports
  p53-independence of the regimen and is consistent with amino-acid-starvation killing being
  p53-independent; it is **not** an isolated asparaginase p53-null IC50.
- **A direct asparaginase-alone p53-mutant vs p53-WT lymphoma comparison: NOT FOUND.** Four PubMed query
  forms (asparaginase + p53-independent; + p53 status/sensitivity; + TP53 apoptosis independent; +
  resistance/p53/BCL2) returned 0-1 hits. **This is the main missing number for criterion (b).**
  Mechanistically, asparagine starvation signals through amino-acid-deprivation sensing (GCN2/ATF4-type
  integrated stress response) rather than through DNA damage → p53, so p53-independence is the expected
  direction; I could not verify that with a citation in lymphoma and say so plainly.

### Does it kill non-dividing (quiescent) cells?

**No. The evidence is negative, and this is already the record's settled conclusion — do not re-open it.**
`SWEEP_regrade.md:11` part (d) and `LYMPHOMA_UNIVERSE.md:356,402`:

- Cytostatic first, then apoptosis (PMID 8485807); TEL/AML1 leukaemic cells arrest in cell cycle (PMID
  14724653).
- **Dormant-cell evidence is explicitly negative:** L-asp alone inhibited glutamine metabolism in CML
  stem-like/dormant cells **"without inducing predominant CML cell death"**; death only after TKI (PMID
  **34863941**).
- Canine lines: amino-acid (arginine) deprivation sends checkpoint-competent cells **to quiescence with
  full recovery**, killing only checkpoint-defective lines (PMID **23365669**).
- Marrow MSC secrete asparagine and protect ALL cells (PMIDs 17380207, 34614505); though PMID 22961784
  found no increase in marrow Asn in patients.

**So asparaginase answers the P-gp + p53 conjunction but NOT the dormancy (E5) requirement.** Those are
different requirements and must not be conflated.

### CNS / exposure (for completeness; all [REC])

The enzyme does **not** enter CSF (IT-injected asparaginase clears at bulk-flow rate, PMID 6895481);
the CNS effect is entirely via **systemic asparagine depletion**. Rhesus: CSF Asn 4.7-13.6 → <0.25 µM by
48 h, held <0.25 µM for 10-14 d in 4/6 (PMID **8324873**). Children: CSF Asn median 4.42 → <0.04 µM,
undetectable in 73.9% during therapy (PMID **10334545**); PEG-asp holds CSF Asn <1 µM for 15.3 d after
1 dose / 30.7 d after 2 (PMID **34170389**), and CNS relapse was higher when CSF depletion was shorter
(p=0.049). Serum activity ≥0.1 IU/mL suffices to deplete CSF Asn (PMID 6895481); median 0.44 IU/mL to
hold <1 µM (PMID 34170389). **Dog CSF asparagine: NOT FOUND.** Dog PEG-asp PK scaled by BSA matches
paediatric ALL (PMID **24934864**). Grade: **TRANSFER (rhesus + human), justified in writing.**

### US lawful status — careful, because this is where asparaginase is genuinely awkward

Verified against **DailyMed** (current SPLs) and the **Oncaspar BLA record**:

| product | ingredient | status | source |
|---|---|---|---|
| **Elspar** (native E. coli) | asparaginase | **DISCONTINUED in the US.** "Use of compounded L-asparaginase became routine in veterinary oncology when manufacturing of Elspar was **discontinued in 2012**." | PMID **27086733**, [DOI](https://doi.org/10.1111/jvp.12310) |
| **Oncaspar** (pegaspargase) | PEG-asparaginase | **Current SPL in DailyMed** (listed labeler Enzon Pharmaceuticals; BLA **103411**, original approval 1 Feb 1994, now Servier). Record already holds the SPL id `ac7b6a6f-6ddb-48c6-8088-d8a8e3fea6ce` (`SWEEP_inhibitors_partial.md:29,247`). | DailyMed search "asparaginase"; FDA BLA 103411 |
| **Asparlas** (calaspargase pegol-mknl) | PEG-asparaginase, longer-acting | **Current.** DailyMed NDC 72694-515-01, labeler **Servier Pharmaceuticals LLC**, marketing category **BLA 761102**, marketing start **27 Sep 2019**, no end date. | DailyMed |
| **Rylaze** (asparaginase erwinia chrysanthemi (recombinant)-rywn) | Erwinia asparaginase | **Current.** DailyMed, labeler **Jazz Pharmaceuticals**. FDA-approved 2021 for ALL/LBL in patients ≥1 month with hypersensitivity to E. coli asparaginase. | DailyMed |
| **Erwinaze** (asparaginase Erwinia chrysanthemi) | Erwinia asparaginase | **Discontinued/withdrawn from the US market**; manufacturing ceased around the 2021 Rylaze approval. An "Erwinase" SPL (Porton Biopharma) still appears in DailyMed, which is **not** the same as current US marketing — flagged as **PARTLY VERIFIED**. | DailyMed; web sources (payer criteria removal) — **not confirmed on an FDA page; I could not load Drugs@FDA or the Purple Book (HTTP error / 404)** |
| bulk "L-asparaginase" entries (Changzhou Qianhong, BlueBay Shandong, Sajjala, CBSChem, Loka, AX Pharmaceutical) | asparaginase API | DailyMed lists these as generic/API, two tagged "animal drug". These are **bulk drug substances, not FDA-approved finished products.** | DailyMed |

**Lawfulness for a dog — the nuance that matters.** Extra-label use under AMDUCA / **21 CFR 530** applies
to an **FDA-approved** human or animal drug used by/on the order of a licensed veterinarian. On that
route, **Oncaspar, Asparlas and Rylaze are each lawfully usable extra-label in a dog today**; there is no
FDA-approved *animal* asparaginase product. **But the product US veterinary oncology actually uses is
compounded from bulk API** (PMID 27086733), and **compounding an animal drug from a bulk drug substance is
not covered by 21 CFR 530** — it remains unlawful under the FD&C Act, with FDA describing only limited
**enforcement discretion** in **GFI #256** ("Compounding Animal Drugs from Bulk Drug Substances",
finalised April 2022), conditioned on the substance appearing on FDA's office-stock bulk-substances list.
**I did not verify whether asparaginase is on that FDA list** — stated as unverified. Practical reading
for the model: **prefer Oncaspar / Asparlas / Rylaze as the lawful supply route** (clean 21 CFR 530
extra-label), and treat compounded bulk L-asp as the cheaper but legally weaker route.

**Published canine use of the PEGYLATED forms — important caveat.** Yes, pegylated asparaginase has been
used in dogs, in two randomised trials and one single-agent study (PMIDs **1522554**, **2145933**,
**3567863**). **But those used a 1987-1992-era PEG-asparaginase conjugate, not the modern Oncaspar
pegaspargase product** — the papers predate Oncaspar's 1994 approval. A PubMed search for
pegaspargase/Oncaspar + dogs + lymphoma returned only those same historical papers (PMIDs 7744644,
1522554, 2145933, 2076022). **Published canine use of Oncaspar, Asparlas or Rylaze specifically:
NOT FOUND.** Under rule 15 this is a cross-compound question: the historical PEG conjugate and modern
pegaspargase share the enzyme and the pegylation principle but are not shown to share PK, so the dog
efficacy data transfer as a **class-level TRANSFER, with the enzyme activity (IU) as the common unit**,
not as a product-identical claim.

### Canine IC50 / measured kill rate

- **No canine IC50 exists in retrievable form.** PMID **24033105** (`Expression of asparagine synthetase
  predicts in vitro response to L-asparaginase in canine lymphoid cell lines`,
  [DOI](https://doi.org/10.3109/10428194.2013.842980)) establishes that **L-asp sensitivity in canine
  lymphoid lines is strongly negatively correlated with ASNS promoter methylation**, that selected
  resistance raised ASNS methylation and lowered ASNS mRNA, and that 5-azacytidine **increased** resistance
  to L-asp. **IC50 values are not in the abstract and the full text is not open** — unchanged from the
  record's "Dose-response numbers: NOT OBTAINED" (`SWEEP_regrade.md:10`). Critically, the same paper
  reports that **"ASNS methylation and expression is not predictive of overall survival or progression-free
  survival in canine lymphoma patients treated with L-asp"** — so the in-vitro predictor does **not**
  carry to the clinic.
- PMID **23738234** (PMC3655665, [DOI](https://doi.org/10.1155/2013/786162)): canine **17-71** and
  **OSW** lines (and feline MYA-1, F1B) at **10 IU/mL × 24 h** lose proliferation with asparagine
  depleted; cold-stored enzyme retains activity. **Single concentration, no dose-response, no IC50.** **[REC]**
- **Why no kill rate can be derived, and what is missing.** The project's formula
  `k = ln(1 + C_free/IC50_free)/assay_days` **does not apply**: the dose unit is enzymatic activity
  (IU/mL), not a free concentration, and the pharmacodynamic driver is **days held at CSF/serum Asn < ~1 µM**,
  not a concentration ratio. The record states this (`SWEEP_regrade.md:11`). **Missing numbers that would
  let a kill rate be derived:** (i) a canine-lymphoma dose-response in IU/mL with a time axis, (ii) the
  canine serum/CSF asparagine-vs-time curve at a stated dose, (iii) a kill-vs-duration-of-depletion
  relation. **Only an OUTCOME rate is available**, and the record already carries it as **0.03-0.05 /day**
  (`LYMPHOMA_UNIVERSE.md:356`). **I am not estimating a new one.** The new 217-day randomised CR-relapse
  figure (PMID 1522554) is a **combination** outcome and must not be attributed to asparaginase alone.

### Verdict for the catalogue

**ENTER, with its grade stated, as a non-pumped, non-p53, non-marrow, non-GI agent — but NOT as a
dormancy closer.** Honest grading: potency **OUTCOME** (dog, incl. one randomised n=69 trial); pump
status **MECHANISM/class**; p53-independence **MECHANISM + one p53-null combination result (PMID
11561778)**, direct comparison **NOT FOUND**; dormant-cell kill **negative (settled, do not re-open)**;
toxicity axes **immune/hypersensitivity (48% native → ~0% PEG) + pancreatic (0/52 alone; 14% cPLI with
vincristine) + hepatic**, marrow **not dose-limiting**; limiter is an **antibody clock**, not a cumulative
organ dose.

---

## 2. PLATINUM AGENTS

### 2a. Carboplatin — **NEW for canine lymphoma**

- **Efficacy, n=22 relapsed/refractory canine lymphoma** (carboplatin alone n=8; carboplatin + cytarabine
  n=14): **ORR 18.2% (4/22)**. **All four responders received both drugs**, giving **28.6% (4/14) for the
  combination and 0/8 for carboplatin alone.** Median **TTP 18 days** (56 d responders, 12 d
  non-responders, P=0.0006); median **OS 28 days** (109 vs 21 d, P=0.0007). PMID **26463827**,
  [DOI](https://doi.org/10.1111/vco.12176). Grade: **MEASURED (dog)**. **Single-agent carboplatin has
  0/8 responses in canine lymphoma — that is a kill-contradicted exclusion under rule 13, not an
  absence-of-data exclusion.**
- **Dose-limiting axis: MARROW, severely — both lineages.** Thrombocytopenia **84.2% (16/19)**,
  neutropenia **52.6% (10/19)**; **grade IV** thrombocytopenia in **56.3% (9/16)** and grade IV
  neutropenia in **60.0% (6/10)** of those affected. Dogs receiving both drugs were significantly more
  likely to become neutropenic (P=0.022) or thrombocytopenic (P=0.001). "toxicity was high and the
  responses were not durable." Same PMID 26463827. Also: carboplatin induced relative normoblastemia
  >1% in 37.0% and absolute normoblastemia in 34.8% of treated dogs (PMID **26109175**,
  [DOI](https://doi.org/10.1111/vco.12156)) — which **can mask neutropenia** by inflating WBC counts.
- Canine dose/schedule: the paper's dose is not in the abstract — **NOT FOUND here**; canine carboplatin
  is conventionally 250-300 mg/m² IV q3wk, which I did **not** verify in a source read this sweep, so it
  is **unverified**.
- P-gp substrate? **No** — platinum complexes are not ABCB1 substrates; platinum resistance runs through
  reduced uptake (CTR1), glutathione/metallothionein conjugation and **MRP2/ATP7A/B**, not ABCB1. Grade:
  **MECHANISM, class-level. I could not retrieve a clean primary citation** (my PubMed query was
  mis-translated into a NOT-expression returning 611 irrelevant hits) — so **ASSERTED, UNVERIFIED**.
- p53-dependent? Platinum kills by DNA crosslink → damage response, with **p53 a major but not exclusive**
  effector; platinum resistance is classically associated with p53 mutation. **Direction: partly
  p53-dependent — the wrong direction for this model.** No canine lymphoma p53-stratified data. **NOT FOUND.**
- Kills non-dividing cells? Crosslinking is formally cell-cycle-non-specific, but lethality requires
  replication/repair processing. **No quiescent-lymphoma data. NOT FOUND.**
- US lawful: carboplatin is FDA-approved (human, multiple ANDAs) → lawful extra-label in dogs under
  21 CFR 530. **Paraplatin brand discontinued; generics current** (not re-verified on an FDA page).
- Canine IC50: **NOT FOUND.**
- **Verdict: EXCLUDE on contradicted kill (0/8 single agent) plus a marrow axis that is the model's most
  contested budget. Fails the three-way conjunction on (c) outright.**

### 2b. Cisplatin

- **Canine lymphoma efficacy: NOT FOUND.** No canine lymphoma cisplatin series retrieved. The record
  holds cisplatin only as a dCK-cross-resistance comparator — in araC-resistant mantle-cell lymphoma
  lines, sensitivity to doxorubicin, **cisplatin**, bendamustine, bortezomib, temsirolimus and rituximab
  was "unaffected, or ... increased" (PMID **24972933**, `SWEEP_pk.md:155` **[REC]**). That is a
  statement about E2 (dCK loss), not about canine lymphoma efficacy.
- **Dose-limiting axis in dogs: RENAL.** Cisplatin nephrotoxicity in dogs is initiated by "an acute,
  mainly proximal tubular impairment, preceding alterations in renal hemodynamics" — renal blood flow and
  GFR unchanged immediately after dosing while proximal reabsorption fell significantly; by 48-72 h both
  proximal and distal reabsorptive capacity were impaired with increased renal vascular resistance. "The
  use of the drug is hampered by side effects — especially **renal toxicity which is dose limiting**."
  PMID **2178884** (dog + rat + human). Grade: **MEASURED (dog), mechanism of the DLT**. Secondary: GI
  (emesis) — in dogs and rats, calcium/ergocalciferol supplementation "seem to protect against severe
  gastrointestinal toxicity and nephrotoxicity", with gastrointestinal and nephrotoxicity named as "their
  dose-limiting factors in clinical oncology" (PMID **9436642**,
  [DOI](https://doi.org/10.1097/00001813-199711000-00010)).
  **Incidence figures in dogs with lymphoma: NOT FOUND.**
  *Cross-species caution:* cisplatin is contraindicated in cats (fatal pulmonary oedema); that is a feline
  finding and must not be transferred to dogs.
- Canine dose/schedule: **NOT FOUND in a source read this sweep** (conventionally 60-70 mg/m² IV with
  saline diuresis; unverified).
- P-gp? Same class answer and same caveat as carboplatin: **not an ABCB1 substrate (MECHANISM,
  UNVERIFIED)**.
- p53? Partly p53-dependent (as above). Non-dividing cells? **NOT FOUND.**
- US lawful: FDA-approved human generics → extra-label in dogs under 21 CFR 530.
- Canine lymphoma IC50: **NOT FOUND.**
- **Verdict: NOT ASSESSABLE for efficacy (no canine lymphoma data at all), and its renal axis is a new
  budget line. Interesting only because renal is NOT marrow/GI — but the GI co-DLT (PMID 9436642) and the
  p53 dependence both break the conjunction. Do not enter on current evidence.**

---

## 3. MITOXANTRONE

- **Single-agent efficacy in relapsing canine lymphoma, n=15** (12 B-cell, 3 T-cell; stage IV n=12,
  V n=3; all at first relapse after standard combination chemotherapy; median 98 days of prior
  chemotherapy). **6 mg/m² IV every 21 days.** **CR 7/15 (47%)**, **overall median duration of response
  21 days**, **median CR duration 84 days**; 9/15 (60%) later achieved CR with other chemotherapy after
  failing mitoxantrone. Authors' conclusion: mitoxantrone "as a single agent, has **limited value** for
  dogs with lymphoma at 1st relapse". PMID **9773407**,
  [DOI](https://doi.org/10.1111/j.1939-1676.1998.tb02130.x). Grade: **MEASURED (dog)**. **[NEW — the
  record had only mitox+DTIC]**
- Combination, n=44 relapsed after a doxorubicin-containing protocol: mitoxantrone **5 mg/m² IV over
  10 min** then DTIC **600 mg/m² IV over 5 h, every 3 weeks**: **ORR 34% (15/44, 95% CI 20-48%)**,
  **median duration 97 days** (range 24-636, 95% CI 44-150). Dogs that had achieved CR on initial
  **L-asparaginase/CHOP** were more likely to respond (23% vs 11%, P=0.035). PMID **30653362**,
  [DOI](https://doi.org/10.5326/JAAHA-MS-6878). **[REC — `SWEEP_modalities.md:123`]**
- **Dose-limiting axis: MARROW (neutrophil).** Grade 4 neutropenia **18%**, sepsis hospitalisation **5%**;
  GI toxicity uncommon (PMID 30653362). Single agent at 6 mg/m²: "Mild toxicities ... No adverse reactions
  were observed during mitoxantrone infusions" (PMID 9773407). Secondary axis **CARDIAC** — mitoxantrone
  is an anthracenedione with a cumulative cardiotoxicity ceiling in humans; **canine cardiac incidence
  figures: NOT FOUND.**
- **P-gp substrate? YES — and this is disqualifying.** Mitoxantrone is a classical substrate of **ABCG2
  (BCRP)** — BCRP was originally cloned from mitoxantrone-resistant cells and is still assayed with
  mitoxantrone — and is also handled by ABCB1. **I did not retrieve a primary citation this sweep**, and
  the record explicitly lists mitoxantrone P-gp status as "not verified; do not assume"
  (`SWEEP_modalities.md:206`). So: **expected YES, formally UNVERIFIED.** Either way it cannot be entered
  as pump-independent. Note the record's canine-specific finding that canine lymphoma becomes
  **P-gp/BCRP-positive after chemotherapy** (PMID 33518631, `SWEEP_regrade.md`), which makes a BCRP
  substrate a poor choice at relapse — exactly where mitoxantrone is used.
- p53-dependent? Topoisomerase-II poisoning → DNA damage → **p53-dependent apoptosis in large part**.
  No p53-stratified canine lymphoma data. **NOT FOUND.**
- Kills non-dividing cells? Topo-II poisoning requires replication/transcription; **essentially
  division-gated. No quiescent-cell data. NOT FOUND.**
- US lawful: mitoxantrone injection is FDA-approved (human) → extra-label in dogs under 21 CFR 530.
- Canine IC50: **NOT FOUND** (PMID 9773407 cites "its tumoricidal effect against canine lymphoma" without
  a number in the abstract).
- **Verdict: real, modest, measured dog efficacy (CR 47%, CR duration 84 d). Fails conjunction (a)
  (BCRP/P-gp), probably (b) (topo-II/p53), and (c) (marrow). Enter as a sequential non-cross-resistant
  line if desired, NOT as a conjunction candidate.**

---

## 4. ACTINOMYCIN-D / DACTINOMYCIN

- **Single-agent rescue, n=49 dogs** with relapsed or resistant lymphoma (1999-2006). Median dose
  **0.68 mg/m² (range 0.46-0.72) IV every 3 weeks** for 5 treatments or until progression; 26/49 (53%)
  got concurrent prednisone. **CR 20/49 (41%)**, **median disease-free interval in those dogs 129 days**.
  Concurrent prednisone, shorter first remission, and more prior chemotherapy agents each predicted
  **lower** response and shorter DFI. PMID **18673031**,
  [DOI](https://doi.org/10.2460/javma.233.3.446). Grade: **MEASURED (dog)**. **[NEW — the record had
  actinomycin-D only inside DMAC and the maintenance arm]**
- **Dose-limiting axis: MARROW, specifically PLATELET.** **Thrombocytopenia was the most common
  haematologic toxicosis, 22/49 (45%)**, described as mild; "treatment was well tolerated" (PMID
  18673031).
- In DMAC (dexamethasone, melphalan, actinomycin-D, cytarabine), two independent series:
  - n=54 relapsed: **72% remission (CR 44%, PR 28%)**, SD 11%, PD 17%; **median remission 61 days**
    (range 2-467+); CR/PR/SD subgroup medians **112 / 44 / 27 days**. **Thrombocytopenia 56%** (grade 3
    in 7, grade 4 in 7), neutropenia 17% (grade 4 in 4), GI 22%. PMID **17063713**,
    [DOI](https://doi.org/10.1892/0891-6640(2006)20[1178:dmadca]2.0.co;2). **[NEW pmid]**
  - n=86 after CHOP: **43% remission (CR 16%, PR 27%)**, 57% non-responders, **median PFS 24 days**;
    thrombocytopenia 41%, neutropenia 17%, GI 13%; grade III-IV thrombocytopenia 13/79 (16%). "The main
    toxicity is **thrombocytopenia, which may limit treatment**." PMID **24489398**, PMC3894879. **[NEW pmid]**
- Dacarbazine + an anthracycline (doxorubicin **or dactinomycin**) vs temozolomide + anthracycline, n=63
  relapsed/refractory: CR+PR **25/35 (71%)** dacarbazine arm vs **13/18 (72%)** temozolomide arm; median
  duration of response **50 d** (0-587) vs **40 d** (0-217); high-grade haematologic toxicoses
  significantly **more** frequent with dacarbazine. PMID **17696856**,
  [DOI](https://doi.org/10.2460/javma.231.4.563). **[NEW pmid]**
- **P-gp substrate? YES, expected — actinomycin-D is one of the canonical ABCB1 substrates** (used as a
  reference substrate in MDR assays). **Primary citation not retrieved this sweep**; the record says "not
  verified; do not assume" (`SWEEP_modalities.md:206`). **Expected YES, formally UNVERIFIED** — either
  way, not enterable as pump-independent.
- p53-dependent? Actinomycin-D intercalates and blocks RNA polymerase → **it is a classical p53
  STABILISER/activator** (nucleolar stress, used experimentally to induce p53). That makes p53-dependence
  the expected direction and makes it a poor choice against a TP53-mutant clone. **No lymphoma
  p53-stratified data. NOT FOUND.**
- Kills non-dividing cells? Transcription inhibition is not strictly replication-dependent, so there is a
  mechanistic argument for quiescent activity — but **no quiescent-lymphoma measurement. NOT FOUND.**
- US lawful: Cosmegen (dactinomycin) is FDA-approved (human) → extra-label in dogs under 21 CFR 530.
- Canine IC50: **NOT FOUND.**
- **Verdict: best measured single-agent rescue numbers of any drug in this sweep (CR 41%, DFI 129 d).
  Fails conjunction (a) and (b) on expected grounds and (c) on the 45% thrombocytopenia.**

---

## 5. CHLORAMBUCIL, MELPHALAN, BENDAMUSTINE

### 5a. Chlorambucil

- **Efficacy — and this is the longest survival in this entire sweep, but it is a DIFFERENT DISEASE.**
  Low-grade **gastrointestinal** lymphoma, n=20 dogs, **95% T-cell phenotype**, 60% epitheliotropic;
  "chlorambucil and prednisone were most commonly prescribed"; **ORR 70%**, **median survival 424 days
  (95% CI 105-1206)**. PMID **29027206**, [DOI](https://doi.org/10.1111/jsap.12769). Grade: **MEASURED
  (dog)**. **[NEW]** **Scope warning (rule 10): this is INDOLENT, low-grade, alimentary T-cell disease —
  not the multicentric high-grade T-cell lymphoma the model is built on. The 424-day median reflects the
  indolent biology at least as much as the drug, and must be labelled INDIRECT for the model's case.**
- Mott-cell lymphoma, n=9 miniature dachshunds (alimentary, young dogs), treated with large-cell protocols
  **or alkylators such as melphalan or chlorambucil**: ORR **78%**, median **PFS 105 days**, median OS
  **240 days** (range 6 to >1513), significantly longer than 29 dachshunds with non-MCL alimentary
  large-cell lymphoma (57 d, p=0.0491). PMID **36401603**, PMC10029887,
  [DOI](https://doi.org/10.1002/vms3.975). **[NEW]** Again indolent/variant disease — INDIRECT.
- In the 408-dog maintenance trial the maintenance arm was **vincristine + chlorambucil + actinomycin-D**
  (no doxorubicin, cyclophosphamide or prednisolone), at **chlorambucil alternating with vincristine
  0.5-0.7 mg/m² IV q15d**, over a 2-year total treatment duration. PMID **28100766**. **[REC —
  `LYMPHOMA_UNIVERSE.md:723`, `SWEEP_additivity_calibration.md:19,49,83,389`; this is load-bearing for
  M.9/M.10 and must not be re-derived]**
- **Dose-limiting axis: MARROW, with a notable additional RENAL/TUBULAR axis in another species.**
  Myelosuppression (chiefly thrombocytopenia) is the classical DLT; **canine incidence figures: NOT
  FOUND** in any source read. **[NEW, cross-species]** **Acquired Fanconi syndrome (proximal tubular
  dysfunction: glucosuria with normoglycaemia, aminoaciduria) in 4 CATS on chlorambucil**, onset 2-26
  months, resolving partially or completely in 3/4 within 3 months of stopping. PMID **26170278**,
  PMC11112229, [DOI](https://doi.org/10.1177/1098612X15593108). **Label this FELINE and INDIRECT — it is
  a 4-cat case series and must not be transferred to dogs as a rate**; it is reported because a
  chronic-dosing program would need to watch for it, and the model has no "renal tubular" sub-axis.
- **CNS access — already in record and important:** canine **CSF chlorambucil median 0.1 ng/mL (range
  0-0.3)** (PMID **29775768**). **[REC — `SWEEP_exists.md:113`, `SWEEP_regrade.md:45`; the record also
  explicitly warns "do not transfer" this to lomustine.]** 0.1 ng/mL is a vanishingly small CSF level.
- P-gp substrate? Nitrogen-mustard alkylators are generally **not** ABCB1 substrates. **Chlorambucil
  specifically: NOT FOUND.**
- p53-dependent? Chlorambucil-induced apoptosis in CLL is substantially **p53-dependent**, and TP53
  mutation is an established mechanism of chlorambucil resistance in human CLL. **I did not retrieve a
  primary citation this sweep — ASSERTED, UNVERIFIED.** Direction is the wrong one for this model.
- Kills non-dividing cells? Mechanistically cell-cycle-non-specific, and it works clinically in indolent,
  low-proliferation disease (PMID 29027206) — which is **suggestive** but is an outcome in slowly-dividing
  bulk, **not** a dormant-progenitor measurement. **NOT FOUND.**
- US lawful: Leukeran FDA-approved (human) → extra-label in dogs under 21 CFR 530.
- Canine IC50: **NOT FOUND.**

### 5b. Melphalan — **ALREADY IN RECORD WITH NUMBERS; not re-derived**

`SWEEP_nongated.md:30` already holds: NCI-60 48 h GI50 **MOLT-4 2.8 / SR 1.7 / CCRF-CEM 2.9 µM**;
**P388 2.39 vs P388/ADR 5.72 = 2.4-fold cross-resistance, i.e. PARTIAL MDR — so melphalan IS partly
pump-affected**; Evomela label 100 mg/m² Cmax 5.8 µg/mL, AUC 451 µg·min/mL (24.6 µM·h), t½ 75 min,
protein binding 50-90%, "penetrates into CSF" with **no ratio**; derived systemic k 0.06-0.19/day,
**brain k not derivable**; and, from mouse, **melphalan depletes EARLY not late repopulating stem cells
(PMID 7917905) — "the opposite of what E5 needs"**. Canine role: the **M** of DMAC (PMIDs 17063713,
24489398 above), where the protocol axis is **thrombocytopenia 41-56%**. Canine single-agent melphalan
lymphoma efficacy: **NOT FOUND**. US lawful: Alkeran/Evomela FDA-approved → extra-label. **Verdict
unchanged: partial MDR + marrow axis + wrong stem-cell subset. Fails (a) partly and (c) outright.**

### 5c. Bendamustine

- **Canine lymphoma single-agent efficacy: NOT FOUND.** PubMed "bendamustine AND dogs AND lymphoma"
  returns exactly 2 records, neither an efficacy trial; "bendamustine AND dog AND phase AND maximum
  tolerated dose" returns **0**. **There is no canine bendamustine dose-finding or efficacy study
  retrievable.**
- What does exist in dogs is **lymphodepletion for CAR-T**: Penn is running a phase 0/1 of bendamustine
  lymphodepletion in dogs (**11 dogs piloted**) precisely because **"inability to use Cy/Flu regimens ...
  in canine CAR-T trials ... due to hematological toxicity and the subsequent requirement of transfusions
  that is difficult to meet in the veterinary clinics"**; **no result found**. PMIDs **38573683**
  (PMC11147717, review Table 3), **42480604**, **42969556**. **[REC — `LYMPHOMA_UNIVERSE.md:686`,
  `SWEEP_near_future_cell.md:22,160,171`]**
- **Dose-limiting axis: MARROW** (that is the entire reason it is being trialled as a lymphodepletant,
  and the reason Cy/Flu was abandoned). **Canine incidence: NOT FOUND.**
- Relevant negative-space facts already in record: bendamustine sensitivity is **unaffected or increased**
  in dCK-down araC-resistant MCL lines (PMID **24972933**, so it defeats E2); **no NCI-60 GI50 in ChEMBL**
  (`SWEEP_nongated.md:33`); searched for quiescent/non-dividing kill — **"no usable abstract found"**
  (`SWEEP_outside_model.md:130`); and `SWEEP_lawful_cns_agents.md:180` explicitly flags bendamustine as
  **not re-assessed**.
- P-gp? **NOT FOUND.** p53? Bendamustine is often argued to retain activity in p53-impaired CLL via a
  partly p53-independent, base-excision-repair-linked death — **I could not retrieve a citation this
  sweep; ASSERTED, UNVERIFIED, and it is the one alkylator where the p53 direction might be favourable.**
  **This is a named, worthwhile follow-up.**
- US lawful: Treanda/Bendeka/Belrapzo FDA-approved (human) → extra-label in dogs under 21 CFR 530.
- Canine IC50: **NOT FOUND.**
- **Verdict: NOT ASSESSABLE as a therapeutic agent in dogs (no efficacy or dose data at all). Fails (c)
  on marrow. Its possible p53-independence is unverified and is the single most interesting open thread
  among the alkylators.**

---

## 6. VINBLASTINE, ETOPOSIDE, HYDROXYUREA, PROCARBAZINE, DACARBAZINE, BLEOMYCIN

### 6a. Vinblastine
- **Canine lymphoma efficacy: NOT FOUND** (PubMed vinblastine + canine + lymphoma + rescue + outcome →
  2 hits, neither an efficacy series). Vinblastine is used in canine mast-cell tumour, not lymphoma.
- Toxicity axis in dogs: **MARROW**; and vinblastine+prednisone produced relative normoblastemia >1% in
  25.0% and absolute normoblastemia in 22.5% of dogs, with very severe absolute normoblastemia in 2.5%
  (PMID **26109175**, [DOI](https://doi.org/10.1111/vco.12156)) — again, **can mask neutropenia**.
- **P-gp substrate? YES — vinca alkaloids are canonical ABCB1 substrates.** The record holds the
  mouse P-gp-knockout sensitivity figure (**3×**, `SWEEP_brain_access.md:61`, flagged UNVERIFIED as a
  brain fold). **Disqualifying for (a).**
- p53? Tubulin poisons → mitotic arrest → apoptosis, substantially p53-modulated. Non-dividing cells?
  **No — strictly division-gated (requires mitosis).** US lawful: FDA-approved human generics →
  extra-label. Canine lymphoma IC50: **NOT FOUND.**
- **Verdict: fails (a) definitively, and fails the dormancy requirement by mechanism. Do not pursue.**

### 6b. Etoposide
- **Canine lymphoma efficacy: NOT FOUND.**
- **Canine PK is the decisive, and disqualifying, fact — [NEW].** 8 tumour-bearing dogs, open-label
  single-dose two-way crossover, etoposide 50 mg/m² IV vs the parenteral formulation given PO:
  **4 of 8 dogs had hypersensitivity reactions during IV administration** (vehicle-related: the
  polysorbate-80/Cremophor-type vehicle); plasma etoposide was **undetectable in 2 dogs** after oral
  dosing; **oral bioavailability median 13.4%, range 5.7-57.3%**. Conclusion: "**Vehicle-related
  toxicosis can limit the IV administration of etoposide in dogs**" and routine oral use "was not
  supported because of low and variable oral bioavailability". PMID **18828689**,
  [DOI](https://doi.org/10.2460/ajvr.69.10.1316). Grade: **MEASURED (dog)**.
- **Dose-limiting axis: PROCEDURAL/IMMUNE (vehicle hypersensitivity, 50% of dogs IV) then MARROW.**
  This is an unusual axis — but it is a formulation defect, not a therapeutic window.
- Intrathecal etoposide in dogs **[REC — `SWEEP_regional.md:224`]**: 0.01-1.0 mg/kg IT, CSF 3-4 logs
  above plasma, cord concentration much higher near the injection site than distally, **"Severe
  neurotoxicity occurred at the higher doses"**, "limited diffusion" (PMID **1517797**,
  [DOI](https://doi.org/10.1007/BF00172472)).
- **P-gp substrate? YES — etoposide is a well-established ABCB1 substrate.** (Primary citation not
  retrieved this sweep; class-level, **UNVERIFIED**.) p53? Topo-II poison → largely p53-dependent.
  Non-dividing? Division-gated. US lawful: FDA-approved (human) → extra-label. Canine IC50: **NOT FOUND.**
- **Verdict: EXCLUDE — 50% IV hypersensitivity and 13% erratic oral bioavailability in dogs make it
  undeliverable, independent of the P-gp and p53 failures.**

### 6c. Hydroxyurea
- **Record status: a NAMED LEAD, not an evaluated agent** — `LYMPHOMA_UNIVERSE.md:359` ("hydroxyurea
  (dCK-independent; dog on continuous dosing ≥448 days; CSF penetration not found)") and `:402`;
  `SWEEP_lawful_cns_agents.md:180` flags it as **not re-assessed**. **[REC]**
- **Canine lymphoma efficacy: NOT FOUND.** My PubMed queries (hydroxyurea + dogs + leukemia/lymphoma;
  + chronic leukemia/polycythemia/dose) returned **0 usable hits** because of query translation; this is
  a **search failure as much as an evidence absence**, and I say so plainly. Hydroxyurea is used clinically
  in canine polycythaemia vera and chronic myeloid leukaemias, which I could **not** document here.
- The one quantitative CNS datum in the record **[REC — `SWEEP_cnsregimens.md:116`]**: rhesus
  ventriculocisternal perfusion periventricular distribution space **hydroxyurea 56 µL/100 mg**
  (vs MTX 27, thiotepa 28, BCNU 64, ara-C >170) (PMID **810575**).
- Axis: **MARROW** (it is an antiproliferative used to cytoreduce), with a secondary **SKIN/mucosal** axis
  in humans. **Canine incidence: NOT FOUND.** P-gp: **NOT FOUND** (small, hydrophilic — a substrate is
  unlikely). p53: ribonucleotide-reductase inhibition → replication stress → S-phase arrest; p53
  involvement unclear, **NOT FOUND**. Non-dividing cells: **NO — hydroxyurea is strictly S-phase-specific
  by mechanism**, which rules it out for dormancy. US lawful: Hydrea/Droxia FDA-approved → extra-label.
  Canine IC50: **NOT FOUND.**
- **Verdict: appealing on its oral, continuous-dosing, dCK-independent profile (which is why the record
  listed it as a T-cell-brain lead), but S-phase specificity kills the dormancy case and its marrow axis
  breaks (c). Its canine lymphoma evidence remains genuinely unsearched — flagged, not claimed.**

### 6d. Procarbazine — **ALREADY IN RECORD, EVALUATED; not re-derived**
`SWEEP_lawful_cns_agents.md:100-112` already holds: Matulane FDA-approved, extra-label in dogs, used in
LOPP/MOPP/PPC; label "crosses the blood-brain barrier and rapidly equilibrates between plasma and
cerebrospinal fluid after oral administration" (qualitative, **no ratio**); parent t½ ~10 min IV, needs
hepatic CYP activation so **parent CSF level does not measure the active species**; Kp,uu **NOT FOUND**.
Canine outcomes: oral procarbazine + prednisolone + cyclophosphamide daily, n=50 failed/intolerant dogs
**ORR 70% (CR 46%), "very well tolerated"** (PMID **35338560**,
[DOI](https://doi.org/10.1111/vco.12814)); **LOPP naive T-cell n=35 median PFS 431 d** (PMID 30117253);
n=31 ORR 97% (28508557); n=67 PFS 118 d (34464024); UF-LOPP rescue n=33 ORR 61% (21756176); MPP rescue
n=41 ORR 34% (19222829). Escapes **MGMT** (shared with lomustine/TMZ) and MMR loss; **dCK/RFC-independent**;
**P-gp NOT FOUND; cycle dependence NOT FOUND**; kill **OUTCOME-only** (prodrug, multi-agent).
**Nothing in this sweep changes that. The 431-day LOPP PFS in naive T-cell disease is the strongest
T-cell outcome among these drugs and is already recorded.**

### 6e. Dacarbazine
- Single agent **800-1000 mg/m²**, n=40: **ORR 35%, median PFI 43 days; thrombocytopenia dose-limiting.**
  PMID **19709354**, [DOI](https://doi.org/10.1111/j.1939-1676.2009.0376.x). **[REC —
  `SWEEP_modalities.md:122`; PMID 20391633 is a duplicate record of the same title]**
- Combinations: with mitoxantrone, ORR 34%/97 d, grade 4 neutropenia 18%, sepsis 5% (PMID 30653362);
  with an anthracycline, 71% ORR / 50 d median duration, **significantly more high-grade haematologic
  toxicoses than the temozolomide arm** (PMID 17696856). **[NEW pmid for the latter]**
- **Dose-limiting axis: MARROW — specifically PLATELET** (explicit in PMID 19709354), with neutropenia in
  combination. Secondary GI.
- P-gp? **NOT FOUND**; the record says "not verified; do not assume" (`SWEEP_modalities.md:206`).
  Alkylating triazene — a substrate is unlikely. p53? Methylating agent → O6-methylguanine → MMR-dependent
  damage signalling, **largely p53-dependent**, with **MGMT** the dominant escape (shared with lomustine,
  temozolomide and procarbazine — so it stacks poorly with them). Non-dividing cells? Record: temozolomide
  NCI-60 GI50 **84/>100/78 µM**, "far above CSF levels: not a closer" (`SWEEP_nongated.md:32`) — the same
  class limitation. **NOT FOUND** for dacarbazine quiescence. US lawful: FDA-approved (human) →
  extra-label. Canine IC50: **NOT FOUND.**
- **Verdict: measured dog efficacy, but fails (c) on dose-limiting thrombocytopenia and shares MGMT with
  agents already in the program.**

### 6f. Bleomycin
- **Canine lymphoma efficacy: NOT FOUND.** PubMed bleomycin + dogs + lymphoma + intralesional → **0**.
  The only canine-lymphoma bleomycin datum in the record is **as an assay reagent, not a therapy**:
  a G2 chromosomal-radiosensitivity assay on stimulated lymphocytes from 21 golden retrievers with
  lymphoma vs 20 healthy GR vs 20 healthy mixed-breed dogs, after 1.0 Gy or bleomycin; lymphoma-bearing
  GR were **21.2× more likely to be classified "sensitive"** (OR 21.2, 95% CI 2.3-195.8). PMID
  **23935952** (Thamm 2013, PLoS One 8:e69192). **[REC — `SWEEP_rt2.md:136`; the record already labels
  this "not a tumour radiosensitivity measurement" because the cells are germline, not malignant.]**
- **Dose-limiting axis: PULMONARY (fibrosis), cumulative — NOT marrow, NOT GI.** This is the one
  genuinely interesting thing about bleomycin for this model's budget. **Canine lymphoma incidence
  figures: NOT FOUND.** (The record's pulmonary-axis precedent is rabacfosadine: pulmonary fibrosis
  5/120 = 4%, all fatal or euthanised, capping that agent at ~4 doses — so this axis is already known to
  be a hard, irreversible cap.)
- P-gp? Bleomycin is a large hydrophilic glycopeptide — **not an ABCB1 substrate; NOT FOUND as a
  citation.** Resistance runs through **bleomycin hydrolase**, not efflux. p53? Causes free-radical DNA
  strand breaks → damage response; **p53 involvement NOT FOUND.** Non-dividing cells? Direct DNA
  scission is not replication-dependent — mechanistically promising, but **NOT FOUND** in lymphoma.
  US lawful: FDA-approved (human) → extra-label. Canine IC50: **NOT FOUND.**
- **Verdict: NOT ASSESSABLE — no canine lymphoma efficacy at all. Its non-marrow, non-GI axis means it
  would pass (c), and it may pass (a); but with zero efficacy data and an irreversible pulmonary cap it
  cannot be entered. Listed in the shortlist as a research lead only.**

---

## 7. SUMMARY TABLE

Axis names use the model's own list (marrow, GI, hepatic, cardiac, renal, pulmonary, bladder, peripheral
nerve, local CNS, steroid-class, immune/cytokine, ocular, skin, procedural).

| drug | canine lymphoma efficacy (n) | canine dose | dose-limiting axis + incidence (dogs) | P-gp substrate? | p53-dependent? | kills non-dividing? | US lawful status | grade |
|---|---|---|---|---|---|---|---|---|
| **L-asparaginase / PEG-asp** | **RCT n=69 +CHOP: CR 85.7%/94.1%, median TTR 217/214 d** (1522554); single agent n=20: CR 7/PR 7/NR 5, median 48 d (14-102) (3567863); n=73 +steroid ORR 80% (27086733); no benefit as COP add-on (15995158) | 400 IU/kg IP (native); 10,000 IU/m² SC; PEG 10-30 IU/kg IP/IM weekly | **IMMUNE/hypersensitivity: 48% native (anaphylaxis 9/29) → ~0% PEG** (2145933); **pancreatic: 0/52 ASNase alone, 14% cPLI rise with vincristine** (19436578); hepatic. **MARROW NOT DOSE-LIMITING** (no cytopenia in 5 series). Limiter = anti-drug antibodies 3/10 after 1 dose (23253146) | **NO — extracellular ~140 kDa enzyme, no transportable species** (MECHANISM, class) | **Expected NO** (starvation, not DNA damage); p53-null synergy shown for the 3-drug TGAP regimen (11561778); **asparaginase-alone comparison NOT FOUND** | **NO — cytostatic-then-apoptotic; dormant evidence NEGATIVE** (34863941, 23365669) | Elspar discontinued 2012; **Oncaspar (BLA 103411), Asparlas (BLA 761102), Rylaze current** → lawful extra-label 21 CFR 530. Compounded bulk (what vets use) is outside 530, GFI #256 enforcement discretion only | **OUTCOME (dog, randomised)**; pump MECHANISM; p53 MECHANISM+partial; dormancy NEGATIVE |
| **Carboplatin** | **ORR 18.2% (4/22); 0/8 single agent, 4/14 (28.6%) with cytarabine; TTP 18 d, OS 28 d** (26463827) | not in abstract (NOT FOUND) | **MARROW: thrombocytopenia 84.2%, neutropenia 52.6%; grade IV 56.3%/60.0%** (26463827) | NO (MECHANISM, class; **UNVERIFIED**) | Partly **YES** (crosslink→damage) | NOT FOUND | FDA-approved generics → extra-label | **EXCLUDE: kill contradicted (0/8)** |
| **Cisplatin** | **NOT FOUND** | NOT FOUND | **RENAL (proximal tubular), dose-limiting** (2178884); GI co-DLT (9436642). Dog lymphoma incidence NOT FOUND | NO (MECHANISM, class; **UNVERIFIED**) | Partly **YES** | NOT FOUND | FDA-approved → extra-label | **NOT ASSESSABLE** |
| **Mitoxantrone** | **single agent n=15: CR 47% (7/15), median DOR 21 d, median CR duration 84 d** (9773407); +DTIC n=44 ORR 34%, 97 d (30653362) | **6 mg/m² IV q21d** single agent; 5 mg/m² with DTIC | **MARROW: grade 4 neutropenia 18%, sepsis 5%** (30653362); single agent "mild" (9773407). Secondary **CARDIAC** (cumulative; dog incidence NOT FOUND) | **Expected YES (ABCG2/BCRP + ABCB1)**; record says "not verified" | Expected **YES** (topo-II) | NO (division-gated) | FDA-approved → extra-label | MEASURED (dog); fails (a)(b)(c) |
| **Actinomycin-D** | **single agent n=49: CR 41% (20/49), median DFI 129 d** (18673031); DMAC n=54 72%/61 d (17063713), n=86 43%/24 d (24489398) | **0.68 mg/m² (0.46-0.72) IV q3wk ×5** | **MARROW/PLATELET: thrombocytopenia 45% (22/49)** (18673031); DMAC thrombocytopenia 41-56%, "may limit treatment" | **Expected YES (canonical ABCB1)**; record "not verified" | Expected **YES** (p53 stabiliser) | NOT FOUND (mechanistic case exists) | Cosmegen FDA-approved → extra-label | MEASURED (dog); fails (a)(b)(c) |
| **Chlorambucil** | **low-grade GI (95% T): ORR 70%, MST 424 d (105-1206)** (29027206) — **INDOLENT disease, INDIRECT**; Mott-cell n=9 ORR 78%, PFS 105 d (36401603) | per protocol (maintenance: alternating with vincristine q15d, 2 y) (28100766) | **MARROW (dog incidence NOT FOUND)**; **feline Fanconi syndrome 4 cats, INDIRECT** (26170278) | NOT FOUND (mustard; unlikely) | Expected **YES** (CLL p53-dependent; **UNVERIFIED**) | NOT FOUND (works in indolent bulk, not a dormancy measurement) | Leukeran FDA-approved → extra-label | MEASURED (dog) but **wrong disease scope** |
| **Melphalan** | DMAC component only; single agent NOT FOUND | DMAC protocol | **MARROW/PLATELET 41-56%** (DMAC) | **PARTIAL (2.4× P388 vs P388/ADR)** [REC] | NOT FOUND | **NO — depletes EARLY not late HSC (7917905), opposite of E5** [REC] | Alkeran/Evomela → extra-label | **ALREADY IN RECORD; unchanged** |
| **Bendamustine** | **NOT FOUND (no canine efficacy or dose-finding study exists)** | NOT FOUND; lymphodepletion pilot 11 dogs, no result | **MARROW** (the reason Cy/Flu was abandoned in dog CAR-T) | NOT FOUND | **Possibly NO** — the one favourable direction, **UNVERIFIED** | searched, **"no usable abstract found"** [REC] | Treanda/Bendeka → extra-label | **NOT ASSESSABLE; p53 thread open** |
| **Vinblastine** | **NOT FOUND** | — | **MARROW**; normoblastemia 25%/22.5% masks neutropenia (26109175) | **YES (canonical vinca/ABCB1)** | Partly YES | **NO (needs mitosis)** | FDA-approved → extra-label | **EXCLUDE on (a) + mechanism** |
| **Etoposide** | **NOT FOUND** | 50 mg/m² IV/PO studied; **oral F median 13.4% (5.7-57.3%), undetectable in 2/8** (18828689) | **PROCEDURAL/IMMUNE: vehicle hypersensitivity 4/8 (50%) on IV** (18828689); then MARROW; IT: severe neurotoxicity at higher dose (1517797) | **YES (class)** | Expected YES (topo-II) | NO (division-gated) | FDA-approved → extra-label | **EXCLUDE: undeliverable in dogs** |
| **Hydroxyurea** | **NOT FOUND (also under-searched — my queries failed to translate)** | NOT FOUND; record: one dog continuous ≥448 d | **MARROW**; secondary skin/mucosal. Dog incidence NOT FOUND | NOT FOUND (unlikely) | NOT FOUND | **NO — S-phase-specific by mechanism** | Hydrea/Droxia → extra-label | **LEAD only [REC]** |
| **Procarbazine** | **LOPP naive T-cell n=35 median PFS 431 d** (30117253); n=50 ORR 70%/CR 46% (35338560); +4 more series | oral daily, in LOPP/MOPP/PPC | "very well tolerated" (35338560); human: marrow + GI. Dog axis incidence NOT FOUND | **NOT FOUND** [REC] | NOT FOUND; **MGMT escape** (shared with lomustine/TMZ) | **NOT FOUND** [REC] | Matulane FDA-approved → extra-label | **ALREADY IN RECORD, evaluated; unchanged** |
| **Dacarbazine** | **single agent n=40: ORR 35%, PFI 43 d** (19709354); +anthracycline 71%/50 d (17696856) | **800-1000 mg/m²**; 600 mg/m² over 5 h with mitoxantrone | **MARROW/PLATELET: thrombocytopenia dose-limiting** (19709354); grade 4 neutropenia 18% in combination | NOT FOUND [REC "do not assume"] | Expected YES; **MGMT escape** | NOT FOUND (TMZ class GI50 78->100 µM, "not a closer") | FDA-approved → extra-label | MEASURED (dog); fails (c) |
| **Bleomycin** | **NOT FOUND** (only as an assay reagent, 23935952) | NOT FOUND | **PULMONARY fibrosis, cumulative — NOT marrow, NOT GI.** Dog incidence NOT FOUND | Expected NO (hydrophilic glycopeptide; resistance = bleomycin hydrolase) | NOT FOUND | Mechanistically plausible (direct strand scission); **NOT FOUND** | FDA-approved → extra-label | **NOT ASSESSABLE; lead only** |

---

## 8. THE THREE-WAY CONJUNCTION

**Question asked:** is there any other FDA-approved drug, of any class, whose killing of lymphoma cells is
(a) not defeated by P-glycoprotein efflux, **and** (b) not dependent on p53/apoptosis, **and** (c) whose
dose-limiting toxicity is **not** myelosuppression or gastrointestinal?

Candidate universe searched (rule 9): all 21 drugs above, plus every class the record already holds —
cytotoxics, alkylators, nucleoside analogues, targeted/inhibitors, antibodies and ADCs, bispecifics,
immunotoxins, cell therapies, transplant, vaccines, checkpoint/cytokine agents, radiation and
sanctuary-site delivery. **Ranked shortlist, with the failure named for each rejection:**

### Tier 1 — passes all three

**1. L-ASPARAGINASE (and pegaspargase / calaspargase pegol / Erwinia asparaginase).**
(a) **PASS** — extracellular ~140 kDa enzyme; nothing to efflux. (b) **PASS (expected)** — kill is
protein-synthesis starvation via asparagine depletion, not DNA-damage→p53; supported by p53-null synergy
in PMID 11561778, with the asparaginase-alone comparison **NOT FOUND**. (c) **PASS** — axes are
immune/hypersensitivity (48% native → ~0% PEG, PMID 2145933), pancreatic (**0/52** on asparaginase alone,
PMID 19436578) and hepatic; **marrow is not dose-limiting and GI is minor**. Plus: real randomised dog
efficacy (CR 85.7%, median TTR 217 d with CHOP, PMID 1522554) and three lawful FDA-approved supply
routes. **Caveat that must travel with it: it does NOT kill dormant cells (settled, negative), and its
limiter is an antibody clock, not an organ dose.**

**2. DENILEUKIN DIFTITOX-cxdl (Lymphir), FDA-approved 2024 — the strongest NEW candidate, and already
flagged in the record as "lawful but never evaluated" (`LYMPHOMA_UNIVERSE.md:591`).**
- Mechanism: diphtheria-toxin fragments A/B fused to human IL-2; the toxin ADP-ribosylates elongation
  factor 2 and **arrests protein synthesis** — the *same* death mode as asparaginase, and likewise not a
  DNA-damage/p53 route. (a) **PASS** — a fusion protein entering by IL-2-receptor-mediated endocytosis is
  not an ABCB1 substrate. (b) **PASS (expected, mechanism-level; a p53-stratified lymphoma comparison was
  NOT FOUND).** (c) **PASS** — phase III, n=69 R/R CTCL: TEAEs of special interest were **infusion
  reaction 73.9%, hypersensitivity 68.1%, hepatotoxicity 36.2%, capillary leak syndrome 20.3% (grade ≥3
  5.8%)**, plus nausea 43.5% and fatigue 31.9%; **no cytopenia among the special-interest AEs**. Axes:
  immune/cytokine + hepatic + procedural.
- Efficacy: **ORR 36.2% (95% CI 25.0-48.7), CR 8.7%, median DOR 8.9 months, median TTR 1.4 months**;
  84.4% had decreased skin tumour burden. PMID **39700456**, PMC11949209,
  [DOI](https://doi.org/10.1200/JCO-24-01549). **This is T-cell lymphoma — the model's hard case.**
  Record also notes human ORR ~16% in PTCL (`LYMPHOMA_UNIVERSE.md:591`).
- **It has a canine dose already, at the same mg/kg as the human label — this is the key transfer.**
  6 dogs given **denileukin diftitox 9 µg/kg/day IV** on days 2,4,5,7,8,10 post-transplant with
  methotrexate (PMID **16920555**, [DOI](https://doi.org/10.1016/j.bbmt.2006.05.005)); and a **single
  18 µg/kg IV dose** in DLA-identical mixed-chimerism dogs, where **canine Treg were confirmed as a
  target in vitro** (suppression abolished, proliferation +300%, range 200-425%, at 10 nM) (PMID
  **22173275**, [DOI](https://doi.org/10.1016/j.vetimm.2011.11.009)). The human phase III dose is
  **9 µg/kg/day × 5 days q21d** — **identical to the canine 9 µg/kg/day**. So the dose transfer is
  essentially 1:1 and already demonstrated tolerable in dogs.
- **Honest limits:** both canine studies used it as a **Treg-depleting immunomodulator in transplant, not
  as an anti-lymphoma agent**; it did **not** prevent GVHD (median survival 16 d vs 20 d in 35 historical
  controls) and did not shift chimerism. **No canine lymphoma efficacy, no canine IC50, no canine kill
  rate.** CD25/IL-2R expression on canine lymphoma cells: **NOT FOUND** — and that is the gating input,
  because the drug only reaches IL-2R-bearing cells. **Grade: lawful (FDA 2024); human efficacy MEASURED;
  canine dose MEASURED; canine anti-lymphoma kill NOT FOUND → OUTCOME-transferable only after CD25
  status in canine lymphoma is established.**

**3. MOXETUMOMAB PASUDOTOX — same logic, already in record with durable-remission data.**
A CD22-targeted Pseudomonas exotoxin PE38 immunotoxin: also an **EF-2/protein-synthesis** killer, so (a)
and (b) pass on the same mechanistic grounds, and (c) passes — in 80 hairy-cell-leukaemia patients
**HUS and capillary leak each ≤10%**, with **CR 41%, durable CR (>180 d) 36%, 82% of complete responders
MRD-negative, CR lasting ≥60 months in 61%, median PFS without loss of haematologic remission 71.7
months** (PMID **33627164**, [DOI](https://doi.org/10.1186/s13045-020-01004-y)). **[REC —
`SWEEP_bispecific.md:86`, where the record already draws the right lesson: "a PE toxin can give
MRD-negative, multi-year remission in a B-cell neoplasm (a leukaemia with low proliferation)".]**
**Limits: CD22 is B-lineage (wrong target for the T-cell case); moxetumomab was WITHDRAWN from the US
market in 2023 — so its FDA-approved status is historical, which breaks the lawfulness premise.** Keep it
as the **proof of principle that this mechanism class delivers multi-year remissions**, not as a usable agent.

### Tier 2 — passes (a) and (b), fails or is unverified on (c)

**4. ARSENIC TRIOXIDE (Trisenox).** (c) **PASSES on axis** — the DLT is differentiation syndrome and
**QT prolongation/cardiac**, not marrow or GI. (b) plausibly passes (p53-independent routes). (a)
plausibly passes ABCB1, **but** As-GSH is transported by **MRP1** (PMID **32470611**) — so it is
pump-affected, just by a different pump, which fails the spirit of (a). **Already EXCLUDED in the record
on CNS access**: DLBCL-line IC50 **2.21 µM** vs CSF only **14-19% of plasma** (CSF 95.8 vs plasma 498.9
nmol/L, PMID 18703707), giving k 0.014-0.024/day (`SWEEP_nongated.md:50,71`). **Canine lymphoma: NOT
FOUND.** Verdict: **stays excluded, for the reason already recorded.**

**5. BLEOMYCIN.** (c) **PASSES** (pulmonary, cumulative — not marrow/GI). (a) probably passes. (b)
unknown. **Fails on having zero canine lymphoma efficacy data and an irreversible pulmonary cap.**
Research lead only.

**6. CISPLATIN.** (c) **half-passes** (renal is a fresh axis) but GI is a named co-DLT (PMID 9436642),
and (b) fails (p53-dependent). **Rejected.**

### Explicitly rejected, with the reason named (rule 13 — never "no canine data")

| candidate | fails on | evidence |
|---|---|---|
| Bortezomib / proteasome inhibitors | **(a)** — record: "**pump substrates** (panobinostat, bortezomib)", entered at k 0.048/day, "below the bar everywhere" | `LYMPHOMA_UNIVERSE.md:26,124` [REC] |
| Romidepsin | **(a)** — a well-known ABCB1 substrate; record groups it with "pump substrates or division-gated" | `LYMPHOMA_UNIVERSE.md:220` [REC] |
| Panobinostat | **(a)** — "P-gp and BCRP substrate" | `LYMPHOMA_UNIVERSE.md:26` [REC] |
| Vorinostat | **(c)/potency** — not a pump substrate, but k 0.026, "sub-bar" | `LYMPHOMA_UNIVERSE.md:26,124` [REC] |
| Brentuximab vedotin / PBD ADCs | **(a)** — MMAE is a P-gp substrate; PBD payloads effluxed by ABCG2 | `SWEEP_tcell_agents.md:5`, `SWEEP_nongated.md:71` [REC] |
| Venetoclax | **(b)** — it IS the apoptosis/BCL2 axis, so it is p53/apoptosis-machinery-dependent by definition | `LYMPHOMA_UNIVERSE.md:224` [REC] |
| Vincristine, vinblastine, etoposide, mitoxantrone, actinomycin-D | **(a)** — canonical ABCB1 (or BCRP) substrates | above |
| Glucocorticoids | **(a)** — dexamethasone is an ABCB1 substrate; and already in the catalogue on the steroid-class axis | `lymphoma_catalogue.py:145` |
| Duvelisib / idelalisib / RV1001 | **(a)** — "P-gp/BCRP; dog TTP 21-25 d" | `SWEEP_tcell_agents.md:5` [REC] |
| Tazemetostat / EZH2 | **(a)** — "(P-gp)" | `SWEEP_tcell_agents.md:5` [REC] |
| Lenalidomide / IMiDs | target mismatch — **canine CRBN Ile** variant | `SWEEP_tcell_agents.md:5`, `SWEEP_nongated.md:71` [REC] |
| Magrolimab / CD47 | **withdrawn** (deaths) + CNS | `SWEEP_nongated.md:71` [REC] |
| Omacetaxine (Synribo) | **(c)** — a protein-synthesis inhibitor, so (a)/(b) look favourable, but its DLT **is myelosuppression**. **Not in record (grep: zero hits) — the one Tier-1-mechanism drug I did not find a record entry for; flagged as unassessed.** | — |

### Ranked shortlist meeting the conjunction

1. **L-asparaginase / pegaspargase / calaspargase / Rylaze** — passes all three; randomised dog efficacy;
   three lawful FDA-approved routes; marrow-free, GI-light. **Does not kill dormant cells.**
2. **Denileukin diftitox-cxdl (Lymphir)** — passes all three; FDA-approved 2024 **for T-cell lymphoma**;
   **canine dose already published at the identical 9 µg/kg/day**; gated on an unmeasured input (CD25/IL-2R
   on canine lymphoma cells).
3. **Moxetumomab pasudotox** — the mechanism-class proof of multi-year MRD-negative remission, but
   **US-withdrawn** and CD22/B-lineage. Not usable; keep as the precedent.
4. **Bleomycin** — axis passes (pulmonary), (a) likely passes, but no canine lymphoma efficacy at all.
5. **Arsenic trioxide** — cardiac axis passes, but MRP1-transported and already excluded on CNS access.

**The structural finding: every drug that passes this conjunction kills by arresting PROTEIN SYNTHESIS
(asparagine starvation, or EF-2 ADP-ribosylation) rather than by damaging DNA.** That is why they escape
both P-gp (the effector is an enzyme or a protein toxin, not a small-molecule permeant) and p53 (no DNA
damage to signal). It is also why they share the *same* weakness: protein-synthesis arrest kills
proliferating cells and sends quiescent ones into reversible dormancy (PMIDs 34863941, 23365669), so
**this class answers the model's "P-gp + TP53" blocking combination but does not touch the dormant-cell
(E5) requirement.** Those two requirements need different agents, and conflating them would be the
error CLAUDE.md failure #4 warns about.

---

## 9. WHAT I COULD NOT VERIFY (stated plainly)

1. **No canine IC50 or measured kill rate for L-asparaginase** against canine lymphoma cells. PMID
   24033105's dose-response is behind a paywall; PMID 23738234 used a single 10 IU/mL concentration. The
   record's "NOT OBTAINED" stands. **Missing for a derivation:** a canine IU/mL dose-response with a time
   axis; a canine serum/CSF asparagine-vs-time curve at a stated dose; a kill-vs-duration-of-depletion
   relation. **I did not estimate one.**
2. **No direct asparaginase-alone p53-mutant vs p53-WT lymphoma comparison.** Four query forms returned
   0-1 hits. The p53-independence of asparaginase is **mechanistically expected and partially supported
   (PMID 11561778, a three-drug combination)**, not directly measured.
3. **P-gp/ABCB1 substrate status is formally UNVERIFIED for mitoxantrone, actinomycin-D, etoposide,
   vinblastine, melphalan, dacarbazine, chlorambucil, bendamustine, hydroxyurea, procarbazine, bleomycin
   and the platinums.** For several (vinca, etoposide, actinomycin-D, mitoxantrone) the class answer is
   not in real doubt, but I did not retrieve a primary citation this sweep, and the record's own standing
   instruction is "not verified; do not assume" (`SWEEP_modalities.md:206`). I have not upgraded any of
   them.
4. **FDA primary sources were partly unreachable.** Drugs@FDA returned "Unexpected error" and the Purple
   Book API returned 404. Asparaginase product status is therefore from **DailyMed** (current SPLs, which
   I did read) plus secondary sources. **Erwinaze's US withdrawal is PARTLY VERIFIED only** — an
   "Erwinase" (Porton Biopharma) SPL still appears in DailyMed, which is not the same as current US
   marketing.
5. **Whether asparaginase appears on FDA's bulk-drug-substances list under GFI #256 — NOT VERIFIED.**
   This matters, because compounded bulk L-asp is what US veterinary oncology actually uses (PMID
   27086733) and it is **not** covered by 21 CFR 530.
6. **Published canine use of the modern pegylated products (Oncaspar, Asparlas, Rylaze) specifically:
   NOT FOUND.** The canine PEG-asparaginase trials (PMIDs 1522554, 2145933, 3567863) used a 1987-1992-era
   conjugate predating Oncaspar's 1994 approval. Per rule 15 this transfers at the level of **enzyme
   activity (IU)**, as a class-level TRANSFER, not as a product-identical claim.
7. **Canine dose and schedule NOT FOUND for:** carboplatin (in the lymphoma paper's abstract), cisplatin,
   bendamustine, hydroxyurea, bleomycin.
8. **Canine lymphoma efficacy does not exist (or I could not find it) for:** cisplatin, bendamustine,
   vinblastine, etoposide, bleomycin, hydroxyurea. For **hydroxyurea this is partly a search failure** —
   my PubMed queries mis-translated and returned 0 hits; hydroxyurea's canine haematologic-neoplasia use
   remains genuinely under-searched, which I flag rather than claim as absence.
9. **CD25 / IL-2 receptor expression on canine lymphoma cells: NOT FOUND.** This is the gating input for
   denileukin diftitox, the best new conjunction candidate, and is the single highest-value next search.
10. **Omacetaxine (Synribo)** has zero hits in the record and was not evaluated anywhere; it shares the
    protein-synthesis mechanism of the Tier-1 candidates but its DLT is myelosuppression, so it fails (c).
    Flagged as unassessed rather than excluded.
11. **Canine incidence figures for the secondary axes are missing** for: mitoxantrone cardiac,
    chlorambucil marrow, dacarbazine in dogs beyond the "thrombocytopenia dose-limiting" statement,
    bleomycin pulmonary, cisplatin renal *in lymphoma-bearing dogs*.
