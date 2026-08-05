"""Fetch and parse AlphaFold DB predicted structures for per-residue confidence signals."""

import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

import numpy as np
import pandas as pd

API_URL = "https://alphafold.ebi.ac.uk/api/prediction/{}"
USER_AGENT = "canine-genome-dsp/0.1 research"
CONFIDENCE_BANDS = [(90, "very_high"), (70, "confident"), (50, "low"), (0, "very_low")]
THREE_TO_ONE = {
    "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C", "GLN": "Q", "GLU": "E",
    "GLY": "G", "HIS": "H", "ILE": "I", "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F",
    "PRO": "P", "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V", "SEC": "U", "PYL": "O",
}


def fetch_prediction_metadata(uniprot_id: str) -> list[dict]:
    """Query the AlphaFold DB REST API for a UniProt accession's prediction entries."""
    request = Request(API_URL.format(uniprot_id), headers={"User-Agent": USER_AGENT})
    with urlopen(request) as response:
        return json.loads(response.read())


def download_structure(uniprot_id: str, out_dir: str | Path) -> Path:
    """Download the primary AlphaFold mmCIF model and record a provenance manifest."""
    entries = fetch_prediction_metadata(uniprot_id)
    if not entries:
        raise ValueError(f"No AlphaFold prediction found for {uniprot_id}")
    entry = entries[0]
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / f"{uniprot_id}.cif"
    request = Request(entry["cifUrl"], headers={"User-Agent": USER_AGENT})
    digest = hashlib.sha256()
    with urlopen(request) as response, target.open("wb") as handle:
        while block := response.read(1024 * 1024):
            handle.write(block)
            digest.update(block)
    manifest = {"uniprot_id": uniprot_id, "cif_url": entry["cifUrl"],
                "model_created_date": entry.get("modelCreatedDate"),
                "alphafold_version": entry.get("latestVersion"),
                "bytes": target.stat().st_size, "sha256": digest.hexdigest()}
    (out_dir / f"{uniprot_id}_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return target


def read_plddt_track(path: str | Path) -> pd.DataFrame:
    """Parse per-residue CA pLDDT and coordinates from an AlphaFold mmCIF file.

    This reads only the `_atom_site` loop by column name, not a general mmCIF parser.
    """
    path = Path(path)
    columns: list[str] | None = None
    rows: list[list[str]] = []
    with path.open() as handle:
        lines = iter(handle)
        for line in lines:
            if line.strip() != "loop_":
                continue
            header = []
            trailing = None
            for header_line in lines:
                if header_line.strip().startswith("_atom_site."):
                    header.append(header_line.strip())
                else:
                    trailing = header_line
                    break
            if not header:
                continue
            columns = [name.split(".", 1)[1] for name in header]
            if trailing and trailing.strip():
                rows.append(trailing.split())
            for data_line in lines:
                stripped = data_line.strip()
                if not stripped or stripped.startswith("_") or stripped in ("#", "loop_"):
                    break
                rows.append(stripped.split())
            break
    if not columns or not rows:
        raise ValueError(f"No _atom_site loop found in {path}")
    table = pd.DataFrame(rows, columns=columns)
    ca = table[table["label_atom_id"] == "CA"].copy()
    if ca.empty:
        raise ValueError(f"No CA atoms found in {path}")
    ca["auth_seq_id"] = ca["auth_seq_id"].astype(int)
    for column in ("Cartn_x", "Cartn_y", "Cartn_z", "B_iso_or_equiv"):
        ca[column] = ca[column].astype(float)
    ca = ca.sort_values("auth_seq_id").drop_duplicates("auth_seq_id")
    return pd.DataFrame({
        "residue_number": ca["auth_seq_id"].to_numpy(),
        "residue_type": [THREE_TO_ONE.get(code, "X") for code in ca["auth_comp_id"]],
        "plddt": ca["B_iso_or_equiv"].to_numpy(),
        "x": ca["Cartn_x"].to_numpy(), "y": ca["Cartn_y"].to_numpy(), "z": ca["Cartn_z"].to_numpy(),
    })


def align_residue_numbers(source_seq: str, target_seq: str) -> dict[int, tuple[int, bool]]:
    """Global (Needleman-Wunsch) alignment mapping 1-based source residue numbers to target.

    Returns {source_position: (target_position, identical)}; unaligned (gapped) source
    positions are absent. Residue numbering is not guaranteed to match between orthologs
    (indels shift it), so this is required before comparing a hotspot position across species
    rather than assuming the same index applies to both structures.
    """
    match, mismatch, gap = 2, -1, -2
    n, m = len(source_seq), len(target_seq)
    score = np.zeros((n + 1, m + 1))
    score[:, 0] = np.arange(n + 1) * gap
    score[0, :] = np.arange(m + 1) * gap
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            diag = score[i - 1, j - 1] + (match if source_seq[i - 1] == target_seq[j - 1] else mismatch)
            score[i, j] = max(diag, score[i - 1, j] + gap, score[i, j - 1] + gap)
    mapping: dict[int, tuple[int, bool]] = {}
    i, j = n, m
    while i > 0 and j > 0:
        diag = score[i - 1, j - 1] + (match if source_seq[i - 1] == target_seq[j - 1] else mismatch)
        if score[i, j] == diag:
            mapping[i] = (j, source_seq[i - 1] == target_seq[j - 1])
            i, j = i - 1, j - 1
        elif score[i, j] == score[i - 1, j] + gap:
            i -= 1
        else:
            j -= 1
    return mapping


def whole_sequence_identity(source_seq: str, target_seq: str) -> dict:
    """Overall ortholog conservation, not a single hotspot: reuses `align_residue_numbers`'s
    alignment but reports identity across the whole protein.

    Useful for questions `align_residue_numbers`/a single-hotspot comparison can't answer --
    e.g. whether a whole-protein antigen (an antibody target, not a point-mutation neoepitope)
    or a receptor a human-designed ligand/toxin binds is conserved enough across species for a
    human precedent to plausibly transfer, as opposed to whether one specific residue matches.
    """
    mapping = align_residue_numbers(source_seq, target_seq)
    identical = sum(1 for _, is_identical in mapping.values() if is_identical)
    aligned = len(mapping)
    return {
        "source_length": len(source_seq), "target_length": len(target_seq),
        "aligned_positions": aligned, "identical_positions": identical,
        "identity_fraction_of_aligned": identical / aligned if aligned else 0.0,
        "identity_fraction_of_source_length": identical / len(source_seq) if source_seq else 0.0,
    }


def extract_mutant_peptide(track: pd.DataFrame, position: int, wt_residue: str, mut_residue: str,
                           flank: int = 12) -> str:
    """Build a mutant peptide window (length `2*flank + 1`) centered on `position`, substituting
    `mut_residue` in for the wild-type residue -- for designing a synthetic long-peptide/mRNA
    vaccine antigen around a specific point mutation.

    Verifies the wild-type residue at `position` actually matches `wt_residue` before
    substituting, rather than trusting the caller's numbering -- a real, structure-derived
    sequence can silently disagree with a hand-transcribed literature position (isoform
    differences, off-by-one errors, stale annotations), and this is the one check that catches
    that class of mistake outright rather than producing a subtly wrong peptide.
    """
    seq = track.set_index("residue_number")["residue_type"]
    observed = seq.get(position)
    if observed != wt_residue:
        raise ValueError(f"expected wild-type residue {wt_residue} at position {position}, "
                         f"found {observed!r} in the supplied structure")
    window = seq.reindex(range(position - flank, position + flank + 1))
    if window.isna().any():
        raise ValueError(f"peptide window around position {position} runs off the end of the "
                         f"resolved structure (need {flank} residues of flank on each side)")
    wt_peptide = "".join(window)
    return wt_peptide[:flank] + mut_residue + wt_peptide[flank + 1:]


def contact_number_burial(track: pd.DataFrame, radius: float = 10.0) -> pd.DataFrame:
    """CA-CA contact-number burial estimate: for each residue, count how many other residues'
    alpha-carbons fall within `radius` angstroms. A densely surrounded residue (high count) is
    packed into the protein core; a sparsely surrounded one (low count) has open space on at
    least one side and is more likely solvent-exposed.

    This is a coarse proxy for true solvent-accessible surface area (SASA), not a replacement for
    it: a real Shrake-Rupley SASA calculation needs every atom's coordinates and van der Waals
    radius, but `read_plddt_track` (this module's only structure parser) reads alpha-carbons
    only -- the AlphaFold mmCIF files it's built for carry full atomic detail, but no side-chain
    atoms are parsed out. Contact number from CA coordinates alone is a real, if coarse, burial
    signal used for exactly this kind of ranking when full atomic detail isn't available, not
    something invented for this module. `radius=10.0` is a standard order-of-magnitude choice for
    CA-based contact counting, not fit to any specific protein -- treat exposure comparisons as
    relative ranks within one structure, not as calibrated absolute solvent-accessibility numbers.
    """
    coords = track[["x", "y", "z"]].to_numpy()
    dist = np.sqrt(((coords[:, None, :] - coords[None, :, :]) ** 2).sum(-1))
    np.fill_diagonal(dist, np.inf)
    result = track.copy()
    result["contact_number"] = (dist <= radius).sum(axis=1)
    return result


def find_exposed_linear_epitopes(track_with_contact: pd.DataFrame, window: int = 9,
                                 top_n: int = 3) -> pd.DataFrame:
    """Slide a `window`-residue frame across the sequence and rank windows by mean contact
    number (ascending -- least-packed first) to surface candidate linear B-cell epitopes: a
    contiguous, solvent-exposed surface loop is a plausible antibody target, unlike an isolated
    exposed residue or a buried stretch no circulating antibody could reach regardless of how
    immunogenic the raw sequence looks. Requires `contact_number_burial`'s output.

    Returns the top `top_n` non-overlapping windows (each starting at least `window` residues
    from the previous one, so results aren't near-duplicates of the same loop), ordered most-
    exposed first. This ranks *within* one structure; it says nothing about immunogenicity,
    antibody titer, or in vivo efficacy -- no structural tool can predict those.
    """
    track_with_contact = track_with_contact.sort_values("residue_number").reset_index(drop=True)
    n = len(track_with_contact)
    if n < window:
        raise ValueError(f"structure has {n} residues, shorter than window={window}")
    means = np.array([track_with_contact["contact_number"].iloc[i:i + window].mean()
                      for i in range(n - window + 1)])
    order = np.argsort(means)
    chosen: list[int] = []
    for start in order:
        if all(abs(start - c) >= window for c in chosen):
            chosen.append(int(start))
        if len(chosen) == top_n:
            break
    rows = []
    for start in chosen:
        segment = track_with_contact.iloc[start:start + window]
        rows.append({
            "start_residue": int(segment["residue_number"].iloc[0]),
            "end_residue": int(segment["residue_number"].iloc[-1]),
            "sequence": "".join(segment["residue_type"]),
            "mean_contact_number": float(segment["contact_number"].mean()),
            "mean_plddt": float(segment["plddt"].mean()),
        })
    return pd.DataFrame(rows)


def confidence_band(plddt: float) -> str:
    """AlphaFold's published pLDDT bands: >=90 very high, >=70 confident, >=50 low, else very low."""
    for threshold, label in CONFIDENCE_BANDS:
        if plddt >= threshold:
            return label
    return "very_low"


def map_variants(track: pd.DataFrame, variants: pd.DataFrame, flank: int = 5) -> pd.DataFrame:
    """Join variant residue positions onto a pLDDT track and summarize local confidence.

    `variants` must carry a `protein_position` column using the same 1-based UniProt residue
    numbering as `track.residue_number` (the caller is responsible for that correspondence;
    this does not perform genome-to-protein coordinate liftover). Positions absent from the
    resolved structure are reported with a null confidence band.
    """
    positions = track.set_index("residue_number")["plddt"]
    rows = []
    for _, variant in variants.iterrows():
        position = int(variant["protein_position"])
        present = position in positions.index
        window = positions.reindex(range(position - flank, position + flank + 1))
        rows.append({**variant.to_dict(),
                     "plddt": positions.get(position, np.nan),
                     "local_mean_plddt": float(window.mean(skipna=True)) if window.notna().any() else np.nan,
                     "confidence_band": confidence_band(positions[position]) if present else None})
    return pd.DataFrame(rows)
