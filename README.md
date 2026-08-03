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

## Evolutionary vaccine inverse problem

The project also contains a hybrid tumor-evolution and immune-response model. Clone states undergo
density-dependent growth, immune killing, and mutation/phenotypic transition. Multichannel vaccine
histories drive antigen-specific immunity through first- and second-order Volterra kernels. A robust
inverse solver chooses bounded doses at fixed administration times against an ensemble of uncertain
models.

```bash
canine-dsp inverse-demo --scenarios 8 --out results/inverse-demo
```

The demonstration is deliberately labeled synthetic and uncalibrated. It produces the optimized
schedule, immune response, all uncertainty-scenario trajectories, an objective comparison, and a
plot. See `docs/HYBRID_VACCINE_MODEL.md` for assumptions and translational requirements.

### Combination immunotherapy inverse problem

The combination workflow treats vaccine, checkpoint blockade, and radiation as bounded inputs to a
three-output Volterra operator: cytotoxic activity, immune exhaustion, and inflammation. Its
second-order vaccine × checkpoint kernel is exported as a timing-synergy surface. Sensitive and
weakly immune-visible tumor states are propagated through an uncertainty ensemble, and the inverse
solver penalizes terminal burden, escape composition, inflammation-bound violations, and dose.

```bash
canine-dsp immunotherapy-demo --scenarios 12 --out results/immunotherapy-demo
```

Outputs include CSVs, a clinical dashboard, machine-readable summary, and a plain-language
`clinical_interpretation.md`. The bundled parameters are synthetic: normalized doses are not drug
doses, tumor state is not RECIST response, and inflammation is not an adverse-event probability.
The workflow becomes evaluative only after its kernels and clinical mappings are fitted and locked
using longitudinal combination-therapy data, then tested on untouched patients and external cohorts.

## Real RNA data

Fetch and prepare the small public canine tachypacing time course:

```bash
python scripts/fetch_public_data.py gse9794
canine-dsp prepare-gse9794 \
  --matrix data/raw/gse9794/GSE9794_series_matrix.txt.gz \
  --out data/processed/gse9794
```

This collapses 45 technical profiles into 15 biological samples at five measured time points and
exports sample-level expression components plus probe loadings. It is a real-data adapter and a
low-resolution methods dataset, not enough by itself to calibrate a vaccine-control policy.

Prepare the public Dog10K whole-blood aging matrix in the same module-oriented format:

```bash
python scripts/fetch_public_data.py dog10k_aging
canine-dsp prepare-dog10k-aging \
  --expression data/raw/dog10k_aging/dog_expression_cpm.txt \
  --information data/raw/dog10k_aging/dog_information.txt \
  --out data/processed/dog10k-aging
```

`data/sources.csv` registers open canine and human datasets, including Dog10K aging RNA, canine
osteosarcoma PBMC scRNA-seq, human pancreatic mRNA-vaccine scRNA/TCR data, human vaccine plus
pembrolizumab scRNA-seq, and a controlled-access longitudinal melanoma vaccine study.

### Real prime–boost Volterra evaluation

GSE190001 contains dense daily RNA-seq after prime and booster mRNA vaccination. The evaluation uses
curated interferon, inflammation, and plasmablast modules; leave-one-subject-out prediction; linear,
quadratic, and immune-state-aware models; published peak-timing checks; residual analysis; and
sampling-schedule ablation.

```bash
python scripts/fetch_public_data.py gse190001
canine-dsp evaluate-gse190001 \
  --prime data/raw/gse190001/GSE190001_COVAX_raw_count_PRIME.txt.gz \
  --boost data/raw/gse190001/GSE190001_COVAX_raw_count_BOOST.txt.gz \
  --soft data/raw/gse190001/GSE190001_family.soft.gz \
  --out results/gse190001
```

Reusable visual functions export observed-versus-held-out trajectories, model comparison, residual
heatmap, and sampling-ablation plots. Fixed-dose data can validate response prediction and expose
model gaps, but cannot validate an optimized alternative dosing schedule outside observed support.

The expanded benchmark adds nested subject-aware regularization, observed pre-boost latent-state
interactions, separate prime/boost regimes, and hierarchical third-order challengers. Replicate the
comparison on the independent two-dose M72/AS01 study:

```bash
python scripts/fetch_public_data.py gse102459
canine-dsp evaluate-gse102459 \
  --matrix data/raw/gse102459/GSE102459_series_matrix.txt.gz \
  --out results/gse102459
```

A tiny GRU can also learn only the cross-fitted second-order Volterra residual. It is trained with
complete subject holdouts, masked irregular sequences, three random seeds, weight decay, and shared
multi-module outputs. Reports include its parameter count, seed variability, and performance on both
GSE190001 and the external GSE102459 study. The inverse controller continues to use the interpretable
model until a neural residual demonstrates stable external improvement.

## Protein structure signals from AlphaFold

The project also treats a predicted structure's per-residue confidence (pLDDT) as a signal, and
lets curated OMIA/variant tables be joined onto it by UniProt residue number. Fetch a canine
protein model from the [AlphaFold DB](https://alphafold.ebi.ac.uk/) by its UniProt accession:

```bash
canine-dsp alphafold-fetch --uniprot Q9N2A1 --out data/raw/alphafold
```

This writes the mmCIF model plus a manifest recording the source URL, AlphaFold version, byte
count, and SHA-256 checksum, matching the provenance conventions in `data/README.md`.

Run spectral analysis on the pLDDT confidence track, reusing the same Welch/multitaper estimators
as the DNA-signal workflow:

```bash
canine-dsp alphafold-analyze --struct data/raw/alphafold/Q9N2A1.cif --out results/alphafold
```

Optionally map known variants onto the structure with `--variants variants.csv`, where the CSV
has at least a `protein_position` column using the same 1-based UniProt residue numbering as the
structure (e.g. an export from OMIA or a VEP/UniProt coordinate lookup). Each variant is annotated
with its local pLDDT, a flanking-window mean, and AlphaFold's own confidence band (very high/
confident/low/very low).

This tool does not perform genome-to-protein coordinate liftover: mapping a genomic variant onto
a UniProt residue number, on the correct canonical isoform, is the caller's responsibility. pLDDT
is a model-confidence estimate, not a measure of stability, function, or pathogenicity, and each
model is a single static predicted conformation with no ligands, complexes, or dynamics.

Human and dog UniProt accessions are resolved at call time from the UniProt REST API by gene
symbol and NCBI taxonomy ID (`canine_dsp.uniprot`), rather than hardcoded: non-model genomes like
dog are automatically annotated with several isoform/paralog hits per gene, and picking one by
hand is easy to get wrong or leave stale.

## MAPK inhibitor resistance in histiocytic sarcoma

Canine histiocytic sarcoma (HS) is driven by recurrent MAPK-pathway mutations, dominated by two
mutually exclusive PTPN11/SHP2 hotspots (E76K, G503V) and KRAS Q61H, altering the pathway in
roughly 43-64% of cases across published cohorts (Takada et al., "Activating Mutations in PTPN11
and KRAS in Canine Histiocytic Sarcomas," Genes 2019;10(7):505, PMID 31277422; "Canine
Histiocytic and Hemophagocytic Histiocytic Sarcomas Display KRAS and Extensive PTPN11/SHP2
Mutations and Respond In Vitro to MEK Inhibition by Cobimetinib," Genes 2024;15(8):1050, PMID
39202410). Three canine HS cell lines respond in vitro to the MEK1/2 inhibitor cobimetinib at
IC50 74-372 nM, well below the achievable canine plasma concentration (PMID 39202410). Human HS
carries MAPK mutations spread across more genes (BRAF, MAP2K1, KRAS, NRAS, PTPN11, NF1, CBL) in
about 57% of cases (Shanmugam et al., Mod Pathol. 2019;32(6):830-843). A MAP2K1-mutant human HS
case had a complete response to the MEK inhibitor trametinib maintained for more than two years
with no relapse reported (Gounder et al., N Engl J Med. 2018;378(20):1945-1947, PMID 29768143);
independent case reports of KRAS- and BRAF-mutant HS on MEK/BRAF inhibitors describe similarly
long remissions (31 months; 3 years). The drug actually in canine clinical development is
trametinib, not cobimetinib: two Phase II trials are open (University of Florida; Michigan State
University, VCT25005905), following a completed Phase I dose-escalation study that set the
recommended dose at 0.5 mg/m^2/day PO, with dose-limiting grade 3 toxicities (hypertension,
proteinuria, lethargy, elevated ALP) and a steady-state concentration of ~10 ng/mL (~16 nM)
reached in ~70% of dogs after about two weeks (Takada et al. 2024, Vet Comp Oncol). No published
trametinib-specific canine HS cellular potency number was found, so the model below still anchors
to cobimetinib's measured cell-line IC50s -- the only MEK inhibitor with a direct canine HS
cellular potency measurement -- while noting the real trametinib trial context in its
`provenance.clinical_development` field rather than converting between drugs by assumption.

`canine_dsp.mapk_resistance` fills the *resistance* data gap (still entirely unpublished for HS in
either species) with a hypothesis-generating Monte Carlo model, not a fitted or validated one. A
sensitive clone and three synthetic escape clones -- pathway reactivation (secondary upstream
RAS/RAF alteration), RTK-mediated bypass (loss of ERK feedback reactivates parallel signaling),
and on-target site mutation (reduced inhibitor binding, the generic kinase-inhibitor resistance
category) -- compete under density-dependent growth and an Emax drug-kill term. Acquired
resistance is scheduled as a Poisson process over the sensitive clone's cell-days of drug exposure
rather than a constant daily transfer: a fixed nonzero daily seeding rate mathematically
guarantees eventual outgrowth given enough follow-up (a 100x rate cut only delayed it by degrees),
which cannot reproduce a genuinely durable, years-long response; the Poisson formulation lets a
resistant lineage truly never arise in a given trial. Each Monte Carlo trial also perturbs potency
parameters, samples plasma-exposure variability, and stochastically seeds (or omits) a
pre-existing resistant subclone before treatment starts, using the same mechanism weighting as
acquired resistance (PTPN11-dominated for dog, more even for human):

```bash
canine-dsp mapk-resistance-demo --species dog --trials 300 --horizon-days 730 --out results/mapk-dog
canine-dsp mapk-resistance-demo --species human --trials 300 --horizon-days 730 --out results/mapk-human
```

Only the dog preset's sensitive-clone IC50 and reference plasma concentration are anchored to the
published in vitro/PK values above; every growth rate, resistance-clone potency shift, and kill
ceiling is illustrative and clearly marked as such in `summary.json`. The overall acquired/
pre-existing seeding rate was loosely tuned so the dog preset's durable-response probability lands
in the same ballpark as the handful of published case reports above -- explicitly not a fit: those
are three case reports, published specifically because the response was durable, so the true rate
is almost certainly lower than "durable in 3 of 3." The human preset reuses the same
pharmacodynamic shape with no fitted PK/IC50 numbers (none were found in the literature) and a
broader, less concentrated resistance-seeding spectrum reflecting the wider mutational
heterogeneity reported in human HS.

**The single most influential parameter -- whether a resistant subclone already exists at
treatment start (`preexisting_prob`) -- has no HS-specific source at all.** Rather than fix it to
one asserted value and report a point estimate that would mostly reflect that choice, the demo
sweeps it over `[0.05, 0.15, 0.30, 0.50, 0.70]` and reports durable-response probability as a
range (`preexisting_prob_sensitivity.csv`/`summary.json`), swinging from roughly 0.9 down to 0.3
across that range in testing. `summary.json` also carries `lomustine_benchmark`, two published
non-targeted-chemo studies in unselected canine HS (Rassnick et al. 2010, J Vet Intern Med, PMID
21155191: 29% response, 96-day median duration; Skorupski et al. 2007, J Vet Intern Med, PMID
17338159: 46% response, 106-day median survival) -- included as an automatic scale check, not a
like-for-like comparator, since their population and endpoints both differ from this module's.
The third plot panel shows where the durability-vs-`preexisting_prob` curve crosses those
published response rates, since a synthetic result several-fold better than the real-world
chemotherapy benchmark for the same disease is exactly the kind of thing worth checking rather
than reporting at face value.

The `preexisting_prob` value matching `_PREEXISTING_PROB_CENTRAL` (0.3) is used only for the
illustrative trajectory (`trajectory_quantiles.csv`: median and 10-90% burden over time) and
mechanism breakdown (`escape_mechanism_breakdown.csv`: which mechanism dominates at the horizon,
or durable response) plots -- read those as *a* scenario, not *the* answer. Progression is
flagged using a RECIST-style >=20% increase from nadir, but only once burden clears an absolute
detection floor -- without that floor, a regrowth ratio computed against a numerically negligible
nadir can trigger "progression" while the tumor is still undetectable. The model also has no
representation of treatment-limiting toxicity, non-adherence, or death from other causes, all of
which would push real-world durability below anything shown here.

Before assuming a MAPK-inhibitor finding transfers across species, check whether the two
orthologs are even structurally comparable at the relevant residues:

```bash
canine-dsp mapk-structure-compare --gene PTPN11 --hotspots 76 503 --out results/ptpn11-compare
```

This resolves human and dog UniProt accessions, fetches both AlphaFold models, and maps the given
hotspot residue numbers (in human numbering) onto the dog structure by global sequence alignment
-- not by assuming the same index applies to both, which indels can break -- before comparing
local pLDDT and residue identity. For PTPN11 both hotspots land on identical, well-resolved
(pLDDT > 85) residues in both species, consistent with the shared E76K/G503V nomenclature in the
literature above; this is a structural confidence check, not evidence that the two species'
pharmacology will match.

### Primary CNS histiocytic sarcoma

Canine HS can present as a primary, localized CNS disease (PIHS). Kishimoto et al. 2020 (J Vet
Med Sci 82(1):77-83, University of Tokyo, 9,270 dogs screened, 20 PIHS cases) found this is by far
the most breed-concentrated tumor type in their cohort: Pembroke Welsh Corgi accounted for 10 of
the 20 PIHS cases -- 50%, from a breed that was only 4.6% of the hospital population (odds ratio
21.5, 95% CI 8.9-51.8, P<0.001) -- and, in the 16 cases with known location, PIHS occurred
exclusively in the cerebrum (100%; temporal lobe most common at 25.0%, then frontal 18.8%), with
zero cerebellar or brainstem cases. Toyoda et al. 2020 (J Vet Intern Med 34(2):828-837, n=102 CNS
HS across multiple US institutions) corroborates the strong cerebral predilection but does report
a real infratentorial (cerebellar/brainstem) minority -- so cerebellar primary CNS HS is not
fictional, just rare wherever it has been counted, and apparently absent in Kishimoto's cohort
specifically. Toyoda's data also shows primary and disseminated CNS HS are pathophysiologically
distinct (CSF pleocytosis 170 vs. 4 cells/uL), with sharply different breed skew: Corgis and
Shetland Sheepdogs get almost exclusively the primary form, Rottweilers almost exclusively the
disseminated form. Neither paper reports PTPN11/KRAS/BRAF mutation status for any CNS case --
this concentration is anatomic and epidemiologic, not (yet) molecular. So
`canine_dsp.mapk_cli.canine_cns_hs_scenarios`/`mapk_cns_demo` extrapolate from the systemic model
in `dog_preset` rather than a real CNS dataset:

```bash
canine-dsp mapk-cns-demo --breed bmd --out results/mapk-cns-bmd
canine-dsp mapk-cns-demo --breed flat_coated_retriever --out results/mapk-cns-fcr
```

This scales the systemic reference plasma concentration by each drug's real brain-to-plasma
ratio (trametinib ~15%, cobimetinib ~2.7%; both P-gp/BCRP-limited) to get an effective CNS
concentration, then runs the same Monte Carlo escape model against it. In testing this produced a
sharp, mechanistic finding: at trametinib's exposure the model looks nearly as effective
intracranially as systemically (durable response ~0.69 vs. ~0.68 systemic), while at cobimetinib's
much lower exposure the effective concentration falls below most of the measured cellular IC50s
and the tumor barely responds at all (durable response ~0.03, median time to progression ~9
days) -- the same drug class, two different real potency/exposure profiles, two very different
outcomes. Rostrotentorial and infratentorial (cerebellar) locations are modeled identically via
`location_penetration_multiplier` (default 1.0): both sit fully behind the blood-brain barrier,
and while regional BBB heterogeneity is real and documented (cerebellum is one of the regions
recent single-cell profiling calls a differentially specialized compartment), no quantified
cerebrum-vs-cerebellum comparison was found, so asserting a numeric difference would be less
honest than exposing the multiplier for anyone who wants to test a hypothesis about one.

`--breed` also switches the resistance-mechanism-weighting spectrum, motivated by real but
separate GWAS findings that different breeds carry different germline predisposition loci: `bmd`
(chromosome 11, spanning *MTAP*/*CDKN2A*, present in 96% of affected Bernese Mountain Dogs) keeps
`dog_preset`'s PTPN11-dominated weighting; `flat_coated_retriever` (two loci on chromosomes 5 and
19, one implicating the PI3K-pathway gene *PIK3R6*) shifts weight toward the PI3K/AKT-linked
`rtk_bypass` mechanism instead. That specific link from a germline predisposition locus to an
*acquired*-resistance mechanism is this module's own speculative extension -- included because it
is a concrete, testable hypothesis, not because any study has connected them. It's a different
kind of homogeneity claim than the anatomic one: breed argues for a shared germline background,
which is not the same thing as a shared acquired driver mutation, and doesn't by itself make one
CNS location more molecularly uniform than another. There's deliberately no `corgi` option here
despite Corgi being the single most striking breed association in the PIHS literature above:
`bmd`/`flat_coated_retriever` each rest on a published germline GWAS locus this module extends;
no such locus (germline or somatic) has been published for Corgi PIHS, so adding one would be
fabricating a number rather than extending a real one -- exactly the mistake this module is
trying not to make. `summary.json` lists every extrapolation this scenario stacks on top of
`mapk_resistance_demo`'s already-uncalibrated systemic model explicitly,
under `unverified_extrapolations`.

## Research path

1. Pin an assembly and record accessions/checksums in `data/README.md`.
2. Start with matched regions, then build chromosome-level GC and variant-density tracks.
3. Test peaks against GC-, length-, and mappability-matched null sequences.
4. Use breed-aware train/test splits and permutation tests; never split related animals randomly.
5. Validate candidates against annotations and an independent cohort.

## Layout

`src/canine_dsp/` contains signal encoding, spectral estimators, wavelets, I/O, AlphaFold structure
parsing, UniProt accession resolution, the MAPK-inhibitor resistance Monte Carlo model, and the
CLI. `tests/` contains deterministic unit tests. `data/` stores only provenance documentation in
Git.
