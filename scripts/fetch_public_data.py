#!/usr/bin/env python3
"""Fetch small, credential-free source files with checksums and provenance."""

import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen


FILES = {
    "dog10k_aging": {
        "dog_information.txt": "https://file.kiz.ac.cn/dog10k/dog_information.txt",
        "dog_expression_cpm.txt": "https://file.kiz.ac.cn/dog10k/dog_count_both_ortholog_cpm.txt",
    },
    "gse9794": {
        "GSE9794_series_matrix.txt.gz":
            "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE9nnn/GSE9794/matrix/"
            "GSE9794_series_matrix.txt.gz",
    },
}


def fetch(collection: str, root: Path) -> None:
    destination = root / collection
    destination.mkdir(parents=True, exist_ok=True)
    manifest = []
    for name, url in FILES[collection].items():
        target = destination / name
        digest = hashlib.sha256()
        if not target.exists():
            with urlopen(url) as response, target.open("wb") as handle:
                while block := response.read(1024 * 1024):
                    handle.write(block)
        with target.open("rb") as handle:
            while block := handle.read(1024 * 1024):
                digest.update(block)
        manifest.append({"file": name, "url": url, "bytes": target.stat().st_size,
                         "sha256": digest.hexdigest()})
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("collection", choices=FILES)
    parser.add_argument("--root", type=Path, default=Path("data/raw"))
    args = parser.parse_args()
    fetch(args.collection, args.root)

