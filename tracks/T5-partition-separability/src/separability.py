"""T5 separability index (v2, corrected) — measured with a FIXED I/O interface.

V1 diagnosis exposed a design flaw: ablating "Base-OS = sensory+motor" trivially kills function
because it deletes the very input and readout neurons the metric depends on (FPS -> 0 for every
partition, including nulls). Separability as "payload standalone function" is ill-posed when the
Base-OS *is* the I/O.

Corrected framing (matches the blueprint's real question): the Base-OS (sensory inputs + motor
outputs) is the FIXED interface and is NEVER ablated. The "payload" is the interneuron core that
TRANSFORMS input->output. Separability asks: is the asserted payload a privileged carrier of the
input->output transformation, i.e. does ablating it degrade function MORE than ablating a random
interneuron subset of equal size? If not, the "identity payload" is not a special separable
module — a corrective to the blueprint.

Metric (all FPS of the motor readout vs the intact reference; I/O fixed):
  * payload_ablation_drop = 1 - FPS(ablate payload interneurons)
  * compared to a null of random equal-size INTERNEURON subsets.
  z>0 and high percentile => the asserted payload carries disproportionate transformation
  (separable/privileged). z~=0 => no more special than any random interneuron set (H2).
"""

from __future__ import annotations

import numpy as np

import ablate


def transformation_drop(c, model, bat, kill: np.ndarray) -> float:
    """1 - FPS after ablating `kill` (interneurons only; I/O interface untouched)."""
    return 1.0 - ablate.fps_after_lesion(c, model, bat, kill=kill)


def payload_privilege(c, model, bat, is_payload: np.ndarray, inter_mask: np.ndarray,
                      n_null: int = 40, seed: int = 0) -> dict:
    """Is the asserted payload a privileged carrier of the I/O transformation vs random
    equal-size interneuron subsets?

    is_payload  : boolean mask of the asserted payload (should be within interneurons).
    inter_mask  : boolean mask of all interneurons (the pool random nulls draw from).
    """
    # restrict the asserted payload to interneurons (never ablate I/O)
    payload = is_payload & inter_mask
    k = int(payload.sum())
    drop = transformation_drop(c, model, bat, payload)

    inter_idx = np.where(inter_mask)[0]
    rng = np.random.default_rng(seed)
    null = []
    for _ in range(n_null):
        sub = np.zeros(c.n, dtype=bool)
        sub[rng.choice(inter_idx, size=min(k, len(inter_idx)), replace=False)] = True
        null.append(transformation_drop(c, model, bat, sub))
    null = np.array(null)
    mu, sd = float(null.mean()), float(null.std())
    return {
        "payload_size": k,
        "payload_ablation_drop": drop,
        "null_mean_drop": mu, "null_std_drop": sd,
        "z_vs_null": (drop - mu) / (sd + 1e-9),
        "percentile_vs_null": float((null < drop).mean()),
    }
