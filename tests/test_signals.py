import numpy as np

from canine_dsp.signals import variant_density, windowed_gc
from canine_dsp.spectral import multitaper_psd, spectral_entropy


def test_windowed_gc_handles_n():
    np.testing.assert_allclose(windowed_gc("GCGCATNN", 4), [1.0, 0.0])


def test_variant_density_uses_vcf_coordinates():
    np.testing.assert_array_equal(variant_density(np.array([1, 10, 11, 20]), 20, 10), [2, 2])


def test_multitaper_finds_period():
    x = np.sin(2 * np.pi * np.arange(1024) / 16)
    f, p = multitaper_psd(x)
    assert abs(f[np.argmax(p)] - 1 / 16) < 0.01
    assert 0 <= spectral_entropy(p) <= 1

