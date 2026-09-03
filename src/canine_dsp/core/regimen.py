"""An object model for combination regimens in which coverage is DERIVED from mechanism position
rather than asserted.

Ported from the histiocytic-sarcoma analysis (`core/regimen.py` on the HS branch) and generalised
for lymphoma with one added mechanic -- DRUG EFFLUX -- because in lymphoma the dominant real
resistance lesion is a pump, not a pathway lesion, and a pump defeats agents by CHEMICAL CLASS
rather than by position on a cascade.

WHY COVERAGE MUST BE DERIVED

If "agent X covers escape Y" is a sentence written by hand, it can be right in one module and wrong
in another. If it is computed from where the agent acts and where the lesion sits, it cannot. The
lymphoma work before this file listed seven escape routes and asserted their closures in prose; this
model recomputes them, and the recomputation is what allows a SEARCH over combinations rather than a
proposal of one.

THE THREE WAYS AN AGENT FAILS AN ESCAPE, ALL DERIVED

  1. POSITION. On a serial axis, signal flows down, so a block covers lesions ABOVE it and is
     defeated by an activating lesion AT or BELOW it. Blocking BTK is defeated by an
     NF-kB-independence lesion below it. So downstream blocking covers more -- the same arithmetic
     the HS analysis found, and it is why "go upstream" is not by itself a coverage argument.
  2. DISPLAY. An ANTIGEN-DIRECTED effector needs the cell to display its target. CD20 loss defeats a
     CD20-directed CAR; it does not defeat doxorubicin, which does not care what the cell displays.
  3. EFFLUX -- the lymphoma addition. A P-glycoprotein or BCRP clone pumps its SUBSTRATES back out.
     That defeats doxorubicin and vincristine and does NOT defeat prednisolone (measured:
     Zandvliet et al. 2014, PMID 24975508), nor an antibody, nor a cell therapy, nor radiation.
     Modelled exactly like the antigen mechanic: a property of the agent meeting a property of the
     escape.

AND THE ONE WAY DELIVERY FAILS IT

Effective kill is potency x access x duty. An agent that covers every escape and reaches 5% of a
sanctuary contributes 5% of its kill. Coverage without delivery is the error that produces
confident-looking regimens that do nothing where the disease actually is.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum


class Layer(IntEnum):
    """Height on a serial signalling cascade. Lower number is further upstream.

    For lymphoma the serial axis of interest is B-cell-receptor signalling:
    BCR -> SYK -> BTK -> PLCg2 -> NF-kB.
    """

    RECEPTOR = 0     # BCR / surface receptor
    SYK = 1
    BTK = 2
    PLCG = 3
    NFKB = 4


class Axis(Enum):
    """Which wire the agent acts on. Serial within an axis, independent across axes."""

    CYTOTOXIC = "DNA damage / mitotic (division-gated)"
    BCR_SIGNAL = "B-cell receptor -> BTK -> NF-kB survival signalling (serial)"
    PI3K_PARALLEL = "PI3K / AKT (parallel survival)"
    APOPTOSIS = "BCL2 / intrinsic apoptosis (position-independent, not division-gated)"
    AUTOPHAGY = "autophagy-lysosome dependence (position-independent, not division-gated)"
    IMMUNE_EFFECTOR = "cytotoxic immune killing"
    LINEAGE = "B-cell lineage identity"
    DELIVERY = "physical delivery (radiation, total body irradiation, local)"
    CELL_CYCLE = "proliferation state (where the persister escape lives)"


#: Axes whose agents act regardless of where a signalling lesion sits.
POSITION_INDEPENDENT = (Axis.IMMUNE_EFFECTOR, Axis.DELIVERY, Axis.APOPTOSIS, Axis.AUTOPHAGY,
                        Axis.CYTOTOXIC, Axis.LINEAGE)


@dataclass(frozen=True)
class Escape:
    """A resistance lesion, located by axis and height, with the properties that defeat agents."""

    name: str
    axis: Axis
    layer: Layer
    seeding_rate: float               # per cell; probability the lesion exists in a given cell
    requires_division: bool = True    # False => a persister: division-gated agents never reach it
    antigen_intact: bool = True       # False => this lesion removes a surface antigen
    removes_antigen: str = ""         # WHICH antigen, e.g. "CD20". An agent is defeated only if
                                      # EVERY antigen it targets is removed -- so a tandem
                                      # CD19/CD20 construct survives losing CD20 alone, and a
                                      # single-antigen CAR does not. Modelling this as one boolean
                                      # made a tandem construct look no better than a single CAR.
    effluxes_substrates: bool = False  # True => agents that are efflux substrates are defeated
    evidence: str = "ASSUMED"
    note: str = ""

    @property
    def is_axis_independence(self) -> bool:
        """True for a GENERIC 'this cell no longer depends on that mechanism' escape -- autophagy
        independence, apoptosis evasion, immune exhaustion.

        Such an escape defeats every agent on its own axis, which is the rule that stops a
        position-independent agent looking universal. It must NOT fire for an escape that already
        carries an explicit, narrower defeat mechanic: drug efflux defeats only its SUBSTRATES (so a
        non-substrate cytotoxic still covers it), and antigen loss defeats only agents targeting
        THAT antigen (so a tandem construct still covers it). Applying the blanket own-axis rule to
        those was a bug that made cyclophosphamide fail against the efflux clone and made a tandem
        CD19/CD20 CAR indistinguishable from a single-antigen one.
        """
        return not self.removes_antigen and not self.effluxes_substrates


@dataclass(frozen=True)
class Agent:
    """A therapy, located by axis and height, and priced by delivery."""

    name: str
    axis: Axis
    layer: Layer
    potency: float                  # unconstrained per-day kill at full exposure
    access: float                   # fraction of systemic exposure reaching this compartment
    duty: float                     # fraction of the interval spent above the effective threshold
    obtainable: bool
    division_gated: bool = True
    antigen_targets: tuple = ()     # e.g. ("CD20",) or ("CD19", "CD20"). Empty => the effector
                                    # does not depend on the tumour DISPLAYING anything, so antigen
                                    # loss cannot defeat it.
    efflux_substrate: bool = False  # True for P-gp/BCRP substrates -- doxorubicin, vincristine.
                                    # False for prednisolone (MEASURED, PMID 24975508), antibodies,
                                    # cell therapies and radiation.
    evidence: str = "ASSUMED"       # strongest real anchor for the MECHANISM
    potency_evidence: str = "ASSUMED"  # separately graded, because a mechanism can be measured in
                                       # this disease while its per-day kill rate is not. Counting
                                       # these honestly is the difference between a result and a
                                       # hypothesis.
    note: str = ""

    @property
    def antigen_directed(self) -> bool:
        return bool(self.antigen_targets)

    @property
    def effective_kill(self) -> float:
        """Potency x access x duty. The only number that can act on a tumour."""
        return self.potency * self.access * self.duty

    def covers(self, escape: Escape) -> bool:
        """Derived from mechanism position and the display/efflux properties. Never asserted."""
        # An antigen-directed effector is defeated only when EVERY antigen it targets is gone.
        # A tandem CD19/CD20 construct therefore survives losing CD20 alone; a single-antigen CAR
        # does not. Representing this as one boolean made the two look identical, which is the
        # false positive this mechanic exists to prevent.
        if self.antigen_targets and not escape.antigen_intact:
            removed = {escape.removes_antigen} if escape.removes_antigen else set(self.antigen_targets)
            if set(self.antigen_targets) <= removed:
                return False
        # An efflux clone defeats exactly the agents that are its substrates.
        if escape.effluxes_substrates and self.efflux_substrate:
            return False
        if self.axis in POSITION_INDEPENDENT:
            # Position-independent agents still do not get a free pass against a GENERIC
            # independence escape on their OWN axis -- losing BCL2 dependence defeats a BCL2
            # inhibitor. But an escape with its own explicit mechanic (efflux, antigen loss) has
            # already been adjudicated above, and must not be re-blocked here.
            if escape.axis is self.axis and escape.is_axis_independence:
                return False
            return True
        if self.axis is not escape.axis:
            return False
        if self.axis in (Axis.BCR_SIGNAL,):
            # serial: a block covers lesions strictly ABOVE it
            return self.layer > escape.layer
        return True

    def reaches(self, escape: Escape) -> bool:
        """Delivery and mechanism both have to hold."""
        if self.effective_kill <= 0.0:
            return False
        if escape.requires_division is False and self.division_gated:
            return False
        return self.covers(escape)


@dataclass
class Regimen:
    name: str
    agents: list = field(default_factory=list)

    @property
    def obtainable(self) -> bool:
        return all(a.obtainable for a in self.agents)

    def effective_kill_against(self, escape: Escape) -> float:
        return sum(a.effective_kill for a in self.agents if a.reaches(escape))

    def uncovered(self, escapes) -> tuple:
        return tuple(e for e in escapes if self.effective_kill_against(e) <= 0.0)

    def margin_against(self, escape: Escape, growth: float) -> float:
        return self.effective_kill_against(escape) - growth

    def closes(self, escapes, growth: float) -> bool:
        return all(self.margin_against(e, growth) > 0.0 for e in escapes)

    def weakest_link(self, escapes, growth: float):
        return min(escapes, key=lambda e: self.margin_against(e, growth))

    def reaches_persisters(self) -> bool:
        return any(not a.division_gated and a.effective_kill > 0.0 for a in self.agents)

    def assumed_inputs(self) -> int:
        """How many agents rest on an ASSUMED POTENCY. A regimen assembled entirely from
        assumptions is a hypothesis, not a result, and the search reports the count.

        Graded on potency specifically, not on the mechanism: nearly every agent here has a real
        mechanistic anchor in this disease while its per-day kill rate is still assumed, and
        conflating the two would let the search look far better evidenced than it is."""
        return sum(1 for a in self.agents if a.potency_evidence == "ASSUMED")


def escape_presence_probability(escape: Escape, tumour_cells: float) -> float:
    """Probability the lesion ALREADY EXISTS at diagnosis, given tumour size.

    This is the quantity early detection actually changes, and the reason "find it earlier" is a
    mechanism argument rather than merely a timing one. A lesion arising at rate `seeding_rate` per
    cell is present with probability 1 - exp(-rate * N). At a clinically obvious burden the common
    lesions are effectively CERTAIN to be present; at an early-detected burden several of them are
    unlikely to have arisen at all -- so early detection does not merely start treatment sooner, it
    reduces the number of escapes the regimen has to close.
    """
    if tumour_cells < 0:
        raise ValueError("tumour_cells must be non-negative")
    import math
    return 1.0 - math.exp(-escape.seeding_rate * tumour_cells)


WHY_COVERAGE_IS_DERIVED = (
    "Coverage written as prose can be right in one module and wrong in another; coverage computed "
    "from where the agent acts and where the lesion sits cannot.",
    "Three derived failure modes: POSITION on a serial axis, DISPLAY for antigen-directed "
    "effectors, and EFFLUX for pump substrates -- the last being the lymphoma-specific one, because "
    "the dominant real resistance lesion in this disease is a pump.",
    "And delivery caps all of it: effective kill is potency x access x duty.",
)
