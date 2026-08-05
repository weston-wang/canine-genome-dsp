import numpy as np
import pandas as pd
import pytest

from canine_dsp.alphafold import (
    align_residue_numbers,
    confidence_band,
    contact_number_burial,
    extract_mutant_peptide,
    find_exposed_linear_epitopes,
    map_variants,
    read_plddt_track,
    whole_sequence_identity,
)

ATOM_SITE_COLUMNS = [
    "group_PDB", "id", "type_symbol", "label_atom_id", "label_alt_id", "label_comp_id",
    "label_asym_id", "label_entity_id", "label_seq_id", "pdbx_PDB_ins_code", "Cartn_x",
    "Cartn_y", "Cartn_z", "occupancy", "B_iso_or_equiv", "pdbx_formal_charge", "auth_seq_id",
    "auth_comp_id", "auth_asym_id", "auth_atom_id", "pdbx_PDB_model_num",
]


def _synthetic_cif(path, n_residues=32):
    plddt = 60 + 30 * np.sin(2 * np.pi * np.arange(n_residues) / 8)
    lines = ["data_TEST", "#", "loop_"]
    lines += [f"_atom_site.{name}" for name in ATOM_SITE_COLUMNS]
    for i in range(n_residues):
        seq = i + 1
        lines.append(f"ATOM {2 * i + 1} N N . ALA A 1 {seq} ? {i:.3f} 0.000 0.000 1.00 "
                     f"{plddt[i]:.2f} ? {seq} ALA A N 1")
        lines.append(f"ATOM {2 * i + 2} C CA . ALA A 1 {seq} ? {i + .5:.3f} 1.000 2.000 1.00 "
                     f"{plddt[i]:.2f} ? {seq} ALA A CA 1")
    lines.append("#")
    path.write_text("\n".join(lines) + "\n")
    return plddt


def test_read_plddt_track_extracts_ca_atoms_only(tmp_path):
    cif = tmp_path / "test.cif"
    plddt = _synthetic_cif(cif)
    track = read_plddt_track(cif)
    assert list(track["residue_number"]) == list(range(1, 33))
    np.testing.assert_allclose(track["plddt"], plddt, atol=1e-2)
    np.testing.assert_allclose(track["y"], 1.0)


def _synthetic_cif_with_sequence(path, residues):
    plddt = np.linspace(50, 95, len(residues))
    lines = ["data_TEST", "#", "loop_"]
    lines += [f"_atom_site.{name}" for name in ATOM_SITE_COLUMNS]
    for i, resname in enumerate(residues):
        seq = i + 1
        lines.append(f"ATOM {2 * i + 1} N N . {resname} A 1 {seq} ? {i:.3f} 0.000 0.000 1.00 "
                     f"{plddt[i]:.2f} ? {seq} {resname} A N 1")
        lines.append(f"ATOM {2 * i + 2} C CA . {resname} A 1 {seq} ? {i + .5:.3f} 1.000 2.000 1.00 "
                     f"{plddt[i]:.2f} ? {seq} {resname} A CA 1")
    lines.append("#")
    path.write_text("\n".join(lines) + "\n")


def test_read_plddt_track_residue_type_column(tmp_path):
    cif = tmp_path / "seq.cif"
    _synthetic_cif_with_sequence(cif, ["ALA", "GLY", "VAL", "LEU"])
    track = read_plddt_track(cif)
    assert list(track["residue_type"]) == ["A", "G", "V", "L"]


def test_align_residue_numbers_identity_for_identical_sequences():
    seq = "MAGVLKQR"
    mapping = align_residue_numbers(seq, seq)
    assert all(target == source and identical for source, (target, identical) in mapping.items())
    assert len(mapping) == len(seq)


def test_align_residue_numbers_handles_insertion_shift():
    source = "MAGVLKQR"
    target = "MAGXVLKQR"
    mapping = align_residue_numbers(source, target)
    assert mapping[1] == (1, True)
    assert mapping[3] == (3, True)
    assert mapping[4] == (5, True)
    assert mapping[8] == (9, True)


def test_whole_sequence_identity_perfect_match():
    seq = "MAGVLKQR"
    stats = whole_sequence_identity(seq, seq)
    assert stats["aligned_positions"] == len(seq)
    assert stats["identical_positions"] == len(seq)
    assert stats["identity_fraction_of_aligned"] == 1.0
    assert stats["identity_fraction_of_source_length"] == 1.0


def test_whole_sequence_identity_partial_match_with_substitution():
    source = "MAGVLKQR"
    target = "MAGVLKQX"  # last residue substituted -- a real mismatch, not just an insertion
    stats = whole_sequence_identity(source, target)
    assert stats["source_length"] == stats["target_length"] == 8
    assert stats["aligned_positions"] == 8
    assert stats["identical_positions"] == 7
    assert stats["identity_fraction_of_aligned"] == pytest.approx(7 / 8)
    assert stats["identity_fraction_of_source_length"] == pytest.approx(7 / 8)


def test_read_plddt_track_missing_loop_raises(tmp_path):
    cif = tmp_path / "empty.cif"
    cif.write_text("data_TEST\n#\n")
    with pytest.raises(ValueError):
        read_plddt_track(cif)


def test_confidence_band_thresholds():
    assert confidence_band(95) == "very_high"
    assert confidence_band(70) == "confident"
    assert confidence_band(55) == "low"
    assert confidence_band(10) == "very_low"


def test_extract_mutant_peptide_substitutes_at_correct_position(tmp_path):
    cif = tmp_path / "seq.cif"
    residues = ["ALA"] * 20
    residues[14] = "GLU"  # position 15 (1-based)
    _synthetic_cif_with_sequence(cif, residues)
    track = read_plddt_track(cif)
    peptide = extract_mutant_peptide(track, position=15, wt_residue="E", mut_residue="K", flank=5)
    assert peptide == "AAAAAKAAAAA"


def test_extract_mutant_peptide_rejects_wrong_wildtype(tmp_path):
    cif = tmp_path / "seq.cif"
    _synthetic_cif_with_sequence(cif, ["ALA"] * 20)
    track = read_plddt_track(cif)
    with pytest.raises(ValueError):
        extract_mutant_peptide(track, position=10, wt_residue="E", mut_residue="K", flank=3)


def test_extract_mutant_peptide_rejects_window_running_off_structure(tmp_path):
    cif = tmp_path / "seq.cif"
    _synthetic_cif_with_sequence(cif, ["ALA"] * 10)
    track = read_plddt_track(cif)
    with pytest.raises(ValueError):
        extract_mutant_peptide(track, position=2, wt_residue="A", mut_residue="K", flank=5)


def test_map_variants_reports_local_window_and_missing_positions(tmp_path):
    cif = tmp_path / "test.cif"
    _synthetic_cif(cif)
    track = read_plddt_track(cif)
    variants = pd.DataFrame({"gene": ["GENE_A", "GENE_B"], "protein_position": [10, 1000]})
    mapped = map_variants(track, variants, flank=2)
    assert mapped.loc[0, "confidence_band"] in {"very_high", "confident", "low", "very_low"}
    expected_local_mean = track.set_index("residue_number")["plddt"].reindex(range(8, 13)).mean()
    assert mapped.loc[0, "local_mean_plddt"] == pytest.approx(expected_local_mean)
    assert pd.isna(mapped.loc[1, "confidence_band"])
    assert np.isnan(mapped.loc[1, "plddt"])


def test_contact_number_burial_ranks_isolated_residue_as_least_contacted():
    track = pd.DataFrame({
        "residue_number": [1, 2, 3, 4],
        "residue_type": list("ABCD"),
        "plddt": [90.0, 90.0, 90.0, 90.0],
        "x": [0.0, 1.0, 0.0, 100.0],
        "y": [0.0, 0.0, 1.0, 100.0],
        "z": [0.0, 0.0, 0.0, 100.0],
    })
    result = contact_number_burial(track, radius=10.0)
    # A, B, C sit within 1-1.4 A of each other (radius=10 covers all pairs among them);
    # D sits ~173 A away from the cluster, so it should have zero contacts -- the most
    # solvent-exposed residue -- while A/B/C each see the other two.
    contacts = result.set_index("residue_number")["contact_number"]
    assert contacts[4] == 0
    assert contacts[1] == contacts[2] == contacts[3] == 2


def test_find_exposed_linear_epitopes_picks_lowest_contact_nonoverlapping_windows():
    track = pd.DataFrame({
        "residue_number": list(range(1, 13)),
        "residue_type": list("ABCDEFGHIJKL"),
        "plddt": [80.0] * 12,
        "contact_number": [9, 9, 1, 1, 1, 9, 9, 9, 2, 2, 2, 9],
        "x": np.zeros(12), "y": np.zeros(12), "z": np.zeros(12),
    })
    top_one = find_exposed_linear_epitopes(track, window=3, top_n=1)
    assert len(top_one) == 1
    assert (top_one.loc[0, "start_residue"], top_one.loc[0, "end_residue"]) == (3, 5)
    assert top_one.loc[0, "sequence"] == "CDE"
    assert top_one.loc[0, "mean_contact_number"] == pytest.approx(1.0)

    top_two = find_exposed_linear_epitopes(track, window=3, top_n=2)
    assert len(top_two) == 2
    windows = set(zip(top_two["start_residue"], top_two["end_residue"]))
    # The second-lowest-contact window (residues 9-11, mean=2.0) is far enough from the
    # first (residues 3-5) not to overlap, so both should be returned rather than the
    # window search collapsing onto near-duplicates of the same low-contact stretch.
    assert windows == {(3, 5), (9, 11)}


def test_find_exposed_linear_epitopes_rejects_window_longer_than_structure():
    track = pd.DataFrame({
        "residue_number": [1, 2, 3],
        "residue_type": list("ABC"),
        "plddt": [80.0, 80.0, 80.0],
        "contact_number": [1, 2, 3],
        "x": np.zeros(3), "y": np.zeros(3), "z": np.zeros(3),
    })
    with pytest.raises(ValueError):
        find_exposed_linear_epitopes(track, window=5, top_n=1)
