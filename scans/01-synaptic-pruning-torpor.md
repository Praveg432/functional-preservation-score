# Scan 01 — Synaptic Pruning & Memory Resilience in Torpor

**Blueprint claim.** "Lin et al., *Science*" proved that massive synaptic turnover (e.g.
during torpor) does not destroy engram integrity, validating aggressive connectome
sparsification and 4-bit quantization.

**Verdict: REAL result, MIS-CITED.**

## What the literature actually shows

- **Synapse loss in torpor is real and large.** Entry into torpor is associated with a
  roughly **50–65% loss of synapses**, measured via loss of colocalization of pre- and
  post-synaptic markers; critically, the loss is of synaptic *clustering/contacts*, not of
  total synaptic protein — synapses re-form on arousal. This is the von der Ohe et al. work
  in the *Journal of Neuroscience* (2006/2007), not a *Science* paper by "Lin et al."
  [J Neurosci](https://www.jneurosci.org/content/27/1/84.full.txt)
- **Memory survives the turnover.** Recent "artificial hibernation" work (2025–2026) finds
  that a subset of spines — those contacting multisynaptic boutons — is preserved through
  hibernation, and that this *engram architecture* (not large spines per se) is what is
  resilient and correlates with long-term retention.
  [PubMed](https://pubmed.ncbi.nlm.nih.gov/42594194/) ·
  [preprint](https://www.biorxiv.org/content/10.64898/2025.12.09.692927v1.full)
- A separate, related 2021 result shows a single torpor/arousal cycle in mice can *increase*
  hippocampal LTP and contextual fear memory rather than degrade it.
  [Nature Sci Rep](https://www.nature.com/articles/s41598-021-94992-x)

## Bearing on the blueprint

- **Supports:** the qualitative claim that memory can survive heavy synaptic turnover. This
  is a genuine, non-trivial result and the most defensible pillar in the blueprint.
- **Does NOT support (over-reach):** that this *validates ternary/4-bit quantization of
  individual synaptic weights* for identity transfer. Torpor pruning is a *biological*
  remove-and-regrow process in which **engram-critical synapses are preferentially
  preserved**. That is nearly the opposite of a uniform low-bit weight quantization applied
  blindly to a static graph. The real lesson is "memory is carried by a resilient *sparse
  subset*," which argues for *structured, engram-aware* sparsification, not uniform ternary
  crushing.

**Correct citation to use:** von der Ohe et al., *J Neurosci* 2006/2007 (synapse loss in
torpor); 2025–26 artificial-hibernation engram-architecture study (resilience). Drop the
"Lin et al., *Science*" attribution — **[UNVERIFIED]**, likely spurious.

*Content rephrased from sources for licensing compliance.*
