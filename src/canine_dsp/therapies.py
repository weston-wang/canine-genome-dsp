"""Conversation-derived catalogue of every therapy and drug discussed.

This module is a faithful, self-contained reconstruction of *every* therapy and
drug that came up anywhere in the long modelling conversation about durable
treatment of canine histiocytic sarcoma (HS) -- both the localized pulmonary
form and primary intracranial HS (PIHS).

It is built strictly from the human+assistant transcript
(`_refactor/conversation.txt`), NOT from the (now-deleted) `canine_dsp` source
tree. Nothing here imports from that package; standard library only.

WHAT "STATUS/VERDICT" MEANS HERE
--------------------------------
The conversation was ruthlessly iterative: claims were made, computed, and then
frequently retracted, superseded, or demoted when a number turned out to be
mismatched, circular, or unschedulable. Each record therefore carries both a
coarse `Verdict` bucket and a one-line free-text `status` that preserves the
*reason* the conversation actually reached -- including retractions.

THE LIVE / "CURRENT ANSWER" as the conversation last left it, for the
all-systemic/oral regimen:

    Induction : liposomal clodronate + hydroxychloroquine + anti-PD-1 (gilvetmab)
                + paxalisib + lisavanbulin + a PRMT5 inhibitor
    Maintenance: the PRMT5 inhibitor alone, indefinitely.

    Only the microtubule agent (lisavanbulin) is load-bearing; the other five
    widen individual margins. The regimen is explicitly NOT curative
    (response-then-relapse), and its "tolerable" verdict rests on two UNMEASURED
    canine toxicity numbers (PRMT5-inhibitor marrow budget; lisavanbulin's DLT
    being CNS/acute rather than marrow/cumulative).

A parallel, genotype-tiered *maintenance* frame was the last thing added:
    ~59% MAPK-driven (PTPN11/SHP2, KRAS)  -> MEK inhibitor (mirdametinib), site-split
    CDKN2A-deleted                        -> abemaciclib (the one BBB-crossing CDK4/6i)
    MTAP-deleted                          -> PRMT5 inhibitor (synthetic lethality)

RECURRING FAILURE MODE the conversation named for itself: "two numbers from
different contexts multiplied together" (a mouse potency with a dog dose; one
drug's brain penetration with another's blood level; an access term from a
monthly procedure with a continuous-dosing duty term). Most retractions below
trace to that.

AMBIGUITIES / THINGS DISCUSSED BUT NOT CLEANLY RESOLVED (see also inline notes):
  * "SHP2 inhibitors" were discussed only as a *node/class* (PTPN11/SHP2 is the
    driver); no specific SHP2-inhibitor drug was ever named or advanced.
  * Whether canine HS is MTAP/CDKN2A-*deleted somatically* is unknown -- the
    Shearin GWAS locus is GERMLINE and in the wrong breed (BMD). The whole
    PRMT5/synthetic-lethal arm is gated on a copy-number assay nobody has run.
  * Ferroptosis has never been studied in canine HS; the lineage argument for it
    cuts both ways (labile-iron-rich vs. professionally iron-buffered).
  * Whether canine HS tumour cells express TLR7/8 (which would make the innate
    depot *feed* the tumour via NF-kB) has never been checked -- the single risk
    that could invert a sign rather than reduce a magnitude.
  * The intrathecal/local-delivery arm produced a headline "470x margin" later
    audited as resting on placeholder constants; treated as retracted/overclaimed.
"""

from dataclasses import dataclass, field
from enum import Enum


class TherapyClass(Enum):
    """Mechanistic grouping actually present in the conversation."""

    ALKYLATING_CHEMO = "alkylating chemotherapy (nitrosoureas / triazenes / O6-alkylators)"
    PLATINUM = "platinum / N7-crosslinking agents"
    MICROTUBULE = "microtubule / mitotic-spindle poisons"
    MAPK_INHIBITOR = "MAPK-pathway inhibitors (MEK / ERK / BRAF / SHP2)"
    PI3K_AKT_MTOR = "PI3K / AKT / mTOR inhibitors"
    CDK46_INHIBITOR = "CDK4/6 inhibitors"
    SYNTHETIC_LETHAL_PRMT5 = "synthetic lethality (MTAP-deletion -> PRMT5 / MAT2A)"
    CSF1R_INHIBITOR = "CSF1R / lineage-survival-receptor inhibitors"
    FUSION_TKI = "fusion-driver / other targeted TKIs (branch C)"
    AURORA_KINASE = "aurora-kinase inhibitors"
    IMMUNE_CHECKPOINT = "immune checkpoint / antibody immunotherapy"
    VACCINE = "therapeutic cancer vaccines"
    CELL_THERAPY = "adoptive cell therapy (CAR-T / CAR-NK / NK / missing-self)"
    ONCOLYTIC_VIRUS = "oncolytic viruses"
    INNATE_ADJUVANT = "innate / local immune adjuvants (TLR7/8, VEGF-C, STING)"
    AUTOPHAGY = "autophagy / lysosome inhibitors"
    FERROPTOSIS = "ferroptosis inducers"
    OXPHOS = "OXPHOS / mitochondrial (persister-metabolism) inhibitors"
    NFKB_INHIBITOR = "NF-kB inhibitors"
    LINEAGE_DEPLETION = "macrophage-lineage depletion"
    MGMT_DIRECTED = "MGMT-directed / DNA-repair modulation"
    DELIVERY_ADJUNCT = "delivery adjuncts, routes and efflux modulation"
    LOCAL_MODALITY = "surgery / radiation (local cytoreduction)"


class Verdict(Enum):
    """Coarse bucket for where a therapy landed in the conversation."""

    IN_CURRENT_ANSWER = "in the current answer (live regimen)"
    MAINTENANCE_TIER = "genotype-tiered maintenance anchor (live, site-conditional)"
    SUPPORTING = "supporting / backbone in current answer (not load-bearing)"
    SUPERSEDED = "superseded by a later regimen"
    RETRACTED = "retracted (claim withdrawn for a specific reason)"
    REJECTED = "rejected (evaluated and ruled out)"
    DEMOTED_DELAY_ONLY = "demoted to delay-only (duration-capped, no durability)"
    CONSIDERED_UNMEASURED = "considered; potency/status unmeasured in this disease"
    PROSE_ONLY = "prose-only candidate (no computed kill rate)"
    COMPARATOR = "used as a comparator / evidence anchor, not a proposed drug"


@dataclass(frozen=True)
class Therapy:
    """One drug or therapy as the conversation actually treated it."""

    name: str
    therapy_class: TherapyClass
    mechanism: str          # one line
    verdict: Verdict
    status: str             # the faithful, specific verdict/reason we reached
    key_numbers: str = ""   # IC50 / access(Kp) / potency / PMID etc., if cited
    aliases: tuple[str, ...] = field(default_factory=tuple)


# ---------------------------------------------------------------------------
# THE CATALOGUE
# ---------------------------------------------------------------------------

THERAPIES: tuple[Therapy, ...] = (

    # --- Alkylating chemotherapy -------------------------------------------
    Therapy(
        "Temozolomide",
        TherapyClass.ALKYLATING_CHEMO,
        "Oral triazene that methylates the O6 position of guanine.",
        Verdict.RETRACTED,
        "Briefly the sole load-bearing drug of an intra-arterial regimen, then "
        "retracted twice over: (1) schedule-coherence contradiction -- monthly "
        "IA/osmotic access cannot be multiplied by continuous (duty 1.0); "
        "(2) defeated by MGMT and, more fundamentally, by class-wide alkylator "
        "resistance in canine HS. Given (after nimustine) in the real 2024 this breed "
        "PIHS case; dog died day 195.",
        "canine HS resists O6-alkylators 134-670x; MGMT makes lomustine 4.3-4.9x "
        "less potent (PMID 26130852); intrinsic brain access ~0.20; weak dual "
        "P-gp/BCRP substrate (~1.5x penetration boost, PMID 29852323).",
        aliases=("TMZ",),
    ),
    Therapy(
        "Lomustine (CCNU)",
        TherapyClass.ALKYLATING_CHEMO,
        "Lipophilic nitrosurea alkylator; canine HS standard-of-care chemo.",
        Verdict.DEMOTED_DELAY_ONLY,
        "Real, potent, but duration-capped by cumulative hepatotoxicity (~105 "
        "days) -> can only buy delay, never durability (cannot permanently flip a "
        "margin sign). Considered as an optional early bridge, then demoted. "
        "Also a marrow/liver toxicity axis and defeated by the same alkylator "
        "resistance / MGMT wall.",
        "finite lomustine course gives ~0.375 durable / ~44-day median benchmark "
        "used as the model's reality gut-check.",
        aliases=("CCNU",),
    ),
    Therapy(
        "Nimustine (ACNU)",
        TherapyClass.ALKYLATING_CHEMO,
        "Nitrosurea O6-alkylator (same repair-defeated lesion class as TMZ).",
        Verdict.CONSIDERED_UNMEASURED,
        "Given in the published Oct-2024 predisposed dog breed PIHS case (partial "
        "response, tumour shrank by day 99, regrowth by day 124); the switch to "
        "temozolomide afterwards was a within-class move that changes nothing "
        "about resistance.",
        "canine HS IC50 190,000-587,000 ng/ml -> 134-670x resistant (PMID 25715778).",
        aliases=("ACNU",),
    ),
    Therapy(
        "Carmustine (BCNU)",
        TherapyClass.ALKYLATING_CHEMO,
        "Nitrosurea alkylator; discussed as the carmustine-wafer local-chemo class.",
        Verdict.CONSIDERED_UNMEASURED,
        "Named in the broad local-therapy scan (carmustine-wafer / brachytherapy "
        "class) as absent from the modules; never parameterized or advanced.",
        aliases=("BCNU",),
    ),
    Therapy(
        "Melphalan",
        TherapyClass.ALKYLATING_CHEMO,
        "N7-guanine DNA crosslinker (same lesion class as carboplatin).",
        Verdict.COMPARATOR,
        "The datum that FALSIFIED the carboplatin fix: canine HS resists melphalan "
        "42-411x, an N7-crosslinker -- so the resistance is alkylator-CLASS-shaped, "
        "not MGMT-shaped. Likely cause named: reduced MSH6 (mismatch-repair loss).",
        "canine HS IC50 29,000-65,000 ng/ml -> 42-411x resistant (PMID 25715778).",
    ),

    # --- Platinum -----------------------------------------------------------
    Therapy(
        "Carboplatin",
        TherapyClass.PLATINUM,
        "Platinum agent; crosslinks at N7-guanine, a lesion MGMT cannot repair.",
        Verdict.RETRACTED,
        "Proposed as the MGMT rescue (margin identical whether MGMT competent or "
        "silenced, so the answer stops depending on the unknown), then retracted: "
        "melphalan shows the whole N7/alkylator class is resisted 42-411x, and it "
        "inherits the IA schedule-coherence defect. (Also appears as toceranib+"
        "carboplatin in the negative HSA/osteosarcoma trials.)",
    ),

    # --- Microtubule / mitotic poisons -------------------------------------
    Therapy(
        "Vincristine",
        TherapyClass.MICROTUBULE,
        "Vinca alkaloid; microtubule destabilizer.",
        Verdict.CONSIDERED_UNMEASURED,
        "Canine HS is highly sensitive to it in vitro, but it is a canonical P-gp "
        "substrate and these cells overexpress the pumps, so it is pumped back out "
        "of the brain. Listed in the systemic microtubule catalogue as MGMT-free.",
        "canine HS IC50 1.77-2.69 ng/ml -- as/more sensitive than a chemosensitive "
        "comparator (PMID 25715778).",
    ),
    Therapy(
        "Vinblastine",
        TherapyClass.MICROTUBULE,
        "Vinca alkaloid; microtubule destabilizer.",
        Verdict.CONSIDERED_UNMEASURED,
        "Same profile as vincristine -- highly HS-sensitive but a P-gp substrate "
        "excluded from brain.",
        "canine HS IC50 1.75-2.78 ng/ml -> 4-14x more sensitive (PMID 25715778).",
    ),
    Therapy(
        "Vinorelbine",
        TherapyClass.MICROTUBULE,
        "Vinca alkaloid; microtubule destabilizer.",
        Verdict.CONSIDERED_UNMEASURED,
        "Raised as a microtubule option and sent to a verification agent for its "
        "drug/number pairing; P-gp-limited like the other vincas.",
    ),
    Therapy(
        "Paclitaxel",
        TherapyClass.MICROTUBULE,
        "Taxane; microtubule stabilizer.",
        Verdict.COMPARATOR,
        "HS-sensitive but the negative-control for brain access: brain:plasma 0.0 "
        "(below detection) in the same experiment where sagopilone measured 0.80. "
        "P-gp substrate, pumped out of brain.",
        "canine HS IC50 23.8-58.4 ng/ml -> 2-11x more sensitive (PMID 25715778); "
        "brain:plasma 0.0.",
    ),
    Therapy(
        "Sagopilone",
        TherapyClass.MICROTUBULE,
        "Epothilone microtubule stabilizer; NOT a P-gp substrate.",
        Verdict.SUPERSEDED,
        "The original brain-penetrant microtubule candidate (access from chemistry, "
        "not surgery). Superseded by lisavanbulin: DISCONTINUED by Bayer for "
        "peripheral neuropathy (the exact axis that binds here), and it failed "
        "glioblastoma phase II (no objective responses) -- the 'brain-penetrant is "
        "not brain-effective' trap. Its Kp still supplies the model's microtubule "
        "access assumption; its +0.25 marrow load is why the generic microtubule "
        "placeholder is intolerable and lisavanbulin specifically is required.",
        "brain:plasma 0.80 measured; glioblastoma PFS6 6.7%; neuropathy 46%.",
    ),
    Therapy(
        "Lisavanbulin (BAL101553)",
        TherapyClass.MICROTUBULE,
        "Oral tubulin-binding (EB-dependent) mitotic poison; 1:1 brain:plasma.",
        Verdict.IN_CURRENT_ANSWER,
        "The single load-bearing agent of the current answer. Chosen because its "
        "dose-limiting toxicity is ACUTE CNS (dose-capped, not duration-capped) "
        "rather than cumulative neuropathy or marrow -- which is the only reason "
        "the PRMT5 arm fits at all (a marrow-loading microtubule agent pushes "
        "marrow to 1.05 -> intolerable). Not discontinued: rights held by the "
        "Glioblastoma Foundation with a post-trial access programme.",
        "peripheral neuropathy 1/26 (4%) vs sagopilone 46%; brain:plasma ~1:1 "
        "(rodent); phase 1/2a, Cell Reports Medicine 2025. Kill rate hard-coded "
        "0.15/day (assumed, not derived from IC50).",
        aliases=("BAL101553",),
    ),
    Therapy(
        "RGN3067",
        TherapyClass.MICROTUBULE,
        "Oral brain-penetrant microtubule agent (mitotic poison).",
        Verdict.CONSIDERED_UNMEASURED,
        "One of three interchangeable microtubule candidates (only one is needed). "
        "Preclinical (Reglagene), oral, rodent-only; notably active against a "
        "temozolomide-resistant line. Not obtainable -- a class argument, not a "
        "prescription.",
        "efflux ratio 0.61; high brain levels after oral dosing.",
    ),
    Therapy(
        "RGN6024",
        TherapyClass.MICROTUBULE,
        "Brain-penetrant microtubule agent (mitotic poison).",
        Verdict.CONSIDERED_UNMEASURED,
        "Interchangeable microtubule candidate; preclinical, IND projected mid-2024 "
        "with no trial evident in late-2025 publications. Not obtainable.",
    ),

    # --- MAPK-pathway inhibitors -------------------------------------------
    Therapy(
        "Trametinib",
        TherapyClass.MAPK_INHIBITOR,
        "MEK1/2 inhibitor.",
        Verdict.SUPERSEDED,
        "Central to the early work and still the standard MAPK anchor, but dropped "
        "from the drug-only regimen: its coverage is a strict subset of an ERK "
        "inhibitor's while it consumes half the shared MAPK toxicity budget. Fails "
        "intracranially (brain:plasma 0.15 -> sensitive clone grows). Its 15/33/180 "
        "nM canine IC50 was RETRACTED as unverifiable (6-7 access attempts). "
        "Sakuma 2025 (banked but not propagated): trametinib response varies across "
        "canine HS lines and is NOT predicted by ERK/Akt activation -- NF-kB "
        "stratifies them.",
        "brain:plasma ~0.15 (P-gp/BCRP substrate); Voruz 2018 PTPN11 case PR at 2 "
        "months, progressed at 5; MAP2K1-mutant HS complete response >2yr "
        "(Gounder, NEJM 2018, PMID 29768143).",
    ),
    Therapy(
        "Cobimetinib",
        TherapyClass.MAPK_INHIBITOR,
        "MEK inhibitor; supplies the real measured canine-HS potency anchor.",
        Verdict.COMPARATOR,
        "The measured potency 'trametinib' was modelled on. Real canine HS IC50s "
        "vs canine Cmax show the exposure problem belongs to trametinib, not to MEK "
        "inhibition per se (Cmax sits 9.2x above its own canine HS IC50).",
        "canine HS IC50 74/91/372 nM (BD/OD/DH82) vs Cmax ~1640 nM (PMID 39202410); "
        "Kp 0.32 / Kp,uu 0.027 (P-gp substrate, not BCRP); 95% protein bound.",
    ),
    Therapy(
        "Mirdametinib (PD-0325901)",
        TherapyClass.MAPK_INHIBITOR,
        "CNS-selected MEK1/2 inhibitor.",
        Verdict.MAINTENANCE_TIER,
        "The brain-penetrant MEK candidate for the MAPK-majority (~59%) maintenance "
        "tier and the brain second-primary branch -- graded MEDIUM and site-split: "
        "SOLID for lung/disseminated, CONDITIONAL for brain. The 0.50 brain access "
        "in the model is a THRESHOLD/hypothesis, not a measured number; no canine "
        "brain:plasma ratio exists for it.",
        "FDA-approved Feb 2025 (NF1-PN); pediatric low-grade glioma trials; "
        "Kp,uu NOT FOUND.",
        aliases=("PD-0325901",),
    ),
    Therapy(
        "ERK1/2 inhibitor (temuterkib / LY3214996)",
        TherapyClass.MAPK_INHIBITOR,
        "ERK1/2 inhibitor at the convergence node below MEK.",
        Verdict.IN_CURRENT_ANSWER,
        "The lead of the two-agent drug-only lung regimen (ERKi at single-agent MTD "
        "+ PI3K/AKTi): sits downstream of 2 of 3 MEK-escape lesions, so a MEK-site "
        "mutation and restored upstream flow don't confer escape from it. Lung: "
        "durability 1.00 full dose / 0.99 realistic. Brain: fails at trametinib-like "
        "penetration. Honest ceiling: an ERKi-resistant clone is a single point of "
        "failure (+0.0089/day). Project REFUSED to assign temuterkib a brain Kp; "
        "its IC50/Emax are placeholders; investigational, no vet use.",
        "temuterkib biochemical IC50 5 nM; phase-0 trigger trial reached "
        "pharmacologically relevant conc. in Gd-non-enhancing GBM; model placeholder "
        "IC50 300 nM, max_kill 0.14-0.18/day (pinned backwards).",
        aliases=("temuterkib", "LY3214996", "ERKi"),
    ),
    Therapy(
        "Ulixertinib",
        TherapyClass.MAPK_INHIBITOR,
        "ERK1/2 inhibitor.",
        Verdict.CONSIDERED_UNMEASURED,
        "Named as a member of the ERK-inhibitor class considered for the convergence "
        "role; not parameterized.",
    ),
    Therapy(
        "Dabrafenib",
        TherapyClass.MAPK_INHIBITOR,
        "BRAF (V600) inhibitor.",
        Verdict.COMPARATOR,
        "Human evidence anchor: a BRAF-V600 HS patient in partial remission at 3 "
        "years on dabrafenib+trametinib. But dabrafenib+trametinib was explicitly "
        "REJECTED as a canine-HS calibration comparator -- mismatched species, "
        "disease, driver (BRAF vs PTPN11/KRAS) and combination mechanism.",
        "melanoma COMBI-d/v: mPFS ~11mo, ORR 64-69%, 5yr PFS ~19%.",
    ),
    Therapy(
        "Vemurafenib",
        TherapyClass.MAPK_INHIBITOR,
        "BRAF (V600E) inhibitor.",
        Verdict.COMPARATOR,
        "Proof-of-concept that intracranial MAPK targeting can work: a BRAF-V600E "
        "primary CNS HS patient had a 'dramatic response' to vemurafenib alone.",
    ),
    Therapy(
        "SHP2 inhibition (PTPN11 node)",
        TherapyClass.MAPK_INHIBITOR,
        "Blockade of SHP2/PTPN11, the mutated upstream node in canine HS.",
        Verdict.CONSIDERED_UNMEASURED,
        "Discussed only as a mechanistic node/class -- PTPN11/SHP2 is the dominant "
        "driver (E76K etc.) and CSF1R->SHP2->RAS->RAF->MEK->ERK is the cascade -- "
        "but NO specific SHP2-inhibitor drug was ever named or advanced. The drug "
        "hits MEK/ERK downstream instead.",
        "PTPN11 mutations ~55.8% of HS / 46.2% hemophagocytic HS; KRAS Q61H "
        "(PMC11353564).",
    ),

    # --- PI3K / AKT / mTOR --------------------------------------------------
    Therapy(
        "Paxalisib (GDC-0084)",
        TherapyClass.PI3K_AKT_MTOR,
        "PI3K/mTOR inhibitor, engineered for BBB penetration (low efflux).",
        Verdict.IN_CURRENT_ANSWER,
        "The PI3K/AKT axis of both the two-agent lung regimen and the current-answer "
        "backbone; a non-P-gp/BCRP substrate, so access comes from chemistry. Its "
        "measured brain penetration collapsed the old '~0.5 requirement' (an "
        "artifact of moving both agents together) to ~0.235-0.30 for the ERK agent. "
        "Investigational human oncology drug -- a supply/regulatory problem in dogs, "
        "not a scientific one.",
        "brain:plasma 1.9-3.3 (rat), ~1.0 clinical; modelled access Kp,uu 0.31; "
        "GBM-AGILE phase II/III.",
        aliases=("GDC-0084",),
    ),
    Therapy(
        "Sapanisertib",
        TherapyClass.PI3K_AKT_MTOR,
        "Dual TORC1/2 inhibitor (blocks the mTORC2->AKT feedback rapalogs miss).",
        Verdict.CONSIDERED_UNMEASURED,
        "A better-evidenced parallel agent than paxalisib for the LUNG cells -- it "
        "has canine PK, canine tolerability in combination with trametinib, and a "
        "real supply history -- and TORC1/2 is the convergence node of the PI3K "
        "axis (mirrors the ERK-over-MEK convergence logic). Missed in the original "
        "analysis. No CNS data, so paxalisib keeps the brain slot.",
    ),
    Therapy(
        "Duvelisib",
        TherapyClass.PI3K_AKT_MTOR,
        "PI3K-delta/gamma inhibitor; FDA-approved.",
        Verdict.CONSIDERED_UNMEASURED,
        "The best measured canine-HS parallel-agent anchor: selectively active in "
        "the Group A subgroup only (pAkt fell in all 8 Group A lines, none in Group "
        "B). Adding it to local MAPK therapy takes Group A 0.961->1.000 and barely "
        "moves Group B -- reproducing Sakuma's two-subgroup finding. Nothing among "
        "1,824 screened compounds worked for Group B.",
        "canine HS Group A IC50 287 nM vs Group B >5 uM; >7.46 uM vs normal PBMCs.",
    ),
    Therapy(
        "VDC-597",
        TherapyClass.PI3K_AKT_MTOR,
        "Dual PI3K/mTOR inhibitor.",
        Verdict.CONSIDERED_UNMEASURED,
        "Supplied the real canine PI3K potency that overturned the claim that 'no "
        "canine PI3K measurement exists' -- the 0.10/day PI3K assumption was in fact "
        "conservative. Originally an HSA cell-line measurement, additive with "
        "doxorubicin; later borrowed for HS.",
        "canine IC50 230/690/710 nM (mean 543), Pyuen 2018 PMID 30011343; canine "
        "dose-escalation reached no MTD, target engagement 8/10 dogs (Paoloni 2010, "
        "PMID 20543980).",
    ),

    # --- CDK4/6 -------------------------------------------------------------
    Therapy(
        "Abemaciclib",
        TherapyClass.CDK46_INHIBITOR,
        "CDK4/6 inhibitor; the one CDK4/6i that crosses the BBB.",
        Verdict.MAINTENANCE_TIER,
        "Role sized down from 'the biggest lever' to a bar-lowerer after the real "
        "potency correction (illustrative 100 nM RETRACTED; real canine 910-3090 nM "
        "-> only 6-29% target saturation, 5-25% bar reduction not 76-81%). NOT "
        "droppable in the brain (dropping it pushes the required delivery budget to "
        "1.168 -> impossible) -- that recommendation was itself retracted. Now the "
        "CDKN2A-deleted maintenance anchor; also de-represses ERVs (branch-D "
        "priming). Marrow toxicity axis.",
        "canine IC50 910-3090 nM; unbound brain-met ~96x CDK4 IC50 / ~19x CDK6; "
        "bar 0.057 -> 0.043/day (lung).",
    ),
    Therapy(
        "Palbociclib",
        TherapyClass.CDK46_INHIBITOR,
        "CDK4/6 inhibitor; P-gp/BCRP-limited (poor CNS).",
        Verdict.CONSIDERED_UNMEASURED,
        "Tested on canine histiocytic/lymphoma/mammary/melanoma cells (dose-"
        "dependent antiproliferative effect); p16/CDKN2A proposed as a sensitivity "
        "biomarker (Maylina 2023). Poor brain penetration rules it out for PIHS.",
    ),
    Therapy(
        "Ribociclib",
        TherapyClass.CDK46_INHIBITOR,
        "CDK4/6 inhibitor; P-gp/BCRP-limited (poor CNS).",
        Verdict.CONSIDERED_UNMEASURED,
        "Named alongside palbociclib as a CDK4/6i that, unlike abemaciclib, does not "
        "cross the BBB.",
    ),
    # NOTE: the "CDKN2A/MTAP loss -> CDK4/6i sensitivity" rationale was RETRACTED
    # in-conversation (CDKN2A-mutant cancers without co-occurring D-cyclin lesions
    # rarely show high sensitivity) -- but that retraction never reached the origin
    # module, an unresolved ambiguity.

    # --- Synthetic lethality / PRMT5 ---------------------------------------
    Therapy(
        "PRMT5 inhibitor (generic)",
        TherapyClass.SYNTHETIC_LETHAL_PRMT5,
        "Synthetic-lethal with MTAP homozygous deletion (MTA accumulation "
        "partially inhibits PRMT5, leaving no reserve).",
        Verdict.IN_CURRENT_ANSWER,
        "The strongest arm ever computed (tier iv-a, 0.98 at 10yr) AND the sole "
        "maintenance agent of the current answer. Antigen-free, immune-free, and "
        "uniquely durable because the target is a deletion the tumour cannot "
        "un-delete -> all-clone coverage by descent. Not unbeatable: model seeds a "
        "double-resistant clone. Marrow toxicity shares the CDK4/6i axis (drop "
        "CDK4/6i to fit). Its marrow budget (0.35) is an unmeasured ordinal guess "
        "on which the entire 10-year arm rides.",
        "modelled IC50 500 nM, max_kill 0.12/day; brain access requirement "
        "~0.69-0.89 (4.6x trametinib); gated on an unrun somatic MTAP copy-number "
        "assay (Shearin GWAS locus is germline, wrong breed).",
    ),
    Therapy(
        "TNG908",
        TherapyClass.SYNTHETIC_LETHAL_PRMT5,
        "Brain-penetrant, MTA-cooperative PRMT5 inhibitor.",
        Verdict.CONSIDERED_UNMEASURED,
        "Real named brain-penetrant PRMT5 inhibitor, in phase I/II including "
        "glioblastoma -- directly relevant since MTAP-CDKN2A is the canine HS "
        "predisposition locus. No canine PK/BBB/formulation data.",
    ),
    Therapy(
        "TNG462",
        TherapyClass.SYNTHETIC_LETHAL_PRMT5,
        "More potent MTA-cooperative PRMT5 inhibitor.",
        Verdict.CONSIDERED_UNMEASURED,
        "The more potent successor to TNG908; roughly five such agents were in the "
        "clinic as of 2025. No canine data.",
    ),
    Therapy(
        "MAT2A inhibitor",
        TherapyClass.SYNTHETIC_LETHAL_PRMT5,
        "Blocks SAM synthesis; alternative synthetic-lethal node for MTAP-deletion.",
        Verdict.CONSIDERED_UNMEASURED,
        "The interchangeable partner node to PRMT5 in the MTAP-deletion synthetic-"
        "lethal arm; same gating, no canine data.",
    ),

    # --- CSF1R inhibitors ---------------------------------------------------
    Therapy(
        "Pexidartinib (PLX3397)",
        TherapyClass.CSF1R_INHIBITOR,
        "CSF1R inhibitor; in a histiocytic tumour CSF1R is the tumour cell's own "
        "lineage-survival receptor (so blockade is direct tumour kill).",
        Verdict.CONSIDERED_UNMEASURED,
        "Reframed from a TAM-depletion adjunct to a direct, persistent, antigen-"
        "independent, MAPK-independent driver-directed agent -- but the durability "
        "OVERCLAIM was RETRACTED: the cited Erdheim-Chester complete response was an "
        "INDIRECT (CBL) dependency that became pexidartinib-resistant and "
        "transformed to HS at 15 months; only DIRECT CSF1R-activating mutation held "
        ">1.5yr. Hepatotoxicity DLT; depletes essentially all microglia; DM/SOD1 "
        "interaction (route TOX-1). Gated on CSF1R sequencing.",
        "IC50 ~20 nM, BBB-penetrant; required 0.0185-0.0391/day at the pessimistic "
        "access bound (zero at the optimistic bound).",
        aliases=("PLX3397",),
    ),
    Therapy(
        "Vimseltinib",
        TherapyClass.CSF1R_INHIBITOR,
        "Switch-control CSF1R inhibitor; lacks pexidartinib's hepatotoxicity.",
        Verdict.CONSIDERED_UNMEASURED,
        "Proposed swap over pexidartinib -- the safety benefit (no hepatotoxicity) "
        "is real and immediate; the resistance benefit is mechanism-based and "
        "untested. FDA-approved Feb 2025.",
    ),
    Therapy(
        "BLZ945",
        TherapyClass.CSF1R_INHIBITOR,
        "Brain-penetrant CSF1R inhibitor (tool/clinical compound).",
        Verdict.COMPARATOR,
        "Cited on both sides of the 'established tumour' debate: Pyonteck 2013 found "
        "majority regression in established, unresected glioma with BLZ945 (opposite "
        "of the O'Brien 'minimal effect' caveat). Repo records it as brain-penetrant "
        "with limited efficacy elsewhere -- the 'brain-penetrant is not brain-"
        "effective' point.",
        "Pyonteck 2013: 64.3% survival to 26 weeks vs 5.7-week median.",
    ),

    # --- Fusion-driver / other TKIs (branch C) -----------------------------
    Therapy(
        "Toceranib (Palladia)",
        TherapyClass.FUSION_TKI,
        "Multi-kinase inhibitor (FLT3, CSF1R, VEGFR, PDGFR, KIT); "
        "the only FDA-approved canine kinase inhibitor.",
        Verdict.CONSIDERED_UNMEASURED,
        "Covers the FLT3 slice of the fusion branch AND the CSF1R axis with real "
        "canine dosing/supply. But: its only real efficacy readout is NEGATIVE "
        "(Gardner HSA trial, DFI 161d, 81% metastasized, no MST benefit); it misses "
        "ALK/NTRK/RET/FGFR; and as a sunitinib analog it likely penetrates the CNS "
        "poorly -- a PIHS-specific failure.",
        "Gardner et al. BMC Vet Res 2015 (PMC4464614): MST 172 vs 169 days.",
        aliases=("Palladia",),
    ),
    Therapy(
        "Larotrectinib / Entrectinib",
        TherapyClass.FUSION_TKI,
        "NTRK-fusion inhibitors (entrectinib CNS-penetrant by design).",
        Verdict.CONSIDERED_UNMEASURED,
        "Matched drugs for NTRK-fusion-driven HS -- real and approved, but human-"
        "only/off-label and never parameterized in the model. The dominant NTRK "
        "resistance mode is on-target (solvent-front G595R/G623R), which KEEPS the "
        "fusion -- so a fusion-junction vaccine target survives it.",
        "'7 of 9' solvent-front resistance figure was flagged as unattributed (no PMID).",
    ),
    Therapy(
        "Lorlatinib / Alectinib",
        TherapyClass.FUSION_TKI,
        "ALK-fusion inhibitors (CNS-penetrant).",
        Verdict.CONSIDERED_UNMEASURED,
        "Matched, CNS-penetrant options for an ALK-fusion driver; human-only, "
        "never parameterized.",
    ),
    Therapy(
        "Selpercatinib",
        TherapyClass.FUSION_TKI,
        "RET-fusion inhibitor.",
        Verdict.CONSIDERED_UNMEASURED,
        "Matched drug for a RET-fusion driver; human-only, off-label, never "
        "parameterized.",
    ),
    Therapy(
        "Pemigatinib",
        TherapyClass.FUSION_TKI,
        "FGFR-fusion inhibitor.",
        Verdict.CONSIDERED_UNMEASURED,
        "Matched drug for an FGFR-fusion driver; used in a real canine histiocytic-"
        "neoplasm index case (KIF5B-FGFR1). Human-only, never parameterized.",
    ),
    Therapy(
        "Sorafenib",
        TherapyClass.FUSION_TKI,
        "Multi-kinase inhibitor (also ferroptosis-adjacent).",
        Verdict.CONSIDERED_UNMEASURED,
        "Used in a real canine histiocytic index case (MEF2C-FLT3). Also the "
        "ferroptosis-adjacent agent with the most GBM trial volume (12/14 studies), "
        "though its ferroptosis mechanism (SLC7A11/BECN1) is contested as off-target; "
        "poor CNS penetration (P-gp/BCRP dual substrate).",
    ),
    Therapy(
        "Imatinib",
        TherapyClass.FUSION_TKI,
        "BCR-ABL / KIT / PDGFR TKI.",
        Verdict.COMPARATOR,
        "Named in the human Voruz 2018 case: response to combined MEK inhibition "
        "(trametinib) and tyrosine-kinase inhibition (imatinib) in multifocal "
        "histiocytic sarcoma.",
    ),
    Therapy(
        "Dasatinib / Ponatinib",
        TherapyClass.FUSION_TKI,
        "SRC/ABL-family multi-kinase inhibitors.",
        Verdict.COMPARATOR,
        "Screened in Sakuma 2025 across canine HS lines: no differential sensitivity "
        "to dasatinib, trametinib or ponatinib -- pointing at NF-kB, not MAPK, as "
        "the discriminating axis.",
    ),

    # --- Aurora kinase ------------------------------------------------------
    Therapy(
        "AT9283",
        TherapyClass.AURORA_KINASE,
        "Aurora-kinase (and JAK) inhibitor; acts in mitosis.",
        Verdict.SUPERSEDED,
        "Briefly the lead systemic find (achievable concentration ABOVE its canine "
        "HS IC50 -- the property trametinib lacks; lung 0.973), then demoted to a "
        "non-MAPK fallback and finally dropped: DISCONTINUED (a research chemical); "
        "mitotic, so blind to persisters; the human Cmax was mislabelled as steady "
        "state; and the 'delivery is the whole therapy' premise it rode was shown "
        "to be trametinib-specific, not a real barrier for MEK/ERK inhibition.",
        "canine HS IC50 117.5-285.7 nM (PMC11940154); patients reach 488-650 nM "
        "(human Cmax, 72h infusion) -> 2.4x above IC50.",
    ),
    Therapy(
        "BI-847325",
        TherapyClass.AURORA_KINASE,
        "Dual aurora/MEK inhibitor.",
        Verdict.REJECTED,
        "Considered alongside AT9283 but its development was halted for the same "
        "toxicity reason that sinks trametinib in dogs.",
    ),

    # --- Immune checkpoint / antibody --------------------------------------
    Therapy(
        "Anti-PD-1 (gilvetmab)",
        TherapyClass.IMMUNE_CHECKPOINT,
        "Canine anti-PD-1 antibody; relieves T-cell exhaustion / multiplies "
        "vaccine-primed effectors.",
        Verdict.SUPPORTING,
        "In the current-answer backbone and the brain/antigen cell. The only real, "
        "already-manufactured canine checkpoint drug here (USDA-conditionally "
        "licensed, off-label for HS). Cannot be standalone and explicitly cannot "
        "cover MHC-I-loss escape; its multiplier is swept (1.25x rescues the CNS "
        "discount at 0.75) but never anchored to a measured value.",
        "MCT ORR 46%, melanoma ORR 20% (JVIM 2026).",
        aliases=("gilvetmab", "PD-1"),
    ),
    Therapy(
        "Pembrolizumab",
        TherapyClass.IMMUNE_CHECKPOINT,
        "Human anti-PD-1 antibody.",
        Verdict.COMPARATOR,
        "Cited as the only human precedent pairing a KRAS hotspot vaccine with "
        "checkpoint blockade (tumour shrinkage in both patients, n=2) -- the "
        "combination HS's own PD-L1/PD-L2 finding suggests might matter.",
    ),
    Therapy(
        "Nivolumab",
        TherapyClass.IMMUNE_CHECKPOINT,
        "Human anti-PD-1 antibody.",
        Verdict.COMPARATOR,
        "Mentioned in passing as a human checkpoint agent; not advanced for dogs.",
    ),
    Therapy(
        "Anti-CD47 / SIRPa blockade",
        TherapyClass.IMMUNE_CHECKPOINT,
        "Blocks the CD47 'don't-eat-me' signal, licensing macrophage phagocytosis.",
        Verdict.PROSE_ONLY,
        "A post-resection glioma paper pairing surgical debulking with CD47 blockade "
        "was surfaced in the same search that found the depot and never opened; "
        "CD47 appears in zero modules. A non-division-gated, antigen-independent "
        "candidate -- considered but never computed.",
    ),

    # --- Vaccines -----------------------------------------------------------
    Therapy(
        "Hotspot / neoantigen peptide vaccine",
        TherapyClass.VACCINE,
        "Synthetic-long-peptide / mRNA-LNP vaccine against driver-mutation "
        "neoepitopes presented on DLA.",
        Verdict.SUPERSEDED,
        "Long the proposed durability mechanism (the only thing that permanently "
        "flips resistance-clone growth signs), fully specified from 6 real peptides "
        "at verified canine-aligned positions -- but later de-emphasized when the "
        "drug-only regimen reached 1.00 with no vaccine, and it never covers the "
        "antigen-loss/MHC-I blind spot. Gated on premise 0b (a vaccinatable "
        "neoantigen exists), which is unmeasured, and on the vaccine clearing its "
        "own potency bar.",
        "AMPLIFY-201 implied kill 0.053/day (re-anchored to 92-day relapse timing "
        "after a circularity fix; earlier '12% short' was 1-HR restated).",
    ),
    Therapy(
        "Fusion-junction vaccine",
        TherapyClass.VACCINE,
        "Vaccine against a gene-fusion breakpoint peptide.",
        Verdict.CONSIDERED_UNMEASURED,
        "Arguably the best antigen in the whole analysis: no self counterpart in the "
        "proteome, retained under the dominant on-target resistance mode, and shared "
        "across dogs with the same fusion. The enumeration tool exists (34 peptides "
        "x 3 DLA alleles = 102 predictions, exhaustive). Gated entirely on a fusion "
        "actually being found -- none has been reported in canine HS (needs RNA-seq; "
        "invisible to WES).",
    ),
    Therapy(
        "Telomerase DNA vaccine",
        TherapyClass.VACCINE,
        "Anti-telomerase (self-antigen) DNA/xenogeneic vaccine.",
        Verdict.COMPARATOR,
        "Platform evidence only: Peruzzi 2010 vaccinated lymphoma-bearing dogs "
        "(MST 97.8 vs 37 weeks); Thalmensi immunized beagles with strong ELISpot "
        "responses. Real same-species proof a vaccine can work in a dog, but a "
        "self-antigen in the wrong lineage -- closes none of the antigen-specific gap.",
    ),

    # --- Adoptive cell therapy ---------------------------------------------
    Therapy(
        "CD204-directed cell therapy (CAR-NK / CAR-T)",
        TherapyClass.CELL_THERAPY,
        "Cell therapy against CD204, a macrophage-lineage marker expressed "
        "universally on canine HS.",
        Verdict.PROSE_ONLY,
        "Conceptually ideal: driver-agnostic (covers the 75-85% MAPK-wild-type "
        "prior), antigen-loss-proof (the target IS the lineage identity, not a "
        "losable neoantigen), MHC-independent, CNS-trafficking; scores 0.973 in the "
        "modal cell. But it does not exist -- canine CAR-NK has never been built, no "
        "CD204-CAR aimed, no CNS-trafficking fraction measured; 0.20/day is a "
        "requirement, not an achieved rate. A direction, not an option.",
        "CD204 expressed in 50/50 canine HS tumours (universal marker).",
    ),
    Therapy(
        "CAR-T (anti-CD18 / anti-CSF1R)",
        TherapyClass.CELL_THERAPY,
        "Chimeric-antigen-receptor T cells against an HS lineage marker.",
        Verdict.REJECTED,
        "Best clone coverage of any modality but dropped: no tumour-restricted HS "
        "antigen exists (CD18 is on every leukocyte, CSF1R on every macrophage/"
        "microglia); intracranial CRS/ICP risk in a closed skull; a published "
        "CSF1R-CAR agonism hazard (ligation could drive target-cell proliferation). "
        "Coverage and toxicity are the same fact. Canine CAR-T platform is real "
        "(Panjwani 2020; CD20, B7-H3 trials).",
    ),
    Therapy(
        "CAR-NK",
        TherapyClass.CELL_THERAPY,
        "Chimeric-antigen-receptor NK cells.",
        Verdict.CONSIDERED_UNMEASURED,
        "Lower CRS/neurotoxicity than CAR-T (matters inside the skull) but shorter "
        "persistence (cuts against durability) and the same missing-antigen problem. "
        "Bolting a CAR onto NK also re-imposes the antigen dependency that "
        "missing-self was chosen to escape; only anti-CD204 CAR-NK is worth pursuing.",
    ),
    Therapy(
        "NK-cell transfer / missing-self / NKG2D",
        TherapyClass.CELL_THERAPY,
        "NK (or vaccine-primed T) cells killing MHC-I-low escape variants without "
        "peptide recognition, via NKG2D-NKG2DL.",
        Verdict.DEMOTED_DELAY_ONLY,
        "The one mechanism whose target IS the antigen-loss clone; requires prior "
        "TCR activation the vaccine supplies. Cut from the minimal regimen (changed "
        "nothing above threshold). As a fixed adoptive-transfer course it is "
        "duration-capped -> delay only. Canine NK transfer is real (Canter 2017 + "
        "RT); the NCI-COTC030 inhaled-IL-15 trial was a real NEGATIVE result.",
        "required NKG2D fraction 61-69% at real drug potency.",
    ),

    # --- Oncolytic viruses --------------------------------------------------
    Therapy(
        "Oncolytic reovirus",
        TherapyClass.ONCOLYTIC_VIRUS,
        "Ras-pathway-permissive lytic virus plus in-situ vaccination.",
        Verdict.DEMOTED_DELAY_ONLY,
        "Raised as the most concrete new option (disease-specific canine HS activity; "
        "human intracranial delivery reached all brain tumours) and the only agent "
        "covering the vaccine's immune-escape blind spot -- then DEMOTED: it is "
        "duration-capped by neutralizing antibodies, so it buys pure delay, never "
        "durability.",
        "0.350 -> 0.983 at 3yr but 0.350 -> 0.350 at 8yr; canine HS Igase 2019; "
        "human intracranial Samson 2018.",
    ),
    Therapy(
        "Oncolytic canine distemper virus",
        TherapyClass.ONCOLYTIC_VIRUS,
        "Oncolytic paramyxovirus.",
        Verdict.CONSIDERED_UNMEASURED,
        "Noted as an actively-worked oncolytic approach in canine HS models; not "
        "parameterized.",
    ),

    # --- Innate / local immune adjuvants -----------------------------------
    Therapy(
        "Intracavitary TLR7/8-agonist depot (resiquimod / Ace-DEX scaffold)",
        TherapyClass.INNATE_ADJUVANT,
        "Biodegradable scaffold releasing resiquimod into the resection cavity; "
        "innate stimulus that (claimed) seeds durable systemic memory.",
        Verdict.PROSE_ONLY,
        "The sole candidate for the hardest cell (brain, no findable antigen): "
        "antigen-free AND delivery-free (starts behind the BBB). But it remains "
        "PROSE ONLY -- no kill rate, no durability figure. It escapes only the "
        "priming toll (worsens afferent drainage, route CNS-2; leaves the "
        "exhaustion toll untouched); the re-challenge result shows resisting a fresh "
        "inoculum, not clearing established residual disease; and the untested risk "
        "that HS myeloid tumour cells express TLR7/8 (MyD88->NF-kB survival axis) "
        "could invert its sign. No safety framing (edema/seizure/ICP).",
        "mouse glioma durable clearance 50% (GL261) / 31.6% (CT2A) + contralateral "
        "re-challenge protection; ~7-day release.",
        aliases=("resiquimod",),
    ),
    Therapy(
        "VEGF-C lymphangiogenic adjunct",
        TherapyClass.INNATE_ADJUVANT,
        "mRNA-delivered VEGF-C expands meningeal lymphatics to restore afferent "
        "priming.",
        Verdict.PROSE_ONLY,
        "Real mouse-GBM mechanism (Song et al., Nature 2020) but effectively "
        "dropped: it pairs with anti-PD-1 (not the vaccine, whose afferent limb is "
        "already bypassed) and carries an unresolved metastasis concern for a "
        "disseminating tumour class.",
    ),
    Therapy(
        "STING agonist",
        TherapyClass.INNATE_ADJUVANT,
        "Innate immune agonist of the STING pathway.",
        Verdict.CONSIDERED_UNMEASURED,
        "Enumerated in the broad landscape scan as absent from the modules; never "
        "built or costed.",
    ),

    # --- Autophagy / lysosome ----------------------------------------------
    Therapy(
        "Hydroxychloroquine (HCQ)",
        TherapyClass.AUTOPHAGY,
        "Lysosomotropic autophagy/lysosome inhibitor (persister dependency).",
        Verdict.SUPPORTING,
        "In the current-answer backbone. Chosen over sulfasalazine on evidence "
        "rather than elegance: the ONLY agent anywhere in the project with a canine "
        "phase I -- spontaneous canine lymphoma, 12.5 mg/kg/day tolerated, tumour "
        "concentration ~100x plasma. Human GBM DLT is marrow (600 mg/day MTD). "
        "Numeric canine brain:plasma ratio NOT FOUND.",
        "canine lymphoma phase I ORR 93.3%, tumour:plasma ~100x (PMC4203518).",
        aliases=("HCQ",),
    ),
    Therapy(
        "Chloroquine",
        TherapyClass.AUTOPHAGY,
        "Lysosomotropic autophagy inhibitor.",
        Verdict.CONSIDERED_UNMEASURED,
        "The HCQ analogue with a randomized human GBM trial (Sotelo 2006) and a "
        "2022 meta-analysis; brain:plasma not found. Considered as part of the "
        "autophagy axis.",
    ),

    # --- Ferroptosis --------------------------------------------------------
    Therapy(
        "Sulfasalazine",
        TherapyClass.FERROPTOSIS,
        "System xc-/SLC7A11 inhibitor -> glutathione starvation -> ferroptosis.",
        Verdict.RETRACTED,
        "Briefly the obtainable ferroptosis inducer, then retracted as the "
        "molecule (mechanism survived): a safety claim was wrong -- its canine "
        "dry-eye (KCS) toxicity is PERMANENT, not reversible (Bjerkas 1985) -- and "
        "on the corrected budget the regimen collapsed. Its one glioma monotherapy "
        "trial was terminated (0 responses, 10/10 toxicity) and brain penetration is "
        "~1.26%. BCRP/MRP2 substrate (efflux-limited, in principle rescuable).",
        "brain:plasma ~1.26% (mouse); glioma trial PFS ~1.1mo (PMID 19840379); but "
        "measured tumour GSH depletion in recurrent GBM (PMID 42229231).",
    ),
    Therapy(
        "Statin (lipophilic; lovastatin / simvastatin)",
        TherapyClass.FERROPTOSIS,
        "Mevalonate-pathway block -> impaired GPX4 biosynthesis + CoQ10/FSP1 "
        "depletion (hits GPX4 AND its FSP1 bypass at once).",
        Verdict.SUPERSEDED,
        "The favoured ferroptosis inducer after sulfasalazine collapsed -- cheap, "
        "safe in dogs, brain-penetrant, and mechanistically it closes the invented-"
        "then-confirmed 'ferroptosis-resistance' (FSP1) escape. Belonged to an "
        "intermediate ferroptosis regimen later superseded by the microtubule route.",
    ),
    Therapy(
        "Artesunate / Auranofin / Altretamine / Metformin (ferroptosis-adjacent)",
        TherapyClass.FERROPTOSIS,
        "Miscellaneous ferroptosis inducers (ROS synergy; TXNRD1; weak GPX4; "
        "ATF4/STAT3).",
        Verdict.CONSIDERED_UNMEASURED,
        "Surveyed as obtainable ferroptosis inducers. Altretamine's GPX4 evidence "
        "is weak/secondary; the others are adjuncts. None advanced -- and ferroptosis "
        "has never been studied in canine HS (lineage argument cuts both ways).",
    ),

    # --- OXPHOS / mitochondria (persister metabolism) ----------------------
    Therapy(
        "Metformin",
        TherapyClass.OXPHOS,
        "Weak mitochondrial complex-I inhibitor (persister OXPHOS dependency).",
        Verdict.CONSIDERED_UNMEASURED,
        "Safe in dogs but too low-potency at achievable exposures; an uptake "
        "(OCT-dependent), not efflux, brain-penetration problem, so a P-gp inhibitor "
        "cannot rescue it.",
    ),
    Therapy(
        "Atovaquone",
        TherapyClass.OXPHOS,
        "FDA-approved mitochondrial inhibitor; brain-exposure-optimised formulation.",
        Verdict.CONSIDERED_UNMEASURED,
        "The more interesting obtainable OXPHOS option -- an amorphous-solid-"
        "dispersion formulation raised brain exposure and radiosensitised DIPG in "
        "an orthotopic mouse model (PMID 42192913). Formulation, not transporter, "
        "is the lever.",
    ),
    Therapy(
        "IACS-010759",
        TherapyClass.OXPHOS,
        "Potent mitochondrial complex-I inhibitor.",
        Verdict.REJECTED,
        "Potent but NOT obtainable (investigational only); recalled DLTs "
        "(peripheral neuropathy / lactic acidosis) were unverified this session.",
    ),
    Therapy(
        "Navitoclax (BCL-XL)",
        TherapyClass.OXPHOS,
        "BCL-XL inhibitor; persisters and senescent cells are hypersensitive.",
        Verdict.REJECTED,
        "Obtainable-ish, but its on-target thrombocytopenia stacks badly with "
        "lomustine's myelosuppression.",
    ),

    # --- NF-kB inhibition ---------------------------------------------------
    Therapy(
        "Parthenolide / DMAPT",
        TherapyClass.NFKB_INHIBITOR,
        "NF-kB inhibitor + glutathione depleter/ROS inducer; small molecule, "
        "non-division-gated (reaches persisters), efflux-rescuable.",
        Verdict.SUPERSEDED,
        "The agent with the STRONGEST species+disease evidence in the project: it "
        "kills canine HS cell lines AND primary cells via GSH depletion/ROS with "
        "NF-kB genes down, and extends survival in a disseminated canine HS mouse "
        "model. NF-kB is exactly the axis Sakuma found stratifies HS subgroups. GI "
        "DLT (an independent organ axis). Central to an intermediate regimen, later "
        "superseded by the microtubule route. (A toxicity-lookup bug that let it "
        "fail-open was caught and fixed.)",
        "kills canine HS lines + primary cells, PMID 38135509.",
        aliases=("DMAPT",),
    ),

    # --- Macrophage-lineage depletion --------------------------------------
    Therapy(
        "Liposomal clodronate",
        TherapyClass.LINEAGE_DEPLETION,
        "Phagocytic-suicide depletion of the macrophage lineage; non-antigen, "
        "non-division-gated.",
        Verdict.SUPPORTING,
        "In the current-answer backbone. The only agent simultaneously lineage-"
        "directed, antigen-independent, non-division-gated, obtainable today, AND "
        "already observed to work in the right species+disease (2/5 dogs with HS "
        "responded). Access is compartment-specific: a liposome does not cross an "
        "intact BBB but depletes blood-side perivascular/meningeal macrophages. Its "
        "kill rate has NEVER been measured in any species -- named the single most "
        "decision-relevant experiment in the project.",
        "responses in 2/5 dogs with HS (PMID 19760220); assumed 0.06/day (0.20/day "
        "would close the leptomeningeal compartment).",
    ),

    # --- MGMT-directed ------------------------------------------------------
    Therapy(
        "O6-benzylguanine",
        TherapyClass.MGMT_DIRECTED,
        "Direct MGMT inhibitor/depleter (restores O6-alkylator lethality).",
        Verdict.REJECTED,
        "Genuinely works on mechanism, but rejected on toxicity: its entire DLT is "
        "bone marrow, which was already pinned at 1.00, so adding it drives marrow "
        "to 1.85.",
        aliases=("O6-BG",),
    ),
    Therapy(
        "Dose-dense temozolomide scheduling (MGMT depletion)",
        TherapyClass.MGMT_DIRECTED,
        "Continuous/dose-dense TMZ to exhaust MGMT (consumed one molecule per repair).",
        Verdict.REJECTED,
        "The 'free rescue' (continuous dosing already assumed) -- but the best trial "
        "designed to find exactly this benefit found none.",
        "RTOG 0525: 16.6 vs 14.9 months, p=0.63, at worse toxicity.",
    ),

    # --- Delivery adjuncts / routes ----------------------------------------
    Therapy(
        "Intra-arterial + osmotic BBB disruption (Neuwelt)",
        TherapyClass.DELIVERY_ADJUNCT,
        "Arterial catheter + mannitol osmotic opening to boost drug brain access.",
        Verdict.RETRACTED,
        "The core RETRACTION of the IA regimen: a ~3.7x access boost delivered by a "
        "MONTHLY surgical procedure cannot be multiplied by a continuous (duty 1.0) "
        "presence -- two schedules that exclude each other. Osmotic disruption does "
        "genuinely raise drug levels in dogs; what was lost was the right to combine "
        "it with continuous dosing.",
        "assumed access 0.73 = intrinsic 0.20 x 3.7 boost -- the falsified product.",
    ),
    Therapy(
        "Focused ultrasound (FUS) BBB opening",
        TherapyClass.DELIVERY_ADJUNCT,
        "Non-invasive, transient BBB opening; a multiplier on a persistent oral drug.",
        Verdict.SUPERSEDED,
        "Structurally attractive (crosses a this breed-weight dog skull without incision; "
        "multiplies a mechanism that already persists, so it escapes the duration "
        "cap). Paired with AT9283 in an intermediate 'closes all four cells' claim, "
        "later superseded. Caveat: episodic sessions vs. a time-averaged margin -- "
        "the average sits near baseline, and it cannot lift trametinib far enough "
        "alone.",
    ),
    Therapy(
        "Intrathecal / intraventricular dosing",
        TherapyClass.DELIVERY_ADJUNCT,
        "Drug placed directly into CSF (bypasses the BBB) for fluid-borne/"
        "leptomeningeal disease.",
        Verdict.RETRACTED,
        "The fluid-compartment rate-control arm. Its headline '470x margin with room "
        "to spare' was AUDITED and retracted -- an absolute nM comparison against a "
        "placeholder CDK4/6i concentration; the scale-free version was the only valid "
        "one. No ERK/PI3K inhibitor has been given intrathecally in any species; "
        "repeated intrathecal dosing collides with the this breed SOD1/degenerative-"
        "myelopathy predisposition and with marrow (cytarabine + craniospinal RT).",
    ),
    Therapy(
        "Convection-enhanced delivery / catheter-reservoir / Gliadel wafer",
        TherapyClass.DELIVERY_ADJUNCT,
        "Chronic local intratumoral drug delivery bypassing the BBB.",
        Verdict.CONSIDERED_UNMEASURED,
        "Proposed as a structural closer (removes the whole pharmacokinetic axis) "
        "for the brain drug-only cell; a named delivery path rather than a computed "
        "result.",
    ),
    Therapy(
        "Efflux-inhibitor co-dose (P-gp/BCRP; elacridar)",
        TherapyClass.DELIVERY_ADJUNCT,
        "P-gp/BCRP inhibitor co-dosed to rescue efflux-limited (not size-excluded) "
        "brain penetration.",
        Verdict.SUPERSEDED,
        "Rescues efflux-limited small molecules (sulfasalazine, parthenolide). But it "
        "is not brain-selective, so it also raises systemic sulfasalazine exposure "
        "(ocular axis to 1.38, forcing a dose cut). This reversed the earlier "
        "'efflux inhibition is the right answer to the wrong question' verdict once "
        "the parthenolide catalogue gap was found. Herding-breed ABCB1-1delta status "
        "is a natural P-gp-inhibited state to check.",
        aliases=("elacridar",),
    ),

    # --- Local modalities ---------------------------------------------------
    Therapy(
        "Surgery / debulking",
        TherapyClass.LOCAL_MODALITY,
        "Maximal resection (assumed before any drug or immune component acts).",
        Verdict.SUPPORTING,
        "Credited in every computed number (DEBULKING_FRACTION = 0.97) and it makes "
        "the intracavitary depot placeable. But it delays regrowth without changing "
        "any clone's growth RATE, so it buys no durable benefit alone -- durability "
        "is a rate question, not a size question.",
        "location-matched reality: 43-day median (Toyoda 2020, n=102).",
    ),
    Therapy(
        "Radiation (focal / craniospinal)",
        TherapyClass.LOCAL_MODALITY,
        "Radiotherapy for cytoreduction / craniospinal coverage.",
        Verdict.SUPPORTING,
        "A coverage/debulking component in several intermediate regimens (a CNS-local "
        "toxicity axis; duty-limited over a 21-day course, so it misses late "
        "persister re-entry). Craniospinal irradiation stacks on marrow with "
        "intrathecal cytarabine.",
    ),

)


# ---------------------------------------------------------------------------
# GROUPING HELPERS
# ---------------------------------------------------------------------------

def by_class() -> dict[TherapyClass, tuple[Therapy, ...]]:
    """Return the catalogue grouped by therapy class (insertion order preserved)."""
    grouped: dict[TherapyClass, list[Therapy]] = {}
    for t in THERAPIES:
        grouped.setdefault(t.therapy_class, []).append(t)
    return {cls: tuple(items) for cls, items in grouped.items()}


def by_verdict() -> dict[Verdict, tuple[Therapy, ...]]:
    """Return the catalogue grouped by the verdict we reached."""
    grouped: dict[Verdict, list[Therapy]] = {}
    for t in THERAPIES:
        grouped.setdefault(t.verdict, []).append(t)
    return {v: tuple(items) for v, items in grouped.items()}


def current_answer() -> tuple[Therapy, ...]:
    """The therapies that are in / support the live ('current answer') regimen."""
    live = {Verdict.IN_CURRENT_ANSWER, Verdict.SUPPORTING, Verdict.MAINTENANCE_TIER}
    return tuple(t for t in THERAPIES if t.verdict in live)


def find(name_fragment: str) -> tuple[Therapy, ...]:
    """Case-insensitive lookup across names and aliases."""
    frag = name_fragment.lower()
    hits = []
    for t in THERAPIES:
        haystack = " ".join((t.name, *t.aliases)).lower()
        if frag in haystack:
            hits.append(t)
    return tuple(hits)


# The live regimen, stated plainly (see module docstring for the full frame).
CURRENT_ANSWER_REGIMEN = {
    "induction": (
        "liposomal clodronate",
        "hydroxychloroquine",
        "anti-PD-1 (gilvetmab)",
        "paxalisib",
        "lisavanbulin",
        "PRMT5 inhibitor",
    ),
    "maintenance": ("PRMT5 inhibitor (alone, indefinitely)",),
    "load_bearing": "lisavanbulin (the microtubule agent) -- the others widen margins",
    "curative": False,
    "genotype_tiered_maintenance": {
        "MAPK-driven (~59%, PTPN11/SHP2, KRAS)": "MEK inhibitor (mirdametinib), site-split",
        "CDKN2A-deleted": "abemaciclib",
        "MTAP-deleted": "PRMT5 inhibitor (synthetic lethality)",
    },
}


if __name__ == "__main__":  # pragma: no cover - quick manual summary
    groups = by_class()
    print(f"{len(THERAPIES)} therapies across {len(groups)} classes\n")
    for cls, items in groups.items():
        print(f"[{cls.name}]  ({len(items)})")
        for t in items:
            print(f"  - {t.name}: {t.verdict.value}")
        print()
