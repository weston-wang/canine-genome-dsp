# Durable response in canine multicentric lymphoma

What carries a lasting remission, how the disease escapes, what closes each escape route, and what
cure or 10-year control would actually require.

This document is the narrative record for the lymphoma pipeline. The modules under
`src/canine_dsp/` carry the code and the constants; the reasoning, provenance and caveats live here.
Every figure is recomputed from the engine by the tests named in each section
(`tests/test_lymphoma_engine_and_bar.py`, `tests/test_lymphoma_analysis.py`).

**Nothing here is a treatment recommendation.** Growth rates, kill ceilings and immunotherapy
potency are illustrative placeholders swept across ranges, not fitted measurements. What is real and
cited: the resistance biology (P-glycoprotein and BCRP drug efflux, measured in this disease), the
CHOP and rabacfosadine trial outcomes, the antigen-loss escape after CD20 CAR-T, and the transplant
cure fraction. No combination described here has been given to a dog on the strength of this model.
All PMIDs/DOIs were verified against PubMed while the modules were written.

This is the same analysis the histiocytic-sarcoma and hemangiosarcoma pipelines ran, applied to a
disease that differs in two structural ways: it is systemic from the start (there is nothing to
resect — the standard of care is chemotherapy, not surgery), and its dominant resistance mechanism
is **measured in the actual disease** rather than extrapolated from human oncology.

---

## 0. The disease and the target

Canine multicentric lymphoma is the most common blood cancer in dogs. The standard of care is the
CHOP protocol — cyclophosphamide, doxorubicin, vincristine, prednisone. It works spectacularly at
first and then almost always fails: in 134 dogs on a 15-week CHOP protocol the overall response rate
was **98%**, and the median progression-free survival was **176 days** with a median
disease-specific survival of **311 days** (Curran & Thamm 2015, *Vet Comp Oncol* 14 Suppl 1:147-55,
PMID 26279153). B-cell disease does better than T-cell; immunophenotype is the prognostic factor
that survives multivariate analysis (Mutz et al. 2013, *Vet Comp Oncol* 13(4):337-47, PMID
23786518). The stated target here is harder than anything the real regimens deliver: **cure, or at
least 10-year durability**, with every escape route closed.

---

## 1. The bar

A tumour is a mixed population, and treatment sorts it. Most cells are drug-sensitive and die; a few
carry a resistance change and regrow. For each resistant cell type, ask whether it is still growing
under treatment and how fast. That per-day growth rate is its head start, and any mechanism meant to
prevent relapse must out-kill it — not slow it, out-pace it.

`clone_growth_margins` against `dog_lymphoma_preset('B')`:

| Exposure assumption | sensitive | mdr1_pgp | abcg2_bcrp | tp53_evasion | **bar** |
|---|---|---|---|---|---|
| full CHOP (5× IC50) | −0.157 | +0.0903 | +0.0883 | +0.0771 | **0.0903** |
| de-rated to 40% for toxicity | −0.107 | +0.0916 | +0.0896 | +0.0795 | **0.0916** |
| **no drug at all** | +0.100 | +0.0920 | +0.0900 | +0.0880 | **0.0920** |

*Tests: `test_lymphoma_engine_and_bar.py::test_the_bar_is_set_by_pgp_efflux_and_barely_moved_by_chemo`*

**The bar is about 0.090/day, and it is set by the P-glycoprotein drug-efflux clone.** CHOP drives
the drug-sensitive clone deeply negative (−0.157/day) — which is why ~90%+ of dogs go into complete
remission — and moves the resistant bar by about **2%** (0.0920 untreated to 0.0903 under full
CHOP). The regimen decides how fast and how deeply the tumour shrinks, and almost nothing about
whether it comes back.

### The resistance is real, and it is why chemo cannot be curative

Unlike the histiocytic-sarcoma and hemangiosarcoma modules — whose resistance mechanisms were this
project's own extrapolation from general oncology — two of the three chemoresistance clones here are
**measured in canine lymphoma**:

- **P-glycoprotein (ABCB1/MDR1) efflux.** A canine lymphoid line selected on doxorubicin became
  resistant to doxorubicin *and* vincristine but **not** prednisolone, with high P-gp expression;
  resistance reversed completely with the P-gp inhibitor PSC833 (Zandvliet et al. 2014, *Toxicol In
  Vitro* 28(8):1498-506, PMID 24975508). This is the dominant real relapse mechanism, and it covers
  the two most active CHOP cytotoxics at once, which is why it sets the bar.
- **BCRP (ABCG2) efflux.** A second pump, upregulated at relapse. Across 63 dogs on doxorubicin-based
  chemotherapy, drug resistance occurred in **35/63 (55.6%)** and was associated with increased
  ABCB1 (B-cell) and ABCG2 (T-cell) expression; glucocorticoids did not change transporter
  expression (Zandvliet et al. 2014, *Vet J* 205(2):263-71, PMID 25475167).
- **Apoptosis evasion (TP53).** A generic category, modelled as a near-zero kill ceiling: a clone
  that cannot execute drug-induced death is unkillable by any cytotoxic no matter how much reaches
  it.

Chemo-only durable response, `run_monte_carlo` at `preexisting_prob = 0.80`:

| horizon | 1 yr | 2 yr | 5 yr | 10 yr |
|---|---|---|---|---|
| B-cell | 0.180 | 0.180 | 0.180 | 0.180 |
| T-cell | — | 0.177 | — | 0.177 |

It is **flat** because the dogs that relapse do so early (matching the real 176-day median), and the
~18% that do not are the ones whose tumour never harboured or acquired an efflux clone. No amount of
follow-up changes that split, because CHOP cannot out-kill the efflux clone at any point.

*Tests: `test_lymphoma_analysis.py::test_chemo_only_is_low_and_flat_across_horizons`*

---

## 2. Achievability: durability runs through immunotherapy

A lasting remission needs a mechanism that (a) covers every chemoresistance clone and (b) clears
~0.090/day. **CD20-directed immunotherapy** (an anti-CD20 CAR-T or monoclonal antibody) covers the
clones for free: CD20 expression is independent of drug efflux and of apoptosis machinery, so a
CD20 effector sees the P-gp, BCRP and apoptosis-evasion clones exactly as well as the sensitive one.
Resistance to a *drug* does not change what the *immune system* was trained to see — the same
argument the HSA and HS vaccine work made.

`run_monte_carlo_with_vaccine`, durable response by CD20-effector potency:

| `immunotherapy_max_kill` | 0.0 | 0.03 | 0.06 | **0.09** | 0.12 |
|---|---|---|---|---|---|
| 2-year durable | 0.217 | 0.220 | 0.217 | **0.993** | 1.000 |
| 10-year durable | 0.250 | 0.260 | 0.240 | **0.970** | 1.000 |

**The threshold sits exactly at the bar.** Below ~0.09/day the effector does essentially nothing to
10-year durability (0.24–0.26, barely above chemo-only); at the bar it reaches 0.97, and above it
1.00. The mechanism and its escape route are both real — canine CD20 CAR-T kills CD20+ lymphoma
cells and spares CD20-negative ones in vitro (Sakai et al. 2020, *Vet Comp Oncol* 18(4):739-752,
PMID 32329214) — but the *kill-rate magnitude* has never been measured in a completed canine
efficacy trial, so it is swept here, and the real durability anchor is the transplant cure fraction
(§6).

*Tests: `test_immunotherapy_threshold_2yr`, `test_immunotherapy_crosses_the_bar_between_0_06_and_0_09`,
`test_immunotherapy_at_the_bar_holds_to_ten_years`*

---

## 3. Escape routes

| # | Route | Status |
|---|---|---|
| 1 | `mdr1_pgp_efflux` | CLOSED by immunotherapy construction — and it sets the bar |
| 2 | `abcg2_bcrp_efflux` | CLOSED by construction |
| 3 | `tp53_apoptosis_evasion` | CLOSED by construction — with a real caveat |
| 4 | `cd20_antigen_loss` | Real; unclosable by single-antigen immunotherapy; **closable by a tandem construct** |
| 5 | CNS sanctuary | **OPEN** under chemo → closed by immunotherapy (§5) |
| 6 | immunotherapy failure without antigen loss | **OPEN** → a take-rate lever (§5) |
| 7 | treatment-related mortality of the cure | **OPEN** → a competing hazard (§5) |

Routes 1–3 are closed **by construction, not by potency**: none of these resistance lesions removes
CD20, so a CD20 effector still sees those cells. Route 3 carries the one honest caveat — immune
killing is only *partly* apoptosis-independent (perforin lysis largely is; granzyme/death-receptor
pathways can be blunted by the same evasion), so it is the least fully-covered of the three, not an
absolute bypass.

### Route 4 is real — and it behaves exactly like HSA's antigen-loss route

CD20 loss is the CD20 effector's own escape route, and unlike the HSA module's inherited MHC-I-loss
assumption, it is **documented in the actual disease**: the group that built canine CD20 CAR-T
observed CD20 loss in canine DLBCL patients treated with it, mirroring CD19/CD20-negative relapse in
humans (Peng et al. 2026, *Mol Cancer Ther*, PMID 42480604).

In simulation it behaves two ways depending on potency. A **sub-threshold** effector does not
out-kill the tumour and instead *converts* drug-resistance relapse into antigen-loss relapse — at
potency 0.03, **80 of 300** ten-year relapses become CD20-loss. At the **bar** (0.09) the route
**starves**: the antigen-positive population collapses before it can seed loss (1 of 300), and
durability is robust even at **100×** the assumed antigen-loss rate (0.970 → 0.927). Above the bar,
the antigen-positive population is gone before the mutation can supply the escape — the route
starves rather than being out-killed, exactly as HSA route 4 did.

*Tests: `test_subthreshold_immunotherapy_converts_relapse_to_antigen_loss`,
`test_antigen_loss_starves_at_threshold_and_is_robust_to_its_rate`*

---

## 4. Closing the potency gap

The achievability analysis leaves a gap: a CD20 effector only reaches durable response at or above
~0.090/day, and no completed canine trial has shown a real CD20 CAR-T gets there. Three closures.

### Route A — lower the bar with a persistent second agent

The bar is `growth − kill`, so a second persistent kill term clears it from the other side. Holding
the CD20 effector at a deliberately sub-threshold **0.06/day** and adding a persistent
mechanism-agnostic agent, 10-year durable response:

| persistent agnostic kill | bar after it | 10-yr durable |
|---|---|---|
| 0 | 0.0903 | 0.240 |
| 0.018 | 0.0719 | 0.367 |
| 0.028 | 0.0628 | 0.603 |
| **0.046** | **0.0444** | **1.000** |

The crossing is where the margin predicts. **One caveat specific to lymphoma**: the persistent agent
must not itself be effluxed by the P-glycoprotein clone it is meant to help suppress. Adding more
doxorubicin or vincristine does *not* lower the bar for the efflux clone — that clone is defined by
pumping exactly those drugs out. The persistent agent has to sidestep efflux (a non-cross-resistant
maintenance drug, or a P-gp inhibitor to restore the effluxed drugs).

*Tests: `test_lowering_the_bar_rescues_a_subthreshold_effector`, `test_lowering_the_bar_is_monotone`*

### Route B — two antigens instead of one (a tandem CD19/CD20 CAR)

The direct analog of the HSA dual-vaccine route, but with **real canine data instead of an assumed
additivity**: the same group that observed CD20 loss built a tandem CD19/CD20 CAR that eliminates
cells expressing CD19 and/or CD20, and showed canine B-cell lymphoma co-expresses both with
human-like heterogeneity (Peng et al. 2026, PMID 42480604). In this parameterization a single
antigen at the bar already starves the loss route, so the tandem construct's value is as **insurance**
when the real antigen-loss rate is higher, and as the necessary closure once the effector is strong
enough that antigen loss would otherwise be the last route standing. Below the bar it does not help:
closing antigen loss at potency 0.06 leaves durability at 0.210, because the drug-resistance clones
relapse regardless of antigen.

*Tests: `test_dual_target_closes_antigen_loss_but_only_matters_at_threshold`*

### Route C is *not* a closure — a one-time consolidation is not persistence

A single high-intensity consolidation — total body irradiation, the myeloablative step of a
transplant — does **not** carry durability on its own in this model, the same finding the HSA work
made for eBAT. Modelled as a strong mechanism-agnostic kill applied for a single ~14-day
conditioning window on top of CHOP + sub-threshold immunotherapy, 10-year durable response barely
moves (0.240 → 0.193 → 0.190 → 0.217 across TBI intensity) and dips within Monte Carlo noise. A
duration-capped kill, however intense, does not clear a bar that persists for a decade.

This is not a strike against transplant — it is the reason **the real curative protocol does not stop
at transplant.** Gareau et al. 2021 reached their cure fraction by adding **adoptive T-cell therapy**
to CHOP + transplant (see §6): a persistent immune effector on top of the consolidation. The model
and the real protocol agree — consolidation sets up the response; a persistent immune mechanism
carries it.

*Tests: `test_capped_duration_tbi_does_not_buy_ten_year_durability`*

---

## 5. Closing the open routes

### Route 5 — the CNS sanctuary → CLOSED by immunotherapy (the model upgrade)

The central nervous system is a pharmacologic sanctuary: the blood-brain barrier excludes most CHOP
cytotoxics (doxorubicin especially), so a clone that has seeded the CNS sees a fraction of the
systemic drug. This is the lymphoma analog of HSA's second compartment, and it is why
`run_monte_carlo_two_compartment` gained a `sanctuary_penetration_multiplier`: the sanctuary
compartment's *drug* exposure is discounted, while a systemic *cellular* effector still traffics
there.

Two-compartment model, 30% CNS involvement, 5-year horizon:

| CNS drug penetration | chemo-only durable | chemo-only CNS relapses | +CD20 effector (0.09) durable | +effector CNS relapses |
|---|---|---|---|---|
| 1.00 (no barrier) | 0.207 | 20 | 0.983 | 0 |
| 0.30 | 0.207 | 80 | 0.973 | 3 |
| 0.15 | 0.167 | 91 | 0.963 | 1 |
| 0.05 (excluded) | 0.170 | 83 | 0.973 | 0 |

Under chemotherapy, as CNS penetration falls the sanctuary becomes the **dominant relapse site** (20
→ ~90 of relapses). A systemic CD20 effector reaches it regardless of drug penetration and closes it
(CNS relapses ~0 at every penetration level). **This is the single sharpest argument for
immunotherapy over chemotherapy intensification** — reaching a drug sanctuary is something dose
escalation structurally cannot do. The specific penetration fractions are illustrative and swept,
not measured for the actual CHOP drugs in dogs.

*Tests: `test_lymphoma_engine_and_bar.py::test_lower_penetration_makes_the_sanctuary_the_relapse_site`,
`test_lymphoma_analysis.py::test_cns_sanctuary_dominates_relapse_under_chemo_and_is_closed_by_immunotherapy`*

### Route 6 — immunotherapy failure without antigen loss → a take-rate lever

T-cell exhaustion, an immunosuppressive microenvironment, or a manufacturing/expansion failure means
the effector never reaches its potency in a given dog. Modelled as a take rate: non-takers get the
chemo-only outcome. After potency itself this is the largest lever on the population durable
fraction, and unlike potency it is **directly measurable in a running trial** — a dog whose MRD
clears took the effector, one whose does not did not, knowable in weeks rather than from a survival
curve (Aresu et al. 2014, PMID 24698669; Sato et al. 2016, PMID 27339366).

### Route 7 — treatment-related mortality of the cure → a competing hazard

The one real curative option kills dogs too. Rupture was HSA's independent competing risk; here it is
transplant TRM. Tumour control (0.970) × survival of an independent annual TRM hazard, 5 years:

| annual TRM hazard | 0% | 7% | 13% |
|---|---|---|---|
| joint 5-yr durability | 0.970 | 0.675 | 0.483 |

The real figures: 7% died before discharge across 94 transplants (Benedict et al. 2024, *Vet Pathol*
61(5):765-770, PMID 38695516), and 8.3% (B-cell) / 13% (T-cell) in-hospital in the cohort studies
(§6). TRM is the largest single subtraction from a curative regimen's real-world success, and
lowering it (reduced-intensity conditioning, infection prophylaxis) is a durability lever in its own
right.

*Tests: `test_lymphoma_engine_and_bar.py::test_transplant_trm_competing_hazard_matches_recorded`*

### The lever that is only a timing lever — MRD

Minimal residual disease monitoring by flow cytometry and PARR, and RT-qPCR to ~1 cell in 10,000,
detects relapse before it is clinical (Aresu et al. 2014, PMID 24698669; Sato et al. 2016, PMID
27339366) — the lymphoma analog of HSA's liquid-biopsy screening. But **early detection alone does
not improve durability**: lowering the burden at intervention from 0.30 to 0.05 with a sub-threshold
effector leaves 10-year durable response flat (0.240 → 0.247 → 0.240), because burden changes where a
clone starts, not the sign of its growth margin. MRD's value is in deciding *when* to deploy a
bar-clearing mechanism and in reading out take — not in substituting for one. Re-treating a P-gp
clone at low burden with the same effluxed drugs still fails. This is exactly the role surgery played
for HSA: a delay/timing lever, not a durability mechanism.

*Tests: `test_mrd_early_retreatment_is_flat_without_a_bar_clearing_agent`*

---

## 6. The curative lever, and the real anchor: transplant + adoptive T cells

Autologous peripheral-blood hematopoietic cell transplant (autoPBHCT) with total body irradiation is
the one real canine-lymphoma therapy with documented long-term cures — and it is the empirical anchor
for what "cure or 10-year durability" actually costs.

- **B-cell** (Willcox, Pruitt, Suter 2012, *J Vet Intern Med* 26(5):1155-63, PMID 22882500): 24 dogs,
  87.5% engrafted, 8.3% in-hospital mortality; median disease-free interval 271 days, median overall
  survival 463 days; **5/15 (33%)** transplanted before relapse remained in remission at a median OS
  of 524 days — a real long-remission fraction, not just a median shift.
- **T-cell** (Warry, Willcox, Suter 2014, *J Vet Intern Med* 28(2):529-37, PMID 24467413): 15 dogs,
  DFI 184 d, OS 240 d, 2/13 alive past 740 days — worse than B-cell, as everywhere else.
- **The cure fraction** (Gareau, Ripoll, Suter 2021, *Front Vet Sci* 8:787373, PMID 34950726): CHOP +
  autoPBHSCT + **adoptive T-cell therapy** in 10 high-grade B-cell dogs — **4/10 (40%) disease-free
  for ≥2 years** (their explicit cure definition), against the ~70% of transplanted dogs that
  otherwise relapse from residual disease.

The 40% cure fraction is why the engine's story is calibrated to land *near*, not far above, that
number, and why the model treats transplant as consolidation + a persistent immune effector rather
than as a stronger dose of chemotherapy. It is the real proof that durability is achievable in this
disease — and its cost, the ~7–13% treatment-related mortality, is route 7.

---

## 7. The answer

A lasting remission runs through **immunotherapy**, not chemotherapy. CHOP makes the tumour shrink —
completely, in ~90%+ of dogs — and does essentially nothing to stop it returning, because the clone
that sets the bar (P-glycoprotein efflux) pumps the two most active CHOP drugs straight back out.
The bar is ~0.090/day, and chemotherapy moves it by 2%.

A CD20-directed immune effector covers all three chemoresistance clones by construction, because
none of them removes CD20. Below the bar it does nothing and merely converts drug-resistance relapse
into antigen-loss relapse; at the bar it reaches 0.97 at ten years, and antigen loss starves out. Its
one real gap — CD20 antigen loss, documented in real dogs — closes with a tandem CD19/CD20 construct
that has been built for canine lymphoma. The bar can also be cleared from the other side, with a
persistent second agent, provided that agent is not itself effluxed by the P-gp clone.

Of the routes left open: the **CNS sanctuary** is closed by the immune effector reaching a place the
drug cannot — the one thing dose escalation structurally cannot do, and the sharpest argument in the
analysis. **Immunotherapy take** is a measurable lever, read out by MRD. **Treatment-related
mortality** of the curative consolidation is the largest real subtraction, and partly reducible.
**Early detection** helps decide timing, not durability.

And durability is not hypothetical here: transplant plus adoptive T cells already cures **40%** of
dogs in a real cohort. The open work is raising that fraction — a stronger, potency-measured immune
effector; a tandem construct to insure against antigen loss; lower-toxicity conditioning — not
proving it is possible.

**T-cell lymphoma is harder on both counts.** Its faster growth raises the bar, so the same effector
potency that cures B-cell (0.09) leaves T-cell at 0.38 and only 0.12 reaches durable response — and
CD20 is a B-cell antigen, so the entire CD20 route does not even apply and a T-cell-directed effector
(CD5, CD52) is required, which is far less developed in dogs.

### What would change the answer

1. **Measure a canine CD20 CAR-T's kill rate directly** (serial imaging or MRD on a treated cohort),
   the way the HSA analysis asks for a vaccine kill rate. It would replace the swept potency with a
   number and settle whether real CD20 immunotherapy clears the ~0.090/day bar.
2. **Genotype the resistance at relapse** — efflux vs. apoptosis evasion vs. antigen loss. Each has a
   different closure, and re-treating a P-gp clone with effluxed drugs still fails.
3. **Measure real CNS penetration for the CHOP drugs in dogs, and the real CNS-involvement rate.**
   The sanctuary argument's strength depends on both.
4. **Power an MRD-response analysis** — does a dog whose MRD clears under immunotherapy stay in
   remission longer? That is the take-rate lever, and it is measurable now.
5. **Report transplant outcomes at 5 and 10 years, not 2.** The 40% cure fraction is defined at ≥2
   years; the stated target is a decade.
