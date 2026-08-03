"""Constrained research designs for multivalent osteosarcoma RNA cargo.

This module ranks *candidate designs* under explicit assumptions.  It does not
predict clinical benefit, replace neoantigen validation, or prescribe a vaccine.
Candidate measurements and uncertainty scenarios are inputs supplied by the
caller; the defaults are deliberately neutral rather than clinically calibrated.

The objective combines first-order antigen attributes with a low-rank
second-order interaction model.  The latter is a compact Volterra-style proxy:
pairwise synergy and competition are Gram matrices of per-antigen loadings, so
the number of interaction parameters grows linearly rather than quadratically.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from itertools import combinations
from math import comb
from typing import Iterable, Mapping, Sequence

import numpy as np


class Species(str, Enum):
    """Supported comparative species."""

    HUMAN = "human"
    CANINE = "canine"


class AntigenSource(str, Enum):
    """Origin of the encoded tumor antigen."""

    SNV = "snv"
    INDEL = "indel"
    FUSION = "fusion"
    STRUCTURAL_VARIANT = "structural_variant"
    CANCER_TESTIS = "cancer_testis"
    OVEREXPRESSED = "overexpressed"
    OTHER = "other"


def _species(value: Species | str) -> Species:
    if isinstance(value, Species):
        return value
    normalized = str(value).strip().lower()
    if normalized == "dog":
        normalized = "canine"
    try:
        return Species(normalized)
    except ValueError as error:
        raise ValueError("species must be 'human', 'canine', or 'dog'") from error


def _source(value: AntigenSource | str) -> AntigenSource:
    if isinstance(value, AntigenSource):
        return value
    normalized = str(value).strip().lower().replace("-", "_")
    if normalized == "sv":
        normalized = "structural_variant"
    try:
        return AntigenSource(normalized)
    except ValueError as error:
        allowed = ", ".join(item.value for item in AntigenSource)
        raise ValueError(f"source_class must be one of: {allowed}") from error


def _bounded(name: str, value: float) -> float:
    value = float(value)
    if not np.isfinite(value) or not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be finite and between 0 and 1")
    return value


def _nonnegative_tuple(name: str, values: Iterable[float]) -> tuple[float, ...]:
    result = tuple(float(value) for value in values)
    if any(not np.isfinite(value) or value < 0 for value in result):
        raise ValueError(f"{name} must contain finite nonnegative values")
    return result


def _clean_strings(name: str, values: Iterable[str]) -> frozenset[str]:
    result = frozenset(str(value).strip() for value in values)
    if any(not value for value in result):
        raise ValueError(f"{name} cannot contain empty identifiers")
    return result


def _validate_alleles(species: Species, name: str, alleles: frozenset[str]) -> None:
    prefix = "HLA-" if species == Species.HUMAN else "DLA-"
    wrong = sorted(allele for allele in alleles if not allele.upper().startswith(prefix))
    if wrong:
        raise ValueError(
            f"{name} for {species.value} candidates must use {prefix} identifiers: {wrong}"
        )


@dataclass(frozen=True)
class AntigenCandidate:
    """One pre-screened sequence or shared-antigen RNA cargo candidate.

    Scores are normalized to ``[0, 1]`` and should be produced by a locked,
    independently validated upstream pipeline. ``normal_proteome_safety=1`` is
    safest; ``escape_risk=1`` is highest risk.  Interaction loadings are
    nonnegative low-rank coordinates and have no clinical meaning on their own.
    """

    candidate_id: str
    species: Species | str
    source_class: AntigenSource | str
    expression: float
    clonality: float
    truncality: float
    mhc_i_presentation: float
    mhc_ii_presentation: float
    normal_proteome_safety: float
    presentation_retention: float
    escape_risk: float
    manufacturability: float
    subclones: frozenset[str] | Iterable[str]
    class_i_alleles: frozenset[str] | Iterable[str] = field(default_factory=frozenset)
    class_ii_alleles: frozenset[str] | Iterable[str] = field(default_factory=frozenset)
    gene: str | None = None
    synergy_loadings: tuple[float, ...] | Iterable[float] = ()
    competition_loadings: tuple[float, ...] | Iterable[float] = ()

    def __post_init__(self) -> None:
        candidate_id = str(self.candidate_id).strip()
        if not candidate_id:
            raise ValueError("candidate_id cannot be empty")
        species = _species(self.species)
        source = _source(self.source_class)
        object.__setattr__(self, "candidate_id", candidate_id)
        object.__setattr__(self, "species", species)
        object.__setattr__(self, "source_class", source)
        for name in (
            "expression",
            "clonality",
            "truncality",
            "mhc_i_presentation",
            "mhc_ii_presentation",
            "normal_proteome_safety",
            "presentation_retention",
            "escape_risk",
            "manufacturability",
        ):
            object.__setattr__(self, name, _bounded(name, getattr(self, name)))
        subclones = _clean_strings("subclones", self.subclones)
        if not subclones:
            raise ValueError("subclones must contain at least one tumor clone identifier")
        class_i = _clean_strings("class_i_alleles", self.class_i_alleles)
        class_ii = _clean_strings("class_ii_alleles", self.class_ii_alleles)
        _validate_alleles(species, "class_i_alleles", class_i)
        _validate_alleles(species, "class_ii_alleles", class_ii)
        if self.mhc_i_presentation > 0 and not class_i:
            raise ValueError("positive mhc_i_presentation requires at least one class-I allele")
        if self.mhc_ii_presentation > 0 and not class_ii:
            raise ValueError("positive mhc_ii_presentation requires at least one class-II allele")
        object.__setattr__(self, "subclones", subclones)
        object.__setattr__(self, "class_i_alleles", class_i)
        object.__setattr__(self, "class_ii_alleles", class_ii)
        if self.gene is not None:
            gene = str(self.gene).strip()
            object.__setattr__(self, "gene", gene or None)
        synergy = _nonnegative_tuple("synergy_loadings", self.synergy_loadings)
        competition = _nonnegative_tuple("competition_loadings", self.competition_loadings)
        object.__setattr__(self, "synergy_loadings", synergy)
        object.__setattr__(self, "competition_loadings", competition)


@dataclass(frozen=True)
class CargoConstraints:
    """Hard eligibility and coverage requirements for a cargo design."""

    species: Species | str
    min_antigens: int = 1
    max_antigens: int = 20
    min_class_i_antigens: int = 1
    min_class_ii_antigens: int = 1
    class_i_cutoff: float = 0.5
    class_ii_cutoff: float = 0.5
    min_truncal_antigens: int = 1
    truncal_cutoff: float = 0.8
    required_subclones: frozenset[str] | Iterable[str] = field(default_factory=frozenset)
    min_hits_per_subclone: int = 1
    required_class_i_alleles: frozenset[str] | Iterable[str] = field(default_factory=frozenset)
    required_class_ii_alleles: frozenset[str] | Iterable[str] = field(default_factory=frozenset)
    required_source_classes: frozenset[AntigenSource | str] | Iterable[AntigenSource | str] = (
        field(default_factory=frozenset)
    )
    max_per_source_class: Mapping[AntigenSource | str, int] = field(default_factory=dict)
    min_expression: float = 0.0
    min_clonality: float = 0.0
    min_truncality: float = 0.0
    min_any_presentation: float = 0.0
    min_normal_proteome_safety: float = 0.0
    min_presentation_retention: float = 0.0
    max_escape_risk: float = 1.0
    min_manufacturability: float = 0.0

    def __post_init__(self) -> None:
        species = _species(self.species)
        object.__setattr__(self, "species", species)
        integer_fields = (
            "min_antigens",
            "max_antigens",
            "min_class_i_antigens",
            "min_class_ii_antigens",
            "min_truncal_antigens",
            "min_hits_per_subclone",
        )
        for name in integer_fields:
            value = getattr(self, name)
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                raise ValueError(f"{name} must be a nonnegative integer")
        if self.min_antigens < 1:
            raise ValueError("min_antigens must be at least 1")
        if self.max_antigens < self.min_antigens:
            raise ValueError("max_antigens must be at least min_antigens")
        for name in (
            "class_i_cutoff",
            "class_ii_cutoff",
            "truncal_cutoff",
            "min_expression",
            "min_clonality",
            "min_truncality",
            "min_any_presentation",
            "min_normal_proteome_safety",
            "min_presentation_retention",
            "max_escape_risk",
            "min_manufacturability",
        ):
            object.__setattr__(self, name, _bounded(name, getattr(self, name)))
        required_subclones = _clean_strings("required_subclones", self.required_subclones)
        class_i = _clean_strings("required_class_i_alleles", self.required_class_i_alleles)
        class_ii = _clean_strings("required_class_ii_alleles", self.required_class_ii_alleles)
        _validate_alleles(species, "required_class_i_alleles", class_i)
        _validate_alleles(species, "required_class_ii_alleles", class_ii)
        sources = frozenset(_source(source) for source in self.required_source_classes)
        limits: dict[AntigenSource, int] = {}
        for source, limit in self.max_per_source_class.items():
            if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
                raise ValueError("max_per_source_class limits must be positive integers")
            limits[_source(source)] = limit
        object.__setattr__(self, "required_subclones", required_subclones)
        object.__setattr__(self, "required_class_i_alleles", class_i)
        object.__setattr__(self, "required_class_ii_alleles", class_ii)
        object.__setattr__(self, "required_source_classes", sources)
        object.__setattr__(self, "max_per_source_class", limits)


@dataclass(frozen=True)
class SpeciesScenario:
    """One explicit species-matched uncertainty or immune-escape scenario."""

    name: str
    species: Species | str
    expression_scale: float = 1.0
    presentation_scale: float = 1.0
    retention_scale: float = 1.0
    escape_scale: float = 1.0
    manufacturability_scale: float = 1.0
    interaction_scale: float = 1.0
    lost_class_i_alleles: frozenset[str] | Iterable[str] = field(default_factory=frozenset)
    lost_class_ii_alleles: frozenset[str] | Iterable[str] = field(default_factory=frozenset)
    escaped_antigens: frozenset[str] | Iterable[str] = field(default_factory=frozenset)
    candidate_effect_scale: Mapping[str, float] = field(default_factory=dict)
    weight: float = 1.0

    def __post_init__(self) -> None:
        name = str(self.name).strip()
        if not name:
            raise ValueError("scenario name cannot be empty")
        species = _species(self.species)
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "species", species)
        for field_name in (
            "expression_scale",
            "presentation_scale",
            "retention_scale",
            "escape_scale",
            "manufacturability_scale",
            "interaction_scale",
            "weight",
        ):
            value = float(getattr(self, field_name))
            if not np.isfinite(value) or value < 0:
                raise ValueError(f"{field_name} must be finite and nonnegative")
            object.__setattr__(self, field_name, value)
        if self.weight == 0:
            raise ValueError("scenario weight must be positive")
        lost_i = _clean_strings("lost_class_i_alleles", self.lost_class_i_alleles)
        lost_ii = _clean_strings("lost_class_ii_alleles", self.lost_class_ii_alleles)
        _validate_alleles(species, "lost_class_i_alleles", lost_i)
        _validate_alleles(species, "lost_class_ii_alleles", lost_ii)
        escaped = _clean_strings("escaped_antigens", self.escaped_antigens)
        effects: dict[str, float] = {}
        for candidate_id, scale in self.candidate_effect_scale.items():
            candidate_id = str(candidate_id).strip()
            scale = float(scale)
            if not candidate_id or not np.isfinite(scale) or scale < 0:
                raise ValueError("candidate_effect_scale needs nonempty IDs and nonnegative values")
            effects[candidate_id] = scale
        object.__setattr__(self, "lost_class_i_alleles", lost_i)
        object.__setattr__(self, "lost_class_ii_alleles", lost_ii)
        object.__setattr__(self, "escaped_antigens", escaped)
        object.__setattr__(self, "candidate_effect_scale", effects)


@dataclass(frozen=True)
class DesignWeights:
    """Transparent coefficients for the dimensionless research objective."""

    expression: float = 1.0
    clonality: float = 1.2
    truncality: float = 1.2
    mhc_i_presentation: float = 1.0
    mhc_ii_presentation: float = 0.8
    normal_proteome_safety: float = 1.2
    presentation_retention: float = 1.2
    escape_penalty: float = 1.2
    manufacturability: float = 0.6
    subclone_breadth: float = 0.25
    class_i_allele_breadth: float = 0.08
    class_ii_allele_breadth: float = 0.08
    synergy: float = 0.25
    competition: float = 0.25
    antigen_count_penalty: float = 0.02
    robust_mean_weight: float = 0.10

    def __post_init__(self) -> None:
        for name, value in self.__dict__.items():
            value = float(value)
            if not np.isfinite(value) or value < 0:
                raise ValueError(f"{name} must be finite and nonnegative")
            object.__setattr__(self, name, value)
        if not 0 <= self.robust_mean_weight <= 1:
            raise ValueError("robust_mean_weight must be between 0 and 1")


@dataclass(frozen=True)
class ScheduleCandidate:
    """Prespecified schedule surrogate used only to scale the design objective."""

    name: str
    administration_days: tuple[float, ...] | Sequence[float]
    relative_doses: tuple[float, ...] | Sequence[float]
    first_order_scale: float = 1.0
    second_order_scale: float = 1.0
    objective_penalty: float = 0.0

    def __post_init__(self) -> None:
        name = str(self.name).strip()
        days = tuple(float(day) for day in self.administration_days)
        doses = tuple(float(dose) for dose in self.relative_doses)
        if not name:
            raise ValueError("schedule name cannot be empty")
        if not days or len(days) != len(doses):
            raise ValueError("administration_days and relative_doses need equal nonzero length")
        if any(not np.isfinite(day) or day < 0 for day in days):
            raise ValueError("administration_days must be finite and nonnegative")
        if any(later <= earlier for earlier, later in zip(days, days[1:])):
            raise ValueError("administration_days must be strictly increasing")
        if any(not np.isfinite(dose) or dose <= 0 for dose in doses):
            raise ValueError("relative_doses must be finite and positive")
        for field_name in ("first_order_scale", "second_order_scale", "objective_penalty"):
            value = float(getattr(self, field_name))
            if not np.isfinite(value) or value < 0:
                raise ValueError(f"{field_name} must be finite and nonnegative")
            object.__setattr__(self, field_name, value)
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "administration_days", days)
        object.__setattr__(self, "relative_doses", doses)


@dataclass(frozen=True)
class CandidateRanking:
    candidate_id: str
    robust_singleton_score: float
    worst_scenario: str
    scenario_scores: Mapping[str, float]


@dataclass(frozen=True)
class CargoRanking:
    rank: int
    candidate_ids: tuple[str, ...]
    schedule_name: str | None
    robust_score: float
    worst_case_score: float
    weighted_mean_score: float
    worst_scenario: str
    scenario_scores: Mapping[str, float]
    first_order_score_by_scenario: Mapping[str, float]
    interaction_score_by_scenario: Mapping[str, float]
    covered_subclones: frozenset[str]
    covered_class_i_alleles: frozenset[str]
    covered_class_ii_alleles: frozenset[str]


@dataclass(frozen=True)
class CandidateExclusion:
    candidate_id: str
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class CargoDesignResult:
    """Ranked feasible designs and enough detail to audit the objective."""

    selected: CargoRanking
    rankings: tuple[CargoRanking, ...]
    candidate_rankings: tuple[CandidateRanking, ...]
    exclusions: tuple[CandidateExclusion, ...]
    search_mode: str
    feasible_designs_evaluated: int
    species: Species
    clinical_use: bool = False
    claim_scope: str = (
        "Research ranking under supplied inputs and scenarios; not a clinical prescription."
    )


class InfeasibleCargoError(ValueError):
    """Raised instead of returning a constraint-violating fallback design."""

    def __init__(self, reasons: Iterable[str]):
        self.reasons = tuple(dict.fromkeys(str(reason) for reason in reasons))
        super().__init__("No feasible cargo design: " + "; ".join(self.reasons))


def _eligibility_reasons(candidate: AntigenCandidate,
                         constraints: CargoConstraints) -> tuple[str, ...]:
    reasons = []
    comparisons = (
        ("expression", candidate.expression, constraints.min_expression),
        ("clonality", candidate.clonality, constraints.min_clonality),
        ("truncality", candidate.truncality, constraints.min_truncality),
        ("normal_proteome_safety", candidate.normal_proteome_safety,
         constraints.min_normal_proteome_safety),
        ("presentation_retention", candidate.presentation_retention,
         constraints.min_presentation_retention),
        ("manufacturability", candidate.manufacturability,
         constraints.min_manufacturability),
    )
    for name, observed, threshold in comparisons:
        if observed < threshold:
            reasons.append(f"{name}<{threshold:g}")
    if max(candidate.mhc_i_presentation, candidate.mhc_ii_presentation) < (
        constraints.min_any_presentation
    ):
        reasons.append(f"any_presentation<{constraints.min_any_presentation:g}")
    if candidate.escape_risk > constraints.max_escape_risk:
        reasons.append(f"escape_risk>{constraints.max_escape_risk:g}")
    return tuple(reasons)


def _interaction_rank(candidates: Sequence[AntigenCandidate]) -> tuple[int, int]:
    synergy_ranks = {len(candidate.synergy_loadings) for candidate in candidates}
    competition_ranks = {len(candidate.competition_loadings) for candidate in candidates}
    if len(synergy_ranks) != 1:
        raise ValueError("all candidates must use the same synergy-loading rank")
    if len(competition_ranks) != 1:
        raise ValueError("all candidates must use the same competition-loading rank")
    return next(iter(synergy_ranks)), next(iter(competition_ranks))


def _allele_fraction(alleles: frozenset[str], lost: frozenset[str]) -> float:
    if not alleles:
        return 0.0
    return len(alleles - lost) / len(alleles)


def _candidate_score(candidate: AntigenCandidate, scenario: SpeciesScenario,
                     weights: DesignWeights) -> float:
    if candidate.candidate_id in scenario.escaped_antigens:
        return 0.0
    i_fraction = _allele_fraction(candidate.class_i_alleles, scenario.lost_class_i_alleles)
    ii_fraction = _allele_fraction(candidate.class_ii_alleles, scenario.lost_class_ii_alleles)
    expression = min(1.0, candidate.expression * scenario.expression_scale)
    mhc_i = min(
        1.0, candidate.mhc_i_presentation * scenario.presentation_scale * i_fraction
    )
    mhc_ii = min(
        1.0, candidate.mhc_ii_presentation * scenario.presentation_scale * ii_fraction
    )
    retention = min(1.0, candidate.presentation_retention * scenario.retention_scale)
    escape = min(1.0, candidate.escape_risk * scenario.escape_scale)
    manufacturability = min(
        1.0, candidate.manufacturability * scenario.manufacturability_scale
    )
    # Presentation is a necessary gate, not merely another favorable feature.
    # This prevents a well-expressed but unpresentable sequence from scoring as
    # useful after an HLA/DLA-loss scenario.
    presentation_gate = max(mhc_i, mhc_ii) * retention
    intrinsic_benefit = (
        weights.expression * expression
        + weights.clonality * candidate.clonality
        + weights.truncality * candidate.truncality
        + weights.mhc_i_presentation * mhc_i
        + weights.mhc_ii_presentation * mhc_ii
        + weights.normal_proteome_safety * candidate.normal_proteome_safety
        + weights.presentation_retention * retention
        + weights.manufacturability * manufacturability
    )
    score = intrinsic_benefit * presentation_gate - weights.escape_penalty * escape
    return score * scenario.candidate_effect_scale.get(candidate.candidate_id, 1.0)


def _coverage(cargo: Sequence[AntigenCandidate]) -> tuple[frozenset[str], frozenset[str],
                                                          frozenset[str]]:
    subclones = frozenset().union(*(candidate.subclones for candidate in cargo))
    class_i = frozenset().union(*(candidate.class_i_alleles for candidate in cargo))
    class_ii = frozenset().union(*(candidate.class_ii_alleles for candidate in cargo))
    return subclones, class_i, class_ii


def _is_feasible(cargo: Sequence[AntigenCandidate], constraints: CargoConstraints,
                 partial: bool = False) -> bool:
    if len(cargo) > constraints.max_antigens:
        return False
    source_counts: dict[AntigenSource, int] = {}
    for candidate in cargo:
        source_counts[candidate.source_class] = source_counts.get(candidate.source_class, 0) + 1
    if any(source_counts.get(source, 0) > limit
           for source, limit in constraints.max_per_source_class.items()):
        return False
    if partial:
        return True
    if len(cargo) < constraints.min_antigens:
        return False
    class_i_count = sum(candidate.mhc_i_presentation >= constraints.class_i_cutoff
                        for candidate in cargo)
    class_ii_count = sum(candidate.mhc_ii_presentation >= constraints.class_ii_cutoff
                         for candidate in cargo)
    truncal_count = sum(candidate.truncality >= constraints.truncal_cutoff for candidate in cargo)
    if class_i_count < constraints.min_class_i_antigens:
        return False
    if class_ii_count < constraints.min_class_ii_antigens:
        return False
    if truncal_count < constraints.min_truncal_antigens:
        return False
    subclones, class_i, class_ii = _coverage(cargo)
    if not constraints.required_subclones <= subclones:
        return False
    if any(sum(subclone in candidate.subclones for candidate in cargo)
           < constraints.min_hits_per_subclone
           for subclone in constraints.required_subclones):
        return False
    if not constraints.required_class_i_alleles <= class_i:
        return False
    if not constraints.required_class_ii_alleles <= class_ii:
        return False
    if not constraints.required_source_classes <= set(source_counts):
        return False
    return True


def _constraint_diagnostics(candidates: Sequence[AntigenCandidate],
                            constraints: CargoConstraints) -> list[str]:
    reasons: list[str] = []
    if len(candidates) < constraints.min_antigens:
        reasons.append(
            f"only {len(candidates)} eligible candidates for "
            f"min_antigens={constraints.min_antigens}"
        )
    class_i = [candidate for candidate in candidates
               if candidate.mhc_i_presentation >= constraints.class_i_cutoff]
    class_ii = [candidate for candidate in candidates
                if candidate.mhc_ii_presentation >= constraints.class_ii_cutoff]
    truncal = [candidate for candidate in candidates
               if candidate.truncality >= constraints.truncal_cutoff]
    if len(class_i) < constraints.min_class_i_antigens:
        reasons.append("insufficient class-I-presented candidates")
    if len(class_ii) < constraints.min_class_ii_antigens:
        reasons.append("insufficient class-II-presented candidates")
    if len(truncal) < constraints.min_truncal_antigens:
        reasons.append("insufficient truncal candidates")
    subclones, alleles_i, alleles_ii = _coverage(candidates) if candidates else (
        frozenset(), frozenset(), frozenset()
    )
    missing_subclones = constraints.required_subclones - subclones
    if missing_subclones:
        reasons.append(f"uncovered subclones: {sorted(missing_subclones)}")
    for subclone in constraints.required_subclones:
        hits = sum(subclone in candidate.subclones for candidate in candidates)
        if hits < constraints.min_hits_per_subclone:
            reasons.append(
                f"subclone {subclone!r} has {hits} eligible hits, needs "
                f"{constraints.min_hits_per_subclone}"
            )
    missing_i = constraints.required_class_i_alleles - alleles_i
    missing_ii = constraints.required_class_ii_alleles - alleles_ii
    if missing_i:
        reasons.append(f"uncovered class-I alleles: {sorted(missing_i)}")
    if missing_ii:
        reasons.append(f"uncovered class-II alleles: {sorted(missing_ii)}")
    present_sources = {candidate.source_class for candidate in candidates}
    missing_sources = constraints.required_source_classes - present_sources
    if missing_sources:
        reasons.append(
            f"missing required source classes: {sorted(source.value for source in missing_sources)}"
        )
    return reasons


def _scenario_active(candidate: AntigenCandidate, scenario: SpeciesScenario) -> bool:
    if candidate.candidate_id in scenario.escaped_antigens:
        return False
    if scenario.candidate_effect_scale.get(candidate.candidate_id, 1.0) == 0:
        return False
    class_i_available = bool(candidate.class_i_alleles - scenario.lost_class_i_alleles)
    class_ii_available = bool(candidate.class_ii_alleles - scenario.lost_class_ii_alleles)
    return class_i_available or class_ii_available


def _pair_score(cargo: Sequence[AntigenCandidate], weights: DesignWeights,
                scenario: SpeciesScenario) -> float:
    score = 0.0
    for first, second in combinations(cargo, 2):
        if not _scenario_active(first, scenario) or not _scenario_active(second, scenario):
            continue
        effect_scale = np.sqrt(
            scenario.candidate_effect_scale.get(first.candidate_id, 1.0)
            * scenario.candidate_effect_scale.get(second.candidate_id, 1.0)
        )
        if first.synergy_loadings:
            score += effect_scale * weights.synergy * float(
                np.dot(first.synergy_loadings, second.synergy_loadings)
            )
        if first.competition_loadings:
            score -= effect_scale * weights.competition * float(
                np.dot(first.competition_loadings, second.competition_loadings)
            )
    return score


def _score_design(cargo: Sequence[AntigenCandidate], scenarios: Sequence[SpeciesScenario],
                  weights: DesignWeights, schedule: ScheduleCandidate | None,
                  rank: int = 0) -> CargoRanking:
    schedule_first = 1.0 if schedule is None else schedule.first_order_scale
    schedule_second = 1.0 if schedule is None else schedule.second_order_scale
    schedule_penalty = 0.0 if schedule is None else schedule.objective_penalty
    subclones, class_i, class_ii = _coverage(cargo)
    scenario_scores: dict[str, float] = {}
    first_scores: dict[str, float] = {}
    interaction_scores: dict[str, float] = {}
    for scenario in scenarios:
        active = [candidate for candidate in cargo if _scenario_active(candidate, scenario)]
        scenario_subclones = frozenset().union(
            *(candidate.subclones for candidate in active)
        )
        scenario_class_i = frozenset().union(
            *(candidate.class_i_alleles - scenario.lost_class_i_alleles
              for candidate in active)
        )
        scenario_class_ii = frozenset().union(
            *(candidate.class_ii_alleles - scenario.lost_class_ii_alleles
              for candidate in active)
        )
        breadth = (
            weights.subclone_breadth * len(scenario_subclones)
            + weights.class_i_allele_breadth * len(scenario_class_i)
            + weights.class_ii_allele_breadth * len(scenario_class_ii)
        )
        first_order = sum(_candidate_score(candidate, scenario, weights) for candidate in cargo)
        interaction = _pair_score(cargo, weights, scenario) * scenario.interaction_scale
        total = (
            schedule_first * (first_order + breadth)
            + schedule_second * interaction
            - weights.antigen_count_penalty * len(cargo)
            - schedule_penalty
        )
        scenario_scores[scenario.name] = float(total)
        first_scores[scenario.name] = float(first_order + breadth)
        interaction_scores[scenario.name] = float(interaction)
    worst_scenario = min(scenario_scores, key=lambda name: (scenario_scores[name], name))
    worst = scenario_scores[worst_scenario]
    scenario_weights = np.asarray([scenario.weight for scenario in scenarios], float)
    values = np.asarray([scenario_scores[scenario.name] for scenario in scenarios], float)
    mean = float(np.average(values, weights=scenario_weights))
    robust = (1 - weights.robust_mean_weight) * worst + weights.robust_mean_weight * mean
    return CargoRanking(
        rank=rank,
        candidate_ids=tuple(candidate.candidate_id for candidate in cargo),
        schedule_name=None if schedule is None else schedule.name,
        robust_score=float(robust),
        worst_case_score=float(worst),
        weighted_mean_score=mean,
        worst_scenario=worst_scenario,
        scenario_scores=scenario_scores,
        first_order_score_by_scenario=first_scores,
        interaction_score_by_scenario=interaction_scores,
        covered_subclones=subclones,
        covered_class_i_alleles=class_i,
        covered_class_ii_alleles=class_ii,
    )


def _progress(cargo: Sequence[AntigenCandidate], constraints: CargoConstraints) -> int:
    subclones, class_i, class_ii = _coverage(cargo)
    score = min(
        constraints.min_class_i_antigens,
        sum(candidate.mhc_i_presentation >= constraints.class_i_cutoff for candidate in cargo),
    )
    score += min(
        constraints.min_class_ii_antigens,
        sum(candidate.mhc_ii_presentation >= constraints.class_ii_cutoff for candidate in cargo),
    )
    score += min(
        constraints.min_truncal_antigens,
        sum(candidate.truncality >= constraints.truncal_cutoff for candidate in cargo),
    )
    score += len(constraints.required_subclones & subclones)
    score += len(constraints.required_class_i_alleles & class_i)
    score += len(constraints.required_class_ii_alleles & class_ii)
    score += len(constraints.required_source_classes & {item.source_class for item in cargo})
    return score


def _combination_count(candidate_count: int, max_antigens: int) -> int:
    return sum(comb(candidate_count, size)
               for size in range(1, min(candidate_count, max_antigens) + 1))


def _beam_combinations(candidates: Sequence[AntigenCandidate], constraints: CargoConstraints,
                       scenarios: Sequence[SpeciesScenario], weights: DesignWeights,
                       beam_width: int) -> Iterable[tuple[int, ...]]:
    """Generate a deterministic score/coverage-diverse beam of combinations."""
    beam: list[tuple[int, ...]] = [()]
    for _depth in range(1, min(len(candidates), constraints.max_antigens) + 1):
        expanded: set[tuple[int, ...]] = set()
        for prefix in beam:
            start = prefix[-1] + 1 if prefix else 0
            for index in range(start, len(candidates)):
                indices = prefix + (index,)
                cargo = [candidates[item] for item in indices]
                if _is_feasible(cargo, constraints, partial=True):
                    expanded.add(indices)
        if not expanded:
            break
        ordered = sorted(expanded)
        if len(ordered) > beam_width:
            scored = []
            for indices in ordered:
                cargo = [candidates[item] for item in indices]
                score = _score_design(cargo, scenarios, weights, None).robust_score
                scored.append((indices, score, _progress(cargo, constraints)))
            half = max(1, beam_width // 2)
            by_score = sorted(scored, key=lambda item: (-item[1], item[0]))[:half]
            by_progress = sorted(
                scored, key=lambda item: (-item[2], -item[1], item[0])
            )[:beam_width]
            retained = {item[0] for item in by_score}
            for item in by_progress:
                if len(retained) >= beam_width:
                    break
                retained.add(item[0])
            ordered = sorted(retained)
        beam = ordered
        for indices in beam:
            cargo = [candidates[item] for item in indices]
            if _is_feasible(cargo, constraints):
                yield indices


def design_vaccine_cargo(
    candidates: Sequence[AntigenCandidate],
    constraints: CargoConstraints,
    *,
    scenarios: Sequence[SpeciesScenario] | None = None,
    weights: DesignWeights | None = None,
    schedules: Sequence[ScheduleCandidate] | None = None,
    top_k: int = 10,
    beam_width: int = 512,
    exact_enumeration_limit: int = 200_000,
) -> CargoDesignResult:
    """Rank feasible cargo/schedule designs with a robust maximin objective.

    Small spaces are enumerated exactly. Larger spaces use a deterministic beam
    that preserves both high-scoring and high-coverage partial designs. The
    result records which mode ran; beam-search optimality is not implied.
    """
    if not isinstance(constraints, CargoConstraints):
        raise TypeError("constraints must be CargoConstraints")
    if not isinstance(top_k, int) or isinstance(top_k, bool) or top_k < 1:
        raise ValueError("top_k must be a positive integer")
    if not isinstance(beam_width, int) or isinstance(beam_width, bool) or beam_width < 2:
        raise ValueError("beam_width must be an integer of at least 2")
    if exact_enumeration_limit < 1:
        raise ValueError("exact_enumeration_limit must be positive")
    candidates = tuple(candidates)
    if not candidates:
        raise InfeasibleCargoError(["no candidates supplied"])
    if any(not isinstance(candidate, AntigenCandidate) for candidate in candidates):
        raise TypeError("all candidates must be AntigenCandidate instances")
    ids = [candidate.candidate_id for candidate in candidates]
    duplicates = sorted({candidate_id for candidate_id in ids if ids.count(candidate_id) > 1})
    if duplicates:
        raise ValueError(f"candidate_id values must be unique: {duplicates}")
    wrong_species = sorted(candidate.candidate_id for candidate in candidates
                           if candidate.species != constraints.species)
    if wrong_species:
        raise ValueError(
            f"candidate species must match {constraints.species.value}: {wrong_species}"
        )
    _interaction_rank(candidates)
    weights = weights or DesignWeights()
    if scenarios is None:
        scenarios = (SpeciesScenario("nominal", constraints.species),)
    else:
        scenarios = tuple(scenarios)
        if not scenarios:
            raise ValueError("scenarios cannot be empty")
    if any(not isinstance(scenario, SpeciesScenario) for scenario in scenarios):
        raise TypeError("all scenarios must be SpeciesScenario instances")
    scenario_names = [scenario.name for scenario in scenarios]
    if len(set(scenario_names)) != len(scenario_names):
        raise ValueError("scenario names must be unique")
    if any(scenario.species != constraints.species for scenario in scenarios):
        raise ValueError("all scenarios must match the constraint species")
    unknown_scenario_ids = sorted({
        candidate_id
        for scenario in scenarios
        for candidate_id in (*scenario.escaped_antigens, *scenario.candidate_effect_scale)
        if candidate_id not in ids
    })
    if unknown_scenario_ids:
        raise ValueError(f"scenarios reference unknown candidates: {unknown_scenario_ids}")
    if schedules is None:
        schedule_options: tuple[ScheduleCandidate | None, ...] = (None,)
    else:
        schedules = tuple(schedules)
        if not schedules:
            raise ValueError("schedules cannot be empty when supplied")
        if any(not isinstance(schedule, ScheduleCandidate) for schedule in schedules):
            raise TypeError("all schedules must be ScheduleCandidate instances")
        names = [schedule.name for schedule in schedules]
        if len(set(names)) != len(names):
            raise ValueError("schedule names must be unique")
        schedule_options = schedules

    exclusions = []
    eligible = []
    for candidate in candidates:
        reasons = _eligibility_reasons(candidate, constraints)
        if reasons:
            exclusions.append(CandidateExclusion(candidate.candidate_id, reasons))
        else:
            eligible.append(candidate)
    eligible.sort(key=lambda candidate: candidate.candidate_id)
    diagnostics = _constraint_diagnostics(eligible, constraints)
    if diagnostics:
        raise InfeasibleCargoError(diagnostics)

    candidate_rankings = []
    for candidate in eligible:
        scores = {
            scenario.name: _candidate_score(candidate, scenario, weights)
            for scenario in scenarios
        }
        worst_scenario = min(scores, key=lambda name: (scores[name], name))
        values = np.asarray([scores[scenario.name] for scenario in scenarios])
        scenario_weights = np.asarray([scenario.weight for scenario in scenarios])
        mean = float(np.average(values, weights=scenario_weights))
        robust = (
            (1 - weights.robust_mean_weight) * scores[worst_scenario]
            + weights.robust_mean_weight * mean
        )
        candidate_rankings.append(
            CandidateRanking(candidate.candidate_id, float(robust), worst_scenario, scores)
        )
    candidate_rankings.sort(
        key=lambda ranking: (-ranking.robust_singleton_score, ranking.candidate_id)
    )

    count = _combination_count(len(eligible), constraints.max_antigens)
    if count <= exact_enumeration_limit:
        search_mode = "exact"
        index_sets: Iterable[tuple[int, ...]] = (
            indices
            for size in range(constraints.min_antigens,
                              min(len(eligible), constraints.max_antigens) + 1)
            for indices in combinations(range(len(eligible)), size)
            if _is_feasible([eligible[index] for index in indices], constraints)
        )
    else:
        search_mode = "beam"
        index_sets = _beam_combinations(eligible, constraints, scenarios, weights, beam_width)

    scored: list[CargoRanking] = []
    feasible_count = 0
    for indices in index_sets:
        cargo = [eligible[index] for index in indices]
        feasible_count += 1
        for schedule in schedule_options:
            scored.append(_score_design(cargo, scenarios, weights, schedule))
    if not scored:
        raise InfeasibleCargoError([
            "coverage requirements cannot be met simultaneously within max_antigens "
            "and source-class caps"
        ])
    scored.sort(
        key=lambda ranking: (
            -ranking.robust_score,
            -ranking.worst_case_score,
            len(ranking.candidate_ids),
            ranking.candidate_ids,
            ranking.schedule_name or "",
        )
    )
    rankings = tuple(
        CargoRanking(**{**ranking.__dict__, "rank": rank})
        for rank, ranking in enumerate(scored[:top_k], 1)
    )
    return CargoDesignResult(
        selected=rankings[0],
        rankings=rankings,
        candidate_rankings=tuple(candidate_rankings),
        exclusions=tuple(exclusions),
        search_mode=search_mode,
        feasible_designs_evaluated=feasible_count,
        species=constraints.species,
    )
