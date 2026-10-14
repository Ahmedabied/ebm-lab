"""M2 — SIGNAL-TO-NOISE of the policy gradient the body gives an untrained creature.

The learning rule moves theta by the batch mean of d_i = R_i · ∂log π(a_i|x_i)/∂θ. For the one
weight direction that matters most in the linear world, "turn toward the side with more A"
(w[LEFT,cA] − w[RIGHT,cA]), we measure over a day of an UNTRAINED creature:
    mu = E[d_i], sd = std(d_i), N = samples per day
    SNR_day = mu·sqrt(N)/sd        (the day's batch-mean estimate, in standard errors)
    days_needed(SNR=3) = (3·sd / (mu·sqrt(N)))^2
This is a plain sample-size calculation. If days_needed is far above the 3–4 days an untrained
creature survives, EXP-01's failure is a sample-complexity fact, not a bug. We also report the
sign of mu (is the expected update even in the right direction?) and the same for the C-aversion
direction. Days are taken from the first 3 days of a no-learning life (what the learner actually sees).

Seeds 300-319 (the proof seeds). Run from ~/ebm-lab:
    .venv/bin/python research/07-proof-of-possibility/m2_snr.py
"""
import sys, os, json
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, "experiments"))
import numpy as np
from creature.sim import Life, SimConfig, git_commit, source_hash
from harness import ci

OUT = os.path.dirname(os.path.abspath(__file__))
LEFT, RIGHT = 0, 1
SEEDS = list(range(300, 320))


def day_samples(seed, blend, days=3):
    cfg = SimConfig(seed=seed, label=f"m2_{blend}", policy="ebm", days=days, runs_dir="/tmp/ebm-runs/proof",
                    sleep="none", growth="none", day_learning=False, cache_days=days)
    cfg.world.blend_mode = blend
    L = Life(cfg); L.run()
    return L.brain, L.cache.days          # [(X, a, R, lp)] per day survived


def main():
    res = {"commit": git_commit(), "source_hash": source_hash(), "seeds": SEEDS, "per_day": []}
    for blend in ("linear", "xor"):
        rows = []
        for s in SEEDS:
            brain, days = day_samples(s, blend)
            for d, (X, a, R, lp) in enumerate(days):
                if len(a) < 10: continue
                g = brain.grad_logpi(X, a)["w"]                       # (N, A, dim)
                dA = R * (g[:, LEFT, 0] - g[:, RIGHT, 0])             # toward more A
                dC = R * (g[:, LEFT, 2] - g[:, RIGHT, 2])             # toward more C (should be <0)
                N = len(a)
                row = {"seed": s, "day": d, "N": N}
                for name, dd in (("A", dA), ("C", dC)):
                    mu, sd = float(dd.mean()), float(dd.std())
                    snr = mu * np.sqrt(N) / sd if sd > 0 else 0.0
                    # The lessons R_t are λ-credited sums (λ = 0.95 → ~20-tick memory), so consecutive
                    # d_i are NOT independent and sd/sqrt(N) understates the standard error. Batch-means
                    # estimate: split the day into blocks of B ticks, se = std(block means)/sqrt(m).
                    B = 30; m = N // B
                    if m >= 3:
                        bm = dd[:m * B].reshape(m, B).mean(axis=1)
                        se_block = float(bm.std(ddof=1) / np.sqrt(m)); snr_block = mu / se_block if se_block > 0 else 0.0
                    else:
                        se_block = None; snr_block = None
                    row[name] = {"mu": mu, "sd": sd, "snr_day": float(snr),
                                 "snr_block": snr_block, "n_blocks": m,
                                 "days_for_snr3": float((3 * se_block / abs(mu)) ** 2) if (se_block and mu != 0) else None}
                row["meals"] = int((np.abs(R) > 2.0).sum())             # big lessons (standardised)
                rows.append(row)
        res["per_day"] += [{"blend": blend, **r} for r in rows]
        rows = [r for r in rows if r["A"]["snr_block"] is not None]
        snrA = [r["A"]["snr_day"] for r in rows]; muA = [r["A"]["mu"] for r in rows]
        snrAb = [r["A"]["snr_block"] for r in rows]; snrCb = [r["C"]["snr_block"] for r in rows]
        daysA = [r["A"]["days_for_snr3"] for r in rows if r["A"]["days_for_snr3"] is not None]
        res[blend] = {"n_days": len(rows), "snr_A_iid": ci(snrA), "snr_A_block": ci(snrAb),
                      "mu_A_positive_frac": float(np.mean(np.array(muA) > 0)),
                      "snr_C_block": ci(snrCb), "days_for_snr3_A_median": float(np.median(daysA)),
                      "days_for_snr3_A_q25_q75": [float(np.percentile(daysA, 25)), float(np.percentile(daysA, 75))],
                      "frac_days_snr_block_gt2": float(np.mean(np.array(snrAb) > 2))}
        b = res[blend]
        print(f"{blend}: {b['n_days']} creature-days | SNR_A iid {b['snr_A_iid']['mean']:.2f} | SNR_A block-means "
              f"{b['snr_A_block']['mean']:.2f} [{b['snr_A_block']['lo']:.2f},{b['snr_A_block']['hi']:.2f}] | "
              f"mu_A>0 in {100*b['mu_A_positive_frac']:.0f}% of days | days with block-SNR>2: {100*b['frac_days_snr_block_gt2']:.0f}% | "
              f"days for SNR 3 (block): median {b['days_for_snr3_A_median']:.0f} (IQR {b['days_for_snr3_A_q25_q75'][0]:.0f}-{b['days_for_snr3_A_q25_q75'][1]:.0f}) | "
              f"SNR_C block {b['snr_C_block']['mean']:.2f}")
    json.dump(res, open(os.path.join(OUT, "m2_snr.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
