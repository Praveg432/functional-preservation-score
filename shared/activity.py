"""Real C. elegans whole-brain calcium activity loader (Kato et al. 2015, WT_NoStim).

Source: OSF osf.io/na4f9 (WT_NoStim.mat, MATLAB v7.3 / HDF5). 5 worms, per-worm
delta-F/F traces (n_neurons x n_timepoints), named neurons, sampling rate, behavioral states.

This is the expressive, biologically-grounded functional readout used to resolve the V4 block:
instead of a hand-built dynamics model, we fit a CONNECTOME-MASKED linear dynamics model to
predict real next-step activity, and score preservation of that predictive function under
compression (see tracks/T1 .../T1_v5_real_activity.py).

Contract:
    WormActivity:
      dff   : (n_neurons, T) float64  delta-F/F traces
      names : list[str]               neuron labels (may include '' for unidentified)
      fps   : float                   frames per second
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import h5py
import numpy as np

_DATA = Path(__file__).resolve().parents[1] / "data"
_KATO = _DATA / "kato2015_WT_NoStim.mat"


@dataclass(frozen=True)
class WormActivity:
    dff: np.ndarray
    names: list[str]
    fps: float

    @property
    def n_neurons(self) -> int:
        return self.dff.shape[0]

    @property
    def T(self) -> int:
        return self.dff.shape[1]

    def identified(self) -> np.ndarray:
        """Indices of neurons with a non-empty label (matchable to the connectome)."""
        return np.array([i for i, n in enumerate(self.names) if n and n.strip()], dtype=int)


def _deref_name(f, ref) -> str:
    try:
        arr = f[ref][()]
        return "".join(chr(int(c)) for c in np.asarray(arr).flatten() if int(c) > 0)
    except Exception:
        return ""


def load_kato(path: str | Path = _KATO, worm: int = 0) -> WormActivity:
    """Load one worm's whole-brain activity from the Kato 2015 WT_NoStim file."""
    with h5py.File(path, "r") as f:
        g = f["WT_NoStim"]
        dff = np.asarray(f[g["deltaFOverF"][worm, 0]][()], dtype=np.float64)
        # stored as (T, n) or (n, T); Kato stores (T, n) -> transpose to (n, T)
        if dff.shape[0] > dff.shape[1]:
            dff = dff.T
        fps_ref = g["fps"][worm, 0]
        fps = float(np.asarray(f[fps_ref][()]).flatten()[0])

        names: list[str] = []
        nn = g["NeuronNames"][worm, 0]
        nn_obj = f[nn]
        # NeuronNames[worm] is itself an array of refs to char arrays
        flat = np.asarray(nn_obj[()]).flatten()
        for r in flat:
            if isinstance(r, h5py.Reference):
                names.append(_deref_name(f, r))
            else:
                names.append("")
        # align name count to neuron count
        if len(names) < dff.shape[0]:
            names += [""] * (dff.shape[0] - len(names))
        names = names[: dff.shape[0]]

    return WormActivity(dff=dff, names=names, fps=fps)


def n_worms(path: str | Path = _KATO) -> int:
    with h5py.File(path, "r") as f:
        return int(f["WT_NoStim"]["deltaFOverF"].shape[0])
