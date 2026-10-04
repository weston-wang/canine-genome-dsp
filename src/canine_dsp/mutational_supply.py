"""Mutational supply: why a low-mutation-burden tumor should endure better, and by how much.

WHY THIS MODULE EXISTS
----------------------
This repo has been using half of an argument. `mapk_scenarios._PREEXISTING_PROB_CENTRAL` carries a
long comment rejecting the human melanoma COMBI-d/v trial as a recentering basis, and one of its
stated reasons is mutational burden:

    "melanoma has an unusually high, UV-mutagenesis-driven tumor mutational burden, so whatever
     rate of pre-existing resistant clones it implies is not evidence about a UV-unrelated canine
     sarcoma's clonal heterogeneity"

That reasoning was used *defensively* -- to block a pessimistic recalibration -- and then never
applied in its positive form. But it is the same argument in both directions: if high mutational
burden supplies abundant raw material for many independent resistance routes to arise from, then a
genuinely low-burden tumor is supplied *less*, and that predicts better durability. Both HS and HSA
scenario modules nonetheless ship the identical `_SEEDING_RATE_TOTAL = 0.012`, and HS's
`preexisting_prob` was never adjusted for burden at all.

WHAT THE ARGUMENT IS, PRECISELY -- AND WHAT IT IS NOT
----------------------------------------------------
It is a *rate* (mutational-supply) argument, not a *count* (how-many-mechanisms) argument. This
distinction is load-bearing and easy to get wrong:

  * NOT CLAIMED: that a lineage-restricted tumor has fewer distinct escape mechanisms. Nothing here
    reduces the model's clone count. An RTK-driven tumor hit with an RTK inhibitor generally
    accumulates a rich catalog of resistance routes -- gatekeeper mutations, bypass receptor
    activation, downstream reactivation -- so assuming a smaller *number* of routes from anatomic or
    lineage uniqueness alone would be unjustified.
  * CLAIMED: that the *rate at which any given route gets populated* scales with the tumor's
    underlying mutation rate. Fewer mutations per cell division means each escape route is seeded
    more slowly and is less likely to already exist at treatment start -- which improves durability
    regardless of how many routes are drawn on the diagram.

In this repo's engine those are exactly two named parameters: `seeding_rates` (Poisson rate per
source-clone cell-day, `poisson_mutation_injections`) and `preexisting_prob` (`sample_initial_state`).
This module scales those two and only those two.

EMPIRICAL STATUS: PARTLY CONFIRMED, AND NOT FOR HS
--------------------------------------------------
Real canine pan-cancer TMB data now exists (Alsaihati et al. 2021), and it does two things:

  1. It *confirms* the defensive half of the argument in dogs rather than by analogy to human UV
     biology: canine oral melanoma really is high-burden. The melanoma comparator's rejection is now
     empirically backed, not merely inferred.
  2. It *undercuts* an earlier conclusion of this repo. The HS-vs-HSA comparison concluded the two
     diseases' different modelled outcomes trace to calibration choices rather than biology, having
     checked mechanism counts and margins. That check was correct about counts and incomplete about
     rates: canine hemangiosarcoma is measured high-burden, so a genuinely higher seeding rate and
     higher `preexisting_prob` for HSA than for HS may be biologically justified rather than an
     arbitrary calibration difference.

What it does NOT do is measure histiocytic sarcoma. HS is absent from that cohort's tumor types, and
the only canine HS whole-exome study found (Tani et al. 2023, 5 dogs) reports Sanger-validated
mutation counts but no burden in mutations per megabase. So the HS/HSA burden ratio -- the single
number this whole argument turns on -- is unmeasured, and is therefore swept here
(`TMB_RATIO_SWEEP`) rather than asserted, exactly as this repo treats every other unmeasured
parameter.

THE CONSEQUENCE IS LARGE, WHICH IS WHY IT NEEDS SWEEPING RATHER THAN A POINT ESTIMATE
------------------------------------------------------------------------------------
`single_patient.partition_by_preexisting_subclone` showed that at a realistic exposure duration the
cohort durable-response fraction is nearly a pure readout of `preexisting_prob` (the two patient
arms sit near 1.0 and near 0.0, so the average is essentially `1 - p`). That makes `preexisting_prob`
the highest-leverage parameter in the model, and it is precisely the parameter mutational supply
acts on. A fourfold burden reduction moves `p` from 0.30 to about 0.09 -- i.e. predicted durable
response from ~70% to ~91% -- on a mechanistic argument with no HS burden measurement behind it.
That is a real derivation and an unverified input at the same time, and both halves have to travel
together.

It also means one number must NOT travel: `single_patient.implied_preexisting_prob` inverted the
Skorupski benchmark to imply `p ~= 0.62` for the BMD context. That benchmark is breed-unstratified
and mixed-treatment, and if the low-burden argument holds for this HS presentation specifically then 0.62 is a
BMD-context number that would be wrong to carry over -- the same breed-mismatch error
`driver_conditioned_arms` was rewritten to prevent, running in the opposite (pessimistic) direction.
`refuse_bmd_benchmark_transfer` states that explicitly rather than leaving it to a reader's memory.
"""

import numpy as np

# Real measured canine pan-cancer tumor mutational burden. The load-bearing observation for this
# module is as much what is ABSENT as what is present: histiocytic sarcoma is not among the tumor
# types, so this data can bound HS's comparators but never HS itself.
CANINE_TMB_BY_TUMOR_TYPE = {
    "citation": "Alsaihati et al. 2021, Nat Commun 12:4670 (doi:10.1038/s41467-021-24836-9) -- "
               "'Canine tumor mutational burden is correlated with TP53 mutation across tumor types "
               "and breeds'",
    "cohort": "684 cases, >7 common tumor types, >35 breeds (reanalysis of whole-exome and "
             "whole-genome sequencing data)",
    "low_burden_types": {"mammary_tumor": "median < 0.5 mutations/Mb",
                        "glioma": "median < 0.5 mutations/Mb"},
    "high_burden_types": {"oral_melanoma": "median >= 1 mutations/Mb",
                         "osteosarcoma": "median >= 1 mutations/Mb",
                         "hemangiosarcoma": "median >= 1 mutations/Mb"},
    "threshold_used_by_authors": "the paper's own low/high split is drawn at roughly 0.5 vs 1.0 "
                                "mutations/Mb median; these are the reported medians, not a "
                                "validated clinical cutoff",
    "histiocytic_sarcoma_included": False,
    "why_this_matters_here": "Two of this repo's comparators are now measured rather than assumed. "
                           "Canine oral melanoma being genuinely high-burden empirically backs the "
                           "existing rejection of the human melanoma trial as a recentering basis. "
                           "Canine hemangiosarcoma being genuinely high-burden means HSA's more "
                           "pessimistic calibration may be biologically justified rather than "
                           "arbitrary -- which partially revises the earlier 'the HS/HSA difference "
                           "is calibration, not biology' conclusion.",
    "caveat": "TMB reflects accumulated mutations, which depends on the tumor's mutation RATE and on "
             "how many divisions it has been through. Treating a burden ratio as a pure mutation-"
             "rate ratio assumes comparable division history, which is not established across these "
             "tumor types.",
}

# The only canine HS exome study located. Reports mutations but not burden, which is exactly why the
# ratio this module needs has to be swept.
CANINE_HS_EXOME = {
    "citation": "Tani et al. 2023, Sci Rep 13 (PMC10212919) -- 'Whole exome and transcriptome "
               "analysis revealed the activation of ERK and Akt signaling pathway in canine "
               "histiocytic sarcoma'",
    "n_dogs_whole_exome_sequenced": 5,
    "validated_mutations_total": 35,
    "recurrent_genes": {"TP53": "2/5", "PTPN11": "2/5", "PDGFRB": "1/5", "SH3KBP1": "1/5"},
    "ras_mutations_found": False,
    "tumor_mutational_burden_reported": None,
    "caveat": "n=5, and the 35 mutations are a Sanger-validated subset after filtering, not a "
             "genome-wide burden estimate -- they cannot be converted into mutations/Mb. Breeds were "
             "not specified, so this says nothing about this HS presentation specifically. This is the entire "
             "published canine HS exome evidence base as far as could be found.",
}

MUTATIONAL_SUPPLY_HYPOTHESIS = {
    "claim": "The rate at which each resistance route gets populated scales with the tumor's "
            "underlying mutation rate, so a low-burden tumor seeds every route more slowly and is "
            "less likely to harbour one already at treatment start.",
    "does_not_claim": "That a lineage-restricted or anatomically-uniform tumor has FEWER distinct "
                     "escape mechanisms. Nothing in this module changes the model's clone count. "
                     "Anatomic and lineage uniformity are evidence about cell of origin and "
                     "dissemination, not about how many ways a tumor can evade a drug.",
    "acts_on_exactly": ["seeding_rates (poisson_mutation_injections)",
                        "preexisting_prob (sample_initial_state)"],
    "provenance": "Derived in this project's own reasoning from the mechanism behind melanoma's poor "
                 "durability under BRAF/MEK inhibition (high UV-driven burden supplying many "
                 "independent parallel resistance routes), then partially confirmed in dogs by "
                 "CANINE_TMB_BY_TUMOR_TYPE for the comparator tumors -- but NOT for HS, whose "
                 "burden is unmeasured.",
    "status": "mechanistically coherent, empirically unverified for histiocytic sarcoma",
}

# HS burden relative to a high-burden comparator (HSA/melanoma at >= 1 mut/Mb). 1.0 means "HS is
# just as mutable as hemangiosarcoma" (the status quo both scenario modules currently encode by
# sharing _SEEDING_RATE_TOTAL); 0.25 is roughly "HS resembles the low-burden types (< 0.5 mut/Mb)
# against a >= 1 mut/Mb comparator"; 0.1 is an aggressive low-burden case. Swept, not fixed, because
# no canine HS burden measurement exists to pick a value from.
TMB_RATIO_SWEEP = [1.0, 0.5, 0.25, 0.1]


def scale_preexisting_prob(preexisting_prob_reference: float, tmb_ratio: float) -> dict:
    """Rescale `preexisting_prob` for a tumor with `tmb_ratio` times the reference mutation supply.

    Not linear, and the non-linearity matters. `preexisting_prob` is the probability that at least
    one resistant clone exists by treatment start -- a saturating quantity, not a rate. Under a
    Poisson mutational-supply model with expected number of resistance-conferring hits `lambda`:

        p = 1 - exp(-lambda)        so      lambda = -ln(1 - p)

    Scaling the supply by `r` gives:

        p' = 1 - exp(-r * lambda) = 1 - (1 - p)**r

    Scaling `p` linearly instead would be wrong in both directions: it would understate the benefit
    of low burden when `p` is small and overstate it when `p` is near 1, where the reference tumor is
    already saturated and reducing supply cannot help much.
    """
    if not 0 <= preexisting_prob_reference <= 1:
        raise ValueError("preexisting_prob_reference must lie in [0, 1]")
    if tmb_ratio <= 0:
        raise ValueError("tmb_ratio must be positive")
    scaled = 1.0 - (1.0 - preexisting_prob_reference) ** tmb_ratio
    return {
        "preexisting_prob_reference": float(preexisting_prob_reference),
        "tmb_ratio": float(tmb_ratio),
        "preexisting_prob_scaled": float(scaled),
        "implied_poisson_lambda_reference": (
            float(-np.log(1 - preexisting_prob_reference))
            if preexisting_prob_reference < 1 else float("inf")),
        "approximate_durable_response_if_arms_are_saturated": float(1.0 - scaled),
        "note": "The last field uses the finding that at a realistic exposure duration the cohort "
               "durable-response fraction is nearly 1 - preexisting_prob (see "
               "single_patient.partition_by_preexisting_subclone). It is a shortcut for reading off "
               "the consequence, not a substitute for running the Monte Carlo.",
    }


def scale_seeding_rate(seeding_rate_reference: float | np.ndarray, tmb_ratio: float):
    """Rescale acquired-resistance seeding rates by the mutational-supply ratio.

    Linear here, unlike `scale_preexisting_prob`, because a seeding rate *is* a rate: halving the
    mutation supply halves the expected number of new resistant lineages per source-clone cell-day.
    No saturation applies, since `poisson_mutation_injections` draws a Poisson count from it rather
    than a probability.

    Accepts a scalar or the per-mechanism weight vector the scenario modules build, and preserves the
    relative weighting between mechanisms -- this argument is about total supply, not about which
    escape route is favoured.
    """
    if tmb_ratio <= 0:
        raise ValueError("tmb_ratio must be positive")
    rates = np.asarray(seeding_rate_reference, dtype=float)
    if np.any(rates < 0):
        raise ValueError("seeding rates must be nonnegative")
    scaled = rates * float(tmb_ratio)
    return float(scaled) if scaled.ndim == 0 else scaled


def refuse_bmd_benchmark_transfer(implied_bmd_preexisting_prob: float = 0.62) -> dict:
    """Why the BMD benchmark inversion must not be carried onto a low-burden or pulmonary arm.

    `single_patient.implied_preexisting_prob` inverted the Skorupski localized-HS CCNU benchmark and
    implied `p ~= 0.62` -- about double this module's 0.30 -- concluding the model is roughly twice
    too optimistic. That inference is sound for what it covers and unsound to generalize, and the two
    directions of error are symmetric enough to be worth stating together, since the same reasoning
    that blocks an optimistic transfer blocks this pessimistic one.
    """
    return {
        "implied_bmd_preexisting_prob": float(implied_bmd_preexisting_prob),
        "valid_for": "the BMD-context, debulked, localized-HS-plus-adjuvant-systemic-drug scenario "
                    "the benchmark actually describes",
        "must_not_transfer_to": [
            "any pulmonary arm -- the benchmark's breed composition is unreported and skews to the "
            "referral HS population (BMD/flat-coated retriever/rottweiler), and the one breed-"
            "matched this breed benchmark (single_patient.BREED_MATCHED_PULMONARY_HS_BENCHMARK) describes a "
            "different natural history entirely",
            "any low-mutational-supply arm -- the benchmark cohort was not stratified by burden or "
            "by driver status, so it averages over exactly the variation this scaling isolates",
        ],
        "symmetry_note": "This is the same class of error as applying BMD's 44/96 driver frequency "
                        "to an unsequenced breed, which driver_conditioned_arms was rewritten to refuse. It ran "
                        "in the pessimistic direction here, which made it easier to miss: a "
                        "correction that makes a model look worse still has to be scoped correctly.",
        "what_would_make_it_transferable": "a burden- or breed-stratified canine HS outcome cohort, "
                                          "which does not exist",
    }


def mutational_supply_report(preexisting_prob_reference: float,
                             seeding_rate_reference: float,
                             tmb_ratios: list[float] = TMB_RATIO_SWEEP) -> dict:
    """Full swept consequence of the mutational-supply argument on the two parameters it touches."""
    rows = []
    for ratio in tmb_ratios:
        scaled = scale_preexisting_prob(preexisting_prob_reference, ratio)
        rows.append({
            "tmb_ratio": float(ratio),
            "preexisting_prob": scaled["preexisting_prob_scaled"],
            "seeding_rate_total": scale_seeding_rate(seeding_rate_reference, ratio),
            "approximate_durable_response": scaled[
                "approximate_durable_response_if_arms_are_saturated"],
            "is_status_quo": bool(ratio == 1.0),
        })
    return {
        "hypothesis": MUTATIONAL_SUPPLY_HYPOTHESIS,
        "reference_preexisting_prob": float(preexisting_prob_reference),
        "reference_seeding_rate_total": float(seeding_rate_reference),
        "sweep": rows,
        "measured_canine_burden": CANINE_TMB_BY_TUMOR_TYPE,
        "hs_burden_evidence": CANINE_HS_EXOME,
        "benchmark_transfer_guard": refuse_bmd_benchmark_transfer(),
        "reading": "tmb_ratio=1.0 is what both scenario modules currently encode by sharing "
                  "_SEEDING_RATE_TOTAL between HS and a measured-high-burden disease. Every lower "
                  "ratio is the mutational-supply argument taken seriously. The spread across this "
                  "sweep is the size of the bet being made on an unmeasured quantity -- which is "
                  "the honest form of the answer, not any single row.",
    }
