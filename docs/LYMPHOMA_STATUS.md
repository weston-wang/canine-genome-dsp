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
| `pkpd.py` `emax_kill_rate`, `free concentration`, `margin`, `DrugPKPD`, `min_access_to_close` | kill rate derived from measured IC50 x exposure; can report "does not close" | **To port** (this rebuild) |
| `pkpd.py` trametinib target-attainment / dose-for-attainment / dosing workaround | population-PK spread for one HS drug | **Skipped**: built on one HS drug's Phase I; no lymphoma equivalent input. Revisit if a canine PK spread is found for a lymphoma agent |
| `core/evidence.py` | `Measurement` that refuses to be read for another population; `transfer_to()` | **To port** (this rebuild), with lymphoma `Disease` members added |
| `core/toxicity.py` | organ-axis budgets; same-axis adds; de-rating not free; `profile_for` raises rather than failing open; efflux co-dose multiplier | **To port** (this rebuild) |
| `core/tolerable_search.py` | search under organ budgets; efflux co-dose charged on partner's axis | **To port** (this rebuild) |
| `core/dormancy.py` | persister is a duty-cycle problem, not a wall for division-gated agents | **To adapt** (this rebuild). **Not raised earlier in this project.** It changes the lymphoma "persister filter". Its `kill_from` multiplies by duty twice (`effective_kill` already contains duty); do not copy that |
| `core/response_duration.py`, `core/treatment_horizon.py` | time to clear = ln(N0)/margin; treatment clock vs cumulative toxicity; "cure" only if cleared inside the tolerable window | **To adapt** (this rebuild). Bears directly on 10+ year durability |
| `core/schedule_coherence.py` | access and duty must come from one dosing schedule | **To adapt** as a per-agent check (CAR-T persistence, IT cytarabine, TBI, HD-MTX) |
| `core/delivery.py` | delivery routes as composable objects (FUS, CED, IT, efflux inhibition) | **Partly covered**: lymphoma CNS routes are already agents with per-compartment access. FUS/CED **skipped** (not evaluated for lymphoma; flagged) |
| `core/hs_drug_sensitivity.py` | IC50 measured in the actual disease, outranks assumed potency | **To adapt** as canine-lymphoma sensitivity inputs (PMID 25715778 includes canine lymphoma lines) |
| `sequence_conservation.py` | human-vs-dog target identity for transferred drugs | **Skipped for now**: lymphoma agents that are human-designed (acalabrutinib, venetoclax) have canine in-vivo or in-vitro measurements. Flagged: revisit for any agent whose potency ends up TRANSFERRED |
| `docs/PRIOR_ART_COMBINATIONS.md` | has each proposed combination been tried, in what species | **Not covered here yet.** To do for the combinations that survive the search |
| `docs/THERAPY_STRATEGY.md` coverage-by-evidence-tier table | escape x closing agent x evidence grade | **To adapt** as the lymphoma coverage ledger (this is the direct answer to the coverage question) |
| `core/durable_regimen.py`, `cycled_regimen.py`, `breed_wide_durability.py`, `genotype_tiered_durability.py`, `microtubule_route.py`, `brain_*.py`, `intraarterial_route.py`, `metronomic_bbb_check.py`, `mgmt_escape.py`, `presentation.py` | HS-specific: brain tumour, MTAP/breed, intra-arterial route, MGMT | **Skipped**: no lymphoma analogue (different organ, driver and route). The P-gp escape already plays the MGMT role |
| `docs/CONSOLIDATED_REPORT.md`, `plain_language_report.html`, `researcher_brief.html`, `preprint/` | HS write-ups | **Skipped** as outputs; the lymphoma layman report exists and is updated only if conclusions change |

## Known gaps versus the histiocytic-sarcoma method (factual, not yet fixed)

- Catalogue potencies are hand-set and labelled ASSUMED (only venetoclax's B/T EC50 split is measured).
  `pkpd.py` (kill from measured IC50 x canine exposure) was not ported.
- Toxicity in the search is a crude `duty` factor plus prose. Organ-axis budgets (`core/toxicity.py`) and
  the toxicity-aware search (`core/tolerable_search.py`) were not ported, so the "robust" multi-agent
  regimens were never checked for organ oversubscription. The P-gp chemosensitiser's raised normal-tissue
  exposure is written in prose and never charged.
- `core/evidence.py` provenance enforcement was not ported; evidence is free-text labels.
- Found after the reports and not yet in the catalogue: half-body radiation (real multi-year remissions),
  verdinexor (fully approved 2026), T-cell kinase inhibitors, the dog anti-CD20 antibody 1E4-cIgGB, canine
  IL-15, the PD-1/CD28 switch receptor (armored canine CAR-T, lab only). Immune rejection of mouse-derived
  CAR binders is not modelled.
- Model conflict: real half-body radiation and transplant data show multi-year remissions, but the model
  says a one-time consolidation adds no durability. Hypothesis (untested): the model treats leftover
  resistant cells as a continuous quantity that can never reach zero, while real tumours are countable.
- The model treats immune exhaustion as defeating every immune agent, so an armored CAR-T cannot earn
  credit for resisting it.
- Other sanctuaries (eyes, testes), non-DLBCL subtypes and breed effects were raised once by an assistant
  and never discussed with the user; treat as unscoped, not as agreed gaps.
- Proposed, awaiting the user's go-ahead: rebuild the catalogue on the potency and toxicity modules and
  re-run the search under organ budgets.

## Branch drift

`claude/codex-branch-audit-clfeiz` has moved since this branch duplicated it at `66cfa76`; its tip is now
`5656f74` (2026-09-08, "Record the three published HSA reports in the narrative document"). This branch has
not picked those commits up.
