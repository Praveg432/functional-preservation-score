"""T5-V2 : separability-vs-null gate (load-bearing) — corrected (fixed I/O interface).

V1 diagnosis: ablating Base-OS (=sensory+motor) trivially zeroes FPS (deletes I/O). Corrected
framing (src/separability.py): Base-OS = fixed I/O interface, never ablated. Test whether the
asserted "identity payload" (a privileged interneuron subset) carries the input->output
TRANSFORMATION more than a random interneuron subset of equal size.

Asserted-payload candidates (sub-partitions of the interneuron core):
  * hub_core     : highest in+out-strength interneurons (the blueprint's "integrative core").
  * recurrent    : interneurons with the most interneuron<->interneuron recurrence.
Null: random interneuron subsets of equal size.

Outcome:
  * z>2, high percentile  -> H1: the asserted payload is a privileged/separable carrier.
  * z~=0                  -> H2 (corrective): no more special than a random interneuron set.
Writes results/T5_v2.json. Needs .venv.
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

from shared.connectome import load_celegans, INTER  # noqa: E402
import ablate       # noqa: E402
import separability as sep  # noqa: E402

RESULTS = Path(__file__).resolve().parents[1] / "results"
REAL_NPZ = _ROOT / "data" / "celegans_real.npz"
N_NULL = 40
PAYLOAD_FRAC = 0.4   # top fraction of interneurons forming the asserted payload


def run():
    c = load_celegans(path=REAL_NPZ)
    model, bat = ablate.make_battery(c)
    inter_mask = (c.roles == INTER)
    inter_idx = np.where(inter_mask)[0]
    k = max(1, int(round(PAYLOAD_FRAC * len(inter_idx))))

    # candidate asserted payloads (sub-partitions of interneurons)
    instr = c.W.sum(axis=0) + c.W.sum(axis=1)                 # total strength
    hub_core = np.zeros(c.n, dtype=bool)
    hub_core[inter_idx[np.argsort(instr[inter_idx])[::-1][:k]]] = True

    Wii = c.W[np.ix_(inter_idx, inter_idx)]
    recur = (Wii != 0).sum(axis=0) + (Wii != 0).sum(axis=1)   # interneuron recurrence degree
    recurrent = np.zeros(c.n, dtype=bool)
    recurrent[inter_idx[np.argsort(recur)[::-1][:k]]] = True

    cands = {"hub_core": hub_core, "recurrent": recurrent}
    results = {}
    for name, mask in cands.items():
        r = sep.payload_privilege(c, model, bat, mask, inter_mask, n_null=N_NULL, seed=0)
        results[name] = r

    # verdict from the strongest candidate
    best = max(results.values(), key=lambda r: r["z_vs_null"])
    if best["z_vs_null"] > 2:
        hyp = "H1: an asserted payload carries the I/O transformation more than random interneurons"
    elif abs(best["z_vs_null"]) <= 2:
        hyp = ("H2 (corrective): the asserted 'identity payload' is NO MORE privileged than a "
               "random interneuron subset — no special separable module")
    else:
        hyp = "asserted payload carries LESS than random (corrective)"

    out = {
        "experiment": "T5-V2 separability vs null (fixed I/O interface, corrected)",
        "substrate": "real-celegans",
        "n_null": N_NULL, "payload_frac_of_interneurons": PAYLOAD_FRAC,
        "n_interneurons": int(inter_mask.sum()), "payload_size": k,
        "partitions": results,
        "verdict": hyp,
        "passed": True,
    }
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "T5_v2.json").write_text(json.dumps(out, indent=2))
    for name, r in results.items():
        print(f"{name}: drop={r['payload_ablation_drop']:.3f}  "
              f"null={r['null_mean_drop']:.3f}±{r['null_std_drop']:.3f}  "
              f"z={r['z_vs_null']:+.2f}  beats {r['percentile_vs_null']*100:.0f}% of nulls")
    print("VERDICT:", hyp)
    return out


if __name__ == "__main__":
    run()
