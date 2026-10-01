# Lymphoma: the candidate universe (what was searched, what is in the model, what is not)

Written after the user's objection of 2026-09-30: "I don't get how you can claim the goal is completed when even I
know vaccine should be part of the equation, and maybe even stem cell. Go back and be thorough." Rule 9 in
`CLAUDE.md`: a closure claim is only as complete as the candidate universe behind it, so the universe is recorded here.

**Source of everything below:** four literature sweeps, saved in full in `docs/universe/SWEEP_*.md` (vaccines;
stem cell and transplant; every other modality; independent escape audit). Every PMID in those files was fetched from
PubMed by an agent; they are agent-written and should be spot-checked before quoting. Where a sweep could only
read an abstract, the file says so. A fifth sweep (exposures, P-gp status, CD52 source, glucocorticoid IC50s) was cut
off by a rate limit and resumed and finished; its output is saved as `docs/universe/SWEEP_pk.md`; items still missing are marked **needs exposure**.

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
| Targeted | PI3K-delta (RV1001; duvelisib, idelalisib) | NOT ASSESSABLE as a kill rate | dog ORR 62-77% but TTP 21-25 d; **no canine IC50 found for any**; inversion: duvelisib would need a canine free IC50 <= ~160 nM to reach the 0.09 /day bar; duvelisib and idelalisib are P-gp/BCRP substrates (labels) |
| Targeted | panobinostat, vorinostat, bortezomib | **IN MODEL (new), TRANSFER** | canine IC50 x free human label exposure: panobinostat 0.115 /day (range 0.017-0.38; P-gp and BCRP substrate; brain Kp,uu 0.2-0.3 in mouse); vorinostat 0.026 (0.005-0.09; not a pump substrate; assay duration assumed); bortezomib 0.048 (0.026-0.13; below the bar everywhere). Dog PK not found for any |
| Targeted | ixazomib, flavopiridol, OSU-HDAC42 | EVALUATED, EXCLUDED | ixazomib 0.001-0.024 /day; flavopiridol IC50 only bounded above (<=400 nM) so no kill derivable; OSU-HDAC42 no exposure |
| Targeted | oclacitinib (JAK1), CDK4/6, ATR, PARP, BET, EZH2, BCL6, MCL1, mTOR, MDM2, azacitidine/decitabine | EVALUATED, EXCLUDED | in vitro only, conflicting or no dog clinical data, no exposure |
| Antibody | anti-CD20 | IN MODEL | MEASURED depletion; trial-stage |
| Antibody | anti-CD52 (AT-005, Tactress) | EVALUATED, EXCLUDED | **licensed (conditional 2014, full 2016) but the only peer-reviewed RCT (n=49, with L-CHOP) showed no benefit: median PFS 64 d vs 103 d placebo, p=0.82; the authors report the antibody lacks binding specificity for CD52 and it is off the market (PMID 36329876).** Not a usable T-lineage antibody |
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

**Claim, stated as rule 9 requires:** within a catalogue of about 28 agent entries (the count differs by lineage and compartment) and 23 escapes (the original 14 plus 9 from
the audit; adhesion protection run separately as a sensitivity), at sound grades (measured, derived, outcome-calibrated or
transferred with a written basis), searching every combination of up to 4 agents (5 for the first pass), requiring
closure of EVERY escape whether or not it is likely present, and counting a regimen as closing only if the treatment
clock clears every lineage inside the evidence-limited windows. All of it is MODELLED. Nothing here is shown in a dog.

| compartment | agents allowed | does any combination close every escape? |
|---|---|---|
| B-cell body | licensed + off-label | **No.** Best margin +0.012 /day, response then relapse from the quiescent efflux-high progenitor (E5) |
| B-cell body | + trial-stage | **Yes, 39 combinations of 3-4 agents.** All 3-agent ones contain the autologous vaccine, whose credit is the weakest input here. A 4-agent one without the vaccine also clears: prednisolone + anti-CD20 + HCQ + verdinexor (margin +0.201) |
| B-cell body | + buildable (CAR-T specification) | Yes, 304 combinations, down to 2 agents (verdinexor + persistence-engineered CAR-T). The CAR-T does not exist |
| T-cell body | licensed + off-label, or + trial | **No** (best +0.012) |
| T-cell body | + buildable | Yes, 166 combinations, all containing the CD7 or CD5/CD7 CAR-T, which does not exist |
| **Brain, B-cell** | **any tier, including buildable** | **No.** Best margin +0.062 /day; response then relapse from E5 (never clears inside the window) |
| **Brain, T-cell** | **any tier, including buildable** | **No.** Same |

**What changed from the first result and why.** The earlier four-part B-cell program (HCQ + verdinexor + continuous
intrathecal cytarabine + anti-CD20) no longer closes. Two audit escapes break it. E5 (a quiescent, pump-high progenitor
that is measured in dogs as a hierarchy) is missed by every division-gated agent and every pump substrate, which leaves
only prednisolone, the antibody and CAR-T able to reach it, and almost none of those reach the brain. E2 (loss of the enzyme
that activates cytarabine) removes the brain's cytarabine arm on its own. The first result was closure within 14 escapes,
and that was its limit.

**Vaccine, tested as asked.** The autologous vaccine (OUTCOME 0.055 /day, from a 2.55x time-to-progression ratio against weak
controls) is load-bearing in every 3-agent B-cell body set. The antibody + HCQ + vaccine set clears the clock only at full vaccine credit (margin +0.064); at 0.5, 0.25 and 0 of that credit it
does not clear (+0.036, +0.022, +0.009), so closure there rests on a credit that the
dog data (3-year survival 10% vs 8%) do not support. The vaccine gives nothing against persisters or the brain
by construction.

**Radiation sensitivity.** The model treats radiation as division-gated (conservative). Re-running with radiation not division-gated (lymphoid cells die by interphase apoptosis, so this is physically defensible) changes nothing: the brain still does not close for B- or T-cell disease at any tier. This was checked after seeing the result, so it is reported as a sensitivity and was not used to choose the headline.

**Fault tolerance.** None of the body sets tested clears with all potencies halved, and none clears after removing any one agent
(the same weakness as before, now across the widened set).

**Design requirement for the brain (and for any closure).** Adding one hypothetical agent that is not division-gated, not a
pump substrate and not dependent on CD20/CD19 to HCQ + verdinexor (+ the intrathecal pump for the brain) closes the widened set
only if it kills at least **0.10 /day** with full access, **0.19 /day** at half access (brain), and **not at all at 10% access**.
No existing agent in the sound pool meets that. A T-cell effector that crosses the barrier and does not need a pump-
vulnerable or division-gated mechanism is the class that would. **Allogeneic transplant with graft-versus-lymphoma is the only real-data route
in this universe that plausibly belongs to that class** (T-cell mediated, not division-gated, not a pump substrate, not
dependent on CD20/CD19; 8 of 9 first-remission DLA-identical dogs lived over 4 years without lymphoma death). Whether it
delivers 0.10 /day in the brain is untested: there is no canine CNS or minimal-residual-disease data, no T-cell-lymphoma series,
it needs a DLA-identical donor, and 7-55% of transplanted dogs die of the procedure depending on era.

**Exposure-transfer drugs (resumed sweep).** Adding panobinostat, vorinostat and bortezomib at transferred exposures changes none of the rows above: the brain still does not close at any tier, the T-cell body still needs the unbuilt CD7 CAR-T, and the minimal B-cell sets are unchanged. They are pump substrates (panobinostat, bortezomib) or sub-bar (vorinostat 0.026), so none reaches the quiescent efflux-high progenitor (E5) at a useful rate.

**Other findings from the resumed sweep.** (a) The "~15x disagreement" in the prednisolone bracket is an artefact of mixing an Emax (35% growth inhibition plateau by ~1 uM at 72 h in GL-1) with an IC50 (44 uM in line 1771, duration unstated); the two are not the same measurand. Prednisolone remains graded BRACKET at the low end. (b) Venetoclax is a P-gp and BCRP substrate by label and clinical interaction studies (not shown in canine cells); the model already flags it as a substrate. Venetoclax T-cell derived kill 0.07-2.1 /day (central 0.52), free fraction the hinge. (c) The anti-CD52 antibody is resolved (above).

**Not yet done.** (1) PI3K-delta and flavopiridol kill rates (no canine IC50). (2) Anything outside the model:
unattributed multidrug resistance (E12, which bounds every closure claim), eye and testis compartments, late second cancers.
(4) A real answer on 10 years: no dog has 10-year follow-up; the longest transplant survivor is about 8 y.
