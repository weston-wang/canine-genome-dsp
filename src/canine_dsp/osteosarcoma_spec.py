"""Versioned patient-specific cargo-design specifications.

The specification separates patient DLA/HLA and clone requirements from the
benchmark's illustrative defaults.  It contains no outcome data and does not
constitute a vaccine or treatment recommendation.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, fields
from enum import Enum
from pathlib import Path
from typing import Any, Mapping, Sequence

from .osteosarcoma_design import CargoConstraints, SpeciesScenario


SCHEMA_VERSION = 1
_TOP_LEVEL_KEYS = frozenset({"schema_version", "constraints", "scenarios"})


def _json_value(value: Any) -> Any:
    """Convert validated specification values to deterministic JSON values."""
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Mapping):
        converted = {}
        for key, item in value.items():
            json_key = key.value if isinstance(key, Enum) else str(key)
            converted[json_key] = _json_value(item)
        return {key: converted[key] for key in sorted(converted)}
    if isinstance(value, (set, frozenset)):
        converted = [_json_value(item) for item in value]
        return sorted(converted, key=lambda item: json.dumps(item, sort_keys=True))
    if isinstance(value, (tuple, list)):
        return [_json_value(item) for item in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise TypeError(f"specification value is not JSON serializable: {type(value).__name__}")


def _field_manifest(instance: object) -> dict[str, Any]:
    return {
        item.name: _json_value(getattr(instance, item.name))
        for item in fields(instance)
    }


@dataclass(frozen=True)
class DesignSpecification:
    """Validated hard constraints and robustness scenarios for one species."""

    constraints: CargoConstraints
    scenarios: tuple[SpeciesScenario, ...] | Sequence[SpeciesScenario]
    schema_version: int = SCHEMA_VERSION

    def __post_init__(self) -> None:
        if (
            not isinstance(self.schema_version, int)
            or isinstance(self.schema_version, bool)
            or self.schema_version != SCHEMA_VERSION
        ):
            raise ValueError(f"schema_version must be the integer {SCHEMA_VERSION}")
        if not isinstance(self.constraints, CargoConstraints):
            raise TypeError("constraints must be a CargoConstraints instance")
        scenarios = tuple(self.scenarios)
        if not scenarios:
            raise ValueError("scenarios must contain at least one scenario")
        if any(not isinstance(scenario, SpeciesScenario) for scenario in scenarios):
            raise TypeError("scenarios must contain only SpeciesScenario instances")
        names = [scenario.name for scenario in scenarios]
        if len(names) != len(set(names)):
            raise ValueError("scenario names must be unique")
        mismatched = sorted(
            scenario.name
            for scenario in scenarios
            if scenario.species != self.constraints.species
        )
        if mismatched:
            raise ValueError(
                "constraint and scenario species must match; mismatched scenarios: "
                f"{mismatched}"
            )
        object.__setattr__(self, "scenarios", scenarios)

    def to_dict(self) -> dict[str, Any]:
        """Return a deterministic manifest containing every effective field."""
        return {
            "schema_version": self.schema_version,
            "constraints": _field_manifest(self.constraints),
            "scenarios": [_field_manifest(scenario) for scenario in self.scenarios],
        }


def _object(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be a JSON object")
    return value


def _reject_unknown_fields(value: Mapping[str, Any], instance_type: type,
                           name: str) -> None:
    allowed = {item.name for item in fields(instance_type)}
    unknown = set(value) - allowed
    if unknown:
        raise ValueError(f"{name} contains unknown fields: {sorted(unknown)}")


def load_design_spec(path: str | Path) -> DesignSpecification:
    """Load and validate a schema-v1 JSON design specification."""
    path = Path(path)
    try:
        payload = json.loads(path.read_text())
    except json.JSONDecodeError as error:
        raise ValueError(f"design specification is not valid JSON: {error.msg}") from error
    payload = _object(payload, "design specification")
    unknown = set(payload) - _TOP_LEVEL_KEYS
    if unknown:
        raise ValueError(f"design specification contains unknown keys: {sorted(unknown)}")
    missing = _TOP_LEVEL_KEYS - set(payload)
    if missing:
        raise ValueError(f"design specification is missing keys: {sorted(missing)}")
    version = payload["schema_version"]
    if not isinstance(version, int) or isinstance(version, bool) or version != SCHEMA_VERSION:
        raise ValueError(f"schema_version must be the integer {SCHEMA_VERSION}")

    constraint_values = _object(payload["constraints"], "constraints")
    _reject_unknown_fields(constraint_values, CargoConstraints, "constraints")
    scenario_values = payload["scenarios"]
    if not isinstance(scenario_values, list) or not scenario_values:
        raise ValueError("scenarios must be a nonempty JSON list")
    scenarios = []
    for index, value in enumerate(scenario_values):
        scenario = _object(value, f"scenarios[{index}]")
        _reject_unknown_fields(scenario, SpeciesScenario, f"scenarios[{index}]")
        try:
            scenarios.append(SpeciesScenario(**scenario))
        except (TypeError, ValueError) as error:
            raise ValueError(f"invalid scenarios[{index}]: {error}") from error
    try:
        constraints = CargoConstraints(**constraint_values)
    except (TypeError, ValueError) as error:
        raise ValueError(f"invalid constraints: {error}") from error
    return DesignSpecification(
        constraints=constraints,
        scenarios=tuple(scenarios),
        schema_version=version,
    )


def illustrative_canine_design_spec(escape_target: str) -> DesignSpecification:
    """Return the benchmark's schema-v1 illustrative canine design assumptions."""
    escape_target = str(escape_target).strip()
    if not escape_target:
        raise ValueError("escape_target must be a nonempty candidate identifier")
    constraints = CargoConstraints(
        species="canine",
        min_antigens=4,
        max_antigens=7,
        min_class_i_antigens=2,
        min_class_ii_antigens=2,
        min_truncal_antigens=2,
        required_subclones={"trunk", "lung_A", "lung_B", "lung_C"},
        min_hits_per_subclone=1,
        required_class_i_alleles={"DLA-88*001:01", "DLA-88*508:01"},
        required_class_ii_alleles={"DLA-DRB1*015:01", "DLA-DQA1*001:01"},
        required_source_classes={"structural_variant", "fusion"},
        min_expression=.50,
        min_clonality=.55,
        min_normal_proteome_safety=.75,
        min_presentation_retention=.65,
        max_escape_risk=.35,
        min_manufacturability=.65,
    )
    scenarios = (
        SpeciesScenario("nominal", "canine"),
        SpeciesScenario(
            "DLA_88_001_loss",
            "canine",
            lost_class_i_alleles={"DLA-88*001:01"},
        ),
        SpeciesScenario(
            "DLA_DRB1_015_loss",
            "canine",
            lost_class_ii_alleles={"DLA-DRB1*015:01"},
        ),
        SpeciesScenario(
            "low_expression_and_retention",
            "canine",
            expression_scale=.72,
            retention_scale=.75,
        ),
        SpeciesScenario(
            "single_antigen_loss",
            "canine",
            escaped_antigens={escape_target},
        ),
    )
    return DesignSpecification(constraints=constraints, scenarios=scenarios)


__all__ = [
    "SCHEMA_VERSION",
    "DesignSpecification",
    "illustrative_canine_design_spec",
    "load_design_spec",
]
