"""Functional Preservation Score (FPS) -- the keystone metric.

FPS answers one question in a substrate-agnostic way:

    After an operation X transforms a neural system A into A' (compress / align+transport /
    ablate / install), how much of A's input->output FUNCTION does A' preserve?

Design requirements (from analysis/IMPACT-STRATEGY.md):
  * behaviorally grounded -- scored on OUTPUTS over a fixed stimulus battery, not on weights;
  * normalized to a null -- 1.0 = indistinguishable from the reference; 0.0 = no better than
    a trivial control (shuffled/constant output);
  * bounded and comparable across substrates and operations.

Definition:
    Let Y_ref = reference outputs over the battery (reference system on all stimuli).
    Let Y     = transformed system's outputs on the same stimuli.
    Let Y_null= a trivial control (reference outputs with the stimulus->response mapping
                shuffled, i.e. "right statistics, wrong function").

    raw(Y)  = 1 - ||Y - Y_ref||^2 / ||Y_ref - mean(Y_ref)||^2      (an R^2-style fit)
    FPS     = clip( (raw(Y) - raw(Y_null)) / (1 - raw(Y_null)), 0, 1 )

    FPS = 1  <=> perfectly reproduces reference function.
    FPS = 0  <=> no better than the shuffled-function control.

The null-normalization is what makes FPS a real score rather than a bare error: it quantifies
"how far from trivial" the preservation is, which is exactly the claim every track must defend.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


def _r2_fit(Y: np.ndarray, Y_ref: np.ndarray) -> float:
    """R^2-style agreement of Y with Y_ref (1.0 = exact, 0 = predicts the mean, <0 = worse)."""
    ss_res = float(np.sum((Y - Y_ref) ** 2))
    ss_tot = float(np.sum((Y_ref - Y_ref.mean(axis=0, keepdims=True)) ** 2))
    if ss_tot <= 1e-12:
        return 1.0 if ss_res <= 1e-12 else 0.0
    return 1.0 - ss_res / ss_tot


@dataclass(frozen=True)
class FPSResult:
    fps: float
    raw: float
    raw_null: float
    n_stim: int


class Battery:
    """A fixed stimulus battery + its reference outputs. The scoreboard's 'test set'.

    `run_fn(stimulus) -> output_array` is any callable mapping one stimulus (T, d_in) to an
    output (T, d_out). The battery caches the reference outputs and a shuffled-function null.
    """

    def __init__(self, stimuli: np.ndarray, ref_run_fn, null_seed: int = 7):
        self.stimuli = stimuli  # (P, T, d_in)
        self.Y_ref = np.stack([ref_run_fn(s) for s in stimuli])  # (P, T, d_out)
        # shuffled-function null: reference outputs reassigned to the wrong stimuli.
        rng = np.random.default_rng(null_seed)
        perm = rng.permutation(len(stimuli))
        while len(stimuli) > 1 and np.all(perm == np.arange(len(stimuli))):
            perm = rng.permutation(len(stimuli))
        self.Y_null = self.Y_ref[perm]

    @property
    def n_stim(self) -> int:
        return len(self.stimuli)

    def score(self, run_fn) -> FPSResult:
        """Score a transformed system's run_fn against the cached reference + null."""
        Y = np.stack([run_fn(s) for s in self.stimuli])
        Yf = Y.reshape(-1, Y.shape[-1])
        ref = self.Y_ref.reshape(-1, self.Y_ref.shape[-1])
        null = self.Y_null.reshape(-1, self.Y_null.shape[-1])

        raw = _r2_fit(Yf, ref)
        # Null = the BEST trivial baseline: max of {shuffled-function, predict-the-mean}.
        # This makes FPS=0 mean "no better than any trivial control", not just the shuffle.
        raw_null_shuffle = _r2_fit(null, ref)
        mean_pred = np.broadcast_to(ref.mean(axis=0, keepdims=True), ref.shape)
        raw_null_mean = _r2_fit(mean_pred, ref)  # == 0 by construction of R^2
        raw_null = max(raw_null_shuffle, raw_null_mean)
        denom = 1.0 - raw_null
        fps = 0.0 if denom <= 1e-9 else (raw - raw_null) / denom
        fps = float(np.clip(fps, 0.0, 1.0))
        return FPSResult(fps=fps, raw=float(raw), raw_null=float(raw_null), n_stim=self.n_stim)
