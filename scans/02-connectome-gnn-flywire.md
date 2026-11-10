# Scan 02 — Whole-Brain Connectomic GNNs (FlyWire)

**Blueprint claim.** "Eon Systems / FlyWire, 2026" converted the complete EM connectome of a
*Drosophila* brain into a PyTorch GNN, proving raw anatomical graphs drive motor behavior in
simulated bodies.

**Verdict: REAL capability; attribution partly [UNVERIFIED]; one technical nuance.**

## What the literature actually shows

- **The connectome exists.** FlyWire published the first full wiring diagram of an adult
  *Drosophila* brain — ~139,255 proofread neurons — in *Nature* (Oct 2024).
  [FlyWire](https://flywire.ai/) · [Nature](https://www.nature.com/immersive/d42859-024-00053-4/)
- **A connectome-GNN that drives a body exists.** *flyGNN* (NeurIPS 2025) implements the
  FlyWire connectome as a recurrent message-passing network and uses it to control a
  physics-based fruit-fly model (whole-body locomotion).
  [NeurIPS 2025](https://neurips.cc/virtual/2025/131402)
- **An embodied simulation exists.** A 138,639-neuron whole-brain spiking simulation (FlyWire
  v783) has been placed in a biomechanical body (NeuroMechFly v2 / MuJoCo) showing vision,
  olfaction, locomotion, and escape behaviors.
  [repo](https://github.com/erojasoficial-byte/fly-brain)
- **It also runs on neuromorphic hardware.** The full FlyWire connectome (~140K neurons, ~50M
  synapses) has been mapped onto 12 Intel Loihi-2 chips, orders of magnitude faster than
  conventional simulation. [arXiv 2508.16792](https://arxiv.org/html/2508.16792v1)

## Technical nuance the blueprint glosses

The connectome gives **topology only** (who connects to whom). It does **not** give synaptic
weights, signs, or time constants. In the work above, the topology is *fixed from the
connectome* while the unknown dynamical parameters are **optimized** to match recorded
activity or to produce behavior (e.g. the OpenReview whole-brain network optimizes weights
and cellular time constants to match in-vivo resting activity,
[OpenReview](https://openreview.net/pdf?id=wCBNxp1qWe)). So the honest statement is:
*the anatomical graph is a strong scaffold, but function requires fitting parameters the
connectome does not contain.* "Raw anatomical graph drives behavior" overstates it.

## Bearing on the blueprint

- **Supports:** the Phase-1 premise that a connectome can be loaded as a PyTorch graph and
  made to drive behavior in a simulated body — this is the single most *buildable* part of
  the whole proposal, and public data + code exist.
- **Caveat:** "Eon Systems" as the author is **[UNVERIFIED]**; the real anchors are FlyWire
  (data), flyGNN/NeuroMechFly (embodiment), and the Loihi-2 team (hardware). Use those.
- **Caveat:** behavioral transfer across *perturbed/differently-wired* graphs (the actual
  thesis question) is **not** demonstrated by these papers — they model one fixed connectome.
  That gap is exactly what a Phase-1 thesis would test.

*Content rephrased from sources for licensing compliance.*
