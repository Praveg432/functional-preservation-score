"""T1-V2 : structure-advantage gate (load-bearing).

At 50% sparsity + int4 quantization, does engram-aware compression preserve function where
uniform compression fails? Pre-registered criteria in ../PRE-REGISTRATION.md:
  pass if engram-aware FPS >= 0.5 AND (engram-aware - uniform) >= 0.15 on >=2/3 seeds.

Writes results/T1_v2.json. Deterministic; runs in a few seconds on CPU.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

# make the repo root importable when run as a standalone script
_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from shared.connectome import load_celegans
from shared.model import ConnectomeModel, default_stimulus_bank
from shared.fps import Battery
from shared import compress

RESULTS = Path(__file__).resolve().parents[1] / "results"
SEEDS = [0, 1, 2]
SPARSITY = 0.5
QUANT = "int4"
PROTECT = 0.25

# pre-registered thresholds
MIN_ENGRAM_FPS = 0.5
MIN_MARGIN = 0.15
KILL_MARGIN = 0.05


def _compose_uniform(W):
    return compress.quantize(compress.prune_uniform(W, SPARSITY), QUANT)


def _compose_engram(W):
    pruned = compress.prune_engram_aware(W, SPARSITY, protect_frac=PROTECT)
    return compress.quantize_mixed(pruned, low_mode=QUANT, protect_frac=PROTECT, high_mode="int8")


REAL_NPZ = _ROOT / "data" / "celegans_real.npz"


def _load(seed: int, real: bool):
    if real:
        return load_celegans(path=REAL_NPZ)
    return load_celegans(n=300, seed=seed)


def run(real: bool = False):
    rows = []
    # Real connectome is fixed; the stimulus battery seed varies to give >1 behavioral sample.
    stim_seeds = [1, 2, 3] if real else [1, 1, 1]
    for k, seed in enumerate(SEEDS):
        c = _load(seed, real)
        model = ConnectomeModel.from_connectome(c)
        stim = default_stimulus_bank(len(model.sensory_idx), n_patterns=8, T=40, seed=stim_seeds[k])
        bat = Battery(stim, model.run)

        W_uni = _compose_uniform(c.W)
        W_eng = _compose_engram(c.W)

        fps_uni = bat.score(model.with_weights(W_uni).run).fps
        fps_eng = bat.score(model.with_weights(W_eng).run).fps

        rows.append({
            "seed": seed,
            "stim_seed": stim_seeds[k],
            "sparsity_uniform": compress.actual_sparsity(c.W, W_uni),
            "sparsity_engram": compress.actual_sparsity(c.W, W_eng),
            "fps_uniform": fps_uni,
            "fps_engram": fps_eng,
            "margin": fps_eng - fps_uni,
        })

    margins = np.array([r["margin"] for r in rows])
    eng = np.array([r["fps_engram"] for r in rows])
    seeds_pass = int(np.sum((eng >= MIN_ENGRAM_FPS) & (margins >= MIN_MARGIN)))
    mean_margin = float(margins.mean())

    passed = seeds_pass >= 2
    killed = mean_margin < KILL_MARGIN

    out = {
        "gate": "T1-V2 structure-advantage",
        "substrate": "real-celegans" if real else "synthetic-celegans",
        "operating_point": {"sparsity": SPARSITY, "quant": QUANT, "protect_frac": PROTECT},
        "criterion": f"engram FPS>={MIN_ENGRAM_FPS} AND margin>={MIN_MARGIN} on >=2/3 seeds",
        "per_seed": rows,
        "mean_fps_uniform": float(np.mean([r["fps_uniform"] for r in rows])),
        "mean_fps_engram": float(eng.mean()),
        "mean_margin": mean_margin,
        "seeds_passing": seeds_pass,
        "passed": bool(passed),
        "killed_hypothesis": bool(killed),
    }
    RESULTS.mkdir(exist_ok=True)
    fname = "T1_v2_real.json" if real else "T1_v2.json"
    (RESULTS / fname).write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    run(real="--real" in sys.argv)
