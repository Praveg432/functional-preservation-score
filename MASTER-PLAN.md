# Master Plan — feasible core + surrogate attacks on the blocked points

This plan does two things the earlier analysis asked for: (1) commit the **feasible
in-silico core** to concrete, runnable tracks, and (2) **not abandon the blocked Tier-A/B
points** — instead attack each with an honest *in-silico surrogate* that tests whether the
blocked step is even coherent in simulation, and maps exactly where it fails.

Guiding stance: we go as close to the final goal as the evidence and an M4 Pro allow, and
every step produces a falsifiable result that is a genuine contribution on its own — even
when the biological endpoint remains out of reach.

## The five tracks

| Track | Open question (from `NOVELTY-SCAN.md`) | Type | Primary substrate | Attacks blocked point |
|---|---|---|---|---|
| **T1** | Structured engram-aware compression of a connectome-GNN, scored by embodied/functional fidelity; breakdown-boundary map | Feasible core | FlyWire sub-circuits, MICrONS column, C. elegans | Stage 2 (quantize) |
| **T2** | Cross-individual connectome node-correspondence via hierarchical GW, scored by **functional transport** | Feasible core | C. elegans (full), FlyWire (coarsened) | Stage 3 (alignment) — **B1** |
| **T3** | Replay→low-bit latent **compression-fidelity frontier** | Feasible core | Hippocampal single-session, MICrONS traces | Stage 5c (sync/backup) |
| **T4** | Can a biologically-plausible **in-silico write-compiler** install a transported circuit's function into a differently-wired net, and where does it fail? | Surrogate | C. elegans, small recurrent nets | Stage 4 (write) — **A3** |
| **T5** | Is the **Base-OS vs. identity payload** partition empirically separable with a functional readout? | Surrogate | MICrONS, FlyWire, C. elegans | Stage 1 (partition) — **B2** |

## Dependency map

```
            ┌────────────────────────── shared substrate (datasets + loaders) ──────────────────────────┐
            │                                                                                            │
   T1 (compress) ──provides──► compressed/distilled connectome models                                   │
            │                                                                                            │
   T5 (partition) ──defines──► which sub-graph is the "payload" ──feeds──► T2 (align that payload)       │
            │                                                                   │                        │
   T2 (align) ──produces──► node-correspondence W_align + transported weights ──┘                        │
            │                                                                   │                        │
            └──────────────────────────────────────────────────► T4 (write): install transported weights
                                                                               via local plasticity, test function
   T3 (replay→latent) ──independent──► backup/sync fidelity (parallel; no hard dep)
```

- **T1 and T3 are independent and can start immediately** (lowest risk, highest "ship a
  result" probability).
- **T5 → T2 → T4 is the surrogate chain** that mirrors the blueprint's partition → align →
  write, each link falsifiable, each honest about being a simulation.
- No track depends on a biological read/write or on another track's *unpublished* claim; any
  cross-track use is an explicit, logged dependency (workspace rule).

## Sequencing (suggested)

1. **Phase 0 — substrate (shared).** Build dataset loaders (C. elegans, FlyWire sub-circuits,
   MICrONS column, one hippocampal session). Deliver a tiny "hello-connectome" GNN that
   reproduces a baseline readout. Gate: loaders + baseline reproduce published-order behavior.
2. **Phase 1 — ship the core.** Execute T1 and T3 to first results (they need only Phase 0).
3. **Phase 2 — surrogate chain.** T5 (separability) → T2 (functional transport) → T4
   (write-compiler sim), each behind its own vetting gate; stop the chain at the first gate
   that fails and report the failure as the result.

## Compute budget (M4 Pro)

- All training is small-model / sub-circuit scale; target < a few hours per run on MPS.
- Keep every experiment resumable and checkpointed (the workspace `run_all.py` pattern).
- Full spiking whole-brain sim and the PB-scale MICrONS EM are **explicitly excluded**; use
  GNN message-passing forms, coarsened graphs, and column/sub-circuit subsets.
- Hard rule: if an experiment does not fit in unified memory or exceeds a day, it is
  re-scoped to a sub-circuit, not run — and that limit is reported, not hidden.

## What success looks like (and what it does not)

- **Success:** three capability/boundary papers' worth of results (T1, T2, T3) that stand
  alone, plus two honest surrogate studies (T4, T5) that map where the blocked biological
  steps break down in simulation — a real, citable contribution to connectomics + ML.
- **Not success, and we say so:** none of this demonstrates human mind migration, non-
  destructive synaptic reading, or cross-subject identity transfer. Those remain absent
  (Tier-A). The surrogates test *coherence in simulation*, not biological feasibility.

## Ethics / scope gate

All work is computational on public animal datasets. No human subjects, no wet-lab, no
organoid work. The identity/continuity and bioethics questions in
`analysis/FEASIBILITY-RISK-LEDGER.md` remain open and are out of scope for the computational
tracks; any future wet-lab extension would require separate ethical review and is not planned
here.
