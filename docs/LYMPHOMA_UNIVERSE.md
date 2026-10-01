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


## D. Closing the brain (2026-10-01; the user: "So your goal isn't met yet, close the brain ones")

**What was missing from the universe:** sanctuary-site delivery, the class named in rule 9 of `CLAUDE.md` and skipped in the first pass.
Two further sweeps were run: regional (spinal-fluid) delivery (`docs/universe/SWEEP_regional.md`) and human brain-lymphoma regimens
(`docs/universe/SWEEP_cnsregimens.md`). They added four candidates, all graded below; none has a dog trial.

| candidate | status | grade and basis |
|---|---|---|
| anti-CD20 antibody given into the ventricles/CSF (B-cell) | IN MODEL (new, buildable route) | TRANSFER. Human intraventricular rituximab cleared CSF lymphoma cells within hours with CSF complement activation (PMID 24190981); CSF access 1.0 (systemic route 0.002); potency = the measured canine depletion rate 0.099 /day; duty 2/7 (about a day of CSF coverage per dose). Quiescent-progenitor kill NOT measured; deep-parenchyma access unmeasured |
| tandem CD19/CD20 CAR-T into the CSF (B-cell); CD7 and CD5+CD7 CAR-T into the CSF (T-cell) | IN MODEL (new, buildable) | TRANSFER-OUTCOME. Intraventricular/intrathecal CAR-T reaches CSF in human CNS tumours; potency is the model's 0.12 /day (an assumed in-vivo kill); CSF persistence 1 to 7+ days per dose, so the duty is the swept unknown; neurotoxicity budget 0.30 |
| high-dose thiotepa consolidation with autologous stem-cell rescue | IN MODEL (new, human regimen) | OUTCOME. Human CNS lymphoma: 3-year PFS 78% (n=114 transplanted), 8-year event-free 67%; implies an effective brain kill of 0.13-0.21 /day over ~115 days (program average; low end used). Default is conservative: division-gated and a pump substrate (transporter status not found). No canine thiotepa data |
| intrathecal glucocorticoid; depot cytarabine (DepoCyt) | EVALUATED, EXCLUDED | glucocorticoid defeated by receptor loss (E1, measured in dogs); depot cytarabine is division-gated and dCK-dependent (E2). Neither can close the quiescent-progenitor escape however well delivered |
| lenalidomide, BTK inhibitors, intrathecal chemotherapy, whole-brain radiotherapy | EVALUATED, EXCLUDED as closers | responses last months; whole-brain radiotherapy has durable human data but real neurotoxicity (cognitive decline 64% at 8 y in the transplant comparison) and radiation is already in the model |

**Result (model, sound grades, every one of the 23 escapes required closed, up to 4 agents).**
- **B-cell brain:** closes, conditional on the CSF CAR-T being active in the CSF for at least about 35% of each dosing interval (minimum duty 0.35, found by bisection). At the conservative 1/7 duty exactly one 4-agent set clears, with margin +0.015 /day and last lineage gone by day 178: the continuous intrathecal cytarabine pump + a persistence-engineered systemic CAR-T + the CSF antibody + the CSF tandem CAR-T. At duty 0.5: 29 sets (smallest 3 agents: pump + systemic CAR-T + CSF tandem CAR-T; best margin +0.115 /day, clear by day 112). At duty 1.0: 403 sets, down to 2 agents (pump + CSF tandem CAR-T).
- **T-cell brain:** closes under the same condition (minimum duty 0.35). At the conservative 1/7 duty nothing clears. At 0.5: 139 sets; at 1.0: 1,240.
- **Thiotepa route:** if thiotepa is taken as acting on dormant cells and not being pumped out (the implication of its human cure plateau, but not shown), a 3-agent brain set that does not need the CSF CAR-T clears: pump + systemic CAR-T + thiotepa (28 B-cell sets, 24 T-cell sets). With the conservative default thiotepa adds nothing.
- **Fault tolerance: none.** Every clearing set fails with all potencies halved and fails with any one agent removed, at every duty tested.
- **What every clearing set depends on that does not exist:** the CSF CAR-T (or the systemic persistence-engineered/CD7 CAR-T), and the continuous intrathecal pump. The CAR-T potency 0.12 /day is itself an assumed in-vivo kill. The weakest escape in every best set is E2 (loss of the enzyme that activates cytarabine), carried by the other agents.

**So the brain is closed in the model only conditionally.** The conditions, each of which is a measurement a trial could make:
1. CAR-T persistence in the CSF of at least about 2.5 days out of every 7 (human intrathecal cells last 1 to 7+ days; the one monkey measurement is 24 hours).
2. A CAR-T kill rate in vivo of about 0.12 /day, now assumed.
3. Access of the CSF-delivered cells and antibody to the brain parenchyma, unmeasured; the evidence reaches the leptomeninges and perivascular spaces (canine neural lymphoma is meningeal, perivascular and periventricular, PMID 27511313, which favours the route) but not deep tissue, and intravascular lymphoma (PMID 36329600) cannot be reached from the CSF at all.
4. Chronic CSF access in dogs for years (reservoir infection about 0.2% per device-year in one human series, 100-fold spread); no decade-scale data exists.
5. CNS neurotoxicity from CAR-T within budget (30-100% any grade in human CNS trials, grade 3 or higher up to ~30%).


## E. Human-grounded CAR-T inputs and the joint programs (2026-10-01; /goal: "keep going by more research or modeling to fully close every mechanism and escape then. I know car t has human results for CNS")

**The user was right that human CNS CAR-T data exist, and they replace what had been assumed.** Two sweeps (`docs/universe/SWEEP_cart_human.md`,
`SWEEP_cart_kill.md`) gave:

| input | was | now | grade |
|---|---|---|---|
| CAR-T kill rate in vivo | 0.12 /day, ASSUMED | low 0.12 / **central 0.35** / high 1.1 | TRANSFER from human models (Kimmel 2021 PMID 33757357; Singh 2021 PMID 33565700; Kalos 2011) |
| CAR-T brain access, IV route | 0.5, assumed | 0.5 (range 0.1-1.0) | OUTCOME / TRANSFER: CR in CNS lymphoma 47-57% vs 40-54% systemic (ratio ~1), durability about half; CSF:blood concentration ratio ~0.01-0.03 |
| CSF-delivered CAR-T duty | 1/7, one monkey | low 0.15 / **central 0.4** / high 0.7 | derived from human CNS-tumour trials (each dose active 5-14 d; PMIDs 38454126, 39775044, 40451950) |
| CAR-T on non-dividing cells | assumed not gated | not division-gated | TRANSFER (in vitro, mouse, primate; human CLL clearance at 0.1-1%/day cell turnover), no human G0 measurement |
| neurotoxicity budgets | assumed | CNS_LOCAL 0.18 (0.10-0.30), immune-mediated 0.17 | MEASURED human, scales with burden, so the low end is used for early detection |
| 5-10 year durability | unknown | ~30% of all treated LBCL, ~60% of responders, 92% 5-year OS if event-free at 2 years, no relapse after 5.4 years (n=38) | MEASURED / TRANSFER: supports "2 years disease-free implies 10 years" in humans, not proven in dogs |

**Result at the central human-grounded inputs (kill 0.35 /day, CSF duty 0.4), every one of the 23 escapes required closed, toxicity charged on
the UNION of the whole program, body and brain evaluated together, clock inside the evidence-limited windows (`src/canine_dsp/lymphoma_joint.py`):**

| program | agents | body margin | brain margin | halved potency | any one agent removed |
|---|---|---|---|---|---|
| B-cell, 7 agents | anti-CD20 antibody, hydroxychloroquine, persistence-engineered canine-binder CAR-T, autologous tumour vaccine, panobinostat, continuous intrathecal cytarabine pump, CSF tandem CD19/CD20 CAR-T | +0.36 | +0.30 | **clears** | **clears** |
| B-cell, 8 agents | the above with verdinexor and cytarabine CRI in place of panobinostat | +0.39 | +0.27 | clears | clears |
| T-cell, 5 agents | hydroxychloroquine, intrathecal pump, CD7 CAR-T, CD5+CD7 dual CAR-T, verdinexor | +0.67 | +0.34 | **clears** | **clears** |
| T-cell, 8 agents | the above with CSF CD7 and CD5+CD7 CAR-T and venetoclax | +0.43 | +0.37 | clears | clears |

At the LOW inputs (kill 0.12 /day, duty 0.15) the B-cell programs do not clear and the T-cell 5-agent program clears but is not fault tolerant; at kill 0.12 and duty 0.4
both clear but fail halving. So **the closure depends on the CAR-T kill rate reaching its central human value, which in dogs is set by expansion**: 0.12 /day needs about
6.5e7 CAR-T cells, 4-90 times the doses given to dogs so far, and dog CAR-T has not yet shown efficacy (Mol Ther 2026, PMID 41376156).

**Calibration against the human data.** A systemic CD20-directed CAR-T alone does NOT close the brain in the model (margin -0.09 /day; CD20 loss and antigen-low are
uncovered), which agrees with the human result that CAR-T alone leaves 59% CNS relapse by 24 months (PMID 40400509) and that thiotepa-based transplant beat it (PFS HR 0.45, PMID 41490516).

**What "closed" means here, and what is still outside it.**
1. Closed = the model, with 23 escapes and the sound-grade agents, shows every lineage cleared inside the evidence windows, with margin to spare and fault tolerance, at the central human-transfer inputs. It is NOT an observation in a dog.
2. Every program depends on agents that do not yet exist in dogs (a persistence-capable canine-binder CAR-T with expansion; the CSF CAR-T; the continuous spinal pump) and on trial-stage anti-CD20.
3. Outside the model: unattributed multidrug resistance (E12), eye and testis, late second cancers (21% at 10 years in human CAR-T survivors), non-relapse mortality (18% at 10 years), parenchymal access.
4. The tumour vaccine is not load-bearing: the 7-agent B-cell program still clears with it removed.
5. A note on method: the search's clock stage evaluates only a subset of sets when more than 6000 cover every escape, so counts of "robust" sets from the search are lower bounds; the programs above were verified by direct evaluation.
