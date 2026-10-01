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


def test_surveillance_helps_the_anchored_tier_less_than_the_reroutable_one():
    """REVISED: the MTAP tier is genotype-ANCHORED, not immune. Acquired PRMT5i resistance via MAPK
    reprogramming is documented (DOI 10.64898/2026.04.16.719008), so surveillance genuinely helps it
    too -- just less than it helps a pathway target, which is the honest ordering."""
    mtap_off = _p("MTAP", "Lung / disseminated", with_surveillance=False).p_median
    mtap_on = _p("MTAP", "Lung / disseminated", with_surveillance=True).p_median
    mapk_off = _p("MAPK", "Lung / disseminated", with_surveillance=False).p_median
    mapk_on = _p("MAPK", "Lung / disseminated", with_surveillance=True).p_median
    mtap_lift, mapk_lift = mtap_on - mtap_off, mapk_on - mapk_off
    assert mtap_lift > 0.0                 # not immune to escape -- watching still pays
    assert mtap_lift < mapk_lift           # but less than for a reroutable pathway target


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


def test_csf_reach_failure_is_derived_not_assumed():
    """The CSF prior was a flat 0.70 ASSUMED, written before the bar was computed. It must now be
    DERIVED, and lower, because the pharmacologic term turned out to be the weak one."""
    from canine_dsp.core.evidence import Provenance

    p = em.reach_fail_param("Leptomeninges / CSF")
    assert p.provenance is Provenance.DERIVED
    assert p.center < 0.70
    assert p.lo < p.center < p.hi


def test_csf_terms_name_delivery_as_the_dominant_risk():
    """The point of decomposing the term: the CSF is delivery-limited, not potency-limited."""
    t = em.csf_reach_fail_terms()
    assert t["dominant_term"] == "delivery"
    assert t["delivery_fail"][0] > t["pharmacologic_fail"][0]
    assert t["superseded_assumed_value"] == 0.70
    # combination is a probability, and strictly worse than either term alone
    c = t["combined"][0]
    assert max(t["delivery_fail"][0], t["pharmacologic_fail"][0]) < c < 1.0
