"""T2 transport: push A's functional weights onto B's node-space via a node correspondence,
with a Peters'-rule-style feasibility mask (only write onto edges B is wired to support).

corr maps A-node i -> B-node corr[i]. The transported weight matrix in B-space:
    W_T[corr[i], corr[j]] = W_A[i, j]
Then (optional) feasibility mask: zero any transported edge where B has no structural edge
(B cannot physically host a connection it is not wired for) -> isolates H3 (the mask is the
limiter, not the correspondence).
"""

from __future__ import annotations

import numpy as np


def transport_weights(W_A: np.ndarray, corr: np.ndarray, n_B: int,
                      feasibility: np.ndarray | None = None) -> np.ndarray:
    """Transport A's weights into B-space via correspondence `corr` (len n_A, values in [0,n_B)).

    If `feasibility` (n_B x n_B boolean, B's existing edges) is given, mask transported edges to
    only those B supports.
    """
    n_A = W_A.shape[0]
    W_T = np.zeros((n_B, n_B))
    rows, cols = np.nonzero(W_A)
    for i, j in zip(rows, cols):
        W_T[corr[i], corr[j]] += W_A[i, j]
    if feasibility is not None:
        W_T = W_T * feasibility
    return W_T


def feasibility_mask(W_B: np.ndarray) -> np.ndarray:
    """Boolean mask of edges that exist in B (the Peters'-rule constraint surface)."""
    return W_B != 0.0
