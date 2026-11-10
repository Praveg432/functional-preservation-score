# T1 — Pre-Registration (fixed before running V2)

Locked choices. No post-hoc changes; any deviation is logged in RESEARCH-LOG with a reason.

## Substrate
- C. elegans connectome via `shared.connectome.load_celegans` (deterministic synthetic
  fallback, `n=300`, seeds `0,1,2` for multi-seed checks). Real-data swap is a documented hook
  and, when used, re-runs the same gates.

## Model + battery
- `shared.model.ConnectomeModel` leaky-rate dynamics (leak=0.3, gain=1.0).
- Behavioral battery: `default_stimulus_bank(n_sensory, n_patterns=8, T=40, seed=1)`.
- Reference = full-precision, un-pruned model. FPS via `shared.fps.Battery`.

## Metrics
- Primary: **FPS** (null-normalized functional preservation), as defined in `shared/fps.py`.
- Sparsity measured as actual removed-edge fraction vs. original (`actual_sparsity`).

## V1 — baseline-reality gate
- **Pass criterion:** reference model FPS vs. itself ≈ 1.0 AND a shuffled-graph control
  scores FPS < 0.2. (The connectome carries function that a random graph does not.)

## V2 — structure-advantage gate (load-bearing)

**AMENDED 2026-11-07 after real-data validation.** The original single-point "50% prune + int4"
test was confounded: int4 quantization on the real connectome's heavy-tailed integer weights
induces extra sparsity, so matched *pruning* budget ≠ matched *total* compression. The canonical
gate is now the matched-total-effective-sparsity curve (V2b). The original point-test is retained
as `T1_v2*` for the record but is not load-bearing.

- **Canonical gate (V2b):** compare uniform vs. engram-aware at MATCHED total effective sparsity
  (measured after prune+quant), swept over {0.5, 0.6, 0.7, 0.8}, FPS averaged over stimulus
  batteries {1,2,3}.
- **Pass criterion:** engram-aware FPS > uniform FPS at ≥ (n_targets − 1) of the swept points
  AND mean margin > **0.05**, on the REAL connectome.
- **Fail → kill/re-scope:** if engram-aware ≈ uniform across the curve (mean margin < 0.05), H1
  is refuted; report as a corrective to the blueprint's "structured sparsification" premise.
- `protect_frac=0.25`; `quant=int4`; high-precision tier `int8` for hub edges.
- **Status:** PASS on real data (mean margin +0.23) and synthetic (+0.27). See `RESULTS.md`.

## Seeds / repeats
- Seeds {0,1,2}. Report per-seed and mean. No seed selection after the fact.
