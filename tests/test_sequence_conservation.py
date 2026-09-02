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


def test_pgp_gates_delivery_and_is_far_below_the_kinase_targets():
    """The report's delivery caveat rests on P-gp being much less conserved than the kinase
    targets an inhibitor must fit -- so a fit that transfers does not mean penetration does."""
    pgp = CONSERVATION["ABCB1"]
    assert pgp.identity_percent == pytest.approx(91.08, abs=0.05)
    assert pgp.identity_fraction < CONSERVATION["MAPK1"].identity_fraction
    assert pgp.identity_fraction < CONSERVATION["PIK3CA"].identity_fraction


def test_pd1_is_the_lowest_and_warns_against_antibody_transfer():
    """PD-1/PDCD1 is the least-conserved target overall -- an antibody target, not a pocket. Its
    low identity is why the immune arm needs a caninized antibody, not a human one."""
    pd1 = CONSERVATION["PDCD1"]
    assert pd1.identity_percent == pytest.approx(67.72, abs=0.1)
    assert all(pd1.identity_fraction <= rec.identity_fraction for rec in CONSERVATION.values())
    assert "caninized" in pd1.note.lower()


def test_csf1r_is_the_lowest_small_molecule_kinase_target():
    """Among the small-molecule kinase targets, CSF1R is the least conserved -- so a human CSF1R
    inhibitor's transfer is the least certain of those, consistent with deprioritizing that arm."""
    kinase_targets = ("MAPK1", "PIK3CA", "MAP2K1", "PRMT5", "CDK4", "CDK6", "CSF1R")
    csf1r = CONSERVATION["CSF1R"]
    assert csf1r.identity_percent == pytest.approx(85.30, abs=0.05)
    assert all(csf1r.identity_fraction <= CONSERVATION[g].identity_fraction for g in kinase_targets)


def test_transfer_set_covers_the_kinase_targets_but_not_the_low_ones():
    # everything at/above 0.90 -- all targets except CSF1R (0.853) and PD-1 (0.677)
    supported = orthologs_supporting_transfer(threshold=0.90)
    assert set(supported) == {"MAPK1", "PIK3CA", "ABCB1", "MAP2K1", "PRMT5", "CDK4", "CDK6", "TUBB"}
    assert "CSF1R" not in supported and "PDCD1" not in supported
    # raise the bar to 0.95: the near-identical inhibitor targets remain; P-gp drops out
    strict = set(orthologs_supporting_transfer(threshold=0.95))
    assert strict == {"MAPK1", "PIK3CA", "MAP2K1", "PRMT5", "CDK4", "CDK6", "TUBB"}
    assert "ABCB1" not in strict


def test_the_maintenance_targets_are_high_conservation():
    """The MEK / PRMT5 / CDK4/6 maintenance-arm targets should all be >=97% identical, so the
    target-fit half of those arms is computed fact, not assumption."""
    for gene in ("MAP2K1", "PRMT5", "CDK4", "CDK6"):
        assert CONSERVATION[gene].identity_fraction >= 0.97


def test_records_are_frozen():
    rec = CONSERVATION["MAPK1"]
    assert isinstance(rec, OrthologConservation)
    with pytest.raises(FrozenInstanceError):
        rec.identical_positions = 0  # type: ignore[misc]
