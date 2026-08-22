# Therapy strategy for primary intracranial histiocytic sarcoma in the predisposed breed

### The best evidence-supported design, its honest coverage grade, and the protocol that would make coverage *backed*

> **This is an analysis, not veterinary advice.** No agent in this strategy has been given to a
> dog with this disease. Every treatment decision belongs with clinicians who can examine the
> animal.

## Honest status in one line

A therapy *designed* to cover all sites, mechanisms, and escapes for this presentation exists and
is specified below. Whether it *does* cover them is, today, a **structural / hypothesis-level**
claim, not an evidence-backed result: of the twelve escape routes the model closes, **1** rests on
a measurement in canine HS, **2** on transfers from another disease, **2** on mechanism/design
arguments, and **7** on assumed, never-measured kill rates. This document states the design, grades
every line, and gives the prioritized experiments that would move each line from *assumed* to
*measured*. Producing an evidence-backed "covers everything" without those experiments would
require inventing the missing numbers, which this project does not do.

## The disease, scoped

- **Occupied sites (CNS):** invaded brain parenchyma (23/23 dogs, no clean edge) and
  leptomeninges/CSF (~52% CSF-positive). A discrete resectable "lump" is **ruled out**.
- **Co-equal presentation:** pulmonary / disseminated form, same germline MTAP/CDKN2A lesion,
  systemically accessible.
- **Drivers:** germline MTAP/CDKN2A deletion (recurrent across ~104 HS cases) plus a somatic MAPK
  majority (PTPN11/SHP2 and KRAS, ~43–64% across cohorts).

## The recommended therapy (design)

**Move 1 — Induction (same for every dog, ~4–6 months).** A brain-penetrant microtubule agent
(mitotic poison; the load-bearing agent) plus three supporting agents: paxalisib (PI3K/AKT,
non-substrate of P-gp/BCRP), liposomal clodronate (macrophage-lineage depletion), and anti-PD-1
(gilvetmab). Delivered systemically/orally — no catheter, no efflux co-dose, no osmotic disruption.

**Move 2 — Genotype-matched maintenance (indefinite).** A single targeted pill keyed to the
tumour's driver, lethal only to cells carrying the lesion:

| Genotype | Maintenance | Durability grade (design) |
| --- | --- | --- |
| MTAP deleted | PRMT5 inhibitor (MTA-cooperative; TNG908/TNG462) | strongest — genotype-locked |
| PTEN deleted | PI3K inhibitor (paxalisib) | strong dependency |
| CDKN2A deleted, RB1 intact | CDK4/6 inhibitor (abemaciclib) | strong dependency |
| SHP2/KRAS driver (~59%) | MEK inhibitor (mirdametinib, CNS-penetrant) | medium — surveillance-dependent |
| none targetable | immune surveillance + cycled chemotherapy | floor — monitored |

**Delivery to the CNS.** Systemic at favourable access; for the parenchyma a resection-cavity
drug-eluting implant / convection-enhanced delivery removes the penetration bottleneck by
construction; the fluid-borne remainder is addressed by craniospinal radiation + intrathecal
dosing + the immune arm (no durability number computed for that compartment, by design).

## Coverage by evidence tier (from `canine_dsp.coverage_assessment`)

| # | Escape | Axis | Closing agent in the design | Evidence grade |
| --- | --- | --- | --- | --- |
| 1 | MAPK reactivation above the block | pathway | radiation / microtubule cytotoxic / PRMT5i | ASSUMED |
| 2 | MEK target-site mutation | pathway | radiation / microtubule cytotoxic / PRMT5i | ASSUMED |
| 3 | Activating ERK lesion | pathway | downstream / position-independent agents | ASSUMED |
| 4 | RTK bypass into PI3K/AKT | pathway | paxalisib | MEASURED (other disease) |
| 5 | CSF1R / lineage independence | lineage | liposomal clodronate | ASSUMED |
| 6 | Antigen loss (MHC-I intact) | immune | radiation + cytotoxic + anti-PD-1 | ASSUMED |
| 7 | NF-κB independence | pathway | parthenolide / DMAPT | **MEASURED (canine HS)** |
| 8 | Ferroptosis resistance | metabolic | lipophilic statin | ASSUMED (possibly counter-indicated) |
| 9 | Autophagy independence | metabolic | hydroxychloroquine | MEASURED (other disease) |
| 10 | Drug-tolerant persister | dormancy | continuous/metronomic schedule | STRUCTURAL |
| 11 | MGMT repair | DNA repair | drop the alkylator class (use a mitotic poison) | STRUCTURAL |
| 12 | Germline second primary | germline | PRMT5i maintenance (synthetic-lethal on MTAP) | ASSUMED (conditional) |

**Target-side transfer is no longer an assumption.** The kinase targets are essentially identical
dog-to-human — ERK2/MAPK1 **100.0%**, PI3Kα **99.81%** (ATP-binding domain 100%) — computed from
real UniProt sequences in `canine_dsp.sequence_conservation`. Only P-gp/ABCB1, at **91.08%** (the
efflux transporter that gates CNS delivery), remains a target where conservation does not license
transfer, so canine penetration must be measured.

## The validation protocol — how coverage becomes *backed*

Prioritized cheapest / most decisive first. Each converts one or more graded lines from *assumed*
toward *measured*.

1. **MTAP immunohistochemistry stain on archived tumour tissue.** *Settles escape 12 and the entire
   ten-year arm.* No live dog; archived tissue + matched normal. If MTAP-intact, the synthetic-lethal
   maintenance does nothing and durability collapses to the induction-only answer. **Do this first.**
2. **Tumour growth rate from imaging already taken.** The 0.055/day placeholder sets the pass/fail
   bar for *every* escape; it likely reads off serial scans already in the record. No new procedure.
3. **Microtubule-agent kill rate in canine HS cells** (IC50 → Emax in a standard cytotoxicity assay).
   *Settles escapes 1–3 and 11* — the load-bearing induction agent.
4. **PI3K/AKT-inhibitor IC50 in canine HS lines.** *Upgrades escape 4* from a hemangiosarcoma transfer.
5. **11-line ERK-inhibitor panel** (PRJDB17594), stratified by NF-κB cluster. *Settles the contested
   premise behind escapes 3/7* — does ERK activation actually predict response.
6. **Liposomal clodronate cytotoxicity vs canine HS cells** (*escape 5*), **ferroptosis sensitivity
   / GPX4-FSP1 axis** (*escape 8* — may show it is counter-indicated), **autophagy/HCQ dependence**
   (*escape 9*).
7. **Canine CNS penetration (Kp,uu) of the chosen PRMT5 inhibitor.** The runner-up ten-year
   falsifier: below ~0.37 the maintenance arm fails.
8. **Anti-PD-1 (or other immune-effector) response in canine HS** (*escape 6*).

The current measured benchmark for this disease is a **~44-day** median under definitive therapy;
the structurally-matched durability comparator (lomustine after debulking in localized HS) is
**568 days / 37.5% relapse-free** (n=16). The strategy's claim is that the biology **permits**
durable multi-site control — the gap to a *prognosis* is exactly the protocol above.

## What blocks going further right now

Live literature grounding (PubMed / ChEMBL) to pull real measured IC50/PK values into the graded
lines requires interactive connector approval that this session cannot perform. With those
connectors approved, several *assumed* lines can be upgraded to *measured (with citation)* without
any new wet-lab work — the target-level potencies for these drug classes are published.
