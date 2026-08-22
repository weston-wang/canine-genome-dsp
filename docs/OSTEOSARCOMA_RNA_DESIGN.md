# Comparative osteosarcoma RNA-vaccine inverse design

## Scope

This program is research software for designing a falsifiable canine osteosarcoma vaccine and its
prospective validation experiment. It does not prescribe veterinary or human treatment, infer a
manufacturing-ready sequence, or establish that an RNA vaccine improves disease-free or overall
survival. For this postoperative canine target, amputation and adjuvant chemotherapy remain fixed
current-care constraints.

The initial target is appendicular osteosarcoma after amputation, before radiographically visible
pulmonary relapse. Dogs provide a spontaneous immunocompetent disease model and a compressed disease
clock; humans and dogs share pathway-level priors but use separate MHC models, transition clocks,
and observation distributions.

The inverse-design hypothesis is an antigen-defined multivalent mRNA cargo. The direct canine pilot
and human RNA-PRIME platform instead use total-tumor RNA (with pp65 bridging in RNA-PRIME). Those
programs support RNA-platform feasibility and sampling ideas, not equivalence to this cargo or its
schedule.

## Model stack

The latent states are:

1. no evident disease / minimal residual disease;
2. innate priming;
3. adaptive immune control;
4. occult immune-escape disease;
5. visible relapse; and
6. exhaustion or suppression.

An explicit elapsed-duration state turns the HMM into a hidden semi-Markov model. This avoids the
plain-HMM assumption that the chance of leaving a state is independent of how long the patient has
occupied it. Dog and human dwell-time hazards and emissions are separate.

Treatment histories modify conditional transition logits through a bounded low-rank Volterra
operator:

\[
\operatorname{logit} P(z_{t+1}=j\mid z_t=i)
=a_{ij}+\sum_{\tau}h^{(1)}_{ij\tau}u_{t-\tau}
+\sum_r(L_{ijr}*u)_t(R_{ijr}*u)_t.
\]

The inputs are antigen coverage, normalized RNA exposure, chemotherapy, checkpoint blockade, and
immune suppression. First-order kernels encode delayed memory. The factored second-order term can
represent antigen-coverage × RNA-exposure, vaccine × chemotherapy timing, or checkpoint × immune-
suppression interactions without estimating an unconstrained lag-by-lag-by-treatment tensor. All
logit adjustments are bounded. Third order is intentionally excluded until intervention diversity
and cohort size identify it.

The forward filter is normalized in the log domain, accepts missing observations, and returns state
and elapsed-duration posteriors. Viterbi decoding returns the most likely augmented-state path. The
bundled parameters are illustrative priors used for software tests and prospective design—not fitted
clinical parameters. The benchmark stretches the canine dwell-time scales by a fixed factor of 1.29
so the standard-care proxy has an approximately 180-day median first visible relapse, matching the
COTC022 aggregate median DFI. This is a coarse clock anchor only: it is not a patient-level fit and
does not validate individual transition probabilities, emissions, or treatment effects. The
postoperative benchmark moves the reference model's day-zero visible-disease mass into occult escape
so the target population begins without modeled radiographically visible relapse.

Policy probabilities use exact finite-state propagation over state, elapsed duration, and an
ever-relapsed flag. The disease-free objective rewards immune control only before first visible
relapse, so a later return from visible disease cannot undo a DFI event. Monte Carlo remains only in
the synthetic filter/decoder ablation and representative visualization, not in schedule ranking.

## Cargo inverse problem

The upstream antigen pipeline must start from paired tumor/normal DNA, tumor RNA, and patient DLA or
HLA typing. Candidate construction should include SNVs, indels, fusions, structural variants, and
carefully safety-screened shared antigens. The inverse layer receives normalized measurements for:

- tumor expression, clonality, and truncality;
- class-I and class-II presentation;
- normal-proteome dissimilarity/safety;
- presentation retention and antigen/HLA/DLA-loss risk;
- covered tumor subclones; and
- manufacturability.

The optimizer filters unsafe/ineligible rows, enforces class-I and class-II breadth, covers required
subclones and alleles, requires structural-variant/fusion diversity, and ranks feasible cargo under
nominal and escape scenarios. Pairwise effects use low-rank synergy and competition loadings. Small
spaces are enumerated exactly; large spaces use a deterministic coverage-diverse beam search and
report that optimality is not guaranteed.

The candidate CSV accepted by `--candidates` requires these columns:

```text
candidate_id,species,source_class,expression,clonality,truncality,
mhc_i_presentation,mhc_ii_presentation,normal_proteome_safety,
presentation_retention,escape_risk,manufacturability,subclones,
class_i_alleles,class_ii_alleles
```

Optional columns are `gene`, `synergy_loadings`, and `competition_loadings`. Sets and loading
vectors use semicolon separators. `source_class` is one of `snv`, `indel`, `fusion`,
`structural_variant`, `cancer_testis`, `overexpressed`, or `other`. Human allele names must begin
with `HLA-`; canine names must begin with `DLA-`. Values in `[0,1]` must come from a locked,
independently evaluated upstream pipeline. The file should contain no owner, patient, or directly
identifying information.

A real candidate file requires `--design-spec`. This schema-v1 JSON records the actual patient or
cohort clone labels, typed DLA alleles, safety thresholds, cargo breadth constraints, and explicit
escape scenarios; demo labels are never silently substituted. For example:

```json
{
  "schema_version": 1,
  "constraints": {
    "species": "canine",
    "min_antigens": 4,
    "max_antigens": 7,
    "required_subclones": ["founder", "pulmonary_clone_7"],
    "required_class_i_alleles": ["DLA-88*034:01"],
    "required_class_ii_alleles": ["DLA-DRB1*001:01"],
    "min_normal_proteome_safety": 0.9
  },
  "scenarios": [
    {"name": "nominal", "species": "canine"},
    {
      "name": "patient_dla_loss",
      "species": "canine",
      "lost_class_i_alleles": ["DLA-88*034:01"]
    }
  ]
}
```

The cargo-design module accepts human/HLA specifications for comparative work. The integrated
clinical benchmark remains canine-first because it uses the canine clock and canine standard-care
comparator; it rejects a human specification instead of applying the wrong species model.

Cargo ranking and the HSMM are connected in two transparent stages, not an end-to-end fitted model.
The dynamic input proxy combines required clone and allele coverage, expression/clonality/truncality,
retained class-I/II presentation, escape risk, and the low-rank cargo interaction. Safety, source
diversity, and manufacturability remain hard eligibility gates rather than invented immune potency.

## Evidence layers and outputs

The benchmark keeps evidence types separate:

- `clinical_anchors_used.csv` preserves published aggregate outcomes and their comparability
  caveats. Aggregate Kaplan-Meier estimates are never expanded into pseudo-patients.
- `real_data/` runs a static prognostic sensitivity analysis on the real GSE76127 pretreatment
  tumors. Probe selection, scaling, PCA, and ridge fitting are repeated inside each held-out-dog
  fold, but the public GEO matrix was cohort-wide preprocessed upstream, so this is not an
  end-to-end inductive validation or a test of the HSMM emissions.
- `candidate_antigen_ranking.csv` and `cargo_design_ranking.csv` audit cargo eligibility, coverage,
  scenario scores, and exclusions.
- `cargo_scenario_contributions.csv` separates first-order and low-rank interaction contributions
  for every retained cargo and robustness scenario.
- `joint_cargo_schedule_search.csv` compares only fixed, enumerated, normalized schedules under the
  reference prior. They are specified for the software run, not clinically preregistered regimens.
  Each schedule includes its analog source, lack of observed RNA-policy support, extrapolation flag,
  and an explicit statement that its dose values are unitless model inputs with no clinical-dose
  evidence. Scores are exact fixed-prior calculations, not clinical response estimates.
- `joint_cargo_schedule_scenarios.csv` exposes every cargo/schedule/escape-scenario calculation;
  selection uses 90% worst-case and 10% scenario-weighted mean performance. Designs within 0.001
  objective units of the winner are labeled near-equivalent instead of treated as distinct winners.
- `run_manifest.json` is the completion gate and records input hashes, the full effective design
  specification, schedules, model hash, code hashes, dependencies, seed, ablation budget, and a
  checksum/size inventory of every published artifact. Runs build in a fresh staging directory and
  replace an earlier owned result tree only after the completion gate succeeds.
- `synthetic_model_ablation.csv` checks software self-consistency for full second-order HSMM,
  first-order HSMM, no-Volterra HSMM, and a mean-dwell-matched truncated-geometric HMM challenger.
- `identifiability_audit.csv` says which model components real data can and cannot estimate.
- reusable plots show cargo selection, clinical anchors, state posteriors, Volterra memory, and real
  held-out-dog predictions.
- `prospective_validation_protocol.csv` exports the locked randomized canine validation requirements.

The GSE76127 cohort has only one pretreatment sample per dog, heterogeneous chemotherapy, and no
public event/censor indicator. Its ordinary regression is therefore only a crude,
treatment-conditioned static prognostic sensitivity analysis, not a survival model. It cannot
identify vaccine memory or hidden-state transitions. A poor held-out result is retained rather than
tuned away because this particular PCA/ridge pipeline did not generalize in this cohort. Any
threshold summaries refer only to whether the reported DFI value is at most 180 days; they are not
validated early-relapse labels because event/censor status is unavailable.

## Clinical comparator and claim gate

The 2025 canine consensus and 2026 AAHA guideline define current care as definitive local control
plus systemic chemotherapy; carboplatin is the preferred canine adjuvant single agent in the
consensus. For this postoperative target, the randomized COTC021/022 standard-care
arm—amputation plus carboplatin—is the reference anchor, with published median DFI of 180 days and
median OS of 282 days. Sequential sirolimus did not improve those endpoints. These current-care
anchors are separate from completed non-RNA intervention studies: COTC026 used a Listeria vector,
COTC030 used inhaled IL-15, and the June 2026 pilot used palliative radiation plus a Listeria vector.
All three are timing or immune-correlate guardrails, not causal RNA-vaccine comparisons.

The completed five-dog canine RNA-LPA abstract supplies early feasibility and acute-response
observations but no controlled efficacy estimate. The UF canine RNA-nanoparticle plus anti-PD-1
study is recruiting, and human RNA-PRIME is active but not recruiting; neither has posted outcomes.
Their protocols can inform sampling and prospective design, but their status pages cannot calibrate
an efficacy effect. In humans, surgery plus MAP-based chemotherapy remains the localized-disease
benchmark; EURAMOS outcome anchors are not directly comparable with canine DFI or recurrent-disease
RNA-PRIME.

The June 2026 radiation-plus-Lm-LLO-HER2 pilot adds a recent completed non-RNA
timing/immune-correlate analog, but it is a 15-dog nonrandomized study in a different local-control
setting with a historical comparator. No completed canine or human randomized osteosarcoma
RNA-vaccine study provides cargo, serial immune measurements, treatment histories, and outcomes
together. Therefore:

```text
clinical_evidence_status = NOT_CLINICALLY_EVALUABLE_NO_RANDOMIZED_RNA_POLICY_DATA
clinical_superiority_supported = false
patient_treatment_recommendation = false
```

These values do not change when the fixed illustrative prior favors a candidate.

## Reference run on 2026-08-02

The reproducible default run used the real 33-dog GSE76127 matrix and public COS33 supplement, plus
the explicitly synthetic candidate panel. The fold-local expression sensitivity analysis had
log-DFI MAE **0.793**, versus **0.792** for the training-median baseline, and Spearman correlation
**-0.469**. It therefore failed both current explicit directional checks; this negative result is
retained. These checks are versioned in the software report, not clinically preregistered endpoints.
Because censoring status is unavailable and chemotherapy is heterogeneous, this is not a survival,
early-relapse, or HSMM-emission validation.

The exact fixed prior ranked an interleaved five-input timing hypothesis. In the worst of five
specified cargo-escape scenarios it assigned visible relapse by the 553-day horizon to **91.29%**,
versus **92.27%** under its standard-care proxy—about a **0.98 percentage-point** model difference.
The conservative fixed-prior comparison gate favored the research hypothesis, but all five retained
interleaved cargo designs were within the **0.001** equivalence tolerance, so the reported cargo rank
is a deterministic tie-break rather than a resolved biological winner. The timing has
`mechanistic_extrapolation_only` evidence support and all antigen IDs are synthetic. The
standard-care proxy's median first visible relapse was **182 days**, two days from the 180-day
aggregate anchor. These are software/prior diagnostics, not estimates of vaccine efficacy;
clinical superiority remained false and not evaluable.

## Prospective validation path

The decisive canine study would lock the candidate pipeline and model before outcomes are seen,
then randomize standard care versus standard care plus the model-ranked RNA vaccine. Serial samples
should include cytokines, CBC, TCR sequencing, ctDNA, thoracic imaging, toxicity, DFI, and survival.
The design must preserve owner/euthanasia and breed/body-size covariates, group every repeated sample
by dog, and predefine missing-data and competing-risk handling.

The first analysis asks whether held-out observations and transition timing are calibrated. Only a
prospective concurrent comparison can test clinical benefit. Human translation follows safety,
immunogenicity, state-recovery, and randomized canine validation; dog and human records are never
treated as exchangeable rows.
