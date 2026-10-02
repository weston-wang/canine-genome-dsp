"""The two remaining gaps, and the constraint that closing them uncovered.

`hsa_open_item_closures` left two items as missing measurements rather than contradictions:
trametinib engaging its target inside a canine tumour, and NK cells given systemically. Both have
been done. Finding them also surfaced a phase 2 result that constrains WHEN the immune components
can be given -- and it converges with the eBAT failure from a completely independent direction.

See docs/HSA_DURABLE_RESPONSE.md.
"""

# ---------------------------------------------------------------------------------------------
# GAP 1 CLOSED. Trametinib target engagement in canine tumour tissue was demonstrated in 2018,
# six years before the canine phase I that looked for it too early.
TRAMETINIB_ENGAGES_ITS_TARGET_IN_CANINE_TUMOURS = {
    "citation": "Takada et al. 2018, Mol Cancer Ther 17(11):2439-2450, PMID 30135215, "
                "doi 10.1158/1535-7163.MCT-17-1273",
    "same_investigator": "Takada M is first author on both this and the 2024 canine phase I "
                         "(PMID 38889903) whose day-7 biopsy found nothing.",
    "system": "canine histiocytic sarcoma cells in an intrasplenic orthotopic xenograft -- a "
              "disseminated model, and canine tumour tissue",
    "target_engagement": "'Target engagement was validated as activity of ERK, downstream of MEK, "
                         "was significantly downregulated in neoplasms of treated mice.'",
    "drug_reached_the_tumour": "'trametinib was found in plasma AND NEOPLASTIC TISSUES within "
                               "projected therapeutic levels' -- exposure confirmed at the tumour, "
                               "not merely in blood",
    "mechanism_of_kill": "apoptosis, shown by a significant increase in caspase 3/7",
    "efficacy": "significantly longer survival in treated mice",
    "the_mapk_lesions": "one canine line carries PTPN11 E76K and another KRAS Q61H, both reported in "
                        "human histiocytic sarcoma -- the MAPK node is genuinely driving, not "
                        "incidental",
    "what_it_does_and_does_not_settle": "pERK suppression plus intratumoural drug levels in canine "
                                        "tumour tissue is direct target-engagement evidence. It is "
                                        "canine cells in a mouse host, and histiocytic sarcoma "
                                        "rather than hemangiosarcoma. It removes 'never "
                                        "demonstrated' and replaces it with 'demonstrated in the "
                                        "wrong tumour type'.",
    "status": "CLOSED -- the drug reaches canine tumour tissue at therapeutic levels and shuts down "
              "the pathway it targets.",
}

# ---------------------------------------------------------------------------------------------
# GAP 2 CLOSED. NK cells have been given INTRAVENOUSLY to dogs, autologous and allogeneic, safely.
NK_CELLS_HAVE_BEEN_GIVEN_INTRAVENOUSLY = {
    "citation": "Razmara et al. 2024, J Immunother Cancer 12(4):e007963, PMID 38631708, "
                "doi 10.1136/jitc-2023-007963",
    "manufacturing_advance": "expanded from unmanipulated PBMCs rather than CD5-depleted cells, "
                             "which lifts the yield ceiling; the day-14 product is CD3- NKp46+ with "
                             "equivalent or better killing than the older method",
    "autologous_trial": {
        "route": "INTRAVENOUS, slow bolus",
        "dose": "7.5e6 NK cells/kg with 5 ng/mL rhIL-15 in 50 mL",
        "schedule": "two infusions, days 0 and 7",
        "n_dogs": 9, "tumours": "4 melanoma, 5 osteosarcoma",
        "cytokine_support": "inhaled IL-15, 50 ug twice daily for 14 days",
        "safety": "no treatment-related serious adverse events",
        "efficacy": "one partial response and one stable disease by RECIST",
    },
    "allogeneic_trial": {
        "route": "INTRAVENOUS",
        "dose": "7.5e6 NK cells/kg with 5 ng/mL rhIL-15 in 50 mL, single infusion on the day of "
                "final radiotherapy",
        "n_dogs": 5, "tumours": "unresectable oral melanoma",
        "cytokine_support": "rhIL-15 3 ug/kg subcutaneously after infusion and again at 20-30 h",
        "safety": "no serious adverse events related to NK cell injections",
        "efficacy": "median survival 145 days, one dog at 445 days",
    },
    "no_lymphodepletion": "neither trial used conditioning chemotherapy before transfer",
    "why_allogeneic_matters": "an allogeneic product works off the shelf. Per-dog manufacture from "
                              "the patient's own blood is the harder logistics, and it turns out not "
                              "to be mandatory.",
    "status": "CLOSED -- systemic NK delivery in dogs is established, dosed, and safe. What has not "
              "been done is giving it for hemangiosarcoma.",
}

# ---------------------------------------------------------------------------------------------
# THE CONSTRAINT THIS UNCOVERED. Two independent groups, two different immune agents, the same
# failure -- and this one measured the mechanism.
SURGERY_AND_CHEMOTHERAPY_SUPPRESS_THE_EFFECTOR = {
    "citation": "Rebhun et al. 2025, Front Immunol 16:1672790, PMID 41209004, "
                "doi 10.3389/fimmu.2025.1672790 (NCI-COTC030)",
    "design": "multicentre phase 2, dogs with appendicular osteosarcoma: two weeks of inhaled rhIL-15 "
              "after amputation and before chemotherapy, powered to cut metastatic failure from 40% "
              "to 20%",
    "result": "disease-free and overall survival were statistically INFERIOR to a well-validated "
              "historical control cohort. The trial was halted for futility.",
    "the_measured_mechanism": "PBMC cytotoxicity fell significantly after surgery AND after "
                              "chemotherapy, -18.2 +/- 16.1% from start to end of therapy (P<0.001). "
                              "IL-6 rose after amputation and after chemotherapy, and those rises "
                              "tracked the falls in cytotoxicity.",
    "the_biomarker_runs_both_ways": "dogs whose PBMC cytotoxicity INCREASED lived significantly "
                                    "longer (P=0.004, r=0.62). The assay predicts outcome, which "
                                    "makes it a usable go/no-go rather than a post-hoc curiosity.",
    "authors_conclusion": "'These data have important implications on novel immunotherapy strategies "
                          "involving multimodality approaches including surgery and chemotherapy.'",
}

# The convergence is the point: two agents, two groups, two diseases, one lesson.
TWO_INDEPENDENT_FAILURES_WITH_THE_SAME_SHAPE = {
    "failure_1": "eBAT redosed at a REDUCED interval from doxorubicin: greater toxicity, reduced "
                 "efficacy, no survival benefit (Borgatti et al. 2020, PMID 32187827). The authors "
                 "attribute it to schedule relative to chemotherapy.",
    "failure_2": "inhaled IL-15 between amputation and chemotherapy: inferior survival, halted for "
                 "futility (Rebhun et al. 2025, PMID 41209004). The authors measured surgery and "
                 "chemotherapy suppressing the effector cells the therapy depends on.",
    "what_they_share": "both put an immune therapy INSIDE the peri-surgical and peri-chemotherapy "
                       "window. Neither failed because the mechanism was wrong; both failed in the "
                       "window where the host's effector function is measurably at its lowest.",
    "why_this_matters_here": "splenectomy followed by doxorubicin is exactly that window, and it is "
                             "exactly where an HSA regimen would be tempted to add its immune "
                             "components. Two trials have now run that experiment and both went "
                             "backwards.",
    "the_design_consequence": "the vaccine, the boosters and any NK component should be scheduled to "
                              "AVOID the peri-operative and active-chemotherapy window rather than "
                              "to fill it -- and PBMC cytotoxicity gives a measured gate for when "
                              "the host has recovered enough to be worth dosing.",
    "consistency_with_the_model": "the engine already says the same thing from the other direction: "
                                  "starting the second drug on day 0, 60 or 180 barely changes the "
                                  "outcome (0.932 / 0.928 / 0.896). Delay is nearly free in the "
                                  "model, and these two trials say it is not free to be early.",
}

VERDICT = {
    "both_gaps_closed": "trametinib suppresses ERK in canine tumour tissue at measured intratumoural "
                        "drug levels; NK cells have been given intravenously to dogs, autologous and "
                        "allogeneic, without serious adverse events.",
    "what_replaced_them": "a sharper and more useful constraint. The open question is no longer "
                          "whether these therapies can be delivered -- it is WHEN.",
    "the_residual": "no trial has given either component for hemangiosarcoma, and the two "
                    "demonstrations sit in histiocytic sarcoma, melanoma and osteosarcoma. Species "
                    "and delivery are settled; the disease is not.",
    "the_experiment_this_now_points_at": "the same trial as before, with one design change carried "
                                         "over from two independent failures: schedule the immune "
                                         "components after the chemotherapy backbone rather than "
                                         "inside it, and gate dosing on recovered PBMC cytotoxicity.",
}
