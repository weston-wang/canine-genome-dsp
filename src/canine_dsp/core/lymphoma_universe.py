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


# --------------------------------------------------------------------------------------------------------
# Brain-closing candidates (docs/universe/SWEEP_regional.md and SWEEP_cnsregimens.md). Added after the widened
# search left the brain open; each is a route or regimen with human data behind it, graded below. Brain-only agents
# are returned for the CNS compartment only. NONE of these has a canine trial.
# --------------------------------------------------------------------------------------------------------
IT_ANTIBODY_DUTY = 2.0 / 7.0        # two intraventricular doses a week, ~1 day of CSF coverage per dose (DERIVED, popPK n=7)
#: CSF duty of a CSF-delivered CAR-T, from the human CNS-tumour trials in docs/universe/SWEEP_cart_kill.md: each dose is active about
#: 5-14 days; low 0.15 (dosing every 14 d, cells detected in ~38% of CSF samples), central 0.4 (every 14 d), high 0.7 (weekly).
#: DERIVED from window lengths, not measured as a duty fraction (ASSUMED-with-basis). Replaces the earlier 1/7 (one monkey, 24 h).
IT_CAR_T_DUTY_CONSERVATIVE = 0.15
IT_CAR_T_DUTY_CENTRAL = 0.4
IT_CAR_T_DUTY_HIGH = 0.7
#: In-vivo CAR-T kill rate (TRANSFER from human models; docs/universe/SWEEP_cart_kill.md): low 0.12 (Kimmel 2021 at an unexpanded
#: pool, PMID 33757357), central 0.35 (clinical myeloma fit 0.343, PMID 33565700), high 1.1 (Kimmel saturation 1.15). The dog value is
#: set by EXPANSION (0.12 needs ~6.5e7 CAR-T cells, 4-90x the doses given to dogs so far), not by potency.
CAR_T_KILL_LOW, CAR_T_KILL_CENTRAL, CAR_T_KILL_HIGH = 0.12, 0.35, 1.1
THIOTEPA_PROGRAM_DAYS = 115.0
THIOTEPA_PROGRAM_KILL = 0.13        # low end of the 0.13-0.21 /day outcome-implied range (SWEEP_cnsregimens s9)
#: Thiotepa is NOT a P-gp substrate on the evidence: the MDR1-overexpressing P388/ADR line has a GI50 1.07x that of the parent line
#: (NCI-60/ChEMBL, SWEEP_nongated); the only transporter link is MRP efflux of its glutathione conjugate (PMID 9788613).
#: Division-gating stays at the conservative default (dormant-cell kill is assumed, not shown).
THIOTEPA_PUMP_SUBSTRATE = False
#: Oral cytarabine ocfosfate time-average CSF level (nM) used for the kill rate; see the correction note in reassessed_agents.
OCFOSFATE_CSF_NM = 300.0


def brain_agents(compartment: str, immunophenotype: str, *, car_duty: float = IT_CAR_T_DUTY_CONSERVATIVE,
                 thiotepa_nongated: bool = False) -> tuple:
    from .lymphoma_catalogue import CNS
    out = [Agent(
        "high-dose thiotepa-based consolidation with autologous stem-cell rescue [human regimen]", Axis.CYTOTOXIC,
        Layer.RECEPTOR, THIOTEPA_PROGRAM_KILL, 1.0, THIOTEPA_PROGRAM_DAYS / 365.0, True,
        division_gated=not thiotepa_nongated, efflux_substrate=THIOTEPA_PUMP_SUBSTRATE and not thiotepa_nongated,
        evidence="HUMAN primary and secondary CNS lymphoma: 3-year PFS 78% (carmustine-thiotepa ASCT, n=114, PMID "
                 "42486133); 8-year event-free survival 67% (thiotepa-busulfan-cyclophosphamide ASCT, PMID 35834762); "
                 "treatment-related mortality 3-8%. Late relapses to 21 years show quiescent clones survive in some.",
        potency_evidence=("OUTCOME: whole-program effective brain kill 0.13-0.21 /day over ~115 days (Poisson cure model "
                          "from three randomised comparisons, residual burden 1e6-1e10 assumed; brain access is inside "
                          "the figure). It is a program average, not a per-agent potency, and says nothing about "
                          "division-gating, so the default is conservative: division-gated. NOT a pump substrate: no P-gp "
                          "cross-resistance (P388/ADR GI50 1.07x parent; MRP efflux of the glutathione conjugate only, PMID "
                          "9788613). Canine thiotepa PK or transplant use NOT FOUND."),
        note="A human regimen carried to the dog by transfer only; busulfan-autologous rescue is measured in 4 dogs "
             "(PMID 10534062) and autologous HCT is routine at specialist centres. Obligatory marrow aplasia needs a graft.")]
    if compartment == CNS and immunophenotype == "B":      # CD20 is a B-lineage antigen
        out.append(Agent(
            "anti-CD20 monoclonal antibody, intraventricular/intrathecal [buildable route]", Axis.IMMUNE_EFFECTOR,
            Layer.RECEPTOR, 0.099, 1.0, IT_ANTIBODY_DUTY, False, division_gated=False, antigen_targets=("CD20",),
            vulnerable_to=frozenset({"antigen_density", "macrophage_checkpoint", "adhesion_protection"}),
            evidence="HUMAN: intraventricular rituximab 25 mg cleared CSF lymphoma cells within hours with complement "
                     "activation in CSF (PMID 24190981); intravenous rituximab reaches CSF at ~0.1% of serum, so the "
                     "systemic route's 0.002 is consistent. No dog or Ommaya-in-dog data found.",
            potency_evidence="TRANSFER: the MEASURED canine B-cell depletion rate 0.099 /day (PMID 38662527) applied "
                             "inside the CSF compartment (access 1.0, human CSF pharmacokinetics); duty 2/7 from a "
                             "~1-day CSF coverage per dose. Kill of a quiescent progenitor is NOT measured. Deep "
                             "parenchymal access is unmeasured, so this is a leptomeningeal/periventricular claim.",
            note="Complement is limited in CSF (rat); CD20 loss defeats it."))
    if compartment == CNS:
        if immunophenotype == "B":
            out.append(Agent(
                "tandem CD19/CD20 CAR-T, intraventricular/intrathecal [buildable]", Axis.IMMUNE_EFFECTOR,
                Layer.RECEPTOR, 0.12, 1.0, car_duty, False, division_gated=False, antigen_targets=("CD19", "CD20"),
                resists_axis_independence=True, vulnerable_to=frozenset({"antigen_density"}),
                evidence="HUMAN: intraventricular/intrathecal CAR-T in CNS tumours reaches CSF and gives parenchymal "
                         "regressions in glioma (PMID 38454126, 41495049); IV CD19 CAR-T ORR 58-62% in CNS lymphoma "
                         "(PMID 35167655, 36537908). No dog data.",
                potency_evidence="TRANSFER-OUTCOME: 0.12 /day = the LOW end of a human-model kill rate (Kimmel 2021, PMID 33757357; "
                                 "central 0.35, high 1.1) at CSF access 1.0; CSF window 5-14 days per dose, duty low 0.15 / "
                                 "central 0.4 / high 0.7 (human CNS-tumour trials). The dog value is limited by expansion. "
                                 "Neurotoxicity 30-100% any grade, grade >=3 up to ~30% in human solid CNS trials."))
        else:
            for nm, ants in (("CD7-directed CAR-T, intraventricular/intrathecal [buildable]", ("CD7",)),
                             ("CD5 + CD7 dual-target CAR-T, intraventricular/intrathecal [buildable]", ("CD5", "CD7"))):
                out.append(Agent(
                    nm, Axis.IMMUNE_EFFECTOR, Layer.RECEPTOR, 0.12, 1.0, car_duty, False, division_gated=False,
                    antigen_targets=ants, resists_axis_independence=True,
                    vulnerable_to=frozenset({"antigen_density"}) if len(ants) == 1 else frozenset(),
                    evidence="HUMAN: CD7 CAR-T MRD-negative remission 19/20 (PMID 35500125); intraventricular CAR-T "
                             "reaches CSF (PMID 38454126). No dog product.",
                    potency_evidence="TRANSFER-OUTCOME: 0.12 /day (low end of the human-model range) at CSF access 1.0; duty low 0.15."))
    return tuple(out)


# --------------------------------------------------------------------------------------------------------
# Classes re-assessed after the user's objection ("I think you are dismissing vaccines, ebats, inhibitors, stem cells too
# easily"; docs/universe/SWEEP_hct_model.md, SWEEP_bispecific.md, SWEEP_exists.md, SWEEP_vaccines.md). Each is entered with
# an OUTCOME-calibrated or TRANSFERRED input, never excluded for lacking canine data (CLAUDE.md rule 13).
# --------------------------------------------------------------------------------------------------------
HCT_WINDOW_DAYS = 166.0           # day 14 to day 180
HCT_GRAFT_KILL_GROSS = 0.106      # central: 2.6 net e-folds over 166 d = 0.0157 /day net, plus the 0.0903 growth bar the clock subtracts
VACCINE_DTERT_PFS_K = 0.0         # PFS 11.4 vs 11.3 weeks (PMID 23902422)
VACCINE_DTERT_OS_K = outcome_kill(2.6)   # OS 76.1 vs 29.3 weeks, owner-selected controls
VACCINE_DTERT_KILL = 0.5 * (VACCINE_DTERT_PFS_K + VACCINE_DTERT_OS_K)   # midpoint of the two endpoint calibrations


def reassessed_agents(compartment: str, immunophenotype: str) -> tuple:
    from .lymphoma_catalogue import SYSTEMIC
    from .. import lymphoma_grounded_inputs as gi
    sys_ = compartment == SYSTEMIC
    out = [
        Agent("allogeneic DLA-identical HCT (graft-versus-lymphoma)", Axis.IMMUNE_EFFECTOR, Layer.RECEPTOR,
              HCT_GRAFT_KILL_GROSS, 1.0 if sys_ else 0.5, HCT_WINDOW_DAYS / 365.0, True, division_gated=False,
              antigen_targets=(), efflux_substrate=False, vulnerable_to=frozenset({"antigen_presentation"}),
              evidence="DOG: 15 B-cell dogs, 8 of 9 evaluable first-remission dogs alive >4 y (longest 2920 d), 2x4 Gy TBI + "
                       "cyclosporine, TRM 2/15 (PMID 35789057). HUMAN: allo vs auto relapse 8% vs 55% in T-cell lymphoma "
                       "(PMID 39270145); GVL responses to DLI in DLBCL, PTCL, follicular lymphoma (PMIDs 18684698, 21904377, 20606089).",
              potency_evidence=("OUTCOME: Poisson cure model on the dog plateau fractions gives a graft effect of 2.6 e-folds "
                                "(range 0.65-4.2) over a 166-day window, 0.0157 /day net, entered as gross 0.106 /day because the "
                                "clock subtracts growth; human AATT gives 2.26 e-folds. CNS access 0.5 from human secondary-CNS-lymphoma "
                                "allo (relapse 25% vs 8% systemic, PMID 34293518). Not division-gated and not a pump substrate by mechanism "
                                "(TRANSFER). T-cell disease: no dog series; human AATT transferred."),
              note="Needs a DLA-identical littermate (25% per sibling) and a transplant centre. MHC loss is its open escape. "
                   "Includes the 2x4 Gy TBI conditioning, so it replaces the autologous TBI+transplant entry."),
        Agent("dTERT genetic vaccine (Tel-eVax-type)", Axis.IMMUNE_EFFECTOR, Layer.RECEPTOR, VACCINE_DTERT_KILL,
              1.0 if sys_ else 0.0, 1.0, True, division_gated=True, antigen_targets=(),
              vulnerable_to=frozenset({"antigen_presentation"}),
              evidence="DOG: immune response in 13/14 and 19/21 dogs; OS 76.1 vs 29.3 weeks with COP (PMID 23902422); OS "
                       ">97.8 vs 37 weeks (PMID 20531395); OS 64.5 weeks with CHOP, n=17 (PMID 30537967); no adverse effects in 52 dogs.",
              potency_evidence=("OUTCOME: k = g(1 - 1/ratio) from two endpoints, PFS ratio 1.01 (k 0.0) and OS ratio 2.6 (k %.3f); the "
                                "midpoint %.3f /day is used. Controls are historical or owner-selected. Acts on dividing cells only "
                                "(assumed); no brain credit." % (VACCINE_DTERT_OS_K, VACCINE_DTERT_KILL))),
    ]
    # Existing continuous cytarabine delivery: oral cytarabine ocfosfate in dogs (serum Cmax 1.88-2.98 uM, half-life 23-29 h, CSF:serum
    # 0.54-1.2, PMID 37670479, 4 dogs). CORRECTION 2026-10-04: the "CSF 1.0-3.6 uM" earlier recorded as measured was the product of a
    # trough-sampled CSF:serum ratio and a PEAK serum value. The directly measured CSF values are troughs of 0.04-0.27 uM; the time-average
    # CSF level is DERIVED at about 0.3-1.4 uM (AUC/24 h x accumulation 2.1 x CSF:serum), so the LOW end, 0.3 uM, is used.
    ara = gi.continuous_it_cytarabine(immunophenotype, csf_setpoint_nM=OCFOSFATE_CSF_NM)
    out.append(Agent(
        "cytarabine ocfosfate, oral continuous", Axis.CYTOTOXIC, Layer.RECEPTOR, ara["kill_per_day"], 1.0, 1.0, True,
        division_gated=True, efflux_substrate=False, vulnerable_to=frozenset({"nucleoside_activation"}),
        evidence="DOG: oral cytarabine ocfosfate serum Cmax 1.88-2.98 uM, half-life 23-29 h, CSF:serum 0.54-1.2, measured CSF troughs "
                 "0.04-0.27 uM after 7 daily doses (PMID 37670479, 4 healthy dogs); "
                 "IV cytarabine CSF 8.3 uM at CSF:plasma 0.62 (PMID 1742843).",
        potency_evidence=("DERIVED: kill at a time-average CSF level of 0.3 uM (low end of the derived 0.3-1.4 uM band; measured troughs are "
                          "0.04-0.27 uM) against the canine lymphoma-line IC50 (48 h); continuous. Human use is intermittent (10-14 days per 28); "
                          "continuous dosing for years is not documented. Dog availability of the prodrug is research import only (Japan)."),
        note="Division-gated; defeated by loss of the activating enzyme (E2)."))
    if immunophenotype == "B":
        out.append(Agent(
            "CD3xCD20 bispecific T-cell engager (canine-specific) [needs development]", Axis.IMMUNE_EFFECTOR, Layer.RECEPTOR,
            0.16, 1.0 if sys_ else 0.5, 1.0, False, division_gated=False, antigen_targets=("CD20",),
            vulnerable_to=frozenset({"antigen_density"}),
            evidence="HUMAN: epcoritamab relapsed LBCL CR 40%, 64% of CRs ongoing at 24 months (PMID 39322711); epcoritamab + R-CHOP "
                     "CR 85%, 2-year PFS 80% (PMID 42622258); glofitamab PCNSL ORR 88% (PMID 42579821). Human CD3 arms do not bind canine "
                     "CD3 (43% identity), so a canine engager must be made; canine CD20 and CD3 binders exist.",
            potency_evidence="TRANSFER-OUTCOME: net tumour kill 0.08/0.16/0.30 per day derived from human time to CR (docs/universe/SWEEP_bispecific.md); "
                             "central used as gross. Brain multiplier 0.5 (range 0.2-0.85) from human CNS responses. Not division-gated, not MHC "
                             "dependent, not a pump substrate by mechanism."))
    return tuple(out)


# --------------------------------------------------------------------------------------------------------
# Human-licensed inhibitors entered by TRANSFER (docs/universe/SWEEP_inhibitors_partial.md): lymphoma-line IC50 x label exposure with
# free-fraction and medium-binding correction, k = ln(1 + C_free/IC50_free)/assay_days. Division-gating is assumed True and the pump
# status follows the label unless noted, both conservative. Brain access is the human CSF/plasma figure where one exists, else 0.
# --------------------------------------------------------------------------------------------------------
def inhibitor_agents(compartment: str, immunophenotype: str) -> tuple:
    from .lymphoma_catalogue import SYSTEMIC
    sys_ = compartment == SYSTEMIC
    out = []
    if immunophenotype == "T":
        out += [
            Agent("romidepsin (HDAC inhibitor, human-licensed for PTCL)", Axis.APOPTOSIS, Layer.RECEPTOR, 0.23,
                  1.0 if sys_ else 0.02, 1.0, True, division_gated=True, efflux_substrate=True,
                  evidence="HUMAN PTCL: ORR 25%, CR/CRu 15%, 89% of CR/CRu progression-free at 13.4 months (PMID 22271479, n=130). Dog: not studied.",
                  potency_evidence="TRANSFER: 0.23 /day (range 0.14-0.31) = label exposure (28-day mean 12.8 nM total, fu 0.07) against human "
                                   "T-cell line MOLT-4 GI50 2.06 nM at 72 h (PMID 26331334); brain access 0.02 (rhesus CSF:plasma AUC, PMID 15042312). "
                                   "P-gp substrate by label.",
                  note="Human-licensed; usable off-label in dogs."),
            Agent("belinostat (HDAC inhibitor, human-licensed for PTCL)", Axis.APOPTOSIS, Layer.RECEPTOR, 0.47,
                  1.0 if sys_ else 0.0, 1.0, True, division_gated=True, efflux_substrate=True,
                  evidence="HUMAN PTCL: ORR 25.8%, CR 10.8%, median duration of response 13.6 months, longest >=36 months (PMID 26101246, n=129).",
                  potency_evidence="TRANSFER: 0.47 /day (range 0.17-0.60) from a label clearance 74.4 L/h and an assumed 1.8 m2 body surface "
                                   "(ASSUMED for the AUC), fu 0.05, against Jurkat IC50 70 nM at 48 h (PMID 29533873). P-gp substrate; brain access not found (0)."),
        ]
    else:
        out.append(Agent(
            "zanubrutinib (BTK inhibitor, human-licensed)", Axis.BCR_SIGNAL, Layer.BTK, 0.087, 1.0 if sys_ else 0.43, 1.0, True,
            division_gated=False, efflux_substrate=True,
            evidence="HUMAN: PCNSL pooled ORR 85%, CR 54% (PMID 40931981); CSF/plasma 42.7% (PMID 35004280); canine acalabrutinib dogs: BTK "
                     "occupancy >90% but ORR 25%, PFS 22.5 d (PMID 27434128).",
            potency_evidence="TRANSFER: lineage-averaged 0.087 /day (range 0.03-0.23) = 25% BCR-dependent lineages at 0.34 /day plus 75% independent at "
                             "0.002 /day; the 25% responsive fraction is the measured dog acalabrutinib response rate. Acts at the BCR axis only."))
    return tuple(out)
