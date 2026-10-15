"""Readers for the lab's real files. Nothing here invents a number; every function says where it reads.
All paths are relative to the lab root (~/ebm-lab)."""
import os, json, functools, numpy as np
LAB = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
P = lambda *a: os.path.join(LAB, *a)
LIFE_NPZ = P("video", "data", "life203.npz")                       # replay dump of runs/exp02-linear/203-ebm-td
RUN_JSON = P("runs", "exp02-linear", "203-ebm-td", "run.json")
RES02 = P("experiments", "results", "02_main_linear", "results.json")
RES01 = P("experiments", "results", "01_main_linear", "results.json")
FROZEN = P("video", "data", "frozen_brain_test.json")
M3 = P("research", "07-proof-of-possibility", "m3_bias.json")
PROVENANCE = []     # (label, file, field, value) appended by scenes via note()


def note(label, file, field, value):
    PROVENANCE.append((label, os.path.relpath(file, LAB), field, value))


@functools.lru_cache(None)
def life():
    d = np.load(LIFE_NPZ, allow_pickle=True)
    out = {k: d[k] for k in d.files}
    out["input_names"] = [str(s) for s in out["input_names"]]
    return out


@functools.lru_cache(None)
def run():
    return json.load(open(RUN_JSON))


@functools.lru_cache(None)
def results(which="02"):
    return json.load(open(RES02 if which == "02" else RES01))


@functools.lru_cache(None)
def frozen():
    return json.load(open(FROZEN))


@functools.lru_cache(None)
def m3():
    return json.load(open(M3))


def arm_stats(arm, which="02", metric="ticks_alive"):
    s = results(which)["stats"][arm][metric]
    return s["mean"], s["lo"], s["hi"]


def nightly_w():
    """(nights, 3, 12) weight matrix after each night, from run.json brain[]."""
    return np.array([np.array(s["w"]) for s in run()["brain"]])


def field_rgb(f, C0=0.01, VMAX=0.3):
    """The viewer's colour rule (run.json fields.scale): A->red, B->green, C->blue, log-scaled."""
    f = np.asarray(f, dtype=np.float32)
    v = np.log1p(np.clip(f, 0, None) / C0) / np.log1p(VMAX / C0)
    v = np.clip(v, 0, 1)
    return (np.transpose(v, (1, 2, 0)) * 255).astype(np.uint8)


def softmax(q, T):
    z = np.asarray(q, dtype=np.float64) / T; z = z - z.max(); p = np.exp(z); return p / p.sum()


def softplus(z):
    return np.logaddexp(0.0, z)


def F_of(theta, x, centre=True):
    """F(x, a) exactly as creature/brain.py computes it (kept here so a scene can recompute from
    weights it shows). theta: dict b (3,), w (3,12), c (H,), u (H,12), v (H,3)."""
    x = np.asarray(x, dtype=np.float64)
    pre = theta["c"][:, None] + (theta["u"] @ x)[:, None] + theta["v"]          # (H, A)
    F = -theta["b"] - theta["w"] @ x - softplus(pre).sum(axis=0)
    if centre: F = F + theta["c"].shape[0] * np.log(2.0)
    return F


def theta_at(i):
    """Weights the brain USED to act at waking index i (the online step for transition i-1 is applied at
    the start of wake_tick(i), before acting; the dump records theta after wake_tick(i)). NaN rows = unit not born."""
    L = life(); th = {}
    for k in ("b", "w", "c", "u", "v"):
        a = L["theta_" + k][i]
        if k in ("c", "u", "v"):
            m = ~np.isnan(a if a.ndim == 1 else a[:, 0]); a = a[m]
        th[k] = np.asarray(a, dtype=np.float64)
    return th
