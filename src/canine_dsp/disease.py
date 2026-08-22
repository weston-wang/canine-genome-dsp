"""Canine histiocytic sarcoma (predisposed dog breed presentations) — knowledge model.

CONVERSATION-DERIVED. Every record in this module is reconstructed from a long
research/modelling conversation transcript (``_refactor/conversation.txt``), not
from primary literature and not from the ``canine_dsp`` source tree. It is a
faithful distillation of what that conversation *concluded* — including its
retractions, its honest "closed by a whisker" caveats, and the several places
where an earlier claim was overturned by a later check. Where the conversation
withdrew a claim, the withdrawal is recorded here rather than the withdrawn
claim. Numbers are the figures quoted in the transcript; they are illustrative
model inputs, most of them explicitly never measured in this species/disease.

The disease studied: primary intracranial histiocytic sarcoma (PIHS) in the
predisposed dog breed, a breed that supplies roughly half of all PIHS cases
(odds ratio ~21.5) — the signature of a single high-frequency germline
predisposition. The same lesion (MTAP/CDKN2A deletion, the most recurrent
genomic event across 104 canine HS cases) also drives the breed's pulmonary /
disseminated form. Measured benchmark for the intracranial disease: ~44-day
median survival with definitive therapy (Toyoda 2020), ~5-day palliative.

Four axes are captured:
  * SITES        — anatomical compartments and their occupancy/reachability
  * ESCAPES      — the twelve resistance/escape routes (ten + MGMT + germline)
  * MECHANISMS   — the load-bearing modelling ideas the answer turned on
  * ROUTES       — routes of drug delivery and the verdict attached to each

Pure standard library only (dataclasses + enum).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

# --------------------------------------------------------------------------- #
# 1. SITES / COMPARTMENTS                                                      #
# --------------------------------------------------------------------------- #

class SiteStatus(Enum):
    """Occupancy status of an anatomical compartment for this tumour."""

    OCCUPIED = "occupied"                  # the disease actually sits here
    RULED_OUT = "ruled_out"                # a compartment that does not exist
    OTHER_PRESENTATION = "other_presentation"  # same lesion, a different site


@dataclass(frozen=True)
class Site:
    """An anatomical compartment discussed for canine HS."""

    name: str
    status: SiteStatus
    reachability: str          # what makes it reachable — or not
    evidence: str              # the record the status rests on
    conclusion: str            # the call reached in the conversation


SITES: tuple[Site, ...] = (
    Site(
        name="Invaded brain parenchyma",
        status=SiteStatus.OCCUPIED,
        reachability=(
            "Tumour cells are tangled through brain tissue behind an INTACT "
            "blood-brain barrier. A systemic small molecule sees only its "
            "intrinsic penetration fraction; rodent-derived figures put that "
            "near ~2% (0.021-0.027), though dog brain is ~3x more permeable "
            "than mouse for P-gp substrates, so those figures are pessimistic."
        ),
        evidence=(
            "Thongtharb 2016 (PMC4873849), 23 primary intracranial HS, 11 of "
            "them dogs of the predisposed breed: 'brain masses of all cases were poorly "
            "demarcated and invading to the brain parenchyma' — 23/23, no "
            "exceptions. Corroborated by Mariani 2015, Toyoda 2020, Wada 2017."
        ),
        conclusion=(
            "Occupied in every dog from the start. The worst structural problem "
            "in the CNS scenario: access, not coverage. Closed in the model only "
            "by an intrinsically brain-penetrant agent (no procedure)."
        ),
    ),
    Site(
        name="Leptomeninges / CSF (fluid-borne, membrane-spreading)",
        status=SiteStatus.OCCUPIED,
        reachability=(
            "A bounded fluid compartment (brain-and-spine axis, CNS-restricted, "
            "unlike the disseminated form). Not reached by systemic drug at "
            "useful levels, but reachable directly by intrathecal dosing — a "
            "clean mass-balance PK problem: CSF ~12.5 mL, turnover 0.4%/min, "
            "~2.9 h half-life. Concentration is achievable with ~470x headroom; "
            "the real constraint is dosing FREQUENCY, i.e. a device problem."
        ),
        evidence=(
            "Mariani 2015: meningeal enhancement in 19/19 dogs, 'often profound "
            "and remote from the primary mass', even with a solitary well-defined "
            "mass; CSF pleocytosis in every dog sampled (mean 1509 cells/uL). "
            "Toyoda 2020: ~52% CSF-positive."
        ),
        conclusion=(
            "Occupied in every dog from the start. 'Removing the lump' is not a "
            "cure because this fluid-borne component carries the disease onward. "
            "~30x closer to closing than the parenchyma for an obtainable agent."
        ),
    ),
    Site(
        name='Discrete / extra-axial resectable "lump"',
        status=SiteStatus.RULED_OUT,
        reachability=(
            "Would be the most surgically removable kind of brain tumour — a "
            "discrete meningioma-like mass peelable off the brain surface. It "
            "would make surgery curative. It does not exist for this tumour."
        ),
        evidence=(
            "Retraction of an earlier reading. Ide 2011's 'focal solitary "
            "subdural' is a LOCATION descriptor, not an invasion statement — the "
            "abstract never describes the tumour-brain interface. The repo (and "
            "the assistant) had read it as 'discrete, peelable, resectable', "
            "which no paper says. Toyoda 2020 denies the compartment: 'in the "
            "absence of a defined intracranial subdural space'."
        ),
        conclusion=(
            "RULED OUT. The favourable compartment was a mirage — and it was the "
            "only favourable access number in the whole analysis. The 0.70 brain "
            "access figure it rested on was never measured anywhere. Part of the "
            "four-sites-to-two correction (anatomy, not pharmacology)."
        ),
    ),
    Site(
        name="Pulmonary / disseminated form",
        status=SiteStatus.OTHER_PRESENTATION,
        reachability=(
            "Systemically accessible: full drug exposure, no BBB discount. A "
            "resectable primary plus a regional nodal deposit surgery can't "
            "reach (two-compartment problem). Same underlying lesion."
        ),
        evidence=(
            "Sakai et al. 2015, 19 Dogs of this breed with pulmonary HS: 133-day median "
            "survival, frequent regional nodal involvement. Same germline-"
            "anchored MTAP/CDKN2A deletion as the CNS form."
        ),
        conclusion=(
            "The breed's other presentation of the same disease. Pharmacologically "
            "the easy case (intrinsic systemic access); its own durability is "
            "bounded by the nodal compartment debulking cannot reach and by the "
            "same escape biology as the brain."
        ),
    ),
)


# --------------------------------------------------------------------------- #
# 2. ESCAPE ROUTES                                                            #
# --------------------------------------------------------------------------- #

class EscapeAxis(Enum):
    """Which layer of biology an escape lives on."""

    PATHWAY = "pathway / signalling"
    LINEAGE = "lineage / cell identity"
    IMMUNE = "immune recognition"
    METABOLIC = "metabolic / stress-defence"
    DORMANCY = "dormancy / duty-cycle"
    DNA_REPAIR = "DNA repair"
    GERMLINE = "germline / host predisposition"


class Closure(Enum):
    """Honest status of an escape's closure."""

    CLOSED = "closed"                      # positive kill margin in the model
    MADE_IRRELEVANT = "made irrelevant"    # drug choice removes the lesion entirely
    ADDRESSED_CONDITIONAL = "addressed (conditional)"  # closed only if a hinge holds


@dataclass(frozen=True)
class Escape:
    """A resistance/escape route enumerated in the conversation."""

    number: int
    name: str
    axis: EscapeAxis
    meaning: str               # what the escape actually is
    closure: Closure
    how_closed: str            # by which agent/mechanism, if at all
    caveat: str                # the honest limit on that closure


ESCAPES: tuple[Escape, ...] = (
    # ---- the ten pathway/lineage/immune/metabolic/dormancy escapes ---------
    Escape(
        number=1,
        name="MAPK reactivation above the block",
        axis=EscapeAxis.PATHWAY,
        meaning=(
            "The tumour restores MAPK signalling above a MEK block "
            "(pathway reactivation / crosstalk), defeating trametinib."
        ),
        closure=Closure.CLOSED,
        how_closed=(
            "Covered by agents that are position-independent: radiation is "
            "antigen- and position-indifferent by physics (access 1.0); the "
            "load-bearing cytotoxic kills through mitotic machinery, not the "
            "signalling wire; PRMT5i attacks a genotype, not a pathway node."
        ),
        caveat=(
            "A block only covers lesions ABOVE it on a serial cascade, so "
            "trametinib (at MEK) alone buys only this route. Coverage comes from "
            "not depending on a pathway-position-specific agent."
        ),
    ),
    Escape(
        number=2,
        name="MEK target-site mutation",
        axis=EscapeAxis.PATHWAY,
        meaning=(
            "A mutation in MEK itself (the drug target) confers on-target "
            "resistance to the MEK inhibitor."
        ),
        closure=Closure.CLOSED,
        how_closed="Same position-independent agents as route 1 (radiation / cytotoxic / PRMT5i).",
        caveat=(
            "In the Monte Carlo it was the slowest-collapsing route; a next-gen "
            "target-site-resistant inhibitor would answer the drug side, but the "
            "final answer routes around it by not depending on MEK at all."
        ),
    ),
    Escape(
        number=3,
        name="Activating ERK lesion",
        axis=EscapeAxis.PATHWAY,
        meaning=(
            "A single activating ERK mutation sits at the convergence node and "
            "escapes BOTH a MEK inhibitor and an ERK inhibitor — a single-hit "
            "event, the crux that caps an ERK-convergence arm at ~0.97."
        ),
        closure=Closure.CLOSED,
        how_closed=(
            "Downstream blocking covers more (block ERK -> cover everything "
            "above it), but the convergence node is also the single point of "
            "failure. Ultimately closed by position-independent agents."
        ),
        caveat=(
            "Targeting a convergence node concentrates the vulnerability along "
            "with the coverage — deliberately seeded pessimistically (single-hit)."
        ),
    ),
    Escape(
        number=4,
        name="RTK bypass into PI3K/AKT",
        axis=EscapeAxis.PATHWAY,
        meaning=(
            "The cell reroutes survival through a receptor tyrosine kinase into "
            "the parallel PI3K/AKT axis, bypassing the MAPK block entirely."
        ),
        closure=Closure.CLOSED,
        how_closed=(
            "Paxalisib — a PI3K inhibitor, brain-penetrant (Kp,uu 0.31) and a "
            "confirmed non-substrate of both P-gp and BCRP — covers the parallel "
            "axis directly."
        ),
        caveat="A parallel-axis escape needs a parallel-axis drug; a serial-cascade block cannot reach it.",
    ),
    Escape(
        number=5,
        name="CSF1R / lineage independence",
        axis=EscapeAxis.LINEAGE,
        meaning=(
            "CSF1R is the master survival receptor for microglia and alveolar "
            "macrophages — the two lineages matching the two sites. The cell "
            "survives on CSF1R (partly MAPK-independent) or becomes lineage-"
            "independent; one CSF1R-inhibitor-resistance lesion can be downstream."
        ),
        closure=Closure.CLOSED,
        how_closed=(
            "Lineage REMOVAL rather than a rejoined wire: liposomal clodronate "
            "depletes the macrophage lineage by phagocytic suicide delivery — "
            "the only obtainable agent that is lineage-directed, non-antigen-"
            "directed and non-division-gated at once (responses in 2/5 HS dogs). "
            "PRMT5i backstops via the genotype."
        ),
        caveat=(
            "Clodronate's kill rate against canine HS has never been measured in "
            "any species; a liposome cannot cross an intact BBB (it depletes only "
            "blood-side perivascular/meningeal macrophages). Pexidartinib (the "
            "receptor-side option) is not obtainable for a dog and carries a "
            "microglia-depletion hazard."
        ),
    ),
    Escape(
        number=6,
        name="Antigen loss (MHC-I intact)",
        axis=EscapeAxis.IMMUNE,
        meaning=(
            "The tumour drops the neoantigen so a T-cell/vaccine effector can no "
            "longer recognise it. Critically, if MHC-I stays intact the NK "
            "'missing-self' backstop never fires — the one leak a vaccine can't "
            "cover, sharpened here because HS is a tumour OF the antigen-"
            "presenting lineage."
        ),
        closure=Closure.CLOSED,
        how_closed=(
            "Non-antigen-directed effectors: radiation is antigen-indifferent by "
            "physics; the cytotoxic doesn't care what the cell displays; anti-"
            "PD-1 (gilvetmab) carries the antigen-directed arm to the bar."
        ),
        caveat=(
            "Escape-substrate collapse + NK missing-self only insure the case "
            "where MHC-I IS lost. Antigen loss WITHOUT MHC-I loss (see the "
            "distinct 'vaccine failure without antigen loss' concern) is a "
            "separate, multiplicative discount that anti-PD-1 must carry."
        ),
    ),
    Escape(
        number=7,
        name="NF-kB independence",
        axis=EscapeAxis.PATHWAY,
        meaning=(
            "Canine HS subgroups are stratified by NF-kB, not MAPK. Trametinib "
            "sensitivity varies widely across lines and ERK/Akt activation does "
            "not predict which lines respond — a cell surviving on NF-kB evades "
            "any MAPK-directed therapy. Cuts against the whole MAPK premise."
        ),
        closure=Closure.CLOSED,
        how_closed=(
            "Parthenolide / DMAPT — an NF-kB inhibitor and glutathione depleter "
            "with actual canine-HS data (kills cell lines and primary cells, "
            "extends survival in a disseminated-HS mouse model)."
        ),
        caveat=(
            "The falsifying finding (Sakuma/Sakuma-adjacent 2025, PMID 40500939, "
            "11 lines; accession PRJDB17594) was banked in the sources file and "
            "its conclusion never propagated into code or README. The cheap "
            "experiment that would settle it: run the 11-line panel against an "
            "ERK inhibitor, stratified by NF-kB cluster."
        ),
    ),
    Escape(
        number=8,
        name="Ferroptosis resistance",
        axis=EscapeAxis.METABOLIC,
        meaning=(
            "Added for symmetry so a ferroptosis-inducing agent got no free "
            "pass — then turned out to be REAL: FSP1 (and HDACs) brake persister "
            "ferroptosis downstream of GPX4, so GPX4 inhibition alone is often "
            "insufficient."
        ),
        closure=Closure.CLOSED,
        how_closed=(
            "A lipophilic statin: the mevalonate block impairs GPX4 "
            "biosynthesis AND depletes CoQ10 (the FSP1 bypass's fuel) — it hits "
            "the axis and its escape at once."
        ),
        caveat=(
            "Ferroptosis has never been studied in canine HS, not once. The "
            "lineage argument runs the WRONG way: canine HS upregulates "
            "ferroportin and ferritin (anti-ferroptotic defences) and macrophages "
            "are described as the ferroptosis-resistant cell of the microenv."
        ),
    ),
    Escape(
        number=9,
        name="Autophagy independence",
        axis=EscapeAxis.METABOLIC,
        meaning=(
            "Drug-tolerant persisters depend on an expanded autophagy-lysosomal "
            "compartment as a survival state; a cell independent of it evades an "
            "autophagy inhibitor."
        ),
        closure=Closure.CLOSED,
        how_closed=(
            "Hydroxychloroquine (autophagy/lysosome inhibitor) — the only agent "
            "anywhere in the project with a canine phase I (spontaneous canine "
            "lymphoma, 12.5 mg/kg/day, ~100x tumour accumulation)."
        ),
        caveat=(
            "Unmeasured in canine HS. Nearly free to drop from the regimen "
            "(cost ~0.00002 to the margin), which is what shifts the weakest link "
            "to antigen loss when it goes."
        ),
    ),
    Escape(
        number=10,
        name="Drug-tolerant persister",
        axis=EscapeAxis.DORMANCY,
        meaning=(
            "A cell survives saturating drug not by mutating but by reversibly "
            "going quiet (growth ~0). Invisible to every division-gated agent — "
            "kinase inhibitors, radiation, lomustine — because there is little "
            "proliferative signalling to act on. The one escape that beat every "
            "targeted agent in the catalogue."
        ),
        closure=Closure.CLOSED,
        how_closed=(
            "NOT a new mechanism — a SCHEDULE. Persistence is a transient, "
            "reversible state, not a lineage, so it only threatens durability at "
            "RE-ENTRY. A continuously present agent (duty -> 1.0; metronomic "
            "dosing) is there when the cell wakes up. Duty-cycle, the third term "
            "of the kill identity."
        ),
        caveat=(
            "Two earlier modelling errors ran here: demanding kill > growth-rate "
            "against a non-dividing cell (comparing a rate to a state), and "
            "excluding DNA-damaging cytotoxics from position-independence. No "
            "persister-directed therapy has ever reached clinical approval in any "
            "species."
        ),
    ),
    # ---- the eleventh: MGMT repair ----------------------------------------
    Escape(
        number=11,
        name="MGMT repair",
        axis=EscapeAxis.DNA_REPAIR,
        meaning=(
            "MGMT is a repair enzyme that removes the exact O6-methylguanine "
            "lesion temozolomide (and, similarly, lomustine) makes — repairing "
            "damage as fast as the drug does it. Not a signalling reroute, so "
            "being indiscriminate is no defence: it is aimed straight at the "
            "drug's mechanism. THE strongest single predictor of alkylator "
            "benefit in human GBM. The eleventh route, absent from the ten."
        ),
        closure=Closure.MADE_IRRELEVANT,
        how_closed=(
            "Made IRRELEVANT (not defeated) by abandoning the DNA-damaging class "
            "entirely: switching to a microtubule agent (a mitotic poison) leaves "
            "no O6-lesion for MGMT to repair, so MGMT — and the whole alkylator-"
            "class resistance — cannot apply. An interim carboplatin swap "
            "(platinum crosslinks at N7, MGMT-irreparable) was rejected as too "
            "small a move; dose-dense TMZ and O6-benzylguanine were also tried "
            "and rejected (RTOG 0525 found no benefit; O6-BG oversubscribes the "
            "marrow axis)."
        ),
        caveat=(
            "Canine HS MGMT status genuinely unknown (canine glioma silenced 3/3, "
            "favourable but wrong lineage; human soft-tissue sarcoma ~92% MGMT-"
            "active, unfavourable but wrong species). A drug-resistance-gene "
            "paper suggests these cells are NOT MGMT-silenced and that resistance "
            "is alkylator-CLASS-shaped (MSH6 / mismatch-repair loss), which no "
            "within-class lesion swap can fix — the reason the class was dropped."
        ),
    ),
    # ---- the twelfth: germline second-primary -----------------------------
    Escape(
        number=12,
        name="Germline second primary",
        axis=EscapeAxis.GERMLINE,
        meaning=(
            "Not a way THIS tumour reroutes — a NEW independent primary. The "
            "predisposed dog breed carries a germline predisposition (the "
            "MTAP/CDKN2A locus) for HS. Curing the first tumour does not remove "
            "the predisposition, so the same lesion can re-arise in the brain, "
            "the lung, or the next tumour. Historically 'Route 6', long called "
            "permanently untestable (unobservable in a disease that kills in "
            "months; no dog survives long enough)."
        ),
        closure=Closure.ADDRESSED_CONDITIONAL,
        how_closed=(
            "PRMT5-inhibitor MAINTENANCE (TNG908 / TNG462, brain-penetrant, "
            "phase I/II). MTAP deletion makes a cell synthetically lethal-"
            "dependent on PRMT5 in a way normal cells are not, so indefinite "
            "dosing holds the germline genotype under selection: any clone from "
            "the same background dies before it becomes a tumour. This is what "
            "ten-year durability is actually made of — maintenance-at-emergence, "
            "not treating a tumour."
        ),
        caveat=(
            "Conditional on CNS access >= 0.50 (the ten-year hinge; the arm "
            "fails at 0.30, and CNS access has never been measured in a dog). "
            "The falsifier is one MTAP immunohistochemistry stain — if the "
            "tumour is MTAP-intact, maintenance does nothing. Cheapest decisive "
            "test in the project."
        ),
    ),
)


# --------------------------------------------------------------------------- #
# 3. MECHANISMS (the load-bearing modelling ideas)                            #
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Mechanism:
    """A modelling principle the conversation's conclusions turned on."""

    name: str
    statement: str
    conclusion: str


MECHANISMS: tuple[Mechanism, ...] = (
    Mechanism(
        name="Effective kill = potency x access x duty",
        statement=(
            "Every per-day kill rate in the model is the product of three terms: "
            "intrinsic potency (Emax against the cell), access (fraction that "
            "reaches the compartment), and duty cycle (fraction of time the drug "
            "is present). A kill margin closes an escape iff kill > tumour growth "
            "rate (~0.055/day at the assumed ~13-day doubling)."
        ),
        conclusion=(
            "The single recurring failure was multiplying two numbers from "
            "schedules/contexts that exclude each other: a mouse potency with a "
            "dog dose; one drug's penetration with another's blood level; a "
            "coverage claim in prose the arithmetic couldn't see; and — the "
            "retraction that broke a published answer — an ACCESS term from a "
            "monthly intra-arterial procedure multiplied by a DUTY term of "
            "continuous dosing."
        ),
    ),
    Mechanism(
        name="Coverage from pathway position (downstream covers more)",
        statement=(
            "Signal flows DOWN a serial cascade, so a block covers lesions ABOVE "
            "it and is defeated by lesions at or below it. Blocking MEK is "
            "defeated by an activating ERK lesion; blocking ERK covers everything "
            "above. On a serial axis, downstream blocking covers more."
        ),
        conclusion=(
            "'Go upstream' is NOT, by itself, a coverage argument — the "
            "arithmetic disagrees with the instinct. Upstream earns its place a "
            "different way: lineage survival is not on the cascade, so removing "
            "the macrophage lineage removes the cell's identity (a wire that "
            "cannot be rejoined below), which is why lineage removal is worth "
            "pursuing while a pathway-position argument is not."
        ),
    ),
    Mechanism(
        name="Dormancy is a duty-cycle problem, not a mechanism problem",
        statement=(
            "A drug-tolerant persister is a transient, reversible STATE, not a "
            "lineage or a mutation. It only threatens durability at re-entry, so "
            "an agent that is continuously present catches it when it wakes. A "
            "division-gated agent does not fail against persisters — a TRANSIENT "
            "one does."
        ),
        conclusion=(
            "The answer to the persister is a schedule (duty -> 1.0 / metronomic "
            "dosing), obtainable today, not an unproven persister-directed drug "
            "class. Fixed two model bugs: comparing a kill rate to a non-dividing "
            "STATE, and excluding cytotoxics from position-independence."
        ),
    ),
    Mechanism(
        name="Treatment clock: cumulative vs acute toxicity",
        statement=(
            "Fixing access x duty at an instant ignores whether the schedule can "
            "be SUSTAINED for as long as the cure calculation needs. An ACUTE "
            "dose-limiting toxicity caps the DOSE; a CUMULATIVE one caps the "
            "DURATION. Only the second breaks a plan that must run for months."
        ),
        conclusion=(
            "Sagopilone's cumulative neuropathy capped duration at ~84 days "
            "(17% of the ~498 needed) -> complete response then relapse — which "
            "matches the one real this breed case (response day 99, regrowth day 124, "
            "death day 195). Lisavanbulin's toxicity is ACUTE (CNS), capping "
            "dose not duration. This gave the model its missing third outcome "
            "beyond 'cure or death': respond-then-relapse / sustained control via "
            "on/off cycling (an effective duty of 0.6-0.75 held indefinitely)."
        ),
    ),
    Mechanism(
        name="Synthetic-lethal genotype vs reroutable pathway",
        statement=(
            "Every pathway-directed agent attacks a wire that can be rerouted — "
            "the ten escapes are ways to reroute a pathway. A synthetic-lethal "
            "agent (PRMT5 inhibitor against MTAP deletion) attacks a GENOTYPE: "
            "the tumour cannot reroute around a homozygous deletion, because "
            "escaping would require re-acquiring a deleted locus (a reversal, not "
            "a mutation). It is also not division-gated, so it reaches dormant "
            "cells directly."
        ),
        conclusion=(
            "A different KIND of target than anything else considered. It is "
            "antigen-free, immune-free, and durable for a reason nothing else "
            "shares, and it collapses all three of the user's requirements "
            "(all cases, all sites, ten-plus years) into one target, because the "
            "MTAP/CDKN2A deletion is the same lesion in the brain, the lung, and "
            "the next tumour."
        ),
    ),
    Mechanism(
        name="Maintenance-at-emergence",
        statement=(
            "Ten-year durability is not treating a tumour — it is holding the "
            "germline genotype under selection so that any clone arising from the "
            "same background dies before it becomes a tumour. Indefinite dosing "
            "is plausible precisely because the drug is active only in cells "
            "carrying a deletion normal tissue does not have."
        ),
        conclusion=(
            "This is the only construct in the project that can address a SECOND "
            "primary, and thus the only one that can carry a >10-year claim. It "
            "turns on one measured-nowhere number: CNS access >= 0.50 (holds) vs "
            "0.30 (fails) — the honest hinge of the whole ten-year story."
        ),
    ),
)


# --------------------------------------------------------------------------- #
# 4. ROUTES of delivery                                                       #
# --------------------------------------------------------------------------- #

class RouteVerdict(Enum):
    """The disposition the conversation reached for a delivery route."""

    ADOPTED = "adopted"                # the route the final answer rests on
    VIABLE_FOR_CSF = "viable for CSF"  # works for the leptomeningeal compartment
    RETRACTED = "retracted"            # was adopted, then withdrawn
    INEFFECTIVE = "ineffective"        # doesn't change the answer here
    ABANDONED = "abandoned"            # superseded, no longer needed


@dataclass(frozen=True)
class DeliveryRoute:
    """A route for getting drug into the CNS compartments."""

    name: str
    how_it_works: str
    access_figures: str
    verdict: RouteVerdict
    reasoning: str


ROUTES: tuple[DeliveryRoute, ...] = (
    DeliveryRoute(
        name="Oral / systemic, intrinsic access",
        how_it_works=(
            "Pick agents selected FOR CNS exposure so access travels with the "
            "drug at every dose — one schedule, nothing to reconcile between "
            "access and duty."
        ),
        access_figures=(
            "Access >= ~0.30 closes both compartments with no efflux co-dose. "
            "Lisavanbulin 1:1 brain:plasma (rodent), oral; paxalisib Kp,uu 0.31, "
            "confirmed non-substrate of P-gp/BCRP; temozolomide CSF:plasma ~0.20 "
            "(later superseded). Dog brain ~3x more permeable than mouse for "
            "P-gp substrates — the rodent was the outlier, so 0.021-0.027 figures "
            "were too pessimistic."
        ),
        verdict=RouteVerdict.ADOPTED,
        reasoning=(
            "Buying access with chemistry instead of a procedure removed the "
            "single point of failure. Contrast — brain-penetrant is NOT brain-"
            "effective: ANG1005 (receptor-mediated transcytosis) delivered "
            "paclitaxel at 86x free drug into brain and still returned 5.8% "
            "glioma response. The final regimen is delivered entirely this way."
        ),
    ),
    DeliveryRoute(
        name="Intra-arterial + osmotic (mannitol) BBB disruption",
        how_it_works=(
            "Catheterise the artery feeding the tumour, briefly open the barrier "
            "with hyperosmolar mannitol, deliver drug directly (Neuwelt "
            "protocol, run monthly)."
        ),
        access_figures=(
            "The ONLY in-vivo canine tissue-access number in the project: "
            "methotrexate 100-300 ng/g via artery alone -> 1,100-5,000 ng/g "
            "after mannitol, n=33 dogs — a measured 3.7-50x gain."
        ),
        verdict=RouteVerdict.RETRACTED,
        reasoning=(
            "SCHEDULE-COHERENCE CONTRADICTION. The published margins multiplied "
            "this access boost (a monthly surgical procedure) by duty = 1.0 "
            "(continuous presence). A drug delivered by a monthly procedure "
            "cannot be present continuously — only the physically impossible row "
            "closed. Also stacked toxicity: osmotic opening raises seizure risk, "
            "which compounds with radiation on the CNS axis. What SURVIVES: "
            "osmotic disruption genuinely raises drug levels in dogs; what was "
            "lost was the right to multiply that by continuous dosing."
        ),
    ),
    DeliveryRoute(
        name="Intrathecal (into the CSF)",
        how_it_works=(
            "Inject drug directly into the spinal fluid to reach the "
            "leptomeningeal / fluid-borne compartment that systemic drug and "
            "surgery cannot."
        ),
        access_figures=(
            "Clean mass-balance PK: CSF ~12.5 mL (production 0.05 mL/min / "
            "turnover 0.4%/min; cross-checks 16.2 mL), ~2.9 h half-life. At 1 mg, "
            "peak 176,367 nM = 470x the 375 nM target. Frequency wall: 24 h "
            "needs 0.675 mg, 48 h needs 214 mg, 72 h ~68 g — a 317x dose buys "
            "one extra day."
        ),
        verdict=RouteVerdict.VIABLE_FOR_CSF,
        reasoning=(
            "Concentration is not the constraint (by ~470x) — the first number in "
            "the chain to come back with room to spare. The real constraint is "
            "dosing FREQUENCY, i.e. a device problem (implanted port or slow-"
            "release), not pharmacology. Caveats: bulk-flow clearance only, so "
            "residence times are upper bounds and the daily interval is the soft "
            "number; bulk fluid level != cell exposure on membrane surfaces; "
            "neurotoxicity unaddressed."
        ),
    ),
    DeliveryRoute(
        name="Focused ultrasound",
        how_it_works=(
            "Focally open tight junctions in the BBB with focused ultrasound to "
            "admit systemic drug at a targeted spot."
        ),
        access_figures=(
            "No usable gain here: even granting a focal tumour, trametinib still "
            "reaches only ~0.042/day — under the ~0.055/day growth rate."
        ),
        verdict=RouteVerdict.INEFFECTIVE,
        reasoning=(
            "It is FOCAL and this disease is DIFFUSE (23/23 poorly demarcated; "
            "meningeal enhancement remote from the mass in 19/19), so apply() "
            "returns the agent unimproved against diffuse disease. And it opens "
            "tight junctions while the binding constraint is an efflux PUMP — "
            "opening junctions does nothing for a drug that is pumped back out. "
            "Changes nothing structurally."
        ),
    ),
    DeliveryRoute(
        name="Efflux modulation (P-gp / BCRP co-dose)",
        how_it_works=(
            "Co-dose a P-gp/BCRP inhibitor so a systemic small molecule is no "
            "longer pumped out of the brain."
        ),
        access_figures=(
            "20x access boost, measured (Choo 2014: cobimetinib brain:plasma 0.3 "
            "wild-type -> 6.0 with a co-dosed inhibitor; 11.0 in knockout). "
            "Applied to parenchymal access 0.021 -> ~0.42."
        ),
        verdict=RouteVerdict.ABANDONED,
        reasoning=(
            "Raises access for SMALL MOLECULES ONLY, and the escapes that bind "
            "this tumour are covered by things that aren't small molecules "
            "(liposomes excluded by SIZE, which a pump-blocker cannot rescue). It "
            "closes only one escape (the sole obtainable pathway agent, "
            "trametinib, sits at MEK, so it buys only MAPK-reactivation above "
            "it). It is not brain-selective, so it also raises the partner drug's "
            "systemic exposure (gut/liver/kidney), forcing toxicity de-rating, "
            "and it has no canine protocol — it became the single point of "
            "failure for the brain result. The breed note: Dogs of this breed are MDR1/ABCB1 "
            "wild-type (~0.05%, not enriched) — read as unfavourable (intact pump "
            "keeps drug out), but under inhibition a wild-type pump is fully "
            "inhibitable. Abandoned once intrinsic-access agents removed the need."
        ),
    ),
)


# --------------------------------------------------------------------------- #
# The regimen the arc converged on, and the honest bottom line                #
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Regimen:
    """The therapeutic combination the conversation converged on."""

    induction: tuple[str, ...]
    maintenance: tuple[str, ...]
    load_bearing: str
    delivery: str
    durability: str
    honest_status: str


FINAL_REGIMEN = Regimen(
    induction=(
        ("Brain-penetrant microtubule agent (mitotic poison; lisavanbulin / "
        "RGN3067 / RGN6024 — one of the class, not all three)"),
        "Paxalisib (PI3K inhibitor; non-substrate of P-gp/BCRP)",
        "Liposomal clodronate (lineage depletion)",
        "Anti-PD-1 (gilvetmab)",
        ("PRMT5 inhibitor (TNG908 / TNG462) — genotype-directed, added for the "
        "breed-wide MTAP/CDKN2A target"),
    ),
    maintenance=(
        ("PRMT5 inhibitor alone — holds the germline genotype under selection "
        "against a second primary (maintenance-at-emergence)"),
    ),
    load_bearing=(
        "Only the microtubule agent is load-bearing for the tumour itself "
        "(dropping any other companion keeps the margin positive; dropping it "
        "reopens everything). The PRMT5 inhibitor is what carries the ten-year / "
        "second-primary claim."
    ),
    delivery=(
        "Systemic / oral, intrinsic access — NO catheter, NO anaesthesia, NO "
        "efflux co-dose, NO osmotic disruption procedure."
    ),
    durability=(
        "Induction clears in ~112-187 days. With realistic on/off cycling, "
        "sustained control ~1.4-2.0 years (all eleven modelled escapes close at "
        "both sites; 0/45 double and 0/120 triple combination-escapes "
        "uncovered). >10 years is NOT a default property — it requires the "
        "maintenance arm and CNS access >= 0.50."
    ),
    honest_status=(
        "A class-and-mechanism argument, not a prescription. The named drugs are "
        "not obtainable (one out-licensed/discontinued, others preclinical and "
        "rodent-only). Three-plus potencies and the tumour growth rate have "
        "never been measured in this disease. Against a measured 44-day "
        "benchmark this is a large improvement; against the model's own history "
        "it is one more step in a build/retract/rebuild arc whose recurring "
        "error is 'two numbers from different contexts multiplied together'."
    ),
)


# --------------------------------------------------------------------------- #
# Convenience accessors                                                        #
# --------------------------------------------------------------------------- #

def escapes_by_axis(axis: EscapeAxis) -> list[Escape]:
    """Return all escapes living on a given biological axis."""
    return [e for e in ESCAPES if e.axis is axis]


def occupied_sites() -> list[Site]:
    """Return the compartments the disease actually occupies."""
    return [s for s in SITES if s.status is SiteStatus.OCCUPIED]


def counts() -> dict[str, int]:
    """Return record counts for the four captured axes."""
    return {
        "sites": len(SITES),
        "escapes": len(ESCAPES),
        "mechanisms": len(MECHANISMS),
        "routes": len(ROUTES),
    }


if __name__ == "__main__":
    c = counts()
    print("canine histiocytic sarcoma — conversation-derived knowledge model")
    print(f"  sites:      {c['sites']}")
    print(f"  escapes:    {c['escapes']}")
    print(f"  mechanisms: {c['mechanisms']}")
    print(f"  routes:     {c['routes']}")
    print(f"  occupied compartments: {[s.name for s in occupied_sites()]}")
