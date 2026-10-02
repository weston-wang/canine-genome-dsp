"""Human-vs-dog whole-sequence conservation for the drug-target orthologs the therapy
analysis relies on -- computed from real sequences, not asserted.

WHY THIS MODULE EXISTS
----------------------
Three conservation figures carried the "a human-designed drug should transfer to the dog"
argument in the consolidated report: ERK2/MAPK1 "100% identical", PI3Kalpha/PIK3CA "99.81%
with an identical ATP pocket", and P-glycoprotein/ABCB1 "91% conserved" (the one divergence
that matters, because P-gp is the efflux transporter that decides CNS access). An audit found
those numbers were stated in prose but were NOT reproducible from the code: the machinery to
compute them existed (`uniprot.resolve_uniprot_accession` + `alphafold.whole_sequence_identity`,
a global Needleman-Wunsch aligner) but no result was stored, so the figures could not be checked.

This module closes that gap. Every figure in ``CONSERVATION`` was COMPUTED with that machinery
from the UniProtKB sequences named in each record, not transcribed from a paper. ``recompute()``
regenerates a record from live UniProt so the cached numbers can be re-verified at any time.

WHAT THE NUMBERS DO AND DO NOT SUPPORT
--------------------------------------
High ortholog identity supports *target-side* transfer -- that a molecule which fits a human
binding site should fit the dog's, because the site is the same. It says nothing about potency,
kill rate, exposure, or efflux *kinetics* in the dog; those are separate, still-unmeasured
questions handled elsewhere. The load-bearing caveat the report itself draws survives here: the
two kinase targets are essentially identical (so an inhibitor's *fit* transfers), while P-gp --
the transporter that governs whether the inhibitor ever reaches a brain target -- is the least
conserved of the three at 91%, so canine CNS penetration cannot be assumed from human data and
must be measured. See ``pharmacology``/``core.evidence`` for the penetration side.

This is an analysis, not veterinary advice.
"""

from dataclasses import dataclass

from .uniprot import DOG_TAXID, HUMAN_TAXID, resolve_uniprot_accession

UNIPROT_SEQUENCE_API = "https://rest.uniprot.org/uniprotkb/search"
USER_AGENT = "canine-genome-dsp/0.1 research"

# The exact method behind every fraction in CONSERVATION, named so the provenance is inspectable.
ALIGNER = (
    "canine_dsp.alphafold.whole_sequence_identity -- global Needleman-Wunsch, "
    "match/mismatch/gap = 2/-1/-2"
)
# Date the cached records below were computed from live UniProt (see recompute() to refresh).
COMPUTED_ON = "2026-08-22"


@dataclass(frozen=True)
class OrthologConservation:
    """One human-vs-dog ortholog comparison, with enough provenance to re-verify it."""

    gene: str
    protein: str
    human_accession: str
    dog_accession: str
    human_length: int
    dog_length: int
    aligned_positions: int
    identical_positions: int
    # (human_position, human_residue, dog_residue) for each aligned mismatch, when small enough
    # to enumerate usefully (the point-for-point differences that let a pocket claim be checked).
    differing_positions: tuple[tuple[int, str, str], ...] = ()
    note: str = ""
    aligner: str = ALIGNER
    computed_on: str = COMPUTED_ON

    @property
    def identity_fraction(self) -> float:
        return self.identical_positions / self.aligned_positions if self.aligned_positions else 0.0

    @property
    def identity_percent(self) -> float:
        return 100.0 * self.identity_fraction


# Computed 2026-08-22 with ALIGNER from the named UniProtKB accessions (human taxid 9606,
# dog taxid 9615). resolve_uniprot_accession() selected each accession by best evidence.
CONSERVATION: dict[str, OrthologConservation] = {
    "MAPK1": OrthologConservation(
        gene="MAPK1",
        protein="ERK2 (MAP kinase 1) -- the ERK-inhibitor / downstream-MAPK target",
        human_accession="P28482",
        dog_accession="A0A8I3PZP0",
        human_length=360,
        dog_length=360,
        aligned_positions=360,
        identical_positions=360,
        differing_positions=(),
        note="100.0% identical over the full 360-residue protein: zero differences. An ERK "
             "inhibitor's binding site is identical in the dog.",
    ),
    "PIK3CA": OrthologConservation(
        gene="PIK3CA",
        protein="PI3K-alpha catalytic subunit (p110-alpha) -- the PI3K/AKT-inhibitor target",
        human_accession="P42336",
        dog_accession="A0A5F4C2B1",
        human_length=1068,
        dog_length=1068,
        aligned_positions=1068,
        identical_positions=1066,
        # Both differences fall in the helical domain (~517-694); the kinase/ATP-binding domain
        # (~697-1068) is 100% identical, so the "identical ATP pocket" sub-claim holds. K532R is
        # additionally a conservative (basic->basic) substitution.
        differing_positions=((532, "K", "R"), (535, "S", "C")),
        note="99.81% identical (1066/1068). The only two differences (K532R, S535C) are in the "
             "helical domain; the ATP-binding kinase domain (~697-1068) is 100% identical.",
    ),
    "ABCB1": OrthologConservation(
        gene="ABCB1",
        protein="P-glycoprotein (MDR1) -- the efflux transporter that governs CNS drug access",
        human_accession="P08183",
        dog_accession="C0KKU9",
        human_length=1280,
        dog_length=1281,
        aligned_positions=1278,
        identical_positions=1164,
        # 114 aligned differences -- too many to enumerate; the point is that this is a LOW-
        # conservation target and it is the one that decides CNS penetration.
        differing_positions=(),
        note="91.08% identical (1164/1278 aligned). A low-conservation target that gates drug "
             "delivery -- so canine CNS penetration must be measured, not inferred from human data.",
    ),
    # --- the remaining drug targets in the regimen (maintenance + supporting arms) --------------
    "MAP2K1": OrthologConservation(
        gene="MAP2K1",
        protein="MEK1 -- the MEK-inhibitor target (mirdametinib / cobimetinib; MAPK maintenance)",
        human_accession="Q02750",
        dog_accession="A0A8I3RYU6",
        human_length=393,
        dog_length=434,
        aligned_positions=393,
        identical_positions=391,
        differing_positions=(),
        note="99.49% identical (391/393 aligned, 2 differences). A MEK inhibitor designed for the "
             "human target should bind the canine one -- the target-fit half of the MAPK-majority "
             "maintenance arm, whose drug-class response is separately measured in canine HS.",
    ),
    "PRMT5": OrthologConservation(
        gene="PRMT5",
        protein="PRMT5 -- the synthetic-lethal target for MTAP-deleted cells (TNG908/TNG462)",
        human_accession="O14744",
        dog_accession="A0A8I3RQT2",
        human_length=637,
        dog_length=637,
        aligned_positions=637,
        identical_positions=633,
        differing_positions=(),
        note="99.37% identical (633/637 aligned, 4 differences). The MTAP-maintenance target is "
             "near-identical in the dog, so the synthetic-lethal MECHANISM should transfer; the "
             "canine-HS kill rate and CNS penetration remain unmeasured.",
    ),
    "CDK4": OrthologConservation(
        gene="CDK4",
        protein="CDK4 -- a CDK4/6-inhibitor target (abemaciclib; CDKN2A-deleted maintenance)",
        human_accession="P11802",
        dog_accession="A0A8I3NU36",
        human_length=303,
        dog_length=303,
        aligned_positions=303,
        identical_positions=294,
        differing_positions=(),
        note="97.03% identical (294/303 aligned, 9 differences).",
    ),
    "CDK6": OrthologConservation(
        gene="CDK6",
        protein="CDK6 -- a CDK4/6-inhibitor target (abemaciclib; CDKN2A-deleted maintenance)",
        human_accession="Q00534",
        dog_accession="A0A8I3RZY6",
        human_length=326,
        dog_length=326,
        aligned_positions=326,
        identical_positions=320,
        differing_positions=(),
        note="98.16% identical (320/326 aligned, 6 differences).",
    ),
    "CSF1R": OrthologConservation(
        gene="CSF1R",
        protein="CSF1R -- lineage-survival receptor / pexidartinib target",
        human_accession="P07333",
        dog_accession="A0A8I3MXT5",
        human_length=972,
        dog_length=1044,
        aligned_positions=966,
        identical_positions=824,
        differing_positions=(),
        note="85.30% identical (824/966 aligned) -- the lowest-conservation KINASE target here "
             "(matching the repo's independently noted 85.3%). A human-designed CSF1R inhibitor's "
             "transfer to the dog is correspondingly less certain than for MEK/PRMT5/CDK4-6.",
    ),
    "TUBB": OrthologConservation(
        gene="TUBB",
        protein="beta-tubulin -- the microtubule (mitotic-poison) induction agent's target",
        human_accession="P07437",
        dog_accession="A0A8I3MY05",
        human_length=444,
        dog_length=449,
        aligned_positions=444,
        identical_positions=437,
        differing_positions=(),
        note="98.42% identical (437/444 aligned). Backs the target-fit of the LOAD-BEARING "
             "induction agent -- though its per-day kill rate in canine HS is still unmeasured "
             "(that gap is what keeps escapes 1-3 graded ASSUMED, not target fit).",
    ),
    "PDCD1": OrthologConservation(
        gene="PDCD1",
        protein="PD-1 -- the immune-checkpoint target of the anti-PD-1 arm (gilvetmab)",
        human_accession="Q15116",
        dog_accession="A0A090BAM7",
        human_length=288,
        dog_length=288,
        aligned_positions=285,
        identical_positions=193,
        differing_positions=(),
        note="Only 67.72% identical (193/285 aligned) -- the LOWEST-conservation target in the "
             "regimen, and an antibody target rather than a small-molecule pocket. A human "
             "anti-PD-1 antibody would not reliably cross-react with canine PD-1, which is exactly "
             "why the immune arm must use a CANINIZED antibody (gilvetmab), not a human one. Here "
             "conservation actively WARNS against transfer, rather than licensing it.",
    ),
    # Computed 2026-10-02 by recompute("CLPP"). The target of dordaviprone (ONC201), the licensed
    # ClpP agonist brought in to supply the one kill mechanism that does not require the cell to be
    # dividing. The raw figure UNDERSTATES the transfer and the domain partition is the whole point.
    "CLPP": OrthologConservation(
        gene="CLPP",
        protein="ClpP -- mitochondrial ATP-dependent protease, the agonist target of dordaviprone "
                "(ONC201); the non-division-gated kill mechanism",
        human_accession="Q16740",
        dog_accession="A0A8I3N7L4",
        human_length=277,
        dog_length=273,
        aligned_positions=272,
        identical_positions=252,
        differing_positions=((14, "S", "V"), (15, "C", "G"), (17, "Y", "S"), (27, "H", "R"),
                             (30, "A", "P"), (31, "Q", "R"), (33, "P", "T"), (47, "C", "S"),
                             (50, "A", "V"), (53, "T", "A"), (125, "V", "M"), (128, "A", "S"),
                             (207, "N", "G"), (257, "T", "E"), (265, "E", "M"), (267, "A", "V"),
                             (268, "P", "V"), (273, "V", "A"), (275, "A", "T"), (277, "T", "I")),
        note="92.65% identical overall (252/272), AND THE RAW NUMBER IS THE WRONG ONE TO QUOTE. "
             "UniProt Q16740 annotates residues 1-56 as a MITOCHONDRIAL TRANSIT PEPTIDE, cleaved "
             "during import and absent from the mature protein, and 246-277 as DISORDERED. Of the "
             "20 differences, 10 fall in the cleaved transit peptide and 7 in the disordered "
             "C-terminal tail. The mature, ordered, catalytic region 57-245 carries only THREE "
             "(V125M, A128S, N207G) -- 186/189 = 98.41% identical -- and BOTH ANNOTATED ACTIVE-SITE "
             "RESIDUES, the Ser153 nucleophile and His178, ARE IDENTICAL. So the protease dordaviprone "
             "agonises is effectively the same enzyme in the dog. See clpp_domain_partition().",
    ),
    # Computed 2026-10-02 by recompute("DRD2"). Dordaviprone's second mechanism.
    "DRD2": OrthologConservation(
        gene="DRD2",
        protein="DRD2 -- dopamine D2 receptor, the antagonist half of dordaviprone's dual mechanism",
        human_accession="P14416",
        dog_accession="Q9GJU1",
        human_length=443,
        dog_length=443,
        aligned_positions=443,
        identical_positions=427,
        differing_positions=((15, "R", "S"), (26, "D", "E"), (29, "A", "P"), (30, "D", "G"),
                             (31, "R", "K"), (39, "T", "M"), (46, "A", "F"), (47, "V", "I"),
                             (157, "S", "A"), (177, "A", "T"), (226, "K", "E"), (235, "H", "N"),
                             (237, "R", "K"), (319, "P", "A"), (345, "T", "S"), (400, "D", "E")),
        note="96.39% identical (427/443) over equal-length orthologs, with the differences "
             "concentrated in the N-terminus and the loops rather than spread through the "
             "transmembrane bundle. Independently corroborated by practice rather than by sequence "
             "alone: D2 antagonists are given to dogs routinely, so this half of dordaviprone's "
             "mechanism has species precedent as well as a conserved target.",
    ),
}


def clpp_domain_partition() -> dict:
    """Where the human-dog ClpP differences actually fall, computed from the UniProt annotation.

    The overall 92.65% identity is the least informative way to state this transfer, because more
    than half the differences are in a 56-residue peptide that is CUT OFF during mitochondrial
    import. This function partitions them against the annotated boundaries so the claim that
    dordaviprone's target is conserved rests on the catalytic region rather than on the average.

    Boundaries are UniProt Q16740 features: transit peptide 1-56 (mitochondrion), mature chain
    57-277, disordered region 246-277, active sites Ser153 (nucleophile) and His178.
    """
    c = CONSERVATION["CLPP"]
    transit_end, ordered_start, ordered_end = 56, 57, 245
    active_sites = (153, 178)
    pos = [p for p, _, _ in c.differing_positions]
    transit = [p for p in pos if p <= transit_end]
    ordered = [p for p in pos if ordered_start <= p <= ordered_end]
    disordered = [p for p in pos if p > ordered_end]
    n_ordered = ordered_end - ordered_start + 1
    return {
        "overall_identity_percent": round(c.identity_percent, 2),
        "transit_peptide_1_56_cleaved": {"differences": transit, "n": len(transit)},
        "mature_ordered_57_245": {
            "differences": ordered, "n": len(ordered),
            "identity_percent": round(100.0 * (n_ordered - len(ordered)) / n_ordered, 2),
        },
        "disordered_tail_246_277": {"differences": disordered, "n": len(disordered)},
        "active_sites": {"positions": list(active_sites),
                         "any_differ": [p for p in pos if p in active_sites],
                         "both_identical": not any(p in active_sites for p in pos)},
        "reading": "the differences are concentrated in the cleaved transit peptide and the "
                   "disordered tail; the catalytic region is 98.41% identical and both active-site "
                   "residues are conserved, so a ClpP agonist's target is effectively the same "
                   "enzyme in the dog. The overall figure understates the transfer.",
    }


def fetch_uniprot_sequence(accession: str) -> str:
    """Fetch the amino-acid sequence for one UniProtKB accession (live network call)."""
    import json
    from urllib.parse import quote
    from urllib.request import Request, urlopen

    query = f"accession:{accession}"
    url = f"{UNIPROT_SEQUENCE_API}?query={quote(query)}&fields=sequence&format=json&size=1"
    with urlopen(Request(url, headers={"User-Agent": USER_AGENT})) as response:
        results = json.loads(response.read())["results"]
    if not results:
        raise ValueError(f"No UniProt entry for accession {accession}")
    return results[0]["sequence"]["value"]


def recompute(gene: str) -> dict:
    """Regenerate a conservation record from live UniProt, so a cached figure can be re-verified.

    Resolves the human and dog accessions for ``gene``, fetches both sequences, and runs the same
    Needleman-Wunsch aligner named in ALIGNER. Returns the raw identity dict from
    ``whole_sequence_identity`` plus the accessions used. Requires network and the scientific
    stack (numpy, via ``alphafold``), so it is imported lazily.
    """
    from .alphafold import align_residue_numbers, whole_sequence_identity

    human_accession = resolve_uniprot_accession(gene, HUMAN_TAXID)
    dog_accession = resolve_uniprot_accession(gene, DOG_TAXID)
    human_seq = fetch_uniprot_sequence(human_accession)
    dog_seq = fetch_uniprot_sequence(dog_accession)
    identity = whole_sequence_identity(human_seq, dog_seq)
    mapping = align_residue_numbers(human_seq, dog_seq)
    differing = tuple(
        (pos, human_seq[pos - 1], dog_seq[tgt - 1])
        for pos, (tgt, same) in sorted(mapping.items())
        if not same
    )
    return {
        "gene": gene,
        "human_accession": human_accession,
        "dog_accession": dog_accession,
        "identity": identity,
        "differing_positions": differing,
    }


def orthologs_supporting_transfer(threshold: float = 0.90) -> list[str]:
    """Genes whose human-dog identity is at or above ``threshold`` -- i.e. where a human
    binding-site precedent plausibly transfers to the dog on target-fit grounds alone."""
    return [gene for gene, rec in CONSERVATION.items() if rec.identity_fraction >= threshold]
