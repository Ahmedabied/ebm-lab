"""EXP-00 — world calibration. Not a result about brains.

Question: how harsh is the world? A learner that sleeps only learns at night, so a NAIVE creature
must survive long enough to reach a few nights, while still being under pressure. Target band
(pre-registered): the RANDOM policy survives a median of 2–5 days across seeds; the ORACLE survives
all days. We scan metabolic cost and food budget, record the whole grid, and pick ONE setting.

Also measures the scent profile: steady-state concentration vs distance from one food item, so we
know how far a creature can "smell" (readable radius) relative to the spacing between items.

Run: uv run python experiments/00_calibration.py
"""
import json, os, sys, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from creature.sim import Life, SimConfig
from creature.world import World, WorldConfig, FOOD, BLEND

OUT = os.path.join(os.path.dirname(__file__), "results", "00_calibration")
os.makedirs(OUT, exist_ok=True)


def life(policy, seed, metabolic, food_budget, days=8):
    cfg = SimConfig(seed=seed, label=f"_cal_{policy}_{metabolic}_{food_budget}", policy=policy,
                    days=days, day_len=300, runs_dir="/tmp/ebm-cal")
    cfg.body.metabolic = metabolic; cfg.body.E0 = 0.8
    cfg.world.food_budget = food_budget
    return Life(cfg).run()


def scent_profile():
    """One food item in an empty world, run to steady state, read concentration vs distance."""
    w = World(WorldConfig(H=48, W=48, n_poison=0, food_budget=0.0), np.random.default_rng(0))
    w.kind = np.array([FOOD]); w.pos = np.array([[24.5, 24.5]], np.float32); w.mass = np.array([2.0], np.float32)
    for _ in range(400): w.step()
    prof = [(d, float(w.fields[0, 24, 24 + d])) for d in range(0, 16)]
    return prof


if __name__ == "__main__":
    grid = {"metabolic": [0.0005, 0.001, 0.002], "food_budget": [6.0, 12.0, 24.0]}
    seeds = list(range(8))
    rows = []
    for m, fb in itertools.product(grid["metabolic"], grid["food_budget"]):
        for pol in ["random", "oracle"]:
            ds = [life(pol, s, m, fb)["days"] for s in seeds]
            foods = [life(pol, s, m, fb)["food"] for s in seeds]
            rows.append({"policy": pol, "metabolic": m, "food_budget": fb,
                         "days_median": float(np.median(ds)), "days_min": int(min(ds)), "days_max": int(max(ds)),
                         "food_mean": float(np.mean(foods))})
            print(rows[-1])
    prof = scent_profile()
    json.dump({"grid": rows, "scent_profile": prof, "seeds": seeds,
               "note": "days capped at 8; day_len 300; E0 0.8"},
              open(os.path.join(OUT, "results.json"), "w"), indent=1)
    print("scent profile (distance, A):", [(d, round(c, 4)) for d, c in prof])
