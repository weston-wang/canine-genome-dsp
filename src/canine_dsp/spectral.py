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


def bicoherence(x: np.ndarray, nperseg: int = 64, noverlap: int | None = None
                ) -> tuple[np.ndarray, np.ndarray]:
    """Squared bicoherence b^2(f1,f2): normalized third-order spectrum measuring *quadratic phase
    coupling* between frequency pairs. This is a genuinely nonlinear measure, not another linear
    one. The ordinary power spectrum and coherence are blind to phase relationships between
    components: a linear Gaussian process and a nonlinearly-coupled process can share an identical
    PSD.
    """
    x = _clean(x)
    noverlap = nperseg // 2 if noverlap is None else noverlap
    if not 8 <= nperseg <= x.size:
        raise ValueError(f"require 8 <= nperseg <= len(x); got nperseg={nperseg}, len(x)={x.size}")
    if not 0 <= noverlap < nperseg:
        raise ValueError("require 0 <= noverlap < nperseg")
    step = nperseg - noverlap
    starts = range(0, x.size - nperseg + 1, step)
    window = signal.windows.hann(nperseg)
    segments = np.array([np.fft.rfft(window * x[s:s + nperseg]) for s in starts])
    if len(segments) < 2:
        raise ValueError("bicoherence needs >=2 segments to average; use a smaller nperseg")

    n_freq = segments.shape[1]
    b2 = np.full((n_freq, n_freq), np.nan)
    # Triple product <X(f1) X(f2) X*(f1+f2)> normalized by <|X(f1)X(f2)|^2><|X(f1+f2)|^2>.
    for i in range(n_freq):
        for j in range(i, n_freq):
            if i + j >= n_freq:
                continue
            pair = segments[:, i] * segments[:, j]
            sum_term = segments[:, i + j]
            numerator = np.abs(np.mean(pair * np.conj(sum_term))) ** 2
            denominator = np.mean(np.abs(pair) ** 2) * np.mean(np.abs(sum_term) ** 2)
            value = numerator / denominator if denominator > 0 else np.nan
            b2[i, j] = b2[j, i] = value
    return np.fft.rfftfreq(nperseg), b2

