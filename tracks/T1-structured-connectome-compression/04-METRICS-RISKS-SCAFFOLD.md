# T1 — Metrics, Risks, Scaffold

## Metrics

- **Behavioral/functional fidelity** (primary): task-appropriate — heading error (fly
  locomotion), held-out calcium R² / correlation (MICrONS), activity-motif similarity
  (C. elegans). Reported as fraction of full-precision baseline retained.
- **Compression ratio:** effective bits/edge × edges retained vs. baseline.
- **Collapse boundary:** the (sparsity, bit-depth) contour where fidelity drops below a
  pre-registered threshold (e.g. 90% of baseline).
- **Structure advantage:** boundary shift (engram-aware − uniform), in budget units.

## Risks

| Risk | Mitigation |
|---|---|
| Embodied fly loop too heavy for M4 | Fall back to activity-matching readout; use sub-circuits, not whole brain. |
| "Engram-aware" heuristic is arbitrary | Pre-register 2–3 graph-theoretic definitions; report all, no cherry-picking. |
| Result is just the known "50% prune is fine" | Push to int4/ternary + high sparsity *jointly*, where generic results stop; the joint frontier is the contribution. |
| MPS op gaps | Keep models in ops with MPS support; CPU-fallback acceptable at this scale. |

## Scaffold (code layout, to build in Phase 0/1)

```
T1-structured-connectome-compression/
  src/
    load_connectome.py     # shared loader wrappers (fly/micron/elegans)
    gnn_model.py           # recurrent message-passing / LIF readout model
    compress.py            # pruning (uniform + engram-aware) + quantization (int8/int4/ternary)
    distill.py             # teacher->student functional distillation
    fidelity.py            # behavioral/functional fidelity metrics
  experiments/
    T1a_baseline.py        # fit + validate baseline readout
    T1b_sparsity_sweep.py  # uniform vs engram-aware edge removal
    T1c_quant_sweep.py     # int8 -> int4 -> ternary
    T1d_joint_frontier.py  # crossed sparsity x bit-depth x structure -> breakdown map
    T1e_scaling_rule.py    # test H3 (boundary vs spectral/hub quantity)
  results/                 # committed JSONs + figures
```

## Compute

Single-model training per config in minutes–low hours on MPS; the sweep is embarrassingly
parallel across configs but run serially/resumably. Full run fits in a day.
