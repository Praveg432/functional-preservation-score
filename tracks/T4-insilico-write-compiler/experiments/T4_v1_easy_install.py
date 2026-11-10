"""T4-V1 : local-rule installs *something* gate.

On a host whose topology MATCHES the target's (low divergence), do local rules (reward-modulated
Hebbian + global reward) move the host output toward the target function, above the no-plasticity
control? If local rules install nothing even here, the in-silico write is incoherent.

Target shares the host's input/output projections (W_in, W_out) and topology mask, differing only
in recurrent weights -> the only thing to "install" is the recurrent weight set on fixed edges.

Pass: installed fidelity > no-plasticity control by a clear margin (>0.1), on >=2 seeds.
Writes results/T4_v1.json. Needs .venv.
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

RESULTS = Path(__file__).resolve().parents[1] / "results"
N, D_IN, D_OUT, DENSITY = 40, 3, 2, 0.2
SEEDS = [0, 1, 2]


def make_inputs(d_in, n_patterns, T, seed):
    rng = np.random.default_rng(seed)
    raw = rng.standard_normal((n_patterns, T, d_in))
    for _ in range(3):
        raw[:, 1:-1] = 0.25 * raw[:, :-2] + 0.5 * raw[:, 1:-1] + 0.25 * raw[:, 2:]
    return [raw[i] for i in range(n_patterns)]


def build_pair(seed):
    """Host and target share W_in/W_out/mask; target has different recurrent weights."""
    host = HostNet.random(N, D_IN, D_OUT, DENSITY, seed=seed)
    target = host.copy()
    rng = np.random.default_rng(seed + 999)
    target.W = rng.standard_normal((N, N)) * 0.3 * host.mask   # different recurrent weights
    return host, target


def run():
    rows = []
    for seed in SEEDS:
        host, target = build_pair(seed)
        tr = make_inputs(D_IN, 8, 30, seed=seed)
        te = make_inputs(D_IN, 4, 30, seed=seed + 50)
        ctrl = inst.no_plasticity_fidelity(host, target, te)
        res = inst.install(host, target, tr, te, episodes=300, use_ripple=False, seed=seed)
        rows.append({"seed": seed, "control_fidelity": ctrl,
                     "installed_fidelity": res["fidelity"],
                     "gain": res["fidelity"] - ctrl})

    gains = [r["gain"] for r in rows]
    passed = sum(g > 0.1 for g in gains) >= 2

    out = {
        "gate": "T4-V1 local-rule installs something",
        "config": {"n": N, "density": DENSITY, "episodes": 300},
        "per_seed": rows,
        "mean_control": float(np.mean([r["control_fidelity"] for r in rows])),
        "mean_installed": float(np.mean([r["installed_fidelity"] for r in rows])),
        "mean_gain": float(np.mean(gains)),
        "criterion": "installed - control > 0.1 on >=2/3 seeds",
        "passed": bool(passed),
    }
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "T4_v1.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    run()
