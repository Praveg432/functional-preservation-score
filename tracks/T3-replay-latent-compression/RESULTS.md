# T3 — Results (replay→latent compression)

Substrate: **real** CA1 linear-track session (nelpy example-data `linear-track`, public;
31 sorted units, 28,829 spikes, ~33 min, + video position). Loader: `src/events.py`. Requires
the `.venv` (scipy/h5py). Pre-registration: `PRE-REGISTRATION.md` (to be fixed before V2).

## V1 — data + event gate → **PASS**
`experiments/T3_v1_data_gate.py` → `results/T3_v1.json`

- 62 run-epoch population sequences (31 units × 25 time-bins), units place-ordered.
- Structure measured by **Bayesian 1-D position decoding** (the canonical replay instrument):
  can the animal's trajectory be decoded from the population sequence?
  - real sequences: mean decode score **0.34**
  - time-shuffled null: **0.20**
  - margin **+0.14** (criterion: >+0.1 and real>0.3) → **PASS** across 62 sequences.
- Conclusion: the real run epochs carry genuine decodable sequential structure that
  time-shuffling destroys. There is a real "sequence" for T3 to compress.

### Instrument note (honest process)
The first V1 metric (peak-firing rank-correlation) gave real 0.31 vs shuffled 0.28 — **failed**
(too weak with ~9 active units per partial-traversal epoch). Diagnosed (`scripts/diagnose_t3.py`):
data is clean (position/spikes aligned, 62 epochs); the *metric* was weak. Replaced once with
Bayesian decoding (literature-standard), which passed. Metric fixed on diagnosis, not blind
iteration.

## Honest scope
This compresses *decoded neural population sequences* (awake run trajectories — the same object
as a replay event), not memories or identity. It tests the information-theoretic compressibility
of such sequences, nothing about synaptic reading or identity (Tier-A).

## V2 — compression-floor gate → **PASS** (on richer DANDI data, with a corrected instrument)
`experiments/T3_v2_compression_floor.py` → `results/T3_v2.json`

### Getting here (honest trail)
V2 first failed on the nelpy session (too few clean laps; headroom margin ~+0.09). Per the
chosen path, richer data was streamed from **DANDI 000044 (Grosmark/Buzsáki, hc-11), Buddy
session** — only spike times + linearized position pulled from the 5 GB remote NWB via
remfile+h5py (`scripts/fetch_dandi_replay.py`), yielding **48 pyramidal units, 55 clean laps**.
Even then, the trajectory-rank decode-fidelity metric had a structurally-high null (every AE
reconstruction looks like a generic place-field sweep). After diagnosing this three times
(lap-filtering → direction-splitting → null decomposition), the **metric** was replaced once,
properly, with **event identification accuracy**: is recon_i nearer its own original than any
other event? Bounded, exact chance = 1/n, immune to the sweep-shape leak.

### Result
- **Headroom:** uncompressed AE identifies held-out events at **top-1 = 0.75 vs chance 0.125
  (6× chance)** — the latent carries event-specific content. Gate passes.
- **Compression frontier (identification top-1 vs bits-per-event):** identification rises with
  the latent bit budget and saturates; it degrades gracefully toward chance as bits shrink.
  Reliable "preserved" operating points include latent-dim 16 @ ~16 bits/event (top-1 0.75) and
  dim 8 @ ~8 bits/event (0.50); the pre-registered threshold (top-1 ≥ 2×chance) is first met
  around **~4–16 bits/event**.
- **Headline (honest):** a replay sequence (48 units × 25 bins, raw ~38k bits) remains
  identifiable from a latent of order **10–50 bits/event — roughly 1000×+ compression** — with
  graceful degradation. This is the information-theoretic plausibility of the "compressed
  backup" idea, measured on real replay data (H1/H2 supported).

### Honest caveats
- Small held-out test set (n≈8 laps per direction) → the frontier is noisy; exact floor
  bits/event is approximate, reported as a region not a precise number.
- This compresses *decoded population sequences*, not memories/identity (Tier-A unchanged). It
  shows such sequences are highly compressible while staying event-identifiable — nothing about
  synaptic reading or that a backup "contains a person."

## V3 — incremental-sync capacity / interference → **PASS**
`experiments/T3_v3_sync_capacity.py` → `results/T3_v3.json`

Tests the blueprint's "background sync into a bounded latent backup" directly: stream real
DANDI replay laps into a FIXED-SIZE store, measure recoverability (identification, chance=1/load)
as load grows. Two architectures:

| load | superposition recovery | oldest-3 recovery | slot store (cap 10) |
|---|---|---|---|
| 2 | 1.00 | 1.00 | 1.00 |
| 6 | 0.67 | 1.00 | 1.00 |
| 10 | 0.50 | 1.00 | 1.00 |
| 15 | 0.40 | 1.00 | 0.67 |
| 20 | 0.30 | 1.00 | 0.50 |

- **Superposition (one holographic latent = the blueprint's W_S):** recovery degrades
  **gracefully and monotonically** with load (crosstalk grows); no hard limit, but fidelity bleeds.
- **Slot store (fixed slots, FIFO):** **perfect up to n_slots=10, then a hard cliff** (recovery
  ≈ n_slots/load; evicted oldest events are gone).
- **Non-obvious finding:** under random-key binding, the *oldest* events are not preferentially
  lost (oldest-3 stays 1.00) — crosstalk is distributed, so average recovery falls while specific
  events remain identifiable.
- H3 supported: a bounded sync store has a real **capacity/interference trade-off**, and the two
  designs trade off differently (graceful bleed vs perfect-then-cliff).

## T3 — final verdict

All three gates pass on real hippocampal replay data (DANDI 000044):
1. **V1** — real population sequences carry decodable trajectory structure (0.34 vs 0.20 null).
2. **V2** — those sequences are highly compressible: **~1000×+ compression (order 10–50
   bits/event) while remaining event-identifiable** (top-1 0.75 vs chance 0.125).
3. **V3** — a bounded "background-sync" latent store shows a genuine capacity/interference
   trade-off; a single fixed latent keeps syncing but recovery fidelity decays with load (no
   free unbounded backup).

**Contribution:** a measured, information-theoretic characterization of the blueprint's
"compressed replay backup" idea — it is plausible *as compression*, with a quantified
compression frontier and capacity limit, on real replay data, scored by a clean identification
instrument.

**Honest scope (unchanged):** compresses *decoded population sequences*, not memories/identity.
Says nothing about non-destructive synaptic reading or that a backup "contains a person"
(Tier-A A1 remains absent). Small test sets → frontier/floor reported as regions, not exact.

**Banked assets:** DANDI NWB streaming extractor, direction-aware lap/sequence loader, Bayesian
decode + identification instruments, quantized sequence autoencoder, two sync-store models.
