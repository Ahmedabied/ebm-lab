"""Brain laws: the gradient is the gradient; weights change actions; learning moves behaviour."""
import numpy as np
from creature.brain import Brain, BrainConfig, A
from creature.senses import DIM


def _logpi(brain, x, a):
    return np.log(brain.policy(x[None, :])[0, a])


def test_gradient_matches_finite_differences():
    rng = np.random.default_rng(0)
    br = Brain(BrainConfig(dim=DIM, H0=3, T=0.7), rng)
    x = rng.normal(size=DIM); a = 1
    g = br.grad_logpi(x[None, :], np.array([a]))
    eps = 1e-6
    for k in br.theta:
        it = np.nditer(br.theta[k], flags=["multi_index"])
        for _ in it:
            idx = it.multi_index
            old = br.theta[k][idx]
            br.theta[k][idx] = old + eps; fp = _logpi(br, x, a)
            br.theta[k][idx] = old - eps; fm = _logpi(br, x, a)
            br.theta[k][idx] = old
            num = (fp - fm) / (2 * eps)
            assert abs(num - g[k][0][idx]) < 1e-6, (k, idx, num, g[k][0][idx])


def test_policy_is_a_distribution_and_depends_on_weights():
    rng = np.random.default_rng(1)
    br = Brain(BrainConfig(dim=DIM), rng)
    X = rng.normal(size=(5, DIM))
    P = br.policy(X)
    assert np.allclose(P.sum(axis=1), 1.0) and (P > 0).all()
    P0 = P.copy()
    br.theta["b"][2] += 3.0
    assert br.policy(X)[:, 2].mean() > P0[:, 2].mean()


def test_learning_moves_behaviour_toward_rewarded_action():
    """Law 5: a learned thing must change an action. Reward FORWARD in a fixed sensation and the
    probability of FORWARD must rise; punish it and it must fall."""
    rng = np.random.default_rng(2)
    br = Brain(BrainConfig(dim=DIM, lr=0.5), rng)
    x = rng.normal(size=DIM)
    p0 = br.policy(x[None, :])[0, 2]
    for _ in range(20):
        br.learn(x[None, :], np.array([2]), np.array([1.0]))
    p1 = br.policy(x[None, :])[0, 2]
    assert p1 > p0
    for _ in range(60):
        br.learn(x[None, :], np.array([2]), np.array([-1.0]))
    assert br.policy(x[None, :])[0, 2] < p1


def test_zero_lesson_changes_nothing():
    rng = np.random.default_rng(3)
    br = Brain(BrainConfig(dim=DIM), rng)
    before = br.snapshot()
    br.learn(rng.normal(size=(4, DIM)), np.array([0, 1, 2, 0]), np.zeros(4))
    for k in before: assert np.array_equal(before[k], br.theta[k])


def test_growth_adds_units_and_keeps_old_behaviour_close():
    rng = np.random.default_rng(4)
    br = Brain(BrainConfig(dim=DIM, H0=2, init_scale=0.1), rng)
    X = rng.normal(size=(8, DIM)); P0 = br.policy(X)
    br.add_units(3, rng)
    assert br.H == 5 and br.theta["u"].shape == (5, DIM) and br.theta["v"].shape == (5, A)
    assert np.allclose(br.policy(X), P0)            # born policy-neutral (v = 0): identical policy


def test_same_seed_same_brain_same_actions():
    def run(seed):
        rng = np.random.default_rng(seed)
        br = Brain(BrainConfig(dim=DIM), rng)
        return [br.act(rng.normal(size=DIM), rng)[0] for _ in range(30)]
    assert run(9) == run(9) and run(9) != run(10)


def test_importance_ratio_is_one_when_policy_unchanged_and_clips_when_it_moved():
    rng = np.random.default_rng(5)
    br = Brain(BrainConfig(dim=DIM, lr=0.0), rng)
    X = rng.normal(size=(6, DIM)); a = np.array([0, 1, 2, 0, 1, 2])
    lp = br.logp(X, a)
    assert br.learn(X, a, np.ones(6), logp_old=lp) == 0.0
    br.theta["b"][0] += 5.0
    assert br.learn(X, a, np.ones(6), logp_old=lp) > 0.0


def test_constant_lesson_teaches_nothing_even_at_day_end():
    """The tail bootstrap: a day of constant drift must give zero credit everywhere."""
    from creature.sim import Cache
    c = Cache()
    for t in range(100):
        c.push(np.zeros(DIM), 0, -0.01, 0.0)
    c.close_day(0.95, 3)
    R = c.days[-1][2]
    assert np.abs(R).max() < 1e-9
