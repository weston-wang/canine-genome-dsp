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

| Report | Audience | Link |
|---|---|---|
| Splenic Hemangiosarcoma Consolidated Analysis | technical reader wanting the whole argument | https://claude.ai/code/artifact/12202c48-d95e-4ca1-abde-b51369d64181 |
| The Three-Move Plan | plain language — clear it, hold it, catch it early | https://claude.ai/code/artifact/3e895f36-2140-4bd3-a533-5545e987c8d8 |
| The Potency Gap | researchers — what is additive here, and the experiments ranked | https://claude.ai/code/artifact/c70ccea7-571f-406f-bcec-bd0c29671e33 |

All three were revised on 2026-10-01 to carry the sweep above; *The Potency Gap* §06 is the changelog.

## Test status

`743 passed` (2026-10-01). Five test modules require `torch` and were not run in that container:
`test_hybrid_rnn`, `test_alphafold`, `test_hsa_cli`, `test_mapk_cli`, `test_vaccine_eval`. The HSA
analysis modules themselves have no such dependency. Run with
`PYTHONPATH=src python3 -m pytest tests/ -q` (needs numpy, scipy, pandas, scikit-learn, matplotlib).
