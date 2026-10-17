"""Re-live seed 203's ebm-td life in each world (same config as EXP-02 main, read from its meta.json),
check the re-run matches the recorded life, and save the brain it ends with at full precision.
Usage: uv run python weights/export_weights.py"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.getcwd())
from creature.sim import Life, SimConfig
from creature.world import WorldConfig
from creature.body import BodyConfig
from creature.senses import SenseConfig
from creature.brain import BrainConfig

def config(d):
    d = dict(d); d.pop("input_names", None)
    d["world"], d["body"] = WorldConfig(**d["world"]), BodyConfig(**d["body"])
    d["sense"], d["brain"] = SenseConfig(**d["sense"]), BrainConfig(**d["brain"])
    d["runs_dir"] = "/tmp/ebm-runs/export"
    return SimConfig(**d)

def main():
    for world in ("linear", "xor"):
        meta = json.load(open(f"runs/exp02-{world}/203-ebm-td/meta.json"))
        life = Life(config(meta["config"]))
        s = life.run()
        for k in ("ticks_alive", "food", "poison", "H"):
            assert s[k] == meta["summary"][k], (world, k, s[k], meta["summary"][k])
        out = f"weights/ebm-td_{world}_seed203_final.npz"
        np.savez(out, **life.brain.theta)
        json.dump({"source": f"runs/exp02-{world}/203-ebm-td (re-run, summary matches the recorded life)",
                   "summary": s, "brain": meta["config"]["brain"],
                   "input_names": meta["config"]["input_names"],
                   "shapes": {k: list(v.shape) for k, v in life.brain.theta.items()}},
                  open(out.replace(".npz", ".json"), "w"), indent=1)
        print(world, s)


if __name__ == "__main__":
    main()
