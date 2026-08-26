"""Tests for `hsa_alternative_approach`.

The module's job is to answer whether the toxicity finding forces a different approach. These
tests check the three claims that answer carries: no schedule rescues the drug, the pair fails a
duration criterion by the same margin that disqualified an earlier candidate, and a modest gain in
vaccine height converts the drug from indefinite therapy into a short induction.
"""
import pytest

from canine_dsp import hsa_alternative_approach as alt


# ---------------------------------------------------------------------------------------------
# Step 1: schedules.

def test_no_schedule_beats_continuous_full_dose():
    """Every reduced-exposure schedule loses ground against continuous full dosing."""
    reduced = (list(alt.DUTY_CYCLING.values())
               + [v for f, v in alt.DOSE_REDUCTION.items() if f < 1.0]
               + [d for _, d in alt.DE_ESCALATION.values()])
    assert reduced, "there should be reduced-exposure schedules to compare"
    assert max(reduced) < alt.CONTINUOUS_FULL_DOSE


def test_dose_reduction_is_monotone_in_dose():
    fractions = sorted(alt.DOSE_REDUCTION)
    durability = [alt.DOSE_REDUCTION[f] for f in fractions]
    assert durability == sorted(durability), "less drug should never do better"


def test_continuous_low_dose_beats_pulsed_full_dose_where_the_schedules_separate():
    """The finding that inverts the usual clinical instinct about drug holidays.

    It holds at three-quarter and half dose. At quarter dose every arm has collapsed to roughly
    the no-second-drug baseline and the schedules are within Monte Carlo noise of each other, so
    the module claims the rule only where the data support it.
    """
    for fraction in (0.75, 0.50):
        continuous = alt.DOSE_REDUCTION[fraction]
        pulsed = [v for (_period, on), v in alt.DUTY_CYCLING.items() if on == fraction]
        assert len(pulsed) == 3, "each on-fraction should be tested at three periods"
        assert continuous > max(pulsed), (
            f"at {fraction:.0%} of cumulative dose, continuous {continuous} should beat "
            f"pulsed {pulsed}")


def test_at_quarter_dose_the_schedules_are_indistinguishable():
    """The stated limit of the rule, checked rather than asserted in prose alone."""
    continuous = alt.DOSE_REDUCTION[0.25]
    pulsed = [v for (_period, on), v in alt.DUTY_CYCLING.items() if on == 0.25]
    assert max(pulsed + [continuous]) - min(pulsed + [continuous]) < 0.05
    assert "indistinguishable" in alt.CONTINUOUS_BEATS_INTERMITTENT_AT_MATCHED_DOSE[
        "where_the_rule_stops_holding"]


def test_duty_cycle_period_matters_less_than_the_on_fraction():
    """Spread within an on-fraction should be much smaller than spread across on-fractions."""
    by_fraction = {}
    for (_period, on), value in alt.DUTY_CYCLING.items():
        by_fraction.setdefault(on, []).append(value)
    within = max(max(v) - min(v) for v in by_fraction.values())
    across = max(max(v) for v in by_fraction.values()) - min(min(v) for v in by_fraction.values())
    assert within < across / 2


def test_de_escalation_records_both_cumulative_dose_and_durability():
    for after, (cumulative, durability) in alt.DE_ESCALATION.items():
        assert 0.0 <= after <= 1.0
        assert 0.0 < cumulative <= 1.0
        assert 0.0 <= durability <= 1.0
    # Two years of full dose then nothing is the same as simply stopping at year two.
    assert alt.DE_ESCALATION[0.0][1] == alt.VACCINE_HEIGHT_VS_DRUG_STOP[(0.0300, 2)]


def test_the_schedule_verdict_rules_out_the_comfortable_answer():
    assert "no schedule" in alt.SCHEDULE_VERDICT["finding"]
    assert "moves off the drug" in alt.SCHEDULE_VERDICT["what_it_leaves"]


# ---------------------------------------------------------------------------------------------
# Step 2: the duration criterion.

def test_duration_shortfall_is_a_ratio_of_required_to_demonstrated():
    assert alt.duration_shortfall(365, 3650) == pytest.approx(10.0)
    assert alt.duration_shortfall(3650, 3650) == pytest.approx(1.0)


def test_duration_shortfall_rejects_nonsense_inputs():
    for bad in (0, -1):
        with pytest.raises(ValueError):
            alt.duration_shortfall(bad)
    with pytest.raises(ValueError):
        alt.duration_shortfall(17, horizon_days=0)


def test_the_pair_fails_the_duration_criterion_by_roughly_two_hundred_fold():
    shortfall = alt.duration_shortfall(alt.DOCUMENTED_TOLERABILITY_DAYS)
    assert not alt.clears_duration_criterion(alt.DOCUMENTED_TOLERABILITY_DAYS)
    assert 200 < shortfall < 230
    assert alt.THE_DURATION_CRITERION["applied_to_the_pair"]["fold_short"] == pytest.approx(shortfall)


def test_an_agent_dosed_beyond_the_horizon_clears_the_criterion():
    assert alt.clears_duration_criterion(alt.TREATMENT_HORIZON_DAYS)
    assert alt.clears_duration_criterion(alt.TREATMENT_HORIZON_DAYS + 1)


def test_the_criterion_is_stated_as_the_same_form_as_the_exposure_criterion():
    """The symmetry is the argument -- applying one standard and not the other is special pleading."""
    assert "special pleading" in alt.THE_DURATION_CRITERION[
        "the_symmetry_that_makes_this_hard_to_wave_away"]
    assert "unknown over" in alt.THE_DURATION_CRITERION["what_it_does_not_say"]


def test_every_obvious_swap_clears_duration_and_fails_for_a_different_reason():
    swaps = {k: v for k, v in alt.WHY_THE_OBVIOUS_SWAPS_DO_NOT_WORK.items() if k != "the_pattern"}
    assert len(swaps) == 3
    for name, entry in swaps.items():
        assert "duration criterion" in entry["verdict"], name
        assert entry["why_it_fails"]
    verdicts = {e["verdict"] for e in swaps.values()}
    assert len(verdicts) == 3, "each should fail for a distinct reason"


# ---------------------------------------------------------------------------------------------
# Step 3: the structural alternative.

def test_drug_days_and_exposure_fraction_agree():
    assert alt.drug_days(1) == 365
    assert alt.drug_days(None) == alt.TREATMENT_HORIZON_DAYS
    assert alt.exposure_fraction(1) == pytest.approx(0.1)
    assert alt.exposure_fraction(None) == pytest.approx(1.0)
    with pytest.raises(ValueError):
        alt.drug_days(0)


def test_drug_days_never_exceeds_the_horizon():
    assert alt.drug_days(50) == alt.TREATMENT_HORIZON_DAYS


def test_the_grid_is_monotone_in_vaccine_height():
    """At any fixed withdrawal time, a taller vaccine never does worse."""
    heights = sorted({h for h, _ in alt.VACCINE_HEIGHT_VS_DRUG_STOP})
    for stop in (1, 2, 3, 5, None):
        column = [alt.VACCINE_HEIGHT_VS_DRUG_STOP[(h, stop)] for h in heights]
        assert column == sorted(column), f"non-monotone at stop={stop}: {column}"


def test_at_the_measured_height_no_withdrawal_time_is_acceptable():
    """The finding this module starts from, restated on the grid."""
    early = [alt.VACCINE_HEIGHT_VS_DRUG_STOP[(alt.MEASURED_VACCINE_HEIGHT, s)] for s in (1, 2, 3)]
    assert max(early) < 0.5
    assert alt.VACCINE_HEIGHT_VS_DRUG_STOP[(alt.MEASURED_VACCINE_HEIGHT, None)] == pytest.approx(
        alt.CONTINUOUS_FULL_DOSE)


def test_a_one_and_a_half_fold_taller_vaccine_makes_the_drug_a_one_year_induction():
    """The headline: 90% less drug AND higher durability."""
    target = alt.THE_EXCHANGE_RATE["at_1_5x"]
    assert target["height"] == pytest.approx(1.5 * alt.MEASURED_VACCINE_HEIGHT)
    stopped_early = alt.VACCINE_HEIGHT_VS_DRUG_STOP[(0.0450, 1)]
    never_stopped_at_measured = alt.VACCINE_HEIGHT_VS_DRUG_STOP[(alt.MEASURED_VACCINE_HEIGHT, None)]
    assert stopped_early > never_stopped_at_measured
    assert alt.exposure_fraction(1) == pytest.approx(0.1)


def test_the_required_height_sits_below_the_bar():
    """The vaccine never has to hold the tumour alone -- that is what makes 1.5x reachable."""
    assert alt.THE_EXCHANGE_RATE["at_1_5x"]["height"] < alt.THE_BAR


def test_a_quarter_taller_is_not_enough_to_stop_early():
    assert alt.VACCINE_HEIGHT_VS_DRUG_STOP[(0.0375, 2)] < 0.8
    assert alt.VACCINE_HEIGHT_VS_DRUG_STOP[(0.0375, None)] == pytest.approx(1.0)


def test_the_escape_clone_suppression_is_explained_rather_than_assumed():
    entry = alt.WHY_A_TALLER_VACCINE_ALSO_SUPPRESSES_THE_ESCAPE_CLONE
    assert "ANTIGEN-POSITIVE burden" in entry["the_actual_mechanism"]
    assert "250 trials" in entry["the_limit_of_the_claim"]


# ---------------------------------------------------------------------------------------------
# The evidence behind the swap.

def test_the_suppression_axis_is_measured_in_this_tumour():
    entry = alt.HSA_ACTIVELY_SUPPRESSES_THE_ARM_THE_VACCINE_USES
    assert "35136176" in entry["citation"]
    assert "PD-L1" in entry["what_is_in_the_tumour"]
    assert "smaller number of T-cells" in entry["the_functional_consequence"]


def test_the_checkpoint_antibody_is_dosed_like_a_booster_not_like_a_kinase_inhibitor():
    entry = alt.A_CANINE_CHECKPOINT_ANTIBODY_IS_AVAILABLE
    assert "42247661" in entry["citation"]
    assert entry["design"].startswith("multi-institutional")
    assert "q28d" in entry["dosing"] and "q14d" in entry["dosing"]
    assert 0.0 < entry["efficacy"]["melanoma_orr"] < entry["efficacy"]["mct_orr"] < 1.0


def test_the_haemorrhage_signal_is_left_open_rather_than_argued_away():
    entry = alt.THE_HAEMORRHAGE_SIGNAL
    assert entry["status"].startswith("OPEN")
    assert "haemorrhage" in entry["the_observation"]
    assert "reasoned away" in entry["status"]


def test_corticosteroids_are_recorded_as_the_third_timing_constraint():
    entry = alt.CORTICOSTEROIDS_ARE_A_THIRD_TIMING_CONSTRAINT
    assert "40342421" in entry["citation"]
    assert "monocytic" in entry["result"]
    for pmid_free_marker in ("Rebhun 2025", "Borgatti 2020"):
        assert pmid_free_marker in entry["the_third_of_a_set"]


# ---------------------------------------------------------------------------------------------
# The regimen and the verdict.

def test_the_revised_regimen_changes_the_drug_from_indefinite_to_an_induction():
    changed = " ".join(alt.REVISED_REGIMEN["changed"])
    assert "ONE-YEAR INDUCTION" in changed
    assert "anti-PD-1" in changed
    unchanged = " ".join(alt.REVISED_REGIMEN["unchanged"])
    assert "q60d boosters" in unchanged, "boosters remain mandatory"
    assert "NK component" in unchanged, "the antigen-loss clone still needs its own answer"


def test_the_cost_of_the_alternative_is_stated_on_both_sides():
    cost = alt.WHAT_THE_ALTERNATIVE_COSTS
    assert "drug-days" in cost["removed"]
    assert "haemorrhage" in cost["added"]
    assert "not an effect size taken from data" in cost["added_uncertainty"]


def test_the_verdict_answers_the_question_that_was_asked():
    assert alt.VERDICT["the_question"].startswith("given the toxicity")
    assert "not an alternative drug" in alt.VERDICT["the_answer"]
    assert alt.VERDICT["what_remains_open"]


# ---------------------------------------------------------------------------------------------
# The second lever: monocyte-recruitment blockade.

def test_the_recruitment_axis_is_characterised_in_hemangiosarcoma_itself():
    entry = alt.HSA_IS_THE_MOST_MONOCYTE_RECRUITING_CANINE_TUMOUR
    assert "27779362" in entry["citation"]
    assert "SIGNIFICANTLY GREATER" in entry["the_comparison"]
    assert "CCL2-DEPENDENT" in entry["the_chemokine"]
    assert "adjuvant strategy" in entry["authors_conclusion"]


def test_losartan_exposure_was_settled_by_dose_escalation_not_by_a_ratio():
    entry = alt.LOSARTAN_HAS_BEEN_DOSE_FOUND_IN_DOGS
    assert "34580111" in entry["citation"]
    assert "TEN-FOLD HIGHER" in entry["the_exposure_result"]
    assert "pharmacodynamic endpoint" in entry["why_that_sentence_matters_so_much"]


def test_losartan_is_the_first_agent_to_clear_both_criteria():
    """Every earlier candidate cleared one criterion and failed the other."""
    entry = alt.LOSARTAN_CLEARS_BOTH_CRITERIA
    assert entry["exposure"] and entry["duration"]
    assert "first agent" in entry["the_significance"]
    # The swaps in step 2 are the contrast: each clears duration and then falls over on something
    # else, so none of them clears both.
    swaps = {k: v for k, v in alt.WHY_THE_OBVIOUS_SWAPS_DO_NOT_WORK.items() if k != "the_pattern"}
    for name, swap in swaps.items():
        head, _, tail = swap["verdict"].partition(",")
        assert "clears the duration criterion" in head, name
        assert tail.strip(), f"{name} should record what it fails on"


def test_the_losartan_limits_are_recorded_at_the_same_volume_as_the_claim():
    limits = alt.WHAT_LOSARTAN_DOES_NOT_ESTABLISH
    assert "osteosarcoma" in limits["no_hemangiosarcoma_trial"]
    assert "toceranib" in limits["the_partner_drug_does_not_transfer"]
    assert "single dog" in limits["a_case_report_shows_the_ceiling"]
    assert "does not measure it" in limits["the_number_is_still_unmeasured"]


def test_the_two_levers_act_at_different_points_on_one_pathway():
    entry = alt.TWO_LEVERS_ON_ONE_COMPARTMENT
    assert "anti-PD-1" in entry["lever_1_effector"]
    assert "CCL2-CCR2" in entry["lever_2_recruitment"]
    assert "Neither has to" in entry["why_independence_matters"]


def test_partial_delivery_of_the_requirement_still_buys_something():
    """The fallback claim, checked against the grid rather than taken on trust."""
    quarter_taller = alt.VACCINE_HEIGHT_VS_DRUG_STOP[(0.0375, 5)]
    measured_never_stopped = alt.VACCINE_HEIGHT_VS_DRUG_STOP[(alt.MEASURED_VACCINE_HEIGHT, None)]
    assert quarter_taller > measured_never_stopped, (
        "1.25x with a five-year stop should beat the measured height dosed forever")
    assert "partial reduction in drug-years" in alt.TWO_LEVERS_ON_ONE_COMPARTMENT[
        "the_fallback_is_graded_not_binary"]


def test_the_pointed_experiment_names_four_arms_and_a_growth_rate_readout():
    experiment = alt.TWO_LEVERS_ON_ONE_COMPARTMENT["the_experiment_this_points_at"]
    assert "ISOS-1" in experiment
    assert "growth-rate" in experiment


# ---------------------------------------------------------------------------------------------
# The third route, and the qualification it forces.

def test_swapping_vaccine_platforms_is_ruled_out_by_the_larger_trial():
    entry = alt.PICKING_A_BETTER_PLATFORM_DOES_NOT_WORK
    assert "26994144" in entry["the_phase_1_signal"]
    assert "39955616" in entry["the_confirmatory_trial"]
    assert "118 dogs" in entry["the_confirmatory_trial"]
    assert "did not replicate" in entry["the_result"]
    assert "no shelf to reach for" in entry["what_this_settles"]


def test_the_platform_failure_is_read_as_evidence_for_the_microenvironment_route():
    reasoning = alt.PICKING_A_BETTER_PLATFORM_DOES_NOT_WORK[
        "why_this_strengthens_the_microenvironment_route"]
    assert "imposed from outside the vaccine" in reasoning


def test_the_booster_claim_is_qualified_rather_than_quietly_kept():
    """This analysis leaned on 'boosters buy persistence, not height'. The 118-dog trial complicates
    that for dogs starting below their own ceiling, and the module has to say so."""
    entry = alt.REPEAT_IMMUNISATION_RAISED_RESPONSE_MAGNITUDE_IN_LOW_RESPONDERS
    assert "COMPARABLE" in entry["the_finding_that_qualifies_the_claim"]
    assert entry["what_this_analysis_had_been_saying"]
    assert "property of the" in entry["where_it_needs_qualifying"]


def test_the_qualification_keeps_what_remains_true():
    """The population-level claim survives -- DFI and OS did not move."""
    entry = alt.REPEAT_IMMUNISATION_RAISED_RESPONSE_MAGNITUDE_IN_LOW_RESPONDERS
    assert "did not move" in entry["what_this_analysis_had_been_saying"]
    assert "remains true" in entry["what_this_analysis_had_been_saying"]


def test_one_assay_now_serves_both_timing_and_redosing_decisions():
    entry = alt.REPEAT_IMMUNISATION_RAISED_RESPONSE_MAGNITUDE_IN_LOW_RESPONDERS
    assert "PBMC cytotoxic" in entry["the_readout_converges_with_the_timing_work"]
    assert "Rebhun 2025" in entry["the_readout_converges_with_the_timing_work"]


def test_the_requirement_now_rests_on_three_independent_routes():
    entry = alt.THREE_ROUTES_TO_THE_REQUIREMENT
    routes = [entry[k] for k in ("route_1", "route_2", "route_3")]
    assert len(set(routes)) == 3
    assert "platforms" in entry["what_is_ruled_out"]
    assert "None of them is measured" in entry["why_three_matters"], (
        "the module must not let three mechanisms read as a measurement")
