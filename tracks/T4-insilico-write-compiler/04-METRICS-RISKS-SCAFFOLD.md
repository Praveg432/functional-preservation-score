# T4 — Metrics, Risks, Scaffold

## Metrics
- **Installation fidelity:** how closely the host reproduces the target function after
  local-rule training (task-appropriate error).
- **Reachability:** fraction of (divergence, complexity) configs where fidelity ≥ threshold.
- **Plausibility gap:** fidelity(global optimizer) − fidelity(local rules), per config.
- **Structured-teaching advantage:** ripple-timed − unstructured STDP reach rate.

## Risks
| Risk | Mitigation |
|---|---|
| "Local rules" quietly become global optimization | Hard constraint: updates use only pre/post-synaptic + eligibility/ripple signals; audited in code review. |
| Toy nets don't generalize to connectomes | Run the easy cases on toy nets, then confirm on a C. elegans sub-circuit target. |
| Unbounded training time confound | Cap training; "not reached within budget" is reported distinctly from "proven unreachable". |
| Over-claiming biological relevance | Every result carries the honest-scope disclaimer from `00-OVERVIEW.md`. |

## Scaffold
```
T4-insilico-write-compiler/
  src/
    host_net.py        # fixed-topology host network (LIF/rate)
    local_rules.py     # STDP, ripple-timed potentiation, homeostasis (local-only, audited)
    installer.py       # drive host toward target function via local rules
    global_baseline.py # idealized optimizer upper bound (for the gap metric)
    reachability.py    # sweep + region classification
  experiments/
    T4a_easy_install.py    # V1
    T4b_divergence_sweep.py# V2 reachability/impossibility map
    T4c_structured_teach.py# V3 ripple vs STDP
  results/
```

## Compute
Small LIF/rate nets; local-rule sims are cheap. Fits M4 easily. Primary cost is the sweep
breadth, run serially/resumably.
