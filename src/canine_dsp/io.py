from pathlib import Path
import gzip

import numpy as np


def _open_text(path: Path):
    return gzip.open(path, "rt") if path.suffix == ".gz" else path.open()


def read_first_fasta(path: str | Path) -> tuple[str, str]:
    """Read the first FASTA record, normalizing sequence to uppercase."""
    path = Path(path)
    name, chunks = None, []
    with _open_text(path) as handle:
        for raw in handle:
            line = raw.strip()
            if line.startswith(">"):
                if name is not None:
                    break
                name = line[1:].split()[0]
            elif name is not None:
                chunks.append(line)
    if name is None or not chunks:
        raise ValueError(f"No FASTA record found in {path}")
    sequence = "".join(chunks).upper()
    invalid = set(sequence) - set("ACGTN")
    if invalid:
        raise ValueError(f"Unsupported FASTA symbols: {sorted(invalid)}")
    return name, sequence


def read_vcf_positions(path: str | Path, contig: str | None = None) -> np.ndarray:
    """Read 1-based POS values from a plain or gzipped VCF (no genotype parsing)."""
    positions = []
    with _open_text(Path(path)) as handle:
        for line in handle:
            if line.startswith("#"):
                continue
            fields = line.split("\t", 3)
            if len(fields) >= 2 and (contig is None or fields[0] == contig):
                positions.append(int(fields[1]))
    return np.asarray(positions, dtype=np.int64)

