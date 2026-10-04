"""Does the oral arm actually get into the brain? Checking it catches three errors, two of them mine.

WHY THE CHECK WAS NEEDED

`core.dormancy` established that the persister escape is a DUTY-CYCLE problem: a continuously present
division-gated agent reaches a persister at re-entry, and metronomic oral chemotherapy has duty ~1.0
by construction. That result is right. But it prices only ONE of the three terms, and the identity
has three:

    effective kill = potency x ACCESS x duty

A schedule fixes duty. It says nothing about whether the drug reaches the compartment, and this
project's entire brain problem is an ACCESS problem. Solving the third term while assuming the second
is exactly the error that produced most of the retracted headlines here.

ERROR 1, MINE: I APPLIED THE EFFLUX MULTIPLIER TO LOMUSTINE. IT IS NOT A P-gp SUBSTRATE.

The metronomic computation ran lomustine through `EFFLUX_INHIBITION.apply()`, giving it the measured
20x access boost. But `therapies.nitrosoureas` -- a module in this same repository -- records the
opposite, with a citation:

    Radtke 2022 (PMID 36252775): ABCB1 knockout altered response to temozolomide and carmustine
    but NOT to lomustine.
    Halsey 2014 (PMID 24885200): toceranib-resistant CANINE sublines retained lomustine
    sensitivity, with minimal and non-functional P-gp.

A P-gp inhibitor does nothing for a drug the pump does not carry. THE 20x DOES NOT APPLY, and
removing it costs the metronomic arm a factor of twenty at the parenchyma.

The irony is exact: lomustine's NOT being an efflux substrate was recorded in this project as a point
in its FAVOUR -- "the efflux term that foreclosed the kinase inhibitors does not apply here". It is
the same fact, and under efflux inhibition it becomes a point against, because there is nothing to
un-pump.

ERROR 2, ALSO MINE, AND OLDER: LOMUSTINE'S CANINE CNS ACCESS HAS NEVER BEEN MEASURED.

`therapies.nitrosoureas` states it flatly: "CANINE BRAIN OR INTRATUMOURAL CONCENTRATION: DOES NOT
EXIST, at any dose." The one dog datum is Oliverio 1970 (PMID 4987693), CSF radioactivity ~3x plasma
-- and it is TOTAL RADIOACTIVITY, NOT PARENT DRUG, in a compound that decomposes within minutes, and
CSF is not brain. The commonly quoted "CSF 15-30% of plasma" is a class-level review assertion with
no traceable primary measurement.

So the metronomic arm's access term is not merely uncertain. IT IS THE SAME UNMEASURED QUANTITY THAT
THIS PROJECT HAS SPENT ITS ENTIRE HISTORY BEING WRONG ABOUT.

ERROR 3, WHICH IS NOT A MISTAKE BUT AN UNPRICED TRADE: METRONOMIC DOSING BUYS DUTY BY SELLING PEAK.

    standard canine lomustine     60-90 mg/m2 every 3-4 weeks    ~75 mg/m2 per 28-day cycle
    metronomic canine lomustine   2.84 mg/m2/day                 ~79.5 mg/m2 per 28 days

TOTAL EXPOSURE IS ESSENTIALLY IDENTICAL -- within about 6%. What changes is the shape: the peak falls
by roughly TWENTY-SIX FOLD. Metronomic dosing does not add drug. It redistributes the same drug from
a spike into a plateau.

That redistribution is unambiguously good for the persister, which needs PRESENCE at an unpredictable
re-entry moment. It is NOT unambiguously good behind a barrier, and here is the failure mode:

    if a threshold concentration T must be exceeded for any kill at all, then
        standard pulse works when     75 x access  > T
        metronomic works when       2.84 x access  > T

    THERE IS A BAND OF ACCESS VALUES -- A FACTOR OF 26 WIDE -- IN WHICH THE PULSE CLEARS THRESHOLD
    AND THE PLATEAU NEVER DOES.

Behind a barrier that admits ~2% of plasma, that band is exactly where this tumour might sit. And
the direction of the error is the dangerous one: metronomic dosing would convert "briefly above
threshold" into "continuously below it", while LOOKING better on the duty-cycle term the model
rewards.

WHAT SURVIVES THE CHECK

The DORMANCY CORRECTION survives completely. It is a statement about how a persister must be priced,
not about any particular drug, and it holds for any continuously present agent -- including the ones
whose access IS measured or at least argued.

WHAT DOES NOT SURVIVE is the specific claim that METRONOMIC LOMUSTINE is the obtainable answer to the
persister at the BRAIN. It fails the access check three ways: the efflux boost does not apply to it,
its canine CNS concentration has never been measured at any dose, and metronomic dosing may push it
below threshold precisely where the barrier is tightest.

IT REMAINS A REASONABLE ARM AT THE LEPTOMENINGES, where access is less hostile, and it remains the
standard-of-care agent for this disease systemically. It is not the brain answer.

AND THE AGENT THAT DOES SURVIVE THE CHECK IS ALREADY IN THE REGIMEN

Of the continuously dosed agents here, the ones whose brain access has an argument behind it are the
small molecules that ARE efflux substrates -- because for those the 20x is a measured, applicable
multiplier rather than a borrowed one. That is parthenolide and the statin. Both are already in the
revised regimen for other reasons, and both are continuous, so both carry the duty-cycle property the
dormancy correction rewards.

The persister is still closed. It is closed by agents already present, not by adding lomustine.
"""

from __future__ import annotations

THE_IDENTITY_HAS_THREE_TERMS = (
    "effective kill = potency x ACCESS x duty",
    "A SCHEDULE FIXES DUTY. It says nothing about whether the drug reaches the compartment, and this "
    "project's entire brain problem is an ACCESS problem.",
    "Solving the third term while assuming the second is exactly the error that produced most of the "
    "retracted headlines here.",
)

ERROR_1_THE_EFFLUX_BOOST_DOES_NOT_APPLY = {
    "what_I_did": "Ran metronomic lomustine through EFFLUX_INHIBITION.apply(), giving it the "
                  "measured 20x access boost.",
    "why_it_is_wrong": "LOMUSTINE IS NOT A MEANINGFUL P-gp SUBSTRATE. Radtke 2022 (PMID 36252775): "
        "ABCB1 knockout altered response to temozolomide and carmustine but NOT to lomustine. "
        "Halsey 2014 (PMID 24885200): toceranib-resistant CANINE sublines retained lomustine "
        "sensitivity with minimal and non-functional P-gp. A P-gp inhibitor does nothing for a drug "
        "the pump does not carry.",
    "cost": "A factor of twenty at the parenchyma.",
    "THE_IRONY_IS_EXACT": "Lomustine's NOT being an efflux substrate was recorded in this project as "
        "a point IN ITS FAVOUR -- 'the efflux term that foreclosed the kinase inhibitors does not "
        "apply here'. Same fact. Under efflux inhibition it becomes a point AGAINST, because there "
        "is nothing to un-pump.",
}

ERROR_2_THE_ACCESS_HAS_NEVER_BEEN_MEASURED = {
    "the_repo_already_said_so": "`therapies.nitrosoureas`: CANINE BRAIN OR INTRATUMOURAL "
                                "CONCENTRATION -- DOES NOT EXIST, at any dose.",
    "the_one_dog_datum": "Oliverio 1970 (PMID 4987693), CSF radioactivity ~3x plasma -- TOTAL "
        "RADIOACTIVITY, NOT PARENT DRUG, in a compound that decomposes within minutes. CSF is also "
        "not brain.",
    "the_textbook_figure": "'CSF 15-30% of plasma' is a class-level review assertion with no "
                           "traceable primary measurement.",
    "SO": "The metronomic arm's access term is not merely uncertain. IT IS THE SAME UNMEASURED "
          "QUANTITY THIS PROJECT HAS SPENT ITS ENTIRE HISTORY BEING WRONG ABOUT.",
}

# mg/m2
STANDARD_PER_CYCLE = 75.0        # 60-90 mg/m2 every 3-4 weeks
METRONOMIC_PER_DAY = 2.84        # canine metronomic lomustine protocol
CYCLE_DAYS = 28


def total_exposure_ratio() -> float:
    """Metronomic total dose over a cycle, against a standard pulse. ~1.0 -- the same drug."""
    return (METRONOMIC_PER_DAY * CYCLE_DAYS) / STANDARD_PER_CYCLE


def peak_ratio() -> float:
    """How far the peak falls. This is what metronomic dosing actually trades away."""
    return STANDARD_PER_CYCLE / METRONOMIC_PER_DAY


ERROR_3_THE_UNPRICED_TRADE = {
    "what_metronomic_does": "It does not add drug. IT REDISTRIBUTES THE SAME DRUG from a spike into "
                            "a plateau -- total exposure is identical within about 6%.",
    "what_it_costs": f"The peak falls by roughly {peak_ratio():.0f}-fold.",
    "good_for_the_persister": "A persister needs PRESENCE at an unpredictable re-entry moment, so "
                              "the plateau is unambiguously better for it.",
    "THE_FAILURE_MODE_BEHIND_A_BARRIER": "If a threshold concentration T must be exceeded for any "
        "kill, the standard pulse works when 75 x access > T and the plateau when 2.84 x access > T. "
        "THERE IS A BAND OF ACCESS VALUES, A FACTOR OF 26 WIDE, IN WHICH THE PULSE CLEARS THRESHOLD "
        "AND THE PLATEAU NEVER DOES.",
    "and_the_direction_is_the_dangerous_one": "Behind a barrier admitting ~2% of plasma, that band "
        "is exactly where this tumour might sit -- and metronomic dosing would convert 'briefly "
        "above threshold' into 'continuously below it' WHILE LOOKING BETTER on the duty-cycle term "
        "the model rewards.",
}

WHAT_SURVIVES = (
    "THE DORMANCY CORRECTION SURVIVES COMPLETELY. It is a statement about how a persister must be "
    "priced, not about any particular drug, and it holds for any continuously present agent.",
    "WHAT DOES NOT SURVIVE is the specific claim that METRONOMIC LOMUSTINE is the obtainable answer "
    "to the persister AT THE BRAIN. It fails the access check three ways: the efflux boost does not "
    "apply, its canine CNS concentration has never been measured at any dose, and metronomic dosing "
    "may push it below threshold precisely where the barrier is tightest.",
    "It remains a reasonable arm AT THE LEPTOMENINGES, where access is less hostile, and the "
    "standard-of-care agent for this disease systemically. IT IS NOT THE BRAIN ANSWER.",
)

AND_THE_PERSISTER_IS_STILL_CLOSED = (
    "Of the continuously dosed agents here, the ones whose brain access has an argument behind it "
    "are the small molecules that ARE efflux substrates -- because for those the 20x is a measured, "
    "applicable multiplier rather than a borrowed one. That is PARTHENOLIDE and the STATIN.",
    "Both are already in the revised regimen for other reasons, and both are continuous, so both "
    "carry the duty-cycle property the dormancy correction rewards.",
    "THE PERSISTER IS STILL CLOSED. It is closed by agents already present, not by adding lomustine.",
)
