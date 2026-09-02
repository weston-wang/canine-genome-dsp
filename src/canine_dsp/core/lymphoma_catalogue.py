"""The escapes and agents this lymphoma analysis actually has, instantiated once so the search runs
on them rather than on prose.

ACCESS IS PER COMPARTMENT, because it has to be. Canine multicentric lymphoma is systemic, so most
of the disease sits where a systemic drug reaches it at full strength. But the disease has a
sanctuary -- the central nervous system, behind the blood-brain barrier -- and the interesting fact
about that compartment is not that access is low, it is that ACCESS IS LOW FOR SOME MODALITIES AND
NOT OTHERS:

    an antibody is essentially excluded (~0.002)
    most CHOP small molecules barely enter (~0.05)
    a lipophilic nitrosourea (lomustine) does enter (~0.50)
    hydroxychloroquine is lysosomotropic and ACCUMULATES (tumour:plasma ~100x, MEASURED in canine
        lymphoma, PMID 24991836)
    a T cell TRAFFICS ACROSS UNDER ITS OWN POWER (~0.50)

So the same regimen that closes every escape systemically can fail entirely in the sanctuary, and
the modality that rescues it is not a bigger dose of the same drug. That asymmetry is invisible to
any model carrying one access number per agent, and it is the lymphoma analogue of the
parenchyma/leptomeningeal split the histiocytic-sarcoma analysis found.

EVERY POTENCY IS ASSUMED UNLESS ITS `evidence` FIELD SAYS OTHERWISE. The search reports how many of
its inputs are assumptions, because a combination assembled entirely from assumptions is a
hypothesis rather than a result. All PMIDs were verified against PubMed.
"""

from __future__ import annotations

from .regimen import Agent, Axis, Escape, Layer

# The per-day growth rate the regimen must out-kill, from `lymphoma_scenarios` /
# `lymphoma_durable_response_analysis`: the P-glycoprotein efflux clone under full CHOP.
GROWTH_PER_DAY = 0.0903

SYSTEMIC = "systemic / nodal / marrow"
CNS = "CNS sanctuary (behind the blood-brain barrier)"
COMPARTMENTS = (SYSTEMIC, CNS)

# access by modality and compartment
SMALL_MOLECULE_ACCESS = {SYSTEMIC: 1.0, CNS: 0.05}
CNS_PENETRANT_ACCESS = {SYSTEMIC: 1.0, CNS: 0.50}    # lomustine class
LYSOSOMOTROPIC_ACCESS = {SYSTEMIC: 1.0, CNS: 0.30}   # hydroxychloroquine: accumulates in tissue
ANTIBODY_ACCESS = {SYSTEMIC: 1.0, CNS: 0.002}
HIGH_DOSE_ACCESS = {SYSTEMIC: 1.0, CNS: 0.30}        # high-dose methotrexate saturates the barrier
GLUCOCORTICOID_ACCESS = {SYSTEMIC: 1.0, CNS: 0.40}   # corticosteroids cross readily and are a
                                                     # mainstay of CNS lymphoma management; giving
                                                     # them generic small-molecule access (0.05)
                                                     # understated the one non-division-gated agent
                                                     # that is obtainable everywhere
INTRATHECAL_ACCESS = {SYSTEMIC: 0.05, CNS: 1.0}      # delivered INTO the compartment; the
                                                     # asymmetry runs the other way
CELL_ACCESS = {SYSTEMIC: 1.0, CNS: 0.50}             # a T cell crosses actively
RADIATION_ACCESS = {SYSTEMIC: 1.0, CNS: 1.0}         # by physics, if the field includes the site


# --- the escapes ---------------------------------------------------------------------------------
# One per axis at minimum, so that no agent is handed a free pass its neighbours do not get, plus
# the specific lesions that are real and measured in this disease.

ESCAPES = (
    Escape("P-glycoprotein / ABCB1 efflux", Axis.CYTOTOXIC, Layer.RECEPTOR, 1e-8,
           effluxes_substrates=True, evidence="MEASURED in canine lymphoma",
           note="THE DOMINANT REAL RELAPSE MECHANISM, and it sets the bar. Pumps doxorubicin and "
                "vincristine back out; does NOT pump prednisolone; fully reversed in vitro by "
                "PSC833 (Zandvliet et al. 2014, PMID 24975508). Upregulated at relapse in a subset "
                "of B-cell disease (PMID 25475167)."),
    Escape("BCRP / ABCG2 efflux", Axis.CYTOTOXIC, Layer.RECEPTOR, 1e-8,
           effluxes_substrates=True, evidence="MEASURED in canine lymphoma",
           note="A second pump, upregulated at relapse especially in T-cell disease; drug "
                "resistance occurred in 35/63 (55.6%) dogs (Zandvliet et al. 2014, PMID 25475167)."),
    Escape("TP53 / intrinsic-apoptosis evasion", Axis.APOPTOSIS, Layer.RECEPTOR, 1e-8,
           evidence="TRANSFER (general oncology)",
           note="A cell that cannot execute the intrinsic apoptotic programme is unkillable by an "
                "agent that works THROUGH that programme -- which includes BCL2 inhibition and "
                "glucocorticoids. Not genotyped routinely in these dogs."),
    Escape("CD20 antigen loss", Axis.IMMUNE_EFFECTOR, Layer.RECEPTOR, 1e-8,
           antigen_intact=False, removes_antigen="CD20", evidence="OBSERVED in canine lymphoma",
           note="OBSERVED, not hypothesised: CD20 loss in canine DLBCL patients treated with "
                "CD20-directed CAR-T (Peng et al. 2026, PMID 42480604), mirroring antigen-negative "
                "relapse after CAR-T in humans."),
    Escape("CD19 antigen loss", Axis.IMMUNE_EFFECTOR, Layer.RECEPTOR, 1e-8,
           antigen_intact=False, removes_antigen="CD19", evidence="TRANSFER (human CAR-T)",
           note="Included so a tandem CD19/CD20 construct is not handed a free pass: the model "
                "must be able to represent losing EITHER antigen. Canine B-cell lymphoma "
                "co-expresses CD19 and CD20 heterogeneously (PMID 42480604)."),
    Escape("BCR / NF-kB signal independence", Axis.BCR_SIGNAL, Layer.NFKB, 1e-8,
           evidence="TRANSFER (human DLBCL)",
           note="A lesion at or below the block restores survival signalling around it. Placed at "
                "the NF-kB layer so it defeats a BTK inhibitor, which acts above it -- the serial "
                "arithmetic, derived rather than asserted."),
    Escape("PI3K / AKT bypass", Axis.PI3K_PARALLEL, Layer.RECEPTOR, 1e-8,
           evidence="TRANSFER (general oncology)",
           note="Routes around the BCR arm entirely via the parallel survival axis."),
    Escape("drug-tolerant persister (non-dividing)", Axis.CELL_CYCLE, Layer.RECEPTOR, 1e-7,
           requires_division=False, evidence="TRANSFER (general oncology)",
           note="Survives by CEASING TO DIVIDE. EVERY division-gated agent -- all of CHOP, "
                "rabacfosadine, radiation -- has a margin of exactly zero against it by "
                "construction. Seeded at the highest rate here because it is a phenotypic state, "
                "not a mutation."),
    Escape("autophagy independence", Axis.AUTOPHAGY, Layer.RECEPTOR, 1e-9,
           evidence="ASSUMED",
           note="Symmetric with the other axis-specific escapes, so the autophagy inhibitor gets no "
                "free pass. UNMEASURED in canine lymphoma."),
    Escape("T-cell exhaustion / immunosuppressive microenvironment", Axis.IMMUNE_EFFECTOR,
           Layer.RECEPTOR, 1e-7, evidence="TRANSFER (human CAR-T)",
           note="The effector is present and primed but functionally silenced -- antigen is still "
                "displayed, so this is NOT antigen loss and is a separate escape. High rate "
                "because it is a reversible state rather than a mutation. This is the escape "
                "behind the first-in-dog CAR-T's transient response (PMID 27401141)."),
    Escape("B-lineage identity switch", Axis.LINEAGE, Layer.RECEPTOR, 1e-9,
           evidence="ASSUMED",
           note="A clone that stops being a B cell escapes every B-lineage-directed arm at once. "
                "Rare, and included so a lineage-directed agent is not handed a free pass."),
)


# --- the agents ----------------------------------------------------------------------------------

def agents_in(compartment: str) -> tuple:
    """Every candidate agent with access resolved for the compartment supplied."""
    sm = SMALL_MOLECULE_ACCESS[compartment]
    steroid = GLUCOCORTICOID_ACCESS[compartment]
    cnspen = CNS_PENETRANT_ACCESS[compartment]
    lyso = LYSOSOMOTROPIC_ACCESS[compartment]
    ab = ANTIBODY_ACCESS[compartment]
    cell = CELL_ACCESS[compartment]
    rad = RADIATION_ACCESS[compartment]
    return (
        # --- the CHOP backbone -------------------------------------------------------------------
        Agent("doxorubicin", Axis.CYTOTOXIC, Layer.RECEPTOR, 0.28, sm, 0.35, True,
              efflux_substrate=True, evidence="MEASURED (regimen outcome)", potency_evidence="ASSUMED",
              note="The most active CHOP cytotoxic and a P-gp SUBSTRATE, so the clone that sets the "
                   "bar pumps it out. Duty 0.35 reflects q21d dosing and the cumulative "
                   "cardiotoxicity cap. Regimen-level outcome measured (PMID 26279153)."),
        Agent("vincristine", Axis.CYTOTOXIC, Layer.RECEPTOR, 0.15, sm, 0.35, True,
              efflux_substrate=True, evidence="MEASURED (regimen outcome)", potency_evidence="ASSUMED",
              note="Also a P-gp substrate -- the same pump defeats both, which is why P-gp is one "
                   "lesion that covers the two most active drugs (PMID 24975508)."),
        Agent("cyclophosphamide", Axis.CYTOTOXIC, Layer.RECEPTOR, 0.12, sm, 0.35, True,
              efflux_substrate=False, evidence="MEASURED (regimen outcome)", potency_evidence="ASSUMED",
              note="An alkylator and NOT a classical P-gp substrate, so it survives the efflux "
                   "clone that defeats doxorubicin and vincristine."),
        Agent("prednisolone (glucocorticoid)", Axis.APOPTOSIS, Layer.RECEPTOR, 0.10, steroid, 1.0, True,
              division_gated=False, efflux_substrate=False,
              evidence="MEASURED in canine lymphoma (efflux-independence)", potency_evidence="ASSUMED",
              note="THE QUIETLY IMPORTANT AGENT. Kills lymphocytes by inducing apoptosis, so it is "
                   "NOT division-gated and reaches persisters; and the P-gp-selected canine "
                   "lymphoid line was resistant to doxorubicin and vincristine but NOT to "
                   "prednisolone -- measured, PMID 24975508. Defeated only by apoptosis evasion."),
        # --- other real cytotoxics ---------------------------------------------------------------
        Agent("rabacfosadine", Axis.CYTOTOXIC, Layer.RECEPTOR, 0.20, sm, 0.30, True,
              efflux_substrate=False, evidence="MEASURED in canine lymphoma", potency_evidence="ASSUMED",
              note="ORR 87%, median PFI 122 d as a single agent in naive dogs (Saba et al. 2020, "
                   "PMID 32346934). Duty capped by the delayed fatal pulmonary-fibrosis signal."),
        Agent("lomustine (CNS-penetrant nitrosourea)", Axis.CYTOTOXIC, Layer.RECEPTOR, 0.12,
              cnspen, 0.25, True, efflux_substrate=False, evidence="MEASURED in canine lymphoma", potency_evidence="ASSUMED",
              note="A real rescue agent (PMID 38961691) and LIPOPHILIC, so it is one of the few "
                   "cytotoxics that enters the CNS sanctuary. Duty capped by cumulative "
                   "hepatotoxicity/myelosuppression."),
        # --- CNS-directed delivery: the agents the search asked for -------------------------------
        # The first search found the sanctuary short on exactly three escapes -- CD20 loss, CD19
        # loss and immune exhaustion -- all of them IMMUNE-AXIS escapes, which by the own-axis rule
        # must be covered by NON-IMMUNE agents. In the CNS the non-immune agents were throttled to
        # 5% access, so the gap was a DELIVERY gap, not a potency one. These three are the real
        # clinical answer to that gap, and they are how CNS lymphoma is actually treated.
        Agent("high-dose methotrexate", Axis.CYTOTOXIC, Layer.RECEPTOR, 0.22,
              HIGH_DOSE_ACCESS[compartment], 0.20, True, efflux_substrate=False,
              evidence="TRANSFER (human CNS lymphoma standard)", potency_evidence="ASSUMED",
              note="The backbone of human CNS-lymphoma therapy precisely because high dosing "
                   "saturates the barrier and achieves cytotoxic CNS concentrations. Division-"
                   "gated, so it does not reach persisters. Requires leucovorin rescue and renal "
                   "monitoring; the duty cycle reflects that it cannot be given continuously."),
        Agent("intrathecal cytarabine", Axis.CYTOTOXIC, Layer.RECEPTOR, 0.20,
              INTRATHECAL_ACCESS[compartment], 0.15, True, efflux_substrate=False,
              evidence="TRANSFER (human/veterinary CNS prophylaxis)", potency_evidence="ASSUMED",
              note="Delivered INTO the sanctuary, so its access asymmetry runs the opposite way "
                   "from every systemic agent here: ~1.0 in the CNS and poor systemically. That is "
                   "why it is a sanctuary agent and not a systemic one. Division-gated."),
        Agent("craniospinal radiotherapy", Axis.DELIVERY, Layer.RECEPTOR, 0.30, rad, 21 / 365, True,
              efflux_substrate=False, evidence="TRANSFER (radiobiology)", potency_evidence="ASSUMED",
              note="Access 1.0 by physics and antigen-indifferent by physics, so it covers the "
                   "antigen-loss escapes the immune arm cannot. Still DIVISION-GATED, and its duty "
                   "is a 21-day course against a year -- which is why it contributes far less than "
                   "its potency suggests."),
        # --- the immune arms ---------------------------------------------------------------------
        Agent("anti-CD20 monoclonal antibody", Axis.IMMUNE_EFFECTOR, Layer.RECEPTOR, 0.10, ab, 1.0,
              False, division_gated=False, antigen_targets=("CD20",), evidence="ASSUMED",
              potency_evidence="ASSUMED",
              note="ANTIBODY ACCESS -- essentially excluded from the CNS sanctuary (0.002). No "
                   "efficacious caninized anti-CD20 product is currently established."),
        Agent("CD20 CAR-T", Axis.IMMUNE_EFFECTOR, Layer.RECEPTOR, 0.12, cell, 1.0, True,
              division_gated=False, antigen_targets=("CD20",),
              evidence="MEASURED in canine lymphoma (feasibility)", potency_evidence="ASSUMED",
              note="First-in-dog CD20 CAR-T was WELL TOLERATED but its TRANSIENT RNA construct gave "
                   "only a transient response -- stable expression is needed for durability "
                   "(Panjwani et al. 2016, PMID 27401141). Kills CD20+ and spares CD20-negative "
                   "cells in vitro (Sakai et al. 2020, PMID 32329214). CELL ACCESS: traffics into "
                   "the CNS under its own power, unlike the antibody. Potency ASSUMED."),
        Agent("tandem CD19/CD20 CAR-T", Axis.IMMUNE_EFFECTOR, Layer.RECEPTOR, 0.12, cell, 1.0,
              False, division_gated=False, antigen_targets=("CD19", "CD20"),
              evidence="MEASURED (construct)", potency_evidence="ASSUMED",
              note="Built for canine lymphoma to defeat single-antigen loss (Peng et al. 2026, "
                   "PMID 42480604). Modelled as antigen-directed still -- losing BOTH antigens "
                   "defeats it -- but the search treats CD20 loss and CD19 loss as separate "
                   "escapes, so a tandem construct is the only immune agent that survives either "
                   "one alone. Not yet obtainable as a product."),
        Agent("anti-PD-1 / anti-PD-L1 checkpoint blockade", Axis.IMMUNE_EFFECTOR, Layer.RECEPTOR,
              0.04, ab, 1.0, True, division_gated=False,
              evidence="TRANSFER (canine melanoma)", potency_evidence="ASSUMED",
              note="Not itself antigen-directed, but it works by relieving exhaustion of an "
                   "existing T-cell response. Antibody access, so excluded from the sanctuary."),
        # --- the position-independent, non-division-gated agents (the persister answers) ---------
        Agent("hydroxychloroquine (autophagy)", Axis.AUTOPHAGY, Layer.RECEPTOR, 0.10, lyso, 1.0,
              True, division_gated=False, efflux_substrate=False,
              evidence="MEASURED in canine lymphoma (Phase I)", potency_evidence="ASSUMED",
              note="THE BEST-EVIDENCED PERSISTER AGENT HERE, and it is in the right species AND the "
                   "right disease: a Phase I in 30 dogs with spontaneous lymphoma, HCQ + "
                   "doxorubicin, ORR 93.3%, median PFI 5 months, well tolerated, with TUMOUR "
                   "CONCENTRATION ~100x PLASMA (Barnard et al. 2014, PMID 24991836). "
                   "Lysosomotropic, so it accumulates rather than being efflux-limited. Potency "
                   "ASSUMED; the trial measured response, not a kill rate."),
        Agent("venetoclax (BCL2 inhibitor)", Axis.APOPTOSIS, Layer.RECEPTOR, 0.15, sm, 1.0, True,
              division_gated=False, efflux_substrate=False,
              evidence="MEASURED in canine lymphoma -- AND IT SPLITS BY IMMUNOPHENOTYPE",
              potency_evidence="MEASURED (EC50, PMID 36433867)",
              note="THE MOST CONSEQUENTIAL REAL MEASUREMENT IN THIS CATALOGUE. Neoplastic canine "
                   "T lymphocytes are SENSITIVE (mean EC50 0.023 uM) while most non-indolent "
                   "B-cell cancers are RESISTANT (mean EC50 288 uM), and BCL2 protein level does "
                   "NOT predict sensitivity (Jegatheeson et al. 2022, PMID 36433867). So this "
                   "agent belongs in a T-CELL regimen and not a B-cell one -- see "
                   "`venetoclax_potency_for`."),
        Agent("acalabrutinib (BTK)", Axis.BCR_SIGNAL, Layer.BTK, 0.06, sm, 1.0, True,
              division_gated=False, efflux_substrate=False,
              evidence="MEASURED in canine lymphoma (Phase I/II)", potency_evidence="ASSUMED",
              note="A real 20-dog canine B-cell lymphoma trial: well tolerated, ORR 25%, median PFS "
                   "22.5 days (Harrington et al. 2016, PMID 27434128). The modest single-agent "
                   "result is itself informative -- it does not clear the bar alone. Acts at BTK, "
                   "so it is defeated by an NF-kB-independence lesion BELOW it, which the model "
                   "derives rather than asserts."),
        # --- efflux reversal ---------------------------------------------------------------------
        Agent("P-gp / TGF-beta-inhibitor chemosensitiser", Axis.CYTOTOXIC, Layer.RECEPTOR, 0.08, sm,
              1.0, False, efflux_substrate=False, evidence="MEASURED in canine DLBCL (in vitro)", potency_evidence="ASSUMED",
              note="Attacks the efflux clone from the DRUG side: PSC833 fully reversed doxorubicin "
                   "and vincristine resistance in vitro (PMID 24975508), and a TGF-beta inhibitor "
                   "raised intracellular doxorubicin and LOWERED P-gp expression in a "
                   "doxorubicin-resistant canine DLBCL line (Hsu et al. 2021, PMID 33961622). Not "
                   "obtainable as a licensed veterinary product, and systemic P-gp inhibition "
                   "raises normal-tissue exposure of everything else."),
        # --- consolidation -----------------------------------------------------------------------
        Agent("total body irradiation + transplant", Axis.DELIVERY, Layer.RECEPTOR, 0.35, rad,
              14 / 365, True, efflux_substrate=False,
              evidence="MEASURED in canine lymphoma", potency_evidence="ASSUMED",
              note="Mechanism-agnostic and ANTIGEN-INDIFFERENT by physics, and it reaches the CNS "
                   "if the field includes it. But DIVISION-GATED, so it does not reach persisters, "
                   "and DUTY IS TINY -- a single ~14-day conditioning window against a year, which "
                   "is exactly why the engine finds a one-time consolidation does not carry "
                   "durability. Real cures exist with it (4/10 disease-free >=2 y when adoptive "
                   "T cells were added, PMID 34950726) at a real 7-13% mortality (PMID 38695516)."),
    )


def venetoclax_potency_for(immunophenotype: str) -> float:
    """Venetoclax's potency is not one number -- it is two, and the measurement says so.

    Jegatheeson et al. 2022 (PMID 36433867) measured mean EC50 0.023 uM in neoplastic canine T
    lymphocytes and 288 uM in most non-indolent B-cell cancers -- a ~10,000-fold split. Returning a
    single potency would erase the single most actionable real finding in this catalogue.
    """
    if immunophenotype not in ("B", "T"):
        raise ValueError("immunophenotype must be 'B' or 'T'")
    return 0.15 if immunophenotype == "T" else 0.005


#: Antigens that only exist on B-lineage disease. A CD20- or CD19-directed agent has NO TARGET on a
#: T-cell lymphoma, and offering it one is a category error, not a therapy.
B_LINEAGE_ANTIGENS = frozenset({"CD19", "CD20"})


def t_cell_effector(compartment: str) -> Agent:
    """The T-cell disease's equivalent of the CD20 CAR -- and it does not exist as a product.

    T-cell lymphoma is CD20-negative, so the entire CD20/CD19 arm is unavailable and a
    CD5- or CD52-directed effector is required instead. Marked NOT OBTAINABLE deliberately: no
    canine CD5/CD52-directed cellular product is established, and pretending otherwise would hand
    the T-cell search a therapy it does not have.
    """
    return Agent("CD5/CD52-directed cellular effector (T-lineage)", Axis.IMMUNE_EFFECTOR,
                 Layer.RECEPTOR, 0.12, CELL_ACCESS[compartment], 1.0, False,
                 division_gated=False, antigen_targets=("CD5",), evidence="NONE (does not exist)",
                 potency_evidence="ASSUMED",
                 note="Structurally the T-cell analogue of the CD20 CAR. NO CANINE PRODUCT EXISTS. "
                      "Included so the T-cell search is not silently handed the B-cell arm, and so "
                      "the gap it leaves is visible rather than hidden. A further hazard the model "
                      "does not price: a CD5-directed T-cell product attacks T cells, including "
                      "itself (fratricide).")


def agents_for(compartment: str, immunophenotype: str = "B", obtainable_only: bool = False) -> tuple:
    """Agents available for this immunophenotype, with venetoclax's potency resolved.

    Two immunophenotype-specific corrections, both of which the search got wrong without them:
      * B-lineage antigen-directed agents are REMOVED for T-cell disease -- a CD20 CAR has no
        target on a CD20-negative tumour. The first run of this search returned "CD20 CAR-T +
        venetoclax" as the minimal T-cell regimen, which is a category error.
      * Venetoclax's potency is resolved from the MEASURED immunophenotype split.
    """
    from dataclasses import replace
    out = []
    for a in agents_in(compartment):
        if a.name.startswith("venetoclax"):
            a = replace(a, potency=venetoclax_potency_for(immunophenotype))
        if immunophenotype == "T" and set(a.antigen_targets) & B_LINEAGE_ANTIGENS:
            continue  # no target on a CD20-negative tumour
        if obtainable_only and not a.obtainable:
            continue
        out.append(a)
    if immunophenotype == "T":
        t_arm = t_cell_effector(compartment)
        if not (obtainable_only and not t_arm.obtainable):
            out.append(t_arm)
    return tuple(out)


THE_FALSE_POSITIVE_THIS_FILE_CAUGHT = (
    "The first run of the search returned CD20 CAR-T + venetoclax as the MINIMAL T-CELL regimen. "
    "T-cell lymphoma is CD20-NEGATIVE. The agent had no target and the search could not see it, "
    "because the catalogue offered every agent to every immunophenotype.",
    "The correction is not a smaller number -- it is that ANTIGEN AVAILABILITY IS A PROPERTY OF "
    "THE DISEASE, not of the drug, so the agent pool itself has to depend on immunophenotype.",
    "Once corrected, the T-cell arm loses its obtainable cellular effector entirely, and the gap "
    "that was hidden by the category error becomes the headline finding for that phenotype.",
)


# Tumour burdens for the early-detection premise. A clinically obvious multicentric lymphoma is a
# large-burden disease; an MRD-level or screen-detected one is orders of magnitude smaller, and the
# probability that a given escape has ALREADY ARISEN scales with that number.
BURDEN_CLINICALLY_OBVIOUS = 1e11
BURDEN_EARLY_DETECTED = 1e8
BURDEN_MRD = 1e6

THE_ASYMMETRY_THAT_SHAPES_THE_ANSWER = (
    "TWO ESCAPES FORCE THE REGIMEN'S SHAPE, exactly as they did for histiocytic sarcoma. The "
    "drug-tolerant persister requires a NON-DIVISION-GATED agent, which excludes all of CHOP, "
    "rabacfosadine, lomustine and radiation. Antigen loss requires an effector that is not "
    "defeated by losing the target.",
    "In lymphoma there is a THIRD, and it is the one that is actually measured in this disease: the "
    "P-glycoprotein clone requires an agent that is NOT ITS SUBSTRATE, which excludes doxorubicin "
    "and vincristine -- the two most active drugs in the standard regimen.",
    "The agents that survive all three filters are a short list, and none of them is a conventional "
    "cytotoxic: prednisolone, hydroxychloroquine, venetoclax (T-cell only), a BTK inhibitor, and a "
    "cellular immune effector.",
)
