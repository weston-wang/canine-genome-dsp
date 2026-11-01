# SWEEP_rt3 (2026-11-01): can the brain radiation be escalated above 23.4 Gy / 13 x 1.8 Gy, and what kill does it buy?

**Question.** Can whole-brain or craniospinal radiation in the canine B-cell lymphoma program go above one 23.4 Gy course
(13 x 1.8 Gy) and stay within documented canine tolerance? How much more lymphoma kill would that buy, using measured canine
radiosensitivity? Context: the B-cell brain closure needs 29-45 intrathecal methotrexate doses because the radiation
contributes too little. A model run found that +25% in-vivo e-folds (1.67 to 2.09) cuts the B-cell brain from 34 to 18
intrathecal doses.

**Bar (user, verbatim):** "real data or rigorous model"; "I'm okay with no specific data but if scientifically sound".
So a dose limit transferred from humans, or derived from canine data in another field, counts **if the transfer is written
down**. It is graded TRANSFERRED or DERIVED, never MEASURED.

**Case:** canine B-cell lymphoma in the brain compartment (the T-cell brain uses the same arithmetic with the OSW line).
Evidence from other tumours (meningioma, glioma, nasal), other species and the systemic TBI setting is labelled indirect.

## 0. Record check (what was already there, and where)
- ALREADY IN RECORD (`SWEEP_rt2.md` Q1.1-Q1.4, `LYMPHOMA_UNIVERSE.md` K.5): the canine focal brain standard of 40 Gy / 10 x 4 Gy
  (PMIDs 42304866, 41420297, 35775129), 50 Gy / 20 x 2.5 Gy (41588441), and 35-52.5 Gy at 2.5-4 Gy per fraction (16355679). No severe
  late toxicity was seen in these series. The record also has the canine dose-volume constraints Brain-GTV V32Gy <= 13 cm^3 and
  whole-brain gEUD <= 30 Gy (41420297), and the comparison "23.4 Gy = 44.5 Gy2 BED = 37-40% of the dog routine". On the cord it has
  alpha/beta 3.9, BED5 83.9 Gy3.9 (26366252), and the result that 4 Gy fractions put the cord at tolerance while 1.8 Gy needs a
  craniospinal field. It has Couto 1984 (6547126: 4 dogs, intrathecal cytarabine plus craniospinal cobalt, no dose given) and the
  23.4 Gy human neurotoxicity data (24101038, 35772168, 32725379). Adhikari 2018 (29633112) is there: 23.4 Gy under-treats compared
  with 45 Gy, n=22. So are leukoencephalopathy from intrathecal methotrexate (39269476), the low-dose and 8 Gy single-fraction
  analysis, OSW as a T-cell line (17532464), and the anaesthesia cost.
- ALREADY IN RECORD: the LQ fit (`lymphoma_grounded_inputs.lq_alpha_beta`, `RT_SURVIVAL`, Maeda PMID 27257868), the in-vivo
  dose-modifying factor (DMF) 1.9 (PMID 3009370), and `lymphoma_sustained.RT_EFOLDS_IN_VITRO` = 1.71 / 3.18 / 7.05 (OSW 5.58).
  TBI 8.4 vs 13.5 Gy (3887690, 3901841) is in `SWEEP_stemcell` s4.1 and UNIVERSE I.1, with the rule "not credited above one
  conventional course". The half-body PMIDs 19627472, 42525883, 37700548, 40088118, 41183984 and 19178684 are in SWEEP_exists /
  SWEEP_hct_model. Human PCNSL radioresistance (1572835, 10563430) is in SWEEP_rt / grounded inputs. CNS lymphoma in 18 dogs
  (30022475) is in UNIVERSE J.1. The program's own TBI is 2 x 5 Gy (`RT_COURSES`), and its brain access is transferred at 1.0
  (`SWEEP_hct_model` l.263).
- NOT in the record before this sweep: **any escalation above 23.4 Gy.** No document computes the e-folds or the late-effect
  dose for 30.6-45 Gy, or the canine WHOLE-brain late-effect dose-response. None tests whether the TBI escalation result transfers
  to a brain-confined compartment, and none adds the program's own TBI to the brain and cord budget. Every PMID below marked NEW
  was checked against `docs/` and `src/` by grep.

## 1. Sources

### 1a. Canine brain tolerance: whole-brain and experimental data (NEW unless marked)
| PMID / DOI | what | numbers |
|---|---|---|
| **12065111** (Benczik 2002 Radiother Oncol, doi 10.1016/s0167-8140(02)00028-2) and **12537525** (same dogs, doi 10.1667/0033-7587(2003)159[0199:eotrbe]2.0.co;2, which says "whole-brain irradiation ... 6 MV photons") | **Canine WHOLE-BRAIN single-dose dose-response**, 4 groups of 5 beagles at 10/12/14/16 Gy, followed 77-115 weeks | ED50: any histological lesion **11.4 +/- 0.6 Gy**; macroscopic lesion **13.0 +/- 1.1 Gy**; T2 focal change 11.0, diffuse 10.8; contrast enhancement 13.4 (MRI) / 13.0 (CT) |
| **3335464** (Fike 1988 IJROBP, doi 10.1016/0360-3016(88)90052-1) | hemibrain single dose, beagles, 11.5-17 Gy | **LD50 14.9 Gy** (deaths at 5-8 months); ED50 for low-density volume 14.6 Gy (lethal range); sublethal white-matter low density ED50 **12.8 Gy**; the curves are "extremely steep" |
| **11026694** (doi 10.1023/a:1006419210584) | whole-brain BNCT in 12 dogs (mixed LET) | threshold whole-brain dose **9.8 Gy-Eq single**; indirect because of the mixed-LET field |
| **10519690** (Thrall 1999 Int J Hyperthermia, doi 10.1080/026567399285576) | phase III, 45 dogs with brain masses, **total dose randomised to 44, 48, 52, 56 or 60 Gy** | brain necrosis occurred, and the tumour could not be separated from necrosis as the cause of progressive neuropathy. No dose-necrosis numbers in the abstract and no full text (UNVERIFIED). It shows a randomised canine dose range up to 60 Gy was given |
| **10955504** (doi 10.1111/j.1740-8261.2000.tb02091.x) | 29 dogs, cobalt, **48 Gy / 16 x 3 Gy** | "late radiation effects could not be evaluated"; median OS 250 d |
| **9303051** (doi 10.1002/(SICI)1520-6823(1997)5:1<8::AID-ROI2>3.0.CO;2-1) | cites **"25 dogs given 46-48 Gy of cobalt-60 radiation to the WHOLE BRAIN"**, MST 150 d | the only canine fractionated whole-brain dose found. **Secondary citation; primary source not identified (UNVERIFIED).** Survival was too short to see late effects |
| **6421785** (JAVMA 1984) | 4 dogs, 30-36 Gy in 5-6 fractions | 100% 1-year survival corrected for intercurrent death; no late toxicity reported |
| **1941756** (Heidner 1991, doi 10.1111/j.1939-1676.1991.tb00952.x) | 86 dogs, cobalt | MST 4.9 mo with radiation; no dose-toxicity data |
| **32356907** (Van Asselt 2020, doi 10.1111/vru.12868, PMC7953428) | 52 dogs, IMRT **45-50 Gy / 18-20 x 2.25-2.5 Gy** | "few reported acute, acute delayed, or late side effects"; **7 dogs retreated with a second course** (full text: no late effects reported) |
| **39391956** (Staudinger 2024, doi 10.1111/jvim.17213) | 34 dogs, 10 x 4 Gy | cerebral microbleeds in **62%** after RT, +14%/month, **OR 4.7 in the >30 Gy region vs <20 Gy**. A canine late-effect dose-response, subclinical, clinical relevance unknown |
| 41420297 ALREADY IN RECORD; full text read now (PMC12875757) | 105 dogs, 10 x 4 Gy | gEUD computed with **a = 4**; whole-brain gEUD >= 29.7 Gy HR 1.72 (adjusted 30.07 Gy, HR 2.22); recommended **<= 30 Gy**; median follow-up 559 d. **No necrosis or neurotoxicity counts**: the threshold is a survival association that the authors attribute to possible necrosis |

### 1b. Human whole-brain tolerance and dose-response anchors (NEW)
| PMID / DOI | numbers |
|---|---|
| **20171513** (QUANTEC brain, Lawrence 2010, doi 10.1016/j.ijrobp.2009.02.091, full text) | partial brain, <2.5 Gy/fx: **5% necrosis at BED 120 Gy3 (EQD2 72 Gy, range 60-84); 10% at BED 150 Gy3 (EQD2 90)**. The brain's alpha/beta "has been estimated to be 2". Cognitive dysfunction in children "largely seen for whole brain doses >= 18 Gy"; 24 Gy cranial in ALL gave a median 13-point IQ loss |
| **1517781** (Silber 1992 JCO, doi 10.1200/JCO.1992.10.9.1390) | whole-brain dose and IQ: **36 Gy gave 8.2 points (CI 1.8-14.6) less than 24 Gy, and 12.3 less than 18 Gy** (children) |
| **11773174** (Bessell 2002 JCO, doi 10.1200/JCO.2002.20.1.231) | PCNSL after CHOD/BVAM, CR patients: **45 Gy vs 30.6 Gy WBRT, 3-year relapse 29% vs 70%; age <60: 25% vs 83% (p=.01); 3-year OS 92% vs 60%**. A brain-compartment lymphoma dose-response; sequential, non-randomised trials |
| **37964132** (Ko 2023, doi 10.1007/s11060-023-04504-2) | PCNSL curative or salvage, n=66: <=30 Gy (median 25.2) vs >30 Gy (median 49.6). **3-year intracranial control 35.2% vs 41.6%, p=0.30**; grade >=3 neurotoxicity in 6 patients, **5 of them in the high-dose group** |
| **6110090** (Nesbit 1981 Lancet, doi 10.1016/s0140-6736(81)91849-3) | ALL CNS prophylaxis: **18 Gy vs 24 Gy gave no significant increase in CNS relapse** (478 children) |
| **10048422** (Ha 1999, doi 10.3109/10428199909058407) | leukaemic cranial-nerve palsy, whole-brain 16-30 Gy at 2-3 Gy/fx: "**No dose-response relationship** was observed" |
| **16809737** (Barredo 2006 JCO, doi 10.1200/JCO.2005.03.3373), **10717213** (Kun 1997) | isolated CNS relapse of ALL: standard salvage is **craniospinal 24 Gy cranial / 15 Gy spinal**, with >60% durable second remission |
| **18037587** (Mayer & Sminia 2008 IJROBP, doi 10.1016/j.ijrobp.2007.08.015) | re-irradiation of human brain: **necrosis at cumulative EQD2 (alpha/beta 2) >100 Gy**; conventional series 81.6-101.9 Gy; the interval did not predict necrosis |

### 1c. Canine re-irradiation (Q4; NEW)
| PMID / DOI | numbers |
|---|---|
| 32356907 (above) | 7/52 dogs with brain tumours given a second IMRT course; no late effects reported |
| **39395151**, **40417366** (case reports, doi 10.1111/vru.13454, 10.3389/fvets.2025.1572808) | a second stereotactic course to the canine brain; one pseudoprogression |
| **21388476** (Bommarito 2011, doi 10.1111/j.1740-8261.2010.01763.x) | nasal (field next to brain), 50 Gy then 36 Gy at a median 539 d: **2/9 severe late (blindness)**; 8/9 second remissions |
| **35023604** (Gieger 2022, doi 10.1111/vco.12801) | nasal SRT 10 Gy x 3 twice: **adverse events 8/11 (73%)**, seizures in 2 |
| **23861260**, **40201825**, **26729295** | nasal re-irradiation 37-117 Gy lifetime; mostly grade 1-2 late effects |
No canine series re-irradiates the WHOLE brain. Re-treating a focal field is done routinely; re-treating the whole brain is not documented (NOT FOUND).

### 1d. Canine CNS lymphoma treated with radiation (Q2)
- 30022475 (ALREADY IN RECORD): 18 dogs, 7 received RT in some combination; overall MST 171 d (1-1,942 d). **Doses are not in the abstract (UNVERIFIED).**
- 6547126 (ALREADY IN RECORD): 4 dogs, craniospinal cobalt plus intrathecal cytarabine, no dose given.
- 40216556 (case, NEW to this file; cited in SWEEP_cnsregimens): a "glioma" irradiated, later B-cell lymphoma, brain mass resolved; dose not stated.
- **No canine CNS-lymphoma radiation series reports a dose or a dose-response.** Q2 cannot be answered from dogs.

### 1e. Primary canine lymphoma radiosensitivity and half-body data (Q3)
- Primary-cell SF2 or alpha/beta for canine lymphoma: **does not exist** (ALREADY IN RECORD, SWEEP_rt2 Q4.1; this sweep found none either).
- Half-body, NEW to the record: **15515588** (Williams 2004, 52 dogs, 2 x 4 Gy per half; median first remission 311 d), **2654376**
  (Laing 1989, 14 dogs, **7 Gy single per half**, measurable shrinkage in 11/14 (79%) of chemoresistant bulky disease, CR/PR mean 102/54 d),
  **17186856** (Axiak 2006, 6 vs 8 Gy per half, no toxicity difference, 2 thrombocytopenic deaths), **19379300** (6 dogs, 2 x 4 Gy).
  **None measures a log-kill.** All report outcomes only. Rough consistency check: the LQ fit for line 1771 at 7 Gy single gives 2.38
  e-folds in vitro, or 1.25 in vivo after DMF 1.9, which predicts about 71% cell loss. That fits "measurable decrease in 79%" in
  direction. It is not a calibration.

## 2. Q5: does "dose escalation did not reduce relapse" apply to the brain?
The two papers (3887690, 3901841; abstracts re-read) are **total-body irradiation followed by marrow transplant**. Four confounders
are written into them:
1. **Graft contamination.** Deeg 1985 (3901841) says it directly: "recurrent disease may have been due to lymphoma cells contained in the
   infused remission marrow." Escalating TBI cannot sterilise tumour that is re-infused afterwards. The program uses a DLA-matched
   ALLOGENEIC graft (no tumour in it), and a brain field has no re-infusion step, so **this mechanism does not exist in the brain compartment**.
2. **Toxic deaths at the higher dose** (55% vs 26%, 3887690). These shrink and select the evaluable set (16/20 and 14/20 in 3901841).
3. **Dose-rate.** The doses were single low-dose-rate exposures at 2-4 cGy/min. For lines with low alpha/beta, repair during delivery
   removes part of the LQ quadratic term, so "13.5 vs 8.4 Gy" is a smaller kill increment than the nominal ratio implies.
4. Relapse was systemic, with no site analysis.

Brain-compartment evidence, all human and all INDIRECT:
- **For** a dose-response: Bessell (11773174), with relapse 29% at 45 Gy vs 70% at 30.6 Gy, and Adhikari (29633112, record).
- **Against**: Ko (37964132), no difference between <=30 and >30 Gy in salvage; Nesbit (6110090), 18 = 24 Gy for prophylaxis with
  intrathecal methotrexate; Ha (10048422), flat from 16 to 30 Gy; Nelson (1572835 / 10563430, record), 61% brain recurrence even at
  40+20 Gy and a "threshold, not a classic dose-response".
- **Reading:** a dose-response shows where radiation is the main CNS agent against measurable disease (PCNSL, 30.6 to 45 Gy). It
  flattens where intrathecal or systemic therapy is also present (ALL prophylaxis) and in refractory or salvage disease. The model's
  setting is radiation plus intrathecal methotrexate against residual disease, which is between the two.

**Verdict on the cap:** the TBI result is about a systemic, graft-contaminated, low-dose-rate setting. It is **not a written transfer
to a brain-confined field**, so it does not justify capping brain e-folds at 23.4 Gy. The right handling is to credit the LQ e-folds
of the escalated course (DERIVED) and state the human plateau evidence as the caution. The cap has no transfer behind it. The
escalation has a derivation behind it plus one positive human brain dose-response (Bessell).

## 3. Computed table (LQ, with the record's own canine-line fits)
Line fits, `gi.lq_alpha_beta` on Maeda SF2/SF5 (PMID 27257868):

| line | SF2 / SF5 | alpha (Gy^-1) | beta (Gy^-2) | alpha/beta (Gy) |
|---|---|---|---|---|
| CLL1390 (resistant) | 0.85 / 0.36 | 0.000 (floored) | 0.0406 | 0 |
| 1771 (median) | 0.75 / 0.27 | 0.0652 | 0.0393 | 1.66 |
| OSW (T-cell) | 0.61 / 0.15 | 0.1590 | 0.0441 | 3.61 |
| CLBL1 (sensitive, B-cell) | 0.53 / 0.06 | 0.1539 | 0.0817 | 1.88 |

Formulae:
- e-folds = n(alpha d + beta d^2); in vivo = e-folds / 1.9.
- Brain BED2 = D(1 + d/2) and EQD2(2) = BED2/2 (alpha/beta 2 per QUANTEC 20171513).
- Cord BED = D(1 + d/3.9), compared with BED5 = 83.9 Gy3.9 (26366252).

Worked example for 36 Gy / 20 x 1.8 at line 1771:
- e-folds = 20 x (0.0652 x 1.8 + 0.0393 x 3.24) = 20 x (0.1174 + 0.1273) = 4.90 in vitro, and 4.90 / 1.9 = **2.58 in vivo**.
- BED2 = 36 x 1.9 = 68.4, so EQD2 = 34.2.
- Cord BED = 36 x 1.4615 = 52.6, which is 63% of BED5.

| schedule | brain EQD2(2) | cord BED3.9 (% of BED5) | CLL1390 in vitro / **in vivo** | 1771 median | OSW (T) | CLBL1 | x vs 23.4 Gy (1771) |
|---|---|---|---|---|---|---|---|
| **23.4 / 13 x 1.8** (current) | 22.2 | 34.2 (41%) | 1.71 / **0.90** | 3.18 / **1.67** | 5.58 / **2.94** | 7.05 / **3.71** | 1.00 |
| 30.6 / 17 x 1.8 | 29.1 | 44.7 (53%) | 2.24 / **1.18** | 4.16 / **2.19** | 7.29 / **3.84** | 9.21 / **4.85** | 1.31 |
| **36 / 20 x 1.8** | **34.2** | 52.6 (63%) | 2.63 / **1.39** | 4.90 / **2.58** | 8.58 / **4.52** | 10.84 / **5.70** | **1.54** |
| 39.6 / 22 x 1.8 (canine whole-brain ceiling, see s4) | 37.6 | 57.9 (69%) | 2.90 / **1.52** | 5.38 / **2.83** | 9.44 / **4.97** | 11.92 / **6.28** | 1.69 |
| 40 / 20 x 2 | 40.0 | 60.5 (72%) | 3.25 / **1.71** | 5.75 / **3.03** | 9.89 / **5.20** | 12.70 / **6.68** | 1.81 |
| 45 / 25 x 1.8 | 42.8 | 65.8 (78%) | 3.29 / **1.73** | 6.12 / **3.22** | 10.72 / **5.64** | 13.55 / **7.13** | 1.92 |
| 40 / 10 x 4 (canine focal standard) | 60.0 | 81.0 (97%) | 6.50 / 3.42 | 8.90 / 4.68 | 13.41 / 7.06 | 19.24 / 10.12 | 2.80 |
| 50 / 20 x 2.5 (canine pituitary) | 56.2 | 82.1 (98%) | 5.08 / 2.67 | 8.18 / 4.30 | 13.46 / 7.08 | 17.92 / 9.43 | 2.57 |
| 48 / 16 x 3 (canine, 10955504) | 60.0 | 84.9 (101%) | 5.85 / 3.08 | 8.79 / 4.63 | 13.98 / 7.36 | 19.16 / 10.08 | 2.76 |
| program TBI 10 / 2 x 5 (`RT_COURSES`) | 17.5 | 22.8 (27%) | 2.03 / 1.07 | 2.62 / 1.38 | 3.79 / 2.00 | 5.63 / 2.96 | -- |

Observations:
- At fixed 1.8 Gy fractions the kill scales linearly with total dose.
- The canine lines' alpha/beta (0-1.9 for the B/CLL lines) is **at or below the brain's alpha/beta of 2**, so larger fractions do NOT
  cost therapeutic ratio for these lines. Per unit of brain EQD2 they are slightly better (CLL1390: 40/20 x 2 gives 1.71 at EQD2 40;
  39.6/22 x 1.8 gives 1.52 at EQD2 37.6).
- Fraction size is limited by the cord in a craniospinal field and by the human-derived <2.5 Gy/fx predictability rule (20171513),
  not by tumour kill.
- Caution, stated rather than tuned: a two-point SF2/SF5 fit gives very uncertain alpha/beta, and clinical lymphoma is usually
  assigned alpha/beta ~10. So the "larger fractions are free" reading is model-internal.

**Cumulative with the program's own TBI** (NEW observation: the record credits TBI kill to the brain at access 1.0 but never adds
TBI to the brain and cord late-effect budget):

| brain course | brain EQD2(2) + TBI 17.5 | cord BED3.9 + TBI 22.8 (% BED5) |
|---|---|---|
| 23.4 / 13 x 1.8 | 39.7 | 57.0 (68%) |
| 30.6 / 17 x 1.8 | 46.6 | 67.5 (80%) |
| 36 / 20 x 1.8 | 51.7 | 75.4 (90%) |
| 39.6 / 22 x 1.8 | 55.1 | 80.7 (96%) |
| 45 / 25 x 1.8 | 60.2 | 88.6 (106%) |

## 4. Tolerance limits applied, and the recommended maximum
Limits, each graded:
- (a) **Canine whole-brain anchor, DERIVED from canine data.** Whole-brain gEUD <= 30 Gy in 10 fractions (41420297). A uniform 30 Gy
  in 10 fractions is 3 Gy/fx, so EQD2(2) = 30 x (3+2)/(2+2) = **37.5 Gy**. At 1.8 Gy/fx that is D = 37.5 x 4 / 3.8 = **39.5 Gy, i.e.
  22 x 1.8 = 39.6 Gy**. Caveat: this is a survival association in tumour-bearing dogs, gEUD a = 4 is borrowed from humans, and no
  necrosis counts were given.
- (b) **Canine single-dose whole-brain ED50**: 11.4 Gy for any histological lesion (12065111). Converted with alpha/beta 2, EQD2 =
  11.4 x 13.4 / 4 = 38.2 Gy. This is a 50% subclinical-lesion level, and LQ conversion of single doses >10 Gy over-predicts. It
  agrees in magnitude with (a). The macroscopic-lesion ED50 of 13.0 Gy gives EQD2 48.8.
- (c) **Canine focal routine**: EQD2 56-60 Gy with no severe late effects reported (record). This is focal, so it is an upper bound for whole-brain.
- (d) **Human**: whole-brain 36-45 Gy at 1.8 Gy/fx was the historical PCNSL dose, with dose-dependent cognitive loss (36 Gy is 8
  IQ points worse than 24 Gy in children, 1517781). QUANTEC partial-brain 5% necrosis is at EQD2 72.
- (e) **Cord**: BED5 83.9 Gy3.9 (26366252, DERIVED from a fit that includes dog data).

**Recommended maximum defensible course: 36 Gy in 20 x 1.8 Gy to the whole brain, with the spinal portion held at 23.4 Gy /
13 x 1.8 Gy if the field is craniospinal. Grade: TRANSFERRED** (human 36 Gy whole-brain and CSI practice; canine whole-brain anchor
DERIVED; canine cord DERIVED). It is not MEASURED: no dog has had a 1.8 Gy/fx whole-brain course in any retrieved series.

Why 36 Gy and not more:
- Radiation alone is at brain EQD2 34.2, under the canine whole-brain anchor (37.5) and the canine single-dose ED50 equivalent (38.2).
- With the program's TBI added it is 51.7, still under the canine focal routine (56-60) and under QUANTEC 5%.
- Spinal cord at 23.4 Gy plus TBI = 57.0 Gy3.9 (68% of BED5). A full 36 Gy craniospinal field plus TBI would be 75.4 (90% of BED5),
  which is too close for a 10-year horizon. Hence the split field, which is the human pattern (24 Gy cranial / 15 Gy spinal, 16809737).

Further limits:
- **39.6 / 22 x 1.8 is the absolute ceiling** for radiation alone, set by limit (a). With TBI it reaches EQD2 55 and is not recommended.
- **45 Gy is excluded**:
  - it exceeds the canine whole-brain anchor (42.8 > 37.5);
  - with TBI it reaches the canine focal routine (60.2);
  - it is the human dose abandoned for neurotoxicity (32725379 record, 37964132: 5/6 grade >=3 events in the high-dose group).

**Kill bought** (in vivo, 36 vs 23.4 Gy, x1.54):

| line | 23.4 Gy | 36 Gy |
|---|---|---|
| median 1771 | 1.67 | **2.58** (+0.91 e-fold) |
| resistant CLL1390 | 0.90 | 1.39 |
| sensitive CLBL1 | 3.71 | 5.70 |
| OSW (T-cell) | 2.94 | 4.52 |

This is +54%, more than double the +25% (2.09) that the coordinator's run showed cuts the B-cell brain from 34 to 18 intrathecal
doses. **30.6 / 17 x 1.8** (+31%, 2.19 at median; brain EQD2 with TBI 46.6) is the conservative fallback and alone already exceeds
the +25% point. The window and dose count at 2.58 and 2.19 should be re-run with `minimal_lawful_window(..., rt_efolds=2.58)`.
This sweep did not edit code.

Cost of escalation:
- 7 more anaesthetics (20 vs 13 fractions). At the record's 0.1-0.5% per-event rate, cumulative mortality goes from 1.3-6.3% to 2.0-9.5%.
- A larger cognitive and white-matter dose: human, 8 IQ points from 24 to 36 Gy in children.
- More radiation added to the leukoencephalopathy driver that matters most (intrathecal methotrexate, HR 4.50 by dose number,
  39269476 record). The trade is fewer methotrexate doses for more radiation. Since the methotrexate dose COUNT is the measured
  hazard, cutting it from 34 toward ~18 probably lowers net white-matter risk. That is a judgement, not a computation.

## 5. Re-irradiation (Q4)
Canine re-irradiation of FOCAL brain and nasal fields is documented (32356907: 7 dogs; 21388476: 2/9 severe late after 50 + 36 Gy;
35023604: 73% adverse events after a second 30 Gy SRT). A **second whole-brain course in a dog: NOT FOUND.** Human cumulative
tolerance is EQD2(2) ~100 Gy (18037587, focal glioma re-irradiation). On that basis a second 23.4 Gy course (cumulative 44.4, or 61.9
with TBI) is TRANSFERRED as within tolerance. Splitting the dose into two courses buys no kill over one 36 Gy course, though, and it
doubles the anaesthesia blocks. Re-irradiation is a salvage option, not a better primary plan.

## 6. UNVERIFIED / NOT FOUND
- The primary source of "25 dogs, 46-48 Gy cobalt whole brain" (cited in 9303051): not identified.
- Thrall 1999 (10519690) necrosis incidence by dose arm (44-60 Gy) and its fraction size: not in the abstract, no full text.
- Radiation doses for the 7 irradiated dogs in 30022475: not in the abstract.
- A canine whole-brain fractionated late-toxicity series at any dose per fraction: not found. Canine series are focal; the whole-brain data are single-dose experimental.
- A second whole-brain course in a dog: not found.
- Primary canine lymphoma SF2 or alpha/beta: does not exist (record already says so).
- Measured log-kill from canine half-body irradiation: does not exist (outcomes only).
