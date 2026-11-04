# Lab plan: the 29 experiments that decide the open candidates

**Case:** primary intracranial (non-disseminated) canine histiocytic sarcoma. Generated 2026-11-04 from
`candidate_universe.candidates()`. Each row is the single measurement recorded as deciding that class;
no literature search can supply it (`DECIDING_MEASUREMENT_SWEEP_2026_11_04` found none in print).

**Ordering:** (1) classes with a measurement in canine HS already; (2) those decided by an assay on the
canine HS cell lines that already exist (cheapest: one plate, no animal); (3) agents obtainable today
before near-future ones.

**Batch suggestion:** every tier-A/B row whose test is a cell-line IC50 can run as ONE dose-response
panel on the existing lines (DH82, CHS-3 and the rest of the ten-line panel), with CHS-3 as the TP53
wild-type control. Exposure ceilings to compare against are in each row (e.g. digoxin canine toxicity
~6 nM, PMID 35821778).

| # | tier | class | deciding measurement | obtainable |
|---|---|---|---|---|
| 1 | A canine-HS evidence | nuclear export inhibition (XPO1 / SINE compounds) | verdinexor IC50 in canine HS lines and a canine CSF:plasma at the labelled dose | exists today |
| 2 | A canine-HS evidence | proteasome inhibition | an IC50 in canine HS for a member with measured unbound brain exposure | exists today |
| 3 | A canine-HS evidence | cardiac glycosides / Na+,K+-ATPase inhibition | a digoxin IC50 in canine HS lines, compared with the canine therapeutic serum range | exists today |
| 4 | A canine-HS evidence | translation-elongation inhibition | omacetaxine IC50 in canine HS and its CSF:plasma | exists today |
| 5 | A canine-HS evidence | nitrogen-bisphosphonate chemosensitisation (free zoledronate) | zoledronate plus vincristine (the in-model partner) in canine HS lines, and zoledronate's CSF level | exists today |
| 6 | A canine-HS evidence | HSP90 inhibition | retaspimycin or ganetespib IC50 in canine HS lines (cells exist) | near future |
| 7 | A canine-HS evidence | survivin suppression (YM155 / sepantronium) | YM155 unbound brain or CSF exposure in any species, against its canine HS IC50 | near future |
| 8 | B cell-line assay | targeted protein degradation / cereblon modulators (immunomodulatory imides, CELMoDs) | pomalidomide IC50 in the ten canine HS lines, then a priced marrow burden replacing (not adding to) one of the two licensed marrow agents | exists today |
| 9 | B cell-line assay | glucocorticoid-receptor agonists (corticosteroids) | a prednisolone/dexamethasone IC50 in canine HS lines (cells exist; a trivial assay) | exists today |
| 10 | B cell-line assay | apoptosis induction / BH3 mimetics (BCL-2, BCL-XL) | BH3 profiling or a venetoclax IC50 in canine HS lines | exists today |
| 11 | B cell-line assay | polyamine-synthesis inhibition (ornithine decarboxylase) | eflornithine growth inhibition of canine HS lines at achievable concentration | exists today |
| 12 | B cell-line assay | acyclic nucleotide phosphonate prodrugs (rabacfosadine) | rabacfosadine (or PMEG) IC50 in canine HS lines and its CSF level in dogs | exists today |
| 13 | B cell-line assay | farnesyltransferase inhibition | lonafarnib or tipifarnib IC50 in canine HS lines, including PTPN11-mutant ones | exists today |
| 14 | B cell-line assay | JAK/STAT inhibition | ruxolitinib or oclacitinib IC50 in canine HS lines | exists today |
| 15 | B cell-line assay | arsenic trioxide | arsenic trioxide IC50 in canine HS lines | exists today |
| 16 | B cell-line assay | MDM2-p53 interaction inhibition | TP53 status of the case itself (digital PCR for the insertion plus sequencing), then an MDM2-inhibitor IC50 in p53-wild-type canine HS lines (CHS-3 is wild-type); combination use only | near future |
| 17 | B cell-line assay | ligand-toxin fusions / immunotoxins (catalytic protein toxins) | a CD204- or CD18-directed fusion toxin's IC50 in canine HS lines | near future |
| 18 | C other | interleukin-1 blockade as a tolerability enabler (not a tumour-kill modality) | rate of MAPK-inhibitor intolerance in dogs on maintenance, with and without IL-1 blockade | exists today |
| 19 | C other | photodynamic / sonodynamic therapy (energy-activated sensitiser) | 5-ALA or Ce6 fluorescence in a resected canine intracranial HS specimen | exists today |
| 20 | C other | anti-invasion / adhesion / chemokine-axis blockade (integrin, CXCR4) | CXCR4 expression in canine intracranial HS | exists today |
| 21 | C other | amino-acid-depleting enzymes (L-asparaginase) | asparagine synthetase expression in canine HS | exists today |
| 22 | C other | inflammatory-cytokine blockade (TNF, IL-6) | effect of TNF blockade on canine HS growth in a macrophage co-culture | exists today |
| 23 | C other | RANKL inhibition | RANK expression in canine HS | exists today |
| 24 | C other | alteration-matched agents gated on lesions not reported in canine HS (ALK/NTRK/RET fusions, IDH1) | a fusion / IDH1 panel on canine HS (the tumour's own sequencing) | exists today |
| 25 | C other | nucleic-acid therapeutics (antisense oligonucleotide, siRNA) | an intrathecally deliverable anti-survivin oligonucleotide's knockdown in canine HS in vivo | near future |
| 26 | C other | high-Z nanoparticle radioenhancement | NBTXR3 retention and dose enhancement in an intracranial tumour in any species | near future |
| 27 | C other | tumour-treating fields (alternating electric fields) | field-intensity modelling or measurement for a transducer array on a canine skull | near future |
| 28 | C other | targeted radionuclide therapy / radioconjugates | uptake of a CD204/CD18-directed radioconjugate in canine HS | near future |
| 29 | C other | boron neutron capture therapy | BPA tumour:normal-brain uptake ratio in canine intracranial HS (FBPA-PET) | near future |

A result in either direction settles the row: an IC50 above the achievable exposure is a rule-13
KILL_CONTRADICTED or TOXICITY_UNAFFORDABLE ground; one below it moves the class toward IN_MODEL,
subject to the toxicity ledger.
