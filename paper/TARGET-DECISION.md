# Primary Target Decision and Submission Plan

## Decision: TMLR (Transactions on Machine Learning Research) as the primary archival venue,
## with arXiv as the simultaneous preprint and the NeurIPS ICBINB-bio workshop as a parallel
## short-form outlet.

### Why TMLR is the optimum primary target (not eLife / PLOS-CB / a workshop alone)

The paper's defining characteristics are: (i) a reproducible *characterization + corrective*
rather than a splashy positive claim; (ii) a released metric and toolkit (methods contribution);
(iii) rigorous statistics on deliberately modest-scale systems; (iv) a central negative result.
Matching these to venue acceptance criteria:

- **TMLR accepts on correctness and clarity of claims, not novelty or impact.** This is decisive.
  Our strongest material is a set of *correct, well-scoped, well-evidenced* findings — exactly
  what TMLR is designed to reward. A novelty/impact-gated venue would penalize the modest scale
  and the negative framing; TMLR explicitly does not.
- **Negative and characterization results are in-scope and routinely accepted at TMLR**, whereas
  most selective ML conferences and many bio journals still implicitly favor positive results.
- **Methods/metric contributions fit.** Reframing the paper so FPS + the connectome operations
  (compression, GW transport, local-rule write) are the centerpiece makes it a clean ML-methods
  submission with neuroscience as the application domain.
- **Reviewing model reduces risk.** TMLR's claims-based review and action-editor model is a
  better fit for an interdisciplinary, honest-negative paper than a single-shot conference
  rebuttal cycle or a bio journal that may desk-reject on perceived scope.
- **Permits a public preprint** (the `[preprint]` style option), so arXiv posting is compatible.

Why not the alternatives as *primary*:
- *eLife (Tools & Resources)* — excellent for the toolkit angle, but the biology framing invites
  "scale / relevance to real brains" objections that TMLR's correctness standard sidesteps. Keep
  as a strong secondary if an ML venue is declined or if the biology framing is preferred later.
- *NeurIPS ICBINB-bio workshop* — ideal topical fit and fast visibility, but a workshop is
  non-archival and short-form. Run it **in parallel** for feedback, not as the archival home.
- *PLOS Computational Biology* — good fit, but slower and more biology-reviewer-weighted than TMLR.

### Plan (ordered)

1. **arXiv preprint (now).** Post the de-anonymized version (`paper/paper.pdf`, or the TMLR
   `[preprint]` build) to `q-bio.NC` with cross-list `cs.LG`. Needs a q-bio.NC endorsement for a
   first submission. Gives a citeable timestamp and does not conflict with TMLR.
2. **TMLR submission (primary).** Submit the **anonymized** TMLR build (`paper-tmlr/paper.pdf`)
   via OpenReview. Single-paragraph abstract, authors hidden, code/data links given as an
   anonymized repository. Appendix (statistical audit detail) after references.
3. **NeurIPS ICBINB-bio workshop (parallel).** Submit a 4-page short form (abstract + Study 3
   corrective + FPS) for fast expert feedback; workshops are non-archival so this is compatible
   with the TMLR submission.
4. **Fallback / alternative framing.** If TMLR declines or a biology framing is preferred:
   eLife (Tools and Resources) using `paper/paper.pdf`, then PLOS Computational Biology.

### Pre-submission checklist (TMLR)
- [ ] Use the **official** `tmlr.sty` / `tmlr.bst` unmodified (done; fetched from JmlrOrg).
- [ ] **Anonymous**: no author names, no identifying repo URLs in the review PDF.
- [ ] Abstract is a **single paragraph**.
- [ ] Every claim states estimate, 95% CI, n, and p (done in the statistics pass).
- [ ] Reproducibility statement + anonymized code/data link.
- [ ] Limitations and scope stated prominently (done).
- [ ] Figures legible at print size; captions self-contained (done).

### What needs human input before submission
- Author names/affiliations (withheld in the review build; added for camera-ready/arXiv).
- arXiv q-bio.NC endorser.
- An anonymized code/data repository URL for the review version.
