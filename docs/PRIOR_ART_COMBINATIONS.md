# Prior art: which of our proposed combinations have actually been tried

Scope: the drug *combinations* this repo proposes, checked against PubMed (Sep 2026).
Question answered here is narrow — **has someone already run this pairing, and in what species?**
It is not a review of the underlying single-agent biology, which is covered in
`CONSOLIDATED_REPORT.md`.

Verdict in one line: **every drug-drug combination we propose has been tested in human cell
lines and mouse models. None has been tested in dogs, and none has been tested as
maintenance.**

---

## Tried — and it worked

### PRMT5 inhibitor + MAPK-pathway inhibitor (MEK / KRAS / ERK / RAF)

Knoll et al., *Cancer Research* 85(18):3518-3539, Sep 2025.
[10.1158/0008-5472.CAN-25-1464](https://doi.org/10.1158/0008-5472.CAN-25-1464) · PMID 40694540

CRISPR paralog/single-gene screen against MTAP-deleted cancers ± MTA-cooperative PRMT5
inhibitors. Loss of MAPK-pathway members sensitised cells to PRMT5 inhibition; chemical
KRAS, MEK, ERK and RAF inhibitors synergised with PRMT5i to kill CDKN2A/MTAP-null,
RAS-active tumours. PRMT5i + KRAS or RAF inhibitor gave **complete responses in vivo**.
Resistance to KRAS inhibition did not confer resistance to PRMT5i, or vice versa.

This is **stronger than what this repo proposes**. Our MTAP tier treats MEK as a *second
line on acquired resistance*; this paper uses the MAPK inhibitor as an *up-front partner*.

### PRMT5-inhibitor resistance confers collateral MEK sensitivity

Fu et al., *Biomolecules* 16(8):1198, Aug 2026.
[10.3390/biom16081198](https://doi.org/10.3390/biom16081198) · PMID 42650864
Preprint: [10.64898/2026.04.16.719008](https://doi.org/10.64898/2026.04.16.719008) · PMID 42079286

MTAP-null NSCLC lines made resistant to BMS-986504/MRTX1719. Resistance was *not* explained
by restored PRMT5 activity or changed MTA levels; it came with cross-resistance to
mechanistically distinct PRMT5 inhibitors, rewired MAPK transcriptional programs, and
reproducible sensitivity to MEK inhibitors.

This is the evidence behind our "genotype-anchored, not locked" correction and the defined
MEK second line. The claim is backed by data, not inference.

### MAT2A inhibitor + PRMT5 inhibitor

Yu et al., *MedComm* 5(10):e705, Sep 2024.
[10.1002/mco2.705](https://doi.org/10.1002/mco2.705) · PMID 39309689

SCR-7952 (selective MAT2A inhibitor) showed marked synergy with SAM-competitive **and**
MTA-cooperative PRMT5 inhibitors in MTAP-deleted tumours, via aggravated PRMT5 inhibition
and FANCA splicing perturbation.

**Caveat this repo does not currently carry:** the synergy did **not** extend to
substrate-competitive PRMT5 inhibitors. The PRMT5i class matters for this pairing.

Foundational MAT2A synthetic-lethality work: Kalev et al., *Cancer Cell* 39(2):209-224, 2021.
[10.1016/j.ccell.2020.12.010](https://doi.org/10.1016/j.ccell.2020.12.010) · PMID 33450196
(also proposes AG-270 + antimitotic taxanes).

---

## Not tried

### Any MTAP-directed work in dogs

PubMed `MTAP AND canine AND tumor` returns two records, neither reporting MTAP status in a
canine tumour. The nearest is Meek et al., *Genes* 13(10):1693, 2022
([10.3390/genes13101693](https://doi.org/10.3390/genes13101693) · PMID 36292578), which
identified a hypomorphic **FANCG** variant near the CFA11 locus in Bernese Mountain Dogs and
concluded the variant is "neither necessary nor sufficient for the development of HS."

### MTAP / CDKN2A deletion frequency in canine histiocytic sarcoma

PubMed `canine AND histiocytic sarcoma AND CDKN2A AND MTAP AND deletion AND copy number`:
**zero results.** This is the gap the deposit is built on, and it is still open.

### PRMT5 inhibition as adjuvant, maintenance, or MRD-directed prevention

PubMed `PRMT5 inhibitor AND adjuvant AND maintenance AND minimal residual disease AND
prevention`: **zero results**, in any species. Every trial of this class is in measurable,
established disease. The maintenance-at-emergence framing is untested everywhere.

---

## Known divergence between this repo's model and the human data

`core.genotype_tiered_durability.best_tier_for()` resolves a tumour carrying **both** an MTAP
deletion and a MAPK driver by priority — MTAP wins, MAPK is ignored. Knoll et al. (above)
indicates that is the wrong resolution: MTAP-null **and** RAS-active is exactly the population
where the *combination* produced complete responses.

This matters more in canine HS than in human cancer, because ~59% of canine HS carries a MAPK
driver (PTPN11/SHP2 ~56% + KRAS ~3%). An MTAP-null canine HS is therefore *likely* also
MAPK-driven — so the overlap is probably the typical MTAP-null tumour in this disease, not an
edge case.

**Deliberately not acted on.** Recorded here rather than patched into the model, so the
divergence is visible rather than silently resolved. Changing `best_tier_for()` to a
combination rule for the MTAP∩MAPK overlap would change the durability outputs and is a
separate decision.

---

*All records retrieved from PubMed, September 2026. Searches are reproducible from the query
strings quoted above.*
