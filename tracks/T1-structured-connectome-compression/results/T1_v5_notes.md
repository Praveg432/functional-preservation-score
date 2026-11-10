# T1-V5 — resolving the Effect-B block with REAL activity: status

Result file: `T1_v5_real_activity.json`. Data: Kato et al. 2015 whole-brain calcium
(`data/kato2015_WT_NoStim.mat`, OSF osf.io/na4f9, 5 worms, ~109–135 neurons, ~3000 frames
@ ~3 fps). Loader: `shared/activity.py`. Requires the `.venv` (h5py).

## Goal
Resolve the V4 block: Effect B (engram > uniform at high sparsity) flipped between two hand-
built dynamics models, so it needed an expressive, biologically-grounded readout. Plan: fit a
data-driven model to real activity, then test compression preservation on real-dynamics
prediction.

## What was tried (two readout framings; stopped after two per the no-patch-twice rule)
1. **One-step prediction** (`x[t+1]=A x[t]`, ridge): base predictive FPS ≈ 0.03. Calcium ΔF/F
   at 3 fps is very smooth, so the persistence null (`x[t+1]≈x[t]`) is nearly perfect —
   almost no headroom for any model, so it cannot discriminate compression methods.
2. **H=10-step free-run forecast** (persistence fails over a horizon): base predictive FPS
   ≈ 0.05. A *linear* free-run map decays or diverges and cannot track real nonlinear dynamics
   over 10 steps, so it still barely beats the null (except worm 4, base ≈ 0.23).

## Honest conclusion
- **The linear data-driven readout is too weak to carry the Effect-B test.** With base FPS
  ≈ 0.05, there is essentially no function to preserve, so uniform vs engram margins are ≈ 0
  on 4/5 worms and slightly negative on the one worm with signal. This **does not** resolve the
  block — it shows the instrument is inadequate, not that Effect B is true or false.
- Importantly, it also does **not** reproduce the leaky-rate boundary. Combined with V4, the
  weight of evidence is that **Effect B is NOT a robust, substrate-independent result** — it
  appeared only under one hand-built model. We should not claim it.

## Decision / recommendation
- **Effect B remains unclaimed (treat as refuted-pending-stronger-evidence).** A proper test
  needs a *nonlinear* connectome-constrained model (e.g. a small GNN/RNN trained to forecast
  real activity) whose base predictive FPS is meaningfully above the persistence null — that is
  a multi-day modeling sub-project, not a quick readout swap, and is logged as future work.
- **Effect A (the quantization sparsity floor) stands** — it is dynamics-independent and does
  not need the activity readout. It is the paper-grade T1 result.
- Net for the program: build T1's contribution and the FPS "compression operation" asset on
  **Effect A only**. Real activity (Kato) is now wired in (`shared/activity.py`) and ready for
  the future nonlinear-model work.

## What is nonetheless banked
- A working real-activity loader (`shared/activity.py`) + the Kato dataset (56 MB, cached).
- A clear, evidence-based decision to drop the Effect-B claim rather than overclaim it.
- The persistence-null finding (smooth calcium ⇒ trivial 1-step prediction) is a useful
  methodological note for anyone scoring connectome models on this data.
