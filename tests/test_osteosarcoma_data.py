import gzip
import json
import zipfile
from io import BytesIO

import numpy as np
import pandas as pd

from canine_dsp.osteosarcoma_data import prepare_gse76127, read_cos33_clinical


WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def _cell(value):
    return f"<w:tc><w:p><w:r><w:t>{value}</w:t></w:r></w:p></w:tc>"


def _supplement(path):
    header = ["Unique ID", "DFI", "Sex", "Breed", "Tumor Site",
              "Age at Dx (years)", "Chemotherapy treatment"]
    rows = [header]
    for index in range(33):
        rows.append([
            str(100000 + index),
            str(90 + 12 * index),
            "FS" if index % 2 else "MC",
            f"Breed {index % 4}",
            "Radius" if index % 3 else "Humerus",
            str(5 + index / 10),
            "DoxCarbo" if index % 2 else "Carboplatin",
        ])
    xml = (
        f'<w:document xmlns:w="{WORD_NS}"><w:body><w:tbl>'
        + "".join("<w:tr>" + "".join(_cell(value) for value in row) + "</w:tr>"
                  for row in rows)
        + "</w:tbl></w:body></w:document>"
    )
    docx_buffer = BytesIO()
    with zipfile.ZipFile(docx_buffer, "w") as docx:
        docx.writestr("word/document.xml", xml)
    with zipfile.ZipFile(path, "w") as supplements:
        supplements.writestr("12859_2016_942_MOESM4_ESM.docx", docx_buffer.getvalue())


def _series_matrix(path):
    samples = [f"GSM{index:07d}" for index in range(33)]
    lines = [
        "!Sample_title\t" + "\t".join(f'"patient {100000 + index}"'
                                            for index in range(33)) + "\n",
        "!series_matrix_table_begin\n",
        '"ID_REF"\t' + "\t".join(f'"{sample}"' for sample in samples) + "\n",
    ]
    rng = np.random.default_rng(5)
    for probe in range(12):
        values = 5 + rng.normal(size=33) + .02 * np.arange(33) * (probe % 3)
        lines.append(f'"probe_{probe}"\t' + "\t".join(map(str, values)) + "\n")
    lines.append("!series_matrix_table_end\n")
    with gzip.open(path, "wt") as handle:
        handle.writelines(lines)


def test_cos33_supplement_parser_preserves_public_outcomes(tmp_path):
    supplement = tmp_path / "supplements.zip"
    _supplement(supplement)
    table = read_cos33_clinical(supplement)
    assert len(table) == 33
    assert table.patient_id.is_unique
    assert table.dfi_days.min() == 90
    assert table.received_carboplatin.all()
    assert table.received_doxorubicin.sum() == 16


def test_gse76127_preparation_holds_out_entire_dogs_and_fails_closed(tmp_path):
    supplement = tmp_path / "supplements.zip"
    matrix = tmp_path / "series_matrix.txt.gz"
    out = tmp_path / "out"
    _supplement(supplement); _series_matrix(matrix)
    summary = prepare_gse76127(matrix, supplement, out, components=3, seed=4)
    assert summary["dogs"] == 33
    assert summary["held_out_unit"] == "dog"
    assert summary["outcome"] == "dfi_days_as_reported_censoring_status_unavailable"
    assert summary["analysis_type"].startswith("crude_static")
    assert summary["chemotherapy_regimen_counts"] == {
        "Carboplatin": 17,
        "DoxCarbo": 16,
    }
    assert not summary["vaccine_kernel_identifiable"]
    assert not summary["longitudinal_state_transition_identifiable"]
    assert not summary["reported_dfi_binary_endpoint_clinically_valid"]
    assert "reported_dfi_le_180_balanced_accuracy_sensitivity" in summary
    assert "reported_dfi_le_180_roc_auc_sensitivity" in summary
    predictions = pd.read_csv(out / "gse76127_leave_one_dog_out.csv")
    assert len(predictions) == 33
    assert predictions.patient_id.nunique() == 33
    assert {"chemotherapy", "received_carboplatin", "received_doxorubicin"} <= set(
        predictions.columns
    )
    assert {
        "reported_dfi_le_180", "predicted_reported_dfi_le_180"
    } <= set(predictions.columns)
    assert not any("early_relapse" in column for column in predictions.columns)
    saved = json.loads((out / "gse76127_real_data_summary.json").read_text())
    assert saved == summary
