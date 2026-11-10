# T4 — Overview

## Problem

The blueprint "writes" an aligned weight set into a clone via holographic STDP or ripple-timed
stimulation. The vetting marks the biological version absent (A3). The *simulation* version is
a legitimate open question: **can local plasticity rules install an externally-specified
function into a fixed foreign topology, and what is the reachable set?**

## Approach

1. **Target.** Take a functional circuit and its weights (from T2's transport, or a known
   target on C. elegans / a small recurrent net).
2. **Installer.** On a *differently-wired* host network (fixed topology ≠ source), apply only
   local rules: STDP, ripple/replay-timed potentiation, homeostatic normalization. No global
   backprop to the target — that would be cheating the "biological-plausibility" premise.
3. **Teaching signal.** Drive the host with the same inputs that elicit the target function
   and let local rules adjust weights toward reproducing the target outputs.
4. **Reachability map.** Characterize when local-rule installation converges vs. fails, as a
   function of (host-vs-target topology divergence, rule type, teaching-signal richness).
5. **Contrast control.** Compare to an idealized global optimizer (the upper bound) to
   quantify the *gap* local rules leave — the real cost of biological plausibility.

## Hypotheses

- H1: local rules can install simple transported functions into mildly-divergent hosts.
- H2: there is a divergence/complexity threshold beyond which local rules cannot reach the
  target even in unlimited time (a provable-in-sim impossibility region).
- H3: ripple-timed (structured) teaching outperforms unstructured STDP — the in-silico analogue
  of the blueprint's sleep-ripple mechanism.

## Honest scope (stated loudly)

A success here means "idealized local rules can install a reflex-scale function into a toy
foreign network in simulation." It does **NOT** mean the biological write is feasible, safe,
or possible in a living brain. T4 maps the *mathematical ceiling* of the idea, nothing more.
A failure here would be strong evidence the write is not merely unbuilt but incoherent.
