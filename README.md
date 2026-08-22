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

The stochastic extension adds patient random effects, uncertain kernel gains, correlated immune
process variation, birth/death/escape events, modality-specific observations, bootstrap particle
filtering, and tail-risk-aware inverse control:

```bash
canine-dsp stochastic-immunotherapy-demo \
  --draws 256 --particles 384 --maxiter 24 \
  --out results/stochastic-immunotherapy-demo
```

It reports conditional probabilities of modeled response, escape dominance, and inflammation-bound
crossing; terminal-burden uncertainty and CVaR; filtered state intervals; simulated assay data; and a
six-panel clinical dashboard. See `docs/STOCHASTIC_IMMUNOTHERAPY_MODEL.md` for the statistical
assumptions, identifiability limits, validation sequence, and clinical guardrails.

### Locked treatment-policy comparison

The policy benchmark adds reduced plasma/tumor PK, target engagement, protocol and exposure bounds,
a first-order PK/PD virtual-population optimizer, a fixed-protocol proxy, and a QSP–Volterra
candidate. Locked policies are evaluated on untouched PK, tumor, escape, and interaction shifts with
prespecified benefit, safety, evolutionary-risk, feasibility, and replication gates.

```bash
canine-dsp immunotherapy-policy-benchmark \
  --draws 96 --scenarios 12 --maxiter 18 \
  --out results/immunotherapy-policy-benchmark
```

The output distinguishes `IN_SILICO_ADVANTAGE` from clinical superiority and fails closed when any
gate is missed. The built-in comparator is a research proxy—not a disease-specific standard of care.
See `docs/POLICY_SUPERIORITY_BENCHMARK.md` for the locked estimand, claim limits, and evidence ladder.

For a target-trial-aligned logged longitudinal dataset with externally cross-fitted behavior-policy
and value-model nuisance estimates, run:

```bash
canine-dsp evaluate-logged-policy --table logged_decisions.csv --cross-fitted \
  --out results/logged-policy-evaluation
```

This triangulates importance-weighted and sequential doubly robust estimates and returns
`NOT_EVALUABLE_*` when overlap, effective sample size, weights, cross-fitting, or estimator agreement
is inadequate. Even a passing result is labeled a retrospective causal estimate, not clinical
superiority.

### Disease-specific melanoma benchmark

The first disease-specific target is macroscopic resectable stage III melanoma treated with
neoadjuvant ipilimumab plus nivolumab before week-six surgery. It was selected because two distinct
checkpoint inputs, serial immune sampling, randomized dose/timing variation, an early pathology
endpoint, and a phase-3 care benchmark all exist in the same biological setting.

The model combines Hammerstein antibody exposure/occupancy, bilinear progenitor-exhausted-to-
effector T-cell dynamics, a bounded low-rank second-order Volterra interaction, stochastic tumor
birth/death and immune-escape events, and constrained risk-aware search. It is tested against
published GSE272993 immune-wave directions, leave-one-arm-out OpACIN-neo response/toxicity, and the
NADINA regimen and outcomes.

```bash
python scripts/fetch_public_data.py gse272993_metadata
canine-dsp melanoma-neoadjuvant-benchmark \
  --anchors data/clinical/melanoma_clinical_anchors.csv \
  --draws 192 --candidates 96 \
  --out results/melanoma-neoadjuvant-benchmark
```

Outputs include real-arm held-out predictions, method ablations, directional GSE checks, paired
virtual-population draws, candidate and NADINA schedules, a clinical dashboard, and a plain-language
interpretation. A candidate is always labeled a research hypothesis. Aggregate public data cannot
show that its timing is clinically superior; that requires patient-level calibration followed by a
prospective randomized comparison. See `docs/MELANOMA_DSP_BENCHMARK.md` and
`docs/MELANOMA_DATA.md`.

### Comparative osteosarcoma RNA-vaccine design

The next disease program targets canine appendicular osteosarcoma after surgery, when occult
pulmonary disease may remain. It combines a species-aware explicit-duration hidden semi-Markov
model with bounded low-rank second-order Volterra terms in the state-transition logits. A separate
robust inverse-design layer selects multivalent DLA/HLA cargo under clonality, presentation,
subclone-coverage, normal-proteome safety, escape, and manufacturing constraints.

Fetch the small real GSE76127 canine tumor/DFI cohort and run the complete benchmark:

```bash
python scripts/fetch_public_data.py gse76127
canine-dsp osteosarcoma-rna-design \
  --gse76127-matrix data/raw/gse76127/GSE76127_series_matrix.txt.gz \
  --gse76127-supplements data/raw/gse76127/PMC4759767_SupplementaryFiles.zip \
  --out results/osteosarcoma-rna-design
```

The default candidate-antigen panel is deliberately synthetic and exercises the constraints and
visualizations. A real tumor-derived panel requires both a deidentified upstream candidate-feature
CSV (`--candidates`) and a schema-v1 patient/cohort constraint manifest (`--design-spec`) containing
the actual DLA and clone labels. The benchmark never substitutes its demo labels, and it still does
not construct a manufacturing-ready nucleotide sequence or a patient treatment plan.

Outputs include cargo and schedule rankings, exact fixed-prior state probabilities, schedule
evidence flags, scenario-long escape stress tests with near-equivalence labels, state-conditioned
Volterra memory plots, model ablations, a real held-out-dog static prognostic sensitivity analysis,
separate dog/human clinical comparators, an identifiability audit, an atomically published
checksum/size manifest, a prospective validation protocol, and a plain-language clinical
interpretation. The clinical-superiority gate always fails closed because no completed randomized
osteosarcoma RNA-vaccine dataset currently identifies the policy effect. See
`docs/OSTEOSARCOMA_RNA_DESIGN.md` and
`docs/OSTEOSARCOMA_DATA.md`.

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
pembrolizumab scRNA-seq, longitudinal melanoma checkpoint scRNA/TCR/ADT, and a controlled-access
longitudinal melanoma vaccine study.

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
trametinib, not cobimetinib: a Phase II trial is open (Michigan State University, University of
Florida, University of Wisconsin, Virginia Tech; VCT24005793 in the Veterinary Clinical Trials
Registry -- corrected here from an earlier, unverifiable VCT25005905 after a direct search turned
up no real registry entry under that ID), following a completed Phase I dose-escalation study that
set the
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
the most breed-concentrated tumor type in their cohort: one breed accounted for 10 of
the 20 PIHS cases -- 50%, from a breed that was only 4.6% of the hospital population (odds ratio
21.5, 95% CI 8.9-51.8, P<0.001) -- and, in the 16 cases with known location, PIHS occurred
exclusively in the cerebrum (100%; temporal lobe most common at 25.0%, then frontal 18.8%), with
zero cerebellar or brainstem cases. Toyoda et al. 2020 (J Vet Intern Med 34(2):828-837, n=102 CNS
HS across multiple US institutions) corroborates the strong cerebral predilection but does report
a real infratentorial (cerebellar/brainstem) minority -- so cerebellar primary CNS HS is not
fictional, just rare wherever it has been counted, and apparently absent in Kishimoto's cohort
specifically. Toyoda's data also shows primary and disseminated CNS HS are pathophysiologically
distinct (CSF pleocytosis 170 vs. 4 cells/uL), with sharply different breed skew: this presentations and
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
CNS location more molecularly uniform than another. There's deliberately no `unsequenced_breed` option here
despite this presentation being the single most striking breed association in the PIHS literature above:
`bmd`/`flat_coated_retriever` each rest on a published germline GWAS locus this module extends;
no such locus (germline or somatic) has been published for localized PIHS, so adding one would be
fabricating a number rather than extending a real one -- exactly the mistake this module is
trying not to make. `summary.json` lists every extrapolation this scenario stacks on top of
`mapk_resistance_demo`'s already-uncalibrated systemic model explicitly,
under `unverified_extrapolations`.

### Debulking plus adjuvant therapy for a localized, single-lineage tumor

localized PIHS's anatomic/breed concentration is more than an epidemiological curiosity: it's the
kind of profile (anatomically predictable, likely non-disseminating, arising from one dendritic
cell population) that in other cancers has changed the prognosis ceiling when local therapy is
combined with a targeted drug, rather than relying on either alone. PIHS arises from dendritic
cells resident specifically in the meninges and choroid plexus -- developmentally distinct from
the body-wide interstitial dendritic cells behind disseminated HS. In mice, that specific
CNS-resident population has a documented dependency on FLT3-ligand signaling and the
transcription factors BATF3, IRF8, and ID2 (Anandasabapathy et al. 2011, J Exp Med
208:1695-1705) -- unverified in dogs, and offered here only as a candidate-gene hypothesis for
what a this presentation germline variant might affect, distinct from BMD's generic CDKN2A/MTAP mechanism.
Combining local and systemic therapy is not speculative for canine HS generally: Skorupski et al.
2009 (Vet Comp Oncol) reported 568-day median survival across 16 dogs with localized HS on
aggressive local therapy plus adjuvant CCNU, against 96-106 days for disseminated/unresectable
disease on CCNU alone (that cohort's CNS-specific fraction isn't confirmed, so treat it as
suggestive scale, not a location-matched number) -- and a single CNS-specific case report
(frontal-lobe PIHS, resection plus low-dose CCNU) survived recurrence-free past a year.

```bash
canine-dsp mapk-localized-control-demo --breed bmd --out results/mapk-localized
```

This runs a four-arm factorial comparison -- debulking (a `debulking_fraction=0.97` reduction in
starting tumor burden, modeling surgery/focal radiation) crossed with adjuvant trametinib -- by
substituting a MAPK inhibitor for CCNU as the adjuvant. In testing: `intact_untreated` and
`debulked_untreated` both progress almost immediately (median ~4-5 days) and converge to full
tumor burden by day ~150-200, confirming that debulking alone, without adjuvant drug therapy,
buys essentially no durable benefit in this model -- consistent with why adjuvant chemotherapy is
standard practice for canine HS already. `intact_trametinib` reached ~67% durable response;
`debulked_trametinib` reached ~69% -- barely different -- but median time to progression among
the dogs that do relapse extended from ~165 to ~211 days (roughly +28%), and the escape-mechanism
mix among relapses was nearly identical between the two arms (still `pathway_reactivation`
dominant for the bmd preset in both). That pattern has a specific mechanistic explanation in the
model, not just noise: debulking shrinks a pre-existing resistant subclone proportionally (it
removes resistant and sensitive cells alike), which delays how long it takes that subclone to
regrow to a detectable size, but does not change *whether* one was already present at the time of
surgery. **Debulking's modeled benefit here is buying time, not preventing relapse** -- and
whether real localized PIHS ever reaches a durable cure depends on a question this model cannot
answer: whether a resistant subclone is typically already present by the time these tumors are
diagnosed and resected, which nobody has measured. Every extrapolation this scenario relies on
-- that localized PIHS is MAPK-driven at all, that it doesn't disseminate, the candidate-gene
hypothesis, the debulking fraction, the survival benchmark's location match -- is listed in
`summary.json` under `unverified_extrapolations`, alongside the full multidisciplinary
`reasoning_chain` behind the scenario.

### Adding a second, mechanism-agnostic drug

`mapk_resistance.ResistanceModel` optionally carries a second drug (`ic50_nM_2`/`max_kill_2`)
applied as a single scalar identical across every clone, rather than per-clone values like the
MEK inhibitor -- modeling a CDK4/6 inhibitor acting on the shared cyclin D/CDK4/6 node downstream
of MAPK signaling, which all three escape mechanisms still have to drive through to actually
divide, unlike the MEK inhibitor itself, which each route was specifically built to evade. This
mirrors a real combination strategy in RAS/RAF-mutant human cancers (adaptive MEK-inhibitor
resistance commonly proceeds through cyclin D1 upregulation and CDK4/6 dependence), but no
canine, or even confirmed human, potency/exposure number exists for a CDK4/6 inhibitor in this
disease, so `mapk_cli.combination_control_demo` sweeps its illustrative potency rather than
picking one value -- the same reason `preexisting_prob` is swept rather than fixed.

```bash
canine-dsp mapk-combination-demo --breed bmd --out results/mapk-combo
```

In testing (debulked CNS context, trametinib plus a swept CDK4/6-inhibitor `max_kill_2` against
an illustrative, unmeasured exposure): durable response was 69% at `max_kill_2=0` (trametinib
alone, matching `localized_control_demo`), 72% at 0.02, then jumped to **99.5% at 0.05** and 100%
at 0.08-0.12 -- a sharp threshold, not a gradual improvement, and the stacked-mechanism plot shows
all three escape routes collapsing toward zero at the same potency step rather than being picked
off one at a time. That's the shared-downstream-node hypothesis behaving exactly as advertised
*if* it holds: because every modeled escape route's growth-rate margin over the MEK inhibitor's
residual kill is small (0.02-0.043/day) and similarly sized, a second kill-rate contribution of
comparable magnitude tips all three negative at roughly the same potency, rather than closing
routes off gradually one by one. That sharpness is itself partly a property of these particular
illustrative growth-rate parameters being clustered close together -- if the escape routes had
more widely separated fitness advantages, closing them off would look more gradual, not a cliff.

This is offered as a demonstration of the mechanism's *shape*, not a probability estimate: no
canine PK/safety data for any CDK4/6 inhibitor exists, and the scenario still assumes localized PIHS
is MAPK-driven at all -- the load-bearing, unverified premise beneath every scenario in this
module. The efficacy side is stronger than pure speculation, though: palbociclib has real,
published in vitro growth-inhibitory activity against canine histiocytic disease cell lines
specifically -- localized HS, disseminated HS, systemic histiocytosis, and Langerhans cell
histiocytosis all responded, with significant activity also shown in a disseminated-HS mouse
xenograft model (Hirabayashi et al. 2022, Vet Comp Oncol 20(3):587-601) -- though that study
didn't dose actual dogs, so it speaks to efficacy, not safety. `summary.json` lists every
extrapolation under `unverified_extrapolations` alongside `mechanism_agnostic_rationale`.

**Combination and CDK4/6i monotherapy are not interchangeable at the same potency**, and
`combination_control_demo` runs both side by side (`combination_scenarios(..., trametinib_active=`
`False)` zeroes trametinib's concentration to isolate monotherapy) rather than leaving that as an
untested assumption. In testing, CDK4/6i monotherapy stayed at **0% durable response through
`max_kill_2=0.05`** -- the same potency at which combination already reached 99.7% -- and only
caught up (99.3%) at `max_kill_2=0.08`. The reason is visible directly in the model's own
parameters (`DIVISION_OF_LABOR` in `summary.json`): trametinib's job is suppressing the *bulk*
tumor (the sensitive clone's net growth under trametinib alone is already -0.12/day: 0.06 growth
minus 0.18 kill), while the resistant clones it can't touch have much smaller margins
(0.02-0.043/day) that a modest additional CDK4/6i kill-rate easily tips negative. CDK4/6i
monotherapy has no help on the bulk tumor, so it must beat the sensitive clone's own 0.06/day
growth rate single-handedly before it does anything -- a higher bar than combination needs.
Practically, this means the combination's advantage is dose-sparing the less-characterized drug
(reaching the same endpoint at roughly 60% lower required CDK4/6i potency), not a mechanistic
requirement that both drugs be present -- if a high enough CDK4/6i dose turns out to be
achievable and tolerable on its own, monotherapy is mathematically viable in this model too.

### Does the combination stay under tolerable combined toxicity?

No real combination dose-finding trial has been run in dogs for trametinib plus any CDK4/6
inhibitor, so this can't be answered directly -- but it can be extrapolated on real mechanistic
grounds rather than left as a bare assumption. Trametinib's canine dose-limiting toxicities are
vascular/hepatic (hypertension, proteinuria, elevated ALP). CDK4/6 inhibitors' dose-limiting
toxicity in human use is neutropenia -- an on-target, mechanism-driven effect (CDK4/6 inhibition
halts proliferation of any rapidly dividing cell, including marrow progenitors), not an
idiosyncratic host reaction, so extrapolating this specific toxicity to dogs is reasonable even
without canine-specific confirmation: the same cell-cycle machinery is being blocked regardless
of species. These are different organ systems -- the standard reason combinations are often
feasible near full dose -- but real combination Phase I/Ib trials still typically de-escalate
both agents below their single-agent MTDs when starting out, reflecting patient-level cumulative
burden beyond any one organ system.

```bash
canine-dsp mapk-combination-toxicity-demo --breed bmd --max-kill-2 0.05 --out results/mapk-tox
```

This fixes CDK4/6i potency at the threshold that closed off all escape routes in
`combination_control_demo` (0.05) and sweeps `COMBINED_EXPOSURE_DERATING` (`[1.0, 0.8, 0.6, 0.4]`)
applied to *both* drugs' reference concentrations simultaneously, to see whether the benefit
survives realistic dose reduction rather than silently assuming full, unconstrained dosing holds.
In testing, the benefit degraded gracefully, not as a cliff: durable response was 99.5% at full
illustrative dose, 99.3% at 80%, 96% at 60%, and 83% at just 40% of that dose -- still well above
trametinib monotherapy's ~69-70% even under an aggressive four-fold dose reduction. That's a
genuinely reassuring shape (the combination doesn't need to be pushed to its full illustrative
dose to keep most of its benefit), but it answers "is the benefit robust to dose reduction,"
not "is dosing safe" -- real toxicity still depends on a combination dose-finding trial that
doesn't exist yet for this drug pair. `summary.json` carries `toxicity_extrapolation_rationale`
alongside the same `unverified_extrapolations` discipline as every other scenario in this module.

### How long does "durable response" actually mean?

Everywhere else in this module, "durable response" means only *no relapse detected within the
horizon that specific run used* -- almost always 730 days (2 years). That is not a claim of
permanence, and it matters: at the potency that looked like a near-cure at 2 years (99.5% durable,
full-dose combination), extending simulated follow-up erodes it -- **91.5% at 5 years, 81% at 10
years**.

```bash
canine-dsp mapk-durability-horizon-demo --breed bmd --max-kill-2 0.05 --out results/mapk-durability
```

The reason is identifiable, not just numeric drift: the combination *slows* the
`pathway_reactivation` escape route rather than eliminating it. `clone_growth_margins` (an exact,
deterministic per-clone growth-minus-kill calculation, not a simulated estimate) shows its net
margin at these central parameters is **still +0.004/day, positive, not reversed** -- a clone with
a genuinely positive margin will eventually regrow given enough time from any nonzero foothold,
independent of luck. Given enough years, that shows up as a growing minority of trials crossing the
detection threshold late. The mechanism breakdown confirms it directly: `pathway_reactivation`
accounts for essentially all of the growth in relapses between year 2 and year 10 (0% to 17%),
while the other two escape routes stay flat near zero across the same horizons. So "cure" language
anywhere in this module should be read as "no relapse detected in the tested window," with the
actual multi-year erosion rate reported in `durability_horizon_sensitivity.csv`, not assumed to be
zero. (An earlier draft of this section described the margin as flipping to slightly *negative*;
direct calculation via `clone_growth_margins` -- added later, see "Feasibility of curing one
specific dog" below -- corrects that: it stays slightly positive, which is in fact the more
consistent explanation for why relapse risk keeps growing rather than plateauing.)

### Is there a purely pharmacological path forward, without any immune/vaccine mechanism?

`clone_growth_margins` makes the erosion problem above precisely diagnosable, and precisely
fixable without invoking a vaccine at all: sweeping `max_kill_2` past the 0.05 value used
everywhere above shows exactly where every resistant clone's margin actually flips negative.

```bash
canine-dsp mapk-combination-toxicity-demo --breed bmd --max-kill-2 0.08 --out results/mapk-tox-08
canine-dsp mapk-durability-horizon-demo --breed bmd --max-kill-2 0.08 --out results/mapk-durability-08
```

| `max_kill_2` | pathway_reactivation | rtk_bypass | target_site_mutation |
|---|---|---|---|
| 0.05 (used above) | +0.004/day | -0.010/day | +0.012/day |
| **0.08** | **-0.024/day** | -0.038/day | **-0.016/day** |
| 0.12 | -0.060/day | -0.074/day | -0.052/day |

At `max_kill_2=0.08`, every resistant clone's margin goes negative -- a genuine mechanistic
elimination, not just a low probability of detection within a given follow-up window. Verified two
ways, not just asserted: (1) the reversal survives this module's own `COMBINED_EXPOSURE_DERATING`
sweep at every level tested, down to 40% of full illustrative dose; (2) run through the actual
Monte Carlo, durable response is **100% flat across 1, 2, 5, and 10 years** at `max_kill_2=0.08`
(`durability_horizon_sensitivity.csv`), versus the 100%->99.5%->91.5%->81% erosion at 0.05 -- the
long-horizon problem doesn't just improve, it disappears.

This route doesn't depend on antigen presentation, DLA genotype, or which driver mutation (PTPN11
or KRAS) a given dog carries at all -- it works purely by suppressing the shared downstream node
harder, which is exactly why it matters as a fallback for a KRAS Q61H-driven case where the vaccine
antigen-binding check below came back unsupported. One honest, load-bearing caveat: **this is not
simply "give a higher dose of the same drug."** `drug_kill_rate`'s own Emax shape means kill
asymptotically approaches `max_kill` as concentration rises but can never exceed it -- confirmed
directly: at `max_kill_2=0.05`, even a 1000x-higher concentration than the illustrative dose (50 µM
vs. 500 nM) only reaches kill=0.05, never more. Reaching the 0.08 regime requires a genuinely more
potent CDK4/6 inhibitor (a different molecule, or a favorable resolution of the real uncertainty in
this module's own illustrative potency guess), not a dose-escalation decision about the one already
discussed. It also reopens the toxicity question from a different direction than before: the
earlier toxicity analysis asked whether the *0.05* benefit survives *dose reduction*; a more potent
drug reaching 0.08 has not been checked for tolerability at all, and myelosuppression risk plausibly
scales with how potent the drug actually is, not just how much of it is given.

### Following the combination with a tailored mRNA vaccine

Shared/hotspot-mutation mRNA vaccines are a real, active human-oncology approach, not something
invented for this module: mRNA-5671 (Moderna/Merck) is a Phase 1 lipid-nanoparticle vaccine
targeting four recurrent KRAS mutations (G12D, G13D, G12C, G12V) as monotherapy or with
pembrolizumab, and a KRAS G12V-specific mRNA vaccine combined with pembrolizumab reported clinical
benefit in advanced solid tumors (Cell Research 2024). localized PIHS's own PTPN11/KRAS hotspot
mutations, *if confirmed present*, would be the same kind of small, recurrent, shareable target --
what makes an "off-the-shelf" vaccine plausible at all, rather than a fully personalized one
requiring per-patient sequencing and manufacture. No canine cancer vaccine trial of any kind exists
for this disease; everything below is this module's own extension of that human precedent.

The key mechanistic point motivating this scenario: **none of the three modeled drug-resistance
escape mechanisms requires losing the driver-mutation antigen a vaccine would target.**
`pathway_reactivation` adds a secondary RAS/RAF hit on top of the original mutation, `rtk_bypass`
reactivates parallel signaling around it, and `target_site_mutation` only changes the MEK-inhibitor
binding site -- all three keep expressing the original PTPN11/KRAS hotspot peptide. A vaccine
targeting that hotspot should therefore still recognize cells using any of those three routes,
including the very `pathway_reactivation` clone responsible for the long-horizon erosion above.
Only a genuinely new, separate antigen-loss/immune-evasion event would evade it -- modeled here as
a 5th clone, `immune_escape`, seeded by its own Poisson process from the antigen-positive
population (not the sensitive clone) and restricted to days on/after `VACCINE_START_DAY`, since
antigen loss confers no advantage before immune pressure exists. It inherits
`pathway_reactivation`'s drug susceptibility with an illustrative 15% growth penalty, reflecting
the assumption that an antigen-loss variant most plausibly arises from a lineage that already
survived MAPK-inhibitor selection. Vaccine-induced kill is modeled as time-gated and ramping (not
concentration-driven like the two drugs): zero before `VACCINE_START_DAY` (illustrative, 90 days,
allowing debulking recovery plus an initial drug course), then rising with a saturating time
constant (`VACCINE_RAMP_DAYS`, illustrative, 21 days -- general T-cell priming/expansion kinetics,
not measured for this vaccine).

```bash
canine-dsp mapk-vaccine-followon-demo --breed bmd --cdk46-max-kill 0.05 --horizon-days 3650 --out results/mapk-vaccine
```

Run at the same 10-year horizon that exposed the erosion (400 trials), sweeping
`VACCINE_MAX_KILL_SWEEP` (`[0.0, 0.01, 0.03, 0.05, 0.08]`) on top of the fixed full-potency
combination: durable response rose from **80% (vaccine off) to 98.75% at max_kill=0.01, to 100% at
max_kill>=0.03** across all 400 trials at that potency and above. The mechanism breakdown confirms
*why*: at vaccine_max_kill=0.0, relapses are 17.25% `pathway_reactivation` and 2.75%
`target_site_mutation`; by max_kill=0.01, `pathway_reactivation` relapses are already fully
suppressed (0%), leaving only a residual sliver of `target_site_mutation`; by 0.03 both are zero.
Across every potency tested, out to 10 years, **`immune_escape` never appeared as the dominant
mechanism in any trial** -- consistent with this module's own choice to set
`IMMUNE_ESCAPE_SEEDING_RATE` an order of magnitude below the rarest existing drug-resistance
mechanism, not evidence that antigen loss can't happen; a higher assumed rate would show up here
if tested.

Two caveats specific to this scenario, beyond the general disclaimers every other scenario in this
module already carries:

- **PIHS's own cell-of-origin is dendritic cells** -- the same lineage antigen presentation itself
  depends on. This is worth flagging as an open biological question, not dismissing: it is the
  patient's *normal*, non-malignant dendritic cells that would actually present the vaccine antigen,
  not the tumor cells, which only partially (not fully) allays the concern, since it is not
  established whether malignant transformation of this lineage locally impairs nearby normal
  antigen presentation.
- A human primary CNS HS case report noted PD-L1/PD-L2 expression on tumor cells, consistent with a
  T-cell-exhaustion phenotype that could blunt vaccine-induced killing independent of antigen loss
  -- not modeled explicitly here, and a reason a checkpoint-inhibitor combination (as in the real
  KRAS G12V vaccine + pembrolizumab trial above) might matter for this specific application, not
  just as a generic add-on.

Read the vaccine's near-elimination of the long-horizon gap as a demonstration of the *shape* of
the antigen-persistence argument (a vaccine should suppress an escape route that hasn't shed the
antigen it targets), not as a probability estimate for an actual dog: `vaccine_start_day`,
`vaccine_ramp_days`, `vaccine_max_kill`, and the immune-escape clone's seeding rate and fitness
cost are all illustrative placeholders, and the premise that localized PIHS carries a shareable
PTPN11/KRAS hotspot at all remains unconfirmed in dogs.

### Feasibility of curing one specific dog

Every scenario above reports a population-level probability (a new hypothetical dog's parameters
are redrawn every trial), which doesn't directly answer "can this one dog be cured" -- that
requires separating uncertainty about *which dog this is* (in principle resolvable by testing that
specific dog) from genuinely irreducible chance (whether/when a resistant mutation happens to
strike, which no test on that dog could predict).

```bash
canine-dsp mapk-single-patient-feasibility-demo --breed bmd --cdk46-max-kill 0.05 --out results/mapk-single-patient
```

`run_monte_carlo_fixed_patient` holds one dog's model, drug exposure, and starting tumor state
fixed and repeats only the stochastic mutation-timing draw; `decompose_patient_uncertainty` draws
many such dogs and splits the population variance into between-dog and within-dog components
(a method-of-moments/ANOVA-style variance-components estimate). In testing (60 simulated dogs, 80
repeats each, 5-year horizon): **99.8% of the outcome variance was "which dog you are," not
chance** -- the per-dog histogram was sharply bimodal (52/60 dogs at ~100% durable response, 7/60
at ~0%, almost none in between). Tracing why led to a real refinement of the earlier combination
narrative: `clone_growth_margins` shows the combination *reduces but does not reverse* two of the
three resistant clones' growth advantage at the illustrative central parameters
(`pathway_reactivation`: +0.004/day, `target_site_mutation`: +0.012/day, both still positive; only
`rtk_bypass` flips negative, at -0.010/day). A clone with a genuinely positive margin will
eventually regrow given enough time from *any* nonzero foothold -- so whether a specific dog is
cured or relapses is driven almost entirely by whether it already harbors (or develops) such a
foothold, not by luck once one exists. Directly confirming this: for the same fixed dog, a
detectable pre-existing subclone (10⁻³ of tumor burden) flips durable response from 100% to 0%; a
worst-/best-case bracket at this module's own 5th/95th-percentile exposure and mutation-rate
assumptions likewise collapses to 0%/100%, not a smooth range.

This reframes what would actually matter for one dog in front of a clinician: not "what's the
expected response rate," but "does this dog's tumor already carry a resistant subclone" -- a real,
if not yet clinically applied, diagnostic question (deep/ctDNA sequencing for the known hotspot at
low variant-allele frequency), rather than a question luck can answer. It also sharpens the
vaccine case above: since the two surviving-margin clones both still express the original driver
antigen, the "already harbors a subclone" scenario -- otherwise a deterministic treatment failure
-- is exactly the case a shared-antigen vaccine is built to rescue (confirmed directly: the same
fixed "doomed" dog goes from 0% to 100% durable response with even the mildest vaccine potency
tested). No real diagnostic pipeline for pretreatment subclone detection exists for canine HS; this
quantifies what one *would* be worth if it existed and were accurate, not a claim that it does.

### What the vaccine actually is: antigen design and real canine MHC-I binding prediction

"The vaccine" above was an abstract kill-rate parameter. Concretely, it would be an mRNA-LNP
multi-epitope construct (mirroring the real mRNA-5671 KRAS-multi-mutation design) encoding a
25-residue synthetic long peptide around each candidate driver mutation, so it works regardless of
which one a given dog's tumor carries -- PTPN11 p.E76K (N-SH2 domain), PTPN11 p.G503V (PTP
catalytic domain), and KRAS p.Q61H (switch II region).

```bash
canine-dsp mapk-vaccine-epitope-binding-demo --out results/mapk-epitope
```

`vaccine_antigen_peptides` builds each peptide *fresh* from the real canine AlphaFold/UniProt
sequence (`extract_mutant_peptide`, with a hard wild-type-residue check against numbering
mistakes) rather than a hardcoded string. Cross-species check: all three 25-residue windows are
100% sequence-identical between dog and human, so the canine peptide is exactly what a human
trial would encode, substitution for substitution -- not guaranteed in general, but true here.

Two different tools were asked about. A canine epitope-*prediction* tool -- yes, real. NetMHCpan's
training data explicitly includes dog (DLA) alongside cattle/pig/primate/equine non-human species,
exposed live via IEDB's public REST API; confirmed directly (not assumed) by querying
`method=netmhcpan_el&species=dog`, which returns exactly three allele names: DLA-88\*034:01,
DLA-88\*501:01, DLA-88\*508:01 -- the same three alleles that happen to be the only
functionally-characterized DLA-88 allotypes in the published literature. Checking further turned
up a real *consensus* opportunity, the way real neoantigen-vaccine pipelines like pVACtools trust
an ensemble rather than one algorithm: of IEDB's several MHC-I methods, only `netmhcpan_el`
(trained on mass-spec-eluted ligand data) and `netmhcpan_ba` (trained on quantitative binding-
affinity data) return any canine allele at all (`ann`, `smm`, `smmpmbec`, `pickpocket`,
`consensus`, `netmhccons` all return none) -- two real, differently-trained methods, not thirteen,
but a genuine agreement check rather than one algorithm's unverified opinion.
`fetch_consensus_binding_predictions` queries both and flags disagreement.

A DLA allele *typing* tool (calling one specific dog's actual genotype from its own sequencing
reads, the way OptiType/HLA-HD do for human HLA) -- also turned out to exist, contradicting an
earlier pass over this question: **KPR** (Hess et al. 2023, iScience 26(2), PMID 36798440;
https://github.com/ZhaoS-Lab/KPR) genotypes DLA-I directly from an individual dog's paired-end
RNA-seq reads and was validated on 152 real dogs. It doesn't close the actual gap here, though:
this project has no dog's real RNA-seq reads to feed it, so the missing piece is now "no input
data," not "no tool" -- worth keeping on file for whenever real sequencing exists.

Real result from the live consensus query: on the method used as primary throughout this module
(`netmhcpan_el`), PTPN11 p.E76K and p.G503V each predict as a **strong binder** (percentile rank
0.05 and 0.32) against DLA-88\*034:01. The two methods agree on only 6 of 9 (mutation x allele)
pairs tested; the disagreements matter. Most notably, **KRAS p.Q61H against DLA-88\*034:01** was
first reported as clean "no predicted binding" under `netmhcpan_el` alone (percentile rank 3.0) --
under `netmhcpan_ba` it comes back as a **weak binder** (1.6). That earlier clean negative doesn't
hold up unqualified: it's method-dependent, not a settled result, which is exactly the failure
mode a consensus check exists to catch. KRAS Q61H is still the weakest of the three candidates (the
only one with zero full-agreement binder hits across all three alleles), just not as cleanly
negative as the single-method result first suggested. Predicted affinity is necessary but not
sufficient for actual immunogenicity, no specific dog's real DLA genotype was typed (the three
alleles are literature stand-ins, not any dog's measured genotype), canine MHC class II (the CD4+
axis) has no supporting method in IEDB at all for any DLA allele -- checked directly, not assumed
-- so it is unchecked here rather than approximated with a human-allele substitute, and whether
localized PIHS carries any of these three mutations at all remains unconfirmed.

### Does the approach transfer to localized pulmonary HS?

A real, independently-described localized HS presentation exists distinct from PIHS:
localized pulmonary histiocytic sarcoma (Sakai et al. 2015, J Vet Med Sci 77(12):1667-1670, PMID
26155931; 19 dogs of one breed, median survival 133 days). Two things are concretely
different from the PIHS scenarios above, both checked directly rather than assumed:

1. **Lung tissue has no blood-brain-barrier-type restriction** -- drug reaches it at full
   systemic concentration (Cmax ~1640 nM), not the 15% brain-penetration-discounted value used
   for the CNS scenarios. Verified (`clone_growth_margins`) that this alone does *not* close the
   same two-of-three-clones-still-positive-margin gap found in the CNS scenarios: those clones
   resist trametinib via a capped maximum kill rate, not merely insufficient concentration, so
   removing the brain-penetration penalty mainly speeds up how fast the drug-sensitive bulk
   responds, not whether the resistant routes are actually closed.
2. **Unlike Kishimoto's near-zero-dissemination PIHS cohort, this case series reports regional
   lymph node involvement in many cases.** The single-compartment model used throughout this
   module implicitly assumes debulking (surgery) reaches all disease -- an assumption this
   presentation's own published natural history argues against.

```bash
canine-dsp mapk-pulmonary-two-compartment-demo --cdk46-max-kill 0.05 --out results/mapk-pulmonary
```

`run_monte_carlo_two_compartment` models a resectable primary plus a possible nodal deposit that
surgery can't reach: the nodal compartment, if present, is seeded from the *pre-debulking*
primary's clonal composition (metastasis is a biological event that already happened before the
later surgical decision), left untouched by `debulking_fraction`, and swept across
`NODAL_INVOLVEMENT_PROB_SWEEP` since no precise nodal-involvement rate was published (the paper
says "many cases," not a percentage).

A genuinely interesting, non-obvious finding surfaced by actually running this rather than
assuming a clean story: **at trametinib monotherapy (this demo's default), nodal disease's effect
on overall durable-response probability is small and can sit within ordinary Monte Carlo noise**
-- because at full systemic exposure without a second drug, two of three resistant clones' growth
margins are already strongly positive (not just barely, the way they are at CNS-discounted
exposure), so an existing subclone is close to guaranteed to reach detectable size within a
multi-year horizon regardless of which compartment it started in. The stacked relapse-source panel
still shows the *mechanism* working correctly -- nodal disease's share of relapses rises cleanly
from 0% to 6% of trials as `nodal_involvement_prob` rises from 0 to 0.6 -- it just doesn't move the
*overall* probability much when relapse is already nearly certain either way. Switching to the
CDK4/6i-combination arm (`--cdk46-max-kill 0.05`), where margins sit close to the suppression
threshold instead of far above it, makes the effect clearly visible and robust: durable response
was consistently and meaningfully lower with guaranteed nodal involvement than without it across
multiple random seeds (e.g. 94.4% vs. 88.4% at one tested parameter set) -- **undebulked regional
disease matters most exactly when the rest of the regimen would otherwise be close to working**,
which is also exactly the situation where surgery's real limits are easiest to overlook.

This is offered as a demonstration that reusing a single-compartment model's numbers for a
disease presentation with a different natural history can be actively misleading, not as a
calibrated estimate for a real dog: `NODAL_SEED_FRACTION` and the involvement-probability sweep
are both illustrative placeholders, no lymphadenectomy option is modeled, and -- as with every
other scenario in this module -- whether localized pulmonary HS actually carries the same PTPN11/KRAS
driver spectrum has never been directly confirmed.

### Is the simulation engine's own math actually right?

Every scenario above trusts one core stochastic mechanism: acquired resistance is scheduled as a
Poisson process over a source clone's cumulative cell-days (`poisson_mutation_injections`), not a
constant daily transfer rate, specifically because a Poisson draw can come back exactly zero --
the property that lets a resistant lineage genuinely never arise in a given trial. That claim has
an exact, closed-form answer from real point-process theory (the same mutation-supply framework
used in mathematical-oncology branching-process models): for a fixed source trajectory, the
probability a clone receives zero seeded events should equal `exp(-rate * total_cell_days)`. A
regression test (`test_poisson_injections_zero_event_probability_matches_analytical_poisson_process`)
checks the simulation's empirical zero-event rate against that exact formula across 20,000 repeats
-- it matched within statistical tolerance, confirming the engine correctly implements the theory
it's supposed to implement, rather than assuming it does.

### Is the three-drug combination actually the best option tested?

"Inhibitors plus vaccine" reads like a conclusion, but nothing in this module searches therapy
space for one -- every regimen tested is a scenario someone wrote by hand, and the three-part
combination (trametinib + CDK4/6i + vaccine) had never actually been compared against a *simpler*
two-part alternative until asked directly. The vaccine's kill term in
`run_monte_carlo_with_vaccine` applies to every clone except the immune-escape one -- meaning it
should in principle suppress `pathway_reactivation`, `rtk_bypass`, and `target_site_mutation` on
its own, not just mop up what CDK4/6i already weakened. Testing that directly (1000 trials, 5-year
horizon): **trametinib + vaccine alone, with no CDK4/6i at all, reached 98.2% durable response**,
versus 100% for the full three-part combination -- CDK4/6i's entire marginal contribution on top of
the vaccine was closing the last ~1.8 percentage points, and specifically only the
`target_site_mutation` route. Given CDK4/6 inhibitors carry real added toxicity risk
(myelosuppression) for that small a gain once a vaccine is already present, this is a genuine,
if narrow, case for questioning whether CDK4/6i belongs in the regimen at all -- not something the
earlier "combination is best" framing surfaced, because the two-drug alternative had simply never
been run.

### Searching for real data to de-risk the placeholders

A broad search for published libraries/databases that could replace this module's illustrative
constants with real, clinically-grounded numbers turned up a mix of genuine finds and dead ends,
each checked directly rather than taken on a search summary's word:

- **Used**: the KPR DLA-typing tool above; the corrected VCT24005793 trial ID; and
  `MAPK_INHIBITOR_HUMAN_BENCHMARK` (Schreuer et al. 2016, J Transl Med, PMID 27095081) -- a real
  111-day median time-to-progression from 36 human BRAF-mutant melanoma patients on
  dabrafenib+trametinib, added to `durability_horizon_demo`'s output as a labeled sanity-check
  comparator, the same role the lomustine benchmark already plays. On closer reading this paper is
  weaker than it first sounded, though: it's a ctDNA-monitoring report, not a full efficacy trial
  writeup (no response rate, no PFS-from-treatment-start, no OS, no toxicity data), and its 111-day
  clock starts at ctDNA-monitoring enrollment, not confirmed treatment start -- corrected in the
  benchmark's own `caveat` field once that came up.
- **Checked and not used**: a BRAF/MEK+checkpoint-inhibitor systems-pharmacology model
  turned out to be calibrated against mouse xenograft data, not patients, and models no resistance
  dynamics at all -- using its numbers would have been worse than not having them. A 2026
  Communications Biology paper was paywalled and no number from it could be verified, so nothing
  from it was cited. SIApopr/ESTIpop (real branching-process simulation packages) have no
  drug-kill term and no clinical calibration -- they'd replace this module's already-validated
  simulation plumbing with unvalidated plumbing, not worth the migration.
- **Real trial data that exists but wasn't folded in as a model parameter**: dabrafenib+trametinib's
  actual pivotal-trial efficacy in melanoma is far more complete than the benchmark above --
  COMBI-d/COMBI-v report median PFS 11.0-11.4 months, median OS up to 25.1 months, objective
  response 64-69%, and a 5-year pooled follow-up showing 19% PFS / 34% OS at 5 years overall but
  **71% five-year OS among the 19% of patients who achieved a complete response** -- a real-world
  echo of this module's own high-intraclass-correlation finding that outcome is sharply bimodal
  depending on whether a resistant route gets a foothold, not smoothly distributed. Not used as a
  fitted parameter for the same reason the ctDNA benchmark isn't: mapping a human/melanoma/BRAF
  cohort onto a canine/HS/PTPN11-KRAS model would stack a cross-species extrapolation on top of an
  already-illustrative one.
- **The real canine trial's own status**: the actual trametinib-for-canine-HS trial (VCT24005793)
  is live -- University of Florida's own page shows "Currently Enrolling," and a 2023 Morris
  Animal Foundation announcement confirms dosing had already begun by then. No public source gives
  a target enrollment number or an expected results date. It is also, as far as could be
  determined, testing trametinib **monotherapy**, not the drug+vaccine combination this module
  spends most of its effort exploring -- so even a full readout of that trial would only speak to
  the weakest arm modeled here.

### Does the durable-response finding hold up against real human data? (And a mistake caught doing it)

The "real trial data that exists but wasn't folded in as a model parameter" bullet above already
found the closest available real analog -- COMBI-d/COMBI-v's pooled 5-year follow-up of
dabrafenib+trametinib in human BRAF-mutant melanoma -- and explicitly declined to fit it into any
model parameter, for good reason: "mapping a human/melanoma/BRAF cohort onto a canine/HS/PTPN11-
KRAS model would stack a cross-species extrapolation on top of an already-illustrative one."

That standard was then violated a few steps later. Prompted to check whether this module's
durable-response finding "holds up," a first pass ran `mapk-durability-horizon-demo` across the
full `preexisting_prob` sweep and compared the output to COMBI-d/COMBI-v's numbers -- at the
original default (0.30), 5-year durable response (92%) overshot even the trial's most favorable
subgroup (71% 5-year OS among complete responders) by 21 points; at `preexisting_prob=0.70`, the
gap narrowed to 11 points. That narrowing was then used to actually recenter
`_PREEXISTING_PROB_CENTRAL` to 0.70 -- exactly the kind of fitting the comment above had just said
not to do, framed at the time as "the same loose analogy used for HSA's eBAT recentering." On
challenge, that framing doesn't hold up:

- **HSA's eBAT recentering (below) differs from this module's modeled drug in mechanism only.**
  Same species (dog), same disease (HSA), same question (does a real HSA outcome suggest more
  pre-existing resistance than assumed). That's a genuinely loose analogy, but a single-axis one.
- **COMBI-d/COMBI-v stacks four mismatches against this module at once**: different species
  (human vs. dog), different disease and cell lineage (melanocyte-derived metastatic melanoma vs.
  histiocyte-derived HS), different driver mutation/pathway node (BRAF V600E/K vs. this module's
  PTPN11/KRAS), and a mechanistically different drug pairing (COMBI-d/v is two real MAPK-pathway
  inhibitors blocking the *same* pathway at sequential nodes; this module pairs its MAPK inhibitor
  with an illustrative, deliberately *mechanism-agnostic* drug hitting a *different* pathway
  entirely). It is a worse analogy than the eBAT one on every axis, not an equivalent one.
- **It's specifically a bad source for this parameter.** `preexisting_prob` represents how much
  pre-existing clonal heterogeneity a disease carries. Melanoma has an unusually high,
  UV-mutagenesis-driven tumor mutational burden -- among the highest of any human cancer -- so
  whatever rate of pre-existing resistant clones it implies says very little about a UV-unrelated
  canine sarcoma's clonal heterogeneity, independent of the species/disease mismatch already
  disqualifying the comparison.

`_PREEXISTING_PROB_CENTRAL` is reverted to its original **0.30**. `COMBI_D_V_FIVE_YEAR_BENCHMARK`
stays in `mapk_scenarios.py`, but demoted to the same role `LOMUSTINE_BENCHMARK` and
`MAPK_INHIBITOR_HUMAN_BENCHMARK` already play: a labeled reference line reported for scale,
explicitly *not* a calibration target, with a caveat field that says so directly this time.

One fix from this pass does survive on its own merits, independent of the recentering mistake: the
same CLI-default-drift bug already found and fixed in the HSA module existed here too --
`cli.py`'s `--preexisting-prob` defaults for all eight `mapk-*` commands were hardcoded `0.30`
literals duplicating `mapk_scenarios._PREEXISTING_PROB_CENTRAL`, decoupled from it in a way that
would have silently broken if that constant ever legitimately changed for an unrelated reason.
Fixed by importing the constant directly, with a regression test exercising the actual CLI path,
not just the Python function default -- this is worth keeping even though the specific recentering
that motivated finding the bug was itself wrong.

### Is the potency the model needs actually achievable?

Every "100% durable response, flat to ten years" figure above rests on `max_kill_2 = 0.08`, and the
model could not say whether that is reachable, because `max_kill_2` entered it as a bare asserted
number with no link to anything measurable. `pharmacology.py` closes that gap — converting real in
vitro and PK observables into `max_kill_2`/`ic50_nM_2` so achievability becomes a question about
named, individually-checkable inputs.

```bash
canine-dsp cdk46-achievability-demo --target-max-kill 0.08 --out results/cdk46-achievability
```

**The answer is no, and it fails two independent checks that would need different fixes.**

**Constraint 1 — the cytostatic ceiling.** `max_kill` is a per-day rate and only means anything
against a clone's own growth rate. A drug that arrests the cell cycle can at most drive *net* growth
to zero; it cannot remove cells, because arrested cells are still there. So for a cytostatic agent
`max_kill <= growth_rate`. That is arithmetic, not a modeling convention, and it needs no PK data at
all. CDK4/6 inhibitors are the textbook cytostatic class, and this was checked in *canine* cells
rather than assumed from human pharmacology: in canine melanoma lines abemaciclib inhibited
proliferation "primarily through G1 phase arrest and senescence," with cleaved PARP showing "only
weak signal intensity, suggesting that apoptosis may not be a major mechanism" (PMC12240792).

| Clone | growth/day | cytostatic ceiling | is 0.08 above it? |
|---|---|---|---|
| sensitive | 0.0600 | 0.0600 | yes |
| pathway_reactivation | 0.0500 | 0.0500 | yes |
| rtk_bypass | 0.0550 | 0.0550 | yes |
| target_site_mutation | 0.0580 | 0.0580 | yes |

0.08 exceeds every resistant clone's ceiling by **38–60%**. No dose reaches it, because it is not a
dosing question. And the corollary is stronger than the headline: even at infinite concentration
with perfect arrest of every cell, a purely cytostatic second drug drives each margin to *exactly
zero* — stasis — never negative. So it cannot produce the **mechanistic elimination** this module
attributes to `max_kill_2=0.08` at all; indefinite stasis is its theoretical best case.

**Constraint 2 — real canine potency is 9–31x weaker than assumed.** Independently:
`CDK46_ILLUSTRATIVE_IC50_NM = 100.0` was always labeled illustrative, and the real measured value in
canine cells is **910–3090 nM** (abemaciclib, five canine melanoma lines; normal fibroblasts 5230 nM,
so there is real selectivity). `CDK46_ILLUSTRATIVE_CSS_NM = 500.0` was set as a 5x margin over the
*assumed* IC50 — against the real range it sits at or below the IC50:

| IC50 | saturation reached at the modeled 500 nM |
|---|---|
| 100 nM (assumed) | 0.918 |
| 910 nM (real, most potent line) | 0.289 |
| 3090 nM (real, least potent line) | 0.061 |

This compounds rather than offsets constraint 1, because the requirement scales as
1/saturation_fraction — operating below saturation *raises* the Emax you would need. Required
`max_kill` to reverse the worst resistant clone (margin 0.0579/day on trametinib alone):

| IC50 | exposure | saturation | required max_kill | vs. ceiling (0.058) |
|---|---|---|---|---|
| 100 nM | 500 nM | 0.918 | 0.0631 | **above — impossible** |
| 100 nM | 2000 nM | 0.989 | 0.0586 | **above — impossible** |
| 910 nM | 2000 nM | 0.765 | 0.0757 | **above — impossible** |
| 3090 nM | 500 nM | 0.061 | 0.9482 | **above — impossible** |

Note the first row: the requirement exceeded the cytostatic ceiling *even at this module's own
optimistic assumptions*. The real-IC50 discovery did not create the problem, it deepened it by an
order of magnitude. In the most generous defensible cytostatic case — perfect arrest, real canine
potency, modeled exposure — achieved kill is 0.003–0.004/day against margins of 0.036–0.058, short
by roughly 15x.

**What would change the answer** (recorded in `summary.json` so it is actionable rather than
rhetorical): a genuinely **cytotoxic** second agent is the only route that lifts constraint 1, and
that means a different drug class, not a different dose of a CDK4/6 inhibitor. Beyond that: a real
canine *HS* dose-response measurement (every potency number here comes from melanoma/mammary/lymphoma
lines — no CDK4/6 inhibitor has ever been tested against a canine HS line); real canine PK for a
specific CDK4/6 inhibitor (none found, so exposure is swept, not known); or better primary-drug
suppression, since the bar for drug 2 is set by what trametinib leaves behind.

The demo also emits a **feasibility frontier** over (IC50 x exposure) with the cytostatic ceiling
drawn as a contour, so a future real measurement can be located on it directly instead of re-arguing
from scratch.

**What this means for everything above.** The `max_kill_2=0.08` results are not wrong as model
output — they are correct arithmetic on a parameter now shown to be pharmacologically unreachable
for the drug class named. The honest reading of this module's HS durability story therefore shifts
to the `max_kill_2=0.05` regime (100% → 99.7% → 92% → 81% at 1/2/5/10 years, with erosion driven by
`pathway_reactivation`) — and even 0.05 requires potency this analysis suggests is optimistic. The
"purely pharmacological path to mechanistic elimination" section above should be read as
*conditional on a cytotoxic agent that has not been identified*, not as an available option.

### Reasoning toward the driver mutation instead of looking it up

The load-bearing unverified premise of this whole module is that this presentation primary CNS / primary
pulmonary HS carries a PTPN11 or KRAS hotspot at all. Searching confirmed that gap is real rather
than an oversight: the paper that *defines* the localized pulmonary entity (19 dogs of one breed,
PMID 26155931) is purely histopathologic and predates the canine HS mutation literature entirely;
the largest canine HS sequencing cohort found (129 HS + 26 HHS, PMC11353564) contains exactly one
Welsh unsequenced_breed, pooled into an undifferentiated "other breeds" bucket. **No canine HS study stratifies
mutations by anatomic site at all.** So the mutation can't be looked up — but it can be reasoned
toward, which is what `histiocytic_origin.py` encodes.

```bash
canine-dsp driver-hypothesis-demo --out results/unsequenced_breed-drivers
```

**The inference chain.** Two clinical observations do the work. (1) The tumors are **Iba-1
positive** (AIF1 — macrophage/microglial lineage, not Langerhans or interdigitating-DC lineage).
(2) The disease is **anatomically localized to lung and CNS**, unlike BMD HS's disseminated
splenic/hepatic pattern. Those two facts intersect at something specific: lung and brain are
precisely the two mammalian tissues whose macrophage compartments — alveolar macrophages and
microglia — are seeded prenatally from yolk-sac erythro-myeloid progenitors, self-renew in situ,
and are maintained largely independently of bone-marrow output in adults (Gomez Perdiguero et al.
2015, *Nature*, PMID 25470051). That yields the **tissue-resident macrophage hypothesis**: localized HS
may be a neoplasm of a prenatally-seeded, locally self-renewing macrophage compartment, and it
stays localized because its cell of origin *does not circulate* — not because it was caught early.
This is the same cell-of-origin logic already established for human LCH, where MAPK activation in
an HSPC gives multisystem disease and the same lesion in a tissue-restricted precursor gives
localized single-system disease (PMC7556147).

**What the hypothesis predicts that a conventional candidate list wouldn't:** CSF1R. It is the
master survival receptor for exactly those two compartments (CSF1R inhibition depletes essentially
all microglia in healthy animals), so it explains the lung/CNS restriction rather than merely
tolerating it. No canine HS study found has sequenced CSF1R. It also implies a *different second
drug* than this module models: pexidartinib is FDA-approved (2019, for tenosynovial giant cell
tumour — itself a CSF1-driven histiocytic proliferation), CSF1R IC50 ~20 nM, oral, and **BBB
penetrant** — which speaks directly to the ~15% brain penetration ceiling recorded for trametinib
in `BRAIN_PENETRATION_FRACTION`, the single worst structural problem facing the PIHS scenario.

Separately, this pass turned up the **first real genetic rationale for the CDK4/6 inhibitor** this
module already models as a deliberately mechanism-agnostic second node: the BMD HS susceptibility
GWAS narrows to a 75 kb window spanning MTAP through the last exon of CDKN2A (Shearin et al. 2012,
PMID 22623710). CDKN2A encodes p16INK4a, the endogenous brake on CDK4/6 — loss of that brake is the
canonical setting for CDK4/6-inhibitor sensitivity. That was not why CDK4/6i was chosen, so this is
retrospective support rather than circularity; whether this presentations share the BMD locus is unknown.

**Structural triage of the 9-gene panel** (all resolved; human + dog AlphaFold models, real):

| Gene | Tier | Dog identity | Human-dog pLDDT coherence | Hotspots conserved |
|---|---|---|---|---|
| NRAS | B | **100%** | 1.00 | Q61 ✓ |
| MAP2K1 | B | 99.5% | 0.64 | Q56, K57, C121 ✓ |
| PTPN11 | A | 99.3% | 0.81 | E76, G503 ✓ |
| KRAS | A | 98.9% | 1.00 | Q61 ✓ |
| BRAF | B | 98.8% | 0.53 | V600 ✓ |
| MTAP | D | 95.4% | 1.00 | — |
| **CSF1R** | **C** | **85.3%** | **0.21** | — |
| CDKN2A | D | 83.0% | 1.00 | — |
| CSF1 | C | 74.5% | 0.48 | — |

Three real findings, one of them a caution against the module's own new hypothesis:

- **All 8 checkable hotspots are conserved in dog**, and all 8 literature positions carried the
  expected wild-type residue in the human structure (so no stale or mis-transcribed coordinate
  slipped through). Every MAPK candidate is chemically plausible in dog; none can be excluded on
  conservation grounds.
- **Residue numbering does not transfer, and this is the most immediately actionable output.**
  BRAF V600 aligns to dog position **583** (offset 17); MAP2K1 Q56/K57/C121 align to dog **97/98/162**
  (offset −41). A lab sequencing a dog tumor at the human coordinate would interrogate the wrong
  residue entirely. (Computed against the specific dog accessions listed; most dog entries are
  automatically annotated and isoform choice can shift numbering, so confirm against whichever
  reference a lab actually uses.)
- **CSF1R is the most mechanistically motivated candidate but the least structurally assured** —
  lowest identity of any MAPK-pathway candidate (85.3%) and by far the lowest human-dog pLDDT
  coherence (0.21, versus 0.53–1.00 for everything else), with CSF1 worse still at 74.5%. Since
  pexidartinib was designed against *human* CSF1R, that materially weakens the "an approved human
  drug would work here" half of the CSF1R argument, while leaving the cell-of-origin reasoning
  intact. This is the opposite of what the hypothesis would have preferred to find, and it was
  found by checking rather than assuming.

**The nonlinear analysis failed its own positive control, and is reported as failed.** A
second-order Volterra model (reusing the repo's existing basis-reduced, elastic-net machinery
unchanged, protein treated as one group so lag histories never cross a sequence boundary) was fit
to predict structural confidence (pLDDT) from local Kyte-Doolittle hydropathy. The hypothesis: the
residual — structure *not* explained by local chemistry — should be elevated at allosteric and
autoinhibitory positions, which is where several known hotspots sit (PTPN11 E76 is at the
N-SH2/PTP autoinhibitory interface). Tested against a 10,000-draw permutation null at the four
verified control hotspots: **p = 0.70 (PTPN11), 0.10 (KRAS), 0.76 (BRAF) — none significant.** So
the method does not earn the right to nominate residues in CSF1R or CSF1, and deliberately isn't
used to. `summary.json` records `cleared_for_downstream_use: false`. The low power (1–2 positions
per protein) cuts both ways: this is a failed validation, not proof no such signal exists.

`spectral.bicoherence` was added as a genuinely nonlinear primitive (quadratic phase coupling; zero
for a linear Gaussian process with the same PSD, so it sees what a power spectrum and coherence
structurally cannot). Writing its test surfaced a real interpretation caveat now documented in the
function: bicoherence measures phase-relationship *consistency across averaged segments*, so it
saturates near 1 for any signal whose segments share an identical phase geometry — a deterministic
sinusoid triplet scores ~1 whether or not its components are truly coupled. The per-gene values
above the diagonal (0.07–0.43) are therefore reported descriptively, not as a finding.

The honest bottom line: this narrows *what to sequence first* and supplies a mechanistically-matched,
BBB-penetrant drug candidate nobody in this line of work had considered — but it does not identify
the mutation, and the one novel analysis that might have gone further failed validation. The
highest-value real-world action is unchanged and cannot be substituted for by modeling: **sequence a
series of this presentation primary CNS and primary pulmonary HS tumors, stratified by anatomic site.**

### Testing the CSF1R hypothesis in the model — and watching it lose

The obvious next move was to swap the illustrative CDK4/6 inhibitor for a CSF1R inhibitor and see
whether the better-matched, BBB-penetrant drug does better. Taking the biology seriously first
predicted it wouldn't, and the model confirms it.

**Why a scalar second drug is the wrong model for CSF1R.** The engine's second drug was documented
and validated as a *scalar applied identically to every clone* — correct for CDK4/6i, which acts on
the cyclin D/CDK4/6 cell-cycle node, a genuinely **parallel** axis that doesn't care how a clone
reactivated upstream signaling. CSF1R is the opposite case. It sits at the top of the same **serial**
cascade the resistance lesions live on:

```
CSF1R → SHP2/PTPN11 → RAS (KRAS/NRAS) → RAF (BRAF) → MEK (MAP2K1) → ERK
```

Every resistance mechanism this module models, and every Tier A/B candidate driver above, is
constitutively active *downstream* of the receptor — and a downstream activating lesion is by
definition insensitive to blocking an upstream receptor. Modeling CSF1Ri with a scalar would
silently credit it with resistance coverage it cannot have. So `ResistanceModel` was generalized to
accept a `(k,)` array for `ic50_nM_2`/`max_kill_2` (scalar still means mechanism-agnostic; the
validator rejects wrong-length arrays rather than letting them broadcast), and
`csf1r_combination_scenarios` de-rates the CSF1Ri kill term to `CSF1R_DOWNSTREAM_ESCAPE_FRACTION`
on every resistant clone.

Note this is the one place in the whole repo with a **real measured second-drug potency**:
pexidartinib's CSF1R IC50 = 20 nM. Two caveats keep it from being the clean anchor it looks like —
it's measured against *human* CSF1R, and the triage above found dog CSF1R the *least* conserved
candidate (85.3% identity, 0.21 pLDDT coherence), so this is the candidate where cross-species
potency transfer is least assured. And IC50 is not a kill ceiling: `max_kill` stays swept.

**Deterministic growth margins at matched potency** (positive = clone still expands; the exact
calculation, not a simulation):

| Clone | MEK+CDK4/6i @0.08 | MEK+CSF1Ri @0.08 |
|---|---|---|
| sensitive | −0.1245 | −0.1245 |
| pathway_reactivation | **−0.0236** | +0.0389 |
| rtk_bypass | **−0.0377** | +0.0247 |
| target_site_mutation | **−0.0155** | +0.0469 |

CDK4/6i flips all three negative — the mechanistic elimination documented earlier. CSF1Ri leaves all
three positive at *every* potency in the swept range (0.02–0.12), verified by test. **Monte Carlo:**

| Regimen | 1yr | 2yr | 5yr | 10yr |
|---|---|---|---|---|
| MEK + CDK4/6i @0.05 | 100% | 99.7% | 92.0% | 81.0% |
| MEK + CDK4/6i @0.08 | 100% | 100% | 100% | **100%** |
| MEK + CSF1Ri @0.05 | 72.3% | 70.0% | 70.0% | **70.0%** |
| MEK + CSF1Ri @0.08 | 73.7% | 70.0% | 70.0% | **70.0%** |

CSF1Ri pins at **exactly 70.0%** regardless of potency or horizon, and that number is interpretable
rather than arbitrary: it is `1 − preexisting_prob` (0.30). CSF1Ri rescues precisely the dogs who
start *without* a pre-existing downstream-mutant clone and cannot help any dog who starts with one —
so its ceiling is the fraction of patients with no pre-existing resistance, and raising its potency
moves that ceiling not at all. A cleaner illustration of "potency cannot substitute for pathway
coverage" than anything designed on purpose.

**Even in the CNS, where CSF1Ri's BBB advantage should matter most, it still loses** (trametinib at
its real 15% brain penetration):

| Regimen | 1yr | 2yr | 5yr | 10yr |
|---|---|---|---|---|
| MEK alone (15% brain) | 0% | 0% | 0% | **0%** |
| + CDK4/6i @0.08 | 100% | 100% | 100% | **100%** |
| + CSF1Ri @0.08 | 70.7% | 70.0% | 70.0% | **70.0%** |

The resistance-coverage deficit dominates the delivery advantage. **One honest caveat that could
flip this specific comparison:** the CNS runs scale only *trametinib* by the brain-penetration
factor — CDK4/6i is implicitly given full CNS availability, which is unverified and probably
generous, since CDK4/6 inhibitors as a class penetrate the brain poorly. If real CDK4/6i brain
penetration is bad, the CNS column could reverse. That is a genuine open question, not a settled
result, and it is the strongest remaining argument for CSF1Ri.

**So the combined-therapy answer, revised by its own findings:** the durable-response regimen
remains **MEK inhibitor + CDK4/6 inhibitor** — and this pass *strengthened* the case for it, via the
MTAP-CDKN2A locus giving that drug real genetic rationale for the first time. CSF1R's role is
demoted from "better second drug" to, at most, **a debulking/CNS-delivery adjunct**: it kills the
receptor-dependent bulk population and reaches the brain, but it cannot cover resistance and
therefore cannot deliver durability on its own. The lineage-matched drug and the
resistance-covering drug turn out to be different drugs, which is exactly the kind of conclusion
that only shows up if the pathway topology is modeled rather than assumed away.

### Was the melanoma potency data even the right objection? And treating one sequenced dog

Two challenges to the achievability finding above, both of which changed the answer.

**First: is "canine melanoma cells, not canine HS cells" actually a valid criticism of the IC50
data?** Partly, but it names the wrong axis, and correcting it makes the conclusion *stronger*
rather than weaker. CDK4/6-inhibitor sensitivity does not track tissue of origin; it tracks the
molecular state of the cyclin D–CDK4/6–RB axis. The determinants are intact RB1 (loss is the
dominant resistance mechanism), D-cyclin activating features, and CCND1/CDK4/6 amplification
([ASCO Educational Book review](https://ascopubs.org/doi/10.1200/EDBK_281085);
[Gong et al., *Cancer Cell* 2017](https://www.cell.com/cancer-cell/fulltext/S1535-6108(17)30509-3)).
So the right question is not "melanoma vs. histiocytic sarcoma" but "does canine HS share the
RB-pathway genotype of those melanoma lines" — which is unknown, because no canine HS line has been
profiled for it. One inference I had been tempted to make is also wrong: BMD HS's CDKN2A/MTAP locus
does *not* imply CDK4/6i sensitivity, since CDKN2A-mutant cancers without co-occurring D-cyclin
lesions "rarely show high sensitivity" and instead show intermediate response.

But none of this rescues the potency requirement, because it only touches constraint 2. Even if HS
turned out to be maximally sensitive — IC50 exactly at the illustrative 100 nM — constraint 1 is
untouched: a cytostatic drug still cannot kill faster than cells divide, and the worst clone still
needs 0.063/day against a 0.058/day ceiling. **Accepting the objection moves the binding constraint
from "the drug is too weak" to "the drug's mechanism forbids it", which is the harder of the two
failures.** That reframing is what motivated looking for a different second drug entirely.

**Second: had any of this been done as an N=1 problem, given that a real patient's tumor can be
sequenced?** Partially — the variance decomposition above already found 99.8% of outcome variance is
"which dog you are" and already named pretreatment subclone detection as the diagnostic that would
matter. What it never did was check whether that diagnostic can work. It assumed it would.

```bash
canine-dsp single-patient-demo --breed bmd --out results/single-patient
```

`single_patient.py` closes that gap, and the answer is no — with a compensating discovery that the
sequencing is worth doing anyway, for a different reason.

| What sequencing is asked to resolve | Can it? | Effect on the model |
| --- | --- | --- |
| Is a MAPK driver present (is trametinib even on-target)? | **Yes, outright** | 44/96 BMD HS carry PTPN11 or KRAS (Takada et al. 2019, *Genes* 10(7):505). Driver lesions are clonal, ~25–50% VAF — orders of magnitude above any assay floor. |
| Does a resistant subclone already exist? | **Effectively no** | The model's own prior puts it at 10⁻⁶–10⁻³ of tumor, i.e. ≤0.05% VAF. Every clinically orderable assay's floor sits *above* that entire range. |

The second row is the sharper result, so it is worth being precise about. `posterior_preexisting_prob`
does the Bayes update for a *negative* sequencing result, and because the size prior is log-uniform
the detectable fraction is a ratio of log-widths, not linear widths — which is why intuition
overestimates it badly:

| Assay | VAF floor | Cell-fraction floor | Prior mass visible | `preexisting_prob` after a negative result |
| --- | --- | --- | --- | --- |
| standard targeted NGS | 2% | 4×10⁻² | 0% | 0.30 → **0.30** (no change) |
| UMI panel, clinical operating point | 1% | 2×10⁻² | 0% | 0.30 → **0.30** (no change) |
| UMI best published / ddPCR | 0.1% | 2×10⁻³ | 0% | 0.30 → **0.30** (no change) |
| QBDA (research) | 0.01% | 2×10⁻⁴ | 23% | 0.30 → 0.25 |
| duplex sequencing, best ever published | 0.0031% | 6.2×10⁻⁵ | 40% | 0.30 → 0.20 |

**Every assay a clinician can actually order leaves the number exactly where it started.** A negative
result is uninformative, not reassuring, and the best sensitivity ever published in a research
setting buys a 1.5× shrinkage. Input DNA is *not* the limit — seeing a 10⁻⁶ subclone needs ~40 µg,
which a resection yields. Two other things are: the assay error floor, and spatial sampling, which
no sequencing depth fixes. `spatial_detection_probability` brackets it and the bracket is the
finding: sampling 1% of a 10¹⁰-cell tumor detects a dispersed 10⁻⁶ subclone with near-certainty and
a single focal one with probability ~0.01. Which regime holds is unmeasured, so a negative result
cannot be interpreted even given a perfect assay.

`partition_by_preexisting_subclone` then splits any existing Monte Carlo ensemble by its day-0 state,
with no re-simulation, and the split is stark enough to undermine how the population numbers
throughout this README should be read:

| lomustine `max_kill` | no pre-existing subclone | pre-existing subclone | cohort average |
| --- | --- | --- | --- |
| 0 (trametinib alone) | 99.1% | 0.0% | 68.2% |
| 0.05 | 99.1% | 0.0% | 68.6% |
| 0.12 | 99.4% | 1.3% | 69.0% |
| 0.20 | 100% | 13.5% | 73.2% |

The cohort column is almost exactly `1 − preexisting_prob`. **At a realistic exposure duration the
reported durable-response fraction is mostly a readout of that one unfitted parameter, and barely a
readout of the drug at all** — a 4× potency range moves it five points. No patient is 68% durable;
each is in one of the two outer columns.

That near-degeneracy has one useful consequence: it makes a matched real-world cohort outcome an
unusually direct estimator of `preexisting_prob`. `implied_preexisting_prob` inverts the mixture, and
Skorupski et al. 2009 (already cited above for its 568-day median survival) supplies the admissible
comparator — its 6/16 relapse-free fraction matches on all four axes that made the COMBI-d/v
comparison inadmissible: species, disease, localized presentation, and treatment *structure* (local
therapy then adjuvant systemic drug). Inverting against it implies **p ≈ 0.62, roughly double the
0.30 this module centres on** — i.e. the model is optimistic on durable-response fraction by about
2×, while its progression *timing* is in the right range (214-day median vs. the benchmark's 243-day
median disease-free interval). This is deliberately **not** written back into
`_PREEXISTING_PROB_CENTRAL`: the benchmark's systemic agent is a cytotoxic rather than a MEK
inhibitor, it has no molecular stratification (so it mixes the two arms of the driver split above),
n=16, and "relapse-free at follow-up" is not the model's "no progression in 730 days". The existing
`[0.05, 0.15, 0.30, 0.50, 0.70]` sweep already spans it, which is the honest way to carry it.

### A different second drug: lomustine, and the two candidates failing on opposite axes

Given that constraint 1 is mechanistic, the fix has to be a drug class, not a dose. Lomustine (CCNU)
is the obvious candidate and is better-evidenced than the CDK4/6 inhibitor on three independent
counts, all real: it is a DNA-alkylating nitrosourea, so **genuinely cytotoxic** and not
ceiling-bound; it has measured activity **in this exact disease and species** (46% ORR, 60–90 mg/m²,
n=56 with measurable disease — [Skorupski et al. 2007](https://pubmed.ncbi.nlm.nih.gov/17338159/)),
so there is no lineage-proxy problem at all; and it is **CNS-penetrant**, which addresses the
~15%-of-plasma brain exposure that is the MEK inhibitor's worst structural weakness in the primary
CNS presentation. A scalar `max_kill_2` is also the *correct* model here, unlike for CSF1R: DNA
crosslinking acts downstream-independently, so there is no pathway-serial de-rating to apply.

It works, in-model, and then it doesn't — because it trades the ceiling for a different hard limit.
Lomustine's dose-limiting toxicity on repeated dosing is cumulative and, for the liver, irreversible
(median 350 mg/m² cumulative and 4 doses in dogs that developed hepatotoxicosis). `cumulative_dose_limited_days(70, 21, 350)`
turns that into 5 cycles / **105 days** of exposure, which populates the engine's
`css_reference_2_duration_days` from real toxicity data rather than leaving it always-on. Running each
potency both capped and counterfactually chronic isolates what the cap costs:

| lomustine `max_kill` | worst clone's margin | capped at 105 d (real) | chronic (counterfactual) |
| --- | --- | --- | --- |
| 0.05 | +0.012 | 68.6% | 99.6% |
| 0.08 | −0.015 | 68.6% | 100% |
| 0.12 | −0.052 | 69.0% | 100% |
| 0.20 | −0.126 | 73.2% | 100% |

At ≥0.08 the drug genuinely reverses every resistant clone's growth margin — the thing the CDK4/6
inhibitor cannot do at any dose. It changes almost nothing, because 625 of the 730 days are spent
unsuppressed, and the margin snaps back from −0.015 to +0.058 the day dosing stops. In the
pre-existing-subclone arm specifically, chronic dosing at 0.05 gives 98.7% and the real 105-day cap
gives **0.0%**. This is the same pattern the HSA module found for eBAT — a time-limited agent's
benefit erodes once exposure ends — now reproduced independently in HS.

**Which gives the sharpest negative result of this whole pass.** Reversing these clones needs two
things simultaneously: a kill rate at or above their growth rates, *and* that rate sustained long
enough that the subclone cannot regrow. The two candidates each satisfy exactly one:

- **CDK4/6 inhibitor** — dosable chronically (oral, no cumulative organ cap), and reaches ~100%
  durable response in-model when dosed continuously. Cannot reach the kill rate: cytostatic agents
  are capped at the clone's own growth rate.
- **Lomustine** — reaches the kill rate (cytotoxic, ceiling does not apply). Cannot sustain it:
  cumulative irreversible hepatotoxicity caps exposure at ~105 days.

Neither is the answer, for non-overlapping reasons, which is a stronger statement than either
analysis alone and names the target precisely: a ceiling-free partner *without* a cumulative-dose
duration cap. Whether one exists for canine HS is not established here. The most concrete thing left
to test is the trade along exactly that axis — metronomic lomustine has been reported tolerable in
dogs for up to ~12 months ([Tripp et al. 2011](https://academic.oup.com/jvim/article/25/2/278/8451316)),
i.e. lower kill rate for much longer duration, and this model does not yet evaluate it.

On the vaccine question: nothing here argues for a *different* vaccine, and the driver-conditioning
result argues for the same shared-hotspot design already modeled, applied more selectively. A fully
personalized neoantigen vaccine is the intuitive N=1 answer, but the sequencing analysis above cuts
against it — the mutations worth targeting are the clonal driver (which the existing shared-antigen
PTPN11/KRAS construct already covers, and which is what makes an off-the-shelf design viable for a
rare veterinary disease) rather than subclonal resistance mutations, which are exactly the ones that
sit below every assay floor. What the driver split *does* change is patient selection: the vaccine
and the whole MAPK premise apply to the ~46% of **BMD** dogs with a sequenced MAPK lesion, and for
the rest the actionable response is a different primary drug, not this regimen with worse odds. That
"46%" figure is BMD-specific, which the next section exists to make impossible to miss.

### Everything above is BMD. A this presentation is not "a BMD in a different breed's body"

Everything in this N=1 section — the 44/96 driver frequency, the `localized_pihs_scenarios` tumor
model, the Skorupski calibration benchmark — is BMD-context end to end. `single-patient-demo`
originally applied it to "one sequenced dog" without saying so, which given this whole module's own
prior, extensively-modeled premise (`histiocytic_origin.py`: localized PIHS/pulmonary HS as a clinically
distinct, unsequenced presentation) is a real mismatch — the same species of error as treating
canine-melanoma CDK4/6i data as informative about canine-HS potency, just one level up: treating
one breed's HS as informative about a different breed's, without checking whether the clinical
picture actually matches.

It doesn't, on the one axis where real breed-matched data exists. `LOCALIZED_PULMONARY_HS_BENCHMARK`
(Sakai et al. 2015, 19 dogs of one breed) reports a **133-day median survival** — roughly a
quarter of the BMD-context Skorupski benchmark's 568 days — and regional nodal involvement in many
cases, meaning the single-compartment "debulking reaches everything" premise the BMD arm leans on
does not hold for this presentation at all (this repo already built the right tool for that:
`run_monte_carlo_two_compartment`, used in `mapk-pulmonary-two-compartment-demo` above). And on
driver frequency, a this presentation isn't a worse coin flip than BMD's 46/54 — there is no coin to flip: zero
this presentations have ever been sequenced for canine HS drivers, so `driver_conditioned_arms(breed="unsequenced_breed")`
returns `None`, not a number, and the honest state is "unknown, `histiocytic_origin.py`'s Tier A-D
panel is a hypothesis, not a measurement."

`single_patient_demo` now runs a real, separate fifth analysis for this rather than reusing the BMD
numbers: `localized_pulmonary_scenarios` + `run_monte_carlo_two_compartment`, swept over
`NODAL_INVOLVEMENT_PROB_SWEEP`, checked against the Sakai benchmark instead of Skorupski. In testing
(200 trials, `preexisting_prob=0.30`): median time to progression came out at 205–233 days across
the nodal sweep — much closer to Sakai's 133-day median survival than the BMD arm's 568-day
benchmark is, though "time to progression" and "survival" are not the same endpoint, so this is
a directional consistency check, not a validation. The function also now refuses to run its BMD
arm (findings 1–4) for `breed="unsequenced_breed"` at all, with an error pointing at the presentation-specific arm
instead of silently producing a mislabeled number — and, closing a second mismatch caught building
this fix, `driver_conditioned_arms` generalizes cleanly to *any* unsequenced breed, including
flat-coated retriever, which has its own real GWAS germline locus but was never in Takada et al.'s
driver-sequencing cohort either.

The corrected, complete statement of what N=1 sequencing buys, by breed:

| | BMD (or golden retriever) | this presentation |
| --- | --- | --- |
| Driver present? | Known base rate → fact (44/96, or 3/13) | Unknown — sequencing is discovery, not confirmation |
| Pre-existing resistance? | Effectively unresolvable (finding 2) | Same — the detection-floor argument doesn't depend on breed |
| Matched natural-history benchmark | Skorupski 2009, 568-day median survival | Sakai 2015, 133-day median survival |
| Structural model | Single-compartment (debulking reaches all disease) | Two-compartment (regional nodal spread documented) |

### The half of the argument this repo had been using in only one direction

`_PREEXISTING_PROB_CENTRAL`'s comment rejects the human melanoma COMBI-d/v trial as a recentering
basis, and one of its stated reasons is mutational burden: *"melanoma has an unusually high,
UV-mutagenesis-driven tumor mutational burden, so whatever rate of pre-existing resistant clones it
implies is not evidence about a UV-unrelated canine sarcoma's clonal heterogeneity."* That reasoning
was only ever used **defensively** — to block a pessimistic recalibration — and never applied in its
positive form. Both scenario modules still ship the identical `_SEEDING_RATE_TOTAL = 0.012`, meaning
the model as written assumes HS is exactly as mutable as hemangiosarcoma.

**The argument is a *rate* argument, not a *count* argument, and conflating those is a mistake made
in this project's own discussion.** It does **not** claim a lineage-restricted tumor has fewer
distinct escape mechanisms — nothing here changes the clone count, and an RTK-driven tumor hit with
an RTK inhibitor generally accumulates a *rich* catalog of resistance routes. It claims that the rate
at which each route gets populated scales with the tumor's mutation rate. In this engine those are
exactly two parameters: `seeding_rates` and `preexisting_prob`.

```bash
canine-dsp mutational-supply-demo --breed bmd --out results/mutational-supply
```

`scale_preexisting_prob` gets the functional form right, which matters: `preexisting_prob` is a
saturating probability ("at least one clone exists"), not a rate, so it scales as
`p' = 1 − (1−p)^r`, not linearly. Linear scaling would understate the benefit at small `p` and
overstate it near `p = 1`, where the reference tumor is already saturated and cutting supply can't
help. Seeding rates *are* rates and do scale linearly.

| HS burden vs. a high-burden comparator | `preexisting_prob` | durable response (MC) | analytic `1−p` |
| --- | --- | --- | --- |
| 1.0 — **status quo, as shipped** | 0.300 | 0.700 | 0.700 |
| 0.5 | 0.163 | 0.837 | 0.837 |
| 0.25 | 0.085 | **0.917** | 0.915 |
| 0.1 | 0.035 | 0.960 | 0.965 |

So yes — the derivation holds, and it's large: ~70% → ~92% durable response at a fourfold lower
burden. The analytic shortcut tracks the simulation within half a point, but only because the two N=1
arms are saturated (0.997 vs 0.000); that's asserted against the engine rather than assumed, since it
would fail in a regime where the arms sat closer together.

**The decomposition is the actual finding, and it narrows the argument.** Scaling each parameter
separately at 0.25× burden:

| arm | durable response | Δ |
| --- | --- | --- |
| baseline | 0.700 | — |
| acquired seeding rate scaled only | 0.703 | **+0.003** |
| `preexisting_prob` scaled only | 0.910 | **+0.210** |
| both | 0.917 | +0.217 |

Essentially all of it runs through pre-existing resistance; the acquired-mutation-rate half — the way
the argument is usually stated — contributes ~0.3 of a point. Two saturation effects explain it: the
no-subclone arm is already ~99.7% durable so a lower acquired rate has nothing left to improve, and
the with-subclone arm is lost to lomustine's 105-day duration cap regardless of any mutation rate.
**What matters is whether a resistant clone is already there at treatment start, not the rate at
which new ones arise** — which is an uncomfortable landing, because that's precisely the parameter
the detection-floor analysis above showed no assay can measure.

**Empirically: partly confirmed, and not for HS.** Real pan-canine TMB data now exists
([Alsaihati et al. 2021, *Nat Commun* 12:4670](https://www.nature.com/articles/s41467-021-24836-9);
684 cases, >7 tumor types, >35 breeds) and it does three things:

- **Confirms the defensive half in dogs** rather than by analogy to human UV biology: canine oral
  melanoma really is high-burden (median ≥1 mut/Mb). The melanoma comparator's rejection now has
  dog-specific support.
- **Revises an earlier conclusion of this repo.** The HS-vs-HSA check concluded their differing
  outcomes trace to calibration rather than biology. That was right about mechanism *counts* and
  incomplete about *rates* — canine hemangiosarcoma is measured high-burden, so HSA's more
  pessimistic calibration may be biologically justified rather than arbitrary.
- **Does not measure histiocytic sarcoma.** HS is absent from that cohort, and the only canine HS
  exome study found ([Tani et al. 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10212919/), n=5)
  reports 35 Sanger-validated mutations with no mutations/Mb figure. The ratio the whole argument
  turns on is unmeasured, which is why it's swept rather than asserted, and why neither
  `_SEEDING_RATE_TOTAL` nor `_PREEXISTING_PROB_CENTRAL` was changed.

**One number must not travel with it.** `refuse_bmd_benchmark_transfer` records this explicitly: the
Skorupski inversion implying `p ≈ 0.62` is BMD-context, breed-unstratified and mixed-treatment. If
the low-burden argument holds for localized HS, carrying 0.62 over would be the same breed/stratification
mismatch `driver_conditioned_arms` was rewritten to refuse — running in the *pessimistic* direction,
which is exactly why it was easy to miss. A correction that makes a model look worse still has to be
scoped correctly.

### The correction: three analyses ran with the vaccine switched off

Everything in the three preceding sections — the N=1 reframing, the lomustine work, the
mutational-supply sweep — calls `run_monte_carlo`, **not** `run_monte_carlo_with_vaccine`. All of it
ran with the vaccine at zero. That matters because this project derived a specific structural argument
early on and then stopped using it:

> **None of the three modeled drug-resistance escape mechanisms requires losing the driver-mutation
> antigen a vaccine would target.** `pathway_reactivation` adds a secondary RAS/RAF hit *on top of*
> the original mutation, `rtk_bypass` reactivates parallel signaling *around* it, and
> `target_site_mutation` only alters the MEK-inhibitor *binding site*. All three keep expressing the
> original PTPN11/KRAS hotspot peptide.

That's a **convergence** claim, and it's a different kind from the pharmacological one about a shared
CDK4/6 node. The pharmacological version says the escape routes share a *dependency* one drug can
block — and it needs a potency threshold. This one says they share an *antigen they cannot shed while
remaining what they are*, so the vaccine is escape-route-agnostic **by construction**, not by potency.

```bash
canine-dsp antigen-convergence-demo --breed bmd --out results/antigen-convergence
```

`verify_antigen_convergence` checks this against the engine's actual kill mask rather than restating
it: every drug-resistance clone receives nonzero vaccine kill, exactly one clone (`immune_escape`)
doesn't. It passes, and a deliberately broken mask makes it fail.

**What switching the vaccine on does to the conclusions above** (trametinib + duration-capped
lomustine, 2-year horizon):

| vaccine `max_kill` | whole cohort | **pre-existing-subclone arm** |
| --- | --- | --- |
| 0 — *what the three prior analyses reported* | 0.688 | **0.000** |
| 0.01 | 0.700 | 0.026 |
| 0.03 | 0.872 | 0.579 |
| 0.05 | **1.000** | **1.000** |

The arm I reported three times as "flat 0%, lost to the duration cap regardless of any mutation rate"
goes to 100% at a mid-sweep vaccine potency. That is exactly what antigen convergence predicts: a
pre-existing drug-resistant subclone acquired resistance *without shedding the antigen*, so it is
precisely the patient type a hotspot vaccine covers and the drug-only regimen cannot.

**Two specific things this retracts:**

1. *"Neither agent is the answer... what this regimen would need is a ceiling-free partner without a
   cumulative-dose duration cap. Whether one exists for canine HS is not established here."* — a
   mechanism satisfying both was **already implemented in this repo**. The two-drug analysis was
   correct about the two drugs and wrong to generalize from them:

   | | cytostatic ceiling? | cumulative-dose cap? | covers all routes? |
   | --- | --- | --- | --- |
   | CDK4/6 inhibitor | **yes** (fatal) | no | yes |
   | Lomustine | no | **yes** (fatal) | yes |
   | Hotspot vaccine | **no** | **no** | yes |

   Immune cytolysis removes cells, so no arrest ceiling applies; immunological memory persists after
   dosing, so no cumulative-organ-toxicity stop applies.

2. *"The duration cap is the binding constraint for HS."* True only with nothing to hand off to.
   `handoff_timing` reports the actual schedule: the vaccine starts ramping at day 90, **inside**
   lomustine's 105-day window, and is at ~51% of maximum when the cumulative-dose cap forces the drug
   to stop. Coverage is continuous — though not instantaneously full, since the ramp keeps climbing
   for ~6 more days. Worth being clear that this favourable timing is a **coincidence of two
   independently-set constants** (`VACCINE_START_DAY = 90` predates lomustine entering the model), not
   a designed schedule.

**Endurance, and what actually leaks.** At vaccine `max_kill = 0.05`: flat 100% to 2 years, ~98.8% at
5 years, ~97.3% at 10. I initially wrote that the erosion was antigen loss — **the relapse breakdown
does not support that.** Every 10-year relapse is `target_site_mutation`, and the `immune_escape`
clone never establishes in any trial. The real reason is arithmetic: `target_site_mutation` grows at
0.058/day and the swept potency 0.05 sits just below it, so after lomustine stops that one clone keeps
a small positive margin. Raising vaccine potency just past that growth rate (0.06) gives **flat 100%
at 10 years with no relapses of any kind** — the same threshold arithmetic as the cytostatic ceiling,
except an immune mechanism is *permitted* to cross it.

That antigen loss never fires is doing real work and rests on an unmeasured constant:
`IMMUNE_ESCAPE_SEEDING_RATE` is 6×10⁻⁵, ~200× below the drug-resistance total, and it only begins
seeding at day 90. A meaningfully higher antigen-loss rate would reintroduce the one leak the vaccine
cannot cover by construction, and nothing in this repo constrains it.

### The endurance numbers, with the vaccine on

Full grid, trametinib + duration-capped lomustine + vaccine, 300 trials per cell. Reported at both
`preexisting_prob = 0.30` (this module's central value) **and** `0.62` (what inverting the Skorupski
benchmark implies for the BMD context), because that parameter is unmeasurable and reporting one value
would hide the real uncertainty. Monte Carlo noise floor at n=300 is roughly ±5pp near 0.7, so
differences under ~5pp aren't meaningful.

**P(durable response), `preexisting_prob = 0.30`:**

| vaccine `max_kill` | 1 yr | 2 yr | 5 yr | 10 yr |
| --- | --- | --- | --- | --- |
| 0 (drugs only) | 0.867 | 0.687 | 0.700 | 0.710 |
| 0.03 | 1.000 | 0.877 | 0.727 | 0.723 |
| 0.05 | 1.000 | 1.000 | 0.990 | 0.967 |
| **0.06** | **1.000** | **1.000** | **1.000** | **1.000** |
| 0.08 | 1.000 | 1.000 | 1.000 | 1.000 |

**Same grid at `preexisting_prob = 0.62`:**

| vaccine `max_kill` | 1 yr | 2 yr | 5 yr | 10 yr |
| --- | --- | --- | --- | --- |
| 0 (drugs only) | 0.707 | 0.377 | 0.403 | 0.420 |
| 0.03 | 1.000 | 0.737 | 0.423 | 0.433 |
| 0.05 | 1.000 | 1.000 | 0.987 | 0.980 |
| **0.06** | **1.000** | **1.000** | **1.000** | **1.000** |

**The structural result is in the comparison between those two tables, not in either one.** At
10 years:

| vaccine `max_kill` | p=0.30 | p=0.62 | spread |
| --- | --- | --- | --- |
| 0 | 0.710 | 0.420 | **0.290** |
| 0.03 | 0.723 | 0.433 | **0.290** |
| 0.05 | 0.967 | 0.980 | −0.013 |
| 0.06 | 1.000 | 1.000 | **0.000** |

Below threshold the outcome swings by 29 points with `preexisting_prob` — it is essentially a readout
of the one parameter every sequencing assay was shown unable to measure. **At and above threshold that
dependence doesn't shrink, it disappears.** `vaccine_potency_threshold` computes why: 0.058/day is the
fastest vaccine-covered clone's growth rate (`target_site_mutation`), and a persistent, ceiling-free
mechanism exceeding it drives every covered clone to a permanently negative margin — so a pre-existing
subclone is suppressed indefinitely instead of eventually outgrowing.

That is worth being precise about, because it is a different *kind* of result than a better number:
crossing this threshold does not improve an estimate of an unmeasurable quantity, it removes the
model's dependence on it. No recalibration of `preexisting_prob` — in either direction, including the
pessimistic 0.62 — can do that.

**Two practical readings:**

- **The cytotoxic is nearly redundant above threshold.** Vaccine alone (no lomustine) at p=0.30 gives
  0.993 / 0.983 / 0.993 at 2/5/10 years for `max_kill` 0.05, and flat 1.000 at 0.06 — statistically
  indistinguishable from the with-lomustine column. Lomustine's value is concentrated at *sub*-threshold
  vaccine potency (at 0.03, 2-year: 0.877 with it vs 0.740 without). It buys insurance against an
  under-potent vaccine, not additive benefit against a good one.
- **Sub-threshold potency only delays.** At p=0.62 the pre-existing-subclone arm at `max_kill` 0.03
  runs 1.000 → 0.580 → 0.075 → 0.040 across 1/2/5/10 years — it collapses, just later. At 0.05 it holds
  at 0.967, at 0.06 flat 1.000. This is a threshold, not a gradient, and being close to it is not
  close to the benefit.

**What this does not fix.** Antigen loss stays outside the threshold by construction — no vaccine
potency covers a clone that shed the antigen. Its share of relapses never exceeds 3.3% anywhere in the
grid, but that is a consequence of `IMMUNE_ESCAPE_SEEDING_RATE = 6×10⁻⁵` being an unmeasured constant
~200× below the drug-resistance total. It is the one place where "just raise the potency" stops being
the answer, and nothing in this repo constrains it.

**So the honest form of the endurance case:** it rests on the vaccine, not on either drug; the number
that matters is not a durability percentage but whether vaccine potency clears ~0.058/day; and above
that line the result is robust to the model's least-measurable parameter in a way no drug arm was.
All of which sits on top of two unfitted inputs — `vaccine_max_kill` is a swept knob (no canine cancer
vaccine trial exists for this disease, so nothing here says 0.06 is reachable, which is exactly the
question `pharmacology.py` had to ask about CDK4/6i and got a "no" for) and the antigen-loss rate — and
on the oldest open premise in this repo: whether localized HS carries a PTPN11/KRAS hotspot at all.

## The answer: one this presentation, durable response

```bash
canine-dsp endurance-answer-demo --out results/unsequenced_breed-answer
```

Everything above was BMD-context or generic. This assembles all of it for the actual target: the
localized pulmonary presentation, in a single dog. Two code upgrades were needed first, both because the
localized pulmonary arm literally could not express the answer:

- **`run_monte_carlo_two_compartment` had no vaccine support** — so the localized pulmonary arm of
  `single-patient-demo` was trametinib monotherapy, repeating the exact omission corrected for BMD
  one section earlier. It now takes the same time-gated ramping vaccine plus
  `css_reference_2_duration_days`, applied **identically to both compartments**, and seeds immune
  escape per compartment. Vaccine-off defaults are byte-identical to before (asserted in tests).
- **`localized_pulmonary_scenarios` is 4-clone**, which cannot carry an immune-escape clone at all.
  `pulmonary_full_regimen_scenarios` is the 5-clone pulmonary equivalent of `vaccine_followon_scenarios`.

**Why the compartment structure matters here and doesn't break the answer:** Sakai et al. report
regional nodal involvement in many localized pulmonary cases, so "debulking reaches everything" is false. But
debulking is the *only* modality with a reach problem — the MEK inhibitor (full systemic exposure, no
brain-barrier discount in the lung), lomustine, and the vaccine all reach the node. Surgery misses the
compartment; the systemic mechanisms don't.

**10-year durable response, localized pulmonary, two-compartment, trametinib + duration-capped lomustine
+ vaccine** (columns = nodal involvement probability):

| vaccine `max_kill` | 0.0 | 0.2 | 0.4 | 0.6 |
| --- | --- | --- | --- | --- |
| *at `preexisting_prob` = 0.30* | | | | |
| 0 | 0.700 | 0.725 | 0.675 | 0.700 |
| 0.03 | 0.733 | 0.767 | 0.725 | 0.792 |
| 0.05 | 0.983 | 0.992 | 0.983 | 0.983 |
| **0.06** | **1.000** | **1.000** | **1.000** | **1.000** |
| *at `preexisting_prob` = 0.62* | | | | |
| 0 | 0.400 | 0.400 | 0.383 | 0.383 |
| 0.03 | 0.475 | 0.467 | 0.442 | 0.500 |
| 0.05 | 0.983 | 1.000 | 0.967 | 0.983 |
| **0.06** | **1.000** | **1.000** | **1.000** | **1.000** |

At threshold potency the result is flat 1.000 across **every** nodal-involvement rate, **both**
`preexisting_prob` values, and all four horizons (1/2/5/10 yr), with zero nodal relapses and zero
antigen-loss relapses. Sensitivity to `preexisting_prob` — the parameter no assay can measure — is
0.292 with the vaccine off and 0.000 above threshold.

### So: what's the answer?

**Conditionally yes, and the condition is unusually clean.** *If* this dog's tumor is sequenced and
carries a targetable MAPK hotspot, *and* a vaccine against that hotspot reaches ~0.06/day of kill,
*then* the model gives a durable response robust to everything else — including undebulkable nodal
disease and the pre-existing-resistance question that cannot be answered for this patient at all.
Below that potency the answer is no, and no amount of drug optimization substitutes.

What makes this a usable answer rather than a hedge is that the uncertainties partition cleanly for
**one** dog:

| Measurable in this dog | Not measurable in this dog |
| --- | --- |
| **Driver hotspot status** — clonal, ~25–50% VAF, far above every assay floor. *Never done in any this presentation.* | **Pre-existing resistant subclone** — ≤0.05% VAF, below every clinical assay; plus spatial sampling as a second wall |
| **Nodal involvement** — staging/imaging at diagnosis | **Vaccine potency in this dog** — no canine vaccine trial exists for this disease |
| **Burden and resectability** — imaging, surgical margins | **Antigen-loss rate** — unmeasured constant |

The useful asymmetry: **the presentation-specific risk (nodal disease) is resolvable for an individual
patient even though its cohort rate was never published, while the generic risk (subclonal resistance)
is unresolvable at any sequencing depth.** That's the opposite of how the population model treats
them — and above threshold, the unresolvable one stops mattering.

**The regimen the model supports**, in order: (1) resect/irradiate the primary — necessary but
worthless alone, both untreated arms regrow in ~150–200 days; (2) **sequence the specimen** — the
gate; (3) trametinib at full systemic exposure; (4) lomustine as an optional ~105-day bridge —
insurance against an under-potent vaccine, near-redundant above threshold; (5) the hotspot vaccine —
the only mechanism subject to neither the cytostatic ceiling nor a cumulative-dose cap while still
covering every drug-resistance route.

**The single point of failure, stated plainly.** Two unmeasured quantities carry the whole result, and
they are different in kind:

- The **driver hotspot** is measurable and simply has not been measured in any this presentation. That is a
  tissue-and-funding problem, resolvable by sequencing one tumor, and it gates everything downstream.
- **Vaccine potency** is not measurable in advance at all — and the analogous achievability question,
  asked of a CDK4/6 inhibitor by `pharmacology.py`, came back **no**. Nothing here establishes 0.06/day
  is reachable by a real canine vaccine. That is the load-bearing gap, and it is not the kind that more
  modeling can close.

So the defensible statement is: **this is a well-posed strategy with one clearly identified point of
failure and one clearly identified cheap first experiment — not a predicted outcome.** The first
experiment is to sequence a localized HS specimen. Against a real benchmark of 133-day median survival
(Sakai et al., 19 this presentations), the upside if both conditions hold is large; the probability that both hold
is unknown, and one of them has never been tested in any species for this antigen.

## Where this leaves things

`canine_dsp.mapk_resistance` (the generic Monte Carlo/branching-process engine) and
`canine_dsp.mapk_scenarios` (every illustrative breed/drug/disease-site preset, case-series
citation, and placeholder constant) are now deliberately separate modules, with
`canine_dsp.mapk_cli`'s demo functions consuming a scenario and producing CSV/plot/summary.json
output without needing to change when the scenario does. The point of that split: once real data
lands for this disease -- tumor sequencing, canine-specific drug PK, DLA genotyping, vaccine
immunogenicity, relapse-timing/ctDNA kinetics -- a new scenario module built from that data can
reuse every demo function and every line of the engine unchanged. Nothing here is an optimizer;
it's a consistent battery of analyses pointed at whichever scenario, real or illustrative, gets
handed to it.

What's actually anchored to real data, end to end: the sensitive clone's IC50 (canine HS cell
lines), the systemic reference plasma concentration and dose-limiting toxicities (a real Phase I
trial), the epitope-binding predictions (a live query to real prediction methods against real
characterized alleles), and the two comparators added this pass (lomustine response rates, the
human BRAF+MEK-inhibitor benchmark). Everything else -- every growth rate, resistance-clone potency
shift, kill ceiling, seeding rate, CDK4/6i potency, and vaccine parameter -- remains an illustrative
placeholder, swept across a range rather than asserted as a point estimate wherever the module
itself is the reason to doubt a single value. The load-bearing, unconfirmed premise underneath
every scenario is unchanged by any of this work: whether localized PIHS or localized pulmonary HS actually
carries a PTPN11/KRAS hotspot mutation at all. Nothing here can answer that; the actual canine
trametinib trial is running but hasn't reported results, and no shortcut to canine HS tumor
sequencing was found in a broad search for one. That is the single highest-leverage next step this
whole module points at, and the one piece no amount of modeling can substitute for.

## PI3K/mTOR-inhibitor resistance in canine hemangiosarcoma

A second, deliberately separate pipeline (`hsa_scenarios.py`/`hsa_cli.py`, reusing
`mapk_resistance.py`'s generic engine unchanged) for canine hemangiosarcoma (HSA) -- started by
running the same grounding-research discipline as the histiocytic-sarcoma module above, not by
assuming the same MEK-inhibitor-resistance story would transfer to a different disease.

HSA turned out to need a different framing than HS. Real, published somatic-mutation cohorts
(Megquier et al. 2019, Mol Cancer Res, whole-exome sequencing of 47 golden retriever HSA cases +
RNA-seq of 74 tumors, Broad/NHGRI Lindblad-Toh lab; Estabrooks et al. 2023, Vet Comp Oncol, PMID
37734854; Wong et al. 2017, PLOS ONE, PMID 29190660) find TP53 loss-of-function in up to ~66% of
cases, activating PIK3CA mutations (H1047R the dominant hotspot) in ~30-46%, PTEN loss-of-function
in 3-10%, and NRAS Q61 hotspot mutations (splenic-only, largely mutually exclusive with TP53) in
~7-24% -- heterogeneous and subtype-stratified, not one clean shared hotspot the way HS's
PTPN11/KRAS story is. The obvious first instinct -- build an NRAS-driven scenario mirroring HS's
MEK-inhibitor structure -- was checked against real data and dropped: a 508-dog real-world-evidence
cohort (Rodrigues et al. 2025, Sci Rep, PMID 40368987, PMC12078565, the FidoCure precision-medicine
platform) found trametinib conferred **no survival benefit** in NRAS-mutant HSA (241 vs. 259 days,
p=0.7775, n=71 vs. 26), despite real in vitro MEK-dependence data existing for NRAS-mutant HSA cell
lines. Building an optimistic hypothetical there would have contradicted a real result already in
hand -- exactly the mistake the histiocytic-sarcoma module's own "don't fabricate a this presentation locus"
discipline exists to avoid.

The PI3K/mTOR angle instead has three real anchors verified directly against source, not taken
from a summary: a real in vitro cellular potency measurement (Pyuen et al. 2018, PLOS ONE
13(7):e0200634, PMID 30011343 -- the dual PI3K/mTOR inhibitor VDC-597 gave IC50 0.23, 0.69, and
0.71 uM on three canine HSA cell lines, additive with doxorubicin); real canine PK/PD for the
clinically relevant drug in this class, rapamycin (Paoloni et al. 2010, PLOS ONE 5(6):e11013, PMID
20543980 -- a comparative-oncology dose-escalation study in dogs *with cancer*, not HSA
specifically, found trough concentrations exceeding 10 ng/mL at 0.06-0.08 mg/kg IM daily with
confirmed target inhibition and no MTD reached); and, in that same FidoCure cohort, a real HSA
survival benchmark: TP53-mutant dogs given rapamycin had a median survival of 193 vs. 118 days
without it (p<0.0001), and PIK3CA-mutant dogs 179 vs. 119 days (p=0.005).

```bash
canine-dsp hsa-resistance-demo --trials 300 --horizon-days 730 --out results/hsa-resistance
```

`dog_hsa_preset` anchors the sensitive clone's IC50 to VDC-597's real cell-line measurement, and
models three illustrative escape mechanisms chosen for general applicability to any mTORC1
inhibitor (loss of mTORC1-negative-feedback reactivating PI3K/AKT; parallel MAPK/ERK bypass;
on-target FKBP12-mTOR binding-site mutation) -- the same "chosen for general applicability, not
HSA-specific evidence" discipline the HS module uses for its own three mechanisms, since no
HSA-specific resistance data exists either. One problem surfaced and fixed before publishing this
preset, not after: naively pairing VDC-597's real IC50 (mean 543 nM) with rapamycin's real ~10.9 nM
trough would put achievable exposure roughly 50x *below* IC50 -- predicting the drug barely works
at all, directly contradicting the real, significant FidoCure survival benefit just cited for the
same drug. That's a more severe version of the cobimetinib/trametinib proxy-drug mismatch the
HS module documents (there, both numbers came from the *same* drug's own measurements, so pairing
them was internally consistent; here, no drug has both halves). Rather than publish a
self-contradictory model, `css_reference` is kept illustrative (5x the mean measured IC50, the
same "assumed, not measured, margin" convention `mapk_cli.CDK46_ILLUSTRATIVE_CSS_NM` already uses),
and rapamycin's real PK/PD and survival numbers are reported as separate real-world context to
sanity-check this scenario's *output* durability numbers against, not fed into its kill-rate math.

In testing (300 trials, 2-year horizon, `preexisting_prob` swept as the least-grounded input, same
as the HS module): durable-response probability ranged from 90% at `preexisting_prob=0.05` down to
31% at 0.70, with median time-to-progression among progressors 168-277 days across that sweep --
landing in a broadly plausible range next to the real standard-of-care benchmarks (splenectomy
alone: 48-day median survival, Wendelburg et al. 2015, JAVMA 247(4):393-403, PMID 26225611;
splenectomy+doxorubicin: ~120-180 days per a 2026 review's citation of Ogilvie et al. 1996, not
independently verified against that primary source) without being a fit to them -- the endpoints
aren't the same thing (this module's synthetic progression-from-nadir vs. real overall survival
mixing unstandardized concurrent treatments), so read this as "not absurd," not "validated."

### Cancer-vaccine follow-on

Checking "is there real vaccine work in HSA" directly turned up more than a first pass found, and
caught a real mistake in the process: an earlier draft of this section named a single vaccine,
"eVim," with numbers that turned out on closer inspection to belong to a *different*, unrelated
real trial. There are at least four real, distinct HSA vaccine programs, plus one still enrolling:

- **ERstrePs** (endoplasmic-reticulum-stress peptides from Salmonella-infected HSA cells) --
  the strongest real result: Marconato et al. 2023, Cancers (Basel) 15(17):4402, PMID 37686485;
  28 vaccinated dogs vs. 32 historical controls, median OS 276 vs. 175 days (**p=0.002**), 1-year
  survival 35.7% vs. 6.3%.
- **eVim** (extracellular vimentin, "iBoost" conjugate technology) -- a second, independent real
  trial, not the same one: Engbersen et al. 2025, Int J Mol Sci, PMID 41009669; 23 vs. 22 dogs,
  median OS 235 vs. 136 days (**not significant on its own**), but 1-year survival 44% vs. 14%
  (p=0.034) and a restricted-mean-survival advantage of 81 days at one year (p=0.02) both were.
- **Autologous whole-cell vaccine** -- real but far weaker evidence: Lucroy et al. 2020, BMC Vet
  Res 16:447, PMID 33208160; n=8, uncontrolled, metastatic (Stage III) dogs only.
- **Xenogeneic VEGFR-2 DNA vaccine** -- a real negative signal, included deliberately rather than
  omitted, the same discipline as the NRAS/trametinib result above: reliably raised antibodies in
  healthy dogs, but produced *no increase* in cytotoxic response against a real HSA cell line
  (Oncotarget, DOI 10.18632/oncotarget.7265, PMC4905448, 2016).
- **Calviri frameshift-peptide vaccine** -- real, currently enrolling (Wisconsin, Colorado State,
  UC Davis, as of late 2024), no results yet, the same "real trial running, no readout" situation
  as the canine trametinib-for-HS trial.

None of the four targets a driver-mutation neoantigen the way the HS module's mRNA-vaccine
hypothesis does -- a real, deliberate design choice by vaccine developers that independently
confirms this module's own earlier scoping decision (HSA has no single shared hotspot to build a
mutation-specific vaccine around). If anything, that makes the antigen-persistence argument more
secure here than for HS: none of the three modeled drug-resistance mechanisms has any documented
reason to alter vimentin expression, ER-stress signaling, or whole-tumor antigen presentation.

```bash
canine-dsp hsa-vaccine-followon-demo --trials 300 --horizon-days 730 --out results/hsa-vaccine
```

`hsa_vaccine_followon_scenarios` layers a vaccine kill term and the same antigen/MHC-I-loss 5th
clone onto the PI3K/mTOR resistance model, reusing `run_monte_carlo_with_vaccine` unchanged. In
testing (2-year horizon, 300 trials, at the recentered `preexisting_prob=0.70` -- see "Checking
the model's own outcome against the real eBAT trial" below for why): durable response was 32% at
vaccine off, climbing to 53% at `vaccine_max_kill=0.03`, then **100% at 0.05 and 0.08** -- the same
sharp-threshold shape found for histiocytic sarcoma's vaccine follow-on, and `immune_escape` never
appeared as the dominant mechanism at any potency tested. Read this the same way as every other
number in this pipeline:
the four real trials above establish that cancer vaccines have real, in some cases statistically
significant, benefit in canine HSA generally -- none of them were tested specifically with a
PI3K/mTOR inhibitor, none report outcomes by driver mutation, and `vaccine_max_kill` here is
swept, not fit to any of them.

**Can vaccine alone -- no inhibitor at all -- do the job?** Worth asking directly rather than
assuming the answer, and worth asking for a reason beyond curiosity: none of the four real HSA
vaccine trials this scenario is grounded in were actually combined with a PI3K/mTOR inhibitor --
they were tested with surgery +/- doxorubicin-based chemo, so vaccine-without-this-inhibitor is,
if anything, closer to how these vaccines have actually been used than vaccine-with-inhibitor is.
`hsa_vaccine_followon_scenarios`/`hsa_vaccine_followon_demo` now take `inhibitor_active=False`
(`--no-inhibitor` on the CLI) to isolate this directly, mirroring the same monotherapy-isolation
pattern eBAT already had.

```bash
canine-dsp hsa-vaccine-followon-demo --no-inhibitor --out results/hsa-vaccine-only
```

In testing: at low vaccine potency (`vaccine_max_kill<=0.03`) with no drug of any kind
suppressing the bulk tumor, durable response was **0%**, with a median time to progression of
just 5 days -- unsurprising, since nothing is holding the sensitive clone back before the vaccine
itself ramps up. But at `vaccine_max_kill>=0.05`, durable response jumps to **97-98%** -- nearly
matching the drug-combined case, on vaccine potency alone. It isn't quite as clean, though: unlike
the drug+vaccine combination (where `immune_escape` never appeared), vaccine-alone showed a small
but nonzero `immune_escape` fraction (1.7-2.7%) among the relapses that did occur. The likely
mechanism: without a drug knocking down the bulk sensitive-clone population first, tumor burden
stays higher for longer during the vaccine's ramp-up window, giving the antigen-loss escape
route (seeded from the antigen-positive population) more cell-days to arise from before the
vaccine's kill fully engages -- a real, mechanistically sensible reason drug+vaccine could be
more robust than vaccine alone, not just an assumption.

So: yes, in this model, a sufficiently potent vaccine can reach durable response on its own --
but "sufficiently potent" is doing real work in that sentence (the same illustrative,
unmeasured-for-any-real-vaccine potency threshold as everywhere else in this section), and it
comes with a small, real reason (the immune-escape route) to prefer pairing it with *something*
that suppresses bulk disease first, not necessarily this specific inhibitor.

### Searching combination space directly, not assuming a winner

The goal here was never "does the inhibitor work" or "does the vaccine work" in isolation --
it's finding *a combination that yields durable response*, which means not artificially
restricting the search to two ingredients once a third real option exists. **eBAT** (a
bispecific EGF/uPAR-targeted immunotoxin, mechanistically distinct from a small-molecule pathway
inhibitor) has real Phase I/II dose-finding data (Borgatti et al. 2017, Mol Cancer Ther 16(5):956-965,
PMID 28193671): a single IV cycle at 50 ug/kg, 6-month survival ~70% (n=17) vs. <40% historical,
6 long-term survivors past 450 days. Unlike VDC-597, no multi-dose-level response curve was
reported -- one active dose, not a titratable relationship -- so `ebat_max_kill` is swept across
an illustrative range, the same discipline `CDK46_MAX_KILL_SWEEP` uses for histiocytic sarcoma's
own real-but-unquantified second agent. EGFR/uPAR are broadly expressed on tumor vasculature and
aren't a documented target of any of this scenario's three drug-resistance mechanisms, so eBAT is
modeled the same mechanism-agnostic way CDK4/6i is modeled for HS.

```bash
canine-dsp hsa-combination-control-demo --out results/hsa-combination
canine-dsp hsa-combination-search-demo --out results/hsa-search
```

`hsa_combination_control_demo` compares inhibitor+eBAT against eBAT monotherapy (inhibitor
inactive), mirroring `combination_control_demo`'s side-by-side structure. `hsa_combination_search_demo`
goes further: a full grid over eBAT potency x vaccine potency (inhibitor always present), plus
the eBAT-monotherapy point, so "does the inhibitor even matter" is answered rather than assumed.

**Updated after a later fix -- this section originally claimed eBAT alone or inhibitor+eBAT alone
could each reach >=95% durable response without any vaccine at all. That claim depended on
modeling eBAT's exposure as constant for the entire simulated horizon, which was never realistic
(see "A real biological gap in the engine" further down this HSA section): the real drug was given
as a single treatment cycle, not sustained for years.** Corrected: `ebat_max_kill` alone,
at any potency tested (0.0 through 0.12), no longer moves this grid's durable-response probability
meaningfully above the inhibitor's own ~30-38% baseline -- once eBAT's kill pressure is capped to
a realistic, front-loaded window, its total contribution to a 730-day outcome is small regardless
of how potent it was assumed to be while active. The vaccine is the only lever in this grid that
reaches the >=95% threshold on its own: every eBAT potency level needs `vaccine_max_kill>=0.05` to
cross it, with or without eBAT alongside. There is no eBAT-alone or inhibitor+eBAT-alone route to
durable response left in this corrected grid -- the vaccine is doing essentially all of the work
this section originally credited to either eBAT or the inhibitor+eBAT pairing.

### Checking the model's own outcome against the real eBAT trial -- and recalibrating on it

Comparing this scenario's population-level output directly against the one real HSA efficacy
number available (eBAT's own trial, not a different drug's) turned up a real mismatch, not a
reassuring match: at this module's original default (`preexisting_prob=0.30`), inhibitor-alone
durable response (~66-73% at a 2-year horizon) was several times higher than the real trial's
1-year survival (26-29%, PMID 28193671) and its actual median survival (8.1-8.6 months). Two
things contribute, and only one is fixable by a parameter change:

- **A real, HSA-specific mechanism this model has no representation of at all.** Hemangiosarcoma's
  signature complication is tumor rupture and acute internal hemorrhage -- death independent of
  whether a resistant clone is regrowing. Histiocytic sarcoma kills more through progressive
  infiltration and mass effect, which a growth-threshold proxy approximates reasonably well; HSA's
  vascular/endothelial biology doesn't fit that proxy the same way. No parameter fixes a missing
  mechanism, and this module does not add one without a real rate to calibrate it to.
- **`preexisting_prob` was probably set too optimistically.** Sweeping it (as the module already
  did) shows durable response at `preexisting_prob=0.70` (the pessimistic end of the module's own
  range) drops to ~31% -- landing in the real trial's range. `_PREEXISTING_PROB_CENTRAL` is
  recentered to 0.70 on that basis. This is a loose analogy, not a same-drug calibration -- eBAT
  is mechanistically distinct from this scenario's modeled PI3K/mTOR inhibitor -- so treat it as
  "moved in the direction the one comparison available supports," not as validated.

Checked deeper into progression specifically (excluding survival's confound with rupture/other
extreme events) via the one real HSA disease-free-interval (DFI) number found -- Gardner et al.'s
toceranib trial, a *negative* result: median DFI 161 days with 81% of dogs developing metastatic
disease. This scenario's own time-to-progression (182-238 days across the eBAT sweep, before this
recentering) lands in the same range, but its progression *rate* (2-34% at any working potency)
doesn't -- and there is no real DFI number from a trial where the treatment actually worked to
check that specific mismatch against. That's a genuine data gap, not something this recentering
resolves.

```bash
canine-dsp hsa-resistance-demo --out results/hsa-resistance-v2
canine-dsp hsa-vaccine-followon-demo --out results/hsa-vaccine-v2
```

Rerunning after the recentering answers the actual question this section exists to ask: **does
adding another therapy still reach durable response once the baseline is corrected to be less
optimistic, or was the earlier "vaccine closes the gap" finding an artifact of an overoptimistic
baseline?** It wasn't. The inhibitor-alone baseline drops from ~68% to **32%** durable response at
`preexisting_prob=0.70` -- but adding vaccine still restores it to **100% at `vaccine_max_kill>=0.05`**,
the identical threshold found before recentering. Rerunning the full combination grid confirms the
same pattern holds throughout: the *baseline* got substantially worse, but the *thresholds* at
which each combination becomes sufficient didn't move. Mechanistically this makes sense --
`preexisting_prob` only changes how large a resistant population starts out, not whether a
sufficiently potent kill term eventually reverses its growth margin; a stronger baseline pessimism
mainly matters when nothing is added on top of the primary drug.

**Can vaccine alone -- no inhibitor -- do the job?** Worth testing directly, and worth asking for
a real reason: none of the four real HSA vaccine trials above were actually combined with a
PI3K/mTOR inhibitor (surgery +/- doxorubicin was the backbone in the ones that used one at all),
so vaccine-without-this-inhibitor is closer to how these vaccines have actually been used than
vaccine-with-inhibitor is. `hsa_vaccine_followon_scenarios`/`hsa_vaccine_followon_demo` take
`inhibitor_active=False` (`--no-inhibitor`) to isolate this, mirroring eBAT's existing monotherapy
flag.

```bash
canine-dsp hsa-vaccine-followon-demo --no-inhibitor --out results/hsa-vaccine-only
```

At low vaccine potency with no drug suppressing the bulk tumor at all, durable response was
**0%** (median time to progression 5 days) -- unsurprising, nothing is holding the sensitive clone
back before the vaccine ramps up. At `vaccine_max_kill>=0.05`, it jumps to **97-98%**, nearly
matching the drug-combined case. Not quite as clean, though: unlike drug+vaccine (where
`immune_escape` never appeared), vaccine-alone showed a small nonzero `immune_escape` fraction
(1.7-2.7%) among relapses -- plausibly because tumor burden stays higher for longer during the
vaccine's ramp-up window without a drug knocking down the bulk population first, giving the
antigen-loss escape route more cell-days to arise from. A real, mechanistic reason to prefer
pairing a vaccine with *something* that suppresses bulk disease first, not just an assumption
that combination is always better.

One important caveat surfaced by checking this claim more carefully, not by assuming it: only
one of the four real trials (Lucroy et al. 2020, the autologous whole-cell vaccine) actually
tested a vaccine with zero concurrent systemic therapy -- confirmed directly (dogs were
*excluded* if they received adjuvant chemotherapy). Its real result was unremarkable: median
survival 142 days, only 12.5% (1/8) alive at one year. But that trial also differs from this
scenario on two axes at once, not one -- **disease stage** (Stage III/metastatic, versus this
scenario's post-splenectomy adjuvant framing) and **vaccine mechanism** (whole-cell autologous,
not the genotype-agnostic antigen types like vimentin/ER-stress peptides this scenario's
antigen-persistence argument is built around). The trials that *do* match this scenario's disease
stage (ERstrePs, eVim) were never tested without a chemo backbone. There is no real trial that
matches this scenario on both axes simultaneously, so the honest position is that this specific
prediction (vaccine alone reaching 97-98%) is neither confirmed nor refuted by real data --
genuinely unknown, not validated and not contradicted.

### Grounding the mechanism in genomics and structure, not just (confounded) outcome data

The eBAT comparison above found a real gap between this scenario's output and a real trial's
outcome, and part of that gap turned out to be a missing mechanism (tumor rupture/hemorrhage) no
amount of outcome-data comparison could have identified on its own. That's a reason to check what
genomics and structure can answer *directly* -- independent of any clinical trial's confounds --
rather than lean only on outcome comparisons for everything.

**The driver mutation itself**: PIK3CA H1047R, checked with the same tool built for histiocytic
sarcoma's PTPN11/KRAS hotspots --

```bash
canine-dsp mapk-structure-compare --gene PIK3CA --hotspots 1047 --out results/pik3ca-compare
```

-- confirms the hotspot residue is identical between human and dog (H1047, both proteins 1068
aa): real, direct structural support that a PIK3CA-driven HSA subtype is chemically plausible in
dogs, independent of the somatic-mutation-frequency numbers cited earlier.

**The real drugs' molecular targets** needed a different tool, since none of eBAT's two targets
or eVim's antigen is a point-mutation neoepitope -- a single-hotspot comparison doesn't apply.
`alphafold.whole_sequence_identity` (new: overall ortholog conservation, not one residue) answers
"conserved enough to matter" for a whole-protein target instead:

```bash
canine-dsp hsa-receptor-conservation-demo --out results/hsa-receptors
```

Real results: **EGFR** (eBAT's first target) is 91.6% identical across 1154 aligned positions
(human P00533, dog A0A8D6L9C2) -- real structural support for why a human-EGF-ligand-based
immunotoxin could plausibly still engage canine EGFR. **PLAUR/uPAR** (eBAT's second target):
checked directly and found to have **no curated UniProt entry for dog at all** -- confirmed live
(a broader search than the exact gene symbol returns only an unrelated gene, LYPD3), not assumed
-- a real, unresolved data gap, not a negative finding. **VIM/vimentin** (eVim's antigen): 98.1%
identical (human P08670, dog A0A8C0N8E3, both 466 aa) -- but checking the actual paper directly
surfaced something more important than the number itself: eVim is a full-length recombinant
vimentin fusion protein designed to raise an **antibody** response, not a short peptide presented
on MHC-I to T cells. That makes IEDB/NetMHCpan-style MHC-binding prediction -- the tool built for
histiocytic sarcoma's driver-mutation neoantigen vaccine -- **the wrong tool for eVim entirely**;
applying it here would have been a category error, not a finding. No real B-cell/antibody-epitope
prediction tool was substituted for it at the time; the mismatch was reported rather than papered
over. The structural half of that gap -- not a full B-cell epitope predictor, but the piece
AlphaFold can actually contribute -- is addressed directly below.

### Replacing the vaccine's generic placeholder with a structure-based candidate antigen

AlphaFold predicts structure from a known sequence; it does not generate or invent new antigen
sequences the way a generative protein-design tool would. So "use AlphaFold to design a vaccine"
has to mean something narrower and checkable: for an antibody vaccine like eVim, only the parts
of the folded antigen actually exposed on its surface are reachable by a circulating antibody at
all -- a buried residue is a useless target no matter how promising it looks in the raw sequence.
That's a question AlphaFold's own output can answer, using structure this module had already
fetched (dog VIM, A0A8C0N8E3) but never analyzed past pLDDT and whole-sequence identity.

`alphafold.contact_number_burial` adds a CA-CA contact-number calculation: for each residue,
how many other residues' alpha-carbons fall within 10 A. A densely surrounded residue is packed
into the core; a sparsely surrounded one has open space on at least one side and is more likely
solvent-exposed. This is a coarse, honestly-labeled proxy for true solvent-accessible surface
area (SASA), not a replacement for it -- a real Shrake-Rupley SASA calculation needs every atom's
coordinates, and this module's mmCIF parser reads alpha-carbons only. `alphafold.
find_exposed_linear_epitopes` then slides a window across the sequence and ranks the least-packed,
non-overlapping stretches -- contiguous exposed loops, the shape a real linear B-cell epitope
needs, not isolated exposed points.

```bash
canine-dsp hsa-vaccine-antigen-design-demo --out results/hsa-antigen-design
```

Run against dog VIM: the three top candidates are residues **1-9** (`MSTRSVSSS`), **20-28**
(`TGSRPSSTR`), and **418-426** (`FSSLNLRET`) of 466 -- vimentin's N-terminal head and C-terminal
tail domains, not anywhere in its long central body. That's independently corroborated by a
second, unrelated signal: AlphaFold's own per-residue confidence (pLDDT) drops sharply in exactly
these same regions (down to 30-50, versus 90-99 through the central coiled-coil rod) --
AlphaFold's confidence collapses in genuinely disordered regions, and intrinsically disordered
regions are, independently, the regions a folded structure leaves solvent-exposed. Two different
computations (contact number from coordinates, confidence from the prediction itself) landing on
the same three stretches is a real consistency check, not a single tool agreeing with itself.
Cross-referencing conservation: residues 1-9 and 418-426 are 100% identical to human VIM, and
20-28 is 77.8% identical -- so a human-vaccine-derived epitope from either terminal domain would
plausibly transfer to dogs, and vice versa.

What this does *not* do, stated as directly as the finding itself: it does not produce a
`vaccine_max_kill` value or feed anything into the Monte Carlo model. No structural tool predicts
immunogenicity, antibody titer, or in vivo tumor-clearing efficacy from a folded structure alone
-- solvent exposure is necessary but nowhere near sufficient for a good antibody target, and this
ranks candidates within one structure, unvalidated against any real epitope-mapping experiment for
VIM. `vaccine_max_kill` remains exactly as illustrative and swept as before this analysis, for any
vaccine construct, real or hypothetical. What changed is narrower and real: "eVim's antigen: some
generic antibody target" is now "eVim's antigen has two independently-corroborated, actually-
exposed, human-conserved candidate epitope regions, structurally identifiable rather than assumed."

### A real biological gap in the engine, found by asking why the results were this poor

Everything through the last two sections rested on one simplification that had gone unquestioned:
`css_reference_2` (the second drug's exposure) was held *constant for the entire simulated
horizon* -- years, in the durability-horizon runs -- exactly like the continuously-dosed,
oral-pill inhibitor. Real eBAT was never dosed that way. The pivotal trial gave it as a single IV
cycle (three doses on alternating days) before starting chemotherapy, not ongoing maintenance
(Borgatti et al. 2017); its own toxicity profile paper also documents real neutralizing anti-toxin
antibodies developing in ~30% of dogs despite deliberate deimmunization -- a real immunological
ceiling on how many cycles can ever be given, unlike a small molecule dosed daily indefinitely. No
eBAT-specific pharmacokinetic half-life was found in a search for one, but modeling years of
sustained kill pressure from a single treatment cycle was never defensible regardless of the exact
number.

`mapk_resistance.run_monte_carlo`/`run_monte_carlo_with_vaccine` now accept
`css_reference_2_duration_days`: after that many days, the second drug's concentration drops to
zero instead of persisting for the rest of the horizon. `None` (the default for every *other*
caller, including every HS scenario, where the second drug is a small-molecule CDK4/6 inhibitor
that genuinely could be dosed chronically) preserves the original always-on behavior exactly --
this is a targeted, backward-compatible fix, not a change to HS's own results. HSA's eBAT-using
demos now default to `HSA_EBAT_EXPOSURE_DURATION_DAYS = 28` -- a generous, explicitly illustrative
upper bound (one dosing cycle plus a plausible tail for cellular kill to play out), not a fitted
or measured clearance time.

```bash
canine-dsp hsa-durability-horizon-demo --ebat-max-kill 0.05 --vaccine-max-kill 0.0 --out results/hsa-durability-inhib-ebat
canine-dsp hsa-durability-horizon-demo --ebat-max-kill 0.05 --vaccine-max-kill 0.0 --no-inhibitor --out results/hsa-durability-ebat-alone
canine-dsp hsa-combination-toxicity-demo --ebat-max-kill 0.05 --out results/hsa-toxicity
```

This resolves both open threads from the last two sections at once, and reverses one of them:

| Regimen | 1yr | 2yr | 5yr | 10yr |
|---|---|---|---|---|
| Inhibitor alone (unaffected by this fix -- unchanged) | 34.7% | 32.3% | 29.7% | **30.0%** |
| eBAT alone, no inhibitor, potency 0.02 | 0% | 0% | 0% | **0%** |
| eBAT alone, no inhibitor, potency 0.05 | 0% | 0% | 0% | **0%** |
| Inhibitor + eBAT, potency 0.02 | 40.7% | 32.0% | 30.0% | **28.7%** |
| Inhibitor + eBAT, potency 0.05 | 43.3% | 30.7% | 30.7% | **29.0%** |
| Inhibitor + eBAT, potency 0.08 | 46.0% | 31.3% | 31.3% | **30.7%** |

**First, the cliff-side ambiguity from the previous section is gone.** eBAT alone now gives 0%
durable response at *every* potency tested, not just the pessimistic side of an arbitrary
threshold -- with nothing else suppressing the tumor once its 28-day window closes, a transient
pulse cannot hold off regrowth indefinitely, however potent it was while active. This is a more
biologically sensible result than either side of the old cliff, and it matches the real trial's
own design: eBAT was never given as monotherapy with no other treatment, which this result now
explains rather than merely accommodates.

**Second, and this reverses the previous section's headline finding: adding the inhibitor is not
a net liability.** Inhibitor+eBAT now converges to essentially the *same* ~29-31% at 10 years
regardless of which eBAT potency is assumed (0.02 through 0.08) -- indistinguishable from the
inhibitor-alone baseline (30.0%) within Monte Carlo noise. eBAT still buys a real, modest early
bump (32.3% -> 40-46% at 1 year, since it's doing something for its first 28 days), but that
bump fades once its exposure ends, and by 10 years the inhibitor's own ceiling is what actually
determines long-horizon durability -- not whichever potency eBAT was assumed to have. The earlier
finding that inhibitor-specific resistance routes (`pi3k_akt_feedback_reactivation`,
`target_site_mutation`) made the combination *worse* than eBAT alone was real given the model's
prior assumptions, but those assumptions -- eBAT sustaining kill pressure for a decade -- were
themselves the artifact. Once fixed, eBAT alone can no longer sustain anything at all (0% at every
horizon), so there is no "worse than eBAT alone" left to be worse than.

**The toxicity de-rating picture flattens for the same reason.** Re-run with the front-loaded
window: durable response is **30.3% at full dose, 30.3% at 80%, 29.3% at 60%, 29.3% at 40%** --
essentially flat, because eBAT's total contribution is now capped to a brief window regardless of
concentration, so de-rating its dose barely moves the long-horizon outcome one way or the other.
The inhibitor's own de-rating is what would matter most now, not eBAT's -- a genuinely different,
and more defensible, picture than the substantial 97.3%->65.3% erosion shown before this fix.

One combination-space result is worth flagging rather than silently updating: eBAT(0.02)+vaccine
(0.03) with no inhibitor now shows 0% durable response at every horizon, down from ~89% before
this fix. Checked directly (not assumed): this isn't a new interaction effect -- `eBAT` at potency
0.02 was already shown incapable of controlling tumor growth *at all*, even during its own active
window (median burden actually *increases* from day 0, since its kill rate doesn't exceed the
sensitive clone's own growth rate). Pairing an already-inadequate eBAT dose with a vaccine that
doesn't start suppressing anything until day 30 doesn't change that. Consistent with, not
contradicting, what potency 0.02 was already shown to do alone.

**Does HS have fewer escape mechanisms than HSA -- is that why HS's combination could reach a
clean mechanistic elimination while HSA's picture stayed this murky?** Checked directly with
`clone_growth_margins` (the same deterministic tool used for HS) rather than assumed: no. Both
scenarios model exactly three non-sensitive resistance clones, and at matched potency the margins
are nearly identical in structure and magnitude:

| | HS, `max_kill_2=0.05` | HSA, `ebat_max_kill=0.05` |
|---|---|---|
| Route 1 (feedback/pathway reactivation) | +0.0040/day | +0.0031/day |
| Route 2 (parallel-pathway/receptor bypass) | -0.0102/day (already negative) | -0.0229/day (already negative) |
| Route 3 (target-site mutation) | +0.0121/day | +0.0056/day |
| At `max_kill=0.08`: all three routes | negative | negative |

Both diseases show the identical qualitative pattern -- one route already suppressed at the
lower potency, two barely positive, all three flipping negative at a meaningfully higher potency
-- because HSA's illustrative growth/kill parameters were deliberately built reusing HS's own
shared conventions, not because either disease's biology is intrinsically easier or harder. The
real differences driving the very different-looking outcomes are elsewhere: HSA's
`preexisting_prob` was recentered to a far more pessimistic value (0.70 vs. HS's 0.30) against
real eBAT survival data; HSA's primary drug exposure is an illustrative margin rather than a
canine-PK-anchored real dose the way HS's trametinib is; and, until this section, HSA's second
drug was modeled as chronically dosed when the real drug never was -- a difference in how each
scenario was built and calibrated, not in how many ways either tumor can escape its treatment.

### Does this change whether a durable-response combination exists for HSA?

None of the three genomics/structure findings above were fed into the Monte Carlo model as a
parameter -- they're an independent plausibility check, not a calibration input -- so they don't
change the combination-search grid's own numbers (which have since been corrected for a separate
reason -- eBAT's exposure duration, see above -- and now show the vaccine as the only route to
>=95% durable response in that grid; eBAT no longer contributes enough on its own to matter).
What changed here is how much weight each piece of that finding can actually bear, and the answer
is uneven across the two "extra" ingredients:

- **eBAT is better grounded now than before, on two independent axes.** Its first target, EGFR,
  is structurally conserved enough in dogs (91.6% identical) that a human-EGF-ligand-based
  immunotoxin engaging it is plausible, not just asserted from the trial having worked. That sits
  on top of eBAT already being the one drug in this module with real trial outcome data at all
  (Borgatti et al. 2017) -- two different kinds of evidence, structural and clinical, both
  pointing the same direction.
- **eBAT's second target, uPAR, is not similarly grounded, and can't be with the tools used here.**
  No curated dog PLAUR entry exists to check -- a real gap in the evidence, not a negative result.
  eBAT's real-world efficacy signal doesn't depend on this check succeeding (the trial data stands
  on its own), but half of its stated dual-target mechanism remains unconfirmed at the sequence
  level, and the same trial data needed `preexisting_prob` recentered to 0.70 (an admittedly loose
  analogy) before this module's own output even landed in the trial's neighborhood -- so "eBAT
  works" rests on outcome data with its own acknowledged looseness, not on a clean structural story.
- **The vaccine half of the combination search turns out to be more of a generic placeholder than
  it looked.** `immune_escape` in this module represents MHC-I/antigen-presentation loss -- the
  right resistance mechanism for a T-cell peptide vaccine, which is exactly how histiocytic
  sarcoma's vaccine is modeled and checked (IEDB/NetMHCpan against a real neoantigen). But the one
  real HSA vaccine with both a statistically significant efficacy signal and a fully verified
  mechanism, eVim, is antibody-based -- its actual escape routes would be antigen shedding,
  extracellular-epitope mutation, or surface-vimentin downregulation, not MHC-I loss. So unlike
  HS, where the mechanism-matched check was run and came back unsupported for one specific case
  (KRAS Q61H), here the vaccine resistance mechanism itself was never mechanism-matched to the
  strongest real candidate in the first place. `vaccine_max_kill` remains a swept, unfitted
  potency knob standing in for "some vaccine, some mechanism" -- not eVim, not ERstrePs (whose
  antigen composition couldn't even be pinned down earlier), and the >=95% thresholds found above
  should be read that way: a property of the model's generic vaccine term, not a projection for
  any specific real vaccine's actual behavior. The antigen-design work above narrows one part of
  this gap -- eVim's antigen now has identified, structurally-exposed, human-conserved candidate
  epitopes instead of being an unexamined black box -- but it doesn't touch the resistance-
  mechanism mismatch at all: `immune_escape` is still MHC-I-loss, still the wrong escape route for
  an antibody vaccine, regardless of which epitope on VIM is targeted. Knowing *where* on the
  antigen a real vaccine could bind says nothing about *how* a real HSA tumor would evade it.

Net: the model still finds parameter regions that reach the durable-response threshold, and that
hasn't changed. What genomics and structure did was sharpen *which* piece of that finding is solid
versus illustrative rather than answer the underlying question -- eBAT/EGFR engagement is now
backed by both structure and outcome data; eVim's antigen now has real candidate epitopes instead
of an unexamined placeholder; eBAT/uPAR and the vaccine's resistance-mechanism mismatch remain
open, now-named gaps rather than diffuse uncertainty. That's a real improvement in honesty about
what's known, not a new answer to "is there a real combination": neither confirmed, nor refuted,
just a more precisely located hole than before this pass. The HS module's own "does the durable-
response finding hold up" check (above) reached a related but distinct honest conclusion from a
different angle: not a new gap in the mechanism, but a caught mistake in how a real comparator was
used -- a reminder that "we checked against real data" is not automatically rigorous just because
the data is real; the comparison itself has to actually match on the axes that matter.

## Research path

1. Pin an assembly and record accessions/checksums in `data/README.md`.
2. Start with matched regions, then build chromosome-level GC and variant-density tracks.
3. Test peaks against GC-, length-, and mappability-matched null sequences.
4. Use breed-aware train/test splits and permutation tests; never split related animals randomly.
5. Validate candidates against annotations and an independent cohort.

## Layout

`src/canine_dsp/` contains signal encoding, spectral estimators, wavelets, I/O, AlphaFold structure
parsing, UniProt accession resolution, and the CLI. The MAPK-inhibitor resistance work is split
three ways: `mapk_resistance.py` (the generic Monte Carlo/branching-process engine), `mapk_scenarios.py`
(illustrative breed/drug/disease-site presets and case-series citations), and `mapk_cli.py` (demo
functions that consume a scenario and produce CSV/plot/summary.json output); `dla_binding.py` is
the real IEDB MHC-I epitope-binding client. `hsa_scenarios.py`/`hsa_cli.py` follow the same
scenarios/demo split for canine hemangiosarcoma, reusing `mapk_resistance.py`'s engine directly
rather than duplicating it. Two modules exist to check the resistance model against constraints it
cannot see from inside itself: `pharmacology.py` converts real in vitro/PK observables into the
engine's `max_kill_2`/`ic50_nM_2` parameters, so "is this potency achievable" becomes a question
about named, individually-checkable inputs (cytostatic ceiling, Emax/Hill saturation,
cumulative-dose duration caps) rather than an unexaminable constant; `single_patient.py` reframes the
population Monte Carlo as an N=1 problem, quantifying what tumor sequencing can and cannot resolve
(assay detection floors, spatial sampling, driver conditioning) and splitting an existing ensemble
into the patient types its cohort average hides; `mutational_supply.py` scales the engine's two
mutation-supply parameters (`seeding_rates`, `preexisting_prob`) by a tumor-mutational-burden ratio,
turning "a low-burden tumor should endure better" from a stated intuition into a swept, checkable
transformation with the real canine TMB data attached; `antigen_convergence.py` formalizes why every
drug-resistance route in the model retains the vaccine's target antigen, verifies that claim against
the engine's own kill mask rather than asserting it, and computes the cytotoxic-to-immune handoff
timing. Each pairs with a `*_cli.py` demo module following the same split. `tests/` contains deterministic unit tests. `data/` stores only provenance documentation
in Git.
