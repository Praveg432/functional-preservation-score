"""T3-V1 : data + event gate.

Check that real run-epoch population sequences carry extractable structure a trivial baseline
does not: a place-ordered sequence should have a significant diagonal (sequential) structure,
quantified as the correlation between unit place-order and the time-bin of peak firing.

Pass: mean sequence has sequence-structure score clearly above a shuffled-row null.
Writes results/T3_v1.json. Deterministic.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

import events  # noqa: E402

RESULTS = Path(__file__).resolve().parents[1] / "results"


def build_place_fields(sess, n_space=20, eps=1e-3):
    """Estimate per-unit place fields f_u(space) = mean firing rate vs linear position."""
    edges = np.linspace(0, 1, n_space + 1)
    centers = 0.5 * (edges[:-1] + edges[1:])
    # occupancy (time per space bin), from position samples
    occ, _ = np.histogram(sess.x, bins=edges)
    dt = np.median(np.diff(sess.t)) if sess.t.size > 1 else 1.0
    occ_time = occ * dt + eps
    fields = np.zeros((len(sess.spikes), n_space))
    for u, s in enumerate(sess.spikes):
        xi = np.interp(s, sess.t, sess.x, left=np.nan, right=np.nan)
        xi = xi[~np.isnan(xi)]
        h, _ = np.histogram(xi, bins=edges)
        fields[u] = h / occ_time
    return fields, centers


def decode_trajectory(seq_counts, fields, dt=1.0):
    """Bayesian 1-D position decode per time bin from population counts (Poisson model).

    seq_counts: (n_units, n_bins) spike counts; fields: (n_units, n_space) rate maps.
    Returns decoded space-bin index per time bin (argmax posterior).
    """
    n_space = fields.shape[1]
    log_post = np.zeros((seq_counts.shape[1], n_space))
    f = fields + 1e-3
    for b in range(seq_counts.shape[1]):
        n = seq_counts[:, b][:, None]                 # (n_units, 1)
        # log P(space) ~ sum_u [ n_u log f_u(space) - dt f_u(space) ]
        log_post[b] = (n * np.log(f)).sum(axis=0) - dt * f.sum(axis=0)
    return np.argmax(log_post, axis=1)


def decode_score(seq_counts, fields):
    """How monotonic/sequential is the decoded trajectory? |rank-corr(time-bin, decoded pos)|.

    A real run/replay sequence decodes to a smoothly sweeping position -> high |corr|.
    """
    if seq_counts.sum() < 5:
        return 0.0
    dec = decode_trajectory(seq_counts, fields)
    tb = np.arange(len(dec))
    if dec.std() < 1e-9:
        return 0.0
    r_t = np.argsort(np.argsort(tb))
    r_d = np.argsort(np.argsort(dec))
    return float(abs(np.corrcoef(r_t, r_d)[0, 1]))


def run():
    sess = events.load_session()
    seqs = events.sequences(sess)
    n_units = len(sess.spikes)
    fields, _ = build_place_fields(sess)

    real_scores = [decode_score(m, fields) for m in seqs]
    # column-shuffle null: destroy temporal sequence while keeping per-bin population vector
    rng = np.random.default_rng(0)
    null_scores = []
    for m in seqs:
        mm = m[:, rng.permutation(m.shape[1])]
        null_scores.append(decode_score(mm, fields))

    mean_real = float(np.mean(real_scores)) if real_scores else 0.0
    mean_null = float(np.mean(null_scores)) if null_scores else 0.0
    passed = (len(seqs) >= 5) and (mean_real > mean_null + 0.1) and (mean_real > 0.3)

    out = {
        "gate": "T3-V1 data+event (Bayesian decode score)",
        "n_units": n_units,
        "n_sequences": len(seqs),
        "seq_shape_example": list(seqs[0].shape) if seqs else None,
        "mean_decode_score_real": mean_real,
        "mean_decode_score_timeshuffled": mean_null,
        "criterion": "n_seq>=5 AND real>shuffled+0.1 AND real>0.3",
        "passed": bool(passed),
    }
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "T3_v1.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    run()
