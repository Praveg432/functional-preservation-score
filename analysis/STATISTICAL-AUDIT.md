# Statistical & Methodological Audit (pre-submission)

A skeptical review of every numerical finding for the flaws that invalidate results: missing
uncertainty, small-n, single-seed dependence, data leakage, improper nulls, and
multiple-comparisons / selection bias. Severity: CRITICAL (can invalidate a claim), MODERATE
(weakens it / needs a caveat), MINOR (note).

## Findings ledger

| # | Track | Issue | Severity | Remediation |
|---|---|---|---|---|
| A1 | all | **No uncertainty quantification** — point estimates (means over 3 seeds) with no CIs or significance tests. | CRITICAL | Bootstrap 95% CIs on every headline number; permutation p-values for the key comparisons. |
| A2 | T3-V2 | **Single train/test split** (seed 0, 18/8). Frontier + headroom rest on one split; top-1 is coarse (steps of 1/8). | CRITICAL | Repeated stratified CV (≥20 splits) → mean ± CI; permutation null for identification. |
| A3 | T1-V3 | **Selection bias: "best engram policy" = max over 3 definitions** inflates the advantage. | MODERATE | Report each policy separately + a pre-registered primary (strength); no max-over-policies in the headline. |
| A4 | T3-V2 | **Multiple comparisons** across 24 (dim×bits) configs picking the floor, uncorrected. | MODERATE | Report the full surface with CIs; define the floor by a monotone criterion, not the single best cell. |
| A5 | T5 | z-score reported **without a p-value**; one payload set per definition. | MODERATE | Permutation p-value from the null draws; report both hub definitions (already identical). |
| A6 | T2, T4 | **No seeds/CIs on divergence curves** (T2 single perturbation seed; T4 3 seeds, no CI). | MODERATE | Multiple perturbation seeds + bootstrap CIs; permutation/sign tests on the gap. |
| A7 | FPS | Null is deterministic single-permutation (seed 7); not a null *distribution*. | MINOR | For significance, use a permutation distribution (many shuffles), not one draw. |
| A8 | T3 AE | `coord_min/max` (quantization range) fit on train only — **verified no leakage**. PCA fit on train only — **verified**. | OK | No action; documented. |
| A9 | all | Effect sizes not reported alongside significance. | MODERATE | Report effect size (margin, Cohen's d where applicable) + CI, not just pass/fail. |

## What was already sound (credit where due)
- FPS null is the *best* trivial baseline (shuffle ∨ mean), not a weak single null (A7 only
  concerns significance testing, not the metric's validity).
- T3-V2 AE is fit on train, scored on held-out test (no leakage) — A8 verified by code read.
- T5 null is 40 random equal-size subsets (a real null distribution); only the p-value was missing.
- T1 policies are compared at matched *effective* sparsity (the earlier budget-confound was fixed).
- Determinism + committed artifacts mean every number is reproducible.

## Remediation plan (this audit)
1. Add a shared `stats.py`: bootstrap CI, permutation test, repeated-CV helper.
2. T3-V2: repeated-CV identification with per-config mean ± 95% CI + permutation p-value for the
   uncompressed headroom claim; floor defined by a monotone rule.
3. T1-V3: report per-policy curves with bootstrap CIs over stimulus seeds; drop max-over-policies
   from the headline; keep the floor phenomenon (which is deterministic, not a mean).
4. T5: permutation p-value for the privilege test (already has the null distribution).
5. T2/T4: multiple perturbation/model seeds + bootstrap CIs; sign/permutation test on the gap.
6. Update PAPER.md: every headline number as estimate ± 95% CI with n and p where applicable;
   add a "Statistical Methods" subsection; soften any claim whose CI crosses the threshold.

## Honest expectations
Several results will survive with wider error bars (T1 floor is deterministic; T5 corrective and
T4 gap are large). The small-n ones (T3-V2 n=8 test, T2 single-perturbation) will get materially
wider CIs — and if a CI crosses the decision threshold, the claim is softened accordingly. That
is the point of the audit.

---

## Remediation outcomes (executed)

Added `shared/stats.py` (bootstrap CI, permutation tests, Cohen's d) and a `*_stats.py`
experiment per track. All headline claims survived hardening; several point estimates moved to
honest (usually slightly lower / wider) values. Hardened artifacts: `tracks/*/results/*_stats.json`.

| Claim | Before (point) | After (hardened) | Survives? |
|---|---|---|---|
| T1 engram advantage @int4 | "margin +0.25, best-of-3 policies" | strength-only: engram 0.30 [0.12,0.48] vs uniform 0.03 [0,0.09], p=0.015–0.031, d=1.0–1.4 | **Yes** (selection bias removed) |
| T1 quantization floor | 0.73/0.98 uniform vs 0.27/0.32 engram | identical (deterministic weight-distribution property, no seed variance) | **Yes** (strongest result) |
| T3 identification | 0.75 (single split) | 0.69 [0.63,0.74], 30-fold CV, p=10⁻⁴ | **Yes** (single-split optimism corrected) |
| T3 frontier | single-split floor cell | per-config CIs, all > chance, non-overlapping | **Yes** |
| T5 no separable module | z≈+1 (no p) | p=0.16–0.37 (500-sample null), ns at all sizes | **Yes, strengthened** (corrective is significant) |
| T2 GW corr @5% | 0.88 (1 seed) | 0.76 [0.74,0.78] (8 seeds) | **Yes** (optimism corrected) |
| T2 transport collapse | masked 0.33, gw ~0 (1 seed) | masked 0.40 [0.31,0.49] p=3e-4; gw 0.06 [0,0.13] p=2e-4 | **Yes** |
| T4 plausibility gap | ~0.5–0.67 (3 seeds, no test) | 0.45 [0.27,0.64], 10 seeds, p=10⁻⁴, d=2.0 | **Yes** |
| T4 ripple helps (H3) | "no" (3 seeds) | Δ=−0.000 [−0.003,+0.002], CI∋0 | **Yes** (negative confirmed) |

**Net:** no claim was invalidated; two were *strengthened* by adding significance (T5, T4-H3);
three point estimates were corrected downward to remove single-split/selection optimism (T3
0.75→0.69, T2 0.88→0.76, T1 best-of-3→strength-only). The quantization floor is deterministic and
unchanged. PAPER.md now reports every headline as estimate ± 95% CI with n and p, and §3.4
documents the statistical methods.

## Residual limitations (carried into the paper, not fixed)
- Absolute n remains small for some substrates (T3 laps, T2/T4 seeds): CIs are wide and honestly
  reported; conclusions rest on effect direction + significance, not precise magnitudes.
- Single real connectome / single replay session: results are substrate-specific; cross-substrate
  replication (mouse MICrONS, more worms) is future work, flagged in §8.
- Toy-net scale for T4; idealized dynamics throughout — qualitative claims only.
