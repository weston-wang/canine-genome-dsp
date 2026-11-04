"""The THERAPY-MODALITY UNIVERSE for primary intracranial canine HS, enumerated before any claim of closure.

WHY THIS MODULE EXISTS
----------------------
`CLAUDE.md` rule 9: before any "closed / found / complete" claim, enumerate the candidate universe
and record, for every modality class, whether it is in the model, evaluated and excluded with a
reason, or not yet assessed. The rule exists because of a real failure -- the lymphoma
closing-combination was reported as "found" over a catalogue that had no vaccine and no
stem-cell/transplant arm, and the user had to point that out.

The HS work had the same hole. `core.catalogue` holds sixteen agents, and the coverage claim was
always phrased as if the agent list were the universe. It is not: the list was assembled escape by
escape, so a modality that no enumerated escape happened to call for was never considered at all.
This module fixes that by starting from the MODALITY CLASSES rather than from the escapes.

WHAT RULE 13 CHANGED IN THIS MODULE, AND IT IS NOT COSMETIC
-----------------------------------------------------------
`CLAUDE.md` rule 13:

    "A class (vaccine, engager, inhibitor, transplant, cell therapy) is excluded only because its
     kill is contradicted, it is defeated by a named escape, or its toxicity cannot be afforded,
     NEVER because canine data are absent; when canine data are absent, derive a graded TRANSFER or
     OUTCOME-calibrated input and test with it."

Five of this module's ten exclusions were stated in terms the rule forbids -- "not obtainable for a
dog", "no canine-HS activity data", "no canine product exists", "in-vitro only", "unmeasured in
dogs". Those are statements about the literature, not about the therapy, and under the user's own
standard ("I'm okay with no specific data but if scientifically sound") they are not grounds at all.
Every exclusion now carries an `ExclusionGround` from the rule's closed list, and `_validate()`
rejects an EXCLUDED class that has none. Where the old wording was the only ground, a transfer was
derived and tested instead:

  * CSF1R -- re-grounded on DEFEATED_BY_ESCAPE. CSF1R-independence is OBSERVED as acquired resistance
    in human histiocytosis, so the class loses durability to a named escape rather than to missing
    canine data. Availability is recorded separately and is no longer a reason.
  * EPIGENETIC (HDAC/BET) -- re-grounded on TOXICITY_UNAFFORDABLE, and the arithmetic is now computed
    rather than asserted: see `epigenetic_toxicity_arithmetic()`, which reads the live marrow
    headroom out of `core.toxicity` and compares it with the class's transferred marrow burden.
  * BISPECIFIC ENGAGERS -- re-grounded on DEFEATED_BY_ESCAPE (the tumour is the antigen-presenting
    lineage itself, and it exports an immunosuppressive metabolite -- escape_audit.A16).
  * ONCOLYTIC VIROTHERAPY -- re-grounded on DEFEATED_BY_ESCAPE: it must be injected into a lesion
    that is already known, so the second-primary route (a new tumour from the same germline lesion,
    elsewhere) is untouched -- and that route is the one the decade turns on.
  * METABOLIC / DIETARY -- re-grounded on TOXICITY_UNAFFORDABLE: years of methionine restriction in
    an older large-breed dog costs lean mass, which is a toxicity statement, not a data statement.

Availability is now a SEPARATE AXIS from status, because rule 13 forbids conflating them. A class
can be in the model and still need an agent that does not exist for dogs (that is tiered and
reported in `availability_tiers.py`), and a class can be excluded on biology while being perfectly
obtainable (marrow transplant is established in dogs; it is excluded anyway).

THE CASE, STATED SO SCOPE IS NOT DRIFTED
----------------------------------------
Primary intracranial (non-disseminated) histiocytic sarcoma in a predisposed breed: an extra-axial,
meninges-based mass that invades brain tissue and seeds the leptomeninges, in a host carrying a
germline MTAP/CDKN2A-locus predisposition, treated with the intent of indefinite maintenance.

WHAT THE ENUMERATION CHANGED
----------------------------
Three classes were NOT_ASSESSED before this module and are now assessed:

  * ANTIBODY-DRUG CONJUGATES -- excluded on delivery arithmetic, not on hand-waving: antibody access
    to invaded parenchyma is 0.001 in this project's own compartment model (``core.catalogue``), so
    an ADC is three orders of magnitude short at the one site that forced the whole local-delivery
    programme. Keeps a real role at the blood-side/meningeal compartment.
  * BISPECIFIC T-CELL ENGAGERS -- excluded for this case on two grounds that compound: the same
    antibody-access problem, and the tumour IS an antigen-presenting myeloid cell, so a T-cell
    engager asks T cells to kill the lineage that primes them.
  * HAEMATOPOIETIC STEM-CELL / MARROW TRANSPLANT -- the interesting one, and the reason this module
    matters. It is established in dogs (autologous and allogeneic PBSC transplant for lymphoma, with
    total-body irradiation) so it is not infeasible. But resident microglia are YOLK-SAC-DERIVED and
    self-renewing (PMID 20966214), not marrow-derived, so replacing the marrow does not replace the
    cell of origin of a brain-resident histiocytic tumour. It is excluded on BIOLOGY rather than on
    feasibility -- and that is a much stronger exclusion than "not available for dogs".

ONCOLYTIC VIROTHERAPY was mentioned in the report but never assessed; it is now assessed.

TWO MORE CLASSES WERE MISSING, FOUND 2026-11-01, AND ONE OF THEM IS STILL OPEN
------------------------------------------------------------------------------
The catalogue reached "26 classes, 0 unassessed" and that line was published. A second-pass
literature sweep found two classes that had never been rows at all:

  * ANTIMETABOLITES / NUCLEOSIDE ANALOGUES -- the hole that matters. Cytotoxics were split into
    microtubule agents and alkylators and the enumeration stopped there, while
    `core.hs_drug_sensitivity.DrugClass` carried an ANTIMETABOLITE member with no drug under it.
    Three members (5-fluorouracil, clofarabine, floxuridine) are measured active in ALL TEN canine
    HS lines, and clofarabine additionally holds the only durability readout in this project from a
    histiocytic neoplasm (2-year PFS 89% in relapsed/refractory LCH). It is NOT excludable: at the
    intracranial site the members split the three legs -- 5-FU has the quantified canine potency and
    causes cerebral vacuolation in beagles, clofarabine has potency plus the outcome but 5% CSF
    penetration, cytarabine has a measured canine CSF:plasma of 0.62 with an unconfirmed kill. So it
    sat in KNOWN_OPEN_CLASSES and the claim became "28 classes, 1 open" -- for one day. See the
    next section: it is now EXCLUDED, and a third hole took its place in that list.
  * FGFR AXIS -- every other targeted axis had its own row; this one did not, although three FGFR
    inhibitors score in the canine screen and two are licensed. It is EXCLUDED on measured data at
    the right site: infigratinib's phase 2 in FGFR-altered recurrent glioma gave 6-month PFS 16%
    and ORR 3.8%, with every durable responder carrying an activating FGFR point mutation or fusion
    -- a biomarker canine HS is not reported to have, it being an overexpression tumour.

The lesson is about the ENUMERATION PROCEDURE, not about these two drugs: both holes were at a
level of granularity the table itself uses everywhere else (per-chemotype for cytotoxics,
per-axis for targeted agents), and a count of "0 unassessed" says nothing about rows that were
never written. Rule 9's candidate list has to be rebuilt from the literature each time, which is
exactly what the rule says and what had stopped happening.

THEN A THIRD HOLE, 2026-11-02 -- AND THE ANTIMETABOLITE CLASS CLOSED THE SAME DAY
---------------------------------------------------------------------------------
The count is now 29 classes: 15 in the model, 13 excluded, 1 open. Two things moved at once.

  * ANTIMETABOLITES CLOSED, on KILL_CONTRADICTED, and the measurements that closed them were
    ALREADY CITED BY THIS PROJECT. `core.hs_drug_sensitivity` is built from PMID 25715778 and had
    transcribed FIVE of that paper's TEN rows; the five dropped rows include methotrexate and
    cytarabine. So when this module recorded the class as open on 2026-11-01, and explained the
    empty `DrugClass.ANTIMETABOLITE` member as "the paper tested no antimetabolite", both the
    opening and the explanation were wrong against a table one function call away. Cytarabine is
    measured at 38.2-583.8 uM in canine HS against its own measured canine CSF steady state of
    8.3 uM; methotrexate at 69.7x to >14,000x the chemosensitive comparator; and cladribine, from a
    second laboratory, at 64-222 uM against 0.028 uM achievable plasma (PMID 29490634). All ten rows
    are now in the table, and `resistant_classes()` now reproduces the 2015 authors' own sentence as
    a computation.
  * TARGETED PROTEIN DEGRADATION OPENED -- cereblon molecular glues, which no row covered. A
    licensed member has a phase 2 with POSTED RESULTS in a cohort including histiocytic sarcoma
    (NCT02523040: ORR 0.67, 12-month PFS 62%, OS 92%), so it cannot be dismissed; and its measured
    human CSF:plasma of 1.3-2.4% straddles this project's CSF requirement while falling 8-15x short
    at the parenchyma, so it cannot be called closed either.

THEN SEVEN MORE, 2026-11-03, WHEN THE COMPLETENESS CRITIC FINALLY RAN
---------------------------------------------------------------------
The count is now 36 classes: 15 in the model, 15 excluded, 6 OPEN. The critic had been planned as a
phase of the sweep, failed twice on usage limits, and was then deferred on the argument that it
"should not be self-assessed by the thread that built the list". That argument was wrong -- it is a
quality preference, not a reason to leave a step unrun -- and running it changed the headline more
than anything else in the exercise.

WHAT MADE IT WORK WAS THE SOURCE OF THE LIST, not the diligence of the reader. Instead of re-reading
this catalogue and asking "what is missing", the class list was rebuilt from an EXTERNAL taxonomy --
ATC L01, the WHO's antineoplastic classification -- and from the drug classes represented in the
2026 canine screen's own pan-active table. Diffing those against the 29 rows found seven classes
with no row at all, every one of them represented among the compounds that reduced viable cell
counts to <=70% at 5 uM in ALL TEN canine HS lines:

  * TOPOISOMERASE INHIBITORS (ATC L01CB/L01CE) -- EXCLUDED on DEFEATED_BY_ESCAPE. And note what this
    one exposes: `core.hs_drug_sensitivity.DrugClass` has carried a TOPOISOMERASE member all along,
    and `resistant_classes()` has been RETURNING it since the table was completed, while the
    catalogue had no such class. The same empty-container failure as the antimetabolites, inverted:
    the data was present and the row was not.
  * CYTOTOXIC ANTIBIOTICS / ANTHRACYCLINES (ATC L01D) -- EXCLUDED on TOXICITY_UNAFFORDABLE, and the
    surprise of the diff, because the potency does NOT fail: doxorubicin's canine-HS IC50 of
    0.175-0.631 uM sits BELOW a measured achievable canine plasma of 1.13 uM. A catalogue that never
    listed anthracyclines was hiding the best cytotoxic potency-to-exposure ratio in the project
    after the vincas. The cumulative cardiac ceiling is what excludes it, on the same argument
    already used against the alkylators' dose caps.
  * NUCLEAR EXPORT INHIBITION (XPO1 / SINE) -- OPEN, and the most consequential hole of the whole
    exercise, because the class contains a CANINE-LICENSED, ORALLY DOSED, INDEFINITELY SCHEDULED
    agent: verdinexor (Laverdia-CA1). Rule 1 found the pharmacology already done on a SIBLING BRANCH
    of this same project, and CLAUDE.md failure 11 is itself about this drug pair -- so the class had
    been discussed in this project and never enumerated in this case's universe.
  * PROTEASOME INHIBITION (ATC L01XG) -- OPEN. Two members pan-active; ixazomib is oral.
  * HSP90 INHIBITION, CARDIAC GLYCOSIDES, TRANSLATION-ELONGATION INHIBITION -- OPEN, on weaker
    evidence, and recorded anyway because rule 9 asks every class to carry a status rather than
    asking for the convincing ones to be listed. Each says plainly what it lacks.

AND A SECOND TAXONOMY, BECAUSE THE FIRST ONE IS USED UP (same day)
-----------------------------------------------------------------
ATC L01 is a CHEMICAL taxonomy, so diffing against it again would re-ask the same question. The
second diff used a BIOLOGICAL one -- the Hanahan hallmarks therapeutic map, one column per hallmark
-- plus the ATC branches L02/L03/L04 that the first pass never touched. Count: 39 classes,
15 / 16 / 8 open. Three more rows, and the middle one is not bookkeeping:

  * ANTI-ANGIOGENIC / VEGFR-AXIS ("inducing or accessing vasculature") -- EXCLUDED on
    KILL_CONTRADICTED. Rule 1 first: both members were ALREADY assessed as agents in `therapies.py`
    (toceranib carries CONSIDERED_UNMEASURED with a negative canine efficacy readout), so the
    science was examined and only the class row was missing. What this adds is the arithmetic that
    replaces a "likely penetrates the CNS poorly": toceranib 1.7-1.9 uM and sunitinib 4.5-17.9 uM
    against achievable canine plasma of 0.1 and 0.12 uM, and the screen's own unused headline of
    sunitinib median 608 nM -- 5x above achievable even at its most favourable.
  * APOPTOSIS INDUCTION / BH3 MIMETICS ("resisting cell death") -- OPEN, and it exposes an error of
    exactly the shape rule 15 names. `therapies.py` rejected navitoclax because its on-target
    thrombocytopenia stacks with lomustine, and that reasoning then stood for the whole mechanism.
    But navitoclax's thrombocytopenia IS BCL-XL inhibition, and VENETOCLAX WAS ENGINEERED TO SPARE
    BCL-XL -- which is why it reached licensure where navitoclax did not. The class was set aside on
    a liability its leading member is designed not to have, and venetoclax appears NOWHERE in this
    repository. It is licensed, oral and dosed continuously to progression, which is the schedule
    C3 demands.
  * IL-1 BLOCKADE AS A TOLERABILITY ENABLER ("tumour-promoting inflammation") -- OPEN, enumerated on
    the model of the `molecular surveillance` row: not a therapy, but in the catalogue because the
    plan's deliverability depends on it. Anakinra went with 18-month retention of 94% vs 65% in ECD,
    as an association in a retrospective series of 16 anakinra courses out of 60.

Two hallmark columns were considered and judged NOT to meet rule 9's "could plausibly matter" bar --
differentiation therapy and microbiome modulation -- and that judgement is written down next to
KNOWN_OPEN_CLASSES rather than left as a silent omission.

A THIRD TAXONOMY, AND THE RESULT THAT MATTERS MORE THAN THE CLASSES (same day)
-----------------------------------------------------------------------------
Third axis: molecular TARGET CLASS -- nuclear receptors, protein-protein interactions, nucleic acid
as target, ion channels, proteases -- orthogonal to both the chemical list and the biological map.
Count: 42 classes, 15 / 16 / 11 open. Three more rows:

  * GLUCOCORTICOID-RECEPTOR AGONISTS -- OPEN, and the most embarrassing hole of the eleven. The words
    `prednisone`, `prednisolone` and `glucocorticoid` appeared NOWHERE in this repository. The
    cheapest, most available, most routinely dosed class in veterinary oncology -- licensed for dogs,
    oral, indefinitely dosable, already given to a dog with this presentation for peritumoural oedema
    -- was absent from a catalogue reporting "0 unassessed". Nobody in this project has ever looked
    for a glucocorticoid potency in canine HS, which is a trivial assay on cells that already exist.
  * MDM2-p53 -- OPEN. The project had already NAMED the lesion (low TP53 expression in the HS lines;
    TP53 variants in 4/7 corgi cases, both recorded in other modules) and never enumerated the class
    that targets it. Gated on a p53 state the project has never resolved.
  * NUCLEIC-ACID THERAPEUTICS -- OPEN, ranked last, and clearing the plausibility bar on DELIVERY
    (intrathecal ASO has a licensed precedent and this model already has an intrathecal arm) rather
    than on any oncology evidence.

THE RESULT: THREE AXES, THREE SETS OF FINDS, NO CONVERGENCE -- AND THAT BOUNDS THE CLAIM
----------------------------------------------------------------------------------------
ATC L01 added seven. The hallmarks map added three. Target class added three more. Each independent
external axis found classes the previous ones missed, and the third found as many as the second. So
the honest conclusion is NOT "the catalogue is now complete". It is this:

    "Modality class" has no canonical granularity, so the denominator of any closure claim is
    AXIS-DEPENDENT. A claim of the form "closed within a catalogue of N classes" is only as
    meaningful as the list of axes the catalogue was built from -- which is why those axes are
    now named in the record (chemical/ATC L01 + L02-L04; biological/Hanahan hallmarks; molecular
    target class) and why the next thread should add a fourth rather than re-run one of these.

That is a weaker claim than this module used to make, and it is the correct one. The guard
`_validate()` still cannot see a row nobody wrote; what has changed is that the record now says so
and names what was checked instead of implying the enumeration terminated.

READING THE ELEVEN OPEN CLASSES, because one number hides a real distinction
---------------------------------------------------------------------------
`open_with_canine_hs_evidence()` returns FIVE (XPO1, proteasome, HSP90, cardiac glycosides,
translation elongation) -- each with a measurement in canine HS, all from the 2026 screen's
pan-active table, and these are the ones worth working up first. `open_without_canine_hs_evidence()`
returns SIX (cereblon degraders, glucocorticoids, MDM2-p53, nucleic-acid therapeutics, BH3 mimetics,
IL-1 blockade) -- nothing in this disease at all. Being in the second list is NOT a rule-13 ground
for exclusion and NOT a rule-11 gap to report; it is a statement about where to look next. Quoting
"11 open" without that split invites a reader to treat a pan-active screen hit and an unsearched
mechanism as the same kind of thing.

Two of the eight open classes carry an explicit refusal to assert the obvious: no CNS figure is
claimed for the proteasome inhibitors, and no achievable-exposure arithmetic is claimed for the
cardiac glycosides, because neither was fetched. Under rule 16 an unsourced explanation is how a
class gets wrongly graded, and the general belief about bortezomib's CNS penetration or digoxin's
nanomolar therapeutic range is not a source.

THE PROCEDURAL FINDING, WHICH IS WORTH MORE THAN ANY OF THE THREE CLASSES
------------------------------------------------------------------------
Three holes in three days, in a catalogue that had reported "0 unassessed" for weeks. Each was found
by rebuilding the class list from the literature, and none by auditing the existing list against
itself. A guard that checks every enumerated class is sound and says nothing at all about the
classes nobody enumerated; `_validate()` cannot see a missing row. The second lesson is narrower and
sharper: an EMPTY CONTAINER in the model -- a declared enum member with no data, a class with no
agent -- is indistinguishable from an absent measurement, and the cheap move is to explain the
emptiness from memory. Re-read the source instead. That is CLAUDE.md failure 12 / rule 16, and it
cost a day here.

THE HONEST EFFECT ON THE HEADLINE
---------------------------------
Enumerating the universe does not add a drug to the regimen. It converts "every escape is closed"
from a claim over an unstated list into a claim over a STATED one: closed within this catalogue of
N modality classes and M escapes, with the excluded classes named and the ground for each recorded.
That is the claim ``statement()`` returns. Rule 13 then adds a second axis to the same claim: of the
classes in the model, how many are available today -- which is what `availability_tiers.py` reports.

This is an analysis, not veterinary advice.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Status(Enum):
    """Rule-9 status of a modality class for this case."""

    IN_MODEL = "represented by at least one agent in the model"
    EXCLUDED = "evaluated and excluded, with the reason recorded"
    NOT_ASSESSED = "not yet assessed -- an open hole in the catalogue"


class ExclusionGround(Enum):
    """The ONLY admissible grounds for excluding a class (CLAUDE.md rule 13).

    Absence of canine data is deliberately not on this list. It was the stated ground for five of
    the exclusions here before rule 13, and it is a statement about the literature rather than about
    the therapy -- which the user's standard ("I'm okay with no specific data but if scientifically
    sound") rules out as a reason to drop anything.
    """

    KILL_CONTRADICTED = (
        "measured or derived evidence contradicts a durable kill in this disease at this site"
    )
    DEFEATED_BY_ESCAPE = (
        "a named escape route in the ledger defeats the class, so it cannot hold for a decade"
    )
    TOXICITY_UNAFFORDABLE = (
        "the class's burden exceeds the remaining headroom on an axis the regimen already loads"
    )


class Availability(Enum):
    """Rule-13 tier. Orthogonal to Status: a class can be in the model and not yet exist for dogs.

    The user corrected this scale on 2026-10-02: *"I don't mean you can only use therapies that
    exist today, I meant to include near future ones that are scientifically sound. Just nothing
    that's pure theoretical."* So TO_BUILD was too coarse -- it lumped a compound in human Phase III
    together with a mechanism nobody has ever dosed. NEAR_FUTURE splits them, and closure may use it.
    The three-part test for NEAR_FUTURE is applied explicitly per agent in
    `availability_tiers.near_future_test()`, not asserted.
    """

    EXISTS_TODAY = "licensed (veterinary or human, off-label), or available through a dog trial"
    NEAR_FUTURE = ("clinical-stage evidence of the modality in humans or dogs, a stated path to the "
                   "dog, and a derived or transferred dose/kill. Counts toward closure.")
    THEORETICAL = ("no clinical evidence of the mechanism anywhere. NEVER counts toward closure.")


@dataclass(frozen=True)
class Modality:
    """One therapy-modality class, with its status, its exclusion ground and its availability tier."""

    name: str
    status: Status
    representative: str          # the agent in the model, or the class member considered
    basis: str                   # why this status -- data, arithmetic, or biology
    canine_hs_evidence: str      # what exists in this disease specifically, if anything
    availability: Availability   # rule 13: exists-today vs to-build, for the representative named
    availability_basis: str      # what makes it obtainable, or what the exists-today substitute is
    exclusion_ground: ExclusionGround | None = None   # required iff status is EXCLUDED


#: Enumerated from the modality list in CLAUDE.md rule 9, plus classes the HS literature names.
UNIVERSE: tuple[Modality, ...] = (
    Modality(
        "cytotoxic chemotherapy -- microtubule agents",
        Status.IN_MODEL,
        "colchicine-site tubulin binder (avanbulin/RGN3067 class); vinca as the measured comparator",
        "The induction backbone, and the only pharmacology in this project measured in the right "
        "species and disease. Carries six of the twelve original escape closures -- a concentration "
        "the escape audit flags as a single point of failure (escape_audit.A13).",
        "MEASURED: 4 canine HS lines, vincristine IC50 1.77-2.69, vinblastine 1.75-2.78, paclitaxel "
        "23.8-58.4 ng/ml (PMID 25715778). Same paper: ABCB1/ABCG2 elevated.",
        Availability.NEAR_FUTURE,
        "THE CLASS EXISTS TODAY; THE AGENT THE CLOSURE USES DOES NOT. Vincristine and vinblastine "
        "are licensed for dogs and carry the measured canine-HS potency, but both are canonical "
        "P-gp substrates against the elevated ABCB1/ABCG2 the same paper reports, so they supply "
        "the class potency and NOT the brain access. The closing agent RGN3067 (efflux ratio 0.61, "
        "oral, brain Cmax 20 uM) is preclinical and rodent-only, PMID 38398008. Sagopilone, the "
        "access exemplar, was not carried forward after its glioma trials. This is the one "
        "load-bearing to-build agent in the regimen -- see availability_tiers.",
    ),
    Modality(
        "cytotoxic chemotherapy -- alkylators / nitrosoureas",
        Status.EXCLUDED,
        "lomustine (CCNU), the veterinary standard of care",
        "DROPPED AS A CLASS, deliberately. Canine HS lines are 134-670x and 42-411x RESISTANT to "
        "alkylators versus microtubule agents (PMID 25715778), and dropping the class also makes "
        "MGMT repair (escape 11) inapplicable. Retained only as the comparator that sets the honest "
        "baseline (568-day median after debulking in localized HS).",
        "MEASURED, and measured UNFAVOURABLE -- the resistance is the finding.",
        Availability.EXISTS_TODAY,
        "Lomustine is the veterinary standard of care for HS and entirely obtainable. Availability "
        "is not the issue; the measured resistance is.",
        ExclusionGround.KILL_CONTRADICTED,
    ),
    Modality(
        "cytotoxic chemotherapy -- antimetabolites / nucleoside analogues",
        Status.EXCLUDED,
        "cytarabine, methotrexate and cladribine (all three measured in canine HS); clofarabine, "
        "5-FU, floxuridine (screen-active, no IC50)",
        "CARRIED OPEN FOR ONE DAY, THEN CLOSED ON 2026-11-02 BY THREE MEASURED IC50s -- two of which "
        "were in a table this project had already half-transcribed, and one in a paper nobody had "
        "read. The class is excluded on KILL_CONTRADICTED, from measurements in the right species "
        "and the right disease, by two independent laboratories:\n"
        "  * CYTARABINE, and this is the decisive row because BOTH sides are measured in the dog. "
        "Canine-HS IC50 38.2 uM in the most sensitive of four lines (9.29 ug/ml, CHS-3) rising to "
        "583.8 uM in DH82 (PMID 25715778 Table 1, 48-h CCK-8), i.e. 101x to 1549x the chemosensitive "
        "canine lymphoma comparator CLBL-1 -- and a correction to that framing, 2026-11-04: Table 1 reports SIX cell lines, and this row cited only CLBL-1 while dropping Ema, the T-cell lymphoma line (cytarabine 736 ng/ml, methotrexate 17.3 ng/ml). CLBL-1 is the MORE SENSITIVE comparator, so quoting it alone MAXIMISES the apparent resistance: against Ema the cytarabine fold is 12.6x rather than 101x. The exclusion does not depend on which comparator is used -- the decisive argument is the IC50 against cytarabine's OWN measured canine CSF concentration, not the fold against any lymphoma line -- but the figure that travels should be the range 12.6-1549x across both comparators, not the single most unfavourable number. Its own measured canine CSF exposure with an INTACT "
        "barrier is 8.3 uM at steady state and 29 uM at the bolus peak (PMID 1742843), so the best "
        "line needs 4.6x the steady state and 1.3x more than even the transient peak. And the canine "
        "toxicity ceiling sits BELOW the dose that produced that peak: fatal suspected "
        "cytarabine-induced infiltrative lung disease in a dog after the fourth 300 mg/m2 infusion, "
        "against the 600 mg/m2 that gave the 29 uM peak (PMID 27062671). Kill, reach and toxicity "
        "are each measured, in the dog, and they do not meet. See "
        "`core.hs_drug_sensitivity.CYTARABINE_CSF_ARITHMETIC`.\n"
        "  * METHOTREXATE: >100 ug/ml in CHS-1 and DH82, 8.56 ug/ml in CHS-2, 495 ng/ml in CHS-3, "
        "against 7.10 ng/ml in CLBL-1 -- 69.7x in the best line and >14,000x in the worst (same "
        "table; the >100 entries are right-censored, so those folds are LOWER BOUNDS).\n"
        "  * CLADRIBINE, from a second laboratory and a second cell-line panel: IC50 64 uM (BD, a "
        "Bernese-derived line) and 222 uM (DH82) against an ACHIEVABLE PLASMA CONCENTRATION of "
        "0.028 uM -- short by 2,286x to 7,929x (PMID 29490634 Table 2, 72-h MTS). That table exists "
        "precisely to compare IC50 with achievable exposure, and dasatinib is the only agent in it "
        "that clears its own bar; cladribine is the worst in the table after CCNU.\n"
        "BOTH PAPERS STATE THE CONCLUSION THEMSELVES, which is why this is not an inference: "
        "PMID 25715778 -- 'it was suggested that alkylating agents, ANTIMETABOLITES, antitumor "
        "antibiotics and topoisomerase inhibitors might not be effective as treatment of HS'. "
        "The completed `hs_drug_sensitivity` table now reproduces that sentence as a computation: "
        "`resistant_classes()` returns the alkylators, the antimetabolites and the topoisomerase "
        "agents, and `sensitive_classes()` returns the microtubule agents alone.\n"
        "THE COUNTER-EVIDENCE, RECORDED AT ITS OWN STRENGTH AND NOT HIDDEN, because it is real and "
        "it is what made this class worth a day's work: in HUMAN histiocytic disease the same drugs "
        "perform well. Methotrexate 1 g/m2 + cytarabine 0.1 g/m2 x5 for six cycles in 95 adults with "
        "newly diagnosed LCH gave ORR 89.5%, 6-year OS 93.2% and EFS 55.2% at a median 78 months' "
        "follow-up -- the LONGEST durability readout anywhere in this project (PMID 39428688) -- and "
        "cladribine + cytarabine produced clinical improvement and radiologic remission in isolated, "
        "MAPK-wild-type CNS Erdheim-Chester disease that had failed steroids, radiotherapy AND "
        "cladribine monotherapy (PMID 42780343, n=1). Under rule 15 neither bounds the canine-HS "
        "kill: they are EFFICACY readouts in a different and far less aggressive disease, and a "
        "transfer from another disease cannot overturn a measurement in this one. Under rule 14 the "
        "measurement in the species and disease at issue outranks the flattering cross-disease "
        "outcome, EVEN THOUGH the measured number is the worse one. So the honest statement is "
        "'these drugs work in LCH and are measured resistant in canine HS', not 'the class works'.\n"
        "WHAT WOULD REOPEN IT -- two obtainable things, and neither is a demonstration: (a) a "
        "CLOFARABINE IC50 in canine HS lines below achievable exposure. Clofarabine is the one "
        "member with pan-activity in all ten lines at 5 uM and no IC50, and rule 15 forbids "
        "transferring cladribine's resistance to it: clofarabine was designed to resist the "
        "deamination that limits cytarabine and cladribine, so the chemistry differs in the "
        "direction that matters and its 2'-fluoro substitution makes it the one member whose "
        "resistance is NOT bounded by the other two. (b) a measured canine-HS uptake or activation "
        "advantage -- deoxycytidine kinase expression, or a nucleoside-transporter level -- that "
        "would explain the cell-line resistance as culture artefact. Absent either, the class stays "
        "excluded.\n"
        "HISTORY, KEPT BECAUSE IT IS THE POINT. The catalogue "
        "split cytotoxics into microtubule agents and alkylators and stopped. Antimetabolites were "
        "never a row -- even though `core.hs_drug_sensitivity.DrugClass` had an ANTIMETABOLITE "
        "member with no drug under it. On 2026-11-01 that empty member was explained here as 'the "
        "paper tested no antimetabolite'. IT HAD TWO ANTIMETABOLITE ROWS; the table had been "
        "transcribed five rows out of ten. The empty member was the signature not of an absent "
        "measurement but of a HALF-COPIED ONE, and the difference is the whole of this entry -- the "
        "numbers that closed the class were already cited by the project, one function call away. "
        "That is CLAUDE.md failure 12 / rule 16. "
        "WHAT THE FIRST DAY'S ASSESSMENT SAID, AND WHERE IT WAS WRONG: it found that at the "
        "INTRACRANIAL site the members split three legs with no single member carrying all of them, "
        "and concluded the class was not excludable. Legs (1) and (2) below stand as written. Leg "
        "(3) was wrong, and it was the leg holding the class open: "
        "(1) POTENCY WITHOUT THE BRAIN -- 5-fluorouracil is pan-active in all 10 lines with a "
        "quantified median IC50 of 7.49 uM, and it is the member this disease should NOT get. "
        "STATED UNDER RULE 15, because the toxicity finding is about a DIFFERENT COMPOUND and must "
        "be transferred with a written direction rather than asserted: what was dosed to beagles "
        "orally for 3 months was FBAL (alpha-fluoro-beta-alanine) and fluoroacetate, 5-FU's "
        "CATABOLITES, with tegafur-uracil as a positive control; all three gave hyperaesthesia, "
        "excitement, CONVULSIONS and VACUOLAR CHANGES IN SEVERAL AREAS OF THE DOG CEREBRUM, and the "
        "authors' stated purpose was to identify which catabolite carries the neurotoxicity of "
        "'5-FU and/or its masked compounds' (PMID 15206584). The DIRECTION is what makes it "
        "transfer: FBAL is the principal catabolite of 5-FU, so FBAL exposure is a consequence of "
        "dosing 5-FU rather than an alternative to it, and a second fluoropyrimidine in the same "
        "pathway (tegafur-uracil) produced the same lesion. What transfers is therefore a "
        "MECHANISM-LEVEL DISQUALIFICATION at this site, dog-specific and cerebrum-specific, and NOT "
        "a measured neurotoxic dose for 5-FU itself -- no number is carried across, and none is "
        "needed, because the conclusion is qualitative. "
        "FLOXURIDINE inherits the concern by the same route and no further: it is a fluoropyrimidine "
        "catabolised through the same DPD pathway to the same FBAL, so the mechanism applies; it was "
        "not dosed in that study, so nothing quantitative transfers to it either. Rule 15 forbids "
        "calling this a contradicted number for floxuridine -- it bounds the class's brain use, it "
        "does not measure it. "
        "(2) POTENCY AND A HISTIOCYTIC OUTCOME, WITHOUT ACCESS -- clofarabine is pan-active in all "
        "10 canine HS lines AND carries the only durability readout any agent in this project has "
        "in a histiocytic neoplasm: prospective phase 2 in relapsed/refractory LCH, 17/20 (85%) "
        "responders, NO on-treatment progression, 2-year PFS 89% +/- 7% and OS 100% (n=20, median "
        "follow-up 40.9 months) after a FINITE six-cycle course, PMID 42126265. DIRECTION OF THAT "
        "TRANSFER, under rule 15: it is an EFFICACY figure, not an exposure one, and it moves across "
        "species and across disease within the histiocytic lineage. LCH is a far less aggressive "
        "neoplasm than histiocytic sarcoma, so an LCH durability number is a CEILING for HS and "
        "never a floor -- it establishes that the class can produce multi-year control in this "
        "lineage, not that it would do so here. Its CSF penetration is separately measured and "
        "modest: median 5% (range 3-26%) in non-human primates, PMID 16115942. That one is an "
        "EXPOSURE figure in a third species, used as an order of magnitude only; no NHP-to-dog "
        "direction is established in this project, so it is not converted into a canine number and "
        "nothing closes on it. "
        "(3) ACCESS WITHOUT A CONFIRMED KILL -- cytarabine is the rule-14 ideal on access and is "
        "measured IN THE DOG WITH AN INTACT BARRIER: CSF:plasma 0.62 +/- 0.14 at steady state on a "
        "12-hour infusion, CSF Css 8.3 +/- 1.1 uM, bolus CSF peak 29 +/- 11 uM, in ten healthy dogs "
        "with no significant toxicity at 600 mg/m2 (PMID 1742843). This is cytarabine's OWN "
        "measurement in the species and compartment at issue -- no transfer at all, which is why it "
        "is the strongest access datum in the project at 0.62 (total, not unbound; the study assayed "
        "drug by HPLC in both fluids). But cytarabine is NOT in the pan-active table: it was a "
        "Group-B-specific CANDIDATE that the authors then rejected on IC50 ('no compound was "
        "identified as Group B-specific'), with >=30% inhibition at 5 uM in 5 of 10 lines. "
        "THE DAY-ONE CONCLUSION WAS THAT ITS KILL WAS THEREFORE 'UNCONFIRMED, NOT CONTRADICTED', "
        "AND THAT IS THE SENTENCE THE NEXT DAY FALSIFIED. Cytarabine's canine-HS IC50 was not "
        "unmeasured -- it was measured in 2015, in the paper that supplies this project's whole "
        "sensitivity table, and the answer is 38.2-583.8 uM against that measured 8.3 uM CSF steady "
        "state. The day-one text also reasoned that '8.3 uM is above the 5 uM at which its own "
        "screen result was obtained, which is why the class is open rather than dead'. That "
        "comparison was legitimate under rule 15 (cytarabine against itself) but it was the WRONG "
        "QUANTITY: a 5 uM screening concentration at which 5 of 10 lines showed >=30% inhibition is "
        "not an IC50, and the IC50 is 4.6x higher than the exposure. Reaching a compartment at a "
        "concentration that inhibits some lines by 30% is not a kill. "
        "The lesson generalises past this class: a screening threshold is a lower bound on potency "
        "and must never be read as a potency when the real IC50 is obtainable.",
        "MEASURED, in ten canine HS lines, for three members. Table 2 of PMID 42129963 -- the "
        "compounds that reduced viable cell counts to <=70% at 5 uM in ALL CHS lines with "
        "reproducibility -- contains 5-FLUOROURACIL, CLOFARABINE and FLOXURIDINE. The same paper "
        "lists METHOTREXATE among the drugs it excluded from screening a priori 'because they had "
        "been previously reported to have antiproliferative effects on CHS cells and cases'. "
        "MISREAD ON 2026-11-01 AS 'the class has prior-literature activity in this disease as well'. "
        "It does not say that. MELPHALAN is on the same exclusion list and melphalan is measured "
        "42-411x RESISTANT in these lines, so the phrase means 'already studied', not 'found "
        "active' -- and the prior report for methotrexate is the 2015 paper, which measures it "
        "69.7x to >14,000x resistant. Its racemate (amethopterin) and TRIMETREXATE, ANCITABINE, "
        "CYTARABINE and 5-fluoro-5'-deoxyuridine all appear among the 19 Group-B candidates, i.e. "
        "five of those nineteen are antimetabolites, but the authors confirmed NONE of them on IC50. "
        "Trimetrexate had low IC50 in 8 of 10 lines, which the authors note but did not pursue, and "
        "which is the one screen-level signal in the class that nobody has followed up. "
        "DECISIVE, AND FROM TWO LABORATORIES: PMID 25715778 Table 1 gives cytarabine 9.29-142 ug/ml "
        "and methotrexate 495 ng/ml->100 ug/ml across four lines against a 7.10-91.7 ng/ml "
        "chemosensitive comparator; PMID 29490634 Table 2 gives cladribine 64 and 222 uM against "
        "0.028 uM achievable plasma. All ten rows of the 2015 table are now in "
        "`core.hs_drug_sensitivity`, where they were five.",
        Availability.EXISTS_TODAY,
        "Every member is obtainable today, verified at openFDA on 2026-11-01: clofarabine is "
        "marketed as generics (ANDA 209775 MSN, ANDA 205375 Dr Reddy's, ANDA 216233 ScinoPharm) "
        "although the CLOLAR brand, NDA 021673 Genzyme, is discontinued; cytarabine is marketed by "
        "several holders (ANDA 072168 Hospira, ANDA 074245 West-Ward, ANDA 205696/208485 Meitheal) "
        "while DEPOCYT, NDA 021041 Pacira, is discontinued -- which independently confirms this "
        "project's existing statement that the sustained-release intrathecal product is gone; "
        "5-fluorouracil is generic and ancient. Availability was never the issue, which is why this "
        "exclusion is a scientific one: three measured IC50s, two laboratories, one of them against "
        "a measured canine CSF concentration and a measured canine toxicity ceiling.",
        ExclusionGround.KILL_CONTRADICTED,
    ),
    Modality(
        "targeted protein degradation / cereblon modulators (immunomodulatory imides, CELMoDs)",
        Status.NOT_ASSESSED,
        "lenalidomide (licensed, and the member with a histiocytic trial); pomalidomide (the member "
        "for a brain site)",
        "THE THIRD RULE-9 HOLE, FOUND 2026-11-02, and the reason the catalogue is now 29 classes "
        "rather than 28. Targeted protein degradation -- molecular glues acting through the CRL4-CRBN "
        "E3 ligase -- is a distinct modality in any modern catalogue, and it was not a row. It is not "
        "a kinase inhibitor, not an epigenetic agent, and not a checkpoint or cytokine agent, so no "
        "existing row covers it. The only trace in the project was a parenthetical note in "
        "`maintenance_durability` that PRMT5 PROTAC degraders are 'emerging', which is a remark about "
        "a future agent on another axis, not an enumerated class.\n"
        "WHY IT CANNOT BE DISMISSED: there is a registered PHASE 2 of a licensed degrader in this "
        "disease family, WITH POSTED RESULTS. NCT02523040, 'Lenalidomide for Adult Histiocyte "
        "Disorders', phase 2, n=12 actual, conditions Langerhans cell histiocytosis, Erdheim-Chester "
        "disease AND HISTIOCYTIC SARCOMA, results first posted 2025-04-25: overall response rate "
        "0.67, 12-month progression-free survival 62%, 12-month overall survival 92%, grade 3-4 "
        "treatment-related toxicity 0.25, and a pharmacodynamic readout (serum TNF-alpha maximum "
        "change -14.4%). Under rule 13 a licensed agent with a human outcome calibration in the "
        "right disease family is a sound input, so absent canine data is not a ground.\n"
        "WHY IT CANNOT BE CALLED IN-MODEL EITHER, which is the honest reason it sits open: no agent "
        "of the class is wired into the regimen, there is no canine-HS potency for any member, and "
        "the brain arithmetic for the member that has the trial does not close. Rule 14's proxy for "
        "'reaches the brain' is a measured CSF:plasma ratio, and it exists TWICE for lenalidomide, "
        "which is exactly the case rule 14 legislates for: non-human primates give CSF penetration "
        "11% (AUC CSF/AUC plasma, detected in 2 of 3 animals, PMID 22109830), while THREE HUMAN "
        "PATIENTS give CSF:plasma 1.3-2.4% (PMID 35732975). Rule 14 says prefer the measurement in "
        "the compartment at issue even when it is the worse number, so this project uses 1.3-2.4%, "
        "not 11%. Against the requirements this project computes -- 0.0145 in CSF and 0.196 in "
        "parenchyma -- that STRADDLES the CSF bar (0.013 just under, 0.024 clearing it by 1.7x) and "
        "falls 8-15x SHORT at the parenchyma. The parenchymal site is the one the case turns on, so "
        "the class does not close the brain today.\n"
        "THE MECHANISM IS KNOWN, AND IT NAMES THE NEXT STEP UNDER RULE 15. The same paper that "
        "measured the human ratio also measured why it is low: lenalidomide's influx permeability in "
        "a monkey blood-brain-barrier model and in human placental cells is ONE ORDER OF MAGNITUDE "
        "BELOW thalidomide, pomalidomide and a caffeine positive control, and the authors conclude "
        "lenalidomide 'exerts its favorable immunomodulatory effects via systemic exposures'. That "
        "is a within-class, same-assay permeability comparison, so it transfers as a DIRECTION and "
        "not as a number: POMALIDOMIDE is the class member to take to a brain site, and thalidomide "
        "is measured at 42% CSF penetration in the NHP study. Rule 15 forbids attaching "
        "pomalidomide's permeability to lenalidomide's trial result or vice versa -- the trial is an "
        "EFFICACY readout for lenalidomide, the permeability is an EXPOSURE property of pomalidomide, "
        "and they are different quantities about different compounds.\n"
        "THE SEARCH FOR THAT NUMBER FOUND SOMETHING THAT OUTRANKS IT, 2026-11-03. Rule 14 asks for "
        "the measurable proxy; the proxy for 'does this class work behind an intact barrier' is not "
        "only a CSF ratio but a RESPONSE RATE IN A PRIMARY CNS TUMOUR, and that is measured. "
        "NCT01722305, phase 1 of POMALIDOMIDE plus dexamethasone in relapsed/refractory PRIMARY CNS "
        "lymphoma and primary vitreoretinal lymphoma (PMID 30262659, Blood 2018): MTD of "
        "pomalidomide 5 mg daily for 21 of 28 days; 25 of 29 patients evaluable at a median of "
        "THREE prior treatments; WHOLE-STUDY ORR 48% (12/25, 95% CI 27.8-68.7) with SIX COMPLETE "
        "RESPONSES, 2 CRu and 4 PR; MTD-cohort ORR 50% (8/16) with 5 CR; median PFS 5.3 months "
        "whole-study and 9 months among responders. Grade 3/4 neutropenia 21%, lung infection 12%, "
        "respiratory failure 8%. The authors conclude 'significant therapeutic activity against "
        "relapsed/refractory PCNSL'. "
        "WHY THIS IS STRONGER THAN THE RATIO IT REPLACES: a COMPLETE RESPONSE in a tumour that is "
        "primary to the central nervous system is the most direct evidence obtainable that a drug "
        "both reaches and kills behind an intact barrier -- it outranks any CSF:plasma figure under "
        "rule 14's own ordering, because it is an outcome measured in the compartment at issue "
        "rather than an inference into it. And it lands on exactly the member the permeability "
        "comparison predicted: pomalidomide, measured an order of magnitude more permeable than "
        "lenalidomide in the same assay. The within-class direction was right.\n"
        "SO THE QUESTION THIS CLASS FACES HAS CHANGED, and the class stays open for a different and "
        "narrower reason than yesterday. It is no longer 'can a cereblon degrader reach and kill in "
        "the brain' -- a licensed one produces complete responses in a primary CNS tumour. It is now "
        "(a) what is the KILL RATE in this tumour, there being no canine-HS potency for any member, "
        "and (b) does it FIT THE TOXICITY BUDGET, given 21% grade 3/4 neutropenia against a marrow "
        "axis this regimen already loads to 95%. Those are the two inputs the project's machinery "
        "requires before an arm is wired in, and neither is a demonstration -- a transferred potency "
        "and a computed budget would satisfy both. "
        "SCOPE, so this is not overread: PCNSL is a LYMPHOMA, not a histiocytic neoplasm, so it is "
        "indirect on disease even while being direct on SITE; it is human; the patients were "
        "relapsed/refractory at a median of three prior lines; and pomalidomide was given WITH "
        "DEXAMETHASONE, which has activity of its own in PCNSL, so the 48% is a combination result "
        "and may not be attributed to the degrader alone.",
        "NONE IN THIS DISEASE AND NONE IN THE DOG. The canine side of this class is empty: no "
        "canine-HS IC50 for any degrader, no canine PK for lenalidomide or pomalidomide, no dog "
        "trial. Under rule 13 that is not a ground for exclusion, and under rule 11 it is not a gap "
        "to report -- it is the reason the class is graded on a human outcome transfer (NCT02523040) "
        "and a human exposure measurement (PMID 35732975) instead.",
        Availability.EXISTS_TODAY,
        "Lenalidomide, thalidomide and pomalidomide are all human-licensed and obtainable off-label; "
        "the histiocytic trial used lenalidomide orally, days 1-21 of a 28-day cycle, up to 12 "
        "cycles, which is a continuous-enough schedule to satisfy condition C3 unlike the weekly "
        "agents. The newer CELMoDs (mezigdomide, golcadomide, iberdomide) are clinical-stage rather "
        "than licensed and would be NEAR_FUTURE if the class were taken forward on one of them.",
    ),
    Modality(
        "glucocorticoid-receptor agonists (corticosteroids)",
        Status.NOT_ASSESSED,
        "prednisone / prednisolone (licensed for dogs, oral, indefinitely dosable); dexamethasone",
        "FOUND MISSING 2026-11-03 BY THE THIRD TAXONOMY DIFF (molecular TARGET CLASS -- nuclear "
        "receptors -- an axis orthogonal to both the chemical ATC list and the biological hallmarks "
        "map). THIS IS THE MOST EMBARRASSING HOLE OF THE TEN, and it is worth saying so plainly: "
        "`prednisone`, `prednisolone` and `glucocorticoid` appear NOWHERE in this repository -- not "
        "in the catalogue, not in `therapies.py`, not in the docs. The single most obtainable, "
        "cheapest, most routinely used drug class in veterinary oncology was absent from a catalogue "
        "that reported '0 unassessed' for weeks.\n"
        "WHAT IT HAS, and it is formidable on every axis this project usually complains about: "
        "licensed for dogs, ORAL, dosable INDEFINITELY (so condition C3 is satisfied trivially, "
        "where most of this catalogue's agents fail on schedule), decades of canine dosing "
        "experience, and standard first-line use in the human histiocytoses this project transfers "
        "from. Dexamethasone is additionally standard for peritumoural oedema in brain tumours, so "
        "it is already the drug a dog with this presentation would receive.\n"
        "WHAT ARGUES AGAINST IT, stated at the strength the evidence actually has: (1) a NEGATIVE in "
        "the right disease family at the right site, n=1 -- the isolated CNS Erdheim-Chester case "
        "verified in this session was 'refractory to CORTICOSTEROIDS, radiotherapy, and cladribine "
        "monotherapy' before the cladribine-cytarabine combination worked (PMID 42780343). Steroids "
        "were tried first and failed. (2) Mechanistically, glucocorticoid cytotoxicity is a LYMPHOID "
        "lineage property; histiocytic and myeloid tumours are not steroid-sensitive in the way "
        "lymphoma is, and in the histiocytoses steroids function largely as anti-inflammatory and "
        "supportive therapy rather than as cytoreduction. (3) ANTAGONISM WITH THIS MODEL'S IMMUNE "
        "ARMS: the regimen carries anti-PD-1 (gilvetmab), a vaccine arm and CD47 blockade, and "
        "sustained glucocorticoid exposure is immunosuppressive. That is a real interaction cost and "
        "it is NOT one of rule 13's three grounds, so it cannot be used to exclude the class -- it is "
        "a quantity someone has to put a number on.\n"
        "WHY IT IS OPEN RATHER THAN EXCLUDED: none of the three arguments above is an admissible "
        "ground. An n=1 refractory case is not a contradicted kill; 'this lineage is usually not "
        "sensitive' is a mechanism expectation and not a measurement in canine HS; and immune "
        "antagonism is an interaction, not a toxicity budget. WHAT WOULD SETTLE IT: a glucocorticoid "
        "IC50 in canine HS lines -- which is a trivial assay on cells that already exist and which, "
        "remarkably, nobody in this project has looked for -- plus a quantified immune-arm "
        "interaction if it survives that.",
        "NONE, and that absence is itself the finding: this project has never searched for a "
        "glucocorticoid potency in canine HS. Dexamethasone appears in the record only as the "
        "CO-DOSED agent in the pomalidomide primary-CNS-lymphoma trial (which is why that trial's "
        "48% response rate is a combination result and not attributable to the degrader alone), and "
        "corticosteroids appear only as the therapy the CNS Erdheim-Chester case had already failed.",
        Availability.EXISTS_TODAY,
        "The most available class in the entire catalogue: licensed for dogs, oral, pennies per dose, "
        "indefinitely dosable, and already in routine use for the peritumoural oedema this "
        "presentation causes. Availability could not be less of an obstacle, which is exactly why "
        "the missing potency measurement is the whole question.",
    ),
    Modality(
        "MDM2-p53 interaction inhibition",
        Status.NOT_ASSESSED,
        "idasanutlin, milademetan, navtemadlin (clinical-stage); nutlin-3a as the tool compound",
        "FOUND MISSING 2026-11-03 by the same target-class diff (protein-protein interaction). The "
        "catalogue had no p53-directed class -- although p53 IS ALREADY NAMED IN THIS PROJECT AS A "
        "RESISTANCE MECHANISM: `core.hs_drug_sensitivity` records the 2015 authors' conclusion that "
        "'the low expression level of TP53 in HS cell lines might play a role in the resistance "
        "against a diverse range of chemotherapeutic agents', and TP53 variants are recorded in 4 of "
        "7 corgi HS cases. So the project identified the lesion and never enumerated the class that "
        "targets it.\n"
        "THE GATE, WHICH IS WHY THIS IS NOT A SIMPLE ADDITION: MDM2 inhibitors work by blocking the "
        "degradation of WILD-TYPE p53. They are useless, and potentially counterproductive, where "
        "p53 is mutated. The record carries BOTH states for this disease -- LOW EXPRESSION in the "
        "cell lines (which is compatible with wild-type protein and would be the favourable case) "
        "and VARIANTS in 4 of 7 corgi cases (which is the unfavourable case). Those are different "
        "tumours and different assays, and the project has never resolved which state the case under "
        "analysis would be in.\n"
        "WHY IT IS OPEN: no canine-HS measurement for any MDM2 inhibitor, no member licensed in any "
        "species, and the eligibility gate above is undetermined. It cannot be excluded on an "
        "admissible ground. WHAT WOULD SETTLE IT: p53 sequencing plus protein status on the tumour, "
        "which is the same tissue block the MTAP immunostain of condition C5 already needs -- so it "
        "is a second stain on a sample that has to be taken anyway, not a new procedure.",
        "NONE for any MDM2 inhibitor. What exists is the LESION side rather than the drug side: low "
        "TP53 expression in the canine HS lines (PMID 25715778) and TP53 variants in 4/7 corgi cases "
        "-- recorded in `mutational_supply` and `core.breed_wide_durability`, and never connected to "
        "a therapeutic class until now.",
        Availability.NEAR_FUTURE,
        "No MDM2 inhibitor is licensed in any species; several are in human phase I/II after a long "
        "history of haematological toxicity. So this is NEAR_FUTURE at best and shares condition "
        "C7's sponsor-access problem.",
    ),
    Modality(
        "nucleic-acid therapeutics (antisense oligonucleotide, siRNA)",
        Status.NOT_ASSESSED,
        "intrathecal antisense oligonucleotide, on the nusinersen delivery precedent",
        "FOUND MISSING 2026-11-03 by the target-class diff (nucleic acid as the target rather than a "
        "protein), and recorded as the weakest of the three because rule 9 asks every plausible class "
        "to carry a status, not only the convincing ones. The reason it clears 'could plausibly "
        "matter' at all is DELIVERY RATHER THAN TARGET: intrathecal antisense is an established CNS "
        "route with a licensed precedent (nusinersen in spinal muscular atrophy), and this project "
        "already carries an intrathecal delivery arm for the leptomeningeal compartment -- so the "
        "route exists in the model even though no nucleic-acid agent does.\n"
        "WHY IT IS OPEN: no canine-HS evidence, no oncology precedent for an intrathecal ASO against "
        "a solid intracranial mass, and the same parenchymal problem every antibody-sized agent has "
        "in this analysis -- intrathecal drug reaches CSF and perivascular space rather than deep "
        "parenchyma, which is the site that decides this case. It cannot be excluded on an "
        "admissible ground, but it is ranked last of the open classes and should be triaged rather "
        "than worked up.",
        "NONE, in this disease or species.",
        Availability.NEAR_FUTURE,
        "No oncology ASO is licensed for an intracranial solid tumour; the licensed precedent "
        "(nusinersen) is a non-oncological indication and establishes the ROUTE rather than the "
        "agent. NEAR_FUTURE on the route, nothing on the drug.",
    ),
    Modality(
        "anti-angiogenic / VEGFR-axis multikinase inhibition",
        Status.EXCLUDED,
        "toceranib (Palladia -- the only FDA-approved canine kinase inhibitor); sunitinib",
        "FOUND MISSING 2026-11-03 BY THE SECOND TAXONOMY DIFF -- against the Hanahan hallmarks "
        "therapeutic map (a BIOLOGICAL taxonomy) rather than ATC L01 (a chemical one), which is the "
        "point of using a second axis. 'Inducing or accessing vasculature' is a hallmark with its own "
        "therapeutic column, and this catalogue had no row for it.\n"
        "BUT RULE 1 FIRST, because this is a bookkeeping gap and not an unexamined one: both members "
        "are ALREADY ASSESSED AS AGENTS in `therapies.py`. Toceranib carries "
        "`Verdict.CONSIDERED_UNMEASURED` with the note that its only real efficacy readout is "
        "NEGATIVE (Gardner, BMC Vet Res 2015, PMC4464614: median survival 172 vs 169 days in canine "
        "haemangiosarcoma) and that 'as a sunitinib analog it likely penetrates the CNS poorly'. So "
        "the science was examined; the class was never enumerated. Presenting this as a discovery "
        "would be CLAUDE.md failure 1.\n"
        "WHAT THIS ROW ADDS IS THE ARITHMETIC THAT REPLACES A 'LIKELY'. The existing note rests on a "
        "guess about CNS penetration. Two independent measured datasets settle it on ACHIEVABILITY "
        "instead, without needing the CNS at all: (a) PMID 29490634 Table 2, the achievability table, "
        "gives toceranib canine-HS IC50 1.9 and 1.7 uM against an achievable canine plasma of 0.1 uM "
        "at 3.25 mg/kg therapeutic dose -- short by 17-19x; and sunitinib 4.5 and 17.9 uM against an "
        "achievable 0.12 uM -- short by 37-149x. (b) The 2026 screen's own headline figure, which "
        "this project had never used: sunitinib's MEDIAN canine-HS IC50 across all ten lines is "
        "608 nM (PMID 42129963) -- the second of the paper's two named compounds beside 5-FU. Even "
        "that most favourable figure is 5x above the 0.12 uM achievable plasma. So the class fails "
        "on exposure in both datasets and on both members, which is a measured ground rather than a "
        "prediction about the brain.",
        "MEASURED, in this disease, for both members and in two laboratories: toceranib 1.7-1.9 uM "
        "and sunitinib 4.5-17.9 uM against achievable plasma of 0.1 and 0.12 uM (PMID 29490634 "
        "Table 2); sunitinib median 608 nM across ten lines (PMID 42129963). Plus a NEGATIVE canine "
        "in-vivo efficacy readout for toceranib in another canine sarcoma (PMC4464614).",
        Availability.EXISTS_TODAY,
        "Toceranib is the ONLY FDA-approved canine kinase inhibitor, so availability is as good as it "
        "gets in this species -- which is exactly why the exclusion has to be, and is, quantitative. "
        "Sunitinib is human-licensed and obtainable off-label.",
        ExclusionGround.KILL_CONTRADICTED,
    ),
    Modality(
        "apoptosis induction / BH3 mimetics (BCL-2, BCL-XL)",
        Status.NOT_ASSESSED,
        "venetoclax (BCL-2-selective, licensed, oral, continuous -- and ABSENT FROM THIS REPO); "
        "navitoclax (BCL-XL, already rejected)",
        "FOUND MISSING 2026-11-03 by the hallmarks diff ('resisting cell death'), and this one is "
        "not mere bookkeeping -- it exposes an error in the existing record of exactly the shape "
        "rule 15 names.\n"
        "WHAT THE RECORD SAYS: `therapies.py` carries navitoclax with `Verdict.REJECTED`, on the "
        "ground that 'its on-target thrombocytopenia stacks badly with lomustine's "
        "myelosuppression'. That reasoning is sound FOR NAVITOCLAX. It was then allowed to stand for "
        "the whole mechanism, and no BH3 row was ever enumerated.\n"
        "WHY THAT IS AN ERROR: navitoclax's dose-limiting thrombocytopenia is ON-TARGET BCL-XL "
        "inhibition -- platelets depend on BCL-XL for survival -- and VENETOCLAX WAS ENGINEERED "
        "SPECIFICALLY TO SPARE BCL-XL, which is the entire reason it reached licensure where "
        "navitoclax did not. So the class was set aside on a liability that its leading member is "
        "designed not to have. Under rule 15 one compound's toxicity may bound another's only with a "
        "written comparison and a direction, and here the direction runs the opposite way to the "
        "assumption: BCL-2 selectivity REMOVES the platelet liability. Venetoclax does not appear "
        "anywhere in this repository -- not in `therapies.py`, not in the catalogue, not in the "
        "docs.\n"
        "WHY IT MATTERS HERE RATHER THAN BEING A TECHNICALITY: venetoclax is licensed, ORAL and dosed "
        "CONTINUOUSLY to progression, which is the schedule condition C3 demands and which most "
        "near-future agents in this catalogue fail; and apoptosis evasion is a named resistance "
        "mechanism in this project's own escape ledger (`escape_audit` references BCL-2). "
        "SENOLYTICS ARE FOLDED IN HERE rather than given a separate row, because navitoclax is "
        "itself the canonical senolytic and the persister/senescent-cell rationale is the same "
        "mechanism.\n"
        "WHY IT IS OPEN AND NOT GRADED EITHER WAY: no canine-HS IC50 for venetoclax or any BH3 "
        "mimetic -- it is NOT among the 73 pan-active compounds of the 2026 screen, and this thread "
        "did not establish whether it was in the 1824-compound library at all, so its absence from "
        "the hit list is not yet evidence of inactivity. No CNS access figure was fetched for it "
        "either, and none is asserted. WHAT WOULD SETTLE IT: whether venetoclax was in the screened "
        "library and failed (which would be a measured negative in this disease), plus a venetoclax "
        "brain or CSF concentration.",
        "NONE for the licensed member. Venetoclax does not appear in the 2026 screen's pan-active "
        "table, but whether it was in the 1824-compound library is UNDETERMINED by this thread, so "
        "that absence is not graded as a negative. Navitoclax has no canine-HS measurement either; "
        "its rejection was on toxicity stacking, not potency.",
        Availability.EXISTS_TODAY,
        "Venetoclax is human-licensed (VENCLEXTA), oral, and labelled for continuous daily dosing -- "
        "the schedule profile this project needs and rarely finds. Obtainable off-label. Canine "
        "dosing would need deriving; dogs have received it in research settings.",
    ),
    Modality(
        "interleukin-1 blockade as a tolerability enabler (not a tumour-kill modality)",
        Status.NOT_ASSESSED,
        "anakinra, added alongside a MAPK-axis agent rather than instead of one",
        "FOUND MISSING 2026-11-03 by the hallmarks diff ('tumour-promoting inflammation'), and "
        "enumerated on the model of the `molecular surveillance` row -- which is likewise not a "
        "therapy but is in the catalogue because the plan's durability depends on it. This class "
        "does not kill the tumour; it addresses the one soft spot condition C3 admits to, which is "
        "whether a decade of continuous maintenance can actually be DELIVERED.\n"
        "THE EVIDENCE, VERIFIED IN THIS SESSION AND ALREADY RECORDED AGAINST C3: adding anakinra to "
        "MAPK-targeted therapy in Erdheim-Chester disease went with 18-month drug retention of 94% "
        "against 65% without it (PMID 39814074). It travels as an ASSOCIATION and not an effect: "
        "retrospective, observational, two referral centres, 52 patients across 60 treatment "
        "courses with the anakinra arm only 16 of those 60, anakinra at physician discretion and no "
        "adjustment for confounding. The paper's own body says 'was associated with'; only its title "
        "says 'improves'.\n"
        "WHY IT IS OPEN: an association in a human histiocytosis is not an effect size this project "
        "may apply to a dog, and no canine data exist. It cannot be excluded on any of rule 13's "
        "three grounds -- its 'kill' is not contradicted because kill is not its claim. WHAT WOULD "
        "SETTLE IT: a prospective retention comparison, or a canine tolerability series on a "
        "MAPK agent with and without IL-1 blockade.",
        "NONE in this disease or species. The retention figures are human Erdheim-Chester disease, "
        "retrospective, 16 of 60 courses.",
        Availability.EXISTS_TODAY,
        "Anakinra is human-licensed, used off-label in dogs, and short-acting -- which suits a "
        "tolerability adjunct. Availability is not what is open.",
    ),
    Modality(
        "cytotoxic chemotherapy -- topoisomerase inhibitors",
        Status.EXCLUDED,
        "etoposide and teniposide (measured); topotecan, belotecan, exatecan, rubitecan, amsacrine",
        "FOUND MISSING 2026-11-03 BY THE COMPLETENESS CRITIC, which diffed this catalogue against an "
        "EXTERNAL taxonomy (ATC L01) instead of against itself. ATC L01CB/L01CE is a subgroup with no "
        "row here, and `core.hs_drug_sensitivity.DrugClass` has carried a TOPOISOMERASE member all "
        "along -- `resistant_classes()` has been RETURNING it since the table was completed, while "
        "the catalogue had no corresponding class. The same empty-container failure as the "
        "antimetabolites, in the opposite direction: the data was present and the row was not.\n"
        "MEASURED: etoposide 755 ng/ml in the most sensitive canine HS line rising to 8180 ng/ml "
        "(1.28-13.9 uM at MW 588.56), i.e. 3.3x to 121x the chemosensitive canine lymphoma "
        "comparator (PMID 25715778 Table 1). Six further members are pan-active at 5 uM in all ten "
        "lines of the 2026 screen (belotecan, exatecan, rubitecan, topotecan, teniposide, "
        "amsacrine), so the class is NOT inert in this disease -- which is why it needs a real "
        "ground rather than a dismissal.\n"
        "GROUND -- DEFEATED_BY_ESCAPE, on two of this project's own named routes. (1) Etoposide and "
        "topotecan are canonical P-gp/BCRP substrates, and ABCB1/ABCG2 are MEASURED elevated in "
        "these very cell lines in the same paper that supplies the potency -- the single point of "
        "failure `escape_audit.A13` names, and the reason condition C4 exists. (2) Topoisomerase "
        "poisoning is REPLICATION-COUPLED: it converts a transient enzyme-DNA intermediate into a "
        "double-strand break only in a cell that is replicating, so it cannot reach the "
        "non-dividing drug-tolerant persister the ledger carries. Those two are the same grounds "
        "that already govern this project's cytotoxic choices, applied consistently.",
        "MEASURED, and measured unfavourable: etoposide 3.3-121x resistant versus the comparator "
        "(PMID 25715778). The authors' own conclusion names this class: 'alkylating agents, "
        "antimetabolites, antitumor antibiotics and TOPOISOMERASE INHIBITORS might not be effective "
        "as treatment of HS.' Six members pan-active at a 5 uM screening concentration "
        "(PMID 42129963) -- which is a lower bound on potency and not an IC50, per CLAUDE.md "
        "failure 13.",
        Availability.EXISTS_TODAY,
        "Etoposide, teniposide, topotecan and mitoxantrone are all generic and etoposide is used in "
        "dogs. Availability is not the issue; efflux and division-gating are.",
        ExclusionGround.DEFEATED_BY_ESCAPE,
    ),
    Modality(
        "cytotoxic chemotherapy -- cytotoxic antibiotics / anthracyclines",
        Status.EXCLUDED,
        "doxorubicin (measured, and the potency CLEARS); daunorubicin, idarubicin, aclarubicin, "
        "mitoxantrone, dactinomycin, mitomycin C, trabectedin",
        "ALSO FOUND MISSING 2026-11-03 (ATC L01D, no row here), AND IT IS THE SURPRISE OF THE "
        "CRITIC'S DIFF -- because this class's potency does NOT fail. It is the only cytotoxic "
        "class in this project, besides the vincas, whose measured canine-HS IC50 sits BELOW a "
        "measured achievable canine exposure:\n"
        "  * doxorubicin canine-HS IC50 95.0-343.0 ng/ml = 0.175-0.631 uM (MW 543.52; PMID 25715778 "
        "Table 1), against an ACHIEVABLE CANINE PLASMA CONCENTRATION of 1.13 uM at 30 mg/m2, "
        "therapeutic dose, in the DOG (PMID 29490634 Table 2). That clears by 1.8x to 6.5x. In that "
        "second paper's own achievability framing, doxorubicin and dasatinib are the ONLY two agents "
        "of thirteen that clear their own bar -- and doxorubicin is also the weakest resistance in "
        "the 2015 table at 1.4-14x versus the comparator.\n"
        "  * seven members are pan-active at 5 uM in all ten lines of the 2026 screen.\n"
        "So this class must not be waved away on potency, and saying so is the point of recording "
        "it: a catalogue that had simply never listed anthracyclines would have hidden the best "
        "cytotoxic potency-to-exposure ratio in the project after the microtubule class.\n"
        "GROUND -- TOXICITY_UNAFFORDABLE, and it is the identical argument this project already "
        "makes against the alkylators' dose caps rather than a new one invented for this row. "
        "Anthracyclines carry a CUMULATIVE LIFETIME DOSE CEILING set by irreversible "
        "cardiomyopathy, which is structurally incompatible with condition C3 -- maintenance dosed "
        "CONTINUOUSLY and indefinitely, duty -> 1.0. A decade of continuous anthracycline is not a "
        "dosing question, it is an arithmetic impossibility, exactly as lomustine's ~4-dose cap is. "
        "Doxorubicin is additionally a canonical P-gp substrate against the measured elevated "
        "ABCB1/ABCG2, so escape A13 applies as a second ground. The honest summary is 'the potency "
        "clears and the schedule cannot'.",
        "MEASURED, and favourably on potency: doxorubicin 0.175-0.631 uM in four canine HS lines, "
        "below the 1.13 uM achievable canine plasma; weakest fold-resistance in the 2015 table at "
        "1.4-14x. Seven members pan-active at 5 uM (PMID 42129963). The 2015 authors nonetheless "
        "group 'antitumor antibiotics' with the classes they judge ineffective, on the fold-"
        "resistance rather than on achievability -- a disagreement with their own data that this "
        "row records rather than resolves.",
        Availability.EXISTS_TODAY,
        "Doxorubicin is a veterinary standard of care with a canine therapeutic dose and a canine "
        "achievable plasma concentration in the literature. Entirely obtainable; the lifetime "
        "cardiac ceiling is what excludes it.",
        ExclusionGround.TOXICITY_UNAFFORDABLE,
    ),
    Modality(
        "nuclear export inhibition (XPO1 / SINE compounds)",
        Status.NOT_ASSESSED,
        "verdinexor (Laverdia-CA1 -- LICENSED FOR DOGS); selinexor (XPOVIO, and the member with the "
        "canine-HS screen activity and the measured brain access)",
        "THE MOST CONSEQUENTIAL HOLE THE CRITIC FOUND, because this class contains a CANINE-LICENSED, "
        "ORALLY DOSED, INDEFINITELY SCHEDULED agent -- and this catalogue had no row for it, while a "
        "SIBLING BRANCH of this same project had already done the pharmacology. Rule 1 found it: "
        "`git show origin/claude/duplicate-codex-prefix-branch-lt1qh6:docs/LYMPHOMA_STATUS.md`. "
        "CLAUDE.md failure 11 is itself about this drug pair, so the class was discussed in this "
        "project and never enumerated in this case's universe.\n"
        "WHAT IT HAS: (1) SELINEXOR IS PAN-ACTIVE in all ten canine HS lines at 5 uM "
        "(PMID 42129963 Table 2) -- verified directly, so the class has canine-HS activity in this "
        "disease. (2) MEASURED BRAIN ACCESS ACROSS THREE SPECIES: selinexor total brain:plasma "
        "0.71 mouse / 0.72 rat / 0.6 monkey, from Table 1 of PMC5143172 (PMID 27323910, Leukemia "
        "2016) -- plasma 1760/1670/2545 h.ng/mL against brain 1295/1207/1565 h.ng/g at 2 h after "
        "oral dosing. The same table is the basis on which its successor KPT-8602 was designed for "
        "LOWER CNS penetration (0.19/0.22/<0.02), so selinexor's brain entry is the deliberate, "
        "documented property of the pair. "
        "FOUR CORRECTIONS FROM INDEPENDENT RE-VERIFICATION, 2026-11-04, three of which this row had "
        "not recorded: (a) 'AT AN INTACT BARRIER' AND 'IN HEALTHY ANIMALS' ARE NOT IN THE SOURCE. "
        "The paper has NO methods section for this PK experiment, and zero occurrences of 'healthy', "
        "'naive', 'tumor-bearing' or 'intact'. Those words were THIS PROJECT'S INFERENCE and are now "
        "graded as inferred, never as part of the measurement. The inference is also UNEQUAL across "
        "species, which the row had flattened: strong for rat and monkey (the paper runs no rat or "
        "monkey tumour model anywhere, so those animals cannot have been tumour-bearing in it), "
        "weaker for mouse (the paper is full of leukaemia-bearing mice, and the only discriminator is "
        "that the PK doses differ from the efficacy doses). Note the tumour models are CLL/AML "
        "haematological rather than intracranial, so even a tumour-bearing mouse need not have a "
        "disrupted blood-brain barrier. (b) THE PRINTED 0.71 DOES NOT RECONCILE WITH ITS OWN TABLE: "
        "1295/1760 = 0.7358, i.e. 0.74. Every other row reconciles exactly (rat 1207/1670 = 0.72; "
        "KPT-8602 0.19, 0.22, <0.02), so the mouse selinexor row is the ONE row in that table that "
        "contradicts its own quotient. That is a defect in the SOURCE rather than a transcription "
        "error here, but this project is quoting a number its own cited table contradicts, and must "
        "say so. Direction: the arithmetic is MORE favourable (0.74), so the access case is not "
        "weakened by the discrepancy. (c) The monkey cell prints '0.6', not '0.60', and 1565/2545 = "
        "0.6149 rounds to 0.61 -- so quote it as 0.6 and do not add a significant figure the source "
        "does not carry. (d) DOSE MISMATCH INSIDE THE COMPARISON, unrecorded until now: the KPT-8602 "
        "mouse and rat rows are at 5 mg/kg while ALL THREE selinexor rows are at 10 mg/kg, so the "
        "'0.71/0.72 versus 0.19/0.22' contrast compares the comparator AT HALF THE DOSE in two of "
        "three species. Only the monkey pair is dose-matched. "
        "CONFIRMED IN THIS PROJECT'S FAVOUR by the same check: these ARE total and not unbound "
        "ratios -- 'unbound', 'free fraction' and 'protein binding' appear nowhere in the article, "
        "Table 1 carries no footnote, and brain is reported as ng/g of homogenate against total "
        "plasma ng/mL -- so the rule-15 caution below stands as written. And there is NO DOG "
        "anywhere in that paper; its disease context is CLL, AML and DLBCL. "
        "(3) A LICENSED CANINE AGENT -- AND THE SCHEDULE HALF OF THIS CLAIM DID NOT SURVIVE "
        "VERIFICATION. It was taken from the sibling branch and flagged as unverified; an "
        "independent agent then checked it at the FDA primary record on 2026-11-04 and corrected "
        "three of its five elements:\n"
        "   - WHAT STANDS: conditional approval 11 January 2021 (application 141-526, Anivive "
        "Lifesciences), indication LYMPHOMA IN DOGS, oral, 1.25 mg/kg TWICE WEEKLY at least 72 h "
        "apart, escalating to 1.5 mg/kg after two weeks if tolerated.\n"
        "   - CORRECTED: full approval is 18 DECEMBER 2025, not January 2026 -- NADA 141-614, a "
        "DIFFERENT application from the conditional one. The January 2026 date was FDA's CVM Update "
        "PUBLICISING it; the record had mistaken the announcement for the approval.\n"
        "   - CORRECTED: the product is now LAVERDIA, not Laverdia-CA1. '-CA1' is FDA's mandatory "
        "suffix for a CONDITIONALLY approved product and it is gone from the full-approval record; "
        "tablet strengths went from three to four, so this is a relabelled product.\n"
        "   - RETRACTED, AND IT WAS THE LOAD-BEARING HALF: 'UNTIL PROGRESSION' IS NOT ON THE LABEL "
        "IN ANY WORDING. The word 'until' does not appear in the 26-page approval summary. The label "
        "gives dose, frequency, escalation and reduction rules and then STOPS -- it is SILENT on "
        "duration, neither directing indefinite treatment nor capping it. The pivotal field study "
        "was a FIXED 56-DAY course with a 37-day median time to progression.\n"
        "   WHY THAT MATTERS HERE RATHER THAN BEING A FOOTNOTE: this row previously used 'until "
        "progression' to make verdinexor the one agent in the catalogue 'simultaneously licensed in "
        "the target species, orally dosed and INDEFINITELY SCHEDULED', and to resolve the tension "
        "with condition C3. That distinguishing property has no label basis. 'The label places no "
        "limit on duration' is SILENCE, which a prescriber fills; it is not an affirmative "
        "indefinite-dosing instruction. Under rule 5 the honest grade for indefinite scheduling here "
        "is ASSUMED, or at best a clinical-practice inference -- and the contrast this row drew with "
        "the anthracyclines' and alkylators' hard dose caps DOES NOT SURVIVE, because those are "
        "affirmative ceilings while this is an absence of guidance.\n"
        "   ALSO ESTABLISHED BY THAT CHECK: the approval record reports NO tissue distribution and "
        "NO brain or CSF concentration for verdinexor in any species. So the regulatory file "
        "establishes existence, legality, route, dose and frequency in dogs, and NOTHING about reach "
        "into an intracranial compartment.\n"
        "WHY IT IS OPEN RATHER THAN IN-MODEL, and the reasons are rule-15 reasons: (a) the 0.60-0.72 "
        "figures are TOTAL brain:plasma ratios, not unbound, so they CANNOT be compared directly "
        "with this project's unbound parenchymal access requirement of 0.196 -- that comparison is "
        "precisely the trap rule 15 names, and it is not made here. (b) They are SELINEXOR's "
        "numbers, and the licensed canine agent is VERDINEXOR; the sibling branch's own 2026-11-01 "
        "correction states that selinexor's CSF figure is a FLOOR for verdinexor rather than its "
        "value, and verdinexor's tissue distribution is unmeasured in any species. (c) No canine-HS "
        "IC50 exists for either member -- the screen gives a 5 uM threshold, which failure 13 "
        "forbids reading as a potency. (d) Verdinexor's canine-lymphoma efficacy is modest where it "
        "is measured: 37% response, median duration 18 days (cross-branch record). (e) Twice-weekly "
        "dosing is the same tension with C3's continuous presence that dordaviprone and tovorafenib "
        "carry -- though 'until progression' makes it indefinite rather than capped, unlike the "
        "anthracyclines and alkylators.\n"
        "WHAT WOULD CLOSE IT, and the sibling branch already names them as its two cheapest decisive "
        "measurements: a VERDINEXOR BRAIN:PLASMA RATIO FROM ANY DOG ON THE LICENSED DRUG, and a "
        "canine-HS IC50 for either member. Both are obtainable from animals already receiving an "
        "approved drug.",
        "MEASURED, in this disease, for one member: selinexor reduced viable cell counts to <=70% at "
        "5 uM in ALL TEN canine HS lines (PMID 42129963 Table 2). No canine-HS IC50 for any member, "
        "and no verdinexor tissue distribution in any species -- which under rule 13 is not a ground "
        "for exclusion and under rule 11 is not a gap to report, but IS the reason the class cannot "
        "yet be graded into the model.",
        Availability.EXISTS_TODAY,
        "UNIQUELY STRONG IN THIS CATALOGUE: verdinexor is LICENSED FOR DOGS (Laverdia-CA1), oral, "
        "and labelled until progression -- the only agent in any class here that is simultaneously "
        "licensed in the target species, orally dosed and indefinitely scheduled. Selinexor is "
        "human-licensed (XPOVIO, NDA 212306) and obtainable off-label, and it is the member carrying "
        "both the canine-HS screen activity and the three-species brain measurement. The class is "
        "therefore the opposite of a to-build problem.",
    ),
    Modality(
        "proteasome inhibition",
        Status.NOT_ASSESSED,
        "ixazomib (oral); carfilzomib; bortezomib",
        "FOUND MISSING 2026-11-03 (ATC L01XG, no row here). TWO MEMBERS ARE PAN-ACTIVE in all ten "
        "canine HS lines at 5 uM -- carfilzomib and ixazomib citrate, both in Table 2 of "
        "PMID 42129963, verified directly. All three members are human-licensed, and IXAZOMIB IS "
        "ORAL, which matters because condition C3 requires continuous presence and most of this "
        "catalogue's near-future agents fail on schedule rather than on potency.\n"
        "WHY IT IS OPEN: no canine-HS IC50 for any member (the 5 uM figure is a screening threshold, "
        "not a potency -- failure 13), and NO CNS ACCESS FIGURE WAS ESTABLISHED BY THIS THREAD for "
        "any proteasome inhibitor. It would have been easy to assert that bortezomib penetrates the "
        "CNS poorly, which is the general belief; this row does not, because no source for it was "
        "fetched. Under rule 16 an unsourced explanation is what gets a class wrongly graded. "
        "WHAT WOULD CLOSE IT: a measured brain or CSF concentration for any proteasome inhibitor, "
        "and a canine-HS IC50 for ixazomib or carfilzomib.",
        "MEASURED, in this disease, for two members: carfilzomib and ixazomib reduced viable cell "
        "counts to <=70% at 5 uM in all ten canine HS lines (PMID 42129963 Table 2). Nothing further "
        "in dogs.",
        Availability.EXISTS_TODAY,
        "Bortezomib, carfilzomib and ixazomib are all human-licensed and obtainable off-label; "
        "ixazomib is oral, which is the schedule this project needs. Availability is not what is "
        "open here -- the access measurement is.",
    ),
    Modality(
        "HSP90 inhibition",
        Status.NOT_ASSESSED,
        "retaspimycin (the screen hit); ganetespib, onalespib as the clinical-stage members",
        "FOUND MISSING 2026-11-03 by the same diff, on weaker evidence than the four above and "
        "recorded anyway, because rule 9 asks for every class to carry a status rather than for the "
        "convincing ones to be listed. Retaspimycin hydrochloride is pan-active at 5 uM in all ten "
        "canine HS lines (PMID 42129963 Table 2). That is the whole of the evidence: one member, one "
        "screening concentration, no IC50, no canine PK, no CNS figure, and no licensed member. "
        "It cannot be excluded on any admissible ground and cannot be graded in. The honest "
        "assessment is that it is the weakest of the six open classes and should be triaged before "
        "it is worked up.",
        "MEASURED, in this disease, at a screening threshold only: retaspimycin pan-active at 5 uM "
        "across ten canine HS lines (PMID 42129963). No IC50, no canine PK.",
        Availability.NEAR_FUTURE,
        "No HSP90 inhibitor is licensed in any species; several reached human phase II and were not "
        "carried forward. So this class is NEAR_FUTURE at best and would need a sponsor, which is "
        "the same position as condition C7.",
    ),
    Modality(
        "cardiac glycosides / Na+,K+-ATPase inhibition",
        Status.NOT_ASSESSED,
        "digoxin, ouabain, lanatoside C, proscillaridin A, resibufogenin",
        "FOUND MISSING 2026-11-03, and recorded with an explicit caution rather than enthusiasm. "
        "FIVE members are pan-active at 5 uM in all ten canine HS lines (PMID 42129963 Table 2), "
        "which is the largest member count of any newly found class, and digoxin is licensed, oral "
        "and dosed indefinitely in dogs for heart failure -- so on the face of it this is an "
        "exists-today, continuously-dosed, canine-dosed class.\n"
        "THE CAUTION, WHICH IS WHY IT IS NOT BEING WORKED UP FIRST: cardiac glycosides are a "
        "notorious recurring hit class in drug-repurposing screens, because Na+,K+-ATPase inhibition "
        "is broadly cytotoxic at micromolar concentrations in culture and the therapeutic plasma "
        "range for digoxin in vivo is roughly 1-2 ng/ml (about 1-3 nM), three orders of magnitude "
        "below the 5 uM screening concentration. So the expected finding is that the achievable "
        "exposure falls far short of the screen concentration -- but this thread has NOT fetched a "
        "canine digoxin achievable-concentration source, so that arithmetic is stated as the "
        "expectation to test and NOT as a ground. Asserting it unsourced is exactly rule 16's "
        "failure. WHAT WOULD SETTLE IT: a canine digoxin therapeutic plasma concentration, which is "
        "a routine veterinary monitoring value, set against a canine-HS IC50.",
        "MEASURED, at a screening threshold only: five members pan-active at 5 uM across ten canine "
        "HS lines (PMID 42129963). No IC50 in this disease and no achievable-exposure comparison "
        "fetched by this thread.",
        Availability.EXISTS_TODAY,
        "Digoxin is licensed, oral, cheap and dosed indefinitely in dogs, with routine therapeutic "
        "drug monitoring -- so if the exposure arithmetic worked this would be among the most "
        "obtainable agents in the whole catalogue. The arithmetic is what is unestablished.",
    ),
    Modality(
        "translation-elongation inhibition",
        Status.NOT_ASSESSED,
        "homoharringtonine (omacetaxine, licensed); emetine; cycloheximide (tool compound)",
        "FOUND MISSING 2026-11-03. Three members pan-active at 5 uM in all ten canine HS lines "
        "(PMID 42129963 Table 2), and one of them -- homoharringtonine, as omacetaxine mepesuccinate "
        "-- is human-licensed for chronic myeloid leukaemia, so the class is not purely preclinical. "
        "No canine-HS IC50, no canine PK, no CNS access figure, and cycloheximide is a laboratory "
        "tool rather than a drug. Cannot be excluded on an admissible ground; cannot be graded in. "
        "Recorded as open and ranked below the four substantive classes above.",
        "MEASURED, at a screening threshold only: three members pan-active at 5 uM across ten canine "
        "HS lines (PMID 42129963). Nothing further in dogs.",
        Availability.EXISTS_TODAY,
        "Omacetaxine is human-licensed and therefore obtainable off-label, though it is a "
        "subcutaneous cycled agent, which sits badly with C3's continuous-presence requirement.",
    ),
    Modality(
        "targeted small molecules -- MAPK axis (MEK/ERK/SHP2)",
        Status.IN_MODEL,
        "trametinib / cobimetinib / mirdametinib; tovorafenib as the licensed pan-RAF option",
        "The maintenance arm for the ~59% MAPK-driver majority. Site-split: closes the lung "
        "systemically; brain closure depends on unmeasured canine CNS access. "
        "ADDED 2026-10-31 -- a pan-RAF member, which this class did not list and the project had "
        "nowhere: TOVORAFENIB (DAY101/TAK-580/MLN2480), a type II RAF inhibitor, is FDA-APPROVED for "
        "paediatric BRAF-altered glioma (PMID 41201564) -- i.e. a licensed MAPK-axis agent whose "
        "approved indication is a BRAIN TUMOUR, which is exactly what the MEK members lack. Phase 2 "
        "FIREFLY-1 gave ORR 67% by RANO-HGG, with response INDEPENDENT of histology, of BRAF "
        "alteration type, of prior lines, and -- load-bearing for the reroute escape -- of PRIOR "
        "MAPK-PATHWAY INHIBITOR USE; its CNS-penetration properties are the stated reason it was "
        "taken into a first-line phase 3 (PMID 38291372, NCT05566795). It is also in phase 2 for "
        "recurrent/refractory Langerhans cell histiocytosis (NCT05828069), i.e. inside the "
        "histiocytic family this project transfers from. "
        "LABEL READ AT FDA 2026-11-01, and it tightens limit (1) below from a caveat into a hard "
        "constraint: OJEMDA is indicated for 'relapsed or refractory pediatric low-grade glioma "
        "(LGG) harboring a BRAF fusion or rearrangement, or BRAF V600 mutation', the label "
        "DIRECTS confirming that lesion PRIOR TO INITIATION, the approval is ACCELERATED on "
        "response rate and duration pending confirmatory trials, and dosing is ORAL ONCE WEEKLY. "
        "Canine HS carries BRAF alterations in under 1%, so the licensed indication is "
        "genotype-gated to a lesion this disease essentially does not have. It therefore remains an "
        "OFF-LABEL, MECHANISM-BASED option here (type II RAF inhibition acts on RAF dimers, the "
        "right node for RAS-driven signalling) and must NOT be read as 'licensed for this "
        "tumour's genotype'. "
        "TWO HONEST LIMITS, both of which stop this from closing the brain branch today: (1) the "
        "clinical evidence is in BRAF-ALTERED tumours, whereas canine HS is PTPN11/SHP2 (~56%) and "
        "KRAS (~3%) driven with BRAF under 1% -- a type II RAF inhibitor acts on RAF DIMERS, which is "
        "the mechanistically right place for RAS-driven signalling, but that is a mechanism argument, "
        "not the trial result; (2) dosing is ONCE WEEKLY (420 mg/m2, cap 600 mg), the same tension "
        "with continuous presence that dordaviprone carries. No canine PK, HS IC50 or brain:plasma "
        "ratio exists for it. So it enters as a LISTED EXISTS-TODAY OPTION on this axis, not as a "
        "graded closure of the brain branch.",
        "MEASURED: canine HS sensitivity surveyed; a canine Phase I exists (trametinib), ~30% of "
        "dogs underdosed at the MTD.",
        Availability.EXISTS_TODAY,
        "Trametinib has a COMPLETED canine Phase I with a recommended dose (PMID 38889903), and "
        "cobimetinib has both a canine-HS IC50 and a canine plasma Cmax (PMID 39202410). This is "
        "the best-tiered maintenance class in the project: obtainable AND measured in the dog. "
        "AND THE STRONGEST EVIDENCE AGAINST THIS AXIS AT THE CNS SITE, FOUND 2026-11-03. The largest "
        "MAPK-in-histiocytosis dataset that exists -- 288 children with refractory LCH, 26 "
        "countries, off-label MAPK inhibitors, median follow-up 3.7 years, including 42 cobimetinib "
        "and 45 trametinib prescriptions (PMID 41678955) -- reports short-term response rates by "
        "indication, and the CNS indication is the one that fails: 98% in risk-organ-positive and "
        "risk-organ-negative disease, 30% in lung destruction, and 'NONE (ND, DI, and SC)' -- zero "
        "short-term responses in NEURODEGENERATIVE CNS LCH, in 49 such cases, although the authors "
        "note 'long-term lung and ND responses could be observed'. Worse for the protective claim: "
        "among 143 patients WITHOUT CNS neurodegeneration when MAPK inhibition began, 60 developed "
        "it -- a 45% five-year risk WHILE ON the drug. So in the human histiocytic family, MAPK "
        "inhibition is near-universally active outside the CNS and neither promptly active within "
        "it nor protective of it. "
        "RETRACTED IN PART ON 2026-11-04, BY INDEPENDENT RE-VERIFICATION, AND THE RETRACTION IS THE "
        "IMPORTANT PART. Using those ND figures as evidence about this axis AT THE CNS SITE WAS "
        "WRONG, and wrong in the specific way rule 14 names -- reading a label instead of the "
        "measured quantity. 'ND-LCH' is not an intracranial tumour mass: the paper defines it as a "
        "late NEURODEGENERATIVE syndrome, assessed by MRI criteria, and its Discussion attributes it "
        "to 'disease sequestration in the brain microglia'. So neither 'no short-term response in "
        "ND' nor the 45% five-year ND risk is a statement about drug activity against, or drug "
        "access to, an intracranial tumour LESION -- which is the only thing this row needed from "
        "it. Worse for the original framing, the same paper reports the OPPOSITE direction for CNS "
        "symptomatic disease on prolonged therapy: 66% stabilisation and 33% mild regression. "
        "THREE NUMBERS ALSO CORRECTED, all because this row quoted the abstract where the body "
        "disagrees: the ND denominator is 147 assessable, not 143 (so 60/147 = 41% crude, with the "
        "45% being a Kaplan-Meier five-year risk carrying a 35-55% confidence interval); the ND "
        "endpoint is MRI-DETECTED and only 23 OF THE 60 WERE SYMPTOMATIC, so '60 developed it' "
        "overstates what was observed in 37 of them; and the 98% and 30% response figures EXIST "
        "ONLY IN THE ABSTRACT -- the body gives 157 complete and 57 partial responses of 215, and "
        "for lung '20 out of 22 assessable patients had good clinical responses' (91%), with no 30% "
        "anywhere. WHAT SURVIVES for this row is narrow and still worth keeping: MAPK inhibition is "
        "near-universally active in systemic risk-organ LCH and this axis's CNS weakness has been "
        "looked for clinically at scale in the right lineage -- but the ND data cannot carry the "
        "weight, and the row no longer asks them to. "
        "SCOPE, because it decides how much this bites: human, paediatric, LCH rather than "
        "histiocytic sarcoma, observational and off-label; and 'neurodegenerative LCH' is a "
        "distinct CNS pathology -- a progressive cerebellar/brainstem degeneration -- rather than "
        "the parenchymal mass this project targets, so the site matches better than the lesion "
        "does. It is indirect on disease and on CNS pathology type. What it nonetheless establishes "
        "is that this axis's CNS weakness is not merely an unmeasured access figure in a dog: it "
        "has been looked for clinically, in the right lineage, at scale, and was not found "
        "short-term. That strengthens rather than contradicts this row's existing self-assessment "
        "('brain closure depends on unmeasured canine CNS access'), and it is why the row's brain "
        "branch stays ungraded for the parenchyma. "
        "THE STRONGEST SINGLE FACT FOUND IN THIS WHOLE SWEEP, 2026-11-02, AND IT WAS A LABEL READ: "
        "COBIMETINIB IS LICENSED FOR THIS DISEASE FAMILY, WITH NO GENOTYPE GATE. COTELLIC, NDA "
        "206192, label effective_time 20260729, reads: 'As a single agent for the treatment of adult "
        "patients with HISTIOCYTIC NEOPLASMS' -- and the absence of a qualifier is the point, because "
        "the SAME LABEL gates its other indication ('unresectable or metastatic melanoma with a BRAF "
        "V600E or V600K mutation, in combination with vemurafenib'). So the drug's sponsor and the "
        "FDA have agreed an indication in histiocytic neoplasms that does not require any mutation "
        "to be demonstrated first. That is exactly the problem tovorafenib has and cannot solve: "
        "tovorafenib's label DIRECTS confirming a BRAF fusion or V600 mutation before initiation, "
        "and this disease is BRAF under 1%. Cobimetinib's does not. "
        "WHY THIS MATTERS MORE THAN A TIER LABEL: cobimetinib already carries, in this project, a "
        "MEASURED canine-HS IC50 of 74-372 nM and a MEASURED canine plasma Cmax of 1640 nM "
        "(PMID 39202410). It is therefore the only agent anywhere in this analysis that is "
        "simultaneously (a) licensed, (b) licensed for the disease FAMILY under analysis without a "
        "biomarker precondition, and (c) measured in canine histiocytic sarcoma cells with a canine "
        "exposure to compare against. Nothing else in the catalogue has all three. "
        "WHAT IT DOES NOT DO, stated so this is not read as more than it is: the indication is for "
        "ADULT HUMAN patients, so a dog is still off-label; 'histiocytic neoplasms' in the human "
        "nosology is dominated by Erdheim-Chester and LCH rather than histiocytic sarcoma -- and INDEPENDENT RE-VERIFICATION ON 2026-11-04 made that sharper than 'dominated by': label section 14.2 ENUMERATES ALL 26 SUPPORTING PATIENTS BY ENTITY (Langerhans cell histiocytosis n=4, Rosai-Dorfman n=4, Erdheim-Chester and others) and THERE IS NO HISTIOCYTIC SARCOMA AMONG THEM. So the indication covers this tumour by the WORDING of its entity class while its evidentiary base contains none of it. The disease match is to the family and not to this tumour, and so the "
        "disease match is to the family and not to this tumour; and the brain is untouched by it -- "
        "cobimetinib's brain headroom in this project remains 0.5x, i.e. SHORT, so a licensed "
        "indication does not supply parenchymal access. It upgrades the systemic arm and the "
        "regulatory story, not the site that decides the case. The repo had cited NDA 206192 only "
        "for the canine minimum lethal dose in `core.toxicity`; the indication itself was absent. "
        "CORRECTED 2026-11-01: this class's two CNS-relevant members are LICENSED, which the record "
        "had not said -- it treated both as investigational. Verified at Drugs@FDA: mirdametinib is "
        "GOMEKLI, NDA 219379 and NDA 219389 (SpringWorks), oral, approved 2025-02-11 for NF1-"
        "associated plexiform neurofibromas, and a peer-reviewed review states its 'added advantage "
        "of CNS penetration' (PMID 40932001); tovorafenib is OJEMDA, NDA 217700 and NDA 218033 (Day "
        "One Biopharms), oral, approved 2024-04-23, for a BRAIN TUMOUR indication. So 'the agent "
        "does not exist' is no longer a reason the brain branch is weak -- both are obtainable "
        "off-label today. The remaining reason is the MEASUREMENT: no canine brain:plasma ratio "
        "exists for either, and for the parenchymal site the class is still ungraded. For the CSF "
        "site it is not: mirdametinib's NHP CSF/unbound-plasma ratio is 2.5-3.0 (PMC9661017), a "
        "measured transfer against a 0.0145 requirement.",
    ),
    Modality(
        "targeted small molecules -- PI3K/AKT/mTOR axis",
        Status.IN_MODEL,
        "duvelisib (the exists-today member); paxalisib for brain access",
        "Covers the RTK-bypass escape. The 2026 screen gives this axis real canine-HS grounding that "
        "the model's transferred hemangiosarcoma IC50s lacked.",
        "MEASURED (axis): duvelisib selective in one HS expression subgroup, median IC50 287 nM vs "
        ">5 uM in the other and 7.46 uM in normal PBMC (PMID 42129963). Paxalisib itself: transfer.",
        Availability.EXISTS_TODAY,
        "Duvelisib is human-licensed (COPIKTRA) and therefore obtainable off-label, and it is the "
        "member with the canine-HS IC50. Paxalisib -- the member with the measured Kp,uu 0.31 and "
        "confirmed P-gp/BCRP non-substrate status -- is investigational, so the class splits: the "
        "exists-today member supplies the potency, the to-build member supplies the access.",
    ),
    Modality(
        "targeted small molecules -- FGFR axis",
        Status.EXCLUDED,
        "infigratinib; erdafitinib (BALVERSA); pemigatinib (PEMAZYRE)",
        "NEWLY ASSESSED 2026-11-01, enumerated in the same sweep as the antimetabolites and unlike "
        "them it closes out. The table "
        "gives every other targeted axis its own row (MAPK, PI3K, CDK4/6, synthetic lethality, "
        "CSF1R) and had no FGFR row, although FGFR1 OVEREXPRESSION is reported in canine HS cases "
        "and three FGFR inhibitors score in the canine screen: infigratinib inhibited proliferation "
        "in ALL CHS lines EXCEPT CHS8, erdafitinib had low IC50 in the Group A lines 'although not "
        "as low as duvelisib', and pemigatinib hit 6 of the 8 Group A lines on the screen criterion "
        "(PMID 42129963). Two of the three are licensed. On paper that is a stronger starting hand "
        "than several classes that are IN_MODEL. "
        "IT IS EXCLUDED ANYWAY, ON MEASURED DATA AT THE RIGHT SITE AND FOR THE RIGHT BIOMARKER. The "
        "class has already been tested in human recurrent BRAIN tumours: a multicentre phase 2 of "
        "infigratinib in FGFR-altered recurrent glioma (n=26) gave 6-month PFS 16.0%, median PFS "
        "1.7 months and ORR 3.8% -- and the four patients with durable control beyond a year ALL "
        "carried an activating FGFR1 (K656E) or FGFR3 (K650E) POINT MUTATION or an FGFR3-TACC3 "
        "FUSION (PMID 35344029). Canine HS is reported with FGFR1 OVEREXPRESSION, not with "
        "activating FGFR point mutations or fusions, so this tumour's biomarker is precisely the one "
        "in which the class failed at this site. "
        "RULE 15, APPLIED TO THIS EXCLUSION, BECAUSE IT IS THE OBVIOUS OBJECTION: the trial dosed "
        "INFIGRATINIB, while the licensed members here are erdafitinib and pemigatinib, and one "
        "compound's trial cannot contradict another compound's number. This exclusion does not make "
        "that move. What transfers is a statement about the TARGET, which all three share -- that "
        "FGFR-axis benefit at this site tracked an activating lesion rather than the FGFR-altered "
        "population at large -- and not infigratinib's potency, exposure or response rate attached "
        "to either other compound. The DIRECTION is what makes the transfer safe: the trial enrolled "
        "tumours with FGFR ALTERATIONS, a population already enriched beyond mere overexpression, so "
        "its 3.8% response rate is a CEILING for an overexpression-only tumour, not a floor. A "
        "ceiling that low at this site is what the exclusion rests on. The screen's own authors "
        "reach the same place from "
        "the other direction: ponatinib, which also targets FGFR1, did not inhibit most CHS lines, "
        "so they conclude infigratinib's canine-HS effect 'may not be solely attributable to FGFR1 "
        "inhibition and could involve FGFR1-independent mechanisms' -- i.e. the canine signal is "
        "not evidence that the FGFR axis is the driver. On-target hyperphosphataemia in 76.9% is a "
        "second cost against a class whose benefit is unsupported in this biomarker.",
        "MEASURED, and the canine signal is real but mechanistically unattributed: infigratinib "
        "9/10 lines, erdafitinib Group-A-selective, pemigatinib 6/8 Group A (PMID 42129963); FGFR1 "
        "overexpression reported in CHS cases. The exclusion rests on the human brain-tumour trial, "
        "not on any absence of canine data.",
        Availability.EXISTS_TODAY,
        "Verified at openFDA 2026-11-01: erdafitinib is BALVERSA, NDA 212018, Janssen Biotech; "
        "pemigatinib is PEMAZYRE, NDA 213736, Incyte. Both are obtainable off-label today. "
        "Infigratinib (TRUSELTIQ) is the one with the glioma trial and is no longer marketed. "
        "Availability is not the ground; the glioma phase 2 is.",
        ExclusionGround.KILL_CONTRADICTED,
    ),
    Modality(
        "targeted small molecules -- cell-cycle (CDK4/6)",
        Status.IN_MODEL,
        "abemaciclib (brain-penetrant); palbociclib as the measured class comparator",
        "Now the lead brain arm for the deletion-carrying tumour (HS_STATUS section A): measured "
        "human brain-tumour tissue exposure 19-96x the CDK4/6 IC50, and a met endpoint in "
        "CDK-pathway meningioma, the same extra-axial niche. "
        "THREE MEASUREMENTS ADDED 2026-11-03, AND THEY DO NOT ALL POINT THE SAME WAY -- which is "
        "why this row is now the best-evidenced AND the most qualified in the catalogue.\n"
        "  (1) THE PROJECT'S OWN METHOD, APPLIED TO ABEMACICLIB, IN THE PROJECT'S OWN GENOTYPE. "
        "NCT04391595 (Sanai, Ivy Brain Tumor Center) is a Phase 0/2 in 42 recurrent GBM patients "
        "selected for INTACT RB, >30% pERK, and CDKN2A/B DELETION or CDK4/6 amplification -- the "
        "same lesion configuration as this tumour. Six days of abemaciclib plus the ERK1/2 "
        "inhibitor LY3214996 (= temuterkib, already in this project's catalogue) before planned "
        "resection, with tissue taken from Gd-ENHANCING and Gd-NONENHANCING regions plus CSF and "
        "plasma, unbound by validated LC-MS/MS. MEDIAN UNBOUND ABEMACICLIB IN Gd-NONENHANCING "
        "TUMOUR: 31 nM, against a PK trigger (>5x IC50) the trialists set at 12 nM for this drug -- "
        "so it CLEARS its own threshold by 2.6x in the compartment that defines an intact barrier. "
        "PD in the same tissue: RB phosphorylation down in 47.5%, MIB-1 proliferation down in "
        "72.5%. No DLTs. The honest qualifier is the dual-drug rate: only 9 of 40 (22.5%) exceeded "
        "the thresholds for BOTH agents, and LY3214996's own median was 10 nM against its 25 nM "
        "trigger, i.e. the ERK partner FAILED where abemaciclib passed "
        "(DOI 10.1093/neuonc/noae165.0425, PMC11553480).\n"
        "AND THE DECISIVE OMISSION, SUPPLIED BY INDEPENDENT RE-VERIFICATION ON 2026-11-04: THIS "
        "TRIAL'S EFFICACY RESULT IS NEGATIVE, AND THIS ROW HAD CITED ONLY ITS ACCESS WIN. The same "
        "abstract reports that the 9 threshold-exceeding patients who proceeded to the Phase 2 "
        "component had MEDIAN PFS 2.4 MONTHS AND MEDIAN OS 7.2 MONTHS, and it concludes on 'the "
        "unremarkable clinical efficacy profile' of the combination. So the project's strongest "
        "access measurement and a null efficacy readout come from THE SAME 42 PATIENTS: the drug "
        "cleared its concentration trigger in Gd-non-enhancing tumour, engaged its target in that "
        "tissue, and did not help. Quoting the 31 nM without the 2.4 months is exactly the "
        "selective reading rule 5 exists to stop, and it was done here.\n"
        "  (2) A SECOND, INDEPENDENT METHOD FOR THE PARENCHYMA, replacing a rodent ratio with a "
        "human one. NCT05413304 (NCI) measured abemaciclib in brain tumour INTERSTITIAL FLUID by "
        "INTRATUMORAL MICRODIALYSIS and has posted results: median brain-dialysate Cmax 7.5, 19.1 "
        "and 105.8 nM across subgroups, AUC 148.2, 440.3 and 1433.0 hr*nM, and -- the load-bearing "
        "figure -- MEDIAN RATIO OF BRAIN-DIALYSATE AUC TO UNBOUND PLASMA AUC of 0.27, 0.72 and "
        "2.73. Against this project's parenchymal access requirement of 0.196 that clears even at "
        "the low end (1.4x), on a HUMAN measurement in brain tumour tissue rather than on the "
        "rodent ratio the project had been using. Rule 14 prefers it for that reason. The qualifier "
        "is decisive to how it may be used: PHASE 1, n=5, and the ratio spans an order of magnitude "
        "across three subgroups, so it is a measured transfer with wide bounds, not a settled "
        "number. CORRECTED 2026-11-04: the numbers are exact, but BARRIER STATUS IS NOWHERE STATED "
        "in the posted record, and for the two Arm 1 values (0.27 and 0.72) the catheter was placed "
        "after 'a maximally safe surgical resection' -- i.e. into a RESECTION BED, where the "
        "barrier is surgically disrupted. So these ratios must NOT be read as access behind an "
        "intact barrier, which is the quantity this project actually needs; they are interstitial "
        "concentrations in and around an operated cavity. Also: n=5 is ENROLLED, with 1 of 5 not "
        "evaluable on both outcomes, so three subgroup medians rest on four animals' worth of data.\n"
        "  (3) AND A NEGATIVE, AGAINST THE ROW THIS PROJECT SCORES HIGHEST. Abemaciclib MONOTHERAPY "
        "in brain metastases, phase 2, NCT02308020, n=51 (NSCLC 28, melanoma 23), 200 mg BID: 'NO "
        "CONFIRMED INTRACRANIAL RESPONSE WAS OBSERVED IN EITHER COHORT'. "
        "THREE NUMERICAL CORRECTIONS FROM INDEPENDENT RE-VERIFICATION, 2026-11-04, and one of them "
        "was this row quoting the more favourable of two inconsistent figures: (i) INTRACRANIAL "
        "CLINICAL BENEFIT IS 21.4% (NSCLC) AND 8.7% (MELANOMA) per the paper's RESULTS section, not "
        "the 26.1% and 9.1% printed in its abstract. The published paper is internally "
        "inconsistent; the Results values are the arithmetically correct ones (6/28 and 2/23, with "
        "those numerators stated in the text), while the abstract's reconstruct as mis-denominated. "
        "This row had cited the abstract's HIGHER NSCLC figure, overstating benefit by ~4.7 points. "
        "(ii) 'MONOTHERAPY' IS NOT TRUE OF THE WHOLE COHORT: 3 of 28 NSCLC patients received "
        "concurrent pemetrexed by design, so it is 48 of 51, not 51 of 51. (iii) the 1.6 and 1.4 "
        "months are INTRACRANIAL PFS specifically; the NSCLC EXTRACRANIAL PFS was 4.9 months, three "
        "times the quoted figure, so 'median PFS' unqualified is materially misleading. "
        "Volumetric decrease 22.7% and 18.8%. "
        "The authors' own conclusion is the sentence this project must carry: 'although abemaciclib "
        "can achieve therapeutic concentrations in brain metastases tissue, this study did not meet "
        "its primary endpoint... further clinical trials should focus on the use of abemaciclib "
        "COMBINATION therapy' (PMID 41768125, DOI 10.1093/noajnl/vdag005). "
        "WHY IT DOES NOT SINK THE ROW, stated so this is neither buried nor overread: the trial is "
        "indirect on disease (NSCLC and melanoma brain metastases, not primary CNS histiocytic "
        "sarcoma), it is MONOTHERAPY where this project uses the agent in combination, and -- the "
        "point that matters most -- it was NOT SELECTED for the genotype that makes CDK4/6 "
        "inhibition rational, whereas NCT04391595 above was selected for exactly that genotype and "
        "did show target engagement. So the two results are compatible: reaching the tissue is "
        "measured, and reaching it is not sufficient WITHOUT the lesion and without a partner. That "
        "is the 'brain-penetrant is not brain-effective' caveat the project already states, now "
        "instantiated a second time, in 51 patients, on this project's own lead agent. It is a "
        "STRENGTH-OF-EVIDENCE correction under rule 5, not a margin change.\n"
        "AND THE AUTHORS SAY SO THEMSELVES, WHICH IS STRONGER THAN THE PARAPHRASE ABOVE AND WAS "
        "MISSING UNTIL 2026-11-04. The trial's own surgical cohort measured unbound abemaciclib in "
        "brain-metastasis tissue at 96x the CDK4 and 19x the CDK6 in-vitro IC50, and the authors "
        "write that 'failure to achieve a therapeutic concentration in brain metastases is unlikely "
        "to be the etiology of this study's lack of response', attributing it instead to late-line "
        "therapy, high symptomatic disease burden, and primary or acquired resistance. TWO "
        "CONSEQUENCES THIS ROW MUST CARRY. First, the 19-96x figure cited at the TOP of this row as "
        "the project's favourable CDK4/6 access evidence COMES FROM THIS SAME TRIAL -- the "
        "project's best access number and its starkest efficacy negative are one dataset, which the "
        "catalogue had been presenting as two independent things. Second, it fixes the DIRECTION in "
        "which this trial may be used: it is evidence that access is INSUFFICIENT for CDK4/6 "
        "monotherapy, and it is NOT evidence that the drug fails to reach an intracranial site. "
        "Using it the latter way would reverse its meaning, and it cuts against any rule-14 "
        "inference -- here the measurement in the compartment at issue is POSITIVE and the clinical "
        "result is still negative. Scope, for completeness: heavily pre-treated and pre-irradiated "
        "(prior brain radiation in 20/28 and 16/23), KPS <=80 in ~57%, median two cycles received; a "
        "0% response rate in that setting does not transfer to an early-detection premise. And "
        "NCT02308020 enrolled 162 patients overall, so this is not a 51-patient trial.",
        "MEASURED (class, canine HS): palbociclib inhibited growth in ALL canine histiocytic lines "
        "including localized-HS lines, with CDKN2A down and Rb preserved, plus a xenograft "
        "(PMID 35278028).",
        Availability.EXISTS_TODAY,
        "A BRAIN-PENETRANT SELECTIVE CDK2 INHIBITOR NOW HAS A REGISTRY RECORD, added 2026-11-03, "
        "and it bears on escape A15 (RB1 loss / CDK2-cyclin E bypass of this very arm). NCT07524140, "
        "'A Phase 1, First-in-Human Study of ZE94-0605 in Patients With Advanced Solid Tumors', "
        "Eilean Therapeutics, RECRUITING, n=60, whose registry keyword list contains verbatim "
        "'Brain-penetrant CDK2 inhibitor' alongside 'Selective CDK2 inhibitor' and 'CCNE1 "
        "amplification'. GRADED THE SAME WAY THIS PROJECT GRADES AMG 193's 'CNS-penetrant': that is "
        "a SPONSOR DESCRIPTOR in a registry field, not a measured concentration, and it must not be "
        "read as a Kp,uu. What it establishes is narrower and still useful -- that the successor "
        "agent A15 would need is now in first-in-human development rather than hypothetical, which "
        "moves it from THEORETICAL to NEAR_FUTURE on the modality tier while supplying no number. "
        "Abemaciclib and palbociclib are both human-licensed and dosed in dogs off-label; "
        "palbociclib's canine-HS activity is measured. THE MOST IMPORTANT EXISTS-TODAY ENTRY IN THE "
        "TABLE: it is the only class that is simultaneously obtainable, measured in canine HS, and "
        "clears the parenchymal access bar on its own measured exposure (min access 0.0031 against "
        "a generic small-molecule 0.021). Its limit is that CDK4/6 inhibition is cytoSTATIC, so it "
        "holds rather than clears -- which is exactly what maintenance needs and not what induction "
        "needs.",
    ),
    Modality(
        "targeted small molecules -- synthetic lethality on the germline lesion (PRMT5, MAT2A)",
        Status.IN_MODEL,
        "MTA-cooperative PRMT5 inhibitor (TNG456); MAT2A inhibitor (IDE397 class)",
        "The genotype-anchored maintenance arm -- the only one aimed at the germline lesion itself, "
        "so the only one that is automatically matched to a second primary. Brain evidence is the "
        "weak point: no MTAP-directed agent has human CNS activity data yet.",
        "NONE IN THIS DISEASE. Zero records for PRMT5 inhibitors in canine cells. The gate is one "
        "MTAP immunostain; the region containing MTAP is deleted in 62.8% of canine HS "
        "(PMID 21341759).",
        Availability.NEAR_FUTURE,
        "Human Phase I/II only; no veterinary access and no canine PK for either chemotype. This is "
        "condition C7 in deterministic_closure -- a sponsor decision, not a scientific gap. The "
        "exists-today stand-in for the same axis is dietary methionine restriction, which lowers SAM "
        "in the same direction and is excluded below on toxicity, so there is NO exists-today "
        "substitute for this arm.",
    ),
    Modality(
        "targeted small molecules -- lineage survival (CSF1R)",
        Status.EXCLUDED,
        "pexidartinib; BLZ945 as the brain-penetrant class member",
        "RE-GROUNDED UNDER RULE 13. The old ground was 'not obtainable for a dog', which rule 13 "
        "forbids. The admissible ground is that a named escape defeats the class: CSF1R-independence "
        "is OBSERVED as acquired resistance in human histiocytosis, i.e. the lineage-survival route "
        "reroutes around the inhibitor, so the class cannot anchor a decade even where it works at "
        "first. A second, independent ground compounds it -- the inhibitor depletes microglia, which "
        "in this patient are the NORMAL COUNTERPART of the tumour, so the toxicity lands on the "
        "same lineage as the effect. The lineage escape is closed instead by lineage REMOVAL "
        "(liposomal clodronate, which has canine in-vivo regression data) plus the genotype arm.",
        "None in canine HS. The ground is the human-histiocytosis resistance observation, which "
        "transfers as a CLASS mechanism (receptor-independence of a myeloid-lineage tumour), not as "
        "a species-specific efficacy claim.",
        Availability.NEAR_FUTURE,
        "Pexidartinib is human-licensed but carries a hepatotoxicity REMS; BLZ945 is "
        "investigational; neither is dosed in dogs. RECORDED, NOT USED AS THE REASON.",
        ExclusionGround.DEFEATED_BY_ESCAPE,
    ),
    Modality(
        "epigenetic / transcriptional agents (HDAC, BET, DNMT)",
        Status.EXCLUDED,
        "vorinostat / BET inhibitors",
        "RE-GROUNDED UNDER RULE 13, and the arithmetic is now computed rather than asserted. The old "
        "ground led with 'no canine-HS activity data'. The admissible ground is toxicity: the "
        "induction backbone and the maintenance pill already load the marrow and GI axes, and "
        "`epigenetic_toxicity_arithmetic()` reads the LIVE remaining headroom out of core.toxicity "
        "and compares it with this class's transferred marrow burden. The class also offers no "
        "brain-penetration advantage over agents already in the model. It would be reconsidered if "
        "the ferroptosis arm were revived (HDACs brake persister ferroptosis), but that arm is "
        "dropped as counter-indicated in a macrophage-lineage tumour.",
        "None in canine HS. The marrow burden is a TRANSFER from human grade 3/4 thrombocytopenia "
        "and neutropenia rates for the class, which is the admissible way to test a class with no "
        "canine data (rule 13) -- see epigenetic_toxicity_arithmetic().",
        Availability.EXISTS_TODAY,
        "Vorinostat is human-licensed with published canine PK, and valproate has been given to dogs "
        "with cancer. Obtainable; excluded anyway, on the budget.",
        ExclusionGround.TOXICITY_UNAFFORDABLE,
    ),
    Modality(
        "monoclonal antibodies / checkpoint inhibitors",
        Status.IN_MODEL,
        "anti-PD-1 (gilvetmab); anti-CD47 as the phagocytosis-restoring option",
        "Supplementary antigen-directed arm. Antibody access to invaded parenchyma is 0.001, so the "
        "role is blood-side and meningeal, not parenchymal.",
        "Limited: PD-L1/PD-L2 expression reported in a human primary CNS HS case; canine-HS efficacy "
        "unmeasured. No canine anti-CD47 product exists.",
        Availability.EXISTS_TODAY,
        "Gilvetmab is a caninized anti-PD-1 with conditional USDA licensure, so this arm is "
        "obtainable for a dog today. The anti-CD47 option is to-build and is not load-bearing.",
    ),
    Modality(
        "antibody-drug conjugates (ADCs)",
        Status.EXCLUDED,
        "a CD204- or CD11c-directed ADC",
        "NEWLY ASSESSED. Excluded on this project's own delivery arithmetic: antibody access to "
        "invaded parenchyma is 0.001 (core.catalogue.ANTIBODY_ACCESS), three orders of magnitude "
        "below the small-molecule figure at the site that forced the local-delivery programme, and "
        "two orders below the required access of 0.196. An ADC's payload advantage cannot recover a "
        "1000-fold access deficit, so the derived kill at that site is below the growth bar whatever "
        "the payload -- the kill is contradicted by arithmetic, not by missing data. Retains a "
        "theoretical role in the leptomeningeal/blood-side compartment, where antibody access is "
        "0.01 -- still an order of magnitude below the liposome that is already there. "
        "FLAGGED FOR RE-TEST, 2026-10-31. This ground is an INFERENCE INTO the compartment (a "
        "generic antibody-access figure scaled by a payload advantage), and rule 14 says a "
        "measurement in the compartment at issue outranks any inference into it. A Phase 0/1 trial "
        "of a B7-H3-directed ADC in recurrent grade 4 glioma and brain metastases is now recruiting "
        "(GSK5764227, NCT07268053, start 2026-02-11), and its Phase 0 design selects the surgical "
        "window by the highest median unbound PAYLOAD concentration in gadolinium-NON-ENHANCING "
        "tissue -- i.e. it measures exactly the quantity this exclusion currently infers, for the "
        "payload rather than the antibody. B7-H3 is also a plausible histiocytic target. The "
        "exclusion stands for now, because no concentration has been reported and the arithmetic is "
        "the best estimate available; but when that trial reports, this ground must be recomputed "
        "against the measured payload figure rather than defended. Recorded so the re-test is not "
        "left to memory.",
        "None in canine HS. The exclusion does not rest on that: it rests on the compartment access "
        "figures, which are measured and already in the model.",
        Availability.NEAR_FUTURE,
        "No canine ADC against a histiocytic antigen exists. RECORDED, NOT USED AS THE REASON -- the "
        "access arithmetic would exclude it even if one were licensed tomorrow.",
        ExclusionGround.KILL_CONTRADICTED,
    ),
    Modality(
        "bispecific T-cell engagers",
        Status.EXCLUDED,
        "a CD3 x CD204 engager",
        "NEWLY ASSESSED, and RE-GROUNDED UNDER RULE 13 -- the old wording leaned on 'no canine "
        "construct exists'. The admissible ground is that named escapes defeat it: HS is a tumour OF "
        "the antigen-presenting myeloid lineage, so an engager recruits T cells against the cell "
        "type that primes them, and the tumour is simultaneously exporting an immunosuppressive "
        "metabolite into its own microenvironment (escape_audit.A16, MTA export from the MTAP-null "
        "lesion) -- the same mechanism that suppresses the floor tier's immune half. Antigen loss "
        "with MHC-I intact (escape 6) is a third route past it. The antibody-access deficit at the "
        "parenchymal site compounds all of that.",
        "None. The grounds are the escape ledger's own routes plus the compartment access model, "
        "both already in the project.",
        Availability.NEAR_FUTURE,
        "No canine bispecific construct exists. RECORDED, NOT USED AS THE REASON.",
        ExclusionGround.DEFEATED_BY_ESCAPE,
    ),
    Modality(
        "adoptive cell therapy (CAR-T, CIK, NK)",
        Status.IN_MODEL,
        "CD204-directed cell therapy (structurally the best answer)",
        "Kept in the model as the structural benchmark, with access 0.50 because a trafficking cell "
        "crosses actively rather than diffusing -- the one modality that is lineage-directed, "
        "non-antigen-dependent in the relevant sense, and not division-gated. Canine feasibility is "
        "real but early: B7-H3 CAR-CIK against canine sarcoma, first-in-dog expanded NK cells, and "
        "adoptive T-cell therapy after chemotherapy all exist in dogs.",
        "None in HS specifically. Canine cell-therapy platforms exist in other canine tumours "
        "(PMID 40944715, PMID 38631708, PMID 22355761).",
        Availability.NEAR_FUTURE,
        "The PLATFORM exists in dogs (canine CAR-CIK, expanded NK, adoptive T cells, all published) "
        "but no CD204- or histiocyte-directed canine construct does, so the specific agent is "
        "to-build. It is kept in the model as a structural benchmark and is not load-bearing for any "
        "closure -- availability_tiers checks that.",
    ),
    Modality(
        "haematopoietic stem-cell / marrow transplant",
        Status.EXCLUDED,
        "autologous or allogeneic peripheral-blood HSC transplant with total-body irradiation",
        "NEWLY ASSESSED, and the exclusion is on BIOLOGY, not feasibility -- which makes it a strong "
        "exclusion rather than a gap, and makes it rule-13-clean as written. Transplant is "
        "established in dogs (autologous PBSC for B- and T-cell lymphoma, allogeneic PBSC, with "
        "published post-mortem series). But the rationale for transplant in a germline-predisposed "
        "histiocytic tumour would be to replace the predisposed cell of origin, and that fails here: "
        "adult resident microglia are YOLK-SAC-derived and self-renewing, NOT marrow-derived "
        "(PMID 20966214). Replacing the marrow does not replace the brain-resident histiocytic "
        "compartment, so it cannot remove the predisposition at the site that matters, while adding "
        "total-body irradiation and graft-versus-host risk. Would be a different calculation for the "
        "disseminated form, which is not this case.",
        "Established in canine LYMPHOMA (PMID 24467413, PMID 22882500, PMID 35789057); never "
        "reported for canine HS.",
        Availability.EXISTS_TODAY,
        "ESTABLISHED IN DOGS -- the one excluded class that is fully obtainable. That is what makes "
        "the exclusion informative: it is not availability that rules it out.",
        ExclusionGround.KILL_CONTRADICTED,
    ),
    Modality(
        "therapeutic vaccines / active immunotherapy",
        Status.IN_MODEL,
        "an autologous tumour-cell or defined-antigen vaccine",
        "Present in the regimen for the lung/disseminated site, and explicitly discounted at the "
        "brain: antigen loss with MHC-I intact (escape 6) defeats an antigen-directed arm and the "
        "NK missing-self backstop never fires, which is why the closure is carried by "
        "position-independent agents instead. A vaccine kill rate in a dog is a named open "
        "experiment in the report.",
        "None in canine HS. The vaccine/immune kill rate in a dog is listed as a decisive experiment.",
        Availability.EXISTS_TODAY,
        "Autologous tumour-cell vaccines are prepared and given to dogs in veterinary oncology "
        "practice, so the modality is obtainable. It is IN the model and NOT load-bearing at the "
        "brain, which is the honest position -- it is discounted on escape 6, not on availability.",
    ),
    Modality(
        "cytokines / innate agonists",
        Status.EXCLUDED,
        "resiquimod (TLR7/8); IL-2",
        "RE-GROUNDED UNDER RULE 13. The ground is a mechanistic contradiction specific to this "
        "tumour, not missing data: HS is a tumour OF the TLR-bearing antigen-presenting lineage, so "
        "the same dose that activates innate immunity also signals the tumour's own receptors. The "
        "direction of the net effect is therefore not established even in principle, which is a "
        "contradiction of kill rather than an absence of measurement -- and in a tumour already "
        "exporting an immunosuppressive metabolite (escape_audit.A16) the immune arm is the half "
        "least able to carry a decade. Retained as a candidate SUPPLEMENT if the floor tier's immune "
        "arm needs support, and as an enumerated in-vitro experiment on canine HS cells.",
        "None; resiquimod on canine HS cells is an enumerated open experiment. The ground is the "
        "lineage-receptor overlap, which is a class mechanism.",
        Availability.EXISTS_TODAY,
        "Imiquimod/resiquimod are used topically in dogs and IL-2 has been given to dogs. "
        "Obtainable; excluded on the mechanism.",
        ExclusionGround.KILL_CONTRADICTED,
    ),
    Modality(
        "oncolytic virotherapy",
        Status.EXCLUDED,
        "BoHV4EGFPdeltaTK (recombinant bovine herpesvirus 4)",
        "NEWLY ASSESSED -- previously mentioned in the report's 'also noted' without a status, which "
        "rule 9 forbids -- and RE-GROUNDED UNDER RULE 13, because 'in-vitro only' is a data "
        "statement and not a ground. The admissible ground is that a named escape defeats it: the "
        "virus must be injected into a lesion that is ALREADY KNOWN, so it does nothing about the "
        "second primary -- a new tumour arising elsewhere from the same germline deletion -- and "
        "that route is precisely the one the decade turns on (the breed is born predisposed, so "
        "clearing one tumour does not clear the fault). It also cannot be dosed indefinitely, so it "
        "fails the continuous-duty condition C3. Genuine canine-HS in-vitro activity with "
        "tumour-selective tropism means it keeps a role at the resection cavity for INDUCTION; it is "
        "the maintenance claim that is excluded.",
        "MEASURED in vitro: infects and kills canine HS lines with apoptosis and raised GSDM-D, "
        "sparing fibroblasts (PMID 42517970). The best canine-HS data of any excluded class.",
        Availability.NEAR_FUTURE,
        "A research construct, not a product. RECORDED, NOT USED AS THE REASON -- the second-primary "
        "route would exclude it from maintenance even if it were licensed.",
        ExclusionGround.DEFEATED_BY_ESCAPE,
    ),
    Modality(
        "radiation",
        Status.IN_MODEL,
        "fractionated external-beam; craniospinal for the leptomeningeal compartment",
        "Access 1.0 and antigen-indifferent by physics; still division-gated, so it does not reach "
        "persisters. The computed toxicity collision -- full-dose radiation plus the CNS microtubule "
        "agent oversubscribe the normal-brain axis (0.80 + 0.70) -- forces sequencing or local "
        "delivery instead of whole-brain treatment.",
        "MEASURED outcome data: the model's prediction that radiation alone fails is validated "
        "against measured medians.",
        Availability.EXISTS_TODAY,
        "Fractionated external-beam radiotherapy is routine veterinary practice. Together with "
        "surgery it is the whole of the exists-today INDUCTION programme -- see availability_tiers.",
    ),
    Modality(
        "surgery / cytoreduction",
        Status.IN_MODEL,
        "debulking of the extra-axial mass; the resection cavity as a delivery route",
        "Load-bearing but explicitly NOT curative here: the tumour invades (23/23 dogs) and seeds "
        "the leptomeninges (19/19), so surgery removes the part drugs could reach and leaves the "
        "parts they cannot. Its real contribution is the cavity it creates for local delivery.",
        "MEASURED: the 568-day median after debulking plus lomustine in localized HS is the honest "
        "comparator for the whole analysis.",
        Availability.EXISTS_TODAY,
        "Routine. The measured 568-day median IS the exists-today induction result, which is why "
        "availability_tiers can state the exists-today programme's outcome from data rather than "
        "from the model.",
    ),
    Modality(
        "sanctuary-site / local delivery",
        Status.IN_MODEL,
        "intrathecal bolus (obtainable); convection-enhanced delivery; drug-eluting cavity implant; "
        "focused ultrasound BBB opening. Two further device modalities were assessed and are NOT "
        "scored, each for a stated reason rather than for absent canine data: HISTOTRIPSY, which in "
        "the first-in-dog brain series could not be delivered transcranially and was applied through "
        "a cranial defect, and H-FIRE, which needs electrodes placed through craniotomy defects. "
        "Both are single-session ablative procedures, so neither supplies the continuous presence "
        "C3 requires, and both are strictly more invasive than the backup that already closes.",
        "Removes penetration as a constraint by construction (access 1.0) where it is used. The "
        "delivery analysis demoted this from a requirement to a BACKUP: the required access is 0.196 "
        "/ 0.0145, which intrinsic molecular penetration already clears, so no procedure is on the "
        "critical path. Intrathecal dosing exceeds the computed CSF bar by orders of magnitude in "
        "BULK CSF; the open quantity is fluid-to-cell transfer.",
        "FUS BBB opening and convection-enhanced delivery have both been performed in dogs; "
        "intrathecal dosing in dogs runs about 1 complication in 112.",
        Availability.EXISTS_TODAY,
        "Intrathecal bolus, CED and FUS have all been done in dogs, so the BACKUP route is "
        "obtainable. The sustained-release intrathecal product is to-build (DepoCyt discontinued "
        "2017) and is NOT required -- it was only needed under the duty-0.07 framing.",
    ),
    Modality(
        "metabolic / dietary intervention",
        Status.EXCLUDED,
        "methionine restriction (to deepen the MAT2A/PRMT5 axis)",
        "RE-GROUNDED UNDER RULE 13. The old ground was 'unmeasured in dogs', which rule 13 forbids. "
        "The admissible ground is toxicity, and it is specific: dietary methionine restriction "
        "deliberately limits an essential amino acid, and the cost over the YEARS this regimen runs "
        "is lean-mass loss in an older large-breed dog that is simultaneously carrying a continuous "
        "cytotoxic. The relevant number is not an efficacy measurement but a tolerability one, and "
        "it cannot be afforded for a decade. Retained as a short-term ADJUNCT to the MTAP arm, where "
        "it lowers SAM in the same direction as MAT2A inhibition -- which matters because it is the "
        "nearest exists-today stand-in for the to-build genotype-anchored agent.",
        "None in canine HS. The ground is the sustained-restriction tolerability argument, which "
        "transfers from protein-restriction data as a CLASS effect on lean mass.",
        Availability.EXISTS_TODAY,
        "A diet is obtainable by definition. Excluded on what years of it costs, not on access.",
        ExclusionGround.TOXICITY_UNAFFORDABLE,
    ),
    Modality(
        "ferroptosis induction",
        Status.EXCLUDED,
        "lipophilic statin; sulfasalazine (system xc-)",
        "DROPPED as counter-indicated, and the reasoning runs the opposite way to the original "
        "intuition: HS is a macrophage-lineage tumour, canine HS upregulates ferroportin and "
        "ferritin, and macrophages are described as the ferroptosis-RESISTANT cell of the "
        "microenvironment. So a ferroptosis inducer targets the lineage least likely to die of it. "
        "The escape it was meant to answer (escape 8) is closed by the position-independent "
        "cytotoxic instead. Rule-13-clean as written: the ground is the canine-HS iron-handling "
        "expression data, which contradicts the kill.",
        "MEASURED, and measured UNFAVOURABLE: canine HS upregulates ferroportin and ferritin. The "
        "lineage argument is the basis for dropping it.",
        Availability.EXISTS_TODAY,
        "Statins and sulfasalazine are obtainable and dosed in dogs. Excluded on the lineage biology.",
        ExclusionGround.KILL_CONTRADICTED,
    ),
    Modality(
        "live bacterial vector / intracellular delivery platform",
        Status.EXCLUDED,
        "attenuated Listeria monocytogenes-derived 'quasiorganelles' delivering a genetic payload "
        "into tumour and immune cells (MSU pilot in dogs with HS, Morris Animal Foundation "
        "26CAANEI-0062, start 2026-01-31); Listeria- and Salmonella-vectored cancer immunotherapy "
        "in humans (axalimogene filolisbac, VNP20009, Clostridium novyi-NT)",
        "FOUND AS A RULE-9 HOLE on 2026-10-31 -- the class was absent from the universe entirely "
        "while an enrolling dog trial used it in THIS DISEASE -- then ASSESSED and excluded on "
        "2026-10-31 once its access mechanism was read at primary source. It was carried at "
        "NOT_ASSESSED in between, deliberately, rather than graded on a guess. "
        "THE GROUND IS A DERIVED SITE MISMATCH, not absent canine data. Bacterial tumour tropism is "
        "documented as driven by HYPOXIA, NECROSIS and aberrant vasculature, with hypoxic/necrotic "
        "regions described as the preferred sites of colonisation; engineered obligate anaerobes are "
        "built to replicate strictly in necrotic cores and explicitly NOT to persist in normoxic "
        "tissue. In the one directly relevant brain study the bacteria do not themselves cross an "
        "intact barrier at all: attenuated Salmonella colonises the hypoxic region, repolarises "
        "macrophages, downregulates P-gp and RECRUITS NEUTROPHILS, and the payload crosses by "
        "hitchhiking those neutrophils (PMC9978951, Acta Pharm Sin B, mouse glioma, 8e6 CFU). "
        "The site that decides this case is the INVADING EDGE BEHIND AN INTACT BARRIER -- the least "
        "hypoxic, least necrotic part of the tumour, and the one compartment this tropism does not "
        "select for. So the kill at the site that matters is contradicted by the mechanism's own "
        "documented behaviour, which is what ExclusionGround.KILL_CONTRADICTED means by 'at this "
        "site'. No search found colonisation measured at a normoxic tumour margin or invasive front "
        "in any species. "
        "A SECOND, INDEPENDENT GROUND, recorded because it would bite even if access were solved: "
        "the class cannot be CO-ADMINISTERED with this programme. The MSU protocol excludes "
        "immunosuppressants, systemic antibiotics within 14 days, neutropenia and immune-mediated "
        "disease, and any prior anti-cancer treatment (no chemotherapy within 14 days, no radiation "
        "within 30) -- while this programme runs continuous myelosuppressive maintenance at 95% of "
        "the marrow axis after debulking and radiation. A live attenuated bacterium given for years "
        "to a myelosuppressed dog is a listeriosis/sepsis exposure, not a tolerable addition. "
        "WHAT WOULD REOPEN IT, stated so the exclusion is falsifiable: a measured colonisation or "
        "payload-expression figure in gadolinium-NON-ENHANCING tumour tissue, in any species. That "
        "would defeat the site-mismatch ground directly. The hypoxic/necrotic CORE of the "
        "extra-axial mass is the one compartment where this class retains a theoretical role, the "
        "same way the ADC exclusion retains a leptomeningeal note -- and that is not the compartment "
        "the decade turns on.",
        "None for this case. The MSU pilot is the first administration to dogs with naturally "
        "occurring HS and has not reported. Its own framing -- 'tested in laboratory and preclinical "
        "studies but not yet in dogs with naturally occurring cancer' -- is the honest status. "
        "Human experience is also cautionary rather than supportive: reviews record that the "
        "attenuation required for safety compromised antitumour immunity and that early clinical "
        "trials did not reproduce preclinical success.",
        Availability.EXISTS_TODAY,
        "Obtainable TODAY through a named, funded, enrolling dog trial in this disease -- which is "
        "why leaving the class unenumerated was a defect, and why the exclusion rests on site "
        "access and co-administration rather than on availability.",
        ExclusionGround.KILL_CONTRADICTED,
    ),
    Modality(
        "autophagy inhibition",
        Status.IN_MODEL,
        "hydroxychloroquine",
        "Retained but near-free to drop (margin cost ~2e-5). Its value is that it is the only agent "
        "in the project with any canine phase I at all.",
        "TRANSFER: canine LYMPHOMA phase I, 12.5 mg/kg/day, ~100x tumour accumulation. Unmeasured in "
        "canine HS.",
        Availability.EXISTS_TODAY,
        "A completed canine Phase I with a published dose. The most unambiguously obtainable agent "
        "in the regimen.",
    ),
    Modality(
        "survival-signal inhibition (NF-kB)",
        Status.IN_MODEL,
        "parthenolide / DMAPT",
        "The only small molecule in the catalogue that is neither division-gated nor "
        "antigen-directed, so it reaches persisters and survives antigen loss. The escape's premise "
        "is contested by an 11-line finding that ERK/Akt activation does not predict response.",
        "MEASURED in canine HS: kills cell lines and primary cells dose-dependently; extends "
        "survival in a disseminated canine-HS mouse model.",
        Availability.NEAR_FUTURE,
        "Research-stage: parthenolide is a natural product with poor bioavailability and DMAPT has "
        "not been carried past early human study, with no canine formulation. Note the asymmetry "
        "with the PRMT5 arm -- this class has GOOD canine-HS data and no product, which is the "
        "cleanest illustration of why availability and evidence are separate axes.",
    ),
    Modality(
        "lineage depletion",
        Status.IN_MODEL,
        "liposomal clodronate",
        "Uptake by phagocytosis, so not division-gated and not antigen-directed. Access is "
        "ASYMMETRIC and that asymmetry is the useful part: it depletes blood-side perivascular and "
        "meningeal macrophages, not parenchymal microglia behind an intact barrier.",
        "MEASURED in canine malignant histiocytosis: in-vitro apoptosis, and 2/5 dogs with "
        "significant tumour regression in vivo (PMID 19760220).",
        Availability.EXISTS_TODAY,
        "ALREADY GIVEN TO DOGS WITH THIS LINEAGE OF TUMOUR, with in-vivo regression in 2/5 "
        "(PMID 19760220). Clodronate is licensed and the liposomal formulation is compoundable. The "
        "strongest exists-today entry after CDK4/6.",
    ),
    Modality(
        "molecular surveillance (not a therapy -- the enabler)",
        Status.IN_MODEL,
        "ctDNA / liquid biopsy detect-and-switch on the PTPN11 driver",
        "Not a modality but the term that converts reroutable maintenance from 0.56 to 0.81 in the "
        "durability model, so it belongs in the universe. The escape audit adds a new requirement: "
        "A15 (acquired RB1 loss) also needs this loop, and a hotspot-only assay can miss a "
        "divergent clone.",
        "MEASURED: a canine PTPN11 plasma assay with 91% detection and 98.8% specificity. Liquid "
        "biopsy in veterinary oncology more broadly remains review-level (PMID 42794612).",
        Availability.EXISTS_TODAY,
        "A canine PTPN11 plasma assay exists with measured detection and specificity, so the "
        "detect-and-switch loop that the reroutable tiers depend on is buildable from today's "
        "reagents. What is to-build is broad-panel canine HS ctDNA, which A15 would want.",
    ),
)


#: A class may sit at NOT_ASSESSED only by being named here. The import-time guard below still
#: raises for any unassessed class that is NOT on this list, so the thing it was built to stop --
#: a SILENT hole in the catalogue -- still fails loudly. The list was non-empty for one day: the
#: live-bacterial-vector class was found missing on 2026-10-31, carried here while its access
#: mechanism was read at primary source, and then EXCLUDED on a derived site mismatch the same day.
#: It was empty again by ASSESSMENT, not by deleting the row, which is the distinction that matters.
#:
#: IT IS NON-EMPTY AGAIN AS OF 2026-11-01, and this one does not resolve the same day. The
#: antimetabolite / nucleoside-analogue class was never a row, has three members measured active in
#: all ten canine HS lines, and cannot be excluded on any of rule 13's grounds -- so it is carried
#: here, openly, and the catalogue claim drops from "0 unassessed" to "1 open". That is a downgrade
#: of a headline this project has already published, which is the point: the alternative was to
#: write the class in as IN_MODEL without an agent wired into the regimen, and that would be the
#: overstatement rule 5 exists to stop.
#: UPDATED 2026-11-02. The antimetabolite class closed -- EXCLUDED on three measured canine-HS
#: IC50s, so it leaves this list by ASSESSMENT, exactly as the bacterial vector did. But the same
#: sweep found a THIRD never-enumerated class, targeted protein degradation, so the list is not
#: empty: one hole closes, another opens, and the count of classes goes 28 -> 29. Three holes in
#: three days is itself the finding -- see the docstring.
KNOWN_OPEN_CLASSES: tuple[str, ...] = (
    "targeted protein degradation / cereblon modulators (immunomodulatory imides, CELMoDs)",
    "nuclear export inhibition (XPO1 / SINE compounds)",
    "proteasome inhibition",
    "HSP90 inhibition",
    "cardiac glycosides / Na+,K+-ATPase inhibition",
    "translation-elongation inhibition",
    "apoptosis induction / BH3 mimetics (BCL-2, BCL-XL)",
    "interleukin-1 blockade as a tolerability enabler (not a tumour-kill modality)",
    "glucocorticoid-receptor agonists (corticosteroids)",
    "MDM2-p53 interaction inhibition",
    "nucleic-acid therapeutics (antisense oligonucleotide, siRNA)",
)

#: TWO HALLMARK COLUMNS WERE CONSIDERED AND JUDGED NOT TO MEET RULE 9's "COULD PLAUSIBLY MATTER"
#: BAR, recorded here rather than silently omitted so the judgement is reviewable:
#:   * DIFFERENTIATION THERAPY (retinoids / ATRA, the "unlocking phenotypic plasticity" column).
#:     Differentiation induction is lineage-specific and its one clinical success is APL, driven by
#:     PML-RARA. Canine HS is an already-differentiated myeloid/dendritic tumour with no analogous
#:     fusion, and there is no retinoid evidence in this lineage in any species. Not enumerated.
#:   * MICROBIOME MODULATION (the "polymorphic microbiomes" column). Its documented oncology effect
#:     is modulation of CHECKPOINT-INHIBITOR response, which this catalogue already carries as its
#:     own row; there is no route by which it reaches a primary intracranial mass as a therapy in
#:     its own right. Not enumerated.
#: Both are judgements about plausibility, not exclusions on rule 13 grounds -- which is why they sit
#: here as a stated decision rather than as EXCLUDED rows with a ground they do not have.


def _validate() -> None:
    names = [m.name for m in UNIVERSE]
    if len(names) != len(set(names)):
        raise ValueError("duplicate modality names")
    undeclared = [m.name for m in UNIVERSE
                  if m.status is Status.NOT_ASSESSED and m.name not in KNOWN_OPEN_CLASSES]
    if undeclared:
        raise ValueError(f"rule 9 violated: modality classes left unassessed: {undeclared}")
    stale = [n for n in KNOWN_OPEN_CLASSES
             if n not in {m.name for m in UNIVERSE if m.status is Status.NOT_ASSESSED}]
    if stale:
        raise ValueError(f"KNOWN_OPEN_CLASSES names a class that is no longer open: {stale}")
    # Rule 13: an exclusion without one of the three admissible grounds is not an exclusion.
    ungrounded = [m.name for m in UNIVERSE
                  if m.status is Status.EXCLUDED and m.exclusion_ground is None]
    if ungrounded:
        raise ValueError(f"rule 13 violated: EXCLUDED without an admissible ground: {ungrounded}")
    stray = [m.name for m in UNIVERSE
             if m.status is not Status.EXCLUDED and m.exclusion_ground is not None]
    if stray:
        raise ValueError(f"exclusion ground recorded on a non-excluded class: {stray}")


_validate()


def tally() -> dict[str, int]:
    out = {s.name: 0 for s in Status}
    for m in UNIVERSE:
        out[m.status.name] += 1
    return out


def availability_tally() -> dict[str, int]:
    """Rule-13 tier counts across the whole universe."""
    out = {a.name: 0 for a in Availability}
    for m in UNIVERSE:
        out[m.availability.name] += 1
    return out


def in_model() -> list[Modality]:
    return [m for m in UNIVERSE if m.status is Status.IN_MODEL]


def excluded() -> list[Modality]:
    return [m for m in UNIVERSE if m.status is Status.EXCLUDED]


def open_with_canine_hs_evidence() -> list[Modality]:
    """The open classes that already have a measurement in canine HS -- i.e. the ones worth working
    up first. Eleven open classes is a lot to read as one number, and they are not equivalent: five
    carry a canine-HS screen result and six carry nothing in this disease at all. A closure claim
    quantified over "11 open" without that split invites the reader to treat a pan-active screen hit
    and an unsearched mechanism as the same kind of gap."""
    return [m for m in not_assessed() if m.canine_hs_evidence.startswith("MEASURED")]


def open_without_canine_hs_evidence() -> list[Modality]:
    """The open classes with no measurement in this disease. Being here is NOT a rule-13 ground for
    exclusion and NOT a rule-11 gap to report -- it is a statement about where to look next."""
    return [m for m in not_assessed() if not m.canine_hs_evidence.startswith("MEASURED")]


def not_assessed() -> list[Modality]:
    """Must be empty for a rule-9-compliant closure claim."""
    return [m for m in UNIVERSE if m.status is Status.NOT_ASSESSED]


def exists_today_in_model() -> list[Modality]:
    """Classes in the model whose named representative is obtainable for a dog today (rule 13)."""
    return [m for m in in_model() if m.availability is Availability.EXISTS_TODAY]


def near_future_in_model() -> list[Modality]:
    """Classes in the model whose agent is clinical-stage but not yet obtainable for a dog.

    Under the user's 2026-10-02 clarification these COUNT toward closure, so they are no longer
    lumped with the theoretical.
    """
    return [m for m in in_model() if m.availability is Availability.NEAR_FUTURE]


def theoretical_in_model() -> list[Modality]:
    """Must be empty: a theoretical agent never counts toward closure (rule 13)."""
    return [m for m in in_model() if m.availability is Availability.THEORETICAL]


def to_build_in_model() -> list[Modality]:
    """Back-compatible name: classes in the model not obtainable for a dog TODAY, at any tier."""
    return [m for m in in_model()
            if m.availability in (Availability.NEAR_FUTURE, Availability.THEORETICAL)]


def excluded_by_ground() -> dict[str, list[str]]:
    """Exclusions grouped by their rule-13 ground, so no ground can hide an empty argument."""
    out: dict[str, list[str]] = {g.name: [] for g in ExclusionGround}
    for m in excluded():
        assert m.exclusion_ground is not None  # guaranteed by _validate
        out[m.exclusion_ground.name].append(m.name)
    return out


def excluded_citing_absent_canine_data() -> list[str]:
    """Rule-13 self-check: exclusions whose BASIS still leads on missing canine data.

    Must be empty. This is the lint that catches the lapse rule 13 was written for -- it looks for
    the forbidden phrasing in the ground-bearing text rather than trusting that it was cleaned up.
    The availability field is exempt by design: recording that no canine product exists is correct,
    as long as it is not the reason.
    """
    forbidden = ("not obtainable", "no canine product", "no canine construct", "in-vitro only",
                 "unmeasured in dogs", "no canine-hs activity data", "no canine data")
    out = []
    for m in excluded():
        low = m.basis.lower()
        # A mention inside an explicit RE-GROUNDED disclaimer is the correction, not the lapse.
        if "rule 13" in low or "rule-13" in low:
            continue
        if any(f in low for f in forbidden):
            out.append(m.name)
    return out


def epigenetic_toxicity_arithmetic() -> dict:
    """Compute, rather than assert, the ground for excluding the epigenetic class.

    Rule 13 requires that a class with no canine data be tested against a derived TRANSFER instead
    of being dropped. The transfer here is the class's MARROW burden, taken from the human grade 3/4
    thrombocytopenia and neutropenia rates that define HDAC-inhibitor dose-limiting toxicity, and the
    test is whether it fits the headroom the closing regimen actually leaves on that axis. The
    headroom is read LIVE out of core.toxicity via the regimen in core.microtubule_route, so this
    cannot drift away from the regimen it is about.
    """
    from .core import microtubule_route as mr
    from .core import toxicity as tox

    profiles = mr.toxicity_profiles()
    loads = tox.axis_loads(profiles)
    # TRANSFER, graded TRANSFERRED and not measured: an HDAC inhibitor is a marrow-DLT agent --
    # thrombocytopenia and neutropenia are what cap vorinostat's dose -- and it carries a GI burden
    # of the same order (nausea/diarrhoea are its commonest grade 3 events). Both are put at 0.45 of
    # their axis, the share a dose-limiting agent consumes at full dose elsewhere in core.toxicity.
    class_burden = {tox.Organ.MARROW: 0.45, tox.Organ.GI: 0.45}
    rows = {}
    for axis, add in class_burden.items():
        used = loads.get(axis, 0.0)
        rows[axis.name] = {
            "already_loaded_by_the_closing_regimen": round(used, 3),
            "headroom_remaining": round(1.0 - used, 3),
            "hdac_class_burden_transferred": add,
            "total_if_added": round(used + add, 3),
            "oversubscribed_if_added": used + add > 1.0,
        }
    blown = [a for a, r in rows.items() if r["oversubscribed_if_added"]]
    return {
        "axes": rows,
        "oversubscribed_axes_if_added": blown,
        "fits": not blown,
        "provenance": "TRANSFERRED -- the HDAC class's dose-limiting marrow and GI events from human "
                      "label-level data; no canine-HS number is used, and none is needed, because "
                      "the ground is tolerability rather than efficacy",
        "reading": (
            f"adding the class oversubscribes {', '.join(blown)}, so it makes the closing regimen "
            f"UNTOLERABLE rather than merely unproven -- an admissible rule-13 ground "
            f"(TOXICITY_UNAFFORDABLE), tested against a transfer rather than asserted from absence "
            f"of canine data"
            if blown else
            "the transferred burden fits the remaining headroom on every axis, so "
            "TOXICITY_UNAFFORDABLE is NOT an admissible ground here and this exclusion must be "
            "re-argued on kill or escape, or reversed"
        ),
    }


def with_canine_hs_evidence() -> list[Modality]:
    """Modality classes with any measurement in canine histiocytic sarcoma itself."""
    return [m for m in UNIVERSE if m.canine_hs_evidence.startswith("MEASURED")]


def newly_assessed() -> list[Modality]:
    """The classes this module assessed for the first time."""
    return [m for m in UNIVERSE if "NEWLY ASSESSED" in m.basis]


def regrounded_under_rule_13() -> list[Modality]:
    """The exclusions whose stated ground was replaced because it was a data-absence statement."""
    return [m for m in UNIVERSE if "RE-GROUNDED UNDER RULE 13" in m.basis]


def closure_claim(n_escapes: int) -> str:
    """The rule-9-shaped claim: closed within a STATED catalogue, with exclusions named."""
    t = tally()
    ex = "; ".join(m.name for m in excluded())
    g = excluded_by_ground()
    return (
        f"Closed within this catalogue of {len(UNIVERSE)} modality classes and {n_escapes} escape "
        f"routes: {t['IN_MODEL']} classes represented in the model, {t['EXCLUDED']} evaluated and "
        f"excluded with an admissible rule-13 ground recorded, {t['NOT_ASSESSED']} unassessed. "
        f"Grounds for exclusion: {len(g['KILL_CONTRADICTED'])} kill contradicted, "
        f"{len(g['DEFEATED_BY_ESCAPE'])} defeated by a named escape, "
        f"{len(g['TOXICITY_UNAFFORDABLE'])} toxicity unaffordable; "
        f"{len(excluded_citing_absent_canine_data())} excluded for absent canine data. "
        f"Outside the catalogue (excluded): {ex}. "
        f"{len(with_canine_hs_evidence())} classes carry a measurement in canine HS itself. "
        f"Of the {t['IN_MODEL']} classes in the model, {len(exists_today_in_model())} are obtainable "
        f"for a dog today and {len(to_build_in_model())} need an agent that does not exist yet."
    )


def statement() -> str:
    t = tally()
    new = ", ".join(m.name for m in newly_assessed())
    re_g = ", ".join(m.name for m in regrounded_under_rule_13())
    return (
        f"Therapy-modality universe for primary intracranial canine HS: {len(UNIVERSE)} classes "
        f"enumerated from the literature rather than from the agent list. {t['IN_MODEL']} in the "
        f"model ({len(exists_today_in_model())} obtainable today, {len(to_build_in_model())} "
        f"to-build), {t['EXCLUDED']} excluded on an admissible rule-13 ground, "
        f"{t['NOT_ASSESSED']} unassessed. "
        f"Newly assessed here: {new}. "
        f"RE-GROUNDED under rule 13 (the stated reason had been absence of canine data, which is not "
        f"a ground): {re_g}. The strongest exclusion is marrow transplant -- excluded on biology "
        f"(resident microglia are yolk-sac-derived and self-renewing, so replacing the marrow does "
        f"not replace the predisposed brain-resident compartment), not on feasibility, since "
        f"transplant is established in dogs for lymphoma."
    )
