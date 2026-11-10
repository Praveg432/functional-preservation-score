"""T1-V4 : dynamics-robustness of the Effect-B regime boundary.

The whole program scores on FPS, which depends on a dynamics model. Effect B (engram beats
uniform only at HIGH sparsity; uniform wins at LOW sparsity) was measured with the leaky-rate
tanh model. If that boundary is an artifact of the model, the result is not trustworthy.

This experiment re-runs the clean int8 matched-sparsity comparison (no quantization floor, so
it is a genuine apples-to-apples pruning test) under TWO independent dynamics models:
  * ConnectomeModel        (leaky-rate, tanh, additive drive)
  * SigmoidConductanceModel(logistic, divisive conductance normalization)

Robustness criterion: the SIGN of the regime boundary is preserved -- uniform wins at low
sparsity, engram (strength) wins at high sparsity -- under BOTH models, on the REAL connectome.

Writes results/T1_v4_real.json. Deterministic.
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
from shared.model import ConnectomeModel, SigmoidConductanceModel, default_stimulus_bank
from shared.fps import Battery
from shared import compress

RESULTS = Path(__file__).resolve().parents[1] / "results"
REAL_NPZ = _ROOT / "data" / "celegans_real.npz"
BITDEPTH = "int8"                     # no floor -> clean matched comparison
TARGETS = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
PROTECT = 0.25
STIM_SEEDS = [1, 2, 3]
LOW_REGIME = [0.3, 0.4]
HIGH_REGIME = [0.5, 0.6, 0.7]


def _uniform(W, target):
    lo, hi, best = 0.0, 1.0, None
    for _ in range(16):
        mid = 0.5 * (lo + hi)
        Wc = compress.quantize(compress.prune_uniform(W, mid), BITDEPTH)
        s = compress.actual_sparsity(W, Wc)
        best = Wc
        lo, hi = (mid, hi) if s < target else (lo, mid)
    return best


def _engram(W, target):
    lo, hi, best = 0.0, 1.0, None
    for _ in range(16):
        mid = 0.5 * (lo + hi)
        pruned = compress.prune_engram_aware(W, mid, protect_frac=PROTECT, method="strength")
        Wc = compress.quantize_mixed(pruned, low_mode=BITDEPTH, protect_frac=PROTECT,
                                     high_mode="int8", method="strength")
        s = compress.actual_sparsity(W, Wc)
        best = Wc
        lo, hi = (mid, hi) if s < target else (lo, mid)
    return best


def _eval(model_cls, c):
    model = model_cls.from_connectome(c)
    bats = [Battery(default_stimulus_bank(len(model.sensory_idx), 8, 40, seed=s), model.run)
            for s in STIM_SEEDS]

    def fps(Wc):
        return float(np.mean([b.score(model.with_weights(Wc).run).fps for b in bats]))

    rows = []
    for t in TARGETS:
        fu = fps(_uniform(c.W, t))
        fe = fps(_engram(c.W, t))
        rows.append({"target": t, "fps_uniform": fu, "fps_engram": fe, "margin": fe - fu})
    return rows


def _boundary_ok(rows):
    """Uniform should win (margin<0) in LOW regime, engram should win (margin>0) in HIGH regime."""
    low = [r["margin"] for r in rows if r["target"] in LOW_REGIME]
    high = [r["margin"] for r in rows if r["target"] in HIGH_REGIME]
    return (np.mean(low) < 0) and (np.mean(high) > 0)


def run():
    c = load_celegans(path=REAL_NPZ)
    out = {"experiment": "T1-V4 dynamics robustness of Effect-B boundary",
           "substrate": "real-celegans", "bitdepth": BITDEPTH, "models": {}}
    all_ok = True
    for name, cls in [("leaky_rate_tanh", ConnectomeModel),
                      ("sigmoid_conductance", SigmoidConductanceModel)]:
        rows = _eval(cls, c)
        ok = _boundary_ok(rows)
        all_ok = all_ok and ok
        out["models"][name] = {"curve": rows, "boundary_preserved": bool(ok)}

    out["boundary_model_invariant"] = bool(all_ok)
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "T1_v4_real.json").write_text(json.dumps(out, indent=2))
    for name, m in out["models"].items():
        print(f"\n{name}: boundary_preserved={m['boundary_preserved']}")
        for r in m["curve"]:
            print(f"  t={r['target']}: uni {r['fps_uniform']:.3f} eng {r['fps_engram']:.3f} "
                  f"margin {r['margin']:+.3f}")
    print(f"\nboundary_model_invariant = {out['boundary_model_invariant']}")
    return out


if __name__ == "__main__":
    run()
