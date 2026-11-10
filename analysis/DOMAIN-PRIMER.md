# Domain Primer — the actual background, plainly stated

This primer establishes the real concepts the blueprint invokes, so the rest of the
analysis can reason precisely. It is deliberately neutral: it states what each field
*actually* claims, independent of the blueprint's framing.

## 1. Connectomics: wiring diagrams and what they omit

A **connectome** is a map of which neurons connect to which, via synapses. The state of the
art is the FlyWire adult *Drosophila* connectome (~139K neurons), reconstructed from
**volume electron microscopy (vEM)** of fixed, sliced tissue. Two facts matter:

- **vEM is destructive.** You get a connectome by cutting and imaging dead tissue. There is
  no established way to read a full synaptic-resolution connectome from a *living* brain.
- **Topology is not dynamics.** A connectome gives edges, not the **synaptic weights, signs,
  neuromodulatory state, or time constants** that determine what the network *computes*.
  Driving behavior from a connectome requires *fitting* those missing parameters (see
  `../scans/02-connectome-gnn-flywire.md`).

Human cortex is ~86B neurons total; the association cortex + limbic structures the blueprint
targets are ~10^10 neurons with ~10^14 synapses. No imaging modality reads that from a live
human.

## 2. Engrams, memory, and synaptic turnover

An **engram** is the physical substrate of a stored memory — a sparse, distributed set of
neurons and the synapses among them. Two robust findings:

- Memory is carried by a **resilient sparse subset** of synapses. During torpor/hibernation
  the brain can shed 50–65% of synapses and still retain memories, because engram-critical
  contacts are preferentially preserved (`../scans/01-synaptic-pruning-torpor.md`).
- This argues for **structured, engram-aware** sparsification, not uniform low-bit crushing
  of every weight. The distinction is central to judging the blueprint's quantization claim.

## 3. Neural interfaces: surface vs. depth, read vs. write

- **Surface arrays (µECoG), e.g. BISC:** sit on the cortical surface, read field potentials
  and population activity at high channel count, wirelessly and chronically. They do **not**
  resolve single neurons or synapses (`../scans/04-neural-interfaces-bisc.md`).
- **Penetrating/intracortical probes (e.g. Neuropixels, Utah arrays):** resolve single-unit
  spikes but sample a tiny fraction of neurons and cause tissue damage over time.
- **Writing** to neurons: electrical microstimulation (coarse), and **optogenetics**
  (cell-type-specific, millisecond light control, but needs genetic opsin expression).
  Optogenetics underlies the 2026 Nobel and animal engram-tagging work
  (`../scans/05-optogenetics-and-ot-alignment.md`).

**Key asymmetry:** we can *read populations* and *write coarse patterns*, but we cannot read
or write individual synaptic weights across a whole brain in vivo.

## 4. Memory prosthetics: restoring vs. uploading

The USC/Wake Forest MIMO prosthetic learns the hippocampus's own **input→output transform**
and writes a corrected output to improve a patient's *own* recall (+37%). It restores the
*operation* of memory formation; it does **not** store or move a person's identity, and
cross-*subject* identity transfer in humans is unsupported
(`../scans/03-hippocampal-prosthetics-mimo.md`).

## 5. Cross-brain alignment: optimal transport

Two brains have no shared neuron labelling, so mapping one onto another is a **graph/
distribution matching** problem. **Gromov-Wasserstein (GW)** optimal transport matches
structure without a shared coordinate system and is genuinely used to align brains at the
level of functional parcels. But GW is **NP-hard and non-convex**, and does not scale to
10^10 nodes as written (`../scans/05-optogenetics-and-ot-alignment.md`).

## 6. The three paradigms of "not dying," framed honestly

1. **In-situ molecular repair** (epigenetic reprogramming, senolytics): real, active field;
   faces hard limits (e.g. extracellular-matrix cross-linking, somatic mutation load). The
   blueprint's framing here is a reasonable summary of a genuine debate.
2. **Whole-brain emulation (destructive scan + simulate):** conceptually clear, data-volume
   and scanning requirements are extreme; synapse-resolution scanning is destructive.
3. **The blueprint's "partitioned + quantized migration":** a *third* framing that tries to
   avoid (2)'s destructiveness and data volume by (a) dropping "Base-OS" regions, (b)
   quantizing, (c) reading non-destructively, (d) writing into a clone. As the vetting shows,
   steps (c) and (d) have no evidentiary basis; (a) and (b) are hypotheses with partial
   analogues.

**Takeaway for the reader.** The individual fields are real and impressive. The blueprint's
move is to *chain* their most optimistic edges into a pipeline whose two middle links (live
synaptic read, identity-level write into another brain) do not exist even in principle today.
