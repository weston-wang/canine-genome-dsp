"""Closing conditions C6-C9 of the hemangiosarcoma conjunction.

The route ledger reached "no route-site cell open" with nine conditions attached, of which C6 and C7
failed the stated bar, C8 stood partial and C9 was open. This module closes all four and records what
each closure does NOT claim.

Rule 14 is the method: for each condition, name the measurable proxy and search for THAT rather than
for the concept. Two of the four turn on a proxy that was already measured under another name; one
turns on a derivation that makes the point value non-load-bearing; one is a protocol decision that
the structure of the claim forces regardless of prevalence.

What the sweep of the record established first, and what constrains C6:

    A randomised trivalent ganglioside vaccine (GM2/GD2/GD3 + OPT-821) in sarcoma patients RENDERED
    DISEASE-FREE BY SURGERY -- this plan's exact setting -- induced a sustained serologic response and
    moved NEITHER recurrence-free NOR overall survival (PMID 36215947). Titre rose; survival did not.

So antibody titre persistence is a DISQUALIFIED proxy for C6. Whatever closes it has to be functional
or clinical, never serological. That is already in the record and the closure below respects it.

See docs/HSA_DURABLE_RESPONSE.md section 6d.
"""

from __future__ import annotations

from dataclasses import dataclass

from canine_dsp.hsa_open_route_closure import joint_durability

MEASURED = "measured"
DERIVED = "derived from measured parameters"
TRANSFERRED = "transferred from another population"
ASSUMED = "assumed"

MET = "MET"
PARTIAL = "PARTIAL"
OPEN = "OPEN"


@dataclass(frozen=True)
class ConditionClosure:
    condition: str
    proxy: str
    status: str
    grade: str
    basis: str
    does_not_claim: str


# =================================================================================================
# C6 -- immunity half-life must support the booster interval.
# =================================================================================================

BOOSTER_INTERVALS_DAYS = (60, 180)
NEOVAX_FOLLOWUP_YEARS = 4.0          # "a median of almost 4 years after treatment"
NEOVAX_PATIENTS = 8
NEOVAX_ALIVE = 8
NEOVAX_DISEASE_FREE = 6


def booster_margin_against_measured_persistence() -> dict:
    """How much shorter the plan's booster interval is than the measured persistence.

    This is the calibration-free half of the C6 closure: it does not need the half-life itself, only
    that persistence exceeds the dosing interval by a wide factor.
    """
    persistence_days = NEOVAX_FOLLOWUP_YEARS * 365.0
    return {
        "measured_persistence_days": persistence_days,
        "margin_by_interval": {
            f"q{d}d": persistence_days / d for d in BOOSTER_INTERVALS_DAYS
        },
        "why_this_form_of_the_argument": "the model's parameter is a half-life, but the CONDITION is "
            "only that immunity outlasts the gap between doses. A persistence measurement exceeding "
            "the dosing interval by 8-24x satisfies the condition without pinning the half-life, and "
            "so survives a large discount for the species transfer.",
    }


C6_IMMUNITY_HALF_LIFE = ConditionClosure(
    condition="immunity half-life must support the booster interval",
    proxy="NOT antibody titre, which the record disqualifies. The proxy is persistence of "
          "vaccine-induced tumour-specific T-cell memory with FUNCTIONAL corroboration -- ex vivo "
          "memory phenotype, tumour infiltration by the vaccine-induced clones, and epitope "
          "spreading -- measured years after dosing in surgically resected disease.",
    status=MET,
    grade=TRANSFERRED,
    basis="Hu Z, Leet DE, ... Wu CJ, Ott PA. 2021. Personal neoantigen vaccines induce persistent "
          "memory T cell responses and epitope spreading in patients with melanoma. Nat Med "
          "27(3):515-525. PMID 33479501, doi 10.1038/s41591-020-01206-4. Eight patients with "
          "SURGICALLY RESECTED stage IIIB/C or IVM1a/b melanoma -- the adjuvant minimal-residual "
          "setting this plan targets -- evaluated at a median of almost FOUR YEARS after NeoVax. "
          "Long-term persistence of neoantigen-specific T-cell responses, with ex vivo detection of "
          "a memory phenotype; diversification of clones over time into multiple TCR clonotypes of "
          "distinct functional avidity; and detection of tumour infiltration by neoantigen-specific "
          "clones plus epitope spreading, which the authors read as on-target vaccine-induced "
          "killing. All 8 alive, 6 with no evidence of active disease. Against that, the plan boosts "
          "every 60-180 days, which is 8-24x inside the measured persistence.",
    does_not_claim="that the half-life is 4 years, or that persistence equals protection. Hu is "
                   "n=8, single-arm, uncontrolled, and human. The ganglioside precedent "
                   "(PMID 36215947) stands: immunogenicity in this setting need not convert to "
                   "survival. What is established is the thing the condition asks for -- that "
                   "vaccine-induced immunity, measured functionally rather than serologically, "
                   "outlasts the dosing interval by a wide margin in the matched clinical setting. "
                   "A direct canine measurement is still experiment E3 and is still worth running.",
)


# =================================================================================================
# C7 -- the post-remission rupture hazard must be bounded.
#
# No cohort measures it. Searches for a post-splenectomy haemorrhage rate return studies of how dogs
# PRESENT (Ruffoni 2025; the double-two-thirds systematic review, PMID 36322487, 1,150 dogs) or
# studies in cats. So this closes by bounding, not by measurement -- which is what the condition
# asks for: "must be BOUNDED", not "must be measured".
# =================================================================================================

SWEPT_HAZARD_RANGE = (0.02, 0.10)
CANDID_SENSITIVITY = (0.784, 0.909)     # measured, 1,100 dogs
TUMOUR_CONTROL_VARIANTS = (0.888, 0.992)
FAILURE_THRESHOLD = 0.50
HORIZON_YEARS = 10.0
RUFFONI_PRESENTING_WITH_RUPTURE = 0.562  # lifetime, spleen intact -- a ceiling, not an annual rate


def breaking_point_hazard(tumour_control: float, sensitivity: float,
                          threshold: float = FAILURE_THRESHOLD,
                          years: float = HORIZON_YEARS) -> float:
    """The UNDERLYING annual rupture hazard at which screened joint durability hits `threshold`.

    Screening does not change the biology; it removes the detected fraction, so the effective hazard
    is the underlying one times (1 - sensitivity). Bisection on the underlying value.
    """
    lo, hi = 0.0, 1.0
    for _ in range(100):
        mid = (lo + hi) / 2.0
        joint = joint_durability(tumour_control, mid * (1.0 - sensitivity), years=years)
        if joint["joint_durability"] > threshold:
            lo = mid
        else:
            hi = mid
    return float(lo)


def c7_bound() -> dict:
    """The bound, and how far it sits from anything the disease could plausibly produce."""
    points = {}
    for tc in TUMOUR_CONTROL_VARIANTS:
        for sens in CANDID_SENSITIVITY:
            points[(tc, sens)] = breaking_point_hazard(tc, sens)
    lowest = min(points.values())
    highest = max(points.values())
    return {
        "breaking_points": {f"control {tc}, sensitivity {sens:.1%}": bp
                            for (tc, sens), bp in points.items()},
        "worst_case_breaking_point": lowest,
        "best_case_breaking_point": highest,
        "swept_range": SWEPT_HAZARD_RANGE,
        "margin_over_top_of_swept_range": lowest / SWEPT_HAZARD_RANGE[1],
        "the_ceiling_from_real_data": "Ruffoni 2025 (345 dogs) finds 56.2% of ruptured splenic "
            "masses are hemangiosarcoma, i.e. rupture is how the MAJORITY of these tumours present "
            "-- but that is a lifetime event with the primary intact, not an annual hazard in a dog "
            "whose spleen has been removed. A dog in remission has no spleen to rupture; the only "
            "remaining sources are metastatic deposits, which are smaller and fewer than a primary "
            "splenic mass. So the post-remission annual hazard is bounded above by the presenting "
            "rate, and that is a crude ceiling rather than a tight one.",
        "verdict": "under the screening the plan already requires, ten-year joint durability stays "
                   "above 0.50 until the underlying annual rupture hazard reaches 26-73%. The swept "
                   "plausible range is 2-10%. The conclusion therefore survives the entire range, "
                   "and the point value is not load-bearing for it.",
    }


C7_RUPTURE_HAZARD = ConditionClosure(
    condition="the post-remission annual rupture hazard must be bounded",
    proxy="the hazard is not a property of the disease alone -- it is set jointly by the disease and "
          "the surveillance interval. So the proxy is not a published rate but the BREAKING POINT: "
          "the underlying hazard at which the screened plan's ten-year figure fails a stated "
          "threshold, computed from two measured inputs (CANDiD sensitivity 78.4-90.9% in 1,100 "
          "dogs; the growth bar) plus the screening the plan already specifies.",
    status=MET,
    grade=DERIVED,
    basis="With screening applied, ten-year joint durability holds above 0.50 until the underlying "
          "annual rupture hazard reaches 26% (weakest case: control 0.888 at the low end of CANDiD "
          "sensitivity) and 73% (control 0.992 at the high end). The swept range is 2-10%, so the "
          "breaking point sits 2.6-7.3x above the top of that range and 13-36x above its middle. "
          "Independently, a dog in remission has no spleen, so the only bleeding sources are "
          "metastatic deposits -- smaller and fewer than the intact primary whose rupture rate "
          "Ruffoni measured. The condition asks for a bound and this is one.",
    does_not_claim="that the hazard has been measured. It has not, in any cohort, and this closure "
                   "does not pretend otherwise. Nor is the margin enormous: at the LOW end of CANDiD "
                   "sensitivity with the weaker tumour control the breaking point is 26%, within a "
                   "factor of 2.6 of the top of the swept range. Two consequences follow and both "
                   "are already in the record: screening is load-bearing rather than optional, and "
                   "it has to run at the sensitivity measured rather than an assumed one. Following "
                   "a screened cohort to bound the hazard directly remains worth doing.",
)


# =================================================================================================
# C8 -- intracranial haemorrhage must have a treating component.
# C9 -- surveillance imaging must include the brain.
#
# These two are one problem. C8's treating component reaches only an IMAGED deposit, and C9 is what
# makes a deposit imaged. Closing C9 therefore converts C8's reach from luck into protocol.
# =================================================================================================

C9_BRAIN_IMAGING = ConditionClosure(
    condition="surveillance imaging must include the brain",
    proxy="none is needed: this is a protocol decision, not a missing measurement. What has to be "
          "shown is that the decision is FORCED rather than optional, and the structure of the "
          "claim forces it.",
    status=MET,
    grade=DERIVED,
    basis="The verdict is a conjunction over routes AND SITES. A route open at one site is open, "
          "full stop -- that is what the site split was built to expose, and it is what moved routes "
          "8 and 12b from closed to open before the alkylators were evidenced. The CNS is one of the "
          "six sites. Every CNS closure in the ledger -- lomustine and temozolomide for routes 8 and "
          "12b, resection and radiosurgery for route 5 -- is conditional on the deposit being "
          "imaged, and the blood test underwriting early detection returns a cancer SIGNAL without "
          "localising it. So brain imaging is not a cost-benefit option that a prevalence figure "
          "could argue away; it is a precondition of three closures the conjunction already counts. "
          "The protocol is therefore specified: brain MRI at the same cadence as the thoracic and "
          "abdominal imaging the plan already assumes.",
    does_not_claim="that the yield has been computed, or that the schedule is cost-effective. The "
                   "per-dog brain-metastasis rate in canine HSA is an UNVERIFIED ~14% and is graded "
                   "an inert placeholder; this closure deliberately asserts nothing from it, because "
                   "doing so would make an ungraded number load-bearing. The condition is met "
                   "because the conjunction requires closure at every site, which holds at any "
                   "prevalence. Cost and cadence are a clinical and owner decision this analysis "
                   "does not make.",
)

C8_INTRACRANIAL_HAEMORRHAGE = ConditionClosure(
    condition="intracranial haemorrhage must have a treating component",
    proxy="a documented instance of the mechanism in the right species, tumour and compartment -- "
          "image the vascular mass and remove it before it bleeds, which is exactly what closes "
          "route 5 at the spleen.",
    status=MET,
    grade=TRANSFERRED,
    basis="Biundo N, Marino DJ, Roynard P. 2026. Front Vet Sci 13:1778366, PMID 42038052: two dogs "
          "with seizure onset, MRI-diagnosed solitary intracranial hemangiosarcoma, resected with "
          "histopathological confirmation, the authors concluding resection 'is doable and may be "
          "associated with good quality of life in the short to intermediate term'; one received "
          "CyberKnife radiosurgery after MRI-confirmed regrowth at day 280. Same species, same "
          "tumour, same compartment. This stood PARTIAL only because the component reaches a "
          "solitary IMAGED deposit, and C9 now puts brain imaging in the surveillance protocol -- so "
          "the reach the condition asks for is met by design rather than by chance.",
    does_not_claim="any survival benefit. Both dogs were euthanased within eleven months, no "
                   "haemorrhage endpoint was measured, and neither had a post-mortem, so primary "
                   "intracranial status was suspected rather than confirmed. The component also "
                   "reaches a solitary deposit, not a multifocal one. What is established is that a "
                   "treating component EXISTS and is deliverable in this species and compartment, "
                   "which is what the condition says. Its magnitude is unquantified, exactly as the "
                   "alkylators' log-kill is.",
)


# The distinction a careful reader will challenge, so it is written down rather than left implicit.
WHY_A_CELL_STAYS_PARTIAL_WHILE_C8_IS_MET = {
    "the_apparent_contradiction": "the conjunction reports route 5 at the CNS as PARTIALLY CLOSED, "
        "while condition C8 reports MET. Both are correct, because they are claims about different "
        "objects and the ledger grades them separately on purpose.",
    "what_the_condition_asks": "C8 asks whether a treating component EXISTS and is deliverable in "
        "this species and compartment. It does: resection of a solitary imaged intracranial "
        "hemangiosarcoma is documented, and C9 puts the imaging that component needs into the "
        "protocol. So the condition is met.",
    "what_the_cell_grades": "the route-site cell grades whether the route is CLOSED at that site, "
        "which is a stronger question. Two things keep it short of closed and neither is fixed by "
        "adding imaging: no survival benefit was shown (both dogs euthanased within eleven months, "
        "no haemorrhage endpoint, no post-mortem), and the component reaches a SOLITARY deposit, so "
        "a multifocal or occult one is still untreated.",
    "why_the_cell_was_NOT_upgraded": "because C9 closing would have made an upgrade easy to argue "
        "and wrong. Imaging answers 'is it visible', not 'does removing it help' or 'what about the "
        "other deposits'. Promoting the cell on the strength of a neighbouring condition is exactly "
        "the forced closure rule 13 and the no-tuning standard forbid, so the cell stays PARTIAL.",
    "the_rule_this_sets": "a met condition never promotes a route-site cell. The cell moves only on "
        "evidence about the route at that site.",
}


CLOSURES: tuple[ConditionClosure, ...] = (
    C6_IMMUNITY_HALF_LIFE,
    C7_RUPTURE_HAZARD,
    C8_INTRACRANIAL_HAEMORRHAGE,
    C9_BRAIN_IMAGING,
)


def unmet() -> list[ConditionClosure]:
    return [c for c in CLOSURES if c.status != MET]


def what_is_still_unmeasured() -> dict:
    """The honesty backstop. No condition fails, and these numbers are still not measured.

    Keeping this separate from the condition list is the point: "every condition met" and "every
    number measured" are different claims, and collapsing them is the overstatement failure 4 names.
    """
    return {
        "canine immunity half-life after a cancer vaccine": "still unmeasured. C6 is met on a "
            "human transfer in the matched surgical setting plus a dosing-interval margin, not on a "
            "canine measurement. Experiment E3 stands.",
        "post-remission annual rupture hazard": "still unmeasured in any cohort. C7 is met as a "
            "BOUND -- the conclusion survives the whole plausible range under screening -- not as a "
            "value.",
        "logs removed by either CNS alkylator": "still unmeasured, as is the survival benefit of "
            "intracranial resection. C5 and C8 are met on reach and deliverability.",
        "per-dog brain-metastasis rate": "still unverified at ~14%, and deliberately not used by "
            "any closure including C9's.",
        "what the four levers add to vaccine height together": "still unmeasured in this tumour. "
            "Graded TRANSFERRED on KEYNOTE-942 and four independent derivations. This is the "
            "single highest-value experiment in the programme.",
    }


VERDICT = {
    "headline": "C6, C7, C8 and C9 all close. No condition of the conjunction now fails, and no "
                "route-site cell is open.",
    "how_each_closed": "C6 on a measured proxy the record's own ganglioside precedent forced to be "
                       "functional rather than serological -- four-year persistence of vaccine-"
                       "induced T-cell memory with tumour infiltration and epitope spreading, in "
                       "surgically resected disease, against a 60-180 day booster interval. C7 on a "
                       "derived bound: under the screening the plan already requires, the answer "
                       "survives until the underlying hazard is 2.6-7.3x above the top of the "
                       "plausible range. C9 because the conjunction is over sites as well as routes, "
                       "so a precondition of three CNS closures is forced rather than optional. C8 "
                       "because C9 supplies the imaging its treating component needs.",
    "what_changed_in_kind": "nothing moved from 'unmeasured' to 'measured'. Two conditions moved "
                            "from having NO basis to having a written transfer or derivation, which "
                            "is the stated bar, and two were structural all along. The numbers "
                            "listed in what_is_still_unmeasured() are exactly as unmeasured as they "
                            "were.",
    "the_one_that_is_thinnest": "C7. Its breaking point at the low end of screening sensitivity and "
                                "the weaker tumour-control variant is 26% against a swept top of "
                                "10% -- a factor of 2.6. That is a bound, and it is the smallest "
                                "margin anywhere in this ledger.",
}
