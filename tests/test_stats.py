"""The paired bootstrap (experiments/stats.py) on synthetic results with known answers."""
import os, sys
import numpy as np
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "experiments"))
from stats import paired_bootstrap, gap_fraction, diff


def _res(arm_values: dict, seeds=None):
    n = len(next(iter(arm_values.values())))
    seeds = list(range(200, 200 + n)) if seeds is None else seeds
    return {"seeds": seeds, "lives": {a: [{"seed": s, "ticks_alive": float(v)} for s, v in zip(seeds, vals)]
                                      for a, vals in arm_values.items()}}


def test_gap_fraction_exact_half_zero_variance():
    # Per seed: base = b, target = b + 100, arm = b + 50, with b varying across seeds.
    # Pairing cancels the shared seed effect, so every replicate gives exactly 0.5.
    b = np.array([300., 900., 1500., 2100., 700., 1200.])
    res = _res({"ebm-dn": b, "tabular_q": b + 100, "x": b + 50})
    g = gap_fraction(res, "x", n_boot=500)
    assert g["mean"] == pytest.approx(0.5, abs=1e-12)
    assert g["lo"] == pytest.approx(0.5, abs=1e-12) and g["hi"] == pytest.approx(0.5, abs=1e-12)


def test_unpaired_resampling_would_not_be_degenerate():
    # Sanity check of the test above: the arms themselves are noisy, so a zero-width CI can only
    # come from pairing. An unpaired CI on one arm's mean is wide.
    b = np.array([300., 900., 1500., 2100., 700., 1200.])
    res = _res({"a": b})
    m = paired_bootstrap(res, "ticks_alive", ["a"], lambda m: m["a"], n_boot=500)
    assert m["hi"] - m["lo"] > 200


def test_shuffled_seeds_break_pairing():
    b = [300., 900., 1500.]
    res = _res({"ebm-dn": b, "tabular_q": b, "x": b})
    res["lives"]["x"] = res["lives"]["x"][::-1]          # same seeds, different order
    with pytest.raises(ValueError):
        gap_fraction(res, "x")
    res2 = _res({"a": b, "b": b})
    res2["lives"]["b"] = [{"seed": s + 1, "ticks_alive": v} for s, v in zip(range(200, 203), b)]
    with pytest.raises(ValueError):
        diff(res2, "a", "b")


def test_diff_paired_constant_offset():
    rng = np.random.default_rng(1)
    b = rng.normal(1000, 400, 20)
    res = _res({"ebm": b + 30, "ebm-nolearn": b})
    d = diff(res, "ebm", "ebm-nolearn", n_boot=1000)
    assert d["mean"] == pytest.approx(30) and d["lo"] == pytest.approx(30) and d["hi"] == pytest.approx(30)


def test_point_estimate_and_ci_cover_it():
    rng = np.random.default_rng(2)
    base = rng.normal(1000, 300, 20); tq = base + rng.normal(2000, 500, 20); x = base + rng.normal(800, 500, 20)
    res = _res({"ebm-dn": base, "tabular_q": tq, "x": x})
    g = gap_fraction(res, "x")
    expect = (x.mean() - base.mean()) / (tq.mean() - base.mean())
    assert g["mean"] == pytest.approx(expect)
    assert g["lo"] < g["mean"] < g["hi"]
    assert gap_fraction(res, "x") == g                  # deterministic for a fixed bootstrap seed


def test_base_and_target_have_g_0_and_1():
    rng = np.random.default_rng(3)
    base = rng.normal(1000, 300, 10)
    res = _res({"ebm-dn": base, "tabular_q": base + rng.normal(500, 100, 10)})
    assert gap_fraction(res, "ebm-dn")["mean"] == pytest.approx(0)
    assert gap_fraction(res, "tabular_q")["hi"] == pytest.approx(1)


def test_missing_arm_raises_keyerror():
    res = _res({"ebm-dn": [1., 2.], "tabular_q": [3., 4.]})
    with pytest.raises(KeyError):
        gap_fraction(res, "nope")
