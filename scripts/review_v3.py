"""Critical review extraction: separate the two effects conflated in the V3 headline.

Effect A (floor): at low bit-depth, uniform quantization forces high sparsity it cannot undo.
Effect B (matched-conditions advantage): at the SAME effective sparsity AND same bit-depth,
does engram actually preserve more function? int8 (no floor) is the clean place to check B.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
d = json.load(open(ROOT / "tracks/T1-structured-connectome-compression/results/T1_v3_real.json"))
S = d["surface"]
targets = d["axes"]["targets"]


def best_engram(bd, t):
    vals = [r["fps"] for r in S if r["bitdepth"] == bd and r["policy"].startswith("engram") and r["target"] == t]
    return max(vals) if vals else None


def uni(bd, t):
    r = [r for r in S if r["bitdepth"] == bd and r["policy"] == "uniform" and r["target"] == t]
    return r[0] if r else None


for bd in ["int8", "int4", "ternary"]:
    print(f"\n=== {bd}: uniform vs best-engram at matched target sparsity ===")
    ew = uw = 0
    for t in targets:
        u = uni(bd, t)
        e = best_engram(bd, t)
        if u is None or e is None:
            continue
        floor_note = " [uniform BELOW-FLOOR: cannot reach this sparsity]" if u["below_floor"] else ""
        tag = "ENGRAM" if e > u["fps"] + 1e-6 else ("tie" if abs(e - u["fps"]) <= 1e-6 else "uniform")
        if tag == "ENGRAM":
            ew += 1
        elif tag == "uniform":
            uw += 1
        print(f"  t={t}: uniform {u['fps']:.3f} (eff {u['achieved_sparsity']:.3f}) "
              f"best-engram {e:.3f}  -> {tag}{floor_note}")
    print(f"  tally: engram wins {ew}, uniform wins {uw}")
