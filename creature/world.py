"""L1 — the world: three chemical fields, items that emit into them, and a ledger.

The words "food" and "poison" live HERE and in the metrics only. The creature never sees an item;
it reads fields at its antennae and feels its own body. Items are sources of a chemical blend
with a mass; eating moves mass from an item into a body, and every unit is booked.
"""
from dataclasses import dataclass, field
import numpy as np
from . import physics

NOTES = 3                      # chemical notes A, B, C
FOOD, POISON = 0, 1            # item kinds (world bookkeeping only)

# Blend tables: what each item kind smells like. Two worlds (R2, research/04 §Q7):
#   linear: food = A+B, poison = B+C. Solvable from A and C alone; B carries no information.
#           Tests valence learning + steering. A linear brain can do it.
#   xor:    food = A+B TOGETHER; poison = A alone or B alone. "The blend is the food, the pure
#           notes are poison." No linear rule solves it: it needs a unit that reads the conjunction.
#           This is the world where "chemistry blends" actually matters.
BLENDS = {
    "linear": {FOOD: [np.array([1.0, 1.0, 0.0], np.float32)],
               POISON: [np.array([0.0, 1.0, 1.0], np.float32)]},
    "xor":    {FOOD: [np.array([1.0, 1.0, 0.0], np.float32)],
               POISON: [np.array([1.0, 0.0, 0.0], np.float32), np.array([0.0, 1.0, 0.0], np.float32)]},
}


@dataclass
class WorldConfig:
    H: int = 48
    W: int = 48
    alpha: float = 0.18          # diffusion coefficient per tick
    keep: float = 0.95           # fraction of each field kept per tick
    emit_rate: float = 0.05      # field mass emitted per tick per unit of item mass
    food_budget: float = 24.0    # regrow when total food mass is below this (EXP-00, decisions/0001)
    food_mass: float = 2.0       # mass of a new food item
    n_poison: int = 4            # permanent poison items
    poison_mass: float = 2.0     # emission strength of a poison item (never depleted)
    eat_radius: float = 1.0      # cells
    bite: float = 0.05           # mass per tick a body can take from an item in reach
    blend_mode: str = "linear"   # linear | xor  (see BLENDS)


@dataclass
class Ledger:
    """Books for the conservation test. All in mass units."""
    emitted: float = 0.0         # field mass added by sources
    decayed: float = 0.0         # field mass removed by decay
    created: float = 0.0         # item mass spawned (food)
    eaten_food: float = 0.0      # item mass moved into bodies (food)
    ingested_poison: float = 0.0 # poison "mass" that entered bodies (poison is not depleted)


class World:
    def __init__(self, cfg: WorldConfig, rng: np.random.Generator):
        self.cfg = cfg
        self.rng = rng
        self.t = 0
        self.fields = np.zeros((NOTES, cfg.H, cfg.W), dtype=np.float32)
        # items: parallel arrays
        self.kind = np.zeros(0, dtype=np.int32)
        self.pos = np.zeros((0, 2), dtype=np.float32)     # (y, x) cell centres
        self.mass = np.zeros(0, dtype=np.float32)
        self.blend = np.zeros((0, NOTES), dtype=np.float32)  # what each item emits
        self.blends = BLENDS[cfg.blend_mode]
        self.ledger = Ledger()
        for i in range(cfg.n_poison):
            self._spawn(POISON, cfg.poison_mass, variant=i % len(self.blends[POISON]))
        self.regrow()

    # ---- items ----------------------------------------------------------------------------
    def _spawn(self, kind: int, mass: float, variant: int = 0):
        y = self.rng.integers(self.cfg.H) + 0.5
        x = self.rng.integers(self.cfg.W) + 0.5
        self.kind = np.append(self.kind, kind)
        self.pos = np.vstack([self.pos, [[y, x]]]).astype(np.float32)
        self.mass = np.append(self.mass, np.float32(mass))
        self.blend = np.vstack([self.blend, self.blends[kind][variant][None, :]]).astype(np.float32)
        if kind == FOOD:
            self.ledger.created += mass

    def regrow(self):
        """Keep food mass near the budget. Spawning is the ONE random act in the world."""
        while self.food_mass_total() < self.cfg.food_budget:
            self._spawn(FOOD, self.cfg.food_mass)

    def food_mass_total(self) -> float:
        return float(self.mass[self.kind == FOOD].sum())

    def _remove(self, idx: np.ndarray):
        keep = np.ones(len(self.kind), dtype=bool); keep[idx] = False
        self.kind, self.pos, self.mass, self.blend = (self.kind[keep], self.pos[keep],
                                                      self.mass[keep], self.blend[keep])

    # ---- physics step ----------------------------------------------------------------------
    def step(self):
        """diffuse -> decay -> emit. Physics first, then sources. Books every unit."""
        c = self.cfg
        f = physics.diffuse(self.fields, c.alpha)
        before = float(f.sum())
        f = physics.decay(f, c.keep)
        self.ledger.decayed += before - float(f.sum())
        # emit: each item adds blend * mass * emit_rate at its cell
        for bl, (y, x), m in zip(self.blend, self.pos, self.mass):
            e = bl * m * c.emit_rate
            f[:, int(y), int(x)] += e
            self.ledger.emitted += float(e.sum())
        self.fields = f
        self.t += 1

    # ---- eating ----------------------------------------------------------------------------
    def eat_at(self, y: float, x: float) -> tuple[float, float]:
        """A body at (y, x) takes one bite from every item in reach.
        Returns (food_mass_taken, poison_mass_ingested). Food depletes; poison does not."""
        if len(self.kind) == 0:
            return 0.0, 0.0
        dy = (self.pos[:, 0] - y + self.cfg.H / 2) % self.cfg.H - self.cfg.H / 2
        dx = (self.pos[:, 1] - x + self.cfg.W / 2) % self.cfg.W - self.cfg.W / 2
        near = (dy * dy + dx * dx) <= self.cfg.eat_radius ** 2
        food_taken = 0.0; poison_taken = 0.0
        gone = []
        for i in np.where(near)[0]:
            if self.kind[i] == FOOD:
                b = float(min(self.cfg.bite, self.mass[i]))
                self.mass[i] -= b
                food_taken += b
                if self.mass[i] <= 1e-9:
                    gone.append(i)
            else:
                poison_taken += self.cfg.bite
        if gone:
            self._remove(np.array(gone))
        self.ledger.eaten_food += food_taken
        self.ledger.ingested_poison += poison_taken
        return food_taken, poison_taken

    # ---- reads -----------------------------------------------------------------------------
    def read(self, y: float, x: float) -> np.ndarray:
        """The three notes at a continuous point. This is all a creature can know of the world."""
        return physics.bilinear(self.fields, y, x)

    # ---- books -----------------------------------------------------------------------------
    def field_mass(self) -> float:
        return float(self.fields.sum())

    def item_food_mass(self) -> float:
        return self.food_mass_total()
