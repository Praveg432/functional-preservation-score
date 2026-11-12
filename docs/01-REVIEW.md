# Review of the paper and its findings

A self-review of the live preprint, written in the style of a careful referee: what is claimed,
what the evidence actually supports, strengths, weaknesses, and threats to validity. All numbers
are quoted from the committed statistical artifacts (`tracks/*/results/*_stats.json`), not from
memory.

**Paper:** *A Functional Preservation Score for Auditing Connectome Operations: Compression,
Alignment, Transport, and Local-Rule Writing.*
**Preprint:** arXiv:2611.13681 — https://doi.org/10.48550/arXiv.2611.13681

---

## 1. What the paper claims

A single measurement tool (the Functional Preservation Score, FPS) is used to audit the
computational operations behind speculative "mind-migration" pipelines. The headline is a split:
**compression of neural data is measurable and bounded; migration of function across substrates
is not supported by the proposed partition→align→write pipeline.** Five pre-registered studies
support this, on the *C. elegans* connectome, Kato-2015 whole-brain calcium, and DANDI-000044
hippocampal replay.

## 2. Claims vs. evidence (as committed)

| Claim | Evidence (artifact) | Assessment |
|---|---|---|
| Uniform low-bit quantisation has a sparsity floor | int4 floor 0.73, ternary 0.98 (uniform) vs 0.27, 0.32 (engram); `T1_v3_stats.json` | **Strong.** Deterministic weight-distribution property, not a statistical estimate. |
| Structured compression beats uniform at matched int4 | engram FPS 0.30 [0.12,0.48] vs uniform 0.03 [0,0.09]; p=0.015, d=1.3 (target 0.5) | **Supported but regime-limited** (paper states it does not reproduce under a 2nd dynamics model; claim is scoped accordingly). |
| Replay sequences compress ~10^3x yet stay identifiable | CV top-1 0.69 [0.63,0.74] vs chance 0.125, p=1e-4; `T3_v2_stats.json` | **Strong.** 30-split CV, permutation p, non-overlapping CIs along the frontier. |
| No separable "identity payload" | payload-ablation not significantly > random-interneuron null (p=0.17/0.16/0.27/0.37); `T5_v2_stats.json` | **Strong as a negative.** 500-sample null; fails to reach significance at every size. |
| Transport collapses under realism | oracle 1.00 → masked 0.40 [0.31,0.49] (p=3e-4) → GW 0.06 [0,0.13] (p=2e-4); `T2_v2_stats.json` | **Strong.** 8 seeds, permutation tests. |
| Local-rule write cannot reach the achievable function | gap 0.45 [0.27,0.64], p=1e-4, d=2.0; ripple Δ CI∋0; `T4_v2_stats.json` | **Strong.** 10 seeds; ripple-null confirmed. |

## 3. Strengths
- **Measurement-first design.** A single, null-normalised metric (FPS) makes otherwise
  incomparable operations comparable, and the trivial-baseline null blocks the most common
  inflation artifact.
- **Statistical hygiene.** Bootstrap CIs, permutation p-values, effect sizes, pre-registered
  primary policies (no max-over-variants), and repeated CV. The negatives are backed by explicit
  null distributions, not just low point estimates.
- **Reproducibility.** Deterministic, laptop-scale, every claim mapped to a committed artifact
  and the script that produced it; a documented record of five methodological corrections.
- **Honest scope.** Positive and negative results are each stated at their true strength, and the
  biological out-of-scope boundary is stated repeatedly.

## 4. Weaknesses / threats to validity (and how the paper handles them)
- **Scale.** 306-neuron connectome, ≤135-neuron activity, 40-neuron write-nets; reflex/trajectory
  functions. Generalisation to mammalian cortex is untested. *Handled:* stated as a primary
  limitation; conclusions rest on effect direction + significance, not magnitudes.
- **Simple dynamics.** Leaky-rate models. The T1 structured-advantage result already showed
  dynamics-sensitivity, which the paper used to *drop* the universal version of that claim —
  evidence the authors took this threat seriously. *Residual risk:* the floor and the three
  negatives could in principle shift under richer biophysics; the paper argues the qualitative
  pipeline-level conclusion is robust because the binding constraint (target wiring) is structural.
- **Small test sets.** T3 uses ~26 laps / 30 CV splits; T2/T4 use 8–10 seeds. *Handled:* CIs are
  wide and reported; frontiers given as regions.
- **Perturbation-model "individual B" (T2).** B is a controlled divergence of one real
  connectome, not a second organism. *Handled:* flagged explicitly; this bounds the *mathematics*
  of transport, not cross-organism biology.
- **FPS is functional, not phenomenal.** It measures input→output preservation, not subjective
  continuity. *Handled:* stated.

## 5. Where a skeptical reader should push
- Replicate the floor and the three negatives on a mammalian connectome subset (MICrONS) and
  under a spiking/biophysical model — the most valuable follow-up.
- Stress the FPS null on adversarial "looks-right" outputs beyond the shuffle/mean baselines.
- For T4, test richer local-plasticity rules (eligibility traces, three-factor variants with
  structured credit) to see whether the plausibility gap narrows — the paper flags this as open.

## 6. Overall
A methodologically careful paper whose contribution is a measurement framework plus a clear,
evidence-backed map of where a speculative pipeline does and does not hold. The positive results
(compression floor, replay compressibility) and the negatives (no separable module, transport
collapse, write gap) are each appropriately scoped and statistically supported at the stated
scale. The main caveat is scale/dynamics generalisation, which the paper states plainly rather
than obscures.
