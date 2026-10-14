"""EXP-02 laws for the senses+acting builder: sign features (no valence, mirror TabularQ), Senses.dim,
egreedy behaviour log-prob, RNG draw order, determinism, IS-weighted online learning, and the
softmax default path being bit-for-bit the EXP-01 code."""
import hashlib
import numpy as np
import pytest
from creature.brain import Brain, BrainConfig, A
from creature.senses import Senses, SenseConfig, DIM, DIM_SIGN
from creature.world import NOTES
from creature.baselines import TabularQ
from creature.sim import Life, SimConfig


# ---- a tiny deterministic fake world: three distinct smooth fields ---------------------------
class FakeWorld:
    def __init__(self, perm=None):
        self.perm = np.arange(NOTES) if perm is None else np.asarray(perm)

    def read(self, y, x):
        v = np.array([0.3 + 0.2 * np.sin(0.7 * y + 0.1 * x),
                      0.5 + 0.4 * np.cos(0.3 * x - 0.2 * y),
                      0.2 + 0.1 * np.sin(1.1 * x * 0.5 + 0.9 * y)], dtype=np.float64)
        return v[self.perm]


def _blocks(x):
    n = NOTES
    return {"contrast": x[0:n], "mean": x[n:2 * n], "change": x[2 * n:3 * n],
            "body": x[3 * n:3 * n + 2], "sign": x[3 * n + 2:3 * n + 2 + n], "bias": x[-1:]}


# ---- sign features ---------------------------------------------------------------------------
def test_senses_dim_and_default_vector_unchanged():
    assert Senses(SenseConfig()).dim == DIM == 12
    assert Senses(SenseConfig(sign_features=True)).dim == DIM_SIGN == 15
    body = np.array([0.7, 0.1], np.float32)
    a = Senses(SenseConfig(noise=0.0)).sense(FakeWorld(), 3.0, 4.0, 0.5, body)
    b = Senses(SenseConfig(noise=0.0, sign_features=True)).sense(FakeWorld(), 3.0, 4.0, 0.5, body)
    assert a["x"].shape == (12,) and b["x"].shape == (15,) and "sign" not in a
    # sign dims are inserted before the bias; everything else is identical to the default vector
    assert np.array_equal(b["x"][:11], a["x"][:11]) and b["x"][-1] == a["x"][-1] == 1.0
    assert np.array_equal(b["x"][11:14], b["sign"])


@pytest.mark.parametrize("perm", [(1, 0, 2), (2, 0, 1), (0, 2, 1), (1, 2, 0)])
def test_sign_features_carry_no_valence_permuting_notes_permutes_features(perm):
    """Relabel which note is which in the world's readings: the sign block is permuted the same way
    and nothing note-independent (body, bias) moves. The feature never singles out a note."""
    perm = np.array(perm)
    body = np.array([0.6, 0.2], np.float32)
    s0 = Senses(SenseConfig(noise=0.0, sign_features=True, dead=0.0005))
    s1 = Senses(SenseConfig(noise=0.0, sign_features=True, dead=0.0005))
    pts = [(2.0, 3.0, 0.1), (5.5, 1.2, 2.0), (7.0, 7.0, 4.0), (1.0, 9.0, 5.5), (4.0, 4.0, 3.1)]
    nonzero = 0
    for (y, x, h) in pts:
        o0 = s0.sense(FakeWorld(), y, x, h, body)
        o1 = s1.sense(FakeWorld(perm), y, x, h, body)
        b0, b1 = _blocks(o0["x"]), _blocks(o1["x"])
        assert np.array_equal(b1["sign"], b0["sign"][perm])
        for k in ("contrast", "mean", "change"):
            assert np.array_equal(b1[k], b0[k][perm])
        assert np.array_equal(b1["body"], b0["body"]) and np.array_equal(b1["bias"], b0["bias"])
        nonzero += int(np.abs(b0["sign"]).sum())
    assert nonzero > 0                                   # the test actually exercised nonzero signs


def test_sign_features_are_odd_in_left_right():
    """Swapping the two antennae negates every sign: the feature is a symmetric direction code."""
    s = Senses(SenseConfig(sign_features=True))
    rng = np.random.default_rng(0)
    L = rng.normal(0.5, 0.1, (200, NOTES)).astype(np.float32)
    R = rng.normal(0.5, 0.1, (200, NOTES)).astype(np.float32)
    for l, r in zip(L, R):
        assert np.array_equal(s.signs(r, l), -s.signs(l, r))
        assert set(np.unique(s.signs(l, r))) <= {-1.0, 0.0, 1.0}


def test_sign_features_mirror_tabular_q_state():
    """On the same noisy readings the sim hands TabularQ, the three sign dims decode to exactly the
    three ternary digits of TabularQ._state (digit 0 <-> +1, 1 <-> 0, 2 <-> -1)."""
    s = Senses(SenseConfig(sign_features=True))
    q = TabularQ(np.random.default_rng(0))
    assert q.dead == s.cfg.dead
    rng = np.random.default_rng(1)
    world = FakeWorld()
    hits = {-1.0: 0, 0.0: 0, 1.0: 0}
    for t in range(3000):
        y, x, h = rng.uniform(0, 10), rng.uniform(0, 10), rng.uniform(0, 2 * np.pi)
        body = np.array([rng.uniform(0, 1), 0.0], np.float32)
        o = s.sense(world, y, x, h, body, rng)              # noisy readings (noise 0.02 > dead)
        digits = (1 - o["sign"]).astype(int)
        expect = (digits[0] * 9 + digits[1] * 3 + digits[2]) * 2 + (1 if body[0] < 0.5 else 0)
        assert q._state(o) == expect, (o["left"] - o["right"], o["sign"])
        for v in o["sign"]: hits[float(v)] += 1
    assert min(hits.values()) > 100                      # all three sign values were exercised


def test_life_builds_brain_with_senses_dim_and_does_not_mutate_config(tmp_path):
    for sign, d in ((False, 12), (True, 15)):
        cfg = SimConfig(seed=3, policy="ebm", days=2, day_len=40, day_learning=True,
                        growth="timer", growth_every=1, runs_dir=str(tmp_path))
        cfg.sense.sign_features = sign
        L = Life(cfg)
        assert L.senses.dim == d and L.brain.cfg.dim == d
        assert L.brain.theta["w"].shape == (A, d) and L.brain.theta["u"].shape[1] == d
        assert cfg.brain.dim == 12                       # config untouched
        H0 = L.brain.theta["u"].shape[0]
        L.run()                                          # runs through acting, learning, growth
        assert L.body.alive and L.day == cfg.days - 1    # both nights happened (growth had a chance)
        H = L.brain.theta["u"].shape[0]
        assert H > H0                                    # timer growth every night actually grew
        assert L.brain.theta["u"].shape == (H, d)        # new units have the senses' width


# ---- egreedy acting --------------------------------------------------------------------------
@pytest.mark.parametrize("eps,zero_theta", [(0.1, False), (0.3, False), (0.1, True)])
def test_egreedy_logp_is_the_true_behaviour_probability(eps, zero_theta):
    """exp(logp) returned by act equals the empirical action frequency over 20000 draws, to within
    0.01 absolute (binomial sd at p=0.033 is 0.0013). zero_theta: all F tie -> action 0 is greedy."""
    rng = np.random.default_rng(11)
    br = Brain(BrainConfig(dim=DIM, act_mode="egreedy", eps=eps, init_scale=0.5), rng)
    if zero_theta:
        for k in br.theta: br.theta[k][:] = 0.0
    x = rng.normal(size=DIM)
    greedy = int(np.argmin(br.F(x[None, :])[0]))
    if zero_theta: assert greedy == 0
    N = 20000
    counts = np.zeros(A); lp = {}
    for _ in range(N):
        a, Fx, l = br.act(x, rng)
        counts[a] += 1
        assert lp.setdefault(a, l) == l                  # same action, same reported log-prob
    assert len(lp) == A
    p = np.array([np.exp(lp[a]) for a in range(A)])
    assert np.isclose(p.sum(), 1.0)
    assert np.isclose(p[greedy], 1 - eps + eps / A) and np.allclose(np.delete(p, greedy), eps / A)
    assert np.abs(counts / N - p).max() < 0.01, (counts / N, p)


def test_egreedy_rng_draw_order():
    """One rng.random() per act, then one rng.integers(A) only if it explored; nothing else."""
    eps = 0.25
    rng = np.random.default_rng(5); ref = np.random.default_rng(5)
    br = Brain(BrainConfig(dim=DIM, act_mode="egreedy", eps=eps), np.random.default_rng(0))
    X = np.random.default_rng(1).normal(size=(500, DIM))
    explored = 0
    for x in X:
        a, Fx, _ = br.act(x, rng)
        if ref.random() < eps:
            assert a == int(ref.integers(A)); explored += 1
        else:
            assert a == int(np.argmin(Fx))
    assert 0 < explored < len(X)
    assert rng.random() == ref.random()                  # generators are in the same state


def test_softmax_act_logp_equals_policy_logp_exactly():
    """So the online IS ratio is exactly 1.0 under softmax acting (same theta)."""
    rng = np.random.default_rng(2)
    br = Brain(BrainConfig(dim=DIM, init_scale=0.5), rng)
    for _ in range(200):
        x = rng.normal(size=DIM)
        a, _, l = br.act(x, rng)
        assert np.exp(br.logp(x[None, :], np.array([a]))[0] - l) == 1.0


def test_unknown_act_mode_raises():
    br = Brain(BrainConfig(dim=DIM, act_mode="greedy"), np.random.default_rng(0))
    with pytest.raises(ValueError):
        br.act(np.zeros(DIM), np.random.default_rng(0))


# ---- online learning with the IS ratio -------------------------------------------------------
def test_online_learn_weights_gradient_by_unclipped_behaviour_ratio(tmp_path):
    """Session-03 referee fix: the behaviour ratio π_T/β is NOT clipped (clipping made the estimator
    baseline-dependent with a possibly wrong sign); it is bounded by A/ε because β ≥ ε/A."""
    cfg = SimConfig(seed=4, policy="ebm", day_learning=True, runs_dir=str(tmp_path), clip=1.0)
    cfg.brain.act_mode = "egreedy"; cfg.brain.eps = 0.05
    L = Life(cfg)
    x = np.random.default_rng(0).normal(size=DIM).astype(np.float32)
    greedy = int(np.argmin(L.brain.F(x[None, :])[0]))
    for a, lb in ((greedy, np.log(1 - 0.05 + 0.05 / A)), ((greedy + 1) % A, np.log(0.05 / A))):
        L.trace = None
        g = L.brain.grad_logpi(x[None, :], np.array([a]))
        lpi = float(L.brain.logp(x[None, :], np.array([a]))[0])
        rho = np.exp(lpi - lb)
        L.online_learn(x, a, 0.0, lb, lpi)               # r = rbar = 0: theta stays, trace is set
        for k in g: assert np.allclose(L.trace[k], rho * g[k][0])
    assert 2.0 < rho <= A / 0.05                         # off-greedy action: ratio ~10, NOT clipped


def test_softmax_behaviour_ratio_is_exactly_one(tmp_path):
    cfg = SimConfig(seed=5, policy="ebm", day_learning=True, days=2, day_len=60, runs_dir=str(tmp_path))
    L = Life(cfg); L.run()
    X, a, R, lp, lpi = L.cache.batch_source(False)
    assert np.array_equal(lp, lpi) and np.all(np.exp(lpi - lp) == 1.0)


# ---- determinism and bit-for-bit default path ------------------------------------------------
def _theta_hash(brain):
    h = hashlib.sha256()
    for k in sorted(brain.theta): h.update(np.ascontiguousarray(brain.theta[k]).tobytes())
    return h.hexdigest()


def _life(tmp_path, seed, days, **kw):
    cfg = SimConfig(seed=seed, policy="ebm", days=days, day_learning=True,
                    runs_dir=str(tmp_path / f"{seed}-{len(list(tmp_path.iterdir()))}"))
    cfg.brain.act_mode = kw.get("act_mode", "softmax")
    cfg.sense.sign_features = kw.get("sign", False)
    L = Life(cfg); s = L.run()
    return s["ticks_alive"], _theta_hash(L.brain)


@pytest.mark.parametrize("sign", [False, True])
def test_determinism_per_seed_with_egreedy(tmp_path, sign):
    a = _life(tmp_path, 30, 2, act_mode="egreedy", sign=sign)
    b = _life(tmp_path, 30, 2, act_mode="egreedy", sign=sign)
    c = _life(tmp_path, 31, 2, act_mode="egreedy", sign=sign)
    assert a == b and a[1] != c[1]


# Recorded on main @ 2e30295 (EXP-01 code, before EXP-02 changes) with this venv's numpy 1.26:
# SimConfig(seed, policy="ebm", days, day_learning=True), all other defaults.
GOLDEN_MAIN = {(20, 2): (549, "1b9c5ca2126c790c17061deb8bc90b4463c881b49ccd6b75df6be16b79d7b1e5"),
               (21, 2): (700, "ad1ad2b18f8ddae1dc2d8fa3941b3bbfe00dc4b05952cef813da7f3f26f54dcb"),
               (22, 3): (958, "7ce7a257bc876cbaa65b3094a46d70a9128c5731e320765b3c12f01fecfbf88b"),
               (23, 3): (807, "49f4fd13f3a4aa33b8fc59983fddad6431fbfb60d433fc53dc9587dd51dc90d4")}


@pytest.mark.parametrize("seed,days", sorted(GOLDEN_MAIN))
def test_softmax_default_path_is_bit_for_bit_exp01(tmp_path, seed, days):
    assert _life(tmp_path, seed, days) == GOLDEN_MAIN[(seed, days)]
