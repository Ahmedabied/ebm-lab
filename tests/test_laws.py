"""The laws (DESIGN.md §0). If one of these fails, no number from the lab is trustworthy."""
import numpy as np
import pytest
from creature import physics
from creature.world import World, WorldConfig, FOOD, POISON, NOTES
from creature.body import Body, BodyConfig


# ---- physics ---------------------------------------------------------------------------------
def test_diffusion_conserves_mass():
    rng = np.random.default_rng(0)
    f = rng.random((NOTES, 16, 16)).astype(np.float64)
    g = physics.diffuse(f, 0.2)
    assert abs(g.sum() - f.sum()) < 1e-9


def test_diffusion_is_bounded_and_smoothing():
    f = np.zeros((8, 8)); f[4, 4] = 1.0
    g = physics.diffuse(f, 0.25)
    assert g.min() >= 0 and g.max() <= 1.0 and g[4, 4] < 1.0 and g[4, 5] > 0


def test_decay_removes_exactly():
    f = np.full((4, 4), 2.0)
    assert np.allclose(physics.decay(f, 0.9), 1.8)


def test_bilinear_reads_corners_and_wraps():
    f = np.zeros((4, 4)); f[0, 0] = 1.0
    assert physics.bilinear(f, 0.0, 0.0) == 1.0
    assert np.isclose(physics.bilinear(f, 3.5, 3.5), 0.25)  # wraps to (0,0) with weight 1/4
    assert physics.bilinear(f, 2.0, 2.0) == 0.0


# ---- world books -----------------------------------------------------------------------------
def test_field_books_close_every_tick():
    w = World(WorldConfig(H=16, W=16), np.random.default_rng(1))
    for _ in range(50):
        before = w.field_mass(); e0, d0 = w.ledger.emitted, w.ledger.decayed
        w.step()
        after = w.field_mass()
        assert abs((after - before) - ((w.ledger.emitted - e0) - (w.ledger.decayed - d0))) < 1e-3


def test_item_books_close_after_eating_and_regrowth():
    w = World(WorldConfig(H=16, W=16, n_poison=0), np.random.default_rng(2))
    total_food = 0.0
    for _ in range(300):
        y, x = w.pos[0]                       # stand on the first item and bite
        f, p = w.eat_at(float(y), float(x))
        total_food += f
        assert p == 0.0
        w.regrow()
        assert abs(w.item_food_mass() - (w.ledger.created - w.ledger.eaten_food)) < 1e-4
    assert total_food > 0


def test_poison_is_not_depleted_but_is_booked():
    w = World(WorldConfig(H=16, W=16, n_poison=1, food_budget=0.0), np.random.default_rng(3))
    y, x = w.pos[0]
    m0 = float(w.mass[0])
    f, p = w.eat_at(float(y), float(x))
    assert f == 0.0 and p == w.cfg.bite and float(w.mass[0]) == m0
    assert w.ledger.ingested_poison == p


def test_world_is_deterministic_per_seed():
    def run(seed):
        w = World(WorldConfig(H=16, W=16), np.random.default_rng(seed))
        for _ in range(40):
            w.step(); w.eat_at(8.0, 8.0); w.regrow()
        return w.fields.copy(), w.pos.copy(), w.mass.copy()
    a, b = run(7), run(7)
    assert np.array_equal(a[0], b[0]) and np.array_equal(a[1], b[1]) and np.array_equal(a[2], b[2])
    c = run(8)
    assert not np.array_equal(a[1], c[1])


def test_creature_can_only_read_notes_not_items():
    """The world's read() returns NOTES numbers and nothing that names an item."""
    w = World(WorldConfig(H=16, W=16), np.random.default_rng(4))
    for _ in range(20): w.step()
    r = w.read(5.5, 5.5)
    assert r.shape == (NOTES,) and r.dtype.kind == "f"


# ---- body -------------------------------------------------------------------------------------
def test_drive_is_zero_at_setpoint_and_grows_away():
    b = Body(BodyConfig()); b.E = 1.0; b.X = 0.0
    assert b.drive() == 0.0
    b.E = 0.5; assert b.drive() == pytest.approx(0.25)
    b.X = 0.5; assert b.drive() == pytest.approx(0.5)


def test_eating_lowers_drive_and_poison_raises_it():
    b = Body(BodyConfig())
    r_food = b.tick(moved=False, n_units=0, food_mass=0.1, poison_mass=0.0)
    assert r_food > 0
    r_poison = b.tick(moved=False, n_units=0, food_mass=0.0, poison_mass=0.1)
    assert r_poison < 0


def test_starvation_kills_and_toxin_drains():
    b = Body(BodyConfig(E0=0.01))
    for _ in range(100): b.tick(False, 0, 0.0, 0.0)
    assert not b.alive and b.E == 0.0
    b2 = Body(BodyConfig()); b2.X = 1.0
    e0 = b2.E; b2.tick(False, 0, 0.0, 0.0)
    assert e0 - b2.E > BodyConfig().metabolic


def test_growth_is_paid_for():
    a = Body(BodyConfig()); b = Body(BodyConfig())
    a.tick(False, 0, 0, 0); b.tick(False, 10, 0, 0)
    assert b.E < a.E


def test_xor_world_has_two_poison_blends_and_books_close():
    from creature.world import POISON
    w = World(WorldConfig(H=16, W=16, blend_mode="xor", n_poison=4), np.random.default_rng(5))
    pb = w.blend[w.kind == POISON]
    assert len(np.unique(pb, axis=0)) == 2 and (pb.sum(axis=1) == 1).all()
    for _ in range(30):
        before = w.field_mass(); e0, d0 = w.ledger.emitted, w.ledger.decayed
        w.step()
        assert abs((w.field_mass() - before) - ((w.ledger.emitted - e0) - (w.ledger.decayed - d0))) < 1e-3
