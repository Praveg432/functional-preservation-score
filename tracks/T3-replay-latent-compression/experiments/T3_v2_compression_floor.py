"""T3-V2 : compression-floor gate (load-bearing) — identification-accuracy instrument.

History (honest): earlier passes used a trajectory-rank decode-fidelity vs a time-shuffle null.
Repeated diagnosis showed the null was structurally high because every AE reconstruction looks
like a generic place-field sweep, so that metric could not cleanly discriminate (headroom stuck
~+0.09 regardless of data/direction). Fixed the METRIC once, properly: **event identification
accuracy** — is recon_i nearer to its own original than to any other event? This is bounded,
has an exact chance level (1/n), and is immune to the sweep-shape leak.

Protocol:
  STEP 0 (headroom): uncompressed AE identification top-1 must clearly beat chance (1/n).
  STEP 1 (frontier): sweep latent_dim x bits -> bits_per_event; top-1 vs bits. Floor = fewest
         bits/event still well above chance.

Data: DANDI 000044 Buddy, direction-split clean laps (if cached), else nelpy windows.
Writes results/T3_v2.json. Deterministic. Requires the .venv.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

_ROOT = Path(__file__).resolve().parents[3]
_SRC = Path(__file__).resolve().parents[1] / "src"
for p in (_ROOT, _SRC):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import events          # noqa: E402
import fidelity as fid  # noqa: E402
from seq_autoencoder import SeqAutoencoder  # noqa: E402

RESULTS = Path(__file__).resolve().parents[1] / "results"

LATENT_DIMS = [2, 4, 8, 16]
BITS = [1, 2, 3, 4, 6, 8]
FULL_DIM = 20
DIRECTION = 1


def split(seqs, frac=0.7, seed=0):
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(seqs))
    cut = int(frac * len(seqs))
    return [seqs[i] for i in idx[:cut]], [seqs[i] for i in idx[cut:]]


def id_top1(ae, test, bits):
    recons = [ae.reconstruct(s, bits) for s in test]
    return fid.identification_accuracy(test, recons)


def run():
    dandi = _ROOT / "data" / "hippocampus" / "dandi000044_buddy.npz"
    if dandi.exists():
        sess = events.load_dandi(dandi)
        seqs = events.sequences(sess, min_span=0.7, direction=DIRECTION)
        substrate = f"DANDI-000044-Buddy-laps-dir{DIRECTION}"
    else:
        sess = events.load_session()
        seqs = events.windowed_sequences(sess)
        substrate = "nelpy-linear-track-windows"
    tr, te = split(seqs)

    # STEP 0 -- headroom via identification accuracy (uncompressed)
    ae_full = SeqAutoencoder.fit(tr, FULL_DIM)
    h = id_top1(ae_full, te, 32)
    headroom_ok = (h["n"] >= 5) and (h["top1"] >= 3 * h["chance"]) and (h["top1"] >= 0.3)

    out = {
        "experiment": "T3-V2 compression-floor (identification accuracy)",
        "substrate": substrate,
        "n_train": len(tr), "n_test": len(te),
        "headroom": {"uncompressed_top1": h["top1"], "chance": h["chance"],
                     "ratio_vs_chance": h["top1"] / h["chance"] if h["chance"] else 0,
                     "passed": bool(headroom_ok)},
    }

    if not headroom_ok:
        out["frontier"] = None
        out["passed"] = False
        out["verdict"] = "NO HEADROOM: uncompressed AE cannot identify events above chance."
        RESULTS.mkdir(exist_ok=True)
        (RESULTS / "T3_v2.json").write_text(json.dumps(out, indent=2))
        print(json.dumps(out["headroom"], indent=2))
        return out

    # STEP 1 -- frontier
    frontier = []
    for d in LATENT_DIMS:
        ae = SeqAutoencoder.fit(tr, d)
        for b in BITS:
            r = id_top1(ae, te, b)
            frontier.append({"latent_dim": d, "bits": b,
                             "bits_per_event": ae.bits_per_event(b),
                             "top1": r["top1"], "chance": r["chance"]})

    chance = frontier[0]["chance"]
    good_thresh = max(0.3, 2 * chance)   # "preserved" = top-1 >= 2x chance (and >= 0.3)
    above = [r for r in frontier if r["top1"] >= good_thresh]
    floor_bpe = min((r["bits_per_event"] for r in above), default=None)
    raw_bits = seqs[0].size * 32

    out["frontier"] = sorted(frontier, key=lambda r: r["bits_per_event"])
    out["floor_bits_per_event"] = floor_bpe
    out["good_threshold_top1"] = good_thresh
    out["uncompressed_raw_bits"] = int(raw_bits)
    out["compression_ratio_at_floor"] = (raw_bits / floor_bpe) if floor_bpe else None
    out["passed"] = bool(floor_bpe is not None)
    out["verdict"] = (
        f"Floor ~{floor_bpe} bits/event (~{raw_bits/floor_bpe:.0f}x vs raw {raw_bits} bits) "
        f"holding identification top-1 >= {good_thresh:.2f} (chance {chance:.2f})."
        if floor_bpe else "No bit budget stays above threshold; degradation profile only."
    )

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "T3_v2.json").write_text(json.dumps(out, indent=2))
    print(f"headroom top1 {h['top1']:.3f} vs chance {h['chance']:.3f} "
          f"({h['top1']/h['chance']:.1f}x) -> {'OK' if headroom_ok else 'FAIL'}")
    print(f"floor: {floor_bpe} bits/event   ratio {out['compression_ratio_at_floor']}")
    for r in out["frontier"]:
        print(f"  dim {r['latent_dim']:2d} b{r['bits']} bpe {r['bits_per_event']:3d}  top1 {r['top1']:.2f}")
    return out


if __name__ == "__main__":
    run()
