# T5 — Empirical Separability of the Base-OS / Identity-Payload Partition

**Type:** surrogate. **Attacks:** blueprint Stage 1 (partition) / risk **B2**.
**Open question N5.** **Status:** scaffold, not executed.

## One-line claim

The blueprint *asserts* a clean split between a regenerable "Base-OS" and a transferable
"identity payload." T5 tests that assertion the only way currently possible: on a connectome
with a functional readout, **ablate "Base-OS-like" sub-graphs and measure whether a defined
"payload-like" function survives, and vice versa** — turning an assumption into a measurement.

## Why it is novel

- Connectome ablation studies exist, but nobody has posed the blueprint's specific
  **separability** question: is there a partition whose two sides are *functionally
  dissociable* enough that one could, in principle, be swapped? This is a graph-functional
  property that can be quantified and has not been.

## Boundary

- Owns: the partition + ablation + functional-dissociation measurement.
- Feeds: T2 (defines the "payload" sub-graph to align) and T4 (defines what to install).
- Does **not** claim the human partition is real; it measures separability on animal
  connectomes as the nearest testable proxy.

See `00-OVERVIEW.md`, `04-METRICS-RISKS-SCAFFOLD.md`, `vetting/VETTING-PLAN.md`.
