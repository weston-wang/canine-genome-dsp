import pandas as pd

from canine_dsp.policy_benchmark import heldout_scenarios, superiority_analysis


def synthetic_outcomes(candidate_safety=False):
    rows = []
    for scenario in ["a", "b", "c", "d"]:
        for draw in range(12):
            rows.append({"scenario": scenario, "draw": draw,
                         "policy": "qsp_risk_optimized", "utility_loss": 1.0,
                         "terminal_tumor": 1.0, "escape_fraction": .2,
                         "inflammation_exceeded": False})
            rows.append({"scenario": scenario, "draw": draw,
                         "policy": "candidate", "utility_loss": .8,
                         "terminal_tumor": .8, "escape_fraction": .2,
                         "inflammation_exceeded": candidate_safety})
    return pd.DataFrame(rows)


def test_structural_shift_scenarios_include_zero_interaction_stress_tests():
    scenarios = heldout_scenarios(6)
    assert all(scenario.kernels.h2 is not None for scenario in scenarios)
    assert not scenarios[-1].kernels.h2.any()
    assert not scenarios[-2].kernels.h2.any()


def test_superiority_requires_benefit_safety_and_shift_replication():
    result = superiority_analysis(synthetic_outcomes(), "candidate", seed=2)
    assert result["efficacy_superiority_criterion_met"]
    assert result["minimum_meaningful_improvement_criterion_met"]
    assert result["tumor_noninferiority_criterion_met"]
    assert result["safety_noninferiority_criterion_met"]
    assert result["escape_noninferiority_criterion_met"]
    assert result["distribution_shift_robustness_criterion_met"]
    assert result["simulation_superiority_supported"]
    assert not result["clinical_superiority_established"]


def test_superiority_fails_closed_when_safety_is_worse():
    result = superiority_analysis(synthetic_outcomes(candidate_safety=True), "candidate", seed=2)
    assert not result["safety_noninferiority_criterion_met"]
    assert not result["simulation_superiority_supported"]
