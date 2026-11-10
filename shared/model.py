"""Baseline connectome-driven functional model.

The connectome's weighted adjacency *is* the model: we run leaky recurrent rate dynamics on
the graph and read out motor-neuron activity. This gives a deterministic input -> output
"function" that compression / transport / ablation can be scored against via FPS.

Dynamics (discrete leaky-integrator rate network):
    x[t+1] = (1 - leak) * x[t] + leak * phi( W^T x[t] + B_in @ u[t] + bias )
    y[t]   = x[t][motor_idx]

where phi = tanh. W^T because W[i, j] is i -> j, so presynaptic i drives postsynaptic j via
column j. The model is pure numpy (N ~ 300 runs in milliseconds, fully reproducible).

This is intentionally simple: the research question is about *preservation of function under
graph operations*, not about state-of-the-art dynamics. A richer LIF/GNN model is a drop-in
replacement behind the same `run()` contract.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .connectome import Connectome, MOTOR, SENSORY


@dataclass
class ConnectomeModel:
    W: np.ndarray            # (N, N) i -> j weights
    sensory_idx: np.ndarray  # input sites
    motor_idx: np.ndarray    # readout sites
    leak: float = 0.3
    gain: float = 1.0
    bias: float = 0.0

    @classmethod
    def from_connectome(cls, c: Connectome, leak: float = 0.3, gain: float = 1.0) -> "ConnectomeModel":
        return cls(
            W=c.W.copy(),
            sensory_idx=np.where(c.roles == SENSORY)[0],
            motor_idx=np.where(c.roles == MOTOR)[0],
            leak=leak,
            gain=gain,
        )

    def with_weights(self, W: np.ndarray) -> "ConnectomeModel":
        """Return a copy with a different weight matrix (same I/O wiring)."""
        return ConnectomeModel(
            W=W, sensory_idx=self.sensory_idx, motor_idx=self.motor_idx,
            leak=self.leak, gain=self.gain, bias=self.bias,
        )

    def run(self, u: np.ndarray, steps: int | None = None) -> np.ndarray:
        """Run dynamics on input sequence u.

        Args:
            u: (T, n_sensory) input drive sequence.
        Returns:
            y: (T, n_motor) motor readout sequence.
        """
        n = self.W.shape[0]
        T = u.shape[0] if steps is None else steps
        Wt = self.W.T  # postsynaptic drive: (W^T x)[j] = sum_i W[i,j] x[i]

        B_in = np.zeros((n, len(self.sensory_idx)))
        for k, s in enumerate(self.sensory_idx):
            B_in[s, k] = 1.0

        x = np.zeros(n)
        ys = np.empty((T, len(self.motor_idx)))
        for t in range(T):
            drive = Wt @ x + self.gain * (B_in @ u[t]) + self.bias
            x = (1.0 - self.leak) * x + self.leak * np.tanh(drive)
            ys[t] = x[self.motor_idx]
        return ys


@dataclass
class SigmoidConductanceModel:
    """Independent alternative dynamics for robustness checks (different from ConnectomeModel).

    Differences that make it a genuine robustness test, not a reskin:
      * logistic sigmoid activation in [0, 1] (vs tanh in [-1, 1]);
      * input-normalized (divisive) drive: each postsynaptic node normalizes by its total
        incoming weight, a conductance-style scaling absent from the leaky-rate model;
      * faster integration constant.
    Same `run(u) -> (T, n_motor)` contract, so T1 experiments can swap it in unchanged.
    """
    W: np.ndarray
    sensory_idx: np.ndarray
    motor_idx: np.ndarray
    leak: float = 0.5

    @classmethod
    def from_connectome(cls, c: "Connectome") -> "SigmoidConductanceModel":
        return cls(W=c.W.copy(),
                   sensory_idx=np.where(c.roles == SENSORY)[0],
                   motor_idx=np.where(c.roles == MOTOR)[0])

    def with_weights(self, W: np.ndarray) -> "SigmoidConductanceModel":
        return SigmoidConductanceModel(W=W, sensory_idx=self.sensory_idx,
                                       motor_idx=self.motor_idx, leak=self.leak)

    def run(self, u: np.ndarray, steps: int | None = None) -> np.ndarray:
        n = self.W.shape[0]
        T = u.shape[0] if steps is None else steps
        Wt = self.W.T
        in_tot = np.abs(self.W).sum(axis=0) + 1.0  # divisive conductance normalizer per node
        B_in = np.zeros((n, len(self.sensory_idx)))
        for k, s in enumerate(self.sensory_idx):
            B_in[s, k] = 1.0
        # center activity at 0.5 and keep gain modest so the sigmoid stays in its dynamic
        # range (avoids saturation that would make output stimulus-independent).
        x = np.full(n, 0.5)
        ys = np.empty((T, len(self.motor_idx)))
        for t in range(T):
            rec = (Wt @ (x - 0.5)) / in_tot          # recurrent drive from deviations
            drive = rec + (B_in @ u[t])
            x = (1.0 - self.leak) * x + self.leak * (1.0 / (1.0 + np.exp(-1.5 * drive)))
            ys[t] = x[self.motor_idx] - 0.5          # readout centered (comparable to tanh model)
        return ys


def default_stimulus_bank(n_sensory: int, n_patterns: int = 8, T: int = 40, seed: int = 1) -> np.ndarray:
    """A fixed bank of input sequences used as the 'behavioral battery'.

    Returns (n_patterns, T, n_sensory). Deterministic given seed. Each pattern is a smooth
    random drive (low-pass noise) so the readout reflects network processing, not input noise.
    """
    rng = np.random.default_rng(seed)
    raw = rng.standard_normal((n_patterns, T, n_sensory))
    # low-pass along time for smooth, structured drive
    kernel = np.array([0.25, 0.5, 0.25])
    out = raw.copy()
    for _ in range(3):
        out[:, 1:-1, :] = (
            kernel[0] * out[:, :-2, :] + kernel[1] * out[:, 1:-1, :] + kernel[2] * out[:, 2:, :]
        )
    return out
