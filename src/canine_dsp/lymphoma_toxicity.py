"""Toxicity, considered alongside potency, for every agent in the canine-lymphoma closure stack.

Potency without toxicity is not a plan. This module records, for each agent, its real documented
toxicity (with citations) and how that toxicity interacts with the potency the durability argument
needs -- because the interaction differs by agent, and the difference is the point:

  * The durability carrier (CD20 immunotherapy) has LOAD-BEARING potency (a cliff at the bar) but a
    toxicity (cytokine release) that is managed pharmacologically WITHOUT lowering that potency, so
    its efficacy and its toxicity are decoupled.
  * Chemotherapy is de-ratable for toxicity in isolation (it was never carrying durability) but is
    PARTLY load-bearing inside the curative combination, because its cytoreduction depth lowers the
    burden the immune effector must clear -- a genuine potency/toxicity tension the model quantifies.
  * The consolidation (total body irradiation + transplant) has a toxicity -- treatment-related
    mortality -- that is a direct competing hazard, the one place toxicity subtracts straight from
    the cure (modelled in lymphoma_open_route_closure.TRANSPLANT_TRM).

Every numeric figure is recomputed from the engine by tests/test_lymphoma_inference_and_toxicity.py.
See docs/LYMPHOMA_DURABLE_RESPONSE.md section 9. All PMIDs verified against PubMed.
"""

# Per-agent toxicity ledger. Real, cited, and paired with the potency role so the trade-off is
# explicit rather than asserted.
TOXICITY_LEDGER = [
    {
        "agent": "CHOP (cyclophosphamide, doxorubicin, vincristine, prednisone)",
        "toxicity": "myelosuppression (neutropenia) and gastrointestinal signs; hospitalisation for "
                    "adverse events was itself a negative prognostic factor, i.e. real and "
                    "sometimes serious (Curran & Thamm 2015, PMID 26279153). Doxorubicin carries a "
                    "cumulative-dose cardiotoxicity ceiling.",
        "potency_role": "response depth/speed; partly load-bearing for durability in the combination",
        "de_ratable": "yes in isolation (durability-neutral); NO for free in the curative combo -- "
                      "de-rating costs 10-year durability because cytoreduction depth matters",
    },
    {
        "agent": "Rabacfosadine (Tanovea)",
        "toxicity": "gastrointestinal and dermatologic signs, and -- the serious one -- DELAYED "
                    "grade-5 (fatal) pulmonary fibrosis in a small number of dogs across two "
                    "prospective trials (Thamm et al. 2017, PMID 28370378; Saba et al. 2020, PMID "
                    "32346934). A real cumulative-exposure ceiling.",
        "potency_role": "an optional second cytotoxic; not a durability mechanism",
        "de_ratable": "yes -- and the pulmonary-fibrosis ceiling caps total exposure regardless",
    },
    {
        "agent": "CD20 CAR-T / antibody immunotherapy",
        "toxicity": "cytokine release syndrome and neurotoxicity are the class toxicities in humans; "
                    "B-cell aplasia is on-target/off-tumour. First-in-dog CD20 CAR-T was WELL "
                    "TOLERATED (Panjwani et al. 2016, PMID 27401141). Critically, cytokine release "
                    "is managed pharmacologically (anti-IL-6, corticosteroids) WITHOUT reducing the "
                    "CAR's kill.",
        "potency_role": "THE durability carrier; potency is fully load-bearing (a cliff at the bar)",
        "de_ratable": "no -- and it does not need to be: its toxicity is decoupled from its potency, "
                      "unlike a small molecule where lowering dose lowers both",
    },
    {
        "agent": "Total body irradiation + hematopoietic cell transplant",
        "toxicity": "treatment-related mortality of ~7-13% (mostly infection on marrow depletion; "
                    "Benedict et al. 2024, PMID 38695516; Willcox et al. 2012, PMID 22882500; Warry "
                    "et al. 2014, PMID 24467413), plus a long-term risk of therapy-related "
                    "myeloid neoplasia from the radiation.",
        "potency_role": "one-time definitive consolidation; mechanism-agnostic",
        "de_ratable": "reduced-intensity conditioning lowers the toxicity (and is a durability lever "
                      "in its own right); the residual TRM is modelled as a competing hazard",
    },
    {
        "agent": "Persistent second agent (metronomic chemo / P-gp or TGF-beta inhibitor)",
        "toxicity": "metronomic cyclophosphamide carries sterile haemorrhagic cystitis risk; a P-gp "
                    "inhibitor raises exposure of co-administered drugs (the mechanism that makes it "
                    "useful is also a toxicity multiplier).",
        "potency_role": "lowers the bar from the other side (lymphoma_gap_closure.LOWER_THE_BAR)",
        "de_ratable": "swept; must be chosen to sidestep P-gp efflux, which constrains the options",
    },
]

# Finding 1: chemotherapy dose de-rating is durability-neutral WHEN CHEMO IS THE ONLY AGENT -- it
# was never carrying durability, so lowering it for toxicity costs response depth, not the 10-year
# figure (which is low regardless). Recomputed by the test module.
CHEMO_DERATING_CHEMO_ONLY = {1.0: 0.180, 0.6: 0.173, 0.4: 0.173, 0.2: 0.123}

# Finding 2: INSIDE the curative combination (CD20 effector at the bar), chemo's cytoreduction
# depth IS partly load-bearing -- de-rating CHOP for toxicity now costs 10-year durability, because
# a shallower induction leaves more burden and more late resistant-clone seeding for the immune
# effector to overcome. This is the real potency/toxicity tension: you want deep induction, and
# CHOP's own myelosuppression caps how deep you can safely go.
CHEMO_DERATING_IN_COMBINATION = {1.0: 0.970, 0.6: 0.850, 0.4: 0.737}

# Finding 3: the durability carrier's potency is a cliff at the bar -- it cannot be de-rated the way
# a toxic small molecule can, which is why the decoupling of its toxicity from its potency matters.
IMMUNOTHERAPY_POTENCY_IS_LOAD_BEARING = {0.12: 1.000, 0.09: 0.970, 0.06: 0.240}

TOXICITY_FINDINGS = {
    "the_asymmetry": "Potency and toxicity trade off differently for each agent. For the durability "
                     "carrier the trade-off is broken in the patient's favour -- its toxicity is "
                     "managed without touching its potency. For chemotherapy the trade-off is real "
                     "and quantified -- deeper induction buys durability but costs toxicity. For the "
                     "consolidation the toxicity is a direct competing hazard.",
    "why_this_matters_for_the_target": "A 10-year-durability regimen cannot be assembled by summing "
                                       "potencies and ignoring toxicity: the model says the winning "
                                       "combination needs a deep (hence toxic) induction AND a "
                                       "load-bearing immune effector AND a consolidation with its "
                                       "own mortality. The realistic optimisation is to make the "
                                       "induction as deep as tolerated, keep the immune effector "
                                       "above the bar (managing its toxicity pharmacologically), and "
                                       "reduce the consolidation's intensity as far as durability "
                                       "allows -- not to trade any one of them away.",
}

# Route-1 closure from the DRUG side (complementing the immunotherapy-construction closure): real,
# disease-specific evidence that P-glycoprotein-mediated doxorubicin resistance in canine DLBCL can
# be reversed pharmacologically -- so the efflux clone that sets the bar is closable by chemo too,
# not only by an effector that ignores it. This strengthens route 1 from "immunotherapy doesn't
# care about efflux" to "efflux itself is druggable in this disease."
PGP_REVERSAL_DRUG_SIDE_CLOSURE = {
    "in_vitro_reversal": "Zandvliet et al. 2014 (PMID 24975508): the P-gp inhibitor PSC833 fully "
                         "reversed doxorubicin and vincristine resistance in a canine lymphoid line.",
    "disease_specific_chemosensitization": "Hsu et al. 2021 (PMID 33961622, "
        "DOI 10.1371/journal.pone.0250013): in a doxorubicin-resistant canine DLBCL line, a "
        "TGF-beta inhibitor increased chemo-sensitivity and intracellular doxorubicin accumulation "
        "AND decreased P-glycoprotein expression -- a real, disease-specific route to lowering the "
        "efflux clone's resistance from the drug side.",
    "caveat": "Both are in vitro. Systemic P-gp inhibition also raises normal-tissue drug exposure "
              "(a toxicity multiplier, see the ledger), so this closure is not free -- it trades "
              "efflux reversal against wider toxicity, which is exactly why the model still routes "
              "durability through the efflux-indifferent immune effector as the primary mechanism.",
}
