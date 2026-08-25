"""Probabilistic ten-year durability: P(no second primary establishes), with confidence intervals
and a value-of-information ranking over the inputs.

WHY THIS EXISTS
---------------
``maintenance_durability`` returns a *categorical* verdict per genotype x site (DURABLE_10Y,
SURVEILLANCE_DEPENDENT, ...). That is honest about the *ordering* of robustness but hides two things
the durability question actually turns on: (1) the rate at which a predisposed dog throws a NEW
primary over the horizon (the branching model drops it once margin > 0), and (2) how uncertain the
answer is. This module puts both back: it computes a probability with an interval, and it says which
single measurement would most reduce that uncertainty. It converts "coverage exists, model-based"
into "P(10-year durable) = x, 90% CI [lo, hi], and the highest-value experiment is Y."

THE MODEL (emergence x per-event escape, Poisson horizon)
---------------------------------------------------------
Over the maintenance horizon a predisposed dog initiates would-be second primaries at expected count
``Lambda`` (calibrated so that WITHOUT maintenance, exp(-Lambda) reproduces the observed adjuvant
recurrence-free fraction -- anchored to the canine-HS adjuvant CCNU cohort). Each would-be primary is
a single founding cell the maintenance pill must extinguish. It escapes with probability

    p_esc = 1 - (1 - p_reach_fail) * (1 - p_reroute * (1 - eps_surv))

  * ``p_reach_fail`` -- the drug fails to hold margin > 0 at that founding cell (site not reached,
    CNS penetration below threshold, or an adherence gap). A DRUG-PRESENCE risk, shared by every
    genotype; it is high at the CSF compartment and low at the lung. (Gaps 5, 6.)
  * ``p_reroute``    -- given the drug IS present and margin > 0, the target is bypassed over a decade
    of selective pressure. This is the LOCK axis: ~0 for MTAP (you cannot reroute around a deleted
    gene), moderate for a pathway target. (Gaps 3, 4.)
  * ``eps_surv``     -- detect-and-switch efficiency (serial ctDNA + the genotype switch tree) claws
    back the reroute term; 0 without surveillance. (Gap 3.)

Then, treating founding cells as independent (Poisson),

    P(no second primary over horizon) = exp(-Lambda * p_esc).

Every input carries an uncertainty distribution with stated provenance; Monte Carlo propagates them to
a median and a 90% CI, and a variance-based one-at-a-time analysis ranks the inputs by how much fixing
each would shrink the spread (value of information). If margin <= 0 the founding cell is itself
supercritical, p_esc -> 1, and P collapses to the no-maintenance floor exp(-Lambda) -- the model is
not rigged to pass.

THIS RAISES CONFIDENCE; IT DOES NOT PROVE DURABILITY. A model upgrade sharpens the estimate, bounds
it, and prioritises the next experiment. Only the experiments it points to (an adjuvant recurrence-
free-survival study, a tumour target-engagement biopsy, a canine PRMT5i sensitivity, a CSF PK) close
the gap. This is an analysis, not veterinary advice.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .core.evidence import Provenance

HORIZON_YEARS = 10
DEFAULT_DRAWS = 40_000
DEFAULT_SEED = 20260824  # fixed for reproducibility (Date/random are avoided elsewhere by policy)


@dataclass(frozen=True)
class Param:
    """One uncertain input: a Beta (for probabilities) or lognormal (for Lambda) prior with a stated
    central value, a 90% interval, and provenance. Priors are wide and documented, not point guesses."""

    name: str
    kind: str            # "beta" | "lognormal" | "fixed"
    center: float        # median / point value
    lo: float            # 5th percentile (for the interval); ignored for "fixed"
    hi: float            # 95th percentile
    provenance: Provenance
    source: str

    def sample(self, rng: np.random.Generator, n: int) -> np.ndarray:
        if self.kind == "fixed":
            return np.full(n, self.center)
        if self.kind == "lognormal":
            mu = np.log(self.center)
            # sigma from the 90% interval width in log space (z_0.95 = 1.6449)
            sigma = (np.log(self.hi) - np.log(self.lo)) / (2 * 1.6449)
            return np.exp(rng.normal(mu, sigma, n))
        if self.kind == "beta":
            a, b = _beta_from_ci(self.center, self.lo, self.hi)
            return rng.beta(a, b, n)
        raise ValueError(f"unknown kind {self.kind}")


def _beta_from_ci(center: float, lo: float, hi: float) -> tuple[float, float]:
    """Method-of-moments Beta from a central value and a rough 90% interval.

    Uses the interval half-width as ~1.645 sigma to set the variance, then solves a, b from the
    mean/variance. Clamped so the concentration stays sensible for wide priors near 0/1."""
    m = min(max(center, 1e-4), 1 - 1e-4)
    sd = max((hi - lo) / (2 * 1.6449), 1e-3)
    var = min(sd * sd, m * (1 - m) * 0.98)  # variance must stay below the Bernoulli bound
    conc = m * (1 - m) / var - 1
    conc = max(conc, 0.5)
    return m * conc, (1 - m) * conc


# ---- Inputs, each with provenance -------------------------------------------------------------

def lambda_param() -> Param:
    """Expected would-be second primaries over the horizon, calibrated so exp(-Lambda) matches the
    observed adjuvant recurrence-free fraction. Anchored to the canine-HS adjuvant CCNU cohort
    (median relapse ~201-243 d; ~10/16 relapsed/metastasised -> ~10-year RFS well under 0.3 without a
    genotype-matched maintenance arm), PMID 19453368. Wide interval; extrapolation to 10 y is ASSUMED."""
    # exp(-1.6) ~ 0.20 baseline 10 y RFS; interval spans exp(-0.8)=0.45 to exp(-3.0)=0.05.
    return Param("Lambda_second_primaries", "lognormal", 1.6, 0.8, 3.0,
                 Provenance.DERIVED, "canine-HS adjuvant CCNU recurrence baseline, PMID 19453368; "
                 "10-year extrapolation assumed")


# Per-site drug-presence failure (margin not held at the founding cell). Tied to reach/penetration.
def reach_fail_param(site_name: str) -> Param:
    table = {
        "Lung / disseminated": (0.05, 0.02, 0.12,
                                "systemic exposure; MEK inputs measured in canine HS (PMID 39202410)"),
        "Brain -- local delivery (cavity implant / CED / SRS)": (
            0.08, 0.03, 0.18, "barrier-free local delivery; radiation control demonstrated PMID 34556593"),
        "Brain -- systemic penetration": (
            0.30, 0.15, 0.55, "canine CNS Kp,uu unmeasured; brain-penetrant TNG456 in Ph I/II PMID 42150143"),
        "Leptomeninges / CSF": (
            0.70, 0.45, 0.90, "no agent given intrathecally in any species; fluid-to-cell fraction unmeasured"),
    }
    c, lo, hi, src = table.get(site_name, (0.30, 0.15, 0.55, "unspecified site"))
    return Param(f"p_reach_fail[{site_name}]", "beta", c, lo, hi, Provenance.ASSUMED, src)


# Per-lock reroute probability over the horizon, given the drug is present (margin > 0). Keyed to the
# maintenance_durability.Lock kind, so the four robustness classes get distinct, ordered priors.
_REROUTE_PRIORS = {
    # lock kind : (center, lo, hi, source)
    "LOCKED": (0.02, 0.005, 0.06,
               "MTAP deletion non-reroutable; residual = unknown synthetic-lethal-dependency bypass"),
    "REROUTABLE": (0.35, 0.15, 0.60,
                   "pathway (MEK) bypass over 10 y; human targeted-adjuvant recurrence + PMID 39576953"),
    "DEPENDENCY": (0.30, 0.12, 0.55,
                   "strong dependency (PI3K / CDK4/6) with known resistance routes"),
    "FLOOR": (0.60, 0.35, 0.85,
              "no targeted anchor; immune + cycled chemo backstop, the weakest hold"),
}


def reroute_param(lock_kind: str) -> Param:
    c, lo, hi, src = _REROUTE_PRIORS.get(lock_kind, _REROUTE_PRIORS["REROUTABLE"])
    return Param(f"p_reroute[{lock_kind.lower()}]", "beta", c, lo, hi, Provenance.ASSUMED, src)


def surveillance_param(with_surveillance: bool) -> Param:
    if not with_surveillance:
        return Param("eps_surv", "fixed", 0.0, 0.0, 0.0, Provenance.ASSUMED, "no monitoring arm")
    # ctDNA/MRD detect-and-switch efficiency; transferred from human MRD-guided adjuvant data
    # (IMvigor011, PMID 41124204). Transfer to canine HS is ASSUMED (no validated canine-HS ctDNA assay).
    return Param("eps_surv", "beta", 0.70, 0.40, 0.90, Provenance.TRANSFERRED,
                 "ctDNA MRD-guided switch efficiency, PMID 41124204; canine-HS transfer assumed")


@dataclass(frozen=True)
class Scenario:
    genotype: str
    site: str
    lock_kind: str             # "LOCKED" | "REROUTABLE" | "DEPENDENCY" | "FLOOR" (maintenance_durability.Lock)
    with_surveillance: bool
    margin: float | None       # from pkpd; None where no measured IC50+Cmax (dependency/floor tiers)

    @property
    def locked(self) -> bool:
        return self.lock_kind == "LOCKED"


@dataclass(frozen=True)
class DurabilityProbability:
    scenario: Scenario
    p_median: float
    p_lo: float                # 5th percentile
    p_hi: float                # 95th percentile
    voi: list[tuple[str, float]] = field(default_factory=list)  # (input, variance-share), ranked


def _p_decade(lam, reach_fail, reroute, eps, margin_ok) -> np.ndarray:
    """Vectorised P(no second primary). margin_ok is a boolean array; where False, p_esc -> 1."""
    p_esc = 1.0 - (1.0 - reach_fail) * (1.0 - reroute * (1.0 - eps))
    p_esc = np.where(margin_ok, p_esc, 1.0)
    return np.exp(-lam * p_esc)


def assess(scenario: Scenario, draws: int = DEFAULT_DRAWS,
           seed: int = DEFAULT_SEED) -> DurabilityProbability:
    """Monte-Carlo P(10-year durable) for one scenario, with a 90% CI and a value-of-information rank."""
    rng = np.random.default_rng(seed)
    params = {
        "Lambda": lambda_param(),
        "reach_fail": reach_fail_param(scenario.site),
        "reroute": reroute_param(scenario.lock_kind),
        "eps_surv": surveillance_param(scenario.with_surveillance),
    }
    draws_by = {k: p.sample(rng, draws) for k, p in params.items()}
    # margin_ok: if a measured margin exists and is <= 0, the founding cell is supercritical.
    margin_ok = np.full(draws, True) if scenario.margin is None else np.full(draws, scenario.margin > 0)

    p = _p_decade(draws_by["Lambda"], draws_by["reach_fail"], draws_by["reroute"],
                  draws_by["eps_surv"], margin_ok)
    p_median = float(np.median(p))
    p_lo, p_hi = (float(np.percentile(p, 5)), float(np.percentile(p, 95)))

    # Value of information: variance of P remaining if each input were fixed at its median (the drop
    # from total variance is that input's share). One-at-a-time; ranked descending.
    total_var = float(np.var(p))
    voi = []
    for key, prm in params.items():
        if prm.kind == "fixed":
            continue
        fixed = dict(draws_by)
        fixed[key] = np.full(draws, prm.center)
        p_fixed = _p_decade(fixed["Lambda"], fixed["reach_fail"], fixed["reroute"],
                            fixed["eps_surv"], margin_ok)
        share = 0.0 if total_var <= 0 else max(0.0, (total_var - float(np.var(p_fixed))) / total_var)
        voi.append((prm.name, round(share, 3)))
    voi.sort(key=lambda t: t[1], reverse=True)
    return DurabilityProbability(scenario, round(p_median, 3), round(p_lo, 3), round(p_hi, 3), voi)


# ---- Scenario construction from the durability tiers/sites ------------------------------------

def _scenarios(with_surveillance: bool) -> list[Scenario]:
    from . import maintenance_durability as md
    out: list[Scenario] = []
    for tier in md.TIERS:
        for site in md.SITES:
            d = md.durability(tier, site)
            out.append(Scenario(tier.genotype, site.name, tier.lock.name, with_surveillance, d.margin))
    return out


def probabilistic_grid(with_surveillance: bool = False,
                       draws: int = DEFAULT_DRAWS) -> list[DurabilityProbability]:
    """P(10-year durable) with CI for every genotype x site, at a fixed surveillance setting."""
    return [assess(s, draws=draws) for s in _scenarios(with_surveillance)]


def surveillance_lift(genotype_startswith: str = "MAPK",
                      site_name: str = "Lung / disseminated",
                      draws: int = DEFAULT_DRAWS) -> dict:
    """How much detect-and-switch raises the reroutable tier's P(decade) -- the concrete value of the
    surveillance arm, off vs on."""
    from . import maintenance_durability as md
    tier = next(t for t in md.TIERS if t.genotype.startswith(genotype_startswith))
    site = next(s for s in md.SITES if s.name == site_name)
    margin = md.durability(tier, site).margin
    lk = tier.lock.name
    off = assess(Scenario(tier.genotype, site.name, lk, False, margin), draws=draws)
    on = assess(Scenario(tier.genotype, site.name, lk, True, margin), draws=draws)
    return {
        "genotype": tier.genotype, "site": site.name,
        "P_no_surveillance": off.p_median, "P_with_surveillance": on.p_median,
        "absolute_lift": round(on.p_median - off.p_median, 3),
    }


def headline(draws: int = DEFAULT_DRAWS) -> str:
    """One paragraph: the probabilistic durability result and what it changes."""
    from . import maintenance_durability as md
    lung = "Lung / disseminated"
    mtap = next(t for t in md.TIERS if t.lock is md.Lock.LOCKED)
    mapk = next(t for t in md.TIERS if t.genotype.startswith("MAPK"))
    m_mtap = md.durability(mtap, md.SITES[0]).margin
    m_mapk = md.durability(mapk, md.SITES[0]).margin
    p_mtap = assess(Scenario(mtap.genotype, lung, mtap.lock.name, False, m_mtap), draws=draws)
    p_mapk_off = assess(Scenario(mapk.genotype, lung, mapk.lock.name, False, m_mapk), draws=draws)
    p_mapk_on = assess(Scenario(mapk.genotype, lung, mapk.lock.name, True, m_mapk), draws=draws)
    return (
        "Probabilistic ten-year durability (P = no second primary establishes), lung site, 90% CI: "
        f"MTAP (locked) {p_mtap.p_median:.2f} [{p_mtap.p_lo:.2f}, {p_mtap.p_hi:.2f}]; "
        f"MAPK majority WITHOUT surveillance {p_mapk_off.p_median:.2f} "
        f"[{p_mapk_off.p_lo:.2f}, {p_mapk_off.p_hi:.2f}], WITH detect-and-switch "
        f"{p_mapk_on.p_median:.2f} [{p_mapk_on.p_lo:.2f}, {p_mapk_on.p_hi:.2f}]. So the lock buys a "
        "high, tight probability; the reroutable majority is a wide, lower probability that the "
        "surveillance loop measurably lifts. The dominant uncertainty (value of information) differs "
        "by scenario -- see voi on each result -- which names the single experiment that most reduces "
        "the spread. This is calibrated model confidence with intervals, not proof of a decade."
    )


if __name__ == "__main__":
    print(headline())
    print()
    print("P(10-year durable) grid -- WITHOUT surveillance:")
    for d in probabilistic_grid(with_surveillance=False):
        top = d.voi[0] if d.voi else ("-", 0.0)
        print(f"  {d.scenario.genotype:28} | {d.scenario.site:44} | "
              f"P={d.p_median:.2f} [{d.p_lo:.2f},{d.p_hi:.2f}] | top VoI: {top[0]} ({top[1]})")
    print()
    print("surveillance lift (MAPK, lung):", surveillance_lift())
