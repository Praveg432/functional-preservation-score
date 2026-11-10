# T3 — Replay→Latent Compression-Fidelity Frontier

**Type:** feasible in-silico core. **Attacks:** blueprint Stage 5c (incremental sync/backup).
**Open question N3.** **Status:** scaffold, not executed.

## One-line claim

Treating a replayed neural **sequence** (sharp-wave-ripple event) as the thing to back up,
there is a measurable frontier: how few bits / how sparse a latent can encode a replay event
while still reconstructing the represented sequence above a fidelity threshold.

## Why it is novel

- Replay decoding (PMC5102323, real-world-speed replay) answers *what trajectory* a replay
  represents — a classification/decoding task. T3 asks a **compression** question: the
  minimal-bit latent that reconstructs the sequence. The blueprint's "incremental LoRA
  sync into a compressed latent W_S" is exactly a compression claim, never tested as one.

## Boundary

- Owns: the autoencoder/latent model, the bit/sparsity sweep, the fidelity frontier.
- Independent of the surrogate chain (T5→T2→T4); can run in parallel from Phase 0.

## Shared dependencies

- One public hippocampal single-session recording (CRCNS/DANDI) **[access-to-confirm]**, with
  MICrONS calcium traces as a non-ripple fallback for the sequence-compression method.

See `00-OVERVIEW.md`, `04-METRICS-RISKS-SCAFFOLD.md`, `vetting/VETTING-PLAN.md`.
