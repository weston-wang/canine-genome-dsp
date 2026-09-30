# Lymphoma pipeline: settled results and known gaps

Branch-specific state, kept out of `CLAUDE.md` so that file can stay identical on every branch. Read this
before answering any "did we cover X / what's missing" question about lymphoma. Update it in the same
session as any new result or user decision.

## Settled (do not re-raise as new)

All in `docs/LYMPHOMA_DURABLE_RESPONSE.md` unless noted.
- The bar (~0.090/day, set by P-glycoprotein efflux; chemo moves it ~2%), section 1.
- Immunotherapy threshold at the bar, and CD20 antigen-loss behaviour, sections 2-3.
- Lower-the-bar, tandem CD19/CD20, and "a one-time consolidation is not persistence" (in the model),
  section 4.
- CNS sanctuary and the `sanctuary_penetration_multiplier` engine upgrade, section 5.
- 2-year to 10-year inference: mechanism-dependent; ~3% late drug-resistant tail at the bar, section 7.
- Toxicity ledger and chemo de-rating findings, section 8; completeness ledger and its two flagged
  exceptions (apoptosis evasion partly covered; late tail managed, not eliminated), section 9.
- Combination search (derived coverage, three filters, early detection removes rare mutational escapes
  but not phenotypic ones), section 10. **CNS T-cell does not close with anything obtainable** (short
  1.16x on the persister; a T-lineage cellular effector that traffics into the CNS is the missing object).
- Second cancers and therapy-related neoplasia are noted as a limit that cuts against long-term
  durability, section 7.
- The user's bar is "real data or rigorous model." "Not demonstrated in dogs" is already known and is not
  a finding.

## Inventory of the HS method reference (CLAUDE.md rule 3)

Every component of `origin/claude/canine-hs-analysis-graft` (the user's "HSA branch"), listed before any
rebuild. **Scope the user set for this rebuild:** "Rebuild if it helps answer the question I had about
whether we covered all mechanisms and potential escapes ... Ignore otherwise." So an item is "skipped"
only where it does not bear on that question, with the reason. Skips are flagged for the user's
confirmation and were not confirmed interactively.

| HS component | what it does | status here |
|---|---|---|
| `core/regimen.py` | derived-coverage object model | **Ported earlier** (`core/regimen.py`, plus an efflux mechanic) |
| `core/catalogue.py` | escapes and agents, per-compartment access | **Ported earlier** (`core/lymphoma_catalogue.py`) |
| `core/combination_search.py` | search over combinations | **Ported earlier** (`core/lymphoma_search.py`) |
| `pkpd.py` `emax_kill_rate`, `free concentration`, `margin`, `DrugPKPD`, `min_access_to_close` | kill rate derived from measured IC50 x exposure; can report "does not close" | **Ported** (`lymphoma_pkpd.py`), plus a required-IC50 inversion for agents with an exposure but no IC50 |
| `pkpd.py` trametinib target-attainment / dose-for-attainment / dosing workaround | population-PK spread for one HS drug | **Skipped**: built on one HS drug's Phase I; no lymphoma equivalent input. Revisit if a canine PK spread is found for a lymphoma agent |
| `core/evidence.py` | `Measurement` that refuses to be read for another population; `transfer_to()` | **Ported** verbatim (`core/evidence.py`) + 3 lymphoma `Disease` members |
| `core/toxicity.py` | organ-axis budgets; same-axis adds; de-rating not free; `profile_for` raises rather than failing open; efflux co-dose multiplier | **Ported** (`core/lymphoma_toxicity.py`, `_profiles.py`) **plus a time dimension** (evidence-limited window and hard cap per agent) |
| `core/tolerable_search.py` | search under organ budgets; efflux co-dose charged on partner's axis | **Adapted** (`core/lymphoma_grounded.py`): the reverser is a mechanism that charges its partners |
| `core/dormancy.py` | persister is a duty-cycle problem, not a wall for division-gated agents | **Adapted and corrected** (`core/lymphoma_dormancy.py`). Not raised earlier in this project. HS `kill_from` counts duty twice and credits division-gated kill at full strength against a partly-awake pool; the exact two-state solution weights it by the awake fraction f |
| `core/response_duration.py`, `core/treatment_horizon.py` | time to clear = ln(N0)/margin; treatment clock vs cumulative toxicity; "cure" only if cleared inside the tolerable window | **Adapted** (`core/lymphoma_horizon.py`) | 
| `core/schedule_coherence.py` | access and duty must come from one dosing schedule | **Partly adapted**: courses (TBI, HBI, RT) use full strength inside the course in the clock; CAR-T persistence is a measured duration cap. A full access-vs-duty schedule check per agent is not built |
| `core/delivery.py` | delivery routes as composable objects (FUS, CED, IT, efflux inhibition) | **Partly covered**: lymphoma CNS routes are already agents with per-compartment access. FUS/CED **skipped** (not evaluated for lymphoma; flagged) |
| `core/hs_drug_sensitivity.py` | IC50 measured in the actual disease, outranks assumed potency | **Adapted** as canine-lymphoma inputs (`lymphoma_grounded_inputs.py`) |
| `sequence_conservation.py` | human-vs-dog target identity for transferred drugs | **Skipped for now**: lymphoma agents that are human-designed (acalabrutinib, venetoclax) have canine in-vivo or in-vitro measurements. Flagged: revisit for any agent whose potency ends up TRANSFERRED |
| `docs/PRIOR_ART_COMBINATIONS.md` | has each proposed combination been tried, in what species | **Not covered here yet.** To do for the regimens in `LYMPHOMA_COVERAGE_LEDGER.md` §6 |
| `docs/THERAPY_STRATEGY.md` coverage-by-evidence-tier table | escape x closing agent x evidence grade | **Adapted**: `docs/LYMPHOMA_COVERAGE_LEDGER.md` |
| `core/durable_regimen.py`, `cycled_regimen.py`, `breed_wide_durability.py`, `genotype_tiered_durability.py`, `microtubule_route.py`, `brain_*.py`, `intraarterial_route.py`, `metronomic_bbb_check.py`, `mgmt_escape.py`, `presentation.py` | HS-specific: brain tumour, MTAP/breed, intra-arterial route, MGMT | **Skipped**: no lymphoma analogue (different organ, driver and route). The P-gp escape already plays the MGMT role |
| `docs/CONSOLIDATED_REPORT.md`, `plain_language_report.html`, `researcher_brief.html`, `preprint/` | HS write-ups | **Skipped** as outputs; the lymphoma layman report exists and is updated only if conclusions change |

## Settled by the potency / toxicity / clock rebuild (2026-09-30; do not re-raise as new)

Full record: `docs/LYMPHOMA_COVERAGE_LEDGER.md`. Tests: `tests/test_lymphoma_ledger.py`,
`tests/test_lymphoma_grounded.py`.

- **Answer to "did we cover all mechanisms and escapes, with potency and toxicity considered":** every
  mechanism raised is in the model and reached by an agent (13 lineages: the earlier 11 plus
  antigen-presentation loss and MGMT repair). **Not every escape is closed by measured or derived
  potency.** No combination of only STRICT-grade agents (verdinexor, the canine anti-CD20 antibody,
  venetoclax on T-cell) closes every escape.
- **Smallest anchored sets:** B-cell doxorubicin + canine anti-CD20 antibody + verdinexor (+0.101, clears
  by day 51, 25% tightest-axis headroom, TP53 closes on strict potency at only +0.009); T-cell
  doxorubicin + vincristine + venetoclax (+0.060) or doxorubicin + venetoclax (+0.008). With licensed and
  off-label agents only, nothing outcome-graded clears the B-cell persister inside the windows.
- **The CNS sanctuary is open at every evidence grade.** B-cell clears in the model only with the
  trial-stage CD20 CAR-T + craniospinal RT + half-body irradiation on four assumed potencies; T-cell needs
  the non-existent T-lineage effector.
- **Corrections to earlier statements** (kept in place in `LYMPHOMA_DURABLE_RESPONSE.md`, qualified there):
  (a) the two-drug "minimal closing" regimens relapse when a drug has to stop; (b) the CNS B-cell closure by
  immunotherapy holds only while the CAR-T lasts, and measured canine persistence is about 14 to 50 days
  (anti-mouse antibodies, PMID 32002286, 35898541); (c) P-gp is closed in vitro from the drug side but a
  canine randomised trial of valspodar + doxorubicin (n = 20, PMID 28357033) showed no survival difference;
  (d) the "no efficacious caninized anti-CD20 product is established" note is out of date (PMID 38662527,
  41742528); (e) the persister "wall" is the corner f = 1, r = 1 of the two-state model, so the "three
  filters" claim that no conventional cytotoxic survives the persister filter no longer holds: a
  division-gated agent counts f times its kill; (f) the primary source for observed CD20 loss in dogs is
  PMID 32002286 (exons 4 and 5 absent), not only the Peng 2026 citation.
- **Model conflict resolved in direction, not in size.** The old model said a one-time consolidation adds
  no durability because it averaged a 28-day course over a year. The clock uses in-course strength: adding
  low-dose-rate half-body irradiation to CHOP removes the pump-lineage relapses, in the direction of the
  real data (first remission 39% vs 8.7% at 2 y, 18% vs 4.4% at 5 y, n = 75 vs 115, PMID 42525883). The
  deterministic clock gives cure or relapse, not fractions.
- **Calibration:** CHOP alone at a clinically obvious burden is predicted to relapse (bulk after day 126,
  pump lineages after day 150) against real median PFS 176 d. Regression: the grounded model reproduces
  v1's recorded margins for v1's regimens.
- **Founder lesions:** TP53 (25.6%) and TRAF3 (58.1%) are present from the start in that share of B-cell
  dogs (PMID 39922874), so earlier detection cannot remove those escapes; they stay in the set to close.

## Known gaps (factual)

- **Potencies still ASSUMED or unresolved:** rabacfosadine, lomustine, high-dose methotrexate, IT
  cytarabine, radiation, anti-PD-1, CD20 CAR-T in vivo, acalabrutinib (killing modest, no IC50). Hinges:
  hydroxychloroquine closes only if its canine-lymphoma IC50 <= ~100 uM (none found); prednisolone is a
  bracket 0.0098-0.144/day (two canine measurements disagree ~15x); venetoclax T-cell exposure is
  second-hand and its free fraction unmeasured.
- **Verdinexor:** derived kill 0.27/day (B) vs clinical response 37%, median duration 18 d. Unexplained.
- **Loads are summed as if every agent were given at once**; a scheduling layer (induction then
  consolidation) is not built. It penalises sequenced consolidation: full CHOP + TBI puts marrow at 1.5.
- **The clock is mean-field** and clears only lineages present at diagnosis.
- **Persister awake fraction f, retained tolerance r, switching rate** are unmeasured in canine lymphoma.
- Not built (flagged skips from the inventory): genotype-tiered agent choice (TRAF3/TP53 status),
  focused-ultrasound / convection-enhanced delivery, target-conservation checks, per-combination prior
  art. T-cell kinase inhibitors and canine IL-15 armouring: nothing found to model.
- Other sanctuaries (eye, testis, marrow niche) and breed effects remain unscoped: no canine mechanistic
  data found; one testis-to-brain relapse case (PMID 37265807).
- **The HS dormancy module (`core/dormancy.py` on the HS branch) has the double-duty / full-strength
  issue described in `LYMPHOMA_COVERAGE_LEDGER.md` §2.** Not changed there; it is the user's call.

## Branch drift

`claude/codex-branch-audit-clfeiz` has moved since this branch duplicated it at `66cfa76`; its tip is now
`5656f74` (2026-09-08, "Record the three published HSA reports in the narrative document"). This branch has
not picked those commits up.


## Closing-combination result (see `LYMPHOMA_CLOSING_COMBINATION.md`)

- **Settled at MODEL strength:** with derived cytarabine, transferred HCQ, derived radiotherapy and
  sustained intrathecal delivery, programs exist that close every modelled escape in body and CNS. Best:
  B-cell = HCQ + verdinexor + continuous intrathecal cytarabine + anti-CD20 (survives halved potencies).
- **T-cell:** existing-drug version is fragile (fails halving, fails clinical burden); CD7 CAR-T version
  closes body robustly but brain fails at halved potency. T-cell brain needs the pump.
- **Corrections to earlier notes:** HCQ is a P-gp substrate (not independent of efflux); derived
  radiotherapy potency is lower than the assumed 0.30; CNS access values corrected; CNS clearing needs
  sustained intrathecal delivery, not bolus.
- **Standard recorded:** sound-grade bar = measured, derived, or transferred-with-written-basis; assumed
  inputs never tuned to force closure.
- **Known gaps:** every agent load-bearing (no redundancy); HCQ CNS access assumed; verdinexor
  derived-vs-clinical mismatch; pump chronic toxicity unknown; buildable agents; mean-field clock.

## Gap raised by the user (2026-09-30): "How come vaccine isn't part of this"

- **Record check:** the rebuilt catalogue (`core/lymphoma_grounded.py`, `core/lymphoma_catalogue.py`) has **no
  vaccine agent**, and no document records a decision to exclude one. The only "vaccine" in the lymphoma work is
  v1's use of the vaccine *engine* (`run_monte_carlo_with_vaccine`) as a stand-in for a CD20 effector
  (`LYMPHOMA_DURABLE_RESPONSE.md` s5). So this is **not covered**, and was an omission, not a settled exclusion.
- **Canine lymphoma vaccine literature found (PubMed, not yet graded or modelled):** dTERT genetic vaccine +
  COP (PMID 20531395; 13/14 immune responders, survival >97.8 vs 37 wk historic controls) and larger follow-up
  (PMID 23902422; >76.1 vs 29.3 wk); Tel-eVax + CHOP (PMID 30537967; OS 64.5 wk, no control arm);
  autologous tumour-cell + hGM-CSF vaccine, randomised placebo-controlled, **no clinical benefit**
  (PMID 19754780); autologous DC vaccine pulsed with a canine B-cell leukaemia lysate gave no DTH response
  (PMID 17917377). Reviews: PMIDs 41006003, 26545847.
- **Why it may matter:** a vaccine targets a different antigen (e.g. TERT) from CD20/CD19, so it is a candidate
  for the antigen-loss escapes. **Why it is not yet closure:** the evidence is survival in weeks against
  historical controls, not a kill rate against persisters; it would be graded at best REGIMEN-CALIBRATED and
  cannot be called closing without a derived potency.
- **Next step, not done:** add a TERT-vaccine agent to the grounded catalogue with an explicit transfer basis,
  and test whether it removes the "every agent is load-bearing" weakness.
