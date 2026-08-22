# Melanoma clinical and dynamic anchors

`data/clinical/melanoma_clinical_anchors.csv` is a long-format, aggregate evidence table for a
stage-specific melanoma benchmark. It combines a longitudinal immune-dynamics series with two
randomized trials; it is not a patient-level joined cohort.

## What the records represent

- **GSE272993** provides open longitudinal PBMC scRNA-seq, TCR, and antibody-derived-tag data from
  32 deposited patients with stage IV melanoma sampled at baseline and nominally every three weeks
  during anti-PD-1, anti-CTLA-4, or combination blockade. The associated Cancer Cell analysis used
  36 patients across GSE272993 and related accessions and reported melanoma-specific CD8 responses
  at weeks 3 and 6 and larger combination-therapy clonal-response waves at weeks 6 and 9. The CSV
  retains the GSE272993 deposited count of 32 rather than silently assigning all 36 to that accession.
- **OpACIN-neo (NCT02977052)** randomized 86 treated patients with macroscopic resectable stage III
  melanoma across three neoadjuvant dose/schedule arms. The table records the published week-6
  pathological and radiological response counts and grade 3-4 immune-related adverse events through
  week 12. Its broad pathological response rate (pRR) uses less than 50% viable tumor and therefore
  includes both major and partial pathological responses. Separate MPR rows use no more than 10%
  residual viable tumor: 21/30 (70.0%), 19/30 (63.3%), and 12/26 (46.2%) in arms A, B, and C. In the
  sequential arm C, ipilimumab was given at weeks 0 and 3 and nivolumab just after the week-3
  ipilimumab dose and again at week 5; this calendar should not be reconstructed as simultaneous
  q3-week combination dosing.
- **NADINA (NCT04949113)** randomized 423 patients with macroscopic resectable stage III melanoma.
  The clinical benchmark is two cycles of ipilimumab 80 mg plus nivolumab 240 mg every three weeks,
  surgery at week 6, and pathological-response-directed adjuvant therapy. The comparator is upfront
  surgery followed by 12 cycles of nivolumab 480 mg every four weeks. Major pathological response
  (MPR) means no more than 10% residual viable tumor.

NADINA event-free survival (EFS) runs from randomization to unresectable progression before surgery,
recurrence, or death caused by melanoma or treatment. The CSV includes the peer-reviewed 12-month
primary result and the later 24-month EFS, distant-metastasis-free survival (DMFS), and completed-
treatment safety update. The 24-month values come from a published conference abstract; arm-level
confidence intervals for the survival percentages and safety denominators were not reported there,
so those cells are intentionally blank.

NADINA toxicity has three distinct snapshots in the table. The primary report observed grade 3 or
higher systemic-treatment-related adverse events in 63/212 (29.7%) neoadjuvant-arm patients through
the January 2024 cutoff. Of the neoadjuvant group, 23.1% had such an event within 12 weeks and hence
attributable solely to neoadjuvant treatment; the article did not publish its numerator, so the CSV
does not back-calculate one. The later completed-treatment abstract reports 31.1%, without an arm
safety denominator. These are not duplicate estimates at the same follow-up.

## Modeling limits

- These rows are aggregate anchors, not individual observations. They can test whether simulated
  arm-level response and toxicity are calibrated, but cannot identify a patient-level treatment
  policy or support off-policy causal evaluation.
- GSE272993 is observational stage IV disease, whereas OpACIN-neo and NADINA are randomized stage III
  neoadjuvant trials. Immune-state dynamics may inform a hierarchical prior, but outcomes cannot be
  row-merged or transported without explicit stage and cohort effects.
- Four approximately three-weekly immune observations support event-aligned trajectory or low-order
  memory summaries. They do not support claims about oscillatory frequency, resonance, or a stable
  high-order Volterra kernel.
- OpACIN-neo supplies randomized dose and schedule variation but has small arms. NADINA supplies the
  clinically relevant comparator and longer-horizon outcome benchmark but not randomized continuous
  timing variation. Candidate schedules should remain within tested clinical support unless a new
  prospective trial supplies the missing excitation.
- Toxicity endpoints differ: OpACIN-neo reports grade 3-4 immune-related events within 12 weeks;
  NADINA reports grade 3 or higher systemic treatment-related events for a 12-week neoadjuvant-only
  window and for longer primary and completed-treatment snapshots. They are separate calibration
  targets, not interchangeable labels.
- NADINA's proportional-hazards assumption was violated in the primary analysis. Preserve landmark
  EFS and restricted-mean-survival analyses rather than using one constant hazard ratio as the whole
  response model.

The defensible near-term use is a fail-closed benchmark: reproduce OpACIN-neo arm response/toxicity
within uncertainty, then compare a locked model-generated policy against the NADINA regimen on MPR,
EFS/DMFS, surgery feasibility, and serious toxicity. Any apparent improvement remains a trial
hypothesis, not a treatment recommendation.

## Primary provenance

- [GSE272993 GEO record](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE272993) and
  [associated Cancer Cell article](https://doi.org/10.1016/j.ccell.2024.08.007)
- [OpACIN-neo primary report](https://pubmed.ncbi.nlm.nih.gov/31160251/) and
  [trial record](https://clinicaltrials.gov/study/NCT02977052)
- [NADINA primary report](https://doi.org/10.1056/NEJMoa2402604),
  [trial record](https://clinicaltrials.gov/study/NCT04949113), and
  [two-year update](https://doi.org/10.1016/j.annonc.2025.09.069)
- [2025 ESMO cutaneous-melanoma clinical practice guideline](https://doi.org/10.1016/j.annonc.2024.11.006)
