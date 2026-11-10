# Scan 05 — Optogenetic Engram Tooling + Gromov-Wasserstein Alignment

Two claims are grouped here: the "write" enabler (optogenetics) and the cross-brain
alignment math (optimal transport).

## 5a. Optogenetic engram implantation / 2026 Nobel

**Blueprint claim.** "2026 Nobel-recognized optogenetic tooling" provides precise
light-driven engram writing into living neural tissue.

**Verdict: Nobel REAL; "engram-implantation tooling" framing OVERSTATED.**

- The **2026 Nobel Prize in Physiology or Medicine** went to **Karl Deisseroth, Peter
  Hegemann, and Georg Nagel** for the discoveries underpinning **optogenetics** (including
  channelrhodopsin), which lets researchers switch neurons on/off with light at
  millisecond precision.
  [Nobel press release](https://www.nobelprize.org/prizes/medicine/2026/press-release/) ·
  [Nobel popular info](https://www.nobelprize.org/prizes/medicine/2026/popular-information/)
- Optogenetics **has** been used in rodents to activate, label, and even artificially
  associate engram cells (classic Tonegawa-lab line of work), and closed-loop variants have
  been used for memory-related manipulation.
  [The Transmitter](https://www.thetransmitter.org/optogenetics/how-nobel-prize-winning-optogenetics-has-revolutionized-neuroscience/)
- **Over-reach:** the prize is for optogenetics *broadly*, not for "engram-implantation
  tooling," and existing engram work is (i) in animals, (ii) requires genetic modification to
  express opsins, and (iii) *re-activates or tags* existing engrams — it does **not** write a
  novel, structured identity payload from an external source into an adult human brain.

## 5b. Gromov-Wasserstein cross-brain alignment

**Blueprint claim.** Gromov-Wasserstein OT + Riemannian tangent-space alignment compute the
transform that maps the source identity graph onto a differently-wired target clone graph.

**Verdict: REAL and apt as a method; feasibility at connectome scale OMITTED.**

- GW/Fused-GW is a legitimate, well-studied tool for **graph matching** and **node
  correspondence** without a shared coordinate system (Xu et al.,
  [arXiv 1901.06003](https://arxiv.org/html/1901.06003v2)); it is used for **cross-domain
  alignment** ([arXiv 2006.14744](https://arxiv.org/html/2006.14744v3)).
- It is used specifically to **align individual brains** — Fused Unbalanced GW aligns
  cortical functional data across subjects (Thual et al.,
  [arXiv 2206.09398](https://arxiv.org/pdf/2206.09398)).
- **Omitted obstacle:** GW distance is **NP-hard**, the optimization is **non-convex**, and
  exact computation suffers the curse of dimensionality; scalability to large graphs is an
  open research problem ([arXiv 2312.07397](https://arxiv.org/html/2312.07397v1),
  [arXiv 2506.12025](https://arxiv.org/html/2506.12025)). Current brain-alignment uses are at
  the level of **thousands of functional parcels**, not **1.4×10^10 nodes**. Applying GW
  directly at connectome scale, as written, is computationally infeasible with known methods —
  a hierarchical/coarsened formulation would be mandatory and is not specified.

## Bearing on the blueprint

- **Supports:** both tools are real and individually credible for small-scale analogues
  (optogenetic engram manipulation in animals; GW alignment of functional brain data).
- **Breaks / unproven:** composing them into "compute W_align over the full identity graph and
  optically write it into a living clone" is unproven in principle and infeasible at the
  stated scale. These are the two stages carrying the most risk — see the ledger.

*Content rephrased from sources for licensing compliance.*
