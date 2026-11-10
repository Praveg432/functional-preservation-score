# T3 — Overview

## Problem

The blueprint's Sub-Track 1 compiles sleep-replayed engrams into a compressed latent "backup"
(LoRA-style). The vetting (`../../scans/03`, `../../scans/04`) found the *reading* of such
content at identity scale is absent, but the **compression question is well-posed and testable
on public replay data**: given a decoded replay sequence, how compressible is it?

## Approach

1. **Event extraction.** From a hippocampal session, detect SWR events and build population
   spike-sequence tensors (or use MICrONS stimulus-evoked trace sequences as a fallback).
2. **Latent model.** Train a sequence autoencoder / VQ-style quantized latent; sweep latent
   dimensionality, codebook bit-depth (8→4→ternary), and sparsity.
3. **Fidelity frontier.** Measure reconstruction of the represented *sequence* (decoded
   trajectory / order / timing), not raw voltage. Chart fidelity vs. bits-per-event.
4. **Incremental-sync sim.** Simulate streaming many events into a fixed-size latent store
   (the "background sync") and measure catastrophic interference vs. capacity — how much can
   one latent hold before older events are overwritten?

## Hypotheses

- H1: replay sequences compress to far fewer bits than raw spikes with high sequence fidelity.
- H2: there is a bits-per-event floor below which sequence identity is lost.
- H3: incremental sync into a fixed store shows a capacity/interference trade-off (relevant to
  the blueprint's "up-to-date backup" claim).

## Honest scope

This compresses *decoded neural sequences*, not memories or identity. It tests the
information-theoretic plausibility of the "compressed backup" idea, not that the backup
contains a person. It says nothing about non-destructive synaptic reading (Tier-A A1).
