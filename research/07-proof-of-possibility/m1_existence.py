"""M1 — EXISTENCE: does the EBM's model class contain a foraging solution at all?

(a) By construction (linear world): hand-set weights that implement Braitenberg inside F(x,a):
        -F(x,a) = w_a·x + b_a,  w[LEFT,cA] = +k, w[RIGHT,cA] = -k, w[LEFT,cC] = -k, w[RIGHT,cC] = +k,
        b[FORWARD] = beta  (go straight when the contrast is small).
    No learning, no growth, no sleep: the policy is frozen. If this lives as long as Braitenberg,
    the class contains the linear solution and EXP-01's failure is learning, not capacity.
(b) By search (both worlds): an evolution strategy over theta (H=4 hidden units) with fitness =
    mean ticks_alive on SEARCH seeds 300-303; the best theta is then evaluated on HELD-OUT seeds
    320-339. If search finds a theta that matches tabular Q in the xor world, the class can express
    the conjunction "A and B together" with 4 units.

Seeds 300-339 are declared here for the proof and are not used for tuning any learner.
Run from ~/ebm-lab:  .venv/bin/python research/07-proof-of-possibility/m1_existence.py [construct|search]
"""
import sys, os, json, time
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, "experiments"))
import numpy as np
from creature.sim import Life, SimConfig, git_commit, source_hash
from creature.brain import A
from harness import ci

OUT = os.path.dirname(os.path.abspath(__file__))
RUNS = "/tmp/ebm-runs/proof"
LEFT, RIGHT, FORWARD = 0, 1, 2
HELD = list(range(320, 340))
SEARCH = [300, 301, 302, 303]


def life(seed, blend, theta=None, policy="ebm", H0=4, days=15):
    cfg = SimConfig(seed=seed, label=f"m1_{blend}_{policy}", policy=policy, days=days, runs_dir=RUNS,
                    sleep="none", growth="none", day_learning=False)
    cfg.world.blend_mode = blend; cfg.brain.H0 = H0
    L = Life(cfg)
    if theta is not None:
        L.brain.theta = {k: np.array(v, dtype=np.float64).copy() for k, v in theta.items()}
    return L.run()


def braitenberg_theta(k, beta, dim=12, H=0):
    w = np.zeros((A, dim)); b = np.zeros(A)
    w[LEFT, 0] = +k; w[RIGHT, 0] = -k          # toward the side with more A
    w[LEFT, 2] = -k; w[RIGHT, 2] = +k          # away from the side with more C
    b[FORWARD] = beta
    return {"b": b, "w": w, "c": np.zeros(H), "u": np.zeros((H, dim)), "v": np.zeros((H, A))}


def construct():
    res = {"commit": git_commit(), "source_hash": source_hash(), "seeds": HELD, "arms": {}}
    arms = {"braitenberg": ("braitenberg", None)}
    for k in (3.0, 10.0, 30.0):
        arms[f"ebm-handset-k{k:g}"] = ("ebm", braitenberg_theta(k, 0.05 * k))
    arms["ebm-untrained"] = ("ebm", None)
    for blend in ("linear", "xor"):
        for name, (pol, th) in arms.items():
            ticks = []; food = []; poison = []
            for s in HELD:
                summ = life(s, blend, th, policy=pol, H0=0 if th is not None else 4)
                ticks.append(summ["ticks_alive"]); food.append(summ["food"]); poison.append(summ["poison"])
            res["arms"][f"{blend}/{name}"] = {"ticks": ci(ticks), "food": ci(food), "poison": ci(poison)}
            t = res["arms"][f"{blend}/{name}"]["ticks"]
            print(f"{blend:6s} {name:20s} ticks {t['mean']:7.1f} [{t['lo']:7.1f},{t['hi']:7.1f}]  food {np.mean(food):5.2f}  poison {np.mean(poison):5.2f}", flush=True)
    json.dump(res, open(os.path.join(OUT, "m1_construct.json"), "w"), indent=1)


def flat(theta):
    return np.concatenate([theta[k].ravel() for k in ("b", "w", "c", "u", "v")])


def unflat(z, dim=12, H=4):
    i = 0; th = {}
    for k, shp in (("b", (A,)), ("w", (A, dim)), ("c", (H,)), ("u", (H, dim)), ("v", (H, A))):
        n = int(np.prod(shp)); th[k] = z[i:i + n].reshape(shp); i += n
    return th


def fitness(z, blend, seeds):
    th = unflat(z)
    return float(np.mean([life(s, blend, th, days=15)["ticks_alive"] for s in seeds]))


def search(blend, gens=40, pop=24, elite=6, sigma=0.5, seed=7):
    """(mu, lambda)-ES with per-coordinate sigma adaptation. Search RNG is its own."""
    rng = np.random.default_rng(seed)
    dim = len(flat(unflat(np.zeros(3 + 36 + 4 + 48 + 12))))
    mean = np.zeros(dim); sig = np.full(dim, sigma)
    best = (-1, None); log = []
    t0 = time.time()
    for g in range(gens):
        Z = mean[None, :] + sig[None, :] * rng.normal(size=(pop, dim))
        f = np.array([fitness(z, blend, SEARCH) for z in Z])
        order = np.argsort(-f); E = Z[order[:elite]]
        mean = E.mean(axis=0); sig = 0.9 * sig + 0.1 * E.std(axis=0) + 1e-3
        if f[order[0]] > best[0]: best = (float(f[order[0]]), Z[order[0]].copy())
        log.append({"gen": g, "best": float(f[order[0]]), "mean": float(f.mean()), "sig": float(sig.mean())})
        print(f"{blend} gen {g:3d} best {f[order[0]]:7.1f} mean {f.mean():7.1f} sig {sig.mean():.3f} "
              f"all-time {best[0]:7.1f} ({time.time()-t0:.0f}s)", flush=True)
    th = unflat(best[1])
    held = [life(s, blend, th)["ticks_alive"] for s in HELD]
    heldf = [life(s, blend, th)["food"] for s in HELD[:5]]
    out = {"blend": blend, "commit": git_commit(), "source_hash": source_hash(), "search_seeds": SEARCH,
           "held_seeds": HELD, "search_best": best[0], "held": ci(held), "held_food_first5": heldf,
           "log": log, "theta": {k: v.tolist() for k, v in th.items()}}
    json.dump(out, open(os.path.join(OUT, f"m1_search_{blend}.json"), "w"), indent=1)
    print(f"{blend} HELD-OUT ticks {out['held']['mean']:.1f} [{out['held']['lo']:.1f},{out['held']['hi']:.1f}]")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "construct"
    if mode == "construct": construct()
    else: search(sys.argv[2] if len(sys.argv) > 2 else "xor")
