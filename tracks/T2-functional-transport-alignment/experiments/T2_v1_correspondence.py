"""T2-V1 : correspondence sanity gate.

Does entropic GW recover the ground-truth node correspondence between A and a mildly-perturbed
B (known permutation + small rewire) above a permutation baseline? If GW can't match near-
identical graphs, the alignment premise is dead in-silico.

Pass: GW correspondence accuracy (fraction of A-nodes mapped to their true B-node) clearly
above chance (1/n) and above a random-coupling baseline, at low rewire.
Writes results/T2_v1.json. Needs .venv.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

_ROOT = Path(__file__).resolve().parents[3]
_SRC = Path(__file__).resolve().parents[1] / "src"
for p in (_ROOT, _SRC):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from shared.connectome import load_celegans  # noqa: E402
import gw_align as gw  # noqa: E402

RESULTS = Path(__file__).resolve().parents[1] / "results"
REAL_NPZ = _ROOT / "data" / "celegans_real.npz"


def corr_accuracy(pred_corr, true_perm):
    """Fraction of A-nodes i whose GW match equals the ground-truth image true_perm[i]."""
    return float(np.mean(pred_corr == true_perm))


def run():
    c = load_celegans(path=REAL_NPZ)
    n = c.n
    chance = 1.0 / n

    rows = []
    for rewire in [0.0, 0.05, 0.1, 0.2]:
        W_B, perm = gw.perturb_connectome(c.W, rewire_frac=rewire, seed=0)
        T = gw.entropic_gw(c.W, W_B, epsilon=5e-3, n_iter=200)
        pred = gw.correspondence_from_coupling(T)
        acc = corr_accuracy(pred, perm)
        rows.append({"rewire_frac": rewire, "corr_accuracy": acc, "chance": chance})

    acc0 = rows[0]["corr_accuracy"]
    passed = acc0 > 50 * chance and acc0 > 0.3   # well above chance at zero rewire

    out = {
        "gate": "T2-V1 correspondence sanity",
        "substrate": "real-celegans + perturbation model",
        "n": n, "chance": chance,
        "per_rewire": rows,
        "criterion": "GW accuracy at rewire=0 >> chance (>0.3 and >50x chance)",
        "passed": bool(passed),
    }
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "T2_v1.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    run()
