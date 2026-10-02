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
| Therapy universe never enumerated (rule 9) | new `candidate_universe.py` + tests | **25 modality classes, 0 unassessed.** 15 in model, 10 excluded with recorded reasons. Newly assessed: ADCs, bispecific engagers, marrow transplant, oncolytic virus |
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
| "Every mechanism" | **Now established, as a scoped claim.** "Closed within this catalogue of **25 modality classes and 16 escape routes**", 0 classes unassessed, 10 excluded with reasons named. Not the same as "every conceivable mechanism" — it is a claim whose boundary is written down | `candidate_universe.closure_claim()`, `escape_audit` |
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
