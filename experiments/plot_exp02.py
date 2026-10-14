"""Plots for EXP-02 from experiments/results/<prefix>_{linear,xor}/results.json. Headless (Agg); files only.
Writes experiments/results/02_main_ticks.png and 02_main_gap.png; with another --results-prefix
(smoke test) it writes smoke_exp02_<prefix>_{ticks,gap}.png instead (to --out-dir if given).
Run: uv run python experiments/plot_exp02.py
     uv run python experiments/plot_exp02.py --results-prefix 01_main --base ebm-nosleep \\
         --gap-arms ebm,ebm-nolearn,ebm-linear,oracle   (smoke test on EXP-01 data)"""
import os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from report_exp02 import R, ARMS, parse, load_worlds, present, gap_rows

P1_BAR, P2_BAR = 0.75, 0.4


def main(argv=None):
    args = parse(argv, __doc__, extra=[("--out-dir", dict(default=None))])
    worlds = load_worlds(args.results_prefix)
    if not worlds: sys.exit("no results files found")
    pre = args.results_prefix
    # Never overwrite another experiment's figures (01_main_ticks.png is EXP-01's): a non-02 prefix is a
    # smoke test and goes to <out-dir>/smoke_exp02_<prefix>_*.png.
    stem = "02_main" if pre == "02_main" else f"smoke_exp02_{pre}"
    out_dir = args.out_dir or R; os.makedirs(out_dir, exist_ok=True)
    arms = present(worlds, ARMS)
    r0 = next(iter(worlds.values()))
    stamp = f"commit {r0['commit']}, src {r0['source_hash']}, n={len(r0['seeds'])} seeds"

    # ---- ticks_alive per arm -------------------------------------------------------------------
    fig, axes = plt.subplots(1, len(worlds), figsize=(13, 0.45 * len(arms) + 2), sharey=True, squeeze=False)
    for ax, (w, res) in zip(axes[0], worlds.items()):
        st = res["stats"]
        ys = [i for i, a in enumerate(arms) if a in st]
        c = [st[arms[i]]["ticks_alive"] for i in ys]
        means = [x["mean"] for x in c]
        err = [[x["mean"] - x["lo"] for x in c], [x["hi"] - x["mean"] for x in c]]
        colors = ["#888" if not arms[i].startswith("ebm") else
                  ("#d9534f" if arms[i] in ("ebm-all", "ebm-td") else "#f0ad4e") for i in ys]
        ax.barh(ys, means, xerr=err, color=colors, capsize=3)
        for ref, col, ls in ((args.target, "#337ab7", "-"), (args.base, "#5cb85c", "--")):
            if ref in st:
                ax.axvline(st[ref]["ticks_alive"]["mean"], color=col, ls=ls, lw=1.2, label=f"{ref} mean")
        ax.set_yticks(range(len(arms))); ax.set_yticklabels(arms)
        ax.set_ylim(len(arms) - 0.5, -0.5)
        ax.set_title(f"{w} world  (mean, 95% bootstrap CI)"); ax.set_xlabel("ticks_alive")
        ax.grid(axis="x", alpha=0.3); ax.legend(loc="lower right", fontsize=8)
    fig.suptitle(f"{pre}: ticks alive per arm ({stamp})")
    fig.tight_layout(); out = os.path.join(out_dir, f"{stem}_ticks.png"); fig.savefig(out, dpi=120); plt.close(fig)
    print("wrote", out)

    # ---- gap fraction --------------------------------------------------------------------------
    gaps = gap_rows(worlds, args)
    garms = [a for a in args.gap_arms if any(a in gaps[w] for w in gaps)]
    fig, ax = plt.subplots(figsize=(9, 0.6 * max(len(garms), 1) + 2.2))
    h = 0.38; cols = {"linear": "#337ab7", "xor": "#d9534f"}
    for k, w in enumerate(worlds):
        ys, m, lo, hi = [], [], [], []
        for i, a in enumerate(garms):
            g = gaps[w].get(a)
            if g is None: continue
            ys.append(i + (k - 0.5) * h); m.append(g["mean"]); lo.append(g["mean"] - g["lo"]); hi.append(g["hi"] - g["mean"])
        ax.barh(ys, m, height=h, xerr=[lo, hi], color=cols.get(w, "#888"), capsize=3, label=f"{w} world")
    ax.axvline(0, color="k", ls="--", lw=1); ax.axvline(1, color="k", ls="--", lw=1)
    ax.axvline(P1_BAR, color="k", ls=":", lw=0.8); ax.axvline(P2_BAR, color="k", ls=":", lw=0.8)
    ax.text(P1_BAR, -0.75, "P1 0.75", fontsize=7, ha="center", va="bottom")
    ax.text(P2_BAR, -0.75, "P2 0.4", fontsize=7, ha="center", va="bottom")
    ax.set_yticks(range(len(garms))); ax.set_yticklabels(garms); ax.set_ylim(len(garms) - 0.5, -0.9)
    ax.set_xlabel(f"gap fraction G = (arm - {args.base}) / ({args.target} - {args.base}),  ticks_alive")
    ax.set_title(f"{pre}: gap fraction, paired bootstrap 95% CI ({stamp})", fontsize=10)
    ax.grid(axis="x", alpha=0.3); ax.legend(loc="best", fontsize=8)
    fig.tight_layout(); out = os.path.join(out_dir, f"{stem}_gap.png"); fig.savefig(out, dpi=120); plt.close(fig)
    print("wrote", out)


if __name__ == "__main__":
    main()
