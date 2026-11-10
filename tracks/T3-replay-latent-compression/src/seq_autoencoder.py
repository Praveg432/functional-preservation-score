"""T3 sequence autoencoder with a quantized (bits-per-event) latent.

Goal: compress a population run/replay sequence (n_units x n_bins) into a small latent code,
then reconstruct, and measure how few bits the latent can use before the represented trajectory
(decoded) breaks. The research question is the bits-per-event FLOOR, so we use an interpretable
linear latent with EXPLICIT quantization rather than a black-box deep net:

  encode : flatten sequence -> project onto top-k PCA components (fit across all sequences)
  quantize: scalar-quantize each latent coord to `bits` bits (per-coordinate min/max range)
  decode : inverse-project -> reshape to (n_units, n_bins), clip to >=0 (counts)

bits_per_event = latent_dim * bits   (the compression budget).

This is deterministic and fast; a deep VQ-AE is a drop-in future upgrade behind the same
encode/decode contract. The contribution is the measured fidelity-vs-bits frontier, not the
fanciness of the encoder.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class SeqAutoencoder:
    mean: np.ndarray          # (D,) flattened-sequence mean
    components: np.ndarray    # (k, D) PCA basis
    shape: tuple              # (n_units, n_bins)
    coord_min: np.ndarray     # (k,) per-coord quantization range
    coord_max: np.ndarray

    @property
    def latent_dim(self) -> int:
        return self.components.shape[0]

    @classmethod
    def fit(cls, seqs: list[np.ndarray], latent_dim: int) -> "SeqAutoencoder":
        shape = seqs[0].shape
        X = np.stack([s.ravel().astype(float) for s in seqs])     # (N, D)
        mean = X.mean(axis=0)
        Xc = X - mean
        # PCA via SVD
        U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
        k = min(latent_dim, Vt.shape[0])
        comp = Vt[:k]                                              # (k, D)
        codes = Xc @ comp.T                                        # (N, k)
        return cls(mean=mean, components=comp, shape=shape,
                   coord_min=codes.min(axis=0), coord_max=codes.max(axis=0))

    def encode(self, seq: np.ndarray) -> np.ndarray:
        return (seq.ravel().astype(float) - self.mean) @ self.components.T

    def quantize(self, code: np.ndarray, bits: int) -> np.ndarray:
        if bits >= 32:
            return code
        levels = max(1, 2 ** bits - 1)
        lo, hi = self.coord_min, self.coord_max
        rng = np.where(hi - lo > 1e-9, hi - lo, 1.0)
        q = np.round((code - lo) / rng * levels)
        return q / levels * rng + lo

    def decode(self, code: np.ndarray) -> np.ndarray:
        flat = code @ self.components + self.mean
        return np.clip(flat.reshape(self.shape), 0.0, None)

    def reconstruct(self, seq: np.ndarray, bits: int) -> np.ndarray:
        return self.decode(self.quantize(self.encode(seq), bits))

    def bits_per_event(self, bits: int) -> int:
        return self.latent_dim * (bits if bits < 32 else 32)
