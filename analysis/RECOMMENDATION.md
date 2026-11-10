# Recommendation — what to actually build

## Bottom line

The end-to-end "Partitioned Base-OS + Quantized Connectome Migration" vision is **not
thesis-grade**. Three middle links are absent in principle, not merely immature: a
non-destructive single-synapse human read (A1), an identity-level write into a
differently-wired living brain (A3), and cross-subject human transfer (A4) — see
`FEASIBILITY-RISK-LEDGER.md`. The individually-real references do not compose into the claim.

Do **not** frame a thesis around migration, life extension, or "mind uploading." Frame it
around the one closed, testable sub-system that survives vetting.

## The buildable residual — a genuine thesis

**Title (working):** *Structured, Engram-Aware Sparsification and Low-Bit Quantization of
Connectome Graph Networks: How Much Can You Compress a Wiring Diagram Before Behavior Breaks?*

**One-line claim.** On *public* connectomes (FlyWire), there exists a structured
sparsification + quantization regime that preserves behavioral function far beyond uniform
pruning, and the breakdown boundary is characterizable — a concrete, measurable science.

**Why it is sound.**
- Uses only Tier-C assumptions that **hold**: memory/behavior survives *structured* turnover
  (C1), and a connectome-GNN can drive simulated behavior (C2).
- Needs **no** biological read/write, no humans, no clone — sidesteps every failing Tier-A link.
- Has public data and prior code (FlyWire, flyGNN, NeuroMechFly, Loihi-2 sim).
- Produces a falsifiable *capability/boundary* result in the style of the workspace's other
  projects (e.g. coverage-boundary and quantization-floor tracks), not a hype claim.

## Concrete Phase-1 plan (the only phase to commit to now)

1. **Load** the FlyWire connectome as a recurrent message-passing GNN; reproduce a baseline
   behavioral readout in a simulated body (locomotion/escape).
2. **Pruning sweep.** Compare *uniform* vs *structured/engram-aware* sparsification (preserve
   high-centrality / multi-synaptic-bouton-analogue edges) at 10–70% removal.
3. **Quantization sweep.** 8-bit → 4-bit → ternary {-1,0,+1} on synaptic weights, measuring
   behavioral fidelity, not reconstruction error.
4. **Teacher–student distillation.** Full-precision teacher → sparse/quantized student;
   measure behavioral-transfer fidelity across *perturbed* graphs (the gap the FlyWire papers
   do not test).
5. **Breakdown map.** Chart the (sparsity × bit-depth × structure) frontier where behavior
   collapses. That map is the contribution.

**Vetting gate (go/no-go before full commitment):** on a small sub-circuit, structured
sparsification at 50% + 4-bit must retain ≥ a pre-registered behavioral-fidelity threshold
while uniform pruning at the same budget fails. If structured ≈ uniform, the central claim is
dead and the track is killed — exactly the cheap, falsifiable probe pattern used elsewhere in
this workspace.

## What to explicitly drop (and say so in any writeup)

- Human mind migration, cloning, life extension framing.
- "Non-destructive synaptic read" and "identity write" — absent-in-principle, not future work.
- GW alignment at connectome scale — infeasible as stated; if alignment is studied at all,
  restrict to small graphs and treat scaling as an open theory question, not a solved step.
- The 300 TB / 5–10 TB footprint numbers — unverified arithmetic downstream of a false premise.

## How this maps to the source roadmap

The blueprint's **Phase 1** is the *only* phase that is real and buildable, and even it must
be reframed from "test behavioral transfer en route to migration" to "characterize the
structured-compression/behavior frontier as a standalone result." Phases 2–4 depend on the
failing Tier-A links and should not be planned as research deliverables.

## Suggested next action

Promote the Phase-1 residual into a standalone experimental track (its own `TRACK.md`,
`00`–`04` docs, and a `vetting/` gate on structured-vs-uniform behavioral fidelity), matching
the `research-program/tracks/` pattern. Keep it in this folder or move it beside the other
tracks — your call. Nothing beyond Phase-1 should be scaffolded until the vetting gate passes.
