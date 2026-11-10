"""T2 alignment: self-contained entropic Gromov-Wasserstein + a controlled-divergence model
for generating "individual B" from the real connectome A with KNOWN ground-truth correspondence.

Why a perturbation model: we have one real C. elegans connectome, not two labeled individuals.
To test alignment honestly we build B = perturb(A) by (1) applying a known node permutation
(so ground-truth correspondence is the inverse permutation) and (2) rewiring a tunable fraction
of edges (the A<->B structural divergence knob). This is stated as a divergence MODEL, not two
real worms (honest scope in RESULTS).

Entropic GW (Peyré, Cuturi, Solomon 2016): given intra-domain distance/affinity matrices
C1 (A) and C2 (B) and marginals p, q, find coupling T minimizing the GW cost with entropic
regularization via Sinkhorn projections. Node correspondence = argmax over T rows.
"""

from __future__ import annotations

import numpy as np


def perturb_connectome(W: np.ndarray, rewire_frac: float, seed: int = 0):
    """Build B from A: permute nodes (known GT correspondence) + rewire `rewire_frac` of edges.

    Returns (W_B, perm) where perm maps A-index -> B-index (ground-truth correspondence), i.e.
    B node perm[i] corresponds to A node i.
    """
    rng = np.random.default_rng(seed)
    n = W.shape[0]

    # 1) rewire a fraction of edges in A's frame (reassign their endpoints), preserving count
    Wr = W.copy()
    mask = np.argwhere(Wr != 0)
    n_rewire = int(round(rewire_frac * len(mask)))
    if n_rewire > 0:
        pick = rng.choice(len(mask), size=n_rewire, replace=False)
        for idx in pick:
            i, j = mask[idx]
            w = Wr[i, j]
            Wr[i, j] = 0.0
            # move weight to a new random off-diagonal slot
            ni, nj = rng.integers(0, n), rng.integers(0, n)
            if ni != nj:
                Wr[ni, nj] += w

    # 2) permute node labels -> B
    perm = rng.permutation(n)
    P = np.zeros((n, n))
    P[np.arange(n), perm] = 1.0           # P maps A-space -> B-space
    W_B = P.T @ Wr @ P                     # relabel nodes
    return W_B, perm


def _affinity(W: np.ndarray) -> np.ndarray:
    """Symmetric structural affinity used as the GW intra-domain matrix."""
    A = np.abs(W) + np.abs(W.T)
    # normalize to comparable scale across graphs
    s = A.max()
    return A / (s + 1e-9)


def entropic_gw(W1: np.ndarray, W2: np.ndarray, epsilon: float = 5e-3,
                n_iter: int = 200, sinkhorn_iter: int = 50, seed: int = 0) -> np.ndarray:
    """Entropic Gromov-Wasserstein coupling between graphs W1 (n1) and W2 (n2).

    Returns coupling T (n1 x n2). Node correspondence: for A-node i, argmax_j T[i, j].
    Uniform marginals. Square-loss GW with Sinkhorn projection each outer step.
    """
    C1, C2 = _affinity(W1), _affinity(W2)
    n1, n2 = C1.shape[0], C2.shape[0]
    p = np.ones(n1) / n1
    q = np.ones(n2) / n2
    T = np.outer(p, q)                     # init

    # constants for square-loss GW gradient: L(C1,C2) tensor product
    C1sq = C1 ** 2
    C2sq = C2 ** 2
    f1 = C1sq @ p                          # (n1,)
    f2 = C2sq @ q                          # (n2,)
    const = f1[:, None] + f2[None, :]      # (n1, n2)

    for _ in range(n_iter):
        # GW gradient: const - 2 C1 T C2^T
        grad = const - 2.0 * (C1 @ T @ C2.T)
        K = np.exp(-grad / epsilon) * T    # proximal / mirror-descent step
        # Sinkhorn to project onto U(p,q)
        u = np.ones(n1)
        v = np.ones(n2)
        for _s in range(sinkhorn_iter):
            u = p / (K @ v + 1e-12)
            v = q / (K.T @ u + 1e-12)
        T = u[:, None] * K * v[None, :]
    return T


def correspondence_from_coupling(T: np.ndarray) -> np.ndarray:
    """Hard correspondence: A-node i -> B-node argmax_j T[i, j]."""
    return np.argmax(T, axis=1)
