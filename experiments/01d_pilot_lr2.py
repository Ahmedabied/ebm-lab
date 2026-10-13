"""EXP-01d PILOT — lr × clip sweep under opponent-coded senses. Seeds 0-7 (burned). Linear world.
Run: uv run python experiments/01d_pilot_lr2.py"""
from harness import run_arms, table
arms = {}
for lr in (0.5, 1.0, 2.0):
    for clip in (0.2, 1.0):
        arms[f"lr{lr}-clip{clip}"] = {"policy": "ebm", "brain.lr": lr, "clip": clip}
arms["nolearn"] = {"policy": "ebm", "sleep": "none", "growth": "none"}
res = run_arms("01d_pilot_lr2", arms, seeds=range(8), days=15)
print(table(res))
