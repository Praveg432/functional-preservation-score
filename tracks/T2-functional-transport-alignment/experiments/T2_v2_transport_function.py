"""T2-V2 (+V3): transport-preserves-function gate + divergence boundary.

V2 (load-bearing): with the ORACLE (ground-truth) correspondence, does transporting A's weights
onto B reproduce A's input->output function? Oracle isolates TRANSPORT failure from ALIGNMENT
failure. Also run with the GW-estimated correspondence to show the alignment-quality cost.

V3: sweep A<->B structural divergence (rewire fraction) and chart transport fidelity -> locate
the boundary. Also the feasibility-mask ceiling (H3): transport restricted to edges B supports.

Pre-registered: TRANSPORT_THRESHOLD = 0.5 (oracle transport fidelity considered "preserved").
Writes results/T2_v2.json. Needs .venv.
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
import gw_align as gw        # noqa: E402
import transport as tr       # noqa: E402
import function_test as ft   # noqa: E402

RESULTS = Path(__file__).resolve().parents[1] / "results"
REAL_NPZ = _ROOT / "data" / "celegans_real.npz"
REWIRES = [0.0, 0.05, 0.1, 0.2, 0.4]
TRANSPORT_THRESHOLD = 0.5


def run():
    c = load_celegans(path=REAL_NPZ)
    model_A, bat = ft.build_reference(c)
    n = c.n

    rows = []
    for rewire in REWIRES:
        W_B, perm = gw.perturb_connectome(c.W, rewire_frac=rewire, seed=0)
        # B's I/O indices are images of A's under the true permutation
        sidx_B = perm[model_A.sensory_idx]
        midx_B = perm[model_A.motor_idx]

        # --- oracle correspondence (ground truth) ---
        oracle = perm                      # A-node i -> B-node perm[i]
        W_T_oracle = tr.transport_weights(c.W, oracle, n)
        fid_oracle = ft.transport_fidelity(model_A, bat, W_T_oracle, sidx_B, midx_B)

        # --- oracle + feasibility mask (H3: only edges B supports) ---
        feas = tr.feasibility_mask(W_B)
        W_T_masked = tr.transport_weights(c.W, oracle, n, feasibility=feas)
        fid_masked = ft.transport_fidelity(model_A, bat, W_T_masked, sidx_B, midx_B)

        # --- GW-estimated correspondence (alignment-quality cost) ---
        T = gw.entropic_gw(c.W, W_B, epsilon=5e-3, n_iter=150)
        gw_corr = gw.correspondence_from_coupling(T)
        W_T_gw = tr.transport_weights(c.W, gw_corr, n)
        fid_gw = ft.transport_fidelity(model_A, bat, W_T_gw, sidx_B, midx_B)

        rows.append({
            "rewire_frac": rewire,
            "fidelity_oracle": fid_oracle,
            "fidelity_oracle_masked": fid_masked,
            "fidelity_gw": fid_gw,
        })

    # V2 verdict: oracle transport at zero divergence
    oracle0 = rows[0]["fidelity_oracle"]
    v2_pass = oracle0 >= TRANSPORT_THRESHOLD
    # V3: find boundary where oracle fidelity drops below threshold
    boundary = next((r["rewire_frac"] for r in rows if r["fidelity_oracle"] < TRANSPORT_THRESHOLD), None)
    # H3: does the feasibility mask cap fidelity even with oracle correspondence?
    mask_cost0 = rows[0]["fidelity_oracle"] - rows[0]["fidelity_oracle_masked"]

    out = {
        "experiment": "T2-V2 transport-preserves-function (+V3 boundary)",
        "substrate": "real-celegans + perturbation model",
        "transport_threshold": TRANSPORT_THRESHOLD,
        "per_rewire": rows,
        "v2_oracle_fidelity_at_zero": oracle0,
        "v2_passed": bool(v2_pass),
        "v3_boundary_rewire": boundary,
        "h3_feasibility_mask_cost_at_zero": mask_cost0,
        "verdict": (
            f"Oracle transport {'PRESERVES' if v2_pass else 'does NOT preserve'} function at "
            f"zero divergence (fid {oracle0:.2f}). "
            + (f"Collapses past rewire {boundary}. " if boundary is not None else "Holds across swept divergence. ")
            + (f"Feasibility mask costs {mask_cost0:.2f} FPS (H3)." )
        ),
    }
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "T2_v2.json").write_text(json.dumps(out, indent=2))
    print("rewire | oracle | oracle+mask | gw")
    for r in rows:
        print(f"  {r['rewire_frac']:.2f}  |  {r['fidelity_oracle']:.2f}  |  "
              f"{r['fidelity_oracle_masked']:.2f}      |  {r['fidelity_gw']:.2f}")
    print("VERDICT:", out["verdict"])
    return out


if __name__ == "__main__":
    run()
