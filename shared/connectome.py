"""Connectome loaders.

The research targets the real C. elegans connectome (OpenWorm / WormNeuroAtlas) and, later,
FlyWire sub-circuits and MICrONS columns (see ../DATASETS.md). To keep Phase-0 fully
reproducible and offline on an M4, this module provides:

  * `load_celegans(...)` -- tries a real adjacency file if present, else falls back to a
    deterministic, structurally-realistic synthetic connectome.
  * `synth_celegans(...)` -- the deterministic fallback: a directed, weighted graph with a
    sensory -> interneuron -> motor layering, heavy-tailed hub degree, and a KNOWN
    ground-truth partition (base-OS vs. payload) and node roles.

The synthetic graph is NOT a claim about the real worm. It is a controlled substrate with the
structural properties the experiments need (layering, hubs, a known partition), so that
method behavior (uniform vs. engram-aware compression, transport, ablation) can be measured
before swapping in real data via the documented hook.

Contract:
    A Connectome is a frozen dataclass with:
      W     : (N, N) float64 weighted adjacency, W[i, j] = weight of edge i -> j (0 = none)
      roles : (N,) int   node role: 0=sensory, 1=inter, 2=motor
      part  : (N,) int   ground-truth partition: 0=base-OS, 1=payload
      names : list[str]  node labels
    Absence of an edge is an explicit 0.0 weight, never NaN.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

SENSORY, INTER, MOTOR = 0, 1, 2
BASE_OS, PAYLOAD = 0, 1


@dataclass(frozen=True)
class Connectome:
    W: np.ndarray
    roles: np.ndarray
    part: np.ndarray
    names: list[str]

    @property
    def n(self) -> int:
        return self.W.shape[0]

    def in_strength(self) -> np.ndarray:
        return self.W.sum(axis=0)

    def out_strength(self) -> np.ndarray:
        return self.W.sum(axis=1)

    def n_edges(self) -> int:
        return int((self.W != 0).sum())


def synth_celegans(
    n: int = 300,
    seed: int = 0,
    frac_sensory: float = 0.18,
    frac_motor: float = 0.18,
    n_hubs: int = 12,
) -> Connectome:
    """Deterministic, structured synthetic connectome.

    Properties engineered in on purpose:
      * three roles with feedforward bias sensory -> inter -> motor (plus recurrence in inter);
      * a small set of high-degree interneuron HUBS (the "engram-critical" nodes the
        engram-aware policy is meant to protect);
      * a ground-truth partition: sensory+motor+their direct interneurons = base-OS,
        the recurrent interneuron core = payload.
    """
    rng = np.random.default_rng(seed)

    n_sens = max(1, int(round(n * frac_sensory)))
    n_mot = max(1, int(round(n * frac_motor)))
    n_int = n - n_sens - n_mot

    roles = np.empty(n, dtype=int)
    roles[:n_sens] = SENSORY
    roles[n_sens : n_sens + n_int] = INTER
    roles[n_sens + n_int :] = MOTOR

    sens_idx = np.where(roles == SENSORY)[0]
    int_idx = np.where(roles == INTER)[0]
    mot_idx = np.where(roles == MOTOR)[0]

    # hubs: a handful of interneurons that receive/emit disproportionately many edges.
    n_hubs = min(n_hubs, n_int)
    hub_idx = rng.choice(int_idx, size=n_hubs, replace=False)
    is_hub = np.zeros(n, dtype=bool)
    is_hub[hub_idx] = True

    W = np.zeros((n, n), dtype=np.float64)

    def _connect(src, dst, p, wscale, hub_boost=1.0):
        for i in src:
            for j in dst:
                if i == j:
                    continue
                pp = p * (hub_boost if (is_hub[i] or is_hub[j]) else 1.0)
                if rng.random() < min(pp, 0.95):
                    W[i, j] = rng.gamma(2.0, wscale)

    # feedforward backbone
    _connect(sens_idx, int_idx, p=0.04, wscale=0.5, hub_boost=4.0)
    _connect(int_idx, int_idx, p=0.03, wscale=0.4, hub_boost=5.0)   # recurrent core
    _connect(int_idx, mot_idx, p=0.05, wscale=0.5, hub_boost=4.0)
    _connect(sens_idx, mot_idx, p=0.01, wscale=0.3)                 # sparse direct reflex

    # ground-truth partition:
    #   payload = recurrent interneuron core (the "identity"-like processing)
    #   base-OS = sensory, motor, and the interneurons that only relay (non-hub, low recurrence)
    in_str = W.sum(axis=0)
    out_str = W.sum(axis=1)
    recur = np.array(
        [W[int_idx][:, int_idx][k].sum() + W[int_idx][:, int_idx][:, k].sum()
         for k in range(len(int_idx))]
    )
    recur_thresh = np.quantile(recur, 0.5) if len(recur) else 0.0

    part = np.full(n, BASE_OS, dtype=int)
    for pos, node in enumerate(int_idx):
        if is_hub[node] or recur[pos] > recur_thresh:
            part[node] = PAYLOAD

    names = []
    for i in range(n):
        tag = {SENSORY: "S", INTER: "I", MOTOR: "M"}[roles[i]]
        names.append(f"{tag}{i:03d}{'*' if is_hub[i] else ''}")

    return Connectome(W=W, roles=roles, part=part, names=names)


def load_celegans(path: str | Path | None = None, **synth_kwargs) -> Connectome:
    """Load a real C. elegans adjacency if available, else the deterministic synthetic fallback.

    Real-data hook: pass `path` to a .npz with keys W, roles, part, names (produced by a
    future `scripts/fetch_openworm.py`). When absent, returns `synth_celegans(**synth_kwargs)`.
    This keeps Phase-0 runnable offline while leaving a clean seam for real data.
    """
    if path is not None and Path(path).exists():
        d = np.load(path, allow_pickle=True)
        return Connectome(
            W=d["W"].astype(np.float64),
            roles=d["roles"].astype(int),
            part=d["part"].astype(int),
            names=list(d["names"]),
        )
    return synth_celegans(**synth_kwargs)
