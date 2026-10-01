# HS branch status

Settled results and known gaps for the histiocytic sarcoma work, so a later thread does not
re-derive or re-litigate them. Written per `CLAUDE.md` rules 1, 4, 5 and 7.

**The case under analysis:** primary intracranial (non-disseminated) histiocytic sarcoma in a
predisposed breed — an extra-axial, meninges-based mass that invades brain tissue (23/23 dogs) and
the leptomeninges (19/19), with extracranial spread never reported (`CONSOLIDATED_REPORT.md`, "Where
the disease is"). Evidence from *disseminated* HS is labelled **indirect** below.

Labels: **NEW** (not in the record), **PARTIAL** (the record has the source or the claim, not this
detail), **ALREADY COVERED** (with where). Checked by DOI/PMID against `docs/` and `src/`, not by
keyword.

---

## A. The brain arm for the deletion-carrying tumour: CDK4/6 now holds up better than PRMT5 (Oct 2026)

### What weakened

The brain arm of the MTAP tier relied on a brain-penetrant MTA-cooperative PRMT5 inhibitor. As of
October 2026:

| Agent | Brain evidence | Status in record |
|---|---|---|
| TNG908 | Failed to reach therapeutic CNS exposure in glioblastoma | ALREADY COVERED (`pkpd.py`, 2026-08-23); CNS anchor moved to TNG456 |
| TNG462 (vopimetostat) | Glioblastoma: 23 evaluable patients at active doses, **0 partial responses**, median time on study < 8 weeks (Tango, Oct 2025) | **NEW.** `core/breed_wide_durability.py:255` still calls TNG462 "designed brain-penetrant" |
| TNG456 | No human efficacy data yet (expected 2026). Mouse U87MG: 84% growth inhibition at 30 mg/kg BID, 56% regression at 90 mg/kg BID. Phase 1/2 NCT06810544, **alone and with abemaciclib**. [J Med Chem](https://doi.org/10.1021/acs.jmedchem.6c00035) | PARTIAL (named as CNS anchor; trial design and mouse numbers new) |
| MAT2A inhibitors | **No brain-penetrant MAT2A inhibitor published.** PubMed `brain-penetrant MAT2A inhibitor MTAP-deleted glioblastoma`: 0 records | NEW |

So there is **no MTAP-directed drug with human evidence of activity in the brain.** The PRMT5 brain
arm is a promise pending TNG456.

### What holds up: hit the same deletion through CDKN2A, with abemaciclib

The CFA11q16 deletion removes CDKN2A as well as MTAP. Losing CDKN2A (p16) makes the cell depend on
CDK4/6 — a dependency an approved, oral, brain-reaching drug already blocks. Abemaciclib is in the
repo as the CDKN2A/RB1-intact tier agent (`core/genotype_tiered_durability.py:126`), but its brain
claim was graded "class effect; canine data absent" (`core/toxicity.py:331`). The evidence for each
link:

| Link | Evidence | Grade |
|---|---|---|
| Target present in this disease | CFA11q16 deletion including CDKN2A/B in **62.8%** of canine HS (60.7% BMD, 66.7% FCR). Hédan 2011 [10.1186/1471-2407-11-201](https://doi.org/10.1186/1471-2407-11-201) | MEASURED, canine HS (PARTIAL: paper already in report refs; figure not used) |
| Rb intact, p16 down | CDKN2A down and **Rb preserved in every canine histiocytic line**, including lines from **localized HS**. Hirabayashi 2022 [10.1111/vco.12812](https://doi.org/10.1111/vco.12812) | MEASURED, canine HS (ALREADY COVERED) |
| Canine HS cells respond to the class | Palbociclib inhibited growth of **all** lines, including localized-HS lines, and a xenograft. Same paper | MEASURED, class (ALREADY COVERED) |
| Abemaciclib acts on canine cancer cells | G1 arrest, growth suppression in 5 canine melanoma lines + xenograft (Kim 2025 [10.3389/fvets.2025.1603686](https://doi.org/10.3389/fvets.2025.1603686)); canine lymphoma lines, p16-low most sensitive, high p16 = resistance (Maylina 2022 [10.1292/jvms.22-0498](https://doi.org/10.1292/jvms.22-0498)) | MEASURED in canine cells, other tumours. Abemaciclib on canine HS itself: **TRANSFERRED** (same class, same target, Rb intact) — NEW |
| Reaches a brain tumour | Resected human brain-metastasis tissue: unbound active abemaciclib **96× CDK4 IC50, 19× CDK6 IC50**. Tolaney 2020 [10.1158/1078-0432.CCR-20-1764](https://doi.org/10.1158/1078-0432.CCR-20-1764) | MEASURED in humans; TRANSFERRED to dog — NEW |
| Holds tumours in the same anatomical place | Alliance A071401: progressive grade 2/3 **meningioma** (dura-based, extra-axial — the same niche as the breed's tumour) with NF2 or CDK-pathway loss. **PFS6 58% (14/24), met primary endpoint**; best response stable disease 16/24; well tolerated. Brastianos 2026, *Nat Med* [10.1038/s41591-025-04141-4](https://doi.org/10.1038/s41591-025-04141-4) | MEASURED in humans — NEW |
| Can be dosed for years | Approved, oral, continuous; human adjuvant use runs 2 years. Dogs: repeat-dose toxicology to 3 months, target organs marrow, GI, lymphoid, male reproductive (FDA NDA 208716 review). Canine exposure numbers not extracted (file exceeds fetch limit) | MEASURED (human, dog tox); canine exposure **not yet in hand** — NEW |

### Limits, at the strength shown

1. **It holds; it does not shrink.** Cytostatic: the meningioma trial's best response was stable
   disease. That is the job of maintenance (stop a new clone growing), not induction. Division-gated.
2. **The barrier still pumps it out.** Abemaciclib is a P-gp/BCRP substrate: oral unbound
   brain:plasma (Kp,uu) **0.03 in mice, 0.11 in rats**, yet it extended survival in orthotopic
   glioma at those exposures (Raub 2015 [10.1124/dmd.114.062745](https://doi.org/10.1124/dmd.114.062745));
   knocking out both pumps raises brain penetration 25× (Martínez-Chávez 2021
   [10.1016/j.phrs.2021.105954](https://doi.org/10.1016/j.phrs.2021.105954)). The extra-axial mass
   sits largely outside the intact barrier, which is what the meningioma data speaks to. Tumour cells
   that have **invaded behind an intact barrier**, and the CSF, may see much less — the same gap the
   report already assigns to local delivery, radiation and intrathecal dosing. This does not close it.
3. **Per-tumour gates.** Needs Rb intact and p16 lost — two stains, the same kind of cheap test as the
   MTAP stain.
4. **Not a lock.** CDK4/6-inhibitor resistance is well documented in humans; this arm is
   surveillance-grade, like MEK. (The MTAP arm was itself already downgraded to "anchored, not locked".)
5. **Backups exist but are preclinical.** GLR2007, a CDK4/6 inhibitor designed for the brain:
   Kp,uu 0.23 in mice, 95.9% growth inhibition in orthotopic glioblastoma
   ([PMC9403987](https://pmc.ncbi.nlm.nih.gov/articles/PMC9403987/)); no clinical results found.
   Lerociclib (G1T38): 28 days of continuous dosing in beagles without severe neutropenia
   ([10.18632/oncotarget.16216](https://doi.org/10.18632/oncotarget.16216)) — relevant to dosing for years.

### Net

For the deletion-carrying brain tumour, **every link of the CDK4/6 arm has a human or canine
measurement except two transfers** (abemaciclib potency on canine HS; brain exposure in the dog).
The PRMT5 arm has none in the brain. Lead the brain arm with abemaciclib now; add TNG456 on the same
deletion if it reads out — its own trial already pairs the two.

---

## B. September 2026 sweep — relabelled after a record check

| # | Finding | Label | Note |
|---|---|---|---|
| 1 | Disseminated HS often clonally independent (24–45%). Mottier 2026 [10.1371/journal.pone.0345429](https://doi.org/10.1371/journal.pone.0345429) | **ALREADY COVERED** (`CONSOLIDATED_REPORT.md` finding 4, since 2026-09-02) | Disseminated-case evidence: **indirect** for this case. Earlier version of this file wrongly called it new |
| 2 | CDKN2A/B region deleted in 62.8% of canine HS. Hédan 2011 | PARTIAL | Paper in report refs; figure not used; contradicts "minority" labels |
| 3 | MTAP IHC formally reviewed as a routine surrogate. Salzano 2026 [10.3390/diagnostics16132069](https://doi.org/10.3390/diagnostics16132069) | NEW | De-risks the MTAP stain |
| 4 | 10 canine HS lines + 1824-compound screen; duvelisib. Sakuma 2026 [10.1111/vco.70077](https://doi.org/10.1111/vco.70077) | **ALREADY COVERED** (report, "Also noted"; `v2/engine.py`) | The in-vitro falsifier route it enables is the new point |
| 5 | TNG908 CNS failure | **ALREADY COVERED** (`pkpd.py`) | |
| 5b | TNG462: 0 PRs in 23 evaluable GBM patients | NEW | See section A |
| 6 | MAT2A outperforms PRMT5 on response rate (IDE397 38%/30% PR; AMG 193 ORR 21.4%) | NEW | Systemic sites only; no brain data |
| 7 | MTAP-deleted tumours are immunologically cold (MTA-mediated) | NEW | Weakens the immune floor exactly where the MTAP tier applies |
| 8 | Oncolytic BoHV4 on canine HS lines. Di Pentima 2026 [10.1007/s11259-026-11428-5](https://doi.org/10.1007/s11259-026-11428-5) | **ALREADY COVERED** (report, "Also noted") | Mentioned, not assessed in the catalogue (rule 9) |
| 9 | CT subtypes periarticular vs systemic HS. Folie 2026 [10.3389/fvets.2026.1917708](https://doi.org/10.3389/fvets.2026.1917708) | NEW | Not relevant to the intracranial case |
| 10 | Liquid-biopsy review. [10.3390/ijms27188183](https://doi.org/10.3390/ijms27188183) | NEW | No canine HS assay; surveillance dependence unchanged |
| 11 | PRMT5 inhibitors in canine cells | Still **zero** records | The deposit's central gap is still open |

---

## Open corrections, none applied

| # | Correction | Where | Basis |
|---|---|---|---|
| 1 | CDKN2A and MTAP tiers labelled "minority"; the CDKN2A/B region is deleted in 62.8% | `core/genotype_tiered_durability.py:11,126`, `maintenance_durability.py:102` | Hédan 2011 |
| 2 | ~~Demote TNG908 for the brain~~ | `pkpd.py` | **Already applied 2026-08-23**; the dict key is still named `"tng908"` |
| 3 | TNG462 called "designed brain-penetrant" | `core/breed_wide_durability.py:255` | 0 PRs in 23 evaluable GBM patients |
| 4 | Brain arm for the deletion should lead with abemaciclib (CDK4/6), PRMT5 as the pending upgrade; abemaciclib's brain claim should cite measured exposure, not "class effect" | MTAP/CDKN2A tiers; `core/toxicity.py:331` | Section A |
| 5 | PRMT5-before-MAT2A ordering may be inverted (systemic sites) | MTAP tier maintenance string | IDE397 vs AMG 193 |
| 6 | MTAP∩MAPK overlap resolved by priority, not combination | `best_tier_for()` | Knoll 2025 (`PRIOR_ART_COMBINATIONS.md`) |
| 7 | Immune floor tier not independent of the MTAP tier | floor tier rationale | MTA-mediated immune coldness |
| 8 | Oncolytic virotherapy mentioned but not assessed | catalogue | `CLAUDE.md` rule 9 |
