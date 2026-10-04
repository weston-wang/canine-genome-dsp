"""Rule 13 ledger for the hemangiosarcoma program: agent tiers and class dispositions.

CLAUDE.md rule 13 requires two things this branch had never recorded in one place:

  1. every agent tiered as exists-today (licensed, off-label, or in dog trials) or to-build, with
     the program searched from exists-today agents first and any to-build dependency reported
     separately and as such;
  2. every modality class dispositioned, and excluded ONLY because its kill is contradicted, it is
     defeated by a named escape, or its toxicity cannot be afforded -- never because canine data
     are absent.

The rule exists because of failure 8: on the lymphoma branch the closing programs rested on a
CAR-T for dogs, a spinal-fluid CAR-T and a spinal pump, all to-build, while vaccines, engagers,
inhibitors and transplant were set aside for having no canine kill rate. This module is the audit
that shows whether the HSA program has the same defect. It does not: every component exists today.

Two classes were genuinely unexamined before this audit (T-cell engagers, marrow transplant) and
one was examined only as a toxicity note (radiation). They are dispositioned here for the first
time, on stated scientific reasons.

See docs/HSA_DURABLE_RESPONSE.md section 6c.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

# -------------------------------------------------------------------------------------------------
# TIERS. Rule 13's own vocabulary.
# -------------------------------------------------------------------------------------------------

LICENSED = "exists today -- licensed or standard of care in this species"
OFF_LABEL = "exists today -- given to dogs off-label"
DOG_TRIALS = "exists today -- administered in a published canine trial"
NEAR_FUTURE = ("near-future -- clinical-stage evidence of the modality in humans or dogs, a stated "
               "path to the dog, and a derived or transferred dose/kill")
TO_BUILD = "theoretical -- no clinical evidence of the mechanism anywhere, or the construct does not exist"

EXISTS_TODAY = (LICENSED, OFF_LABEL, DOG_TRIALS)
# Rule 13 admits the first two groups for closure; a theoretical agent never counts. The user
# (2026-10-02): "I don't mean you can only use therapies that exist today, I meant to include near
# future ones that are scientifically sound. Just nothing that's pure theoretical." This program
# happens to use none of the near-future tier -- its mix is 13 / 0 / 0 -- so the allowance is
# recorded and unused rather than absent. Do not retreat to "only what exists today".
USABLE_FOR_CLOSURE = EXISTS_TODAY + (NEAR_FUTURE,)


@dataclass(frozen=True)
class Agent:
    name: str
    tier: str
    role_in_program: str
    existence_evidence: str


# -------------------------------------------------------------------------------------------------
# THE PROGRAM, AGENT BY AGENT.
# -------------------------------------------------------------------------------------------------

PROGRAM_AGENTS: tuple[Agent, ...] = (
    Agent("splenectomy", LICENSED,
          "removes the primary and with it the splenic rupture hazard (route 5 at the spleen)",
          "the standard of care in canine splenic hemangiosarcoma; every trial in this record "
          "enrols post-splenectomy dogs"),
    Agent("ERstrePs vaccine", DOG_TRIALS,
          "the load-bearing floor-holder: the only permanently present mechanism in the program",
          "Marconato et al. 2023, Cancers 15(17):4209, PMID 37686485 -- 28 vaccinated vs 32 "
          "control dogs with this disease, 35.7% vs 6.3% at the reported landmark"),
    Agent("doxorubicin", LICENSED,
          "finite-course log-remover; the comparator every canine HSA trial is measured against",
          "standard of care; disease-free interval 133 d in Lana et al. 2007, PMID 17708397"),
    Agent("eBAT", DOG_TRIALS,
          "stromal lever (uPAR+ myeloid depletion) and a finite-course log-remover",
          "Borgatti et al. 2017 -- 23 dogs with this exact disease in this exact setting, "
          "positive at a tolerated dose; and the informative negative SRCBST-2, Borgatti et al. "
          "2020, Vet Comp Oncol 18(4):664-674, PMID 32187827, 25 dogs, where repeat cycles at a "
          "reduced interval from doxorubicin gave greater toxicity and reduced efficacy"),
    Agent("losartan", OFF_LABEL,
          "blocks the CCL2-CCR2 axis that recruits the suppressive macrophages capping vaccine "
          "height",
          "an angiotensin receptor blocker dogs already take indefinitely; canine exposure "
          "settled by dose-escalation to a measured pharmacodynamic endpoint in 28 dogs"),
    Agent("caninized anti-PD-1 / anti-PD-L1", DOG_TRIALS,
          "disarms PD-L1+ M2 macrophages that measurably exclude T cells",
          "dosed in 51 dogs on a booster-like schedule; and a commercially available veterinary "
          "checkpoint inhibitor now exists (Chon, Greene & Stock 2026, JAVMA)"),
    Agent("trametinib (MEK)", OFF_LABEL,
          "one half of the parallel-pathway pair that clears the exposure criterion",
          "target engagement demonstrated in canine tumour tissue at the tolerated canine dose "
          "(~16 nM against an ~11 nM combination requirement)"),
    Agent("dual TORC1/2 inhibitor", OFF_LABEL,
          "the other half of the pair; reduced to a one-year induction once the vaccine is raised",
          "tolerability data in healthy beagles -- 17 days, which is the duration shortfall this "
          "analysis treats as the component's binding weakness, not its existence"),
    Agent("lomustine", LICENSED,
          "CNS-penetrant finite-course log-remover for routes 8 and 12b in the brain",
          "Moore, Rassnick & Frimberger 2017, JAVMA 251(5):559-565, PMID 28828962 -- 30 dogs with "
          "stage II splenic hemangiosarcoma, splenectomy plus an anthracycline alternated with "
          "lomustine"),
    Agent("temozolomide", OFF_LABEL,
          "the second CNS-penetrant alkylator; covers lomustine's cross-species weakness",
          "given to dogs off-label; angiosarcoma-specific CNS response evidence is human "
          "(PMID 37811120, PMID 42125685) with a target rationale in angiosarcoma tissue "
          "(PARP1 46/47, SLFN11 80%, PMID 34085099)"),
    Agent("brain stereotactic radiosurgery", LICENSED,
          "treats an IMAGED intracranial deposit; deliberately not credited against occult seeding",
          "CyberKnife SRS was delivered to a dog with intracranial hemangiosarcoma on day 310 "
          "after resection (Biundo, Marino & Roynard 2026, Front Vet Sci 13:1778366, "
          "PMID 42038052) -- the indication is documented, the benefit is not"),
    Agent("craniotomy and resection of a solitary intracranial deposit", LICENSED,
          "the CNS analogue of splenectomy: removes a vascular mass before it bleeds",
          "Biundo, Marino & Roynard 2026, PMID 42038052 -- two dogs, ante-mortem MRI diagnosis, "
          "resection performed, histopathology confirmed hemangiosarcoma, 'surgical resection of "
          "this solitary mass is doable'"),
    Agent("meloxicam", LICENSED,
          "the COX-2 arm of the Treg lever, and the cheapest component in the program",
          "a licensed canine NSAID given to dogs indefinitely, so its duration criterion is met by "
          "ordinary veterinary practice rather than by a transfer"),
)


def to_build_dependencies() -> list[Agent]:
    """Rule 13: a program needing a theoretical agent is reported separately and as such."""
    return [a for a in PROGRAM_AGENTS if a.tier == TO_BUILD]


def near_future_agents() -> list[Agent]:
    """Rule 13 admits these for closure. Empty for this program, which is a fact worth reporting:
    the allowance exists and this program did not need it."""
    return [a for a in PROGRAM_AGENTS if a.tier == NEAR_FUTURE]


def tier_mix() -> dict[str, int]:
    """The three-way mix rule 13 asks a program to be reported with."""
    return {
        "exists_today": sum(1 for a in PROGRAM_AGENTS if a.tier in EXISTS_TODAY),
        "near_future": len(near_future_agents()),
        "theoretical": len(to_build_dependencies()),
    }


def program_is_built_from_existing_agents() -> bool:
    return not to_build_dependencies()


def tier_counts() -> dict[str, int]:
    counts: dict[str, int] = {}
    for a in PROGRAM_AGENTS:
        counts[a.tier] = counts.get(a.tier, 0) + 1
    return counts


# The distinction that must not be collapsed: no new molecule is required, but one combination
# effect is unmeasured. Those are different kinds of gap and failure 4 was committed by merging them.
NO_NEW_MOLECULE_BUT_ONE_UNMEASURED_COMBINATION = {
    "what_the_program_needs_that_no_single_agent_delivers": "a vaccine ~1.40x taller than the "
        "ERstrePs trial measured (0.030 -> 0.042/day).",
    "is_that_a_to_build_agent": "No. It is produced by adding exists-today levers to an "
        "exists-today vaccine: anti-PD-1, losartan, eBAT and recurrent immunisation, each of which "
        "is tiered above. No molecule has to be invented.",
    "what_it_is_instead": "a QUANTIFICATION gap -- nobody has measured what those levers add to "
        "vaccine height in combination. The required transfer fractions are 7.3-22.3% (losartan), "
        "17.8-23.4% (eBAT) and 22.6-45.2% (anti-PD-L1); see hsa_route_effect_sizes.",
    "why_the_distinction_matters": "failure 4 in CLAUDE.md was overstating closure by merging "
        "'the model contains an agent that covers it' with 'real data supports this'. A missing "
        "molecule would be a coverage gap and fatal to a program built from existing agents. An "
        "unmeasured combination is a quantification gap, and it is the one this program carries.",
}


# -------------------------------------------------------------------------------------------------
# THE CLASS LEDGER. Rule 9 fixes the candidate universe; rule 13 fixes the admissible reasons.
# -------------------------------------------------------------------------------------------------

IN_PROGRAM = "IN THE PROGRAM"
EXCLUDED = "EXCLUDED on a stated scientific reason"
NOT_YET_ASSESSED = "NOT YET ASSESSED -- named path to assessment recorded"

# The only three reasons rule 13 admits for excluding a class.
KILL_CONTRADICTED = "its kill is contradicted"
DEFEATED_BY_ESCAPE = "it is defeated by a named escape"
TOXICITY_UNAFFORDABLE = "its toxicity cannot be afforded"
ADMISSIBLE_REASONS = (KILL_CONTRADICTED, DEFEATED_BY_ESCAPE, TOXICITY_UNAFFORDABLE)

# The reason rule 13 forbids. Present so the compliance test can assert it is never used.
FORBIDDEN_REASON = "canine data are absent"


@dataclass(frozen=True)
class ClassDisposition:
    modality_class: str
    status: str
    tier_of_the_best_available_agent: str
    reason: str
    reason_kind: str
    the_evidence: str


CLASS_LEDGER: tuple[ClassDisposition, ...] = (
    ClassDisposition(
        "cytotoxics", IN_PROGRAM, LICENSED,
        "three are carried: doxorubicin systemically, lomustine and temozolomide for the CNS",
        "", "Lana 2007 PMID 17708397; Moore 2017 PMID 28828962"),
    ClassDisposition(
        "targeted small molecules / inhibitors", IN_PROGRAM, OFF_LABEL,
        "trametinib plus a dual TORC1/2 inhibitor clear the exposure criterion; losartan carries "
        "the stromal arm",
        "", "canine target engagement for trametinib; 28-dog dose escalation for losartan. "
            "Toceranib MAINTENANCE was separately tried in this disease and failed -- that is a "
            "contradicted kill for one agent on one schedule, not an excluded class"),
    ClassDisposition(
        "antibodies (checkpoint)", IN_PROGRAM, DOG_TRIALS,
        "caninized anti-PD-1/PD-L1 is one of four independent ways to raise vaccine height",
        "", "51 dogs on a booster-like schedule; a veterinary checkpoint inhibitor is now "
            "commercially available"),
    ClassDisposition(
        "antibody-drug conjugates", EXCLUDED, TO_BUILD,
        "the ADC bystander effect INCREASES with the antigen-positive fraction and dissipates as "
        "that fraction falls, so it is weakest exactly where route 8 needs it -- against rare "
        "antigen-null cells. The mechanism runs backwards for this geometry",
        KILL_CONTRADICTED,
        "the bystander literature's own finding, recorded in "
        "hsa_route8_alternatives.BYSTANDER_KILLING_FAILS_FOR_A_REASON_WORTH_RECORDING"),
    ClassDisposition(
        "bispecifics -- angiotoxin", IN_PROGRAM, DOG_TRIALS,
        "eBAT is in the program. It survives route 8 because it is not antigen-directed: it "
        "targets uPAR and EGFR on host stroma as well as tumour",
        "", "Borgatti 2017 (23 dogs, positive) and PMID 32187827 (25 dogs, negative on repeat "
            "dosing)"),
    ClassDisposition(
        "bispecifics -- T-cell engagers", EXCLUDED, TO_BUILD,
        "an engager is antigen-directed, so it is void against the antigen-null fraction that "
        "route 8 names, and against the antigen-positive fraction it duplicates the vaccine's "
        "T-cell arm, which is already present permanently. It adds nothing against the escape "
        "that decides the question",
        DEFEATED_BY_ESCAPE,
        "NO canine T-cell-engager trial exists -- a PubMed search for one returns only a human "
        "cardio-oncology review (PMID 33934609). That absence is recorded and is explicitly NOT "
        "the reason for exclusion; the reason is the antigen dependence"),
    ClassDisposition(
        "cell therapy -- NK", EXCLUDED, DOG_TRIALS,
        "NK augmentation was administered to dogs and the outcome was WORSE, with a measured "
        "mechanism for why",
        KILL_CONTRADICTED,
        "hsa_route8_alternatives.AUGMENTING_NK_WAS_TRIED_IN_DOGS_AND_MADE_THINGS_WORSE and "
        "WHY_IT_FAILED_IS_MEASURED_AND_IT_MATTERS -- a contradicted kill in the right species"),
    ClassDisposition(
        "cell therapy -- CAR-T", EXCLUDED, TO_BUILD,
        "a single-antigen receptor is void against the antigen-null fraction, the same defect as "
        "the engager. The canine platform exists but an HSA-directed construct does not, so "
        "relying on it would repeat failure 8 exactly: building the answer on an agent to build",
        DEFEATED_BY_ESCAPE,
        "the canine platform is real -- Panjwani et al. 2016, Mol Ther 24(9):1602-14, "
        "PMID 27401141: autologous CD20 CAR T cells given to a dog with relapsed B-cell lymphoma, "
        "well tolerated, 'modest, but transient' antitumour activity, the authors concluding "
        "stable expression is needed for durable remission. Platform exists today; an HSA "
        "construct is to-build"),
    ClassDisposition(
        "stem-cell and marrow transplant", EXCLUDED, DOG_TRIALS,
        "transplant acts only on the log-removal term, and section 3h established that log "
        "removal alone cannot close route 8 -- only a permanently present negative-growth floor "
        "can. It is the most toxic possible finite-course log-remover added to a stack that "
        "already has three, in a dog with minimal residual disease rather than refractory bulk; "
        "and its dose-intensification rationale is void here because the binding toxicities are "
        "cardiac, hepatic and renal, not marrow",
        TOXICITY_UNAFFORDABLE,
        "the class exists in dogs and is not hypothetical -- nonmyeloablative DLA-identical "
        "marrow allografts give stable mixed chimerism in dogs (Zaucha et al. 2001, Biol Blood "
        "Marrow Transplant 7(1):14-24, PMID 11215693). So the exclusion is NOT for absent canine "
        "data: it is the wrong shape for the escape and the wrong toxicity for the setting"),
    ClassDisposition(
        "vaccines and active immunotherapy", IN_PROGRAM, DOG_TRIALS,
        "ERstrePs is the load-bearing component and the only permanent mechanism",
        "", "PMID 37686485. eVim is excluded as the PLATFORM CHOICE, not as a class, because it "
            "lacks the T-cell arm route 9 requires"),
    ClassDisposition(
        "radiation -- body", EXCLUDED, LICENSED,
        "no transferable canine dataset exists for this disease and the modality is a "
        "field-limited log-remover, which is the term the stack is already strongest in",
        DEFEATED_BY_ESCAPE,
        "the one canine curative-intent SBRT series in soft-tissue sarcoma EXPLICITLY EXCLUDED "
        "hemangiosarcoma from enrolment (Gagnon et al. 2020, JAVMA 256(1):102-110, "
        "PMID 31841095), and a PubMed search for canine hemangiosarcoma radiotherapy outcome "
        "returns only the eBAT trial. Route 7 is disseminated micrometastatic disease, which a "
        "radiation field cannot cover -- that is the named escape, not the missing dataset"),
    ClassDisposition(
        "radiation -- brain, to an imaged deposit", IN_PROGRAM, LICENSED,
        "credited only against an imaged intracranial deposit, and deliberately NOT credited "
        "against routes 8 and 12b, which describe occult seeding a beam cannot be aimed at",
        "", "SRS was delivered to a dog with intracranial hemangiosarcoma (PMID 42038052)"),
    ClassDisposition(
        "surgery", IN_PROGRAM, LICENSED,
        "splenectomy for the primary; craniotomy and resection for a solitary imaged "
        "intracranial deposit",
        "", "standard of care, and PMID 42038052 for the intracranial case"),
    ClassDisposition(
        "sanctuary-site delivery", IN_PROGRAM, LICENSED,
        "solved pharmacologically by two lipophilic alkylators, so no intrathecal catheter or "
        "pump is required -- which is what keeps this program free of to-build hardware",
        "", "lomustine and temozolomide, tiered above"),
    ClassDisposition(
        "oncolytic virus", NOT_YET_ASSESSED, TO_BUILD,
        "the only canine hemangiosarcoma datum is a single case in a DIFFERENT primary site "
        "(bone), which cannot yield a gradable kill rate. Under rule 11 a number with no basis "
        "stays ASSUMED and does not count as closure -- so this class is unassessed, NOT excluded",
        "",
        "the named path to assessment: human angiosarcoma intratumoural oncolytic data would give "
        "a transfer of the same kind already accepted for temozolomide (same tumour type, "
        "different species). Until that transfer is written the class stays unassessed. Recorded "
        "in hsa_route8_alternatives.ONCOLYTIC_VIRUS_IS_AN_ANECDOTE_NOT_EVIDENCE"),
    ClassDisposition(
        "cytokine agents", NOT_YET_ASSESSED, OFF_LABEL,
        "never assessed on their own. The one canine datum adjacent to them is the NK "
        "augmentation trial that made outcomes worse, which does not settle the class",
        "",
        "the named path: an IL-15 or IL-2 exposure-response transfer would have to clear the same "
        "two criteria every other lever here clears -- achievable exposure above effect "
        "concentration, and documented tolerability across the horizon"),
)


def classes_excluded_for_absent_canine_data() -> list[ClassDisposition]:
    """Rule 13 compliance. MUST return an empty list."""
    return [c for c in CLASS_LEDGER
            if c.status == EXCLUDED and FORBIDDEN_REASON in c.reason.lower()]


def exclusions_with_inadmissible_reasons() -> list[ClassDisposition]:
    """Rule 13 compliance. Every exclusion must cite one of the three admissible reasons."""
    return [c for c in CLASS_LEDGER
            if c.status == EXCLUDED and c.reason_kind not in ADMISSIBLE_REASONS]


def unassessed_classes() -> list[ClassDisposition]:
    return [c for c in CLASS_LEDGER if c.status == NOT_YET_ASSESSED]


def classes_in_program() -> list[ClassDisposition]:
    return [c for c in CLASS_LEDGER if c.status == IN_PROGRAM]


# -------------------------------------------------------------------------------------------------
# THE FINDING THIS AUDIT TURNED UP: canine intracranial hemangiosarcoma is now documented.
# -------------------------------------------------------------------------------------------------

INTRACRANIAL_HSA_IS_NOW_DOCUMENTED_IN_DOGS = {
    "citation": "Biundo N, Marino DJ, Roynard P. 2026. Surgical treatment and outcome of "
                "intracranial hemangiosarcoma in two dogs: case series. Front Vet Sci "
                "13:1778366. PMID 42038052, doi 10.3389/fvets.2026.1778366",
    "why_it_matters_here": "the conjunction's one remaining open cell is route 5 in its CNS form: "
                           "haemorrhage from a vascular brain deposit, with no treating component. "
                           "This is the first canine series of ante-mortem diagnosed, surgically "
                           "treated intracranial hemangiosarcoma -- the same species, the same "
                           "tumour, the same compartment.",
    "what_it_establishes": (
        "MRI gave an ante-mortem diagnosis of an intracranial mass in both dogs",
        "resection was performed and histopathology confirmed hemangiosarcoma in both",
        "the authors' conclusion: 'surgical resection of this solitary mass is doable and may be "
        "associated with good quality of life in the short to intermediate term'",
        "stereotactic radiosurgery (CyberKnife) was deliverable to a canine intracranial "
        "hemangiosarcoma -- one dog received it on day 310 after MRI-confirmed regrowth on day 280",
    ),
    "what_it_does_not_establish": (
        "no survival benefit: the dogs were euthanased at 87 and 314 days post-operatively",
        "no reduction in haemorrhage risk is measured -- neither death was attributed to "
        "haemorrhage, but n=2 and neither had a necropsy",
        "primary intracranial status was suspected, not confirmed, for want of necropsy",
        "both were SOLITARY imaged masses. Resection cannot treat a deposit imaging has not "
        "found, which is the same objection that keeps brain radiotherapy uncredited against "
        "routes 8 and 12b",
    ),
    "the_grading_it_supports": "route 5 at the CNS moves OPEN -> PARTIALLY CLOSED. The mechanism "
                               "that closes route 5 at the spleen is 'image the vascular mass and "
                               "remove it before it bleeds', and that mechanism is now documented "
                               "in the canine brain. It closes for a solitary IMAGED deposit and "
                               "stays open for occult or multifocal ones.",
    "the_new_condition_it_exposes": "the project assumes early detection, but the surveillance it "
                                    "assumes is abdominal and thoracic. For the detection "
                                    "assumption to reach the CNS at all, surveillance imaging has "
                                    "to include the brain. No canine HSA surveillance protocol in "
                                    "this record does. That is a NEW open condition, and it is the "
                                    "honest cost of the regrade.",
}


# -------------------------------------------------------------------------------------------------
# RULE 14. Before calling a quantity unmeasured, name its measurable proxy and search for THAT.
#
# The quantity this ledger called unmeasured was "how much alkylator reaches the antigen-null cells
# behind the blood-brain barrier". The proxy is a drug concentration measured in brain interstitium
# BEHIND AN INTACT BARRIER -- which for a microdialysis study means a catheter in peritumoral brain
# rather than in the enhancing core, where the barrier is already broken. Searching the concept
# ("CNS reach") found nothing gradable. Searching the proxy found a human trial.
# -------------------------------------------------------------------------------------------------

TEMOZOLOMIDE_MW_G_PER_MOL = 194.15

# Portnow et al. 2009, intracerebral microdialysis, catheter in PERITUMORAL brain tissue, single
# oral 150 mg/m2, 7 of 9 patients yielding paired dialysate and plasma.
TMZ_BRAIN_PEAK_UG_PER_ML = 0.6
TMZ_BRAIN_PEAK_SD_UG_PER_ML = 0.3
TMZ_BRAIN_AUC_UG_H_PER_ML = 2.7
TMZ_PLASMA_AUC_UG_H_PER_ML = 17.1
TMZ_BRAIN_TMAX_HOURS = 2.0
# The paper reports 17.8% as the mean of the per-patient brain:plasma AUC ratios. Dividing the two
# reported MEAN AUCs gives 15.8%. Both are kept: a mean of ratios is not the ratio of means, and
# quoting one while computing the other would be an inconsistency hiding in a rounding.
TMZ_REPORTED_MEAN_OF_RATIOS = 0.178


def ug_per_ml_to_micromolar(ug_per_ml: float,
                            mw_g_per_mol: float = TEMOZOLOMIDE_MW_G_PER_MOL) -> float:
    """1 ug/mL = 1 mg/L; divide by g/mol to get mmol/L, then x1000 for umol/L."""
    return float(ug_per_ml / mw_g_per_mol * 1000.0)


def tmz_brain_interstitium_exposure() -> dict:
    """The measured half of the exposure criterion, in the compartment at issue."""
    peak = TMZ_BRAIN_PEAK_UG_PER_ML
    lo = peak - TMZ_BRAIN_PEAK_SD_UG_PER_ML
    hi = peak + TMZ_BRAIN_PEAK_SD_UG_PER_ML
    return {
        "peak_uM": ug_per_ml_to_micromolar(peak),
        "peak_uM_range_1sd": (ug_per_ml_to_micromolar(lo), ug_per_ml_to_micromolar(hi)),
        "brain_AUC_uM_h": ug_per_ml_to_micromolar(TMZ_BRAIN_AUC_UG_H_PER_ML),
        "ratio_of_mean_AUCs": TMZ_BRAIN_AUC_UG_H_PER_ML / TMZ_PLASMA_AUC_UG_H_PER_ML,
        "reported_mean_of_per_patient_ratios": TMZ_REPORTED_MEAN_OF_RATIOS,
        "tmax_hours": TMZ_BRAIN_TMAX_HOURS,
    }


RULE_14_PROXY_SEARCH = {
    "the_quantity_called_unmeasured": "how much alkylator reaches antigen-null hemangiosarcoma "
                                      "cells seeded behind the blood-brain barrier -- recorded in "
                                      "the conjunction as 'reach TRANSFERRED, logs UNMEASURED'.",
    "the_proxy_written_down_first": "a drug concentration measured in brain interstitium behind an "
                                    "INTACT barrier. Operationally that is intracerebral "
                                    "microdialysis with the catheter in PERITUMORAL brain, not in "
                                    "the enhancing core where the barrier is already broken, and "
                                    "not a rodent brain:plasma ratio.",
    "what_the_proxy_search_found_for_temozolomide": {
        "citation": "Portnow J, Badie B, Chen M, Liu A, Blanchard S, Synold TW. 2009. The "
                    "neuropharmacokinetics of temozolomide in patients with resectable brain "
                    "tumors. Clin Cancer Res 15(22):7092-8. PMID 19861433, "
                    "doi 10.1158/1078-0432.CCR-09-1349",
        "design": "intracerebral microdialysis catheter placed in PERITUMORAL brain tissue at "
                  "debulking, CT-confirmed position, single oral temozolomide 150 mg/m2 on "
                  "postoperative day 1, serial paired plasma and dialysate over 24 h by tandem "
                  "mass spectrometry. 9 enrolled, 7 yielding paired samples.",
        "the_numbers": "brain interstitial AUC 2.7 vs plasma 17.1 ug/mL*h; mean peak brain "
                       "concentration 0.6 +/- 0.3 ug/mL; brain Tmax 2.0 +/- 0.8 h. The paper's "
                       "headline brain:plasma AUC ratio is 17.8%, which is the mean of the "
                       "per-patient ratios; dividing the two mean AUCs gives 15.8%. Both are "
                       "carried, because a mean of ratios is not the ratio of means.",
        "why_it_is_the_right_compartment": "the catheter is in brain parenchyma adjacent to the "
                                           "tumour, which is what 'behind an intact barrier' means "
                                           "operationally. The authors also note the values agree "
                                           "with preclinical microdialysis and with clinical CSF "
                                           "studies, so three independent routes to the same "
                                           "compartment concur.",
        "grade": "MEASURED, in humans. The transfer to the dog is the species step and nothing "
                 "more -- it is not an inference INTO the compartment.",
    },
    "what_this_settles_and_what_it_does_not": "it settles the EXPOSURE half of the criterion: the "
        "achievable concentration in the compartment at issue is ~3.1 uM at peak (1.5-4.6 uM at "
        "+/-1 SD) with 16-18% of plasma AUC, and that number is measured rather than inferred. It "
        "does NOT complete the criterion, because the matching EFFECT concentration for "
        "angiosarcoma is not published: a search for a temozolomide concentration-response in "
        "angiosarcoma cell lines returns nothing, including in the paper that reports "
        "olaparib + temozolomide synergy in those lines (PMID 34085099).",
    "and_an_in_vitro_comparison_would_be_the_wrong_test_anyway": "temozolomide's in-vitro IC50s "
        "are high and strongly schedule-dependent, because a short assay cannot reproduce a "
        "multi-day alkylation schedule and the response is MGMT- and mismatch-repair-dependent. So "
        "the stronger evidence for this agent stays what it already was: documented CNS responses "
        "in angiosarcoma, in the right tumour type and the right compartment (PMID 37811120, "
        "PMID 42125685). The exposure figure is now a floor under that, not a replacement for it.",
    "where_the_proxy_search_FAILED": "lomustine. A search for a measured brain-tissue or CSF "
        "lomustine concentration returns nothing in PubMed. Its CNS credit therefore still rests "
        "on clinical use in canine intracranial disease plus the same-species, same-disease "
        "deliverability trial (PMID 28828962) -- reach, not exposure. Rule 14 is a method, not a "
        "guarantee, and reporting the half that failed is the point of running it.",
    "the_net_effect_on_the_ledger": "temozolomide moves from 'reach only' to 'reach plus a MEASURED "
        "right-compartment exposure, effect concentration still unpublished'. Lomustine does not "
        "move. The CNS closure for routes 8 and 12b is unchanged in status and better anchored on "
        "one of its two agents.",
}


# -------------------------------------------------------------------------------------------------
# VERDICT.
# -------------------------------------------------------------------------------------------------

VERDICT = {
    "headline": "The hemangiosarcoma program is built entirely from agents that exist today. "
                "Thirteen components, zero to-build: six licensed or standard of care, four "
                "off-label in dogs, and three administered in published canine trials. No molecule "
                "has to be invented, no construct engineered and no hardware implanted.",
    "the_contrast_that_prompted_the_audit": "this is the opposite of failure 8. The lymphoma "
                                            "closing programs rested on a CAR-T for dogs, a "
                                            "spinal-fluid CAR-T and a spinal pump -- all to-build "
                                            "-- while real classes were set aside for lacking "
                                            "canine kill rates. Rule 13 was written from that, and "
                                            "the HSA program passes it.",
    "what_the_program_does_carry": "one unmeasured combination effect, not a missing agent: the "
                                   "~1.40x vaccine height is assembled from existing levers whose "
                                   "joint contribution nobody has measured. A quantification gap, "
                                   "graded as one.",
    "classes_excluded_and_why": "six, each on an admissible reason. ADCs and NK augmentation on a "
                                "CONTRADICTED KILL (the ADC bystander mechanism runs backwards at "
                                "low antigen-positive fraction; NK augmentation made canine "
                                "outcomes worse). T-cell engagers, CAR-T and body radiation on a "
                                "NAMED ESCAPE (antigen dependence for the first two, "
                                "micrometastatic dissemination for the third). Marrow transplant "
                                "on UNAFFORDABLE TOXICITY plus wrong shape -- it is a "
                                "finite-course log-remover, and route 8 needs a permanent floor.",
    "classes_left_unassessed_and_named_as_such": "two -- oncolytic virus and cytokine agents. "
                                                 "Neither is excluded; each has a named transfer "
                                                 "that would make it assessable. Saying 'unassessed' "
                                                 "rather than 'closed' is rule 9, and saying it "
                                                 "rather than 'excluded for want of canine data' is "
                                                 "rule 13.",
    "the_net_change_to_the_conjunction": "one cell improves and one condition appears. Route 5 at "
                                         "the CNS moves OPEN -> PARTIALLY CLOSED on a same-species "
                                         "same-compartment feasibility series (PMID 42038052), and "
                                         "that regrade exposes a new open condition: surveillance "
                                         "imaging has to include the brain, which no protocol in "
                                         "this record does. The ledger did not simply get better.",
}
