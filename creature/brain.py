"""L3b — the brain: an energy-based model.

    F(x, a) = -b_a - w_a·x - Σ_h softplus(c_h + u_h·x + v_{h,a})

F is the free energy of a conditional RBM whose binary hidden units have been summed out. Each
hidden unit h is a small model: it looks at the sensation through u_h and at the action through
v_h, and lowers the energy by softplus(...) when both fit. u and v are "the connections".

Acting:   π(a|x) = softmax_a(-F(x,a) / T).  Three actions, so the partition is exact.
Learning: Δθ = lr · R · ∂ log π(a|x) / ∂θ
          = (lr·R/T) · [ -∂F(x,a)/∂θ  +  Σ_{a'} π(a'|x) ∂F(x,a')/∂θ ]
          positive phase: lower the energy of what was done, in proportion to the body's lesson R;
          negative phase: raise the energy of what the brain itself would have done.
This is the policy gradient for a Boltzmann policy (REINFORCE); the body's drive change is R.
Growth: add_units() appends hidden units with small random weights.
"""
from dataclasses import dataclass
import numpy as np

ACTIONS = ("LEFT", "RIGHT", "FORWARD")
A = len(ACTIONS)


@dataclass
class BrainConfig:
    dim: int = 12
    H0: int = 4
    T: float = 0.3                 # pilot 01e: 0.3 > 0.5 > 1.0; 0.1 collapses (too greedy)
    lr: float = 1.0                # pilot 01d (seeds 0-7 burned): batch-mean lr; 3 epochs > 10
    init_scale: float = 0.01       # near-uniform policy at birth (pilot 01: a turning bias traps
                                   # an untrained creature in loops; see findings)
    act_mode: str = "softmax"      # "softmax": sample π_T | "egreedy": argmin F w.p. 1-ε, else uniform
                                   # (EXP-02). Learning stays the softmax PG at T in both modes; the
                                   # behaviour log-prob returned by act() feeds the IS ratio π_T/β.
    eps: float = 0.1               # exploration rate for act_mode="egreedy" (= TabularQ's ε)


def _softplus(z):
    return np.logaddexp(0.0, z)


def _sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


class Brain:
    def __init__(self, cfg: BrainConfig, rng: np.random.Generator, theta: dict | None = None):
        self.cfg = cfg
        if theta is None:
            s = cfg.init_scale
            theta = {"b": np.zeros(A), "w": rng.normal(0, s, (A, cfg.dim)),
                     "c": np.zeros(cfg.H0), "u": rng.normal(0, s, (cfg.H0, cfg.dim)),
                     "v": rng.normal(0, s, (cfg.H0, A))}
        self.theta = {k: np.asarray(v, dtype=np.float64).copy() for k, v in theta.items()}

    @property
    def H(self) -> int:
        return self.theta["c"].shape[0]

    # ---- energy ----------------------------------------------------------------------------
    def pre(self, X: np.ndarray) -> np.ndarray:
        """Hidden pre-activations, shape (N, H, A)."""
        th = self.theta
        return th["c"][None, :, None] + (X @ th["u"].T)[:, :, None] + th["v"][None, :, :]

    def F(self, X: np.ndarray) -> np.ndarray:
        """Free energy for every action, shape (N, A). X is (N, dim)."""
        X = np.atleast_2d(X)
        th = self.theta
        return -th["b"][None, :] - X @ th["w"].T - _softplus(self.pre(X)).sum(axis=1)

    def policy(self, X: np.ndarray) -> np.ndarray:
        z = -self.F(X) / self.cfg.T
        z -= z.max(axis=1, keepdims=True)
        p = np.exp(z)
        return p / p.sum(axis=1, keepdims=True)

    def act(self, x: np.ndarray, rng: np.random.Generator) -> tuple[int, np.ndarray, float]:
        """Choose an action. Returns (a, F(x, ·), log β(a|x)) where β is the BEHAVIOUR policy that
        actually chose a. The log-prob is cached so that learning can importance-correct toward
        π_T (sleep replay: the policy moved since; egreedy: β differs from π_T even online).

        RNG draw order (determinism per seed is a law):
          softmax: exactly one rng.choice(A, p=π_T) (one uniform double internally).
          egreedy: exactly one rng.random(); if it is < ε, then exactly one rng.integers(A) (the
                   explore action, uniform over all A, which may coincide with the greedy one);
                   otherwise no further draw. Same order as TabularQ.act.
        egreedy greedy action = argmin_a F(x, a), ties broken by the first index (np.argmin).
        log β = log((1-ε) + ε/A) on the greedy action, log(ε/A) on every other action."""
        Fx = self.F(x[None, :])[0]
        if self.cfg.act_mode == "softmax":
            p = self.policy(x[None, :])[0]
            a = int(rng.choice(A, p=p))
            return a, Fx, float(np.log(p[a]))
        if self.cfg.act_mode == "egreedy":
            eps = self.cfg.eps
            greedy = int(np.argmin(Fx))
            a = int(rng.integers(A)) if rng.random() < eps else greedy
            pb = (1.0 - eps) + eps / A if a == greedy else eps / A
            return a, Fx, float(np.log(pb))
        raise ValueError(f"unknown act_mode {self.cfg.act_mode!r}")

    def logp(self, X: np.ndarray, a: np.ndarray) -> np.ndarray:
        P = self.policy(X)
        return np.log(P[np.arange(len(a)), a])

    def entropy(self, X: np.ndarray) -> float:
        P = self.policy(X)
        return float(-(P * np.log(P + 1e-12)).sum(axis=1).mean())

    # ---- learning --------------------------------------------------------------------------
    def grad_logpi(self, X: np.ndarray, a: np.ndarray) -> dict:
        """Per-sample gradient of log π(a|x), summed over the batch and weighted later by R.
        Returns dict of arrays shaped like theta, for a batch X (N,dim), a (N,) ints."""
        N = X.shape[0]
        th = self.theta
        P = self.policy(X)                                  # (N, A)
        S = _sigmoid(self.pre(X))                           # (N, H, A)  = ∂softplus
        onehot = np.zeros((N, A)); onehot[np.arange(N), a] = 1.0
        # weight on each action: +1 for the taken action, -π(a') for the fantasy.
        # ∂(-F)/∂θ terms get +, so coefficient per action is (onehot - P).
        coef = (onehot - P) / self.cfg.T                    # (N, A)
        g = {}
        g["b"] = coef                                        # (N, A)
        g["w"] = coef[:, :, None] * X[:, None, :]            # (N, A, dim)
        SC = S * coef[:, None, :]                            # (N, H, A)
        g["v"] = SC                                          # (N, H, A)
        g["c"] = SC.sum(axis=2)                              # (N, H)
        g["u"] = g["c"][:, :, None] * X[:, None, :]          # (N, H, dim)
        return g

    def learn(self, X: np.ndarray, a: np.ndarray, R: np.ndarray, lr: float | None = None,
              logp_old: np.ndarray | None = None, clip: float = 0.2) -> float:
        """One contrastive update on a batch of (sensation, action, lesson).
        If logp_old is given (sleep replay), each sample is weighted by the clipped importance
        ratio π_now(a|x)/π_old(a|x) ∈ [1-clip, 1+clip] (PPO-style; R1 research/03 §Q2).
        Returns the fraction of samples whose ratio was clipped (an instrument)."""
        lr = self.cfg.lr if lr is None else lr
        g = self.grad_logpi(X, a)
        N = X.shape[0]
        clipped = 0.0
        if logp_old is not None:
            rho = np.exp(self.logp(X, a) - logp_old)
            clipped = float(((rho < 1 - clip) | (rho > 1 + clip)).mean())
            R = R * np.clip(rho, 1 - clip, 1 + clip)
        for k in self.theta:
            self.theta[k] += lr * np.tensordot(R, g[k], axes=(0, 0)) / N
        return clipped

    def downscale(self, delta: float):
        """Sleep's synaptic downscaling: shrink the connections (w, u, v) a little. Biases b and c
        are left alone: decaying b pulls the policy toward uniform, decaying c shifts every hidden
        unit's offset (R1, research/03 §Q5)."""
        for k in ("w", "u", "v"):
            self.theta[k] *= (1.0 - delta)

    # ---- growth ----------------------------------------------------------------------------
    def add_units(self, n: int, rng: np.random.Generator):
        """Born policy-neutral: v = 0 means the new unit adds the same term to every action's
        energy, so the policy is unchanged at birth (R1, research/03 §Q5). It only starts to
        matter once learning gives it an action preference."""
        s = self.cfg.init_scale
        th = self.theta
        th["c"] = np.concatenate([th["c"], np.zeros(n)])
        th["u"] = np.vstack([th["u"], rng.normal(0, s, (n, self.cfg.dim))])
        th["v"] = np.vstack([th["v"], np.zeros((n, A))])

    def snapshot(self) -> dict:
        return {k: v.copy() for k, v in self.theta.items()}
