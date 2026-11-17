# Can 29-45 intrathecal methotrexate doses be given to a dog WITHOUT a general anaesthetic each time? (agent notes, 2026-11-16)

Question (from `SWEEP_it_longcourse.md` (c)-1 and `LYMPHOMA_UNIVERSE.md` lines 630/634): the B-cell brain closure needs **29-45 intrathecal
methotrexate doses**. The drug side is **TRANSFERRED** (`SWEEP_it_longcourse.md` (b)). The residual is **procedural**: if every dose needs a
general anaesthetic plus a puncture, cumulative mortality is ~7-18% at 30 doses and ~11-25% at 45 (`LYMPHOMA_UNIVERSE.md:630`). The record
already names the deciding measurement: *"whether a canine ventricular port can be dosed awake for 30+ doses"* (`LYMPHOMA_UNIVERSE.md:634`).
This sweep answers that, plus the depot / fewer-events alternative.

Bar (CLAUDE.md): real data **or** a rigorous model; a cross-species / cross-disease transfer is acceptable if justified in writing (rule 11,
standing standards). Absence of canine data is not a reason to exclude an option (rule 13).

## 0. Record check (done before searching; rules 1 and 10)

Searched by keyword and by PMID: `docs/universe/SWEEP_it_longcourse.md`, `SWEEP_itmtx2.md`, `SWEEP_nm600_itmtx.md`, `SWEEP_regional.md`,
`SWEEP_rt2.md`, `SWEEP_brain_access.md`, `SWEEP_exists.md`, `SWEEP_cnsregimens.md`, `docs/LYMPHOMA_UNIVERSE.md`, `docs/LYMPHOMA_STATUS.md`,
`docs/research_notes/`, and `src/`.

**ALREADY IN RECORD — not re-reported as new:**

| item | where |
|---|---|
| Peyrl 2014 PMID 25017328: 98 children, 5,472 Ommaya instillations, median 36/reservoir (2-280), 199,956 device-days, **1 infection**, 2 early + 2 delayed surgical revisions, one disconnection after 24 accesses, "only specially trained personnel … strict aseptic conditions" | `SWEEP_it_longcourse.md:11`, `SWEEP_regional.md` D2 |
| Vuillemenot 2014 PMID 25257657 + Katz 2014 PMC4263309: TPP1-null Dachshunds, ICV + IT-L catheters to **subcutaneous titanium ports**, every other week, ~20-28 doses over 8-11 months; 2 dogs euthanised for meningitis + obstructive hydrocephalus; catheters occluded/migrated | `SWEEP_itmtx2.md:125`; `SWEEP_it_longcourse.md:17` |
| West 2014 PMID 24694254: chronic lumbar intrathecal catheter + vascular access port **"in conscious dogs"**; patency 67% >30 d (first surgery), 86% with repair/replacement | `SWEEP_itmtx2.md:126` (the word "conscious" is already there) |
| Ellinwood 2022 PMID 35717448: MPS IIIB dogs, ICV + IT-L catheters, QOW up to 20 months (~43 doses); all administrations switched to isovolumetric **IT-cervical** injection between doses 7 and 23; anaesthesia per IT-C dose **UNVERIFIED** | `SWEEP_it_longcourse.md:38` |
| Dickson 2007 PMID 17321776: 19 dogs, 4 cisternal injections, 1 fatal brainstem haemorrhage | `SWEEP_it_longcourse.md:17`, `LYMPHOMA_UNIVERSE.md:526` |
| King 2017 PMID 27832416: MPS IIIA dogs, repeated cisternal/lumbar bolus **vs SynchroMed II pump** | `SWEEP_it_longcourse.md:47` ("route precedent only") |
| Genoni PMID 25041580 / Lyseight PMC10507905 (37732143): canine IT dose = 100 mg ara-C + **2.5 mg MTX** flat, cisternal puncture, 1 mL CSF withdrawn, **"under GA"** | `SWEEP_itmtx2.md:31` |
| Bleyer 1978 PMID 638249: 12 mg/m² single doses vs 1 mg q12h x6; **neurotoxicity 7/10 vs 1/8 (p<0.05) at equal efficacy**; toxicity tracks CSF concentration and cumulative dose | `SWEEP_it_longcourse.md:28` and (b)-3 |
| Canine CSF MTX terminal t½ **5.20 h** (PMID 581360); human intra-Ommaya 5.7 h (PMID 2809687) | `SWEEP_itmtx2.md:4, 67` |
| Canine CSF collection major complication **11/7,545 = 0.146%**, 8 of 11 euthanised (PMID 40526210); Fentem 0/108 deteriorations (PMID 36906911) | `SWEEP_regional.md:233`, `SWEEP_itmtx2.md:128` |
| Canine anaesthetic mortality **0.1-0.2% healthy / 0.5-2% sick** (PMID 18658000, Brodbelt 2008 Vet J review) and **0.11% death, 2.1% complications in 8,087 dogs** (PMID 9657167, Dyson 1998); ASA 3-5 raises complication odds 2.5x | `SWEEP_rt2.md:96` |
| **Per-tap** Ommaya infection: historical 10.25% of 322 patients = **1.71% of 1,932 treatments**; **0% in 0/501 treatments** with 10 mg intraventricular vancomycin co-administered (PMID 40719464). H-port vs Ommaya infection 14/152 vs 12/89 (PMID 38061763) | `SWEEP_regional.md:102, 250-251` |
| DepoCyt (liposomal cytarabine) randomised trial PMID 10506606: **50 mg q2wk vs free ara-C 50 mg 2x/wk**, response 71% vs 15% (P=.006), all vs 53% completed induction, dexamethasone 4 mg bid d1-5 each cycle, AEs headache + arachnoiditis | `SWEEP_regional.md:74, 213`; cited in `lymphoma_grounded_inputs.py:317` |
| Depot cytarabine as a **modality**: EVALUATED, EXCLUDED — division-gated and dCK-dependent, cannot close the quiescent-progenitor escape E2 | `LYMPHOMA_UNIVERSE.md:144` |

Everything below marked **NEW** was not in the record by PMID, DOI or keyword.

## (a) How was each dose actually given? Anaesthesia vs sedation vs awake

### Dogs

| source | device / route | how each dose was given | status |
|---|---|---|---|
| **Katz 2014, PMID 24938720, PMC4263309, doi 10.1002/jnr.23423** (the canine CLN2 ERT study; paper already in record) | ICV catheter → paracervical subcutaneous titanium port; IT-L catheter → paralumbar port; 2 h or 4 h infusions QOW from ~2.5 months to end-stage (51-87 weeks of age) | **"Dogs were _sedated_ during ITL or ICV infusions of rhTPP1 as previously described (Vuillemenot et al., 2011)."** And, for the fallback route: **"When this occurred, the treatment administration was continued by bolus injection of the agent into the subarachnoid space at the CM over a 2-min period. For the bolus injections the dogs were _anesthetized_ as previously described (Vuillemenot et al., 2011)."** General anaesthesia was additionally used for MRI | **NEW (the statement). This is the single most load-bearing finding in this sweep: in a real canine CSF-port programme, PORT doses were SEDATED and only CISTERNAL-PUNCTURE doses were ANAESTHETISED** |
| same paper, device outcomes | 20 dogs implanted (Table I); 9 treated affected dogs | **"Among the nine treated dogs, five were terminated prior to reaching disease end stage because of complications related to the catheters or to the dose administration procedures and not to either disease progression or toxicity of the rhTPP1."** Causes: meningitis + obstructive hydrocephalus (2 early at 48 mg, 2 at 57/63 wk at 16 mg), and one hydrocephalus from a **lesion along the ICV catheter track** at 87 wk. The paper attributes these to **foreign-body reaction to catheters after long indwelling periods** and to **growth of the cranial cavity** migrating the ICV tip | **NEW (the 5/9 figure and the attributions)** |
| **Barni 2020, Acta Scientiae Veterinariae 48:1738, doi 10.22456/1679-9216.102523** (full text read) | 6 dogs with multicentric lymphoma, BardPort M.R.I. 6.6 Fr jugular **subcutaneous vascular access port**, Madison-Wisconsin protocol over 25 weeks, port left in place afterwards with 4-weekly heparinisation | Implantation under inhalational anaesthesia + lidocaine 4 mg/kg block. **Each chemotherapy access: hair shaved, antisepsis, 20 G x 20 mm Huber needle into the reservoir, aspirate for blood return, infuse. "The owner restrained the animal during all the procedure." No sedation, no anaesthesia and no local anaesthetic appear anywhere in the access procedure.** Handling time **110.6 ± 8.4 s** (port) vs 219.2 ± 24.7 s (peripheral catheter), P<0.001. Systolic BP **fell** from arrival to immediately-after-puncture in the port group and **rose** in the catheter group (significant) | **NEW. Direct canine evidence that a subcutaneous port is punctured repeatedly in a fully conscious dog with owner restraint only, and is measurably LESS stressful than a peripheral IV catheter** |
| **West 2014, PMID 24694254, doi 10.3109/08941939.2014.882450** | 3.5 Fr lumbar intrathecal catheter → vascular access port | **"a reliable and reproducible chronic system was developed to collect lumbar CSF from conscious dogs"** | **ALREADY IN RECORD** (`SWEEP_itmtx2.md:126`) — the "conscious" wording is already recorded; re-stated here because it is the second canine conscious-CSF-port datum |
| **Culp 2010, PMID 20550447, doi 10.2460/javma.236.12.1322** | 46 cats + 126 dogs, subcutaneous vascular access ports during **fractionated radiotherapy** | Accessed during the radiotherapy anaesthetics (risk factors include "lack of administration of **propofol** during anaesthetic induction", OR 19.15 for major complications), so **not** awake. Device burden: **18 major and 36 minor complications in 172 animals** (10.5% / 20.9%) | **NEW.** Establishes that subcutaneous ports are routine in veterinary oncology for repeat access, and gives a device-failure rate over a course of fractions |
| **Ellinwood 2022, PMID 35717448, PMC9426762** (full text re-read this pass) | ICV + IT-L catheters to ports; ~43 QOW doses to 20 months; switched to isovolumetric IT-cervical between doses 7 and 23 | **Anaesthesia/sedation per dose is NOT STATED anywhere in the paper.** The only statement is about surgery: "Surgical and postsurgical recovery and monitoring procedures were designed and approved to ensure full analgesia and pain management." | **NEW as a verified negative** — the record flagged this as UNVERIFIED; it is now confirmed that the primary text does not say |
| Vuillemenot 2011, PMID 21784683, doi 10.1016/j.ymgme.2011.06.018 | 2 dogs, 4 monthly IT administrations of 32 mg TPP1 via the **cerebellomedullary cistern** | This is the paper Katz 2014 cites for both the sedation and the anaesthesia protocols. Full text is not in PMC; **the protocol text itself was NOT RETRIEVED** | **NEW (citation), protocol text UNVERIFIED** |
| Genoni PMID 25041580 / Lyseight PMC10507905 | 112 dogs + 8 cats, percutaneous cisternal IT ara-C ± MTX | **Under general anaesthesia**, 1 mL CSF withdrawn, injected over 1 min; 1 seizure during anaesthetic recovery | **ALREADY IN RECORD** (`SWEEP_itmtx2.md:31, 70`) |
| King 2017, PMID 27832416 | MPS IIIA Huntaway dogs; **SynchroMed II pump** on a spinal infusion cannula vs repeated cisternal or lumbar bolus, ~3-6 months of age | Anaesthesia per bolus **not in the abstract**; full text not retrieved. Result: continuous pump infusion **reduced primary substrate but was NOT as efficacious as repeated cisternal or spinal bolus** — less reduction of secondary substrate (GM ganglioside) in deep cerebral cortex, and "little impact on microgliosis" | **ALREADY IN RECORD (route); the pump-vs-bolus efficacy comparison is NEW to the record** |
| Canine CSF ports/ICV dosed **fully awake** (no sedation) for repeated **drug** administration | — | **NOT FOUND.** No canine series dosed a CSF port awake. The awake canine precedent is for a **vascular** port (Barni) and for **CSF sampling** (West); the CSF-**dosing** precedent is **sedation** (Katz) | **NOT FOUND — stated plainly** |

### Other species (procedural transfer anchors)

| source | what was done | status |
|---|---|---|
| **Gilberto 2003, PMID 12906404** (Contemp Top Lab Anim Sci 42:53-9, Merck) | 3.5 Fr fenestrated silicone catheter 1.0 cm into the **cisterna magna** → **titanium port between the scapulae**, "to permit easy access for sampling CSF **in a conscious, chaired rhesus monkey**"; CSF collected **consistently for over 18 months**. Notes that chronic CSF models "previously have been established for nonhuman primates **and canines**" | **NEW. The closest existing model to what the lymphoma programme needs: a cisternal catheter to a subcutaneous port, tapped awake, for >18 months** |
| **UC San Diego Health Standardized Procedure SP006, "Intraventricular Chemotherapy via Ommaya Reservoir (Adult, Peds)"**, revised 2/26/2014 and 9/28/2016, approved by the Medical Staff Executive Committee 3/20/2014 and 10/7/2016 (PDF read) | Performed by **Nurse Practitioners / Certified Nurse Midwives**, inpatient **or outpatient** per privileges. Materials: preservative-free **methotrexate 12 mg** and/or Ara-C 50 mg and/or hydrocortisone 50 mg, standard LP tray, povidone iodine, **25 gauge butterfly needle** and stopcock. Procedure: compress bulb twice, scrub x3 with povidone iodine (dry 2 min), drape, **"A 25 gauge butterfly needle is inserted directly into reservoir at a perpendicular angle to skin, and a volume of cerebrospinal fluid equal to chemotherapy drug volume (usually 2 - 6 ml) is removed"**, inject over ~5 min, flush 1 mL, spot bandage. **No anaesthetic, no sedative and no local anaesthetic appears in the materials list or in any of the 13 procedure steps.** | **NEW. This is the explicit institutional statement that an Ommaya tap is an awake, un-anaesthetised, nurse-performed clinic procedure** |
| Peyrl 2014, PMID 25017328 | 5,472 instillations, **1 infection**. Per-access arithmetic (mine): infection **1/5,472 = 0.0183% per access**; surgical revision 4/5,472 = **0.073% per access**; mechanical disconnection after 24 accesses in one device | source ALREADY IN RECORD; **per-access rates are NEW (my arithmetic)** |
| Trifoi 2025, PMID 40719464 | **1.71% per treatment** historically (1,932 treatments) vs **0/501 treatments** with 10 mg intraventricular vancomycin per dose | **ALREADY IN RECORD** (`SWEEP_regional.md:251`) |
| Pels 2003, PMID 14597744, doi 10.1200/JCO.2003.04.056 (Bonn pilot/phase II, 65 PCNSL) | Intraventricular MTX + prednisolone + ara-C with systemic HD-MTX/ara-C; **Ommaya infection in 12/65 patients (19%)**; permanent cognitive dysfunction 2/65 (3%) | **NEW** (the Bonn protocol is in record via 32989105/33324883; this per-patient infection figure is new) |
| Human **per-tap haemorrhage** rate | **NOT FOUND.** No series reporting intracranial haemorrhage per Ommaya access was located. The haemorrhage risk in the record is from **needle insertion into brain** (percutaneous cisternal puncture: Dickson 17321776, 1 fatal brainstem haemorrhage in 19 dogs), which a reservoir tap does not involve — the needle enters a silicone dome under the scalp | **NOT FOUND — stated plainly** |

### Anaesthetic / sedation mortality per event (question 5)

| source | figure | status |
|---|---|---|
| **Brodbelt 2008, PMID 18466167, doi 10.1111/j.1467-2995.2008.00397.x — CEPSAF, the primary prospective cohort** | 117 UK practices, **98,036 dogs** anaesthetised **and sedated**, June 2002-June 2004. Risk of **anaesthetic- and sedation-related death within 48 h: dogs overall 0.17% (1 in 601, 95% CI 0.14-0.19%); healthy dogs (ASA 1-2) 0.05% (1 in 1,849, 95% CI 0.04-0.07%); sick dogs (ASA 3-5) 1.33% (1 in 75, 95% CI 1.07-1.60%)**. **47% of canine deaths were postoperative.** | **NEW.** The record carried only the derivative review (18658000: 0.1-0.2% / 0.5-2%) and Dyson 1998 (9657167: 0.11%). CEPSAF is the primary source, has the tightest CIs, and its **0.05% healthy-dog figure is 2x lower** than the 0.11% the record has been compounding |
| **Brodbelt 2008, PMID 18828720, doi 10.2460/javma.233.7.1096** (CEPSAF case-control, 148 cases / 487 controls) | Increased odds of anaesthetic-related death with: **increasing ASA grade, urgency, age, intended duration of the procedure**; **decreasing body weight**; **major vs minor procedure**; and injectable induction + halothane or inhalant-alone maintenance (vs injectable + isoflurane) | **NEW** |
| A **sedation-only** mortality figure for dogs, separable from general anaesthesia | **NOT FOUND.** CEPSAF explicitly pools "anaesthetic and sedation-related death" and reports no separate sedation denominator or numerator. Searches for sedation-specific canine mortality returned nothing usable. | **NOT FOUND — stated plainly. This is the one number that would make the sedation route quantitative rather than directional.** |

## (b) Proposed written transfer

**Claim.** In a dog, **doses given through an implanted subcutaneous CSF reservoir can be given with the dog conscious or under light
sedation, not under general anaesthesia**, and the number of general anaesthetics in a 29-45 dose intrathecal methotrexate course can
therefore be reduced from one per dose to **two to three in total** (implantation, plus one or two expected revisions), **provided** the port
is patent and the aseptic access protocol below is run. A general anaesthetic is required only for the **cisternal-puncture fallback**.

**Grade: TRANSFERRED** (not MEASURED). Specifically:
- **"A CSF port dose in a dog does not require general anaesthesia": MEASURED IN DOGS, for sedation** — Katz 2014 (PMC4263309) states that
  ICV and IT-L port infusions of 2-4 h were given to **sedated** dogs, biweekly, for 8-20 months, and that only the cisternal-bolus fallback
  used anaesthesia. That is the exact comparison the record asked for, in the exact device, in dogs.
- **"…and can be done fully awake": TRANSFERRED**, from three directions, none of them a canine CSF-port dose:
  (i) awake subcutaneous **vascular** port puncture in conscious dogs with owner restraint only, 20 G Huber needle, 111 s, with blood pressure
  *falling* on puncture (Barni 2020, doi 10.22456/1679-9216.102523) — same device class, same needle class, same species, different compartment;
  (ii) awake **CSF** sampling from a lumbar catheter + port in **conscious dogs** (West 24694254) and from a **cisterna magna** catheter + port
  in **conscious, chaired rhesus monkeys for >18 months** (Gilberto 12906404) — same compartment, same device, awake, but sampling not dosing;
  (iii) human practice: an Ommaya tap with a 25 G butterfly, 2-6 mL CSF out and 12 mg methotrexate in, is a **nurse-practitioner outpatient
  procedure with no anaesthetic of any kind in the written standardized procedure** (UCSD SP006), performed 5,472 times in 98 children with one
  infection (Peyrl 25017328).
- **Direction of each difference (rule 15).** Dog vs human: the dog cannot consent and may move, which pushes **toward** needing sedation, not
  anaesthesia — Barni shows owner restraint suffices for a scalp-equivalent subcutaneous dome in a non-aggressive dog. Vascular port vs CSF
  port: a CSF port is over the skull or paralumbar fascia rather than the neck, and a mis-seated needle leaks drug subcutaneously rather than
  perivascularly — direction neutral for pain, **worse** for consequence of failure, which argues for sedation over fully awake. Sampling vs
  dosing: drawing CSF and injecting into CSF use the same needle in the same dome; the dosing step adds ~5 min of still time (UCSD), which
  pushes toward light sedation for a long infusion and is irrelevant for a 1-2 min bolus. Infusion duration: Katz's sedated doses were **2-4 h
  infusions**; the methotrexate dose is a **1-2 min bolus** (Genoni/Lyseight), i.e. two orders of magnitude shorter, so if 2-4 h was achievable
  under sedation a 2-minute bolus is achievable under sedation or awake. **Transfer as a ceiling on what is needed: sedation suffices; awake is
  plausible but is a floor claim resting on the vascular-port and sampling data, not on a canine CSF-dosing series.**
- **What is NOT transferred.** No claim that sedation is *quantitatively* safer than general anaesthesia in dogs: CEPSAF pools them
  (18466167) and no separable sedation mortality exists (NOT FOUND). The reduction below is claimed only for the route that **eliminates** the
  anaesthetic event, and the sedation route is reported separately as directional.

### Revised cumulative procedural mortality

Per-event inputs: CEPSAF **0.05%** healthy / **1.33%** sick (18466167, NEW, replaces the 0.11% Dyson figure as the primary anchor; Dyson's
0.11% shown for continuity); percutaneous CSF puncture major complication **0.146%** (40526210, record). All compounded as 1-(1-p)^n (my
arithmetic; "mortality" for the anaesthetic term, "major complication" for the puncture term, kept separate from infection).

| route (45 doses unless stated) | GA events | cumulative mortality, ASA 1-2 (0.05%) | ASA 1-2 at Dyson 0.11% | cumulative, ASA 3-5 (1.33%) |
|---|---|---|---|---|
| **Current worst case in record:** GA + cisternal puncture every dose, 30 doses | 30 | 5.71% | 7.39% | 35.95% |
| GA + cisternal puncture every dose, 45 doses | 45 | 8.44% | 10.88% | 48.74% |
| **Hybrid:** port awake/sedated, 25% of doses fall back to GA + cisternal (11 of 45), + 2 device GAs | 13 | **2.23%** | — | **17.31%** |
| **Hybrid:** 50% fall back (22 of 45), + 2 device GAs | 24 | **4.31%** | — | **29.77%** |
| **Target route:** port awake or sedated for all 45 doses; GA only for implantation + 1 expected revision | **2** | **0.10%** | 0.22% | **2.64%** |
| same, implantation + 2 revisions | 3 | 0.15% | 0.33% | 3.94% |

So the transfer supports replacing **~7-18% (30 doses) / ~11-25% (45 doses)**, as `LYMPHOMA_UNIVERSE.md:630` states it, with **0.10-2.64%** —
roughly a **20- to 80-fold reduction in the anaesthetic term**, and it moves the dominant risk from anaesthesia to **the device**.
Note the CEPSAF numbers widen the bracket at both ends: the healthy-dog figure is half what the record compounded (so the optimistic case is
better than recorded), and the measured sick-dog figure of 1.33% is worse than the 0.5% the record used (so GA-per-dose is worse than
recorded — 49% at 45 doses, not 25%). The conclusion is unchanged in direction and larger in magnitude.

### The cost that replaces it: per-access and per-device-month terms (kept separate, rule 5)

| term | per-event | at 30 accesses | at 45 accesses | source |
|---|---|---|---|---|
| Reservoir infection, **strict aseptic protocol, trained staff only** | 0.0183% | 0.55% | 0.82% | Peyrl 25017328 (record); per-access arithmetic mine |
| Reservoir infection, **ordinary practice** | **1.71%/treatment** | 40.4% | **54.0%** | Trifoi 40719464 (record); arithmetic mine |
| Reservoir infection, **10 mg intraventricular vancomycin co-administered each dose** | 0/501 treatments | — | — | Trifoi 40719464 (record). A cumulative figure is not quoted: 0/501 bounds the rate loosely (95% upper ~0.7%/access) |
| Surgical revision (not death) | 0.073% | 2.2% | 3.2% | Peyrl; arithmetic mine |
| **Canine device-related loss over 8-20 months of indwelling CSF catheters** | — | **5 of 9 treated dogs terminated for catheter- or administration-related complications** | same | Katz 2014 PMC4263309 (NEW figure) |

The **100-fold spread** between Peyrl and Trifoi is the whole game: it is not biology, it is whether a trained-personnel aseptic access
protocol (and vancomycin) is run. That makes it a **decidable condition**, not an open gap.

The canine 5/9 figure is the honest upper bound and must be reported as an upper bound, with the reasons (rule 15 direction statement):
those dogs were **implanted at ~2 months of age with TWO catheters**, so the ICV tip migrated as the cranial cavity grew (the paper says so);
they had a **progressive fatal neurodegenerative disease**; they received a **foreign human protein** that caused anaphylaxis and anti-drug
antibodies; and the catheters were indwelling for 8-20 months. A single ventricular catheter in a skeletally mature dog receiving a small
molecule removes every one of those four factors. Direction: all four push the canine figure **down**. No measured canine figure for an adult
single-catheter CSF port exists (**NOT FOUND**).

### Access protocol the transfer is conditional on (all elements from sources above)

1. **Single** ventricular catheter to a subcutaneous reservoir, implanted in a **skeletally mature** dog (removes the growth-migration mode,
   Katz); cisterna-magna catheter + scapular port is the alternative with the longest awake precedent (Gilberto, in primates).
2. Access by **named trained personnel only, to a written protocol** — the explicit determinant of the 1% vs 19% vs 0.018% infection spread
   (Peyrl vs Pels 14597744 vs ordinary practice).
3. **Clip, povidone-iodine x3 with a 2-minute dry time, drape, non-coring needle** (25 G butterfly per UCSD; 20 G x 20 mm Huber per Barni),
   aspirate to confirm, remove CSF equal to the injectate volume, inject over 1-5 min, flush, spot bandage.
4. **10 mg intraventricular vancomycin with each dose** (Trifoi 40719464, 0/501).
5. **Light sedation as the default, conscious with owner restraint as the de-escalation** once the dog has tolerated several accesses — this is
   the order Katz (sedated) and Barni (conscious) jointly support; do not start awake.
6. **Cisternal puncture under GA as the declared fallback**, as Katz and Ellinwood both did, with the dose count that falls back entering the
   hybrid rows of the table above.
7. Port patency check before each dose; Katz used contrast CT, which is itself an anaesthetic — substitute aspiration-for-CSF-return
   (Barni's test, awake) and reserve imaging for failures.

## (c) Depot / fewer-dosing-events options, with a verdict on each

| option | does it cut dosing events at equal exposure? | obtainable? | tier (rule 13) | verdict |
|---|---|---|---|---|
| **Liposomal cytarabine (DepoCyt / DepoCyte)** | **Yes, proven 4-fold**: 50 mg once every 2 weeks vs free ara-C 50 mg twice weekly, with response **71% vs 15%** and **100% vs 53%** completing induction (PMID 10506606, record). PK: free ara-C in CSF falls biexponentially, initial t½ 9.4 h and terminal **141 ± 23 h** in one published study, vs the FDA label's terminal range **5.9-82.4 h** — the two do not agree and I could not resolve which is right (**UNVERIFIED**); both are >> free ara-C's 3.4 h | **No.** US production ended **June 2017** (Pacira board decision; persistent **technical/manufacturing** problems specific to the DepoCyt process; notified regulators 29 June 2017; ~2.6% of 2016 revenue, ~$5M charge — SEC FY2017 10-K and trade press). **EU marketing authorisation withdrawn 10 July 2018** at the holder's request, for **commercial reasons** (EMA EPAR). No source states a safety rationale; "not safety" is consistent with the sources but **not stated by them** | — | **The principle is proven; the agent is gone.** And it is the wrong drug for this model anyway: depot cytarabine is **already EVALUATED and EXCLUDED** in `LYMPHOMA_UNIVERSE.md:144` on mechanism (division-gated, dCK-dependent, cannot close escape E2). Nothing changes |
| **Depot / sustained-release intrathecal METHOTREXATE** (liposomal, DepoFoam, hydrogel, polymer, extended-release) | would be the ideal answer | **NOT FOUND.** No product, no clinical trial, and no preclinical formulation located. PubMed searches for liposomal/sustained-release intrathecal methotrexate and for DepoFoam methotrexate return nothing relevant; web search for 2024-2026 depot CSF formulations returns only repeated-dose Ommaya trials (e.g. intrathecal pemetrexed NCT05289908, thiotepa/MTX NCT06543992) | **THEORETICAL** | **Does not exist; cannot count** (rule 13: no clinical evidence of the mechanism anywhere). This is the single formulation that would collapse the whole problem, and nobody has made it |
| **Implanted intrathecal pump (SynchroMed-type)** | **Yes in principle** — converts n punctures into 1 implantation plus percutaneous **refills** (themselves awake-compatible port taps). **But** the only canine head-to-head says continuous **under-performs** bolus: in MPS IIIA dogs, SynchroMed II continuous spinal infusion reduced primary substrate but was "**not as efficacious as repeated cisternal or spinal CSF bolus**", with less secondary-substrate reduction in deep cerebral cortex and "little impact on microgliosis" (PMID 27832416). Beagle 28-day continuous lumbar infusions are well established (Yaksh; record) | **Yes** — SynchroMed is a marketed human device and has been implanted in dogs (27832416) | **exists-today (device) / NEAR-FUTURE (for methotrexate in a dog)** | **The only dose-event-sparing route that actually exists.** Two caveats, both real: (1) the canine comparison favours bolus for brain-tissue effect; (2) for methotrexate specifically a continuous low concentration is the wrong exposure shape — a flat level is exactly the "C x T" arm that Bleyer found equi-effective but it is also a *sustained* level, and sustained CSF concentration is one of the two things neurotoxicity tracked (638249). A pump is worth modelling as a **lumbar/spinal-compartment** option, not as a brain option (record: lumbar-to-cisternal ratio ~1:0.017) |
| **Convection-enhanced delivery** | **No.** CED drives drug through an intraparenchymal cannula into a focal mass; it needs stereotactic cannula placement and anaesthesia per infusion, and it does not dose the CSF axis. I did **not** search the canine CED literature in depth this pass (declared) | n/a | n/a | **Not applicable to this problem.** It changes *where* drug goes, not *how many* CSF dosing events are needed |
| **Ventriculolumbar perfusion** (record, PMID 25209375) | **No** — 72 h x 3 per cycle is *more* clinical contact, not less | yes | exists-today | Not a dose-event-sparing option |

## (d) Equivalence check: would fewer, larger intrathecal methotrexate doses give the same kill?

**No. Dose-sparing by larger boluses is ruled out, by a measurement the record already holds.**

1. **The randomised comparison went the other way.** Bleyer 1978 (PMID 638249, record) randomised meningeal-leukaemia patients to 12 mg/m²
   single doses vs "concentration x time" 1 mg q12h x 6: **equal efficacy**, cumulative dose 173 ± 64 vs 66 ± 41 mg/m², and **neurotoxicity
   7/10 vs 1/8 (p<0.05)**. Neurotoxicity correlated with **elevated CSF concentration** and with **cumulative dose**. Trading 45 small doses for,
   say, 15 triple-size ones moves the schedule onto the arm that was 7/10 neurotoxic.
2. **The kinetics give almost nothing back.** Canine CSF methotrexate terminal t½ is **5.20 h** (PMID 581360, record). Tripling the bolus
   triples the **peak** and extends time above any threshold by only **log2(3) x 5.2 h = 8.2 h** (my arithmetic). So a 3x dose buys ~8 extra
   hours above threshold at 3x the peak — the worst possible trade against a toxicity that tracks peak.
3. **Therefore the schedule in the record is already the right shape**: 2.5 mg flat (0.055 mg/mL in a 20 kg dog's 45.3 mL CSF, my arithmetic,
   below the human per-volume standard of 0.080 mg/mL), every 10-14 days, which is ≥46 half-lives apart, i.e. independent low-peak pulses.
4. **A depot does avoid the peak problem — that is exactly what it is for.** DepoCyt raises AUC without raising peak, which is why it could go
   from twice weekly to fortnightly with *better* response and *better* completion (10506606). So the depot is the **only** dose-event-sparing
   route not forbidden by Bleyer. The problem is item 2 of table (c): **no methotrexate depot exists.**
5. **Consequence.** The number of dosing events, 29-45, is **not negotiable by pharmacology**. It is negotiable only by (i) making each event
   cheap — the awake/sedated port of section (b); (ii) raising brain radiation to 36 Gy, which the record already shows cuts the **brain**
   requirement to 17-18 injections while leaving the **spinal** sub-compartment at 34-45 (`LYMPHOMA_UNIVERSE.md:631`); or (iii) a pump for the
   spinal compartment only.

## (e) What would make each of these fail

**The awake/sedated port transfer fails if:**
1. **The port does not stay patent.** This is the live failure mode and it is measured: Katz's ICV catheters occluded or migrated and **5 of 9
   treated dogs** were lost to catheter- or administration-related complications; Ellinwood switched **all** dogs to cisternal injection between
   doses 7 and 23; West's lumbar ports were 67% patent at 30 days. Every dose that falls back to cisternal puncture is a GA — the hybrid rows of
   the (b) table. At 100% fallback the transfer buys nothing and mortality is 8.5% (ASA 1-2) to 50% (ASA 3-5) at 45 doses.
2. **The aseptic protocol is not run.** 1.71% infection per treatment in ordinary practice compounds to **54% at 45 accesses**; with Peyrl's
   trained-personnel protocol it is 0.82%. A clinic that cannot commit to named trained staff, a written protocol and per-dose intraventricular
   vancomycin fails this item outright.
3. **The dog will not tolerate conscious access.** Barni excluded dogs with "aggressive behaviour". A dog that needs chemical restraint for every
   access converts the awake route into the sedation route (acceptable, Katz) or, if sedation is insufficient, into the GA route (fails).
4. **A sedation-only mortality figure turns out to be high.** It is currently **NOT FOUND**; CEPSAF pools sedation with anaesthesia (18466167).
   If dog sedation mortality were measured at the pooled 0.17%, 45 sedated doses would carry 7.4% cumulative mortality and the transfer would
   recover only the puncture term, not the anaesthetic term. **This is the one measurement that decides between the "awake" and "sedated"
   columns, and it does not exist.** It is a genuine open input in the rule-11 sense (a number with no basis), unlike the items in section (c).
5. **Foreign-body reaction to a long-indwelling ventricular catheter.** Katz attributes the hydrocephalus deaths to it, and found a lesion along
   the catheter track at 87 weeks. A 45-dose course at 14-day intervals is ~63 weeks of indwelling catheter. Peyrl's human counter-evidence is
   strong (199,956 device-days, "no leucodystrophic changes along the catheter track") but is a human counter-evidence against a canine positive.
6. **The dog is ASA 3-5 at implantation.** 2-3 anaesthetics at 1.33% is 2.6-3.9%, which is tolerable; but a sick dog is also the dog in which a
   port infection becomes fatal. The transfer assumes implantation while in remission, not at diagnosis.

**The depot options fail as follows:** DepoCyt has already failed (unobtainable since 2017/2018, and excluded on mechanism); depot methotrexate
fails because it does not exist and is therefore THEORETICAL; the pump fails if the canine bolus-beats-continuous result (27832416) generalises
to methotrexate kill, or if a sustained CSF methotrexate level reproduces the sustained-concentration limb of Bleyer's neurotoxicity finding.

**The larger-bolus option is already failed** by Bleyer 638249 and by the 5.2 h canine half-life; it should not be re-proposed.

## Bottom line for `failing()` / `procedural_cost()`

- **"Can repeated intrathecal dosing be done in a dog without a general anaesthetic each time?" — YES, graded TRANSFERRED**, by a
  **sedated subcutaneous CSF port**, with the measured canine statement in Katz 2014 (PMC4263309) and the awake canine vascular-port,
  awake canine CSF-sampling, awake primate cisternal-port and awake human Ommaya-tap anchors behind the fully conscious variant.
- **Revised cumulative procedural mortality: 0.10% (ASA 1-2) to 2.64% (ASA 3-5)** on 2 anaesthetics, replacing the recorded
  7-18% / 11-25%. The hybrid rows give the honest middle: at 25% cisternal fallback, 2.2% / 17.3%.
- **The dominant procedural risk moves from anaesthesia to the device**, where the canine upper bound is 5 of 9 dogs over 8-20 months
  (Katz, with four stated reasons it is an upper bound) and the human anchor is 1 infection in 5,472 accesses (Peyrl).
- **Code paths that would have to change:** `lymphoma_sustained.PROCEDURAL_MORTALITY_AT_DOSES` (add a route argument: `ga_per_dose`,
  `sedated_port`, `awake_port`, `hybrid(f)`; per-event anaesthetic rate from 18466167 rather than 9657167), and
  `lymphoma_standard_audit.procedural_cost` (report the device term separately from the anaesthetic term, and carry the aseptic-protocol
  condition as a named condition in `deterministic_closure.conjunction()`, since it swings infection 100-fold).
- **Genuinely open (rule 11, a number with no basis): canine sedation-only mortality per event.** Everything else here has a measurement or a
  written transfer behind it. Also **NOT FOUND** and declared: a canine CSF port dosed fully awake; a per-tap human haemorrhage rate; the
  anaesthesia protocol in Ellinwood 35717448 (verified absent from the text) and in Vuillemenot 21784683 (text not retrieved); whether
  DepoCyt's withdrawal had any safety component (no source says so either way); the DepoCyt CSF terminal half-life (141 h published vs
  5.9-82.4 h on the FDA label, unresolved). Canine convection-enhanced delivery was not searched in depth.
