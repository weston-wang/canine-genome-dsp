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

The small GSE76127 comparative osteosarcoma cohort can be fetched reproducibly with:

```bash
python scripts/fetch_public_data.py gse76127
```

That collection includes the 33-dog GEO series matrix, GEO SOFT metadata, and the open Europe PMC
supplementary archive containing the published disease-free intervals. The preparation code joins
samples by the public dog identifier and never treats probes, technical files, or repeated records
as additional patients. The supplement does not expose an event/censor indicator, chemotherapy is
heterogeneous, and the GEO matrix was cohort-wide preprocessed upstream; the bundled regression is
therefore a crude fold-local prognostic sensitivity analysis, not a survival or HSMM validation.

`clinical/` contains small, hand-curated aggregate endpoint tables whose rows link directly to
primary sources. Blank numerators, denominators, or confidence limits mean the cited public report
did not provide them; they must not be imputed. These tables support arm-level calibration and
benchmarking only. They are not individual participant data and must never be expanded into
pseudo-patients.
