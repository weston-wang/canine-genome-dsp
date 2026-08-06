"""Demo/report for `pharmacology`: is the second-drug potency the model needs actually reachable?"""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .mapk_resistance import CLONE_NAMES, clone_growth_margins
from .mapk_scenarios import (
    CDK46_ILLUSTRATIVE_CSS_NM,
    CDK46_ILLUSTRATIVE_IC50_NM,
    CDK46_MAX_KILL_SWEEP,
    DEBULKING_FRACTION,
    combination_scenarios,
)
from .pharmacology import (
    CDK46_CANINE_POTENCY,
    CYTOSTATIC,
    PALBOCICLIB_DOG_PK,
    DrugPotency,
    achievability_report,
    cytostatic_ceiling,
    feasibility_frontier,
    required_max_kill,
    saturation_fraction,
)


def cdk46_achievability_demo(out: Path, breed: str = "bmd",
                             debulking_fraction: float = DEBULKING_FRACTION,
                             target_max_kill: float = 0.08,
                             location_penetration_multiplier: float = 1.0) -> None:
    """Answers the question the resistance model could not: is `max_kill_2 = target_max_kill`
    (default 0.08, the value that produces 100% durable response flat to ten years) reachable by a
    real CDK4/6 inhibitor?

    Runs two independent checks, and reports them separately because they fail for different
    reasons and would need different things to fix:

      1. The cytostatic ceiling -- purely arithmetic, needs no PK data. A cell-cycle-arresting drug
         cannot kill faster than cells divide, so `max_kill <= growth_rate` per clone.
      2. Real measured canine potency vs. the illustrative value, propagated through the Emax/Hill
         occupancy term, which determines how much of a permissible `max_kill` is actually realized
         at an achievable exposure -- and therefore how much `max_kill` would be *required*.

    Also emits a feasibility frontier over (IC50 x exposure), so the answer is visible as a region
    rather than a single verdict, and so a future real measurement can be located on it directly.
    """
    out.mkdir(parents=True, exist_ok=True)
    base = combination_scenarios(breed, debulking_fraction, [0.0],
                                 location_penetration_multiplier)[0.0]
    model, css, _, _, _ = base
    margins = clone_growth_margins(model, css, None)   # trametinib alone: what drug 2 must overcome
    growth = np.asarray(model.growth, dtype=float)
    ceiling = cytostatic_ceiling(growth)
    real_low, real_high = CDK46_CANINE_POTENCY["ic50_nM_range"]

    ceiling_rows = [{
        "clone": name, "growth_rate_per_day": float(g), "cytostatic_ceiling": float(c),
        "target_max_kill": target_max_kill,
        "target_exceeds_ceiling": bool(target_max_kill > c),
        "target_as_multiple_of_ceiling": float(target_max_kill / c) if c > 0 else None,
    } for name, g, c in zip(CLONE_NAMES, growth, ceiling)]
    pd.DataFrame(ceiling_rows).to_csv(out / "cytostatic_ceiling.csv", index=False)

    # Required max_kill for the worst resistant clone across assumed vs. real potency and exposure.
    worst_margin = float(np.max(margins[1:]))
    worst_index = int(np.argmax(margins[1:])) + 1
    requirement_rows = []
    for ic50, ic50_label in ((CDK46_ILLUSTRATIVE_IC50_NM, "illustrative (assumed)"),
                             (real_low, "real canine, most potent line"),
                             (real_high, "real canine, least potent line")):
        for exposure in (CDK46_ILLUSTRATIVE_CSS_NM, 2 * CDK46_ILLUSTRATIVE_CSS_NM, 2000.0, 10000.0):
            needed = required_max_kill(worst_margin, exposure, ic50)
            requirement_rows.append({
                "ic50_nM": ic50, "ic50_source": ic50_label, "exposure_nM": exposure,
                "saturation_fraction": saturation_fraction(exposure, ic50),
                "required_max_kill": needed,
                "cytostatic_ceiling_for_worst_clone": float(ceiling[worst_index]),
                "reachable_by_a_cytostatic_drug": bool(needed <= ceiling[worst_index]),
            })
    pd.DataFrame(requirement_rows).to_csv(out / "required_max_kill.csv", index=False)

    # Most generous defensible cytostatic case: perfect arrest of every cell (emax == growth rate),
    # at the least favorable end of the real measured potency range.
    generous = DrugPotency(
        name="CDK4/6 inhibitor, perfect arrest at real canine potency (most generous cytostatic case)",
        ic50_nM=real_high, emax_fraction_of_growth=1.0, mechanism_class=CYTOSTATIC,
        provenance=CDK46_CANINE_POTENCY["citation"])
    report = achievability_report(growth, margins, generous, CDK46_ILLUSTRATIVE_CSS_NM, CLONE_NAMES)
    pd.DataFrame(report["per_clone"]).to_csv(out / "achievability_per_clone.csv", index=False)

    ic50_grid = np.geomspace(50, 5000, 40)
    exposure_grid = np.geomspace(50, 20000, 40)
    frontier = feasibility_frontier(worst_margin, ic50_grid, exposure_grid)
    np.savez_compressed(out / "feasibility_frontier.npz", ic50_nM=ic50_grid,
                        exposure_nM=exposure_grid, required_max_kill=frontier)

    fig, ax = plt.subplots(figsize=(8, 6))
    reachable = ceiling[worst_index]
    shown = np.clip(frontier, 0, 4 * reachable)
    mesh = ax.pcolormesh(exposure_grid, ic50_grid, shown, shading="auto", cmap="magma_r")
    ax.contour(exposure_grid, ic50_grid, frontier, levels=[reachable], colors="tab:cyan",
               linewidths=2.2)
    ax.contour(exposure_grid, ic50_grid, frontier, levels=[target_max_kill], colors="white",
               linewidths=1.4, linestyles="--")
    ax.axhspan(real_low, real_high, color="tab:green", alpha=.18)
    ax.axhline(CDK46_ILLUSTRATIVE_IC50_NM, color="tab:blue", linestyle=":", linewidth=1.6)
    ax.axvline(CDK46_ILLUSTRATIVE_CSS_NM, color="tab:blue", linestyle=":", linewidth=1.6)
    ax.set(xscale="log", yscale="log", xlabel="achievable free exposure (nM)",
           ylabel="IC50 (nM)",
           title=f"max_kill required to reverse {CLONE_NAMES[worst_index]}\n"
                 f"cyan = cytostatic ceiling ({reachable:.3f}); green band = real canine IC50; "
                 f"dotted blue = values this module assumed")
    fig.colorbar(mesh, ax=ax, label="required max_kill (per day)")
    fig.tight_layout(); fig.savefig(out / "feasibility_frontier.png", dpi=160); plt.close(fig)

    summary = {
        "question": f"Is max_kill_2 = {target_max_kill} -- the second-drug potency at which this "
                   "module reports 100% durable response flat to 10 years -- achievable by a real "
                   "CDK4/6 inhibitor?",
        "answer": "No, and it fails two independent checks that would need different fixes.",
        "constraint_1_cytostatic_ceiling": {
            "principle": "A cell-cycle-arresting drug can at most drive net growth to zero; it "
                        "cannot remove cells, so max_kill <= growth_rate per clone. This is "
                        "arithmetic, not a modeling convention, and needs no PK data.",
            "mechanism_evidence": CDK46_CANINE_POTENCY["mechanism"],
            "per_clone": ceiling_rows,
            "verdict": f"target_max_kill={target_max_kill} exceeds every resistant clone's ceiling "
                      f"({ceiling[1:].min():.4f}-{ceiling[1:].max():.4f}/day) by "
                      f"{target_max_kill / ceiling[1:].max() - 1:.0%}-"
                      f"{target_max_kill / ceiling[1:].min() - 1:.0%}. No dose reaches it because "
                      "it is not a dosing question.",
            "stricter_corollary": "Even at infinite concentration and perfect arrest of every cell, "
                                 "a purely cytostatic second drug drives each clone's margin to "
                                 "exactly zero (stasis), never negative -- so it cannot produce the "
                                 "*mechanistic elimination* this module attributes to "
                                 "max_kill_2=0.08 at all, only indefinite stasis in the best case.",
        },
        "constraint_2_real_potency": {
            "assumed_ic50_nM": CDK46_ILLUSTRATIVE_IC50_NM,
            "real_canine_ic50_nM_range": [real_low, real_high],
            "fold_weaker_than_assumed": [real_low / CDK46_ILLUSTRATIVE_IC50_NM,
                                        real_high / CDK46_ILLUSTRATIVE_IC50_NM],
            "assumed_exposure_nM": CDK46_ILLUSTRATIVE_CSS_NM,
            "saturation_at_assumed_ic50": saturation_fraction(CDK46_ILLUSTRATIVE_CSS_NM,
                                                             CDK46_ILLUSTRATIVE_IC50_NM),
            "saturation_at_real_ic50_range": [
                saturation_fraction(CDK46_ILLUSTRATIVE_CSS_NM, real_low),
                saturation_fraction(CDK46_ILLUSTRATIVE_CSS_NM, real_high)],
            "consequence": "Operating below saturation does not merely waste potency -- it raises "
                          "the max_kill required (requirement scales as 1/saturation_fraction), so "
                          "a weaker-than-assumed IC50 compounds constraint 1 instead of trading "
                          "off against it.",
            "requirements": requirement_rows,
            "source": CDK46_CANINE_POTENCY,
        },
        "most_generous_cytostatic_case": report,
        "worst_resistant_clone": CLONE_NAMES[worst_index],
        "worst_resistant_margin_on_primary_drug_alone": worst_margin,
        "what_would_change_the_answer": [
            "a genuinely cytotoxic second agent (documented net cell loss, not arrest+senescence) "
            "-- this is the only route that lifts constraint 1, and it means a different drug "
            "class, not a different dose of a CDK4/6 inhibitor",
            "a real canine HS cell-line dose-response measurement: every potency number here comes "
            "from canine melanoma/mammary/lymphoma lines, and no CDK4/6 inhibitor has ever been "
            "tested against a canine HS line",
            "real canine PK for a specific CDK4/6 inhibitor (dose, schedule, clearance, unbound "
            "fraction) -- none was found, so achievable exposure is swept rather than known",
            "a lower primary-drug-alone margin: the requirement is set by what trametinib leaves "
            "behind, so better MAPK-pathway suppression lowers the bar for the second drug",
        ],
        "unverified_extrapolations": [
            "the cytostatic classification is from canine melanoma cells (weak cleaved PARP, "
            "arrest plus senescence), not canine HS; a different lineage could conceivably respond "
            "cytotoxically to the same drug",
            "emax_fraction_of_growth=1.0 in the generous case is an assumed upper bound (perfect "
            "arrest of every cell), not a measured Emax -- real Emax is generally below this",
            "growth rates the ceiling is computed from are themselves illustrative, unfitted "
            "constants; the *ordering* of the conclusion is robust to their exact values but the "
            "numeric ceiling is not",
        ],
        "dog_pk_context": PALBOCICLIB_DOG_PK,
        "warning": "This evaluates whether a model parameter is pharmacologically reachable. It "
                  "does not establish that any drug works in this disease, and a reachable "
                  "parameter would still be an illustrative model, not a prediction.",
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, default=str) + "\n")
