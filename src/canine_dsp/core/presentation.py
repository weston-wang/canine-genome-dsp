"""The disease this project is actually about, as measured -- not as it has repeatedly been assumed.

WHY THIS MODULE IS THE ANCHOR

Every wrong turn in this project traces back to modelling a disease that is not this one. The this breed
presentation has been described, at various points, as focal, solitary, subdural, discrete,
resectable, extra-axial and outside the blood-brain barrier. The primary literature says none of
those things about the tumour-brain interface, and the one series weighted most heavily toward this
breed says the opposite in every case it examined.

So the presentation is defined ONCE, here, from measured sources, and everything else in the
restructured package reads it from here rather than restating it.

WHAT THE MEASURED LITERATURE SAYS

    Thongtharb 2016 (PMID 26668164, PMC4873849) -- 23 primary intracranial HS, 11 of them the
    predisposed breed, the most breed-weighted histopathology series available:
        "brain masses of all cases were poorly demarcated and invading to the brain parenchyma"
    23 of 23. No exceptions.

    Mariani 2015 (PMID 25711602, PMC4895499) -- 19 dogs, CNS HS, dogs of this breed overrepresented:
        "Mass lesions were unencapsulated, with compression and frequent invasion of adjacent brain
         or spinal cord parenchyma."
        "One striking observation was diffuse, marked enhancement of the meninges, EVEN WHEN THERE
         APPEARED TO BE A SOLITARY, WELL-DEFINED MASS LESION."
        Meningeal enhancement in 19/19. CSF pleocytosis in every dog sampled -- mean 1509 cells/uL
        against a reference below 5.
        "Dissemination of HS through the subarachnoid space occurs more commonly than with most
         other neoplasms."

    Toyoda 2020 (PMC7096655) -- n=102:
        "In the absence of a defined intracranial subdural space, both primary and disseminated HS
         involve both the meninges and the brain parenchyma."
        The authors deny that the compartment this project was relying on exists.

    Wada 2017 (PMID 28335080) -- imaging, solitary intracranial HS vs meningioma:
        "all cases of intracranial histiocytic sarcoma showed leptomeningeal enhancement and/or mass
         formation invading into the sulci"

    Ide 2011 (PMID 21217043) -- 15 dogs, subdural HS, THE PREDISPOSED BREED 47%:
        12/15 focal solitary subdural cerebral masses, 2/15 diffuse leptomeningeal.
        CRITICAL SCOPE NOTE: this is a LOCATION descriptor. The abstract contains NO description of
        the tumour-brain interface. This project read "focal solitary subdural" as "discrete,
        peelable, resectable, outside the barrier". The paper does not say that, and the three
        series above say the opposite.

WHAT FOLLOWS, AND IT REMOVES THE ONLY FAVOURABLE COMPARTMENT

A this breed PIHS does not occupy a resectable extra-axial compartment with meningeal blood supply
outside the blood-brain barrier. It occupies, simultaneously and from presentation:

    INVADED PARENCHYMA      behind an intact barrier, supplied by pial and cortical vessels
    LEPTOMENINGES / CSF     enhancing in 19/19 dogs, pleocytosis in all sampled

SURGERY REMOVES THE BULK AND LEAVES BOTH OF THESE. That is the entire problem stated once: the
operation removes the compartment where drugs reach and leaves the compartments where they do not.

AND THE FAVOURABLE ACCESS NUMBER WAS NEVER MEASURED ANYWHERE

No brain:plasma or tumour:plasma drug concentration measurement exists for any canine EXTRA-AXIAL
brain tumour -- not meningioma, not subdural HS. The only canine intracranial intratumoural
measurement is in GLIOMA. So the 0.70 extra-axial access figure that made a single agent look
sufficient was not merely optimistic; it had no measurement behind it in any canine extra-axial
tumour, and it describes a compartment this tumour does not stay inside.

WHAT THIS MODULE DELIBERATELY DOES NOT DO

It does not claim the disease is hopeless, and it does not choose a therapy. It fixes the target so
that a therapy is evaluated against the tumour that exists. The one published long survivor in
canine primary intracranial HS (Hidari 2025, PMID 39761568 -- resection plus low-dose lomustine,
359 days) is recorded in the therapy modules, not here.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .evidence import (BarrierState, Disease, Measurement, Population, Provenance, Quantity,
                       Species)

BREED_PIHS = Population(
    species=Species.DOG,
    disease=Disease.HISTIOCYTIC_SARCOMA_CNS,
    note="predisposed dog breed, primary intracranial histiocytic sarcoma",
)


class Compartment(Enum):
    """Where disease sits, cut on drug ACCESS rather than on anatomy-crossed-with-antigen.

    The previous partition was {lung, brain} x {antigen present, antigen lost}. Testing it showed
    the antigen axis moves the answer by 0.000 at every site this disease occupies, while the site
    axis moves it by 0.767 -- and the whole of that 0.767 lived INSIDE the single cell called
    "brain". See `v3.the_partition_is_on_the_wrong_axis`.
    """

    EXTRACRANIAL = "extracranial / lung"
    EXTRA_AXIAL = "extra-axial / subdural"
    INVADED_PARENCHYMA = "invaded parenchyma, intact barrier"
    LEPTOMENINGEAL = "leptomeningeal / CSF"


# --- the measured record ------------------------------------------------------------------------

PARENCHYMAL_INVASION = Measurement(
    value=23 / 23,
    quantity=Quantity.FRACTION_OF_CASES,
    population=Population(Species.DOG, Disease.HISTIOCYTIC_SARCOMA_CNS,
                          note="23 primary intracranial HS, 11 dogs of the predisposed breed"),
    source="Thongtharb 2016, PMID 26668164, PMC4873849 -- 'brain masses of all cases were poorly "
           "demarcated and invading to the brain parenchyma'",
    n=23,
)

MENINGEAL_ENHANCEMENT = Measurement(
    value=19 / 19,
    quantity=Quantity.FRACTION_OF_CASES,
    population=Population(Species.DOG, Disease.HISTIOCYTIC_SARCOMA_CNS,
                          note="19 dogs, CNS HS, dogs of this breed overrepresented"),
    source="Mariani 2015, PMID 25711602, PMC4895499 -- meningeal enhancement in all dogs, 'often "
           "profound and remote from the primary mass lesion', and present 'even when there "
           "appeared to be a solitary, well-defined mass lesion'",
    n=19,
)

CSF_PLEOCYTOSIS = Measurement(
    value=1.0,
    quantity=Quantity.FRACTION_OF_CASES,
    population=Population(Species.DOG, Disease.HISTIOCYTIC_SARCOMA_CNS),
    source="Mariani 2015, PMC4895499 -- pleocytosis in every dog with CSF evaluation; mean 1509 "
           "cells/uL, median 254.5, range 10-8000, against a reference below 5",
)

BREED_FRACTION_OF_SUBDURAL_HS = Measurement(
    value=0.47,
    quantity=Quantity.FRACTION_OF_CASES,
    population=Population(Species.DOG, Disease.HISTIOCYTIC_SARCOMA_CNS,
                          note="15 dogs with subdural HS"),
    source="Ide 2011, PMID 21217043",
    n=15,
)

MEDIAN_SURVIVAL_DEFINITIVE = Measurement(
    value=44,
    quantity=Quantity.MEDIAN_SURVIVAL_DAYS,
    population=Population(Species.DOG, Disease.HISTIOCYTIC_SARCOMA_CNS),
    source="Toyoda 2020, PMC7096655, n=102 -- definitive therapy, 95% CI 17-97",
    n=102,
)

MEDIAN_SURVIVAL_PALLIATIVE = Measurement(
    value=5,
    quantity=Quantity.MEDIAN_SURVIVAL_DAYS,
    population=Population(Species.DOG, Disease.HISTIOCYTIC_SARCOMA_CNS),
    source="Toyoda 2020, PMC7096655 -- palliative, 95% CI 3-22",
    n=102,
)

# The one access figure that exists for a canine intracranial tumour, and it is the wrong tumour,
# the wrong drug and the wrong barrier state. Recorded so that reading it for this disease raises.
CHLORAMBUCIL_NORMAL_BRAIN = Measurement(
    value=0.021,
    quantity=Quantity.TISSUE_PLASMA_RATIO,
    population=Population(Species.RAT, Disease.HEALTHY, agent="chlorambucil",
                          barrier=BarrierState.INTACT),
    source="PMC6128565 -- 'poor penetration of the BBB'",
)

CHLORAMBUCIL_GLIOMA_INTRATUMOURAL = Measurement(
    value=0.37,
    quantity=Quantity.TISSUE_PLASMA_RATIO,
    population=Population(Species.DOG, Disease.GLIOMA, agent="chlorambucil",
                          barrier=BarrierState.DISRUPTED),
    source="Bentley RT, Thomovsky SA, Miller MA, Knapp DW, Cohen-Gadol AA. World Neurosurgery "
           "2018;116:e534-e542, PMID 29775768 -- range 0-178%; the authors conclude the drug's "
           "presence 'indicated an ALTERED blood-brain barrier that varied from case to case'",
    n=8,
)

EXTRA_AXIAL_ACCESS_HAS_NEVER_BEEN_MEASURED = (
    "No brain:plasma or tumour:plasma drug concentration measurement exists for any canine "
    "EXTRA-AXIAL brain tumour -- not meningioma, not subdural histiocytic sarcoma. The only canine "
    "intracranial intratumoural measurement is in GLIOMA.",
    "So the 0.70 extra-axial access figure that made a single agent look sufficient had no "
    "measurement behind it in any canine extra-axial tumour, and it describes a compartment this "
    "tumour does not stay inside.",
)


@dataclass(frozen=True)
class CompartmentOccupancy:
    """Whether this disease occupies a compartment, and on what evidence."""

    compartment: Compartment
    occupied: bool
    fraction: Measurement | None
    access: Measurement | None
    access_provenance: Provenance
    what_surgery_does: str
    note: str


OCCUPANCY = (
    CompartmentOccupancy(
        compartment=Compartment.EXTRACRANIAL,
        occupied=False,
        fraction=None,
        access=None,
        access_provenance=Provenance.ASSUMED,
        what_surgery_does="not applicable",
        note="Dogs of this breed do get a localised PULMONARY HS variant (Nakamura 2015), but that is a "
             "different presentation. It is not this dog's intracranial disease, and 4 of 19 in "
             "Mariani were part of a disseminated multiorgan process at diagnosis.",
    ),
    CompartmentOccupancy(
        compartment=Compartment.EXTRA_AXIAL,
        occupied=False,
        fraction=None,
        access=None,
        access_provenance=Provenance.ASSUMED,
        note="THE COMPARTMENT THIS PROJECT RELIED ON DOES NOT EXIST FOR THIS TUMOUR. Toyoda 2020: "
             "'In the absence of a defined intracranial subdural space...'. Thongtharb 2016: all "
             "23 of 23 poorly demarcated and invading parenchyma. Ide 2011's 'focal solitary "
             "subdural' is a LOCATION descriptor whose abstract contains no interface description.",
        what_surgery_does="removes the bulk mass -- which is the part where drugs reached",
    ),
    CompartmentOccupancy(
        compartment=Compartment.INVADED_PARENCHYMA,
        occupied=True,
        fraction=PARENCHYMAL_INVASION,
        access=None,
        access_provenance=Provenance.ASSUMED,
        note="Behind an intact barrier, supplied by pial and cortical vessels. This is where "
             "microscopic residual disease sits after resection, and it is non-enhancing -- so an "
             "enhancing-core access figure describes the tissue that was REMOVED, not the tissue "
             "left behind.",
        what_surgery_does="LEAVES IT",
    ),
    CompartmentOccupancy(
        compartment=Compartment.LEPTOMENINGEAL,
        occupied=True,
        fraction=MENINGEAL_ENHANCEMENT,
        access=None,
        access_provenance=Provenance.ASSUMED,
        note="Enhancing in 19/19 dogs, often remote from the mass and present even when imaging "
             "suggested a solitary lesion; CSF pleocytosis in every dog sampled. This is NOT the "
             "13% minority that 2-of-15 in Ide 2011 was read as.",
        what_surgery_does="does not reach it",
    ),
)


def occupied_compartments() -> tuple:
    return tuple(o.compartment for o in OCCUPANCY if o.occupied)


def the_problem_in_one_line() -> str:
    return ("Surgery removes the compartment where drugs reach and leaves the two compartments "
            "where they do not.")


WHAT_THIS_MODULE_DOES_NOT_DO = (
    "It does not claim the disease is hopeless, and it does not choose a therapy. It fixes the "
    "TARGET so that any therapy is evaluated against the tumour that exists.",
    "The one published long survivor in canine primary intracranial HS -- Hidari 2025, PMID "
    "39761568, resection plus low-dose lomustine, 359 days with no recurrence on serial MRI -- is "
    "recorded in the therapy modules rather than here.",
)
