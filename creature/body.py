"""L2 — the body: metabolism, toxin, death, and the DRIVE, which is an energy.

The drive D(h) is how far the body is from its setpoints (Keramati & Gutkin 2014, via Genesis
report 02). The creature's only teacher is the change in D. Nothing here knows what food is: a
bite of something arrives as (food_mass, poison_mass) from the world's books, and the body only
feels its energy and toxin move.
"""
from dataclasses import dataclass
import numpy as np


@dataclass
class BodyConfig:
    E0: float = 0.6              # starting energy
    E_max: float = 1.0
    metabolic: float = 0.002     # energy per tick, resting
    move_cost: float = 0.001     # extra per tick when moving
    unit_cost: float = 0.0002    # per hidden unit per tick (growth is paid for)
    yield_: float = 1.0          # energy per unit food mass
    toxicity: float = 0.5        # toxin per unit poison mass ingested
    toxin_decay: float = 0.98    # fraction of toxin kept per tick
    toxin_drain: float = 0.01    # energy drained per tick per unit toxin
    # drive
    E_set: float = 1.0
    X_set: float = 0.0
    n: float = 2.0               # exponent
    w_E: float = 1.0
    w_X: float = 1.0


class Body:
    def __init__(self, cfg: BodyConfig):
        self.cfg = cfg
        self.E = cfg.E0
        self.X = 0.0
        self.alive = True

    def drive(self) -> float:
        c = self.cfg
        return c.w_E * abs(c.E_set - self.E) ** c.n + c.w_X * abs(c.X_set - self.X) ** c.n

    def tick(self, moved: bool, n_units: int, food_mass: float, poison_mass: float) -> float:
        """Advance one tick. Returns the lesson r = D_before - D_after (drive reduction)."""
        c = self.cfg
        D0 = self.drive()
        self.E -= c.metabolic + (c.move_cost if moved else 0.0) + c.unit_cost * n_units
        self.X *= c.toxin_decay
        self.E -= self.X * c.toxin_drain
        self.E = min(c.E_max, self.E + c.yield_ * food_mass)
        self.X += c.toxicity * poison_mass
        if self.E <= 0.0:
            self.E = 0.0
            self.alive = False
        return D0 - self.drive()

    def state(self) -> np.ndarray:
        return np.array([self.E, self.X], dtype=np.float32)
