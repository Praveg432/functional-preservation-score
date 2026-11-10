# Paper package

Submission-ready artifacts for the connectome mind-migration audit paper.

## Contents
- `paper.pdf` — the built paper (7 pages, figures embedded). Primary artifact.
- `paper.tex` — LaTeX source (single-column article; natbib + plainnat).
- `references.bib` — bibliography (verified in the related-work audit).
- `PAPER.md` — the Markdown version (same content, for quick reading / diffs).
- `make_figures.py` — regenerates `figures/*.pdf` from committed result JSONs.
- `figures/` — the four figures (also `.png` copies).
- `COVER-LETTER.md` — review-submission cover letter.
- `SUBMISSION-VENUES.md` — recommended venues and staged submission plan.

## Rebuild from scratch
Requires the project `.venv` (numpy, scipy, h5py, matplotlib) and `tectonic` (self-contained
LaTeX; auto-fetches packages). From the repo root:

```bash
.venv/bin/python paper/make_figures.py      # figures from tracks/*/results/*.json
cd paper && tectonic paper.tex               # -> paper.pdf (runs bibtex automatically)
```

All figures are generated from committed result artifacts; the paper recomputes nothing. Every
quantitative value in the text maps to an artifact listed in `../RESULTS-INDEX.md` and
Appendix A, with statistically hardened counterparts (`tracks/*/results/*_stats.json`).
