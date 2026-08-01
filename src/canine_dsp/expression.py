"""Adapters for public expression matrices and longitudinal module construction."""

import gzip
import re
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def read_geo_series_matrix(path: str | Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Read expression and sample annotations from a GEO series-matrix file."""
    path = Path(path)
    opener = gzip.open if path.suffix == ".gz" else open
    metadata: dict[str, list[str]] = {}
    data_lines = []
    in_table = False
    with opener(path, "rt") as handle:
        for line in handle:
            if line.startswith("!series_matrix_table_begin"):
                in_table = True
            elif line.startswith("!series_matrix_table_end"):
                break
            elif in_table:
                data_lines.append(line)
            elif line.startswith("!Sample_"):
                key, values = line.rstrip().split("\t", 1)
                metadata[key[8:]] = [value.strip('"') for value in values.split("\t")]
    from io import StringIO
    expression = pd.read_csv(StringIO("".join(data_lines)), sep="\t", index_col=0)
    expression.columns = [str(column).strip('"') for column in expression.columns]
    expression.index = expression.index.astype(str).str.strip('"')
    samples = pd.DataFrame(metadata, index=expression.columns)
    samples.index.name = "sample_id"
    return expression.apply(pd.to_numeric), samples


def parse_gse9794_time(samples: pd.DataFrame) -> pd.Series:
    """Map GSE9794 titles to days since pacing, using 24 days for its 3-4 week endpoint."""
    title = samples["title"].astype(str)
    mapping = {"Day-0": 0.0, "Day-3": 3.0, "Week-1": 7.0, "Week-2": 14.0,
               "End-stage": 24.0}
    result = pd.Series(np.nan, index=samples.index, name="time_days")
    for label, day in mapping.items():
        result[title.str.contains(label, case=False, regex=False)] = day
    if result.isna().any():
        raise ValueError("unrecognized GSE9794 sample title")
    return result


def collapse_technical_replicates(expression: pd.DataFrame, samples: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Collapse GSE9794 RNA technical replicates, retaining 15 biological samples."""
    titles = samples["title"].astype(str)
    biological = titles.str.replace(r", technical replicate \d+$", "", regex=True)
    collapsed = expression.T.groupby(biological).mean().T
    annotations = samples.assign(biological_sample=biological, time_days=parse_gse9794_time(samples))
    annotations = annotations.groupby("biological_sample", sort=False).first()
    return collapsed, annotations


def pca_modules(expression: pd.DataFrame, n_modules: int = 8) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Create sample-level expression components and gene loadings for small time courses."""
    values = np.log2(np.maximum(expression.T.to_numpy(float), 0) + 1)
    values = StandardScaler().fit_transform(values)
    n_modules = min(n_modules, values.shape[0] - 1, values.shape[1])
    model = PCA(n_components=n_modules).fit(values)
    scores = pd.DataFrame(model.transform(values), index=expression.columns,
                          columns=[f"module_{i + 1}" for i in range(n_modules)])
    loadings = pd.DataFrame(model.components_.T, index=expression.index, columns=scores.columns)
    return scores, loadings


def read_dog10k_aging(expression_path: str | Path, information_path: str | Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Read Dog10K's public ortholog CPM matrix and dog sample information."""
    expression = pd.read_csv(expression_path, sep=None, engine="python", index_col=0)
    information = pd.read_csv(information_path, sep=None, engine="python")
    return expression, information
