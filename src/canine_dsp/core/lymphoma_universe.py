"""The widened universe: escapes found by the independent audit and agents found by the modality sweeps.

WHY THIS FILE EXISTS. The first closing-combination was reported as found while the catalogue had no vaccine and
no separate stem-cell mechanism, and the escape list had not been independently audited. The user's objection:
"I don't get how you can claim the goal is completed when even I know vaccine should be part of the equation, and
maybe even stem cell. Go back and be thorough." The sweeps are saved in docs/universe/SWEEP_*.md (every PMID there
was fetched from PubMed by an agent; spot-check before quoting). This file turns what they found into model terms.

WHAT IS AND IS NOT HERE.
 * UNIVERSE_ESCAPES: escapes the audit found that have a defeat set the model can express. Rates are the
   catalogue's conventions (mutation 1e-8, phenotypic 1e-7), NOT measurements. Escapes with no expressible
   mechanism (unattributed cross-resistance, host and logistic modifiers, therapy-induced second cancers,
   eye/testis compartments) are listed in docs/LYMPHOMA_UNIVERSE.md as OUTSIDE the model.
 * `TAGS`: which existing agents each new escape defeats. Applied in `core/lymphoma_grounded._ground`; a tag
   only matters against an escape that carries the same tag, so earlier results are unchanged.
 * `universe_agents`: only agents whose potency can be graded at the user's bar (a measured clinical outcome
   converted by a stated rule, or a derivation/transfer). Candidates with a measured IC50 but no exposure, or with
   no kill measurement at all, are NOT given a made-up number; they are listed in the universe ledger.
"""

from __future__ import annotations

from dataclasses import replace

from .lymphoma_catalogue import GROWTH_PER_DAY
from .regimen import Agent, Axis, Escape, Layer

# --------------------------------------------------------------------------------------------------------
# Escapes found by the independent audit (docs/universe/SWEEP_escapes.md, Table A). IDs follow that table.
# --------------------------------------------------------------------------------------------------------
UNIVERSE_ESCAPES = (
    Escape("E1 glucocorticoid-receptor loss (GC resistance)", Axis.APOPTOSIS, Layer.RECEPTOR, 1e-5,
           defeats=frozenset({"gc_resistance"}),
           evidence="DOG: prednisone resistance 'essentially universal', median onset 68 d, NR3C1-alpha down in 6/6 "
                    "high-grade cases (PMID 31943234); GR-low canine lines resistant (PMID 20362310); high cortisol "
                    "predicts worse outcome (PMID 38471970). Rate ASSUMED, set HIGH on purpose: it is acquired under "
                    "glucocorticoid exposure, so it is treated as present.",
           note="Defeats prednisolone only. Separate from TP53 / apoptosis evasion: other apoptosis agents still work."),
    Escape("E2 nucleoside-activation loss (dCK down)", Axis.CYTOTOXIC, Layer.RECEPTOR, 1e-7,
           defeats=frozenset({"nucleoside_activation"}),
           evidence="HUMAN mantle-cell lymphoma: dCK down in 50% of primary cytarabine-failure samples, 20-1000x "
                    "cross-resistance to other nucleoside analogues, no cross-resistance to doxorubicin or "
                    "cyclophosphamide (PMID 24972933). Not found in dogs.",
           note="Defeats every cytarabine arm, including the intrathecal pump that closes the brain."),
    Escape("E3 topoisomerase-IIa loss (anthracycline target)", Axis.CYTOTOXIC, Layer.RECEPTOR, 1e-8,
           defeats=frozenset({"topo2"}),
           evidence="MOUSE Emu-myc lymphoma: Top2A level determines doxorubicin response (PMID 18574145). Not found "
                    "in dogs.", note="A doxorubicin failure that is not a pump."),
    Escape("E4 BCL2-family rewiring (MCL1/BCL-xL, phosphorylation)", Axis.APOPTOSIS, Layer.RECEPTOR, 1e-7,
           defeats=frozenset({"bcl2_dependence"}),
           evidence="HUMAN: BCL2-family hyperphosphorylation underlies acquired venetoclax resistance in DLBCL/CLL "
                    "(PMID 37751299). DOG: 6/7 non-indolent B-cell cancers resistant to venetoclax and navitoclax "
                    "(PMID 36433867).", note="Defeats venetoclax. The T-cell programs lean on venetoclax."),
    Escape("E5 quiescent efflux-high lymphoid progenitor", Axis.CELL_CYCLE, Layer.RECEPTOR, 1e-2,
           requires_division=False, effluxes_substrates=True,
           evidence="DOG: CD34+/CD117+/CD133+ lymphoid progenitors expanded in 28 dogs, clonally identical to bulk "
                    "(PMID 21777289); side-population cells efflux-high, not shifted by verapamil (PMID 23167606, "
                    "23820219); valspodar did not change progenitor counts (PMID 28357033). Fraction ~1% per the "
                    "stem-cell sweep. Dormancy of these cells is NOT shown; modelled as both non-dividing and "
                    "pump-high on purpose (conservative).",
           note="A conjunction. Only agents that are neither division-gated nor pump substrates reach it."),
    Escape("E7 antigen-low (sub-threshold CD20/CD19, not null)", Axis.IMMUNE_EFFECTOR, Layer.RECEPTOR, 1e-7,
           defeats=frozenset({"antigen_density"}),
           evidence="HUMAN: CD19-low tumours 1-y PFS 16% vs 64% (n=301), CD19-low share 17% -> 35% at CAR-T relapse, "
                    "genetic locus loss only 8-11% (PMID 42671910); CD20 density threshold for complement killing "
                    "(PMID 22228637). Not measured in dogs.",
           note="Defeats single-antigen antibody and single-antigen CAR; a two-antigen CAR keeps the other."),
    Escape("E8 XPO1 C528S (verdinexor target mutation)", Axis.APOPTOSIS, Layer.RECEPTOR, 1e-9,
           defeats=frozenset({"xpo1_target"}),
           evidence="Engineered heterozygous C528S is sufficient for resistance (PMID 27634897); not yet observed "
                    "clinically.", note="Defeats verdinexor."),
    Escape("E9 antifolate transport loss (RFC)", Axis.CYTOTOXIC, Layer.RECEPTOR, 1e-7,
           defeats=frozenset({"antifolate_uptake"}),
           evidence="HUMAN: RFC promoter methylation in 30% of CNS lymphoma vs 8% of systemic DLBCL (PMID 15327516).",
           note="Defeats high-dose methotrexate, the brain arm."),
    Escape("E10 macrophage checkpoint (CD47/SIRPa)", Axis.IMMUNE_EFFECTOR, Layer.RECEPTOR, 1e-7,
           defeats=frozenset({"macrophage_checkpoint"}),
           evidence="Canine CD47/SIRPa axis conserved and functional (PMID 27856424); prevalence NOT found.",
           note="Modelled as defeating the antibody (its phagocytosis arm). Conservative: the antibody also acts by "
                "other routes."),
)

#: Sensitivity only: cell-adhesion protection by marrow/node stroma (audit E6). The model can only express a total
#: defeat, but the real effect is partial, so this is reported separately and never in the headline result.
NICHE_ESCAPE = Escape(
    "E6 niche / adhesion-mediated protection (SENSITIVITY)", Axis.CYTOTOXIC, Layer.RECEPTOR, 1e-2,
    defeats=frozenset({"adhesion_protection"}),
    evidence="HUMAN: stroma protects B-lymphoma cells from rituximab, reversed by VLA-4 blockade (PMID 21749361). "
             "DOG: marrow involvement 57% (PMID 2470709) predicts worse outcome (PMID 23735731). Mechanism not "
             "measured in dogs.", note="Partial in life; modelled as total, so sensitivity only.")

FULL_ESCAPE_NAMES = tuple(e.name for e in UNIVERSE_ESCAPES)

#: Tags: agent name prefix -> the vulnerabilities it carries (see Escape.defeats).
TAGS = {
    "prednisolone": frozenset({"gc_resistance"}),
    "cytarabine CRI": frozenset({"nucleoside_activation"}),
    "intrathecal cytarabine": frozenset({"nucleoside_activation"}),
    "continuous intrathecal cytarabine": frozenset({"nucleoside_activation"}),
    "doxorubicin": frozenset({"topo2"}),
    "venetoclax": frozenset({"bcl2_dependence"}),
    "verdinexor": frozenset({"xpo1_target"}),
    "high-dose methotrexate": frozenset({"antifolate_uptake"}),
    "anti-CD20 monoclonal antibody": frozenset({"antigen_density", "macrophage_checkpoint", "adhesion_protection"}),
    "CD20 CAR-T": frozenset({"antigen_density"}),
    "CD7-directed CAR-T": frozenset({"antigen_density"}),
    "persistence-engineered": frozenset({"antigen_density"}),
}
#: Agents that carry the adhesion tag in the sensitivity run (division-gated cytotoxics are stroma-protected).
ADHESION_TAGGED = ("doxorubicin", "vincristine", "cyclophosphamide", "cytarabine CRI", "rabacfosadine",
                   "lomustine", "high-dose methotrexate", "intrathecal cytarabine",
                   "continuous intrathecal cytarabine")


def apply_tags(a: Agent) -> Agent:
    extra = frozenset()
    for prefix, tags in TAGS.items():
        if a.name.startswith(prefix):
            extra |= tags
    if any(a.name.startswith(p) for p in ADHESION_TAGGED):
        extra |= frozenset({"adhesion_protection"})
    return replace(a, vulnerable_to=a.vulnerable_to | extra) if extra - a.vulnerable_to else a


# --------------------------------------------------------------------------------------------------------
# New agents with a gradable potency
# --------------------------------------------------------------------------------------------------------

def outcome_kill(ttp_ratio: float, growth: float = GROWTH_PER_DAY) -> float:
    """Per-day kill implied by a measured prolongation of time-to-progression, treating the agent as acting only on
    regrowing cells: k = g * (1 - 1/ratio). OUTCOME-graded (from docs/universe/SWEEP_vaccines.md); inherits every bias
    of the control arm it is measured against."""
    return growth * (1.0 - 1.0 / ttp_ratio)


#: Time-to-progression ratios and their sources.
APAVAC_TTP_RATIO = 2.55            # 148 DLBCL dogs, retrospective, weak controls (PMID 31174615)
CD8_ADDBACK_TFS_RATIO = 338 / 71   # tumour-free survival, 8 infused vs 12 matched historical dogs (PMID 22355761)


def universe_agents(compartment: str, immunophenotype: str) -> tuple:
    from .lymphoma_catalogue import SYSTEMIC
    sys_ = compartment == SYSTEMIC
    out = []
    if immunophenotype == "B":
        out.append(Agent(
            "autologous tumour vaccine (APAVAC-type, HSPPC + hydroxyapatite)", Axis.IMMUNE_EFFECTOR, Layer.RECEPTOR,
            outcome_kill(APAVAC_TTP_RATIO), 1.0 if sys_ else 0.0, 1.0, True, division_gated=True,
            antigen_targets=(), vulnerable_to=frozenset({"antigen_presentation"}),
            evidence="DOG: 148 DLBCL dogs, median LSS 413 vs 165 d, 3-year survival 10% vs 8% (the tail is flat), no "
                     "adverse events in 300 dogs (PMID 31174615); RCT n=19 TTP 304 vs 41 d (PMID 24300788).",
            potency_evidence=("OUTCOME: k = g(1 - 1/2.55) = %.3f/day from the TTP ratio; control arms are weak "
                              "(median TTP 98 d vs ~176-244 d for contemporary CHOP) so this OVERSTATES. Treated as "
                              "acting on regrowing cells only: no persister effect (assumed, not shown). No brain "
                              "data, so brain access 0." % outcome_kill(APAVAC_TTP_RATIO)),
            note="Antigen-independent of CD20/CD19 (patient's own tumour antigens) but needs MHC-I; needs a surgical "
                 "node excision at diagnosis. Investigational in Europe."))
    # --- exposure-transfer agents from the resumed PK sweep (docs/universe/SWEEP_pk.md, sections 12, 14) ---
    # k = ln(1 + C/IC50)/assay_days, C = time-averaged FREE HUMAN exposure at label dosing (TRANSFER), IC50 = canine
    # CLBL-1 / lymphoid assay (MEASURED). The central scenario is used; the sweep's low/high are in the file.
    # Division-gating is assumed True for all three (cycle-independence is not shown) and brain access is 0 unless a
    # transferred value exists, both conservative. Substrate status from the label / mouse studies.
    out += [
        Agent("panobinostat (HDAC inhibitor)", Axis.APOPTOSIS, Layer.RECEPTOR, 0.115, 0.25 if not sys_ else 1.0, 1.0,
              True, division_gated=True, efflux_substrate=True,
              evidence="IN VITRO canine CLBL-1 IC50 5.4 nM (PMID 29983882) and 18.32 nM (PMID 37711439), both 24 h; "
                       "human label exposure 20 mg three times weekly; P-gp and BCRP substrate (label; mouse, PMID 37827699).",
              potency_evidence="TRANSFER: 0.115 /day central (range 0.017-0.38) from the geometric-mean IC50 9.95 nM "
                               "against a time-averaged free human concentration; no dog PK found. Brain access 0.25 "
                               "= mouse unbound Kp,uu 0.2-0.3 (PMID 37827699).",
              note="A pump substrate, so it does not reach the quiescent efflux-high progenitor (E5)."),
        Agent("vorinostat (HDAC inhibitor)", Axis.APOPTOSIS, Layer.RECEPTOR, 0.026, 0.0 if not sys_ else 1.0, 1.0,
              True, division_gated=True, efflux_substrate=False,
              evidence="IN VITRO canine IC50 0.6-4.8 uM, T-cell lines most sensitive (PMID 18593248; per-line values "
                       "and duration not retrieved); not limited by P-gp/BCRP in mouse (PMID 39893010).",
              potency_evidence="TRANSFER: 0.026 /day central (range 0.005-0.09) from human label exposure; the 2-day assay "
                               "duration is ASSUMED. Brain access 0 (no figure found).",
              note="Not a pump substrate."),
        Agent("bortezomib (proteasome inhibitor)", Axis.BCR_SIGNAL, Layer.NFKB, 0.048, 0.0 if not sys_ else 1.0, 1.0,
              True, division_gated=True, efflux_substrate=True,
              evidence="IN VITRO canine CLBL-1 IC50 15.1 nM at 48 h (thesis, PMID 38237918); NF-kB abolished (PMID "
                       "23337362); dog blood proteasome inhibition 66-90% at 1 h, n=2 (PMID 23579193).",
              potency_evidence="TRANSFER: 0.048 /day central (range 0.026-0.13) from human label exposure; below the bar "
                               "in every scenario. Antagonised by the cyclophosphamide metabolite in vitro (PMID 38237918).",
              note="Acts at the NF-kB layer of the serial B-cell receptor axis; P-gp substrate in cultured cells."),
    ]
    out.append(Agent(
        "autologous T-cell add-back after chemotherapy", Axis.IMMUNE_EFFECTOR, Layer.RECEPTOR,
        outcome_kill(CD8_ADDBACK_TFS_RATIO), 1.0 if sys_ else 0.0, 1.0, True, division_gated=True,
        antigen_targets=(), vulnerable_to=frozenset({"antigen_presentation"}),
        evidence="DOG: 8 infused vs 12 matched historical controls, tumour-free survival 338 vs 71 d, OS 392 vs 167 d; "
                 "cells persisted up to 49 d and reached tumour nodes (PMID 22355761).",
        potency_evidence=("OUTCOME: k = g(1 - 1/%.2f) = %.3f/day from tumour-free-survival ratio; historical controls, "
                          "n=8. Division-gated by assumption (conservative); brain access 0 (no data)."
                          % (CD8_ADDBACK_TFS_RATIO, outcome_kill(CD8_ADDBACK_TFS_RATIO))),
        note="Polyclonal, so independent of CD20/CD19; needs MHC-I. Window limited to the 49-day persistence."))
    return tuple(out)
