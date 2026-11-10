"""Stream the STRUCTURE of a remote DANDI NWB (no full download) to locate spikes + position.

Uses remfile + h5py to read only the HDF5 metadata/datasets we need from the 5 GB NWB over
HTTP. We do NOT pull the raw ephys; only spike_times and position SpatialSeries.
"""
import sys
import h5py
import remfile

ASSET = "a13eb5ce-89c8-4c21-a5a2-34e00a59ac0f"
URL = f"https://api.dandiarchive.org/api/assets/{ASSET}/download/"


def walk(g, depth=0, max_depth=3, prefix=""):
    if depth > max_depth:
        return
    for k in g.keys():
        item = g[k]
        path = f"{prefix}/{k}"
        if isinstance(item, h5py.Group):
            print("  " * depth + f"[grp] {path}")
            walk(item, depth + 1, max_depth, path)
        else:
            print("  " * depth + f"[dat] {path}  shape={item.shape} dtype={item.dtype}")


f = remfile.File(URL)
h = h5py.File(f, "r")
print("== top ==", list(h.keys()))
print("\n== /units ==")
if "units" in h:
    walk(h["units"], max_depth=1, prefix="/units")
print("\n== /processing (behavior/position) ==")
if "processing" in h:
    walk(h["processing"], max_depth=4, prefix="/processing")
print("\n== /intervals (epochs/laps) ==")
if "intervals" in h:
    walk(h["intervals"], max_depth=2, prefix="/intervals")
h.close()
