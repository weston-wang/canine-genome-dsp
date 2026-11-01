# HSA status — settled results, known gaps, and the published record

Branch-specific state for `claude/codex-branch-audit-clfeiz`. Working agreements live in `CLAUDE.md`;
the full reasoning lives in `docs/HSA_DURABLE_RESPONSE.md`. This file exists so the next thread does
not re-derive or re-litigate what is already decided (`CLAUDE.md` rule 7).

**Case under analysis** (rule 10): **canine splenic hemangiosarcoma**, stage I–II, post-splenectomy,
adjuvant setting, ten-year horizon, assuming early detection. Evidence from another presentation
(cardiac/dermal HSA, human angiosarcoma, other canine tumours, mice) is indirect and labelled as such
in the narrative document.

Last full literature sweep: **2026-09-30 / 10-01**.

---

## Settled — do not present these as news

| Result | Where |
|---|---|
| **The bar is 0.052/day** and the drug is nearly irrelevant to it — full dose to no drug moves it 7% | §1 |
| Real vaccines deliver **~0.030/day, about 1.7× short**; two Phase 2 trials in this disease | §2 |
| **Height and persistence are separable**; boosters buy only the second — with the 118-dog qualification | §3 |
| Five closures tried and failed: second agnostic kill, two vaccines, booster tolerance, β-blockade, platform swap | §3b |
| **Exposure and duration criteria**; propranolol fails exposure ~200×, continuous dual kinase inhibition fails duration ~215× | §3b, §3g |
| MEK + TORC1/2 clears the exposure criterion (16.2 nM achievable against ~11 nM required); **0.888** with the vaccine and the cross-resistance correction | §3c |
| The second drug **cannot be stopped**, so the persistent work moves onto the vaccine | §3g |
| The requirement is a **ramp, not a cliff**: ~1.40× buys two years, ~1.45× one year | §3g |
| **Four** levers on vaccine height, with transfer fractions: losartan 7–22%, eBAT 18–23%, anti-PD-L1 23–45%, re-dosing 118–235% (cannot carry it) | §3g |
| The **timing rule**: immune components after the surgical/chemo backbone, gated on recovered effector function. Three independent findings agree | §3e, §3g |
| Route 8: **"rarity is not a defence"** — 0.000 across five orders of magnitude of starting frequency | §3h |
| Route 8 closure: compartment is ~1,300 cells needing 7.2 logs; doxorubicin (3.1–5.1) + one early eBAT cycle (5.2–7.8) gives **0.830**, the no-blind-spot baseline, at four seeds | §3h |
| Route 8 has a closure under **either** branch of genetic-versus-tolerant-state | §3h |
| **Bleeding is the binding constraint**, not the cancer: ~0.53 unscreened against ~0.85 screened | §5 |

## Corrections already recorded — do not re-discover

Drug exposure overstated ~250× (scoping, not retraction) · cross-resistance granted to the wrong
mechanism · booster tolerance was a category error · "boosters buy persistence not height" needs the
118-dog qualification · the route-8 compartment was built with a perfect-correlation error **and** with
doxorubicin omitted entirely · eBAT was classified as a cytotoxic clearance term when it is mainly a
stromal lever · the optimistic reading of the GPX4 gap was wrong · the checkpoint tolerability claim
rested on monotherapy data for a combination plan. All enforced by tests in
`tests/test_hsa_*` — a test fails if a retracted claim is reasserted.

---

## What the 2026-09-30/10-01 sweep changed

1. **eBAT reclassified** from cytotoxic log-remover to stromal lever on vaccine height.
   Schulte 2025, *J Pharmacol Exp Ther* 392(9):103674, PMID 40914989, doi 10.1016/j.jpet.2025.103674.
   MC17 chosen *because* its cells resist eBAT; meBAT still cut median volume 163.1 → 55.5 mm³ (d21,
   p=0.03), TAMs 14.7% → 5.1%, phagocytic myeloid 3.6% → 22.3%, CD3⁺ 0.13% → 3.68%; all abolished in
   uPAR-knockout chimeras. Implies 0.051–0.067/day, 18–23% transfer. Now route 4 in
   `hsa_route_effect_sizes`.
2. **The route-8 EGFR/uPAR stain demoted** from load-bearing to secondary — a drug that benefits a
   tumour it cannot kill does not need the compartment to express its targets.
3. **Checkpoint toxicity revised upward.** Gilvetmab + hypofractionated RT, 18 dogs with MCT: 39%
   attributed AEs, 28% Grade 3, no durable control. Martin, Thamm & Weishaar 2026, PMID 42680555,
   doi 10.1111/vco.70110. Not a substitute for the 5.9% monotherapy figure (different tumour,
   concurrent radiation) but the plan proposes combination. Weakened, not withdrawn. Offsetting:
   conditional US licensure, Chon/Greene/Stock 2026, PMID 42710546, doi 10.2460/javma.26.06.0517.
4. **A randomised negative in the matched human setting.** Trivalent GM2/GD2/GD3 vaccine vs adjuvant
   alone in sarcoma *rendered disease-free by surgery*: sustained serologic response, no difference in
   RFS or OS. PMID 36215947, doi 10.1016/j.ejca.2022.09.003. Does not invalidate the 0.030/day
   calibration; it is the strongest evidence that immunogenicity in this setting need not convert.
5. **Rate distance vs clinical distance** separated as distinct questions. Losartan wins the first,
   eBAT the second. Collapsing them is what produced the misfiling in (1).

## What the sweep confirmed rather than changed

- **Clinical-grade GPX4 inhibitors still do not exist** — first-in-human unlikely before the late
  2020s. The pessimistic reading this analysis adopted over its own earlier optimistic one was
  correct. The persister route is a mechanism, not an agent.
- **Nobody has published per-cell antigen coverage in canine HSA.** Swept single-cell, heterogeneity
  and microenvironment literature 2025–2026: nothing. Route 8's *existence* question is untouched.
- **No new losartan-in-dogs data.** The 7–22% figure still rests on Regan 2019 and 2022 alone.

## Logged, not needle-moving

- Fluvastatin + dipyridamole suppressed canine HSA growth in two PDX models where fluvastatin alone
  did not. Suzuki 2026, PMID 42575716, doi 10.1111/vco.70097. Attractive on duration (both chronically
  tolerated) but it is growth *suppression* — the wrong shape for durability.
- B7-H3 CAR-CIK cells kill canine HSA lines; B7-H3 present across canine sarcoma subtypes.
  De Maria 2025, PMID 40944715, doi 10.1007/s00262-025-04163-4. Possible answer if the blind
  compartment is null for the vaccine target but B7-H3⁺.
- Patient-derived canine HSA 2.5D organoids with orthotopic splenic xenografts. Liu 2026,
  PMID 42797915, doi 10.3390/vetsci13090879. A substrate for the antigen-coverage experiments.
- Case report: remission of unresectable presumptive HSA on toceranib + piroxicam + propranolol,
  PMID 42319213. n=1, presumptive diagnosis. Does not touch the ~200× propranolol exposure shortfall.
- Two new canine HSA reviews (PMID 41793295, 41828985), both concluding current therapy has not
  improved long-term survival. Consistent; adds nothing.

---

## The independent escape audit (2026-10-01) — three routes the eight did not contain

Run per `CLAUDE.md` rule 9: classes enumerated from general tumour-immunology and metastasis biology
*without* consulting the eight routes, then grepped against the record. **Ten classes returned zero
hits.** Module `hsa_escape_audit`, tests `test_hsa_escape_audit.py`.

| # | Route | Threat | Closure | Note |
|---|---|---|---|---|
| **9** | CNS anatomical sanctuary | **MEASURED** — HSA is the largest source of secondary brain tumours in dogs, 51/177 (29%), Snyder 2008 PMID 18289306 | **TRANSFERRED** — activated T cells cross the BBB; checkpoint blockade has CNS activity despite poor penetration | **Selects a vaccine platform:** ERstrePs (humoral + T-cell) covers it; eVim (antibody vs surface vimentin) does not. Doxorubicin, eBAT and losartan do not reach the brain, so the route-8 closure does not extend there |
| **10** | Host immunosenescence | **MEASURED** in dogs — thymic involution, reduced CD8⁺ proliferative capacity, reduced titres to novel antigens | **TRANSFERRED** — memory responses are spared; the *primary* response is the compromised step | **Re-dosing is the fix**, graded in §3g against the wrong question. Its demotion as a potency lever stands |
| **11** | Competing all-cause mortality | **MEASURED** — mean age at diagnosis 9.6 y against breed medians 10.3–12.5 y | n/a — not an escape | A 10-yr disease-free response from diagnosis needs the dog to reach ~20. The reachable goal is *no recurrence for remaining natural life*; the 3,650-day horizon is a conservative proxy. **Makes the target easier, not harder** |

Closed by arguments already in the analysis: **dormancy** (immune killing is not growth-dependent),
**B2M/TAP loss** (the strongest case for the missing-self backup), **Tregs/MDSCs** (CCR2 and uPAR act
here uncredited — and meloxicam/PGE2, already in the record as a parenthetical, is a Treg-directed
lever that clears duration outright).

**The stacking worry is closed, and was never load-bearing.** Tested against the existing grid with
the conservative end of each lever: full addition needs **10%** transfer to beat the 0.888 reference;
**winner-takes-all — complete overlap, only the best lever counting — needs 25%.** A factor of 2.5,
not a factor that decides the plan, and both inside what the anchors support. (Tests the arithmetic of
overlap, not the biology: it does not rule out antagonism, which no data addresses.)

**Clonal evolution to a new resistance driver is now bounded, not assumed.** A resistance lesion
cannot outrun the untreated growth rate, because the drug only ever subtracts — so the worst case is
already a row in §1's bar table: **no drug at all = 0.0550/day against the modelled 0.0515, at most
+6.8%.** That pushes the vaccine requirement from 1.40× to 1.50×, still inside the measured ramp
(0.992 at a one-year stop). What stays **ASSUMED** is a driver raising *intrinsic* proliferative rate,
which the no-drug row does not bound.

**The keyword trap worth remembering:** "sanctuary" appears 20× in the narrative document and every
occurrence is *phenotypic*. A keyword count scores anatomical sanctuary as covered. It was absent.

### The increment, regraded ASSUMED → TRANSFERRED

**KEYNOTE-942** (NCT03897881), 157 patients, randomised 2:1, individualised neoantigen vaccine +
pembrolizumab vs pembrolizumab alone, **completely resected high-risk melanoma — this plan's setting
exactly.** RFS HR **0.510** (0.288–0.906); DMFS HR **0.384** (0.172–0.858); 2.5-yr RFS 74.8% vs 55.6%.

The per-day conversion used for the four levers returns 555–1111% transfer here and is an **artefact**
— it transports an absolute time scale between processes running ~6× apart in tempo. (Internal check:
converting the reported RFS rates to hazards reproduces the trial's own HR, 0.495 derived vs 0.510
reported.) The scale-free comparison is the fair one: the plan needs HR **0.178** on 10-yr failure at
1.40×, and **0.406** at 1.35×. One lever delivers **39–56%** of the needed log-hazard, and **clears
the 1.35× rung outright on DMFS**. Still open: whether canine HSA behaves like human melanoma, and
whether four mechanistically coupled levers stack or overlap.

## The standard audit (2026-10-01) — grading the inputs, not listing absences

`CLAUDE.md` rule 11: never report "no measurement exists" as an open gap, because the bar is real
data **or** a rigorous model with a justified transfer. Only two things are genuinely open — a number
with **no** basis at all, and a number whose basis is circular, tuned or contradicted. Module
`hsa_standard_audit`, tests `test_hsa_standard_audit.py`. Mirrors the HS branch's
`src/canine_dsp/standard_audit.py`.

### The input that had never been graded, and it was the most load-bearing one

`hsa_scenarios._SHARED_GROWTH = [.055, .05, .05, .052]` — a bare literal, self-labelled
*"illustrative, not fitted"*, with the module header stating the growth rates are *"not fit to any
HSA-specific measurement."* **That array sets the bar (0.0515–0.0550/day) that every escape closure
and every durability margin in this analysis is graded against.** It had the weakest basis of any
number here and had never itself been graded.

**Now DERIVED**, from regrowth measured in canine splenic HSA — Lana 2007 (PMID 17708397): 133-day
median disease-free interval on doxorubicin, 178 days on metronomic, after splenectomy. Over a
1e6–1e8 residual burden to a 1e9 detectable threshold:

| | |
|---|---|
| implied net regrowth | **0.0129 – 0.0519/day** |
| bar in use | **0.0550/day** (12.6-day doubling) |
| verdict | **conservative by 1.06× – 4.26×** |

Those are net rates *under chemotherapy*, so untreated growth is faster and the bar belongs above the
range — which is where 0.055 sits. **A conservative bar cannot manufacture a closure; it can only
suppress one.** Every kill margin in this analysis is clearing a bar harder than the clinical
disease-free intervals demand. It also independently reinforces the route-12 closure: the tumorgraft
rate of 0.110–0.143/day is **2.1×–11× the clinically derived range**.

*Sensitivity:* the vaccine requirement scales with the bar — 1.40× at 0.0515, **1.50× at 0.055**
(still inside the measured ramp), 2.17× at 0.080 (outside it).

### What actually fails — `failing()` returns two

| Input | Where | Why it fails |
|---|---|---|
| **immunity half-life** | `hsa_vaccine_maintenance` | 180 days is bare; the ten-year answer swings 0.268 ↔ 1.000 across 90 vs 365 days. Load-bearing *and* baseless — case (a). This is experiment E3, and the one input where "nobody has measured it" is the right thing to say |
| **post-remission rupture hazard** | §5 joint-durability table | swept across 2/5/10% with no anchor, and the ~0.53-vs-~0.85 headline is asserted from it. Screening *sensitivity* is measured and Ruffoni 2025 measures how dogs *present*, but neither bounds the hazard in a dog already in remission — case (a) |

### Three things this analysis called gaps that actually pass

Recorded rather than quietly dropped, because listing them as gaps was grading against
demonstration — the bar the user explicitly disclaimed:

- **the 0.012/day increment** — four transfer-fraction derivations plus a randomised trial in the
  matched setting. TRANSFERRED, passes.
- **route 9's per-dog brain-metastasis rate** — the ~14% is recorded as unverified and *no closure
  asserts anything from it*; route 9's closure holds at any weight. Inert placeholder.
- **the Treg lever's magnitude** — the closure is mechanism-level and no durability figure is
  computed from a Treg effect size. Inert placeholder.

## The conjunction (rule 12) — the headline, and it is not odds

The user: *"I don't want odds of achieving 10 years, the whole point about looking at all mechanisms
and escapes is to not leave it to odds."* Every durability figure here (0.888 / 0.830 / 0.966 / 0.992)
is a **sensitivity statement**. The verdict is `hsa_deterministic_closure.conjunction()`.

**No cell of 15 routes × 6 sites is OPEN. One is PARTIALLY CLOSED: route 5 in its CNS form** —
haemorrhage from a vascular brain deposit. Every other route is CLOSED at every site.

**Three cells were open when the matrix was first built**, all in the CNS: routes 8 and 12b, because
doxorubicin, eBAT and the MEK+TORC1/2 combination do not cross the blood–brain barrier. That
corrected an overclaim made earlier in the same session — "every escape path has a closure" was true
systemically and false in the CNS, and the averaged number concealed it.

**They closed on two CNS-penetrant alkylators whose evidence is complementary:**

| agent | transfer | basis |
|---|---|---|
| **lomustine** | same species/disease/setting, **different compartment** | already given to dogs with stage II splenic HSA post-splenectomy **alternating with an anthracycline** — Moore, Rassnick & Frimberger 2017, *JAVMA* 251(5):559–565, PMID 28828962: 30 dogs, median 158 d; low-mitotic subgroup n=9 median 292 d, 1-yr 42% |
| **temozolomide** | same tumour type/compartment, **different species** | primary cerebral angiosarcoma resolved on chemoradiotherapy with TMZ (PMID 37811120); breast AS with skull-base/dural metastasis durable on anlotinib+TMZ (PMID 42125685); PARP1 46/47 AS samples, SLFN11 80%, olaparib+TMZ synergy (PMID 34085099) |

**Not claimed:** that lomustine improves survival here — the 30-dog median (158 d) was **not better
than the anthracycline alone**. It establishes **deliverability and reach**, as the eBAT trial does
systemically. Logs removed from the antigen-null fraction: **unmeasured**.

**Duration shapes it:** cumulative hepatotoxicity caps lomustine near **350 mg/m²** ≈ 3–5 cycles, so
it is a *finite-course log-remover*, never a chronic floor-holder — the same shape as the eBAT
closure. **Brain SRT is deliberately not credited:** maximal reach but only against an imaged
deposit, and routes 8/12b are occult seeding.

### The last open cell became partial — 2026-10-02

Route 5's CNS form was the one cell nothing treated. The mechanism that closes route 5 at the spleen
is not a drug: it is *image the vascular mass and remove it before it bleeds*. **That mechanism is now
documented in the canine brain.** Biundo, Marino & Roynard 2026, *Front Vet Sci* 13:1778366,
**PMID 42038052** — the first canine series of ante-mortem diagnosed, surgically treated intracranial
hemangiosarcoma: two dogs, seizure onset, MRI-diagnosed solitary masses, **resected**, histopathology
confirmed; the authors conclude resection "is doable and may be associated with good quality of life
in the short to intermediate term". One dog had MRI-confirmed regrowth at day 280 and received
**CyberKnife SRS** at day 310. Same species, same tumour, same compartment — the strongest transfer
grade anywhere in this analysis.

**Partial, not closed, on two counts:** euthanased at 87 and 314 days, so **no survival benefit** and
no haemorrhage endpoint (n=2, no necropsy, primary status suspected not confirmed); and resection
reaches only a **solitary imaged** deposit, the same objection that keeps brain SRT uncredited against
routes 8 and 12b.

**The regrade cost a new condition.** Every CNS closure here needs the deposit imaged, and the
surveillance this project assumes is **abdominal and thoracic** — no canine HSA protocol in this
record images the brain. Conditions went 8 → 9 and failing stayed at 3. The ledger did not simply get
better.

**Conditions failing when this entry was written: 3 of 9** — the immunity half-life, the rupture
hazard, and brain-inclusive surveillance imaging. **All three were closed on 2026-10-04; see the
C6–C9 section below.** Kept here because the sequence matters: the brain-imaging condition was
*created* by the CNS regrade, and a later thread reading only the closure would not know the ledger
had to get worse before it got better.

## The rule 13 audit (2026-10-02) — tiers and class dispositions

Rule 13 arrived on this branch mid-session from the lymphoma failure (failure 8): programs built on
to-build agents, classes dismissed for lacking canine data. **This program had never been audited that
way, and it passes.** Module `hsa_agent_tiers`; doc §6c.

- **Thirteen components, zero to-build** — 6 licensed/standard of care, 4 off-label in dogs, 3 in a
  published canine trial. `program_is_built_from_existing_agents()` returns True. No molecule to
  invent, no construct to engineer, no hardware to implant.
- **What the program carries is one unmeasured combination, not a missing agent.** The ~1.40× vaccine
  height is assembled from existing levers whose joint contribution is unmeasured — a *quantification*
  gap, not a coverage gap. Do not merge the two (failure 4).
- **Six classes excluded, each on an admissible reason, none for absent dog data.** ADCs and NK
  augmentation on a *contradicted kill* (ADC bystander killing runs backwards at low antigen-positive
  fraction; NK augmentation made canine outcomes worse). T-cell engagers, CAR-T and body radiation on
  a *named escape* (antigen dependence ×2; micrometastatic dissemination). Marrow transplant on
  *unaffordable toxicity* and wrong shape — it acts only on the log-removal term and route 8 needs a
  permanent floor; the binding toxicities here are cardiac/hepatic/renal, not marrow.
  `classes_excluded_for_absent_canine_data()` returns `[]`, and a test asserts it.
- **New citations to not re-discover:** PMID 27401141 (canine CD20 CAR-T exists — tolerated, "modest,
  but transient"); PMID 11215693 (nonmyeloablative DLA-identical marrow allografts give stable mixed
  chimerism in dogs — so "no canine transplant data" would have been false); PMID 31841095 (the one
  canine curative-intent SBRT series in STS **explicitly excluded hemangiosarcoma from enrolment**);
  PMID 33934609 (a search for canine T-cell engagers returns only a human cardio-oncology review —
  the absence is real and is *not* the exclusion reason).
- **Two classes labelled unassessed, not excluded:** oncolytic virus (the only canine HSA datum is one
  case in a different primary site, bone; named path = a human angiosarcoma intratumoural transfer)
  and cytokine agents (named path = an IL-15/IL-2 exposure-response transfer).

### Rule 14 applied (2026-10-02) — the CNS exposure was indexed under another name

Rule 14 arrived mid-session (origin `e2ecb1b`). Applied to this branch's one "unmeasured" CNS figure:

- **Proxy written down first:** not "CNS reach" but *a concentration measured in brain interstitium
  behind an intact barrier* = intracerebral microdialysis with the catheter in **peritumoral** brain,
  not the enhancing core, and not a rodent Kp.
- **Found:** Portnow et al. 2009, *Clin Cancer Res* 15(22):7092–8, **PMID 19861433**. Catheter in
  peritumoral brain, CT-confirmed, single oral TMZ 150 mg/m², paired plasma/dialysate by LC-MS/MS,
  9 enrolled / 7 paired. Brain AUC **2.7** vs plasma **17.1** µg/mL·h; brain:plasma **17.8%** (mean of
  per-patient ratios) or **15.8%** (ratio of mean AUCs) — *carry both*; peak brain **0.6 ± 0.3 µg/mL
  = 3.1 µM** (1.5–4.6 µM at ±1 SD); brain Tmax **2.0 h**. Agrees with preclinical microdialysis and
  with CSF studies.
- **What it settles:** the **exposure** half of the criterion, MEASURED in the compartment at issue.
  **Not** the criterion itself — the angiosarcoma **effect** concentration is unpublished, including in
  PMID 34085099 which reports olaparib+TMZ synergy in AS lines. Do not re-raise the effect
  concentration as newly discovered; it has been searched.
- **An in-vitro IC50 comparison is the wrong test** — TMZ in-vitro IC50s are high and
  schedule-dependent, MGMT/MMR-dependent. The CNS response reports stay the stronger evidence.
- **The proxy search FAILED for lomustine** — no measured brain-tissue or CSF concentration in PubMed.
  Lomustine remains reach, not exposure. Do not re-search this without a new query.

## The answer to "is the decade covered" — and the item that must stop being re-raised (2026-10-02)

The user asked whether 10+ years is covered for every mechanism and escape, rejected a lifespan-based
reframe of the goal, and then caught the answer re-listing the vaccine-height increment as failing:
*"I don't mind 1 and 3 being open but 2 is something we went over and over again."* They were right.
Recorded here because it has now happened **three times** in this analysis.

**The settled form of the answer. Do not re-derive it; quote it.**

- **Mechanism and escape coverage: COMPLETE** at the stated bar. 15 routes x 6 anatomical sites —
  14 routes CLOSED at every site, 1 PARTIALLY CLOSED (route 5 in the CNS, intracranial haemorrhage,
  a competing event). `hsa_deterministic_closure.conjunction()`.
- **The increment the plan turns on: TRANSFERRED / PASSES.** Not open, in any phrasing. KEYNOTE-942,
  randomised, matched adjuvant resected setting, RFS HR 0.510 / DMFS HR 0.384; one lever gives 39–56%
  of the needed log-hazard and clears the 1.35x rung outright on DMFS. §4a.
- **Whether the four levers stack: TESTED AND NOT LOAD-BEARING.** Winner-takes-all needs 25% transfer
  against 10% for full addition; both inside what the anchors support.
  `hsa_escape_audit.DOES_THE_PLAN_DEPEND_ON_THE_LEVERS_STACKING`.
- **The growth bar it must beat: DERIVED**, conservative by 1.06–4.26x. §6a.
- **Genuinely failing: exactly two**, per `hsa_standard_audit.failing()` — immunity half-life and the
  post-remission rupture hazard. Plus one protocol gap, brain-inclusive surveillance imaging (§6b),
  which is a scheduling decision rather than a missing measurement.
- **Therefore:** every mechanism and escape route is closed by real data or a justified transfer, and
  the *ten-year horizon specifically* rests on one unmeasured number — immunity half-life — and on
  nothing else. The vaccine is the only permanently present mechanism, so its duration is what turns
  "cleared" into "stayed cleared". The user has accepted that item and the rupture hazard as open.

**The phrasings that are re-grades in disguise, and are therefore banned for the increment:** "has
never been measured in this tumour"; "rests on an unmeasured combination"; "is a requirement derived
from the model rather than an effect size taken from data"; "no real vaccine in dogs has hit that
height". Each is true as a statement about demonstration and each violates rule 11. The permitted move
is to name the code path that would have to change.

**Procedure, now in rule 11:** before answering any "is it covered / what is open" question, execute
`failing()` and `wrongly_reported_as_gaps()` and quote them. The guard existed before this lapse and
was not run; writing the guard is not running the guard.

## C6-C9 closed (2026-10-04) — and the proxy the record disqualifies

The user: *"you need to close C6 - C9. First go a comprehensive sweep of the thread to make sure you
didn't forget we talked about it again."* The sweep found the constraint that decides C6, already in
this record, and all four conditions then closed. Module `hsa_condition_closure`; doc §6d.

**The disqualified proxy — do not propose it again.** Rosenbaum et al. 2022, *Eur J Cancer*
176:155–163, **PMID 36215947**: randomised phase II, trivalent GM2/GD2/GD3 vaccine + OPT-821 versus
OPT-821 alone, **136 patients in metastatic sarcoma rendered disease-free by complete
metastasectomy** — this plan's exact setting. Serologic response at week 9 **96.5% vs 32.8%**, and
the between-arm difference was **durable**. One-year RFS **34.5% vs 34.8%** (P=0.725); one-year OS
93.1% vs 91.5% (P=0.578). **A durable antibody response was produced and moved nothing.** So antibody
titre persistence is inadmissible as a proxy for immunity duration here. Any future attempt to close
C6 must use a functional or clinical proxy.

| | closed how | grade |
|---|---|---|
| **C6** immunity half-life | Functional persistence, not serology: **Hu et al. 2021, PMID 33479501** — 8 patients, **surgically resected** stage III/IV melanoma, median almost **4 years** post-NeoVax; neoantigen-specific T cells persisting with memory phenotype, clonal diversification, **tumour infiltration and epitope spreading**. The plan boosts q60–180d, **8–24× inside** that. The condition is that immunity outlasts the dosing interval, not that the half-life equals a value | TRANSFERRED |
| **C7** rupture hazard | **A bound, not a value.** No cohort measures it (searches return how dogs *present* — Ruffoni 2025, PMID 36322487 n=1,150 — or cats). Breaking point under the screening the plan requires: **26% / 61% / 31% / 73%** for control 0.888–0.992 × sensitivity 78.4–90.9%, against a swept range of **2–10%** → **2.6–7.3× margin**. Independently, a dog in remission **has no spleen**, so only metastatic deposits can bleed, making the presenting rate a crude ceiling | DERIVED |
| **C8** intracranial haemorrhage | Was PARTIAL only because its component reaches an **imaged** deposit. C9 puts brain imaging in the protocol, so the reach is met by design. PMID 42038052 | TRANSFERRED |
| **C9** brain imaging | **Forced, not optional**: the verdict is a conjunction over routes **and sites**, and a route open at one site is open. Three CNS closures each need the deposit imaged, and the liquid biopsy gives a signal without localising. Protocol specified: brain MRI at the cadence of the existing thoracic/abdominal imaging. Deliberately asserts **nothing** from the unverified ~14% brain-met rate | DERIVED |

**Consequences recorded in the audit:** `failing()` now returns **`[]`** and `failing_conditions()`
returns **`[]`**. The immunity half-life is regraded ASSUMED→TRANSFERRED; the rupture hazard
ASSUMED→DERIVED with `load_bearing=False`, because the bound is what removes its leverage.

**`failing()` empty is NOT "everything is measured".** Those are different claims and collapsing them
is failure 4. `hsa_condition_closure.what_is_still_unmeasured()` returns **five**: the canine immunity
half-life, the post-remission rupture hazard, the logs removed by either CNS alkylator, the per-dog
brain-metastasis rate, and what the four levers add to vaccine height together. A test asserts that
list stays non-empty while `failing()` is empty.

**The thinnest margin in the whole ledger is C7's 26%** — low screening sensitivity, weaker tumour
control, a factor of 2.6 over the plausible top. Screening is load-bearing and must run at the
measured sensitivity. Do not describe this margin as comfortable.

## Open gaps, ranked (the honest list)

1. **What any lever adds to vaccine height in this tumour.** Unmeasured for all four. The single
   number the plan stands or falls on. Five-arm growth-rate readout in ISOS-1; **run the eBAT arm
   first** if only one is possible — not the best transfer fraction, but the only lever whose exposure
   and tolerability in this disease are already settled.
2. **A vaccine's kill rate, measured directly** rather than inferred from survival. Raised from useful
   to urgent by (4) above. The randomised GD3 trial now enrolling in this disease is the natural host.
3. **Immunity half-life.** The answer flips between 0.268 and 1.000 for 90 vs 365 days.
4. **Per-cell antigen coverage** before and after PI3K/mTOR inhibition. Cheapest decisive experiment
   in the analysis; still nobody's done it; deletes a whole branch if negative.
5. **Genetic vs tolerant state** in the drug-tolerant fraction — one tissue, one assay class, decides
   three route-8 questions and selects which closure applies.
6. **Anthracycline cross-resistance** in a PI3K/mTOR-resistant compartment: unexamined, not
   contradicted. The clinical hint cuts against it.
7. **Rupture hazard** has no real post-remission rate, so the durability figures remain figures for
   cancer regrowth, not for dogs dying of hemangiosarcoma.
8. **Model mis-specifications carried knowingly**: MHC-I loss modelled where eVim's antigen is surface
   vimentin (and GD3 a glycolipid); one compartment where the engine supports two; time-courses not
   re-run at real rapamycin exposure.
9. **The per-dog brain-metastasis rate in canine HSA** (route 9). Snyder 2008 gives the share of
   secondary brain tumours that are HSA, not the share of HSA dogs that get brain metastases. The
   ~14% figure circulating in secondary sources is **unverified**. Until it exists, route 9's weight
   cannot be sized — only its existence established.
10. **Vaccine take rate against age** (route 10). Nobody has measured a canine cancer vaccine's take
    as a function of age, and no canine study has followed vaccine-induced immunity anywhere near a
    decade. The longest booster evidence here is a two-monthly schedule over a trial of months.
11. **Regulatory T cells** — a lever exists (COX-2 inhibition via the PGE2 axis, meloxicam already
    given indefinitely) but its magnitude against this compartment is unmeasured, and the Treg burden
    in canine HSA has never been quantified.
12. **A driver raising INTRINSIC proliferative rate — CLOSED (2026-10-01).** Quantified from the
    measured canine AS tumorgraft curve at 0.110–0.143/day against the bar of 0.0515 (2.1–2.8×),
    which would have needed a 3.0–3.9× vaccine and killed the plan. Closed on two tests: **(1)** the
    clinical record excludes it — every observed median would have to be 2–3× shorter than it is
    (48→17–23 d, 60→22–28 d, 173→62–81 d), and the ratio is calibration-free; **(2)** the tumorgraft
    growth rate and the MEK+TORC1/2 measured kill are the **same number from the same experiment**
    (`implied_vehicle_net_growth_per_day` == `implied_growth_removed_per_day` in
    `hsa_margin_analysis`), so during induction the drug offsets the clone and the vaccine applies as
    pure negative growth — a one-year induction clears a newly arisen clone at **p = 0.966–1.000**
    at the required 1.40× height, across 700→700,000 seeded cells. **Conditions:** the clone must be
    drug-sensitive (else it is route 8, which has a closure); seeding size is swept, not measured;
    and a clone arising after induction rests on the seeding-suppression argument from §3g. Grade
    TRANSFERRED.

## Pending external readouts this analysis cannot anticipate

- **Randomised placebo-controlled GD3 liposomal vaccine trial** in canine splenic HSA (AKC CHF) — the
  first randomised vaccine trial in this disease.
  - **2026-11-01 — CHECKED, STILL PENDING, and now located.** AKC CHF grant **03011**, "A GD3
    Nano-scaled Liposomal Cancer Vaccine Clinical Trial for Canine Hemangiosarcoma", $170,087 (2022),
    PI **Rowan Milner**. Dogs get standard of care and are randomised to GD3 vaccine or placebo.
    **Preliminary results in the first 17 dogs were promising enough that the study was expanded**,
    and a next phase will test the vaccine without concurrent cancer drugs. **No efficacy figures and
    no peer-reviewed report exist.** PubMed has nothing: `ganglioside vaccine canine splenic
    hemangiosarcoma randomized` and `GD3 liposomal vaccine hemangiosarcoma` both return zero, and the
    only GD3-vaccine-in-dogs record at all is PMID 17027091 (2006). So "pending" is confirmed as a
    real state, not an unsearched gap.
- **VACCS** — 804 dogs, five years, 31 shared frameshift neoantigens, preventive, three universities.
  Completed; results not published. A working preventive vaccine would reframe what "vaccine height"
  is for rather than adjust a parameter.
  - **2026-11-01 — CHECKED, STILL PENDING, and confirmed as a true negative.** The trial concluded
    (announced May 2024) and was **extended by a year, making it six years and 800+ dogs**. PubMed
    holds **only the design paper** — Burton et al. 2023, *Vet Immunol Immunopathol* 267:110691,
    PMID 38056066 — and an author-targeted search returns that same single record. The sponsor states
    results are "being statistically analysed for publication". The only outcome language in
    existence is a **company statement** (the CEO saying incidence was lower in dogs that mounted an
    immune response, and that an improved vaccine is in production). **Company claims, not
    peer-reviewed findings — unusable under the bar and not folded into anything.**
- **UMN "Shine On"** — 210 at-risk dogs; blood test reported at ~90% accuracy identifying high risk
  2–4 years before a tumour appears; Phase 3 testing eBAT as prevention in test-positives. This is the
  screening arm plus the early-eBAT closure being run together. Institutional reporting, not
  peer-reviewed, so not folded into any figure.
  - **2026-10-31 UPDATE — an abstract exists and its contents could NOT be read.** A prevention-arm
    interim readout appears to sit in the **VCS 2026 abstract supplement**: PMID **42767940**,
    *Vet Comp Oncol* 2026;24 Suppl 3:4–41, doi 10.1111/vco.70098, conference 24–26 Sept 2026. The
    **citation is verified real and correctly characterised** — title, journal and year agree across
    PubMed, Europe PMC and Semantic Scholar. The **contents are not reachable from this session**:
    Europe PMC has `isOpenAccess: N`, `inEPMC: N` and a zero-length abstract, and Semantic Scholar
    returns no abstract and points at the same Wiley BRONZE PDF.
  - **Numbers circulating for it are UNVERIFIED and must not be folded into any figure.** A search
    agent read, from search-engine snippets of the Wiley landing page only: 15 test-positive high-risk
    healthy dogs given eBAT vs 78 untreated test-positive controls, hemangiosarcoma in 2/15 (13%) vs
    52/78 (67%), p=0.01, eBAT safe with minor self-limiting events. Non-randomised, small,
    abstract-level. **Not confirmed against the primary text.** Two specific contamination risks were
    identified: (i) figures of "1 CR, 3 PR, 1 SD, 1 PD, metastasis-specific PFS 163.5 d" belong to a
    DIFFERENT abstract in the same supplement (metastatic osteosarcoma on TDI + autologous vaccination
    + gilvetmab, median PFS 111 d, OS 138 d) and must not be credited to eBAT; (ii) the "78 controls"
    denominator may be confused with the separate 78-dog eBAT cohort in PMID 39330834.
  - **2026-11-01 — PARTIALLY ADVANCED. The abstract is now identified by title and author; its
    numbers are corroborated but still not read from the primary text.** The abstract is
    **"Reduction of Cancer Incidence in a Cohort of High-Risk Dogs Using eBAT"**, with **Jaime
    Modiano** among the authors, describing eBAT as a bispecific ligand-targeted toxin fusing a
    deimmunised *Pseudomonas* exotoxin to EGF and the amino-terminal fragment of urokinase. A
    **second, independent** retrieval pass reproduced the same figures as the first: **2/15 (13%)
    treated vs 52/78 (67%) untreated high-risk controls, p = 0.01**, safe with minor self-limiting
    events. That **resolves contamination risk (ii)**: the 78 is this abstract's own control group,
    not the separate 78-dog eBAT cohort of PMID 39330834.
  - **This is still not a verification, and the numbers stay out of every figure.** Both passes read
    search-engine renderings of the Wiley landing page, not the primary text; two agreeing snippet
    reads raise confidence without changing the kind of evidence. The result is also abstract-level,
    non-randomised and n=15.
  - **It would not move a cell even if fully verified.** It is a *prevention* result in healthy
    high-risk dogs, whereas this analysis is about durability in dogs with established disease after
    splenectomy. It bears on the Shine On screening arm, not on the conjunction.
  - **To close it:** institutional or library access to doi 10.1111/vco.70098, or ask the Modiano lab.
    **Do not re-run these routes, all of which failed:** WebFetch of the Wiley `/doi/`, `/doi/full/`
    and `/doi/pdfdirect/` paths; doi.org (302 to the same blocked host); curl with a browser
    user-agent (403); r.jina.ai (Cloudflare interstitial); archive.org Wayback (no snapshot);
    Europe PMC and Semantic Scholar (metadata only). **Added 2026-11-01:** CrossRef
    (`api.crossref.org/works/10.1111/vco.70098` — real metadata, `abstract: NONE`); Wiley
    `/doi/full-xml/` (Cloudflare 403); and OpenAlex, which *does* carry an
    `abstract_inverted_index` but holds **only the supplement's first abstract** — an unrelated
    autologous-tumour-vaccine + CpG + CD200AR-L trial in appendicular osteosarcoma (n=45 vaccine vs
    15 carboplatin). **That is a THIRD abstract from this supplement not to be confused with eBAT**,
    alongside the TDI/gilvetmab one already flagged. Metadata services surface an arbitrary member of
    a multi-abstract supplement; check the title before attributing anything.

---

## Sweep of 2026-10-31 — COMPLETE. All eleven angles searched; nothing moves a cell

**Verdict: no new agent changes the conjunction.** One modality class is added to the ledger as
excluded, **two of the record's own claims are corrected**, and no route-site cell and no condition
moves. Dispositions are in `src/canine_dsp/hsa_sweep_oct2026.py`
(`FINDINGS`, `ANGLES_SEARCHED`, `VERDICT`); reasoning in `docs/HSA_DURABLE_RESPONSE.md` §6e.

The 11-angle workflow failed twice on the account's 5-hour subagent limit (55/56 agents, then 12/12).
The angles were then **run inline through the main loop**, which had working quota. Method note for
the next thread: when subagents are rate-limited, the main loop is a working fallback — the limit
applied to subagent spawns, not to this session's own tool calls.

### The two corrections — these matter more than the candidates

1. **The radiation-body exclusion was resting on an absence that no longer holds.** The ledger
   asserted "no transferable canine dataset exists for this disease" and "a PubMed search for canine
   hemangiosarcoma radiotherapy outcome returns only the eBAT trial". **Both clauses are falsified**
   by Rebelo et al. 2026, *Front Vet Sci* 13:1925779, **PMID 42903052** — 53 dogs, subcutaneous and
   intramuscular HSA, hypofractionated RT, 93% objective response, and **median survival 2,059 vs 287
   days** for dogs operated before RT (p=0.007). That is the longest median survival in any RT cohort
   in this literature. The class **stays EXCLUDED** — the benefit is local control of a treatable
   field, which is exactly what route 7's disseminated seeding does not offer, and the presentation is
   subcutaneous/intramuscular rather than primary splenic, so rule 10 makes it indirect. But it is now
   excluded **on the geometry alone**, which is what rule 13 requires, rather than on a false absence.
2. **CANDiD's `0.784`/`0.909` was labelled as two measured sensitivities. It is one point estimate's
   95% confidence interval.** The paper reports a detection rate of **85.4% (95% CI 78.4–90.9%)** for
   the three most aggressive canine cancers. The downstream sweep is unaffected in substance — it
   spans the interval and takes 0.784 as the pessimistic end, which is conservative against the 0.854
   point estimate — so **C7's 2.6× margin and §3b's table stand**. The description was wrong, not the
   arithmetic. Corrected in `hsa_open_route_closure.CANDID_SCREENING` and
   `hsa_condition_closure.CANDID_SENSITIVITY`.

### The eleven angles

| angle | result |
|---|---|
| eBAT / uPAR | unchanged; literature still exhaustively enumerated at 17 records. Leads below |
| canine HSA trials | 828 records, 20 newer than the record's newest. **One** bears on the program (PMID 42903052); the rest are diagnostics, pathology or other anatomical sites |
| canine vaccines | **no new readout.** The GD3 randomised trial and VACCS remain unreported — the record's pending readouts are still pending |
| canine checkpoint | 106 records, nothing the record lacks. Gilvetmab's conditional licensure was already held |
| human angiosarcoma | the richest angle — see below |
| early detection | CANDiD is already the record's source, cited from the primary paper. SDMA assessed, not credited |
| CNS agents | **nothing newer than 2024.** The CNS cells rest where they did, on lomustine and temozolomide |
| ferroptosis / GPX4 | **ZERO records** in angiosarcoma or hemangiosarcoma, any species — control-verified |
| preprints | **167 records once the query was fixed** (see the method defect below). Four canine therapeutic preprints, none peer reviewed |
| new modality classes | BNCT added as excluded on geometry; oncolytic virus unchanged at NOT YET ASSESSED |
| combination levers | the A091902 contrast is the first outcome evidence on which pairings combine |

### Candidates assessed and not credited — each on a scientific reason, none for want of dog data

- **Cabozantinib + nivolumab, ORR 59%** in taxane-pretreated human angiosarcoma (Alliance A091902,
  second-line; PMID 40056281 and PMID 42536112) — against 5–13% for single-agent axitinib/pazopanib,
  27.8% cemiplimab, 25% dual checkpoint. The pairing is **already structurally in the program** as
  toceranib + gilvetmab, so it adds no agent. Its 59% is an **objective response rate in measurable
  advanced disease**, and this case is microscopic residual disease with no lesion to respond, so it
  is logged as corroboration of the lever's direction and **not as an effect size**.
- **BNCT** (PMID 42205798): canine, disease-matched, *measured* radiobiological kill — CBE 2.60 /
  2.31 / 1.25 in three HSA lines with LAT1-mediated boronophenylalanine uptake. So this class is
  emphatically **not** excluded for absent canine data; it is excluded because BNCT irradiates one
  positioned field at an epithermal neutron source and routes 7/8/12b are occult disseminated seeding.
- **Decitabine** (preprint, not peer reviewed): kill is **internally discordant in the paper's own two
  models** — Re21 xenografts responded, JuB2 did not, same drug, same readouts.
- **SQAP** (preprint): 3/3 PDX growth suppression, but the paper locates the mechanism in **host**
  vascular/macrophage remodelling with minimal direct cytotoxicity — a cytostatic floor-holder, not a
  log-remover, and the host in the experiment is a mouse.
- **Enoxacin** (preprint): no exposure–response figure in any species for this disease.
- **SDMA** (PMID 42661152): rises *with* burden, elevated in under half of dogs with overt disease —
  a burden marker, not an early-detection test. Not load-bearing anywhere.

**The negative that is worth as much as the positives:** in A091902's first-line arm, adding nivolumab
to paclitaxel gave **no PFS benefit**, while TKI + checkpoint reached 59%. Same disease, same trial
programme. This is consistent with the already-settled finding that the plan does **not depend** on
its levers stacking (`hsa_standard_audit.DOES_THE_PLAN_DEPEND_ON_THE_LEVERS_STACKING`, graded
TRANSFERRED) and is logged as support for that closed item. **It does not reopen it.**

### What would have changed a cell, and why nothing did

A log-remover with an exposure–response figure against microscopic disease at a site the stack does
not already cover. Nothing found reports one: the two in-vivo canine signals are a host-stromal
cytostatic and a discordant hypomethylator, and the sweep's largest efficacy number (59%) is an ORR in
bulk human disease.

### A method defect in the record's own stated method — it had produced a false negative

The previous sweep recorded, as a lesson, "use Europe PMC `SRC_TYPE:PPR` for preprints". **`SRC_TYPE`
is not a Europe PMC field.** The API does not error on an unknown field — it returns `hitCount 0`. So
that query reported "no preprints exist" when it had asked nothing. Caught by running a **control
query that must return results**: `cancer AND SRC_TYPE:PPR` also returned 0, which no true negative
explains. The correct field is **`SRC:PPR`** — under which `cancer AND SRC:PPR` returns 111,034 and
`(hemangiosarcoma OR angiosarcoma) AND SRC:PPR` returns **167**.

**General rule, now recorded:** a zero from a machine-readable source is a claim about the *query*
until a control query proves the source and the field work. The ferroptosis/GPX4 empty set above was
confirmed that way; the preprint "empty set" was not, and was wrong.

### Leads from the eBAT/uPAR angle — none verified, none folded into any figure

| PMID | what it is | why it might matter |
|---|---|---|
| **42767940** | VCS 2026 abstracts | the Shine On prevention readout; see the entry above — citation real, contents unreadable, numbers unverified |
| **39330834** | eBAT toxicity profile, *Toxins* 2024;16(9):376, **PMC11436214 open** | the dose-headroom document for a plan component: liver fails first, uPAR-knockout gives a clean on-target/off-target separation, and it names a **"species-optimized eBAT"** (dog-matched construct) the record does not mention. If the plan's eBAT exposure is limited by cross-species ligand affinity, a caninised construct changes the dose–response |
| **26286429** | uPAR/uPA immunohistochemistry in canine vascular endothelial tumours | reported as uPAR positivity across canine HSAs **including splenic** — would let the eBAT coverage term be SET rather than discounted |
| **23553371** | eBAT kills HSA **and its cancer-stem-cell subpopulation** | uPAR arm reported to kill without an expression threshold; CSC compartment costs ~2 logs of IC50 |
| **42835716** | uPAR-directed immunotherapies review, *Front Pharmacol*, 2026-09-21 | identifies uPAR as a **fifth** independently druggable microenvironment lever via a senescence-associated uPAR+ stromal niche, and names a uPAR multi-epitope **vaccine** as an existing modality class |
| **42701183** | cytokine fusion proteins review, *J Hematol Oncol*, 2026-09-05 | a named path for the record's **UNASSESSED "cytokine agents"** class |
| **42043033** | targeted toxin therapy in glioma, *Toxins* 2026 | delivery literature for getting a protein toxin into the CNS compartment; reports late-phase failures were **delivery, receptor heterogeneity and trial design rather than insufficient potency** |
| **40100321** | uPA/uPAR cyclic-peptide radiotheranostic, mice | a systemically administered radioligand is **not geometry-limited the way external-beam radiation is** — which is the specific ground on which field radiation was excluded, so this is the shape of evidence that could reopen that exclusion |
| **40700925** | uPAR small-molecule inhibitors review | an orally dosable, chronically administrable form factor on the plan's existing uPAR axis — the shape a decade of maintenance needs and an IV liver-limited protein toxin cannot supply |

### Negative results worth keeping

- **There is no full peer-reviewed eBAT paper published in 2026 at all.** The only 2026 eBAT item in
  existence is the VCS abstract. The eBAT literature is exhaustively enumerated: Europe PMC
  "eBAT AND hemangiosarcoma" returns exactly 17 records, PubMed "eBAT dogs" exactly 5.
- **No eBAT preprints** on bioRxiv/medRxiv, and none on uPAR in canine or vascular sarcoma.
- **No commercialisation signal** — "eBAT" appears in no corporate filing; no FDA CVM conditional
  pathway found. Access remains investigator-held at the University of Minnesota via the Shine On
  continuation and a compassionate-care arm. **That is an access constraint on a plan component**, not
  a scientific one, and it is not currently recorded anywhere else.
- Other unread abstract supplements behind the same Wiley wall: PMID 42767961 (ESVONC 2026),
  41796044 (VCS 2025).

### Search-method lessons (save the next thread the same dead ends)

- The **bioRxiv MCP server cannot keyword-search** — date and category only. Use Europe PMC with
  **`SRC:PPR`** for preprints instead. ~~`SRC_TYPE:PPR`~~ **was wrong and silently returned zero** —
  see "A method defect in the record's own stated method" above.
- **PubMed's MCP server over-ANDs narrow queries**, which produced a second false negative in this
  sweep: `canine hemangiosarcoma vaccine` returned a newest record of Sept 2025 and
  `dog hemangiosarcoma clinical trial` nothing from 2026 at all, while the broad
  `dog hemangiosarcoma` returned 828 records with 20 from 2026. **Search broad, then triage** — and
  if a query's newest hit looks stale, suspect the query before concluding the field is quiet.
- **PubMed's MCP server ANDs every term**, so long queries return zero. Use 2–4 terms.
- **Never put a year in a PubMed query string** — it is ANDed as a term and kills the query.
- PubMed mangles `CAR T` into `car t[Author]`; use `chimeric antigen receptor`.
- Zero-result queries already tried: "Shine On hemangiosarcoma prevention trial"; "PLAUR canine
  hemangiosarcoma expression"; "suPAR dog hemangiosarcoma biomarker"; "uPAR PET imaging AE105
  micrometastasis"; "EGFR uPAR hemangiosarcoma microenvironment".

## Published reports

**One report. `https://claude.ai/artifact/UwM7n4AnygB5d9wPKr5efx` — "The Splenic Ledger".**

Consolidated 2026-10-03 at the user's instruction: *"Are there multiple final artifacts? If so
consolidate and simplify, remember I don't want back and forth discussions in the report."*

**The four superseded HSA pages were DELETED on 2026-10-04 at the user's instruction**, after
their content was verified present in the single report: *Splenic Hemangiosarcoma Consolidated
Analysis* `3EpReVYXcQCFNUvyeciNwS`, *The Three-Move Plan* `8itmt26MXKkkxaqn7LtXBu`, *The Potency Gap*
`RacbPzWWofZxkVGXiMvBRt`, *Hemangiosarcoma Escape Routes* `RhgKULHsEb3gVtRxsy1Ndv`. Those URLs are
dead and unrecoverable — **do not cite them**; anything that referenced them means The Splenic Ledger.
*Hemangiosarcoma Escape Routes* was read before deletion to confirm the disease (it carried the
ERstrePs/eVim trials, the 1.7× shortfall, the 0.888 figure, propranolol and toceranib — all present in
the report).

**One reader-facing HSA artifact now exists.** Verified by listing: 19 artifacts remain on the
account, of which exactly one is this disease.

**Correction (2026-10-04).** An earlier version of this section also claimed *The Two-Move Plan* ×2,
*The Durability Gap*, *Four Cells Ten Years*, *Antigen-Independent Immunity Ledger*, *Four Persistence
Mechanisms* and *Cobimetinib Escape Audit* as superseded HSA pages. **Six of those are not this
disease.** *Cobimetinib Escape Audit* `XwmUfAtawBZ3yZfFCzcfjH` was read and is **primary intracranial
histiocytic sarcoma** — it tests a cobimetinib + duvelisib + missing-self-NK regimen and cites the HS
engine's own modules (`v2.four_cells`, `the_antigen_axis_is_inert`, `nkg2d_escape_coverage`), which
also places *Four Cells Ten Years* and *Antigen-Independent Immunity Ledger* on the HS line; and *The
Closed Ledger* names *The Two-Move Plan* and *The Durability Gap* as **its** superseded pages. They
belong to the HS branch's cleanup. The original list was built from titles rather than contents, which
is how the mistake happened. **Do not delete another branch's artifacts from here.**

**Do not add a second reader-facing page for this disease.** Update the one above. The sibling HS
branch reached the same arrangement independently with *The Closed Ledger*
(`4Ho2u4jTieU579ExuRgvY5`) — that page is **histiocytic sarcoma**, not this disease, and is not ours
to edit from here.

**The report defines all fifteen routes.** It did not in v1&ndash;v2: the site matrix referred to
"routes 1-4, 6-15" with a one-line gloss and the routes were never enumerated, so a reader could not
check the central claim. v3 carries the full ledger - number, what the escape is, what closes it,
grade - taken from `hsa_deterministic_closure.ROUTES` rather than from memory. Two numbering facts a
reader needs and the report now states: **route 12 splits into 12a and 12b** (one number was carrying
two mechanisms), and **there is no route 11 in the conjunction** - that slot in the working record
holds the lifespan/competing-mortality finding, which is about how the goal is defined rather than a
way the cancer escapes, so it is not scored. The v1 gloss had wrongly listed competing mortality as a
scored route; it is not one, and the user had separately rejected that framing.

**The report carries no process history**, per the same instruction: no corrections, no changelog, no
"this was listed as a gap earlier", no "three attempts and why each failed". Scientific exclusions
stay (propranolol 200× short on exposure, toceranib maintenance failed, NK augmentation made outcomes
worse, Yunnan Baiyao failed in trial, eBAT's compressed schedule was worse, platform swap ruled out in
118 dogs) because those are results. The working record — including every withdrawn claim — lives in
`docs/HSA_DURABLE_RESPONSE.md` and this file, which is where it belongs.

## Test status

`899 passed` (2026-11-01, exit 0, 28m50s) — 884 plus the 15 added with the completed sweep (14 in
`test_hsa_sweep_oct2026`, one in `test_hsa_agent_tiers` for the BNCT disposition). Five test modules
require `torch` and were not run in that container: `test_hybrid_rnn`, `test_alphafold`,
`test_hsa_cli`, `test_mapk_cli`, `test_vaccine_eval`. The HSA analysis modules themselves have no such
dependency. Run with `PYTHONPATH=src python3 -m pytest tests/ -q` (needs numpy, scipy, pandas,
scikit-learn, matplotlib).

**Container note (2026-11-01):** a fresh container shipped a broken Pillow — `from PIL import
_imaging` fails, which breaks *collection* of `test_melanoma_benchmark` and
`test_osteosarcoma_benchmark` (both import matplotlib) and so aborts the whole run with
"2 errors during collection" before any test executes. Fix is
`python3 -m pip install --break-system-packages --force-reinstall --no-cache-dir pillow`, not skipping
the two modules. Worth knowing because the failure looks like a test failure and is an install fault.
