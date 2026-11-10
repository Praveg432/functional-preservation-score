"""T4 global-optimizer upper bound: the best a NON-local method can do on the SAME fixed topology.

This is the 'plausibility gap' reference. We fit the host's plastic weights (on the fixed mask)
to match the target's states by linear least squares on the recurrent update — a global,
non-biological optimizer. The gap [global - local] quantifies what biological-plausibility costs,
and the global ceiling itself reveals whether the FIXED TOPOLOGY can host the target function at
all (the T2 feasibility limit, re-tested here as an upper bound).
"""

from __future__ import annotations

import numpy as np

from host_net import HostNet


def _states(net: HostNet, u):
    _, xs = net.run(u, return_states=True)
    return xs


def fit_global(host: HostNet, target: HostNet, train_inputs, ridge=1e-3) -> HostNet:
    """Least-squares fit of host.W (masked) so host state-transitions mimic target's.

    For each target trajectory we collect (x[t] -> pre-activation target) pairs and solve, per
    post-neuron i, for the weights on its EXISTING incoming edges only (respects fixed topology).
    """
    h = host.copy()
    n = h.W.shape[0]
    # gather target states and the desired pre-activation a[t] = atanh of target's step
    X, A = [], []
    for u in train_inputs:
        xs = _states(target, u)
        for t in range(1, len(xs)):
            # target produced x[t] from x[t-1]: invert leak+tanh to get desired recurrent drive
            x_prev, x_cur = xs[t - 1], xs[t]
            inner = (x_cur - (1 - target.leak) * x_prev) / target.leak
            inner = np.clip(inner, -0.999, 0.999)
            a = np.arctanh(inner) - target.W_in @ u[t]     # desired W @ x_prev per neuron
            X.append(x_prev)
            A.append(a)
    X = np.array(X)                   # (M, n)
    A = np.array(A)                   # (M, n)
    # solve per post-neuron i over its existing incoming edges
    for i in range(n):
        cols = np.where(h.mask[i])[0]
        if cols.size == 0:
            continue
        Xi = X[:, cols]
        G = Xi.T @ Xi + ridge * np.eye(cols.size)
        w = np.linalg.solve(G, Xi.T @ A[:, i])
        h.W[i, cols] = np.clip(w, -3.0, 3.0)
    return h


def global_ceiling(host, target, train_inputs, test_inputs) -> float:
    from installer import _fidelity
    h = fit_global(host, target, train_inputs)
    return _fidelity(h, target, test_inputs)
