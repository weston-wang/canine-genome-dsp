"""What is distinctive about one breed's presentation of histiocytic sarcoma.

This module is a structured, importable reference summarizing the ways a single
genetically predisposed dog breed presents histiocytic sarcoma (HS) differently
from the textbook disease and from HS in other breeds -- biologically,
genomically, anatomically/clinically, and epidemiologically.

Every fact below is sourced from a long research conversation (distilled
transcript). Nothing here was pulled from the wider literature independently or
invented; where the conversation cited a primary paper, PMID, or PMC id, it is
carried through, and where the conversation flagged a claim as unverified,
extrapolated, a minority finding, or later retracted, that status is recorded in
the data rather than smoothed over.

Naming: the predisposed breed is deliberately never named. It is referred to only
as "the breed" / "this breed" / "the predisposed breed". Other breeds mentioned
purely for contrast (Bernese Mountain Dog, flat-coated retriever, golden
retriever) ARE named, since the constraint is only about not identifying the
subject breed. Two of the cited case series carry the breed name in their
published titles; those titles are therefore paraphrased rather than quoted.

Scope: pure standard-library Python. Importing this module has no side effects
and no third-party dependencies.

See PROVENANCE for the important caveat: this is an analysis of a specific dog
breed's disease derived from a research conversation. It is NOT veterinary advice
and must not be used to diagnose or treat any animal.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

__all__ = [
    "ANATOMICAL_CLINICAL_UNIQUENESS",
    "CANDIDATE_SOMATIC_DRIVERS",
    "CELL_OF_ORIGIN",
    "CITATIONS",
    "CONTRAST_BREEDS",
    "CORRECTIONS_AND_RETRACTIONS",
    "DISTINCTIVENESS_IN_ONE_LINE",
    "EPIDEMIOLOGICAL_PREDISPOSITION",
    "GENOMIC_UNIQUENESS",
    "GERMLINE_VS_SOMATIC",
    "OPEN_QUESTIONS",
    "PROVENANCE",
    "Citation",
    "DriverTier",
    "EvidenceStatus",
    "Fact",
    "all_facts",
    "facts_by_status",
    "summary",
]


# ---------------------------------------------------------------------------
# Provenance / disclaimer
# ---------------------------------------------------------------------------

PROVENANCE = """\
This module summarizes the DISEASE of one specific, deliberately-unnamed dog
breed -- its histiocytic sarcoma presentation -- as established across a long
research conversation. It is a reconstruction of that conversation's conclusions,
an analysis and reference only. It is NOT veterinary advice, NOT a diagnosis, and
NOT a treatment recommendation. The single most important caveat, repeated
throughout the source conversation: no tumor of this breed at either signature
site has ever been molecularly sequenced, so every genomic claim about the breed
specifically is an extrapolation from other breeds and from the wider HS
literature, not a measurement in this breed. Frequencies, odds ratios, and PMIDs
are reproduced only where they actually appear in the conversation.\
"""


# ---------------------------------------------------------------------------
# Vocabulary
# ---------------------------------------------------------------------------

class EvidenceStatus(Enum):
    """How well-supported a statement is, per the source conversation."""

    VERIFIED = "verified"          # checked against a primary source / measured data
    EXTRAPOLATED = "extrapolated"  # real data, but from other breeds/species/sites
    HYPOTHESIS = "hypothesis"      # a structured, explicitly-unproven proposal
    UNCONFIRMED = "unconfirmed"    # never measured for this breed; an open gap
    MINORITY = "minority"          # a real but minority / non-dominant finding
    RETRACTED = "retracted"        # a claim the conversation walked back


class DriverTier(Enum):
    """Tiering of candidate somatic drivers used in the conversation's panel."""

    A = "A: recurrent canine-HS somatic hotspot (sequenced in dogs)"
    B = "B: human-histiocytosis hotspot, never reported in a dog"
    C = "C: mechanistically motivated, no point-mutation hotspot to target"
    D = "D: germline/deletion lesion, not a somatic point-mutation neoantigen"


@dataclass(frozen=True)
class Citation:
    """A primary source referenced in the conversation.

    Titles that contain the breed name are paraphrased on purpose.
    """

    key: str
    authors_year: str
    what: str
    pmid: str | None = None
    pmc: str | None = None
    venue: str | None = None


@dataclass(frozen=True)
class Fact:
    """One distinctive-feature statement, with its evidence status and source."""

    statement: str
    status: EvidenceStatus
    citation_keys: tuple = ()
    note: str = ""


# ---------------------------------------------------------------------------
# Citation registry (only sources tied to the breed's HS or to direct contrasts)
# ---------------------------------------------------------------------------

CITATIONS = {
    "kishimoto_2020": Citation(
        key="kishimoto_2020",
        authors_year="Kishimoto, Uchida et al. 2020",
        what="Primary-intracranial-tumor case series, University of Tokyo; the "
             "breed-predisposition and cerebrum-only localization data (read from "
             "the full PDF, Table 5).",
        venue="J Vet Med Sci 82(1):77-83",
    ),
    "ide_2011": Citation(
        key="ide_2011",
        authors_year="Ide et al. 2011",
        what="15 subdural HS dogs; marked predominance of the breed (47%), "
             "focal-solitary-subdural vs diffuse-leptomeningeal split.",
        pmid="21217043",
        venue="J Vet Diagn Invest 23(1):127-32",
    ),
    "mariani_2015": Citation(
        key="mariani_2015",
        authors_year="Mariani et al. 2015",
        what="19 CNS HS dogs (retrievers and the breed overrepresented); "
             "meningeal enhancement in all, CSF pleocytosis in all, parenchymal "
             "invasion, 3-day median survival.",
        pmid="25711602",
        pmc="PMC4895499",
        venue="J Vet Intern Med 29(2):607-613",
    ),
    "thongtharb_2016": Citation(
        key="thongtharb_2016",
        authors_year="Thongtharb, Uchida, Chambers, Kagawa, Nakayama 2016",
        what="23 primary intracranial HS, 11/23 of the breed; all cases poorly "
             "demarcated and invading brain parenchyma; 'localized HS might be "
             "the main form of intracranial HS in dog'.",
        pmid="26668164",
        pmc="PMC4873849",
        venue="J Vet Med Sci 78(4):593-9",
    ),
    "toyoda_2020": Citation(
        key="toyoda_2020",
        authors_year="Toyoda et al. 2020",
        what="102 CNS HS dogs; meninges+parenchyma both involved, CSF neoplastic "
             "cells in 52%, definitive-therapy MST 44 days.",
        pmc="PMC7096655",
        venue="J Vet Intern Med",
    ),
    "wada_2017": Citation(
        key="wada_2017",
        authors_year="Wada et al. 2017",
        what="Imaging of solitary intracranial HS vs meningioma; all HS showed "
             "leptomeningeal enhancement and/or invasion into the sulci.",
        pmid="28335080",
        venue="Vet Radiol Ultrasound 58(4):422-432",
    ),
    "mai_2022": Citation(
        key="mai_2022",
        authors_year="Mai et al. 2022",
        what="25 HS vs 26 meningiomas; HS had more extensive edema and combined "
             "perilesional+distant meningeal enhancement (pachy- and leptomeninges).",
        pmid="34881469",
        venue="Vet Radiol Ultrasound 63(2):176-184",
    ),
    "pulmonary_2015": Citation(
        key="pulmonary_2015",
        authors_year="Sakai et al. 2015",
        what="Localized pulmonary HS case series in the breed (n=19); purely "
             "histopathological (location, IHC markers, survival), no genetics; "
             "regional nodal involvement in many, 133-day median survival. "
             "(Title paraphrased: it names the breed.)",
        pmid="26155931",
    ),
    "takada_2019": Citation(
        key="takada_2019",
        authors_year="Takada et al. 2019",
        what="Somatic PTPN11/KRAS hotspot frequencies in canine HS "
             "(Bernese Mountain Dog and golden retriever cohorts).",
        pmid="31277422",
        pmc="PMC6678586",
        venue="Genes 10(7):505",
    ),
    "cobimetinib_2024": Citation(
        key="cobimetinib_2024",
        authors_year="Genes 2024",
        what="Cobimetinib in vitro potency on canine HS cell lines "
             "(IC50 74-372 nM vs achievable canine Cmax ~1640 nM).",
        pmid="39202410",
    ),
    "ptpn11_shp2_cohort": Citation(
        key="ptpn11_shp2_cohort",
        authors_year="(large canine HS/hemophagocytic-HS cohort)",
        what="Extensive PTPN11/SHP2 and KRAS mutations across canine HS; the "
             "source of the refined PTPN11 ~56% figure. Contains exactly one dog "
             "of the breed, folded into an undifferentiated 'other breeds' bucket, "
             "with no anatomic-site breakdown.",
        pmc="PMC11353564",
    ),
    "wes_2023": Citation(
        key="wes_2023",
        authors_year="Whole-exome + transcriptome study 2023",
        what="Unbiased WES/RNA of canine HS independently found ERK (MAPK) and "
             "Akt (PI3K) pathway activation as recurrent themes.",
        venue="Scientific Reports 2023 (s41598-023-35813-1)",
    ),
    "cytogenetics": Citation(
        key="cytogenetics",
        authors_year="Molecular cytogenetic study",
        what="Older canine-HS cytogenetics: deletions in RB1 and PTEN in some "
             "cases, alongside CDKN2A deletions.",
        pmc="PMC3121728",
    ),
    "macrophage_ontogeny": Citation(
        key="macrophage_ontogeny",
        authors_year="tissue-resident macrophage ontogeny review",
        what="Alveolar macrophages and microglia are seeded prenatally from "
             "yolk-sac progenitors, self-renew in place, and are largely "
             "bone-marrow-independent in adults.",
        pmid="25470051",
    ),
    "mtap_cdkn2a_locus": Citation(
        key="mtap_cdkn2a_locus",
        authors_year="BMD HS susceptibility GWAS",
        what="Bernese Mountain Dog HS susceptibility locus spanning MTAP-CDKN2A.",
        pmid="22623710",
    ),
    "shanmugam_2019": Citation(
        key="shanmugam_2019",
        authors_year="Shanmugam et al. 2019",
        what="Human HS MAPK-pathway mutation spectrum (~57%).",
        venue="Mod Pathol",
    ),
}


# ---------------------------------------------------------------------------
# 1. Epidemiological / breed-predisposition uniqueness
# ---------------------------------------------------------------------------

EPIDEMIOLOGICAL_PREDISPOSITION = (
    Fact(
        "The breed accounts for ~50% of ALL primary intracranial histiocytic "
        "sarcoma (PIHS) cases in a large single-institution series (10 of 20 "
        "PIHS cases), despite being only 4.6% of the hospital population: "
        "422 of the breed examined, 16 with any primary intracranial tumor, "
        "10 specifically PIHS.",
        EvidenceStatus.VERIFIED,
        ("kishimoto_2020",),
        note="Read directly from the paper's Table 5.",
    ),
    Fact(
        "Odds ratio 21.45 (95% CI 8.9-51.8, p<0.001) for the breed to develop "
        "PIHS -- by far the strongest breed association of any tumor type in that "
        "study.",
        EvidenceStatus.VERIFIED,
        ("kishimoto_2020",),
    ),
    Fact(
        "That degree of concentration (one breed, one cell lineage, one anatomic "
        "site) is the same order of magnitude as the Bernese Mountain Dog's known "
        "germline HS locus (present in ~96% of affected BMDs) -- read by the "
        "conversation's geneticist lens as the signature of a single, currently "
        "unidentified, high-frequency GERMLINE variant, not sampling noise.",
        EvidenceStatus.HYPOTHESIS,
        ("kishimoto_2020", "mtap_cdkn2a_locus"),
    ),
    Fact(
        "The breed is repeatedly overrepresented across independent CNS-HS "
        "cohorts: 47% of 15 subdural HS dogs (Ide 2011); 11 of 23 primary "
        "intracranial HS (~48%, Thongtharb 2016); overrepresented alongside "
        "retrievers in 19 CNS HS dogs (Mariani 2015).",
        EvidenceStatus.VERIFIED,
        ("ide_2011", "thongtharb_2016", "mariani_2015"),
    ),
    Fact(
        "The breed also has a second, independently described site-restricted "
        "presentation -- a localized PULMONARY HS case series (n=19) -- giving "
        "two separate examples of this breed producing a site-restricted rather "
        "than diffusely disseminated form of HS.",
        EvidenceStatus.VERIFIED,
        ("pulmonary_2015",),
    ),
)


# ---------------------------------------------------------------------------
# 2. Anatomical / clinical uniqueness (vs textbook disseminated/visceral HS)
# ---------------------------------------------------------------------------

ANATOMICAL_CLINICAL_UNIQUENESS = (
    Fact(
        "The breed's signature entity is PRIMARY INTRACRANIAL HS (PIHS) -- a "
        "distinct entity from the textbook disseminated/systemic (splenic, "
        "hepatic, pulmonary, nodal, marrow) HS that dominates the disease in "
        "most breeds.",
        EvidenceStatus.VERIFIED,
        ("kishimoto_2020", "thongtharb_2016"),
    ),
    Fact(
        "Where PIHS location is known, it occurs essentially only in the CEREBRUM "
        "(16/16 known-location cases, 100%), temporal-lobe-predominant "
        "(temporal 25%, frontal 18.8%, parietal 12.5%, occipital 12.5%, diffuse "
        "31.3%), with ZERO cerebellar or brainstem cases in that series.",
        EvidenceStatus.VERIFIED,
        ("kishimoto_2020",),
        note="Corrects an earlier 'cerebellum' guess; the real signal is "
             "cerebrum-only, temporal/frontal-predominant.",
    ),
    Fact(
        "The disease is predominantly CNS-confined at diagnosis rather than "
        "multi-organ: 15 of 19 dogs apparently confined to the CNS, only 4 of 19 "
        "part of a disseminated multi-organ process (Mariani 2015).",
        EvidenceStatus.VERIFIED,
        ("mariani_2015",),
    ),
    Fact(
        "Despite the anatomic restriction, the intracranial tumor is locally "
        "INVASIVE, not an encapsulated peelable mass: 23/23 cases 'poorly "
        "demarcated and invading brain parenchyma' (Thongtharb 2016); masses "
        "'unencapsulated, with frequent invasion of adjacent brain/spinal cord "
        "parenchyma' (Mariani 2015).",
        EvidenceStatus.VERIFIED,
        ("thongtharb_2016", "mariani_2015"),
    ),
    Fact(
        "Extra-axial masses predominate on imaging, but leptomeningeal/pial "
        "involvement is the distinguishing feature vs meningioma: all intracranial "
        "HS show leptomeningeal enhancement and/or invasion into the sulci "
        "(Wada 2017); HS shows more extensive edema and combined "
        "perilesional+distant enhancement of both pachy- and leptomeninges "
        "(Mai 2022).",
        EvidenceStatus.VERIFIED,
        ("wada_2017", "mai_2022"),
    ),
    Fact(
        "Meningeal enhancement is present in ALL dogs, often profound and remote "
        "from the primary mass; there is no defined intracranial subdural space, "
        "so both meninges and parenchyma are consistently involved.",
        EvidenceStatus.VERIFIED,
        ("mariani_2015", "toyoda_2020"),
    ),
    Fact(
        "Leptomeningeal / subarachnoid spread is characteristic: 'dissemination "
        "of HS through the subarachnoid space occurs more commonly than with most "
        "other neoplasms'. CSF pleocytosis in all sampled dogs (mean 1509 "
        "cells/uL, median 254.5, range 10-8000; reference <5); CSF neoplastic "
        "cells identifiable in 52% of cases (9/18 primary CNS HS, 4/7 "
        "disseminated CNS HS).",
        EvidenceStatus.VERIFIED,
        ("mariani_2015", "toyoda_2020"),
        note="The 4/7 figure is CSF cytology in disseminated CNS HS, not a "
             "mutation frequency.",
    ),
    Fact(
        "Clinically aggressive with short survival: median survival 3 days in one "
        "series (dominated by euthanasia at presentation); definitive-therapy MST "
        "44 days (95% CI 17-97) vs palliative MST 5 days (95% CI 3-22).",
        EvidenceStatus.VERIFIED,
        ("mariani_2015", "toyoda_2020"),
    ),
    Fact(
        "The second (pulmonary) site-restricted form behaves differently from the "
        "CNS form: regional lymph-node involvement in many cases and a shorter "
        "median survival (133 days), i.e. it spreads regionally (primary + nodal) "
        "where the CNS cohort looked near-non-disseminating.",
        EvidenceStatus.VERIFIED,
        ("pulmonary_2015",),
    ),
    Fact(
        "The overall clinical picture is unusually 'clean' for a cancer: one "
        "breed, one cell type, almost always the same anatomic site, low tendency "
        "to spread to distant organs -- implying fewer escape routes than a "
        "typical genomically chaotic tumor.",
        EvidenceStatus.MINORITY,
        ("kishimoto_2020", "mariani_2015"),
        note="Flagged in-conversation as resting largely on small case series -- "
             "real observations, not guaranteed properties of the disease.",
    ),
)


# ---------------------------------------------------------------------------
# 3. Cell-of-origin biology
# ---------------------------------------------------------------------------

CELL_OF_ORIGIN = (
    Fact(
        "The tumor cells are Iba-1 positive -- a macrophage/microglial lineage "
        "marker, not a Langerhans-cell marker.",
        EvidenceStatus.VERIFIED,
        ("pulmonary_2015",),
        note="Canine HS broadly is classed as interstitial-dendritic-cell "
             "derived; the Iba-1 positivity anchors the tissue-resident "
             "macrophage refinement below.",
    ),
    Fact(
        "Cell-of-origin hypothesis: the breed's HS is a neoplasm of a "
        "NON-CIRCULATING, TISSUE-RESIDENT MACROPHAGE compartment. Lung and brain "
        "are precisely the two tissues whose macrophage pools (alveolar "
        "macrophages, microglia) are seeded prenatally from yolk-sac "
        "progenitors, self-renew locally, and are largely bone-marrow-independent "
        "in adults -- which would explain why the disease STAYS LOCALIZED as a "
        "property of its cell of origin, not because it is merely caught early.",
        EvidenceStatus.HYPOTHESIS,
        ("macrophage_ontogeny", "pulmonary_2015"),
        note="Parallels human LCH cell-of-origin logic: a mutation in a stem "
             "cell gives multisystem disease; the same mutation in a "
             "tissue-restricted precursor gives localized disease.",
    ),
    Fact(
        "This lineage depends on FLT3 -> RAS/MAPK signaling for normal survival, "
        "so a MAPK-hijacking mutation is closer to a natural failure mode for "
        "this specific cell type than a random coincidence.",
        EvidenceStatus.HYPOTHESIS,
        (),
    ),
    Fact(
        "The lineage logic nominates CSF1R (the master survival receptor for "
        "alveolar macrophages and microglia) as a candidate never sequenced in "
        "any canine HS study. As a therapeutic target it was DEMOTED, however: "
        "CSF1R sits upstream (CSF1R -> SHP2/PTPN11 -> RAS -> RAF -> MEK -> ERK), "
        "so it cannot cover downstream activating resistance lesions; it was also "
        "the least structurally assured candidate (85.3% dog-human identity; "
        "structural coherence 0.21).",
        EvidenceStatus.HYPOTHESIS,
        (),
        note="Pexidartinib (CSF1R inhibitor, BBB-penetrant; ~20 nM IC50) has a "
             "real human precedent in CSF1R-mutated Erdheim-Chester disease, but "
             "was designed against human CSF1R.",
    ),
)


# ---------------------------------------------------------------------------
# 4. Genomic uniqueness
#    NOTE: the breed's own tumors have never been sequenced. Every somatic
#    frequency here is a base-rate PRIOR extrapolated from other breeds/species.
# ---------------------------------------------------------------------------

GENOMIC_UNIQUENESS = (
    Fact(
        "Load-bearing gap: ZERO tumors of the breed, at either signature site "
        "(intracranial or pulmonary), have ever been sequenced for PTPN11/KRAS or "
        "anything else. Whether the breed's HS is even MAPK-driven is unconfirmed. "
        "The breed's entity was defined by pathology (location, IHC markers, "
        "survival), never by genetics.",
        EvidenceStatus.UNCONFIRMED,
        ("pulmonary_2015", "ptpn11_shp2_cohort"),
    ),
    Fact(
        "Base-rate prior from canine HS broadly (other breeds): the somatic "
        "driver landscape is MAPK-dominated -- PTPN11/SHP2 ~56% (cited range "
        "~56-57%) plus KRAS ~3% (cited range ~3-7%), i.e. a MAPK-driven majority "
        "of ~59%.",
        EvidenceStatus.EXTRAPOLATED,
        ("ptpn11_shp2_cohort", "takada_2019"),
        note="This ~56% figure superseded an earlier, vaguer 'PTPN11+KRAS "
             "43-64% combined' range.",
    ),
    Fact(
        "Primary-source detail (Bernese Mountain Dog HS, Takada 2019): PTPN11 in "
        "41/96 (43%; E76K ~32%, G503V ~10%), KRAS Q61H in 3/96 (3.1%). In golden "
        "retrievers: PTPN11 3/13 (23%), KRAS 0/13. Combined PTPN11+KRAS = 44/96, "
        "i.e. under half of real dogs with this cancer carry a targetable MAPK "
        "hotspot.",
        EvidenceStatus.EXTRAPOLATED,
        ("takada_2019",),
    ),
    Fact(
        "A substantial fraction of canine HS (36-57%) carries NO MAPK driver at "
        "all -- a MEK inhibitor does nothing for those cases. So even the "
        "MAPK-majority framing leaves a large driver-negative subset.",
        EvidenceStatus.EXTRAPOLATED,
        ("ptpn11_shp2_cohort", "takada_2019"),
    ),
    Fact(
        "Somatic DELETIONS (MTAP, CDKN2A, RB1, PTEN) each occur in a MINORITY of "
        "canine HS tumors -- so no single deletion is the dominant genotype. RB1 "
        "loss specifically would defeat the mechanism of a CDK4/6 inhibitor; its "
        "co-occurrence frequency with the MAPK hotspots is unknown.",
        EvidenceStatus.MINORITY,
        ("cytogenetics", "ptpn11_shp2_cohort"),
    ),
    Fact(
        "Independent, unbiased confirmation of the pathway (not the breed): a 2023 "
        "whole-exome/transcriptome study found recurrent ERK (MAPK) and Akt "
        "(PI3K) pathway activation in canine HS -- two independent methodologies "
        "converging on MAPK raises the prior that the breed's HS is MAPK-driven "
        "too, without proving it.",
        EvidenceStatus.EXTRAPOLATED,
        ("wes_2023",),
    ),
    Fact(
        "The largest PTPN11/SHP2 canine-HS sequencing cohort contains exactly ONE "
        "dog of the breed, folded into an undifferentiated 'other breeds' bucket "
        "with no anatomic-site (pulmonary vs CNS vs splenic) breakdown -- so it "
        "cannot bound the breed's mutations either.",
        EvidenceStatus.UNCONFIRMED,
        ("ptpn11_shp2_cohort",),
    ),
    Fact(
        "Broader-field context: human histiocytoses (Erdheim-Chester disease, "
        "Langerhans cell histiocytosis) have converged on being understood as "
        "fundamentally MAPK-pathway diseases regardless of anatomic site, and "
        "human HS overall runs ~57% MAPK -- consistent with, but not proof of, "
        "the same for the breed's PIHS.",
        EvidenceStatus.EXTRAPOLATED,
        ("shanmugam_2019",),
    ),
    Fact(
        "No published germline OR somatic predisposition locus exists for the "
        "breed's PIHS to build on. By contrast, other breeds have real, "
        "breed-specific GWAS loci (below) -- underscoring that the breed's "
        "extreme concentration is genetically real but molecularly uncharacterized.",
        EvidenceStatus.UNCONFIRMED,
        ("kishimoto_2020",),
    ),
)


# ---------------------------------------------------------------------------
# 4b. Candidate somatic-driver panel (a structured hypothesis, not measurements)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class DriverCandidate:
    gene: str
    tier: DriverTier
    hotspots: dict = field(default_factory=dict)  # wild-type residue by position
    note: str = ""


CANDIDATE_SOMATIC_DRIVERS = (
    DriverCandidate("PTPN11", DriverTier.A, {76: "E", 503: "G"},
                    "SHP2 adaptor; the dominant recurrent canine-HS hotspot."),
    DriverCandidate("KRAS", DriverTier.A, {61: "Q"},
                    "Q61H; minority driver (~3%) but a real canine hotspot."),
    DriverCandidate("BRAF", DriverTier.B, {600: "V"},
                    "Human LCH driver (40-70%); never reported in a dog. Dog "
                    "residue numbering shifts: human V600 -> dog 583."),
    DriverCandidate("MAP2K1", DriverTier.B, {56: "Q", 57: "K", 121: "C"},
                    "Human LCH (~27.5%); never reported in a dog. Dog numbering "
                    "shifts by -41 (56/57/121 -> 97/98/162). Its other real "
                    "lesion is a 6-residue in-frame deletion, not a point mutation."),
    DriverCandidate("NRAS", DriverTier.B, {61: "Q"},
                    "Human LCH driver; no clean canine frequency."),
    DriverCandidate("CSF1R", DriverTier.C, {},
                    "Lineage-motivated (tissue-resident macrophage survival "
                    "receptor); no point-mutation hotspot to target."),
    DriverCandidate("CSF1", DriverTier.C, {},
                    "Lineage-motivated ligand; no point-mutation hotspot."),
    DriverCandidate("CDKN2A", DriverTier.D, {},
                    "Deletion/germline lesion (p16); not a somatic neoantigen."),
    DriverCandidate("MTAP", DriverTier.D, {},
                    "Deletion lesion co-located with CDKN2A; not a neoantigen."),
)


# ---------------------------------------------------------------------------
# 5. Germline-vs-somatic distinction
# ---------------------------------------------------------------------------

GERMLINE_VS_SOMATIC = (
    Fact(
        "The breed clustering is a BETWEEN-DOG (germline predisposition / tumor "
        "INITIATION) signal -- why the tumor forms at all, in this cell type, in "
        "this location. It is a separate axis from the WITHIN-TUMOR (somatic "
        "evolution) question of which acquired mutation drives a given tumor and "
        "whether a resistant subclone already exists.",
        EvidenceStatus.VERIFIED,
        ("kishimoto_2020",),
    ),
    Fact(
        "Two structurally different germline mechanisms could produce the "
        "clustering, and they point opposite ways: (1) a genomic-instability / "
        "checkpoint-loss mechanism (the BMD-type CDKN2A/MTAP analogy) that raises "
        "mutation rate broadly; or (2) a LINEAGE-RESTRICTION mechanism "
        "(FLT3/BATF3/IRF8/ID2-type genes gatekeeping which dendritic/macrophage "
        "subset can transform at all) that does not touch mutation rate.",
        EvidenceStatus.HYPOTHESIS,
        (),
    ),
    Fact(
        "The clustering data favors the LINEAGE-RESTRICTION mechanism: the strict "
        "anatomic homogeneity plus apparent low dissemination are explained by "
        "one mechanism ('only one narrow cell population can become this tumor'), "
        "and there is no epidemiological signal of a broad mutator phenotype "
        "(no elevated second-cancer rate, no implicated DNA-repair gene). So the "
        "breed's germline variant most plausibly gates tumor INITIATION, not "
        "genomic instability.",
        EvidenceStatus.HYPOTHESIS,
        (),
    ),
    Fact(
        "Testable prediction that would discriminate the two: a lineage-gatekeeping "
        "germline mechanism implies the breed's tumors show a restricted "
        "dendritic/macrophage transcriptional signature but NOT elevated tumor "
        "mutational burden vs other HS; a mutator-type mechanism implies the "
        "opposite. Untested -- no tumor of the breed has been sequenced.",
        EvidenceStatus.HYPOTHESIS,
        (),
    ),
    Fact(
        "Germline DELETION lesions (CDKN2A, MTAP) are germline, not somatic "
        "neoantigens -- so they cannot serve as shared-antigen vaccine targets "
        "even if present (Tier D). The candidate SOMATIC neoantigens are the "
        "MAPK-pathway point-mutation hotspots (Tiers A/B).",
        EvidenceStatus.VERIFIED,
        (),
    ),
)


# ---------------------------------------------------------------------------
# 6. Contrast breeds (named on purpose -- they are NOT the subject breed)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ContrastBreed:
    breed: str
    presentation: str
    germline_locus: str
    somatic_notes: str
    citation_keys: tuple = ()


CONTRAST_BREEDS = (
    ContrastBreed(
        breed="Bernese Mountain Dog",
        presentation="Disseminated / systemic (visceral, splenic) HS -- the "
                     "textbook aggressive multi-organ form.",
        germline_locus="CFA11, a susceptibility peak spanning MTAP-CDKN2A; the "
                       "shared risk haplotype is present in ~96% of affected BMDs.",
        somatic_notes="PTPN11 41/96 (43%; E76K ~32%, G503V ~10%), KRAS Q61H "
                      "3/96 (3.1%) (Takada 2019). Note: the MTAP/CDKN2A locus "
                      "does NOT by itself sensitize to CDK4/6 inhibitors.",
        citation_keys=("mtap_cdkn2a_locus", "takada_2019"),
    ),
    ContrastBreed(
        breed="flat-coated retriever",
        presentation="Predisposed to HS via a different germline mechanism than "
                     "the BMD.",
        germline_locus="CFA5 (PIK3R6) and CFA19 -- a PI3K-pathway-flavored link "
                       "rather than the BMD's MTAP/CDKN2A axis.",
        somatic_notes="Breed-specific mechanism differs from BMD; PI3K link "
                      "described in-conversation as more speculative.",
    ),
    ContrastBreed(
        breed="golden retriever",
        presentation="Systemic/disseminated HS; sequenced in the same cohorts as "
                     "the BMD.",
        germline_locus="(not the focus; used as a somatic-frequency comparator)",
        somatic_notes="PTPN11 3/13 (23%), KRAS 0/13 (Takada 2019).",
        citation_keys=("takada_2019",),
    ),
)


# ---------------------------------------------------------------------------
# 7. Corrections / retractions to reflect (final state, not abandoned claims)
# ---------------------------------------------------------------------------

CORRECTIONS_AND_RETRACTIONS = (
    Fact(
        "CORRECTED: the localization is CEREBRUM-only (temporal/frontal "
        "predominant), not cerebellar -- an earlier 'cerebellum' framing was "
        "wrong.",
        EvidenceStatus.RETRACTED,
        ("kishimoto_2020",),
    ),
    Fact(
        "CORRECTED: the breed's PIHS is NOT a peelable, encapsulated, purely "
        "extra-axial mass resectable en bloc; the literature affirmatively shows "
        "parenchymal invasion and leptomeningeal spread. The 'confined "
        "extra-axial compartment' model was walked back.",
        EvidenceStatus.RETRACTED,
        ("thongtharb_2016", "mariani_2015", "wada_2017"),
    ),
    Fact(
        "CORRECTED: the BMD/golden-retriever PTPN11/KRAS frequencies do NOT "
        "'bound' the breed's mutations. Choosing the localized presentation "
        "strengthens only the mechanical/debulking argument, not the "
        "mutation-presence argument -- those are separate axes.",
        EvidenceStatus.RETRACTED,
        ("pulmonary_2015", "ptpn11_shp2_cohort"),
    ),
    Fact(
        "CORRECTED: a CDKN2A/MTAP germline lesion does NOT by itself sensitize a "
        "tumor to CDK4/6 inhibitors -- 'CDKN2A-mutant cancers without co-occurring "
        "D-cyclin lesions rarely show high sensitivity'. Earlier assumption "
        "walked back.",
        EvidenceStatus.RETRACTED,
        ("mtap_cdkn2a_locus",),
    ),
    Fact(
        "CORRECTED: synthetic lethality against an MTAP deletion applies to a "
        "MINORITY of tumors, not 'all cases' -- the MAPK-driven majority "
        "(PTPN11/SHP2 ~56% + KRAS ~3%) is the dominant genotype, and MTAP-deleted "
        "is not the dominant case.",
        EvidenceStatus.RETRACTED,
        ("ptpn11_shp2_cohort",),
    ),
    Fact(
        "CORRECTED: an early citation error attributed the breed's PIHS location "
        "data to Thongtharb et al. 2016; the correct source for the "
        "predisposition/location numbers is Kishimoto et al. 2020 (Thongtharb "
        "2016 remains the correct source for the parenchymal-invasion finding).",
        EvidenceStatus.RETRACTED,
        ("kishimoto_2020", "thongtharb_2016"),
    ),
)


# ---------------------------------------------------------------------------
# 8. Open questions / known gaps
# ---------------------------------------------------------------------------

OPEN_QUESTIONS = (
    ("Does the breed's PIHS (or pulmonary HS) actually carry a PTPN11/KRAS/other "
    "MAPK hotspot? No tumor of the breed at either site has ever been sequenced."),
    ("Is the germline predisposition a lineage-restriction gene or a "
    "genomic-instability gene? The clustering favors lineage-restriction, but no "
    "germline variant has been identified for the breed."),
    ("Is CSF1R (or the tissue-resident-macrophage cell of origin) real for the "
    "breed's HS? Never sequenced; nominated only by lineage reasoning."),
    ("How often does RB1/PTEN loss co-occur with the MAPK hotspots? Unknown, and "
    "it bears on whether CDK4/6- or PI3K-directed strategies could apply."),
    ("Do the favorable 'clean disease' features (homogeneity, low distant spread) "
    "hold beyond the small case series they were observed in?"),
)


# ---------------------------------------------------------------------------
# Headline
# ---------------------------------------------------------------------------

DISTINCTIVENESS_IN_ONE_LINE = (
    "This breed converts histiocytic sarcoma -- normally a disseminated, visceral, "
    "aggressive multi-organ cancer -- into a strikingly site-restricted disease "
    "(cerebrum-only primary intracranial HS, plus a separate localized pulmonary "
    "form), concentrated in this one breed to an extreme degree (OR ~21.5) that "
    "looks like a single high-frequency germline predisposition, most plausibly a "
    "lineage-restriction (tissue-resident macrophage) mechanism rather than a "
    "mutator phenotype -- while its somatic driver genetics remain entirely "
    "unmeasured in the breed and are only inferred from the MAPK-dominated "
    "(PTPN11/SHP2 ~56%, KRAS ~3%) landscape of HS in other breeds and species."
)


# ---------------------------------------------------------------------------
# Convenience accessors
# ---------------------------------------------------------------------------

_FACT_GROUPS = {
    "epidemiological_predisposition": EPIDEMIOLOGICAL_PREDISPOSITION,
    "anatomical_clinical": ANATOMICAL_CLINICAL_UNIQUENESS,
    "cell_of_origin": CELL_OF_ORIGIN,
    "genomic": GENOMIC_UNIQUENESS,
    "germline_vs_somatic": GERMLINE_VS_SOMATIC,
    "corrections_and_retractions": CORRECTIONS_AND_RETRACTIONS,
}


def all_facts():
    """Return every Fact across all groups as a flat tuple."""
    out = []
    for group in _FACT_GROUPS.values():
        out.extend(group)
    return tuple(out)


def facts_by_status(status):
    """Return all Facts (across groups) matching a given EvidenceStatus."""
    if not isinstance(status, EvidenceStatus):
        raise TypeError("status must be an EvidenceStatus")
    return tuple(f for f in all_facts() if f.status is status)


def summary():
    """Return a short human-readable text summary of the module's contents."""
    lines = [
        "Distinctive features of one (unnamed) breed's histiocytic sarcoma",
        "=" * 64,
        DISTINCTIVENESS_IN_ONE_LINE,
        "",
    ]
    for name, group in _FACT_GROUPS.items():
        lines.append(f"[{name}] ({len(group)} facts)")
        for f in group:
            lines.append(f"  - ({f.status.value}) {f.statement}")
        lines.append("")
    lines.append("Open questions / known gaps:")
    for q in OPEN_QUESTIONS:
        lines.append(f"  - {q}")
    lines.append("")
    lines.append(PROVENANCE)
    return "\n".join(lines)


if __name__ == "__main__":
    print(summary())
