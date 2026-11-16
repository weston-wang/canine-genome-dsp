"""Sanity + fidelity checks for the conversation-sourced therapies catalogue."""

from __future__ import annotations

from canine_dsp import therapies as t


def test_module_imports_and_is_documented():
    assert t.__doc__ and len(t.__doc__) > 100


def test_catalogue_is_populated_and_well_typed():
    assert len(t.THERAPIES) >= 50
    for x in t.THERAPIES:
        assert isinstance(x, t.Therapy)
        assert x.name.strip()
        assert isinstance(x.therapy_class, t.TherapyClass)
        assert isinstance(x.verdict, t.Verdict)
        assert x.mechanism.strip()
        assert x.status.strip()


def test_hsa_era_content_was_scrubbed():
    """The parent goal deletes the early hemangiosarcoma exploration; no HSA-era bucket survives."""
    assert "HSA_ERA" not in t.TherapyClass.__members__
    assert "HSA_ERA" not in t.Verdict.__members__
    # None of the purely-HSA agents should remain as catalogued therapies.
    names = " ".join(x.name.lower() for x in t.THERAPIES)
    for gone in ("ebat", "evim", "erstreps", "yunnan", "propranolol"):
        assert gone not in names, gone


def test_by_class_and_by_verdict_partition_the_catalogue():
    assert sum(len(v) for v in t.by_class().values()) == len(t.THERAPIES)
    assert sum(len(v) for v in t.by_verdict().values()) == len(t.THERAPIES)


def test_current_answer_is_the_live_induction_regimen():
    live = t.current_answer()
    assert live, "there must be a live regimen"
    joined = " ".join(x.name.lower() for x in live)
    # the load-bearing microtubule agent and the PI3K partner are in the live answer
    assert "lisavanbulin" in joined
    assert "paxalisib" in joined


def test_find_locates_a_named_agent():
    hits = t.find("paxalisib")
    assert hits and any("paxalisib" in x.name.lower() for x in hits)


def test_current_answer_regimen_is_declared_not_curative():
    reg = t.CURRENT_ANSWER_REGIMEN
    assert "induction" in reg and "maintenance" in reg
    # the conversation was explicit that the regimen is not curative
    assert reg.get("curative") in (False, "no", "No") or "not curative" in str(reg).lower()


def test_retractions_are_preserved_as_a_verdict_bucket():
    """The catalogue must keep withdrawn claims labelled, not silently drop them."""
    assert "RETRACTED" in t.Verdict.__members__
    assert any(x.verdict is t.Verdict.RETRACTED for x in t.THERAPIES)
