"""Rule 9: a closure claim is only as good as the stated candidate universe behind it."""

from canine_dsp import candidate_universe as cu, escape_audit as ea


def test_no_modality_class_is_left_unassessed_SILENTLY():
    """The failure this module exists to prevent: claiming closure over a list with holes in it.

    History, because it is the point. This was `cu.not_assessed() == []` twice over. The 2026-10-31
    sweep found a class the universe had never enumerated (live bacterial vector) while a funded dog
    trial in THIS disease was already using it; it was carried as a declared hole for a day, then
    EXCLUDED on a derived site mismatch, and the assertion went back to `== []`.

    Then the 2026-11-01 sweep found two more rows that had never existed, and one of them --
    antimetabolites -- cannot be excluded on any admissible ground and cannot be called in-model
    without an agent wired into the regimen. At that point `== []` stopped being an invariant and
    started being a thing to satisfy, which is the failure mode in miniature: the test would have
    pushed towards grading the class rather than reporting it.

    So the invariant is restated as what it always meant: no hole may be SILENT. Every open class
    must be declared in KNOWN_OPEN_CLASSES, which `candidate_universe._validate()` enforces at
    import and which the published catalogue line must match. The count of open classes is pinned
    separately, in `test_the_catalogue_count_and_the_open_count_are_what_the_docs_say`, so a change
    to it fails loudly instead of passing quietly.
    """
    undeclared = [m.name for m in cu.not_assessed() if m.name not in cu.KNOWN_OPEN_CLASSES]
    assert undeclared == [], undeclared
    stale = [n for n in cu.KNOWN_OPEN_CLASSES
             if n not in {m.name for m in cu.not_assessed()}]
    assert stale == [], stale


def test_the_bacterial_vector_class_is_excluded_on_a_site_mismatch_not_on_absent_canine_data():
    """Rule 13: the ground must be scientific. This one is a derived mismatch between a documented
    hypoxia-driven tropism and a target site that is the least hypoxic part of the tumour."""
    m = next(x for x in cu.UNIVERSE if x.name.startswith("live bacterial vector"))
    assert m.status is cu.Status.EXCLUDED
    assert m.exclusion_ground is cu.ExclusionGround.KILL_CONTRADICTED
    for phrase in ("HYPOXIA", "INVADING EDGE BEHIND AN INTACT BARRIER", "WHAT WOULD REOPEN IT",
                   "hitchhiking"):
        assert phrase in m.basis, phrase
    # the exclusion must stay falsifiable and must not rest on missing dog data
    assert "NON-ENHANCING" in m.basis
    assert m in cu.excluded()
    assert cu.excluded_citing_absent_canine_data() == []


def test_every_excluded_class_records_a_reason():
    """'Excluded' without a reason is just 'not assessed' with better manners."""
    for m in cu.excluded():
        assert len(m.basis) > 40
        assert m.representative.strip()


def test_the_classes_rule_9_names_are_all_present():
    """CLAUDE.md rule 9 lists the minimum modality classes for cancer work."""
    names = " ".join(m.name.lower() for m in cu.UNIVERSE)
    for required in ("cytotoxic", "targeted", "antibod", "bispecific", "cell therapy",
                     "transplant", "vaccine", "cytokine", "radiation", "sanctuary"):
        assert required in names, required


def test_transplant_is_excluded_on_biology_not_availability():
    """A feasibility exclusion is weak; this one has to rest on the microglial origin argument."""
    t = next(m for m in cu.UNIVERSE if "transplant" in m.name)
    assert t.status is cu.Status.EXCLUDED
    assert "yolk" in t.basis.lower()
    assert "lymphoma" in t.canine_hs_evidence.lower()  # feasibility is conceded, not the reason


def test_closure_claim_states_the_catalogue_size_and_the_exclusions():
    claim = cu.closure_claim(ea.audited_escape_count())
    assert str(len(cu.UNIVERSE)) in claim
    assert str(ea.audited_escape_count()) in claim
    assert "excluded" in claim.lower()


def test_tally_covers_every_class():
    assert sum(cu.tally().values()) == len(cu.UNIVERSE)


def test_some_classes_carry_canine_hs_measurements():
    """If nothing were measured in this disease the universe would be pure speculation."""
    assert len(cu.with_canine_hs_evidence()) >= 5


# --- rule 13: exclusions need a scientific ground, and availability is a separate axis ------------

def test_no_class_is_excluded_for_absent_canine_data():
    """CLAUDE.md rule 13 and failure 8. The lapse this lint exists to catch, in one assertion."""
    assert cu.excluded_citing_absent_canine_data() == []


def test_every_exclusion_carries_an_admissible_ground():
    """Rule 13 allows exactly three grounds. _validate() enforces it; this pins the behaviour."""
    for m in cu.excluded():
        assert m.exclusion_ground in set(cu.ExclusionGround), m.name


def test_no_ground_is_recorded_on_a_class_that_is_in_the_model():
    for m in cu.in_model():
        assert m.exclusion_ground is None, m.name


def test_every_ground_is_actually_used():
    """If a ground has no members, the enum is aspirational rather than descriptive."""
    for ground, members in cu.excluded_by_ground().items():
        assert members, f"{ground} has no members"


def test_availability_is_independent_of_status():
    """The point of the rule-13 split: obtainable classes get excluded, and model classes can be
    near-future."""
    assert any(m.availability is cu.Availability.EXISTS_TODAY for m in cu.excluded())
    assert any(m.availability is cu.Availability.NEAR_FUTURE for m in cu.in_model())


def test_no_modality_class_in_the_model_is_theoretical():
    """Rule 13 after the user's clarification: near-future counts, theoretical never does."""
    assert cu.theoretical_in_model() == []


def test_transplant_is_the_exists_today_exclusion_that_proves_the_point():
    t = next(m for m in cu.UNIVERSE if "transplant" in m.name)
    assert t.availability is cu.Availability.EXISTS_TODAY
    assert t.exclusion_ground is cu.ExclusionGround.KILL_CONTRADICTED


def test_the_epigenetic_toxicity_ground_is_computed_not_asserted():
    """Rule 13: where canine data are absent, test against a derived transfer. This is that test."""
    arith = cu.epigenetic_toxicity_arithmetic()
    assert not arith["fits"], "the exclusion claims the budget is blown; the arithmetic must agree"
    assert arith["oversubscribed_axes_if_added"]
    assert "TRANSFERRED" in arith["provenance"]


def test_every_class_records_an_availability_basis():
    for m in cu.UNIVERSE:
        assert len(m.availability_basis) > 20, m.name


def test_availability_tally_covers_every_class():
    assert sum(cu.availability_tally().values()) == len(cu.UNIVERSE)


def test_the_regrounded_exclusions_are_named_in_the_statement():
    """A silent re-grounding is indistinguishable from a cover-up; the statement must say so."""
    assert cu.regrounded_under_rule_13()
    assert "RE-GROUNDED" in cu.statement()


def test_closure_claim_reports_the_availability_split():
    claim = cu.closure_claim(ea.audited_escape_count())
    assert str(len(cu.exists_today_in_model())) in claim
    assert "today" in claim


def test_the_two_ablative_device_modalities_are_assessed_with_a_stated_reason():
    """Histotripsy and H-FIRE were named only on a superseded page. Rule 13: a modality may be set
    aside for a scientific reason, never for absent canine data -- here, both need a cranial defect
    in the dog and neither gives continuous presence."""
    m = next(x for x in cu.UNIVERSE if x.name == "sanctuary-site / local delivery")
    assert "HISTOTRIPSY" in m.representative and "H-FIRE" in m.representative
    assert "cranial defect" in m.representative or "craniotomy" in m.representative
    assert cu.excluded_citing_absent_canine_data() == []


def test_the_antimetabolite_class_is_closed_on_three_measured_ic50s():
    """Enumerated 2026-11-01 as the second rule-9 hole, carried open for ONE DAY, then EXCLUDED on
    2026-11-02 -- because the measurements that close it were already cited by this project, in a
    table it had transcribed five rows out of ten. This test pins the closure and its ground so the
    class cannot drift back to open on the day-one reasoning, which rested on reading a 5 uM
    screening threshold as a potency (CLAUDE.md failure 13)."""
    m = next(x for x in cu.UNIVERSE if "antimetabolite" in x.name)
    assert m.status is cu.Status.EXCLUDED
    assert m.exclusion_ground is cu.ExclusionGround.KILL_CONTRADICTED
    assert m.name not in cu.KNOWN_OPEN_CLASSES
    assert m.availability is cu.Availability.EXISTS_TODAY, "availability was never the issue"
    # the three measured members, from two independent laboratories
    for pmid in ("25715778", "29490634"):
        assert pmid in m.basis, f"{pmid} carries one of the measured IC50 sets"
    assert "27062671" in m.basis, "the canine toxicity ceiling below the dose that reached the CSF"
    # the decisive arithmetic: both sides measured in the dog
    assert "38.2" in m.basis and "8.3 uM" in m.basis
    assert "4.6x" in m.basis
    # the counter-evidence is recorded, not buried, and scoped
    assert "39428688" in m.basis, "the human LCH 6-year OS that cuts the other way"
    assert "42780343" in m.basis, "the n=1 CNS Erdheim-Chester remission"
    assert "93.2%" in m.basis
    # and it is labelled as cross-disease rather than allowed to overturn the canine measurement
    assert "cannot overturn a measurement in this one" in m.basis


def test_the_antimetabolite_exclusion_names_what_would_reopen_it():
    """Rule 13 exclusions stay falsifiable. Clofarabine is the one member with pan-activity and no
    IC50, and rule 15 forbids transferring cladribine's resistance onto it -- so the exclusion must
    say so rather than quietly treating the class as uniform."""
    m = next(x for x in cu.UNIVERSE if "antimetabolite" in x.name)
    assert "WHAT WOULD REOPEN IT" in m.basis
    assert "CLOFARABINE IC50" in m.basis
    assert "deamination" in m.basis, "the chemistry that blocks the within-class transfer"
    assert "deoxycytidine kinase" in m.basis, "the second reopening route"


def test_the_false_explanation_for_the_empty_enum_member_is_recorded_not_deleted():
    """CLAUDE.md failure 12. The empty DrugClass.ANTIMETABOLITE member was explained in the code as
    'the paper tested no antimetabolite'. It had two. Keeping the retraction in the file is the only
    thing that stops the same invented explanation being written again."""
    m = next(x for x in cu.UNIVERSE if "antimetabolite" in x.name)
    assert "IT HAD TWO ANTIMETABOLITE ROWS" in m.basis
    assert "five rows out of ten" in m.basis
    assert "failure 12" in m.basis
    # and the misreading of the 2026 screen's a-priori exclusion list
    assert "MISREAD" in m.canine_hs_evidence
    assert "MELPHALAN is on the same exclusion list" in m.canine_hs_evidence


def test_the_open_class_does_not_become_a_failing_input():
    """Rule 11 keeps two axes apart: `standard_audit.failing()` grades the inputs the model USES,
    while rule 9 grades the candidate list the claim is quantified OVER. An unenumerated class is
    the second kind. Collapsing them would re-grade a live input against demonstration."""
    from canine_dsp import standard_audit
    assert standard_audit.failing() == [] or all(
        "antimetabolite" not in str(f).lower() for f in standard_audit.failing()
    )


def test_the_fgfr_axis_is_excluded_on_brain_tumour_data_not_on_absent_canine_data():
    """Found in the same sweep and it closes out: the licensed members exist, the canine signal is
    real, and the class still fails -- in human recurrent glioma, in the biomarker this tumour
    actually has."""
    m = next(x for x in cu.UNIVERSE if "FGFR" in x.name)
    assert m.status is cu.Status.EXCLUDED
    assert m.exclusion_ground is cu.ExclusionGround.KILL_CONTRADICTED
    assert m.availability is cu.Availability.EXISTS_TODAY
    assert "35344029" in m.basis, "the infigratinib glioma phase 2 is the ground"
    assert "212018" in m.availability_basis and "213736" in m.availability_basis
    assert m in cu.newly_assessed()
    assert cu.excluded_citing_absent_canine_data() == []


def test_the_catalogue_count_and_the_open_count_are_what_the_docs_say():
    """The published line has moved three times in three days as holes were found by looking:
    '26 -- 15/11/0 unassessed' -> '28 -- 15/12/1 open' -> '29 -- 15/13/1 open'. If this test fails,
    three documents and a reader-facing page are now lying."""
    t = cu.tally()
    assert len(cu.UNIVERSE) == 64
    assert t["IN_MODEL"] == 17
    assert t["EXCLUDED"] == 18
    assert t["CANDIDATE"] == 29
    assert t["NOT_ASSESSED"] == 0
    claim = cu.closure_claim(ea.audited_escape_count())
    assert "64 modality classes" in claim
    assert "29 assessed candidates" in claim and "0 unassessed" in claim


def test_c3_records_the_maintenance_pincer_at_the_strength_shown():
    """Rule 5: the 75% relapse figure CONFIRMS C3 and the 60% discontinuation figure pressures it.
    Both are human and indirect, and the answer to the second is structural, not demonstrated."""
    from canine_dsp import deterministic_closure as dc
    c3 = next(c for c in dc.CONDITIONS if c.tag == "C3")
    blob = " ".join(str(v) for v in vars(c3).values())
    assert "41178439" in blob
    assert "75%" in blob and "60%" in blob
    assert "structural, not demonstrated" in blob


def test_every_cross_compound_transfer_in_the_new_classes_states_a_direction():
    """Rule 15, added to CLAUDE.md on 2026-11-01 while these two classes were being written up.
    A transfer from one compound to another needs a written comparison and a DIRECTION, and may
    bound the other compound's number but never contradict it. Both new entries lean entirely on
    cross-compound and cross-species evidence, so both must show their work."""
    anti = next(x for x in cu.UNIVERSE if "antimetabolite" in x.name)
    # 5-FU: the study dosed the CATABOLITE, not the drug -- that must be stated, not glossed
    assert "FBAL" in anti.basis and "CATABOLITE" in anti.basis.upper()
    assert "principal catabolite" in anti.basis, "the direction that licenses the transfer"
    assert "NOT a measured neurotoxic dose for 5-FU itself" in anti.basis
    # floxuridine: bounded, never contradicted
    assert "it bounds the class's brain use, it does not measure it" in anti.basis
    # clofarabine: an efficacy transfer across disease, and LCH is the milder one -> a ceiling
    assert "CEILING for HS and never a floor" in anti.basis
    # within-class: cladribine's measured resistance may NOT be carried onto clofarabine
    assert "rule 15 forbids transferring cladribine's resistance to it" in anti.basis
    # and the cross-disease human outcomes bound nothing about the canine kill
    assert "Under rule 15 neither bounds the canine-HS kill" in anti.basis

    fgfr = next(x for x in cu.UNIVERSE if "FGFR" in x.name)
    assert "one compound's trial cannot contradict another compound's number" in fgfr.basis
    assert "statement about the TARGET" in fgfr.basis
    assert "CEILING for an overexpression-only tumour" in fgfr.basis


def test_the_degrader_class_is_the_third_hole_and_is_carried_open():
    """Found 2026-11-02. Targeted protein degradation was not a row, and no existing row covers it:
    a cereblon molecular glue is not a kinase inhibitor, not an epigenetic agent and not a
    checkpoint or cytokine agent. It cannot be dismissed (a licensed member has a phase 2 with
    POSTED results in a cohort including histiocytic sarcoma) and cannot be called closed (its
    measured human CSF access falls short at the parenchyma), so it is OPEN and declared."""
    m = next(x for x in cu.UNIVERSE if "degradation" in x.name)
    assert m.status is cu.Status.CANDIDATE
    assert m.name in cu.OPEN_BEFORE_ASSESSMENT_2026_11_04
    assert m.deciding_measurement
    assert m.exclusion_ground is None
    assert m.availability is cu.Availability.EXISTS_TODAY
    # the trial that forbids dismissing it, with its posted numbers
    assert "NCT02523040" in m.basis
    assert "HISTIOCYTIC SARCOMA" in m.basis
    for n in ("0.67", "62%", "92%"):
        assert n in m.basis, n
    # rule 14: the proxy was named and searched, and the WORSE of two measurements is the one used
    assert "22109830" in m.basis and "35732975" in m.basis
    assert "1.3-2.4%" in m.basis
    assert "even when it is the worse number" in m.basis
    # and the arithmetic is stated in both directions rather than rounded to a verdict
    assert "STRADDLES" in m.basis and "8-15x SHORT" in m.basis


def test_the_degrader_class_names_its_next_step_as_a_within_class_direction():
    """Rule 15: the same assay measured pomalidomide an order of magnitude more permeable than
    lenalidomide, so that transfers as a DIRECTION (which member to take to a brain site) and never
    as a number attached to the other compound."""
    m = next(x for x in cu.UNIVERSE if "degradation" in x.name)
    assert "POMALIDOMIDE is the class member to take to a brain site" in m.basis
    assert "ONE ORDER OF MAGNITUDE" in m.basis
    assert "forbids attaching" in m.basis
    # and the direction was then CONFIRMED by searching it: rule 14 found an outcome, not a ratio
    assert "30262659" in m.basis, "pomalidomide in primary CNS lymphoma"
    assert "SIX COMPLETE RESPONSES" in m.basis
    assert "48%" in m.basis
    # the question the class now faces is narrower than the one it was opened with
    assert "HAS CHANGED" in m.basis.upper()
    # and the two confounds are stated rather than glossed
    assert "WITH DEXAMETHASONE" in m.basis
    assert "PCNSL is a LYMPHOMA" in m.basis
    # no canine data at all, and that is explicitly NOT the ground for anything
    assert m.canine_hs_evidence.startswith("NONE IN THIS DISEASE")
    assert "not a ground for exclusion" in m.canine_hs_evidence


def test_cobimetinib_carries_a_licensed_genotype_agnostic_histiocytic_indication():
    """The strongest single fact in the sweep, and it was a label read rather than a trial. The
    record had cited NDA 206192 only for the canine minimum lethal dose."""
    m = next(x for x in cu.UNIVERSE if "MAPK axis" in x.name)
    # it lives in availability_basis, which is where a regulatory fact belongs
    a = m.availability_basis
    assert "206192" in a and "20260729" in a
    assert "HISTIOCYTIC NEOPLASMS" in a
    # the point is the ABSENCE of a genotype gate, shown by contrast with the same label's other use
    assert "V600E or V600K" in a
    assert "74-372 nM" in a, "the measured canine-HS IC50 that makes it more than a tier label"
    # and it must not be read as closing the brain
    assert "WHAT IT DOES NOT DO" in a
    assert "0.5x" in a


def test_the_cdk_row_carries_the_negative_as_well_as_the_two_positives():
    """Rule 5. The 2026-11-03 sweep found three measurements on this row pointing two ways: a 31 nM
    unbound concentration in Gd-non-enhancing tumour in THIS project's genotype, a human
    microdialysis ratio that clears the parenchymal bar, and 51 patients with NO confirmed
    intracranial response. A row that recorded only the first two would be the overstatement rule 5
    exists to stop."""
    m = next(x for x in cu.UNIVERSE if "cell-cycle" in x.name)
    # the positive, in the compartment at issue and the matching genotype
    assert "31 nM" in m.basis and "12 nM" in m.basis
    assert "CDKN2A/B DELETION" in m.basis and "INTACT RB" in m.basis
    # the second, independent method -- and its n
    assert "0.27" in m.basis and "2.73" in m.basis
    assert "n=5" in m.basis, "the microdialysis n must travel with the ratio"
    # the negative, and the authors' own sentence
    assert "NO CONFIRMED INTRACRANIAL RESPONSE" in m.basis.upper()
    assert "41768125" in m.basis
    assert "COMBINATION" in m.basis
    # why it does not sink the row -- the reasoning must be explicit, not implied
    assert "NOT SELECTED for the genotype" in m.basis
    assert "STRENGTH-OF-EVIDENCE correction" in m.basis


def test_the_mapk_row_carries_the_288_patient_cns_negative():
    """The most adverse finding of the sweep sits on the weakest row. Zero short-term responses in
    neurodegenerative CNS LCH, and a 45% five-year risk of DEVELOPING CNS disease while on the drug."""
    m = next(x for x in cu.UNIVERSE if "MAPK axis" in x.name)
    a = m.availability_basis   # it sits with the other regulatory/availability facts
    assert "41678955" in a
    assert "288 children" in a
    assert "45%" in a
    assert "NONE (ND, DI, and SC)" in a
    # scoped, so it is not overread
    assert "distinct CNS pathology" in a


def test_c3_records_the_largest_discontinuation_dataset_and_its_attack_on_the_mitigation():
    """61% reactivation after discontinuation in 113 patients CONFIRMS C3. The next sentence --
    that no empirical maintenance prevented reactivation -- attacks C3's structural answer, and the
    condition has to carry both halves."""
    from canine_dsp import deterministic_closure as dc
    c3 = next(c for c in dc.CONDITIONS if c.tag == "C3")
    blob = " ".join(str(v) for v in vars(c3).values())
    assert "41678955" in blob
    assert "79 REACTIVATED" in blob, "the Results section says 79, not the abstract's 69"
    assert "UNDERSTATED the necessity" in blob
    assert "NONE of the various" in blob
    # and the correction to the figure this project published on 2026-11-01
    assert "40053897" in blob
    assert "31% of the cohort" in blob
    assert "ALL-CAUSE" in blob


def test_the_completeness_critic_ran_and_its_seven_classes_are_recorded():
    """The critic was a planned phase of the sweep, failed twice on usage limits, and was then
    deferred on the argument that it should not be self-assessed. That argument was wrong. Running it
    -- against ATC L01 and the source screen's pan-active table rather than against this list --
    found seven more classes and took the headline from '29, 1 open' to '36, 6 open'."""
    names = {m.name for m in cu.UNIVERSE}
    for expected in ("cytotoxic chemotherapy -- topoisomerase inhibitors",
                     "cytotoxic chemotherapy -- cytotoxic antibiotics / anthracyclines",
                     "nuclear export inhibition (XPO1 / SINE compounds)",
                     "proteasome inhibition",
                     "HSP90 inhibition",
                     "cardiac glycosides / Na+,K+-ATPase inhibition",
                     "translation-elongation inhibition"):
        assert expected in names, expected
    # the external taxonomy must be named in the record, so the next thread can pick a different one
    assert "ATC L01" in cu.__doc__


def test_the_xpo1_class_carries_the_canine_licensed_agent_and_its_rule_15_limits():
    """The most consequential hole: a canine-LICENSED, oral, indefinitely-scheduled agent in a class
    with no row -- whose pharmacology a sibling branch of this project had already done."""
    m = next(x for x in cu.UNIVERSE if "XPO1" in x.name)
    assert m.status is cu.Status.CANDIDATE
    assert m.name in cu.OPEN_BEFORE_ASSESSMENT_2026_11_04
    assert m.deciding_measurement
    assert m.availability is cu.Availability.EXISTS_TODAY
    assert "LICENSED FOR DOGS" in m.availability_basis
    assert "Laverdia" in m.basis
    # the regulatory claim was corrected on three counts and its load-bearing half retracted
    assert "18 DECEMBER 2025" in m.basis
    assert "141-614" in m.basis
    assert "NOT ON THE LABEL" in m.basis
    assert "DOES NOT SURVIVE" in m.basis
    # the measured three-species access, verified in this thread from the source table
    assert "0.71" in m.basis and "0.72" in m.basis and "0.6 monkey" in m.basis
    # the source table does not reconcile on its own headline figure, and the row must say so
    assert "DOES NOT RECONCILE" in m.basis
    assert "DOSE MISMATCH" in m.basis
    # "intact barrier" was this project's inference, not the source's words
    assert "ARE NOT IN THE SOURCE" in m.basis
    assert "27323910" in m.basis
    # and the two rule-15 limits that keep it from being graded in
    assert "total and not unbound" in m.basis
    # cross-branch provenance labelled, not passed off as this thread's own verification
    assert "taken from the sibling branch and flagged as unverified" in m.basis


def test_the_anthracycline_row_records_that_its_potency_CLEARS():
    """Rule 5, in the direction that is easy to skip: this class was missing, and when assessed its
    measured potency turned out to sit BELOW achievable canine exposure. The exclusion rests on the
    cumulative cardiac ceiling, not on a pretence that the drug does not work."""
    m = next(x for x in cu.UNIVERSE if "anthracyclines" in x.name)
    assert m.exclusion_ground is cu.ExclusionGround.TOXICITY_UNAFFORDABLE
    assert "0.175-0.631 uM" in m.basis
    assert "1.13 uM" in m.basis
    assert "clears by 1.8x to 6.5x" in m.basis
    assert "the potency clears and the schedule cannot" in m.basis


def test_two_open_classes_refuse_to_assert_the_unsourced_obvious():
    """Rule 16. It would have been easy to exclude the proteasome inhibitors on bortezomib's
    reputation for poor CNS entry, and the cardiac glycosides on digoxin's nanomolar therapeutic
    range. Neither source was fetched, so neither claim is made."""
    pro = next(x for x in cu.UNIVERSE if x.name == "proteasome inhibition")
    assert "NO CNS ACCESS FIGURE WAS ESTABLISHED BY THIS THREAD" in pro.basis
    assert "this row does not" in pro.basis
    gly = next(x for x in cu.UNIVERSE if "cardiac glycosides" in x.name)
    assert "NOT as a ground" in gly.basis
    assert "has NOT fetched" in gly.basis


def test_the_second_taxonomy_diff_used_a_different_axis_and_named_it():
    """Rule 16's corollary. ATC L01 is a CHEMICAL taxonomy; re-diffing against it would re-ask the
    same question. The second pass used a BIOLOGICAL one and must name it, so a third pass can pick
    yet another."""
    assert "Hanahan hallmarks" in cu.__doc__
    assert "L02/L03/L04" in cu.__doc__
    names = {m.name for m in cu.UNIVERSE}
    for expected in ("anti-angiogenic / VEGFR-axis multikinase inhibition",
                     "apoptosis induction / BH3 mimetics (BCL-2, BCL-XL)"):
        assert expected in names, expected


def test_the_vegfr_row_credits_the_existing_agent_verdict_rather_than_claiming_discovery():
    """CLAUDE.md failure 1. Toceranib was already assessed in therapies.py; only the class row was
    missing. Calling that a discovery would be the failure rule 1 exists to stop. What the row adds
    is measured arithmetic in place of a 'likely'."""
    m = next(x for x in cu.UNIVERSE if "VEGFR-axis" in x.name)
    assert m.exclusion_ground is cu.ExclusionGround.KILL_CONTRADICTED
    assert "ALREADY ASSESSED AS AGENTS" in m.basis
    assert "CONSIDERED_UNMEASURED" in m.basis
    assert "failure 1" in m.basis
    # the arithmetic that replaces the guess, from two independent datasets
    assert "17-19x" in m.basis and "37-149x" in m.basis
    assert "608 nM" in m.basis, "the screen's own headline figure, previously unused here"


def test_the_bh3_row_records_the_rule_15_error_in_the_existing_record():
    """The class was set aside on navitoclax's on-target thrombocytopenia -- which is BCL-XL
    inhibition, the very thing venetoclax was engineered to spare. One compound's toxicity was
    allowed to bound another's in the direction opposite to the chemistry."""
    m = next(x for x in cu.UNIVERSE if "BH3" in x.name)
    assert m.status is cu.Status.CANDIDATE
    assert m.name in cu.OPEN_BEFORE_ASSESSMENT_2026_11_04
    assert m.deciding_measurement
    assert "ENGINEERED" in m.basis and "SPARE" in m.basis
    assert "does not appear anywhere in this repository" in m.basis, \
        "venetoclax is absent from the whole repo"
    # and the absence from the screen's hit list is NOT graded as a negative
    assert "UNDETERMINED by this thread" in m.canine_hs_evidence


def test_the_two_rejected_hallmark_columns_are_recorded_not_silently_dropped():
    """Rule 9 asks for a status on everything that could plausibly matter. Two columns were judged
    not to meet that bar; the judgement is written down so it can be challenged, and deliberately
    NOT dressed up as a rule-13 exclusion it has no ground for."""
    src = __import__("inspect").getsource(cu)
    assert "DIFFERENTIATION THERAPY" in src and "MICROBIOME MODULATION" in src
    assert "judgements about plausibility, not exclusions on rule 13 grounds" in src
    names = {m.name for m in cu.UNIVERSE}
    assert not any("differentiation" in n or "microbiome" in n for n in names)


def test_three_independent_axes_are_named_and_none_converged():
    """The result that matters more than any of the classes. Three external taxonomies on different
    axes each found classes the others missed -- 7, then 3, then 3 -- so the denominator of a closure
    claim is axis-dependent and the module must say so instead of implying the enumeration
    terminated."""
    doc = cu.__doc__
    for axis in ("ATC L01", "Hanahan hallmarks", "molecular TARGET CLASS"):
        assert axis in doc, axis
    assert "AXIS-DEPENDENT" in doc
    assert "NOT \"the catalogue is now complete\"" in doc
    assert "add a fourth rather than re-run one of these" in doc


def test_the_open_classes_split_by_whether_canine_evidence_exists():
    """Eleven open classes is not one number. Five carry a canine-HS measurement and are worth
    working up; six carry nothing in this disease and are a statement about where to look next.
    Collapsing them would let a pan-active screen hit read as the same kind of gap as an unsearched
    mechanism."""
    withev = cu.open_with_canine_hs_evidence()
    without = cu.open_without_canine_hs_evidence()
    assert len(withev) + len(without) == len(cu.candidates()) + len(cu.not_assessed())
    assert len(withev) == 7 and len(without) == 22
    assert all(m.canine_hs_evidence.startswith("MEASURED") for m in withev)
    names = {m.name for m in withev}
    assert "nuclear export inhibition (XPO1 / SINE compounds)" in names


def test_the_glucocorticoid_hole_is_recorded_as_the_embarrassment_it_is():
    """prednisone, prednisolone and glucocorticoid appeared NOWHERE in the repo -- the cheapest and
    most available class in veterinary oncology, missing from a catalogue claiming 0 unassessed.
    Recorded bluntly, with the n=1 negative and the immune-arm antagonism each at its own strength,
    and with the explicit note that neither is an admissible ground for exclusion."""
    m = next(x for x in cu.UNIVERSE if "glucocorticoid" in x.name)
    assert m.status is cu.Status.CANDIDATE
    assert m.availability is cu.Availability.EXISTS_TODAY
    assert "NOWHERE in this repository" in m.basis
    assert "42780343" in m.basis, "the n=1 CNS-ECD case that was refractory to corticosteroids"
    assert "NOT one of rule 13's three grounds" in m.basis
    # and the reason that matters: the measurement nobody looked for
    assert "trivial assay on cells that already exist" in m.basis


def test_the_fourth_axis_found_parp_was_load_bearing_and_unrowed():
    """NCIt diff, 2026-11-04: niraparib was priced in the regimen and appeared zero times in the
    catalogue. The fix is a row, IN_MODEL, recorded as an integrity discrepancy -- not a discovery."""
    m = next(x for x in cu.UNIVERSE if x.name.startswith("DNA-damage-response / PARP"))
    assert m.status is cu.Status.IN_MODEL
    assert "niraparib" in m.representative
    assert "zero times in this catalogue" in m.basis
    assert "ENZYMATIC" in m.canine_hs_evidence


def test_fourth_and_fifth_axes_are_named_and_did_not_converge():
    doc = cu.__doc__
    assert "NCI Thesaurus (v26.10d)" in doc and "38578405" in doc
    assert "veterinary formulary" in doc
    assert "Five axes, five sets of finds" in doc
    assert "SIXTH AXIS" in doc and "SEVENTH AXIS" in doc


def test_formulary_exclusions_use_admissible_grounds():
    cox = next(x for x in cu.UNIVERSE if x.name.startswith("COX-2"))
    assert cox.exclusion_ground is cu.ExclusionGround.KILL_CONTRADICTED
    assert "15872381" in cox.basis and "1 of 20" in cox.basis
    tig = next(x for x in cu.UNIVERSE if x.name.startswith("intralesional"))
    assert tig.exclusion_ground is cu.ExclusionGround.DEFEATED_BY_ESCAPE
    assert "NOT quantified" in tig.basis


def test_rabacfosadine_is_not_swept_into_the_antimetabolite_exclusion():
    """Rule 15: cytarabine/methotrexate IC50s may not be carried onto a different compound."""
    m = next(x for x in cu.UNIVERSE if "rabacfosadine" in x.name)
    assert m.status is cu.Status.CANDIDATE
    assert "RULE 15" in m.basis


def test_unfetched_claims_are_flagged_not_asserted():
    """Rule 16: what the reviewers asserted but nobody fetched is labelled as such."""
    by = {x.name: x for x in cu.UNIVERSE}
    assert "NOT fetched" in by["anti-invasion / adhesion / chemokine-axis blockade (integrin, CXCR4)"].basis
    assert "NOT verified" in by["high-Z nanoparticle radioenhancement"].availability_basis
    assert "INDIRECT" in by["anti-invasion / adhesion / chemokine-axis blockade (integrin, CXCR4)"].canine_hs_evidence
    assert "MOUSE" in by["photodynamic / sonodynamic therapy (energy-activated sensitiser)"].canine_hs_evidence


def test_pomalidomide_csf_ratio_was_in_the_cited_paper():
    """Rule 16: the 'missing' number was in PMID 30262659's PK section; the row now carries it,
    with the human within-class contradiction and the dexamethasone-duration correction."""
    m = next(x for x in cu.UNIVERSE if x.name.startswith("targeted protein degradation"))
    assert "19% and 17%" in m.basis
    assert "about the same for POM and LEN" in m.basis
    assert "TWO cycles" in m.basis


def test_every_program_agent_has_a_catalogue_class():
    """Two integrity discrepancies were found on 2026-11-04 (niraparib, dordaviprone): agents in
    the treatment program whose class had no row. This guard makes a third one fail loudly."""
    from canine_dsp import availability_tiers as at
    blob = " ".join((m.name + " " + m.representative).lower() for m in cu.UNIVERSE)
    aliases = {"ribociclib": "cdk4/6"}
    for ag in at.PROGRAM:
        key = ag.name.split()[0].lower().strip("(,")
        assert key in blob or aliases.get(key, "~") in blob, ag.name


def test_registry_and_pipeline_axes_recorded():
    by = {m.name: m for m in cu.UNIVERSE}
    assert "NCT00048373" in by["inflammatory-cytokine blockade (TNF, IL-6)"].basis
    assert "42030266" in by["inflammatory-cytokine blockade (TNF, IL-6)"].canine_hs_evidence
    assert by["mitochondrial-protease activation / OXPHOS collapse (imipridones)"].status is cu.Status.IN_MODEL
    assert "37231193" in by["JAK/STAT inhibition"].canine_hs_evidence
    assert "not fetched" in by["boron neutron capture therapy"].availability_basis


def test_every_formerly_open_class_was_assessed_and_given_a_verdict():
    """2026-11-04: all 28 open classes searched; each is EXCLUDED on a rule-13 ground or a CANDIDATE
    carrying the one measurement that decides it. Nothing is left NOT_ASSESSED."""
    assert cu.not_assessed() == []
    assert set(cu.OPEN_BEFORE_ASSESSMENT_2026_11_04) <= set(cu.ASSESSMENT_2026_11_04)
    for m in cu.UNIVERSE:
        if m.name in cu.ASSESSMENT_2026_11_04:
            assert "ASSESSED 2026-11-04 (PubMed" in m.basis, m.name
            assert m.status in (cu.Status.CANDIDATE, cu.Status.EXCLUDED), m.name
    by = {m.name: m for m in cu.UNIVERSE}
    mdm2 = by["MDM2-p53 interaction inhibition"]
    assert mdm2.status is cu.Status.CANDIDATE and "REVERTED THE SAME DAY" in mdm2.basis
    assert "30852355" in mdm2.basis and "MONOTHERAPY" in mdm2.basis
    fti = by["farnesyltransferase inhibition"]
    assert fti.status is cu.Status.CANDIDATE and "REVERTED THE SAME DAY" in fti.basis
    assert "32212266" in fti.basis and "withdrawn" in fti.basis
    assert "38502052" in by["proteasome inhibition"].basis
    assert "34556593" in by["glucocorticoid-receptor agonists (corticosteroids)"].basis
    assert "36556469" in by["photodynamic / sonodynamic therapy (energy-activated sensitiser)"].basis
    assert "24260303" in by["nucleic-acid therapeutics (antisense oligonucleotide, siRNA)"].basis


def test_deciding_measurement_sweep_covers_every_original_candidate_and_found_ym155():
    assert len(cu.DECIDING_MEASUREMENT_SWEEP_2026_11_04) == 28
    assert all("DH82" in q for _, q in cu.DECIDING_MEASUREMENT_SWEEP_2026_11_04.values())
    m = next(x for x in cu.UNIVERSE if x.name.startswith("survivin suppression"))
    assert m.status is cu.Status.CANDIDATE
    assert "25744435" in m.canine_hs_evidence and "A1" in m.basis


def test_every_candidate_was_independently_verified():
    names = {m.name for m in cu.candidates()}
    assert names <= set(cu.VERIFICATION_2026_11_04)
    for m in cu.candidates():
        assert "VERIFIED 2026-11-04 (independent)" in m.basis, m.name
    by = {m.name: m for m in cu.UNIVERSE}
    assert "36504314" in by["glucocorticoid-receptor agonists (corticosteroids)"].basis
    assert "two years" in by["polyamine-synthesis inhibition (ornithine decarboxylase)"].basis
    assert "five doses" in by["acyclic nucleotide phosphonate prodrugs (rabacfosadine)"].basis
    assert "11026694" in by["boron neutron capture therapy"].basis
    assert by["farnesyltransferase inhibition"].availability is cu.Availability.EXISTS_TODAY
    xpo = by["nuclear export inhibition (XPO1 / SINE compounds)"]
    assert "labelled until progression --" not in xpo.availability_basis
