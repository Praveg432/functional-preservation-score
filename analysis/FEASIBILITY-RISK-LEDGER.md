# Feasibility & Risk Ledger

Load-bearing assumptions, each with the single observation that would falsify it
(kill-criterion) and current status. Mirrors the workspace's vetting-gate discipline:
an assumption is only "held" if it survives its kill-criterion.

## Tier A — fatal to the end-to-end vision (currently FAILING)

| ID | Assumption | Kill-criterion | Status |
|---|---|---|---|
| A1 | A living human brain can be read **non-destructively at single-synapse resolution**, chronically. | No in-vivo human modality resolves single synapses across the payload. | **FAILED** — BISC is surface µECoG; synapse-resolution = destructive vEM. (`../scans/04`) |
| A2 | A person's **identity is fully captured by a static weighted connectome graph**. | Function demonstrably requires non-graph state (dynamics, neuromodulation, glia, plasticity). | **FAILED (partial)** — connectome-GNNs must *fit* weights/time-constants absent from topology. (`../scans/02`) |
| A3 | An external **identity payload can be written** into a differently-wired adult human brain. | No demonstration, even in animals, of installing a *novel structured identity* (only re-activation of existing engrams). | **FAILED** — absent in principle. (`../scans/05`) |
| A4 | **Cross-subject identity transfer** is possible in humans. | No human donor→recipient identity/memory transfer at any scale. | **FAILED** — absent. (`../scans/03`) |

Any one of A1–A4 failing breaks the series chain (see `ARCHITECTURE-DECOMPOSITION.md`). All
four currently fail. **The end-to-end migration architecture is not feasible with current or
clearly-foreseeable technology, and is not thesis-grade.**

## Tier B — serious obstacles (open, would need major work)

| ID | Assumption | Kill-criterion | Status |
|---|---|---|---|
| B1 | GW alignment scales to ~10^10 nodes. | No tractable GW variant at >10^6–10^7 nodes. | **OPEN/UNLIKELY** — NP-hard; parcel-scale today. (`../scans/05`) |
| B2 | The Base-OS / identity-payload partition is cleanly separable. | Identity-relevant computation found in "dropped" regions. | **OPEN** — distributed substrates argue against a clean cut. |
| B3 | Boundary "anchors" between payload and clone Base-OS can be functionally re-aligned. | Anchor wiring is individual/experience-shaped, not re-creatable. | **OPEN.** |

## Tier C — real but modest enablers (hold, bounded effect)

| ID | Assumption | Status |
|---|---|---|
| C1 | Memory survives large *structured* synaptic turnover. | **HOLDS** (engram-aware only). (`../scans/01`) |
| C2 | A connectome can drive behavior in a simulated body (with fitted params). | **HOLDS.** (`../scans/02`) |
| C3 | Hippocampal prosthetics improve *within-subject* recall (~37%). | **HOLDS.** (`../scans/03`) |
| C4 | IQ/EQ priming interventions have real but small effects. | **HOLDS, bounded.** |

## Non-technical gates (flagged, not resolved)

- **Identity/continuity:** even if a copy were made and instantiated, whether it is "you"
  (continuity of consciousness vs. a copy) is an unresolved philosophical question that gates
  the entire premise — not a detail.
- **Ethics/consent/cloning:** human reproductive cloning and experimental brain-writing are
  broadly prohibited and raise consent, welfare, and identity-rights issues.
- **Organoid sentience:** Phase-2 iPSC cortical-organoid "write" testing raises active
  bioethics questions about organoid moral status.

These are listed because they are **blocking**, not peripheral: a thesis cannot route around
them by treating them as future work.

## Bottom-line feasibility call

- **End-to-end non-destructive human mind migration:** **NOT FEASIBLE** (Tier A all failing).
  Not a near-term thesis.
- **Phase-1 in-silico core** (structured connectome sparsification + cross-graph behavioral
  transfer on public connectomes): **FEASIBLE** and buildable. Depends only on C1 + C2, which
  hold. This is the residual to pursue. See `RECOMMENDATION.md`.
