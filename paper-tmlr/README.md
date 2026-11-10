# TMLR submission package

TMLR-formatted version of the paper, reframed so the Functional Preservation Score (FPS) and the
connectome operations are the lead (ML-methods contribution; neuroscience as the application).

## Contents
- `paper.tex` — TMLR-formatted source (`\documentclass[10pt]{article}` + `\usepackage{tmlr}`).
- `paper.pdf` — built, 5 pages, anonymous (for review).
- `tmlr.sty`, `tmlr.bst`, `math_commands.tex` — **official** TMLR files (JmlrOrg), unmodified.
- `references.bib`, `figures/` — shared with the main paper.

## Anonymity (important for TMLR)
The default `\usepackage{tmlr}` renders the submission **anonymous** and adds the "under review"
header; authors are hidden by the style file. Do **not** modify the style file (grounds for
rejection). For a public preprint use `\usepackage[preprint]{tmlr}`; for the accepted
camera-ready use `\usepackage[accepted]{tmlr}` and fill in the author block.

## Build
Requires `tectonic` (fetches LaTeX packages automatically) and the figures (shared from the main
paper; regenerate with `.venv/bin/python paper/make_figures.py`).

```bash
cd paper-tmlr && tectonic paper.tex   # -> paper.pdf (runs bibtex; uses official tmlr.bst)
```

## Submission notes (see ../paper/TARGET-DECISION.md)
- Submit via OpenReview using this anonymous PDF.
- Single-paragraph abstract (required) — done.
- Provide an anonymised code/data repository link in the Reproducibility section before submitting.
- Keep authors hidden until acceptance; non-anonymous submissions are rejected without review.
