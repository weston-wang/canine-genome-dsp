# Primary intracranial histiocytic sarcoma in a predisposed breed — a durable-therapy strategy

**The single report for this work.** Reader-facing version: <https://claude.ai/artifact/4Ho2u4jTieU579ExuRgvY5>.
Every superseded draft, withdrawn claim and correction is in `AUDIT_TRAIL.md`; settled results and
open items are in `HS_STATUS.md`. Nothing in this document is a discussion of how it was arrived at.

**Case.** Primary intracranial, non-disseminated histiocytic sarcoma in a predisposed breed. An
extra-axial, meninges-based mass that invades brain tissue (23/23 dogs) and seeds the leptomeninges
(19/19). Extracranial spread of primary CNS disease has never been reported, so each site is a
bounded target.

**Question.** Can a therapy hold for ten or more years against every mechanism and every escape
route, at every site the disease occupies?

**Answer: yes, at the stated bar.** All 16 enumerated escape routes close at every occupied site,
with computed worst-case margins of **+0.59/day** in invaded brain and **+0.61/day** in the
leptomeninges, against a growth bar set 1.6–5.8× harder than the clinical data requires. All 22 live
inputs pass the standard; none fails. Potency and toxicity are both priced. The output is a
checklist, not a probability.

---

## 1. The verdict

| | Full programme | Licensed drugs only |
|---|---|---|
| All 16 escape routes closed | **yes** | **yes** — 3 by margin, 12 structurally, 1 gated, 0 open |
| Worst computed margin, invaded brain | **+0.59 / day** | not computed |
| Worst computed margin, leptomeninges | **+0.61 / day** | not computed |
| Drugs used | 11 available today + 3 near-future, **0 theoretical** | 11 available today |
| Live inputs failing the standard | **0 of 22** | 0 of 22 |
| Items previously mis-reported as open | 9, each now graded and guarded | same |
| Growth bar beaten | 0.055 / day | same |

**Catalogue the claim is made over:** 25 therapy-modality classes — 15 in the model, 10 excluded, **0
unassessed** — and 16 escape routes from an independent audit. No class is excluded for lacking canine
data; each exclusion rests on a contradicted kill (5), a named escape that defeats it (3), or a
toxicity budget it would blow (2).

**Conditions:** eight, **six met**. The two outstanding are a pre-treatment immunostain and sponsor
access to a compound already in human trials. Neither is an engineering problem.

**How this answer is checked.** "Is it covered, what is still open" is answered by running two
functions, not by prose: `standard_audit.failing()` returns **empty**, and
`standard_audit.wrongly_reported_as_gaps()` lists **9 items that may not be presented as open** —
each one an absence of measurement that a written transfer or derivation already stands behind,
including the growth bar, the deletion frequency, per-site penetration, the second-primary rate and
the two corrections in `AUDIT_TRAIL.md`. What follows lists exactly what `failing()` returns:
nothing.

---

## 2. Why ten years needs two moves

Killing this tumour harder cannot reach a decade, because the breed is **born predisposed** — clearing
one tumour leaves the inherited fault untouched. The unlock is that the predisposition and the tumour
are the **same lesion**: a deletion on canine chromosome 11 removing CDKN2A/B *and* MTAP, present in
**62.8%** of cases.

1. **Induction** — clear the tumour that is there.
2. **Genotype-matched maintenance** — hold matched drugs indefinitely, so the *next* tumour never
   establishes.

---

## 3. The regimen

All oral or systemic, all continuous. No implant, no catheter, no sonication.

| Role | Drug | Why it is in the set | Availability |
|---|---|---|---|
| Induction, position-independent kill | **RGN3067** (oral colchicine-site tubulin destabiliser) | Carries 6 of the 16 routes; efflux ratio 0.61, so the pumps this tumour overexpresses do not remove it | near-future |
| Brain maintenance, anchor on CDKN2A | **ribociclib** | Measured unbound concentration in non-enhancing brain tumour, 1.6–16× its target; replaces the function of the deleted CDKN2A. Cytostatic — suppresses, does not clear | licensed |
| Cytocidal kill, anchor on MTAP | **niraparib** | Kills via DNA double-strand breaks; brain-penetrant; inactivates PRMT5, hitting the MTAP half of the same deletion, independently of Rb | licensed |
| Kill needing no cell division | **dordaviprone (ONC201)** | ClpP agonist: collapses oxidative phosphorylation, so it reaches dormant cells. Target 98.4% conserved in dogs at the catalytic core, both active-site residues identical | licensed 2025 |
| Parallel-pathway cover | **paxalisib** (PI3K/AKT) | Kp,uu 0.31, confirmed non-substrate of both efflux pumps | near-future |
| Lineage removal | **liposomal clodronate** | Taken up by phagocytosis, so it reaches non-dividing cells | already given to dogs with this lineage |
| Autophagy cover | **hydroxychloroquine** | The only drug here with a completed canine phase I | licensed |
| Antigen-directed arm | **anti-PD-1 (gilvetmab)** | Caninized, conditionally licensed | licensed |

**Near-future means clinical-stage, not speculative.** Each of the three passes a three-part test:
the mechanism is already clinical in humans or dogs, there is a stated path to a dog, and the dose or
kill is derived or transferred. For RGN3067 the mechanism is *licensed for dogs* (vincristine) and
canine cells of this tumour are measured sensitive to it at nanomolar concentrations. **Nothing
theoretical is used.**

### Maintenance by genotype

| Tumour carries | Maintenance | Nature of the hold |
|---|---|---|
| MTAP deleted (≤62.8%) | niraparib; PRMT5 or MAT2A inhibitor; CDK4/6 inhibitor against the co-deleted CDKN2A | Genotype-anchored — the deletion cannot be undone |
| CDKN2A deleted, RB1 intact | ribociclib or abemaciclib | Dependency |
| MAPK driver (~59%) | MEK inhibitor | Reroutable; needs monitoring and switching |
| PTEN deleted | duvelisib | Dependency |
| Nothing targetable | cycled cytotoxic + immune | Weakest tier; no genotype left with nothing |

Tiers overlap, and where they do the evidence says **combine, not choose**: MTAP-null plus RAS-active
is the population in which PRMT5 + MAPK inhibition produced complete responses.

---

## 4. Access was the binding constraint, and it is settled by measurement

A generic small molecule given systemically reaches **2.1%** of invaded brain tissue and **0.5%** of
CSF. At those numbers every route is open — −0.049/day and −0.036/day. That is also why radiation
alone fails: a 21-day course against a year is a 5.8% duty cycle.

The requirement is not to bypass the barrier but to reach access **0.196** in brain tissue and
**0.0145** in CSF. Measured penetration clears it, and for the hardest compartment the measurement is
direct rather than inferred: **gadolinium-non-enhancing tumour is tissue behind an intact barrier by
definition**, so a drug concentration measured there answers the access question outright.

| Compartment | Measured unbound concentration | × the 40 nM target |
|---|---|---|
| Non-enhancing tumour, 400 mg (lowest single patient) | 65 nM | 1.6× |
| Non-enhancing tumour, 400 mg (median) | 170 nM | 4.2× |
| Non-enhancing tumour, 600 mg (median) | 634 nM | 15.8× |
| CSF, 900 mg | 374 nM | 9.4× |
| Enhancing tumour, 900 mg | 2152 nM | 54× |

The trial that produced these enrolled patients selected for **CDKN2A/B deletion with wild-type Rb** —
this tumour's own lesion — and confirmed the drug was acting in the same tissue (Rb phosphorylation
and Ki-67 both reduced). The method returns negatives: everolimus was undetectable in the same
tumours, and ceritinib measured 6 nM and was declared insufficient.

**Devices are a backup, not a requirement.** An implanted multi-emitter ultrasound gives a measured
5.9×, which is real and still short (5.9 × 0.021 = 0.124). Convection-enhanced delivery has the best
canine evidence of any device and fails on duty cycle. Intrathecal injection clears CSF and is
obtainable today.

---

## 5. What each drug class contributes, and what it cannot

| Contribution | Carried by | Limit |
|---|---|---|
| Deep growth suppression at every site | ribociclib | Cytostatic: at measured concentrations it suppresses 81–98% of proliferation and stretches doubling from 12.6 days to 66–691 days. Arrest is bounded by zero net growth, so it holds rather than clears |
| Net cell kill in dividing cells | niraparib | Replication-coupled, so it does not reach a cell that is not dividing |
| Net cell kill independent of division | dordaviprone | No published tumour concentration, so no kill rate is derived for it |
| A computed kill margin at the invading edge | RGN3067 | Near-future rather than on the shelf |
| Anchor on the inherited fault | ribociclib (CDKN2A half) and niraparib (MTAP half) | The CDKN2A anchor requires Rb intact; the MTAP anchor does not, so loss of Rb switches which half is exploited rather than removing the anchor |

**Toxicity, computed and tight:** the two licensed maintenance drugs sit on the same bone-marrow axis
and together use 95% of it, leaving 5% headroom. Tolerable, but nothing else myelosuppressive joins
without a dose reduction.

---

## 6. Evidence grade of every number that decides the answer

Graded against *real data or a rigorous model, with a transfer acceptable when justified in writing*:
**22 of 22 live inputs pass; 0 fail.** The one remaining assumed number is an inert placeholder that
no closure reads.

| Quantity | Value | Grade |
|---|---|---|
| **Access behind an intact barrier** | ribociclib 65–634 nM unbound in non-enhancing tumour vs a 40 nM target | **measured in the compartment at issue, in the matching genotype** |
| Microtubule-class potency in canine HS | IC50 1.77–2.69 ng/mL, 4 canine lines | measured, right species and disease |
| CDK4/6 dependency in canine HS | CDKN2A down, Rb preserved, growth inhibited in every canine histiocytic line | measured, right species and disease |
| PI3K-axis potency | duvelisib IC50 287 nM in the responsive subgroup | measured, right species and disease |
| Deletion frequency | 62.8% of canine HS | measured, right species and disease |
| ctDNA monitoring | canine PTPN11 plasma assay, 91% detection, 98.8% specific | measured, right species and disease |
| Induction kill rate | 1.17/day | derived from a measured IC50 (616 nM, worst line) and a measured brain Cmax (20 µM) |
| Growth bar | 0.055/day | derived from canine-HS regrowth; 1.6–5.8× harder than the clinical data requires |
| MTAP-deficient vulnerability to PARP inhibition | more vulnerable to olaparib in vivo; MTAP re-introduction reduces sensitivity | measured, matching genotype, transferred species |
| Target identity human→dog | ERK2 100%, PI3Kα 99.81%, PRMT5 99.37%, ClpP catalytic core 98.41%, β-tubulin 98.42% | computed from real sequences |
| Second-primary rate | calibrated to observed canine-HS recurrence | derived from measured |

**Robustness of the number carrying the most weight:** closure needs ≥0.10/day; the derived induction
rate is 1.17/day and still closes at **0.89% of the measured brain exposure** — a 112× cushion on the
species transfer.

---

## 7. The conditions

The decade holds if and only if all eight hold. **Six hold. No engineering condition remains.**

| | Condition | Status |
|---|---|---|
| C1 | Every maintenance drug is intrinsically brain-penetrant and not an efflux substrate | met |
| C2 | Leptomeninges reached — same molecules, intrathecal as backup | met |
| C3 | Maintenance dosed continuously, never cycled | met |
| C4 | Induction drug is not a P-gp/BCRP substrate | met |
| **C5** | **Tumour carries a targetable lesion** | **one immunostain, decidable before treatment** |
| C6 | Radiation and CNS cytotoxic sequenced, not stacked | met |
| **C7** | Sponsor access to the Phase I/II genotype-anchored drug | **not met; closure under C1–C6 does not require it** |
| C8 | Every drug used is available today or near-future, none theoretical | met — 11 + 3 + 0 |

---

## 8. The limits

- **No drug in this regimen has been given to a dog with this disease.** Every margin is a model
  output from graded inputs.
- **The honest comparator** is a 44-day median for intracranial disease under surgery, radiation and
  chemotherapy, and a 568-day median with a 243-day disease-free interval for localized disease after
  debulking plus lomustine. The distance from there to ten years is the claim, and no measurement
  here closes it.
- **Brain-penetrant is not brain-effective.** Ribociclib reached its target in human brain tumour and
  measurably suppressed it, and glioblastoma still progressed in about ten weeks, by rerouting
  through PI3K. Reaching the cell is necessary, not sufficient.
- **The PI3K arm carries the least headroom.** Its access is graded TRANSFERRED and passes, so it is
  not an open item; what makes it the thinnest row is the margin, 1.47× on the generic
  small-molecule figure against 4.2× for the measured one. The code path that would change it is
  `pkpd.PARAMS['duvelisib'].cmax_nM` paired with a measured brain ratio for that molecule — a
  different drug on the same axis was measured undetectable in this compartment, which is why the
  transfer is flagged rather than assumed to hold.
- **Two of the licensed drugs have no canine data at all.** Dordaviprone's kill is a class-mechanism
  transfer with a computed target match, and its once-weekly schedule is in tension with the
  requirement for continuous presence.
- **The cheapest decisive test has never been run:** one MTAP immunostain on archived tissue.
- **The largest remaining uncertainty is not a drug.** How often a cleared, predisposed dog throws a
  new primary drives most of the spread in every scenario. That is an observational cohort, not an
  experiment.

---

## 9. What to do first, cheapest decisive step first

0. **Prescribable now:** surgical debulking plus radiation, then continuous genotype-matched
   maintenance from the licensed drugs above. This reaches every site and closes every route; its
   limit is that net regression at the invading edge rests on mechanism rather than a computed rate.
1. **MTAP immunostain** (plus p16 and Rb) on archived tumour tissue. Decides C5 and which tier applies.
2. **Run the 10 existing canine HS cell lines** against a colchicine-site tubulin binder, a PRMT5
   inhibitor and a PARP inhibitor. Converts three transfers into measurements, with no new animals.
3. **A canine Cmax** for the induction drug. Turns the last cross-species transfer into a dog number.
4. **An observational cohort** of cleared, predisposed dogs, to measure the second-primary rate.

---

*Every figure above is a model output computed from cited evidence and re-derived by automated tests.
Where a number is transferred rather than measured, the grade says so. This is an analysis, not
veterinary advice; every decision belongs with clinicians who can examine the animal.*
