"""EXP-02a PILOT: step sizes of the two new EXP-02 components, pre-registered in EXP-02-prereg.md.
alpha_v (critic lr, learner="ac", arm ebm-dn-critic) and alpha_q (Q-mode lr, learner="q", arm
ebm-td). ONLY pilot seeds 20-27, linear world, 15 days. Pick each by mean ticks_alive; nothing
else is tuned here. ebm-dn and tabular_q run alongside as reference points only (no selection).
Re-run after amendment A14 (raw-delta online actor lesson in "ac"); alpha_q grid extended to 0.3.
Also records each life's end-of-day-0 policy entropy (on day 0's cache, before night 0's replay;
the `wake_entropy` field of the first sleep_start event) as a policy-collapse instrument.
Run (from the repo root): python experiments/02a_pilot_alpha.py
"""
import json, os
import numpy as np
from harness import run_arms, table, RESULTS
RUNS = "/tmp/ebm-runs"
B0 = {"policy": "ebm", "day_learning": True}
arms = {}
for av in (0.01, 0.03, 0.1, 0.3):
    arms[f"ac-alpha_v{av}"] = {**B0, "learner": "ac", "alpha_v": av}
for aq in (0.003, 0.01, 0.03, 0.1, 0.3):
    arms[f"q-alpha_q{aq}"] = {**B0, "learner": "q", "alpha_q": aq}
arms["ebm-dn (ref)"] = dict(B0)
arms["tabular_q (ref)"] = {"policy": "tabular_q"}
NAME = "02a_pilot_alpha"
res = run_arms(NAME, arms, seeds=range(20, 28), days=15, runs_dir=RUNS,
               world_overrides={"world.blend_mode": "linear"})
# day-0 entropy instrument, read back from each life's event log
for arm, lives in res["lives"].items():
    for life in lives:
        ev = os.path.join(RUNS, f"{NAME}_{arm}", str(life["seed"]), "events.jsonl")
        first = next((json.loads(l) for l in open(ev) if '"sleep_start"' in l), None)
        life["day0_wake_entropy"] = None if first is None else first.get("wake_entropy")
    ents = [l["day0_wake_entropy"] for l in lives if l["day0_wake_entropy"] is not None]
    res["stats"][arm]["day0_wake_entropy"] = {"mean": float(np.mean(ents)) if ents else None,
                                              "n": len(ents), "values": ents}
json.dump(res, open(os.path.join(RESULTS, NAME, "results.json"), "w"), indent=1)
print(table(res))
print(f"{'arm':28s} day-0 end-of-day entropy (max ln3=1.099)")
for arm, st in res["stats"].items():
    e = st["day0_wake_entropy"]
    print(f"{arm:28s} mean={e['mean'] if e['mean'] is None else round(e['mean'], 3)} n={e['n']}  {e['values']}")
