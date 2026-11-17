import pytest

from canine_dsp.uniprot import _select_best


def test_select_best_prefers_reviewed_entries():
    entries = [
        {"entryType": "UniProtKB unreviewed (TrEMBL)", "primaryAccession": "A1",
         "proteinExistence": "1: Evidence at protein level"},
        {"entryType": "UniProtKB reviewed (Swiss-Prot)", "primaryAccession": "P1",
         "proteinExistence": "3: Inferred from homology"},
    ]
    assert _select_best(entries)["primaryAccession"] == "P1"


def test_select_best_prefers_stronger_evidence_among_unreviewed():
    entries = [
        {"entryType": "UniProtKB unreviewed (TrEMBL)", "primaryAccession": "A1",
         "proteinExistence": "3: Inferred from homology"},
        {"entryType": "UniProtKB unreviewed (TrEMBL)", "primaryAccession": "A2",
         "proteinExistence": "2: Evidence at transcript level"},
    ]
    assert _select_best(entries)["primaryAccession"] == "A2"


def test_select_best_raises_on_empty_list():
    with pytest.raises(ValueError):
        _select_best([])
