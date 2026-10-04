"""Sanity + fidelity checks for the conversation-sourced disease module."""

from __future__ import annotations

from canine_dsp import disease as d


def test_module_imports_and_is_documented():
    assert d.__doc__ and len(d.__doc__) > 100


def test_counts_match_the_populated_tables():
    c = d.counts()
    assert c == {"sites": len(d.SITES), "escapes": len(d.ESCAPES),
                 "mechanisms": len(d.MECHANISMS), "routes": len(d.ROUTES)}
    assert c["sites"] == 4
    assert c["escapes"] == 12  # the ten + MGMT + the germline second primary
    assert c["mechanisms"] >= 5
    assert c["routes"] >= 5


def test_escapes_are_numbered_one_through_twelve_contiguously():
    assert sorted(e.number for e in d.ESCAPES) == list(range(1, 13))
    for e in d.ESCAPES:
        assert isinstance(e.closure, d.Closure)
        assert e.caveat.strip(), e.name  # every escape carries an honest caveat


def test_mgmt_is_made_irrelevant_not_closed():
    """MGMT repair has no lesion to repair under a non-DNA-damaging regimen."""
    mgmt = next(e for e in d.ESCAPES if "MGMT" in e.name.upper())
    assert mgmt.closure is d.Closure.MADE_IRRELEVANT


def test_the_germline_second_primary_is_only_conditionally_addressed():
    """It hinges on an unmeasured CNS access; it must not be sold as closed."""
    germline = next(e for e in d.ESCAPES
                    if "germline" in e.name.lower() or "second" in e.name.lower())
    assert germline.closure is d.Closure.ADDRESSED_CONDITIONAL


def test_occupied_sites_are_the_two_unreachable_ones():
    occ = d.occupied_sites()
    assert all(s.status is d.SiteStatus.OCCUPIED for s in occ)
    assert len(occ) == 2  # invaded parenchyma + leptomeninges/CSF


def test_the_resectable_lump_is_ruled_out():
    assert any(s.status is d.SiteStatus.RULED_OUT for s in d.SITES)


def test_the_intra_arterial_route_is_recorded_as_retracted():
    """Schedule-coherence defect: a monthly procedure's access times a continuous duty."""
    ia = next(r for r in d.ROUTES
              if "arterial" in r.name.lower() or "intra-arterial" in r.name.lower())
    assert "RETRACT" in ia.verdict.name.upper()


def test_final_regimen_is_present():
    assert d.FINAL_REGIMEN is not None
