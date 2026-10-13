"""Experiment harness: arms × seeds → one results.json with every life's summary, the arm
configs, bootstrap CIs, the commit and the source hash. Every number in findings/ comes from a
file this writes, and the file names the command that wrote it.

Usage from an experiment script:
    from harness import run_arms, table
    res = run_arms("01_pilot", arms={"random": {"policy": "random"}, ...}, seeds=range(8), days=15)
    print(table(res))
"""
import json, os, sys, time, dataclasses
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from creature.sim import Life, SimConfig, source_hash, git_commit

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
METRICS = ("ticks_alive", "days", "food", "poison", "mean_drive", "poison_bites_after_first")


def _apply(cfg, overrides: dict):
    """Overrides use dotted keys: {"policy": "ebm", "world.blend_mode": "xor", "brain.H0": 8}."""
    for k, v in overrides.items():
        obj = cfg; parts = k.split(".")
        for p in parts[:-1]: obj = getattr(obj, p)
        setattr(obj, parts[-1], v)
    return cfg


def run_arms(name: str, arms: dict, seeds, days: int, runs_dir: str = "/tmp/ebm-runs",
             day_len: int = 300, world_overrides: dict | None = None, quiet=False) -> dict:
    out_dir = os.path.join(RESULTS, name); os.makedirs(out_dir, exist_ok=True)
    t0 = time.time()
    res = {"name": name, "command": " ".join(sys.argv), "commit": git_commit(),
           "source_hash": source_hash(), "seeds": list(seeds), "days": days, "day_len": day_len,
           "arms": {}, "lives": {}}
    for arm, ov in arms.items():
        res["arms"][arm] = ov; res["lives"][arm] = []
        for s in seeds:
            cfg = SimConfig(seed=int(s), label=f"{name}_{arm}", days=days, day_len=day_len, runs_dir=runs_dir)
            _apply(cfg, {**(world_overrides or {}), **ov})
            summ = Life(cfg).run(); summ["seed"] = int(s)
            res["lives"][arm].append(summ)
        if not quiet:
            print(f"  {arm:28s} " + "  ".join(f"{m}={np.mean([l[m] for l in res['lives'][arm]]):.3f}" for m in ("ticks_alive", "food", "poison")))
    res["seconds"] = round(time.time() - t0, 1)
    res["stats"] = {arm: {m: ci([l[m] for l in lives]) for m in METRICS} for arm, lives in res["lives"].items()}
    json.dump(res, open(os.path.join(out_dir, "results.json"), "w"), indent=1)
    return res


def ci(xs, n_boot=2000, seed=0) -> dict:
    """Mean with a 95% bootstrap CI. The bootstrap RNG is its own; it never touches a run."""
    xs = np.array(xs, dtype=np.float64); rng = np.random.default_rng(seed)
    if len(xs) == 0: return {"mean": None}
    boots = np.array([rng.choice(xs, len(xs)).mean() for _ in range(n_boot)])
    return {"mean": float(xs.mean()), "lo": float(np.percentile(boots, 2.5)),
            "hi": float(np.percentile(boots, 97.5)), "n": int(len(xs)), "median": float(np.median(xs))}


def table(res: dict, metrics=("ticks_alive", "food", "poison", "mean_drive")) -> str:
    lines = [f"{res['name']}  seeds={len(res['seeds'])} days={res['days']} commit={res['commit']} src={res['source_hash']}",
             f"{'arm':28s} " + " ".join(f"{m:>26s}" for m in metrics)]
    for arm, st in res["stats"].items():
        cells = []
        for m in metrics:
            c = st[m]; cells.append(f"{c['mean']:9.3f} [{c['lo']:8.3f},{c['hi']:8.3f}]")
        lines.append(f"{arm:28s} " + " ".join(cells))
    return "\n".join(lines)
