"""Sanity + fidelity checks for the conversation-sourced presentation module.

The load-bearing check here is the breed-name guard: the module must summarise the
breed's disease without ever naming the breed.
"""

from __future__ import annotations

import re
from pathlib import Path

from canine_dsp import presentation as p


def test_module_imports_and_is_documented():
    assert p.__doc__ and len(p.__doc__) > 100


def test_the_breed_is_never_named():
    """Explicit user constraint: summarise the breed's HS without naming the breed."""
    source = Path(p.__file__).read_text()
    for token in ("corgi", "pembroke", "welsh", "pwc"):
        assert not re.search(rf"\b{token}\b", source, re.IGNORECASE), token


def test_facts_are_populated_and_carry_evidence_status():
    facts = p.all_facts()
    assert len(facts) >= 20
    for f in facts:
        assert f.statement.strip()
        assert isinstance(f.status, p.EvidenceStatus)


def test_facts_by_status_partitions_all_facts():
    total = sum(len(p.facts_by_status(s)) for s in p.EvidenceStatus)
    assert total == len(p.all_facts())


def test_provenance_frames_this_as_analysis_not_advice():
    assert "not veterinary" in p.PROVENANCE.lower()


def test_genomic_uniqueness_records_the_key_lesions_and_the_mapk_majority():
    genomic = " ".join(f.statement for f in p.GENOMIC_UNIQUENESS).upper()
    assert "MTAP" in genomic or "CDKN2A" in genomic
    # the MAPK majority (PTPN11/SHP2 + KRAS) is the dominant extrapolated driver class
    genes = {c.gene.upper() for c in p.CANDIDATE_SOMATIC_DRIVERS}
    assert "PTPN11" in genes or "KRAS" in genes


def test_contrast_breeds_are_present_and_may_be_named():
    """Other breeds are allowed to be named; the constraint is only about the subject breed."""
    assert len(p.CONTRAST_BREEDS) >= 1


def test_corrections_and_open_questions_are_kept():
    assert p.CORRECTIONS_AND_RETRACTIONS
    assert p.OPEN_QUESTIONS
