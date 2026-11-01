# Long-course intrathecal / intraventricular methotrexate: is 30-45 doses over 12-16 months tolerable? (agent notes, 2026-11-01)

Question (from `LYMPHOMA_STATUS.md` 2026-10-31 / `LYMPHOMA_UNIVERSE.md` M.3-M.4): the B-cell brain closure at verdinexor's 0.09
brain-reach floor needs **29-45 intrathecal methotrexate doses** (every 10-14 d, 2.5 mg flat, CSF port or tap) plus one 23.4 Gy course.
`failing()` returns exactly this item, graded ASSUMED ("no canine series beyond 28 doses, no written human transfer yet").
Bar (CLAUDE.md): real data OR a rigorous model; a cross-species transfer is acceptable if justified in writing.

## 0. Record check (done before searching; rule 1)
Searched: `LYMPHOMA_UNIVERSE.md` J/K/M, `LYMPHOMA_STATUS.md`, `SWEEP_nm600_itmtx.md`, `SWEEP_itmtx2.md`, `SWEEP_rt2.md`,
`SWEEP_regional.md`, `SWEEP_exists.md`, `SWEEP_cnsregimens.md`, `SWEEP_brain_access.md`, research_notes (grep by PMID and keyword).
**ALREADY IN RECORD (not re-reported as new):** Peyrl 25017328 (98 children, 5,472 Ommaya instillations, median 36/reservoir, max 280,
1 infection); Obbens-type 9347977 (120 LM pts, median 46 administrations+punctures/pt, leukoencephalopathy 1.7%, reservoir surgery 6%);
33316084, 30447448, 38061763, 40719464, 26479760, 33101460, 33324883 (Ommaya complication rates); 31466902, 32989105 (Bonn), 38416167,
2809687 (CSF PK); TT16 31657981 (13-27 IT doses); 19553647, 19694717, 34034929 (cranial RT omitted; EORTC 10-19 IT); 39269476 (tLE 29%,
HR 4.5, mostly asymptomatic, WBRT not a risk factor); 36230611 (>12 vs <=12 IT: no MRI difference except ventricle width);
24101038, 35772168 (23.4 Gy cohorts, no Fazekas 4-5); Katz/Vuillemenot 25257657 + PMC4263309 (dog ICV/IT-L ports QOW, 20-28 doses,
8-11 mo); West 24694254 (dog lumbar port patency 67%/86% at 30 d); Dickson 17321776 (19 dogs, cisternal x4, 1 fatal brainstem
haematoma); Fentem 36906911 (0/108 deteriorations); 40526210 (CSF collection major complication 11/7,545); Yaksh 28-day beagle
infusions; Genoni 25041580; 6547126 (4 dogs IT ara-C + craniospinal RT, 1984); anaesthetic mortality 18658000, 9657167.

Everything below marked NEW was not found in the record by PMID or keyword.

## (a) Sources: dose counts and complication rates

### Human, long intrathecal/intraventricular courses
| source | population / route | IT/ICV doses per patient, duration | complications (as reported) | status |
|---|---|---|---|---|
| **von Bueren 2011, PMID 21636711, doi 10.1093/neuonc/nor025 (PMC3107096, full text via WebFetch)** HIT 2000 | 45 children <4 y, medulloblastoma, Ommaya-type ventricular reservoir, **with systemic HD-MTX** | **36 planned single intraventricular doses of 2 mg over 6 months** (with chemo cycles 1-3); per cycle >9 doses in 28-37 of 45 children | reservoir revision 8/45 (1 S. aureus CSF infection, 7 malfunction); nervous-system grade 4 toxicity 4/43 in cycles 1-3; leukoencephalopathy a dose-modification reason in 1 child per cycle; seizures 3 events | **NEW** |
| **Pompe 2015, PMID 26346136, doi 10.1016/j.ejca.2015.08.009** HIT 2000, all arms | 240 registered, 211 with ventricular reservoir, 2-3 cycles of ICV MTX + systemic chemo | (same 2 mg schedule; 519 cycles) | **reservoir complications 57/211 (27%): infection 32 (15%), malfunction 19 (9%); removal 39 (18%)**; acute neurotoxicity likely from ICV MTX **9/202 (4.5%)**, mostly mild; **1 death** (toxic oedema then seizures); 226/519 cycles (43%) reduced or omitted, mostly no device; >=75% of planned ICV MTX -> better EFS (61.5 vs 46.2%, p=.004) | **NEW** |
| **Rutkowski 2005, PMID 15758008, doi 10.1056/NEJMoa042176** HIT-SKK'92 | 43 children <3 y, IV chemo incl. HD-MTX + ICV MTX, no RT | 3 cycles with ICV MTX (count per child not in abstract) | "no major instances of unexpected toxicity"; **asymptomatic leukoencephalopathy 19/23 (83%)**; mean IQ below healthy controls but above a prior irradiated cohort | **NEW** |
| **Merlin 2023, PMID 37171700, doi 10.1007/s11060-023-04328-0** HIT-SKK in France | 35 children <5 y, median f/u 72 mo | per-protocol cumulative ICV + IV MTX (n=30); 5 got higher cumulative | LE in **20/30**; **grade 2-3 LE did NOT correlate with cumulative ICV-MTX (p=0.698)**; LE tended to decrease over time; FSIQ deficient 6/17; processing speed borderline with cumulative ICV dose (p=0.055) | **NEW** |
| **Ottensmeier 2025, PMID 42131756, doi 10.1093/nop/npaf100** HIT-SKK'87/'92, 15-y f/u | 24 children <3 y | ICV MTX arm vs deferred CSI arm | "MTX-recipients never scored worse than irradiated patients"; motor/fluid-IQ decline in both arms by 15 y | **NEW** |
| **Bhojwani 2014, PMID 24550419, doi 10.1200/JCO.2013.53.0808** St Jude (Total XV cohort) | 369 children with ALL, prospective MRI x4, **5 courses HD-MTX** | **13 to 25 doses of triple intrathecal therapy** (~2.5 y) | clinical MTX neurotoxicity **14 (3.8%), transient**; **12 of 13 rechallenged with IT and/or HD-MTX had no recurrence**; leukoencephalopathy 73/355 (20.6%) of asymptomatic, all symptomatic; LE associated with **systemic** MTX exposure (42-h plasma MTX:leucovorin, p=.038) | **NEW** |
| **Bleyer 1978, PMID 638249 (Blood 51:835)** | 19 pts meningeal leukaemia, Ommaya, randomised | 12 mg/m2 single doses vs "C x T" 1 mg q12h x6 per course | "Neurotoxicity ... correlate[s] with elevated concentrations of the drug in the CSF as well as with the total cumulative dosage"; cumulative 173 +/- 64 vs 66 +/- 41 mg/m2; **neurotoxicity 7/10 vs 1/8 (p<0.05)**, equal efficacy -> more, smaller doses are LESS neurotoxic | **NEW** |
| **Bleyer 1983, PMID 6366138, doi 10.1200/JCO.1983.1.5.317** CCG-141A/160 | 3,241 children | IT MTX x6 in consolidation +/- maintenance IT; **dosed by CNS volume (age), not BSA**; 18-24 Gy cranial RT concurrent | CNS relapse fell (8-10% -> 2-5% average risk); toxicity not in abstract | **NEW** (dosing principle used in (b)) |
| **Mahoney 1998, PMID 9586883, doi 10.1200/JCO.1998.16.5.1712** POG 9005 | 1,218 children | age-adjusted IT MTX or triple IT, 12 intensification courses q2wk | acute neurotoxicity **7.8%** overall (3.7-11.2% by arm), mostly seizures, median 10-11 d after IT; driven by repeated **IV** MTX with low leucovorin and by TIT timing | **NEW** |
| Peyrl 2014, PMID 25017328 | 98 children, brain tumours, Ommaya | **median 36 (2-280)** per reservoir, median 1,336 device-days | 1 infection (1%); 2 early + 2 delayed surgical; one disconnection after 24 accesses; **no leukodystrophic change along the catheter track** | ALREADY IN RECORD (SWEEP_regional D2) |
| PMID 9347977 | 120 adults, leptomeningeal mets (22 NHL), Ommaya | **median 46 administrations + punctures/pt**, 1,110 cycles | aseptic meningitis 52, infection 9, leukoencephalopathy 2 (1.7%), myelopathy 1, reservoir surgery 7 (6%) | ALREADY IN RECORD |
| TT16, PMID 31657981 | 598 children | 13-21 (LR) / 16-27 (SR) IT | no excess seizure/infection with 2 extra IT | ALREADY IN RECORD |
| Masuda 2024, PMID 39269476 | 126 adult CNSL, HD-MTX +/- IT MTX + response-adapted WBRT | IT count dose-dependent | tLE 29.2% at 2 y, HR 4.50, mostly asymptomatic, onset median 3.0 mo | ALREADY IN RECORD |

### Dogs and other veterinary species
| source | what was done | CSF-route doses per animal | complications | status |
|---|---|---|---|---|
| **Ellinwood 2022, PMID 35717448, doi 10.1124/jpet.122.001119 (PMC9426762, full text read via efetch)** tralesinidase alfa, MPS IIIB dogs (BioMarin/Allievex) | ICV catheter (lateral ventricle) + IT-lumbar catheter implanted at ~4 mo; 12 or 48 mg (or vehicle) **every other week for up to 20 months**; ~4 MPS IIIB dogs per group x 3 + unaffected littermates | **~43 biweekly CSF-route doses per dog** (my arithmetic: 20 mo x 30.4 / 14); "**When ICV catheters were no longer patent, doses were infused via the IT-L catheter or via bolus isovolumetric intrathecal cervical (IT-C) injection after removing ~3 ml of CSF**"; "**to address the potential for complications due to catheter patency and port contamination, all administrations were switched to isovolumetric IT-C infusions between doses 7 and 23**" => roughly 20-36 cisterna-magna punctures per dog (my arithmetic) | "Direct CNS administration ... of up to 48 mg of TA biweekly for up to 20 months was **well tolerated and did not generate clinical signs of CNS or systemic toxicity**"; only 2 dogs in one group had patent catheters for PK. Anaesthesia/sedation for each IT-C dose: **not stated in the text extracted (UNVERIFIED)**; per-dog catheter failure counts not extracted | **NEW. Longest canine repeated CSF-access series found: ~43 doses / 20 months.** Different agent (an enzyme), so procedural, not drug, precedent |
| **Crawley 2011, PMID 21550404, doi 10.1016/j.nbd.2011.04.014** MPS IIIA Huntaway | intra-CSF rhSGSH 3 or 15 mg weekly or fortnightly from 8-12 wk to 23 wk of age, 6 dogs | ~6-15 (my arithmetic from the stated window) | "All dogs completed the protocol without incident" | **NEW** |
| **King 2017, PMID 27832416, doi 10.1007/s10545-016-9994-1** | MPS IIIA dogs, repeated cisternal or lumbar bolus vs SynchroMed pump, ~3-6 mo of age | count not in abstract | no safety statement in abstract | **NEW** (route precedent only) |
| **Hemsley 2009, PMID 19699666** | 3 adult MPS IIIA dogs, cisternal rhSGSH x2 or weekly x4 | 2-4 | "moderately severe meningitis" + anti-rhSGSH antibodies (immune response to a human protein) | **NEW** |
| **Kakkis 2004, PMID 15464431, doi 10.1016/j.ymgme.2004.07.003**; Dickson 2010, PMID 20655780 | MPS I dogs: 4 weekly IT ~1 mg rhIDU; long-term IT every 3 months for 12-18 mo | 4; ~4-6 | dose-dependent immune response and meningeal lymphoplasmacytic infiltrate (Kakkis) | **NEW** |
| **Kondagari 2011, PMID 21575633** | canine fucosidosis, 3 monthly intracisternal enzyme injections | 3 | "safe and well-tolerated", no inflammatory reaction in CSF | **NEW** |
| **Rijsdijk 2012, PMID 22139590, doi 10.1097/ALN.0b013e31823cf035** | 17 dogs, IT catheters, methylprednisolone acetate 4 x weekly | 4 | dose-dependent intrathecal inflammatory masses (drug/vehicle-specific) | **NEW** |
| Yaksh lab beagle IT toxicology: adenosine 28 d (10485794), neostigmine 28 d (7856900), baclofen 28 d (Sabbe 1993, PMID 8164885), oxytocin 5 daily (24492326), SP-saporin single bolus, 28/90-d f/u (16500924) | chronic lumbar or cisterna-to-lumbar catheters, vest pumps | continuous 28 d or <=5 boluses | catheter-related fibrosis/inflammation in saline AND drug groups (adenosine, neostigmine); no drug neurotoxicity | **NEW** (but no beagle IT toxicology longer than ~28 d / 90-d follow-up found) |
| Canine CNS lymphoma / MUE intrathecal chemotherapy with repeat counts | PubMed "intrathecal cytarabine AND (meningoencephalitis) AND dogs" returns only Genoni 25041580; MUE cytarabine is given SC/IV, not IT | -- | -- | NOT FOUND (no repeat-count series) |

### Methotrexate neurotoxicity in dogs (question 3)
- PubMed `methotrexate AND (dogs OR beagle) AND (neurotoxicity OR encephalopathy OR leukoencephalopathy OR myelopathy OR arachnoiditis)`:
  28 hits, none is a canine MTX CNS-toxicity study (osmotic-BBBD dog studies, marrow-transplant work, and the PK papers 581360/582316
  already in record). Title search `methotrexate[ti] AND dog/beagle/canine[ti] AND intrathecal/intracisternal/intraventricular` returns
  only 25041580 and 581360. **Canine intrathecal-MTX toxicology and canine MTX leukoencephalopathy: NOT FOUND.**
- Nearest canine datum, **NEW: Tiller-Borcich 1987, PMID 3575649 (Radiat Res 110:161)**: normal dogs, 10/15/30 Gy single fraction to one
  hemisphere; dose-dependent white-matter oedema to necrosis resembling human delayed radiation necrosis; "**many of the changes ascribed
  to combined treatment with methotrexate and radiation in humans are induced in the normal dog brain by radiation alone**", and the dog
  is "a suitable model of the human brain for studying radiation brain injury". This supports transferring human white-matter injury data
  to the dog; it is not an MTX measurement.

### Radiation + repeated IT methotrexate, by timing (question 4)
- Masuda 39269476 (record): WBRT (response-adapted) NOT a risk factor; IT MTX count was (HR 4.5); onset median 3.0 mo.
- **NEW: DeAngelis 2002, RTOG 93-10, PMID 12488408, doi 10.1200/JCO.2002.11.013**: 98 PCNSL pts, 5 cycles HD-MTX 2.5 g/m2 +
  **intraventricular MTX 12 mg** (number of IT doses per patient not in the abstract) **before 45 Gy WBRT**: **severe delayed neurotoxicity 12 (15%), 8 died**;
  age >=60 the dominant factor. Sequence here is chemo then high-dose RT; WBRT dose ~2x the model's 23.4 Gy.
- **NEW: Bleyer 1981, PMID 6948611 (Cancer Treat Rep 65 Suppl 1:89)**: classification of MTX/RT neurotoxicity; "**combinations including
  CNS irradiation appear to be the most neurotoxic**"; single modalities safest. No numbers in abstract.
- **NEW: Bleyer 1983, PMID 6366138**: thousands of children received 18-24 Gy cranial RT **concurrent** with 6 IT MTX doses in
  consolidation (CCG-141A/160); neurotoxicity by timing not in abstract.
- Record (SWEEP_rt2 Q2): 23.4 Gy/13 fx cohorts without severe white-matter change (24101038, 35772168); recommendation there: RT first,
  then the IT series, not concurrent.
- A primary source quantifying neurotoxicity of IT MTX given AFTER vs DURING cranial RT, by dose count: **NOT FOUND this pass**.
- Canine RT + repeated IT MTX series: none (record statement stands; 6547126 is IT cytarabine, 4 dogs, 1984).

### Not verified this pass
AIEOP-BFM, UKALL 2003/2011 and COG per-child IT counts (record has EORTC 58951: 10-19); per-risk-group IT counts in Total XV beyond
Bhojwani's "13 to 25"; Ellinwood 2022 anaesthesia per IT-C dose and per-dog device-failure numbers (Table 1/supplement not extracted);
Peyrl 2014 drug mix per instillation (the 280 maximum is not known to be all MTX); a per-dose arachnoiditis rate for IT MTX.

## (b) Proposed written transfer: tolerability of 30-45 intrathecal MTX doses in a dog

**Claim.** A dog can receive up to **45** preservative-free methotrexate doses into the CSF, **2.5 mg each, no more often than every
10 days**, over 12-16 months, **after** completing the 23.4 Gy course and **without concurrent systemic high-dose methotrexate**, with a
drug-related neurotoxicity burden no worse than the human long-course experience: transient clinical neurotoxicity in ~4-8% (re-dosable
in 12/13), and mostly asymptomatic white-matter change.

**Grade: TRANSFERRED** for the drug side (human -> dog); **MEASURED-in-dog (procedure only, different agent)** for the CSF-access count.
Not MEASURED for methotrexate in dogs (no canine IT-MTX series beyond single doses; no canine MTX neurotoxicity study exists).

**Why the transfer is justified (written, each step with its direction):**
1. **Dose count is inside human precedent.** 30-45 doses sits at or below the human medians for long CSF-directed courses: 46
   administrations/patient in leptomeningeal Ommaya therapy (9347977), 36 planned ICV MTX doses in 6 months in children <4 y (HIT 2000,
   21636711), median 36 (max 280) Ommaya instillations (25017328); paediatric ALL gives 13-27 over ~2.5 y (24550419, 31657981).
   Direction: neutral-to-favourable; the dog course is spread over 12-16 months, slower than HIT 2000 (36 in 6 months) and than
   leptomeningeal induction (twice weekly).
2. **Per-dose CSF concentration matches or is below the human standard.** Human IT MTX is dosed by CNS volume (Bleyer 1983,
   6366138): 12 mg into ~150 mL adult CSF = 0.080 mg/mL. Dog CSF is measured (record: V = 1.39 x BW + 17.5 mL, 28244335). 2.5 mg gives
   0.102 mg/mL at 5 kg, **0.080 at 10 kg**, 0.055 at 20 kg, 0.042 at 30 kg, 0.034 at 40 kg (my arithmetic). So the flat 2.5 mg is at or
   below the human per-volume dose for dogs >=10 kg; below 10 kg scale the dose to <=0.08 mg/mL x V.
3. **Clearance between doses is the same in both species, so nothing accumulates.** CSF MTX terminal t1/2 5.2 h in dogs (581360) vs
   5.7 h in humans (2809687) (record). A 10-14-day interval is >=46 half-lives; each dose is an independent pulse, as in the human series.
   Bleyer 1978 (638249) shows neurotoxicity tracks peak/sustained CSF concentration and cumulative dose, and that more frequent smaller
   doses are less toxic (1/8 vs 7/10) -- the dog course is a low-peak, widely spaced schedule.
4. **Cumulative exposure per mL of CSF is inside the human range.** 45 x 2.5 mg / 45.3 mL = 2.48 mg/mL (20 kg dog); 30 doses = 1.66.
   Human: TT16 maximum 27 x 12 mg / 150 mL = 2.16 mg/mL; leptomeningeal median 46 x 12 mg / 150 mL = 3.68 mg/mL (assuming all doses
   were 12 mg MTX, an upper bound). A 10 kg dog at 45 doses reaches 3.58, still below the leptomeningeal median; a 5 kg dog at 45 (4.6)
   is above it, hence the small-dog scaling in item 2.
5. **The main human co-driver is absent in the dog program.** Human leukoencephalopathy and acute neurotoxicity rise with systemic MTX
   exposure (Bhojwani 24550419: plasma MTX:leucovorin ratio; Mahoney 9586883: repeated IV MTX; HIT/TT/Masuda all with HD-MTX). The
   canine program gives no systemic HD-MTX, so the human rates are an upper bound for this element. Direction: favourable.
6. **Dose count does not consistently drive white-matter injury.** Two cohorts found no count effect (Merlin 37171700: p=0.698 for
   cumulative ICV dose vs LE grade; 36230611: >12 vs <=12 IT, no MRI difference), one found a dose-number effect (Masuda 39269476,
   HR 4.5, mostly asymptomatic). Take Masuda as the conservative bound: the expected cost of more doses is more asymptomatic white-matter
   change, not more symptomatic disease, and symptomatic events were re-dosable in 12/13 (24550419).
7. **The dog white-matter response transfers.** The canine brain reproduces the human delayed white-matter radiation lesions, including
   those ascribed to MTX + RT in humans (3575649), so human white-matter injury data are a reasonable model for the dog; no evidence
   points to greater canine sensitivity (and none to lesser).
8. **The procedure count is within canine experience.** Dogs have received ~43 CSF-route doses every other week for 20 months via ICV
   catheter then cisternal (IT-C) injection, "well tolerated" without clinical CNS signs (35717448), extending the record's 20-28 dose
   port series (25257657, PMC4263309). A 45-dose course every 10-14 days lasts 15-21 months, similar.

**Limits this transfer supports (not beyond):**
- **Max doses: 45** (at or below the human leptomeningeal median of 46 and the canine ~43-dose procedural series). Past ~46 the human
  medians no longer cover it and the dose-number hazard (Masuda) is unbounded by data here.
- **Interval: >=10 days** (10-14 d as the model uses). Shorter intervals are covered by human data (twice weekly) but not by the
  canine procedural series.
- **Dose: 2.5 mg preservative-free MTX for dogs >=10 kg; <=0.08 mg/mL x CSF volume (1.39 x BW + 17.5 mL) below 10 kg.** MTX alone
  (Genoni's MTX + cytarabine 100 mg is a different exposure; adding cytarabine is not covered by this transfer).
- **Route: ventricular catheter to subcutaneous port (preferred) with cisterna-magna injection as the planned fallback** (exactly what
  35717448 did). Lumbar delivery is not recommended for the brain target (record: lumbar-to-cisternal ratio ~1:0.017, PMC3514653).
  Remove ~1 mL CSF before an isovolumetric injection, as in both canine protocols.
- **Sequence: finish the 23.4 Gy course first; no IT dose during radiation; no systemic HD-MTX at any point.**
- **Monitoring:** MRI at 3 months into the series (human tLE onset median 3.0 mo) and every ~6 months; hold or space out doses on
  new white-matter signal with clinical signs (rechallenge precedent 12/13).

## (c) What would make it fail
1. **Procedural cumulative mortality, not the drug.** If every dose needs general anaesthesia plus a cisternal puncture, compounding the
   record's per-event figures gives (my arithmetic, 1-(1-p)^n): puncture major complication 0.146% (40526210) -> 4.3% at 30 doses,
   6.4% at 45; anaesthesia 0.11% healthy (9657167) -> 3.2% / 4.8%; 0.5% sick-dog rate (18658000) -> 14% / 20%; **combined 7.4-17.7% at
   30 doses and 10.9-25.3% at 45.** This is larger than the "few percent" in `LYMPHOMA_UNIVERSE.md` K.5/K.6 (which counted the 13 RT
   anaesthetics plus 12-20 IT doses). The transfer holds only if most doses go through a port under sedation or without anaesthesia;
   whether the 20-month canine series used anaesthesia per IT-C dose is UNVERIFIED. If ports fail early (they did: 35717448 switched all
   dogs to cisternal injection between doses 7 and 23; West 24694254: 67% lumbar patency at 30 d), the course becomes 20-40 anaesthetised
   punctures and this item fails at the sick-dog rate.
2. **Device infection / meningitis / hydrocephalus.** Canine ports: 2 dogs euthanised for meningitis + obstructive hydrocephalus
   (25257657, record). Human reservoirs: 15% infection, 27% complications, 18% removal in HIT 2000 (26346136); 1% with strict aseptic
   protocol (25017328); 0/501 accesses with prophylactic intraventricular vancomycin (40719464, record). Fails if an aseptic access
   protocol cannot be run at the treating clinic.
3. **Symptomatic leukoencephalopathy.** The transfer assumes human-like behaviour: mostly asymptomatic, transient clinical events. It
   fails if MTX is given concurrently with or within weeks after RT at higher doses (RTOG 93-10: 15% severe delayed neurotoxicity, 8
   deaths, with 45 Gy after IT + HD-MTX, 12488408), if systemic HD-MTX is added, or if the dog is small and flat-dosed (item 2 of (b)).
4. **Any count above 45 or interval below 10 days** (for example, the pessimistic-IC50 schedule needing more doses). Outside the limits.
5. **A canine-specific MTX neurotoxicity.** No canine IT-MTX toxicology exists; one dog in an IT-chemo case review died of tentorial
   herniation "believed" secondary to IT chemotherapy (record, 37732143 ref 13). A first-dose MRI/neurological check and the 3-month MRI
   are the detection points. Transporter differences (for example ABCB1-1Delta breeds) are untested for IT MTX.
6. **Arachnoiditis.** No canine series; human chemical arachnoiditis/aseptic meningitis occurred in 52 events across 120 LM patients
   (9347977, record). Not a lethal mode in the human data, but a reason to hold dosing.

## Bottom line for `failing()`
- Drug-side tolerability of up to 45 doses (>=10-d interval, 2.5 mg, MTX alone, after RT, no HD-MTX): **TRANSFERRED** with the written
  justification above. Under the stated bar it is no longer ASSUMED.
- The residual that can still fail is **procedural**: the cumulative anaesthesia + puncture/device risk of 30-45 accesses
  (7-25% depending on route and anaesthetic risk). That is a quantity with measured per-event inputs (DERIVED), not an absence of data,
  and it is decided by route: a working port dosed without anaesthesia keeps it low; repeated anaesthetised cisternal puncture does not.
  Code path that would need to change to reflect this: `lymphoma_standard_audit.lawful_brain_items` (re-grade the B-cell dose-count
  item from ASSUMED to TRANSFERRED with the limits above) and the toxicity budget, which carries no procedural-mortality term today.
