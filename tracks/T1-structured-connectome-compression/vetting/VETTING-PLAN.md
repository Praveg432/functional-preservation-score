# T1 — Vetting Plan (go/no-go gates)

Cheap, synthetic-first, falsifiable probes before committing to the full sweep. Pattern
follows the workspace's track-1 vetting discipline.

## V1 — Baseline reality gate
- **Test:** can a connectome-GNN reproduce a baseline functional readout above a trivial
  control on at least one substrate (start with C. elegans, then one FlyWire sub-circuit)?
- **Pass:** fidelity clearly above shuffled-graph / random-readout control.
- **Fail → stop:** if a connectome graph gives no functional signal, T1 has no object to
  compress. (Low risk — flyGNN already shows this is possible.)

## V2 — Structure-advantage gate (the load-bearing one)
- **Test:** at a single hard budget (50% sparsity + int4), does engram-aware compression
  retain a pre-registered fidelity threshold while uniform fails?
- **Pass:** engram-aware ≥ threshold AND uniform < threshold, with a margin, on ≥2 seeds.
- **Fail → re-scope or kill:** if engram-aware ≈ uniform, H1 is refuted. Report it as a
  corrective to the blueprint's "structured sparsification" premise and do **not** scale up.

## V3 — Boundary sharpness gate
- **Test:** is there a genuine collapse contour (sharp) rather than smooth decay?
- **Pass:** fidelity shows an identifiable knee over the swept grid.
- **Inconclusive allowed:** if smooth, the "map" is still reportable; just reframe the claim
  from "boundary" to "degradation profile."

## Pre-registration

Fix fidelity thresholds, engram-aware definitions, seeds, and controls in a committed file
**before** running V2. No post-hoc threshold changes.
