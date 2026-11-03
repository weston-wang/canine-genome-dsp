"""An object model for combination regimens, in which coverage is DERIVED from pathway position
rather than asserted.

WHY COVERAGE MUST BE DERIVED

Throughout this project, "agent X covers escape Y" was written down by hand, module by module. That
is how the same route came to be CLOSED in one enumeration and MOOT in another, and how "abemaciclib
covers CSF1R escape unconditionally" survived long enough to need a formal retraction. If coverage is
a sentence, it can be wrong in one place and right in another. If it is computed from where the agent
acts and where the lesion sits, it cannot.

THE RULE, AND IT RUNS THE OPPOSITE WAY FROM THE INTUITION ABOUT "UPSTREAM"

Signal flows down a serial cascade. A block at a node stops everything that must pass THROUGH that
node -- so a block covers lesions ABOVE it and is defeated by activating lesions AT or BELOW it.

    CSF1R -> SHP2 -> RAS -> RAF -> MEK -> ERK

    Blocking MEK is defeated by an activating ERK lesion, and covers a RAS lesion.
    Blocking ERK is defeated by almost nothing on this axis, and covers everything above it.

SO ON A SERIAL AXIS, DOWNSTREAM BLOCKING COVERS MORE. That is the arithmetic reason this project
converged on ERK as the convergence node, and it is why "go upstream" is not, by itself, a coverage
argument. Stated plainly because the instinct is strong and the arithmetic disagrees with it.

THEN WHY GO UPSTREAM AT ALL? BECAUSE COVERAGE IS NOT THE ONLY THING THAT MATTERS, AND CSF1R IS NOT
ON THIS AXIS IN THE WAY THE OTHERS ARE.

Three separate arguments survive, and the model represents each:

  1. LINEAGE SURVIVAL IS A DIFFERENT AXIS. CSF1R in a histiocytic tumour is not merely the top of the
     MAPK cascade -- it supplies MAPK-INDEPENDENT survival signalling to a cell whose identity is
     defined by that receptor. Blocking it is not a serial block that can be bypassed downstream; it
     removes a survival input. In the model this is `Axis.LINEAGE_SURVIVAL`, and MAPK lesions do not
     confer resistance to it. That is the honest upstream argument, and it is a lineage argument
     rather than a pathway one.
  2. THE CONVERGENCE NODE IS A SINGLE POINT OF FAILURE. Blocking ERK covers every upstream lesion at
     the cost that ONE activating ERK lesion escapes the whole arm at a SINGLE-HIT rate, rather than
     needing two independent events. Maximal coverage and minimal redundancy are the same property.
  3. VERTICAL PAIRS RAISE THE SEEDING EXPONENT. Two blocks on one axis at different heights require a
     clone to solve both, which is a double-hit. The model prices this by seeding rate, not by
     coverage.

WHAT THE MODEL DELIBERATELY WILL NOT DO

It will not let an agent's coverage exceed its DELIVERY. Every agent carries an access term and a
duty cycle, and effective kill is their product with potency. An agent that covers every escape and
reaches 2% of the compartment contributes 2% of its kill. Coverage without delivery is the error
that produced most of this project's retracted headlines.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum


class Layer(IntEnum):
    """Height on the serial MAPK cascade. Lower number is further upstream."""

    RECEPTOR = 0     # CSF1R
    ADAPTOR = 1      # SHP2 / PTPN11
    RAS = 2
    RAF = 3
    MEK = 4
    ERK = 5


class Axis(Enum):
    """Which wire the agent acts on. Serial within an axis, independent across axes."""

    MAPK_SERIAL = "MAPK cascade (serial)"
    PI3K_PARALLEL = "PI3K / AKT (parallel survival)"
    CELL_CYCLE = "cyclin D - CDK4/6 - RB (parallel)"
    LINEAGE_SURVIVAL = "CSF1R lineage survival (MAPK-independent)"
    IMMUNE_EFFECTOR = "cytotoxic immune killing"
    SURVIVAL_SIGNAL = "NF-kB survival signalling (position-independent, not division-gated)"
    FERROPTOSIS = "lipid-peroxide / GPX4 axis (position-independent, not division-gated)"
    AUTOPHAGY = "autophagy-lysosome dependence (position-independent, not division-gated)"
    CYTOTOXIC = "DNA damage / mitotic (division-gated)"
    DELIVERY = "physical delivery (radiation, local)"


@dataclass(frozen=True)
class Escape:
    """A resistance lesion, located by axis and height."""

    name: str
    axis: Axis
    layer: Layer
    seeding_rate: float          # per cell-day
    requires_division: bool = True
    antigen_intact: bool = True
    note: str = ""


@dataclass(frozen=True)
class Agent:
    """A therapy, located by axis and height, and priced by delivery."""

    name: str
    axis: Axis
    layer: Layer
    potency: float               # unconstrained kill rate per day at full exposure
    access: float                # fraction of systemic concentration reaching the compartment
    duty: float                  # fraction of the interval spent above the effective threshold
    obtainable: bool
    division_gated: bool = True
    antigen_directed: bool = False  # True ONLY for agents whose effector step requires the tumour
                                    # to DISPLAY something -- a T-cell response, a vaccine, an
                                    # antigen-targeted antibody. Everything else (chemotherapy,
                                    # kinase inhibitors, radiation, innate effectors) is indifferent
                                    # to what the cell displays.
                                    #
                                    # THIS DEFAULT WAS ORIGINALLY True, WHICH WAS A BUG: it made
                                    # LOMUSTINE fail against antigen loss. A DNA-damaging agent does
                                    # not care what the cell displays. The old default silently
                                    # applied an immune-effector property to every unannotated
                                    # agent, and the flat rows it produced in an access sweep are
                                    # what exposed it.
    note: str = ""

    @property
    def effective_kill(self) -> float:
        """Potency x access x duty. The only number that can act on a tumour."""
        return self.potency * self.access * self.duty

    def covers(self, escape: Escape) -> bool:
        """Derived, not asserted.

        On a SERIAL axis a block covers lesions strictly ABOVE it and is defeated by lesions at or
        below. Across axes there is no interaction unless the escape is explicitly on that axis.
        An immune or delivery agent is indifferent to pathway position entirely.
        """
        if self.axis in (Axis.IMMUNE_EFFECTOR, Axis.DELIVERY, Axis.SURVIVAL_SIGNAL,
                         Axis.FERROPTOSIS, Axis.AUTOPHAGY, Axis.CYTOTOXIC):
            # CYTOTOXIC belongs here: a DNA-damaging agent does not care which signalling lesion
            # the cell carries. Excluding it was an artefact that made metronomic chemotherapy look
            # useless against every pathway escape.
            # These do not care where the lesion sits. Only an ANTIGEN-DIRECTED effector is defeated
            # by antigen loss -- an innate or lineage-directed one is not, which is precisely why a
            # lineage target is worth having.
            if self.antigen_directed and not escape.antigen_intact:
                return False
            # A survival-signal blocker is position-independent but NOT immune to an escape on its
            # own axis. Removing NF-kB dependence defeats it exactly as CSF1R-independence defeats a
            # CSF1R inhibitor, and the model must not hand it a free pass the others do not get.
            if self.axis in (Axis.SURVIVAL_SIGNAL, Axis.FERROPTOSIS,
                             Axis.AUTOPHAGY) and escape.axis is self.axis:
                return False
            return True
        if self.axis is not escape.axis:
            return False
        if self.axis is Axis.MAPK_SERIAL:
            return self.layer > escape.layer
        # On a non-serial axis, acting on that axis at all defeats a lesion on it.
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
        """Kill minus growth. Positive means the clone shrinks."""
        return self.effective_kill_against(escape) - growth

    def closes(self, escapes, growth: float) -> bool:
        return all(self.margin_against(e, growth) > 0.0 for e in escapes)

    def weakest_link(self, escapes, growth: float):
        return min(escapes, key=lambda e: self.margin_against(e, growth))

    def vertical_pairs(self) -> tuple:
        """Pairs of agents blocking the same serial axis at different heights.

        A clone must solve BOTH to escape, which is a double-hit rather than a single-hit event.
        This is the mechanism by which upstream blocking earns its place -- not through coverage,
        but through the seeding exponent.
        """
        serial = [a for a in self.agents if a.axis is Axis.MAPK_SERIAL]
        return tuple((a.name, b.name) for i, a in enumerate(serial)
                     for b in serial[i + 1:] if a.layer != b.layer)

    def axes_covered(self) -> set:
        return {a.axis for a in self.agents}

    def reaches_persisters(self) -> bool:
        """Only a non-division-gated agent reaches a cell that has stopped dividing."""
        return any(not a.division_gated and a.effective_kill > 0.0 for a in self.agents)


WHY_UPSTREAM_IS_NOT_A_COVERAGE_ARGUMENT = (
    "Signal flows DOWN a serial cascade, so a block covers lesions ABOVE it and is defeated by "
    "activating lesions AT or BELOW it. Blocking MEK is defeated by an activating ERK lesion and "
    "covers a RAS lesion; blocking ERK covers everything above it.",
    "SO ON A SERIAL AXIS, DOWNSTREAM BLOCKING COVERS MORE. That is the arithmetic reason this "
    "project converged on ERK, and it is why 'go upstream' is not by itself a coverage argument.",
)

WHY_UPSTREAM_STILL_EARNS_ITS_PLACE = (
    "LINEAGE SURVIVAL IS A DIFFERENT AXIS. CSF1R in a histiocytic tumour is not merely the top of "
    "the MAPK cascade -- it supplies MAPK-INDEPENDENT survival signalling to a cell whose identity "
    "is defined by that receptor. Blocking it removes a survival input rather than interrupting a "
    "wire that can be rejoined downstream. THAT IS A LINEAGE ARGUMENT, NOT A PATHWAY ONE.",
    "THE CONVERGENCE NODE IS A SINGLE POINT OF FAILURE. Blocking ERK covers every upstream lesion "
    "at the cost that ONE activating ERK lesion escapes the whole arm at a SINGLE-HIT rate. Maximal "
    "coverage and minimal redundancy are the same property.",
    "VERTICAL PAIRS RAISE THE SEEDING EXPONENT. Two blocks on one axis at different heights force a "
    "clone to solve both -- a double-hit. The model prices this by SEEDING RATE, not by coverage.",
)

WHAT_THE_MODEL_WILL_NOT_DO = (
    "Let an agent's coverage exceed its DELIVERY. Effective kill is potency x access x duty. An "
    "agent that covers every escape and reaches 2% of the compartment contributes 2% of its kill.",
    "COVERAGE WITHOUT DELIVERY is the error that produced most of this project's retracted "
    "headlines.",
)
