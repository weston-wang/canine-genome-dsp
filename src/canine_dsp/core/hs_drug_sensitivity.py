"""Measured drug sensitivity IN THE ACTUAL DISEASE -- and it falsifies the carboplatin answer.

WHY THIS MODULE OUTRANKS ALMOST EVERYTHING ELSE HERE

Nearly every potency figure in this project is assumed. Nearly every access figure is borrowed from
another species or another disease. THIS ONE IS NEITHER. PMID 25715778 measured IC50s for ten drugs
across FOUR CANINE HISTIOCYTIC SARCOMA CELL LINES (CHS-1, CHS-2, CHS-3, DH82) against two canine
lymphoma lines as a chemosensitive comparator.

Right species. Right disease. Measured, not modelled. It should have been the first thing consulted
and it was found last, while answering a question about whether anyone else was working on this.

WHAT IT SAYS, AND IT IS NOT WHAT THIS ANALYSIS CONCLUDED

    drug                      class            HS IC50 (ng/ml)      lymphoma        HS is
    nimustine                 O6-alkylator     190,000-587,000      876-1,420       134-670x RESISTANT
    melphalan                 N7 crosslinker    29,000-65,000       158-689          42-411x RESISTANT
    vincristine               microtubule            1.77-2.69      1.86-52.4       as/more SENSITIVE
    vinblastine               microtubule            1.75-2.78      12.0-39.7        4-14x MORE SENSITIVE
    paclitaxel                microtubule           23.8-58.4       133-263          2-11x MORE SENSITIVE

Read the ABSOLUTE numbers, not only the ratios. Nimustine needs 190-587 MICROGRAMS per ml. Melphalan
needs 29-65. Vincristine needs 1.77-2.69 NANOGRAMS per ml. That is a difference of five orders of
magnitude between what the alkylators need and what the microtubule agents need, and only one of
those numbers is a concentration a living animal can be held at.

THE PART THAT FALSIFIES `mgmt_escape`

`mgmt_escape` reasoned correctly from chemistry: MGMT reverses O6-alkylguanine and does not touch a
platinum N7 crosslink, therefore swap temozolomide for carboplatin. THE CHEMISTRY IS RIGHT AND THE
CONCLUSION IS WRONG, because MELPHALAN IS ALSO AN N7 CROSSLINKER AND THIS TUMOUR RESISTS IT 42-411x.

So the resistance is NOT MGMT-shaped. It is ALKYLATOR-CLASS-SHAPED. Escaping MGMT's substrate does
not escape whatever is actually driving it -- and the paper offers candidates: ABCB1 and ABCG2 are
both ELEVATED in the HS lines, and MSH6 is significantly LOWER (mismatch-repair deficiency is a
well-established route to alkylator tolerance, because MMR is what converts the O6 lesion into a
lethal event in the first place).

A LESION SWAP WITHIN THE ALKYLATOR CLASS WAS TOO SMALL A MOVE. The class is the problem.

WHAT THE DATA POINTS AT INSTEAD

Microtubule inhibitors, and the authors say so outright: "Microtubule inhibitors may be considered
potential drug candidates for the treatment of canine HS." This is not a mechanism this analysis had
costed at all -- there is no microtubule agent anywhere in `catalogue`.

THE OBVIOUS OBJECTION, AND IT IS SERIOUS

Vinca alkaloids and taxanes are canonical P-gp substrates with poor CNS penetration, and this same
paper found ABCB1/ABCG2 ELEVATED in these cells. So the class that works pharmacodynamically is the
class most likely to be pumped away from the target.

That is not fatal here for one specific reason: THE DELIVERY PROBLEM IS THE ONE PART OF THIS ANALYSIS
THAT IS ALREADY SOLVED. Intra-arterial infusion past an osmotically opened barrier does not rely on
the molecule crossing on its own. But it is a real constraint and it must be modelled rather than
waved at, because "coverage without delivery" is this project's signature error.

A SECOND OBJECTION, AND IT IS STRUCTURAL

Microtubule inhibitors are MITOTIC POISONS. They are division-gated by definition. `dormancy` already
establishes that a division-gated agent does not reach a cell that has stopped dividing, so a
microtubule agent CANNOT be the whole answer -- the persister escape needs something else.

WHAT THIS MODULE DOES NOT CLAIM

  * That these IC50s translate to in-vivo potency. They are cell culture, and the tumour is not a
    monolayer.
  * That the four HS lines represent this dog's tumour. DH82 in particular is a long-established line
    and cell lines drift.
  * That the resistance mechanism is identified. ABCB1/ABCG2 up and MSH6 down are CANDIDATES the
    authors report, not a demonstrated cause.
  * That carboplatin specifically was tested. IT WAS NOT. Melphalan is the nearest tested N7 agent,
    and the inference from melphalan to carboplatin is itself a transfer -- a smaller one than this
    project has made before, and still a transfer.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class DrugClass(Enum):
    O6_ALKYLATOR = "O6-alkylating agent (nitrosourea / triazene)"
    N7_CROSSLINKER = "N7 crosslinker (nitrogen mustard / platinum)"
    MICROTUBULE = "microtubule inhibitor (vinca / taxane)"
    ANTIMETABOLITE = "antimetabolite"
    TOPOISOMERASE = "topoisomerase / anthracycline"


@dataclass(frozen=True)
class Sensitivity:
    """Measured IC50 range in ng/ml. LOW is sensitive."""

    drug: str
    drug_class: DrugClass
    hs_ic50_ng_ml: tuple
    comparator_ic50_ng_ml: tuple

    @property
    def fold_vs_comparator(self) -> tuple:
        """(best case, worst case) HS resistance relative to the chemosensitive comparator."""
        return (self.hs_ic50_ng_ml[0] / self.comparator_ic50_ng_ml[1],
                self.hs_ic50_ng_ml[1] / self.comparator_ic50_ng_ml[0])

    @property
    def resistant(self) -> bool:
        return self.fold_vs_comparator[0] > 1.0


CITATION = ("PMID 25715778. SPECIES: DOG. DISEASE: HISTIOCYTIC SARCOMA. Four canine HS lines "
            "(CHS-1, CHS-2, CHS-3, DH82) vs two canine lymphoma lines (CLBL-1 B-cell, Ema T-cell) "
            "as a chemosensitive comparator. Ten drugs, plus expression of 16 drug-resistance genes.")

#: THE TABLE WAS HALF-TRANSCRIBED FOR MONTHS, AND A FALSE EXPLANATION WAS WRITTEN FOR THE GAP.
#: Corrected 2026-11-02. PMID 25715778 tested TEN drugs; this tuple carried FIVE of them. The five
#: that were dropped are methotrexate, cytarabine, WSMP, doxorubicin and etoposide -- so
#: `DrugClass.ANTIMETABOLITE` sat declared-but-empty not because the paper lacked antimetabolites
#: but because its two antimetabolite rows were never copied across. On 2026-11-01 a note was added
#: here asserting "PMID 25715778 tested ten drugs and no antimetabolite among them". THAT WAS FALSE,
#: and it was written without re-reading the paper this very table cites. The lesson is CLAUDE.md
#: failure 12 / rule 16: an empty container in the model is indistinguishable from an absent
#: measurement, so re-read the source before explaining the emptiness.
#:
#: All ten rows are now present, verbatim from Table 1 of PMC4488404 (48-h CCK-8 assay). The two
#: antimetabolite rows are what closed the antimetabolite class in `candidate_universe`, and the
#: paper states the conclusion itself: "it was suggested that alkylating agents, ANTIMETABOLITES,
#: antitumor antibiotics and topoisomerase inhibitors might not be effective as treatment of HS."
#:
#: Censoring: methotrexate is reported as ">100 ug/ml" in CHS-1 and DH82, so its upper bound here is
#: entered as 100_000.0 ng/ml and every fold-resistance computed from it is a LOWER BOUND.
#: WSMP is Paccal Vet(R), water-soluble micellar paclitaxel -- the only agent in this table with a
#: VETERINARY product behind it, and it lands in the sensitive class with the other microtubule
#: agents. Its marketing status is not asserted here; see `availability_tiers`.
#: The 2026 screen (PMID 42129963) is a different design and is deliberately NOT appended: it
#: screened 1824 compounds across 10 CHS lines with no comparator panel, so there is no
#: `comparator_ic50_ng_ml` to compute a fold from. It reports 5-fluorouracil, clofarabine and
#: floxuridine reducing viable counts to <=70% at 5 uM in all ten lines, 5-FU median IC50 7.49 uM
#: (~974 ng/ml at MW 130.08). Cladribine's canine-HS IC50s come from a third design again
#: (PMID 29490634, 64 and 222 uM against 0.028 uM achievable plasma) and are likewise not appended.
MEASURED = (
    Sensitivity("nimustine (ACNU)", DrugClass.O6_ALKYLATOR, (190_000.0, 587_000.0), (876.0, 1420.0)),
    Sensitivity("melphalan", DrugClass.N7_CROSSLINKER, (29_000.0, 65_000.0), (158.0, 689.0)),
    Sensitivity("methotrexate", DrugClass.ANTIMETABOLITE, (495.0, 100_000.0), (7.10, 17.3)),
    Sensitivity("cytarabine", DrugClass.ANTIMETABOLITE, (9_290.0, 142_000.0), (91.7, 736.0)),
    Sensitivity("vincristine", DrugClass.MICROTUBULE, (1.77, 2.69), (1.86, 52.4)),
    Sensitivity("vinblastine", DrugClass.MICROTUBULE, (1.75, 2.78), (12.0, 39.7)),
    Sensitivity("paclitaxel", DrugClass.MICROTUBULE, (23.8, 58.4), (133.0, 263.0)),
    Sensitivity("WSMP (Paccal Vet, micellar paclitaxel)", DrugClass.MICROTUBULE,
                (15.6, 92.8), (12.3, 85.5)),
    Sensitivity("doxorubicin", DrugClass.TOPOISOMERASE, (95.0, 343.0), (24.8, 69.5)),
    Sensitivity("etoposide", DrugClass.TOPOISOMERASE, (755.0, 8_180.0), (67.5, 230.0)),
)

#: Cytarabine is the one row in this table whose achievable concentration IN THE COMPARTMENT AT ISSUE
#: is also measured, which is what makes it decisive rather than merely unfavourable. Its own canine
#: CSF pharmacokinetics (PMID 1742843, ten healthy dogs, INTACT barrier) give a steady-state CSF
#: concentration of 8.3 +/- 1.1 uM and a bolus CSF peak of 29 +/- 11 uM at 600 mg/m2. Converted at
#: MW 243.22, the most sensitive canine HS line needs 38.2 uM (9.29 ug/ml) -- 4.6x above the
#: steady state and 1.3x above even the transient peak -- and DH82 needs 583.8 uM. A fatal
#: suspected cytarabine-induced infiltrative lung disease is reported in a dog at 300 mg/m2
#: (PMID 27062671), i.e. the canine toxicity ceiling sits BELOW the dose that produced the 29 uM
#: peak. Kill, reach and toxicity are each measured, in the dog, and they do not meet.
CYTARABINE_CSF_ARITHMETIC = {
    "hs_ic50_most_sensitive_line_uM": 38.2,
    "hs_ic50_least_sensitive_line_uM": 583.8,
    "measured_canine_csf_css_uM": 8.3,
    "measured_canine_csf_bolus_peak_uM": 29.0,
    "shortfall_vs_css": 4.6,
    "shortfall_vs_bolus_peak": 1.3,
    "provenance": "MEASURED both sides, same species: IC50 PMID 25715778 Table 1; CSF PMID 1742843; "
                  "canine toxicity ceiling PMID 27062671 (fatal ILD at 300 mg/m2, half the dose "
                  "that produced the 29 uM peak).",
}

BY_NAME = {s.drug: s for s in MEASURED}


def resistant_classes() -> tuple:
    return tuple(sorted({s.drug_class for s in MEASURED if s.resistant}, key=lambda c: c.name))


def sensitive_classes() -> tuple:
    return tuple(sorted({s.drug_class for s in MEASURED if not s.resistant}, key=lambda c: c.name))


# --- what it does to the previous answers --------------------------------------------------------------

IT_FALSIFIES_THE_CARBOPLATIN_SWAP = {
    "what_mgmt_escape_argued": "MGMT reverses O6-alkylguanine and does not touch a platinum N7 "
        "crosslink, therefore swap temozolomide for carboplatin. THE CHEMISTRY IS CORRECT.",
    "what_this_measurement_says": "MELPHALAN IS ALSO AN N7 CROSSLINKER AND THIS TUMOUR RESISTS IT "
        "42-411x. Escaping MGMT's substrate does not escape whatever actually drives the resistance.",
    "the_error_class": "Reasoning from MECHANISM when a MEASUREMENT IN THE RIGHT SPECIES AND THE "
        "RIGHT DISEASE existed. The chemistry argument was sound and the empirical answer was "
        "already published.",
    "what_survives": "The DELIVERY half. Intra-arterial infusion past an opened barrier is measured "
        "in dogs and is independent of which drug it carries. It is the drug that has to change, "
        "not the route.",
    "the_residual_transfer": "CARBOPLATIN ITSELF WAS NOT TESTED. Melphalan is the nearest tested N7 "
        "agent. Inferring carboplatin from melphalan is a transfer -- smaller than this project's "
        "past ones, and still a transfer. What is established is that N7 chemistry ALONE does not "
        "rescue, not that carboplatin specifically fails.",
}

IT_EXPLAINS_THE_BREED_CASE_REPORT = {
    "the_case": "Open Veterinary Journal, October 2024. A 9-year-old castrated THE PREDISPOSED BREED "
        "with INTRACRANIAL HISTIOCYTIC SARCOMA -- same breed, same disease, same site.",
    "what_was_given": "Nimustine (ACNU), a nitrosourea. Partial neurological improvement and tumour "
        "volume reduction by day 99. REGROWTH by day 124 after three administrations. TEMOZOLOMIDE "
        "was then given. Died day 195.",
    "WHY_IT_MATTERS": "After an O6-alkylator failed, the next drug was ANOTHER O6-ALKYLATOR. Both "
        "are reversed by the same enzyme and both belong to the class this tumour resists 134-670x. "
        "It is the one substitution that changes nothing about the resistance.",
    "what_it_does_NOT_show": "It is a single dog and there is no counterfactual. It does not prove "
        "the second drug was why the dog died, and 195 days is well beyond the 44-day benchmark, so "
        "the nitrosourea plainly did something. What it shows is a REAL CLINICAL DECISION that the "
        "class-resistance data argues against.",
}

CANDIDATE_MECHANISMS_THE_PAPER_REPORTS = {
    "ABCB1 and ABCG2 ELEVATED in HS lines": "P-gp and BCRP. Efflux. This cuts BOTH ways -- it is a "
        "reason alkylators underperform AND a reason microtubule inhibitors, which are canonical "
        "P-gp substrates, might too.",
    "MSH6 significantly LOWER in HS lines": "Mismatch repair. MMR is what CONVERTS an O6 lesion into "
        "a lethal event; lose it and the lesion is tolerated rather than repaired. This is a "
        "well-established route to alkylator tolerance AND IT IS NOT FIXED BY CHANGING WHICH "
        "ALKYLATOR IS USED.",
    "MGMT: no significant difference vs lymphoma": "So the HS lines are NOT MGMT-silenced. Combined "
        "with PMID 26130852 finding MGMT activity in 2 of 5 canine lymphoma lines, the favourable "
        "branch of `mgmt_escape.REFERENCE_CLASSES_DISAGREE` is the less likely one.",
    "TP53 lower, p21waf1 higher": "Reported, not interpreted here.",
}

WHAT_THE_AUTHORS_CONCLUDE = ("Microtubule inhibitors may be considered potential drug candidates "
                             "for the treatment of canine HS.")

THE_TWO_OBJECTIONS_TO_MICROTUBULE_AGENTS = {
    "EFFLUX": "Vincas and taxanes are canonical P-gp substrates and this same paper reports "
        "ABCB1/ABCG2 ELEVATED in these cells. The class that works pharmacodynamically is the class "
        "most likely to be pumped away from the target. NOT FATAL HERE only because the delivery "
        "problem is the one part of this analysis already solved -- intra-arterial infusion past an "
        "opened barrier does not rely on the molecule crossing on its own.",
    "DIVISION-GATED": "Microtubule inhibitors are MITOTIC POISONS. `dormancy` establishes that a "
        "division-gated agent does not reach a cell that has stopped dividing. A microtubule agent "
        "therefore CANNOT be the whole regimen -- the persister escape needs a non-division-gated "
        "partner, exactly as it did before.",
}

WHAT_THIS_MODULE_ESTABLISHES = (
    "THE MOST DISEASE-SPECIFIC PHARMACOLOGY IN THIS PROJECT SAYS THE ALKYLATOR CLASS IS THE WRONG "
    "CLASS. Not the wrong lesion within the class -- the class.",
    "IT FALSIFIES THE CARBOPLATIN SWAP. Melphalan is an N7 crosslinker and this tumour resists it "
    "42-411x, so escaping MGMT's substrate does not escape the resistance.",
    "IT WAS FOUND LAST, WHILE ANSWERING A QUESTION ABOUT WHETHER ANYONE ELSE WAS WORKING ON THIS. "
    "Right species, right disease, published, and consulted after two regimens had been built.",
    "THE DELIVERY HALF SURVIVES INTACT. The route is independent of what it carries.",
    "MICROTUBULE INHIBITORS ARE THE SIGNAL, at concentrations five orders of magnitude below what "
    "the alkylators need -- and they are division-gated, so they cannot cover the persister alone.",
)
