"""Treating one sequenced dog, not a cohort: what tumor sequencing actually resolves, and what it
cannot. WHY THIS MODULE EXISTS ---------------------- Every Monte Carlo function in this repo
answers a *population* question: run 500 trials that differ in parameters, exposure, and initial
clonal composition, and report the fraction achieving durable response. That number is a cohort
average. See docs/HS_MAPK_RESISTANCE.md.
"""

import numpy as np

# Mass of one diploid canine genome equivalent, used to convert a required molecule count into a
# required DNA input. 6.6 pg is the standard figure for a ~3 Gb diploid mammalian genome.
GENOME_EQUIVALENT_PG = 6.6

# Real, published detection limits, expressed as the assay's floor in variant allele fraction.
# These are floors on *what fraction of molecules must carry the variant to call it*, and they are
# the numbers that decide whether a negative sequencing result is informative.
SEQUENCING_ASSAYS = {
    "standard_hybrid_capture": {
        "vaf_lod": 0.02,
        "description": "conventional targeted NGS panel without molecular barcoding",
        "citation": "PMC6126605 (rare-event detection review): standard NGS is limited to variants "
                   "above ~0.02 VAF, because uncorrected polymerase/sequencing error sets the floor",
        "clinically_available_for_dogs": True,
    },
    "umi_clinical": {
        "vaf_lod": 0.01,
        "description": "UMI/barcoded panel at a validated clinical operating point",
        "citation": "PMC5915090 (EGFR T790M liquid-biopsy assay validation): UMI-based assay "
                   "limit of detection 1% VAF at 95.8% sensitivity, vs. 5% for the non-UMI arm",
        "clinically_available_for_dogs": True,
    },
    "umi_best_case": {
        "vaf_lod": 0.001,
        "description": "UMI/barcoded panel at its published best case with ample input DNA",
        "citation": "PMC6126605: UMI error-correction reaches ~0.001 VAF starting from 50 ng DNA",
        "clinically_available_for_dogs": False,
    },
    "ddpcr_known_variant": {
        "vaf_lod": 0.001,
        "description": "droplet digital PCR, one pre-specified variant per assay",
        "citation": "PMC6126605: ddPCR detects point mutations at frequencies <=0.1%",
        "clinically_available_for_dogs": False,
        "caveat": "one known variant per assay -- cannot discover an unanticipated resistance "
                 "mechanism, only confirm or exclude a specific pre-named one",
    },
    "qbda": {
        "vaf_lod": 1e-4,
        "description": "quantitative blocker displacement amplification",
        "citation": "Nat Commun 2021 (doi:10.1038/s41467-021-26308-6): quantitation below 0.01% "
                   "VAF at 23,000x depth",
        "clinically_available_for_dogs": False,
    },
    "duplex_research_best": {
        "vaf_lod": 3.1e-5,
        "description": "duplex (double-strand consensus) sequencing, best published sensitivity",
        "citation": "duplex sequencing report of 100% detection down to 0.0031% VAF at mean 3128x",
        "clinically_available_for_dogs": False,
        "caveat": "a research-grade result on a favorable target, not a validated assay; treated "
                 "here as an optimistic upper bound on what sequencing could ever deliver",
    },
}

# Real driver frequencies in canine histiocytic sarcoma. This is the distribution the N=1 question
# is conditioned on, and the reason sequencing matters more for drug *choice* than for resistance.
CANINE_HS_DRIVER_FREQUENCY = {
    "citation": "Takada et al. 2019, Genes 10(7):505 -- targeted sequencing of canine HS",
    "cohort": "96 Bernese mountain dogs, 13 golden retrievers",
    "bmd": {
        "PTPN11": 41 / 96,          # E76K 32%, G503V 10%
        "KRAS": 3 / 96,             # Q61H
    },
    "golden_retriever": {"PTPN11": 3 / 13},
    "mapk_activating_any_bmd": 44 / 96,
    "no_identified_mapk_driver_bmd": 1 - 44 / 96,
    "note": "PTPN11 and KRAS were counted as mutually exclusive in this cohort's reporting, so "
            "the union is taken as their sum.",
    "breed_scope": "Bernese mountain dog and golden retriever ONLY.",
}

# The matched comparator this repo did not previously have. Unlike COMBI-d/v (rejected in
# mapk_scenarios for stacking four mismatches), this study matches on every axis that matters:
# species (dog), disease (histiocytic sarcoma), presentation (localized), and treatment STRUCTURE
# (aggressive local therapy -- i.e. the modeled debulking step -- followed by adjuvant systemic
# therapy). It is therefore a legitimate scale reference for a debulked-plus-systemic HS model.
LOCALIZED_HS_CCNU_BENCHMARK = {
    "citation": "Skorupski et al. 2009, Vet Comp Oncol 7:139-144, PMID 19453368 -- long-term "
               "survival in dogs with localized HS treated with CCNU as adjuvant to local therapy",
    "n_dogs": 16,
    "median_survival_days": 568,
    "median_disease_free_interval_days": 243,
    "n_relapsed": 10,               # 2 local recurrence, 8 distant metastasis
    "median_time_to_relapse_days": 201,
    "relapse_free_fraction": 6 / 16,
    "matches_on": ["species: dog", "disease: histiocytic sarcoma", "presentation: localized",
                   "structure: local therapy (debulking) + adjuvant systemic drug"],
    "mismatches_on": ["systemic agent is a DNA-alkylating cytotoxic (lomustine), not a MAPK-pathway "
                     "inhibitor -- so this bounds the *structure*, not the modeled drug mechanism",
                     "no molecular stratification: driver status was not sequenced, so this mixes "
                     "MAPK-driven and non-MAPK-driven tumors"],
    "caveat": "n=16, single-arm, retrospective. Breed composition was not reported -- HS in the "
              "referral-hospital population this drew from skews toward BMD/flat-coated "
              "retriever/rottweiler, not this breed, so treat this as matched on "
              "species/disease/structure but UNRESOLVED on breed, same as "
              "CANINE_HS_DRIVER_FREQUENCY.",
}

# The genuinely breed-matched comparator for an unsequenced-breed patient -- and it tells a materially
# different, worse story than LOCALIZED_HS_CCNU_BENCHMARK above, which is why the two must never
# be conflated. This is the same case series `localized_pulmonary_scenarios` in mapk_scenarios.py
# already models: unlike Skorupski's cohort, this one reports regional nodal involvement in many
# cases, meaning debulking cannot be assumed to reach all disease (a structural mismatch, not just
# a numeric one) and survival is roughly a quarter as long.
LOCALIZED_PULMONARY_HS_BENCHMARK = {
    "citation": "Sakai et al. 2015, J Vet Med Sci 77(12):1667-1670, PMID 26155931 -- localized "
               "localized pulmonary histiocytic sarcoma",
    "n_dogs": 19,
    "breed": "single breed (all 19)",
    "median_survival_days": 133,
    "nodal_involvement": "reported in many cases, no precise rate published",
    "prognostic_factors_significant": "none reached statistical significance (including surgical "
                                      "resection status) -- likely underpowered, not evidence "
                                      "those factors don't matter",
    "matches_on": ["species: dog", "breed: this presentation", "disease: histiocytic sarcoma",
                  "anatomic presentation: primary lung"],
    "mismatches_on": ["treatment: mixed/unspecified across the cohort, not a single systemic "
                     "agent -- so this cannot isolate a drug effect the way the CCNU benchmark can",
                     "structure: regional nodal involvement in many cases means the debulking-"
                     "reaches-everything premise this repo's single-compartment scenarios lean on "
                     "does not hold here -- see run_monte_carlo_two_compartment"],
    "caveat": "n=19, retrospective, no molecular data (driver status unknown in every dog).",
}


def vaf_lod_to_cell_fraction(vaf_lod: float, mutant_copies: int = 1, ploidy: int = 2) -> float:
    """Convert an assay's variant-allele-fraction floor into a floor on *tumor cell fraction*. The
    resistance model's `preexisting_prob` machinery works in cell fractions; assays report VAF.
    For a heterozygous SNV in a diploid genome, one of two alleles carries the variant, so VAF =
    cell_fraction * mutant_copies / ploidy and the cell-fraction floor is *twice* the VAF floor.
    """
    if not 0 < vaf_lod < 1:
        raise ValueError("vaf_lod must lie in (0, 1)")
    if mutant_copies <= 0 or ploidy <= 0:
        raise ValueError("mutant_copies and ploidy must be positive")
    return float(vaf_lod * ploidy / mutant_copies)


def detectable_prior_mass(lod_cell_fraction: float, log10_low: float = -6.0,
                          log10_high: float = -3.0) -> float:
    """Fraction of the model's own pre-existing-subclone size prior that lies above an assay floor.
    `sample_initial_state` draws the resistant fraction log-uniformly over [10**log10_low,
    10**log10_high], so the answer is a ratio of log-widths, not of linear widths -- which matters
    a great deal here: linear reasoning would suggest an assay at 1e-4 sees almost the whole
    range, when in log terms it sees only a third of it.
    """
    if lod_cell_fraction <= 0:
        return 1.0
    if log10_high <= log10_low:
        raise ValueError("log10_high must exceed log10_low")
    lod_log10 = np.log10(lod_cell_fraction)
    if lod_log10 >= log10_high:
        return 0.0
    if lod_log10 <= log10_low:
        return 1.0
    return float((log10_high - lod_log10) / (log10_high - log10_low))


def posterior_preexisting_prob(prior: float, lod_cell_fraction: float, log10_low: float = -6.0,
                               log10_high: float = -3.0) -> dict:
    """Bayesian update of `preexisting_prob` after sequencing finds *no* resistance variant. A
    negative result does not set the probability to zero, because the assay can only exclude the
    part of the size prior it can actually see. With prior `p` that a subclone exists and
    detectable prior mass `d`: P(exists | not detected) = p(1-d) / [p(1-d) + (1-p)] The (1-p) term
    carries no factor of d because a tumor with no subclone at all also produces a negative result
    -- that is precisely why a negative test is weak evidence when d is small.
    """
    if not 0 <= prior <= 1:
        raise ValueError("prior must lie in [0, 1]")
    detectable = detectable_prior_mass(lod_cell_fraction, log10_low, log10_high)
    undetectable_existing = prior * (1 - detectable)
    denominator = undetectable_existing + (1 - prior)
    posterior = 0.0 if denominator <= 0 else undetectable_existing / denominator
    return {
        "prior": float(prior),
        "lod_cell_fraction": float(lod_cell_fraction),
        "detectable_prior_mass": detectable,
        "posterior": float(posterior),
        "fold_reduction": float(prior / posterior) if posterior > 0 else float("inf"),
        "interpretation": (
            "a negative result excludes nothing: the assay floor sits above every subclone size "
            "the model considers possible" if detectable <= 0 else
            f"a negative result rules out the largest {detectable:.0%} (in log-size terms) of "
            f"possible subclones, moving the probability from {prior:.2f} to {posterior:.2f}"),
    }


def genome_equivalents_required(cell_fraction: float, confidence: float = 0.95,
                                mutant_copies: int = 1, ploidy: int = 2) -> dict:
    """Input-material floor: how many genome equivalents must be sampled to see such a subclone.
    Independent of, and logically prior to, assay chemistry -- if the variant molecule is not in
    the tube, no error-correction scheme recovers it. Sampling is Poisson in the number of mutant
    molecules, so requiring at least one with probability `confidence` needs n >= -ln(1 -
    confidence) / (cell_fraction * mutant_copies / ploidy) Reported alongside the DNA mass,
    because that is the number that says whether a real specimen could ever suffice.
    """
    if not 0 < cell_fraction <= 1:
        raise ValueError("cell_fraction must lie in (0, 1]")
    if not 0 < confidence < 1:
        raise ValueError("confidence must lie in (0, 1)")
    variant_molecule_fraction = cell_fraction * mutant_copies / ploidy
    n = -np.log(1 - confidence) / variant_molecule_fraction
    return {"cell_fraction": float(cell_fraction), "confidence": float(confidence),
            "genome_equivalents": float(n),
            "dna_input_ug": float(n * GENOME_EQUIVALENT_PG / 1e6)}


def spatial_detection_probability(subclone_cell_fraction: float, tumor_cells: float,
                                 sampled_cells: float) -> dict:
    """The limit no sequencing depth fixes: is the subclone in the piece of tumor you took? Assay
    sensitivity and spatial sampling are different failure modes and are worth reporting
    separately. A subclone present at 1e-6 of a 1e9-cell tumor is ~1000 cells; if it arose as a
    single focal expansion rather than being uniformly dispersed, a needle core or a fragment of a
    resection may contain none of it, and the sequencing result is negative for reasons that have
    nothing to do with the machine.
    """
    for name, value in (("tumor_cells", tumor_cells), ("sampled_cells", sampled_cells)):
        if value <= 0:
            raise ValueError(f"{name} must be positive")
    if not 0 < subclone_cell_fraction <= 1:
        raise ValueError("subclone_cell_fraction must lie in (0, 1]")
    if sampled_cells > tumor_cells:
        raise ValueError("sampled_cells cannot exceed tumor_cells")
    subclone_cells = subclone_cell_fraction * tumor_cells
    sampled_fraction = sampled_cells / tumor_cells
    return {
        "subclone_cells": float(subclone_cells),
        "sampled_fraction_of_tumor": float(sampled_fraction),
        "probability_if_well_mixed": float(1 - np.exp(-subclone_cells * sampled_fraction)),
        "probability_if_single_focus": float(sampled_fraction),
    }


#  Breeds Takada et al. 2019 actually sequenced -- the only ones with a real driver-frequency base
# rate. Every other breed string (flat_coated_retriever's own real data is a GWAS germline locus,
# a different thing entirely; unsequenced breeds have no published HS driver sequencing at all; anything else is
# simply unmeasured) gets the explicit "no data" branch below, generically -- not a this presentation special
# case, since the flat-coated-retriever tumor-scenario preset makes exactly the same mistake
# possible if this were hardcoded to only two named outcomes.
_SEQUENCED_DRIVER_FREQUENCY_BREEDS = {"bmd", "golden_retriever"}


def driver_conditioned_arms(breed: str = "bmd",
                            driver_frequency: dict = CANINE_HS_DRIVER_FREQUENCY) -> dict:
    """The swing sequencing *does* resolve: is a MAPK-pathway inhibitor on-target for this patient?
    `breed` matters here in a way it does not for the rest of this module, because the answer is
    not "apply the same discount everywhere" -- it is a different epistemic situation depending on
    whether this breed was in Takada et al.
    """
    if breed not in _SEQUENCED_DRIVER_FREQUENCY_BREEDS:
        return {
            "breed": breed,
            "source": f"no published canine HS driver sequencing exists for {breed!r}",
            "probability_mapk_driver_identified": None,
            "probability_no_mapk_driver_identified": None,
            "detectability": "Unchanged in principle -- a driver lesion, if present, would still "
                             "sit at ~25-50% VAF, orders of magnitude above every assay floor.",
            "on_target_arm": "N/A -- sequencing here is discovery, not confirmation of a known split",
            "off_target_arm": "N/A",
            "why_this_dominates": "For a sequenced breed, sequencing converts a known base rate "
                                  "into a fact for this dog.",
            "do_not_borrow_bmd_frequency": f"Applying 44/96 (BMD) to {breed!r} is a category error, "
                                          "not a conservative estimate, unless that breed's own "
                                          "clinical presentation and natural history are shown to "
                                          "match BMD's -- for this presentation specifically, they are shown "
                                          "NOT to (see LOCALIZED_PULMONARY_HS_BENCHMARK: 133-day median "
                                          "survival vs. 568 days in the BMD-context benchmark).",
        }
    on_target = float(driver_frequency[breed]["PTPN11"] + driver_frequency[breed].get("KRAS", 0.0)) \
        if breed == "golden_retriever" else float(driver_frequency["mapk_activating_any_bmd"])
    cohort_n = 96 if breed == "bmd" else 13
    return {
        "breed": breed,
        "source": driver_frequency["citation"],
        "cohort_n": cohort_n,
        "probability_mapk_driver_identified": on_target,
        "probability_no_mapk_driver_identified": 1.0 - on_target,
        "detectability": "A driver lesion is clonal or near-clonal, so it sits at roughly 25-50% "
                        "VAF -- orders of magnitude above every assay floor in SEQUENCING_ASSAYS. "
                        "This is the part of the N=1 question sequencing answers outright.",
        "on_target_arm": "resistance model applies as written; trametinib engages the driver",
        "off_target_arm": "no sequenced MAPK lesion -- the model's premise is unsupported for this "
                         "patient, and the actionable response is to choose a different primary "
                         "agent, not to run this model with a lower expected value",
        "why_this_dominates": "Sequencing shifts this from a known base rate to a known fact for "
                              "this dog, whereas the same sequencing shifts preexisting_prob by "
                              "at most a fold or so (see posterior_preexisting_prob).",
    }


def implied_preexisting_prob(observed_durable_fraction: float, durable_without_subclone: float,
                            durable_with_subclone: float) -> dict:
    """Invert the mixture: what `preexisting_prob` would reproduce an observed cohort outcome?
    `partition_by_preexisting_subclone` shows the ensemble is a two-component mixture, cohort = (1
    - p) * durable_without + p * durable_with which is invertible for `p` whenever the two arms
    differ.
    """
    separation = float(durable_without_subclone - durable_with_subclone)
    if abs(separation) < 1e-9:
        return {"implied_preexisting_prob": None, "identifiability": separation,
                "note": "arms are indistinguishable; the cohort outcome carries no information "
                       "about preexisting_prob and the inversion is undefined"}
    raw = (durable_without_subclone - observed_durable_fraction) / separation
    return {
        "observed_durable_fraction": float(observed_durable_fraction),
        "durable_without_subclone": float(durable_without_subclone),
        "durable_with_subclone": float(durable_with_subclone),
        "identifiability": separation,
        "implied_preexisting_prob": float(np.clip(raw, 0.0, 1.0)),
        "in_range": bool(0.0 <= raw <= 1.0),
        "caveat": "This is an inversion of *this model's* mixture, so it inherits every one of "
                  "the model's other assumptions -- growth rates, kill ceilings, detection "
                  "threshold, horizon.",
    }


def partition_two_compartment_by_preexisting_subclone(outcome,
                                                       resistant_indices: slice = slice(1, None)
                                                       ) -> dict:
    """`partition_by_preexisting_subclone`, adapted for `TwoCompartmentOutcome` (the localized pulmonary
    scenario), which carries separate `primary_trajectories`/`nodal_trajectories` instead of one
    `trajectories` array. Reads the day-0 state from the primary compartment only.
    """
    initial = np.asarray(outcome.primary_trajectories)[:, 0, :]
    has_subclone = initial[:, resistant_indices].sum(axis=1) > 0
    durable = ~np.asarray(outcome.progressed)

    def _arm(mask):
        n = int(mask.sum())
        return {"n_trials": n,
                "durable_response_fraction": float(durable[mask].mean()) if n else None,
                "median_time_to_progression_days":
                    float(np.nanmedian(np.asarray(outcome.time_to_progression)[mask]))
                    if n and not np.all(np.isnan(np.asarray(outcome.time_to_progression)[mask]))
                    else None}

    with_subclone, without_subclone = _arm(has_subclone), _arm(~has_subclone)
    spread = None
    if with_subclone["durable_response_fraction"] is not None and \
       without_subclone["durable_response_fraction"] is not None:
        spread = (without_subclone["durable_response_fraction"]
                  - with_subclone["durable_response_fraction"])
    return {
        "population_durable_response_fraction": float(durable.mean()),
        "with_preexisting_subclone": with_subclone,
        "without_preexisting_subclone": without_subclone,
        "spread_attributable_to_preexisting_resistance": spread,
    }


def partition_by_preexisting_subclone(outcome, resistant_indices: slice = slice(1, None)) -> dict:
    """Split a Monte Carlo ensemble into the two patient types it is silently averaging over.
    `preexisting_prob` makes the ensemble a *mixture*: some trials begin with a resistant subclone
    and some do not. The reported durable-response fraction is the mixture average, which is the
    correct cohort statistic and a misleading individual one -- no patient is a mixture.
    """
    initial = np.asarray(outcome.trajectories)[:, 0, :]
    has_subclone = initial[:, resistant_indices].sum(axis=1) > 0
    durable = ~np.asarray(outcome.progressed)

    def _arm(mask):
        n = int(mask.sum())
        return {"n_trials": n,
                "durable_response_fraction": float(durable[mask].mean()) if n else None,
                "median_time_to_progression_days":
                    float(np.nanmedian(np.asarray(outcome.time_to_progression)[mask]))
                    if n and not np.all(np.isnan(np.asarray(outcome.time_to_progression)[mask]))
                    else None}

    with_subclone, without_subclone = _arm(has_subclone), _arm(~has_subclone)
    spread = None
    if with_subclone["durable_response_fraction"] is not None and \
       without_subclone["durable_response_fraction"] is not None:
        spread = (without_subclone["durable_response_fraction"]
                  - with_subclone["durable_response_fraction"])
    return {
        "population_durable_response_fraction": float(durable.mean()),
        "with_preexisting_subclone": with_subclone,
        "without_preexisting_subclone": without_subclone,
        "spread_attributable_to_preexisting_resistance": spread,
        "n1_interpretation": (
            "The population number is a weighted average of these two arms."),
    }
