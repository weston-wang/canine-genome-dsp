# Working agreements for canine-genome-dsp

**This file is byte-identical on every branch, on purpose.** That keeps merges conflict-free and means a
thread on any branch reads the same rules. Branch-specific state goes in `docs/*_STATUS.md`, not here.
If you change this file, apply the same change to every branch listed under "Where things live".

## Why this exists

The user has flagged the same failure repeatedly, across threads and branches: context that was already
settled gets dropped or re-litigated. Each thread starts with no memory of any other thread. Only two
things cross threads: files in git, and account or environment settings. So state must live in git.

Concrete failures (so the rules have a reason):
1. **Re-raising settled work as a new gap.** Asked "did we cover everything?", gaps were listed that were
   already in the reports or in earlier answers, without checking.
2. **Grading against a bar the user never set.** The user's bar is "real data **or a rigorous model**."
   It was graded against "demonstrated in dogs," which the user said they already know is unmet.
3. **Replicating half of a referenced method and calling it the method.** Told to "do what the HSA
   branch did," only its object model was ported; its potency derivation (`pkpd.py`), toxicity budgets
   (`core/toxicity.py`, `core/tolerable_search.py`) and provenance rules (`core/evidence.py`) were dropped.
4. **Overstating closure.** "Every escape is closed" was said when the accurate claim was "the model
   contains an agent that covers it."

## Rules

1. **Search the record before answering any "what did we cover / what's missing / did we discuss X"
   question.** The record is: this file; `docs/`; `git log --all`; **other branches** via
   `git fetch origin` then `git show origin/<branch>:<path>`; and this session's transcript
   (`/root/.claude/projects/*/*.jsonl`, which covers only the current session). Label every item
   "already covered (where)" or "not covered". Only items that survive that check may be presented as
   gaps. Never write "supposedly" or guess at what was discussed; check.
2. **Quote the user's success criteria verbatim at the start of a task and grade against exactly
   those.** Do not substitute a stricter or looser bar. If the user says they already know something is
   unmet, do not report it back as a finding.
3. **When told to replicate a method, branch or approach, inventory every component of the reference
   first.** List each as ported, adapted, or skipped with a reason, and get agreement to any skip. Never
   call a partial port the method.
4. **Do not present a settled conclusion as news.** Check the `docs/*_STATUS.md` files first.
5. **Report results at the strength shown.** Keep "the model has an agent covering this" separate from
   "real data supports this" and from "assumed".
6. **A new or reset session rebuilds context before acting.** Read this file and the relevant
   `docs/*_STATUS.md`, run `git fetch origin`, and compare with `git log HEAD..origin/<branch>`. A fresh
   container can hold a stale checkout (this has happened: a local branch reset to `main`, hiding all
   the work on the remote branch).
7. **Record state in git before finishing.** When the user states a standard or a decision, or a
   meaningful result is reached, write it into this file (standards) or a `docs/*_STATUS.md` (settled
   results and known gaps), commit and push. The next thread cannot see this one.
8. **When the user corrects a lapse, add the lesson here in the same session** and propagate it to every
   branch.

## Standing standards for the cancer durable-response work (the user's words)

- "make sure every mechanism and every escape is closed by either real data or rigorous model, potency,
  toxicity etc all need to be considered"
- "looking for 10+ years of durability"; and whether 2+ years disease-free is a reasonable inference
  for 10+
- "assuming early detection"
- Reports "in layman's terms"
- "I'm not asking if it's been demonstrated, I know it's not."
- "I'm okay with no specific data but if scientifically sound" (2026-09-30). So a potency, exposure or
  access figure transferred from another species, disease or a class-level mechanism is acceptable **if the
  transfer is justified in writing** and the number is graded TRANSFERRED (never MEASURED). A number with no
  basis at all stays ASSUMED and does not count as closure. Do not tune any input to force a closure.
- Method reference: "Look at how we went and found all possible mechanisms and routes of escapes, then
  searched and found combined approaches for closing each" -- the user calls this "the HSA branch";
  its content is histiocytic sarcoma (see terminology).

## Where things live

Verify with `git branch -a`; this list can drift.

| branch | what it holds |
|---|---|
| `main` | base DSP engine, melanoma and osteosarcoma benchmarks. No durable-response work. |
| `claude/canine-hs-analysis-graft` (PR #3) | **Histiocytic sarcoma** pipeline. `src/canine_dsp/core/` (regimen object model, catalogue, combination search, `tolerable_search`, `toxicity`, `evidence`), `pkpd.py`, `docs/THERAPY_STRATEGY.md`, `docs/CONSOLIDATED_REPORT.md`, `docs/PRIOR_ART_COMBINATIONS.md`. **The method reference.** |
| `claude/codex-branch-audit-clfeiz` (PR #5 open; the earlier PR #2 is closed) | **Hemangiosarcoma** durable-response analysis: `docs/HSA_DURABLE_RESPONSE.md` and the `hsa_*` modules. |
| `claude/duplicate-codex-prefix-branch-lt1qh6` (PR #4) | The codex branch as of `66cfa76`, merged with `main`, plus the **lymphoma** work: `docs/LYMPHOMA_DURABLE_RESPONSE.md`, `docs/LYMPHOMA_PLAIN_LANGUAGE.html`, `docs/LYMPHOMA_STATUS.md`, `src/canine_dsp/lymphoma_*.py`, `src/canine_dsp/core/lymphoma_*.py`. |

Read the lymphoma state without switching branches:
`git show origin/claude/duplicate-codex-prefix-branch-lt1qh6:docs/LYMPHOMA_STATUS.md`

## Terminology

- **HS** = histiocytic sarcoma (branch `claude/canine-hs-analysis-graft`).
- **HSA** = hemangiosarcoma (branch `claude/codex-branch-audit-clfeiz`).
- The user has referred to the HS branch as "the HSA branch". If the difference matters to the task,
  confirm which is meant before building on it.
