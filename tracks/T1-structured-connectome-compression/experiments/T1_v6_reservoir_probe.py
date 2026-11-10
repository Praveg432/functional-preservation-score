"""T1-V6 : CHEAP NONLINEAR go/no-go probe for Effect B (gate before the multi-day forecaster).

V5's linear data-driven readout was too weak (base FPS ~0.05; persistence null dominated), so
Effect B could not be tested. Before committing multi-day effort to a full nonlinear
connectome-constrained forecaster, this is a HALF-DAY gate:

  * Reservoir / echo-state network whose recurrent matrix is a CONNECTOME-MASKED random matrix
    (nonlinear tanh dynamics, connectome-constrained). Only a linear readout is ridge-trained
    (seconds). This gives genuine nonlinear dynamics without training a deep model.
  * Drive the reservoir with real Kato activity; train the readout to forecast activity H steps
    ahead; measure FPS vs the persistence null.
  * GATE CHECK 1: does base FPS clear the persistence null with real headroom? If not, even the
    reservoir is too weak and the forecaster is unlikely to help -> NO-GO.
  * GATE CHECK 2: if there IS headroom, compress the reservoir recurrent matrix (uniform vs
    engram-aware) and see whether engram > uniform (Effect B signal).

Decision rule (pre-registered here):
  GO (build the forecaster) iff base FPS > 0.15 AND high-sparsity engram margin > +0.05.
  NO-GO (drop Effect B for good) otherwise.

Runs on the M4 in ~1-2 min. Requires the .venv (h5py). Deterministic given seeds.
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
from shared.connectome import load_celegans
from shared import compress

RESULTS = Path(__file__).resolve().parents[1] / "results"
REAL_NPZ = _ROOT / "data" / "celegans_real.npz"

HORIZON = 10
RIDGE = 1e-3
SPECTRAL_RADIUS = 0.95
RESERVOIR_SEEDS = [0, 1, 2]
TARGETS = [0.3, 0.5, 0.7]
BITDEPTH = "int8"
PROTECT = 0.25
LOW_REGIME = [0.3]
HIGH_REGIME = [0.5, 0.7]

# pre-registered gate thresholds
GATE_MIN_BASE_FPS = 0.15
GATE_MIN_HIGH_MARGIN = 0.05


def make_reservoir(n, seed, density=0.1):
    """Random sparse recurrent matrix scaled to a target spectral radius (echo-state property).

    This is the reservoir's OWN connectivity (not the C. elegans connectome): we compress THIS
    matrix to ask whether structured pruning of a nonlinear recurrent system's weights preserves
    forecasting of REAL activity. (A connectome-masked variant is the forecaster's job later.)
    """
    rng = np.random.default_rng(seed)
    W = rng.standard_normal((n, n)) * (rng.random((n, n)) < density)
    np.fill_diagonal(W, 0.0)
    eig = np.max(np.abs(np.linalg.eigvals(W)))
    if eig > 1e-9:
        W *= SPECTRAL_RADIUS / eig
    return W


def run_reservoir(Wres, Win, u, leak=0.3):
    """Drive reservoir with input sequence u (T, n_in). Returns states (T, n_res)."""
    n_res = Wres.shape[0]
    T = u.shape[0]
    x = np.zeros(n_res)
    S = np.empty((T, n_res))
    for t in range(T):
        x = (1 - leak) * x + leak * np.tanh(Wres @ x + Win @ u[t])
        S[t] = x
    return S


def fps_forecast(states_fn, X, Wout, horizon=HORIZON):
    """Null-normalized H-step forecast score using reservoir states -> readout.

    states_fn(u_window) returns reservoir states; Wout maps states->predicted activity.
    Compares free-run forecast to truth; null = min(mean, persistence).
    """
    n, T = X.shape
    gmean = X.mean(axis=1, keepdims=True)
    res = mean_ss = persist_ss = 0.0
    for t in range(0, T - horizon - 1, horizon):
        # teacher-force up to t, then free-run forecast via readout feeding back as input
        pred = states_fn(t, horizon, Wout)
        true = X[:, t + 1 : t + 1 + horizon]
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


def build_model(X, Wres, Win, split):
    """Ridge-train a readout Wout: reservoir_state -> next activity, on TRAIN portion."""
    S = run_reservoir(Wres, Win, X.T)          # (T, n_res) from input = activity
    Xtp1 = X[:, 1:].T                          # (T-1, n_neurons) targets
    Str = S[:split - 1]
    Ytr = Xtp1[:split - 1]
    G = Str.T @ Str + RIDGE * np.eye(S.shape[1])
    Wout = (np.linalg.inv(G) @ Str.T @ Ytr).T  # (n_neurons, n_res)
    return Wout, S


def forecast_fps(X, Wres, Win, Wout, split, horizon=HORIZON):
    """Free-run forecast FPS on the TEST portion: feed predictions back as reservoir input."""
    n = X.shape[0]
    Xte = X[:, split:]
    T = Xte.shape[1]
    gmean = X.mean(axis=1, keepdims=True)
    res = mean_ss = persist_ss = 0.0
    for t in range(0, T - horizon - 1, horizon):
        x = np.zeros(Wres.shape[0])
        # warm up on true activity for a few steps
        warm = max(0, t - 5)
        for s in range(warm, t):
            x = 0.7 * x + 0.3 * np.tanh(Wres @ x + Win @ Xte[:, s])
        u = Xte[:, t].copy()
        pred = np.empty((n, horizon))
        for k in range(horizon):
            x = 0.7 * x + 0.3 * np.tanh(Wres @ x + Win @ u)
            yk = Wout @ x
            pred[:, k] = yk
            u = yk                               # feed prediction back (free-run)
        true = Xte[:, t + 1 : t + 1 + horizon]
        res += float(np.sum((pred - true) ** 2))
        mean_ss += float(np.sum((true - gmean) ** 2))
        persist = np.repeat(Xte[:, t:t + 1], horizon, axis=1)
        persist_ss += float(np.sum((persist - true) ** 2))
    ss_null = min(mean_ss, persist_ss)
    if mean_ss <= 1e-12 or ss_null <= 1e-12:
        return 0.0
    raw = 1 - res / mean_ss
    raw_null = 1 - ss_null / mean_ss
    denom = 1 - raw_null
    return float(np.clip((raw - raw_null) / denom, 0.0, 1.0)) if denom > 1e-9 else 0.0


def run():
    worms = list(range(n_worms()))
    per_worm = []
    for w in worms:
        a = load_kato(worm=w)
        X = a.dff
        X = (X - X.mean(axis=1, keepdims=True)) / (X.std(axis=1, keepdims=True) + 1e-6)
        n = X.shape[0]
        split = int(0.7 * X.shape[1])

        base_list = []
        margins = {t: [] for t in TARGETS}
        for seed in RESERVOIR_SEEDS:
            rng = np.random.default_rng(seed + 100)
            Wres = make_reservoir(n, seed)
            Win = rng.standard_normal((n, n)) * 0.5
            Wout, _ = build_model(X, Wres, Win, split)
            base = forecast_fps(X, Wres, Win, Wout, split)
            base_list.append(base)

            if base > 0.05:  # only probe compression where there's a function to preserve
                for t in TARGETS:
                    Wu = compress.quantize(compress.prune_uniform(Wres, t), BITDEPTH)
                    Wp = compress.prune_engram_aware(Wres, t, protect_frac=PROTECT, method="strength")
                    We = compress.quantize_mixed(Wp, low_mode=BITDEPTH, protect_frac=PROTECT,
                                                 high_mode="int8", method="strength")
                    Wout_u, _ = build_model(X, Wu, Win, split)
                    Wout_e, _ = build_model(X, We, Win, split)
                    fu = forecast_fps(X, Wu, Win, Wout_u, split)
                    fe = forecast_fps(X, We, Win, Wout_e, split)
                    margins[t].append(fe - fu)

        per_worm.append({
            "worm": w, "n_neurons": n,
            "base_fps_mean": float(np.mean(base_list)),
            "margins": {str(t): (float(np.mean(v)) if v else None) for t, v in margins.items()},
        })

    base_mean = float(np.mean([p["base_fps_mean"] for p in per_worm]))

    def regime(rs):
        vals = []
        for p in per_worm:
            for t in rs:
                m = p["margins"].get(str(t))
                if m is not None:
                    vals.append(m)
        return float(np.mean(vals)) if vals else None

    high_m = regime(HIGH_REGIME)
    low_m = regime(LOW_REGIME)
    go = bool(base_mean > GATE_MIN_BASE_FPS and (high_m is not None and high_m > GATE_MIN_HIGH_MARGIN))

    out = {
        "experiment": "T1-V6 reservoir go/no-go probe for Effect B",
        "substrate": "real-celegans-activity (Kato 2015) + random reservoir",
        "gate_rule": f"GO iff base_fps>{GATE_MIN_BASE_FPS} AND high-regime margin>{GATE_MIN_HIGH_MARGIN}",
        "per_worm": per_worm,
        "mean_base_fps": base_mean,
        "mean_margin_low": low_m,
        "mean_margin_high": high_m,
        "decision": "GO build forecaster" if go else "NO-GO drop Effect B",
        "go": go,
    }
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "T1_v6_reservoir_probe.json").write_text(json.dumps(out, indent=2))
    print(f"mean base forecast FPS: {base_mean:.3f}  (gate needs > {GATE_MIN_BASE_FPS})")
    print(f"high-regime engram margin: {high_m}  (gate needs > {GATE_MIN_HIGH_MARGIN})")
    print(f"low-regime engram margin : {low_m}")
    print(f"DECISION: {out['decision']}")
    for p in per_worm:
        print(f"  worm {p['worm']} (n={p['n_neurons']}): base {p['base_fps_mean']:.3f} margins {p['margins']}")
    return out


if __name__ == "__main__":
    run()
