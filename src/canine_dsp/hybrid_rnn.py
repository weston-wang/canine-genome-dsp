"""Tiny recurrent residual model layered on cross-fitted Volterra predictions."""

from dataclasses import dataclass

import numpy as np
import pandas as pd
import torch
from torch import nn


class ResidualGRU(nn.Module):
    def __init__(self, inputs: int, outputs: int, hidden: int = 6):
        super().__init__()
        self.gru = nn.GRU(inputs, hidden, batch_first=True)
        self.output = nn.Linear(hidden, outputs)

    def forward(self, x):
        values, _ = self.gru(x)
        return self.output(values)


@dataclass
class SequenceBatch:
    x: torch.Tensor
    y: torch.Tensor
    mask: torch.Tensor
    keys: list[tuple[str, str]]
    indices: list[list[str]]


def _sequences(table: pd.DataFrame, residuals: pd.DataFrame, modules: list[str],
               subjects: set[str]) -> SequenceBatch:
    rows, targets, masks, keys, indices = [], [], [], [], []
    groups = table[table.subject.astype(str).isin(subjects)].groupby(["subject", "phase"])
    max_len = max(len(group) for _, group in groups)
    for (subject, phase), group in groups:
        group = group.sort_values("day")
        memory = [float(group.iloc[0].get(f"memory_{module}", 0)) for module in modules]
        day = group.day.to_numpy(float)
        x = np.column_stack([day / max(1, table.day.max()), np.sin(day / 2), np.cos(day / 2),
                             np.full(len(day), phase == "boost"),
                             np.tile(memory, (len(day), 1))])
        y = residuals.loc[group.index, modules].to_numpy(float)
        pad = max_len - len(group)
        rows.append(np.pad(x, ((0, pad), (0, 0))))
        targets.append(np.pad(y, ((0, pad), (0, 0))))
        masks.append(np.r_[np.ones(len(group)), np.zeros(pad)])
        keys.append((str(subject), str(phase))); indices.append(group.index.astype(str).tolist())
    return SequenceBatch(torch.tensor(np.stack(rows), dtype=torch.float32),
                         torch.tensor(np.stack(targets), dtype=torch.float32),
                         torch.tensor(np.stack(masks), dtype=torch.float32), keys, indices)


def crossvalidated_hybrid(table: pd.DataFrame, base_predictions: pd.DataFrame,
                          modules: list[str], seeds: tuple[int, ...] = (7, 19, 31),
                          hidden: int = 6, epochs: int = 160) -> tuple[pd.DataFrame, dict]:
    """Add GRU residual predictions without allowing subject leakage."""
    base = base_predictions.pivot(index="sample", columns="module", values="predicted").reindex(table.index)
    observed = table[modules]
    residuals = observed - base
    subjects = table.subject.astype(str).unique()
    collected = []
    parameter_count = None
    for held_out in subjects:
        train_subjects = set(subjects) - {held_out}
        train = _sequences(table, residuals, modules, train_subjects)
        test = _sequences(table, residuals, modules, {held_out})
        fold_predictions = []
        for seed in seeds:
            torch.manual_seed(seed); np.random.seed(seed)
            model = ResidualGRU(train.x.shape[-1], len(modules), hidden)
            parameter_count = sum(parameter.numel() for parameter in model.parameters())
            optimizer = torch.optim.AdamW(model.parameters(), lr=.015, weight_decay=.03)
            for _ in range(epochs):
                optimizer.zero_grad()
                estimate = model(train.x)
                loss = (((estimate - train.y) ** 2) * train.mask[..., None]).sum() / train.mask.sum()
                loss.backward(); optimizer.step()
            with torch.no_grad(): fold_predictions.append(model(test.x).numpy())
        mean = np.mean(fold_predictions, axis=0); sd = np.std(fold_predictions, axis=0)
        for sequence, sample_ids in enumerate(test.indices):
            for position, sample in enumerate(sample_ids):
                for channel, module in enumerate(modules):
                    collected.append({"sample": sample, "subject": held_out, "module": module,
                                      "phase": table.at[sample, "phase"], "day": int(table.at[sample, "day"]),
                                      "observed": float(table.at[sample, module]),
                                      "volterra_predicted": float(base.at[sample, module]),
                                      "predicted": float(base.at[sample, module] + mean[sequence, position, channel]),
                                      "rnn_residual": float(mean[sequence, position, channel]),
                                      "seed_sd": float(sd[sequence, position, channel])})
    return pd.DataFrame(collected), {"architecture": "GRU residual over cross-fitted Volterra",
                                      "hidden_units": hidden, "seeds": list(seeds),
                                      "parameters": parameter_count, "epochs": epochs}

