"""T4 installer: drive the host toward a target I/O function using ONLY local rules + a global
reward scalar. This is the in-silico "write-compiler".

Loop (episodic, three-factor):
  for each episode:
    pick a teaching input u; run host -> y_host, states x; run target -> y_target
    global_error = mean squared error (a SINGLE scalar); reward = -(error - running_baseline)
    for each timestep: apply reward_modulated_hebb using the host's own x_pre/x_post and reward,
      gated by the (optional) ripple window.
No per-weight target gradient is ever used (audited). Fidelity = FPS-style preservation of the
target function on held-out inputs.
"""

from __future__ import annotations

import numpy as np

from host_net import HostNet
import local_rules as lr


def _fidelity(host: HostNet, target: HostNet, inputs) -> float:
    """Null-normalized agreement of host output with target output (R^2-style, clipped)."""
    res = tot = 0.0
    for u in inputs:
        yh = host.run(u)
        yt = target.run(u)
        res += float(np.sum((yh - yt) ** 2))
        tot += float(np.sum((yt - yt.mean(axis=0, keepdims=True)) ** 2))
    if tot <= 1e-12:
        return 0.0
    return float(np.clip(1 - res / tot, 0.0, 1.0))


def install(host: HostNet, target: HostNet, train_inputs, test_inputs,
            episodes=300, lr_rate=0.02, use_ripple=False, seed=0):
    """Install target's function into host via local rules + global reward. Returns dict."""
    rng = np.random.default_rng(seed)
    h = host.copy()
    baseline = None
    for ep in range(episodes):
        u = train_inputs[rng.integers(len(train_inputs))]
        yh, xs = h.run(u, return_states=True)
        yt = target.run(u)
        err = float(np.mean((yh - yt) ** 2))
        if baseline is None:
            baseline = err
        reward = np.tanh(baseline - err)         # positive if better than running baseline
        baseline = 0.95 * baseline + 0.05 * err
        # apply local rule across the episode's timesteps
        for t in range(1, xs.shape[0]):
            g = lr.ripple_gate(t) if use_ripple else 1.0
            h.W = lr.reward_modulated_hebb(h.W, h.mask, x_pre=xs[t - 1], x_post=xs[t],
                                           reward=reward, lr=lr_rate, gate=g)
    return {
        "fidelity": _fidelity(h, target, test_inputs),
        "final_host": h,
    }


def no_plasticity_fidelity(host: HostNet, target: HostNet, test_inputs) -> float:
    """Control: host fidelity to target with NO learning (random init baseline)."""
    return _fidelity(host, target, test_inputs)
