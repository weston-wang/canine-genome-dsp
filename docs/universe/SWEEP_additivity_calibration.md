# SWEEP: additivity under sustained dosing — what the maintenance trial tested, and what the combination rule should be

Resolves the `CONTRADICTED` item in `lymphoma_standard_audit.sustained_additivity_item()`
(`src/canine_dsp/lymphoma_standard_audit.py:129-151`) and `docs/LYMPHOMA_STATUS.md:394`.

**Success criterion, quoted (CLAUDE.md):** "real data **or a rigorous model**", with a cross-species /
disease / class transfer acceptable "if the transfer is justified in writing", graded MEASURED /
TRANSFERRED / DERIVED / ASSUMED. "I'm not asking if it's been demonstrated, I know it's not."
Nothing below is graded against "demonstrated in dogs". Sources: PubMed (DOI links given per claim),
plus the project's own record.

---

## Headline

Three separate things are true, and only the first was in the status doc:

1. **PMID 28100766 does NOT test sustained full-dose CHOP.** Its maintenance arm swapped the drugs:
   **vincristine + chlorambucil + actinomycin-D**, containing **no doxorubicin, no cyclophosphamide, no
   prednisolone and no L-asparaginase**. So the trial refutes *spaced maintenance with three partly
   different drugs*, not *sustained full-dose CHOP*. The contradiction as written in
   `LYMPHOMA_STATUS.md:394` is **partly an artefact of comparing different things**.

2. **But the model is still wrong, and a better-matched canine trial proves it.** Zandvliet 2013
   (PMID 23746872) is a **prospective randomised trial, 81 dogs, same multidrug protocol, prednisolone
   in one arm and omitted in the other**, and found **no difference in anything**. That is a measured,
   in-species, in-disease, randomised measurement of exactly the quantity the model over-credits: the
   marginal contribution of the non-gated agent added to the gated ones. Measured value: **zero**.
   In the model, that same agent is the difference between **cure at day 98.7 and never curing**.

3. **A graded discount on additivity does not fix it.** Swept below: scaling the non-leading agents'
   contribution from 100% down to 10% moves the clear day from 98.7 to 99.5. The defect is not the
   *size* of the summed kill; it is that **an agent is credited for longer than its own resistance
   escape allows, and the verdict is a knife-edge on one agent's potency**.

---

## (a) What PMID 28100766 actually tested

**Lautscham EM, Kessler M, Ernst T, Willimzig L, Neiger R.** "Comparison of a CHOP-LAsp-based protocol
with and without maintenance for canine multicentric lymphoma." *Vet Rec* 2017;180(12):303.
PMID 28100766, [DOI 10.1136/vr.104077](https://doi.org/10.1136/vr.104077). Single centre
(Small Animal Clinic Hofheim, Germany), retrospective, sequential cohorts — **not randomised**.

| | cohort 1 (maintenance) | cohort 2 (discontinuous) |
|---|---|---|
| n | **75** | **333** |
| induction | CHOP-LAsp-based, **28 weeks** (cyclophosphamide, hydroxydaunorubicin=doxorubicin, Oncovin=vincristine, prednisolone, L-asparaginase) | **the same 28-week induction** |
| after induction | **maintenance phase: vincristine, chlorambucil, actinomycin-D**, total treatment duration **2 years** | **therapy discontinued** |
| median duration of first remission (DFR) | **216 d** | **184 d** |
| median survival (ST) | **375 d** | **304 d** |
| 6-month / 1-year / 2-year survival | **73% / 50% / 24%** | **67% / 39% / 21%** |
| significance | ST **P=0.291**; DFR **P=0.071** | — |

Multivariate factors negative for ST in both groups: corticosteroid pretreatment (P=0.005),
thrombocytopenia at diagnosis (P=0.019), stage (P=0.009), substage b at relapse (P<0.001), age
(P=0.002), incomplete/unstable remission needing intensification (P=0.004).
Conclusion as published: "This study supports the use of a discontinuous protocol for canine
multicentric lymphoma."

**ALREADY IN RECORD** as a citation and a conclusion: `docs/LYMPHOMA_PRIOR_ART_TREATMENTS.md:559-563`,
`docs/LYMPHOMA_STATUS.md:394`, `src/canine_dsp/lymphoma_standard_audit.py:147-151`.
**NEW:** the *drug composition of the maintenance arm*, the per-arm 6-month/1-year/2-year survival
rates, and the multivariate factor list. The record cited the paper's conclusion without recording
which drugs the maintenance phase contained — which is the fact that decides the question.

### Does it refute sustained full-dose therapy, or only spaced maintenance?

**Only spaced, partly-substituted maintenance.** Three mismatches against what the model simulates,
in descending order of importance:

1. **Drug substitution, not continuation (decisive).** Of the model's four CHOP agents, **one**
   (vincristine) continued into maintenance. **Doxorubicin, cyclophosphamide and prednisolone all
   stopped.** Two drugs that are *not in the model's CHOP regimen at all* (chlorambucil, actinomycin-D)
   were introduced. So the arm cannot speak to sustaining doxorubicin, cyclophosphamide or
   prednisolone, and it is prednisolone that carries the model's entire margin (see (e)).
   **This alone makes the "sustained CHOP clears" claim untested by this trial, in either direction.**
2. **Dose intensity.** Canine lymphoma maintenance is given at intervals of about 2 weeks and at
   reduced intensity, against induction intervals of 1-2 weeks. I **could not obtain this trial's own
   doses and intervals** — see "Not verified" below — so I cannot put a number on cohort 1's dose
   intensity. Indicative canine maintenance dosing from a different protocol (LMP/DMAC, VIN WSAVA 2005
   proceedings, **not this trial, indicative only**): chlorambucil 20 mg/m² PO q15d; vincristine
   0.5-0.7 mg/m² IV q15d alternating with chlorambucil; actinomycin-D 0.75 mg/m² IV q15d; prednisone
   20 mg/m² PO every other day. Against that, the model credits **continuous** kill (`duty=1.0` for
   prednisolone) or a 0.35 duty cycle for the cytotoxics.
3. **On-therapy duration.** Both arms got 196 days (28 weeks) of induction; cohort 1 added maintenance
   to 730 days, i.e. **3.7x longer on therapy**. So the trial *is* a real test of therapy duration
   past 6 months — just not of *this* regimen at *this* intensity.

**Honest statement of what survives.** The trial does not refute sustained full-dose CHOP. It does
establish that **3.7x more on-therapy time with a vincristine-containing, partly-substituted,
spaced regimen buys at most 32 days of remission and 71 days of survival, neither significant, in
408 dogs.** That is a hard upper bound on what *any* "keep going for longer" strategy of this shape
delivers, and it is the correct thing for the model to be calibrated against.

---

## (b) Other canine maintenance / protocol-duration evidence

| study | design | n | result |
|---|---|---|---|
| **Garrett 2002**, *JVIM* 16(6):704-9, PMID 12465768, [DOI](https://doi.org/10.1892/0891-6640(2002)016<0704:eoacpw>2.3.co;2) **NEW** | 6-month maintenance-**free** modified UW-25 CHOP vs **historical** control on a similar protocol **with a prolonged maintenance phase** | **53** vs **55** | Remission 94.2% (CR 92.3%). **Median DFI 282 d and survival 397 d (no maintenance) vs 220 d and 303 d (maintenance)**; P=0.2835 and P=0.3365. 41.5% (22/53) needed a delay or dose reduction; 9.4% (5/53) hospitalised. Maintenance-free "provides similar DFI and survival". **Note the point estimates favour NO maintenance.** |
| **Hahn 1992**, *JVIM* 6(1):3-10, PMID 1548624, [DOI](https://doi.org/10.1111/j.1939-1676.1992.tb00979.x) **NEW** | "Is maintenance chemotherapy appropriate…": single-agent doxorubicin, **3 cycles then nothing**, vs COP then **maintenance** (cyclophosphamide + prednisone + methotrexate). Retrospective | **38** vs **67** (105 total) | "**No significant differences** were observed in first-remission length or survival time" (P>0.05). Sex, weight, age, stage, performance status, cell type and grade were not predictive of responsiveness to either protocol. |
| **Vos 2019**, *Vet Comp Oncol* 17(3):276-84, PMID 31140707, [DOI](https://doi.org/10.1111/vco.12465) **NEW — and it points the other way** | 12-week CHOP (designed **+58% dose intense** for doxorubicin and cyclophosphamide, **−21%** for vincristine) vs 19-week CHOP; non-randomised **contemporaneous** controls | **47** total | CR 89.3% vs 89.5% (equal). **12-week: median PFS 141 d, OS 229 d. 19-week: median PFS 245 d, OS 347 d.** PFS **P=0.047**, OS **P=0.013** — the **shorter** protocol was **worse** despite higher dose intensity. Authors implicate vincristine dose intensity and/or "shorter overall temporal drug exposure". |
| **Lautscham 2017** (above), PMID 28100766 | 28-week induction ± 2-year maintenance | 75 vs 333 | DFR 216 vs 184 d, ST 375 vs 304 d, both NS |

**Is the consistent finding that extending therapy adds nothing? No — and this correction matters.**
The evidence is **two-sided and saturating**:

- **Below ~19 weeks, duration helps.** Vos 2019: going from 19 weeks to 12 weeks *lost* 104 days of
  PFS and 118 days of OS, significantly, **even though dose intensity went up**. So "total temporal
  exposure" is doing real work inside the induction range.
- **Beyond ~25-28 weeks, duration adds nothing.** Garrett 2002 (point estimates favour stopping),
  Hahn 1992 (NS), Lautscham 2017 (NS).

So the canine literature puts a **saturation point at roughly 19-28 weeks (133-196 days)** of
multi-agent therapy. Any model whose cure depends on sustaining a regimen past ~6 months must explain
why 408 dogs (Lautscham) + 108 (Garrett) + 105 (Hahn) show **no** benefit past that point.
`GROUNDED_ESCAPES`-based clearance windows of 365 d and beyond sit squarely in the region the dog data
say is empty. This saturation bound is **NEW to the record** and is the single most useful calibration
constraint found in this sweep.

---

## (c) What combination pharmacology says the right rule is

### The three "no-interaction" null models, and which one the field actually uses clinically

Palmer AC & Sorger PK, "Combination cancer therapy can confer benefit via patient-to-patient
variability without drug additivity or synergy", *Cell* 2017;171(7):1678-1691.
PMID 29245013, [DOI 10.1016/j.cell.2017.11.009](https://doi.org/10.1016/j.cell.2017.11.009),
PMC5741091 (full text read). **NEW to the record** — the record cites Saputra, Bozic/Nowak and
Komarova & Wodarz but not this.

Quoted definitions from the paper:

- **Bliss Independence** — "there is no drug interaction when two toxins confer statistically
  independent probabilities of cell death (thus, **surviving fractions are multiplied**)".
- **Loewe Additivity** — "no interaction … when a two drug mixture has potency equa[l]" to the
  dose-equivalent sum.
- **Independent drug action** (the paper's model) — "proposes **neither additive effect nor even a
  small 'sub-additive' enhancement of effect**"; "each patient's response equals **the better one of
  their two single agent responses**"; "In some contemporary literature this model is called
  **'Highest Single Agent'**." Under Gaddum's classification the paper invokes, "a combined effect
  **exactly equal to the strongest single drug**" is *independence*, and — critically —
  "**effects consistent with either 'Loewe Additivity' or 'Bliss Independence' would cause two drugs to
  be more effective than one drug, and would be called 'synergistic'**".

That last sentence is the heart of the answer: **in the clinical literature, what this project's model
calls "additivity" is classified as synergy, not as the no-interaction null.** Summing kill rates is
not a conservative default; it is an above-null assumption.

### How much of the single-agent effect is retained in combination — the published numbers

- **Clinical trials.** "The clinically observed benefits for the majority of cancer combination
  therapies we analyzed were indistinguishable from those predicted for independen[t drug action]",
  across melanoma, ovarian, colorectal, pancreatic and breast cancers. Models fitted with explicit
  synergy parameters were ">1000-fold less probable than models of drug independence" by AIC.
- **The measured correlation parameter.** Response correlation across drug pairs in patient-derived
  xenografts: **ρ = 0.28 ± 0.20** for cytotoxic and targeted therapies (from >400 treatment models,
  >2000 animals, 230-277 PDX tumours; "fewer than 10% of biological replicates differed by >1 RECIST
  category"). ρ=0 gives maximal independent-action benefit; "No benefit is predicted at ρ=1.0, which
  corresponds to complete cross-resistance."
- **Diminishing returns in n.** "As the number of drugs in the combination increases, benefit is
  predicted to increase but **with diminishing returns**, consistent with trials showing that more
  intensive combination regimens do not necessarily confer additional benefit." (This is the general
  form of section (b)'s canine saturation.)
- **Combinations cannot be assembled by addition.** "fewer than 5% of combinations of individually
  active drugs were expected to improve PFS when compared to the best observed monotherapy per tumor
  type."

### The exception the project needs to honour — and it is lymphoma

Palmer & Sorger state it explicitly: "**In the case of curable blood cancers, for example,
monotherapies achieve few if any cures whereas multi-agent cure rates are as high as 80%**" — i.e.
true additivity/synergy above independent action **does** occur, and blood cancers are where it occurs.
They also note "A clear exception is childhood acute lymphoblastic leukemia where the benefits of
two-drug combinations were originally explained by independent action", and that the cytotoxic
three-plus-drug regimens are under-studied: "**the absence of data also precludes us from assessing the
relevance of independent action to neo-adjuvant or adjuvant combinations of cytotoxic agents**."

**So the pharmacology gives a two-sided bracket, not a single rule.** For multi-agent cytotoxic therapy
of a lymphoid malignancy the true combined effect lies **between highest-single-agent (α=0) and full
addition (α=1)**, and the literature supplies **no measured α for a CHOP-type cytotoxic combination in
any species**. That is a genuine absence of data, and it is why (e) grades the rule TRANSFERRED and
anchors the duration constraint on canine measurements instead.

### Why combination chemotherapy works, per these sources

Not by summing kill rates. Bozic/Nowak (see (e)) and Komarova & Wodarz both make the benefit
**multiplicative on the resistance axis**: Bozic, "If there is no mutation that could confer
cross-resistance to both drugs simultaneously … [the expected number of resistant cells] **scales with
the square of the point mutation rate**"; for n drugs with no cross-resistance the resistant count is
the product of the per-drug terms. This is Goldie-Coldman logic. Bozic's clinical conclusion: "even if
there is one genetic alteration … that can confer resistance to two targeted agents, therapy with
those agents will not result in sustained benefit", and simultaneous beats sequential dosing
(sequential "fails in 100% of cases" with no cross-resistance, simultaneous "succeeds in >99%").

---

## (d) Canine outcome anchors a corrected model must reproduce

Burden/clearance conventions as in `docs/universe/SWEEP_growth_bar.md`; growth bar g = 0.0903/day
(`lymphoma_grounded.GROWTH_PER_DAY`).

| # | anchor | number | n | source | grade | in record? |
|---|---|---|---|---|---|---|
| **A1** | **Prednisolone alone, median OS** | **50 d** (95% CI 41-59) | **109** | Rassnick 2021 CLASS trial, *JAVMA*, PMID 34125606 | MEASURED, dog | **ALREADY IN RECORD** `SWEEP_growth_bar.md:28` (row B2) |
| **A2** | **Prednisolone's marginal effect ON TOP of a multidrug cytotoxic protocol** | **ZERO** — CR 75%, disease-free period 176 d, rescue CR 45%/133 d, **OS 283 d**, adverse events: all "similar for both groups" | **81**, **prospective randomised** | Zandvliet 2013, *Vet J* 197(3):656-61, PMID 23746872, [DOI](https://doi.org/10.1016/j.tvjl.2013.04.022) | **MEASURED, dog, randomised** | **ALREADY IN RECORD** `SWEEP_regional.md:297` — **but recorded only as a CNS/regional-delivery note ("glucocorticoid adds little systemically"), never connected to the additivity defect.** Connecting it is NEW. |
| **A3** | **Time to clinical prednisolone resistance** | **median 68 d (range 7-348)**; NR3C1-α mRNA fell in **6/6** high-grade cases (p=.031); "resistance develops rapidly and essentially universally" | 7 | PMID 31943234 | MEASURED, dog | **ALREADY IN RECORD** `SWEEP_escapes.md:65` (escape **E1**), `SWEEP_regional.md:65`, `LYMPHOMA_PRIOR_ART_ESCAPES.md:392` |
| **A4** | **Doxorubicin + prednisone (near single-agent), high-grade B-cell** | ORR **84%**; median **PFS 147 d**, **OS 182 d**; **1-year survival 23%** | **33** (31 evaluable) | Al-Nadaf 2018, *BMC Vet Res* 14:356, PMID 30458771, [DOI](https://doi.org/10.1186/s12917-018-1688-5) | MEASURED, dog | **NEW** |
| **A5** | **Single-agent doxorubicin, 3 cycles then nothing, vs COP + maintenance** | **no significant difference** in first-remission length or survival (P>0.05) | **38** vs 67 | Hahn 1992, PMID 1548624, [DOI](https://doi.org/10.1111/j.1939-1676.1992.tb00979.x) | MEASURED, dog | **NEW** |
| **A6** | **Full CHOP, 19-week, median** | CR **89.5%**, **PFS 245 d**, **OS 347 d** | 47 (both arms) | Vos 2019, PMID 31140707, [DOI](https://doi.org/10.1111/vco.12465) | MEASURED, dog | **NEW** |
| **A7** | **Full CHOP, 25-week maintenance-free (UW-25 modified)** | CR **92.3%** (remission 94.2%), **DFI 282 d**, **OS 397 d** | 53 | Garrett 2002, PMID 12465768 | MEASURED, dog | **NEW** |
| **A8** | **CHOP-LAsp 28-week, discontinuous** | **DFR 184 d**, **ST 304 d** | **333** | Lautscham 2017, PMID 28100766 | MEASURED, dog | partly (see (a)) |
| **A9** | **Long-term / "cure" fraction on CHOP-type therapy** | **1-year 39%, 2-year 21%** (discontinuous); **1-year 50%, 2-year 24%** (maintenance). 1-year 23% on doxorubicin+prednisone (A4) | 333 / 75 / 33 | PMID 28100766; PMID 30458771 | MEASURED, dog | **NEW** |
| **A10** | **Relapse/death hazard SHAPE — no plateau by 2 years** | DERIVED from A9's interval survivals: discontinuous **0.00219 → 0.00297 → 0.00170 /day** over 0-6 mo, 6-12 mo, 12-24 mo; maintenance **0.00172 → 0.00207 → 0.00201 /day**. **Essentially flat, ~0.0017-0.0030/day throughout**, with no decline toward zero | 408 | DERIVED from PMID 28100766 | **DERIVED** (arithmetic: h = −ln(S₂/S₁)/Δt) | **NEW** |
| **A11** | **Dose-intensity vs duration trade** | +58% doxorubicin/cyclophosphamide dose intensity with −21% vincristine and 7 fewer weeks = **worse** (PFS 141 vs 245 d, P=0.047) | 47 | Vos 2019, PMID 31140707 | MEASURED, dog | **NEW** |
| **A12** | **Therapy-duration saturation point** | benefit accrues to ~**19-28 weeks (133-196 d)**; **nothing** beyond, up to 730 d | 621 across 4 studies | A6-A8, PMID 1548624, 12465768, 28100766, 31140707 | DERIVED | **NEW** |

**A10 is the hardest constraint and the one a kill-rate model fails most cleanly.** A flat hazard out
to 2 years with ~21-24% still alive and still dying at a constant rate is the signature of a
population in which **no subgroup has been cleared**. A model that reports clearance ("cure") at day
98.7 predicts a survival curve that plateaus; the dogs do not plateau.

---

## (e) The recommended combination rule

### Where the model actually breaks (computed, this sweep)

Run against `lymphoma_grounded.grounded_agents(SYSTEMIC)` with
`escapes_to_close(BURDEN_EARLY_DETECTED)` (12 escapes at burden 1e8):

| agent (CHOP) | potency | duty | `effective_kill` | potency grade |
|---|---|---|---|---|
| doxorubicin | 0.2800 | 0.350 | **0.0980** | REGIMEN-CALIBRATED |
| vincristine | 0.1500 | 0.350 | **0.0525** | REGIMEN-CALIBRATED |
| cyclophosphamide | 0.1200 | 0.350 | **0.0420** | REGIMEN-CALIBRATED |
| prednisolone (glucocorticoid) | 0.1000 | **1.000** | **0.1000** | **BRACKET** |

`kill_against` (`lymphoma_grounded.py:412-413`) sums these. Results:

| regimen / rule | worst margin | weakest escape | model verdict |
|---|---|---|---|
| CHOP, summed (as shipped) | **+0.0517** | P-glycoprotein / ABCB1 efflux | **clears at day 98.7** |
| 3 cytotoxics only, summed | −0.0483 | P-glycoprotein / ABCB1 efflux | never |
| prednisolone only | −0.0903 | TP53 / intrinsic-apoptosis evasion | never |
| **CHOP with prednisolone's kill set to 0** | **−0.0483** | P-glycoprotein / ABCB1 efflux | **never** |
| **CHOP with prednisolone's sustain capped at 68 d (A3)** | +0.0517 | P-glycoprotein / ABCB1 efflux | **never** |

**The binding escape is the P-gp clone, and against it the only agents that reach are prednisolone
(0.1000) and cyclophosphamide (0.0420) — total 0.1420 against g=0.0903.** Doxorubicin and vincristine
are efflux substrates and contribute nothing there. So **71% of the margin that produces "cure" is
prednisolone**, the agent that A2 shows, in a randomised canine trial, can be **deleted from a
multidrug protocol with no change in CR rate, disease-free period, survival or toxicity**.

**Sweep of a graded additivity discount.** Define `k = k_max + α·Σ(rest)`:

| α | 1.00 | 0.75 | 0.50 | 0.35 | 0.25 | 0.10 | 0.00 |
|---|---|---|---|---|---|---|---|
| worst margin | +0.0517 | +0.0412 | +0.0307 | +0.0244 | +0.0202 | +0.0139 | +0.0077 |
| clear day | 98.7 | 98.7 | 98.7 | 98.7 | 98.7 | 99.5 | **never** |

**A discount factor is the wrong instrument.** The verdict is invariant from α=1.0 to α=0.1 and flips
only at α=0 exactly. Any positive margin clears a seeded lineage quickly, so the model is
near-insensitive to the *magnitude* of summed kill and hypersensitive to its *sign* — which is why
calibrating α against outcomes cannot work, and why `LYMPHOMA_STATUS.md:394`'s proposed fix
("calibrating the additivity against the maintenance null") would not have closed this.

### The recommended rule — two parts

**Part 1 (the combination rule). Highest single agent plus a discounted remainder, per escape:**

```
kill_against(agents, escape) = k_max + alpha * sum(k_i for i != argmax)
    where k_i = effective_kill of agents that reach `escape`
          alpha = 0.25   (central), swept over 0.0 - 0.5
```

**Grade: TRANSFERRED.** Written justification for the transfer, as rule 15 requires:

- *What is being transferred:* a **dimensionless retention fraction** on the non-leading agents'
  contribution — not a potency, not an exposure, not a kill rate. No compound's binding, clearance or
  potency is attached to another.
- *Source and direction:* α=0 is the measured clinical null for drug combinations across five tumour
  types (Palmer & Sorger, PMID 29245013; synergy-fitted models >1000x less probable by AIC). α=1 is
  what the code does now, which that paper classifies as **synergy**. The measured PDX response
  correlation **ρ = 0.28 ± 0.20** for cytotoxic/targeted pairs is the quantitative handle; α≈0.25
  sits at that value. **Direction of the species/disease transfer: α=0.25 is a CEILING, not a point
  estimate**, because (i) the source is human and mixed-tumour, and (ii) all four CHOP agents converge
  on the intrinsic apoptosis pathway, so their responses should be *more* correlated (higher ρ, lower
  α) than the cytotoxic/targeted pairs the ρ was measured on. **Offsetting consideration, stated
  because it cuts the other way:** Palmer & Sorger exempt curable blood cancers ("multi-agent cure
  rates are as high as 80%"), so for a lymphoid malignancy α is **not** 0. Hence the sweep 0.0-0.5
  and the use of Part 2, not α, as the load-bearing constraint.
- *What is NOT transferred:* no claim that α=0.25 is measured for CHOP. **No measured α for a
  multi-agent cytotoxic combination exists in any species** — Palmer & Sorger say so explicitly.

**Part 2 (the duration constraint — this is the load-bearing half, and it is MEASURED in dogs).
No agent may be credited beyond the measured onset of its own resistance escape, and prednisolone's
marginal kill in a multidrug protocol is zero.**

```
effective window of agent a = min(profile_for(a).sustainable_days, escape_onset_days(a))
    prednisolone: escape_onset_days = 68      # A3, PMID 31943234, median (range 7-348)
    prednisolone: marginal kill added to a gated multidrug set = 0.0
                                              # A2, PMID 23746872, randomised, n=81
```

**Grade: MEASURED (dog, right disease; A2 randomised).** Currently
`profile_for('prednisolone (glucocorticoid)').sustainable_days = 150.0`, i.e. **2.2x the measured
68-day median time to clinical resistance**, and the clearance day of 98.7 is **1.45x past it**.
Either correction alone flips the verdict to "never clears" (table above).

**Part 3 (a model-level consequence worth recording).** Escape **E1 `gc_receptor_loss`** is enumerated
in the project's own escape audit (`docs/universe/SWEEP_escapes.md:65`) as *exposure-driven, median
68 d*, explicitly defeating "prednisolone (full), prednisolone (maintenance)" — and it is **absent
from both `V1_ESCAPES` (11 escapes) and `GROUNDED_ESCAPES` (14 escapes)**. That omission is the exact
code path by which a non-gated agent gets credited indefinitely. **Adding E1 to `GROUNDED_ESCAPES` is
the minimal structural fix**, and it is a rule-9 catalogue gap: the escape was enumerated in the audit
and never carried into the model. This is **NEW** as a located defect.

### What would falsify the recommended rule

Each of these is decidable, and the first two are the cheap ones:

1. **A2's replication fails.** A second randomised canine trial of a multidrug protocol ± prednisolone
   that shows a **significant** prednisolone benefit would falsify Part 2's zero. Zandvliet 2013 is
   n=81 single-centre with an acknowledged imbalance (substage b 5 vs 14, P=0.015) **against** the
   prednisolone arm — so the true marginal effect could be slightly positive, not zero. A trial
   powered for a 30-day DFP difference would settle it.
2. **A canine lymphoma cohort shows a survival plateau.** A10's flat hazard is the claim that nothing
   is being cleared. A CHOP-type series with ≥3-year follow-up showing the hazard fall toward zero
   after year 2 would falsify it and restore room for a clearance model.
3. **α is measured above 0.5 for a cytotoxic combination.** A dose-response surface for any two CHOP
   agents in canine lymphoma cells or xenografts, analysed by Loewe or Bliss and showing retention of
   the non-leading agent above 50%, would falsify Part 1's ceiling. (In-record canine pairwise data
   exist but point the other way for one pair: bortezomib shows **antagonism with
   4-hydroperoxycyclophosphamide** and synergy with doxorubicin — `SWEEP_modalities.md:94`, PMID
   38237918.)
4. **Prednisolone resistance onset is longer than measured.** A3 is n=7. A larger canine series giving
   a median time to glucocorticoid resistance beyond ~150 days would remove Part 2's cap (though not
   A2's zero).
5. **Part 3 is wrong about the code.** If adding E1 to `GROUNDED_ESCAPES` does **not** change any
   closure claim, then prednisolone was never load-bearing and the computed tables above are wrong.

### Cross-check against the model's own margin arithmetic

Under Part 1 at α=0.25 **and** Part 2, CHOP's P-gp margin becomes
`0.1420 → prednisolone excluded → 0.0420 → 0.0420 − 0.0903 = −0.0483`: **CHOP does not clear.**
That reproduces every anchor in (d): CHOP gives long remissions and ~21-24% 2-year survival with a
flat hazard, not clearance; prednisolone alone gives ~50 days (A1, margin near zero = stable disease,
not cure); and deleting prednisolone from a multidrug protocol changes nothing (A2), because under
the corrected rule it was contributing nothing to begin with.

---

## (f) Does anyone model it this way? — and what rule each known model assumes

**Direct answer to the project's question: no published model sums per-agent kill rates the way
`kill_against` does. All four relevant models use resistance-axis independence with a treated-decline
rate that does NOT scale with the number of drugs.** The project's rule is the outlier.

| model | combination rule it assumes | quantitative detail |
|---|---|---|
| **Bozic et al., *eLife* 2013**, PMID **23805382**, [DOI 10.7554/eLife.00747](https://doi.org/10.7554/eLife.00747) (full text read; the record cites the DOI at `LYMPHOMA_PRIOR_ART_ESCAPES.md:630` but **not the PMID, and not the rule**) | **Strict highest-single-agent.** Quoted from Materials and methods: "During the treatment phase, **all cell types that are sensitive to one or more drugs have birth rate b′ and death rate d′**; fully resistant cells maintain the pretreatment birth and death rates." **A cell sensitive to BOTH drugs declines at exactly the same rate as a cell sensitive to only ONE.** All combination benefit is on the resistance axis. | b=0.14/day (7-day division), d=0.13, net **+0.01/day** pretreatment; treated sensitive cells decline at **b′−d′ = −0.03/day** median (10th-90th pct −0.01 to −0.07), from 68 lesions in 20 vemurafenib-treated melanoma patients; µ≈1e-9; ~50 resistance mutations per drug. Eradication probability given in closed form as a product of four independent no-resistant-lineage probabilities. |
| **Komarova & Wodarz, *PNAS* 2005**, PMID 15980154, [DOI](https://doi.org/10.1073/pnas.0501870102) | Resistance-axis independence; counts independent mutational routes. No kill-rate summation. | "a combination of **three** targeted drugs with different specificities might overcome the problem of resistance"; resistance "arises mainly before the start of treatment". **ALREADY IN RECORD** `LYMPHOMA_PRIOR_ART_ESCAPES.md:627`, `LYMPHOMA_UNIVERSE.md:690` |
| **Saputra et al., *Cancer Res* 2018**, PMID 29686021, [DOI](https://doi.org/10.1158/0008-5472.CAN-17-1201) | Explicit pharmacodynamic interaction term, swept from antagonistic to synergistic **at matched initial efficacy** | "At **equal initial efficacy, antagonistic combinations suppressed singly-resistant clones better than synergistic ones**", because synergistic combinations are "inherently fragile toward the development of single resistance". **ALREADY IN RECORD** `LYMPHOMA_PRIOR_ART_ESCAPES.md:628` |
| **Palmer & Sorger, *Cell* 2017**, PMID 29245013 | **Highest single agent** with a correlation parameter ρ | ρ = **0.28 ± 0.20** measured in PDX; clinical combination outcomes across 5 tumour types indistinguishable from the ρ-parameterised independence prediction; synergy models >1000x less probable by AIC. **NEW** |

**Published kill-rate models fitted to CANINE lymphoma outcomes: none found.** Searched PubMed for
canine lymphoma pharmacodynamic/kill-rate/log-kill modelling; nothing retrieved. The nearest canine
quantitative work in the record is proliferation kinetics, not a treatment-response model
(Larue 1999 PMID 10598945 Tpot 3.4 d; Vail 1996 PMID 8647231 — `SWEEP_growth_bar.md:21-22`).
**So there is no canine precedent to copy, and the honest grade for any canine combination rule is
TRANSFERRED or DERIVED, never MEASURED.** Note that Bozic's own treated-decline rate (−0.03/day for a
human melanoma lesion) is **3.4x smaller** than this model's summed CHOP margin of +0.1022/day against
the gated clones — a useful sanity bound.

---

## Not verified / could not obtain

Stated plainly, per the working agreement:

1. **PMID 28100766's own maintenance doses and dosing intervals.** The *Vet Record* full text is
   paywalled; `bvajournals.onlinelibrary.wiley.com` and `europepmc.org` both returned **HTTP 403**.
   The drug identity (vincristine, chlorambucil, actinomycin-D) and the 2-year total duration are from
   the **PubMed abstract**, which is authoritative for those facts. **The dose-intensity difference
   between the two arms is therefore NOT quantified** — I could not give a ratio. The LMP/DMAC doses
   quoted in (a) are from VIN WSAVA 2005 proceedings for a **different** protocol and are indicative
   only; they must not be attributed to Lautscham. Getting the real numbers needs the PDF.
2. **PMID 28100766's follow-up duration.** Not in the abstract; the 2-year survival rates imply ≥2
   years of follow-up in both cohorts, but the median follow-up is unverified.
3. **Garrett 2002's control-arm maintenance drugs.** The abstract says "a similar protocol with a
   prolonged maintenance phase" without naming the maintenance agents. Not retrieved.
4. **Hahn 1992's medians.** The abstract reports "no significant differences" but gives **no median
   remission or survival figures**, so A5 contributes a null result, not a number.
5. **A measured α (retention of single-agent kill in combination) for any multi-agent cytotoxic
   regimen, in any species.** Does not exist, per Palmer & Sorger's own statement. This is the one
   genuine data absence in this sweep, and Part 1 is graded TRANSFERRED because of it — Part 2 carries
   the weight instead.
6. **A canine lymphoma kill-rate/log-kill model.** None found (see (f)).

## PubMed attribution

Article metadata and full texts in this document were retrieved from **PubMed / PubMed Central**.
DOI links are given inline for every cited article, per PubMed's attribution requirement.
