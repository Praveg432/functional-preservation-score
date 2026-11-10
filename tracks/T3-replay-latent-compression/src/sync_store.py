"""T3 incremental-sync store: a fixed-size latent memory written to event-by-event.

Models the blueprint's "background sync / up-to-date backup": replay events stream in during
sleep and are compiled into a bounded latent state W_S. The question V3 tests: how many events
can a FIXED-SIZE store hold before older ones become unrecoverable (catastrophic interference)?

Two write schemes (both bounded; the contrast is the whole point):
  * SuperpositionStore -- all events summed into one fixed vector (holographic / distributed,
    like the blueprint's single latent W_S). Capacity is graceful-degradation limited: every
    new event adds crosstalk to all stored ones.
  * SlotStore          -- fixed number of slots with LRU/FIFO eviction. Hard capacity: beyond
    the slot count, the oldest event is simply gone (no crosstalk, but a hard cliff).

Recovery of event i = nearest-neighbour match of the store's readout for i against the bank of
true event latents (identification accuracy, consistent with V2).
"""

from __future__ import annotations

import numpy as np


def _unit(v):
    n = np.linalg.norm(v)
    return v / (n + 1e-9)


class SuperpositionStore:
    """Fixed-dim store: sum of (random-key-bound) event latents. One vector, unbounded writes.

    Binding: each event e_i is stored as sum += key_i * e_i (outer-product style via a random
    key matrix), and read back as store @ key_i. This is a standard distributed-memory /
    holographic scheme; crosstalk grows with the number of stored events.
    """

    def __init__(self, latent_dim: int, seed: int = 0):
        self.d = latent_dim
        self.rng = np.random.default_rng(seed)
        self.keys: list[np.ndarray] = []
        self.M = np.zeros((latent_dim, latent_dim))  # associative matrix

    def write(self, code: np.ndarray):
        key = _unit(self.rng.standard_normal(self.d))
        self.keys.append(key)
        self.M += np.outer(code, key)                # bind value to key

    def read(self, i: int) -> np.ndarray:
        return self.M @ self.keys[i]                  # unbind -> code_i + crosstalk

    @property
    def size_bits_per_dim(self):
        return self.d * self.d                        # store footprint (constant, fixed size)


class SlotStore:
    """Fixed number of slots; FIFO eviction once full (hard capacity, no crosstalk)."""

    def __init__(self, n_slots: int):
        self.n_slots = n_slots
        self.codes: list[np.ndarray] = []
        self.ids: list[int] = []

    def write(self, code: np.ndarray, event_id: int):
        self.codes.append(code)
        self.ids.append(event_id)
        if len(self.codes) > self.n_slots:
            self.codes.pop(0)
            self.ids.pop(0)

    def read(self, event_id: int):
        if event_id in self.ids:
            return self.codes[self.ids.index(event_id)]
        return None                                   # evicted -> unrecoverable


def recover_accuracy(readouts: dict[int, np.ndarray], true_codes: dict[int, np.ndarray]) -> float:
    """Fraction of queried events whose store readout nearest-matches its own true latent.

    readouts[i] = store's reconstruction for event i (or None if evicted -> counts as miss).
    Matched against the bank of ALL true codes (identification, chance = 1/n_bank).
    """
    ids = list(true_codes.keys())
    bank = np.stack([_unit(true_codes[i]) for i in ids])
    hits = 0
    total = 0
    for i, r in readouts.items():
        total += 1
        if r is None:
            continue
        sims = bank @ _unit(r)
        if ids[int(np.argmax(sims))] == i:
            hits += 1
    return hits / total if total else 0.0
