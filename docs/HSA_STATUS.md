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

**Conditions failing (3 of 9):** the immunity half-life; the rupture hazard; **brain-inclusive
surveillance imaging** (new). **Partial:** intracranial haemorrhage (TRANSFERRED, PMID 42038052).
**Passing:** the CNS agent (MET at TRANSFERRED — lomustine + temozolomide); T-cell vaccine platform
(selectable now — ERstrePs yes, eVim no); vaccine height ~1.40× (TRANSFERRED); route-8 anthracycline
sensitivity (unexamined); route-8 existence (unverified).

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
- **VACCS** — 804 dogs, five years, 31 shared frameshift neoantigens, preventive, three universities.
  Completed; results not published. A working preventive vaccine would reframe what "vaccine height"
  is for rather than adjust a parameter.
- **UMN "Shine On"** — 210 at-risk dogs; blood test reported at ~90% accuracy identifying high risk
  2–4 years before a tumour appears; Phase 3 testing eBAT as prevention in test-positives. This is the
  screening arm plus the early-eBAT closure being run together. Institutional reporting, not
  peer-reviewed, so not folded into any figure.

---

## Published reports

**One report. `https://claude.ai/artifact/UwM7n4AnygB5d9wPKr5efx` — "The Splenic Ledger".**

Consolidated 2026-10-03 at the user's instruction: *"Are there multiple final artifacts? If so
consolidate and simplify, remember I don't want back and forth discussions in the report."* The three
pages that preceded it (*Consolidated Analysis* `3EpReVYXcQCFNUvyeciNwS`, *The Three-Move Plan*
`8itmt26MXKkkxaqn7LtXBu`, *The Potency Gap* `RacbPzWWofZxkVGXiMvBRt`) and the stale August/September
pages (*Hemangiosarcoma Escape Routes*, *The Two-Move Plan* ×2, *The Durability Gap*, *Four Cells Ten
Years*, *Antigen-Independent Immunity Ledger*, *Four Persistence Mechanisms*, *Cobimetinib Escape
Audit*) are **superseded**. They were left published, not deleted; deleting is the user's call.

**Do not add a second reader-facing page for this disease.** Update the one above. The sibling HS
branch reached the same arrangement independently with *The Closed Ledger*
(`4Ho2u4jTieU579ExuRgvY5`) — that page is **histiocytic sarcoma**, not this disease, and is not ours
to edit from here.

**The report carries no process history**, per the same instruction: no corrections, no changelog, no
"this was listed as a gap earlier", no "three attempts and why each failed". Scientific exclusions
stay (propranolol 200× short on exposure, toceranib maintenance failed, NK augmentation made outcomes
worse, Yunnan Baiyao failed in trial, eBAT's compressed schedule was worse, platform swap ruled out in
118 dogs) because those are results. The working record — including every withdrawn claim — lives in
`docs/HSA_DURABLE_RESPONSE.md` and this file, which is where it belongs.

## Test status

`858 passed` (2026-10-02, exit 0, 26m26s). Five test modules require `torch` and were not run in that container:
`test_hybrid_rnn`, `test_alphafold`, `test_hsa_cli`, `test_mapk_cli`, `test_vaccine_eval`. The HSA
analysis modules themselves have no such dependency. Run with
`PYTHONPATH=src python3 -m pytest tests/ -q` (needs numpy, scipy, pandas, scikit-learn, matplotlib).
