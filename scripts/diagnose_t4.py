"""Is T4-V1's weak local install a real gap or a weak instrument? Check the global ceiling.

If the GLOBAL optimizer reaches the target on the same fixed topology but LOCAL rules don't,
that's the plausibility-gap finding. If global ALSO fails, the topology can't host the function
(T2 feasibility limit) and the local result is uninformative.
"""
import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tracks/T4-insilico-write-compiler/src"))
from host_net import HostNet
import installer as inst
import global_baseline as gb

N, D_IN, D_OUT, DENSITY = 40, 3, 2, 0.2


def make_inputs(d_in, k, T, seed):
    rng = np.random.default_rng(seed)
    raw = rng.standard_normal((k, T, d_in))
    for _ in range(3):
        raw[:, 1:-1] = 0.25 * raw[:, :-2] + 0.5 * raw[:, 1:-1] + 0.25 * raw[:, 2:]
    return [raw[i] for i in range(k)]


for seed in (0, 1, 2):
    host = HostNet.random(N, D_IN, D_OUT, DENSITY, seed=seed)
    target = host.copy()
    rng = np.random.default_rng(seed + 999)
    target.W = rng.standard_normal((N, N)) * 0.3 * host.mask
    tr = make_inputs(D_IN, 8, 30, seed)
    te = make_inputs(D_IN, 4, 30, seed + 50)
    ctrl = inst.no_plasticity_fidelity(host, target, te)
    glob = gb.global_ceiling(host, target, tr, te)
    loc = inst.install(host, target, tr, te, episodes=300, seed=seed)["fidelity"]
    print(f"seed {seed}: control={ctrl:.3f}  LOCAL={loc:.3f}  GLOBAL_ceiling={glob:.3f}")
