"""Paired statistics over seeds for experiments whose arms share the same seed list.

Every arm in a results.json is run on the same seeds, so a life of arm A on seed s and a life of
arm B on seed s share the world layout and noise draws up to the point the policies diverge.
A PAIRED bootstrap resamples seed indices once per replicate and applies the same indices to every
arm, so the correlation between arms is kept and the CI of a contrast (difference, ratio) is not
inflated by between-seed variance the arms have in common.

    from stats import paired_bootstrap, gap_fraction, diff
    gap_fraction(res, "ebm-all")            # {"mean", "lo", "hi", "n", "n_boot"}
    diff(res, "ebm", "ebm-nolearn", "ticks_alive")
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


def paired_bootstrap(res: dict, metric: str, arms, fn, n_boot: int = 5000, seed: int = 0) -> dict:
    """Mean and 95% percentile CI of fn({arm: mean}) under a joint resample of seed indices.
    `mean` is fn on the full-sample means (the point estimate), not the bootstrap average."""
    arms = list(arms)
    X = _matrix(res, metric, arms)
    n = X.shape[1]
    rng = np.random.default_rng(seed)            # own RNG; never touches a run
    idx = rng.integers(0, n, size=(n_boot, n))   # one set of seed indices per replicate, shared by all arms
    boot_means = X[:, idx].mean(axis=2)          # (n_arms, n_boot)
    vals = np.array([fn({a: boot_means[i, b] for i, a in enumerate(arms)}) for b in range(n_boot)])
    point = fn({a: X[i].mean() for i, a in enumerate(arms)})
    finite = vals[np.isfinite(vals)]
    out = {"mean": float(point), "n": int(n), "n_boot": int(n_boot),
           "n_nonfinite": int(len(vals) - len(finite))}
    if len(finite):
        out["lo"] = float(np.percentile(finite, 2.5)); out["hi"] = float(np.percentile(finite, 97.5))
    else:
        out["lo"] = out["hi"] = float("nan")
    return out


def gap_fraction(res: dict, arm: str, base: str = "ebm-dn", target: str = "tabular_q",
                 metric: str = "ticks_alive", **kw) -> dict:
    """G(arm) = (mean(arm) - mean(base)) / (mean(target) - mean(base)), paired bootstrap CI.
    G = 0: no better than the baseline; G = 1: closes the whole gap to the target."""
    def g(m):
        den = m[target] - m[base]
        return (m[arm] - m[base]) / den if den != 0 else np.nan
    arms = [base, target] if arm in (base, target) else [base, target, arm]
    return paired_bootstrap(res, metric, arms, g, **kw)


def diff(res: dict, a: str, b: str, metric: str = "ticks_alive", **kw) -> dict:
    """Paired difference mean(a) - mean(b) with its bootstrap CI."""
    return paired_bootstrap(res, metric, [a, b], lambda m: m[a] - m[b], **kw)
