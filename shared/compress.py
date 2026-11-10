"""Compression operations on a connectome weight matrix.

Two pruning policies (the load-bearing comparison for T1):
  * `prune_uniform`       -- remove the globally smallest-magnitude edges (the standard
                             magnitude-pruning baseline).
  * `prune_engram_aware`  -- protect "engram-critical" edges (those touching high-strength /
                             hub nodes), prune the rest. Motivated by torpor engram-resilience
                             (scans/01): biology preferentially preserves a structured subset.

And weight quantization:
  * `quantize`            -- per-matrix symmetric quantization to {int8, int4, ternary}.
  * `quantize_mixed`      -- keep hub-touching edges at higher precision (the structured
                             analogue for the bit-depth axis).

All functions are pure: they take W and return a new W (same shape, zeros = pruned edges).
Sparsity is measured against the ORIGINAL edge count so uniform and engram-aware are compared
at identical budgets.
"""

from __future__ import annotations

import numpy as np


def _hub_score(W: np.ndarray, method: str = "strength") -> np.ndarray:
    """Per-node importance score. `method` selects the engram-aware definition (robustness axis):

      * "strength"   : in-strength + out-strength (cheap degree/weight hub proxy). Default.
      * "betweenness": approximate betweenness via random-walk / shortest-path load on the
                       binarized graph (nodes that bridge many paths).
      * "kcore"      : weighted k-core number (nodes embedded in dense cores).

    All are deterministic. Returns a length-N vector; higher = more "engram-critical".
    """
    if method == "strength":
        return W.sum(axis=0) + W.sum(axis=1)

    if method == "kcore":
        # iterative weighted-degree peeling; core number proxy = peel round survived.
        A = (W != 0).astype(float)
        A = np.maximum(A, A.T)  # undirected for core
        deg = A.sum(axis=1)
        alive = np.ones(W.shape[0], dtype=bool)
        core = np.zeros(W.shape[0])
        round_i = 0
        d = deg.copy()
        while alive.any():
            round_i += 1
            thr = d[alive].min() if alive.any() else 0
            peel = alive & (d <= thr)
            if not peel.any():
                peel = alive & (d == d[alive].min())
            core[peel] = round_i
            alive = alive & ~peel
            if alive.any():
                d = (A[np.ix_(np.arange(len(alive)), alive)]).sum(axis=1)
                d = np.where(alive, d, 0)
        return core

    if method == "betweenness":
        # approximate: stationary-distribution load of a random walk on the binarized graph.
        A = (W != 0).astype(float)
        row = A.sum(axis=1, keepdims=True)
        row[row == 0] = 1.0
        P = A / row
        # power-iterate to the stationary distribution (bridging nodes carry more flow).
        n = W.shape[0]
        v = np.ones(n) / n
        for _ in range(200):
            v_new = v @ P
            s = v_new.sum()
            if s > 0:
                v_new /= s
            if np.linalg.norm(v_new - v, 1) < 1e-9:
                v = v_new
                break
            v = v_new
        return v

    raise ValueError(f"unknown hub-score method {method!r}")


def _edge_mask(W: np.ndarray) -> np.ndarray:
    return W != 0.0


def prune_uniform(W: np.ndarray, sparsity: float, tie_seed: int = 0) -> np.ndarray:
    """Remove EXACTLY round(sparsity * n_edges) smallest-magnitude edges.

    Real connectomes have integer synapse-count weights with huge ties at small values
    (many weight-1 edges). A plain magnitude threshold over-removes (it drops every tied
    edge at once). We instead rank edges by (magnitude, deterministic random tie-break) and
    remove exactly the budgeted count, so uniform and engram-aware are compared at IDENTICAL
    actual budgets. This fix was prompted by real-data validation (see RESEARCH-LOG 2026-11-07).
    """
    if sparsity <= 0:
        return W.copy()
    mask = _edge_mask(W)
    idx = np.argwhere(mask)
    n_edges = idx.shape[0]
    n_remove = int(round(sparsity * n_edges))
    if n_remove <= 0:
        return W.copy()

    mags = np.abs(W[mask])
    rng = np.random.default_rng(tie_seed)
    jitter = rng.random(mags.size)  # deterministic tie-break
    order = np.lexsort((jitter, mags))  # smallest magnitude first, ties broken by jitter
    drop = idx[order[:n_remove]]
    out = W.copy()
    out[drop[:, 0], drop[:, 1]] = 0.0
    return out


def prune_engram_aware(W: np.ndarray, sparsity: float, protect_frac: float = 0.25,
                       method: str = "strength") -> np.ndarray:
    """Protect edges touching top-`protect_frac` hub nodes; magnitude-prune the rest.

    Same total edge budget as `prune_uniform(sparsity)`; the difference is WHICH edges go.
    `method` selects the engram-aware node-importance definition (see `_hub_score`).
    """
    if sparsity <= 0:
        return W.copy()
    mask = _edge_mask(W)
    n_edges = int(mask.sum())
    n_remove = int(round(sparsity * n_edges))
    if n_remove <= 0:
        return W.copy()

    hub = _hub_score(W, method=method)
    n_protect_nodes = max(1, int(round(protect_frac * W.shape[0])))
    protected_nodes = np.argsort(hub)[::-1][:n_protect_nodes]
    is_protected = np.zeros(W.shape[0], dtype=bool)
    is_protected[protected_nodes] = True
    # an edge is protected if either endpoint is a hub
    prot_edge = (is_protected[:, None] | is_protected[None, :]) & mask

    out = W.copy()
    rng = np.random.default_rng(0)  # deterministic tie-break for integer-weight connectomes

    # Phase 1: prune smallest-magnitude UNPROTECTED edges first (exact count via tie-break).
    prunable = mask & ~prot_edge
    pr_idx = np.argwhere(prunable)
    if pr_idx.shape[0] == 0:
        return prune_uniform(W, sparsity)

    mags = np.abs(out[prunable])
    order = np.lexsort((rng.random(mags.size), mags))  # smallest first, ties jittered
    n_from_unprot = min(n_remove, pr_idx.shape[0])
    drop = pr_idx[order[:n_from_unprot]]
    out[drop[:, 0], drop[:, 1]] = 0.0

    # Phase 2: if the budget is not met from unprotected edges alone, continue into the
    # smallest-magnitude PROTECTED edges so the total budget matches `prune_uniform`.
    # Comparing at identical actual budgets is what makes uniform vs. engram-aware a fair test.
    remaining = n_remove - n_from_unprot
    if remaining > 0:
        prot_now = (out != 0.0) & prot_edge
        prot_idx = np.argwhere(prot_now)
        if prot_idx.shape[0] > 0:
            pmags = np.abs(out[prot_now])
            porder = np.lexsort((rng.random(pmags.size), pmags))
            pdrop = prot_idx[porder[:min(remaining, prot_idx.shape[0])]]
            out[pdrop[:, 0], pdrop[:, 1]] = 0.0
    return out


_BITS = {"int8": 8, "int4": 4, "ternary": 2}


def quantize(W: np.ndarray, mode: str) -> np.ndarray:
    """Symmetric per-matrix quantization. mode in {int8, int4, ternary}."""
    if mode not in _BITS:
        raise ValueError(f"unknown quantization mode {mode!r}; expected one of {list(_BITS)}")
    out = W.copy()
    mask = _edge_mask(W)
    if not mask.any():
        return out
    scale = np.abs(W[mask]).max()
    if scale <= 1e-12:
        return out
    if mode == "ternary":
        # {-1, 0, +1} * scale, with a dead-zone at 1/3 of range
        q = np.zeros_like(out)
        thr = scale / 3.0
        q[W > thr] = scale
        q[W < -thr] = -scale
        return q
    levels = 2 ** _BITS[mode] - 1
    step = (2 * scale) / levels
    q = np.round(W / step) * step
    q[~mask] = 0.0
    return q


def quantize_mixed(W: np.ndarray, low_mode: str, protect_frac: float = 0.25,
                   high_mode: str = "int8", method: str = "strength") -> np.ndarray:
    """Quantize hub-touching edges at `high_mode`, the rest at `low_mode`."""
    hub = _hub_score(W, method=method)
    n_protect_nodes = max(1, int(round(protect_frac * W.shape[0])))
    protected_nodes = np.argsort(hub)[::-1][:n_protect_nodes]
    is_protected = np.zeros(W.shape[0], dtype=bool)
    is_protected[protected_nodes] = True
    prot_edge = is_protected[:, None] | is_protected[None, :]

    low = quantize(W, low_mode)
    high = quantize(W, high_mode)
    out = np.where(prot_edge, high, low)
    out[W == 0.0] = 0.0
    return out


def actual_sparsity(W_orig: np.ndarray, W_new: np.ndarray) -> float:
    e0 = int((W_orig != 0).sum())
    e1 = int((W_new != 0).sum())
    return 0.0 if e0 == 0 else 1.0 - e1 / e0
