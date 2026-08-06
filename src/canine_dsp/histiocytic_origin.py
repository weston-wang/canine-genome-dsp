"""Inferring a candidate driver landscape for Pembroke Welsh Corgi primary CNS / primary pulmonary
histiocytic sarcoma from clinical phenotype, cross-species genetics, and structural signal analysis.

WHY THIS MODULE EXISTS
----------------------
`mapk_scenarios` models Corgi primary intracranial HS (PIHS) and localized pulmonary HS as
PTPN11/KRAS-driven, and has always flagged that premise as its single largest unverified
assumption. Searching for Corgi-specific sequencing data confirms the gap is real rather than an
oversight: the paper that *defines* the Corgi pulmonary entity (Nakamura et al. 2015, PMID
26155931, 19 Pembroke Welsh Corgis) is purely histopathologic and predates the canine HS
MAPK-mutation literature; the largest canine HS sequencing cohort found (Takada et al. 2024, PMC
11353564, 129 HS + 26 HHS) contains exactly one Welsh corgi, pooled into an undifferentiated
"other breeds" bucket with no per-case or per-anatomic-site breakdown. No study stratifies canine
HS mutations by anatomic site at all.

So the mutation cannot be looked up. It can, however, be *reasoned toward* -- and that reasoning
is what this module encodes, along with the structural analyses that test parts of it. This is
explicitly hypothesis generation to prioritize what to sequence first, not a claim about what the
answer is.

THE INFERENCE CHAIN
-------------------
Observation (1): the Corgi tumors are Iba-1 positive (Nakamura et al. 2015). Iba-1 (AIF1) marks
macrophage/microglial lineage, not Langerhans-cell or interdigitating-dendritic-cell lineage.

Observation (2): they are HLA-DR (MHC class II) positive -- professional antigen-presenting cells,
consistent with the mononuclear phagocyte system.

Observation (3): the disease is anatomically *localized* -- focal/multifocal lung +/- regional
lymph node, or CNS-restricted for PIHS -- rather than the disseminated splenic/hepatic/nodal
pattern that dominates Bernese Mountain Dog HS.

Observation (4): median survival 133 days with no significant prognostic factor identified among
gender, age, lesion multiplicity, nodal involvement, resection status, or chemotherapy -- an
aggressive tumor whose behavior is not obviously modified by the usual clinical variables.

Observation (5): the presentation is breed-restricted, in a closed-population breed -- consistent
with a shared germline susceptibility haplotype, as was directly demonstrated for BMD HS
(MTAP_CDKN2A_LOCUS below).

The load-bearing step is (1) + (3) together. Iba-1 positivity places the cell of origin in the
macrophage lineage, and the two anatomic sites where this disease appears in Corgis -- lung and
brain -- are precisely the two mammalian tissues whose macrophage compartments (alveolar
macrophages and microglia) are seeded prenatally from yolk-sac-derived erythro-myeloid
progenitors, self-renew locally in situ, and are maintained largely or entirely independently of
bone-marrow output in adults (Gomez Perdiguero et al. 2015, Nature, PMID 25470051; both
populations are Csf1r+ by origin). Microglia and Langerhans cells are only marginally replaced by
circulating cells over a mouse lifetime; alveolar macrophages somewhat more so with age.

That yields a specific, mechanistically coherent hypothesis, stated as
TISSUE_RESIDENT_MACROPHAGE_HYPOTHESIS below: Corgi HS may be a neoplasm *of a tissue-resident,
prenatally-seeded, self-renewing macrophage compartment*, and it stays localized because its cell
of origin does not circulate -- not because it was caught early. BMD disseminated HS, by contrast,
behaves like a disease of a bone-marrow-derived, circulating monocyte/DC precursor.

This is not a novel form of argument: it is the same cell-of-origin logic established for human
Langerhans cell histiocytosis, where MAPK activation in a hematopoietic stem/progenitor cell
produces multisystem disease while the same lesion in a tissue-restricted precursor produces
localized single-system disease (the "misguided myeloid differentiation" model; BRAFV600E in human
CD34+ HSPCs is sufficient to generate LCH-like disease, PMC7556147).

WHAT THE HYPOTHESIS PREDICTS, AND WHY IT MATTERS THERAPEUTICALLY
---------------------------------------------------------------
If the cell of origin is a tissue-resident macrophage rather than a marrow-derived precursor, then
CSF1R moves from "not considered" to a leading candidate: CSF1R is the master survival and
maintenance receptor for exactly these two compartments (CSF1R inhibition depletes essentially all
microglia in healthy animals), whereas it is not the defining dependency of a circulating
monocyte-DC precursor in the same way. That prediction is *anatomically specific* -- it explains
the lung/CNS restriction rather than merely tolerating it.

It also carries a therapeutic consequence distinct from anything currently in `mapk_scenarios`,
which models its second agent as a mechanism-agnostic CDK4/6 inhibitor. A CSF1R-dependent
tissue-resident-macrophage neoplasm would instead be matched by a CSF1R inhibitor -- and
pexidartinib is real, FDA-approved (2019, for tenosynovial giant cell tumour, itself a
CSF1-driven histiocytic/giant-cell proliferation), orally bioavailable, potent on CSF1R
(IC50 ~20 nM), and blood-brain-barrier penetrant. BBB penetration is not incidental here: it is
the exact axis on which `mapk_scenarios.BRAIN_PENETRATION_FRACTION` records trametinib reaching
only ~15% of plasma concentration in brain, the single worst structural problem facing the primary
CNS scenario. A brain-penetrant agent whose target is the lineage's own survival receptor is a
better-matched second drug for PIHS than an illustrative CDK4/6 inhibitor, if the hypothesis holds.

Separately, the MTAP-CDKN2A susceptibility locus (verified below) supplies the *first real genetic
rationale* for the CDK4/6 inhibitor this module's sibling already models: CDKN2A encodes p16INK4a,
whose loss releases CDK4/6, which is the canonical setting for CDK4/6-inhibitor sensitivity. That
connection was not the reason CDK4/6i was chosen in `mapk_scenarios` (it was chosen as a
deliberately mechanism-agnostic second node), so this is retrospective support, not circularity --
but it does mean the second drug is less arbitrary than it was labeled.

WHAT IS ACTUALLY TESTED HERE VS. ASSERTED
-----------------------------------------
Asserted (with verified citations, but still an argument): the ontogeny reasoning and the candidate
ranking.

Tested computationally: (a) whether each candidate gene has a dog ortholog at all and how
conserved it is; (b) whether each human hotspot residue is actually present at the aligned dog
position -- a candidate whose hotspot residue differs in dog is a weaker candidate on chemistry
grounds, independent of any clinical argument; (c) whether a nonlinear (second-order Volterra)
model of structural confidence from local sequence physicochemistry assigns known histiocytosis
hotspots unusually large residuals, validated against a permutation null, and if so, what it
nominates in candidates with no established hotspot. (c) is exploratory and reported honestly
including when it fails; see `hotspot_salience` for its stated limitations.
"""

from dataclasses import dataclass

import numpy as np

# Kyte & Doolittle (1982) hydropathy index -- the standard, uncontroversial per-residue
# physicochemical scale. Used as the input signal for the nonlinear structural model below;
# nothing here depends on any disputed sequence-to-property mapping.
AA_HYDROPATHY = {
    "A": 1.8, "R": -4.5, "N": -3.5, "D": -3.5, "C": 2.5, "Q": -3.5, "E": -3.5, "G": -0.4,
    "H": -3.2, "I": 4.5, "L": 3.8, "K": -3.9, "M": 1.9, "F": 2.8, "P": -1.6, "S": -0.8,
    "T": -0.7, "W": -0.9, "Y": -1.3, "V": 4.2,
}

CORGI_CLINICAL_FEATURES = {
    "citation": "Nakamura K, et al. Localized pulmonary histiocytic sarcomas in Pembroke Welsh "
               "Corgis. J Vet Med Sci / (see PMID 26155931), 19 dogs",
    "anatomic_pattern": "focal or multiple masses in lung, regional lymph nodes, or both -- "
                        "localized, not the disseminated splenic/hepatic pattern of BMD HS",
    "immunophenotype": ["HLA-DR positive (MHC class II -- professional antigen-presenting cell)",
                        "Iba-1 positive (AIF1 -- macrophage/microglial lineage marker)"],
    "histology": "pleomorphic histiocytic cells combined with various inflammatory cells",
    "median_survival_days": 133,
    "prognostic_factors_found": None,
    "prognostic_factors_tested": ["gender", "age", "single vs multiple lesions",
                                  "lymph node involvement at diagnosis", "surgical resection status",
                                  "additional chemotherapy"],
    "molecular_data_in_source": "none -- this paper is histopathologic/immunohistochemical only "
                                "and predates the canine HS MAPK-mutation literature",
}

TISSUE_RESIDENT_MACROPHAGE_ONTOGENY = {
    "citation": "Gomez Perdiguero E, et al. Tissue-resident macrophages originate from "
               "yolk-sac-derived erythro-myeloid progenitors. Nature 2015, PMID 25470051",
    "finding": "Adult microglia (brain), alveolar macrophages (lung), Kupffer cells (liver) and "
              "Langerhans cells (epidermis) derive from Tie2+/Csf1r+ yolk-sac erythro-myeloid "
              "progenitors distinct from HSCs, self-renew in situ, and are maintained largely "
              "independently of circulating monocyte input in adulthood (microglia and Langerhans "
              "cells only marginally replaced over a mouse lifetime; alveolar macrophages more so "
              "with age)",
    "why_it_matters_here": "Corgi HS presents in exactly two sites -- lung and CNS -- whose "
                          "macrophage compartments are prenatally seeded, locally self-renewing, "
                          "and bone-marrow-independent. Iba-1 positivity places the tumor in that "
                          "lineage. A neoplasm arising in a non-circulating compartment would be "
                          "expected to stay anatomically confined, which is what is observed.",
}

HUMAN_HISTIOCYTOSIS_DRIVERS = {
    "why_cross_species": "Human Langerhans cell histiocytosis (LCH) and Erdheim-Chester disease "
                        "are the closest well-sequenced counterparts to canine HS by lineage "
                        "(mononuclear phagocyte system). Their driver landscape is far better "
                        "characterized than canine HS's and is almost entirely MAPK-pathway.",
    "braf_v600e_fraction_lch": "0.40-0.70 across cohorts; 0.45 and 0.32 in two specific series",
    "map2k1_fraction_lch": "0.275 (and 0.175 in a second series), mutually exclusive with BRAF",
    "mutual_exclusivity_note": "BRAF and MAP2K1 mutations being mutually exclusive is itself "
                               "evidence that a single MAPK activation event is the driving lesion "
                               "rather than one of several cooperating hits",
    "cell_of_origin_model": "BRAFV600E or mutant MAP2K1 in human CD34+ HSPCs is sufficient to "
                           "generate LCH-like disease (PMC7556147); lesion in a stem/progenitor "
                           "cell yields multisystem disease, in a tissue-restricted precursor "
                           "yields localized single-system disease",
    "conspicuous_absence": "BRAF V600E is the single most common human histiocytosis driver but is "
                          "essentially absent from published canine HS series, which report "
                          "PTPN11 and KRAS instead. Either canine HS genuinely differs at this "
                          "node, or BRAF has not been adequately sequenced in the right canine "
                          "cases -- an open question this module treats as a testable candidate "
                          "rather than a settled difference.",
}

MTAP_CDKN2A_LOCUS = {
    "citation": "Shearin AL, et al. The MTAP-CDKN2A locus confers susceptibility to a naturally "
               "occurring canine cancer. Cancer Epidemiol Biomarkers Prev 2012;21(7):1019, "
               "PMID 22623710",
    "finding": "GWAS in 474 Bernese Mountain Dogs localized the major HS susceptibility locus to "
              "CFA11 (max association p=1.11e-13), narrowing to a 75 kb region spanning MTAP "
              "through the last exon of CDKN2A",
    "breed_caveat": "This is a BMD germline susceptibility locus. Whether Pembroke Welsh Corgis "
                   "share it is unknown -- no Corgi GWAS for this disease was found. A shared "
                   "locus would argue the two presentations are variants of one disease; a "
                   "different locus would argue they are distinct entities that happen to share a "
                   "name and a lineage.",
    "therapeutic_implication": "CDKN2A encodes p16INK4a, the endogenous brake on CDK4/6. Loss of "
                              "that brake is the canonical setting for CDK4/6-inhibitor "
                              "sensitivity -- supplying a real genetic rationale for the CDK4/6 "
                              "inhibitor that mapk_scenarios models purely as a "
                              "mechanism-agnostic second node. Retrospective support for that "
                              "drug choice, not the reason it was made.",
}


@dataclass(frozen=True)
class DriverCandidate:
    """One candidate driver gene, with its rationale and any established human hotspot residues.

    `hotspots` maps 1-based human residue position -> expected wild-type single-letter residue, so
    the conservation check can verify the position actually carries that residue in the human
    structure before asking whether dog matches (catching stale or mis-transcribed literature
    positions rather than trusting them).
    """
    gene: str
    tier: str
    rationale: str
    hotspots: dict[int, str]
    lineage_link: str | None = None
    druggable_by: str | None = None


# Tiers encode *why* a gene is a candidate, which is the actual output of the reasoning above --
# not a confidence score. Tier C is the part that follows specifically from the tissue-resident
# macrophage hypothesis and would not appear on a conventional canine-HS candidate list.
CANDIDATE_DRIVERS = [
    DriverCandidate(
        gene="PTPN11", tier="A: precedented in canine HS",
        rationale="Most frequent published canine HS lesion (41/96 = 43% of BMD in Takada et al. "
                 "2019, Genes 10(7):505: E76K 32%, G503V 10%; 3/13 = 23% of golden retrievers). "
                 "Zero Corgi-specific and zero anatomic-site-stratified data exists.",
        hotspots={76: "E", 503: "G"},
        lineage_link="SHP2 is required for CSF1R/M-CSF signal transduction, so a PTPN11 gain-of-"
                    "function lesion sits directly on the tissue-resident macrophage survival axis "
                    "-- compatible with the hypothesis rather than an alternative to it",
        druggable_by="MEK inhibitor (trametinib, cobimetinib) downstream; allosteric SHP2 "
                    "inhibitors exist in human trials but none is canine-approved",
    ),
    DriverCandidate(
        gene="KRAS", tier="A: precedented in canine HS",
        rationale="Q61H reported in 3/96 (3.1%) of BMD HS (Takada et al. 2019) and 0/13 golden "
                 "retrievers. Low frequency, but a definitive MAPK activator when present.",
        hotspots={61: "Q"},
        druggable_by="MEK inhibitor downstream; Q61 is not addressable by the G12C-specific "
                    "covalent inhibitors",
    ),
    DriverCandidate(
        gene="BRAF", tier="B: dominant in human histiocytosis, untested in canine HS",
        rationale="V600E is the most common driver of human LCH (40-70%) and Erdheim-Chester "
                 "disease, yet is essentially absent from canine HS reports. Highest-value "
                 "single residue to sequence in a Corgi case precisely because its absence in "
                 "dogs may reflect ascertainment rather than biology.",
        hotspots={600: "V"},
        druggable_by="vemurafenib/dabrafenib (mutation-specific); MEK inhibitor downstream",
    ),
    DriverCandidate(
        gene="MAP2K1", tier="B: dominant in human histiocytosis, untested in canine HS",
        rationale="MEK1; mutated in ~27.5% of human LCH and mutually exclusive with BRAF, i.e. it "
                 "is the main alternative route to the same pathway output. If canine HS lacks "
                 "BRAF, MAP2K1 is the next node to interrogate.",
        hotspots={56: "Q", 57: "K", 121: "C"},
        druggable_by="MEK inhibitor -- but note class-III/allosteric-site MAP2K1 mutations can "
                    "confer resistance to some MEK inhibitors, so this candidate is not simply "
                    "'also treatable with trametinib'",
    ),
    DriverCandidate(
        gene="NRAS", tier="B: dominant in human histiocytosis, untested in canine HS",
        rationale="Recurrent in human histiocytic neoplasms; the RAS paralog most often mutated in "
                 "myeloid lineages, and canine HS RAS screening has focused on KRAS.",
        hotspots={61: "Q"},
        druggable_by="MEK inhibitor downstream",
    ),
    DriverCandidate(
        gene="CSF1R", tier="C: predicted by the tissue-resident macrophage hypothesis",
        rationale="The prediction that distinguishes this hypothesis from a generic MAPK story. "
                 "CSF1R is the master survival/maintenance receptor for microglia and alveolar "
                 "macrophages specifically -- the two compartments matching the two anatomic sites "
                 "where Corgi HS occurs. CSF1R inhibition depletes essentially all microglia in "
                 "healthy animals, establishing the dependency is absolute rather than modulatory. "
                 "No canine HS study found has sequenced CSF1R.",
        hotspots={},  # no single established activating hotspot; interrogate the whole kinase domain
        lineage_link="defining survival dependency of both implicated tissue-resident compartments",
        druggable_by="pexidartinib -- FDA-approved 2019 for tenosynovial giant cell tumour (itself "
                    "a CSF1-driven histiocytic/giant-cell proliferation), CSF1R IC50 ~20 nM, oral, "
                    "and blood-brain-barrier penetrant, which directly addresses the ~15% brain "
                    "penetration ceiling recorded for trametinib in BRAIN_PENETRATION_FRACTION",
    ),
    DriverCandidate(
        gene="CSF1", tier="C: predicted by the tissue-resident macrophage hypothesis",
        rationale="Ligand side of the same axis. CSF1 overexpression (usually by translocation) "
                 "drives tenosynovial giant cell tumour, showing that this axis can transform a "
                 "histiocytic population via the ligand rather than the receptor -- so a CSF1 "
                 "structural rearrangement would be missed entirely by hotspot sequencing of "
                 "CSF1R and needs its own assay.",
        hotspots={},
        lineage_link="ligand for the receptor above; the transforming lesion in a real, "
                    "drug-validated human histiocytic proliferation",
        druggable_by="pexidartinib (blocks the receptor regardless of which side is altered)",
    ),
    DriverCandidate(
        gene="CDKN2A", tier="D: germline susceptibility locus, somatic status unknown",
        rationale="The BMD HS GWAS peak narrows to a 75 kb MTAP-CDKN2A window (Shearin et al. "
                 "2012). Whether Corgis share the locus is unknown. Included because it is the "
                 "one real canine HS genetic finding that is not a MAPK hotspot, and because it "
                 "would explain CDK4/6-inhibitor sensitivity mechanistically.",
        hotspots={},
        druggable_by="CDK4/6 inhibitor (palbociclib/ribociclib/abemaciclib class) -- the drug "
                    "mapk_scenarios already models as its second agent",
    ),
    DriverCandidate(
        gene="MTAP", tier="D: germline susceptibility locus, somatic status unknown",
        rationale="Co-implicated with CDKN2A in the same 75 kb GWAS window and frequently "
                 "co-deleted with it. MTAP loss is separately actionable (PRMT5/MAT2A synthetic "
                 "lethality) so distinguishing MTAP from CDKN2A involvement is not academic.",
        hotspots={},
        druggable_by="PRMT5 or MAT2A inhibitors exploit MTAP deletion by synthetic lethality; "
                    "none canine-approved",
    ),
]

# The positive-control set for the nonlinear structural analysis: hotspots whose gene, residue
# number, and wild-type identity were each verified against a primary source in building this
# module. Deliberately excludes MAP2K1/NRAS positions (recalled, not verified here) so the
# validation set contains no position this module is not confident about -- a small, clean control
# set is more informative than a larger one with soft members.
VERIFIED_HOTSPOT_CONTROLS = {"PTPN11": {76: "E", 503: "G"}, "KRAS": {61: "Q"}, "BRAF": {600: "V"}}


def hydropathy_track(sequence: str) -> np.ndarray:
    """Per-residue Kyte-Doolittle hydropathy; unknown residues map to 0 (scale midpoint-ish).

    This is the *input* signal for the nonlinear structural model -- a purely local, per-residue
    physicochemical property carrying no structural or evolutionary information, which is what
    makes it a meaningful predictor to test against a structure-derived output.
    """
    return np.array([AA_HYDROPATHY.get(residue, 0.0) for residue in sequence], dtype=float)


def hotspot_salience(plddt: np.ndarray, sequence: str, memory: int = 11, n_basis: int = 4,
                     alpha: float = 0.01) -> np.ndarray:
    """Per-residue |residual| from a second-order Volterra model predicting structural confidence
    (pLDDT) from local sequence hydropathy. Higher = structure less explained by local chemistry.

    The rationale, and the reason a *nonlinear* model is the right tool: pLDDT is high in
    well-packed, locally-determined structure and low in disordered or conformationally ambivalent
    regions, and that relationship to local hydrophobicity is not linear -- a hydrophobic stretch
    raises confidence only in the context of what surrounds it, which is exactly a
    second-order (pairwise lag interaction) effect. Fitting the quadratic Volterra kernel absorbs
    the part of the structural signal that *is* predictable from local chemistry; what remains in
    the residual is structure whose confidence is set by something non-local -- long-range packing,
    an autoinhibitory interface, an allosteric contact. Known kinase/phosphatase hotspots
    frequently sit at exactly such positions (PTPN11 E76 is at the N-SH2/PTP autoinhibitory
    interface; BRAF V600 is in the activation-segment/P-loop regulatory contact).

    Reuses `volterra.volterra_design`/`fit_volterra` unchanged -- the same basis-reduced,
    elastic-net-regularized machinery validated for genomic tracks, with the protein treated as a
    single group so lag histories never leak across a sequence boundary.

    LIMITATIONS, stated rather than buried: this is exploratory. It is a within-protein relative
    ranking, not a calibrated pathogenicity score; it is fit on one protein at a time with no
    held-out data; and it can only nominate positions whose structural confidence is anomalous,
    which is neither necessary nor sufficient for a residue to be an oncogenic hotspot. Whether it
    carries real signal at all is tested by `permutation_pvalue` against a null of random
    positions, and reported honestly including when the answer is no.
    """
    from .volterra import fit_volterra, predict, volterra_design

    plddt = np.asarray(plddt, dtype=float)
    hydropathy = hydropathy_track(sequence)
    n = min(len(plddt), len(hydropathy))
    if n <= memory:
        raise ValueError(f"sequence of length {n} is too short for memory={memory}")
    plddt, hydropathy = plddt[:n], hydropathy[:n]

    groups = np.zeros(n, dtype=int)  # one protein == one group; no cross-boundary lag leakage
    design, names, valid = volterra_design(
        hydropathy.reshape(-1, 1), groups, ["hydropathy"], memory=memory, n_basis=n_basis, order=2)
    from .volterra import dct_lag_basis
    fit = fit_volterra(design[valid], plddt[valid], names, dct_lag_basis(memory, n_basis),
                       ["hydropathy"], order=2, family="gaussian", alpha=alpha)
    residual = np.full(n, np.nan)
    residual[valid] = np.abs(plddt[valid] - predict(fit, design[valid]))
    return residual


def permutation_pvalue(salience: np.ndarray, positions: list[int], n_permutations: int = 10_000,
                       seed: int = 7) -> dict:
    """Is the mean salience at `positions` (1-based) higher than at randomly chosen positions?

    An empirical one-sided p-value against a null that resamples the same number of valid
    positions uniformly. With only a handful of known hotspots this has very low power -- a
    non-significant result here is weak evidence of absence, and a significant one on n=4 is a
    hypothesis worth pursuing rather than an established method. Both readings are reported.
    """
    salience = np.asarray(salience, dtype=float)
    valid = np.flatnonzero(~np.isnan(salience))
    indices = np.array([p - 1 for p in positions if 0 <= p - 1 < len(salience)])
    indices = np.array([i for i in indices if not np.isnan(salience[i])], dtype=int)
    if indices.size == 0:
        return {"n_positions_scored": 0, "observed_mean_salience": None, "p_value": None,
                "note": "no supplied position was inside the scored region"}
    observed = float(salience[indices].mean())
    rng = np.random.default_rng(seed)
    draws = np.array([salience[rng.choice(valid, indices.size, replace=False)].mean()
                      for _ in range(n_permutations)])
    p_value = float((np.sum(draws >= observed) + 1) / (n_permutations + 1))
    return {
        "n_positions_scored": int(indices.size),
        "observed_mean_salience": observed,
        "null_mean_salience": float(draws.mean()),
        "null_sd": float(draws.std()),
        "p_value": p_value,
        "permutations": n_permutations,
        "interpretation": ("hotspots score higher than chance in this protein"
                          if p_value < 0.05 else
                          "no evidence hotspots score higher than chance in this protein"),
        "power_caveat": f"n={int(indices.size)} scored position(s); this test has very low power, "
                        "so a null result is weak evidence of absence and a significant result is "
                        "a lead, not a validated method",
    }
