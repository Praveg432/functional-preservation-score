# T2 — Cross-Individual Connectome Alignment with Functional Transport

**Type:** feasible in-silico core. **Attacks:** blueprint Stage 3 (alignment) / risk **B1**.
**Open question N2.** **Status:** scaffold, not executed.

## One-line claim

Given two individuals' connectomes, a hierarchical Gromov-Wasserstein node-correspondence can
be found on an M4, and — the open part — we can measure whether **transporting a functional
circuit from A onto B's wiring via that correspondence preserves A's input→output function**.
Alignment quality is judged by *function transported*, not matching distance.

## Why it is novel

- Scalable GW (S-GWL, HOT, multi-scale) and brain alignment (FUGW) already solve *matching*.
  They score correspondence by distance/accuracy. **None test functional transport**: take
  A's weights, push them through the A→B correspondence onto B's graph, run B, and ask if B
  reproduces A's behavior. That composition is the contribution.
- This is the honest, testable core of the blueprint's "compute W_align and write it" step,
  minus the biology.

## Boundary

- Owns: the alignment→transport→function-test pipeline and its failure analysis.
- Consumes: T5's definition of which sub-graph counts as the "payload" (explicit cross-track
  dependency); shared loaders.
- Does not own: the biological write (T4 simulates installation; T2 assumes exact weight set).

## Shared dependencies

- C. elegans across individuals (worm-to-worm) as the primary testbed (same cell labels give
  a **ground-truth correspondence** to score GW against — a rare luxury).
- FlyWire left/right hemisphere or coarsened inter-individual proxy as a harder case.

See `00-OVERVIEW.md`, `04-METRICS-RISKS-SCAFFOLD.md`, `vetting/VETTING-PLAN.md`.
