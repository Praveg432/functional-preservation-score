"""T1-V3b : scaling-rule probe (hypothesis H3).

Question: does the engram-aware ADVANTAGE track a graph-structural quantity, giving a
predictive rule rather than a one-off observation?

Candidate structural quantity: HUB-MASS FRACTION = share of total edge weight carried by edges
touching the top-`protect_frac` strength-hub nodes. Intuition: the more weight concentrated on
hubs, the more a hub-protecting policy should help.

Method: take the real connectome and interpolate it toward its degree-preserving weight-shuffle
(which destroys hub-mass concentration) in steps. At each step, measure:
  * hub_mass_fraction (the structural quantity)
  * engram advantage = best-engram FPS - uniform FPS at int4, averaged over a sparsity grid.
Then report the correlation. A strong positive correlation supports H3.

Writes results/T1_v3b_real.json. Deterministic.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from shared.connectome import load_celegans
from shared.model import ConnectomeModel, default_stimulus_bank
from shared.fps import Battery
from shared import compress

RESULTS = Path(__file__).resolve().parents[1] / "results"
REAL_NPZ = _ROOT / "data" / "celegans_real.npz"
PROTECT = 0.25
TARGETS = [0.5, 0.6, 0.7]
BITDEPTH = "int4"
ALPHAS = [0.0, 0.25, 0.5, 0.75, 1.0]  # 0 = real, 1 = fully weight-shuffled
STIM_SEEDS = [1, 2, 3]


def weight_shuffle(W, seed=0):
    """Keep the edge SET, permute the weight VALUES among edges (destroys hub-mass structure)."""
    rng = np.random.default_rng(seed)
    mask = W != 0
    vals = W[mask].copy()
    rng.shuffle(vals)
    out = np.zeros_like(W)
    out[mask] = vals
    return out


def hub_mass_fraction(W, protect_frac=PROTECT):
    hub = compress._hub_score(W, "strength")
    k = max(1, int(round(protect_frac * W.shape[0])))
    prot = np.zeros(W.shape[0], dtype=bool)
    prot[np.argsort(hub)[::-1][:k]] = True
    prot_edge = prot[:, None] | prot[None, :]
    total = float(np.abs(W).sum())
    return 0.0 if total == 0 else float(np.abs(W[prot_edge]).sum() / total)


def _to_target(W, policy, target):
    lo, hi, best = 0.0, 1.0, None
    for _ in range(14):
        mid = 0.5 * (lo + hi)
        if policy == "uniform":
            Wc = compress.quantize(compress.prune_uniform(W, mid), BITDEPTH)
        else:
            pruned = compress.prune_engram_aware(W, mid, protect_frac=PROTECT, method="strength")
            Wc = compress.quantize_mixed(pruned, low_mode=BITDEPTH, protect_frac=PROTECT,
                                         high_mode="int8", method="strength")
        s = compress.actual_sparsity(W, Wc)
        best = Wc
        if s < target:
            lo = mid
        else:
            hi = mid
    return best


def run():
    c = load_celegans(path=REAL_NPZ)
    model = ConnectomeModel.from_connectome(c)
    W_shuf = weight_shuffle(c.W, seed=0)
    batteries = [Battery(default_stimulus_bank(len(model.sensory_idx), 8, 40, seed=s), model.run)
                 for s in STIM_SEEDS]

    def fps_of(Wc):
        return float(np.mean([b.score(model.with_weights(Wc).run).fps for b in batteries]))

    rows = []
    for a in ALPHAS:
        W = (1 - a) * c.W + a * W_shuf
        hmf = hub_mass_fraction(W)
        margins = []
        for tgt in TARGETS:
            uni = fps_of(_to_target(W, "uniform", tgt))
            eng = fps_of(_to_target(W, "engram", tgt))
            margins.append(eng - uni)
        rows.append({"alpha": a, "hub_mass_fraction": hmf,
                     "engram_advantage": float(np.mean(margins))})

    hmf = np.array([r["hub_mass_fraction"] for r in rows])
    adv = np.array([r["engram_advantage"] for r in rows])
    if hmf.std() > 1e-9 and adv.std() > 1e-9:
        corr = float(np.corrcoef(hmf, adv)[0, 1])
    else:
        corr = float("nan")

    out = {
        "experiment": "T1-V3b scaling rule (H3)",
        "substrate": "real-celegans",
        "structural_quantity": "hub_mass_fraction",
        "bitdepth": BITDEPTH,
        "points": rows,
        "correlation_hubmass_vs_advantage": corr,
        "h3_supported": bool(corr > 0.7) if corr == corr else False,
    }
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "T1_v3b_real.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    run()
