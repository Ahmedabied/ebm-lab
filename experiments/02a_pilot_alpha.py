"""EXP-02a PILOT: step sizes of the two new EXP-02 components, pre-registered in EXP-02-prereg.md.
alpha_v (critic lr, learner="ac", arm ebm-dn-critic) and alpha_q (Q-mode lr, learner="q", arm
ebm-td). ONLY pilot seeds 20-27, linear world, 15 days. Pick each by mean ticks_alive; nothing
else is tuned here. ebm-dn and tabular_q run alongside as reference points only (no selection).
Run (from the repo root): python experiments/02a_pilot_alpha.py
"""
from harness import run_arms, table
B0 = {"policy": "ebm", "day_learning": True}
arms = {}
for av in (0.01, 0.03, 0.1, 0.3):
    arms[f"ac-alpha_v{av}"] = {**B0, "learner": "ac", "alpha_v": av}
for aq in (0.003, 0.01, 0.03, 0.1):
    arms[f"q-alpha_q{aq}"] = {**B0, "learner": "q", "alpha_q": aq}
arms["ebm-dn (ref)"] = dict(B0)
arms["tabular_q (ref)"] = {"policy": "tabular_q"}
res = run_arms("02a_pilot_alpha", arms, seeds=range(20, 28), days=15,
               world_overrides={"world.blend_mode": "linear"})
print(table(res))
