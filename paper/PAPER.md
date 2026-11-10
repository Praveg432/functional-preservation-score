# What Survives Compression and What Does Not: An In-Silico Audit of Connectome-Based Mind-Migration Proposals Using a Functional Preservation Score

**Status:** preprint draft prepared for review. Every quantitative claim maps to a committed
result artifact (`tracks/*/results/*.json`); see §9.

---

## Abstract

Speculative proposals for "mind migration" describe reading a brain's identity, compressing it,
and installing it into a new substrate. Such proposals assemble several active research areas
(connectomics, graph neural networks, memory prosthetics, neural interfaces, optogenetics) into a
single pipeline, typically relying on the most optimistic reading of each. We examine the
computational core of this pipeline directly, using an auditable procedure on public data that
runs on a single laptop. The study is organised around a Functional Preservation Score (FPS): a
null-normalised, behaviourally grounded measure of how much of a neural system's input–output
function survives an operation such as compression, alignment, transport, or writing. We apply
FPS across five pre-registered studies on the *C. elegans* connectome, whole-brain calcium
activity (Kato et al., 2015), and hippocampal replay (DANDI 000044).

Two of the studies yield positive characterisations and three form a negative result. First,
low-bit quantisation of a real connectome runs into a structure-dependent sparsity floor: uniform
int4/ternary quantisation is forced to roughly 73%/98% effective sparsity because the
heavy-tailed integer synaptic weights round to zero, whereas mixed-precision protection of hub
neurons lowers these floors to about 27%/32%. Second, decoded hippocampal replay sequences
compress heavily while remaining identifiable: a 48-unit × 25-bin sequence (~38 kbit) stays
identifiable at a cross-validated top-1 accuracy of 0.69 (95% CI [0.63, 0.74]; chance 0.125;
permutation p < 10⁻³) from latents on the order of 10–50 bits per event, and a bounded
"background-sync" store shows a graceful-versus-cliff trade-off between capacity and
interference. Third, the migration pipeline fails in simulation at each stage, for reasons that
are largely independent. The putative "identity payload" is not a functionally separable module
(it is no more disruptive to ablate than a random interneuron subset of the same size;
permutation p ≥ 0.16 at every tested size). Cross-individual functional transport collapses once
the target's actual wiring is respected (fidelity falls from 1.00 to 0.40, 95% CI [0.31, 0.49],
p < 10⁻³) or the alignment is imperfect (fidelity 0.06, 95% CI [0.00, 0.13]). And the proposed
biologically plausible write mechanism (reward- or ripple-gated local plasticity) cannot reach the
function that the target topology provably admits (plausibility gap 0.45, 95% CI [0.27, 0.64],
p < 10⁻³, Cohen's d = 2.0), with ripple timing providing no measurable benefit (the
ripple-minus-continuous difference has a CI that includes zero).

Taken together, the results indicate that compression of neural data is a real and quantifiable
phenomenon, while migration of function across substrates is not supported by the proposed
pipeline on the systems we can currently test. We release FPS, the dataset loaders, and the full
set of operations as a measurement toolkit.

**Scope.** All results are obtained on a 306-neuron nematode connectome, small recurrent
networks, and reflex- or trajectory-scale functions. They say nothing about reading or writing a
living human brain. The biological prerequisites for the full pipeline — non-destructive
synaptic-resolution reading, identity-scale writing, and cross-subject transfer — remain absent,
and we make no claim about them. The studies test whether each stage is coherent in simulation,
not whether it is biologically feasible.

---

## 1. Introduction

A recurring theme in recent discussions of biological aging is to treat it as a reversible
information-processing problem. Mind migration is one speculative endpoint of that view. In the
version we examine, a brain is partitioned into a regenerable "Base-OS" (autonomic, sensory, and
motor circuitry) and a transferable "identity payload" (association cortex and hippocampus); the
payload is then compressed through sparsification and low-bit quantisation, aligned to a
differently wired target brain, and installed through activity-dependent plasticity. Each of
these steps draws on a real experimental result, but the composition has never been tested as a
whole, and several of the links have no supporting evidence at any scale.

We do not attempt the biological pipeline, which is infeasible with current or foreseeable tools.
Instead we treat preservation of function as a measurable quantity and ask which stages of the
computational pipeline can actually be built, and where and why the remaining ones fail. Posing
the question this way turns an otherwise unfalsifiable goal into a measurement problem that admits
decision-relevant evidence from public data on ordinary hardware.

The paper makes five contributions. (1) We define FPS, a substrate-agnostic measure of functional
preservation with an explicit trivial-baseline null (§3.1). (2) We characterise compression of a
real connectome and identify a quantisation sparsity floor, together with the limits of
structured sparsification (§4). (3) We characterise the compressibility of real hippocampal replay
sequences and describe a capacity–interference relationship for bounded incremental storage (§5).
(4) We provide a three-stage in-silico test of the partition–align–write pipeline (separability,
functional transport, local-rule writing) and locate the failure mode at each stage (§6). (5) We
release a reproducible, laptop-scale toolkit comprising the metric, the data loaders, and the
operations (§9).

---

## 2. Related work and claim provenance

We checked the frontier results that the pipeline depends on against their primary sources. Most
are genuine, but several are mis-attributed or overstated in popular accounts; the full audit is
given in `analysis/REFERENCED-WORK-VETTING.md`, and we summarise the relevant points here.

On synaptic turnover and memory, torpor is known to shed roughly 50–65% of synapses with memory
preserved (von der Ohe et al., *J. Neurosci.*, 2006/07, with more recent artificial-hibernation
work on engram resilience, 2025–26). This supports sparsification that is structured rather than
uniform low-bit removal. On connectome-driven models, FlyWire (Nature, 2024) and flyGNN (NeurIPS,
2025) show that a connectome can drive simulated behaviour, but only once the dynamical
parameters are fitted; the topology alone does not suffice. On memory prosthetics, the USC and
Wake Forest multi-input multi-output devices improved human recall by about 35–37% (Hampson et
al., 2018), but this is restoration within a single subject rather than transfer of identity
between subjects. On neural interfaces, high-density wireless arrays (Columbia, 65,536
electrodes, *Nat. Electron.*, 2025) record from the subdural surface (µECoG); they do not read at
synaptic resolution. On alignment, Gromov–Wasserstein optimal transport aligns brains at the
scale of functional parcels (Thual et al.; Xu et al.), but it is NP-hard and has not been tested
for functional transport on connectomes.

Generic graph-network pruning and quantisation (e.g. arXiv:2510.22058) and scalable
Gromov–Wasserstein (S-GWL; HOT) are established methods. What is new here is their composition on
connectome substrates under a functional, behaviourally grounded metric, together with the
explicit test of the migration stages that have no empirical basis.

---

## 3. Methods

### 3.1 Functional Preservation Score (FPS)

Let a system map a fixed battery of stimuli to outputs. For a reference system with outputs
`Y_ref` and a transformed system with outputs `Y`, define an R²-style fit
`raw(Y) = 1 − ‖Y − Y_ref‖² / ‖Y_ref − mean(Y_ref)‖²`. The score is normalized by the **best
trivial baseline** — the maximum of a shuffled-stimulus–response mapping and a predict-the-mean
predictor:

```
FPS = clip( (raw(Y) − raw(Y_null)) / (1 − raw(Y_null)), 0, 1 )
```

An FPS of 1 means the transformed system reproduces the reference function; an FPS of 0 means it
performs no better than the best trivial control. Normalising by the null is important in
practice, because without it a system that always produces a plausible-looking but
input-independent output can score deceptively well; we encountered exactly this problem and
corrected for it (§5.2, §7). For identity-style tasks we also use identification accuracy, which
asks whether reconstruction *i* is nearest to its own original among all events. This measure is
bounded and has an exact chance level of 1/*n*.

### 3.2 Substrates and data

- **C. elegans connectome (real).** White/Cook somatic connectome via the OpenWorm
  ConnectomeToolbox: 306 neurons, 3,158 edges, 81 sensory / 95 interneuron / 130 motor; chemical
  synapses directed, gap junctions symmetric at half weight. Dynamics: leaky-rate tanh recurrent
  model reading out motor neurons over a fixed low-pass stimulus battery.
- **Whole-brain calcium (real).** Kato et al. 2015 *WT_NoStim* (OSF): 5 worms, ~109–135 neurons,
  ~3,000 frames at ~3 Hz.
- **Hippocampal replay (real).** DANDI 000044 (Grosmark/Buzsáki, hc-11), Buddy session:
  48 pyramidal units + linearized position, streamed (spike times + position only) from a 5 GB
  NWB without full download; and a nelpy CA1 linear-track session (31 units) for the V1 gate.

### 3.3 Operations (released as a toolkit)

- **Compression.** Magnitude pruning (uniform) vs. engram-aware pruning (protect top-degree /
  betweenness / k-core hubs); symmetric quantization to int8/int4/ternary; mixed-precision
  (hubs at higher bit-depth). Policies compared at **matched total effective sparsity**.
- **Alignment/transport.** Self-contained entropic Gromov–Wasserstein (square loss + Sinkhorn
  projection); weight transport through a node correspondence with a Peters'-rule *feasibility
  mask* (write only edges the target supports); FPS function test on the target.
- **Write.** Fixed-topology rate host; strictly local plasticity (three-factor reward-modulated
  Hebbian + optional ripple gating; audited: no backprop, no per-weight target gradient);
  a global least-squares optimizer as the upper-bound ceiling.

### 3.4 Statistical methods

All headline numbers are reported as point estimate with a **percentile bootstrap 95% CI**
(10,000 resamples) over the relevant randomization (stimulus seeds, model seeds, perturbation
realizations, or cross-validation splits), with the sample size *n* stated. Comparisons carry a
**one-sided permutation test** (10,000 permutations; add-one-corrected p-value) and, where
applicable, **Cohen's d** as an effect size. Nulls are explicit: for identification, a
label-permutation distribution; for separability, 500 random equal-size interneuron subsets; for
the FPS metric, the best trivial baseline (shuffle ∨ mean). To avoid selection bias we report a
**pre-registered primary** engram policy (strength) rather than the maximum over policy
variants, and avoid single-best-cell "floors" in favor of monotone criteria. The T3
identification frontier uses **repeated cross-validation (30 random train/test splits)** with the
autoencoder fit on training data only (no leakage; verified by code audit). Full audit and
remediation: `analysis/STATISTICAL-AUDIT.md`; hardened artifacts: `tracks/*/results/*_stats.json`.

### 3.5 Experimental discipline (pre-registration and gates)

Each study is organized as go/no-go gates with thresholds fixed before running. We adopted four
rules after early overclaims: (i) validate on real data, not only synthetic; (ii) verify the
instrument has headroom over its trivial null *before* trusting any comparison; (iii) diagnose a
failing result's cause before modifying anything, and change an instrument at most once per
diagnosis; (iv) report honest negatives rather than threshold-shopping. Instances where these
rules changed conclusions are documented in §7.

---

## 4. Study 1 — Connectome compression (T1)

This study asks how far a connectome-driven model can be compressed, along the axes of sparsity,
bit depth, and structure, before its function collapses, and whether biologically motivated
structured sparsification outperforms uniform pruning. We load the real connectome as the
recurrent model, compress it under either a uniform or an engram-aware policy at matched total
effective sparsity, and score the motor-readout FPS against the intact network. We sweep bit
depth over {int8, int4, ternary} and use three engram definitions and several stimulus seeds. To
check that the findings are not an artefact of the dynamics, we repeat the key comparison with an
independent sigmoid-conductance model.

At matched effective sparsity under int4, using the pre-registered primary policy (strength) and
eight stimulus seeds, the engram-aware policy preserves function better than uniform pruning: FPS
of 0.30 (95% CI [0.12, 0.48]) versus 0.03 ([0.00, 0.09]) at target sparsity 0.5 (p = 0.015,
d = 1.3), 0.31 versus 0.03 at 0.6 (p = 0.012, d = 1.4), and 0.20 versus 0.03 at 0.7 (p = 0.031,
d = 1.0) (`T1_v3_stats.json`). The confidence intervals are wide at n = 8, but the comparison is
significant because uniform pruning sits near its floor.

That floor is the central finding. Uniform quantisation cannot reach low sparsity on the real
connectome, because the heavy-tailed integer weights round to zero: the effective-sparsity floor
is 0.73 for int4 and 0.98 for ternary under uniform quantisation, against 0.27 and 0.32 under
engram-aware mixed precision. At int8 there is no floor, and the advantage of the engram policy
is negligible (`T1_v3_real.json`). These floors are deterministic properties of the weight
distribution rather than statistical estimates.

The structured advantage, by contrast, is not robust. In a clean matched-sparsity comparison at
int8, it depends on regime (uniform wins below about 0.4 sparsity, engram wins above it) and does
not reproduce under the independent sigmoid-conductance model. We therefore treat the floor as
the robust result and drop the broader claim that structured compression is universally superior
(`T1_v4_real.json`; see §7). The usable conclusion is narrow but solid: uniform low-bit
quantisation of a real integer-weighted connectome has a severe and measurable over-sparsification
floor that mixed-precision hub protection can lower.

---

## 5. Study 2 — Replay-sequence compression (T3)

This study asks whether decoded hippocampal replay sequences can be compressed to a small number
of bits while preserving their represented content, and whether a bounded incremental store shows
a capacity limit.

### 5.1 Structure exists (V1)
Place-ordered run-epoch population sequences carry decodable trajectory structure. The Bayesian
decode score is 0.34, against a time-shuffled null of 0.20, across 62 sequences (`T3_v1.json`).
This establishes that there is real sequential content for the compression stage to act on.

### 5.2 Compression–identifiability frontier (V2)
We score reconstructions with identification accuracy (chance 1/*n*) under 30-split repeated
cross-validation, with the autoencoder fit on the training split only. The uncompressed
autoencoder identifies held-out replay events at a top-1 accuracy of 0.69 (95% CI [0.63, 0.74])
against a chance level of 0.125 (permutation p = 10⁻⁴) (`T3_v2_stats.json`). Identification rises
with the latent bit budget and degrades gradually, with non-overlapping confidence intervals: at
latent dimension 16, accuracy is 0.69 ([0.63, 0.74]) at 128 bits per event and 0.58 ([0.53, 0.64])
at 32; at dimension 8, it is 0.40 ([0.35, 0.45]) at 16 bits per event; and at dimension 4, it is
0.28 ([0.24, 0.32]) at 8 bits per event. A 48 × 25 sequence (about 38 kbit in raw form) therefore
remains well above chance down to roughly 8–16 bits per event, a compression ratio on the order
of 10³. For reference, a single train/test split gave 0.75, so cross-validation lowers the
estimate somewhat. We note that an earlier trajectory-rank fidelity measure was abandoned once we
found its null to be structurally high; identification accuracy is its replacement (§7).

### 5.3 Capacity and interference (V3)
We then stream events into a fixed-size store (`T3_v3.json`). A superposition (holographic) store
degrades gradually and monotonically, with recovery falling from 1.00 to 0.50 to 0.30 as the load
rises from 2 to 10 to 20. A slot store, by contrast, is perfect up to its capacity (10 slots) and
then drops sharply (0.67 at a load of 15, 0.50 at 20, approximately slots divided by load). Under
random-key binding the oldest events are not preferentially lost. The two architectures therefore
trade capacity against interference in different ways, but both exhibit a genuine limit.

The practical reading is modest. These results show that the idea of a compressed replay backup
is plausible in an information-theoretic sense, as compression of decoded sequences. They do not
show that such a backup contains a memory, let alone a person.

---

## 6. Study 3 — The migration pathway, in-silico (T5 → T2 → T4)

Each of the three stages is a surrogate test of a biological stage for which no direct evidence
exists; the question in each case is whether the stage is coherent in simulation on the nearest
testable substrate.

### 6.1 Partition separability (T5)
We ask whether the putative "identity payload" is a functionally separable module. Holding the
sensory and motor interface fixed (an earlier version that ablated it was degenerate, as noted in
§7), we test whether ablating the asserted interneuron payload degrades the input–output
transformation more than ablating a random interneuron subset of the same size. It does not.
Against a 500-sample null of random equal-size interneuron subsets, the asserted payload is not
significantly more disruptive to ablate at any tested size (permutation p = 0.17, 0.16, 0.27, and
0.37 at payload fractions of 0.1, 0.2, 0.3, and 0.4; z ≈ +0.9 to +1.4) (`T5_v2_stats.json`). We
find no significantly separable identity module; the function is distributed across the
interneuron population.

### 6.2 Functional transport via Gromov–Wasserstein (T2)
We generate "individual B" as a controlled-divergence perturbation of A, in which a known node
permutation provides the ground-truth correspondence and a fraction of edges is rewired. The
alignment itself works well: entropic Gromov–Wasserstein recovers 92% of the ground-truth
correspondence at zero divergence (chance 0.3%, single realisation) and 0.76 (95% CI [0.74, 0.78])
at 5% rewiring, averaged over eight independent realisations of B (`T2_v1.json`,
`T2_v2_stats.json`).

The transport, however, does not survive realistic conditions (`T2_v2_stats.json`, eight seeds at
5% divergence). Given an oracle correspondence and unconstrained writing, fidelity is 1.00 (95% CI
[1.00, 1.00]). Once we require the transported weights to respect the target's actual wiring (the
feasibility mask), fidelity collapses to 0.40 (95% CI [0.31, 0.49]; p = 3×10⁻⁴). Using the
GW-estimated correspondence instead of the oracle, fidelity is 0.06 (95% CI [0.00, 0.13];
p = 2×10⁻⁴). High correspondence accuracy does not imply preserved function: the binding
constraint is the target's own wiring.

### 6.3 Local-rule write-compiler (T4)
We ask whether biologically plausible local plasticity can install a target function into a fixed
foreign topology. Across ten seeds at zero divergence (`T4_v2_stats.json`), a global optimiser
reaches a ceiling of 1.00 (95% CI [1.00, 1.00]), confirming that the topology can host the
function. Strictly local reward-modulated plasticity reaches only 0.55 (95% CI [0.36, 0.73]),
leaving a plausibility gap of 0.45 (95% CI [0.27, 0.64]; permutation p = 10⁻⁴, Cohen's d = 2.0).
Ripple-timed gating confers no advantage: the difference between ripple-timed and continuous
plasticity is −0.000 (95% CI [−0.003, +0.002]), a CI that includes zero. The global ceiling
itself falls with divergence (from 1.00 to 0.88; `T4_v2.json`), which again reflects the
feasibility limit identified in §6.2. Local fidelity varies considerably across seeds, which is
why the confidence interval is wide; this variability is itself informative, since it means the
mechanism is unreliable even in the cases where it occasionally succeeds.

### 6.4 The three stages together
The three stages fail for reasons that are largely independent and that compound. There is no
clean module to extract (T5); even the whole graph cannot be placed once alignment is imperfect
and the target's wiring is respected (T2); and even where the topology can host the function, the
proposed write mechanism cannot reach it (T4). One constraint, the target substrate's own wiring,
recurs as the binding limit in both T2 and T4. The original proposal assumes this constraint away
at each stage.

---

## 7. Methodological episodes that changed conclusions

Several of our conclusions were revised once we understood a measurement problem, and we record
these cases because they bear on how the final numbers should be read.

The FPS null was hardened after we found that a constant-output system could beat a shuffle-only
null; we redefined the null as the better of a shuffled mapping and a predict-the-mean baseline.
In Study 1 we found a matched-budget error in which ties among the real integer weights caused
uniform pruning to over-remove edges; we fixed this with deterministic tie-breaking so that the
two policies are compared at identical budgets. Also in Study 1, an earlier "structured beats
uniform" claim did not survive a cheap nonlinear reservoir test, which showed that short-horizon
forecasting of slow calcium cannot beat a persistence baseline even for a model that genuinely
learns; we dropped the claim rather than tune a threshold to keep it. In Study 2 we replaced a
trajectory-rank fidelity measure, whose null was structurally high, with the bounded
identification-accuracy measure. In Study 3 (separability) an initial definition that ablated the
sensory and motor neurons trivially drove FPS to zero for every partition, because it removed the
input and readout the metric depends on; we reformulated the test around a fixed input–output
interface. In each case the change was made once, following an explicit diagnosis, and the
earlier (incorrect) result is retained in the project record.

---

## 8. Discussion, limitations, and ethics

The computational core of the pipeline separates into two parts. Compression of neural data is
real, measurable, and bounded (Studies 1 and 2). Migration of function across substrates is not
supported by the proposed partition–align–write pipeline (Study 3). The recurring obstacle is the
target substrate's wiring: a function cannot be transported into, or written onto, a substrate
that is not wired to support it. The original proposal does not account for this at any stage.

Several limitations qualify these conclusions, and they matter. The work is conducted at small
scale: a 306-neuron connectome, activity recordings of at most 135 neurons, and 40-neuron
recurrent networks, with functions at the reflex or trajectory level. Generalisation to
mammalian cortex is untested here. The dynamics are simple rate or leaky-integrator models;
richer biophysical models could shift the exact numbers, though we expect the qualitative pattern
across the three stages to hold, and a more expressive plasticity rule could narrow the gap in
Study 3. Some test sets are small (for instance, about eight laps per direction in Study 2), so
we report frontiers as regions rather than precise floors. The second individual in Study 2 is a
divergence model built from a single real connectome, not a second organism. Finally, FPS is a
functional measure; it is not a claim about subjective experience or personal identity.

The biological prerequisites for the full pipeline are absent. Non-destructive
synaptic-resolution reading of a living brain, identity-scale writing, and cross-subject transfer
have no supporting evidence at any scale, and we do not address them. The surrogate studies
concern only coherence in simulation.

All of the work is computational and uses public animal datasets. It involves no human subjects,
no wet-lab experiments, and no organoid or cloning work. We have been careful not to imply that
human mind migration is feasible; the contribution is a bound on where the idea breaks.
Questions about the continuity of personal identity are philosophical and fall outside the scope
of this paper.

---

## 9. Reproducibility

All results are deterministic and run on a laptop (Apple M4 class) with a Python venv
(numpy, scipy, torch, h5py; optional remfile for DANDI streaming). Each claim maps to a committed
JSON under `tracks/*/results/` and the script that produced it (indexed in `RESULTS-INDEX.md`).
Data are fetched via documented scripts (`scripts/fetch_celegans.py`, OSF/DANDI URLs); large
files are not committed. The FPS metric, dataset loaders, and all operations (compression,
GW alignment, transport, local-rule write, sync store) are released as `shared/` plus per-track
`src/` modules. A test suite (`pytest`) covers the substrate contracts.

---

## 10. Conclusion

Treating mind migration as a measurement problem gives a reasonably clear answer. Compression of
neural data, whether of connectome weights or of replay sequences, is a measurable phenomenon
with quantifiable floors and capacity limits. Migration of function across substrates, as
described by the partition–align–write pipeline, does not hold up in simulation: it fails at the
partition, transport, and write stages, and the target substrate's own wiring is the limit common
to the last two. We offer these results as a more precise map of a speculative area, along with a
reusable measurement toolkit. More generally, in a field where claims are easy to make and hard
to test, a careful account of where and why an idea breaks is worth reporting in its own right.

---

## Appendix A — Result artifact index (selected)

Primary (point-estimate) artifacts and their statistically-hardened counterparts (`*_stats.json`,
with bootstrap CIs and permutation p-values; see `analysis/STATISTICAL-AUDIT.md`).

| Claim | Primary artifact | Hardened artifact |
|---|---|---|
| Engram advantage at matched int4 sparsity (p≈0.01–0.03, d≈1.0–1.4) | `T1_v2b_real.json` | `T1_v3_stats.json` |
| Quantization floors int4 0.73 / ternary 0.98 (uniform) vs 0.27 / 0.32 (engram) — deterministic | `T1_v3_real.json` | `T1_v3_stats.json` |
| Effect-B dynamics non-robustness (dropped claim) | `T1_v4_real.json` | — |
| Replay structure 0.34 vs null 0.20 | `T3_v1.json` | — |
| Identification CV 0.69 [0.63,0.74] vs chance 0.125, p=10⁻⁴; bits/event frontier w/ CIs | `T3_v2.json` | `T3_v2_stats.json` |
| Capacity/interference curves | `T3_v3.json` | — |
| No significantly separable payload (p≥0.16, 500-sample null) | `T5_v2.json` | `T5_v2_stats.json` |
| GW corr 0.76 [0.74,0.78] @5%; transport 1.00→0.40 [0.31,0.49] (p=3e-4) / →0.06 (p=2e-4) | `T2_v2.json` | `T2_v2_stats.json` |
| Write plausibility gap 0.45 [0.27,0.64], p=10⁻⁴, d=2.0; ripple Δ CI∋0 | `T4_v2.json` | `T4_v2_stats.json` |
