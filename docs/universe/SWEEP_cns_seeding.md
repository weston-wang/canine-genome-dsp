# SWEEP: the CNS seeding fraction at diagnosis — replacing `LYMPHOMA_CNS_SEED_FRACTION = 0.05`

2026-11-16. Task: the one item `lymphoma_standard_audit.failing()` returns. `lymphoma_scenarios.py:250` and
`core/lymphoma_grounded.py:377` carry `0.05` with the source-line comment "illustrative fraction of
pre-treatment burden seeding the CNS". It feeds `lymphoma_grounded.evaluate(..., cns_fraction=)` into every CNS
horizon and so sets every brain dose count in `LYMPHOMA_UNIVERSE.md` §J–M.6 (0.05 → 18 doses + implanted CSF
port; 0.0001 → 7 doses, within ordinary percutaneous practice: 112 dogs, PMID 25041580).

**Success criteria quoted (CLAUDE.md rule 2).** "make sure every mechanism and every escape is closed by either
real data or rigorous model"; "I'm not asking if it's been demonstrated, I know it's not."; "I'm okay with no
specific data but if scientifically sound" — so a written, directional transfer graded TRANSFERRED or DERIVED
closes this; absence of a canine measurement does not reopen it (rule 11). "Do not tune any input to force a
closure" — the bracket below is derived before its dose consequence is looked at, and the conservative ceiling
is kept.

All literature below retrieved via PubMed and web search; DOI links given per source.

---

## 0. Record check first (rule 1), including the `30% CNS involvement` question

| item | status |
|---|---|
| **Where "30% CNS involvement" at `LYMPHOMA_DURABLE_RESPONSE.md:242` came from** | **ALREADY IN RECORD, and UNSOURCED.** It is `lymphoma_scenarios.LYMPHOMA_CNS_INVOLVEMENT_PROB_SWEEP = [0.0, 0.15, 0.30]` (`lymphoma_scenarios.py:249`). The dictionary immediately above it states its own grade: `"involvement_note": "... the involvement probability is swept, not asserted."` (`lymphoma_scenarios.py:239-241`). So the 30% is a sweep endpoint, **not a literature figure**, and it is a *different quantity* from the seeding fraction (share of dogs, not share of burden). It coincidentally lands near the "nearly 30%" in a canine review (§1) but that review's 30% has a different denominator again (intracranial tumours, not lymphoma patients) — the agreement is accidental. |
| PMID 6547126 (Couto 1984, 8 dogs, IT cytarabine + craniospinal RT in 4) | ALREADY IN RECORD — `LYMPHOMA_UNIVERSE.md` §M.8, `SWEEP_rt2.md`, `SWEEP_it_longcourse.md` |
| PMID 27511313 (Sisó, Vet Pathol 2017, 37 necropsied dogs) | **Paper ALREADY IN RECORD** (`SWEEP_regional.md:113,226`, `SWEEP_brain_access.md:36`, `LYMPHOMA_UNIVERSE.md:157`) **but only for its ANATOMY finding** (meningeal/perivascular/periventricular DLBCL pattern; CSF >64 cells/µL). **Its prevalence sentence — 4% primary / 5–12% secondary of all canine NHL — is NEW to the record** and is the single most relevant canine number for this task. |
| PMID 22210944 (3 dogs, CNS relapse during chemotherapy) | ALREADY IN RECORD — `SWEEP_regional.md:231`, `SWEEP_exists.md:107`, `SWEEP_cnsregimens.md:8`, cited in `core/lymphoma_grounded.py` |
| PMID 33769594 (choroid plexus, 5 dogs, 4/5 CSF diagnostic) | ALREADY IN RECORD — `SWEEP_regional.md:114,229`, `SWEEP_exists.md:109` |
| PMID 36899719 (Fonti 2023, 45 canine nervous-system lymphomas) | ALREADY IN RECORD — `SWEEP_exists.md:108`, `SWEEP_cnsregimens.md:208`, `SWEEP_brain_access.md:36` |
| PMID 30022475 (LaRue, CNS lymphoma 18 dogs, MST 171 d) | ALREADY IN RECORD — `LYMPHOMA_UNIVERSE.md:417`, `SWEEP_brain_access.md:36` |
| PMID 31769013 (CEOP + cytarabine CRI, n=26 with BM or CNS involvement) | ALREADY IN RECORD — `LYMPHOMA_PRIOR_ART_TREATMENTS.md:113`, `SWEEP_exists.md:41` |
| PMID 40526210 (11 major complications in 7,545 canine CSF collections, 0.15%) | ALREADY IN RECORD — `SWEEP_regional.md:233`. Used here for the cost of a *diagnostic* tap (§5) |
| PMIDs 31657981, 19694717 (TT16 / paediatric ALL: 13–27 IT doses, no cranial RT, CNS relapse 1.5%; T-phenotype HR 5.15) | ALREADY IN RECORD — `LYMPHOMA_UNIVERSE.md:417,497,524`. The T-lineage anchor; reused here, not re-presented as new |
| PMID 18466167 (CEPSAF canine anaesthetic mortality 0.05% / 1.33%) | ALREADY IN RECORD — §M.6 |
| PMID 38497149 (human HD-MTX CNS prophylaxis RR 0.54, no survival benefit, GRADE low) | ALREADY IN RECORD — §M.8 |
| PMID 40400509 (CAR-T alone, 59% CNS relapse by 24 months) | ALREADY IN RECORD — `LYMPHOMA_UNIVERSE.md:191` |
| "no canine occult-CNS-seeding measurement exists" | ALREADY IN RECORD as the open item — `LYMPHOMA_STATUS.md:387`, `LYMPHOMA_UNIVERSE.md:664-673`, `LYMPHOMA_PRIOR_ART_ESCAPES.md:572-578` |
| **NEW** | PMID 16734106; PMID 34101197; PMID 27382100 (CNS-IPI); PMID 15358629 (Hegde); PMID 24727817 (Wilson); doi 10.1111/j.1939-1676.2007.0002.x (Snyder 2008); doi 10.1292/jvms.19-0486 (Kishimoto 2020); doi 10.3389/fonc.2022.874462 (Czech PTCL registry); doi 10.1055/s-0042-1743507 (lymphoblastic lymphoma); CSU Clinical Hematopathology Laboratory prices and CSF PARR cell-number requirement |

---

## (a) Canine evidence table

| what it gives | source | n / method | number | which quantity |
|---|---|---|---|---|
| **Nervous-system involvement as a share of all canine NHL** | Sisó et al., *Vet Pathol* 2017;54:53-60. PMID 27511313, [doi 10.1177/0300985816658101](https://doi.org/10.1177/0300985816658101) | abstract's opening literature statement, in a paper whose own cohort is 37 dogs with neural lymphoma at necropsy (36/37 = 97.3% secondary, 1/37 = 2.7% primary; T 16, B 21) | **primary 4%; secondary 5–12%** | **fraction of DOGS** (eventual, necropsy-era). Not a burden fraction. Note: these are literature figures the authors cite, not their own denominator — their 37 dogs are a selected neural-lymphoma series, so the 5–12% cannot be recomputed from this paper |
| CSF cell count that tracks real infiltration | same, PMID 27511313 | 37 dogs, CSF vs histology | **>64 cells/µL** correlated with marked meningeal + periventricular infiltration | assay threshold; see §5 |
| Primary CNS lymphoma among canine primary brain tumours | Snyder et al., *J Vet Intern Med* 2006;20:669-75. PMID 16734106, [doi 10.1892/0891-6640(2006)20[669:cipnc]2.0.co;2](https://doi.org/10.1892/0891-6640(2006)20[669:cipnc]2.0.co;2) | 173 primary intracranial tumours, postmortem | **7/173 (4%) primary CNS lymphoma** | fraction of BRAIN TUMOURS. Wrong denominator for this task; included because the canine reviews' "4%" traces here |
| The canine review figures "up to 12%" and "nearly 30%" | Fonti et al., *Animals* 2023;13:862. PMID 36899719, [doi 10.3390/ani13050862](https://doi.org/10.3390/ani13050862) (full text read) | review sentence: "Lymphoma within the CNS develops most commonly as part of a multicentric process in both species with a reported prevalence up to 12% [3] or even nearly 30% [4] in dogs" | 12% → Snyder 2008, *secondary intracranial neoplasia*, 177 cases, [doi 10.1111/j.1939-1676.2007.0002.x](https://doi.org/10.1111/j.1939-1676.2007.0002.x); 30% → Kishimoto 2020, *retrospective survey of canine intracranial tumours 2007-2017*, [doi 10.1292/jvms.19-0486](https://doi.org/10.1292/jvms.19-0486) | **both denominators are INTRACRANIAL TUMOURS, not lymphoma patients.** The review's wording invites reading them as lymphoma-patient prevalences; they are not. **Do not use either as the involvement rate.** Their own 45 dogs: 24/45 (53.3%) primary, 21/45 (46.7%) multicentric — a referral neuropathology series, not a staging cohort |
| **CSF cytology / flow / PARR positivity in dogs STAGED for multicentric lymphoma with no neurological signs** | — | — | **NOT FOUND. No such study exists in any search run here.** Every canine CSF-lymphoma dataset found is a cohort selected *by* neurological signs or by necropsy neural involvement | the quantity the task asked for first is unmeasured in the dog |
| **Canine CNS relapse rate after CHOP, with site of relapse** | — | — | **NOT FOUND as a rate.** `SWEEP_cnsregimens.md:208` already records "no PubMed series of dogs with CNS lymphoma treated ... with survival numbers". The only canine CNS-relapse reports are case-level: 3 dogs during chemotherapy (PMID 22210944); 1 spermatic-cord B-cell relapsing to brain at 5 months (PMID 37265807, in record). Large canine series (L-CHOP ± half-body RT, first-rescue cohorts) report overall relapse but **do not break out CNS** | the operational proxy is unmeasured in the dog |
| Canine CSF cytology is a weak instrument even when disease is suspected | Danciu et al., *Vet Rec* 2021;189:e557. PMID 34101197, [doi 10.1002/vetr.557](https://doi.org/10.1002/vetr.557) | 102 dogs, central vs peripheral vestibular disease | raised CSF TNCC: **sensitivity 49%**, specificity 90%; raised protein: sensitivity 58%, specificity 39% | assay performance (not lymphoma-specific) |
| Diagnostic tap risk in dogs | PMID 40526210, [doi 10.1111/jvim.70165](https://doi.org/10.1111/jvim.70165) (ALREADY IN RECORD) | 7,545 CSF collections | **11 major complications (0.15%)**, 8 of 11 euthanised | cost of making the brain arm selective (§5) |

**Canine bottom line.** The only canine number with the right denominator is **5–12% of dogs** with secondary
nervous-system involvement (PMID 27511313), and it is an eventual/necropsy figure, not an at-diagnosis one.
There is **no canine measurement of occult CNS disease at diagnosis and no canine CNS-relapse rate.** That
matches what the record already said; this sweep confirms it by search rather than assuming it.

---

## (b) Human anchor table

| anchor | source | n / method | number |
|---|---|---|---|
| **CNS-IPI: CNS relapse without CNS-directed prophylaxis, by risk group** | Schmitz et al., *J Clin Oncol* 2016;34:3150-6. PMID 27382100, [doi 10.1200/JCO.2015.65.6520](https://doi.org/10.1200/JCO.2015.65.6520) | DSHNHL derivation cohort, R-CHOP-treated DLBCL | **2-year CNS disease: low risk 0.6% (46% of patients), intermediate 3.4% (41%), high 10.2% (12%)**. BC Cancer validation: 0.8% (CI 0.0-1.6), 3.9% (2.3-5.5), 12.0% (7.9-16.1). Score = 5 IPI factors + kidney/adrenal involvement; low 0-1, intermediate 2-3, high 4-6 |
| **Occult CSF positivity at diagnosis, flow cytometry vs cytology** | Hegde et al., *Blood* 2005;105:496-502. PMID 15358629 | 51 newly diagnosed aggressive B-cell lymphomas at CNS risk, no neurological signs | **11/51 (22%) occult CSF involvement; 11/11 by flow cytometry, 1/11 by cytology.** Flow detected clones down to **0.2% of total CSF lymphocytes** |
| **Occult CSF positivity and its link to CNS relapse** | Wilson et al., *Haematologica* 2014;99:1228-35. PMID 24727817, [doi 10.3324/haematol.2013.101741](https://doi.org/10.3324/haematol.2013.101741) | 326 untreated patients with pre-treatment CSF (246 DLBCL, 80 Burkitt), flow + cytology | DLBCL: flow-positive **42/246 (17%)** total, of which **flow-only (occult) 33 (13%)**; cytology 11 (4.5%). Burkitt: occult 9/80 (11%), cytology 5 (6%). **Occult-positive DLBCL: 3-year freedom from CNS relapse 73% vs 94% (p<0.0001)**; 3-year OS 38% vs 69% (p=0.0001) |
| Yield of universal CSF flow screening | Ho et al. (8-colour CSF flow, 361 patients screened; retrieved via web, **primary source not fetched — UNVERIFIED**) | 361 DLBCL/HGBCL | "low proportion of positive results, mostly in the setting of overt CNS disease"; **only 4 patients flow-positive without other evidence of CNS spread** |
| **Peripheral T-cell lymphoma CNS rates** | Czech Lymphoma Study Group registry, *Front Oncol* 2022;12:874462. [doi 10.3389/fonc.2022.874462](https://doi.org/10.3389/fonc.2022.874462), PMC9133472 | 1,040 PTCL patients | **29/1,040 (2.79%) with any CNS involvement; 16/1,040 (1.54%) CNS relapse.** A CNS-PINK-style score gave 2-year CNS relapse **4.1% low risk vs 22.8% high risk** (score derived for NK/T, applied here — indirect) |
| PTCL without prophylaxis, single institution | Korean series, PMC5376067 (**PMID not retrieved**) | 228 PTCL, no CNS prophylaxis | **CNS relapse 8.7%** |
| PTCL pooled range | review cited in the above (**secondary citation**) | — | CNS relapse **2.1–8.8%** across PTCL subtypes |
| Prophylaxis effect in PTCL | same sources (secondary) | — | IT MTX prophylaxis **not** associated with reduced CNS recurrence in PTCL; it *is* for high-risk ENKTCL with MTX ≥2 g/m² inside SMILE |
| **Lymphoblastic lymphoma (the closest human analogue of the canine T-cell arm)** | *Indian J Med Paediatr Oncol* 2022;43:177-84. [doi 10.1055/s-0042-1743507](https://doi.org/10.1055/s-0042-1743507) | retrospective, paediatric + adult T-LBL | **CNS involved at diagnosis in 2–7%**; **"CNS relapse can be seen in up to one-third of LBL patients if CNS prophylaxis treatment is not delivered"**; with prophylactic cranial irradiation, CNS failure **3/48 (6.25%)** |
| T-lineage anchor already in the record | PMIDs 31657981, 19694717 (ALREADY IN RECORD) | TT16, 598 children, 13-27 IT doses, no cranial RT | CNS relapse **1.5%**; T-phenotype the only independent CNS-relapse factor, **HR 5.15**; 1 of 21 CSF-positive patients relapsed in the CNS |

**Human bottom line.** Two independent facts matter for the conversion. (1) **Occult CSF-detectable disease at
diagnosis is 2–5× more common than CNS relapse** (13–22% positive vs 0.6–10.2% relapsing) — so most occult
seeding is cleared by systemic therapy, and the seeded compartment is small enough that systemic drug plus
immune clearance suffices in the majority. (2) **Occult positivity is not a clean switch**: 6% of
flow-*negative* DLBCL still relapsed in the CNS (Wilson, 94% 3-year freedom), so a negative CSF test does not
mean an unseeded CNS.

---

## (c) Conversion to "fraction of total burden in the CNS at diagnosis"

### Why the literature cannot be read off directly
Every source above gives one of two things: **P(a patient/dog has CNS disease)** or **P(a patient/dog relapses
in the CNS)**. The model needs **E[CNS cells] / E[total cells] at day 0** (`lymphoma_grounded.evaluate` multiplies
`burden` by `cns_fraction` to get the compartment's starting cell count; `burden = BURDEN_EARLY_DETECTED = 1e8`,
`core/lymphoma_catalogue.py:341`). **No paper in any species reports a CNS-to-total tumour-cell ratio.** So the
conversion must be derived. Two independent derivations follow; they are then reconciled.

### Route 1 — Poisson inversion of the CNS-relapse rate
A CNS relapse requires **at least one clonogenic cell seeded in the CNS at diagnosis that survives the systemic
regimen.** If surviving CNS clonogens are Poisson with mean μ, then

    P(CNS relapse) = 1 − exp(−μ)    ⇒    μ = −ln(1 − P)

Inputs for P: canine 5–12% (PMID 27511313, eventual nervous-system involvement) bracketed with the
stage-matched human CNS-IPI intermediate-to-high 3.4–10.2% (PMID 27382100). Canine multicentric lymphoma is
predominantly stage III–V with raised LDH, so the canine cohort maps to CNS-IPI intermediate/high, not low.
Take **P = 0.03 to 0.12 ⇒ μ = 0.030 to 0.128 surviving clonogens per dog.**

Then μ = n₀ · S, where n₀ is clonogens present in the CNS at diagnosis and S is per-cell survival through the
systemic regimen *inside the CNS*. S is bracketed by the model's own sanctuary penetration sweep,
`LYMPHOMA_CNS_SANCTUARY["penetration_multiplier_sweep"] = [1.0, 0.3, 0.15, 0.05]` (`lymphoma_scenarios.py:236`):
at 5–30% of systemic exposure, CHOP's 4–5 body logs collapse to very little, so **S = 10⁻¹ (near-sanctuary) to
10⁻³ (partial penetration)**.

| S | n₀ = μ/S | f = n₀ / 10⁸ |
|---|---|---|
| 10⁻¹ | 0.30 – 1.28 cells | 3.0×10⁻⁹ – 1.3×10⁻⁸ |
| 10⁻² | 3.0 – 12.8 cells | 3.0×10⁻⁸ – 1.3×10⁻⁷ |
| 10⁻³ | 30 – 128 cells | 3.0×10⁻⁷ – 1.3×10⁻⁶ |

**Route 1 ⇒ f = 3×10⁻⁹ to 1.3×10⁻⁶.** Direction of the residual error, stated: canine P is *censored* — dogs
die of systemic disease at a median of roughly a year, so CNS relapses that would have occurred later are never
observed. Censoring pushes P down, so **Route 1 is a FLOOR**, not a central value.

### Route 2 — occult CSF positivity converted by cell counts
Hegde's flow cytometry detected clones at **0.2% of total CSF lymphocytes** (PMID 15358629). Human CSF volume
≈150 mL and normal CSF WBC ≤5/µL (**textbook values; NOT retrieved from a cited source in this sweep —
UNVERIFIED**) give ≤7.5×10⁵ CSF lymphocytes, so the smallest detected occult clone is **≈1.5×10³ cells in the
CSF**. Human DLBCL burden at diagnosis is of order 10¹¹–10¹² cells (the model's own
`BURDEN_CLINICALLY_OBVIOUS = 1e11` is the same order). So

    f_CSF  ≈  1.5×10³ / 10¹¹  ≈  1.5×10⁻⁸   (10⁻⁹ at 10¹² burden)

But CSF-borne cells are only part of the CNS compartment the model must clear. Let **φ = (free-floating CSF
tumour cells) / (all CNS tumour cells)**. Then f_CNS = f_CSF / φ. **φ has never been measured in any species**
— this is the same unmeasured "fluid-to-cell fraction" the HSA branch hit (CLAUDE.md failure 7). Canine neural
lymphoma is meningeal, perivascular and periventricular (PMID 27511313), i.e. CSF-facing, which argues φ is not
vanishingly small; taking **φ = 10⁻² to 10⁻³** gives

**Route 2 ⇒ f = 1.5×10⁻⁶ to 1.5×10⁻⁵.** φ is the single weakest link in this document: **one decade of error in
φ is one decade of error in f.**

### Route 3 — the overt-involvement branch (what 0.05 would actually mean)
A dog with overt CNS lymphoma has a meningeal or parenchymal lesion. At the standard 10⁹ cells/cm³, a 1 cm³
lesion is 10⁹ cells. Against the clinically obvious burden of 10¹¹ that is **f ≈ 10⁻²**. Note the incoherence:
against the model's early-detection burden of 10⁸, a 1 cm³ CNS lesion gives f > 1 — **overt CNS involvement is
logically incompatible with the early-detection premise the whole project assumes**. If the brain arm were
applied to an *unscreened* cohort, the population mean would be
P(overt) × 10⁻² = (0.05 … 0.12) × 10⁻² = **5×10⁻⁴ to 1.2×10⁻³.**

### The bracket

| branch | f | reasoning | grade |
|---|---|---|---|
| **LOW** | **3×10⁻⁹** | Route 1 at S = 10⁻¹ and P = 0.03: the CNS is essentially a sanctuary, so one surviving cell per 33 dogs implies well under one seeded cell per dog | DERIVED (floor; censoring-biased) |
| **CENTRAL** | **1×10⁻⁶** (≈ 100 CNS cells at a 10⁸ burden) | the point where Route 1's upper end (1.3×10⁻⁶, S = 10⁻³) and Route 2's lower end (1.5×10⁻⁶, φ = 10⁻²) converge from opposite directions and on different data (canine involvement rates vs human occult CSF cell counts) | **DERIVED**, on TRANSFERRED human inputs (PMIDs 27382100, 15358629, 24727817) and one ASSUMED factor (φ) |
| **HIGH** | **1.2×10⁻³** | Route 3 population mixture: the brain arm applied to a cohort that was never screened for overt CNS disease, 12% of whom carry a ~1 cm³ lesion | DERIVED on a TRANSFERRED cell-density constant |

**Overall grade: TRANSFERRED/DERIVED — not MEASURED.** The canine quantity does not exist (§a). What stands
behind the bracket is a written inversion of canine involvement rates and human CNS-IPI relapse rates through
the model's own kill structure, plus a human occult-CSF cell-count conversion. Under the stated bar
("real data **or a rigorous model**", cross-species transfer acceptable when justified in writing) this
**closes** the item; it does not make it measured. One input, φ, remains ASSUMED and is named as such.

---

## (d) Where the current 0.05 sits

**ABOVE the bracket — by ~40× above the HIGH branch and ~5×10⁴ above the CENTRAL.** `0.05` is not a conservative
version of the right quantity; it is **Route 3's within-dog overt value (10⁻²) multiplied by five**, i.e. it
describes a dog with more than a cubic centimetre of CNS lymphoma while the whole-body burden is only 10⁸ cells.
That combination does not occur: it is arithmetically inconsistent with the early-detection premise.

Consequence, read off the record's own sensitivity table (`LYMPHOMA_UNIVERSE.md` §M.7):

| f | B-cell brain doses | T-cell brain doses | device | where this f sits |
|---|---|---|---|---|
| 0.05 (current literal) | 18 | 16 | implanted port | **outside the bracket (far above)** |
| 0.01 | 14 | 14 | port | outside the bracket (above) |
| 0.001 | 10 | 10 | borderline | ≈ **HIGH** branch |
| 0.0001 | 7 | 7 | percutaneous cisternal puncture, ordinary canine practice (PMID 25041580) | between CENTRAL and HIGH |

So **the 18-dose / implanted-port requirement is driven entirely by a value outside the defensible bracket.**
At the HIGH branch the brain arm needs ~10 doses (borderline for a port); at the CENTRAL branch ≤7, which
ordinary percutaneous practice covers.

Three cautions, so this is not read as a closure that was tuned into existence:

1. **The record's table stops at 10⁻⁴.** The dose count at the CENTRAL branch (10⁻⁶) has **not been computed**.
   It is **≤7** but the table does not resolve it, and it will not fall indefinitely: each injection delivers a
   fixed log-kill but the schedule also has to span the dosing window, so there is a floor set by duty, not by
   cell count. The code path to run is `lymphoma_grounded.evaluate(..., compartment=CNS, cns_fraction=1e-6,
   clock=True)` and `cns_capacity()`, whose own bracket is already log10 −8 to 0
   (`core/lymphoma_grounded.py:682`) — the model can express this range; it was never asked to.
2. **The conservative ceiling should be kept as a reported branch, not deleted.** Every dose count quoted in
   §J–M.6 was computed at 0.05 and is a valid *upper* bound. The honest restatement is "18 doses at the
   retained ceiling, ~10 at the high branch, ≤7 at the central branch", not "7 doses".
3. **The direction of the correction is now known, which it was not before.** `LYMPHOMA_UNIVERSE.md:675`
   says "The direction of the error is unknown, because the literal could be too high or too low." It is
   **too high**, by three to five orders of magnitude.

---

## (e) Could a diagnostic test make the brain arm selective?

**Yes in one direction only, and the limiting number is an assay floor, not a biology.**

**What is available and what it costs.** Colorado State University's Clinical Hematopathology Laboratory runs
both assays on CSF: **flow cytometry $165**, **PARR $165**, **add-on PARR to flow (or a simultaneous second
sample) $90**, Ki67 $120, cell block $140, non-viable flow accession fee $22.60
([CSU CHL prices](https://vetmedbiosci.colostate.edu/chl/prices/), read 2026-11-16). The CSU research test list
prices **CSF Analysis & Cytology at $59.36** and CSF protein at $29.00
([CSU research test list](https://www.research.colostate.edu/epf/wp-content/uploads/sites/15/2025/12/Clinical-Pathology-Research-Test-List.pdf);
labelled research pricing, so clinical price unconfirmed). Add a cisternal or lumbar puncture under general
anaesthesia: canine anaesthetic/sedation mortality 0.05% (ASA 1-2) to 1.33% (ASA 3-5) in 98,036 dogs
(PMID 18466167, ALREADY IN RECORD) plus 0.15% major complications per CSF collection in 7,545 taps, 8 of 11
fatal (PMID 40526210, ALREADY IN RECORD). So the test is **available at referral centres today for roughly
$200-250 plus one anaesthetic**, at a combined procedural risk of order 0.2-1.5%.

**Why it cannot rule the brain arm out.** CSU states the sample requirement plainly:
**"For the sample to be diagnostic we estimate you need 50,000 lymphoid cells"**, with the worked example
**"if the CSF has a lymphocyte count of 100/ul, we need at least 500 ul of fluid"**
([CSU sample collection instructions](https://vetmedbiosci.colostate.edu/chl/sample-collection-and-submission-instructions/),
read 2026-11-16; the 5×10⁴ figure is stated for PARR). A dog with a normal CSF (TNCC ≤5/µL) yields only about
**2.5×10³ cells in 500 µL — roughly 20× below the stated requirement.** The assay floor is therefore ~5×10⁴
cells, while the CENTRAL branch of the bracket is **~10² cells**. **A canine CSF clonality assay is about 500×
too insensitive to see the compartment the model actually has to clear.** Cytology is worse: Sisó's threshold
for marked meningeal/periventricular infiltration is >64 cells/µL (PMID 27511313), i.e. a frank pleocytosis, and
canine CSF TNCC had only 49% sensitivity for central disease in 102 dogs (PMID 34101197).

**So the selective design that the evidence supports:**

| test result | what it establishes | brain arm |
|---|---|---|
| CSF pleocytosis with clonal cells (or a lesion on MRI) | f at or above the HIGH branch — overt disease | **full arm: ~10-18 doses, implanted port.** These dogs are also outside the early-detection premise and should be scored separately |
| CSF normal, PARR/flow uninformative for want of cells | **nothing.** The test is blind below ~5×10⁴ cells | **cannot be omitted.** Human corroboration: 6% of flow-NEGATIVE DLBCL still relapsed in the CNS (3-year freedom 94%, PMID 24727817) |

**The route that does not need a tap, and is untried in dogs.** CNS-IPI stratifies on routine staging alone —
age, stage, LDH, performance status, extranodal sites, plus kidney/adrenal involvement — and separates 0.6% from
10.2% two-year CNS risk (PMID 27382100). A **canine CNS-IPI has never been built or validated** (NEW gap; no
canine series reports site of relapse, §a, so the outcome column to fit it against does not exist). That is the
cheap, zero-risk selectivity lever, and it is a data-collection task, not a modelling one: it needs one canine
cohort with staging covariates and site-of-relapse recorded.

**Two measurements would settle this item**, in priority order:
1. **CSF flow cytometry / PARR at diagnosis in dogs staged for multicentric lymphoma with no neurological
   signs** (n ≈ 50-100), reporting the fraction positive *and* the absolute clonal cell count. This is the
   canine analogue of Hegde and Wilson, it is doable with assays that already exist and are priced above, and it
   would replace Route 2's transfer and pin down φ.
2. **Site of relapse recorded in any large canine CHOP series.** That single column converts Route 1 from a
   human-anchored transfer into a canine measurement.

---

## What this sweep could not verify

- **Canine total CSF volume (mL/kg) and canine CSF production rate**: no reference value retrieved. The
  cell-count arithmetic in §5 therefore uses the *sample* volume CSU specifies (500 µL), not a whole-compartment
  volume, which avoids the gap.
- **Human CSF volume (~150 mL) and normal CSF WBC (≤5/µL)**: textbook values, not retrieved from a citable
  source here. Route 2 depends on them; a factor-of-two error in either moves f by a factor of two (not a
  decade).
- **φ, the CSF-fluid-to-CNS-tissue tumour-cell fraction**: unmeasured in every species. Named as the ASSUMED
  step; it is the dominant uncertainty in the CENTRAL branch.
- **Benevolo et al. (CSF flow cytometry in high-risk NHL, multicentre)**: the paper exists but its positivity
  figure was not retrieved and no PMID/DOI was confirmed. Not used.
- **Ho et al. 8-colour CSF flow in 361 patients**: web-sourced only, primary source not fetched. Marked
  UNVERIFIED and not load-bearing.
- **PMIDs for the Czech PTCL registry (PMC9133472) and the Korean PTCL series (PMC5376067)**: cited by DOI and
  PMC ID; PMIDs not retrieved.
- **CSU clinical (as opposed to research) price for CSF analysis and cytology**: the $59.36 figure is from the
  research test list.

## Suggested follow-up in code (not applied here — this sweep edits no other file)

- Replace the bare literal with a named bracket and its grade, e.g.
  `CNS_SEED_FRACTION_BRACKET = {"low": 3e-9, "central": 1e-6, "high": 1.2e-3}` plus
  `CNS_SEED_FRACTION_CEILING = 0.05` retained as the conservative reported branch, each with its derivation
  string, in `core/lymphoma_grounded.py` and `lymphoma_scenarios.py`.
- Re-run the §M.7 dose table at 1e-6 and 1.2e-3 via
  `evaluate(..., compartment=CNS, cns_fraction=..., clock=True)` so the CENTRAL branch's dose count exists.
- Re-grade `lymphoma_standard_audit.cns_seeding_item()` from the item `failing()` returns to **TRANSFERRED /
  DERIVED**, with this file as its stored reason, and move it into `wrongly_reported_as_gaps()` so it cannot be
  re-raised as "no canine measurement exists" (rule 11).
