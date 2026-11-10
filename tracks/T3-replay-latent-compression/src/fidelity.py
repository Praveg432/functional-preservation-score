"""T3 fidelity: Bayesian-decode reconstruction scoring for population sequences.

Shared instrument (factored out of the V1 gate). The "function" of a replay/run sequence is the
trajectory it represents. We score a (reconstructed) sequence by how well the animal's path can
be decoded from it, and compare to a time-shuffle null. This is the literature-standard replay
instrument and is reused across V1/V2/V3 so every gate scores the same thing.
"""

from __future__ import annotations

import numpy as np


def build_place_fields(sess, n_space: int = 20, eps: float = 1e-3):
    """Per-unit place fields f_u(space) = mean firing rate vs linearized position."""
    edges = np.linspace(0, 1, n_space + 1)
    centers = 0.5 * (edges[:-1] + edges[1:])
    occ, _ = np.histogram(sess.x, bins=edges)
    dt = np.median(np.diff(sess.t)) if sess.t.size > 1 else 1.0
    occ_time = occ * dt + eps
    fields = np.zeros((len(sess.spikes), n_space))
    for u, s in enumerate(sess.spikes):
        xi = np.interp(s, sess.t, sess.x, left=np.nan, right=np.nan)
        xi = xi[~np.isnan(xi)]
        h, _ = np.histogram(xi, bins=edges)
        fields[u] = h / occ_time
    return fields, centers


def decode_trajectory(seq_counts: np.ndarray, fields: np.ndarray, dt: float = 1.0) -> np.ndarray:
    """Bayesian 1-D position decode per time bin (Poisson model). Returns space-bin per time bin."""
    f = fields + 1e-3
    n_bins = seq_counts.shape[1]
    log_post = np.empty((n_bins, fields.shape[1]))
    for b in range(n_bins):
        n = seq_counts[:, b][:, None]
        log_post[b] = (n * np.log(f)).sum(axis=0) - dt * f.sum(axis=0)
    return np.argmax(log_post, axis=1)


def decode_score(seq_counts: np.ndarray, fields: np.ndarray) -> float:
    """|rank-corr(time-bin, decoded position)| — how monotonic the decoded trajectory is."""
    if seq_counts.sum() < 5:
        return 0.0
    dec = decode_trajectory(seq_counts, fields)
    if dec.std() < 1e-9:
        return 0.0
    tb = np.arange(len(dec))
    r_t = np.argsort(np.argsort(tb))
    r_d = np.argsort(np.argsort(dec))
    return float(abs(np.corrcoef(r_t, r_d)[0, 1]))


def decode_fidelity(orig: np.ndarray, recon: np.ndarray, fields: np.ndarray) -> float:
    """Trajectory-agreement between the ORIGINAL and a RECONSTRUCTED sequence.

    Decode both; score how well the reconstructed trajectory matches the original's (rank-corr
    of decoded position sequences). 1.0 = identical trajectory; ~0 = unrelated.
    """
    if orig.sum() < 5 or recon.sum() < 5:
        return 0.0
    d0 = decode_trajectory(orig, fields)
    d1 = decode_trajectory(recon, fields)
    if d0.std() < 1e-9 or d1.std() < 1e-9:
        return 0.0
    r0 = np.argsort(np.argsort(d0))
    r1 = np.argsort(np.argsort(d1))
    return float(np.clip(np.corrcoef(r0, r1)[0, 1], 0.0, 1.0))


def time_shuffle(seq: np.ndarray, rng) -> np.ndarray:
    """Null: permute time bins (destroys the sequence, keeps per-bin population vectors)."""
    return seq[:, rng.permutation(seq.shape[1])]


def identification_accuracy(origs: list, recons: list) -> dict:
    """Leave-one-in matching: is recon_i closer to orig_i than to any orig_j (j != i)?

    This is a clean, bounded fidelity instrument immune to the "every reconstruction looks like
    a generic place-field sweep" leak that inflates trajectory-rank nulls. If the latent
    preserves event-SPECIFIC content, recon_i identifies its own original.

      distance : negative cosine similarity between flattened sequences
      top1     : fraction where orig_i is the nearest original to recon_i
      chance   : 1 / n  (random identification)

    Returns top1, chance, and the margin (top1 - chance).
    """
    n = len(origs)
    if n < 3:
        return {"top1": 0.0, "chance": 1.0 / max(n, 1), "margin": 0.0, "n": n}
    O = np.stack([o.ravel().astype(float) for o in origs])
    R = np.stack([r.ravel().astype(float) for r in recons])
    On = O / (np.linalg.norm(O, axis=1, keepdims=True) + 1e-9)
    Rn = R / (np.linalg.norm(R, axis=1, keepdims=True) + 1e-9)
    sim = Rn @ On.T                      # (n, n) cosine sim recon_i vs orig_j
    pred = np.argmax(sim, axis=1)
    top1 = float(np.mean(pred == np.arange(n)))
    chance = 1.0 / n
    return {"top1": top1, "chance": chance, "margin": top1 - chance, "n": n}
