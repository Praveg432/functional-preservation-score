# Methodology — How this deep-dive was built

## Objective

Build a correct, non-credulous understanding of the mind-migration blueprint: establish
the real neuroscience/ML background, verify each cited breakthrough against primary
literature, decompose the proposed pipeline into independently-checkable claims, and
separate the thesis-grade buildable core from the speculative remainder.

## Approach

1. **Preserve the input.** The source blueprint is stored verbatim in
   `inputs/00-source-blueprint.md`. Nothing in the analysis edits or paraphrases it in
   place; the analysis sits beside it.
2. **Verify every referenced breakthrough live.** Each of the five "cannibalized
   breakthroughs" plus the core alignment math (Gromov-Wasserstein) was checked against
   primary sources (journal papers, preprints, Nobel committee material, lab publications).
   Findings are in `scans/`.
3. **Decompose before judging.** The end-to-end architecture is split into six stages
   (partition → quantize → align → write → read → prime). Each stage gets its own set of
   sub-claims, each tagged with an evidence level.
4. **Ledger the risk.** Load-bearing assumptions are listed with an explicit kill-criterion
   — the single observation that would falsify them. This mirrors the workspace's
   vetting-gate discipline.

## Evidence tags

| Tag | Meaning |
|---|---|
| **REAL** | Claim is supported by a verifiable primary source, used correctly. |
| **OVERSTATED** | Underlying work exists but the blueprint claims more than the source shows. |
| **MIS-CITED / MIS-DESCRIBED** | The work exists but the attribution or technical description is wrong. |
| **HYPOTHESIS** | A plausible-sounding design choice with no established support. |
| **[UNVERIFIED]** | Could not be grounded in any source; treat as unproven. |

## Evidence standard

- Every external factual claim carries an inline source and a tag.
- Where the blueprint gives a precise number (e.g. "300 TB", "37%", "86B neurons"), the
  number is checked; if it traces to a real source it is kept with attribution, otherwise
  flagged.
- Source text is rephrased for licensing compliance; no long verbatim quotes.
- Speculative extrapolations in the blueprint are labelled HYPOTHESIS, not repeated as fact.

## Known limitations of this deep-dive

- This is a desk study. It verifies *claims and feasibility*, not laboratory reproduction.
- Literature search reflects what was publicly indexed at the capture date in
  `RESEARCH-LOG.md`; fast-moving fields may have newer results.
- Ethical, legal, and philosophical questions (personal identity, consent, continuity of
  self) are flagged where they gate the science but are not resolved here.
