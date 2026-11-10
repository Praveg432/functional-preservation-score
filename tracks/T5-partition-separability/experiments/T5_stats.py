"""T5 statistical hardening: permutation p-value for the separability-privilege test.

Addresses audit A5: T5-V2 reported a z-score vs a 40-sample null but no p-value. Here we compute
the one-sided permutation p-value (is the asserted payload's ablation-drop GREATER than the
random-interneuron-subset null?) with a large null, for both hub definitions, across payload
fractions. The verdict (H2 corrective) stands iff the p-value is NOT significant (the payload is
no more privileged than random).

Writes results/T5_v2_stats.json. Needs .venv.
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

from shared import stats          # noqa: E402
from shared.connectome import load_celegans, INTER  # noqa: E402
import ablate                      # noqa: E402
import separability as sep         # noqa: E402

RESULTS = Path(__file__).resolve().parents[1] / "results"
REAL_NPZ = _ROOT / "data" / "celegans_real.npz"
N_NULL = 500           # large null for a stable p-value
FRACS = [0.1, 0.2, 0.3, 0.4]


def run():
    c = load_celegans(path=REAL_NPZ)
    model, bat = ablate.make_battery(c)
    inter_mask = (c.roles == INTER)
    inter_idx = np.where(inter_mask)[0]
    instr = c.W.sum(axis=0) + c.W.sum(axis=1)

    rows = []
    for frac in FRACS:
        k = max(1, int(round(frac * len(inter_idx))))
        payload = np.zeros(c.n, dtype=bool)
        payload[inter_idx[np.argsort(instr[inter_idx])[::-1][:k]]] = True
        drop = sep.transformation_drop(c, model, bat, payload)

        # explicit null distribution of random equal-size interneuron subsets
        rng = np.random.default_rng(0)
        null = []
        for _ in range(N_NULL):
            sub = np.zeros(c.n, dtype=bool)
            sub[rng.choice(inter_idx, size=min(k, len(inter_idx)), replace=False)] = True
            null.append(sep.transformation_drop(c, model, bat, sub))
        null = np.array(null)
        p = stats.permutation_p_vs_null(drop, null, greater=True)
        rows.append({
            "payload_frac": frac, "payload_size": k,
            "payload_drop": drop,
            "null_mean": float(null.mean()), "null_std": float(null.std()),
            "z": float((drop - null.mean()) / (null.std() + 1e-9)),
            "p_value_one_sided": p,
            "significant_at_0.05": bool(p < 0.05),
        })

    any_sig = any(r["significant_at_0.05"] for r in rows)
    out = {
        "experiment": "T5 statistical hardening (permutation p-value)",
        "substrate": "real-celegans", "n_null": N_NULL,
        "per_frac": rows,
        "verdict": ("At least one payload fraction is significantly privileged (revisit H2)"
                    if any_sig else
                    "H2 CONFIRMED with significance: asserted payload NOT significantly more "
                    "privileged than random interneurons at any tested fraction (all p>=0.05)"),
        "h2_holds": bool(not any_sig),
    }
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "T5_v2_stats.json").write_text(json.dumps(out, indent=2))
    for r in rows:
        print(f"frac {r['payload_frac']}: drop {r['payload_drop']:.3f} vs null "
              f"{r['null_mean']:.3f}+/-{r['null_std']:.3f}  z={r['z']:+.2f}  p={r['p_value_one_sided']:.3f}"
              f"  {'SIG' if r['significant_at_0.05'] else 'ns'}")
    print("VERDICT:", out["verdict"])
    return out


if __name__ == "__main__":
    run()
