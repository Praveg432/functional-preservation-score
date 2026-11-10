# Surrogate-Chain Synthesis — T5 → T2 → T4

The surrogate chain is the project's honest attack on the blueprint's three *blocked* biological
stages (partition, align, write). Each link is an in-silico test of whether the stage is even
*coherent in simulation* on the nearest testable substrate. Read together, they form a single,
layered, measured corrective to the blueprint's core "partition → align → write" pathway.

## The chain and what each link found

| Stage | Blueprint claim | Surrogate link | Measured result |
|---|---|---|---|
| 1. Partition | Identity is a clean, separable "payload" module, swappable onto a regenerated Base-OS | **T5** | **No separable module.** On the real C. elegans connectome the asserted payload is no more functionally privileged than a random interneuron subset (z≈+1, beats ~70% of nulls). Function is distributed. |
| 3. Align+transport | Compute W_align (GW) and transport the payload onto the target | **T2** | **Transport breaks under realism.** GW recovers 92% correspondence, and oracle+unconstrained transport is perfect — but requiring the target's real wiring (feasibility mask) collapses fidelity to ~0.33 at 5% divergence, and real GW correspondence gives ~0. |
| 4. Write | Install the aligned weights via ripple-timed local plasticity | **T4** | **Mechanism insufficient.** A global optimizer installs the function (ceiling ~1.0) but biologically-plausible local plasticity reaches only 0.2–0.4 (gap ~0.5–0.67); ripple-timing does not help. |

## The composed story

The three links fail for *different, independent, and compounding* reasons — which is what makes
the corrective strong rather than a single fragile point:

1. **There is nothing clean to extract (T5).** The "identity payload" is not a separable module;
   function is distributed across the interneuron pool. The very first premise is unsupported.
2. **Even if you extract the whole graph, you cannot place it (T2).** Transport works only in a
   double-idealized limit (perfect correspondence AND unconstrained writing). Real alignment
   error destroys function, and the target's own wiring caps it — *you cannot write what the
   target is not wired to support.*
3. **Even where the target can host the function, the proposed write mechanism cannot reach it
   (T4).** A non-biological optimizer succeeds, but broadcast-signal local plasticity (the
   blueprint's ripple-timed mechanism) falls far short.

A single feasibility constraint — **the target substrate's own wiring** — recurs as the binding
limit across T2 (feasibility mask) and T4 (global ceiling falls with divergence). The blueprint
silently assumed this away at every stage.

## What this is, and is not

- **Is:** a measured, reproducible, in-silico demonstration that the blueprint's partition →
  align → write pathway is unsupported on the nearest testable biological system, with the
  specific failure mode isolated at each stage. A genuine contribution: it tells the field *where*
  and *why* the idea breaks, not just that it is hard.
- **Is not:** a claim about human brains. All three links use a 306-neuron nematode connectome (or
  toy nets), reflex-scale functions, and idealized biology. Tier-A (non-destructive synaptic read,
  identity-scale write, cross-subject transfer) remains absent — the surrogates test *coherence in
  simulation*, not biological feasibility.
- **Caveat honestly carried:** richer plasticity rules (T4) or finer alignment (T2) might shift
  the exact numbers; the *qualitative* chain (distributed function → feasibility-capped transport
  → mechanism-insufficient write) is the robust result, and each is logged with its limits.

## Where this leaves the program

Combined with the two positive tracks, the project now holds:
- **T1** — a real compression phenomenon (low-bit quantization floor on connectomes).
- **T3** — replay sequences are highly compressible yet event-identifiable (compressed-backup is
  information-theoretically plausible), with a bounded-store capacity limit.
- **T5+T2+T4** — a layered corrective: the blueprint's migration pathway fails in-silico at every
  stage, each for an independent reason, with the target's own wiring as the recurring limit.

That is the honest shape of the contribution: **compression of neural data is real and
characterizable; migration of function across substrates is not supported by the proposed
pathway** — and we can say precisely why.
