# Durable response in canine hemangiosarcoma

What carries a lasting remission, how the tumour escapes, what closes each escape route, and what
10-year control would actually require.

This document is the narrative record for the HSA pipeline. The modules under `src/canine_dsp/`
carry the code and the constants; the reasoning, provenance and caveats live here. Every figure is
recomputed from the engine by the tests named in each section.

**Nothing here is a treatment recommendation.** Growth rates, kill ceilings and vaccine potency are
illustrative placeholders swept across ranges, not fitted measurements. What is real and cited: the
cell-line potency, the drug exposure, the trial survival figures, and the toxicity data. No
combination described here has been given to a dog.

---

## 1. The bar

A tumour is a mixed population, and treatment sorts it. Most cells are drug-sensitive and die; a few
carry a resistance change and regrow. For each resistant cell type, ask whether it is still growing
under treatment and how fast. That per-day growth rate is its head start, and any mechanism meant to
prevent relapse must out-kill it — not slow it, out-pace it.

Take the fastest-growing resistant clone and you get one number: **the bar**, about **0.052/day**.

`clone_growth_margins` against `dog_hsa_preset`:

| Exposure assumption | sensitive | pi3k_akt | mapk_cross | target_site | **bar** |
|---|---|---|---|---|---|
| assumed 5× IC50 (module default) | −0.0919 | +0.0490 | +0.0230 | +0.0515 | **0.0515** |
| de-rated to 40% for toxicity | −0.0632 | +0.0497 | +0.0291 | +0.0519 | **0.0519** |
| real rapamycin trough (10.9 nM) | +0.0545 | +0.0500 | +0.0499 | +0.0520 | **0.0545** |
| **no drug at all** | +0.0550 | +0.0500 | +0.0500 | +0.0520 | **0.0550** |

*Tests: `test_hsa_durable_response_analysis.py::test_the_bar_is_nearly_unchanged_by_the_drug`*

### The drug is nearly irrelevant to durability

Full dose to **no drug at all** changes the bar by 7%. The inhibitor drives the sensitive clone
deeply negative — which is why patients respond — and moves the three resistant clones by 1–2%. It
decides how fast the tumour shrinks and almost nothing about whether it returns.

Sharper still: the lab potency comes from VDC-597 (real, on canine HSA cell lines) and the dose from
rapamycin (the drug actually used in dogs). Rapamycin's real measured trough is >10 ng/mL = 10.9 nM
(Paoloni et al. 2010, PMID 20543980) against VDC-597's 543 nM mean IC50 (Pyuen et al. 2018,
PMID 30011343) — **50× below IC50**. At that exposure the sensitive clone is not suppressed either
(+0.0545 vs +0.0550 untreated). The modelled inhibitor is a hypothetical agent ~250× more potent
than rapamycin.

This is a **scoping correction, not a retraction**: the drug was never carrying durability, so
over-stating its exposure inflates response *speed*, not the vaccine threshold.

---

## 2. Achievability: what real vaccines deliver

Unlike the histiocytic-sarcoma pipeline, which has no vaccine trial in its disease, HSA has two real
Phase 2 trials in the actual disease.

| Trial | n | Vaccinated 1-yr | Control 1-yr | Gain |
|---|---|---|---|---|
| ERstrePs (Marconato et al. 2023, PMID 37686485, *Cancers* 15(17):4209) | 28 vs 32 | 35.7% | 6.3% | +29.4 pp |
| eVim (Engbersen et al. 2025, PMID 41009669, *Int J Mol Sci* 26(18):9096) | 23 | 44% | 14% | +30.0 pp |

Engine, 1-year durable response at `_PREEXISTING_PROB_CENTRAL = 0.70`:

| `vaccine_max_kill` | 0 | 0.01 | 0.02 | **0.03** | 0.04 | 0.05 |
|---|---|---|---|---|---|---|
| 1-yr durable | 0.338 | 0.443 | 0.508 | **0.647** | 0.848 | 1.000 |

+30 pp lands at ≈ **0.03/day** against a bar of **0.052/day** — short by about **1.7×**.

Two ways this comparison is loose, neither hidden:

1. **Endpoint.** The trials report overall survival; the engine reports progression from nadir. HSA
   is the disease where these diverge most, because rupture kills independently of regrowth. Survival
   ≤ progression-free, so matching them *overstates* the implied potency. 0.03/day is an upper bound
   and 1.7× a lower bound on the shortfall.
2. **Baseline.** The engine's no-vaccine 1-year figure (0.338) is ~5× the real control arms. Matching
   the *increment* rather than the level is what makes the comparison usable, and assumes the
   increment transfers across that mismatch.

*Tests: `test_real_trial_implied_potency_falls_short_of_the_bar`*

---

## 3. Height is not persistence

**This is the answer to "does it just take boosters?"** No — and the reason is that a vaccine has two
independent properties, and the shortfall is in the one boosters cannot touch.

- **Height** — how hard the response kills (`max_kill`). Must exceed the bar. Currently ~0.03 vs 0.052.
- **Persistence** — how long it stays at that height. This is what boosters buy, and all they buy.

### Boosters do not substitute for potency

10-year durable response, boosting every 60 days against never waning at all:

| `max_kill` | engine (never wanes) | wanes 180 d, boosted q60d |
|---|---|---|
| 0.03 *(what real trials imply)* | 0.492 | 0.492 |
| 0.04 | 0.536 | 0.536 |
| 0.05 | 0.924 | 0.916 |
| 0.06 *(above the bar)* | 1.000 | 1.000 |

Below the bar, boosting forever changes nothing to three decimal places. You cannot re-dose your way
over a threshold you are under — each booster restores the same insufficient height.

*Tests: `test_hsa_vaccine_maintenance.py::test_boosters_do_not_substitute_for_potency`*

### But boosters are still required — for a different reason

The engine's vaccine ramps to `max_kill` and stays there forever, with no waning. That assumption is
doing enormous work. At threshold potency (0.06), 10-year durable response by immunity half-life:

| immunity half-life | no boosters | boost q180d | boost q60d |
|---|---|---|---|
| 90 d | 0.268 | 0.528 | 1.000 |
| 180 d | 0.300 | 1.000 | 1.000 |
| 365 d | 0.296 | 1.000 | 1.000 |
| never wanes *(engine default)* | 1.000 | 1.000 | 1.000 |

With realistic waning and no boosters, the headline 1.000 collapses to roughly the **no-vaccine**
level. And maintenance cannot be a course:

| q60d maintenance stopped after | 1 yr | 2 yr | 5 yr | never stop |
|---|---|---|---|---|
| 10-yr durable | 0.276 | 0.436 | 0.536 | **1.000** |

**So 10-year control needs both**: potency above 0.052/day, *and* lifelong boosting at an interval
matched to the immunity half-life. `required_booster_interval` gives ~57.9 days to hold 80% of peak
against a 180-day half-life. eVim's real two-monthly schedule holds **79.4%** — right at that
threshold rather than clear of it, and well short of it if canine immunity to this antigen halves
faster than 180 days, which nobody has measured. Boosters are necessary and not sufficient; potency
is the unsolved half.

*Tests: `test_at_threshold_potency_waning_without_boosters_collapses_ten_year_durability`,
`test_stopping_maintenance_forfeits_durability`*

---

## 3b. Three attempts to close the gap, and why each fails

Sections 2 and 3 leave the vaccine ~1.7× too weak. Three routes look like they close it. Checked
against what the evidence supports, **none of them does**, and this section records why — each is
the kind of route that survives arithmetic but not scrutiny.

### Route A — lower the bar instead of raising the vaccine

The bar is `growth − kill`, so a second persistent mechanism-agnostic agent should clear it from the
other side. The arithmetic works. Holding the vaccine at the real achievable 0.03/day:

| persistent agnostic kill | bar after it | 10-yr durable |
|---|---|---|
| 0 | 0.0515 | 0.492 |
| 0.02 | 0.0331 | 0.832 |
| **0.03** | **0.0240** | **1.000** |

**The anchoring destroys it.** Metronomic oral chemotherapy was the candidate. Anchor it the way
vaccine potency was anchored — find the rate reproducing the real trial's numbers — and no rate
does. As an agnostic agent alone the model gives a median time-to-progression of 10 d at 0.02,
20 d at 0.03, 41 d at 0.035, 72–81 d at 0.04–0.045, then never progresses at 0.05. It is a cliff,
not a gradient: **the maximum reachable median is 81 days against a real disease-free interval of
178 days** (Lana et al. 2007, PMID 17708397).

Worse, 178 days is almost exactly what the modelled **inhibitor-alone** arm gives (174 days) — the
arm that moves the bar by 7% and does not clear it. So metronomic chemotherapy's own trial places it
with the agents that fail, not the ones that succeed. Route A is not supported.

*What metronomic cyclophosphamide does have real canine evidence for is immunological, not
cytotoxic*: it selectively depletes regulatory T cells and inhibits angiogenesis in dogs (Burton
et al. 2011, PMID 21736624), and prolonged disease-free interval at P < 0.0001 in 30 dogs versus 55
matched controls (Elmslie et al. 2008, PMID 18976288), at a cost of sterile cystitis in 40%. That
mechanism acts on the **height of the vaccine already present**, not as an independent kill term —
a different proposition, and an unquantified one.

### Route B — two vaccines instead of one

ERstrePs and eVim target different antigens through different effector arms, so on paper they add:
0.03 + 0.03 = 0.06 clears the bar and gives 1.000 at ten years.

**Antigenic competition destroys it.** B cells compete for restricted T-cell help, suppressing the
subordinate response 10-fold at 2× antigen excess and 100-fold at 10× — stable across a 6-log dose
range, apparent within 10 days, and **resistant to boosting and adjuvants** (Woodruff et al. 2018,
Cell Rep 25(2):321-327.e3, PMID 30304673). The source names immunodominance explicitly as an
obstacle to polyvalent vaccination. eVim is an antibody vaccine — precisely the arm this suppresses.

| scenario | combined | clears bar? | 10-yr durable |
|---|---|---|---|
| perfect additivity | 0.0600 | yes | 1.000 |
| weaker arm suppressed 2× | 0.0450 | **no** | 0.540 |
| weaker arm suppressed 10× *(Woodruff's weakest)* | 0.0330 | **no** | 0.500 |
| weaker arm suppressed 100× | 0.0303 | **no** | 0.516 |

The pair tolerates a **28%** loss in the weaker arm. The weakest suppression Woodruff reports is
10-fold — a **90%** loss. Route B fails under any documented level of competition, and the
competition cannot be dosed or adjuvanted around.

This is an interference problem, not a safety one: both trials individually reported no
vaccine-related toxicity (PMID 37686485, PMID 41009669).

### Route C — booster-interval tolerance is not a route at all

Immunity only has to stay above the bar, not near peak, so headroom buys interval tolerance:

| max_kill | may decay to | q-interval @ hl=90 d | @ hl=180 d | @ hl=365 d |
|---|---|---|---|---|
| 0.06 | 85.8% | 20 d | 40 d | 80 d |
| 0.08 | 64.4% | 57 d | 114 d | 232 d |
| 0.10 | 51.5% | 86 d | 172 d | 349 d |

Every row requires potency **above** the bar. `tolerable_booster_interval` returns exactly 0.0 for
any potency at or below it. Route C is a consequence of having closed the gap, never a way of
closing it — presenting it alongside A and B as a third option was a category error.

### Where that leaves it — and what does work

Those three failed because they all attacked the same side of one equation. The bar is
`max_clone(growth − drug_kill)`, and every route above tried to add kill. Two things were never
tried: correcting how much resistance the model grants, and reducing **growth** itself.

#### Component 1 — match the resistance to the drug, which costs nothing

`_SHARED_IC50_RATIOS` grants 35× resistance to `pi3k_akt_feedback_reactivation` and 50× to
`target_site_mutation`. Both are **rapalog** resistance mechanisms — the module documents the second
as "(FKBP12-mTOR binding site) mutation reducing **rapamycin** binding". But the potency anchor is
VDC-597: a dual PI3K/mTOR inhibitor with kinase-assay IC50s of 19 nM and 14 nM, i.e.
**ATP-competitive**, binding the kinase domain rather than FKBP12.

The dual PI3K/mTOR class exists specifically to defeat both mechanisms. Rapamycin causes feedback
AKT activation while the dual inhibitor PI-103 does not, and is more effective (Kharas et al. 2008,
*J Clin Invest* 118(9):3038-50, PMID 18704194); the class was "developed with the idea of overcoming
resistance to mTOR inhibition through preventing the activation of PI3K/Akt as a result of release
negative feedback loops" (Gomez-Pinillos & Ferrari 2012, PMID 22520976).

The module cannot have it both ways. If the drug is rapamycin, the mechanisms fit and the IC50
anchor is the wrong drug. If it is VDC-597, the anchor fits and the two ratios are far too high.
**The measured fold-shifts.** Rodrik-Outmezguine et al. 2016 (*Nature* 534(7606):272-6, PMID
27279227) built both resistance classes in isogenic cells and cross-tested them. They are
**reciprocal, not additive**:

| mechanism | vs rapamycin | vs ATP-competitive (AZD8055 / MLN0128) |
|---|---|---|
| FRB / FKBP12-site mutation (A2034V, F2108L) | resistant — S6K T389 unaffected at 100 nM rapalog | **"maintained full sensitivity to AZD8055 and RapaLink-1"** → 1.0× |
| kinase-domain M2327I | **"retained full sensitivity to rapamycin"** | **"3 to 30 fold higher"** → 9.5× (geometric mean) |

So the correction is not a matter of scaling 50× down to something small. The model's
`target_site_mutation` — explicitly a FKBP12-binding-site mutation — confers **no resistance at all**
to the drug its potency anchor describes, while the mechanism that *does* resist ATP-competitive
inhibitors is absent from the model entirely.

Measured ratios `[1.0, 9.5, 1.15, 1.0]` take **the bar from 0.0515 to 0.0445**. Durable response
goes 0.492 → **0.500** — under one point. The residual is now a *potency* limit (the kinase-domain
clone at 9.5×), sitting above a hard efficacy floor at about **0.038/day** set by `max_kill` for
`target_site_mutation`, which no IC50 change can pass. Even a perfect drug leaves the vaccine short.

#### Component 2 — reduce growth, not kill — and the exposure that decides it

HSA is an endothelial tumour, and β-adrenergic blockade acts on proliferation rather than supplying
a kill term. ADRB1 and ADRB2 are expressed in transformed endothelial cells and in angiosarcoma
tumours (Pasquier et al. 2016, *EBioMedicine* 6:87-95, PMID 27211551).

**But "reduce growth by 29%" is a requirement, not a drug.** `hsa_growth_pharmacodynamics` puts real
numbers on both sides of it — a Hill/Emax curve whose EC50 is inverted from measured dose-response,
evaluated at measured canine exposure:

| quantity | value | source |
|---|---|---|
| propranolol antiproliferative threshold | **25 µM** (15–67% reduction across lines) | Stiles et al. 2013, PLOS ONE 8(3):e60021, PMID 23555867 |
| achieved in dogs at 1.3 mg/kg three times daily | **18.7 ng/mL = 0.072 µM** | PRO-DOX, Borgatti et al. 2025, PMID 40386412 |
| **gap** | **~350×** | |
| implied growth suppression | **0.05–0.6%** | Emax fit |
| required | **28.9%** | this model |
| plasma level that would be needed | **~3,792 ng/mL — 203× what the trial achieved** | |

Run through the stack, propranolol at its real exposure returns **0.500 on every anchor** — bit for
bit the correction-only figure. It contributes nothing measurable.

This is also a better explanation of PRO-DOX than the partner-drug hypothesis in §"Is propranolol the
only option": the drug never reached an active concentration. Unlike the partner hypothesis, it
predicts propranolol **with vinblastine** would fail too.

**Does this criterion reject everything?** A screening rule that disqualified every candidate would
be worthless, so it needs a control. Toceranib is it. Bernabe et al. 2013 (*BMC Vet Res* 9:190,
PMID 24079884) measured 2.4–2.9 mg/kg every other day reaching **100–120 ng/mL**, which the authors
call *"well above the 40 ng/ml concentration associated with target inhibition"* — and confirmed
engagement pharmacodynamically, with plasma VEGF rising significantly over 30 days. It was still
negative in 43 dogs.

So the two negative trials mean opposite things:

| | reached its own threshold? | what the negative means |
|---|---|---|
| propranolol | no — **0.003×** | **uninformative** — PRO-DOX tested a dose, not a hypothesis |
| toceranib | yes — **2.75×**, engagement confirmed | **informative** — target hit, no benefit in 43 dogs |

The criterion discriminates: one agent fails before biology is reached, the other fails on biology.

*Scope limit.* Toceranib's targets are VEGFR/PDGFR/KIT — angiogenic and stromal rather than the
tumour cell's own proliferation rate. Its failure indicts the **anti-angiogenic route**, not growth
reduction as a category. The 28.9% requirement is not refuted; what is established is that neither
agent with canine HSA exposure data can meet it — one for want of exposure, one for want of effect
at adequate exposure.

**Two contrary data, recorded rather than resolved.** Chow et al. 2015 (*JAMA Dermatol*
151(11):1226-9, PMID 26375166) measured a **34% fall in proliferative index** in a human angiosarcoma
after one week of propranolol 40 mg twice daily — an exposure no higher than the dogs received. That
disagrees with the in vitro anchor by two orders of magnitude; it is n=1, and Ki-67 is not net growth
rate, but it is not dismissible. And Saha et al. 2021 (*Front Oncol* 10:614288, PMID 33598432) found
that in **canine HSA cells** propranolol's action is **β-AR-independent** — the receptor-inactive
R-(+) enantiomer performs identically — operating by lysosomal drug sequestration. That is
**chemosensitisation**: a multiplier on a partner drug's kill term, not the growth modifier this
component asks for.

#### The stack

10-year durable response at `preexisting_prob = 0.70`, vaccine held at the real 0.03/day:

| | bar | clears 0.03? | 10-yr durable |
|---|---|---|---|
| vaccine only | 0.0515 | no | 0.492 |
| + measured cross-resistance correction | 0.0445 | no | 0.500 |
| + correction + 16.3% growth cut | 0.0363 | no | 0.688 |
| **+ correction + 28.9% cut (the requirement)** | **0.0298** | **yes** | **0.936** |
| + correction + 35% cut | 0.0270 | yes | 1.000 |
| 28.9% cut, no correction | 0.0347 | no | 0.544 |

**No component works alone, and the correction is nearly worthless by itself** (0.492 → 0.500). What
the pair has is a strong interaction: cut alone 0.544, correction alone 0.500, both together 0.936.
The correction still lowers the therapeutic ask — growth must fall by **28.9%** with it versus
**41.4%** without, a 1.43× reduction.

The stack is also insensitive to `preexisting_prob` (0.936 at 0.70, 0.50 and 0.30), and the vaccine
remains load-bearing inside it — remove it and durability falls to 0.284.

#### Two things that 1.000 does not include

**It assumed immunity never wanes.** The table above uses the engine's `half_life_days=None`
default — the same assumption that was caught carrying the original headline number in §3. Re-run
under real waning:

| immunity half-life | no boosters | q180d | q60d (eVim's real schedule) |
|---|---|---|---|
| never wanes | 1.000 | 1.000 | 1.000 |
| 365 d | 0.276 | 1.000 | 1.000 |
| 180 d | 0.284 | 1.000 | 1.000 |
| 90 d | 0.292 | 0.544 | 1.000 |

The stack survives waning — but **only on a booster schedule**. Unboosted it falls to roughly the
no-vaccine level at every half-life. q60d holds 1.000 even at a pessimistic 90-day half-life; q180d
is adequate only if immunity genuinely lasts 180 days or more. Boosting is also maintenance rather
than a tapering course — stopping q60d at 1, 2 and 5 years gives **0.244 / 0.388 / 0.668**. A
ten-year claim requires ten years of dosing.

**It is freedom from regrowth, not survival.** The engine does not model rupture; a dog that bleeds
to death with a perfectly controlled tumour counts as a durable response by its definition. Carrying
rupture as an independent competing hazard (`hsa_open_route_closure.joint_durability`) over ten
years:

| annual rupture hazard | unscreened | CANDiD 78.4% | CANDiD 90.9% |
|---|---|---|---|
| 2% | 0.817 | 0.958 | 0.982 |
| 5% | 0.599 | 0.897 | 0.955 |
| 10% | 0.349 | 0.804 | 0.913 |

So the defensible ten-year figure is **~0.6–0.8 unscreened and ~0.9+ under surveillance**, not
1.000. Screening is a third load-bearing component of the plan, not an optional extra — and the
hazard values above are swept, not measured.

#### What is still unmeasured, and the experiment that would settle it

Nobody has measured how much propranolol reduces canine HSA growth rate. 16.3% is what the stack
*requires*, not what any study reports. The evidence around it is genuinely mixed, and the largest
piece is negative:

- **PRO-DOX** (Borgatti et al. 2025, PMID 40386412) — phase I, **20 dogs**, stage 1–2 splenic HSA:
  propranolol + **doxorubicin** "did not appear to influence treatment outcomes." The biggest canine
  test, in the exact disease.
- But Pasquier's own in vitro work found propranolol synergizes strongly with **vinblastine** and
  shows "only additivity or slight antagonism" with **doxorubicin**. PRO-DOX used the partner the
  human data predicted would not work.
- Terauchi et al. 2023 (PMID 37545711): anthracycline + propranolol, 5 dogs stage 3 HSA — clinical
  benefit in 4/5, no serious adverse events. n=5, retrospective.
- Moirano et al. 2023 (PMID 37800663): **vinblastine** + propranolol with radiotherapy, 7 dogs with
  right atrial tumours — effusions resolved in all seven, median PFS 290 d, median OS 326 d.

That the negative trial used doxorubicin and the positive ones used vinblastine is a hypothesis, not
a demonstrated explanation. It is, however, a specific and pre-existing one: **propranolol +
vinblastine metronomic in canine splenic HSA, with a progression-free readout**, is the experiment
this analysis points at.

*Tests: `test_hsa_gap_stack.py`*

#### Is propranolol the only option? No — but the class has a poor record

The stack asks for a ~16% growth reduction. It does not ask for propranolol specifically. Five
growth-directed agents have canine splenic-HSA readouts, and every one of them was given **without a
vaccine**:

| agent | n | median OS | verdict |
|---|---|---|---|
| toceranib (VEGFR/PDGFR/KIT) — Gardner 2015, PMID 26062540 | 43 | 172 d | **negative** — "does not improve either disease free interval or overall survival" |
| propranolol + doxorubicin — Borgatti 2025, PMID 40386412 | 20 | — | **negative** — "did not appear to influence treatment outcomes" |
| thalidomide — Bray 2018, PMID 29210452 | 15 | 172 d | uncontrolled; identical median to the negative toceranib arm |
| metronomic cyclophosphamide/etoposide/piroxicam — Lana 2007, PMID 17708397 | 9 | 178 d | suggestive, unrandomised (vs 133 d on doxorubicin) |
| propranolol + vinblastine + RT — Moirano 2023, PMID 37800663 | 7 | 326 d | positive, small, **cardiac** site |

So there is no shortage of candidates. The problem is that the class has largely failed in this
disease — and where a partner drug is involved the split runs along the partner, not the agent: both
clear negatives used **doxorubicin**, while the one clearly positive propranolol readout here and
the human angiosarcoma result (Pasquier 2016, PMID 27211551) both used **vinblastine**. Lana's
metronomic cocktail is the exception that fits neither side: no vinblastine, but also no randomised
comparison.

#### The back-test: the model predicts those failures

The engine now takes a `growth_modifier` array, so an antiproliferative agent can be **scheduled** —
ramped in from a start day, applied to chosen clones, optionally stopped — instead of being faked by
permanently rewriting `model.growth`. A multiplier can never push net growth below zero, which is
exactly right for this class: arrest is not death (the *cytostatic ceiling*).

Running the configuration those five trials actually used — growth reduction, **no vaccine**:

| growth suppression | 10-yr durable |
|---|---|
| 0% | 0.284 |
| 16.3% | 0.336 |
| 30% | 0.324 |
| 50% | 0.524 |

Slowing a clone that still has a positive margin delays relapse; it does not prevent it. The spread
across the plausible range is inside Monte Carlo noise (±3 points at 250 trials), and only an
implausible 50% cut moves the needle. **That is the real record**: three negative-or-flat trials at
~172–178 days.

Re-running the stack through the scheduled agent reproduces the permanent-growth-rewrite figures to
within Monte Carlo noise — 0.500 / 0.540 / 0.928 here against 0.500 / 0.544 / 0.936 there — which is
the cross-check that scheduling a `growth_modifier` and rewriting `model.growth` mean the same thing.

It adds one practically useful result: at the required 28.9%, starting the agent on day 0, 60 or 180
gives **0.932 / 0.928 / 0.896**. It does not have to be given up front — it can follow the
chemotherapy backbone, and a six-month delay costs about four points.

And it confirms the exposure finding from the other direction: fed the suppression propranolol
actually reaches in a dog (0.05–0.6%), the scheduled agent returns **0.500 on every anchor** — bit
for bit the correction-only figure.

The back-test is a check on the *model*, not evidence for the stack. None of those trials included a
vaccine or the corrected cross-resistance backbone; the stack's prediction is about a combination
that has never been given to a dog, so the negative record neither confirms nor refutes it. What the
back-test does establish is that the model does not naively reward antiproliferative agents — it
predicted their failure before being asked to predict their success.

*Tests: `test_hsa_antiproliferative.py`*


---

## 3c. The combination that clears the exposure criterion

§3b's growth-reduction route asks for something no agent is shown to deliver. This section records
a different route that passes both halves of the test — and is the first candidate in this analysis
to do so.

### Why the drug class was wrong, mechanistically

Murai et al. 2012 (*BMC Vet Res* 8:128, PMID 22839755; *J Comp Pathol* 147(4):430-40, PMID 22789858)
found canine HSA runs on **mTORC2/Akt/4E-BP1, regulated independently of mTORC1**. In 37 canine
haemangiosarcomas ~80% expressed p-Akt Ser473 and p-4E-BP1, but **only 35% expressed p-mTORC1**.

Rapamycin inhibits mTORC1. It does not touch the pathway this disease actually runs on. That
predicts a rapalog underperforms here — and Andersen et al. 2015 state flatly that *"angiosarcomas
are insensitive to mTOR inhibition."* This is the mechanistic reason the FidoCure rapamycin signal
is real but small, and the reason an ATP-competitive dual TORC1/2 inhibitor is the right class
rather than a modelling convenience.

### The measured synergy, in canine angiosarcoma

Andersen et al. 2015 (*Int J Oncol* 47(1):71-80, PMID 25955301), in the canine AS isolate VCT261e:

| | IC50 |
|---|---|
| MEK inhibitor alone | 150 ± 30 nM |
| rapamycin alone | >50 nM (insensitive) |
| **combined, 4:1** | **11 ± 6 nM** — 13.6× shift, **CI = 0.07** |

In canine AS tumorgrafts: vehicle reached 1000 mm³ by day 21; the combination showed virtually no
growth by week 3, with no weight loss over 38 days. Adachi et al. 2016 (PMID 27408334) independently
found MAPK inhibitors alone do **not** affect canine HSA viability — the same result from the other
side. Neither node is a monotherapy target; each becomes one once the parallel pathway is blocked.

### It clears the exposure criterion

Takada et al. 2024 (*Vet Comp Oncol* 22(3):410-421, PMID 38889903) ran phase I trametinib in 18
dogs: MTD 0.5 mg/m²/day, with ~70% reaching 10 ng/mL = **16.2 nM**.

| | requirement | achieved | verdict |
|---|---|---|---|
| as monotherapy | 150 nM | 16.2 nM | **9.2× short** |
| **in combination** | **11 nM** | **16.2 nM** | **1.48× margin — passes** |

That asymmetry *is* the finding, and it independently explains Adachi's null result. And Wei et al.
2022 (*Front Vet Sci* 9:1056408, PMID 36590793) already gave sapanisertib with trametinib to 12
dogs — tolerated, without dose-limiting toxicity. This is not a proposed combination.

### What it buys

Modelled through the engine's existing per-clone second-drug support, with no existing ceiling
adjusted. The bar clears 0.03/day if MEK contributes **0.0225/day** at achievable exposure
(0.0145/day at saturation) — inside the range the model already grants the primary drug against
resistant clones.

| MEK kill/day | 10-yr freedom from regrowth |
|---|---|
| 0 | 0.500 |
| 0.0100 | 0.536 |
| **0.0225** *(the requirement)* | **0.888** |
| 0.0300 | 0.980 |

Every component is load-bearing: drop the vaccine and it falls to **0.312**; drop the
cross-resistance correction and it falls to **0.560**.

**And unlike the growth-reduction route, it is insensitive to waning** — 0.888 at a 180-day *and* a
90-day immunity half-life under q60d boosters. The second drug carries load the vaccine cannot.

Freedom from regrowth is still not survival. At a 5%/yr rupture hazard over ten years, 0.888 becomes
**0.532 unscreened** and **0.797–0.848 under CANDiD-sensitivity surveillance**.

### Mechanism by mechanism

| mechanism | answer |
|---|---|
| PI3K/AKT feedback reactivation *(sets the bar)* | dual TORC1/2 blocks the arm the feedback uses — the class's design purpose |
| MAPK crosstalk bypass | MEK inhibition acts directly on the node |
| target-site (FRB/FKBP12) mutation | invisible to ATP-competitive inhibitors (measured) |
| **kinase-domain mutation** | **not covered.** 3–30× against ATP-competitive drugs. Bivalent third-generation inhibitors (RapaLink-1) exist for it, with no canine data at all. |

### What is not established

Andersen measured PD0325901; Takada dosed trametinib. Both inhibit MEK1/2 and trametinib is
generally more potent, so carrying the requirement across is directionally conservative but not
rigorous. Per-clone kill rates for either drug against these specific mechanisms have never been
measured. And Takada **looked for target engagement in canine tumours on days 0 and 7 and did not
find it** — weaker evidence than toceranib, where a rising plasma VEGF confirmed engagement.

This is the strongest candidate the analysis has produced and the first to clear the exposure
criterion. It is a well-supported hypothesis, not a demonstrated closure.

*Tests: `test_hsa_parallel_pathway.py`*


---

## 3d. The items left open, and what closes each

Four things were flagged as unresolved when the two-node combination was proposed. Three close on
evidence or arithmetic already in hand; the fourth narrows.

### The kinase-domain mutation is covered — that gap was a counting error

`VERDICT` listed `kinase_domain_mutation` as not covered while listing
`pi3k_akt_feedback_reactivation` as covered. **In the model those are the same clone** — index 1,
carrying the 9.5× fold-shift measured for M2327I. A lesion in mTOR's own kinase domain confers no
protection against MEK inhibition, because that is a different node on a different pathway; Wei et
al. 2020 (PMID 32943547) report the pair suppressing *reciprocal* crosstalk in vivo. Verified against
the engine: clone 1 sets the bar at 0.0445 without the second drug and falls to 0.0300 with it.

### "The therapy that made things worse" tested something else

SRCBST-2 (Borgatti et al. 2020, PMID 32187827) did produce more toxicity and less benefit. But it
changed **three things at once**: three cycles instead of one, a *reduced* interval before
doxorubicin, and eligibility widened to stage 3 from a minimal-residual-disease setting. The authors'
own conclusion attributes the harm to schedule — *"starting 1 week prior to doxorubicin … compared
with a single cycle given between surgery and a delayed start of chemotherapy."*

The requirement is a persistent kill term that antigen loss does not affect. That trial varied
schedule, chemotherapy interval and disease stage simultaneously and never tested persistence. The
negative result stands as a fact about that regimen; it is not evidence against the requirement.

### A supplier for route 4 that turns the escape into the target

Antigen loss is the escape where the tumour stops displaying what the vaccine trained against. NK
cells are the one effector class for which that is an *attractant*: MHC class I restrains them, so a
cell that hides from T cells removes the signal holding NK cells back — "missing self" (Malmberg et
al. 2017, PMID 28699110).

**Does the mechanism exist in dogs?** Canine Ly49 had been reported mutated and nonfunctional, which
would rule this out entirely. Gingrich et al. 2023 (*ImmunoHorizons* 7(11):760-770, PMID 37971282)
find Ly49/KLRA1 expressed in resting and activated canine NK cells, almost exclusively in the NK
cluster, with modelled structure closely similar to the murine system and favourable docking to
MHC-I. That resolves the doubt **in favour of the mechanism existing** — but it is predicted binding
and expression, not a functional demonstration that canine NK cells preferentially kill MHC-I-low
targets.

Canine NK cells are manufacturable and have been given to dogs: 19-fold expansion to 259 × 10⁶ cells
by day 14, and a first-in-dog trial of 10 dogs with osteosarcoma where **5 of 10 were metastasis-free
at six months** and one lived 17.9 months (Canter et al. 2017, PMID 29254507; Judge et al. 2020,
PMID 32084139). And the eBAT redosing failure does not transfer: eBAT is a foreign bacterial toxin
construct whose repeat-dose problems were hypotension and immunogenicity, and autologous NK cells are
the dog's own cells.

*Not yet given for hemangiosarcoma, and delivery in every canine trial so far was intra-tumoral —
splenectomised minimal residual disease has no target to inject.*

### Target engagement was assayed a week before steady state

Takada et al. 2024 looked for trametinib target engagement on **days 0 and 7**. The same paper
reports steady state at **approximately 14 days**, and trametinib accumulates 3–4× on daily dosing.
The assay ran before the exposure existed. That removes the finding as evidence *against* engagement;
it does not supply evidence *for* it.

### The exposure claim no longer depends on the drug substitution

Two anchors, reached independently: Andersen's canine combination IC50 of **11 nM** (measured with
PD0325901), and the **10 ng/mL** trametinib concentration Takada identify as clinically effective,
which ~70% of dogs reach at the tolerated dose. **10 ng/mL is 16.2 nM** — the same number from canine
tumour pharmacology and from the drug's own clinical threshold.

### The rupture hazard is now grounded

Ruffoni et al. 2025 (*JAVMA* 263(8):985-990, PMID 40334697) prospectively enrolled **345 dogs** with
haemoperitoneum from a ruptured splenic tumour: 56.2% hemangiosarcoma, 35.7% benign, 8.1% other
malignant. Rupture is not a rare complication to sweep over — it is how the majority of these tumours
present. The *post-remission* annual hazard remains unmeasured, but the screening conclusion is
insensitive to it: surveillance removes the detected fraction of whatever the hazard is.

### What genuinely remains

Two gaps, both missing measurements rather than contradictions: **nobody has shown trametinib
engaging its target inside a canine tumour**, and **nobody has given NK cells systemically for
hemangiosarcoma**. Neither is refuted; both are simply untested.

*Tests: `test_hsa_open_item_closures.py`*


---

## 3e. Both gaps close — and the search found a constraint that matters more

§3d left two items as missing measurements. Both have been done. Finding them also surfaced a phase 2
result that changes *when* the immune components should be given.

### Trametinib engages its target in canine tumour tissue

Takada et al. 2018 (*Mol Cancer Ther* 17(11):2439-2450, PMID 30135215) — the **same first author** as
the 2024 canine phase I whose day-7 biopsy found nothing — tested trametinib against canine
histiocytic sarcoma cells in an intrasplenic orthotopic xenograft:

- *"Target engagement was validated as activity of ERK, downstream of MEK, was significantly
  downregulated in neoplasms of treated mice."*
- *"trametinib was found in plasma **and neoplastic tissues** within projected therapeutic levels"* —
  exposure confirmed at the tumour, not merely in blood
- apoptosis by caspase 3/7; significantly longer survival
- the canine lines carry **PTPN11 E76K** and **KRAS Q61H**, both reported in human histiocytic
  sarcoma — the MAPK node is genuinely driving

This replaces "never demonstrated" with "demonstrated in the wrong tumour type."

### NK cells have been given intravenously to dogs

Razmara et al. 2024 (*J Immunother Cancer* 12(4):e007963, PMID 38631708) expanded NK cells from
**unmanipulated PBMCs** rather than CD5-depleted cells, lifting the yield ceiling, and ran two
first-in-dog trials:

| | route | n | schedule | outcome |
|---|---|---|---|---|
| autologous | **IV**, 7.5×10⁶ cells/kg | 9 (4 melanoma, 5 OSA) | days 0 and 7, inhaled IL-15 50 µg BID × 14 d | no treatment-related SAEs; 1 PR, 1 SD |
| **allogeneic** | **IV**, 7.5×10⁶ cells/kg | 5 (oral melanoma) | single infusion, rhIL-15 3 µg/kg SC | no serious AEs; median survival 145 d, one dog 445 d |

No lymphodepletion in either. **The allogeneic arm matters most**: an off-the-shelf product removes
per-dog manufacture from the critical path.

### The constraint this uncovered

Rebhun et al. 2025 (*Front Immunol* 16:1672790, PMID 41209004, NCI-COTC030) ran a multicentre phase 2
of inhaled rhIL-15 given **after amputation and before chemotherapy** in canine osteosarcoma, powered
to cut metastatic failure from 40% to 20%.

**Disease-free and overall survival were statistically inferior to historical controls. The trial was
halted for futility.** And they measured why:

- PBMC cytotoxicity fell significantly after surgery **and** after chemotherapy — **−18.2 ± 16.1%**
  across therapy (P<0.001)
- IL-6 rose at both points and tracked the falls
- **dogs whose cytotoxicity rose lived significantly longer** (P=0.004, r=0.62)

*"These data have important implications on novel immunotherapy strategies involving multimodality
approaches including surgery and chemotherapy."*

### Two independent failures with the same shape

| | agent | setting | result |
|---|---|---|---|
| Borgatti 2020 (PMID 32187827) | eBAT | redosed at a *reduced* interval from doxorubicin | more toxicity, less benefit |
| Rebhun 2025 (PMID 41209004) | inhaled IL-15 | between amputation and chemotherapy | inferior survival, halted |

Different agents, different groups, different diseases — both placed an immune therapy **inside the
peri-surgical and peri-chemotherapy window**. Neither failed because the mechanism was wrong. Both
failed where host effector function is measurably at its lowest.

**Splenectomy followed by doxorubicin is exactly that window**, and exactly where an HSA regimen would
be tempted to add its immune components.

### The design consequence, and why it is affordable

Schedule the vaccine, boosters and any NK component to **avoid** the peri-operative and
active-chemotherapy window, and gate dosing on recovered PBMC cytotoxicity — a biomarker that
predicts outcome rather than merely describing it.

The engine already says this is nearly free: starting the second drug on day 0, 60 or 180 gives
**0.932 / 0.928 / 0.896**. Delay costs a few points. Being early, on this evidence, costs more.

### What is genuinely left

Every component has now been given to a dog, and the delivery questions are settled. **No trial has
given any of it for hemangiosarcoma** — the demonstrations sit in histiocytic sarcoma, melanoma and
osteosarcoma. Species and route are answered; the disease is not.

*Tests: `test_hsa_immune_timing.py`*


---

## 3f. How thin is the margin, really?

The exposure margin was reported as "1.48×, clears." That used point estimates. Carried through the
reported **11 ± 6 nM**:

| | margin |
|---|---|
| at IC50 − 1 SD (5 nM) | 3.25× |
| at the point estimate (11 nM) | 1.48× |
| **at IC50 + 1 SD (17 nM)** | **0.96×** |

Only ~70% of dogs reach even the point-estimate exposure. "Clears with 1.5× to spare" overstated
what the data support.

### But reading 0.96× as "fails" is also wrong

Effect is an Emax curve, not a switch. Sitting *at* the IC50 gives half-maximal effect, not none.
Run through the engine rather than argued from the ratio:

| combination IC50 | 10-yr durable |
|---|---|
| 5 nM (−1 SD) | 0.996 |
| 11 nM (point) | 0.888 |
| **17 nM (+1 SD)** | **0.748** |
| 34 nM (2× worst) | 0.528 |

Across the full reported uncertainty durability spans **0.748–0.996**, and even at twice the
worst-case IC50 it is 0.528 — still above the 0.500 the correction alone gives. **The plan degrades
gracefully rather than failing at a threshold.**

### The steep axis is the kill rate, not the IC50

| MEK kill/day | 10-yr durable |
|---|---|
| 0 | 0.500 |
| 0.011 | 0.576 |
| **0.0225** *(required)* | **0.888** |
| 0.034 | 0.996 |

Halving the kill rate loses most of the benefit. Durability is more sensitive to *how well the second
drug works* than to *how precisely we know its IC50* — which is why the in vivo derivation below
matters more than the concentration ratio.

### The weakest joint, replaced with a measurement

The 0.0225/day requirement was defended by analogy to ranges the model already grants other clones.
It doesn't have to be. Andersen's canine angiosarcoma tumorgrafts started at **50–100 mm³**, vehicle
reached **1000 mm³ by day 21**, and the combination held it flat. That implies **0.110–0.143/day of
net growth removed** — a **4.9–6.3× margin** over what the model needs, from a growth curve in the
right species and tumour.

*Limits kept visible:* that is the combination's *total* effect, so attributing all of it to the
second drug double-counts what the model already gives the first; and a subcutaneous mouse tumorgraft
grows far faster than residual disease in a dog. What transfers is that the requirement sits well
inside the measured envelope rather than at its edge.

### Protein binding hits one anchor, not the other

The objection is real: 16.25 nM is *total* plasma trametinib, and the drug is extensively bound.

- **The in vitro anchor is vulnerable.** Andersen's IC50 was measured in DMEM with 10% FBS — roughly
  a tenth of plasma protein — so the equivalent total *plasma* concentration is **higher**, not
  lower. The correction runs against the plan and nobody has quantified it.
- **The clinical anchor is not.** 10 ng/mL is the concentration Takada et al. associate with
  *clinical efficacy in humans* — derived from outcomes in real plasma. Protein binding is already
  inside that number; correcting it would double-count.

Resting the case on the clinical anchor removes the objection entirely, at the cost of the
canine-tumour specificity the in vitro number provided. That is the right trade.

### The second drug cannot be stopped

The obvious answer to chronic toxicity — dose for a few years, then stop once the resistant clones
should be gone — does not work:

| stop the second drug at | 10-yr durable |
|---|---|
| 1 year | 0.464 |
| 2 years | 0.460 |
| 3 years | 0.488 |
| 5 years | 0.576 |
| **never** | **0.888** |

Stopping at one, two or three years lands **below the 0.500 the correction alone delivers**. The
clones are suppressed, not eliminated, and they resume. This closes the escape hatch and makes
cumulative toxicity over a decade the sharpest remaining objection.

### Which makes the published schedule load-bearing

Wei et al. 2020 (PMID 32943547) found *"a staggered sapanisertib dose, coupled with daily
trametinib, was optimal … **while minimizing hematologic and renal side effects**."* Those are
exactly trametinib's canine dose-limiting toxicities — hypertension, proteinuria, elevated ALP. The
regimen should specify staggered sapanisertib with daily trametinib rather than both daily.

*One correction to the record:* the claim that the combination reduces sapanisertib exposure is the
**canine** finding (Wei 2022). In **mice**, the same group found sapanisertib PK unchanged and
**trametinib AUC increased**. The trametinib direction cushions the thin side of the margin, since
16.25 nM came from monotherapy dosing.

### Where this leaves the defence

| | |
|---|---|
| **stronger** | kill requirement from a measured growth curve; protein-binding objection answered by demoting the vulnerable anchor; IC50 uncertainty costs 0.888 → 0.748, not collapse |
| **still weak** | second drug cannot be stopped, so a decade of cumulative toxicity; in dogs the pairing weakens the sapanisertib arm the mechanism depends on; tolerability is 17 days in *healthy* beagles; no data for the full stack |

*Tests: `test_hsa_margin_analysis.py`*

---

## 3g. Given the toxicity, is a different approach needed?

Yes — but not a different drug. A different place to put the persistent work.

### First: can the same drug simply be given less?

Three ways of cutting cumulative exposure, all run through the same engine, same seed, same 250
trials. Continuous full dose is **0.888**.

| approach | cumulative dose | 10-yr durable |
|---|---|---|
| duty cycling, 3 periods × 75% on | 75% | 0.740–0.760 |
| duty cycling, 3 periods × 50% on | 50% | 0.576 |
| continuous at 75% of dose | 75% | **0.784** |
| continuous at 50% of dose | 50% | **0.668** |
| full dose 2 yr, then half | 60% | 0.696 |
| full dose 2 yr, then stop | 20% | 0.460 |

**Nothing rescues it.** Durability tracks cumulative exposure, and every schedule that gives less
gives less protection.

One result is worth keeping. At matched cumulative dose, **giving less drug continuously beats
giving full doses intermittently** — 0.784 vs 0.740–0.760 at three-quarter dose, 0.668 vs 0.576 at
half. The period doesn't matter; only the fraction of time the drug is *absent* does. This is the
opposite of the usual clinical instinct, which is drug holidays. It is also not the adaptive-therapy
result: the engine has competition between clones built in, and the resistant ones still regrow
during the gaps faster than competition suppresses them.

### Second: what does the pair actually fail?

Not potency. It cleared the exposure criterion — that is why it replaced propranolol. It fails a
second criterion that was never written down, because nothing before it needed a time axis:

> **The duration criterion.** An agent meant to be given continuously over a horizon qualifies only
> if its tolerability has been demonstrated over a comparable horizon.

| | |
|---|---|
| documented tolerability | **17 days**, in healthy laboratory beagles |
| required | **3650 days**, in tumour-bearing dogs |
| shortfall | **215×** |

Propranolol was thrown out of this analysis for being ~200× short on *exposure*. This pair is ~200×
short on *duration*. Applying the first standard and not the second would be special pleading.

This does not say the pair is unsafe over ten years. It says it is **unknown** over ten years — and
the toxicities actually recorded were proteinuria, reduced reticulocytes and acute-phase
inflammation, which are renal and marrow signals. Those are exactly the organs where seventeen days
of "mild change" carries no information about a decade.

### Third: no available agent clears both criteria

The natural fix is to swap in a better-tolerated drug. Three candidates have genuine chronic-dosing
records in dogs, and each fails differently:

| candidate | duration | why it still fails |
|---|---|---|
| metronomic chemotherapy | passes | **negative in this disease** — 65 vs 255 days against anthracycline in dogs with hepatic metastases (Valenti 2026, n=66, P=0.02) |
| a rapalog alone | passes | targets mTORC1; canine HSA runs on mTORC2, and the measured cross-resistance is reciprocal, not additive |
| toceranib | passes | already screened — clears exposure, fails on biology |

Everything with a decade-scale safety record fails on effect in this tumour, and the one thing with
measured effect in canine angiosarcoma has seventeen days of safety data. **The two criteria are in
tension and nothing available clears both.**

### So the persistent work moves off the drug

The vaccine is already given on a schedule tolerable for a decade — boosters every sixty days. The
question the model can answer is how much taller it has to be before the drug becomes stoppable.

**Ten-year durability, by vaccine height and when the second drug is withdrawn:**

| vaccine kill/day | stop y1 | stop y2 | stop y3 | stop y5 | never stop |
|---|---|---|---|---|---|
| **0.030** *(measured)* | 0.464 | 0.460 | 0.488 | 0.576 | 0.888 |
| 0.0375 *(1.25×)* | 0.652 | 0.696 | 0.740 | 0.920 | 1.000 |
| **0.045** *(1.5×)* | **0.992** | **1.000** | 1.000 | 1.000 | 1.000 |
| 0.0515 *(= the bar)* | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

| drug exposure | | |
|---|---|---|
| stop at year 1 | 365 drug-days | 10% of the decade |
| never stop | 3650 drug-days | 100% |

**A vaccine half again as tall turns the second drug from a life sentence into a one-year
induction** — 90% less drug exposure, and durability *rises* from 0.888 to 0.992. Both axes improve;
it is not a trade at all.

Two details make this more than arithmetic:

- **The threshold sits below the bar.** 0.045 < 0.0515. The vaccine never has to hold the tumour
  alone. It only has to be tall enough that one year of drug plus a taller vaccine finishes what a
  decade of drug plus the measured vaccine could not.
- **The curve is a cliff, not a slope.** Between 0.0375 and 0.045 the year-one stop moves from 0.652
  to 0.992 — and that cliff sits inside the range a 1.25–1.5× improvement covers. A modest gain in
  vaccine potency is worth far more than any further work on the drug schedule.

*Why the 1.000s aren't a trick:* the vaccine doesn't touch the antigen-loss clone at all. But escape
seeding is proportional to the **antigen-positive** burden, since that is the population the escape
variant arises from. A taller vaccine crushes that population faster, so there is less of it to throw
off a variant. The suppression is indirect and real. (1.000 over 250 trials bounds escape below
roughly 1%; it does not mean impossible.)

### Is a 1.5× taller vaccine a real target?

The vaccine's ceiling was treated as a fixed property of the product. In this disease a substantial
part of it is a property of the **microenvironment** — which is a different problem, with an existing
intervention.

- **The suppression is measured, in this tumour.** Canine HSA is full of CD204⁺ M2 macrophages
  expressing PD-L1, and *"canine HSA with macrophages expressing PD-L1 had a smaller number of
  T-cells in tumour tissues than tumours with PD-L1 negative macrophages."* Tumour-conditioned medium
  induces that polarisation in naive macrophages — the tumour creates the suppression. (Gulay 2022,
  PMID 35136176)
- **The intervention exists, in dogs.** Gilvetmab, a caninized anti-PD-1, in 51 client-owned dogs:
  6 mg/kg q28d or 10 mg/kg q14d, ORR 20% melanoma / 46% mast cell tumour, serious adverse events in
  5.9%. (Chon 2026, PMID 42247661)
- **The schedule doesn't reintroduce the problem.** A q14–28d antibody is in the same tolerability
  class as a q60d booster, not the same class as daily dual kinase inhibition.
- **A testbed now exists.** ISOS-1 is a syngeneic model matching canine HSA — every immune question
  here was previously stuck with xenografts, which have no host immune system to suppress.

### What it costs

| | |
|---|---|
| **removed** | ~3285 of 3650 drug-days, and with them a decade of renal and marrow toxicity that had no supporting data past day 17 |
| **added** | a checkpoint antibody with a 5.9% serious-adverse-event rate — one instance of which was **tumour haemorrhage** |
| **added uncertainty** | nobody has measured what checkpoint blockade adds to vaccine height. The 1.5× is a requirement derived from the model, not an effect size taken from data |

The haemorrhage signal deserves to be named rather than reasoned away. Splenic rupture is the
competing hazard that dominates early mortality here, and the tumour is made of endothelium. It is
mitigated — the checkpoint component is proposed post-splenectomy, and the published event was in
dogs with tumours in place — but it is **open**, with no hemangiosarcoma data.

**The honest comparison:** the previous plan needed an unmeasured decade of safety. This one needs an
unmeasured 1.5× of potency. The second is the better bet, because it can be measured in months, in a
model that exists, before any dog is committed to it — and because falling short degrades back to the
previous plan rather than to nothing.

### A third timing constraint

Corticosteroid pre-treatment significantly alters canine PBMC composition — *primarily the monocytic
compartment* — and blunts the interferon-γ response to both anti-PD-L1 and anti-PD-1 blockade
(Zimmermann 2025, PMID 40342421). Steroids are routine around splenectomy and haemoabdomen, and the
compartment they suppress is exactly where HSA's PD-L1 suppression lives.

That makes three independent findings pointing the same way: surgery and chemotherapy suppress
effector function (§3e), dosing immune agents inside that window went backwards twice (§3e), and now
steroids blunt the specific axis this swap depends on. **The immune components belong after the
surgical and chemotherapy backbone, gated on recovered effector function — not inside it.**

*Tests: `test_hsa_alternative_approach.py`*

---

## 4. Escape routes

| # | Route | Status |
|---|---|---|
| 1 | `pi3k_akt_feedback_reactivation` | CLOSED by construction |
| 2 | `mapk_crosstalk_bypass` | CLOSED by construction |
| 3 | `target_site_mutation` | CLOSED — and it sets the bar |
| 4 | antigen / MHC-I loss | Modelled unclosable; over-weighted for HSA; closable at 0.05/day |
| 5 | splenic rupture / haemorrhage | **OPEN** → partially closed (§5) |
| 6 | vaccine failure without antigen loss | **OPEN** → closable (§5) |
| 7 | disease outside the resected compartment | **OPEN** → already closed (§5) |

Routes 1–3 are closed **by construction, not by potency**: none of these resistance lesions requires
shedding the antigen a real HSA vaccine targets, so the vaccine still sees those cells. Route 3 sets
the bar. Just below it, at `vaccine_max_kill` 0.05, 23 of 24 ten-year relapses are ordinary drug
resistance — the bar is what binds, not antigen loss.

### Route 4 is over-weighted for HSA

The engine hard-codes escape-clone vaccine coverage to 0.0, inherited from the HS module's
hypothetical peptide/MHC-I mRNA vaccine. Three independent reasons it does not transfer:

1. **eVim raises antibodies against *extracellular* vimentin** — MHC-I is not involved.
   `hsa_scenarios` establishes this itself when it refuses to run NetMHCpan against eVim's antigen,
   calling that a category error — then simulates MHC-I loss anyway. eVim's real escape route is loss
   of surface vimentin, a structural cytoskeletal protein, which is a costlier event.
2. **ERstrePs raises both** humoral and vaccine-specific T-cell responses, so MHC-I loss degrades it
   rather than evading it.
3. **MHC-loss variants upregulate NKG2D ligands**, and primed CD8 T-cells kill them through NKG2D;
   killing was completely abrogated by anti-NKG2D blockade (Lerner et al., *Nat Cancer*
   2023;4(9):1258-1272, PMID 37537301). The event creating the blind spot creates the backup target,
   and prior antigen-specific priming licenses it — a property of the vaccine-primed population, not
   an added agent.

Simulation agrees it is minor: at potency 0.06 it never fires even at 10× the assumed seeding rate
(1.000 / 0.990 / 0.963 at 10× / 100× / 1000×). Above the bar the antigen-positive population
collapses before it can supply the mutation, so the route starves rather than being out-killed.

---

## 5. Closing the open routes

### The obvious closure for route 4, which real data refutes

The natural way to close route 4 is "eBAT, minus its 28-day cap" — give more of it, for longer.
**That experiment was run.** SRCBST-2 (Borgatti et al. 2020, *Vet Comp Oncol* 18(4):664-674, PMID 32187827) gave eBAT as
three cycles instead of one, at a reduced interval from doxorubicin, in 25 dogs: greater toxicity
(six acute hypotension, two hospitalised), **reduced** efficacy, and no significant survival benefit
against contemporary standard of care — versus the same team's single-cycle trial, which did show
one. More eBAT was worse than less eBAT.

The modelled *requirement* stands (≥0.05/day persistent agnostic kill closes route 4 even at 1000×
the assumed rate). What fails is the agent proposed to supply it.

### Route 5 — rupture and haemorrhage → PARTIALLY CLOSED

Modelled as an **independent competing hazard**, so it multiplies against tumour control:

| annual rupture hazard | 0% | 5% | 10% | 20% | 40% |
|---|---|---|---|---|---|
| 5-yr joint durability | 0.967 | 0.748 | **0.571** | 0.317 | 0.075 |

A 10%/year hazard costs 40 points. This route can erase the entire vaccine benefit without touching a
growth margin, which makes it the most dangerous of the three despite being the least modelled.

- **5a — Yunnan Baiyao ± aminocaproic acid: FAILED in a real trial.** Murphy et al. 2017, *J Vet Emerg
  Crit Care* 27(1):121-126, PMID 27669112: 16 dogs YB, 8 YB+EACA, 43 controls, all with right atrial
  masses and pericardial effusion. Median time to recurrence 12 d vs 14.5 d; median survival 18 d vs
  16 d. Neither significant. It *does* kill canine HSA lines in vitro via caspase-mediated apoptosis
  (Wirth et al. 2016, *Vet Comp Oncol* 14(3):281-94, PMID 24976212) — a clean case of in vitro
  activity not transferring. **Do not model this as a closure.**
- **5b — Local control of the bleeding site: real, positive, small.** Hypofractionated IMRT with
  vinblastine and propranolol in seven dogs with right atrial tumours: **effusions resolved in all
  seven**, one CR, four PR, median PFS 290 d, median OS 326 d; the three confirmed HSA survived 244,
  326 and 445 days (Moirano et al. 2023, *Vet Radiol Ultrasound* 64(6):1099-1102, PMID 37800663).
  Seven dogs is a case series — but it is a direct readout on the exact failure mode.
- **5c — Pre-empt the rupture: the strongest lever.** The hazard is a consequence of finding the
  tumour late, not a fixed property of it. The CANDiD study validated a canine multi-cancer liquid
  biopsy in 1,100 dogs at 54.7% overall sensitivity and 98.5% specificity, rising to **78.4–90.9% for
  the three most aggressive canine cancers** (a group including HSA), and detected cancer signal in
  four presumably cancer-free dogs before clinical signs (Flory et al. 2022, *PLOS ONE*
  17(4):e0266623, PMID 35471999). Screening a high-risk breed converts an emergency rupture into an
  elective splenectomy — a change in the hazard, not a treatment for its consequences. Limits: a test
  is not a screening schedule, and 98.5% specificity in a low-prevalence population still produces
  false positives whose cost is not modelled.

### Route 6 — vaccine failure without antigen loss → CLOSABLE

Modelled as a **take rate**: the fraction of dogs mounting any response, with non-takers receiving
exactly the no-vaccine outcome.

| take rate | 1.0 | 0.8 | 0.6 | 0.4 |
|---|---|---|---|---|
| population durable | 0.967 | 0.833 | 0.699 | 0.565 |

Linear, at ~6.7 points of durability per 10 points of take. After potency itself this is the largest
lever, and unlike potency it is directly measurable in a running trial.

- **6a — Anti-PD-L1, with an HSA-specific mechanistic case.** Canine HSA induces M2 polarisation and
  PD-L1 expression in tumour-associated macrophages, and — the load-bearing observation — canine HSA
  tumours whose macrophages express PD-L1 contained **fewer T-cells** than those with PD-L1-negative
  macrophages (Gulay et al. 2022, *Sci Rep* 12(1):2124, PMID 35136176). That is route 6 with a named
  mechanism, measured in the actual disease: a response can be primed and then excluded. The matching
  therapy exists in dogs — canine chimeric anti-PD-L1 c4G12 in 29 dogs with pulmonary metastatic oral
  malignant melanoma gave median survival 143 d vs 54 d for historical controls, with one CR among 13
  with measurable disease and any-grade treatment-related AEs in 51.7% (Maekawa et al. 2021, *NPJ
  Precis Oncol* 5(1):10, PMID 33580183). Limits: never given for HSA; historical-control comparison.
  What makes it testable rather than speculative is that the selecting biomarker — PD-L1 IHC on the
  resected spleen — is the same assay that produced the mechanism.
- **6b — Measure the take.** Neither real HSA vaccine trial powered an analysis of whether immune
  responders survived longer than non-responders. Until one does, a dog in whom the vaccine did
  nothing and a dog in whom it worked and was escaped are indistinguishable in a survival curve. A
  trial-design closure, not a drug, and the cheapest item here.

### Route 7 — disease outside the resected compartment → ALREADY CLOSED

Real and quantified in this disease: among 99 dogs with non-traumatic haemoperitoneum from splenic
tumour rupture, **22% of liver lesions found at surgery had been missed on preoperative ultrasound**
(Ramirez et al. 2024, *JAVMA* 262(11):1499-1503, PMID 39111340).

`run_monte_carlo_two_compartment` has existed since the HS work and HSA has never called it. Running
HSA's own 5-clone scenario through it, at threshold potency, 5-year horizon:

| P(occult second site) | 0.0 | 0.3 | 0.6 |
|---|---|---|---|
| durable, vaccine on | 1.000 | 1.000 | 1.000 |
| relapses in that site | 0 | 0 | 0 |
| durable, vaccine off | 0.340 | — | 0.325 |
| relapses in that site | 0 | — | **46 of 135** |

Surgery cannot reach the second compartment; a systemic persistent mechanism reaches it exactly as
well as the first. **No new agent needed** — this is the sharpest argument for the vaccine in the
analysis, the one place adding it does something surgery structurally cannot.

Backstop for dogs where the vaccine does not take: metronomic oral chemotherapy
(cyclophosphamide/etoposide/piroxicam) in nine dogs with stage II splenic HSA gave median overall
survival *and* median disease-free interval both 178 d, against 133 d and 126 d for 24 dogs on
conventional doxorubicin (Lana et al. 2007, *J Vet Intern Med* 21(4):764-9, PMID 17708397). Nine
dogs, non-randomised — what recommends it is its shape: continuously dosed, oral, systemic.

---

## 6. A hypothesis that failed

Every trial this module calibrates against is post-splenectomy adjuvant therapy on minimal residual
disease. The HSA scenarios never model that resection: they use `initial_burden=0.3` with no
`debulking_fraction`, unlike the HS module's `DEBULKING_FRACTION = 0.97`.

The obvious hypothesis — that `_PREEXISTING_PROB_CENTRAL`'s 0.30 → 0.70 recentering was compensating
for the missing resection — was tested and is **false**. Modelling splenectomy makes durable response
*higher*, moving further from the eBAT benchmark the recentering was argued on:

| `preexisting_prob` | 1-yr, no resection | 1-yr, post-splenectomy | 2-yr, no resection | 2-yr, post-splenectomy |
|---|---|---|---|---|
| 0.30 | 0.665 | 0.750 | 0.635 | 0.672 |
| 0.70 | 0.385 | 0.500 | 0.305 | 0.320 |

So the recentering is if anything under-corrected, and the module's own preferred explanation — an
unmodelled rupture/haemorrhage pathway — survives the test. Independently useful: resection moves the
1-year figure by 8–11 points and the 2-year figure by 1.5–4, because `initial_burden` changes where a
clone starts and not the sign of its growth margin. **Surgery is a delay mechanism**, matching the
real 48-day surgery-alone median (Wendelburg et al. 2015, *JAVMA* 247(4):393-403, PMID 26225611).

---

## 7. The answer

A lasting remission runs through the **vaccine**, not the targeted drug. The drug makes tumours
shrink and does essentially nothing to stop them returning; at its real achievable dose it may do
nothing at all. Three of the four modelled resistance routes are covered by any vaccine
automatically, because resistance to a drug does not change what the immune system was trained to
see. The fourth is treated as unclosable and probably is not, for three independent reasons specific
to this disease. Of the three routes left open, one is already closed by the regimen already
proposed, one is closable with a dog-specific antibody that exists, and the third — bleeding — has no
drug that works, so the honest answer is to find the tumour earlier rather than treat the rupture
better.

Real vaccines in real dogs deliver roughly **60% of the killing power** that permanent control
requires. Boosters do not close that gap — they are required for a different reason, to hold
whatever height you have for the animal's life, and without them even a threshold-clearing vaccine
falls back to roughly the no-vaccine outcome by ten years.

**No single fix closes the gap** (§3b): lowering the bar with a second kill term is unanchored,
two vaccines fail under antigenic competition, and booster tolerance was never a route to closing it.
Growth suppression by β-blockade was tried and abandoned — achievable propranolol exposure is ~200×
short of what the required suppression needs (§3b).

**A parallel-pathway combination does close it** (§3c). A MEK inhibitor added to the dual TORC1/2
agent is the first candidate to clear the exposure criterion: at the tolerated canine dose
trametinib reaches ~16 nM against an ~11 nM combination requirement, where MEK inhibition alone
would need ~150 nM. Combined with the cross-resistance correction and the vaccine, ten-year
durability reaches **0.888** — and all three components are load-bearing (0.312 for the drug alone,
0.560 without the correction).

**That answer degrades gracefully rather than collapsing** (§3f). Across the full reported IC50
uncertainty durability spans 0.748–0.996, and the kill requirement of 0.0225/day sits 4.9–6.3× inside
what a canine angiosarcoma tumorgraft growth curve actually measured.

**Its real weakness is time, not potency** (§3g). The second drug cannot be stopped — withdrawing it
at one, two or three years lands *below* what the correction alone delivers. That makes a decade of
continuous dual kinase inhibition mandatory, against 17 days of tolerability data in healthy beagles:
a 215× shortfall on duration, the same magnitude and the same shape as the exposure shortfall that
disqualified propranolol. No schedule rescues it, and no available agent clears both criteria.

**So the persistent work moves off the drug and onto the vaccine.** A vaccine 1.5× taller than what
real trials deliver (0.030 → 0.045/day) turns the second drug into a **one-year induction**: 90% less
drug exposure, and durability *rises* to 0.992. The threshold sits below the bar, so the vaccine
never has to hold the tumour alone — and in this disease a substantial part of the vaccine's ceiling
is microenvironmental, from PD-L1⁺ M2 macrophages that measurably exclude T cells, with a caninized
anti-PD-1 already dosed in 51 dogs on a booster-like schedule.

**What is not established** is that 1.5×. Nobody has measured what checkpoint blockade adds to
vaccine height in this tumour. That is the single number the plan now stands or falls on — and unlike
a decade of safety data, it can be measured in months in a syngeneic model that now exists.

### What would change the answer

1. **Measure what checkpoint blockade adds to vaccine height** — the number the plan now turns on
   (§3g). Vaccine ± anti-PD-1 in the ISOS-1 syngeneic model, read out as a growth-rate difference.
   Anything at or above 1.5× converts a decade of dual kinase inhibition into a one-year induction;
   anything below it falls back to the continuous-dosing plan rather than to nothing.
2. **Measure a vaccine's kill rate directly** instead of inferring it from survival. Serial imaging or
   ctDNA on a vaccinated cohort gives the progression-free readout the engine consumes natively, and
   removes the endpoint mismatch that makes the 1.7× shortfall a floor rather than a number.
3. **Measure the immunity half-life.** The booster interval follows from it, and §3 shows the answer
   flips between 0.268 and 1.000 depending on whether it is 90 days or 365.
4. **Re-run every HSA time-course at real rapamycin exposure.** The bar barely moves, so the
   conclusions should survive — but "should survive" is a prediction, and the HS pipeline's equivalent
   prediction was wrong.
5. **Model the right escape route for the right vaccine** — surface-vimentin loss for eVim, not MHC-I
   loss, and with a fitness cost of its own.
6. **Adopt the two-compartment model** the engine already provides.
7. **Add a rupture hazard** once any real rate exists. Until then these are figures for cancer
   regrowth, not for dogs dying of hemangiosarcoma.
