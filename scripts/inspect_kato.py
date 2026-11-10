"""Inspect the Kato 2015 WT_NoStim group: worms, traces, neuron IDs."""
from pathlib import Path
import h5py
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "data" / "kato2015_WT_NoStim.mat"


def deref_str(f, ref):
    """Decode a MATLAB char array referenced by an HDF5 object reference."""
    try:
        arr = f[ref][()]
        chars = arr.flatten()
        return "".join(chr(int(c)) for c in chars if int(c) > 0)
    except Exception:
        return None


with h5py.File(path, "r") as f:
    g = f["WT_NoStim"]
    print("WT_NoStim fields:", list(g.keys()))
    for k in g.keys():
        item = g[k]
        print(f"  {k}: shape={getattr(item,'shape',None)} dtype={getattr(item,'dtype',None)}")

    # typical Kato fields: traces, IDs, deltaFOverF, tv (time vector), etc.
    for cand in ("traces", "deltaFOverF", "IDs", "tv", "NeuronIds", "fullIDs"):
        if cand in g:
            d = g[cand]
            print(f"\n== {cand} == shape={d.shape} dtype={d.dtype}")
            if d.dtype == h5py.ref_dtype:
                print("  (object references; dereferencing first element)")
                first = d[0, 0] if d.ndim == 2 else d[0]
                sub = f[first]
                print("  first ref ->", sub.shape, sub.dtype)
