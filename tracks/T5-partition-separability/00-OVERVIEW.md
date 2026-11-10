# T5 — Overview

## Problem

The blueprint drops cerebellum/brainstem/primary sensory-motor as "Base-OS" and keeps
association cortex + limbic as "identity payload," assuming clean separability
(`../../analysis/ARCHITECTURE-DECOMPOSITION.md §1`, risk B2). That dissociation is asserted,
never measured on a connectome. T5 measures it.

## Approach

1. **Define candidate partitions** on a connectome with function:
   - MICrONS: lower sensory layers (Base-OS-like) vs. higher associative connections.
   - FlyWire: sensory/motor periphery vs. central complex / mushroom body (integrative).
   - C. elegans: sensory/motor neurons vs. interneuron core.
2. **Functional readouts** for each side (stimulus response, locomotion, activity motifs).
3. **Ablation dissociation.** Lesion one side; measure which functions degrade. Compute a
   **separability index**: how cleanly do "Base-OS" lesions spare "payload" functions and
   vice versa, vs. a random-partition null.
4. **Swap test (the migration-relevant one).** Replace the "Base-OS" side with a *different
   individual's* Base-OS (or a regenerated/randomized analogue) and ask whether "payload"
   function is preserved — the in-silico analogue of docking a payload onto a clone's
   native Base-OS.

## Hypotheses

- H1: some partitions are significantly more separable than a random null (there is *structure*
  to separability).
- H2: no partition is *cleanly* separable — "payload" functions still depend on "Base-OS"
  substrate beyond a threshold (the likely corrective to the blueprint).
- H3: swap tolerance decreases sharply with Base-OS divergence (bounds the "dock onto a clone"
  idea).

## Honest scope

Separability on a worm/fly/mouse connectome does not establish a human identity/Base-OS split.
T5 measures a *graph-functional property* and reports it as a bound on the blueprint's
partition premise — most likely a corrective (H2), which is itself a valuable result.
