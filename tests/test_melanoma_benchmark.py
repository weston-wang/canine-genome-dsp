import json
from pathlib import Path

import numpy as np
import pandas as pd

from canine_dsp.melanoma_benchmark import (
    opacin_equivalent_schedules,
    run_melanoma_benchmark,
)


ANCHORS = Path(__file__).parents[1] / "data/clinical/melanoma_clinical_anchors.csv"


def test_curated_trial_counts_preserve_like_for_like_endpoints():
    anchors = pd.read_csv(ANCHORS)
    opacin = anchors.loc[
        (anchors.study == "OpACIN-neo")
        & (anchors.endpoint == "major_pathological_response")
    ].set_index("arm")
    assert opacin.numerator.astype(int).to_dict() == {
        "arm A": 21, "arm B": 19, "arm C": 12}
    assert opacin.denominator.astype(int).to_dict() == {
        "arm A": 30, "arm B": 30, "arm C": 26}

    nadina = anchors.set_index("record_id")
    assert int(nadina.loc["nadina_neoadj_mpr", "numerator"]) == 125
    assert int(nadina.loc["nadina_neoadj_mpr", "denominator"]) == 212
    assert nadina.loc["nadina_neoadj_efs_12m", "estimate"] == 83.7


def test_opacin_schedule_encodes_the_published_sequential_arm():
    schedules = opacin_equivalent_schedules()
    assert schedules["arm A"][0].tolist() == [240.0, 80.0]
    assert schedules["arm B"][21].tolist() == [80.0, 240.0]
    assert schedules["arm C"][0, 0] == 240.0
    assert schedules["arm C"][21].tolist() == [240.0, 240.0]
    assert schedules["arm C"][35, 1] == 240.0
    assert schedules["arm C"][0, 1] == 0.0


def test_benchmark_exports_real_arm_validation_and_fails_closed(tmp_path):
    run_melanoma_benchmark(tmp_path, ANCHORS, draws=16, candidates=5, seed=7)
    summary = json.loads((tmp_path / "summary.json").read_text())
    assert summary["data_sources"] == [
        "GSE272993", "OpACIN-neo NCT02977052", "NADINA NCT04949113"]
    assert not summary["clinical_superiority_supported"]
    assert summary["clinical_evidence_status"] == "NOT_CLINICALLY_EVALUABLE_AGGREGATE_ONLY"
    assert "full_dsp_stack" in summary["randomized_arm_validation"]
    assert len(pd.read_csv(tmp_path / "opacin_leave_one_arm_out_predictions.csv")) == 15
    candidate = pd.read_csv(tmp_path / "candidate_schedule.csv")
    assert np.all(candidate[["ipilimumab", "nivolumab"]].to_numpy() >= 0)
    assert candidate.role.eq("research_hypothesis_not_recommendation").all()
    assert (tmp_path / "melanoma_dsp_dashboard.png").stat().st_size > 0
