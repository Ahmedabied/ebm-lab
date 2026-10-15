"""Replay one recorded life bit-for-bit (law: determinism per seed) and dump what run.json does not
keep: the full sensation x per waking tick, Q(x,·) = -F, the greedy action, the TD target, the fields.
Usage: uv run python video/data/extract_life.py runs/exp02-linear/203-ebm-td/run.json video/data/life203.npz
Checks the replay's summary against the recorded one before writing anything."""
import json, sys, os, numpy as np
sys.path.insert(0, os.getcwd())
from dataclasses import fields as dc_fields
from creature.sim import Life, SimConfig
from creature.world import WorldConfig
from creature.body import BodyConfig
from creature.senses import SenseConfig
from creature.brain import BrainConfig

src, dst = sys.argv[1], sys.argv[2]
run = json.load(open(src)); cfgd = run["meta"]["config"]

def build(cls, d):
    names = {f.name for f in dc_fields(cls)}
    return cls(**{k: v for k, v in d.items() if k in names})

cfg = build(SimConfig, {k: v for k, v in cfgd.items() if k not in ("world", "body", "sense", "brain", "input_names")})
cfg.world = build(WorldConfig, cfgd["world"]); cfg.body = build(BodyConfig, cfgd["body"])
cfg.sense = build(SenseConfig, cfgd["sense"])
bcfg = dict(cfgd["brain"]); bcfg.pop("centre", None); bcfg.pop("act_mode", None)   # Life sets these
cfg.brain = build(BrainConfig, bcfg)
cfg.runs_dir = "/tmp/claude-1000/ebm-replay"

life = Life(cfg)
rec = {"t": [], "x": [], "Q": [], "a": [], "greedy": [], "r": [], "E": [], "X": [], "D": [], "y": [], "xpos": [], "h": [],
       "y_target": [], "td": [], "fields": [], "food": [], "poison": [], "theta0": life.brain.snapshot()}
orig_sense = life.senses.sense
state = {}
def sense_hook(*a, **k):
    out = orig_sense(*a, **k); state["x"] = out["x"].copy(); state["sens"] = out; return out
life.senses.sense = sense_hook
orig_act = life.brain.act
def act_hook(x, rng):
    Fx_before = life.brain.F(x[None, :])[0].copy()
    a, Fx, lp = orig_act(x, rng)
    state["Q"] = -Fx_before; state["a"] = a; state["greedy"] = int(np.argmin(Fx_before)); return a, Fx, lp
life.brain.act = act_hook
orig_learnq = life.brain.learn_q
def learnq_hook(X, a, y, alpha):
    if X.shape[0] == 1:            # the online step (one transition); nights use batches
        state["y_target"] = float(np.asarray(y)[0]); state["td"] = float(np.asarray(y)[0] - life.brain.Q(X)[0, int(np.asarray(a)[0])])
    return orig_learnq(X, a, y, alpha)
life.brain.learn_q = learnq_hook
orig_eat = life.world.eat_at
def eat_hook(y, x):
    f, p = orig_eat(y, x); state["food"] = f; state["poison"] = p; return f, p
life.world.eat_at = eat_hook
orig_wake = life.wake_tick
def wake_hook():
    t = life.t; E0 = life.body.E
    rec["fields"].append(life.world.fields.astype(np.float16).copy())
    orig_wake()
    rec["t"].append(t); rec["x"].append(state["x"]); rec["Q"].append(state["Q"]); rec["a"].append(state["a"])
    rec["greedy"].append(state["greedy"]); rec["food"].append(state["food"]); rec["poison"].append(state["poison"])
    rec["E"].append(life.body.E); rec["X"].append(life.body.X); rec["D"].append(life.body.drive())
    rec["y"].append(life.y); rec["xpos"].append(life.x); rec["h"].append(life.heading)
    # the online TD step for tick t happens at tick t+1 (needs x_next); record what is known so far
    rec["y_target"].append(state.get("y_target", np.nan)); rec["td"].append(state.get("td", np.nan))
    for k, v in life.brain.theta.items(): rec.setdefault("theta_" + k, []).append(v.copy())
life.wake_tick = wake_hook
summary = life.run()
recorded = run["meta"]["summary"]
ok = all(abs(float(summary[k]) - float(recorded[k])) < 1e-9 for k in ("ticks_alive", "food", "poison", "mean_drive"))
print("replay summary", summary); print("recorded      ", recorded); print("MATCH" if ok else "MISMATCH")
if not ok: sys.exit(1)
ticks = run["ticks"]
# r in run.json is per tick (wake+sleep); compare the wake ticks' r
r_rec = [ticks["r"][i] for i in rec["t"]]
rec["r"] = r_rec
# shift the online TD record: y_target recorded at wake t+1 belongs to transition t
out = {k: np.array(v) for k, v in rec.items() if k not in ("theta0", "fields") and not k.startswith("theta_")}
for k in [k for k in rec if k.startswith("theta_")]:
    arrs = rec[k]; Hmax = max(a.shape[0] for a in arrs) if k in ("theta_c", "theta_u", "theta_v") else None
    if Hmax is None:
        out[k] = np.array(arrs, dtype=np.float32)
    else:   # H grows at night (4 -> 5 here): pad the missing unit with NaN so the array is rectangular
        padded = np.full((len(arrs), Hmax) + arrs[0].shape[1:], np.nan, dtype=np.float32)
        for i, a in enumerate(arrs): padded[i, :a.shape[0]] = a
        out[k] = padded
out["fields"] = np.array(rec["fields"])
for k, v in rec["theta0"].items(): out["theta0_" + k] = v
out["input_names"] = np.array(run["input_names"])
np.savez_compressed(dst, **out)
print("wrote", dst, {k: out[k].shape for k in ("x", "Q", "fields")})
