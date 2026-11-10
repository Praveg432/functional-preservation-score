"""T4-V2 (+V3): reachability map (local vs global) + structured-teaching.

V1 diagnosis established the key structure: the GLOBAL optimizer reaches fidelity ~1.0 on the
fixed topology (the write is coherent in principle), but LOCAL reward-modulated plasticity does
not. This experiment maps that PLAUSIBILITY GAP across host<->target divergence, and tests
whether RIPPLE-TIMED (structured) teaching narrows it (H3 / the blueprint's sleep-ripple idea).

Divergence = fraction of the target's topology that DIFFERS from the host's (edges the host
lacks -> the T2 feasibility constraint re-enters). We report, per divergence:
  * global_ceiling  : best achievable on the host's fixed topology (upper bound)
  * local_plain     : reward-modulated Hebb, continuous plasticity
  * local_ripple    : reward-modulated Hebb, ripple-gated plasticity (structured)
  * plausibility_gap: global - best(local)

Writes results/T4_v2.json. Needs .venv.
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

from host_net import HostNet  # noqa: E402
import installer as inst      # noqa: E402
import global_baseline as gb  # noqa: E402

RESULTS = Path(__file__).resolve().parents[1] / "results"
N, D_IN, D_OUT, DENSITY = 40, 3, 2, 0.2
DIVERGENCES = [0.0, 0.1, 0.3, 0.5]
SEEDS = [0, 1, 2]


def make_inputs(d_in, k, T, seed):
    rng = np.random.default_rng(seed)
    raw = rng.standard_normal((k, T, d_in))
    for _ in range(3):
        raw[:, 1:-1] = 0.25 * raw[:, :-2] + 0.5 * raw[:, 1:-1] + 0.25 * raw[:, 2:]
    return [raw[i] for i in range(k)]


def build_pair(seed, divergence):
    """Host fixed topology; target = different recurrent weights on a topology that DIFFERS
    from the host's by `divergence` (target has some edges the host lacks -> feasibility gap)."""
    host = HostNet.random(N, D_IN, D_OUT, DENSITY, seed=seed)
    rng = np.random.default_rng(seed + 999)
    tmask = host.mask.copy()
    # flip a `divergence` fraction of edge-slots: add/remove to create target-only edges
    n_flip = int(round(divergence * host.mask.sum()))
    if n_flip:
        off = np.argwhere(~host.mask & ~np.eye(N, dtype=bool))
        add = off[rng.choice(len(off), size=min(n_flip, len(off)), replace=False)]
        for i, j in add:
            tmask[i, j] = True
    target = host.copy()
    target.W = rng.standard_normal((N, N)) * 0.3 * tmask
    return host, target


def run():
    rows = []
    for div in DIVERGENCES:
        gc, lp, lr_, gaps = [], [], [], []
        for seed in SEEDS:
            host, target = build_pair(seed, div)
            tr = make_inputs(D_IN, 8, 30, seed)
            te = make_inputs(D_IN, 4, 30, seed + 50)
            g = gb.global_ceiling(host, target, tr, te)
            lpl = inst.install(host, target, tr, te, episodes=300, use_ripple=False, seed=seed)["fidelity"]
            lrp = inst.install(host, target, tr, te, episodes=300, use_ripple=True, seed=seed)["fidelity"]
            gc.append(g); lp.append(lpl); lr_.append(lrp)
            gaps.append(g - max(lpl, lrp))
        rows.append({
            "divergence": div,
            "global_ceiling": float(np.mean(gc)),
            "local_plain": float(np.mean(lp)),
            "local_ripple": float(np.mean(lr_)),
            "plausibility_gap": float(np.mean(gaps)),
        })

    # verdicts
    gap0 = rows[0]["plausibility_gap"]
    large_gap = gap0 > 0.3
    ripple_helps = sum(r["local_ripple"] > r["local_plain"] + 0.02 for r in rows) >= 2
    # does global ceiling itself fall with divergence? (feasibility limit re-entering)
    ceiling_falls = rows[-1]["global_ceiling"] < rows[0]["global_ceiling"] - 0.1

    out = {
        "experiment": "T4-V2 reachability (local vs global) + V3 structured teaching",
        "config": {"n": N, "density": DENSITY, "episodes": 300},
        "per_divergence": rows,
        "plausibility_gap_at_zero": gap0,
        "large_plausibility_gap": bool(large_gap),
        "ripple_beats_plain": bool(ripple_helps),
        "global_ceiling_falls_with_divergence": bool(ceiling_falls),
        "verdict": (
            f"Global optimizer reaches {rows[0]['global_ceiling']:.2f} on the fixed topology but "
            f"local rules reach at most {max(rows[0]['local_plain'], rows[0]['local_ripple']):.2f} "
            f"-> plausibility gap {gap0:.2f}. "
            + ("Ripple-timing helps. " if ripple_helps else "Ripple-timing does not materially help. ")
            + ("Global ceiling also falls with divergence (feasibility limit)." if ceiling_falls
               else "Global ceiling robust to divergence here.")
        ),
    }
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "T4_v2.json").write_text(json.dumps(out, indent=2))
    print("div | global | local_plain | local_ripple | gap")
    for r in rows:
        print(f"  {r['divergence']:.1f} | {r['global_ceiling']:.2f}   | {r['local_plain']:.2f}"
              f"        | {r['local_ripple']:.2f}         | {r['plausibility_gap']:.2f}")
    print("VERDICT:", out["verdict"])
    return out


if __name__ == "__main__":
    run()
