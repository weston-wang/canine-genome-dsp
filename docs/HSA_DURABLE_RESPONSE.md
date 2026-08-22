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

Sections 2 and 3 leave the vaccine ~1.7× too weak. Three routes were tried. **None of them closes
the gap**, and this section records why, because an earlier draft of this document claimed two of
them did.

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

#### Component 1 — an inconsistency in the model, not a therapy

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
Resolving it in the direction the potency anchor implies takes **the bar from 0.0515 to 0.0385**.

That is not enough on its own — durable response goes 0.492 → 0.640 — and the residual is an
*efficacy* ceiling, not a potency one: `max_kill` for `target_site_mutation` is 0.015/day, so no
further IC50 change moves it.

#### Component 2 — reduce growth, not kill

HSA is an endothelial tumour, and β-adrenergic blockade acts on proliferation rather than supplying
a kill term. ADRB1 and ADRB2 are expressed in transformed endothelial cells and in angiosarcoma
tumours (Pasquier et al. 2016, *EBioMedicine* 6:87-95, PMID 27211551).

#### The stack

10-year durable response at `preexisting_prob = 0.70`, vaccine held at the real 0.03/day:

| | bar | clears 0.03? | 10-yr durable |
|---|---|---|---|
| vaccine only | 0.0515 | no | 0.492 |
| + cross-resistance correction | 0.0385 | no | 0.640 |
| 20% growth cut, no correction | 0.0411 | no | 0.536 |
| **correction + 20% growth cut** | **0.0281** | **yes** | **1.000** |

**No component works alone; together they do.** And the correction is what makes the therapeutic ask
small: growth must fall by **16.3%** with it, versus **41.4%** without — a 2.5× reduction, bought by
fixing a modelling inconsistency rather than by adding a drug.

The stack is also insensitive to `preexisting_prob` (1.000 at 0.70, 0.50 and 0.30), and the vaccine
remains load-bearing inside it — remove it and durability falls to 0.284.

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

Re-running the stack through the scheduled agent reproduces the earlier table (0.492 / 0.640 / 0.532
/ 1.000), and adds one practically useful result: starting the agent on day 0, 60 or 180 all give
1.000. It does not have to be given up front — it can follow the chemotherapy backbone.

The back-test is a check on the *model*, not evidence for the stack. None of those trials included a
vaccine or the corrected cross-resistance backbone; the stack's prediction is about a combination
that has never been given to a dog, so the negative record neither confirms nor refutes it. What the
back-test does establish is that the model does not naively reward antiproliferative agents — it
predicted their failure before being asked to predict their success.

*Tests: `test_hsa_antiproliferative.py`*

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

### A closure this project proposed, which real data refutes

An earlier draft proposed closing route 4 with "eBAT, minus its 28-day cap." **That experiment was
run.** SRCBST-2 (Borgatti et al. 2020, *Vet Comp Oncol* 18(4):664-674, PMID 32187827) gave eBAT as
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

**A stack of three does.** Correcting a cross-resistance inconsistency in the model — the two
high-resistance clones are rapalog mechanisms while the potency anchor is an ATP-competitive dual
PI3K/mTOR inhibitor — takes the bar from 0.0515 to 0.0385 and costs nothing, because it is a
modelling fix rather than an added therapy. Adding a ~16–20% reduction in tumour growth rate via
β-adrenergic blockade takes it under 0.03, where the vaccine real trials already deliver reaches
**1.000 at ten years**, insensitive to `preexisting_prob`. No component works alone; the correction
is what makes the therapeutic ask small, cutting the required growth reduction from 41.4% to 16.3%.

**What is not established** is the growth reduction itself. β-blockade has the target, a 100%
response rate in human angiosarcoma with vinblastine, and a positive canine series with the same
partner — but the largest canine trial paired it with doxorubicin and was negative, and no study
reports a growth-rate reduction in canine HSA. The next experiment is propranolol + vinblastine
metronomic with a progression-free readout.

### What would change the answer

1. **Measure a vaccine's kill rate directly** instead of inferring it from survival. Serial imaging or
   ctDNA on a vaccinated cohort gives the progression-free readout the engine consumes natively, and
   removes the endpoint mismatch that makes the 1.7× shortfall a floor rather than a number.
2. **Measure the immunity half-life.** The booster interval follows from it, and §3 shows the answer
   flips between 0.268 and 1.000 depending on whether it is 90 days or 365.
3. **Re-run every HSA time-course at real rapamycin exposure.** The bar barely moves, so the
   conclusions should survive — but "should survive" is a prediction, and the HS pipeline's equivalent
   prediction was wrong.
4. **Model the right escape route for the right vaccine** — surface-vimentin loss for eVim, not MHC-I
   loss, and with a fitness cost of its own.
5. **Adopt the two-compartment model** the engine already provides.
6. **Add a rupture hazard** once any real rate exists. Until then these are figures for cancer
   regrowth, not for dogs dying of hemangiosarcoma.
