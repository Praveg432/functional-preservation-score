# Master Submission Guide

This is the single checklist to get the paper published as fast as possible. I have prepared
every format; **the actual submissions must be done by a human** (each venue requires an
authenticated login, license/originality/authorship declarations, and CAPTCHAs that cannot and
should not be automated). Each step below is copy-paste-and-click.

## What can go out in parallel vs. not

- **PARALLEL-SAFE (submit together, same day):** arXiv, TMLR (OpenReview), and the NeurIPS
  ICBINB-bio workshop. These are mutually compatible, and arXiv/workshop do not count as prior
  publication for TMLR.
- **NOT parallel:** eLife and PLOS Computational Biology are mutually exclusive (both forbid
  concurrent submission elsewhere). Submit to **one** journal; the other is a fallback only.
  Recommended primary archival venue overall is **TMLR** (see `TARGET-DECISION.md`), so a journal
  is optional; if you want a journal too, pick eLife OR PLOS-CB, not both.

## Fastest-publication ordering (recommended)

1. **arXiv first (today).** Public, citeable in ~1 business day. Does not block anything else.
2. **TMLR same day.** Primary archival; rolling submission, no deadline.
3. **ICBINB-bio workshop** when its call is open (check the deadline); non-archival, fast feedback.
4. **(Optional) one journal** later, only if you want a traditional journal record; do not run
   this concurrently with another journal.

## One-command rebuild (if anything changes)

```bash
bash paper/build_all.sh
```
Regenerates all figures from the committed result artifacts and rebuilds every PDF + the arXiv
tarball. Requires the `.venv` and `tectonic`.

## Step 1 — arXiv  (files: `paper-arxiv/`)
1. Log in to arXiv. You are endorsed for cs (not q-bio), so submit under a cs primary category.
2. Start a new submission; upload `paper-arxiv/arxiv-submission.tar.gz`.
3. Confirm the auto-built PDF matches `paper-arxiv/paper.pdf`.
4. Paste fields from `paper-arxiv/ARXIV-METADATA.md`: title, authors, abstract (plain text),
   primary **cs.NE** (cs-endorsed; cs.LG is an equally valid primary), cross-list **cs.LG** and
   optionally **q-bio.NC** (cross-list only -- do not set q-bio as primary without endorsement),
   comments.
5. License: **CC BY 4.0**.
6. Submit. (Author block already set to Praveg Vashishtha.)

## Step 2 — TMLR / OpenReview  (files: `paper-tmlr/`, fields: `VENUE-FIELDS.md §2`)
1. Log in to OpenReview; go to the TMLR submission portal.
2. Upload the anonymous PDF `paper-tmlr/paper.pdf` (authors hidden by the style file).
3. Fill title + single-paragraph abstract; enter real authors in the OpenReview form.
4. Provide an **anonymised** code/data repository link.
5. Complete declarations; submit. (No deadline; rolling.)

## Step 3 — ICBINB-bio workshop  (files: `paper-workshop/`, fields: `VENUE-FIELDS.md §3`)
1. Check the current call for the deadline and the official `neurips_20XX.sty`.
2. Swap the stand-in `tmlr.sty` for that style file (one line in `paper-workshop/paper.tex`), set
   anonymity per the call, rebuild with `tectonic paper.tex`.
3. Submit the 4-page PDF via the workshop's OpenReview.

## Step 4 (optional) — one journal  (files: `paper/paper.pdf` + `paper/COVER-LETTER.md`)
Pick eLife (Tools and Resources) **or** PLOS Computational Biology (Methods). Submit via that
journal's portal; attach the cover letter; complete the data/code availability statement. Do not
submit to the second journal unless the first declines.

## Pre-flight checklist (all venues)
- [ ] `bash paper/build_all.sh` runs clean; PDFs look right.
- [ ] Author/affiliation correct in `paper-arxiv/paper.tex` (Praveg Vashishtha, IIT Patna + Sopra).
- [ ] Anonymised repo link ready for TMLR.
- [ ] CC BY 4.0 selected on arXiv.
- [ ] Only one journal targeted at a time.

## Why I did not auto-submit
Submitting requires logging in as you and agreeing to binding legal declarations (license,
originality, authorship, no-concurrent-submission). It is neither technically possible from here
nor appropriate to do on your behalf. Everything up to the final "Submit" click is prepared.
