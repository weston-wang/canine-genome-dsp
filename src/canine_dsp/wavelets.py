import numpy as np
import pywt


def cwt_power(
    x: np.ndarray, scales: np.ndarray | None = None, wavelet: str = "cmor1.5-1.0"
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Complex Morlet continuous-wavelet power and cone-free nominal frequencies."""
    x = np.asarray(x, dtype=float)
    if x.size < 8:
        raise ValueError("signal needs at least 8 samples")
    x = np.nan_to_num(x - np.nanmean(x))
    scales = np.asarray(scales if scales is not None else np.geomspace(2, max(4, x.size / 4), 48))
    coefficients, frequencies = pywt.cwt(x, scales, wavelet)
    return scales, frequencies, np.abs(coefficients) ** 2

