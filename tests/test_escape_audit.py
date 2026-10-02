"""The independent escape audit must stay honest: every new gap closed, nothing silently assumed."""

from canine_dsp import disease, escape_audit as ea
from canine_dsp.core.evidence import Provenance


def test_every_new_gap_is_closed_or_explicitly_folded():
    """A gap with no closure record and no fold-in would be an open hole presented as an audit."""
    gaps = {c.tag for c in ea.new_gaps()}
    closed = {n.tag for n in ea.NEW_ESCAPE_CLOSURES}
    folded = {"A1", "A5"}
    assert gaps - folded == closed
    assert folded < gaps  # the folded ones are real gaps, not dropped


def test_no_new_closure_rests_on_a_bare_assumption():
    """The audit may not import the failure mode it exists to catch."""
    for n in ea.NEW_ESCAPE_CLOSURES:
        assert n.provenance in (Provenance.MEASURED, Provenance.TRANSFERRED, Provenance.DERIVED)
        assert n.decisive_experiment.strip()


def test_mapped_candidates_point_at_real_escapes():
    known = {e.number for e in disease.ESCAPES}
    for c in ea.CANDIDATES:
        if c.maps_to is not None:
            assert c.maps_to in known


def test_audited_count_exceeds_the_original_twelve():
    """The audit's whole point is that the list in hand was incomplete."""
    assert ea.audited_escape_count() == len(disease.ESCAPES) + len(ea.load_bearing_gaps())
    assert ea.audited_escape_count() > len(disease.ESCAPES)


def test_the_single_agent_dependency_is_stated():
    """The audit's main result is structural; it must not be buried."""
    s = ea.single_agent_dependency()
    assert "microtubule" in s.lower()
    assert "ABCB1" in s or "efflux" in s.lower()


def test_tally_covers_every_candidate():
    assert sum(ea.tally().values()) == len(ea.CANDIDATES)


def test_every_candidate_names_a_source_and_a_rationale():
    for c in ea.CANDIDATES:
        assert c.rationale.strip()
        assert c.mechanism.strip()
