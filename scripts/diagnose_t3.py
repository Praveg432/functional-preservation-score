"""Diagnose why T3-V1 sequences lack structure: position signal + per-epoch activity + ordering."""
from pathlib import Path
import sys
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tracks/T3-replay-latent-compression/src"))
import events

sess = events.load_session()
print(f"units: {len(sess.spikes)}  pos samples: {sess.t.size}")
print(f"pos t: {sess.t.min():.1f}..{sess.t.max():.1f}  spike t: "
      f"{min(s.min() for s in sess.spikes):.1f}..{max(s.max() for s in sess.spikes):.1f}")
print(f"x normalized range: {sess.x.min():.3f}..{sess.x.max():.3f}  std {sess.x.std():.3f}")

# Is position actually aligned to spikes in time? check overlap
allt = np.concatenate(sess.spikes)
overlap = ((sess.t >= allt.min()) & (sess.t <= allt.max())).mean()
print(f"fraction of position samples within spike window: {overlap:.3f}")

eps = events.run_epochs(sess)
print(f"\nrun epochs: {len(eps)}")
if eps:
    durs = [b - a for a, b in eps]
    print(f"epoch dur s: min {min(durs):.2f} max {max(durs):.2f} median {np.median(durs):.2f}")

seqs = events.sequences(sess)
act = [int((m.sum(axis=1) > 0).sum()) for m in seqs]
print(f"sequences: {len(seqs)}  active units/seq: min {min(act)} max {max(act)} median {int(np.median(act))}")

# how many units have a well-defined place field (spatial info)?
order = events._place_order(sess)
# check whether position actually varies during epochs (real traversals) vs noise
if eps:
    a, b = eps[len(eps)//2]
    m = (sess.t >= a) & (sess.t <= b)
    print(f"\nmid-epoch position span: {sess.x[m].min():.3f}..{sess.x[m].max():.3f} (want near 0..1 for a full traversal)")
