# Stochastic Volterra immunotherapy model

## Scope

This workflow is a synthetic methods benchmark. It demonstrates how a second-order Volterra
treatment operator can drive a partially observed stochastic tumor–immune system. It is not fitted
to patient outcomes and cannot recommend a drug, dose, sequence, or treatment change.

## Model layers

1. **Exposure and treatment operator.** Normalized administrations pass through reduced plasma PK,
   tumor equilibration, and saturable target engagement before entering a multi-input, multi-output
   Volterra model. First-order kernels encode delayed individual effects; second-order cross-kernels
   encode a bounded residual schedule-dependent interaction.
2. **Patient and kernel uncertainty.** Growth, killing, switching, and response gains vary across
   Monte Carlo draws using log-normal random effects.
3. **Immune process.** Cytotoxic activity, exhaustion, and inflammation receive correlated
   multiplicative innovations around the Volterra response.
4. **Tumor evolution.** Sensitive and weakly immune-visible populations undergo stochastic
   tau-leap birth, death, and phenotype-switching events. An effective population size maps the
   normalized state into integer events; it is a dispersion parameter, not a tumor cell count.
5. **Observation process.** Imaging is log-normal, ctDNA alternate counts are binomial conditional
   on modeled escape fraction, and RNA module counts are negative binomial.
6. **Filtering.** A bootstrap particle filter updates tumor-burden, escape-state, parameter, and
   immune-response distributions from imaging, ctDNA, and RNA-module measurements.
7. **Inverse control.** Differential evolution uses common random numbers and penalizes the 90%
   conditional-value-at-risk (CVaR) of terminal burden, median burden, residual escape composition,
   inflammation-bound violations, and total normalized dose. Per-dose, cumulative-dose, plasma-Cmax,
   and tumor-AUC bounds provide additional protocol constraints.

The uncertainty ensemble is specified rather than learned from a posterior distribution in the
synthetic demonstration. “Filtered” intervals are particle approximations to latent-state
distributions conditional on observations; unconditioned ensemble intervals are simply predictive,
not posterior-predictive.

## Identifiability and validation

These layers must be introduced incrementally in real work. Observation dispersion can otherwise be
confounded with biological process variation, and random effects can be confounded with kernel
heterogeneity. Kernel memory/order, random-effect distributions, process noise, transition rates,
assay likelihoods, clinical thresholds, and objective weights must be selected without consulting
the final test cohort.

A credible validation sequence is subject-level temporal validation, untouched-patient validation,
external-cohort validation, posterior-predictive checking by modality, calibration of response and
toxicity probabilities, and prospective silent evaluation. Decision-curve analysis should precede
any interventional evaluation.

## Clinical interpretation

- Response probability is conditional on the specified model, threshold, horizon, and input bounds;
  it is not an objective response rate.
- Escape probability is a latent evolutionary-risk estimate; it is not proof of an antigen-loss
  mutation or resistant clone.
- Inflammation exceedance is a biomarker-model event; it is not a CTCAE toxicity prediction.
- Predictive and filtered intervals omit structural uncertainty unless competing models are included.
- A schedule is a hypothesis for protocol-level evaluation, never an individual prescription.
