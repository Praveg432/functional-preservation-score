"""T5 ablation: lesion a neuron set and measure the functional effect via FPS.

Reuses the T1 substrate: a connectome-driven leaky-rate dynamics model (shared.model) and the
FPS metric (shared.fps). "Function" = the motor-readout response to the standard stimulus
battery. Ablating a set of neurons = zeroing their rows+columns in W (removing them from the
dynamics). We then score how much the intact function is preserved (FPS vs the un-lesioned
reference).

Two function families, so we can ask about dissociation:
  * global function : the full motor readout (what the whole network computes).
  * payload-driven  : the component of the readout that depends on payload activity (measured
                      by how much ablating the OTHER side degrades it).
"""

from __future__ import annotations

import numpy as np

from shared.connectome import Connectome
from shared.model import ConnectomeModel, default_stimulus_bank
from shared.fps import Battery


def lesion(W: np.ndarray, kill: np.ndarray) -> np.ndarray:
    """Return W with neurons in boolean mask `kill` removed (rows+cols zeroed)."""
    out = W.copy()
    out[kill, :] = 0.0
    out[:, kill] = 0.0
    return out


def make_battery(c: Connectome, n_patterns=8, T=40, seed=1):
    model = ConnectomeModel.from_connectome(c)
    stim = default_stimulus_bank(len(model.sensory_idx), n_patterns=n_patterns, T=T, seed=seed)
    bat = Battery(stim, model.run)
    return model, bat


def fps_after_lesion(c: Connectome, model, bat, kill: np.ndarray) -> float:
    """FPS of the lesioned network's motor readout vs the intact reference."""
    W_les = lesion(c.W, kill)
    return bat.score(model.with_weights(W_les).run).fps
