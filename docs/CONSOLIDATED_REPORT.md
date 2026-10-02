# Primary intracranial histiocytic sarcoma in a predisposed breed — a durable-therapy strategy

*Published, reader-facing version: <https://claude.ai/artifact/4Ho2u4jTieU579ExuRgvY5>. Full audit trail including every withdrawn claim: `AUDIT_TRAIL.md`.*

**Case:** primary intracranial (non-disseminated) histiocytic sarcoma in a predisposed breed. An
extra-axial, meninges-based mass that invades brain tissue (23/23 dogs) and seeds the leptomeninges
(19/19). Extracranial spread of primary CNS HS has never been reported.

**Question:** can a therapy hold for ten or more years against every mechanism and every escape
route, at every site the disease occupies?

**Answer: yes, within a stated catalogue and under five conditions that are met plus two that are
not.** The result is a checklist, not a probability. Full audit trail, including every withdrawn
claim, is in `AUDIT_TRAIL.md`.

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

| Role | Agent | Why it is in the set |
|---|---|---|
| Induction / position-independent kill | **RGN3067** (oral colchicine-site tubulin destabiliser) | Carries 6 of the 16 routes. Not an efflux-pump substrate (ratio 0.61) |
| Parallel-pathway cover | **paxalisib** (PI3K/AKT) | Kp,uu 0.31, confirmed non-substrate of both efflux pumps |
| Lineage removal | **liposomal clodronate** | Kills by being eaten, so it reaches non-dividing cells |
| Persister / autophagy cover | **hydroxychloroquine** | The only agent here with a canine phase I |
| Antigen-directed arm | **anti-PD-1 (gilvetmab)** | Obtainable for dogs |

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

The decade holds if and only if all seven hold. **Five hold today. No engineering condition remains.**

| | Condition | Status |
|---|---|---|
| C1 | Every maintenance agent is intrinsically brain-penetrant and not an efflux substrate | **met** |
| C2 | Leptomeninges reached — same molecules, intrathecal as backup | **met** |
| C3 | Maintenance dosed continuously, never cycled | **met** |
| C4 | Induction agent is not a P-gp/BCRP substrate | **met** |
| **C5** | **Tumour carries a targetable lesion** | **one immunostain, decidable before treatment** |
| C6 | Radiation and CNS cytotoxic sequenced, not stacked | **met** |
| **C7** | Sponsor access to the investigational genotype-anchored agent | **not met; closure under C1–C6 does not require it** |

---

## 7. The limits, stated plainly

- **No agent in any regimen here has been given to a dog with this disease.** Every margin is a model
  output from graded inputs.
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

1. **MTAP immunostain** (plus p16 and Rb) on archived tumour tissue. Decides C5 and which tier applies.
2. **Run the 10 existing canine HS cell lines** against a colchicine-site tubulin binder and against
   a PRMT5 inhibitor. Converts two transfers into measurements, with no new animals.
3. **A canine Cmax** for the induction agent. Turns the last cross-species transfer into a dog number.
4. **An observational cohort** of cleared, predisposed dogs, to measure the second-primary rate.

---

*Every figure above is a model output computed from cited evidence and re-derived by automated tests
(768 passing). Where a number is transferred rather than measured, the grade says so. This is an
analysis, not veterinary advice; every decision belongs with clinicians who can examine the animal.*
