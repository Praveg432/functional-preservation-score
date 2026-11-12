# arXiv submission metadata

> **POSTED:** arXiv:2611.13681 — https://doi.org/10.48550/arXiv.2611.13681 (live).
> The fields below record what was submitted.

Copy these fields into the arXiv submission form. The abstract is given as plain text (arXiv's
abstract field does not render LaTeX macros; keep plain ASCII / simple math).

## Title
A Functional Preservation Score for Auditing Connectome Operations: Compression, Alignment,
Transport, and Local-Rule Writing

## Authors
Praveg Vashishtha
Affiliation: Department of Computer Science and Engineering, Indian Institute of Technology
Patna, India; and Sopra Banking Software India.
Email: praveg_pa2503mth259@iitp.ac.in

## Primary category
cs.NE (Neural and Evolutionary Computing)
   Rationale: you are endorsed for cs but not q-bio, and arXiv requires endorsement for the
   PRIMARY category. cs.NE is the most natural cs home for connectome / neural-network modelling.
   Acceptable alternative primary (also cs-endorsed): cs.LG (Machine Learning).

## Cross-list categories
cs.LG (Machine Learning). Optionally q-bio.NC (Neurons and Cognition) as a cross-list only --
cross-lists to non-endorsed categories are permitted, though a moderator may drop them. Do NOT
set q-bio.NC as primary (no endorsement -> submission would be held/reclassified).

## License
CC BY 4.0 (Creative Commons Attribution 4.0 International). Select "arXiv.org perpetual,
non-exclusive license" plus CC BY 4.0 on the arXiv license step.

## Comments field
"5 pages, 4 figures. Code, data loaders, and all result artifacts at
https://github.com/Praveg432/functional-preservation-score . Submitted to TMLR."
(Update the TMLR line once an OpenReview ID exists.)

## Abstract (plain text for the arXiv form)
We introduce the Functional Preservation Score (FPS), a null-normalised, behaviourally grounded
measure of how much of a neural network's input-output function survives a structural operation,
and use it to audit the operations underlying speculative "mind-migration" pipelines on public
data that runs on a single laptop. Across five pre-registered studies on the C. elegans
connectome, whole-brain calcium activity, and hippocampal replay, FPS yields two positive
characterisations and a three-part negative. Low-bit quantisation of a real connectome exhibits a
structure-dependent sparsity floor: uniform int4/ternary quantisation is forced to roughly 73%/98%
effective sparsity because heavy-tailed integer synaptic weights round to zero, while
mixed-precision protection of hub neurons lowers these floors to about 27%/32%. Decoded
hippocampal replay sequences compress heavily yet remain identifiable at a cross-validated top-1
accuracy of 0.69 (95% CI [0.63, 0.74]; chance 0.125; permutation p < 1e-3) from latents of order
10-50 bits per event, and a bounded incremental store shows a graceful-versus-cliff capacity
trade-off. The migration pipeline fails in simulation at each stage for largely independent
reasons: the putative "identity payload" is not a functionally separable module (p >= 0.16 at
every tested size); cross-individual functional transport via Gromov-Wasserstein collapses once
the target's wiring is respected (fidelity 1.00 to 0.40, [0.31, 0.49], p < 1e-3) or alignment is
imperfect (0.06, [0.00, 0.13]); and biologically plausible local plasticity cannot reach the
function the target topology provably admits (gap 0.45, [0.27, 0.64], p < 1e-3, d = 2.0). We
release FPS, the data loaders, and all operations as a toolkit. All results are at nematode /
small-network scale and concern coherence in simulation, not the feasibility of reading or
writing a living brain.

## Source upload
Upload `arxiv-submission.tar.gz` (contains paper.tex, paper.bbl, tmlr.sty, math_commands.tex,
figures/). arXiv compiles from source and does NOT run BibTeX, so the pre-built paper.bbl is
included deliberately; do not add references.bib or .bst to the upload. Verified to compile from
a clean extraction.

## Pre-upload checklist
- [ ] Replace author placeholders in paper.tex (and re-run `tectonic paper.tex`), then
      regenerate the tarball (see README).
- [ ] Confirm paper.bbl is current (rebuild if references.bib changed).
- [ ] Submit under a cs primary (cs.NE or cs.LG) -- you are cs-endorsed; q-bio.NC is cross-list only.
- [ ] Match the Authors field here to the paper.tex author block exactly.
