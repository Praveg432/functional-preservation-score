# T5 — Vetting Plan (go/no-go gates)

## V1 — Readout + ablation sanity
- **Test:** do the functional readouts respond to ablation at all (lesions change function)?
- **Pass:** ablation produces measurable, non-random functional change.
- **Fail → fix readout:** a readout insensitive to lesions cannot test separability.

## V2 — Separability-vs-null gate (load-bearing)
- **Test:** is any candidate partition significantly more separable than a random-partition
  null?
- **Pass:** separability index > null with margin on ≥2 substrates/seeds.
- **Fail → corrective result:** "the asserted partition is no more separable than random" is a
  direct, publishable refutation of the blueprint's Stage-1 premise. Report it.

## V3 — Swap-tolerance gate
- **Test:** does payload function survive swapping in a different Base-OS, and how does it
  decay with Base-OS divergence?
- **Pass:** identifiable tolerance region + decay curve.
- **Inconclusive allowed.**

## Pre-registration
Fix candidate partitions, separability index, null model, and seeds before V2.
