"""Dispositions from the 2026-10-31 literature sweep of the hemangiosarcoma program.

Eleven angles were searched. This module records what each returned and, for every candidate that
surfaced, whether it is credited, already in the record, or assessed and excluded on a stated
scientific reason. Rule 13 forbids excluding a class for want of canine data, so each exclusion
below names a contradicted kill, a defeating escape, or an unaffordable toxicity instead.

Two entries are corrections to the record rather than new candidates:
  * the radiation-body exclusion cited an absence that PMID 42903052 has since falsified
    (handled in hsa_agent_tiers, not here);
  * CANDiD's 0.784/0.909 pair was labelled as two measured sensitivities when it is one point
    estimate's 95% confidence interval (handled in hsa_open_route_closure and
    hsa_condition_closure).

See docs/HSA_DURABLE_RESPONSE.md section 6e and docs/HSA_STATUS.md.
"""

from __future__ import annotations

from dataclasses import dataclass

# -------------------------------------------------------------------------------------------------
# Dispositions available to a candidate this sweep surfaced.
# -------------------------------------------------------------------------------------------------

ALREADY_IN_RECORD = "already in the record before this sweep"
CREDITED = "credited -- changes an input or a cell"
ASSESSED_NOT_CREDITED = "assessed and NOT credited, on a stated scientific reason"
CORRECTS_THE_RECORD = "corrects a claim the record was making"

# Reason kinds rule 13 permits for withholding credit. "canine data are absent" is not among them.
KILL_CONTRADICTED = "its kill is contradicted or internally discordant"
DEFEATED_BY_ESCAPE = "it is defeated by a named escape"
WRONG_COMPARTMENT = "measured in a compartment or presentation other than the one at issue"
NOT_A_KILL = "the mechanism is cytostatic or host-directed, not a log-remover"


@dataclass(frozen=True)
class Finding:
    candidate: str
    angle: str
    citation: str
    what_it_reports: str
    disposition: str
    reason_kind: str
    why: str


FINDINGS: tuple[Finding, ...] = (
    Finding(
        "eVim conjugate vaccine plus doxorubicin",
        "canine vaccines",
        "Engbersen et al. 2025, Int J Mol Sci 26(18):9096, PMID 41009669",
        "23 dogs, visceral hemangiosarcoma, post-splenectomy: 1-year survival 44% vs 14% in "
        "historical doxorubicin controls (p=0.0344), restricted mean survival +81 days at one "
        "year (p=0.02), median 136 -> 235 days (not significant), no systemic vaccine toxicity",
        ALREADY_IN_RECORD, "",
        "this is the program's own vaccine arm and has been since it was built -- carried in "
        "hsa_durable_response_analysis, hsa_scenarios and hsa_vaccine_maintenance, whose 60-day "
        "maintenance interval is taken from this trial. The sweep re-found the program's own "
        "input, which is a negative result for the sweep, not a new finding"),
    Finding(
        "oncolytic vesicular stomatitis virus plus doxorubicin",
        "new modality classes",
        "Labé et al. 2025, Vet Sci 12(10):921, PMID 41150061",
        "one dog with primary BONE hemangiosarcoma, neoadjuvant VSV then amputation and "
        "doxorubicin, alive beyond seven years",
        ALREADY_IN_RECORD, "",
        "already quarantined as an anecdote in hsa_route8_alternatives, and the oncolytic class "
        "is already NOT YET ASSESSED with a named path to assessment in hsa_agent_tiers. A single "
        "case in a different primary site yields no gradable kill rate"),
    Finding(
        "gilvetmab (caninized anti-PD-1)",
        "canine checkpoint",
        "Chon et al. 2026, J Am Vet Med Assoc, PMID 42710546, doi 10.2460/javma.26.06.0517",
        "review confirming gilvetmab is the only commercially available veterinary checkpoint "
        "inhibitor, holding conditional US licensure for melanoma and mast cell tumour",
        ALREADY_IN_RECORD, "",
        "the conditional licensure is already recorded in hsa_route_effect_sizes as 'the "
        "offsetting development', and the checkpoint class is already IN THE PROGRAM at the "
        "exists-today tier. The review adds no number the record lacks"),
    Finding(
        "hypofractionated radiotherapy",
        "canine hemangiosarcoma trials",
        "Rebelo et al. 2026, Front Vet Sci 13:1925779, PMID 42903052, "
        "doi 10.3389/fvets.2026.1925779",
        "53 dogs, subcutaneous or intramuscular hemangiosarcoma: 93% objective response, overall "
        "median survival 306 days, and 2,059 vs 287 days median survival for dogs operated before "
        "radiotherapy (p=0.007)",
        CORRECTS_THE_RECORD, WRONG_COMPARTMENT,
        "the finding's own conclusion does not change the radiation disposition -- local control "
        "of a treatable field is not cover for route 7's disseminated seeding, and the disease is "
        "subcutaneous/intramuscular rather than primary splenic, so rule 10 makes it indirect. "
        "What it does change is the record's STATED REASON: the ledger asserted that no "
        "transferable canine dataset existed and that a search returned only the eBAT trial. Both "
        "are now false. Corrected in hsa_agent_tiers"),
    Finding(
        "boron neutron capture therapy",
        "new modality classes",
        "Iwasaki et al. 2026, Front Vet Sci 13:1763965, PMID 42205798, "
        "doi 10.3389/fvets.2026.1763965",
        "three canine hemangiosarcoma lines take up boronophenylalanine by LAT1 transport; "
        "compound biological effectiveness after neutron irradiation 2.60, 2.31 and 1.25",
        ASSESSED_NOT_CREDITED, DEFEATED_BY_ESCAPE,
        "a measured, canine, disease-matched radiobiological kill -- so the class is emphatically "
        "not excluded for absent canine data. It is excluded because BNCT irradiates a single "
        "positioned field at an epithermal neutron source, and routes 7, 8 and 12b are occult "
        "disseminated seeding with no field to aim at. Added to the class ledger"),
    Finding(
        "cabozantinib plus nivolumab",
        "human angiosarcoma",
        "Alliance A091902, second-line, reported in Chen 2025, Curr Treat Options Oncol "
        "26(4):242-250, PMID 40056281, doi 10.1007/s11864-025-01307-7; and Murshid & Nawawi 2026, "
        "J Gastrointest Cancer 57(1), PMID 42536112, doi 10.1007/s12029-026-01552-5",
        "objective response 59% in taxane-pretreated human angiosarcoma, cutaneous and "
        "non-cutaneous alike -- against 5-13% for single-agent axitinib or pazopanib (Axi-STS, "
        "TAPPAS), 27.8% for cemiplimab and 25% for dual checkpoint blockade (SWOG S1609)",
        ASSESSED_NOT_CREDITED, WRONG_COMPARTMENT,
        "the pairing it validates -- a multi-target TKI with a checkpoint antibody -- is already "
        "structurally in the program as toceranib plus gilvetmab, so it adds no agent. Its 59% is "
        "an objective response rate in MEASURABLE ADVANCED disease, and this case is microscopic "
        "residual disease after splenectomy, where there is no measurable lesion to respond. An "
        "ORR in bulk disease does not transfer to a log-kill against micrometastases, so it is "
        "recorded as corroboration for the lever's direction and NOT as an effect size"),
    Finding(
        "paclitaxel plus nivolumab (first line)",
        "combination levers",
        "Alliance A091902 first-line arm, reported in Chen 2025, PMID 40056281",
        "adding nivolumab to first-line paclitaxel produced NO overall progression-free survival "
        "benefit in human angiosarcoma, while the TKI-plus-checkpoint pairing reached 59%",
        ASSESSED_NOT_CREDITED, WRONG_COMPARTMENT,
        "a negative that is useful precisely because it is negative: in the same disease and the "
        "same trial programme, checkpoint blockade added to a cytotoxic did not stack, while "
        "checkpoint blockade added to an anti-angiogenic did. It is consistent with the already "
        "settled finding that this plan does not DEPEND on its levers stacking "
        "(hsa_standard_audit's DOES_THE_PLAN_DEPEND_ON_THE_LEVERS_STACKING, graded TRANSFERRED). "
        "It is logged as support for that closed item and must not be read as reopening it"),
    Finding(
        "decitabine",
        "new modality classes / preprints",
        "preprint, Research Square 2026-08-24, doi 10.21203/rs.3.rs-10623493/v1 (NOT peer "
        "reviewed)",
        "hypomethylating agent in canine hemangiosarcoma: reduced ROBO1 promoter methylation and "
        "retarded growth in two cell lines, but inhibited tumour growth in Re21 xenografts and "
        "NOT in JuB2, with 5mC/5hmC shifts likewise seen only in Re21",
        ASSESSED_NOT_CREDITED, KILL_CONTRADICTED,
        "the agent exists today for humans, so the tier is not the obstacle. The obstacle is that "
        "the kill is internally discordant within the paper's own two models -- one xenograft "
        "responded, the other did not, on the same drug and the same readouts. Under rule 11 a "
        "number whose basis is contradicted is not a closure input. Peer review is also absent"),
    Finding(
        "sulfoquinovosylacylpropanediol (SQAP)",
        "preprints",
        "preprint, bioRxiv 2026-07-05, doi 10.64898/2026.07.03.735423 (NOT peer reviewed)",
        "suppressed tumour growth in three of three canine hemangiosarcoma patient-derived "
        "xenografts with minimal direct cytotoxicity in vitro; the transcriptional response was "
        "larger in MOUSE host cells than in canine tumour cells, acting through host vascular and "
        "macrophage remodelling",
        ASSESSED_NOT_CREDITED, NOT_A_KILL,
        "three-for-three in vivo is a real signal, but the paper locates the mechanism in the "
        "host stroma rather than the tumour cell, and reports minimal direct cytotoxicity. That "
        "makes it a cytostatic floor-holder, not a log-remover, and the stack's weakness is log "
        "removal against microscopic disease. The host in the experiment is also a mouse, so the "
        "host-mediated effect is the one quantity the model cannot transfer to a dog"),
    Finding(
        "enoxacin",
        "preprints",
        "preprint, bioRxiv 2025-07-17, doi 10.1101/2025.07.15.664801 (NOT peer reviewed)",
        "canonical microRNA loss in angiosarcoma, with enoxacin proposed as a therapeutic "
        "exploitation of it",
        ASSESSED_NOT_CREDITED, NOT_A_KILL,
        "preclinical and not peer reviewed, with no exposure-response figure in any species for "
        "this disease -- so there is nothing to grade against the exposure criterion. Recorded so "
        "a later thread finds it assessed rather than unexplored"),
    Finding(
        "fluvastatin plus dipyridamole",
        "ferroptosis and metabolic angles",
        "preprint, bioRxiv 2026-03-05, doi 10.64898/2026.03.03.709271 (NOT peer reviewed)",
        "fluvastatin alone did not suppress growth in two canine hemangiosarcoma PDX models; "
        "fluvastatin with dipyridamole did",
        ALREADY_IN_RECORD, "",
        "captured in docs/HSA_STATUS.md by the preceding sweep. Noted again only because the "
        "single-agent arm is explicitly negative, which is evidence about that arm"),
    Finding(
        "symmetric dimethylarginine (SDMA)",
        "early detection",
        "Marques et al. 2026, Vet Comp Oncol, PMID 42661152, doi 10.1111/vco.70108",
        "SDMA above the reference interval in 47% of 15 dogs with hemangiosarcoma and 0% of "
        "benign splenic lesions; higher in presumed disseminated disease (21.5 vs 12 ug/dL)",
        ASSESSED_NOT_CREDITED, WRONG_COMPARTMENT,
        "it rises WITH tumour burden and was elevated in under half of dogs who already had overt "
        "disease, so it is a burden marker, not an early-detection test. The early-detection "
        "premise is a stated assumption of this analysis and nothing here strengthens or weakens "
        "it. Not load-bearing anywhere"),
)

# -------------------------------------------------------------------------------------------------
# Angles searched, including the ones that returned nothing. An empty angle is a result.
# -------------------------------------------------------------------------------------------------

ANGLES_SEARCHED: dict[str, str] = {
    "eBAT / uPAR": "no peer-reviewed 2026 eBAT paper exists; the INDEXED literature is enumerated at "
                   "17 Europe PMC records. One source in this angle is identified but UNREADABLE -- "
                   "see THE_ONE_UNREADABLE_SOURCE. Its contents are excluded from every figure, so "
                   "no conclusion here depends on it",
    "canine hemangiosarcoma trials": "828 PubMed records; 20 newer than the record's newest "
                                     "citation. One bears on the program (PMID 42903052); the "
                                     "rest are diagnostics, pathology, or other anatomical sites",
    "canine vaccines": "no new canine hemangiosarcoma vaccine readout. The GD3 randomised trial "
                       "and VACCS remain unreported, so the record's pending readouts are still "
                       "pending",
    "canine checkpoint": "106 records; nothing the record lacks. Gilvetmab's licensure already "
                         "held",
    "human angiosarcoma": "the richest angle. Cabozantinib plus nivolumab at 59% ORR, and the "
                          "first-line chemotherapy-plus-checkpoint negative",
    "early detection": "CANDiD is already the record's screening source, cited from the primary "
                       "paper. SDMA assessed and not credited",
    "CNS agents": "nothing newer than 2024 in canine brain-metastasis chemotherapy. The CNS cells "
                  "rest where they did, on lomustine and temozolomide",
    "ferroptosis / GPX4": "ZERO records for ferroptosis or GPX4 in angiosarcoma or "
                          "hemangiosarcoma, in any species. A genuine empty set, verified against "
                          "a working control query",
    "preprints": "167 records once the query was fixed. Four canine therapeutic preprints, all "
                 "assessed above; none peer reviewed",
    "new modality classes": "BNCT added to the ledger as excluded on geometry. Oncolytic virus "
                            "unchanged at NOT YET ASSESSED",
    "combination levers": "the A091902 contrast -- TKI plus checkpoint stacked, cytotoxic plus "
                          "checkpoint did not -- is the first outcome evidence in this disease on "
                          "which pairings combine",
}

# -------------------------------------------------------------------------------------------------
# A search-method defect this sweep found in the record's own stated method.
# -------------------------------------------------------------------------------------------------

SEARCH_METHOD_CORRECTION: dict[str, str] = {
    "the_lesson_that_was_wrong": "docs/HSA_STATUS.md recorded, as a search-method lesson, that "
                                 "preprints should be found with Europe PMC 'SRC_TYPE:PPR' "
                                 "because the bioRxiv MCP cannot keyword-search.",
    "why_it_was_wrong": "SRC_TYPE is not a Europe PMC field. The API does not error on an unknown "
                        "field; it returns hitCount 0. So the query reported 'no preprints exist' "
                        "when it had in fact asked nothing.",
    "how_it_was_caught": "by running a control query that MUST return results. "
                         "'cancer AND SRC_TYPE:PPR' also returned 0, which no true negative can "
                         "explain. The correct field is SRC:PPR, under which 'cancer AND SRC:PPR' "
                         "returns 111,034 and '(hemangiosarcoma OR angiosarcoma) AND SRC:PPR' "
                         "returns 167.",
    "the_general_rule": "a zero from a machine-readable source is a claim about the QUERY until a "
                        "control query proves the source and the field work. Report an empty set "
                        "only after the control passes -- the ferroptosis/GPX4 zero in "
                        "ANGLES_SEARCHED was confirmed that way, the preprint zero was not.",
    "what_it_cost": "one false negative of record, asserting no preprints where there were 167.",
}

# -------------------------------------------------------------------------------------------------
# The single source this sweep could not read. Recorded separately so the completeness claim is
# explicitly BOUNDED and no conclusion is left resting on an unread document.
# -------------------------------------------------------------------------------------------------

THE_ONE_UNREADABLE_SOURCE: dict[str, str] = {
    "what_it_is": "PMID 42767940, doi 10.1111/vco.70098 -- the VCS 2026 conference abstract "
                  "supplement (Vet Comp Oncol 24 Suppl 3:4-41). It contains an abstract titled "
                  "'Reduction of Cancer Incidence in a Cohort of High-Risk Dogs Using eBAT', with "
                  "Modiano among the authors.",
    "why_it_is_unreadable": "its full text exists in exactly one place: a Wiley PDF behind "
                            "Cloudflare bot protection, on an article whose OA status is only "
                            "BRONZE. PubMed's own record carries the literal text '[Abstract not "
                            "available]' and the NCBI ID converter returns no PMCID; Europe PMC has "
                            "inEPMC: N and a zero-length abstract; Unpaywall shows the sole OA "
                            "location to be that same blocked PDF. CrossRef, OpenAlex, CORE, "
                            "scholar.archive.org, lifescience.net and the society's own site hold "
                            "metadata or nothing. The session's egress proxy is NOT the blocker "
                            "(recentRelayFailures: []), so there is no configuration fix.",
    "why_no_conclusion_rests_on_it": "its figures (2/15 vs 52/78, p=0.01) are excluded from every "
                                     "input, grade, route, condition and margin in this project. "
                                     "They appear nowhere outside the status document's narrative. "
                                     "So the sweep's verdict is unchanged whether the abstract is "
                                     "read or not.",
    "why_it_could_not_change_a_cell_anyway": "it is a PREVENTION result in healthy high-risk dogs. "
                                            "This analysis is durability in dogs with established "
                                            "disease after splenectomy. It bears on the Shine On "
                                            "screening arm, not on the route-site conjunction.",
    "the_only_thing_that_closes_it": "a human with institutional or library access to "
                                     "doi 10.1111/vco.70098, or asking the Modiano lab. Defeating "
                                     "the bot protection is forbidden by /root/.ccr/README.md for "
                                     "this failure class and must not be attempted.",
    "scope_of_the_completeness_claim": "the sweep is complete over REACHABLE sources. It is not and "
                                       "cannot be claimed exhaustive over the whole literature "
                                       "while this one document is unreadable -- that is a property "
                                       "of the source, not of the search, and it is enumerated here "
                                       "rather than glossed.",
}


VERDICT: dict[str, str] = {
    "headline": "no new agent changes the conjunction. One class is added to the ledger as "
                "excluded, two of the record's own claims are corrected, and no route-site cell "
                "or condition moves.",
    "what_would_have_changed_a_cell": "a log-remover with an exposure-response figure against "
                                      "microscopic disease at a site the stack does not already "
                                      "cover. Nothing found reports one: the two in vivo canine "
                                      "signals are a host-stromal cytostatic (SQAP) and a "
                                      "discordant hypomethylator (decitabine), and the strongest "
                                      "efficacy number of the sweep, 59%, is an ORR in bulk human "
                                      "disease.",
    "the_corrections_matter_more_than_the_candidates": "the radiation exclusion was resting on an "
                                                      "absence that no longer holds, and CANDiD's "
                                                      "confidence interval was being described as "
                                                      "two measurements. Both were load-bearing "
                                                      "descriptions; neither changes a verdict.",
}


def findings_by_disposition(disposition: str) -> list[Finding]:
    """Every finding carrying `disposition`."""
    return [f for f in FINDINGS if f.disposition == disposition]


def credited() -> list[Finding]:
    """Findings that change an input or a cell. Expected empty: the sweep moved nothing."""
    return findings_by_disposition(CREDITED)


def excluded_for_absent_canine_data() -> list[Finding]:
    """Rule 13 compliance. MUST stay empty: no candidate may be set aside for want of dog data."""
    return [f for f in FINDINGS
            if f.disposition == ASSESSED_NOT_CREDITED and f.reason_kind not in (
                KILL_CONTRADICTED, DEFEATED_BY_ESCAPE, WRONG_COMPARTMENT, NOT_A_KILL)]


def angles_that_returned_nothing() -> list[str]:
    """Angles whose result was an empty or unchanged set."""
    return [a for a, r in ANGLES_SEARCHED.items()
            if r.startswith("ZERO") or "nothing" in r or "no new" in r or "no peer-reviewed" in r]
