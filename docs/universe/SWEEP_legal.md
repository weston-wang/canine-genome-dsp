# Lawful availability of every closing agent for a pet dog (2026-10-06)

The user: "I know there's that rule where human meds can be used for pets under exceptions. Make sure the human ones you cited qualify."

## The rule, verified
US: the Animal Medicinal Drug Use Clarification Act of 1994, implemented at **21 CFR Part 530**. Extra-label use is permitted for
**FDA-approved new animal drugs and FDA-approved human drugs**, by or on the lawful order of a licensed veterinarian within a valid
veterinarian-client-patient relationship. FDA's own statement of the part's purpose is that it establishes the conditions for extra-label use
"of Food and Drug Administration approved new animal drugs and approved new human drugs".

**The consequence that matters here: extra-label use does not make an unapproved drug lawful.** A product approved only in a foreign
country is not an FDA-approved drug, so there is no extra-label route for it. (Sources: FDA's AMDUCA page and "The Ins and Outs of
Extra-Label Drug Use in Animals"; 21 CFR 530 subpart A. The prohibited-drug list at 530.41 does not bear on any agent used here.)

## Agent by agent

| agent | status | authority | obstacle |
|---|---|---|---|
| **verdinexor** (Laverdia-CA1) | **approved ANIMAL drug** | FDA conditional approval Jan 2021, **full approval Jan 2026**; label is oral tablets twice weekly at home, at least 72 h apart, for canine lymphoma | none; sustained dosing is **on-label**, which is why the 6-month body programs sit on the firmest ground of anything in this project |
| **methotrexate, preservative-free injection** | approved HUMAN drug, extra-label in the dog | FDA-approved, and **intrathecal is a labelled route** in the human product; the preserved formulation contains benzyl alcohol and must never be given intrathecally | the preservative-free product must be specified; intrathecal methotrexate + cytarabine is reported in 112 dogs (PMID 25041580) |
| **cytarabine** injection (infusion or subcutaneous) | approved HUMAN drug, extra-label | FDA-approved | published in dogs (PMIDs 31769013, 22943060) |
| prednisolone | approved ANIMAL drug | veterinary products | none |
| romidepsin | approved HUMAN drug, extra-label | the relapsed/refractory PTCL indication was **withdrawn in 2021-22** after Ro-CHOP missed its endpoint, but the drug **remains approved and marketed for cutaneous T-cell lymphoma**, so it is still an approved human drug | cost; not load-bearing (dropping it changes no window) |
| hydroxychloroquine | approved HUMAN drug, extra-label | FDA-approved generic | not load-bearing |
| lomustine, doxorubicin, vincristine, cyclophosphamide, thiotepa, high-dose methotrexate, venetoclax, HDAC and BTK inhibitors | approved HUMAN drugs, extra-label | FDA-approved | standard veterinary oncology for the first four |
| rabacfosadine (Tanovea) | approved ANIMAL drug | NADA 141-545 | pulmonary fibrosis cap |
| matched-donor transplant with total-body irradiation; whole-brain or craniospinal radiotherapy | **procedures**, not drug approvals | performed at referral and veterinary radiation-oncology centres | a DLA-identical littermate (about 25% per sibling); anaesthesia per fraction; cost |
| **cytarabine ocfosfate** (Starasid) | **NO US APPROVAL** | approved only in **Japan** | **no lawful extra-label route in the US.** Removed from every program |
| **canine anti-CD20 antibody** | **investigational only** | Blontress (AT-004) conditionally licensed 2012, fully licensed 2015, **discontinued 2017**; the Elanco 1E4 antibody is investigational | **no licensed canine anti-CD20 product exists.** Removed from every program |
| CAR-T, CD3xCD20 engager, implanted intrathecal pump, autologous vaccines, T-cell add-back | not products | trials or specifications | not counted |

## What this changed in the model
Two agents the earlier programs leaned on had no lawful route, and both were load-bearing: the oral cytarabine prodrug carried the
B-cell brain in section I, and the anti-CD20 antibody carried the B-cell body in section F. The programs were rebuilt from lawful agents only
(`lymphoma_sustained.lawful_pool`, `LAWFUL_PROGRAMS`) and all four cases still close; see section K.

## Not checked
EU and UK: the prescribing cascade (Regulation (EU) 2019/6 Articles 112-114) has an import limb that may permit a product authorised in a
third country, so cytarabine ocfosfate could have a route there. Not verified, so it is not relied on. DEA scheduling, state practice acts,
hazardous-drug handling rules for cytotoxics, and compounding from bulk substances (FDA GFI #256) were not examined.
