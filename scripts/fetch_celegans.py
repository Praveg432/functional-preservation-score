"""Fetch the real C. elegans somatic connectome (White 1986, via OpenWorm ConnectomeToolbox)
and cache it as data/celegans_real.npz in the Connectome contract.

Sources (public, OpenWorm ConnectomeToolbox mirror of the primary data):
  * aconnectome_white_1986_whole.csv -- tab-separated: pre, post, type, synapses
  * all_cell_info.csv                -- Cell name, Type, ... (role classification)

Role mapping (roles: 0=sensory, 1=inter, 2=motor), from the `Type`/`Classification` columns:
  * sensory : contains any of {sensory, mechanosensory, amphid, touch, nocicept, chemosens,
              thermosens, photo, polymodal, oxygen, phasmid}
  * motor   : contains {motor}
  * inter   : contains {interneuron, inter} (default for ring/command/relay neurons)
  * fallback: any unmatched neuron -> inter (and flagged in the printed summary)

Ground-truth partition (part: 0=base-OS, 1=payload): base-OS = sensory + motor neurons
(the "native" I/O layer); payload = interneurons (the integrative core). This mirrors the
blueprint's Base-OS / identity-payload split applied honestly to real roles.

Run:
    python3 scripts/fetch_celegans.py
Requires network access the first time; thereafter the .npz is reused by the loader.
"""

from __future__ import annotations

import io
import sys
import urllib.request
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
BASE = "https://raw.githubusercontent.com/openworm/ConnectomeToolbox/main/cect/data"
CONN_URL = f"{BASE}/aconnectome_white_1986_whole.csv"
INFO_URL = f"{BASE}/all_cell_info.csv"

SENSORY_KEYS = ("sensory", "mechanosens", "amphid", "touch", "nocicept", "chemosens",
                "thermosens", "photo", "polymodal", "oxygen", "phasmid", "deirid")
MOTOR_KEYS = ("motor",)
INTER_KEYS = ("interneuron", "inter")

SENSORY, INTER, MOTOR = 0, 1, 2
BASE_OS, PAYLOAD = 0, 1
GAP_WEIGHT = 0.5  # gap junctions added symmetrically at half weight (standard convention)


def _get(url: str) -> str:
    with urllib.request.urlopen(url, timeout=60) as r:
        return r.read().decode("utf-8", errors="replace")


def _classify(type_str: str, classification: str) -> int:
    s = f"{type_str} {classification}".lower()
    if any(k in s for k in MOTOR_KEYS):
        # motor wins only if not also clearly sensory-labeled first token
        if any(k in s for k in SENSORY_KEYS):
            return SENSORY
        return MOTOR
    if any(k in s for k in SENSORY_KEYS):
        return SENSORY
    if any(k in s for k in INTER_KEYS):
        return INTER
    return INTER  # fallback


def build() -> dict:
    info_txt = _get(INFO_URL)
    conn_txt = _get(CONN_URL)

    # --- parse roles ---
    role_by_cell: dict[str, int] = {}
    reader = io.StringIO(info_txt)
    header = reader.readline().rstrip("\n").split(",")
    # columns: Cell name, Type, Name details, Lineage, Classification
    for line in reader:
        # naive CSV: classification field may contain commas inside quotes; split carefully
        parts = _split_csv(line.rstrip("\n"))
        if len(parts) < 2:
            continue
        cell = parts[0].strip()
        typ = parts[1].strip() if len(parts) > 1 else ""
        clsf = parts[4].strip() if len(parts) > 4 else ""
        if cell:
            role_by_cell[cell] = _classify(typ, clsf)

    # --- parse edges (only between classified neurons; drop muscles/organs) ---
    edges = []
    for line in conn_txt.splitlines()[1:]:
        if not line.strip():
            continue
        f = line.split("\t")
        if len(f) < 4:
            f = line.split(",")
        if len(f) < 4:
            continue
        pre, post, etype, syn = f[0].strip(), f[1].strip(), f[2].strip().lower(), f[3].strip()
        if pre not in role_by_cell or post not in role_by_cell:
            continue  # skip non-neuronal targets (muscles, organs)
        try:
            w = float(syn)
        except ValueError:
            continue
        edges.append((pre, post, etype, w))

    cells = sorted(role_by_cell.keys())
    # keep only neurons that participate in at least one neuron-neuron edge
    active = set()
    for pre, post, _, _ in edges:
        active.add(pre)
        active.add(post)
    cells = [c for c in cells if c in active]
    idx = {c: i for i, c in enumerate(cells)}
    n = len(cells)

    W = np.zeros((n, n), dtype=np.float64)
    for pre, post, etype, w in edges:
        i, j = idx[pre], idx[post]
        if etype.startswith("chem"):
            W[i, j] += w
        else:  # electrical / gap junction -> symmetric, half weight
            W[i, j] += GAP_WEIGHT * w
            W[j, i] += GAP_WEIGHT * w

    roles = np.array([role_by_cell[c] for c in cells], dtype=int)
    part = np.where(roles == INTER, PAYLOAD, BASE_OS).astype(int)
    names = cells

    return {"W": W, "roles": roles, "part": part, "names": np.array(names, dtype=object),
            "n": n, "n_edges": int((W != 0).sum()),
            "n_sensory": int((roles == SENSORY).sum()),
            "n_inter": int((roles == INTER).sum()),
            "n_motor": int((roles == MOTOR).sum())}


def _split_csv(line: str) -> list[str]:
    """Minimal CSV split honoring double-quoted fields with internal commas."""
    out, cur, inq = [], [], False
    for ch in line:
        if ch == '"':
            inq = not inq
        elif ch == "," and not inq:
            out.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    out.append("".join(cur))
    return out


def main():
    DATA.mkdir(exist_ok=True)
    d = build()
    np.savez(DATA / "celegans_real.npz",
             W=d["W"], roles=d["roles"], part=d["part"], names=d["names"])
    print(f"saved {DATA/'celegans_real.npz'}")
    print(f"  neurons kept   : {d['n']}")
    print(f"  edges          : {d['n_edges']}")
    print(f"  sensory/inter/motor: {d['n_sensory']}/{d['n_inter']}/{d['n_motor']}")


if __name__ == "__main__":
    sys.exit(main())
