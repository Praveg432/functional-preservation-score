# Architecture Decomposition — the pipeline as verifiable sub-claims

The end-to-end architecture is six stages. Each is stated as the blueprint intends it, then
reduced to its load-bearing sub-claims with an evidence tag (REAL / OVERSTATED / HYPOTHESIS /
ABSENT). This is the spine of the feasibility judgment in `FEASIBILITY-RISK-LEDGER.md`.

---

## Stage 1 — Partition (Base-OS vs. Identity Payload)

**Intent.** Drop cerebellum, brainstem, hypothalamus, primary sensory/motor cortex as
"natively regenerated Base-OS"; keep association cortex + hippocampus + amygdala + basal
ganglia (~12–14B neurons) as the "identity payload."

- 1a. Neuron counts are roughly right (cerebellum holds the majority of neurons). **REAL.**
- 1b. Identity is *localized* to the "payload" regions and cleanly *separable* from the
  dropped regions. **HYPOTHESIS.** Identity, skill, and procedural memory are distributed;
  basal ganglia/cerebellar loops participate in personality-relevant habit and affect. A
  clean cut is an assumption, not a finding.
- 1c. The clone's genome regenerates the dropped regions into a *compatible* interface the
  payload can dock onto. **HYPOTHESIS.** Boundary wiring (the "anchors") is individual and
  experience-shaped, not purely genetic.

## Stage 2 — Quantize & compress

**Intent.** Exploit ~99.99995% sparsity; quantize synaptic weights to 4-bit/ternary; CSR
encode → ~300 TB structural or 5–10 TB "functional latent" payload.

- 2a. Cortical connectivity is extremely sparse. **REAL** (order-of-magnitude plausible).
- 2b. Memory tolerates aggressive sparsification. **REAL but conditional** — only when
  *engram-aware* (structured), per `../scans/01`. Uniform ternary crushing is not what the
  biology supports.
- 2c. The identity is captured by a static weighted graph at all. **HYPOTHESIS / likely
  false in part** — dynamics, neuromodulation, glia, and plasticity state are not in the graph.
- 2d. The specific footprints (300 TB / 5–10 TB) are derived, not measured. **[UNVERIFIED]** —
  arithmetic from assumed bit-depths; depends entirely on 2c being true.

## Stage 3 — Cross-brain alignment (the math core)

**Intent.** Align source graph G_S to target clone graph G_T via Gromov-Wasserstein OT +
Riemannian tangent-space alignment; constrain by Peters' rule (write only where axons and
dendrites physically meet within 2–5 µm).

- 3a. GW/FUGW is a valid method for label-free graph/brain alignment. **REAL.**
- 3b. It scales to 10^10 nodes. **ABSENT/INFEASIBLE** — GW is NP-hard, non-convex; current
  brain uses are at parcel scale. Needs an unspecified hierarchical formulation.
- 3c. Peters' rule as a hard constraint makes the target graph writable. **OVERSTATED** —
  Peters' rule (statistical potential connectivity) is contested and is a population
  heuristic, not a per-synapse wiring guarantee.

## Stage 4 — Write compiler

**Intent.** Install aligned weights via holographic STDP (3D SLMs) or closed-loop
sleep-ripple BCI emitting synthetic sharp-wave ripples during slow-wave sleep.

- 4a. Optogenetics can drive precise activity and manipulate *existing* engrams in animals.
  **REAL.**
- 4b. Sharp-wave-ripple-timed stimulation can bias consolidation. **REAL (animal, limited).**
- 4c. These can *write a structured external identity payload* into a differently-wired adult
  human brain. **ABSENT** — no evidence in principle; requires opsin expression, synapse-level
  addressing, and that identity be writable as weights (depends on 2c). This is the single
  least-supported stage.

## Stage 5 — Non-destructive chronic read (Sub-Track 1)

**Intent.** Chronic subdural intracortical mesh (BISC variants) continuously reads spiking +
LFP; sleep-time ripple replay is compiled into a latent state vector incrementally.

- 5a. Chronic high-channel wireless *surface* reads exist (BISC). **REAL.**
- 5b. They read at **single-synapse resolution** across the payload. **ABSENT** — BISC is a
  surface array; synapse-resolution connectomics is destructive vEM (`../scans/04`).
- 5c. Sleep replay can be decoded into a compressed personality/identity vector. **HYPOTHESIS**
  — replay decoding exists for simple trajectories in animals; identity-level compilation does not.

## Stage 6 — Vessel priming (Sub-Track 2, IQ/EQ)

**Intent.** iTBS to DLPFC + acoustic slow-wave boosting (IQ); fMRI/EEG neurofeedback +
tVNS (EQ) to ready the recipient.

- 6a. iTBS induces LTP-like plasticity; closed-loop acoustic stimulation can enhance slow-wave
  activity; tVNS modulates autonomic tone/HRV; neurofeedback can shift connectivity. **REAL,
  individually** — each is a real, modest-effect intervention.
- 6b. These "double slow-wave density," "thicken the uncinate fasciculus," and make a brain
  able to "accept" a transferred identity matrix. **OVERSTATED** — effect sizes are small and
  the "accept a transfer" framing presupposes Stages 3–5, which are absent.

---

## Dependency chain (why the whole fails even though parts pass)

```
Stage1(1b HYP) ─┐
Stage2(2c HYP) ─┼─► Stage3(3b ABSENT) ─► Stage4(4c ABSENT) ─► migration
Stage5(5b ABSENT)┘                         ▲
                                           └─ requires 2c + 5b to even define the payload
```

The pipeline is a **series chain**: it is only as strong as its weakest link, and three links
(3b, 4c, 5b) are *absent*, not merely immature. No amount of strength in Stages 1, 2a, 6
rescues a chain with absent middle links.

## The separable, sound sub-system

Stages **2a/2b (structured sparsification) + the connectome-GNN capability (ref #2)** form a
closed, testable in-silico loop that needs *none* of the absent biological links. That is the
Phase-1 residual promoted in `RECOMMENDATION.md`.
