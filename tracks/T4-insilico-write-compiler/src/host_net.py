"""T4 host network: a fixed-topology rate recurrent net whose EXISTING edges are plastic.

The "write" installs a target input->output function into this host by adjusting only the
weights of edges the host already has (fixed topology = the foreign substrate). New edges are
never created (that is the Peters'-rule / feasibility constraint T2 showed is the binding limit).

Dynamics (leaky rate, tanh), matching the shared connectome model family:
    x[t+1] = (1-leak) x[t] + leak * tanh(W x[t] + W_in u[t])
    y[t]   = W_out x[t]          (W_out fixed, random readout from a motor subset)

Only W (on the fixed topology mask) is plastic. W_in, W_out fixed.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class HostNet:
    W: np.ndarray            # (n, n) recurrent weights (plastic, on fixed mask)
    mask: np.ndarray         # (n, n) bool: which edges EXIST (fixed topology)
    W_in: np.ndarray         # (n, d_in) fixed input projection
    W_out: np.ndarray        # (d_out, n) fixed readout
    leak: float = 0.3

    @classmethod
    def random(cls, n: int, d_in: int, d_out: int, density: float, seed: int = 0) -> "HostNet":
        rng = np.random.default_rng(seed)
        mask = (rng.random((n, n)) < density) & ~np.eye(n, dtype=bool)
        W = rng.standard_normal((n, n)) * 0.1 * mask
        W_in = rng.standard_normal((n, d_in)) * 0.5
        W_out = rng.standard_normal((d_out, n)) * (1.0 / np.sqrt(n))
        return cls(W=W, mask=mask, W_in=W_in, W_out=W_out)

    def copy(self) -> "HostNet":
        return HostNet(W=self.W.copy(), mask=self.mask, W_in=self.W_in, W_out=self.W_out, leak=self.leak)

    def run(self, u: np.ndarray, return_states: bool = False):
        """u: (T, d_in) -> y: (T, d_out). Optionally also return states (T, n)."""
        n = self.W.shape[0]
        T = u.shape[0]
        x = np.zeros(n)
        ys = np.empty((T, self.W_out.shape[0]))
        xs = np.empty((T, n)) if return_states else None
        for t in range(T):
            x = (1 - self.leak) * x + self.leak * np.tanh(self.W @ x + self.W_in @ u[t])
            ys[t] = self.W_out @ x
            if return_states:
                xs[t] = x
        return (ys, xs) if return_states else ys


def make_target_function(n: int, d_in: int, d_out: int, density: float, seed: int):
    """A target is a (different) random recurrent net; its I/O map is what we try to install."""
    tgt = HostNet.random(n, d_in, d_out, density, seed=seed)
    return tgt
