# Veterinary regulatory approvals and commercial products for canine lymphoma, 2025 to 31 Oct 2026

Scope: new FDA CVM approvals and label changes, USDA CVB biologic licences, company pipelines, EU/UK/Japan approvals, and radiopharmaceuticals for canine lymphoma (B- and T-cell). Sweep date 31 Oct 2026. Items dated after 1 Oct 2026 are marked **POST-SWEEP**. Record checks were case-insensitive Grep over `docs/` and `src/canine_dsp/`.

**Bottom line:** No new lymphoma-indicated veterinary drug, biologic, or radiopharmaceutical was approved, licensed, or launched anywhere I could find between 1 Oct and 31 Oct 2026. The only post-sweep regulatory item is the EMA CVMP meeting of 6-8 Oct 2026, which contained nothing for oncology. In the 2025-2026 window, the one lymphoma regulatory event is Laverdia's move from conditional to full approval, and the project already has it. Two smaller points are not in the record: Laverdia's US commercial availability (dvm360, 23 Sep 2026) and an open UGA field trial of an unnamed oral investigational product in naive large B-cell lymphoma. Neither changes what a US vet can lawfully use.

## Q1. New FDA CVM approvals or conditional approvals for canine lymphoma, or label changes to Laverdia or Tanovea

### Takeaway
Laverdia (verdinexor, NADA 141-614) moved from conditional to full approval. This is the only FDA lymphoma action in the window, and the record already has it. The sources give three different dates for it (detailed below), and the record repeats that inconsistency. Tanovea has no new label change, discontinuation, or supply notice. I found no other new FDA approval or conditional approval for canine lymphoma.

### Cited Findings
- **Laverdia (verdinexor tablets), full approval.**
  - **Status and sponsor:** FDA full approval for "to treat dogs with lymphoma" (all lymphoma, with no B/T restriction stated). Sponsor is Anivive Lifesciences.
  - **Pathway:** Conditional approval in Jan 2021 under the Minor Use/Minor Species pathway. That conditional approval was renewed four times before full approval. The FDA CVM update is dated 16 Jan 2026 and says FDA "recently granted" the approval — [FDA CVM update](https://www.fda.gov/animal-veterinary/cvm-updates/fda-grants-full-approval-first-oral-treatment-lymphoma-dogs).
  - **US use:** Lawful now as an on-label approved animal drug.
  - **Record:** ALREADY IN RECORD (`docs/LYMPHOMA_STATUS.md:307`; `docs/universe/SWEEP_legal.md:19`; `src/canine_dsp/lymphoma_sustained.py:205`).
- **Date conflict for the Laverdia approval.**
  - Anivive's PR Newswire release announcing the full approval is dated 26 Jun 2026 and gives no approval date — [PR Newswire](https://www.prnewswire.com/news-releases/anivive-lifesciences-announces-fda-approval-of-laverdia-the-first-oral-treatment-of-its-kind-for-canine-lymphoma-302811840.html).
  - The project's own record holds the FOI summary dated 2025-12-18 (`docs/universe/SWEEP_xpo1_cns.md:4`).
  - `docs/universe/SWEEP_dog_programs.md:65` records "FULL 2026-06-26 per Anivive PR".
  - A web-search summary also gave "December 2025" but cited no primary source, so it is treated as unverified.
  - The most likely sequence is: FOI or approval mid-to-late Dec 2025, FDA announcement 16 Jan 2026, company PR 26 Jun 2026.
- **Same Anivive release, other content:**
  - Approvals are "being pursued" in Australia, Brazil, Canada, Europe, Japan and the UK. This is announced intent only.
  - Dechra Veterinary Products holds the US rights, and Dechra plans a support program "starting later this summer" — [PR Newswire](https://www.prnewswire.com/news-releases/anivive-lifesciences-announces-fda-approval-of-laverdia-the-first-oral-treatment-of-its-kind-for-canine-lymphoma-302811840.html).
  - Record: the ex-US filings are NOT IN RECORD (grep for "Australia|Brazil|Canada" with Laverdia found no hit; Dechra's US rights are at `SWEEP_dog_programs.md:65`).
- **Laverdia commercial availability (US).**
  - dvm360 reported on 23 Sep 2026, attributing the news to Dechra: "Verdinexor tablets (Laverdia) are now available for purchase."
  - Label details in the article: twice weekly, starting at 1.25 mg/kg, at least 72 h apart, with food. The dose can rise to 1.5 mg/kg after 2 weeks if tolerated. Not for use in pregnant, lactating or breeding dogs — [dvm360](https://www.dvm360.com/view/laverdia-now-available-for-purchase-for-dogs-with-lymphoma).
  - This is the commercial launch, not a new approval. It is dated before 1 Oct, so it is pre-sweep.
  - Record: NOT IN RECORD as a launch event (grep "available for purchase" returned nothing). The approval itself is in the record.
- **Tanovea (rabacfosadine, NADA 141-545).**
  - I found no 2025-2026 label change, discontinuation or supply notice.
  - Elanco's current product page still calls it "the first and only FDA fully approved treatment for lymphoma in dogs" and carries the pulmonary fibrosis warning — [Elanco product page](https://yourpetandyou.elanco.com/us/our-products/tanovea); label: [vetlabel](https://vetlabel.com/lib/vet/meds/tanovea/).
  - A third-party patent tracker lists its NCE exclusivity expiring 15 Jul 2026. That is unverified, and no generic has been announced — [Pharsight](https://pharsight.greyb.com/drug/tanovea-patent-expiration).
  - Record: ALREADY IN RECORD (`docs/universe/SWEEP_legal.md:26`; `src/canine_dsp/lymphoma_sustained.py:208`).
- **Guideline status lag.** The AAHA 2026 Oncology Guidelines (Jan 2026 issue) still describe verdinexor as conditionally approved, so they predate the full-approval announcement. The AAHA page returned 403; this comes from search snippets and the [VetGirl PDF mirror](https://vetgirlontherun.com/wp-content/uploads/2026/01/AAHA-Oncology-Guidelines-for-Dogs-and-cats.pdf).

### Inferences
- Laverdia's label is all lymphoma with no B/T restriction, so its on-label use covers all four cases.
- The record's date for full approval is internally inconsistent: Jan 2026 in STATUS, legal and src; 2026-06-26 in `SWEEP_dog_programs.md:65`; FOI 2025-12-18 in `SWEEP_xpo1_cns.md:4`. The FDA's 16 Jan 2026 announcement is the authoritative public date. The 26 Jun 2026 date is the company PR.
- No new FDA lymphoma approval appeared in Oct 2026. Searches for "FDA approves canine lymphoma 2026" and "dog lymphoma new treatment October 2026" returned only Laverdia items.

### Gaps
- I did not query the FDA Green Book or Animal Drugs @ FDA database directly for every 2025-2026 NADA. Coverage rests on CVM updates and news.
- The precise approval date in Animal Drugs @ FDA was not re-fetched; the record's FOI date is 2025-12-18.

## Q2. USDA CVB-licensed biologics for canine lymphoma (antibodies, vaccines, cell therapies): new, conditional or withdrawn

### Takeaway
I found no new, conditional or withdrawn USDA licence for a lymphoma-indicated canine biologic in 2025 to Oct 2026. The one relevant USDA event is ELIAS Cancer Immunotherapy: a full approval in Mar 2025, for osteosarcoma, not lymphoma. The record lists ELIAS's USDA status as "UNVERIFIED"; this sweep verifies it. Blontress is still discontinued. The Elanco 1E4 / K9LO-133 anti-CD20 antibody shows no regulatory change.

### Cited Findings
- **ELIAS Cancer Immunotherapy (ECI), ELIAS Animal Health.**
  - **Status:** The USDA CVB "issued a full approval" for an adoptive cell therapy for canine osteosarcoma. Announced 19 Mar 2025 — [dvm360](https://www.dvm360.com/view/usda-approves-new-canine-cancer-therapy).
  - **Company claim:** As a USDA-approved Autologous Prescription Product, ECI "can also be used by licensed veterinarians to treat other cancers" — [ELIAS pipeline](https://eliasanimalhealth.com/pipeline/).
  - **Lymphoma data:** None published or announced.
  - **Record:** ALREADY IN RECORD as a program, but its USDA status is marked "UNVERIFIED" (`docs/universe/SWEEP_dog_programs.md:73`). The verification is new.
- **Merial/Boehringer canine lymphoma DNA vaccine (xenogeneic murine CD20).** Conditional USDA licence in 2015 for large B-cell lymphoma in remission. I found no 2025-2026 change in status. The current-availability source is a secondary summary (AAHA via search snippet) — [AAHA 2026 guidelines](https://www.aaha.org/resources/2026-aaha-oncology-guidelines-for-dogs-and-cats/section-2-whats-new-in-veterinary-oncology/). Record: ALREADY IN RECORD (`docs/universe/SWEEP_dog_programs.md:62`).
- **Blontress (AT-004).** Discontinued 2017. I found no revival. Record: ALREADY IN RECORD (`docs/LYMPHOMA_UNIVERSE.md:451`; `docs/universe/SWEEP_legal.md:29`).
- **Elanco anti-CD20 (1E4-cIgGB; patent name K9LO-133).**
  - Patents assigned to Elanco US describe a chimeric canine anti-CD20 for B-cell NHL — [Justia US 10941206](https://patents.justia.com/patent/10941206).
  - I found no 2025-2026 regulatory filing, conditional licence or launch.
  - Record: ALREADY IN RECORD (`docs/universe/SWEEP_exists.md:63`; `src/canine_dsp/lymphoma_joint.py:222`).
- **Gilvetmab (Merck anti-PD-1).** Conditional USDA licence for melanoma and mast cell tumour only, not lymphoma — [search summary; AAHA](https://www.aaha.org/resources/2026-aaha-oncology-guidelines-for-dogs-and-cats/section-2-whats-new-in-veterinary-oncology/). Record: ALREADY IN RECORD (`docs/universe/SWEEP_dog_programs.md:67`; `docs/universe/SWEEP_bispecific.md:144`; `src/canine_dsp/core/lymphoma_grounded.py:145`).
- **Akston AKS-701d (anti-PD-L1).** A conditional USDA licence is planned, for canine bladder cancer, not lymphoma. The trial is in solid tumours — [Akston S-1/A](https://www.sec.gov/Archives/edgar/data/1776612/000110465926004158/tm2516611-15_s1a.htm); [dvm360](https://www.dvm360.com/view/akston-launches-clinical-trial-for-novel-canine-cancer-therapy). Record: NOT IN RECORD (grep "Akston" returned nothing). It is not lymphoma-relevant.

### Inferences
- A US vet still has no licensed canine anti-CD20 antibody.
- ECI can be used in a lymphoma dog only under the autologous-prescription-product framework. Per the company, that framework allows other cancers. It has zero lymphoma efficacy data, so it does not meet the project's "near-future agent with clinical-stage evidence" bar for lymphoma.

### Gaps
- I did not download the USDA APHIS CVB "Veterinary Biologics Product Catalogue" or the conditional-licence list directly. Coverage relies on news and search; a direct catalogue check would confirm there is no lymphoma entry.
- The Merial/BI lymphoma DNA vaccine's current marketing status (still distributed or not) was not confirmed from a primary source.

## Q3. Company pipelines with 2025-2026 news (broad search)

### Takeaway
None of the companies named or found has a lymphoma product at approval or launch. Lymphoma-relevant pipeline activity is all at trial or preclinical stage, and most of it is already in the record. Two trial items are not in the record: the UGA unnamed oral IVP field trial and the Tufts/London NCI-funded anti-CD20 + immunomodulator trial. Neither is a product.

### Cited Findings
- **UGA, unnamed oral investigational veterinary product (IVP)** in treatment-naive large B-cell lymphoma.
  - Design: "multi-centered, prospective, single arm open label exploratory field trial."
  - Daily oral dosing at home, 84-day study period, dogs 10-50 kg. Status "currently OPEN"; no sponsor named; investigator Corey Saba — [UGA CVM](https://vet.uga.edu/clinical-trial/dogs-diagnosed-with-b-cell-lymphoma/).
  - Status: in trial (industry-style field study).
  - Record: NOT IN RECORD as a UGA listing (grep "exploratory field" hits only `docs/universe/SWEEP_tcell_agents.md:37`). That line describes the Boehringer BI705564 oral BTK inhibitor (5 mg/kg daily x 84 d, an "Exploratory field trial" at Colorado Animal Specialty).
- **Tufts (Cheryl London), NCI-funded trial in diffuse large B-cell lymphoma.**
  - Regimen: chemotherapy + an unnamed anti-CD20 antibody + one of KPT-9274, RV1001 or TAK-981. More than 70 dogs enrolled.
  - News of 11 Feb 2026 reports one dog in remission 5 years after diagnosis (TAK-981 arm) — [Tufts news](https://vet.tufts.edu/news-events/news/german-shepherd-clinical-trial-still-remission-five-years-after-lymphoma-diagnosis).
  - Status: completed or ongoing academic trial. Single anecdote; no regulatory status.
  - Record: RV1001 ALREADY IN RECORD (`docs/LYMPHOMA_UNIVERSE.md:25`). TAK-981 (subasumstat), KPT-9274 and this Tufts trial are NOT IN RECORD (grep returned nothing).
- **Penn tandem CD19/CD20 canine CAR-T (Atherton/Mason).**
  - Preclinical; an AKC-CHF grant ran Feb 2024 to Jan 2026 — [AKC-CHF 3194](https://www.akcchf.org/research/research-portfolio/3194.html).
  - Record: ALREADY IN RECORD (`docs/universe/SWEEP_dog_programs.md:6-7`; PMID 42480604).
- **Canine CAR-T companies.** I found no commercial canine CAR-T company with a lymphoma product or trial. Caribou Biosciences (a human CAR-T company) is shutting down, per STAT, 7 Oct 2026 (POST-SWEEP), but it is irrelevant to veterinary products — [STAT](https://www.statnews.com/2026/10/07/caribou-biosciences-shutting-down-lymphoma-car-t-therapy/). Record: Caribou NOT IN RECORD; not relevant.
- **Yamaguchi / Nippon Zenyaku Kogyo (Japan) anti-CD20 antibody.** A vet-led clinical trial was announced in 2020 — [AMED 2020](https://www.amed.go.jp/news/release_20200710-02.html). I found no 2025-2026 Japanese approval. Record: the program is ALREADY IN RECORD (`docs/universe/SWEEP_dog_programs.md:10`; 4E1-7-B at `SWEEP_cart_kill.md:194`).
- **Zoetis / Merck lymphoma antibody claims (2025).** These appear only on market-research sites. The record already flags them as UNVERIFIED (`docs/universe/SWEEP_tcell_agents.md:37`). I found no primary press release in this sweep either.
- **Torigen, VetStem, NovaBay, PetCure.** I found no 2025-2026 lymphoma product news. A search on "ELIAS OR Torigen OR VetStem cancer immunotherapy licensed" returned only ELIAS (osteosarcoma). A 2025 review notes that autologous vaccines have been used in research chemoimmunotherapy for canine lymphoma — [Anticancer Res 2025](https://ar.iiarjournals.org/content/45/10/4115).

### Inferences
- The UGA trial's profile (oral, daily, 84 days, naive large B-cell, multi-centre field trial) matches the BI705564 BTK-inhibitor exploratory field trial already in the record. This is likely, but unverified, because UGA does not name the product.
- No pipeline item reached announced-approval stage for lymphoma in 2025-2026.

### Gaps
- I did not systematically check Elanco, Zoetis, Merck AH or Boehringer investor reports for Q3 2026; no lymphoma item surfaced in search.
- I could not identify the UGA IVP or its sponsor.

## Q4. EU (EMA CVMP), UK (VMD) and Japan approvals

### Takeaway
I found none. The post-sweep CVMP meeting (6-8 Oct 2026) gave no oncology opinions. I found no VMD authorisation of verdinexor or rabacfosadine, and no Japanese approval of a canine lymphoma drug. Anivive says ex-US filings are "being pursued" (intent only).

### Cited Findings
- **POST-SWEEP. EMA CVMP, 6-8 Oct 2026.** Positive opinions went to:
  - Stemyca (equine umbilical-cord MSCs), dogs, chronic inflammatory enteropathy.
  - Bovilis Lumpyvax (cattle).
  - A Mirataz safety variation.
  - Vaxxitek HVT+IBD+H5 validity extension.
  - A Vetmedin oral solution referral.

  None concern oncology or lymphoma — [EMA CVMP highlights Oct 2026](https://www.ema.europa.eu/en/news/meeting-highlights-committee-veterinary-medicinal-products-cvmp-6-8-october-2026). Record: NOT IN RECORD; not relevant to lymphoma.
- **UK VMD.** A search for verdinexor or rabacfosadine on the VMD product database returned only unrelated public assessment reports (for example Numelvi, Lozenord) — [VMD PAA example](https://www.vmd.defra.gov.uk/productinformationDatabase/files/PAA_Documents/PAA_3213461.PDF). Record: "No UK authorisation" is already in the record (`docs/universe/SWEEP_import.md:436`).
- **Japan.** A Japanese-language search for 2026 canine lymphoma drug approvals (犬 リンパ腫 動物用医薬品 承認 2026) found only the 2020 AMED/Nippon Zenyaku trial announcement and market reports — [AMED](https://www.amed.go.jp/news/release_20200710-02.html).
- **Laverdia ex-US.** Approvals are "being pursued" in Australia, Brazil, Canada, Europe, Japan and the UK (announced intent) — [PR Newswire 26 Jun 2026](https://www.prnewswire.com/news-releases/anivive-lifesciences-announces-fda-approval-of-laverdia-the-first-oral-treatment-of-its-kind-for-canine-lymphoma-302811840.html). Record: NOT IN RECORD.

### Inferences
- Nothing ex-US changes US lawful access.

### Gaps
- I did not check CVMP highlights for each 2025 and early-2026 meeting individually; only the Oct 2026 meeting was read in full.
- I did not query the Japanese MAFF/NVAL approval lists directly.

## Q5. New radiotherapy or radiopharmaceutical products for dogs (90Y-NM600, Lu-177, etc.)

### Takeaway
I found no new veterinary radiopharmaceutical approval, and no canine lymphoma radiopharmaceutical trial, in 2025-2026. Archeus NM600 news in 2026 is a murine preprint only.

### Cited Findings
- **Archeus / NM600, 2026.** A bioRxiv preprint (late Oct 2026, POST-SWEEP) tests Lu-177 radiopharmaceutical therapy plus checkpoint blockade in mice, not dogs, and one author is an Archeus cofounder — [bioRxiv 2026.10.27.762270](https://www.biorxiv.org/content/10.64898/2026.10.27.762270v1). The canine NM600 safety study is from 2021 — [PLOS ONE 2021](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0255798). Record: NM600 ALREADY IN RECORD (`docs/universe/SWEEP_nm600_itmtx.md`). The Oct 2026 murine preprint is NOT IN RECORD; it is preclinical and not lymphoma.
- **Veterinary radiopharmaceuticals already marketed.** The previously marketed products are Y-90 hydrogel and Sn-117m colloid; neither is for lymphoma — [Johns Hopkins 2023](https://www.hopkinsmedicine.org/news/articles/2023/02/radiopharmaceutical-therapy-in-veterinary-patients). A 2026 review says Y-90 and Lu-labelled agents have only been piloted in dogs — [MDPI Life 2026](https://www.mdpi.com/2075-1729/16/4/626).

### Inferences
- External-beam radiotherapy and total-body irradiation remain the only radiation tools available for the project's lymphoma cases. No new product changes this.

### Gaps
- I did not search clinicaltrials.gov, AVMA AAVSR or the Veterinary Cancer Society trial registry for canine radiopharmaceutical lymphoma trials.

## Summary table

| Item | Date | Regulator | Status | Label / indication | US vet can use now? | Post-sweep? | Record |
|---|---|---|---|---|---|---|---|
| Laverdia (verdinexor) NADA 141-614 | FOI 2025-12-18; FDA announcement 2026-01-16; Anivive PR 2026-06-26 | FDA CVM | Full approval (from 2021 MUMS conditional) | Lymphoma in dogs | Yes, on-label | No | ALREADY (`LYMPHOMA_STATUS.md:307`; `SWEEP_legal.md:19`); date inconsistent at `SWEEP_dog_programs.md:65` |
| Laverdia US commercial availability | 2026-09-23 | — (Dechra launch) | Marketed | as above | Yes | No (just before) | NOT IN RECORD (launch) |
| Laverdia ex-US filings | 2026-06-26 | AU/BR/CA/EU/JP/UK | Announced intent | — | n/a | No | NOT IN RECORD |
| Tanovea (rabacfosadine) NADA 141-545 | no change found | FDA CVM | Full (2021) | Lymphoma in dogs | Yes | No | ALREADY (`SWEEP_legal.md:26`) |
| ELIAS Cancer Immunotherapy | 2025-03-19 | USDA CVB | Full approval, autologous prescription product | Osteosarcoma (company says other cancers allowed) | Legally yes under the APP framework; no lymphoma data | No | ALREADY as program (`SWEEP_dog_programs.md:73`, marked UNVERIFIED); USDA status now verified |
| Blontress | — | USDA | Discontinued 2017 | B-cell lymphoma | No | No | ALREADY (`LYMPHOMA_UNIVERSE.md:451`) |
| Elanco 1E4 / K9LO-133 anti-CD20 | no change | — | Investigational | B-cell | No | No | ALREADY (`SWEEP_exists.md:63`) |
| UGA oral IVP, large B-cell, field trial | undated, OPEN | — | In trial | — | Only via trial enrolment | Unknown | NOT IN RECORD (likely BI705564, `SWEEP_tcell_agents.md:37`) |
| Tufts anti-CD20 + TAK-981 / KPT-9274 / RV1001 | news 2026-02-11 | — | Academic trial | DLBCL | Only via trial | No | RV1001 ALREADY; TAK-981, KPT-9274 NOT IN RECORD |
| EMA CVMP Oct 2026 | 2026-10-06..08 | EMA | No oncology opinions | — | n/a | **Yes** | NOT IN RECORD (nothing relevant) |
| Archeus Lu-177 murine preprint | late Oct 2026 | — | Preclinical (mouse) | not lymphoma | No | **Yes** | NOT IN RECORD (not relevant) |
