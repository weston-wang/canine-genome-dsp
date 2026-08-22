"""Basis-reduced, second-order Volterra models for spatial genomic tracks."""

from dataclasses import dataclass
from itertools import combinations_with_replacement

import numpy as np
from scipy.fft import dct
from scipy.signal import lfilter
from sklearn.linear_model import ElasticNet, PoissonRegressor
from sklearn.metrics import mean_absolute_error, mean_poisson_deviance, r2_score
from sklearn.preprocessing import StandardScaler


def dct_lag_basis(memory: int, n_basis: int) -> np.ndarray:
    """Return low-frequency orthonormal DCT basis vectors over causal lags."""
    if memory < 1 or not 1 <= n_basis <= memory:
        raise ValueError("require memory >= 1 and 1 <= n_basis <= memory")
    return dct(np.eye(memory), type=2, norm="ortho", axis=0)[:n_basis]


def _filter_by_group(x: np.ndarray, groups: np.ndarray, basis: np.ndarray) -> np.ndarray:
    """Causally filter each track without leaking across chromosome boundaries."""
    n, channels = x.shape
    result = np.empty((n, channels, len(basis)))
    for group in dict.fromkeys(groups.tolist()):
        rows = np.flatnonzero(groups == group)
        if rows.size and np.any(np.diff(rows) != 1):
            raise ValueError(f"group {group!r} must occupy one contiguous block")
        for channel in range(channels):
            for r, kernel in enumerate(basis):
                result[rows, channel, r] = lfilter(kernel, [1.0], x[rows, channel])
    return result


def _term_names(input_names: list[str], n_basis: int) -> tuple[list[str], list[str]]:
    linear = [f"L:{name}:b{r}" for name in input_names for r in range(n_basis)]
    quadratic = [f"Q:{linear[a][2:]}*{linear[b][2:]}"
                 for a, b in combinations_with_replacement(range(len(linear)), 2)]
    return linear, quadratic


def volterra_design(
    x: np.ndarray,
    groups: np.ndarray,
    input_names: list[str],
    memory: int,
    n_basis: int,
    order: int = 2,
) -> tuple[np.ndarray, list[str], np.ndarray]:
    """Construct linear and reduced quadratic Volterra regressors.

    Initial samples whose lag histories are incomplete are marked invalid separately for each group.
    """
    x = np.asarray(x, dtype=float)
    groups = np.asarray(groups)
    if x.ndim != 2 or x.shape[0] != groups.size or x.shape[1] != len(input_names):
        raise ValueError("x, groups, and input_names have inconsistent dimensions")
    if order not in (1, 2):
        raise ValueError("only first- and second-order models are supported")
    basis = dct_lag_basis(memory, n_basis)
    filtered = _filter_by_group(x, groups, basis).reshape(len(x), -1)
    linear_names, quadratic_names = _term_names(input_names, n_basis)
    columns = [filtered]
    names = linear_names.copy()
    if order == 2:
        pairs = list(combinations_with_replacement(range(filtered.shape[1]), 2))
        columns.append(np.column_stack([filtered[:, a] * filtered[:, b] for a, b in pairs]))
        names.extend(quadratic_names)
    valid = np.ones(len(x), dtype=bool)
    for group in dict.fromkeys(groups.tolist()):
        rows = np.flatnonzero(groups == group)
        valid[rows[: min(memory - 1, len(rows))]] = False
    return np.column_stack(columns), names, valid


@dataclass
class VolterraFit:
    model: object
    scaler: StandardScaler
    term_names: list[str]
    basis: np.ndarray
    input_names: list[str]
    order: int
    family: str

    @property
    def coefficients(self) -> np.ndarray:
        """Coefficients expressed in the unscaled Volterra design coordinates."""
        return np.asarray(self.model.coef_) / self.scaler.scale_

    def reconstruct_kernels(self) -> tuple[np.ndarray, np.ndarray | None]:
        """Reconstruct h1[channel, lag] and h2[filtered_channel, filtered_channel, lag, lag]."""
        channels, rank = len(self.input_names), len(self.basis)
        linear_count = channels * rank
        h1 = self.coefficients[:linear_count].reshape(channels, rank) @ self.basis
        if self.order == 1:
            return h1, None
        h2 = np.zeros((channels, channels, self.basis.shape[1], self.basis.shape[1]))
        coefficient = iter(self.coefficients[linear_count:])
        for a, b in combinations_with_replacement(range(linear_count), 2):
            value = next(coefficient)
            ca, ra = divmod(a, rank)
            cb, rb = divmod(b, rank)
            surface = value * np.outer(self.basis[ra], self.basis[rb])
            h2[ca, cb] += surface
            if a != b:
                h2[cb, ca] += surface.T
        return h1, h2


def fit_volterra(
    design: np.ndarray,
    y: np.ndarray,
    term_names: list[str],
    basis: np.ndarray,
    input_names: list[str],
    order: int = 2,
    family: str = "gaussian",
    alpha: float = 0.01,
    l1_ratio: float = 0.5,
    exposure: np.ndarray | None = None,
) -> VolterraFit:
    """Fit a sparse Gaussian model or exposure-aware Poisson rate model."""
    design, y = np.asarray(design, float), np.asarray(y, float)
    scaler = StandardScaler().fit(design)
    z = scaler.transform(design)
    if family == "gaussian":
        model = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, max_iter=50_000).fit(z, y)
    elif family == "poisson":
        exposure = np.ones_like(y) if exposure is None else np.asarray(exposure, float)
        if np.any(exposure <= 0) or np.any(y < 0):
            raise ValueError("Poisson counts must be nonnegative and exposure must be positive")
        # Fitting rate with exposure as sample weight is equivalent to a log-exposure offset.
        model = PoissonRegressor(alpha=alpha, max_iter=2_000).fit(
            z, y / exposure, sample_weight=exposure
        )
    else:
        raise ValueError("family must be 'gaussian' or 'poisson'")
    return VolterraFit(model, scaler, term_names, basis, input_names, order, family)


def predict(fit: VolterraFit, design: np.ndarray, exposure: np.ndarray | None = None) -> np.ndarray:
    estimate = fit.model.predict(fit.scaler.transform(design))
    if fit.family == "poisson" and exposure is not None:
        estimate = estimate * np.asarray(exposure)
    return estimate


def regression_metrics(y: np.ndarray, prediction: np.ndarray, family: str) -> dict[str, float]:
    result = {
        "r2": float(r2_score(y, prediction)),
        "mae": float(mean_absolute_error(y, prediction)),
    }
    if family == "poisson":
        result["mean_poisson_deviance"] = float(
            mean_poisson_deviance(y, np.maximum(prediction, np.finfo(float).eps))
        )
    return result

