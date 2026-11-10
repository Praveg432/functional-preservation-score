# T1 — Structured, Engram-Aware Compression of Connectome-GNNs

**Type:** feasible in-silico core. **Attacks:** blueprint Stage 2 (quantization/compression).
**Open question N1.** **Status:** scaffold, not executed.

## One-line claim

On a connectome loaded as a graph network and driven to a **functional/behavioral** readout,
there is a *structured, engram-aware* sparsification + low-bit quantization regime that
preserves function far beyond uniform compression, and the breakdown boundary over
(sparsity × bit-depth × structure) is a measurable law.

## Why it is novel (vs. prior art in `NOVELTY-SCAN.md`)

- Generic GNN prune+quant (arXiv 2510.22058) and BitNet-1.58 GNNs optimise **accuracy on
  standard graph benchmarks**. T1's readout is **behavior/function of a connectome** in an
  embodied or activity-matched loop — a different, biologically-meaningful objective.
- SimCert certifies behavioral similarity of **standard DNNs**, not connectome function.
- The **engram-aware structure axis** (preserve high-centrality / multi-synaptic-bouton-
  analogue / high-betweenness edges, motivated by torpor engram-resilience in `scans/01`) vs.
  **uniform magnitude pruning** is the contribution — nobody has compared them on a connectome.

## Boundary (what this track owns / does not own)

- Owns: the compression method, the behavioral-fidelity metric, and the breakdown map.
- Does not own: the alignment (T2), the write (T4), the partition (T5). It consumes shared
  loaders only.

## Shared dependencies

- Phase-0 shared loaders: FlyWire sub-circuits (central complex / mushroom body), MICrONS
  column traces, C. elegans whole-brain (fast sanity harness). See `../../DATASETS.md`.

See `00-OVERVIEW.md`, `04-METRICS-RISKS-SCAFFOLD.md`, and `vetting/VETTING-PLAN.md`.
