# T3 — Metrics, Risks, Scaffold

## Metrics
- **Sequence reconstruction fidelity:** decoded-trajectory correlation / order-preservation /
  timing error between original and reconstructed replay event.
- **Bits per event:** effective bits of the latent (dim × codebook bit-depth × density).
- **Compression frontier:** fidelity vs. bits-per-event curve; locate the floor (H2).
- **Capacity/interference:** events stored before fidelity of the oldest drops below threshold.

## Risks
| Risk | Mitigation |
|---|---|
| Hippocampal dataset access/licensing | Confirm CRCNS/DANDI terms first; MICrONS trace-sequence fallback keeps the method testable without it. |
| Replay detection is itself nontrivial | Use published detectors/thresholds; or operate on externally-provided decoded sequences. |
| "Compression works" is unsurprising | The contribution is the *floor* and the *capacity trade-off*, quantified — not that compression exists. |

## Scaffold
```
T3-replay-latent-compression/
  src/
    events.py         # SWR detection / sequence tensor construction (or trace sequences)
    seq_autoencoder.py# sequence AE + VQ/low-bit latent
    fidelity.py       # sequence reconstruction metrics
    sync_store.py     # fixed-size incremental store + interference sim
  experiments/
    T3a_frontier.py   # fidelity vs bits-per-event (H1,H2)
    T3b_capacity.py   # incremental-sync capacity/interference (H3)
  results/
```

## Compute
Small sequence models; minutes–low hours on MPS. Single-session data fits in RAM.
