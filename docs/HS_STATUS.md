# HS branch status — literature sweep, September 2026

Purpose: settled results and known gaps for the histiocytic sarcoma work, so a later thread does
not re-derive or re-litigate them. Written per `CLAUDE.md` rules 1, 4, 5 and 7.

Sweep date: 2026-09-30. Sources: PubMed, Europe PMC, company disclosures, and the 2026 MTAP
review. Every item below is labelled **NEW**, **PARTIAL** (repo has the claim, not the detail), or
**ALREADY COVERED**, with where the repo already holds it.

---

## 1. The premise of Move 2 now has direct empirical support — NEW

Mottier, Houel, … Hédan, *PLoS One* 21(7):e0345429, Jul 2026.
[10.1371/journal.pone.0345429](https://doi.org/10.1371/journal.pone.0345429) · PMID 42475297

38 dogs with disseminated HS; PTPN11 E76/G503 hotspots by high-sensitivity ddPCR on paired
abdominal and thoracic tumours. Divergent PTPN11 mutations directly observed in **3 of 28** dogs
with mutated tumour pairs; after correcting for hotspot-only detectability, the authors estimate
**24–45% of disseminated HS cases carry clonally independent PTPN11 mutations in distinct
tumours**. NGS and copy-number analysis of two cell lines from the same patient confirmed
independent clonal origin. Their conclusion: "this clonal diversity challenges the assumption that
DHS is predominantly metastatic."

**Why it matters here.** The repo's Move 2 (maintenance-at-emergence) rests on the claim that a
predisposed dog generates *new primaries*, not only metastases — so a genotype-matched maintenance
agent has a fresh, dividing, driver-matched target to kill. Until now that was a logical
consequence of the germline predisposition. It is now measured, in this disease, by the group that
owns the canine HS genomics. This is the single strongest external support the prevention framing
has received.

Repo status: the logic is present (`core/breed_wide_durability.py`, "the same lesion in the brain
tumour, in the lung tumour, and in the NEXT tumour") but cites nothing for independent clonality.
**Citation should be added.**

## 2. Frequency of the CFA11q16 CDKN2A/B+MTAP deletion — PARTIAL, and it exposes an internal contradiction

Hedan, … Breen, *BMC Cancer* 11:201, 2011.
[10.1186/1471-2407-11-201](https://doi.org/10.1186/1471-2407-11-201)

Deletion of CFA11q16 at ~44 Mb, which includes CDKN2A/B, in **62.8% of HS cases (60.7% of Bernese
Mountain Dogs, 66.7% of Flat-Coated Retrievers)**. MTAP is inside the deleted region but was **not
separately named or measured**, and no therapeutic implication of MTAP loss was discussed.

Repo status: `core/breed_wide_durability.py` already calls this lesion "THE MOST RECURRENT genomic
aberration in canine histiocytic sarcoma, across 104 histiocytic malignancy cases." The **62.8%
figure itself is new to the repo.**

**The contradiction it exposes.** Two modules label the MTAP tier a *"recurrent minority"*:
- `core/genotype_tiered_durability.py:11` — "MTAP / CDKN2A homozygous deletion — recurrent minority (CFA11q16)"
- `maintenance_durability.py:102` — `GenotypeTier("MTAP deleted", "recurrent minority", …)`

A region-level deletion rate of 62.8% is not a minority. Either the label is wrong or the two
modules disagree with `breed_wide_durability`. **Open correction; not applied.**

**Be careful about the inference.** 62.8% is the *region*, not MTAP protein loss. MTAP is co-deleted
with CDKN2A often but not universally. So 62.8% is an **upper bound** on the MTAP-null fraction, not
an estimate of it. The MTAP stain remains the falsifier — this finding raises the prior that the
stain comes back positive, it does not replace it.

## 3. MTAP immunohistochemistry is now a formally reviewed routine assay — NEW

Salzano, … Broggi, *Diagnostics* 16(13):2069, Jul 2026.
[10.3390/diagnostics16132069](https://doi.org/10.3390/diagnostics16132069) · PMID 42449850

Narrative review of MTAP IHC as a diagnostic and prognostic surrogate for CDKN2A/B homozygous
deletion, with an explicit framework for integrating it into routine surgical pathology workflows,
and a section on the PRMT5/MAT2A synthetic vulnerabilities that follow from MTAP deficiency.

**Why it matters here.** The deposit's headline ask is one MTAP stain on archived tissue. That ask
is now backed by a 2026 review treating the assay as standardized and routine, rather than
something a canine lab would have to develop. It lowers the cost and the perceived novelty risk of
the cheapest decisive experiment.

## 4. A canine HS cell line panel and a 1824-compound screen now exist — NEW

Sakuma, Tomiyasu, … Okuda, *Vet Comp Oncol* 24(3):554-567, May 2026.
[10.1111/vco.70077](https://doi.org/10.1111/vco.70077) · PMID 42129963

High-throughput screen of 1824 compounds across **10 canine HS cell lines**, previously
subclassified by expression profile into Group A and Group B. 73 compounds active across all lines
(5-FU median IC50 7.49 µM; sunitinib 608 nM). **Duvelisib** (PI3Kδ/γ) was selectively active in
Group A — median IC50 287 nM vs >5 µM in Group B and 7.46 µM in normal PBMC — reducing
phospho-Akt in all eight Group A lines, with cell-cycle arrest and cell death.

Two consequences:
1. **The falsifier experiment has a cheaper form than a stain on archived tissue.** Ten
   characterised canine HS lines exist. MTAP status and PRMT5-inhibitor sensitivity could be read
   out in vitro, with no new animals.
2. **Independent support for a PI3K/Akt-dependent subgroup** — the repo's PTEN tier. But note the
   differences honestly: the drug is duvelisib, not paxalisib, and the stratifier is an expression
   subclass, not PTEN status. It corroborates the axis, not the tier definition.

## 5. CNS delivery got worse, not better — NEW, and a correction

From the 2026 MTAP-targeting review ([PMC12733126](https://pmc.ncbi.nlm.nih.gov/articles/PMC12733126/))
and Tango disclosures:

- **TNG908 (ralometostat) failed in glioblastoma on insufficient CNS penetration** — roughly 60% of
  the projected CSF:plasma ratio. The repo lists TNG908 among MTAP-tier options; it should be
  demoted for the brain site.
- **TNG462 (vopimetostat) showed no GBM activity**: of 33 GBM patients, 23 treated at active doses
  with at least one assessment, **zero partial responses**, median time on study under 8 weeks.
  Non-CNS responses were modest — pancreatic 2/9, NSCLC 1/4, urothelial 1/1 (Oct 2025).
- **TNG456 is the remaining brain-penetrant candidate**: 55× selective for MTAP deletion, GI50
  20 nM, FDA **Orphan Drug Designation for malignant glioma**, Phase 1/2 enrolling, initial data
  expected 2026 — **and trialled in combination with abemaciclib**, which is the repo's own
  CDKN2A-deleted/RB1-intact tier drug. Two of our tiers are being combined in a real trial.

Net: the brain arm of the MTAP tier is **less** supported than the repo assumes. Two of three named
PRMT5 inhibitors have now failed or shown nothing in CNS disease, and the one that remains has no
efficacy data yet.

## 6. MAT2A now outperforms PRMT5 on reported response rate — PARTIAL

- **IDE397** (IDEAYA, MAT2A): 38% partial response in squamous NSCLC, 30% in urothelial; molecular
  responses in 81% of heavily pre-treated patients by first evaluation; median time to response
  2.7 months.
- **AMG 193** (PRMT5): ORR 21.4% across 80 patients and eight tumour types at 600–1200 mg, median
  duration of response 8.3 months, low myelosuppression.
- **AG-270/S095033** (MAT2A, first generation): 2 partial responses in 40 patients.
  [10.1038/s41467-024-55316-5](https://doi.org/10.1038/s41467-024-55316-5)

The repo's MTAP tier leads with PRMT5 and lists MAT2A as a "parallel MTAP-directed option." On
current clinical numbers that ordering is arguably inverted. **Open question; not applied.**

Also from the review: **dual PRMT5 + MAT2A inhibition shows "strong synthetic lethality in MTAP
homozygous-deficient glioma models"** — i.e. in the site the repo finds hardest.

## 7. An adverse finding for the immune floor tier — NEW

The same review reports that MTAP-deleted tumours have "cold" microenvironments with reduced T-cell
infiltration, attributed to MTA-mediated immunosuppression.

The repo's floor tier is "immune surveillance + cycled microtubule," used as the genotype-independent
backstop when nothing is targetable. This finding says that backstop is **weakest precisely in
MTAP-null tumours** — the tier the repo is most confident about. The two are not independent.
**Record as a known gap.**

## 8. Noted, not needle-moving

- **Folie et al.**, *Front Vet Sci* 13:1917708, Aug 2026
  ([10.3389/fvets.2026.1917708](https://doi.org/10.3389/fvets.2026.1917708) · PMID 42676415):
  CT features differ between periarticular and systemic HS pulmonary lesions, raising "the
  possibility of distinct biological subtypes." Relevant to the site axis if subtypes are real.
- **Di Pentima et al.**, *Vet Res Commun* 50(5), Jul 2026
  ([10.1007/s11259-026-11428-5](https://doi.org/10.1007/s11259-026-11428-5) · PMID 42517970):
  oncolytic BoHV4EGFPΔTK kills canine HS lines in vitro. **Oncolytic virotherapy is a modality class
  absent from the repo's catalogue** — per `CLAUDE.md` rule 9 it must be recorded as a candidate,
  either assessed or explicitly excluded with a reason. Currently neither.
- **Liquid biopsy in veterinary medicine**, *Int J Mol Sci* 27(18):8183, Sep 2026
  ([10.3390/ijms27188183](https://doi.org/10.3390/ijms27188183) · PMID 42794612): review; no new
  canine HS-specific ctDNA assay. MRD monitoring in dogs remains aspirational, which leaves the
  surveillance dependence where the repo already puts it.
- **PRMT5 in canine cells: still nothing.** PubMed `PRMT5 AND canine AND dog AND cells AND
  veterinary` returns one unrelated record. The core gap the deposit is built on is **still open**.

---

## Open corrections, none applied

Listed so a later thread does not mistake them for settled.

| # | Correction | Where | Basis |
|---|---|---|---|
| 1 | MTAP tier labelled "recurrent minority" contradicts "most recurrent aberration" elsewhere in the repo | `core/genotype_tiered_durability.py:11`, `maintenance_durability.py:102` | Hedan 2011, 62.8% region-level |
| 2 | TNG908 should be demoted for the brain site | MTAP tier drug list | TNG908 GBM failure on CNS penetration |
| 3 | PRMT5-before-MAT2A ordering may be inverted | MTAP tier maintenance string | IDE397 38%/30% PR vs AMG 193 ORR 21.4% |
| 4 | MTAP∩MAPK overlap resolved by priority, not combination | `best_tier_for()` | Knoll 2025 (see `PRIOR_ART_COMBINATIONS.md`) |
| 5 | Immune floor tier is not independent of the MTAP tier | floor tier rationale | MTA-mediated immune coldness |
| 6 | Oncolytic virotherapy not in the candidate catalogue | catalogue completeness | Di Pentima 2026; `CLAUDE.md` rule 9 |

## Net assessment

The needle moved **in favour of the premise and against the brain arm**.

- The prevention framing gained its first direct empirical support (independent clonal origin, item 1).
- The prior that an MTAP-null subset exists in canine HS rose sharply (62.8% region-level deletion, item 2).
- The cheapest decisive experiment got cheaper and better standardised (items 3 and 4).
- The brain arm got materially weaker: two of three named PRMT5 inhibitors have now failed in CNS
  disease (item 5).
- Nobody has still looked at MTAP in a canine tumour. The deposit's central claim stands.
