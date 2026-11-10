"""Verify we can parse the nelpy linear-track hippocampal session (spikes + position)."""
from pathlib import Path
import numpy as np
from scipy.io import loadmat

ROOT = Path(__file__).resolve().parents[1]
H = ROOT / "data" / "hippocampus"

mat = loadmat(H / "spikes.mat")
sp = mat["spikes"]
print("spikes top:", type(sp), sp.dtype, sp.shape)


def _as_times(field):
    """Unwrap a 'time' field to a 1-D float array of spike times (handles nested object cells)."""
    a = np.asarray(field)
    while a.dtype == object and a.size >= 1:
        a = np.asarray(a.ravel()[0])
    return a.ravel().astype(float) if a.size else np.array([])


def extract_times(obj, out):
    """Recursively pull any 'time' arrays out of the nested MatClust structure."""
    a = np.asarray(obj)
    if a.dtype.names and "time" in a.dtype.names:
        for elem in a.ravel():
            t = _as_times(elem["time"])
            if t.size:
                out.append(t)
        return
    if a.dtype == object:
        for elem in a.ravel():
            if np.asarray(elem).size:
                extract_times(elem, out)


spikes = []
extract_times(sp, spikes)
spikes = [s for s in spikes if s.size > 0]
print(f"units parsed: {len(spikes)}")
if spikes:
    allt = np.concatenate(spikes)
    dur = allt.max() - allt.min()
    print(f"spike time range: {allt.min():.2f} .. {allt.max():.2f}  total spikes: {allt.size}  dur: {dur:.1f}")
    rates = [len(s) / dur for s in spikes]
    print(f"per-unit rate Hz: min {min(rates):.3f} max {max(rates):.3f} median {np.median(rates):.3f}")

raw = (H / "trajectory.bin").read_bytes()
hdr_end = raw.find(b"<End settings>\n") + len(b"<End settings>\n")
body = raw[hdr_end:]
rec = np.dtype([("time", "<u4"), ("x", "<u2"), ("y", "<u2"), ("x2", "<u2"), ("y2", "<u2")])
pos = np.frombuffer(body[: (len(body) // rec.itemsize) * rec.itemsize], dtype=rec)
print(f"\nposition samples: {pos.size}  time {pos['time'].min()}..{pos['time'].max()} "
      f"x {pos['x'].min()}..{pos['x'].max()} y {pos['y'].min()}..{pos['y'].max()}")
