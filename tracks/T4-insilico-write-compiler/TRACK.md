# T4 — In-Silico Write-Compiler (surrogate for the biological write)

**Type:** surrogate. **Attacks:** blueprint Stage 4 (write) / Tier-A risk **A3** (absent).
**Open question N4.** **Status:** scaffold, not executed.

## One-line claim

Hold the biology fixed and ask the clean theory question the blueprint never does: using only
**local, biologically-plausible plasticity rules** (STDP, ripple-timed potentiation), can a
*differently-wired* target network be driven to install a transported circuit's **function** —
and where does local-rule installation provably fail?

## Why this is the honest way to attack a blocked point

The biological write into a living differently-wired human brain is **absent in principle**
(`../../analysis/FEASIBILITY-RISK-LEDGER.md`, A3). We cannot build it. What we *can* build is
the **simulation** that tests whether the idea is even coherent: given a target set of weights
(from T2's transport) and only local update rules, does the network converge to the target
function? This separates "the write is biologically impossible" (true, Tier-A) from "the write
is mathematically impossible even with idealized local rules" (open, testable, novel).

## Why it is novel

- Plenty of work uses STDP to *train* networks. Nobody frames it as a **compiler**: install a
  *specific externally-specified* functional target into a *fixed foreign topology* via local
  rules only, and map the reachability/failure set. Optogenetic/ripple engram work
  (`../../scans/05`) re-activates existing engrams; it does not install a transported circuit.

## Boundary

- Owns: the local-rule installation simulator and its reachability analysis.
- Consumes: T2's transported weights (target) and T5's payload definition (what to install).
- Does **not** claim any biological write capability. Strictly a coherence-in-simulation study.

See `00-OVERVIEW.md`, `04-METRICS-RISKS-SCAFFOLD.md`, `vetting/VETTING-PLAN.md`.
