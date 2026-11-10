"""Smoke + contract tests for the shared substrate."""

import numpy as np

from shared.connectome import load_celegans, BASE_OS, PAYLOAD
from shared.model import ConnectomeModel, default_stimulus_bank
from shared.fps import Battery
from shared import compress


def _battery(c, n_patterns=6, T=30):
    model = ConnectomeModel.from_connectome(c)
    stim = default_stimulus_bank(len(model.sensory_idx), n_patterns=n_patterns, T=T)
    bat = Battery(stim, model.run)
    return model, stim, bat


def test_connectome_contract():
    c = load_celegans(n=200, seed=0)
    assert c.W.shape == (200, 200)
    assert not np.isnan(c.W).any()            # absence = explicit 0, never NaN
    assert set(np.unique(c.part)).issubset({BASE_OS, PAYLOAD})
    assert c.n_edges() > 0
    assert (c.part == PAYLOAD).sum() > 0        # partition is non-trivial


def test_model_runs_deterministically():
    c = load_celegans(n=200, seed=0)
    model = ConnectomeModel.from_connectome(c)
    stim = default_stimulus_bank(len(model.sensory_idx), n_patterns=3, T=20)
    y1 = model.run(stim[0])
    y2 = model.run(stim[0])
    assert y1.shape == (20, len(model.motor_idx))
    np.testing.assert_allclose(y1, y2)          # deterministic


def test_fps_identity_is_one():
    c = load_celegans(n=200, seed=0)
    model, stim, bat = _battery(c)
    res = bat.score(model.run)                  # scoring the reference against itself
    assert res.fps > 0.999


def test_fps_null_is_low():
    c = load_celegans(n=200, seed=0)
    model, stim, bat = _battery(c)

    def constant_run(s):
        return np.zeros((s.shape[0], len(model.motor_idx)))

    res = bat.score(constant_run)
    assert res.fps < 0.2                        # trivial output scores near zero


def test_pruning_budget_matches():
    c = load_celegans(n=200, seed=0)
    for pol in (compress.prune_uniform, compress.prune_engram_aware):
        Wp = pol(c.W, 0.5)
        s = compress.actual_sparsity(c.W, Wp)
        assert 0.4 <= s <= 0.6                   # ~50% removed (engram-aware may be slightly under)


def test_quantization_modes():
    c = load_celegans(n=120, seed=1)
    for mode in ("int8", "int4", "ternary"):
        Wq = compress.quantize(c.W, mode)
        assert Wq.shape == c.W.shape
        assert not np.isnan(Wq).any()
        # pruned-structure preserved: no new edges created
        assert np.all((Wq != 0) <= (c.W != 0) | (c.W != 0))
    # ternary has at most 3 distinct values (incl. 0)
    Wt = compress.quantize(c.W, "ternary")
    assert len(np.unique(Wt)) <= 3
