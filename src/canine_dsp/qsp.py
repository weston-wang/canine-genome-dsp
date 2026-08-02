"""Reduced PK/QSP exposure constraints for immunotherapy system identification."""

from dataclasses import dataclass, replace

import numpy as np


@dataclass(frozen=True)
class ExposureModel:
    """One-compartment plasma PK with tumor equilibration and saturable target engagement."""

    half_life: np.ndarray
    bioavailability: np.ndarray
    tumor_penetration: np.ndarray
    tumor_equilibration: np.ndarray
    ec50: np.ndarray
    linear_channel: np.ndarray

    def __post_init__(self):
        arrays = [np.asarray(value) for value in [self.half_life, self.bioavailability,
                  self.tumor_penetration, self.tumor_equilibration, self.ec50,
                  self.linear_channel]]
        if any(value.shape != arrays[0].shape for value in arrays):
            raise ValueError("all exposure parameters must contain one value per channel")
        if np.any(arrays[0] <= 0) or np.any(np.asarray(self.ec50) <= 0):
            raise ValueError("half_life and ec50 must be positive")
        if np.any(np.asarray(self.bioavailability) < 0) or np.any(
                np.asarray(self.tumor_penetration) < 0):
            raise ValueError("bioavailability and tumor_penetration must be nonnegative")
        if np.any(np.asarray(self.tumor_equilibration) <= 0) or np.any(
                np.asarray(self.tumor_equilibration) > 1):
            raise ValueError("tumor_equilibration must lie in (0, 1]")


@dataclass(frozen=True)
class ExposureTrajectory:
    plasma: np.ndarray
    tumor: np.ndarray
    effective_input: np.ndarray


@dataclass(frozen=True)
class ProtocolConstraints:
    """Normalized protocol bounds; values require drug-specific clinical replacement."""

    allowed_days: tuple[tuple[int, ...], ...]
    max_per_dose: np.ndarray
    max_cumulative: np.ndarray
    max_plasma_cmax: np.ndarray
    max_tumor_auc: np.ndarray

    def __post_init__(self):
        channels = len(self.allowed_days)
        for value in [self.max_per_dose, self.max_cumulative,
                      self.max_plasma_cmax, self.max_tumor_auc]:
            if np.asarray(value).shape != (channels,) or np.any(np.asarray(value) <= 0):
                raise ValueError("protocol bounds must be positive and contain one value per channel")


def reference_protocol_constraints() -> ProtocolConstraints:
    return ProtocolConstraints(
        allowed_days=((0, 7, 14, 21), (0, 7, 14, 21), (0, 7, 14, 21)),
        max_per_dose=np.array([1., .8, .7]),
        max_cumulative=np.array([3.6, 2.8, 2.4]),
        max_plasma_cmax=np.array([1.5, 2.4, .75]),
        max_tumor_auc=np.array([10., 16., 2.8]),
    )


def reference_exposure_model() -> ExposureModel:
    """Synthetic normalized vaccine/checkpoint/radiation exposure constraints."""
    return ExposureModel(
        half_life=np.array([2.5, 12.0, .35]),
        bioavailability=np.array([.85, 1.0, 1.0]),
        tumor_penetration=np.array([.55, .32, 1.0]),
        tumor_equilibration=np.array([.45, .18, 1.0]),
        ec50=np.array([.30, .22, .50]),
        linear_channel=np.array([False, False, True]),
    )


def simulate_exposure(doses: np.ndarray, model: ExposureModel) -> ExposureTrajectory:
    """Map normalized administered doses to plasma, tumor, and target-engagement histories."""
    doses = np.asarray(doses, float)
    channels = len(np.asarray(model.half_life))
    if doses.ndim != 2 or doses.shape[1] != channels:
        raise ValueError("dose schedule has the wrong number of channels")
    if not np.all(np.isfinite(doses)) or np.any(doses < 0):
        raise ValueError("doses must be finite and nonnegative")
    plasma = np.zeros_like(doses); tumor = np.zeros_like(doses)
    retention = np.exp(-np.log(2) / np.asarray(model.half_life))
    for day in range(len(doses)):
        previous_plasma = plasma[day - 1] if day else np.zeros(channels)
        previous_tumor = tumor[day - 1] if day else np.zeros(channels)
        plasma[day] = previous_plasma * retention + doses[day] * model.bioavailability
        target = plasma[day] * model.tumor_penetration
        tumor[day] = previous_tumor + model.tumor_equilibration * (target - previous_tumor)
    occupancy = tumor / (np.asarray(model.ec50) + tumor)
    effective = np.where(np.asarray(model.linear_channel, bool), tumor, occupancy)
    return ExposureTrajectory(plasma, tumor, effective)


def perturb_exposure(model: ExposureModel, rng: np.random.Generator,
                     scale: float = .15) -> ExposureModel:
    """Create an external-validation PK shift without changing treatment bounds."""
    channels = len(np.asarray(model.half_life))
    return replace(
        model,
        half_life=np.asarray(model.half_life) * rng.lognormal(0, scale, channels),
        tumor_penetration=np.clip(np.asarray(model.tumor_penetration)
                                 * rng.lognormal(0, scale, channels), .05, 1.5),
        ec50=np.asarray(model.ec50) * rng.lognormal(0, scale, channels),
    )


def protocol_violations(schedule: np.ndarray, exposure_model: ExposureModel,
                        constraints: ProtocolConstraints) -> dict[str, np.ndarray]:
    schedule = np.asarray(schedule, float)
    trajectory = simulate_exposure(schedule, exposure_model)
    allowed = np.zeros_like(schedule, dtype=bool)
    for channel, days in enumerate(constraints.allowed_days):
        valid_days = [day for day in days if 0 <= day < len(schedule)]
        allowed[valid_days, channel] = True
    return {
        "disallowed_dose": np.maximum(np.where(allowed, 0, schedule), 0).sum(axis=0),
        "per_dose": np.maximum(schedule.max(axis=0) - constraints.max_per_dose, 0),
        "cumulative": np.maximum(schedule.sum(axis=0) - constraints.max_cumulative, 0),
        "plasma_cmax": np.maximum(trajectory.plasma.max(axis=0)
                                  - constraints.max_plasma_cmax, 0),
        "tumor_auc": np.maximum(trajectory.tumor.sum(axis=0)
                                - constraints.max_tumor_auc, 0),
    }


def protocol_is_feasible(schedule: np.ndarray, exposure_model: ExposureModel,
                         constraints: ProtocolConstraints, tolerance: float = 1e-8) -> bool:
    return all(np.all(value <= tolerance) for value in protocol_violations(
        schedule, exposure_model, constraints).values())
