# T1 — Results

All numbers map to committed JSONs in `results/` and the script that produced them. Substrate:
C. elegans connectome (deterministic synthetic fallback, `n=300`, seeds 0/1/2). Metric: FPS
(`shared/fps.py`). Pre-registration: `PRE-REGISTRATION.md`.

## V1 — baseline-reality gate → **PASS**
`experiments/T1_v1_baseline.py` → `results/T1_v1.json`

- Reference model FPS vs. itself: **1.00** (all seeds).
- Degree/weight-shuffled graph control: **0.00** (all seeds).
- Conclusion: the connectome carries function a random graph does not, and FPS discriminates
  it perfectly. The object T1 compresses is real.

## V2 — structure-advantage gate (synthetic) → **PASS (3/3 seeds)**
`experiments/T1_v2_structure_advantage.py` → `results/T1_v2.json`
Operating point: 50% prune + int4, matched pruning budget.

| mean | Uniform FPS | Engram-aware FPS | Margin |
|---|---|---|---|
| synthetic | 0.31 | 0.79 | +0.49 |

Pre-registered pass met on 3/3 seeds on the synthetic substrate.

## V2 — structure-advantage gate (REAL connectome) → pre-registered threshold **NOT met**, advantage holds
`experiments/T1_v2_structure_advantage.py --real` → `results/T1_v2_real.json`

Validating on the real White-1986 somatic connectome (306 neurons, 3158 edges) exposed two
things the synthetic data hid — this is exactly why we validated before proceeding:

1. **A quantization confound.** The real connectome has heavy-tailed *integer* synapse-count
   weights (35% of edges are weight 1, max 37). int4 quantization (15 levels, step ~2.5) zeroes
   all weight-1/2 edges, so "50% prune + int4" produces ~**73% total effective sparsity** for
   the uniform path — the comparison at matched *pruning* budget was not matched in *total*
   compression. (A separate pruning tie-handling bug was also found and fixed; see RESEARCH-LOG.)
2. On the real graph, engram-aware mean FPS (~0.32) is **well below** the synthetic 0.79, so the
   pre-registered absolute threshold (engram FPS ≥ 0.5) does **not** cleanly hold at this point.

The *relative* advantage (engram > uniform) still holds, but a single confounded point is not a
clean test. We therefore ran the unconfounded V2b.

## V2b — matched TOTAL effective sparsity (the rigorous test) → **engram advantage CONFIRMED on real data**
`experiments/T1_v2b_matched_effective.py --real` → `results/T1_v2b_real.json`

Both policies driven to the *same* total effective sparsity (measured after prune+quant), swept
over targets 0.5–0.8, FPS averaged over 3 stimulus batteries.

| Target eff. sparsity | Uniform FPS | Engram-aware FPS | Margin |
|---|---|---|---|
| 0.50 | 0.08 | 0.32 | +0.24 |
| 0.60 | 0.08 | 0.35 | +0.27 |
| 0.70 | 0.08 | 0.35 | +0.27 |
| 0.80 | 0.00 | 0.14 | +0.14 |
| **mean margin** | | | **+0.23** |

- **Engram-aware beats uniform across the entire curve** on the real connectome (mean margin
  +0.23); synthetic contrast gives +0.27 — the effect is substrate-robust, not an artifact of
  the engineered synthetic graph.
- **New real-data finding the synthetic data could not show:** int4 imposes a hard effective-
  sparsity **floor (~0.73)** on the real connectome — uniform int4 *cannot* operate below it,
  because the heavy-tailed integer weights collapse. Engram-aware mixed-precision escapes the
  floor by keeping hub edges at higher precision. This is a sharper, more publishable result
  than the original synthetic single-point claim.

## Honest verdict

- **Confirmed and validated on real data:** structured, engram-aware compression preserves
  connectome function better than uniform at matched effective compression (H1 supported on the
  REAL C. elegans somatic connectome, not just synthetic).
- **Corrected:** the original "50% + int4" operating point was confounded by quantization-
  induced sparsity; the clean comparison is at matched *total effective* sparsity (V2b).
- **Tempered:** absolute preservation on the real graph is modest (FPS ~0.3), lower than
  synthetic. The win is relative + the newly-found int4 floor, not a high-fidelity reconstruction.
- Validates the **method + FPS metric** on real data. No claim about biological mind migration.

## V3 — breakdown map (bit-depth × effective-sparsity × structure) on REAL data
`experiments/T1_v3_breakdown_map.py --real` → `results/T1_v3_real.json`

> **Framing correction (2026-11-07 critical review).** The first pass reported a single
> "mean engram advantage by bit-depth" (0.04 / 0.25 / 0.29) and called it "advantage grows as
> bits shrink." A review of the raw surface (`scripts/review_v3.py`) showed that number
> **conflated two distinct effects** and was misleading. The corrected decomposition is below.
> This is the honest result and supersedes the earlier headline.

### Effect A — the quantization floor (strong, robust)
At low bit-depth, uniform quantization on the real connectome **cannot operate below a hard
effective-sparsity floor**, because the heavy-tailed *integer* synapse weights round to zero:

| Bit-depth | Uniform floor | Engram floor (best) |
|---|---|---|
| int8 | 0.00 | 0.00 |
| int4 | **0.73** | **0.24** |
| ternary | **0.98** | **0.32** |

Engram-aware mixed-precision escapes the floor by keeping hub edges at int8. At int4/ternary,
uniform is *pinned at its floor* — it literally cannot reach the lower-sparsity regimes where
function survives, so engram "wins" those points by **default (uniform disqualified), not by
out-preserving at matched conditions.** This floor is the robust, publishable phenomenon.

### Effect B — matched-conditions advantage (partial, regime-dependent)
The clean apples-to-apples test is **int8**, where there is no floor, so both policies reach
every target sparsity and the comparison is genuine. There, engram-aware is **not universally
better**:

| int8 target sparsity | Uniform FPS | Best-engram FPS | Winner |
|---|---|---|---|
| 0.3 | **0.75** | 0.50 | uniform |
| 0.4 | **0.43** | 0.39 | uniform |
| 0.5 | 0.23 | **0.36** | engram |
| 0.6 | 0.27 | **0.36** | engram |
| 0.7 | 0.16 | **0.36** | engram |
| 0.8 | 0.04 | **0.19** | engram |

**Corrected claim:** the engram advantage is a **high-compression-regime phenomenon**. At gentle
compression (≤40% sparsity, int8), hub-protection *hurts* — it forces removal of mid-weight
edges to meet budget, and uniform magnitude pruning wins. The advantage emerges only under
**aggressive sparsity (≥50%) or low bit-depth**. This mirrors the torpor biology precisely:
structured pruning matters when pruning is *severe*, not mild (`../../scans/01`).

### Robustness to engram definition (tempered)
At int8 mid-sparsity, the **strength** definition is the one that beats uniform; betweenness and
k-core are weaker and sometimes do not. So "robust across all three definitions" (earlier) is
**too strong** — the effect is clearest for strength-hub protection. All three still escape the
quantization floor (Effect A). Protected hubs are the known command interneurons
(AVAL/AVAR/AVBL/PVCL/R), a real-biology sanity signal.

- Synthetic contrast (`T1_v3_synth.json`): milder floor (int4 uniform 0.18 vs real 0.73) and —
  tellingly — a large synthetic "int8 advantage" that is an **artifact of the engineered graph**;
  the real int8 comparison is the trustworthy one. This is exactly why real-data validation was
  done before proceeding.

## V3b — scaling-rule probe (H3): does the advantage track structure?
`experiments/T1_v3b_scaling_rule.py` → `results/T1_v3b_real.json`

Interpolating the real connectome toward its weight-shuffle and measuring engram advantage vs.
hub-mass fraction. Correlation = **0.96**. **Read honestly:** the aggregate hub-mass fraction
barely changes under shuffling (0.79→0.76), yet the advantage collapses (0.26 → ~0.00) as soon
as weights are shuffled. So the clean interpretation is **not** a simple "advantage ∝ hub-mass"
law; it is that the advantage depends on the **specific placement of heavy weights on hub
edges** in the real connectome, and vanishes when that placement is randomized.

- **This is the strongest validation in T1:** the engram advantage is a property of the real
  connectome's *specific weight organization*, not a generic graph artifact — it disappears
  under weight-shuffling while edge topology is preserved.
- H3 (a predictive structural rule) is **partially supported**: structure governs the advantage,
  but the predictive quantity is finer than aggregate hub-mass. A cleaner structural predictor
  is future work; the robust claim is the shuffle-sensitivity itself.

## Updated honest verdict (T1 overall) — after critical review + V4 dynamics robustness

Two separable findings, and only one survives hardening:

1. **Quantization-floor phenomenon (STRONG — survives all checks).** Uniform low-bit
   quantization of a real integer-weighted connectome catastrophically over-sparsifies
   (int4→0.73, ternary→0.98 forced sparsity); engram-aware mixed-precision escapes it. Depends
   on the weight distribution + bit-depth, **not** on dynamics (V4), and is structure-specific
   (collapses under weight-shuffle, V3b). This is the defensible, paper-grade result.

2. **Matched-conditions preservation advantage (NOT a safe claim — dynamics-dependent).** At
   equal sparsity + bit-depth (int8), engram:strength beats uniform at high sparsity under the
   leaky-rate model — **but this boundary does NOT reproduce under an independent sigmoid-
   conductance model** (V4: uniform wins nearly everywhere there). So Effect B is **model-
   sensitive and unproven**; it must not be advertised as a general result until confirmed on an
   expressive, biologically-grounded readout (real functional activity — Randi 2023).

- Absolute preservation is modest (FPS ~0.3–0.5) and, for weakly-expressive models, inflated.
- No claim about biological mind migration.

### Effect B — final status after real-activity test (V5): DROPPED
`experiments/T1_v5_real_activity.py` → `results/T1_v5_real_activity.json` (+ `T1_v5_notes.md`)

To resolve the V4 block we wired in **real** C. elegans whole-brain calcium activity (Kato
2015, 5 worms) via `shared/activity.py` and fit a data-driven dynamics model to test Effect B
on real data instead of a hand-built model.

- The linear data-driven readout (V5) was **too weak**: smooth calcium makes a persistence null
  nearly perfect, so base FPS ≈ 0.03–0.05. No headroom to test compression.
- **A cheap nonlinear gate was then run (V6)** before committing multi-day effort: a reservoir
  echo-state model. Diagnostic confirmed it **genuinely learns** (teacher-forced 10-step R²
  vs mean = +0.52 / +0.41) — but it **still cannot beat the persistence null** (R² vs
  persistence strongly negative). So the obstacle is not model weakness; short-horizon
  forecasting of this slow calcium above persistence is genuinely hard, leaving no function
  headroom for structured-vs-uniform compression to differentiate.
- **Decision (final, well-evidenced):** V4 (model-flip) + V5 (no linear headroom) + V6
  (confirmed-learning nonlinear model still can't beat persistence) ⇒ **Effect B is dropped.**
  The multi-day forecaster was gated; the gate returned NO-GO; it was not built. Revisit only if
  a dataset with real forecast headroom over persistence becomes available. See
  `results/T1_v5_notes.md`, `results/T1_v6_notes.md`.

### Final T1 status
- **Effect A (quantization sparsity floor): the paper-grade result.** Robust to dynamics and
  structure-specific. Build the FPS "compression operation" asset on this.
- **Effect B (matched engram advantage): dropped.** Not reproducible across models/readouts.
- **Banked:** real connectome loader (`shared/connectome.py` + `scripts/fetch_celegans.py`),
  real activity loader (`shared/activity.py` + Kato data), FPS metric, compression ops, and an
  honest trail of two corrected overclaims (V3 conflation, V4/V5 Effect-B).

## Next (per MASTER-PLAN Phase 1)
- Richer dynamics (LIF/GNN) + real functional activity (Randi 2023) as alternative readouts.
- Find a finer structural predictor of the advantage (V3b follow-up).
- Then T3 (replay→latent compression), which is independent.
