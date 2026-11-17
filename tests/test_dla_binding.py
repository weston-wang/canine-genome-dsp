import pytest

from canine_dsp.dla_binding import binding_class, parse_mhci_response

# Real response captured from a live query to IEDB's tools_api/mhci/ endpoint
# (method=netmhcpan_el&sequence_text=DLYGGEKFATLAKLVQYYMEHHGQL&allele=DLA-8803401&length=9),
# used verbatim as a parsing fixture -- not a fabricated/idealized example.
REAL_MHCI_RESPONSE = """allele\tseq_num\tstart\tend\tlength\tpeptide\tcore\ticore\tscore\tpercentile_rank
DLA-8803401\t1\t9\t17\t9\tATLAKLVQY\tATLAKLVQY\tATLAKLVQY\t0.715\t0.05
DLA-8803401\t1\t10\t18\t9\tTLAKLVQYY\tTLAKLVQYY\tTLAKLVQYY\t0.576\t0.11
DLA-8803401\t1\t17\t25\t9\tYYMEHHGQL\tYYMEHHGQL\tYYMEHHGQL\t0.239\t0.64
DLA-8803401\t1\t13\t21\t9\tKLVQYYMEH\tKLVQYYMEH\tKLVQYYMEH\t0.19\t0.86
DLA-8803401\t1\t3\t11\t9\tYGGEKFATL\tYGGEKFATL\tYGGEKFATL\t0.0619\t2.8
"""

REAL_INVALID_ALLELE_RESPONSE = """Invalid allele name DLA-88*508:01 found.

* Please go to the link below for more usage info:
http://tools.iedb.org/main/html/tools_api.html
"""


def test_binding_class_thresholds():
    assert binding_class(0.05) == "strong_binder"
    assert binding_class(0.49) == "strong_binder"
    assert binding_class(0.5) == "weak_binder"
    assert binding_class(1.9) == "weak_binder"
    assert binding_class(2.0) == "no_predicted_binding"
    assert binding_class(50.0) == "no_predicted_binding"


def test_parse_mhci_response_parses_real_captured_output():
    table = parse_mhci_response(REAL_MHCI_RESPONSE)
    assert len(table) == 5
    assert list(table.columns[:2]) == ["allele", "seq_num"]
    assert "binding_class" in table.columns
    strong = table[table["peptide"] == "ATLAKLVQY"].iloc[0]
    assert strong["percentile_rank"] == pytest.approx(0.05)
    assert strong["binding_class"] == "strong_binder"
    weak = table[table["peptide"] == "KLVQYYMEH"].iloc[0]
    assert weak["percentile_rank"] == pytest.approx(0.86)
    assert weak["binding_class"] == "weak_binder"
    no_binding = table[table["peptide"] == "YGGEKFATL"].iloc[0]
    assert no_binding["percentile_rank"] == pytest.approx(2.8)
    assert no_binding["binding_class"] == "no_predicted_binding"


def test_parse_mhci_response_raises_on_error_text():
    with pytest.raises(ValueError):
        parse_mhci_response(REAL_INVALID_ALLELE_RESPONSE)


def test_parse_mhci_response_raises_on_empty_text():
    with pytest.raises(ValueError):
        parse_mhci_response("")
