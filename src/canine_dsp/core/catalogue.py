"""The agents and escapes this analysis actually has, instantiated once so the search runs on them.

Access is PER COMPARTMENT, because it has to be. The first version of this file gave liposomal
clodronate an access of 1.0 and the search promptly returned it as a single agent closing every
escape -- a false positive produced entirely by that one number. A liposome does not cross an intact
blood-brain barrier. The correction is not merely to lower the number; it is that CLODRONATE'S ACCESS
IS DIFFERENT IN THE TWO COMPARTMENTS THIS TUMOUR OCCUPIES, and the difference is the interesting part.

    Systemic liposomal clodronate depletes PERIVASCULAR and MENINGEAL macrophages, which sit on the
    blood side of the barrier. It does NOT deplete parenchymal microglia behind an intact barrier.

So it has real access to the leptomeningeal compartment -- the one enhancing in 19/19 dogs -- and
almost none to invaded parenchyma. That is a genuinely useful asymmetry, and it is invisible to any
model with one access number per agent.

COMPARTMENT ACCESS, WITH BASIS

    invaded parenchyma, intact barrier      small molecules 0.021 -- MEASURED (chlorambucil, normal
                                            brain, PMC6128565); this project assumed 0.027 and they
                                            agree. Liposomes and antibodies ~0.001-0.01.
    leptomeningeal / CSF                    small molecules ~0.005 -- MEASURED (chlorambucil CSF
                                            0.1 ng/mL against ~20 ng/mL serum). LIPOSOMES ~0.30,
                                            because meningeal macrophages are blood-side and are
                                            depleted by systemic liposomal clodronate. ASSUMED.
    local / intrathecal / radiation         1.0 by construction.

EVERY POTENCY BELOW IS ASSUMED UNLESS THE NOTE SAYS OTHERWISE. The search reports how many of its
inputs are assumptions, because a combination assembled entirely from assumptions is a hypothesis
rather than a result.
"""

from __future__ import annotations

from .regimen import Agent, Axis, Escape, Layer

GROWTH_PER_DAY = 0.055

PARENCHYMA = "invaded parenchyma, intact barrier"
LEPTOMENINGEAL = "leptomeningeal / CSF"
LOCAL = "local / intrathecal / radiation"

# small-molecule access by compartment
SMALL_MOLECULE_ACCESS = {PARENCHYMA: 0.021, LEPTOMENINGEAL: 0.005, LOCAL: 1.0}
# liposome / large-particle access by compartment -- the asymmetry that matters
LIPOSOME_ACCESS = {PARENCHYMA: 0.01, LEPTOMENINGEAL: 0.30, LOCAL: 1.0}
# antibody access
ANTIBODY_ACCESS = {PARENCHYMA: 0.001, LEPTOMENINGEAL: 0.01, LOCAL: 1.0}
# a trafficking cell therapy crosses actively
CELL_ACCESS = {PARENCHYMA: 0.50, LEPTOMENINGEAL: 0.50, LOCAL: 1.0}

COMPARTMENTS = (PARENCHYMA, LEPTOMENINGEAL)

# --- the escapes, located by axis and height -------------------------------------------------------

ESCAPES = (
    Escape("MAPK reactivation above MEK (RAS/RAF)", Axis.MAPK_SERIAL, Layer.RAS, 1e-8,
           note="A secondary upstream alteration restoring ERK flow around the drug."),
    Escape("MEK target-site mutation", Axis.MAPK_SERIAL, Layer.MEK, 1e-8,
           note="Binding-site change. Defeats a MEK block; an ERK block is unaffected."),
    Escape("activating ERK lesion", Axis.MAPK_SERIAL, Layer.ERK, 1e-8,
           note="The convergence node's single point of failure. Escapes MEK and ERK blocks at a "
                "SINGLE-HIT rate rather than needing two independent events."),
    Escape("RTK bypass into PI3K/AKT", Axis.PI3K_PARALLEL, Layer.RECEPTOR, 1e-8,
           note="Loss of ERK-dependent negative feedback reactivates RTKs and the parallel axis, "
                "routing AROUND the whole MAPK arm."),
    Escape("CSF1R-independence (lineage escape)", Axis.LINEAGE_SURVIVAL, Layer.RECEPTOR, 1e-9,
           note="OBSERVED, not hypothesised: Diamond 2023 -- complete response, then resistance and "
                "transformation at 15 months."),
    Escape("antigen loss, MHC-I intact", Axis.IMMUNE_EFFECTOR, Layer.RECEPTOR, 1e-8,
           antigen_intact=False,
           note="Defeats an ANTIGEN-directed arm. MHC-I stays intact, so a missing-self NK "
                "mechanism NEVER FIRES -- these are two different escapes and this project spent a "
                "long time conflating them."),
    Escape("NF-kB-independence", Axis.SURVIVAL_SIGNAL, Layer.RECEPTOR, 1e-9,
           note="Symmetric with CSF1R-independence. Added so a survival-signal blocker is not "
                "handed a free pass the other axes do not get. UNMEASURED in canine HS."),
    Escape("ferroptosis resistance (GPX4 up)", Axis.FERROPTOSIS, Layer.RECEPTOR, 1e-9,
           note="Symmetric with CSF1R- and NF-kB-independence. Added so a ferroptosis inducer gets "
                "no free pass. UNMEASURED in canine HS."),
    Escape("autophagy-independence", Axis.AUTOPHAGY, Layer.RECEPTOR, 1e-9,
           note="Symmetric with the other axis-specific escapes. UNMEASURED in canine HS."),
    Escape("drug-tolerant persister", Axis.CELL_CYCLE, Layer.RECEPTOR, 1e-7,
           requires_division=False,
           note="Survives by CEASING TO DIVIDE. Every division-gated agent has a margin of exactly "
                "zero against it by construction."),
)

# --- the agents, priced by delivery ----------------------------------------------------------------


def agents_in(compartment: str) -> tuple:
    """Every candidate agent, with access resolved for the compartment supplied."""
    sm = SMALL_MOLECULE_ACCESS[compartment]
    lipo = LIPOSOME_ACCESS[compartment]
    ab = ANTIBODY_ACCESS[compartment]
    cell = CELL_ACCESS[compartment]
    return (
        Agent("trametinib (MEK)", Axis.MAPK_SERIAL, Layer.MEK, 0.20, sm, 1.0, True,
              note="Oral, continuous, and a canine HS trial is reported ongoing. The human "
                   "histiocytosis comparator shows MEK response is GENOTYPE-AGNOSTIC (ORR 89%, "
                   "Diamond 2019). Potency ASSUMED."),
        Agent("ERK inhibitor", Axis.MAPK_SERIAL, Layer.ERK, 0.20, sm, 1.0, False,
              note="The convergence node -- covers every lesion above it. NOT OBTAINABLE for a dog; "
                   "potency and kill ceiling both ASSUMED."),
        Agent("PI3K/AKT inhibitor", Axis.PI3K_PARALLEL, Layer.RECEPTOR, 0.15, sm, 1.0, False,
              note="Covers the RTK-bypass route. The only canine potency figure is HEMANGIOSARCOMA, "
                   "not histiocytic sarcoma."),
        Agent("CSF1R inhibitor", Axis.LINEAGE_SURVIVAL, Layer.RECEPTOR, 0.20, sm, 1.0, False,
              note="THE UPSTREAM LINEAGE NODE. Not a serial block that can be bypassed downstream -- "
                   "it removes a survival input. Brain-penetrant class member exists (BLZ945) with "
                   "no ratio ever published. NOT OBTAINABLE."),
        Agent("lomustine (nitrosourea)", Axis.CYTOTOXIC, Layer.RECEPTOR, 0.10, sm, 0.30, True,
              note="Standard of care in canine HS. Duty 0.30 reflects the ~4-dose cumulative "
                   "hepatotoxicity cap. NO canine CNS concentration exists at any dose."),
        Agent("radiation", Axis.DELIVERY, Layer.RECEPTOR, 0.30, 1.0, 21 / 365, True,
              antigen_directed=False,
              note="Access 1.0 by physics, and ANTIGEN-INDIFFERENT by physics too -- ionising "
                   "radiation does not care what the cell displays. Still DIVISION-GATED, so it "
                   "does not reach persisters. Duty is a 21-day course against a year. The model's "
                   "prediction that this fails is VALIDATED against measured 524-day medians."),
        Agent("anti-PD-1 (gilvetmab)", Axis.IMMUNE_EFFECTOR, Layer.RECEPTOR, 0.02, ab, 1.0, True,
              division_gated=False, antigen_directed=True,
              note="OBTAINABLE, with a named Merck grant programme. Antigen-directed, so antigen "
                   "loss defeats it. Magnitude is this project's measured two-point figure."),
        Agent("liposomal clodronate", Axis.IMMUNE_EFFECTOR, Layer.RECEPTOR, 0.06, lipo, 1.0, True,
              division_gated=False, antigen_directed=False,
              note="Responses in 2 of 5 dogs WITH HISTIOCYTIC SARCOMA. Uptake by PHAGOCYTOSIS, so "
                   "NOT division-gated (reaches persisters) and NOT antigen-directed (antigen loss "
                   "does not defeat it). ACCESS IS ASYMMETRIC: meningeal macrophages are blood-side "
                   "and are depleted; parenchymal microglia behind an intact barrier are not. "
                   "Potency ASSUMED -- no kill rate measured in any species."),
        Agent("parthenolide / DMAPT (NF-kB)", Axis.SURVIVAL_SIGNAL, Layer.RECEPTOR, 0.10, sm, 1.0,
              False, division_gated=False, antigen_directed=False,
              note="THE ONLY SMALL MOLECULE HERE THAT IS NEITHER DIVISION-GATED NOR "
                   "ANTIGEN-DIRECTED. NF-kB is a SURVIVAL signal, not a proliferation signal, so it "
                   "reaches persisters -- and being a small molecule it takes SMALL-MOLECULE ACCESS "
                   "and is EFFLUX-INHIBITABLE, which the liposome is not. Canine HS cell lines AND "
                   "primary cells undergo dose-dependent apoptosis; extends survival in a mouse "
                   "model of DISSEMINATED CANINE HS (Colorado State, Schlein/Brill, JPET 2023/24). "
                   "Research-stage, not licensed. Potency ASSUMED."),
        Agent("sulfasalazine (system xc-)", Axis.FERROPTOSIS, Layer.RECEPTOR, 0.10, sm, 1.0, True,
              division_gated=False, antigen_directed=False,
              note="FERROPTOSIS is the canonical persister vulnerability -- a non-dividing, "
                   "drug-tolerant cell depends on GPX4 to detoxify lipid peroxides, and dies without "
                   "it regardless of cell-cycle state. Sulfasalazine inhibits system xc-, starving "
                   "that pathway of cystine. VETERINARY-AVAILABLE, oral, cheap, and its "
                   "dose-limiting toxicity (keratoconjunctivitis sicca) sits on an axis NO OTHER "
                   "AGENT HERE USES and is monitorable by Schirmer tear test. It is also a BCRP "
                   "substrate, so efflux inhibition multiplies it. Potency ASSUMED; canine HS "
                   "ferroptosis sensitivity is UNMEASURED."),
        Agent("hydroxychloroquine (autophagy)", Axis.AUTOPHAGY, Layer.RECEPTOR, 0.10, sm, 1.0, True,
              division_gated=False, antigen_directed=False,
              note="A CANINE PHASE I EXISTS, which no other agent in this analysis can say: "
                   "PMC4203518, spontaneous canine lymphoma, HCQ up to 12.5 mg/kg/day PO tolerated, "
                   "and TUMOUR CONCENTRATION ~100x PLASMA. Persisters depend on an expanded "
                   "autophagy-lysosome compartment (PMID 42106560, PMID 39476057), so this reaches "
                   "them. Lysosomotropic weak base -- accumulates in tissue rather than being "
                   "efflux-limited. Potency ASSUMED; no canine HS data."),
        Agent("lipophilic statin (mevalonate)", Axis.FERROPTOSIS, Layer.RECEPTOR, 0.08, sm, 1.0,
              True, division_gated=False, antigen_directed=False,
              note="Hits GPX4 BIOSYNTHESIS (mevalonate -> selenocysteine tRNA) AND the FSP1/CoQ10 "
                   "bypass -- which is why it is mechanistically preferable to a pure system xc- "
                   "inhibitor: Hangauer's own group showed FSP1 and HDACs brake persister "
                   "ferroptosis (PMID 40909720), so GPX4 blockade alone is often insufficient. "
                   "Cheap, safe in dogs, and lipophilic statins are brain-penetrant. Potency "
                   "ASSUMED and deliberately set BELOW sulfasalazine's."),
        Agent("anti-CD47", Axis.IMMUNE_EFFECTOR, Layer.RECEPTOR, 0.08, ab, 1.0, False,
              division_gated=False, antigen_directed=False,
              note="Restores phagocytosis of the tumour cell by macrophages -- the effector step is "
                   "ENGULFMENT, not mitosis. CD47/SIRPa is conserved in dogs and high-affinity SIRPa "
                   "variants cross-react with canine CD47, but NO CANINE PRODUCT EXISTS. Conceptual "
                   "hazard: the tumour IS a macrophage, so this asks macrophages to eat macrophages."),
        Agent("CD204 cell therapy", Axis.IMMUNE_EFFECTOR, Layer.RECEPTOR, 0.20, cell, 1.0, False,
              division_gated=False, antigen_directed=False,
              note="Structurally the best answer in this project and it DOES NOT EXIST for dogs. "
                   "LINEAGE-directed: a clone that stops expressing CD204 has stopped being this "
                   "tumour."),
        Agent("intrathecal sustained release", Axis.DELIVERY, Layer.RECEPTOR, 0.12, 1.0, 1.0, False,
              antigen_directed=False,
              note="Reaches the compartment enhancing in 19/19 dogs. THE FORMULATION DOES NOT "
                   "EXIST -- DepoCyt discontinued 2017."),
    )


def obtainable_in(compartment: str) -> tuple:
    return tuple(a for a in agents_in(compartment) if a.obtainable)


THE_FALSE_POSITIVE_THIS_FILE_CAUGHT = (
    "The first version gave liposomal clodronate an access of 1.0, and the search returned it as a "
    "SINGLE AGENT CLOSING EVERY ESCAPE. That result was produced entirely by one wrong number.",
    "A liposome does not cross an intact blood-brain barrier. The correction is not just a smaller "
    "number -- it is that clodronate's access DIFFERS BETWEEN THE TWO COMPARTMENTS this tumour "
    "occupies, and the difference is the useful part.",
    "It has real access to the leptomeningeal compartment (meningeal macrophages are blood-side and "
    "are depleted by systemic liposomal clodronate) and almost none to invaded parenchyma. THAT "
    "ASYMMETRY IS INVISIBLE TO ANY MODEL WITH ONE ACCESS NUMBER PER AGENT.",
)
