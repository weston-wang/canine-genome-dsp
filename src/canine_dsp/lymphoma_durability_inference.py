"""Is 2-year disease-free a sound inference for 10-year disease-free in canine lymphoma?

The real transplant cure fraction (40%) is defined at >=2 years, but the stated target is 10-year
durability or cure. This module interrogates the model's relapse *timing* to answer whether the
2-year mark is a reasonable proxy for the decade -- and finds the answer is mechanism-dependent:
it holds when the durability mechanism clears the bar with margin, and it degrades into a small
late-relapse tail (from rare late-emerging drug resistance, not antigen loss) exactly at the bar.

Every figure is recomputed from the engine by tests/test_lymphoma_inference_and_toxicity.py.
See docs/LYMPHOMA_DURABLE_RESPONSE.md section 8.
"""

import numpy as np


def conditional_durability(progressed: np.ndarray, time_to_progression: np.ndarray,
                           dominant_mechanism: list[str],
                           early_day: int = 730, late_day: int = 3650) -> dict:
    """From a MonteCarloOutcome's fields, compute how well disease-free-at-`early_day` predicts
    disease-free-at-`late_day`.

    A trial is disease-free at day D if it never progressed, or progressed only after D. Returns the
    two disease-free fractions, the conditional probability P(df@late | df@early), the count and
    mechanism breakdown of the relapses that fall in the (early, late] window, and the median/90th
    percentile relapse day among all progressors -- the shape of the hazard over time.
    """
    progressed = np.asarray(progressed, dtype=bool)
    ttp = np.asarray(time_to_progression, dtype=float)
    n = len(progressed)
    if n == 0:
        raise ValueError("empty outcome")

    def disease_free_at(day):
        # not progressed at all, or progressed strictly after `day`
        return ~progressed | (ttp > day)

    df_early_mask = disease_free_at(early_day)
    df_late_mask = disease_free_at(late_day)
    df_early = float(df_early_mask.mean())
    df_late = float(df_late_mask.mean())
    # trials disease-free at early_day that then relapse by late_day
    late_relapse_mask = df_early_mask & progressed & (ttp > early_day) & (ttp <= late_day)
    late_relapse = int(late_relapse_mask.sum())
    df_early_count = int(df_early_mask.sum())
    late_hazard = late_relapse / df_early_count if df_early_count else 0.0
    conditional = df_late / df_early if df_early > 0 else float("nan")
    late_mechanisms: dict[str, int] = {}
    for i in np.flatnonzero(late_relapse_mask):
        m = dominant_mechanism[i]
        late_mechanisms[m] = late_mechanisms.get(m, 0) + 1
    progressor_days = ttp[progressed & ~np.isnan(ttp)]
    median_day = float(np.median(progressor_days)) if progressor_days.size else float("nan")
    p90_day = float(np.percentile(progressor_days, 90)) if progressor_days.size else float("nan")
    return {
        "disease_free_early": df_early, "disease_free_late": df_late,
        "conditional_late_given_early": conditional,
        "late_relapse_count": late_relapse, "disease_free_early_count": df_early_count,
        "late_relapse_hazard": late_hazard, "late_relapse_mechanisms": late_mechanisms,
        "median_relapse_day": median_day, "p90_relapse_day": p90_day,
    }


# The regime table, recomputed by the test module (trials=400, seed=7, horizon 10 years). Read
# "P(10y|2y)" as: of the dogs disease-free at 2 years, what fraction are still disease-free at 10.
TWO_YEAR_INFERENCE = {
    "chemo_only": {
        "df_2y": 0.180, "df_10y": 0.180, "conditional": 1.000,
        "late_relapses": 0, "median_relapse_day": 83, "p90_relapse_day": 114,
        "note": "All relapse within ~4 months. 2y is a perfect proxy -- of a bad outcome.",
    },
    "subthreshold_immuno_0_06": {
        "df_2y": 0.215, "df_10y": 0.215, "conditional": 1.000,
        "late_relapses": 0, "median_relapse_day": 164, "p90_relapse_day": 263,
        "note": "Still front-loaded (all by ~9 months). 2y is a perfect proxy, still of a bad outcome.",
    },
    "at_the_bar_immuno_0_09": {
        "df_2y": 0.995, "df_10y": 0.968, "conditional": 0.972,
        "late_relapses": 11, "late_relapse_of": 398,
        "late_mechanisms": {"mdr1_pgp_efflux": 10, "cd20_antigen_loss": 1},
        "median_relapse_day": 1663, "p90_relapse_day": 3213,
        "note": "A ~3% late-relapse tail spread across the decade (median relapse day 1663, 90th "
                "3213). Almost all of it is rare late-emerging P-gp DRUG resistance, not antigen "
                "loss -- so a tandem construct does not remove it, only potency margin does.",
    },
    "at_the_bar_plus_tandem": {
        "df_2y": 0.990, "df_10y": 0.963, "conditional": 0.972,
        "late_relapses": 11, "late_relapse_of": 396,
        "late_mechanisms": {"mdr1_pgp_efflux": 11},
        "median_relapse_day": 2030, "p90_relapse_day": 3185,
        "note": "Closing antigen loss removes the 1 antigen-loss late relapse; the ~3% P-gp tail "
                "remains, confirming the late tail is a drug-resistance phenomenon.",
    },
    "above_the_bar_immuno_0_12": {
        "df_2y": 1.000, "df_10y": 1.000, "conditional": 1.000,
        "late_relapses": 0,
        "note": "Clearing the bar with margin eliminates the late tail entirely. 2y = 10y exactly.",
    },
}

THE_ANSWER = {
    "question": "Is disease-free at 2 years a reasonable inference for disease-free at 10 years?",
    "short_answer": "It depends entirely on whether the regimen clears the durability bar, and by "
                    "how much margin.",
    "cases": [
        "Below the bar (chemo alone, or a sub-threshold immune effector): relapse is entirely "
        "front-loaded -- essentially every dog that will relapse has done so within 9 months -- so "
        "2-year disease-free implies 10-year disease-free with probability ~1.000. The inference is "
        "SAFE but trivial, because almost every dog has already relapsed by 2 years (df ~0.18-0.22).",
        "Exactly at the bar: a small late-relapse tail appears -- about 3% of dogs disease-free at "
        "2 years relapse between years 2 and 10, spread across the whole decade (median relapse day "
        "~4.5 years). So 2-year disease-free OVER-estimates 10-year by ~3 points. Crucially the tail "
        "is rare late-emerging DRUG resistance (P-glycoprotein), not antigen loss, so a tandem CAR "
        "does not shrink it.",
        "Above the bar with margin: no late relapse at all -- 2-year disease-free equals 10-year "
        "disease-free. Potency margin, not antigen insurance, is what makes 2 years a safe proxy.",
    ],
    "practical_reading": "For a dog on a genuinely bar-clearing regimen, 2-year disease-free is a "
                         "strong (~97%) lower bound on 10-year durability, and MRD monitoring "
                         "(Aresu et al. 2014; Sato et al. 2016) is exactly the tool to catch the "
                         "rare late drug-resistant relapse in that tail. And because dogs live "
                         "~10-13 years, 10-year durability is effectively lifetime cure.",
    "the_honest_limit": "This is the MODEL's late-relapse hazard, which arises from its "
                        "exponential-growth + rare-Poisson-seeding structure. Real 2-year-to-10-year "
                        "attrition is bounded by things the model does not include: competing "
                        "non-lymphoma mortality over a decade in an older dog, second primary "
                        "cancers, and therapy-related myeloid neoplasia after total body "
                        "irradiation. Those make real 10-year durability HARDER than 2-year "
                        "disease-free suggests, in the opposite direction from the tumour dynamics. "
                        "The tumour-relapse inference is sound at the bar; the whole-animal "
                        "inference must also clear those competing risks.",
}
