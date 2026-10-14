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
        """Sample an action. Returns (a, F(x, ·), log π(a|x)); the log-prob is cached so that
        sleep replay can correct for the policy having moved since (off-policy ratio)."""
        Fx = self.F(x[None, :])[0]
        if getattr(self.cfg, "act_mode", "softmax") == "egreedy":
            # MINIMAL GUARD (learners builder, EXP-02): the senses+acting builder owns act_mode/eps
            # on BrainConfig; this branch exists only so learner="q" can act before that merge.
            # Behaviour prob per the contract: (1-eps)+eps/A on argmin-F (first index on ties),
            # eps/A otherwise.
            eps = getattr(self.cfg, "eps", 0.1)
            greedy = int(np.argmin(Fx))
            a = int(rng.integers(A)) if rng.random() < eps else greedy
            pa = (1.0 - eps) + eps / A if a == greedy else eps / A
            return a, Fx, float(np.log(pa))
        p = self.policy(x[None, :])[0]
        a = int(rng.choice(A, p=p))
        return a, Fx, float(np.log(p[a]))

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

    def grad_negF(self, X: np.ndarray, a: np.ndarray) -> dict:
        """Per-sample gradient of Q(x,a) = -F(x,a) w.r.t. theta (learner="q", EXP-02).
        Same dict shapes as grad_logpi, with coef = onehot(a) and no 1/T (no partition term:
        Q-learning regresses the energy of the taken action itself)."""
        N = X.shape[0]
        S = _sigmoid(self.pre(X))                           # (N, H, A)
        coef = np.zeros((N, A)); coef[np.arange(N), a] = 1.0
        g = {}
        g["b"] = coef
        g["w"] = coef[:, :, None] * X[:, None, :]
        SC = S * coef[:, None, :]
        g["v"] = SC
        g["c"] = SC.sum(axis=2)
        g["u"] = g["c"][:, :, None] * X[:, None, :]
        return g

    def Q(self, X: np.ndarray) -> np.ndarray:
        """Action values in "q" mode: Q(x, a) = -F(x, a), shape (N, A)."""
        return -self.F(X)

    def learn_q(self, X: np.ndarray, a: np.ndarray, y: np.ndarray, alpha: float) -> float:
        """Semi-gradient Q-learning step on a batch: theta += alpha * mean_i (y_i - Q_i) dQ_i/dtheta.
        y is held fixed (computed by the caller before the step). Returns mean |y - Q| before the
        step (the TD-error instrument)."""
        X = np.atleast_2d(X); a = np.asarray(a); y = np.asarray(y, dtype=np.float64)
        N = X.shape[0]
        td = y - self.Q(X)[np.arange(N), a]
        g = self.grad_negF(X, a)
        for k in self.theta:
            self.theta[k] += alpha * np.tensordot(td, g[k], axes=(0, 0)) / N
        return float(np.abs(td).mean())

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
