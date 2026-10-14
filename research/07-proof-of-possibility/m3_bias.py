"""M3 — MECHANISM: does within-life learning hurt by giving the creature a resting TURNING BIAS?

M2 showed the key gradient direction ("turn toward more A") has block-means SNR ≈ 2 per day with the
right sign in ~96% of creature-days. Yet EXP-01's learner lived LESS than no-learning. Hypothesis:
the same nightly update also moves ~100 other parameters by noise of comparable size, and any net
LEFT−RIGHT preference at a featureless sensation (a resting turning bias) traps the creature in loops
(pilot 01 / amendment A7 found exactly this for init_scale 0.1). Prediction: after night 1 the
learner's resting bias |π(LEFT|x0) − π(RIGHT|x0)| is far larger than the no-learning creature's, and
is negatively correlated with days survived.

x0 = the "nothing here" sensation: zero contrast, zero change, mean log level 0, body (E=0.5, X=0),
bias 1. Seeds 300–319 (proof seeds), EXP-01's `ebm` arm configuration (night-only replay), linear world.
Run from ~/ebm-lab:  .venv/bin/python research/07-proof-of-possibility/m3_bias.py
"""
import sys, os, json
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, "experiments"))
import numpy as np
from creature.sim import Life, SimConfig, git_commit, source_hash
from creature.brain import Brain, BrainConfig
from harness import ci

OUT = os.path.dirname(os.path.abspath(__file__))
SEEDS = list(range(300, 320))
X0 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0.5, 0.0, 1.0], dtype=np.float32)


def resting(theta, T=0.3):
    b = Brain(BrainConfig(dim=12, H0=theta["c"].shape[0], T=T), np.random.default_rng(0), theta)
    p = b.policy(X0[None, :])[0]
    return float(p[0] - p[1]), float(p[2])          # LEFT−RIGHT preference, FORWARD prob


def main():
    res = {"commit": git_commit(), "source_hash": source_hash(), "seeds": SEEDS, "lives": []}
    for arm, ov in (("ebm", {}), ("ebm-nolearn", {"sleep": "none", "growth": "none"})):
        for s in SEEDS:
            cfg = SimConfig(seed=s, label=f"m3_{arm}", policy="ebm", days=15, runs_dir="/tmp/ebm-runs/proof", **ov)
            L = Life(cfg); summ = L.run()
            nights = [resting(th) for th in L._brains]              # one snapshot per night survived
            res["lives"].append({"arm": arm, "seed": s, "days": summ["days"], "ticks": summ["ticks_alive"],
                                 "bias0": resting(Brain(cfg.brain, np.random.default_rng(s)).theta)[0],
                                 "bias_after_night": [n[0] for n in nights], "fwd_after_night": [n[1] for n in nights]})
    for arm in ("ebm", "ebm-nolearn"):
        L = [l for l in res["lives"] if l["arm"] == arm]
        b1 = [abs(l["bias_after_night"][0]) for l in L if len(l["bias_after_night"]) >= 1]
        bl = [abs(l["bias_after_night"][-1]) for l in L if l["bias_after_night"]]
        d = [l["days"] for l in L if l["bias_after_night"]]
        r = float(np.corrcoef(bl, d)[0, 1]) if len(bl) > 2 else None
        res[arm] = {"abs_bias_after_night1": ci(b1), "abs_bias_last_night": ci(bl), "corr_lastbias_days": r,
                    "days": ci([l["days"] for l in L]), "n_with_night": len(b1)}
        a = res[arm]
        print(f"{arm:12s} n={a['n_with_night']:2d} |bias| night1 {a['abs_bias_after_night1']['mean']:.3f} "
              f"[{a['abs_bias_after_night1']['lo']:.3f},{a['abs_bias_after_night1']['hi']:.3f}] | last night "
              f"{a['abs_bias_last_night']['mean']:.3f} | corr(|bias_last|, days) {r if r is None else round(r, 3)} | days {a['days']['mean']:.2f}")
    json.dump(res, open(os.path.join(OUT, "m3_bias.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
