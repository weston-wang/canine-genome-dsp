# Nonlinear stochastic DSP benchmark in resectable melanoma

## Disease and decision

The target is macroscopic resectable stage III cutaneous melanoma. The current benchmark policy is
two neoadjuvant flat doses of ipilimumab 80 mg plus nivolumab 240 mg three weeks apart, surgery at
week 6, and pathological-response-directed adjuvant treatment, as studied in NADINA. The code only
models the six-week neoadjuvant window. Surgery and adjuvant treatment remain fixed clinical
decisions outside its controller.

The 2025 ESMO clinical practice guideline says neoadjuvant nivolumab-ipilimumab followed by surgery
should be offered for resectable stage III melanoma with clinically or radiologically detectable
metastasis. The project therefore treats NADINA as the strongest disease-matched clinical evidence
benchmark, not as a claim that the regimen has identical regulatory status or availability in every
country.

This setting is unusually useful for nonlinear system identification:

- ipilimumab and nivolumab are separate inputs with different mechanisms;
- checkpoint blockade produces delayed, repeated clonal T-cell waves;
- OpACIN-neo randomized three dose/order patterns;
- the resection specimen provides an objective early output; and
- NADINA supplies a randomized phase-3 treatment-policy benchmark.

“Underused” is more accurate than “never used.” Stochastic tumor models, ordinary differential
equations, PK/QSP, and machine learning already exist in immuno-oncology. The uncommon part here is
the engineering combination of a block-oriented input model, bilinear state modulation, an
explicit finite-memory cross-kernel, stochastic escape, held-out-arm system identification, and a
fail-closed control comparison.

## Model stack

For daily administered inputs `u = [ipilimumab, nivolumab]`, a Hammerstein-Wiener block first maps
dose to saturating exposure, antibody disposition, and target occupancy. This prevents the Volterra
kernel from being asked to rediscover basic pharmacology.

The latent immune state is
`x = [progenitor-exhausted CD8 T cells, effectors, exhaustion/inflammation]`. Its update is bilinear:
nivolumab occupancy changes the gain from progenitor to effector state, while ipilimumab occupancy
changes priming and differentiation. The efficacy residual interaction is a bounded rank-one
second-order Volterra term,

`r[t] = bound * tanh(gain * (a * u_ipi)[t] * (b * u_nivo)[t] / bound)`.

The rank-one lag factors are a deliberate identifiability constraint. Four three-weekly immune
measurements cannot support a dense lag-by-lag surface or a third-order tensor.

The same cross-kernel is not automatically inserted into the serious-toxicity head. A real-arm
ablation checks that shared-kernel assumption explicitly; the default keeps toxicity on the
bilinear inflammatory state plus administered-dose burden. This output-specific partition avoids
claiming that therapeutic synergy and immune toxicity share one unidentified nonlinearity.

Visible and immune-escape tumor states evolve through stochastic birth, death, immune killing, and
pressure-dependent phenotype transition. Patient gains and process innovations vary between Monte
Carlo draws. A serious-toxicity proxy depends on the latent inflammatory state and administered
antibody burden. It is not a CTCAE-grade probability until calibrated against individual adverse-
event records.

The search is restricted to days 0–28, no more than the NADINA total dose, and no more than a NADINA
single dose at any administration. This is still not randomized treatment support: a schedule can
be numerically feasible and clinically unevaluated.

## What is real and what is modeled

The evidence sources have non-interchangeable roles:

| Source | Role | What it cannot do |
|---|---|---|
| GSE272993 and associated study | Directional checks for weeks 3/6/9 clonal and effector dynamics | Identify stage-III outcomes or a causal schedule |
| OpACIN-neo | Leave-one-randomized-arm-out MPR/pathology and 12-week grade 3–4 irAE validation | Establish survival superiority from three small arms |
| NADINA | Locked best-clinical regimen and MPR/EFS/DMFS/safety anchors | Validate an unrandomized model-generated timing change |

The benchmark prefers OpACIN-neo major pathological response (MPR, no more than 10% viable tumor)
when those rows are present. Its broader “pathological response” (less than 50% viable tumor) remains
in the registry but is not silently compared with NADINA MPR.

Aggregate counts are represented as binomial events with frequency weights. They are never expanded
into fake independent patients. Each OpACIN arm is held out in turn, and both response and toxicity
are predicted from the remaining arms. The selected-regimen recovery rule is: response no worse
than ten percentage points from the predicted best arm, then lowest predicted serious toxicity.
This tolerance is wider than the observed 6.7-point arm-A versus arm-B MPR difference and reflects
the uncertainty of the small, non-powered phase-2 arm comparison; it is not an efficacy claim.

## Decision gates

The virtual candidate may pass by either route:

1. terminal modeled tumor improves by more than 5% while modeled toxicity is no worse than 5%; or
2. terminal modeled tumor is no worse than 5% while modeled toxicity improves by more than 10%.

Escape fraction must not increase by more than five percentage points. Intervals use paired
bootstrap resampling of common-random-number virtual patients. These gates can support only
`IN_SILICO_CANDIDATE`; the clinical result always remains
`NOT_CLINICALLY_EVALUABLE_AGGREGATE_ONLY`.

## Clinical path to a real test

The next dataset needs exact drug timestamps, baseline tumor and BRAF status, serial PBMC scRNA/TCR
or compact flow panels, ctDNA, imaging, surgical pathology, steroid/rescue treatment, and time-
resolved adverse events. Development and validation must be separated by patient and site.

After locked external validation, the controller should run silently without changing care. A
prospective study could then randomize a narrowly supported timing adjustment against the NADINA
regimen, with co-gates for MPR, surgery completion, grade 3 or higher immune toxicity, EFS/DMFS, and
patient-reported quality of life. Until then, the exported candidate schedule is a hypothesis—not a
prescription or evidence of superiority.
