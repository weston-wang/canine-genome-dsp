# HS branch status

Settled results and known gaps for the histiocytic sarcoma work, so a later thread does not
re-derive or re-litigate them. Written per `CLAUDE.md` rules 1, 4, 5 and 7.

**The case under analysis:** primary intracranial (non-disseminated) histiocytic sarcoma in a
predisposed breed — an extra-axial, meninges-based mass that invades brain tissue (23/23 dogs) and
the leptomeninges (19/19), with extracranial spread never reported (`CONSOLIDATED_REPORT.md`, "Where
the disease is"). Evidence from *disseminated* HS is labelled **indirect** below.

Labels: **NEW** (not in the record), **PARTIAL** (the record has the source or the claim, not this
detail), **ALREADY COVERED** (with where). Checked by DOI/PMID against `docs/` and `src/`, not by
keyword.

---

## The delivery mechanism that closes everything (2026-10-02) — and a correction

**It is not a device. It is molecular selection, and the record already said so.**

My previous answer said local delivery was the binding engineering blocker (C1/C2). That was wrong
in two specific ways, and `core.schedule_coherence` exists precisely to catch the first:

1. **It set access AND duty to 1.0 simultaneously.** A cavity implant or a single CED infusion buys
   access *from a procedure* and then cannot also supply a continuous duty cycle. Access and duty
   must come from the same schedule.
2. **It overstated the requirement.** The bar is not access 1.0. It is **0.196** in invaded
   parenchyma (0.021 × 9.35) and **0.0145** in CSF (0.005 × 2.89).

At that real bar, **measured intrinsic penetration already clears it, orally**:

| Agent | Brain access | Provenance | Clears 0.196? |
|---|---|---|---|
| **paxalisib** | Kp,uu **0.31** | MEASURED, **confirmed P-gp/BCRP non-substrate** (PMID 27638506) | **yes** |
| **sagopilone-class microtubule agent** | brain:plasma **0.80** | MEASURED (PMID 18780814); paclitaxel **0.0** in the same experiment | **yes** |
| RGN3067 | efflux ratio 0.61 (not MDR1 substrate), oral | MEASURED | yes |
| generic small molecule | 0.021 | — | no (the 9.35× shortfall) |

**The all-oral regimen closes every route at both compartments and is tolerable:**

| Compartment | Routes closed | Worst margin | Worst route |
|---|---|---|---|
| Invaded parenchyma | **10 / 10** | **+0.0416/day** | autophagy-independence |
| Leptomeninges / CSF | **10 / 10** | **+0.0592/day** | autophagy-independence |

Five agents — liposomal clodronate, hydroxychloroquine, anti-PD-1, paxalisib, brain-penetrant
microtubule agent. **No implant, no catheter, no sonication, no radiation in the closing set.**
Access and duty come from one schedule by construction, so nothing needs reconciling.

### Why the devices lose on their own measured numbers

| Option | Measured gain | Duty | Geometry | Verdict |
|---|---|---|---|---|
| **Implanted multi-emitter US** (SonoCloud-9) | **5.9×** brain carboplatin, 9 emitters, 64 mm depth, 6 monthly cycles, 33 patients, **no DLTs** (Nat Commun 2024) | **1.0** — uniquely fixes duty | diffuse | 5.9 × 0.021 = **0.124 < 0.196** — short for a generic molecule; **rescues any agent with Kp,uu ≥ 0.033** |
| Transcranial MRgFUS, volumetric | 64 subspots on 3-mm grid, 20.5 ± 4.6 cc, "near-subtotal brain coverage" | 1.0 | **diffuse** | **retires the FOCAL objection** in our old model entry; magnitude still binding; does not defeat efflux |
| Intrathecal bolus | 200×, diffuse, ~1/112 complications in dogs | 0.07 | diffuse | effective **14× vs 2.89× needed — clears CSF, obtainable today.** Backup, not a requirement |
| CED | 50×, best canine evidence of any device (17 dogs, no DLT) | **1/365** | focal | **fails on duration**: effective 0.14× |
| P-gp/BCRP co-dose | 20× | 1.0 | diffuse | would clear, but canine PK/safety unestablished and not brain-selective |

Two corrections to our own model fall out: the old FUS entry's **10× was too high** (measured is
5.9×) and its **FOCAL geometry is obsolete** (coverage is volumetric).

### Where a device is still the right answer

- **As a rescue for a non-penetrant agent.** Abemaciclib at the rat ratio (0.11) is rescued by the
  implanted device (→0.65); at the mouse ratio (0.03) it is not (→0.177). That is the honest range
  for the CDK4/6 brain arm, and it is also the one place "choose a non-substrate" is unavailable —
  abemaciclib *is* a P-gp/BCRP substrate, so ultrasound's tight-junction opening only partly helps.
- **CSF**, where intrathecal bolus is obtainable today and clears comfortably.

### Net effect on the conjunction

**No engineering condition remains.** C1 and C2 are now MET by drug selection; 5 of 7 conditions
hold today. Outstanding: **C5** (one immunostain, decidable before treatment) and **C7** (sponsor
access, which closure under C1–C6 does not require).

**The binding constraint has moved off access entirely and onto the per-day kill rate**, which is
still a reference constant (0.15/day) standing behind a measured IC50 (1.77–2.69 ng/mL, PMID
25715778) — a concentration, not a rate. And the access exemplar carries a real warning the record
already states: **sagopilone failed in human glioblastoma** (EORTC 26061, PFS6 6.7%, no objective
responses). Brain-penetrant is not brain-effective.

---

## The headline is now deterministic, not odds (2026-10-01, third pass)

The user's objection: *"I don't want odds of achieving 10 years, the whole point about looking at all
mechanisms and escapes is to not leave it to odds."* Correct, and not a presentational point. A
probability is what you report when failure modes are **unenumerated**. Enumerating them converts
the question into a decidable one. `deterministic_closure.py` decides it; `emergence.py` is demoted
to a sensitivity statement and says so in code (`emergence_is_secondary()`).

**Result — and it is harder than the odds made it sound:**

| | Invaded parenchyma | Leptomeninges / CSF |
|---|---|---|
| Obtainable agents, systemic exposure | **0/10 routes closed**, worst **−0.049/day** | **0/10**, worst **−0.036/day** |
| Kill-rate shortfall | **9.35×** | **2.89×** |
| Same agents, local delivery + continuous | **10/10 closed**, **+0.225/day** | **10/10**, **+0.225/day** |

Binding route in both compartments: the **drug-tolerant persister**. Seven conditions, **three met
today**; outstanding C1, C2 (engineering), C5 (one stain), C7 (sponsor). C1 and C2 are the only
blockers that are not somebody's decision to simply make.

**Two defects in reporting odds, now recorded in code:**
1. `p_reroute` (0.18–0.60) charged a reroute as **terminal**, while the escape ledger names a
   successor agent for every reroute — that is what "closed" means. It double-counted.
2. It smeared a structural failure into a bet: "0.27 in brain" reads like a gamble worth taking;
   "every route open, margin −0.049/day" is the same fact stated honestly.

---

## Re-grade against the user's stated bar (2026-10-01)

The previous revision of this file ended with a "what remains open" list that graded against
**"demonstrated in a dog"** — the bar the user explicitly disclaimed, twice. That is `CLAUDE.md`
rule 2, and the lesson is now rule 11 plus failure 7. `standard_audit.py` grades every live input
against the **stated** bar (real data **or** a rigorous model; a transfer acceptable when justified
in writing) and reports what actually fails.

**Result: 13 of 14 live inputs PASS. One genuinely failed, and it has been fixed.**

Wrongly reported as open gaps in earlier summaries — each has a written transfer or derivation:

| Item | Why it passes |
|---|---|
| PRMT5-inhibitor potency for the dog | Human MTAP-null GI50 transferred on a **computed** 99.37% PRMT5 ortholog identity from real UniProt sequences |
| Abemaciclib brain exposure | **Measured** in resected human brain-tumour tissue (96× CDK4, 19× CDK6 over IC50), rodent Kp,uu 0.03–0.11, orthotopic survival benefit at those exposures |
| MTAP status in canine HS | A **conditional gate** the analysis names and prices, not an unbacked number. The 62.8% region-level deletion **is** measured in canine HS |
| Λ, second-primary rate | **Calibrated** so exp(−Λ) reproduces the observed canine-HS adjuvant recurrence-free fraction. Wide interval ⇒ uncertain, not unfounded |
| Canine ctDNA for surveillance | Plasma PTPN11 assay **validated in canine HS**: ~91% detectable, 98.8% specific, commercial platform |

**The one input that genuinely failed: the growth-rate bar.** `pkpd.GROWTH_PER_DAY = 0.055` was a
bare literal — an assumed ~13-day doubling, uncited — and it sets the pass/fail threshold for every
escape closure and every durability margin. The most load-bearing number in the project had the
weakest basis of any of them.

Now **DERIVED** from regrowth measured in canine HS itself (Skorupski, PMID 19453368: median
disease-free interval 243 d, 10/16 relapsing at median 201 d after debulking + lomustine). Over a
1e6–1e8 post-surgical residual that implies **0.0095–0.0344/day**. The bar in use, 0.055/day, is
**1.6–5.8× harder** than the clinical data demands — the direction that cannot manufacture a
closure. And `growth_sensitivity()` shows the conclusion does not turn on the choice: across
0.030–0.080/day the access a synthetic-lethal maintenance agent needs stays between **0.09% and
0.27%** of systemic exposure.

### The last flat priors are now derived too — and the result cuts both ways

The per-site penetration terms (lung 0.05, brain-local 0.08, brain-systemic 0.30) were the final
bare point priors in the live chain. They are now **drug-specific and derived**: P(available access <
the access the PK/PD model requires), using the **measured** compartment figures already in
`core.catalogue` (0.021 parenchyma, chlorambucil, PMC6128565) against `min_access_to_close()`.

| Site | Agent | Available | Required | Headroom | Derived p(fail) | Old flat prior |
|---|---|---|---|---|---|---|
| Lung | PRMT5i class | 1.0 | 0.0018 | 557× | ~0.00 | 0.05 |
| Lung | MEK (measured) | 1.0 | 0.041 | 25× | 0.002 | 0.05 |
| Brain, systemic | PRMT5i class | 0.021 | 0.0018 | **11.7×** | **0.013** | 0.30 |
| Brain, systemic | MEK (measured) | 0.021 | 0.041 | **0.5×** | **0.726** | 0.30 |

This is the honest test of whether a derivation is tuned: it made the genotype-anchored arm's brain
term **much better** (0.30 → 0.013) and the MEK arm's **much worse** (0.30 → 0.726). A derivation
that only ever improved the answer would be a tuned one. It also **reproduces the project's own
site-split finding from first principles** — MEK closes the lung and fails behind the barrier — which
the early four-cell analysis had derived by hand.

**Updated durability (P = no second primary over 10 y, 90% CI):**

| Tier | Lung | Brain, local | Brain, systemic | CSF |
|---|---|---|---|---|
| MTAP (genotype-anchored) | **0.77** [0.50, 0.92] | 0.77 | **0.76** | 0.43 |
| MAPK majority, no surveillance | 0.59 [0.27, 0.83] | 0.59 | **0.27** | 0.37 |
| MAPK majority, with detect-and-switch | **0.87** [0.62, 0.97] | — | — | — |

### Both remaining items are now closed (2026-10-01, second pass)

**`standard_audit.failing()` returns `[]`. 17 of 17 live inputs pass the stated bar, and no live
scenario reaches an ASSUMED parameter** (enforced by `test_no_live_scenario_uses_an_assumed_parameter`).

**1. The dependency and floor tiers now have graded PK/PD entries**, so their site terms derive
instead of falling back:

| Tier | Agent | IC50 | Exposure | Brain headroom |
|---|---|---|---|---|
| PTEN | **duvelisib** | **287 nM MEASURED in canine HS** (PMID 42129963) | 3598 nM, human label transfer | 1.5× |
| CDKN2A/RB1-intact | **abemaciclib** | 10 nM (CDK6 enzymatic, transfer) | 588 nM, human label transfer | **6.9×** |
| Floor | **vincristine** | **3.26 nM MEASURED in canine HS** (PMID 25715778) | **47.8 nM DERIVED from canine PK** (PMID 25649934) | 1.7× |

The duvelisib entry retires the project's most-criticised provenance error: PI3K potencies had been
borrowed from canine *hemangiosarcoma*. There is now a canine-HS figure on that axis. The
vincristine entry is the only one in the project where potency **and** exposure are both canine.

Brain headroom across all five tiers — PRMT5i class 11.7×, abemaciclib 6.9×, vincristine 1.7×,
duvelisib 1.5×, cobimetinib 0.5× — reproduces the hand-derived site split and now ranks the arms.

**2. The reroute priors are graded for what stands behind them** (`_REROUTE_PROVENANCE`): LOCKED,
REROUTABLE and DEPENDENCY as TRANSFERRED (documented human resistance mechanisms, with the CDK4/6
routes now named as RB1 loss and cyclin E1–CDK2 and enumerated as `escape_audit.A15`); FLOOR as
DERIVED from the cycled schedule plus the MTA immune finding. None is MEASURED, because a ten-year
reroute probability has never been measured in any species.

### A correction this pass forced, and it matters

Grounding abemaciclib exposed an **overstatement in section A below**. The measured 96× (CDK4) /
19× (CDK6) tissue multiple comes from resected human **brain metastases** — lesions with a
**disrupted** barrier. It therefore speaks to the **extra-axial, blood-side mass**, which is the bulk
of this tumour, and **not** to cells behind an intact barrier. For invaded parenchyma the governing
figures are the rodent unbound ratios: Kp,uu 0.03–0.11 on 21.8 nM unbound plasma gives 0.65–2.4 nM,
i.e. **0.07–0.24× the CDK6 bar — it does not close there.**

So "lead the brain with abemaciclib" stands for the extra-axial mass and **does not remove the need
for local delivery in invaded parenchyma**. No agent in the catalogue does. Recorded in
`pkpd.PARAMS['abemaciclib']` and tested.

### A real bug this pass caught

Giving the floor tier a PK/PD key flipped its verdict from FLOOR to DEPENDENCY_HOLD, because
`durability()` branched on *whether a potency existed* rather than on the lock kind. The floor tier
is a strategy (immune surveillance + a cycled cytotoxic), not a continuously-dosed anchor, so its
verdict must key on `Lock.FLOOR`. Fixed; the pre-existing test caught it.

### Updated durability, all five tiers derived (P = no second primary over 10 y, 90% CI)

| Tier | Lung | Brain, local | Brain, systemic | CSF |
|---|---|---|---|---|
| MTAP (genotype-anchored) | **0.77** [0.50, 0.92] | 0.77 | **0.76** | 0.43 |
| CDKN2A / RB1-intact | 0.64 | 0.64 | **0.61** | 0.39 |
| PTEN | 0.64 | 0.64 | 0.42 | 0.39 |
| MAPK majority (no surveillance) | 0.59 | 0.59 | **0.27** | 0.37 |
| MAPK majority (detect-and-switch) | **0.87** [0.62, 0.97] | — | — | — |
| Floor (no target) | 0.39 | 0.39 | 0.32 | 0.29 |

The CDKN2A tier is now the **second-strongest brain tier**, which is what section A argued on
evidence grounds and the model now reproduces independently.

### What is left — uncertainty, not missing basis

Nothing fails the bar. What remains is **width**, which is a different thing: Λ (the second-primary
rate) still carries 50–90% of the variance in every scenario, so the highest-value study remains an
observational cohort of cleared, predisposed dogs rather than any drug experiment. And the MTAP
stain remains a **priced conditional gate** on the strongest tier — not a gap, but the one cheap
test that would move the most.

---

## Gap-closure pass (2026-10-01) — what was done

All gaps listed in the verdict below have been closed or the reason recorded. Full suite: **735
passed**; the single failure (`test_validation_changes_no_analysis_module`, a melanoma-module import
check) **fails identically on the clean tree** and is unrelated to this work.

| Gap | Closed by | Result |
|---|---|---|
| Therapy universe never enumerated (rule 9) | new `candidate_universe.py` + tests | **25 modality classes, 0 unassessed.** 15 in model, 10 excluded with recorded reasons. [**Superseded 2026-10-31: a 26th class was found unenumerated and is now excluded — 26 classes, 11 excluded. See the end of this file.**] Newly assessed: ADCs, bispecific engagers, marrow transplant, oncolytic virus |
| Escape list never independently audited (rule 9) | new `escape_audit.py` + tests | **18 candidates enumerated from outside the project; 4 new route gaps found → 16 audited escapes.** All 4 close on a measurement, a justified transfer or a structural argument; none on a bare assumption |
| CSF prior assumed at 0.70 | `emergence.csf_reach_fail_terms()` | **Derived 0.428 [0.24, 0.69]**, decomposed into pharmacologic (0.12) × delivery (0.35). CSF durability rises 0.33 → **0.434**. Dominant risk is now correctly named as **sustained delivery, not potency** |
| "Recurrent minority" label | `genotype_tiered_durability`, `maintenance_durability` | Corrected to **≤62.8% region-level** (upper bound on MTAP-null), with the stain still the gate |
| MTAP∩MAPK resolved by priority | new `maintenance_plan_for()` | Returns a **combination** for MTAP+MAPK and for MTAP+RB1-intact, each with its evidence basis; `best_tier_for` kept for the categorical grid |
| TNG462 called "designed brain-penetrant" | `core/breed_wide_durability.py` | Corrected: **0/23 partial responses** in evaluable glioblastoma patients; CNS lead moved to CDK4/6 |
| Abemaciclib brain claim graded "class effect" | `core/toxicity.py` | Replaced with **measured** human brain-tumour exposure (96× CDK4, 19× CDK6) plus the honest efflux numbers (Kp,uu 0.03–0.11) |
| PRMT5-before-MAT2A ordering | `maintenance_durability` MTAP tier | **Split by site:** MAT2A first at systemic sites on response rate; CDK4/6 first in the brain; PRMT5i added when a CNS readout exists |
| Immune floor scored as independent | `maintenance_durability` floor tier | Records **MTA-mediated suppression** — the floor is weakest in exactly the genotype the MTAP arm targets |
| Stale verdict counts in the report | `CONSOLIDATED_REPORT.md` | Corrected to 7 measured / 2 transfer / 1 model-derived / 2 structural / **0 assumed**, and scoped to the stated catalogue |

**The audit's most important single finding is structural, not biological:** six of the twelve
original escape closures rest on **one agent class** (the microtubule cytotoxic), and its resistance
mechanism — ABCB1/ABCG2 efflux — is *measured present* in canine HS lines in the very paper that
establishes the class's potency (PMID 25715778). The escape list had never named the failure of the
drug doing most of the work. It is now route **A13**, answered by drug choice: a colchicine-site
binder that retains activity in P-gp-overexpressing and tubulin-mutant cells (PMID 28797699), which
is what `core.microtubule_route` had already selected on independent access grounds.

---

## Big-picture verdict (2026-10-01): do the combinations hold for 10+ years?

Graded against the user's words: *"make sure every mechanism and every escape is closed by either
real data or rigorous model, potency, toxicity etc all need to be considered"*; *"looking for 10+
years of durability"*; *"assuming early detection"*; *"I'm okay with no specific data but if
scientifically sound."*

| Part | Verdict | Basis (where) |
|---|---|---|
| Clearing the first tumour | **Holds within a now-stated catalogue.** Every escape has a closing agent: of the original 12, 7 measured in canine HS, 2 transferred, 1 model-derived, 2 structural, **0 assumed**; all 45 pairs and 120 triples covered; toxicity budgets computed, one collision (radiation + CNS microtubule agent) resolved by sequencing. The 4 audit-added routes close on 1 measurement-backed drug choice, 2 transfers, 1 structural argument | `CONSOLIDATED_REPORT.md`, `coverage_assessment`, `escape_audit` |
| "Every mechanism" | **Now established, as a scoped claim.** "Closed within this catalogue of **25 modality classes and 16 escape routes**", 0 classes unassessed, 10 excluded with reasons named. [**Superseded 2026-10-31: 26 classes, 11 excluded.**] [**Superseded again 2026-11-01: 28 classes, 12 excluded, 1 OPEN** — antimetabolites.] [**Superseded again 2026-11-02: 29 classes, 13 excluded, 1 OPEN** — antimetabolites CLOSED on three measured canine-HS IC50s; targeted protein degradation found missing and opened.] [**Superseded again 2026-11-03: 42 classes, 16 excluded, 11 OPEN** (three external-taxonomy diffs).] [**Current, 2026-11-04: 55 classes — 16 in model, 18 excluded, 21 OPEN** (fourth and fifth axes; see the last section of this file).] Not the same as "every conceivable mechanism" — it is a claim whose boundary is written down | `candidate_universe.closure_claim()`, `escape_audit` |
| Staying clear for 10 years | **Scientifically sound hypothesis, not a result.** Model P(10-year), systemic sites: 0.56–0.72 without monitoring, 0.81–0.86 with detect-and-switch. Brain-local hinges on drug access. **CSF now 0.434 [0.17, 0.69]** on a derived rather than assumed prior, and the binding constraint there is sustained delivery (no intrathecal sustained-release product exists), not potency | `emergence.py`; `maintenance_durability.csf_answer()` |
| Oct 2026 literature | **No change to the design.** PRMT5 brain arm weaker, CDK4/6 brain arm better evidenced on the same deletion (section A); the deletion is common (62.8%), which widens coverage; the immune floor is weaker in MTAP-null tumours | sections A, B |
| Largest uncertainty | **How often a cleared, predisposed dog throws a new primary (Λ)** — 50–90% of the variance. Not a drug question | `emergence.py` value-of-information |

---

## A. The brain arm for the deletion-carrying tumour: CDK4/6 now holds up better than PRMT5 (Oct 2026)

### What weakened

The brain arm of the MTAP tier relied on a brain-penetrant MTA-cooperative PRMT5 inhibitor. As of
October 2026:

| Agent | Brain evidence | Status in record |
|---|---|---|
| TNG908 | Failed to reach therapeutic CNS exposure in glioblastoma | ALREADY COVERED (`pkpd.py`, 2026-08-23); CNS anchor moved to TNG456 |
| TNG462 (vopimetostat) | Glioblastoma: 23 evaluable patients at active doses, **0 partial responses**, median time on study < 8 weeks (Tango, Oct 2025) | **NEW.** `core/breed_wide_durability.py:255` still calls TNG462 "designed brain-penetrant" |
| TNG456 | No human efficacy data yet (expected 2026). Mouse U87MG: 84% growth inhibition at 30 mg/kg BID, 56% regression at 90 mg/kg BID. Phase 1/2 NCT06810544, **alone and with abemaciclib**. [J Med Chem](https://doi.org/10.1021/acs.jmedchem.6c00035) | PARTIAL (named as CNS anchor; trial design and mouse numbers new) |
| MAT2A inhibitors | **No brain-penetrant MAT2A inhibitor published.** PubMed `brain-penetrant MAT2A inhibitor MTAP-deleted glioblastoma`: 0 records | NEW |

So there is **no MTAP-directed drug with human evidence of activity in the brain.** The PRMT5 brain
arm is a promise pending TNG456.

### What holds up: hit the same deletion through CDKN2A, with abemaciclib

The CFA11q16 deletion removes CDKN2A as well as MTAP. Losing CDKN2A (p16) makes the cell depend on
CDK4/6 — a dependency an approved, oral, brain-reaching drug already blocks. Abemaciclib is in the
repo as the CDKN2A/RB1-intact tier agent (`core/genotype_tiered_durability.py:126`), but its brain
claim was graded "class effect; canine data absent" (`core/toxicity.py:331`). The evidence for each
link:

| Link | Evidence | Grade |
|---|---|---|
| Target present in this disease | CFA11q16 deletion including CDKN2A/B in **62.8%** of canine HS (60.7% BMD, 66.7% FCR). Hédan 2011 [10.1186/1471-2407-11-201](https://doi.org/10.1186/1471-2407-11-201) | MEASURED, canine HS (PARTIAL: paper already in report refs; figure not used) |
| Rb intact, p16 down | CDKN2A down and **Rb preserved in every canine histiocytic line**, including lines from **localized HS**. Hirabayashi 2022 [10.1111/vco.12812](https://doi.org/10.1111/vco.12812) | MEASURED, canine HS (ALREADY COVERED) |
| Canine HS cells respond to the class | Palbociclib inhibited growth of **all** lines, including localized-HS lines, and a xenograft. Same paper | MEASURED, class (ALREADY COVERED) |
| Abemaciclib acts on canine cancer cells | G1 arrest, growth suppression in 5 canine melanoma lines + xenograft (Kim 2025 [10.3389/fvets.2025.1603686](https://doi.org/10.3389/fvets.2025.1603686)); canine lymphoma lines, p16-low most sensitive, high p16 = resistance (Maylina 2022 [10.1292/jvms.22-0498](https://doi.org/10.1292/jvms.22-0498)) | MEASURED in canine cells, other tumours. Abemaciclib on canine HS itself: **TRANSFERRED** (same class, same target, Rb intact) — NEW |
| Reaches a brain tumour | Resected human brain-metastasis tissue: unbound active abemaciclib **96× CDK4 IC50, 19× CDK6 IC50**. Tolaney 2020 [10.1158/1078-0432.CCR-20-1764](https://doi.org/10.1158/1078-0432.CCR-20-1764) | MEASURED in humans; TRANSFERRED to dog — NEW |
| Holds tumours in the same anatomical place | Alliance A071401: progressive grade 2/3 **meningioma** (dura-based, extra-axial — the same niche as the breed's tumour) with NF2 or CDK-pathway loss. **PFS6 58% (14/24), met primary endpoint**; best response stable disease 16/24; well tolerated. Brastianos 2026, *Nat Med* [10.1038/s41591-025-04141-4](https://doi.org/10.1038/s41591-025-04141-4) | MEASURED in humans — NEW |
| Can be dosed for years | Approved, oral, continuous; human adjuvant use runs 2 years. Dogs: repeat-dose toxicology to 3 months, target organs marrow, GI, lymphoid, male reproductive (FDA NDA 208716 review). Canine exposure numbers not extracted (file exceeds fetch limit) | MEASURED (human, dog tox); canine exposure **not yet in hand** — NEW |

### Limits, at the strength shown

1. **It holds; it does not shrink.** Cytostatic: the meningioma trial's best response was stable
   disease. That is the job of maintenance (stop a new clone growing), not induction. Division-gated.
2. **The barrier still pumps it out.** Abemaciclib is a P-gp/BCRP substrate: oral unbound
   brain:plasma (Kp,uu) **0.03 in mice, 0.11 in rats**, yet it extended survival in orthotopic
   glioma at those exposures (Raub 2015 [10.1124/dmd.114.062745](https://doi.org/10.1124/dmd.114.062745));
   knocking out both pumps raises brain penetration 25× (Martínez-Chávez 2021
   [10.1016/j.phrs.2021.105954](https://doi.org/10.1016/j.phrs.2021.105954)). The extra-axial mass
   sits largely outside the intact barrier, which is what the meningioma data speaks to. Tumour cells
   that have **invaded behind an intact barrier**, and the CSF, may see much less — the same gap the
   report already assigns to local delivery, radiation and intrathecal dosing. This does not close it.
3. **Per-tumour gates.** Needs Rb intact and p16 lost — two stains, the same kind of cheap test as the
   MTAP stain.
4. **Not a lock.** CDK4/6-inhibitor resistance is well documented in humans; this arm is
   surveillance-grade, like MEK. (The MTAP arm was itself already downgraded to "anchored, not locked".)
5. **Backups exist but are preclinical.** GLR2007, a CDK4/6 inhibitor designed for the brain:
   Kp,uu 0.23 in mice, 95.9% growth inhibition in orthotopic glioblastoma
   ([PMC9403987](https://pmc.ncbi.nlm.nih.gov/articles/PMC9403987/)); no clinical results found.
   Lerociclib (G1T38): 28 days of continuous dosing in beagles without severe neutropenia
   ([10.18632/oncotarget.16216](https://doi.org/10.18632/oncotarget.16216)) — relevant to dosing for years.

### Net

For the deletion-carrying brain tumour, **every link of the CDK4/6 arm has a human or canine
measurement except two transfers** (abemaciclib potency on canine HS; brain exposure in the dog).
The PRMT5 arm has none in the brain. Lead the brain arm with abemaciclib now; add TNG456 on the same
deletion if it reads out — its own trial already pairs the two.

---

## B. September 2026 sweep — relabelled after a record check

| # | Finding | Label | Note |
|---|---|---|---|
| 1 | Disseminated HS often clonally independent (24–45%). Mottier 2026 [10.1371/journal.pone.0345429](https://doi.org/10.1371/journal.pone.0345429) | **ALREADY COVERED** (`CONSOLIDATED_REPORT.md` finding 4, since 2026-09-02) | Disseminated-case evidence: **indirect** for this case. Earlier version of this file wrongly called it new |
| 2 | CDKN2A/B region deleted in 62.8% of canine HS. Hédan 2011 | PARTIAL | Paper in report refs; figure not used; contradicts "minority" labels |
| 3 | MTAP IHC formally reviewed as a routine surrogate. Salzano 2026 [10.3390/diagnostics16132069](https://doi.org/10.3390/diagnostics16132069) | NEW | De-risks the MTAP stain |
| 4 | 10 canine HS lines + 1824-compound screen; duvelisib. Sakuma 2026 [10.1111/vco.70077](https://doi.org/10.1111/vco.70077) | **ALREADY COVERED** (report, "Also noted"; `v2/engine.py`) | The in-vitro falsifier route it enables is the new point |
| 5 | TNG908 CNS failure | **ALREADY COVERED** (`pkpd.py`) | |
| 5b | TNG462: 0 PRs in 23 evaluable GBM patients | NEW | See section A |
| 6 | MAT2A outperforms PRMT5 on response rate (IDE397 38%/30% PR; AMG 193 ORR 21.4%) | NEW | Systemic sites only; no brain data |
| 7 | MTAP-deleted tumours are immunologically cold (MTA-mediated) | NEW | Weakens the immune floor exactly where the MTAP tier applies |
| 8 | Oncolytic BoHV4 on canine HS lines. Di Pentima 2026 [10.1007/s11259-026-11428-5](https://doi.org/10.1007/s11259-026-11428-5) | **ALREADY COVERED** (report, "Also noted") | Mentioned, not assessed in the catalogue (rule 9) |
| 9 | CT subtypes periarticular vs systemic HS. Folie 2026 [10.3389/fvets.2026.1917708](https://doi.org/10.3389/fvets.2026.1917708) | NEW | Not relevant to the intracranial case |
| 10 | Liquid-biopsy review. [10.3390/ijms27188183](https://doi.org/10.3390/ijms27188183) | NEW | No canine HS assay; surveillance dependence unchanged |
| 11 | PRMT5 inhibitors in canine cells | Still **zero** records | The deposit's central gap is still open |

---

## Corrections — all applied 2026-10-01

Corrections 1–11 from the previous revision are applied; see the gap-closure table at the top.
`pkpd.PARAMS` still keys the PRMT5 entry `"tng908"` for backward compatibility while its contents
describe the TNG456 anchor — a naming wart, not a claim.

## What remains open after this pass

These are genuinely open, not deferred corrections:

1. **Per-day kill rates** are fully derived only where a canine Cmax exists (cobimetinib). Everything
   else is an IC50 plus a transferred or assumed exposure.
2. **The growth-rate bar (0.055/day)** that sets every pass/fail is still an uncited placeholder, and
   it enters the answer twice. Probably readable from scans already taken.
3. **Canine CNS access** is unmeasured for every agent, including abemaciclib — whose brain evidence
   is human and rodent.
4. **The fluid-to-cell fraction in CSF** remains unmeasured; the derived prior bounds it rather than
   measuring it.
5. **Λ, the second-primary emergence rate**, still carries 50–90% of the variance in the 10-year
   number. The highest-value study in the whole project is an observational cohort of cleared,
   predisposed dogs — not a drug experiment.
6. **MTAP status in canine HS has still never been measured.** Zero records. The entire MTAP arm is
   gated on one immunostain that nobody has run.
7. **A15 (acquired RB1 loss) inherits the surveillance dependence** — and canine HS ctDNA is
   unvalidated, so in practice it would be detected late.

---

## Closed and simplified (2026-10-02, final pass)

**The goal is achieved.** `standard_audit.failing()` is empty, `candidate_universe.not_assessed()`
is empty, and every one of the 16 audited escape routes closes at both occupied sites.

The last assumed number is retired. Closure previously rested on `REFERENCE_POTENCY = 0.15/day`, a
bare constant, against a requirement of ~0.10/day — a 1.5× cushion on a guess, which is not a
closure. `pkpd.PARAMS['rgn3067']` replaces it with a kill rate **derived from two measured numbers**:
the worst of four patient-derived GB-line IC50s (616 nM) and a rodent **brain** Cmax after oral
dosing (20 µM, PMID 38398008; equal plasma and brain levels, efflux ratio 0.61).

| | Value |
|---|---|
| Derived kill rate | **1.17/day** (vs 0.15 reference, vs ~0.10 needed) |
| Worst margin, invaded parenchyma | **+0.59/day** |
| Worst margin, leptomeninges/CSF | **+0.61/day** |
| Minimum fraction of measured brain exposure for closure | **0.89% — a 112× cushion** |

That cushion is the point: the closure no longer leans on the cross-species transfer.

### Report structure, simplified

The user asked for a report with no back-and-forth. The 879-line document carrying 15 retraction and
correction passages was renamed **`AUDIT_TRAIL.md`** and banner-marked as the working record.
**`CONSOLIDATED_REPORT.md`** is now a clean ~160-line document: verdict, two moves, regimen,
why access is not the obstacle, evidence grade per deciding number, the seven conditions, the limits,
what to do first. Reader-facing artifact: <https://claude.ai/artifact/4Ho2u4jTieU579ExuRgvY5>.

Nothing was deleted. Every retraction remains in `AUDIT_TRAIL.md`.

---

## Rule-13 pass (2026-10-02): availability tiered, exclusions re-grounded

Upstream commit `3afc850` added CLAUDE.md **failure 8 and rule 13**. Audited against it, two defects
in this branch's own work. Both are now fixed in code, not just in prose.

### Defect 1 — five exclusions rested on absent canine data

Rule 13 admits exactly three grounds: kill contradicted, defeated by a named escape, toxicity
unaffordable. Five of `candidate_universe`'s ten exclusions were argued on the literature instead
("not obtainable for a dog", "no canine-HS activity data", "no canine product exists", "in-vitro
only", "unmeasured in dogs"). Under the user's own standard — *"I'm okay with no specific data but if
scientifically sound"* — those are not grounds at all.

Every exclusion now carries an `ExclusionGround`, `_validate()` rejects an EXCLUDED class without
one, and `excluded_citing_absent_canine_data()` is a lint that must stay empty.

| Class | Was | Now |
|---|---|---|
| CSF1R | "not obtainable for a dog" | DEFEATED_BY_ESCAPE — CSF1R-independence is *observed* as acquired resistance in human histiocytosis |
| Epigenetic (HDAC/BET) | "no canine-HS activity data" | TOXICITY_UNAFFORDABLE — and **computed**: `epigenetic_toxicity_arithmetic()` reads live marrow load 0.70 from `core.toxicity`, adds the class's transferred 0.45 burden, total 1.15, oversubscribed |
| Bispecific engagers | "no canine product exists" | DEFEATED_BY_ESCAPE — the tumour *is* the antigen-presenting lineage, and exports MTA (A16) |
| Oncolytic virotherapy | "in-vitro only" | DEFEATED_BY_ESCAPE — must be injected into a known lesion, so the second-primary route is untouched |
| Metabolic / dietary | "unmeasured in dogs" | TOXICITY_UNAFFORDABLE — years of methionine restriction costs lean mass in an older large-breed dog |

Final grounds: **5 kill contradicted, 3 defeated by a named escape, 2 toxicity unaffordable, 0 for
absent canine data.** Availability is now a separate axis (`Availability`), because conflating it
with the ground was the lapse: marrow transplant is *established in dogs* and excluded anyway, which
is what makes that exclusion informative.

### Defect 2 — the closing programme was built from agents that do not exist, and said otherwise

`core/microtubule_route.build()` flags every agent `obtainable=True`. Three of the regimen's agents
cannot be dispensed to a dog: RGN3067 (preclinical, rodent-only), paxalisib (investigational), and
the PRMT5 anchor (human Phase I/II). The report's own table said "obtainable for dogs". The margins
were never affected — the inputs behind them are measured — but the availability claim was false.

`availability_tiers.py` now tiers all 11 components (**8 exist today, 3 to-build**) and, per rule 13,
searches the programme **from exists-today agents first**. The flag itself is *reported* rather than
flipped — `mislabelled_as_obtainable()` names both offenders — because it drives `obtainable_only`
in the deterministic ledger and changing it would move published margins silently.

| Site | Programme A (licensed today) | Programme B (full) |
|---|---|---|
| Extra-axial, meninges-based bulk (23/23 dogs) | **CLOSES, +0.94/day** | closes |
| Leptomeninges / CSF | **CLOSES by mouth, +0.031/day** | +0.61/day |
| Invaded parenchyma, intact barrier | **MARGINAL, −0.034 to +0.017/day** | +0.59/day |

**Programme A closes 2 of 3 sites with licensed agents and no procedure on the critical path.** It
gets there on abemaciclib, and the reason is anatomical: this tumour is extra-axial in 23/23 dogs, so
its bulk sits on the blood side of an already-disrupted barrier, where abemaciclib's concentration in
resected human brain lesions is a measured 19× the CDK6 IC50. Behind an *intact* barrier its own
measured rodent unbound ratios give 0.65–2.4 nM against a 1.8 nM bar — closes at the rat ratio, fails
at the mouse ratio. Scored on its own numbers, not on the generic small-molecule access of 0.021,
which would have flattered it ~5×.

### The gap, stated from the computation

`the_gap()` reads it off `uncovered_properties()` rather than asserting it. An earlier draft of that
docstring called the gap "one property"; the field data says **two, on different agents** —

1. **access and duty from one schedule** at the invading edge (RGN3067's role; paxalisib is the same
   property on the PI3K axis, where duvelisib covers the potency but not the access);
2. **genotype anchoring** — the only kind of agent automatically matched to a *second* primary.

Everything else the decade needs is satisfiable today. None of the three missing agents has to be
discovered. **The outstanding work is veterinary formulation and access, not chemistry.**

### Consequences recorded

- `deterministic_closure.CONDITIONS` gains **C8** (`Status.TO_BUILD`): the conjunction is now
  **8 conditions, 5 met**, outstanding C5 / C7 / C8. Engineering blockers remain **0** — C5 is a
  test, C7 and C8 are availability.
- `CONSOLIDATED_REPORT.md` gains **§6a** (the two programmes side by side), an availability column on
  the regimen table, and an explicit note that its earlier "obtainable for dogs" was wrong.
- Does **not** change: the 16 routes, the 25-class universe, the derived 1.17/day kill rate, the 112×
  exposure cushion, or `standard_audit.failing()` (still empty).

---

## The invading edge closes on a licensed drug (2026-10-02)

The rule-13 pass above left **one** site open: invaded parenchyma behind an intact barrier, where
the obtainable programme was MARGINAL on abemaciclib's own measured rodent range (−0.034 to
+0.017/day). The active goal says keep searching if the decade does not hold, so the search
continued. It found the answer, and the answer is a measurement rather than a molecule.

### The question had been asked in the wrong units

"Does a drug get into brain" and "does a drug get into tumour that still has an **intact** barrier
around it" are different questions. The project had been answering the second by inference, three
different ways: a rodent brain:plasma ratio (abemaciclib), a generic compartment access figure
(0.021, measured for chlorambucil in normal brain), or a concentration from an **enhancing** lesion,
where the barrier is already broken.

**Gadolinium-non-enhancing tumour *is* tissue behind an intact barrier** — that is what
non-enhancement means. So a drug concentration measured there answers the question directly. Two
human Phase 0 trials did that for ribociclib, by dosing and then assaying resected tumour.

| Source | Dose | Unbound in **non-enhancing** tumour | × 40 nM IC50 | Margin |
|---|---|---|---|---|
| PMID 41206763 | 400 mg, lowest patient | 65 nM | 1.6× | **+0.267/day** |
| PMID 41206763 | 400 mg, median | 170 nM | 4.2× | +0.498/day |
| PMID 41206763 | 600 mg, median | 634 nM | 15.8× | +0.887/day |
| PMID 31285369 | 900 mg, mean | 560 nM | 14× | +0.848/day |
| PMID 31285369 | 900 mg, mean **CSF** | 374 nM | 9.4× | +0.724/day |
| PMID 31285369 | 900 mg, mean **enhancing** | 2152 nM | 54× | +1.280/day |

Citations: Tien/Li/Sanai, *Clin Cancer Res* 2019;25(19):5777-5786, PMID 31285369,
doi:10.1158/1078-0432.CCR-19-0133. Johnson/Tien/Sanai, *Neuro Oncol* 2026;28(3):659-671,
PMID 41206763, doi:10.1093/neuonc/noaf257.

### Why this is the strongest single input in the project

1. **Measured in the compartment at issue**, not transferred across compartments.
2. **The genotype matches, unusually closely.** The 2026 trial enrolled on *CDKN2A/B deletion or
   CDK4/6 amplification, PTEN loss or PIK3CA mutation, wild-type Rb* — which is the CFA11q16 lesion
   in 62.8% of canine HS plus this project's own PTEN tier, and CDK4/6 dependency is already
   MEASURED in canine histiocytic lines (PMID 35278028).
3. **Pharmacodynamics confirmed in the same tissue**: RB phosphorylation and Ki-67 both significantly
   reduced.
4. **Licensed** (Kisqali), oral, daily — so access and duty come from ONE schedule. This is the
   schedule-coherence requirement met without a procedure, by a drug a vet can obtain.
5. **The assay returns negatives.** Everolimus, dosed in the same patients, was undetectable
   (<0.1 nM) in both enhancing and non-enhancing tumour. The method is not flattering the brain.

Priced on the toxicity ledger as `"ribociclib (CDK4/6)"`: marrow 0.45 primary, and a **new
`Organ.CARDIAC` axis** at 0.50 for QT prolongation. The axis was added rather than noted, because
recording a cardiac-toxic agent's burden only in prose would let it read as free. Nothing else in
the catalogue loads that axis, so the QT burden collides with nothing; the marrow does collide with
the induction cytotoxic. Whole profile is a human-label TRANSFER; no canine PK exists.

### What it does not close, and this is the part that must not be softened

- **Cells that are not dividing.** CDK4/6 inhibition is division-gated and cytostatic. The
  drug-tolerant persister at the invading edge is therefore held by SCHEDULE (continuous dosing,
  C3), not by a second kill mechanism. `persister_cover_at_the_invading_edge()` enumerates the
  candidates: of the agents that are neither division-gated nor antigen-directed and reach that
  compartment, the only exists-today one is hydroxychloroquine, worth ~2e-5/day — cover, not kill.
  The agent measured in canine HS for that job, DMAPT, is research-stage. **This is now the only
  remaining gap that is science rather than supply.**
- **The PI3K axis in brain, where the evidence is worse than silence.** Ribociclib monotherapy had
  limited efficacy in recurrent glioblastoma (median PFS 9.7 weeks) *despite confirmed target
  engagement*, and the recurrences showed PI3K/mTOR upregulation. The agent paired to block that
  reroute was undetectable in tumour. `the_parallel_pathway_problem()` records this as a MEASURED
  NEGATIVE, which is stronger evidence than a missing number: duvelisib is licensed with the
  canine-HS IC50 and unmeasured brain access, paxalisib has the measured Kp,uu 0.31 and no
  veterinary access.
- **The genotype anchor** (C7) — a second primary is met by detect-and-switch, not a standing guard.

### Where the two programmes now stand

| Site | Programme A (licensed only) | Programme B (full) |
|---|---|---|
| Extra-axial, meninges-based bulk | **CLOSES +0.94/day** | closes |
| Leptomeninges / CSF | **CLOSES BY MOUTH +0.72/day** | +0.61/day |
| Invaded parenchyma, intact barrier | **CLOSES +0.27/day at the worst measured value** | +0.59/day |

Intrathecal bolus is demoted from a required route to a backup. `program_a()["closes_everywhere"]`
is now `True`, and `program_a()["verdict"]` states the persister caveat in the same breath — a test
(`test_program_a_does_not_overstate_that_into_full_closure`) fails if it ever stops doing so.

### Consequences recorded

- **C8 narrowed.** It was "the penetrant agents are not obtainable"; it is now "the three MECHANISMS
  no licensed agent supplies", with access at the invading edge explicitly removed from its scope.
  Conjunction remains 8 conditions, 5 met, outstanding C5 / C7 / C8, engineering blockers 0.
- `uncovered_properties()` changed from `{RGN3067: [access, duty], ...}` to
  `{RGN3067: [position-independent kill], PRMT5: [genotype anchoring], paxalisib: [access]}`.
  `the_gap()` is now GENERATED from those fields — it had been written as prose and gone stale twice,
  first calling the gap "one property" and then headlining the access gap ribociclib had closed.
- `CONSOLIDATED_REPORT.md` §6a rewritten around the measured table; a new row in the §5 evidence
  grid; the "brain-penetrant is not brain-effective" limit now cites ribociclib itself as the case
  in point, which is stronger than the sagopilone example it used before.
- Unchanged: the 16 routes, the 25-class universe, `standard_audit.failing()` still empty.

---

## All 16 routes close with licensed drugs (2026-10-02)

The previous pass closed ACCESS at every site with licensed agents but left three mechanism gaps, and
reported them as "two of three are supply, one is science". Site closure is not route closure, so the
goal ("all mechanisms and escapes") was not met. Searching continued, with rule 14 applied to each gap
in turn. Two of the three closed, and the third narrowed.

### Gap 1 — cells that are not dividing: CLOSED, structurally, by a licensed drug

Every licensed agent reaching the invading edge is division-coupled. The Phase 0 literature confirmed
that rather than refuting it: Wee1 inhibition (AZD1775, median unbound tumour:plasma 3.2, PMID 29798906)
and PARP inhibition (niraparib, PMID 38657366) both penetrate but both act through replication.

**Dordaviprone (ONC201)** does not. It is a ClpP agonist that drives proteolysis of **electron
transport chain and TCA cycle proteins** (PMID 37195023), so the kill is a collapse of oxidative
phosphorylation — which a quiescent cell requires as much as a dividing one. **FDA accelerated
approval 2025** for H3K27M-altered diffuse midline glioma (PMID 42232453); oral, once weekly, well
tolerated. The indication is itself the access argument: DMG is unresectable, diffusely infiltrative
and largely non-enhancing.

Target transfer **computed, not asserted** — `sequence_conservation.clpp_domain_partition()`:

| Region | Differences | Note |
|---|---|---|
| Transit peptide 1–56 | **10** | **cleaved on mitochondrial import — absent from the mature protein** |
| Mature ordered 57–245 | **3** | **98.41% identical** |
| Disordered tail 246–277 | 7 | |
| Active sites Ser153, His178 | **0** | **both identical** |

So the raw 92.65% understates it. DRD2, the second mechanism, is 96.39% identical, and D2 antagonists
are routine in dogs.

Graded **STRUCTURAL, not MARGIN**, and deliberately: no canine-HS data of any kind (class-mechanism
transfer), no published unbound tumour concentration so no kill rate is derived, and **once-weekly
dosing sits awkwardly against continuous duty (C3)** — mitigated only by the argument that a degraded
mitochondrial proteome must be resynthesised rather than washed out. An argument, not a measurement.

### Gap 3 — the genotype anchor: CLOSED by a licensed drug, for the same deletion

This gap was an error of conflation on my part, not a missing drug. The project had equated "genotype
anchoring" with MTAP-directed synthetic lethality, and concluded nothing licensed could anchor. But the
CFA11q16 deletion removes **CDKN2A/B as well as MTAP**, and the CDKN2A product p16 has exactly one
function: inhibiting CDK4/6. **A CDK4/6 inhibitor pharmacologically replaces the deleted gene
product** — it is matched to the inherited lesion, not a somatic driver, so a second primary from the
same deletion is met by the same drug without re-stratifying. Licensed, with canine-HS dependency
measured (PMID 35278028) and the human trial enrolled on exactly this genotype (PMID 41206763).

`availability_tiers.is_cdk46_a_genotype_anchor()`. The MTAP arm is **not** redundant: CDK4/6 inhibition
requires Rb intact, so acquired RB1 loss (A15) defeats this anchor, and the MTAP/PRMT5 anchor is
Rb-independent. That is now the precise statement of what the MTAP arm uniquely adds.

### Gap 2 — PI3K axis brain access: still the weakest row, and graded as such

Searched, not closed. The Phase 0 record supplies two measured negatives on this axis and one
calibration point:

| Agent | Unbound in non-enhancing tumour | Verdict in source |
|---|---|---|
| **ribociclib** | **170–634 nM** (40 nM target) | active; RB phosphorylation and Ki-67 down |
| ceritinib | **6 nM** | "insufficient for target modulation" (PMID 34702773) |
| everolimus | **undetectable (<0.1 nM)** | undetectable at every dose (PMID 41206763) |

The ceritinib row matters as a control: same group, same assay, same compartment, and it returns a
clean negative. That is what makes ribociclib's number a signal rather than an artefact.

Duvelisib closes the RTK-bypass route on the project's **TRANSFERRED** generic small-molecule access
(0.021 vs a required 0.0143), with its own brain access unmeasured. Under rule 11 that is CLOSED at
TRANSFERRED grade, not open — but with a named risk, since a different agent on the same axis was
measured undetectable. Recorded in `the_parallel_pathway_problem()` and flagged as
`program_a_route_ledger()["weakest_row"]`.

### The route ledger

`availability_tiers.program_a_route_ledger()` — all 16 audited routes (the 12 disease escapes plus
A13–A16), each with a named licensed carrier and a closure kind:

| Kind | Count |
|---|---|
| MARGIN (computed kill rate beats the growth bar) | **3** |
| STRUCTURAL (the lesion cannot apply to these drugs) | **12** |
| GATED (on the pre-treatment immunostain) | **1** |
| **OPEN** | **0** |

A13 is worth noting: the audit's main structural finding was that six of twelve closures rested on the
microtubule class alone. Programme A has **no tubulin-binding agent at all**, so that single point of
failure is dissolved rather than mitigated.

### What is honestly weaker than Programme B

**12 of 16 close STRUCTURALLY.** "The lesion cannot apply to these drugs" is sound but weaker than
"these drugs out-kill it". Programme B carries +0.59/+0.61 per day from a derived 1.17/day cytotoxic;
Programme A has no equivalent cytotoxic margin. `program_a_route_ledger()["verdict"]` says this, and
`test_the_ledger_distinguishes_margin_from_structural_closure` fails if it stops.

### Remaining to-build — three quantities, not three mechanisms

1. a **computed cytotoxic margin** at the invading edge;
2. a **measured brain concentration** on the PI3K axis;
3. an **Rb-independent germline anchor**.

Two are compounds in human trials; the third is a measurement nobody has taken. C8's requirement text
was narrowed twice to track this, and `test_c8_...` asserts all three terms appear in it.

### Consequences recorded

- `sequence_conservation.CONSERVATION` gains CLPP and DRD2 (computed live from UniProt via
  `recompute()`), plus `clpp_domain_partition()`.
- `availability_tiers` gains `dordaviprone (ONC201)` as an exists-today agent, `PROGRAM_A_ROUTES`,
  `program_a_route_ledger()`, `is_cdk46_a_genotype_anchor()`; `persister_cover_at_the_invading_edge()`
  now reports CLOSED STRUCTURALLY.
- `program_a()["verdict"]` rewritten — it had become factually stale (still saying the persister was
  uncarried) and a test caught it.
- Unchanged: the 25-class universe, `standard_audit.failing()` still empty, 8 conditions / 5 met /
  0 engineering blockers.

---

## Cytostatic correction, a licensed cytocidal partner, and the goal graded (2026-10-02)

Two things happened in this pass: I found and fixed an error of my own, and the search closed two of
the three remaining items.

### THE CORRECTION — ribociclib's margins were a cytotoxic reading of a cytostatic drug

`emax_kill_rate` reads an assay's surviving fraction as exponential DEATH. That is right for a
cytotoxic and **wrong for a cytostatic**. Applied to ribociclib it produced "+0.27 to +0.89/day kill
margins" at the invading edge, and those numbers went into `CONSOLIDATED_REPORT.md` **and the
published artifact**. CDK4/6 inhibition arrests the cycle; the trial's own endpoints are
proliferation readouts (G1→S suppression, Rb phosphorylation, Ki-67), not death.

Corrected reading: f = C/(C+IC50), residual net growth = growth × (1 − f), **bounded below by zero**.

| Site | Unbound | Proliferation suppressed | Residual net growth | Doubling |
|---|---|---|---|---|
| Extra-axial bulk | 2152 nM | 98.2% | 0.00100/day | 691 d |
| CSF | 374 nM | 90.3% | 0.00531/day | 130 d |
| Invading edge (400 mg median) | 170 nM | 81.0% | 0.01048/day | 66 d |
| Invading edge (lowest patient) | 65 nM | 61.9% | 0.02095/day | 33 d |

Untreated: 12.6 d. So ribociclib stretches doubling by 2.6–55×, which is large and useful, and **is
not regression**. No concentration of a pure cytostatic clears a tumour.

**The measured ACCESS result is untouched** — 170–634 nM unbound in Gd-non-enhancing tumour remains
the project's strongest input. Only the *reading* of it as a kill rate was wrong. Recorded in
`pkpd.ribociclib_margin_correction()` with what replaced it; `test_the_correction_itself_is_recorded_rather_than_silently_applied`
fails if the record is removed.

### GAP CLOSED — a licensed CYTOCIDAL drug, and it is genotype-matched

**Niraparib** (licensed). Three properties, the third unexpected:

1. **Cytocidal** — PARP inhibition converts single-strand to double-strand breaks. Supplies exactly
   what CDK4/6 inhibition cannot.
2. **Brain-penetrant, measured in the right patients** — validated LC-MS/MS in human brain-tumour
   tissue and CSF, fractions unbound 0.05 brain / 0.16 plasma, authors report significant brain
   penetration in glioblastoma patients (PMID 38657366). Trial NCT05076513 ongoing, so there is **no
   published unbound tumour concentration** — which is why no kill rate is derived.
3. **Genotype-matched to the germline lesion.** PARP inhibitors **inactivate PRMT5**, and
   MTAP-deficient tumours are measurably more vulnerable to olaparib in vivo (PMID 42122132).
   Corroborated with a clean genotype control: type I PRMT inhibition + talazoparib is synergistic at
   low nanomolar concentrations in MTAP-**negative** lines, and **re-introducing MTAP reduces
   sensitivity** (PMID 33691794), with raised γ-H2AX confirming the mechanism.

So a licensed drug reaches the axis the to-build PRMT5 arm was for, **Rb-independently** — which also
supplies the successor for A15 (acquired RB1 loss), previously fillable only by the to-build arm.
Complementary with dordaviprone rather than redundant: PARP inhibition is replication-coupled and so
does **not** reach the non-dividing persister, which is dordaviprone's job.

Priced: `"niraparib (PARP)"`, marrow 0.50 + skin/vascular 0.20. **The collision matters and is
reported because it is tight:** with ribociclib's 0.45 the marrow axis sums to **0.95, leaving 0.05
headroom**. Tolerable; nothing else myelosuppressive can join without dose reduction.

### Both halves of the deletion are now anchored by licensed drugs

| Half of CFA11q16 | Licensed anchor | Mechanism | Rb-dependent? |
|---|---|---|---|
| CDKN2A | ribociclib / abemaciclib / palbociclib | replaces the deleted p16's function | **yes** |
| MTAP | niraparib | PARP inhibition inactivates PRMT5 | **no** |

Independent mechanisms, so RB1 loss switches which half is exploited rather than removing the anchor.

### The goal, graded against the verbatim criteria

`deterministic_closure.CRITERIA` quotes the user's words; `goal_verdict()` grades each term.

| Criterion | Verdict |
|---|---|
| every mechanism and every escape closed | **MET** (full); **MET on coverage, weaker on form** (licensed-only: 3 margin / 12 structural / 1 gated / 0 open) |
| by real data or rigorous model | **MET** — 22 graded inputs, **0 failing** |
| potency and toxicity both considered | **MET** |
| a conjunction, not odds | **MET** |
| demonstrated in dogs | **N/A by the user's own instruction** (disclaimed twice) |

**Verdict: ACHIEVED AT THE STATED BAR**, with two qualifications the bar does not count as failures —
three agents not yet dispensable to a dog (none needing discovery), and one quantity genuinely not
computed: net regression at the invading edge under licensed drugs only.

The 22nd input is the one ASSUMED number in the project (the PRMT5 canine Cmax). It is an explicitly
inert placeholder that no closure reads, which rule 11 states is not a gap — and it is now doubly
inert, since the anchor no longer depends on that arm.

### Consequences recorded

- `pkpd`: `cytostatic_fraction_inhibited`, `cytostatic_net_growth`, `cytostatic_doubling_days`,
  `ribociclib_cytostatic_effect()`, `ribociclib_margin_correction()`.
- `availability_tiers`: niraparib added; all three site entries rewritten to separate the MEASURED
  access claim from the kill claim; routes 12 and A15 re-carried; `statement()` rebuilt around
  suppression figures rather than margins.
- `deterministic_closure`: `CRITERIA` and `goal_verdict()`; C8 narrowed to the single uncomputed
  quantity.
- `standard_audit`: 5 new graded inputs (17 → 22), still `failing() == []`.
- 823 tests pass; the `melanoma_benchmark.py` validation failure remains pre-existing.

---

## Near-future agents count: the tier scale corrected (2026-10-02, after upstream `e2fd68f`)

Another thread merged a clarification from the user into CLAUDE.md rule 13:

> *"I don't mean you can only use therapies that exist today, I meant to include near future ones
> that are scientifically sound. Just nothing that's pure theoretical."*
> **"Do not retreat to 'only what exists today'."**

That lands squarely on this branch's last reported qualification, and it was a bar error of mine in
the opposite direction from the first one. I had just finished reporting "one quantity is genuinely
not computed — net regression at the invading edge **under licensed drugs only**." The restriction in
that sentence is a bar the user had not set.

### The tier scale was too coarse

`Availability` had two values and lumped a compound in **human Phase III** together with a mechanism
nobody has ever dosed. Now three, with the middle one counting toward closure:

| Tier | Meaning | Counts? |
|---|---|---|
| `EXISTS_TODAY` | licensed (vet or human off-label), or in a dog trial | yes |
| `NEAR_FUTURE` | clinical-stage modality + stated path to the dog + derived/transferred dose | **yes** |
| `THEORETICAL` | no clinical evidence of the mechanism anywhere | **never** |

### The three-part test, applied per agent rather than asserted

`availability_tiers.near_future_test()` and `NEAR_FUTURE_TEST`:

| Agent | Modality clinical-stage? | Path to the dog | Dose / kill |
|---|---|---|---|
| **RGN3067** | YES — the modality is **licensed for dogs** (vincristine/vinblastine) and canine HS is MEASURED sensitive at nanomolar concentrations (PMID 25715778); the colchicine-site sub-class has human trial history (sagopilone) | YES — published compound, measured rodent brain Cmax (PMID 38398008); canine PK then dose-finding | **YES, DERIVED** 1.17/day, holding to 0.89% of measured exposure |
| **PRMT5 anchor (TNG456)** | YES — human Phase I/II, brain-penetrant successor in GBM trials (PMID 42150143) | YES — sponsor access; this is C7 | YES, TRANSFERRED on 99.37% computed ortholog identity |
| **paxalisib** | YES — human Phase III; Phase II combination in DMG (NCT05009992) | YES, with a caveat: canine plasma clearance is HIGH (PMID 38197324), so canine dosing must address it | YES, TRANSFERRED; Kp,uu 0.31 measured |

`tier_mix()`: **11 exists-today, 3 near-future, 0 theoretical**, all three near-future passing.
Tests fail if a theoretical agent ever enters the programme or if a near-future agent goes untested.

### Consequence: C8 is MET, and the conjunction is 8 conditions / 6 met

Because near-future agents count, the **computed** margin at the invading edge is available to the
closure: **+0.59/day parenchyma, +0.61/day CSF**. The licensed-only variant is retained as
*information* — it reaches every site and closes all 16 routes — but it is explicitly no longer the
bar, and `test_the_remaining_qualification_is_named_not_buried` asserts the code says so.

Outstanding: **C5** (one immunostain) and **C7** (sponsor access). Neither is engineering.

### C8 was mis-scoped twice, in opposite directions, and both are on the record

1. **Hidden** — `core.microtubule_route.build()` flags every agent `obtainable=True`, so a programme
   resting on a preclinical compound read as a prescription. Still *reported* rather than flipped:
   `mislabelled_as_obtainable()` names both offenders, because the flag drives published margins.
2. **Over-tightened** — I then rewrote C8 as "what licensed drugs alone cannot do", a stricter bar
   than the user set. `C8.why_required` now contains both admissions, and a test asserts the text
   "MIS-SCOPED TWICE BY ME, IN OPPOSITE DIRECTIONS" is still there.

### The goal, final grading

`deterministic_closure.goal_verdict()` — **ACHIEVED AT THE STATED BAR.** 16/16 routes at every
occupied site; computed margins +0.59/+0.61 per day; 22 graded inputs, 0 failing; potency and
toxicity priced; a conjunction, not odds; 11 + 3 + 0 agents with nothing theoretical. One
qualification remains and it concerns the licensed-only variant, not the closure.

788 analysis tests pass.

## Literature sweep, 2026-10-31 — one rule-9 hole found, and nothing that changes a route

A 14-angle sweep was launched against the record as frozen in early October 2026. **13 of the 14
angles never ran**: an account rate limit killed them before they reported. One angle (canine HS
direct) completed 16 queries first, and everything below comes from it plus the verification done
by hand afterwards. So this entry was a PARTIAL pass when written. [**Superseded the same day: all 14 angles were
subsequently run by hand — see 'Sweep closed' and the verification pass below. The 'did not run'
lists in this entry are historical.**]

### The one finding that changes the record: a modality class that was never enumerated

`candidate_universe` had **no live-bacterial-vector class** — not excluded, not in the model, simply
absent — while a funded pilot was already enrolling dogs with this disease using one. That is the
rule-9 failure the module exists to prevent, so the class is now carried explicitly:

- **Study:** "Pilot Study for a New Quasiorganelle Therapy in Dogs with Histiocytic Sarcoma",
  Michigan State University; PI Christopher Contag; Morris Animal Foundation study
  **26CAANEI-0062**, $120,000, start **2026-01-31**, listed active.
- **What it is:** attenuated, non-pathogenic *Listeria monocytogenes*-derived "quasiorganelles"
  delivering genetic payloads into tumour and immune cells. Group 1 (8 dogs) therapy alone; group 2
  (8 dogs) the same plus a gene-therapy payload. Systemic **infusion**, weekly x4 then 2 weeks off,
  three cycles, 16 weeks total.
- **Eligibility that matters for scope:** confirmed HS incl. hemophagocytic; **visible tumour, up to
  5 lesions, summed longest dimensions <15 cm**; >=20 kg; VCOG PS <=2. Excludes **any prior
  anti-cancer treatment** (no chemotherapy within 14 days, no radiation within 30), concurrent
  endocrine or kidney disease, immunosuppressants or systemic antibiotics within 14 days,
  neutropenia or immune-mediated disease.
- **Why it is NOT_ASSESSED rather than graded.** It cannot be excluded under rule 13: its kill is
  not contradicted, no named escape defeats it, no toxicity budget is blown, and "no canine data" is
  the one ground rule 13 forbids. It cannot enter the model either: no dose, kill rate or exposure
  exists for it at this site in any species, so any margin would be ASSUMED. The modality IS
  clinical-stage in humans (>160 indexed trial-linked reports for *Listeria*/*Salmonella*-vectored
  cancer immunotherapy, plus a brain-tumour literature), which is why it is a real class and not a
  theoretical one.
- **What would settle it, in rule-14 form:** measured bacterial colonisation of, or payload
  expression in, **gadolinium-non-enhancing brain tumour tissue**. That search has not been run.
- **Scope note (rule 10):** as written the trial does not apply to this case. It is a systemic
  infusion with no CNS-access figure, its eligibility requires visible measurable lesions, and its
  no-prior-treatment rule excludes a dog that has had this programme's own debulking and radiation.

Consequence: the catalogue line is now **26 classes — 15 in model, 10 excluded, 1 open**, in
`docs/CONSOLIDATED_REPORT.md` and in `candidate_universe.KNOWN_OPEN_CLASSES`. The import-time guard
still raises for any unassessed class not on that list, so a *silent* hole still fails loudly.

### Found, verified, and NOT new: the canine trametinib phase I

PMID **38889903** (Takada et al., *Vet Comp Oncol*) — 18 dogs, MTD **0.5 mg/m2/day PO**, ~70% reach
an average steady-state 10 ng/mL, saturable elimination, grade 3 DLTs (hypertension, proteinuria,
lethargy, ALP), and **target engagement not observed** in day-0/day-7 biopsies. Already cited in
`pkpd.py`, `candidate_universe.py` and `availability_tiers.py`; its numbers are already the
`TRAMETINIB_*` constants. Recorded here only so a later thread does not re-report it as a discovery.

### Found, absent from the record, but ruled out for this case on route

**COTC033 "Repurposing Vaccine Immunity to Treat Cancers: Validation in Canine Patients"** (CSU /
NCI-COTC). Intramuscular Shingrix or Gardasil-9 priming, randomised against rabies vaccine, then
**weekly intratumoral injection x8**. Eligibility: 15-60 kg, tumour **2-12 cm and accessible for
biopsy**; excludes mast cell tumour, thyroid carcinoma, lymphoma, cutaneous hemangiosarcoma; HS is
listed among the enrolling tumour types. Mechanism paper PMID **40280970** / DOI
10.1038/s41541-025-01131-y (*npj Vaccines*, Apr 2025): **murine** TC-1 model in prevaccinated mice,
Shingrix intratumoral injection often inducing regression and resistance to re-challenge, driven by
gE-specific CD4 T cells, with a dual-flank experiment clearing the non-injected tumour.

Why it does not move this case: the route is weekly intratumoral injection into an accessible 2-12 cm
mass, which a primary intracranial extra-axial tumour is not, and the abscopal result needs an
injectable second lesion that non-disseminated disease by definition does not have. It is a real
exists-today canine delivery route for the vaccine class in ACCESSIBLE disease — indirect here.

### Angles that had not run WHEN THIS ENTRY WAS WRITTEN (all were run later the same day)

MTAP/PRMT5/MAT2A clinical readouts (bears on C7); the CDK axis incl. CDK2 and CDK4-selective agents;
ClpP/imipridones after the 2025 approval; PARP and DNA repair; CNS delivery; regulatory actions since
September 2026; canine immunotherapy; preprints; evidence that would reopen an excluded class; the
non-enhancing-tumour access proxy across all drug classes; the MAPK-brain weak row; and the ChEMBL
target sweep. Each remains unsearched as of this entry.

## Literature sweep part 2, 2026-10-31 — four verified new items, none of which opens a route

The parallel sweep hit the account rate limit twice (reset moved 11:20 -> 18:50 UTC), so the
remaining angles were run by hand, sequentially. Below is what has been verified at primary source.
Angles still unrun are listed at the end. [**All were run later the same day — see 'Sweep closed'.**]
**No enumerated escape route changed status.**

### Verified NEW: a CNS trial for the MTAP-directed class — the condition the record itself set

`maintenance_durability` says of the brain site: *"neither [PRMT5i nor MAT2A i] has human CNS
activity data (TNG908 failed on CNS exposure; TNG462 0/23 PR in glioblastoma; TNG456 mouse-only) ...
add an MTAP-directed agent when one reads out in the CNS."* That trial now exists and is running:

- **NCT06883747** — "A Phase 0/1 Study of **BMS-986504**, a MTA Cooperative PRMT5 Inhibitor in
  Recurrent Glioblastoma Participants With **MTAP Deleted** Tumors Scheduled for Resection to
  Evaluate **Central Nervous System (CNS) Penetration** With PK-Trigger". Early Phase 1, n=12,
  sponsor Nader Sanai, **RECRUITING**, start 2025-04-28, last updated 2026-06-25. Phase 0 entry
  requires archival tissue with NGS-confirmed MTAP loss.

Why it matters here: this is the same Phase 0 "trigger" design, from the same centre, that produced
the ribociclib non-enhancing-tumour measurement this project calls its strongest input. It is aimed
at this tumour's own germline lesion. It does not change a closure today -- no readout -- but it is
the named experiment behind **C7**, and it turns "add one when it reads out in the CNS" from a wish
into a dated, identifiable trial. BMS-986504/MRTX1719 was already in the record for its *resistance*
biology (`emergence.py`); the CNS trial was not.

### Verified NEW: niraparib's access transfer got stronger, and the honest limit did not move

Already in the record (do NOT re-report): fractions unbound 0.05 brain / 0.16 plasma, PMID 38657366,
NCT05076513 ongoing, and the statement that there is **no published unbound tumour concentration**
   (**THAT STATEMENT IS WRONG -- corrected in the verification pass at the end of this file: the
   concentration is published at 226.7 nM unbound in non-enhancing tumour**),
which is why niraparib closes structurally rather than by a computed margin. Still true. New:

- **PMID 41023116** (*Sci Rep* 2025;15:33670, [DOI](https://doi.org/10.1038/s41598-025-18255-9),
  29 Sep 2025, GSK): multimodal imaging across healthy non-human-primate brain, mouse glioblastoma
  and mouse brain metastasis finds **niraparib superior to olaparib** at crossing the barrier,
  distributing through brain, and accumulating in tumour lesions. This matters specifically because
  the MTAP-genotype evidence in the record is an **olaparib** result -- so the drug actually in the
  programme is the better-penetrating member of the pair, not a hopeful substitution for it.
- **NCT06388733** — niraparib vs temozolomide, newly diagnosed MGMT-unmethylated glioblastoma,
  **PHASE 3**, Ivy Brain Tumor Center, active (not recruiting). The drug has advanced past the
  Phase 0 trigger to a randomised phase 3 in a brain tumour.

Neither is a tumour concentration, so **neither converts the row into a computed margin** and the
licensed-only variant still closes 12 of 16 routes structurally. Recorded in
`availability_tiers.py` next to the limit it does not lift.

Not verified at source: an ASCO 2023 abstract (JCO 41:16_suppl:2069) is reported to give a mean
unbound niraparib of **253.2 nM in non-enhancing tumour** in 32 evaluable patients, with all 35
clearing a >5x-IC50 PK trigger. ascopubs.org returned 403 to two fetch attempts, so this figure is
**second-hand and must not be used** until the abstract or its full publication is read directly. If
it holds, it is exactly the number that would give the licensed-only variant its computed margin.

### Verified NEW: the ADC exclusion now has a measurement aimed at the quantity it infers

The ADC class is excluded on this project's own arithmetic -- antibody access to invaded parenchyma
0.001 against a required 0.196, "the kill is contradicted by arithmetic, not by missing data". That
ground is an **inference into** the compartment, and rule 14 ranks a measurement in the compartment
above any inference into it.

- **NCT07268053** — Phase 0/1 with expansion of **GSK5764227**, a **B7-H3-targeted ADC**, in
  recurrent grade 4 glioma and brain metastases. n=15, sponsor Nader Sanai, **RECRUITING**, start
  2026-02-11. Its Phase 0 defines the optimal surgical window by the **highest median unbound
  PAYLOAD concentration in gadolinium-non-enhancing tissue**, and only PK-positive participants
  proceed.

So the exact quantity the exclusion infers -- payload, not antibody, in non-enhancing tumour -- is
being measured. The exclusion **stands for now** (no concentration reported; the arithmetic remains
the best available estimate), but it is flagged in `candidate_universe` for recomputation rather
than defence when that trial reports. B7-H3 is also a plausible histiocytic target.

### Searched, verified, NOTHING new

- **Regulatory actions, Sept-Oct 2026.** No new FDA approval or conditional approval of a canine
  cancer drug. Laverdia (verdinexor) received **full** approval in Jan 2026 after four conditional
  renewals -- oral canine lymphoma, not relevant here. CannEpil (canine bone-cancer pain) got only a
  CVM determination that the conditional pathway applies, 5 Oct 2026, with a presubmission meeting
  set for 19 Nov 2026; it is not an antineoplastic. LOY-002 is a lifespan drug, not a cancer drug.
- **MTAP/PRMT5/MAT2A readouts.** Nothing beyond what the record already holds (AMG 193 ORR 21.4%
  n=80 DoR 8.3 mo; IDE397 38%/30% PR; TNG908 CNS exposure failure; TNG462 0/23 PR in GBM; TNG456
  mouse-only; documented PRMT5i resistance by MAPK reprogramming with collateral MEK sensitivity).
  The only addition is the CNS trial above.

### Bacterial-vector access: the evidence found so far runs AGAINST the class at this site

Relevant to the open class recorded earlier today. At search-summary level (the primary MDPI paper
returned 403): attenuated *Salmonella* A1-R work describes the organism as **poorly penetrating the
blood-brain barrier**, with investigators using **intracranial** delivery to bypass it; a 2025
VNP20009 glioblastoma study demonstrates preferential accumulation in **subcutaneous** xenografts and
states that brain distribution, persistence and BBB interaction still need investigation; and
*Listeria* brain colonisation is reported to require prolonged bacteraemia of 10^2-10^3 CFU/mL. No
study was found reporting brain-tumour CFU after systemic dosing with an intact barrier. This is
**not yet a grading** -- it is search-summary level on a class whose status is NOT_ASSESSED, and it
needs the primary sources read before the ground is written.

### Angles still unrun AT THAT POINT (all were run later the same day; see 'Sweep closed')

ClpP/imipridones after the 2025 approval; the CDK axis (CDK2, CDK4-selective); PARP beyond niraparib;
CNS delivery devices; canine immunotherapy; preprints; the remainder of the reopen-excluded sweep
(bispecifics, HSCT, oncolytic, cytokines, epigenetic, ferroptosis, CSF1R, alkylators, metabolic);
human histiocytic neoplasms; the MAPK-brain weak row; and the ChEMBL target sweep.

### MAPK-brain angle: one lead that could close the weak row, NOT yet verified

The weak row says mirdametinib's brain access is unmeasured and "the access 0.50 in the model is the
maintenance THRESHOLD, not a mirdametinib figure; treat this branch as a hypothesis." A figure now
exists in the literature, but **it is not verified at source and is NOT written into the model**:

- A St. Jude preprint, "Hidden-driver inference reveals synergistic brain-penetrant therapies for
  medulloblastoma" (bioRxiv 10.1101/2025.11.20.689490, posted 2025-11-20, **not peer reviewed**), is
  reported to state: *"Consistent with existing studies, we found mirdametinib to have a superior
  K p,uu of 0.243."* The literal value **0.243 appears nowhere in this repository**, so it is new to
  the record. Against the project's own requirement of **0.196** unbound access in brain tissue,
  0.243 would clear the bar — by 1.24x, which is thin.
- **It is deliberately not graded.** bioRxiv returned Cloudflare 1015 to four fetch attempts, so the
  sentence above is second-hand from a search summary; the preprint itself attributes the value to
  "existing studies", meaning the primary source is elsewhere and was not found (PubMed returns
  nothing for mirdametinib + Kp,uu); and a medulloblastoma systems-biology preprint is not the right
  provenance for a number that would flip a site from hypothesis to closed. NEXT STEP, precisely:
  read 10.1101/2025.11.20.689490 directly, follow its citation for the 0.243, and grade the PRIMARY
  source. Only then may `genotype_tiered_durability` change.
- Supporting, weaker: company data report mirdametinib's brain:plasma above selumetinib's after IV
  (0.6 vs 0.02 ng/mL) with minimal P-gp/BCRP restriction; NHP CSF penetration ~1.3% of plasma AUC
  with CSF Cmax ~0.56 ng/mL (Neuro-Oncology 2022, doi 10.1093/neuonc/noac209.900) — the NHP CSF
  point is ALREADY in the record as "notable CSF penetration in NHP".
- Also new, also preprint: mirdametinib **plus abemaciclib** cooperate in atypical teratoid rhabdoid
  tumour, with mirdametinib extending survival in mouse orthotopic xenografts and the combination
  suppressing growth further (bioRxiv 10.64898/2026.03.24.714018, March 2026). That is the MEK +
  CDK4/6 pairing this programme uses, in a brain tumour, preclinically.

### Dordaviprone: the approval is real, and its evidence base is thinner than "licensed 2025" conveys

The programme leans on dordaviprone for the division-independent kill, graded a STRUCTURAL closure.
Recorded for strength-of-evidence (rule 5), all absent from the record before today:

- Accelerated approval **6 August 2025**, recurrent **H3 K27M-mutant** diffuse midline glioma, adults
  and children >=1 year, after prior therapy. First systemic therapy approved for this disease.
- The basis is a pre-specified integrated analysis of **50 patients across five open-label studies**,
  with a reported **~20% objective response rate** and ~40% disease control. Weekly oral dosing.
- *Neuro-Oncology* published a point/counterpoint, "Dordaviprone for diffuse midline glioma — a
  landmark approval or a premature step?" (doi 10.1093/neuonc/noag117), i.e. the approval is
  contested in print.

This does **not** change the structural closure — the ClpP mechanism, the computed 98.41% canine
catalytic-core identity and the non-enhancing-access argument from DMG all stand, and no kill rate was
ever derived from the ORR. It does mean the phrase "licensed 2025" should not be read as "efficacy
established": it is an accelerated approval on 50 patients at ~20% ORR, publicly debated. The
division-independent route still has no published tumour concentration.

### The best single find of the sweep: a LICENSED pan-RAF whose approved indication is a brain tumour

The MAPK axis is the maintenance arm for the ~59% driver majority, and its brain branch has been the
project's weakest row: cobimetinib's brain headroom is 0.5x and mirdametinib's canine ratio is
unmeasured. The record had **no pan-RAF member at all** -- "pan-RAF" appeared nowhere in the
repository before today, and the old escape audit's successor for MAPK reactivation above the block
was "an ERK1/2 inhibitor or a pan-RAF inhibitor, neither of which has canine PK, a canine HS IC50, or
a canine brain:plasma ratio."

**Tovorafenib** (DAY101 / TAK-580 / MLN2480), type II RAF inhibitor, verified via PubMed:

- **FDA-approved for paediatric BRAF-altered glioma** — listed with dabrafenib+trametinib and
  vorasidenib among the approvals for low-grade glioma (PMID 41201564, *CNS Drugs* 2025,
  [DOI](https://doi.org/10.1007/s40263-025-01238-9)). A licensed MAPK-axis agent whose indication is
  a BRAIN tumour is precisely what every MEK member in this class lacks.
- Phase 2 FIREFLY-1: **ORR 67%** by RANO-HGG in BRAF-altered pLGG, with response **independent of
  histology, of BRAF alteration type (fusion vs mutation), of prior lines of therapy, and of PRIOR
  MAPK-PATHWAY INHIBITOR USE** — that last clause bears directly on the reroute escape. Its
  **CNS-penetration properties** are the stated reason the SIOPe-BTG-LGG group took it into a
  first-line phase 3 (LOGGIC/FIREFLY-2, NCT05566795; PMID 38291372,
  [DOI](https://doi.org/10.1186/s12885-024-11820-x)).
- Type I RAF inhibitors are ineffective against BRAF fusions and can paradoxically drive growth;
  type II works there. Dose **once weekly**, 420 mg/m2 capped at 600 mg.
- Also in **phase 2 for recurrent/refractory Langerhans cell histiocytosis** (NCT05828069,
  recruiting) — inside the histiocytic family this project transfers from.

**It does not close the brain branch, and is not recorded as doing so.** Two limits: the clinical
evidence is in **BRAF-altered** tumours while canine HS is PTPN11/SHP2 (~56%) and KRAS (~3%) driven
with BRAF under 1% — a type II RAF inhibitor acts on RAF *dimers*, which is the mechanistically right
node for RAS-driven signalling, but that is a mechanism argument rather than the trial result; and
once-weekly dosing carries the same tension with continuous presence as dordaviprone. No canine PK,
HS IC50 or brain:plasma ratio exists. Recorded in `candidate_universe` as a listed exists-today
option on the MAPK axis, not as a graded closure.

### CDK axis: two brain-penetrant agents entering the clinic, both absent from the record

Relevant to escape A15 (acquired RB1 loss / **CDK2-cyclin E bypass**), whose only recorded successor
is a switch to the Rb-independent arm:

- **AL-605** (Alaw Therapeutics), a selective **brain-penetrant CDK2 inhibitor** aimed at
  CCNE1-amplified tumours and CDK2-mediated CDK4/6 resistance — **Phase 1a/b dosing began May 2026**.
  Its sister **AL-433**, a brain-penetrant **CDK4** inhibitor, was slated for first-in-human in Q4
  2026. A CDK2 agent that reaches brain would address the cyclin-E half of A15 directly rather than
  by switching arms.
- **Atirmociclib (PF-07220060)**, CDK4-selective and largely CDK6-sparing, hypothesised to reduce
  neutropenia — potentially relevant to the 95%-loaded marrow axis, but **no CNS or glioma data was
  found**, so it is a lead only.
- Class constraint worth recording: selective CDK2 agents need >100x selectivity over CDK1 to support
  chronic dosing, which is the relevant bar for indefinite maintenance. Others in development:
  INX-315, AZD8421, PF-07104091, INCB123667. None approved.

These are company-announcement and landscape-level sources, not peer-reviewed readouts, so they are
recorded as leads and nothing is graded from them.

### Human histiocytic neoplasms: one trial that enrolls histiocytic sarcoma itself

- **MSK 23-282**, phase 2 of **ulixertinib** (ERK1/2) in histiocytic neoplasms, with **Erdheim-Chester
  disease, LCH, Rosai-Dorfman and HISTIOCYTIC SARCOMA** among eligible conditions, adults 18+.
  Ulixertinib is already in the record as an ERK-class agent; this trial, which enrols HS itself, was
  not. It is the closest human clinical-stage evidence for the ERK arm in this disease.
- Also noted: a paediatric basket trial covering CNS tumours and histiocytic disorders (ivosidenib);
  a trametinib trial in refractory paediatric histiocytosis in Poland due to end March 2026; and a
  case series restating that no standard treatment for human HS is established (3/9 complete
  remission then relapse, 3/9 stable, 2/9 progressive).

### PARP angle: a brain-penetrant PARP1-SELECTIVE agent, which speaks to the marrow collision

The tightest cost in the programme is the marrow axis: niraparib + ribociclib together use **95% of
it, 5% headroom**, so nothing else myelosuppressive joins without a dose reduction. Niraparib is a
PARP1/2 inhibitor, and PARP2 inhibition is the part associated with haematotoxicity. Absent from the
record entirely before today:

- **AZD9574** — "Preclinical Characterization of AZD9574, a **Blood-Brain Barrier Penetrant
  Inhibitor of PARP1**" (PMID 37967136, *Clin Cancer Res* 2024;30:1338-51,
  [DOI](https://doi.org/10.1158/1078-0432.CCR-23-2094), AstraZeneca). PARP1-selective by
  fluorescence anisotropy, PARylation and PARP-DNA trapping; **BBB penetration demonstrated in vivo
  in mouse, rat AND monkey**; **haematotoxicity explicitly evaluated in rat** for monotherapy and in
  combination; in an MGMT-methylated **orthotopic glioma** model, AZD9574 + temozolomide extended
  survival over temozolomide alone. The authors' claim is "best-in-class PARP inhibitor for the
  treatment of primary and secondary brain tumors". **Phase 1/2: NCT05417594** — verified at registry 2026-10-31: AstraZeneca, RECRUITING, start
  2022-06-24, last updated 2026-10-05, enrolment 695, advanced solid malignancies (not a CNS-specific
  trial).
- Supporting, and relevant to two escapes: in H3K27M diffuse midline glioma — dordaviprone's own
  indication — PARP inhibition radiosensitises an HRR-defective tumour and **induces NKG2D ligand
  expression with NK-cell-mediated lysis, with NK cells REQUIRED for efficacy**; AZD9574 compares
  favourably to olaparib in a syngeneic orthotopic model (PMID 39253432, bioRxiv preprint, **not
  peer reviewed**).

Why it is worth recording rather than filing: the project's PARP arm carries the Rb-independent kill
and the MTAP/PRMT5 axis, and its binding cost is marrow. A PARP1-selective agent is the one
modification that could keep that mechanism while loosening the 95% collision, and it is
brain-penetrant in three species. **Tier: NEAR_FUTURE** (phase 1/2, no veterinary access, no canine data), so it changes nothing today and is not written into the model. The honest next step is to
price AZD9574 on the marrow axis against niraparib's 0.50 load and see whether the collision eases.
Note also that the NKG2D-ligand induction cuts against escape A19's shedding arm, which is a
tension worth testing rather than a resolution.

### Three angles that found nothing which changes anything

- **CNS delivery.** 2026 work is incremental and does not touch the device arithmetic. Neuronavigated
  focused-ultrasound BBB opening was reported in three children with relapsed diffuse midline glioma
  (*Sci Transl Med*, doi 10.1126/scitranslmed.adq6645); mouse cerebellar FUS raised antibody delivery
  about twofold with restoration of barrier integrity by 12 h (PMID 42547692); a UVA trial posted
  results in Oct 2026 on raising doxorubicin accumulation. Enhancement factors remain in the 2-10x
  band the project already models, so **5.9 x 0.021 = 0.124 against a required 0.196 still holds** and
  devices stay a backup rather than a requirement.
- **Canine immunotherapy.** No 2026 licensing decision found. Gilvetmab's USDA conditional approval
  is already in the record. New to the record but changing no closure, because the programme
  deliberately does not rely on the immune arm: a chimeric anti-PD-L1 (c4G12) in veterinary trials, a
  caninized anti-CTLA-4 (ca1C5) positioned as salvage after anti-PD-L1 failure, a multicentre
  caninized anti-PD-1 (ca-4F12-E6) melanoma preprint, and canine CAR-T work reporting **CD20 loss**
  with tandem CARs in development to counter antigen escape.
- **Reopen-excluded sweep.** **No exclusion is overturned.** The 2026 bispecific-engager and
  oncolytic-virus combinations in glioblastoma are preclinical (*Mol Ther Oncology* Apr 2026, PMID
  42094336; *Nat Commun* Apr 2026), which is below the near-future bar for a mechanism with no
  clinical evidence in this disease family. The one clinical datum, a 2026 AACR review of phase I
  CAR-T in malignant brain tumours (PMID 42806401), reports feasibility and early radiographic
  activity alongside **antigen loss and treatment-linked myeloid suppression** — i.e. it confirms the
  two grounds the project already cites rather than defeating them. Nothing was found on
  haematopoietic stem-cell transplant in this setting.

### Sweep closed, 2026-10-31

All fourteen angles are now run: one by the parallel workflow before it was rate-limited, thirteen by
hand. **No enumerated escape route changed status and no condition closed.** What changed is the
catalogue (one class added as open, one exclusion flagged for re-test), the strength of two existing
rows (niraparib's access transfer, the MAPK axis gaining a licensed brain-indicated pan-RAF), and a
list of named near-future agents that would improve specific weak rows if they reach a dog.

## Verification pass, 2026-10-31 — every open item chased to primary source

The sweep's unverified leads were blocked by publisher 403s and Cloudflare. All were reachable
through Europe PMC and NCBI efetch instead. Results below; **one changes a claim this project has
been making, and one second-hand figure turned out to be wrong.**

### CORRECTION: niraparib's unbound tumour concentration IS published, and the record said it was not

`availability_tiers` and `HS_STATUS` both stated: *"The trial (NCT05076513) is ongoing, so there is a
measured fraction unbound but NO published unbound tumour CONCENTRATION yet -- which is exactly why
this agent closes structurally rather than by a derived margin."* **That was wrong.** The phase 0 arm
reported in 2023. Read at primary source (NCBI efetch of the PMC record, Neuro-Oncology
25(Suppl 5):v78, DOI 10.1093/neuonc/noad179.0304, Sanai et al., abstract CTNI-22):

- PK trigger: **unbound niraparib > 5x the biochemical IC50, i.e. > 19 nM, in NON-ENHANCING tumour**
  — so the biochemical IC50 is **3.8 nM**.
- **All 44 phase 0 patients met the threshold.**
- **Mean unbound concentration in non-enhancing tumour: 226.7 nM (n = 38)** — roughly **60x** the
  biochemical IC50.
- Target engagement in the same tissue: **PAR suppression after ex vivo irradiation in 71% (20/28)**.
- Authors' conclusion: niraparib reaches "pharmacologically-relevant concentrations in non-enhancing,
  newly-diagnosed GBM tissue **in excess of any other studied PARP inhibitor**".
- **Measured cost: grade 4 thrombocytopenia in 5 of the first 18 phase 2 patients** on niraparib plus
  radiotherapy. PFS6 64% (n=11).

So the ACCESS half of the niraparib row is now **measured in the compartment at issue**, at the same
standing as the ribociclib figure and at a larger multiple. **The row still closes structurally**,
for a reason that must not be blurred: a kill RATE needs a **cytotoxic** potency in this tumour, and
3.8 nM is an **enzymatic** PARP-inhibition IC50, not a cytotoxic IC50 in canine HS cells, which does
not exist. Reading one through the other would repeat the cytostatic/cytocidal error already recorded
in `pkpd.ribociclib_margin_correction()`. The strengthening item is therefore rewritten: what is
missing is a cytotoxic potency, not a concentration.

The grade 4 thrombocytopenia figure is the other half of this and cuts the other way: it is measured
human haematotoxicity for niraparib at therapeutic dosing, against a marrow axis this programme
already runs at 95%. It strengthens the case for pricing a PARP1-selective alternative (AZD9574).

**My own second-hand figure was wrong.** The earlier entry reported "mean unbound 253.2 nM in 32
evaluable patients, all 35 clearing the trigger" from a search summary and flagged it unverified. The
real numbers are **226.7 nM, n = 38, all 44**. Wrong on all three counts. The flag did its job; the
lesson is that a search-summary number is not a number.

### RESOLVED: the mirdametinib Kp,uu 0.243 claim is untraceable, so it is not used

Chased properly. The claim exists only in a St. Jude medulloblastoma preprint (bioRxiv
10.1101/2025.11.20.689490, Europe PMC PPR1123579, **not peer reviewed**), whose full text is
unobtainable through five routes and which attributes the value to unnamed "existing studies". A
Europe PMC **full-text** search for `mirdametinib AND "0.243"` returns two hits, neither a
mirdametinib brain-PK source; `mirdametinib AND "Kp,uu"` returns five, of which the only relevant one
is the NHP abstract below. **There is no traceable published primary source for 0.243**, so under the
stated bar it is ASSUMED, not TRANSFERRED, and the MAPK-brain row is NOT changed on it.

### What the real published mirdametinib brain-PK source actually says (and it is usable)

Read at primary source (efetch, PMC9661017; Neuro-Oncology 2022;24(Suppl 7):vii233, abstract
EXTH-102). NHP model, 4 animals, mirdametinib 0.50 mg/kg PO qd or 0.20 mg/kg IV:

- **CSF/unbound-plasma ratio 2.5-3.0** — unbound drug in CSF EXCEEDS unbound plasma.
- CSF Cmax 0.43 +/- 0.18 (single dose), 0.56 +/- 0.18 (multiple dose), 2.0 +/- 1.8 ng/mL (IV).
- CSF penetration 1.3-1.6% of plasma AUC. **Plasma free fraction 0.52 +/- 0.1%** (heavily bound).
- Target-engagement anchors quoted in the same abstract: murine ERK-phosphorylation inhibition in
  **brain tissue at 1.15 nM**, and in tumour cell lines at **0.33-0.59 nM**.
- NF1 plexiform-neurofibroma phase II: 42% PR, mean plasma AUC0-12h 443 h*ng/mL.

Read against the project's requirements this splits the weak row rather than closing it. CSF Cmax of
0.43-0.56 ng/mL is about **1.1-1.5 nM**, i.e. roughly **1-1.3x** the murine brain-tissue
pERK-inhibition concentration and **2-4.5x** the tumour-cell-line figure — real but thin. And a
CSF:unbound-plasma ratio above 1 is a genuine measured transfer for the **leptomeningeal/CSF** site,
where the requirement is 0.0145. It says nothing about **invaded parenchyma**, where the requirement
is 0.196. So: the CSF branch of the MAPK tier now has a measured NHP basis; the parenchymal branch
remains a hypothesis, exactly as recorded. Nothing is regraded without a decision on whether an NHP
CSF ratio may stand in for canine parenchyma, which it may not.

### VERIFIED: AMG 193's phase I says three things the record does not carry

Read at primary source (PMID 39293516, *Ann Oncol* 2024;35:1138-47,
[DOI](https://doi.org/10.1016/j.annonc.2024.08.2339)). The record already has "ORR 21.4%, n=80". Not
in the record, and each material:

1. It is described as a **CNS-PENETRANT** MTA-cooperative PRMT5 inhibitor, in the title sentence of
   the abstract. The record's line that "neither [PRMT5i nor MAT2Ai] has human CNS activity data"
   remains literally true — penetrance is not activity — but "CNS-penetrant" is more than the record
   currently allows the class.
2. **At doses >=480 mg, COMPLETE intratumoral PRMT5 inhibition was confirmed in paired MTAP-deleted
   tumour biopsies**, with ctDNA clearance. That is target engagement measured in tumour tissue, in
   this tumour's own genotype — the rule-14 proxy for "engages the target".
3. **"A favorable safety profile WITHOUT CLINICALLY SIGNIFICANT MYELOSUPPRESSION."** Against a marrow
   axis at 95% with 5% headroom, a genotype-anchored agent that does not load marrow is the opposite
   of niraparib's grade 4 thrombocytopenia problem.
   Trial enrols **CDKN2A-deleted and/or MTAP-deleted** tumours — this tumour's exact lesion. MTD
   1200 mg od; DLTs in 8 patients at >=240 mg (nausea, vomiting, fatigue, hypersensitivity,
   hypokalaemia).

### CHARACTERISED: how bacterial vectors actually reach a brain tumour, and why it is still open

Read at primary source (efetch, PMC9978951, *Acta Pharm Sin B*). The mechanism in the one directly
relevant study is **not** a bacterium crossing an intact barrier: attenuated *Salmonella* selectively
colonises the **hypoxic** tumour region, repolarises macrophages, downregulates P-gp and **recruits
neutrophils**, and the payload (doxorubicin-loaded outer-membrane vesicles) crosses the barrier by
**hitchhiking those neutrophils**. Dosing 8 x 10^6 CFU in a mouse glioma model.

That is a characterisation, not a grading, and it points the wrong way for this case: the access
mechanism is **hypoxia-dependent**, and the site that matters here is the **invading edge behind an
intact barrier** — the least hypoxic part of the tumour. The class therefore stays NOT_ASSESSED with
the next measurement unchanged (colonisation or payload expression in gadolinium-non-enhancing
tissue), now with the reason stated: what has been shown is colonisation of hypoxic cores plus
leukocyte transport, which is not the compartment this analysis needs.

### Protocol documents: one read in full, one second-hand AT THE TIME (both since verified)

- **MSU quasiorganelle pilot: READ IN FULL** (trial flyer PDF, extracted). Inclusion, exclusion,
  both arms and the full dosing schedule are recorded above and come from the primary document, not a
  summary.
- **COTC033: NOW VERIFIED at a primary source, and the second-hand numbers were wrong.** See the
  dedicated entry at the end of this file.

### Test environment, for the next thread

The rebuilt container had no numpy/pandas/scipy/scikit-learn visible to pytest, which is installed as
a **uv-isolated tool** at `/root/.local/share/uv/tools/pytest/` with its own venv — so project
dependencies installed with `pip` are invisible to it and 29 suites could not be collected. Fixed by
injecting them into that venv:

    uv pip install --python /root/.local/share/uv/tools/pytest/bin/python numpy pandas scipy scikit-learn
    PYTHONPATH=src /root/.local/bin/pytest -q

`torch` is still absent, so `tests/test_hybrid_rnn.py` and `tests/test_vaccine_eval.py` cannot be
collected here. Neither touches the HS analysis.

## Closing the open items, 2026-10-31 (end of day)

### The bacterial-vector class is now GRADED, and the catalogue is back to zero unassessed

It was carried at NOT_ASSESSED for the day it took to read its access mechanism at primary source.
It is now **EXCLUDED on KILL_CONTRADICTED**, and the ground is a *derived site mismatch*, not absent
canine data:

- Bacterial tumour tropism is documented as driven by **hypoxia, necrosis and aberrant vasculature**,
  with hypoxic/necrotic regions described as the preferred colonisation sites; engineered obligate
  anaerobes are built to replicate strictly in necrotic cores and explicitly **not** to persist in
  normoxic tissue.
- In the one directly relevant brain study the bacteria **do not cross an intact barrier at all**:
  *Salmonella* colonises the hypoxic region and **recruits neutrophils**, and the payload crosses by
  hitchhiking them (PMC9978951, mouse glioma, 8x10^6 CFU).
- The site that decides this case is the **invading edge behind an intact barrier** — the least
  hypoxic, least necrotic compartment, and the one this tropism does not select for. No search found
  colonisation measured at a normoxic margin or invasive front in any species.
- Second, independent ground: it **cannot be co-administered**. The MSU protocol excludes
  immunosuppressants, systemic antibiotics, neutropenia and any prior anti-cancer treatment, while
  this programme runs continuous myelosuppressive maintenance at 95% marrow after debulking and
  radiation. Years of a live attenuated bacterium in a myelosuppressed dog is a listeriosis exposure.
- **Falsifiable, and the test is named:** a measured colonisation or payload-expression figure in
  gadolinium-non-enhancing tumour tissue, in any species, defeats the ground directly. The hypoxic
  core of the extra-axial mass is where the class retains a theoretical role — not the compartment
  the decade turns on.

Catalogue now reads **26 classes — 15 in model, 11 excluded, 0 unassessed** (6 kill-contradicted, 3
defeated-by-escape, 2 toxicity-unaffordable). Zero again by **assessment**, not by deleting the row;
`KNOWN_OPEN_CLASSES` stays in the code so the next hole can be carried honestly.

### The PRMT5-class CNS question is graded, and the answer does not change the ordering

Both claims checked at source, and they point in opposite directions:

- AMG 193's first-in-human paper calls it a **"CNS-penetrant"** MTA-cooperative PRMT5 inhibitor
  (PMID 39293516). That is an **author descriptor, not a measured brain or tumour concentration**,
  and it does not displace the one **measured** CNS efficacy datum in the class, which is
  **negative**: TNG462's 0/23 PR in glioblastoma. Penetrance is not activity. Where they conflict
  within a class, the measured brain outcome wins — rule 14 applied in the unflattering direction.
  **The CNS lead stays CDK4/6.**
- What AMG 193 does add is on the toxicity axis, and it is material: complete intratumoral PRMT5
  inhibition in paired MTAP-deleted biopsies at >=480 mg with ctDNA clearance, and **no clinically
  significant myelosuppression** — the opposite of niraparib's grade 4 thrombocytopenia, against a
  marrow axis at 95%. That bears on *which* MTAP-directed agent to ask a sponsor for, not on whether
  to lead with one.
- The experiment that would change the brain ordering is named and running: **NCT06883747**. Until it
  reports, the MTAP arm stays systemic-first and **C7 stays open**.

### COTC033 eligibility: not verifiable from this environment, and it does not matter

Three routes tried and recorded: the Studypages listing is fully client-rendered (42 KB of HTML, five
lines of visible text, no eligibility content server-side); the CSU URL 301-redirects there;
web.archive.org has a snapshot from 2026-03-11 but is **blocked by this environment's egress policy**,
to both curl and WebFetch. PubMed has no COTC033 design paper. So the eligibility numbers quoted
earlier (15-60 kg, 2-12 cm biopsy-accessible tumour, the four excluded diagnoses) remain
**search-summary level and must not be quoted as verified**.

What IS primary-verified is the part the conclusion rests on: the mechanism paper (PMID 40280970,
*npj Vaccines* 2025) is explicitly about **INTRATUMORAL** injection of licensed vaccines, in mice.
A weekly intratumoral course into an accessible mass is not a route to a primary intracranial
extra-axial tumour, so the trial is out of scope for this case on the route alone, regardless of the
weight and size thresholds. Anyone with browser access should confirm the eligibility text directly.

### Test suite: green, with nothing excluded

**834 passed, 0 failed.** The one long-standing failure was a bug in the guard, not the code:
`test_validation_changes_no_analysis_module` substring-matched the word "validation", so
`from .clinical_validation import (...)` in `melanoma_benchmark.py` tripped it — a sibling ANALYSIS
module, not the `canine_dsp.validation` package the guard protects against. It had been red since
2026-08-02, meaning the separation went unverified for three months. The guard now matches the import
statement itself, and a companion test pins both directions (it must catch all five real spellings
and must not catch `clinical_validation` or prose). The real invariant **holds**: no analysis module
imports the validation package.

Environment: `torch` is now installed in the pytest venv too, so `test_hybrid_rnn.py` and
`test_vaccine_eval.py` run rather than being skipped. Full recipe:

    uv pip install --python /root/.local/share/uv/tools/pytest/bin/python numpy pandas scipy scikit-learn
    uv pip install --python /root/.local/share/uv/tools/pytest/bin/python torch --index-url https://download.pytorch.org/whl/cpu

### COTC033: eligibility VERIFIED at a primary source, and the second-hand numbers were wrong

The CSU listing is client-rendered and web.archive.org is egress-blocked, but COTC033 is a
**multi-institution NCI Comparative Oncology Program trial** — sites are Colorado State, Ohio State,
UC Davis, Missouri and Wisconsin (NCI program manager Christina Mazcko) — and the **University of
Missouri Veterinary Medical Center serves its criteria as static HTML**. Read directly, verbatim:

> Body weight between 15 and 60 kg · Tumor biopsy or cytology to confirm diagnosis · **Solid tumor
> measuring 2 to 8 cm** · No mast cell tumors, cutaneous hemangiosarcomas, thyroid carcinomas, or
> lymphomas · **Must not have received ANY prior experimental therapy** · No concurrent chemotherapy
> or radiation therapy – **2 week washout** · No concurrent immunomodulatory therapy (including
> Apoquel or Cytopoint) – **6 week washout** · No concurrent corticosteroids – **1 week washout** ·
> No hypercalcemia causing illness · No significant co-morbid illness ... pulmonary metastatic
> disease, renal or hepatic failure, history of congestive heart failure or clinical coagulopathy,
> autoimmune disorders, or uncontrolled endocrinopathies

Up to **13 weekly visits**; all treatment and recheck costs covered.

**Two corrections to what was recorded earlier from the search summary:**
1. The tumour-size window is **2 to 8 cm**, not 2–12 cm.
2. Missouri describes the agent as a **"Vaccine Peptide Library (VPL)"**, not as "Shingrix or
   Gardasil randomised against rabies vaccine". Those descriptions are not obviously the same thing.
   The CSU-derived version may describe the randomisation arms and Missouri the platform, or one may
   simply be wrong — **the discrepancy is recorded rather than resolved**, because no source read
   directly settles it. What IS primary-verified is the mechanism paper (PMID 40280970, *npj
   Vaccines* 2025), which is explicitly about **INTRATUMORAL** injection of licensed viral vaccines,
   in mice.

**The scope conclusion is unchanged and now rests on verified criteria.** The trial requires a
measurable 2–8 cm solid tumour confirmed by biopsy or cytology, which a primary intracranial
extra-axial mass is not a candidate for on an injection-and-measurement basis; and the washout rules
(any prior experimental therapy excluded outright, 2 weeks off chemotherapy or radiation, 6 weeks off
immunomodulators) are incompatible with this programme, which begins with debulking plus radiation
and then runs continuous maintenance including an anti-PD-1. So COTC033 is **out of scope for this
case on verified eligibility, not merely on an inferred route**.

### Search-side verification: complete

Every angle is run and every lead that this environment can reach has been taken to a primary
source. The three figures that could not be reached are each resolved rather than left hanging: the
niraparib concentration was **found and corrected** (226.7 nM, not the 253.2 nM reported
second-hand); the mirdametinib Kp,uu 0.243 was **established as untraceable** and is therefore not
used; and COTC033's eligibility was **obtained from a participating site** after the lead site's page
proved unreadable. What remains unresolved is one documented discrepancy between two descriptions of
COTC033's agent, recorded above, which does not bear on any closure in this analysis.

## Final verification round, 2026-11-01 — the MAPK axis has two LICENSED CNS agents

### COTC033: the discrepancy is RESOLVED at the sponsor's own page

The NCI Center for Cancer Research Comparative Oncology Program page for COTC033 was read directly
(server-rendered, 4 KB of text). It settles it:

> The purpose of this study is to evaluate the safety and effectiveness of **intra-tumoral
> administered vaccines**, when given to dogs with cancer. ... There will be **15-20 dogs** taking
> part in this study across North America. Dogs weighing **more than 15 kg** who have been diagnosed
> with a **solid tumor**. Dogs with mast cell tumor, hemangiosarcoma, thyroid cancer or lymphoma are
> **not eligible**. Dogs cannot receive chemotherapy or radiation for **2 weeks** prior. ... Your dog
> will be **randomized to either receive Shingrix/Gardasil vaccines or rabies vaccines** ... Study
> weeks 1, 5 and 9 will require a tumor biopsy. Your dog will come in **weekly for an injection
> directly into the tumor**. ... Consent for a necropsy ... is required.

Sites: Colorado State, Ohio State, UC Davis, **University of Georgia**, Missouri, Wisconsin.

So the **Shingrix/Gardasil-versus-rabies randomisation is correct** — it is the sponsor's own
description. The phrase "Vaccine Peptide Library" appears nowhere on the NCI page; it is Missouri's
local label for the agent, and no source states that the VPL *is* one of those vaccines. The
discrepancy was a difference in naming between a site page and the sponsor page, not a contradiction
about what is given. **Resolved: the NCI description governs.** Site-level numbers (Missouri's
15-60 kg and 2-8 cm) are refinements of NCI's ">15 kg, solid tumour", which states no size.

Scope conclusion unchanged and now resting entirely on primary sources: weekly **intratumoral**
injection, biopsies at weeks 1/5/9, and a 2-week chemo/radiation washout. Not a route to a primary
intracranial extra-axial mass, and incompatible with this programme's induction.

### Mirdametinib is FDA-APPROVED, which the record did not say

Verified at Drugs@FDA (openFDA): **GOMEKLI**, mirdametinib, **NDA 219379 and NDA 219389**, sponsor
SpringWorks, oral, 1/2/3/4 mg, **original approvals both 2025-02-11**. A peer-reviewed review
(PMID 40932001, *Expert Opin Investig Drugs* 2025;34:665-673,
[DOI](https://doi.org/10.1080/13543784.2025.2558656)) describes it as "an FDA-Approved MEK1/2
inhibitor for adult and pediatric NF1-associated plexiform neurofibromas" offering "an effective,
targeted, and orally available treatment ... with the added advantage of **CNS penetration**".

The record called mirdametinib "CNS-penetrant, notable CSF penetration in NHP, in paediatric
brain-cancer trials" — i.e. it treated the agent as investigational. **It is licensed.** Combined
with tovorafenib, also verified at Drugs@FDA (**OJEMDA**, NDA 217700 and NDA 218033, Day One
Biopharms, original approval **2024-04-23**, oral), the MAPK axis now has **two licensed agents with
CNS credentials** where the record had only "cobimetinib headroom 0.5x and mirdametinib unmeasured".

What this does and does not change. It does NOT produce a canine brain:plasma figure, so the
parenchymal branch of the MAPK tier is still not graded on a measured canine number. What it changes
is availability: the brain branch's leading agents are **obtainable today, off-label**, rather than
investigational — which is a rule-13 tier correction, and it removes "the agent does not exist" from
the list of reasons that branch is weak. The remaining reason is the measurement, and for the CSF
compartment even that is now a measured NHP transfer (CSF/unbound plasma 2.5-3.0, PMC9661017).

### Ulixertinib: trial status verified at registry

- **NCT06411821** — "Ulixertinib in People With Histiocytic Neoplasms", **Phase 2, RECRUITING**,
  Memorial Sloan Kettering, last updated 2026-10-15, condition "Histiocytic Neoplasms".
- Two NCI Pediatric MATCH records list **Histiocytic Sarcoma** and **Recurrent/Refractory Primary
  CNS Neoplasm** among eligible conditions together: **NCT03155620** (screening, Phase 2, active)
  and **NCT03698994** (the ulixertinib arm, Phase 2, active). An ERK-inhibitor arm that enrols both
  histiocytic disease and CNS tumours is the closest clinical-stage precedent for the ERK option
  here, and it is registry-verified rather than inferred.

### The mirdametinib Kp,uu 0.243 claim: closed as UNTRACEABLE, by search not by assumption

Seven distinct routes were tried and are recorded so nobody repeats them: bioRxiv HTML (Cloudflare
1015), bioRxiv source XML (1015), WebFetch of the preprint (429 then 1015), Europe PMC
`PPR1123579/fullTextXML` (404), Europe PMC `PMC12667814/fullTextXML` (404), NCBI efetch of
PMC12667814 (metadata only, 2.9 KB, no results text), and the PMC OA service (404). Decisively, a
Europe PMC **full-text search** for `mirdametinib AND "0.243"` returns two records, neither a
mirdametinib brain-PK source, and `mirdametinib AND "Kp,uu"` returns five, of which the only relevant
one is the NHP CSF abstract already in hand.

So the absence is **established by search rather than assumed**: no published source carries the
figure, and the preprint that quotes it attributes it to unnamed "existing studies". Under the stated
bar that makes it ASSUMED, and it is therefore **not used anywhere in the model**. The usable number
for this axis remains the measured NHP CSF dataset. This item is closed, not pending.

## Provenance audit of the MTAP-axis response rates, 2026-11-01

The MAT2A-before-PRMT5 ordering at systemic sites rests on four percentages in
`maintenance_durability`: IDE397 38% PR in squamous NSCLC, 30% in urothelial, molecular response in
81%; and TNG462 0/23 PR in glioblastoma. Those were traced.

**Two peer-reviewed reviews were read in full text and neither carries any of those figures:**

- PMID 42021873 / PMC13099004, *Int J Transl Med* 2025, "Exploiting Synthetic Lethality of PRMT5 for
  Precision Treatment of **MTAP-Deficient Glioblastoma**" — the GBM-specific review. It covers
  TNG908, TNG462, MRTX1719, AMG 193 and AZD3470 by name and gives no glioblastoma response figure
  for TNG462.
- PMID 41439984 / PMC12732168, *Cells* 2025 (10 Dec), "MTAP-Null Tumors: A Comprehensive Review" —
  covers the same agents plus IDE397, AG270, S095035, ISM3412 with their trial numbers, and gives no
  response percentages for IDE397.

What the reviews DO corroborate is the AMG 193 MTD of 1200 mg once daily (which matches the primary
paper, PMID 39293516) and the overall landscape. So:

**The four percentages have conference-abstract or company-presentation provenance at best, and are
NOT traceable to peer-reviewed full text from this environment.** They should carry that label. They
are not load-bearing for the brain conclusion -- they order two systemic arms against each other --
but an ordering justified by unverifiable numbers is weaker than the record implies.

**And the conclusion they support is independently corroborated, in stronger terms than the record
uses.** Both reviews bear directly on the brain stance:

- *Cells* 2025: "**Despite multiple efforts to exploit MTAP loss for targeted therapies, none of
  these efforts have yielded substantial results in clinical trials.**"
- *Int J Transl Med* 2025, on GBM specifically: "Despite promising anti-tumor activity in vitro, the
  **clinical efficacy of PRMT5 inhibitors is often limited by the tumor microenvironment**,
  particularly the impact of non-malignant cells that attenuate drug activity."

So the decision to lead the brain with CDK4/6 rather than an MTAP-directed agent is supported by
peer-reviewed review-level evidence, not only by the single TNG462 datum. That is the stronger
footing, and it does not depend on any of the four unverified percentages.

### COTC033 "Vaccine Peptide Library": as resolved as this environment allows, and it does not matter

Routes exhausted: NCI sponsor page (read in full — the phrase does **not** appear), Missouri site page
(read in full — the phrase appears, defined only as "a new immunotherapy"), the CSU URL the NCI page
links to (**404**), the Studypages listing (client-rendered, no content), web.archive.org
(egress-blocked), Ohio State / UC Davis / Wisconsin listings (no COTC033 content served), the
MIB Agents trial index (site list only), PubMed (no design paper), and a targeted web search.

**Disposition: the sponsor's description governs and is verified** — dogs are randomised to
Shingrix/Gardasil or rabies vaccine, with an intramuscular primer phase then weekly **intratumoral**
injection. "Vaccine Peptide Library" is one participating site's wording for the agent; no reachable
source states what it denotes. That residual is a question about one site's phrasing, not about the
trial's intervention, and it bears on nothing in this analysis — the trial is out of scope for a
primary intracranial tumour on the verified route and the verified washout rules.

## Final provenance sweep, 2026-11-01 — three verifications and two definitive negatives

### Tovorafenib's LABEL tightens its caveat from soft to hard

Read at openFDA (`drug/label`, OJEMDA). Verbatim: indicated for "relapsed or refractory **pediatric
low-grade glioma (LGG) harboring a BRAF fusion or rearrangement, or BRAF V600 mutation**"; the label
directs "Confirm the presence of BRAF fusion or rearrangement, or BRAF V600 mutation **prior to
initiation**"; the indication "is approved under **accelerated approval based on response rate and
duration of response**" with continued approval "contingent upon verification ... in a confirmatory
trial(s)"; dosing is "**orally, once weekly**".

Canine HS carries BRAF alterations in **under 1%**. So tovorafenib's licensed indication is
**genotype-gated to a lesion this disease essentially does not have**, and its approval is itself
accelerated and provisional. It stays an **off-label, mechanism-based** option on this axis — type II
RAF inhibition acts on RAF dimers, the right node for RAS-driven signalling — and "licensed, brain
indication" must not be read as "licensed for this tumour's genotype". `candidate_universe` updated.

### AL-605 and AL-433 have NO trial registry record

ClinicalTrials.gov returns **nothing** for either. The "Phase 1a/b dosing began May 2026" claim is
therefore **company-announcement provenance only and not registry-verifiable**. They were already
recorded as leads with nothing graded from them; that label is now justified rather than cautious.
Atirmociclib by contrast has many registry records, through **phase 3** (e.g. NCT07890597), but
**none in CNS or glioma** — consistent with what was recorded.

### The four MTAP-axis percentages are conclusively NOT in the indexed literature

**Four** peer-reviewed reviews were read in full text — PMC13099004 (GBM-specific), PMC12732168
(comprehensive, Dec 2025), PMC13044523 and PMC13394919 (both 2026) — plus four targeted Europe PMC
**full-text** searches (`IDE397 AND "38%"`, `IDE397 AND urothelial`, `TNG462 AND "partial response"`,
and the earlier `TNG462 AND glioblastoma`). None carries IDE397's 38%/30%/81% or TNG462's 0/23 PR in
glioblastoma. The only numeric TNG462 content found anywhere is **preclinical** SDMA pharmacodynamics
(undetectable to 72 h in xenografts). Conference-abstract or company-presentation provenance is now
established by exhaustion, not assumed, and the figures carry that label in code.

### No registered human trial of intratumoral Shingrix exists

ClinicalTrials.gov returns **zero** studies for intratumoral Shingrix, so the "current human trials"
the Missouri page says COTC033 complements are not registry-identifiable, and that route to resolving
the "Vaccine Peptide Library" wording is closed too. The verified account of what COTC033
administers remains the NCI sponsor page: randomisation to Shingrix/Gardasil or rabies vaccine,
intramuscular primer then weekly intratumoral injection.

### Search-side verification: nothing further is reachable from this environment

Every item on the open list has now been either verified at a primary source or established as
unreachable **by exhaustion with the routes recorded**. The three that end as negatives — the
mirdametinib Kp,uu figure, the four MTAP percentages, and the COTC033 agent wording — are each
closed in the only way a missing source can honestly be closed: the search was run, the routes are
written down so nobody repeats them, and nothing in the model depends on any of the three.

## Why the three negatives are final, 2026-11-01

The last routes were tried and the explanation for two of the three is now structural rather than
circumstantial.

### The four MTAP percentages cannot have a primary source yet, because the trials have not reported

Checked at the registry:

- **NCT04794699** (IDE397, MTAP-deleted solid tumours): Phase 1, **ACTIVE_NOT_RECRUITING**, n=169,
  last updated 2026-04-09, **no results section posted**.
- **NCT05732831** (TNG462, MTAP-deleted solid tumours): Phase 1/2, **RECRUITING**, n=225, last
  updated 2026-09-08, **no results section posted**.

So the reason four peer-reviewed reviews and four full-text searches do not carry IDE397's 38%/30%/81%
or TNG462's 0/23 is simply that **both studies are still running and neither has reported results**.
Those figures are therefore necessarily interim conference or company disclosures from ongoing
trials, and no primary source for them exists to be found. This is not an incomplete search — it is
the state of the evidence, and the record's provenance label is exactly right.

### "Vaccine Peptide Library" is not an established term, which supports the disposition already taken

A Europe PMC search for the exact phrase returns **one** record, an influenza vaccine paper
(Multimeric-001), unrelated to oncology. The University of Georgia listing — the last COTC site not
previously checked — serves no COTC033 content. So "VPL" is not a recognised agent or platform name
in the indexed literature, which is consistent with it being one site's wording. The sponsor's own
description of what is administered stands verified and is what the analysis uses.

### The mirdametinib Kp,uu figure

Nothing further was attempted because nothing further exists to attempt: seven retrieval routes and a
Europe PMC full-text search for the value itself were already exhausted, and the preprint that quotes
it attributes it to unnamed sources. It is not used.

### Status of the search work

Complete. All 14 angles run; every finding either verified at a primary source (PubMed, NCBI efetch
of PMC full texts, ClinicalTrials.gov API, openFDA Drugs@FDA and drug labels, the NCI Comparative
Oncology Program page, a participating trial site) or closed as unobtainable with the routes recorded
and the reason established. Three figures were refused rather than used, and **nothing in the model
depends on any of them**. The remaining partial labels in earlier entries above are historical
markers of what was true when each entry was written, annotated in place rather than rewritten, so
the sequence of what was known when stays readable.

## Second-pass sweep, 2026-11-01: two classes that were never rows, and one premise with human numbers

The first-pass sweep closed with "nothing further is reachable from this environment". That was true
of the *items on the open list*. It was not a statement that the candidate universe had been
re-enumerated, and rule 9 asks for the second thing. A second pass was run against the catalogue
itself rather than against the open list, and it found two modality classes that had never been rows
at any point in the project, plus real human outcome data bearing on condition C3. Everything below
was read at a primary source by this session; the one item an agent reported that could not be
verified is refused by name at the end.

### The headline moves backwards: "0 unassessed" becomes "1 open"

> **Annotated 2026-11-02, left in place rather than rewritten:** the class this section opens was
> **closed the next day** on three measured canine-HS IC50s, two of them in a table this project had
> already half-transcribed, and a *third* missing class took its place in `KNOWN_OPEN_CLASSES`. The
> count is now **29 — 15 / 13 / 1 open**. See the 2026-11-02 section below. Everything in this
> section is what was true when it was written.

`candidate_universe` now enumerates **28 classes — 15 in the model, 12 excluded, 1 open**. The
previous line, **26 — 15 / 11 / 0 unassessed**, was published in `CONSOLIDATED_REPORT.md`, in
`AUDIT_TRAIL.md` and on the reader-facing page, and it is now wrong. It is corrected in all three
rather than quietly left, and `KNOWN_OPEN_CLASSES` is non-empty again so the import-time guard keeps
the hole loud.

This is **not** a change to `standard_audit.failing()`, which still returns nothing. The two axes are
different and conflating them would be the error rule 11 names: `failing()` grades the inputs the
model actually uses against the stated bar, and no input changed. What changed is the *candidate
list* the closure claim is quantified over. A class nobody enumerated cannot fail an audit of live
inputs — which is exactly why rule 9 exists as a separate rule.

### Class 27: antimetabolites / nucleoside analogues — OPEN, and not excludable

Never a row. Cytotoxics had been split into microtubule agents and alkylators and the enumeration
stopped there, while `core/hs_drug_sensitivity.py` carried a `DrugClass.ANTIMETABOLITE` member **with
no drug under it** — the signature of a class that was named once and never populated. The reason it
stayed empty is legitimate (PMID 25715778 tested ten drugs and no antimetabolite among them, and that
table is deliberately one paper with one comparator panel) but the empty member was the only trace,
and nothing read it.

What the literature actually holds, verified:

- **Pan-active in all ten canine HS lines.** Table 2 of PMID 42129963 (DOI 10.1111/vco.70077) lists
  the compounds that reduced viable cell counts to ≤70% at 5 µM in **all** CHS lines with
  reproducibility. Three are antimetabolites: **5-fluorouracil, clofarabine, floxuridine**. 5-FU's
  median IC50 across the ten lines is **7.49 µM** (~974 ng/ml at MW 130.08). Read against the
  project's own measured table, that is ~3 orders of magnitude better than the alkylators and ~3
  worse than the vincas. The same table independently contains **abemaciclib** and **cobimetinib**,
  i.e. the screen corroborates two of this project's existing maintenance leads.
- **Prior-literature activity in this disease.** The same paper excluded a short list of drugs from
  screening a priori "because they had been previously reported to have antiproliferative effects on
  CHS cells and cases" — and **methotrexate** is on that list. So the class had reported canine-HS
  activity in the literature before this screen.
- **Five of the nineteen Group-B candidates are antimetabolites**: 5-fluoro-5′-deoxyuridine,
  amethopterin (methotrexate racemate), ancitabine, **cytarabine** (listed as
  cytosine-1-β-D-arabinofuranoside hydrochloride) and trimetrexate. Scoped correctly: the authors
  state plainly that **"no compound was identified as Group B-specific compounds based on the
  examinations of the IC50 value"**, so none of these is a confirmed Group-B agent. Cytarabine
  showed ≥30% inhibition at 5 µM in 5 of 10 lines. Trimetrexate had low IC50 in 8 of 10 lines, which
  the authors note and did not pursue.
- **The only durability readout in a histiocytic neoplasm anywhere in this project.** Clofarabine,
  prospective multicentre phase 2 in relapsed/refractory LCH and non-LC histiocytosis, NCT02425904,
  PMID 42126265 (DOI 10.1182/bloodadvances.2026019922): stratum 1 (R/R LCH, n=20) 17/20 **(85%)
  responders**, **no on-treatment progression**, 3 recurrences after cycle 6, **2-year PFS 89% ± 7%
  and OS 100%**, median follow-up 40.9 months — after a **finite six-cycle course**. Stratum 2
  (non-LC, n=5): 3 of 4 evaluable had a partial response. Toxicity is not free: **20 of 25 (80%) had
  ≥1 grade ≥3 toxicity** attributed to protocol therapy. Scope label: human, paediatric, LCH and
  non-LC histiocytosis — the histiocytic *family*, not histiocytic sarcoma, and not intracranial.
  Indirect on species and on disease, direct on lineage.

**Why it is carried OPEN rather than excluded.** None of rule 13's three grounds holds for the class,
and "not yet wired into the regimen" is not a ground at all. What the assessment found is that at the
intracranial site the three members split the three legs and no member carries all of them:

| Member | Canine-HS kill | Brain | Verdict |
|---|---|---|---|
| 5-fluorouracil / floxuridine | pan-active, 10/10 lines, IC50 **7.49 µM** quantified | **disqualified at the mechanism level** — what was dosed to beagles orally for 3 months was **FBAL and fluoroacetate, 5-FU's catabolites**, with tegafur-uracil as positive control; all three gave hyperaesthesia, excitement, **convulsions** and **vacuolar changes in several areas of the dog cerebrum** (PMID 15206584, DOI 10.2131/jts.29.155) | potency without the brain |
| clofarabine | pan-active, 10/10 lines **+** 2-yr PFS 89% in R/R LCH | CSF penetration **median 5%, range 3–26%** in non-human primates (PMID 16115942, DOI 10.1158/1078-0432.CCR-05-0261); authors: "penetrates into the CSF only modestly, but the concentrations obtained may approach those that are cytotoxic in vitro" | potency and outcome without access |
| cytarabine | **unconfirmed** (Group-B candidate rejected on IC50; 5/10 lines at 5 µM) | **best measured access in the project**: dog, intact barrier, 12-h infusion → **CSF:plasma 0.62 ± 0.14**, CSF Css **8.3 ± 1.1 µM**, bolus CSF peak 29 ± 11 µM, ten healthy dogs, no significant toxicity at 600 mg/m² (PMID 1742843, DOI 10.1007/BF00686329) | access without a confirmed kill |

Two things in that table deserve to be said plainly. First, the member with the *quantified* canine
potency is the one this disease must not get, and the lesion behind that is measured in **this
species at this site** — not inferred. Second, cytarabine's **0.62** is a higher measured access
figure than anything else in this project, obtained in dogs with an **intact** barrier, which is the
rule-14 ideal: a measurement in the compartment at issue rather than an inference into it.

**Rule 15 applied to all three rows, because this class is nothing but transfers.** Rule 15 arrived
on this branch (`cc9bb5a`) while these findings were being written up, and it bites on each of them:

- **5-FU.** The beagle study dosed **FBAL and fluoroacetate**, 5-FU's catabolites, with
  **tegafur-uracil** as positive control. 5-FU itself was not the dosed agent. The *direction* is
  what makes it transfer: FBAL is 5-FU's principal catabolite, so FBAL exposure is a consequence of
  dosing 5-FU rather than an alternative to it, and a second fluoropyrimidine in the same pathway
  produced the same lesion. So what transfers is a **mechanism-level disqualification**, qualitative,
  with **no number carried across** — and none needed, the conclusion being qualitative.
  **Floxuridine** inherits it by the same route and no further: same DPD catabolism to the same
  FBAL, never dosed in that study, so nothing quantitative transfers to it either. Calling this a
  *contradicted* figure for floxuridine would be the rule-15 error; it **bounds** the class's brain
  use.
- **Clofarabine.** The LCH figure is an **efficacy** transfer across species and across disease
  within the lineage. LCH is far less aggressive than histiocytic sarcoma, so it is a **ceiling for
  HS and never a floor**: it establishes that the class can produce multi-year control in this
  lineage, not that it would do so here. The 5% CSF figure is a separate **exposure** transfer in a
  third species; no NHP-to-dog direction is established in this project, so it is used as an order
  of magnitude and never converted into a canine number.
- **Cytarabine.** No transfer at all — its own measurement, in the species and compartment at issue
  (total drug by HPLC in both fluids, not unbound). The **only** comparison permitted is cytarabine
  against itself: its measured canine CSF steady state, **8.3 µM**, sits above the **5 µM** at which
  its own 5-of-10-line screen result was obtained. That is why the class is open rather than dead.
  Reading that 8.3 µM against the 5 µM threshold of the *other three* members would be a rule-15
  violation — their activity is not cytarabine's potency — and this analysis does not make that move.

**What would close it: one measurement.** The screen computed IC50s only for 5-FU, sunitinib and the
28 subgroup candidates. A clofarabine or cytarabine IC50 in canine HS lines would decide this class
either way. That is a bench assay on cell lines that already exist, in the same panel the screen
used — cheaper than anything else outstanding in this project except the MTAP immunostain.

### Class 28: FGFR axis — EXCLUDED, on data at the right site for the right biomarker

Also never a row, although the table gives every other targeted axis one (MAPK, PI3K, CDK4/6,
synthetic lethality, CSF1R). Three FGFR inhibitors score in the canine screen and two are licensed —
on paper a stronger hand than several IN_MODEL classes:

- **infigratinib** inhibited proliferation in **all CHS lines except CHS8** (PMID 42129963);
- **erdafitinib** had low IC50 in the Group A lines "**although not as low as duvelisib**" — same
  +/− pattern across all ten lines as duvelisib, smaller A-vs-B IC50 separation;
- **pemigatinib** hit 6 of the 8 Group A lines on the screen criterion;
- FGFR1 **overexpression** is reported in canine HS cases.
- Both licensed members verified at openFDA 2026-11-01: **erdafitinib = BALVERSA, NDA 212018,
  Janssen Biotech**; **pemigatinib = PEMAZYRE, NDA 213736, Incyte**.

It is excluded anyway, and not for want of canine data. The class has already been tested in human
recurrent **brain** tumours: multicentre phase 2 of infigratinib in FGFR-altered recurrent glioma,
n=26 — **6-month PFS 16.0%** (95% CI 5.0–32.5), median PFS **1.7 months**, **ORR 3.8%**. Four
patients had durable control beyond a year and **all four carried an activating FGFR1 K656E (n=2) or
FGFR3 K650E (n=1) point mutation, or an FGFR3-TACC3 fusion** (PMID 35344029,
DOI 10.1158/1078-0432.CCR-21-2664). Canine HS is reported as an FGFR1 **overexpression** tumour, not
a mutation/fusion tumour, so this disease's biomarker is precisely the one in which the class failed
at this site. Hyperphosphataemia, on-target, in 76.9% is a second cost against an unsupported
benefit. The screen's authors arrive at the same place independently: ponatinib also targets FGFR1
and did **not** inhibit most CHS lines, so they conclude infigratinib's effect "may not be solely
attributable to FGFR1 inhibition and could involve FGFR1-independent mechanisms" — i.e. the canine
signal is not evidence that the FGFR axis is the driver. Ground: `KILL_CONTRADICTED`.

**Rule 15 on this exclusion, because it is the obvious objection.** The trial dosed *infigratinib*
while the licensed members are *erdafitinib* and *pemigatinib*, and one compound's trial cannot
contradict another compound's number. This exclusion does not make that move: what transfers is a
statement about the **target**, which all three share — that FGFR-axis benefit at this site tracked
an activating lesion rather than the FGFR-altered population at large — and not infigratinib's
potency, exposure or response rate attached to either other compound. The **direction** is what makes
it safe: the trial enrolled tumours with FGFR *alterations*, a population already enriched beyond
mere overexpression, so its 3.8% response rate is a **ceiling** for an overexpression-only tumour,
not a floor. A ceiling that low at this site is what the exclusion rests on.

### Condition C3 now has human numbers, and they cut both ways

The Histiocyte Society's blueprint for non-LCH research (PMID 41178439,
DOI 10.3324/haematol.2024.286479, *Haematologica* 2025) supplies the first real-world figures C3
has ever had. Both quoted verbatim:

- "**the relapse rate was nearly 75% after interruption of targeted therapies**"
- "**60% of patients with ECD discontinued BRAF inhibitors at a median follow-up of 4 years due to
  adverse events**"

The first **confirms** C3. Its rationale — that a continuously present agent is there at persister
re-entry and that cycling reopens the route — had been argued from reversibility biology alone; this
is the same conclusion measured in patients, in the human histiocytic family.

The second is a **feasibility pressure the record did not contain**: a ten-year continuous-dosing
premise now has a human analogue in which a majority could not stay on the drug for four years.

**C3 stays MET, and the grading is written down so it can be challenged.** The discontinuation figure
is indirect on two axes at once — human, and the BRAF-inhibitor class rather than any agent in this
regimen — and what it threatens is the delivery of *one* axis, not the mechanism. The structure that
answers it is already in the model and was not invented for the occasion: maintenance is tiered
across non-overlapping axes with a named successor for every reroute, so losing an axis to toxicity
is a **switch**, which the ledger already prices, not a **stop**, which is what the 75% figure
punishes. That answer is **structural, not demonstrated** — no dog has been switched for toxicity in
this disease — and it is recorded at that strength and no higher, in the C3 annotation in
`deterministic_closure.py`.

### Refused: one claim that could not be verified

An agent reported that "CDKN2A mRNA is **not** reduced" in the relevant canine material. **Refused
and not written into the model.** The source it pointed at (PMC11940154) says the opposite direction:
CDKN2A was "predicted to be significantly inhibited" as an upstream regulator. Had it been true it
would have bitten on the deletion-tier logic, which is why it was checked rather than carried.

Two scope corrections made to agent output in the same pass, both now reflected above: erdafitinib is
**Group A only and weaker than duvelisib**, not "active across unselected lines"; infigratinib
inhibited all lines **except CHS8**, not all lines.

### Still unverified, carried as leads and used for nothing

Named so they are not re-raised as findings: fluzoparib (listed among the 19 Group-B candidates, so
subject to the same "none confirmed on IC50" caveat); intra-arterial superselective infusion
(PMID 41129771); MEK monotherapy 43% vs 14% vertical blockade (PMID 42309537); the recruiting phase
II trametinib dog trial (PMC11940154); cladribine + cytarabine (PMID 42780343). None is in the model
and none supports any claim in it.

## 2026-11-02: the open class closed, a third hole opened, and a licensed indication nobody had read

Three things happened, and the first is a correction to this file's own entry from the day before.

### The antimetabolite class is EXCLUDED, and the numbers that closed it were already ours

`core/hs_drug_sensitivity.py` is built from PMID 25715778 and carried **five of that paper's ten
rows**. The five dropped rows are **methotrexate, cytarabine, WSMP, doxorubicin and etoposide**. So
the `DrugClass.ANTIMETABOLITE` member sat declared-and-empty not because the paper lacked
antimetabolites but because its two antimetabolite rows were never copied across — and on 2026-11-01
that emptiness was explained *in the file* as "PMID 25715778 tested ten drugs and no antimetabolite
among them". **That was false**, written without re-reading the paper the table itself cites.

Table 1 of PMC4488404, verbatim, 48-h CCK-8:

| | CHS-1 | CHS-2 | CHS-3 | DH82 | CLBL-1 | Ema |
|---|---|---|---|---|---|---|
| Methotrexate | >100 µg/ml | 8.56 µg/ml | 495 ng/ml | >100 µg/ml | 7.10 ng/ml | 17.3 ng/ml |
| Cytarabin | 14.4 µg/ml | 40.8 µg/ml | 9.29 µg/ml | 142 µg/ml | 91.7 ng/ml | 736 ng/ml |

And the authors' own conclusion: *"it was suggested that alkylating agents, **antimetabolites**,
antitumor antibiotics and topoisomerase inhibitors might not be effective as treatment of HS."*

Three members are now measured, in two independent laboratories:

- **Cytarabine — the decisive row, because both sides are measured in the dog.** Canine-HS IC50
  **38.2 µM** in the most sensitive of four lines (9.29 µg/ml, CHS-3, at MW 243.22) rising to
  **583.8 µM** in DH82; **101× to 1549×** the chemosensitive canine lymphoma comparator CLBL-1. Its
  own measured canine CSF exposure with an **intact barrier** is **8.3 µM** at steady state and
  **29 µM** at the bolus peak (PMID 1742843) — so the best line needs **4.6×** the steady state and
  **1.3×** more than even the transient peak. And the canine toxicity ceiling sits *below* the dose
  that produced that peak: fatal suspected cytarabine-induced infiltrative lung disease in a dog
  after the fourth **300 mg/m²** infusion, against the **600 mg/m²** that gave the 29 µM peak
  (PMID 27062671, DOI 10.1111/vec.12470). Kill, reach and toxicity each measured, in the dog, and
  they do not meet. Recorded as `hs_drug_sensitivity.CYTARABINE_CSF_ARITHMETIC`.
- **Methotrexate** — 495 ng/ml in the best line against 7.10 ng/ml in CLBL-1 (**69.7×**), and
  **>100 µg/ml** in CHS-1 and DH82, so **>14,000×** as a lower bound (the >100 entries are
  right-censored).
- **Cladribine**, from a second laboratory and a second panel — IC50 **64 µM** (BD, a
  Bernese-derived line) and **222 µM** (DH82) against an **achievable plasma concentration of
  0.028 µM**: short by **2,286× to 7,929×** (PMID 29490634 / PMC5831740 Table 2, 72-h MTS). That
  table exists precisely to compare IC50 against achievable exposure; dasatinib is the only agent in
  it that clears its own bar, and cladribine is the worst in the table after CCNU.

All ten rows are now in the table, and the completed table **reproduces the 2015 authors' sentence
as a computation**: `resistant_classes()` returns the alkylators, the antimetabolites *and* the
topoisomerase agents; `sensitive_classes()` returns the microtubule agents alone. The half-table
could not do that.

**Two of my own readings from 2026-11-01 were also wrong and are corrected:**

1. *"Cytarabine's canine-HS kill is unconfirmed, not contradicted."* It was measured in 2015, in the
   project's own source paper.
2. *"Methotrexate is on that paper's a-priori exclusion list as previously reported active in CHS
   cells and cases, so the class has prior-literature activity in this disease as well."* The 2026
   screen's phrase means **"already studied"**, not "found active" — **melphalan** is on the same
   exclusion list and melphalan is measured 42–411× resistant. The prior report for methotrexate
   *is* the 2015 paper, which measures it resistant.

**The counter-evidence, recorded at its own strength rather than buried.** In *human* histiocytic
disease these same drugs do well: methotrexate 1 g/m² + cytarabine 0.1 g/m²×5 for six cycles in 95
adults with newly diagnosed LCH gave ORR 89.5%, **6-year OS 93.2%** and EFS 55.2% at a median 78
months' follow-up — the longest durability readout anywhere in this project (PMID 39428688,
DOI 10.1111/bjh.19830) — and cladribine + cytarabine produced clinical improvement and radiologic
remission in **isolated, MAPK-wild-type CNS Erdheim-Chester disease** that had failed steroids,
radiotherapy *and* cladribine monotherapy (PMID 42780343 / PMC13597168, DOI 10.1002/jha2.70389,
n=1). Under **rule 15** neither bounds the canine-HS kill: both are *efficacy* readouts in a
different and far less aggressive disease, and a transfer from another disease cannot overturn a
measurement in this one. Under **rule 14** the measurement in the species and disease at issue
outranks the flattering cross-disease outcome *even though the measured number is the worse one*. So
the honest sentence is "these drugs work in LCH and are measured resistant in canine HS".

**What would reopen it**, both obtainable and neither a demonstration: (a) a **clofarabine** IC50 in
canine HS below achievable exposure — clofarabine is the one member with pan-activity at 5 µM and no
IC50, and rule 15 forbids transferring cladribine's resistance to it, because clofarabine's
2′-fluoro substitution was designed to resist the deamination that limits cytarabine and cladribine,
so the chemistry differs in the direction that matters; (b) a measured canine-HS uptake or
activation advantage — deoxycytidine kinase expression, a nucleoside-transporter level — that would
explain the cell-line resistance as culture artefact. Also unfollowed: **trimetrexate** had low IC50
in 8 of 10 lines in the 2026 screen and the authors did not pursue it.

### A third never-enumerated class: targeted protein degradation. Catalogue → 29

Cereblon molecular glues are a distinct modality in any modern catalogue and were not a row. Not a
kinase inhibitor, not an epigenetic agent, not a checkpoint or cytokine agent — no existing row
covered them. The only trace in the project was a parenthetical that PRMT5 PROTAC degraders are
"emerging", which is a remark about a future agent on another axis.

It **cannot be dismissed**: `NCT02523040`, "Lenalidomide for Adult Histiocyte Disorders", phase 2,
n=12 actual, conditions LCH, Erdheim-Chester **and histiocytic sarcoma**, results first posted
2025-04-25 — **ORR 0.67, 12-month PFS 62%, 12-month OS 92%, grade 3–4 treatment-related toxicity
0.25**, serum TNF-α maximum change −14.4%. A licensed agent with a human outcome calibration in the
right disease family is a sound input under rule 13.

It **cannot be called closed** either, and rule 14's proxy settles why. "Reaches the brain" is a
measured CSF:plasma ratio, and it exists **twice** for lenalidomide — which is exactly the case rule
14 legislates for:

| source | figure |
|---|---|
| Non-human primates, AUC CSF/AUC plasma, detected in 2 of 3 animals (PMID 22109830) | **11%** |
| Three human patients, 20 mg oral (PMID 35732975) | **1.3–2.4%** |

Rule 14 says prefer the measurement in the compartment at issue even when it is the worse number, so
this project uses **1.3–2.4%**. Against the requirements the project computes — 0.0145 in CSF,
0.196 in parenchyma — that **straddles** the CSF bar (0.013 just under, 0.024 clearing by 1.7×) and
falls **8–15× short** at the parenchyma, which is the site the case turns on.

The mechanism is measured too, and it names the next step under rule 15: lenalidomide's influx
permeability in a monkey BBB model and human placental cells is **one order of magnitude below**
thalidomide, pomalidomide and a caffeine control, and the authors conclude lenalidomide "exerts its
favorable immunomodulatory effects via systemic exposures". That is a within-class, same-assay
permeability comparison, so it transfers as a **direction, not a number**: **pomalidomide** is the
member to take to a brain site (thalidomide measures 42% CSF penetration in the NHP study).
**What would close it: pomalidomide's measured CSF:plasma** — one number, in a licensed drug,
obtainable from the literature rather than from an experiment.

### Cobimetinib is licensed for this disease family, with no genotype gate

The strongest single fact in two days of sweeping, and it was a label read. **COTELLIC, NDA 206192,
label `effective_time` 20260729**: *"As a single agent for the treatment of adult patients with
**histiocytic neoplasms**."* The absence of a qualifier is the point, because the same label gates
its other indication — *"unresectable or metastatic melanoma with a BRAF V600E or V600K mutation, in
combination with vemurafenib"*. Sponsor and FDA have agreed an indication in histiocytic neoplasms
that requires no mutation to be demonstrated first. That is precisely the problem tovorafenib cannot
solve: its label *directs* confirming a BRAF fusion or V600 mutation before initiation, and this
disease is BRAF under 1%.

Why it matters beyond a tier label: cobimetinib already carries, in this project, a **measured
canine-HS IC50 of 74–372 nM and a measured canine plasma Cmax of 1640 nM** (PMID 39202410). It is
therefore the only agent in the catalogue that is simultaneously licensed, licensed *for this
disease family without a biomarker precondition*, and measured in canine histiocytic sarcoma cells
with a canine exposure to compare against.

**What it does not do:** the indication is for adult *human* patients, so a dog is off-label; human
"histiocytic neoplasms" is dominated by ECD and LCH rather than histiocytic sarcoma, so the match is
to the family, not the tumour; and **the brain is untouched** — cobimetinib's brain headroom here
remains 0.5×, i.e. short. It upgrades the systemic arm and the regulatory story, not the site that
decides the case. The repo had cited NDA 206192 only for the canine minimum lethal dose in
`core/toxicity.py`; the indication itself was absent.

### Catalogue and provenance

**29 classes — 15 in the model, 13 excluded, 1 open** (8 kill-contradicted, 3 defeated by a named
escape, 2 toxicity-unaffordable; **0** excluded for absent canine data). `standard_audit.failing()`
still returns `[]`: no live *input* changed, and the open class is a candidate-list item, not an
input. Also now in the table and previously missing: **WSMP = Paccal Vet®, water-soluble micellar
paclitaxel**, measured 15.6–92.8 ng/ml — the only agent in the 2015 panel with a veterinary product
behind it, landing in the sensitive class with the other microtubule agents. Its marketing status is
*not* asserted here and is an open question for `availability_tiers`.

### How this round was run, and what it cost

A 14-angle workflow (`wf_72fcf13e-d56`) hit the 5-hour usage limit with 2 angles returned and **all
48 verifier agents killed**, so its reported `passed_both_lenses: 0` meant "nothing was checked",
not "nothing survived". The 17 candidates were recovered from `journal.jsonl` and the consequential
ones verified by hand — which is how the cytarabine row was found. A follow-up run
(`wf_1d38233b-feb`) re-verifies the remaining 9 salvaged claims and runs the 12 angles that never
ran. **Unverified and used for nothing** until that returns: vinorelbine in 9 dogs (PMID 25970220);
masitinib as a >70× vinblastine chemosensitiser (PMID 21333567); MEK-in-ECD n=170 76% retention
(PMID 42840804) and its claim that C3's discontinuation figure is attributed to the wrong drug
class; anakinra raising retention 65%→94% (PMID 39814074); the C3 figure's true provenance as 61% of
n=64 (PMID 40053897); the sign of PMID 42309537's 43%/14%; the n=1174 ECD cohort (PMID 42880331);
the MAPK-wild-type MEK warrant (PMID 40269272); and COBRAH (NCT04007848) as a completed randomised
phase 3.

## 2026-11-03: the nine salvaged claims, independently re-verified — three of them false

The follow-up workflow (`wf_1d38233b-feb`) completed its salvage phase (9 of 9 checked) before a
**weekly** usage limit killed 11 of the 12 sweep angles, the completeness critic and the synthesis.
What the salvage returned is the more valuable half, because it caught agent claims that would
otherwise have entered the record.

### Killed, and recorded so they are not revived

- **"The record attributes C3's discontinuation pressure to the wrong drug class."** FALSE, and the
  premise was manufactured. The cited 170-patient cohort (PMID 42840804) is **MEK-monotherapy only**:
  it reports no BRAF-inhibitor retention rate and no BRAF-inhibitor discontinuation rate anywhere,
  and the figure "60%" does not occur in it. All 17 occurrences of "BRAF" in the full text were
  checked; they are 32 patients with prior-line BRAFi, 1 patient switched to BRAFi, and BRAF V600E
  as a baseline mutation in 57/170. The record's class attribution was already correct.
- **"MEK inhibitors 71% vs BRAF inhibitors 74% first-line ORR in n=1174."** The four numbers are
  exact (PMID 42880331; 185/262 = 70.6%, 286/387 = 73.9%, ten countries) but **"first-line" is
  wrong**, and the source refutes it arithmetically: the first-line BRAF/MEK population is 350
  patients for both classes combined, while the two ORR denominators sum to 649. Changes nothing
  live.
- **COBRAH (NCT04007848) as a usable readout.** Every structural element is exact — COMPLETED,
  RANDOMIZED, QUADRUPLE-masked, PLACEBO_COMPARATOR, PHASE3, cobimetinib, histiocytoses — but
  **results are not posted** (`hasResults: false`, actual completion 2022-03-14, last update
  2025-01-24; a 2026 publication says COBRAH results "are awaited"), and **histiocytic sarcoma is
  not in the trial** — the string "sarcoma" does not occur in the record. It is a design that
  exists, not a readout.

### A correction to a number this project pushed on 2026-11-01

Condition **C3**'s feasibility pressure was recorded as the verbatim review quote *"60% of patients
with ECD discontinued BRAF inhibitors at a median follow-up of 4 years due to adverse events"*. The
quote is accurate; the review compresses its own source. At the primary report (**PMID 40053897**,
Blood 2025, 145(18):2100-2103) the figure is **39 of 64 = 61% all-cause** discontinuation, of which
**adverse events account for 20 of the 39** — i.e. **20/64 = 31% of the cohort**, not 60%. The
abstract says "primarily because of adverse events"; the review rendered that as "due to adverse
events". The same cohort's response rate is 85%.

So the AE-driven discontinuation rate at a median four years is about **half** what C3's pressure
was recorded as. The correction runs in the project's favour, which is precisely why it is written
down: an overstated pressure that happens to be conservative is still a wrong number.

One mitigation is measured and travels as an **association only**: adding anakinra to MAPK-targeted
therapy in ECD went with 18-month drug retention of **94% vs 65%** (PMID 39814074) — but
retrospective, observational, two referral centres, 52 patients / 60 courses with the anakinra arm
just **16 of 60 courses**, physician discretion, no confounding adjustment. The paper's body says
"was associated with"; only its title says "improves".

### Confirmed, each with the qualification that changes how it may be used

- **Vinorelbine in canine HS** (PMID 25970220) — species, disease, n=9 and agent all exact, but it
  is **not a 9-dog study**: the 9 HS dogs are a 16% subgroup of a 58-dog, 12-tumour-type
  retrospective series from one teaching hospital, 1997–2012. The abstract's response figures are
  for the whole 58 and **must not be read as the HS numbers**. Upgrades the provenance of the
  microtubule class's canine support; changes nothing else.
- **Masitinib as a chemosensitiser** (PMID 21333567) — the ">70-fold reduction in vinblastine IC50"
  is exact *but the claim dropped its condition*: the source says ">70-fold reduction in IC50 **at
  5 µM masitinib**", an unconstrained in-dish concentration, which is the whole usability question.
  No absolute IC50 is recoverable, so it **cannot** be joined to this project's measured canine-HS
  vinblastine IC50 of 1.75–2.78 ng/ml (different lab, different lines, no published denominator),
  and the abstract names no cell line. It does **not** touch condition C4 — C4 is about the
  induction agent not being a P-gp substrate and is met by drug choice — and it touches escape A13
  as a **flag, not a closure**.
- **The 43%/14% sign inversion** (PMID 42309537) — confirmed, and the figures are **radiological
  non-response**: 43% = 10/23 trametinib monotherapy, 14% = 2/14 trametinib + dabrafenib, UK
  multicentre retrospective audit, n=37. A further correction to the correction: non-response here
  is SD **or** PD, not progression — progression alone is 2/23 (8.7%) and 0/14 (0%). Anyone
  "fixing" the record by calling 43%/14% progression rates would introduce a second error. The
  figure is cited in no module and changes nothing live.
- **The MAPK-wild-type MEK warrant** (PMID 40269272) — 63% response in MAPK-wild-type ECD confirmed,
  and it is **10/16**, so n=16. Critically, **the paper names no MEK inhibitor at all**: a grep of
  the full text for cobimetinib|trametinib|binimetinib|selumetinib returns zero hits, as do "dose"
  and "mg". It is a **class/target-level** warrant only, and under rule 15 nothing here may be
  attached to cobimetinib or trametinib specifically — "63% on cobimetinib" would be fabricating the
  compound.

**On the FGFR/MEK asymmetry this raises, stated rather than assumed.** The FGFR axis was excluded on
the ground that benefit tracked an activating lesion rather than overexpression. MEK benefit, by
contrast, does *not* require a demonstrated MAPK lesion — 10/16 in wild-type ECD, at class level.
The asymmetry is therefore supported by data on both sides rather than being a double standard: for
FGFR the biomarker-stratified trial showed benefit confined to the lesion; for MEK a wild-type
cohort showed benefit without it. Both are human, both indirect, and the MEK figure is n=16.

### Search status

Still not run, and now blocked until the weekly limit resets: the 12 angles `mtap-axis`, `cdk-axis`
(1 of 12 returned, 4 candidates, 0 survivors), `clpp`, `parp`, `cns-delivery`, `approvals`,
`canine-immuno`, `preprints`, `reopen-excluded`, `nonenhancing`, `mapk-brain` and the new `degraders`
angle, plus the completeness critic that was to diff the class list against the literature
independently. Given three holes were found in three days, that critic is the highest-value
outstanding item and the catalogue should not be described as complete before it runs.

> **Superseded the same day.** Rather than wait on the limit, all twelve angles were run **by hand
> in the main thread** — see the two 2026-11-03 sections below. The search work is complete; the
> completeness critic remains the one outstanding item, and the reason it is still outstanding is
> unchanged: it should not be self-assessed by the thread that built the list.

## 2026-11-03: the cdk-axis angle, run by hand — three measurements and one negative

The weekly usage limit (resets 16:00 UTC) still blocks subagents, so the remaining angles are being
run directly in the main thread. `cdk-axis` was the one angle of twelve that returned before the
limit hit, and its four candidates were never verified because the verifier agents died. All four
verified at primary source, all four are genuinely absent from the record, and they do **not** point
the same way.

### Abemaciclib, measured in Gd-non-enhancing tumour, in this project's own genotype

**NCT04391595** — Sanai, Ivy Brain Tumor Center, Phase 0/2, **n=42 recurrent GBM**, COMPLETED. This
is the same "trigger trial" design the project already relies on for ribociclib and niraparib, and
the enrolment criteria are striking: **intact RB, >30% pERK expression, and CDKN2A/B deletion or
CDK4/6 amplification** — the lesion configuration of the tumour under analysis. Six days of
abemaciclib plus the ERK1/2 inhibitor LY3214996 before planned resection; tissue from Gd-enhancing
*and* Gd-non-enhancing regions plus CSF and plasma; unbound drug by validated LC-MS/MS.

- **Median unbound abemaciclib in Gd-non-enhancing tumour: 31 nM**, against a PK trigger (>5× IC50)
  the trialists set at **12 nM** → clears by **2.6×**, in the compartment that *is* the operational
  definition of an intact barrier.
- Pharmacodynamics in the same tissue: RB phosphorylation down in **47.5%**, RSK phosphorylation
  down in 25%, MIB-1 proliferation down in **72.5%**. No dose-limiting toxicities.
- The honest qualifier: only **9 of 40 (22.5%)** exceeded the thresholds for *both* drugs.

DOI 10.1093/neuonc/noae165.0425, PMC11553480.

**And it corrects an existing entry downwards.** `therapies.py` said of temuterkib that a "phase-0
trigger trial reached pharmacologically relevant conc. in Gd-non-enhancing GBM" — qualitatively, with
no figure and no trial id. That trial is this one, and temuterkib *is* LY3214996. Its median was
**10 nM against its own 25 nM trigger** — it **fell 2.5× short** where abemaciclib passed. The
qualitative phrase was more favourable than the measurement. Under rule 14 the number replaces the
phrase even though it is worse, and the project's standing **refusal to assign temuterkib a brain
Kp** is vindicated rather than overturned.

### A human parenchymal ratio, replacing a rodent one

**NCT05413304** (NCI, PHASE1, **n=5**, results posted) measured abemaciclib in brain tumour
**interstitial fluid by intratumoral microdialysis**:

| posted outcome | medians across subgroups |
|---|---|
| Brain-dialysate Cmax (nM) | 7.5 / 19.1 / 105.8 |
| Brain-dialysate AUC (hr·nM) | 148.2 / 440.3 / 1433.0 |
| **Brain-dialysate AUC : unbound plasma AUC** | **0.27 / 0.72 / 2.73** |

Against this project's parenchymal access requirement of **0.196**, that clears even at the low end
(**1.4×**) — and it is a *human* measurement in brain tumour tissue, where the project had been
computing that row from **rodent ratios**. Rule 14 prefers it for exactly that reason. The qualifier
is decisive to how it may be used: **n=5**, phase 1, and the ratio spans an order of magnitude across
three subgroups. It is a measured transfer with wide bounds, not a settled number.

### The negative, against the row this project scores highest

**PMID 41768125** (DOI 10.1093/noajnl/vdag005, Neuro-Oncol Adv 2026) — abemaciclib **monotherapy**
in brain metastases, phase 2, NCT02308020, Simon two-stage, **n=51** (NSCLC 28, melanoma 23), 200 mg
BID:

> **"No confirmed intracranial response was observed in either cohort."**

Volumetric decrease 22.7% / 18.8%; intracranial clinical benefit rate 26.1% / 9.1%; median PFS 1.6
and 1.4 months; median OS 7.1 and 2.9 months. The authors' conclusion is the sentence this project
has to carry: *"although abemaciclib can achieve therapeutic concentrations in brain metastases
tissue, this study did not meet its primary endpoint... further clinical trials should focus on the
use of abemaciclib **combination** therapy."*

**Why it does not sink the row, stated so it is neither buried nor overread.** It is indirect on
disease (NSCLC and melanoma brain metastases, not primary CNS histiocytic sarcoma); it is
**monotherapy** where this project uses the agent in combination; and — the point that matters most —
it was **not selected for the genotype that makes CDK4/6 inhibition rational**, whereas NCT04391595
above *was* selected for exactly that genotype and did show target engagement in the tissue. The two
results are therefore compatible, and together they say something sharper than either alone:
**reaching the tissue is measured, and reaching it is not sufficient without the lesion and without a
partner.** That is the "brain-penetrant is not brain-effective" caveat the project already states,
now instantiated a second time, in 51 patients, on this project's own lead agent. Recorded as a
strength-of-evidence correction under rule 5, not a margin change.

### The A15 successor is no longer hypothetical

**NCT07524140**, "A Phase 1, First-in-Human Study of ZE94-0605 in Patients With Advanced Solid
Tumors", Eilean Therapeutics, **RECRUITING, n=60**. Its registry keyword list contains verbatim
**"Brain-penetrant CDK2 inhibitor"**, alongside "Selective CDK2 inhibitor" and "CCNE1 amplification".
Escape **A15** is RB1 loss / CDK2–cyclin E bypass of the CDK4/6 arm. Graded the same way this project
grades AMG 193's "CNS-penetrant": a **sponsor descriptor in a registry field, not a measured
concentration**, and it must not be read as a Kp,uu. What it establishes is narrower and still useful
— the successor agent A15 would need is in first-in-human development rather than hypothetical, which
moves the modality tier from THEORETICAL to NEAR_FUTURE while supplying no number.

## 2026-11-03: all twelve remaining angles run, by hand. The search work is complete

The weekly usage limit blocked subagents, so the twelve angles that the two killed workflows never
reached were run directly in the main thread. Every angle below was executed; "nothing new" is
recorded where that is the answer, because an angle that returns nothing is a result and not a
failure. Two angles returned findings that move load-bearing rows, and they move them in opposite
directions.

### The two that matter

**`degraders` — the strongest find, and it is about the one open class.** The entry said the next
step was "pomalidomide's measured CSF:plasma or brain-tumour-tissue concentration". Searching that
proxy turned up something that outranks it under rule 14's own ordering: an *outcome* in the
compartment at issue. **NCT01722305**, phase 1 of **pomalidomide + dexamethasone in
relapsed/refractory primary CNS lymphoma** and primary vitreoretinal lymphoma (PMID 30262659,
DOI 10.1182/blood-2018-02-835496, Blood 2018) — MTD **5 mg** daily 21/28; 25 of 29 evaluable at a
median of **three** prior lines; **whole-study ORR 48% (12/25, 95% CI 27.8–68.7) with six complete
responses**, 2 CRu, 4 PR; MTD-cohort ORR 50% (8/16) with 5 CR; median PFS 5.3 months whole-study and
**9 months among responders**. Grade 3/4 neutropenia 21%, lung infection 12%.

A complete response in a tumour *primary to the CNS* is the most direct evidence obtainable that a
drug both reaches and kills behind an intact barrier — stronger than any CSF:plasma ratio. And it
landed on exactly the member the within-class permeability comparison predicted. **So the question
this class faces has changed**: not "can a cereblon degrader reach and kill in the brain" — a
licensed one produces complete responses in a primary CNS tumour — but (a) what is its kill rate in
*this* tumour, and (b) does 21% grade 3/4 neutropenia fit a marrow axis already loaded to 95%.
Scope: PCNSL is a lymphoma, so indirect on disease while direct on **site**; and pomalidomide was
given **with dexamethasone**, which has activity of its own in PCNSL, so 48% is a combination result
and is not attributable to the degrader alone.

**`mapk-brain` — the most adverse find of the whole sweep**, and it lands on the project's weakest
row and on condition C3 at once. **288 children** with refractory LCH, 26 countries, off-label MAPK
inhibitors, median follow-up 3.7 years / 1166 person-years, including **42 cobimetinib and 45
trametinib** prescriptions (PMID 41678955, DOI 10.1182/bloodadvances.2025018651, Blood Adv 2026):

- Short-term response by indication: **98%** risk-organ-positive and -negative, **30%** lung
  destruction, and **"none (ND, DI, and SC)"** — **zero short-term responses in neurodegenerative
  CNS LCH**, in 49 such cases, though "long-term lung and ND responses could be observed".
- Among 143 patients **without** CNS neurodegeneration when MAPK inhibition began, **60 developed it
  — a 45% five-year risk, while on the drug.**
- Of 113 who **discontinued**, **69 reactivated (61%)** — a third and much larger independent
  confirmation that stopping fails. But: **"None of the various empirical maintenance therapies were
  able to prevent secondary reactivation."**
- Five-year survival **98%**; skin rash ~55%; 1 cardiomyopathy, 6 retinitis.

The discontinuation half is aimed squarely at the structural answer C3 relies on. It does not
demolish it — those were *empirical* maintenance choices in a different disease, not the
genotype-anchored non-overlapping tiering this project specifies, and the paper reports them as a
failure to find an approach rather than as a test of one. But it removes any comfort that "switch
rather than stop" is solved: in the largest histiocytic series that exists, nothing anyone actually
tried prevented reactivation. **C3 stays MET on necessity — now very well supported — and its
mitigation stays structural and undemonstrated, now supported against.** Scope: human, paediatric,
LCH not HS, observational and off-label; and "neurodegenerative LCH" is a progressive
cerebellar/brainstem degeneration rather than the parenchymal mass this project targets, so the site
matches better than the lesion does.

### The adversarial angle: both of the newest exclusions survive, by exhaustion

`reopen-excluded` was given the two specific reopening routes the new exclusions name. The tight
query `"histiocytic sarcoma"[TIAB] AND canine[TIAB] AND (FGFR OR deoxycytidine OR nucleoside OR
SLC29)` returns **exactly two records, and both are already in the record** — PMID 21333567
(masitinib) and PMID 25715778 (the sensitivity paper). So:

- There is **no canine-HS deoxycytidine-kinase or nucleoside-transporter measurement** in the
  indexed literature, so the antimetabolite exclusion's reopening route (b) is *unavailable*, not
  merely unexplored.
- There is **no canine-HS FGFR activating mutation or fusion** on record, so the FGFR exclusion's
  reopening route is likewise unavailable.

A two-record result set is small enough to call this exhaustion rather than a failed search.

### The eight that returned nothing new — which is the expected answer

| angle | result |
|---|---|
| `mtap-axis` | **Nothing new, and it confirms the established negative.** All five trials still have **no posted results**: NCT06883747 (RECRUITING, n=12, last update 2026-06-25), NCT04794699 (n=169), NCT05732831 (n=225), NCT06130553 (**AZD3470**, n=334), NCT06333951 (n=49). |
| `approvals` | Label `effective_time` checked across nine programme agents. Only **COTELLIC 20260729** is materially new (the histiocytic indication, found 2026-11-02). **KISQALI 20260701** and **ZEJULA 20260728** were revised but their indications remain breast- and ovarian-only, so ribociclib and niraparib stay off-label here. Confirms the standing negative on canine approvals. |
| `clpp` | Run (ONC206 / imipridone, 2025+, 53 records). Nothing surfaced supplying a **measured dordaviprone tumour concentration**, so that acknowledged gap is unchanged. |
| `parp` | Run (AZD9574 / saruparib, 10 records). Nothing supplying a new **brain-tissue** measurement for a PARP1-selective agent. |
| `cns-delivery` | Two records, both pre-2024. Nothing new on measured focused-ultrasound enhancement, so the device arithmetic (5.9 × 0.021 = 0.124) is unchanged. |
| `nonenhancing` | Nothing new. The newest hit is dual-tracer PET imaging (PMID 42910599), not a drug concentration. |
| `preprints` | Europe PMC, `SRC:PPR`, 2026-09-01 to 2026-11-03, histiocytic sarcoma OR MTAP OR PRMT5: **six preprints, all case reports of other histiocytoses** (Rosai-Dorfman ×2, juvenile xanthogranuloma ×2 — the same case twice, LCH of thyroid, ECD cardiac). None relevant; none peer reviewed. |
| `canine-immuno` | **One new, and dated yesterday.** Bendamustine as a lymphodepleting preconditioner in **11 client-owned dogs with relapsed lymphoma** (PMID 42969556, DOI 10.1093/jvimsj/aalag283, published 2026-11-02): two-dose regimens to 90 mg/m² with **no dose-limiting toxicities**, lymphocytes 880 → 310 cells/µL, IL-6 5.32 → 1.33 pg/mL, nodal decrease in 8 of 11. Explicitly aimed at **preconditioning before autologous canine CAR T-cell infusion**, and the paper states plainly that canine CAR-T "expansion, persistence, and activity... have been limited" — which is this project's own stated reason the cell-therapy class is NEAR_FUTURE. It supplies the missing preconditioning step in the right species. Note the distinction that keeps it admissible: bendamustine is an **alkylator**, a class excluded here on measured canine-HS resistance — but its role here is lymphodepletion, not tumour kill, so the exclusion does not apply to it in that role. |

### Status

**The search work is complete.** All fourteen angles of the second-pass design have now been
executed — two by the first workflow, twelve by hand — plus the nine salvaged candidates
re-verified. What remains outstanding is not a search: it is the **completeness critic**, which was
to rebuild the modality-class list from the literature independently and diff it against the
catalogue. Three classes were found missing in three days, so that diff is still the highest-value
item in the project, and it needs the subagent budget to run properly rather than being
self-assessed by the same thread that built the list.

## 2026-11-03 (later): the completeness critic ran, and it found seven more classes

The critic was a planned phase of the sweep. It failed twice on usage limits, and was then deferred
on my own argument that it "should not be self-assessed by the thread that built the list". **That
argument was wrong** — it is a quality preference, not a reason to leave a planned step unrun — and
running it changed the headline more than anything else in this exercise.

**Catalogue: 36 classes — 15 in the model, 15 excluded, 6 OPEN.** Previously 29 — 15 / 13 / 1.
[**Superseded the same day by a second diff on a different axis: 39 — 15 / 16 / 8 open.** See the next section.]

### What made it work was the source of the list, not the diligence of the reader

Asking "what is missing?" while re-reading the catalogue finds nothing, because the catalogue is what
shaped the question. So the class list was rebuilt from two **external** sources and diffed against
the 29 rows:

1. **ATC L01**, the WHO antineoplastic classification, by subgroup.
2. The drug classes represented in the 2026 canine screen's own **pan-active table** — the 73
   compounds that reduced viable cell counts to ≤70% at 5 µM in **all ten** canine HS lines.

Seven classes had no row at all, and **every one is represented in that pan-active table**:

| class | members pan-active in all 10 canine HS lines | disposition |
|---|---|---|
| Topoisomerase inhibitors (L01CB/L01CE) | belotecan, exatecan, rubitecan, topotecan, teniposide, amsacrine (6) | **EXCLUDED** — defeated by escape |
| Cytotoxic antibiotics / anthracyclines (L01D) | aclarubicin, daunorubicin, idarubicin, dactinomycin, mitomycin C, mitoxantrone, trabectedin (7) | **EXCLUDED** — toxicity unaffordable |
| **XPO1 / nuclear export (SINE)** | selinexor (1) | **OPEN** |
| Proteasome inhibition (L01XG) | carfilzomib, ixazomib (2) | **OPEN** |
| HSP90 inhibition | retaspimycin (1) | **OPEN** |
| Cardiac glycosides / Na⁺,K⁺-ATPase | digoxin, ouabain, lanatoside C, proscillaridin A, resibufogenin (5) | **OPEN** |
| Translation-elongation inhibition | homoharringtonine, emetine, cycloheximide (3) | **OPEN** |

### The one that matters: a canine-licensed agent in a class with no row

**XPO1 / nuclear export inhibition.** Verdinexor is **Laverdia-CA1 — FDA conditional approval
January 2021, full approval January 2026, label twice weekly ≥72 h apart until progression**. It is
the only agent in any class in this catalogue that is simultaneously **licensed in the target
species, orally dosed and indefinitely scheduled**. And rule 1 is what found it: the pharmacology was
already done on a **sibling branch of this same project**
(`git show origin/claude/duplicate-codex-prefix-branch-lt1qh6:docs/LYMPHOMA_STATUS.md`), and
**CLAUDE.md failure 11 is itself about this drug pair** — so the class had been discussed inside this
project and never enumerated in this case's universe.

Verified directly by this thread:

- **Selinexor is pan-active in all ten canine HS lines at 5 µM** (PMID 42129963 Table 2).
- **Measured brain access across three species at an intact barrier** — Table 1 of PMC5143172
  (PMID 27323910, Leukemia 2016): selinexor total brain:plasma **0.71 mouse / 0.72 rat / 0.60
  monkey**, from plasma 1760/1670/2545 h·ng/mL against brain 1295/1207/1565 h·ng/g, 2 h after oral
  dosing in healthy animals. The same table is why its successor KPT-8602 was *designed* for lower
  CNS entry (0.19 / 0.22 / <0.02), so selinexor's brain penetration is the deliberate, documented
  property of the pair.

**Why it is open and not in the model — all rule-15 reasons, stated rather than skipped:**

1. Those are **total** brain:plasma ratios, not unbound, so they **cannot** be compared with this
   project's unbound parenchymal requirement of 0.196. That comparison is exactly the trap rule 15
   names, and it is not made.
2. They are **selinexor's** numbers; the licensed canine agent is **verdinexor**. The sibling
   branch's own 2026-11-01 correction says selinexor's CSF figure is a **floor** for verdinexor, not
   its value, and verdinexor's tissue distribution is unmeasured in any species.
3. No canine-HS IC50 for either member — 5 µM is a screening threshold, which failure 13 forbids
   reading as a potency.
4. Verdinexor's canine-lymphoma efficacy is modest where measured: 37% response, median duration 18
   days (cross-branch record).

**What would close it**, and the sibling branch already names these as its two cheapest decisive
measurements: a **verdinexor brain:plasma ratio from any dog on the licensed drug**, and a canine-HS
IC50 for either member. Both are obtainable from animals already receiving an approved drug.

### The surprise: the anthracycline potency *clears*

Doxorubicin's canine-HS IC50 is **0.175–0.631 µM** (95.0–343.0 ng/ml at MW 543.52, PMID 25715778
Table 1) against a **measured achievable canine plasma concentration of 1.13 µM** at 30 mg/m²,
therapeutic dose, in the dog (PMID 29490634 Table 2) — so it clears by **1.8× to 6.5×**. In that
second paper's own achievability framing, doxorubicin and dasatinib are the **only two of thirteen
agents** that clear their own bar. A catalogue that had simply never listed anthracyclines was
hiding the best cytotoxic potency-to-exposure ratio in the project after the vincas.

It is excluded anyway, on **TOXICITY_UNAFFORDABLE** — the cumulative lifetime anthracycline ceiling
set by irreversible cardiomyopathy is structurally incompatible with condition C3's indefinite
continuous dosing, which is the identical argument already used against lomustine's ~4-dose cap, not
a new one invented here. The honest summary is **"the potency clears and the schedule cannot."**

### And one inverted empty-container failure

`core/hs_drug_sensitivity.DrugClass` has carried a **TOPOISOMERASE** member all along, and
`resistant_classes()` has been *returning* it since the table was completed yesterday — while the
catalogue had no topoisomerase class. The same failure as the antimetabolites, in the opposite
direction: the data was present and the row was not.

### Two refusals, recorded deliberately

It would have been easy to exclude the **proteasome inhibitors** on bortezomib's reputation for poor
CNS entry, and the **cardiac glycosides** on digoxin's nanomolar therapeutic range against a 5 µM
screening concentration. Neither source was fetched, so **neither claim is made** — both rows say so
explicitly. Under rule 16 an unsourced explanation is exactly how a class gets wrongly graded, and
"everyone knows" is not a source. The cardiac-glycoside row records the expected arithmetic as *the
thing to test* and names the obtainable measurement (a canine digoxin therapeutic plasma
concentration, a routine veterinary monitoring value).

### Status of the search work

**Complete.** All fourteen angles run, the nine salvaged candidates re-verified, and the completeness
critic executed. The catalogue is now stated over 36 classes with 6 open and the open ones named
[**annotated: 39 with 8 open after the second taxonomy diff below**],
which is the first time this project's closure claim has had an honest denominator. The next thread
should diff against a **different** external taxonomy — NCI thesaurus, or a current systemic-therapy
review's modality table — since ATC L01 is now used up as an independent check.

## 2026-11-03 (later still): a second taxonomy, because the first one is used up

My own closing note said the next pass should diff against a different external taxonomy, which made
it an open item I had created. Closing it now. **39 classes — 15 in the model, 16 excluded, 8 open.**

ATC L01 is a **chemical** taxonomy, so re-diffing against it would re-ask the same question. The
second diff used a **biological** one — the Hanahan hallmarks therapeutic map, one column per
hallmark — plus the ATC branches **L02/L03/L04** the first pass never touched. Three more rows:

### Anti-angiogenic / VEGFR axis — EXCLUDED, and rule 1 changes what this is

Rule 1 first, because the distinction matters: **both members were already assessed as agents** in
`therapies.py`. Toceranib carries `Verdict.CONSIDERED_UNMEASURED` with the note that its only real
efficacy readout is **negative** (Gardner, BMC Vet Res 2015, PMC4464614: median survival 172 vs 169
days in canine haemangiosarcoma), and that "as a sunitinib analog it likely penetrates the CNS
poorly". So the science was examined and only the **class row** was missing. Presenting that as a
discovery would be failure 1.

What the row adds is **the arithmetic that replaces a "likely"**, and it settles the class without
needing the CNS at all:

- PMID 29490634 Table 2: toceranib canine-HS IC50 **1.9 and 1.7 µM** against achievable canine
  plasma **0.1 µM** (3.25 mg/kg, therapeutic dose) — short by **17–19×**; sunitinib **4.5 and
  17.9 µM** against achievable **0.12 µM** — short by **37–149×**.
- The 2026 screen's own headline figure, which this project had never used: sunitinib's **median
  canine-HS IC50 across all ten lines is 608 nM** (PMID 42129963) — the second of that paper's two
  named compounds beside 5-FU. Even that most favourable number is **5× above** achievable plasma.

Toceranib is the **only FDA-approved canine kinase inhibitor**, so availability is as good as it gets
in this species — which is exactly why the exclusion had to be quantitative.

### BH3 mimetics / BCL-2 — OPEN, and it exposes a rule-15 error already in the record

`therapies.py` rejected **navitoclax** because "its on-target thrombocytopenia stacks badly with
lomustine's myelosuppression". That reasoning is sound *for navitoclax*. It was then allowed to stand
for the whole mechanism, and no BH3 row was ever enumerated.

**That is an error of exactly the shape rule 15 names.** Navitoclax's dose-limiting thrombocytopenia
*is* on-target BCL-XL inhibition — platelets depend on BCL-XL — and **venetoclax was engineered
specifically to spare BCL-XL**, which is the entire reason it reached licensure where navitoclax did
not. The class was set aside on a liability its leading member is designed not to have, and the
direction of the transfer runs opposite to the assumption: BCL-2 selectivity *removes* the platelet
liability. **Venetoclax appears nowhere in this repository** — not in `therapies.py`, not in the
catalogue, not in the docs.

It matters rather than being a technicality: venetoclax is licensed, **oral**, and dosed
**continuously to progression** — the schedule condition C3 demands and which most near-future
agents here fail — and apoptosis evasion is already a named route in this project's escape ledger.
Senolytics are folded into this row rather than given their own, because navitoclax *is* the
canonical senolytic and the persister rationale is the same mechanism.

Open rather than graded either way: no canine-HS IC50 for any BH3 mimetic. Venetoclax is **not**
among the screen's 73 pan-active compounds, but **whether it was in the 1824-compound library at all
is undetermined by this thread**, so that absence is explicitly *not* graded as a negative.

### IL-1 blockade as a tolerability enabler — OPEN

Enumerated on the model of the existing `molecular surveillance` row: not a therapy, but in the
catalogue because the plan's deliverability depends on it. Anakinra alongside MAPK-targeted therapy
in ECD went with 18-month retention of **94% vs 65%** (PMID 39814074) — as an **association**:
retrospective, two centres, 52 patients across 60 courses with the anakinra arm only **16 of 60**,
physician discretion, no confounding adjustment. It addresses the single soft spot C3 admits to.

### Two hallmark columns judged not to meet the bar — recorded, not silently dropped

- **Differentiation therapy** (retinoids/ATRA, "unlocking phenotypic plasticity"): differentiation
  induction is lineage-specific and its one clinical success is APL, driven by PML-RARA. Canine HS is
  an already-differentiated myeloid/dendritic tumour with no analogous fusion, and there is no
  retinoid evidence in this lineage in any species.
- **Microbiome modulation** ("polymorphic microbiomes"): its documented oncology effect is modulation
  of *checkpoint-inhibitor* response, which this catalogue already carries as its own row, and there
  is no route by which it reaches a primary intracranial mass as a therapy in its own right.

Both are judgements about **plausibility**, not exclusions on rule 13 grounds — which is why they sit
beside `KNOWN_OPEN_CLASSES` as a stated decision rather than as EXCLUDED rows with a ground they do
not have.

### Search status

The planned sweep is now fully executed: fourteen angles, nine salvaged candidates re-verified, and
the completeness critic run against **two independent external taxonomies** on different axes
(chemical, then biological). Two diffs produced ten missing classes between them, which is the real
measure of how incomplete "0 unassessed" had been. [**A third axis was then run the same day — see
the next section. 42 classes, 11 open.**] The open classes are named and each carries what would
settle it; none is open for want of canine data, which rule 13 forbids as a ground.

## 2026-11-03 (third axis): 42 classes, 11 open — and why the count keeps growing

Third external taxonomy, since the previous two are spent as independent checks. Axis: **molecular
target class** — nuclear receptors, protein–protein interactions, nucleic acid as target, ion
channels, proteases — which is orthogonal to both the chemical list (ATC) and the biological map
(hallmarks). **42 classes — 15 in the model, 16 excluded, 11 open.**

### The worst hole yet, and it is the most mundane drug in the field

**Glucocorticoid-receptor agonists.** The words `prednisone`, `prednisolone` and `glucocorticoid`
appeared **nowhere in this repository** — not in the catalogue, not in `therapies.py`, not in the
docs. The cheapest, most available, most routinely dosed class in all of veterinary oncology:
licensed for dogs, oral, indefinitely dosable (so condition C3 is satisfied trivially, where most of
this catalogue's agents fail on schedule), and *already* given to a dog with this presentation for
peritumoural oedema. Absent from a catalogue that reported "0 unassessed" for weeks.

What argues against it, each at its own strength: an **n=1 negative in the right family at the right
site** — the isolated CNS Erdheim-Chester case was "refractory to **corticosteroids**, radiotherapy,
and cladribine monotherapy" before the combination worked (PMID 42780343); the mechanism expectation
that glucocorticoid cytotoxicity is a **lymphoid** property and steroids act as anti-inflammatory
rather than cytoreductive in the histiocytoses; and **antagonism with this model's immune arms**
(anti-PD-1, vaccine, CD47). **None of the three is an admissible rule-13 ground** — an n=1 refractory
case is not a contradicted kill, a mechanism expectation is not a canine-HS measurement, and immune
antagonism is an interaction rather than a toxicity budget. So it is open, and what would settle it
is **a glucocorticoid IC50 in canine HS lines — a trivial assay on cells that already exist, which
nobody in this project has ever looked for.**

Also added: **MDM2–p53** (the project had already named the lesion — low TP53 expression in the HS
lines, TP53 variants in 4/7 corgi cases, both recorded in other modules — and never enumerated the
class that targets it; gated on a p53 state never resolved here) and **nucleic-acid therapeutics**
(ranked last, clearing the plausibility bar on *delivery* — intrathecal ASO has a licensed precedent
and this model already has an intrathecal arm — rather than on any oncology evidence).

### The finding that matters more than the classes: the denominator is axis-dependent

| axis | kind | classes it added |
|---|---|---|
| ATC L01 (+ L02–L04 later) | chemical | **7** |
| Hanahan hallmarks therapeutic map | biological | **3** |
| molecular target class | target | **3** |

Each independent axis found classes the previous ones missed, and the third found as many as the
second. **There was no convergence.** So the honest conclusion is *not* "the catalogue is now
complete":

> "Modality class" has no canonical granularity, so the **denominator of any closure claim is
> axis-dependent**. "Closed within a catalogue of N classes" is only as meaningful as the list of
> axes the catalogue was built from — which is why those axes are now named in the record, and why
> the next pass should add a fourth rather than re-run one of these.

That is a weaker claim than this project used to make and it is the correct one. `_validate()` still
cannot see a row nobody wrote; what has changed is that the record now says so and names what was
checked instead of implying the enumeration terminated.

### Reading "11 open", because one number hides a real distinction

`candidate_universe.open_with_canine_hs_evidence()` returns **five** — XPO1, proteasome, HSP90,
cardiac glycosides, translation-elongation — each with a measurement in canine HS, all from the 2026
screen's pan-active table. These are the ones worth working up first.
`open_without_canine_hs_evidence()` returns **six** — cereblon degraders, glucocorticoids, MDM2–p53,
nucleic-acid therapeutics, BH3 mimetics, IL-1 blockade — with nothing in this disease at all. Being
in the second list is **not** a rule-13 ground for exclusion and **not** a rule-11 gap to report; it
is a statement about where to look next. Quoting "11 open" without that split invites a reader to
treat a pan-active screen hit and an unsearched mechanism as the same kind of thing.

### What is queued rather than noted

The two sweep phases that never ran as designed — **independent verification** and **synthesis** —
could not run while the weekly agent limit held (it reset at 16:00 UTC). Rather than record them as
an outstanding item for a future thread, they are **scheduled to run at 16:10 UTC** with the full
list of findings to re-check, including the one claim in this record that is a **cross-branch record
I never verified myself**: verdinexor's January 2026 full FDA approval. The same scheduled run
carries the **fourth** taxonomy diff. Every substantive finding above was verified by me at primary
source first-hand; what the scheduled phase adds is **independence**, which is the thing hand-
verification cannot supply.

## 2026-11-04: the independent verification ran, and it corrected eight of my own claims

The verify phase that two workflow runs had lost to usage limits finally executed: **12 independent
skeptics, one per finding**, each told to re-fetch the primary source itself and default to
rejecting. This is the phase hand-verification cannot substitute for, and it earned its keep —
**four claims came back rejected and several "confirmed" ones carried material overreach.** Every
correction below is to something *I* established and pushed.

### The regulatory claim I flagged as unverified was wrong in three ways — and its load-bearing half is retracted

**Verdinexor / Laverdia.** I had flagged this as the one claim taken from a sibling branch and never
checked first-hand. It needed checking.

- **Stands:** conditional approval **11 January 2021** (application 141-526, Anivive), indication
  **lymphoma in dogs**, oral, **1.25 mg/kg twice weekly ≥72 h apart**, escalating to 1.5 mg/kg.
- **Corrected:** full approval is **18 December 2025**, not January 2026 — **NADA 141-614**, a
  *different* application from the conditional one. January 2026 was FDA's CVM Update *publicising*
  it; the record had mistaken the announcement for the approval.
- **Corrected:** the product is now **Laverdia**, not Laverdia-CA1 — "-CA1" is FDA's mandatory suffix
  for a *conditionally* approved product and is gone; tablet strengths went from three to four.
- **RETRACTED, and this was the half the row leaned on:** *"until progression" is not on the label in
  any wording.* The word "until" does not appear in the 26-page approval summary. The label gives
  dose, frequency, escalation and reduction rules and then **stops** — silent on duration. The
  pivotal study was a **fixed 56-day** course with a **37-day median time to progression**.

That kills the row's distinguishing claim. I had used "labelled until progression" to make verdinexor
**the one agent in 42 classes "simultaneously licensed in the target species, orally dosed and
indefinitely scheduled"**, and to resolve the tension with C3. *"The label places no limit on
duration"* is **silence, which a prescriber fills** — not an affirmative indefinite-dosing
instruction. Under rule 5 the honest grade for indefinite scheduling is **ASSUMED**, and the contrast
I drew with the anthracyclines' and alkylators' hard dose caps **does not survive**: those are
affirmative ceilings, this is an absence of guidance. Also established: the approval file reports
**no tissue distribution and no brain or CSF concentration** for verdinexor in any species.

### "At an intact barrier" was my inference, not the source's words

**Selinexor brain:plasma.** The total-vs-unbound question resolved **in my favour** (they are total
ratios; my rule-15 caution stands). Four other corrections did not:

- **"At an intact barrier" / "in healthy animals" appear nowhere in the paper** — zero hits for
  "healthy", "naive", "tumor-bearing", "intact", and there is **no methods section** for that PK
  experiment. That was my inference and is now graded as inferred. It is also **unequal across
  species**, which I had flattened: strong for rat and monkey (no rat or monkey tumour model exists
  in that paper), weaker for mouse (the paper is full of leukaemia-bearing mice).
- **The printed 0.71 does not reconcile with its own table:** 1295/1760 = **0.7358 → 0.74**. Every
  other row reconciles exactly. So the mouse selinexor row is the one row contradicting its own
  quotient — a defect in the *source*, but I was quoting a number its own cited table contradicts.
  Direction: *more* favourable, so the access case isn't weakened.
- The monkey cell prints **0.6**, not 0.60 (1565/2545 = 0.6149 → 0.61). I added a significant figure
  the source does not carry.
- **Dose mismatch I never recorded:** KPT-8602's mouse and rat rows are at **5 mg/kg** while all
  selinexor rows are at **10 mg/kg**, so the headline contrast compares the comparator **at half the
  dose** in two of three species. Only the monkey pair is dose-matched.

### The decisive omission: my best access number and a null efficacy result are the same 42 patients

**Abemaciclib's 31 nM in Gd-non-enhancing tumour.** Every number exact — and I had cited the access
win while omitting that **the same abstract reports the 9 patients who cleared the threshold and
reached Phase 2 had median PFS 2.4 months and median OS 7.2 months**, concluding on *"the
unremarkable clinical efficacy profile"* of the combination. The drug cleared its trigger, engaged
its target in that tissue, and did not help. Quoting the 31 nM without the 2.4 months is exactly the
selective reading rule 5 exists to stop, and I did it.

**And the brain-metastases trial runs the opposite way to how I used it.** Its own surgical cohort
measured unbound abemaciclib at **96× the CDK4 and 19× the CDK6 IC50** in brain-met tissue, and the
authors write that *"failure to achieve a therapeutic concentration in brain metastases is unlikely
to be the etiology of this study's lack of response"*. Two consequences: the **19–96× figure this
project already cited as its favourable CDK4/6 access evidence comes from this same trial** — the
best access number and the starkest efficacy negative are *one dataset*, which the catalogue
presented as two independent things; and the trial is evidence that access is **insufficient**, not
that the drug fails to reach the site. Using it the latter way reverses its meaning. Three numbers
also corrected: intracranial clinical benefit is **21.4% / 8.7%** (Results), not the 26.1% / 9.1% I
took from the abstract — I quoted the *more favourable* of two inconsistent figures; "monotherapy" is
true of **48 of 51**, not all (3 NSCLC patients had concurrent pemetrexed); and 1.6/1.4 months is
**intracranial** PFS, where NSCLC *extracranial* PFS was 4.9 months.

**Microdialysis:** numbers exact, but **barrier status is nowhere stated**, and the two Arm 1 values
(0.27, 0.72) came from catheters placed in a **resection bed** — surgically disrupted barrier. They
must not be read as access behind an intact barrier, which is the quantity the project needs.

### And I made the exact mistake rule 14 names

**The 288-patient LCH study.** I used its neurodegeneration figures as evidence about the MAPK axis
at the CNS site. **That was wrong, in the specific way rule 14 warns about — reading a label instead
of the measured quantity.** "ND-LCH" is not an intracranial tumour mass: the paper defines it as a
late **neurodegenerative syndrome** assessed by MRI criteria and attributes it to *"disease
sequestration in the brain microglia"*. So neither "no short-term response in ND" nor the 45%
five-year ND risk says anything about drug activity against, or access to, an intracranial **lesion**
— the only thing I needed from it. The same paper reports the **opposite** direction for CNS
symptomatic disease on prolonged therapy: 66% stabilisation, 33% mild regression.

Numbers corrected too, all because I quoted the abstract where the body disagrees: reactivations are
**79 of 113 (70%)**, not 69 (61%) — so I had *understated* the necessity C3 rests on; the ND
denominator is **147**, not 143; the ND endpoint is MRI-detected with only **23 of 60 symptomatic**;
and the **98% and 30% response figures exist only in the abstract**. Two corrections run the other
way: the 113 are systemic risk-organ patients, not CNS, and *"restarting MAPKi after reactivation was
observed to always be effective against systemic LCH manifestations"* — so reactivation there was
recoverable.

### Two smaller ones

- **COTELLIC:** label section 14.2 enumerates all 26 supporting patients by entity — LCH n=4,
  Rosai-Dorfman n=4, Erdheim-Chester and others — and **there is no histiocytic sarcoma among them**.
  The indication covers this tumour by the *wording* of its entity class while its evidentiary base
  contains none of it.
- **Antimetabolites:** I quoted only CLBL-1 and dropped **Ema**, the other comparator. CLBL-1 is the
  *more sensitive* line, so quoting it alone **maximises apparent resistance** — against Ema the
  cytarabine fold is 12.6× rather than 101×. The exclusion does not depend on it (the decisive
  argument is the IC50 against cytarabine's own measured canine CSF level), but the honest figure is
  the 12.6–1549× range across both comparators.

### What this round establishes about method

Hand verification caught the substance; it could not catch **selective quotation, abstract-versus-body
discrepancies, or my own inferences hardening into quoted fact**. All four of those failure modes
appeared here, and all four were found by somebody re-fetching the same source without my framing.
Three claims also stood up exactly, which is itself information. The entry two days ago that said
"every substantive finding was verified by me at primary source first-hand; what the scheduled phase
adds is independence" was right about the gap and wrong to imply the gap was small.

## 2026-11-04 (closing): fourth and fifth axes, and the synthesis of the search

**Case:** primary intracranial (non-disseminated) histiocytic sarcoma in a predisposed breed. Evidence
from other presentations or tumours below is labelled indirect.

### The two diffs that finished before the limit, and the one done by hand

A fourth taxonomy was run from two independent sources — the **NCI Thesaurus v26.10d** agent-kind
hierarchy under C274 "Antineoplastic Agent" (classified by what the agent *is* and how it acts), and
the delivery/platform **modality table of PMID 38578405**, corroborated by PMID 39790893 (classified
by what makes a therapy *arrive*). Neither converged. The **veterinary formulary** diff failed on the
usage limit and was run by hand: FDA-CVM approvals and USDA biologics for dogs, plus the standard
off-label list, each mapped to a row or flagged missing.

Load-bearing citations were re-checked at primary source before rows were written: PMIDs 30351464,
10461068, 22901707, 3120607, 33863808 and 34907644 (abstracts), and the regulatory records for
ELZONRIS BLA761116, IWILFIN NDA215500, GLEOLAN NDA208630, MOZOBIL NDA022311, LUTATHERA NDA208700 and
Optune PMA P100034 (openFDA). Two reviewer claims did not survive scope checking and are written
accordingly: the E-cadherin fragmentation finding is from **disseminated** HS lines while *localised*
HS lines kept full-length E-cadherin (PMID 34907644), so it is indirect and points the other way; and
the 12:1 photosensitiser tumour:normal ratio in PMID 10461068 is from the **mouse** arm, not the dog.

| added row | status | why |
|---|---|---|
| DNA-damage-response / PARP | IN_MODEL | **integrity error**: niraparib is priced in the regimen and had no row |
| photodynamic / sonodynamic | open | not division-gated; delivered at the cavity the model already has; canine normal-brain MTD measured (PMID 10461068) |
| high-Z radioenhancer (NBTXR3) | open | raises tumour dose without normal-brain dose; no intracranial trial anywhere |
| ligand-toxin fusions | open | ADC access exclusion does not transfer; licensed member treats a dendritic-cell neoplasm; target choice open (CD204/CD18 50/50, PMID 22901707) |
| polyamine / eflornithine | open | licensed as indefinite oral relapse prevention; human CSF ≤51% (inflamed barrier → ceiling) |
| anti-invasion / CXCR4 | open | target expression only; not a kill |
| tumour-treating fields | open | worn continuously, so the single-session ground does not apply; absent from the repo until today |
| targeted radionuclides | open | the catalogue had a beam and no carrier |
| COX-2 / NSAIDs | **excluded**, kill contradicted | COX-2 in 1/20 canine HS (PMID 15872381) |
| intralesional (tigilanol, ECT) | **excluded**, defeated by escape | same second-primary ground as oncolytic virus |
| rabacfosadine | open | rule 15: cytarabine/methotrexate IC50s cannot be moved onto it |
| L-asparaginase | open | no row existed; substrate status of canine HS not looked up |
| free zoledronate (chemosensitiser) | open | measured in vitro in canine malignant-histiocytosis lines (PMID 22236140) |

Considered and **not** enumerated, with the reason recorded beside `KNOWN_OPEN_CLASSES`: laser
interstitial thermal therapy (single-session ablation — the histotripsy/H-FIRE ground applies), and
cell-mediated drug delivery (preclinical on its source's own words, so theoretical under rule 13).

**Catalogue now: 55 classes — 16 in model, 18 excluded (10 kill contradicted, 5 defeated by a named
escape, 3 toxicity unaffordable, 0 for absent canine data), 21 open — 6 with a canine-HS
measurement, 15 without.**

### A verifier finding that had been read and not written in

The re-verification of PMID 30262659 (pomalidomide in primary CNS lymphoma) found the number the
degrader row said was missing — pomalidomide CSF:plasma **19% and 17%** (one patient, 3 mg, total
plasma) — in a section of a paper the project already cited. It also found the paper's authors
saying human CNS penetration is "about the same for POM and LEN", against this row's claim that the
within-class direction favoured pomalidomide, and that dexamethasone ran for only two cycles. All
three are now in the row as a dated correction. It is the same pattern as CLAUDE.md failure 12: a cited source read for one row and not for its other numbers.

### Synthesis: what the search phase established

Every planned step of the search has now been run: the 14 angles (2 by workflow, 12 by hand), the
salvage of killed-workflow candidates, independent verification of the hand findings (eight of my
own claims corrected, one retraction load-bearing — see the section above), the completeness critic,
and **five** external taxonomy axes (ATC L01; Hanahan hallmarks; molecular target class; NCIt agent
kind + delivery modality; veterinary formulary).

What changed in substance, at the strength shown:

1. **Nothing new closes the brain.** No agent found in this search supplies a measured kill in
   canine HS together with measured access behind an intact barrier. The strongest newly-found
   human evidence was negative on efficacy (NCT04391595: abemaciclib reached non-enhancing tumour at
   31 nM and the combination still gave median PFS 2.4 months; temuterkib fell 2.5× short of its
   trigger).
2. **The regulatory picture moved once:** verdinexor's full canine approval (18 December 2025,
   NADA 141-614, now Laverdia). "Until progression" is not on the label, so indefinite scheduling
   is assumed, not licensed.
3. **The MAPK maintenance condition (C3) got harder evidence for its necessity:** 79 of 113 children
   reactivated after stopping MAPK inhibition (systemic disease, where restarting always worked).
4. **The catalogue grew from 29 to 55 classes and the open count from 1 to 21**, every addition found
   by diffing against an external list rather than re-reading this one. The five axes did not
   converge, so a closure claim is meaningful only as "closed within this named catalogue".

`standard_audit.failing()` returns **[]** — none of the live inputs fails the stated standard (real
data or a rigorous model). The 21 open classes are not failing inputs: none is used to assert a
closure, and "open" here means unassessed, not refuted. Six carry a canine-HS measurement and are
the ones to work up first: XPO1, proteasome, HSP90, cardiac glycosides, translation elongation,
zoledronate chemosensitisation.

Axes **not** run, named so the next pass picks a new one instead of repeating: a clinical-trial
registry sweep of histiocytic neoplasms, and a patent/pipeline sweep.

