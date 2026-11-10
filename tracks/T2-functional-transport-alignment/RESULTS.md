# T2 — Results (cross-individual functional transport via Gromov-Wasserstein)

Surrogate-chain core, attacking the blueprint's Stage-3 "align G_S onto G_T via GW, then write"
claim (risk B1). Substrate: real C. elegans connectome A (`data/celegans_real.npz`); "individual
B" = a controlled-divergence **perturbation model** of A (known node permutation = ground-truth
correspondence + tunable edge rewiring). Self-contained entropic GW (`src/gw_align.py`). Requires `.venv`.

> Honest framing: B is a *divergence model* of A, not a second real worm (we have one labeled
> connectome). This lets us score alignment against ground truth and sweep A↔B divergence — the
> right in-silico test of the transport *mathematics*, explicitly not a claim about two organisms.

## V1 — correspondence sanity → **PASS**
`experiments/T2_v1_correspondence.py` → `results/T2_v1.json`

Entropic GW recovers the ground-truth node correspondence well above chance (1/306 = 0.3%):

| rewire frac | GW correspondence accuracy |
|---|---|
| 0.00 | **0.92** |
| 0.05 | 0.88 |
| 0.10 | 0.84 |
| 0.20 | 0.54 |

GW alignment works and degrades gracefully with divergence — a clean standalone alignment result.

## V2 (+V3) — transport-preserves-function → PASS in the ideal limit, **corrective under realism**
`experiments/T2_v2_transport_function.py` → `results/T2_v2.json`

Transport fidelity = FPS of B (transported weights) vs A's intact input→output function.

| rewire | oracle corr. | oracle + feasibility mask | GW corr. |
|---|---|---|---|
| 0.00 | 1.00 | 1.00 | 0.19 |
| 0.05 | 1.00 | **0.33** | 0.26 |
| 0.10 | 1.00 | **0.46** | 0.00 |
| 0.20 | 1.00 | 0.34 | 0.00 |
| 0.40 | 1.00 | 0.34 | 0.00 |

Three layered findings:

1. **Transport math is sound in the ideal limit (V2 PASS).** With the *oracle* correspondence
   and unconstrained writing, fidelity is 1.00 at every divergence — the mechanism works if you
   know the exact mapping and can write any edge.
2. **The feasibility mask is the killer (H3 confirmed).** Require transport to respect B's actual
   wiring (write only edges B physically supports — Peters'-rule) and fidelity **collapses from
   1.00 to ~0.33–0.46 at the first hint of divergence (5% rewire).** Even with a *perfect*
   correspondence, the target connectome's structure — not the alignment — is the binding
   constraint. **You cannot write what the target is not wired to support.**
3. **Real alignment is not good enough either.** With the GW-*estimated* correspondence (92%
   accurate at zero rewire), fidelity is already 0.19 at zero divergence and 0.00 by 10% rewire:
   the ~8% mismatched nodes, landing on hub edges, wreck the transported function. High
   correspondence accuracy ≠ preserved function.

## What this means for the blueprint (Stage-3)
A direct, measured corrective. The "compute W_align and write it" step works **only** in a
double-idealized limit the blueprint silently assumed: (a) a *perfect* correspondence and (b)
*unconstrained* writing. Relaxing *either* to realistic conditions breaks it — imperfect GW
alignment destroys function, and the target's own wiring caps function even under perfect
alignment. Combined with **T5** (no separable payload module to transport in the first place),
the align-and-write pathway is unsupported in-silico on the nearest testable system.

## Honest scope
Worm connectome + a divergence model, reflex-level function, idealized biology. Bounds the
transport *mathematics*; says nothing about human identity transfer (Tier-A A4 remains absent).
GW accuracy and the feasibility ceiling are the trustworthy, substrate-grounded numbers.

## Status & chain
- V1 PASS (alignment works), V2 PASS-in-ideal / corrective-under-realism (load-bearing answered),
  V3 boundary characterized (GW collapses by ~10% rewire; masked-oracle collapses by ~5%).
- **Banked:** entropic GW, perturbation/divergence model, feasibility-masked transport, function test.
- **Feeds T4 (write-compiler):** T2 shows the feasibility mask is the dominant limiter → T4's
  in-silico write must confront that the target wiring, not the rule, is the ceiling.