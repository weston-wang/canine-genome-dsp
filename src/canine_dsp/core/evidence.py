"""A measurement that cannot be separated from the population that produced it.

WHY THIS EXISTS

This project has made the same error at least six times, and it has never been an arithmetic
mistake. Every instance was A NUMBER SEPARATED FROM THE POPULATION THAT PRODUCED IT:

    250 nM        cobimetinib's IC50, used as trametinib's -- and inflated from a mean of 179
    0.15          trametinib's brain:plasma ratio, applied to cobimetinib (whose value is 0.027)
    410 nM        presented as a conservative operating point; it is the Cmax of the canine
                  MINIMUM LETHAL DOSE
    230/690/710   PI3K IC50s from canine HEMANGIOSARCOMA lines, used for histiocytic sarcoma
    0.75 mg/kg    a canine OSTEOSARCOMA regimen, used as a histiocytic sarcoma regimen
    0.37          chlorambucil in bulk enhancing GLIOMA with a disrupted barrier, nearly used as
                  dasatinib's access across an intact one
    xenografts    MOUSE xenografts of canine cells, described as canine efficacy data

Prose dicts cannot prevent this, and tests that assert wording cannot either -- a test pins a
sentence for exactly as long as the sentence is there, true or not. `retraction_registry` catches a
claim AFTER it has been identified as false and only if someone writes a regex for it. That is a
post-hoc check on a class of error that is entirely mechanical and therefore preventable.

WHAT THIS DOES INSTEAD

A `Measurement` carries its provenance as REQUIRED STRUCTURE, not as a comment: the value, the
quantity it measures, and the (species, disease, agent) triple it was measured in. Reading the value
for a different triple raises. There is no code path that yields a bare float without asserting what
population it belongs to.

    ic50 = Measurement(9.0, Quantity.IC50_NM, Population(Species.DOG, Disease.HISTIOCYTIC_SARCOMA,
                                                          agent="dasatinib"), source="PMC5831740")

    ic50.value_for(dog_hs_dasatinib)     ->  9.0
    ic50.value_for(dog_hs_trametinib)    ->  raises ProvenanceError

A number may still be used across a mismatch -- borrowing from a related population is legitimate
science -- but only through `transfer_to()`, which demands an explicit written justification and
marks the result as TRANSFERRED rather than MEASURED. The point is not to forbid the move. It is to
make the move impossible to perform SILENTLY, which is how all six instances above happened.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ProvenanceError(AssertionError):
    """Raised when a measurement is read against a population it was not measured in."""


class Species(Enum):
    DOG = "dog"
    MOUSE = "mouse"
    RAT = "rat"
    HUMAN = "human"
    MONKEY = "monkey"
    IN_VITRO = "in vitro"          # a cell line, species recorded separately on the line
    UNSPECIFIED = "unspecified"


class Disease(Enum):
    HISTIOCYTIC_SARCOMA = "histiocytic sarcoma"
    HISTIOCYTIC_SARCOMA_CNS = "histiocytic sarcoma, CNS"
    HEMANGIOSARCOMA = "hemangiosarcoma"
    OSTEOSARCOMA = "osteosarcoma"
    MELANOMA = "melanoma"
    GLIOMA = "glioma"
    MENINGIOMA = "meningioma"
    LANGERHANS_CELL_HISTIOCYTOSIS = "Langerhans cell histiocytosis"
    ERDHEIM_CHESTER = "Erdheim-Chester disease"
    HEALTHY = "healthy / normal tissue"
    NONE = "not disease-specific"


class Quantity(Enum):
    IC50_NM = "IC50 (nM)"
    CMAX_NM = "Cmax (nM)"
    CTROUGH_NM = "trough concentration (nM)"
    TISSUE_PLASMA_RATIO = "tissue:plasma ratio"
    KILL_RATE_PER_DAY = "kill rate (per day)"
    GROWTH_RATE_PER_DAY = "growth rate (per day)"
    MEDIAN_SURVIVAL_DAYS = "median survival (days)"
    RELAPSE_FREE_FRACTION = "relapse-free fraction"
    MUTATION_FREQUENCY = "mutation frequency"
    HALF_LIFE_H = "half-life (h)"
    DOSE_MG_PER_KG = "dose (mg/kg)"
    DOSE_MG_PER_M2 = "dose (mg/m2)"
    FRACTION_OF_CASES = "fraction of cases"


class BarrierState(Enum):
    """Which barrier a tissue:plasma ratio was measured across.

    Introduced because a measured 0.37 intratumoural:serum ratio in canine glioma was very nearly
    used as evidence of access across an INTACT barrier. The paper's own conclusion was that the
    drug's presence "indicated an ALTERED blood-brain barrier". Those are opposite claims about the
    same number, and nothing in a bare float distinguishes them.
    """

    INTACT = "intact barrier"
    DISRUPTED = "disrupted / enhancing tumour"
    NOT_APPLICABLE = "no barrier"
    UNKNOWN = "unknown"


class Provenance(Enum):
    MEASURED = "measured"
    DERIVED = "derived from measured parameters"
    TRANSFERRED = "transferred from another population"
    ASSUMED = "assumed"
    MODEL_OUTPUT = "model output"


@dataclass(frozen=True)
class Population:
    """The (species, disease, agent) triple a number belongs to.

    `agent` is a plain string rather than an enum because the set of agents is open, and because
    every instance of this project's signature error involved an agent name that WAS known -- the
    failure was never in naming the drug, it was in dropping the name when the number moved.
    """

    species: Species
    disease: Disease
    agent: str | None = None
    barrier: BarrierState = BarrierState.NOT_APPLICABLE
    note: str = ""

    def matches(self, other: "Population") -> bool:
        if self.species is not other.species or self.disease is not other.disease:
            return False
        if self.agent is not None and other.agent is not None and self.agent != other.agent:
            return False
        if BarrierState.UNKNOWN not in (self.barrier, other.barrier) and self.barrier is not other.barrier:
            return False
        return True

    def describe(self) -> str:
        parts = [self.species.value, self.disease.value]
        if self.agent:
            parts.append(self.agent)
        if self.barrier is not BarrierState.NOT_APPLICABLE:
            parts.append(self.barrier.value)
        return ", ".join(parts)


@dataclass(frozen=True)
class Measurement:
    """A number that knows what population it came from, and refuses to be read for another."""

    value: float
    quantity: Quantity
    population: Population
    source: str
    provenance: Provenance = Provenance.MEASURED
    n: int | None = None
    spread: tuple | None = None
    justification: str = ""
    superseded_by: str = ""

    def __post_init__(self):
        if not self.source:
            raise ProvenanceError(
                f"{self.quantity.value} = {self.value} has no source. Every number in this project "
                "carries a citation or it does not exist."
            )
        if self.provenance is Provenance.TRANSFERRED and not self.justification:
            raise ProvenanceError(
                f"{self.quantity.value} = {self.value} is marked TRANSFERRED with no justification. "
                "Borrowing a number across populations is legitimate; doing it silently is the error "
                "this class exists to prevent."
            )

    def value_for(self, population: Population) -> float:
        """The value, if and only if it belongs to this population."""
        if self.superseded_by:
            raise ProvenanceError(
                f"{self.quantity.value} = {self.value} ({self.source}) is SUPERSEDED: "
                f"{self.superseded_by}"
            )
        if not self.population.matches(population):
            raise ProvenanceError(
                f"{self.quantity.value} = {self.value} was measured in "
                f"[{self.population.describe()}] ({self.source}) and is being read for "
                f"[{population.describe()}]. If the transfer is intended, call transfer_to() with a "
                "written justification."
            )
        return self.value

    def transfer_to(self, population: Population, justification: str,
                    scale: float = 1.0) -> "Measurement":
        """Borrow this number for a different population, on the record.

        The justification is mandatory and is carried on the result, so a transferred number is
        never indistinguishable from a measured one downstream.
        """
        if not justification:
            raise ProvenanceError("transfer_to() requires a written justification.")
        return Measurement(
            value=self.value * scale,
            quantity=self.quantity,
            population=population,
            source=f"{self.source} (transferred from {self.population.describe()})",
            provenance=Provenance.TRANSFERRED,
            n=self.n,
            justification=justification,
        )

    def supersede(self, reason: str) -> "Measurement":
        """Mark this number dead. Reading it thereafter raises rather than returning quietly."""
        return Measurement(
            value=self.value, quantity=self.quantity, population=self.population,
            source=self.source, provenance=self.provenance, n=self.n, spread=self.spread,
            justification=self.justification, superseded_by=reason,
        )

    def describe(self) -> str:
        core = f"{self.quantity.value} = {self.value} [{self.population.describe()}]"
        tail = f" -- {self.provenance.value}, {self.source}"
        if self.n:
            tail += f", n={self.n}"
        return core + tail


@dataclass
class Registry:
    """A collection of measurements with a self-check for the errors this project actually made."""

    measurements: list = field(default_factory=list)

    def add(self, m: Measurement) -> Measurement:
        self.measurements.append(m)
        return m

    def for_population(self, population: Population, quantity: Quantity) -> list:
        return [m for m in self.measurements
                if m.quantity is quantity and m.population.matches(population)
                and not m.superseded_by]

    def audit(self) -> dict:
        """Find the shapes of error this project has actually committed."""
        same_quantity_different_agent = []
        cross_species = []
        cross_disease = []
        unsourced = []
        transferred_without_justification = []

        by_quantity: dict = {}
        for m in self.measurements:
            by_quantity.setdefault(m.quantity, []).append(m)

        for quantity, group in by_quantity.items():
            agents = {m.population.agent for m in group if m.population.agent}
            if len(agents) > 1:
                same_quantity_different_agent.append(
                    {"quantity": quantity.value, "agents": sorted(agents),
                     "why_this_is_flagged": "The same quantity is recorded for more than one agent. "
                     "That is normal -- it is flagged so that any code reading one of them for the "
                     "other has to do so through transfer_to()."})

        for m in self.measurements:
            if m.population.species is not Species.DOG and m.provenance is Provenance.MEASURED:
                cross_species.append(m.describe())
            if m.population.disease not in (Disease.HISTIOCYTIC_SARCOMA,
                                            Disease.HISTIOCYTIC_SARCOMA_CNS,
                                            Disease.NONE, Disease.HEALTHY):
                cross_disease.append(m.describe())
            if not m.source:
                unsourced.append(m.describe())
            if m.provenance is Provenance.TRANSFERRED and not m.justification:
                transferred_without_justification.append(m.describe())

        return {
            "total": len(self.measurements),
            "same_quantity_recorded_for_multiple_agents": same_quantity_different_agent,
            "not_measured_in_dogs": cross_species,
            "not_measured_in_histiocytic_sarcoma": cross_disease,
            "unsourced": unsourced,
            "transferred_without_justification": transferred_without_justification,
            "what_this_guarantees": "That no number can be read for a population it was not "
                                    "measured in without an explicit, written transfer. It does NOT "
                                    "verify that any measurement is correct -- only that it cannot "
                                    "silently migrate to the wrong drug, species or disease.",
        }
