# Per-venue submission fields (copy-paste sheets)

Common assets (all venues): results are deterministic, laptop-scale, backed by committed
artifacts; code/data loaders released. Author: Praveg Vashishtha, Dept. of CSE, IIT Patna, India
and Sopra Banking Software India, praveg_pa2503mth259@iitp.ac.in.

---

## 1. arXiv (preprint) — PARALLEL-SAFE, do first
See `paper-arxiv/ARXIV-METADATA.md` for the full form. Summary:
- Upload: `paper-arxiv/arxiv-submission.tar.gz`
- Primary: q-bio.NC; cross-list: cs.LG (optionally cs.NE)
- License: CC BY 4.0
- Comments: "4 figures; code and data loaders released. Submitted to TMLR."

---

## 2. TMLR via OpenReview (primary archival) — PARALLEL-SAFE
Submit the anonymous PDF: `paper-tmlr/paper.pdf`.
- **Title:** A Functional Preservation Score for Auditing Connectome Operations: Compression,
  Alignment, Transport, and Local-Rule Writing
- **Authors:** keep hidden in the PDF; enter real authors in the OpenReview form (TMLR review is
  single-blind to the reviewers but authors are entered in the system).
- **Abstract:** single paragraph (as in the PDF).
- **Code/data:** provide an anonymised repository link in the submission (required field varies).
- **Supplementary:** optional; may attach the statistical-audit appendix.
- **Certifications:** none required at submission.
- **Conflicts/declarations:** complete as prompted.
- Note: arXiv posting is allowed by TMLR and does not count as prior publication.

---

## 3. NeurIPS ICBINB-bio workshop (parallel, non-archival) — PARALLEL-SAFE
Submit: `paper-workshop/paper.pdf` (4 pages + refs). **Before submitting, replace the stand-in
`tmlr.sty` with the official `neurips_20XX.sty` from that year's workshop call** (layout +
anonymity are mandated by the workshop). Non-archival, so compatible with the TMLR submission.
- **Title:** Where a Mind-Migration Pipeline Breaks: A Functional-Preservation Audit of Partition,
  Transport, and Local-Rule Writing
- **Topic fit:** ML-for-life-science failure analysis ("what breaks, why, how to evaluate").

---

## 4a. eLife (Tools and Resources) — JOURNAL OPTION A (pick ONE journal)
Submit: `paper/paper.pdf` + `paper/COVER-LETTER.md`.
- **Article type:** Tools and Resources (or Short Report).
- **Abstract, significance statement:** derive from the paper abstract.
- **Data/code availability:** release statement (public repo).
- eLife reviewed-preprint model: every reviewed paper is published with public reviews.

## 4b. PLOS Computational Biology (Methods) — JOURNAL OPTION B (fallback)
Submit: `paper/paper.pdf` + `paper/COVER-LETTER.md`.
- **Section:** Methods (or Research Article).
- **Data availability statement + code (open) required.**

> **DUAL-SUBMISSION WARNING.** eLife and PLOS-CB both require the manuscript NOT be under
> consideration elsewhere. Submit to only ONE at a time. Use 4b only if 4a declines. arXiv +
> TMLR + the workshop are all compatible with each other and with one journal.
