# T5 — Results (Base-OS / identity-payload separability)

Surrogate track attacking the blueprint's Stage-1 premise (risk B2): a clean, swappable split
between a regenerable "Base-OS" and a transferable "identity payload." Substrate: the real
C. elegans connectome (`data/celegans_real.npz`, 306 neurons; 81 sensory / 95 inter / 130 motor).
Readout + FPS reuse the T1 substrate. Requires the `.venv`.

## V1 — readout + ablation sanity → **PASS**
`experiments/T5_v1_ablation_sanity.py` → `results/T5_v1.json`

- Intact FPS = 1.0; ablation measurably disrupts function (drops to 0 at most lesion levels,
  large lesions well below intact). The readout is lesion-sensitive — the instrument works.
- The dose-response is non-monotone (which neurons are removed matters more than how many) —
  itself a preview of the T5 thesis.

## Instrument correction (honest process — V1→V2)
The first separability definition ablated "Base-OS = sensory+motor" and measured residual
payload function. Diagnosis (`scripts/diagnose_t5.py`) showed this is **ill-posed**: ablating
Base-OS deletes **all 130 motor readout neurons and all 81 sensory inputs**, so FPS is trivially
0 for *every* partition (incl. nulls) — a degenerate instrument, not a finding. Corrected
framing (`src/separability.py`): the **Base-OS (sensory inputs + motor outputs) is a FIXED
interface, never ablated**; the test is whether the asserted "identity payload" (an interneuron
core) carries the input→output *transformation* more than a random interneuron subset of equal
size. (Metric fixed once, from diagnosis — not blind iteration.)

## V2 — separability vs null (load-bearing) → **H2, corrective**
`experiments/T5_v2_separability_null.py` → `results/T5_v2.json`

Asserted payloads (interneuron sub-cores): hub-strength core and recurrent core, vs random
interneuron subsets of equal size. Robust across payload fractions 10–40%:

| payload frac | payload ablation drop | random-null drop | z vs null | beats nulls |
|---|---|---|---|---|
| 0.10 | 0.85 | 0.63 ± 0.26 | +0.87 | 75% |
| 0.20 | 1.00 | 0.70 ± 0.24 | +1.25 | 75% |
| 0.30 | 1.00 | 0.79 ± 0.20 | +1.06 | 72% |
| 0.40 | 1.00 | 0.83 ± 0.17 | +1.03 | 70% |

- The asserted "identity payload" is **mildly more disruptive to ablate than random** (beats
  ~70–75% of nulls) but **never significantly** (z ≈ +0.9 to +1.3, never near z>2).
- **Verdict (H2, corrective):** on the real C. elegans connectome there is **no cleanly
  separable "identity payload."** The integrative interneuron core carries function, but barely
  more than a random interneuron subset of the same size — function is **distributed**, not
  localized to a special swappable module.

## What this means for the blueprint
This is a direct, measured corrective to Stage-1: the premise that identity-bearing computation
forms a clean, separable module you can lift out and transplant onto a regenerated Base-OS is
**not supported** on the one substrate where we can test it end-to-end. The split is a design
assumption, not a graph-functional property.

## Honest scope
Separability on a 306-neuron nematode connectome does not prove anything about a human
Base-OS/identity split; it bounds the blueprint's premise on the nearest testable system and
finds it wanting. Near-saturation at large ablation fractions compresses dynamic range, but the
corrective holds with headroom at 10% too. This is a surrogate/coherence result, not a claim
about biological migration (Tier-A unchanged).

## Status
- V1 PASS (instrument works), V2 corrective H2 (load-bearing question answered).
- V3 (swap-tolerance, H3) is **optional given V2**: with no separable module, "swap the Base-OS
  and keep the payload" has no clean module to preserve — the swap question is largely mooted by
  the corrective. Can be run as a bound if the chain to T2/T4 needs it.
- **Banked:** partitions, ablation, corrected separability (fixed-I/O privilege test).
- **Feeds the surrogate chain:** T5's finding (distributed, non-separable function) directly
  informs T2 (functional transport) — there is no privileged sub-module to align/transport,
  which raises the bar for T2's transport test.