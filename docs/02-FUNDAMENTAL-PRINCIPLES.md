# Fundamental principles

The concepts needed to read the paper in depth, each explained from first principles and tied to
where it appears in the work. Companion to `01-REVIEW.md` and `03-DATA-PRIMER.md`.

---

## 1. The reframing: from "mind migration" to a measurable fidelity problem
The speculative goal — read a brain, compress it, install it elsewhere — is unfalsifiable as
stated. The paper's move is to ask a single operational question for every stage: *how much of a
neural system's input→output function survives this operation?* That converts an argument into a
measurement with a gradient, which is what makes the rest of the work possible.

## 2. Function, not weights
A neural system is treated as a map from a fixed battery of input stimuli to outputs (e.g. motor
readout). "Preservation" is judged on **behaviour over that battery**, never on how similar the
weights look. Two networks with very different weights can compute the same function; two with
similar weights can diverge. Scoring on function is what keeps the conclusions meaningful.

## 3. Functional Preservation Score (FPS)
For reference outputs `Y_ref` and transformed outputs `Y`, an R²-style agreement
`raw(Y) = 1 − ||Y − Y_ref||² / ||Y_ref − mean(Y_ref)||²` is normalised by the **best trivial
baseline** `Y_null` (the larger of a shuffled stimulus→response mapping and a predict-the-mean
predictor):

```
FPS = clip( (raw(Y) − raw(Y_null)) / (1 − raw(Y_null)), 0, 1 )
```

- **FPS = 1:** reproduces the reference function. **FPS = 0:** no better than the best trivial control.
- **Why the null matters:** a system that outputs a constant or an input-independent "typical"
  response can look good under a bare error measure. Normalising by the best trivial baseline
  removes that free lunch. The paper discovered this empirically (a constant output beat a
  shuffle-only null) and hardened the metric — see `docs/04-FINDINGS-WALKTHROUGH.md` §episodes.
- **Identification accuracy** (used for replay): instead of regressing outputs, ask whether a
  reconstruction is nearest to its *own* original among all events. Bounded, chance = 1/n, and
  immune to the "everything looks like a generic pattern" artifact.

## 4. Connectomes and connectome-driven dynamics
A **connectome** is a weighted directed graph of neurons and synapses. The paper runs the graph
as a **leaky-rate recurrent model**: `x[t+1] = (1−leak)·x[t] + leak·tanh(W·x[t] + W_in·u[t])`,
reading out motor neurons. Key point echoing the connectomics literature: **topology alone does
not fix function** — the dynamics depend on weights/signs/time-constants, so a connectome is a
scaffold whose functional behaviour must be instantiated by a model.

## 5. The three operations under audit
1. **Compression** — reduce the graph's information: *pruning* (remove edges) and *quantisation*
   (few-bit weights, down to ternary {−1,0,+1}). Compared *uniform* (magnitude) vs *engram-aware*
   (protect hub neurons), at **matched total effective sparsity** so the comparison is fair.
2. **Alignment + transport** — map one individual's graph onto another's differently-wired graph
   (a correspondence), then push weights through it. Correspondence via **Gromov–Wasserstein**;
   writing is constrained by a **feasibility mask** (you can only write edges the target has).
3. **Writing** — install a target function into a fixed foreign topology using only **local
   plasticity** (reward-/ripple-gated Hebbian), compared to a **global optimiser** upper bound.

## 6. Gromov–Wasserstein (GW) optimal transport, briefly
Two connectomes have no shared neuron labels, so aligning them is a structure-matching problem.
GW finds a soft correspondence that best preserves *intra-graph* relationships (it matches the
geometry of connectivity, not absolute positions). It is powerful but NP-hard and non-convex; the
paper uses an entropic (Sinkhorn-regularised) solver. Crucially, the paper tests not just
*matching accuracy* but whether a *transported circuit keeps its function* — the step the prior
literature skips.

## 7. The feasibility mask (Peters' rule) — the recurring limit
You cannot write a connection the target substrate is not wired to support. Formally, transport
is restricted to edges present in the target graph. This single constraint is what breaks both
transport (T2) and writing (T4): it is the paper's central structural finding — *the target
substrate's own wiring is the binding limit*.

## 8. Local vs global learning (the plausibility gap)
A **global optimiser** (e.g. least squares over all weights) is non-biological but establishes
what the fixed topology *can* represent — an upper bound. **Local plasticity** uses only
pre/post-synaptic activity and a broadcast reward/ripple signal (biologically plausible). The gap
between them quantifies the cost of biological plausibility. A large gap means the function is
achievable in principle but not by the proposed mechanism.

## 9. Statistical principles used
- **Bootstrap 95% CIs** on every headline estimate (10⁴ resamples).
- **One-sided permutation tests** for comparisons (10⁴ permutations, add-one-corrected p).
- **Explicit null distributions** (shuffle/mean for FPS; label-permutation for identification;
  500 random subsets for separability).
- **Cohen's d** effect sizes; **pre-registered primary policies** (no max-over-variants);
  **repeated cross-validation** with train-only fitting (no leakage).

## 10. Scope discipline (read this before over-interpreting)
Everything is at nematode / small-network scale with reflex-level functions. The studies test
**coherence in simulation**, not biological feasibility. The pipeline's absent prerequisites —
non-destructive synaptic-resolution reading, identity-scale writing, cross-subject transfer —
have no evidence at any scale and are not claimed. FPS measures function, not subjective
experience or personal identity.
