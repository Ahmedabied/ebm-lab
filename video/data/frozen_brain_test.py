"""Re-derive for the lesson, on fresh seeds (500-514, not in any burned set): take seed 203's
ebm-td brain as it was after night 4 (day-5 brain, run.json brain[4]), freeze it (no learning,
no sleep, no growth), and (a) let it live 15 fresh lives, (b) the same with mirrored antennae
(left <-> right swapped: every contrast flips sign). Same question findings/02 asked of the
referee reruns; this version is in the repo with its command.
Usage: uv run python video/data/frozen_brain_test.py > video/data/frozen_brain_test.json"""
import json, sys, os, numpy as np, subprocess
sys.path.insert(0, os.getcwd())
from dataclasses import replace
from creature.sim import Life, SimConfig
from creature.senses import Senses
from creature.brain import BrainConfig

run = json.load(open("runs/exp02-linear/203-ebm-td/run.json"))
snap = run["brain"][4]; assert snap["night"] == 4
theta = {k: np.array(snap[k], dtype=np.float64) for k in ("b", "w", "c", "u", "v")}
seeds = list(range(500, 515))
out = {"source_brain": "runs/exp02-linear/203-ebm-td/run.json brain[4] (after night 4 = day-5 brain)",
       "seeds": seeds, "days": 15, "arms": {}}
orig_ant = Senses.antennae
def mirrored(self, y, x, heading):
    L, R = orig_ant(self, y, x, heading); return R, L
for arm, mirror in (("frozen", False), ("frozen-mirrored", True)):
    Senses.antennae = mirrored if mirror else orig_ant
    lives = []
    for s in seeds:
        cfg = SimConfig(seed=s, label=f"lesson_{arm}", policy="ebm", days=15, learner="q", day_learning=False,
                        sleep="none", growth="none", runs_dir="/tmp/claude-1000/ebm-frozen",
                        brain=BrainConfig(dim=12, H0=4, T=0.3, init_scale=0.01))
        life = Life(cfg)
        life.brain.theta = {k: v.copy() for k, v in theta.items()}   # the day-5 brain, verbatim
        lives.append(life.run()["ticks_alive"])
    out["arms"][arm] = {"ticks_alive": lives, "mean": float(np.mean(lives)), "at_ceiling": int(sum(t == 5250 for t in lives))}
Senses.antennae = orig_ant
# birth brain (theta0, untrained) under the same frozen e-greedy rule, for the comparison the lesson makes
lives = []
for s in seeds:
    cfg = SimConfig(seed=s, label="lesson_birth", policy="ebm", days=15, learner="q", day_learning=False,
                    sleep="none", growth="none", runs_dir="/tmp/claude-1000/ebm-frozen",
                    brain=BrainConfig(dim=12, H0=4, T=0.3, init_scale=0.01))
    lives.append(Life(cfg).run()["ticks_alive"])
out["arms"]["birth-brain"] = {"ticks_alive": lives, "mean": float(np.mean(lives)), "at_ceiling": int(sum(t == 5250 for t in lives))}
out["commit"] = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()
out["command"] = "uv run python video/data/frozen_brain_test.py > video/data/frozen_brain_test.json"
print(json.dumps(out, indent=1))
