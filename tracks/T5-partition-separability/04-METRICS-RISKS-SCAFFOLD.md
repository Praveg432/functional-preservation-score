# T5 — Metrics, Risks, Scaffold

## Metrics
- **Separability index:** degree to which Base-OS lesions spare payload function and vice
  versa, normalized against a random-partition null.
- **Cross-dependence:** residual payload-function loss attributable to Base-OS ablation.
- **Swap tolerance:** payload fidelity after Base-OS swap vs. Base-OS divergence (decay curve).

## Risks
| Risk | Mitigation |
|---|---|
| Partition labels are subjective | Use anatomically/ type-grounded partitions (layer, cell type, sensory vs. interneuron); report sensitivity to the labeling. |
| Readout too coarse to show dissociation | Validate readout sensitivity in V1 before separability claims. |
| Over-generalizing from animals to humans | Honest-scope disclaimer on every result; frame as a bound, not a human claim. |

## Scaffold
```
T5-partition-separability/
  src/
    partitions.py      # candidate Base-OS / payload partitions per substrate
    ablate.py          # lesion + functional readout
    separability.py    # separability index + random-partition null
    swap.py            # Base-OS swap test + divergence control
  experiments/
    T5a_ablation.py        # V1 + dissociation
    T5b_separability_null.py# V2 vs null
    T5c_swap_tolerance.py  # V3 swap/divergence
  results/
```

## Compute
Ablation + readout on sub-circuits / columns is cheap; C. elegans whole-brain is instant.
Fits M4 comfortably.
