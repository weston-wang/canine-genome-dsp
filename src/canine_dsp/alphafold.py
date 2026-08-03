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
        "plddt": ca["B_iso_or_equiv"].to_numpy(),
        "x": ca["Cartn_x"].to_numpy(), "y": ca["Cartn_y"].to_numpy(), "z": ca["Cartn_z"].to_numpy(),
    })


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
