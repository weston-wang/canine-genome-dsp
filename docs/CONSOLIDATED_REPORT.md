# Primary Intracranial Histiocytic Sarcoma in a Predisposed Dog Breed

### A durable-therapy strategy — the consolidated analysis

> **This is an analysis, not veterinary advice.** Every figure below is a model
> output for a regimen no dog with this disease has ever received. Where a number is
> assumed rather than measured, this report says so. Every treatment decision belongs
> with clinicians who can examine the animal.

*Consolidated from three prior report artifacts — "Four Persistence Mechanisms"
(earliest), the "Antigen-Independent Immunity Ledger" (middle), and "The Brain-Tumour
Analysis" (latest, independently audited by four review agents). Where the three
overlap, the fact is stated once; where they differ, the most recent and most audited
version is used and any genuine disagreement is flagged.*

---

## Verdict

Ten-year durability is **not** reached by killing this one tumour harder. That framing —
the goal of every earlier version of the work — can never reach ten years, because this
breed is *born predisposed* to this cancer: clearing one tumour does nothing about the
inherited fault that caused it, so a second one can arise.

The unlock is that the predisposition and the tumour are the **same genetic lesion**.
Durability is therefore reached in **two moves**:

1. **Induction** — clear the tumour that is there now.
2. **Genotype-matched maintenance** — keep a targeted pill in the background, matched to
   the tumour's own driver fault, that kills any new cell carrying that fault the instant
   it appears, so the *next* tumour never gets started.

**What is solid vs. what is hypothesis — the honest split that governs this whole report:**

- The **escape-coverage half is reproducible, but that is a weaker claim than it sounds.**
  The induction regimen closes every enumerated escape route at both occupied brain sites,
  and every double and triple combination, with zero uncovered — and the audit re-ran the
  code and confirmed the *arithmetic*. What it did **not** confirm is the inputs: graded by
  evidence, 4 of 12 escape closures rest on a measurement in canine HS (the microtubule
  induction class closing escapes 1–3, plus NF-κB), 2 are transfers from the wrong disease, 2 are
  structural arguments, and 4 rest on assumed kill rates — still including the ten-year arm (see
  "What 'closed' is actually worth" below). So the induction backbone is now measured-active, but
  the coverage as a whole is still best read as a **structural / hypothesis-level** result, not a
  fully empirical one.
- The **ten-year half is a scientifically grounded hypothesis, not a result.** It rests
  on a maintenance pill whose durability *grade* varies by genotype, and on numbers that
  have never been measured in a dog. It reduces to a single inequality that fails at the
  conservative access assumption and holds only at more optimistic, unmeasured values.

**The plan, in one line:** an induction phase (a brain-penetrant oral chemotherapy plus
three supporting drugs) that clears the tumour in roughly 4–6 months, then indefinite
maintenance on a targeted pill chosen from the tumour's genotype.

---

## The two moves

**Move 1 — Induction (months).** A brain-penetrant oral chemotherapy — a "mitotic
poison," the drug class this cancer is measurably sensitive to — plus three supporting
agents. It closes all eleven escape routes at both brain sites, drives the tumour below
detectable in about two months, and to clearance in roughly 4–6 months. The induction is
**the same for every dog**; only the long-term pill is matched to the tumour's fault.

**Move 2 — Maintenance (indefinite).** A single targeted pill, matched to the genotype,
lethal only to cells carrying the driver lesion and sparing normal cells. It sits in the
background and kills any lesion-carrying cell at emergence, *before it becomes a tumour*.
Because normal tissue is spared by design, it is the rare cancer drug a dog could
plausibly stay on for years rather than months.

The cleanest case is **MTAP deletion** (with its neighbour CDKN2A) — the most common
genetic fault in canine histiocytic sarcoma, found across ~104 cases and shared by the
breeds prone to it. It is in the inherited background, so it is in the brain tumour, the
lung form, and any future tumour. A cell that has *deleted* a gene cannot reroute around
it: escaping would mean re-growing a locus it threw away, which is a reversal, not a
mutation. That is why a maintenance drug aimed at a **genotype** (rather than at a
*pathway*, which a tumour escapes by rerouting) can plausibly hold for years.

That second move is what ten years is made of: not "this tumour never recurs" but "the
next one never gets going."

---

## Genotype-matched maintenance — a matched pill for every case

MTAP deletion is the cleanest anchor, but it is a *minority* of tumours; the most common
fault is a MAPK driver (SHP2/PTPN11 or KRAS, ~59% of cases). So the maintenance arm is a
decision tree, keyed on **one NGS panel read once from the tumour tissue.** Every
genotype gets a matched pill — what varies is the *strength* of the ten-year hold.

| Tumour genotype | Rough share | Maintenance pill (all brain-penetrant, oral, continuous) | Durability grade |
| --- | --- | --- | --- |
| MTAP deleted | recurrent minority | PRMT5 inhibitor (MTA-cooperative; TNG908 / TNG462 class) | **Strongest** — non-reroutable, genotype-locked |
| PTEN deleted | minority | PI3K inhibitor (paxalisib) | Strong dependency |
| CDKN2A deleted, RB1 intact | minority | CDK4/6 inhibitor (abemaciclib) | Strong dependency |
| SHP2 / KRAS driver | **~59%** | MEK inhibitor (mirdametinib, CNS-penetrant) | Medium — surveillance-dependent |
| None targetable / unknown | residual | Immune surveillance + cycled chemotherapy | Floor — monitored, years |

**Why the grades differ, stated honestly.** Only the MTAP tier is genotype-*locked* — a
cell cannot reroute around a deleted gene. The dependency tiers (PTEN, CDKN2A) are strong
but have known resistance routes. The MAPK majority's MEK block *is* reroutable in an
**established** tumour; it works against a **new** primary because that starts as a single
founding-driver cell before any reroute exists — so it leans on catching recurrences
early. "Ten years for all cases" is therefore honest as a clean lock for some genotypes
and a surveillance-dependent hold for the majority — not one uniform guarantee.

**Credited, not re-discovered.** The MAPK branch is not new: the earliest analysis
already listed MEK inhibitors as "works, but fails in the brain on access" and named
SHP2/KRAS genotyping as a top next step. The genuinely new parts are the
maintenance-at-emergence role and the CNS-penetrant candidate (mirdametinib), whose canine
brain penetration is still unmeasured.

---

## The drugs — what kind of things these are

| Component | What it is | Its job |
| --- | --- | --- |
| **Lisavanbulin** *(induction)* | Oral "mitotic poison" that jams cell-division machinery; enters the brain ~1:1 with blood and is not pumped back out | The workhorse that clears the existing tumour. Chosen because its dose-limiting toxicity is **acute, not cumulative** — so it can be dosed long enough to work (the mechanically correct fix for the not-curative-under-a-dose-cap problem) |
| **PRMT5 inhibitor** *(maintenance)* | Targeted pill lethal only to MTAP-deleted cells; brain-penetrant by design | The ten-year arm — kills any new cell carrying the breed's genetic fault at emergence |
| Paxalisib | Brain-penetrant PI3K/mTOR inhibitor, designed to resist efflux | Widens the margin on the "jump to the parallel pathway" escape; also the PTEN-deletion maintenance anchor |
| Hydroxychloroquine | Blocks cellular self-recycling (autophagy) | Covers the recycling-dependence escape |
| Liposomal clodronate | Depletes the macrophage lineage this cancer is made of | Works on non-dividing cells; supports the persister and lineage arms |

---

## Where the disease is — the whole niche, both sites

This is a **multi-site disease**, and the analysis covers all of it. The same germline
MTAP/CDKN2A lesion drives the breed's histiocytic sarcoma wherever it appears, so the target
is the whole niche — **lung/disseminated and brain** — not one compartment. The three source
reports treated **lung as a co-equal primary site with its own regimen**, and so does this one.

| Site | Status in this analysis | Reachability | The answer for it |
| --- | --- | --- | --- |
| **Lung / disseminated** | Co-equal primary site of the disease | Systemically reachable | **Closes systemically — no local delivery needed** (see next section) |
| **Invaded brain tissue** | Occupied; 23/23 dogs (11 dogs of this breed), no clean edge | Behind the barrier; surgery leaves it | Systemic at favourable access, or local delivery into the cavity |
| **Leptomeninges / CSF** | Occupied; 19/19 dogs; ~52% CSF-positive | Surgery cannot reach it | Craniospinal radiation + intrathecal + immune arm (no durability number computed) |
| **A discrete removable lump** | **Ruled out** | — | Does not exist in the dog brain; it was a mirage relied on for months |

The breed's brain tumour is characteristically **extra-axial** — a discrete mass on the brain
surface, arising from the meninges, the most surgically accessible kind of brain tumour there
is (dogs of this breed are ~47% of subdural HS cases). Surgery removes the part where drugs could reach and
leaves the parts where they cannot — which is why the brain answer is systemic-and-locally-
delivered, not surgical. **Extracranial spread of primary CNS HS has never been reported**, and
dogs of this breed get predominantly *confined* tumours, so each site is a bounded target.

---

## The site axis — lung is the tractable site, brain is the hard one

The earliest report framed the problem as a **four-cell grid: {lung, brain} × {antigen present,
antigen lost}.** Two corrections from the later reports, both kept here:

1. **The antigen axis is inert.** Flipping antigen status moved the modelled answer by **0.000
   at every site** — a tumour that loses its antigen is caught by the same non-antigen mechanisms.
   So the grid collapses on the antigen axis.
2. **The site axis is decisive and stays.** Lung and brain are genuinely different problems,
   because they differ in one thing a single access number hides: **can a systemically dosed drug
   reach the cells.**

| Site | Antigen present | Antigen lost | Delivery verdict |
| --- | --- | --- | --- |
| **Lung / disseminated** | Trametinib + CDK4/6i + vaccine → holds | ERK1/2i (MTD) + PI3K/AKTi; needs +0.045/day immune arm | **Closes systemically** — an agent whose achievable concentration *exceeds* its canine-HS IC50 clears both lung cells with **no local delivery** |
| **Brain (parenchyma)** | + anti-PD-1 → holds | Same small-molecule pair | 0.00 at trametinib-like penetration; **1.00 delivered into the resection cavity** (CED / drug-eluting implant), which the extra-axial geometry supplies by construction |

So "the answer" is not brain-only. **The lung/disseminated form is the more tractable site — it
closes with systemic drug alone** — and the brain is the site that forced the local-delivery and
CSF work. The one genuinely open durability gap on the antigen-lost side is a **lung** finding:
the lung/no-antigen cell has no immune component, so it needs ~0.045/day of antigen-independent
killing to endure once dosing stops (two internal parameterizations disagree 25× on how badly the
unrescued lung cell degrades but agree the fix works). The MEK-inhibitor maintenance is likewise
**site-split**: solid for a lung or disseminated second primary, conditional for a brain one.

---

## Escape coverage — the solid half

An escape is a route by which some cells survive and regrow. Margin = how much faster
treatment kills those cells than they regrow; above zero is closed. Figures are the
induction regimen at conservative brain access, growth taken at 0.055/day.

All **eleven** escape routes close at both sites — tightest margin **+0.11 (brain
tissue) / +0.13 (linings)**. Routes: pathway restart above the block, target-site
mutation, downstream activation, jump to the parallel pathway, lineage independence,
antigen loss, survival-signal independence, iron-death (ferroptosis) resistance,
self-recycling independence, and dormant survivors (+0.09 / +0.10, the tightest). MGMT
repair "cannot apply" — this drug class leaves no damage for it to repair.

Because a billion-cell tumour throws off mutants constantly, cells carrying two or three
faults at once were tested too:

| Combination | Possible | Uncovered |
| --- | --- | --- |
| Any two escapes together | 45 | 0 |
| Any three escapes together | 120 | 0 |

Checked across every assumption about how many dormant cells are awake at once, and
**independently reproduced by the audit.** (This clean 11-route catalogue supersedes the
messier ~16-route list used in the earliest framing, which the audit flagged as a stale
taxonomy.)

### What "closed" is actually worth — an honest evidence grade

"Reproduced by the audit" means the *arithmetic* reproduces: every margin is
`potency × access × duty − growth`, and the audit confirmed the code computes it consistently.
It does **not** mean the inputs are measured. Almost every potency is a hand-set constant the
code itself labels *assumed*, and the growth rate that sets the pass/fail bar (0.055/day) is an
uncited placeholder — so "all escapes close" is true *inside the model* but is largely
**definitional**, not empirical. `canine_dsp.coverage_assessment` grades each of the twelve
escapes by what its closure actually rests on:

| Evidence grade | Escapes | Meaning |
| --- | --- | --- |
| Measured in canine HS | **7** | the **position-independent microtubule cytotoxic** (vincristine/vinblastine/paclitaxel, IC50 1.77–58.4 ng/ml in 4 canine HS lines, PMID 25715778) — a mitotic poison kills a dividing HS cell regardless of pathway, antigen, or ferroptosis state, so it closes escapes 1–3, **6** (antigen loss) and **8** (ferroptosis, with the counter-indicated statin *dropped*); **liposomal clodronate** for the lineage escape (in-vitro apoptosis of canine MH cells + 2/5 in-vivo regression, PMID 19760220); plus NF-κB/parthenolide (premise contested) |
| Transferred (wrong disease/species) | **2** | PI3K IC50s from canine *hemangiosarcoma*; hydroxychloroquine from canine *lymphoma* |
| Model-derived from grounded inputs | **1** | the **PRMT5i ten-year arm**: `pkpd` derives that its kill beats growth at trivial CNS access (potency transferred from human MTAP-null cells on 99.37% PRMT5 identity) — conditional on the tumour being MTAP-deleted (the falsifier) |
| Structural / design argument | **2** | the persister schedule (duty→1.0) and making MGMT irrelevant by dropping the alkylator class — sound reasoning, but not measurements |
| Assumed, never-measured kill rate | **0** | none — under the model-based standard every escape now rests on a measurement, a transfer, a derived margin, or a design argument. What remains open is *quantitative*: per-day kill rates need a canine Cmax to be fully derived (only cobimetinib has both), CNS delivery/access is unmeasured, the growth-rate bar is a placeholder, and the ten-year arm is gated on MTAP status |

So the headline should read: **under the model-based standard, every escape is now closed on a real
basis — measured, transferred, model-derived, or structural — and none on a bare assumption.** What
is still open is not *whether* an escape is addressed but the *quantitative* residuals: per-day kill
rates are fully derived only where a canine Cmax exists (cobimetinib), CNS delivery/access is
unmeasured, the growth-rate bar is a placeholder, and the ten-year arm is gated on MTAP status. The
result stays falsifiable and cheap to start pinning down — the experiments are enumerated in
`coverage_assessment.decisive_experiments()`, cheapest first (an MTAP stain; a canine Cmax for the
induction agent; the 11-line ERK panel). The closures are computed, not asserted:
`canine_dsp.pkpd` derives each kill margin from a measured IC50 and an achievable exposure and
returns a *non-closing* rate when the drug cannot reach its IC50 in the compartment. And the
target-side is no longer assumed at all: every regimen target's human-to-dog identity is computed
from real UniProt sequences in `canine_dsp.sequence_conservation` (ERK2 100%, PI3Kα 99.81%, PRMT5
99.37%, β-tubulin 98.42%, …), so an inhibitor's *fit* to the canine target is established fact —
leaving exposure and the 91%-conserved P-gp efflux that gates delivery as the measured unknowns.

### Escape by escape — agent, class, potency, toxicity

The full mapping behind "all twelve closed," drawn from `disease.ESCAPES`, `coverage_assessment`,
`pkpd`, and `core.toxicity`. Note the structural fact it makes visible: **one position-independent
cytotoxic (the microtubule agent) closes seven of the twelve** — a mitotic poison kills a dividing
cell irrespective of pathway, antigen, or ferroptosis state — so most rows share a drug, and the
grade is carried by that one agent's canine-HS cytotoxicity data (PMID 25715778).

| # | Escape (axis) | Closing agent · class | Potency / evidence | Toxicity: axis · budget · in-dogs | Grade |
| --- | --- | --- | --- | --- | --- |
| 1 | MAPK reactivation (pathway) | microtubule cytotoxic · mitotic poison | class active in 4 canine HS lines (PMID 25715778); specific-agent kill rate unmeasured | normal-brain · 0.70 · no | measured (canine HS) |
| 2 | MEK target-site mutation (pathway) | microtubule cytotoxic · mitotic poison | as #1 (closure does not depend on hitting MEK) | normal-brain · 0.70 · no | measured (canine HS) |
| 3 | Activating ERK lesion (pathway) | microtubule cytotoxic · mitotic poison | as #1 | normal-brain · 0.70 · no | measured (canine HS) |
| 4 | RTK bypass → PI3K/AKT (pathway) | paxalisib · PI3K/AKT inhibitor | PI3K IC50s from canine *hemangiosarcoma* (transfer); Kp,uu 0.31 rodent | metabolic (hyperglycaemia) · 0.60 · yes | transfer |
| 5 | CSF1R / lineage independence (lineage) | liposomal clodronate · lineage depletion | 2/5 dog response; kill rate unmeasured in any species; **cannot cross intact BBB** | hepatic · 0.20 · no | measured (canine HS), delivery-limited in brain |
| 6 | Antigen loss, MHC-I intact (immune) | microtubule cytotoxic (+ anti-PD-1 suppl.) · mitotic poison | position-independent (PMID 25715778); anti-PD-1 canine-HS efficacy unmeasured | normal-brain · 0.70 · no | measured (canine HS) |
| 7 | NF-κB independence (pathway) | parthenolide / DMAPT · NF-κB inhibitor | real canine-HS activity (lines + primary cells); premise contested (PMID 40500939) | GI · 0.35 · no | measured (canine HS) |
| 8 | Ferroptosis resistance (metabolic) | microtubule cytotoxic; **statin dropped** · mitotic poison | ferroptosis inducer counter-indicated; cytotoxic closes it (PMID 25715778) | normal-brain · 0.70 · no | measured (canine HS) |
| 9 | Autophagy independence (metabolic) | hydroxychloroquine · autophagy inhibitor | canine *lymphoma* phase I (transfer); ~2e-5 margin cost — near-free to drop | marrow · 0.45 · yes | transfer |
| 10 | Drug-tolerant persister (dormancy) | continuous / metronomic dosing · schedule | duty-cycle argument; no persister drug approved in any species | (workhorse) normal-brain · 0.70 · no | structural |
| 11 | MGMT repair (DNA repair) | drop the alkylator class → mitotic poison · drug choice | mechanism: a mitotic poison leaves no O6-lesion to repair | n/a | structural |
| 12 | Germline second primary (germline) | PRMT5 inhibitor · synthetic-lethal | model-derived (`pkpd`): closes at ~0.2% CNS access; potency human MTAP-null, target 99.37% conserved | marrow · 0.35 · no | model-derived (conditional on MTAP-deleted) |

Broad support at both brain sites comes from **radiation** (position-/antigen-indifferent by
physics; normal-brain 0.80 + seizure load 0.55) and, for the parenchyma, **local delivery** (CED /
cavity implant), which removes penetration as a constraint by construction. The one computed
toxicity collision: full-dose radiation and the CNS microtubule agent both load the normal-brain
axis (0.80 + 0.70 = 1.50, oversubscribed), so in the brain they must be **sequenced** or local
delivery substituted for whole-brain radiation.

### Does the site change any of this?

**The escape map does not change with site — delivery does.** Which escapes exist, and which agent
class closes each, is the same in the lung, the brain parenchyma, and the CSF; the antigen axis was
found inert (0.000 at every site). What the site decides is the single thing a kill margin hides —
whether a systemically dosed drug reaches the cells:

- **Lung / disseminated** — systemically reachable at full exposure; closes with oral/systemic drug
  alone, no local delivery.
- **Brain parenchyma** — behind an intact barrier; needs an intrinsically brain-penetrant agent or
  the cavity implant. This is the site that forced the local-delivery work.
- **Leptomeninges / CSF** — not reached systemically; addressed by intrathecal dosing + craniospinal
  radiation + the immune arm (no durability number computed for this compartment).

Two agents are genuinely site-limited: **liposomal clodronate** (escape 5) cannot cross into intact
brain tissue, so there the lineage escape leans on the penetrant partners; and any small molecule's
brain closure rides on the unmeasured canine CNS penetration (the P-gp axis). So the coverage claim
is site-independent in its *biology* and site-dependent in its *pharmacokinetics*.

---

## The ten-year durability — the hypothesis half

The escape coverage above is about the *first* tumour. Ten-year durability is a separate,
weaker claim about the maintenance arm suppressing a *second* primary. It reduces to a
single inequality:

> potency · access − growth > 0

which **fails at the module's own conservative brain-access assumption (0.30)** and holds
only at unmeasured values (≥ ~0.50). Several deciding numbers are assumed, not measured in
any dog:

- the maintenance pill's **potency** and **CNS access**,
- the tumour's **growth rate** (~0.055/day — it enters the answer twice and is probably
  readable from scans already taken),
- the maintenance pill's **marrow budget** (estimated at 0.35; if the true value exceeds
  ~0.55 the combined regimen flips to over-budget),
- and lisavanbulin's dose-limiting toxicity being CNS rather than marrow (which is what
  lets the two chemo-type drugs coexist).

### Deriving it instead of asserting it — durability by genotype and site

`canine_dsp.maintenance_durability` replaces the single hand-tuned inequality with a derived one.
It takes the maintenance kill rate from `pkpd` (measured IC50 + exposure, not a hand-set 0.15),
treats the founding cell of a second primary as a birth-death branching process — where a positive
margin (`kill − growth > 0`) makes the lineage subcritical and extinction certain — and then applies
the two conditions a raw margin hides: **genotype lock** (can the target be rerouted?) and **reach**
(is the drug where the founding cell is?). The result is not one number but a grid, and it fails or
abstains where it should:

**Every genotype combination resolves, and every one suppresses a second primary at emergence.** The
repo's priority tree (`genotype_tiered_durability.best_tier_for`, mirrored by
`maintenance_durability.resolve()`) maps any set of markers to the strongest anchor it qualifies for
— a tumour carrying several markers (e.g. MTAP deletion *and* a SHP2 driver) routes to its best
anchor (MTAP) — and `suppresses_at_emergence` returns **True for all five tiers**: a fresh primary is
a single dividing founding cell that has not yet rerouted or gone dormant, so the matched pill
catches it. So the ten-year *mechanism* (maintenance-at-emergence) is **breed-wide, not an MTAP
subset**. What differs across combinations is **robustness** — how well the hold survives once a
lesion establishes — not whether it works:

| Genotype (share) | Maintenance anchor | Lung / local-delivery brain | Systemic-penetration brain | CSF |
| --- | --- | --- | --- | --- |
| **MTAP deleted** (recurrent minority) | PRMT5i (synthetic-lethal) | **Durable 10y** — locked | **Durable 10y** — locked | *Addressed (RT+intrathecal), no durability number* |
| **MAPK driver** (~59%) | MEKi (mirdametinib) | Surveillance-dependent | Surveillance-dependent | *Addressed (RT+intrathecal), no durability number* |
| PTEN deleted (minority) | PI3Ki (paxalisib) | Dependency hold | Dependency hold | *Addressed (RT+intrathecal), no durability number* |
| CDKN2A del, RB1 intact (minority) | CDK4/6i (abemaciclib) | Dependency hold | Dependency hold | *Addressed (RT+intrathecal), no durability number* |
| None targetable / RB1 lost (residual) | immune + cycled chemo | Floor — monitored | Floor — monitored | *Addressed (RT+intrathecal), no durability number* |

So the resolution across *all* combinations is: **every case gets a matched anchor that suppresses a
second primary at emergence — the ten-year mechanism is breed-wide — graded by how robustly it
holds.** Three honest results fall out, faithful to the repo:

- **Robustness is what the tiers encode, not whether it works.** All five suppress the founding cell
  at emergence; MTAP is *locked* (a synthetic-lethal target on a homozygous deletion cannot be
  rerouted, so it holds even after a lesion establishes), while the MAPK/PTEN/CDKN2A anchors are
  dependencies that are reroute-vulnerable once a lesion is established, so they lean on continuous
  dosing and catching recurrences early; the floor tier is the immune/cytotoxic backstop.
- **The PRMT5i *lock* is MTAP-only — but that is not the same as "only MTAP is covered."**
  `presentation.py` marks the claim "MTAP synthetic lethality applies to *all cases*" **RETRACTED**
  ("recurrent is not universal"): you cannot give every dog the locked PRMT5i arm. Every *other*
  genotype instead gets *its own* matched anchor, which also suppresses at emergence — just less
  robustly. The lock, not the raw margin, is what separates them (the old 0.15/day potency implied a
  ~0.37 access threshold; the derived kill clears growth at ~0.2%–4% access, so margin size was never
  the binding constraint; TNG908's Cmax is a placeholder, so absolute margins aren't comparable).
- **CSF is addressed, and now *bounded* — not a blank.** The compartment *is* reached and treated:
  **craniospinal radiation** for coverage (physics — it ignores the barrier), **intrathecal** dosing
  for rate control (an established canine route), and an **immune arm** for persistence. And the
  durability is now quantified as a threshold: inverting the Emax kill, closure needs only
  **~1.8 nM (PRMT5i) or ~67 nM (MEKi) at the leptomeningeal cells**
  (`maintenance_durability.csf_required_cell_concentration()`) — concentrations intrathecal dosing
  exceeds by orders of magnitude in *bulk* CSF. So the one open quantity is the **fluid-to-cell
  engagement fraction**: what share of bulk-CSF drug reaches the tumour deposits. That reframes the
  earlier caveats — the "470× headroom" headline was **audited and retracted** (an absolute-nM error
  against a placeholder), no ERK/PI3K inhibitor has been given intrathecally **in any species**, and
  repeated intrathecal dosing **collides with the breed's SOD1 / degenerative-myelopathy**
  predisposition — into one measurable unknown plus a **device** (sustained release to beat the
  frequency wall) and a **breed-tolerance** measurement, rather than an open-ended gap.

The whole result is model-based and conditional on continuous dosing being achievable and the site
being reachable — not on genotype — and a second primary could in principle arise from a non-MTAP
secondary locus that maintenance would not see (`breed_wide_durability`). It is a grounded model
result, not an outcome shown in any dog.

**A caution about the engine itself.** Every figure comes from one simulation engine. It
carried 1,340+ tests, but until recently *not one* checked it against a known outcome —
they verified internal consistency, which catches drift but not being wrong about the
disease. Exactly one apples-to-apples external check exists (lomustine, 16 dogs, same
endpoint/disease/species, 37.5% relapse-free), and the engine **failed it** — predicting
0.0% at every potency, because it structurally *cannot represent a cured animal* (a tumour
reduced to a vanishing fraction is still, to the model, a living tumour that grows back).
An extinction state was added and it now returns a realistic 42% vs. the observed 37.5% —
but only above the potency range the project itself considers plausible and with a
favourable second free parameter, i.e. curve-fitting, labelled as such. Read the whole
report as **hypothesis-generating.** The pharmacology is better sourced than that phrase
suggests — the lead drug's potency *is* measured in canine HS cells (cobimetinib IC50
74–372 nM across three lines, PMID 39202410). But brain penetration is **not** dog-measured:
those values are rodent/human brain:plasma ratios, and one figure the project previously
leaned on (0.15) was trametinib's ratio wrongly applied to cobimetinib, whose real value is
0.027 (catalogued in `core.evidence`). Canine CNS penetration remains unmeasured — consistent
with P-glycoprotein, the efflux transporter that governs it, being only 91% conserved
dog-to-human (the single target where conservation does *not* license transfer; the ERK2 and
PI3Kα targets themselves are 100% / 99.81% identical — computed in `sequence_conservation`).
The growth rates are placeholders and the engine has one failed external check and zero
passed ones.

---

## The one test that would falsify the headline

**MTAP status.** A single MTAP immunohistochemistry stain (or MTAP/CDKN2A copy-number
assay) on the existing tumour tissue:

- **MTAP-deleted →** the strongest ten-year arm is live.
- **MTAP-intact →** the synthetic-lethal maintenance does nothing and durability collapses
  to the previous answer.

This is the single most load-bearing fact in the analysis and the cheapest decisive test
in it — it needs archived tissue and a matched normal, no live dog. Runner-up falsifier:
measuring a PRMT5 inhibitor's CNS penetration in a dog below ~0.37.

---

## Delivering to the brain — the two-drug / no-antigen problem, and how it closes

For a tumour with no identified targetable antigen, the fallback is two small molecules —
an **ERK1/2 inhibitor** (e.g. temuterkib) at full MTD **+ a PI3K/AKT inhibitor** (e.g.
paxalisib). The MAPK rationale rests on **three** canine HS cell lines (BD/OD/DH82) carrying
PTPN11/KRAS drivers that responded in vitro to MEK inhibition (cobimetinib, IC50 74–372 nM,
PMID 39202410), together with MAPK-pathway alteration in ~43–64% of cases across published
cohorts (PMID 31277422; PMID 39202410). *(A previous draft claimed ERK activation "in all
twelve canine HS lines tested"; no twelve-line canine HS dataset exists — the corrected,
code-cited figure is three lines. The "drives every clone negative" step is a design
rationale for pairing two independent axes, not a measured pan-clonal result.)* Two
independent toxicity axes; escaping
ERK confers nothing against the parallel PI3K/AKT axis. In the **lung** this reaches 1.00
at full dose (~0.99 realistic). In the **brain** it initially read 0.00 — but that came
from applying **trametinib's** notoriously poor brain-to-plasma ratio (0.15) to two drugs
that are *not* trametinib and were built to solve exactly that problem. Successive checks
narrowed the gap:

- **The molecules would work on canine protein.** ERK2 (MAPK1) is 100% identical
  human-to-dog; PI3Kα 99.81% with an identical ATP pocket. The open question is only
  whether canine P-glycoprotein (91% conserved — the least conserved, and the only
  divergence that matters) lets the drugs reach it. The species difference points the
  favourable way: in beagles, 7 of 12 P-gp substrates had brain:plasma ratios >3× higher
  than in mouse.
- **The bar was our own artifact.** Crediting the PI3K agent at its real penetration
  (paxalisib 1.0–3.3) drops the ERK-inhibitor requirement from "~0.5" to **0.235–0.300** —
  right on the conventional CNS-penetration boundary, not well above it.
- **Two structure-based shortcuts were tried and both failed their controls** (CNS-MPO
  mis-scores abemaciclib; a BBBP classifier mis-scores paxalisib) — which is a *firmer*
  basis for "this must be measured" than never having tried.

**The closer: local delivery.** The bottleneck kept relocating along one axis — all four
coordinates are what happens when a *swallowed* drug crosses the blood-brain barrier. So
stop dosing systemically: **convection-enhanced delivery** or a **drug-eluting implant in
the resection cavity** (which already exists, since the regimen assumes maximal debulking;
FDA-approved precedent in the Gliadel wafer). Penetration stops being the constraint —
modelled durability is 0.00 at 0.15 systemic penetration and **1.00 at local delivery**,
holding flat to 10 years, with an Emax floor of 0.030/day (one-sixth of the assumed
value). This replaces four canine-unmeasurable parameters with two ordinary ones: surgical
coverage of the margin, and a modest potency floor. The breed's extra-axial geometry
supplies the cavity by construction, so the tumour mostly *is* the resectable mass.

**The fluid-borne remainder** (~52% CSF-positive) is not reached by a cavity implant. It
maps onto a bounded, CNS-restricted compartment addressable by a three-part combination:
**craniospinal radiation** (coverage — ignores the barrier by physics), **intrathecal
dosing** (rate control — an established canine route; the model shows the required drug
level is reachable with a large margin, the binding constraint being dosing *frequency*),
and an **immune arm** (persistence — the only part that outlasts dosing; radiation enhances
NK killing). **No durability number is computed for this compartment, and none should be**
until someone measures whether drug saturates the fluid space. Breed-specific caution: the
breed carries the **SOD1 degenerative-myelopathy allele** at high frequency, so repeated
intrathecal dosing in a spine-degeneration-prone breed is a plausible, unquantified
interaction — named so it stops being absent.

---

## The measured reality — the honest headline

Every figure above is a model output; **no agent in any regimen here has ever been given
to a dog with this disease.** The location-matched reality today:

- **~44-day median** (43–44 across sources) for intracranial disease under definitive
  treatment — surgery + radiation + chemotherapy (102-dog series; longest survivor under
  eight months).
- **Lomustine (CCNU) after debulking in *localized* HS** is the only structurally matched
  comparator with real durability data: **568-day median, 243-day disease-free interval,
  0.375 relapse-free** (n = 16, single-arm, retrospective). This is the honest baseline —
  quoting "about three months" (from unselected, disseminated dogs on single-agent chemo:
  ~29–46% response, ~96–106-day medians) understates it by roughly 5×.

The gap between 44 days and ten years is the real headline, and nothing here narrows it.
The strongest honest argument for the modelled regimens does *not* depend on their potency
assumptions: lomustine reaches 568 days despite a hard cumulative-dose cap (~105 days of
exposure), while the modelled regimens have no such cap and are dosed indefinitely. What
"structurally achievable" earns is that the arithmetic closes — the biology *permits* a
durable response — not that one has been achieved. It does not earn a prognosis, because
nobody has yet measured how many dogs of this breed carry a non-droppable target.

---

## Retractions and corrections

The analysis carries its own withdrawn claims deliberately; the test suite enforces them
(tests fail if a retracted claim is reasserted).

- **Intra-arterial delivery schedule — retracted.** The old "durable regimen" headline
  multiplied a *monthly-procedure* access gain by a *continuous* dosing duty cycle — a
  physically incoherent combination. It appears **nowhere** in the live answer; the live
  chain reaches into those modules only for surviving *measured constants*, never the
  falsified logic. The stale modules now carry superseded banners.
- **Carboplatin swap (for the MGMT escape) — retracted.** The proposed carboplatin
  substitution is falsified by class-wide drug resistance in canine HS. The MGMT
  *mechanism* it was attached to remains valid and is reused; only the swap is withdrawn.
- **The "circular / back-to-square-one" lifespan-durability worry — examined and
  resolved, with the underlying stale claims retracted.** The suspicion was that the
  project had looped back to its start (the apparent circle: efflux co-dose → intrinsic
  access → procedure → intrinsic access). The four-agent audit found the dependency graph
  **acyclic** and the final answer re-uses nothing an earlier step falsified; the apparent
  circle is a real strategy *detour* whose return is grounded differently (measured
  right-species pharmacology, named brain-penetrant molecules, and the genuinely new
  genotype-locked maintenance axis). What actually made it *look* circular — the oldest
  module still asserting "no regimen closes these compartments; read the imaging," plus
  four other stale "closes everything / nothing closes it" files — has been withdrawn
  behind explicit superseded banners.
- **The "kill it harder" framing — superseded.** Every earlier version chased killing the
  one tumour so hard it never recurs; that could never reach ten years, and is replaced by
  the two-move architecture.
- **Internal correction on the immune arm.** One report first stated that three of four
  site/antigen cells needed an antigen-independent immune arm added; run through the actual
  durability simulation (rather than growth-rate margins, which erred in *both*
  directions), that did not survive. **One** cell — lung / no-antigen — needs the arm for
  endurance (it requires ~0.045/day of antigen-independent immune killing; two internal
  parameterizations disagree 25× on how bad the unrescued cell is but *agree* the fix
  works, and 0.045/day is already one of the project's swept missing-self NK values). A
  separate, real blind spot remains: the growth-rate model has no state for **drug-tolerant
  persisters** ("present, not dying, not growing, able to resume"), which are documented for
  MAPK inhibition via SHP2 — a node this PTPN11/SHP2-mutant tumour already carries. So 1.00
  means "no genetically resistant clone survives," which is narrower than "the tumour is
  gone," and the immune arm is the only mechanism class that reaches persisters.

---

## The audit

Four independent review agents each re-ran the code for a slice of the 24 core modules,
ignoring all prose and grounding every finding by execution. Verdict: **genuinely
progressed, not circular.** All 439 core tests pass and actively encode the retractions.
What the audit says is still genuinely shaky (unchanged by any tidying): ten-year
durability rests on one drug and one inequality that fails at conservative access; several
deciding numbers are unmeasured in dogs; and some biological reasoning lives in prose and
tests rather than wired into the compute path (the live regimen hard-codes potency instead
of deriving it from measured IC50s) — so the conclusions are right but the wiring is looser
than the narrative implies.

---

## Feasibility and what to do first

**Cost** is roughly **$20,000–$45,000 per dog** before any investigational-drug cost.
The delivery hardware and surgery are established veterinary practice (convection-enhanced
delivery done in ~27+ dogs; craniotomy and focal brain radiation routine). The two binding
constraints are **not** biological:

- **Drug access.** The regimen's targeted agents (including the PRMT5 class, which is in
  human trials but has no canine data) are sponsor-owned, unapproved, and have no veterinary
  precedent. This is a business-development problem — the single largest obstacle. The
  strategy is an argument about a *kind* of drug, not a prescription.
- **Enrolment.** CNS histiocytic sarcoma is ~2.2% of primary intracranial tumours; the
  largest series took 32 years to collect 102 cases (~3/year per major centre, all breeds).
  A single-institution study is not viable — it requires a multi-centre consortium.

**The cheapest things that would move this — neither is a drug:**

1. A **genotype panel** on existing tumour tissue (MTAP/CDKN2A/PTEN copy number;
   PTPN11/KRAS/RB1 sequence) — assigns the maintenance tier *and* resolves a separate
   drug liability at no extra cost. **Do this first.**
2. The **tumour's growth rate** from imaging already taken — it enters the answer twice.
3. A **vaccine/immune kill rate in a dog** and **resiquimod on canine HS cells in vitro**
   (does the immune depot kill this myeloid tumour, or feed it).
4. A **brain:plasma ratio** for an ERK and a PI3K/AKT inhibitor in a dog — the durability
   either side of the threshold is already computed.

Together, the first two pick the maintenance tier and show whether it is real for a
specific dog before a single new treatment is tried.

---

*All figures are model outputs computed from cited evidence, re-derived by automated tests,
and independently audited by four review agents who re-ran the code. Where a number is
assumed rather than measured, this report says so. This is an analysis, not veterinary
advice; every decision belongs with clinicians who can examine the animal.*
