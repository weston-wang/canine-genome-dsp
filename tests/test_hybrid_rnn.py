import torch

from canine_dsp.hybrid_rnn import ResidualGRU


def test_tiny_gru_preserves_sequence_and_output_dimensions():
    model = ResidualGRU(inputs=7, outputs=3, hidden=4)
    result = model(torch.zeros(2, 9, 7))
    assert result.shape == (2, 9, 3)
    assert sum(parameter.numel() for parameter in model.parameters()) < 500
