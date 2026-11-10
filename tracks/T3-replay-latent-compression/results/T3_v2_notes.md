# T3-V2 — compression-floor gate: UNDERPOWERED on this session (honest stop)

Result: `T3_v2.json` (headroom gate result). Diagnostics: `scripts/diagnose_t3_ae.py`.

## What was tested
Does a bits-per-event floor exist for compressing real population sequences while preserving
the represented trajectory? Protocol required a **headroom gate first** (T1 lesson): the
uncompressed AE must reconstruct sequences whose decode-fidelity clearly beats a time-shuffle
null, before any floor claim.

## What happened (iterated data-conditioning twice, then stopped per the no-patch-twice rule)
1. **Epoch sequences (62):** headroom margin +0.07 (recon 0.24 vs null 0.18) — FAIL. Diagnosis:
   run epochs are *partial* traversals pinned to one track end; little trajectory content.
2. **Clean laps (full traversals):** decode-score improves (0.41) but only **3–10 laps exist**
   in this session — far too few to train an AE + held-out sweep. Sample-size wall.
3. **Overlapping windows (110):** enough samples, but headroom margin +0.092 (recon 0.20 vs
   null 0.11) — still just under the +0.1 bar. Raw-sequence-correlation framing is a bit better
   (0.57 vs 0.43, margin +0.13) but the time-shuffle null is high (0.43), so correlation is not
   a clean sequence instrument here either.

## Honest conclusion
- The obstacle is **not** a bug and not blind: three independent conditionings all say the same
  thing — **this single CA1 session has genuinely weak, hard-to-reconstruct sequential content**
  (originals self-decode only ~0.34; AE reconstructions ~0.20). There is too little trajectory
  signal above the null to define a meaningful compression floor on this data.
- Per the discipline applied to Effect B: **do not manufacture a pass by threshold-shopping.**
  T3-V2 is **underpowered on this session**, not resolved.

## Decision / recommendation (flagged for user)
Two honest options:
- **(a) More data:** use a session (or pooled sessions) with many clean laps and strong place
  coding — e.g. a CRCNS hc-3/hc-11 session (needs login) or a DANDI replay dataset. With
  hundreds of clean traversals the headroom gate can be tested properly. Medium lift (auth +
  loader), but the *right* way to make a real T3 claim.
- **(b) Shelve T3-V2** like Effect B: bank the V1 structure result + the working pipeline
  (events/fidelity/autoencoder) and move to the surrogate chain T5->T2->T4, where the novel
  "attack the blocked points" contributions live.

## What is banked regardless
- Real hippocampal loader (`src/events.py`: epochs, laps, windowed sequences).
- Shared Bayesian decode instrument (`src/fidelity.py`).
- Sequence autoencoder with quantized latent (`src/seq_autoencoder.py`).
- V1 PASS (structure exists) + an honest, diagnosed negative on V2 headroom for this session.
