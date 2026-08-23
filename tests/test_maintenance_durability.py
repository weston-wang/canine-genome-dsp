from canine_dsp import maintenance_durability as md


def _by_genotype(name):
    return next(t for t in md.TIERS if t.genotype.startswith(name))


def _verdict(genotype_prefix, site_name):
    tier = _by_genotype(genotype_prefix)
    site = next(s for s in md.SITES if s.name == site_name)
    return md.durability(tier, site).verdict


def test_mtap_is_durable_at_reachable_sites():
    for site in ("Lung / disseminated",
                 "Brain -- local delivery (cavity implant / CED / SRS)",
                 "Brain -- systemic penetration"):
        assert _verdict("MTAP", site) is md.Verdict.DURABLE_10Y


def test_csf_is_addressed_but_durability_unquantified():
    """CSF is not 'unexplored' -- it is reached (craniospinal radiation + intrathecal + immune) but
    its durability figure is deliberately withheld. The verdict must say so, not read as a blank."""
    assert _verdict("MTAP", "Leptomeninges / CSF") is md.Verdict.LOCAL_UNQUANTIFIED
    a = md.csf_answer()
    assert a["reached"] is True
    assert a["why_no_durability_number"]  # the specific reasons are enumerated
    assert "retracted" in " ".join(a["why_no_durability_number"]).lower()  # the 470x headline
    # better-quantified: a computed cell-level concentration bar per drug, and it is low
    q = a["quantified_threshold"]
    assert q["tng908"]["cell_concentration_to_close_nM"] < 5
    assert q["cobimetinib"]["cell_concentration_to_close_nM"] < 100


def test_mapk_majority_is_never_locked():
    """The ~59% MAPK tier is surveillance-dependent everywhere reachable -- never a locked decade,
    because a pathway target reroutes even though its derived margin is positive."""
    for d in md.grid():
        if d.tier.genotype.startswith("MAPK"):
            assert d.verdict in (md.Verdict.SURVEILLANCE_DEPENDENT, md.Verdict.LOCAL_UNQUANTIFIED)
            assert d.verdict is not md.Verdict.DURABLE_10Y


def test_csf_is_never_given_a_quantified_durability_number():
    for d in md.grid():
        if d.site.name.startswith("Leptomeninges"):
            assert d.verdict is md.Verdict.LOCAL_UNQUANTIFIED
            assert d.margin is None
            # addressed for coverage, but not a quantified continuous-maintenance hold
            assert d.suppresses_second_primary_at_emergence is False


def test_every_combination_resolves_to_an_anchor():
    """Resolution on ALL combinations: every marker set -- empty, single, or co-occurring -- routes
    to exactly one matched anchor with a real verdict. Nothing is left unresolved."""
    for _label, d in md.full_resolution():
        assert d.verdict in (md.Verdict.DURABLE_10Y, md.Verdict.SURVEILLANCE_DEPENDENT,
                             md.Verdict.DEPENDENCY_HOLD, md.Verdict.FLOOR)
        assert d.tier.maintenance  # a concrete matched pill/strategy


def test_every_reachable_combination_suppresses_at_emergence():
    """The repo's maintenance-at-emergence verdict: every genotype's matched anchor suppresses a
    fresh second primary at emergence -- not an MTAP-only property. Only unreachable sites (CSF) or
    a negative margin make it False. The grade below is robustness, not whether it works."""
    for _label, d in md.full_resolution():
        assert d.suppresses_second_primary_at_emergence is True
    # and it stays True across reachable sites in the grid
    for dd in md.grid():
        if dd.site.access is not None and dd.verdict is not md.Verdict.FAILS:
            assert dd.suppresses_second_primary_at_emergence is True
    # CSF (unreachable) is the honest False
    csf = [dd for dd in md.grid() if dd.site.name.startswith("Leptomeninges")]
    assert csf and all(not dd.suppresses_second_primary_at_emergence for dd in csf)


def test_co_occurring_markers_route_to_the_strongest_anchor():
    """A tumour with BOTH an MTAP deletion and a SHP2 driver is routed to the MTAP (locked) anchor,
    not the MAPK one -- the priority tree picks the best anchor a tumour qualifies for."""
    lung = md.SITES[0]
    d = md.resolve({"MTAP_del", "SHP2"}, lung)
    assert d.tier.genotype == "MTAP deleted"
    assert d.verdict is md.Verdict.DURABLE_10Y


def test_dependency_and_floor_tiers_still_resolve_without_pkpd():
    """No measured IC50+Cmax -> still resolved (dependency/floor grade from the genotype tree),
    never left as an unresolved gap."""
    for d in md.grid():
        if d.site.access is None:
            continue
        if d.tier.lock is md.Lock.DEPENDENCY:
            assert d.verdict is md.Verdict.DEPENDENCY_HOLD
        if d.tier.lock is md.Lock.FLOOR:
            assert d.verdict is md.Verdict.FLOOR


def test_only_mtap_reaches_a_locked_decade():
    durable = md.durable_scenarios()
    assert durable  # non-empty
    assert {d.tier.genotype for d in durable} == {"MTAP deleted"}


def test_the_model_can_fail_at_low_access():
    """Integrity: below the drug's min access to close, the derived margin goes negative and the
    verdict must be FAILS -- the model is not rigged to always pass."""
    mapk = _by_genotype("MAPK")
    starved = md.Site("test -- starved access", 0.02)  # below cobimetinib's ~0.041 threshold
    d = md.durability(mapk, starved)
    assert d.margin is not None and d.margin <= 0
    assert d.verdict is md.Verdict.FAILS


def test_reconciliation_shows_lock_is_decisive():
    r = md.reconciliation()
    # the old hand-set model implied a ~0.37 access threshold; the derived one is far lower
    assert r["old_access_threshold_approx"] > 0.3
    assert r["derived_min_access_MTAP_tng908"] < 0.05
    assert "lock" in r["decisive_condition"].lower()


def test_headline_leads_with_all_combinations_and_stays_honest():
    h = md.headline().lower()
    # leads with the breed-wide suppression-at-emergence result, framed as robustness not yes/no
    assert "all genotype combinations" in h
    assert "at emergence" in h
    assert "robustness" in h
    # still honest about the one gap and the model-based status
    assert "csf" in h
    assert "not yet demonstrated" in h
    # the brain-spread case is now hardened, and surveillance is made precise
    assert "hardened" in h
    assert "tng456" in h


def test_brain_spread_is_hardened_and_hands_residual_to_csf():
    """The brain-spread answer names the old weak point (TNG908 CNS failure), replaces it with a
    brain-penetrant successor, backs it with demonstrated radiation control, and narrows the residual
    to the CSF compartment -- not the brain parenchyma."""
    a = md.brain_spread_answer()
    assert "tng908" in a["was_the_weak_point"].lower()
    assert "failed" in a["was_the_weak_point"].lower()
    # pillar 1: a brain-penetrant successor keeps the genotype lock at the brain site
    assert "tng456" in a["pillar_1_targeted_drug"].lower()
    # pillar 2: local control is clinically demonstrated (radiation), not modelled
    assert any(w in a["pillar_2_local_control_is_demonstrated"].lower()
               for w in ("radiation", "radiosurgery", "gy"))
    # pillar 3: the failure mode is CSF seeding, handed off to csf_answer()
    assert "csf" in a["pillar_3_failure_mode_named"].lower()
    assert "hardened" in a["verdict"].lower()


def test_surveillance_model_is_precise_about_locked_vs_conditional():
    """'Surveillance-dependent' resolves to a concrete distinction: locked tiers need no watching;
    reroutable tiers run a detect-and-switch loop. MTAP is the only locked tier."""
    sm = md.surveillance_model()
    assert sm["locked_tiers"] == ["MTAP deleted"]
    assert "MAPK driver (SHP2/KRAS)" in sm["reroutable_tiers"]
    assert "MTAP deleted" not in sm["reroutable_tiers"]
    # the loop has all three named components, and detection is grounded in a real modality
    loop = sm["the_loop"]
    assert set(loop) == {"1_detect", "2_switch", "3_cadence"}
    assert "ctdna" in loop["1_detect"].lower()
    # locked needs no watching; reroutable is conditional -- stated in the bottom line
    assert "holds on its own" in sm["bottom_line"].lower()
