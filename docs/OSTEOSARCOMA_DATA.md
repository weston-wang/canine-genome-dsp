# Osteosarcoma evidence and data map

This document defines the evidence boundary for the osteosarcoma Volterra-HSMM program. The source
registry is `data/sources.csv`; aggregate clinical calibration targets are in
`data/clinical/osteosarcoma_clinical_anchors.csv`. The registry was checked on **2026-08-02**.

The central limitation is deliberate and important: there is currently no public, patient-level,
longitudinal cohort in which an osteosarcoma RNA-vaccine composition, dose history, immune trajectory,
and clinical outcome are all observed together. The available data can support comparative state
definitions, prior estimation, retrospective calibration, and prospective trial design. They cannot
establish that a model-designed vaccine is superior to current care.

Four evidence categories must remain distinct throughout the project: current standard care;
completed non-RNA intervention studies; completed, early RNA-platform feasibility evidence; and
active or recruiting RNA studies with no posted outcomes. A protocol or trial-status page is not an
outcome dataset, and a completed Listeria, cytokine, or mTOR study is not evidence for an RNA cargo.

## Data resources

| Resource | What it is | Public granularity | Intended use | Important limitation |
|---|---|---|---|---|
| **ICDC COTC021** | 152 dogs assigned standard amputation/carboplatin plus sequential adjuvant sirolimus in the COTC021/022 randomized study | Open clinical, RNA-seq, and NanoString resources in ICDC | Tested treatment-timing interaction and randomized no-significant-difference outcome anchor | The intervention is sirolimus, not an RNA vaccine; files and clinical records must be joined through ICDC identifiers rather than inferred from GEO row order |
| **ICDC COTC022** | 157-dog contemporaneous standard-of-care arm from the same randomized study | Open clinical, RNA-seq, and NanoString resources in ICDC | Primary canine standard-of-care calibration cohort | Canine disease-free interval starts at amputation and is not numerically interchangeable with human event-free survival |
| **GSE238110** | Bulk RNA-seq from 186 primary canine tumors: 93 labeled COTC021 and 93 labeled COTC022 | Open counts, TPM values, and raw sequencing | Prognostic features, cross-species expression alignment, and HMM emission priors | It is an omics subset of the 309-dog intent-to-treat population, not the full trial; do not reconstruct missing subjects or outcomes |
| **GSE76127 / COS33** | Pretreatment microarrays from 33 canine primary tumors with published individual DFI and chemotherapy metadata | Open series matrix plus Europe PMC supplementary table | Bundled held-out-dog static prognostic sensitivity analysis | One sample per dog, heterogeneous chemotherapy, no public event/censor indicator, and cohort-wide upstream GEO preprocessing; ordinary regression is not a survival analysis or an HSMM-emission validation and cannot estimate vaccine memory, state transitions, or a policy effect |
| **COTC026 publication** | Prospective 118-dog single-arm study of standard care followed by the HER2-expressing Listeria vaccine ADXS31-164 | Aggregate clinical and correlative results in the article | Completed non-RNA timing benchmark and repeated-immunization hypothesis generation | No public patient-level accession was identified; its COTC022 comparison is historical, its vector is not RNA, and it showed no significant DFI or OS difference |
| **2026 radiation + Lm-LLO-HER2 pilot** | Fifteen treatment-naive dogs received palliative radiation followed by repeated HER2-expressing Listeria immunotherapy instead of amputation/chemotherapy | Open article with individual clinical graphics; aggregate nCounter comparisons used nine dogs at baseline/treatment 4 (five longer-term, four shorter-term) and five dogs at treatment 8; no raw patient-level accession identified | Recent non-RNA timing and immune-correlate analog | Small, nonrandomized, historically compared, and in a different limb-preserving/palliative-radiation setting; the subcohorts are exploratory and not an RNA efficacy comparator |
| **GSE252470** | Single-cell RNA-seq of six treatment-naive canine primary osteosarcomas, represented by eight libraries because two dogs have technical replicates | Open raw and processed 10x data | Tumor, myeloid, lymphoid, stromal, and exhaustion-state emission signatures | Six biological subjects cannot estimate clinical transition probabilities; technical replicates are not independent dogs |
| **GSE304066 / COTC030** | Bulk RNA-seq from 26 canine primary tumors collected in the adjuvant inhaled recombinant human IL-15 study | Open count matrix and raw sequencing | Completed non-RNA timing guardrail and tumor-state covariates | The clinical trial enrolled 37 dogs; the GEO tumor subset is not the full intent-to-treat cohort and is not longitudinal |
| **GSE299494** | Visium spatial transcriptomics of 14 samples from 11 dogs, including 11 primary tumors, two matched metastases, and one matched recurrence | Open spatial counts and images | Spatial immune exclusion, macrophage niches, metastatic escape, and primary-to-relapse contrasts | Only three non-primary samples are present; paired observations must stay grouped by dog |
| **TARGET-OS** | NCI human osteosarcoma collection with clinical annotations and multiple genomic/transcriptomic data types | Mixed: derived clinical/omics resources are public while some underlying sequence-level data require controlled access | Human antigen priors, conserved pathways, outcome stratification, and external validation | File and case counts vary by modality and release; access status must be checked at download time, and TARGET is not an RNA-vaccine cohort |
| **Canine total-tumor RNA-LPA pilot** | Conference abstract describing five treated dogs | Aggregate-only abstract; one individual radiographic course is described | Direct RNA-platform feasibility and acute-response hypothesis generation | No controlled efficacy estimate or public patient-level time series; one reported response followed by relapse |
| **UF canine RNA-nanoparticle plus anti-PD-1 trial** | Currently enrolling study in dogs with appendicular osteosarcoma; tumor-derived RNA vaccine, anti-PD-1, required radiation, serial blood, and imaging | Public study page only | Prospective validation target and candidate sampling template | Target enrollment and outcomes are not posted; status is time-sensitive |
| **RNA-PRIME, NCT05660408** | Human phase I/II pp65 RNA-LP bridge followed by personalized pp65/total-tumor-mRNA RNA-LP for recurrent high-grade glioma or recurrent pulmonary/unresectable osteosarcoma | Public registry; no posted results | Human feasibility, safety, schedule, and future external-validation target | Estimated enrollment of 36 combines glioma and osteosarcoma; no osteosarcoma-specific denominator or efficacy result is public |

The ICDC June 2026 release reports open NanoString additions for COTC021 and COTC022, including
primary and predominantly metastatic lesions. Its subject counts describe the clinical studies; its
file counts are not patient counts. GEO likewise describes deposited samples, which must not be
silently expanded to the parent clinical cohort.

## Clinical anchors

The clinical CSV uses one row per aggregate endpoint. Blank numerator or denominator fields mean the
source reported a Kaplan-Meier estimate, qualitative observation, or registry status rather than a
simple binomial count. Values are never reconstructed by multiplying a rounded percentage by a cohort
size. The `study_status` and `intervention_class` columns explicitly separate completed studies from
active or recruiting studies without posted outcomes and RNA interventions from non-RNA comparators.

### Canine current standard care and completed non-RNA combinations

The 2025 canine appendicular-osteosarcoma consensus describes definitive local control plus systemic
chemotherapy as standard care and identifies carboplatin as the adjuvant single agent of choice. The
2026 AAHA oncology guideline likewise lists amputation, limb-sparing surgery, or stereotactic
radiation for local control and carboplatin- or doxorubicin-based chemotherapy. For this project's
post-amputation minimal-residual-disease target, the current-care reference remains amputation plus
adjuvant carboplatin; that choice does not imply that amputation is the only valid local-control
option for every dog.

In the randomized COTC021/022 intent-to-treat population, the COTC022 standard-care arm had median
disease-free interval (DFI) **180 days** and median overall survival (OS) **282 days**. Adding
sirolimus sequentially after carboplatin produced median DFI **204 days** and OS **280 days**, with no
significant difference from standard care. This is the most defensible canine arm-to-arm calibration
source because treatment allocation was concurrent and randomized.

COTC026 used three intravenous vaccine doses at three-week intervals after amputation and four
carboplatin cycles. It reported median DFI **217 days** and OS **341 days** after the HER2 Listeria
vaccine, versus historical COTC022 values of 180 and 282 days. The reported comparisons were not
significant (DFI p=0.33; OS p=0.10). These numerical differences must not be labeled improvement or
superiority.

COTC030 tested two weeks of inhaled IL-15 after amputation and before carboplatin. In its 37-dog
intent-to-treat cohort, median DFI was **109 days** and median OS **224 days**, compared with 180 and
282 days in historical COTC022 controls. The study stopped for futility. Although the historical
comparisons were statistically significant (DFI p=0.033; OS p=0.003), they were not randomized; they are a strong guardrail
against unsupported timing extrapolation, not proof that IL-15 itself caused worse outcomes.

A June 2026 pilot treated 15 dogs whose owners declined standard amputation/chemotherapy with two
8-Gy palliative-radiation fractions followed by repeated Lm-LLO-HER2. Aggregate nCounter comparisons
used nine dogs at baseline and treatment 4 (five longer-term and four shorter-term survivors), with
five dogs represented at treatment 8; no raw patient-level accession was identified. The report gave
median OS of **159 days** for the 15 combination-treated dogs versus **124 days** for an 83-dog
historical palliative-radiation-only cohort (log-rank p=0.0237). This was a small, nonrandomized,
non-RNA study in a different local-control setting, and salvage treatment was permitted after
progression. The historical comparison cannot establish treatment benefit or calibrate the
postoperative RNA policy; the study is retained only as a timing and serial immune-measurement analog.

### Completed early RNA-platform evidence

The five-dog total-tumor RNA-LPA abstract reports that vaccination was feasible, caused acute blood
count and cytokine changes within six hours, and that one dog receiving four two-weekly doses had an
initial radiographic resolution of pulmonary metastases followed by new metastases. The other dogs'
measurable-disease evaluability is not reported, so this must not be encoded as a 1/5 response rate.

This abstract is the only completed direct canine RNA-platform evidence in the current map. It is
feasibility and acute pharmacodynamic evidence, not a controlled efficacy benchmark.

### Active or recruiting RNA trials with no posted outcomes

The UF canine RNA-nanoparticle plus anti-PD-1 page says the study is currently enrolling. It requires
radiation, gives vaccine and anti-PD-1 by intravenous infusion, and follows blood immune markers and
imaging. No enrollment target or outcome is posted.

RNA-PRIME is active but not recruiting in the ClinicalTrials.gov snapshot used here. Its estimated
enrollment is 36 across both pediatric high-grade glioma and osteosarcoma. The osteosarcoma arms use
at least three two-weekly off-the-shelf pp65 RNA-LP doses during personalized-product manufacture,
then three two-weekly and nine monthly personalized pp65/total-tumor-mRNA RNA-LP doses. Manufacturing
feasibility and maximum tolerated dose are primary outcomes; no results are posted.

Neither active study can be used to estimate a response rate, survival effect, Volterra kernel, or
optimal schedule until results are posted and the relevant patient-level data become available.

### Human current-care benchmark

The EURAMOS-1 M0-CSR landmark cohort contains **1,549** patients with localized high-grade
osteosarcoma who reached complete surgical remission after induction therapy. Five-year EFS from
surgery was **64% (95% CI 61-66%)** and five-year OS was **79% (95% CI 77-81%)**. EURAMOS used MAP
induction—high-dose methotrexate, doxorubicin, and cisplatin—with surgery and protocol-defined
postoperative treatment.

These EURAMOS estimates are conditional on complete surgical remission and include postoperative
treatment variation. They are a current-care clinical target, not a pure MAP-only randomized arm and
not a valid direct comparator for recurrent-disease RNA-PRIME. Human and dog survival times should be
modeled with separate clocks and observation processes.

## Evidence tiers

- **A_randomized_concurrent**: prospective randomized comparison with a concurrent control. This is
  the strongest causal calibration tier in the current registry.
- **B_prospective_historical_control** or **B_prospective_cohort**: prospective data without a
  randomized concurrent contrast for the recorded endpoint. Useful for calibration, not a standalone
  superiority claim.
- **C_early_exploratory**: small case series or conference abstract. Useful only for feasibility and
  prior support.
- **D_registry_no_outcomes**: active study metadata without posted outcome results. Useful for
  protocol design and future validation only.

## Rules for Volterra-HMM use

1. Keep **patient-level observations**, **aggregate clinical anchors**, and **trial registries** in
   separate likelihood components. Never expand aggregate endpoints into synthetic patients.
2. Split train and validation data by dog or human patient. Technical replicates, primary-metastatic
   pairs, and repeated samples stay in the same fold.
3. Estimate species-specific baseline hazards, dwell times, MHC/DLA presentation models, and
   observation noise. Share only explicitly modeled pathway- or feature-level priors across species.
4. Treat the COTC030, COTC026, and June 2026 radiation-plus-Listeria comparisons as
   historical-control evidence. Preserve their p-values and comparability caveats; do not label the
   interventions beneficial or harmful from the model alone.
5. Use GSE252470 and GSE299494 mainly to define latent-state emissions. They do not contain enough
   longitudinal treatment excitation to identify a treatment-transition kernel.
6. Restrict Volterra interactions to low-order, low-rank terms supported by real intervention timing.
   Neither co-administered antigen mixtures nor aggregate survival curves identify unrestricted
   antigen-by-antigen kernels.
7. Keep stage- and setting-appropriate standard care fixed in inverse design: surgery and
   chemotherapy for the postoperative canine MRD program, MAP-based therapy and surgery for
   localized human disease, and radiation only where the chosen clinical protocol requires it. A
   generated cargo or schedule is a prospective trial hypothesis, never a clinical recommendation.

## Primary and official provenance

- [COTC021/022 randomized trial](https://pmc.ncbi.nlm.nih.gov/articles/PMC8172450/) and
  [ICDC COTC021/022 release notes](https://datacommons.cancer.gov/news/crdc-components-updates-june-2026)
- [GSE238110](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE238110),
  [GSE76127](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE76127),
  [GSE252470](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE252470),
  [GSE304066](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE304066), and
  [GSE299494](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE299494)
- [COTC026 primary report](https://pubmed.ncbi.nlm.nih.gov/39955616/) and
  [COTC030 primary report](https://pmc.ncbi.nlm.nih.gov/articles/PMC12589053/), plus the
  [2026 radiation + Lm-LLO-HER2 pilot](https://pmc.ncbi.nlm.nih.gov/articles/PMC13264224/)
- [TARGET-OS catalog](https://datacatalog.ccdi.cancer.gov/dataset/TARGET-OS)
- [Canine RNA-LPA pilot abstract](https://jitc.bmj.com/content/11/Suppl_1/A1519) and
  [UF canine RNA-nanoparticle trial page](https://research.vetmed.ufl.edu/research-programs/clinical-trials/small-animal/mrna-vaccine-study-for-dogs-with-appendicular-osteosarcoma-currently-enrolling/)
- [RNA-PRIME NCT05660408](https://clinicaltrials.gov/study/NCT05660408) and
  [NCI trial description](https://www.cancer.gov/research/participate/clinical-trials-search/v?id=NCI-2025-02759&r=1)
- [EURAMOS-1 outcomes](https://pmc.ncbi.nlm.nih.gov/articles/PMC6506906/) and
  [NCI osteosarcoma treatment PDQ](https://www.cancer.gov/types/bone/hp/osteosarcoma-treatment-pdq)
- [2025 canine appendicular osteosarcoma consensus](https://www.frontiersin.org/journals/veterinary-science/articles/10.3389/fvets.2025.1633593/full)
  and [2026 AAHA oncology guideline](https://www.aaha.org/resources/2026-aaha-oncology-guidelines-for-dogs-and-cats/section-1-overview-of-common-cancers/)
