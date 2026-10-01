# Lymphoma: the candidate universe (what was searched, what is in the model, what is not)

Written after the user's objection of 2026-09-30: "I don't get how you can claim the goal is completed when even I
know vaccine should be part of the equation, and maybe even stem cell. Go back and be thorough." Rule 9 in
`CLAUDE.md`: a closure claim is only as complete as the candidate universe behind it, so the universe is recorded here.

**Source of everything below:** four literature sweeps, saved in full in `docs/universe/SWEEP_*.md` (vaccines;
stem cell and transplant; every other modality; independent escape audit). Every PMID in those files was fetched from
PubMed by an agent; they are agent-written and should be spot-checked before quoting. Where a sweep could only
read an abstract, the file says so. A fifth sweep (exposures, P-gp status, CD52 source, glucocorticoid IC50s) was cut
off by a rate limit and is being re-run; its items are marked **needs exposure**.

Status words: **IN MODEL** (an agent or escape object, graded) / **EVALUATED, EXCLUDED** (assessed; reason given) /
**NEEDS EXPOSURE** (canine IC50 exists, no exposure, so no derived kill) / **NOT ASSESSABLE** (no kill measurement of
any kind) / **OUTSIDE MODEL** (cannot be expressed as an agent or escape here).

## A. Treatment universe

| class | candidate | status | grade / reason |
|---|---|---|---|
| Cytotoxics | doxorubicin, vincristine, cyclophosphamide (+metronomic), lomustine, rabacfosadine, HD-methotrexate, cytarabine (IT, CRI, pump) | IN MODEL | regimen-calibrated, assumed or derived as before |
| Cytotoxics | actinomycin D, dacarbazine, mitoxantrone, temozolomide, MOMP, DMAC, melphalan, MOC, L-asparaginase | EVALUATED, EXCLUDED | canine rescue series exist (n 19-100) but responses last 14-130 d; no exposure-derived kill; P-gp status unverified. Sequential lines, not closure |
| Glucocorticoid | prednisolone (full, maintenance) | IN MODEL | BRACKET; new escape E1 (GC-receptor loss) now defeats it |
| Targeted | venetoclax, verdinexor, acalabrutinib, hydroxychloroquine | IN MODEL | see ledger |
| Targeted | PI3K-delta (RV1001; duvelisib, idelalisib) | NEEDS EXPOSURE | dog ORR 62-77% but TTP 21-25 d; no IC50; human PTCL ORR ~48% |
| Targeted | HDAC (vorinostat, panobinostat), proteasome (bortezomib, ixazomib), CDK9 (flavopiridol) | NEEDS EXPOSURE | canine IC50s measured (18 nM, 15 nM, 400 nM); no dog exposure found; P-gp/BCRP status mixed |
| Targeted | oclacitinib (JAK1), CDK4/6, ATR, PARP, BET, EZH2, BCL6, MCL1, mTOR, MDM2, azacitidine/decitabine | EVALUATED, EXCLUDED | in vitro only, conflicting or no dog clinical data, no exposure |
| Antibody | anti-CD20 | IN MODEL | MEASURED depletion; trial-stage |
| Antibody | anti-CD52 | NOT ASSESSABLE | one review sentence claims a conditional licence; primary source not found (re-check running) |
| Antibody | anti-CD22/CD19/CD79b/CD25/CD30, ADCs, radioimmunotherapy, CD3-bispecifics | NOT ASSESSABLE | reagents or imaging only in dogs; no therapy data |
| Antibody | anti-CD47 / SIRP-alpha-Fc + opsonin | NOT ASSESSABLE | conserved axis; mouse xenograft cures; human DLBCL ORR 40%; no dog trial or kill rate. Escape E10 added instead |
| Checkpoint | anti-PD-1 / PD-L1 | IN MODEL, re-graded | **zero objective responses in 15 dogs with lymphoma (gilvetmab, PMID 42247661)**; the model's ASSUMED 0.04 /day is contradicted |
| Checkpoint | CTLA-4, LAG-3, TIM-3 | NOT ASSESSABLE | no canine antibody or trial found |
| Cell therapy | CD20 CAR-T, tandem CD19/CD20, PD-1/CD28 switch, persistence-engineered, CD7, CD5+CD7 | IN MODEL | assumed / transferred / buildable |
| Cell therapy | autologous T-cell add-back after CHOP | **IN MODEL (new)** | OUTCOME: tumour-free survival 338 vs 71 d, n=8 vs 12 historical; k = 0.071 /day |
| Cell therapy | NK, CAR-NK, gamma-delta, TIL, iNKT, allogeneic CAR-T, CAR-macrophage | NOT ASSESSABLE | no dog lymphoma data (NK/iNKT only in solid tumours or healthy dogs) |
| Cytokine | canine IL-15, IFN-gamma, IL-2/12 | EVALUATED, EXCLUDED | IL-15 + chemo ORR 77.8% vs 57.9% (weak, n small); IFN-gamma no benefit |
| Vaccine | autologous tumour vaccine (APAVAC) | **IN MODEL (new)** | OUTCOME: TTP ratio 2.55 gives 0.055 /day; **3-year survival 10% vs 8%: no tail effect**; antigen-presentation-vulnerable; no persister or brain credit |
| Vaccine | dTERT genetic vaccine (3 trials) | EVALUATED, EXCLUDED from model | survival gain but **PFS 11.4 vs 11.3 weeks** (k ~ 0); controls historical or owner-selected; TERT is not tumour-specific |
| Vaccine | CD40-B RNA vaccine | EVALUATED, EXCLUDED | TTP ratio 1.12 (k ~ 0.01); 3 vaccinated dogs alive 959-1287 d (longest vaccine tail seen) |
| Vaccine | hGM-CSF cell vaccine, DC vaccines | EVALUATED, EXCLUDED | randomised null; no DTH response |
| Vaccine | idiotype, DNA/xenogeneic, neoantigen/mRNA, TLR9 in situ, oncolytic virus | NOT ASSESSABLE in dogs | human idiotype Phase 3s negative or marginal; no canine lymphoma trial; VSV in 2 dogs transient |
| Transplant | autologous TBI + HSCT | IN MODEL | OUTCOME for durability; radiation kill DERIVED (LQ from canine lines); B 5/15 and T 2/13 long remissions |
| Transplant | **allogeneic DLA-identical HCT (graft-versus-lymphoma)** | **EVALUATED; best dog durability tail, not composable** | 8 of 9 first-remission dogs >4 y without lymphoma death, longest 2920 d (~8 y), n=10-15, 4 centres; needs a DLA-identical donor; TRM 7-55% by era; no CNS or T-cell data; MHC loss is an escape route. Kept as an empirical route with no kill rate, so it cannot be put in the kill-rate model |
| Transplant | haploidentical, cord blood, DLI | NOT ASSESSABLE | lethal GVHD in research series; no client-dog data |
| Stem-cell concept | "cancer stem cell" / lymphoma-initiating cell | IN MODEL as escape E5 | measured hierarchy; efflux-high; modelled as non-dividing AND pump-high (conservative) |
| Stem-cell product | mesenchymal cells, iPSC products, gene-modified HSC | EVALUATED, EXCLUDED | no anti-lymphoma role; MSC did not prevent GVHD; iPSC only red cells/platelets |
| Radiation | craniospinal, half-body, TBI | IN MODEL | derived from canine clonogenic survival; half-body has real 2- and 5-year remission data |
| Delivery | continuous intrathecal pump | IN MODEL (buildable) | transfer |
| Sanctuary | eye/uvea, testis | OUTSIDE MODEL | 11.6% ocular involvement in disseminated necropsy dogs; no access data. Not modelled |

## B. Escape universe

| ID | escape | status |
|---|---|---|
| 1-14 | the original 14 (P-gp, BCRP, TP53/apoptosis, CD20 loss, CD19 loss, BCR/NF-kB, PI3K/AKT, persister, autophagy, exhaustion, lineage switch, antigen-presentation loss, MGMT, CD7 loss) | IN MODEL |
| E1 | glucocorticoid-receptor loss (NR3C1) | IN MODEL (new). Measured in dogs: resistance 'essentially universal', median onset 68 d |
| E2 | nucleoside-activation loss (dCK) | IN MODEL (new). Human data (50% of primary cytarabine failures); defeats every cytarabine arm |
| E3 | topoisomerase-IIa loss | IN MODEL (new). Mouse data |
| E4 | BCL2-family rewiring | IN MODEL (new). Defeats venetoclax |
| E5 | quiescent efflux-high lymphoid progenitor | IN MODEL (new). Measured hierarchy in dogs; the conjunction (non-dividing + pump) is what most agents miss |
| E6 | niche / adhesion protection | SENSITIVITY ONLY. Real effect is partial; the model can only express a total defeat |
| E7 | antigen-low (sub-threshold) | IN MODEL (new). Human data |
| E8 | XPO1 C528S | IN MODEL (new). Not yet seen clinically |
| E9 | antifolate transport loss | IN MODEL (new). Human data; defeats the brain arm's methotrexate |
| E10 | macrophage checkpoint CD47/SIRP-alpha | IN MODEL (new). Prevalence unknown |
| E11 | eye/uvea and testis compartments | OUTSIDE MODEL |
| E12 | unattributed cross-resistant relapse | OUTSIDE MODEL. A residual that bounds every closure claim; 55.6% of CHOP-treated dogs become drug-resistant (PMID 25475167) and only part is attributed |
| E13-E19 | epigenetic plasticity, second cancers and clonal haematopoiesis, asparaginase, tubulin, BTK C481S, weak immune modifiers, host/logistic | OUTSIDE MODEL as separate lineages (parameters or out-of-model hazards) |

**Corrections found by the sweeps.** (1) Gareau 2021: adoptive T cells were NOT shown to add benefit to transplant; the
earlier statement here and on the plain-language page was wrong and is fixed. (2) The "testis-to-brain relapse" case
(PMID 37265807) is a spermatic-cord lymphoma that received no chemotherapy. (3) Anti-PD-1 has no objective responses in dog
lymphoma. (4) Venetoclax P-gp status is mixed; it is flagged as a substrate in the model (conservative). (5) TP53
loss is MEASURED in dogs (16-27%), not only transferred.

## C. Results with the widened universe

(Filled in from the search below.)
