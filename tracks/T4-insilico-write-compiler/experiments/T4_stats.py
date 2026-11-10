"""T4 statistical hardening: plausibility gap with seed CIs + permutation significance.

Addresses audit A6: T4-V2 reported 3-seed means with no CIs/tests. Here we use more seeds,
report global/local per-seed, bootstrap the gap CI, and run a one-sided permutation test that
global_ceiling > local_fidelity (the plausibility-gap claim), plus a paired test that
ripple != plain (H3). At divergence 0 (cleanest: topology feasible).

Writes results/T4_v2_stats.json. Needs .venv.
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

from shared import stats      # noqa: E402
from host_net import HostNet  # noqa: E402
import installer as inst      # noqa: E402
import global_baseline as gb  # noqa: E402

RESULTS = Path(__file__).resolve().parents[1] / "results"
N, D_IN, D_OUT, DENSITY = 40, 3, 2, 0.2
SEEDS = list(range(10))      # audit: more seeds than the original 3
DIVERGENCE = 0.0


def make_inputs(d_in, k, T, seed):
    rng = np.random.default_rng(seed)
    raw = rng.standard_normal((k, T, d_in))
    for _ in range(3):
        raw[:, 1:-1] = 0.25 * raw[:, :-2] + 0.5 * raw[:, 1:-1] + 0.25 * raw[:, 2:]
    return [raw[i] for i in range(k)]


def build_pair(seed):
    host = HostNet.random(N, D_IN, D_OUT, DENSITY, seed=seed)
    rng = np.random.default_rng(seed + 999)
    target = host.copy()
    target.W = rng.standard_normal((N, N)) * 0.3 * host.mask
    return host, target


def run():
    g_vals, lp_vals, lr_vals = [], [], []
    for seed in SEEDS:
        host, target = build_pair(seed)
        tr = make_inputs(D_IN, 8, 30, seed)
        te = make_inputs(D_IN, 4, 30, seed + 50)
        g_vals.append(gb.global_ceiling(host, target, tr, te))
        lp_vals.append(inst.install(host, target, tr, te, episodes=300, use_ripple=False, seed=seed)["fidelity"])
        lr_vals.append(inst.install(host, target, tr, te, episodes=300, use_ripple=True, seed=seed)["fidelity"])

    g = np.array(g_vals); lp = np.array(lp_vals); lr = np.array(lr_vals)
    best_local = np.maximum(lp, lr)
    gaps = g - best_local

    gm, glo, ghi, _ = stats.bootstrap_ci(g, seed=1)
    lm, llo, lhi, _ = stats.bootstrap_ci(best_local, seed=2)
    gapm, gaplo, gaphi, _ = stats.bootstrap_ci(gaps, seed=3)
    _, p_gap = stats.permutation_test_greater(g, best_local, n_perm=10000, seed=4)
    # H3: paired difference ripple - plain
    dpm, dplo, dphi, _ = stats.bootstrap_ci(lr - lp, seed=5)

    out = {
        "experiment": "T4 statistical hardening (gap CI + permutation)",
        "config": {"n": N, "divergence": DIVERGENCE, "n_seeds": len(SEEDS), "episodes": 300},
        "global_ceiling": {"mean": gm, "ci95": [glo, ghi]},
        "best_local": {"mean": lm, "ci95": [llo, lhi]},
        "plausibility_gap": {"mean": gapm, "ci95": [gaplo, gaphi], "cohens_d": stats.cohens_d(g, best_local)},
        "p_value_global_gt_local": p_gap,
        "ripple_minus_plain": {"mean": dpm, "ci95": [dplo, dphi],
                               "ripple_helps_significantly": bool(dplo > 0)},
        "verdict": (f"Plausibility gap {gapm:.2f} (95% CI [{gaplo:.2f},{gaphi:.2f}]), "
                    f"global>local p={p_gap:.4f}. "
                    + ("Ripple helps (CI>0)." if dplo > 0 else "Ripple does not help (CI includes 0).")),
    }
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "T4_v2_stats.json").write_text(json.dumps(out, indent=2))
    print(f"global {gm:.2f}[{glo:.2f},{ghi:.2f}]  best_local {lm:.2f}[{llo:.2f},{lhi:.2f}]")
    print(f"gap {gapm:.2f}[{gaplo:.2f},{gaphi:.2f}]  p(global>local)={p_gap:.4f}  d={out['plausibility_gap']['cohens_d']:.2f}")
    print(f"ripple-plain {dpm:+.3f}[{dplo:+.3f},{dphi:+.3f}] -> {out['ripple_minus_plain']['ripple_helps_significantly']}")
    return out


if __name__ == "__main__":
    run()
