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
- Oral cytarabine does not help the T-cell dormant lineage: the T-cell lymphoma-line IC50 is higher, so at a CSF level of 0.3 uM the kill is 0.043 /day (B-cell 0.27), below the awake growth rate 0.09; the sustained agents never touch it. The dCK-loss lineage (E2) is covered only by radiation, thiotepa and a few weak agents.
- Radiation alone would need **19.6 e-folds in vivo** (36 Gy gives about 2.6 times the 23.4 Gy value). Human primary T-lineage lymphoma cells are SF2 0.36-0.44 (D0 about 1.9 Gy; PMID 1429095): 36 Gy would be about 10 e-folds after the in-vivo factor, half of what is needed. Only if the canine T-lymphoma CNS lineages were as radiosensitive as human haematopoietic stem cells (D0 about 0.9 Gy; about 21 e-folds at 36 Gy in vivo) would it close, and the whole-brain dose of 36 Gy carries real late-neurotoxicity risk (the dog evidence for it was not retrieved before the rate limit).
- The thing that would decide it is a measurement, not a new product: **primary canine T-cell lymphoma radiosensitivity (clonogenic or apoptosis, cycling vs resting, from fine-needle samples)**; if D0 is at the stem-cell end, a 36 Gy whole-brain course with the T-cell body program closes the brain; if it is at the human T-lineage value, it does not and the T-cell brain stays open with everything that exists.
- Other existing agents re-graded for the T-cell brain do not change this: lomustine (0.004-0.04 /day derived; CSF about 50% of plasma), rabacfosadine (dCK-independent but acts on dividing cells, CSF access not found), L-asparaginase (cytostatic; dormant-cell evidence negative), hydroxyurea and procarbazine (dCK-independent; CSF level not found).

### I.5 What this changes
- The B-cell case no longer needs a CAR-T, an engager or a spinal-fluid route, and the T-cell body no longer needs one either. They remain additional, independent routes (sections E, G, H), not requirements.
- The T-cell brain is the one case that stays open from existing agents, and it is stated as an open quantity (primary canine T-lymphoma radiosensitivity; toxicity budget), not as "a future program will solve it".
- Two inputs carry the B-cell brain: radiation e-folds on the dormant progenitor (a TRANSFER from lymphoid and stem-cell radiobiology, not canine E5 data) and multi-year oral cytarabine tolerability (ASSUMED beyond about 2 years). If the sensitive-line value holds, the sustained window drops from 975 to 250 days (8 months), inside the human maintenance experience.
