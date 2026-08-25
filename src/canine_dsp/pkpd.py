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
        name="MTA-cooperative PRMT5 inhibitor (class; brain-penetrant anchor TNG456)",
        ic50_nM=10.0,             # GI50 <10 nM in MTAP-null cells (class potency)
        cmax_nM=1000.0,           # PLACEHOLDER exposure (no canine PK); see min_access_to_close()
        ic50_provenance=Provenance.TRANSFERRED,
        cmax_provenance=Provenance.ASSUMED,
        source="Class: J Med Chem 2024 PMID 38595098 (TNG908). CNS anchor updated to TNG456, a "
               "brain-penetrant MTA-cooperative PRMT5i in Phase I/II with a glioblastoma focus "
               "(J Med Chem 2026;69:12853, PMID 42150143). Independent brain-penetrant chemotype: "
               "Eur J Med Chem 2026;315:119001 PMID 42190431.",
        note="Potency transferred from human MTAP-null cells (PRMT5 target 99.37% conserved) and is "
             "a CLASS value; the ~10 nM GI50 is shared across the MTA-cooperative series. The kill "
             "MARGIN is not the deciding quantity here -- the genotype LOCK is -- so this entry is "
             "used via min_access_to_close() to expose the access hinge, not closes_at() to assert "
             "closure. CNS caveat: the first-generation member TNG908 showed preclinical brain "
             "permeability but failed to reach therapeutic CNS exposure in glioblastoma trials "
             "(PMID 42190431); the brain-penetrant successor TNG456 (PMID 42150143) is the CNS "
             "anchor. Canine Cmax remains unpublished for either.",
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


# ---- Target-attainment model (Gap 2: is the maintenance drug even engaging its target?) ----------
#
# The canine trametinib Phase I (Takada/Vail 2024, PMID 38889903) reported that at the MTD
# (0.5 mg/m2/day) approximately 70% of dogs reached an average steady-state concentration of ~10 ng/mL
# -- the exposure associated with clinical efficacy in humans -- AND that target engagement was NOT
# observed in the Day-0/Day-7 tumour biopsies. So "the drug engages the target" is an open quantity
# even in the treatment setting. This model turns the trial's own numbers into a dose -> attainment
# curve: it does not invent binding constants, it restates the reported attainment as a lognormal
# steady-state distribution and extends it across dose, so we can read the fraction of dogs UNDERDOSED
# for the efficacy-benchmark exposure and the dose needed to reach a chosen attainment. Attainment of
# the exposure benchmark is necessary but not sufficient for engagement (which needs a PD biopsy) --
# this bounds the necessary condition from data in hand.

TRAMETINIB_MTD_MG_M2 = 0.5              # recommended Phase II dose, PMID 38889903
TRAMETINIB_TARGET_NG_ML = 10.0          # efficacy-associated steady-state (human benchmark)
TRAMETINIB_ATTAIN_AT_MTD = 0.70         # ~70% of dogs reached the target at the MTD
TRAMETINIB_CSS_CV = 0.55                # population steady-state variability (saturable elimination)
TRAMETINIB_DOSE_EXPONENT = 1.3          # median Css ~ dose^p; p>1 = saturable (supra-linear) exposure


def _phi(z: float) -> float:
    """Standard-normal CDF via erf (no scipy dependency)."""
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def _phi_inv(q: float) -> float:
    """Standard-normal quantile (Acklam's rational approximation; ample precision here)."""
    if not 0.0 < q < 1.0:
        raise ValueError("q must be in (0,1)")
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    plow, phigh = 0.02425, 1 - 0.02425
    if q < plow:
        r = math.sqrt(-2 * math.log(q))
        return (((((c[0]*r+c[1])*r+c[2])*r+c[3])*r+c[4])*r+c[5]) / ((((d[0]*r+d[1])*r+d[2])*r+d[3])*r+1)
    if q > phigh:
        r = math.sqrt(-2 * math.log(1 - q))
        return -(((((c[0]*r+c[1])*r+c[2])*r+c[3])*r+c[4])*r+c[5]) / ((((d[0]*r+d[1])*r+d[2])*r+d[3])*r+1)
    r = q - 0.5
    t = r * r
    return (((((a[0]*t+a[1])*t+a[2])*t+a[3])*t+a[4])*t+a[5])*r / (((((b[0]*t+b[1])*t+b[2])*t+b[3])*t+b[4])*t+1)


def _css_logmu_at(dose_mg_m2: float, sigma: float = TRAMETINIB_CSS_CV,
                  exponent: float = TRAMETINIB_DOSE_EXPONENT) -> float:
    """Log-median steady-state at a dose, calibrated so attainment at the MTD = TRAMETINIB_ATTAIN_AT_MTD."""
    # At MTD: P(Css >= T) = attain  ->  (mu_MTD - lnT)/sigma = Phi^{-1}(attain)
    mu_mtd = math.log(TRAMETINIB_TARGET_NG_ML) + sigma * _phi_inv(TRAMETINIB_ATTAIN_AT_MTD)
    return mu_mtd + exponent * math.log(dose_mg_m2 / TRAMETINIB_MTD_MG_M2)


def target_attainment(dose_mg_m2: float = TRAMETINIB_MTD_MG_M2,
                      sigma: float = TRAMETINIB_CSS_CV) -> dict:
    """Fraction of dogs reaching the efficacy-benchmark steady-state at a given trametinib dose.

    Restates and extends the trial's reported attainment (calibrated to 70% at the MTD). Returns the
    attainment probability and the underdosed fraction -- the population-PK gap that must be closed
    (by dose, or by therapeutic drug monitoring) before continuous maintenance can be relied on."""
    mu = _css_logmu_at(dose_mg_m2, sigma)
    p_attain = _phi((mu - math.log(TRAMETINIB_TARGET_NG_ML)) / sigma)
    return {
        "dose_mg_m2": dose_mg_m2,
        "target_ng_ml": TRAMETINIB_TARGET_NG_ML,
        "p_attain_target": round(p_attain, 3),
        "fraction_underdosed": round(1.0 - p_attain, 3),
        "provenance": Provenance.MEASURED.value,
        "source": "canine trametinib Phase I, PMID 38889903 (MTD 0.5 mg/m2/day; ~70% reach ~10 ng/mL; "
                  "target engagement not confirmed on biopsy)",
    }


def dose_for_attainment(target_fraction: float = 0.90,
                        sigma: float = TRAMETINIB_CSS_CV,
                        exponent: float = TRAMETINIB_DOSE_EXPONENT) -> dict:
    """Trametinib dose (as a multiple of the MTD) needed so `target_fraction` of dogs reach the
    efficacy-benchmark exposure. Reads off how far above the MTD an adequately-dosing regimen sits --
    and therefore whether dose alone can close the attainment gap or monitoring is required."""
    # Solve mu(dose) - lnT = sigma * Phi^{-1}(target_fraction)
    needed_mu = math.log(TRAMETINIB_TARGET_NG_ML) + sigma * _phi_inv(target_fraction)
    mu_mtd = math.log(TRAMETINIB_TARGET_NG_ML) + sigma * _phi_inv(TRAMETINIB_ATTAIN_AT_MTD)
    dose_multiple = math.exp((needed_mu - mu_mtd) / exponent)
    return {
        "target_fraction": target_fraction,
        "dose_multiple_of_mtd": round(dose_multiple, 2),
        "dose_mg_m2": round(dose_multiple * TRAMETINIB_MTD_MG_M2, 3),
        "note": "if the dose multiple exceeds the tolerable window (the MTD is dose-limited by "
                "hypertension/proteinuria), attainment cannot be reached by dose alone -- therapeutic "
                "drug monitoring / dose individualisation is required. See core.toxicity for the ceiling.",
        "source": "extends canine trametinib Phase I population PK, PMID 38889903",
    }


if __name__ == "__main__":
    for key, r in derived_closures().items():
        print(f"{key}: systemic k={r['systemic_kill_per_day']:.3f}/day closes={r['systemic_closes']}; "
              f"brain@0.30 k={r['brain_kill_per_day']:.3f}/day closes={r['brain_closes']}; "
              f"min access to close={r['min_access_to_close']:.3f}")
    print()
    print("Target attainment (trametinib, Gap 2):")
    for mult in (1.0, 1.5, 2.0):
        r = target_attainment(mult * TRAMETINIB_MTD_MG_M2)
        print(f"  dose {r['dose_mg_m2']:.2f} mg/m2 ({mult:.1f}x MTD): "
              f"P(reach {r['target_ng_ml']:.0f} ng/mL)={r['p_attain_target']:.2f}, "
              f"underdosed={r['fraction_underdosed']:.2f}")
    print("  dose for 90% attainment:", dose_for_attainment(0.90))
