"""Real-data adapters for the comparative osteosarcoma program.

The GSE76127 cohort contains one pretreatment tumor expression profile per dog
and a supplementary table with disease-free interval (DFI).  It can inform a
baseline tumor-emission model, but it has no serial vaccination measurements
and therefore cannot identify Volterra kernels or hidden-state transitions.
"""

from __future__ import annotations

import json
import zipfile
from io import BytesIO
from pathlib import Path
from xml.etree import ElementTree

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.decomposition import PCA
from sklearn.linear_model import Ridge
from sklearn.metrics import balanced_accuracy_score, mean_absolute_error, roc_auc_score
from sklearn.preprocessing import StandardScaler

from .expression import read_geo_series_matrix


COS33_DOCX = "12859_2016_942_MOESM4_ESM.docx"
WORD_NAMESPACE = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def _docx_tables(payload: bytes) -> list[list[list[str]]]:
    """Extract cell text from a DOCX without adding a python-docx dependency."""
    with zipfile.ZipFile(BytesIO(payload)) as archive:
        document = archive.read("word/document.xml")
    root = ElementTree.fromstring(document)
    namespace = {"w": WORD_NAMESPACE}
    tables: list[list[list[str]]] = []
    for table in root.findall(".//w:tbl", namespace):
        rows = []
        for row in table.findall("./w:tr", namespace):
            cells = []
            for cell in row.findall("./w:tc", namespace):
                text = "".join(node.text or "" for node in cell.findall(".//w:t", namespace))
                cells.append(text.strip())
            rows.append(cells)
        tables.append(rows)
    return tables


def read_cos33_clinical(supplementary_zip: str | Path) -> pd.DataFrame:
    """Read the public COS33 clinical table bundled in PMC4759767 supplements."""
    with zipfile.ZipFile(supplementary_zip) as archive:
        tables = _docx_tables(archive.read(COS33_DOCX))
    matching = [table for table in tables if any(
        row and row[0].strip().lower() == "unique id" for row in table)]
    if len(matching) != 1:
        raise ValueError("expected one COS33 sample-information table")
    table = matching[0]
    header_index = next(index for index, row in enumerate(table)
                        if row and row[0].strip().lower() == "unique id")
    header = table[header_index]
    records = [row for row in table[header_index + 1:] if len(row) == len(header)
               and row[0].strip().isdigit()]
    if not records:
        raise ValueError("COS33 clinical table contains no patient rows")
    frame = pd.DataFrame(records, columns=header).rename(columns={
        "Unique ID": "patient_id",
        "DFI": "dfi_days",
        "Sex": "sex",
        "Breed": "breed",
        "Tumor Site": "tumor_site",
        "Age at Dx (years)": "age_years",
        "Chemotherapy treatment": "chemotherapy",
    })
    required = {"patient_id", "dfi_days", "sex", "breed", "tumor_site",
                "age_years", "chemotherapy"}
    if not required.issubset(frame.columns):
        raise ValueError("COS33 clinical table schema has changed")
    frame["patient_id"] = frame.patient_id.astype(str)
    frame["dfi_days"] = pd.to_numeric(frame.dfi_days, errors="raise")
    frame["age_years"] = pd.to_numeric(frame.age_years, errors="coerce")
    frame["chemotherapy"] = frame.chemotherapy.str.strip()
    frame["received_carboplatin"] = frame.chemotherapy.str.contains(
        "carbo", case=False, regex=False)
    frame["received_doxorubicin"] = frame.chemotherapy.str.contains(
        "dox", case=False, regex=False)
    if frame.patient_id.duplicated().any() or len(frame) != 33:
        raise ValueError("expected 33 unique COS33 dogs")
    return frame.sort_values("patient_id").reset_index(drop=True)


def _pca_components(expression: pd.DataFrame, components: int,
                    seed: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    values = expression.T.to_numpy(float)
    variance = values.var(axis=0)
    retained = np.flatnonzero(np.isfinite(variance) & (variance > 1e-12))
    if len(retained) < 2:
        raise ValueError("expression matrix has too few variable probes")
    values = StandardScaler().fit_transform(values[:, retained])
    count = min(components, values.shape[0] - 1, values.shape[1])
    model = PCA(n_components=count, svd_solver="randomized", random_state=seed)
    scores = pd.DataFrame(model.fit_transform(values), index=expression.columns,
                          columns=[f"tumor_pc_{index + 1}" for index in range(count)])
    loadings = pd.DataFrame(model.components_.T, index=expression.index[retained],
                            columns=scores.columns)
    return scores, loadings


def _leave_one_dog_out(expression: pd.DataFrame, metadata: pd.DataFrame,
                       components: int, seed: int,
                       variable_probes: int = 2_000) -> tuple[pd.DataFrame, dict]:
    """Fold-local static expression benchmark for log DFI.

    Probe variance selection, scaling, PCA, and ridge fitting are repeated
    inside every held-out-dog fold, preventing outcome-label leakage in this
    code. The public GEO matrix was cohort-wide preprocessed upstream, so the
    workflow is not end-to-end inductive. This is a crude static sensitivity
    analysis, not a survival model: the supplement does not expose an
    event/censor indicator.
    """
    values = expression.loc[:, metadata.sample_id].T.to_numpy(float)
    target = np.log1p(metadata.dfi_days.to_numpy(float))
    predictions = np.zeros(len(metadata)); baseline = np.zeros(len(metadata))
    for held_out in range(len(metadata)):
        train = np.arange(len(metadata)) != held_out
        variance = values[train].var(axis=0)
        retained = np.flatnonzero(np.isfinite(variance) & (variance > 1e-12))
        if len(retained) > variable_probes:
            order = np.argsort(variance[retained])[-variable_probes:]
            retained = retained[order]
        scaler = StandardScaler().fit(values[train][:, retained])
        train_values = scaler.transform(values[train][:, retained])
        test_values = scaler.transform(values[[held_out]][:, retained])
        count = min(components, train_values.shape[0] - 1, train_values.shape[1])
        pca = PCA(n_components=count, svd_solver="randomized", random_state=seed + held_out)
        train_scores = pca.fit_transform(train_values)
        test_scores = pca.transform(test_values)
        model = Ridge(alpha=10.0).fit(train_scores, target[train])
        predictions[held_out] = model.predict(test_scores)[0]
        baseline[held_out] = np.median(target[train])
    predicted_days = np.expm1(predictions).clip(0)
    baseline_days = np.expm1(baseline).clip(0)
    reported_le_180 = metadata.dfi_days.to_numpy(float) <= 180
    predicted_le_180_score = -predictions
    result = metadata[[
        "sample_id", "patient_id", "dfi_days", "chemotherapy",
        "received_carboplatin", "received_doxorubicin",
    ]].copy()
    result["predicted_dfi_days"] = predicted_days
    result["training_median_dfi_days"] = baseline_days
    result["reported_dfi_le_180"] = reported_le_180
    result["predicted_reported_dfi_le_180"] = predicted_days <= 180
    correlation = spearmanr(metadata.dfi_days, predicted_days).statistic
    metrics = {
        "dogs": int(len(metadata)),
        "held_out_unit": "dog",
        "outcome": "dfi_days_as_reported_censoring_status_unavailable",
        "analysis_type": "crude_static_prognostic_sensitivity_not_survival_analysis",
        "preprocessing_scope": (
            "fold_local_modeling_on_upstream_cohort_preprocessed_geo_matrix"
        ),
        "chemotherapy_regimen_counts": {
            str(name): int(count)
            for name, count in metadata.chemotherapy.fillna("missing").value_counts().items()
        },
        "clinical_covariates_used": [],
        "expression_log_dfi_mae": float(mean_absolute_error(target, predictions)),
        "training_median_log_dfi_mae": float(mean_absolute_error(target, baseline)),
        "expression_dfi_spearman": float(correlation) if np.isfinite(correlation) else None,
        "reported_dfi_le_180_balanced_accuracy_sensitivity": float(
            balanced_accuracy_score(
                reported_le_180, result.predicted_reported_dfi_le_180)),
        "reported_dfi_le_180_roc_auc_sensitivity": float(
            roc_auc_score(reported_le_180, predicted_le_180_score)),
        "reported_dfi_binary_endpoint_clinically_valid": False,
        "vaccine_kernel_identifiable": False,
        "longitudinal_state_transition_identifiable": False,
        "interpretation": (
            "DFI censoring status is unavailable, chemotherapy is heterogeneous, and the GEO "
            "matrix was cohort-wide preprocessed upstream, so this is only a crude "
            "treatment-conditioned static prognostic sensitivity analysis. It "
            "cannot validate vaccine timing, a Volterra kernel, or a counterfactual policy."
        ),
    }
    return result, metrics


def prepare_gse76127(matrix: str | Path, supplementary_zip: str | Path, out: str | Path,
                     components: int = 5, seed: int = 76127) -> dict:
    """Prepare COS33 expression/DFI data and run a held-out-dog static benchmark."""
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    expression, samples = read_geo_series_matrix(matrix)
    clinical = read_cos33_clinical(supplementary_zip)
    titles = samples["title"].astype(str)
    sample_map = pd.DataFrame({"sample_id": samples.index.astype(str),
                               "patient_id": titles.str.extract(r"(\d+)", expand=False)})
    metadata = sample_map.merge(clinical, on="patient_id", how="left", validate="one_to_one")
    if len(metadata) != 33 or metadata.dfi_days.isna().any():
        raise ValueError("GSE76127 samples do not map one-to-one to the COS33 clinical table")
    expression = expression.loc[:, metadata.sample_id]
    scores, loadings = _pca_components(expression, components, seed)
    scores.index.name = "sample_id"
    component_table = metadata.merge(scores.reset_index(), on="sample_id", validate="one_to_one")
    predictions, metrics = _leave_one_dog_out(expression, metadata, components, seed)
    top_rows = []
    for component in loadings.columns:
        ranked = loadings[component].abs().nlargest(20).index
        for probe in ranked:
            top_rows.append({"component": component, "probe_id": probe,
                             "loading": float(loadings.loc[probe, component])})
    metadata.to_csv(out / "gse76127_clinical.csv", index=False)
    component_table.to_csv(out / "gse76127_expression_components.csv", index=False)
    pd.DataFrame(top_rows).to_csv(out / "gse76127_top_component_loadings.csv", index=False)
    predictions.to_csv(out / "gse76127_leave_one_dog_out.csv", index=False)
    (out / "gse76127_real_data_summary.json").write_text(json.dumps(metrics, indent=2) + "\n")
    return metrics
