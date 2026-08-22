from dataclasses import FrozenInstanceError

import pytest

from canine_dsp.sequence_conservation import (
    CONSERVATION,
    OrthologConservation,
    orthologs_supporting_transfer,
)


def test_every_record_is_internally_consistent():
    """identity_fraction must equal identical/aligned, and counts must be sane -- the cached
    numbers cannot silently drift away from their own definition."""
    for rec in CONSERVATION.values():
        assert 0 < rec.identical_positions <= rec.aligned_positions
        assert rec.aligned_positions <= min(rec.human_length, rec.dog_length)
        assert rec.identity_fraction == pytest.approx(
            rec.identical_positions / rec.aligned_positions
        )
        # provenance must be present so a figure can always be traced back and re-verified
        assert rec.human_accession and rec.dog_accession
        assert rec.aligner and rec.computed_on


def test_erk2_is_fully_identical():
    rec = CONSERVATION["MAPK1"]
    assert (rec.human_accession, rec.dog_accession) == ("P28482", "A0A8I3PZP0")
    assert rec.aligned_positions == 360
    assert rec.identical_positions == 360
    assert rec.identity_fraction == 1.0
    assert rec.differing_positions == ()


def test_pi3k_alpha_atp_pocket_is_identical():
    """The '99.81%, identical ATP pocket' claim: both differences must lie OUTSIDE the
    kinase/ATP-binding domain (~697-1068), or the pocket claim is unsupported."""
    rec = CONSERVATION["PIK3CA"]
    assert rec.identical_positions == 1066
    assert rec.aligned_positions == 1068
    assert rec.identity_percent == pytest.approx(99.81, abs=0.01)
    positions = [pos for pos, _, _ in rec.differing_positions]
    assert positions == [532, 535]
    assert all(pos < 697 for pos in positions), "a difference falls inside the ATP-binding domain"


def test_pgp_is_the_least_conserved_and_gates_delivery():
    """P-gp must remain the lowest-identity target -- the report's delivery caveat rests on it
    being the one divergence that matters."""
    pgp = CONSERVATION["ABCB1"]
    assert pgp.identity_percent == pytest.approx(91.08, abs=0.05)
    others = [rec.identity_fraction for gene, rec in CONSERVATION.items() if gene != "ABCB1"]
    assert all(pgp.identity_fraction < o for o in others)


def test_transfer_set_covers_the_targets_but_flags_nothing_below_threshold():
    supported = orthologs_supporting_transfer(threshold=0.90)
    assert set(supported) == {"MAPK1", "PIK3CA", "ABCB1"}
    # raise the bar above P-gp: only the two near-identical kinase targets should remain
    assert set(orthologs_supporting_transfer(threshold=0.95)) == {"MAPK1", "PIK3CA"}


def test_records_are_frozen():
    rec = CONSERVATION["MAPK1"]
    assert isinstance(rec, OrthologConservation)
    with pytest.raises(FrozenInstanceError):
        rec.identical_positions = 0  # type: ignore[misc]
