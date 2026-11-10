"""Is the reservoir readout learning anything at all? Teacher-forced vs free-run.

If teacher-forced forecast has headroom but free-run collapses, the probe's FREE-RUN is the
problem (compounding divergence), not the reservoir. We then fix the readout target (predict
H-step-ahead directly, teacher-forced) rather than free-running.
"""
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from shared.activity import load_kato

def reservoir(n, seed, density=0.1, sr=0.95):
    rng = np.random.default_rng(seed)
    W = rng.standard_normal((n, n)) * (rng.random((n, n)) < density)
    np.fill_diagonal(W, 0.0)
    e = np.max(np.abs(np.linalg.eigvals(W)))
    if e > 1e-9: W *= sr / e
    return W

def states(Wres, Win, U, leak=0.3):
    n = Wres.shape[0]; T = U.shape[0]; x = np.zeros(n); S = np.empty((T, n))
    for t in range(T):
        x = (1-leak)*x + leak*np.tanh(Wres@x + Win@U[t]); S[t] = x
    return S

for w in [0, 4]:
    a = load_kato(worm=w); X = a.dff
    X = (X - X.mean(1, keepdims=True)) / (X.std(1, keepdims=True)+1e-6)
    n = X.shape[0]; split = int(0.7*X.shape[1]); H = 10
    rng = np.random.default_rng(1); Wres = reservoir(n, 0); Win = rng.standard_normal((n, n))*0.5
    S = states(Wres, Win, X.T)
    # teacher-forced H-step-ahead readout: state[t] -> X[t+H]
    St, Yt = S[:split-H], X[:, H:split].T
    G = St.T@St + 1e-3*np.eye(n); Wout = (np.linalg.inv(G)@St.T@Yt).T
    Ste = S[split:-H]; true = X[:, split+H:].T
    pred = (Wout@Ste.T).T
    ss_res = np.sum((pred-true)**2); 
    gmean = X.mean(1); ss_mean = np.sum((true-gmean)**2)
    persist = X[:, split:X.shape[1]-H].T; ss_persist = np.sum((persist-true)**2)
    r2_vs_mean = 1 - ss_res/ss_mean
    r2_vs_persist = 1 - ss_res/ss_persist
    print(f"worm {w} (n={n}): teacher-forced H={H} readout  R2_vs_mean={r2_vs_mean:+.3f}  "
          f"R2_vs_persistence={r2_vs_persist:+.3f}  (persist beats mean by {1-ss_persist/ss_mean:+.3f})")
