# docs/ — understanding the paper in depth

Companion documentation for the preprint
*A Functional Preservation Score for Auditing Connectome Operations* (arXiv:2611.13681,
https://doi.org/10.48550/arXiv.2611.13681). These documents explain the fundamental principles,
the data, and the findings so a reader can understand the work beyond the paper itself, with every
number tied to a committed artifact.

## Read in this order
1. **`02-FUNDAMENTAL-PRINCIPLES.md`** — the concepts: the fidelity reframing, FPS and its null,
   connectome dynamics, the three operations (compression / alignment+transport / writing),
   Gromov–Wasserstein, the feasibility-mask limit, local-vs-global learning, and the statistics.
2. **`03-DATA-PRIMER.md`** — every dataset (C. elegans connectome, Kato-2015 calcium, DANDI-000044
   replay) with source, size, processing, role, and fetch commands.
3. **`04-FINDINGS-WALKTHROUGH.md`** — study-by-study results with the exact committed numbers,
   their artifacts, how to read them, and the methodological episodes that shaped them.
4. **`01-REVIEW.md`** — a referee-style assessment: claims vs evidence, strengths, weaknesses,
   threats to validity, and where a skeptical reader should push.

## Key pointers in the repo
- Metric + operations: `shared/` (fps, connectome, model, compress, stats) and per-track `src/`.
- Results: `tracks/*/results/*.json` (raw) and `*_stats.json` (CIs + p-values; the paper's numbers).
- Paper builds: `paper/` (general), `paper-tmlr/` (TMLR), `paper-arxiv/` (preprint), `paper-workshop/`.
- Full result index: `../RESULTS-INDEX.md`. Statistical audit: `../analysis/STATISTICAL-AUDIT.md`.

## One-line summary
Compression of neural data is measurable and bounded; migration of function across substrates is
not supported by the proposed partition→align→write pipeline, with the target substrate's own
wiring the recurring limit. All at nematode / small-network scale — coherence in simulation, not
biological feasibility.
