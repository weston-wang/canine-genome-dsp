# Model re-run: brain closure at the measured selinexor CSF level (2026-10-31)

Source of the new input: `verification_selinexor_csf_and_leah.md` (primary abstract text, Blood 2025;146(Suppl 1):3550,
DOI 10.1182/blood-2025-3550, MSZ trial, 21 patients): selinexor CSF 0.919 ng/mL at plasma 204.67 ng/mL (4 h after 40 mg),
"stable CSF-to-plasma ratio (~0.6%)" from 4 to 25 h. With 95% plasma protein binding (FDA Xpovio label), CSF / unbound
plasma = 0.919 / 10.2 = **0.09**.

Why it is the right number to use (project rule 14): CSF is the standard measurable proxy for unbound drug in brain
interstitial fluid. The value the closure used, verdinexor brain access 0.30, was chosen as "below the 0.60-0.72" rodent and
monkey TOTAL brain:plasma ratio (PMID 27323910), which counts drug bound to brain tissue and is not an unbound ratio. A
measurement in the compartment at issue outranks a flattering inference, even when it is worse. Caveats: selinexor, not
verdinexor (same chemical series, sister compound); CSF, not brain parenchyma; a conference abstract that does not say how
many patients were sampled; 0.919/204.67 is 0.45%, not the abstract's 0.6% (0.09 uses the stated numbers).

Model: `lymphoma_sustained` lawful programs (verdinexor + the lawful agents + one 23.4 Gy course + repeated intrathecal
methotrexate), lineage-matched radiation e-folds (B median line 1771, T line OSW), methotrexate kill from
`it_mtx_derived_kill(interval, ic50)` (measured canine CSF volume and half-life). Window = smallest sustained period that
clears the CNS compartment; "never" = not inside 15 years. Script: scratchpad `selx.py` (reproduced in the test added to
`tests/test_lymphoma_universe.py`).

## Result 1: the reported schedule depended on the 0.30 figure

| schedule | verdinexor brain access | B-cell brain | T-cell brain |
|---|---|---|---|
| every 21 d, pessimistic IC50 118 nM (the reported program) | 0.30 (old) | 420 d = 20 doses | 241 d = 11 doses |
| same | **0.09 (measured)** | **never** | **never** |
| same | 0.0 | never | never |

So the claim "two independent routes, either of which suffices" did not hold for the reported every-3-weeks schedule: at the
pessimistic IC50 that schedule gives a methotrexate kill of 0.044/day, below the half-strength 0.06 at which the redundancy
test was run, so it needed BOTH inputs.

## Result 2: both brains still close at the measured level, with more frequent methotrexate

| IC50 | interval | access 0.09: B-cell brain | access 0.09: T-cell brain | access 0: B | access 0: T |
|---|---|---|---|---|---|
| 118 nM (pessimistic) | 7 d | 378 d = 54 doses | 231 d = 33 doses | 409 d = 58 | 231 d = 33 |
| 118 nM | 10 d | 451 d = 45 doses | **241 d = 24 doses** | 3,610 d | 241 d = 24 |
| 118 nM | 14 d | never | never | never | never |
| 14 nM (human T-ALL anchor) | 10 d | 388 d = 39 doses | 231 d = 23 doses | 430 d = 43 | 231 d = 23 |
| 14 nM | 14 d | **483 d = 34 doses** | **241 d = 17 doses** | never | 241 d = 17 |
| 2.5 nM (canine, secondary citation) | 14 d | 409 d = 29 doses | 231 d = 16 doses | 567 d = 40 | 241 d = 17 |

Canine precedent for repeated intrathecal dosing: subcutaneous CSF ports dosed every other week for 8-11 months, 20-28 doses
(already in the record, `LYMPHOMA_UNIVERSE.md` K.6).

- **T-cell brain: still closes inside canine precedent** at every IC50: 24 doses every 10 days at the pessimistic IC50,
  17 doses every 14 days at the central one. Verdinexor's brain reach no longer matters for it (same window at access 0).
- **B-cell brain: still closes in the model, but now needs more intrathecal doses than any dog on record has received**:
  29-34 doses every 14 days (central to favourable IC50) or 45 every 10 days (pessimistic IC50), against 20-28 in canine
  series. Verdinexor at 0.09 still contributes (at access 0 the central-IC50 14-day schedule never clears).
- The brain closure is no longer redundant: it rests on the intrathecal methotrexate reaching the CSF compartment.
- New load-bearing input for the B-cell brain: tolerability of ~30-45 intrathecal doses over 13-16 months in a dog. No canine
  source; human precedent (TT16: 13-27 doses per child; long-course intraventricular therapy via Ommaya reservoirs in
  leptomeningeal disease) not yet searched for this question.
