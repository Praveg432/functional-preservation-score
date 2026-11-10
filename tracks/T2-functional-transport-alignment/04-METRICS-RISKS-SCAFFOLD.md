# T2 — Metrics, Risks, Scaffold

## Metrics

- **Correspondence accuracy:** precision/recall vs. ground-truth matching (C. elegans labeled
  neurons); for fly/mouse, structural consistency + known hemisphere homologs.
- **Functional transport fidelity:** fraction of A's input→output behavior reproduced by B
  after transport (task-appropriate error, as in T1).
- **Transport boundary:** fidelity vs. A↔B structural divergence (e.g. GW distance, degree-
  distribution distance); locate the collapse point.
- **Mask-limited ceiling:** best achievable transport fidelity given only edges present in B
  (isolates H3).

## Risks

| Risk | Mitigation |
|---|---|
| GW too slow even coarsened | Start with worm (302 nodes, exact GW trivial); coarsen fly/mouse aggressively; cap node budget. |
| No ground truth for fly/mouse individuals | Use C. elegans for ground-truth validation; treat fly/mouse as qualitative stress cases. |
| Transport "works" trivially (near-identical graphs) | Inject controlled structural divergence (rewire fraction) to find the real boundary. |
| Confounding alignment vs. transport failure | Ablation: oracle correspondence (ground truth) isolates transport-only failure. |

## Scaffold

```
T2-functional-transport-alignment/
  src/
    gw_align.py            # entropic/hierarchical GW + FUGW option; coarsening
    transport.py           # weight transport through correspondence + Peters'-rule mask
    function_test.py       # run target net, measure reproduced function
    divergence.py          # A<->B structural divergence measures
  experiments/
    T2a_worm_groundtruth.py   # GW vs labeled-neuron ground truth (H1)
    T2b_transport_fidelity.py # transport + function test (H2)
    T2c_divergence_sweep.py   # controlled rewiring -> transport boundary
    T2d_mask_ceiling.py       # feasibility-mask limiter (H3)
  results/
```

## Compute

C. elegans GW is instant. Coarsened fly/mouse GW within minutes–hours on CPU/MPS. Fits the
M4 budget comfortably; the hard cap is node count after coarsening (keep ≤ ~5–10k).
