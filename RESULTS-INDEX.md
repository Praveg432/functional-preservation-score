# Results Index

Every committed result maps to the script that produced it. All Phase-0 results are
deterministic and run in seconds on CPU (M4 Pro).

| Result | Script (in `tracks/T1-structured-connectome-compression/`) | File | Status |
|---|---|---|---|
| T1-V1 baseline (synthetic) | `experiments/T1_v1_baseline.py` | `results/T1_v1.json` | **PASS** (ref 1.0, shuffled 0.0) |
| T1-V1 baseline (REAL) | `experiments/T1_v1_baseline.py --real` | `results/T1_v1_real.json` | **PASS** (ref 1.0, shuffled 0.0) |
| T1-V2 structure-adv (synthetic) | `experiments/T1_v2_structure_advantage.py` | `results/T1_v2.json` | **PASS 3/3** (engram 0.79 vs uniform 0.31) |
| T1-V2 structure-adv (REAL, confounded point) | `experiments/T1_v2_structure_advantage.py --real` | `results/T1_v2_real.json` | threshold not met; confound found |
| T1-V2b matched-effective (REAL) | `experiments/T1_v2b_matched_effective.py --real` | `results/T1_v2b_real.json` | **engram advantage CONFIRMED** (margin +0.23; int4 floor found) |
| T1-V2b matched-effective (synthetic) | `experiments/T1_v2b_matched_effective.py` | `results/T1_v2b_synth.json` | advantage confirmed (margin +0.27) |
| T1-V3 breakdown map (REAL) | `experiments/T1_v3_breakdown_map.py --real` | `results/T1_v3_real.json` | **floor phenomenon** (int4 uniform 0.73 vs engram 0.24). *Headline corrected — see below.* |
| T1-V3 breakdown map (synthetic) | `experiments/T1_v3_breakdown_map.py` | `results/T1_v3_synth.json` | milder floor; int8 advantage is a synthetic artifact |
| T1-V3b scaling rule / H3 (REAL) | `experiments/T1_v3b_scaling_rule.py` | `results/T1_v3b_real.json` | advantage collapses under weight-shuffle (structure-specific); H3 partially supported |
| T1-V3 critical review | `scripts/review_v3.py` | (prints) | decomposes V3 into Effect A (floor, strong) + Effect B (matched advantage, regime-dependent) |

> **Important (critical review 2026-11-07):** the first-pass V3 headline "engram advantage
> grows as bits shrink (0.04/0.25/0.29)" was **misleading** — it conflated the quantization
> floor (uniform disqualified) with a true matched-conditions advantage. Corrected finding:
> (A) a robust low-bit **sparsity floor** that engram-aware escapes [KEPT], and (B) a matched
> advantage that proved **dynamics-dependent (V4) and unsupported on real activity (V5) —
> DROPPED**. See `tracks/T1-structured-connectome-compression/RESULTS.md`.

| T1-V4 dynamics robustness | `experiments/T1_v4_dynamics_robustness.py` | `results/T1_v4_real.json` + `_notes.md` | Effect B NOT model-invariant (flips under sigmoid model) |
| T1-V5 real-activity (Kato 2015) | `experiments/T1_v5_real_activity.py` (needs `.venv`) | `results/T1_v5_real_activity.json` + `_notes.md` | linear readout too weak (persistence null dominates) |
| T1-V6 Effect-B go/no-go gate (reservoir) | `experiments/T1_v6_reservoir_probe.py` (needs `.venv`) | `results/T1_v6_reservoir_probe.json` + `_notes.md` | **NO-GO**: nonlinear model confirmed-learning (R²vs-mean +0.5) but cannot beat persistence; Effect B **dropped for good** |

## T3 — replay→latent compression

| Result | Script (needs `.venv`) | File | Status |
|---|---|---|---|
| T3-V1 data gate (nelpy) | `tracks/T3-.../experiments/T3_v1_data_gate.py` | `results/T3_v1.json` | **PASS** (decode 0.34 vs 0.20) |
| T3-V2 floor (nelpy, underpowered) | — | `results/T3_v2_notes.md` | underpowered on small session (honest stop) |
| T3-V2 floor (DANDI 000044, identification) | `tracks/T3-.../experiments/T3_v2_compression_floor.py` | `results/T3_v2.json` | **PASS**: top-1 0.75 vs chance 0.125; ~1000x+ compression stays event-identifiable |
| T3-V3 sync capacity/interference | `tracks/T3-.../experiments/T3_v3_sync_capacity.py` | `results/T3_v3.json` | **PASS**: superposition degrades gracefully, slot store perfect-then-cliff; real capacity trade-off |

Data fetch: `scripts/fetch_dandi_replay.py` (streams spikes+position from a 5 GB remote NWB, no
full download). **T3 COMPLETE (3/3 gates pass on real replay data):** decoded replay population sequences are
highly compressible (~10–50 bits/event, ~1000x+) while remaining event-identifiable (V2), and a
bounded "background-sync" latent store has a real capacity/interference trade-off (V3) — graceful
bleed (holographic) vs perfect-then-cliff (slots). This is a measured, information-theoretic
characterization of the blueprint's "compressed replay backup" idea on real data. Does NOT touch
Tier-A (synaptic read / identity): it compresses decoded sequences, not memories or a person.

## T5 — Base-OS / identity-payload separability (surrogate; attacks Stage-1 / B2)

| Result | Script (needs `.venv`) | File | Status |
|---|---|---|---|
| T5-V1 ablation sanity | `tracks/T5-.../experiments/T5_v1_ablation_sanity.py` | `results/T5_v1.json` | **PASS** (readout lesion-sensitive) |
| T5-V2 separability vs null | `tracks/T5-.../experiments/T5_v2_separability_null.py` | `results/T5_v2.json` | **H2 corrective**: asserted payload no more privileged than random interneurons (z≈+1, beats ~70% of nulls) |

**T5 finding:** on the real C. elegans connectome there is **no cleanly separable "identity
payload"** — the integrative interneuron core carries function but barely more than a random
interneuron subset; function is distributed, not a localized swappable module. A direct, measured
**corrective to the blueprint's Stage-1 clean-partition premise**. (Instrument was corrected once
after V1 diagnosis: Base-OS = fixed I/O interface, never ablated.) Surrogate scope: bounds the
premise on the nearest testable system; no human claim.

## T2 — cross-individual functional transport via GW (surrogate; attacks Stage-3 / B1)

| Result | Script (needs `.venv`) | File | Status |
|---|---|---|---|
| T2-V1 correspondence sanity | `tracks/T2-.../experiments/T2_v1_correspondence.py` | `results/T2_v1.json` | **PASS**: GW recovers 92% of ground-truth matching (chance 0.3%) |
| T2-V2 transport + V3 boundary | `tracks/T2-.../experiments/T2_v2_transport_function.py` | `results/T2_v2.json` | PASS-in-ideal / **corrective-under-realism** |

**T2 finding (layered):** (1) transport math is sound with an *oracle* correspondence +
unconstrained writing (fidelity 1.0); (2) **feasibility mask is the killer** — require writing
only edges the target supports and fidelity collapses 1.0→~0.35 at 5% divergence (H3: can't write
what the target isn't wired for); (3) real GW correspondence (92% acc) still gives fidelity 0.19→0
— high matching accuracy ≠ preserved function. **Corrective to the blueprint's "align-and-write"
Stage-3**, which silently assumed perfect correspondence AND unconstrained writing. With T5 (no
separable module to transport), the pathway is unsupported in-silico. Worm + divergence model;
no human claim (Tier-A A4 unchanged).

## T4 — in-silico write-compiler (surrogate; attacks Stage-4 / A3)

| Result | Script (needs `.venv`) | File | Status |
|---|---|---|---|
| T4-V1 easy install (+ diagnosis) | `tracks/T4-.../experiments/T4_v1_easy_install.py` | `results/T4_v1.json` | gap finding: global ceiling 1.0, local rules 0.03–0.82 |
| T4-V2 reachability + V3 ripple | `tracks/T4-.../experiments/T4_v2_reachability.py` | `results/T4_v2.json` | **large plausibility gap** (global 1.0 vs local 0.2–0.4); ripple-timing does not help |

**T4 finding:** the write is coherent in principle (a global optimizer installs the function,
ceiling ~1.0 on a feasible topology) but the blueprint's **biologically-plausible mechanism**
(broadcast-reward local plasticity, incl. ripple-timing) is **insufficient** — gap ~0.5–0.67 at
all divergences; ripple-timing confers no advantage. Toy nets, idealized rules; no living-brain
claim (Tier-A A3 unchanged).

## Surrogate chain T5→T2→T4 — see `analysis/SURROGATE-CHAIN-SYNTHESIS.md`
Layered corrective to the blueprint's partition→align→write pathway: (T5) no separable payload
module, (T2) transport breaks under realistic alignment + the target's own wiring, (T4) the
proposed write mechanism can't reach the solution the topology permits. Each fails for an
independent reason; the target substrate's wiring is the recurring binding limit.

**Final T1 verdict:** Effect A (quantization sparsity floor) is the paper-grade result. Effect B
(matched engram advantage) is **dropped on strong evidence** — V4 (model-flip) + V5 (no linear
headroom) + V6 (a *confirmed-learning* nonlinear reservoir still cannot beat the persistence
null). The multi-day forecaster was gated and the gate returned NO-GO, so it was not built.
Real connectome + real activity loaders + reservoir harness are banked. Methodological finding:
on slow whole-brain calcium, persistence is a near-ceiling short-horizon baseline.

See `tracks/T1-structured-connectome-compression/RESULTS.md` for the full honest write-up,
including the quantization confound found on real data and the int4 effective-sparsity floor.

## Reproduce

```bash
python3 -m pip install -r requirements.txt
python3 -m pytest -q                                      # 6 substrate tests
python3 scripts/fetch_celegans.py                         # fetch real connectome (once, needs net)
T1=tracks/T1-structured-connectome-compression/experiments
python3 $T1/T1_v1_baseline.py           ; python3 $T1/T1_v1_baseline.py --real
python3 $T1/T1_v2_structure_advantage.py; python3 $T1/T1_v2_structure_advantage.py --real
python3 $T1/T1_v2b_matched_effective.py ; python3 $T1/T1_v2b_matched_effective.py --real
```

## Keystone asset status

- **FPS metric** (`shared/fps.py`): implemented, tested (identity→1.0, trivial→0.0), and in
  use as the scoring currency for T1. This is the asset `analysis/IMPACT-STRATEGY.md` elevates
  to the first deliverable. Next: factor the compression/alignment/ablation operations into a
  released `connectome-operations` API, all FPS-scored.
