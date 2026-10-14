"""Paired statistics over seeds for experiments whose arms share the same seed list.

Every arm in a results.json is run on the same seeds, so a life of arm A on seed s and a life of
arm B on seed s share the world layout and noise draws up to the point the policies diverge.
A PAIRED bootstrap resamples seed indices once per replicate and applies the same indices to every
arm, so the correlation between arms is kept and the CI of a contrast (difference, ratio) is not
inflated by between-seed variance the arms have in common.

    from stats import paired_bootstrap, gap_fraction, diff
    gap_fraction(res, "ebm-all")            # {"mean","lo","hi","n","n_boot","n_nonfinite","den","defined"}
    diff(res, "ebm", "ebm-nolearn", "ticks_alive")
    compare_gap(res, "ebm-dn-greedy", "ebm-dn-sign")       # ΔG = G_a - G_b, plus frac_a_gt_b
    cross_world(res_linear, res_xor, "ebm-dn-sign")        # ΔG = G_linear - G_xor (P4)
"""
import numpy as np


def _matrix(res: dict, metric: str, arms) -> np.ndarray:
    """(n_arms, n_seeds) array of the metric, after checking all arms share one seed order."""
    ref = None
    rows = []
    for a in arms:
        if a not in res["lives"]:
            raise KeyError(f"arm {a!r} not in results")
        lives = res["lives"][a]
        seeds = [l["seed"] for l in lives]
        if ref is None:
            ref = seeds
        elif seeds != ref:
            raise ValueError(f"seed lists differ between arms {arms[0]!r} and {a!r}: pairing is broken")
        rows.append([float(l[metric]) for l in lives])
    if len(ref) != len(set(ref)):
        raise ValueError("duplicate seeds within an arm")
    return np.array(rows, dtype=np.float64)


def _summ(point, vals, n, n_boot) -> dict:
    vals = np.asarray(vals, dtype=np.float64)
    finite = vals[np.isfinite(vals)]
    out = {"mean": float(point), "n": int(n), "n_boot": int(n_boot),
           "n_nonfinite": int(len(vals) - len(finite))}
    if len(finite):
        out["lo"] = float(np.percentile(finite, 2.5)); out["hi"] = float(np.percentile(finite, 97.5))
    else:
        out["lo"] = out["hi"] = float("nan")
    return out


def _boot(X: np.ndarray, n_boot: int, seed: int):
    """Bootstrap means (n_arms, n_boot) under one shared resample of seed indices per replicate."""
    n = X.shape[1]
    rng = np.random.default_rng(seed)            # own RNG; never touches a run
    idx = rng.integers(0, n, size=(n_boot, n))   # one set of seed indices per replicate, shared by all arms
    return X[:, idx].mean(axis=2)


def _replicates(res, metric, arms, fn, n_boot, seed):
    arms = list(arms)
    X = _matrix(res, metric, arms)
    bm = _boot(X, n_boot, seed)
    vals = np.array([fn({a: bm[i, b] for i, a in enumerate(arms)}) for b in range(n_boot)], dtype=np.float64)
    point = fn({a: X[i].mean() for i, a in enumerate(arms)})
    return point, vals, X.shape[1]


def paired_bootstrap(res: dict, metric: str, arms, fn, n_boot: int = 5000, seed: int = 0) -> dict:
    """Mean and 95% percentile CI of fn({arm: mean}) under a joint resample of seed indices.
    `mean` is fn on the full-sample means (the point estimate), not the bootstrap average.
    Non-finite replicates (e.g. a zero denominator) are dropped from the CI and counted in n_nonfinite."""
    point, vals, n = _replicates(res, metric, arms, fn, n_boot, seed)
    return _summ(point, vals, n, n_boot)


def _g(arm, base, target):
    def g(m):
        den = m[target] - m[base]
        return (m[arm] - m[base]) / den if den != 0 else np.nan
    return g


def _arms(base, target, *others):
    out = [base, target]
    for a in others:
        if a not in out: out.append(a)
    return out


def gap_fraction(res: dict, arm: str, base: str = "ebm-dn", target: str = "tabular_q",
                 metric: str = "ticks_alive", **kw) -> dict:
    """G(arm) = (mean(arm) - mean(base)) / (mean(target) - mean(base)), paired bootstrap CI.
    G = 0: no better than the baseline; G = 1: closes the whole gap to the target.
    Also returns `den`, the paired CI of the denominator mean(target) - mean(base), and
    `defined` = that CI excludes 0. When it does not, G is a ratio over a possibly-zero gap and its
    CI is meaningless (it can be arbitrarily wide or flip sign): report it as undefined."""
    out = paired_bootstrap(res, metric, _arms(base, target, arm), _g(arm, base, target), **kw)
    den = paired_bootstrap(res, metric, [base, target], lambda m: m[target] - m[base], **kw)
    out["den"] = den
    out["defined"] = bool(np.isfinite(den["lo"]) and (den["lo"] > 0 or den["hi"] < 0))
    return out


def compare_gap(res: dict, a: str, b: str, base: str = "ebm-dn", target: str = "tabular_q",
                metric: str = "ticks_alive", **kw) -> dict:
    """Paired bootstrap of ΔG = G(a) - G(b) = (mean(a) - mean(b)) / (mean(target) - mean(base)).
    All four arms are resampled with the same seed indices. `frac_a_gt_b` is the share of finite
    replicates with G(a) > G(b) (descriptive; not a p-value). With a negative denominator, G(a) > G(b)
    means a is CLOSER to the target, which is what the sign of ΔG reports too."""
    def dg(m):
        den = m[target] - m[base]
        return (m[a] - m[b]) / den if den != 0 else np.nan
    n_boot = kw.get("n_boot", 5000)
    point, vals, n = _replicates(res, metric, _arms(base, target, a, b), dg, n_boot, kw.get("seed", 0))
    out = _summ(point, vals, n, n_boot)
    fin = vals[np.isfinite(vals)]
    out["frac_a_gt_b"] = float(np.mean(fin > 0)) if len(fin) else float("nan")
    return out


def cross_world(res_linear: dict, res_xor: dict, arm: str, base: str = "ebm-dn",
                target: str = "tabular_q", metric: str = "ticks_alive", n_boot: int = 5000,
                seed: int = 0) -> dict:
    """P4: paired bootstrap of ΔG = G_linear(arm) - G_xor(arm). Both worlds were run on the same
    seed list, so seed s in linear and seed s in xor are joined and resampled together (one index
    set per replicate across both files). Asserts the seed lists are equal."""
    arms = _arms(base, target, arm)
    XL = _matrix(res_linear, metric, arms); XX = _matrix(res_xor, metric, arms)
    sl = [l["seed"] for l in res_linear["lives"][arms[0]]]
    sx = [l["seed"] for l in res_xor["lives"][arms[0]]]
    assert sl == sx, f"seed lists differ between worlds: {sl} vs {sx}"
    bm = _boot(np.vstack([XL, XX]), n_boot, seed)
    k = len(arms)
    g = _g(arm, base, target)
    vals = np.array([g({a: bm[i, b] for i, a in enumerate(arms)}) - g({a: bm[k + i, b] for i, a in enumerate(arms)})
                     for b in range(n_boot)], dtype=np.float64)
    gl = g({a: XL[i].mean() for i, a in enumerate(arms)}); gx = g({a: XX[i].mean() for i, a in enumerate(arms)})
    out = _summ(gl - gx, vals, XL.shape[1], n_boot)
    out["G_linear"] = float(gl); out["G_xor"] = float(gx)
    return out


def diff(res: dict, a: str, b: str, metric: str = "ticks_alive", **kw) -> dict:
    """Paired difference mean(a) - mean(b) with its bootstrap CI."""
    return paired_bootstrap(res, metric, [a, b], lambda m: m[a] - m[b], **kw)
