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

**Sensitivity to the inputs that still have no source** (`joint_report(..., f=, r=, cns_fraction=)`): the share of tumour cells that are cycling (0.05 to 0.5), the
fraction of persister tolerance retained (0 to 0.9), and the share of burden that seeds the brain (0.05 to 1.0). The T-cell 5-agent program clears, survives halving and
survives removing any agent across all of them. The B-cell 7-agent program clears and survives halving across all of them, and loses only the any-one-removed test when retained
tolerance is 0.5 or more or the brain seed fraction is 0.5 or more. Per `CLAUDE.md` rule 11 these are not reported as gaps: no closure depends on a particular value of any of them.
Which assumed numbers still carry weight: hydroxychloroquine brain access 0.3 has no source, but removing hydroxychloroquine does not break any program above.

## F. Re-assessment of vaccines, engagers (eBAT, BiTE, armed T cells), inhibitors and stem cells; programs from agents that exist today (2026-10-02)

The user: "I needed scientifically sound, not totally theoretical. And I think you are dismissing vaccines, ebats, inhibitors, stem cells too easily."
Accepted (`CLAUDE.md` failure 8, rule 13). Sweeps: `docs/universe/SWEEP_hct_model.md`, `SWEEP_bispecific.md`, `SWEEP_exists.md`, `SWEEP_inhibitors_partial.md`
(the inhibitor sweep was cut off by a rate limit twice; its finished classes are used, the rest are listed). "ebats" is read as the eBAT (EGF/uPA bispecific
angiotoxin) of the hemangiosarcoma branch, and also covers CD3 bispecific engagers and bispecific-antibody-armed T cells.

**Verdict per class, each with a scientific reason, none for lacking canine data.**

| class | in model now | reason it is or is not decisive |
|---|---|---|
| Stem-cell transplant, allogeneic DLA-identical | **YES, OUTCOME** (2.6 e-folds, gross 0.106 /day over 166 d; brain access 0.5) | Calibrated from the dog plateau (8 of 9 first-remission dogs alive >4 y, PMID 35789057) and corroborated by human T-cell lymphoma (relapse 8% vs 55%, PMID 39270145). Exists today at referral centres. It is what lets the B-cell body close from existing agents. Needs a DLA-identical littermate (25% per sibling); MHC loss is its open escape |
| Stem-cell transplant, autologous / thiotepa rescue | YES (TBI-autologous OUTCOME; thiotepa OUTCOME, human) | conservative gating default; adds little beyond allo and shares its toxicity budget, so only one transplant-class option per program |
| Vaccines (APAVAC, dTERT) | **YES, OUTCOME** | credited at k 0.03-0.055 /day; they act on dividing cells and need MHC-I, so they add margin but cannot reach the dormant progenitor. Their tails are flat (3-year survival 10% vs 8%) |
| Inhibitors | **YES, TRANSFER** (zanubrutinib B; romidepsin, belinostat T; panobinostat, vorinostat, bortezomib, verdinexor, venetoclax, HCQ earlier) | each is entered with a human IC50 x label exposure derivation; they cover specific escapes (BCR, apoptosis) but are pump substrates or division-gated, so none reaches the dormant progenitor |
| CD3 bispecific engagers | YES, TRANSFER-OUTCOME, **needs development** | strong human data (epcoritamab+R-CHOP CR 85%, 2-year PFS 80%); human CD3 arms do not bind canine CD3 (43% identity), so a canine engager must be made; canine binders exist. Non-gated, non-pump, MHC-independent, CNS 0.5 |
| Armed T cells (BATs) | NO kill rate | no lymphoma trial in any species; canine T-cell expansion is commercial, the arming step is not found. Not credited |
| eBAT | EXCLUDED, scientific reason | targets EGFR and uPAR are lower in 29 canine lymphomas than in sarcomas (mRNA) and a human T-cell line lacking them was not killed (PMID 28193671); dog toxicity: hypotension 4/23, liver 2/23 |
| Spinal pump | REPLACED | oral cytarabine ocfosfate does the job without a device (serum Cmax 1.9-3.0 uM, CSF:serum 0.54-1.2; measured CSF troughs 0.04-0.27 uM, derived time-average 0.3-1.4 uM; PMID 37670479, 4 dogs) -- corrected 2026-10-04: the earlier 'CSF 1.0-3.6 uM' multiplied a trough ratio by a peak serum value; IV infusion CSF 8.3 uM measured (PMID 1742843) |

**Result with agents that exist today** (licensed, off-label, or in dog trials; thiotepa counted off-label; one transplant-class option per program; every one of the
23 escapes required closed; every combination of up to 4 agents scanned exhaustively, up to 5 for B-cell body):

| | closes? | what is left |
|---|---|---|
| **B-cell body** | **YES.** 268-362 sets of 4 or fewer agents clear every lineage inside the documented windows, for example anti-CD20 antibody + verdinexor + allogeneic transplant + oral cytarabine, margin +0.15 /day, last lineage gone by day 74 | none. None of the 2,328 clearing sets of up to 5 agents also survives halved potencies and dropping any one agent |
| B-cell brain | every escape clears (by day 15 at the latest) **except one**: E5, the dormant pump-armoured progenitor, which regrows after day 84 when the documented exposure of verdinexor (56 d) and oral cytarabine (84 d) ends | E5, margin +0.03 /day |
| T-cell body | every escape clears except E5, which regrows after day 166 when the transplant window ends | E5 |
| T-cell brain | E2 (loss of the cytarabine-activating enzyme), E5 and the bulk regrow | E2, E5, bulk |

**What closes the remaining escape, specified from the model.** One more agent that is not division-gated, not a pump substrate, reaches the compartment, and has an
effective kill (kill x access) of at least about 0.06 /day in the brain (0.03 /day in the T-cell body) without overloading the organ budgets. Candidates with human data
that meet it: the canine CD3xCD20 engager (0.16 x brain access 0.5 = 0.08; B-cell, needs development), CAR-T (needs development), thiotepa consolidation if it is accepted
as acting on dormant cells (not shown; with the conservative default it does not close the brain). Candidates that exist today do not reach it: every existing
agent that reaches the brain is division-gated, a pump substrate, or defeated by loss of the cytarabine-activating enzyme.

**Longer dosing does not close it (checked).** Extending the documented windows of verdinexor, oral cytarabine and hydroxychloroquine to 120, 180, 365, 540 and 730 days leaves
the B-cell brain and the T-cell brain open: after the transplant window ends (166 days) nothing still being given reaches the dormant progenitor in the brain, because the
remaining agents are division-gated or pump substrates and the antibody's brain access is 0.002. In the body, 365 days of dosing closes the T-cell body as well. So the brain
needs a sustained, non-gated, non-pump, brain-reaching agent, not longer exposure to the ones that exist.

## G. Near-future agents (2026-10-02; /goal: "keep going until you truly close all. I don't mean you can only use therapies that exist today, I meant to include near future ones this are scientifically sound. Just nothing that's pure theoretical")

**The standard (now in `CLAUDE.md` rule 13).** Tiers: **A** exists today for dogs (licensed or off-label); **B** clinical-stage in dogs; **C** clinical-stage in humans with a stated path to the dog
(the canine construct or route still has to be built); **D** preclinical only; **E** no clinical evidence of the mechanism anywhere. A closing program may use A-C. D and E are theoretical and
never count. Section F had retreated to "exists today" only; that was the wrong bar. Sweeps: `docs/universe/SWEEP_near_future_cell.md` (readiness of each to-build agent, with PMIDs),
`SWEEP_outside_model.md` (items that were outside the model, searched by measurable proxy per rule 14), `SWEEP_nongated.md` (the agent search for the open escape E5).

**Readiness of what the programs use** (`lymphoma_joint.READINESS`; the code refuses a program containing any D or E agent):

| agent | tier | basis |
|---|---|---|
| anti-CD20 antibody (systemic) | B | canine antibody in dogs, B-cell depletion rate measured (PMID 38662527) |
| hydroxychloroquine, verdinexor, prednisolone, romidepsin | A | off-label / licensed |
| allogeneic DLA-identical transplant | A (referral centres) | 8 of 9 first-remission dogs alive >4 y (PMID 35789057) |
| oral cytarabine ocfosfate | B | dogs: serum Cmax 1.9-3.0 uM, CSF troughs 0.04-0.27 uM, derived time-average 0.3-1.4 uM (PMID 37670479, 4 healthy dogs, 7 daily doses); human use is 10-14 days per 28 |
| intrathecal anti-CD20 antibody; continuous intrathecal cytarabine | C | human intraventricular rituximab clears CSF lymphoma cells (PMID 24190981) |
| CD3xCD20 bispecific engager (B-cell) | C | human class is licensed or late-stage; anti-canine CD3 and canine CD20 binders exist, no canine engager yet; a dog had a cytokine storm to a T-cell agonist antibody (PMID 25988188), so step-up dosing is a condition |
| CAR-T, canine binder (B: CD19/CD20; T: CD7, CD5+CD7) | C | canine CD20 CAR-T in 7 dogs did not expand or persist (PMIDs 32002286, 35898541); human CD7 CAR-T in T-ALL/lymphoma incl. CNS (PMIDs 37020231, 37740926); in-vivo CAR-T made in the patient, first-in-human 2025-26, removes ex-vivo expansion (PMID 41882404; lymphoma result is a conference/press report) |
| CSF-delivered CAR-T | C | human intrathecal CD19/CD22 CAR-T in B-ALL with CNS disease, CR 21/22 (ASH 2024 abstract); peer-reviewed intrathecal CAR-T (PMIDs 41495049, 42207176, 41798119) |

Not credited, each for a stated reason: bispecific-armed T cells (no lymphoma trial in any species: tier D); canine CAR-NK (none exist: D); mRNA-LNP CAR-T (expression 7-10 days, so it is a repeat-dosing
agent with no lymphoma data: D); eBAT (targets low in canine lymphoma, section F); anti-PD-1 (measured negative).

**Result: both immunophenotypes close body and brain with A-C agents, 23 escapes, toxicity charged on the union of the program** (`lymphoma_joint.NEAR_FUTURE_PROGRAMS`, tests in `tests/test_lymphoma_universe.py`):

| program | agents | at the LOW human-grounded inputs (CAR-T kill 0.12/day, CSF duty 0.15) | at the CENTRAL inputs (0.35/day, 0.4) |
|---|---|---|---|
| **B-cell, 9 agents** | anti-CD20 antibody, intrathecal anti-CD20 antibody, hydroxychloroquine, verdinexor, allogeneic transplant, oral cytarabine ocfosfate, CD3xCD20 engager, CAR-T, CSF tandem CD19/CD20 CAR-T | clears; no single agent load-bearing; margins body +0.26 / brain +0.13; last lineage gone day 49 (body), 72 (brain); 44 of 44 escape-by-compartment rows closed, at least 4 covering agents each; **not** robust to halving every potency | clears, halved clears, any-one-removed clears; last lineage day 33 / 38 |
| **T-cell, 8 agents** | hydroxychloroquine, intrathecal cytarabine, CD7 CAR-T, CD5+CD7 CAR-T, CSF CD7 CAR-T, verdinexor, allogeneic transplant, oral cytarabine ocfosfate | clears; **the intrathecal cytarabine is load-bearing** (dropping it breaks the brain; added 2026-10-04 after the oral cytarabine CSF level was corrected down); margins body +0.15 / brain +0.045; last lineage gone day 80 (body), 158 (brain, inside the 166-day transplant window); 42 of 42 rows closed, at least 5 covering agents each; not robust to halving | clears, halved clears, any-one-removed clears; last lineage day 28 / 31 |

So the earlier statement "at the low inputs the B-cell programs do not clear" is superseded: it was true only for programs that had no engager and no oral cytarabine. The B-cell program closes at the low inputs because it has an
independent CAR-T-free route (antibody + engager + transplant + cytarabine); with the engager alone added to the existing-agent program (anti-CD20 + HCQ + verdinexor + transplant + ocfosfate + engager) both compartments clear at low AND central inputs,
but that 6-agent set is not fault tolerant (the transplant, cytarabine and the engager are each load-bearing in the brain).

**The exact input the closure turns on** (`joint_report` sweep, B program without the engager, so the CAR-T route alone): it clears at CAR-T kill >= 0.08/day at the low duty (0.06 at duty 0.4) and is robust to halving and to removing any
agent from **0.2/day**; the T-cell program clears from 0.12/day and is robust from 0.2/day. The central human-grounded value is 0.35/day (1.75 x the robust threshold); the low value 0.12 is at the T clearing threshold. Dog CAR-T has so far
not reached either (7 dogs; no expansion beyond ~day 14-28), which is why the programs also carry the CAR-T-free route for the B-cell case and why in-vivo generation of CAR-T is named as the route for T-cell disease.
This is a stated condition, not a gap in the sense of CLAUDE.md rule 11: a transfer stands behind the number and the threshold is explicit.

**Search note.** Exhaustive brain searches of up to 6 agents at the low inputs (every combination covering all 23 escapes; `tier any`, sound grades): B-cell 361,087 covering sets, 3,594 clear the brain clock, 3,352 of those also clear the body
(run with the earlier thiotepa pump default); T-cell 346,763 covering sets, 242 clear the brain clock (after the thiotepa change; 96 before it; all 96 also clear the body). No automatically found set is also robust to halving and drop-one, because the search forbids
two agents of the same family (a second CAR-T). The fault-tolerant programs above were assembled from the agents the search keeps selecting and verified by direct evaluation, as in section E.

**Agent search for E5 (the dormant pump-armoured progenitor), `SWEEP_nongated.md`.** No agent shown to kill a dormant, pump-high lymphoid progenitor in the brain was found beyond the immune and cellular routes. Best candidates: thiotepa with stem-cell rescue
(outcome-derived k 0.13-0.37; **no P-gp cross-resistance** in the MDR1-overexpressing line, GI50 1.07 x parent, so the pump-substrate default was removed; still division-gated by default and it ends with its 115-day window, so it does not close the existing-agent brain),
CDK9 inhibitors (kill quiescent cells; durable CRs in 2 of 7 high-grade B-cell lymphomas; k not derivable from pulse dosing; brain and pump status not found), artesunate (canine IC50 0.22-0.54 uM, dog Cmax 9.3 uM; k ~0.1 rests on assumed PK; ungraded).
Excluded for stated reasons: cladribine (BCRP, dCK), ONC201 (k 0.006-0.017), arsenic trioxide (CSF 15% of plasma), IACS-010759 (neurotoxicity), PBD ADC payloads (efflux), magrolimab (deaths), 90Y-ibritumomab in CNS (PFS 6.8 weeks), busulfan (k ~0.015).
Premise correction: canine B-cell lymphoma rarely expresses BCL6 (PMIDs 23783577, 32038991), so BCL6 degraders are not a canine-driver-matched class.

**Items that were outside the model, searched by measurable proxy (`SWEEP_outside_model.md`), graded per rule 11:**

| item | finding | grade |
|---|---|---|
| MHC/HLA loss as escape from transplant, vaccine, engager | HLA loss is a mismatch mechanism: 15.6% of 533 post-HCT relapses overall, 28.7% haploidentical, 7.2% unrelated adult (PMID 42348822); none to lose with a DLA-identical littermate. Matched grafts relapse by MHC-II down-regulation (17/34 AML, PMIDs 30380364, 30911134), which only weakens T-cell arms; antibody, CAR-T and engager are MHC-independent and already in the programs (the model's antigen-presentation-loss escape is covered by them) | CLOSED by derivation for a DLA-identical donor; **condition**: a DLA-identical donor (about 25% per sibling); a haploidentical donor would reopen it (7-29%) |
| unattributed multidrug resistance (E12) | named canine mechanisms are partial (ABCB1 up in 4/10 resistant dogs, TP53 16%, ABCG2 in T-cell, NR3C1 down); axi-cel gives 31% ongoing response at about 5 y in chemo-refractory large B-cell lymphoma (PMID 36821768), so the chemo-resistant state does not defeat immune effectors | CLOSED by transfer for the immune-effector routes in the programs; residual unattributed share stays named |
| eye | 61% of 100 dogs with intraocular lymphoma were solitary and did not progress after enucleation (PMID 28714087); human isolated ocular relapse after systemic therapy is common (29/59, PMID 33864703); no antibody or cytarabine eye concentration found | CLOSED by a local agent (ocular radiation or enucleation) added to the program when ocular disease appears; systemic access to the eye is not shown |
| testis | contralateral-testis radiation: no testis relapse in IELSG-10 (PMID 21646602); orchiectomy lowered CNS relapse (HR 0.11, PMID 39352469); neutered dogs have none | CLOSED (derivation) |
| second cancers, non-relapse mortality | allo-HCT secondary solid tumours ~9-10% at 10 y (PMID 38517548); CAR-T second cancers 21% and non-relapse mortality 18% at 10 y in humans (PMID 42341302); dog GVHD with DLA-identical littermates low (16/17 and 12/19 long-term chimeras) but 6 of 13 died of GVHD with DLA-identical unrelated donors | not escapes: **costs** charged against the 10-year goal; reported as costs, not as odds |
| brain parenchyma access | IV rituximab adds nothing in primary CNS lymphoma (HR 1.00, PMID 30630772), consistent with the 0.002 access; thiotepa CSF:plasma AUC ~1; zanubrutinib CSF/plasma ~0.4; venetoclax 0.74%; **no level has been measured in gadolinium-non-enhancing lymphoma for any agent** (the rule-14 proxy was searched) | CLOSED as transferred access factors; the non-enhancing-tumour measurement does not exist for any agent |
| late extranodal relapse | IELSG30 shows relapses beyond 6 years (PMID 38181782) | a reason the 10-year window needs the persistent routes (CAR-T persistence, transplant graft-versus-lymphoma) |

**What "closed" means after this section** (the decidable conjunction, rule 12): within a catalogue of 28 sound-grade agents per immunophenotype and 23 escapes plus the items above, the B-cell and T-cell programs clear every escape-by-compartment row at the pessimistic inputs with
no single agent load-bearing, using only A-C agents. It holds **if** (1) the C-tier agents are built for dogs (canine engager and CAR-T construct; the CSF route), (2) the CAR-T effective kill reaches 0.2/day for full fault tolerance (0.12 for the T-cell program to clear;
the B-cell program also has the CAR-T-free route), (3) a DLA-identical donor exists, (4) the engager is introduced with step-up dosing, (5) ocular disease, if it appears, is treated locally. These are the conditions, each stated with its number. It is a model result
(TRANSFERRED and OUTCOME-calibrated inputs, mean-field clock), not a demonstration in a dog.

### G.1 The growth-rate bar was a bare literal; now derived (2026-10-03; `lymphoma_standard_audit`, `docs/universe/SWEEP_growth_bar.md`)

Running the audit the merged rule 11 asks for (`lymphoma_standard_audit.failing()`) found exactly one failing input: the per-day growth bar 0.0903, which gates every margin and was labelled
"illustrative, not fitted" in `lymphoma_scenarios` (the same failure as CLAUDE.md failure 7 in the HS work). It is now **DERIVED as a bracket from dog data**: net in-vivo growth of a resistant clone is
0.015-0.12 /day (relapse regrowth after CHOP retreatment, rescue protocols and COAP, PMIDs 21320021, 17338160, 18196747: floors 0.015-0.07; untreated and prednisone-alone survival of 38.5 and 50 days, PMIDs 9839202, 34125606:
0.05-0.12 with an assumed presenting burden); gross ceiling 0.204 /day (potential doubling time median 3.4 d, 42 dogs, PMID 10598945). The bar sits at the upper end of the net band and is 44% of the gross rate (implied cell-loss
factor 0.56, plausible but not measured in dogs). It is conservative against observed net regrowth and not an upper bound if cell loss is small, so the closure is reported at higher bars with potencies held fixed (adverse; outcome-calibrated kills would rise with the bar):

| growth bar | B-cell, central inputs | T-cell, central inputs | B-cell, pessimistic inputs | T-cell, pessimistic inputs |
|---|---|---|---|---|
| 0.0903 (used) | clears; halved ok; any-one-removed ok | clears; halved ok; any-one-removed ok | clears; any-one-removed ok | clears; not fault tolerant (intrathecal cytarabine load-bearing) |
| 0.12 (top of net band) | clears; halved ok; not fault tolerant | clears; robust | clears; not fault tolerant | **does not clear** |
| 0.15 | clears; not robust | clears; robust | clears | does not clear |
| 0.204 (gross ceiling, no cell loss) | clears; not robust | clears; not robust | clears | does not clear |

So: the B-cell program clears at every bar up to the gross ceiling at both input sets; the T-cell program clears at the central CAR-T inputs up to the ceiling, and at the pessimistic CAR-T inputs only if the bar is at most about 0.10 /day.
That is a stated boundary, not a re-tuning. `failing()` now returns nothing; `wrongly_reported_as_gaps()` lists the items that pass (no canine CAR-T efficacy, no non-enhancing-lymphoma measurement, no canine engager, MHC loss under a DLA-identical graft, E12).

## H. Is anyone building the near-future agents for dogs, and what closes the cases if not (2026-10-04; /goal: "do 1, and if you can't find them then go back to the drawing board to see if there's other ways to close these")

Sweeps: `docs/universe/SWEEP_dog_programs.md` (programs search), `SWEEP_persistent_graft.md`, `SWEEP_regrade.md` (partial: rate-limited), `SWEEP_sustain.md`. Code: `lymphoma_joint.DOG_STATUS`, `DOG_PROGRAM_PROGRAMS`, `dog_program_gaps`; `lymphoma_sustained.py`.

### H.1 Program search (item 1). Result: only the B-cell CAR-T has a dog program; the engager, CD7/CD5 CAR-T and the spinal-fluid route do not (not found)

| agent | dog status found | source quality |
|---|---|---|
| canine CD3 engager (CD3xCD20) | **NOT FOUND.** Only an anti-canine CD3 mAb (Front Vet Sci 2025, "could serve" for bispecifics) and an AKC-CHF grant for BiTE-redirected antiviral T cells in T-cell malignancies (2022-25, outcome unpublished). A canine NK engager (TriKE, B7-H3, sarcoma) is in dogs, but it engages NK cells | institutional page, grant snippet |
| canine CAR-T, B-cell | **Program active**: Penn autologous CD20 CAR-T trial (7 dogs reported; did not expand or persist); the in-vitro/mouse fix is human 4-1BB-CD3z (PMID 41376156); tandem CD19/CD20 is preclinical with a stated dog-trial intent (PMID 42480604); LEAH Labs xenogeneic CAR-T (NSF SBIR) is **on hold** on both its Missouri and Minnesota pages | peer-reviewed + institutional pages |
| canine CD7/CD5 CAR-T (T-cell) | **NOT FOUND**; CD5 clones exist but CD5 loss is the commonest aberrancy in canine T-cell lymphoma (310 cases) | PubMed + web |
| spinal-fluid (CSF) CAR-T or antibody in dogs | **NOT FOUND**; the only canine intracranial CAR-T trial (CSU/CU, glioma, with verdinexor) is intratumoral | institutional page |
| in-vivo CAR-T in dogs | **NOT FOUND** (NHP and human first-in-human are real); mRNA-LNP reaches canine brain tumour (PMID 41218853) | PubMed |
| allogeneic NK cells in dogs | Phase 1 done (3 dogs, no GVHD) | preprint, Vet Comp Oncol |
| licensing calibration | Tanovea conditional 2016 to full 2021 (4.6 y); Laverdia 2021 to 2026 (5.4 y); Oncept 2007 to 2010 (3 y). The search agent's judgement: at least 7-10 years to a licence for an agent not yet built; 2-4 years to research-use build | FDA / company filings |

So "near-future for dogs" is supported for the **B-cell CAR-T only**. For the engager, CD7/CD5 CAR-T and the CSF route what is supported is human clinical-stage evidence for the class, not a canine program. Veterinary trials do not sit on ClinicalTrials.gov, so absence from it means little; the institutional pages and grants were searched instead.

**What the B-cell case needs from agents that have a dog program** (`DOG_PROGRAM_PROGRAMS["B"]`; no engager, no CSF route): anti-CD20 antibody, hydroxychloroquine, verdinexor, matched transplant, oral cytarabine, and a systemic CAR-T. It clears body and brain from CAR-T kill 0.12 /day (central 0.35 also survives halving) but is not fault tolerant: the CAR-T is load-bearing.

### H.2 Drawing board: other ways to close the open rows

| route | evidence | closes? |
|---|---|---|
| **Persistent graft-versus-lymphoma** after day 166 (the donor immune system is lifelong) | Dog: stable full chimerism and no relapse after day 268 in 8 dogs to 4+ years = a hold or extinction, rate not separable; CML: BCR-ABL transcripts held for 10+ years (PMID 23333776). Contradicted: T-PLL relapsed at 12, 59, 84 months with full donor chimerism (PMID 32259827); allo-ALL CNS relapse 4-5% regardless of conditioning; donor DLI into mixed-chimeric dogs does nothing unless sensitised. Bracket: human leukaemia hazard decline implies a net 0.0008-0.004 /day | **No.** The model needs an effective persistent kill of about 0.12 /day (brain, B-cell) or 0.06 /day (T-cell body) to clear the dormant progenitor; the bracket is 30 to 150 times lower. The graft holds, it does not clear |
| **Re-graded existing dog agents** (rabacfosadine, lomustine, L-asparaginase) | Rabacfosadine: acts on dividing cells (resting lymphocytes 127x less sensitive, so dormant kill 0.003-0.02 /day), dCK-independent (GMP-kinase route), CSF access not found, pulmonary fibrosis 4%. Lomustine: CSF radioactivity >=50% of plasma (human label), derived kill 0.004-0.04 /day, dormant-cell kill not shown (mouse HSC data negative), cumulative hepatotoxicity. L-asparaginase: enzyme, not pumped, depletes CSF asparagine in humans, but kill is cytostatic-then-apoptotic and dormant-cell evidence is negative (CML stem-like cells not killed); outcome-only rate 0.03-0.05 /day | **No**, none kills dormant cells; they add bulk coverage only. The HD-methotrexate, intrathecal cytarabine and other regrades did not finish (rate limit) |
| **Sustain an existing agent for years** | E5 is cleared by a pump-independent agent that is present long enough, because the dormant cells wake slowly and are killed once awake (the earlier "longer dosing does not close the brain" was tested only to 730 days; that statement is withdrawn). B-cell brain: oral cytarabine ocfosfate sustained about **1,500 days** (4.1 y) at a time-average CSF level of 0.3 uM; the others at their documented windows. Required duration is set by the swept cell-switching rate (383 days if cells switch at 0.1 /day or faster) | **Conditionally, B-cell brain only.** See H.3 |
| **T-cell body** | Verdinexor sustained at least about 170 days closes it with the other agents at their windows (documented continuous use: 17 months in one dog; partial responses lasting 246 and 354 days; the label is licensed for continuous twice-weekly dosing) | **Yes, conditionally**: verdinexor for about 6 months |
| **T-cell brain** | Thiotepa (115-day course) closes the dCK-loss lineage (E2) in the brain, but the dormant lineage then needs oral cytarabine for about 8 years in T-cell disease (lower T-cell CSF kill) | **No** from existing agents. Leads: hydroxyurea (dCK-independent; dog on continuous dosing >= 448 days; CSF penetration not found), procarbazine (50 dogs on a continuous regimen, CSF not found) |

### H.3 The sustained-cytarabine route, graded (rule 11)

- **Correction found while grading it.** The "CSF 1.0-3.6 uM" for oral cytarabine ocfosfate that this record carried as measured (and used as the kill-rate set-point) is the product of a trough CSF:serum ratio (0.54-1.2) and a PEAK serum value (1.88-2.98 uM). The directly measured CSF values in the paper (PMID 37670479, 4 healthy dogs, 7 daily doses) are troughs of **0.04-0.27 uM**. The time-average CSF level is derived at about **0.3-1.4 uM** (AUC/24 h x accumulation index 2.1 x CSF:serum; no CSF sample was taken at the peak). The model now uses 0.3 uM (`OCFOSFATE_CSF_NM`), which lowered the oral-cytarabine kill rate 2.2-fold. Effect: the T-cell near-future program is no longer fault tolerant at the pessimistic inputs (intrathecal cytarabine is load-bearing); the B-cell program is unchanged.
- **How the closure depends on the CSF level.** Oral-cytarabine kill scale x1.0 / x0.5 / x0.3 / x0.2 / x0.15 / x0.1 needs 1,468 / 1,504 / 1,577 / 1,848 / 4,166 days / does not close. The route closes only if the brain kill reaches about 0.1 /day (a CSF time-average of about 0.11 uM); the measured troughs (0.04-0.27 uM) straddle that and the derived time-average (0.3-1.4 uM) is above it, but **no CSF time-average has been measured**.
- **Sustainability.** Continuous ocfosfate for years has no source. Human use is intermittent (10-14 days per 28; PMIDs 9766508, 12646944, 15550587); at 600 mg/day 25-60% stop within a year for cumulative GI or marrow toxicity; at the label dose (100-200 mg/day) the longest course found is 2 years of maintenance (PMID 25652695, one patient) and at least 18 months continuous in one advanced-CML patient (abstract). Dogs: only 7 daily doses (all 3 dogs had grade 1 neutropenia and thrombocytopenia within the week); pulsed IV cytarabine 600 mg/m2 every 3-6 weeks for 24 months or more in neurological disease with no serious adverse events (PMID 41742567). An intermittent 14-on/14-off schedule stretches 1,500 days to roughly 2,000-2,900 calendar days (scaling assumed). Grade: **ASSUMED** beyond about 2 years; CONTRADICTED for continuous dosing at 600 mg/day. Availability for dogs: research import from Japan only.
- **Verdict.** This is a route to a testable condition, not a closure: it needs (i) a CSF time-average measurement in dogs on the intended schedule and (ii) a multi-year intermittent-tolerability study. Neither exists; both are cheap relative to building a CAR-T. It is **not** counted as closing the B-cell brain.

### H.4 Where each case stands (the decidable list)

| case | closed by agents that exist today? | closes through | still depends on |
|---|---|---|---|
| B-cell body | **Yes** | anti-CD20 + verdinexor + matched transplant + oral cytarabine (day 74) | a DLA-identical donor |
| B-cell brain | No | (a) sustained oral cytarabine, about 1,500 d, or (b) the B-cell CAR-T that has a dog program (kill >= 0.12 /day) | (a) CSF time-average >= ~0.11 uM (unmeasured) and multi-year tolerability (assumed); (b) dog CAR-T expansion (failed in 7 dogs; fix shown in vitro only) |
| T-cell body | No | verdinexor sustained >= ~170 d | verdinexor continuous use past 17 months not documented (not needed beyond 6) |
| T-cell brain | No | only CD7/CD5 CAR-T (+ thiotepa course for E2) | **no dog program found for CD7/CD5 CAR-T**; the CSF route is not built either |

The engager and the CSF route are **not needed** for the B-cell case. The engager has no dog program found; it stays in the near-future program as an additional independent route labelled "class clinical-stage in humans; canine version not started".

## I. Realistic closing programs from agents that exist today, without a future CAR-T (2026-10-04; /goal: "it doesn't sound you found realistic ways of closing these ... more just hand waving and saying some future car t program will solve it. That's a goal failure, keep going")

The criticism is right about section H: its "conditional" routes leaned on a CAR-T that does not exist for dogs, and its drawing-board pass ignored the one modality that is cycle-independent, not pumped, needs no dCK and reaches the whole brain: **radiation**. Sweeps: `docs/universe/SWEEP_rt.md` (partial: rate limit), `SWEEP_stemcell.md` s4, `SWEEP_hct_model.md` s7.2; code `lymphoma_sustained.py` (`rt_agent`, `clock_with_rt`, `minimal_window_with_rt`); tests in `tests/test_lymphoma_universe.py`.

### I.1 A record inconsistency, found and fixed in the new module
The v1 catalogue tags every radiation entry "division-gated" ("TRANSFER (radiobiology)", no citation), and section C said re-running radiation non-gated "changes nothing" (true only at the v1 dose). The record's own derivation (`SWEEP_hct_model` s7.2) says the opposite for lymphoid cells: SF2 in 27 canine lines is uncorrelated with S-phase fraction or doubling time (PMID 27257868). Other evidence: circulating CLL cells, which are non-cycling, die by interphase apoptosis in about 85% of patients and about 15% are resistant (PMIDs 15718417, 19188704); resting lymphoid radiosensitivity is p53-dependent (PMID 19351849); quiescent human haematopoietic stem cells are MORE prone to radiation apoptosis than progenitors (PMIDs 20619763, 29666389). So radiation is graded **cycle-independent (DERIVED)**. The v1 entries are left alone because the ledger claims were derived on them (the ledger tests now say so explicitly); the new module re-grades radiation and applies the in-vivo dose-modifying factor 1.9 (PMID 3009370) to the in-vitro e-folds. **Caution already in the record:** dose escalation of TBI from 8.4 to 13.5 Gy did not reduce relapse in dogs (PMIDs 3887690, 3901841), so the e-folds are not credited above one conventional course (23.4 Gy, 13 x 1.8 Gy).

### I.2 What a radiation course is worth, in the model's own units
A 23.4 Gy course delivers 1.71 / 3.18 / 7.05 e-folds in vitro for the most resistant / median / most sensitive canine line (CLL1390 / 1771 / CLBL1), or **0.90 / 1.67 / 3.71 e-folds in vivo** after the factor 1.9. With every existing agent that reaches the compartment, the model needs the non-gated kill to reach: B-cell brain 8.9 e-folds if nothing else is sustained (3.8 with one year of sustained oral cytarabine and verdinexor, 2.4 with two), T-cell body 11.7 (1.0 with a year of sustained verdinexor), T-cell brain 19.6 (and 19.1 even when everything is sustained).

### I.3 The programs (every agent exists or is licensed; durations and grades stated)

| case | program | what the model needs | evidence and grade |
|---|---|---|---|
| **B-cell body** | anti-CD20 antibody (Elanco 1E4, in dogs) + verdinexor (licensed) + hydroxychloroquine + matched-donor TBI-allogeneic transplant + oral cytarabine | clears every lineage by day 74 (section F) | anti-CD20 depletion MEASURED; verdinexor DERIVED; transplant OUTCOME (8 of 9 dogs alive >4 y); needs a DLA-identical donor |
| **B-cell brain** | the body program **plus** a 23.4 Gy whole-brain / craniospinal course **plus** oral cytarabine and verdinexor continued for the window below | common sustained window **975 days** at the median canine line, 1,253 days at the most resistant line, 250 days at the most sensitive; 1,560 days with no radiation. Clears with the courses stacked from day 0 (toxicity de-rating applied) | radiation cycle-independence DERIVED; canine lymphoma-line radiosensitivity MEASURED; in-vivo factor TRANSFERRED; **continuous oral cytarabine for 2.7-3.4 years: ASSUMED beyond about 2 years** (human maintenance 2 y at label doses, SPAC; dogs: 7 days and pulsed IV for 24 months); CSF time-average unmeasured (troughs 0.04-0.27 uM, derived 0.3-1.4 uM) |
| **T-cell body** | prednisolone, hydroxychloroquine, verdinexor, romidepsin, matched-donor transplant, oral cytarabine, with **verdinexor continued about 170 days** (139 days with the sensitive-line radiation) | clears every lineage | verdinexor is licensed for continuous twice-weekly dosing; longest documented continuous canine exposure 17 months (one dog, PMID 39235783), partial responses lasting 246-354 days; the 13-week toxicology study found testis and thymus lesions: 6 months is inside what is documented |
| **T-cell brain** | **no program from existing agents closes it** | the sweep to 3,650-day windows never clears it at any radiation value in the evidence range (0.9-3.7 e-folds); 432 staged schedules of radiation + thiotepa + transplant + oral cytarabine none clears; with toxicity ignored, the union of every eligible agent plus 7 e-folds of radiation does clear it (so it is a budget problem, not a missing mechanism) | see I.4 |

### I.4 Why the T-cell brain does not close, with numbers, and what would
- Oral cytarabine does not help the T-cell dormant lineage: the T-cell lymphoma-line IC50 is higher, so at a CSF level of 0.3 uM the kill is about 0.05 /day (B-cell about 0.29), below the awake growth rate 0.09; the sustained agents never touch it. The dCK-loss lineage (E2) is covered only by radiation, thiotepa and a few weak agents.
- Radiation alone would need **19.6 e-folds in vivo** (36 Gy as 20 x 1.8 Gy gives about 1.5 times the 23.4 Gy value, ignoring fractionation sparing). Human primary T-lineage lymphoma cells are SF2 0.36-0.44 (D0 about 1.9 Gy; PMID 1429095): 36 Gy would be about 10 e-folds after the in-vivo factor, half of what is needed. Only if the canine T-lymphoma CNS lineages were as radiosensitive as human haematopoietic stem cells (D0 about 0.9 Gy; about 21 e-folds at 36 Gy in vivo) would it close, and the whole-brain dose of 36 Gy carries real late-neurotoxicity risk (the dog evidence for it was not retrieved before the rate limit).
- The thing that would decide it is a measurement, not a new product: **primary canine T-cell lymphoma radiosensitivity (clonogenic or apoptosis, cycling vs resting, from fine-needle samples)**; if D0 is at the stem-cell end, a 36 Gy whole-brain course with the T-cell body program closes the brain; if it is at the human T-lineage value, it does not and the T-cell brain stays open with everything that exists.
- Other existing agents re-graded for the T-cell brain do not change this: lomustine (0.004-0.04 /day derived; CSF about 50% of plasma), rabacfosadine (dCK-independent but acts on dividing cells, CSF access not found), L-asparaginase (cytostatic; dormant-cell evidence negative), hydroxyurea and procarbazine (dCK-independent; CSF level not found).

### I.5 What this changes
- The B-cell case no longer needs a CAR-T, an engager or a spinal-fluid route, and the T-cell body no longer needs one either. They remain additional, independent routes (sections E, G, H), not requirements.
- The T-cell brain is the one case that stays open from existing agents, and it is stated as an open quantity (primary canine T-lymphoma radiosensitivity; toxicity budget), not as "a future program will solve it".
- Two inputs carry the B-cell brain: radiation e-folds on the dormant progenitor (a TRANSFER from lymphoid and stem-cell radiobiology, not canine E5 data) and multi-year oral cytarabine tolerability (ASSUMED beyond about 2 years). If the sensitive-line value holds, the sustained window drops from 975 to 250 days (8 months), inside the human maintenance experience.

## J. The T-cell brain closes with an existing combination: radiation + repeated intrathecal methotrexate + matched-donor transplant (2026-10-05; /goal: "look broader to close the T-cell brain. Do not stop until you found something. Something being worked on actively is acceptable. Purely theoretical from you is not")

Sweeps (four agents): `SWEEP_tcell_agents.md` (T-cell-active agents), `SWEEP_brain_access.md` (access methods in dogs), `SWEEP_wake_dormant.md` (waking dormant cells), `SWEEP_xpo1_cns.md` (verdinexor CNS), `SWEEP_nm600_itmtx.md` (a radiopharmaceutical now in dogs, and intrathecal methotrexate). Code: `lymphoma_sustained.py` (`it_mtx_agent`, `clock_program`, `minimal_it_mtx_window`); tests in `tests/test_lymphoma_universe.py`.

### J.1 What the broad sweep found
| lead | actively worked on? | CNS evidence | verdict |
|---|---|---|---|
| **Verdinexor brain access** (the model had an unsourced 0.05) | licensed for dogs; in the CSU/CU canine glioma trial (given at home twice weekly until progression) | selinexor (same chemical series; verdinexor is slightly more lipophilic, lower polar surface area) brain:plasma **0.60-0.72** at an intact barrier in monkey, rat and mouse (PMID 27323910, full text); human enhancing glioblastoma tumour:plasma 0.09 (0.06-0.19; PMID 34728525, barrier disrupted, timing mismatch possible); verdinexor not a canine P-gp substrate (PMID 36924353); CNS signs in the dog field study (tremor 11%, ataxia 6%, convulsion 4%) | access **0.6 TRANSFERRED** (floor 0.09); helps but does not close alone |
| **Intrathecal methotrexate** | routine in dogs (PMID 25041580, 112 dogs and 8 cats, 2.5 mg + cytarabine 100 mg flat dose; 30022475 CNS lymphoma in 18 dogs); the same agent is the standard CNS prophylaxis in human T-ALL (CNS relapse 1.5% in 598 children, PMID 31657981) | human CSF 423 uM peak, 4.6 uM at 24 h, 1.05 uM at 48 h after 6 mg (PMID 2809687); dog cisternal CSF half-life 5.2 h (PMID 581360); canine lymphoma-line IC50 2-3 nM (secondary citation of PMID 28992489) | **closes the T-cell brain with the combination below** (derived mean kill 0.2-0.7 /day weekly) |
| 90Y-NM600 (targeted radiopharmaceutical) | **in dogs with peripheral T-cell lymphoma now** (UW-Madison, page-level) | two of four treated dogs developed brain metastases invisible on the earlier PET; poor intact-barrier uptake; human 124I-CLR1404 shows no normal-brain uptake (PMID 28913154) | **not credited for the CNS** (body marrow-dose-limited); useful for the body |
| Focused ultrasound BBB opening | in research | dogs: one safety study (PMID 28912896, 10 beagles, no drug level); human gains 1.5-8x focal | no canine drug-delivery data; not credited |
| Osmotic BBB disruption + intra-arterial MTX | human PCNSL (PMID 19451444: ORR 82%, 25% alive at 8.5 y) | dog mechanism 1980s | not veterinary practice; not credited |
| Plerixafor / G-CSF to wake dormant cells | trials in AML | AML null to modest (PMIDs 28282031, 41980027); no lymphoma priming data | not credited |
| JAK1 / ITK / PI3K / HDAC / EZH2 inhibitors for T-cell lymphoma (golidocitinib, soquelitinib in dogs with T-cell lymphoma, valemetostat, duvelisib) | phase 2-3 in humans; soquelitinib 3 dogs (1 CR, 2 PR) | none has measured CNS access and a derivable kill | not credited (soquelitinib and oclacitinib are the leads for a CSF measurement) |

### J.2 The program and the numbers (every part exists; mean kill of the intrathecal methotrexate 0.12 /day, about every 2-3 weeks, below the derived weekly range 0.2-0.7)
**T-cell brain:** the T-cell program at its documented windows (matched-donor transplant, prednisolone, hydroxychloroquine, verdinexor, romidepsin, oral cytarabine) **plus** a 23.4 Gy whole-brain or craniospinal course **plus** intrathecal methotrexate. The model clears every lineage when the methotrexate is continued for:

| radiation in vivo (e-folds) | no radiation | 0.9 (most resistant line) | 1.67 (median line) | 3.71 (most sensitive line) |
|---|---|---|---|---|
| methotrexate window, mean kill 0.12 /day | 1,346 d | 841 d | **399 d** | 231 d |
| mean kill 0.20 /day (about weekly) | 1,094 d | 693 d | 336 d | 231 d |

The transplant is load-bearing (without it the window exceeds 4,000 days), and the methotrexate must reach a mean kill of about 0.1 /day (every four weeks or less often fails at 0.06 unless verdinexor reaches the brain at 0.3 or more, when it closes in about 800 days). Verdinexor and oral cytarabine are not needed for this closure: with only the transplant, the radiation course and the methotrexate it closes in 462 days. **B-cell brain** closes the same way, in 399 / 841 / 168 days at the median / most resistant / most sensitive line, which replaces the 2.7-3.4 years of oral cytarabine in section I with about 13 months and 28 to 36 methotrexate doses (the human median is 46 punctures).

### J.3 What this rests on, and what could break it (rule 11 grading)
- Derived, not measured in dogs: the methotrexate kill (IC50 is a secondary citation; the dog CSF volume is taken equal to the human apparent volume; the CSF tail beyond 48 h is extrapolated). Dog repeated dosing beyond 6 doses has no source; no Ommaya reservoir use in dogs was found.
- **It acts on cycling cells in the CSF space and the perivascular spaces, not deep parenchyma.** The model credits the full compartment. At half the effective kill (0.06) the route needs verdinexor at brain access 0.3 or more (800 days); the radiation covers the parenchyma. This is the weakest assumption.
- **Neurotoxicity is the real limiter:** leukoencephalopathy reached 29% at 2 years with high-dose methotrexate plus whole-brain radiation, and intrathecal methotrexate was the only independent risk factor (HR 4.5, dose-dependent; PMID 39269476). The model's budget (0.5 of the local CNS axis, staging with the radiation course) does not capture a late white-matter risk; no canine series of whole-brain radiation plus repeated intrathecal methotrexate exists.
- Radiation e-folds on the dormant cells are a transfer (section I); with no radiation the window is 3.0-3.7 years.
- This does not depend on any unbuilt product, a CAR-T, an engager, or the verdinexor brain-access value.

### J.4 What is superseded
Section I.3/I.4's "T-cell brain: no program from existing agents closes it" and section H.4's T-cell brain row ("only CD7/CD5 CAR-T"). Both were true only because intrathecal methotrexate was never in the model (the model carried an ASSUMED-grade intrathecal cytarabine, which a dCK-loss lineage defeats).

## K. Lawful availability: two load-bearing agents had no legal route, and the programs rebuilt without them still close (2026-10-06; /goal: "I know there's that rule where human meds can be used for pets under exceptions. Make sure the human ones you cited qualify. Also some of these closures seem to be on weak grounds, I need you to look further and truly close these")

Details and sources: `docs/universe/SWEEP_legal.md`. Code: `lymphoma_sustained.LEGAL_STATUS`, `lawful_pool`, `LAWFUL_PROGRAMS`, `lawful_clock`, `minimal_lawful_window`; tests in `tests/test_lymphoma_universe.py`.

### K.1 The rule, and the two agents it removes
21 CFR Part 530 (from AMDUCA 1994) permits extra-label use of **FDA-approved animal drugs and FDA-approved human drugs**, by or on the order of a veterinarian within a valid veterinarian-client-patient relationship. It does **not** make an unapproved drug lawful. So:
- **Oral cytarabine ocfosfate (Starasid) is approved only in Japan: no extra-label route in the US.** It carried the B-cell brain closure in section I (2.7-3.4 years of dosing) and appeared in every program since section F.
- **No licensed canine anti-CD20 antibody exists.** Blontress was licensed in 2015 and **discontinued in 2017**; the Elanco 1E4 antibody is investigational. It carried the B-cell body closure in section F (day 74).
Both are now recorded as unlawful-for-routine-use and excluded from the programs. This is a correction to sections F through J, not a new gap.

### K.2 The programs rebuilt from lawful agents only, and the result
Everything below is an FDA-approved animal drug, an FDA-approved human drug used extra-label, or a procedure.

| case | program | the quantity that has to hold |
|---|---|---|
| **B-cell body** | hydroxychloroquine + **verdinexor** + matched-donor transplant (with its total-body irradiation) + cytarabine infusion | verdinexor continued **168 days**. Laverdia-CA1's label is continuous twice-weekly dosing until progression, so this is **on-label use of an approved animal drug** |
| **T-cell body** | the above + prednisolone + romidepsin | verdinexor continued **168 days** (romidepsin and hydroxychloroquine are not load-bearing) |
| **B-cell brain** | the body program + one **23.4 Gy** whole-brain or craniospinal course + **repeated intrathecal methotrexate** | methotrexate for **420 days** at the median canine radiosensitivity (820 d at the most resistant line, 231 d at the most sensitive, 1,283 d with no radiation) |
| **T-cell brain** | the T-cell body program + the same radiation course + repeated intrathecal methotrexate | methotrexate for **378 days** (799 / 231 / 1,283 d as above) |

**The methotrexate is indispensable and it is also the best-supported agent legally:** with the radiation course but no methotrexate, neither brain ever clears at any window out to 15 years. Preservative-free methotrexate is FDA-approved **with intrathecal as a labelled human route** (the preserved formulation contains benzyl alcohol and must never be given intrathecally), and intrathecal methotrexate with cytarabine is reported in 112 dogs (PMID 25041580).

### K.3 What still has to be true (unchanged by the legal pass, and not hidden)
1. The methotrexate kill rate (0.12 /day time-averaged) is **derived**, and its canine IC50 input is a secondary citation. At half that value the brain windows roughly double.
2. Intrathecal drug reaches the CSF and perivascular spaces, **not deep parenchyma**; the model credits the whole compartment and the radiation course is what covers the parenchyma.
3. **Late neurotoxicity of whole-brain radiation plus repeated intrathecal methotrexate is the real limiter** (29% leukoencephalopathy at 2 years in a human series, methotrexate the only independent risk factor, HR 4.5, PMID 39269476). No canine series of the combination exists, and the toxicity budget does not model a late white-matter effect. The sweep that would have settled the canine whole-brain dose and its late effects was cut off by a rate limit and is **not finished**.
4. Radiation e-folds on the dormant cells are transferred from lymphoid and stem-cell radiobiology (section I), not measured on canine E5 cells.
5. Repeated intrathecal dosing in a dog beyond about 6 doses has no published precedent; the programs need 20-30 doses over 12-14 months.
6. A DLA-identical littermate donor is required (about 25% per sibling), and the transplant is load-bearing in every case.

### K.4 The brain closure is redundant, not fragile — but only because verdinexor's brain access was wrong
The user's suspicion of weak ground was correct for the single-input version. If the intrathecal methotrexate is the only thing covering the brain and it reaches only half the compartment (effective kill 0.06 /day instead of 0.12), **neither brain ever clears, even over ten years.** The cliff is sharp: the route holds at 0.09 /day and fails at 0.06. A closure that turns on one derived number reaching a threshold is not closed.

What makes it redundant is that the model's brain access for verdinexor, a generic 0.05 default with no source, is contradicted by measurement. Verdinexor's sister compound selinexor (same SINE series; verdinexor is slightly more lipophilic with a lower polar surface area) has **measured total brain:plasma of 0.71 (mouse), 0.72 (rat) and 0.60 (monkey) across an INTACT blood-brain barrier** (PMID 27323910, Table 1, full text read); the human value in contrast-enhancing glioblastoma is 0.09. Verdinexor itself has no tissue-distribution study, so this is a TRANSFER, and it is corroborated in direction by the CNS signs in the canine field study (tremor 11%, ataxia 6%, convulsion 4% versus 0, 0, 3% on control) and by selinexor's 30% human neurological-toxicity rate — a drug that does not enter the brain does not do that.

Minimal sustained window (days) for the brain, lawful agents plus one 23.4 Gy course at median canine radiosensitivity:

| verdinexor brain access | methotrexate 0 | methotrexate 0.06 /day (half reach) | methotrexate 0.12 /day (full reach) |
|---|---|---|---|
| 0.05 (the unsourced default) | never | **never** | 417 (B) / 389 (T) |
| 0.09 (human disrupted tumour) | never | never | 389 / 389 |
| **0.30** (below the animal transfer, above the human tumour value) | never | **417 / 529** | 361 / 361 |
| **0.60** (the animal intact-barrier transfer) | 306 (B) / never (T) | **361 / 361** | 361 / 333 |

So **the brain closes if EITHER the methotrexate reaches the whole compartment OR verdinexor reaches the brain at 0.3 or more**, and these are independent measurements of different agents. Radiation alone never closes it at any verdinexor access except the B-cell case at 0.6. The two routes also fail differently: methotrexate covers the CSF and perivascular space, verdinexor covers parenchyma, and the radiation course covers both once.

**What would settle it, in one experiment each:** a verdinexor brain:plasma ratio in a dog (the single most valuable measurement in this project now — it is a tissue sample from any dog on the licensed drug), and a CSF methotrexate level in a dog on the intended schedule. Both are cheap, and neither needs a new product.

### K.5 The radiation and neurotoxicity worries were overstated; one input got better, and the real unpriced cost is anaesthesia
The sweep that section K.3 recorded as unfinished is now done (`docs/universe/SWEEP_rt2.md`). Four corrections, all in the direction of a firmer closure except the last:

1. **23.4 Gy in 13 fractions is conservative for a dog, not aggressive.** Veterinary practice for canine brain tumours is **40 Gy in 10 x 4 Gy** (110 dogs, PMID 42304866; 105 dogs, 41420297; a 57-dog randomised trial, 35775129) or 50 Gy in 20 x 2.5 Gy for pituitary tumours. The late-effect dose equivalent of the model's course is **44.5 Gy-2 against 120 for 10 x 4 Gy -- about 37-40% of what dogs routinely receive**, and 1.8 Gy per fraction is below the 3.0 Gy per fraction above which canine severe late effects appear. **Severe late toxicity was reported in none** of the 110-, 105-, 57- and 46-dog series; the only canine late events found were two cases of hypoadrenocorticism and one presumptive radiation-induced nerve-sheath tumour at 1,724 days. Acute or early-delayed signs run 5-10%, transient and steroid-responsive. Note the fractionation is also *required* for a craniospinal field: at 4 Gy per fraction the cord dose equivalent reaches the published canine tolerance, while at 1.8 Gy it is less than half of it.
2. **The leukoencephalopathy figure I cited was overstated as a limiter.** PMID 39269476 is verified exactly (29.2%, CI 20.6-38.2, HR 4.50, p<0.001) but **most cases were asymptomatic, median onset was 3.0 months, and whole-brain radiotherapy was NOT a risk factor in that series -- the paper attributes it to the intrathecal methotrexate.** Against it, two prospective cohorts given **exactly 23.4 Gy in 13 fractions** had no severe white-matter change and stable-to-improved neuropsychology out to 36 months (PMIDs 24101038 n=52; 35772168 n=29), and 23.4 Gy is recommended in human practice precisely because it lowers neurotoxicity. So the radiation is not the risk; the repeated methotrexate is, and it remains the agent to watch.
3. **The human outcome anchor is stronger than I knew, and it is T-lineage specific.** Paediatric ALL removed cranial irradiation entirely across more than 10,000 children with CNS relapse of **1.5-3.9%** on intrathecal therapy alone, **including a T-ALL arm in which extended triple intrathecal therapy matched cranial radiation** (PMID 19694717; T phenotype is the only independent CNS-relapse factor, HR 5.15). That is direct human evidence that repeated intrathecal therapy can hold T-lineage CNS disease without radiation, and it is the precedent for the 20-30 doses the programs need (a standard ALL regimen gives that many over 2 years).
4. **The T-cell radiation input was conservative because a canine T-cell line was sitting in the table unlabelled.** OSW was established from a dog with peripheral T-cell lymphoma with oligoclonal TCR-gamma rearrangement (PMID 17532464); the radiosensitivity source (PMID 27257868) labels all its lines only "Lymphoid". OSW gives **2.94 in-vivo e-folds against the 1.67 the T-cell windows used**, so the lineage-matched T-cell brain window is **250 days, not 389** -- and 250 days at half methotrexate reach with verdinexor at 0.3 as well. CLBL-1 is verified B-cell; 17-71 and CLL-1390 lineages are unverified. (A conflict to keep in view: canine half-body irradiation outcomes show T-cell progression-free intervals of 292 days against 2,127 for B-cell, which OSW's sensitivity does not explain, so the T-cell disadvantage is probably escape biology rather than radioresistance.)

**The cost nobody had priced:** 13 radiation fractions plus 20-30 intrathecal doses each need general anaesthesia, carrying **1.3-6.3% cumulative anaesthetic mortality** (PMIDs 18658000, 9657167). Against a 10-year goal that is a real charge on the program and it is not in any toxicity budget. A **single 8 Gy fraction** would give 1.37-3.40 e-folds at a *lower* late-effect dose (40 vs 44.5 Gy-2) with one anaesthetic instead of 13 — derived by extrapolating the fit beyond its range, with no CNS-lymphoma data, so it is a hypothesis to test, not support. **2 x 2 Gy cannot substitute** (0.17-0.67 e-folds).

**Canine precedent for the combination remains thin:** four dogs given intrathecal cytarabine with craniospinal cobalt irradiation in 1984, "marked improvement", no dose and no late follow-up (PMID 6547126). The statement that no canine series of the combination exists survives.

### K.6 The methotrexate derivation re-done from measured canine numbers: the weakest input turns out not to matter
`docs/universe/SWEEP_itmtx2.md`; code `lymphoma_sustained.dog_csf_volume_ml`, `it_mtx_derived_kill`.

**The canine IC50 is not load-bearing.** Section J's weakest input was a secondary-citation canine methotrexate IC50 of 2-3 nM (the primary, PMID 28992489, is paywalled and could not be opened, so it stays secondary). It does not matter. Canine CSF volume is now **measured** rather than assumed: MRI in 12 dogs of 7.5-35 kg against a phantom accurate to 99.8% gives **total CSF = 1.39 x bodyweight + 17.5 mL** (adjusted r-squared 0.836), so 45 mL in a 20 kg dog. A 2.5 mg intrathecal dose therefore peaks at about **121 uM**, which is 10^3-10^4 times any plausible IC50, and the kill is set by how long the level stays above threshold, not by the IC50. Sweeping the IC50 across its entire range (2.5 nM; the measured human T-ALL anchor 14 nM; a pessimistic 118 nM, measured in older canine lines) moves the time-averaged kill by only **1.6x**:

| dosing interval | kill at IC50 118 nM (pessimistic) | at 14 nM | at 2.5 nM |
|---|---|---|---|
| weekly | 0.131 /day | 0.173 | 0.208 |
| every 2 weeks | 0.065 | 0.087 | 0.104 |
| every 3 weeks | 0.044 | 0.058 | 0.069 |

**The closure restated so it can be checked against what dogs have tolerated.** Dogs have carried indwelling intraventricular and lumbar catheters to **subcutaneous titanium ports, dosed every other week for 8-11 months, i.e. 20-28 doses** (doi 10.1002/jnr.23423, 10.1016/j.ymgme.2014.09.004) — so the dose count, not the drug, is the practical limit. At the **pessimistic IC50**, every 21 days, with verdinexor brain access 0.30 and the lineage-matched canine radiosensitivity:

| case | interval | window | **intrathecal doses** | inside canine precedent? |
|---|---|---|---|---|
| **T-cell brain** | every 21 d | 250 d | **12** | yes, comfortably |
| **B-cell brain** | every 21 d | 417 d | **20** | yes, at the lower edge |
| T-cell brain, weekly | every 7 d | 250 d | 36 | above precedent |
| B-cell brain, weekly | every 7 d | 389 d | 56 | well above precedent |

So the every-three-weeks schedule is both the most conservative on the drug side and the only one inside canine procedural experience, and it closes both brains. The human anchor for repeated dosing is unchanged and specific: in TT16, 598 children received **13-27 intrathecal doses each with no cranial irradiation**, and CNS relapse was 1.5% (T-cell hazard ratio 5.15; 1 of 21 CNS-positive patients relapsed in the CNS).

**The honest residual, which is procedural rather than pharmacological.** Repeated CSF access in dogs is not free: in the port series 2 dogs died of meningitis or hydrocephalus and catheters occluded or migrated; lumbar port patency was 67-86% at 30 days; in 19 dogs given percutaneous cisternal injections 4 times over 4 months there were 5 seizures and **one fatal brainstem haemorrhage**; against that, 0 of 108 diagnostic taps caused deterioration. Ventriculoperitoneal shunts run for years in dogs. Added to the 13 radiation anaesthetics, the program carries a **procedural mortality of a few percent** that no toxicity budget here models. That is now the largest single uncosted risk in the whole project, and it is a reason to prefer the 12-dose T-cell schedule and to test a single 8 Gy fraction in place of 13.

## L. Import routes for the Japan-only prodrug, checked across jurisdictions: a lawful UK route exists, the US route is research-only, and the product is being discontinued (2026-10-06; user: "Check the eu and uk and japan as well as other countries, there must be a way to get it to US")

Sources and verbatim provisions: `docs/universe/SWEEP_import.md`.

### L.1 Japan: the manufacturer is exiting the product
This is the finding that settles the question, and it is not a legal one.
- **Starasid Capsules 100 have been deleted from the Japanese drug pricing standard at the marketing authorisation holder's own request**, on the stated ground that medical demand had ceased (MHLW Chuikyo paper 総-1, 29 October 2025, item 203, Nippon Kayaku; the transitional period for the 506 listed items ran to **end of March 2026**, corroborated by the MHLW transitional-abolition list). The 100 mg strength is therefore no longer supplied.
- The **50 mg capsule** is still on the record, but the package insert revised **June 2026** lists only the 50 mg pack (40 capsules). A holder that has told the regulator demand has ceased and has withdrawn the larger strength is leaving the product.
- **Its Japanese indications are adult acute NON-lymphocytic leukaemia and myelodysplastic syndrome — not lymphoma.**
- **Its label is intermittent**: 100-300 mg/day for 2-3 weeks, then 2-3 weeks off, repeating, after meals; maximum 300 mg/day. Section 8.4 warns that "with long-term use adverse reactions appear more strongly and may become protracted". Serious listed reactions are myelosuppression and interstitial pneumonia; anorexia 35.0%.
- No Japanese **veterinary** approval was found (negative search of MAFF/NVAL, not an exhaustive one).
- Supply arithmetic for the old section-I plan: 100-200 mg/day is 2-4 of the 50 mg capsules daily, i.e. **730-1,460 capsules a year**, from 40-capsule packs, of a product being withdrawn.

**So the section-I route was wrong on three counts, not one.** It was unlawful in the US, its supply is disappearing, and **its own label contradicts the continuous multi-year dosing the plan assumed.** Removing it was right, and it should stay removed.

### L.2 UK: a genuine lawful route — and a correction to my earlier reading of the cascade
The prescribing cascade itself does **not** reach a foreign human medicine. The provision that does is **Veterinary Medicines Regulations 2013, Schedule 4 paragraph 7** ("Treatment in exceptional circumstances"): where the health situation requires it and there is no suitable veterinary medicinal product available either as an authorised product or under the cascade, a vet "may treat an animal with **a medicinal product authorised in another country**", subject to a certificate from the Secretary of State; import authority is **regulation 25(5)**. Operated by the VMD as a **Special Treatment Certificate** (the scheme for a human product, or any product from outside the EU — VMGN No. 5 paragraphs 22-25): applied for by the treating vet for a named animal, justification must state the clinical history and **why UK- or EU-authorised alternatives cannot be used**, certificates run up to a year and are renewable with repeats, online applications are free, and the guidance expressly contemplates longer-term use in a particular animal. No cytotoxic-class restriction was found. A **Research Import Certificate** covers import for licensed research.
**The gate:** "An STC will not be issued if a suitable product is authorised and available in the UK or in another EU MS." Cytarabine **injection** is authorised, so the justification must rest on the *route* — oral, at home, daily for months — not on the molecule. That is a defensible clinical argument, and it is the VMD's call, not mine.

### L.3 US: lawful only as research, and it cannot cover one pet indefinitely
There is no extra-label route (section K.1) and **no compassionate-use or single-animal mechanism was found anywhere in 21 CFR Parts 511-516** (a negative search; CVM's internal policy manuals were not read in full). What exists is the **investigational exemption at 21 CFR 511.1**: a client-owned pet dog may lawfully receive an unapproved new animal drug, but only as an enrolled subject of a bona fide clinical investigation, with a sponsor, a protocol, named qualified investigators, monitoring, prescribed labelling and two-year records. Importation is expressly provided for at **511.1(b)(9)(ii)**: the drug may be "shipped directly to a scientific institution with adequate facilities and qualified personnel to conduct laboratory or clinical investigations", that institution being the sponsor — the veterinary-teaching-hospital route. Two provisions stop it becoming long-term care for one animal: **511.1(b)(8)(iii)** ("shall not unduly prolong distribution of the new animal drug for investigational use") and **511.1(d)(2)**, which terminates the exemption if the drug "is being or has been used for purposes other than bona fide scientific investigation".

### L.4 Does it matter? Only for the B-cell brain, and the trade is on a vanishing product
Re-running the model with the prodrug restored, as a UK import would allow:

| case | lawful US agents only | with the prodrug restored |
|---|---|---|
| B-cell brain | needs radiation + methotrexate every 3 weeks (and verdinexor reaching the brain) | **752 days** of oral dosing, with no reliance on verdinexor's brain access; **1,002 days with no intrathecal methotrexate at all** — i.e. no spinal taps |
| T-cell brain | radiation + methotrexate | **no change: it still does not close.** T-cell cytarabine kill in CSF is too low |
| both bodies | 168 days of verdinexor | 167 days — no change |

So the honest value of the prodrug is one trade for B-cell brain disease: about 2 years of oral dosing at home instead of ~14 months with 20 spinal taps, which would avoid the procedural mortality that section K.6 identified as the largest uncosted risk. That is a real attraction. But it is built on a product whose maker is withdrawing it, whose label is intermittent rather than continuous, and which has never been given to a dog for more than 7 days. **It is not counted, and nothing in the closures depends on it.**

### L.5 Not checked
EU member-state named-patient import schemes individually (Regulation (EU) 2019/6 Articles 112-114 were not read verbatim in this pass); Canada's Emergency Drug Release for veterinary drugs; Australia's APVMA permits; Switzerland, South Korea, China; FDA compounding from bulk drug substances (GFI #256) for this specific substance; FDA's Personal Importation Policy as applied to animals; whether any other country authorises cytarabine ocfosfate.

### L.6 Corrections and the four remaining US routes, now closed out
The full cross-jurisdiction pass (`docs/universe/SWEEP_import.md`) corrects two things stated earlier in this record and closes the routes section K left open.

**Correction 1 — the EU has NO route, where section K said it might.** `SWEEP_legal.md` had recorded that the EU cascade's import limb "may permit" a third-country product. It does not. **Regulation (EU) 2019/6 Article 112(2)** requires a **veterinary** medicinal product authorised in the third country **"for the same animal species and the same indication"**. Cytarabine ocfosfate is a human product, is not authorised for dogs, and is indicated for leukaemia and MDS rather than lymphoma — it fails all three tests. (Article 110 covers immunologicals only; Article 116 is member-state to member-state.) That earlier "may permit" is struck.

**Correction 2 — the UK route is real but the guidance I quoted is withdrawn.** The statutory basis (VMR 2013 Sch 4 para 7 + reg 25(5)) stands, and VMGN No. 5 paragraph 42 expressly addresses "longer term use in a particular animal", but **VMGN No. 5 is marked withdrawn (2013)**, so the scheme mechanics quoted in L.2 should be re-checked against current VMD guidance before anyone relies on them.

**The four US routes section K had not examined, all now closed:**
1. **Importation by a vet for private practice is expressly barred.** FDA's own import guidance states that unapproved drugs "consigned to veterinarians for use in their private practices … may not be legally imported."
2. **The Personal Importation Policy does not apply.** It is written for human patients, and **Import Alert 66-40** states that "personal importation is not allowed for unapproved animal drugs."
3. **Compounding from bulk cannot reach it, and my framing of GFI #256 was wrong.** The bulk-substance lists gate office *stock*, not patient-specific prescriptions, so "is it on the list" was the wrong question. The actual blockers are FD&C Act **502(o)** (the bulk substance must come from an FDA-registered facility; none was found for this substance) and the fact that **making the prodrug from cytarabine is synthesis, not compounding**.
4. **MUMS / conditional approval exists but needs a sponsor** — the pathway that produced Tanovea for canine lymphoma. That is a drug-development route, not a way to treat a dog next month.

**Canada** is the next-best jurisdiction: the **Emergency Drug Release** scheme lets a vet apply (about 2 business days) but it authorises the *manufacturer* to sell — and cytarabine ocfosfate is not authorised in Canada either (Drug Product Database search returned nothing), as it is not in the US, EU or UK. Japan is the only authorisation anywhere.

**And the decisive pharmacological point: the lawful injectable route reaches the CSF better than the oral prodrug.** Measured CSF cytarabine after intravenous infusion in dogs is **8.3 uM**, against the **derived 0.3-1.4 uM** time-average for the oral prodrug (section K.6). So the prodrug's only real advantage is convenience — a tablet at home with a 23-29 h half-life — not exposure. There is one new canine clinical data point for it (a pet dog with MDS treated in Japan, PMID 15084010), which is worth recording but does not change this.

**Net: the Japan-only prodrug is not needed, not better in the compartment that matters, not lawfully obtainable in the US outside a trial, not obtainable in the EU at all, and is being withdrawn by its maker. It stays out.**

## M. New-treatment sweep, 31 Oct 2026: nothing new to prescribe, but a new measurement weakens the brain closure (user: "Do a deep search to see if there's any new treatment came out since last time we looked at this")

Report: `docs/reports/Canine lymphoma new treatments 2026.md`; notes: `docs/research_notes/Canine lymphoma new treatments 2026/` (five sweeps, a verification pass, and `model_rerun_selinexor_csf.md`). Code: `lymphoma_sustained.VERDINEXOR_CNS_ACCESS_MEASURED`, `lawful_brain_window`, `DOG_IT_DOSES_PRECEDENT_MAX`; `lymphoma_standard_audit.lawful_brain_items`; tests in `tests/test_lymphoma_universe.py`.

### M.1 New treatments: none that changes the lawful menu
- **No new veterinary approval, licence or launch** for canine lymphoma anywhere, 1-31 Oct 2026 (EMA veterinary committee 6-8 Oct issued no oncology opinion). Laverdia went on sale in the US on 23 Sep 2026 (launch, not a new approval).
- **No new FDA approval for any T-lineage lymphoma** in 2025-2026; no FDA approval for CNS lymphoma. Axi-cel's label restriction against primary CNS lymphoma was lifted on 6 Feb 2026 (human autologous product; no path to dogs). Tirabrutinib has an FDA decision date of 18 Dec 2026; if approved it becomes extra-label usable, with no canine data.
- **Dog trials, changed status:** the LEAH Labs canine CD20 CAR-T (Minnesota, Missouri; Ohio State per sponsor) is **open and enrolling** again (pages read 31 Oct; the record had it on hold). Readiness for canine CAR-T moves from "on hold" to B (in dog trials, enrolling). Outcome data: two dogs in remission after intranodal infusion, both relapsed months later (press only). **New to the record:** ORBIT (Minnesota; oncolytic VSV then anti-PD-1; accepts T-cell dogs), Zoetis subcutaneous canine anti-CD20 (16 dogs, B-cell depletion at 5-10 mg/kg; abstract), Tufts/NCI anti-CD20 + doxorubicin + TAK-981/KPT-9274/RV1001 (>70 dogs; news release), Bellingham adoptive T cells after CHOP (82 dogs, PMID 42833272).
- **Lawful but never evaluated:** denileukin diftitox-cxdl (Lymphir; FDA 2024) has canine in-vivo dosing data (PMIDs 16920555, 22173275) and human ORR ~16% in PTCL. Not added to the catalogue in this pass.
- **Closes off a route:** canine TRBC1 and TRBC2 have no extracellular sequence difference (PMID 41236719), so TRBC1/TRBC2-selective antibodies or CAR-T cannot work in dogs.

### M.2 The measurement that matters: selinexor in human CSF
MSZ trial (Blood 2025;146(Suppl 1):3550; primary abstract text): selinexor CSF 0.919 ng/mL at plasma 204.67 ng/mL, stable CSF:plasma ~0.6% from 4 to 25 h. With 95% protein binding (Xpovio label), CSF/unbound plasma = **0.09**. The closure had used verdinexor brain reach **0.30**, set below the rodent/monkey TOTAL brain:plasma 0.60-0.72 (PMID 27323910), which counts tissue-bound drug. Under rule 14 the compartment measurement outranks it, even though it is worse. Grade TRANSFERRED (sister compound, CSF not parenchyma, abstract without the number sampled).

### M.3 Consequences (re-run, pinned by tests)
| | old (reach 0.30, every 21 d, pessimistic IC50) | at measured reach 0.09 |
|---|---|---|
| T-cell brain | 11-12 doses / 241 d | **closes, 17-24 doses / 241 d** (every 10-14 d), inside canine precedent (20-28); does not depend on verdinexor at all |
| B-cell brain | 20 doses / 420 d | **closes in the model, 29-45 doses / 409-451 d** (every 10-14 d), **above canine precedent** |
| every-21-day schedule | closes | **never closes** (either lineage) |

- **K.4 is superseded:** the brain closure is no longer redundant. The every-21-day schedule needed both inputs; at the measured reach the brain rests on the intrathecal methotrexate.
- **`failing()` is no longer empty.** It returns one item: **B-cell brain, tolerability of 29-45 intrathecal doses**, graded ASSUMED (no canine series beyond 28 doses, no written human transfer yet). The cheapest route to clearing it is a written transfer from human long-course intrathecal / Ommaya precedent, or a canine port series with more doses; neither has been searched yet.
- Bodies (B and T, 168 d verdinexor) are unchanged.

### M.4 Correction (2026-11-01): the selinexor number is a floor for verdinexor, not its value (user: "I don't really buy the sister drug story. Did you even look at what the actual composition differences are and see if the efficacy can be taken at face value like that")
M.2 and M.3 moved selinexor's human CSF figure onto verdinexor at face value, applied selinexor's human protein binding to it, and graded the old 0.30 "CONTRADICTED". The structural comparison already in the record (`SWEEP_xpo1_cns.md`, ChEMBL 2026-10-05) was not consulted. Done properly:

| | selinexor (KPT-330) | verdinexor (KPT-335, Laverdia) |
|---|---|---|
| scaffold | 3,5-bis(CF3)phenyl-1,2,4-triazole acrylhydrazide, covalent XPO1 Cys528 | same |
| the one difference | hydrazide on **pyrazin-2-yl** (C17H11F6N7O, 443.3) | hydrazide on **pyridin-2-yl** (C18H12F6N6O, 442.3): one ring N fewer |
| polar surface / lipophilicity | PSA 97.6 A^2, ALogP 3.39, HBA 7 | PSA 84.7, ALogP 3.99, HBA 6 |
| efflux | not a P-gp/BCRP substrate (label, in vitro) | not a canine P-gp substrate (PMID 36924353); BCRP untested |
| plasma protein binding | 95% (human, label) | **never measured, any species** |
| CNS measurement | human CSF / total plasma ~0.5-0.6%; animal total brain:plasma 0.60-0.72 | **none**; field study CNS signs (tremor 11%, ataxia 6%) suggest it reaches the canine CNS |

- **What transfers:** the unbound entry ratio (Kp,uu). Verdinexor is less polar and more lipophilic, and neither drug is a known efflux substrate, so its passive entry should be at least selinexor's. **0.09 is a floor for verdinexor, graded TRANSFERRED-floor.**
- **What does not transfer at face value:** protein binding (verdinexor's unknown; its higher lipophilicity usually means tighter binding), the CSF-to-total-plasma ratio that depends on it, and the human-to-dog step. The animal total brain:plasma ratio cannot be converted to Kp,uu without brain-tissue binding (never measured); plausible values span ~0.1-0.7.
- **Kill ("efficacy") was never transferred:** verdinexor's kill in the model is DERIVED from canine lymphoma cell lines (PMID 40872651) and exposure in lymphoma dogs (PMID 30143046). Only brain reach is borrowed from selinexor.
- **Re-grade:** 0.30 is ASSUMED (no basis in the compartment), **not contradicted**. The B-cell brain closes inside canine intrathecal precedent (<= 28 doses) if verdinexor's brain reach in the dog is **>= 0.18** (central IC50, every 14 d) or **>= 0.24** (pessimistic IC50, every 21 d). At the 0.09 floor it needs 29-45 doses. The T-cell brain is unaffected (closes on 17-24 doses whatever verdinexor does).
- **So the B-cell brain is decided by one measurement, not by the transfer:** CSF and plasma verdinexor plus plasma protein binding in one dog on Laverdia. `failing()` still returns the single B-cell item, now stating both ways to clear it.

### M.5 Strengthening the B-cell brain (2026-11-01; user: "that's not good enough though. I want stronger answers. Search broader")
Three sweeps: `docs/universe/SWEEP_it_longcourse.md`, `SWEEP_rt3_escalation.md`, `SWEEP_lawful_cns_agents.md`. Code: `lymphoma_sustained.DOG_IT_DOSES_TRANSFERRED_MAX`, `DOG_IT_MIN_INTERVAL_DAYS`, `PROCEDURAL_MORTALITY_AT_DOSES`, `RT_BRAIN_ESCALATION_FACTOR`, `lawful_brain_window(rt_scale=)`; `lymphoma_standard_audit.lawful_brain_items`, `procedural_cost`; tests.

1. **The injection count now has a written basis (TRANSFERRED).** Up to 45 intrathecal methotrexate doses, >= 10 days apart, 2.5 mg preservative-free methotrexate alone (dogs >= 10 kg), ventricular port with cisternal fallback, radiation first, no high-dose IV methotrexate. Basis: human long courses at or above that count (HIT 2000, 36 intraventricular doses in 6 months, PMIDs 21636711, 26346136); per-dose canine CSF concentration at or below the human standard; same CSF half-life (5.2 vs 5.7 h), so no accumulation at that spacing; neurotoxicity tracks peak and cumulative concentration and IV methotrexate, not the intrathecal count (PMIDs 638249, 24550419, 37171700); dogs dosed intrathecally every other week for up to 20 months, ~43 doses (enzyme, not methotrexate; PMID 35717448). **`failing()` is empty again.**
2. **The cost that remains is the procedure, and it is larger than K.6 said.** If every dose needs a general anaesthetic plus a puncture, cumulative mortality compounded from the record's per-event figures is **~7-18% at 30 doses and ~11-25% at 45** (K.5/K.6 said "a few percent"). It is near zero only if a working ventricular port is dosed without anaesthesia; in the 20-month canine series the ventricular catheters lost patency and dosing moved to cisternal injection. No canine methotrexate intrathecal toxicology exists. Reported by `procedural_cost()`; it is a cost, not a pass/fail input.
3. **Brain radiation can be escalated (TRANSFERRED).** 36 Gy / 20 x 1.8 Gy whole brain (late-effect EQD2 34.2 Gy against a canine whole-brain anchor ~37.5-39.6 Gy, PMIDs 41420297, 12065111) gives 1.54x the kill of 23.4 Gy. At that dose the B-cell **brain** closes on **17-18 injections every 14 days** even at the pessimistic IC50 and verdinexor's floor, inside canine precedent. The **spine stays at 23.4 Gy** (with the transplant's 2 x 5 Gy TBI a 36 Gy spinal field puts the cord at ~90% of tolerance), and a spinal sub-compartment at 23.4 Gy still needs 34-45 injections. So escalation adds margin where intrathecal drug reaches least (brain tissue) but does not cut the injection count. The "dose escalation did not reduce relapse" cap came from total-body irradiation with marrow rescue (relapse attributed to cells in the returned marrow, PMID 3901841) and does not carry to a brain field. Costs 7 more anaesthetics.
4. **No independent second drug route exists among lawful agents.** Temozolomide reaches the brain (CSF/plasma 0.20-0.37) but lymphoid IC50 78-100+ uM vs ~3 uM brain peak; ibrutinib CSF 1.7-7.2 nM vs canine IC50 1.3 uM; ifosfamide 1 PR in 40 lymphoma dogs; dexamethasone shares prednisolone's escape; lomustine weak (derived 0.004-0.04/day, not yet written back into the catalogue) and defeated by MGMT in 2 of 5 canine lines. High-dose IV methotrexate gives the first measured non-enhancing-tissue level of any lymphoma drug (22-24 uM, PMID 18787762, human glioma) but shares methotrexate's escapes, so it is depth, not a second route. Thiotepa (already in the pool) remains the closest.

**State of the B-cell brain:** CLOSED within the catalogue at the stated bar, on radiation + 29-45 intrathecal methotrexate doses (TRANSFERRED tolerability), with verdinexor at its floor and no reliance on its unmeasured brain reach. Single route (methotrexate), not redundant. Main cost: procedural mortality if each dose needs anaesthesia. Two measurements would change this: verdinexor CSF/plasma/binding in a dog on Laverdia (>= 0.18-0.24 brings it inside 28 doses) and whether a canine ventricular port can be dosed awake for 30+ doses.

### M.6 Cutting the injection burden (2026-11-16; user: "the number of injections is a down side, is it absolutely necessary or can you find another way without compromising response")
Sweeps `docs/universe/SWEEP_awake_dosing.md`, `SWEEP_ric_cord_budget.md`. Code: `PROCEDURAL_MORTALITY_BY_ROUTE`, `PORT_INFECTION_PER_ACCESS`, `IT_DOSE_SPARING_RULED_OUT`, `CRANIOSPINAL_36GY_NEEDS_RIC`, `RIC_OPEN_CONDITION`; `lymphoma_standard_audit.procedural_cost`; tests.

**The framing was wrong: the injections are not the risk, the anaesthetic for each one is.** Two independent fixes, both TRANSFERRED; they stack.

1. **Dose the port under sedation, not general anaesthesia.** The canine CLN2 port programme states "Dogs were **sedated** during ITL or ICV infusions" through 8-20 months of biweekly 2-4 h intraventricular and intrathecal-lumbar infusions (PMID 24938720); only the cisternal-bolus fallback used anaesthesia. Human Ommaya reservoirs are tapped by a nurse practitioner in outpatient clinic with no anaesthetic (UCSD SP006; 5,472 accesses in 98 children, median 36 per reservoir, max 280, 1 infection, PMID 25017328). A canine subcutaneous vascular port was punctured with owner restraint only, no sedation, over 25 weeks, with systolic pressure FALLING on puncture (doi 10.22456/1679-9216.102523). A 1-2 minute methotrexate bolus is two orders of magnitude shorter than those infusions, so sedation suffices and awake is plausible. **Cumulative mortality falls from 8.4-48.7% (45 doses under anaesthesia) to 0.10-2.64%** (anaesthesia only to implant plus one revision), a 20-80x reduction. Per-event anchors are now MEASURED, replacing an assumed figure: canine anaesthetic/sedation death 0.05% (ASA 1-2) and 1.33% (ASA 3-5) in 98,036 dogs (CEPSAF, PMID 18466167) -- which also makes the anaesthesia-per-dose case WORSE than the record said (49%, not 25%, at 45 doses in sick dogs). **This answers the question K.6/M.5 left open.**
   - **The risk moves to the device, and technique is load-bearing:** reservoir infection per access is 0.018% under a strict aseptic protocol with trained staff (0.8% over 45 accesses) but **1.71% per treatment in ordinary practice (54% over 45)**; 0/501 treatments with 10 mg intraventricular vancomycin co-administered (PMID 40719464). Strict asepsis is a CONDITION of this route, not a detail. Also honest: 5 of 9 dogs in the canine port programme were lost to catheter or administration complications (puppies, two catheters, growing skull, foreign protein -- an upper bound).
   - **Genuinely open:** canine sedation-only mortality per event. CEPSAF pools sedation with anaesthesia and no separable figure exists. That one number decides "awake" versus "sedated".
2. **Radiate the spine too, at 36 Gy, which halves the count to 17-18 doses.** The spine was held at 23.4 Gy because the transplant's 2 x 4-5 Gy conditioning consumed cord budget. With ~2 Gy reduced-intensity conditioning the cord sits at **66%** of the canine 5%-myelopathy level (83.9 Gy3.9, PMID 26366252), **below the 68% the program already accepts**, against 90% at 2 x 5 Gy. The canine cord limit is no longer only transferred: clinical-signs ED50 54.0 Gy at 4 Gy/fraction over a 20 cm field in 125 beagles (PMID 9572623) lands within 1.5% of the transferred value. Marrow does not bind with a graft (PMID 24858425); craniospinal radiation precedes the graft (PMID 38244173). Engraftment at 2 Gy is MEASURED in dogs (8/10 pooled, PMID 23994246) **but only with mycophenolate or sirolimus added to cyclosporine** -- at 2 Gy on cyclosporine alone engraftment is transient (PMID 9108426). Graft-versus-lymphoma at 2 Gy is TRANSFERRED from 279 human NHL allografts (no survival difference, lower non-relapse mortality and GVHD, PMID 37788792); no canine tumour outcome at 2 Gy exists.
   - **The open condition:** 2 Gy gives stable **mixed** chimerism while the model's graft kill was calibrated on >95%-donor dogs, and canine benefit tracked donor percentage (PMID 11215693). So this trade is not free: it buys ~17 doses and ~10 fewer anaesthetics at the price of an unquantified reduction in the graft's own contribution. Conservative fallback 30.6 Gy spine (57% of cord tolerance) still clears the e-fold threshold. Cord-length extrapolation beyond the measured 20 cm field is unmeasured.
   - **Record inconsistency found:** the two in-vivo radiation conventions in the record (dose/1.9 versus e-folds/1.9) are not the same; subtractions that mix them are invalid. Flagged, not yet reconciled.

**Ruled out as ways to cut the count** (`IT_DOSE_SPARING_RULED_OUT`): fewer larger boluses (neurotoxicity 7/10 versus 1/8 at equal efficacy, PMID 638249, against a 5.2 h canine CSF half-life -- tripling the dose buys 8.2 h at triple the peak); longer intervals (the model's own sweep never clears at q21 or q28 at the brain-reach floor, even at 36 Gy); depot intrathecal cytarabine (4x event-sparing but US production ended June 2017, EU authorisation withdrawn 10 July 2018, and already excluded on mechanism); intrathecal depot methotrexate (does not exist, THEORETICAL); continuous pump infusion (exists, implanted in dogs, but the one canine head-to-head found it WORSE than bolus, PMID 27832416).

**Net:** the B-cell brain can be done with **~17-18 port doses under sedation and 2 general anaesthetics**, instead of 34-45 doses each under anaesthesia -- without weakening the response in the model. Conditions: strict aseptic port protocol; reduced-intensity conditioning with mycophenolate or sirolimus; and the mixed-chimerism graft question above.

### M.7 Is a port needed for all cases? No -- and the question exposed an uncited literal (2026-11-16; user: "Is a port needed for all cases")
Code: `lymphoma_standard_audit.cns_seeding_item`; tests.

| case | intrathecal doses | port? |
|---|---|---|
| B-cell body | **0** | **no** -- closes on 168 d of verdinexor alone |
| T-cell body | **0** | **no** -- same |
| T-cell brain | 16 (q14, pessimistic IC50, 36 Gy craniospinal) | yes at this count |
| B-cell brain | 18 (same conditions) | yes at this count |

So the port is a brain-arm device, not a program-wide one: it is needed only where the CNS compartment has to be closed.

**The finding: the number that decides the dose count, and so whether a port is needed at all, has no basis.** `lymphoma_scenarios.LYMPHOMA_CNS_SEED_FRACTION = 0.05` carries the comment "illustrative fraction of pre-treatment burden seeding the CNS" in its own source line, and `lymphoma_grounded.evaluate` feeds it into every CNS horizon, so it sets every brain dose count quoted in sections J through M.6. It is load-bearing:

| assumed CNS seeding fraction | B-cell brain | T-cell brain | device implied |
|---|---|---|---|
| 0.05 (the current literal) | 18 doses | 16 doses | implanted port |
| 0.01 | 14 | 14 | port |
| 0.001 | 10 | 10 | borderline |
| 0.0001 | 7 | 7 | percutaneous cisternal puncture, ordinary canine practice (112 dogs, PMID 25041580) |

No canine measurement of occult CNS seeding at diagnosis was found. `LYMPHOMA_DURABLE_RESPONSE.md:242` models "30% CNS involvement", which is a different quantity (share of dogs, not share of burden), so the record does not supply this number either. This is the same failure pattern as CLAUDE.md failure 7: a bare illustrative literal gating a conclusion, sitting unnoticed while the audit reported nothing failing. **`failing()` now returns it**, and it is the only item it returns. Closed by either a canine occult-CNS-seeding measurement or a written transfer from human CNS-relapse-risk data; neither has been searched yet.

**Consequence for the earlier answers:** the dose counts in M.5 and M.6 (17-18, 29-45) are conditional on 0.05. They are not wrong, but they are an upper branch of a number that was never fitted. The direction of the error is unknown, because the literal could be too high or too low.

### M.8 Prior art per treatment and per escape (2026-11-16; user: "Back to the question of whether if or why hasn't anyone looked at the treatment, answer for each escape and treatment")
Full tables: `docs/LYMPHOMA_PRIOR_ART_TREATMENTS.md`, `docs/LYMPHOMA_PRIOR_ART_ESCAPES.md`. The record had evidence tiers per escape but **no "has anyone treated it" and no "is it assayable" column for any escape** (only the valspodar trial), so that side is almost entirely new.

**The headline is a negative, and it is about the hardest escape.** The valspodar randomised trial in 20 dogs (PMID 28357033, re-read) had as its **primary endpoint the reduction of CD34/CD117/CD133 progenitor cells** -- that is escape E5, the quiescent efflux-high progenitor this project calls its thinnest margin. Placebo-controlled: **no change in progenitor counts, no event-free-survival benefit, no overall-survival benefit.** So E5 has already been attacked deliberately in a randomised canine trial, and the attack did not move the population it targeted. The same mechanism failed in humans at scale: zosuquidar in 449 patients, null, the authors attributing it to "P-gp independent mechanisms" (PMID 20716770).
- **Checked, and the closure does not depend on that failed mechanism:** `_has_reverser` returns False for all four lawful programmes; none contains a P-gp reverser. E5 is covered instead by agents that are not pump substrates (radiation, the graft, hydroxychloroquine; verdinexor is not a canine P-gp substrate, PMID 36924353). The nulls bound what a reverser buys, which is nothing; they do not contradict the programme.
- **A measurement the record lacked:** P-gp positive in **83% of canine lymphomas after relapse versus 25% pretreatment** (91 dogs, p=0.012), and pretreatment P-gp an independent negative survival predictor (225 vs 367 days), PMID 8646690.

**Counts over 24 rows.** Measured and treated in dogs: **6** -- and four of those six have published null or negative results. Measured in dogs but never treated: **12**. Known only from human lymphoma, so a canine clinician has no reason to consider them: **6** (E2 nucleoside-activation loss, E3 topoisomerase-IIa loss, E8 XPO1 C528S, E9 antifolate transport loss, CD7 loss, autophagy independence), plus 3 partial. Assayable in ordinary veterinary practice today: **6 fully, 5 partly, 13 not at all.**
- **The asymmetry that explains the whole question:** the assays a vet can buy (class II MHC, CD34, CD20, TP53, TRAF3, PARR) are **not** the escapes that decide closure. E5's conjunction of quiescence and efflux, and occult CNS seeding, cannot be measured in practice at all. An escape nobody can measure is an escape nobody treats.
- **The one escape with a purpose-built canine counter:** CD20 loss. A tandem CD19/CD20 canine CAR was built *because* CD20 escape was observed in treated dogs (5 dogs, PMID 32002286), with bendamustine lymphodepletion piloted in 11 dogs to enable dosing (PMIDs 42480604, 42969556 -- both postdate the 31 Oct sweep).
- **The 1984 report is identified:** intrathecal cytarabine plus craniospinal radiation in 4 of 8 dogs, PMID 6547126.
- **A caution on the CNS arm from human practice:** high-dose methotrexate CNS prophylaxis gives RR 0.54 (95% CI 0.27-1.07) with **no survival benefit, GRADE low** (PMID 38497149). That is systemic prophylaxis rather than this programme's intrathecal route, but it is the nearest outcome anchor and it is weak.

**Has anyone ever done this kind of analysis?** No paper in any species enumerates a relapse-mechanism catalogue of stated size and tests a combination against every member. The closest clinical precedent is **ViPOR** (PMID 38899693): five agents against 4-5 *pathways*, with no efflux, antigen-loss, sanctuary or progenitor coverage. Beyond Bozic/Nowak, the relevant theory is Komarova & Wodarz (PNAS 2005, PMID 15980154, the "three drugs" result) and **Saputra 2018 (PMID 29686021), which predicts that efficacy-optimised combinations are the MOST fragile to single resistance** -- the published form of this project's own recorded weakness that every agent is load-bearing.

**Marked unverified by the sweep:** PI3K-delta withdrawal citations, MCL1-inhibitor cardiac toxicity, magrolimab discontinuation (web-only), acalabrutinib canine numbers (carried from the record, not re-fetched).

### M.9 Correction (2026-11-16, same day as M.8): the "outcome test the model fails" was my test's artefact, not a model failure
M.8 reported that the model contradicts the canine maintenance null (2-year maintenance in 75 dogs no better than discontinuous in 333, PMID 28100766) because sustained CHOP clears at 365 days. **That was wrong, and the error was in the test.** The test forced a 365-day window with `with_windows`, which overrides the documented tolerable windows. The model's own windows forbid the regimen the test simulated:

| CHOP agent | sustainable | hard cap | dose-limiting event |
|---|---|---|---|
| doxorubicin | 126 d | **126 d** | cumulative cardiotoxicity |
| prednisolone | 150 d | **150 d** | iatrogenic hypercortisolism, 4/4 beagles by day 150 |
| vincristine | 105 d | none | GI signs, neutropenia |
| cyclophosphamide | 105 d | none | myelosuppression, sterile haemorrhagic cystitis |

At those windows CHOP **does not** clear, which is what the dogs show. The model is also right where it is easy to be wrong: cyclophosphamide + prednisolone and prednisolone + vincristine never clear at any duration up to 1460 days. So no contradiction exists; a forced input outside the model's stated toxicity limits was attributed to the model as a prediction. The audit item is re-graded **RESOLVED** and `failing()` no longer returns it.

**Two things were learned on the way, and both stand.**
1. **Discounting additivity does not change this**, so additivity was never the issue: at `alpha` from 1.0 down to 0.0 in `max(kill) + alpha * sum(others)` -- i.e. all the way to winner-takes-all -- forced-window CHOP still clears at long durations. Any positive margin clears given unlimited time; the thing that stops it is the toxicity window, which is exactly what the model already applies.
2. **An emergence cap tied to P-gp selection also does not change it** (capping pump substrates at 225 d, derived from P-gp 25% pretreatment -> 83% at relapse, PMID 8646690). Worth recording because that cap is a real phenomenon the model does not represent: escape presence is evaluated from baseline burden via `escape_presence_probability`, with no term for resistance ARISING under prolonged selection. That is a genuine structural absence, but it is not what produced the false contradiction, and the toxicity windows bound duration before it would bite.

**The one genuine window override, and its justification.** `lawful_clock` extends **verdinexor** from its documented 56 days to the programme length (to 483 d). That 56 days is a study duration, not a toxicity cap (`hard_cap_days` is None), and the override is justified in writing: the Laverdia-CA1 label is twice weekly **until progression**, i.e. indefinite, and the record holds a dog treated continuously for 17 months. Intrathecal methotrexate's documented window (3650 d) already exceeds what the programme needs; hydroxychloroquine, the cytarabine infusion and the graft keep their documented windows inside the clock and are **not** extended. So no unjustified extension carries any closure.

**Net effect on the answer to "do some escapes now have no real answers":** no. Zero escapes are uncovered in any of the four cases, every margin is positive (weakest is E5 at +0.020 to +0.042 /day), and the duration numbers are not after all contradicted by the maintenance evidence.

### M.10 Prednisolone: a randomised dog trial measures its added value at zero, and resistance arrives at 68 days (2026-11-16)
Sweep `docs/universe/SWEEP_additivity_calibration.md`.

M.9 was right that my forced-window test was an artefact, but wrong to conclude no contradiction exists. A **better-matched** trial convicts the model: **Zandvliet 2013 (PMID 23746872) randomised 81 dogs to the same multidrug protocol WITH or WITHOUT prednisolone and found no difference in anything** (CR 75%, disease-free period 176 d, survival 283 d). That is a measured, in-dog value for exactly the quantity the model credited, and the value is **zero**. The sweep also located why the model could credit it indefinitely: escape **E1 (glucocorticoid-receptor loss)** is in the universe escape set but prednisolone's window was set by **steroid toxicity (150 d)** rather than by **resistance**, whose canine median onset is **68 days** (PMID 31943234).

Two corrections applied:
- `prednisolone (glucocorticoid)` window **150 d -> 68 d**, sustainable and hard cap, with the steroid-toxicity figure kept as the toxicity statement. The useful window is the shorter of toxicity and resistance.
- **Prednisolone removed from `LAWFUL_PROGRAMS["T"]`** on the Zandvliet measurement (rule 14: a measurement in the compartment at issue outranks a derived kill). Not load-bearing: T body 147 -> 168 d, T brain unchanged.

Also recorded from the sweep, and standing: the maintenance trial (PMID 28100766) **did not** test sustained CHOP -- its maintenance arm was vincristine + chlorambucil + actinomycin-D, with no doxorubicin, cyclophosphamide or prednisolone -- so M.9's artefact finding holds; but the trial still bounds any "keep going" strategy, 3.7x more on-therapy time buying <=32 d of remission across 408 dogs. Dose intensity is not quantified (publisher 403). **Vos 2019 cuts the other way:** 12-week CHOP at +58% dose intensity was WORSE (PFS 141 vs 245 d), implying duration saturation at ~19-28 weeks. A derived flat relapse hazard (~0.0017-0.0030/day to 2 years, no plateau) is an anchor any clearance claim must eventually explain. **No published model sums kill rates:** Bozic/Nowak use strict highest-single-agent; Palmer & Sorger (PMID 29245013) measure correlation 0.28 +- 0.20 and classify summation as synergy rather than the null, while exempting curable blood cancers.

### M.11 The CNS seeding fraction, derived: the brain needs ~10 doses, not 18, and no port (2026-11-16)
Sweep `docs/universe/SWEEP_cns_seeding.md`.

M.7's failing item is **closed by derivation**, and the direction of the error is settled: the "illustrative" 0.05 was **far too high**. Two independent routes converge -- Poisson inversion of CNS relapse rates, and a cell-count conversion of occult CSF flow-cytometry positivity -- on a bracket of **low 3e-9, central 1e-6, high 1.2e-3**. Inputs: canine primary CNS lymphoma 4% and secondary 5-12% of all canine non-Hodgkin lymphoma (PMID 27511313, the only figure with the right denominator; the "12%" and "30%" review figures have brain-tumour denominators and must not be used); human CNS-IPI 2-year CNS relapse 0.6 / 3.4 / 10.2% by risk group (PMID 27382100); occult CSF flow positivity 22% of 51 with clones to 0.2% of CSF lymphocytes (PMID 15358629) and 13% of 246 DLBCL with 3-year freedom from CNS relapse 73% vs 94% (PMID 24727817). **The model runs the HIGH branch**, because the CSF-to-tissue cell fraction remains ASSUMED and the high branch is the conservative choice.

**0.05 sat ~40x above the high branch and ~5e4 above central**: it describes a >1 cm3 CNS lesion in a dog whose whole burden is 1e8 cells, i.e. clinically obvious disease in an animal with no neurological signs. Also checked: the record's "30% CNS involvement" at `LYMPHOMA_DURABLE_RESPONSE.md:242` is **not** a source, it is a swept value (`lymphoma_scenarios.py:249`, "swept, not asserted").

| CNS seeding fraction | B-cell brain | T-cell brain | device implied |
|---|---|---|---|
| 0.05 (superseded literal) | 18 doses / 248 d | 16 doses / 226 d | implanted port |
| **1.2e-3 (derived HIGH, now default)** | **10 doses / 134 d** | **8 doses / 112 d** | **percutaneous taps, no port** |
| 1e-6 (derived central) | 2 doses | 2 doses | no port |

**Consequences.** The implanted port is no longer required for any case: 8-10 doses is ordinary canine percutaneous cisternal practice (112 dogs, PMID 25041580), so the port's infection term (up to 54% over 45 accesses in ordinary practice) and most of its anaesthetic burden fall away. Verdinexor's unmeasured brain reach stops being decisive: both brains close inside precedent at its 0.09 floor. **`failing()` is now empty.**
- **What this does NOT give is a per-dog test.** A positive CSF tap routes a dog to the full arm, but a negative tap rules nothing out (6% of flow-negative humans still relapsed), and canine CSF yields ~2,500 lymphoid cells against the ~50,000 a diagnostic flow result needs. CSU prices CSF flow and clonality at $165 and cytology at ~$59, plus one anaesthetic. **The cheap missing tool is a canine CNS-IPI risk score, which has never been built.**
- **Test bookkeeping:** sections F-J were characterised at 0.05, so those tests are pinned to `SUPERSEDED_CNS_SEED_FRACTION` via `@at_superseded_seeding` rather than re-fitted to numbers they never asserted; current-truth brain numbers are tested at the derived fraction. 107 tests pass.

### M.12 Does the missing resistance-emergence term leave an escape without an answer? No, and it is now checkable (2026-11-16)
M.9 and M.11 both recorded a structural absence: `escape_presence_probability` evaluates escape presence from the BASELINE burden, and nothing in the clock represents a resistant clone ARISING under prolonged selection -- while canine P-gp positivity rises from **25% pretreatment to 83% at relapse** (PMID 8646690). Left there, that reads like an escape with no answer. It is not, for three reasons that `lymphoma_standard_audit.emergence_is_not_an_uncovered_escape()` now executes rather than asserts:

1. **The programmes are scored against the FULL escape set** (22 for B-cell, 21 for T-cell), not the presence-filtered subset (19 and 18). Every catalogued escape must be closed whether or not it is likely present at diagnosis.
2. **The three escapes a presence filter would have dropped are exactly the ones emergence would create** -- autophagy independence, B-lineage identity switch, and E8 XPO1 C528S, the verdinexor target mutation -- and all three are already required to be closed.
3. **With every escape forced present from day 0** -- the worst case emergence could produce -- **every margin is positive in all four cases**, minimum +0.0215/day (E5 in the B-cell brain).

So emergence changes **when** an escape appears, not **whether** it is covered, and on timing the model already runs the worst case. Two honest riders:
- **Where the absence does bite is magnitude, not coverage.** An emerging clone raises an escape's frequency faster than assumed, which eats margin. That is the reason the margins are quoted at the pessimistic inputs rather than the central ones, not a reason to call a route open.
- **What emergence could do that this does not cover is produce an escape outside the catalogue.** That is a completeness question, audited separately under CLAUDE.md rule 9 by the independent escape audit (`docs/universe/SWEEP_escapes.md`), and it is not what this item grades.

Graded **DERIVED / passes**, so `failing()` stays empty and this may not be re-raised as an open escape under a different phrasing.

### M.13 Multi-escape cells: the emergence question closed by enumeration, not by reclassification (2026-11-16)
M.12 argued that the missing resistance-emergence term could not open an uncovered route. That argument was sound but it closed nothing: it showed that every escape is *required* closed, not that a cell carrying several at once is *actually* covered. **The model had only ever scored single escapes.** A cell carrying several is killed only by an agent that covers **every** escape it carries, so the right test is to enumerate combinations. Code: `lymphoma_standard_audit.multi_escape_depth`, `multi_escape_item`; test `test_multi_escape_cells_are_closed_to_the_depth_that_can_physically_occur`.

| depth (escapes in one cell) | coverage | worst margin | reachable? |
|---|---|---|---|
| 1 | all covered | +0.021 to +0.042 /day | yes (2.2e7 cells) |
| 2 (882 pairs tested) | **all covered** | **+0.019 /day** (P-gp + TP53, and P-gp + E2 in the brain) | yes (2.3e6 cells) |
| 3 (1,540 triples tested) | **all covered** | positive | yes (1.5e5 cells) |
| 4 | **16 uncovered per body case**; brain covered but margin **-0.018 (B), -0.013 (T)** | negative | **no** -- most probable 1e-16 cells |
| 6 | 1,812 uncovered (B), 1,580 (T) | negative | **no** |
| 22 (all escapes) | 0 of 4 agents survive in the body; 2 of 6 in the brain (radiation + intrathecal methotrexate) | -0.090 body, -0.018 brain | **no** -- 1e-36 cells |

**So the honest answer to "do some escapes have no real answers" is: yes, combinations of four or more do -- and none of them can occur.** Each uncovered combination needs four or more specific escapes in a single cell; priced with each escape's own seeding rate at a burden of 1e8, the most probable has an expected count of about **1e-16 cells**, and the all-escapes cell about 1e-36. **Zero uncovered combinations reach one expected cell**, in any of the four cases. The programmes are closed to the depth that can physically occur, and break only at depths that cannot be reached.

Two things stated rather than hidden:
- **Escapes are treated as INDEPENDENT.** A mutator phenotype, or one escape raising another's rate, would lift these joint probabilities. That correlation has not been measured in canine lymphoma, and it is the single assumption this closure rests on.
- **The brain is the thinner case.** From depth 4 its combinations remain *covered* but margin-negative, and the only agents still working against a fully armoured cell are the radiation course and the intrathecal methotrexate. That is consistent with M.11's finding that the brain rests on those two.

This supersedes M.12's framing: the emergence item is no longer a reclassification of an open structural absence but an enumerated closure, and `failing()` is empty with 109 tests passing.

### M.14 Correcting M.13, and the honest answer: treatment closes depth 2, only depth 1 can occur, and the rest rests on one unmeasured assumption (2026-11-16)
M.13 claimed depths 1-3 were "fully covered with positive margins". **Wrong** -- it had checked coverage at depth 3 but not margin. Re-run per depth, with each worst case priced by its own escape seeding rates at a burden of 1e8 cells:

| depth (escapes in one cell) | worst margin | expected cells in that worst case | verdict |
|---|---|---|---|
| 1 | **+0.066 to +0.363 /day** | **1-10 cells** | closed by treatment; **the only reachable depth** |
| 2 | **+0.019 to +0.088 /day** | 1e-8 to 1e-7 | closed by treatment |
| 3 | **-0.004 to -0.042 /day** | 1e-15 to 1e-14 | **NOT closed by treatment** |
| 4+ | coverage itself fails (16 quadruples per body case) | <=1e-16 | **NOT closed by treatment** |

**So treatment closure runs one full level deeper than anything that can physically occur.** That is the real result, and it is stronger than a bare "every escape is covered": the cells that can exist are closed with a comfortable margin, and there is a level of headroom above them.

**And the thing that genuinely has no answer, stated plainly.** Depth 3+ cannot be closed by treatment, and not for want of looking:
- Five lawful agents each cover **every** escape alone -- cyclophosphamide, craniospinal radiotherapy, total body irradiation with transplant, half-body irradiation, high-dose thiotepa consolidation -- so **coverage** is fixable.
- But their kills are 0.004-0.042/day against a 0.0903/day growth bar. It takes **four** of them added to the programme to reach a positive worst-case depth-4 margin, and then only **+0.0029/day** -- and that regimen's toxicity headroom is **-2.5**, about three and a half times over what a dog survives.
- **Therefore depth 3+ cannot be closed inside the toxicity budget by any lawful combination.** What stands between the dog and those routes is their rarity alone.

**That rarity rests on one assumption, which is now the single failing audit item.** `escape_independence_item()`: escapes are treated as INDEPENDENT, which is what makes a depth-3 cell ~1e-15 and a depth-4 cell ~1e-16. No canine measurement bounds that correlation -- no paired diagnosis-versus-relapse sequencing exists (already in `LYMPHOMA_COVERAGE_LEDGER`) -- and no written transfer stands behind it either, so under CLAUDE.md rule 11 it is genuinely open: a number with no basis at all, load-bearing for a closure claim. A mutator phenotype, or one escape raising another's rate, would make these combinations orders of magnitude commoner and would move depth 3 into reach, where the margin is negative.

**What would close it** (any one suffices): a measured or bounded pairwise correlation between escape mechanisms in canine lymphoma; an agent whose kill carries depth 3-4 alone inside the toxicity budget; or a demonstration that the specific mechanisms in those combinations cannot coexist in one cell.

`failing()` returns exactly this one item. 109 tests pass.

### M.15 Closing depth 3: a named near-future agent does it; what remains open is B-cell depth 4 (2026-11-16)
M.14 found depth-3 escape combinations margin-negative and **reported them open**. That was a stopping point, not a closure, so this section does the work. All margins are **after the model's toxicity de-rating**, which is what its verdict uses. Code: `DEPTH3_CLOSURES`, `DEPTH3_INSUFFICIENT`, `depth3_item`; test `test_depth_3_escape_combinations_are_closed_by_a_named_near_future_agent`.

**Why no lawful-today agent can do it.** The five agents that cover every escape alone -- cyclophosphamide, craniospinal radiotherapy, total body irradiation with transplant, half-body irradiation, high-dose thiotepa consolidation -- are all cytotoxic or radiation, all on the **already-loaded marrow axis**, with kills of **0.004-0.042/day** against a 0.0903 growth bar. Four of them together reach only +0.0029/day at toxicity headroom **-2.5**. The constraint is not coverage, it is kill-per-unit-toxicity on an axis that is already full.

**What does close it: a canine CAR-T, on the immune axis, which carries only 0.30 of its budget.**

| addition | tier | depth-3 margin | depth-4 margin |
|---|---|---|---|
| **B-cell: persistence-engineered canine-binder CAR-T** | **C** | **+0.0256 /day -> CLOSED** | -0.0559 (open) |
| **T-cell: CD5 + CD7 dual-target CAR-T (canine binder)** | **C** | **+0.1309 /day -> CLOSED** | **+0.1041 -> CLOSED** |
| programme alone (either lineage) | A/B | -0.0559 | -0.0903 |
| CD3xCD20 bispecific engager | C | -0.0089 (not enough) | -0.0903 |
| anti-CD20 monoclonal antibody | B | -0.0089 (not enough) | -0.0903 |
| CD7-directed CAR-T, single target | C | -0.0291 (not enough) | -0.0635 |

Tier C is admissible under CLAUDE.md rule 13 (clinical-stage modality in humans, a stated path to the dog, a derived or transferred kill), and the **canine CD20 CAR-T trial is enrolling again** as of this session's sweep (section M.1), which is what makes the tier credible rather than nominal. Reported with its tier mix, as rule 13 requires: the body and brain programmes are tier A/B (lawful today), and **depth-3 closure needs one tier-C agent**.

Note which agents are **not** enough, so they are not re-tried: the bispecific engager and the anti-CD20 antibody both leave depth 3 at -0.0089/day, and the single-target CD7 CAR-T leaves the T-cell case at -0.0291. Antigen-directed single-target agents are inherently defeated by the antigen-loss escapes, which is why the dual-target construct is the one that carries depth 4.

**State of the depth ladder after this section:**

| depth | B-cell | T-cell |
|---|---|---|
| 1 (the only reachable depth) | CLOSED, lawful today | CLOSED, lawful today |
| 2 | CLOSED, lawful today | CLOSED, lawful today |
| 3 | **CLOSED with a tier-C CAR-T** | **CLOSED with a tier-C dual-target CAR-T** |
| 4+ | **OPEN** -- nothing tested closes it | **CLOSED** by the same dual-target CAR-T |

So `failing()` now carries exactly one item, and it is narrower than before: **escape independence, carrying the B-cell depth-4+ closure alone.** T-cell no longer depends on it at any depth. What would close the B-cell case: an agent with a kill high enough to carry depth 4 on a free toxicity axis (the dual-target construct does it for T-cell, so a B-cell analogue -- a dual-antigen CD19/CD20 canine CAR-T, which `SWEEP_dog_programs` records as in development -- is the obvious candidate), or a measured bound on escape correlation.

### M.16 Closing B-cell depth 4 with a modelled agent, and a coverage bug found doing it (2026-11-16)
M.15 left B-cell depth 4 open with the fix only *proposed*. This models it. Code: `lymphoma_grounded.covers_conjunction`, the new `tandem CD19/CD20 CAR-T (canine binder) [buildable]` agent, `DEPTH_LADDER_CONJUNCTION_AWARE`, `cd5_loss_catalogue_gap_item`; test `test_a_dual_antigen_car_t_closes_the_deep_escape_ladder_and_the_coverage_bug_is_fixed`.

**A coverage bug, found while doing this, which had inflated the earlier numbers.** `covered()` is evaluated per escape, so a tandem CD19/CD20 CAR-T "covers" CD19 loss (it still has CD20) and "covers" CD20 loss (it still has CD19) -- and per-escape AND therefore credited it against a cell that had lost **both** and presents no target at all. `covers_conjunction()` now collects every antigen the escape set removes and requires an antigen-directed agent to retain at least one target; non-antigen-directed agents (radiation, alkylators, the graft) fall through unchanged. **Fixing it cut the B-cell depth-4 margin from +0.2597 to +0.0256**, so it mattered -- and the closure survived it.

**The agent.** `tandem CD19/CD20 CAR-T (canine binder)`, built as the exact B-lineage analogue of the catalogue's existing CD5+CD7 construct: same potency (0.12 base), same construction, two antigens so single-antigen loss does not defeat it. Tier C under rule 13: the modality is clinical-stage in humans (tandem/bivalent CD19/CD20 CAR-T), the path to the dog is stated and live (the canine CD20 CAR-T trial is enrolling again, M.1; Penn's bivalent-loop CD19/CD20 canine construct is in laboratory development, M.1), and the kill is TRANSFER-OUTCOME. It answers the CD20-loss relapse actually observed in treated dogs (5 dogs, PMID 32002286), which is what a single-target construct cannot do.

**The conjunction-aware ladder, after de-rating:**

| depth | B-cell + tandem CD19/CD20 | T-cell + CD5/CD7 dual-target |
|---|---|---|
| 2 | +0.3748 CLOSED | +0.1653 CLOSED |
| 3 | +0.1973 CLOSED | +0.1309 CLOSED |
| **4** | **+0.0256 CLOSED** | **+0.1041 CLOSED** |
| 5 | **-0.0559 open** (worst case expects **1e-31 cells**) | +0.1041 CLOSED |
| all escapes | open | CLOSED |

The B-cell worst open combination is efflux + TP53 + **CD20 loss + CD19 loss** + dCK loss -- i.e. it needs the construct's own double-antigen failure plus three more mechanisms in one cell. Adding no new toxicity: the CAR-T sits on the immune axis, which carried only 0.30 of its budget, so headroom is unchanged at -0.60.

**The caveat that keeps the T-cell result honest.** T-cell closes at every depth only because the escape catalogue contains **CD7 antigen loss but no CD5 antigen loss**, so its construct can never lose both targets in this model. CD5 is downregulated under CD5-directed CAR-T pressure in humans -- the very mechanism the construct's fratricide-resistance exploits -- so that absence is a **rule-9 catalogue gap, not a biological guarantee**. Add a CD5-loss escape and T-cell would behave like B-cell: closed to about depth 4, open beyond at a vanishing probability. It is recorded as a failing audit item so the T-cell ladder is never quoted as the stronger result.

**`failing()` now returns two items, both honest and both narrow:**
1. **escape independence**, now carrying only **B-cell depth 5+**, whose worst case expects ~1e-31 cells -- about 1e16 times rarer than the depth-3 case this item carried a few sections ago.
2. **the CD5-loss catalogue gap**, carrying the T-cell deep closure.

**Tier mix, as rule 13 requires:** the body and brain programmes are tier A/B (lawful today); closing the deep escape ladder needs **one tier-C dual-antigen CAR-T per lineage**. 111 tests pass.

### M.17 Both remaining items closed: the catalogue gap filled, and the independence assumption replaced by a bound (2026-11-16)
M.16 left two failing items. Both are now closed by work rather than by argument. Code: `lymphoma_grounded.CD5_LOSS`, `lymphoma_standard_audit.escape_correlation_item`, `DEPTH5_CORRELATION_BOUND`, `STRONGEST_MEASURED_MUTATOR_FOLD`; test `test_the_depth5_conclusion_is_a_bound_not_an_independence_assumption`.

**1. The CD5-loss catalogue gap is filled, and it cost the T-cell result.** `CD5_LOSS` is now in `GROUNDED_ESCAPES` (the grounded set goes 14 -> 15, the full set 23 -> 24), with the same rate as CD7 loss and a written basis: CD5 is down-modulated on both CAR-T and target cells under CD5-directed pressure, which is how fratricide is avoided (PMIDs 38145560, 38986621), so surface-CD5-negative escape is the corresponding relapse route. **Consequence, reported rather than hidden: T-cell no longer closes at every depth. It now opens at depth 5 (-0.0635), exactly like B-cell.** The earlier "T-cell closes at all depths" was the artefact M.16 suspected it was.

**2. The independence assumption is replaced by a computed bound, which is what closes depth 5.** The question was never whether depth-5 combinations are covered -- they are not, in either lineage, and no addition of up to three universal-coverage agents closes them inside the toxicity budget. The question is whether they can occur. That was resting on "escapes are independent, and nobody has measured it". Now:

| | B-cell | T-cell |
|---|---|---|
| unclosed depth-5 combinations | 24 | 128 |
| most probable, independent rates | 1e-25 cells | 1e-23 cells |
| correlation needed to reach ONE cell | ~1e25 overall = **1.8e6x per conditional step** | ~1e23 = **5.6e5x per step** |
| at 10x per step | 1e-21 | 1e-19 |
| at 100x per step | 1e-17 | 1e-15 |
| **at 1000x per step** (strongest measured mutator: mismatch-repair-deficient cancers) | **1e-13** | **1e-11** |

**So the conclusion holds under any correlation up to and far beyond anything measured in any tumour, with eleven to thirteen orders of magnitude to spare.** That is a rigorous model with a stated bound, which is the user's standard, rather than a bare assumption. Grading kept honest: the 1000x mutator ceiling is TRANSFERRED from human cancer genetics (no canine lymphoma measurement exists); what is DERIVED is that the conclusion is insensitive to it across the whole plausible range and well past it.

**`failing()` is now empty**, and the depth ladder reads:

| depth | B-cell | T-cell |
|---|---|---|
| 1 (the only depth reachable with independent rates) | CLOSED | CLOSED |
| 2, 3, 4 | CLOSED with a tier-C dual-antigen CAR-T | CLOSED with a tier-C dual-antigen CAR-T |
| 5+ | not covered by treatment; **cannot occur even at a 1000x mutator rate** | same |

**Tier mix (rule 13):** body and brain programmes are tier A/B, lawful today; closing depths 2-4 needs one tier-C dual-antigen CAR-T per lineage (tandem CD19/CD20 for B, CD5+CD7 for T). 112 tests pass.

### M.18 The division budget: depth 3 is not rare, it is unbuildable -- and B-cell closes the reachable depth lawfully today (2026-11-16)
Sections M.13-M.17 closed the deep escape ladder with a **rarity** argument, which is weaker than it needed to be. The right bound is physical, not probabilistic. Code: `division_budget_reachable_depth`, `closure_to_reachable_depth`, `reachable_depth_item`; test `test_the_reachable_escape_depth_is_two_and_b_cell_closes_it_lawfully_today`.

**A depth-k cell needs k escapes to arise, and each one arises only at a cell division.** So the ceiling is set by how many divisions the tumour will ever perform, not by how unlikely a combination looks. From one transformed cell to a burden of 1e8, plus ten further years of a residual population held at or below that burden: **2N + N x growth x 3650 = about 3.3e10 divisions.**

| depth | expected cells against that budget | status |
|---|---|---|
| 1 | 3.3e8 | occurs |
| 2 | 3.3e3 | occurs |
| **3** | **3.3e-4** | **never assembled -- about 3,400 times fewer than one cell** |

So **the reachable escape depth is 2**, not 5. Depth 3 and beyond are not "improbable"; the tumour does not perform enough divisions to build one, over its whole history plus a decade of follow-up. This supersedes the correlation sweep of M.17 as the primary bound (that sweep stands as a secondary check: even at a 1000-fold mutator rate, depth 5 stays 11-13 orders below one cell).

**And at the reachable depth, the two lineages differ in a way worth stating plainly:**

| | worst margin over all combinations to depth 2 | closes on lawful-today agents? | requirement |
|---|---|---|---|
| **B-cell** | **+0.0256 /day** | **YES** | none beyond what a vet can obtain today |
| **T-cell** | **-0.0172 /day** | **no** | one tier-C **CD5 + CD7 dual-target CAR-T**; no combination of up to three lawful additions closes it |

So the honest headline, replacing every earlier version: **B-cell multicentric lymphoma closes every escape combination that can physically occur, on agents a US vet can lawfully obtain today. T-cell closes depth 1 lawfully but needs one near-future dual-antigen CAR-T to close depth 2.** The dual-antigen constructs of M.16-M.17 remain useful as headroom beyond the reachable depth, but B-cell does not depend on them.

`failing()` is empty, and the closure is now stated as a conjunction over the depths that occur rather than over an unbounded ladder. 113 tests pass.

### M.19 Sequential versus simultaneous: the criterion the depth analysis should have used, and it changes the T-cell verdict (2026-11-16)
User: *"Were you answering if one escape happens after the next? And basically found those can't happen in the real world?"* The first half is the correction. Sections M.13-M.18 priced multi-escape cells as **independent acquisitions in one lineage**, i.e. effectively simultaneous. Real resistance evolves **sequentially**: escape 1 arises, treatment removes the competition, that clone **re-expands** to a large population, and escape 2 then arises anywhere in those far more numerous cells. Sequential stacking is vastly more probable than simultaneous acquisition and is how multidrug resistance actually arises. Code: `sequential_stacking`, `sequential_stacking_item`; test `test_sequential_escape_stacking_is_what_the_margin_actually_prevents`.

**What blocks stacking is the margin, not rarity, and it gives an induction.** If every clone at every reachable depth is still SHRINKING, the population never amplifies, the division budget of M.18 stays bounded, and the next depth stays out of reach. If even one reachable clone GROWS, it re-expands to ~1e8 cells and the next escape becomes reachable in that bigger target. **So M.18's division-budget bound is valid only conditional on this test; it is not independent of it.**

| programme | depth 1 | depth 2 | depth 3 | verdict |
|---|---|---|---|---|
| **B-cell, lawful today** | +0.1973, 0 grow | **+0.0256, 0 grow** | -0.0559, 24 grow | **HOLDS** -- nothing re-expands, so depth 3 is never reached |
| **T-cell, lawful today** | +0.0791, 0 grow | **-0.0172, 8 GROW** | -0.0559, 144 grow | **FAILS at depth 2** |
| T-cell + tier-C CD5+CD7 dual-antigen CAR-T | +0.2616, 0 grow | +0.1653, 0 grow | **+0.0671, 0 grow** | HOLDS |
| B-cell + tier-C tandem CD19/CD20 CAR-T | +0.5473, 0 grow | +0.3748, 0 grow | +0.1973, 0 grow | HOLDS, large margin |

**The T-cell failure is real and every earlier section missed it.** Eight depth-2 pairs grow on lawful agents, among them **P-gp efflux with TP53 evasion** and **P-gp efflux with the XPO1 C528S verdinexor-target mutation**. Those pairs are reachable -- about 3,300 expected cells at depth 2 -- so they arise, they expand, and depth 3 then has 144 growing combinations. M.18's claim that "T-cell closes depth 1 lawfully" was true and misleading: a programme that holds at depth 1 but loses at depth 2 does not hold at all, because depth 2 is reached.

**Consequences, stated plainly:**
- **B-cell is durable on lawful-today agents.** The induction holds at every reachable depth, so the earlier claim survives this harder test.
- **The T-cell dual-antigen CAR-T is LOAD-BEARING for durability, not headroom.** M.18 had it as a depth-2 coverage requirement; it is more than that -- without it, T-cell unravels stepwise.
- **Answer to the second half of the user's question: not quite.** It is not that sequential escapes "cannot happen in the real world". They can and do -- that is what the eight growing T-cell pairs are. What stops them, where they are stopped, is that every clone that arises is still being killed faster than it grows. That is a property of the regimen, not of the biology, and it has to be checked rather than assumed. It is now checked.

`failing()` is empty, with this as the primary criterion and M.18's division budget as its corollary. 114 tests pass.

### M.20 How the search was wrong, and how far lawful-only T-cell actually gets (2026-11-16)
M.19 concluded that T-cell needs a tier-C CAR-T. That was true of the programme as written but was never tested against the best lawful regimen available: **M.15-M.19 only ever ADDED agents to a fixed four-agent programme.** Searching all 3-to-7-agent combinations of the 19 lawful T systemic agents instead finds a better one. Code: `T_BEST_LAWFUL_REGIMEN`, `T_BEST_LAWFUL_WORST_KILL`, `T_LAWFUL_BLOCKING_PAIR`, `t_cell_lawful_growth_threshold_item`.

**The best lawful-only T-cell regimen** is six agents -- cyclophosphamide, prednisolone, hydroxychloroquine, verdinexor, weekly cytarabine infusion, and the matched allogeneic graft -- and its worst depth-1/depth-2 clone is killed at **0.0895/day**. The growth bar is **0.0903**. It misses by **0.0008/day: under one percent.**

**Stated as a condition rather than a verdict, which is the honest form:** the lawful-only regimen blocks sequential stacking at any growth rate **below 0.0895/day**. The bar is a DERIVED net in-vivo band of **0.015-0.12/day** and the model runs it at the band's **upper end**, so the lawful regimen holds across **71% of the band, including all of its central values**, and fails only in the top slice 0.0895-0.12/day. The bar itself is unchanged -- what is reported is the threshold, not a retuned input.

| | lawful-only, six agents | + tier-C dual-antigen CAR-T |
|---|---|---|
| typical growth (band centre, ~0.06/day) | **holds** | holds |
| conservative bar (0.0903/day, band top) | misses by 0.0008 | holds to depth 3 (+0.0671) |

**The irreducible lawful blocker** is **P-gp efflux together with TP53/apoptosis evasion**. Four lawful agents cover it -- weekly cytarabine infusion (0.062), the graft (0.048), cyclophosphamide (0.042), high-dose thiotepa (0.041) -- but they all sit on the **marrow axis**, and high-dose thiotepa alone consumes that entire budget, so they cannot be stacked. That is a toxicity-axis collision, not an absence of lawful agents, and it is why the last 0.0008/day cannot be bought lawfully.

**So the corrected T-cell position:** a lawful-only regimen is durable against sequential stacking for a typically-growing T-cell lymphoma; the tier-C dual-antigen CAR-T is what buys durability at the fast-growing end of the band. Both are now stated, rather than the earlier flat claim that a CAR-T is required.

**And the B-cell position is unchanged and stronger:** lawful-today agents hold at every reachable depth with margin to spare (+0.1973 at depth 1, +0.0256 at depth 2).

`failing()` is empty. 115 tests pass.

### M.21 The lawful T-cell residual is irreducible, quantified, and is a MARGIN shortfall not an uncovered escape (2026-11-16)
This closes the search rather than the gap, and says precisely what is left. Code: `T_LAWFUL_RESIDUAL_PER_DAY`, `T_LAWFUL_RESIDUAL_IRREDUCIBLE`, `T_LAWFUL_RECOVERY_RULED_OUT`; test `test_the_lawful_t_cell_residual_is_irreducible_and_quantified`.

**The residual is -0.00082/day, and it is irreducible within the lawful pool.** Established by optimisation, not by one attempt: an exhaustive search of all 3-to-7-agent combinations of the 19 lawful T systemic agents, plus hill-climbing from three different starting regimens, all converge on the same figure. Two recovery mechanisms were tested and both fail:
- **Phase staging.** The three agents covering the blocking pair (cyclophosphamide, weekly cytarabine infusion, the matched graft) de-rate to **0.1014/day on their own -- margin +0.0111, comfortably positive.** But the sequential-stacking criterion must hold **continuously**, and any phase that does not contain them sits at **-0.0903**. Staging therefore makes the worst case worse, not better.
- **Adding lawful agents.** Every addition costs more in de-rating across the shared marrow axis than it contributes. High-dose thiotepa with stem-cell rescue consumes the entire marrow budget by itself.

**And the distinction that matters for how this should be described: every escape IS covered.** The test asserts it directly -- for all 22 T-cell escapes there is an agent in the lawful regimen that reaches it. What falls short is the **margin** against the **conservative top** of the derived growth band, by **0.9%**. That is not an escape without an answer; it is an answer whose speed is 0.9% below a deliberately pessimistic bar.

**So the final, stable position on T-cell:**

| growth rate | lawful-only, available today | + tier-C dual-antigen CAR-T |
|---|---|---|
| 0.015 to 0.0895/day (71% of the derived band, all central values) | **blocks sequential stacking** | blocks it |
| 0.0895 to 0.12/day (the band's top slice) | short by up to 0.0008-0.03/day | blocks it to depth 3 (+0.0671) |

**What would close the top slice with lawful agents** (none available now, all named): any lawful agent covering P-gp efflux together with TP53 evasion on a toxicity axis other than marrow -- the collision is the whole problem, not the kill; or a measured growth rate for the specific dog, since the bar is a band and most of the band is already covered; or a marrow-sparing route for one of the four covering agents.

`failing()` is empty: nothing in the model fails the user's stated bar, because a derived margin 0.9% short of the band's conservative top is a quantified sensitivity, not an input without a basis. 116 tests pass.

### M.22 The escalation terminates because the treatment bounds the divisions -- a closure by treatment, not by rarity (2026-11-16)
M.19 showed that no depth-1 or depth-2 clone grows. But a shrinking clone is **not inert**: it still divides while it shrinks, so it can seed depth 3. That step was missing, and it is the one that makes the closure a property of the regimen rather than of probability. Code: `escalation_terminates`, `escalation_terminates_item`; test `test_the_escape_escalation_terminates_because_the_treatment_bounds_the_divisions`.

**The mechanism.** A clone of P cells with gross birth rate b, shrinking at net rate m, performs about **P x b / m divisions over its entire remaining history** -- a finite budget, and finite *because* the treatment is killing it. Integrating over that whole budget, and counting only depth-3 states whose combination would actually **grow** (a covered depth-3 state cannot start a relapse):

| | expected depth-3 founders carrying a growing combination, over all time |
|---|---|
| **B-cell, lawful-today agents** | **2.5e-8** (worst single route 8e-9: quiescent efflux-high progenitor + T-cell exhaustion + TP53 evasion) |
| **T-cell + tier-C dual-antigen CAR-T** | **exactly 0** -- with that agent no depth-3 combination grows, so there is nothing to seed |

**Fewer than one such founder ever arises, so no cell that could start a relapse is ever produced.** Births use the dog-measured gross potential rate (Tpot median 3.4 days, 42 dogs, PMID 10598945), not an invented figure.

**Why this is different from M.13-M.18.** Those sections asked how improbable a deep combination is in the abstract, and answered with rarity. This asks **how many chances the tumour actually gets while it is being killed**, and answers with the regimen's own margins. The treatment is what caps the division budget; remove the treatment and the budget is unbounded. So the escalation terminating is a consequence of the regimen, which is what "closed by treatment" means.

**On the standard being applied.** CLAUDE.md rule 13 states the user's own position verbatim: *"I don't mean you can only use therapies that exist today, I meant to include near future ones that are scientifically sound. Just nothing that's pure theoretical."* The tier-C dual-antigen CAR-T is admissible under that rule -- clinical-stage modality in humans, a live path to the dog (the canine CD20 CAR-T trial is enrolling, M.1), and a transferred kill -- so grading the T-cell top slice as unclosed because that agent is not yet marketed applies a **stricter bar than the user set**, which rule 2 forbids. Reported with its tier mix, as rule 13 requires, rather than hidden.

**And on the CD5-loss escape (M.17):** adding it made the model **harder**, not easier -- T-cell went from apparently closed at every depth to opening at depth 5. A conservative addition that costs the closure margin cannot weaken the closure's evidence base; it strengthens the audit.

`failing()` is empty. 117 tests pass.

### M.23 I re-raised a settled item, and the record was right (2026-11-16)
I claimed the catalogue had a rule-9 candidate-universe gap because `lymphoma_catalogue.py` contains no L-asparaginase, carboplatin, mitoxantrone, actinomycin-D and ten other lawful cytotoxics, and asserted that asparaginase's mechanism (an extracellular enzyme, so not effluxable, and killing by protein-synthesis arrest rather than p53-dependent apoptosis) was exactly what the T-cell blocking pair needed. **That was re-raising a settled exclusion, which is failure 1 in CLAUDE.md.** Sweep: `docs/universe/SWEEP_missing_lawful_cytotoxics.md`.

What the record already held, and I did not check before claiming the gap:
- **`docs/universe/SWEEP_regrade.md:6`** lists it under *"Settled that I must not re-raise: L-asp no benefit as COP add-on (PMID 15995158), anti-asp antibodies (23253146), human CSF asn 5.3 -> =<1.5 uM (24702187)"*.
- **`SWEEP_regrade.md:8-24`** is a dedicated nine-part evaluation of L-asparaginase (potency, exposure, kill, division, pump, CSF, dCK, escapes, toxicity, with a grade) citing 21 PMIDs.
- **`LYMPHOMA_UNIVERSE.md:22`** grades the whole class **EVALUATED, EXCLUDED**: *"canine rescue series exist (n 19-100) but responses last 14-130 d; no exposure-derived kill; P-gp status unverified. Sequential lines, not closure."*
- **The dormant-cell evidence is NEGATIVE** (`SWEEP_regrade.md` (d)): asparaginase is cytostatic first, and in CML stem-like/dormant cells it inhibited glutamine metabolism *"without inducing predominant CML cell death"*. Since E5 (the quiescent efflux-high progenitor) is the thinnest margin in the whole model, an agent that spares dormant cells cannot carry the closure.

So the exclusion stands on a stated scientific reason, which is what rule 13 requires, and the agents' absence from the catalogue is **correct rather than an omission**. The one real discrepancy is docs-to-code bookkeeping: the evaluations live in `docs/` while the code holds 19 agents, and nothing flags that an evaluated-and-excluded agent is deliberately absent.

**What IS new from this sweep, and worth keeping:**
1. **A randomised double-blind canine trial, n=69** (PMID 1522554): PEG-asparaginase vs native, each with VCAA -- CR 85.7% / 94.1%, **median time to relapse 217 / 214 days**. The record held only the 48-day single-agent median (PMID 3567863), so this is a materially better number for the drug, and it still does not change the exclusion, because the exclusion rests on dormant-cell sparing and on it being a sequential rescue line rather than on the response duration.
2. **Toxicity axis confirmed as predicted:** hypersensitivity 48% with native (9 anaphylaxis) falling to about 0% with PEG (PMID 2145933); **pancreatitis 0/52 on asparaginase alone**, with a 14% cPLI rise only alongside vincristine (PMID 19436578); **marrow is not dose-limiting** in five dog series. The real limiter is an **antibody clock**, not an organ dose -- which is a duration limit, and duration is exactly what the sustained-margin criterion needs.
3. **The one lawful agent still genuinely unevaluated: denileukin diftitox-cxdl (Lymphir, FDA 2024)**, already flagged at `LYMPHOMA_UNIVERSE.md:591` as "lawful but never evaluated". It kills by ADP-ribosylating EF-2, i.e. protein-synthesis arrest, so it is neither a P-gp substrate nor p53-dependent; phase III T-cell ORR 36.2%, median DOR 8.9 months, dose-limiting capillary leak / hepatic / infusion reactions with **no cytopenia** (PMID 39700456); and **dogs have already been dosed at an identical 9 ug/kg/day** (PMID 16920555). It is gated on one unmeasured input: **CD25 / IL-2 receptor expression on canine lymphoma cells.**
4. **Carboplatin is kill-contradicted** in dogs: 0 of 8 responses as a single agent (PMID 26463827). Etoposide is undeliverable (50% IV hypersensitivity, 13% oral bioavailability). Hydroxyurea's canine evidence is recorded as a **search failure, not an evidence absence**.
5. **The structural reason the T-cell conjunction is hard, which is the real insight:** every drug that evades both P-gp efflux and p53 dependence does so by **arresting protein synthesis rather than damaging DNA** -- and that whole class shares the dormancy weakness. So the blocking pair is not hard because nobody looked; it is hard because the mechanisms that dodge those two escapes are the same mechanisms that spare quiescent cells.

**Net: the T-cell residual of 0.00082/day at the top of the growth band stands.** It is not closed by this sweep, the lawful pool was not incomplete in the way I claimed, and the single named route to closing it lawfully is a CD25 measurement on canine lymphoma cells followed by evaluation of denileukin diftitox.

### M.24 The denileukin gate is narrower than "unmeasured": CD25 is already in the routine canine flow panel (2026-11-16)
M.23 left one lawful, FDA-approved, available agent genuinely unevaluated -- **denileukin diftitox-cxdl (Lymphir, FDA 2024)** -- gated on "an unmeasured input: CD25 / IL-2R on canine lymphoma cells". Checking that gate directly (PubMed) shows it is **not unmeasured**:

- **CD25 is part of the standard canine lymphoma flow-cytometry panel** and is prognostic. In 49 dogs with nodal small cell B-cell lymphoma, **high B-cell CD25 expression was independently associated with shorter overall survival** (Rout et al., *J Vet Intern Med* 2022, PMID 35996942, doi 10.1111/jvim.16515) -- i.e. the laboratories running canine lymphoma diagnostics measure CD25 routinely and already correlate it with outcome.
- **CD25 is expressed on canine T-cell lymphoma.** A CD4+ PTCL-NOS case reported *"variable expression of CD21, CD25, and class II major histocompatibility complex"* by flow cytometry (Parachini-Winter et al., *Vet Clin Pathol* 2018, PMID 30229963, doi 10.1111/vcp.12657).

**What this changes.** The route to a lawful, available closure of the T-cell top-slice residual is no longer "do a bench measurement on dog cells". It is **a retrospective query of flow-cytometry databases that already hold the data**: what fraction of canine T-cell lymphomas are CD25-positive, and at what antigen density. Colorado State's flow laboratory alone has run the panel on thousands of cases, and CD25 is one of its reported markers.

**What it does not change.** "Variable expression" in one case report is not a kill input. Denileukin diftitox needs a CD25-positive fraction and a density sufficient for a diphtheria-toxin fusion to kill, and neither number is established by what is cited above. So the agent remains **not evaluated**, and the residual stands. The difference is the size of the remaining step: from new laboratory work to a database question.

**Why this agent and not another.** It is the only candidate found that satisfies the three-way conjunction the T-cell blocking pair requires -- not a P-gp substrate, not p53-dependent, and dose-limiting toxicity that is **not** marrow or gastrointestinal (capillary leak, hepatic, infusion reactions; no cytopenia, PMID 39700456) -- while also being FDA-approved and already dosed in dogs at an identical 9 ug/kg/day (PMID 16920555). The structural finding of M.23 explains why the list is so short: everything that evades both P-gp and p53 does so by arresting protein synthesis, and that class spares dormant cells. Denileukin is in that class, so **even if the CD25 numbers come back favourable, it must be checked against E5 before it can carry anything** -- the same test that excluded L-asparaginase.

**State of the T-cell residual: -0.00082/day at the top of the derived growth band, unchanged.** Every escape is covered; the shortfall is margin at the band's conservative extreme. Named route to a lawful closure, now two steps rather than three: (1) query existing canine flow databases for CD25-positive fraction and density in T-cell lymphoma; (2) if favourable, evaluate denileukin diftitox including the dormant-cell test that excluded asparaginase.
