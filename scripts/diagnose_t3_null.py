"""Why is the time-shuffle null so high? Decompose decode-fidelity on DANDI laps."""
import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tracks/T3-replay-latent-compression/src"))
import events, fidelity as fid
from seq_autoencoder import SeqAutoencoder

sess = events.load_dandi()
DIRECTION = 1
seqs = events.sequences(sess, min_span=0.7, direction=DIRECTION)
print(f"direction-split laps (dir={DIRECTION}): n={len(seqs)}")
fields, _ = fid.build_place_fields(sess)
rng = np.random.default_rng(0)
idx = rng.permutation(len(seqs)); cut = int(0.7 * len(seqs))
tr = [seqs[i] for i in idx[:cut]]; te = [seqs[i] for i in idx[cut:]]
ae = SeqAutoencoder.fit(tr, 20)


def tc(a, b):
    if np.std(a) < 1e-9 or np.std(b) < 1e-9:
        return 0.0
    return float(np.corrcoef(np.argsort(np.argsort(a)), np.argsort(np.argsort(b)))[0, 1])


orig_mono, recon_vs_orig, null_vs_orig = [], [], []
for s in te:
    d_orig = fid.decode_trajectory(s, fields)
    d_recon = fid.decode_trajectory(ae.reconstruct(s, 32), fields)
    d_null = fid.decode_trajectory(ae.reconstruct(fid.time_shuffle(s, rng), 32), fields)
    orig_mono.append(tc(d_orig, np.arange(len(d_orig))))
    recon_vs_orig.append(tc(d_recon, d_orig))
    null_vs_orig.append(tc(d_null, d_orig))

print(f"orig decode monotonic (vs time): {np.mean(orig_mono):.3f}")
print(f"recon-decode vs orig-decode:     {np.mean(recon_vs_orig):.3f}")
print(f"null(recon-of-shuffled) vs orig: {np.mean(null_vs_orig):.3f}")
print(f"-> true headroom (recon - null): {np.mean(recon_vs_orig) - np.mean(null_vs_orig):+.3f}")
