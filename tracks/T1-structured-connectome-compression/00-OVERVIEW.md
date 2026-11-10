# T1 — Overview

## Problem

The blueprint asserts synaptic weights can be crushed to 4-bit/ternary because torpor shows
memory survives ~50–65% synapse loss. But torpor **preferentially preserves engram-critical
synapses** (`../../scans/01-synaptic-pruning-torpor.md`) — it is *structured*, not uniform.
So the real question is empirical: **how much, and with what structure, can you compress a
connectome-driven model before its function collapses?**

## Approach

1. **Baseline model.** Load a connectome sub-graph as a recurrent message-passing GNN (or
   LIF network for C. elegans) and fit/validate a functional readout:
   - FlyWire central complex → locomotion heading in a simple embodied loop (or a
     published activity-matching target if embodiment is too heavy).
   - MICrONS column → predict held-out calcium responses to stimuli.
   - C. elegans whole-brain → reproduce stereotyped activity motifs (fast sanity harness).
2. **Two compression axes, crossed:**
   - **Sparsity** (edge removal): 0–80%.
   - **Bit-depth** (weight quantization): fp32 → int8 → int4 → ternary {-1,0,+1}.
3. **Two structure policies:**
   - **Uniform** (magnitude pruning, per-tensor quantization) — the baseline.
   - **Engram-aware** (preserve high-betweenness / high-in-strength / multi-synaptic-hub
     edges; mixed-precision keeping hub weights at higher bit-depth) — the hypothesis.
4. **Teacher–student distillation** (cite CKD / reverse-KD prior art): full-precision teacher
   → compressed student, distilling the *functional output*, measuring behavioral fidelity
   rather than reconstruction error.
5. **Breakdown map:** chart the fidelity surface over (sparsity × bit-depth × structure);
   locate the collapse frontier; test whether engram-aware pushes the frontier out.

## Hypotheses

- H1: engram-aware compression retains function at budgets where uniform fails.
- H2: there is a sharp, characterizable collapse boundary (not a gentle degradation).
- H3: the boundary location scales with a graph-structural quantity (e.g. spectral gap /
  hub-mass fraction), giving a predictive rule.

## What a negative result means (and is still worth)

If engram-aware ≈ uniform, H1 is dead and the blueprint's "structured sparsification" premise
is unsupported even in-silico — a publishable corrective. The breakdown map is a contribution
either way.
