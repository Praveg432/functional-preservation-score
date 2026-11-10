# T4 — Results (in-silico write-compiler)

Final link of the surrogate chain, attacking the blueprint's Stage-4 "write" (Tier-A risk A3).
Question: can **biologically-plausible local plasticity** install an externally-specified
input→output function into a **fixed foreign topology**, and where does it fail? Strict
local-only constraint (reward-modulated Hebbian/three-factor + optional ripple gating; **no
backprop, no per-weight target gradient** — audited). Requires `.venv`.

## V1 — local-rule installs something → FAIL as a bare gate, but **diagnostic is the finding**
`experiments/T4_v1_easy_install.py` → `results/T4_v1.json`; diagnosis `scripts/diagnose_t4.py`

Local-rule installation was inconsistent and mostly *hurt* (mean gain −0.04; only 1/3 seeds
improved). Rather than call the write "incoherent," the diagnosis checked the global-optimizer
ceiling on the same fixed topology:

| seed | no-plasticity control | LOCAL rules | GLOBAL optimizer ceiling |
|---|---|---|---|
| 0 | 0.20 | 0.03 | **1.00** |
| 1 | 0.18 | 0.12 | **1.00** |
| 2 | 0.71 | 0.82 | **1.00** |

The topology **can** host the function (global reaches 1.00) — but local rules cannot find it
(except by luck when already close, seed 2). So V1's "fail" is actually a **clean plausibility-gap
result**, not an inconclusive one.

## V2 (+V3) — reachability map + structured teaching → **large, persistent plausibility gap**
`experiments/T4_v2_reachability.py` → `results/T4_v2.json`

| host↔target divergence | global ceiling | local (plain) | local (ripple-timed) | plausibility gap |
|---|---|---|---|---|
| 0.0 | 1.00 | 0.32 | 0.33 | **0.67** |
| 0.1 | 0.99 | 0.43 | 0.43 | 0.56 |
| 0.3 | 0.88 | 0.22 | 0.22 | 0.66 |
| 0.5 | 0.89 | 0.42 | 0.42 | 0.47 |

Three findings:
1. **Large plausibility gap (the headline).** A non-biological global optimizer installs the
   function (ceiling ~1.0), but biologically-plausible local plasticity reaches only 0.22–0.43 —
   a gap of ~0.5–0.67 at every divergence. **The write is coherent in principle but not
   achievable by the proposed mechanism.**
2. **Ripple-timing does NOT help (H3 negative).** Ripple-gated plasticity ≈ continuous
   plasticity everywhere. The blueprint's specific sleep-ripple consolidation mechanism confers
   no advantage in this model — a clean, honest negative on the proposed write mechanism.
3. **Global ceiling falls with divergence** (1.00 → 0.88), re-confirming T2's feasibility limit:
   as the target needs edges the host lacks, even the optimal write degrades.

## Verdict (Stage-4)
The in-silico write is **not logically impossible** — a perfect global optimizer achieves it on
a feasible topology. But the **biologically-plausible mechanism the blueprint proposes**
(broadcast reward/neuromodulator-gated local plasticity, including sharp-wave-ripple timing) is
**demonstrably insufficient** to install an identity-scale function, by a wide and persistent
margin. The write's bottleneck is not "we haven't built the hardware" — it is that *local,
broadcast-signal learning does not reach the global solution* the topology permits.

## Honest scope (loud)
Toy 40-neuron rate nets, reflex-scale target functions, idealized three-factor rules. This maps
the *mathematical ceiling and the mechanism gap* of the write idea — it does **not** establish
anything about writing to a living brain (Tier-A A3 remains absent). The global ceiling is an
upper bound no biological method would reach; the local result is an optimistic in-silico analogue
of the proposed mechanism. A richer plasticity rule might narrow the gap — logged as future work —
but the proposed mechanism, as specified, fails here.

## Status
- V1 (diagnostic plausibility gap), V2 (gap mapped), V3 (ripple-timing negative) — all run.
- **Banked:** fixed-topology host, audited local-only plasticity, installer, global-optimizer
  baseline, reachability sweep.
- **Closes the surrogate chain** — see `../../analysis/SURROGATE-CHAIN-SYNTHESIS.md`.