# Findings walkthrough

A study-by-study walk through the results, each with the exact committed numbers, the artifact
they come from, and how to read them. This is the "understand the paper in detail" companion:
read `02-FUNDAMENTAL-PRINCIPLES.md` first for the concepts, then this for the evidence.

The headline: **compression of neural data is measurable and bounded; migration of function
across substrates is not supported by the proposed pipeline.** Two positive studies (compression,
replay) and a three-stage negative (partition, transport, write).

---

## Study 1 (T1) — Connectome compression
**Question.** How far can a connectome-driven model be compressed before function collapses, and
does structured (hub-protecting) compression beat uniform?

**Key numbers** (`tracks/T1-structured-connectome-compression/results/T1_v3_stats.json`):
- **Quantisation sparsity floor (deterministic):** uniform int4 → 0.73, ternary → 0.98; engram
  int4 → 0.27, ternary → 0.32. int8 → 0.0 (no floor).
- **Matched int4, engram vs uniform:** FPS 0.30 [0.12, 0.48] vs 0.03 [0.00, 0.09]; p = 0.015,
  d = 1.3 (target sparsity 0.5), with similar margins at 0.6 and 0.7.

**How to read it.** Low-bit uniform quantisation *cannot* represent a heavy-tailed integer
connectome at low sparsity — small weights round to zero, forcing 73%/98% of edges away. Hub
protection escapes this. The structured advantage is real at matched budget but regime-dependent
and not robust across dynamics models, so the paper keeps only the **floor** as the robust claim.

## Study 2 (T3) — Replay-sequence compression
**Question.** Can decoded replay sequences be compressed to few bits while remaining identifiable,
and does a bounded store have a capacity limit?

**Key numbers** (`.../T3_v2_stats.json`, `T3_v3.json`):
- **Uncompressed identification:** top-1 **0.69** (95% CI [0.63, 0.74]) vs chance 0.125;
  permutation **p = 1e-4** (30-split CV).
- **Frontier:** dim16@128 bits/event 0.69; dim16@32 0.58 [0.53,0.64]; dim8@16 0.40 [0.35,0.45];
  dim4@8 0.28 [0.24,0.32] — all above chance, CIs non-overlapping down the ladder.
- **Capacity:** superposition store degrades gracefully (recovery 1.00→0.50→0.30 at loads
  2→10→20); slot store perfect to capacity (10) then cliffs.

**How to read it.** A ~38 kbit sequence stays identifiable from ~8–16 bits/event (≈10³×
compression), with graceful degradation. The "compressed backup" idea is information-theoretically
plausible *as compression of decoded sequences* — not evidence a backup contains a memory.

## Study 3 (T5 → T2 → T4) — The migration pipeline in simulation
Each stage tests a biological stage with no direct evidence; the question is coherence in
simulation.

### T5 — Partition separability
**Numbers** (`.../T5_v2_stats.json`, 500-sample null): payload-ablation drop vs random-interneuron
null — frac 0.1: 0.85 vs 0.58, **p = 0.17**; 0.2: 1.00 vs 0.70, **p = 0.16**; 0.3: **p = 0.27**;
0.4: **p = 0.37**. Not significant at any size.
**Read:** the asserted "identity payload" is no more special than a random interneuron subset of
the same size — **no separable identity module**; function is distributed.

### T2 — Functional transport (Gromov–Wasserstein)
**Numbers** (`.../T2_v2_stats.json`, 8 seeds, 5% divergence): GW correspondence 0.76 [0.74,0.78];
transport fidelity — oracle + unconstrained **1.00**; oracle + feasibility mask **0.40**
[0.31,0.49] (p = 3e-4); GW correspondence **0.06** [0.00,0.13] (p = 2e-4).
**Read:** alignment works, but transport preserves function only in a doubly-idealised limit.
The target's own wiring (feasibility mask) collapses it; imperfect alignment collapses it further.
High matching accuracy ≠ preserved function.

### T4 — Local-rule writing
**Numbers** (`.../T4_v2_stats.json`, 10 seeds): global ceiling **1.00** [1.00,1.00]; best local
**0.55** [0.36,0.73]; **plausibility gap 0.45** [0.27,0.64], p = 1e-4, **d = 2.0**; ripple−plain
Δ = −0.000 [−0.003,+0.002] (CI includes 0).
**Read:** the topology *can* host the function (global reaches 1.0), but biologically-plausible
local plasticity cannot reach it, and ripple timing does not help. The write is coherent in
principle, not achievable by the proposed mechanism.

### The three stages together
Independent, compounding failures: nothing clean to extract (T5); the whole graph cannot be placed
under realistic alignment + target wiring (T2); even a feasible target is unreachable by the
proposed write (T4). One constraint — **the target substrate's wiring** — is the binding limit in
T2 and T4.

---

## Methodological episodes (why some numbers changed)
The paper documents five corrections, each made once from an explicit diagnosis (prior wrong
results retained):
1. **FPS null hardened** — a constant output beat a shuffle-only null → null redefined as
   max(shuffle, mean).
2. **T1 matched-budget bug** — integer-weight ties made uniform pruning over-remove → deterministic
   tie-breaking so policies compare at identical budgets.
3. **"Effect B" dropped** — on real calcium, persistence is near-ceiling, so the matched-conditions
   structured-advantage claim was not supportable and was dropped (not threshold-shopped).
4. **T3 metric replaced** — trajectory-rank fidelity had a structurally-high null → replaced with
   bounded identification accuracy (hence CV top-1 0.69, down from a single-split 0.75).
5. **T5 instrument corrected** — ablating sensory+motor trivially zeroed FPS (removes the I/O the
   metric needs) → reformulated with a fixed I/O interface.

## How to verify any number yourself
Each `*_stats.json` lists the experiment, substrate, seeds/splits, and the CI/p it reports; the
producing script is the matching `tracks/*/experiments/*_stats.py` (or the base experiment). The
figures in `paper/figures/` are built from these JSONs by `paper/make_figures.py`. Nothing is
recomputed at build time, so the paper's numbers and the repo artifacts are guaranteed consistent.
