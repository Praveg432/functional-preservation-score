# T1-V4 dynamics-robustness — reading the result

Result file: `T1_v4_real.json`. Diagnostic: `scripts/diagnose_sigmoid.py`.

## What was tested
Does the Effect-B regime boundary (uniform wins at low sparsity; engram:strength wins at high
sparsity), measured at int8 with the leaky-rate tanh model, survive an **independent dynamics
model**? If FPS-scored results flip with the model, they are not trustworthy.

## What happened (two iterations, logged for honesty)
1. First sigmoid model was **degenerate** — divisive normalization + gain-4 sigmoid saturated
   near 1, across-stimulus signal variance ~2e-6, so every FPS was 0. Not a refutation; a broken
   model. Fixed (center at 0.5, gain 1.5, deviation-based recurrence).
2. Fixed sigmoid model: **Effect B does NOT survive.** Under sigmoid-conductance, uniform wins
   at nearly every sparsity (margins -0.37 to -0.60); engram only edges ahead marginally at one
   point. The leaky-rate boundary is not reproduced.

## Honest conclusion
- **Effect A (quantization sparsity floor): ROBUST.** It depends on the weight distribution and
  bit-depth, not on dynamics; unaffected by this test. Remains the strong, publishable result.
- **Effect B (engram > uniform at high sparsity): DYNAMICS-DEPENDENT — NOT a safe claim.** It
  holds under leaky-rate tanh but not under sigmoid-conductance. Cannot be reported as a general
  finding without resolving the dynamics dependence.

## Caveat on the sigmoid model
Its between-stimulus signal variance is small (~4e-6 vs 0.5 for leaky-rate), i.e. it is weakly
expressive, which inflates absolute FPS (easy to "preserve" a near-constant function). So this
single counter-model is enough to BLOCK the strong Effect-B claim, but not enough to firmly
establish the opposite. The correct status is **Effect B is unproven / model-sensitive**, pending
a readout that is (a) expressive and (b) biologically grounded — real functional activity
(Randi 2023) is the right next instrument, not another hand-built toy model.

## Impact on the program
- The FPS metric and the floor result (Effect A) stand.
- Any "connectome compression operation" asset must report results **per dynamics model** and
  must not advertise the matched-conditions advantage as universal.
- T1 is NOT yet paper-grade on Effect B. It IS a solid result on Effect A.
