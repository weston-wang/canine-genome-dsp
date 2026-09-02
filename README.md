# canine-genome-dsp

Analysis of a durable-therapy strategy for **primary intracranial histiocytic sarcoma (HS)** in a
predisposed dog breed. The repository has two layers:

1. **Conversation-sourced reference modules** — clean, self-contained summaries distilled from the
   research conversation (pure standard library).
2. **The scientific / computational models** — the DSP, genomics, structure, and pharmacology models,
   plus the quantitative therapy engine, that actually compute the analysis.

> **This is an analysis, not veterinary advice.**

## Scope — a specific presentation, not histiocytic sarcoma in general

This repository targets **one specific disease presentation**, not HS broadly. The breed name is
deliberately omitted, but the distinguishing clinical and genomic fingerprint is tracked in full (in
`presentation.py`, `disease.py`, and the report) so future work does **not** collapse into "solve HS
generally." The presentation being solved is:

- **Primary intracranial HS (PIHS)** in a strongly predisposed breed — the breed accounts for ~47% of
  subdural HS cases and ~50% of PIHS cases in the case series.
- **Extra-axial / meningeal-surface** tumours, cerebrum-predominant (temporal/frontal), typically
  **confined to the CNS** at diagnosis yet locally invasive (parenchymal invasion in 23/23 dogs),
  with leptomeningeal/CSF involvement (~52% CSF-positive). A discrete resectable lump is ruled out.
- A **co-equal lung / disseminated** form carrying the same lesion.
- A **germline predisposition** — the recurrent **MTAP/CDKN2A** deletion — plus the somatic
  **MAPK** driver majority (PTPN11/SHP2 ~56%, KRAS ~3%), with TP53/RB1/PTEN in minorities.

If you revisit this repo, start from `presentation.py`: it is the pinned definition of *which* HS this
work is about.

## Layout

```
src/canine_dsp/
  # --- reference modules (pure stdlib, conversation-sourced) ---
  therapies.py        every therapy and drug discussed, grouped by class, with per-agent status
  disease.py          the disease: sites, escape routes, mechanisms, and delivery routes
  presentation.py     what is distinctive about this breed's HS, biologically and genomically

  # --- scientific / DSP / genomics models ---
  alphafold.py        AlphaFold structure integration for canine drug-target orthologs
  uniprot.py          UniProt sequence/accession resolution
  sequence_conservation.py  human-vs-dog ortholog identity (ERK2 100% / PI3Kα 99.81% / P-gp 91%),
                      computed from real UniProt sequences and reproducible (not asserted)
  coverage_assessment.py    evidence grade for every escape closure — how much of "covers all
                      escapes" is measured vs transferred vs model-derived vs structural
  pkpd.py             Emax PK/PD model: DERIVES a per-day kill rate from a measured IC50 + achievable
                      exposure (returns a non-closing rate when the drug can't reach its IC50)
  maintenance_durability.py  derives 10-year durability per genotype and per site from the pkpd kill
                      rate + branching-process extinction + genotype-lock + reach — durable only for
                      the MTAP lock, surveillance-dependent for the MAPK majority, no number for CSF
  dla_binding.py      canine MHC (DLA) peptide-binding prediction
  pharmacology.py     PK/PD pharmacology model
  mutational_supply.py  mutational-supply modelling
  structural_invariance.py  structural-invariance analysis
  volterra.py         Volterra-series nonlinear system modelling
  spectral.py / wavelets.py / signals.py  DSP: spectral, wavelet and signal analysis of genome tracks
  hybrid_rnn.py       hybrid RNN model
  evolution.py / expression.py  evolutionary modelling, gene expression
  mapk_resistance.py / mapk_scenarios.py / single_patient.py  MAPK resistance dynamics and scenarios
  *_cli.py            standalone command-line front-ends for the models above
  io.py / control.py  shared I/O and control helpers

  # --- quantitative therapy engine ---
  core/               regimen, toxicity, dormancy, combination search, evidence typing,
                      genotype-tiered durability, delivery, schedule coherence, and the
                      site/escape catalogue that produce the report's numbers
  v2/ , v3/           later simulation engines and their retraction-encoding modules
  validation/         external back-tests (e.g. the lomustine comparator)

docs/
  CONSOLIDATED_REPORT.md   the plain-language report, consolidated from the published artifacts
tests/                     ~960 tests across the reference modules, scientific models, and engine
```

## The reference modules

- **`therapies`** — every therapy/drug raised, grouped by therapeutic class, each with a mechanism,
  a verdict bucket (including retracted/superseded/demoted) and faithful status text.
- **`disease`** — the anatomical sites, the escape routes a therapy must close, the mechanisms, and
  the delivery routes. Faithful to the conclusions reached, including retractions.
- **`presentation`** — what makes this breed's HS distinctive, genomically and clinically.
  Breed-neutral by design.

## The scientific models and engine

The `alphafold`-family modules and the `core/` engine are the computational substrate behind the
analysis: structure and sequence models for canine drug targets, DSP of genome tracks, pharmacology
and mutational-supply models, and the regimen/toxicity/durability engine that the consolidated report
draws its figures from. Each scientific model has a standalone `*_cli.py` front-end.

## The report

`docs/CONSOLIDATED_REPORT.md` merges the three published report artifacts into one document: the
two-move induction-plus-genotype-matched-maintenance strategy, the escape-coverage results, the
genotype-tiered maintenance table, the retractions, and the single test that would falsify the
headline.

## Running the tests

```
pip install -e ".[dev]"
pytest
```
