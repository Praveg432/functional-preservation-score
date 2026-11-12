# Functional Preservation Score — Auditing Connectome Operations

**Preprint (live):** *A Functional Preservation Score for Auditing Connectome Operations:
Compression, Alignment, Transport, and Local-Rule Writing.*
arXiv:[2611.13681](https://arxiv.org/abs/2611.13681) · DOI [10.48550/arXiv.2611.13681](https://doi.org/10.48550/arXiv.2611.13681)

A measurement-first audit of the computational operations behind speculative "mind-migration"
pipelines. The project introduces the **Functional Preservation Score (FPS)** and applies it in
five pre-registered studies on the *C. elegans* connectome, whole-brain calcium activity, and
hippocampal replay. **One-line result:** compression of neural data is measurable and bounded,
while migration of function across substrates is not supported by the proposed
partition→align→write pipeline — with the target substrate's own wiring the recurring limit.
All at nematode / small-network scale: coherence in simulation, not biological feasibility.

**New reader? Start with [`docs/`](docs/README.md)** — fundamental principles, data primer,
findings walkthrough, and a referee-style review, with every number tied to a committed artifact.

**Status:** preprint live on arXiv; code, data loaders, result artifacts, and four paper build
variants released; statistically hardened (bootstrap CIs + permutation p-values).

> This repository began as a domain deep-dive and research scaffold for the blueprint "Radical
> Life Extension, Identity Quantization, and Mind Migration," then executed the feasible core and
> the surrogate attacks on its blocked stages. The history is preserved in `RESEARCH-LOG.md`.

---

## What this project is (and is not)

**Is:** an honest technical map of a highly speculative proposal — what is real today,
what is overstated in the source blueprint, what is pure hypothesis, and which pieces
are actually buildable as a thesis in the near term.

**Is not:** an endorsement that non-destructive human "mind migration" is achievable with
current or near-future tools. The deep-dive concludes it is **not**, and separates the
small, genuinely buildable in-silico core (connectome quantization + cross-graph behavioral
transfer on *public* connectomes) from the biologically unfounded end-to-end vision.

> **Honest scope up front.** Four of the five breakthroughs the blueprint cites are real
> but **mis-attributed, mis-described, or overstated** (see `scans/` and
> `analysis/REFERENCED-WORK-VETTING.md`). The two claims the whole architecture rests on —
> (1) a chronic *single-synapse-resolution* human read, and (2) a *write* that installs
> one person's identity into another differently-wired living brain — have **zero
> supporting evidence** at any scale in humans. Treat the end-to-end architecture as a
> thought experiment and the Phase-1 in-silico work as the only thesis-grade target.

---

## Repository layout

```
mind-migration-research/
├── README.md                         # this file — index + honest scope
├── METHODOLOGY.md                    # how claims were vetted + evidence standard
├── RESEARCH-LOG.md                   # dated log of what was checked and decided
├── NOVELTY-SCAN.md                   # solved vs. open; each track maps to an open question
├── DATASETS.md                       # public datasets + what the M4 Pro can actually run
├── MASTER-PLAN.md                    # feasible core + surrogate attacks; dependency map
├── inputs/
│   └── 00-source-blueprint.md        # the master blueprint, preserved verbatim as input
├── scans/                            # live literature verification of each referenced claim
│   ├── 01-synaptic-pruning-torpor.md
│   ├── 02-connectome-gnn-flywire.md
│   ├── 03-hippocampal-prosthetics-mimo.md
│   ├── 04-neural-interfaces-bisc.md
│   └── 05-optogenetics-and-ot-alignment.md
├── analysis/
│   ├── DOMAIN-PRIMER.md              # the actual neuroscience/ML background, plainly stated
│   ├── REFERENCED-WORK-VETTING.md    # claim-by-claim: real / overstated / mis-cited
│   ├── ARCHITECTURE-DECOMPOSITION.md # the pipeline broken into verifiable sub-claims
│   ├── FEASIBILITY-RISK-LEDGER.md    # load-bearing assumptions + kill-criteria
│   ├── RECOMMENDATION.md             # what to actually build; the thesis-grade residual
│   ├── IMPACT-AND-EXTENSIBILITY.md   # per-track + aggregate impact; honest probability read
│   └── IMPACT-STRATEGY.md            # realistic-but-stubborn path to the actual end goal
└── tracks/                           # 5 scaffolded tracks (each: TRACK.md + 00/04 + vetting/)
    ├── T1-structured-connectome-compression/   # CORE — engram-aware compress (open Q N1)
    ├── T2-functional-transport-alignment/       # CORE — GW align + functional transport (N2, risk B1)
    ├── T3-replay-latent-compression/            # CORE — replay→latent compression frontier (N3)
    ├── T4-insilico-write-compiler/              # SURROGATE — the write, in simulation (N4, risk A3)
    └── T5-partition-separability/               # SURROGATE — Base-OS/payload split tested (N5, risk B2)
```

## Consolidated output

- **`paper/PAPER.md`** — the full consolidated, submission-ready paper (abstract → methods →
  five studies → discussion/limitations/ethics → reproducibility), every number traceable to a
  committed result artifact (see its Appendix A and `RESULTS-INDEX.md`).
- **`paper/COVER-LETTER.md`** — review-submission cover letter.
- **`paper/SUBMISSION-VENUES.md`** — recommended venues and a staged submission plan.
- **`paper/paper.pdf`** — the built 7-page paper (LaTeX source `paper.tex`, bib `references.bib`,
  figures generated from result artifacts by `paper/make_figures.py`). See `paper/README.md` to rebuild.
- **`paper/TARGET-DECISION.md`** — primary venue decision (TMLR) + staged submission plan.
- **`paper-tmlr/paper.pdf`** — the TMLR-formatted, anonymous 5-page version (official `tmlr.sty`,
  ML-methods framing). See `paper-tmlr/README.md`.
- **`paper-arxiv/`** — de-anonymised arXiv preprint: `paper.pdf`, source `paper.tex`, the upload
  bundle `arxiv-submission.tar.gz` (verified to compile standalone), and `ARXIV-METADATA.md`
  (categories q-bio.NC + cs.LG, plain-text abstract, license). See `paper-arxiv/README.md`.
- **`paper-workshop/paper.pdf`** — condensed 4-page version for the NeurIPS ICBINB-bio workshop
  (swap in the official NeurIPS style before submitting).
- **`paper/SUBMISSION-GUIDE.md`** — master step-by-step for every venue (+ dual-submission warning).
- **`paper/VENUE-FIELDS.md`** — copy-paste field sheets per venue.
- **`paper/build_all.sh`** — one command to rebuild every variant + the arXiv tarball.
- **`analysis/SURROGATE-CHAIN-SYNTHESIS.md`** — the T5→T2→T4 corrective, synthesized.

## Where to start

1. `MASTER-PLAN.md` — the full plan: feasible core + surrogate attacks + dependency map.
2. `analysis/RECOMMENDATION.md` — the bottom line: what is buildable and what to drop.
3. `NOVELTY-SCAN.md` — solved vs. open, so no track rebuilds something already done.
4. `DATASETS.md` — the public datasets and what an M4 Pro can actually run.
5. `analysis/REFERENCED-WORK-VETTING.md` — the claim-by-claim reality check.
6. `inputs/00-source-blueprint.md` — the original proposal, preserved.

## The five tracks at a glance

- **T1–T3 (feasible core):** buildable now on public connectomes with an M4 Pro. Each yields
  a standalone capability/boundary result (compression limits, functional alignment transport,
  replay-compression frontier).
- **T4–T5 (surrogate):** honest in-silico attacks on the two blocked biological steps (the
  write; the Base-OS/payload partition). They test whether the blocked step is *coherent in
  simulation* and map where it fails — explicitly **not** a claim of biological feasibility.
- Sequencing and gates: see `MASTER-PLAN.md`. Start with T1 + T3 (lowest risk), then the
  surrogate chain T5 → T2 → T4, stopping at the first failed vetting gate and reporting it.

## Data availability

Raw datasets are not committed (size/licensing); they are fetched via documented scripts/URLs and
cached under `data/` (git-ignored):
- C. elegans connectome: `python scripts/fetch_celegans.py` (OpenWorm ConnectomeToolbox).
- Whole-brain calcium (Kato 2015): `curl -sL https://osf.io/na4f9/download -o data/kato2015_WT_NoStim.mat`.
- Hippocampal replay (DANDI 000044): `python scripts/fetch_dandi_replay.py` (streams from the NWB).
- Linear-track session (nelpy): `data/hippocampus/` via the nelpy example-data URLs in `DATASETS.md`.

All committed result artifacts (`tracks/*/results/*.json`) were produced from these sources by the
scripts indexed in `RESULTS-INDEX.md`; the pipeline recomputes nothing at figure-build time.

## License
Code: MIT (`LICENSE`). Paper text and figures: CC BY 4.0. See `LICENSE` for scope.

## Evidence standard

Every external claim carries an inline source and is marked **REAL**, **OVERSTATED**,
**MIS-CITED/MIS-DESCRIBED**, or **[UNVERIFIED]**. Source content is rephrased for
licensing compliance. Numbers from the blueprint that could not be grounded are flagged
rather than repeated as fact. See `METHODOLOGY.md`.
