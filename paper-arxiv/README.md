# arXiv preprint package

De-anonymised public-preprint build for arXiv, using the TMLR style file in `[preprint]` mode
(de-anonymises and removes the "under review" banner, as the TMLR style file intends). Same
content and numbers as the TMLR and general builds.

## Contents
- `paper.tex` — de-anonymised source (`\usepackage[preprint]{tmlr}`, real author block w/ placeholders).
- `paper.pdf` — built preview.
- `paper.bbl` — pre-compiled bibliography (REQUIRED in the arXiv upload; arXiv does not run BibTeX).
- `tmlr.sty`, `math_commands.tex` — official style files (unmodified).
- `references.bib`, `tmlr.bst` — kept for local rebuilds only; NOT uploaded to arXiv.
- `figures/` — the four figures.
- `arxiv-submission.tar.gz` — the self-contained source bundle to upload (verified to compile
  from a clean extraction).
- `ARXIV-METADATA.md` — title, authors, plain-text abstract, categories, license, comments.

## Build locally
```bash
cd paper-arxiv && tectonic paper.tex       # -> paper.pdf
```

## Repackage the upload tarball (after editing paper.tex, e.g. real authors)
```bash
cd paper-arxiv
tectonic --keep-intermediates paper.tex    # regenerates paper.bbl + paper.pdf
rm -rf arxiv-src && mkdir -p arxiv-src/figures
cp paper.tex paper.bbl tmlr.sty math_commands.tex arxiv-src/
cp figures/*.pdf arxiv-src/figures/
cd arxiv-src && tar czf ../arxiv-submission.tar.gz * && cd ..
```

## Why the .bbl is bundled (not the .bib)
arXiv compiles LaTeX from source but does not run BibTeX. Including the pre-built `paper.bbl`
makes the bibliography resolve without a BibTeX pass. The tarball deliberately omits
`references.bib` and `tmlr.bst`.

## Before uploading
1. Replace the author placeholders in `paper.tex`, rebuild, and repackage (steps above).
2. Fill the Authors field in `ARXIV-METADATA.md` to match.
3. Submit under a cs primary category (cs.NE or cs.LG); you are endorsed for cs, not q-bio, so
   q-bio.NC can only be an optional cross-list.
4. Choose a license (CC BY 4.0 recommended).
