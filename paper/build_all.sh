#!/usr/bin/env bash
# Build every paper variant from the committed result artifacts, in one command.
# Requires: the project .venv (numpy/scipy/h5py/matplotlib) and `tectonic`.
# Run from the repo root:  bash paper/build_all.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
PY=".venv/bin/python"

echo "== [1/5] regenerating figures from result artifacts =="
"$PY" paper/make_figures.py
# propagate figures to every build dir
for d in paper-tmlr paper-arxiv paper-workshop; do
  [ -d "$d" ] && { mkdir -p "$d/figures"; cp paper/figures/*.pdf "$d/figures/"; }
done

echo "== [2/5] general build (paper/) =="
( cd paper && tectonic paper.tex >/dev/null )

echo "== [3/5] TMLR anonymous build (paper-tmlr/) =="
( cd paper-tmlr && tectonic paper.tex >/dev/null )

echo "== [4/5] arXiv de-anonymised build + source tarball (paper-arxiv/) =="
( cd paper-arxiv
  tectonic --keep-intermediates paper.tex >/dev/null
  rm -rf arxiv-src && mkdir -p arxiv-src/figures
  cp paper.tex paper.bbl tmlr.sty math_commands.tex arxiv-src/
  cp figures/*.pdf arxiv-src/figures/
  ( cd arxiv-src && tar czf ../arxiv-submission.tar.gz * )
)

echo "== [5/5] workshop build (paper-workshop/) if present =="
[ -f paper-workshop/paper.tex ] && ( cd paper-workshop && tectonic paper.tex >/dev/null ) || true

echo
echo "built PDFs:"
ls -1 paper/paper.pdf paper-tmlr/paper.pdf paper-arxiv/paper.pdf paper-workshop/paper.pdf 2>/dev/null || true
echo "arXiv upload bundle: paper-arxiv/arxiv-submission.tar.gz"
echo "done."
