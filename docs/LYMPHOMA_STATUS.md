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
