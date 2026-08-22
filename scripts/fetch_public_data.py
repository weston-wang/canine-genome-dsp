#!/usr/bin/env python3
"""Fetch small, credential-free source files with checksums and provenance."""

import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen


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
    "gse190001": {
        "GSE190001_COVAX_raw_count_PRIME.txt.gz":
            "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE190nnn/GSE190001/suppl/"
            "GSE190001_COVAX_raw_count_PRIME.txt.gz?download=1",
        "GSE190001_COVAX_raw_count_BOOST.txt.gz":
            "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE190nnn/GSE190001/suppl/"
            "GSE190001_COVAX_raw_count_BOOST.txt.gz?download=1",
        "GSE190001_family.soft.gz":
            "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE190nnn/GSE190001/soft/"
            "GSE190001_family.soft.gz?download=1",
    },
    "gse102459": {
        "GSE102459_series_matrix.txt.gz":
            "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE102nnn/GSE102459/matrix/"
            "GSE102459_series_matrix.txt.gz?download=1",
    },
    "gse272993_metadata": {
        # The full processed Seurat object is about 2 GB.  The SOFT record and
        # file inventory are enough to audit cohort/sample provenance without
        # silently downloading that object as part of the small-data fetcher.
        "GSE272993_family.soft.gz":
            "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE272nnn/GSE272993/soft/"
            "GSE272993_family.soft.gz?download=1",
        "filelist.txt":
            "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE272nnn/GSE272993/suppl/"
            "filelist.txt",
    },
    "gse76127": {
        # Thirty-three chemotherapy-naive canine osteosarcoma tumors with
        # amputation/chemotherapy outcomes.  The series matrix is small enough
        # for a reproducible methods benchmark; raw CEL files are intentionally
        # not downloaded by this helper.
        "GSE76127_series_matrix.txt.gz":
            "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE76nnn/GSE76127/matrix/"
            "GSE76127_series_matrix.txt.gz",
        "GSE76127_family.soft.gz":
            "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE76nnn/GSE76127/soft/"
            "GSE76127_family.soft.gz",
        "PMC4759767_SupplementaryFiles.zip":
            "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4759767/"
            "supplementaryFiles",
    },
}


def fetch(collection: str, root: Path) -> None:
    destination = root / collection
    destination.mkdir(parents=True, exist_ok=True)
    manifest = []
    for name, url in FILES[collection].items():
        target = destination / name
        digest = hashlib.sha256()
        if not target.exists() or target.stat().st_size == 0:
            request = Request(url, headers={"User-Agent": "canine-genome-dsp/0.1 research"})
            with urlopen(request) as response, target.open("wb") as handle:
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
