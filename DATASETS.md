# Datasets — public, accessible, and M4-Pro-runnable

Hardware target: **Apple M4 Pro laptop** (unified memory, ~24–64 GB class). PyTorch with the
**MPS** backend for GNN/tensor work; some ops fall back to CPU. No CUDA, no multi-GPU, no
large spiking whole-brain training. The plan is scoped to what fits this envelope.

Each dataset is tagged with whether it fits in RAM, and which tracks use it.

## Tier 1 — the full-pipeline sandbox (fits trivially)

### C. elegans connectome + neural activity
- **What:** entire 302-neuron nervous system (~7K synapses) as a graph, plus homogenized
  whole-brain calcium activity across ~900 worms / ~250 labeled neurons.
- **Access:** homogenized activity+connectivity, [arXiv 2411.12091](https://arxiv.org/html/2411.12091v4);
  [OpenWorm Connectome Toolbox](https://openworm.org/ConnectomeToolbox/) and
  `WormNeuroAtlas` (pip-installable Python; integrates connectome + signal-propagation atlas
  + synapse-sign predictions).
- **Footprint:** megabytes. Fits in RAM many times over.
- **Why it matters:** the **only** substrate where the *entire* blueprint pipeline
  (read → compress → align across individuals → simulate a write) can be run in-silico,
  end to end, on a laptop. It is the backbone of T2, T4, T5 and a fast sanity harness for T1.
- **Caveat:** it is a nematode; "identity" has no meaning here. Treat as a *mechanism* testbed.

## Tier 2 — the insect embodied substrate (fits; sub-circuits for heavy sims)

### FlyWire adult Drosophila connectome
- **What:** ~139K proofread neurons, ~50M synapses, full wiring diagram + neuron types.
- **Access:** [FlyWire](https://flywire.ai/) (CAVEclient / downloadable edge lists);
  flyGNN (NeurIPS 2025) + NeuroMechFly v2 (MuJoCo) provide an embodied loop; a Loihi-2
  neuromorphic port exists for reference ([arXiv 2508.16792](https://arxiv.org/html/2508.16792v1)).
- **Footprint:** the **graph** (CSR edge list + types) is a few GB — fits on M4. A full
  spiking whole-brain sim does **not** fit comfortably; use the **GNN message-passing form**
  or **named sub-circuits** (e.g. central complex for locomotion, mushroom body for
  learning) for anything requiring training.
- **Used by:** T1 (primary behavioral-fidelity substrate via sub-circuits), T5.

## Tier 3 — the mammalian cortical proxy (subset only)

### MICrONS mouse visual cortex (functional connectomics)
- **What:** ~200K cells / ~75K neurons with in-vivo two-photon calcium traces + ~523M
  synapses over ~1 mm³ of mouse visual cortex, structure and function co-registered.
- **Access:** [MICrONS Explorer](https://www.microns-explorer.org/) + `CAVEclient` +
  `microns-explorer` tutorials; *Nature* 2025
  [s41586-025-08790-w](https://www.nature.com/articles/s41586-025-08790-w).
- **Footprint:** the **full** release is ~1.6 PB (EM imagery) — **do not** attempt. The
  **synapse graph + functional calcium traces** subset is queryable in manageable chunks via
  CAVEclient; a single cortical **column / layer-2-3 patch** (hundreds–few-thousand neurons
  with traces) fits on M4.
- **Why it matters:** the closest public analogue to the blueprint's "association cortex" —
  it has **both** structure and recorded function, so it is where structured compression (T1)
  and cross-region separability (T5) can be tested on *mammalian cortex with a functional
  readout*, not just behavior.
- **Used by:** T1 (mammalian generalization), T3 (sequence/trace compression), T5.

## Tier 4 — hippocampal replay / sequence activity (public recordings)

- **What:** published hippocampal place-cell + sharp-wave-ripple recordings used for replay
  decoding. Several labs release spike + LFP data (e.g. via CRCNS / DANDI).
- **Access:** CRCNS hc-* datasets and DANDI Neurodata Without Borders archives (free
  registration); replay-decoding methods references
  [PMC5102323](https://pmc.ncbi.nlm.nih.gov/articles/PMC5102323/),
  [PMC8476125](https://pmc.ncbi.nlm.nih.gov/articles/PMC8476125/).
- **Footprint:** single-session spike/LFP files are hundreds of MB to a few GB — fits.
- **Used by:** T3 (replay→latent compression-fidelity).
- **Caveat:** access/licensing varies per dataset; confirm terms before use. Mark any
  dataset not yet downloaded as **[access-to-confirm]** in the track.

## Out of scope for the M4 (external validation only)

- **Human synaptic-resolution in-vivo reads:** do not exist (see `analysis/`); no dataset.
- **Organoid / MEA wet-lab closed-loop:** UCSC *Cell Reports* 2026; DishBrain / Cortical Labs
  CL1. These are physical experiments, not laptop-runnable. If any processed MEA time-series
  are released, they can seed T4's *simulated* write-compiler as a realism check, but the
  wet-lab loop itself is explicitly out of scope.

## Summary: what the M4 can actually do

| Capability | Feasible on M4? | Substrate |
|---|---|---|
| Load a full connectome as a graph | Yes | C. elegans, FlyWire, MICrONS-subset |
| Train a connectome-GNN to a behavioral/functional readout | Yes (small/sub-circuit) | C. elegans whole; FlyWire sub-circuits; MICrONS column |
| Prune + quantize + distil that model | Yes | all three |
| Hierarchical GW align two individuals' connectomes | Yes (worm full; fly/mouse coarsened) | C. elegans primary |
| Simulate an STDP/ripple write into a target net | Yes | C. elegans; small recurrent nets |
| Replay→latent compression | Yes | hippocampal single-session |
| Full spiking whole-brain sim / training | **No** | — (use GNN form or sub-circuits) |
