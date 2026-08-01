import numpy as np
from scipy import signal


def _clean(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    if x.size < 8:
        raise ValueError("signal needs at least 8 samples")
    if np.isnan(x).any():
        x = np.where(np.isnan(x), np.nanmean(x), x)
    return signal.detrend(x)


def welch_psd(x: np.ndarray, fs: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
    x = _clean(x)
    nperseg = min(256, x.size)
    return signal.welch(x, fs=fs, nperseg=nperseg, window="hann", scaling="density")


def multitaper_psd(
    x: np.ndarray, fs: float = 1.0, time_bandwidth: float = 3.5, tapers: int | None = None
) -> tuple[np.ndarray, np.ndarray]:
    """Thomson-style DPSS multitaper estimate with eigenvalue weighting."""
    x = _clean(x)
    k = tapers or max(1, int(2 * time_bandwidth) - 1)
    windows, ratios = signal.windows.dpss(x.size, time_bandwidth, Kmax=k, return_ratios=True)
    spectra = np.abs(np.fft.rfft(windows * x, axis=1)) ** 2
    psd = np.average(spectra, axis=0, weights=ratios) / (fs * x.size)
    return np.fft.rfftfreq(x.size, d=1 / fs), psd


def spectral_entropy(psd: np.ndarray) -> float:
    p = np.maximum(np.asarray(psd, dtype=float), 0)
    if p.sum() == 0 or p.size <= 1:
        return 0.0
    p /= p.sum()
    p = p[p > 0]
    return float(-(p * np.log2(p)).sum() / np.log2(len(psd)))


def coherence(x: np.ndarray, y: np.ndarray, fs: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
    n = min(len(x), len(y))
    if n < 8:
        raise ValueError("signals need at least 8 aligned samples")
    x, y = _clean(np.asarray(x)[:n]), _clean(np.asarray(y)[:n])
    return signal.coherence(x, y, fs=fs, nperseg=min(256, n))

