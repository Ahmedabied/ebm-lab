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
from creature.sim import Life, SimConfig, source_hash, git_commit, _cfg_dict

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
METRICS = ("ticks_alive", "days", "food", "poison", "mean_drive", "poison_bites_after_first")
# Seeds already looked at while tuning (EXP-00/01 pilots 0-7, EXP-02 alpha pilot 20-27, EXP-01 main
# 100-119) and the proof seeds of research/07 (300-339). A confirmatory run on any of them would not
# be a fresh test, so run_arms refuses them unless the experiment name marks it as a pilot.
BURNED = set(range(0, 8)) | set(range(20, 28)) | set(range(100, 120))
PROOF = set(range(300, 340))
PILOT_PREFIXES = ("00", "01", "02a")


def _apply(cfg, overrides: dict):
    """Overrides use dotted keys: {"policy": "ebm", "world.blend_mode": "xor", "brain.H0": 8}.
    A key whose final attribute is not a dataclass field of its target raises KeyError(k): a typo
    ("brain.act_mod") would otherwise silently add a dead attribute and run the default arm."""
    for k, v in overrides.items():
        obj = cfg; parts = k.split(".")
        for p in parts[:-1]:
            if not dataclasses.is_dataclass(obj) or p not in {f.name for f in dataclasses.fields(obj)}:
                raise KeyError(k)
            obj = getattr(obj, p)
        if not dataclasses.is_dataclass(obj) or parts[-1] not in {f.name for f in dataclasses.fields(obj)}:
            raise KeyError(k)
        setattr(obj, parts[-1], v)
    return cfg


def check_seeds(name: str, seeds):
    """Raise ValueError if a non-pilot experiment uses burned (tuning) or proof seeds."""
    if name.startswith(PILOT_PREFIXES): return
    bad = sorted(set(int(s) for s in seeds) & (BURNED | PROOF))
    if bad:
        raise ValueError(f"{name!r} uses burned/proof seeds {bad}; only pilots ({', '.join(PILOT_PREFIXES)}*) may")


def run_arms(name: str, arms: dict, seeds, days: int, runs_dir: str = "/tmp/ebm-runs",
             day_len: int = 300, world_overrides: dict | None = None, quiet=False) -> dict:
    seeds = list(seeds)
    check_seeds(name, seeds)
    out_dir = os.path.join(RESULTS, name); os.makedirs(out_dir, exist_ok=True)
    t0 = time.time()
    res = {"name": name, "command": " ".join(sys.argv), "commit": git_commit(),
           "source_hash": source_hash(), "seeds": list(seeds), "days": days, "day_len": day_len,
           "arms": {}, "configs": {}, "lives": {}}
    for arm, ov in arms.items():
        res["arms"][arm] = ov; res["lives"][arm] = []
        for s in seeds:
            cfg = SimConfig(seed=int(s), label=f"{name}_{arm}", days=days, day_len=day_len, runs_dir=runs_dir)
            _apply(cfg, {**(world_overrides or {}), **ov})
            if arm not in res["configs"]:     # full effective SimConfig (first seed), not just the overrides
                res["configs"][arm] = _cfg_dict(cfg)
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
