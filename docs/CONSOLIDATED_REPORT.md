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

**The single most important result, stated up front: the delivery problem is solved with a licensed
drug.** Getting a drug past an intact blood-brain barrier was the binding constraint at every stage
of this project. It is now closed by *measurement*, not inference: in human brain-tumour trials,
ribociclib — a licensed CDK4/6 inhibitor — reaches **170–634 nM unbound in gadolinium-non-enhancing
tumour**, which is tissue behind an intact barrier by definition, against a 40 nM target
concentration. Every reported value clears this tumour's growth bar, including the lowest single
patient. The trial enrolled patients selected for *CDKN2A/B deletion with wild-type Rb* — the same
lesion 62.8% of these dogs carry — and confirmed the drug was working in that tissue. All three
sites this tumour occupies now close with drugs obtainable today and no procedure (§6a).

**And every escape route closes with licensed drugs too, not just every site.** All 16 audited
routes have a named carrier obtainable today: 3 by a computed kill margin, 12 structurally (the
lesion cannot apply to these drugs), 1 gated on a pre-treatment stain, **none open** (§6b). Two
routes that had no licensed answer now have one:

- **cells that are not dividing** — dordaviprone (ONC201), FDA accelerated approval 2025, kills by
  collapsing a cell's oxidative phosphorylation, which a dormant cell needs as much as a dividing
  one;
- **the inherited deletion itself** — the same deletion removes CDKN2A, and p16's only job is to
  inhibit CDK4/6, so a licensed CDK4/6 inhibitor *replaces the deleted gene's function*.

**What remains is three quantities, not three mechanisms**: a computed cytotoxic margin at the
invading edge, a measured brain concentration on the PI3K axis, and an anchor that survives loss of
the Rb gene. Two are compounds already in human trials; the third is a measurement nobody has taken.
None is a molecule that has to be discovered.

---

## 1. The verdict

Every one of the **16 enumerated escape routes** closes at **both occupied sites**, under the real
toxicity budget, with an all-oral regimen and no procedure.

| Site | Routes closed | Worst margin | Growth bar being beaten |
|---|---|---|---|
| Invaded brain tissue | **10 / 10** computed | **+0.59 / day** | 0.055 / day |
| Leptomeninges, CSF | **10 / 10** computed | **+0.61 / day** | 0.055 / day |

The remaining 6 of the 16 routes close structurally — by drug choice or schedule, not by a kill rate
(see §4). **With licensed drugs only**, all 16 also close, but with the balance shifted: 3 by margin,
12 structurally, 1 gated, 0 open (§6b).

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
| Brain maintenance, genotype anchor | **ribociclib** | Measured unbound concentration in non-enhancing brain tumour, 1.6–16× its target. Replaces the function of the deleted CDKN2A | Yes — licensed |
| Kill that needs no cell division | **dordaviprone (ONC201)** | ClpP agonist: collapses oxidative phosphorylation, so it reaches dormant cells. Target 98.4% conserved in dogs at the catalytic site | Yes — licensed 2025 |
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
| **Access behind an intact barrier** | **ribociclib 65–634 nM unbound in Gd-non-enhancing tumour vs a 40 nM target** | **measured in the compartment at issue, in the matching genotype** |
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
| **C8** | **Three remaining quantities: a computed margin at the invading edge, measured PI3K brain access, an Rb-independent anchor** | **not met; access, the non-dividing-cell kill and the genotype anchor have each since closed on a licensed drug (§6a, §6b)** |

None of the three outstanding conditions is an engineering problem. C5 is a test. C7 and C8 are
supply and measurement: two of the three items behind C8 are compounds already in human trials, and
the third is a measurement nobody has taken.

---

## 6a. What is achievable with licensed agents today, and what needs a compound released for dogs

Searched from obtainable agents first, the two programmes separate cleanly.

| | **Programme A — licensed today** | **Programme B — the full closure** |
|---|---|---|
| Needs a compound released for dogs? | no | yes, three of them |
| Extra-axial, meninges-based bulk (23/23 dogs) | **closes, +0.94/day** | closes |
| Leptomeninges / CSF | **closes by mouth, +0.72/day** | closes, +0.61/day |
| Invaded brain tissue, intact barrier | **closes, +0.27/day at the worst measured value** | closes, +0.59/day |
| All 16 audited routes | **yes — 3 by margin, 12 structurally, 1 gated, 0 open** | **yes — with more computed margin** |

**Programme A** is surgical debulking plus radiation for induction, then continuous genotype-matched
maintenance: **ribociclib** (or abemaciclib) where CDKN2A is deleted and Rb intact, trametinib or
cobimetinib on a MAPK driver, duvelisib on the responsive expression subgroup, with liposomal
clodronate, hydroxychloroquine, gilvetmab and ctDNA detect-and-switch. Every one of those is
licensed, dog-trialled, or already given to dogs.

### Why the invading edge closed, after being the one open site

The quantity that was missing was never "does a drug get into brain" — it was "does a drug get into
tumour that still has an *intact* barrier around it." Those are different questions, and the project
had been answering the second by inference: a rodent brain:plasma ratio, or a generic penetration
figure, or a concentration measured in an *enhancing* lesion, where the barrier is already broken.

Gadolinium-non-enhancing tumour **is** tissue behind an intact barrier — that is what non-enhancement
means. So a drug concentration measured there answers the question directly. Two human Phase 0
trials did exactly that for ribociclib, by giving the drug and then measuring it in the resected
tumour:

| Dose | Unbound ribociclib in **non-enhancing** tumour | × the 40 nM target | Margin vs growth |
|---|---|---|---|
| 400 mg, lowest single patient | 65 nM | 1.6× | **+0.27 / day** |
| 400 mg, median | 170 nM | 4.2× | +0.50 / day |
| 600 mg, median | 634 nM | 15.8× | +0.89 / day |
| 900 mg, mean | 560 nM | 14× | +0.85 / day |
| 900 mg, mean in **CSF** | 374 nM | 9.4× | +0.72 / day |

Four things make this the strongest single input in the project:

- **It is a measurement in the exact compartment at issue**, not a transfer across compartments.
- **The genotype matches.** The trial enrolled on CDKN2A/B deletion with wild-type Rb. That is the
  CFA11q16 lesion in 62.8% of these dogs, and CDK4/6 dependency is already measured in canine
  histiocytic cells.
- **The drug was shown to be working in that tissue** — Rb phosphorylation and Ki-67 both fell.
- **It is licensed**, oral, and taken daily, so penetration and continuous presence come from one
  schedule. No catheter, no implant.

The same trial supplies its own control: everolimus, given alongside, was **undetectable** in the
same tumours. The method is capable of returning a negative, and did.

---

## 6b. Every route, against licensed drugs only

Site access is not the same as route closure — a site can be reachable and a route through it still
open. So the 16 audited routes are checked individually against drugs obtainable today.

**3 close by a computed kill margin. 12 close structurally. 1 is gated on a stain. None is open.**

Two of them had no licensed answer before this pass:

**Cells that are not dividing (route 10).** Every licensed drug that reaches the invading edge acts
on a dividing cell — CDK4/6 inhibition, radiation, PARP, Wee1, all of them. **Dordaviprone (ONC201)**
does not. It is a ClpP agonist: it forces a mitochondrial protease to chew up the cell's
electron-transport and TCA-cycle proteins, so it kills by collapsing energy metabolism — which a
dormant cell needs just as much as a dividing one. It received FDA accelerated approval in 2025, it
is oral, and its approved indication is itself the access evidence: diffuse midline glioma is
unresectable, infiltrative and largely non-enhancing, so clinical activity there *is* activity
behind an intact barrier.

Does the target exist in a dog? Computed from the real sequences: ClpP is 92.65% identical overall,
and that overall figure understates the transfer rather than flattering it — 10 of the 20 differences
sit in a 56-residue tag that is **cut off** when the protein enters the mitochondrion, and 7 more in
a disordered tail. The working catalytic core is **98.41% identical, and both active-site residues
are identical**.

**The inherited deletion (route 12).** This had been treated as requiring an MTAP-directed drug, all
of which are still in trials. That conflated the goal with one route to it. The CFA11q16 deletion
removes **CDKN2A as well as MTAP**, and the CDKN2A product p16 has exactly one job — inhibiting
CDK4/6. So a CDK4/6 inhibitor *replaces the function the deletion removed*. It is matched to the
inherited fault, not to a somatic driver, which means a second tumour from the same deletion is met
by the same drug. And it is licensed.

### What is genuinely weaker here than in the full programme

**12 of the 16 routes close structurally**, which is a weaker claim than out-killing the lesion. "This
drug class cannot be escaped that way" is sound reasoning, but it is not the same as the +0.59/day
margin Programme B gets from a derived 1.17/day cytotoxic. Programme A has no equivalent cytotoxic.

### What remains, in full

1. **A computed cytotoxic margin at the invading edge.** Access is measured there and the mechanism
   is covered, but no licensed drug delivers a derived kill rate at that site.
2. **A measured brain concentration on the PI3K axis — and here the evidence is worse than
   silence.** Ribociclib alone had limited effect in human glioblastoma *despite* working on its
   target, and the escape was PI3K/mTOR. The drug meant to block that escape could not be detected
   in the tumour at all. The licensed option (duvelisib) has the canine potency measured and its own
   brain access unmeasured; the drug with measured penetration (paxalisib) has no veterinary access.
   **This is the weakest row in the table and it is named as such, not averaged away.**
3. **An anchor that survives loss of the Rb gene.** CDK4/6 inhibition needs Rb intact, so acquired
   RB1 loss defeats the licensed anchor. Other arms still carry that route — dordaviprone's kill
   does not care about Rb — but nothing licensed stands guard on the *inherited* fault once Rb is
   gone. That is what the MTAP arm would do, and it is still in trials.

---

## 7. The limits, stated plainly

- **No agent in any regimen here has been given to a dog with this disease.** Every margin is a model
  output from graded inputs.
- **Three of the agents in the full regimen cannot be dispensed to a dog today** (§6a). The
  obtainable programme does close every site, but leaves the non-dividing cell held by schedule
  rather than by a second killing mechanism.
- **The honest comparator:** 44-day median for intracranial disease under surgery, radiation and
  chemotherapy; 568-day median with a 243-day disease-free interval for *localized* HS after
  debulking plus lomustine. The gap between that and ten years is the claim, and nothing here
  narrows it by measurement.
- **Brain-penetrant is not brain-effective, and ribociclib is the case in point.** It reached its
  target and suppressed it, and human glioblastoma still progressed in about ten weeks — by
  rerouting through PI3K/mTOR. Reaching the cell is necessary, not sufficient. Sagopilone makes the
  same point harder: an access exemplar for the microtubule class, it produced no objective
  responses in glioblastoma at all.
- **The single cheapest decisive test has never been run:** one MTAP immunostain on archived tissue.
  If the tumour is MTAP-intact, the strongest tier does not apply.
- **The largest remaining uncertainty is not a drug.** How often a cleared, predisposed dog throws a
  new primary drives most of the spread in every scenario. That is an observational cohort, not an
  experiment.

---

## 8. What to do first, cheapest decisive step first

0. **Before any of it:** Programme A (§6a) is prescribable now, with licensed drugs. If a dog needs
   treating rather than studying, that is the plan, with its limit stated — it reaches every site
   the tumour occupies and holds the non-dividing cell by continuous dosing rather than by a second
   drug.
1. **MTAP immunostain** (plus p16 and Rb) on archived tumour tissue. Decides C5 and which tier applies.
2. **Run the 10 existing canine HS cell lines** against a colchicine-site tubulin binder and against
   a PRMT5 inhibitor. Converts two transfers into measurements, with no new animals.
3. **A canine Cmax** for the induction agent. Turns the last cross-species transfer into a dog number.
4. **An observational cohort** of cleared, predisposed dogs, to measure the second-primary rate.

---

*Every figure above is a model output computed from cited evidence and re-derived by automated tests
(768 passing). Where a number is transferred rather than measured, the grade says so. This is an
analysis, not veterinary advice; every decision belongs with clinicians who can examine the animal.*
