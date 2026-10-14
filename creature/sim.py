"""L4 — a life: days of acting and caching, nights of sleep, growth, and the log.

One creature, one world, one RNG. Everything the creature does passes through here, and
everything that happens is written to runs/<label>/<seed>/ so the viewer and the metrics read
the same record. Logging never draws from the RNG.
"""
from dataclasses import dataclass, field, asdict, fields, replace
import hashlib, json, os, time
import numpy as np
from .world import World, WorldConfig
from .body import Body, BodyConfig
from .senses import Senses, SenseConfig, DIM
from .brain import Brain, BrainConfig, ACTIONS, A
from . import baselines

LEFT, RIGHT, FORWARD = 0, 1, 2


@dataclass
class SimConfig:
    seed: int = 0
    label: str = "smoke"
    policy: str = "ebm"            # ebm | random | braitenberg | oracle | tabular_q
    days: int = 20
    day_len: int = 300             # EXP-00 calibration (decisions/0001)
    sleep_len: int = 50            # ticks the body metabolises while asleep
    turn: float = np.deg2rad(30.0)
    speed: float = 1.0
    # learning
    lam: float = 0.95              # credit decay: R_t = Σ λ^k r_{t+k}; ~20 ticks of look-ahead
    day_learning: bool = False     # online REINFORCE with an eligibility trace (matched control)
    day_lr: float = 1.0 / 64       # online per-sample step = sleep's batch-mean lr / batch (matched)
    sleep: str = "replay"          # replay | today | noise | none
    sleep_epochs: int = 3
    batch: int = 64
    downscale: float = 0.01
    cache_days: int = 3
    clip: float = 1.0              # importance-ratio clip half-width for replay; pilot 01d: 1.0 > 0.2
    # EXP-02 learners (interface contract in experiments/EXP-02-prereg.md)
    learner: str = "pg"            # pg (EXP-01 day-return REINFORCE) | ac (linear critic, TD error
                                   # lesson) | q (Q = -F, Q-learning, epsilon-greedy acting)
    gamma: float = 0.9             # TD discount for "ac" and "q" (tabular Q's gamma)
    alpha_v: float = 0.03          # critic step size ("ac"); pilot 02a (seeds 20-27, max mean
                                   # ticks_alive over {0.01,0.03,0.1,0.3}; CIs all overlap)
    alpha_q: float = 0.1           # Q-mode step size ("q"); pilot 02a (seeds 20-27, max mean
                                   # ticks_alive over {0.003,0.01,0.03,0.1}: top EDGE of the grid)
    scale_decay: float = 0.99      # "ac": EMA decay of delta^2 for the actor's running scale
                                   # (~100-tick memory, i.e. a third of a day)
    # growth
    growth: str = "surprise"       # surprise | timer | none
    growth_thresh: float = 0.005   # std of the day's raw lessons above this -> eventful day -> grow
    growth_every: int = 3          # for timer: grow every N days
    growth_max: int = 32
    # log
    snap_every: int = 20
    runs_dir: str = "runs"
    world: WorldConfig = field(default_factory=WorldConfig)
    body: BodyConfig = field(default_factory=BodyConfig)
    sense: SenseConfig = field(default_factory=SenseConfig)
    brain: BrainConfig = field(default_factory=lambda: BrainConfig(dim=DIM))


def source_hash() -> str:
    h = hashlib.sha256()
    d = os.path.dirname(__file__)
    for f in sorted(os.listdir(d)):
        if f.endswith(".py"):
            h.update(open(os.path.join(d, f), "rb").read())
    return h.hexdigest()[:16]


def git_commit() -> str:
    try:
        import subprocess
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"],
                                       cwd=os.path.dirname(os.path.dirname(__file__)),
                                       stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return "unknown"


class Critic:
    """Linear state-value critic for learner="ac": V(x) = v.x (x carries a bias dim).
    v is NOT part of brain.theta. It is sized lazily from the first x it sees, so it follows
    whatever sensation dim the senses produce (12, or 15 with sign features).
    It also keeps the running scale of the TD error used to standardise the actor's lesson:
    m <- beta*m + (1-beta)*mean(delta^2), bias-corrected like Adam (m / (1 - beta^n)), so the
    first lessons are not inflated by a zero-initialised EMA."""
    def __init__(self, gamma: float, beta: float = 0.99, floor: float = 1e-3):
        self.gamma, self.beta, self.floor = gamma, beta, floor
        self.v = None; self.m = 0.0; self.n = 0
    def _ensure(self, d: int):
        if self.v is None:
            self.v = np.zeros(d)
        elif self.v.shape[0] != d:
            raise ValueError(f"critic sized for dim {self.v.shape[0]}, got {d}")
    def V(self, X) -> np.ndarray:
        X = np.atleast_2d(np.asarray(X, dtype=np.float64)); self._ensure(X.shape[1])
        return X @ self.v
    def delta(self, X, r, Xn, done) -> np.ndarray:
        """delta = r + gamma*(1-done)*V(x') - V(x); a terminal transition never reads V(x')."""
        r = np.asarray(r, dtype=np.float64); done = np.asarray(done, dtype=np.float64)
        boot = np.where(done > 0, 0.0, self.V(Xn))
        return r + self.gamma * boot - self.V(X)
    def update(self, X, r, Xn, done, alpha: float) -> np.ndarray:
        """TD(0): v += alpha * mean_i delta_i x_i (delta from the pre-step v). Returns delta and
        folds it into the running scale."""
        X = np.atleast_2d(np.asarray(X, dtype=np.float64))
        d = self.delta(X, r, Xn, done)
        self.v += alpha * (d @ X) / X.shape[0]
        self.m = self.beta * self.m + (1.0 - self.beta) * float(np.mean(d * d)); self.n += 1
        return d
    def scale(self) -> float:
        if self.n == 0: return 1.0
        return max(float(np.sqrt(self.m / (1.0 - self.beta ** self.n))), self.floor)
    def state(self):
        return (None if self.v is None else self.v.copy(), self.m, self.n)
    def restore(self, st):
        v, self.m, self.n = st; self.v = None if v is None else v.copy()


def q_targets(brain, r, Xn, done, gamma: float) -> np.ndarray:
    """y = r + gamma*(1-done)*max_a' Q(x', a'), Q = -F. A terminal transition's target is r."""
    r = np.asarray(r, dtype=np.float64); done = np.asarray(done, dtype=np.float64)
    boot = np.where(done > 0, 0.0, brain.Q(np.atleast_2d(Xn)).max(axis=1))
    return r + gamma * boot


class Cache:
    """The day's episodes: what was sensed, what was done, what the body said.
    Each closed day also holds its transitions (x, a, r, logp, x_next, done): x_next is the next
    waking tick's sensation, and the last tick of a day has done=True (no bootstrap across the
    night; its x_next is a placeholder copy of x and is never read)."""
    def __init__(self):
        self.days: list[tuple[np.ndarray, np.ndarray, np.ndarray]] = []   # (X, a, R) per day
        self.X, self.a, self.r, self.lp = [], [], [], []
    def push(self, x, a, r, logp):
        self.X.append(x); self.a.append(a); self.r.append(r); self.lp.append(logp)
    def close_day(self, lam: float, keep_days: int):
        """Turn raw lessons r_t into credited lessons R_t = Σ λ^k r_{t+k}, baseline-subtracted.
        The tail is bootstrapped with the day's mean lesson continuing forever (mean_r/(1-λ)), so
        the last ticks of a day are not credited as if the metabolic drift had stopped."""
        if not self.r:
            return 0.0
        r = np.array(self.r, dtype=np.float64)
        R = np.zeros_like(r); acc = r.mean() / (1.0 - lam)
        for t in range(len(r) - 1, -1, -1):
            acc = r[t] + lam * acc; R[t] = acc
        R -= R.mean()
        sd = R.std()
        if sd < 1e-6:                  # a day in which nothing happened teaches nothing
            R[:] = 0.0
        else:                          # advantage normalisation: the body's lessons are O(0.01),
            R /= max(sd, 1e-3)         # the policy needs O(1) energy gaps; scale-free updates
        X = np.array(self.X)
        Xn = np.concatenate([X[1:], X[-1:]])
        done = np.zeros(len(r)); done[-1] = 1.0
        self.days.append((X, np.array(self.a), R, np.array(self.lp, dtype=np.float64), r, Xn, done))
        self.days = self.days[-keep_days:]
        self.X, self.a, self.r, self.lp = [], [], [], []
        # "surprise" for the growth trigger: how spiky the day's raw lessons were (std of r, in
        # drive units), i.e. how much happened that the body cared about
        return float(r.std())
    def batch_source(self, today_only: bool):
        days = self.days[-1:] if today_only else self.days
        return tuple(np.concatenate([d[i] for d in days]) for i in range(4))
    def transitions(self, today_only: bool):
        """(X, a, r, logp, X_next, done) over the cached days, for the TD learners."""
        days = self.days[-1:] if today_only else self.days
        return tuple(np.concatenate([d[i] for d in days]) for i in (0, 1, 4, 3, 5, 6))


class Life:
    def __init__(self, cfg: SimConfig):
        self.cfg = cfg
        self.rng = np.random.default_rng(cfg.seed)
        self.world = World(cfg.world, self.rng)
        self.body = Body(cfg.body)
        self.senses = Senses(cfg.sense)
        self.y = cfg.world.H / 2; self.x = cfg.world.W / 2
        self.heading = float(self.rng.uniform(0, 2 * np.pi))
        if cfg.learner not in ("pg", "ac", "q"):
            raise ValueError(f"unknown learner {cfg.learner!r}")
        bcfg = cfg.brain
        if cfg.policy == "ebm" and cfg.learner == "q":
            # Q mode acts epsilon-greedy on Q = -F (contract). The act_mode field belongs to the
            # senses+acting builder; until it exists on BrainConfig, set it on a copy (Brain.act
            # reads it with getattr). The caller's config object is never mutated.
            if "act_mode" in {f.name for f in fields(bcfg)}:
                bcfg = replace(bcfg, act_mode="egreedy")
            else:
                bcfg = replace(bcfg); bcfg.act_mode = "egreedy"
        self.brain = Brain(bcfg, self.rng) if cfg.policy == "ebm" else None
        self.critic = Critic(cfg.gamma, cfg.scale_decay) if (self.brain and cfg.learner == "ac") else None
        self._pending = None               # "ac"/"q" online: (x, a, r, logp) awaiting its x_next
        self._td_day = []                  # online |TD error| this day (instrument)
        self.policy = None if self.brain else baselines.make(cfg.policy, self.rng)
        self.cache = Cache()
        self.trace = None
        self.instr = {}
        self.rbar = 0.0                    # running baseline for online learning
        self.t = 0; self.day = 0
        self.dir = os.path.join(cfg.runs_dir, cfg.label, str(cfg.seed))
        os.makedirs(self.dir, exist_ok=True)
        self._ticks = open(os.path.join(self.dir, "ticks.jsonl"), "w")
        self._events = open(os.path.join(self.dir, "events.jsonl"), "w")
        self._snaps = []; self._snap_t = []; self._brains = []
        self.totals = {"food": 0.0, "poison": 0.0, "ticks_alive": 0, "drive_sum": 0.0,
                       "first_food_t": None, "poison_bites_after_first": 0}
        self._first_poison = False

    # ---- helpers ---------------------------------------------------------------------------
    def event(self, kind, **kw):
        self._events.write(json.dumps({"t": self.t, "day": self.day, "kind": kind, **kw}) + "\n")

    def move(self, a):
        c = self.cfg
        if a == LEFT: self.heading += c.turn
        elif a == RIGHT: self.heading -= c.turn
        self.heading %= 2 * np.pi
        self.y = (self.y + c.speed * np.sin(self.heading)) % c.world.H
        self.x = (self.x + c.speed * np.cos(self.heading)) % c.world.W

    def n_units(self):
        return self.brain.H if self.brain else 0

    # ---- one waking tick -------------------------------------------------------------------
    def wake_tick(self):
        sens = self.senses.sense(self.world, self.y, self.x, self.heading, self.body.state(), self.rng)
        x = sens["x"]
        if self._pending is not None:      # the previous tick's transition now has its x_next
            self.online_learn(*self._pending, x_next=x, done=False); self._pending = None
        if self.brain:
            a, Fx, logp = self.brain.act(x, self.rng)
        else:
            a, Fx = self.policy.act(sens, self.world, self.y, self.x, self.heading, self.rng); logp = 0.0
        self.move(a)
        food, poison = self.world.eat_at(self.y, self.x)
        r = self.body.tick(True, self.n_units(), food, poison)
        self.cache.push(x, a, r, logp)
        if self.brain and self.cfg.day_learning:
            if self.cfg.learner == "pg":
                self.online_learn(x, a, r, logp)
            else:
                self._pending = (x, a, r, logp)
        if self.policy is not None:
            sens2 = {"left": sens["left"], "right": sens["right"], "body": self.body.state()}
            self.policy.learn_tick(sens2, r)
        self.world.step(); self.world.regrow()
        # books and log (no RNG here)
        D = self.body.drive()
        self.totals["food"] += food; self.totals["poison"] += poison
        self.totals["ticks_alive"] += 1; self.totals["drive_sum"] += D
        if food > 0 and self.totals["first_food_t"] is None: self.totals["first_food_t"] = self.t
        if poison > 0:
            if self._first_poison: self.totals["poison_bites_after_first"] += 1
            self._first_poison = True
        if food > 0: self.event("eat", food=round(food, 4))
        if poison > 0: self.event("poison", poison=round(poison, 4))
        self._ticks.write(json.dumps({
            "t": self.t, "day": self.day, "phase": "wake", "y": round(float(self.y), 3),
            "x": round(float(self.x), 3), "h": round(float(self.heading), 3), "a": int(a),
            "E": round(self.body.E, 4), "X": round(self.body.X, 4), "D": round(D, 4),
            "r": round(float(r), 5),
            "F": None if Fx is None else [round(float(v), 4) for v in Fx],
            "H": self.n_units()}) + "\n")
        if self.t % self.cfg.snap_every == 0:
            self._snaps.append(self.world.fields.astype(np.float16)); self._snap_t.append(self.t)
        self.t += 1

    def online_learn(self, x, a, r, logp, x_next=None, done=False):
        """One online update. "pg": REINFORCE with an eligibility trace, applied at the tick itself
        (x_next/done unused). "ac"/"q": applied one tick late, once x_next is known (or at day's end
        with done=True). logp (behaviour log-prob) is accepted for the IS-weighting merge; the
        learners here do not use it online (the "ac" arm acts by softmax, so the ratio is ~1)."""
        if self.cfg.learner == "ac":
            return self._online_ac(x, a, r, x_next, done)
        if self.cfg.learner == "q":
            return self._online_q(x, a, r, x_next, done)
        g = self.brain.grad_logpi(x[None, :], np.array([a]))
        if self.trace is None:
            self.trace = {k: np.zeros_like(self.brain.theta[k]) for k in self.brain.theta}
        for k in self.trace:
            self.trace[k] = self.cfg.lam * self.trace[k] + g[k][0]
        self.rbar = 0.99 * self.rbar + 0.01 * r
        for k in self.brain.theta:
            self.brain.theta[k] += self.cfg.day_lr * (r - self.rbar) * self.trace[k]

    def _online_ac(self, x, a, r, x_next, done):
        """Actor-critic(lambda), Sutton & Barto 2018 sec 13.5: critic TD(0); actor trace decays at
        gamma*lam (the textbook AC(lambda) trace; with a TD-error lesson a decay above gamma would
        over-count credit). Lesson = delta / running scale. The trace is cleared at a terminal
        transition (end of day) and on growth."""
        xn = x if x_next is None else x_next
        d = self.critic.update(x[None, :], [r], xn[None, :], [float(done)], self.cfg.alpha_v)[0]
        self._td_day.append(abs(float(d)))
        lesson = d / self.critic.scale()
        g = self.brain.grad_logpi(x[None, :], np.array([a]))
        if self.trace is None:
            self.trace = {k: np.zeros_like(self.brain.theta[k]) for k in self.brain.theta}
        decay = self.cfg.gamma * self.cfg.lam
        for k in self.trace:
            self.trace[k] = decay * self.trace[k] + g[k][0]
        for k in self.brain.theta:
            self.brain.theta[k] += self.cfg.day_lr * lesson * self.trace[k]
        if done:
            self.trace = None

    def _online_q(self, x, a, r, x_next, done):
        """Online Q-learning on Q = -F: y = r + gamma*(1-done)*max Q(x'), one semi-gradient step."""
        xn = x if x_next is None else x_next
        y = q_targets(self.brain, [r], xn[None, :], [float(done)], self.cfg.gamma)
        self._td_day.append(self.brain.learn_q(x[None, :], np.array([a]), y, self.cfg.alpha_q))

    def _flush_pending(self):
        """End of the waking day: the last transition is terminal (no bootstrap over the night)."""
        if self._pending is not None:
            self.online_learn(*self._pending, x_next=None, done=True); self._pending = None

    # ---- night -----------------------------------------------------------------------------
    def sleep(self, surprise: float):
        c = self.cfg
        self.event("sleep_start", surprise=round(surprise, 5), H=self.n_units())
        if self.brain and c.sleep != "none" and self.cache.days:
            if c.sleep == "noise":
                # perturb by the same norm a replay night would have moved the weights
                before = self.brain.snapshot()
                cst = self.critic.state() if self.critic else None
                self._replay(today_only=False)
                if self.critic: self.critic.restore(cst)
                norm = np.sqrt(sum(((self.brain.theta[k] - before[k]) ** 2).sum() for k in before))
                self.brain.theta = before
                for k in self.brain.theta:
                    self.brain.theta[k] += self.rng.normal(0, 1, self.brain.theta[k].shape)
                total = np.sqrt(sum(((self.brain.theta[k] - before[k]) ** 2).sum() for k in before))
                for k in self.brain.theta:
                    self.brain.theta[k] = before[k] + (self.brain.theta[k] - before[k]) * (norm / max(total, 1e-12))
            else:
                self._replay(today_only=(c.sleep == "today"))
            self.brain.downscale(c.downscale)
        # the body still metabolises; no eating, no moving
        for _ in range(c.sleep_len):
            r = self.body.tick(False, self.n_units(), 0.0, 0.0)
            self.world.step(); self.world.regrow()
            self.totals["ticks_alive"] += 1; self.totals["drive_sum"] += self.body.drive()
            self._ticks.write(json.dumps({"t": self.t, "day": self.day, "phase": "sleep",
                "y": round(float(self.y), 3), "x": round(float(self.x), 3), "h": round(float(self.heading), 3),
                "a": None, "E": round(self.body.E, 4), "X": round(self.body.X, 4),
                "D": round(self.body.drive(), 4), "r": round(float(r), 5), "F": None, "H": self.n_units()}) + "\n")
            self.t += 1
            if not self.body.alive: break
        # growth
        if self.brain and self.body.alive and self.n_units() < c.growth_max:
            grow = ((c.growth == "surprise" and surprise > c.growth_thresh)
                    or (c.growth == "timer" and (self.day + 1) % c.growth_every == 0))
            if grow:
                self.brain.add_units(1, self.rng); self.event("grow", H=self.n_units())
                self.trace = None          # the online eligibility trace must match the new shape
        if self.brain: self._brains.append(self.brain.snapshot())
        self.event("sleep_end", H=self.n_units(), **getattr(self, "instr", {}))

    def _replay(self, today_only: bool):
        """Interleaved replay: every cached day shuffled together, importance-corrected."""
        c = self.cfg
        if c.learner != "pg":
            return self._replay_td(today_only)
        X, a, R, lp = self.cache.batch_source(today_only)
        n = len(a); clipped = []
        for _ in range(c.sleep_epochs):
            order = self.rng.permutation(n)
            for i in range(0, n, c.batch):
                idx = order[i:i + c.batch]
                clipped.append(self.brain.learn(X[idx], a[idx], R[idx], logp_old=lp[idx], clip=c.clip))
        self.instr = {"clip_frac": round(float(np.mean(clipped)), 4),
                      "entropy": round(self.brain.entropy(X), 4),
                      "w_norm": round(float(np.sqrt(sum((self.brain.theta[k] ** 2).sum() for k in ("w", "u", "v")))), 4)}

    def _replay_td(self, today_only: bool):
        """Night replay for "ac" and "q": cached transitions, all days shuffled together, same
        epochs/batch as "pg". "ac": per minibatch, delta from the CURRENT critic, critic TD(0) step
        (batch mean, step alpha_v), actor step on delta/scale, IS-clipped as in "pg".
        "q": per minibatch, targets from the current Q, one learn_q step (batch mean, step alpha_q),
        no IS weighting (Q-learning is off-policy)."""
        c = self.cfg
        X, a, r, lp, Xn, done = self.cache.transitions(today_only)
        n = len(a); clipped = []; tds = []
        for _ in range(c.sleep_epochs):
            order = self.rng.permutation(n)
            for i in range(0, n, c.batch):
                idx = order[i:i + c.batch]
                if c.learner == "ac":
                    d = self.critic.update(X[idx], r[idx], Xn[idx], done[idx], c.alpha_v)
                    tds.append(float(np.abs(d).mean()))
                    clipped.append(self.brain.learn(X[idx], a[idx], d / self.critic.scale(),
                                                    logp_old=lp[idx], clip=c.clip))
                else:
                    y = q_targets(self.brain, r[idx], Xn[idx], done[idx], c.gamma)
                    tds.append(self.brain.learn_q(X[idx], a[idx], y, c.alpha_q))
        self.instr = {"clip_frac": round(float(np.mean(clipped)), 4) if clipped else None,
                      "entropy": round(self.brain.entropy(X), 4),
                      "w_norm": round(float(np.sqrt(sum((self.brain.theta[k] ** 2).sum() for k in ("w", "u", "v")))), 4),
                      "td_abs": round(float(np.mean(tds)), 6),
                      "td_abs_day": round(float(np.mean(self._td_day)), 6) if self._td_day else None}
        self._td_day = []

    # ---- the life --------------------------------------------------------------------------
    def run(self) -> dict:
        c = self.cfg
        t0 = time.time()
        for self.day in range(c.days):
            for _ in range(c.day_len):
                self.wake_tick()
                if not self.body.alive: break
            if not self.body.alive: break
            self._flush_pending()
            surprise = self.cache.close_day(c.lam, c.cache_days)
            self.sleep(surprise)
            if not self.body.alive: break
        self.event("death" if not self.body.alive else "end", E=round(self.body.E, 4))
        self._ticks.close(); self._events.close()
        np.savez_compressed(os.path.join(self.dir, "fields.npz"),
                            t=np.array(self._snap_t), fields=np.array(self._snaps))
        if self._brains:
            np.savez_compressed(os.path.join(self.dir, "brain.npz"),
                                **{f"{k}_{i}": v for i, s in enumerate(self._brains) for k, v in s.items()})
        summary = self.summary()
        meta = {"config": _cfg_dict(c), "actions": ACTIONS, "source_hash": source_hash(),
                "commit": git_commit(), "seconds": round(time.time() - t0, 2), "summary": summary,
                "world_ledger": asdict(self.world.ledger)}
        json.dump(meta, open(os.path.join(self.dir, "meta.json"), "w"), indent=1)
        return summary

    def summary(self) -> dict:
        T = self.totals
        return {"alive": self.body.alive, "days": self.day + (1 if self.body.alive else 0),
                "ticks_alive": T["ticks_alive"], "food": round(T["food"], 4),
                "poison": round(T["poison"], 4),
                "mean_drive": round(T["drive_sum"] / max(T["ticks_alive"], 1), 5),
                "first_food_t": T["first_food_t"],
                "poison_bites_after_first": T["poison_bites_after_first"], "H": self.n_units()}


def _cfg_dict(c):
    d = asdict(c)
    return json.loads(json.dumps(d, default=float))
