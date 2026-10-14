"""L3a — senses: what a creature can know. Two antennae read the three notes; the body reports
energy and toxin. That is the entire sensory world. No item, no label, no coordinates.
"""
from dataclasses import dataclass
import numpy as np
from .world import NOTES

DIM = 3 * NOTES + 2 + 1      # contrast(3), mean(3), change(3), body(2), bias(1) = 12  (default)
DIM_SIGN = DIM + NOTES       # + sign(3) before the bias, when SenseConfig.sign_features (EXP-02) = 15
# Opponent coding (amendment A3, pilot 01c): the brain is handed, per note, the left/right CONTRAST
# (L-R)/(L+R+eps) in [-1, 1], the mean log level, and its change since last tick. With raw L and R
# the left-right difference is ~0.15 log units, so a decisive turn would need weights ~13; contrast
# makes it O(1). The brain still has to learn which notes are good and what to do about them.


@dataclass
class SenseConfig:
    antenna_angle: float = np.deg2rad(45.0)
    antenna_len: float = 1.5
    c0: float = 0.05           # log-compression scale: x = log1p(c / c0)
    eps: float = 0.05          # contrast floor: far from any source, contrast -> 0, not noise/noise
    noise: float = 0.02        # Gaussian noise on each antenna reading (log units). R2: without
                               # noise, steering is trivially easy; real sensors are noisy.
    sign_features: bool = False  # EXP-02: append s_k = sign(L_k - R_k) * [|L_k - R_k| > dead] per note,
                               # before the bias. The same discretisation TabularQ._state uses, on the
                               # same noisy log readings. A fixed sense-organ nonlinearity: it is
                               # symmetric in the notes and never says which note is good (no valence).
    dead: float = 0.02         # dead zone for the sign features (= TabularQ's dead)


class Senses:
    def __init__(self, cfg: SenseConfig):
        self.cfg = cfg
        self.prev_mean = np.zeros(NOTES, dtype=np.float32)

    @property
    def dim(self) -> int:
        """Length of the flat sensation vector x: 12, or 15 with sign features."""
        return DIM_SIGN if self.cfg.sign_features else DIM

    def names(self) -> list[str]:
        """Human names of the dims of x, in order (written to meta.json for the viewer/export)."""
        notes = ("A", "B", "C")
        n = [f"contrast_{k}" for k in notes] + [f"mean_{k}" for k in notes] + [f"change_{k}" for k in notes]
        n += ["body_E", "body_X"]
        if self.cfg.sign_features: n += [f"sign_{k}" for k in notes]
        return n + ["bias"]

    def signs(self, left: np.ndarray, right: np.ndarray) -> np.ndarray:
        """Per-note ternary sign of the left-right difference with a dead zone: +1 / 0 / -1.
        Mirrors TabularQ._state exactly (d > dead -> +1, d < -dead -> -1, else 0)."""
        d = left - right
        return ((d > self.cfg.dead).astype(np.float32) - (d < -self.cfg.dead).astype(np.float32))

    def antennae(self, y: float, x: float, heading: float):
        c = self.cfg
        aL = heading + c.antenna_angle; aR = heading - c.antenna_angle
        return ((y + c.antenna_len * np.sin(aL), x + c.antenna_len * np.cos(aL)),
                (y + c.antenna_len * np.sin(aR), x + c.antenna_len * np.cos(aR)))

    def sense(self, world, y: float, x: float, heading: float, body: np.ndarray,
              rng: np.random.Generator | None = None) -> dict:
        """Returns a structured sensation and its flat vector x (self.dim,)."""
        (yl, xl), (yr, xr) = self.antennae(y, x, heading)
        left = np.log1p(world.read(yl, xl) / self.cfg.c0).astype(np.float32)
        right = np.log1p(world.read(yr, xr) / self.cfg.c0).astype(np.float32)
        if rng is not None and self.cfg.noise > 0:
            left = left + rng.normal(0, self.cfg.noise, NOTES).astype(np.float32)
            right = right + rng.normal(0, self.cfg.noise, NOTES).astype(np.float32)
        mean = 0.5 * (left + right)
        change = mean - self.prev_mean
        self.prev_mean = mean
        contrast = (left - right) / (np.abs(left) + np.abs(right) + self.cfg.eps)
        parts = [contrast, mean, change, body]
        out = {"left": left, "right": right, "contrast": contrast, "change": change, "body": body}
        if self.cfg.sign_features:
            out["sign"] = self.signs(left, right)
            parts.append(out["sign"])
        out["x"] = np.concatenate(parts + [[1.0]]).astype(np.float32)
        return out
