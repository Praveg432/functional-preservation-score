"""T4 local plasticity rules — STRICTLY local (audited: no backprop, no gradient-to-target).

Each rule updates a plastic weight W[i,j] (edge j->i on the fixed mask) using ONLY:
  * pre-synaptic activity  x_j
  * post-synaptic activity x_i
  * a GLOBAL scalar signal : a reward/error magnitude r in [-1,1] (neuromodulatory broadcast)
  * optionally a GLOBAL gate g in {0,1} (sharp-wave-ripple window)
plus homeostatic weight decay. This is reward-modulated Hebbian / three-factor plasticity, the
standard biologically-plausible family. There is NO per-weight gradient of the target loss.

The global scalar r is the only teaching signal the "write" is allowed — exactly the blueprint's
premise (a broadcast ripple/neuromodulator entrains plasticity), not surgical per-synapse control.
"""

from __future__ import annotations

import numpy as np


def reward_modulated_hebb(W, mask, x_pre, x_post, reward, lr=0.02, decay=1e-3, gate=1.0):
    """Three-factor update: dW[i,j] = gate * lr * reward * x_post[i] * x_pre[j] - decay*W.

    reward is a SINGLE global scalar (broadcast), x_pre/x_post are the network's own activities.
    No target weights, no gradients. Returns updated W (masked to fixed topology).
    """
    hebb = np.outer(x_post, x_pre)                 # (n,n) local coincidence
    dW = gate * lr * reward * hebb - decay * W
    W = W + dW * mask                               # only existing edges change
    # keep weights bounded (homeostatic clip)
    return np.clip(W, -3.0, 3.0)


def ripple_gate(t, period=5, width=2):
    """Structured teaching: plasticity only ON during periodic 'ripple' windows (g=1 else 0).

    Models sleep sharp-wave-ripple-timed consolidation: learning is gated to replay windows.
    """
    phase = t % period
    return 1.0 if phase < width else 0.0


# Audit helper: assert a rule never sees target weights (used in tests).
LOCAL_SIGNALS = ("x_pre", "x_post", "reward", "gate")
