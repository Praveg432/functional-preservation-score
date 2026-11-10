"""Generate publication figures for the paper from committed result artifacts.

Reads tracks/*/results/*.json (never recomputes) and writes PDFs + PNGs to paper/figures/.
Deterministic. Run: .venv/bin/python paper/make_figures.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "paper" / "figures"
FIG.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 150, "savefig.dpi": 300, "font.size": 9,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.titlesize": 10, "legend.frameon": False, "figure.autolayout": True,
})
C = {"uniform": "#b0b0b0", "engram": "#2c6fbb", "global": "#1a9850",
     "local": "#d73027", "accent": "#333333"}


def load(p):
    return json.load(open(ROOT / p))


def save(fig, name):
    fig.savefig(FIG / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(FIG / f"{name}.png", bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


def fig1_t1_floor():
    """T1: effective-sparsity floor by bit-depth, uniform vs engram."""
    d = load("tracks/T1-structured-connectome-compression/results/T1_v3_real.json")
    fl = d["effective_sparsity_floor"]
    bits = ["int8", "int4", "ternary"]
    uni = [fl[f"{b}|uniform"] for b in bits]
    eng = [fl[f"{b}|engram:strength"] for b in bits]
    x = np.arange(len(bits)); w = 0.38
    fig, ax = plt.subplots(figsize=(4.2, 3.0))
    ax.bar(x - w/2, uni, w, label="uniform", color=C["uniform"])
    ax.bar(x + w/2, eng, w, label="engram-aware (mixed precision)", color=C["engram"])
    for xi, v in zip(x - w/2, uni):
        ax.text(xi, v + 0.02, f"{v:.2f}", ha="center", fontsize=7)
    for xi, v in zip(x + w/2, eng):
        ax.text(xi, v + 0.02, f"{v:.2f}", ha="center", fontsize=7)
    ax.set_xticks(x); ax.set_xticklabels(bits)
    ax.set_ylabel("forced effective sparsity (floor)")
    ax.set_ylim(0, 1.08)
    ax.set_title("T1: low-bit quantisation sparsity floor\n(real C. elegans connectome)")
    ax.legend(loc="upper left")
    save(fig, "fig1_t1_floor")


def fig2_t3_frontier():
    """T3: identification vs bits/event with 95% CIs, + capacity curves."""
    s = load("tracks/T3-replay-latent-compression/results/T3_v2_stats.json")
    fr = sorted(s["frontier_with_ci"], key=lambda r: r["bits_per_event"])
    bpe = [r["bits_per_event"] for r in fr]
    top = [r["top1_mean"] for r in fr]
    lo = [r["top1_mean"] - r["ci95"][0] for r in fr]
    hi = [r["ci95"][1] - r["top1_mean"] for r in fr]
    chance = 0.125

    v3 = load("tracks/T3-replay-latent-compression/results/T3_v3.json")
    sup = v3["superposition_curve"]; slot = v3["slot_curve"]

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.0))
    a1.errorbar(bpe, top, yerr=[lo, hi], marker="o", color=C["engram"], capsize=3, lw=1.5)
    a1.axhline(chance, ls="--", color=C["accent"], lw=1, label=f"chance ({chance:.3f})")
    a1.set_xscale("log", base=2)
    a1.set_xlabel("bits per event"); a1.set_ylabel("identification top-1")
    a1.set_ylim(0, 0.8); a1.set_title("T3: compression vs identifiability\n(30-split CV, 95% CI)")
    a1.legend(loc="lower right")

    a2.plot([r["load"] for r in sup], [r["superposition_recovery"] for r in sup],
            marker="o", color=C["engram"], label="superposition")
    a2.plot([r["load"] for r in slot], [r["slot_recovery"] for r in slot],
            marker="s", color=C["local"], label=f"slots (n={v3['n_slots']})")
    a2.set_xlabel("events stored (load)"); a2.set_ylabel("recovery")
    a2.set_ylim(0, 1.05); a2.set_title("T3: capacity / interference")
    a2.legend(loc="lower left")
    save(fig, "fig2_t3_frontier")


def fig3_t2_transport():
    """T2: transport fidelity under three conditions, with 95% CIs (5% divergence)."""
    s = load("tracks/T2-functional-transport-alignment/results/T2_v2_stats.json")
    conds = [("transport_oracle", "oracle corr.\n+ unconstrained"),
             ("transport_oracle_masked", "oracle corr.\n+ feasibility mask"),
             ("transport_gw", "GW corr.\n+ feasibility")]
    means = [s[k]["mean"] for k, _ in conds]
    lo = [s[k]["mean"] - s[k]["ci95"][0] for k, _ in conds]
    hi = [s[k]["ci95"][1] - s[k]["mean"] for k, _ in conds]
    x = np.arange(len(conds))
    fig, ax = plt.subplots(figsize=(4.4, 3.2))
    ax.bar(x, means, 0.6, yerr=[lo, hi], capsize=4,
           color=[C["global"], C["engram"], C["local"]])
    for xi, v in zip(x, means):
        ax.text(xi, v + 0.03, f"{v:.2f}", ha="center", fontsize=8)
    ax.set_xticks(x); ax.set_xticklabels([lab for _, lab in conds], fontsize=8)
    ax.set_ylabel("transport fidelity (FPS)"); ax.set_ylim(0, 1.12)
    ax.set_title("T2: functional transport at 5% divergence\n(8 realisations, 95% CI)")
    save(fig, "fig3_t2_transport")


def fig4_t4_gap():
    """T4: global ceiling vs local plasticity (plausibility gap), with 95% CIs."""
    s = load("tracks/T4-insilico-write-compiler/results/T4_v2_stats.json")
    g = s["global_ceiling"]; l = s["best_local"]
    labels = ["global optimiser\n(upper bound)", "local plasticity\n(best of plain/ripple)"]
    means = [g["mean"], l["mean"]]
    lo = [g["mean"] - g["ci95"][0], l["mean"] - l["ci95"][0]]
    hi = [g["ci95"][1] - g["mean"], l["ci95"][1] - l["mean"]]
    x = np.arange(2)
    fig, ax = plt.subplots(figsize=(4.0, 3.2))
    ax.bar(x, means, 0.55, yerr=[lo, hi], capsize=4, color=[C["global"], C["local"]])
    for xi, v in zip(x, means):
        ax.text(xi, v + 0.03, f"{v:.2f}", ha="center", fontsize=8)
    gap = s["plausibility_gap"]
    ax.annotate("", xy=(1, means[1]), xytext=(1, means[0]),
                arrowprops=dict(arrowstyle="<->", color=C["accent"]))
    ax.text(1.08, (means[0]+means[1])/2, f"gap {gap['mean']:.2f}\n[{gap['ci95'][0]:.2f},{gap['ci95'][1]:.2f}]",
            fontsize=7, va="center")
    ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("installation fidelity (FPS)"); ax.set_ylim(0, 1.15)
    ax.set_title("T4: write-compiler plausibility gap\n(10 seeds, 95% CI, p=1e-4, d=2.0)")
    save(fig, "fig4_t4_gap")


if __name__ == "__main__":
    fig1_t1_floor()
    fig2_t3_frontier()
    fig3_t2_transport()
    fig4_t4_gap()
    print("all figures ->", FIG)
