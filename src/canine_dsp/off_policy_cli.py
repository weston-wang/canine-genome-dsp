"""File-oriented logged-policy evaluation."""

import json
from pathlib import Path

import pandas as pd

from .off_policy import OPEThresholds, evaluate_logged_policy


def evaluate_logged_policy_file(table: Path, out: Path, gamma: float = 1.0,
                                cross_fitted: bool = False) -> None:
    data = pd.read_csv(table)
    summary = evaluate_logged_policy(data, OPEThresholds(), gamma,
                                     cross_fitted_nuisance=cross_fitted)
    out.mkdir(parents=True, exist_ok=True)
    (out / "off_policy_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    report = f"""# Logged-policy evaluation

Evidence status is **`{summary['evidence_status']}`**. The sequential doubly robust estimate differs from the observed behavior-policy value by **{summary['sequential_dr_improvement']:.4f}** (patient-bootstrap 95% interval **{summary['sequential_dr_improvement_patient_bootstrap95'][0]:.4f} to {summary['sequential_dr_improvement_patient_bootstrap95'][1]:.4f}**). Effective sample size is **{summary['effective_sample_size']:.1f}** across {summary['patients']} patients; action-overlap fraction is **{summary['action_overlap_fraction']:.1%}**.

This estimate is valid only under consistency, sequential exchangeability, positivity, and correct cross-fitted nuisance models. It is not evidence of clinical superiority and must abstain when the status begins with `NOT_EVALUABLE`.
"""
    (out / "clinical_interpretation.md").write_text(report)
