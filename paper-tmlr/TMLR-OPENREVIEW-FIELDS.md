# TMLR submission via OpenReview — field sheet

Submit the anonymous PDF `paper-tmlr/paper.pdf`. TMLR review is double-blind; keep authors out of
the PDF (the `tmlr` style already hides them) and provide an **anonymized** code/data link.

## OpenReview form fields

- **Title:** A Functional Preservation Score for Auditing Connectome Operations: Compression,
  Alignment, Transport, and Local-Rule Writing
- **Authors / author profiles:** enter Praveg Vashishtha (and the OpenReview profile) in the form.
  OpenReview stores author identity for the editorial system; reviewers see the anonymous PDF.
- **Abstract:** paste the single-paragraph abstract from the PDF (TMLR requires one paragraph).
- **PDF:** `paper-tmlr/paper.pdf` (anonymous build; verify no author name appears).
- **Primary area / subject:** evaluation / benchmarking / reproducibility; secondary: neuroscience
  & ML, graph learning, optimal transport.
- **Keywords:** functional preservation, connectome, graph compression, Gromov-Wasserstein,
  plasticity, negative results, evaluation.
- **Code / supplementary:** anonymized repository link (see below). Optionally attach the
  statistical-audit appendix as supplementary.
- **Declarations:** confirm not under review elsewhere as a *journal/conference* paper (arXiv
  preprint and non-archival workshops do NOT count — TMLR allows preprints).
- **Conflicts of interest / funding:** complete as prompted.

## Anonymized code/data mirror (for double-blind review)

The public repo `github.com/Praveg432/functional-preservation-score` deanonymizes the author, so
do NOT link it directly in the review version. Use an anonymizing proxy:

1. Go to https://anonymous.4open.science/ and create an "anonymized repository".
2. Point it at the public GitHub repo (or upload a snapshot). It serves a browsable, identity-
   stripped mirror at a URL like `https://anonymous.4open.science/r/fps-XXXX/`.
3. Before publishing the mirror, scrub identity from the snapshot:
   - `LICENSE` (contains the author name) — replace with "Anonymous" for the mirror only.
   - `RESEARCH-LOG.md` / README author lines / any email — remove or anonymize.
   - git history is not served by 4open.science, so commit-author metadata is not exposed.
4. Put that `anonymous.4open.science` URL in the OpenReview code field and (optionally) in the
   paper's reproducibility sentence for the review version.
5. At camera-ready (`\usepackage[accepted]{tmlr}`), replace the anonymized link with the real
   `github.com/Praveg432/functional-preservation-score` and restore the author block.

Alternative if you prefer not to use a proxy: state in the submission that "code and data are
available in an anonymized repository provided to the area editor on request," and share the
public link with the AE through OpenReview's confidential channel.

## Anonymity checklist (before clicking submit)
- [ ] `paper-tmlr/paper.pdf` shows no author name/affiliation/email (tmlr style handles this).
- [ ] No `github.com/Praveg432/...` or `linkedin.com/...` string anywhere in the PDF.
- [ ] Reproducibility sentence points to the anonymized mirror, not the public repo.
- [ ] Abstract is a single paragraph.
- [ ] Acknowledgements/funding that could identify the author are removed from the review PDF.
- [ ] Self-citations phrased in third person (no "our prior work [X]" that names you).

## After submission
- TMLR is rolling (no deadline); expect an Action Editor assignment, then reviews.
- Keep the arXiv version and this submission consistent; update the arXiv "Comments" with the
  OpenReview link once assigned (optional).
