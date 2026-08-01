import numpy as np

from canine_dsp.volterra import (
    dct_lag_basis,
    fit_volterra,
    predict,
    volterra_design,
)


def test_basis_is_orthonormal():
    basis = dct_lag_basis(9, 4)
    np.testing.assert_allclose(basis @ basis.T, np.eye(4), atol=1e-12)


def test_design_resets_and_masks_group_boundaries():
    x = np.arange(20.0).reshape(-1, 1)
    groups = np.repeat(["a", "b"], 10)
    design, names, valid = volterra_design(x, groups, ["x"], memory=3, n_basis=2)
    assert design.shape == (20, 5)  # 2 linear + 3 unique quadratic terms
    assert len(names) == 5
    np.testing.assert_array_equal(np.flatnonzero(~valid), [0, 1, 10, 11])


def test_second_order_model_recovers_quadratic_mapping():
    rng = np.random.default_rng(8)
    x = rng.normal(size=(1000, 1))
    groups = np.repeat(["a", "b"], 500)
    design, names, valid = volterra_design(x, groups, ["x"], memory=1, n_basis=1)
    y = 1.2 * x[:, 0] - 2.5 * x[:, 0] ** 2 + rng.normal(0, .03, len(x))
    fit = fit_volterra(design[valid], y[valid], names, dct_lag_basis(1, 1), ["x"],
                       order=2, family="gaussian", alpha=1e-5, l1_ratio=.5)
    estimate = predict(fit, design[valid])
    assert np.corrcoef(y[valid], estimate)[0, 1] > .999
    h1, h2 = fit.reconstruct_kernels()
    assert abs(h1[0, 0] - 1.2) < .05
    assert abs(h2[0, 0, 0, 0] + 2.5) < .05
