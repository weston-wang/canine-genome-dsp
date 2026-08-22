# Treatment-policy superiority benchmark

## Question this code can answer

The benchmark can determine whether a locked QSP–Volterra schedule has a reproducible advantage
over prespecified computational comparators inside untouched synthetic model worlds. It cannot
determine whether that schedule is superior to clinical standard of care.

The built-in primary comparator is a reduced PK/PD virtual-population risk optimizer with the
second-order Volterra residual removed. A fixed-protocol proxy is a secondary comparator. Neither is
a disease-, biomarker-, treatment-line-, or jurisdiction-specific clinical standard. A Volterra
policy optimized without the PK layer is included as an ablation.

## Upgraded architecture

Administered inputs pass through one-compartment plasma exposure, tumor equilibration, and saturable
target engagement. Those exposure histories drive a mechanistic tumor–immune baseline plus a
zero-centered second-order Volterra interaction residual. Stochastic virtual patients add biological
random effects, immune-process innovations, birth/death/escape events, and assay-specific
observations. A particle filter updates latent state distributions, while the policy optimizer
emphasizes terminal-burden CVaR and applies per-dose, cumulative-dose, plasma-Cmax, tumor-AUC,
escape, and inflammation constraints.

This is deliberately described as **reduced PK/PD-QSP**, not a drug-specific full QSP platform.
Vaccine, antibody, and radiation require different real pharmacological models. PK must be calibrated
against concentration or occupancy measurements before fitting Volterra memory; otherwise PK delay
and kernel delay are confounded. The Volterra term must remain a bounded residual to avoid
double-counting nonlinear synergy already represented mechanistically.

## Locked evaluation

The command writes a hashed analysis plan and hashed policies before reporting results. Policies are
optimized only on the nominal development system and evaluated with common random numbers across
untouched shifts in growth, killing, escape, PK, response gain, and interaction strength. Two
structural stress tests remove all second-order synergy.

Simulation superiority requires every gate:

1. The lower scenario-clustered bootstrap bound for relative composite-utility improvement exceeds
   a prespecified 5% meaningful margin.
2. Terminal burden is noninferior within 10%.
3. Upper confidence bounds for escape-dominance and inflammation-exceedance differences remain
   within 5% margins.
4. The candidate wins at least 75% of untouched shifts.
5. Both optimizers converge and every protocol/exposure constraint is satisfied.

The result is labeled `IN_SILICO_ADVANTAGE` only if all gates pass. Clinical status remains
`NOT_EVALUABLE_NO_DISEASE_SPECIFIC_SOC_OR_PROSPECTIVE_TRIAL` for every synthetic result.

A candidate disease-specific protocol can be supplied with `--reference-schedule schedule.csv`.
The CSV must contain `day,vaccine,checkpoint,radiation`; its normalized inputs are checked against
the same protocol/exposure constraints and its content hash is included in the locked plan. This
still evaluates the schedule only inside synthetic challenge worlds—it does not turn it into a
clinical comparison.

## Evidence required for a clinical claim

A real comparison needs a prespecified population, disease stage, biomarker stratum, treatment line,
drug/route/dose units, clinical standard comparator, estimand, intercurrent-event strategy, outcome
horizon, clinically meaningful margin, and serious-toxicity margin. The model and statistical plan
must be locked before site-, trial-, and time-separated external validation.

Observational policy evaluation additionally requires a target-trial specification, action-support
and positivity diagnostics, cross-fitted behavior propensities, effective sample size, and agreement
among sequential doubly robust, weighted, and model-based estimators. Poor overlap, failed
calibration, or estimator disagreement must cause abstention. A silent prospective evaluation should
precede a randomized policy-versus-standard-care trial.

The `evaluate-logged-policy` command implements the computational part of that fail-closed check for
a longitudinal table containing `patient,step,reward,behavior_probability,target_probability,`
`q_logged,v_next,v_initial`. Nuisance quantities must be generated out of fold and declared with
`--cross-fitted`. The command triangulates per-decision importance sampling, self-normalized
importance sampling, and sequential doubly robust estimates; reports overlap, effective sample size,
extreme weights, estimator disagreement, and a patient-bootstrap interval; and abstains when a
diagnostic fails. It does not solve unmeasured confounding or replace target-trial design.

Relevant standards and reporting guidance include [ICH M15](https://www.fda.gov/media/184747/download),
[ICH E9(R1)](https://www.ema.europa.eu/en/ich-e9-statistical-principles-clinical-trials-scientific-guideline),
[TRIPOD+AI](https://www.bmj.com/content/385/bmj-2023-078378),
[PROBAST+AI](https://www.bmj.com/content/388/bmj-2024-082505),
[DECIDE-AI](https://www.nature.com/articles/s41591-022-01772-9), and
[CONSORT-AI](https://www.nature.com/articles/s41591-020-1034-x).
