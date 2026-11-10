# T2 — Vetting Plan (go/no-go gates)

## V1 — Correspondence sanity (worm)
- **Test:** does GW recover the known C. elegans neuron matching between two individuals
  above chance?
- **Pass:** precision/recall clearly above a permutation baseline.
- **Fail → stop:** if GW cannot match worms with ground truth, the whole alignment premise is
  dead in-silico; report and halt the surrogate chain here.

## V2 — Transport-preserves-function gate (load-bearing)
- **Test:** with an **oracle** (ground-truth) correspondence, does transporting A's weights
  onto B reproduce A's function above a pre-registered threshold?
- **Pass:** oracle-transport fidelity ≥ threshold.
- **Fail → major finding:** if even *perfect* correspondence does not preserve function, then
  alignment is not the bottleneck — the target wiring cannot host the function (supports H3,
  and is itself a strong corrective result). Record verbatim; do not paper over.

## V3 — Boundary gate
- **Test:** under controlled rewiring, is there a divergence level where transport collapses?
- **Pass:** identifiable collapse point; relationship to divergence reported.
- **Inconclusive allowed:** reframe as a degradation profile if no sharp knee.

## Pre-registration

Fix thresholds, divergence grid, oracle-vs-GW ablation, and seeds before V2.
