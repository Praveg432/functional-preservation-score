"""Verify every quantitative claim in paper/PAPER.md against committed result artifacts."""
import json
from pathlib import Path

R = Path(__file__).resolve().parents[1]


def g(p):
    return json.load(open(R / p))


d = g("tracks/T1-structured-connectome-compression/results/T1_v3_real.json")
fl = d["effective_sparsity_floor"]
print("T1v3 floors uniform int4/ternary:", round(fl["int4|uniform"], 2), round(fl["ternary|uniform"], 2))
print("T1v3 floors engram int4/ternary:", round(fl["int4|engram:strength"], 2), round(fl["ternary|engram:strength"], 2))

d = g("tracks/T1-structured-connectome-compression/results/T1_v4_real.json")
print("T1v4 boundary_model_invariant:", d.get("boundary_model_invariant"))

d = g("tracks/T3-replay-latent-compression/results/T3_v3.json")
print("T3v3 slot:", [(r["load"], round(r["slot_recovery"], 2)) for r in d["slot_curve"]])
print("T3v3 passed/monotone/cliff:", d.get("passed"),
      d.get("superposition_monotone_degradation"), d.get("slot_hard_capacity_cliff"))

d = g("tracks/T4-insilico-write-compiler/results/T4_v2.json")
print("T4 gaps:", [(r["divergence"], round(r["plausibility_gap"], 2)) for r in d["per_divergence"]])
print("T4 ripple_beats_plain / large_gap:", d.get("ripple_beats_plain"), d.get("large_plausibility_gap"))

d = g("tracks/T2-functional-transport-alignment/results/T2_v2.json")
print("T2 v3_boundary_rewire:", d.get("v3_boundary_rewire"))
print("T2 masked fidelity @5%:", round(d["per_rewire"][1]["fidelity_oracle_masked"], 2))
