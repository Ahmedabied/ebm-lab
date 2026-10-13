"""L3a — senses: what a creature can know. Two antennae read the three notes; the body reports
energy and toxin. That is the entire sensory world. No item, no label, no coordinates.
"""
from dataclasses import dataclass
import numpy as np
from .world import NOTES

DIM = 3 * NOTES + 2 + 1      # left(3), right(3), change(3), body(2), bias(1) = 12


@dataclass
class SenseConfig:
    antenna_angle: float = np.deg2rad(45.0)
    antenna_len: float = 1.5
    c0: float = 0.05           # log-compression scale: x = log1p(c / c0)
    noise: float = 0.02        # Gaussian noise on each antenna reading (log units). R2: without
                               # noise, steering is trivially easy; real sensors are noisy.


class Senses:
    def __init__(self, cfg: SenseConfig):
        self.cfg = cfg
        self.prev_mean = np.zeros(NOTES, dtype=np.float32)

    def antennae(self, y: float, x: float, heading: float):
        c = self.cfg
        aL = heading + c.antenna_angle; aR = heading - c.antenna_angle
        return ((y + c.antenna_len * np.sin(aL), x + c.antenna_len * np.cos(aL)),
                (y + c.antenna_len * np.sin(aR), x + c.antenna_len * np.cos(aR)))

    def sense(self, world, y: float, x: float, heading: float, body: np.ndarray,
              rng: np.random.Generator | None = None) -> dict:
        """Returns a structured sensation and its flat vector x (DIM,)."""
        (yl, xl), (yr, xr) = self.antennae(y, x, heading)
        left = np.log1p(world.read(yl, xl) / self.cfg.c0).astype(np.float32)
        right = np.log1p(world.read(yr, xr) / self.cfg.c0).astype(np.float32)
        if rng is not None and self.cfg.noise > 0:
            left = left + rng.normal(0, self.cfg.noise, NOTES).astype(np.float32)
            right = right + rng.normal(0, self.cfg.noise, NOTES).astype(np.float32)
        mean = 0.5 * (left + right)
        change = mean - self.prev_mean
        self.prev_mean = mean
        vec = np.concatenate([left, right, change, body, [1.0]]).astype(np.float32)
        return {"left": left, "right": right, "change": change, "body": body, "x": vec}
