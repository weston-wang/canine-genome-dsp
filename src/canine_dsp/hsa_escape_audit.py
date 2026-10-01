"""An independent audit of the escape list, and a grading of what is actually closed.

`CLAUDE.md` rule 9 requires that before any "closed / found / complete" claim, the candidate
universe is enumerated from the literature rather than from the list already in hand -- and that the
same is done for the ESCAPE list, as an independent audit rather than a re-grading.

This module is that audit. It was run against the eight routes in `docs/HSA_DURABLE_RESPONSE.md` and
found three escape paths that appear nowhere in the analysis, plus one scoping error in the endpoint
itself. It also re-grades the increment the whole plan turns on, which a randomised trial in the
matched clinical setting moves off ASSUMED.

Grading vocabulary, from the user's standing standard:

    MEASURED     -- real data, in this disease, in this species, in this setting.
    TRANSFERRED  -- real data from another species, disease or setting, with the transfer justified
                    in writing. Acceptable as closure.
    ASSUMED      -- no basis. Does NOT count as closure.

See docs/HSA_DURABLE_RESPONSE.md and docs/HSA_STATUS.md.
"""
from __future__ import annotations

import math

MEASURED = "MEASURED"
TRANSFERRED = "TRANSFERRED"
ASSUMED = "ASSUMED"

# =================================================================================================
# HOW THE AUDIT WAS RUN, so the result can be reproduced rather than taken on trust.
# =================================================================================================

HOW_THE_ESCAPE_UNIVERSE_WAS_ENUMERATED = {
    "method": "the candidate escape classes were listed from general tumour-immunology and "
              "metastasis biology WITHOUT consulting the eight routes already in the analysis, "
              "then each was grepped against docs/HSA_DURABLE_RESPONSE.md and the hsa_* modules to "
              "see whether the record addressed it at all.",
    "classes_checked": (
        "anatomical sanctuary sites", "phenotypic sanctuary (antigen-null)", "dormancy and "
        "quiescence", "antigen-presentation machinery loss (B2M/TAP)", "regulatory T cells",
        "myeloid-derived suppressor cells", "tumour-associated macrophages", "T-cell exhaustion",
        "immunosenescence of the host", "tumour-induced lymphopenia", "clonal evolution to a new "
        "driver", "second primary tumour", "competing all-cause mortality", "drug resistance "
        "(pathway, target-site, crosstalk)", "haemorrhage as a competing event"),
    "classes_with_zero_hits_in_the_record": (
        "anatomical sanctuary sites", "dormancy", "regulatory T cells", "MDSC",
        "antigen-presentation machinery (B2M/TAP)", "immunosenescence", "tumour-induced "
        "lymphopenia", "second primary tumour", "clonal evolution", "competing all-cause "
        "mortality"),
    "the_trap_this_caught": "the word 'sanctuary' appears 20 times in the narrative document and "
                            "every one of them is PHENOTYPIC -- an antigen-null state. A keyword "
                            "count would have scored anatomical sanctuary as covered. It is not "
                            "mentioned anywhere.",
}

# =================================================================================================
# ROUTE 9. ANATOMICAL SANCTUARY -- the central nervous system.
#
# This is the most serious omission the audit found, and it is MEASURED, in dogs, in this disease.
# =================================================================================================

ROUTE_9_CNS_SANCTUARY = {
    "grade_of_the_threat": MEASURED,
    "citation": "Snyder et al. 2008, J Vet Intern Med 22(1):172-177, PMID 18289306, "
                "doi 10.1111/j.1939-1676.2007.0002.x",
    "design": "177 client-owned dogs with secondary intracranial neoplasia, all with complete "
              "postmortem examination, 1986-2003",
    "the_finding": "secondary intracranial neoplasia was MORE common than primary, and "
                   "hemangiosarcoma was the single most common source: 51 of 177 (29%), ahead of "
                   "pituitary tumours (25%), lymphosarcoma (12%) and metastatic carcinoma (12%). "
                   "Mean age at diagnosis 9.6 +/- 3.0 years.",
    "what_the_29_percent_is_and_is_not": "it is the share of SECONDARY BRAIN TUMOURS that were "
                                         "hemangiosarcoma. It is NOT the share of hemangiosarcoma "
                                         "dogs that develop brain metastasis -- that denominator is "
                                         "different and this paper does not supply it. Secondary "
                                         "sources put the per-dog figure near 14% at necropsy; that "
                                         "figure is NOT verified here and is recorded as unconfirmed.",
    "why_it_breaks_the_plan": "every cytotoxic and small-molecule component of the regimen has poor "
                              "central nervous system penetration. Doxorubicin is a P-glycoprotein "
                              "substrate and is effectively excluded. eBAT is a ~55 kDa bispecific "
                              "protein toxin and does not cross. Losartan is deliberately not "
                              "CNS-penetrant. A monoclonal antibody reaches roughly 0.1% of its "
                              "serum concentration in CSF. So the route-8 closure -- doxorubicin "
                              "plus one eBAT cycle -- does NOT extend to a central nervous system "
                              "deposit.",
    "the_closure_and_it_selects_a_platform": "activated T cells cross the blood-brain barrier; that "
                                             "is ordinary immune surveillance, not a special "
                                             "property of any product. Central memory T cells enter "
                                             "the CSF through the choroid plexus, and activated "
                                             "effector T cells transmigrate the barrier itself. "
                                             "Checkpoint inhibitors are documented to have CNS "
                                             "activity DESPITE poor penetration, because the "
                                             "antibody acts on T cells systemically and the T cells "
                                             "do the crossing.",
    "the_consequence_that_is_actually_useful": "this makes the CNS route a PLATFORM SELECTOR. A "
                                               "vaccine whose effector arm is T-cell mediated "
                                               "reaches a brain deposit. A vaccine whose effector "
                                               "arm is antibody against a surface protein does not. "
                                               "Of the two real trials in this disease, ERstrePs "
                                               "raises BOTH humoral and T-cell responses and so "
                                               "covers this route; eVim raises antibodies against "
                                               "extracellular vimentin and so does NOT. The "
                                               "analysis had treated the two as interchangeable "
                                               "anchors for a single 0.030/day figure.",
    "grade_of_the_closure": TRANSFERRED,
    "why_transferred_and_not_measured": "T-cell trafficking across the blood-brain barrier and the "
                                        "CNS activity of checkpoint blockade are established in "
                                        "humans and in rodent models, not in dogs with "
                                        "hemangiosarcoma brain metastases. No canine HSA study has "
                                        "measured whether a vaccine-primed T-cell response reaches "
                                        "an intracranial deposit.",
    "what_remains_open": "HSA brain metastases are highly vascular and haemorrhagic. Intracranial "
                         "haemorrhage is a lethal event in its own right that no component of this "
                         "plan treats -- it belongs with the rupture hazard as a competing event, "
                         "not with the cancer-control figures.",
}

# =================================================================================================
# ROUTE 10. HOST IMMUNOSENESCENCE over the treatment horizon.
# =================================================================================================

ROUTE_10_IMMUNOSENESCENCE = {
    "grade_of_the_threat": MEASURED,
    "the_finding_in_dogs": "immunosenescence is documented in dogs: thymic involution reduces naive "
                           "T-cell output, total T cells, B cells, CD4+ and CD8+ all decline with "
                           "age, the CD4:CD8 ratio falls, and older dogs show LOWER PROLIFERATIVE "
                           "CAPACITY OF CD8+ T CELLS -- which is the effector arm this plan runs "
                           "on. Antibody titres to novel antigens are reduced in senior dogs "
                           "relative to young ones.",
    "why_it_is_specific_to_this_plan_and_not_generic": "the plan asks a vaccine to hold a tumour for "
                                                       "ten years in a dog that is already old when "
                                                       "it is primed. The mean age at diagnosis in "
                                                       "the Snyder cohort was 9.6 years. A ten-year "
                                                       "horizon therefore runs the vaccine from "
                                                       "roughly age 10 to age 20, across the "
                                                       "steepest part of the immunosenescence curve.",
    "the_part_that_closes": "the compromised step is the PRIMARY response. Memory responses are "
                            "reported to remain intact in older dogs. The plan's structure is prime "
                            "once, then boost for life -- so the maintenance phase is the part "
                            "immunosenescence spares, and the induction is the part it attacks.",
    "the_lever_already_in_the_analysis_that_fits_this_exactly": "re-dosing. hsa_route_effect_sizes "
                                                               "demoted it as a potency lever "
                                                               "because it needs 118-235% transfer "
                                                               "and cannot close the height gap. But "
                                                               "the finding behind it -- repeat "
                                                               "immunisation raising response "
                                                               "MAGNITUDE in poor responders up to "
                                                               "the level of good responders, in 118 "
                                                               "dogs -- is precisely the right tool "
                                                               "for a compromised primary response "
                                                               "in an old animal. It was being "
                                                               "graded against the wrong problem.",
    "grade_of_the_closure": TRANSFERRED,
    "the_correction_this_forces": "re-dosing is not a weak version of the other levers. It is the "
                                  "answer to a different question -- take rate in an "
                                  "immunosenescent host -- that the analysis never asked. Demoting "
                                  "it on the potency axis was right; implying it is therefore "
                                  "marginal was wrong.",
    "what_remains_open": "no canine study has measured a cancer vaccine's take rate as a function of "
                         "age, and none has followed vaccine-induced immunity in a dog for anything "
                         "approaching ten years. The longest booster-interval evidence in this "
                         "analysis is a two-monthly schedule over a trial of months.",
}

# =================================================================================================
# ROUTE 11. THE ENDPOINT ITSELF -- competing all-cause mortality.
#
# Not an escape of the cancer. A scoping error in what "10+ years of durable response" can mean.
# =================================================================================================

MEAN_AGE_AT_DIAGNOSIS_YEARS = 9.6          # Snyder 2008, secondary intracranial HSA cohort
BREED_MEDIAN_LIFESPAN_YEARS = {
    "German Shepherd Dog": 10.3,           # VetCompass UK, IQR 8.0-12.1, range 0.2-17.0
    "Golden Retriever": 11.75,             # European primary-care range 11.0-12.5, midpoint
    "Labrador Retriever": 12.0,            # VetCompass UK, IQR 9.9-13.8
}
EARLY_DETECTION_LEAD_YEARS = (2.0, 4.0)    # the Shine On claim, institutional reporting only


def remaining_natural_lifespan(breed: str, age_at_diagnosis: float = MEAN_AGE_AT_DIAGNOSIS_YEARS,
                               lead_time_years: float = 0.0) -> float:
    """Years from diagnosis to the breed's median lifespan, given any early-detection lead.

    Negative means the median dog of that breed is already past median lifespan at diagnosis.
    """
    if breed not in BREED_MEDIAN_LIFESPAN_YEARS:
        raise ValueError(f"unknown breed {breed!r}; expected one of "
                         f"{sorted(BREED_MEDIAN_LIFESPAN_YEARS)}")
    if lead_time_years < 0:
        raise ValueError("lead time cannot be negative")
    return float(BREED_MEDIAN_LIFESPAN_YEARS[breed] - (age_at_diagnosis - lead_time_years))


ROUTE_11_THE_DOG_RUNS_OUT_OF_LIFE = {
    "grade_of_the_finding": MEASURED,
    "the_arithmetic": "mean age at diagnosis 9.6 years against breed median lifespans of 10.3 "
                      "(German Shepherd), ~11.0-12.5 (Golden Retriever) and 12.0 (Labrador). A "
                      "ten-year DURABLE RESPONSE from diagnosis requires the dog to reach roughly "
                      "20 -- about double the breed median, and beyond the oldest animal in the "
                      "VetCompass German Shepherd cohort (17.0 years).",
    "with_early_detection": "the user's standing assumption is early detection. A 2-4 year lead "
                            "moves diagnosis to roughly 5.6-7.6 years, so ten years takes the dog "
                            "to 15.6-17.6. Still above the breed median, but inside the observed "
                            "range rather than outside it.",
    "what_this_does_NOT_mean": "it does not mean the analysis is wasted or the modelling is wrong. "
                               "The 3,650-day horizon is a CONSERVATIVE PROXY FOR CURE: anything "
                               "that holds for ten years has certainly held for the animal's "
                               "remaining life. Clearing a stricter bar than the biology requires "
                               "is a safe error.",
    "what_it_DOES_mean": "three things. (1) The honest endpoint for this population is "
                         "'disease-free for remaining natural lifespan', which is ~0.7-2.4 years "
                         "from diagnosis at 9.6 and ~4-7 years with early detection -- so the "
                         "practical target is EASIER than the one being modelled, not harder. "
                         "(2) Competing all-cause mortality must be carried alongside the rupture "
                         "hazard, or ten-year figures overstate what an owner would observe. "
                         "(3) A second primary tumour is a real event over that horizon in these "
                         "breeds and is not an escape of this treatment at all.",
    "the_honest_statement_of_the_goal": "'10+ years of durable response' is, for the median dog "
                                        "diagnosed at 9.6, unreachable for reasons that have "
                                        "nothing to do with hemangiosarcoma. The reachable version "
                                        "of the same goal is 'no recurrence for the rest of the "
                                        "dog's life', and the model's ten-year horizon is a "
                                        "conservative way of testing for it.",
}

# =================================================================================================
# ROUTES 12-14. The remaining audit classes, closed by arguments already in the analysis.
# =================================================================================================

ROUTES_CLOSED_BY_EXISTING_ARGUMENTS = {
    "dormancy_and_quiescence": {
        "the_threat": "a non-dividing cell escapes every growth-dependent mechanism, then resumes.",
        "why_it_closes": "immune killing is not growth-dependent -- a cytotoxic T cell does not "
                         "require its target to be in cycle. A persistent vaccine therefore covers "
                         "a dormant cell both while dormant and on re-entry, which is the same "
                         "argument that closes route 7 (disease outside the resected compartment). "
                         "The targeted drugs do not cover it; the vaccine does.",
        "grade": TRANSFERRED,
        "the_caveat": "this is an argument from mechanism, not a measurement. No study in this "
                      "disease has shown vaccine-primed killing of a dormant hemangiosarcoma cell.",
    },
    "antigen_presentation_machinery_loss_B2M_TAP": {
        "the_threat": "losing B2M or TAP is an irreversible, harder version of route 4 -- the cell "
                      "cannot present ANY peptide antigen, so no T-cell vaccine reaches it.",
        "why_it_closes": "this is the single case where the missing-self backup is STRONGEST rather "
                         "than weakest. B2M loss is the classic trigger for NK missing-self "
                         "recognition, and the analysis already carries Lerner 2023 (PMID 37537301): "
                         "MHC-loss variants upregulate NKG2D ligands and are killed through NKG2D, "
                         "with killing abrogated by NKG2D blockade. Separately, eVim's target is "
                         "extracellular vimentin, which is antibody-recognised and needs no MHC at "
                         "all.",
        "grade": TRANSFERRED,
    },
    "regulatory_T_cells_and_myeloid_derived_suppressor_cells": {
        "the_threat": "suppressive populations distinct from the M2 macrophages the analysis covers.",
        "why_it_partly_closes": "monocytic MDSCs are recruited through the CCR2 axis, which is "
                                "exactly what losartan blocks, and eBAT depletes uPAR-expressing "
                                "myeloid cells. So two of the four levers already act on this "
                                "compartment without having been credited for it.",
        "grade": TRANSFERRED,
        "the_treg_lever_that_was_already_in_the_record_uncredited": "Maekawa 2022 (PMID 35665759), "
            "already cited in this analysis for the CCL2 coupling, also reports that PGE2 predicted "
            "RESISTANCE to checkpoint blockade in dogs, and that meloxicam plus the antibody "
            "enhanced Th1 cytokine production by canine PBMCs. PGE2 is the canonical axis for "
            "inducing and sustaining regulatory T cells, so COX-2 inhibition is a Treg-directed "
            "lever -- and meloxicam is already given to dogs indefinitely, so it clears the "
            "duration criterion outright. The analysis had this in a parenthetical and never "
            "credited it against the Treg compartment.",
        "what_stays_open": "no measurement exists of the regulatory T-cell burden in canine "
                           "hemangiosarcoma, and no effect size for COX-2 inhibition on it. The "
                           "lever is identified and tolerable; its magnitude is unmeasured.",
    },
    "clonal_evolution_to_a_new_resistance_driver": {
        "the_threat": "the engine carries a fixed clone set and a fixed mutation matrix. A driver "
                      "that does not exist on day zero cannot arise in it.",
        "why_it_partly_closes": "the vaccine's coverage is ANTIGEN-based, not driver-based. A cell "
                                "that acquires a new driver is still visible to the vaccine unless "
                                "it also loses the antigen -- which is routes 4 and 8, already "
                                "accounted.",
        "the_bound_that_closes_it_properly": "a RESISTANCE lesion cannot make a clone grow faster "
                                             "than it would with no drug present at all, because "
                                             "the drug only ever subtracts from the untreated rate. "
                                             "The worst case is therefore already a row in the bar "
                                             "table of section 1: 'no drug at all' = 0.0550/day "
                                             "against the modelled 0.0515. A novel resistance "
                                             "mechanism, however exotic, buys at most +6.8% on the "
                                             "bar.",
        "what_that_costs_the_plan": "the vaccine requirement scales with the bar, so 1.40x against "
                                    "the modelled bar becomes 1.50x against the no-drug ceiling -- "
                                    "which is still inside the measured ramp (1.50x returns 0.992 "
                                    "at a one-year stop). The plan survives the worst resistance "
                                    "clone that can exist, at the cost of one rung.",
        "grade": TRANSFERRED,
        "what_this_does_NOT_close": "a driver that raises INTRINSIC proliferative rate rather than "
                                    "relieving drug pressure -- a genuinely more aggressive clone "
                                    "than its parent. That is a different event from resistance and "
                                    "the no-drug row does not bound it. Mitigation, not closure: "
                                    "the requirement degrades along the ramp rather than off a "
                                    "cliff, and such a clone is still antigen-visible.",
    },
}

# =================================================================================================
# THE INCREMENT THE WHOLE PLAN TURNS ON -- regraded.
#
# Every route above ultimately depends on the vaccine clearing the bar, and that depends on an
# increment of 0.012/day that nobody has measured in this tumour. The analysis graded it ASSUMED.
# A randomised trial in the MATCHED CLINICAL SETTING moves part of it.
# =================================================================================================

KEYNOTE_942 = {
    "citation": "Weber et al., KEYNOTE-942 / mRNA-4157 (V940) plus pembrolizumab versus "
                "pembrolizumab monotherapy in resected high-risk stage III/IV melanoma; randomised "
                "phase 2b, NCT03897881. Three-year update reported 2025.",
    "why_this_trial_and_not_another": "it is the only randomised trial this audit found that "
                                      "isolates what adding ONE immune agent to an immune backbone "
                                      "buys, in the ADJUVANT, COMPLETELY RESECTED, "
                                      "MINIMAL-RESIDUAL-DISEASE setting -- which is this plan's "
                                      "setting exactly. Every other anchor in the analysis measures "
                                      "a single agent against no agent, in measurable disease.",
    "design": "157 patients randomised 2:1 to vaccine + pembrolizumab (n=107) or pembrolizumab "
              "alone (n=50), after complete resection",
    "result": {
        "rfs_hazard_ratio": 0.510, "rfs_ci": (0.288, 0.906), "rfs_p": 0.019,
        "rfs_at_2_5_years": (0.748, 0.556),       # combination, control
        "distant_metastasis_free_hazard_ratio": 0.384, "dmfs_ci": (0.172, 0.858),
    },
    "the_direction_it_establishes": "a vaccine and a checkpoint inhibitor are NOT redundant in the "
                                    "minimal-residual-disease setting. The analysis had assumed "
                                    "they combine; this measures it, randomised, in the matched "
                                    "setting.",
}

# The per-day conversion used for the four levers, applied here -- and why it fails.
KEYNOTE_942_RATE_CONVERSION = {
    "implied_rate_per_day": (0.00108, 0.00216),   # lethal burden multiple 10x to 100x
    "transfer_needed": (5.55, 11.11),             # 555% to 1111%
    "why_this_conversion_is_NOT_the_right_one": "it reads as a catastrophic failure and it is an "
                                                "artefact. The conversion assumes time-to-event is "
                                                "inversely proportional to net growth rate, so it "
                                                "carries the ABSOLUTE TIME SCALE across the species "
                                                "jump. Human melanoma's median time to recurrence "
                                                "here is ~1,077 days; canine hemangiosarcoma's "
                                                "untreated median is ~48 days and its treated median "
                                                "~180. A method that transports a per-day rate "
                                                "between processes running at a six-fold different "
                                                "tempo is being used outside its domain.",
    "the_internal_check_that_says_the_arithmetic_is_right": "converting the reported 2.5-year RFS "
                                                            "rates to exponential hazards reproduces "
                                                            "the trial's own hazard ratio: 0.495 "
                                                            "derived against 0.510 reported. The "
                                                            "arithmetic is sound; the transport is "
                                                            "not.",
}


def required_hazard_ratio(durability_with_lever: float, durability_without: float) -> float:
    """Hazard ratio on ten-year FAILURE implied by moving between two durabilities.

    Unitless, so unlike a per-day rate it survives a jump between processes running at different
    tempo. Both quantities answer the same question -- what proportional reduction in the chance of
    failure does adding an immune agent on top of an immune backbone buy?
    """
    for d in (durability_with_lever, durability_without):
        if not 0.0 < d < 1.0:
            raise ValueError("durabilities must lie strictly between 0 and 1")
    return float(math.log(durability_with_lever) / math.log(durability_without))


# Computed against hsa_route_effect_sizes.DURABILITY_BY_INCREMENT at stop_year=1.
SCALE_FREE_COMPARISON = {
    "plan_requirement_by_vaccine_multiple": {
        1.35: 0.406,     # durability 0.732
        1.40: 0.178,     # durability 0.872  <- the headline requirement
        1.45: 0.042,     # durability 0.968
        1.50: 0.010,     # durability 0.992
    },
    "measured_hazard_ratio_rfs": 0.510,
    "measured_hazard_ratio_dmfs": 0.384,
    "fraction_of_the_needed_log_hazard_delivered_at_1_40x": (0.39, 0.56),   # RFS, DMFS
    "the_rung_the_measured_effect_clears_outright": "at 1.35x the plan needs a hazard ratio of "
                                                    "0.406. The measured distant-metastasis-free "
                                                    "hazard ratio is 0.384. ONE lever, at full "
                                                    "transfer, clears the 1.35x rung on that "
                                                    "endpoint -- which buys a two-year induction at "
                                                    "durability 0.864, just under the 0.888 "
                                                    "drug-forever reference.",
    "what_this_changes": "the increment moves from ASSUMED to TRANSFERRED for DIRECTION and for "
                         "PARTIAL MAGNITUDE. A randomised trial in the matched setting shows the "
                         "combination is real and delivers 39-56% of the needed log-hazard from a "
                         "single lever. The plan has four levers and does not need any one of them "
                         "to deliver everything.",
    "what_it_does_NOT_change": "whether canine hemangiosarcoma's microenvironment responds like "
                               "human melanoma's, and whether the four levers STACK rather than "
                               "overlap. The analysis already records that routes 1 and 2 are "
                               "mechanistically coupled, and eBAT depletes the same macrophages "
                               "the other two act on. Coupled levers may overlap rather than sum, "
                               "so four levers is not four times one.",
    "grade_after_this_audit": TRANSFERRED,
    "grade_before_this_audit": ASSUMED,
}

# =================================================================================================
# THE VERDICT against the user's stated goal.
# =================================================================================================

VERDICT = {
    "the_goal_as_stated": "10+ years of durable response, with every mechanism and every escape "
                          "path covered scientifically -- by real data or a rigorous model, with "
                          "potency and toxicity considered.",
    "is_it_covered": "NO, not yet -- but the gap is smaller and more specific than before this "
                     "audit, and one of the three new findings makes the goal EASIER rather than "
                     "harder.",
    "what_newly_fails": (
        "route 9, CNS sanctuary: MEASURED threat, no component of the route-8 closure reaches the "
        "brain. Closable, and the closure selects a vaccine platform.",
        "route 10, host immunosenescence: MEASURED threat in dogs, attacking the induction step "
        "specifically. Closable by re-dosing, which the analysis had demoted against a different "
        "question.",
        "route 11, the endpoint: a ten-year disease-free requirement is unreachable for a median "
        "dog diagnosed at 9.6 for reasons unrelated to the cancer. The reachable version of the "
        "goal is 'no recurrence for the rest of the dog's life'.",
    ),
    "what_newly_improves": "the increment the whole plan turns on moves ASSUMED -> TRANSFERRED on "
                           "the strength of a randomised trial in the matched adjuvant setting.",
    "what_is_still_ASSUMED_and_therefore_still_open": (
        "the magnitude of the increment in canine hemangiosarcoma specifically",
        "whether the four levers stack or overlap",
        "a driver raising INTRINSIC proliferative rate (resistance drivers are now bounded)",
        "the magnitude of COX-2 inhibition against the regulatory T-cell compartment",
        "the per-dog brain-metastasis rate in canine HSA -- route 9's weight, not its existence",
        "the post-remission rupture hazard, still swept rather than measured",
        "the existence of the route-8 compartment at all",
    ),
    "the_honest_one_line": "every escape path now has a named closure or a named gap, and the "
                           "number the plan turns on is no longer baseless -- but four of the "
                           "closures are arguments rather than measurements, and the goal as "
                           "literally worded is the wrong test.",
}
