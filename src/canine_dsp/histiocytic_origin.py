"""Inferring a candidate driver landscape for Pembroke Welsh Corgi primary CNS / primary pulmonary
histiocytic sarcoma from clinical phenotype, cross-species genetics, and structural signal
analysis. WHY THIS MODULE EXISTS ---------------------- `mapk_scenarios` models Corgi primary
intracranial HS (PIHS) and localized pulmonary HS as PTPN11/KRAS-driven, and has always flagged
that premise as its single largest unverified assumption. See docs/HS_MAPK_RESISTANCE.md.
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
                           "macrophage compartments are prenatally seeded, locally "
                           "self-renewing, and bone-marrow-independent.",
}

HUMAN_HISTIOCYTOSIS_DRIVERS = {
    "why_cross_species": "Human Langerhans cell histiocytosis (LCH) and Erdheim-Chester disease "
                         "are the closest well-sequenced counterparts to canine HS by lineage "
                         "(mononuclear phagocyte system).",
    "braf_v600e_fraction_lch": "0.40-0.70 across cohorts; 0.45 and 0.32 in two specific series",
    "map2k1_fraction_lch": "0.275 (and 0.175 in a second series), mutually exclusive with BRAF",
    "mutual_exclusivity_note": "BRAF and MAP2K1 mutations being mutually exclusive is itself "
                               "evidence that a single MAPK activation event is the driving lesion "
                               "rather than one of several cooperating hits",
    "cell_of_origin_model": "BRAFV600E or mutant MAP2K1 in human CD34+ HSPCs is sufficient to "
                           "generate LCH-like disease (PMC7556147); lesion in a stem/progenitor "
                           "cell yields multisystem disease, in a tissue-restricted precursor "
                           "yields localized single-system disease",
    "conspicuous_absence": "BRAF V600E is the single most common human histiocytosis driver but "
                           "is essentially absent from published canine HS series, which report "
                           "PTPN11 and KRAS instead.",
}

MTAP_CDKN2A_LOCUS = {
    "citation": "Shearin AL, et al. The MTAP-CDKN2A locus confers susceptibility to a naturally "
               "occurring canine cancer. Cancer Epidemiol Biomarkers Prev 2012;21(7):1019, "
               "PMID 22623710",
    "finding": "GWAS in 474 Bernese Mountain Dogs localized the major HS susceptibility locus to "
              "CFA11 (max association p=1.11e-13), narrowing to a 75 kb region spanning MTAP "
              "through the last exon of CDKN2A",
    "breed_caveat": "This is a BMD germline susceptibility locus.",
    "therapeutic_implication": "CDKN2A encodes p16INK4a, the endogenous brake on CDK4/6.",
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
                  "2019, Genes 10(7):505: E76K 32%, G503V 10%; 3/13 = 23% of golden retrievers).",
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
                  "disease, yet is essentially absent from canine HS reports.",
        hotspots={600: "V"},
        druggable_by="vemurafenib/dabrafenib (mutation-specific); MEK inhibitor downstream",
    ),
    DriverCandidate(
        gene="MAP2K1", tier="B: dominant in human histiocytosis, untested in canine HS",
        rationale="MEK1; mutated in ~27.5% of human LCH and mutually exclusive with BRAF, i.e. "
                  "it is the main alternative route to the same pathway output.",
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
        rationale="The prediction that distinguishes this hypothesis from a generic MAPK story.",
        hotspots={},  # no single established activating hotspot; interrogate the whole kinase domain
        lineage_link="defining survival dependency of both implicated tissue-resident compartments",
        druggable_by="pexidartinib -- FDA-approved 2019 for tenosynovial giant cell tumour (itself "
                    "a CSF1-driven histiocytic/giant-cell proliferation), CSF1R IC50 ~20 nM, oral, "
                    "and blood-brain-barrier penetrant, which directly addresses the ~15% brain "
                    "penetration ceiling recorded for trametinib in BRAIN_PENETRATION_FRACTION",
    ),
    DriverCandidate(
        gene="CSF1", tier="C: predicted by the tissue-resident macrophage hypothesis",
        rationale="Ligand side of the same axis: a CSF1 structural rearrangement would be missed "
                 "entirely by hotspot sequencing of CSF1R and needs its own assay.",
        hotspots={},
        lineage_link="ligand for the receptor above; the transforming lesion in a real, "
                    "drug-validated human histiocytic proliferation",
        druggable_by="pexidartinib (blocks the receptor regardless of which side is altered)",
    ),
    DriverCandidate(
        gene="CDKN2A", tier="D: germline susceptibility locus, somatic status unknown",
        rationale="The BMD HS GWAS peak narrows to a 75 kb MTAP-CDKN2A window (Shearin et al. "
                  "2012).",
        hotspots={},
        druggable_by="CDK4/6 inhibitor (palbociclib/ribociclib/abemaciclib class) -- the drug "
                    "mapk_scenarios already models as its second agent",
    ),
    DriverCandidate(
        gene="MTAP", tier="D: germline susceptibility locus, somatic status unknown",
        rationale="Co-implicated with CDKN2A in the same 75 kb GWAS window and frequently "
                  "co-deleted with it.",
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
    raises confidence only in the context of what surrounds it, which is exactly a second-order
    (pairwise lag interaction) effect.
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
    """Is the mean salience at `positions` (1-based) higher than at randomly chosen positions? An
    empirical one-sided p-value against a null that resamples the same number of valid positions
    uniformly. With only a handful of known hotspots this has very low power -- a non-significant
    result here is weak evidence of absence, and a significant one on n=4 is a hypothesis worth
    pursuing rather than an established method.
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
