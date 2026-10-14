"""EXP-02a PILOT: step sizes of the two new EXP-02 components, pre-registered in EXP-02-prereg.md.
alpha_v (critic lr, learner="ac", arm ebm-dn-critic) and alpha_q (Q-mode lr, learner="q", arm
ebm-td). ONLY pilot seeds 20-27, linear world, 15 days. Pick each by mean ticks_alive; nothing
else is tuned here. ebm-dn and tabular_q run alongside as reference points only (no selection).
Re-run after amendment A14 (raw-delta online actor lesson in "ac"); alpha_q grid extended to 0.3.
Also records each life's end-of-day-0 policy entropy (on day 0's cache, before night 0's replay;
the `wake_entropy` field of the first sleep_start event) as a policy-collapse instrument.
Extension (on merged main 9dd8c14): alpha_v 0.3 was the top edge, so the grid gains {1.0, 3.0};
if the winner is again the top edge it gains {10.0} once more and stops there regardless.
Also records the per-night `td_abs` instrument (mean |TD error| over night replay minibatches,
from each sleep_end event) for the "ac" and "q" arms.
A16 re-run (prereg addendum item 9): the earlier alpha_q rows ran under the uncentred-Q defect and
are VOID. q mode is now centred; alpha_q in {0.03, 0.1, 0.3} on BOTH arms exactly as 02_main.py
defines them (ebm-td; ebm-all = ebm-td + sign features). alpha_q is chosen by the mean of the two
arms' mean ticks_alive (declared in the addendum before this run). The ac rows are re-run unchanged.
Run (from the repo root): python experiments/02a_pilot_alpha.py
"""
import json, os
import numpy as np
from harness import run_arms, table, RESULTS
RUNS = "/tmp/ebm-runs"
B0 = {"policy": "ebm", "day_learning": True}
arms = {}
ALPHA_V = (0.01, 0.03, 0.1, 0.3, 1.0, 3.0)
for av in ALPHA_V:
    arms[f"ac-alpha_v{av}"] = {**B0, "learner": "ac", "alpha_v": av}
TD = {"policy": "ebm", "learner": "q", "day_learning": True, "brain.act_mode": "egreedy"}  # = 02_main.py
ALPHA_Q = (0.03, 0.1, 0.3)
for aq in ALPHA_Q:
    arms[f"ebm-td-alpha_q{aq}"] = {**TD, "alpha_q": aq}
    arms[f"ebm-all-alpha_q{aq}"] = {**TD, "sense.sign_features": True, "alpha_q": aq}
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
        ends = [json.loads(l) for l in open(ev) if '"sleep_end"' in l]
        life["night_td_abs"] = [e.get("td_abs") for e in ends]
    ents = [l["day0_wake_entropy"] for l in lives if l["day0_wake_entropy"] is not None]
    res["stats"][arm]["day0_wake_entropy"] = {"mean": float(np.mean(ents)) if ents else None,
                                              "n": len(ents), "values": ents}
    tds = [l["night_td_abs"] for l in lives if l["night_td_abs"] and l["night_td_abs"][0] is not None]
    if tds:   # mean over the lives still alive at each night index
        K = max(len(t) for t in tds)
        res["stats"][arm]["night_td_abs"] = {
            "per_night_mean": [float(np.mean([t[k] for t in tds if len(t) > k])) for k in range(K)],
            "per_night_n": [sum(len(t) > k for t in tds) for k in range(K)]}
CEIL = 15 * (300 + 50)        # a life that survives all 15 days and nights (censored)
for arm, lives in res["lives"].items():
    res["stats"][arm]["censored_at_ceiling"] = sum(l["ticks_alive"] == CEIL for l in lives)
    res["stats"][arm]["theta_nonfinite"] = sum(l.get("theta_finite") is False for l in lives)
sel = {}
for aq in ALPHA_Q:
    m_td = res["stats"][f"ebm-td-alpha_q{aq}"]["ticks_alive"]["mean"]
    m_all = res["stats"][f"ebm-all-alpha_q{aq}"]["ticks_alive"]["mean"]
    sel[str(aq)] = {"ebm-td": m_td, "ebm-all": m_all, "two_arm_mean": 0.5 * (m_td + m_all)}
res["alpha_q_selection"] = {"rule": "argmax over alpha_q of mean(mean ticks_alive ebm-td, ebm-all)",
                            "table": sel, "chosen": max(sel, key=lambda k: sel[k]["two_arm_mean"])}
json.dump(res, open(os.path.join(RESULTS, NAME, "results.json"), "w"), indent=1)
print(table(res))
print(f"{'arm':28s} day-0 end-of-day entropy (max ln3=1.099)")
for arm, st in res["stats"].items():
    e = st["day0_wake_entropy"]
    print(f"{arm:28s} mean={e['mean'] if e['mean'] is None else round(e['mean'], 3)} n={e['n']}  {e['values']}")
print(f"{'arm':28s} night td_abs, mean over lives alive at that night (n)")
for arm, st in res["stats"].items():
    if "night_td_abs" in st:
        t = st["night_td_abs"]
        print(f"{arm:28s} " + " ".join(f"{v:.4f}({n})" for v, n in zip(t["per_night_mean"], t["per_night_n"])))
print(f"{'arm':28s} censored@{CEIL}  theta_nonfinite")
for arm, st in res["stats"].items():
    print(f"{arm:28s} {st['censored_at_ceiling']:>4d}  {st['theta_nonfinite']:>4d}")
print("alpha_q selection:", json.dumps(res["alpha_q_selection"], indent=1))
