"""Tests for the rule 13 ledger: agent tiers and class dispositions.

These are compliance tests, not sanity checks. Rule 13 makes two assertions falsifiable -- that the
program needs no to-build agent, and that no class was excluded for lacking canine data -- and the
point of the tests is to fail if a later edit quietly breaks either.
"""

from canine_dsp import hsa_agent_tiers as at


# =================================================================================================
# TIERING.
# =================================================================================================

def test_the_program_needs_no_agent_that_has_to_be_built():
    """Rule 13's first half, and the direct answer to failure 8."""
    assert at.to_build_dependencies() == []
    assert at.program_is_built_from_existing_agents() is True


def test_every_agent_carries_a_tier_and_evidence_of_existing():
    assert len(at.PROGRAM_AGENTS) >= 10
    for a in at.PROGRAM_AGENTS:
        assert a.tier in at.EXISTS_TODAY + (at.TO_BUILD,), a.name
        assert len(a.existence_evidence) > 40, a.name
        assert len(a.role_in_program) > 20, a.name


def test_the_tier_counts_match_the_verdict_text():
    """The verdict quotes six/four/three. If the roster changes, the text has to change with it --
    an earlier draft of this verdict quoted counts that did not match the data."""
    counts = at.tier_counts()
    assert counts[at.LICENSED] == 6
    assert counts[at.OFF_LABEL] == 4
    assert counts[at.DOG_TRIALS] == 3
    assert sum(counts.values()) == len(at.PROGRAM_AGENTS) == 13
    assert "six licensed" in at.VERDICT["headline"]
    assert "four off-label" in at.VERDICT["headline"]
    assert "three administered" in at.VERDICT["headline"]


def test_the_load_bearing_components_are_the_ones_with_canine_trial_evidence():
    """The vaccine, eBAT and the checkpoint antibody carry the argument, and each has been given to
    dogs in a published trial rather than inferred from another species."""
    by_name = {a.name: a for a in at.PROGRAM_AGENTS}
    assert by_name["ERstrePs vaccine"].tier == at.DOG_TRIALS
    assert "PMID 37686485" in by_name["ERstrePs vaccine"].existence_evidence
    assert by_name["eBAT"].tier == at.DOG_TRIALS
    assert "PMID 32187827" in by_name["eBAT"].existence_evidence
    assert by_name["caninized anti-PD-1 / anti-PD-L1"].tier == at.DOG_TRIALS


def test_the_ebat_entry_carries_its_negative_trial_as_well_as_its_positive_one():
    """Reporting only the positive trial would be the selective-evidence failure."""
    ebat = next(a for a in at.PROGRAM_AGENTS if a.name == "eBAT")
    assert "positive" in ebat.existence_evidence
    assert "negative" in ebat.existence_evidence
    assert "greater toxicity and reduced efficacy" in ebat.existence_evidence


def test_the_torc_duration_shortfall_is_not_disguised_as_an_existence_problem():
    """The dual TORC1/2 agent exists; what it lacks is duration data. Those are different gaps."""
    agent = next(a for a in at.PROGRAM_AGENTS if a.name == "dual TORC1/2 inhibitor")
    assert agent.tier == at.OFF_LABEL
    assert "17 days" in agent.existence_evidence
    assert "not its existence" in agent.existence_evidence


def test_no_new_molecule_is_not_confused_with_nothing_unmeasured():
    """Failure 4 was merging 'the model contains an agent for this' with 'data support this'."""
    d = at.NO_NEW_MOLECULE_BUT_ONE_UNMEASURED_COMBINATION
    assert d["is_that_a_to_build_agent"].startswith("No")
    assert "QUANTIFICATION gap" in d["what_it_is_instead"]
    assert "coverage gap" in d["why_the_distinction_matters"]


# =================================================================================================
# CLASS DISPOSITIONS.
# =================================================================================================

def test_no_class_is_excluded_for_absence_of_canine_data():
    """Rule 13's second half. This is the test the rule exists for."""
    assert at.classes_excluded_for_absent_canine_data() == []


def test_every_exclusion_cites_one_of_the_three_admissible_reasons():
    assert at.exclusions_with_inadmissible_reasons() == []
    excluded = [c for c in at.CLASS_LEDGER if c.status == at.EXCLUDED]
    assert len(excluded) == 6
    for c in excluded:
        assert c.reason_kind in at.ADMISSIBLE_REASONS, c.modality_class
        assert len(c.reason) > 60, c.modality_class
        assert len(c.the_evidence) > 40, c.modality_class


def test_the_classes_with_no_canine_data_record_that_absence_without_resting_on_it():
    """T-cell engagers and CAR-T have no canine evidence in this indication. Rule 13 requires the
    absence be recorded AND that it not be the reason -- so both must be true of the entry."""
    for name in ("bispecifics -- T-cell engagers", "cell therapy -- CAR-T"):
        c = next(x for x in at.CLASS_LEDGER if x.modality_class == name)
        assert c.reason_kind == at.DEFEATED_BY_ESCAPE, name
        assert "antigen" in c.reason.lower(), name
    engager = next(x for x in at.CLASS_LEDGER
                   if x.modality_class == "bispecifics -- T-cell engagers")
    assert "NOT the reason for exclusion" in engager.the_evidence


def test_transplant_is_excluded_on_shape_and_toxicity_not_on_missing_dog_data():
    """The dog is the canonical HSCT model, so 'no canine data' would have been simply false."""
    c = next(x for x in at.CLASS_LEDGER if x.modality_class == "stem-cell and marrow transplant")
    assert c.status == at.EXCLUDED
    assert c.reason_kind == at.TOXICITY_UNAFFORDABLE
    assert c.tier_of_the_best_available_agent == at.DOG_TRIALS   # it exists in dogs
    assert "PMID 11215693" in c.the_evidence
    assert "NOT for absent canine" in c.the_evidence
    assert "permanently present negative-growth floor" in c.reason


def test_the_two_bispecific_entries_are_kept_apart():
    """eBAT is a bispecific and is in the program; a T-cell engager is a bispecific and is not.
    Collapsing them would make the ledger look like it had excluded its own component."""
    angio = next(x for x in at.CLASS_LEDGER if x.modality_class == "bispecifics -- angiotoxin")
    engager = next(x for x in at.CLASS_LEDGER
                   if x.modality_class == "bispecifics -- T-cell engagers")
    assert angio.status == at.IN_PROGRAM
    assert engager.status == at.EXCLUDED
    assert "not antigen-directed" in angio.reason


def test_radiation_is_split_by_whether_the_target_can_be_imaged():
    """Body radiation is excluded on dissemination; brain SRS is credited only against an imaged
    deposit. The same modality gets two dispositions because the targets differ."""
    body = next(x for x in at.CLASS_LEDGER if x.modality_class == "radiation -- body")
    brain = next(x for x in at.CLASS_LEDGER
                 if x.modality_class == "radiation -- brain, to an imaged deposit")
    assert body.status == at.EXCLUDED and body.reason_kind == at.DEFEATED_BY_ESCAPE
    assert "PMID 31841095" in body.the_evidence
    assert "EXPLICITLY EXCLUDED" in body.the_evidence      # the canine series excluded HSA itself
    assert brain.status == at.IN_PROGRAM
    assert "NOT credited" in brain.reason and "occult" in brain.reason


def test_unassessed_classes_are_labelled_unassessed_rather_than_excluded_or_closed():
    """Rule 9's third category. Each must carry a named path to assessment."""
    unassessed = at.unassessed_classes()
    assert {c.modality_class for c in unassessed} == {"oncolytic virus", "cytokine agents"}
    for c in unassessed:
        assert c.reason_kind == ""                      # no exclusion reason is claimed
        assert "named path" in c.the_evidence or "path to assessment" in c.the_evidence


def test_the_ledger_covers_the_classes_rule_9_enumerates():
    """Rule 9 fixes the minimum candidate universe for cancer work."""
    text = " ".join(c.modality_class for c in at.CLASS_LEDGER).lower()
    for required in ("cytotoxic", "inhibitor", "antibod", "conjugate", "bispecific",
                     "cell therapy", "transplant", "vaccine", "radiation", "sanctuary",
                     "surgery", "oncolytic", "cytokine"):
        assert required in text, required


def test_every_ledger_entry_has_exactly_one_of_the_three_statuses():
    for c in at.CLASS_LEDGER:
        assert c.status in (at.IN_PROGRAM, at.EXCLUDED, at.NOT_YET_ASSESSED), c.modality_class
    assert len(at.CLASS_LEDGER) == 16
    assert len(at.classes_in_program()) == 8


# =================================================================================================
# THE FINDING, AND WHAT IT COSTS.
# =================================================================================================

def test_the_intracranial_finding_separates_what_it_shows_from_what_it_does_not():
    d = at.INTRACRANIAL_HSA_IS_NOW_DOCUMENTED_IN_DOGS
    assert "PMID 42038052" in d["citation"]
    assert len(d["what_it_establishes"]) >= 3
    assert len(d["what_it_does_not_establish"]) >= 3
    joined = " ".join(d["what_it_does_not_establish"])
    assert "no survival benefit" in joined
    assert "n=2" in joined
    assert "SOLITARY imaged" in joined


def test_the_regrade_is_recorded_with_the_condition_it_creates():
    """A regrade that only improved the ledger would be the overstatement failure. This one costs a
    new condition, and the entry has to say so."""
    d = at.INTRACRANIAL_HSA_IS_NOW_DOCUMENTED_IN_DOGS
    assert "PARTIALLY CLOSED" in d["the_grading_it_supports"]
    assert "include the brain" in d["the_new_condition_it_exposes"]
    assert "NEW open condition" in d["the_new_condition_it_exposes"]
    assert "did not simply get better" in at.VERDICT["the_net_change_to_the_conjunction"]


def test_the_verdict_names_the_failure_that_prompted_the_rule():
    v = at.VERDICT
    assert "failure 8" in v["the_contrast_that_prompted_the_audit"]
    assert "to-build" in v["the_contrast_that_prompted_the_audit"]
    assert "six" in v["classes_excluded_and_why"]
    assert "two" in v["classes_left_unassessed_and_named_as_such"]


# =================================================================================================
# RULE 14 -- the proxy search.
# =================================================================================================

def test_the_proxy_is_written_down_before_the_search():
    """Rule 14's method: name the measurable proxy, then search THAT. The proxy has to be an
    operational definition, not a restatement of the concept."""
    d = at.RULE_14_PROXY_SEARCH
    proxy = d["the_proxy_written_down_first"]
    assert "microdialysis" in proxy
    assert "PERITUMORAL" in proxy
    assert "not in" in proxy and "enhancing core" in proxy   # where the barrier is already broken
    assert "not a rodent brain:plasma ratio" in proxy


def test_the_exposure_is_measured_in_the_compartment_at_issue():
    found = at.RULE_14_PROXY_SEARCH["what_the_proxy_search_found_for_temozolomide"]
    assert "PMID 19861433" in found["citation"]
    assert "PERITUMORAL" in found["design"]
    assert found["grade"].startswith("MEASURED")
    assert "not an inference INTO the compartment" in found["grade"]


def test_the_unit_conversion_is_derived_not_asserted():
    e = at.tmz_brain_interstitium_exposure()
    # 0.6 ug/mL of a 194.15 g/mol compound is ~3.09 uM.
    assert 3.0 < e["peak_uM"] < 3.2
    lo, hi = e["peak_uM_range_1sd"]
    assert lo < e["peak_uM"] < hi
    assert 1.5 < lo < 1.6 and 4.6 < hi < 4.7
    assert at.ug_per_ml_to_micromolar(0.0) == 0.0


def test_both_ratio_definitions_are_carried_and_they_differ():
    """The paper's 17.8% is a mean of per-patient ratios; the ratio of the mean AUCs is 15.8%.
    Quoting one while computing the other would be an inconsistency hiding in a rounding."""
    e = at.tmz_brain_interstitium_exposure()
    assert abs(e["ratio_of_mean_AUCs"] - 0.158) < 0.002
    assert e["reported_mean_of_per_patient_ratios"] == 0.178
    assert e["ratio_of_mean_AUCs"] != e["reported_mean_of_per_patient_ratios"]
    assert "mean of ratios is not the ratio of means" in at.RULE_14_PROXY_SEARCH[
        "what_the_proxy_search_found_for_temozolomide"]["the_numbers"]


def test_the_criterion_is_reported_as_half_settled_not_cleared():
    """The exposure half is measured; the effect concentration is unpublished. Calling the criterion
    cleared would be the overstatement failure 4 names."""
    d = at.RULE_14_PROXY_SEARCH
    note = d["what_this_settles_and_what_it_does_not"]
    assert "does NOT complete the criterion" in note
    assert "not published" in note
    assert "PMID 34085099" in note          # including in the paper that reports the synergy


def test_the_in_vitro_comparison_is_explicitly_rejected_as_the_wrong_test():
    note = at.RULE_14_PROXY_SEARCH["and_an_in_vitro_comparison_would_be_the_wrong_test_anyway"]
    assert "schedule-dependent" in note
    assert "MGMT" in note
    assert "not a replacement for it" in note


def test_the_failed_half_of_the_proxy_search_is_reported():
    """Rule 14 is a method, not a guarantee. Lomustine's proxy search found nothing, and reporting
    that is what keeps the method honest rather than decorative."""
    note = at.RULE_14_PROXY_SEARCH["where_the_proxy_search_FAILED"]
    assert note.startswith("lomustine")
    assert "returns nothing" in note
    assert "reach, not exposure" in note
    assert "Lomustine does not" in at.RULE_14_PROXY_SEARCH["the_net_effect_on_the_ledger"]
