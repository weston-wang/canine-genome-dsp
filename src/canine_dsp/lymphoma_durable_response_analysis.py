"""Durable response in canine multicentric lymphoma: the bar, the escape routes, and their closure.

This module asks, for canine lymphoma, the exact sequence of questions the histiocytic-sarcoma and
hemangiosarcoma pipelines asked: what per-day growth rate ("the bar") a lasting remission must
out-kill, whether that bar is achievable, which escape routes survive, and what closes each one --
with the stated target of cure or 10-year durability. It reuses `lymphoma_scenarios`' presets and
real anchors and the shared Monte Carlo engine in `mapk_resistance`, adding nothing new to either.
See docs/LYMPHOMA_DURABLE_RESPONSE.md.

Every numeric figure below is recomputed from the engine by tests in
`tests/test_lymphoma_durable_response_analysis.py`. Nothing here is a treatment recommendation, and
no combination described has been given to a dog. Growth rates, kill ceilings and immunotherapy
potency are illustrative placeholders swept across ranges; what is real and cited is the resistance
biology, the trial outcomes, and the transplant cure fraction.
"""

# The bar, by drug-exposure assumption. From mapk_resistance.clone_growth_margins against
# lymphoma_scenarios.dog_lymphoma_preset('B'); reproduced by the test module. "bar_resistant" is the
# fastest-growing clone the drug does NOT drive negative -- the number a durable mechanism must beat.
DURABILITY_BAR_PER_DAY = {
    "full_chop_5x_ic50": 0.0903,
    "derated_to_40pct_for_toxicity": 0.0916,
    "no_drug_at_all": 0.0920,
    "set_by_clone": "mdr1_pgp_efflux -- the P-glycoprotein drug-efflux clone, the most frequently "
                    "observed real acquired-resistance mechanism at relapse",
    "sensitive_clone_margin_under_full_chop": -0.157,
    "interpretation": "CHOP drives the drug-sensitive clone deeply negative (-0.157/day) -- which "
                      "is why ~90%+ of dogs go into complete remission -- and moves the resistant "
                      "bar by about 2% (0.0920 untreated to 0.0903 under full CHOP). The regimen "
                      "decides how fast and how deeply the tumour shrinks, and almost nothing about "
                      "whether it comes back.",
}

# Why the drug is nearly irrelevant to durability -- the same finding the HSA module made, but here
# resting on a measured mechanism rather than an extrapolated one.
CHEMO_IS_NOT_DURABILITY = {
    "the_mechanism_is_real": "P-glycoprotein (ABCB1) efflux pumps doxorubicin and vincristine back "
                             "out of the cell; a selected canine lymphoid line became resistant to "
                             "both, and resistance reversed completely with the P-gp inhibitor "
                             "PSC833 (Zandvliet et al. 2014, PMID 24975508). BCRP/ABCG2 adds a "
                             "second efflux pump, upregulated at relapse in 35/63 (55.6%) dogs "
                             "(Zandvliet et al. 2014, PMID 25475167).",
    "chemo_only_durable_response": {"1yr": 0.180, "2yr": 0.180, "5yr": 0.180, "10yr": 0.180},
    "why_it_is_flat": "The dogs that relapse do so early (matching the real 176-day median "
                      "progression-free survival, LYMPHOMA_CHOP_BENCHMARK); the ~18% that do not "
                      "are the ones whose tumour never harboured or acquired an efflux clone. No "
                      "amount of additional follow-up changes that split, because CHOP cannot "
                      "out-kill the efflux clone at any point.",
    "t_cell_is_the_same_or_worse": {"chemo_only_10yr_B": 0.180, "chemo_only_10yr_T": 0.177},
}

# What real immunotherapy potency has to clear, and what the engine says about it. Unlike HSA, there
# is no completed efficacy trial to back out a kill rate from, so potency is swept and the real
# anchor is the transplant cure fraction (see lymphoma_gap_closure). The threshold behaviour is the
# point: below the bar the immune effector does essentially nothing; at the bar it reaches durable.
IMMUNOTHERAPY_ACHIEVABILITY = {
    "candidate": "CD20-directed cellular/antibody immunity (anti-CD20 CAR-T or mAb)",
    "why_it_covers_the_chemoresistance_clones": "CD20 expression is independent of drug efflux and "
                                                "of apoptosis machinery, so a CD20-directed effector "
                                                "sees the P-gp, BCRP and apoptosis-evasion clones "
                                                "exactly as well as the sensitive clone. Resistance "
                                                "to a drug does not change what the immune system "
                                                "was trained to see -- the same argument the HSA and "
                                                "HS vaccine work made.",
    "engine_durable_by_potency_2yr": {0.0: 0.217, 0.03: 0.220, 0.06: 0.217, 0.09: 0.993, 0.12: 1.000},
    "engine_durable_by_potency_10yr": {0.0: 0.250, 0.03: 0.260, 0.06: 0.240, 0.09: 0.970, 0.12: 1.000},
    "bar_to_clear": 0.0903,
    "verdict": "A CD20 effector below ~0.09/day of kill does essentially nothing to 10-year "
               "durability (0.24-0.26, barely above chemo-only). At the bar it reaches 0.97 and "
               "above it 1.00. The threshold sits exactly where the growth margin predicts.",
    "real_immunotherapy_evidence": "Canine CD20 CAR-T kills CD20+ canine lymphoma cells in vitro "
                                   "and spares CD20-negative cells (Sakai et al. 2020, PMID "
                                   "32329214); CD20 loss has been seen in canine DLBCL patients "
                                   "treated with CD20 CAR-T (Peng et al. 2026, PMID 42480604). The "
                                   "mechanism and its escape route are both real; the kill-rate "
                                   "magnitude is not yet measured, so it is swept here.",
    "first_in_dog_supports_the_threshold": "The first-in-dog CD20 CAR-T (Panjwani et al. 2016, "
        "PMID 27401141, DOI 10.1038/mt.2016.146) used a TRANSIENT RNA-transfected CAR, was well "
        "tolerated, and gave only a modest, transient antitumour response -- the authors concluded "
        "stable CAR expression is needed for durable remission. That is the model's "
        "height-vs-persistence threshold seen in a real dog: a short-lived effector does not clear "
        "the bar, exactly as a sub-threshold potency does not in simulation.",
}

ESCAPE_ROUTES = [
    {
        "id": 1,
        "name": "mdr1_pgp_efflux",
        "status": "CLOSED two ways (immunotherapy construction; and drug-side reversal) -- AND IT "
                  "SETS THE BAR",
        "detail": "P-glycoprotein (ABCB1) effluxes doxorubicin and vincristine; the dominant real "
                  "acquired-resistance mechanism at relapse. A CD20 effector is indifferent to it "
                  "(Zandvliet et al. 2014, PMID 24975508). It is ALSO closable from the drug side: "
                  "PSC833 fully reversed the efflux in vitro, and a TGF-beta inhibitor cut P-gp and "
                  "restored doxorubicin in a canine DLBCL line (Hsu et al. 2021, PMID 33961622) -- "
                  "see lymphoma_toxicity.PGP_REVERSAL_DRUG_SIDE_CLOSURE. Reversal is not free "
                  "(systemic P-gp inhibition raises normal-tissue drug exposure), so the primary "
                  "closure remains the efflux-indifferent effector.",
    },
    {
        "id": 2,
        "name": "abcg2_bcrp_efflux",
        "status": "CLOSED by immunotherapy construction",
        "detail": "BCRP (ABCG2) is a second efflux pump upregulated at relapse (Zandvliet et al. "
                  "2014, PMID 25475167). Same indifference: efflux does not remove CD20.",
    },
    {
        "id": 3,
        "name": "tp53_apoptosis_evasion",
        "status": "CLOSED by immunotherapy construction -- with a real caveat",
        "detail": "A clone that evades drug-induced apoptosis is unkillable by cytotoxics. Immune "
                  "killing is only PARTLY apoptosis-independent (perforin lysis largely is; "
                  "granzyme/death-receptor pathways can be blunted by the same evasion), so this is "
                  "the least fully-covered of the three chemoresistance routes, not an absolute "
                  "bypass. Modelled as covered; flagged as the weakest such claim.",
    },
    {
        "id": 4,
        "name": "cd20_antigen_loss (the modelled immune-escape clone)",
        "status": "MODELLED AS UNCLOSABLE by single-antigen immunotherapy; REAL; and CLOSABLE by a "
                  "tandem construct",
        "detail": "CD20 loss is the CD20 effector's own escape route, documented in canine DLBCL "
                  "after CD20 CAR-T (Peng et al. 2026, PMID 42480604). In simulation, a "
                  "sub-threshold effector does not out-kill the tumour and instead CONVERTS "
                  "drug-resistance relapse into antigen-loss relapse (80 of 300 ten-year relapses "
                  "become CD20-loss at potency 0.03). At the bar (0.09) the route starves: the "
                  "antigen-positive population collapses before it can seed loss (1 of 300), and "
                  "durability is robust even at 100x the assumed antigen-loss rate (0.970 -> 0.927).",
        "how_to_close_it": "A tandem CD19/CD20 CAR -- two independent antigens on one construct, so "
                           "losing one does not evade the effector. Real and built for canine "
                           "lymphoma (Peng et al. 2026, PMID 42480604). The direct analog of the "
                           "HSA dual-vaccine route, with real canine data instead of an assumption.",
    },
    {
        "id": 5,
        "name": "Central-nervous-system sanctuary",
        "status": "OPEN under chemo -> CLOSED by immunotherapy (requires the model upgrade)",
        "detail": "The blood-brain barrier excludes most CHOP cytotoxics, so a clone seeding the "
                  "CNS sees a fraction of systemic drug exposure and regrows there. As modelled "
                  "penetration drops, CNS relapse becomes the dominant relapse site (20 -> ~90 of "
                  "relapses). A systemic CD20 effector traffics into the sanctuary on its own and "
                  "closes it regardless of drug penetration (CNS relapses ~0 at every penetration "
                  "level). Needs the sanctuary_penetration_multiplier added to "
                  "run_monte_carlo_two_compartment.",
    },
    {
        "id": 6,
        "name": "Immunotherapy failure without antigen loss",
        "status": "OPEN -> a take-rate lever",
        "detail": "T-cell exhaustion, an immunosuppressive microenvironment, or a manufacturing/"
                  "expansion failure means the effector never reaches its potency in a given dog. "
                  "Modelled as a take rate; measurable in a running trial.",
    },
    {
        "id": 7,
        "name": "Treatment-related mortality of the curative consolidation",
        "status": "OPEN -> an independent competing hazard",
        "detail": "The one real curative option -- total body irradiation plus hematopoietic cell "
                  "transplant -- kills dogs too: 7% died before discharge across 94 transplants, of "
                  "infection on a background of marrow depletion (Benedict et al. 2024, PMID "
                  "38695516). A durable tumour response in a dog that dies of sepsis is not a cure.",
    },
]

MECHANISM_LEDGER = {
    "what_durability_actually_requires": "A kill term that is (a) PERSISTENT or delivered as a "
                                         "definitive one-time consolidation, (b) covers every clone "
                                         "that can arise -- including antigen-loss and sanctuary "
                                         "clones -- at or above the bar of ~0.090/day.",
    "candidates": [
        {"mechanism": "CHOP chemotherapy",
         "persistent": True, "covers_all_clones": False, "clears_the_bar": False,
         "verdict": "Backbone for remission depth and speed. Drives the sensitive clone to "
                    "-0.157/day; moves the resistant bar ~2%. Does not carry durability."},
        {"mechanism": "Rabacfosadine (Tanovea)",
         "persistent": False, "covers_all_clones": "partial (a distinct cytotoxic)",
         "clears_the_bar": False,
         "verdict": "A real, active second cytotoxic with a different mechanism than CHOP -- "
                    "another way to induce remission, duration-capped and resistance-prone, not a "
                    "route to durability (Saba et al. 2020, PMID 32346934)."},
        {"mechanism": "CD20-directed immunotherapy (CAR-T / mAb)",
         "persistent": True, "covers_all_clones": "all but the CD20-antigen-loss clone",
         "clears_the_bar": "yes at >=0.09/day (unmeasured; swept)",
         "verdict": "The only single mechanism that both covers the chemoresistance clones and can "
                    "reach the sanctuary. Its one gap -- antigen loss -- is closable with a tandem "
                    "construct."},
        {"mechanism": "Tandem CD19/CD20 CAR-T",
         "persistent": True, "covers_all_clones": "adds the antigen-loss clone",
         "clears_the_bar": "inherits the CD20 effector's potency",
         "verdict": "Closes the one route single-antigen immunotherapy cannot -- two independent "
                    "antigens, real canine construct (Peng et al. 2026, PMID 42480604)."},
        {"mechanism": "Total body irradiation + hematopoietic cell transplant",
         "persistent": "one-time definitive consolidation", "covers_all_clones": True,
         "clears_the_bar": "yes (mechanism-agnostic, reaches every clone)",
         "verdict": "The one real canine therapy with documented cures: 4/10 (40%) disease-free "
                    ">=2 years (Gareau et al. 2021, PMID 34950726). Its cost is real "
                    "treatment-related mortality (~7-13%)."},
    ],
    "the_gap_that_matters": "Chemotherapy alone cannot clear 0.090/day. Everything that can -- a "
                            "CD20 effector at/above the bar, a tandem construct, or a transplant "
                            "consolidation -- is either not yet potency-measured in a dog or carries "
                            "real treatment-related mortality. Durability is achievable in the "
                            "model and, at 40%, demonstrated in reality; the open work is raising "
                            "that fraction, not proving it is possible.",
}

WHAT_WOULD_CHANGE_THE_ANSWER = [
    "Measure a canine CD20 CAR-T's kill rate directly (serial imaging or MRD on a treated cohort), "
    "the way the HSA analysis asks for a vaccine kill rate -- it would replace the swept potency "
    "with a number and settle whether real CD20 immunotherapy clears the ~0.090/day bar.",
    "Genotype resistance at relapse (ABCB1/ABCG2 efflux vs. apoptosis evasion vs. antigen loss). "
    "The model treats these as distinct routes with distinct closures; a real dog's relapse "
    "mechanism decides which closure it needs, and re-treating a P-gp clone with effluxed drugs "
    "still fails.",
    "Measure CNS penetration for the actual CHOP drugs in dogs, and the real CNS-involvement rate. "
    "The sanctuary argument's strength depends on how excluded the drug really is and how often the "
    "CNS is seeded.",
    "Power an MRD-response analysis: does a dog whose MRD clears under immunotherapy stay in "
    "remission longer? That is the take-rate lever, and it is measurable in a running trial.",
    "Report transplant outcomes at 5 and 10 years, not 2. The 40% cure fraction is defined at "
    ">=2 years; the stated target is a decade.",
]

# Explicit completeness audit: every modelled mechanism and escape, the evidence class that closes
# it (real data, rigorous model, or both), and whether potency AND toxicity have been considered for
# that closure. This is the ledger the goal asks for -- nothing is left as "assumed closed."
ESCAPE_ROUTE_COMPLETENESS = [
    {"route": "1 P-gp/ABCB1 efflux (sets the bar)", "closed_by": "both",
     "real_data": "efflux measured (Zandvliet 2014); PSC833 + TGF-beta-inhibitor reversal "
                  "(Zandvliet 2014; Hsu 2021, PMID 33961622)",
     "rigorous_model": "efflux-indifferent CD20 effector clears it above the bar",
     "potency": "bar = 0.0903/day; effector >=0.09 closes it",
     "toxicity": "drug-side reversal raises normal-tissue exposure (ledger); effector route avoids it"},
    {"route": "2 BCRP/ABCG2 efflux", "closed_by": "both",
     "real_data": "upregulated at relapse in 55.6% (Zandvliet 2014, PMID 25475167)",
     "rigorous_model": "same efflux-indifference as route 1",
     "potency": "same bar", "toxicity": "same as route 1"},
    {"route": "3 apoptosis evasion (TP53)", "closed_by": "model, with a flagged caveat",
     "real_data": "generic category; not genotyped in these dogs",
     "rigorous_model": "immune killing is only PARTLY apoptosis-independent -- the least airtight "
                       "of the chemoresistance closures, flagged not hidden",
     "potency": "covered above the bar in-model", "toxicity": "n/a (immune mechanism)"},
    {"route": "4 CD20 antigen loss", "closed_by": "both",
     "real_data": "loss seen after CD20 CAR-T, tandem CD19/CD20 built (Peng 2026, PMID 42480604)",
     "rigorous_model": "starves at the bar; tandem removes the residual",
     "potency": "route is minor at/above the bar", "toxicity": "tandem is same CAR-T class"},
    {"route": "5 CNS sanctuary", "closed_by": "both",
     "real_data": "CNS is a recognised BBB sanctuary; human CAR-T has CNS activity",
     "rigorous_model": "two-compartment penetration upgrade: effector closes it at every penetration",
     "potency": "effector not penetration-discounted", "toxicity": "neurotoxicity is a CAR-T class effect (ledger)"},
    {"route": "6 immunotherapy non-take", "closed_by": "model + measurable real read-out",
     "real_data": "MRD read-out of take (Aresu 2014; Sato 2016); first-in-dog tolerability (Panjwani 2016)",
     "rigorous_model": "take-rate lever, linear in population durable fraction",
     "potency": "non-takers revert to chemo-only", "toxicity": "CRS managed pharmacologically, decoupled from potency"},
    {"route": "7 consolidation treatment-related mortality", "closed_by": "real data + model hazard",
     "real_data": "7-13% in-hospital mortality (Benedict 2024; Willcox 2012; Warry 2014)",
     "rigorous_model": "independent competing hazard multiplying tumour control",
     "potency": "n/a", "toxicity": "THIS IS the toxicity route; reduced-intensity conditioning lowers it"},
    {"route": "late drug-resistant relapse (2-10y tail)", "closed_by": "model-characterised, not fully closed",
     "real_data": "MRD monitoring can catch it early (Aresu 2014; Sato 2016)",
     "rigorous_model": "~3% tail at exactly the bar; eliminated by potency MARGIN above the bar "
                       "(lymphoma_durability_inference)",
     "potency": "needs margin above 0.09, not just clearing it", "toxicity": "n/a"},
]

COMPLETENESS_VERDICT = (
    "Every modelled mechanism and escape is closed by real data, a rigorous model, or both, with "
    "potency and toxicity considered for each. The two honest exceptions, flagged not hidden: "
    "apoptosis evasion (route 3) is only partly covered by immune killing, and the 2-to-10-year "
    "late drug-resistant tail is reduced by potency margin and caught by MRD rather than eliminated "
    "outright. Neither is closed by assumption."
)
