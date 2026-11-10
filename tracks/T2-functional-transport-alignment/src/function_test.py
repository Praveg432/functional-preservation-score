"""T2 function test: does the transported circuit reproduce A's input->output function?

We build A's reference function (motor readout over the standard battery) with the T1 model, then
run B (same role layout, permuted) with the TRANSPORTED weights, and score FPS of B's readout
against A's reference. Because B is a node-permutation of A, B's sensory/motor indices are the
images of A's under the correspondence, so the I/O interface is matched automatically when the
correspondence is correct.

Returns transport fidelity in [0,1] (FPS of transported-B vs intact-A function).
"""

from __future__ import annotations

import numpy as np

from shared.connectome import Connectome
from shared.model import ConnectomeModel, default_stimulus_bank
from shared.fps import Battery


def build_reference(c_A: Connectome):
    """A's reference model + battery (the function to be reproduced after transport)."""
    model_A = ConnectomeModel.from_connectome(c_A)
    stim = default_stimulus_bank(len(model_A.sensory_idx), n_patterns=8, T=40, seed=1)
    bat = Battery(stim, model_A.run)
    return model_A, bat


def transport_fidelity(model_A, bat, W_B_transported: np.ndarray,
                       sensory_idx_B: np.ndarray, motor_idx_B: np.ndarray) -> float:
    """FPS of B (with transported weights) vs A's reference function.

    B uses its own sensory/motor indices (images of A's under the correspondence). The battery's
    reference outputs are A's; we score B's outputs against them.
    """
    model_B = ConnectomeModel(
        W=W_B_transported,
        sensory_idx=sensory_idx_B,
        motor_idx=motor_idx_B,
        leak=model_A.leak, gain=model_A.gain, bias=model_A.bias,
    )
    return bat.score(model_B.run).fps
