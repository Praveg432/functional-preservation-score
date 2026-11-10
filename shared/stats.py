"""Shared statistics helpers for uncertainty quantification and significance testing.

Deterministic given a seed. Used to harden every headline number with a 95% CI and, where a
comparison is claimed, a permutation p-value. Small-n is handled honestly (percentile bootstrap
+ exact/near-exact permutation), and the n is always reported alongside.
"""

from __future__ import annotations

import numpy as np


def bootstrap_ci(values, n_boot: int = 10000, alpha: float = 0.05, seed: int = 0):
    """Percentile bootstrap 95% CI of the mean of `values`. Returns (mean, lo, hi, n)."""
    v = np.asarray(values, dtype=float)
    n = v.size
    if n == 0:
        return (float("nan"), float("nan"), float("nan"), 0)
    if n == 1:
        return (float(v[0]), float(v[0]), float(v[0]), 1)
    rng = np.random.default_rng(seed)
    boot = rng.choice(v, size=(n_boot, n), replace=True).mean(axis=1)
    lo, hi = np.percentile(boot, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return (float(v.mean()), float(lo), float(hi), int(n))


def permutation_test_greater(group_a, group_b, n_perm: int = 10000, seed: int = 0):
    """One-sided permutation test: is mean(a) > mean(b)? Returns (observed_diff, p_value).

    Pools a,b, repeatedly re-partitions at the original sizes, and counts how often the permuted
    difference >= observed. p = (1 + count) / (1 + n_perm) (add-one for an unbiased estimate).
    """
    a = np.asarray(group_a, dtype=float)
    b = np.asarray(group_b, dtype=float)
    obs = a.mean() - b.mean()
    pooled = np.concatenate([a, b])
    na = a.size
    rng = np.random.default_rng(seed)
    count = 0
    for _ in range(n_perm):
        perm = rng.permutation(pooled)
        if (perm[:na].mean() - perm[na:].mean()) >= obs:
            count += 1
    p = (1 + count) / (1 + n_perm)
    return (float(obs), float(p))


def permutation_p_vs_null(observed: float, null_samples, greater: bool = True):
    """p-value of an observed statistic against an explicit null-sample array (add-one)."""
    null = np.asarray(null_samples, dtype=float)
    if greater:
        count = int(np.sum(null >= observed))
    else:
        count = int(np.sum(null <= observed))
    return (1 + count) / (1 + null.size)


def cohens_d(a, b):
    """Standardized mean difference (pooled SD). Reported as an effect size alongside CIs."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    na, nb = a.size, b.size
    if na < 2 or nb < 2:
        return float("nan")
    sp = np.sqrt(((na - 1) * a.var(ddof=1) + (nb - 1) * b.var(ddof=1)) / (na + nb - 2))
    return float((a.mean() - b.mean()) / (sp + 1e-12))
