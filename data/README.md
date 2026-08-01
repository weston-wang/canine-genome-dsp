# Data provenance

Raw genomic data are intentionally excluded from Git. For every download, record:

- source URL, accession, release date, and download date;
- reference assembly and chromosome naming convention;
- file checksum and upstream license/terms;
- cohort inclusion criteria and consent/access restrictions;
- filters, normalization, and liftover operations.

Never mix coordinate systems silently. In particular, VCF positions are 1-based while internal
NumPy indices are 0-based.

