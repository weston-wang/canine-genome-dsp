"""The one measured-in-dogs delivery number, and what it closes."""

from __future__ import annotations

import math

from canine_dsp.core import intraarterial_route as ia
from canine_dsp.core.catalogue import LEPTOMENINGEAL, PARENCHYMA, GROWTH_PER_DAY


# --- the measurement -------------------------------------------------------------------------------

def test_the_gains_are_derived_from_the_measured_dog_ranges():
    lo, hi = ia.WITHOUT_DISRUPTION
    dlo, dhi = ia.WITH_DISRUPTION
    assert abs(ia.CONSERVATIVE_GAIN - dlo / hi) < 1e-9
    assert abs(ia.OPTIMISTIC_GAIN - dhi / lo) < 1e-9
    assert ia.CONSERVATIVE_GAIN > 3.0


def test_the_measurement_is_in_dogs_with_tissue_concentrations():
    n = ia.NEUWELT_1981
    assert "SPECIES: DOG" in n["citation"] and "n=33" in n["citation"]
    assert "TISSUE CONCENTRATIONS, IN VIVO, IN THE RIGHT SPECIES" in \
        n["why_it_is_the_strongest_number_here"]
    assert "PMID 6796658" in n["citation"]


def test_it_is_corroborated_by_two_further_canine_studies():
    assert "PMID 6809316" in ia.NEUWELT_1981["corroboration"]
    assert "PMID 24932854" in ia.NEUWELT_1981["corroboration"]


# --- what it closes ----------------------------------------------------------------------------------

def test_without_disruption_it_does_not_close():
    assert not ia.closes(1.0)


def test_the_conservative_measured_gain_closes_at_a_seven_day_doubling():
    assert ia.closes(ia.CONSERVATIVE_GAIN, math.log(2) / 7)


def test_the_recorded_margins_are_reproducible():
    g7 = math.log(2) / 7
    for gain, recorded in ia.RESULT_AT_SEVEN_DAY_DOUBLING.items():
        got = min(ia.worst_margin(c, gain, g7) for c in (PARENCHYMA, LEPTOMENINGEAL))
        assert abs(got - recorded) < 1e-3, gain


def test_it_closes_at_the_slower_assumed_growth_too():
    assert ia.closes(ia.CONSERVATIVE_GAIN, GROWTH_PER_DAY)


def test_margins_do_not_fall_as_disruption_rises():
    g7 = math.log(2) / 7
    values = [min(ia.worst_margin(c, gain, g7) for c in (PARENCHYMA, LEPTOMENINGEAL))
              for gain in sorted(ia.RESULT_AT_SEVEN_DAY_DOUBLING)]
    assert values == sorted(values)


def test_no_agent_in_the_regimen_needs_a_transporter_inhibitor():
    for comp in (PARENCHYMA, LEPTOMENINGEAL):
        for a in ia.build(comp, ia.CONSERVATIVE_GAIN).agents:
            assert "P-gp" not in a.name and "BCRP" not in a.name, a.name


def test_the_two_added_agents_carry_measured_intrinsic_access():
    assert ia.PAXALISIB_KPUU == 0.31
    assert ia.TEMOZOLOMIDE_CSF_PLASMA == 0.20
    r = ia.build(PARENCHYMA, 1.0)
    names = [a.name for a in r.agents]
    assert "temozolomide" in names and "paxalisib" in names


def test_paxalisib_is_recorded_as_a_confirmed_non_substrate():
    r = ia.build(PARENCHYMA, 1.0)
    pax = next(a for a in r.agents if a.name == "paxalisib")
    assert "CONFIRMED NON-SUBSTRATE" in pax.note
    assert "27638506" in pax.note


# --- the species correction ----------------------------------------------------------------------------

def test_the_rodent_is_recorded_as_the_outlier():
    s = ia.THE_SPECIES_CORRECTION
    assert "THE RODENT WAS THE OUTLIER" in s["finding"]
    assert "MORE THAN THREE-FOLD HIGHER THAN MOUSE" in s["finding"]


def test_the_project_is_recorded_as_having_been_too_pessimistic():
    s = ia.THE_SPECIES_CORRECTION
    assert "SYSTEMATICALLY TOO PESSIMISTIC" in s["WHAT_IT_MEANS_HERE"]
    assert "modelled from the species that has the most of it" in s["WHAT_IT_MEANS_HERE"]


def test_the_correction_carries_the_caveat_that_cuts_the_other_way():
    s = ia.THE_SPECIES_CORRECTION
    assert "NOT the blood-CSF barrier" in s["THE_CAVEAT_THAT_CUTS_BACK"]
    assert "partly cancel" in s["THE_CAVEAT_THAT_CUTS_BACK"]


# --- what was rejected, and why ---------------------------------------------------------------------------

def test_marizomib_is_rejected_on_a_negative_phase_three_and_unmonitorable_toxicity():
    r = ia.REJECTED_ON_EVIDENCE["marizomib"]
    assert "PHASE 3 NEGATIVE" in r and "HR 1.04" in r
    assert "ATAXIA AND HALLUCINATION" in r
    assert "indistinguishable from tumour progression" in r


def test_disulfiram_is_rejected_on_a_negative_randomised_trial():
    r = ia.REJECTED_ON_EVIDENCE["disulfiram + copper"]
    assert "RANDOMISED" in r and "NO survival benefit" in r
    assert "PMID 37000452" in r


def test_ang1005_is_the_cleanest_demonstration_that_penetration_is_not_efficacy():
    r = ia.REJECTED_ON_EVIDENCE["ANG1005"]
    assert "86-fold" in r
    assert "THE DELIVERY WORKED AND THE DRUG DID NOT" in r
    assert "BRAIN-PENETRANT IS NOT BRAIN-EFFECTIVE" in r


# --- the honest limits -------------------------------------------------------------------------------------

def test_the_transfer_risk_is_named_as_the_projects_recurring_error():
    joined = " ".join(ia.WHAT_IS_STILL_ASSUMED)
    assert "1981 measurement of METHOTREXATE" in joined
    assert "wrong about exactly that kind of transfer before" in joined
    assert "POSTERIOR FOSSA" in joined


def test_the_cost_is_stated_as_a_different_kind_of_constraint():
    assert "different KIND of constraint" in ia.WHAT_IT_COSTS
    assert "general anaesthesia" in ia.WHAT_IT_COSTS


# --- toxicity, which was originally not priced at all --------------------------------------------------

def test_all_three_new_components_now_have_toxicity_profiles():
    from canine_dsp.core.toxicity import profile_for
    for name in ("temozolomide", "paxalisib", "intra-arterial + osmotic disruption"):
        assert profile_for(name) is not None, name


def test_temozolomide_and_hydroxychloroquine_share_the_marrow_axis():
    from canine_dsp.core.toxicity import Organ, profile_for
    assert profile_for("temozolomide").axis is Organ.MARROW
    assert profile_for("hydroxychloroquine").axis is Organ.MARROW
    combined = (profile_for("temozolomide").budget_fraction
                + profile_for("hydroxychloroquine").budget_fraction)
    assert abs(combined - 1.00) < 1e-9, "the collision is exact, and that is the point"


def test_paxalisib_toxicity_is_recorded_as_on_target_not_a_surprise():
    from canine_dsp.core.toxicity import profile_for
    p = profile_for("paxalisib")
    assert "HYPERGLYCAEMIA" in p.dose_limiting_event
    assert "ON-TARGET" in p.dose_limiting_event


def test_the_procedure_itself_carries_a_toxicity_profile():
    from canine_dsp.core.toxicity import profile_for
    p = profile_for("intra-arterial + osmotic disruption")
    assert "SEIZURES" in p.dose_limiting_event
    assert "anaesthesia" in p.dose_limiting_event


def test_the_regimen_without_radiation_is_tolerable_with_real_headroom():
    from canine_dsp.core import tolerable_search as ts
    from canine_dsp.core.toxicity import Organ, PROFILES, ToxicityProfile
    saved_ia = PROFILES["intra-arterial + osmotic disruption"]
    saved_tmz = PROFILES["temozolomide"]
    try:
        PROFILES["intra-arterial + osmotic disruption"] = ToxicityProfile(
            Organ.CNS_LOCAL, 0.30, True, saved_ia.dose_limiting_event, source=saved_ia.source)
        PROFILES["temozolomide"] = ToxicityProfile(
            Organ.MARROW, 0.55 / 3, True, saved_tmz.dose_limiting_event, source=saved_tmz.source)
        r = ts.regimen_toxicity(["liposomal clodronate", "hydroxychloroquine", "anti-PD-1",
                                 "temozolomide", "paxalisib",
                                 "intra-arterial + osmotic disruption"])
        assert r["tolerable"] is True
        assert r["headroom"] > 0.3
    finally:
        PROFILES["intra-arterial + osmotic disruption"] = saved_ia
        PROFILES["temozolomide"] = saved_tmz


def test_the_gap_and_both_collisions_are_recorded():
    assert "TOXICITY WAS NOT PRICED, AND THAT WAS A REAL GAP" in ia.__doc__
    flat = " ".join(ia.__doc__.split())
    assert "EXACTLY 1.00" in flat
    assert "OVERSUBSCRIBED" in flat
    assert "dose-SPARING by construction" in flat
    assert "does not fix the CNS axis" in flat


def test_dropping_radiation_is_recorded_as_removing_an_expired_job():
    flat = " ".join(ia.__doc__.split())
    assert "AND THE FIX IS TO DROP RADIATION" in flat
    assert "an agent is present for a reason that has expired" in flat
