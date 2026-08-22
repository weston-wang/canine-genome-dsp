from canine_dsp import coverage_assessment as cov
from canine_dsp import disease


def test_every_escape_has_exactly_one_grade():
    graded = [c.escape_number for c in cov.COVERAGE]
    assert sorted(graded) == [e.number for e in disease.ESCAPES]
    assert len(graded) == len(set(graded)) == 12


def test_tally_sums_to_the_escape_count():
    t = cov.tally()
    assert sum(t.values()) == len(cov.COVERAGE) == 12


def test_coverage_is_still_not_fully_evidence_backed():
    """The honest headline: the induction backbone (microtubule class, escapes 1-3), lineage
    depletion (clodronate, escape 5) and NF-kB (7) are now measured in canine HS, but a real
    share still is not -- and the ten-year arm remains assumed. If a future edit claims full
    backing, this fails and forces re-justification."""
    backed = cov.evidence_backed()
    assert len(backed) < len(cov.COVERAGE)  # never all twelve
    canine = {c.escape_number for c in cov.measured_in_canine_hs()}
    # microtubule cytotoxic (1-3), liposomal clodronate (5), NF-kB (7) are the canine-HS-measured
    assert canine == {1, 2, 3, 5, 7}
    # escapes 1-3 must cite the canine-HS cytotoxicity paper, not merely assert
    for c in cov.COVERAGE:
        if c.escape_number in (1, 2, 3):
            assert "25715778" in c.key_number_status
    # escape 5 must cite the canine-HS liposomal-clodronate study, not merely assert
    e5 = next(c for c in cov.COVERAGE if c.escape_number == 5)
    assert "19760220" in e5.key_number_status
    # the ten-year arm (escape 12) is still NOT evidence-backed
    e12 = next(c for c in cov.COVERAGE if c.escape_number == 12)
    assert not e12.backing.is_evidence_backed


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


def test_every_maintenance_tier_is_graded_and_cited():
    assert len(cov.MAINTENANCE_TIERS) == 5
    for m in cov.MAINTENANCE_TIERS:
        assert m.citation
        assert m.canine_hs_evidence
        assert m.key_gap  # every tier keeps its honest caveat


def test_the_two_commonest_tiers_have_canine_hs_backing():
    """The upgrade: MAPK-majority and floor tiers rest on measured canine-HS drug response, not
    assumptions. If a future edit downgrades them, this fails and forces a re-check."""
    canine = cov.maintenance_measured_in_canine_hs()
    genotypes = " ".join(m.genotype for m in canine).lower()
    assert "mapk" in genotypes  # the ~59% majority
    assert len(canine) == 2
    # the MAPK tier must cite the cobimetinib canine-HS response paper
    mapk = next(m for m in cov.MAINTENANCE_TIERS if "MAPK" in m.genotype)
    assert "39202410" in mapk.citation


def test_mtap_tier_is_a_transfer_not_canine_measured():
    """MTAP/PRMT5i has no canine-HS data; it must not be graded as canine-measured."""
    mtap = next(m for m in cov.MAINTENANCE_TIERS if "MTAP" in m.genotype)
    assert mtap.backing is cov.Backing.MEASURED_OTHER
    assert "no canine-hs data" in mtap.key_gap.lower()


def test_maintenance_tally_sums_and_statement_is_honest():
    assert sum(cov.maintenance_tally().values()) == len(cov.MAINTENANCE_TIERS)
    statement = cov.maintenance_statement()
    assert "measured in canine hs" in statement.lower()
    assert "unmeasured" in statement
