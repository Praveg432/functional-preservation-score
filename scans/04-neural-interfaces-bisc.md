# Scan 04 — BISC & High-Density Neural Mesh

**Blueprint claim.** Chronic, ultra-flexible **sub-dural intracortical** mesh arrays
(advanced BISC CMOS variants) continuously record multi-unit spiking and LFP across the
association cortex — the "read-net" that enables non-destructive live mapping.

**Verdict: device REAL; description MIS-DESCRIBED in a way that breaks the read premise.**

## What the device actually is

- Columbia (Shepard lab) built a **wireless, mechanically flexible, ~25 µm-thick,
  65,536-electrode / 1,024-channel subdural _surface_ microelectrode array** with integrated
  antennas — published in *Nature Electronics* (2025) and demonstrated with stable chronic
  in-vivo recordings.
  [Nature Electronics](https://www.nature.com/articles/s41928-025-01509-9) ·
  [PubMed](https://pubmed.ncbi.nlm.nih.gov/42394952) ·
  [VLSI'23 PDF](https://sld.cs.columbia.edu/pubs/zeng_vlsi23.pdf) ·
  [Columbia EE](https://www.ee.columbia.edu/news/paper-thin-implant-can-listen-your-brain-signals)

## The mis-description that matters

- **BISC is a _subdural surface_ (µECoG) device, not an _intracortical_ mesh.** It sits on
  the cortical surface and reads **field potentials and surface-resolved population activity**
  — it does **not** penetrate cortex and does **not** resolve individual neurons, let alone
  individual synapses. Calling it an "intracortical mesh" that reads the connectome is simply
  wrong about the modality.
- **65,536 electrodes ≠ 1.4×10^10 nodes.** The blueprint's identity payload is ~12–14 billion
  neurons and ~10^14 synapses. A surface array with ~65K contacts is ~6–9 **orders of
  magnitude** short of per-neuron coverage and cannot in principle observe single synaptic
  weights, which is what the quantization/transfer math requires.

## Bearing on the blueprint

- **Supports:** high-channel-count, chronic, wireless, read+stimulate surface interfaces are
  real and improving fast. Good for population-level decoding and closed-loop stimulation.
- **Breaks:** the Sub-Track 1 premise of a *non-destructive chronic read of the connectome at
  synaptic resolution*. No existing or near-term in-vivo human modality reads individual
  synaptic weights chronically. Synapse-resolution connectomics today is **destructive**
  volume electron microscopy on fixed tissue — the exact thing the blueprint says it avoids.
  This is a load-bearing contradiction, logged in the risk ledger.

*Content rephrased from sources for licensing compliance.*
