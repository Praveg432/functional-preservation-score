"""T3 statistical hardening: repeated cross-validated identification + permutation significance.

Addresses audit A2/A4: the headline identification result rested on ONE 18/8 split with no
uncertainty and a coarse (1/8) metric. Here:
  * Repeated random splits (n_splits) of the clean laps; AE fit on TRAIN only (no leakage);
    identification top-1 measured on held-out TEST, pooled across splits for a mean + bootstrap CI.
  * Permutation null: shuffle the recon<->orig assignment; p-value that observed top-1 > chance.
  * Report a small grid of bits-per-event with CIs (not a single best-cell floor).

Writes results/T3_v2_stats.json. Needs .venv.
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

from shared import stats  # noqa: E402
import events          # noqa: E402
import fidelity as fid  # noqa: E402
from seq_autoencoder import SeqAutoencoder  # noqa: E402

RESULTS = Path(__file__).resolve().parents[1] / "results"
N_SPLITS = 30
TRAIN_FRAC = 0.7
CONFIGS = [(16, 8), (16, 2), (8, 2), (4, 2)]   # (latent_dim, bits) -> a few bits/event points
FULL_DIM, FULL_BITS = 16, 32


def identification_top1(origs, recons):
    return fid.identification_accuracy(origs, recons)["top1"]


def perm_null_top1(origs, recons, n_perm=2000, seed=0):
    """Null: randomly permute which original each recon is matched to; distribution of top-1."""
    import numpy as _np
    n = len(origs)
    O = _np.stack([o.ravel() for o in origs]); R = _np.stack([r.ravel() for r in recons])
    On = O / (_np.linalg.norm(O, axis=1, keepdims=True) + 1e-9)
    Rn = R / (_np.linalg.norm(R, axis=1, keepdims=True) + 1e-9)
    sim = Rn @ On.T
    pred = _np.argmax(sim, axis=1)
    rng = _np.random.default_rng(seed)
    null = []
    for _ in range(n_perm):
        truth = rng.permutation(n)      # random "true" labels => chance identification
        null.append(_np.mean(pred == truth))
    return _np.array(null)


def run():
    dandi = _ROOT / "data" / "hippocampus" / "dandi000044_buddy.npz"
    sess = events.load_dandi(dandi)
    seqs = events.sequences(sess, min_span=0.7, direction=1)
    n = len(seqs)

    # repeated-split uncompressed headroom
    head_vals = []
    head_null_means = []
    for s in range(N_SPLITS):
        rng = np.random.default_rng(s)
        idx = rng.permutation(n); cut = int(TRAIN_FRAC * n)
        tr = [seqs[i] for i in idx[:cut]]; te = [seqs[i] for i in idx[cut:]]
        if len(te) < 3:
            continue
        ae = SeqAutoencoder.fit(tr, FULL_DIM)          # TRAIN-only fit (no leakage)
        recons = [ae.reconstruct(x, FULL_BITS) for x in te]
        head_vals.append(identification_top1(te, recons))
        head_null_means.append(perm_null_top1(te, recons, n_perm=500, seed=s).mean())

    head_mean, head_lo, head_hi, head_n = stats.bootstrap_ci(head_vals, seed=1)
    # significance: observed per-split top1 vs per-split permutation-null means
    _, p_head = stats.permutation_test_greater(head_vals, head_null_means, n_perm=10000, seed=2)
    chance = float(np.mean([1.0 / max(1, len(seqs) - int(TRAIN_FRAC * n))] * 1))

    # per-config frontier with CIs
    frontier = []
    for (dim, bits) in CONFIGS:
        vals = []
        for s in range(N_SPLITS):
            rng = np.random.default_rng(s)
            idx = rng.permutation(n); cut = int(TRAIN_FRAC * n)
            tr = [seqs[i] for i in idx[:cut]]; te = [seqs[i] for i in idx[cut:]]
            if len(te) < 3:
                continue
            ae = SeqAutoencoder.fit(tr, dim)
            recons = [ae.reconstruct(x, bits) for x in te]
            vals.append(identification_top1(te, recons))
        m, lo, hi, nn = stats.bootstrap_ci(vals, seed=3)
        frontier.append({"latent_dim": dim, "bits": bits, "bits_per_event": dim * bits,
                         "top1_mean": m, "ci95": [lo, hi], "n_splits": nn})

    out = {
        "experiment": "T3 statistical hardening (repeated CV + permutation)",
        "substrate": "DANDI-000044-Buddy-laps-dir1",
        "n_laps": n, "n_splits": N_SPLITS, "train_frac": TRAIN_FRAC,
        "uncompressed_headroom": {
            "top1_mean": head_mean, "ci95": [head_lo, head_hi], "n_splits": head_n,
            "mean_chance": float(np.mean(head_null_means)),
            "p_value_vs_permutation_null": p_head,
        },
        "frontier_with_ci": frontier,
    }
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "T3_v2_stats.json").write_text(json.dumps(out, indent=2))
    print(f"uncompressed top1 = {head_mean:.3f}  95% CI [{head_lo:.3f}, {head_hi:.3f}]  "
          f"(n={head_n} splits)  vs chance ~{np.mean(head_null_means):.3f}  p={p_head:.4f}")
    for r in frontier:
        print(f"  dim{r['latent_dim']:2d} b{r['bits']} bpe{r['bits_per_event']:3d}: "
              f"top1 {r['top1_mean']:.3f} CI[{r['ci95'][0]:.3f},{r['ci95'][1]:.3f}]")
    return out


if __name__ == "__main__":
    run()
