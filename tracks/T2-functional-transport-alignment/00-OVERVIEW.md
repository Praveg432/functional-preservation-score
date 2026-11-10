# T2 — Overview

## Problem

The blueprint maps source identity graph G_S onto a differently-wired target G_T via
Gromov-Wasserstein OT. The vetting (`../../scans/05-optogenetics-and-ot-alignment.md`) found
GW is real but NP-hard and demonstrated only at parcel scale, and — critically — **nobody
tests whether the alignment preserves function when you actually transport a circuit.**

## Approach

1. **Correspondence.** Compute a hierarchical / entropic GW (or FUGW) node-correspondence
   `T` between individual A's connectome and individual B's. Use coarsening (S-GWL/HOT style)
   to fit the M4 budget. For C. elegans, labeled neurons give a **ground-truth matching** to
   score `T` against (precision/recall of recovered correspondences).
2. **Transport.** Push A's functional weights onto B's graph: `W_B ← transport(W_A, T)`,
   respecting a Peters'-rule-style feasibility mask (only map onto edges that exist in B).
3. **Function test (the novel step).** Run B's network with the transported weights on the
   same inputs A was driven with. Measure how much of A's input→output behavior B reproduces.
4. **Failure map.** Characterize *where* transport fails: as a function of A↔B structural
   divergence, correspondence confidence, and the feasibility-mask overlap. This is the
   realistic, in-silico answer to "how alignable are two individuals, functionally?"

## Hypotheses

- H1: GW correspondence on C. elegans recovers the ground-truth matching well above chance.
- H2: functional transport degrades gracefully with structural divergence up to a boundary,
  then collapses — and the boundary is measurable.
- H3: the feasibility mask (edges must exist in B) is the dominant limiter, not the
  correspondence quality — i.e. you cannot write what the target is not wired to support.

## Honest scope

Even full success means "weights transported between two *worm* connectomes preserve a
*reflex-level* function." It does **not** imply human identity transfer (Tier-A A4 remains
absent). T2 tests the *mathematics of transport*, with biology held fixed and idealized.
