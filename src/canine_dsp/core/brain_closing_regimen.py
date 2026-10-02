"""[SUPERSEDED — AUDIT BANNER] Its closure rested on a P-gp/BCRP efflux co-dose no dog has ever been
given (a single point of failure), retracted downstream by core.brain_native_regimen. Nothing
imports it. Live answer: core.breed_wide_durability.

A combination that closes the brain compartment -- REVISED after verification demoted my first choice.

WHAT VERIFICATION DID TO THE FIRST VERSION

The first version of this module built the answer on SULFASALAZINE. Verification returned four things
and three of them were damaging:

  1. A SAFETY CLAIM I GOT WRONG. I wrote that its keratoconjunctivitis sicca was "REVERSIBLE ON
     WITHDRAWAL" and called it "the one most easily undone". Bjerkas 1985 (PMID 2860750) documents
     iatrogenic bilateral KCS in dogs from sulfasalazine that was PERMANENT IN ALL BUT ONE CASE.
     Monitoring by Schirmer tear test limits how many dogs are affected; it does not undo the injury
     in one that is. Its toxicity budget is raised 0.55 -> 0.85 accordingly, and at that budget the
     regimen built on it collapses.
  2. ITS ONE GLIOMA MONOTHERAPY TRIAL WAS TERMINATED EARLY. PMID 19840379, recurrent malignant
     glioma: zero clinical responses, median PFS 32 days, grade I-III adverse effects in 10 of 10.
  3. BRAIN:PLASMA 1.26% IN MOUSE, which is roughly the small-molecule access already assumed here --
     so no upside, and no rescue by size.
  4. AND ONE FAVOURABLE FINDING: PMID 42229231 (Redox Biology 2026), phase 1 in recurrent human GBM,
     MEASURED tumour glutathione depletion at day 3 and at one month. Target engagement in brain
     tumour is real. The mechanism works; the molecule is the wrong vehicle for a dog.

THE CENTRAL MECHANISM SURVIVED, AND GOT AN ANALOGUE IN THE RIGHT PLACE

Hangauer 2017 (PMID 29088702) is real and correctly cited, with a companion (Viswanathan 2017, PMID
28678785). More importantly, PMID 39192032 (EMBO J 2024) found QUIESCENT astrocyte-like glioma cells
selectively sensitive to GPX4 inhibition while PROLIFERATING ones were not -- quiescence-associated
GPX4 dependency, in a brain tumour. That is the closest independent support the persister argument
has.

AND THE ESCAPE I INVENTED TURNED OUT TO BE MEASURED. This model added a FERROPTOSIS-RESISTANCE escape
for symmetry so a ferroptosis inducer would get no free pass. PMID 40909720, from Hangauer's own
group, reports FSP1 and HDACs braking persister ferroptosis -- GPX4 blockade alone is often
insufficient. The invented escape is the FSP1/CoQ10 bypass, and it is real.

THAT IS WHY THE REVISED REGIMEN USES A STATIN RATHER THAN A PURE xc- INHIBITOR. A lipophilic statin
blocks the mevalonate pathway, which impairs selenocysteine-tRNA and therefore GPX4 BIOSYNTHESIS, and
ALSO depletes CoQ10, which is the FSP1 bypass's substrate. It hits the axis and its escape at once.
It is cheap, safe in dogs, and brain-penetrant.

AND HYDROXYCHLOROQUINE REPLACES SULFASALAZINE AS THE PERSISTER ARM, ON EVIDENCE RATHER THAN ELEGANCE

Persisters depend on an expanded autophagy-lysosome compartment (PMID 42106560, PMID 39476057).
Hydroxychloroquine blocks it -- and it is the ONLY agent anywhere in this project with a CANINE PHASE
I: PMC4203518, spontaneous canine lymphoma, up to 12.5 mg/kg/day PO tolerated, with TUMOUR
CONCENTRATION ROUGHLY 100x PLASMA. Against sulfasalazine's permanent ocular injury and terminated
glioma trial, that is not a close call.

THE REVISED REGIMEN

    surgical debulking             backbone
    parthenolide / DMAPT           NF-kB survival axis -- and it has DIRECT CANINE HS DATA (PMID
                                   38135509): kills canine HS lines AND primary cells dose-
                                   dependently via GLUTATHIONE DEPLETION AND ROS, and extends
                                   survival in a mouse model of disseminated canine HS. GI axis.
    lipophilic statin              ferroptosis axis -- GPX4 biosynthesis AND the FSP1 bypass.
                                   Hepatic axis.
    hydroxychloroquine             autophagy-lysosome axis. Marrow axis. Canine phase I exists.
    liposomal clodronate           lineage depletion. Hepatic axis.
    radiation                      access 1.0 by physics. CNS-local axis.
    P-gp/BCRP inhibitor co-dose    multiplies parthenolide and the statin

WHAT IT ACHIEVES

    TOLERABLE, headroom +0.05. Hepatic 0.95, GI 0.88, CNS-local 0.80, marrow 0.45.

    Minimum potencies to close ALL TEN escapes in BOTH compartments, at growth 0.055/day:
        parthenolide        0.10/day   (1.0x assumed -- no ask)
        statin              0.10/day   (1.2x assumed)
        hydroxychloroquine  0.10/day   (1.0x assumed -- no ask)
        clodronate          0.12/day   (2.0x assumed)
    margins: +0.0076 parenchyma, +0.0015 leptomeninges

THAT IS A SMALLER ASK THAN THE SULFASALAZINE VERSION ON EVERY AGENT, with no drug carrying a
permanent injury, and with the one agent that has canine phase I data doing the persister work.

WHAT STILL SINKS IT, AND THE FIRST ITEM IS THE MOST IMPORTANT SENTENCE HERE

  * NO PERSISTER-DIRECTED THERAPY HAS EVER REACHED CLINICAL APPROVAL IN ANY SPECIES. ResMap (PMID
    42284402, Sci Adv 2026) screened 94 compounds against 57 literature-derived persister targets and
    reproduced only 9 of 12 conserved hits on validation, "with variable degrees of persister
    specificity relative to general cytotoxicity". Whether GPX4 was among the 9 is not determinable
    from the abstract and is the single highest-value thing left to check.
  * FERROPTOSIS HAS NEVER BEEN STUDIED IN CANINE HISTIOCYTIC SARCOMA. Not once. Every claim here is
    inference from lineage, and THE LINEAGE ARGUMENT POINTS BOTH WAYS: canine HS upregulates SLC40A1
    (ferroportin, the iron EXPORTER) and FTL (ferritin) (PMID 41681403) -- which are ANTI-ferroptotic
    defences -- and tumour-associated macrophages are described in the literature as the
    ferroptosis-RESISTANT cell of the microenvironment (PMID 42226605), not the vulnerable one. The
    high-labile-iron argument I would have made cuts the other way once you read what the genes do.
  * Canine cells lack MLKL and cannot execute necroptosis (PMID 41524925). Cell-death wiring in
    Carnivora is not identical to mouse or human, and nobody has checked whether ferroptosis has
    analogous quirks. The only canine ferroptosis validation is a 2024 PREPRINT.
  * All four potencies are assumed, and the growth rate is unmeasured.

SO THE POSITION IS: A TOLERABLE, MOSTLY-OBTAINABLE REGIMEN CLOSES ALL TEN ESCAPES IN BOTH
COMPARTMENTS AT MODEST POTENCY ASKS -- resting on a mechanism class that has never produced an
approved therapy in any species, and that has never been tested in this disease.
"""

from __future__ import annotations

from .catalogue import ESCAPES, GROWTH_PER_DAY, LEPTOMENINGEAL, PARENCHYMA, agents_in
from .delivery import EFFLUX_INHIBITION
from .regimen import Agent, Regimen

SULFASALAZINE_ASSUMED_POTENCY = 0.10
CLODRONATE_ASSUMED_POTENCY = 0.06
OCULAR_DERATING = 0.73


PARTHENOLIDE_ASSUMED_POTENCY = 0.10
STATIN_ASSUMED_POTENCY = 0.08
HCQ_ASSUMED_POTENCY = 0.10


def _at(agent, potency):
    return Agent(agent.name, agent.axis, agent.layer, potency, agent.access, agent.duty,
                 agent.obtainable, agent.division_gated, agent.antigen_directed, agent.note)


def build(compartment: str, parthenolide_potency: float = PARTHENOLIDE_ASSUMED_POTENCY,
          statin_potency: float = STATIN_ASSUMED_POTENCY,
          hcq_potency: float = HCQ_ASSUMED_POTENCY,
          clodronate_potency: float = CLODRONATE_ASSUMED_POTENCY) -> Regimen:
    """The revised regimen, with all four deciding potencies exposed.

    Every potency is a parameter. A parameter held fixed in a sensitivity analysis is a parameter
    asserted to be irrelevant, and an earlier sweep here produced a FALSE NEGATIVE by fixing one.
    """
    pool = {a.name: a for a in agents_in(compartment)}
    return Regimen(
        "parthenolide + statin + hydroxychloroquine + clodronate + radiation, with efflux co-dose",
        [EFFLUX_INHIBITION.apply(_at(pool["parthenolide / DMAPT (NF-kB)"], parthenolide_potency)),
         EFFLUX_INHIBITION.apply(_at(pool["lipophilic statin (mevalonate)"], statin_potency)),
         _at(pool["hydroxychloroquine (autophagy)"], hcq_potency),
         _at(pool["liposomal clodronate"], clodronate_potency),
         pool["radiation"]])


def worst_margin(compartment: str, growth: float = GROWTH_PER_DAY, **kw) -> float:
    r = build(compartment, **kw)
    return min(r.effective_kill_against(e) - growth for e in ESCAPES)


def closes(compartment: str, growth: float = GROWTH_PER_DAY, **kw) -> bool:
    return worst_margin(compartment, growth, **kw) > 0


WHAT_VERIFICATION_DID_TO_THE_FIRST_VERSION = {
    "the_safety_claim_I_got_wrong": "I wrote that sulfasalazine's keratoconjunctivitis sicca was "
        "REVERSIBLE ON WITHDRAWAL and called it 'the one most easily undone'. Bjerkas 1985 (PMID "
        "2860750): iatrogenic bilateral KCS in dogs from sulfasalazine, PERMANENT IN ALL BUT ONE "
        "CASE. Monitoring limits how many dogs are affected; it does not undo the injury in one "
        "that is.",
    "its_glioma_trial_was_terminated": "PMID 19840379, recurrent malignant glioma: ZERO clinical "
        "responses, median PFS 32 days, grade I-III adverse effects in 10 of 10 patients.",
    "brain_plasma": "1.26% in mouse -- roughly the small-molecule access already assumed, so no "
                    "upside.",
    "and_one_favourable_finding": "PMID 42229231 (Redox Biology 2026), phase 1 in recurrent human "
        "GBM: MEASURED tumour glutathione depletion at day 3 and one month. THE MECHANISM WORKS; "
        "THE MOLECULE IS THE WRONG VEHICLE FOR A DOG.",
}

THE_INVENTED_ESCAPE_TURNED_OUT_TO_BE_REAL = (
    "This model added a FERROPTOSIS-RESISTANCE escape for symmetry, so a ferroptosis inducer would "
    "get no free pass the other axes do not get.",
    "PMID 40909720, from Hangauer's own group, reports FSP1 and HDACs braking persister ferroptosis "
    "-- GPX4 blockade alone is often insufficient. THE INVENTED ESCAPE IS THE FSP1/CoQ10 BYPASS, AND "
    "IT IS REAL.",
    "That is why the revised regimen uses a STATIN rather than a pure system xc- inhibitor: the "
    "mevalonate block impairs GPX4 BIOSYNTHESIS and ALSO depletes CoQ10, the bypass's substrate. It "
    "hits the axis and its escape at once.",
)

WHY_HCQ_REPLACES_SULFASALAZINE = (
    "Persisters depend on an expanded autophagy-lysosome compartment (PMID 42106560, PMID 39476057).",
    "Hydroxychloroquine is the ONLY agent anywhere in this project with a CANINE PHASE I: PMC4203518, "
    "spontaneous canine lymphoma, up to 12.5 mg/kg/day PO tolerated, TUMOUR CONCENTRATION ROUGHLY "
    "100x PLASMA.",
    "Against sulfasalazine's permanent ocular injury and terminated glioma trial, that is not a "
    "close call.",
)

PARTHENOLIDE_HAS_DIRECT_CANINE_HS_DATA = (
    "PMID 38135509 (JPET 2024): parthenolide kills canine HS CELL LINES AND PRIMARY CELLS "
    "dose-dependently, via GLUTATHIONE DEPLETION AND ROS GENERATION, with NF-kB pathway genes "
    "downregulated, and extends survival in a mouse model of DISSEMINATED CANINE HS.",
    "It is the only agent in this regimen with efficacy data in the right species AND the right "
    "disease -- and its mechanism is glutathione depletion, which is the same axis the ferroptosis "
    "arm attacks from the other side.",
)

# minimum potency per day to close all escapes in both compartments at growth 0.055
MINIMUM_POTENCIES = {
    "parthenolide": 0.10,
    "statin": 0.10,
    "hydroxychloroquine": 0.10,
    "clodronate": 0.10,
}
ASKS = {"parthenolide": 1.0, "statin": 1.2, "hydroxychloroquine": 1.0, "clodronate": 1.7}
MARGINS = {"parenchyma": 0.0074, "leptomeningeal": 0.0030}
TOXICITY_HEADROOM = 0.05

WHAT_STILL_SINKS_IT = (
    "NO PERSISTER-DIRECTED THERAPY HAS EVER REACHED CLINICAL APPROVAL IN ANY SPECIES. ResMap (PMID "
    "42284402, Sci Adv 2026) screened 94 compounds against 57 literature-derived persister targets "
    "and reproduced only 9 of 12 conserved hits on validation, 'with variable degrees of persister "
    "specificity relative to general cytotoxicity'. Whether GPX4 was among the 9 is the single "
    "highest-value thing left to check.",
    "FERROPTOSIS HAS NEVER BEEN STUDIED IN CANINE HISTIOCYTIC SARCOMA. Not once.",
    "AND THE LINEAGE ARGUMENT POINTS BOTH WAYS: canine HS upregulates SLC40A1 (ferroportin, the iron "
    "EXPORTER) and FTL (ferritin) (PMID 41681403), which are ANTI-ferroptotic defences, and "
    "tumour-associated macrophages are described as the ferroptosis-RESISTANT cell of the "
    "microenvironment (PMID 42226605). The high-labile-iron argument cuts the OTHER way once you "
    "read what those genes do.",
    "Canine cells lack MLKL and cannot execute necroptosis (PMID 41524925). Cell-death wiring in "
    "Carnivora is not identical to mouse or human, and the only canine ferroptosis validation is a "
    "2024 PREPRINT.",
    "All four potencies are assumed, and the growth rate is unmeasured.",
)

THE_POSITION = (
    "A TOLERABLE, MOSTLY-OBTAINABLE REGIMEN CLOSES ALL TEN ESCAPES IN BOTH COMPARTMENTS at modest "
    "potency asks -- the largest being 2.0x on clodronate.",
    "It rests on a mechanism class that HAS NEVER PRODUCED AN APPROVED THERAPY IN ANY SPECIES, and "
    "that HAS NEVER BEEN TESTED IN THIS DISEASE.",
)


HOW_THE_REQUIREMENT_WAS_DERIVED = {
    "what_was_open": {"NF-kB-independence": 0.0371, "drug-tolerant persister": 0.0124},
    "the_computed_requirement": "ONE non-division-gated small molecule, on an axis other than NF-kB, "
        "at potency >= 0.10/day, carried by efflux inhibition, closes both.",
    "why_a_small_molecule_specifically": "Every other non-division-gated agent here is a LIPOSOME, "
        "an ANTIBODY or a CELL. Those are excluded from the parenchyma by SIZE, and a transporter "
        "inhibitor cannot rescue a particle excluded by size.",
}

WHY_FERROPTOSIS_IS_NOT_A_GUESS = (
    "A drug-tolerant persister survives by CEASING TO DIVIDE, which is why this escape defeated "
    "every kinase inhibitor, radiation and lomustine in this analysis.",
    "The persister state has a known, specific liability: it depends on GPX4 to detoxify lipid "
    "peroxides and dies by FERROPTOSIS without it. Ferroptosis is non-apoptotic and ENTIRELY "
    "INDEPENDENT OF CELL-CYCLE STATE -- exactly the property required.",
    "SULFASALAZINE is the obtainable member of that class: inhibits system xc-, veterinary-available, "
    "oral, cheap, and a BCRP substrate so efflux inhibition multiplies it.",
)

WHY_THE_TOXICITY_AXIS_IS_THE_PART_THAT_MAKES_IT_ASSEMBLE = (
    "Sulfasalazine's dose-limiting toxicity in dogs is KERATOCONJUNCTIVITIS SICCA. NO OTHER AGENT IN "
    "THIS REGIMEN TOUCHES THAT AXIS.",
    "It is MONITORABLE BY SCHIRMER TEAR TEST -- a cheap in-clinic measurement.",
    "RETRACTED, AND IT WAS A SAFETY CLAIM: this module previously called the toxicity REVERSIBLE ON "
    "WITHDRAWAL and 'the one most easily undone'. IT IS PERMANENT IN ALL BUT ONE REPORTED CASE "
    "(Bjerkas 1985, PMID 2860750). Monitoring limits how many dogs are affected; it does not undo "
    "the injury in one that is.",
)

THE_REGIMEN = {
    "surgical debulking": "backbone; the only thing that reliably removes bulk",
    "parthenolide / DMAPT": "NF-kB survival axis -- non-division-gated. GI toxicity.",
    "sulfasalazine": "ferroptosis / system xc- -- non-division-gated. OCULAR toxicity.",
    "liposomal clodronate": "lineage depletion -- non-division-gated. Hepatic toxicity.",
    "radiation": "access 1.0 by physics. CNS-local toxicity.",
    "P-gp/BCRP inhibitor co-dose": "multiplies the two small molecules ~20x",
    "THE_POINT": "Four axes, four different organs, plus a co-dose. NOTHING STACKS.",
}

# escape -> (kill/day, margin) at the parenchyma, assumed potencies, no ocular de-rating
PARENCHYMA_AT_ASSUMED_POTENCY = {
    "MAPK reactivation above MEK (RAS/RAF)": (0.1019, 0.0469),
    "MEK target-site mutation": (0.1019, 0.0469),
    "activating ERK lesion": (0.1019, 0.0469),
    "RTK bypass into PI3K/AKT": (0.1019, 0.0469),
    "CSF1R-independence (lineage escape)": (0.1019, 0.0469),
    "antigen loss, MHC-I intact": (0.1019, 0.0469),
    "NF-kB-independence": (0.0599, 0.0049),
    "ferroptosis resistance (GPX4 up)": (0.0599, 0.0049),
    "drug-tolerant persister": (0.0846, 0.0296),
}

TOXICITY_TAKES_SOME_OF_IT_BACK = {
    "what_happens": "The efflux co-dose is not brain-selective, so it multiplies sulfasalazine's "
        "systemic exposure too. The ocular axis lands at 1.38 -- OVERSUBSCRIBED -- forcing "
        "sulfasalazine to 0.73 of full dose.",
    "the_consequence": "De-rated, the parenchymal margin on NF-kB-independence goes to -0.0065 and "
                       "THE COMPARTMENT REOPENS.",
    "why_this_is_recorded_rather_than_hidden": "This is exactly what the toxicity class was built "
        "for. Before it existed, the regimen above would have been reported as closing the brain.",
}

# doubling time (days) -> (parthenolide, sulfasalazine, clodronate) minimum potency per day
REQUIREMENT_BY_DOUBLING_TIME = {
    12.6: (0.10, 0.15, 0.14),
    10.0: (0.15, 0.20, 0.14),
    7.0: (0.20, 0.30, 0.22),
    5.0: (0.30, 0.40, 0.34),
    4.0: (0.40, 0.50, 0.42),
    3.0: (0.50, 0.70, 0.58),
}

THE_GROWTH_RATE_IS_THE_UNPINNED_PARAMETER = (
    "The assumed 0.055/day is a 12.6-DAY DOUBLING. Against a tumour with a 44-day median survival "
    "that is on the optimistic side.",
    "The requirement DEGRADES GRACEFULLY rather than breaking -- at a five-day doubling the asks are "
    "three- to sixfold on potencies assumed conservatively in the first place. But every row is a "
    "larger bet than the one above it, and NOTHING IN THIS PROJECT PINS WHICH ROW APPLIES.",
)

A_CORRECTION_TO_MY_OWN_STRESS_TEST = (
    "The first sensitivity sweep varied sulfasalazine and clodronate while holding PARTHENOLIDE "
    "FIXED, and concluded that NO combination closes the parenchyma at a seven-day doubling. That "
    "was an artefact of the sweep.",
    "Under fast growth the failing escape is FERROPTOSIS RESISTANCE, which sulfasalazine cannot "
    "cover because it is sulfasalazine's OWN escape. Raising sulfasalazine cannot touch it and ONLY "
    "PARTHENOLIDE CAN. Freeing the third potency closes it at a 2.0x ask.",
    "A PARAMETER HELD FIXED IN A SENSITIVITY ANALYSIS IS A PARAMETER ASSERTED TO BE IRRELEVANT, and "
    "here it was the deciding one.",
)

THE_HONEST_REQUIREMENT = {
    "parthenolide_potency_needed": 0.10,
    "sulfasalazine_potency_needed": 0.15,
    "sulfasalazine_assumed": 0.10,
    "sulfasalazine_ask": "1.5x",
    "clodronate_potency_needed": 0.14,
    "clodronate_assumed": 0.06,
    "clodronate_ask": "2.3x",
    "margins_at_0.15_and_0.15": {"parenchyma": 0.0058, "leptomeningeal": 0.0110},
    "STATUS_OF_BOTH_NUMBERS": "NEITHER HAS EVER BEEN MEASURED IN ANY SPECIES. Both are bench assays "
        "against canine HS cell lines that already exist -- CHS-1, CHS-2, CHS-3, DH82. A "
        "cell-viability curve for two cheap, licensed compounds. THAT IS THE ENTIRE REMAINING GAP.",
}

WHAT_IS_ASSUMED = (
    "Both potencies. They are the deciding numbers.",
    "CANINE HS FERROPTOSIS SENSITIVITY IS UNMEASURED. Macrophages are iron-handling cells, which "
    "could cut either way -- a histiocytic tumour might be unusually ferroptosis-PRONE because of "
    "labile iron, or unusually RESISTANT because of ferritin buffering. Under verification, not "
    "resolved here.",
    "The efflux multiplier is MOUSE, measured with COBIMETINIB, and the 2.5x systemic-toxicity "
    "charge is a reasoned estimate rather than a measurement.",
    "The ferroptosis-resistance escape was ADDED BY THIS MODEL for symmetry so a ferroptosis inducer "
    "would not get a free pass -- and it is one of the two tightest constraints in the table.",
    "Parthenolide is research-stage, and no canine efflux-inhibitor protocol is established.",
)

THE_BOTTOM_LINE = (
    "A REGIMEN THAT CLOSES THE BRAIN EXISTS IN THIS MODEL, it is built from agents that mostly "
    "exist, and it rests on TWO UNMEASURED POTENCIES AND ONE UNMEASURED TUMOUR PROPERTY.",
    "That is a materially different position from 'nothing closes it', and it is NOT the same thing "
    "as a treatment plan.",
)
