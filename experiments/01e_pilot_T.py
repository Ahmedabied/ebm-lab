"""EXP-01e PILOT — temperature sweep (lr 1.0, clip 1.0). Seeds 0-7 (burned). Linear world.
Run: uv run python experiments/01e_pilot_T.py"""
from harness import run_arms, table
arms = {f"T{T}": {"policy": "ebm", "brain.lr": 1.0, "clip": 1.0, "brain.T": T} for T in (1.0, 0.5, 0.3, 0.1)}
arms["nolearn"] = {"policy": "ebm", "sleep": "none", "growth": "none"}
res = run_arms("01e_pilot_T", arms, seeds=range(8), days=15)
print(table(res))
