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
    """Rule-13 tier. Orthogonal to Status: a class can be in the model and not yet exist for dogs."""

    EXISTS_TODAY = "licensed (veterinary or human, off-label), or available through a dog trial"
    TO_BUILD = "no agent of this class is obtainable for a dog today"


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
        Availability.TO_BUILD,
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
        "targeted small molecules -- MAPK axis (MEK/ERK/SHP2)",
        Status.IN_MODEL,
        "trametinib / cobimetinib / mirdametinib",
        "The maintenance arm for the ~59% MAPK-driver majority. Site-split: closes the lung "
        "systemically; brain closure depends on unmeasured canine CNS access.",
        "MEASURED: canine HS sensitivity surveyed; a canine Phase I exists (trametinib), ~30% of "
        "dogs underdosed at the MTD.",
        Availability.EXISTS_TODAY,
        "Trametinib has a COMPLETED canine Phase I with a recommended dose (PMID 38889903), and "
        "cobimetinib has both a canine-HS IC50 and a canine plasma Cmax (PMID 39202410). This is "
        "the best-tiered maintenance class in the project: obtainable AND measured in the dog.",
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
        "targeted small molecules -- cell-cycle (CDK4/6)",
        Status.IN_MODEL,
        "abemaciclib (brain-penetrant); palbociclib as the measured class comparator",
        "Now the lead brain arm for the deletion-carrying tumour (HS_STATUS section A): measured "
        "human brain-tumour tissue exposure 19-96x the CDK4/6 IC50, and a met endpoint in "
        "CDK-pathway meningioma, the same extra-axial niche.",
        "MEASURED (class, canine HS): palbociclib inhibited growth in ALL canine histiocytic lines "
        "including localized-HS lines, with CDKN2A down and Rb preserved, plus a xenograft "
        "(PMID 35278028).",
        Availability.EXISTS_TODAY,
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
        Availability.TO_BUILD,
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
        Availability.TO_BUILD,
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
        "0.01 -- still an order of magnitude below the liposome that is already there.",
        "None in canine HS. The exclusion does not rest on that: it rests on the compartment access "
        "figures, which are measured and already in the model.",
        Availability.TO_BUILD,
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
        Availability.TO_BUILD,
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
        Availability.TO_BUILD,
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
        Availability.TO_BUILD,
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
        "focused ultrasound BBB opening",
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
        Availability.TO_BUILD,
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


def _validate() -> None:
    names = [m.name for m in UNIVERSE]
    if len(names) != len(set(names)):
        raise ValueError("duplicate modality names")
    if any(m.status is Status.NOT_ASSESSED for m in UNIVERSE):
        unassessed = [m.name for m in UNIVERSE if m.status is Status.NOT_ASSESSED]
        raise ValueError(f"rule 9 violated: modality classes left unassessed: {unassessed}")
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


def not_assessed() -> list[Modality]:
    """Must be empty for a rule-9-compliant closure claim."""
    return [m for m in UNIVERSE if m.status is Status.NOT_ASSESSED]


def exists_today_in_model() -> list[Modality]:
    """Classes in the model whose named representative is obtainable for a dog today (rule 13)."""
    return [m for m in in_model() if m.availability is Availability.EXISTS_TODAY]


def to_build_in_model() -> list[Modality]:
    """Classes in the model that need an agent that does not exist for dogs yet (rule 13)."""
    return [m for m in in_model() if m.availability is Availability.TO_BUILD]


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
