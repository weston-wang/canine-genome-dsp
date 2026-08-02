# Data provenance

Raw genomic data are intentionally excluded from Git. For every download, record:

- source URL, accession, release date, and download date;
- reference assembly and chromosome naming convention;
- file checksum and upstream license/terms;
- cohort inclusion criteria and consent/access restrictions;
- filters, normalization, and liftover operations.

Never mix coordinate systems silently. In particular, VCF positions are 1-based while internal
NumPy indices are 0-based.

`sources.csv` is the project registry for dog and human datasets. `scripts/fetch_public_data.py`
downloads only small, credential-free collections and records URL, byte count, and SHA-256 checksum.
Large GEO single-cell and controlled-access dbGaP studies remain registry entries until explicitly
requested. Raw downloads remain ignored by Git.

`clinical/` contains small, hand-curated aggregate endpoint tables whose rows link directly to
primary sources. Blank numerators, denominators, or confidence limits mean the cited public report
did not provide them; they must not be imputed. These tables support arm-level calibration and
benchmarking only. They are not individual participant data and must never be expanded into
pseudo-patients.
