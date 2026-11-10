# Submission Venue Recommendation

The paper straddles computational neuroscience, machine learning (graph compression, optimal
transport, plasticity), and research methodology / failure analysis. Its defining features — a
reproducible negative/corrective result plus two positive characterizations and a released
toolkit — point to venues that explicitly value reproducibility, tools/resources, and negative
findings. A staged plan is recommended.

## Recommended path (staged)

### Step 1 — Preprint first: arXiv `q-bio.NC` (cross-list `cs.LG`)
- **Why:** connectome + ML work lives here; immediate timestamp, citeable, no gatekeeping delay.
  Cross-listing to `cs.LG` reaches the graph-compression / optimal-transport audience.
- **Note:** arXiv requires endorsement for a first submission in a category; a co-author or
  colleague already publishing in q-bio.NC can endorse. Post here *before or alongside* the
  journal/workshop submission.

### Step 2a — Workshop (fastest peer feedback, strong topical fit)
- **NeurIPS 2026 "I Can't Believe It's Not Better" — ML-meets-life-science edition**
  (`icbinb-bio.github.io`). Scope is almost exactly this paper: *"what breaks, why it breaks,
  how we should evaluate it, and what more reliable scientific systems require."* A failure
  analysis of an over-reaching biological-ML pathway, with a measurement framework, is squarely
  in remit. Short-paper format suits the surrogate-chain corrective (T5/T2/T4) + FPS.
- **Fit:** excellent. Lowest-friction way to get expert review and visibility for the negative result.

### Step 2b — Journal (archival, full paper)
Two good fits, choose by framing:
- **eLife** (Tools and Resources, or Scientific Correspondence). eLife runs a reviewed-preprint
  model (every reviewed paper is published with public reviews; no binary accept/reject) and
  explicitly welcomes Tools/Resources, Replication Studies, and null results. The FPS metric +
  released toolkit + reproducibility emphasis fit "Tools and Resources" well.
- **PLOS Computational Biology** (Methods or Research Article). Strong home for reproducible
  computational-neuroscience methods with open data/code; receptive to rigorous negative results.
- Alternative: **Frontiers in Neuroinformatics** (reproducibility/rigour focus) or **Network
  Neuroscience** (connectome methods). Lower selectivity; use if the above decline.

### Step 3 — If repositioned as primarily an ML-methods contribution
- **TMLR (Transactions on Machine Learning Research)** — accepts work judged on correctness and
  clarity rather than novelty/impact, and is friendly to characterization/negative results and
  rigorous evaluation. A good fit if the FPS metric + compression/transport operations are made
  the centerpiece and the neuroscience framing is secondary.

## Recommendation summary
1. **Post to arXiv q-bio.NC (+cs.LG) now** for the timestamp and citeability.
2. **Submit the short form to the NeurIPS ICBINB (bio) workshop** — best topical fit, fast expert
   review, visibility for the "compress yes / migrate no" corrective.
3. **Submit the full paper to eLife (Tools and Resources) or PLOS Computational Biology** for the
   archival version, leaning on the FPS toolkit + reproducibility.
4. Keep **TMLR** as the fallback / alternative if an ML-methods framing is preferred.

## Fit caveats to anticipate from reviewers
- *Scale*: 306-neuron connectome / toy nets — pre-empt by foregrounding the honest-scope framing
  and the cross-substrate replication as stated future work.
- *"Is a negative result publishable?"* — the workshop and eLife/PLOS-CB reproducibility venues
  explicitly say yes; the positive results (T1 floor, T3 compression) and the released metric
  give the paper standalone constructive value beyond the corrective.
