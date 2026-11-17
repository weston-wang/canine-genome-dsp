# SWEEP_ric_cord_budget (2026-11-16): does reduced-intensity conditioning (2 Gy TBI) free the spinal-cord budget for a full 36 Gy craniospinal course?

**Question.** The B-cell brain/spine closure needs 29-45 intrathecal methotrexate doses, each possibly under general
anaesthesia (the dominant procedural risk). A model run shows that a **36 Gy spinal dose (20 x 1.8 Gy) instead of 23.4 Gy
cuts the requirement to 17-18 doses**. The recorded blocker is spinal-cord tolerance: the program's conditioning TBI
(2 x 4 Gy allo / 2 x 5 Gy auto) already spends 16.2-22.8 Gy3.9 of cord BED, so a full 36 Gy craniospinal field puts the
cord at 82-90% of the 5%-myelopathy level. Would **reduced-intensity conditioning (~2 Gy TBI)** (a) preserve the graft and
the donor anti-lymphoma effect, and (b) free enough cord budget for 36 Gy to the spine?

**Bar (user, verbatim):** "make sure every mechanism and every escape is closed by either real data or **rigorous model**,
potency, toxicity etc all need to be considered"; "I'm not asking if it's been demonstrated, I know it's not."; "I'm okay
with no specific data but if scientifically sound". So a dose limit measured in dogs in another disease, or a GVL figure
transferred from humans, counts **if the transfer is written down**, and is graded TRANSFERRED or DERIVED, never MEASURED.

**Case:** canine high-grade **B-cell** multicentric lymphoma, CNS (brain + spinal CSF) compartment, with a DLA-identical
allogeneic graft in the program. Evidence from T-cell dogs, from other canine diseases (pyruvate-kinase deficiency,
leukocyte adhesion deficiency), from non-tumour-bearing research dogs, and from humans is labelled indirect.

---

## 0. Record check (CLAUDE.md rule 1) -- what was already there, and where

**ALREADY IN RECORD:**
- `SWEEP_hct_model.md:200`, `SWEEP_stemcell.md:139` and `SWEEP_persistent_graft.md:7`: PMID **12931117** (2 Gy TBI +
  sirolimus/cyclosporine, DLA-identical, durable chimerism 5/6 evaluable, median follow-up >48 wk; 1 Gy rejected 5/5),
  with the note "**No dog lymphoma outcome with nonmyeloablative HCT found**". `SWEEP_hct_model.md:204` tiers RIC allo as
  "research / to-build".
- Canine myeloablative lymphoma transplant series: PMID 35789057 (15 B-cell allo, **2 x 4 Gy at 7.5-10 cGy/min**,
  cyclosporine alone to ~d30, chimerism >95% in 12/12 by 2 wk, TRM 13% ITT, acute grade-2 skin GVHD 3/13, no chronic
  GVHD), 24467413 (15 T-cell auto, TBI 10-12 Gy), 34950726 (10 B-cell auto, 10 or 12 Gy), 22882500, 16506937 (allo case,
  2 x 4 Gy, chimerism >=58 wk), 38695516 (7/94 died before discharge) -- `SWEEP_hct_model.md` s1.1-1.2, `SWEEP_stemcell.md` s3.
- Cord: PMID **26366252** (Jin 2015) alpha/beta **3.9 Gy**, BED50 111 Gy3.9, **BED5 83.9 Gy3.9**, D5 55.4 Gy at 2 Gy/fx
  -- `SWEEP_rt2.md:49-50`, used again in `SWEEP_rt3_escalation.md` s3.
- The whole escalation table and the cumulative TBI-plus-brain budget, including "**36 / 20 x 1.8 + TBI 2 x 5 = cord 75.4
  (90% of BED5), which is too close for a 10-year horizon**" -- `SWEEP_rt3_escalation.md` s3-s4. The recommendation there is
  36 Gy to the brain with the spine held at 23.4 Gy.
- The LQ fits and the in-vivo dose-modifying factor 1.9 (PMID 27257868, 3009370); TBI e-folds 2 x 4 Gy = 1.37/1.06/0.62/0.36
  and 2 x 5 Gy = 1.94/1.45/0.89/0.56 -- `SWEEP_stemcell.md:151-154`; `RT_COURSES` in `lymphoma_grounded_inputs.py`.
- The graft-versus-lymphoma transfer set (PMIDs 18684698, 21904377, 20606089, 30467838, 39270145) and the secondary-CNS
  anchor **34293518** (nonmyeloablative Flu/Cy/**200 cGy** TBI + PTCy, n=20, median PFS 3.8 y, relapse 25%, NRM 30%)
  -- `SWEEP_hct_model.md` s3.1, 7.1.
- Human CSI salvage pattern 24 Gy cranial / 15 Gy spinal (16809737) and the paediatric-ALL omission of cranial RT
  (34034929, 19694717, 6110090) -- `SWEEP_rt2.md` Q2.3, `SWEEP_rt3_escalation.md` s1b.
- Canine craniospinal precedent: PMID **6547126** (Couto 1984, 4 dogs, intrathecal cytarabine + craniospinal cobalt,
  **no dose given**) -- `SWEEP_rt2.md`, `SWEEP_rt3_escalation.md` s1d.
- `SWEEP_rt2.md:157-158` (addendum): craniospinal fields in a dog must use 1.8-2 Gy fractions, not the canine 4 Gy standard.

**NEW in this sweep (every PMID below grep-checked against `docs/` and `src/`; none returned a hit):**
9108426, 10419907, 12931117-successors 17369487 and 17241922, 11215693, 16906030, 23994246, 15316362, 12963272, 12842608
(canine RIC platform); **9572623** (the direct canine spinal-cord tolerance measurement, 89+36 beagles); 11678571
(radiation-induced canine vertebral osteosarcoma); 38244173, 36845621 (human craniospinal-plus-transplant); 37788792,
12430851, 17325892, 18246114 (human 2 Gy vs higher-intensity conditioning in NHL); 24858425, 22592050, 36263219
(marrow dose with graft rescue).

**Defect found in the record while doing this (not a gap, a unit error to fix):** the record uses **two different
in-vivo corrections**. `SWEEP_stemcell.md:151-154` applies the dose-modifying factor to the **dose** (D/1.9 then LQ), which
reproduces its 1.37/1.06/0.62/0.36 exactly; `SWEEP_rt3_escalation.md` s3 and `lymphoma_sustained.rt_efolds_in_vivo`
divide the **e-folds** by 1.9. The two differ by ~30-50%, so subtracting a TBI figure from one convention from a
craniospinal figure in the other -- which is exactly what the "net trade" in this question asks for -- is invalid.
Section 4 below computes the trade **twice, once in each convention**, and no number is mixed across them.

---

## 1. Q1: the canine nonmyeloablative / reduced-intensity DLA-identical platform

All of this is the Fred Hutch (Storb) canine model, in **healthy research dogs** unless stated. According to PubMed:

### 1a. The established regimen

| element | value | source |
|---|---|---|
| TBI dose | **200 cGy** single exposure, day 0, marrow infused within 4 h | 9108426, 23994246 ([DOI](https://doi.org/10.1016/j.bbmt.2013.08.007)) |
| dose rate | **7 cGy/min** ("the traditional" rate); 70 cGy/min tested and gave **no engraftment advantage** and no extra haematotoxicity | 23994246 |
| delivery | linear accelerator, opposed fields, dog repositioned midway, so the 2 Gy arrives as two ~1 Gy halves | 23994246 |
| graft | DLA-identical littermate marrow, median **4.3 (2.2-6.4) x 10^8 nucleated cells/kg** | 23994246 |
| post-graft immunosuppression | **MMF 10 mg/kg BID SC days 0-28 + CSP 15 mg/kg BID days -1 to +35**; sirolimus/CSP is equally effective | 9108426, 12931117 ([DOI](https://doi.org/10.1016/s1083-8791(03)00148-4)), 23994246 |

### 1b. Engraftment is a steep function of TBI dose, and **cyclosporine alone fails at 2 Gy**

| TBI | post-graft immunosuppression | durable engraftment | source |
|---|---|---|---|
| **200 cGy** | CSP **alone** | **0** -- transient mixed chimerism "for no more than 4 weeks" | 9108426 (group 1) |
| 200 cGy | MTX + CSP | 3/6 stable to 60 wk (3/6 transient 3-11 wk) | 9108426 (group 2) |
| **200 cGy** | **MMF + CSP** | **4/5 stable 54-57 wk** | 9108426 (group 3) |
| **200 cGy** | **SRL + CSP** | **5/6 evaluable durable, median follow-up >48 wk (>32 to >56)**; 1 died d21 of haemorrhagic pneumonitis; the 1 rejecter kept donor-specific tolerance (skin graft not rejected) | 12931117 |
| **200 cGy, pooled** | MMF/CSP or SRL/CSP | **8/10 (80%) stable long-term** | 23994246 |
| 200 cGy, 70 cGy/min | MMF/CSP | 3/6 stable | 23994246 |
| 150 cGy | MMF/CSP | 3/6 (50%) at 7 cGy/min; 3/8 (38%) at 70 cGy/min | 23994246 |
| 100 cGy | MMF/CSP or SRL/CSP | **0/11** historical + 0/n study; all rejected 2-17 wk | 9108426, 12931117, 23994246, 17241922 |
| 0 Gy | MMF/CSP | 0 -- all rejected 2-12 wk | 9108426 (group 5) |
| 100 cGy + anti-CD154 + donor PBMC | MMF/CSP | 3/6 sustained >26 wk (p=.03 vs 11 historical 1 Gy controls) | 17241922 ([DOI](https://doi.org/10.1016/j.bbmt.2006.10.031)) |
| **Bi-213-anti-CD45 or -TCRab RIT, NO TBI** | MMF/CSP | stable >30 wk in all evaluable dogs at 1.4-2.1 mCi/kg (anti-CD45) or 2.0-2.7 (anti-TCRab); <1.3 mCi/kg all rejected; **"No signs of graft-versus-host disease or other toxicities"**; transient LFT rise 4/15 | 15316362 ([DOI](https://doi.org/10.1097/01.tp.0000128853.62545.b2)) |

"Engraftment success is linear for TBI doses at 200 cGy and lower regardless of dose rate" (23994246). **Consequence for
the program: 2 Gy is the floor, not a free parameter**, and the program's current cyclosporine-only post-graft regimen
(35789057) would have to gain MMF or sirolimus. That is not an optional refinement: at 2 Gy with CSP alone the record's own
source shows 0/n durable engraftment.

### 1c. What 2 Gy conditioning does NOT do: it does not make marrow space

Storb 1999 (PMID **10419907**) irradiated cervical/thoracic/abdominal **lymph nodes only** (pelvis spared) instead of TBI:
450 cGy to nodes gave 3/6 long-term mixed chimeras at 57-97 wk, and **mixed chimerism appeared in non-irradiated marrow
and lymph-node spaces**. Conclusion in the paper: "pretransplant radiation provides **host immunosuppression**, and grafts
can create their own marrow space." This matters twice below: (i) irradiating the spinal marrow is not a prerequisite for
engraftment, and (ii) a craniospinal field, which covers cervical nodes and a large lymphoid volume, is itself
immunosuppressive and works in the same direction as the conditioning.

### 1d. GVHD and transplant-related mortality at 2 Gy vs myeloablative

| setting | GVHD | mortality | source |
|---|---|---|---|
| 2 Gy, DLA-identical, MMF/CSP or SRL/CSP, healthy dogs | no GVHD reported in any of the 2 Gy DLA-identical series read here (9108426, 12931117, 23994246, 17369487); 1 GVHD death in the 450 cGy **lymph-node** arm | 1 death/7 at 2 Gy (haemorrhagic pneumonitis d21, 12931117) | as listed |
| No-TBI RIT conditioning, DLA-identical, MMF/CSP | **"No signs of graft-versus-host disease"**, n=15 | 0 | 15316362 |
| 2 Gy, DLA-**haplo**identical + anti-CD44 | rejection 25/44 (57%) at median 7 wk | - | 16906030 ([DOI](https://doi.org/10.1097/01.tp.0000228908.10775.b0)) |
| **4.5 Gy**, DLA-identical, **CSP alone** | **fatal GVHD** from day 52, recurred after steroid taper, dog euthanised | 1/1 | Schaefer case, quoted in the Graves & Storb review 34390541 ([DOI](https://doi.org/10.1002/vms3.601)), which states MMF/MTX/sirolimus with CSP "might have prevented" it |
| 9.2 Gy, DLA-identical G-PBMC, **no** post-graft immunosuppression | **3/9 fatal GVHD** | 3/9 | Sandmaier, quoted in 34390541 |
| 2 x 4 Gy, DLA-identical, CSP alone, **15 lymphoma dogs** (the program's own series) | acute grade-2 skin 3/13 (23%), none grade >=3, chronic 0/13 | TRM 2/15 = 13% ITT; 0/10 TBI-toxicity deaths in first-remission dogs | 35789057, ALREADY IN RECORD |
| 10-12 Gy auto, canine lymphoma | n/a (autologous) | 7/94 = 7.4% before discharge | 38695516, ALREADY IN RECORD |

Review statement, directly on the point: "In the DLA-matched littermate HCT setting, **development of GVHD is less common,
especially when post-grafting immunosuppression is employed**" (34390541). Reading: at 2 Gy with a DLA-identical graft and
two-drug post-graft immunosuppression, GVHD is rare in dogs and TRM is dominated by single non-GVHD events in small series;
nothing read here suggests RIC raises GVHD, and the human comparison in s1f says it lowers it.

### 1e. Canine disease-model (non-tumour) outcomes at 2 Gy -- the only canine RIC outcomes that exist

| disease | n | result | source |
|---|---|---|---|
| Pyruvate-kinase-deficiency haemolytic anaemia (Basenji), 200 cGy + MMF/CSP, DLA-identical | 5 | all engrafted initially; 2 rejected at 6 wk, 1 died d27 liver failure with 60% donor; **2 sustained >1 y at 85% and 12% donor**. Clinical response **tracked the degree of chimerism**: 85% donor = near-complete resolution; 12% donor = partial only. "Complete donor chimerism appears necessary to achieve a long-term cure." | 11215693 ([DOI](https://doi.org/10.1053/bbmt.2001.v7.pm11215693)) |
| Canine leukocyte adhesion deficiency, non-myeloablative DLA-identical marrow | small series | stable **mixed** chimerism reversed the disease phenotype; >2% donor leukocytes sufficed for that phenotype | 12963272 ([DOI](https://doi.org/10.1016/s0165-2427(03)00108-9)), 12842608 |
| Trichimerism: 2 Gy + marrow from **two** DLA-identical donors | 8 | 5/8 sustained trichimerism, 2 rejected one graft, 1 rejected both; normal immune function in the tested dog; 4/5 later kidney grafts surviving drug-free | 17369487 ([DOI](https://doi.org/10.1182/blood-2007-02-071282)) |

**The dose-response of benefit on donor chimerism (11215693) is the single most important caveat for this proposal** and is
developed in s6.

### 1f. Does graft-versus-tumour survive at 2 Gy? Canine: NOT MEASURED. Human: MEASURED, and the answer is yes.

- **Canine GVT is documented, but only at myeloablative doses.** Review 34390541: dogs given an **allograft** after 9.2 Gy
  TBI were tumour-free at autopsy in **88%** of >14-day survivors versus **12%** for autografts after the same 9.2 Gy
  (Weiden) -- i.e. canine GVT is real and large, at 9.2 Gy. The same review: "The conditioning doses for external beam TBI
  followed by HCT reported for dogs with leukaemia/lymphoma ranged between **8.0 and 12.0 Gy**", and the less-intensive
  regimens "relied less on the effectiveness of the conditioning regimen to reduce the tumour burden but, rather, **on GVT
  effects for eradicating malignant cells**."
- **Canine tumour outcome with 2 Gy conditioning: NOT FOUND.** Confirmed independently of the record this session by four
  PubMed queries (dogs x nonmyeloablative x lymphoma/leukaemia/tumour/2 Gy; dogs x reduced-intensity x remission). The
  record's statement at `SWEEP_stemcell.md:139` stands.
- **Human measurement that the 2 Gy step does not cost disease control in NHL** -- this is the transfer that closes the
  question. PMID **37788792** (Nath 2024, Transplant Cell Ther 30:81, [DOI](https://doi.org/10.1016/j.jtct.2023.09.022)),
  n=279 NHL allografts, median follow-up 64 months: **nonmyeloablative Flu-Cy-2Gy-TBI (n=169) versus reduced-intensity
  regimens including Flu-Cy-thiotepa-4Gy-TBI and Flu-Mel (n=110)** gave **no difference in overall survival** (median not
  reached vs 103 months, P=.1) and **no difference in PFS** (adjusted HR 1.38, 95% CI 0.92-2.09, P=.24), while the more
  intensive arm had **higher non-relapse mortality** (adjusted HR 2.61, 95% CI 1.04-6.52, P=.039) and more acute GVHD
  (grade II-IV HR 2.25; grade III-IV HR 5.62). Authors' conclusion: "NMA conditioning with Flu-Cy-TBI-2Gy **may be
  considered over more intensive RIC regimens** for patients with NHL undergoing allo-HCT." Grade: **MEASURED (human)**,
  **TRANSFERRED** to the dog.
- Supporting human 2 Gy TBI platform numbers: PMID 12430851 (Fred Hutch multicentre, 192 related 2 Gy TBI +/- fludarabine:
  non-fatal graft rejection 6.8%, acute GVHD 49%, **day-100 non-relapse mortality 6%**, 2-y OS 50% / PFS 40%; NHL n=31);
  PMID 18246114 (first 100 Danish 2 Gy TBI transplants: NHL and CLL among the **favourable** histologies at PFS 61-71%);
  PMID 17325892 (25 patients, flu + 2 Gy TBI: all engrafted; **full-donor chimerism at day 30 predicted lower relapse**).
- And the record's own CNS anchor is already a **2 Gy** regimen: PMID 34293518, secondary CNS lymphoma, Flu/Cy/**200 cGy**
  TBI + post-transplant cyclophosphamide, median PFS 3.8 y, relapse 25% at 4 y. The model's CNS graft access (0.5) was
  derived from this series, so **the model's CNS allograft input was already calibrated on 2 Gy conditioning, not on
  2 x 4/2 x 5 Gy.** Lowering the program's TBI to 2 Gy brings the program *closer* to the regimen its CNS number came from.

---

## 2. Q2: spinal-cord radiation tolerance in the dog, and the arithmetic

### 2a. The primary canine measurement (NEW to the record -- the record had only the pooled cross-species fit)

**PMID 9572623** (Powers, Thames, Gillette, Gillette 1998, Radiother Oncol 46:297-306,
[DOI](https://doi.org/10.1016/s0167-8140(97)00213-2)). **89 beagles** given 44-84 Gy in **4 Gy fractions** to a **4 cm or
20 cm length of thoracic cord**, plus **36 beagles** given 60-84 Gy in **2 Gy fractions** to a **20 cm** length, plus 6
unirradiated:

| endpoint, 4 Gy/fx | ED50 (95% CI) | cord BED (a/b 3.9) | cord BED (a/b 2) |
|---|---|---|---|
| severe lesions, **20 cm** field | **56.9 Gy (53.1-60.6)** | 115.3 Gy3.9 | 170.7 Gy2 |
| severe lesions, 4 cm field | 68.8 Gy (64.5-75.1) | 139.4 Gy3.9 | 206.4 Gy2 |
| **clinical signs, 20 cm** field | **54.0 Gy** | **109.4 Gy3.9** | 162.0 Gy2 |
| clinical signs, 4 cm field | 77.6 Gy | - | - |
| volume effect, 4 vs 20 cm | **8.3-15.0 Gy at the ED50 level**, and the curves stay apart at low injury probability | | |

**Cross-check that validates the record's cord limit.** Jin 2015 (PMID 26366252, in record) puts **BED50 = 111 Gy3.9**
from a pooled rat + large-animal + patient fit. The direct canine **clinical-signs** ED50 for a long (20 cm) field is
**109.4 Gy3.9** -- within **1.5%**. So the record's **BED5 = 83.9 Gy3.9** is not merely a cross-species import; it sits on a
curve whose D50 reproduces the canine measurement for a craniospinal-length field. Grade: **DERIVED**, with a canine
MEASURED anchor at the D50 level.

At 1.8 Gy/fx, BED5 = 83.9 Gy3.9 corresponds to **D5 = 83.9 / (1 + 1.8/3.9) = 57.4 Gy**.

### 2b. Cord-budget arithmetic for every conditioning / craniospinal combination

Formulae: cord BED = sum over courses of D(1 + d/(a/b)); "EUD at 1.8 Gy/fx" = BED3.9 / 1.4615, comparable with D5 = 57.4 Gy;
BED2 and EQD2(2) given as the conservative sensitivity the question asked for. TBI 2 Gy is treated as **one 2 Gy fraction**
(it is one exposure, split only for repositioning, 23994246).

| conditioning | spinal field | **cord BED3.9** | **% of BED5 (83.9)** | equiv. dose at 1.8 Gy/fx (vs D5 57.4) | cord BED2 | EQD2(2) |
|---|---|---|---|---|---|---|
| **2 Gy x 1 (RIC)** | none | 3.0 | **4%** | 2.1 | 4.0 | 2.0 |
| **2 Gy x 1 (RIC)** | 23.4 / 13 x 1.8 | 37.2 | **44%** | 25.5 | 48.5 | 24.2 |
| **2 Gy x 1 (RIC)** | 30.6 / 17 x 1.8 | 47.7 | **57%** | 32.7 | 62.1 | 31.1 |
| **2 Gy x 1 (RIC)** | **36 / 20 x 1.8** | **55.6** | **66%** | **38.1** | 72.4 | 36.2 |
| 2 Gy x 1 (RIC) | 39.6 / 22 x 1.8 | 60.9 | 73% | 41.7 | 79.2 | 39.6 |
| 2 Gy x 1 (RIC) | 45 / 25 x 1.8 | 68.8 | 82% | 47.1 | 89.5 | 44.8 |
| 2 x 4 Gy (program allo) | none | 16.2 | 19% | 11.1 | 24.0 | 12.0 |
| 2 x 4 Gy | 23.4 / 13 x 1.8 | 50.4 | 60% | 34.5 | 68.5 | 34.2 |
| 2 x 4 Gy | **36 / 20 x 1.8** | 68.8 | **82%** | 47.1 | 92.4 | 46.2 |
| 2 x 4 Gy | 45 / 25 x 1.8 | 82.0 | 98% | 56.1 | 109.5 | 54.8 |
| 2 x 5 Gy (`RT_COURSES`) | none | 22.8 | **27%** | 15.6 | 35.0 | 17.5 |
| 2 x 5 Gy | 23.4 / 13 x 1.8 | 57.0 | 68% | 39.0 | 79.5 | 39.7 |
| 2 x 5 Gy | **36 / 20 x 1.8** | **75.4** | **90%** | 51.6 | 103.4 | 51.7 |
| 2 x 5 Gy | 39.6 / 22 x 1.8 | 80.7 | 96% | 55.2 | 110.2 | 55.1 |
| 2 x 5 Gy | 45 / 25 x 1.8 | 88.6 | **106%** | 60.6 | 120.5 | 60.2 |

The 27% and 90% figures reproduce the recorded blocker exactly (`SWEEP_rt3_escalation.md` s3), so this table is the same
arithmetic with the conditioning varied, not a new model.

**What RIC buys on the cord, stated plainly:** dropping conditioning from 2 x 5 Gy to one 2 Gy fraction removes
**22.8 - 3.0 = 19.8 Gy3.9** of cord BED, i.e. **24 percentage points of BED5**. That takes the 36 Gy craniospinal
combination from **90% to 66%** of the 5%-myelopathy level -- from the figure the record rejected as "too close for a
10-year horizon" to a figure **below** the 68% that the record already accepts today (2 x 5 Gy + 23.4 Gy). From 2 x 4 Gy
the saving is 13.2 Gy3.9 (16 points), taking 36 Gy from 82% to 66%.

**Two reasons the 66% figure is a ceiling (errs safe):**
1. Jin's fit **excluded** studies with dose rate <0.1 Gy/min. The canine RIC TBI is given at **0.07 Gy/min** (7 cGy/min),
   below that threshold, where sublethal repair during delivery removes part of the quadratic term. The 3.0 Gy3.9 charged
   to the 2 Gy TBI is therefore an over-estimate of its late-cord cost.
2. The 2 Gy is delivered as two opposed ~1 Gy halves (23994246); charging it as a single 2 Gy fraction maximises its BED.

**Two reasons it could be optimistic:**
1. **Volume.** Powers' field was 20 cm. A canine craniospinal field covers the **whole cord**, which in a medium-to-large
   dog is longer than 20 cm, and Powers measured a 8.3-15.0 Gy ED50 penalty going from 4 cm to 20 cm, with the curves still
   separated at low injury probability. **Tolerance for a cord length beyond 20 cm has not been measured in any species
   retrieved here (NOT FOUND).** The 20-cm number is the longest canine field on record and is used as the anchor; the
   residual extrapolation is written down rather than assumed away.
2. **Latency.** Human radiation myelopathy latency is bimodal at ~9 and ~26 months (26366252). Powers' follow-up length is
   not in the abstract (UNVERIFIED, no full text retrieved). On a 10-year canine horizon the late peak is inside the window.

---

## 3. Q3: is the marrow the other binding constraint?

A craniospinal field irradiates vertebral marrow. In humans the vertebrae hold roughly **28%** of adult active marrow and
the cranium ~13% (Ellis-based tables; secondary web source, not a primary citation -- the equivalent **canine** active-marrow
distribution was **NOT FOUND**). So a craniospinal field puts a marrow-ablative dose on order 40% of the marrow volume.

**With a graft, the marrow does not bind, and the precedent is measured in humans on the 2 Gy TBI platform itself:**

- **PMID 24858425** (Mawad 2014, BBMT 20:1363, [DOI](https://doi.org/10.1016/j.bbmt.2014.05.014)). 15 patients given
  **iodine-131-anti-CD45 antibody plus fludarabine and 2 Gy TBI** before allografting. Delivered **an average of 27 Gy to
  bone marrow** (84 Gy to spleen, 21 Gy to liver), with marrow doses "arbitrarily capped at 43 Gy to avoid
  radiation-induced stromal damage; **however, no graft failure or evidence of stromal damage was observed**", and the
  authors conclude "the arbitrary limit of 43 Gy to the marrow may be unnecessarily conservative." That is **27-43 Gy to
  marrow on top of 2 Gy TBI with an allograft, with no graft failure** -- which brackets a 36 Gy spinal marrow dose on the
  identical conditioning platform. Grade: **MEASURED (human), TRANSFERRED** to the dog.
- **PMID 22592050 / 36263219** (City of Hope total marrow / total marrow-and-lymphoid irradiation): 12-20 Gy at 1.5-2.0 Gy
  twice daily to the whole skeleton with allografting; "**engraftment in all patients** and a low incidence of radiation
  related toxicities"; dose escalated to 15-20 Gy with acceptable toxicity. So deliberately irradiating all marrow at
  transplant-level doses with graft rescue is routine practice, not a hazard to be modelled.
- **Mechanistic reason the irradiated spinal marrow does not have to recover:** at 2 Gy the conditioning works by host
  immunosuppression, not by emptying marrow space -- "grafts can create their own marrow space", and mixed chimerism
  appeared in non-irradiated marrow spaces when only lymph nodes were irradiated (10419907). Marrow is also a parallel
  organ; pelvis, ribs/sternum and long bones are outside a craniospinal field.

**Sequencing implication: craniospinal radiation goes BEFORE the graft, never after.** Reasons, in order of force:
1. **Human precedent does it that way.** PMID **38244173** (Ebadi 2024, J Neurooncol 166:351,
   [DOI](https://doi.org/10.1007/s11060-023-04501-5)): 39 leukaemia patients had CSI for CNS involvement (median **18 Gy
   brain / 12 Gy spine**); **25 (64%) received CSI immediately prior to allogeneic HCT, of which 21 (84%) then had TBI
   conditioning at a median of 12 Gy**. CSF blast clearance 14/14 assessed (100%) at a median 23 days; 2-y CNS local
   recurrence 14% (5-28%); **"No grade 3 or higher acute toxicity was seen during CSI."** This is the direct precedent for
   craniospinal irradiation stacked on transplant conditioning, and it puts the CSI first.
2. After a 2 Gy graft the recipient is a **stable mixed chimera**; 36 Gy to 40% of the marrow at that point would ablate
   engrafted donor haematopoiesis in-field with no second graft available, and the 2 Gy regimen has no cryopreserved
   autologous back-up in the protocol.
3. Cost of putting it first: 20 fractions at 1.8 Gy is ~4 weeks of elapsed time before conditioning, during which
   systemic lymphoma regrows at the model's growth bar (0.0903/day gross). Mitigation is to keep the dog on its CHOP
   backbone through the radiation course, which is what the human series do; the overlap of craniospinal radiation with
   systemic chemotherapy raises mucositis (PMID 37401225: prior CSI associated with 100% vs 70.2% mucositis in transplant
   recipients, p=.01) but that is a supportive-care cost, not a closure failure.

**Canine craniospinal-plus-transplant precedent: NOT FOUND.** The only canine craniospinal report is still Couto 1984
(PMID 6547126, 4 dogs, no dose), and it had no transplant. So item 3 is **TRANSFERRED (human, n=25 in the CSI-then-allograft
subset)**, not MEASURED in dogs.

---

## 4. Q4: does the lower TBI cost tumour kill? The net trade, computed in both of the record's conventions

LQ parameters from `lymphoma_grounded_inputs.lq_alpha_beta` on the measured canine lymphoid-line SF2/SF5 (PMID 27257868):
CLBL1 a=0.1539 b=0.0817; OSW a=0.1590 b=0.0441; 1771 a=0.0652 b=0.0393; CLL1390 a=0 b=0.0406.

**Convention B -- dose/1.9 then LQ** (the convention of `SWEEP_stemcell.md:151-154`, which is the one the question quotes;
it reproduces the recorded 2 x 4 Gy row exactly):

| schedule | CLBL1 | OSW (T) | 1771 (median) | CLL1390 (resistant) |
|---|---|---|---|---|
| **TBI 1 x 2 Gy (RIC)** | **0.25** | **0.22** | **0.11** | **0.05** |
| TBI 2 x 4 Gy (record: 1.37/1.06/0.62/0.36) | 1.37 | 1.06 | 0.62 | 0.36 |
| TBI 2 x 5 Gy (record: 1.94/1.45/0.89/0.56) | 1.94 | 1.45 | 0.89 | 0.56 |
| CSI 23.4 / 13 x 1.8 | 2.85 | 2.47 | 1.26 | 0.47 |
| CSI 36 / 20 x 1.8 | 4.38 | 3.80 | 1.94 | 0.73 |

**Convention A -- e-folds/1.9** (the convention of `SWEEP_rt3_escalation.md` s3 and `lymphoma_sustained`, which is the one
the "+25% cuts 34 doses to 18" model run was expressed in; it reproduces the recorded 23.4 Gy row 3.71/2.94/1.67/0.90):

| schedule | CLBL1 | OSW (T) | 1771 (median) | CLL1390 (resistant) |
|---|---|---|---|---|
| **TBI 1 x 2 Gy (RIC)** | **0.33** | **0.26** | **0.15** | **0.09** |
| TBI 2 x 4 Gy | 2.02 | 1.41 | 0.94 | 0.68 |
| TBI 2 x 5 Gy | 2.96 | 2.00 | 1.38 | 1.07 |
| CSI 23.4 / 13 x 1.8 (record) | 3.71 | 2.94 | 1.67 | 0.90 |
| CSI 36 / 20 x 1.8 (record) | 5.70 | 4.52 | 2.58 | 1.39 |

Worked example (convention A, line 1771, 2 Gy TBI): e-folds = 1 x (0.0652 x 2 + 0.0393 x 4) = 0.1304 + 0.1572 = 0.288
in vitro, / 1.9 = **0.15 in vivo**. Convention B: dose 2/1.9 = 1.0526 Gy, e-folds = 0.0652 x 1.0526 + 0.0393 x 1.108 =
0.0686 + 0.0435 = **0.11**.

**The net trade, in the CNS compartment** (where the model credits TBI brain access at 1.0, `SWEEP_hct_model.md:263`, so
the compartment genuinely sees both courses). Net = (CSI 36 - CSI 23.4) - (TBI_high - TBI_2Gy):

| line | conv. A: gain from spine | loss vs 2 x 4 | **net** | loss vs 2 x 5 | **net** | conv. B net vs 2 x 4 | conv. B net vs 2 x 5 |
|---|---|---|---|---|---|---|---|
| CLBL1 (sensitive B) | +2.00 | 1.69 | **+0.31** | 2.63 | **-0.63** | **+0.41** | -0.16 |
| OSW (T-cell) | +1.58 | 1.15 | **+0.43** | 1.74 | **-0.16** | **+0.49** | +0.10 |
| 1771 (median) | +0.90 | 0.79 | **+0.12** | 1.23 | **-0.33** | **+0.17** | -0.10 |
| CLL1390 (resistant) | +0.48 | 0.60 | **-0.11** | 0.98 | **-0.50** | -0.06 | -0.26 |

**Reading of the net, stated at the strength shown:**
- Against the program's **allogeneic** conditioning (2 x 4 Gy -- the dose the 15-dog B-cell series actually used,
  35789057), the swap is **net positive or neutral in the CNS compartment for three of four lines in both conventions**
  (+0.12 to +0.49 e-folds), and **net slightly negative only for the most resistant line** (-0.06 to -0.11). Against the
  **autologous** 2 x 5 Gy in `RT_COURSES` it is net negative by 0.1-0.6 e-folds. The program's allograft arm is the one at
  issue, so **the relevant comparison is the 2 x 4 Gy row, and there the LQ trade is a wash to a small gain.**
- **This LQ bookkeeping is the weakest part of the case and should not carry it.** The record already contains the reason:
  TBI dose escalation from 8.4 to 13.5 Gy, 10 to 12 Gy and 10 to 11 Gy produced **no reduction in relapse** while TRM rose
  (3887690, 3901841, 34950726 p=.296, 24467413 p=.7665) although LQ predicts +5 to +11 e-folds across that range
  (`SWEEP_stemcell.md:160`). If LQ over-predicts the benefit of *raising* TBI, it also over-predicts the cost of
  *lowering* it. On outcomes rather than LQ: **allo-HCT at 2 x 4 Gy gave far fewer relapses than auto at 10-12 Gy**
  (`SWEEP_stemcell.md:20`), and in humans the 2 Gy versus 4 Gy / melphalan comparison in 279 NHL allografts showed **no
  PFS difference and lower NRM** (37788792). The conditioning pulse is not what carries durability in either species.
- **Systemic compartment.** Lowering TBI loses 0.4-1.9 e-folds systemically with nothing added back (the craniospinal field
  is CNS-only). That loss is covered by the graft: the record's OUTCOME-calibrated allograft effect is **2.6 e-folds
  (0.65-4.2)** over a 166-day window (`SWEEP_hct_model.md` s2.5, s9), which is larger than the entire TBI pulse at any dose
  tested, and the human NHL data say the conditioning step is not where the PFS comes from.
- **Second-order gains that are not in the LQ arithmetic and all point the same way:** TRM falls (canine 2 x 4/2 x 5 Gy TRM
  13% ITT and 7.4%; human day-100 NRM 6% at 2 Gy, 12430851; RIC-vs-NMA adjusted NRM HR 2.61 against the more intensive arm,
  37788792); GVHD falls (grade III-IV HR 5.62 against the more intensive arm, 37788792); and TBI-driven second-cancer risk
  falls (radiation chimeras at 6.1-21.3 Gy had ~5x malignancy risk, PMID 6355021 in record) -- which matters on a 10-year
  horizon more than one e-fold of conditioning does.

**Anaesthesia arithmetic -- the quantity the question is actually trying to buy down.** Canine radiation fractions and
intrathecal injections both need general anaesthesia; at the record's 0.1-0.5% per-event mortality
(`SWEEP_rt3_escalation.md` s4), compounded as 1-(1-p)^n:

| plan | RT fractions | IT doses | total anaesthetic events | cumulative mortality 0.1% / 0.5% per event |
|---|---|---|---|---|
| current (23.4 Gy spine, 29-45 IT) | 13 | 29-45 | 42-58 | 4.1-5.6% / 19.0-25.2% |
| current, central (34 IT) | 13 | 34 | 47 | 4.6% / 21.0% |
| **proposed (36 Gy spine, 17-18 IT)** | **20** | **17-18** | **37-38** | **3.6-3.7% / 16.9-17.3%** |

So the 7 extra fractions are more than paid for: **~37 events instead of ~47, about 20% fewer anaesthetics**, and the
methotrexate dose count -- the one variable with a measured dose-dependent leukoencephalopathy hazard (HR 4.50, PMID
39269476 in record) -- is halved. That is the real return on the trade, and it is larger than the e-fold bookkeeping.

---

## 5. Q5: alternatives that spare the cord -- is a spinal field needed at all?

1. **Human practice reduced or dropped the spinal field, and the relapse data support that.**
   - PMID **36845621** (Patel 2022, Adv Radiat Oncol 8:101082, [DOI](https://doi.org/10.1016/j.adro.2022.101082)): 115
     adult ALL allografts on TBI-based conditioning. Among the 100 **without** CNS disease, 76% had peri-transplant
     intrathecal chemotherapy (median 4 cycles) and only 10 got a CNS radiation boost; **only 4 failed in the CNS, all
     of them among the un-boosted, 5-y freedom from CNS relapse 95% (84-98%)**, and the boost did **not** improve it
     (100% vs 94%, P=.59). Among the 10 **with** CNS disease, 7 got a boost (6 craniospinal) and **none** subsequently
     failed in the CNS. Authors: "A CNS boost may not be necessary in patients with high-risk ALL **without** CNS disease...
     Favorable outcomes were observed with a **low-dose craniospinal boost in patients with CNS disease**."
   - PMID **38244173** (above): where CSI *is* given before transplant, the spine gets **12 Gy**, not 36.
   - Human ALL salvage CSI is 24 Gy cranial / **15 Gy spinal** (16809737, in record), i.e. the spine is deliberately
     under-dosed relative to the brain.
   - Paediatric ALL removed cranial irradiation altogether and held CNS relapse at 1.5-3.9% on intrathecal therapy alone
     across >10,000 children (ALREADY IN RECORD, `SWEEP_rt2.md` Q2.3).
   - PCNSL: the NCI PDQ physician summary retrieved this session does **not** discuss spinal-axis radiation at all and
     gives no survival data for adding it; its only radiation discussion is whole-brain. A pooled spinal-relapse rate after
     whole-brain radiotherapy in PCNSL was **NOT FOUND**.
   - **Consequence for this proposal, stated honestly:** the human evidence says a high-dose spinal field is *not required*
     when intrathecal therapy is given -- which is the opposite direction from what the model wants, since the model's
     reason for 36 Gy to the spine is precisely to **cut** the intrathecal dose count. What the human evidence does
     establish is that **the spinal dose is a free design parameter anywhere from 0 to 36 Gy**: no human standard forbids
     either end, 12-15 Gy is the common choice, and the model is entitled to pick the end that minimises its own dominant
     risk (anaesthesia events) provided the cord budget holds. It also means a **split field** (36 Gy brain / 23.4 Gy
     spine, the current `SWEEP_rt3` recommendation) sits at only **44% of BED5** with 2 Gy conditioning -- very comfortable
     -- if a lower spinal dose turns out to be enough.
2. **Replace the TBI entirely and the cord pays nothing.** PMID **15316362**: Bi-213 coupled to anti-CD45 or anti-TCRab
   gave stable DLA-identical engraftment >30 weeks in dogs **with no external-beam TBI at all**, at 2 mCi/kg, with "no
   signs of graft-versus-host disease or other toxicities" and only transient LFT rises in 4/15. Radioimmunotherapy
   conditioning deposits dose on marrow and lymphoid tissue, not on cord, so it frees the **entire** 83.9 Gy3.9 budget for
   the craniospinal field (36 Gy = 63%, 45 Gy = 78%). First evaluated in dogs and since taken into human phase I-II
   (34390541). Tier under CLAUDE.md rule 13: **NEAR-FUTURE / to-build** -- it is a research radioconjugate, not an
   off-label product a specialty practice can order. Recorded here as the cord-sparing option that exists in the canine
   literature, not as the primary plan.
3. **Whole-brain 36 Gy with no spinal field.** Cord then takes only the 2 Gy TBI (3.0 Gy3.9, 4%) plus exit dose. Spinal CSF
   relies on intrathecal methotrexate alone, so the intrathecal dose count in the spine is not reduced -- this spares the
   cord but forfeits the entire benefit the question is chasing. Listed for completeness.

---

## 6. (d) Verdict and grade

**Yes. A full 36 Gy / 20 x 1.8 Gy craniospinal course is affordable with ~2 Gy reduced-intensity conditioning, and it is
affordable with room to spare -- 66% of the canine 5%-myelopathy level, below the 68% the record already accepts for
2 x 5 Gy plus 23.4 Gy.** The conditional is that the post-graft immunosuppression must change.

Component grades:

| component of the claim | grade | basis |
|---|---|---|
| 2 Gy TBI + DLA-identical marrow + MMF/CSP or SRL/CSP gives durable engraftment in ~80% of dogs | **MEASURED (dog)** | 8/10 pooled (23994246); 4/5 (9108426); 5/6 (12931117) |
| 1 Gy is not enough; 2 Gy is the floor | **MEASURED (dog)** | 0/11+ at 100 cGy (9108426, 12931117, 23994246, 17241922) |
| **Cyclosporine alone is not enough at 2 Gy** | **MEASURED (dog)** | 9108426 group 1: transient chimerism <=4 wk |
| GVHD at 2 Gy DLA-identical with two-drug prophylaxis is rare | **MEASURED (dog), small n** | no GVHD reported across 9108426 / 12931117 / 23994246 / 17369487 / 15316362; review statement 34390541 |
| Graft-versus-lymphoma survives at 2 Gy | **TRANSFERRED (human, strong)** | 37788792 n=279 NHL: no OS/PFS difference 2 Gy vs 4 Gy or Flu-Mel, lower NRM; 34293518 (the model's own CNS anchor is a 200 cGy regimen); canine GVT itself MEASURED but only at 9.2 Gy (34390541) |
| Canine tumour outcome with 2 Gy conditioning | **DOES NOT EXIST (NOT FOUND)** | confirmed independently this session |
| Canine cord tolerance for a long field | **MEASURED (dog) at the D50 level** | 9572623: clinical-signs ED50 54.0 Gy at 4 Gy/fx over 20 cm = 109.4 Gy3.9, vs Jin BED50 111 Gy3.9 |
| The 5% level and the 1.8 Gy/fx conversion | **DERIVED** | 26366252: BED5 83.9 Gy3.9, D5 57.4 Gy at 1.8 Gy/fx |
| 2 Gy TBI + 36 Gy CSI = 55.6 Gy3.9 = 66% of BED5 | **DERIVED** (arithmetic on the two lines above) | s2b |
| Marrow does not bind, with graft rescue | **TRANSFERRED (human, direct)** | 24858425: 27 Gy mean (cap 43 Gy) to marrow **on top of 2 Gy TBI**, allograft, no graft failure, no stromal damage; 22592050/36263219 TMI 12-20 Gy, engraftment in all |
| Craniospinal radiation before, not after, the graft | **TRANSFERRED (human, n=25)** | 38244173: CSI immediately prior to allo-HCT in 25/39, 21 then TBI 12 Gy, no grade >=3 acute toxicity during CSI |
| Net kill trade vs the program's 2 x 4 Gy allo conditioning | **DERIVED, and weak** | s4; and the record's own evidence that LQ mis-predicts TBI dose-response (`SWEEP_stemcell.md:160`) |

**Overall grade: TRANSFERRED.** Every load-bearing number has either a canine measurement (engraftment, cord ED50) or a
written human transfer (GVL at 2 Gy, marrow dose with graft, CSI-before-transplant sequencing) behind it. It is **not
MEASURED**: no dog has had a craniospinal course at 1.8 Gy/fx, no dog has had a tumour treated with 2 Gy conditioning, and
no dog has had craniospinal radiation plus a transplant.

**Required protocol changes if this is adopted** (these are the proposal, not caveats):
1. Post-graft immunosuppression becomes **MMF 10 mg/kg BID + CSP 15 mg/kg BID** (or sirolimus + CSP), not cyclosporine
   alone. Non-negotiable: 9108426 group 1.
2. TBI becomes **one 200 cGy exposure at 7 cGy/min**, marrow or G-PBMC infused within hours.
3. Craniospinal 36 Gy / 20 x 1.8 Gy is delivered **before** conditioning, on the chemotherapy backbone, with the graft
   following.
4. Donor chimerism is monitored, with **cryopreserved donor CD3+ aliquots available for DLI** to convert mixed to full
   chimerism if needed (already standard in the program's own series, 35789057).

---

## 7. (e) What would make this fail

Ordered by how likely each is to be the thing that actually breaks it.

1. **Mixed chimerism weakens the graft-versus-lymphoma effect. This is the real risk and it is NOT closed.** The program's
   allograft kill (2.6 e-folds, 0.65-4.2) was OUTCOME-calibrated on dogs with **>95% donor WBC within 2 weeks**
   (35789057). 2 Gy conditioning produces **stable mixed** chimerism, sometimes at low donor fractions (85% and 12% in the
   PK-deficiency dogs, 11215693; median 37% at day 35 in the haplo setting, 16906030), and in the one canine disease model
   with a graded benefit endpoint, **clinical benefit tracked the donor percentage** and the paper concluded "complete
   donor chimerism appears necessary to achieve a long-term cure" (11215693). Human corroboration in the same direction:
   full-donor chimerism at day 30 predicted lower relapse (17325892). **No canine or human dataset retrieved here measures
   GVL as a function of donor chimerism fraction in lymphoma.** Mitigations that exist: DLI to convert (human response
   rates 60-77% in the record's transfer set; in dogs, DLI within 3 weeks is fatal, after ~2 months tolerated, PMID
   19446000 in record), or the three-drug MMF/CSP/sirolimus regimen (34390541). The honest statement is that this proposal
   trades a measured cord-budget gain for an **unquantified** GVL risk, and that the trade should be tested by running the
   model with K_graft scaled down and seeing whether the brain still closes.
2. **Post-graft immunosuppression cannot be delivered.** If MMF or sirolimus cannot be added to cyclosporine (cost,
   canine GI toxicity of MMF, monitoring burden), 2 Gy conditioning fails outright -- 0 durable engraftment with CSP alone.
3. **The cord-length extrapolation beyond 20 cm is wrong.** Powers measured an 8.3-15.0 Gy ED50 penalty from 4 cm to 20 cm,
   with the curves still separated at low injury probability; a whole-cord canine field is longer than 20 cm and no data
   exist for that length. If the volume penalty continues at the same slope, the effective D5 falls and the 66% figure
   rises. A plan that wants margin here uses **30.6 Gy / 17 x 1.8 (57% of BED5, and already +31% e-folds, above the +25%
   that the model run showed cuts 34 doses to 18)** rather than 36 Gy.
4. **Late myelopathy appears inside the 10-year window.** Human latency is bimodal at ~9 and ~26 months; Powers' follow-up
   duration is UNVERIFIED. A 10-year goal is long enough to see the late vascular peak, and any myelopathy in a
   craniospinal field is a whole-cord event, not a focal one.
5. **Radiation-induced vertebral tumour.** PMID 11678571: a 2-year-old Rottweiler irradiated for an intradural spinal
   tumour developed vertebral osteosarcoma in the field at **5.5 years**, fulfilling all criteria for a radiation-induced
   tumour; the authors advise **<=3 Gy per fraction** for dogs with a 3-5+ year life expectancy. 1.8 Gy/fx satisfies that,
   and the total is far below the coarse-fraction schedules implicated -- but a 36 Gy field over ~40% of the skeleton on a
   10-year horizon makes this a named competing hazard, not a theoretical one. It is the same unquantified endpoint the
   record already flags for the brain (`SWEEP_rt2.md:144`).
6. **Four weeks of pre-graft radiation lets systemic disease regrow.** At the model's growth bar the dog cannot be left
   untreated through 20 fractions; the plan depends on the chemotherapy backbone holding remission across the course, with
   the mucositis cost of overlapping CSI and conditioning (37401225).
7. **The LQ net trade is read as the justification.** If someone grades this on the e-fold arithmetic alone, the resistant
   line (CLL1390) shows a small net loss (-0.06 to -0.50) and the 2 x 5 Gy comparison shows a loss on most lines. The case
   does not rest there, and must not be written as if it does: it rests on the cord budget (DERIVED from a canine
   measurement), the human 2 Gy-versus-4 Gy NHL outcome (MEASURED, n=279), and the halving of the anaesthetic count.

---

## 8. UNVERIFIED / NOT FOUND

- **Canine tumour (lymphoma or any) outcome with 2 Gy / nonmyeloablative conditioning: does not exist.** Four independent
  PubMed queries this session; confirms `SWEEP_stemcell.md:139`.
- **Canine craniospinal irradiation combined with a transplant: not found.** Only Couto 1984 (6547126), 4 dogs, no dose, no
  transplant.
- **Canine cord tolerance for a field longer than 20 cm: not measured** (no species).
- **Powers 1998 follow-up duration, and the ED50 for the 2 Gy/fx control arm (36 dogs, 60-84 Gy to 20 cm): not in the
  abstract; no full text retrieved.** The 4 Gy/fx ED50s are the quoted values.
- **GVL as a function of donor chimerism percentage, in any species, in lymphoma: not found.**
- **Canine active bone-marrow distribution by skeletal site: not found.** The ~28% vertebral / ~13% cranial figures used in
  s3 are human, from an Ellis-derived table reached through a web search, and are a secondary source.
- **Pooled spinal relapse rate after whole-brain radiotherapy in PCNSL: not found.** The NCI PDQ physician summary does not
  discuss spinal-axis radiation.
- **Dose rate of the 2 x 4 Gy canine allo TBI:** 7.5-10 cGy/min (35789057, in record); the Lupu case states 7 cGy/min with
  the two fractions **3 hours apart** (16506937) -- a detail not previously in the record.
- GVHD **incidence** at 2 Gy is reported as absence of reported cases across small series, not as a measured rate with a
  denominator and a grading scheme. Treat "rare" as qualitative.
