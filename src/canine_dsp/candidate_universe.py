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
    engager asks T cells to kill the lineage that primes them. No canine product exists.
  * HAEMATOPOIETIC STEM-CELL / MARROW TRANSPLANT -- the interesting one, and the reason this module
    matters. It is established in dogs (autologous and allogeneic PBSC transplant for lymphoma, with
    total-body irradiation) so it is not infeasible. But resident microglia are YOLK-SAC-DERIVED and
    self-renewing (PMID 20966214), not marrow-derived, so replacing the marrow does not replace the
    cell of origin of a brain-resident histiocytic tumour. It is excluded on BIOLOGY rather than on
    feasibility -- and that is a much stronger exclusion than "not available for dogs".

ONCOLYTIC VIROTHERAPY was mentioned in the report but never assessed; it is now assessed and
retained as a supplementary local option with canine-HS in-vitro data.

THE HONEST EFFECT ON THE HEADLINE
---------------------------------
Enumerating the universe does not add a drug to the regimen. It converts "every escape is closed"
from a claim over an unstated list into a claim over a STATED one: closed within this catalogue of
N modality classes and M escapes, with the excluded classes named and the reason for each recorded.
That is the claim ``statement()`` returns.

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


@dataclass(frozen=True)
class Modality:
    """One therapy-modality class, with its status for this case."""

    name: str
    status: Status
    representative: str          # the agent in the model, or the class member considered
    basis: str                   # why this status -- data, arithmetic, or biology
    canine_hs_evidence: str      # what exists in this disease specifically, if anything


#: Enumerated from the modality list in CLAUDE.md rule 9, plus classes the HS literature names.
UNIVERSE: tuple[Modality, ...] = (
    Modality(
        "cytotoxic chemotherapy -- microtubule agents",
        Status.IN_MODEL,
        "colchicine-site tubulin binder (avanbulin class); vinca/taxane as the measured comparator",
        "The induction backbone, and the only pharmacology in this project measured in the right "
        "species and disease. Carries six of the twelve original escape closures -- a concentration "
        "the escape audit flags as a single point of failure (escape_audit.A13).",
        "MEASURED: 4 canine HS lines, vincristine IC50 1.77-2.69, vinblastine 1.75-2.78, paclitaxel "
        "23.8-58.4 ng/ml (PMID 25715778). Same paper: ABCB1/ABCG2 elevated.",
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
    ),
    Modality(
        "targeted small molecules -- MAPK axis (MEK/ERK/SHP2)",
        Status.IN_MODEL,
        "trametinib / cobimetinib / mirdametinib",
        "The maintenance arm for the ~59% MAPK-driver majority. Site-split: closes the lung "
        "systemically; brain closure depends on unmeasured canine CNS access.",
        "MEASURED: canine HS sensitivity surveyed; a canine Phase I exists (trametinib), ~30% of "
        "dogs underdosed at the MTD.",
    ),
    Modality(
        "targeted small molecules -- PI3K/AKT/mTOR axis",
        Status.IN_MODEL,
        "paxalisib; duvelisib as the better-grounded canine alternative",
        "Covers the RTK-bypass escape. The 2026 screen gives this axis real canine-HS grounding that "
        "the model's transferred hemangiosarcoma IC50s lacked.",
        "MEASURED (axis): duvelisib selective in one HS expression subgroup, median IC50 287 nM vs "
        ">5 uM in the other and 7.46 uM in normal PBMC (PMID 42129963). Paxalisib itself: transfer.",
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
    ),
    Modality(
        "targeted small molecules -- lineage survival (CSF1R)",
        Status.EXCLUDED,
        "pexidartinib; BLZ945 as the brain-penetrant class member",
        "Not obtainable for a dog, and carries a microglia-depletion hazard in a patient whose "
        "microglia are the normal counterpart of the tumour. The lineage escape is instead closed by "
        "lineage REMOVAL (liposomal clodronate) plus the genotype arm.",
        "None. Human histiocytosis data only, where CSF1R-independence is OBSERVED as resistance.",
    ),
    Modality(
        "epigenetic / transcriptional agents (HDAC, BET, DNMT)",
        Status.EXCLUDED,
        "vorinostat / BET inhibitors",
        "Assessed and excluded for THIS regimen rather than on principle: no canine-HS activity "
        "data, no brain-penetration advantage over agents already in the model, and the marrow and "
        "GI toxicity axes are already loaded by the induction backbone and the maintenance pill. "
        "Would be reconsidered if the ferroptosis arm were revived (HDACs brake persister "
        "ferroptosis), but that arm is dropped as counter-indicated in a macrophage-lineage tumour.",
        "None in canine HS.",
    ),
    Modality(
        "monoclonal antibodies / checkpoint inhibitors",
        Status.IN_MODEL,
        "anti-PD-1 (gilvetmab); anti-CD47 as the phagocytosis-restoring option",
        "Supplementary antigen-directed arm. Antibody access to invaded parenchyma is 0.001, so the "
        "role is blood-side and meningeal, not parenchymal. Gilvetmab is obtainable for dogs.",
        "Limited: PD-L1/PD-L2 expression reported in a human primary CNS HS case; canine-HS efficacy "
        "unmeasured. No canine anti-CD47 product exists.",
    ),
    Modality(
        "antibody-drug conjugates (ADCs)",
        Status.EXCLUDED,
        "a CD204- or CD11c-directed ADC (none exists for dogs)",
        "NEWLY ASSESSED. Excluded on this project's own delivery arithmetic: antibody access to "
        "invaded parenchyma is 0.001 (core.catalogue.ANTIBODY_ACCESS), three orders of magnitude "
        "below the small-molecule figure at the site that forced the local-delivery programme. An "
        "ADC's payload advantage cannot recover a 1000-fold access deficit. Retains a theoretical "
        "role in the leptomeningeal/blood-side compartment, where antibody access is 0.01 -- still "
        "an order of magnitude below the liposome that is already there.",
        "None. No canine ADC against a histiocytic antigen exists.",
    ),
    Modality(
        "bispecific T-cell engagers",
        Status.EXCLUDED,
        "a CD3 x CD204 engager (none exists for dogs)",
        "NEWLY ASSESSED. Two compounding reasons: the same antibody-access deficit at the "
        "parenchymal site, and a mechanistic conflict specific to this tumour -- HS is a tumour OF "
        "the antigen-presenting myeloid lineage, so an engager recruits T cells against the cell "
        "type that primes them, in a tumour already exporting an immunosuppressive metabolite "
        "(escape_audit.A16). No canine construct exists.",
        "None.",
    ),
    Modality(
        "adoptive cell therapy (CAR-T, CIK, NK)",
        Status.IN_MODEL,
        "CD204-directed cell therapy (structurally the best answer; does not exist for dogs)",
        "Kept in the model as the structural benchmark, with access 0.50 because a trafficking cell "
        "crosses actively rather than diffusing -- the one modality that is lineage-directed, "
        "non-antigen-dependent in the relevant sense, and not division-gated. Canine feasibility is "
        "real but early: B7-H3 CAR-CIK against canine sarcoma, first-in-dog expanded NK cells, and "
        "adoptive T-cell therapy after chemotherapy all exist in dogs.",
        "None in HS specifically. Canine cell-therapy platforms exist in other canine tumours "
        "(PMID 40944715, PMID 38631708, PMID 22355761).",
    ),
    Modality(
        "haematopoietic stem-cell / marrow transplant",
        Status.EXCLUDED,
        "autologous or allogeneic peripheral-blood HSC transplant with total-body irradiation",
        "NEWLY ASSESSED, and the exclusion is on BIOLOGY, not feasibility -- which makes it a strong "
        "exclusion rather than a gap. Transplant is established in dogs (autologous PBSC for B- and "
        "T-cell lymphoma, allogeneic PBSC, with published post-mortem series). But the rationale for "
        "transplant in a germline-predisposed histiocytic tumour would be to replace the "
        "predisposed cell of origin, and that fails here: adult resident microglia are YOLK-SAC-"
        "derived and self-renewing, NOT marrow-derived (PMID 20966214). Replacing the marrow does "
        "not replace the brain-resident histiocytic compartment, so it cannot remove the "
        "predisposition at the site that matters, while adding total-body irradiation and "
        "graft-versus-host risk. Would be a different calculation for the disseminated form.",
        "Established in canine LYMPHOMA (PMID 24467413, PMID 22882500, PMID 35789057); never "
        "reported for canine HS.",
    ),
    Modality(
        "therapeutic vaccines / active immunotherapy",
        Status.IN_MODEL,
        "an autologous or defined-antigen vaccine (referenced in the lung-site regimen)",
        "Present in the regimen for the lung/disseminated site, and explicitly discounted at the "
        "brain: antigen loss with MHC-I intact (escape 6) defeats an antigen-directed arm and the "
        "NK missing-self backstop never fires, which is why the closure is carried by "
        "position-independent agents instead. A vaccine kill rate in a dog is a named open "
        "experiment in the report.",
        "None in canine HS. The vaccine/immune kill rate in a dog is listed as a decisive experiment.",
    ),
    Modality(
        "cytokines / innate agonists",
        Status.EXCLUDED,
        "resiquimod (TLR7/8); IL-2",
        "Assessed and excluded as a primary arm: listed in the report as an open in-vitro experiment "
        "on canine HS cells, not as a closure. In a tumour of the antigen-presenting lineage an "
        "innate agonist may stimulate the tumour's own lineage receptors, so it is not a free "
        "addition. Retained as a candidate supplement if the floor tier's immune arm needs support.",
        "None; resiquimod on canine HS cells is an enumerated open experiment.",
    ),
    Modality(
        "oncolytic virotherapy",
        Status.EXCLUDED,
        "BoHV4EGFPdeltaTK (recombinant bovine herpesvirus 4)",
        "NEWLY ASSESSED -- previously mentioned in the report's 'also noted' without a status, which "
        "rule 9 forbids. Excluded as a maintenance arm, retained as a supplementary LOCAL option: "
        "it has genuine canine-HS in-vitro activity with tumour-selective tropism, but it is "
        "in-vitro only, requires local administration (so it does not reach a second primary "
        "anywhere else), and cannot be dosed indefinitely as maintenance, which is what the decade "
        "requires. It fits the resection cavity, alongside the implant.",
        "MEASURED in vitro: infects and kills canine HS lines with apoptosis and raised GSDM-D, "
        "sparing fibroblasts (PMID 42517970).",
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
    ),
    Modality(
        "sanctuary-site / local delivery",
        Status.IN_MODEL,
        "convection-enhanced delivery, drug-eluting cavity implant, intrathecal dosing; focused "
        "ultrasound BBB opening as the non-invasive lever",
        "Removes penetration as a constraint by construction (access 1.0) and is what closes the "
        "parenchymal site in the model. Intrathecal dosing exceeds the computed CSF bar by orders of "
        "magnitude in BULK CSF; the open quantity is fluid-to-cell transfer, which is why the CSF "
        "compartment still has no durability number.",
        "Formulation gap, not a biology gap: the sustained-release intrathecal product does not "
        "exist (DepoCyt discontinued 2017). FUS BBB opening has been performed safely in dogs.",
    ),
    Modality(
        "metabolic / dietary intervention",
        Status.EXCLUDED,
        "methionine restriction (to deepen the MAT2A/PRMT5 axis)",
        "Assessed and excluded as a standalone arm, retained as an adjunct to the MTAP arm: dietary "
        "methionine restriction lowers SAM in the same direction as MAT2A inhibition, but it is "
        "unmeasured in dogs, hard to sustain for years, and risks muscle loss in an older large-"
        "breed dog. It is named in the obtainable-today tier as the closest thing to the MTAP arm "
        "when the drugs are unavailable.",
        "None in canine HS.",
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
        "cytotoxic instead.",
        "Never studied in canine HS. The lineage argument is the basis for dropping it.",
    ),
    Modality(
        "autophagy inhibition",
        Status.IN_MODEL,
        "hydroxychloroquine",
        "Retained but near-free to drop (margin cost ~2e-5). Its value is that it is the only agent "
        "in the project with any canine phase I at all.",
        "TRANSFER: canine LYMPHOMA phase I, 12.5 mg/kg/day, ~100x tumour accumulation. Unmeasured in "
        "canine HS.",
    ),
    Modality(
        "survival-signal inhibition (NF-kB)",
        Status.IN_MODEL,
        "parthenolide / DMAPT",
        "The only small molecule in the catalogue that is neither division-gated nor "
        "antigen-directed, so it reaches persisters and survives antigen loss. Research-stage, not "
        "licensed. The escape's premise is contested by an 11-line finding that ERK/Akt activation "
        "does not predict response.",
        "MEASURED in canine HS: kills cell lines and primary cells dose-dependently; extends "
        "survival in a disseminated canine-HS mouse model.",
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
    ),
    Modality(
        "molecular surveillance (not a therapy -- the enabler)",
        Status.IN_MODEL,
        "ctDNA / liquid biopsy detect-and-switch on the PTPN11 driver",
        "Not a modality but the term that converts reroutable maintenance from 0.56 to 0.81 in the "
        "durability model, so it belongs in the universe. The escape audit adds a new requirement: "
        "A15 (acquired RB1 loss) also needs this loop, and a hotspot-only assay can miss a "
        "divergent clone.",
        "Canine HS ctDNA is unvalidated. Liquid biopsy in veterinary oncology remains a review-level "
        "aspiration (PMID 42794612).",
    ),
)


def _validate() -> None:
    names = [m.name for m in UNIVERSE]
    if len(names) != len(set(names)):
        raise ValueError("duplicate modality names")
    if any(m.status is Status.NOT_ASSESSED for m in UNIVERSE):
        unassessed = [m.name for m in UNIVERSE if m.status is Status.NOT_ASSESSED]
        raise ValueError(f"rule 9 violated: modality classes left unassessed: {unassessed}")


_validate()


def tally() -> dict[str, int]:
    out = {s.name: 0 for s in Status}
    for m in UNIVERSE:
        out[m.status.name] += 1
    return out


def in_model() -> list[Modality]:
    return [m for m in UNIVERSE if m.status is Status.IN_MODEL]


def excluded() -> list[Modality]:
    return [m for m in UNIVERSE if m.status is Status.EXCLUDED]


def not_assessed() -> list[Modality]:
    """Must be empty for a rule-9-compliant closure claim."""
    return [m for m in UNIVERSE if m.status is Status.NOT_ASSESSED]


def with_canine_hs_evidence() -> list[Modality]:
    """Modality classes with any measurement in canine histiocytic sarcoma itself."""
    return [m for m in UNIVERSE if m.canine_hs_evidence.startswith("MEASURED")]


def newly_assessed() -> list[Modality]:
    """The classes this module assessed for the first time."""
    return [m for m in UNIVERSE if "NEWLY ASSESSED" in m.basis]


def closure_claim(n_escapes: int) -> str:
    """The rule-9-shaped claim: closed within a STATED catalogue, with exclusions named."""
    t = tally()
    ex = "; ".join(m.name for m in excluded())
    return (
        f"Closed within this catalogue of {len(UNIVERSE)} modality classes and {n_escapes} escape "
        f"routes: {t['IN_MODEL']} classes represented in the model, {t['EXCLUDED']} evaluated and "
        f"excluded with reasons recorded, {t['NOT_ASSESSED']} unassessed. "
        f"Outside the catalogue (excluded): {ex}. "
        f"{len(with_canine_hs_evidence())} classes carry a measurement in canine HS itself."
    )


def statement() -> str:
    t = tally()
    new = ", ".join(m.name for m in newly_assessed())
    return (
        f"Therapy-modality universe for primary intracranial canine HS: {len(UNIVERSE)} classes "
        f"enumerated from the literature rather than from the agent list. {t['IN_MODEL']} in the "
        f"model, {t['EXCLUDED']} excluded with a recorded reason, {t['NOT_ASSESSED']} unassessed. "
        f"Newly assessed here: {new}. The strongest exclusion is marrow transplant -- excluded on "
        f"biology (resident microglia are yolk-sac-derived and self-renewing, so replacing the "
        f"marrow does not replace the predisposed brain-resident compartment), not on feasibility, "
        f"since transplant is established in dogs for lymphoma."
    )
