"""EXP-02 learner laws: critic TD(0), Q-mode gradient, Q-learning step, terminal transitions,
determinism, and the "pg" path left bit-for-bit as EXP-01 ran it."""
import hashlib
import numpy as np
import pytest
from creature.brain import Brain, BrainConfig, A
from creature.senses import DIM
from creature.sim import Cache, Critic, Life, SimConfig, q_targets


def _theta_hash(theta):
    h = hashlib.sha256()
    for k in sorted(theta):
        h.update(k.encode()); h.update(np.ascontiguousarray(theta[k]).tobytes())
    return h.hexdigest()[:16]


# ---- "pg" unchanged ----------------------------------------------------------------------------
# Golden values produced by the unmodified main (commit 2e30295) with the same code below, before
# any EXP-02 learner change. Float results are machine-specific (same laptop, numpy 1.26/BLAS);
# a mismatch on another machine is not by itself evidence of a behaviour change.
GOLDEN = {(False, 3): (1050, "3e021284c1d4dfa7"), (False, 11): (763, "817925640146d8cd"),
          (True, 3): (1050, "e25b820ed585b3e3"), (True, 11): (1050, "d90afe8bf6447e18")}


@pytest.mark.parametrize("day_learning,seed", list(GOLDEN))
def test_pg_path_bit_for_bit_unchanged(tmp_path, day_learning, seed):
    L = Life(SimConfig(seed=seed, policy="ebm", days=3, day_learning=day_learning, runs_dir=str(tmp_path)))
    s = L.run()
    assert (s["ticks_alive"], _theta_hash(L.brain.theta)) == GOLDEN[(day_learning, seed)]


# ---- critic --------------------------------------------------------------------------------------
def test_critic_td0_converges_to_analytic_value_on_two_state_chain():
    """s1 -> s2 with r=1, s2 -> s1 with r=0, forever. V1 = 1/(1-g^2), V2 = g/(1-g^2)."""
    g = 0.9
    cr = Critic(gamma=g)
    x1, x2 = np.array([1.0, 0.0]), np.array([0.0, 1.0])
    for _ in range(3000):
        cr.update(x1[None], [1.0], x2[None], [0.0], alpha=0.1)
        cr.update(x2[None], [0.0], x1[None], [0.0], alpha=0.1)
    V1, V2 = 1 / (1 - g * g), g / (1 - g * g)
    assert abs(cr.V(x1)[0] - V1) < 1e-3 and abs(cr.V(x2)[0] - V2) < 1e-3


def test_critic_terminal_transition_does_not_bootstrap():
    cr = Critic(gamma=0.9)
    cr.v = np.array([2.0, 5.0])
    x, xn = np.array([1.0, 0.0]), np.array([0.0, 1.0])
    assert cr.delta(x[None], [0.3], xn[None], [1.0])[0] == pytest.approx(0.3 - 2.0, abs=1e-12)
    assert cr.delta(x[None], [0.3], xn[None], [0.0])[0] == pytest.approx(0.3 + 0.9 * 5.0 - 2.0, abs=1e-12)


def test_critic_sizes_itself_from_first_x():
    cr = Critic(gamma=0.9)
    cr.V(np.ones(15)); assert cr.v.shape == (15,)


# ---- Q mode --------------------------------------------------------------------------------------
def test_grad_negF_matches_finite_differences():
    rng = np.random.default_rng(0)
    br = Brain(BrainConfig(dim=DIM, H0=3, T=0.7, init_scale=0.5), rng)
    X = rng.normal(size=(2, DIM)); acts = np.array([1, 2])
    g = br.grad_negF(X, acts)
    eps = 1e-6
    for i in range(2):
        for k in br.theta:
            it = np.nditer(br.theta[k], flags=["multi_index"])
            for _ in it:
                idx = it.multi_index; old = br.theta[k][idx]
                br.theta[k][idx] = old + eps; fp = -br.F(X[i:i + 1])[0, acts[i]]
                br.theta[k][idx] = old - eps; fm = -br.F(X[i:i + 1])[0, acts[i]]
                br.theta[k][idx] = old
                num = (fp - fm) / (2 * eps)
                assert abs(num - g[k][i][idx]) < 1e-6, (k, idx, num, g[k][i][idx])


def test_learn_q_lowers_squared_td_error_on_fixed_batch():
    rng = np.random.default_rng(1)
    br = Brain(BrainConfig(dim=DIM, H0=4, init_scale=0.3), rng)
    X = rng.normal(size=(32, DIM)); acts = rng.integers(A, size=32); y = rng.normal(size=32)
    def mse(): return float(((y - br.Q(X)[np.arange(32), acts]) ** 2).mean())
    e0 = mse()
    for _ in range(5):
        br.learn_q(X, acts, y, alpha=0.01)
    assert mse() < e0


def test_q_target_of_terminal_transition_is_r_exactly():
    rng = np.random.default_rng(2)
    br = Brain(BrainConfig(dim=DIM, init_scale=0.5), rng)
    Xn = 1e3 * rng.normal(size=(3, DIM))           # garbage next sensations must not matter
    r = np.array([0.1, -0.2, 0.05]); done = np.array([1.0, 0.0, 1.0])
    y = q_targets(br, r, Xn, done, 0.9)
    assert y[0] == r[0] and y[2] == r[2]
    assert y[1] == pytest.approx(r[1] + 0.9 * br.Q(Xn[1:2]).max())


def test_cache_marks_last_tick_of_day_done_and_links_next_sensation():
    c = Cache()
    xs = [np.full(DIM, float(t)) for t in range(5)]
    for t, x in enumerate(xs): c.push(x, t % A, 0.01 * t, -1.0)
    c.close_day(0.95, 3)
    X, a, r, lp, Xn, done, lpi = c.transitions(False)
    assert np.array_equal(done, [0, 0, 0, 0, 1])
    assert all(np.array_equal(Xn[t], xs[t + 1]) for t in range(4))
    assert np.allclose(r, 0.01 * np.arange(5)) and np.array_equal(a, [0, 1, 2, 0, 1])


def test_q_mode_acts_egreedy_and_does_not_mutate_caller_config(tmp_path):
    cfg = SimConfig(seed=1, policy="ebm", learner="q", days=1, runs_dir=str(tmp_path))
    L = Life(cfg)
    assert getattr(L.brain.cfg, "act_mode", None) == "egreedy"
    assert getattr(cfg.brain, "act_mode", "softmax") == "softmax"


# ---- determinism ---------------------------------------------------------------------------------
def _life(tmp_path, learner, seed):
    L = Life(SimConfig(seed=seed, policy="ebm", learner=learner, day_learning=True, days=3,
                       runs_dir=str(tmp_path)))
    return L.run(), _theta_hash(L.brain.theta), (None if L.critic is None else L.critic.v.copy())


@pytest.mark.parametrize("learner", ["ac", "q"])
def test_td_learners_are_deterministic_per_seed(tmp_path, learner):
    s1, h1, v1 = _life(tmp_path, learner, 5)
    s2, h2, v2 = _life(tmp_path, learner, 5)
    s3, h3, _ = _life(tmp_path, learner, 6)
    assert s1 == s2 and h1 == h2
    if v1 is not None: assert np.array_equal(v1, v2)
    assert h3 != h1


def test_ac_online_with_zero_critic_and_gamma0_equals_pg_online_with_rbar0(tmp_path):
    """A14: with V = 0 (alpha_v = 0) and gamma = 0, delta = r exactly, and the "ac" online actor step
    must equal the "pg" online step with rbar = 0, bit for bit. lam = 0 so both traces decay alike
    (ac decays at gamma*lam = 0; pg at lam)."""
    mk = lambda learner: Life(SimConfig(seed=7, policy="ebm", learner=learner, gamma=0.0, lam=0.0,
                                        alpha_v=0.0, day_learning=True, runs_dir=str(tmp_path)))
    Lac, Lpg = mk("ac"), mk("pg")
    Lpg._pg_lesson = lambda r: r          # rbar = 0
    theta0 = Lpg.brain.snapshot()
    for k in Lpg.brain.theta: assert np.array_equal(Lpg.brain.theta[k], Lac.brain.theta[k])
    rng = np.random.default_rng(0)
    for t in range(50):
        x = rng.normal(size=DIM).astype(np.float32); a = int(rng.integers(A)); r = float(rng.normal(0, 0.01))
        xn = rng.normal(size=DIM).astype(np.float32)
        Lpg.online_learn(x, a, r, 0.0)
        Lac.online_learn(x, a, r, 0.0, x_next=xn, done=False)
    for k in Lpg.brain.theta: assert np.array_equal(Lpg.brain.theta[k], Lac.brain.theta[k]), k
    assert not np.array_equal(Lpg.brain.theta["b"], theta0["b"])     # the step did move theta


def test_ac_online_lesson_is_raw_delta_not_standardised(tmp_path):
    """One fresh-trace step: theta moves by day_lr * delta * grad log pi, with no scale division."""
    L = Life(SimConfig(seed=8, policy="ebm", learner="ac", alpha_v=0.0, day_learning=True,
                       runs_dir=str(tmp_path)))
    rng = np.random.default_rng(1)
    L.critic.v = rng.normal(size=DIM)
    x, xn = rng.normal(size=DIM), rng.normal(size=DIM); a, r = 1, 0.02
    d = r + L.cfg.gamma * L.critic.v @ xn - L.critic.v @ x
    g = L.brain.grad_logpi(x[None, :], np.array([a])); before = L.brain.snapshot()
    L.online_learn(x, a, r, 0.0, x_next=xn, done=False)
    for k in before:
        assert np.allclose(L.brain.theta[k] - before[k], L.cfg.day_lr * d * g[k][0], atol=1e-12)
