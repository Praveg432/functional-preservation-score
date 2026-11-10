# Referenced-Work Vetting — claim-by-claim reality check

Each referenced breakthrough, judged against primary sources (full detail in `../scans/`).

## Summary table

| # | Blueprint reference | Real? | Verdict | Correction needed |
|---|---|---|---|---|
| 1 | Synaptic pruning / memory resilience — "Lin et al., *Science*" | Yes | **REAL but MIS-CITED** | Cite von der Ohe et al., *J Neurosci* 2006/2007 (synapse loss) + 2025–26 artificial-hibernation study (engram resilience). Drop "Lin et al., *Science*". |
| 2 | Whole-brain connectomic GNNs — "Eon Systems / FlyWire, 2026" | Yes | **REAL; attribution [UNVERIFIED]** | Cite FlyWire (*Nature* 2024), flyGNN (NeurIPS 2025), NeuroMechFly embodiment, Loihi-2 sim. Note topology is fixed but weights are *fit*. |
| 3 | MIMO hippocampal prosthetics — +37%, cross-subject | Partly | **REAL core, OVERSTATED** | +37% is correct (Hampson 2018). Cross-*subject human* transmission is NOT supported — human work is within-subject restoration. |
| 4 | BISC high-density neural mesh | Yes | **REAL but MIS-DESCRIBED** | It is a *subdural surface* µECoG array (65,536 electrodes), NOT an *intracortical* mesh; no single-synapse resolution. |
| 5 | Optogenetic engram implantation / 2026 Nobel | Yes | **REAL but OVERSTATED** | 2026 Nobel (Deisseroth/Hegemann/Nagel) is for optogenetics broadly; engram work is animal re-activation/tagging, not human identity write. |
| 6 | Gromov-Wasserstein cross-brain alignment | Yes | **REAL but SCALE OMITTED** | GW/FUGW aligns brains at parcel scale; NP-hard, non-convex, does not scale to 10^10 nodes as written. |

## What survives verification

- Memory can survive large synaptic turnover (structured, engram-aware). **[pillar — real]**
- A connectome can be loaded as a graph and made to drive behavior in a simulated body, with
  fitted dynamical parameters. **[pillar — real, buildable]**
- Learned nonlinear models can read/bias hippocampal memory codes in humans and improve
  recall. **[real, but within-subject]**
- High-channel chronic wireless *surface* interfaces exist. **[real, wrong resolution for the task]**
- Optogenetics enables precise light control of neurons and animal engram manipulation. **[real]**
- GW is a valid alignment tool at small/medium scale. **[real, scale-limited]**

## What does NOT survive verification

- A **chronic, non-destructive, single-synapse-resolution read** of a living human brain.
  **No modality. Not overstated — absent.**
- **Cross-subject identity/memory transfer in humans.** No evidence at any scale.
- **Writing a structured identity payload** into a differently-wired adult human brain via
  STDP/optogenetics. Unproven in principle; animal work only re-activates existing engrams.
- **GW alignment at 1.4×10^10 nodes.** Computationally infeasible as specified.
- The **"Base-OS vs. identity payload" partition** as a clean neuroscientific fact — it is a
  design hypothesis (see `ARCHITECTURE-DECOMPOSITION.md §1`), not an established dissociation.

## Net

Five of six references are grounded in real work, but each is stretched: three by
attribution/description errors, two by claiming more than the source shows, and the alignment
math by ignoring its scaling wall. The *individually real* pieces do not compose into the
end-to-end claim. The buildable intersection is reference #2 (connectome-as-GNN) plus pillar
#1 (structured sparsification) — the Phase-1 in-silico core.
