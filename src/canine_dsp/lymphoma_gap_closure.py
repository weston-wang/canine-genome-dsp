"""Closing the potency gap for canine lymphoma: lower the bar, add a second antigen, or consolidate.

Mirrors `hsa_gap_closure` for lymphoma. The immunotherapy achievability analysis leaves a potency
gap: a CD20 effector only reaches durable response at or above the ~0.090/day bar, and no completed
canine trial has measured that a real CD20 CAR-T gets there. This module records the three ways the
gap closes, each recomputed from the engine by tests. See docs/LYMPHOMA_DURABLE_RESPONSE.md.
"""

import numpy as np

DURABILITY_BAR_PER_DAY = 0.0903
SUB_THRESHOLD_IMMUNOTHERAPY_MAX_KILL = 0.06  # a deliberately below-the-bar CD20 effector

# Route A: lower the bar with a persistent, mechanism-agnostic second agent instead of raising the
# immune effector. The bar is growth - kill, so a second persistent kill term clears it from the
# other side. Immunotherapy held at the sub-threshold 0.06/day throughout; 10-year durable response.
# Recomputed by the test module.
LOWER_THE_BAR = {
    0.0:    {"agnostic_kill": 0.0000, "bar_after": 0.0903, "ten_year_durable": 0.240},
    0.02:   {"agnostic_kill": 0.0184, "bar_after": 0.0719, "ten_year_durable": 0.367},
    0.03:   {"agnostic_kill": 0.0275, "bar_after": 0.0628, "ten_year_durable": 0.603},
    0.05:   {"agnostic_kill": 0.0459, "bar_after": 0.0444, "ten_year_durable": 1.000},
}

# The persistent second agent has real candidates. Metronomic chemotherapy (continuous low-dose) is
# the shape that fits -- but note the honest limit: a P-glycoprotein clone effluxes the same drugs,
# so the persistent agent must either use a non-effluxed mechanism or pair with a P-gp inhibitor
# (PSC833 reversed efflux in vitro; Zandvliet et al. 2014, PMID 24975508).
PERSISTENT_AGNOSTIC_CANDIDATE = {
    "requirement": "A kill term that is persistent (not duration-capped) and not itself effluxed by "
                   "the P-glycoprotein clone it is meant to help suppress.",
    "candidates": "metronomic (continuous low-dose) chemotherapy; a non-cross-resistant maintenance "
                  "agent; or a P-gp inhibitor to restore the effluxed drugs' effect.",
    "the_efflux_trap": "Adding more of a P-gp-effluxed cytotoxic (doxorubicin, vincristine) does "
                       "NOT lower the bar for the efflux clone -- that clone is defined by pumping "
                       "exactly those drugs out. The persistent agent has to be chosen to sidestep "
                       "efflux, or the bar does not move for the clone that sets it.",
    "kill_rate_is_swept": "The kill rate the persistent agent supplies is not measured; it is swept "
                          "in LOWER_THE_BAR, not asserted.",
}

# Route B: a one-time high-intensity consolidation (total body irradiation) does NOT carry
# durability on its own in this model -- the same finding the HSA work made for eBAT: a
# duration-capped kill term, however strong, does not clear a bar that persists for a decade. TBI
# max_kill swept, applied for a single ~14-day conditioning window on top of CHOP + sub-threshold
# immunotherapy; 10-year durable response barely moves (and dips within Monte Carlo noise).
TBI_CONSOLIDATION_IS_NOT_PERSISTENT = {
    "on_chop_plus_subthreshold_immunotherapy_10yr": {0.0: 0.240, 0.10: 0.193, 0.20: 0.190, 0.35: 0.217},
    "on_chop_alone_10yr": {0.0: 0.250, 0.10: 0.170, 0.20: 0.153, 0.35: 0.153},
    "interpretation": "A single conditioning burst, no matter how intense, does not produce "
                      "10-year durability by itself -- durability needs a mechanism that persists "
                      "past the bar, not a one-time one. This is why the real curative protocol "
                      "does not stop at transplant.",
    "what_the_real_cure_actually_is": "Gareau et al. 2021 (PMID 34950726) reached a 40% cure "
                                      "fraction by adding ADOPTIVE T-CELL THERAPY to CHOP + "
                                      "transplant -- i.e. a persistent immune effector on top of "
                                      "the consolidation. Transplant alone relapses ~70%. The model "
                                      "and the real protocol agree: consolidation sets up the "
                                      "response; a persistent immune mechanism carries it.",
}

# Route C: two antigens instead of one -- a tandem CD19/CD20 CAR. In this parameterization a
# single-antigen effector AT the bar (0.09) already starves the antigen-loss route (1 of 300
# relapses), so the tandem construct adds little at threshold; its value is as insurance when
# antigen-loss seeding is higher, and it is the only closure if the effector is at threshold and
# antigen loss would otherwise be the last route standing. Below the bar (0.06) closing antigen loss
# does not help, because drug-resistance clones relapse anyway. Recomputed by the test module.
DUAL_TARGET = {
    0.06: {"single_antigen_durable": 0.240, "single_antigen_cd20_loss": 43,
           "tandem_durable": 0.210, "tandem_cd20_loss": 0},
    0.09: {"single_antigen_durable": 0.970, "single_antigen_cd20_loss": 1,
           "tandem_durable": 0.953, "tandem_cd20_loss": 0},
}
DUAL_TARGET_RATIONALE = {
    "construct": "Tandem CD19/CD20 CAR -- two independent B-cell antigens on one receptor, so "
                 "losing one does not evade it (Peng et al. 2026, PMID 42480604).",
    "real_grounding": "The same group observed CD20 loss in canine DLBCL after CD20 CAR-T, then "
                      "built the tandem construct to close it -- real antigen escape and a real "
                      "closure in the actual disease, unlike the HSA dual-vaccine route where "
                      "additivity was assumed.",
    "when_it_matters": "At threshold potency a single antigen already starves the loss route in "
                       "this parameterization; the tandem construct is insurance against a higher "
                       "real antigen-loss rate, and is necessary once the effector is strong enough "
                       "that antigen loss would otherwise be the last route left. Below the bar it "
                       "does not help, because drug-resistance clones relapse regardless of antigen.",
}


def bar_after_persistent_kill(agnostic_kill: float, bar: float = DURABILITY_BAR_PER_DAY) -> float:
    """The bar is growth - kill, so a persistent second kill term lowers it one-for-one."""
    return float(bar - agnostic_kill)
