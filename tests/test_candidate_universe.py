"""Rule 9: a closure claim is only as good as the stated candidate universe behind it."""

from canine_dsp import candidate_universe as cu, escape_audit as ea


def test_no_modality_class_is_left_unassessed_SILENTLY():
    """The failure this module exists to prevent: claiming closure over a list with holes in it.

    History, because it is the point. This was `cu.not_assessed() == []` twice over. The 2026-10-31
    sweep found a class the universe had never enumerated (live bacterial vector) while a funded dog
    trial in THIS disease was already using it; it was carried as a declared hole for a day, then
    EXCLUDED on a derived site mismatch, and the assertion went back to `== []`.

    Then the 2026-11-01 sweep found two more rows that had never existed, and one of them --
    antimetabolites -- cannot be excluded on any admissible ground and cannot be called in-model
    without an agent wired into the regimen. At that point `== []` stopped being an invariant and
    started being a thing to satisfy, which is the failure mode in miniature: the test would have
    pushed towards grading the class rather than reporting it.

    So the invariant is restated as what it always meant: no hole may be SILENT. Every open class
    must be declared in KNOWN_OPEN_CLASSES, which `candidate_universe._validate()` enforces at
    import and which the published catalogue line must match. The count of open classes is pinned
    separately, in `test_the_catalogue_count_and_the_open_count_are_what_the_docs_say`, so a change
    to it fails loudly instead of passing quietly.
    """
    undeclared = [m.name for m in cu.not_assessed() if m.name not in cu.KNOWN_OPEN_CLASSES]
    assert undeclared == [], undeclared
    stale = [n for n in cu.KNOWN_OPEN_CLASSES
             if n not in {m.name for m in cu.not_assessed()}]
    assert stale == [], stale


def test_the_bacterial_vector_class_is_excluded_on_a_site_mismatch_not_on_absent_canine_data():
    """Rule 13: the ground must be scientific. This one is a derived mismatch between a documented
    hypoxia-driven tropism and a target site that is the least hypoxic part of the tumour."""
    m = next(x for x in cu.UNIVERSE if x.name.startswith("live bacterial vector"))
    assert m.status is cu.Status.EXCLUDED
    assert m.exclusion_ground is cu.ExclusionGround.KILL_CONTRADICTED
    for phrase in ("HYPOXIA", "INVADING EDGE BEHIND AN INTACT BARRIER", "WHAT WOULD REOPEN IT",
                   "hitchhiking"):
        assert phrase in m.basis, phrase
    # the exclusion must stay falsifiable and must not rest on missing dog data
    assert "NON-ENHANCING" in m.basis
    assert m in cu.excluded()
    assert cu.excluded_citing_absent_canine_data() == []


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


def test_the_two_ablative_device_modalities_are_assessed_with_a_stated_reason():
    """Histotripsy and H-FIRE were named only on a superseded page. Rule 13: a modality may be set
    aside for a scientific reason, never for absent canine data -- here, both need a cranial defect
    in the dog and neither gives continuous presence."""
    m = next(x for x in cu.UNIVERSE if x.name == "sanctuary-site / local delivery")
    assert "HISTOTRIPSY" in m.representative and "H-FIRE" in m.representative
    assert "cranial defect" in m.representative or "craniotomy" in m.representative
    assert cu.excluded_citing_absent_canine_data() == []


def test_the_antimetabolite_class_is_enumerated_and_carried_open():
    """The second rule-9 hole, found 2026-11-01. Three members are measured active in all ten
    canine HS lines, so the class cannot be dismissed; no single member carries potency, brain
    access and tolerability together, so it cannot be closed either. It must therefore be OPEN --
    and declared, so the import-time guard stays loud about it."""
    m = next(x for x in cu.UNIVERSE if "antimetabolite" in x.name)
    assert m.status is cu.Status.NOT_ASSESSED
    assert m.name in cu.KNOWN_OPEN_CLASSES
    assert m.exclusion_ground is None, "an open class must not carry an exclusion ground"
    assert m.availability is cu.Availability.EXISTS_TODAY
    assert m.canine_hs_evidence.startswith("MEASURED")
    # the three members and the leg each one fails
    for token in ("5-fluorouracil", "clofarabine", "cytarabine", "floxuridine"):
        assert token.lower() in m.basis.lower() or token.lower() in m.canine_hs_evidence.lower()
    assert "15206584" in m.basis, "the dog-cerebrum vacuolation finding is what disqualifies 5-FU"
    assert "1742843" in m.basis, "the measured canine CSF:plasma 0.62 is what keeps it open"
    assert "42126265" in m.basis, "clofarabine's LCH durability readout"


def test_the_open_class_does_not_become_a_failing_input():
    """Rule 11 keeps two axes apart: `standard_audit.failing()` grades the inputs the model USES,
    while rule 9 grades the candidate list the claim is quantified OVER. An unenumerated class is
    the second kind. Collapsing them would re-grade a live input against demonstration."""
    from canine_dsp import standard_audit
    assert standard_audit.failing() == [] or all(
        "antimetabolite" not in str(f).lower() for f in standard_audit.failing()
    )


def test_the_fgfr_axis_is_excluded_on_brain_tumour_data_not_on_absent_canine_data():
    """Found in the same sweep and it closes out: the licensed members exist, the canine signal is
    real, and the class still fails -- in human recurrent glioma, in the biomarker this tumour
    actually has."""
    m = next(x for x in cu.UNIVERSE if "FGFR" in x.name)
    assert m.status is cu.Status.EXCLUDED
    assert m.exclusion_ground is cu.ExclusionGround.KILL_CONTRADICTED
    assert m.availability is cu.Availability.EXISTS_TODAY
    assert "35344029" in m.basis, "the infigratinib glioma phase 2 is the ground"
    assert "212018" in m.availability_basis and "213736" in m.availability_basis
    assert m in cu.newly_assessed()
    assert cu.excluded_citing_absent_canine_data() == []


def test_the_catalogue_count_and_the_open_count_are_what_the_docs_say():
    """The published line moved from '26 -- 15/11/0 unassessed' to '28 -- 15/12/1 open'. If this
    test fails, three documents and a reader-facing page are now lying."""
    t = cu.tally()
    assert len(cu.UNIVERSE) == 28
    assert t["IN_MODEL"] == 15
    assert t["EXCLUDED"] == 12
    assert t["NOT_ASSESSED"] == 1
    claim = cu.closure_claim(ea.audited_escape_count())
    assert "28 modality classes" in claim
    assert "1 unassessed" in claim


def test_c3_records_the_maintenance_pincer_at_the_strength_shown():
    """Rule 5: the 75% relapse figure CONFIRMS C3 and the 60% discontinuation figure pressures it.
    Both are human and indirect, and the answer to the second is structural, not demonstrated."""
    from canine_dsp import deterministic_closure as dc
    c3 = next(c for c in dc.CONDITIONS if c.tag == "C3")
    blob = " ".join(str(v) for v in vars(c3).values())
    assert "41178439" in blob
    assert "75%" in blob and "60%" in blob
    assert "structural, not demonstrated" in blob
