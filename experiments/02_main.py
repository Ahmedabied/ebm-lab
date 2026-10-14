"""EXP-02 — the pre-registered decomposition (experiments/EXP-02-prereg.md). Fresh seeds 200-219.
Which of tabular Q's four advantages (sign features, egreedy argmax, TD bootstrap, online learning)
explains its 3x lead over the EBM in EXP-01?
Run: uv run python experiments/02_main.py linear ; uv run python experiments/02_main.py xor
Then: uv run python experiments/report_exp02.py ; uv run python experiments/plot_exp02.py"""
import sys
from harness import run_arms, table

blend = sys.argv[1]
assert blend in ("linear", "xor"), "usage: 02_main.py <linear|xor>"

B0 = {"policy": "ebm", "day_learning": True}            # ebm-dn: the decomposition baseline
TD = {"policy": "ebm", "learner": "q", "day_learning": True, "brain.act_mode": "egreedy"}
# Order = the prereg arms table (report and plots keep it).
arms = {
    "random":        {"policy": "random"},
    "tabular_q":     {"policy": "tabular_q"},
    "ebm-nolearn":   {"policy": "ebm", "sleep": "none", "growth": "none"},   # same as EXP-01
    "ebm":           {"policy": "ebm"},
    "ebm-dn":        dict(B0),
    "ebm-dn-sign":   {**B0, "sense.sign_features": True},
    "ebm-dn-greedy": {**B0, "brain.act_mode": "egreedy"},
    "ebm-dn-critic": {**B0, "learner": "ac"},
    "ebm-td":        dict(TD),
    "ebm-all":       {**TD, "sense.sign_features": True},
}
res = run_arms(f"02_main_{blend}", arms, seeds=range(200, 220), days=15,
               world_overrides={"world.blend_mode": blend})
print(table(res)); print("seconds:", res["seconds"])
