"""Bridging real, measurable pharmacology to the `max_kill_2` parameter the resistance model asserts.

WHY THIS MODULE EXISTS
----------------------
`mapk_scenarios` reports that a second-drug potency of `max_kill_2 = 0.08` per day reverses every
resistant clone's growth margin, producing 100% durable response flat to ten years -- and that
`max_kill_2 = 0.05` does not. Asked whether 0.08 is *achievable*, the model could not answer,
because `max_kill_2` entered it as a bare asserted number with no link to any quantity anyone can
measure. That is the gap this module closes: it converts real in vitro and PK observables into
`max_kill_2`/`ic50_nM_2`, so achievability becomes a question about named, individually-checkable
inputs instead of an unexaminable constant.

Two independent constraints fall out, and both say 0.08 is out of reach for this drug class.

CONSTRAINT 1: THE CYTOSTATIC CEILING (needs no PK data at all)
--------------------------------------------------------------
`max_kill` has units of per-day and only means anything relative to a clone's own growth rate. A
drug that arrests the cell cycle can at most drive *net* growth to zero -- it cannot make a
population shrink, because arrested cells are still there. So for a purely cytostatic agent:

    max_kill <= growth_rate                    (equality = perfect arrest of every cell)

Exceeding it requires genuine cytotoxicity: net cell loss. CDK4/6 inhibitors are the textbook
cytostatic class -- they act by holding cells in G1, and the observed phenotype is arrest plus
senescence, not death. This was checked in canine cells specifically rather than assumed from human
pharmacology: in canine melanoma lines abemaciclib inhibited proliferation "primarily through G1
phase arrest and senescence," with cleaved PARP (an apoptosis marker) showing "only weak signal
intensity, suggesting that apoptosis may not be a major mechanism" (Frontiers Vet Sci 2025,
PMC12240792). The same paper notes prior palbociclib work also acted "primarily through cytostatic
growth inhibition."

This module's own resistant clones grow at 0.050-0.058/day. So `max_kill_2 = 0.08` asks a
cytostatic drug class to kill faster than the cells divide -- above the mechanistic ceiling for
every clone, by 38-60%. No dose achieves that, because it is not a dosing question.

CONSTRAINT 2: REAL CANINE POTENCY IS 9-31x WEAKER THAN ASSUMED
--------------------------------------------------------------
Separately and independently: `CDK46_ILLUSTRATIVE_IC50_NM = 100.0` was always labeled illustrative.
The real measured value in canine cells is 910-3090 nM (abemaciclib across five canine melanoma
lines, same paper) -- 9 to 31 times less potent. And `CDK46_ILLUSTRATIVE_CSS_NM = 500.0` was set as
a nominal 5x margin *over the assumed IC50*; against the real IC50 range, 500 nM sits at or below
the IC50, so the drug would be operating well short of saturation. `saturation_fraction` below
quantifies how much of even a permissible `max_kill` is actually realized at a given exposure --
and `required_max_kill` shows that operating below saturation *raises* the max_kill you would need,
compounding constraint 1 rather than offsetting it.

WHAT IS REAL HERE VS. ASSUMED
-----------------------------
Real and cited: the canine abemaciclib IC50 range and its cytostatic mechanism; palbociclib's dog
oral bioavailability range; the two molecular weights (standard reference values). Assumed, and
exposed as parameters rather than baked in: canine clearance and dosing interval for any specific
CDK4/6 inhibitor (no canine oncology dosing trial exists for one), unbound fraction in dog plasma
(reported qualitatively as "moderate", never as a number), and brain penetration for this class.
Nothing here is fitted to an outcome.
"""

from dataclasses import dataclass

import numpy as np

# Standard reference molecular weights (g/mol), used only for concentration unit conversion.
MOLECULAR_WEIGHT = {"palbociclib": 447.5, "abemaciclib": 506.6, "pexidartinib": 417.8}

CYTOSTATIC = "cytostatic"      # arrest only: max_kill cannot exceed the clone's growth rate
CYTOTOXIC = "cytotoxic"        # net cell loss: max_kill may exceed the growth rate
MIXED = "mixed"                # arrest plus a documented death mechanism; ceiling is soft

CDK46_CANINE_POTENCY = {
    "citation": "Frontiers Vet Sci 2025, PMC12240792 -- abemaciclib in canine melanoma cell lines",
    "ic50_nM_range": (910.0, 3090.0),
    "n_cell_lines": 5,
    "normal_fibroblast_ic50_nM": 5230.0,
    "mechanism": "G1 arrest and senescence; cleaved PARP only weakly detected, so apoptosis is "
                "not a major mechanism -- i.e. cytostatic, with lysosomal dysfunction and blocked "
                "autophagic flux rather than cell death",
    "mechanism_class": CYTOSTATIC,
    "caveat": "Canine melanoma, not canine histiocytic sarcoma -- no CDK4/6 inhibitor has been "
             "tested against any canine HS cell line. This is the closest real canine potency "
             "measurement available for the class, not a measurement in the disease being modeled.",
}

PALBOCICLIB_DOG_PK = {
    "citation": "palbociclib nonclinical PK (rat/dog/monkey) as reported in the drug's development "
               "literature",
    "oral_bioavailability_range": (0.23, 0.56),
    "plasma_clearance": "low to moderate (not resolved to a number here)",
    "volume_of_distribution": "large",
    "plasma_protein_binding": "moderate in mouse, rat, dog and human plasma (never given as a "
                             "numeric unbound fraction)",
    "caveat": "These come from tox/PK species work supporting the human program, not from a canine "
             "oncology dosing study. No canine dose, schedule, or achieved steady-state "
             "concentration for any CDK4/6 inhibitor was found.",
}


@dataclass(frozen=True)
class DrugPotency:
    """A second drug described in *measurable* terms rather than as an asserted kill rate.

    `emax_fraction_of_growth` is the maximal effect expressed as a multiple of the target clone's
    own growth rate -- the natural unit, because that is what decides whether the drug can only
    slow a clone (<1), exactly halt it (==1), or shrink it (>1). Keeping Emax and IC50 separate
    matters: they are different pharmacological quantities, and conflating them is what let a
    single `max_kill_2` number stand in for both.
    """
    name: str
    ic50_nM: float
    emax_fraction_of_growth: float
    mechanism_class: str
    provenance: str
    hill: float = 1.5

    def __post_init__(self):
        if self.ic50_nM <= 0:
            raise ValueError("ic50_nM must be positive")
        if self.emax_fraction_of_growth < 0:
            raise ValueError("emax_fraction_of_growth must be nonnegative")
        if self.mechanism_class not in (CYTOSTATIC, CYTOTOXIC, MIXED):
            raise ValueError(f"mechanism_class must be one of {CYTOSTATIC}/{CYTOTOXIC}/{MIXED}")
        if self.mechanism_class == CYTOSTATIC and self.emax_fraction_of_growth > 1.0:
            raise ValueError(
                "a cytostatic drug cannot exceed the clone's own growth rate "
                f"(emax_fraction_of_growth={self.emax_fraction_of_growth} > 1.0): arrest drives net "
                "growth to zero at best, it does not remove cells. Declare mechanism_class="
                f"'{CYTOTOXIC}' or '{MIXED}' with a documented death mechanism if that is intended.")


def cytostatic_ceiling(growth_rates: np.ndarray) -> np.ndarray:
    """Hard upper bound on `max_kill` per clone for a purely cytostatic drug: its own growth rate.

    Not a modeling convention -- an arithmetic consequence of what arrest does. This is the check
    that answers "is max_kill_2=0.08 achievable?" without needing any PK data at all.
    """
    return np.asarray(growth_rates, dtype=float)


def max_kill_from_emax(growth_rate_per_day: float, emax_fraction_of_growth: float) -> float:
    """Convert a measured maximal effect into the model's `max_kill` units (per day)."""
    return float(growth_rate_per_day) * float(emax_fraction_of_growth)


def saturation_fraction(concentration_nM: float, ic50_nM: float, hill: float = 1.5) -> float:
    """Fraction of `max_kill` actually realized at a given exposure -- the Emax/Hill occupancy term.

    Equals 0.5 at the IC50 and approaches 1 only well above it. This is why quoting a `max_kill`
    without also stating the achievable concentration overstates a drug: the model's kill term is
    `max_kill * saturation_fraction`, never `max_kill` itself.
    """
    c = max(float(concentration_nM), 0.0)
    ic50 = max(float(ic50_nM), 1e-9)
    return float(c ** hill / (ic50 ** hill + c ** hill))


def required_max_kill(margin_without_second_drug: float, concentration_nM: float,
                      ic50_nM: float, hill: float = 1.5) -> float:
    """`max_kill` a second drug needs so a clone's net growth margin reaches zero at this exposure.

    Inverts the kill term: the drug must supply `margin` of kill, but only delivers
    `max_kill * saturation_fraction`, so the requirement inflates by 1/saturation_fraction. Returns
    `inf` when the exposure is effectively zero, and 0.0 when the clone is already suppressed
    without any second drug.

    The practical consequence: being below saturation does not merely waste potency, it *raises the
    Emax you would need* -- so a weaker-than-assumed IC50 and a demanding max_kill compound rather
    than trade off.
    """
    if margin_without_second_drug <= 0:
        return 0.0
    fraction = saturation_fraction(concentration_nM, ic50_nM, hill)
    return float("inf") if fraction <= 0 else float(margin_without_second_drug / fraction)


def steady_state_css_nM(dose_mg_per_kg: float, dosing_interval_h: float,
                        clearance_L_per_h_per_kg: float, bioavailability: float,
                        molecular_weight: float, fraction_unbound: float = 1.0) -> dict:
    """Average steady-state concentration for repeated oral dosing, total and unbound.

        Css_avg (mg/L) = F * Dose / (CL * tau)          then  nM = (mg/L) * 1e6 / MW

    `fraction_unbound` scales to the pharmacologically active free concentration -- the number that
    should be compared against a cell-based IC50, since in vitro potency is measured in largely
    protein-free medium while plasma is not. Defaults to 1.0 (i.e. *no* correction) so the
    assumption is never applied silently; for the CDK4/6 class no numeric dog unbound fraction was
    found, only a qualitative "moderate".
    """
    for name, value in (("dose_mg_per_kg", dose_mg_per_kg), ("dosing_interval_h", dosing_interval_h),
                        ("clearance_L_per_h_per_kg", clearance_L_per_h_per_kg),
                        ("molecular_weight", molecular_weight)):
        if value <= 0:
            raise ValueError(f"{name} must be positive")
    if not 0 < bioavailability <= 1 or not 0 < fraction_unbound <= 1:
        raise ValueError("bioavailability and fraction_unbound must lie in (0, 1]")
    total_mg_per_L = bioavailability * dose_mg_per_kg / (clearance_L_per_h_per_kg * dosing_interval_h)
    total_nM = total_mg_per_L * 1e6 / molecular_weight
    return {"css_total_mg_per_L": total_mg_per_L, "css_total_nM": total_nM,
            "css_free_nM": total_nM * fraction_unbound, "fraction_unbound_applied": fraction_unbound}


def achievability_report(growth_rates: np.ndarray, margins_without_second_drug: np.ndarray,
                         potency: DrugPotency, concentration_nM: float,
                         clone_names: list[str]) -> dict:
    """Can this drug, at this exposure, reverse each clone -- and if not, what would it take?

    Reports per clone: the cytostatic ceiling, the `max_kill` this drug can actually supply, the
    `max_kill` required at this exposure, and whether the requirement clears both the drug's own
    Emax and the mechanistic ceiling. Separating "not potent enough" from "above the ceiling for
    this mechanism" is the point -- the first is a dosing/medicinal-chemistry problem, the second
    cannot be fixed by either.
    """
    growth_rates = np.asarray(growth_rates, dtype=float)
    margins = np.asarray(margins_without_second_drug, dtype=float)
    if not (len(growth_rates) == len(margins) == len(clone_names)):
        raise ValueError("growth_rates, margins_without_second_drug and clone_names must align")

    ceiling = cytostatic_ceiling(growth_rates)
    fraction = saturation_fraction(concentration_nM, potency.ic50_nM, potency.hill)
    rows = []
    for index, name in enumerate(clone_names):
        deliverable = max_kill_from_emax(growth_rates[index], potency.emax_fraction_of_growth)
        needed = required_max_kill(margins[index], concentration_nM, potency.ic50_nM, potency.hill)
        limited_by_mechanism = (potency.mechanism_class == CYTOSTATIC and needed > ceiling[index])
        rows.append({
            "clone": name,
            "growth_rate_per_day": float(growth_rates[index]),
            "margin_without_second_drug": float(margins[index]),
            "cytostatic_ceiling": float(ceiling[index]),
            "max_kill_deliverable_by_this_drug": deliverable,
            "max_kill_required_at_this_exposure": needed,
            "achieved_kill_at_this_exposure": deliverable * fraction,
            "reversed": bool(deliverable * fraction >= margins[index]),
            "blocked_by_cytostatic_ceiling": bool(limited_by_mechanism),
            "shortfall": float(max(0.0, needed - deliverable)),
        })
    return {
        "drug": potency.name, "mechanism_class": potency.mechanism_class,
        "provenance": potency.provenance,
        "ic50_nM": potency.ic50_nM, "concentration_nM": float(concentration_nM),
        "saturation_fraction_at_this_exposure": fraction,
        "per_clone": rows,
        "all_clones_reversed": all(row["reversed"] for row in rows),
        "any_blocked_by_mechanism": any(row["blocked_by_cytostatic_ceiling"] for row in rows),
    }


def feasibility_frontier(margin: float, ic50_values_nM: np.ndarray,
                         concentration_values_nM: np.ndarray, hill: float = 1.5) -> np.ndarray:
    """`max_kill` required to reverse a clone of the given margin, over an (IC50 x exposure) grid.

    Sweeps the two quantities a real experiment would measure, instead of asserting either. Read
    against a mechanistic ceiling: grid cells whose requirement exceeds the clone's growth rate are
    unreachable by a cytostatic agent at any dose, which is a qualitatively different kind of "no"
    than a cell that merely needs a more potent molecule.
    """
    ic50_values_nM = np.asarray(ic50_values_nM, dtype=float)
    concentration_values_nM = np.asarray(concentration_values_nM, dtype=float)
    grid = np.empty((len(ic50_values_nM), len(concentration_values_nM)))
    for i, ic50 in enumerate(ic50_values_nM):
        for j, concentration in enumerate(concentration_values_nM):
            grid[i, j] = required_max_kill(margin, concentration, ic50, hill)
    return grid
