# Novelty Scan — what is already solved vs. what is open

Scan date: 2026-11-07. Purpose: ensure every proposed track attacks an **open** question,
not a solved one. Each track below cites the nearest prior art it must differentiate from.

## Already solved (prior art to cite + differentiate, NOT to re-claim)

| Area | Representative prior art | What it already does |
|---|---|---|
| GNN pruning + quantization (generic) | [arXiv 2510.22058](https://arxiv.org/abs/2510.22058) (Oct 2025); BitNet-1.58 for GNN/MLP [2411.05882](https://arxiv.org/html/2411.05882v1); ternary NN [1705.01462](https://arxiv.org/pdf/1705.01462.pdf) | 50% unstructured pruning + 3 quant methods keep GNN accuracy on standard graph tasks. |
| Behavioral-similarity of compressed nets | SimCert [2603.14818](https://arxiv.org/pdf/2603.14818v1) | Probabilistic certification of behavioral similarity for compressed **standard** DNNs. |
| Scalable Gromov-Wasserstein | S-GWL [1905.07645](https://arxiv.org/html/1905.07645v1); Hierarchical MM-OT "HOT" [2310.04470](https://arxiv.org/html/2310.04470v1); multi-scale hypergraph GW [2608.29635](https://arxiv.org/html/2608.29635) | GW node-correspondence + graph matching at scale via coarsening/hierarchy. |
| Brain alignment via OT | FUGW, Thual et al. [2206.09398](https://arxiv.org/pdf/2206.09398) | Aligns individual brains at **functional-parcel** scale. |
| Lottery ticket | Frankle & Carbin [1803.03635](https://arxiv.org/pdf/1803.03635v2); GW "expressive tickets" [2506.03919](https://arxiv.org/html/2506.03919) | Sparse subnetworks match dense performance when re-trained from init. |
| Hippocampal replay-content decoding | rapid replay classification [PMC5102323](https://pmc.ncbi.nlm.nih.gov/articles/PMC5102323/); real-world-speed replay [PMC8476125](https://pmc.ncbi.nlm.nih.gov/articles/PMC8476125/) | Decode the *trajectory/position* a replay event represents, in real time. |
| Cross-arch distillation (ANN↔SNN) | CKD [2507.09269](https://arxiv.org/html/2507.09269); [2511.06902](https://arxiv.org/html/2511.06902v1); reverse-KD structure learning [2304.09500](https://arxiv.org/html/2304.09500v1) | Distil knowledge across differing architectures/modalities; prune during KD. |
| Connectome ML | flyGNN (NeurIPS 2025); FlyWire latent steering [2505.13011](https://arxiv.org/html/2505.13011v2); connectome-constrained vision stress-test [2610.13018](https://arxiv.org/html/2610.13018v1) | Load a connectome as a model; derive/steer latent organization; test mechanistic claims. |
| Organoid goal-directed learning | UCSC, *Cell Reports* 2026 ([biorxiv 2024.12.07.627350](https://www.biorxiv.org/content/10.1101/2024.12.07.627350v1)); DishBrain | Feedback-driven plasticity makes cultured neurons learn a task. **Wet-lab only.** |

## Open / defensible (each becomes a track)

| ID | Open question | Why it is still open | Track |
|---|---|---|---|
| **N1** | On a **connectome-GNN in an embodied/functional loop**, how far can *structured, engram-aware* sparsification + low-bit quantization go before **behavior** (not accuracy) breaks — and does biologically-motivated structure beat uniform? | Prior GNN compression uses standard graph tasks + accuracy, never a connectome driving behavior, and never the engram-aware structure axis. SimCert certifies standard DNNs, not embodied connectome behavior. | **T1** |
| **N2** | Does cross-individual connectome **node-correspondence (hierarchical GW)** preserve *function* — i.e. if you transport circuit weights from brain A onto brain B's wiring via the alignment, does B reproduce A's input→output behavior? | Alignment work measures matching accuracy / distance, never *functional transport* of a transported circuit on real connectomes. | **T2** |
| **N3** | What is the **compression-fidelity frontier** for turning a replayed neural *sequence* into a low-bit latent that still reconstructs the sequence (the "incremental backup" proxy)? | Replay work decodes *position*, not minimal-bit reconstructable latents of the sequence itself. | **T3** |
| **N4** | Can an **in-silico write-compiler** install a target circuit's function into a *differently-wired* model network using only biologically-plausible local rules (STDP / ripple-timed plasticity), and where does it fail? | The biological write is absent (Tier-A). The *simulation* of whether local plasticity can even in principle install transported weights is untested and is a legitimate theory/sim question. | **T4** |
| **N5** | Is the blueprint's **"Base-OS vs. identity payload" partition** empirically separable in a connectome — can you ablate "Base-OS-like" regions and preserve a defined "identity-like" function, measured, not assumed? | The partition is asserted, never tested on a connectome with a functional readout. | **T5** |

**Honesty rule for all five.** N1–N3 are genuinely buildable capability/boundary results.
N4–N5 are **surrogate** studies: they test whether the blocked biological steps are even
*coherent in simulation*, and each explicitly states what the proxy does **not** show about
the real biological system. No track claims progress toward human migration.
