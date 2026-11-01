"""Per-day kill derived from a measured potency and a measured exposure, for canine lymphoma.

Adapted from the HS branch's `pkpd.py` (`emax_kill_rate`, `free_cns_concentration`, `margin`,
`DrugPKPD.min_access_to_close`). The HS module's stated purpose is unchanged: remove hand-set
potencies by COMPUTING the kill rate from two real, citable quantities -- an IC50 measured in cells
and an exposure -- through a standard exposure-response relation, and return a sub-growth rate whenever
the achievable concentration sits below the IC50, so the model can, and does, report "does not close".

THE MODEL (unchanged from HS)

A cytotoxic assay reports viability V = 1 / (1 + C/IC50) after `assay_days`. Reading the surviving
fraction as exponential decay:

    k(C) = ln(1 + C / IC50) / assay_days

WHAT IS ADAPTED, AND WHY

  * Exposure is a TIME-AVERAGED concentration (AUC over the dosing interval / interval) when the IC50
    came from a multi-day continuous-exposure assay, because comparing a 24-72 h continuous-exposure
    IC50 with a transient plasma peak overstates kill for short-half-life drugs. Where only a peak is
    available the peak is used and the result is flagged as an upper bound.
  * `required_ic50(...)` inverts the relation. Several agents have a measured exposure but NO measured
    IC50 in canine lymphoma (hydroxychloroquine, acalabrutinib). For those the honest, rigorous-model
    statement is not a kill rate but the HINGE: "it closes if its canine-lymphoma IC50 is at or below
    X". That converts an unmeasured potency into a testable threshold without inventing a value.
  * Every input is a `Measurement` (core/evidence.py), so a number cannot be read for a population it
    was not measured in without a written `transfer_to()`.

WHAT THIS DOES AND DOES NOT LICENSE

It licenses a MODEL-DERIVED kill rate from measured potency + measured exposure. It is not an
in-vivo efficacy measurement: protein binding, tumour penetration and schedule are folded into one
concentration. Where an input is transferred or assumed the derived rate is a transfer or an
assumption and is labelled so. This is a model, not veterinary advice.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from .core.evidence import (Disease, Measurement, Population, Provenance, Quantity, Species)

#: The bar: growth of the fastest resistant clone under full CHOP (core.lymphoma_catalogue).
GROWTH_PER_DAY = 0.0903


def emax_kill_rate(ic50_nM: float, concentration_nM: float, assay_days: float) -> float:
    """k = ln(1 + C/IC50) / assay_days. Monotonic in C; ln(2)/assay_days at C = IC50; 0 at C = 0."""
    if ic50_nM <= 0:
        raise ValueError("ic50_nM must be positive")
    if concentration_nM < 0:
        raise ValueError("concentration_nM must be >= 0")
    if assay_days <= 0:
        raise ValueError("assay_days must be positive")
    return math.log1p(concentration_nM / ic50_nM) / assay_days


def required_ic50_nM(concentration_nM: float, target_kill: float, assay_days: float) -> float:
    """The largest IC50 at which the exposure still delivers `target_kill` per day:
    C / (exp(target * assay_days) - 1). Inverse of `emax_kill_rate`."""
    if target_kill <= 0 or assay_days <= 0:
        raise ValueError("target_kill and assay_days must be positive")
    return concentration_nM / math.expm1(target_kill * assay_days)


def time_average_nM(auc_nM_h: float, interval_h: float) -> float:
    """Average concentration over a dosing interval = AUC_tau / tau."""
    if interval_h <= 0:
        raise ValueError("interval_h must be positive")
    return auc_nM_h / interval_h


def ng_per_ml_to_nM(ng_per_ml: float, mol_weight: float) -> float:
    """ng/mL to nM for a compound of molecular weight `mol_weight` (g/mol)."""
    return ng_per_ml / mol_weight * 1000.0


def fraction_of_interval_above(cmax_nM: float, ic50_nM: float, half_life_h: float,
                               interval_h: float) -> float:
    """One-compartment, IV-bolus-shaped decline: time above the IC50 is t_half * log2(Cmax / IC50).
    Returned as a fraction of the dosing interval, capped at 1. Used only for pulsed agents where the
    peak (not the average) is the comparator."""
    if cmax_nM <= ic50_nM:
        return 0.0
    t_above = half_life_h * math.log2(cmax_nM / ic50_nM)
    return min(1.0, t_above / interval_h)


@dataclass(frozen=True)
class DerivedPotency:
    """The outcome of deriving one agent's potency, with every input's provenance visible."""

    agent: str
    kill_per_day: float | None            # None => not derivable (an input is missing)
    basis: str                            # "DERIVED", "PARTIAL", "NOT DERIVABLE"
    ic50: Measurement | None
    concentration: Measurement | None
    assay_days: float | None
    required_ic50_nM_to_close: float | None = None   # the hinge, when the IC50 is missing
    note: str = ""

    @property
    def closes(self) -> bool | None:
        if self.kill_per_day is None:
            return None
        return self.kill_per_day > GROWTH_PER_DAY

    @property
    def provenances(self) -> tuple:
        return tuple(m.provenance for m in (self.ic50, self.concentration) if m is not None)

    @property
    def fully_measured(self) -> bool:
        return (self.ic50 is not None and self.concentration is not None
                and all(p in (Provenance.MEASURED,) for p in self.provenances))


def derive(agent: str, ic50: Measurement | None, concentration: Measurement | None,
           assay_days: float | None, *, access: float = 1.0, target_kill: float = GROWTH_PER_DAY,
           note: str = "") -> DerivedPotency:
    """Derive k from measured inputs. If the IC50 is absent, return the HINGE instead of a made-up
    kill rate. `access` scales the concentration for a compartment (default: systemic)."""
    if concentration is None:
        return DerivedPotency(agent, None, "NOT DERIVABLE", ic50, None, assay_days, None,
                              note or "no exposure measurement")
    c = concentration.value * access
    if ic50 is None:
        need = required_ic50_nM(c, target_kill, assay_days or 3.0)
        return DerivedPotency(agent, None, "NOT DERIVABLE", None, concentration, assay_days, need,
                              note or "no IC50 in canine lymphoma; the hinge is the IC50 it needs")
    k = emax_kill_rate(ic50.value, c, assay_days)
    basis = ("DERIVED" if all(m.provenance is Provenance.MEASURED for m in (ic50, concentration))
             else "PARTIAL")
    return DerivedPotency(agent, k, basis, ic50, concentration, assay_days, None, note)


def dog_lymphoma(agent: str, disease: Disease = Disease.CANINE_LYMPHOMA) -> Population:
    """Population helper: a dog (or canine cell) with lymphoma, for a named agent."""
    return Population(Species.DOG, disease, agent=agent)


def cells_lymphoma(agent: str, disease: Disease = Disease.CANINE_LYMPHOMA) -> Population:
    """Canine lymphoma cells in vitro (cell lines / primary cells), for a named agent."""
    return Population(Species.IN_VITRO, disease, agent=agent,
                      note="canine lymphoma cell line or primary cells")
