"""Diagnose whether SigmoidConductanceModel has a non-trivial reference function at all.

If the full-precision model produces near-identical output across different stimuli, it has no
function to preserve and FPS=0 is correct-but-uninformative (degenerate model, not a real
refutation of Effect B). We measure the between-stimulus variance of the reference output.
"""
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from shared.connectome import load_celegans
from shared.model import ConnectomeModel, SigmoidConductanceModel, default_stimulus_bank

c = load_celegans(path=ROOT / "data" / "celegans_real.npz")

for name, cls in [("leaky_rate_tanh", ConnectomeModel), ("sigmoid_conductance", SigmoidConductanceModel)]:
    m = cls.from_connectome(c)
    stim = default_stimulus_bank(len(m.sensory_idx), n_patterns=8, T=40, seed=1)
    Y = np.stack([m.run(s) for s in stim])      # (P, T, n_motor)
    # how much does the output vary ACROSS stimuli (the signal FPS needs)?
    across_stim_var = float(Y.mean(axis=1).var(axis=0).mean())   # var of per-stim mean output
    within_range = float(Y.max() - Y.min())
    print(f"{name:22s} across-stimulus signal var={across_stim_var:.3e}  output range={within_range:.3f}  "
          f"motor-mean={Y.mean():.3f}")
