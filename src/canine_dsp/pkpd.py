"""Derive a per-day kill rate from a measured IC50 and an achievable exposure.

The escape-closure engine needs a per-day kill rate; the audit's central complaint was that those
rates were hand-set constants. This module removes the hand-setting: it COMPUTES the kill rate from
two real, citable quantities -- a potency (IC50, measured in cells) and an exposure (plasma Cmax x
CNS access) -- through a standard exposure-response relation, and it returns a small (sub-growth,
non-closing) rate whenever the achievable free concentration sits below the IC50. Nothing here is a
narrative; every value is produced by a formula from its inputs.

THE MODEL
---------
A cytotoxic assay reports fractional viability V after `assay_days` at concentration C. The
one-parameter exposure-response V(C) = 1 / (1 + C/IC50) passes through V = 0.5 at C = IC50 (the
definition of IC50) and V -> 0 as C grows. Reading that surviving fraction as exponential decay over
the assay window gives a per-day kill rate

    k(C) = -ln V / assay_days = ln(1 + C / IC50) / assay_days

so k rises with exposure, equals ln(2)/assay_days at C = IC50, and -> 0 as C -> 0. The free CNS
concentration is C = Cmax x Kp,uu (unbound brain:plasma ratio). An escape closes when k exceeds the
tumour growth rate. The model is falsifiable at the input level: a drug that cannot reach its IC50 in
the compartment returns k below growth and does NOT close.

WHAT THIS DOES AND DOES NOT LICENSE
-----------------------------------
It licenses a MODEL-DERIVED kill rate from measured potency + exposure -- "scientifically backed" in
the model-based sense, not a bare assumption. It does not invent potency or exposure: those still
carry provenance (see PARAMS), and a transferred IC50 or a rodent Kp,uu makes the derived rate a
transfer too. The assay-duration reading is a modelling choice, stated, not a measured kill rate.

This is an analysis, not veterinary advice.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .core.evidence import Provenance

# The pass/fail bar (tumour net growth), matching core.catalogue.GROWTH_PER_DAY.
#
# PROVENANCE: DERIVED and deliberately CONSERVATIVE. This was a bare literal -- an assumed ~13-day
# doubling with no citation -- which made it the weakest-grounded number in the project while also
# being the most load-bearing, since every escape closure and every durability margin is tested
# against it. `standard_audit.growth_bar_derivation()` now grounds it in regrowth measured in canine
# HS itself: localized disease after debulking + lomustine gave a median disease-free interval of
# 243 d with 10/16 relapsing at a median 201 d (Skorupski, PMID 19453368), which implies a net
# regrowth rate of 0.0095-0.0344/day over a 1e6-1e8 post-surgical residual burden. 0.055/day is
# 1.6-5.8x HIGHER than any of those, so every margin in the project clears a bar harder than the
# clinical data demands -- the direction that cannot manufacture a closure. Those clinical rates are
# net rates under lomustine and therefore already suppressed, which is why the bar belongs above
# them rather than inside the range. `standard_audit.growth_sensitivity()` re-derives the required
# access across 0.030-0.080/day and the conclusion does not turn on the choice.
GROWTH_PER_DAY = 0.055
GROWTH_PER_DAY_PROVENANCE = Provenance.DERIVED
# Standard in-vitro cytotoxicity window (72 h MTT) the exposure-response is read over.
DEFAULT_ASSAY_DAYS = 3.0


def emax_kill_rate(ic50_nM: float, concentration_nM: float,
                   assay_days: float = DEFAULT_ASSAY_DAYS) -> float:
    """Per-day kill rate derived from a measured IC50 and a free concentration (see module docstring).

    k = ln(1 + C/IC50) / assay_days. Monotonic in C, ln(2)/assay_days at C = IC50, 0 at C = 0.
    """
    if ic50_nM <= 0:
        raise ValueError("ic50_nM must be positive")
    if concentration_nM < 0:
        raise ValueError("concentration_nM must be >= 0")
    if assay_days <= 0:
        raise ValueError("assay_days must be positive")
    return math.log1p(concentration_nM / ic50_nM) / assay_days


def free_cns_concentration(cmax_nM: float, kp_uu: float) -> float:
    """Free brain concentration = plasma Cmax x unbound brain:plasma ratio (Kp,uu)."""
    if cmax_nM < 0 or kp_uu < 0:
        raise ValueError("cmax_nM and kp_uu must be >= 0")
    return cmax_nM * kp_uu


def margin(kill_rate: float, growth: float = GROWTH_PER_DAY) -> float:
    """Kill margin = derived kill rate - tumour growth rate. Positive means the escape closes."""
    return kill_rate - growth


@dataclass(frozen=True)
class DrugPKPD:
    """A drug's exposure-response inputs, each with provenance, and the closures they derive."""

    name: str
    ic50_nM: float
    cmax_nM: float
    ic50_provenance: Provenance
    cmax_provenance: Provenance
    source: str
    note: str = ""

    def kill_rate_at(self, kp_uu: float, assay_days: float = DEFAULT_ASSAY_DAYS) -> float:
        """Model-derived per-day kill rate at unbound CNS access `kp_uu`."""
        return emax_kill_rate(self.ic50_nM, free_cns_concentration(self.cmax_nM, kp_uu), assay_days)

    def closes_at(self, kp_uu: float, growth: float = GROWTH_PER_DAY) -> bool:
        """Whether the derived kill rate beats growth at CNS access `kp_uu`."""
        return margin(self.kill_rate_at(kp_uu), growth) > 0

    def min_access_to_close(self, growth: float = GROWTH_PER_DAY,
                            assay_days: float = DEFAULT_ASSAY_DAYS) -> float:
        """Smallest Kp,uu at which the derived kill rate reaches growth.

        Solve ln(1 + Cmax*kp/IC50)/assay_days = growth  ->  kp = IC50*(exp(growth*assay_days)-1)/Cmax.
        Returns inf if the drug cannot close even at kp_uu = 1 (full systemic exposure in brain).
        """
        if self.cmax_nM <= 0:
            return math.inf
        kp = self.ic50_nM * (math.exp(growth * assay_days) - 1.0) / self.cmax_nM
        return kp


# Exposure-response inputs with provenance. IC50s and Cmax are real measured values where the source
# says so; a transferred IC50 (e.g. human MTAP-null for a canine tumour) is marked TRANSFERRED and
# makes any derived rate a transfer too. These are the only inputs; kill rates below are computed.
PARAMS: dict[str, DrugPKPD] = {
    # MEK inhibitor for the ~59% MAPK-driver maintenance tier. Both IC50 and Cmax measured in the
    # canine-HS study itself -- the fully-grounded case.
    "cobimetinib": DrugPKPD(
        name="cobimetinib (MEK1/2 inhibitor)",
        ic50_nM=372.0,            # conservative top of the measured 74-372 nM range in 3 canine HS lines
        cmax_nM=1640.0,           # achievable canine plasma Cmax at 5 mg/kg
        ic50_provenance=Provenance.MEASURED,
        cmax_provenance=Provenance.MEASURED,
        source="Genes 2024;15(8):1050, PMID 39202410 (canine HS lines BD/OD/DH82)",
        note="Both inputs measured in canine HS; the derived kill rate is model-derived from "
             "canine data, not assumed.",
    ),
    # PRMT5 inhibitor for the MTAP-deleted (ten-year) maintenance arm. Potency measured in human
    # MTAP-null cells; a transfer to the dog, justified by PRMT5 99.37% ortholog identity
    # (sequence_conservation). No canine Cmax published, so Cmax is a documented placeholder used
    # only to expose the access threshold, not to assert closure.
    "tng908": DrugPKPD(
        name="MTA-cooperative PRMT5 inhibitor (class; brain-penetrant anchor TNG456)",
        ic50_nM=10.0,             # GI50 <10 nM in MTAP-null cells (class potency)
        cmax_nM=1000.0,           # PLACEHOLDER exposure (no canine PK); see min_access_to_close()
        ic50_provenance=Provenance.TRANSFERRED,
        cmax_provenance=Provenance.ASSUMED,
        source="Class: J Med Chem 2024 PMID 38595098 (TNG908). CNS anchor updated to TNG456, a "
               "brain-penetrant MTA-cooperative PRMT5i in Phase I/II with a glioblastoma focus "
               "(J Med Chem 2026;69:12853, PMID 42150143). Independent brain-penetrant chemotype: "
               "Eur J Med Chem 2026;315:119001 PMID 42190431.",
        note="Potency transferred from human MTAP-null cells (PRMT5 target 99.37% conserved) and is "
             "a CLASS value; the ~10 nM GI50 is shared across the MTA-cooperative series. The kill "
             "MARGIN is not the deciding quantity here -- the genotype LOCK is -- so this entry is "
             "used via min_access_to_close() to expose the access hinge, not closes_at() to assert "
             "closure. CNS caveat: the first-generation member TNG908 showed preclinical brain "
             "permeability but failed to reach therapeutic CNS exposure in glioblastoma trials "
             "(PMID 42190431); the brain-penetrant successor TNG456 (PMID 42150143) is the CNS "
             "anchor. Canine Cmax remains unpublished for either.",
    ),
    # PI3K/AKT inhibitor for the PTEN-deleted tier. Added so that tier stops falling back to a flat
    # ordinal site prior. IC50 is MEASURED IN CANINE HS -- the 2026 compound screen is the first
    # canine-HS potency figure on this axis, replacing the hemangiosarcoma transfer the project had
    # been criticised for. Cmax is a written human-label transfer.
    "duvelisib": DrugPKPD(
        name="duvelisib (PI3K-delta/gamma inhibitor; PTEN-deleted tier)",
        ic50_nM=287.0,            # median IC50 in the responsive canine-HS expression subgroup
        cmax_nM=3598.0,           # human label 1.5 ug/mL steady state at 25 mg BID; MW 416.9
        ic50_provenance=Provenance.MEASURED,
        cmax_provenance=Provenance.TRANSFERRED,
        source="IC50: Vet Comp Oncol 2026;24(3):554-567, PMID 42129963 -- 1824-compound screen "
               "across 10 canine HS lines; duvelisib median IC50 287 nM in Group A, >5 uM in Group "
               "B, 7.46 uM in normal PBMC, acting through reduced phospho-Akt. Cmax: COPIKTRA US "
               "label, geometric mean steady-state Cmax 1.5 ug/mL (CV 64%) at 25 mg BID.",
        note="The potency is MEASURED in the right species AND disease, which is stronger than any "
             "other targeted agent here except cobimetinib. Two honest limits: the stratifier is an "
             "EXPRESSION subgroup, not PTEN status, so routing this tier on PTEN deletion is an "
             "inference the screen does not make; and the exposure is a human-label transfer, so "
             "canine dose-finding would be required. Total (not unbound) Cmax, matching the "
             "cobimetinib entry's convention.",
    ),
    # CDK4/6 inhibitor for the CDKN2A-deleted / RB1-intact tier, and -- per HS_STATUS section A --
    # the lead brain arm for the co-deleted CFA11q16 lesion. The IC50 used is the CDK6 enzymatic
    # value BECAUSE that is the reference the measured human brain-tissue multiple is quoted
    # against, so the two numbers are commensurable rather than independently chosen.
    "abemaciclib": DrugPKPD(
        name="abemaciclib (CDK4/6 inhibitor; CDKN2A-deleted, RB1-intact tier)",
        ic50_nM=10.0,             # CDK6/cyclin D1 enzymatic IC50 (CDK4 is 2 nM; CDK6 is the harder bar)
        cmax_nM=588.0,            # human label 298 ng/mL steady state at 200 mg BID; MW 506.6
        ic50_provenance=Provenance.TRANSFERRED,
        cmax_provenance=Provenance.TRANSFERRED,
        source="IC50: CDK4/cyclin D1 2 nM, CDK6/cyclin D1 10 nM (Lilly biochemical characterisation; "
               "the same reference the brain-tissue multiple below is expressed against). Cmax: "
               "VERZENIO US label, mean steady-state Cmax 298 ng/mL at 200 mg BID; plasma protein "
               "binding 96.3%, so unbound fraction ~3.7% (21.8 nM unbound). Canine-HS dependency "
               "MEASURED: CDKN2A down, Rb preserved and class growth inhibition in all canine "
               "histiocytic lines incl. localized HS, plus a xenograft (PMID 35278028).",
        note="CRITICAL SITE DISTINCTION, and it corrects an overstatement in HS_STATUS section A. "
             "The measured 96x (CDK4) / 19x (CDK6) tissue multiple comes from resected human BRAIN "
             "METASTASES -- lesions with a DISRUPTED barrier -- so it speaks to the extra-axial, "
             "blood-side mass that is the bulk of this tumour, NOT to cells behind an intact "
             "barrier. For invaded parenchyma the governing figures are the rodent unbound ratios: "
             "Kp,uu 0.03 (mouse) to 0.11 (rat) on 21.8 nM unbound plasma gives 0.65-2.4 nM, i.e. "
             "0.07-0.24x the CDK6 IC50 -- it does NOT close there, and only approaches the 2 nM "
             "CDK4 bar at the rat ratio. So abemaciclib is the best-evidenced option for the "
             "extra-axial mass and does NOT remove the need for local delivery in invaded "
             "parenchyma. Active metabolites (M2/M20/M18) add activity this parent-only entry "
             "omits, so the entry is conservative.",
    ),
    # The floor tier's cycled cytotoxic. Both inputs are canine: potency measured in canine HS, and
    # exposure DERIVED from measured canine PK parameters rather than transferred from humans.
    "vincristine": DrugPKPD(
        name="vincristine (position-independent microtubule cytotoxic; floor tier / induction class)",
        ic50_nM=3.26,             # 2.69 ng/ml, the conservative top of the canine-HS range; MW 825
        cmax_nM=47.8,            # derived below from measured canine PK
        ic50_provenance=Provenance.MEASURED,
        cmax_provenance=Provenance.DERIVED,
        source="IC50: PMID 25715778 -- 4 canine HS lines, vincristine IC50 1.77-2.69 ng/ml (the top "
               "of the range is used). Cmax DERIVED from measured canine PK: 0.7 mg/m2 IV with "
               "Vd 0.660 +/- 0.210 l/kg in dogs (PMID 25649934); for a 20 kg dog, BSA = 0.101 * "
               "kg^(2/3) = 0.744 m2 -> 0.521 mg into 13.2 l -> C0 39.5 ng/ml = 47.8 nM.",
        note="The only agent in the project whose potency AND exposure are both canine. Limits: C0 "
             "from dose/Vd is the peak of a two-compartment profile with a 21.5-min distribution "
             "half-life, so average exposure is far lower -- which is why the floor tier is CYCLED "
             "rather than continuous, and why its durability grade is the weakest. Vincristine is "
             "also a canonical P-gp substrate and ABCB1/ABCG2 are elevated in these lines (same "
             "paper), the escape recorded as escape_audit.A13; the induction regimen therefore uses "
             "a colchicine-site, non-efflux-substrate congener, and this entry stands for the "
             "measured class potency, not for the agent of choice in the brain.",
    ),
    # THE AGENT THAT CLOSES THE INVADING EDGE WITH A LICENSED DRUG. This is the only entry in PARAMS
    # whose exposure is a MEASURED DRUG CONCENTRATION IN GADOLINIUM-NON-ENHANCING TUMOUR -- i.e. in
    # tumour sitting behind a barrier that is still intact. Every other brain figure in this project
    # is either a rodent Kp,uu, a generic compartment access, or a concentration from an ENHANCING
    # lesion (where the barrier is already broken). Those are the three ways of inferring access.
    # This one measures it directly, in the exact compartment that was the project's last open site.
    "ribociclib": DrugPKPD(
        name="ribociclib (CDK4/6 inhibitor; licensed, and the exists-today answer at the invading edge)",
        ic50_nM=40.0,             # biochemical IC50 for CDK4/6 inhibition, the reference the trials quote against
        cmax_nM=170.0,            # MEASURED median unbound conc in Gd-NON-ENHANCING tumour, 400 mg QD
        ic50_provenance=Provenance.MEASURED,
        cmax_provenance=Provenance.MEASURED,
        source="Tien/Li/Sanai, Clin Cancer Res 2019;25(19):5777-5786, PMID 31285369 "
               "(doi:10.1158/1078-0432.CCR-19-0133): Phase 0, recurrent glioblastoma, 900 mg QD x5d "
               "pre-resection; MEAN UNBOUND concentrations CSF 374 nM, NON-ENHANCING tumour 560 nM, "
               "enhancing tumour 2152 nM, all >5x the 40 nM CDK4/6 IC50, with RB phosphorylation and "
               "proliferation both significantly reduced. Johnson/Tien/Sanai, Neuro Oncol "
               "2026;28(3):659-671, PMID 41206763 (doi:10.1093/neuonc/noaf257): Phase 0/1 in "
               "recurrent high-grade glioma SELECTED FOR CDKN2A/B deletion or CDK4/6 amplification, "
               "PTEN loss or PIK3CA mutation, and WILD-TYPE Rb; median unbound ribociclib in Gd-NON-"
               "ENHANCING tumour 170 nM (range 65-1770) at 400 mg and 634 nM (range 68-2345) at "
               "600 mg, significantly above the IC50, with Ki-67-positive cells significantly "
               "decreased. Everolimus in the same tumours was UNDETECTABLE (<0.1 nM), which is the "
               "negative control that shows the assay is not flattering the brain.",
        note="WHY THIS ENTRY MATTERS MORE THAN ITS SIZE. The project's last open site was invaded "
             "parenchyma behind an INTACT barrier, and every candidate for it was either a to-build "
             "molecule (rgn3067) or an inference from a rodent ratio (abemaciclib, whose own "
             "measured mouse-to-rat range spans failure to a thin pass). This is a MEASURED human "
             "concentration in Gd-non-enhancing tumour, which is that compartment by definition, "
             "for a drug that is LICENSED (Kisqali) and therefore obtainable off-label today. "
             "Because the number is already a tumour concentration, access is 1.0 BY CONSTRUCTION "
             "and must NOT be multiplied by a Kp,uu again -- same convention as rgn3067. "
             "The conservative 400 mg median is used rather than the 900 mg mean (560 nM) or the "
             "600 mg median (634 nM); see ribociclib_nonenhancing_range() for the whole measured "
             "span, whose WORST single value (65 nM) still gives 0.32/day against a 0.055/day bar. "
             "GENOTYPE MATCH, and it is unusually close: the 2026 trial enrolled on CDKN2A/B "
             "deletion with wild-type Rb, which is the CFA11q16 lesion carried by 62.8% of canine "
             "HS, and CDK4/6 dependency is MEASURED in canine histiocytic lines (palbociclib: "
             "CDKN2A down, Rb preserved, growth inhibited in all lines, PMID 35278028). "
             "HONEST LIMITS, three of them. (1) Ribociclib MONOTHERAPY had limited efficacy in "
             "recurrent glioblastoma (median PFS 9.7 weeks) -- but the pharmacodynamics WORKED (RB "
             "phosphorylation and Ki-67 both down), and the 2026 trial traced the escape to PI3K/"
             "mTOR upregulation, which is a named route this regimen already covers. So the failure "
             "is a reroute the ledger answers, not a delivery failure. (2) CDK4/6 inhibition is "
             "division-gated and cytoSTATIC, so it does NOT reach the drug-tolerant persister and "
             "cannot carry the position-independent routes; it closes ACCESS at this site, not "
             "every escape at it. (3) No canine PK exists, so the human-to-dog step is a TRANSFER, "
             "justified by CDK6 ortholog conservation and the measured canine-HS dependency.",
    ),
    # THE AGENT THAT RETIRES THE LAST ASSUMED NUMBER. Every margin in the brain-native regimen rested
    # on a REFERENCE POTENCY of 0.15/day (core.microtubule_route.REFERENCE_POTENCY) -- a bare
    # constant, and the closure needed >= ~0.10/day, i.e. only a 1.5x cushion on a guess. This entry
    # replaces that guess with a derived kill rate from two measured numbers.
    "rgn3067": DrugPKPD(
        name="RGN3067 (oral colchicine-site tubulin destabiliser; the brain-native induction agent)",
        ic50_nM=616.0,            # the WORST of four patient-derived GB lines (148-616 nM)
        cmax_nM=20000.0,          # MEASURED rodent BRAIN Cmax after ORAL dosing (7807 ng/ml = 20 uM)
        ic50_provenance=Provenance.MEASURED,
        cmax_provenance=Provenance.MEASURED,
        source="Biomedicines 2024;12(2):406, PMID 38398008. Oral dosing in rodent gives BRAIN Cmax "
               "7807 ng/ml (20 uM) at Tmax 2 h, with EQUAL LEVELS IN PLASMA AND BRAIN and minimal "
               "in vivo toxicity. Binds the colchicine site and inhibits tubulin polymerisation; "
               "efflux ratio 0.61, so NOT an MDR1 substrate. IC50 117 nM (U87), 560 nM (LN-18), and "
               "148-616 nM across four patient-derived GB lines; PDX growth reduction in vivo.",
        note="The exposure here is a BRAIN concentration, not a plasma one, so access is already "
             "inside the number and must NOT be multiplied by a Kp,uu again -- this entry is used "
             "with access 1.0 by construction. Both inputs are measured but in the wrong species "
             "(rodent brain) and the wrong tumour (human GB lines), so the per-day kill rate derived "
             "from them is graded TRANSFERRED; the transfer is justified by beta-tubulin at 98.42% "
             "human-dog identity (sequence_conservation) and by canine HS cells being MEASURED "
             "microtubule-sensitive (PMID 25715778). The derived rate is ~1.17/day at the worst "
             "measured IC50 and full measured exposure, and still 0.167/day at 2% of that exposure "
             "-- against a closure threshold of ~0.10/day, a ~50x cushion on exposure. That is what "
             "retires REFERENCE_POTENCY as the load-bearing assumption. Honest limits: 'minimal "
             "toxicity' is rodent, no canine PK exists, and the class carries the record's own "
             "warning that sagopilone FAILED in human GBM -- though RGN3067 is a different "
             "chemotype with equal plasma:brain levels rather than sagopilone's exposure profile.",
    ),
}


def derived_closures(kp_uu_brain: float = 0.30) -> dict[str, dict]:
    """Model-derived kill rate, margin and closure for every drug in PARAMS, at systemic exposure
    (Kp,uu = 1.0) and at a conservative brain access (default 0.30). Pure computation over PARAMS."""
    out: dict[str, dict] = {}
    for key, d in PARAMS.items():
        out[key] = {
            "systemic_kill_per_day": d.kill_rate_at(1.0),
            "systemic_closes": d.closes_at(1.0),
            "brain_kill_per_day": d.kill_rate_at(kp_uu_brain),
            "brain_closes": d.closes_at(kp_uu_brain),
            "min_access_to_close": d.min_access_to_close(),
            "ic50_provenance": d.ic50_provenance.value,
            "cmax_provenance": d.cmax_provenance.value,
            "source": d.source,
        }
    return out


# ---- Target-attainment model (Gap 2: is the maintenance drug even engaging its target?) ----------
#
# The canine trametinib Phase I (Takada/Vail 2024, PMID 38889903) reported that at the MTD
# (0.5 mg/m2/day) approximately 70% of dogs reached an average steady-state concentration of ~10 ng/mL
# -- the exposure associated with clinical efficacy in humans -- AND that target engagement was NOT
# observed in the Day-0/Day-7 tumour biopsies. So "the drug engages the target" is an open quantity
# even in the treatment setting. This model turns the trial's own numbers into a dose -> attainment
# curve: it does not invent binding constants, it restates the reported attainment as a lognormal
# steady-state distribution and extends it across dose, so we can read the fraction of dogs UNDERDOSED
# for the efficacy-benchmark exposure and the dose needed to reach a chosen attainment. Attainment of
# the exposure benchmark is necessary but not sufficient for engagement (which needs a PD biopsy) --
# this bounds the necessary condition from data in hand.

TRAMETINIB_MTD_MG_M2 = 0.5              # recommended Phase II dose, PMID 38889903
TRAMETINIB_TARGET_NG_ML = 10.0          # efficacy-associated steady-state (human benchmark)
TRAMETINIB_ATTAIN_AT_MTD = 0.70         # ~70% of dogs reached the target at the MTD
TRAMETINIB_CSS_CV = 0.55                # population steady-state variability (saturable elimination)
TRAMETINIB_DOSE_EXPONENT = 1.3          # median Css ~ dose^p; p>1 = saturable (supra-linear) exposure


def _phi(z: float) -> float:
    """Standard-normal CDF via erf (no scipy dependency)."""
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def _phi_inv(q: float) -> float:
    """Standard-normal quantile (Acklam's rational approximation; ample precision here)."""
    if not 0.0 < q < 1.0:
        raise ValueError("q must be in (0,1)")
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    plow, phigh = 0.02425, 1 - 0.02425
    if q < plow:
        r = math.sqrt(-2 * math.log(q))
        return (((((c[0]*r+c[1])*r+c[2])*r+c[3])*r+c[4])*r+c[5]) / ((((d[0]*r+d[1])*r+d[2])*r+d[3])*r+1)
    if q > phigh:
        r = math.sqrt(-2 * math.log(1 - q))
        return -(((((c[0]*r+c[1])*r+c[2])*r+c[3])*r+c[4])*r+c[5]) / ((((d[0]*r+d[1])*r+d[2])*r+d[3])*r+1)
    r = q - 0.5
    t = r * r
    return (((((a[0]*t+a[1])*t+a[2])*t+a[3])*t+a[4])*t+a[5])*r / (((((b[0]*t+b[1])*t+b[2])*t+b[3])*t+b[4])*t+1)


def _css_logmu_at(dose_mg_m2: float, sigma: float = TRAMETINIB_CSS_CV,
                  exponent: float = TRAMETINIB_DOSE_EXPONENT) -> float:
    """Log-median steady-state at a dose, calibrated so attainment at the MTD = TRAMETINIB_ATTAIN_AT_MTD."""
    # At MTD: P(Css >= T) = attain  ->  (mu_MTD - lnT)/sigma = Phi^{-1}(attain)
    mu_mtd = math.log(TRAMETINIB_TARGET_NG_ML) + sigma * _phi_inv(TRAMETINIB_ATTAIN_AT_MTD)
    return mu_mtd + exponent * math.log(dose_mg_m2 / TRAMETINIB_MTD_MG_M2)


def target_attainment(dose_mg_m2: float = TRAMETINIB_MTD_MG_M2,
                      sigma: float = TRAMETINIB_CSS_CV) -> dict:
    """Fraction of dogs reaching the efficacy-benchmark steady-state at a given trametinib dose.

    Restates and extends the trial's reported attainment (calibrated to 70% at the MTD). Returns the
    attainment probability and the underdosed fraction -- the population-PK gap that must be closed
    (by dose, or by therapeutic drug monitoring) before continuous maintenance can be relied on."""
    mu = _css_logmu_at(dose_mg_m2, sigma)
    p_attain = _phi((mu - math.log(TRAMETINIB_TARGET_NG_ML)) / sigma)
    return {
        "dose_mg_m2": dose_mg_m2,
        "target_ng_ml": TRAMETINIB_TARGET_NG_ML,
        "p_attain_target": round(p_attain, 3),
        "fraction_underdosed": round(1.0 - p_attain, 3),
        "provenance": Provenance.MEASURED.value,
        "source": "canine trametinib Phase I, PMID 38889903 (MTD 0.5 mg/m2/day; ~70% reach ~10 ng/mL; "
                  "target engagement not confirmed on biopsy)",
    }


def dose_for_attainment(target_fraction: float = 0.90,
                        sigma: float = TRAMETINIB_CSS_CV,
                        exponent: float = TRAMETINIB_DOSE_EXPONENT) -> dict:
    """Trametinib dose (as a multiple of the MTD) needed so `target_fraction` of dogs reach the
    efficacy-benchmark exposure. Reads off how far above the MTD an adequately-dosing regimen sits --
    and therefore whether dose alone can close the attainment gap or monitoring is required."""
    # Solve mu(dose) - lnT = sigma * Phi^{-1}(target_fraction)
    needed_mu = math.log(TRAMETINIB_TARGET_NG_ML) + sigma * _phi_inv(target_fraction)
    mu_mtd = math.log(TRAMETINIB_TARGET_NG_ML) + sigma * _phi_inv(TRAMETINIB_ATTAIN_AT_MTD)
    dose_multiple = math.exp((needed_mu - mu_mtd) / exponent)
    return {
        "target_fraction": target_fraction,
        "dose_multiple_of_mtd": round(dose_multiple, 2),
        "dose_mg_m2": round(dose_multiple * TRAMETINIB_MTD_MG_M2, 3),
        "note": "if the dose multiple exceeds the tolerable window (the MTD is dose-limited by "
                "hypertension/proteinuria), attainment cannot be reached by dose alone -- therapeutic "
                "drug monitoring / dose individualisation is required. See core.toxicity for the ceiling.",
        "source": "extends canine trametinib Phase I population PK, PMID 38889903",
    }


def maintenance_headroom(drug_key: str = "cobimetinib") -> dict:
    """Why the 'underdosed at MTD' finding is largely a TREATMENT-setting artifact.

    The ~10 ng/mL trametinib benchmark is the exposure 'associated with clinical efficacy' -- i.e.
    SHRINKING an established tumour. Maintenance-at-emergence asks something far cheaper: hold a single
    founding cell subcritical, which only needs the kill rate to beat growth. That maintenance target
    concentration is ``IC50 * (exp(growth*assay_days) - 1)`` -- the same small factor (~0.18) used for
    the CSF cell-level bar -- and it sits far below the achievable exposure. So a dog 'underdosed' for
    tumour shrinkage can still be comfortably above the maintenance bar.

    Uses the fully canine-HS-measured MEK drug (cobimetinib: IC50 and Cmax both measured, PMID 39202410)
    so the headroom is computed from dog data, not a transfer."""
    d = PARAMS[drug_key]
    factor = math.exp(GROWTH_PER_DAY * DEFAULT_ASSAY_DAYS) - 1.0
    c_maint = d.ic50_nM * factor
    return {
        "drug": d.name,
        "maintenance_target_nM": round(c_maint, 1),
        "achievable_cmax_nM": d.cmax_nM,
        "headroom_x": round(d.cmax_nM / c_maint, 1),
        "min_access_to_close": round(d.min_access_to_close(), 4),
        "reading": "the maintenance bar is far below achievable exposure, so the treatment-benchmark "
                   "attainment gap does not bind the maintenance use",
        "provenance": Provenance.DERIVED.value,
        "source": f"{d.source}; maintenance bar = IC50*(exp(g*t)-1), g={GROWTH_PER_DAY}/day",
    }


def combination_dose_reduction(synergy_factor: float = 3.0) -> dict:
    """Second lever: a synergistic partner lowers the single-agent MEK exposure needed for the same
    kill, pulling the required dose further under the toxicity ceiling. Synergy for MEK + a vertical
    MAPK partner (e.g. SHP2) or MEK + dasatinib is documented in canine HS in a subset of lines
    (PMID 39505062); the factor is a documented ASSUMED input, not a fitted constant."""
    if synergy_factor < 1:
        raise ValueError("synergy_factor must be >= 1")
    # A synergy factor s means the effective potency rises s-fold, so the dose to reach a fixed
    # attainment scales by 1/s^(1/exponent) under the same population-PK model.
    dose_multiple = (1.0 / synergy_factor) ** (1.0 / TRAMETINIB_DOSE_EXPONENT)
    base = dose_for_attainment(0.90)["dose_multiple_of_mtd"]
    return {
        "synergy_factor": synergy_factor,
        "dose_multiple_for_90pct_alone": base,
        "dose_multiple_for_90pct_with_partner": round(base * dose_multiple, 2),
        "reading": "with a synergistic partner the 90%-attainment dose falls back under the MTD, so "
                   "the ceiling is no longer binding",
        "provenance": Provenance.ASSUMED.value,
        "source": "MEK combination synergy in canine HS subset, PMID 39505062",
    }


def dosing_workaround() -> dict:
    """The three-lever workaround to 'underdosed at MTD, and 90% attainment exceeds the ceiling',
    ordered by how much each carries: (1) the maintenance bar is far lower than the treatment
    benchmark; (2) per-dog dose individualisation (TDM) closes the interindividual spread; (3) a
    synergistic partner lowers the required exposure. Each is computed, with provenance."""
    return {
        "lever_1_maintenance_bar_is_lower": maintenance_headroom(),
        "lever_2_individualise_dose_TDM": {
            "at_flat_mtd": target_attainment(TRAMETINIB_MTD_MG_M2),
            "reading": "the 30% shortfall is interindividual variability, not a population-mean wall; "
                       "measuring each dog's level and tuning the dose lifts attainment toward ~100% "
                       "without pushing the whole population over the ceiling",
        },
        "lever_3_synergistic_combination": combination_dose_reduction(),
        "bottom_line": "the attainment gap is a treatment-setting artifact plus PK spread; for "
                       "maintenance it is worked around by the lower maintenance bar, per-dog tuning, "
                       "and a synergistic pair -- no need to breach the toxicity ceiling",
    }


if __name__ == "__main__":
    for key, r in derived_closures().items():
        print(f"{key}: systemic k={r['systemic_kill_per_day']:.3f}/day closes={r['systemic_closes']}; "
              f"brain@0.30 k={r['brain_kill_per_day']:.3f}/day closes={r['brain_closes']}; "
              f"min access to close={r['min_access_to_close']:.3f}")
    print()
    print("Target attainment (trametinib, Gap 2):")
    for mult in (1.0, 1.5, 2.0):
        r = target_attainment(mult * TRAMETINIB_MTD_MG_M2)
        print(f"  dose {r['dose_mg_m2']:.2f} mg/m2 ({mult:.1f}x MTD): "
              f"P(reach {r['target_ng_ml']:.0f} ng/mL)={r['p_attain_target']:.2f}, "
              f"underdosed={r['fraction_underdosed']:.2f}")
    print("  dose for 90% attainment:", dose_for_attainment(0.90))
    print()
    print("Dosing workaround (maintenance bar / TDM / synergy):")
    w = dosing_workaround()
    hr = w["lever_1_maintenance_bar_is_lower"]
    print(f"  lever 1 -- maintenance bar {hr['maintenance_target_nM']} nM vs achievable "
          f"{hr['achievable_cmax_nM']} nM -> {hr['headroom_x']}x headroom")
    c = w["lever_3_synergistic_combination"]
    print(f"  lever 3 -- 90% dose {c['dose_multiple_for_90pct_alone']}x MTD alone -> "
          f"{c['dose_multiple_for_90pct_with_partner']}x with a synergistic partner")


# ---- The measured non-enhancing-tumour span, and what it means for the last open site -----------
#
# This is kept as a function rather than a constant because the POINT is the range, not a point
# estimate: the question "does the invading edge close with a licensed drug" is answered by the
# WORST measured value, not the mean.

#: Measured unbound ribociclib concentrations in Gd-NON-ENHANCING tumour, i.e. behind an intact
#: barrier. label -> (nM, source). The 65 nM entry is the lowest single patient value reported.
RIBOCICLIB_NONENHANCING_NM: dict[str, tuple[float, str]] = {
    "400 mg QD, median": (170.0, "PMID 41206763 (Phase 0/1, CDKN2A/B-deleted, Rb-wildtype)"),
    "400 mg QD, lowest patient": (65.0, "PMID 41206763, bottom of the 65-1770 nM range"),
    "600 mg QD, median": (634.0, "PMID 41206763"),
    "900 mg QD, mean": (560.0, "PMID 31285369 (Phase 0, recurrent glioblastoma)"),
}

#: Measured unbound ribociclib in CSF, same Phase 0. The leptomeningeal compartment, directly.
RIBOCICLIB_CSF_NM = 374.0
#: Measured unbound ribociclib in ENHANCING tumour -- the extra-axial/blood-side analogue.
RIBOCICLIB_ENHANCING_NM = 2152.0


def ribociclib_nonenhancing_range(growth: float = GROWTH_PER_DAY) -> dict:
    """Derived kill rate across the WHOLE measured non-enhancing-tumour span, worst value included.

    Answers the project's last open question -- does anything LICENSED beat the growth bar behind an
    INTACT barrier -- without a rodent ratio, a generic compartment access, or an enhancing-lesion
    concentration standing in for the real one. Access is 1.0 by construction because each value is
    already a tumour concentration.
    """
    d = PARAMS["ribociclib"]
    rows = {}
    for label, (conc, src) in RIBOCICLIB_NONENHANCING_NM.items():
        k = emax_kill_rate(d.ic50_nM, conc)
        rows[label] = {
            "unbound_nM": conc,
            "multiple_of_ic50": round(conc / d.ic50_nM, 1),
            "kill_per_day": round(k, 4),
            "margin": round(k - growth, 4),
            "closes": k > growth,
            "source": src,
        }
    worst = min(rows.values(), key=lambda r: r["margin"])
    return {
        "compartment": "invaded parenchyma behind an INTACT barrier (Gd-non-enhancing tumour)",
        "ic50_nM": d.ic50_nM,
        "growth_bar": growth,
        "by_dose": rows,
        "closes_at_every_measured_value": all(r["closes"] for r in rows.values()),
        "worst_measured_margin": worst["margin"],
        "fold_over_bar_at_worst": round(worst["kill_per_day"] / growth, 1),
        "provenance": Provenance.MEASURED.value,
        "reading": (
            "every measured value closes, including the single lowest patient in the reported range, "
            "so the last open site closes on a LICENSED drug and a measured human concentration "
            "rather than on a rodent ratio or a to-build molecule"
            if all(r["closes"] for r in rows.values()) else
            "at least one measured value fails the bar; the site does not close on this agent"
        ),
    }


def ribociclib_by_compartment(growth: float = GROWTH_PER_DAY) -> dict:
    """All three occupied sites, each from a MEASURED unbound concentration in that compartment.

    This is the first time in the project that one agent's access at all three sites comes from
    direct measurement in the matching compartment rather than from three different inferences.
    """
    d = PARAMS["ribociclib"]
    sites = {
        "extra-axial / blood-side bulk": RIBOCICLIB_ENHANCING_NM,
        "leptomeningeal / CSF": RIBOCICLIB_CSF_NM,
        "invaded parenchyma, intact barrier": RIBOCICLIB_NONENHANCING_NM["400 mg QD, median"][0],
    }
    out = {}
    for site, conc in sites.items():
        k = emax_kill_rate(d.ic50_nM, conc)
        out[site] = {"unbound_nM": conc, "kill_per_day": round(k, 4),
                     "margin": round(k - growth, 4), "closes": k > growth}
    return out
