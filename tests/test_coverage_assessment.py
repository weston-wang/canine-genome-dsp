from canine_dsp import coverage_assessment as cov
from canine_dsp import disease


def test_every_escape_has_exactly_one_grade():
    graded = [c.escape_number for c in cov.COVERAGE]
    assert sorted(graded) == [e.number for e in disease.ESCAPES]
    assert len(graded) == len(set(graded)) == 12


def test_tally_sums_to_the_escape_count():
    t = cov.tally()
    assert sum(t.values()) == len(cov.COVERAGE) == 12


def test_the_coverage_claim_is_not_mostly_evidence_backed():
    """The honest headline: most escapes are NOT closed by a real measurement. If a future edit
    quietly upgrades the grades, this test should fail and force a re-justification."""
    backed = cov.evidence_backed()
    assert len(backed) < len(cov.COVERAGE) / 2
    # at most one line may claim canine-HS-measured backing (parthenolide), and its premise is
    # flagged contested in its own record
    canine = cov.measured_in_canine_hs()
    assert len(canine) <= 1
    if canine:
        assert "contested" in canine[0].key_number_status.lower()


def test_the_ten_year_arm_is_not_evidence_backed():
    """Escape 12 (germline second primary / PRMT5i maintenance) carries the ten-year claim; it
    must not be graded as measured while CNS access and MTAP status are unmeasured."""
    e12 = next(c for c in cov.COVERAGE if c.escape_number == 12)
    assert e12.backing is cov.Backing.ASSUMED
    assert not e12.backing.is_evidence_backed
    assert "MTAP" in e12.decisive_experiment


def test_decisive_experiments_are_offered_and_deduplicated():
    experiments = cov.decisive_experiments()
    assert experiments  # non-empty
    assert len(experiments) == len(set(experiments))
    # the cheapest falsifier -- the MTAP stain -- must be among them
    assert any("MTAP" in x for x in experiments)


def test_honest_statement_names_the_structural_verdict():
    statement = cov.honest_coverage_statement()
    assert "hypothesis" in statement.lower() or "structural" in statement.lower()
    assert "12" in statement
