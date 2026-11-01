# Cancer vaccines and vaccine-like active immunotherapy for lymphoma: literature sweep for the canine multicentric lymphoma durable-response model

Date of sweep: 2026-09-30. Source: PubMed (MCP tools plus NCBI E-utilities; every PMID below was re-fetched and exists; DOIs are the PubMed-recorded ones), PMC full text where open (Tel-eVax, CD40-B, APAVAC 2019 read in full; Gavazza 2013 and Peruzzi 2010 full text was publisher-blocked, so their numbers come from the abstract plus machine-summarised page quotes and should be spot-checked by hand; Marconato 2014 abstract only).

User's bar, quoted verbatim: "real data OR a rigorous/scientifically sound model; a transferred input (other species/disease/class mechanism) is acceptable IF the transfer is justified in writing. Unsupported numbers are just 'assumed'." Grades below use exactly: MEASURED / DERIVED / TRANSFER / OUTCOME / ASSUMED.

## 0. Bottom line (read this first)

1. No vaccine platform has a MEASURED or DERIVED per-day kill rate for canine lymphoma cells, and none has a MEASURED effect on non-dividing persisters. The best available quantities are (a) outcome shifts (OUTCOME) over weeks to about 3 years and (b) a mass-action effector:target model whose per-CTL rate is TRANSFERRED from mouse imaging and whose effector:target ratio in dog tumours is ASSUMED.
2. The dog vaccine data consistently show a hazard shift early (TTP/OS medians up 1.1x to 7x depending on study) and NO visible change in the long tail: 3-year survival 10% vaccine vs 8% chemo in 148 DLBCL dogs (PMID 31174615); durable first remission >16 months 21% vaccine vs 23% concurrent controls (PMID 21904611); identical median PFS 11.4 vs 11.3 weeks in the non-randomised 21-vs-21 dTERT study (PMID 23902422). Nothing in the dog literature supports a vaccine-driven plateau, let alone a 10-year one.
3. Human idiotype vaccines (the closest thing to a mature vaccine programme in lymphoma) produced immunogenicity and molecular-remission signals in Phase 2 but failed or only marginally passed three Phase 3 trials (PMIDs 21632504, 24799467, 19414675). No human vaccine has shown a cure plateau.
4. Escape coverage (mechanistic, from the literature below): all T-cell-mediated platforms (dTERT, HSPPC/APAVAC, DC, CD40-B, neoantigen, idiotype-T-cell arm) are defeated by MHC-I/B2M loss and (by reasoning) weak against the quiescent persister; they do cover CD20/CD19 antigen loss because the target is different. CNS access is unsupported by any lymphoma vaccine data.
5. Historic-control bias is demonstrated in this very literature: the Listeria-HER2 canine osteosarcoma Phase 1 beat historical controls (PMID 26994144) but the 118-dog follow-up did not (PMID 39955616); the Oncept melanoma vaccine beat historical controls (PMID 22126691) but a retrospective comparison found no benefit (PMID 23909996). Every dTERT result is against historic or self-selected (owner-consent) controls.

## 0a. Record check (CLAUDE.md rule 1): already covered vs new

Already recorded in `docs/LYMPHOMA_STATUS.md` (branch `claude/duplicate-codex-prefix-branch-lt1qh6`), not new: dTERT 20531395 (13/14 responders, >97.8 vs 37 wk), 23902422 (>76.1 vs 29.3 wk), Tel-eVax 30537967 (OS 64.5 wk, no control), hGM-CSF CLDC negative 19754780, DC lysate no DTH 17917377, reviews 41006003 and 26545847; the statement that vaccine is an omission, not a settled exclusion.
New in this sweep (not in the record): the PFS null in 23902422; Tel-eVax 94% dead at up to 277 wk; APAVAC RCT and 300-dog series with 1/2/3-year survival and the flat tail; CD40-B control-arm durable fraction; LMI microbeads; TERT biology in dog and human B cells; human idiotype/DC/in-situ/neoantigen data; historic-control failure cases; kill-rate transfer logic; list of searches with no hits.

## 1. Platform-by-platform

### 1.1 Telomerase (dTERT) genetic vaccines: Ad6 prime + DNA electro-gene-transfer (Evvivax; Tel-eVax)

Verified citations
- Peruzzi 2010, Mol Ther, PMID 20531395, doi 10.1038/mt.2010.104.
- Gavazza 2013, Hum Gene Ther, PMID 23902422, doi 10.1089/hum.2013.112.
- Impellizeri 2018 (Tel-eVax), J Transl Med, PMID 30537967, doi 10.1186/s12967-018-1738-6.
- Peruzzi 2010 healthy-dog immunogenicity, Vaccine, PMID 19944791, doi 10.1016/j.vaccine.2009.11.031.
- Thalmensi 2019 (alternative canine TERT DNA vaccine pDUV5, Invectys), Oncotarget, PMID 31164958, doi 10.18632/oncotarget.26927 (healthy dogs only; tumour-bearing dogs retain TERT-specific T cells).

Numbers
| Study | n | Design / control | Immune response | Outcome | Tail |
|---|---|---|---|---|---|
| 20531395 | 14 vaccinated B-cell lymphoma; 8 controls | Vaccine after CR with COP maintenance; historic controls "managed by the same clinicians within the same veterinary center" | 13/14 (93%); 50-250 SFC/10^6 PBMC; one dog detectable ~2 y | Median OS >97.8 vs 37 wk (P=0.001); time to first relapse 26 vs 14 wk (P=0.014; page-extracted) | 6 deaths/14 at report; longest follow-up ">98 wk" (<2 y). No vaccinated dog documented past 2 y. Vaccine was never given without chemo |
| 23902422 | 21 vs 21 | Two-arm, **non-randomised; assigned by owner consent**; concurrent COP-only control; vaccine started 2 wk after CR, with maintenance | 19/21 (90.5%); 7-663 SFC after Ad, peak 82-1464 (mean 445 +/- 330) after DNA-EGT | Median OS 76.1 vs 29.3 wk (p<0.0001) | "3.5 y follow-up"; final numbers alive not stated in retrievable text. **Median PFS 11.4 vs 11.3 wk (p>0.1): vaccine did not lengthen first remission.** dTERT mRNA found in all tumours; expression vs OS Spearman rho 0.80 in only 6 vaccinated dogs |
| 30537967 | 17 DLBCL | Single arm, L-CHOP 27 wk, vaccine from wk 4; owner consent; no control | Antibody to TERT pool A low-level in 8/12 (ELISA, arbitrary threshold); no T-cell assay | OS 64.5 wk (452 d) | **94% of dogs dead in the 277-week monitoring window (16/17); i.e. about 1/17 alive at up to ~5 y.** Authors compare 452 d OS to 244 d, which is a median PFS (Wilson-Robles), not OS. No control arm; 4 dogs got extra chemo |

Toxicity: no adverse effects in any of 52 dogs (14+21+17); no autoimmunity signal reported for the vaccine. Electroporation needs anaesthesia (propofol + isoflurane/sevoflurane, about 10 min), Ad 10^11 vp x2 then plasmid 5 mg x3 per cycle.
Availability: trial/buildable (Ad vector + codon-optimised catalytically-dead dTERT plasmid + Vet-ePorator device). No licence found in the literature searched.

Honest reading
- The survival gain is real-looking but concurrent arms were owner-selected, COP is an inferior backbone, and the control median (29.3 wk) is shorter than typical CHOP medians; the first-remission duration did not move. The benefit therefore appears after relapse (rescue response, selection, or both). The same pattern (no TTP gain, better second remission) is seen with CD40-B (1.4).
- Authors state the vaccine does not work without chemotherapy (Impellizeri Discussion, citing their first study): consistent with an MRD-setting effect.
- Dose: minimal effective dose unknown.

TERT as a target (escape questions)
- Expressed in lymphoma? Yes but not tumour-specific in dog. Telomerase activity is also present in normal canine lymph node and overlaps lymphoma (PMIDs 11560275, 19379313); TERT mRNA in normal lymph node, thymus, liver, ovary (PMID 14620776); in lymphoma nodes TERT protein tracks Ki67 (PMID 19754811). dTERT mRNA was detected in all vaccine-trial tumours tested (23902422, 20531395).
- Required and expressed in quiescent cells? Not supported; evidence points the other way. In human B cells telomerase is about 1000x higher in germinal-centre B cells than resting naive or memory B cells (PMID 10556831), and resting naive/memory B cells are telomerase-activity negative (PMID 11872079; PMID 12714249 shows induction on stimulation). Canine TERT tracks Ki67 (19754811). So a resting, drug-tolerant persister is expected (mechanistic inference, not measured in canine persisters) to be TERT-low and unkillable by a TERT-directed T cell. Grade for persister coverage: ASSUMED zero.
- Needs MHC-I? Yes (CD8). Defeated by B2M/MHC-I loss: see 2.2. In the AML human TERT-DC study the responses targeted peptides with predicted low HLA affinity (PMID 28411378).
- CD20/CD19 independent? Yes. Covers antigen-loss escape (mechanistic; TERT is unrelated to B-lineage markers).
- Tumour can shed TERT? A telomerase-negative route exists in principle (alternative lengthening), not evaluated in canine lymphoma: not found.
- Immunosuppressive microenvironment: canine lymphoma nodes have fewer, poorly mitogen-responsive T cells and more Tregs (PMID 22293625), FOXP3+ frequency independently worsens PFS/OS (PMID 25119018), PD-L1 is raised on malignant B cells and on TIL (PMID 29380929), tumour EVs induce CD8 apoptosis and regulatory phenotype in vitro (PMID 37884996). Remission improves CTL activity and lowers circulating Tregs (22293625). This supports giving vaccines in remission (low burden), not at bulk.
- Toxicity class risk: TERT-directed adoptive T cells caused autoimmune B-cell lymphopenia in mice (PMID 19903903) and granulocyte toxicity in a humanised model (PMID 27197263); active vaccination did not (Ugel 2010 states this, Impellizeri Discussion likewise). A stronger vaccine or T-cell version would carry this risk.
- Human TERT evidence in haematology: GV1001 peptide gave 0/6 objective responses in CTCL (PMID 21377838); TERT-mRNA DC vaccine in AML, n=22, 11/19 in CR (58%) without recurrence at median 52 mo, single-arm, selected (PMID 28411378). Neither is evidence of a durable lymphoma effect.
- CNS: no data. Activated T cells can enter CNS (general immunology; not evidenced here); no lymphoma vaccine study measured CSF T cells. Grade: ASSUMED.

Per-day kill / durable-fraction translation: see section 3. Grade of potency: ASSUMED (E/T) on a TRANSFER per-CTL rate; grade of outcome effect: OUTCOME (weeks to ~1.5 y vs historic or self-selected controls).

### 1.2 Autologous tumour-derived vaccines

a) HSPPC + hydroxyapatite ("APAVAC", Urodelia; heat-shock-protein/peptide complexes from a resected node; the "Rossi/Frayssinet HASTIM" line)
Verified: Marconato 2014 Clin Cancer Res PMID 24300788 doi 10.1158/1078-0432.CCR-13-2283; Marconato 2015 Vaccine PMID 26296495 doi 10.1016/j.vaccine.2015.08.017; Marconato 2019 J Immunother Cancer PMID 31174615 doi 10.1186/s40425-019-0624-y; Rossi 2024 on the HA/azoximer adjuvant background PMID 38318840 doi 10.20892/j.issn.2095-3941.2023.0222 (states that the HA autologous vaccine was developed for canine spontaneous lymphoma).
- RCT (24300788): n=19 DLBCL, randomised, placebo-controlled, double-blind, dose-intense chemo. Median TTP 304 vs 41 d (P=0.0004); second-remission duration longer (P=0.02); LSS 505 vs 159 d (P=0.0018); 6 vaccinated dogs reached molecular remission by IgH clonality (control rate not in the abstract). Arm sizes not retrievable. The control TTP of 41 d is far below any contemporary CHOP PFS (about 98-250 d elsewhere in this table), which inflates the contrast; n=19 is very small.
- Indolent B-cell lymphoma (26296495): n=45 (20 chemo, 25 chemo + vaccine), non-randomised: TTP 209 vs 85 d (P=0.015); LSS 349 vs 200 d (P=0.173, not significant). Immune responders had longer TTP and LSS than non-responders (P=0.012, 0.003), which is a prognostic-selection confound.
- Retrospective consecutive series (31174615): n=300 (148 chemo, 152 chemo + vaccine), two centres 2013-2018. Whole population median TTP 147 vs 244 d, LSS 220 vs 401 d (both P<0.001). DLBCL subset n=148 (47 vs 101): TTP 98 vs 250 d, LSS 165 vs 413 d (P=0.001); **1/2/3-year survival 20/13/8% (chemo) vs 51/19/10% (vaccine)**; multivariable HR for no vaccine: progression 2.3 (1.4-3.6), death 2.6 (1.6-4.2). DTH positivity did not predict benefit. In the highest-score subgroup (n=27) 2-y survival 0% vs 15% and 3-y 0% vs 0%. Authors themselves: "the 3-year survival rate remains largely unsatisfactory, ranging from 0 to 12%; the largest survival benefit ... in the short/medium-term". Vaccinated dogs also received a different (lomustine-containing) protocol, stated to be dose-intense-equivalent.
- Toxicity: no local or systemic adverse events (31174615); "no exacerbated toxicity" (26296495). Grade 3-4/5 chemo toxicity similar.
- Availability: commercial investigational use in Europe (APAVAC); requires surgical node excision at diagnosis (compatible with early detection). The vaccine is patient-specific (polyvalent: many peptides, no single target).
- Escapes: CD20/CD19 loss covered (antigen-agnostic); needs MHC-I for CD8 (HSP-peptide cross-presentation is the mechanistic rationale; not canine-measured) so B2M/MHC-I loss defeats it; peptides come from the bulk (dividing) tumour, so non-dividing persisters are not reached except via shared antigens (ASSUMED zero); CNS: none measured; microenvironment: benefit concentrated in high-LDH, stage V, substage a, steroid-naive dogs (Marconato 2019), consistent with steroid/lympholytic pre-treatment and immunosuppression blunting it; combines with chemo (given concurrently, all 8 vaccine injections during protocol).
- Grade: OUTCOME (effect shifts hazard, tail unchanged).

b) CD40-activated B cells loaded with tumour RNA (Penn)
Verified: Mason 2008 Gene Ther PMID 18337841 doi 10.1038/gt.2008.22 (preclinical; RNA-loaded CD40-B induced antigen-specific T cells in dogs with lymphoma); Sorenmo 2011 PLoS One PMID 21904611 doi 10.1371/journal.pone.0024167.
- 30 dogs enrolled, 19 achieved CR and were vaccinated (3 intradermal doses), 64 concurrent chemo-matched controls. TTP 366 vs 327 d (p=0.34), LSS 809 vs 594 d (p=0.18): not significant. Relapse 79% (15/19) vs 76.7% (46/60) (p=1.0); **durable first remission >16 mo in 4/19 (21%) vs 14/60 (23%)**; three vaccinated dogs alive without lymphoma at 959, 1103, 1287 d (2.6-3.5 y). Salvage COP gave durable second remission (>22 mo) in 4/10 vaccinated dogs; three of those alive at 689-1216 d. Tumour-specific IFN-gamma response in 1 of 9 tested dogs (2 more trending). Overall survival at 1 y 89.5% vs 74.1%, at 2 y 41.4% vs 25.4% (not significant).
- Toxicity: none attributed. Grade: OUTCOME. This is the only dog vaccine study that reports individual dogs alive at 2.6-3.5 y, and the concurrent control tail is the same size.

c) Whole-cell / lysate / microbead variants
- hGM-CSF DNA cationic-lipid-complexed autologous tumour cell vaccine, randomised placebo-controlled double-blind: no clinical benefit, small DTH/immunomodulation (Turek 2007, PMID 19754780, doi 10.1111/j.1476-5829.2007.00128.x). NEGATIVE.
- Large multivalent immunogen microbeads + IL-2 + GM-CSF, Phase 1 n=15 after CHOP-type induction: no toxicity, no adverse effect on DFI, DTH in about half (Henson 2011, PMID 21569195, doi 10.1111/j.1476-5829.2010.00234.x). No efficacy claim.
- DC pulsed with canine B-cell leukaemia lysate (GL-1): no DTH response and no T-cell infiltration, unlike the SCC vaccine (Tamura 2007, PMID 17917377, doi 10.1292/jvms.69.925). Not a lymphoma clinical trial.
- ImmuneFx (irradiated autologous tumour cells transfected with Emm55): a Methods chapter asserts "activity ... in canine lymphoma patients" (Ramiya 2014, PMID 24619685, doi 10.1007/978-1-4939-0345-0_21) but no primary lymphoma paper was found. Torigen (autologous tissue vaccine): reviews only (PMID 41006003, 2025; Leitao 2026 systematic review of 24 canine autologous-vaccine studies, PMID 42284812, doi 10.1016/j.vaccine.2026.128836: lymphoma has the most and the only randomised data, heterogeneous results, exploratory pooled trend toward reduced progression). No Torigen lymphoma trial found.
- Adoptive T cells (not a vaccine, but the nearest dog T-cell-effector data): ex vivo expanded autologous T cells after CHOP persisted 49 d, homed to tumour and improved survival (PMID 22355761, doi 10.1038/srep00249); autologous HSCT + adoptive T cells cured 4/10 dogs (disease-free >=2 y; PMID 34950726); allogeneic HSCT, 8/9 evaluable alive >4 y (PMID 35789057). These show dog lymphoma can reach multi-year remission by T-cell-mediated mechanisms; vaccines have not.

### 1.3 Dendritic-cell vaccines
- Dog: only the lysate-pulsed DC with negative DTH (17917377). No canine lymphoma DC clinical trial found.
- Human, idiotype-pulsed DC, n=35 (Timmerman 2002, Blood, PMID 11861263, doi 10.1182/blood.v99.5.1517): among 10 initial patients with measurable disease 4 responded (2 CR progression-free 44 and 57 mo; 1 molecular response PF 75+ mo); 15/23 (65%) of the post-chemo cohort mounted T-cell or humoral responses; 16/23 (70%) without progression at median 43 months after chemotherapy. Single arm.
- Murine: DC loaded with antibody-opsonised whole lymphoma cells protected against idiotype-negative variants, CD8-dependent (Franki 2008, PMID 17993615, doi 10.1182/blood-2007-03-080507): direct evidence that a whole-cell vaccine is not limited to one antigen. Mouse only.
- Review of DC-based FL immunotherapy including intratumoural unloaded DC + rituximab (Cox 2020, PMID 32322910).
- Escape profile: same as 1.2 (MHC-I dependent; persisters not reached; CD20/CD19-agnostic if whole-cell). Grade: TRANSFER (human/mouse).

### 1.4 Idiotype (BCR) vaccines, protein and DNA
Human (no canine idiotype vaccine study found):
- Phase 2: Hsu 1997 (n=41, median follow-up 7.3 y, PMID 9129015): 20/41 (49%) made anti-idiotype responses; in 32 first-remission patients freedom from progression 7.9 y responders vs 1.3 y non-responders (P=.0001), a correlation confounded by prognosis. Bendandi 1999 (n=20, PMID 10502821, doi 10.1038/13928): 8/11 PCR-positive patients converted to molecular remission and stayed; T-cell responses 19/20. Inoges 2006 (n=25 vaccinated in second CR, PMID 16985248, doi 10.1093/jnci/djj358): 80% responded; second CR >33 mo vs 13 mo historic. Navarrete 2011 (n=21+21 Fab-Id, PMID 21045197): 76% immune response, cellular response correlated with PFS and remission. Holman 2012 (n=15 after ASCT, PMID 21736867): PFS 59%, OS 52% at 9.05 y, single arm.
- Phase 3: Schuster/BiovaxID 2011 (PMID 21632504, doi 10.1200/JCO.2010.33.3005): 234 enrolled, 177 randomised 2:1, ITT median DFS 23.0 vs 20.6 mo (HR 0.81, p=.256, **negative primary endpoint**); 60 patients never vaccinated because 55 relapsed first; per-protocol 44.2 vs 30.6 mo (HR 0.62, p=.047); unplanned IgM-Id subgroup 52.9 vs 28.7 mo (p=.001), IgG-Id none. Levy/MyVax 2014 (PMID 24799467, doi 10.1200/JCO.2012.43.9273): 287 randomised 2:1 after CVP, median follow-up 58 mo, **no PFS or time-to-next-therapy difference**; only 41% made anti-Id responses; responders' PFS 40 mo, "whether this reflects a therapeutic benefit or is a marker for ... prognosis requires further study". Freedman/mitumprotimut-T 2009 (PMID 19414675, doi 10.1200/JCO.2008.19.8903): 349 post-rituximab, TTP **worse** with vaccine (9.0 vs 12.6 mo, HR 1.384, p=.019; nonsignificant after FLIPI adjustment).
- Why the Phase 3s failed (what the abstracts support): low immune-response rate (41% with MyVax), benefit confined to responders/IgM subgroups (selection), relapse before vaccination in about a third (55/177), rituximab-era comparators, and control arms that were themselves active immunotherapy (KLH + GM-CSF); Neelapu 2005 (PMID 16116429) shows T-cell priming survives B-cell depletion in MCL, and in that (Phase 2, MCL) study relapsing tumours showed no mutation or expression change in the target antigen, so antigen loss was not the explanation there (not shown for the FL Phase 3s). Whether the control arm's own immune stimulation masked an effect is plausible but not shown by these data.
- DNA idiotype vaccines: next-generation APC-targeted DNA vaccine in asymptomatic LPL, protocol and Phase 1 (Thomas 2018, PMID 29439670; 2012 commentary PMID 22595048). TCL1 as a shared, non-idiotype B-lymphoma target (Weng 2012, PMID 22645177).
- Escape questions: target is the tumour's own surface Ig (covers CD20/CD19 loss; but idiotype can itself be lost/mutated; B-cell receptor loss happens in some lymphomas: not quantified here); T-cell arm needs MHC-I or II; antibody arm does not need MHC and was the correlate in some trials; requires a clonal Ig (canine B-cell lymphoma is clonal by PARR) but no canine idiotype vaccine work exists; persisters: surface Ig often retained on resting B cells, but no persister data. Grade: TRANSFER only, and the transferred trials were negative or marginal.

### 1.5 Xenogeneic / CD20 / CD19 DNA vaccines
- No canine CD20, CD19 or other B-lineage xenogeneic DNA vaccine study was found in PubMed. (See searches not found.)
- Class precedent for xenogeneic DNA vaccines in dogs is melanoma: human tyrosinase DNA, Phase 1 n=9, median survival 389 d (Bergman 2003, PMID 12684396); adjunct to surgery, 58 vs 53 historic controls, improved disease-specific survival (Grosenbaugh 2011, PMID 22126691, doi 10.2460/ajvr.72.12.1631); but a retrospective comparison found no PFS/DFI/MST benefit (Ottnod 2013, PMID 23909996, doi 10.1111/vco.12057) and UK series median survival 455 d similar to US (Verganti 2017, PMID 28094857). Therefore even the licensed canine cancer vaccine class has contested efficacy.
- Mechanistic note: a B-lineage target such as CD20 vaccination induces antibody or T cells that would kill normal B cells too (antigen-agnostic to tumour vs normal), and adds nothing beyond the canine anti-CD20 antibody already in the model; it does not cover CD20 loss by definition. CD19 vaccine: same. Grade: ASSUMED (no data).

### 1.6 Neoantigen / mRNA / personalised vaccines
- Dog lymphoma: nothing found.
- Dog other tumours (platform feasibility and CNS-relevant): systemic mRNA-lipid particle vaccines in 10 dogs with glioma, median survival 123 and 155 d (Group A/B, vs historical palliative), mRNA payload localised to the brain tumour microenvironment with rapid immune signature shift after peripheral dosing (Carrera-Justiz 2025, PMID 41218853, doi 10.1136/jitc-2025-011817); immunomodulatory mRNA-LNP vaccine in 8 dogs with mixed tumours, 6/8 stable disease, median PFI not reached at 168 d (Han 2025, PMID 41173904). Autologous tumour-lysate + CD200 peptide in canine glioma, median survival 12.7 vs 6.36 mo vs historical control (Olin 2019, PMID 30682795). Historic controls again.
- Human lymphoma: neoantigen DNA vaccine in untreated LPL, n=9, stable disease or better, median TTP 72+ mo; **resistance mechanisms seen: HLA class II downregulation and paradoxical IGF upregulation in plasma cells** (Szymura 2024, PMID 39128904, doi 10.1038/s41467-024-50880-2); FL neoantigen landscape (58 tumours, median 15 high-quality neoantigens) and 4-patient pilot with PD-1 (Ramirez 2024, PMID 38713894); review (Shah 2026, PMID 42347594) concludes durable benefit "inconsistent" and best in MRD/post-transplant settings.
- Escapes: personalised multi-epitope (CD20/CD19 loss covered); MHC-I/II dependent (defeated by loss; Szymura shows class II loss as a resistance route); persisters not reached (antigens from mutated transcripts in dividing cells); needs WES+RNA-seq per dog (cost/time), compatible with early detection. Grade: TRANSFER (human LPL/FL) for feasibility only; ASSUMED for dog potency.

### 1.7 TLR agonists, immunostimulant liposomes, bacterial, and in-situ vaccination
- Dog: none found in lymphoma for CpG/TLR9 agonist, BCG, Listeria. The Dow-lab liposome-DNA complex studies found are in other tumours: PMIDs 16076252 (IL-2 gene, osteosarcoma lung metastases), 16138118 (soft-tissue sarcoma), 17338158 (hemangiosarcoma) (titles confirmed via search; abstracts not read, so no numbers claimed). Listeria-HER2 in canine osteosarcoma: Phase 1 n=18, 15/18 IFN-gamma responders, better survival than historical controls (Mason 2016, PMID 26994144, doi 10.1158/1078-0432.CCR-16-0088); **118-dog trial: no significant DFI or OS difference vs historical cohort** (Mason 2025, PMID 39955616, doi 10.1016/j.ymthe.2025.02.023).
- Human in-situ vaccination in lymphoma: low-dose RT (4 Gy) + intratumoural TLR9 agonist. Brody 2010 (PMID 20697067, doi 10.1200/JCO.2010.28.9793): n=15, 1 CR + 3 PR at untreated sites. Frank 2018 (PMID 30154192, doi 10.1158/2159-8290.CD-18-0743): n=29 untreated indolent lymphoma, 24 with shrinkage at untreated sites, 5 PR + 1 CR; Tregs and Tfh fell, effector T cells rose. Kolstad 2015 (PMID 26140239). Hammerich 2019 (Flt3L + RT + TLR3 agonist, abscopal remissions, PD-1+ T cells in non-responders, PMID 30962585, doi 10.1038/s41591-019-0410-x). Shree 2024 adding ibrutinib (ORR 50%, 1 CR, PMID 37939259, doi 10.1182/bloodadvances.2023011589); Shree 2025 adding OX40 agonist (1 PR, 9 SD, worse, PMID 39745391, doi 10.1158/1078-0432.CCR-24-2770). No long-term durability data found for any of these.
- Escape questions: does not need a pre-specified antigen (covers CD20/CD19 loss), but still T-cell dependent (MHC-I/II), works on bulk with accessible injection site (not CNS, not diffuse marrow), and depends on reversing Treg/Tfh suppression (Frank 2018 found low baseline CD4 Treg predicted benefit). Persisters: not reached by injection alone. Chemo combination: given to untreated patients; concurrent lymphodepleting chemo would blunt the tumour-infiltrating T-cell arm (mechanistic). Grade: TRANSFER (human indolent lymphoma only).

### 1.8 Oncolytic viruses
- Dog lymphoma: i.v. VSV-IFNbeta-NIS single dose in 9 dogs, two high-grade peripheral T-cell lymphoma dogs had rapid but **transient** remission and transient hepatotoxicity, no shedding (Naik 2018, PMID 29158470, doi 10.1158/1535-7163.MCT-17-0432). Reovirus killed 4/10 canine lymphoma lines with variable susceptibility, less susceptible than mast cell tumour (Hwang 2016, PMID 25319493). Newcastle disease virus (NDV-MLS) reduced survival of primary canine B-lymphoma cells by 34 +/- 12% in vitro, and localised to kidney, salivary gland, lung, stomach after i.v. in a T-cell lymphoma dog (Sanchez 2015, PMID 26703717). Ad5 infects canine lymphoid cells poorly (integrin and CAR dependent; Agarwal 2017, PMID 28068367).
- Escape questions: lytic kill does not need MHC (covers MHC-I loss for the direct part) and does not need CD20/CD19; needs viral receptor and replication, so quiescent persisters are poor hosts (mechanistic); CNS: viruses i.v. rarely cross BBB (not evidenced here); neutralising antibody after first dose. Grade: OUTCOME (transient, n=2) for T-cell lymphoma; nothing durable.

## 2. The ESCAPE questions, all platforms (matrix)

Legend: Y = covered, N = not covered, ? = no data, grade in brackets.

| Platform | Non-dividing persister | Defeated by MHC-I/B2M loss | CD20/CD19-independent (covers antigen loss) | Target expressed/required in quiescent cells | CNS access | Microenvironment/exhaustion | Chemo timing |
|---|---|---|---|---|---|---|---|
| dTERT Ad/DNA-EGT | N (ASSUMED; TERT low in resting B cells, tracks Ki67 in dog) | Yes, defeated | Y | TERT: expressed mainly in proliferating/GC cells; not shown in quiescent | ? (ASSUMED none) | Vulnerable; works in remission setting | Given from CR/wk 4 with COP/CHOP; no vaccine-alone effect; chemo did not impair response in dogs (see 2.3) |
| HSPPC-HA autologous (APAVAC) | N (ASSUMED) | Yes, defeated | Y (polyvalent) | Peptides of bulk tumour | ? | Benefit concentrated in steroid-naive, high-LDH, stage V | Concurrent with 8-drug protocol |
| CD40-B RNA (autologous) | N | Yes | Y (whole tumour RNA) | n/a | ? | Benefit mostly after salvage | After CR |
| DC / lysate | N | Yes | Y if whole-cell | n/a | ? | Dog DC lysate produced no DTH | After chemo |
| Idiotype protein/DNA | N (resting B cells may keep sIg; unmeasured) | T-cell arm yes; antibody arm no | Y (targets Ig) | sIg | ? | Human Phase 3 failed | After CR; B-cell depletion OK (16116429) |
| Neoantigen / mRNA | N | Yes (and class II loss seen) | Y | mutated genes in dividing cells | ? (mRNA-LPA reached canine glioma) | Needs checkpoint partners | Not tested in lymphoma |
| TLR9 / in situ | N | Yes (T-cell) | Y | n/a | N (needs local injection) | Reverses Treg/Tfh; OX40 add-on failed | Given without chemo |
| Oncolytic virus | N (likely) | No (direct lysis) | Y | Needs receptor | ? | Transient | Not tested with CHOP |

### 2.1 Persisters (non-dividing, drug-tolerant)
- No vaccine study has tested persister kill. The antigen-presentation machinery is downregulated in quiescent normal stem cells via NLRC5, making quiescent cells T-cell resistant until they re-enter cycle (Agudo 2018, PMID 29466757, doi 10.1016/j.immuni.2018.02.001). That is a normal-tissue mouse result; transfer to lymphoma persisters is plausible but unproven. Hold as a risk, not a number.
- In vivo direct CTL killing is insufficient by itself in a modelled mouse tumour; an IFN-gamma antiproliferative effect (which acts on dividing cells) accounted for much of the control (Beck 2019, PMID 31040155, doi 10.1158/0008-5472.CAN-18-3147; Beck 2021, PMID 34073822). That weakens the case that vaccine-induced T cells kill non-cycling residual cells.
- Conclusion for model: persister kill by vaccine = ASSUMED low (0 to a small fraction of the proliferating-compartment rate); no grade above ASSUMED.

### 2.2 MHC-I/B2M loss
- Human DLBCL: B2M inactivated in 29% and CD58 in 21%; HLA-I aberrant in >60% (Challa-Malladi 2011, PMID 22137796, doi 10.1016/j.ccr.2011.11.006). Canine frequency: not found; canine DLBCL genomics reports TRAF3, FBXW7, POT1, TP53, SETD2, DDX3X, TBL1XR1 as top genes with no B2M mention in the abstracts (PMIDs 35726023, 39922874, 40506464). Low class II MHC expression predicts worse canine B-cell lymphoma outcome (Rao 2011, PMID 21781170). So B2M status in dogs is unmeasured (not found), not shown absent.
- Functional proof that MHC-I loss defeats T cells: viral MHC-I downmodulation made CTLs fail to kill (Halle 2016, PMID 26872694, doi 10.1016/j.immuni.2016.01.010); MHC-I-deficient mouse CNS lymphoma did not respond to T-cell-based therapies and was controlled only by macrophages (Pages-Geli 2026, PMID 42021682, doi 10.3324/haematol.2025.300015).
- Conclusion: every MHC-I-dependent platform is defeated by this escape; model it as a pre-existing or selectable sub-clone fraction (canine fraction unmeasured, ASSUMED from the human 29% only as a stated transfer).

### 2.3 Combining with chemotherapy (lymphodepletion vs vaccine)
- Dog data: doxorubicin did not reduce T or B counts; multi-drug chemo gave a persistent B-cell decrease; de novo vaccine antibody titres were not different from controls (Walter 2006, PMID 16594592); pre-existing titres unaffected (Henry 2001, PMID 11697366). Remission after doxorubicin spontaneously improved CTL activity and lowered circulating Tregs (Mitchell 2012, PMID 22293625). Adoptive T cells infused after CHOP persisted 49 d and improved survival (O'Connor 2012, PMID 22355761), i.e. lymphodepletion then add-back is the best-supported sequence. Human MCL: vigorous T-cell responses to idiotype vaccine despite severe B-cell depletion (PMID 16116429).
- Take-home: all dog vaccine benefits were obtained with vaccine started in remission, concurrently with maintenance or late-induction chemo, in a low-burden MRD setting; nothing supports vaccinating bulk disease.

### 2.4 CNS
- No lymphoma vaccine study measured CSF or brain T cells, nor CNS relapse incidence. Closest evidence: peripheral mRNA vaccine reached canine glioma with immune activation (41218853); CD200 + lysate vaccine canine glioma (30682795); both use historical controls. CNS lymphoma in mouse with MHC-I loss resists T-cell therapy (42021682). Grade for CNS sanctuary coverage: ASSUMED (no datum). It should not be counted as closing the CNS sanctuary.

## 3. Turning each vaccine into a model input (transfer logic and weaknesses)

### 3.1 Mechanistic per-day kill (TRANSFER on k_CTL, ASSUMED on E:T)
Structure (mass action, as used for in vivo CTL killing; Regoes 2007 PMID 17242364, Yates 2007 PMID 18074025): net kill rate on visible target cells k_v = k_CTL x (E/T)_eff x p_present x duty.
- Verified per-CTL anchors, both mouse: one CTL took on average 6 h to kill one solid-tumour target by intravital imaging (Breart 2008, PMID 18357341, doi 10.1172/JCI34388), i.e. a ceiling of about 4 kills/CTL/day; 2-16 kills/CTL/day for virus-infected targets, with failure when MHC-I is downmodulated (Halle 2016, PMID 26872694). Beck 2019 (31040155) parameterised from in vivo measurements found contact killing alone too slow to regress EL4 tumours. So k_CTL of roughly 1-4 per day is a defensible TRANSFER ceiling for MHC-I-positive, antigen-presenting cells, and it probably overstates the dog in-tumour rate.
- Worked inversion (arithmetic, not data): to reach the bar of 0.090/day on the visible cells needs (E/T)_eff x p_present x duty = 0.09/k_CTL. At k_CTL = 4 and p = duty = 1, E/T = 0.0225. At k_CTL = 1, p = 0.5, duty = 1: E/T = 0.18. At k_CTL = 1, p = 0.1: E/T = 0.9. So the required intratumoural effector:target ratio spans roughly 2% to about 1:1 depending on assumptions nobody has measured in dog lymphoma.
- What is measured in dogs: blood ELISpot 50-250 SFC/10^6 PBMC (20531395) and 7-1464 (mean peak 445) (23902422), i.e. 0.005%-0.15% of PBMC, in blood not tumour, for one antigen, with no validated conversion to tumour E:T. So E:T is ASSUMED.
- Weakness: applies to dividing or at least MHC-I-expressing cells only; ignores exhaustion and Tregs; single-antigen vaccines (TERT) also lose to antigen-low subclones; the persister term should be set to a low ASSUMED value (see 2.1).

### 3.2 Outcome-calibrated effect (OUTCOME)
If relapse time is regrowth time, T = ln(N_relapse/N_residual)/g and a vaccine that adds kill k_v to regrowth rate g gives T'/T = g/(g - k_v), so k_v = g x (1 - T/T'). Observed TTP ratios (vaccine/control): HSPPC DLBCL 250/98 d = 2.55 (k_v about 0.61 g), HSPPC indolent 209/85 = 2.46, HSPPC RCT 304/41 = 7.4 (k_v about 0.87 g; extreme, n=19), CD40-B 366/327 = 1.12 (k_v about 0.11 g), dTERT COP PFS 11.4/11.3 = 1.0 (k_v about 0). The multivariable HR for no vaccine in 148 DLBCL dogs was 2.3 for progression (31174615), i.e. relapse hazard about 0.43x. The regrowth rate g is the model's own number and is not in these papers. This treats the vaccine as acting on regrowing (dividing) cells only, which is what the data can support. Weakness: control arms differ in quality (HSPPC DLBCL control median TTP 98 d, RCT control 41 d are below contemporary CHOP PFS of about 176-244 d), non-random assignment, retrospective design.

### 3.3 Durable-fraction contribution (OUTCOME; this is the key number for the 10-year goal)
- Canine tail comparisons: DLBCL 2-y survival 19% vs 13%, 3-y 10% vs 8% (31174615); durable first remission >16 mo 21% vs 23% (21904611); dTERT PFS median identical (23902422); dTERT/CHOP 94% dead by 277 wk (30537967). Chemo-only tail in other dog cohorts: 2-y disease-free 0% and 2-y survival 11% (n=9 historical, PMID 37700548); in the same paper sequential low-dose-rate half-body irradiation gave 56% 2-y disease-free (n=9), which is what a durable effect looks like in dogs and which no vaccine series approaches.
- Therefore the best-supported vaccine contribution to the plateau is 0 to about +2 percentage points at 2-3 years. Anything at 10 years is ASSUMED. The vaccine shifts the early hazard; it has not been shown to convert relapsing dogs into cured dogs.

## 4. Toxicity summary
- dTERT Ad/DNA-EGT: none in 52 dogs; needs general anaesthesia for electroporation each cycle; Ad neutralising immunity on repeat; TERT-class autoimmunity (B-cell depletion) seen with adoptive T cells in mouse, not with vaccination.
- HSPPC-HA: none beyond chemo (300 dogs, 31174615; no AEs).
- CD40-B: none attributed; 3 vaccinated dogs euthanised for unrelated causes (2 hemangiosarcoma, 1 "declining health" with no lymphoma or autoimmunity at necropsy).
- Autologous whole-cell/lysate: mild.
- Human: idiotype vaccine toxicity mild (injection-site); the worse outcome in Freedman 2009 was efficacy, not toxicity.
- Oncolytic VSV: transient hepatotoxicity.
- Dog-specific class warning: AAV gene therapy in a haemophilia dog developed multicentric lymphoma with vector integrations (PMID 38094200; title only read), a caution for integrating vectors, not relevant to Ad/plasmid.
- Axis for the toxicity ledger: low, mostly injection-site/anaesthesia; no organ axis reported for vaccines as given.

## 5. Availability
- Licensed: none for canine lymphoma found. (Canine anti-CD20/anti-CD52 antibodies are not vaccines; the 2016 review PMID 26545847 discusses them and autologous vaccines.)
- Investigational/commercial-use: APAVAC (Europe), Tel-eVax (Evvivax; trial), Torigen/ImmuneFx (autologous, reviewed, no lymphoma trial found).
- Buildable: CD40-B RNA (research), DC, neoantigen/mRNA (platform exists in dog glioma), TLR9 in-situ (human reagent; canine use not found).

## 6. Evidence grade table (what the model may use)

| Platform | Potency (per-day kill) | Persister coverage | Escape coverage claims | Outcome evidence |
|---|---|---|---|---|
| dTERT Ad/DNA-EGT | ASSUMED (E:T) on TRANSFER (k_CTL) | ASSUMED ~0 | CD20/CD19 loss: Y (mechanistic). MHC-I loss: N. Persister: N | OUTCOME: OS +, PFS null, n=52, historic/self-selected controls, <=~5 y max |
| HSPPC-HA (APAVAC) | as above; outcome-calibrated k_v ~0.6 x g (OUTCOME) | ASSUMED ~0 | as above | OUTCOME: RCT n=19 + 45 + 300; tail flat |
| CD40-B RNA | as above | ASSUMED ~0 | as above | OUTCOME: null on TTP/LSS; durable fraction equal to control |
| DC/lysate | none | none | none | dog negative (DTH); human single-arm |
| Idiotype | none for dog | none | none for dog | TRANSFER: human Phase 2 positive, Phase 3 negative/marginal |
| Neoantigen/mRNA | none for lymphoma | none | none | TRANSFER: human LPL Phase 1, dog glioma feasibility |
| TLR9 in situ | none for dog | none | none | TRANSFER: human indolent lymphoma, n=15-29 |
| Oncolytic | none | none | none | OUTCOME (n=2, transient) |

## 7. Searched and NOT found
- Any peer-reviewed canine lymphoma trial of: CpG/TLR9 agonist, BCG, Listeria, immunostimulatory liposome-DNA complexes (Dow lab items found were in sarcoma, osteosarcoma, hemangiosarcoma), mRNA or neoantigen vaccines, DNA idiotype vaccines, CD20/CD19 DNA or xenogeneic vaccines, DC-vaccine clinical trials, allogeneic/whole-cell lysate trials beyond those above, an ImmuneFx or Torigen lymphoma primary paper, and cyclophosphamide-timed vaccine studies.
- A canine lymphoma B2M/MHC-I loss frequency; any measurement of TERT in quiescent canine lymphoma cells or persisters; any vaccine-induced T cells in CSF or CNS relapse data for a lymphoma vaccine; per-dog individual survival curve tails beyond what is tabulated above; Kaplan-Meier numbers-at-risk for dTERT beyond 2 years; Marconato 2014 arm sizes and control molecular-remission rate (abstract only).
- Human: long-term (>5 y) durability data for in-situ vaccination; a human lymphoma Phase 3 of a non-idiotype vaccine; any lymphoma mRNA vaccine clinical data.
- "Hastim" as a search term returned no relevant records; Rossi 2024 (38318840) is the only hit linking the HA vaccine to canine lymphoma.

## 8. Candid limits
- Survival gains measured in weeks to about 2-3.5 years are not 10-year data; the longest dog follow-up is about 3.5 y (CD40-B, 1287 d) to about 5.3 y (Tel-eVax window) and the longest human vaccine follow-up (Hsu 1997) is median 7.3 y with only correlative benefit.
- dTERT, APAVAC 2015 and 2019, and CD40-B comparisons are not randomised (owner consent, retrospective, or selected controls); only 24300788 (n=19) and 19754780 (negative) are randomised.
- Immune-response status as a predictor is confounded (responders have better prognosis), so "vaccine response correlates with survival" does not support causality.
- Gavazza/Peruzzi details were taken from publisher-blocked pages via summarised quotes; verify before quoting in a document of record.
- No evidence here supports counting any vaccine as closing persister, MHC-I-loss, or CNS escapes. If the model adds a vaccine agent, the honest entry is "covers CD20/CD19 loss (mechanistic), partial benefit on dividing residual disease (OUTCOME), zero on persisters/MHC-I loss/CNS (ASSUMED)", with no change to the 10-year plateau.
