"""How much of the "covers all sites, all mechanisms, all escapes" claim is actually backed by
evidence -- graded escape by escape, in code, not prose.

WHY THIS MODULE EXISTS
----------------------
The stated goal is a therapy that covers every site, mechanism, and escape route for this
specific canine HS presentation. The engine reports that the induction regimen closes all twelve
escapes at both occupied CNS sites (and 0/45 double, 0/120 triple combinations uncovered). An
audit established that this "closes everything" result is largely DEFINITIONAL: a margin is
``potency x access x duty - growth``, and almost every potency is a hand-set constant labelled
ASSUMED, while the growth rate that sets the pass/fail bar is an uncited placeholder. So "all
escapes covered" is true *inside the model* but says little about the world until you ask what
each closure actually rests on.

This module answers that question head-on. For each of the twelve escapes in ``disease.ESCAPES``
it records the closing agent, the EVIDENCE GRADE behind that closure, exactly what is and is not
measured, and the single decisive experiment that would move it. The grades are read straight
from the honest caveats already written into ``disease.ESCAPES`` and the provenance errors
catalogued in ``core.evidence`` -- this module makes them countable, not new claims.

The verdict it computes is deliberately unflattering and is the honest answer to the goal:
full coverage is a STRUCTURAL / hypothesis claim, not an evidence-backed one. See
``honest_coverage_statement()``.

This is an analysis, not veterinary advice.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from . import disease
from .core.evidence import Provenance


class Backing(Enum):
    """The strongest evidence standing behind an escape's closure, weakest-link graded."""

    MEASURED_CANINE_HS = "measured in canine histiocytic sarcoma"
    MEASURED_OTHER = "measured, but in another species or disease (a transfer)"
    STRUCTURAL = "a mechanism/design argument that needs no kill-rate number"
    ASSUMED = "rests on an assumed, never-measured kill rate"

    @property
    def is_evidence_backed(self) -> bool:
        """True only where a real measurement stands behind the closure (a structural argument
        may be sound, but it is not a measurement; an assumption is neither)."""
        return self in (Backing.MEASURED_CANINE_HS, Backing.MEASURED_OTHER)


@dataclass(frozen=True)
class EscapeCoverage:
    """The evidence status of one escape's closure."""

    escape_number: int
    closing_agent: str
    backing: Backing
    # what specifically IS measured vs is not -- the weakest link that sets the grade
    key_number_status: str
    # the single cheapest experiment that would upgrade this line
    decisive_experiment: str
    provenance: Provenance

    @property
    def escape(self) -> disease.Escape:
        return ESCAPE_BY_NUMBER[self.escape_number]


# Grades are the weakest link in each closure, taken from the caveats in disease.ESCAPES and the
# provenance errors in core.evidence. Where an agent's activity is measured but its per-day KILL
# RATE is not calibrated (the number the margin actually uses), the line says so explicitly.
COVERAGE: tuple[EscapeCoverage, ...] = (
    EscapeCoverage(
        1, "position-independent agents (radiation / microtubule cytotoxic / PRMT5i)",
        Backing.MEASURED_CANINE_HS,
        "Closed by the microtubule cytotoxic, and the microtubule CLASS is measured potently "
        "cytotoxic in 4 canine HS lines (vincristine IC50 1.77-2.69, vinblastine 1.75-2.78, "
        "paclitaxel 23.8-58.4 ng/ml; PMID 25715778). Gaps: the chosen induction agent "
        "(lisavanbulin, colchicine-site) differs from the measured vinca/taxane agents, and an "
        "IC50 is a concentration, not the per-day kill rate the margin uses.",
        "Measure the specific induction agent's per-day kill rate in canine HS cells.",
        Provenance.MEASURED,
    ),
    EscapeCoverage(
        2, "position-independent agents (radiation / microtubule cytotoxic / PRMT5i)",
        Backing.MEASURED_CANINE_HS,
        "Closure does not depend on hitting MEK; it rests on the microtubule cytotoxic, whose "
        "class is measured potently active in canine HS (PMID 25715778). Same specific-agent and "
        "kill-rate gaps as escape 1. In the Monte Carlo this was the slowest-collapsing route.",
        "Measure the specific induction agent's per-day kill rate in canine HS cells.",
        Provenance.MEASURED,
    ),
    EscapeCoverage(
        3, "downstream / position-independent agents (microtubule cytotoxic)",
        Backing.MEASURED_CANINE_HS,
        "A deliberately pessimistic single-hit; closed by the microtubule cytotoxic, whose class "
        "is measured active in canine HS (PMID 25715778). Same specific-agent and kill-rate gaps "
        "as escape 1.",
        "Measure the specific induction agent's per-day kill rate in canine HS cells.",
        Provenance.MEASURED,
    ),
    EscapeCoverage(
        4, "paxalisib (PI3K/AKT inhibitor)",
        Backing.MEASURED_OTHER,
        "The only canine PI3K-inhibitor IC50s are from HEMANGIOSARCOMA lines, used here for "
        "histiocytic sarcoma (catalogued in core.evidence as one of the project's transfers). "
        "Paxalisib brain penetration (Kp,uu 0.31) is rodent, not dog.",
        "Measure a PI3K/AKT-inhibitor IC50 in canine HS lines.",
        Provenance.TRANSFERRED,
    ),
    EscapeCoverage(
        5, "liposomal clodronate (macrophage-lineage depletion)",
        Backing.ASSUMED,
        "Clodronate's kill rate against canine HS has never been measured in any species; the "
        "only signal is a response in 2/5 HS dogs. A liposome also cannot cross an intact BBB.",
        "Measure liposomal clodronate cytotoxicity against canine HS cells.",
        Provenance.ASSUMED,
    ),
    EscapeCoverage(
        6, "radiation + microtubule cytotoxic + anti-PD-1 (gilvetmab)",
        Backing.ASSUMED,
        "Anti-PD-1 efficacy against canine HS is unmeasured (a two-point figure); the closure of "
        "the antigen-loss-with-MHC-intact leak leans on it.",
        "Measure an immune-effector kill rate against canine HS (e.g. anti-PD-1 response).",
        Provenance.ASSUMED,
    ),
    EscapeCoverage(
        7, "parthenolide / DMAPT (NF-kB inhibitor)",
        Backing.MEASURED_CANINE_HS,
        "Parthenolide has actual canine-HS activity data (kills cell lines and primary cells, "
        "extends survival in a disseminated-HS mouse model) -- the strongest single line here. "
        "BUT the escape's premise is contested: an 11-line finding (PMID 40500939, PRJDB17594) "
        "that ERK/Akt activation does not predict response was banked and never propagated.",
        "Run the 11-line panel (PRJDB17594) against an ERK inhibitor, stratified by NF-kB cluster.",
        Provenance.MEASURED,
    ),
    EscapeCoverage(
        8, "lipophilic statin (mevalonate / CoQ10 block)",
        Backing.ASSUMED,
        "Ferroptosis has never been studied in canine HS. Worse, the lineage argument runs the "
        "wrong way: canine HS upregulates anti-ferroptotic defences (ferroportin/ferritin), so "
        "this closure may be not merely unmeasured but counter-indicated.",
        "Test ferroptosis sensitivity (GPX4/FSP1 axis) in canine HS cells.",
        Provenance.ASSUMED,
    ),
    EscapeCoverage(
        9, "hydroxychloroquine (autophagy/lysosome inhibitor)",
        Backing.MEASURED_OTHER,
        "The only canine data is a phase I in spontaneous canine LYMPHOMA (12.5 mg/kg/day); "
        "unmeasured in canine HS. Nearly free to drop from the regimen (margin cost ~2e-5).",
        "Test autophagy dependence / HCQ sensitivity in canine HS cells.",
        Provenance.TRANSFERRED,
    ),
    EscapeCoverage(
        10, "continuous / metronomic dosing (duty -> 1.0), not a new drug",
        Backing.STRUCTURAL,
        "A drug-tolerant persister is a reversible STATE, so a continuously present agent catches "
        "it at re-entry -- a schedule argument, not a kill-rate claim. No persister-directed "
        "therapy has ever been approved in any species, so it cannot be measured, only reasoned.",
        "Demonstrate persister re-entry kill under metronomic dosing in a canine HS model.",
        Provenance.DERIVED,
    ),
    EscapeCoverage(
        11, "made irrelevant by dropping the alkylator class (use a microtubule agent)",
        Backing.STRUCTURAL,
        "A mitotic poison leaves no O6-methylguanine lesion for MGMT to repair, so MGMT cannot "
        "apply -- a sound mechanism-level move, and the substitute (microtubule) class is measured "
        "potently active in canine HS (PMID 25715778); the specific-agent kill rate is the residual "
        "gap, captured under escapes 1-3.",
        "Confirm the chosen agent is a non-alkylator in the canine formulation used.",
        Provenance.DERIVED,
    ),
    EscapeCoverage(
        12, "PRMT5-inhibitor maintenance (synthetic-lethal on MTAP deletion)",
        Backing.ASSUMED,
        "The whole ten-year / second-primary claim. Conditional on CNS access >= 0.50 (fails at "
        "0.30; never measured in a dog) and on the tumour being MTAP-deleted (unknown until "
        "stained). PRMT5i potency and canine CNS penetration are both unmeasured.",
        "One MTAP immunohistochemistry stain on archived tumour tissue (the cheapest falsifier); "
        "then a canine PRMT5i CNS-penetration measurement.",
        Provenance.ASSUMED,
    ),
)

ESCAPE_BY_NUMBER: dict[int, disease.Escape] = {e.number: e for e in disease.ESCAPES}


def _validate() -> None:
    """Every escape in disease.ESCAPES must have exactly one coverage grade, and vice versa."""
    graded = {c.escape_number for c in COVERAGE}
    known = {e.number for e in disease.ESCAPES}
    if graded != known:
        raise ValueError(f"coverage/escape mismatch: graded={sorted(graded)} known={sorted(known)}")


_validate()


def tally() -> dict[str, int]:
    """Count escapes by evidence grade."""
    out: dict[str, int] = {b.name: 0 for b in Backing}
    for c in COVERAGE:
        out[c.backing.name] += 1
    return out


def evidence_backed() -> list[EscapeCoverage]:
    """Escapes whose closure rests on a real measurement (canine-HS or a named transfer)."""
    return [c for c in COVERAGE if c.backing.is_evidence_backed]


def measured_in_canine_hs() -> list[EscapeCoverage]:
    """Escapes whose closing agent has activity measured in canine HS specifically."""
    return [c for c in COVERAGE if c.backing is Backing.MEASURED_CANINE_HS]


def decisive_experiments() -> list[str]:
    """The distinct experiments that would upgrade the weakest lines, cheapest-first intent."""
    seen: list[str] = []
    for c in COVERAGE:
        if c.decisive_experiment not in seen:
            seen.append(c.decisive_experiment)
    return seen


@dataclass(frozen=True)
class MaintenanceTierCoverage:
    """Evidence behind one genotype-matched maintenance arm (the ten-year / second-primary side).

    The escape grades above concern closing the FIRST tumour, where the induction backbone
    deliberately routes around reroutable targets. The maintenance tiers are graded separately
    because their evidence is genuinely different -- and, for the two commonest cases, better:
    the drug class has real measured response in canine HS, which the escape-closure view (which
    treats MEK as reroutable and hands closure to the cytotoxic) never credits.
    """

    genotype: str
    rough_share: str
    anchor: str
    backing: Backing
    canine_hs_evidence: str
    key_gap: str
    citation: str
    provenance: Provenance


# Grades and citations are read from core.genotype_tiered_durability, pharmacology, mapk_resistance
# and core.evidence -- all already in the repo. No external lookup.
MAINTENANCE_TIERS: tuple[MaintenanceTierCoverage, ...] = (
    MaintenanceTierCoverage(
        "PTPN11/SHP2 or KRAS driver (MAPK)", "~59%",
        "MEK inhibitor (mirdametinib, CNS-penetrant)",
        Backing.MEASURED_CANINE_HS,
        "Three canine HS lines (BD/OD/DH82) carrying these drivers responded in vitro to MEK "
        "inhibition, cobimetinib IC50 74-372 nM, below achievable plasma Cmax (~1640 nM).",
        "A MEK block is reroutable in an ESTABLISHED tumour (escapes 1-3); it works at EMERGENCE "
        "of a new primary, so it leans on early detection. Mirdametinib's canine CNS penetration "
        "is unmeasured.",
        "PMID 39202410 (response); PMID 39258288 / 31277422 (frequency)",
        Provenance.MEASURED,
    ),
    MaintenanceTierCoverage(
        "none targetable / unknown", "residual",
        "immune surveillance + cycled lomustine (CCNU)",
        Backing.MEASURED_CANINE_HS,
        "Lomustine has real canine-HS efficacy: phase II ORR 0.46 (n=56, PMID 17338159), and in "
        "localized HS after debulking a 568-day median / 37.5% relapse-free (n=16, PMID 19453368) "
        "-- the disease's only structurally-matched durability datapoint.",
        "Modest ORR and not durable as monotherapy; the 37.5% comparator is the exact external "
        "check the durability engine FAILED (predicted 0.0%). This is a floor, not a cure.",
        "PMID 17338159; PMID 19453368",
        Provenance.MEASURED,
    ),
    MaintenanceTierCoverage(
        "MTAP deleted", "recurrent minority",
        "PRMT5 inhibitor (MTA-cooperative; TNG908/TNG462)",
        Backing.MEASURED_OTHER,
        "The MTAP-deletion -> PRMT5-dependency synthetic lethality is validated in human "
        "MTAP-deleted cancers (the basis of the TNG908/TNG462 phase I/II programs); the cell "
        "cannot reroute around a homozygous deletion.",
        "No canine-HS data at all: PRMT5i potency and canine CNS penetration are both unmeasured, "
        "and the tumour must first be confirmed MTAP-deleted (one IHC stain -- the cheapest "
        "falsifier in the project).",
        "human MTAP-deleted cancers, phase I/II (repo: core.breed_wide_durability)",
        Provenance.TRANSFERRED,
    ),
    MaintenanceTierCoverage(
        "PTEN deleted", "minority",
        "PI3K inhibitor (paxalisib)",
        Backing.MEASURED_OTHER,
        "PI3K-inhibitor IC50s measured in canine cells, and paxalisib is a confirmed non-substrate "
        "of P-gp/BCRP with rodent brain penetration (Kp,uu ~0.31).",
        "The canine PI3K IC50s are from HEMANGIOSARCOMA, not HS (a transfer catalogued in "
        "core.evidence); PTEN-loss dependency has known resistance routes.",
        "canine hemangiosarcoma PI3K IC50s (repo: core.evidence); paxalisib efflux status",
        Provenance.TRANSFERRED,
    ),
    MaintenanceTierCoverage(
        "CDKN2A deleted, RB1 intact", "minority",
        "CDK4/6 inhibitor (abemaciclib)",
        Backing.MEASURED_OTHER,
        "Abemaciclib IC50 910-3090 nM across 5 canine melanoma lines (vs 5230 nM normal "
        "fibroblasts) -- the closest real canine potency for the class.",
        "Canine MELANOMA, not HS; and it is CYTOSTATIC (G1 arrest, weak apoptosis), so its kill "
        "ceiling cannot exceed the clone's growth rate. Needs RB1 intact or it drops to the floor.",
        "PMC12240792 (repo: pharmacology.CDK46_CANINE_POTENCY)",
        Provenance.TRANSFERRED,
    ),
)


def maintenance_tally() -> dict[str, int]:
    """Count maintenance tiers by evidence grade."""
    out: dict[str, int] = {b.name: 0 for b in Backing}
    for m in MAINTENANCE_TIERS:
        out[m.backing.name] += 1
    return out


def maintenance_measured_in_canine_hs() -> list[MaintenanceTierCoverage]:
    """Maintenance tiers whose drug class has response measured in canine HS specifically."""
    return [m for m in MAINTENANCE_TIERS if m.backing is Backing.MEASURED_CANINE_HS]


def maintenance_statement() -> str:
    """One paragraph: the maintenance side is better-evidenced than escape-closure, and why."""
    canine = maintenance_measured_in_canine_hs()
    shares = " + ".join(m.rough_share for m in canine)
    return (
        f"The genotype-matched maintenance arm is better evidenced than the escape-closure view "
        f"suggests. Of {len(MAINTENANCE_TIERS)} tiers, {len(canine)} have drug-class response "
        f"MEASURED in canine HS -- the MAPK-driver majority (MEK inhibition; cobimetinib IC50 "
        f"74-372 nM, PMID 39202410) and the floor (lomustine; PMID 17338159/19453368), covering "
        f"roughly {shares} of cases between them. The remaining tiers (MTAP/PRMT5i, PTEN/PI3Ki, "
        f"CDKN2A/CDK4-6i) rest on transfers from human cancers or other canine diseases. So for "
        f"the commonest genotype the maintenance DRUG CLASS is measured in the disease; what stays "
        f"unmeasured is canine CNS penetration and whether early-emergence dosing holds for years."
    )


def honest_coverage_statement() -> str:
    """One paragraph: what the coverage claim is actually worth, by the numbers."""
    t = tally()
    n = len(COVERAGE)
    return (
        f"All {n} escapes are reported closed by the model at both occupied CNS sites. Graded by "
        f"evidence, that breaks down as: {t['MEASURED_CANINE_HS']} backed by activity measured in "
        f"canine HS (the microtubule induction class, PMID 25715778, closing escapes 1-3, plus "
        f"NF-kB/parthenolide whose premise is contested), {t['MEASURED_OTHER']} transferred from "
        f"another disease/species, {t['STRUCTURAL']} resting on a mechanism/design argument with no "
        f"kill number, and {t['ASSUMED']} resting on assumed, never-measured kill rates -- still "
        f"including the entire ten-year maintenance arm. So the induction backbone is now "
        f"measured-active in the disease, but 'covers all sites, mechanisms and escapes' remains a "
        f"STRUCTURAL / hypothesis-level claim overall -- what stays unmeasured are per-day kill "
        f"rates, canine CNS penetration, and the second-primary hinge. It is falsifiable and cheap "
        f"to start falsifying: {decisive_experiments()[-1]}"
    )


if __name__ == "__main__":
    print(honest_coverage_statement())
    print()
    for c in COVERAGE:
        print(f"  #{c.escape_number:>2} [{c.backing.name:<18}] {c.escape.name}")
    print()
    print(maintenance_statement())
    print()
    for m in MAINTENANCE_TIERS:
        print(f"  [{m.backing.name:<18}] {m.rough_share:<20} {m.genotype} -> {m.anchor}")
