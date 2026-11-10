"""T1-V1 : baseline-reality gate.

Checks that the connectome carries function a random graph does not:
  * reference model scores FPS ~ 1.0 against itself;
  * a degree-preserving shuffled-graph control scores FPS < 0.2.

Writes results/T1_v1.json. Deterministic; runs in < 1 s on CPU.
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

RESULTS = Path(__file__).resolve().parents[1] / "results"
SEEDS = [0, 1, 2]


def shuffle_graph(W: np.ndarray, seed: int) -> np.ndarray:
    """Randomly reassign the existing edge weights to random (i,j) slots (same edge count)."""
    rng = np.random.default_rng(seed)
    mask = W != 0
    weights = W[mask].copy()
    n = W.shape[0]
    out = np.zeros_like(W)
    k = weights.size
    # sample k distinct off-diagonal positions
    all_pos = [(i, j) for i in range(n) for j in range(n) if i != j]
    idx = rng.choice(len(all_pos), size=k, replace=False)
    rng.shuffle(weights)
    for pos, w in zip(idx, weights):
        i, j = all_pos[pos]
        out[i, j] = w
    return out


REAL_NPZ = _ROOT / "data" / "celegans_real.npz"


def _load(seed: int, real: bool):
    """Real mode loads the cached real connectome (shuffle-seed still varies the control)."""
    if real:
        return load_celegans(path=REAL_NPZ)
    return load_celegans(n=300, seed=seed)


def run(real: bool = False):
    rows = []
    # On real data there is one fixed connectome; vary only the shuffle-control seed.
    for seed in SEEDS:
        c = _load(seed, real)
        model = ConnectomeModel.from_connectome(c)
        stim = default_stimulus_bank(len(model.sensory_idx), n_patterns=8, T=40, seed=1)
        bat = Battery(stim, model.run)

        fps_ref = bat.score(model.run).fps

        shuf = model.with_weights(shuffle_graph(c.W, seed=seed))
        fps_shuf = bat.score(shuf.run).fps

        rows.append({"seed": seed, "fps_reference": fps_ref, "fps_shuffled": fps_shuf})

    mean_ref = float(np.mean([r["fps_reference"] for r in rows]))
    mean_shuf = float(np.mean([r["fps_shuffled"] for r in rows]))
    passed = (mean_ref > 0.99) and (mean_shuf < 0.2)

    out = {
        "gate": "T1-V1 baseline-reality",
        "substrate": "real-celegans" if real else "synthetic-celegans",
        "criterion": "reference FPS>0.99 AND shuffled FPS<0.2",
        "per_seed": rows,
        "mean_fps_reference": mean_ref,
        "mean_fps_shuffled": mean_shuf,
        "passed": bool(passed),
    }
    RESULTS.mkdir(exist_ok=True)
    fname = "T1_v1_real.json" if real else "T1_v1.json"
    (RESULTS / fname).write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    run(real="--real" in sys.argv)
