"""Baselines the EBM brain must be compared against. Each has the same act() interface.

random        uniform action. The floor.
braitenberg   hand-wired, and it CHEATS: it is told that note A is good and note C is bad.
              Turn toward the stronger-A side, away from the stronger-C side. "Steering is easy."
oracle        sees item positions (which no creature can). Greedy nearest food, avoids poison.
              An upper bound for greedy foraging, NOT the optimum.
tabular_q     Q-learning on a coarse discretisation of the same sensation, with the same body
              lesson. The standard RL comparison; learns online, every tick.
"""
import numpy as np
from .brain import A
from .world import FOOD, POISON

LEFT, RIGHT, FORWARD = 0, 1, 2


class Random:
    name = "random"
    def act(self, sens, world, y, x, heading, rng):
        return int(rng.integers(A)), None
    def learn_tick(self, *a, **k): pass


class Braitenberg:
    name = "braitenberg"
    def __init__(self, thresh=0.02):
        self.thresh = thresh
    def act(self, sens, world, y, x, heading, rng):
        score = (sens["left"][0] - sens["right"][0]) - (sens["left"][2] - sens["right"][2])
        if score > self.thresh: return LEFT, None
        if score < -self.thresh: return RIGHT, None
        return FORWARD, None
    def learn_tick(self, *a, **k): pass


class Oracle:
    name = "oracle"
    def __init__(self, avoid_radius=3.0, turn=np.deg2rad(30)):
        self.avoid_radius = avoid_radius; self.turn = turn
    def _vec(self, world, y, x, kind):
        m = world.kind == kind
        if not m.any(): return None, None
        dy = (world.pos[m, 0] - y + world.cfg.H / 2) % world.cfg.H - world.cfg.H / 2
        dx = (world.pos[m, 1] - x + world.cfg.W / 2) % world.cfg.W - world.cfg.W / 2
        d2 = dy * dy + dx * dx; i = int(np.argmin(d2))
        return (dy[i], dx[i]), float(np.sqrt(d2[i]))
    def act(self, sens, world, y, x, heading, rng):
        (pv, pd) = self._vec(world, y, x, POISON)
        (fv, fd) = self._vec(world, y, x, FOOD)
        if pv is not None and pd < self.avoid_radius:
            target = np.arctan2(-pv[0], -pv[1])            # away from poison
        elif fv is not None:
            target = np.arctan2(fv[0], fv[1])              # toward food
        else:
            return FORWARD, None
        err = (target - heading + np.pi) % (2 * np.pi) - np.pi
        if err > self.turn / 2: return LEFT, None
        if err < -self.turn / 2: return RIGHT, None
        return FORWARD, None
    def learn_tick(self, *a, **k): pass


class TabularQ:
    name = "tabular_q"
    def __init__(self, rng, alpha=0.1, gamma=0.9, eps=0.1, dead=0.02):
        self.alpha, self.gamma, self.eps, self.dead = alpha, gamma, eps, dead
        self.Q = np.zeros((54, A)); self.prev = None
    def _state(self, sens):
        s = 0
        for k in range(3):
            d = sens["left"][k] - sens["right"][k]
            s = s * 3 + (0 if d > self.dead else 2 if d < -self.dead else 1)
        return s * 2 + (1 if sens["body"][0] < 0.5 else 0)
    def act(self, sens, world, y, x, heading, rng):
        s = self._state(sens)
        a = int(rng.integers(A)) if rng.random() < self.eps else int(np.argmax(self.Q[s]))
        self.prev = (s, a)
        return a, None
    def learn_tick(self, sens_next, r):
        s, a = self.prev
        s2 = self._state(sens_next)
        self.Q[s, a] += self.alpha * (r + self.gamma * self.Q[s2].max() - self.Q[s, a])


def make(name: str, rng):
    return {"random": Random, "braitenberg": Braitenberg, "oracle": Oracle,
            "tabular_q": lambda: TabularQ(rng)}[name]()
