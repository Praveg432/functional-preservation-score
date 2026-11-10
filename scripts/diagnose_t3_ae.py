"""Diagnose T3-V2 no-headroom: is it the AE reconstruction or the fidelity metric?"""
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tracks/T3-replay-latent-compression/src"))
import events, fidelity as fid
from seq_autoencoder import SeqAutoencoder

sess = events.load_session()
seqs = events.sequences(sess)
fields, _ = fid.build_place_fields(sess)

# 1) how well do ORIGINALS decode (self-score)? and raw reconstruction error of the AE?
ae = SeqAutoencoder.fit(seqs, 20)
raw_err = []
for s in seqs:
    r = ae.reconstruct(s, 32)
    denom = np.sum(s**2) + 1e-9
    raw_err.append(np.sum((s - r)**2) / denom)
print(f"AE raw reconstruction rel-MSE (fp32, dim20): mean {np.mean(raw_err):.4f}  (0=perfect)")

# 2) decoded-trajectory agreement orig-vs-recon, and self-consistency orig-vs-orig(=1)
fids = [fid.decode_fidelity(s, ae.reconstruct(s, 32), fields) for s in seqs]
print(f"decode_fidelity(orig, recon): mean {np.mean(fids):.3f}")

# 3) KEY: do originals even decode to a monotonic trajectory? (V1 said 0.34)
self_scores = [fid.decode_score(s, fields) for s in seqs]
print(f"decode_score(orig) [V1 instrument]: mean {np.mean(self_scores):.3f}")

# 4) is the metric the problem? compare decoded trajectories directly for a few
for s in seqs[:3]:
    d0 = fid.decode_trajectory(s, fields)
    d1 = fid.decode_trajectory(ae.reconstruct(s, 32), fields)
    print("  orig decode:", d0[:12], "\n  recon decode:", d1[:12])
