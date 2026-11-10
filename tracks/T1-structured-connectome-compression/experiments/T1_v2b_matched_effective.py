"""T1-V2b : structure-advantage at MATCHED TOTAL EFFECTIVE sparsity (real-data rigor).

Real-data validation (RESEARCH-LOG 2026-11-07) exposed a confound: int4 quantization on the
heavy-tailed integer connectome zeroes most weight-1/2 edges, so "50% prune + int4" yields
~73% effective sparsity for the uniform path but less for the engram mixed-precision path.
Comparing at matched *pruning* budget therefore also varies *total* compression -- unfair.

This experiment removes the confound: both policies are driven to the SAME total effective
sparsity (measured after prune+quant), and FPS is compared there. We sweep target effective
sparsity so the result is a curve, not a single confounded point.

Writes results/T1_v2b_real.json (and _synth.json). Deterministic.
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
QUANT = "int4"
TARGETS = [0.5, 0.6, 0.7, 0.8]          # target TOTAL effective sparsity
STIM_SEEDS = [1, 2, 3]


def _uniform_to_target(W, target):
    """Prune uniformly, then int4-quant, searching the prune level that hits `target` total."""
    lo, hi = 0.0, 1.0
    best = None
    for _ in range(18):  # bisection on prune fraction
        mid = 0.5 * (lo + hi)
        Wc = compress.quantize(compress.prune_uniform(W, mid), QUANT)
        s = compress.actual_sparsity(W, Wc)
        best = Wc
        if s < target:
            lo = mid
        else:
            hi = mid
    return best


def _engram_to_target(W, target):
    lo, hi = 0.0, 1.0
    best = None
    for _ in range(18):
        mid = 0.5 * (lo + hi)
        pruned = compress.prune_engram_aware(W, mid, protect_frac=PROTECT)
        Wc = compress.quantize_mixed(pruned, low_mode=QUANT, protect_frac=PROTECT, high_mode="int8")
        s = compress.actual_sparsity(W, Wc)
        best = Wc
        if s < target:
            lo = mid
        else:
            hi = mid
    return best


def run(real: bool = False):
    c = load_celegans(path=REAL_NPZ) if real else load_celegans(n=300, seed=0)
    model = ConnectomeModel.from_connectome(c)

    rows = []
    for target in TARGETS:
        W_uni = _uniform_to_target(c.W, target)
        W_eng = _engram_to_target(c.W, target)
        s_uni = compress.actual_sparsity(c.W, W_uni)
        s_eng = compress.actual_sparsity(c.W, W_eng)

        fu, fe = [], []
        for ss in STIM_SEEDS:
            stim = default_stimulus_bank(len(model.sensory_idx), n_patterns=8, T=40, seed=ss)
            bat = Battery(stim, model.run)
            fu.append(bat.score(model.with_weights(W_uni).run).fps)
            fe.append(bat.score(model.with_weights(W_eng).run).fps)
        rows.append({
            "target_sparsity": target,
            "actual_sparsity_uniform": s_uni,
            "actual_sparsity_engram": s_eng,
            "fps_uniform_mean": float(np.mean(fu)),
            "fps_engram_mean": float(np.mean(fe)),
            "margin_mean": float(np.mean(fe) - np.mean(fu)),
        })

    # verdict: engram-aware beats uniform at matched effective sparsity across the curve
    margins = np.array([r["margin_mean"] for r in rows])
    advantage = bool(np.mean(margins) > 0.05 and np.sum(margins > 0) >= len(TARGETS) - 1)

    out = {
        "experiment": "T1-V2b matched-effective-sparsity structure advantage",
        "substrate": "real-celegans" if real else "synthetic-celegans",
        "quant": QUANT, "protect_frac": PROTECT,
        "curve": rows,
        "mean_margin": float(margins.mean()),
        "engram_advantage_confirmed": advantage,
    }
    RESULTS.mkdir(exist_ok=True)
    fname = "T1_v2b_real.json" if real else "T1_v2b_synth.json"
    (RESULTS / fname).write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    run(real="--real" in sys.argv)
