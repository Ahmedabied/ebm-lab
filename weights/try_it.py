"""Drop a trained brain into a fresh world and watch it live.

    uv run python weights/try_it.py                       # linear world, seed 9000, brain frozen
    uv run python weights/try_it.py --world xor --seed 9001
    uv run python weights/try_it.py --learn               # let it keep learning (EXP-02 rules)

The brain is the one seed 203's creature ended its 15-day life with (EXP-02, arm ebm-td).
Frozen = no learning, no sleep, no growth: the weights alone decide every move (epsilon-greedy,
eps 0.1). Prints the life's summary and writes a run.json the browser viewer can play.
Seeds you pick here are a demo, not part of the lab's record."""
import argparse, json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from creature.sim import Life
from creature.export import export
from export_weights import config

p = argparse.ArgumentParser()
p.add_argument("--world", choices=("linear", "xor"), default="linear")
p.add_argument("--seed", type=int, default=9000)
p.add_argument("--days", type=int, default=15)
p.add_argument("--learn", action="store_true", help="keep learning from these weights")
a = p.parse_args()

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
os.chdir(root)
meta = json.load(open(f"runs/exp02-{a.world}/203-ebm-td/meta.json"))
cfg = config(meta["config"])
cfg.seed, cfg.days, cfg.runs_dir = a.seed, a.days, "runs/try_it"
cfg.label = f"{a.world}-{'learn' if a.learn else 'frozen'}"
if not a.learn:
    cfg.day_learning, cfg.sleep, cfg.growth = False, "none", "none"
life = Life(cfg)
z = np.load(os.path.join(here, f"ebm-td_{a.world}_seed203_final.npz"))
life.brain.theta = {k: z[k].astype(np.float64).copy() for k in z.files}
s = life.run()
print(json.dumps(s, indent=1))
export(life.dir)
print(f"\nwatch it:  uv run python -m http.server 8765   then open\n"
      f"  http://localhost:8765/viewer/?run={life.dir}/run.json")
