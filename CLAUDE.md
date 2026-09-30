# Working agreements for canine-genome-dsp

These exist because of specific failures, not as generic advice. Read this file first, every session.

## What went wrong (so the rules below have a reason)

1. **Re-raising settled work as a new gap.** Asked "did we cover everything?", I listed gaps that were
   already in our reports or in my own earlier answers, without checking. The user had to point it out.
2. **Grading against a bar the user never set.** The user's standard is "closed by real data **or a
   rigorous model**." I graded against "demonstrated in dogs," which they never asked for and explicitly
   said they already know is unmet.
3. **Replicating half of a referenced method and calling it the method.** Told to "do what the HSA branch
   did," I ported its object model and dropped its potency derivation (`pkpd.py`), its toxicity
   constraints (`core/toxicity.py`, `core/tolerable_search.py`) and its provenance rules
   (`core/evidence.py`), even though my own plan listed PK/PD-derived kill rates as a key part.
4. **Overstating closure.** "Every escape is closed" was said when the accurate claim was "the model
   contains an agent that covers it."

## Rules

- **Search the record before answering any "did we cover X / what's missing / did we already discuss Y"
  question.** The record is: the session transcript (`/root/.claude/projects/*/*.jsonl`), `docs/`, `git log
  --all`, and the reference branch. For every item, say **already covered (where)** or **not covered**.
  Only items that survive that check may be presented as gaps. Never write "supposedly" or guess at what
  was discussed; check.
- **Use the user's stated success criteria verbatim.** At the start of a task, restate the user's own
  words (see "Standing standards" below) and grade against exactly those. Do not substitute a stricter or
  looser bar of my own.
- **When told to replicate a method or branch, inventory every component first.** List each module as
  ported, adapted, or deliberately skipped with a reason, and get the user's agreement to any skip. Do
  not describe a partial port as the method.
- **Do not present a settled conclusion as news.** Anything listed under "Settled" below is referenced,
  not re-derived or re-raised.
- **Claim what was shown, not what was intended.** Separate "the model has an agent covering this" from
  "this is supported by real data" from "this is assumed," in that vocabulary.
- **When a user corrects a lapse, add it here in the same session**, so it persists.

## Standing standards (the user's words)

- "make sure every mechanism and every escape is closed by either real data or rigorous model, potency,
  toxicity etc all need to be considered"
- "looking for 10+ years of durability"; and whether 2+ years disease-free is a reasonable inference for 10+
- "assuming early detection"
- Reports "in layman's terms"
- "I'm not asking if it's been demonstrated, I know it's not."
- Method reference: the HSA branch `origin/claude/canine-hs-analysis-graft` ("how we went and found all
  possible mechanisms and routes of escapes, then searched and found combined approaches for closing each").

## Settled (do not re-raise as new; see the doc)

All in `docs/LYMPHOMA_DURABLE_RESPONSE.md` unless noted.
- The bar (~0.090/day, set by P-glycoprotein efflux; chemo moves it ~2%), §1.
- Immunotherapy threshold at the bar, and CD20 antigen loss behaviour, §2-3.
- Lower-the-bar, tandem CD19/CD20, and "a one-time consolidation is not persistence" (in the model), §4.
- CNS sanctuary and the `sanctuary_penetration_multiplier` engine upgrade, §5.
- 2-year to 10-year inference: mechanism-dependent; ~3% late drug-resistant tail at the bar, §7.
- Toxicity ledger and chemo de-rating findings, §8; completeness ledger and its two flagged exceptions
  (apoptosis evasion partly covered; late tail managed not eliminated), §9.
- Combination search (derived coverage, three filters, early detection removes rare mutational escapes but
  not phenotypic ones), §10. **CNS T-cell does not close with anything obtainable** (short 1.16x on the
  persister; a T-lineage cellular effector that traffics into the CNS is the missing object).
- Second cancers / therapy-related neoplasia are noted as a limit that cuts against long-term durability, §7.

## Known gaps versus the HSA method (factual, not yet fixed)

- Lymphoma catalogue potencies are hand-set and labelled ASSUMED (only venetoclax's B/T EC50 split is
  measured). `pkpd.py` (kill from measured IC50 x canine exposure) was not ported.
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
- The model treats immune exhaustion as defeating every immune agent, so an armored CAR-T cannot earn credit
  for resisting it.
- Other sanctuaries (eyes, testes), non-DLBCL subtypes and breed effects were raised once by me and never
  discussed with the user; treat as unscoped, not as agreed gaps.
