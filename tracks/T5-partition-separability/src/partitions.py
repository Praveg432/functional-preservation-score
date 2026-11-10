"""T5 candidate Base-OS / payload partitions on the real C. elegans connectome.

The blueprint asserts a clean split: a regenerable "Base-OS" (autonomic/sensory/motor) vs. a
transferable "identity payload" (integrative core). On the worm this maps to:
  * role-based : Base-OS = sensory + motor neurons (native I/O); payload = interneurons.
We also provide graph-based candidates so the separability result is not tied to one labeling:
  * periphery  : Base-OS = low-degree boundary nodes; payload = high-degree core (k-core).
  * random     : the null (random assignment of the same payload size).

A partition is a boolean mask `is_payload` over the N neurons. load_celegans already carries a
role-based `part` (0=base-OS, 1=payload); we rebuild candidates here explicitly for clarity +
to generate graph-based and random alternatives.
"""

from __future__ import annotations

import numpy as np

from shared.connectome import Connectome, SENSORY, INTER, MOTOR


def role_based(c: Connectome) -> np.ndarray:
    """Base-OS = sensory+motor, payload = interneurons (the blueprint's split)."""
    return (c.roles == INTER)


def kcore_based(c: Connectome, payload_frac: float | None = None) -> np.ndarray:
    """Payload = highest-degree core; Base-OS = low-degree periphery.

    If payload_frac is None, match the role-based payload size for a fair comparison.
    """
    deg = (c.W != 0).sum(axis=0) + (c.W != 0).sum(axis=1)
    if payload_frac is None:
        k = int(role_based(c).sum())
    else:
        k = int(round(payload_frac * c.n))
    order = np.argsort(deg)[::-1]
    mask = np.zeros(c.n, dtype=bool)
    mask[order[:k]] = True
    return mask


def random_partition(c: Connectome, payload_size: int, seed: int) -> np.ndarray:
    """Null: a random payload of the given size (same size as the tested partition)."""
    rng = np.random.default_rng(seed)
    mask = np.zeros(c.n, dtype=bool)
    mask[rng.choice(c.n, size=payload_size, replace=False)] = True
    return mask


def candidates(c: Connectome) -> dict[str, np.ndarray]:
    return {"role_based": role_based(c), "kcore_based": kcore_based(c)}
