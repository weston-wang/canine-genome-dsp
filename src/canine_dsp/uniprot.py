"""Resolve gene symbols to UniProtKB accessions via the UniProt REST API.

Non-model organisms like dog have automatically annotated (TrEMBL) entries, often with several
isoform/paralog hits per gene query, so accessions are resolved at call time rather than
hardcoded: hand-picked IDs go stale and are easy to get wrong for genes with multiple hits.
"""

import json
from urllib.parse import quote
from urllib.request import Request, urlopen

API_URL = "https://rest.uniprot.org/uniprotkb/search"
USER_AGENT = "canine-genome-dsp/0.1 research"

HUMAN_TAXID = 9606
DOG_TAXID = 9615

_EXISTENCE_RANK = {
    "1: Evidence at protein level": 1,
    "2: Evidence at transcript level": 2,
    "3: Inferred from homology": 3,
    "4: Predicted": 4,
    "5: Uncertain": 5,
}


def fetch_gene_entries(gene_symbol: str, organism_taxid: int) -> list[dict]:
    """Query UniProtKB for all entries with an exact gene-symbol match in one organism."""
    query = f"gene_exact:{gene_symbol} AND organism_id:{organism_taxid}"
    url = (f"{API_URL}?query={quote(query)}&fields=accession,gene_names,protein_existence,"
           f"length,organism_name&format=json&size=25")
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request) as response:
        return json.loads(response.read())["results"]


def _select_best(entries: list[dict]) -> dict:
    """Prefer reviewed (Swiss-Prot) entries, then stronger protein-existence evidence.

    Automatic (TrEMBL) annotation of non-model genomes frequently returns several
    isoform/paralog hits for one gene; this picks the most reliable single entry.
    """
    if not entries:
        raise ValueError("no UniProt entries to select from")

    def rank(entry: dict) -> tuple:
        reviewed = 0 if entry.get("entryType", "").startswith("UniProtKB reviewed") else 1
        existence = _EXISTENCE_RANK.get(entry.get("proteinExistence", ""), 6)
        return (reviewed, existence)

    return min(entries, key=rank)


def resolve_uniprot_accession(gene_symbol: str, organism_taxid: int) -> str:
    """Resolve a gene symbol + NCBI taxonomy ID to the best-evidence UniProtKB accession."""
    entries = fetch_gene_entries(gene_symbol, organism_taxid)
    if not entries:
        raise ValueError(f"No UniProt entry found for {gene_symbol} in taxon {organism_taxid}")
    return _select_best(entries)["primaryAccession"]
