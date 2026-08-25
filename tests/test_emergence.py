from canine_dsp import emergence as em


def _p(genotype_prefix, site_name, with_surveillance=False):
    grid = em.probabilistic_grid(with_surveillance=with_surveillance, draws=8000)
    return next(d for d in grid
               if d.scenario.genotype.startswith(genotype_prefix)
               and d.scenario.site == site_name)


def test_probabilities_are_valid_and_bounded():
    for d in em.probabilistic_grid(draws=6000):
        assert 0.0 <= d.p_lo <= d.p_median <= d.p_hi <= 1.0


def test_lock_beats_reroutable_at_the_same_site():
    lung = "Lung / disseminated"
    assert _p("MTAP", lung).p_median > _p("MAPK", lung).p_median


def test_floor_tier_is_the_weakest():
    lung = "Lung / disseminated"
    floor = _p("None targetable", lung).p_median
    assert floor < _p("MTAP", lung).p_median
    assert floor < _p("MAPK", lung).p_median


def test_reach_gap_makes_csf_worse_than_lung_even_when_locked():
    """The lock does not help if the drug is not present: CSF (reach-limited) scores below lung for
    the same locked genotype -- the model reproduces 'the CSF is the residual gap'."""
    assert _p("MTAP", "Leptomeninges / CSF").p_median < _p("MTAP", "Lung / disseminated").p_median


def test_surveillance_lifts_the_reroutable_tier():
    lift = em.surveillance_lift(draws=8000)
    assert lift["absolute_lift"] > 0.05  # detect-and-switch measurably raises P for MAPK


def test_surveillance_barely_moves_the_lock():
    """A locked tier needs no watching, so surveillance should add little -- unlike the reroutable one."""
    off = _p("MTAP", "Lung / disseminated", with_surveillance=False).p_median
    on = _p("MTAP", "Lung / disseminated", with_surveillance=True).p_median
    assert abs(on - off) < 0.05


def test_negative_margin_collapses_to_the_no_maintenance_floor():
    """Integrity: if the derived margin is <= 0 the founding cell is supercritical and P must fall to
    roughly the no-maintenance floor exp(-Lambda), not stay high."""
    good = em.assess(em.Scenario("test", "Lung / disseminated", "REROUTABLE", False, 0.5), draws=8000)
    bad = em.assess(em.Scenario("test", "Lung / disseminated", "REROUTABLE", False, -0.1), draws=8000)
    assert bad.p_median < good.p_median
    assert bad.p_median < 0.35  # near exp(-Lambda) with Lambda ~ 1.6


def test_value_of_information_is_ranked_and_normalised():
    d = _p("MAPK", "Lung / disseminated")
    assert d.voi  # non-empty
    shares = [s for _, s in d.voi]
    assert shares == sorted(shares, reverse=True)          # ranked descending
    assert all(0.0 <= s <= 1.0 for s in shares)            # variance shares are fractions


def test_headline_states_probabilities_and_stays_honest():
    h = em.headline(draws=6000).lower()
    assert "90% ci" in h or "ci" in h
    assert "locked" in h
    assert "not proof" in h or "not proof of a decade" in h
