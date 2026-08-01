# Hybrid evolutionary–Volterra vaccine model

This is a research scaffold for testing whether longitudinal vaccine and immune measurements can
support evolutionary steering. It is not a clinical decision system.

## State and operator

The latent state contains clone abundances. Each clone has an intrinsic growth rate, antigen
expression, presentation efficiency, and transition probabilities into modeled descendant states.
Density-dependent growth, immune killing, and mutation/phenotypic transition are simulated in
`evolution.py`.

Treatment is a multichannel schedule: individual vaccine antigens, checkpoint inhibitors, or other
therapies may each be a channel. First- and second-order causal kernels map treatment history into
antigen-specific immune pressure. The first-order kernel describes response and decay; the quadratic
kernel describes saturation, priming, synergy, or antagonism.

## Inverse problem

`control.py` chooses bounded doses at allowed administration times. Its objective penalizes terminal
and peak tumor burden, terminal escape-clone fraction, and dose. The implementation minimizes the
worst objective across perturbed model scenarios, making uncertainty explicit.

The included optimizer is a benchmark, not a dosing recommendation. A translational implementation
would require pharmacokinetic constraints, toxicity models, censoring/dropout models, posterior state
estimation, prospective protocol constraints, and independent validation.

## Identifiability

Estimating second-order kernels requires variation in antigen composition, dose, and timing. Many
published vaccine cohorts are too small or homogeneous for this. Cells are not independent patients;
cross-validation and bootstrap resampling must operate at the patient or dog level. A fixed Volterra
operator is only locally valid because antigen/MHC loss can change the system itself. Intended use is
receding-horizon estimation and re-optimization after new ctDNA, RNA, TCR, or imaging observations.

## Comparative design

The registry includes dog and human expression and vaccine studies. Comparative analyses should use
one-to-one orthologs, conserved pathway modules, and species-specific MHC features. Do not directly
pool raw expression counts across species or platforms. Estimate within-study effects first, then
compare effect directions or hierarchical module-level parameters.

