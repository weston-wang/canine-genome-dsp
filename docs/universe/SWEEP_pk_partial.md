# agent_pk.md -- PK / exposure / IC50 / P-gp / CNS sweep (PARTIAL, written incrementally)

Bar quoted verbatim: "real data OR a scientifically sound model; transferring an input from another species is
acceptable IF the transfer is justified in writing (graded TRANSFER); unsupported numbers are just 'assumed'."

Method note: the 11 PMIDs named in the brief were verified with mcp__PubMed__get_article_metadata (all exist, titles match).
Further PMIDs were verified with NCBI E-utilities (same PubMed records: esummary/efetch). Full text read only where PMC open
access allowed (Europe PMC / efetch); where only the abstract was available it is marked ABSTRACT-ONLY.
Unreachable at time of writing: Europe PMC search (HTTP 503), PMC HTML (reCAPTCHA).

## 1. Panobinostat (status: partial)
Verified PMIDs: 29983882 (doi 10.18632/oncotarget.25580), 37711439 (10.3389/fvets.2023.1236136), 28667459 (10.1007/s40262-017-0565-x),
37827699 (10.1124/jpet.123.001826), 34115161 (10.1007/s00280-021-04313-2), 31894347 (10.1007/s00280-019-04021-y), 37526549 (10.1093/neuonc/noad141).

### Canine IC50: TWO measurements, both CLBL-1, both 24 h (assay_days = 1)
- PMID 29983882 (Dias 2018), WST-1, 24 h: "panobinostat (IC50 = 5.4 ± 0.5 nM), scriptaid (218 ± 8.4 nM) and trichostatin A (67 ± 7.5 nM)".
  Methods: "After 24 h of treatment, cell viability and proliferation were assessed using the WST-1 reagent". Same paper: SAHA, CI-994, SBHA, tubacin "showed IC50 values in the µM range".
- PMID 37711439 (André 2023), Alamar Blue, 24 h: "FA-PEG-Pan-Lip, IC50 = 10.9 ± 0.03 nM, PEG-Pan-Lip, IC50 = 12.91 ± 0.02 nM and Pan-free, IC50 = 18.32 ± 0.024 nM".
  Methods: "After 24 h treatment, cell viability was determined using Alamar Blue reagent". (Methods call the readout EC50; n = 2 independent experiments.)
- So the repo's 18.32 nM is the higher of two; the other is 5.4 nM (3.4x lower). Use 5.4 / 11.9 (geometric mean) / 18.32 as low/central/high IC50.
- Xenograft (PMID 29983882): 10 and 20 mg/kg i.p. 5 d/wk x 2 wk gave TGI 82.9% and 97.3% in CLBL-1 SCID mice; 5-10% body weight loss.

### Human exposure
- PMID 28667459 (abstract only): "an oral dose of panobinostat 20 mg resulted in a maximum plasma concentration (Cmax) of 21.6 ng/mL approximately 1 h after administration ... absolute bioavailability of panobinostat is 21.4%, and it is moderately bound to plasma proteins"; AUC changes with CYP3A4 inhibitors and "P-glycoprotein inhibitors"; main side effects "diarrhea, peripheral neuropathy, asthenia and fatigue; hematologic ... neutropenia, thrombocytopenia, and lymphocytopenia".
- PMID 34115161 (Homan 2021, full text): "Panobinostat has a molecular weight of 349.4 g/mol ... but it is 90% protein bound and is a substrate of P-gp"; "median Cmax of 20.7 ng/mL following oral doses of 20 mg/m2"; "Cmax values, ranging from 10.8 ng/mL to 21.6 ng/mL, following oral doses of panobinostat 20 mg".
  Conversion (mine): 21.6 ng/mL / 349.4 = 61.8 nM total; 10.8 = 30.9 nM. Free (fu 0.10) = 3.1-6.2 nM at peak.
- PMID 29983882 discussion: "in a Phase I clinical study on intravenous panobinostat, Cmax reached up to 200 nM and ... oral panobinostat ... a steady state Cmax ranged from 15 to 35 nM".
- Half-life, AUC, trough: NOT FOUND in the full texts reached (the review 28667459 is abstract-only here). Do not use a half-life from memory.
- Non-human primate (PMID 31894347, full text): plasma "Cmax ranged from 5.08 to 149.6 nM, with Tmax of 1.0 h. Mean dose-normalized AUCinf was 7.65 (± 2.64) h*nM/mg"; half-life 6.76-32.2 h across dose cohorts (Table 1).
- DOG PK of panobinostat: NOT FOUND in PubMed (search 'panobinostat AND (dog OR dogs OR canine OR beagle)' returns only the two CLBL-1 papers, a canine fibroblast epigenetics paper 34660761, and an unrelated HZ1006 dog tox paper 27916918, which is NOT panobinostat).

### P-gp / BCRP
- PMID 37827699 (abstract): "Transporter-deficient mouse studies show that panobinostat is a dual substrate of P-glycoprotein (P-gp) and breast cancer resistant protein (Bcrp)"; "CNS delivery ... was moderately limited by P-gp and Bcrp".
- PMID 28667459: AUC changes under P-gp inhibitors (clinical DDI). Status: P-gp SUBSTRATE (mouse + human DDI); strength moderate.

### CNS
- PMID 37827699: unbound brain-to-plasma Kp,uu 0.32 (brain), 0.21 (spinal cord) in wild-type mice; "Simulation using a compartmental BBB model suggests inadequate exposure of free panobinostat in the brain following a recommended oral dosing regimen in patients."
- PMID 34115161: total brain:plasma 2.22 at 1 h (AUC ratio 2.63) in mice -- TOTAL, not unbound; conflicts in direction with Kp,uu, resolved by tissue binding. Use Kp,uu.
- PMID 31894347: macaque CSF "penetration ... low, with levels detectable in only two subjects"; LLOQ in CSF 1.43 nM.
- => CNS access multiplier for the model: 0.2-0.3 (mouse Kp,uu, TRANSFER); CSF in primate lower (below LLOQ most samples).

### DLTs
- PMID 28667459: diarrhoea (GI), peripheral neuropathy, fatigue; neutropenia, thrombocytopenia, lymphocytopenia (marrow).
- PMID 33279887 (Japanese MM phase II, abstract): grade 3/4 thrombocytopenia 48.4%, fatigue 25.8%, diarrhoea 22.6%, neutropenia 22.6% (with bortezomib + dex).
- PMID 37526549 (paediatric DIPG, abstract): DLTs thrombocytopenia, neutropenia, one PRES, nausea, ALT rise; MTD 10 mg/m2 3x/wk 3 wk on/1 off.

## 8. CD52 antibody (status: primary-source trail found; target specificity in doubt)  [priority 1]
Identity: AT-005 = TACTRESS = tamtuvetmab (INN per MedChemExpress listing, not independently verified), Aratana Therapeutics (antibody developed by Vet Therapeutics, acquired by Aratana in 2013, later Elanco).
Trail (strongest source first):
1. PMID 36329876 (Musser et al., Vet Rec Open 2022; doi 10.1002/vro2.49; full text read, PMC9624070, OA; funded by Aratana): the only peer-reviewed RCT.
   - "The canine T-cell (anti-CD52) lymphoma mAb, AT-005 (Tactress; Aratana Therapeutics, Kansas City, KS, USA), received conditional (2014) and full (2016) licensure by the US Department of Agriculture (USDA) for the treatment of dogs with T-cell lymphoma."
   - "AT-005 was licensed by the USDA for dogs with T-cell LSA based on a safety and efficacy study combining AT-005 and a single dose of L-asparaginase." (ref 24 = Aratana 10-K 2015)
   - Design: 49 dogs (25 placebo, 24 AT-005), all on 19-week L-CHOP, AT-005 5 mg/ml "twice weekly, IV" 15-30 min infusion, fixed doses by weight band: 2-15 kg 37.5 mg; 15.1-30 kg 75 mg; 30.1-45 kg 112.5 mg; 45.1-60 kg 150 mg (i.e. ~2.5-5 mg/kg per infusion).
   - Result: "Median PFS was 103 days (95% CI, 56-118) in the placebo group versus 64 days (95% CI, 36-118) in the AT-005 group" (p = 0.8163); ORR 98% (48/49); CR 64% placebo vs 67% AT-005.
   - CRITICAL: "Following initiation of this study, it was determined that AT-005 lacks binding specificity to the intended target (CD52). Given the apparent lack of efficacy, additional studies with this particular formulation are not warranted."
   - "the antibody is not currently available to veterinarians on the open market".
   - Mechanism of antibody generation (same paper): canine CD52 coding sequence cloned from canine PBMC; mouse immunisation; cites US Patent 8,652,470 B2 (Hansen, "Monoclonal antibodies directed to CD52").
2. Aratana press release 28 Jan 2014 (WebFetch of aratana.investorroom.com; quoted by fetch): USDA "granted conditional approval" on "Jan. 28, 2014"; "AT-005 is Aratana's canine-specific monoclonal antibody against CD52, which is intended as an aid in the treatment of T-cell lymphoma in dogs." Press release gave no study numbers.
3. Aratana 10-K for FY2015 (SEC, WebFetch of sec.gov .../petx-20151231x10k.htm): "TACTRESS is a caninized monoclonal antibody approved by the CVB in January 2016 under a full license as an aid for the treatment of T-cell lymphoma in dogs." "our analysis of the results from two randomized, placebo-controlled post-marketing studies (T-CHOMP and T-LAB) indicate that TACTRESS did not seem to be adding significant progression free survival." "scientific studies suggest that BLONTRESS and TACTRESS are not as specific to the target as expected."
   (Note: 10-K text says CVB approval January 2016 as full licence; Musser says full licensure 2016; the user brief's "conditional licence" was 2014.)
4. Aratana press release 22 Jul 2015: "AT-005 has received conditional licensure from the USDA and Aratana continues to anticipate full licensure in 2015"; "Aratana is working to better understand the specificity of its MAbs in an in-vivo setting."
5. PMID 29459862 (Klingemann, Front Immunol 2018, "Immunotherapy for Dogs: Running Behind Humans"; PMC5807660 read): "A caninized mAb against the T-cell antigen CD52 (Tactress) has been tested in two large, well-controlled studies in conjunction with cytotoxic chemotherapy ... the mAb did not improve progression-free survival". Cites ref 23 = Rodriguez C, Hansen G. "Bioavailability and safety of caninized anti-CD52 monoclonal antibody in dogs with T-cell lymphoma." Proc 34th Annual Veterinary Cancer Society Conference, St Louis, 2014 (conference abstract; NOT in PubMed; NOT retrieved; this is the probable licensing-basis dataset).
6. PMID 34421888 (Klingemann, Front Immunol 2021, PMC8374065): "Some caninenized mAbs ... have received conditional approval by the USDA for lymphoma (i.e. Blontress, Tactress). Disappointingly no peer-reviewed clinical evidence of efficacy for those mAbs has been published." (Written before/without citing Musser 2022.)
7. PMID 26545847 (Regan et al., Vet J 2016, abstract only; the secondary source the repo/brief presumably relied on): "caninized monoclonal antibodies targeting CD20 and CD52 just recently received either full (CD20) or conditional (CD52) licensing by the United States Department of Agriculture". Review, not primary.
   (PMID 39954194, a 2025/2026 probiotics review, doi 10.1007/s12602-025-10468-8, repeats the same sentence; it is derivative of 26545847, not independent evidence. NB: an earlier draft of this note wrongly called its DOI mismatched; that was a bug in my own lookup script, now fixed.)
NOT FOUND: any peer-reviewed canine CD52 expression-on-lymphoma dataset; exposure (Cmax/half-life) of AT-005; the USDA/CVB licence summary document; a primary paper demonstrating the non-binding. The statement "lacks binding specificity" is from Musser 2022 citing the Aratana 10-K (which words it more weakly: "not as specific to the target as expected").
Implication for the model: an "anti-CD52 antibody" agent exists as a licensed product (2014 conditional, 2016 full) but (a) the only RCT showed no PFS benefit (median 64 d vs 103 d, n = 49) and (b) the sponsor/authors report it does not bind CD52 specifically. It is NOT a usable CD52-directed effector; the ledger's "CD5/CD52-directed cellular effector ... does not exist" remains right for a cellular product, but the antibody should be recorded as "licensed, evaluated, not effective, target binding doubtful" (not "not assessed"). Grade: MEASURED negative clinical (n = 49, randomised); no PK.
Human comparator: alemtuzumab is anti-CD52 with activity in relapsed T-cell lymphoma (cited in Musser as ref 22); canine CD52 homology/epitope not shown to match.
