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
