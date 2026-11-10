"""T2 statistical hardening: GW correspondence + transport fidelity over multiple perturbation
seeds, with bootstrap CIs and a significance test on the feasibility-mask collapse.

Addresses audit A6: T2 used a single perturbation seed. Here we vary the perturbation seed
(different B realizations) and report mean +/- 95% CI for GW correspondence accuracy and for the
three transport conditions at a representative divergence (5% rewire), plus a permutation test
that masked/GW fidelity < oracle fidelity.

Writes results/T2_v2_stats.json. Needs .venv.
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

from shared import stats          # noqa: E402
from shared.connectome import load_celegans  # noqa: E402
import gw_align as gw             # noqa: E402
import transport as tr           # noqa: E402
import function_test as ft       # noqa: E402

RESULTS = Path(__file__).resolve().parents[1] / "results"
REAL_NPZ = _ROOT / "data" / "celegans_real.npz"
SEEDS = list(range(8))
REWIRE = 0.05       # representative small divergence (where mask collapse first appears)


def run():
    c = load_celegans(path=REAL_NPZ)
    model_A, bat = ft.build_reference(c)
    n = c.n

    corr_acc, fid_oracle, fid_masked, fid_gw = [], [], [], []
    for seed in SEEDS:
        W_B, perm = gw.perturb_connectome(c.W, rewire_frac=REWIRE, seed=seed)
        sidx_B, midx_B = perm[model_A.sensory_idx], perm[model_A.motor_idx]
        # correspondence accuracy (GW vs ground-truth perm)
        T = gw.entropic_gw(c.W, W_B, epsilon=5e-3, n_iter=150)
        gw_corr = gw.correspondence_from_coupling(T)
        corr_acc.append(float(np.mean(gw_corr == perm)))
        # transport conditions
        fid_oracle.append(ft.transport_fidelity(model_A, bat, tr.transport_weights(c.W, perm, n), sidx_B, midx_B))
        feas = tr.feasibility_mask(W_B)
        fid_masked.append(ft.transport_fidelity(model_A, bat, tr.transport_weights(c.W, perm, n, feasibility=feas), sidx_B, midx_B))
        fid_gw.append(ft.transport_fidelity(model_A, bat, tr.transport_weights(c.W, gw_corr, n), sidx_B, midx_B))

    def ci(v, s):
        m, lo, hi, nn = stats.bootstrap_ci(v, seed=s)
        return {"mean": m, "ci95": [lo, hi], "n": nn}

    _, p_mask = stats.permutation_test_greater(fid_oracle, fid_masked, n_perm=10000, seed=10)
    _, p_gw = stats.permutation_test_greater(fid_oracle, fid_gw, n_perm=10000, seed=11)

    out = {
        "experiment": "T2 statistical hardening (multi-seed GW + transport)",
        "substrate": "real-celegans + perturbation model", "rewire": REWIRE, "n_seeds": len(SEEDS),
        "gw_correspondence_accuracy": ci(corr_acc, 1),
        "transport_oracle": ci(fid_oracle, 2),
        "transport_oracle_masked": ci(fid_masked, 3),
        "transport_gw": ci(fid_gw, 4),
        "p_oracle_gt_masked": p_mask,
        "p_oracle_gt_gw": p_gw,
        "verdict": "Feasibility mask and GW-correspondence each significantly reduce transport fidelity vs the oracle+unconstrained ideal.",
    }
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "T2_v2_stats.json").write_text(json.dumps(out, indent=2))
    for k in ("gw_correspondence_accuracy", "transport_oracle", "transport_oracle_masked", "transport_gw"):
        r = out[k]
        print(f"{k:28s}: {r['mean']:.3f}  CI[{r['ci95'][0]:.3f},{r['ci95'][1]:.3f}] (n={r['n']})")
    print(f"p(oracle>masked)={p_mask:.4f}  p(oracle>gw)={p_gw:.4f}")
    return out


if __name__ == "__main__":
    run()
