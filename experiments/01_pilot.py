"""EXP-01 PILOT — does the EBM brain learn anything at all? NOT a result. A smoke-level look
with 8 seeds so the real pre-registered experiment can be written against reality.

Run: uv run python experiments/01_pilot.py [linear|xor]
"""
import sys
from harness import run_arms, table

blend = sys.argv[1] if len(sys.argv) > 1 else "linear"
arms = {
    "random":      {"policy": "random"},
    "braitenberg": {"policy": "braitenberg"},
    "tabular_q":   {"policy": "tabular_q"},
    "oracle":      {"policy": "oracle"},
    "ebm":         {"policy": "ebm"},
    "ebm-nosleep": {"policy": "ebm", "sleep": "none", "day_learning": True},
    "ebm-sleep-matched": {"policy": "ebm", "sleep": "today", "sleep_epochs": 1},   # each sample once, like online
    "ebm-nolearn": {"policy": "ebm", "sleep": "none", "day_learning": False, "growth": "none"},
}
res = run_arms(f"01_pilot_{blend}", arms, seeds=range(8), days=15,
               world_overrides={"world.blend_mode": blend})
print(table(res)); print("seconds:", res["seconds"])
