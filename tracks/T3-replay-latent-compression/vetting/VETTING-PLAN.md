# T3 — Vetting Plan (go/no-go gates)

## V1 — Data + event gate
- **Test:** can we extract usable replay/sequence events (real hippocampal session, or
  MICrONS trace-sequence fallback) with a sane signal?
- **Pass:** events reconstructable by a trivial baseline above chance.
- **Fail → re-scope:** switch to the fallback substrate before investing in the AE.

## V2 — Compression-floor gate (load-bearing)
- **Test:** is there a bits-per-event level where sequence fidelity holds, and a lower one
  where it collapses?
- **Pass:** identifiable floor with a margin over chance.
- **Fail → reframe:** if fidelity is flat (either always good or always bad), report the
  method limitation rather than a floor.

## V3 — Capacity gate
- **Test:** does the fixed-size incremental store show a real capacity/interference trade-off?
- **Pass:** monotone degradation of oldest-event fidelity with load.
- **Inconclusive allowed.**

## Pre-registration
Fix fidelity thresholds, latent-sweep grid, and the event detector before V2.
