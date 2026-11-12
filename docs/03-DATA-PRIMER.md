# Data primer

Every dataset used in the paper: what it is, where it comes from, its size, how it is processed,
and which studies rely on it. Raw data is not committed (size/licensing); it is fetched by the
documented scripts and cached under `data/` (git-ignored). See the repo `DATASETS.md` for the
exact fetch commands.

---

## 1. C. elegans somatic connectome (structural)
- **Source:** White (1986) / Cook et al. (2019) somatic connectome via the OpenWorm
  ConnectomeToolbox. Fetch: `python scripts/fetch_celegans.py`.
- **Size/shape:** 306 neurons, 3,158 edges; 81 sensory, 95 interneuron, 130 motor. Chemical
  synapses directed; gap junctions symmetric at half weight. Integer synaptic weights
  (heavy-tailed — most edges small, a few large). Cached as `data/celegans_real.npz`.
- **Role:** the structural substrate for **T1** (compression), **T5** (partition separability),
  and **T2** (transport, with a perturbed copy as the second individual).
- **Why it matters:** it is the only whole, real connectome small enough to run the full
  pipeline (read → compress → align → simulate a write) deterministically on a laptop. The
  heavy-tailed integer weights are directly responsible for the T1 quantisation floor.

## 2. Kato et al. 2015 whole-brain calcium (functional activity)
- **Source:** OSF (`osf.io/na4f9`). Fetch: `curl -sL https://osf.io/na4f9/download -o data/kato2015_WT_NoStim.mat`.
- **Size/shape:** 5 worms, ~109–135 neurons each, ~3,000 frames at ~3 Hz; MATLAB v7.3 (HDF5).
- **Role:** real functional activity used to probe whether the engram-vs-uniform advantage holds
  on measured dynamics (the dropped "Effect B" check). A key finding here is methodological: slow
  calcium is so autocorrelated that a *persistence* baseline is near-ceiling, which is why that
  secondary claim was dropped rather than overstated.
- **Why it matters:** it is the honesty check that kept the paper from over-claiming the
  structured-compression advantage.

## 3. DANDI 000044 hippocampal replay (sequential activity)
- **Source:** Grosmark/Buzsáki (hc-11) via the DANDI archive, dandiset 000044, "Buddy" session.
  Fetch: `python scripts/fetch_dandi_replay.py` (streams **only** spike times + linearised
  position from the ~5 GB NWB using remfile; no full download).
- **Size/shape:** 48 pyramidal units + linearised track position; direction-split clean laps
  (≈26 laps in the analysed direction). Cached compactly as `data/hippocampus/dandi000044_buddy.npz`.
- **Role:** the substrate for **T3** (replay-sequence compression and the capacity/interference
  store). Sequences are place-ordered population rate matrices (units × time bins).
- **Why it matters:** real replay sequences are the concrete object the blueprint's "compressed
  backup" idea refers to; T3 measures how compressible they are while staying identifiable.
- **Also used:** a nelpy CA1 linear-track session (31 units) for the T3 structure gate (V1).

## 4. Synthetic / model substrates (T2 individual B, T4 host networks)
- **T2 "individual B":** a controlled-divergence perturbation of the real worm connectome — a
  known node permutation (ground-truth correspondence) plus a tunable fraction of rewired edges.
  This is a *divergence model*, not a second organism; it is what lets GW be scored against
  ground truth and the transport boundary be swept.
- **T4 host/target networks:** 40-neuron random recurrent rate networks with a fixed sparse
  topology; the "target function" is another such network. Small by design so the global-optimiser
  upper bound and many seeds are cheap.

## 5. Derived artifacts (what the paper's numbers come from)
- **Result JSONs** (`tracks/*/results/*.json`) — raw per-study outputs.
- **Statistically hardened JSONs** (`*_stats.json`) — bootstrap CIs, permutation p-values,
  effect sizes; these are the numbers quoted in the paper.
- **Figures** (`paper/figures/*.pdf`) — generated from the JSONs by `paper/make_figures.py`;
  nothing is recomputed at figure-build time.

## 6. Reproduction in brief
```bash
python -m venv .venv && .venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/fetch_celegans.py
.venv/bin/python scripts/fetch_dandi_replay.py
curl -sL https://osf.io/na4f9/download -o data/kato2015_WT_NoStim.mat
.venv/bin/python -m pytest -q          # substrate contract tests
# then the per-track experiment scripts in tracks/*/experiments/ regenerate the result JSONs
```
