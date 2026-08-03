"""Canine MHC class I (DLA) peptide-binding prediction via the IEDB Analysis Resource API.

Two tools were asked about: a canine epitope-*prediction* tool, and a DLA allele-*typing* tool.
They are not the same kind of thing, and only the first exists in a form usable here.

Epitope prediction: NetMHCpan's EL 4.1 training set explicitly includes dog (DLA) alongside
mouse (H-2), cattle (BoLA), swine (SLA), equine (Eqca), and several primates -- confirmed live,
not assumed, by querying IEDB's public REST API directly (`method=netmhcpan_el&species=dog`
against https://tools-cluster-interface.iedb.org/tools_api/mhci/), which returns exactly three
allele names: DLA-8803401, DLA-8850101, DLA-8850801 (IEDB's compact nomenclature for
DLA-88*034:01, DLA-88*501:01, DLA-88*508:01). This module is a thin, real client for that live
service -- not a reimplementation of NetMHCpan and not a synthetic stand-in.

DLA allele *typing* (calling a specific dog's actual DLA genotype from its own sequencing reads,
the way OptiType/HLA-HD/arcasHLA do for human HLA) has no equivalent single, widely-adopted
open-source tool: published canine DLA genotyping work (e.g. NGS-based DLA-88 genotyping papers;
PacBio full-length DLA-88/DRB1 typing) describes bespoke amplicon-sequencing-plus-reference-
matching protocols against the curated IPD-MHC Canine database
(https://www.ebi.ac.uk/ipd/mhc/group/DLA/, 173 DLA-I + 297 DLA-II alleles as of the 2026 search
that informed this module), not a single reusable typing program. This project also has no
actual dog's sequencing reads to type in the first place, so a typing step has no real input
here regardless of whether a tool existed. What this module adds instead is the binding-
prediction half only, using the three real, published, functionally characterized DLA-88 alleles
below as population-representative stand-ins for "a dog's DLA-88 genotype" -- not a claim about
any specific dog's actual, unmeasured genotype.
"""

import io
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pandas as pd

MHCI_API_URL = "https://tools-cluster-interface.iedb.org/tools_api/mhci/"
USER_AGENT = "canine-genome-dsp/0.1 research"

# IEDB/NetMHCpan-EL convention: percentile_rank < 0.5 = strong binder, < 2.0 = weak binder,
# otherwise no predicted binding. A real, published convention -- not chosen for this project.
STRONG_BINDER_PERCENTILE = 0.5
WEAK_BINDER_PERCENTILE = 2.0

# The only three DLA-88 (class I) alleles that are both (a) functionally characterized with a
# defined peptide-binding motif in the published literature and (b) present in IEDB's own
# trained allele list for dog (confirmed live, see module docstring) -- not an arbitrary panel.
CHARACTERIZED_DLA_I_ALLELES = {
    "DLA-8803401": {
        "common_name": "DLA-88*034:01",
        "citation": "Nemec et al. 2018, HLA 91(5):331-340 -- the prevalent Boxer MHC class Ia "
                   "allotype DLA-88*034:01 preferentially binds nonamer peptides with a defined "
                   "motif (basic P1, hydrophobic P2, acidic P4, histidine P6, phenylalanine P9)",
    },
    "DLA-8850101": {
        "common_name": "DLA-88*501:01",
        "citation": "Ross et al. 2012, PLOS ONE 7(3):e33473 -- characterization of the canine "
                   "MHC class I DLA-88*50101 peptide-binding motif as a prerequisite for canine "
                   "T-cell immunotherapy",
    },
    "DLA-8850801": {
        "common_name": "DLA-88*508:01",
        "citation": "Characterization of DLA-88*508:01 presenting diverse self- and canine "
                   "distemper virus-origin peptides of varying length with a conserved motif "
                   "(PMC5850932)",
    },
}


def binding_class(percentile_rank: float) -> str:
    """IEDB/NetMHCpan-EL's own strong/weak/none percentile-rank convention."""
    if percentile_rank < STRONG_BINDER_PERCENTILE:
        return "strong_binder"
    if percentile_rank < WEAK_BINDER_PERCENTILE:
        return "weak_binder"
    return "no_predicted_binding"


def parse_mhci_response(text: str) -> pd.DataFrame:
    """Parse the IEDB `tools_api/mhci/` tab-separated response into a DataFrame.

    The API returns plain-text errors (e.g. an invalid allele name) with the same HTTP 200
    status as a real results table, so this checks the response structurally -- the first line
    of a real result starts with `allele`, not on the HTTP status -- and raises rather than
    silently returning an empty/garbage table.
    """
    first_line = text.strip().splitlines()[0] if text.strip() else ""
    if not first_line.startswith("allele"):
        raise ValueError(f"IEDB mhci API did not return a results table: {text.strip()[:200]!r}")
    table = pd.read_csv(io.StringIO(text), sep="\t")
    if "percentile_rank" in table.columns:
        table["binding_class"] = table["percentile_rank"].apply(binding_class)
    return table


def fetch_binding_predictions(sequence: str, alleles: list[str], lengths: list[int],
                              method: str = "netmhcpan_el") -> pd.DataFrame:
    """Query the real IEDB MHC-I binding-prediction API for one protein sequence.

    `alleles` must use IEDB's own compact nomenclature (no `*`/`:`), e.g. `"DLA-8803401"` for
    DLA-88*034:01 -- confirmed live via `list_supported_alleles`, not assumed from a general
    HLA-style naming convention.
    """
    payload = {"method": method, "sequence_text": sequence,
              "allele": ",".join(alleles), "length": ",".join(str(n) for n in lengths)}
    request = Request(MHCI_API_URL, data=urlencode(payload).encode(), headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=120) as response:
        text = response.read().decode()
    return parse_mhci_response(text)


def list_supported_alleles(species: str = "dog", method: str = "netmhcpan_el") -> list[str]:
    """Query IEDB for the allele names it currently supports for a species/method combination."""
    payload = {"method": method, "species": species}
    request = Request(MHCI_API_URL, data=urlencode(payload).encode(), headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=60) as response:
        text = response.read().decode()
    alleles = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(("Available", "*", "Please")) or "://" in stripped:
            continue
        alleles.append(stripped)
    return alleles
