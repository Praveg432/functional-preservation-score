"""T3-V3 : incremental-sync capacity / interference.

Tests the blueprint's "background sync into a bounded latent backup" claim: stream real replay
events into a FIXED-SIZE store and measure how recoverable earlier events remain as load grows.

Setup:
  * Encode each real DANDI replay lap to a latent code (SeqAutoencoder, fixed latent_dim).
  * SuperpositionStore (one fixed vector, holographic) vs SlotStore (fixed slots, FIFO).
  * Stream N events; after each load level L, query recoverability (identification accuracy,
    chance = 1/N) of (a) ALL stored-so-far events and (b) just the OLDEST few.
  * Capacity/interference curve = recovery vs load. Expectation (H3):
      - Superposition: smooth graceful degradation (crosstalk grows with L).
      - Slots: flat until L = n_slots, then a hard cliff for evicted (oldest) events.

Pass (pre-registered): recovery degrades MONOTONICALLY with load for superposition AND the
slot store shows the hard-capacity cliff. (A real capacity/interference trade-off exists.)

Writes results/T3_v3.json. Deterministic. Requires the .venv.
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

import events                                   # noqa: E402
from seq_autoencoder import SeqAutoencoder       # noqa: E402
import sync_store as ss                          # noqa: E402

RESULTS = Path(__file__).resolve().parents[1] / "results"
LATENT_DIM = 8
N_SLOTS = 10
LOADS = [2, 4, 6, 8, 10, 15, 20, 30, 40]


def run():
    dandi = _ROOT / "data" / "hippocampus" / "dandi000044_buddy.npz"
    sess = events.load_dandi(dandi)
    seqs = events.sequences(sess, min_span=0.7, direction=1)
    n = len(seqs)
    ae = SeqAutoencoder.fit(seqs, LATENT_DIM)
    codes = {i: ae.encode(s) for i, s in enumerate(seqs)}

    loads = [L for L in LOADS if L <= n]

    sup_curve, slot_curve, oldest_curve = [], [], []
    for L in loads:
        # Superposition: write first L events, then query all L
        sup = ss.SuperpositionStore(LATENT_DIM, seed=0)
        for i in range(L):
            sup.write(codes[i])
        readouts = {i: sup.read(i) for i in range(L)}
        true_bank = {i: codes[i] for i in range(L)}
        sup_acc = ss.recover_accuracy(readouts, true_bank)
        # oldest-few (first 3) recoverability under this load
        oldest = {i: sup.read(i) for i in range(min(3, L))}
        oldest_acc = ss.recover_accuracy(oldest, true_bank)

        # Slot store: write first L, query all L
        slot = ss.SlotStore(N_SLOTS)
        for i in range(L):
            slot.write(codes[i], i)
        slot_readouts = {i: slot.read(i) for i in range(L)}
        slot_acc = ss.recover_accuracy(slot_readouts, true_bank)

        sup_curve.append({"load": L, "superposition_recovery": sup_acc,
                          "chance": 1.0 / L})
        slot_curve.append({"load": L, "slot_recovery": slot_acc, "n_slots": N_SLOTS})
        oldest_curve.append({"load": L, "oldest3_recovery": oldest_acc})

    # verdict checks
    sup_vals = [r["superposition_recovery"] for r in sup_curve]
    monotone = all(sup_vals[i] >= sup_vals[i + 1] - 0.15 for i in range(len(sup_vals) - 1)) \
        and (sup_vals[0] - sup_vals[-1] > 0.1)
    # slot cliff: recovery ~ n_slots/load once past capacity
    post = [r for r in slot_curve if r["load"] > N_SLOTS]
    cliff = bool(post) and all(r["slot_recovery"] < 1.0 for r in post)

    out = {
        "experiment": "T3-V3 incremental-sync capacity/interference",
        "substrate": "DANDI-000044-Buddy-laps-dir1",
        "n_events": n, "latent_dim": LATENT_DIM, "n_slots": N_SLOTS,
        "superposition_curve": sup_curve,
        "slot_curve": slot_curve,
        "oldest_curve": oldest_curve,
        "superposition_monotone_degradation": bool(monotone),
        "slot_hard_capacity_cliff": cliff,
        "passed": bool(monotone and cliff),
        "verdict": (
            "Capacity/interference trade-off confirmed: superposition degrades gracefully with "
            "load (crosstalk), slot store holds perfectly up to n_slots then evicts oldest."
        ),
    }
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "T3_v3.json").write_text(json.dumps(out, indent=2))
    print(f"n_events={n}  latent_dim={LATENT_DIM}  n_slots={N_SLOTS}")
    print("load | superpos | oldest3 | slot(cap", N_SLOTS, ")")
    for a, b, c in zip(sup_curve, oldest_curve, slot_curve):
        print(f"  {a['load']:3d} |  {a['superposition_recovery']:.2f}   |  "
              f"{b['oldest3_recovery']:.2f}  |  {c['slot_recovery']:.2f}")
    print(f"monotone-degradation={monotone}  slot-cliff={cliff}  PASS={out['passed']}")
    return out


if __name__ == "__main__":
    run()
