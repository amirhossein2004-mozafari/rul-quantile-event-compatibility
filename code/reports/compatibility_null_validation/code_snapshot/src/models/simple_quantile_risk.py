"""Smaller complete-output baselines for the fixed stage-9 architecture comparison."""
import torch
from torch import nn
from torch.nn import functional as F

from src.models.hybrid_lstm_tcn import HybridLSTMTCNPrognostic, TemporalBlock


class QuantileRiskBase(nn.Module):
    def __init__(self):
        super().__init__()
        self.fusion = nn.Sequential(nn.Linear(64, 64), nn.ReLU(), nn.Dropout(.2))
        for name in ('median_head', 'lower_delta_head', 'upper_delta_head', 'risk_head'):
            setattr(self, name, nn.Sequential(nn.Linear(64, 32), nn.ReLU(), nn.Linear(32, 1)))

    def forward(self, x, return_stacked=False):
        feature = self.fusion(self.encode(x))
        median = self.median_head(feature)
        lower = median-F.softplus(self.lower_delta_head(feature))
        upper = median+F.softplus(self.upper_delta_head(feature))
        logit = self.risk_head(feature)
        if return_stacked:
            return torch.cat([lower, median, upper], dim=1), logit, torch.sigmoid(logit)
        return lower, median, upper, logit


class LSTMQuantileRisk(QuantileRiskBase):
    """One 64-unit LSTM and the same-capacity quantile/risk heads: 34,116 params."""
    def __init__(self, input_size=18):
        super().__init__()
        self.lstm = nn.LSTM(input_size=input_size, hidden_size=64, batch_first=True)

    def encode(self, x):
        sequence, _ = self.lstm(x)
        return sequence[:, -1, :]


class TCNQuantileRisk(QuantileRiskBase):
    """Canonical four-block TCN with global mean pooling: 69,668 parameters."""
    def __init__(self, input_size=18):
        super().__init__()
        self.tcn = nn.Sequential(*[
            TemporalBlock(in_channels, out_channels, kernel_size=3, dilation=dilation, dropout=.15)
            for in_channels, out_channels, dilation in [(input_size, 32, 1), (32, 32, 2), (32, 64, 4), (64, 64, 8)]
        ])

    def encode(self, x):
        return self.tcn(x.transpose(1, 2)).mean(dim=2)


PARAMETER_COUNTS = {'lstm': 34116, 'tcn': 69668, 'hybrid': 115095}


def make_model(name):
    constructors = {'lstm': LSTMQuantileRisk, 'tcn': TCNQuantileRisk, 'hybrid': HybridLSTMTCNPrognostic}
    if name not in constructors:
        raise ValueError(f'Unknown baseline model: {name}')
    model = constructors[name]()
    actual = sum(p.numel() for p in model.parameters())
    if actual != PARAMETER_COUNTS[name]:
        raise ValueError(f'Unexpected parameter count for {name}: {actual}')
    return model
