"""T1-V3 : breakdown map over (bit-depth x effective-sparsity x structure policy).

Produces the headline figure's data: the FPS surface as a connectome-GNN is compressed along
two axes (how sparse, how few bits), under four structure policies:
  * uniform                      (magnitude pruning + per-matrix quant)
  * engram:strength              (protect strength hubs + mixed precision)
  * engram:betweenness           (protect random-walk-load bridges)
  * engram:kcore                 (protect dense-core nodes)

For each (bit-depth, policy) we drive to a grid of TOTAL effective sparsities (matched across
policies, per V2b) and record FPS. We also extract, per bit-depth, the effective-sparsity
FLOOR = the minimum total sparsity a policy can reach (quantization alone forces sparsity when
small weights round to zero).

Writes results/T1_v3_real.json (+ _synth.json). Deterministic. Runs in a few minutes on CPU.
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

BITDEPTHS = ["int8", "int4", "ternary"]
TARGETS = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
POLICIES = ["uniform", "engram:strength", "engram:betweenness", "engram:kcore"]
PROTECT = 0.25
STIM_SEEDS = [1, 2, 3]


def _compose(W, policy, bitdepth, prune_frac):
    if policy == "uniform":
        return compress.quantize(compress.prune_uniform(W, prune_frac), bitdepth)
    method = policy.split(":", 1)[1]
    pruned = compress.prune_engram_aware(W, prune_frac, protect_frac=PROTECT, method=method)
    return compress.quantize_mixed(pruned, low_mode=bitdepth, protect_frac=PROTECT,
                                   high_mode="int8", method=method)


def _to_target(W, policy, bitdepth, target):
    """Bisection on prune fraction to hit a target TOTAL effective sparsity (or report floor)."""
    lo, hi = 0.0, 1.0
    best, best_s = None, None
    for _ in range(16):
        mid = 0.5 * (lo + hi)
        Wc = _compose(W, policy, bitdepth, mid)
        s = compress.actual_sparsity(W, Wc)
        best, best_s = Wc, s
        if s < target:
            lo = mid
        else:
            hi = mid
    return best, best_s


def run(real: bool = False):
    c = load_celegans(path=REAL_NPZ) if real else load_celegans(n=300, seed=0)
    model = ConnectomeModel.from_connectome(c)
    batteries = [Battery(default_stimulus_bank(len(model.sensory_idx), 8, 40, seed=s), model.run)
                 for s in STIM_SEEDS]

    def fps_of(Wc):
        return float(np.mean([b.score(model.with_weights(Wc).run).fps for b in batteries]))

    surface = []     # one row per (bitdepth, policy, target)
    floors = {}      # (bitdepth, policy) -> min achievable effective sparsity (floor)
    for bd in BITDEPTHS:
        for pol in POLICIES:
            # floor = effective sparsity with prune_frac -> 0 (quantization-only sparsity)
            Wc0 = _compose(c.W, pol, bd, 0.0)
            floor = compress.actual_sparsity(c.W, Wc0)
            floors[f"{bd}|{pol}"] = floor
            for tgt in TARGETS:
                if tgt < floor - 1e-6:
                    surface.append({"bitdepth": bd, "policy": pol, "target": tgt,
                                    "achieved_sparsity": floor, "fps": fps_of(Wc0),
                                    "below_floor": True})
                    continue
                Wc, s = _to_target(c.W, pol, bd, tgt)
                surface.append({"bitdepth": bd, "policy": pol, "target": tgt,
                                "achieved_sparsity": s, "fps": fps_of(Wc),
                                "below_floor": False})

    # headline summaries
    # 1) int4 floor comparison uniform vs best engram
    floor_summary = {k: round(v, 4) for k, v in floors.items()}
    # 2) mean engram advantage per bit-depth (best engram policy - uniform) at matched targets
    adv = {}
    for bd in BITDEPTHS:
        uni = {r["target"]: r["fps"] for r in surface if r["bitdepth"] == bd and r["policy"] == "uniform"}
        best_margin = []
        for tgt in TARGETS:
            eng_vals = [r["fps"] for r in surface
                        if r["bitdepth"] == bd and r["policy"].startswith("engram") and r["target"] == tgt]
            if eng_vals and tgt in uni:
                best_margin.append(max(eng_vals) - uni[tgt])
        adv[bd] = float(np.mean(best_margin)) if best_margin else None

    out = {
        "experiment": "T1-V3 breakdown map",
        "substrate": "real-celegans" if real else "synthetic-celegans",
        "axes": {"bitdepths": BITDEPTHS, "targets": TARGETS, "policies": POLICIES},
        "surface": surface,
        "effective_sparsity_floor": floor_summary,
        "mean_engram_advantage_by_bitdepth": adv,
    }
    RESULTS.mkdir(exist_ok=True)
    fname = "T1_v3_real.json" if real else "T1_v3_synth.json"
    (RESULTS / fname).write_text(json.dumps(out, indent=2))
    print("floors:", json.dumps(floor_summary, indent=2))
    print("mean engram advantage by bit-depth:", json.dumps(adv, indent=2))
    return out


if __name__ == "__main__":
    run(real="--real" in sys.argv)
