"""Rule 9: a closure claim is only as good as the stated candidate universe behind it."""

from canine_dsp import candidate_universe as cu, escape_audit as ea


def test_no_modality_class_is_left_unassessed():
    """The failure this module exists to prevent: claiming closure over a list with holes in it."""
    assert cu.not_assessed() == []


def test_every_excluded_class_records_a_reason():
    """'Excluded' without a reason is just 'not assessed' with better manners."""
    for m in cu.excluded():
        assert len(m.basis) > 40
        assert m.representative.strip()


def test_the_classes_rule_9_names_are_all_present():
    """CLAUDE.md rule 9 lists the minimum modality classes for cancer work."""
    names = " ".join(m.name.lower() for m in cu.UNIVERSE)
    for required in ("cytotoxic", "targeted", "antibod", "bispecific", "cell therapy",
                     "transplant", "vaccine", "cytokine", "radiation", "sanctuary"):
        assert required in names, required


def test_transplant_is_excluded_on_biology_not_availability():
    """A feasibility exclusion is weak; this one has to rest on the microglial origin argument."""
    t = next(m for m in cu.UNIVERSE if "transplant" in m.name)
    assert t.status is cu.Status.EXCLUDED
    assert "yolk" in t.basis.lower()
    assert "lymphoma" in t.canine_hs_evidence.lower()  # feasibility is conceded, not the reason


def test_closure_claim_states_the_catalogue_size_and_the_exclusions():
    claim = cu.closure_claim(ea.audited_escape_count())
    assert str(len(cu.UNIVERSE)) in claim
    assert str(ea.audited_escape_count()) in claim
    assert "excluded" in claim.lower()


def test_tally_covers_every_class():
    assert sum(cu.tally().values()) == len(cu.UNIVERSE)


def test_some_classes_carry_canine_hs_measurements():
    """If nothing were measured in this disease the universe would be pure speculation."""
    assert len(cu.with_canine_hs_evidence()) >= 5


# --- rule 13: exclusions need a scientific ground, and availability is a separate axis ------------

def test_no_class_is_excluded_for_absent_canine_data():
    """CLAUDE.md rule 13 and failure 8. The lapse this lint exists to catch, in one assertion."""
    assert cu.excluded_citing_absent_canine_data() == []


def test_every_exclusion_carries_an_admissible_ground():
    """Rule 13 allows exactly three grounds. _validate() enforces it; this pins the behaviour."""
    for m in cu.excluded():
        assert m.exclusion_ground in set(cu.ExclusionGround), m.name


def test_no_ground_is_recorded_on_a_class_that_is_in_the_model():
    for m in cu.in_model():
        assert m.exclusion_ground is None, m.name


def test_every_ground_is_actually_used():
    """If a ground has no members, the enum is aspirational rather than descriptive."""
    for ground, members in cu.excluded_by_ground().items():
        assert members, f"{ground} has no members"


def test_availability_is_independent_of_status():
    """The point of the rule-13 split: obtainable classes get excluded, and model classes can be
    near-future."""
    assert any(m.availability is cu.Availability.EXISTS_TODAY for m in cu.excluded())
    assert any(m.availability is cu.Availability.NEAR_FUTURE for m in cu.in_model())


def test_no_modality_class_in_the_model_is_theoretical():
    """Rule 13 after the user's clarification: near-future counts, theoretical never does."""
    assert cu.theoretical_in_model() == []


def test_transplant_is_the_exists_today_exclusion_that_proves_the_point():
    t = next(m for m in cu.UNIVERSE if "transplant" in m.name)
    assert t.availability is cu.Availability.EXISTS_TODAY
    assert t.exclusion_ground is cu.ExclusionGround.KILL_CONTRADICTED


def test_the_epigenetic_toxicity_ground_is_computed_not_asserted():
    """Rule 13: where canine data are absent, test against a derived transfer. This is that test."""
    arith = cu.epigenetic_toxicity_arithmetic()
    assert not arith["fits"], "the exclusion claims the budget is blown; the arithmetic must agree"
    assert arith["oversubscribed_axes_if_added"]
    assert "TRANSFERRED" in arith["provenance"]


def test_every_class_records_an_availability_basis():
    for m in cu.UNIVERSE:
        assert len(m.availability_basis) > 20, m.name


def test_availability_tally_covers_every_class():
    assert sum(cu.availability_tally().values()) == len(cu.UNIVERSE)


def test_the_regrounded_exclusions_are_named_in_the_statement():
    """A silent re-grounding is indistinguishable from a cover-up; the statement must say so."""
    assert cu.regrounded_under_rule_13()
    assert "RE-GROUNDED" in cu.statement()


def test_closure_claim_reports_the_availability_split():
    claim = cu.closure_claim(ea.audited_escape_count())
    assert str(len(cu.exists_today_in_model())) in claim
    assert "today" in claim
