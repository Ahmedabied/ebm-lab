"""The paired bootstrap (experiments/stats.py) on synthetic results with known answers."""
import os, sys
import numpy as np
import pytest
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_ROOT, "experiments")); sys.path.insert(0, _ROOT)
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


# ---- referee fixes (harness2) ------------------------------------------------------------------
from stats import compare_gap, cross_world


def test_gap_fraction_reports_denominator_and_defined_flag():
    b = np.array([300., 900., 1500., 2100., 700., 1200.])
    res = _res({"ebm-dn": b, "tabular_q": b + 100, "x": b + 50})
    g = gap_fraction(res, "x", n_boot=500)
    assert g["defined"] and g["den"]["mean"] == pytest.approx(100) and g["den"]["lo"] == pytest.approx(100)
    # Target no better than base on average: the denominator CI straddles 0, G is undefined.
    rng = np.random.default_rng(5)
    res2 = _res({"ebm-dn": b, "tabular_q": b + rng.normal(0, 200, 6), "x": b + 50})
    g2 = gap_fraction(res2, "x", n_boot=500)
    assert g2["den"]["lo"] < 0 < g2["den"]["hi"] and g2["defined"] is False
    assert "n_nonfinite" in g2


def test_compare_gap_exact_and_frac():
    # Per seed: base b, target b+100, a = b+70, c = b+20  ->  G(a)-G(c) = 0.5 in every replicate.
    b = np.array([300., 900., 1500., 2100., 700., 1200.])
    res = _res({"ebm-dn": b, "tabular_q": b + 100, "a": b + 70, "c": b + 20})
    d = compare_gap(res, "a", "c", n_boot=500)
    assert d["mean"] == pytest.approx(0.5) and d["lo"] == pytest.approx(0.5) and d["hi"] == pytest.approx(0.5)
    assert d["frac_a_gt_b"] == 1.0
    assert compare_gap(res, "c", "a", n_boot=500)["frac_a_gt_b"] == 0.0
    # Point estimate equals the difference of the two gap fractions.
    rng = np.random.default_rng(6)
    res2 = _res({"ebm-dn": b, "tabular_q": b + rng.normal(800, 100, 6), "a": b + rng.normal(400, 300, 6),
                 "c": b + rng.normal(300, 300, 6)})
    d2 = compare_gap(res2, "a", "c")
    assert d2["mean"] == pytest.approx(gap_fraction(res2, "a")["mean"] - gap_fraction(res2, "c")["mean"])
    assert d2["lo"] <= d2["mean"] <= d2["hi"] and 0 < d2["frac_a_gt_b"] < 1


def test_cross_world_exact_and_seed_check():
    b = np.array([300., 900., 1500., 2100., 700., 1200.])
    lin = _res({"ebm-dn": b, "tabular_q": b + 100, "s": b + 60})        # G_linear = 0.6
    xor = _res({"ebm-dn": b + 5, "tabular_q": b + 205, "s": b + 45})    # G_xor = 0.2
    c = cross_world(lin, xor, "s", n_boot=500)
    assert c["G_linear"] == pytest.approx(0.6) and c["G_xor"] == pytest.approx(0.2)
    assert c["mean"] == pytest.approx(0.4) and c["lo"] == pytest.approx(0.4) and c["hi"] == pytest.approx(0.4)
    xor_bad = _res({"ebm-dn": b, "tabular_q": b + 100, "s": b}, seeds=list(range(300, 306)))
    with pytest.raises(AssertionError):
        cross_world(lin, xor_bad, "s")


def test_cross_world_resamples_seeds_jointly():
    # Strongly seed-correlated worlds: joint resampling gives a much tighter ΔG CI than the spread
    # of either world's G alone would suggest.
    rng = np.random.default_rng(7)
    b = rng.normal(1000, 400, 20); tq = b + rng.normal(1000, 300, 20); s = b + rng.normal(500, 300, 20)
    lin = _res({"ebm-dn": b, "tabular_q": tq, "s": s})
    xor = _res({"ebm-dn": b + 1, "tabular_q": tq + 1, "s": s + 1})      # nearly identical world
    c = cross_world(lin, xor, "s")
    gl = gap_fraction(lin, "s")
    assert c["hi"] - c["lo"] < 0.05 * (gl["hi"] - gl["lo"])


# ---- harness guards -----------------------------------------------------------------------------
from harness import _apply, check_seeds, BURNED, PROOF
from creature.sim import SimConfig


def test_apply_rejects_unknown_fields():
    cfg = SimConfig()
    _apply(cfg, {"brain.act_mode": "egreedy", "world.blend_mode": "xor", "learner": "q"})
    assert cfg.brain.act_mode == "egreedy" and cfg.learner == "q"
    for bad in ("brain.act_mod", "lerner", "nope.x", "brain.act_mode.y"):
        with pytest.raises(KeyError) as e:
            _apply(SimConfig(), {bad: 1})
        assert e.value.args[0] == bad


def test_02_main_overrides_are_all_real_fields():
    # Every override key EXP-02 uses must exist, or the arm silently runs the default.
    for k in ("policy", "day_learning", "learner", "sleep", "growth", "brain.act_mode",
              "sense.sign_features", "world.blend_mode"):
        _apply(SimConfig(), {k: getattr(SimConfig(), k.split(".")[0]) if "." not in k else
                             getattr(getattr(SimConfig(), k.split(".")[0]), k.split(".")[1])})


def test_burned_and_proof_seeds_refused_outside_pilots():
    assert {0, 7, 20, 27, 100, 119} <= BURNED and 8 not in BURNED and 200 not in BURNED
    assert PROOF == set(range(300, 340))
    check_seeds("02_main_linear", range(200, 220))                       # fresh: fine
    for seeds in ([200, 201, 105], [300], [25]):
        with pytest.raises(ValueError):
            check_seeds("02_main_linear", seeds)
    for pilot in ("00_calibration", "01_main_linear", "02a_pilot_alpha"):
        check_seeds(pilot, [0, 20, 100, 300])                            # pilots may
    with pytest.raises(ValueError):
        check_seeds("02b_whatever", [300])
