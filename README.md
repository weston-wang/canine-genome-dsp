# Canine Genome DSP

A research starter for treating canine genomic data as discrete signals. It converts DNA into
indicator, GC, and electron-ion interaction potential (EIIP) signals; converts VCF records into
windowed variant-density signals; and applies Welch spectra, multitaper spectra, spectral entropy,
cross-spectral coherence, and continuous wavelets.

This is exploratory signal analysis, not a clinical genetics tool. Spectral peaks are hypotheses,
not evidence of function; population structure, assembly choice, mappability, coverage, and linkage
disequilibrium are major confounders.

## Public data sources

| Resource | Useful data | Notes |
|---|---|---|
| [NCBI Datasets / Genome](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_000002285.5/) | Dog10K Boxer Tasha reference, FASTA/GFF | Stable accession `GCF_000002285.5`; verify assembly compatibility. |
| [NCBI SRA](https://www.ncbi.nlm.nih.gov/sra/) / [ENA](https://www.ebi.ac.uk/ena/browser/home) | Public raw sequence reads | Search by BioProject/species; access can be large. |
| [Ensembl Canis lupus familiaris](https://www.ensembl.org/Canis_lupus_familiaris/Info/Index) | Genome, genes, comparative genomics, variation | Offers browser, REST, BioMart, and downloads. |
| [Dog10K database](https://dog10k.cn/) | SNVs, de novo mutations, expression, genome browsers | Check each release's metadata and terms before redistribution. |
| [Dog Biomedical Variant Database](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7315552/) | Annotated variants from 582 dogs and 8 wolves | Publication links the catalogue and methods. |
| [OMIA](https://omia.org/home/) | Curated inherited traits/disorders and causal variants | Publicly searchable; check reuse terms for bulk extraction. |
| [NHGRI Dog Genome Project](https://research.nhgri.nih.gov/dog_genome/) | Legacy breed, SNP, phenotype, and sequence releases | Valuable historical cohorts; liftover may be required. |

Commercial test-company reference panels are generally not public. Do not upload identifiable
owner/pet data without consent and an appropriate governance plan.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
canine-dsp demo --out results/demo
pytest
```

Analyze a FASTA region (the first record) and, optionally, a VCF on the same assembly:

```bash
canine-dsp analyze --fasta data/raw/region.fa --vcf data/raw/region.vcf \
  --window 1000 --out results/region
```

The command writes `summary.json`, numeric CSV tracks, and PNG plots. Large inputs remain ignored.
For a whole genome, split work by chromosome/contig and compare only like-for-like windows.

## Nonlinear Volterra modeling

Fit a basis-reduced causal spatial Volterra model to a CSV of aligned genomic windows. The example
below models variant counts, uses callable bases as a Poisson exposure, and holds out each chromosome
in turn. Rows belonging to a chromosome must be contiguous and in genomic order.

```bash
canine-dsp volterra-fit --table data/processed/genome_tracks.csv \
  --inputs gc_fraction repeat_fraction gene_density conservation mappability \
  --target variant_count --exposure callable_bases --group chromosome \
  --memory 11 --basis 4 --order 2 --family poisson --alpha 0.01 \
  --out results/volterra
```

Run a complete synthetic example with a known GC-by-repeat interaction:

```bash
canine-dsp volterra-demo --out results/volterra-demo
```

The reduced model filters each input with a low-frequency orthonormal DCT lag basis and builds all
unique quadratic products of the filtered channels. Outputs include held-out chromosome metrics,
predictions, standardized-back-transformed coefficients, reconstructed first- and second-order
kernels, and a kernel plot. The Poisson model uses exposure weighting; the Gaussian option uses an
elastic-net penalty and is appropriate for transformed continuous targets.

Treat the operator as a spatial association model. It does not by itself identify temporal dynamics
or prove that mutation, selection, or another biological mechanism caused a learned interaction.

## Research path

1. Pin an assembly and record accessions/checksums in `data/README.md`.
2. Start with matched regions, then build chromosome-level GC and variant-density tracks.
3. Test peaks against GC-, length-, and mappability-matched null sequences.
4. Use breed-aware train/test splits and permutation tests; never split related animals randomly.
5. Validate candidates against annotations and an independent cohort.

## Layout

`src/canine_dsp/` contains signal encoding, spectral estimators, wavelets, I/O, and the CLI.
`tests/` contains deterministic unit tests. `data/` stores only provenance documentation in Git.
