"""EXP-01 — the pre-registered experiment (experiments/EXP-01-prereg.md). Fresh seeds 100-119.
Run: uv run python experiments/01_main.py linear ; uv run python experiments/01_main.py xor"""
import sys
from harness import run_arms, table
blend = sys.argv[1]
arms = {
    "random":            {"policy": "random"},
    "braitenberg":       {"policy": "braitenberg"},
    "tabular_q":         {"policy": "tabular_q"},
    "oracle":            {"policy": "oracle"},
    "ebm":               {"policy": "ebm"},
    "ebm-nosleep":       {"policy": "ebm", "sleep": "none", "day_learning": True},
    "ebm-sleep-matched": {"policy": "ebm", "sleep": "today", "sleep_epochs": 1},
    "ebm-sleep-today":   {"policy": "ebm", "sleep": "today"},
    "ebm-sleep-noise":   {"policy": "ebm", "sleep": "noise"},
    "ebm-nolearn":       {"policy": "ebm", "sleep": "none", "growth": "none"},
    "ebm-nogrowth":      {"policy": "ebm", "growth": "none"},
    "ebm-linear":        {"policy": "ebm", "brain.H0": 0, "growth": "none"},
}
res = run_arms(f"01_main_{blend}", arms, seeds=range(100, 120), days=15,
               world_overrides={"world.blend_mode": blend})
print(table(res)); print("seconds:", res["seconds"])
