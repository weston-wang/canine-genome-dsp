# Lymphoma: the combination that closes every modelled escape

**Goal, in the user's words:** "We started with a goal of finding combo therapy that closes every
possibility. Go find it." Standard: "make sure every mechanism and every escape is closed by either real
data or rigorous model, potency, toxicity etc all need to be considered", "looking for 10+ years of
durability", "assuming early detection". Evidence bar (user): "I'm okay with no specific data but if
scientifically sound" -- so transferred, justified inputs count (grade TRANSFER); bare assumptions do not,
and no input was tuned to force closure.

**Strength of every claim below: MODELLED.** Nothing here has been shown in a dog. The user has said they
know that ("I'm not asking if it's been demonstrated, I know it's not.").

Method: the HS-branch machinery, rebuilt (see `LYMPHOMA_STATUS.md` inventory): derived potency,
organ-axis toxicity budgets, treatment clock, two-state dormancy, fault-tolerance tests. Reproduce with
`program_report(label)` in `src/canine_dsp/lymphoma_coverage_ledger.py`; the search is
`core/lymphoma_grounded.search` restricted to sound grades.

## The programs found (body and brain given together)

| program | body: margin, cleared by | brain: cleared by, capacity | potency halved | any one agent removed |
|---|---|---|---|---|
| **B-cell**: hydroxychloroquine + verdinexor + continuous intrathecal cytarabine + anti-CD20 antibody | +0.284/day, day 34 | day 15, 1e8 cells | **clears** (body and brain) | fails (every agent load-bearing) |
| B-cell without the trial-stage antibody | +0.185/day, day 41 | day 15, 1e8 | body **fails**, brain clears | fails |
| T-cell, existing drugs: hydroxychloroquine + verdinexor + venetoclax + pump | +0.064/day, day 39 | day 47, 1e8 | **fails** (body and brain) | fails |
| T-cell with CD7 CAR-T: hydroxychloroquine + verdinexor + pump + CD7 CAR-T | +0.184/day, day 41 | day 40, 1e8 | body clears, brain **fails** | fails |

"Closes" = every escape in the model (all 14, lineage-appropriate) has a positive net kill after toxicity
de-rating, and the treatment clock reaches zero surviving cells inside the evidence-limited window, at
early-detection burden. At clinically-obvious burden (1e11 cells): B-cell programs clear (day 46 / 57);
T-cell CD7 program clears (day 57); the T-cell existing-drug program does **not** (response then
relapse from P-gp efflux after day 56).

Union organ loads (all within budget): B-cell with antibody marrow 0.2, GI 0.7, ocular 0.3, hepatic 0.2,
CNS-local 0.6, immune-mediated 0.3. T-cell CD7: marrow 0.6, GI 0.7, immune-mediated 0.5.

## What each program stands on (evidence grade of each part)

| part | grade | basis |
|---|---|---|
| verdinexor | DERIVED | canine-cell potency from pkpd; **known mismatch**: derived vs clinical response |
| hydroxychloroquine | TRANSFER | human/cell IC50 transferred; **P-gp substrate**, so it is not independent of the efflux escape; CNS access 0.3 is ASSUMED |
| continuous intrathecal cytarabine | TRANSFER | canine CSF cytarabine PK (PMID 1742843) + derived cytarabine kill; **the pump is buildable, not existing**; chronic pump toxicity unknown |
| anti-CD20 | MEASURED | depletion rates; canine product is trial-stage |
| CD7 CAR-T | TRANSFER-OUTCOME | buildable (canine binder, fratricide-resistant) |
| venetoclax | PARTIAL | |
| radiotherapy (in the search) | DERIVED | LQ model from measured SF2/SF5; lower than the old assumed 0.30 |

## Caveats (not to be smoothed over)

1. Results depend on the **transferred HCQ potency** and the assumed HCQ CNS access. Brain capacity falls
   with lower access (B-cell no-antibody: 7.5e7 at 0.1, 1.4e7 at 0.03; still large vs. seeded cell count).
2. **Every agent is load-bearing**: removing any one agent in any program breaks closure. That is the
   opposite of fault-tolerant redundancy and is the main weakness.
3. **T-cell brain is sensitive to the pump setpoint**: existing-drug T program capacity collapses at
   1.0 uM (4.4e4) and 0.3 uM (0); CD7 program collapses at 0.3 uM (4.0e4).
4. Clock is mean-field; MRD data suggest clearing to zero cells is optimistic. Seeding rates are assumed.
5. "10+ years": nothing in the model shows a 2-year disease-free interval implies 10 years; the model
   claims only that the modelled persister and escape pools are eliminated inside the window.
6. Buildable items (pump, CD7 CAR-T, canine anti-CD20) do not exist as approved products.

## What this does not claim
It does not claim cure in dogs, that model toxicity equals real toxicity, or that unmodelled mechanisms
(none identified beyond the 14 listed; see the ledger) do not exist.
