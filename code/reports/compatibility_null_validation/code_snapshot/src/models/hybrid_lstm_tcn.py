"""
src/models/hybrid_lstm_tcn.py
=============================
Canonical PyTorch implementation of the Hybrid LSTM-TCN Prognostic Architecture.
Directly matches the 20 saved benchmark checkpoints in models / results (115,095 trainable parameters),
Figure 1, and Sections 3.4-3.11 of the manuscript.

Architecture Breakdown (115,095 Trainable Parameters):
  1. SensorAttention: Feature-wise context reweighting (1,202 params)
  2. LSTM Branch: Sequential recursive degradation modeling (21,504 params)
  3. TemporalAttention: Hidden-state attention pooling over time (2,113 params)
  4. TCN Branch: 4-layer dilated causal convolutions (57,056 params)
  5. Global Average Pooling: Summarizes TCN feature maps across time (0 params)
  6. Shared Fusion MLP: Combines LSTM and TCN representations (24,768 params)
  7. Quantile Heads: Three independent 64 -> 32 -> 1 feed-forward heads (6,339 params total)
     - median_head: Primary point RUL estimate q50 (2,113 params)
     - lower_delta_head: Softplus offset for lower quantile q05 = q50 - softplus(delta_l) (2,113 params)
     - upper_delta_head: Softplus offset for upper quantile q95 = q50 + softplus(delta_u) (2,113 params)
  8. Risk Head: Auxiliary near-failure hazard classification logit (2,113 params)
"""

from __future__ import annotations

from typing import Optional, Tuple, Union

import torch
import torch.nn as nn
import torch.nn.functional as F


class Chomp1d(nn.Module):
    """Trims causal convolution padding from sequence end."""

    def __init__(self, chomp_size: int) -> None:
        super().__init__()
        self.chomp_size = chomp_size

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if self.chomp_size == 0:
            return x
        return x[:, :, :-self.chomp_size]


class TemporalBlock(nn.Module):
    """
    Residual dilated causal convolutional block for TCN (Section 3.6).
    Two 1D dilated convolutions with chomp, ReLU, and dropout.
    """

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        kernel_size: int = 3,
        dilation: int = 1,
        dropout: float = 0.15,
    ) -> None:
        super().__init__()
        padding = (kernel_size - 1) * dilation

        self.conv1 = nn.Conv1d(
            in_channels,
            out_channels,
            kernel_size,
            padding=padding,
            dilation=dilation,
        )
        self.chomp1 = Chomp1d(padding)
        self.relu1 = nn.ReLU()
        self.dropout1 = nn.Dropout(dropout)

        self.conv2 = nn.Conv1d(
            out_channels,
            out_channels,
            kernel_size,
            padding=padding,
            dilation=dilation,
        )
        self.chomp2 = Chomp1d(padding)
        self.relu2 = nn.ReLU()
        self.dropout2 = nn.Dropout(dropout)

        self.downsample = (
            nn.Conv1d(in_channels, out_channels, kernel_size=1)
            if in_channels != out_channels
            else None
        )
        self.final_relu = nn.ReLU()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out = self.conv1(x)
        out = self.chomp1(out)
        out = self.relu1(out)
        out = self.dropout1(out)

        out = self.conv2(out)
        out = self.chomp2(out)
        out = self.relu2(out)
        out = self.dropout2(out)

        residual = x if self.downsample is None else self.downsample(x)
        return self.final_relu(out + residual)


class SensorAttention(nn.Module):
    """
    Sensor attention module (Section 3.4).
    Averages across the temporal dimension to form global context vector c,
    then computes feature weights via a 2-layer MLP with Sigmoid activation.
    """

    def __init__(self, num_features: int = 18, hidden_size: int = 32) -> None:
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(num_features, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, num_features),
            nn.Sigmoid(),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (B, W=30, d=18)
        context = x.mean(dim=1)  # (B, 18)
        weights = self.network(context)  # (B, 18)
        return x * weights.unsqueeze(1)


class TemporalAttention(nn.Module):
    """
    Temporal attention module over recurrent hidden states (Section 3.7).
    Computes an unnormalized alignment score for each time step and
    aggregates via softmax-weighted sum.
    """

    def __init__(self, hidden_size: int = 64, attention_dim: int = 32) -> None:
        super().__init__()
        self.score = nn.Sequential(
            nn.Linear(hidden_size, attention_dim),
            nn.Tanh(),
            nn.Linear(attention_dim, 1),
        )

    def forward(self, sequence: torch.Tensor) -> torch.Tensor:
        # sequence: (B, W=30, H=64)
        scores = self.score(sequence).squeeze(-1)  # (B, 30)
        weights = torch.softmax(scores, dim=1)  # (B, 30)
        return torch.sum(sequence * weights.unsqueeze(-1), dim=1)  # (B, 64)


class OrderedQuantileHeads(nn.Module):
    """
    Ordered quantile regression heads with softplus offsets (Section 3.9).
    Wraps median_head, lower_delta_head, and upper_delta_head.
    Guarantees non-crossing quantiles: q05 <= q50 <= q95 strictly for all inputs.
    """

    def __init__(self, in_features: int = 64, hidden_dim: int = 32) -> None:
        super().__init__()
        self.median_head = nn.Sequential(
            nn.Linear(in_features, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )
        self.lower_delta_head = nn.Sequential(
            nn.Linear(in_features, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )
        self.upper_delta_head = nn.Sequential(
            nn.Linear(in_features, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        q50 = self.median_head(x)
        lower_delta = F.softplus(self.lower_delta_head(x))
        upper_delta = F.softplus(self.upper_delta_head(x))
        q05 = q50 - lower_delta
        q95 = q50 + upper_delta
        return torch.cat([q05, q50, q95], dim=-1)


class HybridLSTMTCNPrognostic(nn.Module):
    """
    Canonical Multi-Task Hybrid LSTM-TCN Prognostic Architecture.
    Exact layer hierarchy and parameter names matching the 20 benchmark checkpoints:
      - sensor_attention (1,202 params)
      - lstm (21,504 params)
      - temporal_attention (2,113 params)
      - tcn: 4 blocks [18->32, 32->32, 32->64, 64->64] (57,056 params)
      - fusion: MLP(128 -> 128 -> 64) (24,768 params)
      - median_head: MLP(64 -> 32 -> 1) (2,113 params)
      - lower_delta_head: MLP(64 -> 32 -> 1) (2,113 params)
      - upper_delta_head: MLP(64 -> 32 -> 1) (2,113 params)
      - risk_head: MLP(64 -> 32 -> 1) (2,113 params)
    Total parameters: exactly 115,095.
    """

    def __init__(
        self,
        input_size: int = 18,
        lstm_hidden: int = 64,
        dropout: float = 0.20,
    ) -> None:
        super().__init__()

        # 1. Sensor Attention
        self.sensor_attention = SensorAttention(
            num_features=input_size, hidden_size=32
        )

        # 2. LSTM Branch
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=lstm_hidden,
            batch_first=True,
        )

        # 3. Temporal Attention over LSTM sequence
        self.temporal_attention = TemporalAttention(
            hidden_size=lstm_hidden, attention_dim=32
        )

        # 4. TCN Branch (dilations: 1, 2, 4, 8)
        self.tcn = nn.Sequential(
            TemporalBlock(input_size, 32, kernel_size=3, dilation=1, dropout=0.15),
            TemporalBlock(32, 32, kernel_size=3, dilation=2, dropout=0.15),
            TemporalBlock(32, 64, kernel_size=3, dilation=4, dropout=0.15),
            TemporalBlock(64, 64, kernel_size=3, dilation=8, dropout=0.15),
        )

        # 5. Shared Fusion MLP (128 -> 128 -> 64)
        self.fusion = nn.Sequential(
            nn.Linear(lstm_hidden + 64, 128),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(128, 64),
            nn.ReLU(),
        )

        # 6. Quantile Regression Heads
        self.median_head = nn.Sequential(
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
        )
        self.lower_delta_head = nn.Sequential(
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
        )
        self.upper_delta_head = nn.Sequential(
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
        )

        # 7. Auxiliary Risk Classification Head
        self.risk_head = nn.Sequential(
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
        )

    def forward(
        self,
        x: torch.Tensor,
        return_stacked: bool = False,
    ) -> Union[
        Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor],
        Tuple[torch.Tensor, torch.Tensor, torch.Tensor],
    ]:
        """
        Forward pass.

        Parameters
        ----------
        x : torch.Tensor of shape (B, 30, 18)
        return_stacked : bool, default False
            If True, returns (quantiles_stacked, risk_logit, risk_prob)
            where quantiles_stacked is (B, 3) [q05, q50, q95].
            If False (canonical), returns (q05, q50, q95, risk_logit).
        """
        # Sensor Attention
        x_att = self.sensor_attention(x)

        # LSTM Branch & Temporal Attention
        lstm_seq, _ = self.lstm(x_att)
        lstm_context = self.temporal_attention(lstm_seq)  # (B, 64)

        # TCN Branch with Global Average Pooling (Section 3.6)
        tcn_out = self.tcn(x_att.transpose(1, 2))  # (B, 64, 30)
        tcn_context = tcn_out.mean(dim=2)  # Global average temporal pooling -> (B, 64)

        # Fusion MLP
        fused = self.fusion(torch.cat([lstm_context, tcn_context], dim=1))  # (B, 64)

        # Quantile estimates
        q50 = self.median_head(fused)
        lower_delta = F.softplus(self.lower_delta_head(fused))
        upper_delta = F.softplus(self.upper_delta_head(fused))
        q05 = q50 - lower_delta
        q95 = q50 + upper_delta

        # Near-failure risk logit
        risk_logit = self.risk_head(fused)

        if return_stacked:
            quantiles = torch.cat([q05, q50, q95], dim=-1)
            risk_prob = torch.sigmoid(risk_logit)
            return quantiles, risk_logit, risk_prob

        return q05, q50, q95, risk_logit

    def get_parameter_breakdown(self) -> dict[str, int]:
        """Return exact parameter counts per component module."""
        modules = {
            "sensor_attention": self.sensor_attention,
            "lstm": self.lstm,
            "temporal_attention": self.temporal_attention,
            "tcn": self.tcn,
            "fusion": self.fusion,
            "median_head": self.median_head,
            "lower_delta_head": self.lower_delta_head,
            "upper_delta_head": self.upper_delta_head,
            "risk_head": self.risk_head,
        }
        return {name: sum(p.numel() for p in mod.parameters()) for name, mod in modules.items()}


class NearFailureRiskHead(nn.Module):
    """Near-failure hazard classification head (Section 3.10)."""

    def __init__(self, in_features: int = 64, hidden_dim: int = 32) -> None:
        super().__init__()
        self.head = nn.Sequential(
            nn.Linear(in_features, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        logit = self.head(x)
        return logit, torch.sigmoid(logit)


class TemporalConvolutionalNetwork(nn.Module):
    """4-layer dilated Temporal Convolutional Network (Section 3.6)."""

    def __init__(
        self,
        in_channels: int = 18,
        channels: Tuple[int, ...] = (32, 32, 64, 64),
        kernel_size: int = 3,
        dilations: Tuple[int, ...] = (1, 2, 4, 8),
        dropout: float = 0.15,
    ) -> None:
        super().__init__()
        layers = []
        for i in range(len(channels)):
            c_in = in_channels if i == 0 else channels[i - 1]
            c_out = channels[i]
            d = dilations[i]
            layers.append(
                TemporalBlock(c_in, c_out, kernel_size=kernel_size, dilation=d, dropout=dropout)
            )
        self.network = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)


# Alias for backward compatibility with checkpoint scripts
FinalRULModel = HybridLSTMTCNPrognostic
