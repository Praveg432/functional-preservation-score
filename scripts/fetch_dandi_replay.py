"""Extract ONLY spike times + linearized position from a remote DANDI NWB (Grosmark/Buzsaki
dandiset 000044, hc-11) via streaming, and cache as a compact .npz for T3.

We stream with remfile+h5py and read only the small datasets we need (spike_times,
spike_times_index, cell_type, linearized_position) -- NOT the 5 GB raw ephys/LFP. The cached
.npz is a few MB and plugs into src/events.py via load_session(path=...).

Run (needs network + .venv with remfile/h5py):
    .venv/bin/python scripts/fetch_dandi_replay.py
"""
from __future__ import annotations

from pathlib import Path
import numpy as np
import h5py
import remfile

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "hippocampus"
# Buddy session (smallest, 5.4 GB remote; we read only ~MB of it)
ASSET = "a13eb5ce-89c8-4c21-a5a2-34e00a59ac0f"
URL = f"https://api.dandiarchive.org/api/assets/{ASSET}/download/"
OUT = DATA / "dandi000044_buddy.npz"


def main():
    DATA.mkdir(parents=True, exist_ok=True)
    f = remfile.File(URL)
    h = h5py.File(f, "r")

    # --- spikes: ragged array split by spike_times_index ---
    st = h["units/spike_times"][:]                     # (total_spikes,)
    idx = h["units/spike_times_index"][:]              # (n_units,) end offsets
    cell_type = [x.decode() if isinstance(x, bytes) else str(x)
                 for x in h["units/cell_type"][:]]
    spikes = []
    start = 0
    for end in idx:
        spikes.append(st[start:end].astype(np.float64))
        start = int(end)

    # --- linearized position ---
    lp = h["processing/behavior/position/linearized_position"]
    pos = lp["data"][:].astype(np.float64)
    pstart = float(lp["starting_time"][()])
    # position sampling rate: linearized_position usually ~39 Hz; derive from rate attr if present
    rate_attr = lp["starting_time"].attrs.get("rate", None)
    if rate_attr is None and "rate" in lp:
        rate_attr = float(lp["rate"][()])
    fs = float(rate_attr) if rate_attr else 39.06
    tpos = pstart + np.arange(pos.size) / fs

    h.close()

    # keep only pyramidal units if labeled (replay sequences are pyramidal place cells)
    pyr = [i for i, c in enumerate(cell_type) if "pyr" in c.lower()] or list(range(len(spikes)))
    spikes = [spikes[i] for i in pyr]

    np.savez(OUT,
             spike_times=np.array(spikes, dtype=object),
             pos=pos, tpos=tpos,
             cell_type=np.array([cell_type[i] for i in pyr], dtype=object))
    allt = np.concatenate([s for s in spikes if s.size])
    print(f"saved {OUT}")
    print(f"  units kept (pyramidal): {len(spikes)}")
    print(f"  spikes: {allt.size}  time {allt.min():.1f}..{allt.max():.1f}")
    print(f"  position samples: {pos.size}  fs~{fs:.2f} Hz  "
          f"range {np.nanmin(pos):.1f}..{np.nanmax(pos):.1f}")


if __name__ == "__main__":
    main()
