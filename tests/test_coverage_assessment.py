from canine_dsp import coverage_assessment as cov
from canine_dsp import disease


def test_every_escape_has_exactly_one_grade():
    graded = [c.escape_number for c in cov.COVERAGE]
    assert sorted(graded) == [e.number for e in disease.ESCAPES]
    assert len(graded) == len(set(graded)) == 12


def test_tally_sums_to_the_escape_count():
    t = cov.tally()
    assert sum(t.values()) == len(cov.COVERAGE) == 12


def test_no_escape_rests_on_a_bare_assumption():
    """Under the model-based standard every escape is now closed on a real basis -- measured,
    transferred, model-derived, or a structural design argument -- so none may be graded ASSUMED.
    If a future edit reintroduces a bare assumption, this fails and forces re-justification."""
    assert cov.assumed() == []
    assert cov.tally()["ASSUMED"] == 0


def test_the_canine_hs_measured_set_is_exactly_the_position_independent_and_direct_lines():
    """Measured-in-canine-HS = the position-independent microtubule cytotoxic (escapes 1-3, 6, 8),
    liposomal clodronate (5) and NF-kB/parthenolide (7). Each must cite its source, not assert."""
    canine = {c.escape_number for c in cov.measured_in_canine_hs()}
    assert canine == {1, 2, 3, 5, 6, 7, 8}
    for c in cov.COVERAGE:
        if c.escape_number in (1, 2, 3, 6, 8):
            assert "25715778" in c.key_number_status  # the canine-HS cytotoxicity paper
    e5 = next(c for c in cov.COVERAGE if c.escape_number == 5)
    assert "19760220" in e5.key_number_status
    # escape 8 must record that the counter-indicated ferroptosis inducer was dropped
    e8 = next(c for c in cov.COVERAGE if c.escape_number == 8)
    assert "DROPPED" in e8.closing_agent or "dropped" in e8.key_number_status.lower()


def test_the_ten_year_arm_is_model_derived_and_conditional_on_mtap():
    """Escape 12 (PRMT5i maintenance) is now MODEL-DERIVED (kill computed by pkpd from grounded
    inputs), but its closure stays conditional on MTAP-deleted status -- not a bare assumption,
    and not an unqualified measurement."""
    e12 = next(c for c in cov.COVERAGE if c.escape_number == 12)
    assert e12.backing is cov.Backing.MODEL_DERIVED
    assert e12.backing.is_evidence_backed
    assert cov.model_derived() == [e12]
    # the MTAP falsifier must remain the named gate
    assert "MTAP" in e12.decisive_experiment
    assert "MTAP" in e12.key_number_status


def test_decisive_experiments_are_offered_and_deduplicated():
    experiments = cov.decisive_experiments()
    assert experiments  # non-empty
    assert len(experiments) == len(set(experiments))
    # the cheapest falsifier -- the MTAP stain -- must be among them
    assert any("MTAP" in x for x in experiments)


def test_honest_statement_names_residuals_not_just_closure():
    """The verdict must not read as an unqualified 'solved': it states every escape is addressed on
    a real basis AND names the quantitative residuals (kill rates, delivery, growth bar, MTAP)."""
    statement = cov.honest_coverage_statement()
    assert "12" in statement
    assert "model-derived" in statement.lower()
    assert "residual" in statement.lower()
    assert "MTAP" in statement


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
