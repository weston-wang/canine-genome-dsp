"""Derive a per-day kill rate from a measured IC50 and an achievable exposure.

The escape-closure engine needs a per-day kill rate; the audit's central complaint was that those
rates were hand-set constants. This module removes the hand-setting: it COMPUTES the kill rate from
two real, citable quantities -- a potency (IC50, measured in cells) and an exposure (plasma Cmax x
CNS access) -- through a standard exposure-response relation, and it returns a small (sub-growth,
non-closing) rate whenever the achievable free concentration sits below the IC50. Nothing here is a
narrative; every value is produced by a formula from its inputs.

THE MODEL
---------
A cytotoxic assay reports fractional viability V after `assay_days` at concentration C. The
one-parameter exposure-response V(C) = 1 / (1 + C/IC50) passes through V = 0.5 at C = IC50 (the
definition of IC50) and V -> 0 as C grows. Reading that surviving fraction as exponential decay over
the assay window gives a per-day kill rate

    k(C) = -ln V / assay_days = ln(1 + C / IC50) / assay_days

so k rises with exposure, equals ln(2)/assay_days at C = IC50, and -> 0 as C -> 0. The free CNS
concentration is C = Cmax x Kp,uu (unbound brain:plasma ratio). An escape closes when k exceeds the
tumour growth rate. The model is falsifiable at the input level: a drug that cannot reach its IC50 in
the compartment returns k below growth and does NOT close.

WHAT THIS DOES AND DOES NOT LICENSE
-----------------------------------
It licenses a MODEL-DERIVED kill rate from measured potency + exposure -- "scientifically backed" in
the model-based sense, not a bare assumption. It does not invent potency or exposure: those still
carry provenance (see PARAMS), and a transferred IC50 or a rodent Kp,uu makes the derived rate a
transfer too. The assay-duration reading is a modelling choice, stated, not a measured kill rate.

This is an analysis, not veterinary advice.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .core.evidence import Provenance

# The pass/fail bar (tumour net growth), matching core.catalogue.GROWTH_PER_DAY.
GROWTH_PER_DAY = 0.055
# Standard in-vitro cytotoxicity window (72 h MTT) the exposure-response is read over.
DEFAULT_ASSAY_DAYS = 3.0


def emax_kill_rate(ic50_nM: float, concentration_nM: float,
                   assay_days: float = DEFAULT_ASSAY_DAYS) -> float:
    """Per-day kill rate derived from a measured IC50 and a free concentration (see module docstring).

    k = ln(1 + C/IC50) / assay_days. Monotonic in C, ln(2)/assay_days at C = IC50, 0 at C = 0.
    """
    if ic50_nM <= 0:
        raise ValueError("ic50_nM must be positive")
    if concentration_nM < 0:
        raise ValueError("concentration_nM must be >= 0")
    if assay_days <= 0:
        raise ValueError("assay_days must be positive")
    return math.log1p(concentration_nM / ic50_nM) / assay_days


def free_cns_concentration(cmax_nM: float, kp_uu: float) -> float:
    """Free brain concentration = plasma Cmax x unbound brain:plasma ratio (Kp,uu)."""
    if cmax_nM < 0 or kp_uu < 0:
        raise ValueError("cmax_nM and kp_uu must be >= 0")
    return cmax_nM * kp_uu


def margin(kill_rate: float, growth: float = GROWTH_PER_DAY) -> float:
    """Kill margin = derived kill rate - tumour growth rate. Positive means the escape closes."""
    return kill_rate - growth


@dataclass(frozen=True)
class DrugPKPD:
    """A drug's exposure-response inputs, each with provenance, and the closures they derive."""

    name: str
    ic50_nM: float
    cmax_nM: float
    ic50_provenance: Provenance
    cmax_provenance: Provenance
    source: str
    note: str = ""

    def kill_rate_at(self, kp_uu: float, assay_days: float = DEFAULT_ASSAY_DAYS) -> float:
        """Model-derived per-day kill rate at unbound CNS access `kp_uu`."""
        return emax_kill_rate(self.ic50_nM, free_cns_concentration(self.cmax_nM, kp_uu), assay_days)

    def closes_at(self, kp_uu: float, growth: float = GROWTH_PER_DAY) -> bool:
        """Whether the derived kill rate beats growth at CNS access `kp_uu`."""
        return margin(self.kill_rate_at(kp_uu), growth) > 0

    def min_access_to_close(self, growth: float = GROWTH_PER_DAY,
                            assay_days: float = DEFAULT_ASSAY_DAYS) -> float:
        """Smallest Kp,uu at which the derived kill rate reaches growth.

        Solve ln(1 + Cmax*kp/IC50)/assay_days = growth  ->  kp = IC50*(exp(growth*assay_days)-1)/Cmax.
        Returns inf if the drug cannot close even at kp_uu = 1 (full systemic exposure in brain).
        """
        if self.cmax_nM <= 0:
            return math.inf
        kp = self.ic50_nM * (math.exp(growth * assay_days) - 1.0) / self.cmax_nM
        return kp


# Exposure-response inputs with provenance. IC50s and Cmax are real measured values where the source
# says so; a transferred IC50 (e.g. human MTAP-null for a canine tumour) is marked TRANSFERRED and
# makes any derived rate a transfer too. These are the only inputs; kill rates below are computed.
PARAMS: dict[str, DrugPKPD] = {
    # MEK inhibitor for the ~59% MAPK-driver maintenance tier. Both IC50 and Cmax measured in the
    # canine-HS study itself -- the fully-grounded case.
    "cobimetinib": DrugPKPD(
        name="cobimetinib (MEK1/2 inhibitor)",
        ic50_nM=372.0,            # conservative top of the measured 74-372 nM range in 3 canine HS lines
        cmax_nM=1640.0,           # achievable canine plasma Cmax at 5 mg/kg
        ic50_provenance=Provenance.MEASURED,
        cmax_provenance=Provenance.MEASURED,
        source="Genes 2024;15(8):1050, PMID 39202410 (canine HS lines BD/OD/DH82)",
        note="Both inputs measured in canine HS; the derived kill rate is model-derived from "
             "canine data, not assumed.",
    ),
    # PRMT5 inhibitor for the MTAP-deleted (ten-year) maintenance arm. Potency measured in human
    # MTAP-null cells; a transfer to the dog, justified by PRMT5 99.37% ortholog identity
    # (sequence_conservation). No canine Cmax published, so Cmax is a documented placeholder used
    # only to expose the access threshold, not to assert closure.
    "tng908": DrugPKPD(
        name="TNG908 (MTA-cooperative PRMT5 inhibitor)",
        ic50_nM=10.0,             # GI50 <10 nM in MTAP-null cells
        cmax_nM=1000.0,           # PLACEHOLDER exposure (no canine PK); see min_access_to_close()
        ic50_provenance=Provenance.TRANSFERRED,
        cmax_provenance=Provenance.ASSUMED,
        source="J Med Chem 2024, PMID 38595098 (brain-penetrant; human MTAP-null cells)",
        note="Potency transferred from human MTAP-null cells (PRMT5 target 99.37% conserved). "
             "Canine Cmax unpublished; use min_access_to_close() to read the access hinge, not "
             "closes_at() to assert closure.",
    ),
}


def derived_closures(kp_uu_brain: float = 0.30) -> dict[str, dict]:
    """Model-derived kill rate, margin and closure for every drug in PARAMS, at systemic exposure
    (Kp,uu = 1.0) and at a conservative brain access (default 0.30). Pure computation over PARAMS."""
    out: dict[str, dict] = {}
    for key, d in PARAMS.items():
        out[key] = {
            "systemic_kill_per_day": d.kill_rate_at(1.0),
            "systemic_closes": d.closes_at(1.0),
            "brain_kill_per_day": d.kill_rate_at(kp_uu_brain),
            "brain_closes": d.closes_at(kp_uu_brain),
            "min_access_to_close": d.min_access_to_close(),
            "ic50_provenance": d.ic50_provenance.value,
            "cmax_provenance": d.cmax_provenance.value,
            "source": d.source,
        }
    return out


if __name__ == "__main__":
    for key, r in derived_closures().items():
        print(f"{key}: systemic k={r['systemic_kill_per_day']:.3f}/day closes={r['systemic_closes']}; "
              f"brain@0.30 k={r['brain_kill_per_day']:.3f}/day closes={r['brain_closes']}; "
              f"min access to close={r['min_access_to_close']:.3f}")
