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
5. **Declaring a search complete over a candidate list that was never enumerated.** The lymphoma
   closing-combination was reported as "found" when the catalogue had no vaccine and no separate
   stem-cell/transplant mechanism, and the user had to point that out ("even I know vaccine should be part of
   the equation, and maybe even stem cell. Go back and be thorough"). A result is only as complete as the
   candidate universe it searched.
6. **Scoping a finding to the wrong case, and calling settled findings new.** The HS case is primary
   intracranial (non-disseminated) disease, but a disseminated-HS paper was headlined as the key finding
   (the user: "I thought we were focused on the non-dessimated case"). In the same report, items labelled
   new were already in `docs/CONSOLIDATED_REPORT.md`; the record had been searched by keyword, and the
   report cites them by DOI.
7. **Listing "unmeasured in the dog" as the open gaps, after the user ruled that bar out.** A
   gap-closure summary ended with "what remains open": no canine MTAP measurement, no canine CNS
   access, no canine ctDNA validation, unmeasured fluid-to-cell fraction. Every one of those has a
   written transfer or a derivation behind it, so under the stated bar none is a gap — the user had
   said, twice, that absence of demonstration is not the test ("I'm not asking if it's been
   demonstrated, I know it's not"; "I'm okay with no specific data but if scientifically sound").
   The genuinely failing input, a growth-rate bar that was a bare uncited literal gating every
   margin in the project, was buried in the same list as the non-gaps. `standard_audit.py` now
   grades every live input against the stated bar and names what actually fails.

8. **Dismissing candidate classes for lacking canine data, and building the answer on agents that do not exist.**
   The lymphoma closing programs rested on a CAR-T for dogs, a spinal-fluid CAR-T and a spinal pump, all "to build",
   while vaccines, bispecific T-cell engagers / armed T cells, inhibitors and stem-cell transplant were set aside as
   "no canine kill rate" or "cannot be modelled". The user: "I needed scientifically sound, not totally theoretical. And I
   think you are dismissing vaccines, ebats, inhibitors, stem cells too easily." Under the stated bar a human-data transfer
   or an outcome calibration is a sound input, so absence of canine data is not a reason to exclude a class.

9. **Stopping the search at a conceptual label instead of its measurable proxy.** The HS analysis reported the
   invading edge as unreachable by any obtainable drug and stopped there, concluding "the biology closes, the
   pharmacy doesn't". The quantity was in fact measured, in two human trials, under a different name: "access
   behind an intact barrier" is "drug concentration in gadolinium-NON-ENHANCING tumour", because non-enhancement
   is what an intact barrier means. Searching the concept found nothing; searching the proxy found a LICENSED drug
   (ribociclib) with 65-634 nM unbound in that compartment against a 40 nM target, in patients enrolled on this
   tumour's own lesion, with the pharmacodynamics confirmed in the same tissue. The site had been "open" only
   because it was being inferred from rodent ratios instead of looked up.

10. **Re-raising the increment as an open gap for the third time, with the function that forbids it sitting
   unrun in the repo.** Asked whether the ten-year goal was covered, the answer listed "the vaccine has to be
   ~1.4x stronger than any real trial has produced, and what the four levers add together has never been
   measured" as one of three failing items. That item is graded **PASSES / TRANSFERRED** in
   `hsa_standard_audit.wrongly_reported_as_gaps()`, whose stored reason already says "This analysis listed it as
   an open gap as recently as this session; under rule 11 that was grading against demonstration." The stacking
   half was also already tested and closed (`DOES_THE_PLAN_DEPEND_ON_THE_LEVERS_STACKING`, grade TRANSFERRED:
   winner-takes-all needs 25% transfer against 10% for full addition, both inside what the anchors support --
   "the plan does NOT depend on the four levers stacking"). The user: *"I don't mind 1 and 3 being open but 2 is
   something we went over and over again."* The machinery to prevent this existed and was not executed; writing
   the guard is not running the guard.

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
9. **Before any "closed / found / complete" claim, enumerate the candidate universe and record it.** List every
   modality class that could plausibly matter (for cancer work at least: cytotoxics, targeted drugs,
   antibodies and ADCs, bispecifics, cell therapies, stem-cell and marrow transplant, vaccines and other active
   immunotherapy, checkpoint and cytokine agents, radiation, sanctuary-site delivery), from the literature,
   not from memory. For each, record in git whether it is in the model, evaluated and excluded with a reason,
   or not yet assessed. State the claim as "closed within this catalogue of N agents and M escapes", and list
   what is outside it. Do the same for the escape list (independent audit, not the list already in hand).
10. **State the case under analysis and scope every finding to it.** For HS that is primary intracranial
   (non-disseminated) histiocytic sarcoma in a predisposed breed. Label evidence from another presentation
   (disseminated disease, another tumour, another species) as indirect. When checking whether a finding is
   already in the record, search by its DOI or PMID as well as by keyword.
11. **Never report "no measurement exists" as an open gap. Run the audit functions before answering, and
   quote them.** Any question of the form "is it covered / what is still open / is the goal met" is answered by
   executing `standard_audit.failing()` **and** `standard_audit.wrongly_reported_as_gaps()` first, and the answer
   lists exactly what `failing()` returns. An item appearing in `wrongly_reported_as_gaps()` may not be presented
   as open under any phrasing -- including softened ones like "has never been measured in this tumour", "rests on
   an unmeasured combination", or "is a requirement derived from the model rather than an effect size from data".
   Those are re-grades against demonstration wearing different words. If a graded-PASSES item seems open, the
   move is to say which code path would have to change and why, not to re-list it.
   The bar is real data **or** a rigorous
   model, with a cross-species/disease/class transfer acceptable when justified in writing. So before
   calling anything open, ask: does a written transfer or a derivation stand behind this number? If
   yes it is CLOSED (graded TRANSFERRED or DERIVED) and saying otherwise re-grades against a bar the
   user disclaimed. Only two things are genuinely open: a number with **no** basis at all, and a
   number whose basis is circular, tuned, or contradicted. Run `standard_audit.failing()` rather than
   listing absences. A number that exists but is never used to assert a closure (an inert
   placeholder) is also not a gap — say which code path uses it.

12. **Report closure as a decidable conjunction, never as odds.** The user: *"I don't want odds of
   achieving 10 years, the whole point about looking at all mechanisms and escapes is to not leave
   it to odds."* A probability is the right output only when failure modes are unenumerated;
   enumerating them is what makes the question decidable. So the headline is
   `deterministic_closure.conjunction()` — every route CLOSED or OPEN at each site, plus the finite
   list of conditions and each one's status. `emergence.py`'s P(10-year) is a SENSITIVITY statement
   and must never be quoted as the verdict (`deterministic_closure.emergence_is_secondary()` says
   why: it charges a reroute as terminal although the ledger names a successor for every reroute,
   and it converts "every route open, margin −0.049/day" into a number that reads like a good bet).

13. **A closure program is built from agents that exist, and a class may be excluded only for a stated scientific
   reason.** Tier every agent as exists-today (licensed, off-label, or in dog trials) or to-build. Search for the program
   from exists-today agents first; a program that needs a to-build agent is reported separately and as such. A class (vaccine,
   engager, inhibitor, transplant, cell therapy) is excluded only because its kill is contradicted, it is defeated by a
   named escape, or its toxicity cannot be afforded, never because canine data are absent; when canine data are absent,
   derive a graded TRANSFER or OUTCOME-calibrated input and test with it.
   **Near-future agents count.** The user (2026-10-02): "I don't mean you can only use therapies that exist today, I meant to
   include near future ones that are scientifically sound. Just nothing that's pure theoretical." So the tiers are:
   exists-today, NEAR-FUTURE (clinical-stage evidence of the modality in humans or dogs, a stated path to the dog, a derived or
   transferred dose/kill) and THEORETICAL (no clinical evidence of the mechanism anywhere). Closure may use the first two; a
   program is reported with its tier mix; a theoretical agent never counts. Do not retreat to "only what exists today".

14. **Before calling a quantity unmeasured, name its measurable proxy and search for THAT.** A compartment, an
   access figure or a mechanism usually has an operational definition that someone has already assayed under a
   different name -- "behind an intact barrier" is "Gd-non-enhancing tumour"; "reaches the cell" is a resected-tissue
   concentration; "engages the target" is a phosphorylation or Ki-67 readout. Write the proxy down, search it, and
   prefer a MEASUREMENT IN THE COMPARTMENT AT ISSUE over any inference into it -- a rodent Kp, a generic
   compartment access, or a concentration from a site where the barrier is already broken. Two consequences:
   a measured value in the right compartment outranks a more flattering inferred one (use the agent's own numbers
   even when they are worse), and a trial that reports a NEGATIVE for one arm (everolimus undetectable) is
   evidence about that arm, not a missing number.

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
