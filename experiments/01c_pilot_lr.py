"""EXP-01c PILOT — learning-rate / replay-epochs sweep for the EBM. A TUNING run: its seeds
(0–7) are burned; the pre-registered experiment must use fresh seeds. Linear world.
Run: uv run python experiments/01c_pilot_lr.py
"""
from harness import run_arms, table
arms = {}
for lr in (0.05, 0.2, 0.5):
    for ep in (3, 10):
        arms[f"ebm-lr{lr}-ep{ep}"] = {"policy": "ebm", "brain.lr": lr, "sleep_epochs": ep}
arms["tabular_q"] = {"policy": "tabular_q"}
res = run_arms("01c_pilot_lr", arms, seeds=range(8), days=15)
print(table(res))
