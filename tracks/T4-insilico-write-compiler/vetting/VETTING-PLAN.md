# T4 — Vetting Plan (go/no-go gates)

## V1 — Local-rule installs *something* gate
- **Test:** on a tiny host net with low divergence, do local rules move output toward a simple
  target function above a no-plasticity control?
- **Pass:** measurable convergence toward target.
- **Fail → major finding:** if local rules install nothing even in the easy case, the write
  idea is incoherent in simulation — report and halt the surrogate chain.

## V2 — Divergence-threshold gate (load-bearing)
- **Test:** sweep host↔target topology divergence; is there a threshold beyond which local
  rules cannot reach the target (vs. the global-optimizer upper bound)?
- **Pass:** identifiable reachable region + impossibility region.
- **This gate's "fail" is still a result:** either a clean threshold (great) or "local rules
  track the global optimizer everywhere" (surprising, also publishable).

## V3 — Structured-teaching gate
- **Test:** does ripple-timed teaching beat unstructured STDP?
- **Pass:** structured > unstructured on reach rate, ≥2 seeds.
- **Inconclusive allowed.**

## Pre-registration
Fix rule definitions, divergence grid, convergence threshold, and the global-optimizer
baseline before V2. Local-only constraint is inviolable (no backprop-to-target).
