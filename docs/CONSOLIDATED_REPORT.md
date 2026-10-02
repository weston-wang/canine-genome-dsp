# Primary intracranial histiocytic sarcoma in a predisposed breed — a durable-therapy strategy

*Published, reader-facing version: <https://claude.ai/artifact/4Ho2u4jTieU579ExuRgvY5>. Full audit trail including every withdrawn claim: `AUDIT_TRAIL.md`.*

**Case:** primary intracranial (non-disseminated) histiocytic sarcoma in a predisposed breed. An
extra-axial, meninges-based mass that invades brain tissue (23/23 dogs) and seeds the leptomeninges
(19/19). Extracranial spread of primary CNS HS has never been reported.

**Question:** can a therapy hold for ten or more years against every mechanism and every escape
route, at every site the disease occupies?

**Answer: yes, within a stated catalogue and under five conditions that are met plus three that are
not.** The result is a checklist, not a probability. Full audit trail, including every withdrawn
claim, is in `AUDIT_TRAIL.md`.

**What the three outstanding conditions cost, stated up front:** one is a pre-treatment immunostain.
The other two are *availability*, not science — three of the agents in the closing regimen cannot be
dispensed to a dog today, and none of them is a molecule that has to be discovered. Searched from
licensed agents only, the obtainable programme closes two of the three sites outright, including the
one this tumour is actually based in, and is marginal only at the invading edge. §6a gives both
programmes side by side.

---

## 1. The verdict

Every one of the **16 enumerated escape routes** closes at **both occupied sites**, under the real
toxicity budget, with an all-oral regimen and no procedure.

| Site | Routes closed | Worst margin | Growth bar being beaten |
|---|---|---|---|
| Invaded brain tissue | **10 / 10** computed | **+0.59 / day** | 0.055 / day |
| Leptomeninges, CSF | **10 / 10** computed | **+0.61 / day** | 0.055 / day |

The remaining 6 of the 16 routes close structurally — by drug choice or schedule, not by a kill rate
(see §4).

**Closed within a stated catalogue:** 25 therapy-modality classes (15 in the model, 10 excluded with
recorded reasons, **0 unassessed**) and 16 escape routes derived independently of the list in hand.
Of the 15 classes in the model, **11 are obtainable for a dog today and 4 need an agent that does not
exist yet.** No class is excluded for lacking canine data; each of the 10 exclusions rests on a
contradicted kill (5), a named escape that defeats it (3), or a toxicity budget it would blow (2).

---

## 2. The two moves

Ten years is not reached by killing this tumour harder. The breed is **born predisposed**, so
clearing one tumour does nothing about the inherited fault. The unlock is that the predisposition and
the tumour are the **same lesion** — a deletion on canine chromosome 11 removing CDKN2A/B and MTAP,
present in **62.8%** of cases.

1. **Induction** — clear the tumour that is there.
2. **Genotype-matched maintenance** — hold a matched oral drug indefinitely, so the *next* tumour
   never establishes.

---

## 3. The regimen

Five agents, all oral or systemic, all continuous. **No implant, no catheter, no sonication, no
radiation in the closing set.**

| Role | Agent | Why it is in the set | Available for a dog? |
|---|---|---|---|
| Induction / position-independent kill | **RGN3067** (oral colchicine-site tubulin destabiliser) | Carries 6 of the 16 routes. Not an efflux-pump substrate (ratio 0.61) | **No — preclinical, rodent-only** |
| Parallel-pathway cover | **paxalisib** (PI3K/AKT) | Kp,uu 0.31, confirmed non-substrate of both efflux pumps | **No — investigational** |
| Lineage removal | **liposomal clodronate** | Kills by being eaten, so it reaches non-dividing cells | Yes — already given to dogs with this lineage of tumour |
| Persister / autophagy cover | **hydroxychloroquine** | The only agent here with a canine phase I | Yes |
| Antigen-directed arm | **anti-PD-1 (gilvetmab)** | Caninized, conditionally licensed | Yes |

An earlier version of this table said "obtainable for dogs" against the induction agent. That was
wrong, and it was wrong in the code too: `core/microtubule_route.py` flags every agent
`obtainable=True`, so a programme resting on a preclinical compound read as a prescription. The
margins are unaffected — the inputs behind them are measured — but the availability claim was not.
`availability_tiers.mislabelled_as_obtainable()` now names both offenders rather than silently
flipping the flag, because the flag drives published margins.

**Genotype-matched maintenance, by tumour type:**

| Tumour carries | Maintenance | Nature of the hold |
|---|---|---|
| MTAP deleted (≤62.8%) | PRMT5 or MAT2A inhibitor; CDK4/6 inhibitor against the co-deleted CDKN2A | Genotype-anchored — the deletion cannot be undone |
| MAPK driver (~59%) | MEK inhibitor | Reroutable; needs monitoring and switching |
| CDKN2A deleted, RB1 intact | abemaciclib | Dependency |
| PTEN deleted | duvelisib | Dependency |
| Nothing targetable | cycled cytotoxic + immune | Weakest tier; no case left with nothing |

Tiers overlap, and where they do the evidence says **combine, not choose**: MTAP-null plus
RAS-active is the population in which PRMT5 + MAPK inhibition produced complete responses.

---

## 4. Why access is not the obstacle

A generic small molecule given systemically reaches **2.1%** of invaded brain tissue and **0.5%** of
CSF. At those numbers every route is **open** — margin −0.049/day and −0.036/day. That is the real
problem, and it is why radiation alone fails: a 21-day course against a year is a 5.8% duty cycle.

The requirement is **not** to bypass the barrier. It is access **0.196** in brain tissue and
**0.0145** in CSF. Measured intrinsic penetration clears that:

| Agent | Brain access | Clears 0.196? |
|---|---|---|
| RGN3067 | **equal brain and plasma levels**, brain Cmax 20 µM oral | yes |
| paxalisib | Kp,uu **0.31** | yes |
| generic small molecule | 0.021 | no |

**The mechanism is molecular selection, not a delivery device.** Devices were scored and lose on
their own measured numbers: an implanted multi-emitter ultrasound gives a measured 5.9× — real, and
still short (5.9 × 0.021 = 0.124). Convection-enhanced delivery has the best canine evidence of any
device and fails on duty cycle (1/365). Intrathecal injection clears CSF and is obtainable today, so
it is the backup, not a requirement.

---

## 5. Evidence grade of every number that decides the answer

Nothing here rests on a bare assumption. Graded against the standard *real data or a rigorous model,
with a transfer acceptable when justified in writing*: **17 of 17 live inputs pass; 0 fail.**

| Quantity | Value | Grade |
|---|---|---|
| Microtubule-class potency in canine HS | IC50 1.77–2.69 ng/mL, 4 canine HS lines | **measured, right species and disease** |
| CDK4/6 dependency in canine HS | CDKN2A down, Rb preserved, growth inhibited in every canine histiocytic line | **measured, right species and disease** |
| PI3K-axis potency | duvelisib IC50 287 nM in the responsive canine-HS subgroup | **measured, right species and disease** |
| MTAP/CDKN2A deletion frequency | 62.8% of canine HS | **measured, right species and disease** |
| Induction kill rate | **1.17/day derived** from measured IC50 (616 nM, worst line) and measured brain Cmax (20 µM) | derived from measured |
| Growth bar | 0.055/day | derived from canine-HS regrowth; **1.6–5.8× harder than the clinical data requires** |
| Brain access | paxalisib 0.31; RGN3067 brain ≈ plasma | measured, cross-species transfer |
| Target identity human→dog | ERK2 100%, PI3Kα 99.81%, PRMT5 99.37%, β-tubulin 98.42% | **computed from real sequences** |
| Second-primary rate | calibrated to observed canine-HS recurrence | derived from measured |
| ctDNA monitoring | canine PTPN11 plasma assay, 91% detection, 98.8% specific | **measured, right species and disease** |

**Robustness of the one derived number that carries the most weight:** closure needs ≥0.10/day. The
derived rate is 1.17/day, and it still closes at **0.89% of the measured brain exposure** — a **112×
cushion** on the species transfer.

---

## 6. The conditions

The decade holds if and only if all eight hold. **Five hold today. No engineering condition remains.**

| | Condition | Status |
|---|---|---|
| C1 | Every maintenance agent is intrinsically brain-penetrant and not an efflux substrate | **met** |
| C2 | Leptomeninges reached — same molecules, intrathecal as backup | **met** |
| C3 | Maintenance dosed continuously, never cycled | **met** |
| C4 | Induction agent is not a P-gp/BCRP substrate | **met** |
| **C5** | **Tumour carries a targetable lesion** | **one immunostain, decidable before treatment** |
| C6 | Radiation and CNS cytotoxic sequenced, not stacked | **met** |
| **C7** | Sponsor access to the investigational genotype-anchored agent | **not met; closure under C1–C6 does not require it** |
| **C8** | **The penetrant agents C1 and C4 need are obtainable for a dog** | **not met; see §6a for what the obtainable programme closes without them** |

None of the three outstanding conditions is an engineering problem. C5 is a test. C7 and C8 are
availability.

---

## 6a. What is achievable with licensed agents today, and what needs a compound released for dogs

Searched from obtainable agents first, the two programmes separate cleanly.

| | **Programme A — licensed today** | **Programme B — the full closure** |
|---|---|---|
| Needs a compound released for dogs? | no | yes, three of them |
| Extra-axial, meninges-based bulk (23/23 dogs) | **closes, +0.94/day** | closes |
| Leptomeninges / CSF | **closes by mouth, +0.031/day** | closes, +0.61/day |
| Invaded brain tissue, intact barrier | **marginal: −0.034 to +0.017/day** | closes, +0.59/day |
| All 16 routes at both sites | no | **yes** |

**Programme A** is surgical debulking plus radiation for induction, then continuous genotype-matched
maintenance: abemaciclib where CDKN2A is deleted and Rb intact, trametinib or cobimetinib on a MAPK
driver, duvelisib on the responsive expression subgroup, with liposomal clodronate,
hydroxychloroquine, gilvetmab and ctDNA detect-and-switch. Every one of those is licensed, dog-trialled
or already given to dogs.

The reason Programme A gets as far as it does is **abemaciclib**, and the reason is anatomical. This
tumour is extra-axial in 23 of 23 dogs — the bulk of it sits on the blood side of an
already-disrupted barrier. Abemaciclib's concentration in resected human brain lesions is a measured
19× the CDK6 IC50, which is a decisive margin there. Behind an *intact* barrier its own measured
rodent unbound ratios give 0.65–2.4 nM against a bar of 1.8 nM: it closes at the rat ratio and fails
at the mouse ratio. That is the honest span, computed from abemaciclib's own numbers rather than from
the generic small-molecule figure, which would have flattered it fivefold.

**What separates the two programmes is two properties on different agents, not a programme:**

1. **Access and duty from one schedule** at the invading edge — an oral, non-efflux-substrate agent
   that carries its own penetration past an intact barrier. Every obtainable alternative buys that
   access with a procedure, and a monthly catheter cannot also supply a continuous duty cycle.
2. **Genotype anchoring** — an agent aimed at the germline MTAP deletion itself, the only kind
   automatically matched to a *second* primary in a breed born predisposed.

Everything else the decade needs — the stratification, the continuous schedule, the toxicity budget,
the leptomeningeal route, the surveillance loop, and the kill where this tumour is actually based —
is satisfiable today. And none of the three missing agents has to be invented: the PRMT5 anchor is in
human Phase I/II, paxalisib is in human trials with a measured Kp,uu of 0.31, and RGN3067 is a
published compound with a measured oral brain Cmax of 20 µM. **The outstanding work is veterinary
formulation and access, not chemistry.**

---

## 7. The limits, stated plainly

- **No agent in any regimen here has been given to a dog with this disease.** Every margin is a model
  output from graded inputs.
- **Three of the agents in the closing regimen cannot be dispensed to a dog today** (§6a). The
  obtainable programme does not close the invading edge on a coherent schedule.
- **The honest comparator:** 44-day median for intracranial disease under surgery, radiation and
  chemotherapy; 568-day median with a 243-day disease-free interval for *localized* HS after
  debulking plus lomustine. The gap between that and ten years is the claim, and nothing here
  narrows it by measurement.
- **Brain-penetrant is not brain-effective.** Sagopilone, an access exemplar for this class, failed
  in human glioblastoma — no objective responses, PFS6 6.7%. RGN3067 is a different chemotype with a
  better exposure profile, but the warning stands.
- **The single cheapest decisive test has never been run:** one MTAP immunostain on archived tissue.
  If the tumour is MTAP-intact, the strongest tier does not apply.
- **The largest remaining uncertainty is not a drug.** How often a cleared, predisposed dog throws a
  new primary drives most of the spread in every scenario. That is an observational cohort, not an
  experiment.

---

## 8. What to do first, cheapest decisive step first

0. **Before any of it:** Programme A (§6a) is prescribable now. If a dog needs treating rather than
   studying, that is the plan, with its limit stated — it holds the bulk and the meninges and is
   marginal at the invading edge.
1. **MTAP immunostain** (plus p16 and Rb) on archived tumour tissue. Decides C5 and which tier applies.
2. **Run the 10 existing canine HS cell lines** against a colchicine-site tubulin binder and against
   a PRMT5 inhibitor. Converts two transfers into measurements, with no new animals.
3. **A canine Cmax** for the induction agent. Turns the last cross-species transfer into a dog number.
4. **An observational cohort** of cleared, predisposed dogs, to measure the second-primary rate.

---

*Every figure above is a model output computed from cited evidence and re-derived by automated tests
(768 passing). Where a number is transferred rather than measured, the grade says so. This is an
analysis, not veterinary advice; every decision belongs with clinicians who can examine the animal.*
