# Verification: selinexor CSF penetration in humans (MSZ trial) and the UMN / LEAH Labs canine CD20 CAR-T trial status

Access date for every web source below: **2026-10-31** unless stated. Pages fetched raw with curl and parsed by me (not only via a summariser) where marked "raw".

**What the record already held (checked before searching):**
- `docs/universe/SWEEP_xpo1_cns.md` line 52 listed "selinexor CSF concentrations" as **Not found**. It records selinexor total brain:plasma of 0.60-0.72 in mouse, rat and monkey (PMID 27323910), human enhancing-GBM resected tumour 0.09 (PMID 34728525), and the rodent microdialysis methods paper PMID 40286321, which reports no Kp,uu.
- `docs/universe/SWEEP_dog_programs.md` lines 12 and 30, and `docs/LYMPHOMA_UNIVERSE.md` line 340: the UMN (Henson) xenogeneic CD20 CAR-T page read **ON HOLD** on 2026-10-04, and the Missouri "LEAH xCAR-T" page also read **ON HOLD** on 2026-10-04.

Both findings below **update** those records. The selinexor CSF number is new to the record; the trial status has changed.

## 1. Selinexor CSF penetration in humans (MSZ phase 2, ASH 2025 abstract 3550)

### Takeaway
The primary abstract was recovered. It is Li L, Pan B, ... Wang X (Second Hospital of Dalian Medical University), *Blood* 2025;146(Suppl 1):3550, DOI 10.1182/blood-2025-3550. The ashpublications.org page returned a Cloudflare 403; the full abstract text was read from the publisher's deposit in Crossref.

The measured values are:
- Mean peak plasma selinexor of **204.67 ng/mL** at 4 h after a 40 mg oral dose.
- CSF **0.919 ng/mL** at the same time point.
- A stated "stable CSF-to-plasma ratio (~0.6%)" from 4 to 25 h.

The abstract does not report the number of patients sampled, whether plasma was total or unbound, or any brain-tissue measurement. The two quoted point values give **0.45%**, not 0.6%.

### Cited Findings
- **Citation and identity.** Title: "From mechanistic synergy to clinical breakthrough: Updated results from a phase II Trial of HD-MTX, selinexor, and zanubrutinib in CNS lymphoma". *Blood* 146(Suppl 1):3550-3550. Crossref issued date 2025-11-03. Authors: Li Li, Bing Pan, Kaiyi Liu, Wenjing Yang, Xin Gao, Qi Zhang, Zhijia Zhao, Yinuo Cai, Xiaobo Wang; all at "The Second Hospital of Dalian Medical University, Dalian, China". — [Crossref record, DOI 10.1182/blood-2025-3550](https://api.crossref.org/works/10.1182/blood-2025-3550); publisher page [ashpublications.org (403 Cloudflare, not readable)](https://ashpublications.org/blood/article/146/Supplement%201/3550/554819/From-mechanistic-synergy-to-clinical-breakthrough)
- **Methods, exact wording:** "We quantified selinexor levels in plasma and cerebrospinal fluid (CSF) using LC-MS/MS at 2, 4, 6, 8, and 25 hours." — [Crossref abstract](https://api.crossref.org/works/10.1182/blood-2025-3550)
- **Results, exact wording:** "Pharmacokinetic analysis showed selinexor plasma levels peaked at 4 hours (average of 204.67 ng/mL) after a 40 mg oral dose, with corresponding CSF levels at 0.919 ng/mL. Serial sampling from 4 to 25 hours demonstrated a stable CSF-to-plasma ratio (~0.6%)." — [Crossref abstract](https://api.crossref.org/works/10.1182/blood-2025-3550)
- **Conclusion, exact wording:** "This is also the first in-human quantification of selinexor's BBB penetration, with pharmacokinetic profiling establishing a novel 'plasma–CSF' exposure-effect model." The Background section also asserts that selinexor "effectively crosses the blood–brain barrier (BBB)". — [Crossref abstract](https://api.crossref.org/works/10.1182/blood-2025-3550)
- **Trial design.** Registration ChiCTR2200062154. 21 CNS lymphoma patients (13 male, 8 female), median age 63 (range 18-80). MSZ regimen: "six 21-day cycles of HD-MTX (3.5 g/m², day 1), selinexor (40 mg twice weekly), and zanubrutinib (160 mg twice daily)". Primary endpoint ORR, by Lugano 2014. — [Crossref abstract](https://api.crossref.org/works/10.1182/blood-2025-3550)
- **Outcomes, as written:**
  - "20/21 patients (95.2%) achieved complete response after a median follow-up of 13.8 months."
  - "1-year PFS of 94.1% and OS of 100%".
  - "13 continued on selinexor–zanubrutinib maintenance (six of whom completed 2 years)".
  - "Grade 3 hematological toxicity was limited to two patients (9.5%)".
  - The Conclusions section instead says "1-year PFS 95.2%", an internal inconsistency with the 94.1% in Results.
  - Cohort type: the title says "CNS lymphoma" and the abstract says "CNSL"; it does not state newly diagnosed only, and it does not separate primary from secondary CNS lymphoma.
  - Source: [Crossref abstract](https://api.crossref.org/works/10.1182/blood-2025-3550)
- **Number of patients with PK/CSF sampling: NOT STATED** in the abstract. The text says only "Pharmacokinetic analysis showed..." with an "average" plasma value.
- **Which dose or cycle was sampled: NOT STATED.** Timepoints are hours after "a 40 mg oral dose", but the abstract does not say which cycle or day, or whether the patient was at steady state.
- **Total vs unbound plasma: NOT STATED.** The abstract says "plasma levels" by LC-MS/MS with no ultrafiltration or unbound fraction mentioned, which by default means total plasma.
- **Brain-tissue measurement: none** in the abstract.
- **What review PMID 41957790 says.** Wei R, Yang S, *J Hematol Oncol* 2026;19, DOI 10.1186/s13045-026-01786-7, PMC13064001; a Letter. Exact sentences: "This study was the first to quantify selinexor concentrations in cerebrospinal fluid, confirming its effective penetration of the blood-brain barrier. While the CR rate is impressive, the reported 1-year PFS requires longer follow-up to confirm durability, especially given the relatively lower CSF quantification (CSF-to-plasma ratio ~ 0.6%) [9] compared to BTK inhibitors (~ 50%) [11]." Its reference 9 is "Li L, et al. ... Blood. 2025;146:3550–3550", i.e. the abstract above. — [Europe PMC full text PMC13064001 (raw XML)](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13064001/fullTextXML); [PubMed 41957790](https://pubmed.ncbi.nlm.nih.gov/41957790/); [DOI](https://doi.org/10.1186/s13045-026-01786-7)
- **Selinexor plasma protein binding.** The FDA label (Xpovio; openFDA set_id f6dd2682-75a6-4863-90a8-a3197f6f78a8, effective 2026-05-12) says: "The protein binding of selinexor is 95%." and "The apparent volume of distribution of selinexor is 133 L in patients with cancer." — [openFDA label API](https://api.fda.gov/drug/label.json?search=openfda.generic_name:selinexor&limit=1)
- **A second human CSF measurement is planned but has no results.** SELINA (NCT07191431: MTX, thiotepa or TMZ + orelabrutinib + selinexor, relapsed/refractory CNS lymphoma) lists blood and CSF selinexor concentration as an exploratory endpoint, with CSF at pre-treatment, before cycle 2, end of treatment and progression. This is from a search-engine summary of the registry entry; I did not fetch the page myself. — [ClinicalTrials.gov NCT07191431](https://clinicaltrials.gov/study/NCT07191431) (secondary: search snippet)
- **PubMed search for other measurements, 2016-2026, 12 hits** (query: selinexor/verdinexor/KPT-330/KPT-335 AND CSF/cerebrospinal/brain tissue/brain-to-plasma/BBB/microdialysis/brain penetration). Metadata or abstracts were read for all. None reports a selinexor or verdinexor CSF or brain concentration beyond what the record already holds:
  - Etchin 2016, PMID 27211268, [DOI](https://doi.org/10.1038/leu.2016.145): qualitative only; KPT-8602 shows "substantially reduced brain penetration compared to selinexor".
  - PMID 39509481, [DOI](https://doi.org/10.1021/acs.jmedchem.4c02169): a different compound, SZJK-0421, with rat brain:plasma "very low (3%)". It is not selinexor.
  - PMID 35163955, [DOI](https://doi.org/10.3390/molecules27030690): a MALDI assay for selinexor in microdialysis fluid; method development only.
  - 42080900, 41890241 and 34405064 describe selinexor as BBB-penetrant without new numbers.
  - 41743042 is a myeloma case where selinexor-based therapy failed to clear CSF plasma cells; no drug level.
  - 40286321 is already in the record.
  - Source: [PubMed search](https://pubmed.ncbi.nlm.nih.gov/?term=%28selinexor+OR+verdinexor+OR+KPT-330+OR+KPT-335%29+AND+%28cerebrospinal+OR+CSF+OR+brain%29)
- **Verdinexor (KPT-335):** no CSF or brain measurement found in any species. This is consistent with the record's existing "Not found".

### Inferences
- **The arithmetic does not match the stated ratio.** 0.919 / 204.67 = **0.449%** at the 4 h peak. The "~0.6%" is the authors' summary of a ratio "stable" over 4-25 h, presumably averaged across timepoints and/or patients. Both numbers come from the same abstract. Neither can be reconciled without the poster or full paper.
- **In molar units:** CSF 0.919 ng/mL ≈ **2.07 nM**; plasma 204.67 ng/mL ≈ **462 nM**, using MW 443.3 from the record's ChEMBL entry.
- **Against unbound plasma.** With 95% binding (label), unbound plasma at peak ≈ 10.2 ng/mL ≈ 23 nM. CSF / unbound plasma ≈ 0.919 / 10.23 ≈ **0.09**. This is a derived Kp,uu,CSF-like figure: it assumes the abstract's plasma was total, applies the label's human binding, and uses a single time pair.
- **Relation to the record's 0.60-0.72.** That figure is total brain tissue / total plasma in animals. CSF / total plasma in humans is 0.0045-0.006. The two are different quantities and do not contradict each other: a 95%-bound, lipophilic drug can have a high total-tissue Kp from tissue binding while its unbound (CSF-like) exposure stays near 0.09 of unbound plasma. Under rule 14, the human CSF value is a measurement in a compartment at issue (CSF and leptomeninges). It should outrank a rodent total Kp for any model input that represents **unbound** exposure, even though it is less flattering.
- **What this means for the model** (stated, not changed; this note edits no code). The brain-access value for verdinexor that rests on the 0.60-0.72 transfer should be checked against how it is used.
  - If it multiplies an exposure that is then compared with an unbound or in-vitro IC50, the human CSF data imply an unbound access nearer **0.09**, roughly 7-8x lower, for the CSF compartment.
  - Grade: TRANSFERRED (human selinexor → canine verdinexor, same SINE series). The source is a conference abstract with n not stated.
  - Parenchymal brain is still unmeasured in humans. CSF is a proxy for brain interstitial fluid, not a measurement of it.
- **Possible inconsistency at the source.** The review contrasts selinexor's ~0.6% with BTK inhibitors at "~50%", citing the zanubrutinib 13-case series. The record should check whether that 50% is also CSF / total plasma before using the contrast. The zanubrutinib series is reported elsewhere at 0.6-5.8% (search snippet), so the review's comparison may be inconsistent.

### Gaps
- **The publisher page and poster were unreadable.** ashpublications.org returned 403 (Cloudflare "Just a moment") to both curl and WebFetch. The Crossref-deposited abstract is the publisher's own text, so the wording above is primary. The poster or slide deck, which would give n sampled, per-patient values and the cycle and day, was not found.
- No Chinese-language source, press release or full paper reporting the MSZ PK in more detail was found in this pass.
- **Not reported:** number of patients with CSF sampling; per-timepoint CSF and plasma values beyond the 4 h peak; whether CSF was paired with steady-state dosing; unbound plasma. No brain-tissue value exists in humans.
- No human or animal measurement of verdinexor in CSF or brain was found; the record's gap stands.

## 2. University of Minnesota / LEAH Labs canine CD20 CAR-T trial status

### Takeaway
As of **2026-10-31** both institutional pages that read ON HOLD on 2026-10-04 now read as enrolling. UMN's own trial page says "Current status: Open and enrolling" (raw HTML). Missouri's page says it "is enrolling patients", and the string "on hold" no longer appears on it (raw HTML). The LEAH Labs homepage says "Trial open — actively enrolling" and lists Minnesota, Ohio State and Missouri. No Ohio State institutional page was found.

UMN names LEAH Labs as sponsor and gives the regimen: pentostatin + cyclophosphamide lymphodepletion, then CAR-T given by IV infusion **and** injection into lymph nodes. Eligibility is naive or relapsed B-cell disease, substage A.

The only outcome data are press-level: two dogs with DLBCL reached remission, and per Newsweek both recurred "months later". There is no peer-reviewed publication and no dose figure.

### Cited Findings
- **UMN trial page (raw HTML, accessed 2026-10-31):**
  - Title "CAR-T cell therapy for canines with B-cell lymphoma". PI "Mike Henson, DVM, PhD"; co-investigator "Caitlin Feiock, DVM".
  - "**Current status: Open and enrolling**". Study title: "Evaluation of xenogeneic CAR-T cell therapy for canine CD20+ B cell lymphoma".
  - Sponsor: "In this study, LEAH Labs is sponsoring an pilot trial to test the safety of a CAR-T cell therapy product in dogs with B-cell lymphoma".
  - The page has no last-updated date; only "© 2026".
  - Source: [vetmed.umn.edu CAR-T page](https://vetmed.umn.edu/departments/centers-and-programs/clinical-investigation-center/current-clinical-trials/car-t-cell). The older URL `vetmed.umn.edu/research/clinical-trials/current-clinical-trials/car-t-cell` returns 404.
- **UMN eligibility, exact wording:**
  - "body weight of at least 10kgs (22lbs)"
  - "any breed, except boxers"
  - "Peripheral multicentric lymphoma (minimum of 4 target peripheral lymph nodes evaluable)"
  - "**Have naïve or relapsed disease, substage A only**"
  - "fine needle aspirate ... consistent with lymphoblastic/high grade lymphoma"
  - "performance status 0-1"
  - Immunomodulators (Apoquel, mycophenolate, cyclosporine, azathioprine) are not allowed. Prednisone is "not allowed if it's used for substage B disease"; the dog must "taper off 72 hours prior to CAR-T administration and remain off for duration of study".
  - Source: [UMN CAR-T page](https://vetmed.umn.edu/departments/centers-and-programs/clinical-investigation-center/current-clinical-trials/car-t-cell)
- **UMN regimen, exact wording:**
  - "Pre-treatment visits (Days -5 to -2): ... **Pentostatin bolus**"
  - "Day -3: ... IV catheter placed, **Cyclophosphamide and Furosemide infusion**; overnight hospital stay"
  - "CAR-T administration (Day 0): ... **CAR-T infusion and injection in lymph nodes**"
  - Follow-up on Day +7 and Day +21, then "Post CAR-T visits (2 and 3 months)".
  - **No cell dose, pentostatin dose or cyclophosphamide dose is given.**
  - Source: [UMN CAR-T page](https://vetmed.umn.edu/departments/centers-and-programs/clinical-investigation-center/current-clinical-trials/car-t-cell)
- **UMN trials listing (raw HTML, 2026-10-31):** "CAR-T cell therapy for canines with B-cell lymphoma ... Current Status | Open and enrolling". The same listing shows "ORBIT - VSV and an anti-PD-1 inhibitor for Canine Lymphoma" (relapsed/refractory aggressive lymphoma) as Open and enrolling. — [UMN current clinical trials](https://vetmed.umn.edu/departments/centers-and-programs/clinical-investigation-center/current-clinical-trials)
- **Secondary source contradicting this.** A search-engine snippet on 2026-10-31 still described the UMN listing as "on hold", and earlier wording mentioned "Elspar or Cyclophosphamide" pre-treatment. This is a stale cache, contradicted by the live page above. — [search snippet, secondary](https://vetmed.umn.edu/departments/centers-and-programs/clinical-investigation-center/current-clinical-trials/car-t-cell)
- **Missouri trial page (raw HTML, 2026-10-31):**
  - "LEAH xCAR-T: Canine B-Cell Lymphoma — The University of Missouri Veterinary Medical Center **is enrolling patients** into a clinical trial evaluating the safety and efficacy of lymphodepleting chemotherapy and xenogenic CAR-T cell therapy in dogs with spontaneous CD20+ lymphoma."
  - Criteria: "Canine patients weighing over 10kg"; "Patients with naive (newly diagnosed) and relapsed (pre-treated) Large Cell B-Cell lymphoma"; "no evidence of primary gastrointestinal or lung involvement"; "off prednisone for a minimum of 72 hours prior to CAR-T therapy".
  - Visits: "minimum of seven visits over the first 21 days".
  - Benefit: all costs covered, plus "up to $4,000 ... for possible adverse events" and a "$2,000 stipend".
  - "on hold" occurs **0 times** on the page. There is no last-updated date.
  - Source: [vhc.missouri.edu current clinical trials](https://vhc.missouri.edu/small-animal-hospital/oncology/clinical-trials/current-clinical-trials/)
- **LEAH Labs homepage (raw HTML, 2026-10-31):**
  - "Our next clinical trial launches in May 2026"
  - "Our fully-funded clinical trial will be enrolling dogs diagnosed with B cell lymphoma. If you can travel to one of our three partner institutions, we want to hear from you. Treatment is provided at no cost to enrolled families."
  - "**Trial open — actively enrolling**"
  - Sites: "University of Minnesota College of Veterinary Medicine · Minneapolis, MN"; "Ohio State University College of Veterinary Medicine · Columbus, OH"; "University of Missouri Veterinary Health Center · Columbia, MO"
  - "3 clinical trial sites actively enrolling"; "1st team in the world to achieve canine CAR-T remissions".
  - No regimen, dose or outcome numbers.
  - Source: [leahlabs.com](https://leahlabs.com/)
- **Ohio State:** no Ohio State veterinary trial page for this study was found by search. Ohio State's participation rests only on the LEAH homepage, a company source. — [leahlabs.com](https://leahlabs.com/)
- **Press reports of outcomes:**
  - Akadeum press release, 2025-09-18. Lou (10-year-old Beagle) and Sadie (8-year-old Collie/Pyrenees mix), "metastatic, multicentric diffuse large B cell lymphoma", reached clinical remission. Over a 3-week study, tumour measurements fell sharply and imaging showed resolution of internal disease. Led by Dr Jeffrey Bryan (Missouri). Full data were promised in "an upcoming publication". No route, dose, lymphodepletion or durability is stated. — [PR Newswire, 2025-09-18](https://www.prnewswire.com/news-releases/akadeum-life-sciences-human-t-cell-leukopak-isolation-kit-successfully-utilized-by-leah-labs-and-the-university-of-missouri-to-treat-canine-cancer-302560144.html)
  - dvm360, "Published: September 18, 2025". "Two dogs with metastatic, multicentric diffuse large B cell lymphoma have gone into remission after receiving human CAR-T cell therapy"; a "3-week study". No relapse is mentioned and no route is stated. — [dvm360](https://www.dvm360.com/view/new-cancer-therapy-for-dogs-shows-promise)
  - Newsweek (publication date not shown in the fetched content; it mentions hoping to test "a third dog ... in February").
    - Two dogs had received the therapy, and the cells were "injected directly into the dog's lymph nodes".
    - The dogs "have gone into complete remission", but "months later" a recurrence occurred in both.
    - These statements are paraphrased from Bryan, not direct quotes.
    - Next steps named: a third dog, and a later Mayo Clinic collaboration toward humans.
    - Source: [Newsweek](https://www.newsweek.com/dog-cancer-almost-back-normal-after-pioneering-new-treatment-2023820)
  - Earlier 2024 Medical Alley release: a NCI-funded LEAH/Missouri study "aimed at visualizing CAR-T cell therapy", aiming to enrol 3 dogs for PET-imaging feasibility and safety. — [Medical Alley](https://www.medicalalley.org/leah-labs-and-university-of-missouri-launch-trial-funded-by-national-cancer-institute-aimed-at-visualizing-car-t-cell-therapy-in-pet-dogs-with-cancer/)

### Inferences
- **The record's "ON HOLD" (2026-10-04) is superseded.** Both institutional pages, plus the sponsor's, now say enrolling. Status: **open and enrolling at UMN and Missouri; Ohio State per sponsor only.** The pages carry no dates, so when each changed is unknown. Most likely the May-2026 launch the LEAH page announces became active between 4 and 31 October 2026, or the 4 October read caught stale pages. This cannot be decided from the sources.
- **Regimen.** The UMN regimen (pentostatin + cyclophosphamide lymphodepletion; IV infusion **plus** intranodal injection) suggests the relaunch added systemic lymphodepletion and IV dosing to the earlier intranodal-only approach in the two press-reported dogs. This is an inference from comparing the UMN page with Newsweek; neither source says so.
- **Outcome evidence for durability is unfavourable but anecdotal.** Two DLBCL dogs reached CR after intranodal xenogeneic CAR-T; both relapsed "months later" (secondary, journalist paraphrase). Grade: press report, n=2, not peer-reviewed. It supports a CAR-T kill input, not persistence.
- **Tier under CLAUDE.md rule 13:** this agent moves from "on hold" to **NEAR-FUTURE, in dog trials (enrolling)**. Eligibility covers both naive and relapsed B-cell disease, substage A, so it is relevant to the B-cell programs. CNS disease is not an explicit exclusion on either page. Missouri excludes primary GI or lung involvement, and UMN requires peripheral multicentric disease.

### Gaps
- No dates on any of the three status pages, so the date of the status change cannot be established.
- No Ohio State page or registry entry was found; Ohio State participation is company-asserted only.
- No CAR-T cell dose, pentostatin dose or cyclophosphamide dose was found on any page.
- No peer-reviewed outcome data. The Akadeum release and dvm360 promise an "upcoming" publication; none was found. Durability (time to relapse) is not quantified beyond "months later".
- Newsweek's publication date was not visible in the fetched content (the "third dog in February" wording suggests early 2025, which is unverified).
- No 2026 news coverage of the relaunch was found beyond LEAH's own homepage.
