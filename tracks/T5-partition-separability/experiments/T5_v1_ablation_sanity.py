"""T5-V1 : readout + ablation sanity gate.

Confirms the functional readout actually RESPONDS to ablation (lesions change function). If a
readout is insensitive to lesions, it cannot test separability -> fix before V2.

Pass: ablating a nontrivial neuron set measurably drops FPS below the intact reference (~1.0),
and a larger lesion drops it more (dose-response). Writes results/T5_v1.json. Needs .venv.
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

from shared.connectome import load_celegans  # noqa: E402
import ablate  # noqa: E402

RESULTS = Path(__file__).resolve().parents[1] / "results"
REAL_NPZ = _ROOT / "data" / "celegans_real.npz"


def run():
    c = load_celegans(path=REAL_NPZ)
    model, bat = ablate.make_battery(c)

    fps_intact = bat.score(model.run).fps  # sanity: should be ~1.0
    rng = np.random.default_rng(0)

    # dose-response: ablate increasing random fractions
    dose = []
    for frac in [0.0, 0.1, 0.2, 0.4, 0.6]:
        k = int(round(frac * c.n))
        kill = np.zeros(c.n, dtype=bool)
        if k:
            kill[rng.choice(c.n, size=k, replace=False)] = True
        f = ablate.fps_after_lesion(c, model, bat, kill)
        dose.append({"ablate_frac": frac, "fps": f})

    fps_vals = [d["fps"] for d in dose]
    # pass: intact ~1, monotone-ish decrease, and big lesion clearly below intact
    responsive = (fps_intact > 0.99) and (fps_vals[-1] < fps_intact - 0.2) and \
                 (fps_vals[-1] <= fps_vals[1] + 0.05)

    out = {
        "gate": "T5-V1 readout+ablation sanity",
        "substrate": "real-celegans",
        "fps_intact": fps_intact,
        "dose_response": dose,
        "criterion": "intact~1.0 AND large lesion drops FPS >0.2 AND dose-responsive",
        "passed": bool(responsive),
    }
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "T5_v1.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    run()
