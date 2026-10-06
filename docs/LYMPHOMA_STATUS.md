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

## Correction (2026-09-30): the closing-combination result is INTERIM, not "goal completed"

The user: "I don't get how you can claim the goal is completed when even I know vaccine should be part of the
equation, and maybe even stem cell. Go back and be thorough." Accepted. The closing programs are closure
within 26 catalogue entries and 14 escapes only; the candidate universe was not enumerated (no vaccine, no
separate stem-cell/transplant mechanism beyond one OUTCOME-graded TBI+transplant entry, no CD52/ADC/bispecific/
proteasome/HDAC etc. sweep) and the escape list was not independently audited (for example glucocorticoid-
receptor loss and cytarabine dCK loss are not separate escapes). Lesson recorded in `CLAUDE.md` (failure 5, rule
9) on all four branches that carry it. Work in progress: four literature sweeps (vaccines; stem cell/transplant;
all other modalities; independent escape audit), then catalogue additions, re-search, and a universe ledger.

## Result of the thorough re-sweep (2026-10-01) -- supersedes the closing-combination claim above

Full tables: `LYMPHOMA_UNIVERSE.md`; sweep reports: `docs/universe/SWEEP_*.md`; code: `core/lymphoma_universe.py`,
`tests/test_lymphoma_universe.py`.

- **The goal is NOT met.** With the audit's 9 added escapes (23 in all) and the sweeps' added agents, at sound grades and every
  escape required closed: the brain does not close for B-cell or T-cell disease at any availability tier, including buildable agents.
  The body closes only with trial-stage agents plus a weak vaccine credit, or with agents that do not exist (a persistence-engineered
  CAR-T; a CD7 CAR-T). Every body set tested fails when potencies are halved or any agent is removed.
- **Why:** E5 (a quiescent, pump-high lymphoid progenitor, measured as a hierarchy in dogs) is missed by every division-gated agent and
  every pump substrate; E2 (dCK loss) removes the cytarabine arm that closed the brain. A closing brain agent must be non-gated,
  non-pump, CD20/CD19-independent and kill at >= 0.10 /day (0.19 at half access); none in the sound pool does.
- **Vaccine:** in the model (OUTCOME 0.055 /day) but gives no persister or brain credit and its benefit disappears at half credit;
  dog data show a flat tail (3-year survival 10% vs 8%). dTERT, CD40-B, GM-CSF cell and DC vaccines were evaluated and excluded
  (PFS null, or no response).
- **Stem cell:** autologous TBI + transplant is in the model; allogeneic DLA-identical transplant (8/9 >4 y) has the best dog
  durability tail but no kill rate, no CNS or T-cell data, and a donor and mortality cost. "Cancer stem cell" is escape E5.
- **Corrections found:** Gareau 2021 (T cells did not add benefit; docs fixed); anti-PD-1 has no responses in 15 lymphoma dogs
  (regraded MEASURED-NEGATIVE, potency 0); the anti-CD52 antibody (Tactress) is licensed but its RCT was null and it lacks target
  specificity (PMID 36329876); the "testis-to-brain" case is spermatic cord with no chemotherapy.
- **Exposure sweep finished:** panobinostat, vorinostat, bortezomib entered at transferred exposures (TRANSFER); the conclusion does
  not change. PI3K-delta and flavopiridol have no canine IC50, so no kill rate (`docs/universe/SWEEP_pk.md`).
- **Still open:** E12 unattributed
  resistance, eye/testis, second cancers sit outside the model; no 10-year dog data.

## Brain closure attempt (2026-10-01; user: "So your goal isn't met yet, close the brain ones")

Details: `LYMPHOMA_UNIVERSE.md` section D; sweeps `docs/universe/SWEEP_regional.md`, `SWEEP_cnsregimens.md`; code `core/lymphoma_universe.brain_agents`;
tests `tests/test_lymphoma_universe.py`.

- **Status: closed in the model only conditionally, not robustly.** With CSF-delivered CAR-T (and antibody), the brain clears every one of the 23 escapes
  for B-cell and T-cell disease IF the CSF CAR-T is active for >= ~35% of each dosing interval. At the conservative one-seventh the B-cell brain
  barely clears (margin +0.015, day 178, one 4-agent set) and the T-cell brain does not. Every clearing set fails with halved potencies or one agent removed.
- **Depends on agents that do not exist** (CSF CAR-T, persistence-engineered/CD7 CAR-T, the intrathecal pump) and on an assumed CAR-T kill (0.12 /day).
- **Thiotepa-based consolidation** (human 8-year event-free 67%) is in the model as an OUTCOME program (0.13 /day); it closes the brain without the CSF CAR-T only
  if it is accepted as acting on dormant cells and not pumped out, which the data do not show.
- **Measurements that would settle it:** CAR-T persistence in dog CSF; in-vivo CAR-T kill; parenchymal access; chronic reservoir safety in dogs; thiotepa
  transporter status and dormant-cell kill.

## /goal (2026-10-01): "keep going by more research or modeling to fully close every mechanism and escape then. I know car t has human results for CNS"

Accepted. The CAR-T brain inputs in the model were ASSUMED (CNS access 0.5, 0.12 /day, CSF persistence swept) although human CNS CAR-T data exist.
Two sweeps launched to replace them with transferred human numbers: `docs/universe/SWEEP_cart_human.md` (CNS lymphoma/leukaemia outcomes, CSF CAR-T
levels, durability, antigen escape) and `docs/universe/SWEEP_cart_kill.md` (in-vivo kill-rate derivation, dog translation, dosing duty).

## Result of the /goal (2026-10-01): closed within the model at human-grounded central inputs -- supersedes the brain note above

Details: `LYMPHOMA_UNIVERSE.md` section E; `src/canine_dsp/lymphoma_joint.py`; tests `tests/test_lymphoma_universe.py`.

- **Within the 23-escape, sound-grade model**, B-cell (7 and 8 agents) and T-cell (5 and 8 agents) programs clear the body AND the brain together, toxicity charged on the union, with all potencies halved and with any one agent removed, at the central human-grounded CAR-T inputs (kill 0.35 /day, CSF duty 0.4).
- **Fails at the low inputs** (kill 0.12, duty 0.15). The dog value is set by CAR-T expansion, not potency; dog CAR-T efficacy is not yet shown.
- **Replaced assumptions:** CAR-T kill rate, brain access, CSF duty, neurotoxicity budgets and 5-10 year durability now come from human data (TRANSFER/OUTCOME/MEASURED).
- **Still outside:** E12, eye/testis, second cancers, non-relapse mortality, parenchymal access, and the existence of the agents.

## Confirmation matrix (2026-10-01; user: "The key is to confirm that all mechanisms and escapes are truly addressed")

`docs/LYMPHOMA_ESCAPE_CONFIRMATION.md`, generated by `lymphoma_joint.escape_matrix` and asserted by tests: B-cell 7-agent program 44 of 44 and T-cell 5-agent program 42 of 42
escape-by-compartment rows closed (positive net margin after toxicity de-rating), at least 3 independent covering agents on every row. Scope: 23 escapes, sound-grade agents,
human-grounded central CAR-T inputs; the items outside the matrix are listed in that file.

## Report simplified (2026-10-02; user: "Simplify and update the report then")

`docs/LYMPHOMA_PLAIN_LANGUAGE.html` rewritten as a short report: the result, the two plans with availability, a per-escape table generated from `lymphoma_joint.escape_matrix`
(so it cannot drift from the tested result), what the numbers rest on, what has to be true, what is outside the check, and what was set aside. The earlier long report is in git history.

## Re-assessment (2026-10-02; user: "I needed scientifically sound, not totally theoretical. And I think you are dismissing vaccines, ebats, inhibitors, stem cells too easily.")

Details: `LYMPHOMA_UNIVERSE.md` section F; `docs/universe/SWEEP_{vaccines,stemcell,bispecific,inhibitors_partial,exists,hct_model}.md`; code `core/lymphoma_universe.reassessed_agents`, `inhibitor_agents`;
`lymphoma_joint.EXISTING_PROGRAMS`, `clock_table`. CLAUDE.md rule 13 (programs from agents that exist; a class is excluded only for a stated scientific reason).

Result, **within the 23-escape sound-grade catalogue, programs built only from agents that exist today** (licensed, off-label or in dog trials):
- **B-cell body: closes** (e.g. anti-CD20 + verdinexor + matched-donor transplant + oral cytarabine ocfosfate; margin +0.15 /day, last lineage gone by day 74). Closes at central inputs; sets of 5 clear but none survives halving or removing one agent.
- **B-cell brain: one escape open**, E5 (dormant, pump-armoured lymphoid progenitor; regrows after ~day 84).
- **T-cell body: one escape open**, E5 (regrows after ~day 166).
- **T-cell brain: three open**, E2 (dCK loss), E5, and bulk.
- Longer dosing does not close the B-cell brain (tested 120-730 d windows).

Class handling: allogeneic DLA-identical HCT credited (OUTCOME); autologous add-back and thiotepa credited (OUTCOME); vaccines credited (APAVAC 0.055, dTERT ~0.028 /day; gated, MHC-dependent, small); inhibitors credited by TRANSFER (HDAC and BTK classes; none reaches E5);
canine CD3xCD20 engager credited at 0.16 /day (TRANSFER-OUTCOME, tier NONE: needs development); bispecific-armed T cells have no kill rate in any lymphoma trial; eBAT excluded for a stated reason (EGFR/uPAR lower in 29 canine lymphomas than in sarcomas; target-negative human T-cell line not killed; dog hypotension 4/23).

Gap specification: one more non-gated, non-pump, compartment-reaching agent, effective kill >= ~0.06 /day in brain (>= ~0.03 /day T body), within organ budgets. Candidates with human data that need development: CAR-T (CSF, CD7/CD5+CD7) and the canine CD3xCD20 engager (B only; 0.16 x 0.5 = 0.08).
With one such agent at central human-grounded inputs the 7-agent B and 5-agent T programs close body and brain (previous section).

Still unresolved: unfinished inhibitor sweep (PI3Kdelta, flavopiridol have no canine IC50; carfilzomib); HCQ brain access 0.3 unsourced (not load-bearing); dog CAR-T expansion; MHC-loss escape for allo/vaccine/engager; E12, eye/testis, second cancers (outside model).
Report: `docs/LYMPHOMA_PLAIN_LANGUAGE.html` (artifact Version 14).

## /goal (2026-10-02): "keep going until you truly close all. I don't mean you can only use therapies that exist today, I meant to include near future ones this are scientifically sound. Just nothing that's pure theoretical"

Details: `LYMPHOMA_UNIVERSE.md` section G; sweeps `docs/universe/SWEEP_near_future_cell.md`, `SWEEP_outside_model.md`, `SWEEP_nongated.md`; code `lymphoma_joint.READINESS`, `NEAR_FUTURE_PROGRAMS`, `tier_mix`; tests `tests/test_lymphoma_universe.py` (25). CLAUDE.md rule 13 amended and propagated to all four branches.

- **Closed within the model** (28 sound-grade agents per immunophenotype, 23 escapes, tiers A-C only, toxicity on the union): B-cell (9 agents) and T-cell (8 agents) programs clear body and brain **at the pessimistic inputs** (CAR-T kill 0.12/day, CSF duty 0.15), no single agent load-bearing; 44/44 (B) and 42/42 (T) escape-by-compartment rows closed with >=4 / >=5 covering agents; last lineage gone day 49/72 (B body/brain), 80/158 (T body/brain). At the central inputs they also survive halving every potency.
- **Not robust to uniform halving at the pessimistic inputs**: B brain E5 regrows after day 84, T brain E2 reopens. This is the same fact as the threshold below.
- **The input the closure turns on**: CAR-T effective kill. B without the engager clears at >=0.08/day (duty 0.15) and is fault tolerant from 0.2/day; T clears from 0.12 and is robust from 0.2; central 0.35. Dog CAR-T (7 dogs) did not expand or persist, so this is a stated condition; in-vivo CAR-T (human first-in-human) and, for B, the CAR-T-free route (antibody + engager + transplant + cytarabine) address it.
- **Superseded**: "at the low inputs the B-cell programs do not clear" (true only without the engager and oral cytarabine); "only exists-today agents" as the bar (section F).
- **Items formerly outside the model, now graded** (rule 11/14): MHC loss closed by derivation for a DLA-identical donor (condition: such a donor; haplo would reopen 7-29%); E12 closed by transfer (axi-cel 31% ongoing at ~5 y in chemo-refractory LBCL); eye closed by a local agent; testis closed; parenchymal access closed as transferred factors (no non-enhancing-lymphoma measurement exists for any agent); second cancers and non-relapse mortality are costs, not escapes.
- **Agent search for E5**: no new agent shown to kill the dormant pump-armoured progenitor in the brain; thiotepa pump-substrate default removed (no P-gp cross-resistance); CDK9 inhibitors and artesunate are candidates without a gradable kill rate. BCL6 is not a canine-DLBCL driver (rarely expressed).
- **Conditions** (decidable list): near-future agents built for dogs (dog engager and CAR-T construct, CSF route); CAR-T kill >=0.2/day for full fault tolerance; DLA-identical donor; step-up engager dosing (dog cytokine storm to a T-cell agonist antibody); local treatment of ocular disease. Strength: model result on TRANSFERRED/OUTCOME inputs, not a demonstration in a dog.
- **Search limitation**: the search forbids two agents of one family, so fault-tolerant programs (two CAR-T constructs) were assembled from the agents it selects and verified by direct evaluation.
- Report regenerated (`docs/LYMPHOMA_PLAIN_LANGUAGE.html`, artifact Version 15) from `lymphoma_joint.clock_table` at the low inputs.

Test-suite note (2026-10-03): six tests in `tests/test_lymphoma_ledger.py` had been failing since the universe widening (they assert the v1-catalogue ledger claims, and the added agents, e.g. oral cytarabine and transplant, change those results). They now run on the v1 catalogue through an explicit fixture; the widened-catalogue claims are tested in `tests/test_lymphoma_universe.py`. All lymphoma suites pass (ledger 53, universe 25, grounded/search/analysis/engine/inference all green).

## Audit and growth bar (2026-10-03)

`src/canine_dsp/lymphoma_standard_audit.py`: `failing()` now returns [] (tested). It had returned one item, the growth-rate bar 0.0903/day, a bare "illustrative, not fitted" literal gating every margin (CLAUDE.md failure 7 again); derived as a dog-data bracket (net 0.015-0.12/day, gross ceiling 0.204; `docs/universe/SWEEP_growth_bar.md`, `LYMPHOMA_UNIVERSE.md` G.1).
Closure at higher bars (potencies fixed): B-cell clears at every bar to 0.204 at both input sets; T-cell clears at the central CAR-T inputs to 0.204, and at the pessimistic CAR-T inputs only for a bar <= ~0.10/day. `growth_sensitivity()` regenerates the table. Unsourced HCQ brain access 0.3 is inert for closure (programs clear without it).

## /goal (2026-10-04): "do 1, and if you can't find them then go back to the drawing board to see if there's other ways to close these"

Details: `LYMPHOMA_UNIVERSE.md` section H; sweeps `docs/universe/SWEEP_dog_programs.md`, `SWEEP_persistent_graft.md`, `SWEEP_sustain.md`, `SWEEP_regrade.md` (partial: rate limit); code `lymphoma_joint.DOG_STATUS`, `lymphoma_sustained.py`, `lymphoma_standard_audit.routes_not_counted`; tests (33 in `tests/test_lymphoma_universe.py`).

- **Item 1 result.** Only the B-cell CAR-T has a dog program (Penn autologous CD20 trial active, did not expand in 7 dogs; LEAH xenogeneic on hold; tandem CD19/CD20 preclinical with stated intent). **Not found**: canine CD3 engager, CD7/CD5 CAR-T, CSF-route CAR-T or antibody, in-vivo CAR-T in dogs. "Near-future for dogs" was overstated for those; they are labelled "class clinical-stage in humans; canine version not started". (Lesson for the next thread: a human trial class is not a dog program; search registries, grants and pipelines before calling an agent near-future.)
- **Drawing board.** Persistent graft-versus-lymphoma holds but does not clear (needs 0.06-0.12 /day vs a 0.0008-0.004 bracket). Re-graded existing dog agents (rabacfosadine, lomustine, L-asparaginase) do not kill dormant cells. **Sustaining an existing agent closes E5**: B-cell brain with oral cytarabine ocfosfate ~1,500 d (conditional on a CSF time-average >= ~0.11 uM and multi-year tolerability, both unevidenced); T-cell body with verdinexor ~170 d; T-cell brain not (E5 needs ~8 y). Section F's "longer dosing does not close the brain" (tested only to 730 d) is withdrawn.
- **Correction (mine, found by reading the full text):** the "CSF 1.0-3.6 uM measured" for oral cytarabine ocfosfate was a trough ratio x peak serum product; measured CSF troughs are 0.04-0.27 uM, derived time-average 0.3-1.4 uM. The model now uses 0.3 uM; the T-cell near-future program is no longer fault tolerant at the pessimistic inputs (the intrathecal cytarabine is load-bearing); B-cell unchanged.
- **Decidable list**: B body closed with existing agents; B brain conditional (sustained cytarabine, or the dog CAR-T at >= 0.12 /day); T body conditional (verdinexor ~6 months); T brain open without CD7/CD5 CAR-T (no dog program). `failing()` is [] for the counted programs; `routes_not_counted()` lists the three routes set aside with their grades.

## /goal (2026-10-04, second): "it doesn't sound you found realistic ways of closing these then, more just hand waving and saying some future car t program will solve it. That's a goal failure, keep going"

Accepted: section H leaned on an unbuilt CAR-T and missed radiation. Details: `LYMPHOMA_UNIVERSE.md` section I; `lymphoma_sustained.py` (`rt_agent`, `clock_with_rt`, `minimal_window_with_rt`); `docs/universe/SWEEP_rt.md` (partial: rate limit); tests.

- **Record inconsistency fixed in the new module:** radiation was tagged division-gated in the v1 catalogue by assertion while `SWEEP_hct_model` s7.2 derived it cycle-independent (27 canine lines, PMID 27257868); plus human non-cycling CLL apoptosis (~85%) and quiescent HSC radiosensitivity. v1 untouched (ledger tests run on v1 explicitly); new module applies the in-vivo factor 1.9.
- **Realistic programs from agents that exist:** B body (closed, day 74); **B brain** = body program + one 23.4 Gy whole-brain/craniospinal course + oral cytarabine and verdinexor sustained 975 d (median canine line; 1,253 d resistant; 250 d sensitive; 1,560 d without radiation), clears with toxicity de-rating and courses stacked from day 0; **T body** = T-cell program with verdinexor sustained ~170 d.
- **T-cell brain stays open**: sweep to 3,650 d never clears at any radiation value in the evidence range; 432 staged schedules of RT + thiotepa + transplant + cytarabine none clears; toxicity-ignored union does clear (budget problem). Needs ~19.6 e-folds in vivo; 36 Gy is ~10 for human T-lineage radiosensitivity, ~21 only at stem-cell radiosensitivity. Decided by a measurement: primary canine T-lymphoma radiosensitivity.
- **Inputs carrying B brain:** radiation e-folds on the dormant progenitor (TRANSFER) and >2-year continuous oral cytarabine tolerability (ASSUMED). Dog TBI dose-escalation did not reduce relapse (PMIDs 3887690, 3901841): e-folds not credited above one conventional course.
- Engager, CAR-T and CSF routes are now additional, not required, for B and T body.

## /goal (2026-10-05): "look broader to close the T-cell brain. Do not stop until you found something. Something being worked on actively is acceptable. Purely theoretical from you is not"

Details: `LYMPHOMA_UNIVERSE.md` section J; sweeps `docs/universe/SWEEP_tcell_agents.md`, `SWEEP_brain_access.md`, `SWEEP_wake_dormant.md`, `SWEEP_xpo1_cns.md`, `SWEEP_nm600_itmtx.md`; code `lymphoma_sustained.it_mtx_agent`, `clock_program`, `minimal_it_mtx_window`; tests (38 in `tests/test_lymphoma_universe.py`).

- **Found: the T-cell brain closes** with the T-cell program at its documented windows (matched-donor transplant, verdinexor, ...) + one 23.4 Gy whole-brain/craniospinal course + **repeated intrathecal methotrexate** (routine in dogs: PMID 25041580, 112 dogs; standard CNS prophylaxis in human T-ALL) at a mean kill of 0.12 /day (about every 2-3 weeks): **399 days** at the median canine line (841 resistant, 231 sensitive, 1,346 with no radiation); 0.2 /day gives 336. The transplant is load-bearing (>4,000 days without). Verdinexor and oral cytarabine are not needed (462 days with only transplant + radiation + methotrexate). The same route closes the B-cell brain in 399 days, replacing 2.7-3.4 years of oral cytarabine.
- **Why it was missed:** the model had no intrathecal methotrexate (only an ASSUMED-grade intrathecal cytarabine, which dCK loss defeats). Verdinexor's brain access (an unsourced 0.05) was also wrong in direction: selinexor brain:plasma 0.60-0.72 at an intact barrier in three species (PMID 27323910), human enhancing tumour 0.09; verdinexor itself unmeasured (TRANSFERRED 0.6, floor 0.09; closes the T-cell brain alone only with 5-7 years of dosing).
- **Looked at and not credited:** 90Y-NM600 (in dogs with PTCL now; brain metastases developed in 2 of 4 treated dogs, poor intact-barrier uptake), focused-ultrasound BBB opening and osmotic BBB disruption (no canine drug-delivery data / not veterinary practice), plerixafor and G-CSF waking of dormant cells (null or weak in AML), JAK1/ITK/PI3K/HDAC/EZH2 inhibitors (no measured CNS access or kill; soquelitinib and oclacitinib are leads for a CSF measurement).
- **Weak points (stated, not hidden):** the methotrexate kill is derived (canine IC50 2-3 nM is a secondary citation; dog CSF volume taken equal to human); intrathecal drug reaches CSF and perivascular spaces, not deep parenchyma (at half the kill, 800 days and verdinexor brain access >= 0.3); leukoencephalopathy with whole-brain radiation plus repeated intrathecal methotrexate (29% at 2 y with high-dose methotrexate; HR 4.5) is not captured by the budget and has no canine series; repeated dosing in a dog beyond 6 doses has no source.
- Supersedes: section I.3/I.4 "T-cell brain: no program closes it" and H.4's T-cell brain row.

## /goal (2026-10-06): "I know there's that rule where human meds can be used for pets under exceptions. Make sure the human ones you cited qualify. Also some of these closures seem to be on weak grounds, I need you to look further and truly close these"

Details: `LYMPHOMA_UNIVERSE.md` section K; `docs/universe/SWEEP_legal.md`; code `lymphoma_sustained.LEGAL_STATUS`, `lawful_pool`, `LAWFUL_PROGRAMS`, `lawful_clock`, `minimal_lawful_window`; tests 41 in `tests/test_lymphoma_universe.py`.

- **The rule, verified:** 21 CFR Part 530 (AMDUCA 1994) permits extra-label use of **FDA-approved animal drugs and FDA-approved human drugs** by/on the order of a veterinarian within a VCPR. It does **not** make an unapproved drug lawful.
- **Two load-bearing agents fail it and are now excluded:** (a) **oral cytarabine ocfosfate (Starasid) is approved only in Japan** -> no extra-label route in the US; it carried the B-cell brain closure in section I and appeared in every program from section F. (b) **No licensed canine anti-CD20 antibody exists** (Blontress licensed 2015, **discontinued 2017**; Elanco 1E4 investigational); it carried the B-cell body closure (day 74).
- **Rebuilt from lawful agents only, all four cases still close:** body (B and T) with **verdinexor sustained 168 d**, which is **on-label** for Laverdia-CA1 (FDA conditional Jan 2021, **full approval Jan 2026**; label is twice weekly, >=72 h apart, until progression); brain (B and T) with one **23.4 Gy** course + **repeated intrathecal methotrexate** for **420 d (B) / 378 d (T)** at the median canine line (820/799 d most resistant, 231 d most sensitive, 1,283 d with no radiation).
- **Methotrexate is indispensable and best-supported legally:** radiation without it never clears either brain at any window to 15 years; preservative-free methotrexate is FDA-approved **with intrathecal a labelled human route**, and intrathecal methotrexate + cytarabine is published in 112 dogs (PMID 25041580).
- **Not load-bearing (checked):** romidepsin (its PTCL indication was withdrawn 2021-22 but the drug remains approved for CTCL, so still ELU-eligible) and hydroxychloroquine.
- **Still weak, being worked:** methotrexate kill 0.12/day is DERIVED from a secondary-citation IC50; intrathecal drug reaches CSF/perivascular space, not deep parenchyma; **late neurotoxicity of whole-brain radiation + repeated intrathecal methotrexate** (29% leukoencephalopathy at 2 y in humans, HR 4.5, PMID 39269476) is not in the budget and has no canine series; repeated intrathecal dosing in a dog beyond ~6 doses has no precedent while the programs need 20-30; radiation e-folds on dormant cells are transferred; a DLA-identical littermate is required.
- **Not checked:** the EU/UK cascade (its import limb might permit ocfosfate there), DEA scheduling, state practice acts, cytotoxic handling rules, compounding from bulk substances (FDA GFI #256).
