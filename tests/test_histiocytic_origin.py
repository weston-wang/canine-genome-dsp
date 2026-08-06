import numpy as np
import pytest

from canine_dsp.histiocytic_origin import (
    AA_HYDROPATHY,
    CANDIDATE_DRIVERS,
    VERIFIED_HOTSPOT_CONTROLS,
    hotspot_salience,
    hydropathy_track,
    permutation_pvalue,
)
from canine_dsp.spectral import bicoherence


def test_candidate_panel_covers_all_four_reasoning_tiers():
    """The tiers are the actual output of the inference chain, not a confidence score: A =
    precedented in canine HS, B = dominant in human histiocytosis but untested in dogs, C =
    predicted specifically by the tissue-resident-macrophage hypothesis, D = germline
    susceptibility locus. Tier C is the part that does not appear on a conventional candidate
    list, so its presence is what makes the panel a hypothesis rather than a literature summary."""
    tiers = {candidate.tier[0] for candidate in CANDIDATE_DRIVERS}
    assert tiers == {"A", "B", "C", "D"}
    tier_c = [c.gene for c in CANDIDATE_DRIVERS if c.tier.startswith("C")]
    assert "CSF1R" in tier_c


def test_every_candidate_states_a_rationale_and_hotspots_are_typed_consistently():
    for candidate in CANDIDATE_DRIVERS:
        assert candidate.rationale and len(candidate.rationale) > 40
        for position, residue in candidate.hotspots.items():
            assert isinstance(position, int) and position > 0
            assert residue in AA_HYDROPATHY, f"{candidate.gene} hotspot residue {residue!r}"


def test_verified_hotspot_controls_are_a_subset_of_the_declared_panel_hotspots():
    """The positive-control set must not contain a position the panel itself doesn't declare --
    otherwise the validation would be testing something the analysis never checks."""
    declared = {c.gene: c.hotspots for c in CANDIDATE_DRIVERS}
    for gene, hotspots in VERIFIED_HOTSPOT_CONTROLS.items():
        assert gene in declared
        for position, residue in hotspots.items():
            assert declared[gene].get(position) == residue


def test_hydropathy_track_matches_kyte_doolittle_and_tolerates_unknown_residues():
    assert hydropathy_track("AIL").tolist() == [1.8, 4.5, 3.8]
    assert hydropathy_track("AXA").tolist() == [1.8, 0.0, 1.8]  # X is unknown -> 0.0
    assert len(hydropathy_track("")) == 0


def test_hotspot_salience_returns_finite_residuals_over_the_valid_region():
    rng = np.random.default_rng(0)
    sequence = "".join(rng.choice(list(AA_HYDROPATHY), 300))
    # pLDDT partly driven by local hydropathy plus noise, so the model has real signal to fit.
    hydropathy = hydropathy_track(sequence)
    plddt = 70 + 4 * np.convolve(hydropathy, np.ones(5) / 5, mode="same") + rng.normal(0, 2, 300)
    salience = hotspot_salience(plddt, sequence, memory=11, n_basis=4)
    assert salience.shape == (300,)
    assert np.isnan(salience[:10]).all()          # incomplete lag history is excluded, not faked
    assert np.isfinite(salience[11:]).all()
    assert (salience[11:] >= 0).all()              # it is an absolute residual


def test_hotspot_salience_rejects_sequences_shorter_than_its_memory():
    with pytest.raises(ValueError):
        hotspot_salience(np.linspace(50, 90, 8), "AAAAAAAA", memory=11)


def test_permutation_pvalue_detects_a_planted_enrichment_and_reports_power_caveat():
    salience = np.full(200, 1.0)
    planted = [50, 100, 150]
    for position in planted:
        salience[position - 1] = 100.0
    report = permutation_pvalue(salience, planted, n_permutations=2000, seed=1)
    assert report["n_positions_scored"] == 3
    assert report["p_value"] < 0.01
    assert "power_caveat" in report


def test_permutation_pvalue_reports_null_result_when_positions_are_unremarkable():
    rng = np.random.default_rng(3)
    salience = rng.normal(5, 1, 400)
    report = permutation_pvalue(salience, [10, 200, 390], n_permutations=2000, seed=2)
    assert report["p_value"] > 0.05
    assert "no evidence" in report["interpretation"]


def test_permutation_pvalue_handles_positions_outside_the_scored_region():
    salience = np.concatenate([np.full(5, np.nan), np.ones(20)])
    report = permutation_pvalue(salience, [1, 2, 999], n_permutations=100)
    assert report["n_positions_scored"] == 0
    assert report["p_value"] is None


def test_bicoherence_detects_quadratic_phase_coupling_and_ignores_uncoupled_components():
    """The property that makes bicoherence a genuinely nonlinear measure: two signals can share a
    power spectrum while differing entirely in phase coupling.

    The construction matters, and getting it wrong was instructive enough to record here. Phases
    must be re-randomized *per segment*: with a single deterministic sinusoid triplet every segment
    observes the same phase relationship, so bicoherence saturates near 1 whether or not the
    components are genuinely coupled. Bicoherence tests phase-relationship *consistency across
    realizations*, so the uncoupled control has to actually vary across them."""
    nperseg, n_segments = 256, 40
    f1, f2 = 0.1, 0.15
    rng = np.random.default_rng(0)
    t = np.arange(nperseg)

    coupled_segments, independent_segments = [], []
    for _ in range(n_segments):
        phase_1, phase_2, phase_free = rng.uniform(0, 2 * np.pi, 3)
        base = (np.sin(2 * np.pi * f1 * t + phase_1) + np.sin(2 * np.pi * f2 * t + phase_2))
        # coupled: the sum component's phase is the sum of the parents' phases (quadratic coupling)
        coupled_segments.append(base + np.sin(2 * np.pi * (f1 + f2) * t + phase_1 + phase_2))
        # uncoupled: identical power spectrum, but the sum component's phase is independent
        independent_segments.append(base + np.sin(2 * np.pi * (f1 + f2) * t + phase_free))

    coupled = np.concatenate(coupled_segments)
    independent = np.concatenate(independent_segments)
    freq, b2_coupled = bicoherence(coupled, nperseg=nperseg, noverlap=0)
    _, b2_independent = bicoherence(independent, nperseg=nperseg, noverlap=0)
    i, j = int(np.argmin(np.abs(freq - f1))), int(np.argmin(np.abs(freq - f2)))
    assert b2_coupled[i, j] > 0.8
    assert b2_independent[i, j] < 0.3
    assert b2_coupled[i, j] > b2_independent[i, j]


def test_bicoherence_is_symmetric_and_masks_pairs_above_nyquist():
    rng = np.random.default_rng(1)
    freq, b2 = bicoherence(rng.normal(0, 1, 1024), nperseg=64)
    upper = ~np.isnan(b2)
    np.testing.assert_allclose(b2[upper], b2.T[upper])
    n_freq = len(freq)
    assert np.isnan(b2[n_freq - 1, n_freq - 1])   # f1+f2 beyond Nyquist must not wrap silently


def test_bicoherence_requires_multiple_segments_to_be_meaningful():
    # With one segment b^2 == 1 everywhere by construction, which is why this must error rather
    # than return a spuriously perfect result.
    rng = np.random.default_rng(2)
    with pytest.raises(ValueError):
        bicoherence(rng.normal(0, 1, 64), nperseg=64, noverlap=0)


def test_bicoherence_rejects_out_of_range_parameters():
    rng = np.random.default_rng(4)
    x = rng.normal(0, 1, 256)
    with pytest.raises(ValueError):
        bicoherence(x, nperseg=4)                 # below the 8-sample floor
    with pytest.raises(ValueError):
        bicoherence(x, nperseg=512)               # longer than the signal
    with pytest.raises(ValueError):
        bicoherence(x, nperseg=64, noverlap=64)   # noverlap must be < nperseg
