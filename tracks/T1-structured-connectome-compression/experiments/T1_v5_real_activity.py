"""T1-V5 : resolve the Effect-B block using REAL neural activity (no hand-built dynamics).

The V4 hardening showed the engram-vs-uniform advantage flips with the dynamics model, so it
could not be claimed. The fix (per RESULTS/T1_v4_notes): use an EXPRESSIVE, BIOLOGICALLY-
GROUNDED readout. Here we use real Kato-2015 whole-brain calcium traces and a DATA-DRIVEN model:

  1. Fit a linear next-step predictor A on real activity:  x[t+1] ~= A x[t]  (ridge, on TRAIN).
     A is the "functional interaction matrix" learned from real dynamics -- no synthetic model.
  2. The function to preserve = one-step prediction of HELD-OUT real activity.
     FPS_activity = 1 - MSE(pred, true)/MSE(mean-predictor, true), null-normalized, clipped.
  3. Compress A (prune + quantize) with UNIFORM vs ENGRAM-AWARE (strength hubs), swept over
     matched effective sparsity, and measure how much held-out predictive function survives.

If engram-aware's advantage (or lack of it) on REAL activity matches V4's leaky-rate finding,
Effect B is model-robust; if it matches the sigmoid finding, Effect B is refuted on real data.
Either way the block is resolved honestly.

Runs on the M4 in seconds per worm. Requires the h5py venv (.venv). Deterministic.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from shared.activity import load_kato, n_worms
from shared import compress

RESULTS = Path(__file__).resolve().parents[1] / "results"
TARGETS = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
BITDEPTH = "int8"          # clean matched comparison (no quant floor), as in V4
PROTECT = 0.25
RIDGE = 1e-2
LOW_REGIME = [0.3, 0.4]
HIGH_REGIME = [0.5, 0.6, 0.7]


def fit_A(X):
    """Ridge-fit A for x[t+1] = A x[t] on columns of X (n, T). Returns A (n, n)."""
    Xt = X[:, :-1]           # (n, T-1)
    Xtp1 = X[:, 1:]          # (n, T-1)
    n = X.shape[0]
    G = Xt @ Xt.T + RIDGE * np.eye(n)
    A = Xtp1 @ Xt.T @ np.linalg.inv(G)
    return A


HORIZON = 10               # multi-step forecast; persistence fails here, so the model must work


def _rollout(A, x0, steps):
    """Free-run A for `steps` from x0 (n,). Returns (n, steps) forecast."""
    out = np.empty((x0.shape[0], steps))
    x = x0.copy()
    for k in range(steps):
        x = A @ x
        out[:, k] = x
    return out


def fps_predict(A, X, horizon=HORIZON):
    """Null-normalized H-STEP forecast score of A on held-out X.

    For each start t, free-run A for `horizon` steps and compare to the true trajectory.
    Nulls: predict-the-mean and PERSISTENCE (hold x[t] for H steps). One-step persistence is
    trivially strong for smooth calcium, but it FAILS over a horizon -- forcing the model to
    capture real dynamics, which is what discriminates compression methods.
    """
    n, T = X.shape
    starts = range(0, T - horizon, horizon)   # non-overlapping windows
    res = mean_ss = persist_ss = 0.0
    gmean = X.mean(axis=1, keepdims=True)
    for t in starts:
        true = X[:, t + 1 : t + 1 + horizon]
        pred = _rollout(A, X[:, t], horizon)
        res += float(np.sum((pred - true) ** 2))
        mean_ss += float(np.sum((true - gmean) ** 2))
        persist = np.repeat(X[:, t:t + 1], horizon, axis=1)
        persist_ss += float(np.sum((persist - true) ** 2))
    ss_null = min(mean_ss, persist_ss)
    if mean_ss <= 1e-12 or ss_null <= 1e-12:
        return 0.0
    raw = 1 - res / mean_ss
    raw_null = 1 - ss_null / mean_ss
    denom = 1 - raw_null
    return float(np.clip((raw - raw_null) / denom, 0.0, 1.0)) if denom > 1e-9 else 0.0


def _compress_to_target(A, policy, target):
    lo, hi, best = 0.0, 1.0, None
    for _ in range(16):
        mid = 0.5 * (lo + hi)
        if policy == "uniform":
            Ac = compress.quantize(compress.prune_uniform(A, mid), BITDEPTH)
        else:
            pruned = compress.prune_engram_aware(A, mid, protect_frac=PROTECT, method="strength")
            Ac = compress.quantize_mixed(pruned, low_mode=BITDEPTH, protect_frac=PROTECT,
                                         high_mode="int8", method="strength")
        s = compress.actual_sparsity(A, Ac)
        best = Ac
        lo, hi = (mid, hi) if s < target else (lo, mid)
    return best


def run_worm(worm):
    a = load_kato(worm=worm)
    X = a.dff
    X = (X - X.mean(axis=1, keepdims=True)) / (X.std(axis=1, keepdims=True) + 1e-6)
    T = X.shape[1]
    split = int(0.7 * T)
    Xtr, Xte = X[:, :split], X[:, split:]
    A = fit_A(Xtr)
    base_fps = fps_predict(A, Xte)

    rows = []
    for t in TARGETS:
        fu = fps_predict(_compress_to_target(A, "uniform", t), Xte)
        fe = fps_predict(_compress_to_target(A, "engram", t), Xte)
        rows.append({"target": t, "fps_uniform": fu, "fps_engram": fe, "margin": fe - fu})
    return {"worm": worm, "n_neurons": a.n_neurons, "base_fps": base_fps, "curve": rows}


def run():
    worms = []
    for w in range(n_worms()):
        worms.append(run_worm(w))

    # aggregate regime margins across worms
    def regime_margin(regime):
        vals = []
        for wd in worms:
            vals += [r["margin"] for r in wd["curve"] if r["target"] in regime]
        return float(np.mean(vals))

    low_m = regime_margin(LOW_REGIME)
    high_m = regime_margin(HIGH_REGIME)
    # V4 leaky-rate pattern was: uniform wins low (margin<0), engram wins high (margin>0)
    matches_leaky = (low_m < 0) and (high_m > 0)

    out = {
        "experiment": "T1-V5 Effect-B on REAL activity (Kato 2015, data-driven dynamics)",
        "substrate": "real-celegans-activity",
        "bitdepth": BITDEPTH,
        "per_worm": worms,
        "mean_margin_low_regime": low_m,
        "mean_margin_high_regime": high_m,
        "reproduces_leaky_rate_boundary": bool(matches_leaky),
        "mean_base_fps": float(np.mean([w["base_fps"] for w in worms])),
    }
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "T1_v5_real_activity.json").write_text(json.dumps(out, indent=2))
    print(f"mean base predictive FPS: {out['mean_base_fps']:.3f}")
    print(f"low-regime margin (eng-uni): {low_m:+.3f}   high-regime margin: {high_m:+.3f}")
    print(f"reproduces leaky-rate boundary (uni wins low, eng wins high): {matches_leaky}")
    for wd in worms:
        ms = " ".join(f"{r['target']}:{r['margin']:+.2f}" for r in wd["curve"])
        print(f"  worm {wd['worm']} (n={wd['n_neurons']}, base {wd['base_fps']:.2f}): {ms}")
    return out


if __name__ == "__main__":
    run()
